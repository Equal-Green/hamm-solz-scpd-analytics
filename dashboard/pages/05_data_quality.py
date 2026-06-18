import os, sys
_here = os.path.dirname(os.path.abspath(__file__))
for _p in (_here, os.path.dirname(_here), os.path.dirname(os.path.dirname(_here))):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import json

import plotly.express as px
import streamlit as st

from db import get_db
from state import ensure_loaded
from style import inject_css, render_header
from theme import COLORS, apply_layout
from analysis import queries as q
from i18n import t
from config import ZIP_PATH
from pipeline.catalog import build_catalog
from pipeline.tables import load_all_tables, REGISTRY_SCHEMA
from pipeline.archive import load_inventory

_HAS_ZIP = os.path.exists(ZIP_PATH)
con = get_db()
inject_css()
ensure_loaded(con)

render_header(t("page.quality"),
              "Orient on the source archive, then verify the data it produced.")

# Curated narrative per top-level folder (keyed by its leading number),
# merged with live file counts from the ZIP.
FOLDER_INFO = {
    "1": {"icon": "🧪", "title": "Waste characterization",
          "purpose": "Composition studies of municipal waste by stratum and "
                     "year (2012–2026) — what the garbage is actually made of.",
          "feeds": "**Composition & Diversion** (calibration). 2 workbooks "
                   "loaded as `src_*` tables."},
    "2": {"icon": "🏗️", "title": "Puná engineering study (future site)",
          "purpose": "Full RSM design study for a *future* landfill on Puná "
                     "island — topography, geology, hydrology, drawings (DWG/"
                     "SHP), budgets. A different site from Las Iguanas.",
          "feeds": "Reference / future-site context. Tabular budgets & "
                   "coordinates load as `src_*` tables; not part of the "
                   "Guayaquil pesaje analytics."},
    "3": {"icon": "🗺️", "title": "Cantonal cartography & cadastre",
          "purpose": "Catastro Urbano — 598,715 parcels — plus a rural "
                     "cartography shapefile.",
          "feeds": "Property reference (`src_catastro_urbano_predios_urbanos`) "
                   "and geographic context."},
    "4": {"icon": "⚖️", "title": "SCPD weighbridge data — the core",
          "purpose": "Every truck weighed at Las Iguanas, 2023–2025, plus "
                     "GEOCYCLE material recovery. This is the heart of the report.",
          "feeds": "The typed data model → **`transactions`** & **`retirados`**. "
                   "Powers Overview, Service Types, Operators, GEOCYCLE, Geo & "
                   "Routes, Forecast, Efficiency, and Integrity."},
    "5": {"icon": "📜", "title": "Regulatory framework (NORMATIVAS)",
          "purpose": "National & municipal norms governing solid-waste "
                     "management.",
          "feeds": "Policy context (PDF reference only)."},
    "6": {"icon": "🏙️", "title": "Territorial planning (PDOT / PUGS)",
          "purpose": "Land-use and development plans, plus an ArcGIS map package.",
          "feeds": "Planning context (reference)."},
    "7": {"icon": "🚛", "title": "Collection zones, sub-zones & routes",
          "purpose": "The routes KML, micro-route drawings (DWG), and the "
                     "EOP01/EOP02 production plans.",
          "feeds": "The **Geo & Routes** map (KML → 48 sub-zone polygons + 472 "
                   "day/night routes); production plans load as `src_*` tables."},
    "8": {"icon": "📍", "title": "AGAS map",
          "purpose": "A supplementary geographic layer (KMZ).",
          "feeds": "Geo reference."},
    "9": {"icon": "🗑️", "title": "Las Iguanas landfill",
          "purpose": "Site engineering drawings (DWG) and disposal-quantity "
                     "records & projections for the active landfill.",
          "feeds": "**Capacity & Forecast** (disposal projection workbook); "
                   "site reference."},
    "10": {"icon": "📋", "title": "Puná operational reports",
           "purpose": "GIRS diagnosis, environmental management plan, and a "
                      "collection-trip register.",
           "feeds": "Reference; the trip register loads as a `src_*` table."},
}


def _folder_num(name):
    return name.split(".")[0].strip()


