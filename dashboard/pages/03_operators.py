import plotly.express as px
import streamlit as st

import os, sys
_here = os.path.dirname(os.path.abspath(__file__))
for _p in (_here, os.path.dirname(_here), os.path.dirname(os.path.dirname(_here))):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from db import get_db
from state import ensure_loaded
from theme import SEQUENCE, COLORS, apply_layout
from analysis import queries as q

st.set_page_config(page_title="Operators & Fleet · SCPD", page_icon="🚛", layout="wide")
con = get_db()
ensure_loaded(con)

st.title("🚛 Operators & Fleet")

c1, c2 = st.columns(2)
with c1:
    year = st.selectbox("Year", ["All"] + [str(y) for y in q.years(con)])
with c2:
    servicio = st.selectbox("Service type", ["All"] + q.services(con))
yf = None if year == "All" else int(year)
sf = None if servicio == "All" else servicio

top = q.top_empresas(con, yf, sf, n=10)

col_a, col_b = st.columns(2)
with col_a:
    fig = px.bar(top.sort_values("trips"), x="trips", y="empresa",
                 orientation="h", color_discrete_sequence=[COLORS["primary"]],
                 text_auto=".2s")
    st.plotly_chart(apply_layout(fig, "Top 10 companies by trips", height=420),
                    use_container_width=True)
with col_b:
    fig2 = px.bar(top.sort_values("tonnes"), x="tonnes", y="empresa",
                  orientation="h", color_discrete_sequence=[COLORS["secondary"]],
                  text_auto=".2s")
    st.plotly_chart(apply_layout(fig2, "Top 10 companies by net tonnage", height=420),
                    use_container_width=True)

st.divider()
col_c, col_d = st.columns([1, 1])
with col_c:
    vd = q.vehicle_distribution(con, yf, sf)
    # Collapse a long tail into "Other" for a readable pie.
    if len(vd) > 8:
        head = vd.head(7).copy()
        other = vd["trips"][7:].sum()
        head.loc[len(head)] = ["Other", other]
        vd = head
    fig3 = px.pie(vd, names="tipo_vehiculo", values="trips", hole=0.45,
                  color_discrete_sequence=SEQUENCE)
    fig3.update_traces(textposition="inside", textinfo="percent")
    st.plotly_chart(apply_layout(fig3, "Vehicle class distribution"),
                    use_container_width=True)
with col_d:
    st.subheader("Avg net weight per trip by company")
    show = top[["empresa", "trips", "tonnes", "avg_kg"]].copy()
    show["avg_kg"] = show["avg_kg"].round(0)
    show["tonnes"] = show["tonnes"].round(1)
    st.dataframe(show, use_container_width=True, hide_index=True,
                 column_config={"avg_kg": "avg kg/trip"})
