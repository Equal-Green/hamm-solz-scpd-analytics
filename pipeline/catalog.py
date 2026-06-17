"""Profile every tabular file in the INFORMACIÓN folder into a data_catalog
table: folder, file, sheet, column model, and row counts.

Reuses the streaming-ZIP machinery in extract.py. The four large SCPD sheets
reuse their known row counts (config) instead of re-parsing ~450 MB of XML each;
every other sheet gets a fast SAX row-count.
"""
import io
import mmap
import struct
import xml.etree.ElementTree as ET
import xml.sax
import zipfile
from datetime import datetime

from config import FILES, ZIP_PATH
from pipeline.extract import (
    LOCAL, _u16, _u32, _col_to_index, _inner_zip_length,
    _strip_ns, load_shared_strings,
)

CATALOG_SCHEMA = """
CREATE TABLE IF NOT EXISTS data_catalog (
    id INTEGER,
    folder VARCHAR,
    file_name VARCHAR,
    file_path VARCHAR,
    file_type VARCHAR,
    size_mb DOUBLE,
    sheet_name VARCHAR,
    n_columns INTEGER,
    n_rows INTEGER,
    columns VARCHAR,
    loaded_table VARCHAR,
    profiled_at TIMESTAMP
);
"""

# (filename match, sheet name) -> known total row count (header + data), and the
# DuckDB table it was loaded into. Avoids re-parsing the giant SCPD sheets.
_KNOWN = {}
for _spec in FILES:
    _KNOWN[(_spec["match"], _spec["sheet"])] = {
        "rows": _spec["expected_rows"] + _spec["header_row"],  # +title/header rows
        "table": _spec["table"],
    }


class _Profiler(xml.sax.ContentHandler):
    """Counts <row> elements and captures the first 'meaningful' row (>=2
    non-empty cells) as the column header. Set stop_after_header to bail out
    early when the row count is already known."""

    def __init__(self, shared, stop_after_header=False):
        self.shared = shared
        self.stop_after_header = stop_after_header
        self.nrows = 0
        self.header = None
        self.cells = {}
        self.cur_idx = -1
        self.t = ""
        self.val = []
        self.inv = False

    def startElement(self, name, attrs):
        if name == "row":
            self.nrows += 1
            self.cells = {}
        elif name == "c":
            ref = attrs.get("r")
            self.cur_idx = _col_to_index(ref) if ref else self.cur_idx + 1
            self.t = attrs.get("t", "")
            self.val = []
        elif name == "v":
            self.inv = True
            self.val = []
        elif name == "t" and self.t == "inlineStr":
            self.inv = True
            self.val = []

    def characters(self, content):
        if self.inv:
            self.val.append(content)

    def endElement(self, name):
        if name in ("v", "t") and self.inv:
            self.inv = False
            v = "".join(self.val)
            if name == "v" and self.t == "s":
                try:
                    v = self.shared[int(v)]
                except (ValueError, IndexError):
                    pass
            self.cells[self.cur_idx] = v
        elif name == "row":
            if self.header is None:
                nonempty = [self.cells[i] for i in sorted(self.cells)
                            if str(self.cells.get(i, "")).strip()]
                if len(nonempty) >= 2:
                    self.header = [str(self.cells.get(i, "")).strip()
                                   for i in range(max(self.cells) + 1)]
                    if self.stop_after_header:
                        raise StopIteration


def _list_sheets(zf):
    """Return [(sheet_name, xml_path)] for every worksheet in the workbook."""
    wb = ET.fromstring(zf.read("xl/workbook.xml"))
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    rid_to_target = {}
    for rel in rels:
        target = rel.get("Target")
        if target.startswith("/"):
            target = target.lstrip("/")
        elif not target.startswith("xl/"):
            target = "xl/" + target
        rid_to_target[rel.get("Id")] = target
    out = []
    for sheets in wb:
        if _strip_ns(sheets.tag) != "sheets":
            continue
        for sheet in sheets:
            rid = None
            for k, v in sheet.attrib.items():
                if k.endswith("}id") or k == "id":
                    rid = v
            if rid in rid_to_target:
                out.append((sheet.get("name"), rid_to_target[rid]))
    return out


