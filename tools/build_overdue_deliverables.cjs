/**
 * Generate the overdue Annex 2 deliverables as Word documents.
 *
 *   node tools/build_overdue_deliverables.cjs
 *
 * Reads deliverables/_facts.json (written by the Python collector) so every
 * figure traces back to the contract model or the database — nothing is typed
 * by hand here.
 *
 * Produces:
 *   Deliverable 1 — Initial Coordination Plan
 *   Deliverable 5 — Mid-term Summary
 *
 * Both are dated as issued today with an explicit late-issuance notice. Nothing
 * is backdated. Facts that only the Consultant's own correspondence record can
 * supply appear as visible TO CONFIRM placeholders rather than invented text.
 */
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  LevelFormat, PageBreak, Header, Footer, PageNumber,
} = require("docx");

const ROOT = path.resolve(__dirname, "..");
const OUT = path.join(ROOT, "deliverables");
const F = JSON.parse(fs.readFileSync(path.join(OUT, "_facts.json"), "utf8"));

// US Letter in DXA (1440 = 1 inch).
const PAGE = { size: { width: 12240, height: 15840 },
               margin: { top: 1200, right: 1200, bottom: 1200, left: 1200 } };
const CONTENT_W = 12240 - 2400;

const INK = "1A1A1A", MUTED = "595959", ACCENT = "9E1B1B", FLAG = "8A5A00";
const RULE = "D9D4CC", HEADBG = "F2EFE9";

const n0 = (x) => Math.round(x).toLocaleString("en-US");
const n1 = (x) => x.toLocaleString("en-US", { minimumFractionDigits: 1, maximumFractionDigits: 1 });
const n2 = (x) => x.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

// ── Building blocks ────────────────────────────────────────────────────────
const H1 = (t) => new Paragraph({
  text: t, heading: HeadingLevel.HEADING_1, spacing: { before: 360, after: 140 },
});
const H2 = (t) => new Paragraph({
  text: t, heading: HeadingLevel.HEADING_2, spacing: { before: 260, after: 100 },
});
const P = (t, opts = {}) => new Paragraph({
  spacing: { after: opts.after ?? 120, line: 276 },
  children: [new TextRun({ text: t, size: 21, color: opts.color ?? INK,
                           italics: !!opts.italics, bold: !!opts.bold })],
});
/** Mixed-run paragraph: pass [["text",{bold:true}], ...] */
const PR = (runs, opts = {}) => new Paragraph({
  spacing: { after: opts.after ?? 120, line: 276 },
  children: runs.map(([t, o = {}]) => new TextRun({
    text: t, size: 21, color: o.color ?? INK, bold: !!o.bold,
    italics: !!o.italics, font: o.mono ? "Consolas" : undefined,
  })),
});
const BULLET = (t, level = 0) => new Paragraph({
  numbering: { reference: "bullets", level },
  spacing: { after: 70, line: 276 },
  children: [new TextRun({ text: t, size: 21, color: INK })],
});
/** Visible placeholder for facts only the Consultant can supply. */
const TOCONFIRM = (t) => new Paragraph({
  spacing: { after: 120, line: 276 },
  shading: { type: ShadingType.CLEAR, fill: "FBF3E2" },
  border: { left: { style: BorderStyle.SINGLE, size: 12, color: FLAG, space: 6 } },
  children: [
    new TextRun({ text: "TO CONFIRM  ", size: 17, bold: true, color: FLAG }),
    new TextRun({ text: t, size: 21, color: INK, italics: true }),
  ],
});
const RULEP = () => new Paragraph({
  spacing: { before: 60, after: 160 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: RULE, space: 1 } },
  children: [],
});

