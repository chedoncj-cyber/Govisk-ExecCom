"""
Regional Regulatory Routing
Maps geographic regions to their applicable client asset protection and money segregation rules.
Imported by report generators to route findings to the correct jurisdiction-specific framework.

Usage:
    from regional_routing import (
        is_n_america, is_latam, get_regional_regs,
        score_us_client_money, score_latam_client_money,
        us_regulatory_refs, latam_regulatory_refs,
        uk_us_comparison_table, uk_latam_comparison_table,
    )
"""

# ── North America country/region identifiers ──────────────────────────────────
N_AMERICA_COUNTRIES = {
    "United States", "USA", "US", "U.S.", "U.S.A.",
    "Canada", "Mexico",
    "Caribbean", "Jamaica", "Cayman Islands", "Bermuda", "Bahamas",
    "Puerto Rico", "Virgin Islands",
}

US_STATES = {
    "New York", "California", "Texas", "Florida", "Illinois",
    "Massachusetts", "Connecticut", "New Jersey", "Delaware",
}

N_AMERICA_KEYWORDS = ("america", "united states", "usa", "u.s.", "cayman", "bermuda", "canada")


# ── US Client Asset Protection Framework ──────────────────────────────────────
US_REGS = {
    "sec_15c3_3": {
        "rule":        "SEC Rule 15c3-3",
        "full_name":   "Customer Protection Rule",
        "authority":   "SEC (Securities and Exchange Commission)",
        "applies_to":  "Registered broker-dealers",
        "uk_equiv":    "CASS 6 / CASS 7",
        "description": (
            "Requires U.S. broker-dealers to segregate customer fully-paid and excess margin "
            "securities into a Special Custody Account and maintain a Special Reserve Bank Account "
            "(SRBA) for the exclusive benefit of customers. Weekly reserve formula calculation "
            "required. Equivalent in purpose to UK CASS 7 (client money) and CASS 6 (custody assets)."
        ),
        "key_obligations": [
            "Segregate fully-paid and excess margin customer securities into a Special Custody Account",
            "Maintain Special Reserve Bank Account (SRBA) — exclusive benefit of customers",
            "Perform weekly reserve formula calculation (credit items minus debit items)",
            "No commingling of customer and proprietary assets",
            "Obtain written acknowledgement from each bank/custodian holding customer assets",
            "Promptly deliver or credit customer fully-paid securities",
        ],
    },
    "cftc_1_20": {
        "rule":        "CFTC Rule 1.20",
        "full_name":   "Segregation of Funds Received from Customers",
        "authority":   "CFTC (Commodity Futures Trading Commission)",
        "applies_to":  "Futures Commission Merchants (FCMs)",
        "uk_equiv":    "CASS 7",
        "description": (
            "Requires FCMs to hold customer money, securities, and property in strictly segregated "
            "accounts at approved depositories under Section 4d of the Commodity Exchange Act (CEA). "
            "Prohibits commingling with firm operational funds. Requires daily calculation of the "
            "customer segregated amount. UK equivalent: CASS 7 for client money held by investment firms."
        ),
        "key_obligations": [
            "Hold customer funds in segregated accounts at approved depositories",
            "Daily calculation of segregated amount required — filed with CFTC",
            "No commingling of customer and firm funds at any time",
            "Obtain written acknowledgement from depository institutions",
            "Maintain sufficient funds to cover the daily net liquidating value of all customer positions",
        ],
    },
    "cea_4d": {
        "rule":        "Section 4d — Commodity Exchange Act (CEA)",
        "full_name":   "CEA Section 4d — FCM Segregation Prohibition",
        "authority":   "CFTC",
        "applies_to":  "Futures Commission Merchants (FCMs)",
        "uk_equiv":    "CASS 7 / FSMA 2000",
        "description": (
            "Primary statutory basis for FCM customer fund segregation. Prohibits FCMs from "
            "commingling customer funds with their own. Works alongside CFTC Rule 1.20 to form "
            "the core U.S. futures industry client money protection framework."
        ),
        "key_obligations": [
            "Statutory prohibition on commingling customer and proprietary funds",
            "Customer funds must be 'separately accounted for' at all times",
            "Failure constitutes a criminal offence under the CEA",
        ],
    },
    "sipc": {
        "rule":        "SIPC Protection",
        "full_name":   "Securities Investor Protection Corporation",
        "authority":   "SIPC (established under Securities Investor Protection Act 1970)",
        "applies_to":  "SIPC-member broker-dealers",
        "uk_equiv":    "FSCS (Financial Services Compensation Scheme)",
        "coverage":    "$500,000 per customer (including up to $250,000 for cash)",
        "description": (
            "Provides backstop protection of up to $500,000 per customer (including up to $250,000 "
            "for cash) if a SIPC-member brokerage fails and customer assets are missing. Functionally "
            "equivalent to the UK FSCS for failed investment firms — activates when segregation has "
            "failed and customer assets cannot be recovered from the estate. Does NOT cover market losses."
        ),
        "key_obligations": [
            "SIPC membership mandatory for all SEC-registered broker-dealers",
            "SIPC trustee appointed on insolvency to recover missing customer assets",
            "Protection up to $500,000 per customer (incl. $250,000 cash) for missing assets",
            "Supplements — does not replace — segregation under SEC Rule 15c3-3",
            "Covers missing cash and securities only; does not cover investment losses",
        ],
    },
}


# ── Helper functions ───────────────────────────────────────────────────────────

def is_n_america(country_or_region: str) -> bool:
    """Return True if the country/region triggers N. America regulatory routing."""
    if not country_or_region:
        return False
    val = country_or_region.strip()
    if val in N_AMERICA_COUNTRIES or val in US_STATES:
        return True
    val_lower = val.lower()
    return any(kw in val_lower for kw in N_AMERICA_KEYWORDS)


def get_regional_regs(country_or_region: str) -> dict:
    """Return the applicable US regulatory framework dict, or empty dict for other regions."""
    return US_REGS if is_n_america(country_or_region) else {}


def score_us_client_money(data: dict) -> list:
    """
    Generate US-specific client money / customer asset segregation findings.
    Mirrors the CASS 7 scoring in generate_client_money_segregation.py but
    mapped to SEC Rule 15c3-3, CFTC Rule 1.20, and SIPC.
    Called when country/jurisdiction is detected as N. America.
    """
    findings = []
    firm_type  = data.get("firm_type", "").lower()
    is_fcm     = any(t in firm_type for t in ("fcm", "futures", "commodity", "derivatives"))
    rule       = "CFTC Rule 1.20 / CEA Section 4d" if is_fcm else "SEC Rule 15c3-3"
    uk_equiv   = "CASS 7" if is_fcm else "CASS 6 / CASS 7"

    # 1. Account segregation
    designated = data.get("all_accounts_designated")
    findings.append({
        "area":        "Account Segregation (US)",
        "rule":        rule,
        "description": "Customer funds/assets held in segregated accounts",
        "status":      "GREEN" if designated else "RED",
        "commentary": (
            f"All customer accounts confirmed segregated per {rule}. "
            f"U.S. equivalent of UK {uk_equiv}."
        ) if designated else (
            f"CRITICAL: Customer accounts NOT fully segregated. Breach of {rule}. "
            f"U.S. equivalent of UK {uk_equiv} failure. Immediate SEC/CFTC enforcement risk."
        ),
    })

    # 2. Daily segregation calculation (CFTC) or weekly reserve formula (SEC)
    freq = data.get("internal_reconciliation_frequency", "").lower()
    if is_fcm:
        findings.append({
            "area":        "Daily Segregation Calculation (US)",
            "rule":        "CFTC Rule 1.20",
            "description": "Daily customer segregated amount calculation",
            "status":      "GREEN" if freq == "daily" else "RED",
            "commentary": (
                "Daily segregation calculation confirmed per CFTC Rule 1.20. "
                "UK equivalent: CASS 7.13.4R daily internal reconciliation."
            ) if freq == "daily" else (
                f"Segregation calculation frequency '{freq}' does not meet CFTC Rule 1.20 "
                "daily requirement. UK equivalent: CASS 7.13.4R daily reconciliation."
            ),
        })
    else:
        findings.append({
            "area":        "Reserve Formula Calculation (US)",
            "rule":        "SEC Rule 15c3-3",
            "description": "Weekly Special Reserve Bank Account (SRBA) reserve calculation",
            "status":      "GREEN" if freq in ("weekly", "daily") else "AMBER",
            "commentary": (
                "Reserve formula calculation frequency meets SEC Rule 15c3-3 weekly SRBA requirement. "
                "UK equivalent: CASS 7 client money calculation method."
            ) if freq in ("weekly", "daily") else (
                "Reserve formula calculation frequency not confirmed. SEC Rule 15c3-3 requires weekly "
                "SRBA computation. UK equivalent: CASS 7 client money calculation."
            ),
        })

    # 3. SIPC membership
    sipc_member = data.get("sipc_member")
    if sipc_member is not None:
        findings.append({
            "area":        "SIPC Protection (US)",
            "rule":        "Securities Investor Protection Act 1970",
            "description": "SIPC membership confirmed",
            "status":      "GREEN" if sipc_member else "RED",
            "commentary": (
                "SIPC membership confirmed. Customer protection up to $500,000 per customer "
                "(including $250,000 for cash). U.S. equivalent of UK FSCS £85,000 protection."
            ) if sipc_member else (
                "SIPC membership NOT confirmed. SEC-registered broker-dealers must be SIPC members. "
                "Absence of SIPC coverage is the U.S. equivalent of a missing FSCS backstop."
            ),
        })

    # 4. Depository acknowledgement letters
    ack = data.get("acknowledgement_letters_all_accounts")
    findings.append({
        "area":        "Depository Acknowledgements (US)",
        "rule":        rule,
        "description": "Written acknowledgements from all depositories/custodians",
        "status":      "GREEN" if ack is True else ("RED" if ack is False else "AMBER"),
        "commentary": (
            f"Written acknowledgements obtained from all depositories per {rule}. "
            "U.S. equivalent of UK CASS 7.18.3R acknowledgement letters."
        ) if ack is True else (
            f"Acknowledgement letters MISSING. {rule} requires written confirmation "
            "from each depository that funds are held exclusively for customer benefit. "
            "U.S. equivalent of UK CASS 7.18.3R breach."
        ) if ack is False else (
            "Acknowledgement letter status unconfirmed. Full depository inventory required."
        ),
    })

    # 5. Commingling check
    commingling = data.get("commingling_identified")
    if commingling is not None:
        findings.append({
            "area":        "Commingling Prohibition (US)",
            "rule":        rule,
            "description": "No commingling of customer and firm funds identified",
            "status":      "RED" if commingling else "GREEN",
            "commentary": (
                f"CRITICAL: Commingling of customer and firm funds detected. Direct breach of {rule}. "
                "U.S. equivalent of UK CASS 7 commingling prohibition. Criminal liability under CEA Section 4d."
            ) if commingling else (
                "No commingling identified. Customer and proprietary funds maintained in separate accounts."
            ),
        })

    return findings


def score_us_cross_border(country: str, data: dict) -> list:
    """
    Add US regulatory context to country risk findings when country is in N. America.
    Called by generate_country_risk.py for cross-border client asset checks.
    """
    findings = []
    purpose = data.get("purpose", "")

    if "client asset" in purpose.lower() or "cass" in purpose.lower() or "segregat" in purpose.lower():
        findings.append({
            "area":        "US Regulatory Framework — Client Assets",
            "rule":        "SEC Rule 15c3-3 / CFTC Rule 1.20",
            "description": f"US client asset protection framework applicable — {country}",
            "status":      "AMBER",
            "commentary": (
                f"Cross-border client assets in {country} fall under U.S. regulatory jurisdiction. "
                "Broker-dealers: SEC Rule 15c3-3 (Customer Protection Rule) requires segregation into "
                "Special Custody Account + Special Reserve Bank Account. "
                "FCMs: CFTC Rule 1.20 / CEA Section 4d requires daily segregation calculations. "
                "UK CASS protections do not apply extraterritorially — U.S. equivalents must be "
                "verified to ensure equivalent client asset protection. "
                "SIPC backstop ($500,000 per customer) is the U.S. equivalent of UK FSCS."
            ),
        })

    findings.append({
        "area":        "SIPC vs FSCS — Backstop Protection",
        "rule":        "Securities Investor Protection Act 1970",
        "description": f"Customer backstop protection in {country}",
        "status":      "GREEN",
        "commentary": (
            "SIPC provides U.S. customer backstop protection of up to $500,000 per customer "
            "(including $250,000 for cash) in the event of a firm failure. "
            "Higher nominal limit than UK FSCS (£85,000) but covers missing assets only — "
            "does not cover market losses. Confirm SIPC membership of all U.S. counterparties."
        ),
    })

    return findings




