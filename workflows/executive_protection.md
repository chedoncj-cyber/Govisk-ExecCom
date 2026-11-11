# Workflow: Executive Protection Report (SM&CR)

## Objective
Assess personal security risks to senior managers and FCA-accountable individuals under SM&CR, and produce a protective intelligence brief covering threat exposure, travel risk, digital footprint, and recommended protective measures.

---

## Regulatory / Framework Basis
| Framework | Summary |
|---|---|
| SM&CR | FCA Senior Manager & Certification Regime — individual accountability |
| FCA SYSC | Systems and controls — personal data and security of key individuals |
| NPSA | National Protective Security Authority guidance (UK) |
| CPNI | Centre for the Protection of National Infrastructure |

---

## Required Inputs
- [ ] Subject name and role (Senior Manager / Certified Person / NEX)
- [ ] FCA SMF function(s) held
- [ ] Public profile level (high / medium / low — media exposure, LinkedIn, etc.)
- [ ] Known threats or security incidents against this individual
- [ ] International travel frequency and destinations
- [ ] Home working arrangements (yes/no)
- [ ] Known digital footprint concerns (yes/no)
- [ ] Protective measures currently in place (security driver, alarm system, etc.)
- [ ] Any harassment, stalking, or protest targeting?

---

## Steps
### Step 1 — Collect subject data (SENSITIVE — handle securely) → `.tmp/exec_prot_<client>_input.json`
### Step 2 — Run Perplexity scan for public threat intelligence relevant to role/sector
```bash
python tools/generate_executive_protection.py --client "<client_name>"
```
### Step 3 — Security analyst review — add physical and OSINT findings
### Step 4 — Deliver securely — do not email unencrypted

---

## Report Structure
```
1. Subject Profile (RESTRICTED)
2. Executive Summary
3. Threat Exposure Assessment
4. Digital Footprint & OSINT Risk
5. Travel Security Assessment
6. Home & Office Security
7. SM&CR Accountability Risk (if targeted)
8. Recommended Protective Measures
9. Live Threat Intelligence
10. References
```

---

## Threat Categories
| Category | Example |
|---|---|
| Targeted harassment | Activist campaigns, social media attacks |
| Physical threat | Stalking, targeted violence |
| Digital threat | Spear phishing, SIM swapping, doxxing |
| Travel risk | Kidnap for ransom, surveillance |
| SM&CR-specific | Regulatory targeting, whistleblower threats |

---

## Handling Instructions
- This report contains personal data — handle under UK GDPR
- Restrict distribution to named recipients only
- Store encrypted — do not leave in .tmp/ after delivery
- FCA SM&CR guidance: https://www.fca.org.uk/firms/senior-managers-certification-regime
