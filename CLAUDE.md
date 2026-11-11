# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Project: CASS Intelligence Reports

This project produces regulatory intelligence and security reports for banking and financial services clients, aligned with **FCA guidelines**, **CASS (Client Assets Sourcebook)** rules, and related UK financial regulations.

---

# Agent Instructions

You're working inside the **WAT framework** (Workflows, Agents, Tools). This architecture separates concerns so that probabilistic AI handles reasoning while deterministic code handles execution.

## The WAT Architecture

**Layer 1: Workflows (The Instructions)**
- Markdown SOPs stored in `workflows/`
- Each workflow defines the objective, required inputs, which tools to use, expected outputs, and how to handle edge cases
- Workflows are named by report type (e.g., `workflows/cass_health_check.md`, `workflows/fca_incident_response.md`)

**Layer 2: Agents (The Decision-Maker)**
- This is your role: read the relevant workflow, run tools in sequence, handle failures, ask clarifying questions when needed
- If you need to pull FCA handbook data or regulatory updates, don't attempt it directly — read the relevant workflow, determine the required inputs, then execute the appropriate tool in `tools/`

**Layer 3: Tools (The Execution)**
- Python scripts in `tools/` that do the actual work: FCA data fetching, report generation, document formatting, email delivery
- Credentials and API keys are stored in `.env`

---

## Report Types Supported

| Report | Workflow File | Description |
|---|---|---|
| CASS Health Check | `workflows/cass_health_check.md` | Reconciliation gaps, CASS 6 & 7 compliance |
| CASS Resolution Pack Readiness | `workflows/cass_resolution_pack.md` | CASS 10 — client asset return readiness |
| Client Money Segregation Audit | `workflows/client_money_segregation.md` | CASS 7 client money rules compliance |
| CASS Breach Log & Remediation | `workflows/cass_breach_log.md` | Documented breaches + corrective actions |
| CASS Oversight Report | `workflows/cass_oversight.md` | CASS Operational Oversight Function (COOF) |
| Threat Intelligence (Banking) | `workflows/threat_intelligence_banking.md` | Sector threats: fraud, insider risk, sanctions |
| Cyber Threat Assessment | `workflows/cyber_threat_assessment.md` | FCA CBEST, PS21/3, operational resilience |
| FCA Incident Response | `workflows/fca_incident_response.md` | FCA 72hr breach notification, CASS breach procedures |
| Due Diligence | `workflows/due_diligence.md` | FCA Fit & Proper, third-party/supplier CASS 6 & 7 |
| Country Risk | `workflows/country_risk.md` | Cross-border client asset risk, sanctions screening |
| Executive Protection (SM&CR) | `workflows/executive_protection.md` | Senior Manager & Certification Regime risk briefings |
| Physical Security Audit | `workflows/physical_security_audit.md` | Branch/office/data centre — FCA operational resilience |

---

## Running Tools

```bash
# Run a tool directly
python tools/<script_name>.py

# Install dependencies
pip install -r requirements.txt

# Load environment variables automatically via python-dotenv
# Just ensure .env is present — tools call load_dotenv() themselves
```

---

## How to Operate

**1. Look for existing tools first**
Before building anything new, check `tools/`. Only create new scripts when nothing exists for that task.

**2. Always reference the FCA Handbook**
- FCA Handbook base: https://www.handbook.fca.org.uk
- CASS Sourcebook: https://www.handbook.fca.org.uk/handbook/CASS/
- When citing rules, always include the CASS chapter and section (e.g., CASS 7.13.4R)

**3. Learn and adapt when things fail**
- Read the full error message and trace
- Fix the script and retest
- If the script uses paid API calls or credits, check with the user before re-running
- Document what you learned in the workflow

**4. Keep workflows current**
Update workflows when you find better methods or discover regulatory changes. Don't create or overwrite workflows without asking unless explicitly told to — these are durable instructions that need to be preserved and refined.

---

## The Self-Improvement Loop

1. Identify what broke or what regulation changed
2. Fix the tool or update the rule reference
3. Verify the fix works
4. Update the workflow with the new approach

---

## File Structure

```
.tmp/           # Temporary files (draft reports, intermediate data). Regenerated as needed.
tools/          # Python scripts for deterministic execution
workflows/      # Markdown SOPs defining report generation procedures
.env            # API keys and environment variables
requirements.txt
```

**Deliverables** are finalized reports delivered to clients (PDF, Word, Google Docs, email). Everything in `.tmp/` is disposable.

---

## Regulatory Reference

| Rule | Source | Summary |
|---|---|---|
| CASS 6 | FCA Handbook | Custody rules — safeguarding client assets |
| CASS 7 | FCA Handbook | Client money rules — segregation requirements |
| CASS 7A | FCA Handbook | Client money distribution and transfer |
| CASS 10 | FCA Handbook | CASS resolution pack |
| SM&CR | FCA/PRA | Senior Manager & Certification Regime |
| PS21/3 | FCA Policy Statement | Operational resilience requirements |
| CBEST | Bank of England | Cyber resilience testing framework |
| OFSI | HM Treasury | UK financial sanctions implementation |
