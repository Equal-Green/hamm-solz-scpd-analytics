"""Agreement & Compliance — the signed consultancy agreement, scored.

Reads the contract model in compliance.py and the received-archive inventory,
then reports two honest numbers: compliance against what is owed *today*, and
completion of the full 90-day deliverable set.
"""
import os, sys
_here = os.path.dirname(os.path.abspath(__file__))
for _p in (_here, os.path.dirname(_here), os.path.dirname(os.path.dirname(_here))):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from datetime import date

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from style import inject_css, render_header
from theme import COLORS, apply_layout
from i18n import t, tr, notr
import compliance as C
from pipeline.archive import load_inventory
from config import TOTAL_EXPECTED_ROWS

inject_css()
render_header(t("page.compliance"), t("comp.subtitle"), eyebrow=t("eyebrow.brand"))

TODAY = date.today()
s = C.score(TODAY)

_BAND = {"good": COLORS["success"], "warn": COLORS["amber"],
         "bad": COLORS["danger"]}


def _band(fraction, elapsed):
    """Green when delivery keeps pace with the term, amber within 15 points."""
    if fraction >= max(elapsed, 0.95):
        return "good"
    return "warn" if fraction >= elapsed - 0.15 else "bad"


# --- Contract facts ----------------------------------------------------------
f1, f2, f3, f4 = st.columns(4)
f1.metric(t("comp.contract_day"), f"{s['day']} / {C.TERM_DAYS}",
          help=f"Effective Date {C.EFFECTIVE_DATE:%d %b %Y} (Clause 2)")
f2.metric(t("comp.days_remaining"),
          notr("expired") if s["expired"] else f"{s['days_remaining']}")
f3.metric(t("comp.term_ends"), notr(f"{C.END_DATE:%d %b %Y}"))
f4.metric(t("comp.contract_amount"),
          notr(f"USD {C.AGREEMENT['amount_usd']:,}"), help="Clause 7 — lump sum")

st.divider()

# --- Headline compliance -----------------------------------------------------
inv = load_inventory() or {}
annex3_rows, annex3_cat_frac = C.annex3_coverage(inv)
item_rows = C.annex3_item_rows(inv)
item_sum = C.annex3_item_summary(inv)

g1, g2 = st.columns([3, 2])
with g1:
    band = _band(s["to_date"], s["term_elapsed"])
    gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=round(s["to_date"] * 100, 1),
        number={"suffix": "%", "font": {"family": "JetBrains Mono", "size": 44}},
        delta={"reference": round(s["term_elapsed"] * 100, 1),
               "suffix": " pts vs term", "position": "bottom",
               "font": {"family": "Inter", "size": 15},
               "increasing": {"color": COLORS["success"]},
               "decreasing": {"color": COLORS["danger"]}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1,
                     "tickcolor": COLORS["muted"], "tickvals": [0, 50, 100]},
            "bar": {"color": _BAND[band], "thickness": 0.7},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 1.5, "bordercolor": COLORS["iron"],
            "steps": [{"range": [0, 100], "color": "rgba(20,20,20,0.05)"}],
            "threshold": {"line": {"color": COLORS["iron"], "width": 3},
                          "thickness": 0.85,
                          "value": round(s["term_elapsed"] * 100, 1)},
        },
    ))
    gauge.update_traces(domain={"x": [0.06, 0.94], "y": [0.16, 1.0]})
    st.plotly_chart(apply_layout(gauge, t("comp.gauge_title"), height=330),
                    use_container_width=True)
    st.caption(t("comp.gauge_caption"))

with g2:
    st.metric(t("comp.overall"), f"{s['overall'] * 100:.0f}%",
              help="Weighted across all six Annex 2 deliverables, including "
                   "those not yet due.")
    st.metric(t("comp.term_elapsed"), f"{s['term_elapsed'] * 100:.0f}%")
    st.metric(t("comp.annex3"), f"{item_sum['weighted'] * 100:.0f}%",
              help=f"{item_sum['received']} of {item_sum['total']} Annex 3 "
                   f"items fully answered by the delivered archive, "
                   f"{item_sum['partial']} partially (counted at half), "
                   f"{item_sum['none']} not delivered. Computed from the source "
                   f"archive, not declared. All "
                   f"{len(C.ANNEX3_CATEGORIES)} categories have some material, "
                   f"so the category-level rollup reads "
                   f"{annex3_cat_frac * 100:.0f}% — the item-level figure is "
                   f"the honest one.")
    sent, due = C.biweekly_progress(TODAY)
    st.metric(t("comp.reports_sent"), f"{sent} / {due}",
              help="Bi-weekly progress reports logged against those due so far.")

