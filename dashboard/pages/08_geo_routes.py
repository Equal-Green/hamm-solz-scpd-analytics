import os, sys
_here = os.path.dirname(os.path.abspath(__file__))
for _p in (_here, os.path.dirname(_here), os.path.dirname(os.path.dirname(_here))):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from db import get_db
from state import ensure_loaded
from style import inject_css, render_header
from theme import COLORS, SEQUENCE, apply_layout
from analysis import queries as q
from analysis import geo as geomod

con = get_db()
inject_css()
ensure_loaded(con)

render_header(
    "Geo & Routes",
    "Where waste comes from — collection zones, sub-zones and micro-routes.",
    eyebrow="EQUALGREEN × FLAMING OWL",
)

if not q.has_routes(con):
    st.warning(
        "Route columns aren't loaded yet. Open **Settings → Re-run pipeline** "
        "to reload the transactions with zona / sub-zona / micro-route fields."
    )
    st.stop()

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

k = q.route_kpis(con)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Zones", f"{k['zonas']:,}")
c2.metric("Sub-zones", f"{k['sub_zonas']:,}")
c3.metric("Micro-routes", f"{k['micro_rutas']:,}")
c4.metric("Route-tagged trips", f"{k['route_coverage']:.0f}%")

years = q.years(con)
year = st.selectbox("Filter by year", ["All"] + [str(y) for y in years])
yf = None if year == "All" else int(year)

# --- Real map from the collection-routes KML --------------------------------
@st.cache_resource
def _geometry():
    geomod.ensure_kml()
    polys, routes = geomod.parse_kml()
    return polys, routes, geomod.subzone_geojson(polys), geomod.center(polys, routes)


st.subheader("🗺️ Collection map — sub-zones & routes")
try:
    polys, routes, gj, ctr = _geometry()
    mc1, mc2 = st.columns([1, 1])
    metric = mc1.radio("Color sub-zones by", ["Net tonnage", "Trips"],
                       horizontal=True, label_visibility="collapsed")
    show_routes = mc2.toggle("Show collection routes", value=True)
    zcol = "tonnes" if metric == "Net tonnage" else "trips"

    geo_df = q.subzona_geo(con, yf)
    fig_map = go.Figure(go.Choroplethmapbox(
        geojson=gj, locations=geo_df["sub_zona"], z=geo_df[zcol],
        featureidkey="id", colorscale="YlOrRd", marker_opacity=0.72,
        marker_line_width=0.6, marker_line_color="#141414",
        colorbar=dict(title="t" if zcol == "tonnes" else "trips"),
        hovertemplate="Sub-zone %{location}<br>%{z:,.0f}<extra></extra>"))

    if show_routes:
        for shift, color in (("DIURN", COLORS["secondary"]), ("NOCTURN", COLORS["iron"])):
            lon, lat = [], []
            for r in routes:
                if r["name"].upper().startswith(shift):
                    lon += r["lon"] + [None]
                    lat += r["lat"] + [None]
            if lon:
                fig_map.add_trace(go.Scattermapbox(
                    lon=lon, lat=lat, mode="lines",
                    line=dict(width=1.1, color=color),
                    name="Day routes" if shift == "DIURN" else "Night routes",
                    hoverinfo="skip"))

    fig_map.update_layout(
        mapbox_style="carto-positron", mapbox_zoom=10.3,
        mapbox_center=ctr, height=620,
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(orientation="h", y=0.99, x=0.01,
                    bgcolor="rgba(255,255,255,.7)"),
        font=dict(family="Inter", color="#141414"))
    st.plotly_chart(fig_map, use_container_width=True)
    st.caption(
        f"{len(gj['features'])} sub-zone polygons and {len(routes)} collection "
        "routes from the source KML, over OpenStreetMap. Categories without a "
        "mapped polygon (INDUSTRIA, MERCADO, SERVICIOS ESPECIALES, …) aren't "
        "shaded. Tiles need an internet connection.")
except Exception as e:  # noqa: BLE001
    st.warning(f"Map geometry unavailable: {e}")

st.divider()

# Hierarchy: zona → sub_zona treemap
zs = q.zona_subzona_tonnage(con, yf)
fig = px.treemap(zs, path=[px.Constant("All zones"), "zona", "sub_zona"],
                 values="tonnes", color="zona",
                 color_discrete_sequence=SEQUENCE)
fig.update_traces(root_color="#F6F4F0")
fig.update_layout(margin=dict(l=8, r=8, t=40, b=8), height=440,
                  font=dict(family="Inter", color="#141414"))
fig.update_layout(title=dict(text="Net tonnage by zone → sub-zone",
                             font=dict(family="Playfair Display", size=16)))
st.plotly_chart(fig, use_container_width=True)

col_a, col_b = st.columns(2)
with col_a:
    bz = q.by_zona(con, yf)
    f2 = px.bar(bz, x="zona", y="tonnes", color="zona",
                color_discrete_sequence=SEQUENCE, text_auto=".2s")
    f2.update_layout(showlegend=False)
    f2.update_xaxes(type="category", title_text="")
    st.plotly_chart(apply_layout(f2, "Net tonnage by zone"), use_container_width=True)
with col_b:
    ts = q.top_subzonas(con, yf, n=15)
    f3 = px.bar(ts.sort_values("tonnes"), x="tonnes", y="sub_zona",
                orientation="h", color="zona", color_discrete_sequence=SEQUENCE,
                text_auto=".2s")
    st.plotly_chart(apply_layout(f3, "Top sub-zones by tonnage", height=420),
                    use_container_width=True)

st.divider()
st.subheader("Sub-zone activity by month")
hm = q.subzona_month_heatmap(con, yf)
if not hm.empty:
    pivot = hm.pivot(index="sub_zona", columns="mes", values="tonnes").fillna(0)
    pivot = pivot.reindex(sorted(pivot.columns), axis=1)
    pivot.columns = [MONTHS[int(m) - 1] for m in pivot.columns]
    pivot = pivot.loc[pivot.sum(axis=1).sort_values(ascending=False).index]
    fig4 = px.imshow(pivot, aspect="auto", color_continuous_scale="Reds",
                     labels=dict(color="tonnes"))
    fig4.update_layout(height=520, margin=dict(l=8, r=8, t=20, b=8),
                       font=dict(family="Inter", color="#141414"),
                       coloraxis_colorbar=dict(title="t"))
    st.plotly_chart(fig4, use_container_width=True)

st.divider()
st.subheader("Top micro-routes")
mr = q.top_micro_routes(con, yf, n=15)
show = mr.copy()
show["tonnes"] = show["tonnes"].round(1)
show["avg_kg"] = show["avg_kg"].round(0)
st.dataframe(show, use_container_width=True, hide_index=True,
             column_config={"micro_ruta": "Micro-route", "avg_kg": "avg kg/trip"})
