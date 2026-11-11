"""
Regional equivalents of the 4 CASS-specific compliance reports.
Provides scoring functions and title maps for non-UK regions, mirroring the
UK CASS report suite structure (Health Check, Resolution Pack, Breach Log, Oversight).
"""

from datetime import datetime, date

# ── Report title maps ─────────────────────────────────────────────────────────

HEALTH_CHECK_TITLES = {
    "UK":            "CASS (Client Assets Sourcebook) Health Check Report",
    "N. America":    "SEC / CFTC / CIRO Client Assets Health Check Report",
    "Latin America": "CVM / CNBV / SFC Client Assets Health Check Report",
    "Asia Pacific":  "MAS / ASIC / SFC / FSA Client Assets Health Check Report",
    "Europe":        "MiFID II Client Assets Safeguarding Health Check Report",
    "Africa":        "FSCA / CBN / CMA Client Assets Health Check Report",
}

RESOLUTION_PACK_TITLES = {
    "UK":            "CASS (Client Assets Sourcebook) Resolution Pack Readiness Report",
    "N. America":    "SEC / CFTC / SIPC Customer Asset Return Readiness Report",
    "Latin America": "Client Asset Resolution Readiness Report",
    "Asia Pacific":  "MAS / ASIC / SFC Client Asset Return Readiness Report",
    "Europe":        "MiFID II Client Asset Return Readiness Report",
    "Africa":        "FSCA / CBN / CMA Client Asset Resolution Readiness Report",
}

BREACH_LOG_TITLES = {
    "UK":            "CASS (Client Assets Sourcebook) Breach Log & Remediation Report",
    "N. America":    "SEC / FINRA / CFTC Compliance Violation Log & Remediation Report",
    "Latin America": "Client Asset Breach Log & Remediation Report",
    "Asia Pacific":  "MAS / ASIC / SFC / FSA Breach Log & Remediation Report",
    "Europe":        "MiFID II Client Asset Breach Log & Remediation Report",
    "Africa":        "FSCA / CBN / CMA Breach Log & Remediation Report",
}

OVERSIGHT_TITLES = {
    "UK":            "CASS (Client Assets Sourcebook) Oversight Report (COOF)",
    "N. America":    "SEC / FINRA Chief Compliance Officer Oversight Report",
    "Latin America": "Client Asset Compliance Officer Oversight Report",
    "Asia Pacific":  "MAS / ASIC / SFC / FSA Compliance Oversight Report",
    "Europe":        "MiFID II Compliance Function Oversight Report",
    "Africa":        "FSCA / CBN / CMA Compliance Oversight Report",
}


# ══════════════════════════════════════════════════════════════════════════════
# HEALTH CHECK — mirrors CASS 6/7 checks, section structure identical to UK
# ══════════════════════════════════════════════════════════════════════════════

def score_us_health_check(data: dict) -> list:
    findings = []

    reserve = data.get("reserve_formula_computed")
    findings.append({
        "area": "Customer Reserve", "rule": "SEC Rule 15c3-3(e)",
        "description": "Customer reserve formula computed weekly",
        "status": "GREEN" if reserve else "RED",
        "commentary": "Customer reserve formula computed and funded weekly per SEC Rule 15c3-3(e)." if reserve
            else "Customer reserve formula not computed. SEC Rule 15c3-3(e) requires weekly reserve computation and funding.",
    })

    reserve_acct = data.get("special_reserve_account_designated")
    findings.append({
        "area": "Customer Reserve", "rule": "SEC Rule 15c3-3(e)(3)",
        "description": "Special Reserve Bank Account designated and acknowledged",
        "status": "GREEN" if reserve_acct else "RED",
        "commentary": "Special Reserve Bank Account designated with qualified bank acknowledgement on file." if reserve_acct
            else "Special Reserve Bank Account not confirmed. SEC 15c3-3(e)(3) requires a dedicated account held at a qualified bank.",
    })

    pos_ctrl = data.get("possession_control_compliant")
    findings.append({
        "area": "Possession & Control", "rule": "SEC Rule 15c3-3(b)",
        "description": "Fully paid and excess margin securities in possession or control",
        "status": "GREEN" if pos_ctrl else "RED",
        "commentary": "Possession/control requirements met — fully paid and excess margin securities confirmed segregated." if pos_ctrl
            else "Possession/control deficiency. SEC 15c3-3(b) requires all fully paid and excess margin customer securities to be in possession or control.",
    })

    cftc = data.get("cftc_segregation_compliant")
    findings.append({
        "area": "CFTC Segregation", "rule": "CFTC Rule 1.20",
        "description": "Customer funds maintained in CFTC-segregated accounts",
        "status": "GREEN" if cftc else ("AMBER" if cftc is None else "RED"),
        "commentary": "CFTC Rule 1.20 segregated accounts maintained — customer funds separate from firm funds." if cftc
            else ("CFTC segregation status not confirmed. Verify if CFTC-registered." if cftc is None
                  else "CFTC segregation deficiency. Rule 1.20 requires customer funds segregated at all times."),
    })

    daily_calc = data.get("daily_segregation_calculation")
    findings.append({
        "area": "CFTC Segregation", "rule": "CFTC Rule 1.32",
        "description": "Daily segregation calculation performed",
        "status": "GREEN" if daily_calc else ("AMBER" if daily_calc is None else "RED"),
        "commentary": "Daily segregation calculation performed and on file." if daily_calc
            else ("Daily seg calculation status not confirmed." if daily_calc is None
                  else "Daily seg calculation not performed. CFTC Rule 1.32 requires daily computation."),
    })

    sipc = data.get("sipc_member")
    findings.append({
        "area": "SIPC / Investor Protection", "rule": "SIPA 15 U.S.C. §78aaa",
        "description": "SIPC membership current",
        "status": "GREEN" if sipc else ("AMBER" if sipc is None else "RED"),
        "commentary": "SIPC membership current — investor protection up to $500,000 per customer confirmed." if sipc
            else ("SIPC membership not confirmed. All broker-dealers must maintain SIPC membership under SIPA." if sipc is None
                  else "SIPC membership lapsed. Broker-dealers must be SIPC members — reinstate immediately."),
    })

    net_cap = data.get("net_capital_compliant")
    findings.append({
        "area": "Net Capital", "rule": "SEC Rule 15c3-1",
        "description": "Net capital requirements met",
        "status": "GREEN" if net_cap else ("AMBER" if net_cap is None else "RED"),
        "commentary": "Net capital in compliance with SEC Rule 15c3-1." if net_cap
            else ("Net capital status not confirmed. Verify compliance with SEC Rule 15c3-1." if net_cap is None
                  else "Net capital deficiency. Immediate remediation required — broker-dealer operations may be at risk."),
    })

    freq = data.get("internal_reconciliation_frequency", "").lower()
    findings.append({
        "area": "Reconciliation", "rule": "SEC Rule 15c3-3 / FINRA",
        "description": "Daily internal customer account reconciliation",
        "status": "GREEN" if freq == "daily" else "RED",
        "commentary": "Daily customer account reconciliation confirmed." if freq == "daily"
            else f"Reconciliation frequency: '{freq}'. Daily reconciliation required for customer accounts.",
    })

    ack = data.get("acknowledgement_letters_all_accounts")
    findings.append({
        "area": "Account Documentation", "rule": "SEC Rule 15c3-3 / CFTC Rule 1.20",
        "description": "Bank / custodian acknowledgement letters in place",
        "status": "GREEN" if ack else "AMBER",
        "commentary": "Acknowledgement letters obtained from all custodian banks and depositories." if ack
            else "Acknowledgement letters not confirmed for all accounts. Required from all custodian banks and depositories.",
    })

    ciro = data.get("ciro_form1_compliant")
    if ciro is not None:
        findings.append({
            "area": "Canada — CIRO", "rule": "CIRO Rule 100 / Form 1",
            "description": "CIRO Form 1 and client asset segregation (Canada)",
            "status": "GREEN" if ciro else "RED",
            "commentary": "CIRO Form 1 filed and client asset segregation confirmed." if ciro
                else "CIRO Form 1 compliance not confirmed. Canadian-registered dealers must segregate client assets under CIRO Rule 100.",
        })

    return findings


