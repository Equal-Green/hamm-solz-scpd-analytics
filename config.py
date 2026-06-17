"""Central configuration for the SCPD analytics application.

Everything a new user must change to run against their own copy of the source
data lives here. The defaults match the consulting deliverable's source ZIP.
"""
import os

# --- Paths -------------------------------------------------------------------
# Project root (this file's directory). All other paths are derived from it so
# the app works regardless of the current working directory.
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# The single source ZIP. CRITICAL: this ZIP was written in streaming mode
# (local-file flag bit 3 set, no End-of-Central-Directory record) and CANNOT be
# opened with `unzip`, Python's `zipfile`, or any standard tool. The pipeline
# scans for PK\x03\x04 local-file-header signatures directly. Point this at your
# own copy of the source ZIP.
ZIP_PATH = os.environ.get(
    "SCPD_ZIP_PATH",
    os.path.expanduser("~/Downloads/INFORMACIÓN.zip"),
)

DATA_DIR = os.path.join(ROOT_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")          # extracted .xlsx land here
DUCKDB_PATH = os.path.join(DATA_DIR, "scpd.duckdb")

# --- Source file specifications ---------------------------------------------
# One entry per data file inside the ZIP. `match` is a substring used to locate
# the file by name during the binary scan. `header_row` is 1-indexed within the
# sheet. `sheet` is the *sheet name* (resolved to its XML part via workbook.xml,
# never assumed to be sheet1.xml). `table` is the DuckDB target table.
FILES = [
    {
        "key": "scpd_2023",
        "match": "DATA SCPD 2023 (1).xlsx",
        "sheet": "Hoja1",
        "header_row": 2,           # row 1 is a merged title cell
        "source_year": 2023,
        "expected_rows": 165505,   # verified by full parse (brief said 165,504)
        "spec_rows": 165504,       # the project brief's stated count
        "table": "transactions",
    },
    {
        "key": "scpd_2024",
        "match": "DATA SCPD 2024 (1).xlsx",
        "sheet": "Hoja1",
        "header_row": 2,
        "source_year": 2024,
        "expected_rows": 176979,   # verified (brief said 176,978)
        "spec_rows": 176978,
        "table": "transactions",
    },
    {
        "key": "scpd_2025",
        "match": "DATA SCPD 2025 (1).xlsx",
        "sheet": "DATA",           # NOT Hoja1; book also has pivot sheets we skip
        "header_row": 1,
        "source_year": 2025,
        "expected_rows": 174042,   # matches brief exactly
        "spec_rows": 174042,
        "table": "transactions",
    },
    {
        "key": "retirados_geocycle",
        "match": "DATA SCPD RETIRADOS GEOCYCLE.xlsx",
        "sheet": "Data",
        "header_row": 1,
        "source_year": None,       # spans years; date carries the year
        "expected_rows": 7515,     # matches brief exactly
        "spec_rows": 7515,
        "table": "retirados",
    },
]

# Verified actual total = 524,041 (brief stated 524,039; 2023 & 2024 each carry
# one more genuine row than the brief recorded -- confirmed distinct tickets,
# no nulls, no duplicates, no totals row).
TOTAL_EXPECTED_ROWS = sum(f["expected_rows"] for f in FILES)

# --- Column resolution -------------------------------------------------------
# Columns are resolved by *header name* (each field lists acceptable aliases),
# falling back to the confirmed 0-indexed positions when no header matches.
# These names/positions were verified by parsing the real source files -- the
# logical names in the project brief (TIPO_SERVICIO, EMPRESA) do not exist as
# literal headers; the service dimension lives in DESC_TIPO_DESECHO and the
# operating company in RAZON_SOCIAL.
FIELD_HEADERS = {
    "num_ticket": ["NUM_TICKET", "NUM_TICKET_CARGA"],
    "tipo_vehiculo": ["TIPO_VEHICULO"],
    "placa": ["PLACA"],
    "tipo_servicio": ["DESC_TIPO_DESECHO"],   # service category dimension
    "empresa": ["RAZON_SOCIAL"],              # operating company
    "organizacion": ["RAZON_SOCIAL"],         # GEOCYCLE org name (retirados)
    "sector": ["SECTOR"],
    "peso_ingreso": ["PESO_INGRESO"],
    "fec_ingreso": ["FEC_INGRESO"],
    "peso_salida": ["PESO_SALIDA"],
    "peso_neto": ["PESO_NETO"],
}

# Fallback positions reflect the 72-column main-file (transactions) layout.
FIELD_FALLBACK_IDX = {
    "num_ticket": 0,
    "tipo_vehiculo": 2,
    "placa": 4,
    "tipo_servicio": 22,
    "empresa": 8,
    "organizacion": 8,
    "sector": 32,
    "peso_ingreso": 24,
    "fec_ingreso": 27,
    "peso_salida": 28,
    "peso_neto": 31,
}

# Insert into DuckDB in chunks; never accumulate a whole file in memory.
BATCH_SIZE = 10000
