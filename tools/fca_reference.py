"""
FCA Regulatory Reference Database
Sourced from: https://www.handbook.fca.org.uk + FCA enforcement notices + financial press
Updated: October 2026
Covers: CASS 1/1A/6/7/7A/10/15 | SM&CR | PS21/3 | PS26/2 | Consumer Duty | OFSI | CBEST
"""

from datetime import date

SOURCED_DATE = "2026-10-07"

# =============================================================================
# FCA NEWS — live regulatory items as of October 2026
# =============================================================================
FCA_NEWS = [
    # ----- CASS ---------------------------------------------------------------
    {
        "date": "25/09/2026",
        "type": "Handbook Update",
        "headline": "CASS 6 & 7 updated — Consumer Duty retail client obligations now live",
        "detail": (
            "CASS 7.11.32 R updated: firms MUST pay interest to retail clients on client money "
            "unless non-payment is compatible with the Consumer Duty (FCA Consumer Duty Outcome 2). "
            "CASS 6.3.2A R added: firms must record grounds for selecting each third-party custodian. "
            "CASS 6.4.1BA R added: retail client TTCA consent alone no longer sufficient — Consumer Duty applies."
        ),
        "tags": ["CASS 6", "CASS 7", "Consumer Duty", "Retail"],
        "severity": "RED",
        "report_types": ["cass_health_check", "client_money_segregation", "cass_oversight"],
    },
    {
        "date": "26/06/2026",
        "type": "Handbook Notice",
        "headline": "Handbook Notice 142 — targeted CASS 6 & 7 reforms effective",
        "detail": (
            "FCA published Handbook Notice 142 (effective 26 June 2026): CASS 6 external custody "
            "reconciliation rules broadened to allow use of specified third-party records. "
            "Due diligence record-keeping requirements simplified. CASS 7 interest treatment clarified "
            "for unallocated client money. Changes reduce administrative burden without weakening protection."
        ),
        "tags": ["CASS 6", "CASS 7", "Handbook Notice 142", "Reconciliation"],
        "severity": "AMBER",
        "report_types": ["cass_health_check", "client_money_segregation", "cass_resolution_pack"],
    },
    {
        "date": "07/05/2026",
        "type": "New Regime",
        "headline": "CASS 15 live — payment and e-money firm safeguarding overhaul",
        "detail": (
            "CASS 15 came into force 7 May 2026 (PS25/12), replacing previous safeguarding rules for "
            "authorised payment institutions, authorised e-money institutions, and small e-money institutions. "
            "New obligations: daily reconciliations, monthly safeguarding returns to FCA, mandatory "
            "safeguarding audits, enhanced due diligence on banks holding safeguarded funds."
        ),
        "tags": ["CASS 15", "Payment Services", "E-Money", "Safeguarding"],
        "severity": "AMBER",
        "report_types": ["cass_health_check", "client_money_segregation"],
    },
    {
        "date": "25/09/2026",
        "type": "Special Administration",
        "headline": "ITI Capital Ltd enters special administration — CASS 10 activated",
        "detail": (
            "FCA-regulated investment firm ITI Capital Ltd entered special administration. "
            "CASS resolution pack and client asset return procedures activated under CASS 10. "
            "Highlights importance of 48-hour retrieval requirement (CASS 10.1.7 R) and resolution "
            "pack completeness for all medium/large CASS firms."
        ),
        "tags": ["CASS 10", "Special Administration", "Resolution Pack"],
        "severity": "RED",
        "report_types": ["cass_resolution_pack"],
    },
    {
        "date": "30/09/2026",
        "type": "Regulatory Gateway",
        "headline": "FCA opens crypto authorisation gateway — CASS 6 custody rules will apply",
        "detail": (
            "FCA opened authorisation gateway for crypto asset service providers. "
            "CASS 6 custody rules will apply to regulated crypto assets held for retail clients. "
            "Firms must ensure segregation, reconciliation, and resolution pack arrangements "
            "cover digital assets by the transition deadline."
        ),
        "tags": ["Crypto", "CASS 6", "Custody"],
        "severity": "AMBER",
        "report_types": ["cass_health_check", "cass_resolution_pack"],
    },
    # ----- Enforcement (CASS) -------------------------------------------------
    {
        "date": "2025",
        "type": "Enforcement — Fine",
        "headline": "Aviva fined £8.2m — first CASS outsourcing oversight case",
        "detail": (
            "FCA fined Aviva Pension Trustees UK Ltd and Aviva Wrap UK Ltd £8.2m "
            "(reduced from £11.8m for early settlement). Breaches: CASS Sourcebook, Principle 3 "
            "(adequate management), Principle 10 (client assets). Core failure: outsourced CASS "
            "administration to Third Party Administrators but failed to maintain adequate controls. "
            "Client money peaked £74.4m under-segregated. Inaccurate CMAR submissions filed. "
            "FCA message: 'regulated activities can be delegated but not abdicated.'"
        ),
        "tags": ["Enforcement", "CASS", "Outsourcing", "Principle 3", "Principle 10"],
        "severity": "RED",
        "report_types": ["cass_health_check", "client_money_segregation", "cass_oversight", "cass_breach_log"],
    },
    {
        "date": "2015",
        "type": "Enforcement — Fine (Historical)",
        "headline": "BNY Mellon fined £126m — largest custody CASS fine on record",
        "detail": (
            "FCA fined Bank of New York Mellon London Branch and BNY Mellon International Ltd "
            "£126m (largest CASS custody fine ever). Period: 1 Nov 2007 to 12 Aug 2013. "
            "Safe custody asset balances: ~£1.3 trillion (London) and £236bn (International). "
            "Key breaches: used global platforms failing to record which BNY entity clients had "
            "contracted; settled other clients' transactions from omnibus accounts without consent. "
            "No client losses but structural risk was systemic."
        ),
        "tags": ["Enforcement", "CASS 6", "Custody", "BNY Mellon"],
        "severity": "RED",
        "report_types": ["cass_health_check", "client_money_segregation", "cass_resolution_pack"],
    },
    # ----- SM&CR / Executive --------------------------------------------------
    {
        "date": "24/04/2026",
        "type": "Regulatory Reform",
        "headline": "SM&CR Phase 1 reforms live — prescribed responsibilities and certification changes",
        "detail": (
            "FCA and PRA confirmed Phase 1 SM&CR reforms effective 24 April 2026 (further changes "
            "10 July 2026). Key changes: SMF18 holders at solo-regulated firms may now hold any "
            "FCA-prescribed senior management responsibility from 10 July 2026. "
            "Certification regime simplified — ~15% reduction in certification role count. "
            "Enhanced firm financial thresholds increased 30% (inflation adjustment since 2019). "
            "Firms have up to 6 months to notify SoR/MRM changes following significant responsibility shifts. "
            "Non-financial misconduct changes aligned with COCON — effective 1 September 2026."
        ),
        "tags": ["SM&CR", "Prescribed Responsibilities", "Certification Regime", "COCON"],
        "severity": "AMBER",
        "report_types": ["executive_protection", "cass_oversight"],
    },
    {
        "date": "01/09/2026",
        "type": "New Rule",
        "headline": "Non-financial misconduct now in scope of COCON — 37,000 firms affected",
        "detail": (
            "FCA extended COCON to capture serious non-financial misconduct (NFM) in all SM&CR firms "
            "(not just banks) from 1 September 2026. New rule COCON 1.1.7FR in force. "
            "Covers: bullying, harassment (including sexual harassment), violence where connected to "
            "firm's financial services business. Applies when either the individual responsible for, "
            "or the subject of, the misconduct works within the firm's financial services business. "
            "FIT test updated — NFM may now affect fitness and propriety assessments."
        ),
        "tags": ["SM&CR", "COCON", "Non-financial misconduct", "Fit and Proper", "COCON 1.1.7FR"],
        "severity": "AMBER",
        "report_types": ["executive_protection", "due_diligence"],
    },
    {
        "date": "13/03/2026",
        "type": "Enforcement — Ban",
        "headline": "CEO Kasim Garipoglu banned — AML disregard and misleading FCA",
        "detail": (
            "FCA banned Kasim Garipoglu (CEO/Director) on 13 March 2026: not fit and proper "
            "due to lack of honesty and integrity. Misconduct: encouraged excessive compliance "
            "risk-taking, disregarded AML and regulatory obligations, misleading and undermining "
            "compliance personnel, and deliberately providing false information to the FCA. "
            "Demonstrates FCA's willingness to pursue individual SMF holders personally."
        ),
        "tags": ["SM&CR", "Ban", "AML", "Integrity", "Fit and Proper"],
        "severity": "RED",
        "report_types": ["executive_protection", "due_diligence"],
    },
    {
        "date": "12/01/2026",
        "type": "Enforcement — Ban and Fine",
        "headline": "Darren Reynolds banned and fined £2m — £1m prohibited commission scheme",
        "detail": (
            "FCA fined Darren Antony Reynolds £2,037,892 and banned him from industry. "
            "Held CF1 (Director) and CF10 (Compliance Oversight) roles at Active Wealth (UK) Ltd. "
            "Dishonestly arranged for himself and other advisers to receive £1m+ in prohibited "
            "commission payments routed through connected companies to disguise origins. "
            "Breached Statement of Principle 1 (integrity)."
        ),
        "tags": ["SM&CR", "Ban", "Compliance Officer", "Prohibited Payments", "Integrity"],
        "severity": "RED",
        "report_types": ["executive_protection", "cass_oversight"],
    },
    {
        "date": "30/09/2026",
        "type": "Enforcement — Fine",
        "headline": "Robin Odey fined £1.5m — integrity failure in asset management",
        "detail": (
            "FCA fined Robin Crispin William Odey £1,529,374 for breaching COCON 2.2.1R (integrity). "
            "Odey Capital Group founder. Case relates to asset management conduct failures. "
            "Underscores that senior individuals in asset management face direct FCA accountability "
            "under SM&CR personal conduct rules."
        ),
        "tags": ["SM&CR", "COCON", "Asset Management", "Fine", "Integrity"],
        "severity": "RED",
        "report_types": ["executive_protection", "threat_intelligence"],
    },
    # ----- Financial Crime / AML / Threat Intelligence -----------------------
    {
        "date": "2025",
        "type": "Enforcement — Fine",
        "headline": "Nationwide fined £44m — financial crime systems and controls failure",
        "detail": (
            "FCA fined Nationwide Building Society £44,078,500 for breaches of Principle 3 and "
            "associated breaches of SYSC 6.1.1R and SYSC 6.3.1R related to financial crime controls. "
            "Serious weaknesses in CDD and transaction monitoring systems. "
            "Failure to identify and assess financial crime risks in account opening procedures."
        ),
        "tags": ["Principle 3", "SYSC", "Financial Crime", "CDD", "AML"],
        "severity": "RED",
        "report_types": ["threat_intelligence", "due_diligence"],
    },
    {
        "date": "2025",
        "type": "Enforcement — Fine",
        "headline": "Barclays fined £39m — money laundering risk management failures",
        "detail": (
            "FCA fined Barclays Bank plc £39,314,700 for breaching Principle 2 (due skill, care, "
            "diligence) regarding money laundering risk management failures spanning Jan 2015–Apr 2021. "
            "Inadequate customer risk assessment and monitoring controls. "
            "Part of wider FCA campaign targeting financial crime enablement."
        ),
        "tags": ["AML", "Principle 2", "Money Laundering", "Financial Crime"],
        "severity": "RED",
        "report_types": ["threat_intelligence", "due_diligence"],
    },
    {
        "date": "2025",
        "type": "Enforcement — Fine",
        "headline": "Monzo fined £21m — financial crime controls failure during rapid growth",
        "detail": (
            "FCA fined Monzo Bank Limited £21,091,300 for breaching Principle 3 and FSMA s.55L. "
            "Inadequate financial crime controls during period of rapid customer growth. "
            "Repeated breaches of an FCA restriction on higher-risk onboarding. "
            "Highlights risk of operational controls failing to keep pace with business growth."
        ),
        "tags": ["Financial Crime", "Principle 3", "Onboarding", "CDD"],
        "severity": "RED",
        "report_types": ["threat_intelligence", "due_diligence"],
    },
    {
        "date": "08/04/2026",
        "type": "Supervisory Finding",
        "headline": "FCA multi-firm CDD review — widespread poor practice found",
        "detail": (
            "FCA published findings from its 2025 multi-firm review of customer due diligence (CDD), "
            "enhanced due diligence (EDD), and ongoing monitoring controls (April 2026). "
            "Poor practice found: policies lack practical guidance for staff; unclear periodic/event-driven "
            "review triggers; weak version control; failures to evidence EDD steps actually taken; "
            "no details on purpose/intended nature of business relationship; no scenarios requiring "
            "senior management approval. FCA put all firms on notice — supervisory action expected."
        ),
        "tags": ["CDD", "EDD", "AML", "Monitoring", "Financial Crime"],
        "severity": "AMBER",
        "report_types": ["due_diligence", "threat_intelligence"],
    },
    # ----- Cyber / Operational Resilience ------------------------------------
    {
        "date": "18/03/2026",
        "type": "Policy Statement",
        "headline": "PS26/2 published — new operational incident and third-party reporting framework",
        "detail": (
            "FCA, PRA and Bank of England published PS26/2 on 18 March 2026. "
            "New framework in force 18 March 2027. Key obligations: "
            "(1) Firms must report operational incidents to FCA within 24 hours of determining a threshold "
            "is met (PSPs within 4 hours of first detection). "
            "(2) Thresholds: risk of intolerable consumer harm; threat to firm safety/soundness; "
            "risk to market stability/integrity. "
            "(3) Annual register of all material third-party arrangements. "
            "(4) Notify FCA of new/significant-change material third-party arrangements. "
            "Scope: all Part 4A FSMA firms, PSPs, RIEs, trade repositories, credit rating agencies."
        ),
        "tags": ["PS26/2", "Operational Incidents", "Third Parties", "Reporting", "SYSC"],
        "severity": "RED",
        "report_types": ["fca_incident_response", "cyber_threat_assessment"],
    },
    {
        "date": "13/07/2026",
        "type": "New Regime",
        "headline": "Critical Third Parties regime live — FCA/PRA/BoE oversee major cloud and tech providers",
        "detail": (
            "From 13 July 2026, the FCA, PRA and Bank of England began overseeing the first "
            "HM Treasury-designated Critical Third Parties (CTPs), including major cloud and "
            "technology providers whose disruption could have system-wide effects. "
            "Firms using CTPs must now: maintain updated third-party registers; assess CTP resilience; "
            "participate in CTP-led scenario testing. "
            "82% of respondents in the BoE 2026 H1 Systemic Risk Survey cited cyber-attack as "
            "a top-5 risk to the UK financial system."
        ),
        "tags": ["Critical Third Parties", "CTP", "Operational Resilience", "Cloud", "PS26/2"],
        "severity": "AMBER",
        "report_types": ["cyber_threat_assessment", "fca_incident_response"],
    },
    {
        "date": "2025",
        "type": "Supervisory Finding",
        "headline": "PS21/3 deadline passed — FCA finds widespread operational resilience gaps",
        "detail": (
            "March 2025 PS21/3 operational resilience deadline has passed. FCA published observations: "
            "firms incorrectly excluded Important Business Services based on single factors (e.g. competitor "
            "substitutability alone). Impact tolerances narrowly set on time-only metrics — no transaction "
            "value, client type, or volume thresholds used. Scenario testing predominantly desk-based and "
            "theoretical — FCA expects penetration tests, DR exercises, simulations. Firms focused on "
            "recovery but neglected tactical response measures. Third-party resilience accepted without "
            "verifying methodology. Enforcement risk now elevated for non-compliant firms."
        ),
        "tags": ["PS21/3", "Operational Resilience", "Impact Tolerances", "Scenario Testing"],
        "severity": "RED",
        "report_types": ["cyber_threat_assessment", "fca_incident_response"],
    },
    {
        "date": "October 2025",
        "type": "Enforcement — Fine",
        "headline": "ICO fines Capita £14m — security failures and breach response gaps",
        "detail": (
            "UK Information Commissioner's Office (ICO) fined Capita £14m in October 2025 for failures "
            "in security measures and breach response capability. Capita is a major outsourcing firm "
            "providing services to FCA-regulated firms. "
            "The case underscores that regulated firms bear accountability for the security standards "
            "of their material third-party providers under both UK GDPR and FCA SYSC requirements. "
            "Firms using Capita services should review their third-party due diligence records."
        ),
        "tags": ["ICO", "Data Breach", "Outsourcing", "Third Party", "Cyber", "UK GDPR"],
        "severity": "RED",
        "report_types": ["cyber_threat_assessment", "physical_security_audit", "due_diligence"],
    },
    {
        "date": "September 2026",
        "type": "Cyber Incident",
        "headline": "Revolut exposes customer data via fraudulent government agency request",
        "detail": (
            "Revolut disclosed in September 2026 that it provided customer data to an unauthorised "
            "third party after receiving fraudulent requests mimicking a legitimate government agency "
            "email domain. Exposed data: identity documents, dates of birth, postal/email addresses, "
            "phone numbers, passport and driver's licence copies. "
            "Regulators reviewing whether adequate technical and organisational security measures "
            "were in place under UK GDPR and FCA SYSC 7 (security and information risk). "
            "PS26/2 reporting obligations would apply to equivalent incidents from March 2027."
        ),
        "tags": ["Cyber", "Data Breach", "Social Engineering", "UK GDPR", "SYSC 7"],
        "severity": "RED",
        "report_types": ["cyber_threat_assessment", "physical_security_audit", "fca_incident_response"],
    },
    {
        "date": "November 2025",
        "type": "Cyber Incident",
        "headline": "Habib Bank hit by Qilin ransomware — UK regulated entity affected",
        "detail": (
            "Habib Bank (operating in UK, Switzerland, UAE, Hong Kong, Kenya, South Africa, Canada) "
            "was targeted by Qilin ransomware group in November 2025. Bank has not confirmed breach "
            "details or client impact. Ransomware attacks on regulated entities trigger FCA SYSC "
            "operational risk requirements and, from March 2027, PS26/2 reporting obligations. "
            "Average cost of a data breach in the financial sector reached $5.56 million in 2025 "
            "(second only to healthcare globally)."
        ),
        "tags": ["Ransomware", "Cyber", "Operational Risk", "SYSC"],
        "severity": "RED",
        "report_types": ["cyber_threat_assessment", "physical_security_audit"],
    },
    # ----- Sanctions / Country Risk -------------------------------------------
    {
        "date": "11/08/2026",
        "type": "Enforcement — OFSI Fine",
        "headline": "Citibank London fined £4.7m for Russia sanctions breach",
        "detail": (
            "OFSI imposed a penalty of £4,732,830.58 on Citibank, N.A. London Branch on 11 August 2026 "
            "for breaches of the Russia (Sanctions) (EU Exit) Regulations 2019. "
            "This is among the largest UK financial sanctions penalties to date. "
            "Demonstrates heightened OFSI enforcement against major financial institutions "
            "for Russia-related sanctions breaches."
        ),
        "tags": ["OFSI", "Russia Sanctions", "Enforcement", "Citibank"],
        "severity": "RED",
        "report_types": ["country_risk", "threat_intelligence"],
    },
    {
        "date": "31/07/2025",
        "type": "Enforcement — OFSI Fine",
        "headline": "Markom Management fined £300k for routing £416k to designated Russia-linked individual",
        "detail": (
            "OFSI fined Markom Management Limited £300,000 on 31 July 2025 for breaching Russia-related "
            "sanctions by instructing a payment of £416,590.92 to a designated individual. "
            "OFSI has 318 open investigations into potential UK Russia sanctions breaches in 2025."
        ),
        "tags": ["OFSI", "Russia Sanctions", "Enforcement", "Designated Person"],
        "severity": "RED",
        "report_types": ["country_risk", "due_diligence"],
    },
    {
        "date": "31/08/2026",
        "type": "Regulatory Change",
        "headline": "OFSI maximum penalty doubled — from 50% to 100% of sanctions breach value",
        "detail": (
            "UK Chancellor of the Exchequer announced on 31 August 2026 that OFSI maximum fine "
            "will double from 50% to 100% of the value of a sanctions breach. "
            "This dramatically increases the financial risk for firms that fail to screen clients, "
            "counterparties, and payments against UK consolidated list. "
            "318 open OFSI investigations underway as of 2025. Also: OFSI fined Sabre Global "
            "Technologies Ltd £1,000,920.59 for Russia sanctions breach via software licensing."
        ),
        "tags": ["OFSI", "Russia Sanctions", "Penalty Cap", "Enforcement"],
        "severity": "RED",
        "report_types": ["country_risk", "threat_intelligence", "due_diligence"],
    },
    {
        "date": "2026",
        "type": "Regulatory Update",
        "headline": "Iran sanctions expanded — new UK financial, trade and transport restrictions",
        "detail": (
            "UK introduced new regulations imposing additional financial, trade and transport "
            "restrictions related to Iran sanctions regime in 2026. "
            "Firms with exposures to Iran-connected entities, transactions, or counterparties must "
            "urgently review and update their screening and risk assessment frameworks. "
            "Affects trade finance, correspondent banking, and cross-border payments."
        ),
        "tags": ["OFSI", "Iran Sanctions", "Trade Finance", "Correspondent Banking"],
        "severity": "AMBER",
        "report_types": ["country_risk", "threat_intelligence"],
    },
    # ----- Due Diligence / Non-Financial Misconduct ----------------------------
    {
        "date": "July 2026",
        "type": "Supervisory Finding",
        "headline": "FCA asset management financial crime review — controls widely inadequate",
        "detail": (
            "FCA published findings from its review of asset management and alternative firms' "
            "financial crime controls in July 2026. Widespread inadequacies found: "
            "CDD policies lack practical staff guidance; EDD triggers unclear or absent; "
            "no evidence of what EDD measures were actually taken; "
            "senior management approval thresholds undefined in policy; version control failures. "
            "FCA stated it will use supervisory and enforcement powers where firms fail to address gaps."
        ),
        "tags": ["Asset Management", "Financial Crime", "CDD", "EDD", "AML"],
        "severity": "RED",
        "report_types": ["due_diligence", "threat_intelligence"],
    },
    # ----- Physical Security --------------------------------------------------
    {
        "date": "20/07/2026",
        "type": "Cyber/Data Incident",
        "headline": "Craneware (financial software) discloses unauthorised data access — LSE notified",
        "detail": (
            "Edinburgh-based healthcare financial software firm Craneware disclosed a cybersecurity "
            "incident to the London Stock Exchange on 20 July 2026, reporting unauthorised access "
            "to a subset of its data environment. Incident contained; external forensic specialists "
            "appointed; ICO and FBI notified. Case demonstrates that financial software supply chain "
            "vulnerabilities create indirect risk for regulated client firms. "
            "Firms using financial software vendors must include them in third-party risk assessments."
        ),
        "tags": ["Supply Chain", "Data Breach", "Third Party", "LSE"],
        "severity": "AMBER",
        "report_types": ["physical_security_audit", "cyber_threat_assessment"],
    },
]