def score_latam_health_check(data: dict) -> list:
    findings = []

    br = data.get("brazil_cvm_compliant")
    findings.append({
        "area": "Brazil — CVM / BCB", "rule": "CVM Instruction 555 / BCB Res. 4,966",
        "description": "Client assets segregated per CVM / BCB rules",
        "status": "GREEN" if br else ("AMBER" if br is None else "RED"),
        "commentary": "CVM / BCB client asset segregation confirmed." if br
            else ("CVM / BCB compliance not confirmed. Brazilian firms must segregate client assets under CVM Instruction 555." if br is None
                  else "CVM / BCB segregation deficiency — immediate remediation required."),
    })

    mx = data.get("mexico_cnbv_compliant")
    findings.append({
        "area": "Mexico — CNBV", "rule": "Ley del Mercado de Valores",
        "description": "Client assets segregated per CNBV rules",
        "status": "GREEN" if mx else ("AMBER" if mx is None else "RED"),
        "commentary": "CNBV client money segregation confirmed." if mx
            else ("CNBV compliance not confirmed. Mexican firms must segregate client assets per LMV." if mx is None
                  else "CNBV segregation deficiency detected."),
    })

    co = data.get("colombia_sfc_compliant")
    findings.append({
        "area": "Colombia — SFC", "rule": "SFC Circular Básica Jurídica",
        "description": "Client assets held per SFC rules",
        "status": "GREEN" if co else ("AMBER" if co is None else "RED"),
        "commentary": "SFC client asset protection rules confirmed." if co
            else ("SFC compliance not confirmed. Colombian firms must segregate client assets per SFC rules." if co is None
                  else "SFC deficiency detected."),
    })

    cl = data.get("chile_cmf_compliant")
    findings.append({
        "area": "Chile — CMF", "rule": "Law 21,521 (Fintech Law)",
        "description": "Client money requirements under Chilean Fintech Law",
        "status": "GREEN" if cl else ("AMBER" if cl is None else "RED"),
        "commentary": "CMF client money requirements met under Law 21,521." if cl
            else ("CMF compliance not confirmed. Law 21,521 requires client money segregation." if cl is None
                  else "CMF deficiency detected."),
    })

    ar = data.get("argentina_bcra_compliant")
    findings.append({
        "area": "Argentina — BCRA", "rule": "BCRA Communication A 6859",
        "description": "Client assets per BCRA A 6859",
        "status": "GREEN" if ar else ("AMBER" if ar is None else "RED"),
        "commentary": "BCRA A 6859 client asset compliance confirmed." if ar
            else ("BCRA compliance not confirmed." if ar is None else "BCRA A 6859 deficiency detected."),
    })

    freq = data.get("internal_reconciliation_frequency", "").lower()
    findings.append({
        "area": "Reconciliation", "rule": "Local Regulator",
        "description": "Internal client asset reconciliation",
        "status": "GREEN" if freq in ("daily", "weekly") else "AMBER",
        "commentary": f"Reconciliation frequency: {freq}. Verify this meets the applicable local regulatory minimum." if freq
            else "Reconciliation frequency not stated. Confirm compliance with local reconciliation requirements.",
    })

    cb = data.get("cross_border_protections_documented")
    findings.append({
        "area": "Cross-Border", "rule": "Local Reg.",
        "description": "Cross-border client asset protections documented",
        "status": "GREEN" if cb else "AMBER",
        "commentary": "Cross-border client asset protections documented and reviewed." if cb
            else "Cross-border protections not documented. Review custody arrangements where assets are held outside the home jurisdiction.",
    })

    return findings


def score_apac_health_check(data: dict) -> list:
    findings = []

    sg = data.get("singapore_mas_compliant")
    findings.append({
        "area": "Singapore — MAS", "rule": "SFA s.104 / MAS SFLCBR",
        "description": "Client money held in trust; trust account acknowledged",
        "status": "GREEN" if sg else ("AMBER" if sg is None else "RED"),
        "commentary": "SFA s.104 trust account maintained with MAS SFLCBR acknowledgement letter on file." if sg
            else ("MAS SFA s.104 compliance not confirmed. Singapore-licensed firms must hold client money in trust." if sg is None
                  else "SFA s.104 deficiency — immediate remediation required."),
    })

    hk = data.get("hk_sfc_compliant")
    findings.append({
        "area": "Hong Kong — SFC", "rule": "SFO Cap.571I / Cap.571H",
        "description": "Client money (Cap.571I) and securities (Cap.571H) rules compliant",
        "status": "GREEN" if hk else ("AMBER" if hk is None else "RED"),
        "commentary": "HK SFC client money (Cap.571I) and client securities (Cap.571H) requirements met." if hk
            else ("SFC compliance not confirmed. HK-licensed firms must comply with SFO Cap.571I and Cap.571H." if hk is None
                  else "SFC Cap.571I / Cap.571H deficiency detected."),
    })

    au = data.get("australia_asic_compliant")
    findings.append({
        "area": "Australia — ASIC", "rule": "Corporations Act Div.2 Pt.7.8 / RG 166",
        "description": "Client money reconciliation and trust account requirements",
        "status": "GREEN" if au else ("AMBER" if au is None else "RED"),
        "commentary": "ASIC client money trust account and daily reconciliation requirements met under Corporations Act Div.2 Pt.7.8." if au
            else ("ASIC compliance not confirmed. Australian AFS licensees must maintain client money per Corporations Act." if au is None
                  else "ASIC Corporations Act Div.2 Pt.7.8 deficiency detected."),
    })

    jp = data.get("japan_fsa_compliant")
    findings.append({
        "area": "Japan — FSA", "rule": "FIEA Art.43-2",
        "description": "Customer asset segregation under FIEA",
        "status": "GREEN" if jp else ("AMBER" if jp is None else "RED"),
        "commentary": "FIEA Art.43-2 customer asset segregation confirmed." if jp
            else ("FSA / FIEA compliance not confirmed. Japanese financial instruments business operators must segregate under FIEA Art.43-2." if jp is None
                  else "FIEA Art.43-2 deficiency detected."),
    })

    freq = data.get("internal_reconciliation_frequency", "").lower()
    findings.append({
        "area": "Reconciliation", "rule": "MAS SFLCBR / SFO Cap.571I / ASIC RG 166",
        "description": "Daily client money reconciliation",
        "status": "GREEN" if freq == "daily" else "RED",
        "commentary": "Daily client money reconciliation confirmed across all accounts." if freq == "daily"
            else f"Reconciliation frequency: '{freq}'. Daily reconciliation required under MAS / SFC / ASIC rules.",
    })

    ack = data.get("acknowledgement_letters_all_accounts")
    findings.append({
        "area": "Account Documentation", "rule": "MAS SFLCBR / ASIC RG 166 / SFO",
        "description": "Trust account acknowledgement letters in place",
        "status": "GREEN" if ack else "AMBER",
        "commentary": "Trust account acknowledgement letters obtained from all institutions." if ack
            else "Acknowledgement letters not confirmed for all accounts. Required by MAS, ASIC, and SFC.",
    })

    return findings


