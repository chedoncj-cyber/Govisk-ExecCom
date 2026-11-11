# Workflow: CASS Breach Log & Remediation Report

## Objective
Document all CASS breaches identified within the review period, assess whether FCA notification obligations were met, and confirm that remediation actions are complete or on track.

---

## Regulatory Basis
| Rule | Summary |
|---|---|
| CASS 7.13.65R | Requirement to identify, record and notify CASS client money breaches |
| CASS 6.6.54R | Requirement to identify, record and notify CASS custody breaches |
| SUP 15.3 | FCA notification of material breaches |
| SUP 15.3.8R | Notification must be made as soon as practicable |
| COBS 10A | Client money breach reporting obligations |

---

## Required Inputs
- [ ] Firm name and FCA FRN
- [ ] List of all CASS breaches in review period (each breach: date, type, rule breached, amount/assets affected, root cause)
- [ ] For each breach: Was FCA notified? (yes/no/not required)
- [ ] For each breach: Notification date (if applicable)
- [ ] For each breach: Remediation action taken
- [ ] For each breach: Remediation status (complete/in-progress/outstanding)
- [ ] Breach register maintained? (yes/no)
- [ ] Root cause analysis performed for each breach? (yes/no)
- [ ] Any repeat breaches of the same type?

---

## Steps
### Step 1 — Collect client data → `.tmp/cass_bl_<client>_input.json`
### Step 2 — Run scan and generate report
```bash
python tools/generate_cass_breach_log.py --client "<client_name>"
```
### Step 3 — Review, annotate, finalise and deliver

---

## Report Structure
```
1. Firm Profile
2. Executive Summary
3. Breach Register Assessment
4. Breach Detail Log
5. FCA Notification Compliance
6. Remediation Status
7. Repeat Breach Analysis
8. Findings Summary (RAG)
9. Remediation Action Plan
10. Live Regulatory Intelligence
11. Regulatory References
```

---

## Auto-Fail Triggers (RED)
- FCA not notified of a material breach where notification was required
- Outstanding remediation for a breach > 30 days old
- No breach register maintained
- Repeat breach of same type within 12 months with no root cause resolution

---

## Regulatory Notes
- SUP 15.3.8R: Notification must be made as soon as practicable — FCA expects same day or next business day for material breaches
- FCA enforcement actions for CASS breaches have resulted in fines up to £37m (see FCA enforcement register)
- FCA Handbook: https://www.handbook.fca.org.uk/handbook/SUP/15/
