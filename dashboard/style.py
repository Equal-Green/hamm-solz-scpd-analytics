"""Flaming Owl portal visual layer, co-branded with the EqualGreen logo.

FO portal design system: crimson single accent on an iron/cream brutalist base,
dark iron sidebar, Playfair Display display headings + Inter body + JetBrains
Mono numerals, 16px cards, fully-rounded buttons, 3px offset-shadow signature.
Every page calls inject_css() after st.set_page_config(); render_header() draws
the branded hero with the EqualGreen mark.
"""
import base64
import os

import streamlit as st

# --- FO portal palette -------------------------------------------------------
CRIMSON = "#DC2828"        # Flaming Owl crimson — single accent  (hsl 0 72% 51%)
CRIMSON_DARK = "#B91C1C"
IRON = "#141414"           # ink / dark sidebar / brutalist border
CREAM = "#F8F5EF"          # warm paper
ASH = "#BFBFBF"            # hairline borders / muted on dark
MUTED = "#5F5F5F"          # secondary text on white
BORDER = "#E4E1DB"
SURFACE = "#F6F4F0"
EG_LIME = "#9BBF3B"        # EqualGreen accent

_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
LOGO_FULL = os.path.join(_ASSETS, "equalgreen-logo.png")
LOGO_MARK = os.path.join(_ASSETS, "equalgreen-mark.png")


def _data_uri(path):
    try:
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f"data:image/png;base64,{b64}"
    except OSError:
        return ""


_LOGO_URI = _data_uri(LOGO_MARK if os.path.exists(LOGO_MARK) else LOGO_FULL)

_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800;900&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600;700&display=swap');