def _profile_sheet(zf, path, shared, known_rows=None):
    handler = _Profiler(shared, stop_after_header=known_rows is not None)
    try:
        with zf.open(path) as fh:
            xml.sax.parse(fh, handler)
    except StopIteration:
        pass
    except Exception:
        return (known_rows or 0, [])
    n_rows = known_rows if known_rows is not None else handler.nrows
    return (n_rows, handler.header or [])


def _scan_tabular(zip_path):
    """Yield (header_offset, data_offset, fname) for every xlsx/csv under
    INFORMACIÓN/."""
    with open(zip_path, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        try:
            offset = 0
            seen = set()
            while True:
                pos = mm.find(LOCAL, offset)
                if pos == -1:
                    break
                fnl = _u16(mm, pos + 26)
                exl = _u16(mm, pos + 28)
                fname = mm[pos + 30:pos + 30 + fnl].decode("utf-8", "replace")
                low = fname.lower()
                if (fname.startswith("INFORMACIÓN/")
                        and (low.endswith(".xlsx") or low.endswith(".csv"))
                        and fname not in seen):
                    seen.add(fname)
                    yield pos, pos + 30 + fnl + exl, fname
                offset = pos + 4
        finally:
            mm.close()


def _folder_of(fname):
    parts = fname.split("/")
    return parts[1] if len(parts) > 2 else "(root)"


def build_catalog(con, zip_path=ZIP_PATH, on_status=None):
    """(Re)build the data_catalog table. Returns the number of sheets profiled."""
    def status(m):
        if on_status:
            on_status(m)

    con.execute(CATALOG_SCHEMA)
    con.execute("DELETE FROM data_catalog")

    files = list(_scan_tabular(zip_path))
    rows = []
    rid = 0
    now = datetime.now()

    with open(zip_path, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        try:
            for i, (hpos, dpos, fname) in enumerate(files, 1):
                short = fname.split("/")[-1]
                folder = _folder_of(fname)
                status(f"Profiling {i}/{len(files)}: {short}")
                low = fname.lower()
                if low.endswith(".csv"):
                    n_rows, cols, size = _profile_csv(mm, dpos)
                    rid += 1
                    rows.append((rid, folder, short, fname, "csv", size,
                                 "(csv)", len(cols), n_rows,
                                 _cols_json(cols), None, now))
                    continue
                try:
                    length = _inner_zip_length(mm, dpos)
                    size_mb = round(length / 1e6, 2)
                    zf = zipfile.ZipFile(io.BytesIO(mm[dpos:dpos + length]))
                    shared = load_shared_strings(zf)
                    for sheet_name, sheet_path in _list_sheets(zf):
                        known = _KNOWN.get((short, sheet_name))
                        kr = known["rows"] if known else None
                        tbl = known["table"] if known else None
                        n_rows, cols = _profile_sheet(zf, sheet_path, shared, kr)
                        rid += 1
                        rows.append((rid, folder, short, fname, "xlsx", size_mb,
                                     sheet_name, len([c for c in cols if c]),
                                     n_rows, _cols_json(cols), tbl, now))
                except Exception as e:  # noqa: BLE001 — record, don't abort
                    rid += 1
                    rows.append((rid, folder, short, fname, "xlsx", 0.0,
                                 f"(profile failed: {type(e).__name__})",
                                 0, 0, "[]", None, now))
        finally:
            mm.close()

    con.executemany(
        "INSERT INTO data_catalog VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", rows)
    status(f"Catalog built: {len(files)} files, {len(rows)} sheets.")
    return len(rows)


def _cols_json(cols):
    import json
    return json.dumps([c for c in cols if c], ensure_ascii=False)


def _profile_csv(mm, data_start):
    """Tiny stored CSVs: content runs to the trailing data descriptor."""
    dd = mm.find(b"PK\x07\x08", data_start)
    nxt = mm.find(LOCAL, data_start)
    end = dd if dd != -1 and (nxt == -1 or dd < nxt) else nxt
    if end == -1:
        end = data_start
    raw = bytes(mm[data_start:end])
    size = round(len(raw) / 1e6, 4)
    try:
        text = raw.decode("utf-8", "replace")
    except Exception:
        return (0, [], size)
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if not lines:
        return (0, [], size)
    sep = ";" if lines[0].count(";") >= lines[0].count(",") else ","
    cols = [c.strip() for c in lines[0].split(sep)]
    return (len(lines), cols, size)
