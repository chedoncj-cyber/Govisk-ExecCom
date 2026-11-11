# Workflow: Due Diligence Report

## Objective
Conduct FCA-aligned due diligence on an individual, entity, or third-party supplier. Covers FCA Fit & Proper assessments, SM&CR background checks, and CASS 6 & 7 third-party supplier vetting.

---

## Regulatory Basis
| Rule | Summary |
|---|---|
| FIT 1.3 | FCA Fit and Proper test — honesty, integrity, competence, financial soundness |
| SM&CR | Senior Manager & Certification Regime — individual accountability |
| CASS 6.3 | Third-party custodian due diligence |
| CASS 7.13 | Third-party agent due diligence for client money |
| SYSC 8 | Outsourcing — due diligence on service providers |
| FCA Register | Public FCA register for authorised firms and individuals |

---

## Required Inputs
- [ ] Subject name (individual or entity)
- [ ] Subject type (individual / firm / third-party supplier)
- [ ] FCA FRN or Individual Reference Number (IRN) if applicable
- [ ] Purpose of due diligence (new hire / SM&CR appointment / CASS supplier / outsourcing)
- [ ] Regulatory history (any known FCA actions, bans, or investigations)
- [ ] Directorship history
- [ ] Financial soundness indicators (CCJs, bankruptcy, insolvency)
- [ ] Professional qualifications and memberships
- [ ] Previous employer references
- [ ] For entities: ownership structure, beneficial owners, group structure

---

## Steps
### Step 1 — Collect subject data → `.tmp/dd_<client>_input.json`
### Step 2 — Run scan (Perplexity screens for regulatory actions, news, sanctions)
```bash
python tools/generate_due_diligence.py --client "<client_name>"
```
### Step 3 — Analyst review and FCA Register check
### Step 4 — Finalise and deliver

---

## Report Structure
```
1. Subject Profile
2. Executive Summary
3. FCA Fit & Proper Assessment
4. Regulatory History
5. Financial Soundness
6. Professional Qualifications & Competence
7. CASS Third-Party Assessment (if applicable)
8. Web Intelligence Findings (Perplexity)
9. Overall Assessment (PASS / CONDITIONAL / FAIL)
10. Regulatory References
```

---

## Auto-Fail Triggers (RED)
- Active FCA ban or prohibition order
- Undisclosed regulatory actions or criminal convictions
- Outstanding CCJs or insolvency proceedings
- Sanctions match (OFSI/OFAC)
- Third-party supplier not FCA authorised where required

---

## Notes
- Always verify directly on the FCA Register: https://register.fca.org.uk
- SM&CR Fit & Proper test must be documented and retained
- FCA Handbook FIT: https://www.handbook.fca.org.uk/handbook/FIT/
