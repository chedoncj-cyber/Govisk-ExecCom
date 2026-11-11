"""
Client Money Segregation Audit Report Generator (CASS 7)
Usage: python tools/generate_client_money_segregation.py --client "<client_name>" [--no-scan]
"""

import argparse
from datetime import datetime, date
from dotenv import load_dotenv
from report_base import *
from regional_routing import (
    detect_region,
    score_regional_client_money,
    regional_regulatory_refs,
)

load_dotenv()
REPORT_TYPE = "client_money_segregation"
PREFIX = "cms_audit"


def score_checks(data: dict) -> list:
    findings = []

    # Account designation
    designated = data.get("all_accounts_designated")
    findings.append({
        "area": "Account Designation", "rule": "CASS 7.17.2R",
        "description": "All client money accounts properly designated",
        "status": "GREEN" if designated else "RED",
        "commentary": "All accounts confirmed designated as client money accounts." if designated
        else "One or more accounts NOT designated. Immediate remediation — CASS 7.17.2R breach.",
    })

    # Acknowledgement letters
    ack = data.get("acknowledgement_letters_all_accounts")
    findings.append({
        "area": "Acknowledgement Letters", "rule": "CASS 7.18.3R",
        "description": "Acknowledgement letters for all approved bank accounts",
        "status": "GREEN" if ack is True else ("RED" if ack is False else "AMBER"),
        "commentary": "All acknowledgement letters in place." if ack is True
        else ("Acknowledgement letters MISSING for one or more accounts. Must be obtained before depositing client money." if ack is False
              else "Status unconfirmed. Full inventory of letters required."),
    })

    # Internal reconciliation frequency
    freq = data.get("internal_reconciliation_frequency", "").lower()
    findings.append({
        "area": "Reconciliation", "rule": "CASS 7.13.4R",
        "description": "Internal reconciliation performed daily",
        "status": "GREEN" if freq == "daily" else "RED",
        "commentary": "Daily internal reconciliation confirmed." if freq == "daily"
        else f"Reconciliation frequency: '{freq}'. CASS 7.13.4R requires daily reconciliation.",
    })

    # Last internal reconciliation date
    last_ir = data.get("last_internal_reconciliation_date")
    if last_ir:
        days = (date.today() - datetime.strptime(last_ir, "%Y-%m-%d").date()).days
        s = "GREEN" if days <= 1 else "RED"
        c = f"Last internal reconciliation: {last_ir} ({days} day(s) ago)." + ("" if days <= 1 else " Overdue — CASS 7.13.4R requires daily reconciliation.")
    else:
        s, c = "AMBER", "Last internal reconciliation date not provided."
    findings.append({"area": "Reconciliation", "rule": "CASS 7.13.4R", "description": "Internal reconciliation current", "status": s, "commentary": c})

    # External reconciliation
    last_er = data.get("last_external_reconciliation_date")
    if last_er:
        days = (date.today() - datetime.strptime(last_er, "%Y-%m-%d").date()).days
        s = "GREEN" if days <= 25 else "AMBER"
        c = f"Last external reconciliation: {last_er} ({days} days ago)."
    else:
        s, c = "AMBER", "External reconciliation date not provided. Verify under CASS 7.15."
    findings.append({"area": "Reconciliation", "rule": "CASS 7.15", "description": "External reconciliation performed", "status": s, "commentary": c})

    # Reconciliation breaks
    breaks = data.get("reconciliation_breaks_identified")
    findings.append({
        "area": "Reconciliation Breaks", "rule": "CASS 7.13",
        "description": "No unresolved reconciliation breaks",
        "status": "RED" if breaks else "GREEN",
        "commentary": f"Reconciliation break(s) identified: {data.get('break_details', 'details not provided')}. Immediate investigation required."
        if breaks else "No reconciliation breaks identified.",
    })

    # Calculation method
    method = data.get("calculation_method", "").lower()
    if method == "standard":
        findings.append({"area": "Calculation Method", "rule": "CASS 7.16", "description": "Client money calculation method", "status": "GREEN", "commentary": "Standard method in use."})
    elif method == "alternative":
        agreed = data.get("alternative_method_fca_agreed", False)
        findings.append({
            "area": "Calculation Method", "rule": "CASS 7.16",
            "description": "Alternative calculation method — FCA agreement",
            "status": "GREEN" if agreed else "RED",
            "commentary": "Alternative method — FCA agreement confirmed." if agreed else "Alternative method in use WITHOUT FCA agreement. CASS 7.16 breach.",
        })
    else:
        findings.append({"area": "Calculation Method", "rule": "CASS 7.16", "description": "Calculation method", "status": "AMBER", "commentary": "Method not specified. Confirm standard or alternative under CASS 7.16."})

    # Diversification
    max_pct = data.get("max_single_institution_pct")
    if max_pct is not None:
        s = "GREEN" if max_pct <= 20 else "AMBER"
        c = f"{max_pct}% held at single institution." + (" Consider diversification under CASS 7.19." if max_pct > 20 else " Within acceptable range.")
    else:
        s, c = "AMBER", "Diversification data not provided. Review under CASS 7.19."
    findings.append({"area": "Diversification", "rule": "CASS 7.19", "description": "Diversification of client money deposits", "status": s, "commentary": c})

    # Affiliated entities
    affiliated = data.get("accounts_with_affiliated_entities")
    if affiliated:
        findings.append({"area": "Third-Party Arrangements", "rule": "CASS 7.13", "description": "Accounts held with affiliated entities", "status": "AMBER", "commentary": "Accounts held with affiliated entities identified. Enhanced oversight required to ensure arms-length segregation."})

    # Third-party agents
    agents = data.get("third_party_agent_arrangements")
    if agents:
        findings.append({"area": "Third-Party Arrangements", "rule": "CASS 7.13", "description": "Third-party agent arrangements", "status": "AMBER", "commentary": "Third-party agent arrangements in place. Ensure written agreements and oversight under CASS 7."})

    # Regional routing — append US / LATAM / APAC checks if applicable
    regional_findings = score_regional_client_money(data)
    findings.extend(regional_findings)

    return findings


