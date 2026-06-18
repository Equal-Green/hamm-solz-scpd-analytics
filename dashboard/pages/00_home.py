import os, sys
_here = os.path.dirname(os.path.abspath(__file__))
for _p in (_here, os.path.dirname(_here), os.path.dirname(os.path.dirname(_here))):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import streamlit as st

from db import get_db
from state import ensure_loaded
from style import inject_css, render_header
from i18n import t
from analysis import queries as q

con = get_db()
inject_css()
ensure_loaded(con)

render_header(
    "Guayaquil's Waste, in Three Years",
    "Every truckload weighed at the Las Iguanas landfill — Consorcio URVASEO, "
    "under CIRCULAREP — from 2023 to 2025.",
)

# --- headline numbers --------------------------------------------------------
k = q.kpis(con)
at = q.annual_tonnage(con)
an = q.servicios_especial_anomaly(con)
rv = q.recovery_vs_landfill(con)
rep = q.quality_report(con)
top = q.top_empresas(con, n=1)

first_y, last_y = int(at["year"].iloc[0]), int(at["year"].iloc[-1])
t_first, t_last = at["tonnes"].iloc[0], at["tonnes"].iloc[-1]
growth = (t_last - t_first) / t_first * 100 if t_first else 0
recovered = rv["recovery_t"].sum()
landfilled = rv["landfill_t"].sum()
recovery_pct = recovered / landfilled * 100 if landfilled else 0
clean = (rep["transactions"]["zero_net"] == 0
         and rep["transactions"]["neg_net"] == 0
         and rep["transactions"]["null_servicio"] == 0)
lead_company = top["empresa"].iloc[0] if len(top) else "—"
lead_share = (top["trips"].iloc[0] / k["trips"] * 100) if len(top) else 0

# --- the story ---------------------------------------------------------------
st.markdown(
    f"""
Between **{first_y} and {last_y}**, **{k['trips']:,} truckloads** crossed the
Las Iguanas weighbridge, delivering **{k['tonnes']:,.0f} tonnes** of municipal
solid waste — an average of **{k['avg_kg']:,.0f} kg per trip**. Annual tonnage
{'grew' if growth >= 0 else 'fell'} **{growth:+.0f}%** over the period.
This dashboard walks through *what* arrived, *who* brought it, *how much* was
recovered, and *how much you can trust the numbers* — and lets you ask the data
questions directly.
"""
)

c1, c2, c3, c4 = st.columns(4)
c1.metric(t("kpi.total_trips"), f"{k['trips']:,}")
c2.metric(t("kpi.net_tonnage"), f"{k['tonnes']:,.0f} t")
c3.metric(t("kpi.avg_per_trip"), f"{k['avg_kg']:,.0f} kg")
c4.metric(t("kpi.period"), f"{first_y}–{last_y}")

st.divider()
st.subheader("Key findings")

f1, f2 = st.columns(2)
with f1:
    with st.container(border=True):
        st.markdown(f"#### 📈 Volume is {'rising' if growth>=0 else 'falling'}")
        st.markdown(
            f"Net tonnage moved from **{t_first:,.0f} t** in {first_y} to "
            f"**{t_last:,.0f} t** in {last_y} (**{growth:+.0f}%**)."
        )
    with st.container(border=True):
        st.markdown("#### ♻️ Recovery is small but real")
        st.markdown(
            f"GEOCYCLE diverted **{recovered:,.0f} t** for material recovery — "
            f"about **{recovery_pct:.2f}%** of everything landfilled."
        )
with f2:
    with st.container(border=True):
        st.markdown("#### ⚠️ One service category spiked")
        st.markdown(
            f"**SERVICIOS ESPECIAL** trips jumped **{an['pct']:+.0f}%** from "
            f"{an['y2023']:,} (2023) to {an['y2024']:,} (2024) — the standout "
            f"anomaly in the data."
        )
    with st.container(border=True):
        st.markdown("#### 🚛 One operator dominates")
        st.markdown(
            f"**{lead_company}** alone accounts for **{lead_share:.0f}%** of all "
            f"trips — the municipal collection consortium."
        )

if clean:
    st.success(
        "✅ **The data is clean.** No zero or negative net weights, no missing "
        "service types, no duplicate tickets. Full integrity checks on the "
        "**Data Quality & Catalog** page."
    )

st.divider()
st.subheader("How to read this dashboard")
st.markdown(
    "- **The story →** *Overview, Service Types, Operators & Fleet, GEOCYCLE "
    "Recovery* — the narrative, in order.\n"
    "- **Explore →** *Ask the Data* — put questions to the dataset and get "
    "instant answers.\n"
    "- **Trust & data →** *Data Quality & Catalog* — integrity checks plus a "
    "model of every spreadsheet in the source archive.\n"
    "- **System →** *Settings* — pipeline status, reloads, cloud export."
)
st.caption("Use the grouped navigation in the sidebar.")
