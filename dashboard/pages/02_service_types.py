import plotly.express as px
import streamlit as st

import os, sys
_here = os.path.dirname(os.path.abspath(__file__))
for _p in (_here, os.path.dirname(_here), os.path.dirname(os.path.dirname(_here))):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from db import get_db
from state import ensure_loaded
from theme import SERVICE_COLORS, SEQUENCE, COLORS, apply_layout
from analysis import queries as q
from style import inject_css, render_header
from i18n import t

con = get_db()
inject_css()
ensure_loaded(con)

render_header(t("page.services"), t("Trips and tonnage by waste service category."))

# Anomaly callout
an = q.servicios_especial_anomaly(con)
if an["pct"] is not None:
    st.error(t("sv.anomaly").format(
        pct=f"{an['pct']:+.1f}%", y23=f"{an['y2023']:,}", y24=f"{an['y2024']:,}",
        pct0=f"{an['pct']:+.0f}%"))

years = q.years(con)
year = st.selectbox(t("word.filter_year"), [t("word.all")] + [str(y) for y in years])
yf = None if year == t("word.all") else int(year)

ss = q.service_summary(con, yf)
col_a, col_b = st.columns(2)
with col_a:
    fig = px.bar(ss, x="trips", y="tipo_servicio", orientation="h",
                 color="tipo_servicio", color_discrete_map=SERVICE_COLORS,
                 color_discrete_sequence=SEQUENCE, text_auto=".2s")
    fig.update_layout(showlegend=False, yaxis=dict(autorange="reversed"))
    st.plotly_chart(apply_layout(fig, t("Trips by service type")),
                    use_container_width=True)
with col_b:
    fig2 = px.bar(ss, x="tonnes", y="tipo_servicio", orientation="h",
                  color="tipo_servicio", color_discrete_map=SERVICE_COLORS,
                  color_discrete_sequence=SEQUENCE, text_auto=".2s")
    fig2.update_layout(showlegend=False, yaxis=dict(autorange="reversed"))
    st.plotly_chart(apply_layout(fig2, t("Net tonnage by service type")),
                    use_container_width=True)

st.divider()
st.subheader(t("Year-over-year trips by service"))
yoy = q.service_yoy(con)
st.dataframe(yoy, use_container_width=True, hide_index=True)
st.caption(t("`A->B %` columns show the year-over-year change in trip count."))
