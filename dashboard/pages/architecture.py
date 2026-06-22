import os, sys
_here = os.path.dirname(os.path.abspath(__file__))
for _p in (_here, os.path.dirname(_here), os.path.dirname(os.path.dirname(_here))):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import streamlit as st

from style import inject_css, render_header
from i18n import t

inject_css()
render_header(t("page.arch"),
              t("The technology behind your deliverable — DuckDB + Streamlit."))

st.markdown(t("arch.intro"))

c1, c2 = st.columns(2)
with c1:
    with st.container(border=True):
        st.markdown(t("arch.duck.h"))
        st.markdown(t("arch.duck.b"))
with c2:
    with st.container(border=True):
        st.markdown(t("arch.stream.h"))
        st.markdown(t("arch.stream.b"))

st.divider()
st.subheader(t("How the data flows"))
st.markdown(
    "```\n"
    "  ┌─────────────────┐   extract &     ┌──────────────┐   SQL queries   ┌────────────┐\n"
    "  │  INFORMACIÓN.zip│   transform     │  scpd.duckdb │   (instant)     │  Streamlit │\n"
    "  │  (6 GB source)  │ ──────────────► │  one file    │ ──────────────► │  dashboard │\n"
    "  │  20 spreadsheets│   (one-time     │  ~½ million   │                 │  (this UI) │\n"
    "  │  + KML + docs   │    pipeline)    │  rows, typed │                 │            │\n"
    "  └─────────────────┘                 └──────────────┘                 └────────────┘\n"
    "```")

st.markdown(t("arch.steps"))

st.divider()
st.subheader(t("Why this approach"))
a, b, c = st.columns(3)
a.markdown(t("arch.portable"))
b.markdown(t("arch.fast"))
c.markdown(t("arch.repro"))

st.divider()
st.subheader(t("What it took to get here"))
m1, m2, m3, m4 = st.columns(4)
m1.metric(t("Source size"), "6 GB ZIP")
m2.metric(t("Rows loaded"), "~524,000")
m3.metric(t("Load time (one-time)"), "~4 min")
m4.metric(t("Query response"), "ms")
st.caption(t("arch.note"))

st.divider()
st.subheader(t("Path to the cloud (optional, Phase 2)"))
st.markdown(t("arch.cloud"))
