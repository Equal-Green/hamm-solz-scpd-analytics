"""Offline 'conversation with the data' engine.

A registry of suggested questions, each mapped to a DuckDB-backed answer
(a plain-language sentence plus an optional chart/table). Free-text questions
are routed to the closest suggestion by keyword overlap — so the whole feature
works with no API key and no network. An optional Claude hook can be enabled
later (see ASK_AI_ENABLED), mirroring the gated Postgres export.
"""
import plotly.express as px
import plotly.graph_objects as go

from analysis import queries as q
from theme import COLORS, SEQUENCE, SERVICE_COLORS, YEAR_COLORS, apply_layout

ASK_AI_ENABLED = False  # Phase-2 hook for free-text NL->SQL via Claude.

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


# --- individual answers ------------------------------------------------------
def _total_trend(con):
    at = q.annual_tonnage(con)
    at["year"] = at["year"].astype(int)
    first, last = at.iloc[0], at.iloc[-1]
    pct = (last.tonnes - first.tonnes) / first.tonnes * 100 if first.tonnes else 0
    fig = px.bar(at, x=at["year"].astype(str), y="tonnes", text_auto=".2s",
                 color=at["year"].astype(str),
                 color_discrete_map={str(y): c for y, c in YEAR_COLORS.items()})
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text="", type="category")
    return {
        "summary": (
            f"The landfill received **{at['tonnes'].sum():,.0f} t** net across "
            f"{int(first.year)}–{int(last.year)}. Annual tonnage went from "
            f"**{first.tonnes:,.0f} t** in {int(first.year)} to "
            f"**{last.tonnes:,.0f} t** in {int(last.year)} (**{pct:+.0f}%**)."),
        "fig": apply_layout(fig, "Net tonnage by year"),
    }


def _busiest_month(con):
    mt = q.monthly_trips(con)
    by_month = mt.groupby("mes")["trips"].sum().reset_index()
    peak = by_month.loc[by_month["trips"].idxmax()]
    fig = px.bar(by_month, x="mes", y="trips",
                 color_discrete_sequence=[COLORS["primary"]])
    fig.update_xaxes(tickmode="array", tickvals=list(range(1, 13)), ticktext=MONTHS,
                     title_text="")
    return {
        "summary": (
            f"**{MONTHS[int(peak.mes)-1]}** is the busiest month, with "
            f"**{int(peak.trips):,} trips** summed across all years."),
        "fig": apply_layout(fig, "Trips by calendar month (all years)"),
    }


def _yoy_growth(con):
    yoy = q.service_yoy(con)
    col = "2023->2024 %"
    if col not in yoy.columns:
        return {"summary": "Year-over-year columns aren't available."}
    row = yoy.loc[yoy[col].idxmax()]
    return {
        "summary": (
            f"**{row['tipo_servicio']}** grew the most from 2023 to 2024: "
            f"**{row[col]:+.1f}%** "
            f"({int(row[2023]):,} → {int(row[2024]):,} trips)."),
        "table": yoy,
    }


def _special_spike(con):
    an = q.servicios_especial_anomaly(con)
    return {
        "summary": (
            f"**SERVICIOS ESPECIAL** trips spiked **{an['pct']:+.1f}%** — from "
            f"**{an['y2023']:,}** in 2023 to **{an['y2024']:,}** in 2024. It's the "
            f"single largest year-over-year movement in the dataset. (The project "
            f"brief labelled it ~+83%; the live figure is {an['pct']:+.0f}%.)"),
    }


def _service_mix(con):
    ss = q.service_summary(con)
    total = ss["trips"].sum()
    top = ss.iloc[0]
    fig = px.pie(ss, names="tipo_servicio", values="trips", hole=0.5,
                 color="tipo_servicio", color_discrete_map=SERVICE_COLORS,
                 color_discrete_sequence=SEQUENCE)
    fig.update_traces(textposition="inside", textinfo="percent")
    return {
        "summary": (
            f"**{top['tipo_servicio']}** dominates the mix at "
            f"**{top['trips']/total*100:.0f}%** of all trips "
            f"({int(top['trips']):,}). {len(ss)} service categories in total."),
        "fig": apply_layout(fig, "Trip share by service type"),
    }


