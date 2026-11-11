"""
Shared utilities for all CASS Intelligence Report generators.
Import this in every report tool to avoid boilerplate repetition.
"""

import json
import sys
from datetime import date
from pathlib import Path
from docx import Document
from docx.shared import RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BASE_DIR = Path(__file__).parent.parent
TMP_DIR = BASE_DIR / ".tmp"
TMP_DIR.mkdir(exist_ok=True)
sys.path.insert(0, str(Path(__file__).parent))

# ── Shared observability / PII / GDPR ─────────────────────────────────────────
_SHARED = Path(__file__).parent.parent.parent / "shared"
sys.path.insert(0, str(_SHARED))
from observability import get_logger, metrics, trace_op, set_request_id
from pii_guard import redact, redact_dict, PIIAuditLog, audit_pii_access
from gdpr import retention, consent, erasure

_log = get_logger("cass.report_base", log_file=BASE_DIR / ".tmp" / "cass.log")
_pii_audit = PIIAuditLog(log_path=BASE_DIR / ".tmp" / "pii_audit.jsonl")

WHITE = RGBColor(0xFF, 0xFF, 0xFF)
HEADER_HEX = "1F4E79"
RAG_BG = {"GREEN": "00B050", "AMBER": "FFC000", "RED": "FF0000", "BLUE": "2E75B6"}
PRIORITY_MAP = {"RED": "IMMEDIATE", "AMBER": "HIGH"}


def set_cell_bg(cell, hex_color: str):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


def header_cell(cell, text: str):
    cell.text = text
    if cell.paragraphs[0].runs:
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = WHITE
    set_cell_bg(cell, HEADER_HEX)


def rag_cell(cell, status: str):
    cell.text = status
    if cell.paragraphs[0].runs:
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = WHITE
    set_cell_bg(cell, RAG_BG.get(status, "888888"))


def rag_counts(findings: list) -> dict:
    counts = {"RED": 0, "AMBER": 0, "GREEN": 0}
    for f in findings:
        counts[f["status"]] = counts.get(f["status"], 0) + 1
    return counts


def _coerce(v):
    """Convert string form values to proper Python types."""
    if isinstance(v, str):
        lv = v.strip().lower()
        if lv == "true":  return True
        if lv == "false": return False
        if lv == "":      return v
        try:    return int(v)
        except ValueError: pass
        try:    return float(v)
        except ValueError: pass
    if isinstance(v, dict):  return {k2: _coerce(v2) for k2, v2 in v.items()}
    if isinstance(v, list):  return [_coerce(i) for i in v]
    return v


def load_client_data(report_prefix: str, client_name: str) -> dict:
    path = TMP_DIR / f"{report_prefix}_{client_name}_input.json"
    if not path.exists():
        raise FileNotFoundError(
            f"Input file not found: {path}\n"
            "Create it with client data before running this tool."
        )
    with open(path) as f:
        raw = json.load(f)
    return {k: _coerce(v) for k, v in raw.items()}


def run_perplexity_scan(report_type: str, region: str = None, country: str = None) -> dict:
    """
    Run live web intelligence scan via Perplexity. Pass region/country to route
    the scan topics to official regulatory websites for that jurisdiction.
    """
    try:
        from perplexity_scan import build_regulatory_context
        region_label = f" [{country or region}]" if (country or region) else ""
        print(f"Running Routing Intelligence Scan{region_label}...")
        return build_regulatory_context(report_type, region=region, country=country)
    except EnvironmentError as e:
        print(f"Routing Intelligence Scan unavailable — {e}")
    except Exception as e:
        print(f"Routing Intelligence Scan encountered an error, continuing — {e}")
    return {}


