"""
Cyber Intelligence Reference Database
Threat intelligence from national cyber bodies across all Govisk regions.
Updated: November 2026
Covers: NCSC · FCA/CBEST · ICO · CISA · FBI · CCCS · CERT.br · CSA ·
        JPCERT/CC · ACSC · ENISA · CERT-EU · BSI · ngCERT · CSIRT-SA
"""

SOURCED_DATE = "2026-11-18"

# =============================================================================
# CYBER BODY METADATA — per region slug
# =============================================================================
CYBER_BODIES = {
    "uk": [
        {"name": "NCSC",      "full": "National Cyber Security Centre",                    "url": "https://www.ncsc.gov.uk/"},
        {"name": "FCA/CBEST", "full": "FCA Cyber Threat-Led Penetration Testing",          "url": "https://www.fca.org.uk/firms/cyber-resilience"},
        {"name": "CPNI",      "full": "Centre for the Protection of National Infrastructure","url": "https://www.cpni.gov.uk/"},
        {"name": "ICO",       "full": "Information Commissioner's Office",                  "url": "https://ico.org.uk/"},
        {"name": "OFCOM",     "full": "Office of Communications",                           "url": "https://www.ofcom.org.uk/research-and-data/telecoms-research/security"},
    ],
    "north-america": [
        {"name": "CISA",      "full": "Cybersecurity and Infrastructure Security Agency",   "url": "https://www.cisa.gov/"},
        {"name": "NSA/CNMF",  "full": "NSA / Cyber National Mission Force",                 "url": "https://www.nsa.gov/cybersecurity/"},
        {"name": "FBI Cyber", "full": "FBI Cyber Division",                                 "url": "https://www.fbi.gov/investigate/cyber"},
        {"name": "SEC",       "full": "Securities and Exchange Commission",                 "url": "https://www.sec.gov/cybersecurity"},
        {"name": "CCCS",      "full": "Canadian Centre for Cyber Security",                 "url": "https://www.cyber.gc.ca/"},
        {"name": "CSE",       "full": "Communications Security Establishment",              "url": "https://www.cse-cst.gc.ca/"},
    ],
    "latin-america": [
        {"name": "CERT.br",   "full": "Brazil National CERT (NIC.br)",                      "url": "https://www.cert.br/"},
        {"name": "ANPD",      "full": "Autoridade Nacional de Proteção de Dados",            "url": "https://www.gov.br/anpd/"},
        {"name": "UNAM-CERT", "full": "Mexico National CERT",                               "url": "https://www.cert.unam.mx/"},
        {"name": "CGCYBER",   "full": "Mexico Cyber Defence Command",                       "url": "https://www.gob.mx/sedena"},
        {"name": "GAFILAT",   "full": "Grupo de Acción Financiera de Latinoamérica",         "url": "https://www.gafilat.org/"},
    ],
    "asia-pacific": [
        {"name": "CSA",        "full": "Cyber Security Agency of Singapore",                "url": "https://www.csa.gov.sg/"},
        {"name": "MAS TRM",    "full": "MAS Technology Risk Management",                    "url": "https://www.mas.gov.sg/regulation/guidelines/technology-risk-management-guidelines"},
        {"name": "JPCERT/CC",  "full": "Japan CERT Coordination Centre",                    "url": "https://www.jpcert.or.jp/english/"},
        {"name": "NISC",       "full": "Japan National Incident Readiness & Strategy",      "url": "https://www.nisc.go.jp/eng/"},
        {"name": "CERT-In",    "full": "India Computer Emergency Response Team",            "url": "https://www.cert-in.org.in/"},
        {"name": "ASD/ACSC",   "full": "Australian Signals Directorate / ACSC",             "url": "https://www.cyber.gov.au/"},
        {"name": "CNCERT",     "full": "China National Computer Network Emergency Response","url": "https://www.cert.org.cn/"},
    ],
    "africa": [
        {"name": "ngCERT",     "full": "Nigeria Computer Emergency Response Team",          "url": "https://www.ngcert.gov.ng/"},
        {"name": "CSIRT-SA",   "full": "South Africa National CSIRT",                       "url": "https://www.csirt.org.za/"},
        {"name": "KE-CIRT/CC", "full": "Kenya CERT (Communications Authority)",             "url": "https://www.ca.go.ke/consumers/kecirtcc"},
        {"name": "AFRIPOL",    "full": "African Union Cybercrime Coordination",             "url": "https://www.afripol.africaunion.org/"},
        {"name": "SSASC",      "full": "South Africa State Security Agency",                "url": "https://www.ssa.gov.za/"},
    ],
    "europe": [
        {"name": "ENISA",      "full": "EU Agency for Cybersecurity",                       "url": "https://www.enisa.europa.eu/"},
        {"name": "CERT-EU",    "full": "EU Institutions CERT",                              "url": "https://cert.europa.eu/"},
        {"name": "BSI",        "full": "German Federal Office for Information Security",    "url": "https://www.bsi.bund.de/EN/"},
        {"name": "ANSSI",      "full": "France National Information Systems Security Agency","url": "https://www.ssi.gouv.fr/en/"},
        {"name": "NCSC-NL",    "full": "Netherlands National Cyber Security Centre",        "url": "https://english.ncsc.nl/"},
        {"name": "CCN-CERT",   "full": "Spain National Cryptologic Centre CERT",            "url": "https://www.ccn-cert.cni.es/en/"},
        {"name": "Europol EC3","full": "European Cybercrime Centre",                        "url": "https://www.europol.europa.eu/about-europol/european-cybercrime-centre-ec3"},
    ],
}

