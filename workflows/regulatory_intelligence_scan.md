# Workflow: Regulatory Intelligence Scan (Perplexity)

## Objective
Before generating any client report, query Perplexity AI's live web search to retrieve the latest FCA announcements, CASS rule changes, enforcement actions, and sector threats. Embed this intelligence into the report so clients always receive current, not static, information.

---

## When to Run This Workflow

Run this workflow **before** generating any of the following reports:
- CASS Health Check
- CASS Resolution Pack Readiness
- Client Money Segregation Audit
- CASS Breach Log & Remediation
- CASS Oversight Report
- Threat Intelligence (Banking)
- Cyber Threat Assessment
- FCA Incident Response
- Due Diligence
- Country Risk
- Executive Protection
- Physical Security Audit

---

## Required Inputs

- [ ] `PERPLEXITY_API_KEY` set in `.env`
- [ ] Report type identifier (e.g., `cass_health_check`, `threat_intelligence_banking`)
- [ ] Optional: additional custom topics specific to the client

---

## Steps

### Step 1 — Run the Scan
```bash
# Scan all pre-built topics for a report type
python tools/perplexity_scan.py --report cass_health_check

# Or scan a single custom topic
python tools/perplexity_scan.py --topic "FCA CASS 7 client money updates 2026"
```

### Step 2 — Review Output
- Output is saved to `.tmp/<report_type>_intel.json`
- Review summaries for relevance and accuracy before embedding in report
- Remove any results that are off-topic or low quality

### Step 3 — Embed in Report
- The report generation tool reads the intel JSON automatically if present
- Intel appears as a **Regulatory Intelligence** section in the final report
- Citations (source URLs) are listed so the client can verify

---

## Pre-Built Scan Topics by Report Type

| Report Type | Topics Scanned |
|---|---|
| `cass_health_check` | CASS 6 & 7 rule updates, FCA enforcement, handbook amendments |
| `cass_resolution_pack` | CASS 10 resolution planning requirements |
| `client_money_segregation` | CASS 7 segregation enforcement, rule changes |
| `cass_breach_log` | SUP 15.3 breach notification, FCA fines & penalties |
| `cass_oversight` | COOF requirements, CASS 1A updates |
| `threat_intelligence_banking` | Fraud, insider threats, financial crime, sanctions evasion |
| `cyber_threat_assessment` | FCA CBEST, PS21/3 operational resilience, cyber incidents |
| `fca_incident_response` | FCA 72hr notification, SUP 15 updates |
| `due_diligence` | FCA Fit & Proper, SM&CR, third-party CASS supplier rules |
| `country_risk` | OFSI/OFAC sanctions, cross-border client asset risk |
| `executive_protection` | SM&CR enforcement, executive security threats |
| `physical_security_audit` | FCA operational resilience (PS6/21), physical security |

---

## Model Used

- **Model:** `sonar` (Perplexity's live web search model)
- **Base URL:** `https://api.perplexity.ai`
- Results include citations — always include these in the delivered report

---

## Edge Cases

| Scenario | Action |
|---|---|
| API key missing | Set `PERPLEXITY_API_KEY` in `.env` — get key at perplexity.ai/settings/api |
| Scan returns no results | Re-run with a more specific topic; check internet connectivity |
| Results seem outdated | Try appending the current year to the topic string |
| Client requests custom scan | Use `--topic` flag with a specific query |
| Rate limit hit | Wait 60 seconds and retry; Perplexity free tier has limits |

---

## Notes

- Perplexity `sonar` searches the live web — results change daily
- Always review before delivery; AI-generated summaries may contain errors
- For sensitive enforcement actions, verify directly at fca.org.uk before citing
- FCA enforcement register: https://www.fca.org.uk/firms/financial-services-register
- FCA handbook: https://www.handbook.fca.org.uk
