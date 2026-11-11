"""
Physical Security Audit Report Generator
Usage: python tools/generate_physical_security_audit.py --client "<client_name>" [--no-scan]
"""

import argparse
from datetime import datetime, date
from dotenv import load_dotenv
from report_base import *
from regional_routing import detect_region, regional_regulatory_refs

load_dotenv()
REPORT_TYPE = "physical_security_audit"
PREFIX = "phys_audit"


def score_checks(data: dict) -> list:
    findings = []
    premises_type = data.get("premises_type", "premises").lower()
    is_sensitive = any(t in premises_type for t in ("data centre", "vault", "server", "cash"))

    # Access control
    access_control = data.get("access_control_in_place")
    access_type = data.get("access_control_type", "unknown")
    findings.append({
        "area": "Access Control", "rule": "NPSA / FCA SYSC",
        "description": "Physical access control system",
        "status": "GREEN" if access_control else ("RED" if is_sensitive else "AMBER"),
        "commentary": f"Access control in place: {access_type}." if access_control
        else f"No access control on {premises_type}. {'CRITICAL for sensitive premises.' if is_sensitive else 'Recommend installation.'} ",
    })

    # CCTV
    cctv = data.get("cctv_coverage")
    cctv_areas = data.get("cctv_areas_covered", "")
    findings.append({
        "area": "CCTV & Surveillance", "rule": "NPSA",
        "description": "CCTV coverage",
        "status": "GREEN" if cctv else ("RED" if is_sensitive else "AMBER"),
        "commentary": f"CCTV in place. Areas covered: {cctv_areas}." if cctv else f"No CCTV. {'Critical gap for {premises_type}.' if is_sensitive else 'Recommend installation for key areas.'}",
    })

    # Intruder alarm
    alarm = data.get("intruder_alarm")
    alarm_standard = data.get("alarm_standard", "")
    findings.append({
        "area": "CCTV & Surveillance", "rule": "PD 6662",
        "description": "Intruder alarm system",
        "status": "GREEN" if alarm else ("RED" if is_sensitive else "AMBER"),
        "commentary": f"Intruder alarm in place{f' ({alarm_standard})' if alarm_standard else ''}." if alarm else "No intruder alarm system. PD 6662 compliant system recommended.",
    })

    # Security personnel
    security_personnel = data.get("security_personnel_on_site")
    security_hours = data.get("security_hours", "unknown")
    findings.append({
        "area": "Security Personnel", "rule": "NPSA",
        "description": "Security personnel on site",
        "status": "GREEN" if security_personnel else "AMBER",
        "commentary": f"Security personnel on site: {security_hours}." if security_personnel else "No on-site security personnel. Consider manned guarding for sensitive areas.",
    })

    # Perimeter
    perimeter = data.get("perimeter_security")
    findings.append({
        "area": "Perimeter Security", "rule": "NPSA / CPNI",
        "description": "Physical perimeter security (fencing, barriers, lighting)",
        "status": "GREEN" if perimeter else "AMBER",
        "commentary": "Perimeter security in place (fencing/barriers/lighting)." if perimeter else "Perimeter security not confirmed. Review external boundaries, lighting, and vehicle barriers.",
    })

    # Visitor management
    visitor_mgmt = data.get("visitor_management_process")
    findings.append({
        "area": "Visitor & Document Management", "rule": "NPSA",
        "description": "Visitor management process",
        "status": "GREEN" if visitor_mgmt else "AMBER",
        "commentary": "Visitor management process in place (sign-in, escorted access)." if visitor_mgmt else "No visitor management process. Implement sign-in and escort procedures.",
    })

    # Secure document disposal
    doc_disposal = data.get("secure_document_disposal")
    findings.append({
        "area": "Visitor & Document Management", "rule": "UK GDPR / FCA SYSC",
        "description": "Secure document and media disposal",
        "status": "GREEN" if doc_disposal else "RED",
        "commentary": "Secure document/media disposal process in place." if doc_disposal else "No secure disposal process. Unshredded documents/media risk data breach and FCA/ICO action.",
    })

    # Business continuity for premises
    bcp = data.get("business_continuity_plan_for_premises")
    findings.append({
        "area": "FCA Operational Resilience", "rule": "PS21/3",
        "description": "Business continuity plan covering premises failure",
        "status": "GREEN" if bcp else "RED",
        "commentary": "Business continuity plan covers premises failure scenarios." if bcp else "No BCP for premises failure. Required under FCA PS21/3 operational resilience.",
    })

    # Last security review
    last_review = data.get("last_physical_security_review_date")
    if last_review:
        days = (date.today() - datetime.strptime(last_review, "%Y-%m-%d").date()).days
        if days > 365:
            s, c = "AMBER", f"Last security review {days} days ago. Annual review recommended."
        else:
            s, c = "GREEN", f"Security review conducted {last_review} ({days} days ago)."
    else:
        s, c = "AMBER", "No security review date on record. Annual physical security review recommended."
    findings.append({"area": "FCA Operational Resilience", "rule": "PS21/3", "description": "Annual physical security review", "status": s, "commentary": c})

    # Prior incidents
    prior_incidents = data.get("prior_incidents")
    if prior_incidents:
        remediated = data.get("prior_incidents_remediated")
        findings.append({
            "area": "Incident History", "rule": "FCA SYSC",
            "description": "Prior security incidents remediated",
            "status": "GREEN" if remediated else "RED",
            "commentary": f"Prior incidents remediated: {prior_incidents}." if remediated else f"Prior incident(s) NOT fully remediated: {prior_incidents}. Immediate action required.",
        })
    else:
        findings.append({"area": "Incident History", "rule": "FCA SYSC", "description": "Prior security incidents", "status": "GREEN", "commentary": "No prior security incidents reported."})

    return findings


