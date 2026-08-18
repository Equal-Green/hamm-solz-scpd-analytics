"""Contractual compliance model for the Ecuador Waste EIPP consultancy agreement.

Single source of truth for the signed Consultancy Service Agreement between
THE HAMM SOLZ Co., Ltd. ("THS") and Mr. Carlos Arcos Pastor ("Consultant").
The Agreement page reads this module and nothing else, so the contract text and
the declared status never drift apart across pages.

MAINTENANCE -- this file records *declared* status. When a deliverable lands,
set its `status` and append an `evidence` line (date + a pointer: email subject,
Drive link, sheet URL). Items left "not_started" surface on the page as open
gaps; that is intentional, not a bug. `verified=False` marks a status nobody has
checked against real artifacts yet, and the page counts those separately.
"""
import os
from datetime import date, timedelta

# --- Agreement facts (Clauses 1, 2, 6, 7 and the signature block) ------------
# Effective Date = date of the last signature. Consultant signed 26 May 2026;
# THS (Mr. Gyuha Choe, Head of Research Institute) signed 04 June 2026.
EFFECTIVE_DATE = date(2026, 6, 4)
TERM_DAYS = 90                      # Clause 2: ninety (90) calendar days

AGREEMENT = {
    "title": "Consultancy Service Agreement",
    "subtitle": "Data Management Consultant Services for the Ecuador Waste "
                "EIPP Project",
    "client": "THE HAMM SOLZ Co., Ltd. (“THS”)",
    "client_signatory": "Mr. Gyuha Choe — Head of Research Institute",
    "consultant": "Mr. Carlos Andrés Arcos Pastor",
    "consultant_email": "carlos@equalgreen.co",
    "counterparty": "Circular EP",   # the only in-scope external stakeholder
    "amount_usd": 2000,              # Clause 7: USD 2,000 lump sum
    "source_document": "Consultancy_Service_Agreement_Ecuador_EIPP_revised"
                       ".docx-signed.pdf",
    "documents": [
        "Agreement (Clauses 1–19)",
        "Annex 1 — Terms of Reference and Scope of Services",
        "Annex 2 — Deliverables, Records, and Implementation Requirements",
        "Annex 3 — Requested Materials List",
        "Annex 4 — Spanish Summary (coordination convenience only)",
    ],
}

# Internal view shows open gaps and maintenance notes; client view shows the
# same scores without the internal to-do commentary.
AUDIENCE = os.environ.get("SCPD_COMPLIANCE_AUDIENCE", "internal").lower()


def is_internal():
    return AUDIENCE != "client"


# --- Contract calendar -------------------------------------------------------
def date_for_day(day):
    """Calendar date for contract Day N (Clause 2: Day 1 = Effective Date)."""
    return EFFECTIVE_DATE + timedelta(days=day - 1)


END_DATE = date_for_day(TERM_DAYS)


def day_of_contract(today=None):
    """Contract day number for `today` (may exceed TERM_DAYS once expired)."""
    today = today or date.today()
    return (today - EFFECTIVE_DATE).days + 1


def biweekly_due_days():
    """Annex 2 #4: a progress report every two weeks inside the term."""
    return [d for d in range(14, TERM_DAYS + 1, 14)]


# --- Annex 2 #1: key deliverables -------------------------------------------
# status: complete | in_progress | not_started
# due_day: None means "ongoing throughout the term" (always in scope).
STATUS_VALUE = {"complete": 1.0, "in_progress": 0.5, "not_started": 0.0}

