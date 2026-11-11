"""
CASS Resolution Pack Readiness Report Generator (CASS 10)
Usage: python tools/generate_cass_resolution_pack.py --client "<client_name>" [--no-scan]
"""

import argparse
import sys
from datetime import datetime, date
from pathlib import Path
from dotenv import load_dotenv
from report_base import *
from regional_routing import detect_region, score_regional_client_money, regional_regulatory_refs
from regional_cass_equivalents import score_regional_resolution_pack, RESOLUTION_PACK_TITLES

load_dotenv()

# ── Shared observability ───────────────────────────────────────────────────────
_SHARED = Path(__file__).parent.parent.parent / "shared"
sys.path.insert(0, str(_SHARED))
from observability import get_logger, metrics, trace_op

REPORT_TYPE = "cass_resolution_pack"
PREFIX = "cass_rp"

_RP_SLUGS = {
    "north-america": "N. America", "latin-america": "Latin America",
    "asia-pacific": "Asia Pacific", "europe": "Europe", "africa": "Africa",
}


@trace_op("score_resolution_pack")
def score_checks(data: dict) -> list:
    _r = _RP_SLUGS.get((data.get("region") or "").strip().lower())
    if _r:
        return score_regional_resolution_pack(data, _r)

    findings = []

    # CRP existence
    crp_exists = data.get("crp_document_exists")
    findings.append({
        "area": "CRP Existence", "rule": "CASS 10.1",
        "description": "Formal CRP document exists",
        "status": "GREEN" if crp_exists else "RED",
        "commentary": "CRP document confirmed." if crp_exists else "No CRP document exists. Immediate creation required under CASS 10.1.",
    })

    # 48-hour accessibility
    accessible = data.get("crp_accessible_48hrs")
    if accessible is True:
        s, c = "GREEN", "CRP accessible within 48-hour requirement (CASS 10.2.3R)."
    elif accessible is False:
        s, c = "RED", "CRP NOT accessible within 48 hours. Insolvency practitioner cannot fulfil obligations — CASS 10.2.3R breach."
    else:
        s, c = "AMBER", "48-hour accessibility not confirmed. Testing required."
    findings.append({"area": "CRP Accessibility", "rule": "CASS 10.2.3R", "description": "Pack accessible within 48 hours", "status": s, "commentary": c})

    # Named responsible individual
    named = data.get("crp_responsible_individual")
    findings.append({
        "area": "CRP Ownership", "rule": "CASS 10.2",
        "description": "Named individual responsible for CRP",
        "status": "GREEN" if named else "AMBER",
        "commentary": f"Responsible individual: {named}." if named else "No named individual. Assign responsibility under CASS 10.2.",
    })

    # Contents checks
    contents = {
        "client_asset_schedule": ("CASS 10.2.2R", "Client asset schedule included"),
        "acknowledgement_letters": ("CASS 10.2.2R", "Acknowledgement letters included"),
        "reconciliation_records": ("CASS 10.2.2R", "Reconciliation records included"),
        "system_access_credentials": ("CASS 10.2.2R", "System access credentials included"),
    }
    for key, (rule, desc) in contents.items():
        present = data.get(key)
        findings.append({
            "area": "CRP Contents", "rule": rule, "description": desc,
            "status": "GREEN" if present else ("RED" if key in ("client_asset_schedule", "acknowledgement_letters") else "AMBER"),
            "commentary": "Confirmed present." if present else f"MISSING from CRP. Required under {rule}.",
        })

    # Annual review
    last_review = data.get("crp_last_review_date")
    if last_review:
        days = (date.today() - datetime.strptime(last_review, "%Y-%m-%d").date()).days
        if days > 365:
            s, c = "RED", f"Last review {days} days ago. Annual review required under CASS 10.3."
        else:
            s, c = "GREEN", f"CRP reviewed within last 12 months ({last_review})."
    else:
        s, c = "RED", "No review date on record. Annual review required under CASS 10.3."
    findings.append({"area": "Annual Review", "rule": "CASS 10.3", "description": "CRP reviewed in last 12 months", "status": s, "commentary": c})

    # Testing
    tested = data.get("crp_tested")
    last_test = data.get("crp_last_test_date", "unknown")
    findings.append({
        "area": "CRP Testing", "rule": "CASS 10.3",
        "description": "CRP dry-run tested",
        "status": "GREEN" if tested else "AMBER",
        "commentary": f"CRP tested. Last test: {last_test}." if tested else "CRP has not been tested. Dry-run recommended to validate 48-hour access.",
    })

    # Secure storage
    secure = data.get("crp_secure_offsite_storage")
    findings.append({
        "area": "CRP Storage", "rule": "CASS 10.2",
        "description": "Secure and off-site/cloud accessible storage",
        "status": "GREEN" if secure else "AMBER",
        "commentary": "Secure off-site/cloud storage confirmed." if secure else "Storage not confirmed as secure/off-site. Review continuity risk.",
    })

    regional_findings = score_regional_client_money(data)
    findings.extend(regional_findings)
    return findings


@trace_op("build_resolution_pack_report")
def build_report(data: dict, findings: list, client_name: str, intel: dict = None) -> Document:
    slug = (data.get("region") or "").strip().lower()
    _r = _RP_SLUGS.get(slug, "UK")
    _title = RESOLUTION_PACK_TITLES.get(_r, RESOLUTION_PACK_TITLES["UK"])
    doc = start_document(_title, data, client_name)
    counts = rag_counts(findings)

    doc.add_heading("2. Executive Summary", level=1)
    if _r == "UK":
        doc.add_paragraph(
            f"This report assesses readiness of the firm's CASS Resolution Pack under FCA CASS 10. "
            f"Assessed {len(findings)} control areas: {counts['GREEN']} PASS | {counts['AMBER']} REQUIRES ATTENTION | {counts['RED']} FAIL."
        )
    else:
        doc.add_paragraph(
            f"This report assesses client asset return readiness for {data.get('firm_name', client_name)} "
            f"under applicable {_r} regulatory requirements. "
            f"Assessed {len(findings)} control areas: {counts['GREEN']} PASS | {counts['AMBER']} REQUIRES ATTENTION | {counts['RED']} FAIL."
        )
    if counts["RED"]:
        p = doc.add_paragraph(f"IMMEDIATE ACTION: {counts['RED']} critical failure(s). A deficient resolution plan exposes clients to harm in insolvency scenarios.")
        p.runs[0].font.bold = True

    add_firm_profile(doc, data, client_name)
    if _r == "UK":
        add_findings_table(doc, [f for f in findings if f["area"] in ("CRP Existence", "CRP Accessibility", "CRP Ownership")], "CRP Existence & Accessibility", 4)
        add_findings_table(doc, [f for f in findings if f["area"] == "CRP Contents"], "CRP Contents Assessment", 5)
        add_findings_table(doc, [f for f in findings if f["area"] in ("Annual Review", "CRP Testing", "CRP Storage")], "Review, Testing & Storage", 6)
    else:
        add_findings_table(doc, findings, "Client Asset Return Readiness Findings", 4)
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
        ("CASS 10.1", "Obligation to maintain a CASS (Client Assets Sourcebook) resolution pack"),
        ("CASS 10.2", "Required contents of the resolution pack"),
        ("CASS 10.2.3R", "48-hour accessibility requirement"),
        ("CASS 10.3", "Annual review requirement"),
        ("FCA Handbook", "https://www.handbook.fca.org.uk/handbook/CASS/10/"),
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
    metrics.inc("report_generated", report_type="cass_resolution_pack")
    print(f"Report saved: {path}")


if __name__ == "__main__":
    main()
