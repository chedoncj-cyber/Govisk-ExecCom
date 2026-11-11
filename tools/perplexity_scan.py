"""
Perplexity Web Intelligence Scanner
Queries Perplexity's sonar model (live web search) for up-to-date regulatory
information relevant to CASS, FCA, and banking security reports.

Usage (standalone):
    python tools/perplexity_scan.py --topic "CASS 7 client money updates 2026"
    python tools/perplexity_scan.py --report country_risk --region "N. America" --country "United States"

Usage (imported by other tools):
    from tools.perplexity_scan import scan_regulatory_topic, build_regulatory_context
"""

import argparse
import json
import os
from datetime import date
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent
TMP_DIR = BASE_DIR / ".tmp"
TMP_DIR.mkdir(exist_ok=True)

PERPLEXITY_BASE_URL = "https://api.perplexity.ai"
PERPLEXITY_MODEL = "sonar"  # live web search model

# ── Official regulatory handbook & source material URLs per region ─────────────
# These are fed into scan queries so Perplexity fetches content directly from
# official government / regulatory sources rather than secondary commentary.
OFFICIAL_SOURCES = {
    "UK": [
        "site:handbook.fca.org.uk",
        "site:fca.org.uk",
        "site:bankofengland.co.uk",
    ],
    "N. America": [
        "site:sec.gov",
        "site:cftc.gov",
        "site:finra.org",
        "site:federalreserve.gov",
        "site:sipc.org",
    ],
    "Latin America": [
        "site:bcb.gov.br",
        "site:bcra.gob.ar",
        "site:cnbv.gob.mx",
        "site:cmfchile.cl",
        "site:superfinanciera.gov.co",
    ],
    "Asia Pacific": [
        "site:sfc.hk",
        "site:asic.gov.au",
        "site:mas.gov.sg",
        "site:fsa.go.jp",
    ],
    "Europe": [
        "site:esma.europa.eu",
        "site:eba.europa.eu",
        "site:bafin.de",
        "site:amf-france.org",
        "site:centralbank.ie",
        "site:bankingsupervision.europa.eu",
    ],
    "Africa": [
        "site:fsca.co.za",
        "site:resbank.co.za",
        "site:sec.gov.ng",
        "site:cbn.gov.ng",
        "site:cma.or.ke",
        "site:fscmauritius.org",
    ],
}

