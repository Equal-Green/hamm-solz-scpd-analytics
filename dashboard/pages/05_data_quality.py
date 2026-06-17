import streamlit as st

import os, sys
_here = os.path.dirname(os.path.abspath(__file__))
for _p in (_here, os.path.dirname(_here), os.path.dirname(os.path.dirname(_here))):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from db import get_db
from state import ensure_loaded
from analysis import queries as q
from style import inject_css, render_header

st.set_page_config(page_title="Data Quality · SCPD", page_icon="🔎", layout="wide")
con = get_db()
inject_css()
ensure_loaded(con)

render_header("Data Quality", "Row counts, null rates, and integrity flags.")

rep = q.quality_report(con)

st.subheader("Row counts: loaded vs. brief")
for f in rep["files"]:
    delta = f["loaded"] - f["spec_rows"]
    flag = "✅" if delta == 0 else f"⚠️ {delta:+d}"
    st.markdown(
        f"- `{f['file']}` — loaded **{f['loaded']:,}**, "
        f"brief **{f['spec_rows']:,}** {flag}"
    )
st.caption(
    "2023 and 2024 each contain one more genuine row than the project brief "
    "recorded (verified: distinct tickets, no nulls, no duplicates, no totals "
    "row). 2025 and GEOCYCLE match exactly."
)

st.divider()
t = rep["transactions"]
st.subheader("Transactions — key-column health")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total rows", f"{t['total']:,}")
c2.metric("Zero net weight", f"{t['zero_net']:,}",
          help="PESO_NETO = 0 — flagged")
c3.metric("Negative net weight", f"{t['neg_net']:,}",
          help="PESO_NETO < 0 — flagged")
c4.metric("Duplicate ticket/year", f"{t['dup_ticket_year']:,}")

if t["zero_net"]:
    st.warning(f"{t['zero_net']:,} trips have zero net weight "
               f"({t['zero_net']/t['total']*100:.2f}%).")
if t["neg_net"]:
    st.warning(f"{t['neg_net']:,} trips have negative net weight "
               f"({t['neg_net']/t['total']*100:.2f}%).")
if not t["zero_net"] and not t["neg_net"]:
    st.success("No zero or negative net-weight trips.")

st.subheader("Null rates on key columns (transactions)")
nulls = {
    "num_ticket": t["null_ticket"], "tipo_servicio": t["null_servicio"],
    "empresa": t["null_empresa"], "sector": t["null_sector"],
    "fec_ingreso": t["null_fecha"], "peso_neto": t["null_neto"],
}
cols = st.columns(len(nulls))
for (name, n), col in zip(nulls.items(), cols):
    pct = n / t["total"] * 100 if t["total"] else 0
    col.metric(name, f"{n:,}", f"{pct:.2f}%")

st.divider()
st.subheader("Date range per year")
st.dataframe(rep["date_range_by_year"], use_container_width=True, hide_index=True)

st.divider()
r = rep["retirados"]
st.subheader("GEOCYCLE (retirados)")
c1, c2, c3 = st.columns(3)
c1.metric("Total rows", f"{r['total']:,}")
c2.metric("Non-positive net", f"{r['nonpos_net']:,}",
          help="net recovered <= 0")
c3.metric("Null date / org", f"{r['null_fecha']:,} / {r['null_org']:,}")

# --- Full source-data catalog (entire INFORMACIÓN folder) --------------------
st.divider()
st.subheader("Source data catalog — INFORMACIÓN folder")
st.caption(
    "Data model (sheets, columns) and row counts for every spreadsheet in the "
    "source ZIP — not just the four pesaje files loaded into DuckDB."
)

from pipeline.catalog import build_catalog  # noqa: E402

if q.catalog_count(con) == 0:
    st.info("The catalog hasn't been built yet. Scanning the full folder takes "
            "~30 seconds (it reads every spreadsheet in the ZIP).")
    if st.button("📇 Scan INFORMACIÓN folder & build catalog", type="primary"):
        box = st.status("Scanning…", expanded=True)
        build_catalog(con, on_status=lambda m: box.update(label=m))
        box.update(label="Catalog built.", state="complete")
        st.rerun()
else:
    tot = q.catalog_totals(con)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Spreadsheets", f"{tot['files']:,}")
    c2.metric("Sheets / tabs", f"{tot['sheets']:,}")
    c3.metric("Total rows (all)", f"{tot['rows']:,}")
    c4.metric("Loaded to DuckDB", "4 files")

    summary = q.catalog_summary(con)
    show = summary.rename(columns={
        "folder": "Folder", "file_name": "File", "file_type": "Type",
        "size_mb": "Size (MB)", "sheets": "Sheets", "total_rows": "Total rows",
        "loaded_table": "DuckDB table"})
    st.dataframe(show, use_container_width=True, hide_index=True)

    st.markdown("**Per-file data model** — expand a file for its sheets and columns.")
    for fname in summary["file_name"]:
        loaded = summary.loc[summary["file_name"] == fname, "loaded_table"].iloc[0]
        tag = "  ·  ✅ loaded" if isinstance(loaded, str) and loaded else ""
        with st.expander(f"{fname}{tag}"):
            sheets = q.catalog_sheets(con, fname)
            for _, srow in sheets.iterrows():
                badge = f" → `{srow['loaded_table']}`" if srow["loaded_table"] else ""
                st.markdown(
                    f"**{srow['sheet_name']}**{badge} — "
                    f"{srow['n_columns']} cols × {srow['n_rows']:,} rows")
                if srow["columns"] and srow["columns"] != "[]":
                    import json
                    cols = json.loads(srow["columns"])
                    st.caption(", ".join(cols) if cols else "—")

    if st.button("🔄 Rebuild catalog"):
        box = st.status("Rescanning…", expanded=True)
        build_catalog(con, on_status=lambda m: box.update(label=m))
        box.update(label="Catalog rebuilt.", state="complete")
        st.rerun()