DELIVERABLES = [
    {
        "no": 1,
        "key": "coordination_plan",
        "title": "Initial Coordination Plan",
        "timing": "Week 1",
        "due_day": 7,
        "weight": 10,
        "content": "Brief document outlining coordination approach, contact "
                   "strategy, Circular EP contact channel, and initial "
                   "request list.",
        "status": "not_started",
        "verified": False,
        "evidence": [],
    },
    {
        "no": 2,
        "key": "tracking_matrix",
        "title": "Data Request Tracking Matrix",
        "timing": "Ongoing; updated bi-weekly",
        "due_day": None,
        "weight": 20,
        "content": "Editable spreadsheet tracking requests, responses, "
                   "follow-ups, receipt status, pending items, unavailable "
                   "items, and comments.",
        "status": "not_started",
        "verified": False,
        "evidence": [],
    },
    {
        "no": 3,
        "key": "file_repository",
        "title": "Organized Digital File Repository",
        "timing": "Ongoing; final on Day 90",
        "due_day": None,
        "weight": 25,
        "content": "Structured folder system or digital handover package with "
                   "clear naming conventions and topic-based organization.",
        "status": "in_progress",
        "verified": True,
        "evidence": [
            "Source archive received from Circular EP and catalogued: "
            "{files} files across {folders} topic folders "
            "(data/archive_inventory.json).",
            "Tabular sources typed and loaded into a single DuckDB file "
            "({rows} rows) — see the Data Quality & Catalog page.",
            "Repository is organized and navigable; the Day-90 handover "
            "package itself is not yet issued.",
        ],
    },
    {
        "no": 4,
        "key": "biweekly_reports",
        "title": "Bi-weekly Progress Reports",
        "timing": "Every 2 weeks",
        "due_day": None,
        "weight": 20,
        "content": "Email-format updates covering activities completed, "
                   "materials received, pending items, follow-up status, "
                   "issues, delays, and next actions.",
        "status": "not_started",
        "verified": False,
        "evidence": [],
    },
    {
        "no": 5,
        "key": "midterm_summary",
        "title": "Mid-term Summary",
        "timing": "Day 45",
        "due_day": 45,
        "weight": 10,
        "content": "Assessment of progress to date, materials obtained, "
                   "challenges, data gaps, Circular EP response status, and "
                   "outlook for the remaining period.",
        "status": "not_started",
        "verified": False,
        "evidence": [],
    },
    {
        "no": 6,
        "key": "final_handover",
        "title": "Final Handover Package",
        "timing": "Day 90",
        "due_day": 90,
        "weight": 15,
        "content": "Organized file repository, final inventory spreadsheet, "
                   "comprehensive summary report, and list of pending or "
                   "unavailable items with explanations.",
        "status": "not_started",
        "verified": False,
        "evidence": [],
    },
]

# Bi-weekly report log: contract day -> ISO date the report was sent, or None.
# Fills deliverable #4's score as sent / due-so-far.
BIWEEKLY_LOG = {day: None for day in biweekly_due_days()}

# --- Annex 2 #3: success indicators (qualitative, declared) ------------------
SUCCESS_INDICATORS = [
    {"text": "Documented communication with Circular EP, including evidence "
             "of requests sent.", "status": "not_started"},
    {"text": "Systematic follow-up conducted and documented for pending "
             "requests.", "status": "not_started"},
    {"text": "Professional organization of materials actually received.",
     "status": "complete"},
    {"text": "Complete and up-to-date tracking matrix maintained.",
     "status": "not_started"},
    {"text": "Timely delivery of bi-weekly progress reports and other "
             "deliverables.", "status": "not_started"},
    {"text": "Clear documentation of pending items, unavailable items, "
             "delays, source limitations, and issues.",
     "status": "in_progress"},
]

# --- Annex 2 #2: implementation requirements --------------------------------
IMPLEMENTATION_REQUIREMENTS = [
    {"text": "Coordination carried out in Ecuador, in person or remotely; "
             "field visits and site inspections are not included.",
     "status": "complete"},
    {"text": "Major progress updates shared by email or online meetings.",
     "status": "not_started"},
    {"text": "Periodic updates on requested materials, pending responses, "
             "data gaps, unavailable materials, and source limitations.",
     "status": "not_started"},
    {"text": "All source files actually received transferred promptly to THS "
             "in editable or original format where possible.",
     "status": "in_progress"},
    {"text": "Reasonable communication records and supporting evidence of "
             "follow-up actions retained.", "status": "not_started"},
]

