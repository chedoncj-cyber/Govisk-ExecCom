"""
CASS Breach Log & Remediation Report Generator
Usage: python tools/generate_cass_breach_log.py --client "<client_name>" [--no-scan]
"""

import argparse
import sys
from datetime import datetime, date
from pathlib import Path
from dotenv import load_dotenv
from report_base import *
from regional_routing import detect_region, score_regional_client_money, regional_regulatory_refs
from regional_cass_equivalents import score_regional_breach_log, BREACH_LOG_TITLES

load_dotenv()

# ── Shared observability ───────────────────────────────────────────────────────
_SHARED = Path(__file__).parent.parent.parent / "shared"
sys.path.insert(0, str(_SHARED))
from observability import get_logger, metrics, trace_op

REPORT_TYPE = "cass_breach_log"
PREFIX = "cass_bl"

_BL_SLUGS = {
    "north-america": "N. America", "latin-america": "Latin America",
    "asia-pacific": "Asia Pacific", "europe": "Europe", "africa": "Africa",
}


def _parse_bool(val) -> bool:
    if isinstance(val, bool):
        return val
    return str(val).strip().lower() in ("true", "yes", "1")


def normalise_data(data: dict) -> dict:
    """
    The portal form submits flat fields for a single breach.
    Wrap them into the breaches list that score_checks() expects.
    Skipped if data already contains a 'breaches' key (e.g. direct API post).
    """
    if "breaches" in data:
        return data

    status_map = {"Closed": "complete", "Monitoring": "in-progress", "Open": "open"}
    form_status = data.get("remediation_status", "")
    mapped_status = status_map.get(form_status, form_status.lower())

    breach_date = data.get("breach_date", "")
    if breach_date or data.get("rule_breached"):
        single_breach = {
            "date": breach_date,
            "type": data.get("breach_type", ""),
            "rule_breached": data.get("rule_breached", "CASS"),
            "fca_notified": _parse_bool(data.get("fca_notified", False)),
            "notification_required": _parse_bool(data.get("notification_required", True)),
            "notification_date": data.get("notification_date", ""),
            "remediation_status": mapped_status,
            "root_cause_analysis": data.get("root_cause_analysis", ""),
        }
        data = {**data, "breaches": [single_breach]}

    return data