@st.cache_resource
def _inventory():
    return load_inventory()


tab_arch, tab_quality, tab_catalog, tab_src = st.tabs(
    ["📂 The archive", "✅ Integrity & quality", "📇 Catalog",
     "🗄️ Source tables"])

# ======================================================================
# TAB 1 — THE ARCHIVE (story of the INFORMACIÓN folder)
# ======================================================================
with tab_arch:
    inv = _inventory()
    st.markdown(
        "Everything in this report traces back to a single delivery: the "
        "**`INFORMACIÓN`** folder handed over by the municipality "
        "(CIRCULAREP / Consorcio URVASEO). It mixes **operational data** "
        "(spreadsheets, a routes map) with a large body of **engineering and "
        "policy documents** (PDFs, CAD drawings, GIS). This tab orients you on "
        "what's inside and how each part feeds the analytics."
    )
    loaded = q.catalog_totals(con)["files_in_duckdb"] if q.catalog_count(con) else 4
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Files delivered", f"{inv['total_files']:,}")
    m2.metric("Top-level folders", f"{len(inv['folders'])}")
    m3.metric("File types", f"{len(inv['ext_totals'])}")
    m4.metric("Tabular files → DuckDB", f"{loaded}")

    sub_map, sub_lineage, sub_types = st.tabs(
        ["🗂️ Folder map", "🔗 Data lineage", "📦 File types"])

    # ---- Folder map ----
    with sub_map:
        st.caption("Each folder, what it is, and where it lands in the report.")
        for f in inv["folders"]:
            num = _folder_num(f["folder"])
            info = FOLDER_INFO.get(num)
            exts = "  ".join(f"`{e}`×{n}" for e, n in list(f["exts"].items())[:6])
            with st.container(border=True):
                head = f"{info['icon'] if info else '📁'} **{f['folder']}**"
                st.markdown(f"{head} — {f['files']} files")
                if info:
                    st.markdown(info["purpose"])
                    st.markdown(f"↳ **Feeds:** {info['feeds']}")
                st.caption(exts)

    # ---- Data lineage ----
    with sub_lineage:
        st.markdown(
            "**How raw files become the data model.** Four folders carry "
            "machine-readable data we ingest; the rest are documents that give "
            "context."
        )
        st.markdown(
            "```\n"
            "4. DATA DEL SISTEMA DE PESAJE  ──►  transactions  (516,526 rows)\n"
            "   DATA SCPD 2023/2024/2025         retirados     (7,515 rows)\n"
            "                                     │\n"
            "        ┌────────────────────────────┴───────────────────────────┐\n"
            "   Overview · Service Types · Operators · GEOCYCLE · Geo & Routes\n"
            "   Forecast · Operational Efficiency · Revenue & Integrity\n"
            "\n"
            "7. PLANO ZONAS Y SUBZONAS      ──►  rutas.kml  ──► Geo map\n"
            "   EOP01/EOP02 plans           ──►  src_eop01_* / src_eop02_*\n"
            "\n"
            "3. CARTOGRAFÍA DEL CANTON      ──►  src_catastro_urbano_* (598,715)\n"
            "1. CARACTERIZACION             ──►  src_caracterizacion_*  ──► Diversion\n"
            "9. INFORMACION LAS IGUANAS     ──►  src_*  ──► Capacity & Forecast\n"
            "\n"
            "2 ESTUDIO PUNA · 5 NORMATIVAS · 6 PDOT/PUGS · 8 AGAS · 10 INFORMES\n"
            "   └► reference documents (PDF/DWG/GIS); tabular parts → src_*\n"
            "```"
        )
        st.info(
            "**Field-name note:** ingested tables keep the source's original "
            "Spanish column names (`NUM_TICKET`, `DESC_TIPO_DESECHO`, "
            "`PESO_NETO`, `SUB_ZONA`, …). The UI is translated; the data model "
            "is not — so it always matches the source files.", icon="🔤")

    # ---- File types ----
    with sub_types:
        import pandas as pd
        et = pd.DataFrame(sorted(inv["ext_totals"].items(),
                                 key=lambda x: -x[1]), columns=["ext", "count"])
        DATA_EXTS = {"xlsx", "csv", "kml", "kmz", "shp", "dbf"}
        et["kind"] = et["ext"].apply(
            lambda e: "Machine-readable data" if e in DATA_EXTS else "Document / drawing")
        fig = px.bar(et, x="count", y="ext", orientation="h", color="kind",
                     color_discrete_map={"Machine-readable data": COLORS["primary"],
                                         "Document / drawing": COLORS["slate"]},
                     text_auto=True)
        fig.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(apply_layout(fig, "Files by type", height=520),
                        use_container_width=True)
        st.caption(
            "Most of the archive is **documents & CAD/GIS** (PDF, DWG, SHP) — "
            "engineering and policy reference. The analytics draw on the small "
            "set of **machine-readable** files (XLSX, CSV, KML, SHP).")