# --- Where we stand ----------------------------------------------------------
if s["at_risk"]:
    names = ", ".join(f"#{r['no']} {r['title']}" for r in s["at_risk"])
    st.error(notr(f"**{len(s['at_risk'])} {tr(t('comp.at_risk'))}** {names}"))
else:
    st.success(t("comp.on_track"))

if C.is_internal() and s["unverified"]:
    st.warning(notr(f"**{s['unverified']}** {tr(t('comp.unverified'))}"))

st.divider()

# --- Detail tabs -------------------------------------------------------------
tab_del, tab_mat, tab_ind, tab_scope, tab_terms = st.tabs([
    t("📋 Deliverables (Annex 2)"),
    t("📦 Materials received (Annex 3)"),
    t("✅ Indicators & implementation"),
    t("🚧 Scope guardrails"),
    t("📄 Agreement terms"),
])

_LABEL = {"complete": "✅ Complete", "in_progress": "🟡 In progress",
          "not_started": "🔴 Not started"}

with tab_del:
    st.markdown(t("comp.del_intro"))
    rows = []
    for r in s["rows"]:
        if r["due_day"] is None:
            due = "Ongoing"
        else:
            due = f"Day {r['due_day']} — {r['due_date']:%d %b %Y}"
        if not r["in_scope_now"]:
            state = "⏳ Not yet due"
        elif r["key"] == "biweekly_reports":
            sent, tot = C.biweekly_progress(TODAY)
            if not sent:
                key = "not_started"
            elif sent < tot:
                key = "in_progress"
            else:
                key = "complete"
            state = f"{_LABEL[key]} ({sent}/{tot})"
        else:
            state = _LABEL[r["status"]]
        rows.append({"#": r["no"], "Deliverable": r["title"], "Due": due,
                     "Weight": f"{r['weight']}%", "Status": state,
                     "Score": f"{r['fraction'] * 100:.0f}%"})
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.markdown(notr("#### " + tr(t("Contribution to the score"))))
    contrib = pd.DataFrame([
        {"deliverable": f"#{r['no']} {r['title']}",
         "earned": r["weight"] * r["fraction"],
         "outstanding": r["weight"] * (1 - r["fraction"])}
        for r in s["rows"]
    ])
    fig = go.Figure()
    fig.add_bar(y=contrib["deliverable"], x=contrib["earned"], name="Earned",
                orientation="h", marker_color=COLORS["success"])
    fig.add_bar(y=contrib["deliverable"], x=contrib["outstanding"],
                name="Outstanding", orientation="h",
                marker_color="rgba(20,20,20,0.13)")
    fig.update_layout(barmode="stack")
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(apply_layout(fig, t("Weighted points earned vs outstanding"),
                                 height=380), use_container_width=True)

    st.markdown(notr("#### " + tr(t("Minimum content and evidence"))))
    for r in s["rows"]:
        head = f"**#{r['no']} · {r['title']}** — {r['timing']}"
        with st.expander(f"{r['no']}. {r['title']}"):
            st.markdown(head)
            st.caption(r["content"])
            ev = [e.format(files=f"{inv.get('total_files', 0):,}",
                           folders=len(inv.get("folders", [])),
                           rows=f"{TOTAL_EXPECTED_ROWS:,}",
                           today=f"{TODAY:%d %B %Y}") for e in r["evidence"]]
            if ev:
                st.markdown("\n".join(f"- {e}" for e in ev))
            else:
                st.markdown(t("comp.no_evidence"))
            if r["key"] == "biweekly_reports":
                log = pd.DataFrame([
                    {"Report": f"Day {d}", "Due": f"{C.date_for_day(d):%d %b %Y}",
                     "Sent": C.BIWEEKLY_LOG.get(d) or "—"}
                    for d in C.biweekly_due_days()
                ])
                st.dataframe(log, use_container_width=True, hide_index=True)

