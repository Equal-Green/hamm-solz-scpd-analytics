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

st.set_page_config(page_title="Service Types · SCPD", page_icon="🧾", layout="wide")
con = get_db()
ensure_loaded(con)

st.title("🧾 Service Types")

# Anomaly callout
an = q.servicios_especial_anomaly(con)
if an["pct"] is not None:
    st.error(
        f"⚠️ **Anomaly — SERVICIOS ESPECIAL trip spike.** "
        f"Trips rose **{an['pct']:+.1f}%** from **{an['y2023']:,}** (2023) to "
        f"**{an['y2024']:,}** (2024). "
        f"(The project brief labelled this ~+83%; the live figure from the data "
        f"is {an['pct']:+.0f}%.)"
    )

years = q.years(con)
year = st.selectbox("Filter by year", ["All"] + [str(y) for y in years])
yf = None if year == "All" else int(year)

ss = q.service_summary(con, yf)
col_a, col_b = st.columns(2)
with col_a:
    fig = px.bar(ss, x="trips", y="tipo_servicio", orientation="h",
                 color="tipo_servicio", color_discrete_map=SERVICE_COLORS,
                 color_discrete_sequence=SEQUENCE, text_auto=".2s")
    fig.update_layout(showlegend=False, yaxis=dict(autorange="reversed"))
    st.plotly_chart(apply_layout(fig, "Trips by service type"),
                    use_container_width=True)
with col_b:
    fig2 = px.bar(ss, x="tonnes", y="tipo_servicio", orientation="h",
                  color="tipo_servicio", color_discrete_map=SERVICE_COLORS,
                  color_discrete_sequence=SEQUENCE, text_auto=".2s")
    fig2.update_layout(showlegend=False, yaxis=dict(autorange="reversed"))
    st.plotly_chart(apply_layout(fig2, "Net tonnage by service type"),
                    use_container_width=True)

st.divider()
st.subheader("Year-over-year trips by service")
yoy = q.service_yoy(con)
st.dataframe(yoy, use_container_width=True, hide_index=True)
st.caption("`A->B %` columns show the year-over-year change in trip count.")
