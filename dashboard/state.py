"""Pipeline-state helpers shared by the home page and the dashboard pages."""
import streamlit as st

from config import FILES


def is_loaded(con):
    """True when every configured source file is present in pipeline_log."""
    logged = {r[0] for r in con.execute(
        "SELECT source_file FROM pipeline_log WHERE rows_loaded > 0").fetchall()}
    return all(spec["match"] in logged for spec in FILES)


def loaded_files(con):
    return {r[0]: r[1] for r in con.execute(
        "SELECT source_file, rows_loaded FROM pipeline_log").fetchall()}


def ensure_loaded(con):
    """Guard for dashboard pages: stop with a friendly message if the pipeline
    hasn't been run yet."""
    if not is_loaded(con):
        st.warning(
            "Data isn't loaded yet. Open the **Home** page (top of the sidebar) "
            "and run the pipeline first."
        )
        st.stop()
