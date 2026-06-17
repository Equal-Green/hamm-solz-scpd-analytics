"""Orchestrate extraction -> DuckDB load. Idempotent via pipeline_log."""
import os
from datetime import datetime, timedelta

import duckdb

from config import (
    BATCH_SIZE,
    DUCKDB_PATH,
    FILES,
    RAW_DIR,
    ZIP_PATH,
)
from pipeline.discover import inventory
from pipeline.extract import extract_to_disk, stream_sheet

SCHEMA = """
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER,
    source_year INTEGER,
    num_ticket INTEGER,
    tipo_vehiculo VARCHAR,
    placa VARCHAR,
    tipo_servicio VARCHAR,
    empresa VARCHAR,
    sector VARCHAR,
    peso_ingreso FLOAT,
    peso_salida FLOAT,
    peso_neto FLOAT,
    fec_ingreso TIMESTAMP,
    mes INTEGER,
    anio INTEGER
);
CREATE TABLE IF NOT EXISTS retirados (
    id INTEGER,
    num_ticket VARCHAR,
    organizacion VARCHAR,
    placa VARCHAR,
    peso_ingreso FLOAT,
    peso_salida FLOAT,
    peso_neto FLOAT,
    fec_ingreso TIMESTAMP
);
CREATE TABLE IF NOT EXISTS pipeline_log (
    source_file VARCHAR,
    rows_loaded INTEGER,
    loaded_at TIMESTAMP
);
"""

_EXCEL_EPOCH = datetime(1899, 12, 30)