def uk_us_comparison_table() -> list:
    """Return (UK rule, US equivalent) rows for a UK CASS vs US comparison narrative."""
    return [
        ("CASS 7 — Client Money segregation",        "CFTC Rule 1.20 / CEA Section 4d (FCMs); SEC Rule 15c3-3 SRBA (broker-dealers)"),
        ("CASS 6 — Custody of client assets",        "SEC Rule 15c3-3 — Special Custody Account for customer securities"),
        ("CASS 7.13.4R — Daily reconciliation",      "CFTC Rule 1.20 — daily segregation calculation; SEC Rule 15c3-3 — weekly SRBA formula"),
        ("CASS 7.18.3R — Acknowledgement letters",   "SEC/CFTC written depository acknowledgement requirements"),
        ("CASS 7.19 — Diversification",              "No direct U.S. equivalent — managed via counterparty credit risk policy"),
        ("FSCS — £85,000 per customer backstop",     "SIPC — $500,000 per customer (incl. $250,000 cash) — missing assets only"),
        ("FCA CASS Oversight Function",              "SEC / CFTC examination, enforcement, and sweep programmes"),
        ("CASS 10 — Resolution Pack",                "FDIC resolution planning (banks); FINRA Rule 4370 (broker-dealers BCP)"),
    ]


# ══════════════════════════════════════════════════════════════════════════════
# LATIN AMERICA REGIONAL ROUTING
# ══════════════════════════════════════════════════════════════════════════════

LATAM_COUNTRIES = {
    "Brazil", "Argentina", "Mexico", "Chile", "Colombia", "Peru",
    "Venezuela", "Ecuador", "Bolivia", "Paraguay", "Uruguay",
    "Panama", "Costa Rica", "Guatemala", "Honduras", "El Salvador",
    "Nicaragua", "Dominican Republic", "Cuba",
}

LATAM_KEYWORDS = ("brazil", "argentina", "chile", "colombia", "peru", "latin", "latam",
                  "south america", "central america", "caribbean")

# Per-country regulatory frameworks
LATAM_REGS = {
    "Brazil": {
        "authority":    "Banco Central do Brasil (BCB)",
        "rule":         "Law No. 12,865 / BCB Resolution",
        "full_name":    "Payment Institution Segregation — Patrimônio Separado",
        "uk_equiv":     "CASS 7",
        "description": (
            "Under Brazil's Law No. 12,865, funds held in payment accounts must be treated as "
            "isolated, separate assets (patrimônio separado). They are legally ring-fenced from "
            "the payment institution's bankruptcy estate and cannot be subject to judicial "
            "attachment for the institution's own debts. The BCB enforces strict operational "
            "and capital standards through resolutions for payment institutions and infrastructure providers."
        ),
        "key_obligations": [
            "Customer funds must be held as patrimônio separado — legally isolated from firm assets",
            "Ring-fencing is statutory — immune from bankruptcy proceedings and judicial attachment",
            "BCB enforces strict operational and capital standards via resolutions",
            "Payment institutions must comply with BCB liquidity and operational requirements",
        ],
    },
    "Argentina": {
        "authority":    "Banco Central de la República Argentina (BCRA)",
        "rule":         "BCRA Communiqué 'A' 6859",
        "full_name":    "PSP Customer Fund Segregation",
        "uk_equiv":     "CASS 7",
        "description": (
            "Under BCRA Communiqué 'A' 6859, Payment Service Providers (PSPs) offering payment "
            "accounts must immediately make 100% of customer funds available and deposit them in "
            "local bank accounts denominated in pesos, keeping them strictly separate from the "
            "PSP's own operational funds and expenses."
        ),
        "key_obligations": [
            "100% of customer funds must be held separately from PSP operational funds",
            "Funds must be deposited in local peso-denominated bank accounts",
            "Immediate availability of 100% of customer balances required at all times",
            "No use of customer funds for PSP operational expenses",
        ],
    },
    "Mexico": {
        "authority":    "CNBV / Banco de México",
        "rule":         "Fintech Law 2018 (Ley Para Regular las Instituciones de Tecnología Financiera)",
        "full_name":    "Mexican Fintech Law — Client Fund Segregation",
        "uk_equiv":     "CASS 7 / FCA Payment Services Regulations",
        "description": (
            "Mexico's 2018 Fintech Law mandates that financial technology institutions (ITFs) and "
            "electronic payment fund institutions (IFPEs) segregate client funds from corporate "
            "assets and follow strict operational and liquidity protections. Supervised jointly by "
            "the CNBV (banking regulator) and Banco de México."
        ),
        "key_obligations": [
            "Strict segregation of client funds from corporate assets — mandatory for ITFs and IFPEs",
            "Operational and liquidity requirements per Fintech Law secondary rules",
            "CNBV authorisation required to hold and manage client funds",
            "Anti-money laundering obligations aligned with FATF recommendations",
        ],
    },
    "Chile": {
        "authority":    "Comisión para el Mercado Financiero (CMF)",
        "rule":         "Law No. 21,521 (Fintech Law) / CMF Framework",
        "full_name":    "Chilean Fintech Law — Customer Asset Security",
        "uk_equiv":     "CASS 6 / CASS 7 / FCA Payment Services Regulations",
        "description": (
            "Chile's Law No. 21,521 (Fintech Law) establishes clear rules for non-bank financial "
            "service providers, including interoperability requirements and customer asset security. "
            "The CMF supervises compliance and sets standards for client fund protection applicable "
            "to Open Finance participants, payment providers, and investment intermediaries."
        ),
        "key_obligations": [
            "Customer asset protection mandated for non-bank financial service providers",
            "Interoperability and open finance rules applicable",
            "CMF authorisation required — ongoing supervision and capital requirements",
            "Client fund segregation from firm assets required",
        ],
    },
    "Colombia": {
        "authority":    "Superintendencia Financiera de Colombia (SFC)",
        "rule":         "SFC Circular Externa / Decree 2555",
        "full_name":    "Customer Fund Protection — Colombian Financial System",
        "uk_equiv":     "CASS 7",
        "description": (
            "Colombia's financial system is supervised by the SFC. Client money segregation "
            "obligations apply to licensed financial entities under Decree 2555 and SFC circulars. "
            "Payment service providers and electronic deposit entities must maintain customer "
            "funds separately from own resources."
        ),
        "key_obligations": [
            "SFC licensing required to hold customer funds",
            "Segregation of customer deposits from operational funds",
            "Ongoing capital and liquidity requirements per SFC circulars",
        ],
    },
}

# Fallback for LATAM countries without specific entries
LATAM_DEFAULT = {
    "authority":    "National Central Bank / Financial Supervisory Authority",
    "rule":         "National Regulatory Framework",
    "uk_equiv":     "CASS 7 (functional equivalent — varies by jurisdiction)",
    "description": (
        "Latin America does not have a single region-wide equivalent to UK CASS. Each country "
        "regulates customer fund segregation independently through its national central bank or "
        "financial supervisory authority. Verify the specific national framework applicable to "
        "the jurisdiction in question before transacting or holding client assets."
    ),
    "key_obligations": [
        "Verify national regulator authorisation for the counterparty/entity",
        "Confirm customer fund segregation obligations under local law",
        "Assess adequacy of local investor/depositor protection schemes",
        "No single LATAM equivalent to UK FSCS — protection varies significantly by country",
    ],
}


def is_latam(country_or_region: str) -> bool:
    """Return True if the country/region triggers Latin America regulatory routing."""
    if not country_or_region:
        return False
    val = country_or_region.strip()
    if val in LATAM_COUNTRIES:
        return True
    val_lower = val.lower()
    return any(kw in val_lower for kw in LATAM_KEYWORDS)


def get_latam_country_regs(country: str) -> dict:
    """Return the LATAM country-specific regulatory framework, or the regional default."""
    return LATAM_REGS.get(country, LATAM_DEFAULT)


def score_latam_client_money(data: dict) -> list:
    """
    Generate Latin America-specific client money / customer fund segregation findings.
    Routes to the correct national framework based on data['country'].
    Called when country/jurisdiction is detected as LATAM.
    """
    findings = []
    country  = data.get("country", "Unknown")
    regs     = get_latam_country_regs(country)
    rule     = regs["rule"]
    authority = regs["authority"]

    # 1. Regulatory authorisation
    authorised = data.get("local_regulator_authorised")
    if authorised is not None:
        findings.append({
            "area":        f"Regulatory Authorisation ({country})",
            "rule":        rule,
            "description": f"Entity authorised by {authority}",
            "status":      "GREEN" if authorised else "RED",
            "commentary": (
                f"Entity confirmed authorised by {authority}. "
                f"Applicable framework: {rule}. UK equivalent: {regs['uk_equiv']}."
            ) if authorised else (
                f"CRITICAL: Entity does NOT hold authorisation from {authority}. "
                f"Operating without local regulatory licence in {country}. "
                f"UK equivalent: operating without FCA authorisation — criminal offence under FSMA 2000."
            ),
        })

    # 2. Fund segregation
    segregated = data.get("all_accounts_designated")
    findings.append({
        "area":        f"Customer Fund Segregation ({country})",
        "rule":        rule,
        "description": f"Customer funds segregated per {authority} requirements",
        "status":      "GREEN" if segregated else "RED",
        "commentary": (
            f"Customer funds confirmed segregated per {rule} ({authority}). "
            f"UK equivalent: {regs['uk_equiv']}."
        ) if segregated else (
            f"Customer funds NOT confirmed segregated under {rule}. "
            f"Breach of {authority} requirements. UK equivalent: CASS 7 failure."
        ),
    })

    # 3. No single LATAM-wide investor protection
    findings.append({
        "area":        f"Investor/Depositor Protection ({country})",
        "rule":        "National Framework",
        "description": "Equivalent of UK FSCS backstop protection",
        "status":      "AMBER",
        "commentary": (
            "Latin America does not have a single region-wide investor protection scheme equivalent "
            f"to the UK FSCS. In {country}, protection depends on the national framework supervised "
            f"by {authority}. Verify existence and scope of any deposit guarantee or investor "
            "compensation scheme before placing or holding client assets."
        ),
    })

    # 4. Cross-border note
    findings.append({
        "area":        "Cross-Border CASS Applicability",
        "rule":        "CASS 6 / CASS 7 (UK)",
        "description": f"UK CASS protections — applicability in {country}",
        "status":      "AMBER",
        "commentary": (
            f"UK CASS rules do not apply extraterritorially in {country}. "
            "Where UK-authorised firms hold client assets cross-border, they must ensure "
            "the local framework provides equivalent protection. Specific due diligence "
            "on the local custody and segregation framework is required under CASS 6.3 "
            "(third-party custody) and CASS 7.13 (third-party money arrangements)."
        ),
    })

    return findings