html, body, [class*="css"], .stApp, [data-testid="stMarkdownContainer"] {{
    font-family: 'Inter', system-ui, sans-serif;
}}
.stApp {{ background: #FFFFFF; }}

/* Hide the Streamlit Deploy button (deployment handled externally) */
[data-testid="stAppDeployButton"], .stAppDeployButton {{ display: none !important; }}

[data-testid="stMainBlockContainer"] {{
    padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1180px;
}}

/* Display headings in Playfair (FO portal display face) */
h1, h2, h3 {{
    font-family: 'Playfair Display', Georgia, serif !important;
    color: {IRON} !important; letter-spacing: -0.01em; font-weight: 800 !important;
}}
h1 {{ font-size: 2.1rem !important; }}
h2 {{ font-size: 1.5rem !important; }}
h3 {{ font-size: 1.18rem !important; }}
h4 {{ font-family: 'Inter', sans-serif !important; color: {IRON} !important;
      font-weight: 700 !important; }}
[data-testid="stCaptionContainer"] {{ color: {MUTED} !important; }}

/* Branded hero header — iron with crimson keyline + EqualGreen mark */
.scpd-header {{
    background: {IRON}; border-radius: 16px; padding: 1.4rem 1.6rem;
    margin-bottom: 1.4rem; position: relative; overflow: hidden;
    border: 1.5px solid {IRON}; box-shadow: 5px 5px 0 0 {CRIMSON};
    display: flex; align-items: center; gap: 1.1rem;
}}
.scpd-header .scpd-logo {{
    width: 60px; height: 60px; border-radius: 12px; flex: 0 0 auto;
    background-image: url('{_LOGO_URI}'); background-size: cover;
    background-position: center; box-shadow: 0 0 0 1px rgba(255,255,255,.12);
}}
.scpd-header h1 {{
    color: {CREAM} !important; margin: 0 0 .15rem 0; font-size: 1.8rem !important;
}}
.scpd-header .scpd-sub {{ color: #C7C4BD; font-size: .92rem; font-weight: 500; }}
.scpd-header .scpd-eyebrow {{
    display:inline-block; color: {CRIMSON}; font-weight: 700; font-size: .72rem;
    letter-spacing: .16em; text-transform: uppercase; margin-bottom: .35rem;
    font-family: 'JetBrains Mono', monospace;
}}

/* Metric cards — brutalist offset shadow */
[data-testid="stMetric"] {{
    background: #fff; border: 1.5px solid {IRON}; border-radius: 14px;
    padding: 1rem 1.15rem; box-shadow: 3px 3px 0 0 {IRON};
}}
[data-testid="stMetric"] [data-testid="stMetricLabel"] {{
    color: {MUTED} !important; font-weight: 600; font-size: .8rem;
    text-transform: uppercase; letter-spacing: .05em;
}}
[data-testid="stMetricValue"] {{
    font-family: 'JetBrains Mono', monospace !important;
    color: {IRON} !important; font-weight: 700; font-size: 1.5rem;
}}
[data-testid="stMetricDelta"] {{ font-weight: 600; }}

/* Dark iron sidebar (FO portal signature) */
[data-testid="stSidebar"] {{ background: {IRON}; border-right: 1px solid #000; }}
[data-testid="stSidebar"] * {{ color: {CREAM}; }}
[data-testid="stSidebarNav"] a {{ border-radius: 8px; color: #CFCCC5 !important; }}
[data-testid="stSidebarNav"] a:hover {{ background: rgba(255,255,255,.06); }}
[data-testid="stSidebarNav"] a[aria-current="page"] {{
    background: rgba(220,40,40,.20); color: #fff !important;
    box-shadow: inset 3px 0 0 {CRIMSON};
}}
[data-testid="stSidebarNav"] a[aria-current="page"] span {{ color:#fff !important; }}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {{ color: {ASH} !important; }}
.scpd-brand {{
    font-family: 'Playfair Display', serif; font-weight: 800; color: {CREAM};
    font-size: 1.16rem; line-height: 1.1; padding: .1rem .2rem .7rem .2rem;
    border-bottom: 1px solid #2A2A2A; margin-bottom: .5rem;
    display: flex; flex-direction: column;
}}
.scpd-brand-sub {{
    font-family: 'JetBrains Mono', monospace; font-size: .66rem; font-weight: 600;
    color: {CRIMSON}; text-transform: uppercase; letter-spacing: .12em;
    margin-top: .35rem;
}}

/* Buttons — fully-rounded crimson pills */
.stButton > button, [data-testid="stBaseButton-secondary"] {{
    border-radius: 999px; font-weight: 600; border: 1.5px solid {IRON};
    color: {IRON};
}}
[data-testid="stBaseButton-primary"] {{
    background: {CRIMSON}; border: 1.5px solid {IRON}; border-radius: 999px;
    color: {CREAM}; box-shadow: 3px 3px 0 0 {IRON}; font-weight: 700;
}}
[data-testid="stBaseButton-primary"]:hover {{ background: {CRIMSON_DARK}; }}

/* Chart cards */
[data-testid="stPlotlyChart"] {{
    background: #fff; border: 1px solid {BORDER}; border-radius: 14px;
    padding: .5rem .4rem; box-shadow: 0 1px 2px rgba(20,20,20,.04);
}}
[data-testid="stDataFrame"] {{ border-radius: 12px; border: 1px solid {BORDER}; overflow: hidden; }}
[data-testid="stAlert"] {{ border-radius: 12px; border: 1px solid {BORDER}; }}
[data-baseweb="select"] > div {{ border-radius: 10px; }}
hr {{ border-color: {BORDER}; }}

/* bordered containers (key-findings cards) */
[data-testid="stVerticalBlockBorderWrapper"] {{ border-radius: 14px; }}
</style>
"""


def hamm_wordmark(on_dark=False, height=34):
    """Recreated THE HAMM Solz wordmark (client / customer brand)."""
    the = "#2BB3F0" if on_dark else "#1B9FE0"
    hamm = "#FFFFFF" if on_dark else "#1A1A1A"
    solz = "#C7C4BD" if on_dark else "#5A5A5A"
    tag = "#A6A6A6" if on_dark else "#3A3A3A"
    ico = int(height * 0.62)
    return (
        f'<div style="display:inline-flex;flex-direction:column;line-height:1;">'
        f'<div style="display:flex;align-items:center;gap:.16em;'
        f'font-family:Arial,Helvetica,sans-serif;font-weight:800;'
        f'font-size:{height}px;letter-spacing:-.01em;">'
        f'<span style="color:{the};">THE</span>'
        f'<svg width="{int(ico*1.2)}" height="{ico}" viewBox="0 0 26 20" '
        f'style="margin:0 .05em;"><path d="M1 4h13l6 6-6 6H1l6-6z" fill="{the}"/>'
        f'<path d="M11 1l7 7-7 7" fill="none" stroke="{hamm}" '
        f'stroke-width="2.6"/></svg>'
        f'<span style="color:{hamm};">HAMM</span>'
        f'<span style="color:{solz};font-weight:700;font-size:.72em;'
        f'align-self:flex-end;padding-bottom:.1em;margin-left:.1em;">Solz</span>'
        f'</div><div style="color:{tag};font-family:Arial,sans-serif;'
        f'font-weight:700;font-size:{max(9, int(height*0.32))}px;'
        f'letter-spacing:.005em;margin-top:.3em;">'
        f'Total Energy &amp; Environment Consultant</div></div>'
    )


def eg_logo_html(size=34):
    if not _LOGO_URI:
        return ""
    return (f'<div style="width:{size}px;height:{size}px;border-radius:8px;'
            f'background:url(\'{_LOGO_URI}\') center/cover;flex:0 0 auto;"></div>')


def inject_css():
    st.markdown(_CSS, unsafe_allow_html=True)


def render_header(title, subtitle="", eyebrow="THE HAMM SOLZ × EQUALGREEN"):
    """Branded hero banner with the EqualGreen mark and FO portal styling."""
    logo = '<div class="scpd-logo"></div>' if _LOGO_URI else ""
    sub = f'<div class="scpd-sub">{subtitle}</div>' if subtitle else ""
    eb = f'<div class="scpd-eyebrow">{eyebrow}</div>' if eyebrow else ""
    st.markdown(
        f'<div class="scpd-header">{logo}'
        f'<div>{eb}<h1>{title}</h1>{sub}</div></div>',
        unsafe_allow_html=True,
    )