@trace_op("start_document")
def start_document(title: str, data: dict, client_name: str) -> Document:
    # Record PII access for audit trail
    from pii_guard import PII_FIELDS, subject_hash as _shash
    _pii_fields_present = [k for k in (data or {}) if k.lower() in PII_FIELDS]
    _identifier = str(
        data.get("firm_name") or data.get("name") or
        data.get("client_name") or data.get("email") or "unknown"
    )
    try:
        from observability import get_request_id as _get_rid
        _rid = _get_rid()
    except Exception:
        _rid = "-"
    _pii_audit.record(
        event="pii_access",
        subject_hash=_shash(_identifier),
        accessor="cass.report_base.start_document",
        fields=_pii_fields_present,
        purpose="report_generation",
        request_id=_rid,
    )
    doc = Document()
    h = doc.add_heading(title, level=0)
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph(
        f"Prepared for: {data.get('firm_name', client_name)}\n"
        f"{reg_id_label(data)}: {data.get('frn', 'N/A')}\n"
        f"Report Date: {date.today().strftime('%d %B %Y')}\n"
        f"Prepared by: CASS Intelligence Reports"
    )
    p = doc.add_paragraph(
        "CONFIDENTIAL — This report is for the exclusive use of the named firm. "
        "It does not constitute legal or regulatory advice."
    )
    p.runs[0].font.italic = True
    return doc


def add_firm_profile(doc: Document, data: dict, client_name: str, extra_rows: list = None):
    doc.add_heading("1. Firm Profile", level=1)
    rows = [
        ("Firm Name", data.get("firm_name", client_name)),
        (reg_id_label(data), data.get("frn", "N/A")),
        ("Assessment Date", date.today().strftime("%d %B %Y")),
        ("Assessment Period", data.get("assessment_period", "Last 12 months")),
    ]
    if extra_rows:
        rows += extra_rows
    tbl = doc.add_table(rows=len(rows), cols=2)
    tbl.style = "Table Grid"
    for i, (label, value) in enumerate(rows):
        tbl.rows[i].cells[0].text = label
        tbl.rows[i].cells[1].text = str(value)
        if tbl.rows[i].cells[0].paragraphs[0].runs:
            tbl.rows[i].cells[0].paragraphs[0].runs[0].font.bold = True


def add_findings_table(doc: Document, findings: list, heading: str, section_num: int):
    doc.add_heading(f"{section_num}. {heading}", level=1)
    tbl = doc.add_table(rows=1 + len(findings), cols=4)
    tbl.style = "Table Grid"
    for j, h in enumerate(["Rule / Ref", "Control Area", "Status", "Commentary"]):
        header_cell(tbl.rows[0].cells[j], h)
    for i, f in enumerate(findings):
        row = tbl.rows[i + 1]
        row.cells[0].text = f.get("rule", "")
        row.cells[1].text = f.get("description", "")
        rag_cell(row.cells[2], f["status"])
        row.cells[3].text = f.get("commentary", "")


def add_summary_table(doc: Document, findings: list, section_num: int):
    doc.add_heading(f"{section_num}. Findings Summary", level=1)
    counts = rag_counts(findings)
    doc.add_paragraph(
        f"Total checks: {len(findings)}   |   "
        f"{counts['GREEN']} PASS   |   "
        f"{counts['AMBER']} REQUIRES ATTENTION   |   "
        f"{counts['RED']} FAIL"
    )
    tbl = doc.add_table(rows=1 + len(findings), cols=4)
    tbl.style = "Table Grid"
    for j, h in enumerate(["Area", "Rule", "Status", "Description"]):
        header_cell(tbl.rows[0].cells[j], h)
    for i, f in enumerate(findings):
        row = tbl.rows[i + 1]
        row.cells[0].text = f.get("area", "")
        row.cells[1].text = f.get("rule", "")
        rag_cell(row.cells[2], f["status"])
        row.cells[3].text = f.get("description", "")


