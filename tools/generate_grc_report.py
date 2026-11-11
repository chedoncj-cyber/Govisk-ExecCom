"""
GRC (Governance, Risk & Compliance) Intelligence Report Generator
Methodology: OCEG GRC Capability Model · COSO · NIST · ISO 31000 · FCA regulatory lens
Produces a scored Word document with RAG findings, KPI table, maturity model, and remediation plan.
Usage: python tools/generate_grc_report.py --client "<client_name>" [--no-scan]
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
    load_client_data, save_report, start_document,
    add_findings_table, add_summary_table, add_remediation_table,
    add_intel_section, add_regulatory_refs,
    add_enforcement_section, add_regulatory_updates_section,
    run_perplexity_scan, reg_id_label,
)
from regional_routing import detect_region, regional_regulatory_refs

REPORT_TYPE = "grc_report"

# ── Maturity level definitions (5-stage model) ──────────────────────────────
MATURITY_LEVELS = {
    1: ("Initial",    "Ad-hoc, reactive, undocumented processes. High risk of control failure."),
    2: ("Defined",    "Processes documented. Inconsistently applied. Limited measurement."),
    3: ("Managed",    "Processes monitored and measured. Controls generally effective."),
    4: ("Optimised",  "Continuous improvement embedded. Proactive risk identification."),
    5: ("Leading",    "Industry-leading practice. Predictive analytics. Full integration."),
}

# ── GRC KPI benchmarks (financial services, FCA-regulated) ──────────────────
KPI_BENCHMARKS = {
    "Policy comprehension rate":          {"target": 90,  "unit": "%",   "domain": "Governance"},
    "Board GRC agenda coverage":          {"target": 85,  "unit": "%",   "domain": "Governance"},
    "Decision-making framework coverage": {"target": 100, "unit": "%",   "domain": "Governance"},
    "Risk register currency (days)":      {"target": 30,  "unit": "days","domain": "Risk",       "lower_is_better": True},
    "Risk identification response time":  {"target": 5,   "unit": "days","domain": "Risk",       "lower_is_better": True},
    "Open critical risk items":           {"target": 0,   "unit": "",    "domain": "Risk",       "lower_is_better": True},
    "Training completion rate":           {"target": 95,  "unit": "%",   "domain": "Compliance"},
    "Control effectiveness rate":         {"target": 85,  "unit": "%",   "domain": "Compliance"},
    "Open audit findings":                {"target": 0,   "unit": "",    "domain": "Compliance", "lower_is_better": True},
    "Regulatory change response time":    {"target": 14,  "unit": "days","domain": "Compliance", "lower_is_better": True},
}


def _pct_status(value, target, lower_is_better=False):
    """Return RAG status given a value vs target."""
    if lower_is_better:
        if value <= target:                return "GREEN"
        if value <= target * 1.5:          return "AMBER"
        return "RED"
    else:
        if value >= target:                return "GREEN"
        if value >= target * 0.80:         return "AMBER"
        return "RED"


def score_governance(data: dict) -> list:
    findings = []

    # Board oversight
    board = data.get("governance_board_oversight", "").lower()
    if board == "strong":
        findings.append({"area": "Governance", "rule": "OCEG / FCA SYSC 4.1", "description": "Board-level GRC oversight",
                         "status": "GREEN", "commentary": "Board provides strong oversight with dedicated GRC agenda items and risk appetite statement."})
    elif board == "adequate":
        findings.append({"area": "Governance", "rule": "OCEG / FCA SYSC 4.1", "description": "Board-level GRC oversight",
                         "status": "AMBER", "commentary": "Board oversight adequate but lacks formal risk appetite statement or dedicated GRC reporting cycle."})
    else:
        findings.append({"area": "Governance", "rule": "OCEG / FCA SYSC 4.1", "description": "Board-level GRC oversight",
                         "status": "RED", "commentary": "Insufficient board-level oversight. FCA SYSC 4.1.1 R requires adequate management and control. Immediate board engagement required."})

    # Policy documentation
    policy_current = data.get("governance_policy_doc_current", False)
    findings.append({"area": "Governance", "rule": "FCA SYSC 4.1 / ISO 37301", "description": "Policy framework currency and documentation",
                     "status": "GREEN" if policy_current else "AMBER",
                     "commentary": "Policy framework is current and version-controlled." if policy_current
                     else "Policies may be out of date. Review against current FCA requirements and update version control."})

    # Policy comprehension
    comp_rate = data.get("governance_policy_comprehension_rate", 0)
    status = _pct_status(comp_rate, 90)
    findings.append({"area": "Governance", "rule": "FCA COCON / SM&CR", "description": f"Employee policy comprehension rate ({comp_rate}%)",
                     "status": status,
                     "commentary": f"Comprehension rate {comp_rate}% vs 90% benchmark. {'On target.' if status == 'GREEN' else 'Launch targeted training for non-compliant staff cohorts.'}"})

    # Decision framework
    decision_fw = data.get("governance_decision_framework", "").lower()
    if decision_fw == "formal":
        findings.append({"area": "Governance", "rule": "OCEG Capability Model", "description": "Formal governance decision-making framework",
                         "status": "GREEN", "commentary": "Formal RACI/escalation framework documented and applied across business lines."})
    elif decision_fw == "informal":
        findings.append({"area": "Governance", "rule": "OCEG Capability Model", "description": "Formal governance decision-making framework",
                         "status": "AMBER", "commentary": "Informal processes create accountability gaps. Formalise RACI and escalation procedures."})
    else:
        findings.append({"area": "Governance", "rule": "OCEG Capability Model", "description": "Formal governance decision-making framework",
                         "status": "RED", "commentary": "No decision-making framework in place. Material governance gap — remediate before next FCA review."})

    return findings


def score_risk(data: dict) -> list:
    findings = []

    # Risk appetite
    risk_appetite = data.get("risk_appetite_defined", False)
    findings.append({"area": "Risk Management", "rule": "COSO ERM / FCA SYSC 7.1", "description": "Risk appetite statement defined and board-approved",
                     "status": "GREEN" if risk_appetite else "RED",
                     "commentary": "Risk appetite statement formally approved by board." if risk_appetite
                     else "No risk appetite statement. FCA expects firms to define risk appetite; absence is a material governance failure."})

    # Risk register
    register = data.get("risk_register_maintained", False)
    last_reviewed_str = data.get("risk_register_last_reviewed", "")
    if register and last_reviewed_str:
        try:
            from datetime import datetime
            last_reviewed = datetime.strptime(last_reviewed_str, "%Y-%m-%d").date()
            days_since = (date.today() - last_reviewed).days
            status = _pct_status(days_since, 30, lower_is_better=True)
            commentary = f"Risk register maintained. Last reviewed {days_since} days ago ({'current' if status == 'GREEN' else 'overdue — review required'})."
        except (ValueError, TypeError):
            status = "AMBER"
            commentary = "Risk register maintained but last review date unreadable — confirm currency."
    elif register:
        status = "AMBER"
        commentary = "Risk register maintained but no review date confirmed. Establish 30-day review cycle."
    else:
        status = "RED"
        commentary = "No risk register in place. Critical gap — implement immediately aligned with COSO ERM."
    findings.append({"area": "Risk Management", "rule": "COSO ERM / ISO 31000", "description": "Risk register maintenance and currency",
                     "status": status, "commentary": commentary})

    # Open critical risks
    critical = data.get("risk_critical_items", 0)
    total_open = data.get("risk_open_items", 0)
    status = "GREEN" if critical == 0 else ("AMBER" if critical <= 2 else "RED")
    findings.append({"area": "Risk Management", "rule": "COSO ERM", "description": f"Open risk items: {total_open} total, {critical} critical",
                     "status": status,
                     "commentary": f"{critical} critical and {total_open} total open risk items. {'All within tolerance.' if status == 'GREEN' else 'Critical items require immediate escalation to board/senior management.'}"})

    # Risk identification process
    risk_proc = data.get("risk_identification_process", "").lower()
    if risk_proc == "automated":
        findings.append({"area": "Risk Management", "rule": "NIST CSF / FCA PS21/3", "description": "Risk identification process",
                         "status": "GREEN", "commentary": "Automated risk identification in place — supports continuous monitoring aligned with PS21/3 operational resilience."})
    elif risk_proc == "manual":
        findings.append({"area": "Risk Management", "rule": "NIST CSF / FCA PS21/3", "description": "Risk identification process",
                         "status": "AMBER", "commentary": "Manual risk identification creates latency. Target <5 day identification response time. Consider GRC platform automation."})
    else:
        findings.append({"area": "Risk Management", "rule": "NIST CSF", "description": "Risk identification process",
                         "status": "RED", "commentary": "No formal risk identification process. Threats may go undetected. Implement structured methodology immediately."})

    # Third-party risk
    tpr = data.get("third_party_risk_assessed", False)
    findings.append({"area": "Risk Management", "rule": "FCA PS26/2 / SYSC 8", "description": "Third-party and supply chain risk assessed",
                     "status": "GREEN" if tpr else "AMBER",
                     "commentary": "Third-party risk assessments conducted and documented." if tpr
                     else "Third-party risk not formally assessed. PS26/2 (effective 18 Mar 2027) requires annual register of material third-party arrangements."})

    return findings


def score_compliance(data: dict) -> list:
    findings = []

    # Regulatory monitoring
    reg_mon = data.get("compliance_regulatory_monitoring", "").lower()
    if reg_mon == "automated":
        findings.append({"area": "Compliance", "rule": "FCA SUP / SM&CR", "description": "Regulatory change monitoring",
                         "status": "GREEN", "commentary": "Automated monitoring of FCA/regulatory updates in place — supports timely policy adaptation."})
    elif reg_mon == "manual":
        findings.append({"area": "Compliance", "rule": "FCA SUP / SM&CR", "description": "Regulatory change monitoring",
                         "status": "AMBER", "commentary": "Manual monitoring creates risk of missed updates. The FCA issues 200+ regulatory changes per day industry-wide."})
    else:
        findings.append({"area": "Compliance", "rule": "FCA SUP 15", "description": "Regulatory change monitoring",
                         "status": "RED", "commentary": "No regulatory monitoring process. Systemic non-compliance risk. Implement formal horizon scanning immediately."})

    # Training completion
    training_rate = data.get("compliance_training_completion_rate", 0)
    status = _pct_status(training_rate, 95)
    findings.append({"area": "Compliance", "rule": "FCA COCON / TC Sourcebook", "description": f"Compliance training completion rate ({training_rate}%)",
                     "status": status,
                     "commentary": f"Training completion {training_rate}% vs 95% target. {'Satisfactory.' if status == 'GREEN' else 'Chase outstanding completions — non-completion may indicate gaps in conduct awareness.'}"})

    # Control effectiveness
    ctrl_eff = data.get("compliance_control_effectiveness", 0)
    status = _pct_status(ctrl_eff, 85)
    findings.append({"area": "Compliance", "rule": "COSO / FCA SYSC 6", "description": f"Control effectiveness rate ({ctrl_eff}%)",
                     "status": status,
                     "commentary": f"Control effectiveness {ctrl_eff}% vs 85% benchmark. {'Controls operating effectively.' if status == 'GREEN' else 'Remediate failing controls — prioritise those linked to FCA-regulated activities.'}"})

    # Open audit findings
    open_findings = data.get("compliance_audit_findings_open", 0)
    status = "GREEN" if open_findings == 0 else ("AMBER" if open_findings <= 5 else "RED")
    findings.append({"area": "Compliance", "rule": "FCA SYSC / Internal Audit Standards", "description": f"Open audit findings ({open_findings})",
                     "status": status,
                     "commentary": f"{open_findings} open audit finding(s). {'All remediated.' if open_findings == 0 else 'Prioritise remediation — FCA expects timely closure of audit findings, particularly those affecting client protection.'}"})

    # FCA regulatory changes tracked
    fca_tracked = data.get("fca_regulatory_changes_tracked", False)
    findings.append({"area": "Compliance", "rule": "FCA SUP 15.3 / SM&CR", "description": "FCA regulatory change tracking",
                     "status": "GREEN" if fca_tracked else "AMBER",
                     "commentary": "FCA regulatory updates formally tracked and actioned." if fca_tracked
                     else "FCA regulatory change tracking not confirmed. New rules effective in 2026 include CASS 7.11.32R, CASS 15, PS26/2 (March 2027), COCON 1.1.7FR."})

    # GRC platform
    grc_platform = data.get("grc_platform_in_use", False)
    findings.append({"area": "Compliance", "rule": "OCEG Best Practice", "description": "GRC platform / integrated tooling",
                     "status": "GREEN" if grc_platform else "AMBER",
                     "commentary": "Integrated GRC platform in use — supports real-time monitoring, audit trails, and reporting." if grc_platform
                     else "No integrated GRC platform. Manual processes create reporting gaps. GRC tooling can reduce compliance costs by ~40% (industry data)."})

    return findings


def derive_maturity_level(gov_findings, risk_findings, comp_findings) -> int:
    """Derive an overall GRC maturity level from findings distribution."""
    all_findings = gov_findings + risk_findings + comp_findings
    counts = rag_counts(all_findings)
    total = len(all_findings)
    if total == 0:
        return 1
    red_pct   = counts["RED"]   / total
    amber_pct = counts["AMBER"] / total
    green_pct = counts["GREEN"] / total
    if red_pct >= 0.4:                                return 1
    if red_pct >= 0.2 or green_pct < 0.4:            return 2
    if amber_pct >= 0.4 or green_pct < 0.6:          return 3
    if green_pct >= 0.8 and amber_pct <= 0.1:        return 4
    return 4  # Cap at 4 unless perfect — 5 requires deep validation


def build_report(data: dict, gov_f: list, risk_f: list, comp_f: list,
                 client_name: str, intel: dict = None):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx import Document
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement

    doc = Document()

    # ── Title ──
    title = doc.add_heading("GRC Intelligence Report", level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph(
        f"Prepared for: {data.get('firm_name', client_name)}\n"
        f"{reg_id_label(data)}: {data.get('frn', 'N/A')}\n"
        f"Assessment Period: {data.get('assessment_period', 'Annual Review')}\n"
        f"Report Date: {date.today().strftime('%d %B %Y')}\n"
        f"Framework: OCEG GRC Capability Model · COSO ERM · NIST CSF · ISO 31000 · FCA Regulatory Lens\n"
        f"Prepared by: CASS Intelligence Reports"
    )
    doc.add_paragraph(
        "CONFIDENTIAL — This report is for the exclusive use of the named firm. "
        "It does not constitute legal or regulatory advice."
    ).runs[0].font.italic = True

    # ── Section 1: Executive Summary ──
    all_findings = gov_f + risk_f + comp_f
    counts = rag_counts(all_findings)
    maturity = derive_maturity_level(gov_f, risk_f, comp_f)
    mat_name, mat_desc = MATURITY_LEVELS[maturity]

    doc.add_heading("1. Executive Summary", level=1)
    gov_score  = round(100 * sum(1 for f in gov_f  if f["status"] == "GREEN") / max(len(gov_f),  1))
    risk_score = round(100 * sum(1 for f in risk_f if f["status"] == "GREEN") / max(len(risk_f), 1))
    comp_score = round(100 * sum(1 for f in comp_f if f["status"] == "GREEN") / max(len(comp_f), 1))
    overall    = round((gov_score + risk_score + comp_score) / 3)

    doc.add_paragraph(
        f"This GRC Intelligence Report assessed {len(all_findings)} control points across Governance, "
        f"Risk Management, and Compliance for {data.get('firm_name', client_name)}.\n\n"
        f"  • Overall GRC Score:      {overall}/100\n"
        f"  • Governance Score:       {gov_score}/100\n"
        f"  • Risk Management Score:  {risk_score}/100\n"
        f"  • Compliance Score:       {comp_score}/100\n\n"
        f"GRC Maturity Level: {maturity} — {mat_name}\n"
        f"{mat_desc}\n\n"
        f"Findings: {counts['GREEN']} PASS  |  {counts['AMBER']} REQUIRES ATTENTION  |  {counts['RED']} FAIL"
    )

    if counts["RED"] > 0:
        p = doc.add_paragraph(
            f"IMMEDIATE ACTION REQUIRED: {counts['RED']} critical finding(s). See Section 7 — Remediation Plan."
        )
        p.runs[0].font.bold = True

    # ── Section 2: Firm Profile ──
    doc.add_heading("2. Firm Profile", level=1)
    profile_rows = [
        ("Firm Name",           data.get("firm_name", client_name)),
        (reg_id_label(data),    data.get("frn", "N/A")),
        ("Assessment Period",   data.get("assessment_period", "Annual Review")),
        ("Assessment Date",     date.today().strftime("%d %B %Y")),
        ("GRC Framework",       "OCEG · COSO ERM · NIST CSF · ISO 31000"),
        ("GRC Maturity Level",  f"{maturity} — {mat_name}"),
        ("Overall GRC Score",   f"{overall}/100"),
    ]
    tbl = doc.add_table(rows=len(profile_rows), cols=2)
    tbl.style = "Table Grid"
    for i, (lbl, val) in enumerate(profile_rows):
        tbl.rows[i].cells[0].text = lbl
        tbl.rows[i].cells[1].text = str(val)
        if tbl.rows[i].cells[0].paragraphs[0].runs:
            tbl.rows[i].cells[0].paragraphs[0].runs[0].font.bold = True

    # ── Section 3: GRC Maturity Model ──
    doc.add_heading("3. GRC Maturity Assessment", level=1)
    doc.add_paragraph(
        f"The firm is assessed at Maturity Level {maturity} ({mat_name}). "
        "The five-level maturity model is based on the OCEG GRC Capability Model and industry benchmarks."
    )
    mat_tbl = doc.add_table(rows=6, cols=3)
    mat_tbl.style = "Table Grid"
    for j, h in enumerate(["Level", "Stage", "Description"]):
        header_cell(mat_tbl.rows[0].cells[j], h)
    for lvl in range(1, 6):
        name, desc = MATURITY_LEVELS[lvl]
        row = mat_tbl.rows[lvl]
        row.cells[0].text = str(lvl)
        row.cells[1].text = name
        row.cells[2].text = desc
        if lvl == maturity:
            set_cell_bg(row.cells[0], RAG_BG.get("GREEN" if maturity >= 4 else ("AMBER" if maturity >= 3 else "RED"), "888888"))
            set_cell_bg(row.cells[1], RAG_BG.get("GREEN" if maturity >= 4 else ("AMBER" if maturity >= 3 else "RED"), "888888"))
            if row.cells[0].paragraphs[0].runs:
                row.cells[0].paragraphs[0].runs[0].font.color.rgb = WHITE
                row.cells[0].paragraphs[0].runs[0].font.bold = True
            if row.cells[1].paragraphs[0].runs:
                row.cells[1].paragraphs[0].runs[0].font.color.rgb = WHITE
                row.cells[1].paragraphs[0].runs[0].font.bold = True

    # ── Section 4: KPI Dashboard ──
    doc.add_heading("4. GRC KPI Dashboard", level=1)
    doc.add_paragraph("Key Performance Indicators benchmarked against financial services industry targets (Concertium / OCEG framework).")

    kpi_data = [
        ("Policy Comprehension Rate",           f"{data.get('governance_policy_comprehension_rate', 0)}%",       "90%",   _pct_status(data.get('governance_policy_comprehension_rate', 0), 90)),
        ("Board GRC Agenda Coverage",           "Reported" if data.get("governance_board_oversight") == "Strong" else "Partial", "85%+", "GREEN" if data.get("governance_board_oversight", "").lower() == "strong" else "AMBER"),
        ("Training Completion Rate",            f"{data.get('compliance_training_completion_rate', 0)}%",        "95%",   _pct_status(data.get('compliance_training_completion_rate', 0), 95)),
        ("Control Effectiveness Rate",          f"{data.get('compliance_control_effectiveness', 0)}%",           "85%",   _pct_status(data.get('compliance_control_effectiveness', 0), 85)),
        ("Open Audit Findings",                 str(data.get("compliance_audit_findings_open", 0)),              "0",     "GREEN" if data.get("compliance_audit_findings_open", 0) == 0 else ("AMBER" if data.get("compliance_audit_findings_open", 0) <= 5 else "RED")),
        ("Open Critical Risk Items",            str(data.get("risk_critical_items", 0)),                         "0",     "GREEN" if data.get("risk_critical_items", 0) == 0 else ("AMBER" if data.get("risk_critical_items", 0) <= 2 else "RED")),
        ("Risk Register Currency",              "Current" if data.get("risk_register_maintained") else "Unknown","≤30d",  "GREEN" if data.get("risk_register_maintained") else "RED"),
        ("Third-Party Risk Assessed",           "Yes" if data.get("third_party_risk_assessed") else "No",        "Yes",   "GREEN" if data.get("third_party_risk_assessed") else "AMBER"),
        ("Regulatory Change Tracking",          "Active" if data.get("fca_regulatory_changes_tracked") else "None","Active","GREEN" if data.get("fca_regulatory_changes_tracked") else "AMBER"),
        ("GRC Platform in Use",                 "Yes" if data.get("grc_platform_in_use") else "No",              "Yes",   "GREEN" if data.get("grc_platform_in_use") else "AMBER"),
    ]

    kpi_tbl = doc.add_table(rows=1 + len(kpi_data), cols=4)
    kpi_tbl.style = "Table Grid"
    for j, h in enumerate(["KPI", "Current", "Target", "Status"]):
        header_cell(kpi_tbl.rows[0].cells[j], h)
    for i, (kpi, current, target, status) in enumerate(kpi_data):
        row = kpi_tbl.rows[i + 1]
        row.cells[0].text = kpi
        row.cells[1].text = current
        row.cells[2].text = target
        rag_cell(row.cells[3], status)

    # ── Section 5: Governance Findings ──
    add_findings_table(doc, gov_f, "Governance Findings", 5)

    # ── Section 6: Risk Management Findings ──
    add_findings_table(doc, risk_f, "Risk Management Findings", 6)

    # ── Section 7: Compliance Findings ──
    add_findings_table(doc, comp_f, "Compliance Findings", 7)

    # ── Section 8: Findings Summary ──
    add_summary_table(doc, all_findings, 8)

    # ── Section 9: Remediation Plan ──
    add_remediation_table(doc, all_findings, 9)

    # ── Section 10: FCA Enforcement Context ──
    add_enforcement_section(doc, REPORT_TYPE, 10)

    # ── Section 11: Regulatory Updates ──
    add_regulatory_updates_section(doc, REPORT_TYPE, 11)

    # ── Section 12: Live Intelligence ──
    sec = 12
    if intel:
        add_intel_section(doc, intel, sec)
        sec += 1

    # ── Regulatory References ──
    country = data.get("country", "") or data.get("jurisdiction", "")
    regional_refs = regional_regulatory_refs(data.get("region", "") or country)
    add_regulatory_refs(doc, [
        ("OCEG GRC Capability Model", "Principal GRC framework — Learn, Align, Perform, Review cycle"),
        ("COSO ERM 2017",             "Enterprise Risk Management — Integrating with Strategy and Performance"),
        ("ISO 31000:2018",            "Risk Management — Guidelines"),
        ("NIST CSF 2.0",              "Cybersecurity risk management framework"),
        ("FCA SYSC 4.1",              "Senior management arrangements, systems and controls"),
        ("FCA SYSC 6.1",              "Compliance function requirements"),
        ("FCA SYSC 7.1",              "Risk management requirements"),
        ("FCA SYSC 8",                "Outsourcing and third-party risk"),
        ("FCA SM&CR / COCON",         "Senior Managers & Certification Regime — individual accountability"),
        ("FCA PS26/2",                "Operational Incident & Third-Party Reporting (in force 18 Mar 2027)"),
        ("COCON 1.1.7FR",             "Non-financial misconduct — in scope from 1 Sep 2026"),
        ("FCA Handbook",              "https://www.handbook.fca.org.uk"),
    ] + regional_refs, sec)

    return doc


def main():
    parser = argparse.ArgumentParser(description="Generate a GRC Intelligence Report")
    parser.add_argument("--client", required=True, help="Client name (used to find input JSON in .tmp/)")
    parser.add_argument("--no-scan", action="store_true", help="Skip Routing Intelligence Scan")
    args = parser.parse_args()

    client_name = args.client.replace(" ", "_")
    print(f"Loading GRC data for: {client_name}")
    data = load_client_data("grc", client_name)

    intel = {}
    if not args.no_scan:
        country = data.get("country", "") or data.get("jurisdiction", "")
        region  = detect_region(data.get("region") or country) if (data.get("region") or country) else None
        intel = run_perplexity_scan(REPORT_TYPE, region=region, country=country)
    else:
        print("Routing Intelligence Scan skipped (--no-scan)")

    print("Scoring Governance...")
    gov_f  = score_governance(data)
    print("Scoring Risk Management...")
    risk_f = score_risk(data)
    print("Scoring Compliance...")
    comp_f = score_compliance(data)

    all_f = gov_f + risk_f + comp_f
    counts = rag_counts(all_f)
    maturity = derive_maturity_level(gov_f, risk_f, comp_f)
    mat_name, _ = MATURITY_LEVELS[maturity]
    print(f"GRC Maturity: Level {maturity} — {mat_name}")
    print(f"Findings: {counts['GREEN']} PASS | {counts['AMBER']} REQUIRES ATTENTION | {counts['RED']} FAIL")

    print("Building report document...")
    doc = build_report(data, gov_f, risk_f, comp_f, client_name, intel=intel)

    output_path = save_report(doc, "grc", client_name)
    print(f"Report saved to: {output_path}")


if __name__ == "__main__":
    main()
