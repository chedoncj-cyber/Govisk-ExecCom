"""
FATF High-Risk Jurisdictions Monitor
Fetches Black List (Call for Action) and Grey List (Increased Monitoring)
from https://www.fatf-gafi.org/ — saves to .tmp/fatf_blacklist.json

Run:  python tools/fatf_blacklist.py
Task: Windows Task Scheduler "FATF Blacklist Daily Update" at 07:30
API:  GET /api/fatf-blacklist
"""
import io
import json
import sys
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE_DIR = Path(__file__).parent.parent
TMP_DIR  = BASE_DIR / ".tmp"
TMP_DIR.mkdir(exist_ok=True)

FATF_URL = "https://www.fatf-gafi.org/en/topics/high-risk-and-other-monitored-jurisdictions.html"

# ── Baseline dataset (verified Oct 2026) ──────────────────────────────────────
# Source: FATF Plenary outcomes & Public Statements
# Black List = High-Risk Jurisdictions subject to a Call for Action
# Grey List  = Jurisdictions under Increased Monitoring

BASELINE = {
    "black_list": [
        {
            "country": "Iran",
            "region":  "Middle East & North Africa",
            "iso2":    "IR",
            "flag":    "\U0001f1ee\U0001f1f7",
            "on_list_since": "2008",
            "primary_concerns": [
                "Terrorism financing",
                "Money laundering",
                "Non-compliance with FATF Recommendations",
            ],
        },
        {
            "country": "North Korea (DPRK)",
            "region":  "Asia-Pacific",
            "iso2":    "KP",
            "flag":    "\U0001f1f0\U0001f1f5",
            "on_list_since": "2009",
            "primary_concerns": [
                "Weapons of mass destruction proliferation financing",
                "Systematic AML/CFT failures",
                "No meaningful engagement with FATF",
            ],
        },
        {
            "country": "Myanmar",
            "region":  "Asia-Pacific",
            "iso2":    "MM",
            "flag":    "\U0001f1f2\U0001f1f2",
            "on_list_since": "2022",
            "primary_concerns": [
                "Systematic ML/TF failures",
                "Drug trafficking proceeds",
                "Absence of effective AML supervision",
            ],
        },
    ],
    "grey_list": [
        # ── Africa ────────────────────────────────────────────────────────────
        {
            "country": "Algeria", "region": "Africa", "iso2": "DZ",
            "flag": "\U0001f1e9\U0001f1ff", "on_list_since": "2024",
            "primary_concerns": [
                "Strategic deficiencies in AML/CFT legal framework",
                "Inadequate supervision of financial institutions and DNFBPs",
                "Weak beneficial ownership transparency and registration",
                "Limited effectiveness of financial intelligence unit",
            ],
        },
        {
            "country": "Angola", "region": "Africa", "iso2": "AO",
            "flag": "\U0001f1e6\U0001f1f4", "on_list_since": "2023",
            "primary_concerns": [
                "Weaknesses in AML/CFT supervisory framework",
                "Inadequate financial intelligence unit capacity",
                "Deficiencies in beneficial ownership registration",
                "Insufficient prosecution of money laundering offences",
            ],
        },
        {
            "country": "Burkina Faso", "region": "Africa", "iso2": "BF",
            "flag": "\U0001f1e7\U0001f1eb", "on_list_since": "2023",
            "primary_concerns": [
                "Significant terrorism financing risk in the Sahel region",
                "Inadequate counter-terrorism financing controls",
                "Weak cross-border currency and asset controls",
                "Insufficient prosecution of TF offences",
            ],
        },
        {
            "country": "Cameroon", "region": "Africa", "iso2": "CM",
            "flag": "\U0001f1e8\U0001f1f2", "on_list_since": "2023",
            "primary_concerns": [
                "Deficiencies in AML/CFT legal and institutional framework",
                "Weak financial intelligence unit and reporting culture",
                "Inadequate prosecution and conviction of ML offences",
                "Insufficient oversight of non-profit organisations",
            ],
        },
        {
            "country": "Democratic Republic of Congo", "region": "Africa", "iso2": "CD",
            "flag": "\U0001f1e8\U0001f1e9", "on_list_since": "2022",
            "primary_concerns": [
                "High corruption risk undermining AML/CFT effectiveness",
                "Conflict-zone money laundering via natural resource extraction",
                "Weak AML/CFT supervision across financial and non-financial sectors",
                "Inadequate prosecution of financial crimes and asset recovery",
            ],
        },
        {
            "country": "Kenya", "region": "Africa", "iso2": "KE",
            "flag": "\U0001f1f0\U0001f1ea", "on_list_since": "2024",
            "primary_concerns": [
                "Deficiencies in beneficial ownership framework",
                "Inadequate AML/CFT supervision of real estate and legal sectors",
                "Weaknesses in financial intelligence unit effectiveness",
                "Insufficient confiscation of criminal proceeds",
            ],
        },
        {
            "country": "Mali", "region": "Africa", "iso2": "ML",
            "flag": "\U0001f1f2\U0001f1f1", "on_list_since": "2021",
            "primary_concerns": [
                "Active terrorism financing risk — Sahel jihadist groups",
                "Inadequate counter-terrorism financing framework",
                "Weak cross-border controls and cash smuggling",
                "Conflict-zone ML via illicit gold and mineral trade",
            ],
        },
        {
            "country": "Mozambique", "region": "Africa", "iso2": "MZ",
            "flag": "\U0001f1f2\U0001f1ff", "on_list_since": "2022",
            "primary_concerns": [
                "Deficiencies in AML/CFT legal framework and supervision",
                "Natural resource extraction ML risk (gas, gemstones)",
                "Weak financial intelligence unit and limited ML prosecutions",
                "Inadequate beneficial ownership and corporate transparency",
            ],
        },
        {
            "country": "Namibia", "region": "Africa", "iso2": "NA",
            "flag": "\U0001f1f3\U0001f1e6", "on_list_since": "2021",
            "primary_concerns": [
                "Deficiencies in AML/CFT supervisory framework",
                "Inadequate oversight of designated non-financial businesses",
                "Weaknesses in beneficial ownership identification",
                "Limited effectiveness of ML/TF investigations and prosecutions",
            ],
        },
        {
            "country": "Nigeria", "region": "Africa", "iso2": "NG",
            "flag": "\U0001f1f3\U0001f1ec", "on_list_since": "2023",
            "primary_concerns": [
                "Deficiencies in AML/CFT supervision of financial institutions",
                "Inadequate prosecution and conviction of ML offences",
                "Weaknesses in financial intelligence effectiveness",
                "High corruption risk and misappropriation of public funds",
                "Insufficient confiscation of proceeds of crime",
            ],
        },
        {
            "country": "Senegal", "region": "Africa", "iso2": "SN",
            "flag": "\U0001f1f8\U0001f1f3", "on_list_since": "2021",
            "primary_concerns": [
                "Deficiencies in AML/CFT legal and regulatory framework",
                "Inadequate financial intelligence unit capacity",
                "Weak oversight of non-profit organisations and charities",
                "Insufficient ML/TF investigations and asset recovery",
            ],
        },
        {
            "country": "South Africa", "region": "Africa", "iso2": "ZA",
            "flag": "\U0001f1ff\U0001f1e6", "on_list_since": "2023",
            "primary_concerns": [
                "Deficiencies in AML/CFT supervision of real estate and legal professions",
                "Weaknesses in beneficial ownership transparency (state capture legacy)",
                "Inadequate prosecution and conviction of complex ML offences",
                "Insufficient oversight of designated non-financial businesses and professions",
                "Limited effectiveness in identifying and freezing criminal proceeds",
            ],
        },
        {
            "country": "Tanzania", "region": "Africa", "iso2": "TZ",
            "flag": "\U0001f1f9\U0001f1ff", "on_list_since": "2022",
            "primary_concerns": [
                "Deficiencies in AML/CFT legal framework and institutional capacity",
                "Weak financial intelligence unit effectiveness",
                "Inadequate prosecution of money laundering offences",
                "Insufficient supervision of non-banking financial sector",
            ],
        },
        # ── Americas ──────────────────────────────────────────────────────────
        {
            "country": "Haiti", "region": "Americas", "iso2": "HT",
            "flag": "\U0001f1ed\U0001f1f9", "on_list_since": "2020",
            "primary_concerns": [
                "Political instability and state fragility undermining AML framework",
                "Weak financial intelligence unit and reporting culture",
                "High corruption risk and inadequate confiscation of criminal proceeds",
                "Inadequate CFT controls amid gang-related financial crime",
            ],
        },
        {
            "country": "Jamaica", "region": "Americas", "iso2": "JM",
            "flag": "\U0001f1ef\U0001f1f2", "on_list_since": "2020",
            "primary_concerns": [
                "Deficiencies in AML/CFT supervisory framework",
                "Weak oversight of money services businesses",
                "Inadequate prosecution and conviction of ML offences",
                "Insufficient beneficial ownership transparency for legal persons",
            ],
        },
        {
            "country": "Venezuela", "region": "Americas", "iso2": "VE",
            "flag": "\U0001f1fb\U0001f1ea", "on_list_since": "2020",
            "primary_concerns": [
                "Narco-trafficking proceeds laundering at scale",
                "Systematic corruption and misappropriation of state assets",
                "Sanctions evasion and use of crypto assets to bypass OFSI/OFAC",
                "Inadequate AML/CFT controls amid economic and political crisis",
                "Hyperinflation enabling informal value transfer and ML structuring",
            ],
        },
        # ── Asia-Pacific ──────────────────────────────────────────────────────
        {
            "country": "Philippines", "region": "Asia-Pacific", "iso2": "PH",
            "flag": "\U0001f1f5\U0001f1ed", "on_list_since": "2021",
            "primary_concerns": [
                "Deficiencies in AML/CFT framework for casino and gaming sector",
                "Inadequate supervision of designated non-financial businesses",
                "Weaknesses in beneficial ownership identification and verification",
                "Insufficient prosecution of TF offences linked to regional groups",
            ],
        },
        {
            "country": "Vietnam", "region": "Asia-Pacific", "iso2": "VN",
            "flag": "\U0001f1fb\U0001f1f3", "on_list_since": "2023",
            "primary_concerns": [
                "Deficiencies in AML/CFT framework for real estate sector",
                "Inadequate supervision of virtual asset service providers",
                "Weaknesses in beneficial ownership transparency",
                "Insufficient ML/TF investigations and prosecutions",
            ],
        },
        # ── Europe ────────────────────────────────────────────────────────────
        {
            "country": "Bulgaria", "region": "Europe", "iso2": "BG",
            "flag": "\U0001f1e7\U0001f1ec", "on_list_since": "2023",
            "primary_concerns": [
                "Deficiencies in AML/CFT preventive measures for financial sector",
                "Inadequate supervision of designated non-financial businesses",
                "Weaknesses in financial intelligence and inter-agency coordination",
                "Insufficient prosecution of complex ML and corruption-linked offences",
            ],
        },
        {
            "country": "Croatia", "region": "Europe", "iso2": "HR",
            "flag": "\U0001f1ed\U0001f1f7", "on_list_since": "2022",
            "primary_concerns": [
                "Deficiencies in beneficial ownership transparency for legal entities",
                "Inadequate AML/CFT supervision of non-banking sector",
                "Weaknesses in financial intelligence unit effectiveness",
                "Insufficient confiscation and asset recovery from ML offences",
            ],
        },
        {
            "country": "Monaco", "region": "Europe", "iso2": "MC",
            "flag": "\U0001f1f2\U0001f1e8", "on_list_since": "2024",
            "primary_concerns": [
                "Inadequate AML/CFT supervision of designated non-financial businesses",
                "Deficiencies in beneficial ownership transparency for trusts and foundations",
                "Weaknesses in enforcement actions for AML/CFT breaches",
                "High-risk wealth management and private banking sector vulnerabilities",
            ],
        },
        # ── Middle East & North Africa ────────────────────────────────────────
        {
            "country": "Syria", "region": "Middle East & North Africa", "iso2": "SY",
            "flag": "\U0001f1f8\U0001f1fe", "on_list_since": "2010",
            "primary_concerns": [
                "State-linked terrorism financing and weapons proliferation",
                "Active conflict enabling systematic ML via shadow economy",
                "Absence of functional AML/CFT supervisory regime",
                "Sanctions violations and circumvention of UN/OFSI/OFAC regimes",
                "Humanitarian aid diversion for terrorist financing",
            ],
        },
        {
            "country": "Yemen", "region": "Middle East & North Africa", "iso2": "YE",
            "flag": "\U0001f1fe\U0001f1ea", "on_list_since": "2010",
            "primary_concerns": [
                "Active terrorism financing — Houthi and al-Qaeda-linked groups",
                "Conflict-zone ML through hawala and informal value transfer",
                "Complete breakdown of AML/CFT supervisory infrastructure",
                "Sanctions violations and illicit arms trade finance",
                "Humanitarian aid diversion and exploitation of financial system",
            ],
        },
    ],
    "last_updated":     datetime.now().isoformat(),
    "source":           FATF_URL,
    "source_verified":  False,
    "fetch_method":     "baseline",
}


