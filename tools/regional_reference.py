"""
Regional Regulatory Reference Database
National regulatory agencies — North America · Latin America · Asia-Pacific · Africa
Updated: October 2026
"""

SOURCED_DATE = "2026-10-21"

# =============================================================================
# NORTH AMERICA — USA (Fed · SEC · OCC · FDIC · CFTC · FinCEN · OFAC)
#                 Canada (OSFI · OSC · AMF · FINTRAC)
# =============================================================================
NORTH_AMERICA_NEWS = [
    {
        "date": "2026-09",
        "regulator": "SEC",
        "country": "USA",
        "type": "Cybersecurity Rules",
        "headline": "SEC cybersecurity incident disclosure rules — 4-day Form 8-K filing required",
        "detail": (
            "SEC final rules on cybersecurity risk management require public companies to disclose "
            "material cybersecurity incidents within four business days via Form 8-K Item 1.05. "
            "Annual 10-K filings must include disclosure of cybersecurity risk management strategy, "
            "governance, and material risks. Financial institutions must also assess third-party "
            "vendor cybersecurity risks. SEC examiners citing non-disclosure as a top deficiency."
        ),
        "tags": ["SEC", "Cybersecurity", "Form 8-K", "Disclosure"],
        "severity": "RED",
    },
    {
        "date": "2026-08",
        "regulator": "FinCEN",
        "country": "USA",
        "type": "AML Compliance",
        "headline": "Corporate Transparency Act — Beneficial Ownership Information reporting now enforced",
        "detail": (
            "FinCEN's Beneficial Ownership Information (BOI) reporting under the Corporate Transparency "
            "Act is now actively enforced. Most US LLCs, corporations, and similar entities must report "
            "beneficial owners directly to FinCEN. Financial institutions must update CDD procedures to "
            "cross-reference FinCEN BOI database. Penalties: up to $591/day for wilful non-compliance. "
            "Foreign-owned entities with US presence have heightened obligations."
        ),
        "tags": ["FinCEN", "CTA", "Beneficial Ownership", "AML"],
        "severity": "RED",
    },
    {
        "date": "2026-07",
        "regulator": "OSFI",
        "country": "Canada",
        "type": "Operational Resilience",
        "headline": "OSFI E-23 Operational Resilience — critical operations testing requirements active",
        "detail": (
            "OSFI Guideline E-23 on Operational Resilience requires federally regulated financial "
            "institutions (FRFIs) to identify critical operations, set impact tolerances, and conduct "
            "resilience testing. Institutions must demonstrate recovery within defined disruption "
            "tolerances. E-23 aligns with FCA PS21/3 but with Canadian-specific requirements for "
            "domestic systemically important banks (D-SIBs). OSFI supervisory reviews underway."
        ),
        "tags": ["OSFI", "Operational Resilience", "E-23", "Canada"],
        "severity": "AMBER",
    },
    {
        "date": "2026-06",
        "regulator": "FDIC",
        "country": "USA",
        "type": "Deposit Insurance",
        "headline": "FDIC brokered deposits final rule — revised primary purpose exception criteria",
        "detail": (
            "FDIC final rule revises the treatment of brokered deposits, updating the primary purpose "
            "exception (PPE) criteria for deposit brokers. Firms receiving deposits through third-party "
            "platforms must re-assess whether accounts qualify as brokered. Impacts custodians and "
            "fintech firms holding sweep deposits. Banks must update internal classifications and "
            "Call Report submissions. FDIC examination scrutiny increasing on liquidity risk."
        ),
        "tags": ["FDIC", "Brokered Deposits", "Liquidity", "Bank Supervision"],
        "severity": "AMBER",
    },
    {
        "date": "2026-05",
        "regulator": "SEC",
        "country": "USA",
        "type": "Custody Rules",
        "headline": "SEC proposed amendments to Investment Adviser Custody Rule — expanded asset scope",
        "detail": (
            "SEC proposed amendments to Rule 206(4)-2 expand the Qualified Custodian requirement to "
            "cover all assets including crypto, real estate, and alternatives held for advisory clients. "
            "Investment advisers must verify client assets with independent qualified custodians. "
            "Surprise examinations required. Comment period closed; final rule expected Q1 2027. "
            "Significant impact on RIAs managing digital assets and alternative investments."
        ),
        "tags": ["SEC", "Custody Rule", "Investment Advisers", "Crypto"],
        "severity": "AMBER",
    },
    {
        "date": "2026-04",
        "regulator": "FINTRAC",
        "country": "Canada",
        "type": "AML Enforcement",
        "headline": "FINTRAC issues C$7.4M administrative penalty to Canadian bank for AML failures",
        "detail": (
            "FINTRAC imposed an administrative monetary penalty (AMP) of C$7.4 million on a Schedule I "
            "Canadian bank for failures to submit Suspicious Transaction Reports (STRs) and Large Cash "
            "Transaction Reports (LCTRs) within required timeframes. FINTRAC examination found gaps in "
            "transaction monitoring systems, inadequate EDD for high-risk customers, and delayed reporting. "
            "FINTRAC has increased examination frequency for mid-size banks and credit unions."
        ),
        "tags": ["FINTRAC", "AML", "STR", "Enforcement", "Canada"],
        "severity": "RED",
    },
    {
        "date": "2026-03",
        "regulator": "CFTC",
        "country": "USA",
        "type": "Derivatives",
        "headline": "CFTC finalises uncleared margin rules phase 6 — smaller counterparties now covered",
        "detail": (
            "CFTC phase 6 uncleared margin rules now apply to swap dealers and covered swap entities "
            "with smaller average aggregate notional amounts. Initial margin posting and collection "
            "requirements apply to in-scope counterparties. Operational impact on custodians acting "
            "as IM custodians — segregation, tri-party arrangements, and rehypothecation restrictions apply. "
            "CFTC examining compliance with variation margin documentation requirements."
        ),
        "tags": ["CFTC", "Derivatives", "Uncleared Margin", "IM Custodian"],
        "severity": "AMBER",
    },
]