def build_report(data: dict, findings: list, client_name: str, intel: dict = None) -> Document:
    country = data.get("country", "") or data.get("jurisdiction", "")
    region  = detect_region(country)
    doc = start_document("Client Money Segregation Audit", data, client_name)
    counts = rag_counts(findings)
    doc.add_heading("2. Executive Summary", level=1)
    doc.add_paragraph(
        f"CASS 7 client money segregation audit for {data.get('firm_name', client_name)}. "
        f"{len(findings)} checks: {counts['GREEN']} PASS | {counts['AMBER']} ATTENTION | {counts['RED']} FAIL."
    )
    if counts["RED"]:
        doc.add_paragraph(f"CRITICAL: {counts['RED']} failure(s) require immediate remediation.").runs[0].font.bold = True

    add_firm_profile(doc, data, client_name)
    add_findings_table(doc, [f for f in findings if f["area"] in ("Account Designation", "Acknowledgement Letters")], "Account Inventory & Designation", 4)
    add_findings_table(doc, [f for f in findings if "Reconciliation" in f["area"]], "Reconciliation Compliance", 5)
    add_findings_table(doc, [f for f in findings if f["area"] in ("Calculation Method", "Diversification", "Third-Party Arrangements")], "Method, Diversification & Arrangements", 6)

    # Regional framework section if applicable
    regional_areas = [f for f in findings if any(k in f["area"] for k in (
        "(US)", "SIPC", "Reserve Formula", "Daily Segregation", "Depository Acknowledgements", "Commingling",
        "Brazil", "Argentina", "Mexico", "Chile", "Colombia", "LATAM",
        "Hong Kong", "Australia", "Singapore", "Japan", "APAC",
        "MiFID", "EU/Europe", "ESMA",
        "Africa", "FSCA", "Nigeria", "Kenya", "Mauritius", "Egypt", "Ghana",
        "Trust/Safeguarding", "Investor Protection", "Regulatory Authorisation", "Cross-Border CASS",
        "No Unified",
    ))]
    if regional_areas:
        add_findings_table(doc, regional_areas, f"Regional Regulatory Framework — {region}", 7)

    add_summary_table(doc, findings, 8)
    add_remediation_table(doc, findings, 9)
    add_intel_section(doc, intel, 10)

    base_refs = [
        ("CASS 7.13.4R", "Daily internal client money reconciliation"),
        ("CASS 7.15", "External reconciliation"),
        ("CASS 7.16", "Client money calculation method"),
        ("CASS 7.17.2R", "Account designation requirements"),
        ("CASS 7.18.3R", "Acknowledgement letters"),
        ("CASS 7.19", "Diversification of deposits"),
        ("FCA Handbook", "https://www.handbook.fca.org.uk/handbook/CASS/7/"),
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