@trace_op("score_breach_log")
def score_checks(data: dict) -> list:
    _r = _BL_SLUGS.get((data.get("region") or "").strip().lower())
    if _r:
        return score_regional_breach_log(data, _r)

    findings = []
    breaches = data.get("breaches", [])

    # Breach register
    register = _parse_bool(data.get("breach_register_maintained", False))
    findings.append({
        "area": "Breach Register", "rule": "CASS 7.13.65R",
        "description": "Formal breach register maintained",
        "status": "GREEN" if register else "RED",
        "commentary": "Breach register confirmed maintained." if register else "No breach register. Required under CASS 7.13.65R and CASS 6.6.54R.",
    })

    if not breaches:
        findings.append({
            "area": "Breach History", "rule": "SUP 15.3",
            "description": "CASS breaches in review period",
            "status": "GREEN",
            "commentary": "No CASS breaches reported in the review period.",
        })
        return findings

    # Per-breach checks
    fca_missed = 0
    outstanding_remediations = 0
    repeat_types = {}

    for i, breach in enumerate(breaches, 1):
        breach_date = breach.get("date", "unknown")
        breach_type = breach.get("type", "unknown")
        rule = breach.get("rule_breached", "CASS")
        notified = _parse_bool(breach.get("fca_notified", False))
        notification_required = _parse_bool(breach.get("notification_required", True))
        remediation_status = breach.get("remediation_status", "").lower()
        root_cause = breach.get("root_cause_analysis", False)

        # Track repeats
        repeat_types[breach_type] = repeat_types.get(breach_type, 0) + 1

        # FCA notification
        if notification_required:
            if notified:
                notif_date = breach.get("notification_date", "date unknown")
                findings.append({
                    "area": f"Breach {i} — {breach_date}", "rule": "SUP 15.3.8R",
                    "description": f"FCA notified: {breach_type}",
                    "status": "GREEN",
                    "commentary": f"FCA notified on {notif_date}.",
                })
            else:
                fca_missed += 1
                findings.append({
                    "area": f"Breach {i} — {breach_date}", "rule": "SUP 15.3.8R",
                    "description": f"FCA notification MISSED: {breach_type}",
                    "status": "RED",
                    "commentary": f"Material breach of {rule} — FCA NOT notified. SUP 15.3.8R requires prompt notification.",
                })

        # Remediation
        if remediation_status == "complete":
            rem_status = "GREEN"
            rem_comment = f"Remediation complete."
        elif remediation_status == "in-progress":
            breach_dt = breach.get("date")
            if breach_dt:
                days_open = (date.today() - datetime.strptime(breach_dt, "%Y-%m-%d").date()).days
                if days_open > 30:
                    outstanding_remediations += 1
                    rem_status = "RED"
                    rem_comment = f"Remediation in-progress for {days_open} days. Escalation required."
                else:
                    rem_status = "AMBER"
                    rem_comment = f"Remediation in-progress ({days_open} days)."
            else:
                rem_status = "AMBER"
                rem_comment = "Remediation in-progress — date unknown."
        else:
            outstanding_remediations += 1
            rem_status = "RED"
            rem_comment = f"Remediation OUTSTANDING for breach on {breach_date}."

        findings.append({
            "area": f"Breach {i} — {breach_date}", "rule": rule,
            "description": f"Remediation: {breach_type}",
            "status": rem_status, "commentary": rem_comment,
        })

        # Root cause analysis
        findings.append({
            "area": f"Breach {i} — {breach_date}", "rule": "CASS 7.13.65R",
            "description": f"Root cause analysis performed: {breach_type}",
            "status": "GREEN" if root_cause else "AMBER",
            "commentary": "Root cause analysis completed." if root_cause else "Root cause analysis not completed. Required to prevent recurrence.",
        })

    # Repeat breaches
    repeats = {t: n for t, n in repeat_types.items() if n > 1}
    if repeats:
        for bt, count in repeats.items():
            findings.append({
                "area": "Repeat Breaches", "rule": "SUP 15.3",
                "description": f"Repeat breach: {bt}",
                "status": "RED",
                "commentary": f"{count} instances of '{bt}' breach. Repeat breaches indicate systemic failure. Root cause resolution required.",
            })
    else:
        findings.append({
            "area": "Repeat Breaches", "rule": "SUP 15.3",
            "description": "No repeat breach types",
            "status": "GREEN", "commentary": "No repeat breach types identified in review period.",
        })

    regional_findings = score_regional_client_money(data)
    findings.extend(regional_findings)
    return findings