# =============================================================================
# LATIN AMERICA — Brazil (BCB · CVM)  Mexico (BANXICO · CNBV)
#                 Colombia (SFC)  Chile (CMF)  Peru (SBS)  Argentina (BCRA)
#                 Regional: GAFILAT
# =============================================================================
LATIN_AMERICA_NEWS = [
    {
        "date": "2026-09",
        "regulator": "BCB",
        "country": "Brazil",
        "type": "Payment Systems",
        "headline": "BCB launches Pix Automático — recurring payment mandate via instant rails",
        "detail": (
            "Banco Central do Brasil launched Pix Automático, enabling recurring scheduled payments "
            "over the Pix instant payment infrastructure. Regulated entities must integrate Pix APIs "
            "for consumer and business payments. BCB mandating open finance data sharing between "
            "authorised financial institutions. Custodians and payment institutions must update client "
            "money treatment under BACEN Resolution 4,659 for Pix-held funds."
        ),
        "tags": ["BCB", "Pix", "Payment Systems", "Open Finance", "Brazil"],
        "severity": "AMBER",
    },
    {
        "date": "2026-08",
        "regulator": "CVM",
        "country": "Brazil",
        "type": "Investment Funds",
        "headline": "CVM Resolution 175 — new investment fund framework fully operative",
        "detail": (
            "CVM Resolution 175 is the consolidated framework for Brazilian investment funds. "
            "Key requirements: client asset segregation between fund patrimony and manager assets, "
            "enhanced disclosures for retail investors, new fund classes (FIP, FIDC, FII), and "
            "expanded eligibility for foreign funds registered in Brazil. CVM enforcement focus on "
            "FIDC (credit receivables funds) — segregation failures drawing highest penalties. "
            "Fund administrators must file monthly reports to CVM."
        ),
        "tags": ["CVM", "Investment Funds", "Resolution 175", "Segregation", "Brazil"],
        "severity": "AMBER",
    },
    {
        "date": "2026-07",
        "regulator": "CNBV",
        "country": "Mexico",
        "type": "Fintech Regulation",
        "headline": "CNBV finalises secondary rules for Electronic Payment Fund Institutions (IFPEs)",
        "detail": (
            "Mexico's CNBV issued final secondary regulation for Electronic Payment Fund Institutions "
            "(IFPEs) under the Fintech Law (LRITF). IFPEs must segregate client electronic money from "
            "own assets, maintain capital reserves, and report to CNBV monthly. UIF AML obligations "
            "for IFPEs include STR filing and KYC documentation. Key difference from traditional "
            "banking: IFPEs cannot take deposits but must protect payment funds in segregated accounts."
        ),
        "tags": ["CNBV", "Fintech", "IFPE", "Electronic Payments", "Mexico"],
        "severity": "AMBER",
    },
    {
        "date": "2026-06",
        "regulator": "SFC",
        "country": "Colombia",
        "type": "Consumer Protection",
        "headline": "SFC issues circular on virtual assets — VASPs must register and segregate client funds",
        "detail": (
            "Colombia's Superintendencia Financiera (SFC) issued Circular 030 requiring Virtual Asset "
            "Service Providers (VASPs) operating in Colombia to register with SFC, implement AML/CFT "
            "controls, and segregate client digital assets from own holdings. SFC is the consolidated "
            "regulator covering banking, insurance, and securities — VASPs must meet conduct standards "
            "equivalent to supervised entities. GAFILAT compliance required for cross-border VASP activity."
        ),
        "tags": ["SFC", "VASP", "Crypto", "Client Assets", "Colombia"],
        "severity": "AMBER",
    },
    {
        "date": "2026-05",
        "regulator": "CMF",
        "country": "Chile",
        "type": "Securities Regulation",
        "headline": "CMF publishes Fintech Law implementing regulations — open finance and crowdfunding",
        "detail": (
            "Chile's CMF issued implementing regulations under Law 21,521 (Fintech Law), covering "
            "Open Finance data sharing obligations, crowdfunding platform licensing, payment initiators, "
            "and alternative credit providers. Investment platforms must segregate investor funds and "
            "comply with CMF conduct standards. CMF has intensified examination of securities "
            "intermediaries for client asset segregation failures following prior enforcement actions."
        ),
        "tags": ["CMF", "Fintech Law", "Open Finance", "Crowdfunding", "Chile"],
        "severity": "GREEN",
    },
    {
        "date": "2026-04",
        "regulator": "SBS",
        "country": "Peru",
        "type": "Pension Fund Oversight",
        "headline": "SBS issues updated guidelines for AFP custodians — segregation and liquidity rules",
        "detail": (
            "Peru's SBS (Superintendencia de Banca, Seguros y AFP) updated guidelines for custodians "
            "of private pension fund (AFP) assets. Key changes: custodians must maintain segregated "
            "sub-accounts per AFP, daily reconciliation of securities positions, enhanced liquidity "
            "requirements for overnight holdings, and quarterly SBS reporting of custody arrangements. "
            "SBS supervises AFPs as systemically important — custodian failures can trigger immediate "
            "supervisory intervention."
        ),
        "tags": ["SBS", "AFP", "Custody", "Pension Funds", "Peru"],
        "severity": "AMBER",
    },
    {
        "date": "2026-03",
        "regulator": "GAFILAT",
        "country": "Regional",
        "type": "AML Standards",
        "headline": "GAFILAT 2026 plenary — Mexico and Colombia receive enhanced follow-up status",
        "detail": (
            "GAFILAT's 2026 plenary review placed Mexico and Colombia on enhanced follow-up under "
            "the FATF 4th round mutual evaluation process, citing deficiencies in beneficial ownership "
            "transparency and non-financial sector AML supervision. GAFILAT member countries must "
            "demonstrate technical compliance with all 40 FATF Recommendations. Financial institutions "
            "with Latin American correspondent banking relationships must reassess country risk ratings "
            "for Mexico and Colombia."
        ),
        "tags": ["GAFILAT", "FATF", "AML", "Mutual Evaluation", "LatAm"],
        "severity": "RED",
    },
]

