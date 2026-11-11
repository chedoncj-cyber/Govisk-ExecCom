"""
FATF Blacklist Intelligence Report Generator
Methodology: FATF 40 Recommendations · UK MLR 2017 · POCA 2002 · OFSI · FCA FCG
Produces a scored Word document covering FATF status, AML/CFT controls, EDD
obligations, sanctions exposure, and remediation plan.
Usage: python tools/generate_blacklist_report.py --client "<client_name>" [--no-scan]
"""

import argparse
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from report_base import (
    BASE_DIR, TMP_DIR,
    WHITE, HEADER_HEX, RAG_BG, PRIORITY_MAP,
    set_cell_bg, header_cell, rag_cell, rag_counts,
    load_client_data, save_report,
    add_findings_table, add_summary_table, add_remediation_table,
    add_intel_section, add_regulatory_refs,
    run_perplexity_scan, reg_id_label,
)
from dotenv import load_dotenv
from regional_routing import detect_region, regional_regulatory_refs

load_dotenv()
REPORT_TYPE = "blacklist_report"
PREFIX      = "blacklist"

# ── FATF lists (kept in sync with fatf_blacklist.py baseline) ─────────────────
FATF_BLACK_LIST = {"Iran", "North Korea", "North Korea (DPRK)", "Myanmar"}

FATF_GREY_LIST = {
    "Algeria", "Angola", "Bulgaria", "Burkina Faso", "Cameroon", "Croatia",
    "Democratic Republic of Congo", "Haiti", "Jamaica", "Kenya", "Mali", "Monaco",
    "Mozambique", "Namibia", "Nigeria", "Philippines", "Senegal", "South Africa",
    "Syria", "Tanzania", "Venezuela", "Vietnam", "Yemen",
}

SANCTIONS_COUNTRIES = {
    "Russia", "Belarus", "Iran", "North Korea", "Syria", "Myanmar", "Sudan",
    "Somalia", "Libya", "Venezuela", "Cuba", "Zimbabwe",
}

# ── Risk typologies by counterparty type ─────────────────────────────────────
TYPOLOGY_RISKS = {
    "Correspondent Bank": [
        "Nested correspondent banking layering",
        "Shell company usage via correspondent chains",
        "Sanctions evasion through intermediaries",
    ],
    "Trade Finance": [
        "Trade-based money laundering (TBML) via invoice manipulation",
        "Over/under invoicing to transfer value",
        "Dual-use goods — proliferation financing risk",
    ],
    "Direct Client": [
        "Placement of illicit funds",
        "PEP / politically exposed person risk",
        "Source of wealth / funds opacity",
    ],
    "Investment": [
        "Layering via complex investment structures",
        "Real estate / high-value asset use for value transfer",
        "Beneficial ownership concealment",
    ],
    "Payment Processing": [
        "Structuring / smurfing below reporting thresholds",
        "Virtual asset conversion risk",
        "Rapid fund movement across jurisdictions",
    ],
}


def _fatf_status(country: str) -> tuple[str, str]:
    """Return (status, description) for a country name."""
    c = country.strip()
    if c in FATF_BLACK_LIST:
        return ("BLACK", f"{c} is on the FATF Black List (High-Risk — Call for Action). "
                "Mandatory counter-measures apply under UK MLR 2017 Reg 33. "
                "HMRC / FCA / NCA notification obligations may apply.")
    if c in FATF_GREY_LIST:
        return ("GREY", f"{c} is on the FATF Grey List (Increased Monitoring). "
                "Enhanced Due Diligence (EDD) is required under UK MLR 2017 Reg 33. "
                "Ongoing monitoring frequency should be increased.")
    return ("CLEAN", f"{c} is not currently listed on the FATF Black or Grey List. "
            "Standard CDD applies, supplemented by any applicable sanctions checks.")


