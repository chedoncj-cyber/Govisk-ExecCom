"""
CASS Oversight Report Generator (COOF / CASS 1A)
Usage: python tools/generate_cass_oversight.py --client "<client_name>" [--no-scan]
"""

import argparse
import sys
from datetime import datetime, date
from pathlib import Path
from dotenv import load_dotenv
from report_base import *
from regional_routing import detect_region, score_regional_client_money, regional_regulatory_refs
from regional_cass_equivalents import score_regional_oversight, OVERSIGHT_TITLES

load_dotenv()

# ── Shared observability ───────────────────────────────────────────────────────
_SHARED = Path(__file__).parent.parent.parent / "shared"
sys.path.insert(0, str(_SHARED))
from observability import get_logger, metrics, trace_op

REPORT_TYPE = "cass_oversight"
PREFIX = "coof"

_OV_SLUGS = {
    "north-america": "N. America", "latin-america": "Latin America",
    "asia-pacific": "Asia Pacific", "europe": "Europe", "africa": "Africa",
}


@trace_op("score_oversight")
def score_checks(data: dict) -> list:
    _r = _OV_SLUGS.get((data.get("region") or "").strip().lower())
    if _r:
        return score_regional_oversight(data, _r)

    findings = []
    category = data.get("cass_category", "").lower()
    is_large = category == "large"

    # COOF named individual
    coof_named = data.get("coof_individual_name")
    if is_large:
        findings.append({
            "area": "COOF Constitution", "rule": "CASS 1A.3.1R",
            "description": "Named COOF individual appointed",
            "status": "GREEN" if coof_named else "RED",
            "commentary": f"COOF individual: {coof_named}." if coof_named else "No named COOF individual. Mandatory for Large CASS firms under CASS 1A.3.1R.",
        })
    else:
        findings.append({
            "area": "COOF Constitution", "rule": "CASS 1A",
            "description": "COOF oversight arrangements",
            "status": "GREEN" if coof_named else "AMBER",
            "commentary": f"COOF-equivalent individual: {coof_named}." if coof_named else f"No COOF individual named. CASS 1A obligations lighter for {category.upper()} firms but oversight still recommended.",
        })

    # Qualifications / expertise
    qualified = data.get("coof_individual_qualified")
    findings.append({
        "area": "COOF Qualifications", "rule": "CASS 1A.3.3R",
        "description": "COOF individual has appropriate CASS skills and expertise",
        "status": "GREEN" if qualified else ("RED" if is_large else "AMBER"),
        "commentary": "COOF individual's qualifications and expertise confirmed." if qualified
        else "COOF individual's CASS expertise not confirmed. CASS 1A.3.3R requires appropriate skills.",
    })

    # Independence — not doubling as compliance officer
    dual_role = data.get("coof_also_compliance_officer")
    findings.append({
        "area": "COOF Independence", "rule": "CASS 1A.3",
        "description": "COOF individual not solely reliant on compliance function",
        "status": "AMBER" if dual_role else "GREEN",
        "commentary": "COOF individual also serves as compliance officer — dual role may limit independence. Consider separation." if dual_role
        else "COOF individual operates independently of compliance officer role.",
    })

    # Annual report to governing body
    last_report = data.get("last_coof_report_to_board_date")
    if last_report:
        days = (date.today() - datetime.strptime(last_report, "%Y-%m-%d").date()).days
        if days > 365:
            s, c = "RED", f"Last COOF report to governing body was {days} days ago. Annual reporting required under CASS 1A.3.4R."
        else:
            s, c = "GREEN", f"COOF report delivered to governing body on {last_report} ({days} days ago)."
    else:
        s, c = "RED" if is_large else "AMBER", "No COOF report date on record. Annual reporting to governing body required under CASS 1A.3.4R."
    findings.append({"area": "COOF Reporting", "rule": "CASS 1A.3.4R", "description": "Annual COOF report to governing body", "status": s, "commentary": c})

    # Board minutes confirmation
    minutes = data.get("board_minutes_confirm_coof_report")
    findings.append({
        "area": "COOF Reporting", "rule": "CASS 1A.3.4R",
        "description": "Board/committee minutes confirm COOF report received",
        "status": "GREEN" if minutes else "AMBER",
        "commentary": "Board/committee minutes confirm COOF report received and noted." if minutes
        else "No board minutes confirming COOF report receipt. Minutes should evidence governance oversight.",
    })

    # Last COOF review of CASS arrangements
    last_review = data.get("last_coof_review_of_cass_date")
    if last_review:
        days = (date.today() - datetime.strptime(last_review, "%Y-%m-%d").date()).days
        s = "GREEN" if days <= 365 else "AMBER"
        c = f"Last COOF review of CASS arrangements: {last_review} ({days} days ago)."
    else:
        s, c = "AMBER", "No COOF review date on record. Regular reviews of CASS arrangements expected under CASS 1A.4."
    findings.append({"area": "COOF Activity", "rule": "CASS 1A.4", "description": "COOF review of CASS arrangements", "status": s, "commentary": c})

    # Outstanding recommendations
    outstanding = data.get("outstanding_coof_recommendations")
    if outstanding:
        rec_count = len(outstanding) if isinstance(outstanding, list) else int(outstanding)
        findings.append({
            "area": "Outstanding Recommendations", "rule": "CASS 1A.4",
            "description": "COOF outstanding recommendations",
            "status": "RED",
            "commentary": f"{rec_count} outstanding COOF recommendation(s) with no confirmed action plan. Immediate escalation required.",
        })
    else:
        findings.append({
            "area": "Outstanding Recommendations", "rule": "CASS 1A.4",
            "description": "COOF outstanding recommendations",
            "status": "GREEN", "commentary": "No outstanding COOF recommendations.",
        })

    regional_findings = score_regional_client_money(data)
    findings.extend(regional_findings)
    return findings


