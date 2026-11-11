"""
Cyber Threat Assessment Report Generator
Usage: python tools/generate_cyber_threat_assessment.py --client "<client_name>" [--no-scan]
"""

import argparse
from datetime import datetime, date
from dotenv import load_dotenv
from report_base import *
from regional_routing import detect_region, regional_regulatory_refs

load_dotenv()
REPORT_TYPE = "cyber_threat_assessment"
PREFIX = "cyber_ta"


def score_checks(data: dict) -> list:
    findings = []

    # PS21/3 — Important Business Services
    ibs = data.get("ibs_identified")
    findings.append({
        "area": "FCA Operational Resilience", "rule": "PS21/3",
        "description": "Important Business Services (IBS) identified",
        "status": "GREEN" if ibs else "RED",
        "commentary": "IBS identified and documented." if ibs else "IBS not identified. PS21/3 required this by 31 March 2022.",
    })

    # PS21/3 — Impact tolerances
    tolerances = data.get("impact_tolerances_set")
    findings.append({
        "area": "FCA Operational Resilience", "rule": "PS21/3",
        "description": "Impact tolerances set for each IBS",
        "status": "GREEN" if tolerances else "RED",
        "commentary": "Impact tolerances defined for all IBS." if tolerances else "Impact tolerances NOT set. Required under PS21/3.",
    })

    # PS21/3 — Scenario testing
    scenario_tested = data.get("scenario_testing_completed")
    findings.append({
        "area": "FCA Operational Resilience", "rule": "PS21/3",
        "description": "Scenario testing completed against impact tolerances",
        "status": "GREEN" if scenario_tested else "AMBER",
        "commentary": "Scenario testing completed." if scenario_tested else "Scenario testing not completed. Required under PS21/3.",
    })

    # CBEST
    cbest = data.get("cbest_assessment_completed")
    last_cbest = data.get("last_cbest_date")
    if cbest and last_cbest:
        days = (date.today() - datetime.strptime(last_cbest, "%Y-%m-%d").date()).days
        if days > 1095:  # 3 years
            s, c = "AMBER", f"Last CBEST/pen test {days} days ago. Recommend refreshing within 3 years."
        else:
            s, c = "GREEN", f"CBEST/equivalent test completed {last_cbest} ({days} days ago)."
    elif cbest is False:
        s, c = "RED", "No CBEST or equivalent penetration test completed. Required for FCA/PRA in-scope firms."
    else:
        s, c = "AMBER", "CBEST status unknown. Confirm scope and schedule."
    findings.append({"area": "CBEST Testing", "rule": "CBEST", "description": "CBEST or equivalent cyber test completed", "status": s, "commentary": c})

    # MFA
    mfa = data.get("mfa_on_critical_systems")
    findings.append({
        "area": "Cyber Controls", "rule": "FCA SYSC 7",
        "description": "MFA deployed on critical systems",
        "status": "GREEN" if mfa else "RED",
        "commentary": "MFA deployed across critical systems." if mfa else "MFA NOT deployed on critical systems. Critical control gap — immediate remediation required.",
    })

    # PAM
    pam = data.get("privileged_access_management")
    findings.append({
        "area": "Cyber Controls", "rule": "FCA SYSC 7",
        "description": "Privileged access management (PAM) solution in place",
        "status": "GREEN" if pam else "AMBER",
        "commentary": "PAM solution in place." if pam else "No PAM solution identified. Privileged access is a primary attack vector.",
    })

    # Incident response plan
    irp = data.get("cyber_incident_response_plan_exists")
    findings.append({
        "area": "Incident Response", "rule": "FCA SYSC 7",
        "description": "Cyber incident response plan exists",
        "status": "GREEN" if irp else "RED",
        "commentary": "Cyber incident response plan in place." if irp else "No cyber incident response plan. Required for operational resilience.",
    })

    # IRP tested
    irp_tested = data.get("cyber_response_plan_tested")
    findings.append({
        "area": "Incident Response", "rule": "PS21/3",
        "description": "Incident response plan tested in last 12 months",
        "status": "GREEN" if irp_tested else "AMBER",
        "commentary": "Incident response plan tested." if irp_tested else "Incident response plan not tested in last 12 months. Regular testing required.",
    })

    # Third-party cyber risk
    tp_assessed = data.get("third_party_cyber_risk_assessed")
    findings.append({
        "area": "Third-Party Risk", "rule": "PS21/3",
        "description": "Third-party/supplier cyber risk assessed",
        "status": "GREEN" if tp_assessed else "RED",
        "commentary": "Third-party cyber risk assessments conducted." if tp_assessed else "No third-party cyber risk assessment. Supply chain attacks are a top threat vector.",
    })

    return findings


def build_report(data: dict, findings: list, client_name: str, intel: dict = None) -> Document:
    doc = start_document("Cyber Threat Assessment", data, client_name)
    counts = rag_counts(findings)
    doc.add_heading("2. Executive Summary", level=1)
    doc.add_paragraph(
        f"Cyber threat and operational resilience assessment for {data.get('firm_name', client_name)}. "
        f"{len(findings)} controls assessed: {counts['GREEN']} PASS | {counts['AMBER']} ATTENTION | {counts['RED']} FAIL."
    )
    if counts["RED"]:
        doc.add_paragraph(f"CRITICAL: {counts['RED']} cyber control failure(s) identified.").runs[0].font.bold = True

    add_firm_profile(doc, data, client_name)
    add_findings_table(doc, [f for f in findings if f["area"] == "FCA Operational Resilience"], "FCA Operational Resilience (PS21/3)", 4)
    add_findings_table(doc, [f for f in findings if f["area"] == "CBEST Testing"], "CBEST Cyber Testing", 5)
    add_findings_table(doc, [f for f in findings if f["area"] == "Cyber Controls"], "Cyber Controls Assessment", 6)
    add_findings_table(doc, [f for f in findings if f["area"] == "Third-Party Risk"], "Third-Party & Supply Chain Risk", 7)
    add_findings_table(doc, [f for f in findings if f["area"] == "Incident Response"], "Incident Response Readiness", 8)
    add_summary_table(doc, findings, 9)
    add_remediation_table(doc, findings, 10)
    add_intel_section(doc, intel, 11)
    country = data.get("country", "") or data.get("jurisdiction", "")
    regional_refs = regional_regulatory_refs(data.get("region", "") or country)
    add_regulatory_refs(doc, [
        ("FCA PS21/3", "Operational resilience — impact tolerances and scenario testing"),
        ("CBEST", "https://www.bankofengland.co.uk/financial-stability/financial-sector-continuity/cbest"),
        ("FCA SYSC 7", "Systems and controls — IT and cyber security"),
        ("DORA", "Digital Operational Resilience Act (EU operations)"),
        ("FCA Operational Resilience", "https://www.fca.org.uk/firms/operational-resilience"),
    ] + regional_refs, 12)
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
    print(f"Report saved: {path}")


if __name__ == "__main__":
    main()