def score_jurisdiction(data: dict) -> list:
    findings = []
    raw = data.get("countries_involved", "")
    countries = [c.strip() for c in raw.replace(";", ",").split(",") if c.strip()]
    if not countries:
        countries = [data.get("country", "Unknown")]

    for country in countries:
        fatf, desc = _fatf_status(country)
        sanctioned = country in SANCTIONS_COUNTRIES or data.get("sanctions_applicable", False)

        # FATF risk
        rag = "RED" if fatf == "BLACK" else ("AMBER" if fatf == "GREY" else "GREEN")
        findings.append({
            "area": "FATF Jurisdiction Risk",
            "rule": "FATF 40 Recs / UK MLR 2017 Reg 33",
            "description": f"FATF status: {country}",
            "status": rag,
            "commentary": desc,
        })

        # Sanctions overlay
        if sanctioned:
            findings.append({
                "area": "Sanctions",
                "rule": "OFSI / UK Sanctions Act 2018",
                "description": f"Sanctions exposure: {country}",
                "status": "RED",
                "commentary": (
                    f"{country} is subject to active UK (OFSI), and likely EU / US (OFAC) sanctions. "
                    "All transactions require an OFSI licence. Engaging without a licence is a criminal offence. "
                    "Notify senior management and legal immediately."
                ),
            })
        else:
            findings.append({
                "area": "Sanctions",
                "rule": "OFSI / OFAC",
                "description": f"Sanctions check: {country}",
                "status": "GREEN",
                "commentary": f"No active UK sanctions regime identified for {country}. Verify directly at OFSI before proceeding.",
            })

    return findings


def score_aml_controls(data: dict) -> list:
    findings = []

    # Sanctions screening tool
    screening_tool = data.get("sanctions_screening_tool", "").strip()
    screening_done = data.get("sanctions_screening_performed", False)
    if screening_done and screening_tool:
        findings.append({"area": "AML/CFT Controls", "rule": "UK MLR 2017 Reg 28",
                         "description": f"Sanctions screening ({screening_tool})",
                         "status": "GREEN",
                         "commentary": f"Sanctions screening completed using {screening_tool}. Ensure daily list updates and document match/non-match decisions."})
    elif screening_done:
        findings.append({"area": "AML/CFT Controls", "rule": "UK MLR 2017 Reg 28",
                         "description": "Sanctions screening",
                         "status": "AMBER",
                         "commentary": "Screening performed but tool not documented. Name the specific screening system used — FCA expects documented and auditable processes."})
    else:
        findings.append({"area": "AML/CFT Controls", "rule": "UK MLR 2017 Reg 28",
                         "description": "Sanctions screening",
                         "status": "RED",
                         "commentary": "Sanctions screening not confirmed. UK MLR 2017 Reg 28 mandates screening before onboarding and on an ongoing basis. Failure is a criminal offence."})

    # EDD procedures
    edd = data.get("edd_procedures_in_place", False)
    findings.append({"area": "AML/CFT Controls", "rule": "UK MLR 2017 Reg 33",
                     "description": "Enhanced Due Diligence (EDD) procedures",
                     "status": "GREEN" if edd else "RED",
                     "commentary": "Documented EDD procedures in place for high-risk jurisdiction relationships." if edd
                     else "EDD procedures absent or undocumented. MLR 2017 Reg 33 mandates EDD for all FATF-listed and high-risk jurisdiction transactions."})

    # PEP screening
    pep = data.get("pep_screening_performed", False)
    findings.append({"area": "AML/CFT Controls", "rule": "UK MLR 2017 Reg 35",
                     "description": "Politically Exposed Person (PEP) screening",
                     "status": "GREEN" if pep else "AMBER",
                     "commentary": "PEP screening performed and documented." if pep
                     else "PEP screening not confirmed. MLR 2017 Reg 35 requires enhanced measures for PEPs — screen all principals, beneficial owners, and directors."})

    # Adverse media
    adverse = data.get("adverse_media_screening", False)
    findings.append({"area": "AML/CFT Controls", "rule": "FCA FCG / FATF Rec 10",
                     "description": "Adverse media and negative news monitoring",
                     "status": "GREEN" if adverse else "AMBER",
                     "commentary": "Adverse media screening performed at onboarding and ongoing." if adverse
                     else "Adverse media screening not confirmed. FCA expects firms to identify negative news on customers — implement periodic checks as part of ongoing monitoring."})

    # Source of funds
    sof = data.get("source_of_funds_verified", False)
    findings.append({"area": "AML/CFT Controls", "rule": "UK MLR 2017 Reg 28(9)",
                     "description": "Source of funds / wealth verification",
                     "status": "GREEN" if sof else "RED",
                     "commentary": "Source of funds verified and documented." if sof
                     else "Source of funds not verified. MLR 2017 Reg 28(9) requires verification for high-risk customers — critical given FATF jurisdictional risk."})

    # Beneficial ownership
    bo = data.get("beneficial_owner_identified", False)
    findings.append({"area": "AML/CFT Controls", "rule": "UK MLR 2017 Reg 5 / FATF Rec 10",
                     "description": "Beneficial ownership identification (UBO ≥25%)",
                     "status": "GREEN" if bo else "RED",
                     "commentary": "Ultimate beneficial owner(s) identified and verified." if bo
                     else "UBO not confirmed. MLR 2017 Reg 5 and the Economic Crime Act 2022 require UBO identification for all corporate customers. Gap increases ML risk."})

    return findings