def score_latam_cross_border(country: str, data: dict) -> list:
    """
    Add LATAM regulatory context to country risk findings.
    Called by generate_country_risk.py for cross-border client asset checks.
    """
    findings = []
    regs      = get_latam_country_regs(country)
    purpose   = data.get("purpose", "")

    if "client asset" in purpose.lower() or "cass" in purpose.lower() or "segregat" in purpose.lower():
        findings.append({
            "area":        f"LATAM Regulatory Framework — Client Assets ({country})",
            "rule":        regs["rule"],
            "description": f"Customer fund protection framework — {country}",
            "status":      "AMBER",
            "commentary": (
                f"Cross-border client assets in {country} are governed by {regs['authority']} "
                f"under {regs['rule']}. {regs['description']} "
                "UK CASS protections do not apply extraterritorially. Confirm that local "
                "segregation standards provide equivalent protection before placing client assets."
            ),
        })

    findings.append({
        "area":        f"No Unified LATAM CASS Equivalent",
        "rule":        "CASS 6.3 / CASS 7.13",
        "description": "Region-wide client asset protection — Latin America",
        "status":      "AMBER",
        "commentary": (
            "Latin America has no single region-wide CASS equivalent. Each country regulates "
            "customer fund segregation independently. FCA-authorised firms holding assets in "
            "the region must conduct country-by-country due diligence on local custody and "
            "segregation laws. Key frameworks: Brazil (Law 12,865 — patrimônio separado), "
            "Argentina (BCRA Communiqué A 6859 — 100% availability), Mexico (Fintech Law 2018), "
            "Chile (Law 21,521). Refer to CASS 6.3 for third-party custody obligations."
        ),
    })

    return findings


def latam_regulatory_refs() -> list:
    """Return (label, detail) tuples for LATAM regulatory reference tables."""
    return [
        ("Brazil — Law No. 12,865",          "BCB framework — patrimônio separado customer fund ring-fencing"),
        ("Argentina — BCRA Communiqué A 6859","PSP 100% customer fund availability and segregation obligation"),
        ("Mexico — Fintech Law 2018",         "CNBV / Banco de México — ITF/IFPE client fund segregation"),
        ("Chile — Law No. 21,521",            "CMF Fintech Law — non-bank financial service provider customer asset protection"),
        ("Colombia — Decree 2555 / SFC",      "SFC supervision of customer fund segregation for licensed entities"),
        ("CASS 6.3",                          "Third-party custody — equivalent protection requirements for cross-border assets"),
        ("CASS 7.13",                         "Third-party money arrangements — due diligence and ongoing monitoring"),
    ]


def uk_latam_comparison_table() -> list:
    """Return (UK rule, LATAM equivalent) rows for a UK CASS vs LATAM comparison narrative."""
    return [
        ("CASS 7 — Client Money",             "Brazil: Law 12,865 patrimônio separado | Argentina: BCRA A 6859 | Mexico: Fintech Law 2018"),
        ("CASS 6 — Custody Assets",           "Country-specific custody frameworks — no single LATAM equivalent"),
        ("CASS 7.13.4R — Daily reconciliation","Varies by country — Brazil BCB resolutions; Argentina 100% availability requirement"),
        ("CASS 7.18.3R — Acknowledgement",    "No standardised LATAM equivalent — verify per local depository requirements"),
        ("FSCS — Customer backstop",          "No single LATAM-wide scheme — national deposit guarantee/investor protection varies"),
        ("FCA CASS Oversight Function",       "BCB (Brazil) | BCRA (Argentina) | CNBV/Banxico (Mexico) | CMF (Chile) | SFC (Colombia)"),
        ("CASS 6.3 — Third-party custody",    "CASS 6.3 applies to UK firms — must verify local law provides equivalent protection"),
    ]


# ══════════════════════════════════════════════════════════════════════════════
# ASIA PACIFIC REGIONAL ROUTING
# ══════════════════════════════════════════════════════════════════════════════

APAC_COUNTRIES = {
    "Hong Kong", "Australia", "Singapore", "Japan", "China", "South Korea",
    "New Zealand", "India", "Taiwan", "Malaysia", "Thailand", "Indonesia",
    "Philippines", "Vietnam", "Cambodia", "Myanmar",
}

APAC_KEYWORDS = ("hong kong", "australia", "singapore", "japan", "asia", "apac",
                 "asia pacific", "asia-pacific", "south korea", "new zealand")

APAC_REGS = {
    # ── Hong Kong ─────────────────────────────────────────────────────────────
    "Hong Kong": {
        "authority":   "Securities and Futures Commission (SFC)",
        "rule":        "Securities and Futures (Client Money) Rules (Cap. 571I) / Securities and Futures (Client Securities) Rules (Cap. 571H)",
        "full_name":   "SFC Client Money Rules (Cap. 571I) and Client Securities Rules (Cap. 571H)",
        "uk_equiv":    "CASS 7 (client money) / CASS 6 (custody assets)",
        "website":     "https://www.sfc.hk",
        "legislation_refs": [
            "Cap. 571I — Securities and Futures (Client Money) Rules",
            "Cap. 571H — Securities and Futures (Client Securities) Rules",
            "Securities and Futures Ordinance (SFO) — parent legislation",
        ],
        "description": (
            "Hong Kong's client asset regime is governed by the SFC under two pieces of subsidiary "
            "legislation to the Securities and Futures Ordinance (SFO): "
            "Cap. 571I (Client Money Rules) requires licensed intermediaries to hold all client money "
            "in designated trust or client accounts with authorised financial institutions — strictly "
            "segregated from the firm's own assets. "
            "Cap. 571H (Client Securities Rules) requires client securities to be held in segregated "
            "accounts, with strict controls over standing authorities and third-party transactions. "
            "Both rules mandate timely daily or periodic reconciliations. "
            "UK equivalent: CASS 7 for client money / CASS 6 for custody assets."
        ),
        "key_obligations": [
            "Cap. 571I — client money held in designated trust/client accounts at authorised financial institutions",
            "Cap. 571H — client securities held in segregated accounts, separate from firm's own securities",
            "Daily or periodic reconciliation of client money and securities positions",
            "Strict controls on standing authorities and third-party transactions",
            "SFC Type 1 (dealing) or Type 9 (asset management) licence required to hold client assets",
            "Client funds and securities protected on firm insolvency — trust account structure",
        ],
    },
    # ── Singapore ─────────────────────────────────────────────────────────────
    "Singapore": {
        "authority":   "Monetary Authority of Singapore (MAS)",
        "rule":        "Securities and Futures Act (SFA) Section 104 / Securities and Futures (Licensing and Conduct of Business) Regulations (SFLCBR) / Payment Services Act (PSA)",
        "full_name":   "MAS Customer Fund Segregation — SFA Section 104 + SFLCBR",
        "uk_equiv":    "CASS 7 / CASS 6 / FCA Payment Services Regulations",
        "website":     "https://www.mas.gov.sg",
        "legislation_refs": [
            "Securities and Futures Act (SFA) — Section 104 (customer money and assets)",
            "Securities and Futures (Licensing and Conduct of Business) Regulations (SFLCBR)",
            "Payment Services Act (PSA) — customer fund safeguarding for payment institutions",
            "MAS Notice SFA 04-N02 — licence conditions and client asset requirements",
        ],
        "description": (
            "Singapore's MAS client asset framework is primarily governed by SFA Section 104 and "
            "the SFLCBR. Capital Markets Services (CMS) licence holders must deposit customer moneys "
            "and custody assets into designated trust accounts or with approved custodians by the "
            "next business day. Firms must maintain separate individual book entries for each customer "
            "and perform daily trust and custody computations. "
            "For payment institutions, the Payment Services Act (PSA) requires customer e-money to "
            "be held in safeguarding accounts at approved financial institutions. "
            "UK equivalent: SFA Section 104 ≈ CASS 7 (client money) + CASS 6 (custody)."
        ),
        "key_obligations": [
            "SFA Section 104 — customer money deposited into designated trust accounts by next business day",
            "SFLCBR — separate individual book entries maintained per customer",
            "Daily trust and custody computations required",
            "Customer assets held with approved custodians — due diligence required",
            "MAS Capital Markets Services (CMS) licence required for capital markets activities",
            "PSA — payment institutions must hold customer funds in safeguarding accounts",
            "MAS Notice SFA 04-N02 — licence conditions on client asset handling",
            "Customer funds protected on insolvency — statutory trust structure",
        ],
    },
    # ── Australia ─────────────────────────────────────────────────────────────
    "Australia": {
        "authority":   "Australian Securities and Investments Commission (ASIC)",
        "rule":        "Corporations Act 2001 — Division 2 of Part 7.8 / ASIC Client Money Reporting Rules",
        "full_name":   "Corporations Act 2001 Division 2 Part 7.8 — Client Money Requirements",
        "uk_equiv":    "CASS 7 / CASS 6",
        "website":     "https://www.asic.gov.au",
        "legislation_refs": [
            "Corporations Act 2001 — Division 2 of Part 7.8 (sections 981A–981H) — client money",
            "ASIC Client Money Reporting Rules 2017 — mandatory reporting for derivatives issuers",
            "Corporations Act 2001 — Section 1017E — portfolio trust accounting",
        ],
        "description": (
            "Australia's client money regime is governed by Division 2 of Part 7.8 of the "
            "Corporations Act 2001 (sections 981A–981H) and the ASIC Client Money Reporting Rules. "
            "Financial services licensees (AFSL holders) must hold client money in dedicated trust "
            "accounts separate from the licensee's own money. The ASIC Client Money Reporting Rules "
            "impose quarterly mandatory reporting obligations on derivatives issuers and clearing "
            "participants. Retail client money rules impose additional protection requirements. "
            "UK equivalent: Division 2 of Part 7.8 ≈ CASS 7."
        ),
        "key_obligations": [
            "Section 981B — client money must be paid into a dedicated client money trust account",
            "Prohibition on mixing client money with the licensee's own money",
            "Division 2 of Part 7.8 — retail client money has enhanced protection requirements",
            "Mandatory daily reconciliation of client trust account balances",
            "ASIC Client Money Reporting Rules — quarterly reporting for derivatives issuers/clearing participants",
            "Australian Financial Services Licence (AFSL) required to hold client money",
            "APRA-regulated bank or approved deposit-taking institution must hold the trust account",
        ],
    },
    # ── Japan ─────────────────────────────────────────────────────────────────
    "Japan": {
        "authority":   "Financial Services Agency (FSA Japan)",
        "rule":        "Financial Instruments and Exchange Act (FIEA) — Customer Asset Separation",
        "full_name":   "FIEA — Separation of Customer Assets from Proprietary Funds",
        "uk_equiv":    "CASS 6 / CASS 7",
        "website":     "https://www.fsa.go.jp/en",
        "legislation_refs": [
            "Financial Instruments and Exchange Act (FIEA) — Article 43-2 (segregation of customer assets)",
            "FIEA Cabinet Office Ordinance — operational requirements for asset separation",
            "Investor Protection Fund (IPF) — backstop equivalent to UK FSCS (up to ¥10M)",
        ],
        "description": (
            "Japan's FSA enforces customer asset protection under the Financial Instruments and "
            "Exchange Act (FIEA). Article 43-2 mandates mandatory separation of customer assets "
            "from the firm's own proprietary funds. Licensed Type I and Type II financial instruments "
            "business operators must hold customer securities and money in dedicated segregated accounts "
            "at approved custodians, with regular internal and external verification of compliance. "
            "UK equivalent: FIEA Article 43-2 ≈ CASS 7 (money) + CASS 6 (securities)."
        ),
        "key_obligations": [
            "FIEA Article 43-2 — mandatory separation of customer assets from firm proprietary assets",
            "Customer securities and money held in designated segregated accounts at approved custodians",
            "Regular internal and external verification of segregation compliance",
            "FSA Type I or Type II Financial Instruments Business registration required",
            "Investor Protection Fund (IPF) membership — ¥10M/customer backstop (equiv. UK FSCS)",
            "Cabinet Office Ordinance — detailed operational requirements for asset separation",
        ],
    },
    # ── India ─────────────────────────────────────────────────────────────────
    "India": {
        "authority":   "SEBI (Securities and Exchange Board of India) / RBI (Reserve Bank of India)",
        "rule":        "SEBI (Stock Brokers) Regulations 1992 / SEBI Circular on Client Funds / RBI Master Directions",
        "full_name":   "SEBI Client Fund Segregation and RBI Banking Regulations",
        "uk_equiv":    "CASS 7 / CASS 6",
        "website":     "https://www.sebi.gov.in",
        "legislation_refs": [
            "SEBI (Stock Brokers) Regulations 1992 — client money segregation",
            "SEBI Circular SEBI/HO/MIRSD/DOP/CIR/P/2019/106 — client securities and funds",
            "RBI Master Direction on KYC — AML obligations",
        ],
        "description": (
            "India's SEBI regulates capital markets and requires registered stock brokers and "
            "investment managers to maintain separate client bank accounts and securities accounts. "
            "SEBI has progressively tightened client fund rules, mandating daily reconciliation and "
            "prohibiting use of client money for proprietary purposes. The RBI regulates banking "
            "and payment systems and enforces AML/CFT through its Master Directions."
        ),
        "key_obligations": [
            "Separate client bank accounts mandatory — no mixing with firm funds",
            "SEBI: daily reconciliation of client money positions",
            "SEBI: prohibition on use of client funds for proprietary trading",
            "SEBI registration required to provide securities services",
            "RBI Master Direction on KYC — full AML/CFT compliance required",
        ],
    },
    # ── South Korea ───────────────────────────────────────────────────────────
    "South Korea": {
        "authority":   "Financial Services Commission (FSC) / Financial Supervisory Service (FSS)",
        "rule":        "Financial Investment Services and Capital Markets Act (FSCMA)",
        "full_name":   "FSCMA — Customer Asset Segregation",
        "uk_equiv":    "CASS 6 / CASS 7",
        "website":     "https://www.fsc.go.kr/en",
        "legislation_refs": [
            "Financial Investment Services and Capital Markets Act (FSCMA) 2009",
            "FSCMA — Article 74 (custody of customer assets by investment dealers/brokers)",
        ],
        "description": (
            "South Korea's FSC and FSS regulate capital markets under the FSCMA. "
            "Licensed investment dealers and brokers must segregate customer assets from "
            "proprietary assets. Regular reconciliation and reporting to the FSS is required."
        ),
        "key_obligations": [
            "FSCMA Article 74 — customer assets held separately from firm assets",
            "Licensed investment dealer or broker status required",
            "Regular reconciliation and FSS reporting",
            "Korea Investor Protection Fund — backstop for failed investment firms",
        ],
    },
    # ── New Zealand ───────────────────────────────────────────────────────────
    "New Zealand": {
        "authority":   "Financial Markets Authority (FMA)",
        "rule":        "Financial Markets Conduct Act 2013 (FMCA) — Client Money and Property Rules",
        "full_name":   "FMCA Client Money and Property Rules 2016",
        "uk_equiv":    "CASS 7 / CASS 6",
        "website":     "https://www.fma.govt.nz",
        "legislation_refs": [
            "Financial Markets Conduct Act 2013 (FMCA)",
            "Financial Markets Conduct (Client Money and Property) Rules 2016",
        ],
        "description": (
            "New Zealand's FMA requires FMC Act-licensed providers to hold client money and "
            "property in accordance with the Client Money and Property Rules 2016. "
            "Client money must be held in dedicated trust accounts. "
            "Rules closely align with ASIC's Australian framework."
        ),
        "key_obligations": [
            "Client money held in separate trust accounts — FMCA Client Money Rules 2016",
            "FMA licence required to provide managed investment or derivatives services",
            "Daily reconciliation of client money trust accounts",
        ],
    },
}