# =============================================================================
# UK — NCSC · FCA/CBEST · CPNI · ICO · OFCOM
# =============================================================================
UK_CYBER_NEWS = [
    {
        "date": "2026-10",
        "regulator": "NCSC",
        "country": "United Kingdom",
        "type": "Threat Advisory",
        "headline": "NCSC critical advisory — ransomware groups escalating attacks on UK financial sector",
        "detail": (
            "NCSC issued a critical advisory warning of a marked escalation in ransomware targeting "
            "UK financial services firms, particularly mid-tier asset managers and payment processors. "
            "The advisory specifically names LockBit 4.0, ALPHV/BlackCat successors, and Cl0p as "
            "active threat actors. Firms are directed to: patch CVE-2024-3400 (PAN-OS) and CVE-2025-1974 "
            "(Kubernetes) immediately; implement offline backups; activate MFA on all remote access; "
            "review third-party VPN credentials. NCSC CISP portal updated with indicators of compromise."
        ),
        "tags": ["Ransomware", "Financial Sector", "LockBit", "ALPHV", "NCSC"],
        "severity": "RED",
        "url": "https://www.ncsc.gov.uk/collection/ransomware",
    },
    {
        "date": "2026-09",
        "regulator": "NCSC",
        "country": "United Kingdom",
        "type": "Annual Report",
        "headline": "NCSC Annual Cyber Threat Report 2026 — state-sponsored attacks at record high",
        "detail": (
            "NCSC published its Annual Cyber Threat Report 2026, citing a record number of "
            "state-sponsored cyber incidents targeting UK critical national infrastructure. "
            "Financial services ranked second-most targeted sector (after government). "
            "Russia (Cozy Bear/APT29), China (Volt Typhoon), Iran (APT34), and North Korea "
            "(Lazarus Group targeting crypto/SWIFT) all named as active threats. "
            "NCSC handled 2,049 cyber incidents in 2025/26 — 20% increase year-on-year."
        ),
        "tags": ["State Actors", "APT", "Annual Report", "Critical Infrastructure", "NCSC"],
        "severity": "RED",
        "url": "https://www.ncsc.gov.uk/section/annual-review/2026",
    },
    {
        "date": "2026-08",
        "regulator": "ICO",
        "country": "United Kingdom",
        "type": "Enforcement",
        "headline": "ICO fines financial services firm £4.4M — inadequate security controls under UK GDPR",
        "detail": (
            "ICO imposed a £4.4 million fine on a UK financial services firm for failing to implement "
            "adequate technical and organisational security measures under UK GDPR Article 32. "
            "The firm failed to: encrypt sensitive customer data at rest; implement MFA on critical "
            "systems; conduct regular penetration testing; maintain an adequate patch management programme. "
            "The incident exposed 340,000 customer records including account numbers and credit scores. "
            "ICO confirmed this is a signal of a tougher enforcement approach for 2026/27."
        ),
        "tags": ["ICO", "UK GDPR", "Enforcement", "Data Breach", "Article 32"],
        "severity": "RED",
        "url": "https://ico.org.uk/action-weve-taken/enforcement/",
    },
    {
        "date": "2026-07",
        "regulator": "FCA/CBEST",
        "country": "United Kingdom",
        "type": "Framework Update",
        "headline": "FCA updates CBEST framework — AI-driven threat simulation and cloud scenarios now required",
        "detail": (
            "FCA published an updated CBEST framework (v4.0) requiring financial firms to incorporate "
            "AI-assisted threat actor simulation and cloud-specific attack scenarios into their "
            "threat-led penetration tests. Firms in scope: banks, insurers, payment infrastructure, "
            "market infrastructure. New requirements: annual CBEST cycle (previously biennial for some); "
            "cloud penetration testing must cover identity and access management (IAM) misconfigurations; "
            "AI-assisted spear phishing scenarios for executive targeting; results must be reported to "
            "the FCA within 30 days of test completion."
        ),
        "tags": ["CBEST", "FCA", "Penetration Testing", "AI", "Cloud"],
        "severity": "AMBER",
        "url": "https://www.fca.org.uk/firms/cyber-resilience/cbest",
    },
    {
        "date": "2026-06",
        "regulator": "OFCOM",
        "country": "United Kingdom",
        "type": "Enforcement",
        "headline": "OFCOM issues network security duty enforcement notices to 3 telecoms operators",
        "detail": (
            "OFCOM issued enforcement notices to three UK telecoms operators for breaches of the "
            "Network and Information Systems (NIS) Regulations 2018 and the Telecoms Security Act 2021. "
            "Failures identified: inadequate SS7 signalling security; insufficient monitoring for "
            "SIM-swap fraud patterns; failure to report security incidents within 24-hour deadline. "
            "Financial firms relying on SMS-based OTP authentication must review dependency on "
            "telecoms infrastructure security as part of their operational resilience assessments."
        ),
        "tags": ["OFCOM", "Telecoms Security", "NIS Regulations", "SS7", "SIM Swap"],
        "severity": "AMBER",
        "url": "https://www.ofcom.org.uk/phones-and-broadband/telecoms-security",
    },
    {
        "date": "2026-05",
        "regulator": "CPNI",
        "country": "United Kingdom",
        "type": "Guidance",
        "headline": "CPNI updated protective security guidance for financial critical infrastructure",
        "detail": (
            "CPNI published updated Protective Security Guidance for organisations designated as "
            "critical national infrastructure within the financial sector. Key updates: insider threat "
            "detection requirements for privileged access holders; physical-cyber convergence controls "
            "for data centres and trading floors; supply chain security assessment mandatory for "
            "third-party technology providers. Guidance aligns with NCSC CAF (Cyber Assessment Framework) "
            "and FCA operational resilience requirements under PS21/3 and PS26/2."
        ),
        "tags": ["CPNI", "Critical Infrastructure", "Insider Threat", "Supply Chain", "CAF"],
        "severity": "GREEN",
        "url": "https://www.cpni.gov.uk/protective-security-guidance",
    },
]

