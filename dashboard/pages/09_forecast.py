import os, sys
_here = os.path.dirname(os.path.abspath(__file__))
for _p in (_here, os.path.dirname(_here), os.path.dirname(os.path.dirname(_here))):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from datetime import timedelta

import numpy as np
import pandas as pd
import plotly.graph_objects as go
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

render_header(t("page.forecast"), t("fc.subtitle"), eyebrow=t("eyebrow.brand"))

s = q.monthly_tonnage_series(con)
s = s[s["tonnes"] > 0].reset_index(drop=True)
if len(s) < 12:
    st.warning("Not enough monthly history to forecast.")
    st.stop()

# --- inputs ------------------------------------------------------------------
c1, c2, c3 = st.columns(3)
cap_mt = c1.number_input(t("fc.remaining_cap"), min_value=0.5, max_value=200.0,
                         value=20.0, step=0.5)
growth = c2.slider(t("fc.annual_growth"), -10, 20, 4) / 100.0
diversion = c3.slider(t("fc.diversion"), 0, 50, 0) / 100.0

# --- build a 60-month projection: trailing baseline × growth × seasonal index
hist = s.copy()
hist["month"] = pd.to_datetime(hist["month"])
last12 = hist.tail(12)
base_monthly = last12["tonnes"].mean()
# seasonal index from last 24 months
recent = hist.tail(24).copy()
recent["m"] = recent["month"].dt.month
seasonal = recent.groupby("m")["tonnes"].mean()
seasonal = (seasonal / seasonal.mean()).to_dict()

HORIZON = 120
last_date = hist["month"].iloc[-1]
eff_factor = 1 - diversion
proj_rows = []
for i in range(1, HORIZON + 1):
    d = last_date + pd.offsets.MonthBegin(i)
    yrs = i / 12.0
    val = base_monthly * ((1 + growth) ** yrs) * seasonal.get(d.month, 1.0)
    proj_rows.append({"month": d, "tonnes": val, "eff_tonnes": val * eff_factor})
proj = pd.DataFrame(proj_rows)

cap_tonnes = cap_mt * 1_000_000           # remaining capacity, tonnes
proj["cum"] = proj["eff_tonnes"].cumsum()  # after diversion
hit = proj[proj["cum"] >= cap_tonnes]
fill_date = hit["month"].iloc[0] if len(hit) else None
# baseline (no diversion) for the life-extension comparison
hit_base = proj[proj["tonnes"].cumsum() >= cap_tonnes]
fill_base = hit_base["month"].iloc[0] if len(hit_base) else None

# --- KPIs --------------------------------------------------------------------
k1, k2, k3 = st.columns(3)
if fill_date is not None:
    yrs_left = (fill_date - last_date).days / 365.25
    k1.metric(t("fc.proj_fill"), f"{fill_date:%b %Y}")
    k2.metric(t("fc.years_left"), f"{yrs_left:.1f}")
else:
    k1.metric(t("fc.proj_fill"), "> 10 yr")
    k2.metric(t("fc.years_left"), "> 10")
if diversion > 0 and fill_date is not None and fill_base is not None:
    ext = (fill_date - fill_base).days / 365.25
    k3.metric(t("fc.life_ext"), f"+{ext:.1f} yr")
else:
    k3.metric(t("fc.life_ext"), "—")

# --- chart 1: history + forecast ---------------------------------------------
fig = go.Figure()
fig.add_trace(go.Scatter(x=hist["month"], y=hist["tonnes"], mode="lines",
                         name="History", line=dict(color=COLORS["iron"], width=2)))
fig.add_trace(go.Scatter(x=proj["month"], y=proj["eff_tonnes"], mode="lines",
                         name="Forecast (after diversion)",
                         line=dict(color=COLORS["primary"], width=2, dash="dot")))
st.plotly_chart(apply_layout(fig, "Monthly net tonnage — history & forecast"),
                use_container_width=True)

# --- chart 2: cumulative vs capacity -----------------------------------------
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=proj["month"], y=proj["cum"], mode="lines",
                          name="Cumulative disposed", fill="tozeroy",
                          line=dict(color=COLORS["secondary"], width=2)))
fig2.add_hline(y=cap_tonnes, line_dash="dash", line_color=COLORS["danger"],
               annotation_text=f"Capacity {cap_mt:g} Mt",
               annotation_position="top left")
if fill_date is not None:
    fig2.add_vline(x=fill_date, line_dash="dot", line_color=COLORS["danger"])
st.plotly_chart(apply_layout(fig2, "Cumulative disposal vs. remaining capacity"),
                use_container_width=True)

st.info(t("fc.assumption"), icon="📉")