def score_reporting(data: dict) -> list:
    findings = []

    # SAR
    sar = data.get("sar_filed", False)
    sar_required = data.get("sar_filing_required", False)
    if sar_required and sar:
        findings.append({"area": "Regulatory Reporting", "rule": "POCA 2002 s330 / TACT 2000 s21A",
                         "description": "Suspicious Activity Report (SAR) filing",
                         "status": "GREEN",
                         "commentary": "SAR filed with National Crime Agency (NCA) as required. Retain all supporting documentation for audit trail."})
    elif sar_required and not sar:
        findings.append({"area": "Regulatory Reporting", "rule": "POCA 2002 s330",
                         "description": "SAR filing — potentially required",
                         "status": "RED",
                         "commentary": "SAR has NOT been filed despite apparent obligation. Failure to file a required SAR is a criminal offence under POCA 2002 s330. Seek MLRO / legal advice immediately."})
    else:
        findings.append({"area": "Regulatory Reporting", "rule": "POCA 2002 s330",
                         "description": "SAR assessment completed",
                         "status": "GREEN",
                         "commentary": "SAR assessment performed. Filing not deemed necessary at this time — document rationale and retain for audit trail."})

    # AML training
    training_rate = data.get("aml_training_completion_rate", 0)
    t_status = "GREEN" if training_rate >= 90 else ("AMBER" if training_rate >= 70 else "RED")
    findings.append({"area": "Regulatory Reporting", "rule": "UK MLR 2017 Reg 24 / FCA SYSC 6.3",
                     "description": f"AML/CFT training completion rate ({training_rate}%)",
                     "status": t_status,
                     "commentary": f"Training completion: {training_rate}% (benchmark ≥90%). "
                     f"{'On target.' if t_status == 'GREEN' else 'Require all staff to complete AML training — failure to train is a MLR 2017 Reg 24 breach.'}"})

    # Last AML risk assessment
    last_aml_date_str = data.get("last_aml_risk_assessment_date", "")
    if last_aml_date_str:
        try:
            from datetime import datetime
            last_aml = datetime.strptime(last_aml_date_str, "%Y-%m-%d").date()
            days_ago = (date.today() - last_aml).days
            if days_ago <= 365:
                findings.append({"area": "Regulatory Reporting", "rule": "UK MLR 2017 Reg 18",
                                 "description": f"Firm-wide AML risk assessment (last: {days_ago} days ago)",
                                 "status": "GREEN",
                                 "commentary": f"AML risk assessment current ({last_aml.strftime('%d %b %Y')}). Next review due {(last_aml.replace(year=last_aml.year+1)).strftime('%d %b %Y')}."})
            else:
                findings.append({"area": "Regulatory Reporting", "rule": "UK MLR 2017 Reg 18",
                                 "description": f"Firm-wide AML risk assessment (OVERDUE — {days_ago} days)",
                                 "status": "AMBER",
                                 "commentary": f"AML risk assessment is {days_ago} days old — overdue for annual review under MLR 2017 Reg 18. Update before next FCA review."})
        except (ValueError, TypeError):
            findings.append({"area": "Regulatory Reporting", "rule": "UK MLR 2017 Reg 18",
                             "description": "AML risk assessment date unreadable",
                             "status": "AMBER",
                             "commentary": "AML risk assessment date provided is not in a recognised format. Confirm and re-record."})
    else:
        findings.append({"area": "Regulatory Reporting", "rule": "UK MLR 2017 Reg 18",
                         "description": "Firm-wide AML risk assessment",
                         "status": "RED",
                         "commentary": "No AML risk assessment date provided. MLR 2017 Reg 18 mandates annual firm-wide AML/CFT risk assessment. Absence is an FCA enforcement trigger."})

    return findings


