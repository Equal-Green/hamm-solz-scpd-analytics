import os, sys
_here = os.path.dirname(os.path.abspath(__file__))
for _p in (_here, os.path.dirname(_here), os.path.dirname(os.path.dirname(_here))):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import streamlit as st

from style import inject_css, render_header

inject_css()
render_header(
    "Quichua",
    "The land carries an Indigenous name.",
    eyebrow="WHO WE ARE · QUICHUA",
)

st.markdown(
    """
**Balsapamba** is a **Quichua (Kichwa)** place name — the language of the Andean
Indigenous peoples of Ecuador. It reads as two roots:

- **balsa** — the *balsa* tree (*Ochroma*), the fast-growing, light-wood species
  abundant in these humid foothills.
- **pamba** *(also* **bamba***)* — a flat, open **plain** or **field**.

Together: **“the plain of the balsa trees.”** The name is a reminder that the
land was named for what grew here long before it was a preserve — and that
stewarding it well means honoring that heritage, not overwriting it.
"""
)

c1, c2 = st.columns(2)
with c1:
    with st.container(border=True):
        st.markdown("#### balsa")
        st.caption("The balsa tree — *Ochroma pyramidale*, native to the region.")
with c2:
    with st.container(border=True):
        st.markdown("#### pamba")
        st.caption("Kichwa for an open plain or field (*pamba / bamba*).")

st.info("✍️ **Draft copy.** Please confirm the Kichwa etymology and the cultural "
        "framing with EqualGreen / a Kichwa speaker before publishing.", icon="✍️")