# ── Region-specific scan topic templates ──────────────────────────────────────
REGIONAL_SCAN_TOPICS = {
    "N. America": [
        "SEC Rule 15c3-3 customer protection rule updates {year} site:sec.gov",
        "CFTC Rule 1.20 FCM segregation requirements {year} site:cftc.gov",
        "SIPC investor protection coverage updates {year} site:sipc.org",
        "FINRA broker-dealer client asset rules {year} site:finra.org",
        "US SEC enforcement broker custody violations {year}",
        "Federal Reserve capital requirements banking {year} site:federalreserve.gov",
        "US FinCEN AML Bank Secrecy Act enforcement {year}",
    ],
    "United States": [
        "SEC Rule 15c3-3 customer protection rule updates {year} site:sec.gov",
        "CFTC Rule 1.20 FCM segregation requirements {year} site:cftc.gov",
        "SIPC investor protection coverage updates {year} site:sipc.org",
        "FINRA broker-dealer enforcement actions {year} site:finra.org",
        "OFAC SDN list sanctions updates {year} site:treasury.gov",
    ],
    "Canada": [
        "OSFI capital requirements updates {year} site:osfi-bsif.gc.ca",
        "CIRO Canadian Investment Regulatory Organization dealer member rules client asset protection {year} site:ciro.ca",
        "CIRO Form 1 client asset segregation reporting requirements {year}",
        "Canada FINTRAC AML reporting requirements {year}",
    ],
    "Latin America": [
        "Banco Central do Brasil payment services regulation {year} site:bcb.gov.br",
        "Brazil Law 12865 patrimônio separado fintech update {year}",
        "BCRA Argentina client asset segregation {year} site:bcra.gob.ar",
        "CNBV Mexico Fintech Law 2018 updates {year} site:cnbv.gob.mx",
        "CMF Chile financial services regulation {year} site:cmfchile.cl",
        "SFC Colombia regulation finanzas {year} site:superfinanciera.gov.co",
        "LATAM cross-border client money regulations {year}",
    ],
    "Brazil": [
        "Banco Central do Brasil regulation {year} site:bcb.gov.br",
        "CVM Brazil securities enforcement {year} site:gov.br/cvm",
        "Brazil Law 12865 payment services updates {year}",
    ],
    "Argentina": [
        "BCRA Communiqué A 6859 PSP client asset segregation {year} site:bcra.gob.ar",
        "CNV Argentina securities regulation {year}",
    ],
    "Mexico": [
        "CNBV Mexico financial services regulation {year} site:cnbv.gob.mx",
        "Banxico Mexico fintech law payments {year} site:banxico.org.mx",
        "Mexico Ley Fintech 2018 enforcement updates {year}",
    ],
    "Chile": [
        "CMF Chile financial markets commission {year} site:cmfchile.cl",
        "Chile Law 21521 fintech financial services {year}",
    ],
    "Colombia": [
        "Superintendencia Financiera Colombia {year} site:superfinanciera.gov.co",
        "SFC Colombia client asset protection rules {year}",
    ],
    "Asia Pacific": [
        "SFC Hong Kong client money securities rules {year} site:sfc.hk",
        "ASIC client money reporting rules {year} site:asic.gov.au",
        "MAS Singapore SFA trust account safeguarding {year} site:mas.gov.sg",
        "FSA Japan FIEA customer asset separation {year} site:fsa.go.jp",
        "APAC cross-border client asset regulations {year}",
        "MAS Notice SFA 04-N18 digital token custody {year} site:mas.gov.sg",
    ],
    "Hong Kong": [
        "SFC Hong Kong client money securities rules {year} site:sfc.hk",
        "HKMA banking supervision client assets {year} site:hkma.gov.hk",
        "SFC Hong Kong enforcement actions {year} site:sfc.hk",
    ],
    "Australia": [
        "ASIC client money reporting rules {year} site:asic.gov.au",
        "APRA prudential requirements banks {year} site:apra.gov.au",
        "AUSTRAC AML CTF enforcement {year} site:austrac.gov.au",
    ],
    "Singapore": [
        "MAS SFA trust account safeguarding PSA {year} site:mas.gov.sg",
        "MAS Technology Risk Management Guidelines {year} site:mas.gov.sg",
        "MAS Notice SFA 04-N18 custody guidance {year} site:mas.gov.sg",
    ],
    "Japan": [
        "FSA Japan FIEA financial instruments exchange law {year} site:fsa.go.jp",
        "Japan FSA customer asset protection regulations {year} site:fsa.go.jp",
    ],
    "India": [
        "SEBI securities regulation client assets {year} site:sebi.gov.in",
        "RBI banking regulations digital payments {year} site:rbi.org.in",
    ],
    "Europe": [
        "ESMA MiFID II Article 16 client asset segregation enforcement {year} site:esma.europa.eu",
        "MiFID II Delegated Regulation EU 2017/593 client asset rules update {year}",
        "EBA banking authority capital requirements DORA {year} site:eba.europa.eu",
        "ECB banking supervision SSM supervisory priorities {year} site:bankingsupervision.europa.eu",
        "EU DORA Digital Operational Resilience Act implementation {year} site:esma.europa.eu",
        "PSD3 EMAR payment services safeguarding rules EU {year} site:ec.europa.eu",
        "EU AMLA Anti-Money Laundering Authority timeline {year}",
        "BaFin Germany financial enforcement actions {year} site:bafin.de",
        "AMF France financial market regulation {year} site:amf-france.org",
        "Central Bank Ireland client asset regulations enforcement {year} site:centralbank.ie",
    ],
    "Germany": [
        "BaFin Germany enforcement actions {year} site:bafin.de",
        "BaFin WpHG securities trading regulation {year} site:bafin.de",
        "Germany MiFID II client asset implementation {year}",
    ],
    "France": [
        "AMF France financial market regulation {year} site:amf-france.org",
        "ACPR France banking supervision {year}",
        "France MiFID II client money enforcement {year}",
    ],
    "Ireland": [
        "Central Bank Ireland client asset regulations {year} site:centralbank.ie",
        "CBI Ireland MiFID II enforcement {year} site:centralbank.ie",
        "Ireland client asset regulations 2015 updates {year}",
    ],
    "Luxembourg": [
        "CSSF Luxembourg fund regulation {year} site:cssf.lu",
        "Luxembourg UCITS fund manager client assets {year}",
    ],
    "Switzerland": [
        "FINMA Switzerland FinSA FinIA updates {year} site:finma.ch",
        "FINMA enforcement actions financial services {year} site:finma.ch",
    ],
    "Africa": [
        "FSCA South Africa financial sector conduct {year} site:fsca.co.za",
        "SARB South Africa Prudential Authority banking supervision {year} site:resbank.co.za",
        "South Africa COFI Bill Conduct of Financial Institutions client asset trust property {year}",
        "SEC Nigeria capital markets regulation ISA {year} site:sec.gov.ng",
        "CBN Nigeria banking sector updates {year} site:cbn.gov.ng",
        "CMA Kenya capital markets regulation {year} site:cma.or.ke",
        "FSC Mauritius VAITOS Act virtual asset digital asset regulation {year} site:fscmauritius.org",
        "Africa FATF mutual evaluation AML compliance {year} site:fatf-gafi.org",
        "ESAAMLG East Southern Africa AML CFT updates {year}",
        "GIABA West Africa AML CFT updates Nigeria Ghana Senegal {year}",
        "BCEAO WAEMU banking regulation West Africa {year} site:bceao.int",
        "BEAC CEMAC banking regulation Central Africa {year} site:beac.int",
    ],
    "South Africa": [
        "FSCA South Africa FAIS Act client asset trust property {year} site:fsca.co.za",
        "SARB Prudential Authority South Africa banking supervision {year} site:resbank.co.za",
        "South Africa Financial Markets Act client securities segregation {year}",
        "South Africa COFI Bill conduct financial institutions {year}",
        "South Africa FATF grey list status updates {year} site:fatf-gafi.org",
        "FICA Financial Intelligence Centre Act South Africa AML {year}",
    ],
    "Nigeria": [
        "SEC Nigeria investment securities act {year} site:sec.gov.ng",
        "CBN Nigeria banking regulation payment services {year} site:cbn.gov.ng",
        "Nigeria FATF AML compliance {year} site:fatf-gafi.org",
    ],
    "Kenya": [
        "CMA Kenya capital markets authority regulation {year} site:cma.or.ke",
        "CBK Kenya central bank regulation {year} site:centralbank.go.ke",
        "Kenya FATF ESAAMLG AML compliance {year}",
    ],
    "Mauritius": [
        "FSC Mauritius financial services commission {year} site:fscmauritius.org",
        "BOM Mauritius bank of mauritius regulation {year} site:bom.mu",
        "Mauritius FATF AML compliance gateway Africa {year}",
    ],
    "Egypt": [
        "EFSA Egypt financial supervisory authority {year} site:efsa.gov.eg",
        "CBE Egypt central bank regulation {year} site:cbe.org.eg",
    ],
    "Ghana": [
        "SEC Ghana securities regulation {year} site:sec.gov.gh",
        "Bank of Ghana financial supervision {year} site:bog.gov.gh",
    ],
}

