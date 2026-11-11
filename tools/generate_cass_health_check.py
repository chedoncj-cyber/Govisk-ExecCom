"""
CASS Health Check Report Generator
Reads client input JSON and produces a scored Word document report.
Optionally runs Routing Intelligence Scan for live regulatory intelligence before scoring.
Usage: python tools/generate_cass_health_check.py --client "<client_name>" [--no-scan]
"""

import argparse
import json
import os
import sys
from datetime import datetime, date
from pathlib import Path
from dotenv import load_dotenv
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

load_dotenv()

# Allow importing perplexity_scan and regional_routing from sibling tools/ directory
sys.path.insert(0, str(Path(__file__).parent))

# ── Shared observability ───────────────────────────────────────────────────────
_SHARED = Path(__file__).parent.parent.parent / "shared"
sys.path.insert(0, str(_SHARED))
from observability import get_logger, metrics, trace_op
from regional_routing import detect_region, score_regional_client_money, regional_regulatory_refs
from report_base import reg_id_label
from regional_cass_equivalents import score_regional_health_check, HEALTH_CHECK_TITLES

_HC_SLUGS = {
    "north-america": "N. America", "latin-america": "Latin America",
    "asia-pacific": "Asia Pacific", "europe": "Europe", "africa": "Africa",
}

BASE_DIR = Path(__file__).parent.parent
TMP_DIR = BASE_DIR / ".tmp"
TMP_DIR.mkdir(exist_ok=True)

# RAG colours
RED    = RGBColor(0xC0, 0x00, 0x00)
AMBER  = RGBColor(0xFF, 0x8C, 0x00)
GREEN  = RGBColor(0x00, 0x70, 0x00)
BLACK  = RGBColor(0x00, 0x00, 0x00)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)

RAG_BG = {
    "GREEN":  "00B050",
    "AMBER":  "FFC000",
    "RED":    "FF0000",
}


def load_client_data(client_name: str) -> dict:
    path = TMP_DIR / f"cass_hc_{client_name}_input.json"
    if not path.exists():
        raise FileNotFoundError(
            f"Input file not found: {path}\n"
            f"Create it with the client data before running this tool."
        )
    with open(path) as f:
        raw = json.load(f)
    return {k: _coerce(v) for k, v in raw.items()}


def _coerce(v):
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


