"""
Threat Intelligence Report Generator — Banking Sector
Usage: python tools/generate_threat_intelligence_banking.py --client "<client_name>" [--no-scan]
"""

import argparse
from datetime import date
from dotenv import load_dotenv
from report_base import *
from regional_routing import detect_region, regional_regulatory_refs

load_dotenv()
REPORT_TYPE = "threat_intelligence_banking"
PREFIX = "threat_intel"

THREAT_CATEGORIES = [
    ("Authorised Push Payment (APP) Fraud", "HIGH", "PSR reimbursement rules increase sector exposure. Banks must demonstrate robust detection and reimbursement processes."),
    ("Trade Finance Fraud", "MEDIUM", "Documentary fraud and letter of credit manipulation remain persistent threats in trade finance divisions."),
    ("Insider Threat", "HIGH", "Privileged access misuse and data exfiltration by employees or contractors targeting client assets and data."),
    ("Sanctions Evasion", "HIGH", "Complex ownership structures and high-risk jurisdiction routing used to evade OFSI/OFAC sanctions screening."),
    ("Crypto-related Financial Crime", "MEDIUM", "Conversion of illicit funds via crypto on/off ramps. FCA expects enhanced monitoring of crypto-related flows."),
    ("Account Takeover / Social Engineering", "HIGH", "Credential theft and social engineering targeting both retail and private banking clients."),
    ("FCA Supervisory Risk", "MEDIUM", "Current FCA priority areas include consumer duty, operational resilience, and financial crime controls."),
]

SEVERITY_RAG = {"HIGH": "RED", "MEDIUM": "AMBER", "LOW": "GREEN"}


def score_threats(data: dict) -> list:
    findings = []
    business_lines = data.get("business_lines", [])
    geo = data.get("geographic_footprint", "UK")

    for category, severity, base_commentary in THREAT_CATEGORIES:
        commentary = base_commentary
        # Elevate sanctions risk for international firms
        if "Sanctions" in category and "international" in geo.lower():
            severity = "HIGH"
            commentary += " International footprint increases sanctions evasion exposure."
        # Elevate crypto risk if crypto-related business lines
        if "Crypto" in category and any("crypto" in bl.lower() for bl in business_lines):
            severity = "HIGH"
            commentary += " Crypto-related business lines identified — enhanced monitoring required."

        findings.append({
            "area": "Threat Assessment",
            "rule": "FCA FCG",
            "description": category,
            "status": SEVERITY_RAG.get(severity, "AMBER"),
            "commentary": commentary,
        })
    return findings


def build_report(data: dict, findings: list, client_name: str, intel: dict = None) -> Document:
    doc = start_document("Banking Sector Threat Intelligence Report", data, client_name)
    counts = rag_counts(findings)

    doc.add_heading("2. Executive Summary", level=1)
    doc.add_paragraph(
        f"Threat intelligence assessment for {data.get('firm_name', client_name)}. "
        f"Assessment period: {data.get('assessment_period', 'Current')}. "
        f"{counts['RED']} HIGH | {counts['AMBER']} MEDIUM | {counts['GREEN']} LOW threat categories identified."
    )
    doc.add_paragraph(
        "This report is intelligence-led and draws on live web sources via Routing Intelligence Scan. "
        "Findings should be reviewed by a qualified analyst and supplemented with NCA/UKFIU intelligence where available."
    ).runs[0].font.italic = True

    add_firm_profile(doc, data, client_name, [
        ("Business Lines", ", ".join(data.get("business_lines", ["Not specified"]))),
        ("Geographic Footprint", data.get("geographic_footprint", "N/A")),
    ])

    add_findings_table(doc, findings, "Threat Assessment by Category", 4)

    # Mitigations section
    doc.add_heading("5. Recommended Mitigations", level=1)
    mitigations = [
        ("APP Fraud", "Implement PSR reimbursement procedures; deploy transaction monitoring rules for APP fraud patterns."),
        ("Insider Threat", "Conduct periodic privileged access reviews; implement user behaviour analytics (UEBA)."),
        ("Sanctions Evasion", "Enhance beneficial ownership checks; screen against OFSI/OFAC consolidated lists daily."),
        ("Account Takeover", "Deploy multi-factor authentication; monitor for unusual login patterns and device changes."),
        ("Crypto Crime", "Screen crypto addresses against on-chain analytics tools; file SARs for suspicious crypto activity."),
        ("FCA Supervisory", "Review Consumer Duty implementation; ensure operational resilience plans meet PS21/3 requirements."),
    ]
    mit_tbl = doc.add_table(rows=1 + len(mitigations), cols=2)
    mit_tbl.style = "Table Grid"
    header_cell(mit_tbl.rows[0].cells[0], "Threat Category")
    header_cell(mit_tbl.rows[0].cells[1], "Recommended Mitigation")
    for i, (cat, mit) in enumerate(mitigations):
        mit_tbl.rows[i + 1].cells[0].text = cat
        mit_tbl.rows[i + 1].cells[1].text = mit

    add_intel_section(doc, intel, 6)
    country = data.get("country", "") or data.get("jurisdiction", "") or data.get("geographic_footprint", "")
    regional_refs = regional_regulatory_refs(data.get("region", "") or country)
    add_regulatory_refs(doc, [
        ("FCA Financial Crime Guide (FCG)", "https://www.handbook.fca.org.uk/handbook/FCG/"),
        ("JMLSG Guidance", "https://www.jmlsg.org.uk"),
        ("NCA Intelligence", "https://www.nationalcrimeagency.gov.uk/what-we-do/crime-threats/financial-crime"),
        ("OFSI Sanctions", "https://www.gov.uk/government/organisations/office-of-financial-sanctions-implementation"),
        ("PSR APP Fraud Rules", "https://www.psr.org.uk/our-work/app-scams/"),
    ] + regional_refs, 7)
    return doc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", required=True)
    parser.add_argument("--no-scan", action="store_true")
    args = parser.parse_args()
    client_name = args.client.replace(" ", "_")
    data = load_client_data(PREFIX, client_name)
    country = data.get("country", "") or data.get("jurisdiction", "") or data.get("geographic_footprint", "")
    region  = detect_region(data.get("region") or country) if (data.get("region") or country) else None
    intel = {} if args.no_scan else run_perplexity_scan(REPORT_TYPE, region=region, country=country)
    findings = score_threats(data)
    counts = rag_counts(findings)
    print(f"Threats: {counts['RED']} HIGH | {counts['AMBER']} MEDIUM | {counts['GREEN']} LOW")
    doc = build_report(data, findings, client_name, intel)
    path = save_report(doc, PREFIX, client_name)
    print(f"Report saved: {path}")


if __name__ == "__main__":
    main()
