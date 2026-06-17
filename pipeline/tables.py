"""Generic ingest of every tabular sheet in the INFORMACIÓN folder into DuckDB.

The four SCPD pesaje files already load into typed `transactions` / `retirados`
tables. This loads *every other* qualifying sheet (header row + >=1 data row)
as an all-VARCHAR table named `src_<file>_<sheet>`, so the whole archive is
queryable. A registry table `source_tables` records what was loaded.
"""
import io
import mmap
import re
import xml.sax
import zipfile

from config import FILES, ZIP_PATH
from pipeline.extract import (
    LOCAL, _u16, _col_to_index, _inner_zip_length, load_shared_strings,
)
from pipeline.catalog import _list_sheets, _scan_tabular, _profile_csv

REGISTRY_SCHEMA = """
CREATE TABLE IF NOT EXISTS source_tables (
    table_name VARCHAR,
    file_name VARCHAR,
    sheet_name VARCHAR,
    n_rows INTEGER,
    n_columns INTEGER
);
"""

_SCPD = {f["match"] for f in FILES}
_BATCH = 5000


def _sanitize(name):
    s = re.sub(r"[^0-9a-zA-Z]+", "_", name.lower()).strip("_")
    return re.sub(r"_+", "_", s) or "x"


def _unique(name, used):
    base = name[:55]
    cand, i = base, 1
    while cand in used:
        i += 1
        cand = f"{base}_{i}"
    used.add(cand)
    return cand


class _RowHandler(xml.sax.ContentHandler):
    """Streams rows as {col_idx: value}; captures the first row with >=2
    non-empty cells as the header, then calls on_row for each later row."""

    def __init__(self, shared, on_header, on_row):
        self.shared, self.on_header, self.on_row = shared, on_header, on_row
        self.header_done = False
        self.cells = {}
        self.idx = -1
        self.t = ""
        self.val = []
        self.inv = False

    def startElement(self, name, attrs):
        if name == "row":
            self.cells = {}
        elif name == "c":
            ref = attrs.get("r")
            self.idx = _col_to_index(ref) if ref else self.idx + 1
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
            self.cells[self.idx] = v
        elif name == "row":
            if not self.header_done:
                nonempty = [c for c in self.cells.values() if str(c).strip()]
                if len(nonempty) >= 2:
                    self.header_done = True
                    self.on_header(self.cells)
            else:
                self.on_row(self.cells)


def _dedupe_headers(raw):
    out, seen = [], {}
    for i, h in enumerate(raw):
        name = _sanitize(str(h)) if str(h).strip() else f"col_{i+1}"
        if name in seen:
            seen[name] += 1
            name = f"{name}_{seen[name]}"
        else:
            seen[name] = 0
        out.append(name)
    return out


def _load_sheet(con, table, zf, sheet_path):
    state = {"cols": None, "n": 0, "ncol": 0}
    batch = []

    def on_header(cells):
        ncol = max(cells) + 1
        cols = _dedupe_headers([cells.get(i, f"col_{i+1}") for i in range(ncol)])
        state["cols"], state["ncol"] = cols, ncol
        coldef = ", ".join(f'"{c}" VARCHAR' for c in cols)
        con.execute(f'CREATE OR REPLACE TABLE "{table}" ({coldef})')

    def on_row(cells):
        if state["cols"] is None:
            return
        row = [cells.get(i) for i in range(state["ncol"])]
        batch.append(row)
        state["n"] += 1
        if len(batch) >= _BATCH:
            _flush(con, table, state["ncol"], batch)

    h = _RowHandler(load_shared_strings(zf), on_header, on_row)
    with zf.open(sheet_path) as fh:
        xml.sax.parse(fh, h)
    if state["cols"] is None:
        return None
    if batch:
        _flush(con, table, state["ncol"], batch)
    return state["n"], state["ncol"]


def _flush(con, table, ncols, batch):
    con.executemany(
        f'INSERT INTO "{table}" VALUES ({",".join(["?"] * ncols)})', batch)
    batch.clear()


def load_all_tables(con, zip_path=ZIP_PATH, on_status=None):
    """Load every non-SCPD tabular sheet into DuckDB. Returns count of tables."""
    def status(m):
        if on_status:
            on_status(m)

    con.execute(REGISTRY_SCHEMA)
    # drop prior src_ tables for a clean rebuild
    for (t,) in con.execute(
            "SELECT table_name FROM information_schema.tables "
            "WHERE table_name LIKE 'src_%'").fetchall():
        con.execute(f'DROP TABLE IF EXISTS "{t}"')
    con.execute("DELETE FROM source_tables")

    files = list(_scan_tabular(zip_path))
    used, loaded = set(), 0
    with open(zip_path, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        try:
            for i, (hpos, dpos, fname) in enumerate(files, 1):
                short = fname.split("/")[-1]
                if short in _SCPD:
                    continue
                status(f"Loading {i}/{len(files)}: {short}")
                if fname.lower().endswith(".csv"):
                    _load_csv(con, mm, dpos, short, used, lambda n, c, s=short:
                              _register(con, n, s, "(csv)", c))
                    loaded += 1
                    continue
                try:
                    length = _inner_zip_length(mm, dpos)
                    zf = zipfile.ZipFile(io.BytesIO(mm[dpos:dpos + length]))
                    for sheet_name, sheet_path in _list_sheets(zf):
                        table = _unique("src_" + _sanitize(short.replace(".xlsx", ""))
                                        + "_" + _sanitize(sheet_name), used)
                        res = _load_sheet(con, table, zf, sheet_path)
                        if res and res[0] > 0:
                            _register(con, table, short, sheet_name, res)
                            loaded += 1
                except Exception:  # noqa: BLE001 — skip unparseable workbooks
                    continue
        finally:
            mm.close()
    status(f"Loaded {loaded} source tables.")
    return loaded


def _register(con, table, file_name, sheet_name, res):
    n, ncol = (res if isinstance(res, tuple) else (res, 0))
    con.execute("INSERT INTO source_tables VALUES (?,?,?,?,?)",
                [table, file_name, sheet_name, n, ncol])


def _load_csv(con, mm, dpos, short, used, register):
    n_rows, cols, _ = _profile_csv(mm, dpos)
    raw = bytes(mm[dpos:mm.find(b"PK\x07\x08", dpos)]) if mm.find(
        b"PK\x07\x08", dpos) != -1 else b""
    text = raw.decode("utf-8", "replace")
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if not lines:
        return
    sep = ";" if lines[0].count(";") >= lines[0].count(",") else ","
    header = _dedupe_headers([c.strip() for c in lines[0].split(sep)])
    table = _unique("src_" + _sanitize(short.replace(".csv", "")), used)
    coldef = ", ".join(f'"{c}" VARCHAR' for c in header)
    con.execute(f'CREATE OR REPLACE TABLE "{table}" ({coldef})')
    rows = [ln.split(sep)[:len(header)] +
            [None] * (len(header) - len(ln.split(sep))) for ln in lines[1:]]
    if rows:
        con.executemany(
            f'INSERT INTO "{table}" VALUES ({",".join(["?"]*len(header))})', rows)
    register(table, len(rows) + 1, (len(rows) + 1, len(header)))