# --- Clause 3 / Annex 1 #4: exclusions the Consultant must stay clear of -----
# Compliance here means *not* having done these without written THS approval.
EXCLUSIONS = [
    "No field visits to Las Iguanas or Puná Island.",
    "No independent research or primary data collection.",
    "No surveys, interviews, or consultations with stakeholders other than "
    "Circular EP.",
    "No site inspections or facility assessments.",
    "No guarantee that Circular EP will possess, collect, disclose, or "
    "deliver any specific material within the Contract Term.",
    "No responsibility for the quality, accuracy, completeness, technical "
    "adequacy, usability, or format of source materials from Circular EP.",
]

# --- Annex 3: requested materials, mapped to the archive actually received ---
# Each category lists the leading numbers of the source-archive top-level
# folders that satisfy it, so coverage is computed from real files rather than
# asserted. Folder numbers match data/archive_inventory.json.
ANNEX3_CATEGORIES = [
    {"letter": "A", "title": "Waste characteristics and generation data",
     "folders": [1, 4]},
    {"letter": "B", "title": "Las Iguanas disposal site and facility data",
     "folders": [4, 9]},
    {"letter": "C", "title": "Drawings, plans, and spatial information",
     "folders": [2, 3, 7, 8]},
    {"letter": "D", "title": "Collection, transport, treatment, and disposal",
     "folders": [7]},
    {"letter": "E", "title": "Puná Island-specific data",
     "folders": [2, 10]},
    {"letter": "F", "title": "Institutional, legal, and planning documents",
     "folders": [5, 6]},
    {"letter": "G", "title": "Socioeconomic and forecasting reference data",
     "folders": [6]},
    {"letter": "H", "title": "Supporting records",
     "folders": [9, 10]},
]


def _folder_number(folder_name):
    """Leading number of an archive folder name ("4. DATA DEL ..." -> 4)."""
    head = folder_name.split(".", 1)[0].strip()
    return int(head) if head.isdigit() else None


def annex3_coverage(inventory):
    """Per-category Annex 3 coverage from the received archive inventory.

    `inventory` is the dict in data/archive_inventory.json. Returns a list of
    rows plus the overall received/mapped fraction.
    """
    present = {}
    for f in (inventory or {}).get("folders", []):
        num = _folder_number(f.get("folder", ""))
        if num is not None and f.get("files", 0) > 0:
            present[num] = f

    rows, got, want = [], 0, 0
    for cat in ANNEX3_CATEGORIES:
        hits = [n for n in cat["folders"] if n in present]
        files = sum(present[n]["files"] for n in hits)
        got += len(hits)
        want += len(cat["folders"])
        rows.append({
            "letter": cat["letter"],
            "title": cat["title"],
            "sources_received": len(hits),
            "sources_mapped": len(cat["folders"]),
            "files": files,
            "folders": [present[n]["folder"] for n in hits],
        })
    return rows, (got / want if want else 0.0)


# --- Scoring -----------------------------------------------------------------
def biweekly_progress(today=None):
    """(sent, due-so-far) counts for the bi-weekly report obligation."""
    day = day_of_contract(today)
    due = [d for d in biweekly_due_days() if d <= day]
    sent = [d for d in due if BIWEEKLY_LOG.get(d)]
    return len(sent), len(due)


def deliverable_score(d, today=None):
    """Fractional completion 0.0-1.0 for one deliverable."""
    if d["key"] == "biweekly_reports":
        sent, due = biweekly_progress(today)
        return (sent / due) if due else 1.0
    return STATUS_VALUE.get(d["status"], 0.0)


def is_in_scope_now(d, today=None):
    """True when the deliverable is ongoing or its due date has passed."""
    return d["due_day"] is None or d["due_day"] <= day_of_contract(today)