# =============================================================================
# CASS RULE REFERENCE DATABASE
# =============================================================================
CASS_RULES = {

    # ── CASS 1 / 1A ─────────────────────────────────────────────────────────
    "CASS 1.1.1 R": {
        "chapter": "CASS 1",
        "title": "Application — firms covered",
        "last_updated": "07/05/2026",
        "obligation": "Applies to firms, electronic money institutions and payment institutions.",
        "new": True,
    },
    "CASS 1.2.2A R": {
        "chapter": "CASS 1",
        "title": "Payment/e-money institution segregation",
        "last_updated": "07/05/2026",
        "obligation": "Payment institutions and e-money firms must not keep client money in the same account as firm money.",
        "new": True,
    },
    "CASS 1A.2.7 R": {
        "chapter": "CASS 1A",
        "title": "CASS firm classification thresholds",
        "last_updated": "01/04/2019",
        "obligation": "Large: >£1bn client money or >£100bn custody. Medium: £1m–£1bn / £10m–£100bn. Small: <£1m / <£10m.",
    },
    "CASS 1A.2.9 R": {
        "chapter": "CASS 1A",
        "title": "Annual FCA classification notification",
        "last_updated": "01/04/2019",
        "obligation": "Notify FCA by 15th business day of January: highest client money held, highest custody value, CASS firm type.",
    },
    "CASS 1A.3.1A R": {
        "chapter": "CASS 1A",
        "title": "COOF — medium and large firm oversight function",
        "last_updated": "09/12/2019",
        "obligation": "Medium/large firms must allocate CASS operational oversight to a single director or senior manager.",
    },

    # ── CASS 6 ───────────────────────────────────────────────────────────────
    "CASS 6.2.1 R": {
        "chapter": "CASS 6",
        "title": "Safeguarding client assets",
        "last_updated": "03/01/2018",
        "obligation": "Adequate arrangements to safeguard ownership rights, especially in event of insolvency.",
    },
    "CASS 6.2.3 R": {
        "chapter": "CASS 6",
        "title": "Registration of legal title",
        "last_updated": "23/05/2025",
        "obligation": "Client assets must be registered in client name or nominee name, not firm name.",
    },
    "CASS 6.3.1 R": {
        "chapter": "CASS 6",
        "title": "Third-party custodian due diligence",
        "last_updated": "03/01/2018",
        "obligation": "Exercise due diligence in selecting, appointing and reviewing third-party custodians.",
    },
    "CASS 6.3.2A R": {
        "chapter": "CASS 6",
        "title": "Third-party selection — record grounds",
        "last_updated": "25/09/2026",
        "obligation": "Firms must record their grounds for selecting each third-party custodian.",
        "new": True,
    },
    "CASS 6.4.1 R": {
        "chapter": "CASS 6",
        "title": "Use of client assets — non-retail",
        "last_updated": "25/09/2026",
        "obligation": "Non-retail clients: express prior written consent required before using client assets.",
    },
    "CASS 6.4.1BA R": {
        "chapter": "CASS 6",
        "title": "Use of client assets — retail (Consumer Duty)",
        "last_updated": "25/09/2026",
        "obligation": "Retail clients: consent required AND non-use must be compatible with Consumer Duty.",
        "new": True,
    },
    "CASS 6.6.2 R": {
        "chapter": "CASS 6",
        "title": "Asset segregation record keeping",
        "last_updated": "03/01/2018",
        "obligation": "Distinguish client assets from firm assets at all times. Five-year retention.",
    },
    "CASS 6.6.4 R": {
        "chapter": "CASS 6",
        "title": "External custody reconciliation — third-party records",
        "last_updated": "26/06/2026",
        "obligation": (
            "External custody reconciliation required at least every 25 business days. "
            "Handbook Notice 142 (June 2026): firms may now use specified third-party records "
            "where appropriate conditions are met, reducing administrative burden."
        ),
        "new": True,
    },

    # ── CASS 7 ───────────────────────────────────────────────────────────────
    "CASS 7.11.1 R": {
        "chapter": "CASS 7",
        "title": "TTCA restriction — retail clients",
        "last_updated": "03/01/2018",
        "obligation": "Firms must NOT enter into a Title Transfer Collateral Arrangement (TTCA) for retail client money.",
    },
    "CASS 7.11.32 R": {
        "chapter": "CASS 7",
        "title": "Interest on client money — retail",
        "last_updated": "25/09/2026",
        "obligation": (
            "Firms MUST pay a retail client any interest earned on client money held for that client, "
            "unless non-payment is notified in writing AND is compatible with the Consumer Duty."
        ),
        "new": True,
    },
    "CASS 7.11.34 R": {
        "chapter": "CASS 7",
        "title": "Discharge of fiduciary duty",
        "last_updated": "02/08/2024",
        "obligation": (
            "Lists nine circumstances where money ceases to be client money, "
            "including regulated clearing transfers and dormant asset fund transfers."
        ),
    },
    "CASS 7.13.4 R": {
        "chapter": "CASS 7",
        "title": "Depositing client money",
        "last_updated": "03/01/2018",
        "obligation": "Client money must be deposited in client bank accounts with approved credit institutions.",
    },
    "CASS 7.13.12 R": {
        "chapter": "CASS 7",
        "title": "Client bank accounts",
        "last_updated": "03/01/2018",
        "obligation": "Client bank accounts must bear the term 'client' in their title/designation.",
    },
    "CASS 7.13.20 R": {
        "chapter": "CASS 7",
        "title": "Diversification of client money",
        "last_updated": "03/01/2018",
        "obligation": "CASS large/medium firms: must diversify client money across at least two institutions unless justified.",
    },
    "CASS 7.15.20 R": {
        "chapter": "CASS 7",
        "title": "External client money reconciliation",
        "last_updated": "03/01/2018",
        "obligation": "External reconciliation of client money records against third-party statements required.",
    },
    "CASS 7.15.29 R": {
        "chapter": "CASS 7",
        "title": "Reconciliation discrepancies",
        "last_updated": "03/01/2018",
        "obligation": "Discrepancies must be investigated and resolved promptly; shortfalls must be paid in immediately.",
    },
    "CASS 7.16 R": {
        "chapter": "CASS 7",
        "title": "Standard internal reconciliation method",
        "last_updated": "03/01/2018",
        "obligation": "Standard method: sum individual client ledger balances = total client money held.",
    },

    # ── CASS 10 ──────────────────────────────────────────────────────────────
    "CASS 10.1.3 R": {
        "chapter": "CASS 10",
        "title": "Resolution pack — maintain and retrieve",
        "last_updated": "01/01/2021",
        "obligation": "Firms must maintain a CASS resolution pack and be able to retrieve it on demand.",
    },
    "CASS 10.1.7 R": {
        "chapter": "CASS 10",
        "title": "Resolution pack retrieval — 48 hours",
        "last_updated": "03/01/2018",
        "obligation": "Resolution pack documents must be retrievable within 48 hours by administrators or on FCA request.",
    },
    "CASS 10.1.11 R": {
        "chapter": "CASS 10",
        "title": "Material inaccuracy correction",
        "last_updated": "03/01/2018",
        "obligation": "Material inaccuracies in the resolution pack must be corrected within 5 business days.",
    },
    "CASS 10.1.14 R": {
        "chapter": "CASS 10",
        "title": "Annual governing body report",
        "last_updated": "03/01/2018",
        "obligation": "CASS oversight individual must report annually to governing body on resolution pack status.",
    },
    "CASS 10.1.16 R": {
        "chapter": "CASS 10",
        "title": "Non-compliance notification",
        "last_updated": "03/01/2018",
        "obligation": "Immediate written notice to FCA if firm is unable to comply with resolution pack requirements.",
    },
    "CASS 10.2.1 R": {
        "chapter": "CASS 10",
        "title": "Core resolution pack content",
        "last_updated": "01/01/2021",
        "obligation": "Must include: master document, appointed institutions, agents, key personnel, third-party agreements, operational procedures.",
    },

    # ── CASS 15 (new 2026) ───────────────────────────────────────────────────
    "CASS 15.1 R": {
        "chapter": "CASS 15",
        "title": "Safeguarding scope — payment and e-money firms",
        "last_updated": "07/05/2026",
        "obligation": (
            "Applies to authorised payment institutions, authorised e-money institutions, "
            "small e-money institutions, and credit unions issuing e-money."
        ),
        "new": True,
    },
    "CASS 15.2 R": {
        "chapter": "CASS 15",
        "title": "Daily reconciliation — payment/e-money safeguarding",
        "last_updated": "07/05/2026",
        "obligation": "Daily reconciliation of safeguarded funds required (replaces previous periodic checks under PSRs/EMRs).",
        "new": True,
    },
    "CASS 15.3 R": {
        "chapter": "CASS 15",
        "title": "Monthly safeguarding returns",
        "last_updated": "07/05/2026",
        "obligation": "Firms must submit a monthly safeguarding return to FCA providing overview of safeguarded funds and controls.",
        "new": True,
    },
    "CASS 15.4 R": {
        "chapter": "CASS 15",
        "title": "Mandatory safeguarding audits",
        "last_updated": "07/05/2026",
        "obligation": "Annual mandatory safeguarding audit required. Enhanced due diligence on banks holding safeguarded funds.",
        "new": True,
    },
}

