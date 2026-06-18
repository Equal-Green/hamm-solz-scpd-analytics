import os

import streamlit as st

import os, sys
_here = os.path.dirname(os.path.abspath(__file__))
for _p in (_here, os.path.dirname(_here), os.path.dirname(os.path.dirname(_here))):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from db import get_db
from analysis import queries as q
from style import inject_css, render_header
from i18n import t
from config import DUCKDB_PATH, ZIP_PATH
from pipeline.load import run_pipeline, reset_pipeline
from pipeline.export import pg_export, CLOUD_EXPORT_ENABLED

con = get_db()
inject_css()

render_header(t("page.settings"), "Pipeline status, reloads, and cloud export.")

# --- Pipeline status ---------------------------------------------------------
st.subheader("Pipeline status")
status = q.pipeline_status(con)
if status.empty:
    st.warning("No files loaded yet. Run the pipeline from the Home page.")
else:
    st.dataframe(status, use_container_width=True, hide_index=True)

counts = q.table_counts(con)
c1, c2, c3 = st.columns(3)
c1.metric("transactions rows", f"{counts['transactions']:,}")
c2.metric("retirados rows", f"{counts['retirados']:,}")
size = os.path.getsize(DUCKDB_PATH) / 1e6 if os.path.exists(DUCKDB_PATH) else 0
c3.metric("DuckDB file size", f"{size:,.1f} MB")

st.divider()

# --- Re-run pipeline ---------------------------------------------------------
st.subheader("Re-run pipeline")
st.caption(f"Source ZIP: `{ZIP_PATH}`")
st.write("Clears all loaded data and `pipeline_log`, then re-extracts and "
         "reloads every file.")
if st.button("🔄 Re-run pipeline (clear & reload)", type="primary"):
    reset_pipeline(con)
    box = st.status("Re-running pipeline…", expanded=True)
    bars = {}

    def on_status(msg):
        box.update(label=msg)
        box.write(msg)

    def on_progress(key, done_rows, expected):
        if key not in bars:
            bars[key] = st.progress(0.0, text=key)
        bars[key].progress(min(done_rows / expected, 1.0) if expected else 1.0,
                           text=f"{key}: {done_rows:,} / {expected:,}")

    run_pipeline(con=con, on_status=on_status, on_file_progress=on_progress)
    box.update(label="Pipeline complete.", state="complete")
    st.cache_data.clear()
    st.success("Reload complete.")
    st.rerun()

st.divider()

# --- Export to Postgres (Phase 2, gated) -------------------------------------
st.subheader("Export to Postgres / Supabase")
st.caption("Phase 2 — build the connection here; export is gated until enabled.")
status_txt = "🟢 enabled" if CLOUD_EXPORT_ENABLED else "🔒 gated (coming soon)"
st.markdown(f"**Cloud export:** {status_txt}")

database_url = st.text_input(
    "DATABASE_URL",
    placeholder="postgresql://user:pass@host:5432/dbname",
    type="password",
)
if st.button("⬆️ Export to Postgres", disabled=not CLOUD_EXPORT_ENABLED and False):
    result = pg_export(con, database_url)
    if result["status"] == "ok":
        st.success(result["message"])
        st.json(result["tables"])
    elif result["status"] == "disabled":
        st.info(result["message"])
    else:
        st.error(result["message"])
