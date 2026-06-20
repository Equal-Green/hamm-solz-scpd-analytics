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
    t("Guayaquil's Waste, in Three Years"),
    t("Every truckload weighed at the Las Iguanas landfill — Consorcio URVASEO, "
      "under CIRCULAREP — from 2023 to 2025."),
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
st.markdown(t("home.narrative").format(
    a=first_y, b=last_y, trips=f"{k['trips']:,}", tonnes=f"{k['tonnes']:,.0f}",
    avg=f"{k['avg_kg']:,.0f}", dir=t("grew") if growth >= 0 else t("fell"),
    growth=f"{growth:+.0f}%"))

c1, c2, c3, c4 = st.columns(4)
c1.metric(t("kpi.total_trips"), f"{k['trips']:,}")
c2.metric(t("kpi.net_tonnage"), f"{k['tonnes']:,.0f} t")
c3.metric(t("kpi.avg_per_trip"), f"{k['avg_kg']:,.0f} kg")
c4.metric(t("kpi.period"), f"{first_y}–{last_y}")

st.divider()
st.subheader(t("Key findings"))

f1, f2 = st.columns(2)
with f1:
    with st.container(border=True):
        st.markdown("#### 📈 " + t("Volume is rising" if growth >= 0
                                   else "Volume is falling"))
        st.markdown(t("home.card.volume").format(
            f=f"{t_first:,.0f}", fy=first_y, l=f"{t_last:,.0f}", ly=last_y,
            g=f"{growth:+.0f}%"))
    with st.container(border=True):
        st.markdown("#### ♻️ " + t("Recovery is small but real"))
        st.markdown(t("home.card.recovery").format(
            rec=f"{recovered:,.0f}", pct=f"{recovery_pct:.2f}%"))
with f2:
    with st.container(border=True):
        st.markdown("#### ⚠️ " + t("One service category spiked"))
        st.markdown(t("home.card.spike").format(
            pct=f"{an['pct']:+.0f}%", y23=f"{an['y2023']:,}", y24=f"{an['y2024']:,}"))
    with st.container(border=True):
        st.markdown("#### 🚛 " + t("One operator dominates"))
        st.markdown(t("home.card.operator").format(
            company=lead_company, share=f"{lead_share:.0f}%"))

if clean:
    st.success(t("home.clean"))

st.divider()
st.subheader(t("How to read this dashboard"))
st.markdown(t("home.howto"))
st.caption(t("Use the grouped navigation in the sidebar."))
