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
from style import inject_css, render_header
from i18n import t

con = get_db()
inject_css()
ensure_loaded(con)

render_header(t("page.operators"), t("Companies and vehicle classes delivering to the landfill."))

c1, c2 = st.columns(2)
with c1:
    year = st.selectbox(t("word.year"), [t("word.all")] + [str(y) for y in q.years(con)])
with c2:
    servicio = st.selectbox(t("word.service_type"), [t("word.all")] + q.services(con))
yf = None if year == t("word.all") else int(year)
sf = None if servicio == t("word.all") else servicio

top = q.top_empresas(con, yf, sf, n=10)

col_a, col_b = st.columns(2)
with col_a:
    fig = px.bar(top.sort_values("trips"), x="trips", y="empresa",
                 orientation="h", color_discrete_sequence=[COLORS["primary"]],
                 text_auto=".2s")
    st.plotly_chart(apply_layout(fig, t("Top 10 companies by trips"), height=420),
                    use_container_width=True)
with col_b:
    fig2 = px.bar(top.sort_values("tonnes"), x="tonnes", y="empresa",
                  orientation="h", color_discrete_sequence=[COLORS["secondary"]],
                  text_auto=".2s")
    st.plotly_chart(apply_layout(fig2, t("Top 10 companies by net tonnage"), height=420),
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
    st.plotly_chart(apply_layout(fig3, t("Vehicle class distribution")),
                    use_container_width=True)
with col_d:
    st.subheader(t("Avg net weight per trip by company"))
    show = top[["empresa", "trips", "tonnes", "avg_kg"]].copy()
    show["avg_kg"] = show["avg_kg"].round(0)
    show["tonnes"] = show["tonnes"].round(1)
    st.dataframe(show, use_container_width=True, hide_index=True,
                 column_config={"avg_kg": "avg kg/trip"})
