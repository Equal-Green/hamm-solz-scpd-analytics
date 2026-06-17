"""SCPD Analytics -- entry point.

Routes between the first-run pipeline UI and the dashboard based on whether the
local DuckDB has been populated. Launch with:

    streamlit run dashboard/app.py
"""
import os
import sys

# Make sibling modules (db/state/theme) and the project root importable,
# regardless of how Streamlit is launched.
_here = os.path.dirname(os.path.abspath(__file__))
for _p in (_here, os.path.dirname(_here), os.path.dirname(os.path.dirname(_here))):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import streamlit as st

from db import get_db          # noqa: E402  (db.py fixes sys.path)
from state import is_loaded, loaded_files
from style import inject_css, render_header

from config import FILES, TOTAL_EXPECTED_ROWS, ZIP_PATH
from pipeline.load import run_pipeline

st.set_page_config(page_title="SCPD Analytics — Guayaquil",
                   page_icon="🗑️", layout="wide")

con = get_db()
inject_css()


def _run_pipeline_ui():
    render_header(
        "First-Run Setup",
        "Sistema de Control y Pesaje de Desechos — Las Iguanas landfill, "
        "Guayaquil (Consorcio URVASEO / CIRCULAREP).",
        eyebrow="SCPD ANALYTICS · PIPELINE",
    )

    zip_ok = os.path.exists(ZIP_PATH)
    st.markdown(f"**Source ZIP:** `{ZIP_PATH}`  ·  "
                f"{'✅ found' if zip_ok else '❌ not found'}")
    if not zip_ok:
        st.error(
            "Source ZIP not found. Set `ZIP_PATH` in `config.py` (or the "
            "`SCPD_ZIP_PATH` environment variable) to your copy of the data, "
            "then reload."
        )
        st.stop()

    done = loaded_files(con)
    st.write("The pipeline will extract and load the following files "
             f"(~{TOTAL_EXPECTED_ROWS:,} rows total). First run takes 3–6 minutes.")
    for spec in FILES:
        state = "✅ loaded" if spec["match"] in done else "⏳ pending"
        st.markdown(f"- `{spec['match']}` — {spec['spec_rows']:,} rows — {state}")

    if st.button("▶️ Run pipeline", type="primary"):
        status_box = st.status("Starting pipeline…", expanded=True)
        bars = {}

        def on_status(msg):
            status_box.update(label=msg)
            status_box.write(msg)

        def on_progress(key, done_rows, expected):
            if key not in bars:
                bars[key] = st.progress(0.0, text=f"{key}: 0 / {expected:,}")
            frac = min(done_rows / expected, 1.0) if expected else 1.0
            bars[key].progress(frac, text=f"{key}: {done_rows:,} / {expected:,}")

        summary = run_pipeline(con=con, on_status=on_status,
                               on_file_progress=on_progress)
        status_box.update(label="Pipeline complete.", state="complete")
        st.success("Data loaded. " + ", ".join(
            f"{s['key']}={s['rows_loaded']:,}" for s in summary))
        st.balloons()
        st.cache_data.clear()
        st.rerun()


# --- Route: first-run setup, or the grouped multipage app -------------------
if not is_loaded(con):
    _run_pipeline_ui()
    st.stop()

# Sidebar brand block above the nested navigation.
with st.sidebar:
    st.markdown(
        '<div class="scpd-brand">🗑️ <span>SCPD Analytics</span>'
        '<div class="scpd-brand-sub">Guayaquil · Las Iguanas</div></div>',
        unsafe_allow_html=True,
    )

home = st.Page("pages/00_home.py", title="Executive Summary", icon="🏠", default=True)
overview = st.Page("pages/01_overview.py", title="Overview", icon="📈")
services = st.Page("pages/02_service_types.py", title="Service Types", icon="🧾")
operators = st.Page("pages/03_operators.py", title="Operators & Fleet", icon="🚛")
geocycle = st.Page("pages/04_geocycle.py", title="GEOCYCLE Recovery", icon="♻️")
ask = st.Page("pages/07_ask.py", title="Ask the Data", icon="💬")
quality = st.Page("pages/05_data_quality.py", title="Data Quality & Catalog", icon="🔎")
settings = st.Page("pages/06_settings.py", title="Settings", icon="⚙️")

nav = st.navigation({
    "Start here": [home],
    "The story": [overview, services, operators, geocycle],
    "Explore": [ask],
    "Trust & data": [quality],
    "System": [settings],
})
nav.run()