def score_europe_health_check(data: dict) -> list:
    findings = []

    mifid_safe = data.get("mifid_safeguarding_compliant")
    findings.append({
        "area": "MiFID II Safeguarding", "rule": "MiFID II Art.16(9)",
        "description": "Client assets safeguarded per MiFID II Art.16(9)",
        "status": "GREEN" if mifid_safe else "RED",
        "commentary": "MiFID II Art.16(9) client asset safeguarding requirements met." if mifid_safe
            else "MiFID II Art.16(9) safeguarding not confirmed. Firms must arrange for client assets to be safeguarded at all times.",
    })

    del_reg = data.get("delegated_reg_2017_593_compliant")
    findings.append({
        "area": "MiFID II Safeguarding", "rule": "Del. Reg. 2017/593 Art.2",
        "description": "Client funds deposited with eligible credit institutions",
        "status": "GREEN" if del_reg else "RED",
        "commentary": "Client funds held with eligible credit institutions as required by Delegated Reg. 2017/593 Art.2." if del_reg
            else "Delegated Reg. 2017/593 Art.2 compliance not confirmed. Client funds must be deposited with eligible institutions only.",
    })

    ttca = data.get("ttca_arrangements")
    if ttca:
        ttca_consent = data.get("ttca_client_consent_obtained")
        findings.append({
            "area": "Title Transfer (TTCA)", "rule": "Del. Reg. 2017/593 Art.3",
            "description": "TTCA arrangements — client consent obtained and documented",
            "status": "GREEN" if ttca_consent else "RED",
            "commentary": "TTCA arrangements in place with client consent documented per Art.3." if ttca_consent
                else "TTCA in use WITHOUT documented client consent. Delegated Reg. 2017/593 Art.3 strictly limits TTCAs for retail clients.",
        })

    freq = data.get("internal_reconciliation_frequency", "").lower()
    findings.append({
        "area": "Reconciliation", "rule": "Del. Reg. 2017/593 Art.6",
        "description": "Daily client asset reconciliation",
        "status": "GREEN" if freq == "daily" else "RED",
        "commentary": "Daily reconciliation confirmed per Delegated Reg. 2017/593 Art.6." if freq == "daily"
            else f"Reconciliation frequency: '{freq}'. Daily reconciliation required under Delegated Reg. 2017/593 Art.6.",
    })

    ack = data.get("acknowledgement_letters_all_accounts")
    findings.append({
        "area": "Account Documentation", "rule": "Del. Reg. 2017/593 Art.4",
        "description": "Depositary / custodian acknowledgement and written agreement",
        "status": "GREEN" if ack else "AMBER",
        "commentary": "Custodian / depositary written agreements confirming segregation in place." if ack
            else "Written agreements with custodians not confirmed. Del. Reg. 2017/593 Art.4 requires acknowledgement of client asset segregation.",
    })

    dora = data.get("dora_compliant")
    findings.append({
        "area": "Operational Resilience", "rule": "DORA (EU Reg. 2022/2554)",
        "description": "DORA operational resilience for asset custody systems",
        "status": "GREEN" if dora else ("AMBER" if dora is None else "RED"),
        "commentary": "DORA operational resilience requirements met for custody systems." if dora
            else ("DORA compliance not confirmed. From 17 Jan 2025, EU financial entities must meet DORA requirements." if dora is None
                  else "DORA non-compliance identified. Immediate remediation required."),
    })

    return findings


def score_africa_health_check(data: dict) -> list:
    findings = []

    fais = data.get("fais_trust_property_compliant")
    findings.append({
        "area": "South Africa — FSCA", "rule": "FAIS Act s.19 / BN 106 of 2008",
        "description": "Client assets held as trust property",
        "status": "GREEN" if fais else "RED",
        "commentary": "FAIS Act trust property requirements met — client assets held separately from firm assets." if fais
            else "FAIS Act trust property compliance not confirmed. FSPs must hold client assets as trust property under FAIS Act s.19.",
    })

    fma = data.get("financial_markets_act_compliant")
    findings.append({
        "area": "South Africa — FMA", "rule": "Financial Markets Act s.78",
        "description": "Client asset segregation under Financial Markets Act",
        "status": "GREEN" if fma else ("AMBER" if fma is None else "RED"),
        "commentary": "FMA s.78 client asset segregation confirmed." if fma
            else ("FMA s.78 compliance not confirmed. Securities services providers must segregate client assets." if fma is None
                  else "FMA s.78 deficiency detected."),
    })

    ng = data.get("nigeria_sec_compliant")
    findings.append({
        "area": "Nigeria — SEC", "rule": "SEC Nigeria Rules 2013",
        "description": "Client money segregation per Nigeria SEC rules",
        "status": "GREEN" if ng else ("AMBER" if ng is None else "RED"),
        "commentary": "Nigeria SEC client money segregation confirmed." if ng
            else ("Nigeria SEC compliance not confirmed. Capital market operators must segregate client money." if ng is None
                  else "Nigeria SEC deficiency detected."),
    })

    ke = data.get("kenya_cma_compliant")
    findings.append({
        "area": "Kenya — CMA", "rule": "CMA Client Asset Regulations",
        "description": "Client assets per Kenya CMA rules",
        "status": "GREEN" if ke else ("AMBER" if ke is None else "RED"),
        "commentary": "Kenya CMA client asset requirements confirmed." if ke
            else ("Kenya CMA compliance not confirmed. Licensed firms must hold client assets per CMA regulations." if ke is None
                  else "Kenya CMA deficiency detected."),
    })

    freq = data.get("internal_reconciliation_frequency", "").lower()
    findings.append({
        "area": "Reconciliation", "rule": "FSCA / Local Regulator",
        "description": "Client asset reconciliation",
        "status": "GREEN" if freq in ("daily", "weekly") else "AMBER",
        "commentary": f"Reconciliation frequency: {freq}. Meets FSCA expectations." if freq in ("daily", "weekly")
            else "Reconciliation frequency not confirmed. FSCA expects regular reconciliation of client assets.",
    })

    vaitos = data.get("mauritius_vaitos_compliant")
    if vaitos is not None:
        findings.append({
            "area": "Mauritius — FSC", "rule": "VAITOS Act",
            "description": "Digital asset client rules under VAITOS Act",
            "status": "GREEN" if vaitos else "AMBER",
            "commentary": "VAITOS Act digital asset client rules confirmed." if vaitos
                else "VAITOS compliance not confirmed. Digital asset service providers in Mauritius must comply with VAITOS Act client rules.",
        })

    return findings


def score_regional_health_check(data: dict, region: str) -> list:
    dispatch = {
        "N. America":    score_us_health_check,
        "Latin America": score_latam_health_check,
        "Asia Pacific":  score_apac_health_check,
        "Europe":        score_europe_health_check,
        "Africa":        score_africa_health_check,
    }
    fn = dispatch.get(region)
    return fn(data) if fn else []


# ══════════════════════════════════════════════════════════════════════════════
# RESOLUTION PACK — mirrors CASS 10
# ══════════════════════════════════════════════════════════════════════════════

def score_us_resolution_pack(data: dict) -> list:
    findings = []

    sipc_prep = data.get("sipc_liquidation_procedures_documented") or data.get("crp_document_exists")
    findings.append({
        "area": "Liquidation Readiness", "rule": "SIPA / SEC Rule 15c3-3(i)",
        "description": "SIPC liquidation procedures documented",
        "status": "GREEN" if sipc_prep else "AMBER",
        "commentary": "SIPC liquidation procedures documented — customer net equity calculation methodology in place." if sipc_prep
            else "SIPC liquidation procedures not documented. Prepare customer net equity calculation procedures per SIPA.",
    })

    schedules = data.get("customer_property_schedules_maintained") or data.get("client_asset_schedule")
    findings.append({
        "area": "Customer Property Records", "rule": "SEC Rule 15c3-3(i)",
        "description": "Customer property schedules maintained",
        "status": "GREEN" if schedules else "RED",
        "commentary": "Customer property schedules maintained — securities and cash positions readily identifiable." if schedules
            else "Customer property schedules not maintained. SEC Rule 15c3-3(i) requires records sufficient for SIPC liquidation.",
    })

    accessible = data.get("crp_accessible_48hrs") or data.get("records_accessible_24hrs")
    findings.append({
        "area": "Records Accessibility", "rule": "SEC Rule 17a-3 / 17a-4",
        "description": "Customer account records accessible within 24 hours",
        "status": "GREEN" if accessible else "AMBER",
        "commentary": "Customer records accessible within the required timeframe." if accessible
            else "Records accessibility not confirmed. SEC Rules 17a-3/17a-4 require prompt access to customer records.",
    })

    bcp = data.get("crp_document_exists") or data.get("business_continuity_plan_exists")
    findings.append({
        "area": "Business Continuity Plan", "rule": "FINRA Rule 4370",
        "description": "Business Continuity Plan (BCP) approved by senior management",
        "status": "GREEN" if bcp else "RED",
        "commentary": "FINRA Rule 4370 BCP approved by senior management." if bcp
            else "No BCP on file. FINRA Rule 4370 requires a written, approved BCP for all member firms.",
    })

    named = data.get("crp_responsible_individual")
    findings.append({
        "area": "Accountability", "rule": "SEC / FINRA",
        "description": "Named individual responsible for customer asset return procedures",
        "status": "GREEN" if named else "AMBER",
        "commentary": f"Responsible individual: {named}." if named else "No named individual for customer asset return. Assign clear accountability.",
    })

    tested = data.get("crp_tested")
    last_test = data.get("crp_last_test_date", "unknown")
    findings.append({
        "area": "BCP Testing", "rule": "FINRA Rule 4370",
        "description": "BCP tested annually",
        "status": "GREEN" if tested else "AMBER",
        "commentary": f"BCP tested. Last test: {last_test}." if tested else "BCP not tested. FINRA Rule 4370 requires annual review and testing.",
    })

    secure = data.get("crp_secure_offsite_storage")
    findings.append({
        "area": "Records Storage", "rule": "SEC Rule 17a-4",
        "description": "Customer records stored securely with off-site / cloud access",
        "status": "GREEN" if secure else "AMBER",
        "commentary": "Secure off-site / cloud storage for customer records confirmed." if secure
            else "Off-site record storage not confirmed. SEC Rule 17a-4 requires secure, accessible storage.",
    })

    return findings


