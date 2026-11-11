---
name: add-regulation
description: >
  Add a new FCA rule, enforcement case, or regulatory update to fca_reference.py
  and optionally wire it into the relevant report generator.
  Usage: /add-regulation <rule_ref> [report_type]
  Example: /add-regulation "CASS 7.11.33R" cass_health_check
---

## What this skill does

You are adding a new regulatory entry to the CASS Intelligence Reports platform.
This involves:

1. **Adding the rule to `tools/fca_reference.py`**
   - Add to `CASS_RULES` dict if it's a CASS rule
   - Add to `FCA_NEWS` if it's a recent development
   - Add to `ENFORCEMENT_CASES[report_type]` if it's an enforcement case
   - Add to `REGULATORY_UPDATES[report_type]` if it's a regulatory update
   - Update `get_new_rules()` effective_date if applicable

2. **Adding scoring logic to the relevant generator** (if `report_type` provided)
   - Add a new `score_check` dict to the appropriate scoring function
   - Follow the existing pattern: `{"rule": "...", "description": "...", "status": "GREEN/AMBER/RED", "commentary": "..."}`
   - For yes/no fields: GREEN if compliant, RED if not, AMBER if partially

3. **Adding a form field to `portal/assets/app.js`** (if user-facing input is needed)
   - Add the field to the correct report's `fields` array in REPORTS
   - Add a tooltip entry to `FIELD_TOOLTIPS`

4. **Verifying syntax**
   - Run `python -m py_compile tools/fca_reference.py` after editing
   - Run `node --check portal/assets/app.js` after editing

## Rule format in CASS_RULES

```python
"CASS X.Y.Z R": {
    "title": "Short title of the rule",
    "description": "Full description of what the rule requires",
    "effective_date": "YYYY-MM-DD",
    "source": "FCA Handbook",
    "category": "client_money | custody | oversight | resolution | payment",
    "applies_to": ["investment_firm", "payment_institution", ...],
}
```

## Enforcement case format

```python
{
    "firm": "Firm Name",
    "fine": "£X,XXX,XXX",
    "year": YYYY,
    "rules": ["CASS X.Y", "SYSC Z"],
    "summary": "One sentence summary of the breach and penalty.",
}
```

## Regulatory update format (for REGULATORY_UPDATES)

```python
"key_slug": (
    "Full description of the regulatory change. Include: what changed, "
    "when it takes effect, what firms must do, and the FCA's stated objective."
)
```