@trace_op("score_health_check")
def score_checks(data: dict) -> list[dict]:
    """
    Evaluate each CASS rule area and return a list of findings.
    Each finding: {area, rule, description, status, commentary}
    """
    _r = _HC_SLUGS.get((data.get("region") or "").strip().lower())
    if _r:
        return score_regional_health_check(data, _r)
    findings = []

    # --- CASS 7: Client Money ---

    # 7.13.4R — Daily reconciliation
    last_recon = data.get("last_cm_reconciliation_date")
    if last_recon:
        days_since = (date.today() - datetime.strptime(last_recon, "%Y-%m-%d").date()).days
        if days_since > 1:
            status = "RED"
            commentary = f"Last reconciliation was {days_since} day(s) ago. CASS 7.13.4R requires daily reconciliation."
        else:
            status = "GREEN"
            commentary = "Client money reconciliation performed within required daily frequency."
    else:
        status = "RED"
        commentary = "No reconciliation date provided. Unable to confirm compliance with CASS 7.13.4R."

    findings.append({
        "area": "CASS 7 — Client Money",
        "rule": "CASS 7.13.4R",
        "description": "Internal client money reconciliation — daily frequency",
        "status": status,
        "commentary": commentary,
    })

    # 7.18 — Acknowledgement letters
    ack_letters = data.get("acknowledgement_letters_in_place")
    if ack_letters is True:
        findings.append({
            "area": "CASS 7 — Client Money",
            "rule": "CASS 7.18",
            "description": "Acknowledgement letters from approved banks",
            "status": "GREEN",
            "commentary": "Acknowledgement letters confirmed in place for all approved banks.",
        })
    elif ack_letters is False:
        findings.append({
            "area": "CASS 7 — Client Money",
            "rule": "CASS 7.18",
            "description": "Acknowledgement letters from approved banks",
            "status": "RED",
            "commentary": "Acknowledgement letters NOT in place. Client must obtain letters within 20 business days.",
        })
    else:
        findings.append({
            "area": "CASS 7 — Client Money",
            "rule": "CASS 7.18",
            "description": "Acknowledgement letters from approved banks",
            "status": "AMBER",
            "commentary": "Acknowledgement letter status not confirmed. Verification required.",
        })

    # 7.19 — Diversification
    max_pct = data.get("max_single_institution_percentage")
    if max_pct is not None:
        if max_pct > 20:
            status = "AMBER"
            commentary = f"{max_pct}% of client money held at a single institution. Consider diversification under CASS 7.19."
        else:
            status = "GREEN"
            commentary = f"Client money diversification within acceptable range ({max_pct}% max single institution)."
    else:
        status = "AMBER"
        commentary = "Diversification data not provided. Review required under CASS 7.19."

    findings.append({
        "area": "CASS 7 — Client Money",
        "rule": "CASS 7.19",
        "description": "Diversification of client money deposits",
        "status": status,
        "commentary": commentary,
    })

    # 7.16 — Calculation method
    calc_method = data.get("client_money_calculation_method", "").lower()
    if calc_method == "standard":
        findings.append({
            "area": "CASS 7 — Client Money",
            "rule": "CASS 7.16",
            "description": "Client money calculation method",
            "status": "GREEN",
            "commentary": "Standard calculation method in use.",
        })
    elif calc_method == "alternative":
        fca_agreed = data.get("alternative_method_fca_agreed", False)
        if fca_agreed:
            findings.append({
                "area": "CASS 7 — Client Money",
                "rule": "CASS 7.16",
                "description": "Client money calculation method",
                "status": "GREEN",
                "commentary": "Alternative calculation method in use — FCA agreement confirmed.",
            })
        else:
            findings.append({
                "area": "CASS 7 — Client Money",
                "rule": "CASS 7.16",
                "description": "Client money calculation method",
                "status": "RED",
                "commentary": "Alternative calculation method in use but FCA agreement NOT confirmed. Must be agreed with FCA under CASS 7.16.",
            })
    else:
        findings.append({
            "area": "CASS 7 — Client Money",
            "rule": "CASS 7.16",
            "description": "Client money calculation method",
            "status": "AMBER",
            "commentary": "Calculation method not specified. Confirm standard or alternative method under CASS 7.16.",
        })

    # --- CASS 6: Custody Assets ---

    # 6.2 — Segregation
    segregated = data.get("custody_assets_segregated")
    if segregated is True:
        findings.append({
            "area": "CASS 6 — Custody Assets",
            "rule": "CASS 6.2",
            "description": "Segregation of client assets from firm assets",
            "status": "GREEN",
            "commentary": "Client custody assets confirmed segregated from firm assets.",
        })
    elif segregated is False:
        findings.append({
            "area": "CASS 6 — Custody Assets",
            "rule": "CASS 6.2",
            "description": "Segregation of client assets from firm assets",
            "status": "RED",
            "commentary": "Client custody assets NOT segregated. Immediate remediation required under CASS 6.2.",
        })
    else:
        findings.append({
            "area": "CASS 6 — Custody Assets",
            "rule": "CASS 6.2",
            "description": "Segregation of client assets from firm assets",
            "status": "AMBER",
            "commentary": "Segregation status not confirmed. Physical verification required.",
        })

    # 6.6.4R — Custody reconciliation frequency
    last_custody_recon = data.get("last_custody_reconciliation_date")
    if last_custody_recon:
        days_since = (date.today() - datetime.strptime(last_custody_recon, "%Y-%m-%d").date()).days
        if days_since > 25:
            status = "RED"
            commentary = f"Last custody reconciliation was {days_since} business day(s) ago. CASS 6.6.4R requires at least every 25 business days."
        else:
            status = "GREEN"
            commentary = f"Custody asset reconciliation within required 25 business day frequency ({days_since} days ago)."
    else:
        status = "AMBER"
        commentary = "Custody reconciliation date not provided. Verification required under CASS 6.6.4R."

    findings.append({
        "area": "CASS 6 — Custody Assets",
        "rule": "CASS 6.6.4R",
        "description": "Safe custody asset reconciliation — 25 business day frequency",
        "status": status,
        "commentary": commentary,
    })

    # --- COOF ---
    coof_named = data.get("coof_individual_named")
    coof_review_date = data.get("coof_last_review_date")
    cass_category = data.get("cass_category", "").lower()

    if cass_category == "large":
        if coof_named and coof_review_date:
            findings.append({
                "area": "CASS 1A — Oversight",
                "rule": "CASS 1A.3",
                "description": "CASS Operational Oversight Function (COOF)",
                "status": "GREEN",
                "commentary": f"COOF individual named. Last review: {coof_review_date}.",
            })
        else:
            findings.append({
                "area": "CASS 1A — Oversight",
                "rule": "CASS 1A.3",
                "description": "CASS Operational Oversight Function (COOF)",
                "status": "RED",
                "commentary": "Large CASS firm must have a named COOF individual with documented reviews under CASS 1A.3.",
            })

    # --- Consumer Duty / CASS 7.11.32R (effective 25 Sep 2026) ---
    retail_clients = data.get("has_retail_clients", True)  # default assume retail present
    interest_paid = data.get("retail_interest_paid")
    interest_notified = data.get("retail_interest_not_paid_notified")
    if retail_clients is not False:
        if interest_paid is True:
            findings.append({
                "area": "Consumer Duty — CASS 7",
                "rule": "CASS 7.11.32 R",
                "description": "Interest on retail client money (effective 25 Sep 2026)",
                "status": "GREEN",
                "commentary": "Interest on retail client money is being paid in compliance with CASS 7.11.32 R.",
            })
        elif interest_paid is False and interest_notified is True:
            findings.append({
                "area": "Consumer Duty — CASS 7",
                "rule": "CASS 7.11.32 R",
                "description": "Interest on retail client money (effective 25 Sep 2026)",
                "status": "AMBER",
                "commentary": (
                    "Non-payment of interest notified in writing. Confirm this is compatible with Consumer Duty "
                    "(FCA Consumer Duty Outcome 2) to avoid dual breach risk."
                ),
            })
        else:
            findings.append({
                "area": "Consumer Duty — CASS 7",
                "rule": "CASS 7.11.32 R",
                "description": "Interest on retail client money (effective 25 Sep 2026)",
                "status": "RED",
                "commentary": (
                    "CASS 7.11.32 R (live 25 Sep 2026): firms MUST pay retail clients interest on client money "
                    "unless non-payment is notified in writing AND compatible with Consumer Duty. "
                    "Confirm payment status immediately."
                ),
            })

    # --- CASS 6.3.2A R — Third-party custodian selection records (25 Sep 2026) ---
    custodian_grounds_recorded = data.get("custodian_selection_grounds_recorded")
    if custodian_grounds_recorded is True:
        findings.append({
            "area": "Consumer Duty — CASS 6",
            "rule": "CASS 6.3.2A R",
            "description": "Third-party custodian selection grounds recorded (effective 25 Sep 2026)",
            "status": "GREEN",
            "commentary": "Grounds for selecting each third-party custodian are documented as required by CASS 6.3.2A R.",
        })
    elif custodian_grounds_recorded is False:
        findings.append({
            "area": "Consumer Duty — CASS 6",
            "rule": "CASS 6.3.2A R",
            "description": "Third-party custodian selection grounds recorded (effective 25 Sep 2026)",
            "status": "RED",
            "commentary": (
                "CASS 6.3.2A R (live 25 Sep 2026): firms must record their grounds for selecting each "
                "third-party custodian. This is a new mandatory obligation — remediate immediately."
            ),
        })

    # --- CASS 15 — Payment/e-money firm safeguarding (effective 7 May 2026) ---
    is_payment_firm = data.get("is_payment_or_emoney_firm", False)
    if is_payment_firm:
        cass15_daily_recon = data.get("cass15_daily_reconciliation_in_place")
        cass15_monthly_return = data.get("cass15_monthly_return_submitted")
        cass15_audit = data.get("cass15_safeguarding_audit_completed")

        if cass15_daily_recon is True:
            findings.append({
                "area": "CASS 15 — Payment Safeguarding",
                "rule": "CASS 15.2 R",
                "description": "Daily reconciliation of safeguarded funds",
                "status": "GREEN",
                "commentary": "Daily safeguarding reconciliation in place as required by CASS 15.2 R (from 7 May 2026).",
            })
        else:
            findings.append({
                "area": "CASS 15 — Payment Safeguarding",
                "rule": "CASS 15.2 R",
                "description": "Daily reconciliation of safeguarded funds",
                "status": "RED",
                "commentary": (
                    "CASS 15.2 R (live 7 May 2026): payment/e-money firms must perform daily reconciliation "
                    "of safeguarded funds. Replaces previous PSR/EMR requirements."
                ),
            })

        if cass15_monthly_return is True:
            findings.append({
                "area": "CASS 15 — Payment Safeguarding",
                "rule": "CASS 15.3 R",
                "description": "Monthly safeguarding return to FCA",
                "status": "GREEN",
                "commentary": "Monthly safeguarding return submitted to FCA as required by CASS 15.3 R.",
            })
        else:
            findings.append({
                "area": "CASS 15 — Payment Safeguarding",
                "rule": "CASS 15.3 R",
                "description": "Monthly safeguarding return to FCA",
                "status": "AMBER",
                "commentary": "CASS 15.3 R: monthly safeguarding return status unconfirmed. Submit to FCA each calendar month.",
            })

        if cass15_audit is True:
            findings.append({
                "area": "CASS 15 — Payment Safeguarding",
                "rule": "CASS 15.4 R",
                "description": "Annual mandatory safeguarding audit",
                "status": "GREEN",
                "commentary": "Annual safeguarding audit completed as required by CASS 15.4 R.",
            })
        else:
            findings.append({
                "area": "CASS 15 — Payment Safeguarding",
                "rule": "CASS 15.4 R",
                "description": "Annual mandatory safeguarding audit",
                "status": "AMBER",
                "commentary": "CASS 15.4 R: annual safeguarding audit required. Arrange external audit if not yet completed.",
            })

    # --- Breach History ---
    breaches = data.get("cass_breaches_last_12_months", False)
    breach_details = data.get("cass_breach_details", "")
    if breaches:
        findings.append({
            "area": "Breach History",
            "rule": "SUP 15.3",
            "description": "CASS breaches in last 12 months",
            "status": "RED",
            "commentary": f"Active/prior breach(es) reported: {breach_details}. Review FCA notification obligations under SUP 15.3.",
        })
    else:
        findings.append({
            "area": "Breach History",
            "rule": "SUP 15.3",
            "description": "CASS breaches in last 12 months",
            "status": "GREEN",
            "commentary": "No CASS breaches reported in the last 12 months.",
        })

    regional_findings = score_regional_client_money(data)
    findings.extend(regional_findings)
    return findings