# =============================================================================
# CONSUMER DUTY x CASS OBLIGATIONS (effective 25 September 2026)
# =============================================================================
CONSUMER_DUTY_CASS = [
    {
        "rule": "CASS 7.11.32 R",
        "area": "Client Money Interest",
        "obligation": "Pay retail clients interest on client money held.",
        "unless": "Non-payment notified in writing AND compatible with Consumer Duty.",
        "effective": "25/09/2026",
        "risk": "Failure = potential breach of Consumer Duty + CASS 7 breach",
    },
    {
        "rule": "CASS 6.4.1BA R",
        "area": "Use of Client Assets — TTCA",
        "obligation": "Retail client consent required; non-use must be Consumer Duty compatible.",
        "effective": "25/09/2026",
        "risk": "Using retail client assets without Consumer Duty review = dual regulatory breach",
    },
    {
        "rule": "CASS 6.3.2A R",
        "area": "Third-Party Custodian Selection",
        "obligation": "Document grounds for selecting each third-party custodian.",
        "effective": "25/09/2026",
        "risk": "Undocumented selection = CASS 6 breach",
    },
]

# =============================================================================
# ENFORCEMENT CASES — mapped by report type for report generation context
# =============================================================================
ENFORCEMENT_CASES = {

    "cass_health_check": [
        {
            "firm": "Aviva Pension Trustees UK Ltd / Aviva Wrap UK Ltd",
            "fine": "GBP 8,200,000",
            "rules": ["CASS Sourcebook", "Principle 3", "Principle 10"],
            "year": 2025,
            "summary": (
                "Outsourced CASS administration but failed to maintain adequate oversight controls. "
                "Client money peaked at GBP 74.4m under-segregated. Inaccurate CMARs filed. "
                "FCA: 'regulated activities can be delegated but not abdicated.'"
            ),
        },
        {
            "firm": "Bank of New York Mellon (London Branch & International)",
            "fine": "GBP 126,000,000",
            "rules": ["CASS 6 (Custody Rules)"],
            "year": 2015,
            "summary": (
                "Largest ever CASS custody fine. Used global platforms that failed to record which BNY entity "
                "clients had contracted with. Settled other clients' transactions from omnibus accounts "
                "without consent. Assets involved: ~GBP 1.3 trillion."
            ),
        },
    ],

    "client_money_segregation": [
        {
            "firm": "Aviva Pension Trustees UK Ltd",
            "fine": "GBP 8,200,000",
            "rules": ["CASS 7", "Principle 10"],
            "year": 2025,
            "summary": "Under-segregation of client money peaked at GBP 74.4m. Outsourcing controls inadequate.",
        },
    ],

    "cass_resolution_pack": [
        {
            "firm": "ITI Capital Ltd",
            "fine": "N/A (special administration)",
            "rules": ["CASS 10"],
            "year": 2026,
            "summary": (
                "Entered special administration September 2026. CASS 10 resolution pack and client asset "
                "return procedures activated. Real-world test of 48-hour pack retrieval requirement."
            ),
        },
    ],

    "cass_oversight": [
        {
            "firm": "Aviva",
            "fine": "GBP 8,200,000",
            "rules": ["Principle 3", "CASS"],
            "year": 2025,
            "summary": "COOF failure: senior management delegated CASS oversight to TPA without maintaining control.",
        },
        {
            "firm": "Darren Reynolds (Compliance Oversight CF10)",
            "fine": "GBP 2,037,892 + industry ban",
            "rules": ["Statement of Principle 1", "SM&CR"],
            "year": 2026,
            "summary": "Compliance Oversight officer dishonestly arranged prohibited commission payments of GBP 1m+.",
        },
    ],

    "threat_intelligence": [
        {
            "firm": "Nationwide Building Society",
            "fine": "GBP 44,078,500",
            "rules": ["Principle 3", "SYSC 6.1.1R", "SYSC 6.3.1R"],
            "year": 2025,
            "summary": "Serious weaknesses in financial crime systems and controls including CDD and transaction monitoring.",
        },
        {
            "firm": "Barclays Bank plc",
            "fine": "GBP 39,314,700",
            "rules": ["Principle 2", "AML"],
            "year": 2025,
            "summary": "Money laundering risk management failures spanning 6 years (Jan 2015 to Apr 2021).",
        },
        {
            "firm": "Monzo Bank Limited",
            "fine": "GBP 21,091,300",
            "rules": ["Principle 3", "FSMA s.55L"],
            "year": 2025,
            "summary": "Financial crime controls failed during rapid growth. Repeated breaches of higher-risk onboarding restriction.",
        },
        {
            "firm": "Citibank N.A. London Branch",
            "fine": "GBP 4,732,830",
            "rules": ["Russia Sanctions Regulations 2019"],
            "year": 2026,
            "summary": "OFSI fine for breach of Russia (Sanctions) (EU Exit) Regulations 2019.",
        },
    ],

    "cyber_threat_assessment": [
        {
            "firm": "Capita (ICO, not FCA)",
            "fine": "GBP 14,000,000",
            "rules": ["UK GDPR", "SYSC 7"],
            "year": 2025,
            "summary": "ICO fine for security failures and inadequate breach response capability. Major regulated-firm outsourcer.",
        },
        {
            "firm": "Revolut",
            "fine": "Pending",
            "rules": ["UK GDPR", "SYSC 7"],
            "year": 2026,
            "summary": "Customer data disclosed via fraudulent government agency request. Identity documents of customers exposed.",
        },
        {
            "firm": "Habib Bank",
            "fine": "Pending",
            "rules": ["SYSC", "PS21/3"],
            "year": 2025,
            "summary": "Qilin ransomware group targeted UK-regulated bank. Breach details not confirmed.",
        },
    ],

    "fca_incident_response": [
        {
            "firm": "Sector-wide (PS26/2)",
            "fine": "N/A — new framework",
            "rules": ["PS26/2", "SYSC"],
            "year": 2026,
            "summary": (
                "PS26/2 published 18 March 2026, in force 18 March 2027. "
                "24-hour reporting window for operational incidents. PSPs: 4 hours from detection. "
                "All Part 4A firms must build incident escalation frameworks by March 2027."
            ),
        },
        {
            "firm": "ITI Capital Ltd",
            "fine": "N/A (administration)",
            "rules": ["CASS", "SUP 15"],
            "year": 2026,
            "summary": "FCA-regulated firm entered special administration. Client asset return process activated.",
        },
    ],

    "due_diligence": [
        {
            "firm": "Kasim Garipoglu (CEO)",
            "fine": "Prohibition (ban)",
            "rules": ["FIT", "COCON", "SM&CR"],
            "year": 2026,
            "summary": "CEO banned: encouraged AML risk-taking, misled compliance staff and FCA. Not fit and proper.",
        },
        {
            "firm": "Nationwide Building Society",
            "fine": "GBP 44,078,500",
            "rules": ["Principle 3", "SYSC 6"],
            "year": 2025,
            "summary": "Serious CDD and transaction monitoring weaknesses. FCA cited inadequate financial crime governance.",
        },
        {
            "firm": "Monzo Bank Limited",
            "fine": "GBP 21,091,300",
            "rules": ["Principle 3"],
            "year": 2025,
            "summary": "Repeated breach of higher-risk customer onboarding restriction during rapid growth phase.",
        },
    ],

    "country_risk": [
        {
            "firm": "Citibank N.A. London Branch",
            "fine": "GBP 4,732,831 (OFSI)",
            "rules": ["Russia Sanctions (EU Exit) Regulations 2019"],
            "year": 2026,
            "summary": "Largest recent UK Russia sanctions fine. OFSI penalty for breach of Russia sanctions regulations.",
        },
        {
            "firm": "Markom Management Ltd",
            "fine": "GBP 300,000 (OFSI)",
            "rules": ["Russia Sanctions"],
            "year": 2025,
            "summary": "Instructed payment of GBP 416,590.92 to a designated Russia-linked individual.",
        },
        {
            "firm": "Sabre Global Technologies Ltd",
            "fine": "GBP 1,000,921 (OFSI)",
            "rules": ["Russia Sanctions"],
            "year": 2025,
            "summary": "Technology firm fined for breaching Russia financial sanctions via software licensing.",
        },
    ],

    "executive_protection": [
        {
            "firm": "Robin Odey (individual)",
            "fine": "GBP 1,529,374",
            "rules": ["COCON 2.2.1R"],
            "year": 2026,
            "summary": "Odey Capital Group founder fined for integrity failures. Asset management sector.",
        },
        {
            "firm": "Kasim Garipoglu (CEO, banned)",
            "fine": "Prohibition",
            "rules": ["FIT", "SM&CR"],
            "year": 2026,
            "summary": "CEO banned for misleading FCA and disregarding AML/regulatory obligations.",
        },
        {
            "firm": "Darren Reynolds (Compliance Director, banned)",
            "fine": "GBP 2,037,892 + ban",
            "rules": ["Statement of Principle 1", "SM&CR"],
            "year": 2026,
            "summary": "Director banned and fined for organising GBP 1m+ prohibited commission scheme.",
        },
        {
            "firm": "James Staley (CEO, Barclays)",
            "fine": "GBP 1,107,307",
            "rules": ["FCA conduct rules"],
            "year": 2025,
            "summary": "Fined for misleading FCA about relationship with Jeffrey Epstein.",
        },
    ],

    "grc_report": [
        {
            "firm": "Nationwide Building Society",
            "fine": "GBP 44,078,500",
            "rules": ["Principle 3", "SYSC 6.1.1R", "SYSC 6.3.1R"],
            "year": 2025,
            "summary": "Governance and compliance system failures — inadequate board-level oversight of financial crime controls and CDD governance framework.",
        },
        {
            "firm": "Barclays Bank plc",
            "fine": "GBP 39,314,700",
            "rules": ["Principle 2", "SYSC 6"],
            "year": 2025,
            "summary": "Risk management governance failure: 6-year span of inadequate AML risk controls with no senior escalation or board intervention.",
        },
        {
            "firm": "Aviva Pension Trustees UK Ltd",
            "fine": "GBP 8,200,000",
            "rules": ["Principle 3", "CASS"],
            "year": 2025,
            "summary": "Governance delegation without oversight: CASS compliance outsourced but board failed to maintain adequate oversight — FCA's 'abdication' ruling.",
        },
        {
            "firm": "Kasim Garipoglu (CEO)",
            "fine": "Prohibition (ban)",
            "rules": ["FIT", "COCON", "SM&CR"],
            "year": 2026,
            "summary": "Senior governance failure: CEO disregarded compliance obligations, misled FCA, and undermined internal controls. Individual accountability under SM&CR.",
        },
    ],

    "physical_security_audit": [
        {
            "firm": "Capita (ICO)",
            "fine": "GBP 14,000,000",
            "rules": ["UK GDPR", "SYSC"],
            "year": 2025,
            "summary": "Major outsourcer fined for security measure failures and inadequate breach response capability.",
        },
        {
            "firm": "Revolut",
            "fine": "Under investigation",
            "rules": ["UK GDPR", "SYSC 7"],
            "year": 2026,
            "summary": "Customer identity data exposed via social engineering attack on firm's security procedures.",
        },
    ],
}

