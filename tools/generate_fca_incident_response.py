"""
FCA Incident Response Report Generator
Usage: python tools/generate_fca_incident_response.py --client "<client_name>" [--no-scan]
"""

import argparse
from datetime import datetime, date
from dotenv import load_dotenv
from report_base import *
from regional_routing import detect_region, regional_regulatory_refs

load_dotenv()
REPORT_TYPE = "fca_incident_response"
PREFIX = "fca_ir"


def hours_since(dt_str: str) -> float:
    try:
        dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M")
        return (datetime.now() - dt).total_seconds() / 3600
    except Exception:
        return None


def score_checks(data: dict) -> list:
    findings = []
    incident_type = data.get("incident_type", "unknown")
    is_data_breach = "data" in incident_type.lower()
    is_cass = "cass" in incident_type.lower()

    # FCA notifiable?
    fca_notified = data.get("fca_notified")
    incident_dt = data.get("incident_datetime")
    notification_dt = data.get("fca_notification_datetime")

    if fca_notified is True:
        # Check timeliness
        if incident_dt and notification_dt:
            inc_time = datetime.strptime(incident_dt, "%Y-%m-%dT%H:%M")
            not_time = datetime.strptime(notification_dt, "%Y-%m-%dT%H:%M")
            hours = (not_time - inc_time).total_seconds() / 3600
            if hours <= 24:
                s, c = "GREEN", f"FCA notified within {hours:.1f} hours of incident discovery."
            else:
                s, c = "AMBER", f"FCA notified after {hours:.1f} hours. SUP 15.3.8R expects notification as soon as practicable (same/next business day)."
        else:
            s, c = "GREEN", f"FCA notified. Ref: {data.get('fca_notification_reference', 'N/A')}."
    elif fca_notified is False:
        s, c = "RED", "FCA NOT notified. If this is a notifiable event, immediate notification required under SUP 15.3.1R."
    else:
        s, c = "AMBER", "FCA notification status unknown. Confirm with compliance team."
    findings.append({"area": "FCA Notification", "rule": "SUP 15.3.1R / SUP 15.3.8R", "description": "FCA notified of material incident", "status": s, "commentary": c})

    # ICO notification (data breaches only)
    if is_data_breach:
        ico_notified = data.get("ico_notified")
        if ico_notified is True:
            findings.append({"area": "ICO Notification", "rule": "UK GDPR Article 33", "description": "ICO notified within 72 hours", "status": "GREEN", "commentary": "ICO notification confirmed."})
        elif ico_notified is False:
            findings.append({"area": "ICO Notification", "rule": "UK GDPR Article 33", "description": "ICO notified within 72 hours", "status": "RED", "commentary": "ICO NOT notified. UK GDPR Article 33 requires notification within 72 hours of a personal data breach."})
        else:
            findings.append({"area": "ICO Notification", "rule": "UK GDPR Article 33", "description": "ICO notification status", "status": "AMBER", "commentary": "ICO notification status not confirmed. Review if personal data was affected."})

    # CASS-specific
    if is_cass:
        client_assets_affected = data.get("client_assets_affected")
        amount = data.get("client_assets_amount", "unknown")
        findings.append({
            "area": "CASS Breach", "rule": "CASS 7.13.65R / CASS 6.6.54R",
            "description": "CASS breach assessment",
            "status": "RED" if client_assets_affected else "GREEN",
            "commentary": f"Client assets affected: £{amount}. CASS breach notification requirements apply." if client_assets_affected
            else "No client assets confirmed affected.",
        })

    # Incident contained
    contained = data.get("incident_contained")
    containment_date = data.get("containment_date", "pending")
    findings.append({
        "area": "Containment", "rule": "FCA SYSC",
        "description": "Incident contained",
        "status": "GREEN" if contained else "RED",
        "commentary": f"Incident contained as of {containment_date}." if contained else "Incident NOT yet contained. Active incident — immediate escalation required.",
    })

    # Root cause
    root_cause = data.get("root_cause")
    findings.append({
        "area": "Root Cause", "rule": "SUP 15.3.11R",
        "description": "Root cause identified",
        "status": "GREEN" if root_cause and root_cause.lower() != "under investigation" else "AMBER",
        "commentary": f"Root cause: {root_cause}." if root_cause else "Root cause under investigation. Update FCA notification when determined.",
    })

    # Remediation
    remediation = data.get("remediation_actions")
    findings.append({
        "area": "Remediation", "rule": "SUP 15.3.11R",
        "description": "Remediation actions documented",
        "status": "GREEN" if remediation else "AMBER",
        "commentary": f"Remediation actions: {remediation}." if remediation else "Remediation actions not yet documented.",
    })

    # Lessons learned
    lessons = data.get("lessons_learned")
    findings.append({
        "area": "Lessons Learned", "rule": "PS21/3",
        "description": "Post-incident lessons learned documented",
        "status": "GREEN" if lessons else "AMBER",
        "commentary": f"Lessons learned documented." if lessons else "Lessons learned not yet documented. Required for FCA operational resilience compliance.",
    })

    return findings


