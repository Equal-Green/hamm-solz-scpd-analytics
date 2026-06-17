# SCPD Analytics — Guayaquil Solid Waste

A self-contained analytics application for Guayaquil, Ecuador's municipal solid
waste system — the **SCPD** (Sistema de Control y Pesaje de Desechos). Data
comes from the **Las Iguanas** landfill, operated by **Consorcio URVASEO** under
the municipal authority **CIRCULAREP**.

Point it at your copy of the source ZIP and get a fully interactive dashboard.
No database server, no cloud account, no subscriptions — **DuckDB** runs as a
local file and **Streamlit** serves the UI.

---

## Quick start (under 5 minutes)

1. **Python 3.10+** (developed on 3.13).
2. Clone this repo and `cd` into it.
3. Put the source ZIP somewhere and set its path. Either edit `ZIP_PATH` in
   [`config.py`](config.py) or export an environment variable:
   ```bash
   export SCPD_ZIP_PATH="/path/to/INFORMACIÓN.zip"
   ```
4. Install dependencies (a virtualenv is recommended):
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
5. Launch:
   ```bash
   streamlit run dashboard/app.py
   ```
6. On first run the app shows a **pipeline UI** — click **Run pipeline**.
   Extraction + load of all ~524K rows takes **3–6 minutes**. After that the
   data is cached in `data/scpd.duckdb` and every later launch goes straight to
   the dashboard.

---

## Architecture

**Phase 1 (this app, fully offline):**

```
ZIP → Python extraction pipeline → data/scpd.duckdb → Streamlit dashboard
```

**Phase 2 (hooks built, gated):** the Settings page has an *Export to Postgres /
Supabase* section. The export function ([`pipeline/export.py`](pipeline/export.py))
is wired but disabled by `CLOUD_EXPORT_ENABLED = False`. The app works 100%
offline without it.

### Why the pipeline is unusual

- **The source ZIP can't be opened by standard tools.** It was written in
  streaming mode (local-file flag bit 3, no End-of-Central-Directory record), so
  `unzip` / Python `zipfile` fail. We `mmap` the (multi-GB) archive and scan for
  `PK\x03\x04` local-file-header signatures. The four target files are *stored*
  (uncompressed) with their sizes in trailing data descriptors, so we
  forward-parse each inner `.xlsx` (itself a normal ZIP) through its local
  headers → central directory → EOCD to find its exact extent.
- **The Excel files are huge** (65–92 MB; one sheet decompresses to ~450 MB of
  XML). `openpyxl` / `pandas.read_excel` load the whole DOM and hang. We
  **SAX-parse** the worksheet XML as a stream, honoring each cell's `r=` column
  reference so empty cells don't shift columns, and batch-insert into DuckDB
  10,000 rows at a time.

### Columns (resolved by header name, verified against the real files)

The logical names in the project brief don't all exist as literal headers. The
verified mapping:

| Field           | Real header          | Notes                                  |
|-----------------|----------------------|----------------------------------------|
| `num_ticket`    | `NUM_TICKET` / `NUM_TICKET_CARGA` | string in GEOCYCLE |
| `tipo_vehiculo` | `TIPO_VEHICULO`      | vehicle class                          |
| `placa`         | `PLACA`              | license plate                          |
| `tipo_servicio` | `DESC_TIPO_DESECHO`  | **service dimension** (DOMICILIARIA, SERVICIOS ESPECIAL, …) |
| `empresa`       | `RAZON_SOCIAL`       | operating company                      |
| `sector`        | `SECTOR`             | city sector                            |
| `peso_ingreso`  | `PESO_INGRESO`       | gross in (kg)                          |
| `peso_salida`   | `PESO_SALIDA`        | tare out (kg)                          |
| `peso_neto`     | `PESO_NETO`          | net waste (kg)                         |
| `fec_ingreso`   | `FEC_INGRESO`        | Excel serial (main) / `dd/mm/yyyy` text (GEOCYCLE) |