# ======================================================================
# TAB 2 — INTEGRITY & QUALITY
# ======================================================================
with tab_quality:
    rep = q.quality_report(con)
    st.subheader("Row counts: loaded vs. brief")
    for f in rep["files"]:
        delta = f["loaded"] - f["spec_rows"]
        flag = "✅" if delta == 0 else f"⚠️ {delta:+d}"
        st.markdown(f"- `{f['file']}` — loaded **{f['loaded']:,}**, "
                    f"brief **{f['spec_rows']:,}** {flag}")
    st.caption("2023 and 2024 each contain one more genuine row than the brief "
               "recorded (verified: distinct tickets, no nulls, no duplicates, "
               "no totals row). 2025 and GEOCYCLE match exactly.")

    st.divider()
    tx = rep["transactions"]
    st.subheader("Transactions — key-column health")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total rows", f"{tx['total']:,}")
    c2.metric("Zero net weight", f"{tx['zero_net']:,}", help="PESO_NETO = 0")
    c3.metric("Negative net weight", f"{tx['neg_net']:,}", help="PESO_NETO < 0")
    c4.metric("Duplicate ticket/year", f"{tx['dup_ticket_year']:,}")
    if not tx["zero_net"] and not tx["neg_net"]:
        st.success("No zero or negative net-weight trips.")

    st.subheader("Null rates on key columns (transactions)")
    nulls = {"num_ticket": tx["null_ticket"], "tipo_servicio": tx["null_servicio"],
             "empresa": tx["null_empresa"], "sector": tx["null_sector"],
             "fec_ingreso": tx["null_fecha"], "peso_neto": tx["null_neto"]}
    cols = st.columns(len(nulls))
    for (name, n), col in zip(nulls.items(), cols):
        pct = n / tx["total"] * 100 if tx["total"] else 0
        col.metric(name, f"{n:,}", f"{pct:.2f}%")

    st.divider()
    st.subheader("Date range per year")
    st.dataframe(rep["date_range_by_year"], use_container_width=True, hide_index=True)

    r = rep["retirados"]
    st.subheader("GEOCYCLE (retirados)")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total rows", f"{r['total']:,}")
    c2.metric("Non-positive net", f"{r['nonpos_net']:,}", help="net recovered <= 0")
    c3.metric("Null date / org", f"{r['null_fecha']:,} / {r['null_org']:,}")

    with st.expander("🛠️ Data improvement opportunities (for the next data pull)"):
        st.markdown(
            "- **`MICRO_RUTA` is ~52% empty** — route-level analysis only covers "
            "half the trips.\n"
            "- **`SECTOR` is effectively constant** — unusable as geography; rely "
            "on `ZONA` / `SUB_ZONA`.\n"
            "- **No coordinates on transactions or Catastro** — mapping comes "
            "from the routes KML. A parcel/sector shapefile with geometry would "
            "enable point-level analysis.\n"
            "- **Characterization isn't a clean per-tonne table** — a tidy "
            "composition % by year/stratum would replace the diversion "
            "assumptions.\n"
            "- **Landfill capacity isn't stated** — a remaining-airspace figure "
            "would make the forecast authoritative.\n"
            "- **Tare-vs-gross & duplicate weighings** — worth a source-side "
            "validation rule at the weighbridge.")