def score_latam_resolution_pack(data: dict) -> list:
    findings = []

    bcp = data.get("crp_document_exists")
    findings.append({
        "area": "Resolution Procedures", "rule": "Local Insolvency Law",
        "description": "Client asset return / resolution procedures documented",
        "status": "GREEN" if bcp else "RED",
        "commentary": "Client asset return procedures documented under applicable local insolvency law." if bcp
            else "No resolution / client asset return procedures. Prepare under applicable local insolvency law.",
    })

    schedules = data.get("client_asset_schedule")
    findings.append({
        "area": "Client Asset Schedule", "rule": "CVM / CNBV / SFC",
        "description": "Client asset schedule maintained",
        "status": "GREEN" if schedules else "AMBER",
        "commentary": "Client asset schedule maintained and current." if schedules
            else "Client asset schedule not confirmed. Maintain an up-to-date schedule of all client assets held.",
    })

    accessible = data.get("crp_accessible_48hrs")
    findings.append({
        "area": "Records Accessibility", "rule": "Local Reg.",
        "description": "Client asset records accessible within 48 hours",
        "status": "GREEN" if accessible else "AMBER",
        "commentary": "Client records accessible within 48 hours." if accessible
            else "48-hour accessibility not confirmed. Ensure records can be produced rapidly in insolvency scenarios.",
    })

    named = data.get("crp_responsible_individual")
    findings.append({
        "area": "Accountability", "rule": "Local Reg.",
        "description": "Named individual responsible for client asset return",
        "status": "GREEN" if named else "AMBER",
        "commentary": f"Responsible individual: {named}." if named else "No named individual for client asset return. Assign responsibility.",
    })

    tested = data.get("crp_tested")
    findings.append({
        "area": "Testing", "rule": "Local Reg.",
        "description": "Resolution procedures tested",
        "status": "GREEN" if tested else "AMBER",
        "commentary": "Resolution procedures tested." if tested else "Resolution procedures not tested. Annual dry-run recommended.",
    })

    return findings


def score_apac_resolution_pack(data: dict) -> list:
    findings = []

    bcp = data.get("crp_document_exists")
    findings.append({
        "area": "Resolution Procedures", "rule": "MAS Reg 17 / ASIC RG 166 / SFC Code",
        "description": "Client asset return readiness procedures documented",
        "status": "GREEN" if bcp else "RED",
        "commentary": "Client asset return procedures documented per regional requirements." if bcp
            else "No resolution procedures. MAS Reg 17, ASIC RG 166, and SFC Code all require client asset return planning.",
    })

    schedules = data.get("client_asset_schedule")
    findings.append({
        "area": "Client Asset Schedule", "rule": "MAS SFLCBR / ASIC RG 166 / SFO",
        "description": "Client asset schedule maintained",
        "status": "GREEN" if schedules else "RED",
        "commentary": "Client asset schedule maintained and current." if schedules
            else "Client asset schedule not confirmed. Required under MAS SFLCBR, ASIC RG 166, and SFC regulations.",
    })

    accessible = data.get("crp_accessible_48hrs")
    findings.append({
        "area": "Records Accessibility", "rule": "MAS / ASIC / SFC",
        "description": "Client asset records accessible within 48 hours",
        "status": "GREEN" if accessible else "AMBER",
        "commentary": "48-hour accessibility confirmed." if accessible else "48-hour access not confirmed. Regional regulators require rapid access.",
    })

    named = data.get("crp_responsible_individual")
    findings.append({
        "area": "Accountability", "rule": "MAS / ASIC / SFC",
        "description": "Named individual responsible for client asset return",
        "status": "GREEN" if named else "AMBER",
        "commentary": f"Responsible individual: {named}." if named else "No named individual for client asset return.",
    })

    tested = data.get("crp_tested")
    last_test = data.get("crp_last_test_date", "unknown")
    findings.append({
        "area": "Testing", "rule": "MAS / ASIC / SFC",
        "description": "Resolution procedures dry-run tested",
        "status": "GREEN" if tested else "AMBER",
        "commentary": f"Resolution procedures tested. Last test: {last_test}." if tested
            else "Resolution procedures not tested. Annual testing recommended by MAS, ASIC, and SFC.",
    })

    secure = data.get("crp_secure_offsite_storage")
    findings.append({
        "area": "Records Storage", "rule": "MAS / ASIC / SFC",
        "description": "Secure off-site / cloud storage for client records",
        "status": "GREEN" if secure else "AMBER",
        "commentary": "Secure off-site / cloud storage confirmed." if secure else "Off-site storage not confirmed.",
    })

    return findings


def score_europe_resolution_pack(data: dict) -> list:
    findings = []

    bcp = data.get("crp_document_exists")
    findings.append({
        "area": "Client Asset Safeguarding Plan", "rule": "MiFID II Art.16 / BRRD",
        "description": "Client asset return / safeguarding plan documented",
        "status": "GREEN" if bcp else "RED",
        "commentary": "Client asset safeguarding and return plan documented per MiFID II Art.16 requirements." if bcp
            else "No client asset return plan. MiFID II Art.16 requires firms to plan for client asset protection in wind-down.",
    })

    schedules = data.get("client_asset_schedule")
    findings.append({
        "area": "Client Asset Schedule", "rule": "Del. Reg. 2017/593 Art.7",
        "description": "Client asset schedule and records maintained",
        "status": "GREEN" if schedules else "RED",
        "commentary": "Client asset schedule maintained per Delegated Reg. 2017/593 Art.7." if schedules
            else "Client asset schedule not confirmed. Art.7 requires records enabling resolution authorities to identify all client assets.",
    })

    accessible = data.get("crp_accessible_48hrs")
    findings.append({
        "area": "Records Accessibility", "rule": "MiFID II / BRRD",
        "description": "Client assets identifiable within 48 hours",
        "status": "GREEN" if accessible else "AMBER",
        "commentary": "Client assets identifiable within 48 hours — resolution authority requirements met." if accessible
            else "48-hour accessibility not confirmed. Resolution authorities require rapid identification of client assets.",
    })

    named = data.get("crp_responsible_individual")
    findings.append({
        "area": "Accountability", "rule": "MiFID II",
        "description": "Named individual for client asset safeguarding plan",
        "status": "GREEN" if named else "AMBER",
        "commentary": f"Responsible individual: {named}." if named else "No named individual for client asset safeguarding plan.",
    })

    psd2 = data.get("psd2_safeguarding_compliant")
    findings.append({
        "area": "Payment Safeguarding", "rule": "PSD2 Art.10 / PSD3",
        "description": "PSD2 / PSD3 payment institution safeguarding",
        "status": "GREEN" if psd2 else ("AMBER" if psd2 is None else "RED"),
        "commentary": "PSD2 Art.10 safeguarding requirements met." if psd2
            else ("PSD2 safeguarding status not confirmed. Verify if payment institution rules apply." if psd2 is None
                  else "PSD2 safeguarding deficiency. Payment institutions must safeguard client funds under PSD2 Art.10."),
    })

    tested = data.get("crp_tested")
    findings.append({
        "area": "Testing", "rule": "MiFID II / ESMA",
        "description": "Safeguarding plan tested",
        "status": "GREEN" if tested else "AMBER",
        "commentary": "Safeguarding plan tested." if tested else "Safeguarding plan not tested. Annual testing recommended.",
    })

    return findings