APAC_DEFAULT = {
    "authority":   "National Financial Supervisory Authority",
    "rule":        "National Regulatory Framework",
    "uk_equiv":    "CASS 7 (functional equivalent — varies by jurisdiction)",
    "description": (
        "Asia Pacific does not have a single, unified equivalent to UK CASS. Each territory "
        "enforces client asset protection through its own national financial regulator. "
        "Verify the specific national framework before holding or managing client assets "
        "in any APAC jurisdiction."
    ),
    "key_obligations": [
        "Verify national regulator authorisation for the entity",
        "Confirm customer asset segregation obligations under local law",
        "Assess adequacy of local investor protection schemes",
        "No single APAC equivalent to UK FSCS — protection varies by territory",
    ],
}


def is_apac(country_or_region: str) -> bool:
    """Return True if the country/region triggers Asia Pacific regulatory routing."""
    if not country_or_region:
        return False
    val = country_or_region.strip()
    if val in APAC_COUNTRIES:
        return True
    val_lower = val.lower()
    return any(kw in val_lower for kw in APAC_KEYWORDS)


def get_apac_country_regs(country: str) -> dict:
    """Return the APAC country-specific regulatory framework, or the regional default."""
    return APAC_REGS.get(country, APAC_DEFAULT)


def score_apac_client_money(data: dict) -> list:
    """
    Generate APAC-specific client money / customer asset segregation findings.
    Routes to the correct national framework based on data['country'].
    """
    findings = []
    country   = data.get("country", "Unknown")
    regs      = get_apac_country_regs(country)
    rule      = regs["rule"]
    authority = regs["authority"]

    # 1. Regulatory authorisation
    authorised = data.get("local_regulator_authorised")
    if authorised is not None:
        findings.append({
            "area":        f"Regulatory Authorisation ({country})",
            "rule":        rule,
            "description": f"Entity authorised by {authority}",
            "status":      "GREEN" if authorised else "RED",
            "commentary": (
                f"Entity confirmed authorised by {authority}. "
                f"Applicable framework: {rule}. UK equivalent: {regs['uk_equiv']}."
            ) if authorised else (
                f"CRITICAL: Entity does NOT hold authorisation from {authority}. "
                f"UK equivalent: operating without FCA authorisation — criminal offence under FSMA 2000."
            ),
        })

    # 2. Asset segregation
    segregated = data.get("all_accounts_designated")
    findings.append({
        "area":        f"Customer Asset Segregation ({country})",
        "rule":        rule,
        "description": f"Customer assets segregated per {authority} requirements",
        "status":      "GREEN" if segregated else "RED",
        "commentary": (
            f"Customer assets confirmed segregated per {rule} ({authority}). "
            f"UK equivalent: {regs['uk_equiv']}."
        ) if segregated else (
            f"Customer assets NOT confirmed segregated under {rule}. "
            f"Breach of {authority} requirements. UK equivalent: CASS 7 / CASS 6 failure."
        ),
    })

    # 3. Trust/safeguarding account structure
    ack = data.get("acknowledgement_letters_all_accounts")
    findings.append({
        "area":        f"Trust/Safeguarding Account Structure ({country})",
        "rule":        rule,
        "description": "Customer funds held in designated trust or safeguarding accounts",
        "status":      "GREEN" if ack is True else ("AMBER" if ack is None else "RED"),
        "commentary": (
            f"Trust/safeguarding account structure confirmed per {rule}. "
            "UK equivalent: CASS 7.17 designated client money account."
        ) if ack is True else (
            "Trust/safeguarding account confirmation not provided. "
            f"Verify structure meets {authority} requirements."
        ),
    })

    # 4. APAC investor protection note
    findings.append({
        "area":        f"Investor Protection Scheme ({country})",
        "rule":        "National Framework",
        "description": "Equivalent of UK FSCS backstop",
        "status":      "AMBER",
        "commentary": (
            "Asia Pacific does not have a single region-wide investor protection scheme equivalent "
            f"to the UK FSCS. In {country}, protection depends on the national framework supervised "
            f"by {authority}. Verify scope of any local investor compensation fund."
        ),
    })

    return findings


def score_apac_cross_border(country: str, data: dict) -> list:
    """Add APAC regulatory context to country risk findings."""
    findings = []
    regs    = get_apac_country_regs(country)
    purpose = data.get("purpose", "")

    if "client asset" in purpose.lower() or "cass" in purpose.lower() or "segregat" in purpose.lower():
        findings.append({
            "area":        f"APAC Regulatory Framework — Client Assets ({country})",
            "rule":        regs["rule"],
            "description": f"Customer asset protection framework — {country}",
            "status":      "AMBER",
            "commentary": (
                f"Cross-border client assets in {country} are governed by {regs['authority']} "
                f"under {regs['rule']}. {regs['description']} "
                "UK CASS protections do not apply extraterritorially. Confirm that local "
                "frameworks provide equivalent protection under CASS 6.3 / CASS 7.13."
            ),
        })

    findings.append({
        "area":        "No Unified APAC CASS Equivalent",
        "rule":        "CASS 6.3 / CASS 7.13",
        "description": "Region-wide client asset protection — Asia Pacific",
        "status":      "AMBER",
        "commentary": (
            "Asia Pacific has no single region-wide CASS equivalent — each territory has its own "
            "jurisdiction-specific laws and regulatory body. Key frameworks: "
            "Hong Kong — SFC Securities and Futures (Client Money) Rules Cap. 571I / (Client Securities) Rules Cap. 571H; "
            "Singapore — MAS SFA Section 104 + SFLCBR (trust accounts by next business day, daily computations); "
            "Australia — Corporations Act 2001 Division 2 of Part 7.8 + ASIC Client Money Reporting Rules; "
            "Japan — FIEA Article 43-2 (mandatory asset separation). "
            "FCA-authorised firms must verify country-by-country equivalent protections per CASS 6.3 / 7.13."
        ),
    })

    return findings


def uk_apac_comparison_table() -> list:
    """Return (UK rule, APAC equivalent) rows for a UK CASS vs APAC comparison narrative."""
    return [
        ("CASS 7 — Client Money",            "HK: SFC Client Money Rules | AU: Corporations Act s981B | SG: MAS SFA/PSA safeguarding | JP: FIEA"),
        ("CASS 6 — Custody Assets",          "HK: SFC Client Securities Rules | AU: AFSL conditions | SG: MAS SFA | JP: FIEA separation"),
        ("CASS 7.13.4R — Daily reconciliation","Varies: HK/SG/JP require regular reconciliation; AU: ASIC Client Money Reporting Rules"),
        ("CASS 7.18.3R — Acknowledgements",  "HK: trust account confirmations; AU: authorised deposit-taking institution letters"),
        ("FSCS — Customer backstop",         "HK: Investor Compensation Fund | AU: ASIC / FCS | SG: no universal scheme | JP: Investor Protection Fund"),
        ("FCA CASS Oversight Function",      "SFC (HK) | ASIC (AU) | MAS (SG) | FSA (JP)"),
        ("CASS 6.3 — Third-party custody",   "Applies to UK firms — local APAC framework must provide equivalent protection"),
    ]


# ══════════════════════════════════════════════════════════════════════════════
# UNIFIED REGION DETECTOR
# ══════════════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════════════
# OFFICIAL REGULATORY WEBSITES — ALL REGIONS
# ══════════════════════════════════════════════════════════════════════════════

