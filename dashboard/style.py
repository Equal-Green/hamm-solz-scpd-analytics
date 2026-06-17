"""Billy.com-inspired visual layer for the dashboard.

Injects a single CSS block (Inter + JetBrains Mono, glass metric cards, navy
headings, refined sidebar/tables/alerts) and provides a branded page header.
Every page calls inject_css() once after st.set_page_config().
"""
import streamlit as st

# Palette (mirrors billy-dash design tokens).
NAVY = "#1E2233"
PRIMARY = "#E65F33"
PRIMARY_DARK = "#CF4E25"
MUTED = "#6B7280"
SURFACE = "#F4F5F8"
BORDER = "#E4E6EC"
CARD_SHADOW = "0 1px 2px rgba(16,24,40,.04), 0 4px 16px rgba(16,24,40,.05)"

_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap');

html, body, [class*="css"], .stApp, [data-testid="stMarkdownContainer"] {{
    font-family: 'Inter', system-ui, sans-serif;
}}
.stApp {{ background: #FBFBFD; }}

/* Tighten the default page padding, widen content. */
[data-testid="stMainBlockContainer"] {{
    padding-top: 2.2rem; padding-bottom: 3rem;
    max-width: 1180px;
}}

/* Headings */
h1, h2, h3, h4 {{
    font-family: 'Inter', sans-serif !important;
    color: {NAVY} !important; letter-spacing: -0.02em; font-weight: 800 !important;
}}
h1 {{ font-size: 2.05rem !important; }}
h2 {{ font-size: 1.4rem !important; font-weight: 700 !important; margin-top: .4rem; }}
h3 {{ font-size: 1.12rem !important; font-weight: 700 !important; }}
[data-testid="stCaptionContainer"], .stCaption {{ color: {MUTED} !important; }}

/* Branded header banner (render_header) */
.scpd-header {{
    background: linear-gradient(135deg, {NAVY} 0%, #2A2F45 100%);
    border-radius: 16px; padding: 1.4rem 1.6rem; margin-bottom: 1.4rem;
    box-shadow: {CARD_SHADOW}; position: relative; overflow: hidden;
}}
.scpd-header::after {{
    content: ""; position: absolute; right: -40px; top: -40px;
    width: 180px; height: 180px; border-radius: 50%;
    background: radial-gradient(circle, rgba(230,95,51,.35), transparent 70%);
}}
.scpd-header h1 {{ color: #fff !important; margin: 0 0 .2rem 0; font-size: 1.7rem !important; }}
.scpd-header .scpd-sub {{ color: #C9CDDB; font-size: .92rem; font-weight: 500; }}
.scpd-header .scpd-eyebrow {{
    display:inline-block; color: {PRIMARY}; font-weight: 700; font-size: .72rem;
    letter-spacing: .14em; text-transform: uppercase; margin-bottom: .35rem;
}}

/* Metric cards — glass-card look */
[data-testid="stMetric"] {{
    background: #fff; border: 1px solid {BORDER}; border-radius: 14px;
    padding: 1rem 1.15rem; box-shadow: {CARD_SHADOW};
}}
[data-testid="stMetric"] [data-testid="stMetricLabel"] {{
    color: {MUTED} !important; font-weight: 600; font-size: .82rem;
    text-transform: uppercase; letter-spacing: .04em;
}}
[data-testid="stMetricValue"] {{
    font-family: 'JetBrains Mono', monospace !important;
    color: {NAVY} !important; font-weight: 700; font-size: 1.5rem;
}}
[data-testid="stMetricDelta"] {{ font-weight: 600; }}

/* Sidebar */
[data-testid="stSidebar"] {{
    background: {SURFACE}; border-right: 1px solid {BORDER};
}}
[data-testid="stSidebar"] [data-testid="stSidebarNav"] a {{ border-radius: 8px; }}
/* Nested-nav section labels */
[data-testid="stSidebarNav"] ul {{ margin-top: .1rem; }}
.scpd-brand {{
    font-weight: 800; color: {NAVY}; font-size: 1.18rem; line-height: 1.1;
    padding: .2rem .2rem .8rem .2rem; border-bottom: 1px solid {BORDER};
    margin-bottom: .4rem; display: flex; flex-direction: column;
}}
.scpd-brand span {{ color: {NAVY}; }}
.scpd-brand-sub {{
    font-size: .72rem; font-weight: 600; color: {MUTED};
    text-transform: uppercase; letter-spacing: .08em; margin-top: .2rem;
}}

/* Buttons */
.stButton > button, [data-testid="stBaseButton-primary"] {{
    border-radius: 10px; font-weight: 600; border: 1px solid {BORDER};
}}
[data-testid="stBaseButton-primary"] {{
    background: {PRIMARY}; border-color: {PRIMARY};
}}
[data-testid="stBaseButton-primary"]:hover {{ background: {PRIMARY_DARK}; border-color: {PRIMARY_DARK}; }}

/* Dataframes */
[data-testid="stDataFrame"] {{ border-radius: 12px; border: 1px solid {BORDER}; overflow: hidden; }}

/* Alerts / callouts */
[data-testid="stAlert"] {{ border-radius: 12px; border: 1px solid {BORDER}; }}

/* Charts: lift onto subtle cards */
[data-testid="stPlotlyChart"] {{
    background: #fff; border: 1px solid {BORDER}; border-radius: 14px;
    padding: .5rem .4rem; box-shadow: {CARD_SHADOW};
}}

/* Selectbox / inputs */
[data-baseweb="select"] > div {{ border-radius: 10px; }}
hr {{ border-color: {BORDER}; }}
</style>
"""


def inject_css():
    st.markdown(_CSS, unsafe_allow_html=True)


def render_header(title, subtitle="", eyebrow="SCPD ANALYTICS"):
    """Branded hero banner used at the top of each page."""
    sub = f'<div class="scpd-sub">{subtitle}</div>' if subtitle else ""
    eb = f'<div class="scpd-eyebrow">{eyebrow}</div>' if eyebrow else ""
    st.markdown(
        f'<div class="scpd-header">{eb}<h1>{title}</h1>{sub}</div>',
        unsafe_allow_html=True,
    )
