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
from style import (inject_css, render_header, hamm_wordmark, eg_logo_html)
from i18n import t, tr, language_selector

from config import FILES, TOTAL_EXPECTED_ROWS, ZIP_PATH
from pipeline.load import run_pipeline
import compliance as compliance_model   # noqa: E402  (repo root is on sys.path)

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

# Co-branded logos (HAMM Solz × EqualGreen) at the top of the sidebar,
# with the language toggle on its own row directly below (both above the nav).
with st.sidebar:
    st.markdown(
        '<div class="scpd-side-logos">'
        f'{hamm_wordmark(on_dark=True, height=16, tagline=False)}'
        '<span class="scpd-x">×</span>'
        f'{eg_logo_html(22)}'
        '<span class="scpd-eg">EqualGreen</span></div>',
        unsafe_allow_html=True,
    )
language_selector()

def P(path, title, icon, default=False):
    return st.Page(path, title=tr(t(title)), icon=icon, default=default)


cover = P("pages/cover.py", "page.cover", "📘", default=True)
home = P("pages/00_home.py", "page.exec", "🏠")
architecture = P("pages/architecture.py", "page.arch", "🧩")
overview = P("pages/01_overview.py", "page.overview", "📈")
services = P("pages/02_service_types.py", "page.services", "🧾")
operators = P("pages/03_operators.py", "page.operators", "🚛")
geocycle = P("pages/04_geocycle.py", "page.geocycle", "♻️")
geo = P("pages/08_geo_routes.py", "page.geo", "🗺️")
forecast = P("pages/09_forecast.py", "page.forecast", "📉")
efficiency = P("pages/10_efficiency.py", "page.efficiency", "⚙️")
integrity = P("pages/11_integrity.py", "page.integrity", "🔐")
diversion = P("pages/12_diversion.py", "page.diversion", "🔄")
ask = P("pages/07_ask.py", "page.ask", "💬")
quality = P("pages/05_data_quality.py", "page.quality", "🔎")
settings = P("pages/06_settings.py", "page.settings", "⚙️")

groups = {
    tr(t("nav.start")): [cover, home, architecture],
    tr(t("nav.story")): [overview, services, operators, geocycle, geo],
    tr(t("nav.analysis")): [forecast, efficiency, integrity, diversion],
    tr(t("nav.explore")): [ask],
    tr(t("nav.trust")): [quality],
}

# Agreement & Compliance is internal and off by default — the deployed report
# does not carry it. Set SCPD_SHOW_COMPLIANCE=1 to bring it back. st.navigation
# routes only the pages it is given, so leaving the page out also makes its URL
# unreachable, not merely hidden from the sidebar.
if compliance_model.page_enabled():
    groups[tr(t("nav.agreement"))] = [
        P("pages/13_compliance.py", "page.compliance", "📜")
    ]

groups[tr(t("nav.system"))] = [settings]

nav = st.navigation(groups)
nav.run()
