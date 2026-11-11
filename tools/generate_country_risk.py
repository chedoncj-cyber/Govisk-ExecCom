"""
Country Risk Report Generator
Usage: python tools/generate_country_risk.py --client "<client_name>" [--no-scan]
"""

import argparse
from datetime import date
from dotenv import load_dotenv
from report_base import *
from regional_routing import (
    detect_region,
    score_regional_cross_border,
    regional_regulatory_refs,
)

load_dotenv()
REPORT_TYPE = "country_risk"
PREFIX = "country_risk"

# FATF blacklisted countries (as of 2026 — update annually)
FATF_BLACK_LIST = ["North Korea", "Iran", "Myanmar"]

# FATF grey list (frequently updated — use Perplexity scan to supplement)
FATF_GREY_LIST = [
    "Bulgaria", "Burkina Faso", "Cameroon", "Croatia", "Democratic Republic of Congo",
    "Haiti", "Jamaica", "Kenya", "Mali", "Mozambique", "Namibia", "Nigeria",
    "Philippines", "Senegal", "South Africa", "Syria", "Tanzania", "Venezuela",
    "Vietnam", "Yemen",
]

# Active UK sanctions regimes (high-level — verify with OFSI)
SANCTIONS_COUNTRIES = [
    "Russia", "Belarus", "Iran", "North Korea", "Syria", "Myanmar", "Sudan",
    "Somalia", "Libya", "Venezuela", "Cuba", "Zimbabwe",
]


def score_country(data: dict) -> list:
    findings = []
    country = data.get("country", "Unknown")
    purpose = data.get("purpose", "")

    # OFSI sanctions check
    sanctioned = country in SANCTIONS_COUNTRIES or data.get("sanctions_applicable")
    findings.append({
        "area": "Sanctions", "rule": "OFSI / OFAC",
        "description": f"Sanctions assessment: {country}",
        "status": "RED" if sanctioned else "GREEN",
        "commentary": f"{country} is subject to UK/US financial sanctions. Transactions require OFSI/OFAC licence. Do not proceed without legal advice." if sanctioned
        else f"No active UK/US sanctions regime identified for {country}. Verify directly with OFSI before transacting.",
    })

    # FATF status
    if country in FATF_BLACK_LIST:
        fatf_status, fatf_commentary = "RED", f"{country} is on the FATF black list (non-compliant jurisdictions). Enhanced due diligence mandatory under UK MLTF Regulations 2017 Regulation 33."
    elif country in FATF_GREY_LIST or data.get("fatf_grey_list"):
        fatf_status, fatf_commentary = "AMBER", f"{country} is on the FATF grey list (increased monitoring). Enhanced due diligence required."
    else:
        fatf_status, fatf_commentary = "GREEN", f"{country} not identified on FATF black or grey list. Standard AML/CFT controls apply."
    findings.append({"area": "FATF / AML Risk", "rule": "FATF / UK MLTF Reg 33", "description": f"FATF status: {country}", "status": fatf_status, "commentary": fatf_commentary})

    # Corruption / political risk
    cpi_score = data.get("corruption_perceptions_index_score")
    if cpi_score is not None:
        if cpi_score < 30:
            cp_status = "RED"
            cp_comment = f"CPI score: {cpi_score}/100. Highly corrupt jurisdiction — elevated financial crime risk."
        elif cpi_score < 50:
            cp_status = "AMBER"
            cp_comment = f"CPI score: {cpi_score}/100. Elevated corruption risk. Enhanced controls recommended."
        else:
            cp_status = "GREEN"
            cp_comment = f"CPI score: {cpi_score}/100. Acceptable corruption risk level."
    else:
        cp_status = "AMBER"
        cp_comment = "Corruption Perceptions Index score not provided. Review Transparency International data."
    findings.append({"area": "Political & Corruption Risk", "rule": "FCA FCG 2", "description": f"Corruption risk: {country}", "status": cp_status, "commentary": cp_comment})

    # Political stability
    stability = data.get("political_stability")
    if stability:
        if stability.lower() in ("stable", "high"):
            findings.append({"area": "Political & Corruption Risk", "rule": "FCA FCG 2", "description": "Political stability", "status": "GREEN", "commentary": f"Political stability assessed as {stability}."})
        elif stability.lower() in ("unstable", "conflict", "low"):
            findings.append({"area": "Political & Corruption Risk", "rule": "FCA FCG 2", "description": "Political stability", "status": "RED", "commentary": f"Political instability / active conflict in {country}. Client assets at risk of expropriation or loss."})
        else:
            findings.append({"area": "Political & Corruption Risk", "rule": "FCA FCG 2", "description": "Political stability", "status": "AMBER", "commentary": f"Political stability: {stability}. Monitor for deterioration."})

    # FCA jurisdiction concern
    fca_concern = data.get("fca_prior_concern")
    if fca_concern:
        findings.append({"area": "FCA Jurisdiction Risk", "rule": "FCA FCG", "description": f"FCA prior concern: {country}", "status": "AMBER", "commentary": f"FCA has previously raised concerns about this jurisdiction: {fca_concern}. Apply enhanced scrutiny."})
    else:
        findings.append({"area": "FCA Jurisdiction Risk", "rule": "FCA FCG", "description": "FCA jurisdiction risk", "status": "GREEN", "commentary": f"No specific FCA jurisdiction concerns on record for {country}."})

    # Client assets cross-border (UK baseline)
    if "client asset" in purpose.lower() or "cass" in purpose.lower():
        cross_border_risk = sanctioned or country in FATF_BLACK_LIST
        findings.append({
            "area": "Cross-Border Client Assets", "rule": "CASS 6 / CASS 7",
            "description": f"Client assets held in {country}",
            "status": "RED" if cross_border_risk else "AMBER",
            "commentary": f"CLIENT ASSETS IN SANCTIONED/HIGH-RISK JURISDICTION. Immediate review required under CASS 6/7." if cross_border_risk
            else f"Cross-border client assets in {country}. Ensure CASS-equivalent protections apply and review custody arrangements.",
        })

    # Regional regulatory routing — N. America / LATAM / APAC
    regional_findings = score_regional_cross_border(country, data)
    findings.extend(regional_findings)

    return findings