# =============================================================================
# REGULATORY UPDATES — non-CASS intelligence by report type
# =============================================================================
REGULATORY_UPDATES = {
    "cass_oversight": {
        "smcr_phase1": (
            "SM&CR Phase 1 reforms effective 24 April 2026: SMF18 holders may hold any FCA-prescribed "
            "responsibility from 10 July 2026. Certification roles reduced ~15%. Enhanced firm thresholds "
            "increased 30%. SoR/MRM changes: 6-month notification window post-significant responsibility shift."
        ),
    },
    "executive_protection": {
        "non_financial_misconduct": (
            "From 1 September 2026, COCON 1.1.7FR extends non-financial misconduct (bullying, harassment, "
            "violence) into scope of COCON for all SM&CR firms. FIT test updated to consider NFM in "
            "fitness and propriety assessments. Approximately 37,000 FCA-authorised organisations affected."
        ),
        "smcr_phase1": (
            "SM&CR Phase 1 reforms: prescribed responsibilities restructured, certification roles reduced, "
            "Enhanced Firm thresholds raised 30%. Phase 2 requires FSMA legislative changes."
        ),
    },
    "cyber_threat_assessment": {
        "ps26_2": (
            "PS26/2 in force 18 March 2027: 24-hour operational incident reporting for most firms, "
            "4 hours for PSPs. Annual register of material third-party arrangements. "
            "82% of BoE H1 2026 Systemic Risk Survey respondents cite cyber-attack as top-5 risk. "
            "Average of 4 nationally significant cyber attacks every week in UK."
        ),
        "critical_third_parties": (
            "Critical Third Parties (CTPs) regime live from 13 July 2026. FCA/PRA/BoE overseeing "
            "first HM Treasury-designated CTPs — major cloud and tech providers. "
            "Firms using CTPs must maintain updated third-party registers and assess CTP resilience."
        ),
        "ps21_3_gaps": (
            "Post-March 2025 PS21/3 deadline: FCA found widespread gaps. Key deficiencies: "
            "single-factor IBS exclusions; time-only impact tolerances; theoretical-only scenario testing; "
            "response plans absent or untested; third-party resilience accepted without verification."
        ),
    },
    "fca_incident_response": {
        "ps26_2_obligations": (
            "PS26/2 (in force 18 March 2027): all Part 4A FSMA firms must report operational incidents "
            "within 24 hours of threshold determination. Thresholds: intolerable consumer harm; "
            "threat to firm safety/soundness; risk to market stability. "
            "Annual third-party arrangement register required."
        ),
    },
    "country_risk": {
        "ofsi_doubled_penalties": (
            "From 31 August 2026, OFSI maximum fine doubles from 50% to 100% of breach value. "
            "318 open OFSI Russia investigations in 2025. "
            "Iran sanctions expanded 2026. Citibank London fined GBP 4.7m for Russia breach."
        ),
    },
    "grc_report": {
        "smcr_governance_reforms": (
            "SM&CR Phase 1 reforms (24 April / 10 July / 1 Sep 2026): SMF18 holders may now hold any "
            "FCA-prescribed senior management responsibility. Certification roles reduced ~15%. "
            "Non-financial misconduct (COCON 1.1.7FR) now in scope for 37,000 firms from 1 Sep 2026. "
            "FIT test updated to include NFM assessments — firms must review governance arrangements."
        ),
        "ps26_2_third_party": (
            "PS26/2 (in force 18 March 2027): firms must maintain annual register of material third-party arrangements. "
            "24-hour operational incident reporting. GRC governance frameworks must accommodate this new obligation."
        ),
        "fca_governance_expectations": (
            "FCA published 'Portfolio strategy letters' (2025/26) emphasising: boards must receive clear MI on risk appetite; "
            "compliance functions must be resourced proportionately; firms must demonstrate control effectiveness not just policy existence. "
            "FCA expects GRC to be embedded — not bolted on."
        ),
    },
    "due_diligence": {
        "cdd_review_2026": (
            "FCA April 2026 CDD multi-firm review found: policies lack practical staff guidance; "
            "EDD triggers unclear; no evidence of EDD steps actually taken; "
            "senior management approval thresholds absent from policies; version control failures."
        ),
        "non_financial_misconduct": (
            "COCON 1.1.7FR effective 1 September 2026: serious non-financial misconduct now relevant "
            "to COCON and FIT assessments. Firms must consider NFM history in DD on SMF individuals."
        ),
    },
}

