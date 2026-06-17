"""Single shared DuckDB connection for the whole app.

Every page imports get_db() from here -- no page opens its own connection.
The path / config import works whether Streamlit is launched from the project
root or elsewhere, by making the project root importable.
"""
import os
import sys

import duckdb
import streamlit as st

# Make the project root importable (config.py, pipeline/, analysis/).
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from config import DUCKDB_PATH  # noqa: E402
from pipeline.load import SCHEMA  # noqa: E402
from pipeline.catalog import CATALOG_SCHEMA  # noqa: E402


@st.cache_resource
def get_db():
    """Return the process-wide DuckDB connection, creating the file + schema
    if needed. Cached so all pages and reruns share one connection."""
    os.makedirs(os.path.dirname(DUCKDB_PATH), exist_ok=True)
    con = duckdb.connect(DUCKDB_PATH)
    con.execute(SCHEMA)
    con.execute(CATALOG_SCHEMA)
    return con