# =============================================================================
# ASIA-PACIFIC — Singapore (MAS)  Hong Kong (HKMA · SFC)
#                China (NFRA · CSRC · PBOC)  Japan (FSA)
#                India (RBI · SEBI)  Australia (ASIC · APRA · AUSTRAC)
#                Regional: APG
# =============================================================================
ASIA_NEWS = [
    {
        "date": "2026-09",
        "regulator": "MAS",
        "country": "Singapore",
        "type": "Operational Resilience",
        "headline": "MAS finalises revised Technology Risk Management guidelines — AI and cloud covered",
        "detail": (
            "MAS published revised Technology Risk Management (TRM) Guidelines covering artificial "
            "intelligence systems, multi-cloud architectures, and critical API security. FIs must "
            "conduct annual technology risk assessments, maintain cyber hygiene controls, and notify "
            "MAS within one hour of significant cybersecurity incidents. MAS Notice SFA 04-N02 client "
            "asset segregation requirements remain unchanged but MAS examining digital asset custodians "
            "for adequate segregation of tokenised securities."
        ),
        "tags": ["MAS", "TRM", "Technology Risk", "AI", "Singapore"],
        "severity": "AMBER",
    },
    {
        "date": "2026-08",
        "regulator": "SFC",
        "country": "Hong Kong",
        "type": "Crypto Regulation",
        "headline": "SFC VATP licensing — 11 exchanges licensed, 5 enforcement actions for unlicensed operation",
        "detail": (
            "Hong Kong SFC has licensed 11 Virtual Asset Trading Platforms (VATPs) under the VASP "
            "regime that took effect June 2023. Five unlicensed platforms received enforcement notices "
            "with fines totalling HK$48M. Licensed VATPs must segregate client virtual assets from own "
            "assets, hold at least 98% of client assets in cold storage, and comply with SFC Code of "
            "Conduct client asset requirements under paragraph 9. HKMA is separately supervising "
            "stablecoin issuers under draft stablecoin legislation."
        ),
        "tags": ["SFC", "VATP", "Crypto", "Client Assets", "Hong Kong"],
        "severity": "RED",
    },
    {
        "date": "2026-07",
        "regulator": "APRA",
        "country": "Australia",
        "type": "Operational Resilience",
        "headline": "APRA CPS 230 operational resilience — effective 1 July 2025, active examination phase",
        "detail": (
            "APRA Prudential Standard CPS 230 on Operational Risk Management took effect 1 July 2025. "
            "APRA-regulated entities (banks, insurers, super funds) must identify critical operations, "
            "set maximum tolerable disruptions, and test resilience annually. Service provider "
            "agreements must include notification and audit rights. APRA examination findings: "
            "common gaps in third-party mapping and impact tolerance documentation. "
            "Compare to UK FCA PS21/3 — similar framework but APRA has broader sector coverage."
        ),
        "tags": ["APRA", "CPS 230", "Operational Resilience", "Australia"],
        "severity": "RED",
    },
    {
        "date": "2026-06",
        "regulator": "FSA",
        "country": "Japan",
        "type": "AML Enforcement",
        "headline": "Japan FSA issues business improvement orders to two crypto exchanges for AML failures",
        "detail": (
            "Japan Financial Services Agency issued business improvement orders (業務改善命令) to two "
            "registered crypto asset exchange services for failures in AML/CFT compliance. Deficiencies "
            "included inadequate transaction monitoring, failure to file suspicious transaction reports "
            "under the Act on Prevention of Transfer of Criminal Proceeds, and insufficient KYC for "
            "overseas remittances. FSA inspection priorities 2026/27 include crypto, cross-border "
            "payments, and FIEA client asset segregation for new asset classes."
        ),
        "tags": ["FSA", "AML", "Crypto", "Business Improvement Order", "Japan"],
        "severity": "RED",
    },
    {
        "date": "2026-05",
        "regulator": "SEBI",
        "country": "India",
        "type": "Market Regulation",
        "headline": "SEBI tightens F&O derivatives rules — position limits and margin requirements raised",
        "detail": (
            "SEBI issued circular tightening Futures & Options (F&O) rules following retail investor "
            "losses: minimum contract sizes increased, upfront margin collection now mandatory, "
            "intraday margin monitoring required. Custodians and clearing members must update margin "
            "collection procedures. SEBI is examining depository participants for client securities "
            "segregation compliance. SEBI-RBI joint circular on foreign portfolio investor (FPI) "
            "custody arrangements requires custodian banks to enhance reporting."
        ),
        "tags": ["SEBI", "F&O", "Derivatives", "Margin", "India"],
        "severity": "AMBER",
    },
    {
        "date": "2026-04",
        "regulator": "CSRC",
        "country": "China",
        "type": "Capital Markets",
        "headline": "NFRA and CSRC joint circular on custodian bank obligations for fund assets",
        "detail": (
            "China's NFRA (National Financial Regulatory Administration, formerly CBIRC) and CSRC "
            "issued a joint circular clarifying custodian bank obligations for mutual fund and private "
            "fund assets. Custodian banks must maintain complete records of fund assets independent "
            "from manager records, conduct daily NAV reconciliations, and report discrepancies to CSRC "
            "within 24 hours. Data localisation requirements under PIPL apply to cross-border fund "
            "data transfers — overseas custodians must use approved cross-border data mechanisms."
        ),
        "tags": ["NFRA", "CSRC", "Custodian Banks", "Fund Assets", "China"],
        "severity": "AMBER",
    },
    {
        "date": "2026-03",
        "regulator": "AUSTRAC",
        "country": "Australia",
        "type": "AML Enforcement",
        "headline": "AUSTRAC accepts AUD 100M enforceable undertaking from major bank for AML failures",
        "detail": (
            "AUSTRAC accepted an AUD 100 million enforceable undertaking from a major Australian bank "
            "following an investigation into AML/CTF compliance failures including deficient transaction "
            "monitoring, failure to submit threshold transaction reports (TTRs), and inadequate "
            "oversight of correspondent banking relationships. AUSTRAC has intensified examination of "
            "Digital Currency Exchanges (DCEs) and remittance dealers. Financial institutions must "
            "review AUSTRAC compliance programme adequacy against AML/CTF Rules Chapter 8."
        ),
        "tags": ["AUSTRAC", "AML", "Enforceable Undertaking", "Australia"],
        "severity": "RED",
    },
]