# =============================================================================
# NORTH AMERICA — CISA · NSA · FBI · SEC · CCCS · CSE
# =============================================================================
NORTH_AMERICA_CYBER_NEWS = [
    {
        "date": "2026-10",
        "regulator": "CISA",
        "country": "USA",
        "type": "Known Exploited Vulnerabilities",
        "headline": "CISA KEV — 7 new exploited vulnerabilities affecting financial sector software added",
        "detail": (
            "CISA added 7 vulnerabilities to its Known Exploited Vulnerabilities (KEV) catalog "
            "confirmed as actively exploited in attacks targeting the financial sector. "
            "Critical entries: CVE-2026-1134 (Cisco IOS XE web UI RCE, CVSS 10.0); "
            "CVE-2026-0892 (Citrix NetScaler auth bypass); CVE-2025-4471 (Palo Alto PAN-OS). "
            "CISA Binding Operational Directive 22-01 applies to federal agencies; "
            "private financial institutions are strongly urged to patch within 15 days. "
            "FS-ISAC threat-sharing alert simultaneously issued to member firms."
        ),
        "tags": ["CISA", "KEV", "CVE", "Vulnerabilities", "Financial Sector"],
        "severity": "RED",
        "url": "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
    },
    {
        "date": "2026-09",
        "regulator": "FBI Cyber",
        "country": "USA",
        "type": "Threat Advisory",
        "headline": "FBI warns Scattered Spider actively targeting US financial sector cloud environments",
        "detail": (
            "FBI Cyber Division issued a Private Industry Notification (PIN) warning that Scattered Spider "
            "(UNC3944/Octo Tempest) is conducting advanced social engineering campaigns targeting "
            "US financial sector help desks and IT support personnel to gain access to cloud environments. "
            "Tactics: impersonating employees to bypass MFA; SIM swapping executive mobile numbers; "
            "vishing attacks on tier-1 IT staff. Targets in 2026: three major US brokerages and two "
            "insurance firms. FBI urges: mandatory video verification for password resets; "
            "out-of-band confirmation for privileged access changes."
        ),
        "tags": ["FBI", "Scattered Spider", "Social Engineering", "Cloud", "Vishing"],
        "severity": "RED",
        "url": "https://www.ic3.gov/",
    },
    {
        "date": "2026-08",
        "regulator": "CISA/NSA",
        "country": "USA",
        "type": "Joint Advisory",
        "headline": "CISA/NSA/CCCS joint advisory — PRC state actors (Volt Typhoon) in financial networks",
        "detail": (
            "CISA, NSA, FBI, CCCS and partner agencies issued a joint advisory confirming Volt Typhoon "
            "(PRC state-sponsored) has pre-positioned access in US and Canadian financial sector "
            "networks, likely for disruption capability rather than immediate exfiltration. "
            "Techniques: living-off-the-land (LOtL) using native tools; targeting SOHO routers as "
            "proxy infrastructure; exploiting OT/IT boundary systems in financial data centres. "
            "Firms urged to hunt for indicators of compromise, review SOHO network devices, and "
            "implement network segmentation between trading and administrative systems."
        ),
        "tags": ["Volt Typhoon", "PRC", "State Actor", "Critical Infrastructure", "LOtL"],
        "severity": "RED",
        "url": "https://www.cisa.gov/news-events/cybersecurity-advisories",
    },
    {
        "date": "2026-09",
        "regulator": "SEC",
        "country": "USA",
        "type": "Enforcement",
        "headline": "SEC charges investment firm $2.9M — failure to disclose material cyber incident within 4 days",
        "detail": (
            "SEC charged a registered investment adviser with violating the cybersecurity incident "
            "disclosure rules (Item 1.05 of Form 8-K) for failing to disclose a material ransomware "
            "attack within the required 4 business days. The firm delayed disclosure by 23 days while "
            "attempting to negotiate with the threat actor. Additionally charged with inadequate "
            "cybersecurity policies and failure to maintain required records of the incident response. "
            "Total penalty: $2,900,000. First major enforcement action under the 2023 cyber disclosure rules."
        ),
        "tags": ["SEC", "Form 8-K", "Disclosure", "Ransomware", "Enforcement"],
        "severity": "RED",
        "url": "https://www.sec.gov/enforce/cyber-enforcement",
    },
    {
        "date": "2026-07",
        "regulator": "CCCS",
        "country": "Canada",
        "type": "Threat Bulletin",
        "headline": "CCCS threat bulletin — LockBit affiliate activity resurging in Canadian banking sector",
        "detail": (
            "Canadian Centre for Cyber Security issued a threat bulletin confirming resurgence of "
            "LockBit affiliate activity targeting Canadian banking and financial infrastructure "
            "following partial law enforcement disruption. Affiliates now deploying customised "
            "variants to evade detection. CCCS observed 11 confirmed incidents in Canadian financial "
            "sector in Q2/Q3 2026. Recommended controls: network segmentation; offline backup testing; "
            "LSASS memory protection; disabling WMIC for non-administrative accounts."
        ),
        "tags": ["CCCS", "LockBit", "Ransomware", "Canada", "Banking"],
        "severity": "RED",
        "url": "https://www.cyber.gc.ca/en/alerts-advisories",
    },
    {
        "date": "2026-06",
        "regulator": "CSE",
        "country": "Canada",
        "type": "Annual Assessment",
        "headline": "CSE National Cyber Threat Assessment 2026 — ransomware-as-a-service dominant threat vector",
        "detail": (
            "Communications Security Establishment published its National Cyber Threat Assessment 2026. "
            "Key findings: ransomware-as-a-service (RaaS) remains the most disruptive cyber threat to "
            "Canadian financial institutions; state-sponsored actors (Russia, China, Iran, DPRK) "
            "increasingly targeting financial infrastructure for pre-positioning; Canadian financial "
            "sector experienced 34% increase in reported cyber incidents in 2025. "
            "CSE recommends adoption of Cyber Essentials framework as baseline for all financial firms."
        ),
        "tags": ["CSE", "RaaS", "Annual Assessment", "State Actors", "Canada"],
        "severity": "AMBER",
        "url": "https://www.cse-cst.gc.ca/en/publication/ncta-2026",
    },
]

