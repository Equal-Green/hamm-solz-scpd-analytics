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

render_header(t("page.integrity"),
              t("Where the SERVICIOS ESPECIAL spike came from, and weighbridge "
                "integrity flags."), eyebrow=t("eyebrow.brand"))

an = q.servicios_especial_anomaly(con)
st.error(t("in.anomaly").format(
    pct=f"{an['pct']:+.0f}%", y23=f"{an['y2023']:,}", y24=f"{an['y2024']:,}"))

# --- who drove the spike -----------------------------------------------------
eg = q.especial_growth_by_empresa(con)
eg = eg.fillna(0)
fig = px.bar(eg.sort_values("delta").tail(10), x="delta", y="empresa",
             orientation="h", color="delta",
             color_continuous_scale=["#0E7C86", "#E0A106", "#DC2828"],
             text_auto=True)
fig.update_layout(coloraxis_showscale=False)
st.plotly_chart(apply_layout(fig, t("SERVICIOS ESPECIAL — trip increase by operator (2023→2024)"),
                             height=430), use_container_width=True)
st.dataframe(eg, use_container_width=True, hide_index=True,
             column_config={"empresa": "Operator (RAZON_SOCIAL)",
                            "y2023": "2023", "y2024": "2024", "delta": "Δ trips"})

st.divider()
st.subheader(t("Weighbridge integrity flags"))
fl = q.integrity_flags(con)
dup = q.duplicate_weighings(con)
total = fl["total"] or 1
c1, c2, c3, c4 = st.columns(4)
c1.metric(t("kpi.dup_weighings"), f"{dup['groups']:,}",
          help="Same plate + same day + identical net weight")
c2.metric(t("kpi.tare_gross"), f"{fl['tare_gt_gross']:,}",
          help="PESO_SALIDA > PESO_INGRESO (inverted for a landfill trip)")
c3.metric(t("kpi.payload_outliers"), f"{fl['payload_outlier']:,}",
          help="Net weight > 45,000 kg")
c4.metric(t("kpi.missing_weight"), f"{fl['missing_weight']:,}")

st.markdown("**Duplicate-weighing candidates** — same plate, same day, "
            "identical net weight:")
st.dataframe(dup["sample"], use_container_width=True, hide_index=True,
             column_config={"placa": "PLACA", "dia": "Day",
                            "peso_neto": "Net kg", "repeats": "Repeats"})
st.caption(t("in.duplicates"))
