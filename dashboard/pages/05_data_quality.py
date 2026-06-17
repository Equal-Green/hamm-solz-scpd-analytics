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
