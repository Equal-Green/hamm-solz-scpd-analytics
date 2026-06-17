"""Plotly color scheme + layout helpers — Flaming Owl portal palette.

Crimson is the FO single accent; the categorical sequence is a clean, standard
dashboard palette (crimson, iron, teal, amber, EqualGreen lime, …) that stays
legible on white. Chart titles use Playfair Display, body text Inter, numerals
JetBrains Mono.
"""

# FO portal anchors.
COLORS = {
    "primary": "#DC2828",     # Flaming Owl crimson
    "secondary": "#0E7C86",   # teal
    "accent": "#9BBF3B",      # EqualGreen lime
    "amber": "#E0A106",
    "danger": "#DC2828",
    "success": "#2E7D5B",
    "iron": "#141414",
    "slate": "#5B6472",
    "muted": "#5F5F5F",
    "2023": "#9BBF3B",        # lime (EqualGreen)
    "2024": "#DC2828",        # crimson (Flaming Owl)
    "2025": "#141414",        # iron
}

# Standard dashboard categorical palette (legible on white, crimson-led).
SEQUENCE = [
    "#DC2828", "#141414", "#0E7C86", "#E0A106", "#9BBF3B",
    "#7A4FBF", "#5B6472", "#C2497A", "#2E7D5B", "#B8742A",
    "#3E73B8", "#9AA0A6",
]

# Stable per-service colors.
SERVICE_COLORS = {
    "DOMICILIARIA": "#5B6472",          # slate (dominant, neutral)
    "SERVICIOS ESPECIAL": "#DC2828",    # crimson — the anomaly / brand accent
    "INDUSTRIAL": "#E0A106",            # amber
    "COMERCIAL": "#0E7C86",             # teal
    "MUNICIPAL": "#7A4FBF",             # purple
    "INSTITUCIONAL": "#9BBF3B",         # lime
    "MERCADO": "#C2497A",               # rose
}

YEAR_COLORS = {2023: COLORS["2023"], 2024: COLORS["2024"], 2025: COLORS["2025"]}

_IRON = "#141414"
_MUTED = "#5F5F5F"
_GRID = "rgba(20,20,20,0.08)"


def apply_layout(fig, title=None, height=380):
    """Apply the consistent FO-portal look to a Plotly figure."""
    fig.update_layout(
        title=dict(text=title,
                   font=dict(size=16, color=_IRON, family="Playfair Display"))
        if title else None,
        height=height,
        margin=dict(l=12, r=12, t=46 if title else 12, b=64),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=13, color=_IRON),
        colorway=SEQUENCE,
        title_x=0,
        legend=dict(orientation="h", yanchor="top", y=-0.18, xanchor="left", x=0,
                    font=dict(size=12, color=_MUTED), title_text=""),
        hoverlabel=dict(font=dict(family="Inter", size=12)),
        hovermode="x unified",
    )
    fig.update_xaxes(showgrid=False, color=_MUTED, linecolor=_GRID)
    fig.update_yaxes(showgrid=True, gridcolor=_GRID, color=_MUTED, zeroline=False)
    return fig
