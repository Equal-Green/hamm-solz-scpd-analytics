import os, sys
_here = os.path.dirname(os.path.abspath(__file__))
for _p in (_here, os.path.dirname(_here), os.path.dirname(os.path.dirname(_here))):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import streamlit as st

from style import inject_css, render_header

inject_css()
render_header(
    "The name",
    "EqualGreen — what it stands for.",
    eyebrow="WHO WE ARE · THE NAME",
)

st.markdown(
    """
**EqualGreen** joins two ideas the company refuses to treat as separate:
**equity** and a **green, regenerative future**.

- **Equal** — sustainability that includes the people on the land, not just the
  carbon on a balance sheet. Community-driven stewardship, fair work, shared
  upside.
- **Green** — regeneration as the standard: restoring soil, forest, and water
  rather than merely extracting less.

The name is a promise that the environmental and the human gains move together —
that a regenerative business should leave both the land and its community better
off than it found them.
"""
)

st.info("✍️ **Draft copy.** Replace with EqualGreen's official naming story so "
        "this reads in the founders' own words.", icon="✍️")