def add_remediation_table(doc: Document, findings: list, section_num: int):
    doc.add_heading(f"{section_num}. Remediation Action Plan", level=1)
    failed = [f for f in findings if f["status"] in ("RED", "AMBER")]
    if not failed:
        doc.add_paragraph("No remediation actions required. All controls assessed as PASS.")
        return
    tbl = doc.add_table(rows=1 + len(failed), cols=4)
    tbl.style = "Table Grid"
    for j, h in enumerate(["Priority", "Rule", "Finding", "Recommended Action"]):
        header_cell(tbl.rows[0].cells[j], h)
    for i, f in enumerate(failed):
        row = tbl.rows[i + 1]
        priority = PRIORITY_MAP.get(f["status"], "MEDIUM")
        row.cells[0].text = priority
        row.cells[1].text = f.get("rule", "")
        row.cells[2].text = f.get("description", "")
        row.cells[3].text = f.get("commentary", "")
        set_cell_bg(row.cells[0], RAG_BG.get(f["status"], "888888"))
        if row.cells[0].paragraphs[0].runs:
            row.cells[0].paragraphs[0].runs[0].font.color.rgb = WHITE
            row.cells[0].paragraphs[0].runs[0].font.bold = True


def add_enforcement_section(doc: Document, report_type: str, section_num: int):
    """Add a section showing relevant FCA enforcement cases for this report type."""
    try:
        from fca_reference import ENFORCEMENT_CASES
        cases = ENFORCEMENT_CASES.get(report_type, [])
    except ImportError:
        return
    if not cases:
        return
    doc.add_heading(f"{section_num}. FCA Enforcement Context", level=1)
    doc.add_paragraph(
        "The following enforcement actions are directly relevant to the subject matter of this report. "
        "They illustrate the FCA's enforcement priorities and the financial consequences of non-compliance."
    ).runs[0].font.italic = True
    tbl = doc.add_table(rows=1 + len(cases), cols=4)
    tbl.style = "Table Grid"
    for j, h in enumerate(["Firm", "Penalty", "Rules Breached", "Summary"]):
        header_cell(tbl.rows[0].cells[j], h)
    for i, c in enumerate(cases):
        row = tbl.rows[i + 1]
        row.cells[0].text = c.get("firm", "")
        row.cells[1].text = c.get("fine", "N/A")
        row.cells[2].text = ", ".join(c.get("rules", []))
        row.cells[3].text = c.get("summary", "")
        if row.cells[1].paragraphs[0].runs:
            row.cells[1].paragraphs[0].runs[0].font.bold = True


def add_regulatory_updates_section(doc: Document, report_type: str, section_num: int):
    """Add a section summarising key regulatory changes relevant to this report type."""
    try:
        from fca_reference import REGULATORY_UPDATES
        updates = REGULATORY_UPDATES.get(report_type, {})
    except ImportError:
        return
    if not updates:
        return
    doc.add_heading(f"{section_num}. Key Regulatory Updates", level=1)
    doc.add_paragraph(
        f"The following regulatory changes are in force and directly affect the scope of this report. "
        f"Sourced from the FCA Handbook and FCA publications as of October 2026."
    ).runs[0].font.italic = True
    for key, text in updates.items():
        title = key.replace("_", " ").title()
        doc.add_heading(title, level=2)
        doc.add_paragraph(text)


def add_intel_section(doc: Document, intel: dict, section_num: int):
    if not intel:
        return
    doc.add_heading(f"{section_num}. Live Regulatory Intelligence", level=1)
    doc.add_paragraph(
        f"Retrieved {date.today().strftime('%d %B %Y')} via Govisk ExecCom Routing Intelligence Scan. "
        "Verify material findings at fca.org.uk before relying on them."
    ).runs[0].font.italic = True
    for topic, result in intel.items():
        doc.add_heading(topic, level=2)
        doc.add_paragraph(result.get("summary", "No data available."))
        for c in result.get("citations", []):
            doc.add_paragraph(c, style="List Bullet")