def score_africa_resolution_pack(data: dict) -> list:
    findings = []

    bcp = data.get("crp_document_exists")
    findings.append({
        "area": "Resolution Procedures", "rule": "FAIS Act / FMA / Local Reg.",
        "description": "Client asset return / resolution procedures documented",
        "status": "GREEN" if bcp else "RED",
        "commentary": "Client asset return procedures documented." if bcp
            else "No resolution procedures. FSCA and local regulators require firms to plan for client asset protection.",
    })

    trust_deed = data.get("trust_deed_in_place") or data.get("client_asset_schedule")
    findings.append({
        "area": "Trust Documentation", "rule": "FAIS Act s.19 / BN 106 of 2008",
        "description": "Trust deed / trust account documentation in place",
        "status": "GREEN" if trust_deed else "RED",
        "commentary": "Trust documentation confirmed." if trust_deed
            else "Trust deed / documentation not confirmed. FAIS Act requires client assets held as trust property — trust documentation is mandatory.",
    })

    accessible = data.get("crp_accessible_48hrs")
    findings.append({
        "area": "Records Accessibility", "rule": "FSCA / Local Reg.",
        "description": "Client asset records accessible within 48 hours",
        "status": "GREEN" if accessible else "AMBER",
        "commentary": "48-hour accessibility confirmed." if accessible else "48-hour access not confirmed.",
    })

    named = data.get("crp_responsible_individual")
    findings.append({
        "area": "Accountability", "rule": "FSCA / Local Reg.",
        "description": "Named individual responsible for client asset return",
        "status": "GREEN" if named else "AMBER",
        "commentary": f"Responsible individual: {named}." if named else "No named individual for client asset return.",
    })

    tested = data.get("crp_tested")
    findings.append({
        "area": "Testing", "rule": "FSCA / Local Reg.",
        "description": "Resolution procedures tested",
        "status": "GREEN" if tested else "AMBER",
        "commentary": "Resolution procedures tested." if tested else "Resolution procedures not tested. Annual dry-run recommended.",
    })

    return findings


def score_regional_resolution_pack(data: dict, region: str) -> list:
    dispatch = {
        "N. America":    score_us_resolution_pack,
        "Latin America": score_latam_resolution_pack,
        "Asia Pacific":  score_apac_resolution_pack,
        "Europe":        score_europe_resolution_pack,
        "Africa":        score_africa_resolution_pack,
    }
    fn = dispatch.get(region)
    return fn(data) if fn else []


# ══════════════════════════════════════════════════════════════════════════════
# BREACH LOG — mirrors CASS 7.13.65R / SUP 15
# ══════════════════════════════════════════════════════════════════════════════

def score_us_breach_log(data: dict) -> list:
    findings = []

    register = data.get("breach_register_maintained", False)
    findings.append({
        "area": "Violation Register", "rule": "FINRA Rule 4530",
        "description": "Compliance violation / breach register maintained",
        "status": "GREEN" if register else "RED",
        "commentary": "Compliance violation register maintained." if register
            else "No violation register. FINRA Rule 4530 requires firms to report and retain records of specified events.",
    })

    finra_notified = data.get("fca_notified") or data.get("finra_notified")
    findings.append({
        "area": "FINRA Notification", "rule": "FINRA Rule 4530",
        "description": "FINRA notified of material violations (within 30 days)",
        "status": "GREEN" if finra_notified else ("AMBER" if finra_notified is None else "RED"),
        "commentary": "FINRA notified as required under Rule 4530." if finra_notified
            else ("FINRA notification status not confirmed. Rule 4530 requires prompt reporting of specified events." if finra_notified is None
                  else "FINRA NOT notified. Rule 4530 requires notification within 30 calendar days."),
    })

    sec_notified = data.get("sec_notified")
    if sec_notified is not None:
        findings.append({
            "area": "SEC Notification", "rule": "SEC Rule 17a-11",
            "description": "SEC notified of net capital or reserve violations",
            "status": "GREEN" if sec_notified else "RED",
            "commentary": "SEC notified per Rule 17a-11 (same/next business day)." if sec_notified
                else "SEC notification NOT confirmed. Rule 17a-11 requires immediate notification of net capital or reserve deficiencies.",
        })

    cftc_notified = data.get("cftc_notified")
    if cftc_notified is not None:
        findings.append({
            "area": "CFTC Notification", "rule": "CFTC Reg 3.12 / NFA Rule 2-45",
            "description": "CFTC / NFA notified of material violations",
            "status": "GREEN" if cftc_notified else "RED",
            "commentary": "CFTC / NFA notified as required." if cftc_notified else "CFTC / NFA notification not confirmed.",
        })

    sar_filed = data.get("sar_filed")
    if sar_filed is not None:
        findings.append({
            "area": "SAR Filing", "rule": "BSA 31 U.S.C. §5318(g)",
            "description": "Suspicious Activity Report (SAR) filed with FinCEN",
            "status": "GREEN" if sar_filed else "RED",
            "commentary": "SAR filed with FinCEN within 30-day requirement." if sar_filed
                else "SAR required but not filed. BSA requires SAR filing within 30 days of detection.",
        })

    rca = data.get("root_cause_analysis", False)
    findings.append({
        "area": "Root Cause Analysis", "rule": "SEC / FINRA Best Practice",
        "description": "Root cause analysis completed for each violation",
        "status": "GREEN" if rca else "AMBER",
        "commentary": "Root cause analysis completed." if rca else "Root cause analysis not completed. Required to prevent recurrence.",
    })

    repeat = data.get("repeat_violations") or data.get("outstanding_coof_recommendations")
    findings.append({
        "area": "Repeat Violations", "rule": "FINRA Rule 4530",
        "description": "No repeat violation patterns",
        "status": "RED" if repeat else "GREEN",
        "commentary": f"Repeat violation(s) identified: {repeat}. Systemic failure — immediate remediation required." if repeat
            else "No repeat violation patterns identified in review period.",
    })

    return findings


def score_latam_breach_log(data: dict) -> list:
    findings = []

    register = data.get("breach_register_maintained", False)
    findings.append({
        "area": "Breach Register", "rule": "Local Regulator",
        "description": "Breach / violation register maintained",
        "status": "GREEN" if register else "RED",
        "commentary": "Breach register maintained." if register else "No breach register. Maintain records of all regulatory breaches per local requirements.",
    })

    notified = data.get("fca_notified") or data.get("local_regulator_notified")
    findings.append({
        "area": "Regulator Notification", "rule": "CVM / CNBV / SFC / CMF",
        "description": "Local regulator notified of material breaches",
        "status": "GREEN" if notified else ("AMBER" if notified is None else "RED"),
        "commentary": "Local regulator notified of material breaches." if notified
            else ("Notification status not confirmed. Local rules require prompt notification of material breaches." if notified is None
                  else "Regulator NOT notified. Immediate notification required."),
    })

    rca = data.get("root_cause_analysis", False)
    findings.append({
        "area": "Root Cause Analysis", "rule": "Local Reg.",
        "description": "Root cause analysis completed",
        "status": "GREEN" if rca else "AMBER",
        "commentary": "Root cause analysis completed." if rca else "Root cause analysis not completed. Required to prevent recurrence.",
    })

    remediation = data.get("remediation_status", "").lower()
    findings.append({
        "area": "Remediation", "rule": "Local Reg.",
        "description": "Remediation actions documented and in progress",
        "status": "GREEN" if remediation == "complete" else ("AMBER" if remediation in ("in-progress", "in progress") else "RED"),
        "commentary": f"Remediation status: {remediation.upper()}." if remediation else "Remediation status not provided.",
    })

    return findings