GEOCYCLE recovery inverts the weight logic: trucks arrive empty and leave loaded,
so `PESO_SALIDA > PESO_INGRESO` and net recovered = exit − entry.

---

## Data notes

- **Verified row counts:** 2023 = 165,505 · 2024 = 176,979 · 2025 = 174,042 ·
  GEOCYCLE = 7,515 → **524,041 total**. The project brief stated 524,039; 2023
  and 2024 each carry one extra *genuine* row (distinct tickets, no nulls, no
  duplicates, no totals row). See the **Data Quality** page.
- **SERVICIOS ESPECIAL anomaly:** trips spiked from 17,150 (2023) to ~30,000
  (2024) — about **+75%** (the brief labelled it +83%; the dashboard computes the
  live figure). Surfaced on the **Service Types** page.

---

## Project layout

```
scpd-analytics/
├── config.py                 # ZIP_PATH, DUCKDB_PATH, file specs, column map
├── pipeline/
│   ├── discover.py           # scan ZIP → file inventory
│   ├── extract.py            # streaming ZIP scanner + SAX Excel parser
│   ├── load.py               # orchestrate extract → DuckDB, idempotent
│   └── export.py             # Phase 2 Postgres export (gated)
├── analysis/
│   └── queries.py            # all analytics as named SQL functions
├── dashboard/
│   ├── app.py                # entry: pipeline UI, then grouped st.navigation
│   ├── db.py / state.py / theme.py / style.py / ask_engine.py
│   └── pages/                # Executive Summary, Overview, Service Types,
│                             #   Operators, GEOCYCLE, Ask the Data,
│                             #   Data Quality & Catalog, Settings
└── data/                     # scpd.duckdb + raw/ (git-ignored)

The sidebar uses a **nested/grouped navigation** (`st.navigation`):
*Start here* (Executive Summary) · *The story* (Overview → Service Types →
Operators → GEOCYCLE) · *Explore* (Ask the Data) · *Trust & data* (Data Quality
& Catalog) · *System* (Settings).

### Ask the Data

A conversational page: a grouped list of suggested questions (volume, service
mix, operators, recovery, quality), each mapped to a DuckDB-backed answer
(sentence + chart/table). Free-text questions are routed to the closest
suggestion by keyword — so it works **fully offline, no API key**. A gated hook
(`ASK_AI_ENABLED` in `dashboard/ask_engine.py`) is left for optional Claude
NL→SQL later, mirroring the gated Postgres export.
```

## Geo & Routes

Transactions carry a collection geography: **ZONA** (A / B / RURAL), **SUB_ZONA**
(~30 zones like 12A), and **MICRO_RUTA** (~265 micro-route codes), ~97% / 48%
populated. The **Geo & Routes** page charts this hierarchy — a zone→sub-zone
treemap, tonnage by zone, top sub-zones, a sub-zone×month heatmap, and a
micro-route leaderboard. No point geometry ships with the data, so there's no
basemap yet; drop a sector/zone shapefile in later to unlock a choropleth (the
page notes this hook).

## All source tables in DuckDB

Beyond the four typed pesaje tables, **Data Quality & Catalog → All source
tables** loads *every* other tabular sheet in the archive (116 tables, incl.
Catastro urbano at ~599K rows) as all-text `src_*` tables, registered in
`source_tables`. One click; the whole archive becomes queryable.

## Source data catalog

The **Data Quality** page includes a catalog of **every spreadsheet in the
INFORMACIÓN folder** — not just the four pesaje files loaded into DuckDB. It
profiles all 20 workbooks (127 sheets/tabs total) and reports each sheet's
column model and row count, tagging the four SCPD files with their DuckDB
table. Build it from the Data Quality page (one-time ~30 s scan; the result is
stored in a `data_catalog` table). The big SCPD sheets reuse their known counts
rather than re-parsing ~450 MB of XML.

## Re-running the pipeline

The pipeline is idempotent: files already in `pipeline_log` are skipped. To force
a full reload, use **Settings → Re-run pipeline**, or delete
`data/scpd.duckdb` and relaunch.