def try_live_fetch() -> dict | None:
    """Attempt to scrape current data from FATF website. Returns dict or None on failure."""
    try:
        import requests  # type: ignore
        from bs4 import BeautifulSoup  # type: ignore
    except ImportError:
        print("[SKIP] requests/beautifulsoup4 not installed — using baseline data")
        return None

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-GB,en;q=0.9",
    }

    try:
        print(f"[FATF] Fetching {FATF_URL} ...")
        resp = requests.get(FATF_URL, headers=headers, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        black_list = []
        grey_list  = []

        # FATF typically uses two sections with distinguishable headings
        # Strategy: find <h2> containing "call for action" → collect following <li> items
        for heading in soup.find_all(["h2", "h3"]):
            text = heading.get_text(strip=True).lower()
            if "call for action" in text or "high-risk" in text:
                target = black_list
            elif "increased monitoring" in text:
                target = grey_list
            else:
                continue
            # Collect <li> or <a> tags in the next sibling section
            sibling = heading.find_next_sibling()
            while sibling and sibling.name not in ("h2", "h3"):
                for li in sibling.find_all(["li", "a"]):
                    name = li.get_text(strip=True)
                    if len(name) > 3 and not name.startswith("http"):
                        target.append({"country": name, "region": "Unknown", "iso2": "", "flag": "", "on_list_since": ""})
                sibling = sibling.find_next_sibling()

        if black_list or grey_list:
            print(f"[FATF] Live fetch: {len(black_list)} blacklisted, {len(grey_list)} grey-listed")
            return {
                "black_list":     black_list if black_list else BASELINE["black_list"],
                "grey_list":      grey_list  if grey_list  else BASELINE["grey_list"],
                "last_updated":   datetime.now().isoformat(),
                "source":         FATF_URL,
                "source_verified": True,
                "fetch_method":   "live_scrape",
            }
        print("[FATF] Live parse returned no countries — falling back to baseline")
        return None

    except Exception as exc:
        print(f"[FATF] Live fetch error: {exc}")
        return None


def build_summary(data: dict) -> dict:
    """Add per-region counts and totals to the dataset."""
    regions: dict[str, dict] = {}
    for item in data["black_list"]:
        r = item.get("region", "Other")
        regions.setdefault(r, {"black": 0, "grey": 0})
        regions[r]["black"] += 1
    for item in data["grey_list"]:
        r = item.get("region", "Other")
        regions.setdefault(r, {"black": 0, "grey": 0})
        regions[r]["grey"] += 1
    data["summary"] = {
        "total_black": len(data["black_list"]),
        "total_grey":  len(data["grey_list"]),
        "total":       len(data["black_list"]) + len(data["grey_list"]),
        "by_region":   regions,
    }
    return data


def main():
    live = try_live_fetch()
    data = live if live else {**BASELINE, "fetch_method": "baseline"}
    data = build_summary(data)

    out_path = TMP_DIR / "fatf_blacklist.json"
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)

    method = data.get("fetch_method", "?")
    print(f"[OK] FATF Blacklist saved ({method}): "
          f"{data['summary']['total_black']} blacklisted, "
          f"{data['summary']['total_grey']} grey-listed → {out_path}")


if __name__ == "__main__":
    main()