def overall_rating(findings: list) -> str:
    statuses = [f["status"] for f in findings]
    if "RED" in statuses:
        return "HIGH RISK — Do not proceed without legal and compliance sign-off."
    elif "AMBER" in statuses:
        return "ELEVATED RISK — Enhanced due diligence and controls required."
    return "STANDARD RISK — Standard controls apply. Monitor for changes."


def build_report(data: dict, findings: list, client_name: str, intel: dict = None) -> Document:
    country = data.get("country", "Unknown")
    region  = detect_region(country)
    doc = start_document(f"Country Risk Report — {country}", data, client_name)
    counts = rag_counts(findings)
    rating = overall_rating(findings)

    doc.add_heading("2. Executive Summary", level=1)
    doc.add_paragraph(
        f"Country risk assessment: {country}\n"
        f"Purpose: {data.get('purpose', 'N/A')}\n"
        f"Overall rating: {rating}\n"
        f"Checks: {counts['GREEN']} LOW | {counts['AMBER']} ELEVATED | {counts['RED']} HIGH RISK"
    )
    if counts["RED"]:
        doc.add_paragraph(f"HIGH RISK: {counts['RED']} critical risk factor(s). Do not proceed without compliance sign-off.").runs[0].font.bold = True

    add_firm_profile(doc, data, client_name, [
        ("Country Assessed", country),
        ("Purpose", data.get("purpose", "N/A")),
        ("Overall Rating", rating),
    ])

    add_findings_table(doc, [f for f in findings if f["area"] == "Sanctions"], "Sanctions Assessment", 4)
    add_findings_table(doc, [f for f in findings if f["area"] == "FATF / AML Risk"], "FATF Status & AML Risk", 5)
    add_findings_table(doc, [f for f in findings if "Political" in f["area"] or "FCA" in f["area"]], "Political, Corruption & FCA Risk", 6)
    cross_border = [f for f in findings if "Cross-Border" in f["area"] or "Client Asset" in f["area"]]
    if cross_border:
        add_findings_table(doc, cross_border, "Cross-Border Client Asset Risk", 7)

    # Regional framework section (all regions)
    regional = [f for f in findings if any(k in f["area"] for k in (
        "(US)", "(N.", "LATAM", "SIPC", "SEC", "CFTC",
        "Brazil", "Argentina", "Mexico", "Chile", "Colombia",
        "Hong Kong", "Australia", "Singapore", "Japan", "APAC",
        "EU/Europe", "MiFID", "ESMA", "BaFin",
        "Africa", "FSCA", "Nigeria", "Kenya", "Ghana", "Mauritius", "Egypt",
        "No Unified",
    ))]
    if regional:
        section_title = f"Regional Regulatory Framework — {region}"
        add_findings_table(doc, regional, section_title, 7 if not cross_border else 8)

    add_summary_table(doc, findings, 9)

    # Recommended controls
    doc.add_heading("9. Recommended Controls", level=1)
    controls = [
        ("Sanctions Screening", "Screen all transactions, counterparties and individuals against OFSI and OFAC lists before proceeding."),
        ("Enhanced Due Diligence", "Apply EDD for FATF grey/black list countries per UK MLTF Regulations 2017 Regulation 33."),
        ("Beneficial Ownership", "Verify ultimate beneficial owners to prevent sanctions evasion via complex structures."),
        ("Ongoing Monitoring", "Monitor for changes in FATF status, sanctions, and political stability on a quarterly basis."),
        ("CASS Protections", "Ensure client assets held cross-border have equivalent CASS protections and insurance arrangements."),
        ("SAR Filing", "File Suspicious Activity Reports with NCA if transactions cannot be explained given jurisdiction risk."),
    ]
    ctrl_tbl = doc.add_table(rows=1 + len(controls), cols=2)
    ctrl_tbl.style = "Table Grid"
    header_cell(ctrl_tbl.rows[0].cells[0], "Control")
    header_cell(ctrl_tbl.rows[0].cells[1], "Detail")
    for i, (ctrl, detail) in enumerate(controls):
        ctrl_tbl.rows[i + 1].cells[0].text = ctrl
        ctrl_tbl.rows[i + 1].cells[1].text = detail

    add_intel_section(doc, intel, 10)

    # Base UK regulatory refs + regional refs
    base_refs = [
        ("OFSI Sanctions", "https://www.gov.uk/government/organisations/office-of-financial-sanctions-implementation"),
        ("OFAC SDN List", "https://ofac.treasury.gov/sanctions-programs-and-country-information"),
        ("FATF High-Risk Jurisdictions", "https://www.fatf-gafi.org/en/topics/high-risk-and-other-monitored-jurisdictions.html"),
        ("Basel AML Index", "https://index.baselgovernance.org"),
        ("UK MLTF Regulations 2017", "Regulation 33 — Enhanced due diligence for high-risk third countries"),
        ("FCA FCG 2", "https://www.handbook.fca.org.uk/handbook/FCG/2/"),
    ]
    regional_refs = regional_regulatory_refs(data.get("region", "") or country)
    add_regulatory_refs(doc, base_refs + regional_refs, 11)
    return doc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", required=True)
    parser.add_argument("--no-scan", action="store_true")
    args = parser.parse_args()
    client_name = args.client.replace(" ", "_")
    data = load_client_data(PREFIX, client_name)
    country = data.get("country", "")
    region  = detect_region(data.get("region") or country) if (data.get("region") or country) else None
    intel = {} if args.no_scan else run_perplexity_scan(REPORT_TYPE, region=region, country=country)
    findings = score_country(data)
    counts = rag_counts(findings)
    print(f"Results: {counts['GREEN']} LOW | {counts['AMBER']} ELEVATED | {counts['RED']} HIGH")
    print(f"Rating: {overall_rating(findings)}")
    doc = build_report(data, findings, client_name, intel)
    path = save_report(doc, PREFIX, client_name)
    print(f"Report saved: {path}")


if __name__ == "__main__":
    main()