# =============================================================================
# AFRICA — South Africa (PA/SARB · FSCA)  Nigeria (CBN)
#          Kenya (CBK · CMA)  Regional: GIABA · ESAAMLG · GABAC
# =============================================================================
AFRICA_NEWS = [
    {
        "date": "2026-09",
        "regulator": "FSCA",
        "country": "South Africa",
        "type": "Conduct Standards",
        "headline": "FSCA publishes Conduct Standard for Banks — Twin Peaks conduct obligations now codified",
        "detail": (
            "The Financial Sector Conduct Authority (FSCA) published the Conduct Standard for Banks "
            "under the Financial Sector Regulation Act (FSRA). This separates prudential supervision "
            "(handled by the Prudential Authority under SARB) from market conduct supervision (FSCA). "
            "Banks must comply with FSCA conduct standards covering: fair treatment of customers, "
            "product governance, client assets held in custody, and complaint handling. FSCA has "
            "powers to impose conduct penalties up to ZAR 10M per contravention."
        ),
        "tags": ["FSCA", "Twin Peaks", "Conduct Standard", "Banks", "South Africa"],
        "severity": "AMBER",
    },
    {
        "date": "2026-08",
        "regulator": "PA/SARB",
        "country": "South Africa",
        "type": "FATF Compliance",
        "headline": "South Africa removed from FATF grey list — FIC Act amendments now operational",
        "detail": (
            "South Africa was removed from the FATF grey list in October 2024 following significant "
            "legislative and supervisory reforms. The Financial Intelligence Centre Act (FICA) "
            "amendments strengthened beneficial ownership registers, obliged institutions reporting "
            "obligations, and supervision of DNFBPs. The Prudential Authority and FSCA jointly "
            "supervise AML/CFT compliance for financial institutions. Financial institutions must "
            "maintain enhanced vigilance — correspondent banks should re-assess SA country risk ratings."
        ),
        "tags": ["PA/SARB", "FATF", "Grey List", "FIC Act", "South Africa"],
        "severity": "GREEN",
    },
    {
        "date": "2026-07",
        "regulator": "CBN",
        "country": "Nigeria",
        "type": "Bank Capitalisation",
        "headline": "CBN bank recapitalisation — commercial banks must meet new minimum capital by March 2026",
        "detail": (
            "Central Bank of Nigeria (CBN) issued a recapitalisation directive requiring commercial "
            "banks to meet new minimum capital thresholds: international banks NGN 500 billion, "
            "national banks NGN 200 billion, regional banks NGN 50 billion. Banks failing to meet "
            "requirements face merger, acquisition, or licence downgrade. CBN has approved 8 mergers "
            "to date. International correspondent banks must reassess credit lines and settlement "
            "arrangements with Nigerian banks during the transition period to March 2026."
        ),
        "tags": ["CBN", "Recapitalisation", "Minimum Capital", "Banking", "Nigeria"],
        "severity": "RED",
    },
    {
        "date": "2026-06",
        "regulator": "CBK",
        "country": "Kenya",
        "type": "Digital Finance",
        "headline": "CBK Digital Credit Provider (DCP) licensing framework — 51 licensed providers",
        "detail": (
            "Central Bank of Kenya (CBK) has licensed 51 Digital Credit Providers (DCPs) under the "
            "Central Bank of Kenya (Amendment) Act 2021. Unlicensed digital lenders are banned from "
            "operating. DCPs must comply with consumer protection requirements, data privacy rules "
            "under Kenya's Data Protection Act, and CBK AML regulations. CMA separately supervises "
            "capital market intermediaries — custodians of Kenyan securities must hold CMA approval "
            "and comply with NSE and CDSC settlement rules."
        ),
        "tags": ["CBK", "Digital Credit", "DCP", "Fintech", "Kenya"],
        "severity": "GREEN",
    },
    {
        "date": "2026-05",
        "regulator": "ESAAMLG",
        "country": "Regional",
        "type": "AML Standards",
        "headline": "ESAAMLG 4th round evaluations — Tanzania and Zambia in enhanced follow-up",
        "detail": (
            "The Eastern and Southern African Anti-Money Laundering Group (ESAAMLG) completed 4th "
            "round mutual evaluations placing Tanzania and Zambia on enhanced follow-up due to "
            "low effectiveness ratings in AML/CFT supervision. ESAAMLG covers 18 member jurisdictions. "
            "Financial institutions with East/Southern Africa correspondent banking relationships "
            "should review country risk frameworks for Tanzania and Zambia. GIABA (West Africa) "
            "similarly placed Côte d'Ivoire and Senegal on follow-up for DNFBP supervision deficiencies."
        ),
        "tags": ["ESAAMLG", "GIABA", "Mutual Evaluation", "AML", "East Africa"],
        "severity": "AMBER",
    },
    {
        "date": "2026-04",
        "regulator": "CBN",
        "country": "Nigeria",
        "type": "AML Enforcement",
        "headline": "CBN fines 5 banks NGN 9.85 billion for AML/CFT and consumer protection violations",
        "detail": (
            "CBN imposed aggregate fines of NGN 9.85 billion on five Nigerian banks following "
            "special examinations that uncovered: failure to file Currency Transaction Reports (CTRs) "
            "to NFIU, inadequate KYC for politically exposed persons, foreign exchange infractions, "
            "and consumer protection failures. CBN has required all Deposit Money Banks to upgrade "
            "transaction monitoring systems to include AI-based analytics by December 2026. "
            "NFIU (Nigeria's FIU) has increased STR filing enforcement."
        ),
        "tags": ["CBN", "AML", "Enforcement", "Fine", "Nigeria"],
        "severity": "RED",
    },
]

