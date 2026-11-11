"""
Executive Protection Report Generator (SM&CR)
Usage: python tools/generate_executive_protection.py --client "<client_name>" [--no-scan]

SENSITIVE: Contains personal data — handle under UK GDPR. Restrict distribution.
"""

import argparse
from datetime import date
from dotenv import load_dotenv
from report_base import *
from regional_routing import detect_region, regional_regulatory_refs

load_dotenv()
REPORT_TYPE = "executive_protection"
PREFIX = "exec_prot"

THREAT_LEVEL_RAG = {"HIGH": "RED", "MEDIUM": "AMBER", "LOW": "GREEN", "UNKNOWN": "AMBER"}


def score_checks(data: dict) -> list:
    findings = []

    # Public profile / exposure
    profile = data.get("public_profile_level", "unknown").lower()
    if profile == "high":
        findings.append({"area": "Threat Exposure", "rule": "NPSA", "description": "Public profile and exposure level", "status": "RED", "commentary": "High public profile — elevated risk of targeted harassment, media attention, and digital threats. Enhanced protective measures required."})
    elif profile == "medium":
        findings.append({"area": "Threat Exposure", "rule": "NPSA", "description": "Public profile and exposure level", "status": "AMBER", "commentary": "Medium public profile. Standard protective measures recommended. Monitor for escalation."})
    else:
        findings.append({"area": "Threat Exposure", "rule": "NPSA", "description": "Public profile and exposure level", "status": "GREEN", "commentary": "Low public profile. Standard security posture adequate."})

    # Known threats / incidents
    known_threats = data.get("known_threats_or_incidents")
    if known_threats:
        findings.append({"area": "Threat Exposure", "rule": "NPSA", "description": "Known threats or security incidents", "status": "RED", "commentary": f"Active threat or prior incident identified: {known_threats}. Immediate protective review required."})
    else:
        findings.append({"area": "Threat Exposure", "rule": "NPSA", "description": "Known threats or security incidents", "status": "GREEN", "commentary": "No known threats or prior incidents reported."})

    # Harassment / protest targeting
    harassment = data.get("harassment_or_protest_targeting")
    if harassment:
        findings.append({"area": "Threat Exposure", "rule": "NPSA", "description": "Harassment or protest targeting", "status": "RED", "commentary": f"Active harassment/protest targeting identified: {harassment}. Review physical security and legal options."})

    # Digital footprint
    digital_concern = data.get("digital_footprint_concerns")
    findings.append({
        "area": "Digital Footprint", "rule": "NPSA / NCSC",
        "description": "Digital footprint and OSINT risk",
        "status": "AMBER" if digital_concern else "GREEN",
        "commentary": f"Digital footprint concerns identified: {digital_concern}. Review exposed personal information and tighten privacy settings." if digital_concern
        else "No significant digital footprint concerns identified. Maintain regular OSINT monitoring.",
    })

    # Travel risk
    travel_freq = data.get("international_travel_frequency", "").lower()
    travel_destinations = data.get("travel_destinations", [])
    high_risk_travel = any(d in ["Russia", "China", "Iran", "Nigeria", "Pakistan", "Afghanistan", "Libya"] for d in travel_destinations)
    if travel_freq in ("frequent", "high") or high_risk_travel:
        findings.append({"area": "Travel Security", "rule": "NPSA", "description": "International travel risk", "status": "RED" if high_risk_travel else "AMBER", "commentary": f"Frequent/high-risk international travel. Destinations include: {', '.join(travel_destinations)}. Pre-travel security briefing and emergency protocol required."})
    elif travel_freq:
        findings.append({"area": "Travel Security", "rule": "NPSA", "description": "International travel risk", "status": "GREEN", "commentary": f"Travel frequency: {travel_freq}. Standard pre-travel briefing recommended."})

    # Home working
    home_working = data.get("home_working")
    if home_working:
        findings.append({"area": "Home & Office Security", "rule": "NCSC", "description": "Home working security", "status": "AMBER", "commentary": "Home working arrangement identified. Ensure home network security, device encryption, and secure document disposal."})

    # Current protective measures
    measures = data.get("protective_measures_in_place", [])
    if not measures:
        findings.append({"area": "Protective Measures", "rule": "NPSA", "description": "Current protective measures in place", "status": "AMBER", "commentary": "No documented protective measures in place. Review personal security posture."})
    else:
        findings.append({"area": "Protective Measures", "rule": "NPSA", "description": "Current protective measures in place", "status": "GREEN", "commentary": f"Protective measures in place: {', '.join(measures)}."})

    # SM&CR accountability risk
    smf_functions = data.get("smf_functions", [])
    if smf_functions:
        findings.append({
            "area": "SM&CR Risk", "rule": "SM&CR",
            "description": f"SM&CR accountability exposure: {', '.join(smf_functions)}",
            "status": "AMBER",
            "commentary": f"Subject holds {', '.join(smf_functions)} function(s). As an FCA-accountable individual, they may be subject to regulatory targeting, whistleblower claims, or media scrutiny. Ensure legal counsel and PR support arrangements are in place.",
        })

    return findings


