"""
CASS Intelligence Reports — Daily Regulatory Intelligence Update
Scans 29+ regulatory topics across 6 regions in parallel.
All queries target official government/regulatory handbook websites.

Regions: UK · North America · Europe · Latin America · Asia-Pacific · Africa
Writes:  .tmp/daily_intelligence.json

Run:  python tools/daily_update.py [--no-scan]
Task: Windows Task Scheduler "CASS Intelligence Daily Update" at 07:00
API:  GET /api/daily-briefing  •  POST /api/daily-update (SSE)
"""
import argparse
import io
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

# Force UTF-8 stdout so emoji/unicode lines don't crash on Windows cp1252
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE_DIR = Path(__file__).parent.parent
TMP_DIR = BASE_DIR / ".tmp"
TMP_DIR.mkdir(exist_ok=True)

sys.path.insert(0, str(Path(__file__).parent))
from dotenv import load_dotenv
load_dotenv()

# ─────────────────────────────────────────────────────────────────────────────
# TOPICS  —  7 UK  ·  3 North America  ·  3 Europe  ·  3 Latin America
#            6 Asia-Pacific  ·  4 Africa  =  26 total
# All queries target official government/regulatory handbook websites directly.
# ─────────────────────────────────────────────────────────────────────────────
TOPICS = [

    # ═════════════════════════════════════════════════════════════════════════
    # UK / FCA
    # ═════════════════════════════════════════════════════════════════════════
    {
        "id": "fca_enforcement",
        "title": "FCA Enforcement Priorities",
        "icon": "⚖",
        "category": "enforcement",
        "region": "UK",
        "preferred_providers": ["Perplexity", "LLM7", "Mistral"],
        "query": (
            "What are the FCA's current enforcement priorities for UK regulated firms? "
            "Summarise the most significant FCA Final Notices from 2023-2024, the rule breaches "
            "most commonly cited, and what compliance failures attract the largest penalties. "
            "Include 3-5 specific enforcement cases with penalty amounts and rules breached."
        ),
    },
    {
        "id": "cass_updates",
        "title": "CASS Key Rules & Requirements",
        "icon": "📋",
        "category": "rules",
        "region": "UK",
        "preferred_providers": ["LLM7", "Mistral", "Perplexity"],
        "query": (
            "Summarise the most important current FCA CASS rules that firms must comply with. "
            "Cover CASS 7 client money reconciliation requirements, CASS 6 custody safeguarding, "
            "CASS 10 resolution packs, CASS 15 payment safeguarding, and the 2025-2026 changes "
            "including retail client interest obligations and custodian selection record-keeping. "
            "List the top 5 compliance actions firms must take."
        ),
    },
    {
        "id": "smcr_cocon",
        "title": "SM&CR & COCON Obligations",
        "icon": "👤",
        "category": "regime",
        "region": "UK",
        "preferred_providers": ["LLM7", "Mistral", "Groq"],
        "query": (
            "What are the key SM&CR Senior Manager obligations for CASS firms in the UK? "
            "Explain the CASS Operational Oversight Function prescribed responsibility, "
            "COCON conduct rules that apply to CASS, non-financial misconduct expectations "
            "under COCON 1.1.7FR, and how the FCA has been enforcing SM&CR recently. "
            "Include what documents Senior Managers must maintain."
        ),
    },
    {
        "id": "op_resilience",
        "title": "Operational Resilience Requirements",
        "icon": "🛡",
        "category": "cyber",
        "region": "UK",
        "preferred_providers": ["LLM7", "Mistral", "Groq"],
        "query": (
            "What must UK financial services firms do to meet FCA operational resilience requirements? "
            "Cover PS21/3 important business service mapping, impact tolerances, self-assessment, "
            "CBEST cyber resilience testing eligibility, third-party and outsourcing risk under "
            "PS26/2, and the DORA requirements applying to UK firms. "
            "List the 5 most critical operational resilience actions."
        ),
    },
    {
        "id": "client_money_market",
        "title": "Client Money & Custody Risks",
        "icon": "£",
        "category": "cass",
        "region": "UK",
        "preferred_providers": ["LLM7", "Perplexity", "Mistral"],
        "query": (
            "What are the most common CASS client money and custody failures identified by the FCA? "
            "Describe the top reconciliation control weaknesses, the most frequent acknowledgement "
            "letter failures, concentration risk issues, and what the FCA expects firms to do about "
            "the new CASS 7.11.32R retail client interest rule and CASS 6.3.2A R custodian "
            "selection grounds recording requirement. Include a practical compliance checklist."
        ),
    },
    {
        "id": "consumer_duty",
        "title": "Consumer Duty for CASS Firms",
        "icon": "🏛",
        "category": "consumer",
        "region": "UK",
        "preferred_providers": ["Mistral", "LLM7", "Groq"],
        "query": (
            "How does FCA Consumer Duty apply to CASS firms holding client money and custody assets? "
            "Explain the four Consumer Duty outcomes, what the FCA expects in outcomes monitoring, "
            "price and value fair treatment for client money interest, the Consumer Support outcome "
            "and what it means for CASS operational processes. "
            "List 5 specific Consumer Duty obligations for investment firms."
        ),
    },
    {
        "id": "ps26_incident",
        "title": "Incident & Third-Party Reporting",
        "icon": "📡",
        "category": "incident",
        "region": "UK",
        "preferred_providers": ["Perplexity", "LLM7", "Groq"],
        "query": (
            "What are the FCA requirements for operational incident reporting and third-party risk? "
            "Explain the current FCA regime for notifying the regulator of operational incidents, "
            "what triggers a material outsourcing notification, DORA requirements for UK-connected "
            "firms, and the timeline for the PS26/2 enhanced incident reporting regime "
            "taking effect March 2027. Include what records firms must keep."
        ),
    },

    # ═════════════════════════════════════════════════════════════════════════
    # North America — USA (Fed · SEC · OCC · FDIC · CFTC) + Canada (OSFI · FINTRAC)
    # ═════════════════════════════════════════════════════════════════════════
    {
        "id": "sec_finra",
        "title": "USA — SEC, FINRA, CFTC",
        "icon": "🏛",
        "category": "north_america",
        "region": "North America",
        "preferred_providers": ["Perplexity", "Groq", "Cerebras"],
        "query": (
            "From sec.gov, finra.org, and cftc.gov: what are the latest regulatory priorities, "
            "examination findings, and enforcement actions from the SEC, FINRA, and CFTC for "
            "US broker-dealers, investment advisers, and custodians? "
            "Cover the SEC's current examination priorities, Regulation Best Interest (Reg BI) "
            "compliance deficiencies, SEC Rule 15c3-3 client asset safeguarding requirements, "
            "FINRA regulatory notices on operations and custody, CFTC derivatives compliance, "
            "and recent penalty amounts in enforcement actions."
        ),
    },
    {
        "id": "us_banking_federal",
        "title": "USA — Fed, OCC, FDIC & AML",
        "icon": "🏦",
        "category": "north_america",
        "region": "North America",
        "preferred_providers": ["Perplexity", "Groq", "Cerebras"],
        "query": (
            "From federalreserve.gov, occ.gov, fdic.gov, fincen.gov, and ofac.treas.gov: "
            "what are the latest supervisory priorities, guidance, and enforcement actions "
            "from the Federal Reserve System, OCC, FDIC, FinCEN, and OFAC? "
            "Cover Federal Reserve supervision of bank holding companies, OCC supervisory focus "
            "for national banks and federal savings associations, FDIC safety-and-soundness priorities, "
            "FinCEN beneficial ownership reporting under the Corporate Transparency Act, "
            "and OFAC SDN list updates and recent civil monetary penalties."
        ),
    },
    {
        "id": "canada_osfi",
        "title": "Canada — CIRO, OSFI, OSC/AMF & FINTRAC",
        "icon": "🍁",
        "category": "north_america",
        "region": "North America",
        "preferred_providers": ["Perplexity", "Groq", "Mistral"],
        "query": (
            "From ciro.ca, osfi-bsif.gc.ca, osc.ca, lautorite.qc.ca, and fintrac-canafe.gc.ca: "
            "what are the latest regulatory guidance and compliance requirements from CIRO, OSFI, "
            "and FINTRAC for Canadian financial institutions? "
            "CIRO (Canadian Investment Regulatory Organization — formed 2023 from IIROC and MFDA merger) "
            "governs investment dealers and mutual fund dealers: cover CIRO Dealer Member Rules on "
            "client asset segregation, trust accounts for free credit balances, Form 1 capital reporting, "
            "and CIRO enforcement actions. "
            "Cover OSFI Guideline B-10 third-party risk management, OSFI E-23 operational "
            "resilience, FINTRAC AML/ATF reporting requirements, recent FINTRAC penalties, "
            "and how CIRO client asset rules compare to UK CASS 6/7."
        ),
    },

    # ═════════════════════════════════════════════════════════════════════════
    # Europe — EU (ESMA/EBA/ECB) · Germany (BaFin) · France (AMF/ACPR)
    #          Ireland (CBI) · Luxembourg (CSSF) · Switzerland (FINMA)
    # MiFID II · EMIR · DORA · PSD2/PSD3 · EMD2
    # ═════════════════════════════════════════════════════════════════════════
    {
        "id": "esma_mifid",
        "title": "EU — ESMA, EBA & ECB Banking Supervision",
        "icon": "🇪🇺",
        "category": "europe",
        "region": "Europe",
        "preferred_providers": ["Perplexity", "Groq", "Mistral"],
        "query": (
            "From esma.europa.eu, eba.europa.eu, and bankingsupervision.europa.eu: "
            "what are the latest regulatory guidance, Q&As, and enforcement actions from ESMA, EBA, "
            "and the ECB's Single Supervisory Mechanism (SSM)? "
            "MiFID II is the EU equivalent of UK CASS for investment firms — cover: "
            "ESMA guidance on MiFID II Article 16 + Delegated Regulation (EU) 2017/593 client asset "
            "segregation requirements (EU equivalent of UK CASS 6/7), "
            "the key difference from UK CASS: EU relies on statutory segregation under civil law (no trust), "
            "less prescriptive than the UK CASS Sourcebook, "
            "EBA guidelines on outsourcing and operational resilience, "
            "ECB SSM supervisory priorities for significant institutions, "
            "EU DORA (Digital Operational Resilience Act) implementation status and upcoming deadlines, "
            "EU AML package — AMLA (Anti-Money Laundering Authority) setup timeline, "
            "and recent ESMA/EBA enforcement and fine data."
        ),
    },
    {
        "id": "eu_psd3_emar",
        "title": "EU — PSD3, EMAR & E-Money Safeguarding",
        "icon": "🇪🇺",
        "category": "europe",
        "region": "Europe",
        "preferred_providers": ["Perplexity", "Groq", "Cohere"],
        "query": (
            "From ec.europa.eu, esma.europa.eu, and eba.europa.eu: "
            "what is the current status of PSD3 (Payment Services Directive 3) and EMAR "
            "(E-Money and Payments Institutional Regulation) in the EU, and how do these replace "
            "PSD2 and the E-Money Directive for safeguarding client funds? "
            "EU payment institutions must segregate client funds in dedicated bank accounts or "
            "cover them with insurance — this is the EU equivalent of UK PSRs 2017 / CASS 15. "
            "Cover: PSD3 safeguarding rules timeline and key changes from PSD2, "
            "EMAR requirements for e-money institutions and how they compare to UK EMRs, "
            "recent NCA enforcement on payment institution safeguarding failures across the EU, "
            "and MiCA (Markets in Crypto-Assets Regulation) implementation status for crypto-asset "
            "service providers."
        ),
    },
    {
        "id": "bafin_amf_cbi",
        "title": "Europe — BaFin, AMF/ACPR, CBI, CSSF & FINMA",
        "icon": "🌍",
        "category": "europe",
        "region": "Europe",
        "preferred_providers": ["Perplexity", "Groq", "Mistral"],
        "query": (
            "From bafin.de, amf-france.org, acpr.banque-france.fr, centralbank.ie, "
            "cssf.lu, and finma.ch: "
            "what are the latest enforcement actions, supervisory priorities, and rule updates "
            "from Europe's major national financial regulators? "
            "Cover: BaFin Germany MiFID II client asset enforcement and WpHG breaches, "
            "AMF France market integrity enforcement and client money findings, "
            "ACPR France banking supervision and AML enforcement, "
            "Central Bank of Ireland (CBI) Client Asset Regulations 2015 enforcement — "
            "CBI rules most closely mirror UK CASS and are particularly relevant post-Brexit, "
            "CSSF Luxembourg fund manager and UCITS client asset requirements, "
            "FINMA Switzerland FinSA/FinIA client protection enforcement, "
            "and any EU-wide coordination on MiFID II client asset supervision."
        ),
    },

    # ═════════════════════════════════════════════════════════════════════════
    # Latin America — Brazil · Mexico · Colombia · Chile · Peru · Argentina
    # Regional body: GAFILAT
    # ═════════════════════════════════════════════════════════════════════════
    {
        "id": "brazil_cvm",
        "title": "Brazil — BCB & CVM",
        "icon": "🌎",
        "category": "latin_america",
        "region": "Latin America",
        "preferred_providers": ["Perplexity", "Groq", "Cerebras"],
        "query": (
            "From bcb.gov.br and cvm.gov.br: what are the latest regulatory updates and compliance "
            "requirements from Brazil's Banco Central do Brasil (BCB) and the Comissão de Valores "
            "Mobiliários (CVM)? "
            "Cover BCB operational resilience circulars, BCB's integration of local payment systems "
            "(PIX regulation), CVM Resolution 175 for investment funds and client asset segregation, "
            "CVM enforcement actions and penalty amounts, COAF AML reporting obligations, "
            "and key compliance requirements for international firms with Brazil operations."
        ),
    },
    {
        "id": "mexico_cnbv",
        "title": "Mexico — Banco de México & CNBV",
        "icon": "🌎",
        "category": "latin_america",
        "region": "Latin America",
        "preferred_providers": ["Perplexity", "Cerebras", "Groq"],
        "query": (
            "From banxico.org.mx and cnbv.gob.mx: what are the latest regulatory requirements "
            "and enforcement actions from Mexico's Banco de México (central bank) and the Comisión "
            "Nacional Bancaria y de Valores (CNBV)? "
            "Cover Banco de México payment system and currency regulations, CNBV securities firm "
            "licensing and client asset protection rules, CNBV AML obligations under LFPIORPI, "
            "recent CNBV enforcement actions and administrative sanctions, "
            "Mexico's Fintech Law regulatory framework, and FATF compliance status."
        ),
    },
    {
        "id": "latam_andes",
        "title": "Colombia · Chile · Peru · Argentina",
        "icon": "🌎",
        "category": "latin_america",
        "region": "Latin America",
        "preferred_providers": ["Perplexity", "Groq", "Cohere"],
        "query": (
            "From superfinanciera.gov.co, cmfchile.cl, sbs.gob.pe, and bcra.gob.ar: "
            "what are the latest regulatory updates from Colombia's Superintendencia Financiera "
            "(SFC), Chile's Comisión para el Mercado Financiero (CMF), "
            "Peru's Superintendencia de Banca Seguros y AFP (SBS), and Argentina's BCRA/CNV? "
            "The SFC in Colombia is a consolidated regulator covering banking, insurance, and securities. "
            "The SBS in Peru regulates banks, insurance providers, and private pension funds (AFP). "
            "Cover recent enforcement actions, AML compliance under GAFILAT standards, "
            "client asset protection rules, and pension fund oversight obligations."
        ),
    },

    # ═════════════════════════════════════════════════════════════════════════
    # Asia-Pacific — Singapore · Hong Kong · China · Japan · India · Australia
    # Regional body: APG (Asia/Pacific Group on Money Laundering)
    # ═════════════════════════════════════════════════════════════════════════
    {
        "id": "singapore_mas",
        "title": "Singapore — MAS",
        "icon": "🌏",
        "category": "asia",
        "region": "Asia",
        "preferred_providers": ["Perplexity", "OpenRouter", "Groq"],
        "query": (
            "From mas.gov.sg: what are the latest MAS (Monetary Authority of Singapore) regulatory "
            "guidelines, circulars, and enforcement actions? "
            "MAS is simultaneously the central bank and integrated financial regulator covering "
            "banking, insurance, and securities. "
            "Cover recent MAS circulars on technology risk management (TRM guidelines), "
            "MAS Notice SFA 04-N02 client asset segregation requirements and deficiencies found, "
            "MAS AML/CFT Notice enforcement and civil penalties, MAS outsourcing guidelines updates, "
            "Singapore's digital asset and crypto regulatory framework, "
            "and APG mutual evaluation findings for Singapore."
        ),
    },
    {
        "id": "hong_kong_hkma",
        "title": "Hong Kong — HKMA & SFC",
        "icon": "🌏",
        "category": "asia",
        "region": "Asia",
        "preferred_providers": ["Perplexity", "OpenRouter", "GitHub"],
        "query": (
            "From hkma.gov.hk and sfc.hk: what are the latest regulatory circulars, supervisory "
            "priorities, and enforcement actions from the HKMA and SFC in Hong Kong? "
            "The HKMA handles banking supervision while the SFC regulates securities markets. "
            "Cover SFC Code of Conduct client asset requirements (paragraph 9) and recent SFC "
            "disciplinary actions with penalty amounts, HKMA Supervisory Policy Manual updates "
            "on operational resilience and outsourcing (TM-G-2), AML/CFT requirements under "
            "the Anti-Money Laundering and Counter-Terrorist Financing Ordinance, "
            "Hong Kong's Virtual Asset Service Provider licensing regime, "
            "and cross-border compliance obligations for international firms."
        ),
    },
    {
        "id": "china_nfra",
        "title": "China — NFRA, CSRC & PBOC",
        "icon": "🌏",
        "category": "asia",
        "region": "Asia",
        "preferred_providers": ["Perplexity", "Cerebras", "OpenRouter"],
        "query": (
            "From nfra.gov.cn, csrc.gov.cn, and pbc.gov.cn: what are the latest regulatory "
            "requirements and enforcement actions from China's financial regulators? "
            "The NFRA (National Financial Regulatory Administration) supervises banking and insurance. "
            "The CSRC (China Securities Regulatory Commission) manages capital markets. "
            "The PBOC (People's Bank of China) handles monetary policy and payment systems. "
            "Cover NFRA/CSRC client fund and securities segregation rules, PBOC AML enforcement, "
            "China's data localisation requirements under PIPL and DSL affecting financial firms, "
            "QFII/RQFII program updates, and key compliance risks for international firms in China."
        ),
    },
    {
        "id": "japan_fsa",
        "title": "Japan — FSA",
        "icon": "🌏",
        "category": "asia",
        "region": "Asia",
        "preferred_providers": ["Perplexity", "Groq", "OpenRouter"],
        "query": (
            "From fsa.go.jp: what are the latest FSA (Financial Services Agency Japan) regulatory "
            "guidelines, inspection priorities, and enforcement actions? "
            "Japan's FSA is an integrated regulator overseeing banking, securities, and exchange. "
            "Cover FSA current inspection priorities for securities firms and investment managers, "
            "FIEA (Financial Instruments and Exchange Act) client asset segregation requirements, "
            "FSA cybersecurity guidelines and recent incident enforcement, "
            "AML requirements under the Act on Prevention of Transfer of Criminal Proceeds, "
            "Japan's crypto-asset exchange regulation, and recent FSA enforcement penalties."
        ),
    },
    {
        "id": "india_sebi",
        "title": "India — RBI & SEBI",
        "icon": "🌏",
        "category": "asia",
        "region": "Asia",
        "preferred_providers": ["Perplexity", "Groq", "Cerebras"],
        "query": (
            "From rbi.org.in and sebi.gov.in: what are the latest regulatory priorities, "
            "circulars, and enforcement actions from India's RBI and SEBI? "
            "The Reserve Bank of India (RBI) regulates banking and payment systems. "
            "The Securities and Exchange Board of India (SEBI) oversees capital markets. "
            "Cover RBI operational resilience and cybersecurity guidelines for banks, "
            "SEBI requirements for client asset segregation and custodians, "
            "RBI AML/KYC Master Directions and recent enforcement, "
            "SEBI's mutual fund and portfolio management service regulations, "
            "India's data localisation requirements, and key risks for foreign firms."
        ),
    },
    {
        "id": "australia_asic",
        "title": "Australia — ASIC & APRA",
        "icon": "🌏",
        "category": "asia",
        "region": "Asia",
        "preferred_providers": ["Perplexity", "Groq", "Mistral"],
        "query": (
            "From asic.gov.au, apra.gov.au, and austrac.gov.au: what are the latest regulatory "
            "guidance, enforcement actions, and compliance requirements from ASIC, APRA, and AUSTRAC? "
            "Cover ASIC client money requirements under Corporations Act 2001 Division 2 and recent "
            "ASIC enforcement actions, APRA Prudential Standard CPS 230 on operational resilience "
            "(effective July 2025) and common deficiencies identified, "
            "AUSTRAC AML/CTF enforcement actions and penalty amounts, "
            "how Australian client asset rules compare to UK CASS and MAS requirements, "
            "and APG mutual evaluation findings for Australia."
        ),
    },

    # ═════════════════════════════════════════════════════════════════════════
    # Africa — South Africa (Twin Peaks) · Nigeria · Kenya
    # Regional AML bodies: GIABA · ESAAMLG · GABAC
    # ═════════════════════════════════════════════════════════════════════════
    {
        "id": "south_africa_fsca",
        "title": "South Africa — PA/SARB & FSCA",
        "icon": "🌍",
        "category": "africa",
        "region": "Africa",
        "preferred_providers": ["Perplexity", "Groq", "Mistral"],
        "query": (
            "From resbank.co.za and fsca.co.za: what are the latest regulatory requirements and "
            "enforcement actions from South Africa's Twin Peaks regulatory model? "
            "The Prudential Authority (PA), under the South African Reserve Bank (SARB), ensures "
            "safety and soundness of financial institutions. "
            "The Financial Sector Conduct Authority (FSCA) focuses on market conduct and consumer protection. "
            "Cover recent PA/SARB supervisory priorities for banks and insurers, "
            "FSCA conduct standards for financial institutions and enforcement actions, "
            "South Africa's Financial Intelligence Centre (FIC) AML requirements, "
            "Twin Peaks framework implementation updates, and FATF grey-list compliance status."
        ),
    },
    {
        "id": "nigeria_cbn",
        "title": "Nigeria — CBN Monetary Policy & Banking Regulation",
        "icon": "🌍",
        "category": "africa",
        "region": "Africa",
        "preferred_providers": ["Perplexity", "Groq", "Cerebras"],
        "query": (
            "From cbn.gov.ng: what are the latest CBN (Central Bank of Nigeria) monetary policy "
            "decisions, banking supervision circulars, and regulatory enforcement actions in 2025-2026? "
            "Cover CBN Monetary Policy Committee (MPC) rate decisions and their impact on banks, "
            "CBN prudential guidelines updates for deposit money banks, "
            "CBN foreign exchange policy and recent FX regulations, "
            "CBN cybersecurity and operational resilience frameworks for banks, "
            "recent CBN fines and sanctions against non-compliant institutions, "
            "and CBN AML/CFT compliance requirements for international correspondent banks."
        ),
    },
    {
        "id": "nigeria_sec_fintech",
        "title": "Nigeria — SEC Capital Markets & Fintech Regulation",
        "icon": "🌍",
        "category": "africa",
        "region": "Africa",
        "preferred_providers": ["Perplexity", "Groq", "OpenRouter"],
        "query": (
            "From sec.gov.ng and nfiu.gov.ng: what are the latest regulatory developments from "
            "Nigeria's Securities and Exchange Commission (SEC) and the Nigeria Financial Intelligence "
            "Unit (NFIU) in 2025-2026? "
            "Cover SEC Nigeria capital market rules and client asset protection requirements, "
            "SEC digital assets and crypto regulation framework (Investments and Securities Act 2025), "
            "NFIU AML/CFT compliance requirements and suspicious transaction reporting, "
            "GIABA (FATF body for West Africa) mutual evaluation findings for Nigeria, "
            "and key compliance requirements for foreign firms operating in Nigerian capital markets."
        ),
    },
    {
        "id": "kenya_east_africa",
        "title": "Kenya · East & Southern Africa",
        "icon": "🌍",
        "category": "africa",
        "region": "Africa",
        "preferred_providers": ["Perplexity", "Groq", "OpenRouter"],
        "query": (
            "From centralbank.go.ke, cma.or.ke, esaamlg.org, and giaba.org: "
            "what are the latest regulatory requirements from Kenya's financial regulators and "
            "the East and Southern African AML regional bodies? "
            "The Central Bank of Kenya (CBK) regulates commercial banking while the Capital "
            "Markets Authority (CMA) supervises securities markets. "
            "The ESAAMLG (Eastern and Southern African Anti-Money Laundering Group) oversees "
            "AML compliance across East and Southern Africa. "
            "GIABA coordinates West African AML compliance across 16 member nations. "
            "Cover CBK supervisory priorities, CMA enforcement, ESAAMLG mutual evaluation "
            "findings, and AML compliance standards for international firms across the region."
        ),
    },
]