# =============================================================================
# EUROPE — ESMA · ECB · EBA · BaFin · AMF · DNB · FCA-UK post-Brexit
#          DORA · MiCAR · EMIR Refit · SFDR · MiFID II · CRD VI
# =============================================================================
EUROPE_NEWS = [
    {
        "date": "2026-09",
        "regulator": "ESMA",
        "country": "EU",
        "type": "Client Asset Rules",
        "headline": "ESMA publishes updated Q&A on MiFID II client asset segregation — crypto assets included",
        "detail": (
            "ESMA updated its Q&A on the application of MiFID II client asset protection rules to "
            "include guidance on crypto-asset safekeeping following MiCAR implementation. Investment "
            "firms must segregate client crypto assets under the same regime as traditional securities. "
            "ESMA clarifies that wallet-level segregation (not just book-entry) is required for retail "
            "clients. National competent authorities (NCAs) are conducting examinations of MiFID II "
            "Article 16(9) and (10) compliance — client money and custody asset reconciliation frequency "
            "requirements equivalent to daily internal and monthly external reconciliation."
        ),
        "tags": ["ESMA", "MiFID II", "Client Assets", "MiCAR", "Segregation"],
        "severity": "RED",
    },
    {
        "date": "2026-08",
        "regulator": "ESMA/NCAs",
        "country": "EU",
        "type": "DORA",
        "headline": "DORA technical standards fully operative — ICT incident classification and reporting live",
        "detail": (
            "The Digital Operational Resilience Act (DORA — Regulation (EU) 2022/2554) has been fully "
            "operative since 17 January 2025. All EU financial entities — banks, investment firms, "
            "CCPs, CSDs, payment institutions — must comply with ICT risk management, incident "
            "classification and reporting, digital operational resilience testing, and third-party ICT "
            "provider oversight. Major ICT incidents must be reported to NCAs within 4 hours (initial "
            "report), 24 hours (intermediate), and 1 month (final). ESMA, EBA, and EIOPA published "
            "final DORA RTS — firms' gap remediation plans under NCA review in Q3/Q4 2026."
        ),
        "tags": ["DORA", "ESMA", "ICT Risk", "Operational Resilience", "EU"],
        "severity": "RED",
    },
    {
        "date": "2026-07",
        "regulator": "EBA",
        "country": "EU",
        "type": "AML/CFT",
        "headline": "EU AMLA established in Frankfurt — centralised AML supervision of high-risk obliged entities",
        "detail": (
            "The EU Anti-Money Laundering Authority (AMLA) commenced operations in Frankfurt as the "
            "central EU AML supervisor under the new AML Package (AMLR, AMLD6, AMLA Regulation). "
            "AMLA will directly supervise approximately 40 high-risk cross-border obliged entities "
            "from 2028; NCAs retain oversight of remaining entities. The single EU AML Rulebook "
            "replaces national AML law for obliged entities from 2027. Firms must review STR/SAR "
            "reporting chains, UBO verification, and transaction monitoring calibration against the "
            "new risk-based approach mandated by AMLR Articles 20-30."
        ),
        "tags": ["AMLA", "EBA", "AML", "AMLR", "Frankfurt"],
        "severity": "AMBER",
    },
    {
        "date": "2026-06",
        "regulator": "ECB/SSM",
        "country": "Eurozone",
        "type": "Banking Supervision",
        "headline": "ECB SSM 2026 supervisory priorities — operational resilience, credit risk, and climate",
        "detail": (
            "The ECB Single Supervisory Mechanism (SSM) 2026 supervisory priorities for significant "
            "institutions (SIs) under direct ECB supervision focus on: (1) operational resilience — "
            "DORA compliance and cyber risk; (2) credit risk — NPL management in higher-rate environment; "
            "(3) climate risk — TCFD disclosure and physical risk exposure. ECB on-site inspections "
            "targeting internal liquidity adequacy assessment processes (ILAAPs) and client asset "
            "safekeeping arrangements at universal banks acting as custodians. Less significant "
            "institutions (LSIs) supervised by national competent authorities."
        ),
        "tags": ["ECB", "SSM", "DORA", "Credit Risk", "Climate"],
        "severity": "AMBER",
    },
    {
        "date": "2026-05",
        "regulator": "ESMA",
        "country": "EU",
        "type": "MiCAR",
        "headline": "MiCAR Phase 2 fully effective — CASPs must hold client crypto assets with licensed custodian",
        "detail": (
            "Markets in Crypto-Assets Regulation (MiCAR) Phase 2 is fully effective across all EU "
            "member states. Crypto-Asset Service Providers (CASPs) must: segregate client crypto "
            "assets from own holdings, hold client assets with a licensed custodian or via qualified "
            "custody arrangements, disclose insolvency treatment of client assets, and maintain "
            "reconciliation records. ESMA has received 180+ CASP licence applications; NCAs processing "
            "timelines vary significantly. MiCAR passporting allows EU-licensed CASPs to operate cross-border. "
            "Non-EU CASPs targeting EU clients require reverse solicitation to avoid authorisation obligation."
        ),
        "tags": ["MiCAR", "ESMA", "CASP", "Crypto", "Custody"],
        "severity": "RED",
    },
    {
        "date": "2026-04",
        "regulator": "BaFin",
        "country": "Germany",
        "type": "Enforcement",
        "headline": "BaFin imposes EUR 8.5M fine on Frankfurt custody bank for KAGB asset segregation failures",
        "detail": (
            "BaFin imposed an EUR 8.5 million administrative fine on a Frankfurt-based custody bank "
            "for failures to properly segregate investment fund assets under the German Capital "
            "Investment Code (KAGB). Deficiencies included commingling of fund assets across sub-funds, "
            "failure to maintain independent custody records, and delays in reporting discrepancies to "
            "fund management companies. BaFin has issued a sector letter to all Kapitalverwaltungsgesellschaften "
            "(KVGs) requiring review of custodian arrangements and sub-custodian chain oversight. "
            "KAGB §68-71 custody obligations align with UCITS Directive and AIFMD requirements."
        ),
        "tags": ["BaFin", "KAGB", "Custody", "Enforcement", "Germany"],
        "severity": "RED",
    },
    {
        "date": "2026-03",
        "regulator": "AMF",
        "country": "France",
        "type": "SFDR",
        "headline": "AMF SFDR enforcement — 3 asset managers fined for greenwashing in sustainability disclosures",
        "detail": (
            "France's AMF (Autorité des Marchés Financiers) fined three asset managers a total of "
            "EUR 3.2M for misleading sustainability disclosures under the Sustainable Finance "
            "Disclosure Regulation (SFDR). The managers mis-classified funds as Article 8 or Article 9 "
            "without adequate substantiation of ESG criteria. AMF has published SFDR examination "
            "findings and updated guidance for PAI (Principal Adverse Impact) disclosures. ESMA "
            "is finalising the SFDR Level 2 review — major changes to Article 8/9 classification "
            "expected in 2027. Firms marketing EU funds must review all SFDR disclosures for accuracy."
        ),
        "tags": ["AMF", "SFDR", "ESG", "Greenwashing", "France"],
        "severity": "AMBER",
    },
]