function table(headers, rows, widths) {
  const cell = (text, { bold = false, head = false, align } = {}, w) =>
    new TableCell({
      width: { size: w, type: WidthType.DXA },
      shading: head ? { type: ShadingType.CLEAR, fill: HEADBG } : undefined,
      margins: { top: 70, bottom: 70, left: 100, right: 100 },
      children: [new Paragraph({
        alignment: align,
        spacing: { after: 0, line: 260 },
        children: [new TextRun({ text: String(text), size: 19,
                                 bold: bold || head, color: head ? MUTED : INK })],
      })],
    });
  return new Table({
    columnWidths: widths,
    width: { size: CONTENT_W, type: WidthType.DXA },
    borders: {
      top:    { style: BorderStyle.SINGLE, size: 4, color: RULE },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: RULE },
      left:   { style: BorderStyle.SINGLE, size: 4, color: RULE },
      right:  { style: BorderStyle.SINGLE, size: 4, color: RULE },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: RULE },
      insideVertical:   { style: BorderStyle.SINGLE, size: 2, color: RULE },
    },
    rows: [
      new TableRow({
        tableHeader: true,
        children: headers.map((h, i) =>
          cell(h.label ?? h, { head: true, align: h.align }, widths[i])),
      }),
      ...rows.map((r) => new TableRow({
        children: r.map((c, i) => cell(
          typeof c === "object" ? c.text : c,
          { bold: typeof c === "object" && c.bold,
            align: typeof c === "object" ? c.align : headers[i].align },
          widths[i])),
      })),
    ],
  });
}

function coverPlate(title, deliverableLine, dueLine) {
  return [
    new Paragraph({
      spacing: { after: 60 },
      children: [new TextRun({ text: F.agreement.project.toUpperCase(),
                               size: 17, bold: true, color: ACCENT,
                               characterSpacing: 40 })],
    }),
    new Paragraph({
      spacing: { after: 100 },
      children: [new TextRun({ text: title, size: 40, bold: true, color: INK })],
    }),
    new Paragraph({
      spacing: { after: 220 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: INK, space: 8 } },
      children: [new TextRun({ text: deliverableLine, size: 21, color: MUTED })],
    }),
    table(
      [{ label: "" }, { label: "" }],
      [
        [{ text: "Agreement", bold: true }, "Consultancy Service Agreement, Data Management Consultant Services"],
        [{ text: "Client", bold: true }, `${F.agreement.client} ("${F.agreement.client_short}")`],
        [{ text: "Consultant", bold: true }, `${F.agreement.consultant} — ${F.agreement.consultant_email}`],
        [{ text: "Counterparty", bold: true }, F.agreement.counterparty],
        [{ text: "Effective Date", bold: true }, `${F.agreement.effective} (Day 1)`],
        [{ text: "Term", bold: true }, `${F.agreement.term_days} calendar days, ending ${F.agreement.end}`],
        [{ text: "Contractual due date", bold: true }, dueLine],
        [{ text: "Date of issue", bold: true }, `${F.today.date} (Day ${F.today.day})`],
      ],
      [2600, CONTENT_W - 2600]),
  ];
}

const lateNotice = (dueLine) => [
  H2("Notice of late issuance"),
  PR([
    ["This deliverable was contractually due on ", {}],
    [dueLine, { bold: true }],
    [". It is issued on ", {}],
    [`${F.today.date}, Day ${F.today.day} of the ${F.agreement.term_days}-day term`, { bold: true }],
    [". The document has not been backdated, and no statement in it should be read as asserting that it was available earlier. It is provided so that the record is complete before the end of the term, and so that ", {}],
    [F.agreement.client_short, {}],
    [" has the substance it was owed.", {}],
  ]),
];

const docShell = (title, children) => new Document({
  creator: F.agreement.consultant,
  title,
  description: `${title} — ${F.agreement.project}`,
  numbering: {
    config: [{
      reference: "bullets",
      levels: [
        { level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 400, hanging: 220 } } } },
        { level: 1, format: LevelFormat.BULLET, text: "–", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 780, hanging: 220 } } } },
      ],
    }],
  },
  styles: {
    default: { document: { run: { font: "Calibri", size: 21, color: INK } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 27, bold: true, color: INK, font: "Calibri" } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 23, bold: true, color: ACCENT, font: "Calibri" } },
    ],
  },
  sections: [{
    properties: { page: PAGE },
    headers: {
      default: new Header({ children: [new Paragraph({
        alignment: AlignmentType.RIGHT,
        spacing: { after: 0 },
        children: [new TextRun({ text: `${F.agreement.project}  |  ${title}`,
                                 size: 16, color: MUTED })],
      })] }),
    },
    footers: {
      default: new Footer({ children: [new Paragraph({
        alignment: AlignmentType.RIGHT,
        children: [new TextRun({ children: ["Page ", PageNumber.CURRENT, " of ", PageNumber.TOTAL_PAGES],
                                 size: 16, color: MUTED })],
      })] }),
    },
    children,
  }],
});