# ── FATF, OFSI, global blacklist topics (cross-cutting) ───────────────────────
GLOBAL_INTELLIGENCE_TOPICS = [
    "FATF high risk jurisdictions blacklist {year} site:fatf-gafi.org",
    "FATF grey list updated countries {year} site:fatf-gafi.org",
    "OFSI UK financial sanctions list updates {year} site:gov.uk",
    "OFAC SDN list new designations {year} site:treasury.gov",
    "Basel AML index country risk scores {year}",
]

# Pre-built scan topics per report type
REPORT_SCAN_TOPICS = {
    "cass_health_check": [
        "FCA CASS 6 custody asset rule updates {year}",
        "FCA CASS 7 client money reconciliation changes {year}",
        "FCA enforcement actions CASS breaches {year}",
        "FCA CASS handbook amendments {year}",
    ],
    "cass_resolution_pack": [
        "FCA CASS 10 resolution pack requirements updates {year}",
        "FCA client asset return resolution planning {year}",
    ],
    "client_money_segregation": [
        "FCA CASS 7 client money segregation enforcement {year}",
        "FCA client money rules changes {year}",
    ],
    "cass_breach_log": [
        "FCA CASS breach notification SUP 15.3 updates {year}",
        "FCA enforcement CASS breach fines penalties {year}",
    ],
    "cass_oversight": [
        "FCA COOF CASS operational oversight function updates {year}",
        "FCA CASS 1A oversight requirements {year}",
    ],
    "threat_intelligence_banking": [
        "banking sector fraud threats UK {year}",
        "FCA financial crime enforcement banking {year}",
        "UK banking insider threat incidents {year}",
        "sanctions evasion financial services UK {year}",
    ],
    "cyber_threat_assessment": [
        "FCA CBEST cyber resilience requirements {year}",
        "FCA PS21/3 operational resilience banking {year}",
        "UK banking cyber attacks incidents {year}",
        "FCA cyber security enforcement actions {year}",
    ],
    "fca_incident_response": [
        "FCA 72 hour breach notification requirements {year}",
        "FCA operational incident reporting banking {year}",
        "FCA SUP 15 notification rules updates {year}",
    ],
    "due_diligence": [
        "FCA fit and proper assessment requirements {year}",
        "FCA third party supplier due diligence CASS {year}",
        "FCA SM&CR senior manager certification updates {year}",
    ],
    "country_risk": [
        "OFSI UK financial sanctions updates {year}",
        "OFAC sanctions list changes {year}",
        "UK cross-border client asset risk {year}",
    ],
    "executive_protection": [
        "FCA SM&CR senior manager enforcement actions {year}",
        "UK banking executive security threats {year}",
        "FCA accountability regime updates {year}",
    ],
    "physical_security_audit": [
        "FCA operational resilience physical security banking {year}",
        "FCA PS6/21 operational resilience requirements {year}",
        "UK bank branch office security incidents {year}",
    ],
}


