import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import os, sys
_here = os.path.dirname(os.path.abspath(__file__))
for _p in (_here, os.path.dirname(_here), os.path.dirname(os.path.dirname(_here))):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from db import get_db
from state import ensure_loaded
from theme import YEAR_COLORS, SERVICE_COLORS, SEQUENCE, apply_layout
from analysis import queries as q
from style import inject_css, render_header
from i18n import t

con = get_db()
inject_css()
ensure_loaded(con)

render_header(t("page.overview"), "Volume and tonnage trends across 2023–2025.")

k = q.kpis(con)
c1, c2, c3, c4 = st.columns(4)
c1.metric(t("kpi.total_trips"), f"{k['trips']:,}")
c2.metric(t("kpi.total_net_tonnage"), f"{k['tonnes']:,.0f} t")
c3.metric(t("kpi.avg_per_trip"), f"{k['avg_kg']:,.0f} kg")
c4.metric(t("kpi.date_range"),
          f"{k['first_dt']:%Y}–{k['last_dt']:%Y}" if k["first_dt"] else "—")

st.divider()

# Monthly trip volume, years overlaid
mt = q.monthly_trips(con)
fig = go.Figure()
for year in sorted(mt["source_year"].unique()):
    d = mt[mt["source_year"] == year]
    fig.add_trace(go.Scatter(
        x=d["mes"], y=d["trips"], mode="lines+markers", name=str(year),
        line=dict(color=YEAR_COLORS.get(year), width=2.5)))
fig.update_xaxes(tickmode="array", tickvals=list(range(1, 13)),
                 ticktext=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
st.plotly_chart(apply_layout(fig, "Monthly trip volume (years overlaid)"),
                use_container_width=True)

col_a, col_b = st.columns(2)

with col_a:
    at = q.annual_tonnage(con)
    at["year_str"] = at["year"].astype(str)
    fig2 = px.bar(at, x="year_str", y="tonnes", color="year_str",
                  color_discrete_map={str(y): c for y, c in YEAR_COLORS.items()},
                  text_auto=".2s")
    fig2.update_layout(showlegend=False)
    fig2.update_xaxes(type="category", title_text="")
    st.plotly_chart(apply_layout(fig2, "Total annual net tonnage"),
                    use_container_width=True)

with col_b:
    mts = q.monthly_tonnage_by_service(con)
    fig3 = px.bar(mts, x="mes", y="tonnes", color="tipo_servicio",
                  color_discrete_map=SERVICE_COLORS,
                  color_discrete_sequence=SEQUENCE)
    fig3.update_xaxes(tickmode="array", tickvals=list(range(1, 13)),
                      ticktext=["J", "F", "M", "A", "M", "J",
                                "J", "A", "S", "O", "N", "D"])
    fig3.update_layout(barmode="stack", legend_title_text="")
    st.plotly_chart(apply_layout(fig3, "Monthly tonnage by service type"),
                    use_container_width=True)