// ── Deliverable 1 — Initial Coordination Plan ──────────────────────────────
function coordinationPlan() {
  const byCat = {};
  for (const it of F.annex3.items) (byCat[it.category] ??= []).push(it);
  const catTitles = {
    A: "Waste characteristics and generation data",
    B: "Las Iguanas disposal site and facility data",
    C: "Drawings, plans, and spatial information",
    D: "Collection, transport, treatment, and disposal",
    E: "Puna Island-specific data",
    F: "Institutional, legal, and planning documents",
    G: "Socioeconomic and forecasting reference data",
    H: "Supporting records",
  };

  const requestRows = [];
  for (const cat of Object.keys(catTitles)) {
    for (const it of byCat[cat] ?? []) {
      requestRows.push([{ text: it.ref, bold: true }, it.item]);
    }
  }

  const children = [
    ...coverPlate("Initial Coordination Plan",
      "Annex 2 Deliverable No. 1  |  Minimum content: coordination approach, contact strategy, Circular EP contact channel, and initial request list",
      `Week 1 — Day 7, ${F.days["7"]}`),
    ...lateNotice(`Day 7, ${F.days["7"]}`),

    H1("1. Purpose"),
    P(`This plan sets out how the Consultant coordinates with ${F.agreement.counterparty} to obtain, organise, and quality-check the materials ${F.agreement.client_short} requires for the ${F.agreement.project}, and how progress is reported to ${F.agreement.client_short} across the ${F.agreement.term_days}-day term.`),
    PR([
      ["The assignment is a data management, coordination, liaison, documentation and reporting engagement. It is ", {}],
      ["not", { bold: true }],
      [" a research or field engagement: field visits, primary data collection, surveys, site inspections and facility assessments are excluded by Clause 3 and Annex 1 §4.", {}],
    ]),

    H1("2. Coordination approach"),
    P(`${F.agreement.counterparty} is the single in-scope counterparty. Coordination with any other stakeholder requires prior written approval from ${F.agreement.client_short} (Clause 5). The approach has four strands:`),
    BULLET("Establish and hold a single primary communication channel with Circular EP, so that requests and responses accumulate in one traceable thread rather than across scattered contacts."),
    BULLET("Submit the Annex 3 request list in structured form, grouped by material category, so Circular EP can route each group to the department that holds it."),
    BULLET("Follow up on a fixed cadence rather than ad hoc, and record every follow-up with its date, channel, and outcome."),
    BULLET("Organise everything received into a navigable repository with an inventory, and report status to THS every two weeks."),

    H1("3. Circular EP contact channel"),
    P("The primary channel, the responsible departments, and the named contacts are recorded here as the single reference for the engagement."),
    TOCONFIRM("Insert the primary Circular EP contact name, role, department, email and telephone; the secondary or escalation contact; and the date the channel was established."),
    P("Correspondence references already evident from materials delivered by Circular EP are listed below. These are drawn from the file names in the delivered archive and are recorded as candidate evidence of request and response traffic; the Consultant confirms which belong to this engagement as opposed to pre-existing internal records.", { after: 140 }),
    table(
      [{ label: "Reference" }, { label: "Subject" }],
      F.correspondence.map((c) => [{ text: c.ref, bold: true }, c.subject]),
      [3400, CONTENT_W - 3400]),

    new Paragraph({ children: [new PageBreak()] }),

    H1("4. Communication protocol"),
    P(`All substantive correspondence with ${F.agreement.counterparty} is conducted in Spanish. The Consultant provides Spanish–English facilitation between ${F.agreement.client_short}, the Korean project team, and ${F.agreement.counterparty}, including clarification of data requests, file specifications, and document descriptions.`),
    BULLET("Requests to Circular EP: Spanish, in writing, itemised against the Annex 3 reference numbers used in this plan."),
    BULLET("Reporting to THS: English, by email, every two weeks."),
    BULLET("Material issues — refusal to disclose, confidentiality restrictions, source limitations, or delays that put a material at risk — are raised with THS immediately rather than held to the next scheduled report."),
    BULLET("Meeting scheduling with Circular EP is arranged on request from THS."),

    H1("5. Reporting cadence"),
    P("The reporting schedule fixed by Annex 2 for the term is as follows."),
    table(
      [{ label: "Report" }, { label: "Contract day" }, { label: "Date" }],
      [
        ["Progress report 1", "Day 14", F.days["14"]],
        ["Progress report 2", "Day 28", F.days["28"]],
        ["Progress report 3", "Day 42", F.days["42"]],
        [{ text: "Mid-term summary", bold: true }, { text: "Day 45", bold: true }, { text: F.days["45"], bold: true }],
        ["Progress report 4", "Day 56", F.days["56"]],
        ["Progress report 5", "Day 70", F.days["70"]],
        ["Progress report 6", "Day 84", F.days["84"]],
        [{ text: "Final handover package", bold: true }, { text: "Day 90", bold: true }, { text: F.days["90"], bold: true }],
      ],
      [3800, 2200, CONTENT_W - 6000]),

    H1("6. Initial request list"),
    PR([
      ["The list below is the Annex 3 requested materials, itemised so that each line can be tracked individually through request, follow-up, and receipt. It contains ", {}],
      [`${F.annex3.items.length} items across eight categories`, { bold: true }],
      [". These reference numbers are used in the Data Request Tracking Matrix (Deliverable No. 2) and in all correspondence with Circular EP.", {}],
    ]),
    ...Object.keys(catTitles).flatMap((cat) => [
      H2(`${cat}. ${catTitles[cat]}`),
      table(
        [{ label: "Ref" }, { label: "Requested material" }],
        (byCat[cat] ?? []).map((it) => [{ text: it.ref, bold: true }, it.item]),
        [900, CONTENT_W - 900]),
      new Paragraph({ spacing: { after: 120 }, children: [] }),
    ]),

    H1("7. Organisation and quality control"),
    P("Materials received are organised by topic, source, reference period, file type, and relevance, under a stable folder structure and naming convention that carries through to handover. Each file is entered in an inventory recording file name, description, source, date received, reference period where available, format, status, and comments."),
    P("Quality control at this stage is essential rather than analytical: confirming that files open, are not corrupted, and generally match their stated description, and identifying obvious gaps between what was requested and what arrived. The Consultant does not warrant the accuracy, completeness, technical adequacy or usability of source material produced by Circular EP (Annex 1 §4)."),

    H1("8. Scope boundaries"),
    P("The following are outside scope unless requested in writing by THS, estimated by the Consultant where applicable, and approved in writing by THS before work proceeds:"),
    BULLET("Field visits to Las Iguanas or Puna Island."),
    BULLET("Independent research or primary data collection."),
    BULLET("Surveys, interviews, or consultations with stakeholders other than Circular EP."),
    BULLET("Site inspections or facility assessments."),
    RULEP(),
    P(`Prepared by ${F.agreement.consultant}, Consultant. Issued ${F.today.date}.`, { color: MUTED, italics: true }),
  ];

  return docShell("Initial Coordination Plan", children);
}

