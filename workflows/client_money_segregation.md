# Workflow: Client Money Segregation Audit (CASS 7)

## Objective
Conduct a detailed audit of the firm's client money segregation arrangements under FCA CASS 7, verifying that client money is properly identified, separated from firm money, held in appropriately designated accounts, and supported by the required documentation.

---

## Regulatory Basis
| Rule | Summary |
|---|---|
| CASS 7.13 | Client money segregation — general requirement |
| CASS 7.13.4R | Daily internal reconciliation |
| CASS 7.15 | External reconciliation requirement |
| CASS 7.16 | Calculation method (standard or alternative) |
| CASS 7.17 | Client money accounts — designation requirements |
| CASS 7.18 | Acknowledgement letters from approved banks |
| CASS 7.19 | Diversification of deposits |
| CASS 7A | Client money distribution and transfer on failure |

---

## Required Inputs
- [ ] Firm name and FCA FRN
- [ ] List of all client money bank accounts (institution, account number, balance)
- [ ] Are all accounts designated as "client" accounts? (yes/no)
- [ ] Acknowledgement letters in place for each account? (yes/no per account)
- [ ] Internal reconciliation frequency (daily/weekly/other)
- [ ] Last internal reconciliation date
- [ ] Last external reconciliation date
- [ ] Any reconciliation breaks identified? (yes/no, details)
- [ ] Calculation method (standard/alternative)
- [ ] FCA agreement for alternative method? (yes/no if applicable)
- [ ] Maximum % held at any single institution
- [ ] Are any accounts held with affiliated entities? (yes/no)
- [ ] Third party agent arrangements? (yes/no)

---

## Steps
### Step 1 — Collect client data → `.tmp/cms_audit_<client>_input.json`
### Step 2 — Run scan and generate report
```bash
python tools/generate_client_money_segregation.py --client "<client_name>"
```
### Step 3 — Review, annotate, finalise and deliver

---

## Report Structure
```
1. Firm Profile
2. Executive Summary
3. Account Inventory & Designation
4. Acknowledgement Letters
5. Reconciliation Compliance
6. Calculation Method
7. Diversification
8. Third-Party Arrangements
9. Findings Summary (RAG)
10. Remediation Action Plan
11. Live Regulatory Intelligence
12. Regulatory References
```

---

## Auto-Fail Triggers (RED)
- Any account not designated as a client money account
- Missing acknowledgement letter for any approved bank account
- Internal reconciliation not performed daily
- Reconciliation break identified and unresolved
- Alternative calculation method used without FCA agreement

---

## Regulatory Notes
- CASS 7.17.2R: Client money accounts must be titled to indicate they hold client money
- CASS 7.18.3R: Acknowledgement letters must be obtained before depositing client money
- FCA Handbook: https://www.handbook.fca.org.uk/handbook/CASS/7/