REGULATORY_WEBSITES = {
    # ── UK (baseline) ─────────────────────────────────────────────────────────
    "FCA":           "https://www.fca.org.uk",
    "PRA":           "https://www.bankofengland.co.uk/prudential-regulation",
    "FOS":           "https://www.financial-ombudsman.org.uk",
    "FSCS":          "https://www.fscs.org.uk",
    "HM Treasury":   "https://www.gov.uk/government/organisations/hm-treasury",
    "OFSI":          "https://www.gov.uk/government/organisations/office-of-financial-sanctions-implementation",

    # ── North America ──────────────────────────────────────────────────────────
    "SEC":           "https://www.sec.gov",
    "CFTC":          "https://www.cftc.gov",
    "SIPC":          "https://www.sipc.org",
    "FINRA":         "https://www.finra.org",
    "Federal Reserve": "https://www.federalreserve.gov",
    "OCC":           "https://www.occ.gov",
    "FDIC":          "https://www.fdic.gov",
    "CFPB":          "https://www.consumerfinance.gov",
    "OSFI (Canada)": "https://www.osfi-bsif.gc.ca",
    "CIRO (Canada)": "https://www.ciro.ca",
    "CNBV (Mexico)": "https://www.cnbv.gob.mx",

    # ── Latin America ──────────────────────────────────────────────────────────
    "BCB (Brazil)":  "https://www.bcb.gov.br",
    "CVM (Brazil)":  "https://www.gov.br/cvm",
    "BCRA (Argentina)":"https://www.bcra.gob.ar",
    "CNV (Argentina)":  "https://www.argentina.gob.ar/cnv",
    "Banxico (Mexico)": "https://www.banxico.org.mx",
    "CMF (Chile)":   "https://www.cmfchile.cl",
    "SFC (Colombia)":"https://www.superfinanciera.gov.co",
    "BCRP (Peru)":   "https://www.bcrp.gob.pe",
    "SMV (Peru)":    "https://www.smv.gob.pe",
    "BCU (Uruguay)": "https://www.bcu.gub.uy",

    # ── Asia Pacific ───────────────────────────────────────────────────────────
    "SFC (Hong Kong)":  "https://www.sfc.hk",
    "HKMA":             "https://www.hkma.gov.hk",
    "ASIC":             "https://www.asic.gov.au",
    "APRA":             "https://www.apra.gov.au",
    "AUSTRAC":          "https://www.austrac.gov.au",
    "MAS (Singapore)":  "https://www.mas.gov.sg",
    "FSA (Japan)":      "https://www.fsa.go.jp/en",
    "BOJ":              "https://www.boj.or.jp/en",
    "SEBI (India)":     "https://www.sebi.gov.in",
    "RBI (India)":      "https://www.rbi.org.in",
    "FSC (South Korea)":"https://www.fsc.go.kr/en",
    "FSS (South Korea)":"https://www.fss.or.kr/eng",
    "SC (Malaysia)":    "https://www.sc.com.my",
    "BNM (Malaysia)":   "https://www.bnm.gov.my",
    "SEC (Thailand)":   "https://www.sec.or.th/en",
    "OJK (Indonesia)":  "https://www.ojk.go.id/en",
    "SEC (Philippines)":"https://www.sec.gov.ph",
    "FMC (New Zealand)":"https://www.fma.govt.nz",
    "RBNZ":             "https://www.rbnz.govt.nz",

    # ── Europe ────────────────────────────────────────────────────────────────
    "ESMA":             "https://www.esma.europa.eu",
    "EBA":              "https://www.eba.europa.eu",
    "EIOPA":            "https://www.eiopa.europa.eu",
    "ECB Banking Supervision": "https://www.bankingsupervision.europa.eu",
    "BaFin (Germany)":  "https://www.bafin.de",
    "AMF (France)":     "https://www.amf-france.org",
    "ACPR (France)":    "https://acpr.banque-france.fr",
    "AFM (Netherlands)":"https://www.afm.nl/en",
    "DNB (Netherlands)":"https://www.dnb.nl/en",
    "CONSOB (Italy)":   "https://www.consob.it/web/consob-and-its-activities/home",
    "CBI (Ireland)":    "https://www.centralbank.ie",
    "FINMA (Switzerland)": "https://www.finma.ch/en",
    "CNMV (Spain)":     "https://www.cnmv.es/portal/home.aspx",
    "FSA (Sweden)":     "https://www.fi.se/en",
    "FIN-FSA (Finland)":"https://www.finanssivalvonta.fi/en",
    "KNF (Poland)":     "https://www.knf.gov.pl/en",
    "CySEC (Cyprus)":   "https://www.cysec.gov.cy/en-GB/home",
    "MFSA (Malta)":     "https://www.mfsa.mt",
    "CSSF (Luxembourg)":"https://www.cssf.lu/en",

    # ── Africa ────────────────────────────────────────────────────────────────
    "FSCA (South Africa)":  "https://www.fsca.co.za",
    "SARB":                 "https://www.resbank.co.za",
    "JSE":                  "https://www.jse.co.za",
    "SEC Nigeria":          "https://sec.gov.ng",
    "CBN":                  "https://www.cbn.gov.ng",
    "CMA (Kenya)":          "https://www.cma.or.ke",
    "CBK":                  "https://www.centralbank.go.ke",
    "EFSA (Egypt)":         "https://www.efsa.gov.eg",
    "CBE":                  "https://www.cbe.org.eg",
    "SEC Ghana":            "https://www.sec.gov.gh",
    "BOG":                  "https://www.bog.gov.gh",
    "FSC (Mauritius)":      "https://www.fscmauritius.org",
    "BOM (Mauritius)":      "https://www.bom.mu",
    "CMSA (Tanzania)":      "https://www.cmsa.go.tz",
    "SEC (Zimbabwe)":       "https://www.secz.co.zw",
    "BVMAC (CEMAC)":        "https://www.bvmac.net",
}


# ══════════════════════════════════════════════════════════════════════════════
# EUROPE REGIONAL ROUTING (Financial Services — MiFID II / EMIR / ESMA)
# ══════════════════════════════════════════════════════════════════════════════

EUROPE_COUNTRIES = {
    "Germany", "France", "Italy", "Spain", "Netherlands", "Belgium", "Sweden",
    "Poland", "Denmark", "Finland", "Norway", "Switzerland", "Ireland",
    "Luxembourg", "Austria", "Portugal", "Greece", "Czech Republic", "Hungary",
    "Romania", "Bulgaria", "Croatia", "Cyprus", "Malta", "Slovakia", "Slovenia",
    "Estonia", "Latvia", "Lithuania", "Iceland", "Liechtenstein",
}

EUROPE_KEYWORDS = ("europe", "european union", "eu ", " eu", "eea", "eurozone",
                   "mifid", "esma", "eba ", "emir")

EUROPE_REGS = {
    "EU": {
        "authority":   "ESMA (European Securities and Markets Authority) / National Competent Authorities (NCAs)",
        "rule":        "MiFID II (2014/65/EU) / Delegated Regulation (EU) 2017/593 / PSD2 (2015/2366/EU) / EMD2 (2009/110/EC)",
        "full_name":   "EU Financial Services Regulatory Framework",
        "uk_equiv":    "FCA rules / CASS 6 / CASS 7 / PSRs 2017 (for payment safeguarding)",
        "website":     "https://www.esma.europa.eu",
        "description": (
            "The EU equivalent of UK CASS is primarily MiFID II Article 16 + Delegated Regulation "
            "(EU) 2017/593 for investment firms. For payment institutions and e-money institutions, "
            "PSD2 (transitioning to PSD3 / EMAR) and the E-Money Directive (EMD2) require "
            "safeguarding of client funds either in segregated bank accounts or covered by an "
            "insurance policy or comparable guarantee. "
            "KEY DIFFERENCE from UK CASS: The EU framework is implemented via high-level Directives "
            "transposed into national law — it is less prescriptive and granular than the UK CASS "
            "Sourcebook. Most EU jurisdictions rely on statutory segregation and regulatory priority "
            "rules under civil/commercial law rather than the UK's statutory trust mechanism. "
            "There is no single EU-wide equivalent to CASS 10 resolution pack."
        ),
        "key_obligations": [
            "MiFID II Article 16 + Delegated Reg (EU) 2017/593 — segregation of client funds and instruments from firm assets",
            "Prohibition on title transfer collateral arrangements (TTCAs) for retail clients — mirrors CASS 7 prohibition",
            "Due diligence on credit institutions holding client funds — equivalent to CASS 7.13",
            "Record-keeping of client assets — equivalent to CASS 6/7 register requirements",
            "MiFID II Article 16(9) — explicit written consent required to use client instruments for own account",
            "PSD2 / PSD3 — payment institutions must segregate client funds in dedicated bank accounts OR insurance",
            "EMD2 — e-money institutions must safeguard funds equivalent to outstanding e-money",
            "EMIR — mandatory clearing and reporting of OTC derivatives",
            "CRD V / BRRD — bail-in and resolution framework for banks",
            "GDPR — data protection applicable across all EU financial services",
        ],
        "cass_comparison": (
            "UK CASS vs EU MiFID II: UK CASS is a detailed, standalone rulebook with granular "
            "rules on reconciliation frequency, acknowledgement letters, diversification, and CASS "
            "resolution packs (CASS 10). UK CASS uses statutory trust to protect client money on "
            "insolvency — the most robust legal protection. EU MiFID II relies on statutory "
            "segregation under civil law — functionally similar but with no trust mechanism, "
            "no single prescribed resolution pack standard, and varying enforcement quality "
            "across member states. Post-Brexit, UK firms cannot rely on UK CASS extraterritorially "
            "for EU-based assets; MiFID II Article 16 equivalent protections must be verified."
        ),
    },
    "Germany": {
        "authority":   "BaFin (Bundesanstalt für Finanzdienstleistungsaufsicht)",
        "rule":        "MiFID II / WpHG (Securities Trading Act) / KWG (Banking Act)",
        "uk_equiv":    "FCA / PRA",
        "website":     "https://www.bafin.de",
        "description": (
            "BaFin supervises banks, insurance companies, and financial services in Germany. "
            "Client asset protection is governed by MiFID II implemented through WpHG. "
            "BaFin enforces strict segregation requirements and conducts supervisory reviews."
        ),
    },
    "France": {
        "authority":   "AMF (Autorité des marchés financiers) / ACPR",
        "rule":        "MiFID II / Code monétaire et financier",
        "uk_equiv":    "FCA / PRA",
        "website":     "https://www.amf-france.org",
        "description": (
            "The AMF regulates financial markets and investment services in France. "
            "ACPR (Autorité de contrôle prudentiel et de résolution) supervises banks and insurers. "
            "Client asset protection follows MiFID II implemented through the French Monetary and Financial Code."
        ),
    },
    "Ireland": {
        "authority":   "Central Bank of Ireland (CBI)",
        "rule":        "MiFID II / Central Bank Acts / Client Asset Regulations 2015",
        "uk_equiv":    "FCA / CASS",
        "website":     "https://www.centralbank.ie",
        "description": (
            "The CBI is Ireland's prudential and conduct regulator. Ireland's Client Asset "
            "Regulations 2015 (S.I. No. 384 of 2015) closely mirror UK CASS, requiring "
            "segregation of client money and assets. A popular domicile for EU-passported "
            "financial services post-Brexit."
        ),
    },
    "Luxembourg": {
        "authority":   "CSSF (Commission de Surveillance du Secteur Financier)",
        "rule":        "MiFID II / Luxembourg Fund Law / UCITS Directive",
        "uk_equiv":    "FCA / CASS",
        "website":     "https://www.cssf.lu/en",
        "description": (
            "CSSF supervises Luxembourg's financial sector, including investment funds, banks, "
            "and payment institutions. Luxembourg is the world's second largest fund domicile. "
            "Client asset protection follows MiFID II and UCITS frameworks."
        ),
    },
    "Switzerland": {
        "authority":   "FINMA (Swiss Financial Market Supervisory Authority)",
        "rule":        "FinSA (Financial Services Act) / FinIA (Financial Institutions Act) / FMIA",
        "uk_equiv":    "FCA",
        "website":     "https://www.finma.ch/en",
        "description": (
            "FINMA supervises Swiss banks, securities dealers, and fund managers. "
            "Switzerland's FinSA/FinIA framework (effective 2020) modernised conduct rules "
            "and aligns with MiFID II principles for client protection, though Switzerland "
            "is not an EU member and has its own distinct legal framework."
        ),
    },
}

EUROPE_DEFAULT = {
    "authority":   "National Competent Authority (NCA) / ESMA",
    "rule":        "MiFID II (2014/65/EU) / National Implementation",
    "uk_equiv":    "FCA / CASS",
    "website":     "https://www.esma.europa.eu",
    "description": (
        "EU member states implement MiFID II through national law supervised by their NCA. "
        "Client asset segregation requirements under MiFID II Article 16 are broadly equivalent "
        "to UK CASS in purpose. Verify the specific NCA for the member state in question."
    ),
    "key_obligations": [
        "MiFID II Article 16 — client asset segregation from firm assets",
        "Prohibition on using client assets for firm's own account without explicit consent",
        "Regular reconciliation of client asset positions",
        "NCA authorisation required to hold or manage client assets",
    ],
}


def is_europe(country_or_region: str) -> bool:
    if not country_or_region:
        return False
    val = country_or_region.strip()
    if val in EUROPE_COUNTRIES:
        return True
    return any(kw in val.lower() for kw in EUROPE_KEYWORDS)


def get_europe_country_regs(country: str) -> dict:
    return EUROPE_REGS.get(country, EUROPE_REGS.get("EU", EUROPE_DEFAULT))