def _top_operators(con):
    top = q.top_empresas(con, n=10)
    lead = top.iloc[0]
    fig = px.bar(top.sort_values("tonnes"), x="tonnes", y="empresa",
                 orientation="h", color_discrete_sequence=[COLORS["secondary"]],
                 text_auto=".2s")
    return {
        "summary": (
            f"**{lead['empresa']}** is the largest operator by tonnage "
            f"(**{lead['tonnes']:,.0f} t** over {int(lead['trips']):,} trips). "
            f"Top 10 companies shown below."),
        "fig": apply_layout(fig, "Top operators by net tonnage", height=420),
    }


def _vehicle_types(con):
    vd = q.vehicle_distribution(con)
    lead = vd.iloc[0]
    total = vd["trips"].sum()
    return {
        "summary": (
            f"**{lead['tipo_vehiculo']}** is the most common vehicle class — "
            f"**{lead['trips']/total*100:.0f}%** of trips "
            f"({int(lead['trips']):,}). {len(vd)} classes in all."),
        "table": vd.head(12),
    }


def _num_companies(con):
    n = con.execute(
        "SELECT count(DISTINCT empresa) FROM transactions "
        "WHERE empresa IS NOT NULL").fetchone()[0]
    return {"summary": f"**{n:,} distinct companies** appear in the records."}


def _recovery(con):
    rv = q.recovery_vs_landfill(con)
    rec, lf = rv["recovery_t"].sum(), rv["landfill_t"].sum()
    fig = go.Figure()
    fig.add_bar(x=rv["year"], y=rv["landfill_t"], name="Landfilled",
                marker_color=COLORS["primary"])
    fig.add_bar(x=rv["year"], y=rv["recovery_t"], name="Recovered",
                marker_color=COLORS["success"])
    fig.update_layout(barmode="group")
    fig.update_xaxes(type="category")
    return {
        "summary": (
            f"GEOCYCLE recovered **{rec:,.0f} t** versus **{lf:,.0f} t** "
            f"landfilled — about **{rec/lf*100:.2f}%** of total volume."),
        "fig": apply_layout(fig, "Landfilled vs. recovered tonnage"),
    }


def _top_sectors(con):
    df = con.execute("""
        SELECT sector, sum(peso_neto)/1000.0 AS tonnes, count(*) AS trips
        FROM transactions WHERE sector IS NOT NULL
        GROUP BY 1 ORDER BY tonnes DESC LIMIT 10
    """).df()
    if df.empty:
        return {"summary": "No sector data is available."}
    lead = df.iloc[0]
    fig = px.bar(df.sort_values("tonnes"), x="tonnes", y="sector",
                 orientation="h", color_discrete_sequence=[COLORS["accent"]],
                 text_auto=".2s")
    return {
        "summary": (
            f"**{lead['sector']}** generates the most waste — "
            f"**{lead['tonnes']:,.0f} t**. Top 10 sectors below."),
        "fig": apply_layout(fig, "Top sectors by net tonnage", height=420),
    }


def _avg_load(con):
    ss = q.service_summary(con).sort_values("avg_kg", ascending=False)
    top = ss.iloc[0]
    fig = px.bar(ss.sort_values("avg_kg"), x="avg_kg", y="tipo_servicio",
                 orientation="h", color="tipo_servicio",
                 color_discrete_map=SERVICE_COLORS, color_discrete_sequence=SEQUENCE,
                 text_auto=".0f")
    fig.update_layout(showlegend=False)
    return {
        "summary": (
            f"**{top['tipo_servicio']}** carries the heaviest average load — "
            f"**{top['avg_kg']:,.0f} kg per trip**."),
        "fig": apply_layout(fig, "Average net load per trip, by service"),
    }


def _top_zone(con):
    df = q.by_zona(con)
    if df.empty:
        return {"summary": "Route/zone data isn't loaded. Re-run the pipeline."}
    lead = df.iloc[0]
    fig = px.bar(df, x="zona", y="tonnes", color="zona",
                 color_discrete_sequence=SEQUENCE, text_auto=".2s")
    fig.update_layout(showlegend=False)
    fig.update_xaxes(type="category", title_text="")
    return {
        "summary": (
            f"Zone **{lead['zona']}** produces the most waste — "
            f"**{lead['tonnes']:,.0f} t** across {int(lead['trips']):,} trips."),
        "fig": apply_layout(fig, "Net tonnage by collection zone"),
    }