PLACEHOLDER = (
    "Scan skipped (--no-scan mode). Run without --no-scan and with at least one "
    "AI provider key in .env to fetch live regulatory intelligence."
)


_DEEPSEEK_ENRICH_PROMPT = """\
You are a financial regulatory compliance analyst. You have been given raw regulatory intelligence \
for the topic "{title}" ({region}). Extract and structure the key findings.

Raw intelligence:
{summary}

Respond in this EXACT JSON format (no markdown, no code fences):
{{
  "risk_level": "HIGH|MEDIUM|LOW",
  "key_actions": ["action 1", "action 2", "action 3"],
  "compliance_deadline": "e.g. Q1 2027 or Immediate or Ongoing",
  "insight": "2-3 sentence synthesised insight that adds analytical depth beyond the raw text"
}}"""


def _enrich_with_deepseek(raw: dict) -> dict:
    """Send raw Perplexity scan to DeepSeek for structured analysis enrichment."""
    import os, json as _json
    from ai_connector import chat_regulatory
    if not os.getenv("DEEPSEEK_API_KEY"):
        return raw
    summary = raw.get("summary", "")
    if not summary or raw.get("error"):
        return raw
    prompt = _DEEPSEEK_ENRICH_PROMPT.format(
        title=raw.get("title", ""),
        region=raw.get("region", ""),
        summary=summary[:2000],  # cap to avoid token waste
    )
    try:
        result = chat_regulatory(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            prefer_web_search=False,
            provider_hint="DeepSeek",
        )
        content = result.get("content", "").strip()
        # Strip markdown code fences if present
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        enriched = _json.loads(content)
        return {
            **raw,
            "risk_level":          enriched.get("risk_level", ""),
            "key_actions":         enriched.get("key_actions", []),
            "compliance_deadline": enriched.get("compliance_deadline", ""),
            "insight":             enriched.get("insight", ""),
            "enriched_by":         "DeepSeek",
        }
    except Exception as e:
        # Enrichment failure is non-fatal — return original scan unchanged
        return {**raw, "enrich_error": str(e)}


