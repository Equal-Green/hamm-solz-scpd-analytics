"""Extraction primitives for the SCPD source data.

Two hard problems are solved here:

1. The OUTER ZIP is a streaming-mode archive (local-file flag bit 3 set, no
   End-of-Central-Directory record). Standard tools fail. We mmap the file and
   scan for PK\\x03\\x04 local-file-header signatures. The target files are
   STORED (uncompressed) with their real sizes in trailing data descriptors,
   not the local header -- so to find each inner file's exact extent we
   forward-parse the inner .xlsx (itself a normal ZIP) through its local
   headers -> central directory -> EOCD.

2. The main sheets decompress to ~450 MB of XML. openpyxl / pandas.read_excel
   load the whole DOM and hang. We SAX-parse the worksheet XML as a stream and
   honor each cell's `r=` column reference so sparse/empty cells don't shift
   columns.
"""
import io
import mmap
import os
import struct
import xml.sax
import zipfile

from config import FIELD_FALLBACK_IDX, FIELD_HEADERS

# ZIP signatures
LOCAL = b"PK\x03\x04"
CDIR = b"PK\x01\x02"
EOCD = b"PK\x05\x06"


def _u16(buf, off):
    return struct.unpack_from("<H", buf, off)[0]


def _u32(buf, off):
    return struct.unpack_from("<I", buf, off)[0]


