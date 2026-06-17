"""Shared Plotly color scheme and layout helpers, used by every page.

Palette mirrors the billy-dash design tokens: warm orange-red primary, deep
navy text, and the platform accent colors (blue / amber / green) for series.
"""

# Core palette.
COLORS = {
    "primary": "#E65F33",     # warm orange-red — brand / highlight series
    "secondary": "#2563EB",   # blue
    "accent": "#20B074",      # green
    "amber": "#F5A623",
    "danger": "#DC2626",      # red — anomalies / flags
    "success": "#20B074",     # green — recovery
    "navy": "#1E2233",
    "muted": "#6B7280",
    "2023": "#2563EB",        # blue
    "2024": "#E65F33",        # orange (primary)
    "2025": "#20B074",        # green
}

# Categorical sequence (used wherever a service / company / vehicle list needs
# distinct colors). Brand orange leads.
SEQUENCE = [
    "#E65F33", "#2563EB", "#20B074", "#F5A623", "#7C3AED",
    "#DC2626", "#0EA5A5", "#DB2777", "#64748B", "#1E2233",
    "#A855F7", "#0284C7",
]

# Stable per-service colors so a service is the same color on every page.
SERVICE_COLORS = {
    "DOMICILIARIA": "#2563EB",
    "SERVICIOS ESPECIAL": "#E65F33",   # the anomaly — brand orange, stands out
    "INDUSTRIAL": "#F5A623",
    "COMERCIAL": "#20B074",
    "MUNICIPAL": "#7C3AED",
    "INSTITUCIONAL": "#0EA5A5",
    "MERCADO": "#DB2777",
}

YEAR_COLORS = {2023: COLORS["2023"], 2024: COLORS["2024"], 2025: COLORS["2025"]}

_NAVY = "#1E2233"
_MUTED = "#6B7280"
_GRID = "rgba(30,34,51,0.08)"


def apply_layout(fig, title=None, height=380):
    """Apply the consistent look to a Plotly figure."""
    fig.update_layout(
        title=dict(text=title, font=dict(size=15, color=_NAVY, family="Inter")) if title else None,
        height=height,
        margin=dict(l=12, r=12, t=44 if title else 12, b=64),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=13, color=_NAVY),
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
