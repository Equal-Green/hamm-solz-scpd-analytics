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
from theme import COLORS, apply_layout
from analysis import queries as q
from style import inject_css, render_header
from i18n import t

con = get_db()
inject_css()
ensure_loaded(con)

render_header(t("page.geocycle"), t("Material recovery — inverted weigh logic."), eyebrow="SCPD ANALYTICS · RECOVERY")
st.info(t("gc.inverted"))

rk = q.retirados_kpis(con)
c1, c2, c3, c4 = st.columns(4)
c1.metric(t("kpi.recovery_trips"), f"{rk['trips']:,}")
c2.metric(t("kpi.recovered_tonnage"), f"{rk['tonnes']:,.0f} t")
c3.metric(t("kpi.organizations"), f"{rk['orgs']:,}")
c4.metric(t("kpi.date_range"),
          f"{rk['first_dt']:%Y}–{rk['last_dt']:%Y}" if rk["first_dt"] else "—")

st.divider()

rm = q.retirados_monthly(con)
fig = px.bar(rm, x="month", y="tonnes",
             color_discrete_sequence=[COLORS["success"]])
st.plotly_chart(apply_layout(fig, t("Monthly recovered tonnage")),
                use_container_width=True)

st.subheader(t("Recovery vs. landfill volume"))
rv = q.recovery_vs_landfill(con)
fig2 = go.Figure()
fig2.add_bar(x=rv["year"], y=rv["landfill_t"], name="Landfilled",
             marker_color=COLORS["primary"])
fig2.add_bar(x=rv["year"], y=rv["recovery_t"], name="Recovered",
             marker_color=COLORS["success"])
fig2.update_layout(barmode="group")
fig2.update_xaxes(type="category")
st.plotly_chart(apply_layout(fig2, t("Landfilled vs. recovered tonnage by year")),
                use_container_width=True)

show = rv.copy()
show["landfill_t"] = show["landfill_t"].round(0)
show["recovery_t"] = show["recovery_t"].round(1)
show["recovery_pct"] = show["recovery_pct"].round(3)
st.dataframe(show, use_container_width=True, hide_index=True,
             column_config={"recovery_pct": "recovery % of landfill"})