# =============================================================================
# LATIN AMERICA — CERT.br · ANPD · UNAM-CERT · CGCYBER · GAFILAT
# =============================================================================
LATIN_AMERICA_CYBER_NEWS = [
    {
        "date": "2026-10",
        "regulator": "CERT.br",
        "country": "Brazil",
        "type": "Malware Alert",
        "headline": "CERT.br alert — Grandoreiro banking trojan resurgence targeting Brazilian financial apps",
        "detail": (
            "CERT.br issued an urgent alert on the resurgence of Grandoreiro banking trojan, "
            "a modular remote-access trojan specifically targeting Brazilian financial institution "
            "customers. New variant (Grandoreiro v7) evades current AV signatures and targets "
            "mobile banking apps via overlay attacks. Distributed via phishing campaigns impersonating "
            "Receita Federal (tax authority) and major Brazilian banks. Over 900 Brazilian financial "
            "institutions and 1,500 banks in 60 countries previously targeted. "
            "FEBRABAN has issued a parallel alert to member banks."
        ),
        "tags": ["CERT.br", "Grandoreiro", "Banking Trojan", "Brazil", "Mobile Banking"],
        "severity": "RED",
        "url": "https://www.cert.br/alertas/",
    },
    {
        "date": "2026-09",
        "regulator": "CGCYBER",
        "country": "Mexico",
        "type": "Critical Alert",
        "headline": "Mexico CGCYBER elevates critical infrastructure cyber threat level to HIGH",
        "detail": (
            "Mexico's Cyber Defence Command (CGCYBER) elevated the cyber threat level for critical "
            "financial infrastructure to HIGH following confirmed intrusion attempts against two "
            "major Mexican banks and the SPEI interbank payment system. CGCYBER attributes the "
            "campaign to a threat actor with state-level capabilities. CNBV and Banco de Mexico "
            "issued emergency security directives to all supervised financial institutions. "
            "SPEI transaction monitoring enhanced; anomaly detection thresholds lowered. "
            "Firms with Mexican correspondent banking relationships should review access controls."
        ),
        "tags": ["CGCYBER", "SPEI", "Critical Infrastructure", "Mexico", "Interbank"],
        "severity": "RED",
        "url": "https://www.gob.mx/sedena/acciones-y-programas/ciberdefensa",
    },
    {
        "date": "2026-08",
        "regulator": "ANPD",
        "country": "Brazil",
        "type": "Enforcement",
        "headline": "ANPD fines fintech R$7.2M — LGPD breach notification failure and inadequate controls",
        "detail": (
            "Brazil's ANPD imposed a R$7.2 million fine on a licensed fintech for two violations: "
            "(1) failure to notify ANPD and affected data subjects within 72 hours of a data breach "
            "as required by LGPD Article 48; (2) absence of adequate technical and administrative "
            "security measures under LGPD Article 46. The breach exposed 2.1 million customer "
            "financial records including CPF numbers, account balances, and transaction histories. "
            "ANPD has signalled further enforcement actions targeting financial sector in H2 2026."
        ),
        "tags": ["ANPD", "LGPD", "Data Breach", "Enforcement", "Brazil"],
        "severity": "AMBER",
        "url": "https://www.gov.br/anpd/pt-br/assuntos/noticias",
    },
    {
        "date": "2026-07",
        "regulator": "CSIRT-CO",
        "country": "Colombia",
        "type": "Alert",
        "headline": "Colombia CSIRT — phishing surge targeting Bancolombia and Davivienda customers",
        "detail": (
            "Colombia's national CSIRT issued an alert on a coordinated phishing campaign "
            "targeting customers of major Colombian banks using convincing cloned portals. "
            "Campaign uses SMS smishing and WhatsApp lures impersonating bank security alerts. "
            "Over 45,000 attempted credential thefts recorded in July 2026. "
            "SFC (Superintendencia Financiera) has instructed all supervised entities to "
            "enhance anti-phishing monitoring and customer communications. "
            "GAFILAT cybercrime coordination group notified given cross-border infrastructure."
        ),
        "tags": ["CSIRT", "Phishing", "Colombia", "Banking", "Smishing"],
        "severity": "AMBER",
        "url": "https://www.colcert.gov.co/",
    },
    {
        "date": "2026-06",
        "regulator": "GAFILAT",
        "country": "Regional",
        "type": "Advisory",
        "headline": "GAFILAT advisory — crypto-based financial cybercrime schemes proliferating across LatAm",
        "detail": (
            "GAFILAT issued a regional advisory on the proliferation of crypto-based financial "
            "cybercrime schemes across Latin America, specifically pig-butchering scams (SHA ZHU PAN), "
            "DeFi rug-pulls targeting retail investors, and crypto exchange hacks exploiting weak "
            "wallet key management. Advisory notes: five GAFILAT member jurisdictions recorded "
            "significant crypto-related cyber losses in H1 2026. Financial institutions with "
            "crypto exposure must implement enhanced transaction monitoring for typologies outlined "
            "in GAFILAT Guidance Note 15/2026."
        ),
        "tags": ["GAFILAT", "Crypto", "Pig Butchering", "DeFi", "Financial Crime"],
        "severity": "AMBER",
        "url": "https://www.gafilat.org/index.php/en/",
    },
]