def build_report(data: dict, findings: list, client_name: str, intel: dict = None) -> Document:
    doc = start_document("Executive Protection Report — RESTRICTED", data, client_name)
    counts = rag_counts(findings)

    doc.add_heading("HANDLING INSTRUCTIONS", level=1)
    doc.add_paragraph(
        "RESTRICTED — This report contains personal data and sensitive security intelligence. "
        "Distribute only to named recipients. Store encrypted. Do not transmit unencrypted. "
        "Handle under UK GDPR."
    ).runs[0].font.bold = True

    doc.add_heading("2. Executive Summary", level=1)
    doc.add_paragraph(
        f"Executive protection assessment for: {data.get('subject_name', 'RESTRICTED')}\n"
        f"Role: {data.get('subject_role', 'N/A')} | SMF: {', '.join(data.get('smf_functions', ['N/A']))}\n"
        f"Assessment: {counts['GREEN']} LOW | {counts['AMBER']} MEDIUM | {counts['RED']} HIGH risk areas"
    )
    if counts["RED"]:
        doc.add_paragraph(f"URGENT: {counts['RED']} high-risk area(s) requiring immediate protective action.").runs[0].font.bold = True

    add_firm_profile(doc, data, client_name, [
        ("Subject", data.get("subject_name", "RESTRICTED")),
        ("Role", data.get("subject_role", "N/A")),
        ("SMF Functions", ", ".join(data.get("smf_functions", ["N/A"]))),
        ("Public Profile Level", data.get("public_profile_level", "N/A").upper()),
    ])

    add_findings_table(doc, [f for f in findings if f["area"] == "Threat Exposure"], "Threat Exposure Assessment", 4)
    add_findings_table(doc, [f for f in findings if f["area"] == "Digital Footprint"], "Digital Footprint & OSINT Risk", 5)
    add_findings_table(doc, [f for f in findings if f["area"] == "Travel Security"], "Travel Security Assessment", 6)
    add_findings_table(doc, [f for f in findings if f["area"] in ("Home & Office Security", "Protective Measures", "SM&CR Risk")], "Security Posture & SM&CR Risk", 7)

    # Recommendations
    doc.add_heading("8. Recommended Protective Measures", level=1)
    recs = [
        ("OSINT Monitoring", "Conduct quarterly OSINT sweeps to identify newly exposed personal information."),
        ("Digital Hygiene", "Review privacy settings on all social media; remove home address from public records."),
        ("Pre-Travel Briefing", "Receive threat briefing before all international travel, especially to elevated-risk jurisdictions."),
        ("Incident Reporting", "Establish clear protocol for reporting threats to security team and FCA if SM&CR-related."),
        ("Legal Counsel", "Ensure rapid access to legal counsel for harassment, media, and regulatory matters."),
        ("Emergency Protocol", "Document and rehearse emergency contact and evacuation procedures."),
    ]
    rec_tbl = doc.add_table(rows=1 + len(recs), cols=2)
    rec_tbl.style = "Table Grid"
    header_cell(rec_tbl.rows[0].cells[0], "Measure")
    header_cell(rec_tbl.rows[0].cells[1], "Detail")
    for i, (m, d) in enumerate(recs):
        rec_tbl.rows[i + 1].cells[0].text = m
        rec_tbl.rows[i + 1].cells[1].text = d

    add_summary_table(doc, findings, 9)
    add_intel_section(doc, intel, 10)
    country = data.get("country", "") or data.get("jurisdiction", "")
    regional_refs = regional_regulatory_refs(data.get("region", "") or country)
    add_regulatory_refs(doc, [
        ("SM&CR", "https://www.fca.org.uk/firms/senior-managers-certification-regime"),
        ("NPSA", "https://www.npsa.gov.uk"),
        ("NCSC Personal Security", "https://www.ncsc.gov.uk/guidance/personal-security"),
        ("CPNI", "https://www.cpni.gov.uk"),
    ] + regional_refs, 11)
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
    print(f"Results: {counts['GREEN']} LOW | {counts['AMBER']} MEDIUM | {counts['RED']} HIGH")
    doc = build_report(data, findings, client_name, intel)
    path = save_report(doc, PREFIX, client_name)
    print(f"Report saved: {path}")


if __name__ == "__main__":
    main()
