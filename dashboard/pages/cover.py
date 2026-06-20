import os, sys
_here = os.path.dirname(os.path.abspath(__file__))
for _p in (_here, os.path.dirname(_here), os.path.dirname(os.path.dirname(_here))):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import streamlit as st

from style import inject_css, hamm_wordmark, eg_logo_html
from i18n import t

inject_css()

# --- co-branded logo lockup: HAMM Solz × EqualGreen --------------------------
st.markdown(
    f"""
    <div style="display:flex;align-items:center;justify-content:center;gap:2rem;
                flex-wrap:wrap;margin:2.4rem 0 1.4rem 0;">
        {hamm_wordmark(on_dark=False, height=40)}
        <span style="font-size:2rem;color:#BFBFBF;font-weight:300;">×</span>
        {eg_logo_html(64)}
        <span style="font-family:'Playfair Display',serif;font-weight:800;
                     font-size:1.6rem;color:#141414;">EqualGreen</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- title block -------------------------------------------------------------
st.markdown(
    """
    <div style="text-align:center;padding:1.2rem 0 0.4rem 0;">
      <div style="font-family:'JetBrains Mono',monospace;color:#DC2828;
                  letter-spacing:.18em;font-weight:700;font-size:.8rem;">
        """ + t("MUNICIPAL SOLID WASTE ANALYTICS") + """</div>
      <h1 style="font-family:'Playfair Display',serif;font-weight:900;
                 color:#141414;font-size:2.8rem;margin:.4rem 0 .2rem 0;
                 letter-spacing:-.02em;line-height:1.08;">
        Sistema de Control y Pesaje<br>de Desechos — Guayaquil</h1>
      <div style="color:#5F5F5F;font-size:1.05rem;font-weight:500;">
        Las Iguanas landfill · Consorcio URVASEO · CIRCULAREP · 2023–2025</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"**{t('Prepared for')}**")
    st.markdown("THE HAMM Solz Co., Ltd.  \n"
                "_Total Energy & Environment Consultant_  \n"
                "Gangnam-gu, Seoul, Korea")
with c2:
    st.markdown(f"**{t('Prepared by')}**")
    st.markdown("EqualGreen × Flaming Owl  \n"
                f"_{t('Data & analytics')}_")
with c3:
    st.markdown(f"**{t('Scope')}**")
    st.markdown(f"{t('516,526 weighbridge trips')}  \n"
                f"{t('5.9M tonnes · 2023–2025')}  \n"
                f"{t('20 source datasets')}")

st.divider()
st.markdown(
    "<div style='text-align:center;color:#8a8a8a;font-size:.85rem;'>"
    + t("cover.footer") + "</div>", unsafe_allow_html=True)