# =============================================================================
# ASIA-PACIFIC — CSA · MAS TRM · JPCERT/CC · NISC · CERT-In · ASD/ACSC · CNCERT
# =============================================================================
ASIA_CYBER_NEWS = [
    {
        "date": "2026-10",
        "regulator": "CSA",
        "country": "Singapore",
        "type": "Threat Alert",
        "headline": "CSA SingCERT — Volt Typhoon pre-positioning detected in Singapore financial sector networks",
        "detail": (
            "Singapore's Cyber Security Agency (CSA) SingCERT issued an alert confirming detection "
            "of Volt Typhoon (PRC state-sponsored) activity pre-positioned within Singapore financial "
            "sector networks, mirroring patterns seen in US and Australian advisories. "
            "CSA coordinating with MAS and affected firms under the Cybersecurity Act s.9 information "
            "sharing framework. Indicators of compromise distributed to MAS-supervised financial "
            "institutions via secure channel. Firms urged to audit all SOHO/edge device access logs "
            "and review privileged access credentials immediately."
        ),
        "tags": ["CSA", "Volt Typhoon", "PRC", "Singapore", "Financial Sector"],
        "severity": "RED",
        "url": "https://www.csa.gov.sg/singcert/Advisories",
    },
    {
        "date": "2026-09",
        "regulator": "JPCERT/CC",
        "country": "Japan",
        "type": "APT Alert",
        "headline": "JPCERT/CC alert — APT10 campaign targeting Japanese financial institutions via supply chain",
        "detail": (
            "JPCERT/CC published an alert on an APT10 (Stone Panda, MenuPass — PRC-linked) campaign "
            "targeting Japanese financial institutions through software supply chain compromise. "
            "Attackers compromised update mechanisms of two Japanese financial software vendors "
            "to distribute malicious updates to downstream clients including three major securities "
            "firms and two regional banks. JPCERT/CC has coordinated with affected vendors; patches "
            "available. FSA issued emergency directive to all supervised firms to verify software "
            "integrity and review update processes."
        ),
        "tags": ["JPCERT/CC", "APT10", "Supply Chain", "Japan", "Securities"],
        "severity": "RED",
        "url": "https://www.jpcert.or.jp/english/at/",
    },
    {
        "date": "2026-08",
        "regulator": "CERT-In",
        "country": "India",
        "type": "Emergency Directive",
        "headline": "CERT-In emergency directive — critical vulnerabilities in Indian core banking software",
        "detail": (
            "CERT-In issued an emergency directive under Section 70B of the IT Act regarding "
            "critical vulnerabilities (CVE-2026-5892, CVE-2026-5893) in widely-used Indian core "
            "banking software affecting 47 scheduled commercial banks. Vulnerabilities allow "
            "unauthenticated remote code execution. RBI issued a parallel circular requiring "
            "all affected banks to patch within 48 hours or implement network-level controls. "
            "CERT-In 6-hour mandatory reporting obligation applies to any exploitation. "
            "NCA also notified given potential systemic risk."
        ),
        "tags": ["CERT-In", "RBI", "Core Banking", "CVE", "India"],
        "severity": "RED",
        "url": "https://www.cert-in.org.in/s2cMainServlet?pageid=PUBVLNOTES01",
    },
    {
        "date": "2026-08",
        "regulator": "ASD/ACSC",
        "country": "Australia",
        "type": "Joint Advisory",
        "headline": "ACSC co-signed advisory — ransomware threats escalating against Australian financial sector",
        "detail": (
            "ASD's Australian Cyber Security Centre (ACSC), co-signed with CISA, NCSC-UK, CCCS, "
            "issued an advisory on escalating ransomware threats to Australian financial services. "
            "Specifically names Play ransomware, Black Basta, and BianLian as active threats. "
            "Australian financial sector experienced 28 ransomware incidents in 2026 YTD. "
            "APRA CPS 234 information security requirements mandate timely notification to APRA "
            "of cyber incidents. ACSC Essential Eight Maturity Model Level 2 is minimum recommended "
            "baseline for all APRA-regulated entities."
        ),
        "tags": ["ACSC", "Ransomware", "APRA CPS 234", "Australia", "Essential Eight"],
        "severity": "RED",
        "url": "https://www.cyber.gov.au/resources-business-and-government/advisories",
    },
    {
        "date": "2026-07",
        "regulator": "MAS TRM",
        "country": "Singapore",
        "type": "Notice",
        "headline": "MAS TRM Notice — enhanced cloud risk management and AI system controls required",
        "detail": (
            "MAS published revised Technology Risk Management (TRM) Notice MAS-TRM-2026-01 requiring "
            "all MAS-regulated financial institutions to implement enhanced controls for cloud "
            "environments and AI systems. New requirements: multi-cloud access management reviews "
            "annually; AI system explainability and bias audits for algorithmic trading and credit "
            "decisioning; API security testing for open banking interfaces; cyber incident notification "
            "to MAS within 1 hour of discovery of significant incidents (unchanged threshold). "
            "Compliance deadline: 31 March 2027."
        ),
        "tags": ["MAS", "TRM", "Cloud Security", "AI", "Singapore"],
        "severity": "AMBER",
        "url": "https://www.mas.gov.sg/regulation/notices/",
    },
    {
        "date": "2026-06",
        "regulator": "CNCERT",
        "country": "China",
        "type": "Threat Assessment",
        "headline": "CNCERT H1 2026 report — Chinese financial sector facing APT and supply chain threats",
        "detail": (
            "CNCERT published its H1 2026 internet security situation report noting significant "
            "APT activity targeting Chinese financial sector infrastructure. Key threats: "
            "exploitation of domestic financial software vulnerabilities; targeted attacks on "
            "securities trading platforms; phishing campaigns targeting bank customers. "
            "NFRA and CSRC coordinating with CNCERT on cybersecurity assessments for financial "
            "institutions. Data localisation under PIPL and CSL applicable to all incident "
            "data — cross-border reporting requires MIIT approval."
        ),
        "tags": ["CNCERT", "APT", "China", "Financial Sector", "PIPL"],
        "severity": "AMBER",
        "url": "https://www.cert.org.cn/publish/main/8/index.html",
    },
]

