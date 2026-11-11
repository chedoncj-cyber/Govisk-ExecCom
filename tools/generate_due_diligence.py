"""
Due Diligence Report Generator (FCA Fit & Proper / SM&CR / CASS third-party)
Usage: python tools/generate_due_diligence.py --client "<client_name>" [--no-scan]
"""

import argparse
from datetime import date
from dotenv import load_dotenv
from report_base import *
from regional_routing import detect_region, regional_regulatory_refs

load_dotenv()
REPORT_TYPE = "due_diligence"
PREFIX = "dd"


def score_checks(data: dict) -> list:
    findings = []
    subject_type = data.get("subject_type", "individual").lower()
    purpose = data.get("purpose", "").lower()

    # FCA Register status
    fca_registered = data.get("fca_registered")
    fca_frn = data.get("fca_frn_or_irn", "N/A")
    if fca_registered is True:
        findings.append({"area": "FCA Registration", "rule": "FIT 1.3 / FCA Register", "description": "FCA registered/authorised status", "status": "GREEN", "commentary": f"Confirmed on FCA Register. FRN/IRN: {fca_frn}."})
    elif fca_registered is False:
        required = data.get("fca_registration_required", False)
        findings.append({
            "area": "FCA Registration", "rule": "FIT 1.3",
            "description": "FCA registered/authorised status",
            "status": "RED" if required else "AMBER",
            "commentary": "NOT on FCA Register. FCA authorisation required for this role/activity." if required else "Not on FCA Register. Confirm whether authorisation is required for this engagement.",
        })
    else:
        findings.append({"area": "FCA Registration", "rule": "FIT 1.3", "description": "FCA registration confirmed", "status": "AMBER", "commentary": "FCA Register status not verified. Manual check required at register.fca.org.uk."})

    # Regulatory history — bans
    active_ban = data.get("active_fca_ban_or_prohibition")
    findings.append({
        "area": "Regulatory History", "rule": "FIT 1.3.2G",
        "description": "No active FCA prohibition/ban order",
        "status": "RED" if active_ban else "GREEN",
        "commentary": f"ACTIVE FCA BAN OR PROHIBITION ORDER. Subject must not be approved for regulated activity." if active_ban else "No active FCA prohibition or ban order identified.",
    })

    # Regulatory history — prior actions
    prior_actions = data.get("prior_regulatory_actions")
    if prior_actions:
        findings.append({"area": "Regulatory History", "rule": "FIT 1.3.2G", "description": "Prior regulatory actions", "status": "AMBER", "commentary": f"Prior regulatory actions identified: {prior_actions}. Review materiality and disclosure."})
    else:
        findings.append({"area": "Regulatory History", "rule": "FIT 1.3.2G", "description": "Prior regulatory actions", "status": "GREEN", "commentary": "No prior regulatory actions identified."})

    # Criminal convictions
    criminal = data.get("criminal_convictions")
    findings.append({
        "area": "Regulatory History", "rule": "FIT 1.3.2G",
        "description": "Criminal convictions check",
        "status": "RED" if criminal else "GREEN",
        "commentary": f"Criminal conviction(s) identified: {criminal}. Fails FIT 1.3 honesty and integrity test." if criminal else "No criminal convictions identified.",
    })

    # Sanctions screening
    sanctions_match = data.get("sanctions_match")
    findings.append({
        "area": "Sanctions Screening", "rule": "OFSI / OFAC",
        "description": "OFSI/OFAC sanctions screening",
        "status": "RED" if sanctions_match else "GREEN",
        "commentary": f"SANCTIONS MATCH identified: {sanctions_match}. Do not proceed — report to compliance immediately." if sanctions_match else "No sanctions match identified on OFSI/OFAC consolidated lists.",
    })

    # Financial soundness
    ccj = data.get("ccjs_or_bankruptcy")
    findings.append({
        "area": "Financial Soundness", "rule": "FIT 1.3.4G",
        "description": "No outstanding CCJs or insolvency",
        "status": "RED" if ccj else "GREEN",
        "commentary": f"Outstanding CCJs or insolvency proceedings identified: {ccj}. Fails FIT 1.3.4G financial soundness test." if ccj else "No CCJs or insolvency proceedings identified.",
    })

    # Qualifications / competence
    qualified = data.get("professional_qualifications_verified")
    findings.append({
        "area": "Competence", "rule": "FIT 1.3.3G / SM&CR",
        "description": "Professional qualifications verified",
        "status": "GREEN" if qualified else "AMBER",
        "commentary": "Professional qualifications verified." if qualified else "Professional qualifications not yet verified. Required for SM&CR certification under FCA COCON.",
    })

    # CASS third-party (if applicable)
    if "cass" in purpose:
        fca_authorised_supplier = data.get("supplier_fca_authorised")
        findings.append({
            "area": "CASS Third-Party", "rule": "CASS 6.3 / CASS 7.13",
            "description": "CASS supplier is FCA authorised",
            "status": "GREEN" if fca_authorised_supplier else "RED",
            "commentary": "CASS supplier confirmed FCA authorised." if fca_authorised_supplier else "CASS supplier NOT FCA authorised. Cannot be used as CASS custodian/agent without authorisation.",
        })
        written_agreement = data.get("written_agreement_in_place")
        findings.append({
            "area": "CASS Third-Party", "rule": "CASS 6.3 / CASS 7.13",
            "description": "Written agreement with CASS supplier",
            "status": "GREEN" if written_agreement else "RED",
            "commentary": "Written agreement in place." if written_agreement else "No written agreement. Required under CASS 6.3 / CASS 7.13 before appointing third-party.",
        })

    return findings