def _scan_topic(topic: dict, no_scan: bool) -> dict:
    if no_scan:
        return {
            **topic,
            "summary": PLACEHOLDER,
            "citations": [],
            "provider": None,
            "error": "no_scan",
            "scanned_at": datetime.now().isoformat(),
        }

    try:
        from ai_connector import scan_topic_with_fallback
        preferred = topic.get("preferred_providers", [])
        provider_hint = preferred[0] if preferred else None
        region = topic.get("region", "UK")
        # Collapse sub-regions to the AI connector's known region keys
        ai_region = "UK" if region == "UK" else ("Asia" if region == "Asia" else "Americas")
        # Append extended source list: news, regulatory standards, and business intelligence
        query = topic["query"] + (
            " Supplement official regulator sources with relevant content from the following:"
            " News & analysis: reuters.com, bloomberg.com, centralbanking.com."
            " Global regulatory standards: bis.org (Basel Committee / BIS), fsb.org (Financial Stability Board)."
            " CASS & asset management guidance: fscom.com, theinvestmentassociation.org."
            " Business registries & KYB/AML: opencorporates.com, worldbank.org, oecd.org."
            " Prioritise primary regulator publications first, then these sources for context and verification."
        )
        result = scan_topic_with_fallback(
            query, topic["id"],
            provider_hint=provider_hint,
            region=ai_region,
        )
        raw = {
            **topic,
            "summary": result.get("summary", ""),
            "citations": result.get("citations", []),
            "provider": result.get("provider"),
            "error": result.get("error"),
            "scanned_at": datetime.now().isoformat(),
        }
        return _enrich_with_deepseek(raw)
    except Exception as e:
        return {
            **topic,
            "summary": f"Scan failed: {e}",
            "citations": [],
            "provider": None,
            "error": str(e),
            "scanned_at": datetime.now().isoformat(),
        }


