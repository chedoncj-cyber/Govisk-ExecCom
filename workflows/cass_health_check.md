# Workflow: CASS Health Check Report

## Objective
Produce a structured CASS Health Check report for a banking or investment firm client, assessing their compliance with FCA CASS 6 (custody assets) and CASS 7 (client money) rules. The report identifies gaps, breach risks, and remediation actions.

---

## Regulatory Basis

| Rule | Chapter | Summary |
|---|---|---|
| CASS 6.6 | Custody | Safe custody asset reconciliation — frequency and method |
| CASS 7.13 | Client Money | Internal client money reconciliation |
| CASS 7.15 | Client Money | External client money reconciliation |
| CASS 7.16 | Client Money | Client money calculation method |
| CASS 7.18 | Client Money | Acknowledgement letters from approved banks |
| CASS 7.19 | Client Money | Diversification of client money deposits |
| CASS 6.2 | Custody | Segregation of client assets from firm assets |
| CASS 7.13.4R | Client Money | Reconciliation must be performed daily |

---

## Required Inputs (Collect from Client)

Before running the tool, gather the following from the client:

- [ ] **Firm name** and FCA FRN (Firm Reference Number)
- [ ] **CASS categorisation** — Large, Medium, or Small CASS firm
- [ ] **Client money balances** — total held per bank, per account type
- [ ] **Custody assets held** — total per custodian/depository
- [ ] **Last reconciliation date** — for both client money and custody assets
- [ ] **Reconciliation method used** — standard or alternative method (CASS 7.16)
- [ ] **Acknowledgement letters** — list of approved banks and whether letters are in place
- [ ] **Diversification status** — % of client money held per single institution
- [ ] **CASS breaches in last 12 months** — yes/no, and details if yes
- [ ] **CASS Operational Oversight Function (COOF)** — named individual and last review date
- [ ] **Third-party custodians** — list of approved custodians used under CASS 6

---

## Steps

### Step 1 — Ingest Client Data
- Collect the above inputs from the client (via form, spreadsheet, or interview)
- Store raw input in `.tmp/cass_hc_<client_name>_input.json`

### Step 2 — Run the Health Check Tool
```bash
python tools/generate_cass_health_check.py --client "<client_name>"
```
- The tool reads `.tmp/cass_hc_<client_name>_input.json`
- Scores each CASS area: PASS / FAIL / REQUIRES ATTENTION
- Generates a draft report in `.tmp/cass_hc_<client_name>_draft.docx`

### Step 3 — Review Draft Report
- Open the draft and review findings
- Add qualitative commentary for any FAIL or REQUIRES ATTENTION items
- Confirm remediation recommendations are appropriate and proportionate

### Step 4 — Finalise and Deliver
- Export final report as PDF or Word
- Deliver to client via agreed channel (email, secure portal, Google Drive)
- Log delivery date in client record

---

## Expected Outputs

| Output | File | Description |
|---|---|---|
| Raw input | `.tmp/cass_hc_<client>_input.json` | Client data collected |
| Draft report | `.tmp/cass_hc_<client>_draft.docx` | Auto-generated Word document |
| Final report | Delivered externally | PDF or Word, client-branded |

---

## Report Structure

The generated report follows this structure:

```
1. Executive Summary
2. Firm Profile (name, FRN, CASS category)
3. CASS 7 — Client Money Assessment
   3.1 Segregation & Acknowledgement Letters
   3.2 Reconciliation Compliance (internal + external)
   3.3 Diversification
   3.4 Calculation Method
4. CASS 6 — Custody Asset Assessment
   4.1 Segregation from Firm Assets
   4.2 Reconciliation Compliance
   4.3 Third-Party Custodian Review
5. Breach History
6. COOF Review
7. Findings Summary (RAG status table)
8. Remediation Action Plan
9. Regulatory References
```

---

## Scoring Logic

Each check is scored using a RAG (Red / Amber / Green) system:

| Score | Meaning |
|---|---|
| GREEN — PASS | Fully compliant, no action required |
| AMBER — REQUIRES ATTENTION | Partial compliance, action recommended |
| RED — FAIL | Non-compliant, immediate remediation required |

**Auto-fail triggers (RED):**
- Reconciliation not performed within required frequency (CASS 7.13.4R — daily)
- No acknowledgement letters in place for approved banks (CASS 7.18)
- Client money not segregated from firm money
- Undisclosed CASS breaches in last 12 months

---

## Edge Cases

| Scenario | Action |
|---|---|
| Client is a Large CASS firm | Apply enhanced reconciliation and COOF reporting requirements |
| Client uses alternative calculation method | Validate it was agreed with FCA; flag if not documented |
| Client has active CASS breach | Escalate to FCA Incident Response workflow (`workflows/fca_incident_response.md`) |
| Missing acknowledgement letters | Flag as immediate RED — client must obtain within 20 business days |
| Reconciliation break > 1 day | Flag as RED — potential CASS 7.13.4R breach |

---

## Regulatory Notes

- CASS 7.13.4R requires client money reconciliation to be performed **at least daily**
- CASS 6.6.4R requires custody asset reconciliation **at least every 25 business days** for standard method
- Large CASS firms must have a **CASS Operational Oversight Function (COOF)** under CASS 1A.3
- Any identified breach must be reported to the FCA under **SUP 15.3** (material breach notification)
- FCA Handbook reference: https://www.handbook.fca.org.uk/handbook/CASS/
