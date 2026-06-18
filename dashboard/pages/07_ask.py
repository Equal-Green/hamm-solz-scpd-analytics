import os, sys
_here = os.path.dirname(os.path.abspath(__file__))
for _p in (_here, os.path.dirname(_here), os.path.dirname(os.path.dirname(_here))):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import streamlit as st

from db import get_db
from state import ensure_loaded
from style import inject_css, render_header
from i18n import t
import ask_engine as ae

con = get_db()
inject_css()
ensure_loaded(con)

render_header(t("page.ask"),
    "Put questions to the SCPD dataset — pick a suggestion or type your own.",
    eyebrow="SCPD ANALYTICS · EXPLORE",
)

if "ask_history" not in st.session_state:
    st.session_state.ask_history = []


def _render_answer(ask_id):
    """Recompute and render an answer (cheap DuckDB queries)."""
    ask = ae.get(ask_id)
    if ask is None:
        st.markdown(
            "I can't map that to the data yet. Try one of the suggested "
            "questions above — they cover volume, service mix, operators, "
            "recovery, and data quality."
        )
        return
    ans = ask["run"](con)
    st.markdown(ans.get("summary", ""))
    if ans.get("fig") is not None:
        st.plotly_chart(ans["fig"], use_container_width=True,
                        key=f"{ask_id}_{len(st.session_state.ask_history)}")
    if ans.get("table") is not None:
        st.dataframe(ans["table"], use_container_width=True, hide_index=True)


def _ask(question_text, ask_id):
    st.session_state.ask_history.append({"q": question_text, "id": ask_id})


# --- suggestion chips, grouped by theme -------------------------------------
st.markdown("##### 💡 Suggested questions")
for cat, asks in ae.grouped().items():
    st.caption(cat)
    cols = st.columns(2)
    for i, a in enumerate(asks):
        if cols[i % 2].button(a["label"], key=f"sugg_{a['id']}",
                              use_container_width=True):
            _ask(a["label"], a["id"])
            st.rerun()

st.divider()

# --- conversation transcript -------------------------------------------------
if not st.session_state.ask_history:
    st.info("Pick a question above, or type one below — e.g. *“who hauls the "
            "most waste?”* or *“is volume growing?”*")
else:
    if st.button("🧹 Clear conversation"):
        st.session_state.ask_history = []
        st.rerun()
    for turn in st.session_state.ask_history:
        with st.chat_message("user"):
            st.markdown(turn["q"])
        with st.chat_message("assistant"):
            _render_answer(turn["id"])

# --- free-text input ---------------------------------------------------------
prompt = st.chat_input("Ask a question about the data…")
if prompt:
    _ask(prompt, ae.route(prompt))
    st.rerun()
