import os, sys
_here = os.path.dirname(os.path.abspath(__file__))
for _p in (_here, os.path.dirname(_here), os.path.dirname(os.path.dirname(_here))):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from db import get_db
from state import ensure_loaded
from style import inject_css, render_header
from theme import COLORS, SEQUENCE, apply_layout
from analysis import queries as q
from i18n import t

con = get_db()
inject_css()
ensure_loaded(con)

render_header(t("page.diversion"),
              "How much of what we bury could be diverted instead.",
              eyebrow=t("eyebrow.brand"))

k = q.kpis(con)
rv = q.recovery_vs_landfill(con)
landfilled = k["tonnes"]
recovered = rv["recovery_t"].sum()
cur_div = recovered / landfilled * 100 if landfilled else 0

c1, c2, c3 = st.columns(3)
c1.metric(t("kpi.landfilled"), f"{landfilled:,.0f} t")
c2.metric(t("kpi.geocycle_recovered"), f"{recovered:,.0f} t")
c3.metric(t("kpi.current_diversion"), f"{cur_div:.2f}%")

st.divider()
st.subheader("Composition & diversion scenario")
st.caption(
    "The source caracterización studies aren't a clean per-tonne table, so set "
    "the composition below (defaults reflect typical Ecuadorian municipal solid "
    "waste). Source studies are listed at the bottom for calibration.")

cc1, cc2, cc3 = st.columns(3)
organic = cc1.slider("Organic %", 0, 80, 55)
recyclable = cc2.slider("Recyclable % (paper, plastic, glass, metal)", 0, 60, 22)
capture = cc3.slider("Capture rate of divertible %", 0, 100, 40)
other = max(0, 100 - organic - recyclable)

comp = {"Organic": organic, "Recyclable": recyclable, "Other / residual": other}
fig = px.pie(names=list(comp), values=list(comp.values()), hole=0.5,
             color_discrete_sequence=[COLORS["success"], COLORS["secondary"],
                                      COLORS["slate"]])
fig.update_traces(textposition="inside", textinfo="percent+label")

divertible_t = landfilled * (organic + recyclable) / 100.0
achievable_t = divertible_t * capture / 100.0
new_rate = (recovered + achievable_t) / landfilled * 100 if landfilled else 0

col_a, col_b = st.columns([1, 1])
with col_a:
    st.plotly_chart(apply_layout(fig, "Assumed waste composition"),
                    use_container_width=True)
with col_b:
    fig2 = go.Figure(go.Bar(
        x=["Divertible (theoretical)", "Achievable @ capture", "Current recovery"],
        y=[divertible_t, achievable_t, recovered],
        marker_color=[COLORS["secondary"], COLORS["success"], COLORS["amber"]],
        text=[f"{v:,.0f} t" for v in [divertible_t, achievable_t, recovered]],
        textposition="outside"))
    st.plotly_chart(apply_layout(fig2, "Diversion potential (3-yr total)"),
                    use_container_width=True)

st.success(
    f"At **{capture}%** capture of the divertible fraction, diversion would rise "
    f"from **{cur_div:.2f}%** to **{new_rate:.1f}%** — about "
    f"**{achievable_t:,.0f} t** kept out of Las Iguanas over the period "
    f"(vs {recovered:,.0f} t recovered today).")

st.divider()
st.markdown("**Source characterization studies** (loaded in DuckDB for calibration):")
car = con.execute("""
    SELECT file_name, sheet_name, n_rows, n_columns
    FROM data_catalog
    WHERE upper(folder) LIKE '%CARACTERIZ%'
    ORDER BY file_name, id
""").df()
if not car.empty:
    st.dataframe(car, use_container_width=True, hide_index=True)
else:
    st.caption("Characterization tables not found in the catalog — build the "
               "catalog on the Data Quality page.")