def connect(path=DUCKDB_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    con = duckdb.connect(path)
    con.execute(SCHEMA)
    return con


# --- value coercion ----------------------------------------------------------
def _to_float(v):
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _to_int(v):
    f = _to_float(v)
    return int(f) if f is not None else None


def _to_str(v):
    if v is None:
        return None
    s = str(v).strip()
    return s if s else None


_TEXT_DATE_FORMATS = (
    "%d/%m/%Y %H:%M:%S",   # retirados: 21/10/2025 10:55:24
    "%d/%m/%Y %H:%M",
    "%d/%m/%Y",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d",
)


def parse_excel_date(serial):
    """Parse a date cell to datetime. Main files store an Excel serial float
    (days since 1899-12-30); the GEOCYCLE file stores dd/mm/yyyy text. Both
    forms (plus ISO) are handled."""
    if serial is None or serial == "":
        return None
    s = str(serial).strip()
    if _looks_numeric(s):
        try:
            return _EXCEL_EPOCH + timedelta(days=float(s))
        except (TypeError, ValueError, OverflowError):
            return None
    for fmt in _TEXT_DATE_FORMATS:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        return None


def _looks_numeric(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# --- per-file loaders --------------------------------------------------------
def _load_transactions(con, spec, xlsx_path, id_start, progress=None):
    batch = []
    state = {"n": 0, "id": id_start}

    def on_field_index(_fi):
        pass

    def get(cells, fi, field):
        return cells.get(fi[field])

    def on_record(cells, fi):
        fec = parse_excel_date(get(cells, fi, "fec_ingreso"))
        row = (
            state["id"],
            spec["source_year"],
            _to_int(get(cells, fi, "num_ticket")),
            _to_str(get(cells, fi, "tipo_vehiculo")),
            _to_str(get(cells, fi, "placa")),
            _to_str(get(cells, fi, "tipo_servicio")),
            _to_str(get(cells, fi, "empresa")),
            _to_str(get(cells, fi, "sector")),
            _to_float(get(cells, fi, "peso_ingreso")),
            _to_float(get(cells, fi, "peso_salida")),
            _to_float(get(cells, fi, "peso_neto")),
            fec,
            fec.month if fec else None,
            fec.year if fec else None,
        )
        state["id"] += 1
        batch.append(row)
        state["n"] += 1
        if len(batch) >= BATCH_SIZE:
            _flush(con, "transactions", 14, batch)
            if progress:
                progress(state["n"])

    stream_sheet(xlsx_path, spec["sheet"], spec["header_row"], on_field_index, on_record)
    if batch:
        _flush(con, "transactions", 14, batch)
    if progress:
        progress(state["n"])
    return state["n"], state["id"]


def _load_retirados(con, spec, xlsx_path, id_start, progress=None):
    batch = []
    state = {"n": 0, "id": id_start}

    def on_field_index(_fi):
        pass

    def get(cells, fi, field):
        return cells.get(fi[field])

    def on_record(cells, fi):
        fec = parse_excel_date(get(cells, fi, "fec_ingreso"))
        # GEOCYCLE: trucks arrive empty, leave loaded -> net = salida - ingreso.
        # Prefer the file's PESO_NETO when present; otherwise derive it.
        peso_ing = _to_float(get(cells, fi, "peso_ingreso"))
        peso_sal = _to_float(get(cells, fi, "peso_salida"))
        peso_net = _to_float(get(cells, fi, "peso_neto"))
        if peso_net is None and peso_sal is not None and peso_ing is not None:
            peso_net = peso_sal - peso_ing
        row = (
            state["id"],
            _to_str(get(cells, fi, "num_ticket")),       # compound id e.g. 00000018-10-2025
            _to_str(get(cells, fi, "organizacion")),     # RAZON_SOCIAL = GEOCYCLE org
            _to_str(get(cells, fi, "placa")),
            peso_ing,
            peso_sal,
            peso_net,
            fec,
        )
        state["id"] += 1
        batch.append(row)
        state["n"] += 1
        if len(batch) >= BATCH_SIZE:
            _flush(con, "retirados", 8, batch)
            if progress:
                progress(state["n"])

    stream_sheet(xlsx_path, spec["sheet"], spec["header_row"], on_field_index, on_record)
    if batch:
        _flush(con, "retirados", 8, batch)
    if progress:
        progress(state["n"])
    return state["n"], state["id"]


def _flush(con, table, ncols, batch):
    placeholders = ",".join(["?"] * ncols)
    con.executemany(f"INSERT INTO {table} VALUES ({placeholders})", batch)
    batch.clear()


# --- idempotency -------------------------------------------------------------
def already_loaded(con, source_file):
    # pipeline_log is written only after a file loads completely, so presence
    # with a positive count means the file is fully loaded.
    row = con.execute(
        "SELECT rows_loaded FROM pipeline_log WHERE source_file = ?", [source_file]
    ).fetchone()
    return row is not None and row[0] and row[0] > 0


def _max_id(con, table):
    row = con.execute(f"SELECT COALESCE(MAX(id), -1) FROM {table}").fetchone()
    return row[0] + 1


def run_pipeline(zip_path=ZIP_PATH, con=None, on_status=None, on_file_progress=None):
    """Run the full extract->load pipeline, idempotently.

    on_status(message): coarse progress (per file).
    on_file_progress(key, done, expected): row-level progress for a file.
    Returns a summary list of {key, rows_loaded, skipped}.
    """
    own = con is None
    if own:
        con = connect()

    def status(msg):
        if on_status:
            on_status(msg)

    status("Scanning ZIP for source files...")
    inv = {r["key"]: r for r in inventory(zip_path)}

    summary = []
    for spec in FILES:
        key = spec["key"]
        rec = inv.get(key)
        if not rec or not rec["found"]:
            status(f"MISSING: {spec['match']}")
            summary.append({"key": key, "rows_loaded": 0, "skipped": False, "missing": True})
            continue

        if already_loaded(con, spec["match"]):
            status(f"Skip (already loaded): {spec['match']}")
            summary.append({"key": key, "rows_loaded": spec["expected_rows"], "skipped": True})
            continue

        dest = os.path.join(RAW_DIR, spec["match"])
        status(f"Extracting {spec['match']}...")
        extract_to_disk(zip_path, rec["header_offset"], rec["data_offset"], dest)

        # fresh load: clear any partial rows for this source
        con.execute("DELETE FROM pipeline_log WHERE source_file = ?", [spec["match"]])

        status(f"Loading {spec['match']} ({spec['expected_rows']:,} rows expected)...")
        prog = (lambda done, k=key, exp=spec["expected_rows"]:
                on_file_progress(k, done, exp)) if on_file_progress else None

        if spec["table"] == "transactions":
            n, _ = _load_transactions(con, spec, dest, _max_id(con, "transactions"), prog)
        else:
            n, _ = _load_retirados(con, spec, dest, _max_id(con, "retirados"), prog)

        con.execute(
            "INSERT INTO pipeline_log VALUES (?, ?, ?)",
            [spec["match"], n, datetime.now()],
        )
        status(f"Loaded {spec['match']}: {n:,} rows")
        summary.append({"key": key, "rows_loaded": n, "skipped": False})

    if own:
        con.close()
    return summary


def reset_pipeline(con):
    """Clear all loaded data so the pipeline re-runs from scratch."""
    con.execute("DELETE FROM transactions")
    con.execute("DELETE FROM retirados")
    con.execute("DELETE FROM pipeline_log")
