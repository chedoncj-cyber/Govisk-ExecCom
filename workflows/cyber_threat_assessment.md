# Workflow: Cyber Threat Assessment

## Objective
Assess the firm's cyber risk posture against FCA operational resilience requirements, the CBEST framework, and PS21/3. Identify gaps in cyber controls and provide a prioritised remediation plan.

---

## Regulatory Basis
| Framework | Summary |
|---|---|
| FCA PS21/3 | Operational resilience — impact tolerances, scenario testing |
| FCA PS6/21 | Operational resilience policy statement (banks) |
| CBEST | Bank of England / FCA intelligence-led cyber resilience testing |
| DORA (EU) | Digital Operational Resilience Act — relevant for firms with EU operations |
| NIS2 Directive | Network and Information Security — relevant for critical infrastructure |
| FCA SYSC 7 | Systems and controls — IT and cyber |

---

## Required Inputs
- [ ] Firm name and FCA FRN
- [ ] Has the firm conducted a CBEST assessment? (yes/no/in-progress)
- [ ] Date of last CBEST or equivalent penetration test
- [ ] Important Business Services (IBS) identified under PS21/3? (yes/no)
- [ ] Impact tolerances set for IBS? (yes/no)
- [ ] Scenario testing completed? (yes/no)
- [ ] Last cyber incident date and type (if any)
- [ ] Third-party/supplier cyber risk assessment conducted? (yes/no)
- [ ] Cyber incident response plan exists? (yes/no)
- [ ] Cyber response plan tested in last 12 months? (yes/no)
- [ ] Multi-factor authentication (MFA) deployed across critical systems? (yes/no)
- [ ] Privileged access management (PAM) solution in place? (yes/no)

---

## Steps
### Step 1 — Collect client data → `.tmp/cyber_ta_<client>_input.json`
### Step 2 — Run scan and generate report
```bash
python tools/generate_cyber_threat_assessment.py --client "<client_name>"
```
### Step 3 — Review, supplement with technical findings if available
### Step 4 — Finalise and deliver

---

## Report Structure
```
1. Firm Profile
2. Executive Summary
3. FCA Operational Resilience (PS21/3)
4. CBEST Cyber Testing
5. Cyber Controls Assessment
6. Third-Party & Supply Chain Risk
7. Incident Response Readiness
8. Threat Assessment Summary (RAG)
9. Remediation Action Plan
10. Live Regulatory Intelligence
11. Regulatory References
```

---

## Auto-Fail Triggers (RED)
- No CBEST or equivalent test in last 3 years (for in-scope firms)
- Important Business Services not identified under PS21/3
- No cyber incident response plan
- MFA not deployed on critical systems
- No third-party cyber risk assessment

---

## Notes
- CBEST applies to firms supervised by FCA/PRA — not all firms are in scope
- PS21/3 operational resilience deadline was 31 March 2022 — firms should already be compliant
- FCA CBEST: https://www.bankofengland.co.uk/financial-stability/financial-sector-continuity/cbest