# =============================================================================
# CASS 1A FIRM CLASSIFICATION
# =============================================================================
def classify_cass_firm(client_money: float, custody_assets: float) -> dict:
    """
    Classify a firm under CASS 1A.2.7 R.
    client_money: highest amount held in previous calendar year (GBP)
    custody_assets: highest safe custody value (GBP)
    """
    if client_money > 1_000_000_000 or custody_assets > 100_000_000_000:
        return {"type": "CASS Large", "rule": "CASS 1A.2.7 R", "cmar_required": True}
    elif client_money >= 1_000_000 or custody_assets >= 10_000_000:
        return {"type": "CASS Medium", "rule": "CASS 1A.2.7 R", "cmar_required": True}
    else:
        return {"type": "CASS Small", "rule": "CASS 1A.2.7 R", "cmar_required": False}


def get_new_rules(since_date: str = "2024-01-01") -> list:
    """Return rules added or updated since a given date."""
    since = date.fromisoformat(since_date)
    new = []
    for ref, rule in CASS_RULES.items():
        try:
            d, m, y = rule["last_updated"].split("/")
            rule_date = date(int(y), int(m), int(d))
            if rule_date >= since:
                new.append({"ref": ref, **rule})
        except (ValueError, KeyError):
            pass
    return sorted(new, key=lambda x: x["last_updated"], reverse=True)