def score(today=None):
    """Headline compliance numbers.

    to_date        -- weighted completion of what is owed as of today. This is
                      the accountability number.
    overall        -- weighted completion of the full 90-day deliverable set.
    """
    today = today or date.today()
    rows = []
    for d in DELIVERABLES:
        rows.append({
            **d,
            "fraction": deliverable_score(d, today),
            "in_scope_now": is_in_scope_now(d, today),
            "due_date": date_for_day(d["due_day"]) if d["due_day"] else None,
        })

    def weighted(items):
        w = sum(r["weight"] for r in items)
        return (sum(r["weight"] * r["fraction"] for r in items) / w) if w else 0.0

    due_now = [r for r in rows if r["in_scope_now"]]
    day = day_of_contract(today)
    return {
        "rows": rows,
        "to_date": weighted(due_now),
        "overall": weighted(rows),
        "day": day,
        "days_remaining": max(TERM_DAYS - day, 0),
        "term_elapsed": min(max(day / TERM_DAYS, 0.0), 1.0),
        "expired": day > TERM_DAYS,
        "unverified": sum(1 for d in DELIVERABLES if not d["verified"]),
        "at_risk": [r for r in due_now if r["fraction"] < 1.0],
    }


def indicator_score(items):
    """Fraction complete across a list of {status: ...} declarations."""
    if not items:
        return 0.0
    return sum(STATUS_VALUE.get(i["status"], 0.0) for i in items) / len(items)


