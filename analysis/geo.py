"""Parse the collection-routes KML into polygons (sub-zones) and route lines.

The source ZIP ships `RUTAS_RECOLECCION, ZONAS Y SUZONAS.kml` — 56 sub-zone
polygons (named like "12A") and 472 route LineStrings, in lon/lat. We extract it
from the streaming ZIP (stored, bit-3 data descriptor) on demand, then parse it
into plain Python so Plotly can render a real map of Guayaquil collection.
"""
import os
import re
import struct
import xml.etree.ElementTree as ET

from config import DATA_DIR, ZIP_PATH

KML_NAME = "RUTAS_RECOLECCION"          # substring match in the ZIP
# Tracked path (committed for cloud hosts that lack the source ZIP).
KML_PATH = os.path.join(DATA_DIR, "rutas.kml")


def ensure_kml(zip_path=ZIP_PATH, dest=KML_PATH):
    """Extract the routes KML from the streaming ZIP if not already on disk."""
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        return dest
    import mmap
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(zip_path, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        try:
            off = 0
            while True:
                p = mm.find(b"PK\x03\x04", off)
                if p == -1:
                    raise FileNotFoundError("Routes KML not found in ZIP")
                fnl = struct.unpack_from("<H", mm, p + 26)[0]
                exl = struct.unpack_from("<H", mm, p + 28)[0]
                name = mm[p + 30:p + 30 + fnl].decode("utf-8", "replace")
                if name.endswith(".kml") and KML_NAME in name:
                    ds = p + 30 + fnl + exl
                    dd = mm.find(b"PK\x07\x08", ds)
                    raw = bytes(mm[ds:dd])
                    method = struct.unpack_from("<H", mm, p + 8)[0]
                    if method != 0:
                        import zlib
                        raw = zlib.decompress(raw, -15)
                    with open(dest, "wb") as out:
                        out.write(raw)
                    return dest
                off = p + 4
        finally:
            mm.close()


def _coords(text):
    pts = []
    for tok in text.strip().split():
        parts = tok.split(",")
        if len(parts) >= 2:
            try:
                pts.append((float(parts[0]), float(parts[1])))  # (lon, lat)
            except ValueError:
                continue
    return pts


def parse_kml(path=KML_PATH):
    """Return (polygons, routes).

    polygons: list of {"name", "lon": [...], "lat": [...]} (outer ring)
    routes:   list of {"name", "lon": [...], "lat": [...]}
    """
    root = ET.parse(path).getroot()
    polygons, routes = [], []
    for pm in root.findall(".//{*}Placemark"):
        nm_el = pm.find("{*}name")
        name = (nm_el.text or "").strip() if nm_el is not None else ""
        poly = pm.find(".//{*}Polygon//{*}coordinates")
        line = pm.find(".//{*}LineString/{*}coordinates")
        if poly is not None and poly.text:
            pts = _coords(poly.text)
            if pts:
                polygons.append({"name": name,
                                 "lon": [p[0] for p in pts],
                                 "lat": [p[1] for p in pts]})
        elif line is not None and line.text:
            pts = _coords(line.text)
            if pts:
                routes.append({"name": name,
                               "lon": [p[0] for p in pts],
                               "lat": [p[1] for p in pts]})
    return polygons, routes


def normalize_subzone(name):
    """KML names sub-zones like '1A'; transactions store '01A'. Zero-pad the
    leading number so they join."""
    m = re.match(r"^(\d+)(.*)$", name.strip())
    return (m.group(1).zfill(2) + m.group(2)) if m else name.strip()


def subzone_geojson(polygons):
    """A GeoJSON FeatureCollection keyed by normalized sub-zone name."""
    feats = []
    for p in polygons:
        ring = list(zip(p["lon"], p["lat"]))
        if len(ring) < 3:
            continue
        if ring[0] != ring[-1]:
            ring.append(ring[0])
        sz = normalize_subzone(p["name"])
        feats.append({
            "type": "Feature", "id": sz,
            "properties": {"sub_zona": sz},
            "geometry": {"type": "Polygon",
                         "coordinates": [[[lon, lat] for lon, lat in ring]]},
        })
    return {"type": "FeatureCollection", "features": feats}


def route_shift(name):
    """Day vs night from the route placemark name (DIURNO/DIURNA vs NOCTURNO)."""
    return "night" if name.upper().startswith("NOCTURN") else "day"


def _point_in_ring(lon, lat, ring):
    inside = False
    n = len(ring)
    j = n - 1
    for i in range(n):
        xi, yi = ring[i]
        xj, yj = ring[j]
        if ((yi > lat) != (yj > lat)) and \
                (lon < (xj - xi) * (lat - yi) / ((yj - yi) or 1e-12) + xi):
            inside = not inside
        j = i
    return inside


def polygon_centroids(polygons):
    out = {}
    for p in polygons:
        if p["lon"]:
            out[normalize_subzone(p["name"])] = {
                "lon": sum(p["lon"]) / len(p["lon"]),
                "lat": sum(p["lat"]) / len(p["lat"])}
    return out


def assign_routes_to_subzones(polygons, routes, sample=30):
    """For each route, the set of sub-zones (normalized) it passes through,
    via ray-casting a sample of its vertices against each polygon (bbox
    pre-filtered). Lets the UI scope routes to a focused sub-zone."""
    polys = []
    for p in polygons:
        ring = list(zip(p["lon"], p["lat"]))
        if len(ring) >= 3:
            polys.append((normalize_subzone(p["name"]), ring,
                          min(p["lon"]), max(p["lon"]),
                          min(p["lat"]), max(p["lat"])))
    assign = []
    for r in routes:
        lons, lats = r["lon"], r["lat"]
        step = max(1, len(lons) // sample)
        hit = set()
        for lon, lat in zip(lons[::step], lats[::step]):
            for name, ring, minx, maxx, miny, maxy in polys:
                if minx <= lon <= maxx and miny <= lat <= maxy \
                        and _point_in_ring(lon, lat, ring):
                    hit.add(name)
        assign.append(hit)
    return assign


def center(polygons, routes):
    lons, lats = [], []
    for g in polygons + routes:
        lons += g["lon"]
        lats += g["lat"]
    if not lons:
        return {"lon": -79.9, "lat": -2.17}
    return {"lon": sum(lons) / len(lons), "lat": sum(lats) / len(lats)}
