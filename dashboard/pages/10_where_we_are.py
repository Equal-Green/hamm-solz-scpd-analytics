import os, sys
_here = os.path.dirname(os.path.abspath(__file__))
for _p in (_here, os.path.dirname(_here), os.path.dirname(os.path.dirname(_here))):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import streamlit as st

from style import inject_css, render_header

_ASSETS = os.path.join(os.path.dirname(_here), "assets")

inject_css()
render_header(
    "Where we are",
    "Balsapamba, Ecuador — a 300-acre nature preserve and regenerative farm.",
    eyebrow="WHO WE ARE · WHERE WE ARE",
)

left, right = st.columns([1.4, 1])
with left:
    st.markdown(
        """
**EqualGreen** stewards land in **Balsapamba**, a parish in Ecuador's Bolívar
Province on the western foothills of the Andes — a humid, waterfall-fed valley
where the highlands fall toward the coast.

Here we grow and manage a **nature preserve, a regenerative farm, and an
immersive eco-tourism experience** on roughly **300 acres**. The land is the
product: every guest stay, every harvest, and every restored hectare is part of
the same regenerative system.
"""
    )
    st.markdown("##### What we do on the land")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            "- 🌳 **Nature preserve & reforestation**\n"
            "- 🌱 **Regenerative agriculture & agroforestry**"
        )
    with c2:
        st.markdown(
            "- 🏞️ **Eco-tourism & cultural experiences**\n"
            "- 🤝 **Community-driven land stewardship**"
        )

with right:
    card = os.path.join(_ASSETS, "balsapamba-card.png")
    if os.path.exists(card):
        st.image(card, use_container_width=True)

st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("Preserve & farm", "300 acres")
m2.metric("Region", "Bolívar, Ecuador")
m3.metric("Model", "Regenerative")