# --- Outer streaming ZIP -----------------------------------------------------
def scan_zip_for(zip_path, matches):
    """Scan the outer streaming ZIP for local-file headers whose name contains
    any of `matches` and ends in .xlsx. Returns a list of dicts with the
    filename and the byte offset where the inner file's data begins.

    Uses mmap so a multi-GB archive is never read fully into RAM.
    """
    found = []
    seen = set()
    with open(zip_path, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        try:
            offset = 0
            while True:
                pos = mm.find(LOCAL, offset)
                if pos == -1:
                    break
                fname_len = _u16(mm, pos + 26)
                extra_len = _u16(mm, pos + 28)
                fname = mm[pos + 30 : pos + 30 + fname_len].decode("utf-8", "replace")
                if (
                    fname.lower().endswith(".xlsx")
                    and any(m in fname for m in matches)
                    and fname not in seen
                ):
                    seen.add(fname)
                    found.append(
                        {
                            "filename": fname,
                            "header_offset": pos,
                            "data_offset": pos + 30 + fname_len + extra_len,
                        }
                    )
                offset = pos + 4
        finally:
            mm.close()
    return found


def _inner_zip_length(mm, data_start):
    """Forward-parse the inner .xlsx (a standard ZIP stored verbatim at
    `data_start`) and return its exact length in bytes. Walks local file
    entries, then the central directory, to the EOCD record.
    """
    o = data_start
    # 1. local file entries (inner entries carry their sizes; bit 3 not set)
    while mm[o : o + 4] == LOCAL:
        comp = _u32(mm, o + 18)
        fnl = _u16(mm, o + 26)
        exl = _u16(mm, o + 28)
        o = o + 30 + fnl + exl + comp
    # 2. central directory entries
    while mm[o : o + 4] == CDIR:
        fnl = _u16(mm, o + 28)
        exl = _u16(mm, o + 30)
        cl = _u16(mm, o + 32)
        o = o + 46 + fnl + exl + cl
    # 3. EOCD
    if mm[o : o + 4] != EOCD:
        raise ValueError(
            f"Expected EOCD at inner offset {o - data_start}, got {mm[o:o+4]!r}"
        )
    comment_len = _u16(mm, o + 20)
    end = o + 22 + comment_len
    return end - data_start


def extract_to_disk(zip_path, header_offset, data_offset, dest_path):
    """Extract one inner .xlsx from the outer ZIP to `dest_path`. Returns the
    number of bytes written. Skips work if `dest_path` already exists and is
    a valid ZIP.
    """
    if os.path.exists(dest_path) and zipfile.is_zipfile(dest_path):
        return os.path.getsize(dest_path)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(zip_path, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        try:
            length = _inner_zip_length(mm, data_offset)
            with open(dest_path, "wb") as out:
                out.write(mm[data_offset : data_offset + length])
        finally:
            mm.close()
    if not zipfile.is_zipfile(dest_path):
        raise ValueError(f"Extracted file is not a valid xlsx: {dest_path}")
    return os.path.getsize(dest_path)


# --- Inner xlsx: sheet + shared-strings resolution ---------------------------
def _strip_ns(tag):
    return tag.split("}", 1)[1] if "}" in tag else tag


def resolve_sheet_path(zf, sheet_name):
    """Map a sheet display name (e.g. "DATA") to its worksheet XML part
    (e.g. "xl/worksheets/sheet3.xml") via workbook.xml + its rels.
    """
    import xml.etree.ElementTree as ET

    wb = ET.fromstring(zf.read("xl/workbook.xml"))
    rid = None
    for sheets in wb:
        if _strip_ns(sheets.tag) != "sheets":
            continue
        for sheet in sheets:
            if sheet.get("name") == sheet_name:
                for k, v in sheet.attrib.items():
                    if k.endswith("}id") or k == "id":
                        rid = v
                break
    if rid is None:
        raise ValueError(f"Sheet {sheet_name!r} not found in workbook.xml")

    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    for rel in rels:
        if rel.get("Id") == rid:
            target = rel.get("Target")
            if target.startswith("/"):
                return target.lstrip("/")
            return "xl/" + target if not target.startswith("xl/") else target
    raise ValueError(f"Relationship {rid!r} not found in workbook rels")


class _SharedStringsHandler(xml.sax.ContentHandler):
    """Stream xl/sharedStrings.xml into a list. Concatenates all <t> runs
    within each <si> (rich-text strings have multiple runs)."""

    def __init__(self):
        self.strings = []
        self._cur = []
        self._in_t = False

    def startElement(self, name, attrs):
        if name == "si":
            self._cur = []
        elif name == "t":
            self._in_t = True

    def characters(self, content):
        if self._in_t:
            self._cur.append(content)

    def endElement(self, name):
        if name == "t":
            self._in_t = False
        elif name == "si":
            self.strings.append("".join(self._cur))


def load_shared_strings(zf):
    if "xl/sharedStrings.xml" not in zf.namelist():
        return []
    handler = _SharedStringsHandler()
    with zf.open("xl/sharedStrings.xml") as fh:
        xml.sax.parse(fh, handler)
    return handler.strings


def _col_to_index(ref):
    """'AB27' -> 27 (0-indexed column). Parses leading letters only."""
    idx = 0
    for ch in ref:
        if ch.isalpha():
            idx = idx * 26 + (ord(ch.upper()) - ord("A") + 1)
        else:
            break
    return idx - 1


# --- Worksheet SAX parser ----------------------------------------------------
class _SheetHandler(xml.sax.ContentHandler):
    """Streams worksheet rows. For each completed row it builds a
    {col_index: value} dict (honoring `r=` so empty cells don't shift columns),
    then invokes on_header(cells) for the header row and on_row(cells) for each
    data row. Nothing is accumulated across rows.
    """

    def __init__(self, shared_strings, header_row, on_header, on_row):
        self.shared = shared_strings
        self.header_row = header_row
        self.on_header = on_header
        self.on_row = on_row

        self.row_num = 0
        self.cells = {}
        self.cur_idx = -1
        self.cur_type = ""
        self.cur_val = []
        self.in_value = False
        self.in_inline_t = False

    def startElement(self, name, attrs):
        if name == "row":
            r = attrs.get("r")
            self.row_num = int(r) if r else self.row_num + 1
            self.cells = {}
        elif name == "c":
            ref = attrs.get("r")
            self.cur_idx = _col_to_index(ref) if ref else self.cur_idx + 1
            self.cur_type = attrs.get("t", "")
            self.cur_val = []
        elif name == "v":
            self.in_value = True
            self.cur_val = []
        elif name == "t" and self.cur_type == "inlineStr":
            self.in_inline_t = True
            self.cur_val = []

    def characters(self, content):
        if self.in_value or self.in_inline_t:
            self.cur_val.append(content)

    def endElement(self, name):
        if name == "v":
            self.in_value = False
            raw = "".join(self.cur_val)
            if self.cur_type == "s":  # shared string
                try:
                    raw = self.shared[int(raw)]
                except (ValueError, IndexError):
                    pass
            self.cells[self.cur_idx] = raw
        elif name == "t" and self.in_inline_t:
            self.in_inline_t = False
            self.cells[self.cur_idx] = "".join(self.cur_val)
        elif name == "row":
            if self.row_num == self.header_row:
                self.on_header(self.cells)
            elif self.row_num > self.header_row:
                self.on_row(self.cells)


def build_field_index(header_cells):
    """Given the parsed header row ({col_idx: name}), return {field: col_idx}
    resolving by header name, falling back to the confirmed fixed positions."""
    name_to_idx = {}
    for idx, val in header_cells.items():
        if val is None:
            continue
        key = str(val).strip().upper()
        if key and key not in name_to_idx:
            name_to_idx[key] = idx

    field_index = {}
    for field, aliases in FIELD_HEADERS.items():
        matched = None
        for alias in aliases:
            if alias.upper() in name_to_idx:
                matched = name_to_idx[alias.upper()]
                break
        field_index[field] = matched if matched is not None else FIELD_FALLBACK_IDX[field]
    return field_index


def stream_sheet(xlsx_path, sheet_name, header_row, on_field_index, on_record):
    """Open an extracted .xlsx and stream its rows.

    Calls on_field_index(field_index) once after the header is parsed, then
    on_record(cells, field_index) for each data row, where `cells` is the
    {col_idx: value} dict. Returns the number of data rows seen.
    """
    with zipfile.ZipFile(xlsx_path) as zf:
        shared = load_shared_strings(zf)
        sheet_path = resolve_sheet_path(zf, sheet_name)

        state = {"field_index": None, "count": 0}

        def _on_header(cells):
            fi = build_field_index(cells)
            state["field_index"] = fi
            on_field_index(fi)

        def _on_row(cells):
            if state["field_index"] is None:
                return
            state["count"] += 1
            on_record(cells, state["field_index"])

        handler = _SheetHandler(shared, header_row, _on_header, _on_row)
        with zf.open(sheet_path) as fh:
            xml.sax.parse(fh, handler)
        return state["count"]