def score_apac_breach_log(data: dict) -> list:
    findings = []

    register = data.get("breach_register_maintained", False)
    findings.append({
        "area": "Breach Register", "rule": "MAS Reg 57 / SFO s.201 / ASIC s.912D",
        "description": "Breach / incident register maintained",
        "status": "GREEN" if register else "RED",
        "commentary": "Breach register maintained." if register
            else "No breach register. MAS Reg 57, SFO s.201, and ASIC s.912D all require breach registers.",
    })

    notified = data.get("fca_notified") or data.get("mas_notified") or data.get("local_regulator_notified")
    findings.append({
        "area": "Regulator Notification", "rule": "MAS Reg 57 / SFO s.201 / ASIC s.912D / FIEA",
        "description": "Regulator notified of material breaches",
        "status": "GREEN" if notified else ("AMBER" if notified is None else "RED"),
        "commentary": "Regulator notified as required." if notified
            else ("Notification status not confirmed. MAS, SFC, ASIC, and FSA require prompt notification of material breaches." if notified is None
                  else "Regulator NOT notified. Immediate notification required."),
    })

    rca = data.get("root_cause_analysis", False)
    findings.append({
        "area": "Root Cause Analysis", "rule": "MAS / ASIC / SFC / FSA",
        "description": "Root cause analysis completed",
        "status": "GREEN" if rca else "AMBER",
        "commentary": "Root cause analysis completed." if rca else "Root cause analysis not completed.",
    })

    remediation = data.get("remediation_status", "").lower()
    findings.append({
        "area": "Remediation", "rule": "MAS / ASIC / SFC / FSA",
        "description": "Remediation actions documented",
        "status": "GREEN" if remediation == "complete" else ("AMBER" if remediation in ("in-progress", "in progress") else "RED"),
        "commentary": f"Remediation status: {remediation.upper()}." if remediation else "Remediation status not confirmed.",
    })

    return findings


def score_europe_breach_log(data: dict) -> list:
    findings = []

    register = data.get("breach_register_maintained", False)
    findings.append({
        "area": "Breach Register", "rule": "MiFID II Art.25 / ESMA Guidelines",
        "description": "Safeguarding breach register maintained",
        "status": "GREEN" if register else "RED",
        "commentary": "MiFID II breach register maintained." if register
            else "No breach register. MiFID II Art.25 and ESMA guidelines require recording of all safeguarding breaches.",
    })

    nca_notified = data.get("fca_notified") or data.get("nca_notified")
    findings.append({
        "area": "NCA Notification", "rule": "MiFID II Art.25 / Local NCA Rules",
        "description": "National Competent Authority (NCA) notified",
        "status": "GREEN" if nca_notified else ("AMBER" if nca_notified is None else "RED"),
        "commentary": "NCA notified of material safeguarding breach (BaFin / AMF / CBI / AFM / etc.)." if nca_notified
            else ("NCA notification not confirmed. MiFID II requires notification to the local NCA." if nca_notified is None
                  else "NCA NOT notified. Immediate notification required — failure to notify is a material breach."),
    })

    dora_incident = data.get("dora_incident_reported")
    if dora_incident is not None:
        findings.append({
            "area": "DORA Incident Reporting", "rule": "DORA Art.19",
            "description": "DORA major ICT incident reported to NCA",
            "status": "GREEN" if dora_incident else "RED",
            "commentary": "DORA Art.19 major ICT incident reported to NCA within required timeframe." if dora_incident
                else "DORA incident reporting not confirmed. From 17 Jan 2025, major ICT incidents must be reported under DORA Art.19.",
        })

    rca = data.get("root_cause_analysis", False)
    findings.append({
        "area": "Root Cause Analysis", "rule": "MiFID II / ESMA",
        "description": "Root cause analysis completed",
        "status": "GREEN" if rca else "AMBER",
        "commentary": "Root cause analysis completed." if rca else "Root cause analysis not completed.",
    })

    remediation = data.get("remediation_status", "").lower()
    findings.append({
        "area": "Remediation", "rule": "MiFID II / ESMA",
        "description": "Remediation actions documented",
        "status": "GREEN" if remediation == "complete" else ("AMBER" if remediation in ("in-progress", "in progress") else "RED"),
        "commentary": f"Remediation status: {remediation.upper()}." if remediation else "Remediation status not confirmed.",
    })

    return findings


def score_africa_breach_log(data: dict) -> list:
    findings = []

    register = data.get("breach_register_maintained", False)
    findings.append({
        "area": "Breach Register", "rule": "FSCA / FAIS Act / CBN / CMA",
        "description": "Breach register maintained",
        "status": "GREEN" if register else "RED",
        "commentary": "Breach register maintained." if register
            else "No breach register. FSCA, CBN, and CMA require records of all regulatory breaches.",
    })

    fsca_notified = data.get("fca_notified") or data.get("fsca_notified") or data.get("local_regulator_notified")
    findings.append({
        "area": "Regulator Notification", "rule": "FSCA / CBN / CMA",
        "description": "Local regulator notified of material breaches",
        "status": "GREEN" if fsca_notified else ("AMBER" if fsca_notified is None else "RED"),
        "commentary": "Regulator notified (FSCA / CBN / CMA)." if fsca_notified
            else ("Notification status not confirmed. FSCA, CBN, and CMA require notification of material breaches." if fsca_notified is None
                  else "Regulator NOT notified. Immediate notification required."),
    })

    rca = data.get("root_cause_analysis", False)
    findings.append({
        "area": "Root Cause Analysis", "rule": "FSCA / Local Reg.",
        "description": "Root cause analysis completed",
        "status": "GREEN" if rca else "AMBER",
        "commentary": "Root cause analysis completed." if rca else "Root cause analysis not completed. Required to prevent recurrence.",
    })

    remediation = data.get("remediation_status", "").lower()
    findings.append({
        "area": "Remediation", "rule": "FSCA / Local Reg.",
        "description": "Remediation actions documented",
        "status": "GREEN" if remediation == "complete" else ("AMBER" if remediation in ("in-progress", "in progress") else "RED"),
        "commentary": f"Remediation status: {remediation.upper()}." if remediation else "Remediation status not confirmed.",
    })

    return findings


def score_regional_breach_log(data: dict, region: str) -> list:
    dispatch = {
        "N. America":    score_us_breach_log,
        "Latin America": score_latam_breach_log,
        "Asia Pacific":  score_apac_breach_log,
        "Europe":        score_europe_breach_log,
        "Africa":        score_africa_breach_log,
    }
    fn = dispatch.get(region)
    return fn(data) if fn else []


# ══════════════════════════════════════════════════════════════════════════════
# OVERSIGHT — mirrors CASS 1A COOF
# ══════════════════════════════════════════════════════════════════════════════

