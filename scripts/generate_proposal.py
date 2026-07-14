"""Generate the final AI4I Development-track proposal PDF for Veriq."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "VERIQ_AI4I_Proposal_Development.pdf"
SCREENSHOTS = ROOT / "outputs" / "judge-readiness-zimbabwe" / "browser"

NAVY = colors.HexColor("#10243D")
INK = colors.HexColor("#17243A")
MUTED = colors.HexColor("#60708A")
PURPLE = colors.HexColor("#6D4AFF")
LIGHT_PURPLE = colors.HexColor("#F0ECFF")
PALE = colors.HexColor("#F7F9FC")
LINE = colors.HexColor("#DDE5F0")
GREEN = colors.HexColor("#16875F")
AMBER = colors.HexColor("#B8750F")
RED = colors.HexColor("#C94F49")


def register_fonts() -> None:
    fonts = Path("C:/Windows/Fonts")
    pdfmetrics.registerFont(TTFont("Arial", str(fonts / "arial.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Bold", str(fonts / "arialbd.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Italic", str(fonts / "ariali.ttf")))


register_fonts()
styles = getSampleStyleSheet()
BODY = ParagraphStyle(
    "Body",
    parent=styles["BodyText"],
    fontName="Arial",
    fontSize=11,
    leading=12.65,
    textColor=INK,
    spaceAfter=6,
)
SMALL = ParagraphStyle(
    "Small",
    parent=BODY,
    fontSize=8.5,
    leading=10.2,
    textColor=MUTED,
    spaceAfter=3,
)
CAPTION = ParagraphStyle(
    "Caption",
    parent=SMALL,
    fontName="Arial-Italic",
    fontSize=8,
    leading=9.5,
    alignment=TA_CENTER,
    spaceBefore=3,
)
H1 = ParagraphStyle(
    "H1",
    parent=BODY,
    fontName="Arial-Bold",
    fontSize=22,
    leading=25,
    textColor=NAVY,
    spaceBefore=2,
    spaceAfter=9,
)
H2 = ParagraphStyle(
    "H2",
    parent=BODY,
    fontName="Arial-Bold",
    fontSize=13.5,
    leading=16,
    textColor=NAVY,
    spaceBefore=5,
    spaceAfter=4,
)
LABEL = ParagraphStyle(
    "Label",
    parent=SMALL,
    fontName="Arial-Bold",
    fontSize=7.6,
    leading=9,
    textColor=PURPLE,
    spaceAfter=4,
)
STAT = ParagraphStyle(
    "Stat",
    parent=BODY,
    fontName="Arial-Bold",
    fontSize=17,
    leading=19,
    textColor=NAVY,
    alignment=TA_CENTER,
    spaceAfter=2,
)
CENTER = ParagraphStyle("Center", parent=BODY, alignment=TA_CENTER)


def P(text: str, style: ParagraphStyle = BODY) -> Paragraph:
    return Paragraph(text, style)


def bullets(items: list[str], compact: bool = False) -> list[Paragraph]:
    style = ParagraphStyle(
        "BulletCompact" if compact else "Bullet",
        parent=SMALL if compact else BODY,
        leftIndent=14,
        firstLineIndent=-8,
        bulletIndent=0,
        spaceAfter=2 if compact else 4,
    )
    return [Paragraph(item, style, bulletText="-") for item in items]


def screenshot(name: str, width: float = 6.2 * inch) -> Table:
    path = SCREENSHOTS / name
    image = ImageReader(str(path))
    source_width, source_height = image.getSize()
    height = width * source_height / source_width
    picture = Image(str(path), width=width, height=height)
    frame = Table([[picture]], colWidths=[width + 8], rowHeights=[height + 8])
    frame.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("BOX", (0, 0), (-1, -1), 0.7, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return frame


def info_box(title: str, text: str, color: colors.Color = PURPLE) -> Table:
    table = Table(
        [[P(title.upper(), LABEL), P(text, SMALL)]],
        colWidths=[1.25 * inch, 4.75 * inch],
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PALE),
                ("LINEBEFORE", (0, 0), (0, 0), 3, color),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return table


def stat_row(stats: list[tuple[str, str]]) -> Table:
    cells = [[P(value, STAT) for value, _ in stats], [P(label, CAPTION) for _, label in stats]]
    table = Table(cells, colWidths=[6.15 * inch / len(stats)] * len(stats))
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PALE),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE),
                ("TOPPADDING", (0, 0), (-1, 0), 8),
                ("BOTTOMPADDING", (0, 1), (-1, 1), 7),
            ]
        )
    )
    return table


def evidence_table(headers: list[str], rows: list[list[str]], widths: list[float]) -> Table:
    data = [[P(value, ParagraphStyle("TH", parent=SMALL, fontName="Arial-Bold", textColor=colors.white)) for value in headers]]
    data.extend([[P(value, SMALL) for value in row] for row in rows])
    table = Table(data, colWidths=widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("GRID", (0, 0), (-1, -1), 0.5, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
            ]
        )
    )
    return table


def page_header_footer(canvas, doc) -> None:
    page = canvas.getPageNumber()
    width, height = A4
    canvas.saveState()
    if page == 1:
        canvas.setFillColor(NAVY)
        canvas.rect(0, 0, 0.68 * inch, height, fill=1, stroke=0)
        canvas.setFillColor(PURPLE)
        canvas.circle(width - 0.62 * inch, height - 0.65 * inch, 0.72 * inch, fill=1, stroke=0)
        canvas.setFillColor(LIGHT_PURPLE)
        canvas.circle(width - 0.62 * inch, height - 0.65 * inch, 0.36 * inch, fill=1, stroke=0)
        canvas.restoreState()
        return
    canvas.setStrokeColor(LINE)
    canvas.line(inch, height - 0.62 * inch, width - inch, height - 0.62 * inch)
    canvas.setFont("Helvetica-Bold", 7.5)
    canvas.setFillColor(PURPLE)
    if 2 <= page <= 10:
        canvas.drawString(inch, height - 0.48 * inch, "VERIQ | AI FOR IMPACT | DEVELOPMENT TRACK")
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(width - inch, 0.48 * inch, f"Main proposal {page - 1} of 9")
    else:
        canvas.drawString(inch, height - 0.48 * inch, "VERIQ | TECHNICAL APPENDIX")
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(width - inch, 0.48 * inch, f"Appendix A{page - 10}")
    canvas.setStrokeColor(LINE)
    canvas.line(inch, 0.62 * inch, width - inch, 0.62 * inch)
    canvas.restoreState()


def cover() -> list:
    return [
        Spacer(1, 0.8 * inch),
        P("AI FOR IMPACT - TRACK 3: DEVELOPMENT", LABEL),
        P("VERIQ", ParagraphStyle("CoverTitle", parent=H1, fontSize=35, leading=38, textColor=NAVY, spaceAfter=8)),
        P("Evidence-grounded AI for earlier school intervention", ParagraphStyle("CoverSub", parent=BODY, fontSize=18, leading=22, textColor=PURPLE, spaceAfter=20)),
        info_box("Project ID", "VERIQ", PURPLE),
        Spacer(1, 0.22 * inch),
        P("DEVELOPMENT-TRACK PROPOSAL", LABEL),
        P("A functional decision-support MVP that connects attendance, behaviour, and internal-assessment evidence; explains verified patterns with Beacon AI; and converts insight into accountable human action.", ParagraphStyle("CoverBody", parent=BODY, fontSize=12, leading=15, spaceAfter=20)),
        Spacer(1, 0.1 * inch),
        evidence_table(
            ["Submission detail", "Confirmed information"],
            [
                ["Team", "Veriq"],
                ["Lead Innovator", "Praisegod Chaparika"],
                ["Supporting Team", "Innocent Chaparika - Product Design"],
                ["Contact", "praisegodchaps@gmail.com"],
                ["Submission date", "14 July 2026"],
                ["Repository", "github.com/tech2creative22/veriq"],
            ],
            [1.55 * inch, 4.45 * inch],
        ),
        Spacer(1, 0.25 * inch),
        P("CHALLENGE EVALUATION SUBMISSION", ParagraphStyle("CoverFoot", parent=LABEL, alignment=TA_LEFT)),
        P("Current boundary: synthetic demonstration data only. Beacon recommends; authorised school leadership decides.", SMALL),
    ]


def main_page_1() -> list:
    return [
        P("01 / PROBLEM DEFINITION AND STRATEGIC ALIGNMENT", LABEL),
        P("School evidence exists. Timely, connected interpretation is the gap.", H1),
        P("Zimbabwean secondary-school leaders routinely work with attendance, behaviour, and internal-assessment records. The operational challenge is that these signals can be reviewed separately, by different owners, and after a learner or class problem has become visible. A declining pattern may therefore be treated as an isolated absence, incident, or mark instead of one connected need for support."),
        info_box("Problem statement", "School leaders need a fast, traceable way to identify emerging multi-signal patterns, understand the evidence behind them, and assign a proportionate human response before the pattern becomes urgent.", RED),
        P("Primary users", H2),
        *bullets([
            "Headmasters and deputy heads who need a whole-school health view and accountable actions.",
            "Heads of department who need class and subject context before the next internal assessment.",
            "Authorised student-support staff who monitor individual learner patterns and intervention follow-up.",
        ]),
        P("Zimbabwe education fit", H2),
        P("The demonstration dataset follows a Zimbabwe secondary-school context with Forms 1-4 and internal continuous assessment. Veriq does not calculate or claim an official ZIMSEC pass rate or final examination outcome. It identifies current evidence that leadership can verify and act on."),
        P("Strategic alignment", H2),
        evidence_table(
            ["Development-track expectation", "Veriq response"],
            [
                ["Working AI-enabled product", "Connected production MVP from CSV validation to evidence, Beacon explanation, and Decision Brief."],
                ["Responsible local relevance", "Zimbabwe secondary-school workflow, synthetic judge data, human review, and explicit pre-pilot controls."],
                ["Feasible deployment", "Pinned Next.js/FastAPI stack, SQLite demonstration persistence, and two-container CCE package."],
                ["Measurable evidence", "29 backend tests, 23 AI-control checks, 35 browser checks, deterministic dataset validation."],
            ],
            [2.0 * inch, 4.0 * inch],
        ),
        Spacer(1, 5),
        P("Success means an authorised leader can move from a current school signal to the correct class or learner evidence, ask a grounded question, and record a reviewed action without losing source context.", SMALL),
    ]


def main_page_2() -> list:
    return [
        P("02 / USER INTERACTION AND VALUE", LABEL),
        P("One evidence package, visible from school health to every learner.", H1),
        screenshot("school-pulse-connected.png", 6.15 * inch),
        P("Figure 1. School Pulse summarises the latest persisted CSV upload, reporting coverage, analysis ID, school metrics, every class, and monitored learner distribution.", CAPTION),
        P("Judge workflow", H2),
        evidence_table(
            ["Step", "User action", "Product response"],
            [
                ["1", "Acknowledge synthetic use and upload three CSVs.", "Validate, store, and create one traceable Evidence Package."],
                ["2", "Review School Pulse.", "Show whole-school health, class comparisons, source, coverage, and confidence."],
                ["3", "Open Early Intervention.", "Monitor high-attention, watch, stable, and improving learner patterns."],
                ["4", "Ask Beacon.", "Resolve school, metric, class, or learner scope and explain only verified evidence."],
                ["5", "Create a Decision Brief.", "Record recommendation, owner, target, due date, and human-review status."],
            ],
            [0.45 * inch, 2.25 * inch, 3.3 * inch],
        ),
    ]


def main_page_3() -> list:
    return [
        P("03 / TECHNICAL DESIGN - AS BUILT", LABEL),
        P("Deterministic evidence first. Generative explanation second.", H1),
        screenshot("upload-complete.png", 5.75 * inch),
        P("Figure 2. The upload workflow validates all three fictional files and records the shared analysis used across every workspace.", CAPTION),
        P("Implemented architecture", H2),
        evidence_table(
            ["Layer", "Implemented component", "Responsibility"],
            [
                ["Experience", "Next.js 15.5.20 / React 18", "Six judge-facing workspaces and typed API client."],
                ["API", "FastAPI 0.115.6", "Contracts, validation, scope resolution, AI orchestration, and human-owned decisions."],
                ["Evidence", "Deterministic Python services", "Calculate attendance, incidents, assessment changes, severity, confidence, and trace IDs."],
                ["Persistence", "SQLite", "Store raw imports, normalised rows, snapshots, conversations, workspace, and decisions."],
                ["AI", "Gemini 3.5 Flash via google-genai", "Explain bounded evidence and draft proportionate recommendations."],
            ],
            [1.0 * inch, 1.7 * inch, 3.3 * inch],
        ),
        Spacer(1, 4),
        info_box("Data path", "Browser -> FastAPI -> schema/domain validation -> canonical records -> deterministic Evidence Package -> scoped Gemini explanation -> verified facts reattached -> human review.", PURPLE),
    ]


def main_page_4() -> list:
    return [
        P("04 / AI PRODUCT LOGIC", LABEL),
        P("Beacon makes verified evidence easier to understand, not easier to invent.", H1),
        screenshot("beacon-greeting.png", 6.05 * inch),
        P("Figure 3. Beacon retains the selected evidence scope, handles conversation naturally, shows confidence and trace context, and connects explanation to a scoped Decision Brief.", CAPTION),
        P("Why AI is justified", H2),
        P("A rule-only dashboard can show alerts, but it cannot efficiently answer varied natural-language follow-ups, synthesise multiple verified signals for different roles, explain why a pattern matters, or translate evidence into an editable action narrative. Gemini adds that language and synthesis layer while all values remain deterministic."),
        evidence_table(
            ["Ordinary software owns", "Gemini owns", "Safety boundary"],
            [
                ["Schema checks, calculations, severity, confidence, IDs, persistence.", "Scoped explanation, educational relevance, allowed recommendation category, conversational follow-up.", "Unknown learners clarify; stale analysis rejects; unsupported numbers are not exposed; provider failure is explicit."],
            ],
            [2.0 * inch, 2.0 * inch, 2.0 * inch],
        ),
    ]


def main_page_5() -> list:
    return [
        P("05 / EARLY INTERVENTION AND PRODUCT LOGIC", LABEL),
        P("Monitoring includes concern, watch, stability, and improvement.", H1),
        screenshot("early-intervention.png", 6.1 * inch),
        P("Figure 4. Early Intervention presents continuous learner monitoring from the same persisted evidence, with visible high-attention, watch, stable, and improving distributions.", CAPTION),
        P("How patterns become action", H2),
        evidence_table(
            ["Pattern state", "Evidence interpretation", "Permitted next move"],
            [
                ["High attention", "Two or more connected risk factors require prompt verification.", "Investigate with Beacon and convene an authorised support review."],
                ["Watch", "One emerging signal needs monitoring, not a crisis label.", "Verify source quality and review the next evidence period."],
                ["Stable / improving", "No connected deterioration; positive movement remains visible.", "Continue monitoring and learn from support that appears effective."],
            ],
            [1.2 * inch, 2.55 * inch, 2.25 * inch],
        ),
        Spacer(1, 4),
        P("The MVP intentionally avoids a single risk template. Each learner scope replaces class facts with that learner's own connected records before Beacon receives context.", SMALL),
    ]


def main_page_6() -> list:
    return [
        P("06 / DELIVERABLES, DATA, AND VERIFICATION", LABEL),
        P("The MVP is functional, reproducible, and backed by review evidence.", H1),
        stat_row([("20", "fictional learners"), ("834", "validated records"), ("4", "Forms/classes"), ("0", "production npm vulnerabilities")]),
        Spacer(1, 8),
        P("Synthetic validation dataset", H2),
        P("The deterministic judge dataset contains 400 attendance rows, 34 behaviour incidents, and 400 internal-assessment rows. It encodes three connected high-attention cases, two single-signal watch cases, and fifteen stable controls. A portable SHA-256 manifest and generator reproduce the committed CSVs byte for byte."),
        evidence_table(
            ["Delivered evidence", "Verified result", "Repository location"],
            [
                ["Backend tests", "29/29 pass", "backend/tests/"],
                ["AI grounding/control suite", "23/23 pass", "submission/ai/BEACON_TEST_RESULTS.json"],
                ["Visible browser release flow", "35/35 pass; no console, network, page, encoding, or mobile-overflow failure", "outputs/judge-readiness-zimbabwe/browser/"],
                ["Dataset validation", "Expected labels, domain constraints, keys, hashes, and production evidence path pass", "submission/dataset/"],
                ["Build and security", "Lint, typecheck, standalone build, route smoke, and production dependency audit pass", "submission/SECURITY_BASELINE.md"],
            ],
            [1.35 * inch, 2.6 * inch, 2.05 * inch],
        ),
        P("What the evidence does not yet prove", H2),
        *bullets([
            "The 23 control checks prove grounding and scope behaviour, not educator satisfaction or universal semantic quality.",
            "A fixed 10-question live Gemini protocol must still be run three times and scored before final release.",
            "No real learner pilot, official examination prediction, customer traction, or production security authorisation is claimed.",
        ], compact=True),
    ]


def main_page_7() -> list:
    return [
        P("07 / CCE IMPLEMENTATION ROADMAP", LABEL),
        P("A two-container deployment package is ready for CCE verification.", H1),
        info_box("Deployment unit", "Non-root Next.js standalone frontend on port 3000; non-root FastAPI backend on port 8000; persistent /data volume for SQLite; Gemini key held only by the backend.", GREEN),
        P("Initial demonstration budget", H2),
        evidence_table(
            ["Component", "CPU / memory", "Storage and role"],
            [
                ["Frontend", "0.5 vCPU / 512 MB", "Stateless standalone UI"],
                ["Backend", "1.0 vCPU / 768 MB", "2 GB initial persistent volume; one Uvicorn worker"],
                ["Recommended host", "2 vCPU / 4 GB", "10 GB disk including images, logs, backups, and headroom"],
            ],
            [1.45 * inch, 1.55 * inch, 3.0 * inch],
        ),
        P("CCE delivery phases", H2),
        evidence_table(
            ["Phase", "Work", "Acceptance evidence"],
            [
                ["1. Access", "Confirm account, quota, DNS, ingress, registry, egress, secret, and backup mechanisms.", "Named owner and environment checklist."],
                ["2. Build", "Build pinned images, scan dependencies/images, record digests.", "No unresolved high/critical findings; package inventory."],
                ["3. Synthetic deploy", "Configure HTTPS origins, volume, Gemini secret, and included judge data.", "Healthy containers, smoke result, and screenshots."],
                ["4. Resilience", "Restart, persist evidence, back up/restore, simulate Gemini failure.", "Recovery log and deterministic views remain available."],
                ["5. Performance", "Exercise agreed concurrent demo load; record p95 latency, CPU, RAM, and storage.", "Measured sizing update."],
                ["6. Release", "Pin digests, freeze config, rerun audit/tests, rehearse demo and rollback.", "Release record and backup video."],
            ],
            [0.75 * inch, 2.85 * inch, 2.4 * inch],
        ),
        Spacer(1, 5),
        P("Current external gate: Docker is not installed on the development workstation. Container build/start must be verified on a Docker-capable runner or allocated CCE before claiming deployment success.", SMALL),
    ]


def main_page_8() -> list:
    return [
        P("08 / COMPLIANCE AND RISK MITIGATION", LABEL),
        P("Synthetic-only today. Controlled, human-reviewed pilot before real data.", H1),
        info_box("Current boundary", "The UI and API require authorised synthetic demonstration use. This acknowledgement is not consent and does not establish a lawful basis. Real learner data remains prohibited.", RED),
        P("Zimbabwe compliance context", H2),
        P("The pre-pilot review must address the Cyber and Data Protection Act [Chapter 12:07], POTRAZ's role as Data Protection Authority, and SI 155 of 2024 on controller licensing and Data Protection Officers. The participating authority must confirm controller/processor roles, lawful basis, notices, data-subprocessor terms, and child/representative rights. [1][2]"),
        evidence_table(
            ["Material risk", "Current MVP control", "Mandatory pilot gate"],
            [
                ["Unauthorised learner data", "Synthetic notice plus frontend/API acknowledgement.", "Written lawful basis, controller approval, DPA, notice, and POTRAZ determination."],
                ["Disclosure or cross-tenant access", "Secrets and databases excluded from Git; local single workspace.", "Identity, MFA/admin controls, RBAC, tenant isolation, TLS, encrypted storage/backups, audit logs."],
                ["Hallucination or wrong scope", "Deterministic values, scoped Evidence Package, stale/unknown checks, verified facts reattached.", "30-response live evaluation, adversarial tests, monitoring, and evidence-link UX."],
                ["AI over-reliance", "Advisory language and human-owned Decision Brief.", "Training, review checklist, escalation, correction/appeal route, no solely automated significant decision."],
                ["Poor source data", "Schema, domain, date, score, and shared-class validation.", "Completeness dashboard, reconciliation, authoritative ID mapping, and data-steward sign-off."],
            ],
            [1.4 * inch, 2.2 * inch, 2.4 * inch],
        ),
        P("Go/no-go controls", H2),
        *bullets([
            "Complete a Data Protection Impact Assessment covering children's data and Gemini/cross-border processing.",
            "Deploy and test authentication, authorisation, tenant isolation, encryption, retention/deletion, incident response, audit, backup, and restore.",
            "Name the data-protection and security owners; close every high-severity or pilot-blocking risk before collection.",
        ], compact=True),
        P("This section is an engineering compliance plan, not legal advice; Zimbabwe-qualified legal review is required.", SMALL),
    ]


def main_page_9() -> list:
    return [
        P("09 / SUSTAINABILITY AND FUTURE ADOPTION", LABEL),
        P("Start narrow, prove value, then scale governance and infrastructure.", H1),
        P("The expected customer is a secondary school, responsible authority, school group, or education programme. Day-to-day users are heads, deputies, heads of department, and authorised support staff. The commercial hypothesis is recurring access to an evidence-to-action workflow, not chatbot novelty."),
        evidence_table(
            ["Offer", "Planning price", "Scope"],
            [
                ["Challenge demonstration", "USD 0", "Synthetic judge dataset; no real learner data or service commitment."],
                ["90-day validation pilot", "USD 100/school or sponsor-funded", "One controlled school after legal/security gates, with agreed measures."],
                ["School Core hypothesis", "USD 300/school/year", "Single school, up to five leaders, and 500 Beacon interactions/month planning allowance."],
            ],
            [1.65 * inch, 1.35 * inch, 3.0 * inch],
        ),
        P("Unit economics assumption", H2),
        P("At the reviewed Gemini 3.5 Flash rates, a planning interaction of 2,000 input and 500 output/thinking tokens costs about USD 0.0075. At 500 interactions/month, planned model cost is USD 45/school/year. With shared hosting, monitoring, and eight support hours, estimated allocated annual cost is USD 173, leaving USD 127 contribution at the proposed USD 300 price. Pricing can change and must be refreshed. [3]"),
        stat_row([("$0.0075", "planned AI interaction"), ("$2,440", "known 12-month cash envelope"), ("1-3", "controlled validation schools"), ("8-12", "pilot weeks")]),
        Spacer(1, 8),
        P("Adoption roadmap", H2),
        evidence_table(
            ["Stage", "Decision evidence"],
            [
                ["1. Synthetic demonstration", "Judges and educators complete the fixed workflow without personal data."],
                ["2. Discovery", "Interview 5-10 leaders on data, review effort, trust, ownership, and willingness to pay."],
                ["3. Controlled validation", "Measure data quality, timed interpretation, action ownership, trust, and zero unsupported numeric claims."],
                ["4. Paid school release", "Proceed only if value, support burden, compliance cost, and renewal case are evidenced."],
                ["5. Group expansion", "Add managed database, tenancy, integrations, central governance, and measured capacity first."],
            ],
            [1.55 * inch, 4.45 * inch],
        ),
        Spacer(1, 6),
        info_box("Development-track ask", "Support CCE verification, educator validation, and a governed 1-3 school pilot so Veriq can prove that earlier connected interpretation leads to better-owned school action.", PURPLE),
    ]


def appendix_1() -> list:
    return [
        P("APPENDIX A1 / EVIDENCE INDEX", LABEL),
        P("Reproducible technical evidence", H1),
        P("Repository: <link href='https://github.com/tech2creative22/veriq'>https://github.com/tech2creative22/veriq</link>"),
        evidence_table(
            ["Evidence", "Location / command"],
            [
                ["As-built architecture", "docs/AS_BUILT_ARCHITECTURE.md"],
                ["API and environment", "docs/API_REFERENCE.md; docs/ENVIRONMENT_AND_CONFIGURATION.md"],
                ["Security and threat model", "submission/SECURITY_BASELINE.md; docs/THREAT_MODEL.md"],
                ["Dataset provenance and hashes", "submission/dataset/; demo-data/zimbabwe-secondary-judge/dataset_manifest.json"],
                ["AI rationale, model card, controls", "submission/ai/"],
                ["Compliance and risk register", "submission/compliance/"],
                ["CCE deployment and operations", "deployment/; Dockerfile; backend/Dockerfile; docker-compose.yml"],
                ["Business, pricing, assets", "submission/business/"],
                ["Release report and screenshots", "submission/TEST_AND_RELEASE_REPORT.md; outputs/judge-readiness-zimbabwe/browser/"],
            ],
            [2.1 * inch, 3.9 * inch],
        ),
        P("Verification commands", H2),
        P("npm ci<br/>npm run lint<br/>npm run typecheck<br/>npm run build<br/>npm audit --omit=dev --audit-level=high --package-lock-only<br/>cd backend; python -m unittest discover -s tests -v<br/>python scripts/run_ai_evaluation.py<br/>python scripts/validate_judge_dataset.py<br/>python scripts/smoke_test.py", ParagraphStyle("Code", parent=SMALL, fontName="Courier", fontSize=8.3, leading=10.2, backColor=PALE, borderPadding=8)),
        P("Licence", H2),
        P("The repository uses a protected Challenge Evaluation Licence. Authorised challenge reviewers may access, run, and internally reproduce Veriq for evaluation. No general modification, redistribution, commercialisation, or derivative-product rights are granted."),
    ]


def appendix_2() -> list:
    return [
        P("APPENDIX A2 / SOURCES AND LIMITATIONS", LABEL),
        P("Authoritative references", H1),
        evidence_table(
            ["Ref", "Source"],
            [
                ["[1]", "Zimbabwe Cyber and Data Protection Act [Chapter 12:07], ZimLII: https://zimlii.org/akn/zw/act/2021/5/eng%402022-03-11"],
                ["[2]", "POTRAZ, SI 155 of 2024: https://www.potraz.gov.zw/wp-content/uploads/2025/02/sI-155-of-2024-Cyber-and-Data-Protection-Normal_240913_1250178.pdf"],
                ["[3]", "Google Gemini API pricing: https://ai.google.dev/gemini-api/docs/pricing (reviewed 14 July 2026; refresh before deployment)"],
                ["[4]", "ZIMSEC examinations administration and O-Level materials: https://www5.zimsec.co.zw/examinations-administration/"],
                ["[5]", "AI4I Terms of Reference - Track 3 Development, supplied challenge document."],
            ],
            [0.55 * inch, 5.45 * inch],
        ),
        P("Material limitations", H2),
        *bullets([
            "The dataset is fictional and synthetic; it is not representative evidence from a school population.",
            "First names and learner IDs are fabricated for demonstration and do not correspond to real people.",
            "Assessment values are internal continuous-assessment indicators, not official ZIMSEC predictions or results.",
            "SQLite and a single worker suit a demonstration, not a multi-school production system.",
            "Authentication, role-based access, tenant isolation, encryption-at-rest controls, rights-request tooling, and automated retention are pre-pilot requirements, not implemented claims.",
            "The deterministic control suite does not replace live model evaluation or educator usability research.",
            "Pricing, support effort, school willingness to pay, CCE costs, and legal/security costs are planning assumptions requiring quotations and validation.",
            "No hosted HTTPS demo or Docker/CCE execution evidence is claimed in this proposal version.",
        ]),
        P("Submission contact", H2),
        P("Praisegod Chaparika - Lead Innovator<br/>Veriq<br/>praisegodchaps@gmail.com"),
    ]


def appendix_3() -> list:
    return [
        P("APPENDIX A3 / RESPONSIVE PRODUCT EVIDENCE", LABEL),
        P("School Pulse remains legible on a narrow viewport.", H1),
        Table(
            [[screenshot("school-pulse-mobile.png", 2.15 * inch), P("The 390 px release check confirmed no horizontal document overflow. The mobile view retains source, reporting period, coverage, analysis identity, School Pulse status, and Beacon confidence.<br/><br/><b>Why this matters:</b> school leaders may review urgent evidence away from a desktop. The MVP does not claim offline support, but responsive access reduces device dependence.<br/><br/><b>Release evidence:</b> the same visible-browser run validated all six routes, a real synthetic import, connected School Pulse coverage, Beacon greeting behaviour, and zero network, console, page, or encoding errors.", BODY)]],
            colWidths=[2.3 * inch, 3.7 * inch],
            style=TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6)]),
        ),
        Spacer(1, 8),
        info_box("Submission package", "The main proposal uses four visually verified product screenshots: School Pulse, Upload, Beacon, and Early Intervention. Full-resolution PNGs and the browser result JSON are included in the repository.", PURPLE),
    ]


def build() -> Path:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    page_width, page_height = A4
    frame = Frame(
        inch,
        inch,
        page_width - 2 * inch,
        page_height - 2 * inch,
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )
    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=inch,
        rightMargin=inch,
        topMargin=inch,
        bottomMargin=inch,
        title="Veriq AI4I Proposal - Development Track",
        author="Praisegod Chaparika and Veriq",
        subject="AI for Impact Development-track proposal",
    )
    doc.addPageTemplates([PageTemplate(id="Proposal", frames=[frame], onPage=page_header_footer)])
    sections = [
        cover(),
        main_page_1(),
        main_page_2(),
        main_page_3(),
        main_page_4(),
        main_page_5(),
        main_page_6(),
        main_page_7(),
        main_page_8(),
        main_page_9(),
        appendix_1(),
        appendix_2(),
        appendix_3(),
    ]
    story: list = []
    for index, section in enumerate(sections):
        story.extend(section)
        if index < len(sections) - 1:
            story.append(PageBreak())
    doc.build(story)
    return OUTPUT


if __name__ == "__main__":
    print(build())