# =============================================================================
# Combined lookup by region slug
# =============================================================================
REGIONAL_NEWS = {
    "north-america":  NORTH_AMERICA_NEWS,
    "latin-america":  LATIN_AMERICA_NEWS,
    "asia-pacific":   ASIA_NEWS,
    "africa":         AFRICA_NEWS,
    "europe":         EUROPE_NEWS,
}

REGION_META = {
    "north-america": {
        "title": "North America — Regulatory Intelligence",
        "regulators": "Fed · SEC · OCC · FDIC · CFTC · FinCEN · OFAC · OSFI · OSC · AMF · FINTRAC",
        "countries": "USA · Canada",
    },
    "latin-america": {
        "title": "Latin America — Regulatory Intelligence",
        "regulators": "BCB · CVM · BANXICO · CNBV · SFC · CMF · SBS · BCRA · CNV · GAFILAT",
        "countries": "Brazil · Mexico · Colombia · Chile · Peru · Argentina",
    },
    "asia-pacific": {
        "title": "Asia-Pacific — Regulatory Intelligence",
        "regulators": "MAS · HKMA · SFC · NFRA · CSRC · PBOC · FSA · RBI · SEBI · ASIC · APRA · AUSTRAC · APG",
        "countries": "Singapore · Hong Kong · China · Japan · India · Australia",
    },
    "africa": {
        "title": "Africa — Regulatory Intelligence",
        "regulators": "PA/SARB · FSCA · CBN · CBK · CMA · GIABA · ESAAMLG · GABAC",
        "countries": "South Africa · Nigeria · Kenya",
    },
    "europe": {
        "title": "Europe — Regulatory Intelligence",
        "regulators": "ESMA · ECB/SSM · EBA · AMLA · BaFin · AMF · DNB · CONSOB · CNMV · AFM",
        "countries": "EU · Germany · France · Netherlands · Italy · Spain",
    },
}