def score_us_oversight(data: dict) -> list:
    findings = []
    is_large = data.get("cass_category", "").lower() == "large"

    cco = data.get("coof_individual_name") or data.get("cco_named")
    findings.append({
        "area": "CCO Appointment", "rule": "SEC Rule 206(4)-7 / FINRA Rule 3130",
        "description": "Chief Compliance Officer (CCO) designated",
        "status": "GREEN" if cco else "RED",
        "commentary": f"CCO designated: {cco}." if cco
            else "No CCO designated. SEC Rule 206(4)-7 and FINRA Rule 3130 require a formally designated CCO.",
    })

    qualified = data.get("coof_individual_qualified")
    findings.append({
        "area": "CCO Qualifications", "rule": "FINRA / SEC",
        "description": "CCO qualifications and compliance expertise verified",
        "status": "GREEN" if qualified else "AMBER",
        "commentary": "CCO qualifications confirmed." if qualified
            else "CCO qualifications not confirmed. Verify FINRA Series 14 or equivalent compliance expertise.",
    })

    dual_role = data.get("coof_also_compliance_officer") or data.get("cco_also_revenue_generating")
    findings.append({
        "area": "CCO Independence", "rule": "FINRA Rule 3130",
        "description": "CCO not primarily performing revenue-generating functions",
        "status": "AMBER" if dual_role else "GREEN",
        "commentary": "CCO also performs revenue-generating functions — independence concern under FINRA Rule 3130." if dual_role
            else "CCO operates independently of revenue-generating functions.",
    })

    last_report = data.get("last_coof_report_to_board_date")
    if last_report:
        try:
            days = (date.today() - datetime.strptime(last_report, "%Y-%m-%d").date()).days
            s = "GREEN" if days <= 365 else "RED"
            c = f"Annual compliance review report delivered {last_report} ({days} days ago)." + (" OVERDUE." if s == "RED" else "")
        except Exception:
            s, c = "AMBER", "Annual report date not readable — confirm delivery."
    else:
        s, c = "RED", "No annual compliance review report on record. SEC Rule 206(4)-7 and FINRA Rule 3130 require annual compliance review."
    findings.append({"area": "Annual Review Report", "rule": "SEC Rule 206(4)-7 / FINRA Rule 3130",
                     "description": "Annual compliance review report delivered to senior management", "status": s, "commentary": c})

    wsp = data.get("written_supervisory_procedures") or data.get("board_minutes_confirm_coof_report")
    findings.append({
        "area": "Written Supervisory Procedures", "rule": "FINRA Rule 3110",
        "description": "Written Supervisory Procedures (WSPs) in place and current",
        "status": "GREEN" if wsp else "RED",
        "commentary": "Written Supervisory Procedures in place and current." if wsp
            else "No WSPs confirmed. FINRA Rule 3110 requires written supervisory procedures covering all activities.",
    })

    last_review = data.get("last_coof_review_of_cass_date")
    if last_review:
        try:
            days = (date.today() - datetime.strptime(last_review, "%Y-%m-%d").date()).days
            s = "GREEN" if days <= 365 else "AMBER"
            c = f"Last CCO review of compliance arrangements: {last_review} ({days} days ago)."
        except Exception:
            s, c = "AMBER", "Review date unreadable."
    else:
        s, c = "AMBER", "No review date on record. Regular CCO review of compliance arrangements expected."
    findings.append({"area": "CCO Activity", "rule": "FINRA Rule 3130",
                     "description": "CCO review of compliance arrangements", "status": s, "commentary": c})

    outstanding = data.get("outstanding_coof_recommendations")
    if outstanding:
        rec_count = len(outstanding) if isinstance(outstanding, list) else int(outstanding)
        findings.append({"area": "Outstanding Items", "rule": "SEC / FINRA",
                         "description": "Outstanding CCO recommendations",
                         "status": "RED",
                         "commentary": f"{rec_count} outstanding CCO recommendation(s) with no confirmed action plan."})
    else:
        findings.append({"area": "Outstanding Items", "rule": "SEC / FINRA",
                         "description": "Outstanding CCO recommendations",
                         "status": "GREEN", "commentary": "No outstanding CCO recommendations."})

    return findings


def score_latam_oversight(data: dict) -> list:
    findings = []

    named = data.get("coof_individual_name") or data.get("compliance_officer_named")
    findings.append({
        "area": "Compliance Officer", "rule": "CVM / CNBV / SFC — Compliance",
        "description": "Compliance officer designated",
        "status": "GREEN" if named else "RED",
        "commentary": f"Compliance officer designated: {named}." if named
            else "No compliance officer designated. Local regulations require a named compliance officer.",
    })

    qualified = data.get("coof_individual_qualified")
    findings.append({
        "area": "Qualifications", "rule": "Local Reg.",
        "description": "Compliance officer qualifications verified",
        "status": "GREEN" if qualified else "AMBER",
        "commentary": "Qualifications verified." if qualified else "Qualifications not confirmed. Verify local licensing requirements.",
    })

    dual = data.get("coof_also_compliance_officer")
    findings.append({
        "area": "Independence", "rule": "Local Reg.",
        "description": "Compliance officer independence",
        "status": "AMBER" if dual else "GREEN",
        "commentary": "Independence concern — compliance officer also performing other functions." if dual
            else "Compliance officer operates independently.",
    })

    last_report = data.get("last_coof_report_to_board_date")
    if last_report:
        try:
            days = (date.today() - datetime.strptime(last_report, "%Y-%m-%d").date()).days
            s = "GREEN" if days <= 365 else "RED"
            c = f"Annual compliance report delivered {last_report} ({days} days ago)." + (" OVERDUE." if s == "RED" else "")
        except Exception:
            s, c = "AMBER", "Report date not readable."
    else:
        s, c = "RED", "No annual compliance report on record. Annual reporting to board is required."
    findings.append({"area": "Annual Report", "rule": "CVM / CNBV / SFC",
                     "description": "Annual compliance report to board", "status": s, "commentary": c})

    outstanding = data.get("outstanding_coof_recommendations")
    if outstanding:
        rec_count = len(outstanding) if isinstance(outstanding, list) else int(outstanding)
        findings.append({"area": "Outstanding Items", "rule": "Local Reg.",
                         "description": "Outstanding compliance recommendations",
                         "status": "RED",
                         "commentary": f"{rec_count} outstanding recommendation(s) — no confirmed action plan."})
    else:
        findings.append({"area": "Outstanding Items", "rule": "Local Reg.",
                         "description": "Outstanding compliance recommendations",
                         "status": "GREEN", "commentary": "No outstanding recommendations."})

    return findings


def score_apac_oversight(data: dict) -> list:
    findings = []

    named = data.get("coof_individual_name") or data.get("head_of_compliance")
    findings.append({
        "area": "Compliance Officer", "rule": "MAS Guidelines / ASIC RG 104 / SFC Code",
        "description": "Head of Compliance / Compliance Manager designated",
        "status": "GREEN" if named else "RED",
        "commentary": f"Compliance officer designated: {named}." if named
            else "No compliance officer designated. MAS, ASIC, and SFC all require a designated compliance manager.",
    })

    qualified = data.get("coof_individual_qualified")
    findings.append({
        "area": "Qualifications", "rule": "MAS / ASIC RG 104 / SFC",
        "description": "Compliance officer qualifications confirmed",
        "status": "GREEN" if qualified else "AMBER",
        "commentary": "Qualifications confirmed per MAS / ASIC / SFC requirements." if qualified
            else "Qualifications not confirmed. Verify relevant licensing and compliance expertise.",
    })

    dual = data.get("coof_also_compliance_officer")
    findings.append({
        "area": "Independence", "rule": "MAS / ASIC / SFC",
        "description": "Compliance function independence",
        "status": "AMBER" if dual else "GREEN",
        "commentary": "Independence concern — compliance also performing other functions." if dual
            else "Compliance function operates independently.",
    })

    last_report = data.get("last_coof_report_to_board_date")
    if last_report:
        try:
            days = (date.today() - datetime.strptime(last_report, "%Y-%m-%d").date()).days
            s = "GREEN" if days <= 365 else "RED"
            c = f"Annual compliance report delivered {last_report} ({days} days ago)." + (" OVERDUE." if s == "RED" else "")
        except Exception:
            s, c = "AMBER", "Report date unreadable."
    else:
        s, c = "RED", "No annual compliance report on record. MAS, ASIC, and SFC require periodic compliance reporting to senior management."
    findings.append({"area": "Annual Report", "rule": "MAS / ASIC RG 104 / SFC Code",
                     "description": "Annual compliance report to management body", "status": s, "commentary": c})

    last_review = data.get("last_coof_review_of_cass_date")
    if last_review:
        try:
            days = (date.today() - datetime.strptime(last_review, "%Y-%m-%d").date()).days
            s = "GREEN" if days <= 365 else "AMBER"
            c = f"Last compliance review of arrangements: {last_review} ({days} days ago)."
        except Exception:
            s, c = "AMBER", "Review date unreadable."
    else:
        s, c = "AMBER", "No review date on record. Regular compliance reviews expected by MAS, ASIC, and SFC."
    findings.append({"area": "Compliance Activity", "rule": "MAS / ASIC / SFC",
                     "description": "Review of compliance arrangements", "status": s, "commentary": c})

    outstanding = data.get("outstanding_coof_recommendations")
    if outstanding:
        rec_count = len(outstanding) if isinstance(outstanding, list) else int(outstanding)
        findings.append({"area": "Outstanding Items", "rule": "MAS / ASIC / SFC",
                         "description": "Outstanding compliance recommendations",
                         "status": "RED",
                         "commentary": f"{rec_count} outstanding recommendation(s) with no confirmed action plan."})
    else:
        findings.append({"area": "Outstanding Items", "rule": "MAS / ASIC / SFC",
                         "description": "Outstanding compliance recommendations",
                         "status": "GREEN", "commentary": "No outstanding compliance recommendations."})

    return findings