def score_correspondent_banking(data: dict) -> list:
    findings = []
    has_corr = data.get("correspondent_bank_relationships", False)
    if not has_corr:
        return findings

    # Corr bank in listed jurisdiction
    corr_listed = data.get("correspondent_bank_in_listed_jurisdiction", False)
    if corr_listed:
        findings.append({"area": "Correspondent Banking Risk", "rule": "UK MLR 2017 Reg 34 / FATF Rec 13",
                         "description": "Correspondent bank in FATF-listed jurisdiction",
                         "status": "RED",
                         "commentary": "Correspondent bank relationship exists with an institution in a FATF-listed jurisdiction. MLR 2017 Reg 34 requires enhanced due diligence — obtain senior management approval and document controls."})
    else:
        findings.append({"area": "Correspondent Banking Risk", "rule": "UK MLR 2017 Reg 34",
                         "description": "Correspondent banking jurisdiction review",
                         "status": "GREEN",
                         "commentary": "No correspondent bank relationships identified in FATF-listed jurisdictions. Maintain periodic review as FATF lists change quarterly."})

    # Shell bank prohibition
    shell_bank_check = data.get("shell_bank_check_performed", False)
    findings.append({"area": "Correspondent Banking Risk", "rule": "UK MLR 2017 Reg 34(3) / FATF Rec 13",
                     "description": "Shell bank prohibition check",
                     "status": "GREEN" if shell_bank_check else "RED",
                     "commentary": "Verified correspondent bank has genuine physical presence and is subject to AML supervision." if shell_bank_check
                     else "Shell bank check not documented. MLR 2017 Reg 34(3) prohibits relationships with shell banks — this check must be evidenced."})

    return findings