def get_client() -> OpenAI:
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "PERPLEXITY_API_KEY not set in .env\n"
            "Get your key at: https://www.perplexity.ai/settings/api"
        )
    return OpenAI(api_key=api_key, base_url=PERPLEXITY_BASE_URL)


def _build_system_prompt(region: str = None, country: str = None) -> str:
    """Build a region-aware system prompt for the intelligence scan."""
    base = (
        "You are a global financial regulatory intelligence analyst specialising in "
        "client asset protection, AML/CFT, and banking security. "
        "Always cite official government or regulatory body sources with URLs. "
        "Format: 2-4 bullet points of key findings, then list sources. "
        "Focus on the most recent and material developments. "
        "Prioritise information from official regulatory handbook and government websites."
    )
    if region and region not in ("Other", "UK"):
        base += (
            f" This scan is specifically for the {region} region"
            + (f" — {country}" if country else "")
            + ". Focus on the regulatory framework applicable in that jurisdiction "
            "rather than UK FCA/CASS rules unless the query specifically mentions them."
        )
    else:
        base += (
            " Focus on FCA regulations, CASS rules, and UK financial services. "
            "Reference the FCA Handbook at handbook.fca.org.uk where applicable."
        )
    return base


def scan_regulatory_topic(topic: str, context: str = "", region: str = None, country: str = None) -> dict:
    """
    Query the best available provider for a single regulatory topic.
    Prefers Perplexity (live web search) but falls back to free providers.
    Returns dict with summary and citations.
    """
    year = date.today().year
    user_prompt = topic.format(year=year)
    if context:
        user_prompt += f"\n\nContext: {context}"

    system_prompt = _build_system_prompt(region, country)

    # Try Perplexity first (has live web search)
    if os.getenv("PERPLEXITY_API_KEY"):
        try:
            client = get_client()
            response = client.chat.completions.create(
                model=PERPLEXITY_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=600,
            )
            return {
                "topic": user_prompt,
                "summary": response.choices[0].message.content,
                "citations": list(getattr(response, "citations", []) or []),
                "model": PERPLEXITY_MODEL,
                "provider": "Perplexity",
                "scanned_date": date.today().isoformat(),
            }
        except Exception as e:
            print(f"Perplexity failed ({e}), falling back to free provider chain...")

    # Fallback: use multi-provider chain
    try:
        from ai_connector import scan_topic_with_fallback
        result = scan_topic_with_fallback(topic)
        return result
    except Exception as e:
        return {
            "topic": user_prompt,
            "summary": f"Intelligence scan unavailable — no AI provider configured or all failed. ({e})",
            "citations": [],
            "model": None,
            "provider": None,
            "scanned_date": date.today().isoformat(),
        }