def rag_counts(findings: list[dict]) -> dict:
    counts = {"RED": 0, "AMBER": 0, "GREEN": 0}
    for f in findings:
        counts[f["status"]] = counts.get(f["status"], 0) + 1
    return counts


def set_cell_bg(cell, hex_color: str):
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


@trace_op("build_health_check_report")
def build_report(data: dict, findings: list[dict], client_name: str, intel: dict = None) -> Document:
    doc = Document()
    slug = (data.get("region") or "").strip().lower()
    _r = _HC_SLUGS.get(slug, "UK")
    _report_title = HEALTH_CHECK_TITLES.get(_r, HEALTH_CHECK_TITLES["UK"])

    # Title
    title = doc.add_heading(_report_title, level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph(
        f"Prepared for: {data.get('firm_name', client_name)}\n"
        f"{reg_id_label(data)}: {data.get('frn', 'N/A')}\n"
        f"CASS Category: {data.get('cass_category', 'N/A').upper()}\n"
        f"Report Date: {date.today().strftime('%d %B %Y')}\n"
        f"Prepared by: CASS Intelligence Reports"
    )

    doc.add_paragraph(
        "CONFIDENTIAL — This report is prepared for the exclusive use of the named firm. "
        "It does not constitute legal or regulatory advice. The firm should seek independent "
        "legal counsel for formal compliance determinations."
    ).runs[0].font.italic = True

    # Executive Summary
    doc.add_heading("1. Executive Summary", level=1)
    counts = rag_counts(findings)
    if _r == "UK":
        doc.add_paragraph(
            f"This CASS Health Check assessed {len(findings)} control areas across CASS 6 (Custody Assets), "
            f"CASS 7 (Client Money), and CASS oversight obligations.\n\n"
            f"Summary findings: {counts['GREEN']} PASS  |  {counts['AMBER']} REQUIRES ATTENTION  |  {counts['RED']} FAIL"
        )
    else:
        doc.add_paragraph(
            f"This client assets health check assessed {len(findings)} control areas under applicable "
            f"{_r} regulatory requirements for {data.get('firm_name', client_name)}.\n\n"
            f"Summary findings: {counts['GREEN']} PASS  |  {counts['AMBER']} REQUIRES ATTENTION  |  {counts['RED']} FAIL"
        )

    if counts["RED"] > 0:
        doc.add_paragraph(
            f"IMMEDIATE ACTION REQUIRED: {counts['RED']} critical finding(s) identified. "
            "See Section 7 — Remediation Action Plan."
        ).runs[0].font.bold = True

    # Firm Profile
    doc.add_heading("2. Firm Profile", level=1)
    profile_table = doc.add_table(rows=5, cols=2)
    profile_table.style = "Table Grid"
    rows = [
        ("Firm Name", data.get("firm_name", client_name)),
        (reg_id_label(data), data.get("frn", "N/A")),
        ("CASS Category", data.get("cass_category", "N/A").upper()),
        ("Assessment Date", date.today().strftime("%d %B %Y")),
        ("Assessment Period", data.get("assessment_period", "Last 12 months")),
    ]
    for i, (label, value) in enumerate(rows):
        profile_table.rows[i].cells[0].text = label
        profile_table.rows[i].cells[1].text = str(value)
        profile_table.rows[i].cells[0].paragraphs[0].runs[0].font.bold = True

    # Findings by Area
    if _r == "UK":
        areas = [
            "CASS 7 — Client Money",
            "CASS 6 — Custody Assets",
            "CASS 1A — Oversight",
            "Consumer Duty — CASS 7",
            "Consumer Duty — CASS 6",
            "CASS 15 — Payment Safeguarding",
            "Breach History",
        ]
        section_nums = {
            "CASS 7 — Client Money":              "3",
            "CASS 6 — Custody Assets":            "4",
            "CASS 1A — Oversight":                "5",
            "Consumer Duty — CASS 7":             "6",
            "Consumer Duty — CASS 6":             "7",
            "CASS 15 — Payment Safeguarding":     "8",
            "Breach History":                     "9",
        }
        for area in areas:
            area_findings = [f for f in findings if f["area"] == area]
            if not area_findings:
                continue
            doc.add_heading(f"{section_nums[area]}. {area}", level=1)
            tbl = doc.add_table(rows=1 + len(area_findings), cols=4)
            tbl.style = "Table Grid"
            for j, h in enumerate(["Rule", "Control Area", "Status", "Commentary"]):
                cell = tbl.rows[0].cells[j]
                cell.text = h
                cell.paragraphs[0].runs[0].font.bold = True
                set_cell_bg(cell, "1F4E79")
                cell.paragraphs[0].runs[0].font.color.rgb = WHITE
            for i, f in enumerate(area_findings):
                row = tbl.rows[i + 1]
                row.cells[0].text = f["rule"]
                row.cells[1].text = f["description"]
                row.cells[2].text = f["status"]
                row.cells[3].text = f["commentary"]
                set_cell_bg(row.cells[2], RAG_BG[f["status"]])
                row.cells[2].paragraphs[0].runs[0].font.color.rgb = WHITE
                row.cells[2].paragraphs[0].runs[0].font.bold = True
        _next_sec = 10
    else:
        # Regional findings — group by area dynamically
        seen_areas = []
        for f in findings:
            if f["area"] not in seen_areas:
                seen_areas.append(f["area"])
        sec = 3
        for area in seen_areas:
            area_findings = [f for f in findings if f["area"] == area]
            doc.add_heading(f"{sec}. {area}", level=1)
            tbl = doc.add_table(rows=1 + len(area_findings), cols=4)
            tbl.style = "Table Grid"
            for j, h in enumerate(["Rule", "Control Area", "Status", "Commentary"]):
                cell = tbl.rows[0].cells[j]
                cell.text = h
                cell.paragraphs[0].runs[0].font.bold = True
                set_cell_bg(cell, "1F4E79")
                cell.paragraphs[0].runs[0].font.color.rgb = WHITE
            for i, f in enumerate(area_findings):
                row = tbl.rows[i + 1]
                row.cells[0].text = f["rule"]
                row.cells[1].text = f["description"]
                row.cells[2].text = f["status"]
                row.cells[3].text = f["commentary"]
                set_cell_bg(row.cells[2], RAG_BG[f["status"]])
                row.cells[2].paragraphs[0].runs[0].font.color.rgb = WHITE
                row.cells[2].paragraphs[0].runs[0].font.bold = True
            sec += 1
        _next_sec = sec

    # Findings Summary Table
    doc.add_heading(f"{_next_sec}. Findings Summary", level=1)
    summary_tbl = doc.add_table(rows=1 + len(findings), cols=4)
    summary_tbl.style = "Table Grid"
    for j, h in enumerate(["Area", "Rule", "Status", "Description"]):
        cell = summary_tbl.rows[0].cells[j]
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        set_cell_bg(cell, "1F4E79")
        cell.paragraphs[0].runs[0].font.color.rgb = WHITE

    for i, f in enumerate(findings):
        row = summary_tbl.rows[i + 1]
        row.cells[0].text = f["area"]
        row.cells[1].text = f["rule"]
        row.cells[2].text = f["status"]
        row.cells[3].text = f["description"]
        set_cell_bg(row.cells[2], RAG_BG[f["status"]])
        row.cells[2].paragraphs[0].runs[0].font.color.rgb = WHITE
        row.cells[2].paragraphs[0].runs[0].font.bold = True

    # Remediation Action Plan
    doc.add_heading(f"{_next_sec + 1}. Remediation Action Plan", level=1)
    failed = [f for f in findings if f["status"] in ("RED", "AMBER")]
    if not failed:
        doc.add_paragraph("No remediation actions required. All controls assessed as PASS.")
    else:
        action_tbl = doc.add_table(rows=1 + len(failed), cols=4)
        action_tbl.style = "Table Grid"
        for j, h in enumerate(["Priority", "Rule", "Finding", "Recommended Action"]):
            cell = action_tbl.rows[0].cells[j]
            cell.text = h
            cell.paragraphs[0].runs[0].font.bold = True
            set_cell_bg(cell, "1F4E79")
            cell.paragraphs[0].runs[0].font.color.rgb = WHITE

        priority_map = {"RED": "IMMEDIATE", "AMBER": "HIGH"}
        for i, f in enumerate(failed):
            row = action_tbl.rows[i + 1]
            row.cells[0].text = priority_map.get(f["status"], "MEDIUM")
            row.cells[1].text = f["rule"]
            row.cells[2].text = f["description"]
            row.cells[3].text = f["commentary"]
            set_cell_bg(row.cells[0], RAG_BG[f["status"]])
            row.cells[0].paragraphs[0].runs[0].font.color.rgb = WHITE
            row.cells[0].paragraphs[0].runs[0].font.bold = True

    _enf_sec = _next_sec + 2
    _enf_added = False
    # Enforcement Context (fca_reference.py)
    try:
        from fca_reference import ENFORCEMENT_CASES
        cases = ENFORCEMENT_CASES.get("cass_health_check", [])
        if cases:
            doc.add_heading(f"{_enf_sec}. FCA Enforcement Context", level=1)
            doc.add_paragraph(
                "The following FCA enforcement actions relate directly to CASS 6 and CASS 7 obligations. "
                "They illustrate the financial and reputational consequences of control failures."
            ).runs[0].font.italic = True
            from docx.oxml.ns import qn as _qn
            from docx.oxml import OxmlElement as _OxmlElement
            enf_tbl = doc.add_table(rows=1 + len(cases), cols=4)
            enf_tbl.style = "Table Grid"
            for j, h_text in enumerate(["Firm", "Penalty", "Rules", "Summary"]):
                cell = enf_tbl.rows[0].cells[j]
                cell.text = h_text
                cell.paragraphs[0].runs[0].font.bold = True
                set_cell_bg(cell, "1F4E79")
                cell.paragraphs[0].runs[0].font.color.rgb = WHITE
            for i, c in enumerate(cases):
                row = enf_tbl.rows[i + 1]
                row.cells[0].text = c.get("firm", "")
                row.cells[1].text = c.get("fine", "N/A")
                row.cells[2].text = ", ".join(c.get("rules", []))
                row.cells[3].text = c.get("summary", "")
                if row.cells[1].paragraphs[0].runs:
                    row.cells[1].paragraphs[0].runs[0].font.bold = True
            _enf_added = True
    except Exception:
        pass

    _intel_sec = _enf_sec + (1 if _enf_added else 0)
    # Routing Intelligence Scan
    if intel:
        doc.add_heading(f"{_intel_sec}. Live Regulatory Intelligence", level=1)
        doc.add_paragraph(
            f"The following intelligence was retrieved from live web sources on "
            f"{date.today().strftime('%d %B %Y')} via Routing Intelligence Scan. "
            "Verify material findings directly at fca.org.uk before relying on them."
        ).runs[0].font.italic = True

        for topic, result in intel.items():
            doc.add_heading(topic, level=2)
            doc.add_paragraph(result.get("summary", "No data available."))
            citations = result.get("citations", [])
            if citations:
                p = doc.add_paragraph("Sources: ")
                p.runs[0].font.bold = True
                for c in citations:
                    doc.add_paragraph(c, style="List Bullet")

    # Regulatory References
    ref_section = _intel_sec + (1 if intel else 0)
    doc.add_heading(f"{ref_section}. Regulatory References", level=1)
    country = data.get("country", "") or data.get("jurisdiction", "")
    regional_refs = regional_regulatory_refs(data.get("region", "") or country)
    refs = [
        ("CASS 6", "CASS (Client Assets Sourcebook) 6 — Custody rules — safeguarding and administration of client assets"),
        ("CASS 7", "CASS (Client Assets Sourcebook) 7 — Client money rules — segregation and reconciliation requirements"),
        ("CASS 7.11.32 R", "Interest on retail client money — Consumer Duty obligation (effective 25 Sep 2026)"),
        ("CASS 6.3.2A R", "Third-party custodian selection grounds — record keeping (effective 25 Sep 2026)"),
        ("CASS 6.4.1BA R", "Use of retail client assets — Consumer Duty compatibility (effective 25 Sep 2026)"),
        ("CASS 15", "Payment/e-money safeguarding regime (effective 7 May 2026 — PS25/12)"),
        ("CASS 7A", "Client money distribution and transfer"),
        ("CASS 10", "CASS resolution pack"),
        ("CASS 1A.3", "CASS Operational Oversight Function (COOF)"),
        ("SUP 15.3", "Notification to the FCA — material breach"),
        ("FCA Handbook", "https://www.handbook.fca.org.uk/handbook/CASS/"),
    ] + regional_refs
    ref_tbl = doc.add_table(rows=len(refs), cols=2)
    ref_tbl.style = "Table Grid"
    for i, (ref, desc) in enumerate(refs):
        ref_tbl.rows[i].cells[0].text = ref
        ref_tbl.rows[i].cells[1].text = desc
        ref_tbl.rows[i].cells[0].paragraphs[0].runs[0].font.bold = True

    # Global client assets framework overview
    doc.add_heading("Global Client Assets Regulatory Framework Overview", level=2)
    doc.add_paragraph(
        "The following table summarises client assets equivalent frameworks across six global regions. "
        "Where a client operates across multiple jurisdictions, the most stringent applicable framework applies."
    ).runs[0].font.italic = True
    _gf_data = [
        ("UK", "CASS 6 & 7",
         "FCA CASS Handbook — CASS 6 (custody), CASS 7 (client money), CASS 10 (resolution pack). Baseline for all UK-authorised firms."),
        ("N. America", "SEC Rule 15c3-3 / CFTC Rule 1.20",
         "SEC Rule 15c3-3 (securities), CFTC Rule 1.20 (commodities), SIPC. Canada: CIRO (2023 merger of IIROC + MFDA), Form 1 trust account rules."),
        ("Latin America", "Country-specific acts",
         "Brazil Law 12,865; Argentina BCRA A 6859; Mexico Fintech Law (2018); Chile Law 21,521; Colombia SFC client asset rules."),
        ("Asia Pacific", "Various statutory",
         "HK Cap.571I (client money) / 571H (securities); Singapore SFA s.104 + MAS SFLCBR; Australia Corporations Act Div.2 Pt.7.8; Japan FIEA Art.43-2."),
        ("Europe", "MiFID II Art.16",
         "MiFID II Art.16 + Delegated Reg.2017/593 (safeguarding); PSD2/PSD3 (payment safeguarding); EMD2. Note: EU uses civil-law statutory segregation — no trust mechanism as in UK CASS."),
        ("Africa", "FAIS Act / VAITOS Act",
         "South Africa: FAIS Act (trust property), Financial Markets Act, COFI Bill (pending). Mauritius: VAITOS Act (digital assets). WAEMU/BCEAO; CEMAC/BEAC; COMESA."),
    ]
    gf_tbl = doc.add_table(rows=1 + len(_gf_data), cols=3)
    gf_tbl.style = "Table Grid"
    for j, h in enumerate(["Region", "Client Assets Equivalent", "Key Legislation / Framework"]):
        cell = gf_tbl.rows[0].cells[j]
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        set_cell_bg(cell, "1F4E79")
        cell.paragraphs[0].runs[0].font.color.rgb = WHITE
    for i, (region, equiv, leg) in enumerate(_gf_data):
        row = gf_tbl.rows[i + 1]
        row.cells[0].text = region
        row.cells[1].text = equiv
        row.cells[2].text = leg
        if row.cells[0].paragraphs[0].runs:
            row.cells[0].paragraphs[0].runs[0].font.bold = True

    return doc


def main():
    parser = argparse.ArgumentParser(description="Generate a CASS Health Check Report")
    parser.add_argument("--client", required=True, help="Client name (used to find input JSON in .tmp/)")
    parser.add_argument("--no-scan", action="store_true", help="Skip Routing Intelligence Scan")
    args = parser.parse_args()

    client_name = args.client.replace(" ", "_")
    print(f"Loading client data for: {client_name}")
    data = load_client_data(client_name)
    country = data.get("country", "") or data.get("jurisdiction", "")
    region  = detect_region(data.get("region") or country) if (data.get("region") or country) else None

    # Routing Intelligence Scan
    intel = {}
    if not args.no_scan:
        try:
            from perplexity_scan import build_regulatory_context
            print("Running Routing Intelligence Scan...")
            intel = build_regulatory_context("cass_health_check", region=region, country=country)
        except EnvironmentError as e:
            print(f"Routing Intelligence Scan unavailable — {e}")
        except Exception as e:
            print(f"Routing Intelligence Scan error, continuing — {e}")
    else:
        print("Routing Intelligence Scan skipped")

    print("Scoring CASS compliance checks...")
    findings = score_checks(data)

    counts = rag_counts(findings)
    print(f"Results: {counts['GREEN']} PASS | {counts['AMBER']} REQUIRES ATTENTION | {counts['RED']} FAIL")

    print("Building report document...")
    doc = build_report(data, findings, client_name, intel=intel)

    output_path = TMP_DIR / f"cass_hc_{client_name}_draft.docx"
    try:
        doc.save(output_path)
    except PermissionError:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = TMP_DIR / f"cass_hc_{client_name}_{ts}_draft.docx"
        doc.save(output_path)
    metrics.inc("report_generated", report_type="cass_health_check")
    print(f"Report saved to: {output_path}")


if __name__ == "__main__":
    main()