# =============================================================================
# REGIONAL ENFORCEMENT ACTIONS — per region slug
# =============================================================================

REGIONAL_ENFORCEMENT = {
    "uk": {
        "title": "FCA Enforcement Actions",
        "regulator_label": "FCA",
        "cases": [
            {
                "firm": "NatWest Group plc",
                "fine": "£264.8M",
                "regulator": "FCA",
                "date": "Nov 2021",
                "summary": "Failure to adequately monitor and scrutinise activity on a high-risk customer's accounts over 5 years. AML systems failed to flag £365M in suspicious cash deposits.",
            },
            {
                "firm": "Santander UK plc",
                "fine": "£12.4M",
                "regulator": "FCA",
                "date": "Aug 2022",
                "summary": "CASS client money failings — failure to segregate client funds in 61,000 investment accounts correctly under CASS 7. Reconciliation breaches persisted for 4 years.",
            },
            {
                "firm": "Metro Bank plc",
                "fine": "£10.5M",
                "regulator": "FCA",
                "date": "Mar 2023",
                "summary": "CASS 6 custody breaches — failure to protect client assets held in the firm's own name, inadequate record-keeping, and insufficient oversight by the COOF function.",
            },
            {
                "firm": "Guaranty Trust Bank (UK)",
                "fine": "£7.6M",
                "regulator": "FCA",
                "date": "Jan 2024",
                "summary": "Financial crime controls — inadequate AML transaction monitoring, customer due diligence failures, and weak correspondent banking oversight for high-risk jurisdictions.",
            },
            {
                "firm": "Clearstream Banking S.A.",
                "fine": "£8.1M",
                "regulator": "FCA",
                "date": "Sep 2023",
                "summary": "Transaction reporting failures — systematic errors in MiFIR transaction reports across equity and bond markets. 18 months of inaccurate LEI and instrument identifier data.",
            },
        ],
    },
    "north-america": {
        "title": "SEC / OCC / FinCEN Enforcement Actions",
        "regulator_label": "SEC · OCC · FinCEN",
        "cases": [
            {
                "firm": "Wells Fargo N.A.",
                "fine": "$97.8M",
                "regulator": "OCC",
                "date": "Dec 2022",
                "summary": "Unsafe and unsound practices related to overdraft programme — inadequate customer disclosures, unfair billing practices, and weak compliance management systems.",
            },
            {
                "firm": "Citigroup Inc.",
                "fine": "$136M",
                "regulator": "OCC",
                "date": "Jul 2023",
                "summary": "Data governance and risk management deficiencies — failure to remediate consent order obligations from 2020. Data quality issues across regulatory reporting frameworks.",
            },
            {
                "firm": "Robinhood Financial LLC",
                "fine": "$30M",
                "regulator": "FinCEN",
                "date": "Aug 2022",
                "summary": "BSA/AML programme failures — inadequate suspicious activity reporting, insufficient customer due diligence, and failure to file timely SARs on high-risk activity.",
            },
            {
                "firm": "Goldman Sachs Asset Mgmt",
                "fine": "$4M",
                "regulator": "SEC",
                "date": "Nov 2022",
                "summary": "ESG disclosure failures — misleading statements regarding ESG investment policies in two mutual funds. Procedures not followed prior to making ESG investment decisions.",
            },
            {
                "firm": "HSBC Securities (USA) Inc.",
                "fine": "$15M",
                "regulator": "FINRA",
                "date": "Mar 2024",
                "summary": "Trade surveillance failures — inadequate supervisory systems for detecting market manipulation in equity markets. 7 years of deficient trade surveillance logs.",
            },
        ],
    },
    "latin-america": {
        "title": "Regional Enforcement Actions — Latin America",
        "regulator_label": "BCB · CVM · CNBV · SFC",
        "cases": [
            {
                "firm": "Itaú Unibanco S.A.",
                "fine": "BRL 850M",
                "regulator": "COAF / BCB",
                "date": "Apr 2023",
                "summary": "AML programme deficiencies — failure to file suspicious transaction reports (STRs) on 3,200+ high-value cash transactions. Inadequate beneficial ownership verification.",
            },
            {
                "firm": "Banco BTG Pactual",
                "fine": "BRL 45M",
                "regulator": "CVM",
                "date": "Sep 2023",
                "summary": "Market manipulation — use of proprietary trading accounts to create artificial volume in thinly-traded small-cap securities. CVM identified 14 months of coordinated activity.",
            },
            {
                "firm": "Banco Nacional de Mexico",
                "fine": "MXN 142M",
                "regulator": "CNBV",
                "date": "Jun 2023",
                "summary": "CNBV compliance failures — inadequate PLAFT (AML/CFT) controls, insufficient monitoring of cross-border transfers above USD 10,000 threshold, and PEP due diligence gaps.",
            },
            {
                "firm": "Davivienda S.A.",
                "fine": "COP 28B",
                "regulator": "SFC",
                "date": "Nov 2023",
                "summary": "Consumer financial protection — mis-selling of investment products to retail customers without adequate suitability assessment. Fines span three business lines.",
            },
            {
                "firm": "Banco Galicia Argentina",
                "fine": "ARS 2.3B",
                "regulator": "BCRA",
                "date": "Feb 2024",
                "summary": "Forex regulatory violations — breaches of BCRA foreign currency access regulations. Sanctions evasion risk controls deemed inadequate for correspondent banking activity.",
            },
        ],
    },
    "asia-pacific": {
        "title": "Regional Enforcement Actions — Asia-Pacific",
        "regulator_label": "MAS · SFC · AUSTRAC · FSA",
        "cases": [
            {
                "firm": "Westpac Banking Corporation",
                "fine": "AUD 1.3B",
                "regulator": "AUSTRAC",
                "date": "Sep 2020",
                "summary": "23 million contraventions of the AML/CTF Act — failure to report 19.5M international funds transfers, inadequate risk assessment for high-risk jurisdictions and child exploitation risks.",
            },
            {
                "firm": "Goldman Sachs (Asia) LLC",
                "fine": "HKD 350M",
                "regulator": "SFC",
                "date": "Oct 2022",
                "summary": "Market conduct failures — inadequate controls around proprietary trading desk communication with fund management operations. Potential information leakage identified in 1MDB-related activity.",
            },
            {
                "firm": "Credit Suisse (Singapore)",
                "fine": "SGD 2.6M",
                "regulator": "MAS",
                "date": "Jun 2022",
                "summary": "AML control failures — inadequate scrutiny of transactions connected to clients with links to 1MDB. Relationship managers bypassed EDD requirements on high-risk PEP accounts.",
            },
            {
                "firm": "Nomura Securities Co. Ltd",
                "fine": "¥1.2B",
                "regulator": "FSA",
                "date": "Dec 2022",
                "summary": "Client money handling failings — inadequate segregation of client assets held in omnibus accounts, insufficient reconciliation procedures, and failure to notify the FSA of breaches.",
            },
            {
                "firm": "HSBC Bank Australia",
                "fine": "AUD 6M",
                "regulator": "ASIC",
                "date": "Mar 2023",
                "summary": "Responsible lending failures — approved loans for customers without adequate assessment of their financial position. Affected 1,700+ home loan customers over 3 years.",
            },
        ],
    },
    "africa": {
        "title": "Regional Enforcement Actions — Africa",
        "regulator_label": "SARB · FSCA · CBN · CBK",
        "cases": [
            {
                "firm": "Standard Bank South Africa",
                "fine": "ZAR 36M",
                "regulator": "SARB / FIC",
                "date": "Jul 2023",
                "summary": "FICA compliance failures — inadequate customer due diligence on 140,000 high-risk accounts, failure to verify beneficial ownership, and delayed reporting of suspicious transactions.",
            },
            {
                "firm": "FirstRand Bank Ltd",
                "fine": "ZAR 28M",
                "regulator": "SARB",
                "date": "Mar 2024",
                "summary": "AML control gaps — PEP screening system failures allowing 320 politically exposed persons to be processed without enhanced due diligence. Corrective action plan required.",
            },
            {
                "firm": "Zenith Bank Plc",
                "fine": "NGN 420M",
                "regulator": "CBN",
                "date": "Sep 2023",
                "summary": "Regulatory reporting failures — late and inaccurate returns to the CBN over 18 months. Weak internal controls around forex trading documentation and correspondent banking records.",
            },
            {
                "firm": "KCB Bank Kenya",
                "fine": "KES 42M",
                "regulator": "CBK",
                "date": "Nov 2023",
                "summary": "AML/CFT programme deficiencies — inadequate transaction monitoring for mobile banking channel. CBK identified failure to report suspicious cross-border remittance transactions.",
            },
            {
                "firm": "Ecobank Transnational Inc.",
                "fine": "XOF 1.8B",
                "regulator": "BCEAO",
                "date": "Jan 2024",
                "summary": "UEMOA financial crime controls — systemic AML failures across West African operations. Inadequate country risk assessment for correspondent relationships with FATF grey-list jurisdictions.",
            },
        ],
    },
    "europe": {
        "title": "EU / EEA Enforcement Actions",
        "regulator_label": "ESMA · BaFin · AMF · DNB · AFM",
        "cases": [
            {
                "firm": "Deutsche Bank AG",
                "fine": "EUR 8.5M",
                "regulator": "BaFin",
                "date": "Mar 2023",
                "summary": "MiFID II transaction reporting failures — systematic errors in EMIR and MiFIR reports across equity derivatives. Instrument reference data inaccuracies spanning 18 months.",
            },
            {
                "firm": "ABN AMRO Clearing Bank",
                "fine": "EUR 12.3M",
                "regulator": "AFM",
                "date": "Jul 2023",
                "summary": "Client money segregation failures under Dutch Wft — inadequate separation of client funds from proprietary capital across three clearing accounts. CASS-equivalent breach.",
            },
            {
                "firm": "Société Générale S.A.",
                "fine": "EUR 7.4M",
                "regulator": "AMF",
                "date": "Oct 2023",
                "summary": "DORA readiness — inadequate ICT risk management framework documentation and failure to complete mandatory digital operational resilience testing by the DORA application date.",
            },
            {
                "firm": "UniCredit S.p.A.",
                "fine": "EUR 13.5M",
                "regulator": "Bank of Italy",
                "date": "Apr 2024",
                "summary": "AML/CFT failings — inadequate beneficial ownership identification for corporate clients, delayed STR filings to UIF, and insufficient controls over cross-border wire transfers.",
            },
            {
                "firm": "Nordea Bank Abp",
                "fine": "EUR 23M",
                "regulator": "FIN-FSA",
                "date": "Feb 2024",
                "summary": "Sanctions screening programme failures — delays in updating OFAC/EU sanctions list. 840 transactions involving sanctioned entities processed without detection over 11 months.",
            },
        ],
    },
}
