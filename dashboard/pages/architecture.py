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
              "The technology behind your deliverable — DuckDB + Streamlit.")

st.markdown(
    "Your report isn't a static PDF or a spreadsheet — it's a small, "
    "**self-contained analytics application**. It runs entirely on one machine "
    "with **no database server, no cloud account, and no subscriptions**. Two "
    "open-source technologies make that possible.")

c1, c2 = st.columns(2)
with c1:
    with st.container(border=True):
        st.markdown("### 🦆 DuckDB — the engine")
        st.markdown(
            "DuckDB is an **analytical database that lives in a single file** "
            "(`scpd.duckdb`). Think of it as *“SQLite for analytics”*: it needs "
            "no server to install or run, yet it crunches hundreds of millions "
            "of values in milliseconds because it's **columnar** — built for "
            "summing, grouping and filtering, exactly what a report does.")
with c2:
    with st.container(border=True):
        st.markdown("### 🎈 Streamlit — the interface")
        st.markdown(
            "Streamlit turns Python analysis into an **interactive web app** — "
            "the pages, charts, filters and maps you're clicking now. Every "
            "control re-runs a query against DuckDB and redraws instantly. No "
            "front-end engineering, no separate web server to manage.")

st.divider()
st.subheader("How the data flows")
st.markdown(
    "```\n"
    "  ┌─────────────────┐   extract &     ┌──────────────┐   SQL queries   ┌────────────┐\n"
    "  │  INFORMACIÓN.zip│   transform     │  scpd.duckdb │   (instant)     │  Streamlit │\n"
    "  │  (6 GB source)  │ ──────────────► │  one file    │ ──────────────► │  dashboard │\n"
    "  │  20 spreadsheets│   (one-time     │  ~½ million   │                 │  (this UI) │\n"
    "  │  + KML + docs   │    pipeline)    │  rows, typed │                 │            │\n"
    "  └─────────────────┘                 └──────────────┘                 └────────────┘\n"
    "        raw                              the warehouse                   the report\n"
    "```")

st.markdown(
    "1. **Extract & transform (once).** A Python pipeline reads the source ZIP, "
    "parses the large Excel files row-by-row (they're too big to open normally), "
    "cleans dates and weights, and loads everything into DuckDB. This runs once; "
    "after that the app starts instantly.\n"
    "2. **Store.** All ~524,000 weighbridge records plus every other source "
    "table live in the single `scpd.duckdb` file — the portable *warehouse*.\n"
    "3. **Serve.** Each page asks DuckDB a question in SQL (\"net tonnage by "
    "zone in 2024\") and Streamlit renders the answer as a chart, table or map.")

st.divider()
st.subheader("Why this approach")
a, b, c = st.columns(3)
a.markdown("**Portable**  \nThe whole report is a folder. Clone it, point it at "
           "the data, run one command. No servers to provision.")
b.markdown("**Fast & offline**  \nColumnar queries return in milliseconds, with "
           "no internet required (except map tiles).")
c.markdown("**Reproducible**  \nThe pipeline is code. Re-run it on next year's "
           "data and the same report rebuilds itself.")

st.divider()
st.subheader("What it took to get here")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Source size", "6 GB ZIP")
m2.metric("Rows loaded", "~524,000")
m3.metric("Load time (one-time)", "~4 min")
m4.metric("Query response", "milliseconds")
st.caption(
    "Note on the source files: the delivery ZIP uses a streaming format that "
    "standard tools can't open, and the main Excel files are 65–92 MB each "
    "(one sheet expands to ~450 MB of XML). The pipeline reads them with custom "
    "binary + streaming parsers — a one-time engineering step so the day-to-day "
    "report stays simple and instant.")

st.divider()
st.subheader("Path to the cloud (optional, Phase 2)")
st.markdown(
    "Everything above runs **locally and offline**. When you want it hosted, "
    "the same app deploys to a small container (e.g. Google Cloud Run or "
    "Render) with the prebuilt `scpd.duckdb` baked in — or its tables export to "
    "a Postgres / Supabase database. The hooks are already in **Settings**; "
    "the offline version keeps working regardless.")