def score_europe_cross_border(country: str, data: dict) -> list:
    findings = []
    regs    = get_europe_country_regs(country)
    purpose = data.get("purpose", "")

    if "client asset" in purpose.lower() or "cass" in purpose.lower() or "segregat" in purpose.lower():
        findings.append({
            "area":        f"EU/Europe Regulatory Framework — Client Assets ({country})",
            "rule":        regs["rule"],
            "description": f"Client asset protection framework — {country}",
            "status":      "AMBER",
            "commentary": (
                f"Cross-border client assets in {country} are governed by {regs['authority']} "
                f"under {regs['rule']}. {regs['description']} "
                f"Official regulator: {regs.get('website', 'see ESMA — https://www.esma.europa.eu')}. "
                "UK CASS protections do not apply in EU jurisdictions post-Brexit. Confirm MiFID II "
                "Article 16 equivalent protections are in place."
            ),
        })
    return findings


def score_europe_client_money(data: dict) -> list:
    findings = []
    country  = data.get("country", "Unknown")
    regs     = get_europe_country_regs(country)
    rule     = regs["rule"]
    authority = regs["authority"]

    segregated = data.get("all_accounts_designated")
    findings.append({
        "area":        f"Client Asset Segregation — MiFID II ({country})",
        "rule":        rule,
        "description": f"Client assets segregated per MiFID II / {authority}",
        "status":      "GREEN" if segregated else "RED",
        "commentary": (
            f"Client assets confirmed segregated per {rule}. Supervised by {authority}. "
            f"UK equivalent: CASS 6 / CASS 7. Regulator: {regs.get('website', '')}."
        ) if segregated else (
            f"Client assets NOT confirmed segregated under {rule}. "
            f"Potential MiFID II Article 16 breach. Supervised by {authority}."
        ),
    })
    return findings


def europe_regulatory_refs() -> list:
    return [
        ("ESMA — EU Securities & Markets Authority",     "https://www.esma.europa.eu"),
        ("EBA — EU Banking Authority",                   "https://www.eba.europa.eu"),
        ("ECB Banking Supervision",                      "https://www.bankingsupervision.europa.eu"),
        ("MiFID II — Client Asset Segregation Art. 16",  "Directive 2014/65/EU — equivalent to UK CASS 6/7"),
        ("EMIR — OTC Derivatives Reporting/Clearing",    "Regulation (EU) 648/2012"),
        ("BaFin (Germany)",                              "https://www.bafin.de"),
        ("AMF (France)",                                 "https://www.amf-france.org"),
        ("CBI (Ireland) — Client Asset Regs 2015",       "https://www.centralbank.ie"),
        ("CSSF (Luxembourg)",                            "https://www.cssf.lu/en"),
        ("FINMA (Switzerland)",                          "https://www.finma.ch/en"),
        ("CNMV (Spain)",                                 "https://www.cnmv.es"),
        ("AFM (Netherlands)",                            "https://www.afm.nl/en"),
    ]


# ══════════════════════════════════════════════════════════════════════════════
# AFRICA REGIONAL ROUTING
# ══════════════════════════════════════════════════════════════════════════════

AFRICA_COUNTRIES = {
    "South Africa", "Nigeria", "Kenya", "Egypt", "Ghana", "Ethiopia",
    "Tanzania", "Uganda", "Rwanda", "Zambia", "Zimbabwe", "Mozambique",
    "Botswana", "Namibia", "Mauritius", "Senegal", "Côte d'Ivoire",
    "Ivory Coast", "Morocco", "Tunisia", "Algeria", "Angola",
    "Democratic Republic of Congo", "DRC", "Cameroon", "Mali",
    "Burkina Faso", "Niger", "Benin", "Togo", "Guinea-Bissau",
    "Gabon", "Republic of Congo", "Central African Republic", "Chad",
    "Equatorial Guinea",
    # Regional blocs
    "WAEMU", "CEMAC", "COMESA", "SADC", "EAC", "ECOWAS",
}

AFRICA_KEYWORDS = ("africa", "sub-saharan", "sadc", "ecowas", "comesa", "east africa",
                   "west africa", "southern africa", "north africa", "waemu", "cemac",
                   "beac", "bceao", "esaamlg", "giaba", "gabac")

AFRICA_REGS = {
    # ── South Africa ──────────────────────────────────────────────────────────
    "South Africa": {
        "authority":   "FSCA (Financial Sector Conduct Authority) / Prudential Authority (PA) under SARB",
        "rule":        "Financial Advisory and Intermediary Services Act (FAIS Act) / Financial Markets Act 19 of 2012 / Financial Sector Regulation Act 9 of 2017 / COFI Bill (pending)",
        "full_name":   "South Africa Twin Peaks — FSCA (conduct) + PA/SARB (prudential)",
        "uk_equiv":    "FCA (FSCA) / PRA (Prudential Authority) / CASS (FAIS + Financial Markets Act)",
        "website":     "https://www.fsca.co.za",
        "sarb_website":"https://www.resbank.co.za",
        "legislation_refs": [
            "Financial Advisory and Intermediary Services (FAIS) Act 37 of 2002 — client asset protection for FSPs",
            "Financial Markets Act 19 of 2012 — custody of client securities, segregation obligations",
            "Financial Sector Regulation Act 9 of 2017 — Twin Peaks framework (FSCA + PA)",
            "COFI Bill (Conduct of Financial Institutions) — consolidates conduct rules incl. 'trust property' and client asset protection into one market-conduct framework (pending enactment)",
            "Financial Intelligence Centre Act (FICA) — AML/CFT obligations",
        ],
        "description": (
            "South Africa has the most developed financial regulatory framework on the continent, "
            "operating a Twin Peaks model that closely mirrors the UK FCA/PRA structure. "
            "The FSCA (conduct regulator) and the Prudential Authority (PA, housed within SARB) "
            "are the primary regulators. Client asset protection for licensed Financial Services "
            "Providers (FSPs) is governed by the FAIS Act (conduct) and the Financial Markets Act "
            "(custody and segregation of securities). "
            "The COFI Bill — when enacted — will consolidate conduct-of-business rules across all "
            "sectors into a single market-conduct framework, explicitly codifying 'trust property' "
            "and client asset protection obligations equivalent to UK CASS principles. "
            "The FSCS equivalent in South Africa is the Financial Sector Conduct Authority guarantee — "
            "no single national compensation scheme equivalent to the UK FSCS currently exists."
        ),
        "key_obligations": [
            "FSCA authorisation required for all financial services providers under the FAIS Act",
            "Financial Markets Act — client securities must be held in segregated custody accounts",
            "FAIS Act — client money treated as 'trust property' — cannot be commingled with firm assets",
            "COFI Bill — when enacted, will formally codify client asset protection rules akin to CASS",
            "Twin Peaks: SARB/PA (prudential, capital) + FSCA (market conduct) — mirrors UK PRA/FCA",
            "FICA — full AML/CFT compliance including FATF Recommendations for all FSPs",
            "Treating Customers Fairly (TCF) framework — conduct standard equivalent to FCA Principles",
        ],
    },
    # ── Nigeria ───────────────────────────────────────────────────────────────
    "Nigeria": {
        "authority":   "SEC Nigeria / CBN (Central Bank of Nigeria)",
        "rule":        "Investments and Securities Act (ISA) 2007 (revised 2024/2025) / CBN Guidelines / NFIU AML Rules",
        "uk_equiv":    "FCA / PRA",
        "website":     "https://sec.gov.ng",
        "cbn_website": "https://www.cbn.gov.ng",
        "legislation_refs": [
            "Investments and Securities Act (ISA) — capital markets regulation and client asset rules",
            "CBN Guidelines on Electronic Payment and Fintech Services",
            "NFIU (Nigerian Financial Intelligence Unit) — SAR and AML/CFT obligations",
            "GIABA (FATF body for West Africa) — AML/CFT standards for the region",
        ],
        "description": (
            "Nigeria's SEC regulates the capital markets (securities, investment funds) under the "
            "Investments and Securities Act (ISA). The CBN regulates banks and payment service providers. "
            "Client asset protection for broker-dealers requires segregation of client money in "
            "designated trust accounts. The ISA 2025 revision strengthens digital asset rules. "
            "GIABA coordinates West African AML compliance across 16 member nations."
        ),
        "key_obligations": [
            "SEC Nigeria registration required for all capital market operators",
            "Client money segregation in designated trust accounts — SEC Rules",
            "CBN licensing required for banks and payment service providers",
            "AML/CFT compliance under SCUML (Special Control Unit for Money Laundering)",
            "NFIU — SAR filing obligations and suspicious transaction reporting",
            "GIABA mutual evaluation compliance for AML/CFT standards",
        ],
    },
    # ── Kenya ─────────────────────────────────────────────────────────────────
    "Kenya": {
        "authority":   "CMA Kenya (Capital Markets Authority) / CBK (Central Bank of Kenya)",
        "rule":        "Capital Markets Act (Cap. 485A) / CBK Act / National Payment System Act",
        "uk_equiv":    "FCA / PRA",
        "website":     "https://www.cma.or.ke",
        "cbk_website": "https://www.centralbank.go.ke",
        "legislation_refs": [
            "Capital Markets Act (Cap. 485A) — securities market regulation and client fund protection",
            "CMA Collective Investment Scheme Rules — segregation of client funds from operator funds",
            "National Payment System Act — CBK supervision of payment service providers",
            "ESAAMLG (Eastern & Southern Africa Anti-Money Laundering Group) — AML/CFT standards",
            "Proceeds of Crime and Anti-Money Laundering Act (POCAMLA) — AML obligations",
        ],
        "description": (
            "The CMA regulates Kenya's capital markets, including stockbrokers, fund managers, "
            "and investment banks. The CBK regulates commercial banks, microfinance banks, and "
            "payment service providers. The ESAAMLG coordinates AML compliance across East and "
            "Southern Africa."
        ),
        "key_obligations": [
            "CMA authorisation required for capital market intermediaries",
            "CMA Rules — client funds segregated from operator funds in designated accounts",
            "CBK licensing required for banking and payment services",
            "POCAMLA — AML/CFT compliance obligations",
            "ESAAMLG mutual evaluation compliance requirements",
        ],
    },
    # ── Ghana ─────────────────────────────────────────────────────────────────
    "Ghana": {
        "authority":   "SEC Ghana (Securities and Exchange Commission) / BOG (Bank of Ghana)",
        "rule":        "Securities Industry Act 2016 (Act 929) / Banks and Specialised Deposit-Taking Institutions Act 2016 (Act 930)",
        "uk_equiv":    "FCA / PRA",
        "website":     "https://www.sec.gov.gh",
        "bog_website": "https://www.bog.gov.gh",
        "legislation_refs": [
            "Securities Industry Act 2016 (Act 929) — investment dealer and fund manager regulation",
            "Banks and Specialised Deposit-Taking Institutions Act 2016 (Act 930) — banking regulation",
            "Anti-Money Laundering Act 2020 (Act 1044)",
            "GIABA — West African AML/CFT coordination",
        ],
        "description": (
            "Ghana's SEC regulates investment dealers, fund managers, and stockbrokers under the "
            "Securities Industry Act 2016. The Bank of Ghana supervises banks and specialised "
            "deposit-taking institutions. Client asset segregation is required for licensed "
            "capital market operators. GIABA coordinates West African AML compliance."
        ),
        "key_obligations": [
            "SEC Ghana licence required for investment and capital market services",
            "Client asset segregation from operator funds — SEC Ghana Rules",
            "BOG licence required for banking and payment services",
            "AML/CFT obligations under Anti-Money Laundering Act 2020",
            "GIABA mutual evaluation compliance",
        ],
    },
    # ── Mauritius ─────────────────────────────────────────────────────────────
    "Mauritius": {
        "authority":   "FSC Mauritius (Financial Services Commission) / BOM (Bank of Mauritius)",
        "rule":        "Securities Act 2005 / Financial Services Act 2007 / Banking Act 2004 / VAITOS Act (digital assets)",
        "uk_equiv":    "FCA / PRA",
        "website":     "https://www.fscmauritius.org",
        "bom_website": "https://www.bom.mu",
        "legislation_refs": [
            "Securities Act 2005 — client asset segregation for securities firms",
            "Financial Services Act 2007 — FSC licensing for investment dealers and fund managers",
            "Banking Act 2004 — BOM licensing for banking operations",
            "Virtual Asset and Initial Token Offering Services (VAITOS) Act — digital asset regulation and client safeguarding",
            "FATF/ESAAMLG — AML/CFT compliance obligations",
        ],
        "description": (
            "Mauritius is a major African financial gateway with one of the continent's most "
            "sophisticated regulatory frameworks. The FSC regulates non-banking financial services "
            "including securities, fund management, and global business licences. The BOM supervises "
            "banks. Mauritius enforces strict client asset safeguarding and AML/CFT rules. "
            "The VAITOS Act specifically governs digital asset service providers, including client "
            "asset safeguarding rules for virtual asset custodians and exchanges — one of the most "
            "developed digital asset frameworks in Africa."
        ),
        "key_obligations": [
            "FSC licence required for investment dealers, fund managers, and global business companies",
            "Client asset segregation required under Securities Act 2005",
            "BOM licence required for banking operations",
            "VAITOS Act — digital asset custodians must segregate client virtual assets from firm assets",
            "Strong AML/CFT framework — FATF/ESAAMLG compliant",
        ],
    },
    # ── Egypt ─────────────────────────────────────────────────────────────────
    "Egypt": {
        "authority":   "EFSA (Egyptian Financial Supervisory Authority) / CBE (Central Bank of Egypt)",
        "rule":        "Capital Market Law No. 95 of 1992 / Banking Law No. 194 of 2020",
        "uk_equiv":    "FCA / PRA",
        "website":     "https://www.efsa.gov.eg",
        "cbe_website": "https://www.cbe.org.eg",
        "legislation_refs": [
            "Capital Market Law No. 95 of 1992 (amended) — securities market regulation",
            "Banking Law No. 194 of 2020 — CBE banking supervision",
            "AML Law No. 80 of 2002 (amended) — AML/CFT — EGMONT Group member",
        ],
        "description": (
            "The EFSA supervises Egypt's non-banking financial sector including securities markets, "
            "insurance, and mortgage finance. The CBE regulates banks and payment systems. "
            "Egypt's Capital Market Law governs client asset protection for licensed securities intermediaries."
        ),
        "key_obligations": [
            "EFSA licence required for capital market intermediaries",
            "Client fund segregation for licensed brokers and investment firms",
            "CBE licence required for banking and payment services",
            "AML/CFT compliance — Egypt's AML Law — EGMONT Group and MENAFATF member",
        ],
    },
    # ── Regional Blocs ────────────────────────────────────────────────────────
    "WAEMU": {
        "authority":   "BCEAO (Central Bank of West African States) / CREPMF",
        "rule":        "WAEMU (West African Economic and Monetary Union) financial regulations / BCEAO banking rules",
        "uk_equiv":    "ECB/EBA (functional — regional bloc model)",
        "website":     "https://www.bceao.int",
        "description": (
            "WAEMU covers 8 West African francophone countries (Benin, Burkina Faso, Côte d'Ivoire, "
            "Guinea-Bissau, Mali, Niger, Senegal, Togo). The BCEAO sets commercial banking and "
            "deposit-segregation rules across all member states. The CREPMF regulates capital markets "
            "in the region. Client asset protection rules are set at BCEAO/CREPMF level."
        ),
        "key_obligations": [
            "BCEAO banking licence required for commercial banking operations in WAEMU states",
            "CREPMF approval required for capital market operations in the region",
            "Deposit segregation rules set by BCEAO apply across all 8 member states",
            "GIABA — AML/CFT standards and mutual evaluations for WAEMU members",
        ],
    },
    "CEMAC": {
        "authority":   "BEAC (Banque des États de l'Afrique Centrale) / COSUMAF",
        "rule":        "CEMAC (Central African Economic and Monetary Community) banking regulations",
        "uk_equiv":    "ECB/EBA (functional — regional bloc model)",
        "website":     "https://www.beac.int",
        "description": (
            "CEMAC covers 6 Central African states (Cameroon, Central African Republic, Chad, "
            "Republic of Congo, Equatorial Guinea, Gabon). The BEAC (Banque des États de l'Afrique "
            "Centrale) sets banking and deposit-segregation rules across the region. "
            "COSUMAF regulates financial markets across CEMAC member states."
        ),
        "key_obligations": [
            "BEAC licence required for banking operations in CEMAC states",
            "COSUMAF approval required for capital market operations",
            "GABAC — AML/CFT coordination body for Central Africa",
        ],
    },
    "COMESA": {
        "authority":   "COMESA (Common Market for Eastern and Southern Africa) member state regulators",
        "rule":        "National frameworks of 21 member states — no single unified rulebook",
        "uk_equiv":    "No direct equivalent — country-by-country assessment required",
        "website":     "https://www.comesa.int",
        "description": (
            "COMESA covers 21 East and Southern African member states. Unlike WAEMU/CEMAC, COMESA "
            "does not operate a monetary union or a single banking regulator — each member state "
            "retains its own national regulatory framework. ESAAMLG coordinates AML/CFT standards "
            "across Eastern and Southern Africa. Country-by-country due diligence is required."
        ),
        "key_obligations": [
            "Country-specific national regulator authorisation required in each COMESA state",
            "ESAAMLG mutual evaluation compliance for AML/CFT",
            "No single CASS equivalent — verify national framework for each country",
        ],
    },
}