def get_news_by_severity(severity: str = None) -> list:
    """Return FCA news items, optionally filtered by severity (RED/AMBER/GREEN)."""
    if severity:
        return [n for n in FCA_NEWS if n["severity"] == severity]
    return FCA_NEWS


def get_intel_for_report(report_type: str) -> dict:
    """
    Return all intelligence relevant to a given report type:
    - FCA news items tagged to that report
    - Enforcement cases for that report
    - Regulatory updates for that report
    """
    news = [n for n in FCA_NEWS if report_type in n.get("report_types", [])]
    cases = ENFORCEMENT_CASES.get(report_type, [])
    updates = REGULATORY_UPDATES.get(report_type, {})
    return {
        "report_type": report_type,
        "sourced_date": SOURCED_DATE,
        "news": news,
        "enforcement_cases": cases,
        "regulatory_updates": updates,
    }


if __name__ == "__main__":
    print(f"FCA Reference Database — sourced {SOURCED_DATE}")
    print(f"Total rules: {len(CASS_RULES)}")
    print(f"Total news items: {len(FCA_NEWS)}")
    print(f"\nNew/updated since 2025:")
    for r in get_new_rules("2025-01-01"):
        print(f"  [{r['last_updated']}] {r['ref']} — {r['title']}")
    print(f"\nCritical (RED) FCA news:")
    for n in get_news_by_severity("RED"):
        print(f"  [{n['date']}] {n['headline']}")
    print(f"\nSample — intel for cyber_threat_assessment:")
    intel = get_intel_for_report("cyber_threat_assessment")
    print(f"  News items: {len(intel['news'])}")
    print(f"  Enforcement cases: {len(intel['enforcement_cases'])}")
    print(f"  Regulatory updates: {list(intel['regulatory_updates'].keys())}")
