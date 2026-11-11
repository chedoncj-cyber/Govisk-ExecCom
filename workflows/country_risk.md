# Workflow: Country Risk Report

## Objective
Assess the regulatory, political, sanctions, and financial crime risk of operating in or through a specific country or jurisdiction. Used by banking clients for cross-border client asset decisions, sanctions screening, and correspondent banking risk management.

---

## Regulatory / Framework Basis
| Framework | Summary |
|---|---|
| OFSI (HM Treasury) | UK financial sanctions — designated persons and countries |
| OFAC (US Treasury) | US financial sanctions — OFAC SDN list |
| FATF | Financial Action Task Force — grey list / black list countries |
| FCA FCG 2 | FCA financial crime guide — jurisdiction risk |
| Basel AML Index | Country-level AML/CFT risk scores |
| Transparency International | Corruption Perceptions Index (CPI) |
| UK MLTF Regulations 2017 | Enhanced due diligence for high-risk third countries |

---

## Required Inputs
- [ ] Country / jurisdiction being assessed
- [ ] Purpose (client assets held / correspondent banking / staff travel / supplier)
- [ ] Firm's current exposure to this country (yes/no, nature of exposure)
- [ ] Known sanctions programmes applicable
- [ ] FATF status of the country
- [ ] Any prior regulatory concerns raised by FCA about this jurisdiction

---

## Steps
### Step 1 — Collect country and context data → `.tmp/country_risk_<client>_input.json`
### Step 2 — Run Perplexity scan for live sanctions and risk updates
```bash
python tools/generate_country_risk.py --client "<client_name>"
```
### Step 3 — Analyst review and cross-reference with OFSI/FATF lists
### Step 4 — Finalise and deliver

---

## Report Structure
```
1. Subject Profile (country + purpose)
2. Executive Summary
3. Sanctions Assessment (OFSI / OFAC / UN)
4. FATF Status & AML Risk
5. Political & Stability Risk
6. FCA Jurisdiction Risk
7. Recommended Controls
8. Risk Rating (RAG)
9. Live Regulatory Intelligence
10. References & Sources
```

---

## Risk Levels
| Rating | Meaning |
|---|---|
| RED — HIGH RISK | Active sanctions / FATF black list / extreme instability |
| AMBER — ELEVATED RISK | FATF grey list / elevated corruption / partial sanctions |
| GREEN — STANDARD RISK | No sanctions / FATF compliant / stable jurisdiction |

---

## Notes
- Always verify OFSI list directly: https://www.gov.uk/government/organisations/office-of-financial-sanctions-implementation
- FATF lists updated regularly: https://www.fatf-gafi.org/en/topics/high-risk-and-other-monitored-jurisdictions.html
- Basel AML Index: https://index.baselgovernance.org