def overall_verdict(findings: list) -> str:
    statuses = [f["status"] for f in findings]
    if "RED" in statuses:
        return "FAIL — Subject does not meet FCA Fit & Proper requirements. Do not approve."
    elif "AMBER" in statuses:
        return "CONDITIONAL — Further verification required before approval."
    else:
        return "PASS — Subject meets FCA Fit & Proper requirements based on information provided."


def build_report(data: dict, findings: list, client_name: str, intel: dict = None) -> Document:
    doc = start_document("Due Diligence Report", data, client_name)
    counts = rag_counts(findings)
    verdict = overall_verdict(findings)

    doc.add_heading("2. Executive Summary", level=1)
    doc.add_paragraph(
        f"Due diligence assessment: {data.get('subject_name', 'N/A')} ({data.get('subject_type', 'N/A')})\n"
        f"Purpose: {data.get('purpose', 'N/A')}\n"
        f"Checks: {counts['GREEN']} PASS | {counts['AMBER']} ATTENTION | {counts['RED']} FAIL\n"
        f"Overall verdict: {verdict}"
    )
    if counts["RED"]:
        doc.add_paragraph(f"CRITICAL FAILURE: Do not approve. {counts['RED']} red flag(s) identified.").runs[0].font.bold = True

    add_firm_profile(doc, data, client_name, [
        ("Subject Name", data.get("subject_name", "N/A")),
        ("Subject Type", data.get("subject_type", "N/A")),
        ("Purpose", data.get("purpose", "N/A")),
        ("FRN/IRN", data.get("fca_frn_or_irn", "N/A")),
    ])

    add_findings_table(doc, [f for f in findings if f["area"] in ("FCA Registration", "Regulatory History", "Sanctions Screening")], "FCA & Regulatory Assessment", 4)
    add_findings_table(doc, [f for f in findings if f["area"] in ("Financial Soundness", "Competence")], "Financial Soundness & Competence", 5)
    cass_findings = [f for f in findings if f["area"] == "CASS Third-Party"]
    if cass_findings:
        add_findings_table(doc, cass_findings, "CASS Third-Party Assessment", 6)

    add_summary_table(doc, findings, 7)
    add_remediation_table(doc, findings, 8)
    add_intel_section(doc, intel, 9)
    country = data.get("country", "") or data.get("jurisdiction", "")
    regional_refs = regional_regulatory_refs(data.get("region", "") or country)
    add_regulatory_refs(doc, [
        ("FIT 1.3", "FCA Fit and Proper test — honesty, integrity, competence"),
        ("SM&CR", "Senior Manager & Certification Regime"),
        ("CASS 6.3", "Third-party custodian due diligence"),
        ("CASS 7.13", "Third-party client money agent due diligence"),
        ("FCA Register", "https://register.fca.org.uk"),
        ("FCA Handbook FIT", "https://www.handbook.fca.org.uk/handbook/FIT/"),
    ] + regional_refs, 10)
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
    print(f"Verdict: {overall_verdict(findings)}")
    doc = build_report(data, findings, client_name, intel)
    path = save_report(doc, PREFIX, client_name)
    print(f"Report saved: {path}")


if __name__ == "__main__":
    main()