# =============================================================================
# AFRICA — ngCERT · CSIRT-SA · KE-CIRT/CC · AFRIPOL · SSASC · ESAAMLG
# =============================================================================
AFRICA_CYBER_NEWS = [
    {
        "date": "2026-10",
        "regulator": "ngCERT",
        "country": "Nigeria",
        "type": "Emergency Alert",
        "headline": "ngCERT emergency alert — banking trojan wave targeting Nigerian mobile financial apps",
        "detail": (
            "Nigeria's ngCERT issued an emergency alert on a coordinated banking trojan campaign "
            "targeting Nigerian mobile banking applications and USSD-based financial services. "
            "The trojan (dubbed 'FinStealer-NG') uses overlay attacks on mobile apps of GTBank, "
            "Zenith Bank, Access Bank, and mobile money providers. Distributed via fraudulent "
            "Google Play and third-party APK links. Over 12,000 devices confirmed compromised "
            "in October 2026. CBN directed all DMBs to implement app integrity verification "
            "and enhanced transaction anomaly detection within 72 hours."
        ),
        "tags": ["ngCERT", "Banking Trojan", "Nigeria", "Mobile Banking", "CBN"],
        "severity": "RED",
        "url": "https://www.ngcert.gov.ng/",
    },
    {
        "date": "2026-09",
        "regulator": "CSIRT-SA",
        "country": "South Africa",
        "type": "Ransomware Advisory",
        "headline": "CSIRT-SA advisory — ransomware targeting South African banks and insurance firms",
        "detail": (
            "South Africa's CSIRT-SA issued an advisory on targeted ransomware campaigns against "
            "South African financial institutions. Two major incidents confirmed: a mid-tier bank "
            "and a large insurer both suffered ransomware deployment with demands exceeding R50M. "
            "CSIRT-SA attributes to RansomHub and Medusa ransomware groups. SARB and FSCA jointly "
            "issued a supervisory letter requiring all regulated entities to test backup restoration "
            "capabilities and report results within 30 days. POPIA breach notification obligations "
            "triggered for both affected entities."
        ),
        "tags": ["CSIRT-SA", "Ransomware", "South Africa", "POPIA", "FSCA"],
        "severity": "RED",
        "url": "https://www.csirt.org.za/",
    },
    {
        "date": "2026-08",
        "regulator": "KE-CIRT/CC",
        "country": "Kenya",
        "type": "Fraud Alert",
        "headline": "KE-CIRT/CC — SIM swap fraud campaigns targeting M-Pesa and banking apps at scale",
        "detail": (
            "Kenya's KE-CIRT/CC issued an alert on large-scale SIM swap fraud campaigns targeting "
            "M-Pesa and mobile banking customers. The campaign exploits insider access at Kenyan "
            "mobile network operators to perform unauthorised SIM replacements, then drain mobile "
            "money and banking accounts. CBK and CA Kenya issued joint guidance requiring financial "
            "institutions to implement transaction cooling periods for accounts where SIM changes "
            "occurred within 48 hours; device binding for high-value transactions; enhanced MNO "
            "identity verification requirements."
        ),
        "tags": ["KE-CIRT/CC", "SIM Swap", "M-Pesa", "Kenya", "Mobile Money"],
        "severity": "RED",
        "url": "https://www.ca.go.ke/consumers/kecirtcc",
    },
    {
        "date": "2026-07",
        "regulator": "AFRIPOL",
        "country": "Regional",
        "type": "Operation",
        "headline": "AFRIPOL Operation Serengeti II — 1,006 suspects arrested in Africa-wide cyber fraud",
        "detail": (
            "AFRIPOL and INTERPOL announced the results of Operation Serengeti II, arresting 1,006 "
            "suspects across 19 African countries for cyber-enabled financial fraud. Operations "
            "dismantled: online investment fraud networks causing $193M in losses; romance scam "
            "operations; ransomware groups targeting African financial institutions. "
            "Four cyber crime command centres seized in Nigeria, Kenya, South Africa, and Cameroon. "
            "Financial institutions across Africa should review transaction monitoring for typologies "
            "identified in AFRIPOL's post-operation intelligence bulletin."
        ),
        "tags": ["AFRIPOL", "INTERPOL", "Cybercrime", "Operation Serengeti", "Africa"],
        "severity": "RED",
        "url": "https://www.afripol.africaunion.org/",
    },
    {
        "date": "2026-06",
        "regulator": "ESAAMLG",
        "country": "Regional",
        "type": "Advisory",
        "headline": "ESAAMLG cyber-financial crime advisory — crypto-enabled fraud surging across East Africa",
        "detail": (
            "ESAAMLG published a typologies advisory on crypto-enabled financial cybercrime across "
            "East and Southern Africa, noting a 340% year-on-year increase in crypto fraud losses. "
            "Key typologies: fake investment platforms (pig butchering); crypto ATM fraud; "
            "NFT-based money laundering; cross-border crypto transfers to avoid AML controls. "
            "Financial institutions with East African correspondent relationships must update "
            "their crypto exposure risk assessments and implement enhanced transaction monitoring "
            "for crypto-to-fiat conversion activities."
        ),
        "tags": ["ESAAMLG", "Crypto", "Financial Crime", "East Africa", "AML"],
        "severity": "AMBER",
        "url": "https://www.esaamlg.org/",
    },
]