# ======================================================================
# TAB 3 — CATALOG
# ======================================================================
with tab_catalog:
    st.caption("Data model (sheets, columns) and row counts for every "
               "spreadsheet in the source ZIP.")
    if q.catalog_count(con) == 0 and not _HAS_ZIP:
        st.info("Catalog isn't bundled and the source ZIP isn't available in "
                "this environment.")
    elif q.catalog_count(con) == 0:
        st.info("Catalog not built yet (~30 s scan of every spreadsheet).")
        if st.button("📇 Build catalog", type="primary"):
            box = st.status("Scanning…", expanded=True)
            build_catalog(con, on_status=lambda m: box.update(label=m))
            box.update(label="Catalog built.", state="complete")
            st.rerun()
    else:
        tot = q.catalog_totals(con)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Spreadsheets", f"{tot['files']:,}")
        c2.metric("Sheets / tabs", f"{tot['sheets']:,}")
        c3.metric("Total rows (all)", f"{tot['rows']:,}")
        c4.metric("Files in DuckDB", f"{tot['files_in_duckdb']}/{tot['files']}",
                  help=f"{tot['src_tables']} src_* tables + 2 typed tables")
        summary = q.catalog_summary(con)
        show = summary.rename(columns={
            "folder": "Folder", "file_name": "File", "file_type": "Type",
            "size_mb": "Size (MB)", "sheets": "Sheets", "total_rows": "Total rows",
            "loaded_table": "DuckDB table"})
        st.dataframe(show, use_container_width=True, hide_index=True)
        st.markdown("**Per-file data model** — expand for sheets and columns.")
        for fname in summary["file_name"]:
            loaded = summary.loc[summary["file_name"] == fname, "loaded_table"].iloc[0]
            tag = "  ·  ✅ in DuckDB" if isinstance(loaded, str) and loaded != "—" else ""
            with st.expander(f"{fname}{tag}"):
                sheets = q.catalog_sheets(con, fname)
                for _, srow in sheets.iterrows():
                    tbl = srow["loaded_table"] or srow.get("src_table")
                    badge = f" → `{tbl}`" if tbl else ""
                    st.markdown(f"**{srow['sheet_name']}**{badge} — "
                                f"{srow['n_columns']} cols × {srow['n_rows']:,} rows")
                    if srow["columns"] and srow["columns"] != "[]":
                        cs = json.loads(srow["columns"])
                        st.caption(", ".join(cs) if cs else "—")
        if _HAS_ZIP and st.button("🔄 Rebuild catalog"):
            box = st.status("Rescanning…", expanded=True)
            build_catalog(con, on_status=lambda m: box.update(label=m))
            box.update(label="Catalog rebuilt.", state="complete")
            st.rerun()

# ======================================================================
# TAB 4 — SOURCE TABLES
# ======================================================================
with tab_src:
    st.caption("Every non-SCPD sheet loaded as a queryable `src_*` table "
               "(all-text). The pesaje files live in typed `transactions` / "
               "`retirados`.")
    con.execute(REGISTRY_SCHEMA)
    n_src = con.execute("SELECT count(*) FROM source_tables").fetchone()[0]
    if _HAS_ZIP:
        cta = "📥 Load all source tables" if n_src == 0 else "🔄 Reload all source tables"
        if st.button(cta):
            box = st.status("Loading every tabular sheet…", expanded=True)
            n = load_all_tables(con, on_status=lambda m: box.update(label=m))
            box.update(label=f"Loaded {n} source tables.", state="complete")
            st.rerun()
    elif n_src == 0:
        st.info("Source tables aren't bundled and the ZIP isn't available here.")
    if n_src:
        reg = con.execute("""
            SELECT table_name, file_name, sheet_name, n_rows, n_columns
            FROM source_tables ORDER BY n_rows DESC
        """).df()
        st.metric("Source tables loaded", f"{n_src:,}")
        st.dataframe(reg, use_container_width=True, hide_index=True,
                     column_config={"table_name": "DuckDB table", "file_name": "File",
                                    "sheet_name": "Sheet", "n_rows": "Rows",
                                    "n_columns": "Cols"})