def get_regional_topics(region: str = None, country: str = None) -> list[str]:
    """
    Return regional scan topics for the given region/country.
    Tries country-specific first, then region-level, then empty list.
    """
    topics = []
    if country and country in REGIONAL_SCAN_TOPICS:
        topics.extend(REGIONAL_SCAN_TOPICS[country])
    if region and region in REGIONAL_SCAN_TOPICS:
        # Avoid duplicates if country already matched region key exactly
        for t in REGIONAL_SCAN_TOPICS[region]:
            if t not in topics:
                topics.append(t)
    return topics


def build_regulatory_context(
    report_type: str,
    extra_topics: list[str] = None,
    region: str = None,
    country: str = None,
) -> dict:
    """
    Run all pre-built scan topics for a report type, augmented with regional
    and country-specific live-web topics when region/country are provided.

    Returns a dict of {topic: result} and saves to .tmp/<report_type>_intel.json.
    """
    topics = list(REPORT_SCAN_TOPICS.get(report_type, []))

    # Inject regional topics — queries target official regulatory websites
    regional_topics = get_regional_topics(region, country)
    for t in regional_topics:
        if t not in topics:
            topics.append(t)

    # Country risk reports get FATF/sanctions global scan
    if report_type == "country_risk":
        for t in GLOBAL_INTELLIGENCE_TOPICS:
            if t not in topics:
                topics.append(t)

    if extra_topics:
        topics = topics + extra_topics

    if not topics:
        print(f"No scan topics for report type: {report_type}")
        return {}

    region_label = f" [{country or region}]" if (country or region) else ""
    print(f"Scanning {len(topics)} regulatory topics via Perplexity{region_label}...")
    results = {}
    for i, topic in enumerate(topics, 1):
        year = date.today().year
        label = topic.format(year=year)
        print(f"  [{i}/{len(topics)}] {label}")
        try:
            results[label] = scan_regulatory_topic(topic, region=region, country=country)
        except Exception as e:
            print(f"    WARNING: scan failed — {e}")
            results[label] = {"topic": label, "summary": f"Scan failed: {e}", "citations": []}

    output_path = TMP_DIR / f"{report_type}_intel.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Intelligence saved to: {output_path}")

    return results


def format_intel_for_report(intel: dict) -> str:
    """
    Convert Perplexity scan results into a formatted string for inclusion in a report.
    """
    if not intel:
        return "No regulatory intelligence data available."

    lines = [f"Regulatory Intelligence — Scanned {date.today().strftime('%d %B %Y')}\n"]
    for topic, result in intel.items():
        lines.append(f"\n### {topic}")
        lines.append(result.get("summary", "No summary available."))
        citations = result.get("citations", [])
        if citations:
            lines.append("\nSources:")
            for c in citations:
                lines.append(f"  - {c}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Perplexity Regulatory Web Scanner")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--topic", help="Single topic to scan")
    group.add_argument("--report", help=f"Report type to scan all topics for. Options: {list(REPORT_SCAN_TOPICS.keys())}")
    args = parser.parse_args()

    if args.topic:
        print(f"Scanning: {args.topic}")
        result = scan_regulatory_topic(args.topic)
        print(f"\n{result['summary']}")
        if result["citations"]:
            print("\nSources:")
            for c in result["citations"]:
                print(f"  - {c}")
    else:
        intel = build_regulatory_context(args.report)
        print(f"\nIntelligence report:\n{format_intel_for_report(intel)}")


if __name__ == "__main__":
    main()