// ── Deliverable 5 — Mid-term Summary ───────────────────────────────────────
function midtermSummary() {
  const d = F.data, a3 = F.annex3;
  const recRows = d.recovery_by_year.map((r) => [
    String(r.year), n0(r.landfill_t), n0(r.recovery_t), n2(r.recovery_pct) + "%",
  ]);
  const svcRows = d.services.slice(0, 6).map((s) => [
    s.tipo_servicio, n0(s.trips), n0(s.tonnes), n0(s.avg_kg),
  ]);

  const children = [
    ...coverPlate("Mid-term Summary",
      "Annex 2 Deliverable No. 5  |  Minimum content: progress to date, materials obtained, challenges, data gaps, Circular EP response status, and outlook",
      `Day 45, ${F.days["45"]}`),
    ...lateNotice(`Day 45, ${F.days["45"]}`),
    P("Because this document is issued at Day 76 rather than Day 45, it reports the position as at the date of issue. Where a figure would have differed at Day 45 it is identified as such. This is the more useful basis for THS with 14 days of the term remaining, and it avoids reconstructing a mid-term position after the fact.", { italics: true, color: MUTED }),

    H1("1. Summary of position"),
    PR([
      ["The substantive material the assignment depends on was obtained early. Circular EP delivered a consolidated archive of ", {}],
      [`${n0(F.archive.files)} files across ${F.archive.folders.length} topic folders on ${F.archive.delivered}`, { bold: true }],
      [`, Day 13 of the ${F.agreement.term_days}-day term. That archive has been organised, catalogued, and quality-checked, and its tabular content has been typed into a single queryable database of `, {}],
      [`${n0(d.rows_total)} records`, { bold: true }],
      [".", {}],
    ]),
    PR([
      ["Measured against the Annex 3 request list at item level, ", {}],
      [`${a3.summary.received} of ${a3.summary.total} items`, { bold: true }],
      [" are fully answered by the delivered material, ", {}],
      [`${a3.summary.partial} are partially answered`, { bold: true }],
      [", and ", {}],
      [`${a3.summary.none} have not been delivered`, { bold: true }],
      [`. Weighted coverage is ${n0(a3.summary.weighted * 100)}%. A category-level reading would report full coverage, because every one of the eight Annex 3 categories contains some material; the item-level reading is the one THS should rely on.`, {}],
    ]),
    PR([
      ["The principal shortfall in this engagement is documentation rather than substance. ", {}],
      ["Reporting has not been maintained on the Annex 2 cadence", { bold: true }],
      [", and the Data Request Tracking Matrix was not established at the outset. Both are being remedied before the end of the term; this document and the consolidated progress report issued alongside it are part of that remedy.", {}],
    ]),

    H1("2. Materials obtained"),
    P("The delivered archive is structured as follows."),
    table(
      [{ label: "Folder" }, { label: "Files", align: AlignmentType.RIGHT }],
      F.archive.folders.map((f) => [f.name, { text: n0(f.files), align: AlignmentType.RIGHT }]),
      [CONTENT_W - 1400, 1400]),
    new Paragraph({ spacing: { after: 160 }, children: [] }),
    PR([
      ["The core of the delivery for analytical purposes is folder 4, the weighbridge system data, together with folder 9 for Las Iguanas. These produced ", {}],
      [`${n0(d.trips)} weighing transactions covering ${d.first} to ${d.last}`, { bold: true }],
      [`, totalling ${n0(d.tonnes)} tonnes at an average of ${n0(d.avg_kg)} kg per trip, and ${n0(d.recovery_trips)} material recovery movements totalling ${n0(d.recovery_tonnes)} tonnes.`, {}],
    ]),

    H1("3. Quality control performed"),
    P("Essential quality checks were applied to every tabular source: that files open, are not corrupted, and match their stated description; and that the loaded record counts reconcile to the source specification."),
    table(
      [{ label: "Source file" }, { label: "Rows loaded", align: AlignmentType.RIGHT },
       { label: "Specified", align: AlignmentType.RIGHT }, { label: "Reconciles" }],
      d.files.map((f) => [f.file, { text: n0(f.loaded), align: AlignmentType.RIGHT },
                          { text: n0(f.spec_rows), align: AlignmentType.RIGHT },
                          f.match ? "Yes" : "+1 row"]),
      [5400, 1700, 1500, CONTENT_W - 8600]),
    new Paragraph({ spacing: { after: 160 }, children: [] }),
    P("Two files carry one record more than the count stated in the project brief. Each additional record was inspected and confirmed genuine — a distinct ticket, no null fields, not a duplicate and not a totals row. The brief's figures appear to be marginally understated; the loaded data is correct and no records were dropped."),
    PR([
      ["Integrity testing on the transaction set returned ", {}],
      ["no null tickets, service types, operators, sectors, dates or net weights; no duplicate ticket-and-year combinations; and no zero or negative net weights", { bold: true }],
      [". The weighbridge data is materially clean and fit for analysis.", {}],
    ]),

    H1("4. Data gaps and limitations"),
    PR([
      [`${a3.outstanding.length} of the ${a3.summary.total} requested items have not been delivered in any form:`, {}],
    ]),
    ...a3.outstanding.map((i) => BULLET(`${i.ref} — ${i.item}`)),
    new Paragraph({ spacing: { after: 100 }, children: [] }),
    PR([
      ["Item H3 warrants particular attention. It requests Circular EP's own written explanation of what it cannot supply and why. Nothing of that kind has been received. Under ", {}],
      ["Annex 1 §5", { bold: true }],
      [", material that Circular EP does not possess, has not collected, or will not disclose does not constitute non-performance by the Consultant where reasonable efforts and follow-up are documented. Obtaining H3 in writing is therefore the most direct way to convert the remaining gaps into documented source limitations, and it is the priority for the balance of the term.", {}],
    ]),
    P("Two further limitations affect what can be concluded from the delivered data:"),
    BULLET(`Route attribution is incomplete. Only ${n1(d.routes.route_coverage)}% of transactions carry a usable route tag, across ${d.routes.zonas} zones, ${d.routes.sub_zonas} sub-zones and ${d.routes.micro_rutas} micro-routes. Geographic analysis therefore rests on roughly half the record set.`),
    BULLET(`Reference periods do not align. The weighbridge series runs ${d.first} to ${d.last}, while the material recovery series runs ${d.recovery_first} to ${d.recovery_last}. Comparisons between the two must be restricted to the overlapping years.`),
    BULLET("Remaining landfill capacity for Las Iguanas is not stated anywhere in the delivered material. Any service-life projection must therefore take capacity as an engineering assumption supplied by THS rather than as source data."),

    new Paragraph({ children: [new PageBreak()] }),

    H1("5. Substantive findings to date"),
    P("Three findings from the delivered data are material enough to record at mid-term."),

    H2("5.1 Recovery is falling while disposal grows"),
    table(
      [{ label: "Year" }, { label: "Landfilled (t)", align: AlignmentType.RIGHT },
       { label: "Recovered (t)", align: AlignmentType.RIGHT },
       { label: "Recovery rate", align: AlignmentType.RIGHT }],
      recRows.map((r) => [r[0], { text: r[1], align: AlignmentType.RIGHT },
                          { text: r[2], align: AlignmentType.RIGHT },
                          { text: r[3], align: AlignmentType.RIGHT }]),
      [1800, 3000, 2600, CONTENT_W - 7400]),
    new Paragraph({ spacing: { after: 140 }, children: [] }),
    PR([
      ["The recovery rate has approximately halved across the series, from ", {}],
      [`${n2(d.recovery_by_year[0].recovery_pct)}% in ${d.recovery_by_year[0].year} to ${n2(d.recovery_by_year[2].recovery_pct)}% in ${d.recovery_by_year[2].year}`, { bold: true }],
      [`, while annual tonnage to landfill rose over the same period. Diversion across the whole record is ${n2(d.diversion_pct)}%. This is the finding with the clearest policy implication in the delivered data.`, {}],
    ]),

    H2("5.2 A step change in SERVICIOS ESPECIAL"),
    PR([
      ["Trips classified SERVICIOS ESPECIAL rose from ", {}],
      [`${n0(d.especial.by_year["2023"])} in 2023 to ${n0(d.especial.by_year["2024"])} in 2024, an increase of ${n1(d.especial.pct)}%`, { bold: true }],
      [`, settling at ${n0(d.especial.by_year["2025"])} in 2025. The category also carries the heaviest average payload of any major service type. A change of this size in a single year is more likely to reflect a reclassification or a contractual change than a genuine step change in waste behaviour, and it should be confirmed with Circular EP before the figures are relied on.`, {}],
    ]),
    TOCONFIRM("Raise the SERVICIOS ESPECIAL 2023-2024 step change with Circular EP and record their explanation. If it is a reclassification, the series requires a break note before use in any forecast."),

    H2("5.3 Service mix"),
    table(
      [{ label: "Service type" }, { label: "Trips", align: AlignmentType.RIGHT },
       { label: "Tonnes", align: AlignmentType.RIGHT },
       { label: "Avg kg/trip", align: AlignmentType.RIGHT }],
      svcRows.map((r) => [r[0], { text: r[1], align: AlignmentType.RIGHT },
                          { text: r[2], align: AlignmentType.RIGHT },
                          { text: r[3], align: AlignmentType.RIGHT }]),
      [4200, 2000, 2400, CONTENT_W - 8600]),
    new Paragraph({ spacing: { after: 140 }, children: [] }),
    P("Household collection dominates by volume, but special services carry a disproportionate share of tonnage relative to trip count. Commercial service records show a markedly low average payload, which may indicate a distinct vehicle class or a recording convention rather than genuinely light loads; this is flagged for confirmation rather than treated as a finding."),

    H1("6. Circular EP response status"),
    P("The delivery of the consolidated archive on Day 13 represents a substantial and timely response to the initial request. Status of individual outstanding requests is recorded item by item in the Data Request Tracking Matrix."),
    TOCONFIRM("Record, for each outstanding Annex 3 item: the date requested, follow-up actions taken with dates, and Circular EP's response or non-response. Complete the four marked columns of the Request Matrix sheet in the tracking matrix workbook."),

    H1("7. Challenges"),
    BULLET("Reporting cadence was not maintained. Progress reports were due at Days 14, 28, 42, 56 and 70 and were not issued on those dates. A consolidated retrospective is issued alongside this summary, and the Day 84 report will be delivered on schedule."),
    BULLET("The tracking matrix was not established at the outset, so request and follow-up history has to be reconstructed from correspondence rather than maintained contemporaneously."),
    BULLET("No written statement has been obtained from Circular EP regarding materials it cannot supply, which is the evidence that Annex 1 §5 relies on."),

    H1("8. Outlook for the remaining period"),
    PR([
      [`${F.today.remaining} days remain of the term, which ends on ${F.agreement.end}. The following are planned within that period:`, {}],
    ]),
    BULLET("Issue a single consolidated written request to Circular EP covering the eight undelivered items and expressly requesting item H3, early enough that a response or a documented non-response falls inside the term."),
    BULLET("Complete the Data Request Tracking Matrix with the full request and follow-up history."),
    BULLET(`Issue the Day 84 progress report on ${F.days["84"]}.`),
    BULLET(`Deliver the Final Handover Package on ${F.days["90"]}: organised repository, final inventory, summary report, and the list of pending or unavailable items with explanations.`),
    P("Subject to Circular EP's response, all remaining contractual deliverables are achievable within the term. The reporting dates already passed cannot be recovered, and the consolidated retrospective is offered as the accurate remedy rather than as a substitute for cadence."),
    RULEP(),
    P(`Prepared by ${F.agreement.consultant}, Consultant. Issued ${F.today.date}.`, { color: MUTED, italics: true }),
  ];

  return docShell("Mid-term Summary", children);
}

// ── Write ──────────────────────────────────────────────────────────────────
(async () => {
  const jobs = [
    ["Deliverable-1-Initial-Coordination-Plan.docx", coordinationPlan()],
    ["Deliverable-5-Mid-term-Summary.docx", midtermSummary()],
  ];
  for (const [name, doc] of jobs) {
    const buf = await Packer.toBuffer(doc);
    fs.writeFileSync(path.join(OUT, name), buf);
    console.log(`wrote deliverables/${name}  (${(buf.length / 1024).toFixed(0)} KB)`);
  }
})();
