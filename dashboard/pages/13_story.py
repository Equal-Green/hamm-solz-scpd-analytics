import os, sys
_here = os.path.dirname(os.path.abspath(__file__))
for _p in (_here, os.path.dirname(_here), os.path.dirname(os.path.dirname(_here))):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import streamlit as st

from style import inject_css, render_header

inject_css()
render_header(
    "Story",
    "From extraordinary land to a regenerative business.",
    eyebrow="WHO WE ARE · STORY",
)

st.markdown(
    """
EqualGreen began with two compelling things and nothing connecting them to a
future: **extraordinary land** in Balsapamba — 300 acres of preserve and
regenerative farm — and a body of **sustainability technology and IP** with no
commercial home.

The work since has been to make regeneration *durable* by making it *viable*:

- a **nature preserve** that reforests and protects the valley,
- a **regenerative farm** practicing agroforestry and soil restoration,
- an **immersive eco-tourism experience** that invites people onto the land, and
- **sustainability tools** that turn years of environmental know-how into
  products others can use.

The throughline is simple: prove that a business can regenerate land, include
its community, and still stand on its own — then build the systems that let it
scale from local to national.
"""
)

st.info("✍️ **Draft copy.** Swap in EqualGreen's own founding story and milestones "
        "where you'd like the narrative to differ.", icon="✍️")