def run(no_scan: bool = False) -> dict:
    n = len(TOPICS)
    region_counts = {}
    for t in TOPICS:
        region_counts[t["region"]] = region_counts.get(t["region"], 0) + 1
    regions_str = " · ".join(f"{r}: {c}" for r, c in region_counts.items())
    print(f"[daily_update] Starting — {datetime.now().strftime('%Y-%m-%d %H:%M')} — {n} topics ({regions_str})")

    results: list = [None] * n

    # Scan all topics concurrently — preserves order via index mapping
    workers = min(n, 6)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_idx = {
            executor.submit(_scan_topic, topic, no_scan): i
            for i, topic in enumerate(TOPICS)
        }
        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            result = future.result()
            results[idx] = result
            provider_note = f" via {result['provider']}" if result.get("provider") else ""
            status = "✓" if not result.get("error") else "⚠"
            print(f"[daily_update]   {status} [{idx+1}/{n}] {result['title']}{provider_note}")

    briefing = {
        "generated_at": datetime.now().isoformat(),
        "generated_date": datetime.now().strftime("%d %b %Y"),
        "generated_time": datetime.now().strftime("%H:%M"),
        "no_scan": no_scan,
        "topics": results,
        "topics_scanned": sum(1 for r in results if r and not r.get("error")),
        "providers_used": list({r["provider"] for r in results if r and r.get("provider")}),
        "regions": list(region_counts.keys()),
    }

    out_path = TMP_DIR / "daily_intelligence.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(briefing, f, indent=2, ensure_ascii=False)

    print(f"[daily_update] Done. {briefing['topics_scanned']}/{n} topics scanned. "
          f"Providers: {', '.join(briefing['providers_used']) or 'none'}")
    print(f"[daily_update] Saved to: {out_path}")
    return briefing


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Daily regulatory intelligence update")
    parser.add_argument("--no-scan", action="store_true", help="Skip AI scanning (for testing)")
    args = parser.parse_args()
    run(no_scan=args.no_scan)