def build_report(data: dict, findings: list, client_name: str, intel: dict = None) -> Document:
    doc = start_document("FCA Incident Response Report", data, client_name)
    counts = rag_counts(findings)

    doc.add_heading("2. Incident Summary", level=1)
    doc.add_paragraph(
        f"Incident type: {data.get('incident_type', 'N/A')}\n"
        f"Incident date/time: {data.get('incident_datetime', 'N/A')}\n"
        f"Clients affected: {data.get('clients_affected', 'N/A')}\n"
        f"Status: {'CONTAINED' if data.get('incident_contained') else 'ACTIVE'}\n"
        f"Assessment: {counts['GREEN']} PASS | {counts['AMBER']} ATTENTION | {counts['RED']} FAIL"
    )
    if counts["RED"]:
        doc.add_paragraph(f"CRITICAL: {counts['RED']} compliance gap(s). Review FCA notification obligations immediately.").runs[0].font.bold = True

    add_firm_profile(doc, data, client_name, [
        ("Incident Type", data.get("incident_type", "N/A")),
        ("Incident Date/Time", data.get("incident_datetime", "N/A")),
        ("FCA Notification Ref", data.get("fca_notification_reference", "N/A")),
    ])

    # Timeline
    doc.add_heading("4. Timeline of Events", level=1)
    timeline = data.get("timeline", [])
    if timeline:
        tbl = doc.add_table(rows=1 + len(timeline), cols=2)
        tbl.style = "Table Grid"
        header_cell(tbl.rows[0].cells[0], "Date/Time")
        header_cell(tbl.rows[0].cells[1], "Event")
        for i, event in enumerate(timeline):
            tbl.rows[i + 1].cells[0].text = event.get("datetime", "")
            tbl.rows[i + 1].cells[1].text = event.get("event", "")
    else:
        doc.add_paragraph("Detailed timeline not provided. Add key events for FCA submission.")

    add_findings_table(doc, [f for f in findings if "Notification" in f["area"]], "Notification Compliance", 5)
    add_findings_table(doc, [f for f in findings if f["area"] in ("Containment", "Root Cause", "Remediation", "Lessons Learned", "CASS Breach")], "Containment, Remediation & Lessons", 6)
    add_summary_table(doc, findings, 7)
    add_remediation_table(doc, findings, 8)
    add_intel_section(doc, intel, 9)
    country = data.get("country", "") or data.get("jurisdiction", "")
    regional_refs = regional_regulatory_refs(data.get("region", "") or country)
    add_regulatory_refs(doc, [
        ("SUP 15.3.1R", "Obligation to notify FCA of material events"),
        ("SUP 15.3.8R", "Notification as soon as practicable"),
        ("SUP 15.3.11R", "Content of FCA notification"),
        ("UK GDPR Article 33", "ICO data breach notification within 72 hours"),
        ("CASS 7.13.65R", "CASS (Client Assets Sourcebook) client money breach notification"),
        ("FCA Incident Notification", "https://www.fca.org.uk/firms/supervision/how-to-notify-fca"),
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
    doc = build_report(data, findings, client_name, intel)
    path = save_report(doc, PREFIX, client_name)
    print(f"Report saved: {path}")


if __name__ == "__main__":
    main()