with tab_mat:
    st.markdown(t("comp.mat_intro"))

    i1, i2, i3 = st.columns(3)
    i1.metric(t("comp.items_received"), f"{item_sum['received']} / "
              f"{item_sum['total']}")
    i2.metric(t("comp.items_partial"), f"{item_sum['partial']}")
    i3.metric(t("comp.items_none"), f"{item_sum['none']}")

    _COV = {"received": "✅ Received", "partial": "🟡 Partial",
            "none": "🔴 Not delivered"}
    st.dataframe(pd.DataFrame([
        {"Ref": r["ref"], "Requested item": r["item"],
         "Coverage": _COV[r["coverage"]],
         "Answering folders": "; ".join(r["folders"]) or "—",
         "Note": r["note"]}
        for r in item_rows
    ]), use_container_width=True, hide_index=True, height=420)
    st.caption(t("comp.items_caption"))

    st.markdown(notr("#### " + tr(t("Rollup by category"))))
    mat = pd.DataFrame([
        {"Cat.": r["letter"], "Material category": r["title"],
         "Sources received": f"{r['sources_received']} / {r['sources_mapped']}",
         "Files": f"{r['files']:,}",
         "Archive folders": ", ".join(r["folders"]) or "—"}
        for r in annex3_rows
    ])
    st.dataframe(mat, use_container_width=True, hide_index=True)

    fig = go.Figure(go.Bar(
        x=[r["letter"] for r in annex3_rows],
        y=[r["files"] for r in annex3_rows],
        marker_color=COLORS["secondary"],
        text=[f"{r['files']:,}" for r in annex3_rows], textposition="outside",
    ))
    st.plotly_chart(
        apply_layout(fig, t("Files received per Annex 3 category"), height=330),
        use_container_width=True)
    st.caption(notr(
        f"{inv.get('total_files', 0):,} {tr(t('comp.files'))} · "
        f"{len(inv.get('folders', []))} {tr(t('comp.topic_folders'))} — "
        f"{tr(t('comp.mat_caption'))}"))

with tab_ind:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(notr("#### " + tr(t("Success indicators (Annex 2 §3)"))))
        st.progress(C.indicator_score(C.SUCCESS_INDICATORS))
        for i in C.SUCCESS_INDICATORS:
            st.markdown(f"{_LABEL[i['status']]} — {i['text']}")
    with c2:
        st.markdown(notr("#### " + tr(t("Implementation requirements (Annex 2 §2)"))))
        st.progress(C.indicator_score(C.IMPLEMENTATION_REQUIREMENTS))
        for i in C.IMPLEMENTATION_REQUIREMENTS:
            st.markdown(f"{_LABEL[i['status']]} — {i['text']}")

with tab_scope:
    st.markdown(t("comp.scope_intro"))
    for x in C.EXCLUSIONS:
        st.markdown(f"- 🚫 {x}")
    st.info(t("comp.scope_note"))

with tab_terms:
    a = C.AGREEMENT
    st.markdown(f"### {notr(a['title'])}")
    st.caption(a["subtitle"])
    facts = pd.DataFrame([
        {"Item": "Client", "Detail": a["client"]},
        {"Item": "Client signatory", "Detail": a["client_signatory"]},
        {"Item": "Consultant", "Detail": a["consultant"]},
        {"Item": "In-scope counterparty", "Detail": a["counterparty"]},
        {"Item": "Effective Date (last signature)",
         "Detail": f"{C.EFFECTIVE_DATE:%d %B %Y}"},
        {"Item": "Term", "Detail": f"{C.TERM_DAYS} calendar days "
                                   f"(ends {C.END_DATE:%d %B %Y})"},
        {"Item": "Contract amount",
         "Detail": f"USD {a['amount_usd']:,} — lump sum (Clause 7)"},
    ])
    st.dataframe(facts, use_container_width=True, hide_index=True)

    st.markdown(notr("#### " + tr(t("Contract documents, in order of priority"))))
    st.markdown("\n".join(f"{i}. {d}" for i, d in enumerate(a["documents"], 1)))
    st.caption(notr(f"{tr(t('comp.terms_note'))} `{a['source_document']}`"))