# =============================================================================
# EUROPE — ENISA · CERT-EU · BSI · ANSSI · NCSC-NL · CCN-CERT · Europol EC3
# =============================================================================
EUROPE_CYBER_NEWS = [
    {
        "date": "2026-10",
        "regulator": "ENISA",
        "country": "EU",
        "type": "Annual Threat Landscape",
        "headline": "ENISA Threat Landscape 2026 — ransomware remains #1 threat to EU financial sector",
        "detail": (
            "ENISA published its annual Threat Landscape 2026 report identifying ransomware as the "
            "most significant cyber threat to EU financial services for the fourth consecutive year. "
            "Key findings: 54% increase in ransomware attacks against EU financial institutions; "
            "DDoS attacks against EU banking sector doubled following geopolitical tensions; "
            "AI-generated phishing (spear-phishing at scale) identified as an emerging critical threat. "
            "Report notes DORA has improved incident reporting — ENISA received 847 major ICT incident "
            "reports from EU financial entities in the first 6 months of DORA implementation."
        ),
        "tags": ["ENISA", "Threat Landscape", "Ransomware", "DDoS", "DORA"],
        "severity": "RED",
        "url": "https://www.enisa.europa.eu/publications/enisa-threat-landscape-2026",
    },
    {
        "date": "2026-09",
        "regulator": "CERT-EU",
        "country": "EU",
        "type": "Critical Advisory",
        "headline": "CERT-EU — APT29 (Cozy Bear) campaign targeting EU financial institutions and ECB networks",
        "detail": (
            "CERT-EU issued a CRITICAL advisory on an APT29 (Cozy Bear — Russia SVR) campaign "
            "targeting EU financial institutions and infrastructure connected to the European Central "
            "Bank and EBA. Attack vector: spear-phishing of senior finance ministry officials; "
            "exploitation of CVE-2026-2891 (Microsoft Exchange zero-day) for initial access. "
            "CERT-EU coordinating with Europol EC3 and national NCAs. Affected EU member states: "
            "Germany, France, Netherlands, and Belgium. Firms with ECB/EBA connectivity should "
            "urgently review access logs and implement emergency network monitoring."
        ),
        "tags": ["CERT-EU", "APT29", "Cozy Bear", "ECB", "Russia"],
        "severity": "RED",
        "url": "https://cert.europa.eu/publications/threat-intelligence/",
    },
    {
        "date": "2026-09",
        "regulator": "BSI",
        "country": "Germany",
        "type": "Warning",
        "headline": "BSI Cyber-Sicherheitswarnung — critical vulnerability in German banking infrastructure",
        "detail": (
            "Germany's BSI issued a Cyber-Sicherheitswarnung (Threat Level RED) on a critical "
            "vulnerability in EBICS (Electronic Banking Internet Communication Standard) client "
            "software used by German banks for secure payment file transfer. Vulnerability allows "
            "man-in-the-middle attacks on EBICS sessions. BaFin and Deutsche Bundesbank issued "
            "joint circular to all German credit institutions. Firms must update EBICS client "
            "software to patched version within 5 business days or implement compensating controls. "
            "BSI estimates 2,400 German financial institutions use affected software."
        ),
        "tags": ["BSI", "EBICS", "Germany", "Banking", "Vulnerability"],
        "severity": "RED",
        "url": "https://www.bsi.bund.de/EN/Themen/Unternehmen-und-Organisationen/Cyber-Sicherheitslage/Cyber-Sicherheitswarnungen/cyber-sicherheitswarnungen_node.html",
    },
    {
        "date": "2026-08",
        "regulator": "Europol EC3",
        "country": "EU",
        "type": "Operation",
        "headline": "Europol EC3 Operation BIOS — €40M crypto fraud network dismantled across 12 EU countries",
        "detail": (
            "Europol's European Cybercrime Centre (EC3) coordinated Operation BIOS, dismantling "
            "a €40 million crypto investment fraud network operating across 12 EU member states. "
            "Operation resulted in 68 arrests, seizure of €12M in crypto assets, and takedown of "
            "29 fraudulent investment platforms. The network used AI-generated personas, "
            "deepfake celebrity endorsements, and fake trading platforms to defraud over 4,000 victims. "
            "EC3 has shared typologies with FS-ISAC EU and national financial intelligence units. "
            "AMLA cooperation framework being invoked for asset recovery across borders."
        ),
        "tags": ["Europol EC3", "Crypto Fraud", "Operation BIOS", "AI Deepfake", "EU"],
        "severity": "RED",
        "url": "https://www.europol.europa.eu/media-press/newsroom/news/",
    },
    {
        "date": "2026-07",
        "regulator": "ANSSI",
        "country": "France",
        "type": "Threat Advisory",
        "headline": "ANSSI alerte — Russian APT Sandworm targeting French financial sector since Q2 2026",
        "detail": (
            "France's ANSSI (Agence nationale de la sécurité des systèmes d'information) published "
            "an advisory identifying Sandworm (Russian GRU Unit 74455) activity targeting French "
            "financial sector infrastructure since Q2 2026, coinciding with geopolitical tensions. "
            "Techniques: destructive NotPetya-variant malware pre-positioning; targeting network "
            "monitoring systems to blind defenders before destructive payload delivery. "
            "ANSSI urges French financial institutions to implement network segmentation, "
            "review OT/IT boundary controls, and test incident response playbooks for destructive "
            "cyber scenarios within 90 days."
        ),
        "tags": ["ANSSI", "Sandworm", "GRU", "France", "Destructive Malware"],
        "severity": "AMBER",
        "url": "https://www.ssi.gouv.fr/en/publication/",
    },
    {
        "date": "2026-06",
        "regulator": "ENISA/DORA NCAs",
        "country": "EU",
        "type": "Regulatory Intelligence",
        "headline": "DORA implementation — 847 major ICT incidents reported in first 6 months, classification gaps found",
        "detail": (
            "ENISA and DORA NCAs published a mid-year assessment of DORA ICT incident reporting "
            "in the first 6 months of implementation. 847 major incidents reported across EU financial "
            "entities — below expected volumes, indicating classification gaps. NCAs identified: "
            "firms under-classifying incidents due to threshold ambiguity; inconsistent use of "
            "initial/intermediate/final reporting timelines; inadequate documentation of third-party "
            "ICT provider involvement. ESMA, EBA, and EIOPA issuing Q&A guidance to address "
            "classification inconsistencies before Q4 2026 supervisory review."
        ),
        "tags": ["DORA", "ICT Incident", "ENISA", "NCA", "Reporting"],
        "severity": "AMBER",
        "url": "https://www.eba.europa.eu/regulation-and-policy/operational-resilience/digital-operational-resilience-act-dora",
    },
]

