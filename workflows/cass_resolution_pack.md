# Workflow: CASS Resolution Pack Readiness Report (CASS 10)

## Objective
Assess whether the firm's CASS Resolution Pack (CRP) meets FCA CASS 10 requirements — ensuring client assets can be rapidly identified, segregated, and returned in the event of firm failure or insolvency.

---

## Regulatory Basis
| Rule | Summary |
|---|---|
| CASS 10.1 | Obligation to maintain a CASS resolution pack |
| CASS 10.2 | Contents of the resolution pack |
| CASS 10.2.2R | Documents required: client asset schedule, acknowledgement letters, reconciliation records |
| CASS 10.2.3R | Pack must be accessible to insolvency practitioner within 48 hours |
| CASS 10.3 | Annual review requirement |
| CASS 6 / CASS 7 | Underlying custody and client money rules the pack must reference |

---

## Required Inputs
- [ ] Firm name and FCA FRN
- [ ] Does a formal CRP document exist? (yes/no)
- [ ] Date of last CRP review
- [ ] Is the CRP accessible within 48 hours? (yes/no/unknown)
- [ ] Named responsible individual for the CRP
- [ ] Does the pack include: client asset schedule? acknowledgement letters? reconciliation records? system access credentials?
- [ ] Has the pack been tested (e.g. dry run)? (yes/no)
- [ ] Date of last test
- [ ] Is the pack stored securely and off-site/cloud-accessible?

---

## Steps
### Step 1 — Collect client data → `.tmp/cass_rp_<client>_input.json`
### Step 2 — Run scan and generate report
```bash
python tools/generate_cass_resolution_pack.py --client "<client_name>"
```
### Step 3 — Review, annotate, finalise and deliver

---

## Report Structure
```
1. Firm Profile
2. Executive Summary
3. CRP Document Existence & Accessibility
4. CRP Contents Assessment
5. Annual Review Compliance
6. Testing & Dry Run Assessment
7. Findings Summary (RAG)
8. Remediation Action Plan
9. Live Regulatory Intelligence
10. Regulatory References
```

---

## Auto-Fail Triggers (RED)
- No CRP document exists
- Pack not accessible within 48 hours
- No annual review in last 12 months
- Missing mandatory contents (client asset schedule or acknowledgement letters)

---

## Regulatory Notes
- CASS 10 applies to firms that hold client assets or client money under CASS 6 or CASS 7
- Insolvency practitioners rely on the CRP to return assets — gaps cause client harm
- FCA Handbook: https://www.handbook.fca.org.uk/handbook/CASS/10/