def _busy_routes(con):
    mr = q.top_micro_routes(con, n=15)
    if mr.empty:
        return {"summary": "Micro-route data isn't loaded. Re-run the pipeline."}
    lead = mr.iloc[0]
    return {
        "summary": (
            f"Micro-route **{lead['micro_ruta']}** is the busiest — "
            f"**{int(lead['trips']):,} trips** ({lead['tonnes']:,.0f} t). "
            f"Top 15 routes below."),
        "table": mr[["micro_ruta", "zona", "sub_zona", "trips", "tonnes"]],
    }


def _data_quality(con):
    t = q.quality_report(con)["transactions"]
    return {
        "summary": (
            f"The data is **clean**: of **{t['total']:,}** transactions, "
            f"**{t['zero_net']:,}** have zero net weight, **{t['neg_net']:,}** are "
            f"negative, **{t['null_servicio']:,}** miss a service type, and "
            f"**{t['dup_ticket_year']:,}** are duplicate tickets. "
            f"See the Data Quality page for the full breakdown."),
    }


# --- registry ----------------------------------------------------------------
ASKS = [
    {"id": "total_trend", "cat": "Volume & trends",
     "label": "How much waste is delivered, and is it growing?",
     "kw": "total volume tonnage trend growing grow much how delivered overall",
     "run": _total_trend},
    {"id": "busiest_month", "cat": "Volume & trends",
     "label": "Which month is busiest for deliveries?",
     "kw": "busiest month seasonal peak monthly when time year",
     "run": _busiest_month},
    {"id": "top_sectors", "cat": "Volume & trends",
     "label": "Which city sectors generate the most waste?",
     "kw": "sector sectors area neighborhood city where most waste",
     "run": _top_sectors},
    {"id": "top_zone", "cat": "Geo & routes",
     "label": "Which collection zone produces the most waste?",
     "kw": "zone zona geo area district most waste where region",
     "run": _top_zone},
    {"id": "busy_routes", "cat": "Geo & routes",
     "label": "What are the busiest micro-routes?",
     "kw": "route routes micro ruta busiest collection truck path most",
     "run": _busy_routes},
    {"id": "special_spike", "cat": "Service mix",
     "label": "How big was the SERVICIOS ESPECIAL spike?",
     "kw": "servicios especial special spike anomaly jump increase 83 2024",
     "run": _special_spike},
    {"id": "yoy_growth", "cat": "Service mix",
     "label": "Which service type grew the most year-over-year?",
     "kw": "service type grew growth yoy year over year increase fastest most",
     "run": _yoy_growth},
    {"id": "service_mix", "cat": "Service mix",
     "label": "What's the waste mix by service type?",
     "kw": "mix share service type category breakdown composition proportion pie",
     "run": _service_mix},
    {"id": "avg_load", "cat": "Service mix",
     "label": "Which service carries the heaviest loads?",
     "kw": "average load weight heaviest per trip kg service biggest",
     "run": _avg_load},
    {"id": "top_operators", "cat": "Operators & fleet",
     "label": "Who are the biggest operators by tonnage?",
     "kw": "operator company empresa biggest top tonnage who hauler firm",
     "run": _top_operators},
    {"id": "num_companies", "cat": "Operators & fleet",
     "label": "How many companies use the landfill?",
     "kw": "how many companies distinct count operators firms number",
     "run": _num_companies},
    {"id": "vehicle_types", "cat": "Operators & fleet",
     "label": "What vehicle types deliver most often?",
     "kw": "vehicle truck type fleet class common recolector most",
     "run": _vehicle_types},
    {"id": "recovery", "cat": "Recovery & quality",
     "label": "How much does GEOCYCLE recover vs landfill?",
     "kw": "geocycle recovery recover recycle diverted material ratio percent landfill",
     "run": _recovery},
    {"id": "data_quality", "cat": "Recovery & quality",
     "label": "How complete and clean is the data?",
     "kw": "quality clean complete null missing duplicate trust integrity errors",
     "run": _data_quality},
]

_BY_ID = {a["id"]: a for a in ASKS}


def grouped():
    out = {}
    for a in ASKS:
        out.setdefault(a["cat"], []).append(a)
    return out


def get(ask_id):
    return _BY_ID.get(ask_id)


def route(text):
    """Map free text to the best-matching question id, or None if too weak."""
    words = {w.strip(".,?!¿¡").lower() for w in text.split() if len(w) > 2}
    if not words:
        return None
    best, best_score = None, 0
    for a in ASKS:
        kw = set(a["kw"].split()) | set(a["label"].lower().split())
        score = len(words & kw)
        if score > best_score:
            best, best_score = a["id"], score
    return best if best_score >= 1 else None