# =============================================================================
# Combined lookup
# =============================================================================
CYBER_NEWS = {
    "uk":            UK_CYBER_NEWS,
    "north-america": NORTH_AMERICA_CYBER_NEWS,
    "latin-america": LATIN_AMERICA_CYBER_NEWS,
    "asia-pacific":  ASIA_CYBER_NEWS,
    "africa":        AFRICA_CYBER_NEWS,
    "europe":        EUROPE_CYBER_NEWS,
}

CYBER_REGION_META = {
    "uk": {
        "title": "United Kingdom — Cyber Intelligence",
        "bodies": "NCSC · FCA/CBEST · CPNI · ICO · OFCOM",
    },
    "north-america": {
        "title": "North America — Cyber Intelligence",
        "bodies": "CISA · NSA/CNMF · FBI Cyber · SEC · CCCS · CSE",
    },
    "latin-america": {
        "title": "Latin America — Cyber Intelligence",
        "bodies": "CERT.br · ANPD · UNAM-CERT · CGCYBER · GAFILAT",
    },
    "asia-pacific": {
        "title": "Asia-Pacific — Cyber Intelligence",
        "bodies": "CSA · MAS TRM · JPCERT/CC · NISC · CERT-In · ASD/ACSC · CNCERT",
    },
    "africa": {
        "title": "Africa — Cyber Intelligence",
        "bodies": "ngCERT · CSIRT-SA · KE-CIRT/CC · AFRIPOL · SSASC · ESAAMLG",
    },
    "europe": {
        "title": "Europe — Cyber Intelligence",
        "bodies": "ENISA · CERT-EU · BSI · ANSSI · NCSC-NL · CCN-CERT · Europol EC3",
    },
}
