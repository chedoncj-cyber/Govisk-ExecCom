# Workflow: Threat Intelligence Report — Banking Sector

## Objective
Produce a sector-specific threat intelligence report for a banking client, covering current fraud threats, insider risks, financial crime trends, sanctions evasion typologies, and relevant FCA enforcement activity. Powered by live Perplexity web intelligence.

---

## Regulatory / Framework Basis
| Framework | Relevance |
|---|---|
| FCA Financial Crime Guide (FCG) | Fraud and financial crime obligations for firms |
| JMLSG Guidance | Joint Money Laundering Steering Group — AML/CFT typologies |
| NCA Intelligence Bulletins | National Crime Agency threat assessments |
| OFSI / OFAC | Sanctions compliance obligations |
| FCA Supervisory Focus | Current FCA priorities and enforcement themes |

---

## Required Inputs
- [ ] Firm name and FCA FRN
- [ ] Business lines covered (retail banking, private banking, investment banking, etc.)
- [ ] Geographic footprint (UK only / international)
- [ ] Key counterparty sectors (e.g., real estate, crypto, commodities)
- [ ] Known threat concerns (optional — e.g., specific fraud type, jurisdiction)
- [ ] Assessment period

---

## Steps
### Step 1 — Collect client context → `.tmp/threat_intel_<client>_input.json`
### Step 2 — Run Perplexity scan + generate report
```bash
python tools/generate_threat_intelligence_banking.py --client "<client_name>"
```
### Step 3 — Analyst review — add sector-specific commentary
### Step 4 — Finalise and deliver

---

## Report Structure
```
1. Firm Profile
2. Executive Summary
3. Fraud & Financial Crime Threats
4. Insider Threat Landscape
5. Sanctions & Financial Crime Evasion
6. FCA Enforcement Activity & Supervisory Focus
7. Threat Assessment Summary (RAG by threat category)
8. Recommended Mitigations
9. Live Regulatory Intelligence
10. References & Sources
```

---

## Threat Categories Assessed
| Category | Indicators |
|---|---|
| Authorised Push Payment (APP) Fraud | PSR reimbursement rules, sector exposure |
| Trade Finance Fraud | Documentary fraud, letters of credit manipulation |
| Insider Threat | Privileged access misuse, data exfiltration |
| Sanctions Evasion | Complex structures, high-risk jurisdictions |
| Crypto-related Financial Crime | Conversion of illicit funds |
| Account Takeover | Credential theft, social engineering |
| FCA Supervisory Risk | Current FCA priority areas for banking sector |

---

## Notes
- This report is intelligence-led — Perplexity scan is essential for current threat landscape
- Analyst should verify and supplement with NCA/UKFIU bulletins where available
- FCA Financial Crime Guide: https://www.handbook.fca.org.uk/handbook/FCG/