AFRICA_DEFAULT = {
    "authority":   "National Central Bank / National Financial Regulatory Authority",
    "rule":        "National Securities / Financial Services Legislation",
    "uk_equiv":    "FCA (functional equivalent — varies significantly by country)",
    "website":     "Verify at national regulator website",
    "description": (
        "African financial regulation varies significantly by country. There is no single "
        "continent-wide equivalent to UK CASS or EU MiFID II. Most countries regulate "
        "client asset protection through a national securities regulator (capital markets) "
        "and central bank (banking/payments) operating independently. Quality and enforcement "
        "of client asset protection rules vary materially across the continent."
    ),
    "key_obligations": [
        "Verify national regulator authorisation for counterparty/entity",
        "Confirm client fund segregation obligations under local securities law",
        "Assess existence and scope of local investor protection scheme",
        "No single Africa-wide CASS or FSCS equivalent",
        "AML/CFT compliance varies — check FATF/GIABA/ESAAMLG membership status",
    ],
}


def is_africa(country_or_region: str) -> bool:
    if not country_or_region:
        return False
    val = country_or_region.strip()
    if val in AFRICA_COUNTRIES:
        return True
    return any(kw in val.lower() for kw in AFRICA_KEYWORDS)


def get_africa_country_regs(country: str) -> dict:
    return AFRICA_REGS.get(country, AFRICA_DEFAULT)


def score_africa_cross_border(country: str, data: dict) -> list:
    findings = []
    regs    = get_africa_country_regs(country)
    purpose = data.get("purpose", "")

    if "client asset" in purpose.lower() or "cass" in purpose.lower() or "segregat" in purpose.lower():
        findings.append({
            "area":        f"Africa Regulatory Framework — Client Assets ({country})",
            "rule":        regs["rule"],
            "description": f"Client asset protection framework — {country}",
            "status":      "AMBER",
            "commentary": (
                f"Cross-border client assets in {country} are governed by {regs['authority']} "
                f"under {regs['rule']}. {regs['description']} "
                f"Official regulator: {regs.get('website', 'verify at national regulator')}. "
                "UK CASS protections do not apply extraterritorially. Confirm local segregation "
                "standards meet the equivalent protection test under CASS 6.3 / CASS 7.13."
            ),
        })

    findings.append({
        "area":        "No Unified Africa CASS Equivalent",
        "rule":        "CASS 6.3 / CASS 7.13",
        "description": "Region-wide client asset protection — Africa (54 sovereign nations)",
        "status":      "AMBER",
        "commentary": (
            "Africa has no single continent-wide client asset protection equivalent to UK CASS — "
            "regulation is at national or regional-bloc level across 54 sovereign nations. "
            "Key frameworks by jurisdiction: "
            "South Africa — FSCA/Prudential Authority (SARB) Twin Peaks (closest to FCA/PRA model); "
            "FAIS Act (client assets as 'trust property') + Financial Markets Act (securities custody). "
            "COFI Bill (pending) will consolidate into a single market-conduct framework akin to FCA Handbook. "
            "Mauritius — FSC: strict client safeguarding; VAITOS Act: digital asset client rules. "
            "Nigeria — SEC Nigeria / CBN; GIABA (West Africa AML/CFT body). "
            "Kenya — CMA / CBK; ESAAMLG (East/Southern Africa AML body). "
            "Regional blocs: WAEMU/BCEAO (8 West African francophone states), CEMAC/BEAC (6 Central African states). "
            "FCA-authorised firms must conduct country-by-country due diligence per CASS 6.3 / CASS 7.13."
        ),
    })
    return findings


def score_africa_client_money(data: dict) -> list:
    findings = []
    country   = data.get("country", "Unknown")
    regs      = get_africa_country_regs(country)
    rule      = regs["rule"]
    authority = regs["authority"]

    authorised = data.get("local_regulator_authorised")
    if authorised is not None:
        findings.append({
            "area":        f"Regulatory Authorisation ({country})",
            "rule":        rule,
            "description": f"Entity authorised by {authority}",
            "status":      "GREEN" if authorised else "RED",
            "commentary": (
                f"Entity confirmed authorised by {authority}. "
                f"Applicable framework: {rule}. Regulator: {regs.get('website', '')}. "
                f"UK equivalent: {regs['uk_equiv']}."
            ) if authorised else (
                f"CRITICAL: Entity NOT authorised by {authority}. "
                f"UK equivalent: operating without FCA authorisation."
            ),
        })

    segregated = data.get("all_accounts_designated")
    findings.append({
        "area":        f"Client Fund Segregation ({country})",
        "rule":        rule,
        "description": f"Client funds segregated per {authority} requirements",
        "status":      "GREEN" if segregated else "RED",
        "commentary": (
            f"Client funds confirmed segregated per {rule} ({authority}). "
            f"UK equivalent: {regs['uk_equiv']}."
        ) if segregated else (
            f"Client funds NOT segregated under {rule}. "
            f"UK equivalent: CASS 7 failure. Regulator: {regs.get('website', '')}."
        ),
    })

    findings.append({
        "area":        f"Investor Protection Scheme ({country})",
        "rule":        "National Framework",
        "description": "Equivalent of UK FSCS backstop protection",
        "status":      "AMBER",
        "commentary": (
            f"Africa has no continent-wide investor protection scheme equivalent to UK FSCS. "
            f"In {country}, verify existence and scope of any national investor compensation or "
            f"deposit guarantee scheme with {authority}."
        ),
    })
    return findings


