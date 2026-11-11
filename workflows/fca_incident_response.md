# Workflow: FCA Incident Response Report

## Objective
Document a regulatory incident, assess whether FCA notification obligations have been met, produce a post-incident report suitable for submission to the FCA, and confirm remediation actions.

---

## Regulatory Basis
| Rule | Summary |
|---|---|
| SUP 15.3.1R | Obligation to notify FCA of material events |
| SUP 15.3.8R | Notification as soon as practicable (typically same/next business day) |
| SUP 15.3.11R | Content of notification — nature, impact, remediation |
| CASS 7.13.65R | CASS client money breach notification |
| CASS 6.6.54R | CASS custody asset breach notification |
| PS21/3 | Operational incident impact tolerance breach reporting |
| GDPR / UK GDPR | Data breach notification to ICO within 72 hours |

---

## Required Inputs
- [ ] Firm name and FCA FRN
- [ ] Incident date and time
- [ ] Incident type (CASS breach / cyber / operational / data breach / other)
- [ ] Description of incident
- [ ] Client assets / money affected? (yes/no, amount if applicable)
- [ ] Number of clients affected
- [ ] Root cause (known/under investigation)
- [ ] Was FCA notified? (yes/no)
- [ ] FCA notification date and reference number
- [ ] Was ICO notified? (yes/no, for data breaches)
- [ ] Incident contained? (yes/no)
- [ ] Containment date
- [ ] Remediation actions taken
- [ ] Lessons learned

---

## Steps
### Step 1 — Collect incident data → `.tmp/fca_ir_<client>_input.json`
### Step 2 — Run scan and generate report
```bash
python tools/generate_fca_incident_response.py --client "<client_name>"
```
### Step 3 — Legal/compliance review before FCA submission
### Step 4 — Finalise, submit to FCA if required, deliver to client

---

## Report Structure
```
1. Firm Profile
2. Incident Summary
3. Timeline of Events
4. FCA Notification Assessment
5. Client Impact Assessment
6. Containment & Remediation
7. Root Cause Analysis
8. Lessons Learned
9. Findings Summary (RAG)
10. Live Regulatory Intelligence
11. Regulatory References
```

---

## Auto-Fail Triggers (RED)
- FCA not notified of a notifiable incident
- Notification made more than 1 business day after discovery
- Client assets affected and not segregated/protected
- ICO not notified within 72 hours of a data breach

---

## Notes
- Always involve legal counsel before submitting to FCA
- SUP 15.3.8R: FCA expects notification "as soon as practicable" — do not wait for full investigation
- FCA incident notification: https://www.fca.org.uk/firms/supervision/how-to-notify-fca
