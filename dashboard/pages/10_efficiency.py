import os, sys
_here = os.path.dirname(os.path.abspath(__file__))
for _p in (_here, os.path.dirname(_here), os.path.dirname(os.path.dirname(_here))):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import plotly.express as px
import streamlit as st

from db import get_db
from state import ensure_loaded
from style import inject_css, render_header
from theme import COLORS, apply_layout
from analysis import queries as q
from i18n import t

con = get_db()
inject_css()
ensure_loaded(con)

render_header(t("page.efficiency"),
              "Payload utilization, under-loaded trips, and weighbridge timing.",
              eyebrow=t("eyebrow.brand"))

DOW = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
years = q.years(con)
year = st.selectbox(t("word.filter_year"), [t("word.all")] + [str(y) for y in years])
yf = None if year == t("word.all") else int(year)

pv = q.payload_by_vehicle(con, yf)
# under-loaded threshold = half the fleet-wide median payload
med = con.execute("SELECT median(peso_neto) FROM transactions "
                  "WHERE peso_neto > 0").fetchone()[0] or 0
thr = round(med * 0.5)
ul = q.underloaded(con, thr, yf)

k1, k2, k3, k4 = st.columns(4)
k1.metric(t("kpi.median_payload"), f"{med:,.0f} kg")
k2.metric(t("kpi.under_threshold"), f"< {thr:,} kg")
pct = ul["under"] / ul["total"] * 100 if ul["total"] else 0
k3.metric(t("kpi.under_trips"), f"{ul['under']:,}", f"{pct:.0f}% of trips")
k4.metric(t("kpi.light_tonnage"), f"{ul['under_tonnes']:,.0f} t")

st.caption(
    f"“Under-loaded” = net payload below {thr:,} kg (half the fleet median). "
    "These are trucks dispatched well below capacity — candidates for route "
    "consolidation.")

st.divider()
col_a, col_b = st.columns(2)
with col_a:
    fig = px.bar(pv.sort_values("avg_kg"), x="avg_kg", y="tipo_vehiculo",
                 orientation="h", color_discrete_sequence=[COLORS["primary"]],
                 text_auto=".2s")
    st.plotly_chart(apply_layout(fig, "Avg payload by vehicle class (kg)",
                                 height=420), use_container_width=True)
with col_b:
    ph = q.payload_histogram(con, yf)
    ph["bin_label"] = ph["bin_t"].astype(int).astype(str) + "–" + \
        (ph["bin_t"].astype(int) + 2).astype(str) + "t"
    fig2 = px.bar(ph, x="bin_t", y="trips",
                  color_discrete_sequence=[COLORS["secondary"]])
    fig2.update_xaxes(title_text="net payload (tonnes)")
    st.plotly_chart(apply_layout(fig2, "Payload distribution"),
                    use_container_width=True)

st.divider()
st.subheader("Weighbridge activity — hour × day of week")
hd = q.hour_dow_matrix(con, yf)
if not hd.empty:
    pivot = hd.pivot(index="dow", columns="hr", values="trips").fillna(0)
    pivot = pivot.reindex(range(7)).fillna(0)
    pivot.index = DOW
    fig3 = px.imshow(pivot, aspect="auto", color_continuous_scale="YlOrRd",
                     labels=dict(x="hour of day", y="", color="trips"))
    fig3.update_layout(height=360, margin=dict(l=8, r=8, t=10, b=8),
                       font=dict(family="Inter", color="#141414"))
    st.plotly_chart(fig3, use_container_width=True)
    st.caption("Where the day's arrivals concentrate — peaks are weighbridge "
               "congestion windows worth staffing for.")