def africa_regulatory_refs() -> list:
    return [
        # ── South Africa — Twin Peaks ────────────────────────────────────────
        ("FSCA (South Africa)",          "https://www.fsca.co.za — Twin Peaks conduct regulator. FAIS Act: client assets are 'trust property' — cannot be commingled. UK equiv: FCA."),
        ("Prudential Authority / SARB",  "https://www.resbank.co.za — prudential regulator under SARB. UK equiv: PRA."),
        ("Financial Markets Act 2012",   "Act 19 of 2012 — custody and segregation of client securities in South Africa. UK equiv: CASS 6."),
        ("FAIS Act",                     "Financial Advisory and Intermediary Services Act 37 of 2002 — client asset (trust property) rules. UK equiv: CASS 7."),
        ("COFI Bill",                    "Conduct of Financial Institutions Bill (pending) — will consolidate all conduct rules incl. trust property/client assets into single market-conduct framework. UK equiv: FCA Handbook."),
        ("FICA",                         "Financial Intelligence Centre Act — South Africa AML/CFT obligations"),
        # ── Nigeria ─────────────────────────────────────────────────────────
        ("SEC Nigeria",                  "https://sec.gov.ng — capital markets regulator. Investments and Securities Act (ISA) — client money in designated trust accounts."),
        ("CBN (Nigeria)",                "https://www.cbn.gov.ng — banking and payments regulator"),
        ("GIABA",                        "https://www.giaba.org — FATF body for West Africa (16 member nations incl. Nigeria, Ghana, Senegal)"),
        # ── Kenya / East Africa ──────────────────────────────────────────────
        ("CMA Kenya",                    "https://www.cma.or.ke — capital markets authority. Capital Markets Act Cap. 485A."),
        ("CBK (Kenya)",                  "https://www.centralbank.go.ke — central bank / banking regulator"),
        ("ESAAMLG",                      "https://www.esaamlg.org — AML/CFT coordination body for Eastern and Southern Africa"),
        # ── Mauritius ───────────────────────────────────────────────────────
        ("FSC Mauritius",                "https://www.fscmauritius.org — Securities Act 2005: client asset segregation. VAITOS Act: digital asset client safeguarding."),
        ("VAITOS Act",                   "Virtual Asset and Initial Token Offering Services Act — Mauritius digital asset client asset rules"),
        # ── Ghana ───────────────────────────────────────────────────────────
        ("SEC Ghana",                    "https://www.sec.gov.gh — Securities Industry Act 2016 (Act 929)"),
        ("BOG (Ghana)",                  "https://www.bog.gov.gh — Banks and Specialised Deposit-Taking Institutions Act 2016 (Act 930)"),
        # ── Egypt ───────────────────────────────────────────────────────────
        ("EFSA (Egypt)",                 "https://www.efsa.gov.eg — Capital Market Law No. 95 of 1992"),
        ("CBE (Egypt)",                  "https://www.cbe.org.eg — Banking Law No. 194 of 2020"),
        # ── Regional Blocs ──────────────────────────────────────────────────
        ("BCEAO / WAEMU",                "https://www.bceao.int — Central Bank of West African States. 8 francophone West African states."),
        ("BEAC / CEMAC",                 "https://www.beac.int — Banque des États de l'Afrique Centrale. 6 Central African states."),
        # ── UK cross-border obligations ──────────────────────────────────────
        ("CASS 6.3",                     "Third-party custody — UK firm must verify equivalent protection in each Africa jurisdiction"),
        ("CASS 7.13",                    "Third-party money — due diligence and ongoing monitoring for Africa arrangements"),
    ]


# ══════════════════════════════════════════════════════════════════════════════
# UPDATED US / LATAM / APAC REFS WITH OFFICIAL WEBSITES
# ══════════════════════════════════════════════════════════════════════════════

def us_regulatory_refs() -> list:
    return [
        # ── United States ────────────────────────────────────────────────────────
        ("SEC — Securities and Exchange Commission",     "https://www.sec.gov — Rule 15c3-3 Customer Protection Rule: broker-dealers must segregate fully-paid customer securities into a Special Custody Account and maintain a Special Reserve Bank Account (SRBA). Reserve computation weekly. UK equiv: CASS 6 + CASS 7."),
        ("CFTC — Commodity Futures Trading Commission",  "https://www.cftc.gov — Rule 1.20: FCMs must hold customer funds in segregated accounts at approved depositories. Daily segregation calculation filed with CFTC. UK equiv: CASS 7."),
        ("Section 4d — Commodity Exchange Act",          "Statutory prohibition on FCM commingling of customer and proprietary funds. Criminal offence under the CEA. Works alongside CFTC Rule 1.20."),
        ("SIPC",                                         "https://www.sipc.org — Securities Investor Protection Corporation. Backstop protection: $500,000/customer (incl. $250,000 cash) if SIPC-member firm fails. UK equiv: FSCS (£85,000). Covers missing assets only — not market losses."),
        ("FINRA",                                        "https://www.finra.org — Enforces SEC Rule 15c3-3 for broker-dealers. FINRA Rule 4311: carrying agreements and customer account segregation standards."),
        ("Federal Reserve",                              "https://www.federalreserve.gov — banking supervision and capital requirements"),
        ("FDIC",                                         "https://www.fdic.gov — deposit insurance ($250,000/depositor)"),
        # ── Canada ───────────────────────────────────────────────────────────────
        ("CIRO — Canadian Investment Regulatory Organization", "https://www.ciro.ca — Formed 2023 from merger of IIROC + MFDA. Governs investment dealers and mutual fund dealers. CIRO Dealer Member Rules require: strict client cash and securities segregation; trust accounts for free credit balances; Form 1 risk-adjusted capital reporting tracking client asset segregation. UK equiv: FCA/CASS for broker-dealers."),
        ("OSFI (Canada)",                                "https://www.osfi-bsif.gc.ca — Office of the Superintendent of Financial Institutions. Prudential regulation of federally regulated banks and insurance companies."),
    ]


def latam_regulatory_refs() -> list:
    return [
        ("BCB — Banco Central do Brasil",                "https://www.bcb.gov.br — Law No. 12,865 patrimônio separado"),
        ("CVM (Brazil)",                                 "https://www.gov.br/cvm — securities regulator"),
        ("BCRA — Banco Central de la República Argentina","https://www.bcra.gob.ar — Communiqué A 6859 PSP segregation"),
        ("CNBV / Banxico (Mexico)",                      "https://www.cnbv.gob.mx / https://www.banxico.org.mx — Fintech Law 2018"),
        ("CMF — Comisión para el Mercado Financiero (Chile)","https://www.cmfchile.cl — Law No. 21,521 Fintech Law"),
        ("SFC — Superintendencia Financiera (Colombia)", "https://www.superfinanciera.gov.co — Decree 2555"),
        ("CASS 6.3",                                     "Third-party custody — equivalent protection for cross-border assets"),
        ("CASS 7.13",                                     "Third-party money — due diligence and ongoing monitoring"),
    ]


def apac_regulatory_refs() -> list:
    return [
        # ── Hong Kong ─────────────────────────────────────────────────────────
        ("SFC — Securities and Futures Commission (HK)",  "https://www.sfc.hk — Cap. 571I: Securities and Futures (Client Money) Rules; Cap. 571H: Securities and Futures (Client Securities) Rules. UK equiv: CASS 7 + CASS 6."),
        ("HKMA — Hong Kong Monetary Authority",           "https://www.hkma.gov.hk — banking supervision and authorised institutions"),
        # ── Singapore ─────────────────────────────────────────────────────────
        ("MAS — Monetary Authority of Singapore",         "https://www.mas.gov.sg — SFA Section 104 + SFLCBR: customer moneys in trust accounts by next business day, daily computations. UK equiv: CASS 7 + CASS 6."),
        # ── Australia ─────────────────────────────────────────────────────────
        ("ASIC — Australian Securities & Investments Commission", "https://www.asic.gov.au — Corporations Act 2001 Division 2 of Part 7.8 (s981B client money trust) + ASIC Client Money Reporting Rules. UK equiv: CASS 7."),
        ("APRA — Australian Prudential Regulation Authority",     "https://www.apra.gov.au — prudential supervision of banks, insurers, superannuation"),
        ("AUSTRAC",                                               "https://www.austrac.gov.au — AML/CTF Act obligations"),
        # ── Japan ─────────────────────────────────────────────────────────────
        ("FSA Japan",                                     "https://www.fsa.go.jp/en — FIEA Article 43-2: mandatory separation of customer assets. Investor Protection Fund: ¥10M/customer backstop. UK equiv: CASS 6 + CASS 7."),
        # ── India ─────────────────────────────────────────────────────────────
        ("SEBI (India)",                                  "https://www.sebi.gov.in — SEBI (Stock Brokers) Regulations 1992, client fund segregation and daily reconciliation"),
        ("RBI (India)",                                   "https://www.rbi.org.in — banking supervision, KYC Master Directions"),
        # ── CASS cross-border obligations ─────────────────────────────────────
        ("CASS 6.3",                                      "Third-party custody — UK firm must verify equivalent protection in each APAC jurisdiction"),
        ("CASS 7.13",                                     "Third-party money — due diligence and ongoing monitoring for APAC arrangements"),
    ]


# ══════════════════════════════════════════════════════════════════════════════
# UNIFIED REGION DETECTOR & DISPATCHERS
# ══════════════════════════════════════════════════════════════════════════════

# Portal region selector slugs → internal region labels.
# Checked BEFORE keyword-based is_* functions to prevent slug overlap
# (e.g. "latin-america" contains "america" and would otherwise match is_n_america).
_SLUG_TO_REGION = {
    "uk":            "UK",
    "north-america": "N. America",
    "latin-america": "Latin America",
    "asia-pacific":  "Asia Pacific",
    "africa":        "Africa",
    "europe":        "Europe",
    # Internal region labels also accepted as pass-through
    "n. america":    "N. America",
    "n america":     "N. America",
    "latin america": "Latin America",
    "asia pacific":  "Asia Pacific",
}


def detect_region(country_or_region: str) -> str:
    """Return a region label for the given country/region string.

    Accepts both country names and portal region slugs (e.g. 'north-america').
    """
    if not country_or_region:
        return "Other"
    slug = country_or_region.strip().lower()
    if slug in _SLUG_TO_REGION:
        return _SLUG_TO_REGION[slug]
    if is_n_america(country_or_region):
        return "N. America"
    if is_latam(country_or_region):
        return "Latin America"
    if is_apac(country_or_region):
        return "Asia Pacific"
    if is_europe(country_or_region):
        return "Europe"
    if is_africa(country_or_region):
        return "Africa"
    return "Other"


def score_regional_client_money(data: dict) -> list:
    """
    Dispatch to the correct regional client money scoring function.
    Checks explicit region slug from portal selector before country-based detection.
    Returns [] for UK/unrecognised jurisdictions (use CASS directly).
    """
    slug = data.get("region", "").strip().lower()
    if slug == "north-america": return score_us_client_money(data)
    if slug == "latin-america": return score_latam_client_money(data)
    if slug == "asia-pacific":  return score_apac_client_money(data)
    if slug == "europe":        return score_europe_client_money(data)
    if slug == "africa":        return score_africa_client_money(data)
    if slug == "uk":            return []
    country = data.get("country", "") or data.get("jurisdiction", "")
    if is_n_america(country):   return score_us_client_money(data)
    if is_latam(country):       return score_latam_client_money(data)
    if is_apac(country):        return score_apac_client_money(data)
    if is_europe(country):      return score_europe_client_money(data)
    if is_africa(country):      return score_africa_client_money(data)
    return []


def score_regional_cross_border(country: str, data: dict) -> list:
    """
    Dispatch to the correct regional cross-border scoring function.
    Checks explicit region slug from portal selector before country-based detection.
    Called by generate_country_risk.py.
    """
    slug = data.get("region", "").strip().lower()
    if slug == "north-america": return score_us_cross_border(country, data)
    if slug == "latin-america": return score_latam_cross_border(country, data)
    if slug == "asia-pacific":  return score_apac_cross_border(country, data)
    if slug == "europe":        return score_europe_cross_border(country, data)
    if slug == "africa":        return score_africa_cross_border(country, data)
    if is_n_america(country):   return score_us_cross_border(country, data)
    if is_latam(country):       return score_latam_cross_border(country, data)
    if is_apac(country):        return score_apac_cross_border(country, data)
    if is_europe(country):      return score_europe_cross_border(country, data)
    if is_africa(country):      return score_africa_cross_border(country, data)
    return []


def regional_regulatory_refs(country_or_region: str) -> list:
    """Return the correct regional reference list (with official URLs) for a given country/region.

    Accepts both country names and portal region slugs (e.g. 'north-america').
    """
    if not country_or_region:
        return []
    slug = country_or_region.strip().lower()
    if slug == "north-america": return us_regulatory_refs()
    if slug == "latin-america": return latam_regulatory_refs()
    if slug == "asia-pacific":  return apac_regulatory_refs()
    if slug == "europe":        return europe_regulatory_refs()
    if slug == "africa":        return africa_regulatory_refs()
    if slug == "uk":            return []
    if is_n_america(country_or_region): return us_regulatory_refs()
    if is_latam(country_or_region):     return latam_regulatory_refs()
    if is_apac(country_or_region):      return apac_regulatory_refs()
    if is_europe(country_or_region):    return europe_regulatory_refs()
    if is_africa(country_or_region):    return africa_regulatory_refs()
    return []


def get_regulator_website(regulator_name: str) -> str:
    """Look up official website for a named regulator."""
    return REGULATORY_WEBSITES.get(regulator_name, "")