def build_report(data: dict, jur_f: list, aml_f: list, rep_f: list, corr_f: list,
                 client_name: str, intel: dict = None):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx import Document

    doc = Document()

    # Title
    title = doc.add_heading("FATF Blacklist Intelligence Report", level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph(
        f"Prepared for: {data.get('firm_name', client_name)}\n"
        f"{reg_id_label(data)}: {data.get('frn', 'N/A')}\n"
        f"Counterparty / Subject: {data.get('counterparty_name', 'N/A')}\n"
        f"Counterparty Type: {data.get('counterparty_type', 'N/A')}\n"
        f"Countries Assessed: {data.get('countries_involved', 'N/A')}\n"
        f"Assessment Date: {date.today().strftime('%d %B %Y')}\n"
        f"Framework: FATF 40 Recommendations · UK MLR 2017 · POCA 2002 · OFSI · FCA FCG\n"
        f"Prepared by: Govisk ExecCom Intelligence Reports"
    )
    doc.add_paragraph(
        "CONFIDENTIAL — This report is for the exclusive use of the named firm. "
        "It does not constitute legal or regulatory advice. "
        "Verify all FATF list statuses directly at fatf-gafi.org before making compliance decisions."
    ).runs[0].font.italic = True

    # Section 1: Executive Summary
    all_findings = jur_f + aml_f + rep_f + corr_f
    counts = rag_counts(all_findings)
    doc.add_heading("1. Executive Summary", level=1)

    countries_involved = data.get("countries_involved", "N/A")
    black_count = sum(1 for f in jur_f if f["status"] == "RED" and "Black List" in f.get("commentary", ""))
    grey_count  = sum(1 for f in jur_f if f["status"] == "AMBER")

    doc.add_paragraph(
        f"This FATF Blacklist Intelligence Report assessed {len(all_findings)} compliance control points "
        f"covering jurisdictional FATF risk, AML/CFT controls, regulatory reporting, and correspondent banking "
        f"obligations for {data.get('firm_name', client_name)} in relation to: {countries_involved}.\n\n"
        f"  • Total findings:          {len(all_findings)}\n"
        f"  • PASS:                    {counts['GREEN']}\n"
        f"  • REQUIRES ATTENTION:      {counts['AMBER']}\n"
        f"  • FAIL / IMMEDIATE ACTION: {counts['RED']}\n\n"
        f"Jurisdictional FATF exposure — Black List: {sum(1 for f in jur_f if 'BLACK' in f.get('description','').upper() or 'Black List' in f.get('commentary',''))}, "
        f"Grey List: {grey_count}"
    )

    if counts["RED"] > 0:
        p = doc.add_paragraph(
            f"IMMEDIATE ACTION REQUIRED: {counts['RED']} critical finding(s) identified. "
            "Review Sections 3–6 and implement the Remediation Plan in Section 8."
        )
        p.runs[0].font.bold = True

    # Section 2: Firm & Counterparty Profile
    doc.add_heading("2. Firm & Counterparty Profile", level=1)
    rows = [
        ("Firm Name",             data.get("firm_name", client_name)),
        (reg_id_label(data),      data.get("frn", "N/A")),
        ("Counterparty / Subject",data.get("counterparty_name", "N/A")),
        ("Counterparty Type",     data.get("counterparty_type", "N/A")),
        ("Client Category",       data.get("client_category", "N/A")),
        ("Transaction Type",      data.get("transaction_type", "N/A")),
        ("Countries Assessed",    data.get("countries_involved", "N/A")),
        ("Assessment Period",     data.get("assessment_period", f"As of {date.today().strftime('%d %B %Y')}")),
        ("Assessment Date",       date.today().strftime("%d %B %Y")),
    ]
    tbl = doc.add_table(rows=len(rows), cols=2)
    tbl.style = "Table Grid"
    for i, (label, value) in enumerate(rows):
        tbl.rows[i].cells[0].text = label
        tbl.rows[i].cells[1].text = str(value)
        if tbl.rows[i].cells[0].paragraphs[0].runs:
            tbl.rows[i].cells[0].paragraphs[0].runs[0].font.bold = True

    # Section 3: Jurisdictional FATF Risk
    add_findings_table(doc, jur_f, "Jurisdictional FATF Risk Assessment", 3)

    # Section 4: AML/CFT Controls
    add_findings_table(doc, aml_f, "AML/CFT Controls Assessment", 4)

    # Section 5: Regulatory Reporting Obligations
    add_findings_table(doc, rep_f, "Regulatory Reporting Obligations", 5)

    # Section 6: Correspondent Banking Risk (if applicable)
    if corr_f:
        add_findings_table(doc, corr_f, "Correspondent Banking Risk", 6)
        next_section = 7
    else:
        next_section = 6

    # Typology Risks
    doc.add_heading(f"{next_section}. ML/TF Typology Risks", level=1)
    next_section += 1
    ctype = data.get("counterparty_type", "Direct Client")
    typologies = TYPOLOGY_RISKS.get(ctype, TYPOLOGY_RISKS["Direct Client"])
    doc.add_paragraph(f"The following ML/TF typologies are most relevant for a {ctype} relationship "
                      f"in the assessed jurisdictions:")
    for t in typologies:
        doc.add_paragraph(t, style="List Bullet")

    # Summary
    add_summary_table(doc, all_findings, next_section)
    next_section += 1

    # Remediation
    add_remediation_table(doc, all_findings, next_section)
    next_section += 1

    # Live Intel
    if intel:
        add_intel_section(doc, intel, next_section)
        next_section += 1

    # Regulatory References
    primary_country = data.get("country", "") or (
        data.get("countries_involved", "").split(",")[0].strip()
        if data.get("countries_involved") else ""
    )
    regional_refs = regional_regulatory_refs(data.get("region", "") or primary_country)
    refs = [
        ("FATF 40 Recommendations",     "International standards on combating money laundering and TF/PF"),
        ("UK MLR 2017 Reg 33",          "Enhanced Due Diligence for high-risk third countries"),
        ("UK MLR 2017 Reg 34",          "Enhanced measures for correspondent banking relationships"),
        ("UK MLR 2017 Reg 35",          "Enhanced measures for PEP relationships"),
        ("UK MLR 2017 Reg 28",          "Customer due diligence requirements"),
        ("UK MLR 2017 Reg 18",          "Firm-wide risk assessment obligations"),
        ("UK MLR 2017 Reg 24",          "Staff AML/CFT awareness and training"),
        ("POCA 2002 s330",              "Failure to disclose — money laundering offence"),
        ("TACT 2000 s21A",              "Failure to disclose — terrorism financing offence"),
        ("UK Sanctions Act 2018",       "UK autonomous sanctions regime — OFSI enforcement"),
        ("FCA Financial Crime Guide",   "FCA's guidance on firms' systems and controls to combat financial crime"),
        ("Economic Crime Act 2022",     "Enhanced UBO requirements and corporate transparency reforms"),
    ] + regional_refs
    add_regulatory_refs(doc, refs, next_section)

    return doc


def main():
    parser = argparse.ArgumentParser(description="FATF Blacklist Intelligence Report Generator")
    parser.add_argument("--client",  required=True, help="Client name (used as filename key)")
    parser.add_argument("--no-scan", action="store_true", help="Skip Routing Intelligence Scan")
    args = parser.parse_args()

    data = load_client_data(PREFIX, args.client)

    intel = {}
    if not args.no_scan:
        country = data.get("country", "") or (
            data.get("countries_involved", "").split(",")[0].strip()
            if data.get("countries_involved") else ""
        )
        region = detect_region(data.get("region") or country) if (data.get("region") or country) else None
        intel = run_perplexity_scan(REPORT_TYPE, region=region, country=country)

    jur_f  = score_jurisdiction(data)
    aml_f  = score_aml_controls(data)
    rep_f  = score_reporting(data)
    corr_f = score_correspondent_banking(data)

    doc  = build_report(data, jur_f, aml_f, rep_f, corr_f, args.client, intel)
    path = save_report(doc, PREFIX, args.client)
    print(f"[OK] FATF Blacklist Intelligence Report: {path}")


if __name__ == "__main__":
    main()