@trace_op("build_oversight_report")
def build_report(data: dict, findings: list, client_name: str, intel: dict = None) -> Document:
    slug = (data.get("region") or "").strip().lower()
    _r = _OV_SLUGS.get(slug, "UK")
    _title = OVERSIGHT_TITLES.get(_r, OVERSIGHT_TITLES["UK"])
    doc = start_document(_title, data, client_name)
    counts = rag_counts(findings)
    doc.add_heading("2. Executive Summary", level=1)
    if _r == "UK":
        doc.add_paragraph(
            f"CASS 1A Operational Oversight Function assessment for {data.get('firm_name', client_name)} "
            f"(CASS Category: {data.get('cass_category', 'N/A').upper()}). "
            f"{len(findings)} checks: {counts['GREEN']} PASS | {counts['AMBER']} ATTENTION | {counts['RED']} FAIL."
        )
    else:
        doc.add_paragraph(
            f"Compliance oversight function assessment for {data.get('firm_name', client_name)} "
            f"under applicable {_r} regulatory requirements. "
            f"{len(findings)} checks: {counts['GREEN']} PASS | {counts['AMBER']} ATTENTION | {counts['RED']} FAIL."
        )
    if counts["RED"]:
        doc.add_paragraph(f"CRITICAL: {counts['RED']} failure(s) in compliance oversight governance.").runs[0].font.bold = True

    add_firm_profile(doc, data, client_name, [
        ("CASS Category", data.get("cass_category", "N/A").upper()),
        ("Oversight Individual", data.get("coof_individual_name", "Not named")),
    ])
    if _r == "UK":
        add_findings_table(doc, [f for f in findings if f["area"] in ("COOF Constitution", "COOF Qualifications", "COOF Independence")], "COOF Constitution & Appointment", 4)
        add_findings_table(doc, [f for f in findings if f["area"] in ("COOF Reporting", "COOF Activity")], "COOF Activity & Reporting", 5)
        add_findings_table(doc, [f for f in findings if f["area"] == "Outstanding Recommendations"], "Outstanding Recommendations", 6)
    else:
        add_findings_table(doc, [f for f in findings if f["area"] in ("Compliance Officer", "CCO Appointment", "Qualifications", "CCO Qualifications", "Independence", "CCO Independence")], "Compliance Officer Appointment", 4)
        add_findings_table(doc, [f for f in findings if f["area"] in ("Annual Report", "Annual Review Report", "Compliance Activity", "CCO Activity", "Governance Evidence", "Written Supervisory Procedures")], "Compliance Activity & Reporting", 5)
        add_findings_table(doc, [f for f in findings if "Outstanding" in f["area"]], "Outstanding Recommendations", 6)
    add_summary_table(doc, findings, 7)
    add_remediation_table(doc, findings, 8)
    country = data.get("country", "") or data.get("jurisdiction", "")
    region  = detect_region(data.get("region") or country)
    regional_areas = [f for f in findings if any(k in f["area"] for k in (
        "(US)", "(N.", "SIPC", "SEC", "CFTC", "LATAM",
        "Brazil", "Argentina", "Mexico", "Chile", "Colombia",
        "Hong Kong", "Australia", "Singapore", "Japan", "APAC",
        "EU/Europe", "MiFID", "ESMA", "BaFin",
        "Africa", "FSCA", "Nigeria", "Kenya", "Mauritius", "Egypt", "Ghana",
        "No Unified",
    ))]
    next_sec = 9
    if regional_areas:
        add_findings_table(doc, regional_areas, f"Regional Regulatory Framework — {region}", next_sec)
        next_sec += 1
    add_intel_section(doc, intel, next_sec)
    next_sec += 1
    regional_refs = regional_regulatory_refs(data.get("region", "") or country)
    add_regulatory_refs(doc, [
        ("CASS 1A.3", "CASS (Client Assets Sourcebook) Operational Oversight Function requirement"),
        ("CASS 1A.3.1R", "Named COOF individual"),
        ("CASS 1A.3.3R", "COOF individual skills and expertise"),
        ("CASS 1A.3.4R", "Annual report to governing body"),
        ("CASS 1A.4", "COOF responsibilities"),
        ("FCA Handbook CASS 1A", "https://www.handbook.fca.org.uk/handbook/CASS/1A/"),
    ] + regional_refs, next_sec)
    return doc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", required=True)
    parser.add_argument("--no-scan", action="store_true")
    args = parser.parse_args()
    client_name = args.client.replace(" ", "_")
    data = load_client_data(PREFIX, client_name)
    country = data.get("country", "") or data.get("jurisdiction", "")
    region  = detect_region(data.get("region") or country) if (data.get("region") or country) else None
    intel = {} if args.no_scan else run_perplexity_scan(REPORT_TYPE, region=region, country=country)
    findings = score_checks(data)
    counts = rag_counts(findings)
    print(f"Results: {counts['GREEN']} PASS | {counts['AMBER']} ATTENTION | {counts['RED']} FAIL")
    doc = build_report(data, findings, client_name, intel)
    path = save_report(doc, PREFIX, client_name)
    metrics.inc("report_generated", report_type="cass_oversight")
    print(f"Report saved: {path}")


if __name__ == "__main__":
    main()
