---
name: gen-report
description: >
  Generate a test report for any of the 13 CASS Intelligence report types
  using sample data directly from the CLI, without needing the web portal.
  Usage: /gen-report <report_type> [firm_name]
  Example: /gen-report cass_health_check "Barclays Bank plc"
  Example: /gen-report grc_report "Meridian Capital Partners"
disable-model-invocation: false
---

## What this skill does

Generates a CASS Intelligence Report using sample/test data for the specified
report type. Useful for:
- Testing new report generators after changes
- Demonstrating reports to clients
- Verifying RAG scoring logic works end-to-end

## Steps

1. **Identify the report type** from the user's input. Valid types:
   - `cass_health_check`, `cass_resolution_pack`, `client_money_segregation`
   - `cass_breach_log`, `cass_oversight`, `threat_intelligence`
   - `cyber_threat_assessment`, `fca_incident_response`, `due_diligence`
   - `country_risk`, `executive_protection`, `physical_security_audit`
   - `grc_report`

2. **Find the REPORT_CONFIG entry** in `api/gateway.py` to get the prefix and script name.

3. **Create a sample input JSON** in `.tmp/<prefix>_<safe_name>_input.json`
   Use realistic UK financial services data. Include all fields the generator
   expects. For boolean fields: mix of true/false to produce GREEN/AMBER/RED findings.
   For CASS reports: use realistic dates, percentages, and thresholds.

4. **Run the generator script**:
   ```bash
   python tools/<script_name> --client <safe_name> --no-scan
   ```

5. **Report the output**:
   - Show the output file path
   - List any warnings or errors from the script
   - Confirm the RAG distribution (how many GREEN/AMBER/RED findings)
   - Note if the report needs review

## Sample data template for cass_health_check

```json
{
  "firm_name": "Test Capital Management Ltd",
  "frn": "987654",
  "cass_category": "Medium",
  "assessment_period": "Q3 2026",
  "last_cm_reconciliation_date": "2026-10-13",
  "last_custody_reconciliation_date": "2026-10-13",
  "client_money_calculation_method": "Standard",
  "alternative_method_fca_agreed": false,
  "max_single_institution_percentage": 18,
  "custody_assets_segregated": true,
  "acknowledgement_letters_in_place": true,
  "coof_individual_named": true,
  "coof_last_review_date": "2026-09-01",
  "cass_breaches_last_12_months": false,
  "has_retail_clients": true,
  "retail_interest_paid": true,
  "custodian_selection_grounds_recorded": true,
  "is_payment_or_emoney_firm": false,
  "cass_breach_details": ""
}
```

## Notes
- Always pass `--no-scan` to skip the Perplexity scan during test generation
- Output files appear in `.tmp/` directory
- The portal's download endpoint will serve them at `/api/download/<filename>`
