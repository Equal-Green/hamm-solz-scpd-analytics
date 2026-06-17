"""Shared Plotly color scheme and layout helpers, used by every page."""

# Core palette (consistent across all charts).
COLORS = {
    "primary": "#1f6f6f",     # teal -- landfill / primary series
    "secondary": "#e2a829",   # amber -- secondary series / highlights
    "accent": "#3d6cb9",      # blue
    "danger": "#c0392b",      # red -- anomalies / flags
    "success": "#2e8b57",     # green -- recovery
    "muted": "#8a8f98",
    "2023": "#3d6cb9",
    "2024": "#1f6f6f",
    "2025": "#e2a829",
}

# Categorical sequence for service types / vehicle classes / companies.
SEQUENCE = [
    "#1f6f6f", "#e2a829", "#3d6cb9", "#c0392b", "#2e8b57",
    "#8e44ad", "#16a085", "#d35400", "#7f8c8d", "#2c3e50",
    "#c39bd3", "#5dade2",
]

# Stable per-service colors so a service is the same color on every page.
SERVICE_COLORS = {
    "DOMICILIARIA": "#1f6f6f",
    "SERVICIOS ESPECIAL": "#c0392b",
    "INDUSTRIAL": "#e2a829",
    "COMERCIAL": "#3d6cb9",
    "MUNICIPAL": "#2e8b57",
    "INSTITUCIONAL": "#8e44ad",
    "MERCADO": "#16a085",
}

YEAR_COLORS = {2023: COLORS["2023"], 2024: COLORS["2024"], 2025: COLORS["2025"]}


def apply_layout(fig, title=None, height=380):
    """Apply the consistent look to a Plotly figure."""
    fig.update_layout(
        title=title,
        height=height,
        margin=dict(l=10, r=10, t=40 if title else 10, b=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(size=13),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        hovermode="x unified",
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(128,128,128,0.15)")
    return fig