# --- Annex 3, item level ------------------------------------------------------
# The 36 individual materials listed in Annex 3, each mapped to the archive
# folder numbers that appear to satisfy it. `coverage` is a first-pass reading
# of the delivered archive, NOT a confirmed status:
#   received -- folder contents clearly answer the item
#   partial  -- related material is present but does not fully answer the item
#   none     -- nothing in the archive answers it
# The Consultant confirms or corrects each row; the tracking matrix carries the
# request dates and follow-up history, which only the Consultant's own
# correspondence record can supply.
ANNEX3_ITEMS = [
    # A. Waste characteristics and waste generation data
    ("A1", "A", "Existing waste characterization study results for Las Iguanas, "
     "Guayaquil, and Puná Island", [1], "received",
     "Characterization studies 2012–2026 plus Análisis_Las_Iguanas.pdf."),
    ("A2", "A", "Historical municipal solid waste generation data for Guayaquil "
     "and Puná Island, preferably the most recent five (5) years or more",
     [4, 9], "partial",
     "Weighbridge data covers 2023–2025 (three years, not five)."),
    ("A3", "A", "Daily, monthly, and annual waste quantity records", [4, 9],
     "received", "Ticket-level weighbridge records; 524,041 rows typed."),
    ("A4", "A", "Per capita waste generation data", [], "none",
     "Not delivered as data; would require population figures to derive."),
    ("A5", "A", "Seasonal fluctuation data, including tourism-related variation",
     [], "none",
     "Not delivered as a dataset; seasonality is derivable from A3 but was not "
     "provided as such."),
    # B. Las Iguanas disposal site and related facility data
    ("B1", "B", "Historical waste inflow records for Las Iguanas, preferably "
     "the most recent five (5) years or more", [4, 9], "partial",
     "2023–2025 inflow, plus Cantidad de desechos dispuesto ILM Guayaquil.xlsx."),
    ("B2", "B", "Waste inflow by type, source, or service area", [4], "received",
     "Service type, operator, and collection zone carried per ticket."),
    ("B3", "B", "Current operational status information for Las Iguanas", [9],
     "partial", "Environmental licence and PMA documents; no status statement."),
    ("B4", "B", "Remaining capacity, cell operation information, and expected "
     "service life", [9], "partial",
     "2017 final-disposal design (staged development) is present; remaining "
     "capacity is not stated anywhere in the delivery."),
    ("B5", "B", "Leachate management, landfill gas management, environmental "
     "monitoring, and operational constraints", [9], "received",
     "Leachate drainage and biogás studies, PMA updates, biogas plant records."),
    # C. Drawings, plans, and spatial information
    ("C1", "C", "Site layout drawings for Las Iguanas and related facilities",
     [9], "received", "Plano Proyecto Terreno Natural and related DWG set."),
    ("C2", "C", "Facility plans, process flow diagrams, cross-sections, and "
     "operational area drawings", [9, 2], "received",
     "2017 design study drawings; Puná study engineering drawings."),
    ("C3", "C", "CAD drawings (DWG or equivalent)", [2, 7, 9, 10], "received",
     "269 DWG files across the Puná study, route plans, and site design."),
    ("C4", "C", "GIS data, maps, service area boundaries, and facility location "
     "information", [3, 7, 8], "received",
     "Shapefile sets, cantonal cartography, AGAS.kmz, PUGS map package."),
    ("C5", "C", "Collection routes, transport routes, transfer points, and "
     "related spatial data", [7], "received",
     "Routes KML — 48 sub-zone polygons and 472 day/night routes."),
    # D. Collection, transport, treatment, and disposal system data
    ("D1", "D", "Current waste collection system information for Guayaquil and "
     "Puná Island", [7, 10], "partial",
     "DIÁGNOSTICO DE LA GIRS plus zone/sub-zone plans; no system description."),
    ("D2", "D", "Collection coverage, frequency, service areas, and operating "
     "arrangements", [7], "received",
     "Zone/sub-zone route plans with day and night production schedules."),
    ("D3", "D", "Vehicle and equipment inventory — type, capacity, quantity, "
     "operating entity", [], "none",
     "Plates and operators appear per weighbridge ticket, but no fleet "
     "inventory was delivered."),
    ("D4", "D", "Current waste transport arrangements, including mainland and "
     "island logistics", [10], "partial",
     "Registro de viajes de recolección for Puná; no mainland-island logistics."),
    ("D5", "D", "Treatment, recycling, resource recovery, transfer, and final "
     "disposal practices currently in use", [4, 9], "partial",
     "GEOCYCLE recovery records and the final-disposal design; no current "
     "practice description."),
    ("D6", "D", "Informal recycling, waste picking, or material recovery "
     "activities", [], "none", "Not delivered."),
    # E. Puná Island-specific data
    ("E1", "E", "Current waste generation, collection, transport, treatment, "
     "and disposal conditions on Puná Island", [2, 10], "partial",
     "Puná diagnostic study and trench-disposal records; partial coverage."),
    ("E2", "E", "Existing waste handling points, temporary storage, disposal "
     "sites, or transfer arrangements on Puná Island", [10], "partial",
     "Desechos Dispuestos en trinchera #1 (May 2026) drawing."),
    ("E3", "E", "Waste transport arrangements between Puná Island and the "
     "mainland", [], "none", "Not delivered."),
    ("E4", "E", "Local constraints affecting waste management on Puná Island — "
     "access, distance, weather, transport, institutional", [2], "partial",
     "Hydrological, geological, and diagnostic studies carry some constraints."),
    ("E5", "E", "Documented local environmental issues — open dumping, burning, "
     "marine leakage, unmanaged waste", [2, 10], "partial",
     "Environmental register resolution and PMA matrix; not issue-specific."),
    # F. Institutional, legal, and planning documents
    ("F1", "F", "Laws, regulations, policies, and municipal ordinances on solid "
     "waste management", [5], "received",
     "29 PDFs: COA, LOECI, plastics law, ENECI, Circular EP statute."),
    ("F2", "F", "Waste management plans, master plans, development plans, and "
     "related reports", [5, 6], "received",
     "Circular EP 2025–2027 business/investment plan; PDOT Gaceta-43."),
    ("F3", "F", "Previous studies, feasibility studies, technical assessments, "
     "and environmental reports", [1, 2, 9], "received",
     "Puná Fase I study set, 2017 design study, EIA, characterization studies."),
    ("F4", "F", "Institutional structure, roles, and responsibilities of "
     "relevant agencies and operators", [5], "partial",
     "Circular EP Estatuto y Estructura only; no cross-agency map."),
    # G. Socioeconomic and forecasting reference data
    ("G1", "G", "Population data and population projections for Guayaquil and "
     "Puná Island", [6], "partial",
     "PUGS/PDOT contain projections; no standalone population dataset."),
    ("G2", "G", "Tourism, seasonal population, commercial activity, or urban "
     "development data for generation forecasting", [], "none",
     "Not delivered."),
    ("G3", "G", "Land use plans, urban development plans, and planned projects "
     "relevant to future waste service demand", [6], "received",
     "PUGS 2023–2027 map package and PDOT gazette."),
    # H. Supporting records
    ("H1", "H", "Photographs, site records, monitoring summaries, and "
     "operational reports", [2, 9], "partial",
     "Site photographs and monitoring content inside the study sets."),
    ("H2", "H", "Meeting records or consultation notes with relevant "
     "institutions and operators", [], "none", "Not delivered."),
    ("H3", "H", "Explanatory notes from Circular EP on unavailable, pending, "
     "restricted, or incomplete materials", [], "none",
     "Not delivered — and this is the item that most directly supports the "
     "Annex 1 §5 protection. Worth requesting in writing before Day 90."),
]