def build_report(data: dict, findings: list, client_name: str, intel: dict = None) -> Document:
    doc = start_document("Physical Security Audit Report", data, client_name)
    counts = rag_counts(findings)

    doc.add_heading("2. Executive Summary", level=1)
    doc.add_paragraph(
        f"Physical security audit: {data.get('premises_type', 'premises')} at {data.get('address', 'N/A')}\n"
        f"Firm: {data.get('firm_name', client_name)}\n"
        f"Checks: {counts['GREEN']} PASS | {counts['AMBER']} REQUIRES ATTENTION | {counts['RED']} FAIL"
    )
    if counts["RED"]:
        doc.add_paragraph(f"CRITICAL: {counts['RED']} physical security failure(s). Remediate immediately.").runs[0].font.bold = True

    add_firm_profile(doc, data, client_name, [
        ("Premises Type", data.get("premises_type", "N/A")),
        ("Address", data.get("address", "N/A")),
    ])

    add_findings_table(doc, [f for f in findings if f["area"] in ("Access Control", "Perimeter Security")], "Perimeter & Access Control", 4)
    add_findings_table(doc, [f for f in findings if f["area"] == "CCTV & Surveillance"], "CCTV & Alarm Systems", 5)
    add_findings_table(doc, [f for f in findings if f["area"] == "Security Personnel"], "Security Personnel", 6)
    add_findings_table(doc, [f for f in findings if f["area"] == "Visitor & Document Management"], "Visitor & Document Management", 7)
    add_findings_table(doc, [f for f in findings if f["area"] in ("FCA Operational Resilience", "Incident History")], "FCA Operational Resilience & Incident History", 8)
    add_summary_table(doc, findings, 9)
    add_remediation_table(doc, findings, 10)
    add_intel_section(doc, intel, 11)
    country = data.get("country", "") or data.get("jurisdiction", "")
    regional_refs = regional_regulatory_refs(data.get("region", "") or country)
    add_regulatory_refs(doc, [
        ("FCA PS21/3", "Operational resilience requirements"),
        ("NPSA", "https://www.npsa.gov.uk"),
        ("CPNI", "https://www.cpni.gov.uk"),
        ("PD 6662", "UK standard for intruder alarm systems"),
        ("BS EN 1047", "Security containers and strongrooms"),
        ("FCA SYSC 8", "Outsourcing and premises controls"),
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