def score_europe_oversight(data: dict) -> list:
    findings = []

    named = data.get("coof_individual_name") or data.get("compliance_officer_named")
    findings.append({
        "area": "Compliance Function Head", "rule": "MiFID II Art.16(2)",
        "description": "Compliance function head designated (permanent function)",
        "status": "GREEN" if named else "RED",
        "commentary": f"Compliance function head designated: {named}." if named
            else "No compliance function head designated. MiFID II Art.16(2) requires a permanent, effective compliance function.",
    })

    qualified = data.get("coof_individual_qualified")
    findings.append({
        "area": "Qualifications", "rule": "MiFID II Art.16(2) / ESMA Guidelines",
        "description": "Compliance officer expertise, authority, and resources",
        "status": "GREEN" if qualified else "AMBER",
        "commentary": "Compliance expertise confirmed per ESMA guidelines on compliance function under MiFID II." if qualified
            else "Expertise not confirmed. ESMA guidelines require compliance personnel with appropriate knowledge and authority.",
    })

    dual = data.get("coof_also_compliance_officer")
    findings.append({
        "area": "Independence", "rule": "MiFID II Art.16(2)",
        "description": "Compliance function independence from business lines",
        "status": "AMBER" if dual else "GREEN",
        "commentary": "Independence concern — review against MiFID II Art.16(2) separation requirements." if dual
            else "Compliance function independent from business lines.",
    })

    last_report = data.get("last_coof_report_to_board_date")
    minutes = data.get("board_minutes_confirm_coof_report")
    if last_report:
        try:
            days = (date.today() - datetime.strptime(last_report, "%Y-%m-%d").date()).days
            s = "GREEN" if days <= 365 else "RED"
            c = f"Compliance report to management body: {last_report} ({days} days ago)." + (" OVERDUE." if s == "RED" else "")
        except Exception:
            s, c = "AMBER", "Report date unreadable."
    else:
        s, c = "RED", "No annual compliance report to management body. MiFID II Art.16(2) requires periodic compliance reporting."
    findings.append({"area": "Annual Report", "rule": "MiFID II Art.16(2)",
                     "description": "Annual compliance report to management body", "status": s, "commentary": c})

    findings.append({
        "area": "Governance Evidence", "rule": "MiFID II Art.16(2)",
        "description": "Board / committee minutes confirm compliance report received",
        "status": "GREEN" if minutes else "AMBER",
        "commentary": "Minutes confirm compliance report received and noted." if minutes
            else "No board minutes confirming compliance report receipt. Minutes should evidence governance oversight.",
    })

    last_review = data.get("last_coof_review_of_cass_date")
    if last_review:
        try:
            days = (date.today() - datetime.strptime(last_review, "%Y-%m-%d").date()).days
            s = "GREEN" if days <= 365 else "AMBER"
            c = f"Last compliance review: {last_review} ({days} days ago)."
        except Exception:
            s, c = "AMBER", "Review date unreadable."
    else:
        s, c = "AMBER", "No review date on record. Regular compliance reviews required under MiFID II Art.16(2)."
    findings.append({"area": "Compliance Activity", "rule": "MiFID II Art.16(2)",
                     "description": "Review of compliance arrangements", "status": s, "commentary": c})

    outstanding = data.get("outstanding_coof_recommendations")
    if outstanding:
        rec_count = len(outstanding) if isinstance(outstanding, list) else int(outstanding)
        findings.append({"area": "Outstanding Items", "rule": "MiFID II / ESMA",
                         "description": "Outstanding compliance recommendations",
                         "status": "RED",
                         "commentary": f"{rec_count} outstanding recommendation(s) with no confirmed action plan."})
    else:
        findings.append({"area": "Outstanding Items", "rule": "MiFID II / ESMA",
                         "description": "Outstanding compliance recommendations",
                         "status": "GREEN", "commentary": "No outstanding compliance recommendations."})

    return findings


def score_africa_oversight(data: dict) -> list:
    findings = []

    named = data.get("coof_individual_name") or data.get("compliance_officer_named")
    findings.append({
        "area": "Compliance Officer", "rule": "FAIS Act / FSCA Guidance / CBN / CMA",
        "description": "Compliance officer designated",
        "status": "GREEN" if named else "RED",
        "commentary": f"Compliance officer designated: {named}." if named
            else "No compliance officer designated. FAIS Act and FSCA guidance require a named compliance officer.",
    })

    qualified = data.get("coof_individual_qualified")
    findings.append({
        "area": "Qualifications", "rule": "FSCA / CBN / CMA",
        "description": "Compliance officer qualifications verified",
        "status": "GREEN" if qualified else "AMBER",
        "commentary": "Qualifications confirmed." if qualified
            else "Qualifications not confirmed. FSCA requires appropriate compliance expertise.",
    })

    dual = data.get("coof_also_compliance_officer")
    findings.append({
        "area": "Independence", "rule": "FSCA / Local Reg.",
        "description": "Compliance function independence",
        "status": "AMBER" if dual else "GREEN",
        "commentary": "Independence concern." if dual else "Compliance function operates independently.",
    })

    last_report = data.get("last_coof_report_to_board_date")
    if last_report:
        try:
            days = (date.today() - datetime.strptime(last_report, "%Y-%m-%d").date()).days
            s = "GREEN" if days <= 365 else "RED"
            c = f"Annual compliance report delivered {last_report} ({days} days ago)." + (" OVERDUE." if s == "RED" else "")
        except Exception:
            s, c = "AMBER", "Report date unreadable."
    else:
        s, c = "RED", "No annual compliance report on record. FSCA requires annual compliance reporting to board."
    findings.append({"area": "Annual Report", "rule": "FSCA / CBN / CMA",
                     "description": "Annual compliance report to board", "status": s, "commentary": c})

    last_review = data.get("last_coof_review_of_cass_date")
    if last_review:
        try:
            days = (date.today() - datetime.strptime(last_review, "%Y-%m-%d").date()).days
            s = "GREEN" if days <= 365 else "AMBER"
            c = f"Last compliance review: {last_review} ({days} days ago)."
        except Exception:
            s, c = "AMBER", "Review date unreadable."
    else:
        s, c = "AMBER", "No review date on record. Regular compliance reviews expected by FSCA."
    findings.append({"area": "Compliance Activity", "rule": "FSCA / Local Reg.",
                     "description": "Review of compliance arrangements", "status": s, "commentary": c})

    outstanding = data.get("outstanding_coof_recommendations")
    if outstanding:
        rec_count = len(outstanding) if isinstance(outstanding, list) else int(outstanding)
        findings.append({"area": "Outstanding Items", "rule": "FSCA / CBN / CMA",
                         "description": "Outstanding compliance recommendations",
                         "status": "RED",
                         "commentary": f"{rec_count} outstanding recommendation(s) with no confirmed action plan."})
    else:
        findings.append({"area": "Outstanding Items", "rule": "FSCA / CBN / CMA",
                         "description": "Outstanding compliance recommendations",
                         "status": "GREEN", "commentary": "No outstanding compliance recommendations."})

    return findings


def score_regional_oversight(data: dict, region: str) -> list:
    dispatch = {
        "N. America":    score_us_oversight,
        "Latin America": score_latam_oversight,
        "Asia Pacific":  score_apac_oversight,
        "Europe":        score_europe_oversight,
        "Africa":        score_africa_oversight,
    }
    fn = dispatch.get(region)
    return fn(data) if fn else []
