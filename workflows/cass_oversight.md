# Workflow: CASS Oversight Report (COOF)

## Objective
Assess whether the firm's CASS Operational Oversight Function (COOF) is properly constituted, resourced, and operating effectively in line with FCA CASS 1A requirements. Produce an oversight report suitable for board-level review.

---

## Regulatory Basis
| Rule | Summary |
|---|---|
| CASS 1A.3 | Requirement for CASS Operational Oversight Function |
| CASS 1A.3.1R | Named individual responsible for COOF |
| CASS 1A.3.3R | COOF individual must have appropriate skills and expertise |
| CASS 1A.3.4R | COOF must report to governing body at least annually |
| CASS 1A.4 | COOF responsibilities — monitoring, escalation, reporting |
| SM&CR | Senior Manager accountability for COOF individual |

---

## Required Inputs
- [ ] Firm name and FCA FRN
- [ ] CASS category (Large/Medium/Small)
- [ ] Name and role of COOF individual
- [ ] COOF individual's qualifications / CASS experience
- [ ] Date of last COOF report to governing body
- [ ] Date of last COOF review of CASS arrangements
- [ ] Key findings from last COOF review
- [ ] Outstanding COOF recommendations
- [ ] Is COOF individual also the CASS compliance officer? (yes/no)
- [ ] Board/committee minutes confirming COOF report received? (yes/no)
- [ ] Any COOF-identified issues escalated to FCA? (yes/no)

---

## Steps
### Step 1 — Collect client data → `.tmp/coof_<client>_input.json`
### Step 2 — Run scan and generate report
```bash
python tools/generate_cass_oversight.py --client "<client_name>"
```
### Step 3 — Review, annotate, finalise and deliver

---

## Report Structure
```
1. Firm Profile
2. Executive Summary
3. COOF Constitution & Appointment
4. COOF Qualifications & Independence
5. COOF Activity & Reporting
6. Outstanding Recommendations
7. Findings Summary (RAG)
8. Remediation Action Plan
9. Live Regulatory Intelligence
10. Regulatory References
```

---

## Auto-Fail Triggers (RED)
- No named COOF individual (Large CASS firm only)
- No annual report to governing body in last 12 months
- COOF individual lacks CASS expertise
- Outstanding COOF recommendations with no action plan

---

## Regulatory Notes
- CASS 1A only applies to **Large CASS firms** — verify category before applying
- Medium and Small firms have lighter-touch oversight obligations
- FCA Handbook: https://www.handbook.fca.org.uk/handbook/CASS/1A/