_GLOBAL_FRAMEWORK = [
    (
        "UK",
        "CASS 6 & 7",
        "FCA CASS Handbook — CASS 6 (custody), CASS 7 (client money), CASS 10 (resolution pack). Baseline for all UK-authorised firms.",
    ),
    (
        "N. America",
        "SEC Rule 15c3-3 / CFTC Rule 1.20",
        "SEC Rule 15c3-3 (securities), CFTC Rule 1.20 (commodities), SIPC. Canada: CIRO (2023 merger of IIROC + MFDA), Form 1 trust account rules.",
    ),
    (
        "Latin America",
        "Country-specific acts",
        "Brazil Law 12,865; Argentina BCRA A 6859; Mexico Fintech Law (2018); Chile Law 21,521; Colombia SFC client asset rules.",
    ),
    (
        "Asia Pacific",
        "Various statutory",
        "HK Cap.571I (client money) / 571H (securities); Singapore SFA s.104 + MAS SFLCBR; Australia Corporations Act Div.2 Pt.7.8; Japan FIEA Art.43-2.",
    ),
    (
        "Europe",
        "MiFID II Art.16",
        "MiFID II Art.16 + Delegated Reg.2017/593 (safeguarding); PSD2/PSD3 (payment safeguarding); EMD2. Note: EU uses civil-law statutory segregation — no trust mechanism as in UK CASS.",
    ),
    (
        "Africa",
        "FAIS Act / VAITOS Act",
        "South Africa: FAIS Act (trust property), Financial Markets Act, COFI Bill (pending). Mauritius: VAITOS Act (digital assets). WAEMU/BCEAO; CEMAC/BEAC; COMESA.",
    ),
]


def add_global_framework_table(doc: Document):
    """Append the 6-region client assets framework overview table to the document."""
    doc.add_heading("Global Client Assets Regulatory Framework Overview", level=2)
    doc.add_paragraph(
        "The following table summarises client assets equivalent frameworks across six global regions. "
        "Where a client operates across multiple jurisdictions, the most stringent applicable framework applies."
    ).runs[0].font.italic = True
    tbl = doc.add_table(rows=1 + len(_GLOBAL_FRAMEWORK), cols=3)
    tbl.style = "Table Grid"
    for j, h in enumerate(["Region", "Client Assets Equivalent", "Key Legislation / Framework"]):
        header_cell(tbl.rows[0].cells[j], h)
    for i, (region, equiv, leg) in enumerate(_GLOBAL_FRAMEWORK):
        row = tbl.rows[i + 1]
        row.cells[0].text = region
        row.cells[1].text = equiv
        row.cells[2].text = leg
        if row.cells[0].paragraphs[0].runs:
            row.cells[0].paragraphs[0].runs[0].font.bold = True


def add_regulatory_refs(doc: Document, refs: list, section_num: int):
    doc.add_heading(f"{section_num}. Regulatory References", level=1)
    tbl = doc.add_table(rows=len(refs), cols=2)
    tbl.style = "Table Grid"
    for i, (ref, desc) in enumerate(refs):
        tbl.rows[i].cells[0].text = ref
        tbl.rows[i].cells[1].text = desc
        if tbl.rows[i].cells[0].paragraphs[0].runs:
            tbl.rows[i].cells[0].paragraphs[0].runs[0].font.bold = True
    add_global_framework_table(doc)


_REGION_REG_LABELS = {
    "uk":            "FCA FRN",
    "north-america": "Bodie Ref:",
    "latin-america": "Bodie Ref:",
    "asia-pacific":  "Bodie Ref:",
    "europe":        "Bodie Ref:",
    "africa":        "Bodie Ref:",
}


def reg_id_label(data: dict) -> str:
    """Return the regulatory registration ID label for the firm's region."""
    slug = (data.get("region") or "").strip().lower()
    return _REGION_REG_LABELS.get(slug, "FCA FRN")


def save_report(doc: Document, prefix: str, client_name: str) -> Path:
    path = TMP_DIR / f"{prefix}_{client_name}_draft.docx"
    try:
        doc.save(path)
    except PermissionError:
        from datetime import datetime as _dt
        ts = _dt.now().strftime("%Y%m%d_%H%M%S")
        path = TMP_DIR / f"{prefix}_{client_name}_{ts}_draft.docx"
        doc.save(path)
    _log.info("report_saved", extra={"path": str(path)})
    return path