@trace_op("build_breach_log_report")
def build_report(data: dict, findings: list, client_name: str, intel: dict = None) -> Document:
    slug = (data.get("region") or "").strip().lower()
    _r = _BL_SLUGS.get(slug, "UK")
    _title = BREACH_LOG_TITLES.get(_r, BREACH_LOG_TITLES["UK"])
    doc = start_document(_title, data, client_name)
    counts = rag_counts(findings)
    breaches = data.get("breaches", [])

    doc.add_heading("2. Executive Summary", level=1)
    doc.add_paragraph(
        f"Compliance breach log review for {data.get('firm_name', client_name)}. "
        f"{len(breaches)} breach(es) in review period. "
        f"Assessment: {counts['GREEN']} PASS | {counts['AMBER']} ATTENTION | {counts['RED']} FAIL."
    )
    if counts["RED"]:
        doc.add_paragraph(f"CRITICAL: {counts['RED']} failure(s) — regulator notification gaps or outstanding remediations detected.").runs[0].font.bold = True

    add_firm_profile(doc, data, client_name, [("Breaches in Period", str(len(breaches)))])

    # Breach detail log table
    if breaches and _r == "UK":
        doc.add_heading("4. Breach Detail Log", level=1)
        tbl = doc.add_table(rows=1 + len(breaches), cols=5)
        tbl.style = "Table Grid"
        for j, h in enumerate(["Date", "Type", "Rule", "FCA Notified", "Remediation"]):
            header_cell(tbl.rows[0].cells[j], h)
        for i, b in enumerate(breaches):
            row = tbl.rows[i + 1]
            row.cells[0].text = b.get("date", "")
            row.cells[1].text = b.get("type", "")
            row.cells[2].text = b.get("rule_breached", "")
            notified = b.get("fca_notified")
            row.cells[3].text = "YES" if notified else ("N/A" if not b.get("notification_required", True) else "NO — MISSED")
            if not notified and b.get("notification_required", True):
                set_cell_bg(row.cells[3], RAG_BG["RED"])
                if row.cells[3].paragraphs[0].runs:
                    row.cells[3].paragraphs[0].runs[0].font.color.rgb = WHITE
            row.cells[4].text = b.get("remediation_status", "unknown").upper()
    elif breaches:
        doc.add_heading("4. Breach Detail Log", level=1)
        tbl = doc.add_table(rows=1 + len(breaches), cols=5)
        tbl.style = "Table Grid"
        for j, h in enumerate(["Date", "Type", "Rule", "Regulator Notified", "Remediation"]):
            header_cell(tbl.rows[0].cells[j], h)
        for i, b in enumerate(breaches):
            row = tbl.rows[i + 1]
            row.cells[0].text = b.get("date", "")
            row.cells[1].text = b.get("type", "")
            row.cells[2].text = b.get("rule_breached", "")
            notified = b.get("fca_notified")
            row.cells[3].text = "YES" if notified else ("N/A" if not b.get("notification_required", True) else "NO — MISSED")
            if not notified and b.get("notification_required", True):
                set_cell_bg(row.cells[3], RAG_BG["RED"])
                if row.cells[3].paragraphs[0].runs:
                    row.cells[3].paragraphs[0].runs[0].font.color.rgb = WHITE
            row.cells[4].text = b.get("remediation_status", "unknown").upper()

    if _r == "UK":
        add_findings_table(doc, [f for f in findings if "Breach Register" in f["area"] or "Breach History" in f["area"]], "Breach Register Assessment", 5)
        add_findings_table(doc, [f for f in findings if "Repeat" in f["area"]], "Repeat Breach Analysis", 6)
    else:
        add_findings_table(doc, findings, "Compliance Breach Findings", 5)
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
        ("CASS 7.13.65R", "Client money breach identification, recording and notification"),
        ("CASS 6.6.54R", "Custody breach identification, recording and notification"),
        ("SUP 15.3", "FCA notification of material breaches"),
        ("SUP 15.3.8R", "Notification as soon as practicable"),
        ("FCA Enforcement Register", "https://www.fca.org.uk/firms/financial-services-register"),
        ("FCA Handbook SUP 15", "https://www.handbook.fca.org.uk/handbook/SUP/15/"),
    ] + regional_refs, next_sec)
    return doc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", required=True)
    parser.add_argument("--no-scan", action="store_true")
    args = parser.parse_args()
    client_name = args.client.replace(" ", "_")
    data = load_client_data(PREFIX, client_name)
    data = normalise_data(data)
    country = data.get("country", "") or data.get("jurisdiction", "")
    region  = detect_region(data.get("region") or country) if (data.get("region") or country) else None
    intel = {} if args.no_scan else run_perplexity_scan(REPORT_TYPE, region=region, country=country)
    findings = score_checks(data)
    counts = rag_counts(findings)
    print(f"Results: {counts['GREEN']} PASS | {counts['AMBER']} ATTENTION | {counts['RED']} FAIL")
    doc = build_report(data, findings, client_name, intel)
    path = save_report(doc, PREFIX, client_name)
    metrics.inc("report_generated", report_type="cass_breach_log")
    print(f"Report saved: {path}")


if __name__ == "__main__":
    main()
