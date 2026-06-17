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
from analysis import queries as q
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


def _home():
    render_header(
        "Guayaquil Solid Waste",
        "Las Iguanas landfill · Consorcio URVASEO · CIRCULAREP — "
        "2023–2025 weighbridge records.",
    )

    k = q.kpis(con)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total trips", f"{k['trips']:,}")
    c2.metric("Net tonnage", f"{k['tonnes']:,.0f} t")
    c3.metric("Avg per trip", f"{k['avg_kg']:,.0f} kg")
    rng = (f"{k['first_dt']:%Y}–{k['last_dt']:%Y}" if k["first_dt"] else "—")
    c4.metric("Date range", rng)

    st.divider()
    st.subheader("Pages")
    st.markdown(
        "- **Overview** — volume & tonnage trends\n"
        "- **Service Types** — by service category + anomaly callout\n"
        "- **Operators & Fleet** — companies and vehicle classes\n"
        "- **GEOCYCLE Recovery** — material recovery (inverted weights)\n"
        "- **Data Quality** — row counts, nulls, flags\n"
        "- **Settings** — pipeline status, re-run, cloud export\n\n"
        "Use the sidebar to navigate."
    )

    an = q.servicios_especial_anomaly(con)
    if an["pct"]:
        st.info(
            f"⚠️ **Anomaly:** SERVICIOS ESPECIAL trips jumped "
            f"**{an['pct']:+.0f}%** from 2023 ({an['y2023']:,}) to "
            f"2024 ({an['y2024']:,}). See the Service Types page."
        )


if is_loaded(con):
    _home()
else:
    _run_pipeline_ui()
