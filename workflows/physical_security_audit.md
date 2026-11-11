# Workflow: Physical Security Audit

## Objective
Assess the physical security of a banking firm's premises (branch, office, data centre, vault) against FCA operational resilience requirements and NPSA/CPNI standards. Identify vulnerabilities and produce a remediation plan.

---

## Regulatory / Framework Basis
| Framework | Summary |
|---|---|
| FCA PS21/3 | Operational resilience — premises must support IBS continuity |
| FCA PS6/21 | Operational resilience for banks and insurers |
| FCA SYSC 8 | Outsourcing and premises controls |
| NPSA | National Protective Security Authority — physical security standards |
| CPNI | Centre for Protection of National Infrastructure |
| PD 6662 | UK standard for intruder alarm systems |
| BS EN 1047 | Security containers and strongrooms |

---

## Required Inputs
- [ ] Firm name and FCA FRN
- [ ] Premises type(s) being assessed (branch / head office / data centre / vault)
- [ ] Address(es)
- [ ] Access control system in place? (yes/no, type)
- [ ] CCTV coverage? (yes/no, areas covered)
- [ ] Intruder alarm system? (yes/no, standard)
- [ ] Security personnel on site? (yes/no, hours)
- [ ] Physical perimeter security? (fencing, barriers, lighting)
- [ ] Visitor management process in place? (yes/no)
- [ ] Secure document / media disposal? (yes/no)
- [ ] Business continuity plan for premises failure? (yes/no)
- [ ] Last physical security review date
- [ ] Any prior incidents? (break-ins, theft, tailgating, etc.)

---

## Steps
### Step 1 — Collect premises data → `.tmp/phys_audit_<client>_input.json`
### Step 2 — Run scan and generate report
```bash
python tools/generate_physical_security_audit.py --client "<client_name>"
```
### Step 3 — On-site walkthrough recommended to supplement findings
### Step 4 — Finalise and deliver

---

## Report Structure
```
1. Premises Profile
2. Executive Summary
3. Perimeter & Access Control
4. CCTV & Alarm Systems
5. Security Personnel
6. Visitor & Document Management
7. FCA Operational Resilience (PS21/3)
8. Findings Summary (RAG)
9. Remediation Action Plan
10. Live Regulatory Intelligence
11. Regulatory References
```

---

## Auto-Fail Triggers (RED)
- No access control on premises holding client assets or sensitive data
- No CCTV in cash handling or server areas
- No business continuity plan for premises failure
- Prior break-in with no remediation completed
- Data centre / vault without alarm system

---

## Notes
- Physical security is part of FCA operational resilience — gaps can result in FCA supervisory action
- NPSA guidance: https://www.npsa.gov.uk
- CPNI: https://www.cpni.gov.uk