# Correspondence references found embedded in delivered file names. Candidate
# evidence of formal request/response traffic with Circular EP; the Consultant
# confirms which belong to this engagement versus pre-existing internal records.
CORRESPONDENCE_REFS = [
    ("OFC. No.286-2026", "1. CARACTERIZACION",
     "Resultados de caracterización de residuos sólidos urbanos de Guayaquil"),
    ("OFC. No.572-2023", "1. CARACTERIZACION",
     "Caracterización Residuos Sólidos Urbanos 2022–2023"),
    ("OFC. No.272-2022", "1. CARACTERIZACION",
     "Método de cuarteo CEPIS — selección de muestras"),
    ("OFC. No. 210-2021", "1. CARACTERIZACION", "Caracterización 2021"),
    ("OFC. No.269-2020", "1. CARACTERIZACION",
     "Ensayos de caracterización 2020"),
    ("LO-2022-030", "1. CARACTERIZACION",
     "Aprobación de estudios de selección de muestras"),
    ("OF CIRCULAREP-GG-2025-007-O", "3. CARTOGRAFÍA DEL CANTON",
     "Circular EP General Management transmittal"),
    ("DUMCE-CA-2025-3661 / EXT-DUMCE-2025-52", "3. CARTOGRAFÍA DEL CANTON",
     "Cartography request routing"),
    ("CIRCULAREP-DIR-008-2024", "5. NORMATIVAS",
     "Reglamento de asociatividad, signed and approved"),
    ("DMA-LA-2013-034", "9. INFORMACION LAS IGUANAS",
     "Las Iguanas environmental licence"),
    ("DMA-2019-1494", "9. INFORMACION LAS IGUANAS",
     "Environmental licence change of titleholder"),
]


def annex3_item_rows(inventory):
    """Annex 3 items joined to the folders actually present in the archive."""
    present = {}
    for f in (inventory or {}).get("folders", []):
        num = _folder_number(f.get("folder", ""))
        if num is not None and f.get("files", 0) > 0:
            present[num] = f

    rows = []
    for ref, cat, item, folders, coverage, note in ANNEX3_ITEMS:
        hits = [present[n]["folder"] for n in folders if n in present]
        rows.append({"ref": ref, "category": cat, "item": item,
                     "coverage": coverage, "folders": hits,
                     "files": sum(present[n]["files"] for n in folders
                                  if n in present),
                     "note": note})
    return rows


def annex3_item_summary(inventory):
    """Counts by coverage label across the 36 Annex 3 items."""
    rows = annex3_item_rows(inventory)
    out = {"received": 0, "partial": 0, "none": 0}
    for r in rows:
        out[r["coverage"]] += 1
    out["total"] = len(rows)
    # Partial counts as half credit -- material is on hand but the item is not
    # fully answered.
    out["weighted"] = (out["received"] + 0.5 * out["partial"]) / len(rows)
    return out
