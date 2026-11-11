"""
CASS Intelligence Reports — Multi-Provider AI Connector
Implements a fallback chain across free-tier LLM providers so regulatory
intelligence scanning works even without paid API keys.

Priority order (fastest / best quality first):
  1. Perplexity  — live web search, best for regulatory intelligence
  2. OpenRouter  — free model router (29+ models, 20 RPM / 50 RPD)
  3. Cerebras    — fastest inference, 14,400 RPD free
  4. Groq        — 1,000 RPD free, great quality
  5. Mistral     — EU-hosted (France), 1B tok/month free
  6. LLM7.io     — UK-hosted, ideal for FCA/UK compliance work
  7. GitHub      — 50-150 RPD via GitHub PAT
  8. Cohere      — Command-A, 1K req/month free
  9. Gemini      — 1,500 RPD flash (not available in UK/EU free tier)
"""

import os
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

# Pre-import httpx at module level so threads never hit a partially-initialised
# module (Python 3.14 import-system race when multiple threads call httpx simultaneously)
import httpx  # noqa: F401

from openai import OpenAI, RateLimitError, AuthenticationError
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Provider:
    name: str
    env_var: str
    base_url: str
    model: str
    region: str = "US"
    supports_web_search: bool = False
    rpm: int = 0
    rpd: int = 0
    notes: str = ""


PROVIDERS: list[Provider] = [
    Provider(
        name="Perplexity",
        env_var="PERPLEXITY_API_KEY",
        base_url="https://api.perplexity.ai",
        model="perplexity/sonar",
        region="US",
        supports_web_search=True,
        rpm=20,
        notes="Live web search — best for regulatory intelligence",
    ),
    Provider(
        name="OpenRouter",
        env_var="OPENROUTER_API_KEY",
        base_url="https://openrouter.ai/api/v1",
        model="openrouter/auto",
        region="US",
        rpm=20,
        rpd=50,
        notes="Free model auto-router — 29+ models",
    ),
    Provider(
        name="Cerebras",
        env_var="CEREBRAS_API_KEY",
        base_url="https://api.cerebras.ai/v1",
        model="llama-3.3-70b",
        region="US",
        rpm=30,
        rpd=14400,
        notes="Highest free RPD — purpose-built inference chips",
    ),
    Provider(
        name="Groq",
        env_var="GROQ_API_KEY",
        base_url="https://api.groq.com/openai/v1",
        model="llama-3.3-70b-versatile",
        region="US",
        rpm=30,
        rpd=1000,
        notes="Fast inference, good quality",
    ),
    Provider(
        name="Mistral",
        env_var="MISTRAL_API_KEY",
        base_url="https://api.mistral.ai/v1",
        model="mistral-small-latest",
        region="EU",
        rpm=60,
        notes="EU-hosted (France) — 1B tokens/month free",
    ),
    Provider(
        name="LLM7",
        env_var="LLM7_API_KEY",
        base_url="https://api.llm7.io/v1",
        model="deepseek-v4-pro",
        region="UK",
        rpm=30,
        notes="UK-hosted — DeepSeek V4 Pro",
    ),
    Provider(
        name="GitHub",
        env_var="GITHUB_TOKEN",
        base_url="https://models.inference.ai.azure.com",
        model="gpt-4o",
        region="US",
        rpm=15,
        rpd=150,
        notes="GitHub Models via PAT — no extra signup required",
    ),
    Provider(
        name="Cohere",
        env_var="COHERE_API_KEY",
        base_url="https://api.cohere.com/compatibility/v1",
        model="command-a-03-2025",
        region="US",
        rpm=20,
        notes="1,000 req/month free — Command-A",
    ),
    Provider(
        name="Gemini",
        env_var="GEMINI_API_KEY",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        model="gemini-2.0-flash",
        region="US",
        rpm=15,
        rpd=1500,
        notes="Not available on UK/EU free tier",
    ),
    Provider(
        name="Anthropic",
        env_var="ANTHROPIC_API_KEY",
        base_url="https://api.anthropic.com/v1/",
        model="claude-haiku-4-5-20251001",
        region="US",
        rpm=50,
        notes="Claude Haiku 4.5 via Anthropic OpenAI-compatible endpoint",
    ),
    Provider(
        name="DeepSeek",
        env_var="DEEPSEEK_API_KEY",
        base_url="https://api.deepseek.com/v1",
        model="deepseek-chat",
        region="CN",
        rpm=60,
        notes="DeepSeek V3 — strong reasoning, OpenAI-compatible",
    ),
]


# ── Provider order presets ────────────────────────────────────────────────────
UK_PREFERRED_ORDER = ["LLM7", "Mistral", "Perplexity", "Groq", "Cerebras",
                      "OpenRouter", "GitHub", "Cohere", "Gemini", "Anthropic", "DeepSeek"]

# Groq/Cerebras first — fastest free inference for high-volume scanning
SPEED_ORDER = ["Groq", "Cerebras", "LLM7", "Mistral", "OpenRouter",
               "Perplexity", "GitHub", "Cohere", "Gemini", "Anthropic", "DeepSeek"]

# GPT-4o / Claude / DeepSeek / Mistral Large first — best reasoning for complex analysis
QUALITY_ORDER = ["GitHub", "Anthropic", "DeepSeek", "Mistral", "LLM7", "OpenRouter",
                 "Perplexity", "Groq", "Cerebras", "Cohere", "Gemini"]


def get_configured_providers(preferred_order: list[str] | None = None) -> list[Provider]:
    """Return providers for which an API key is set, in preferred order."""
    order = preferred_order or [p.name for p in PROVIDERS]
    provider_map = {p.name: p for p in PROVIDERS}
    result = []
    for name in order:
        p = provider_map.get(name)
        if p and os.getenv(p.env_var):
            result.append(p)
    return result


def get_provider_status() -> dict[str, bool]:
    """Return {provider_name: is_configured} for all providers."""
    return {p.name: bool(os.getenv(p.env_var)) for p in PROVIDERS}


def _make_client(provider: Provider) -> OpenAI:
    kwargs: dict = {
        "api_key": os.environ[provider.env_var],
        "base_url": provider.base_url,
    }
    if provider.name == "OpenRouter":
        kwargs["default_headers"] = {
            "HTTP-Referer": "https://cass-intelligence.co.uk",
            "X-Title": "CASS Intelligence Reports",
        }
    elif provider.name == "Anthropic":
        kwargs["default_headers"] = {"anthropic-version": "2023-06-01"}
    return OpenAI(**kwargs)


def _call_perplexity(messages: list[dict], system_prompt: str, max_tokens: int) -> dict:
    """
    Call Perplexity Agent API at /v1/responses (migrated from /chat/completions).
    Extracts output_text and search result citations from the response.
    """
    import httpx

    api_key = os.environ.get("PERPLEXITY_API_KEY", "")

    # Combine system prompt + messages into a single input string
    parts = []
    if system_prompt:
        parts.append(system_prompt)
    for m in messages:
        role = m.get("role", "user").upper()
        content = m.get("content", "")
        if content:
            parts.append(f"{role}: {content}" if role != "USER" else content)
    input_text = "\n\n".join(parts)

    payload = {"model": "perplexity/sonar", "input": input_text}

    with httpx.Client(timeout=90) as client:
        resp = client.post(
            "https://api.perplexity.ai/v1/responses",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        resp.raise_for_status()
        data = resp.json()

    # Extract text and URL annotations from Agent API response structure
    text = ""
    citations: list[str] = []
    for item in data.get("output", []):
        if item.get("type") == "message":
            for part in item.get("content", []):
                if part.get("type") == "output_text":
                    text += part.get("text", "")
                    for ann in part.get("annotations", []):
                        url = ann.get("url") or ann.get("link", "")
                        if url and url not in citations:
                            citations.append(url)

    if not text:
        text = data.get("text") or data.get("answer") or ""

    return {
        "content": text,
        "provider": "Perplexity",
        "model": "perplexity/sonar",
        "citations": citations,
        "error": None,
    }


def chat_regulatory(
    messages: list[dict],
    system_prompt: str = "",
    max_tokens: int = 700,
    prefer_web_search: bool = False,
    uk_preferred: bool = True,
    provider_hint: str | None = None,
) -> dict:
    """
    Send a regulatory chat query with automatic provider fallback.

    Returns:
        {
          "content": str,
          "provider": str,
          "model": str,
          "citations": list[str],   # Perplexity returns live web citations
          "error": str | None,
        }
    """
    order = UK_PREFERRED_ORDER if uk_preferred else [p.name for p in PROVIDERS]

    if prefer_web_search:
        order = ["Perplexity"] + [n for n in order if n != "Perplexity"]

    # provider_hint moves a specific provider to the front of the chain
    if provider_hint:
        order = [provider_hint] + [n for n in order if n != provider_hint]

    configured = get_configured_providers(order)

    if not configured:
        return {
            "content": (
                "No AI provider configured. Add at least one API key to .env:\n"
                "PERPLEXITY_API_KEY, GROQ_API_KEY, CEREBRAS_API_KEY, MISTRAL_API_KEY, "
                "LLM7_API_KEY, OPENROUTER_API_KEY, GITHUB_TOKEN, COHERE_API_KEY, GEMINI_API_KEY"
            ),
            "provider": None,
            "model": None,
            "citations": [],
            "error": "no_provider",
        }

    full_messages = messages
    if system_prompt:
        full_messages = [{"role": "system", "content": system_prompt}] + messages

    for provider in configured:
        try:
            # Perplexity uses its own Agent API endpoint — dedicated handler
            if provider.name == "Perplexity":
                return _call_perplexity(messages, system_prompt, max_tokens)

            client = _make_client(provider)
            response = client.chat.completions.create(
                model=provider.model,
                messages=full_messages,
                max_tokens=max_tokens,
            )
            content = response.choices[0].message.content or ""
            citations = list(getattr(response, "citations", []) or [])
            return {
                "content": content,
                "provider": provider.name,
                "model": provider.model,
                "citations": citations,
                "error": None,
            }
        except (RateLimitError, AuthenticationError) as e:
            print(f"[ai_connector] {provider.name} unavailable ({type(e).__name__}) — trying next")
            continue
        except Exception as e:
            print(f"[ai_connector] {provider.name} error: {e} — trying next")
            continue

    return {
        "content": "All configured AI providers failed or are rate-limited. Try again later.",
        "provider": None,
        "model": None,
        "citations": [],
        "error": "all_failed",
    }


def scan_topic_with_fallback(
    topic: str,
    report_type: str = "",
    provider_hint: str | None = None,
    region: str = "UK",
) -> dict:
    """
    Scan a regulatory topic using best available provider.
    region: "UK" | "Americas" | "Asia" — selects the appropriate system prompt.
    provider_hint: preferred provider name to try first.
    """
    if region == "Americas":
        system_prompt = (
            "You are a financial regulatory intelligence analyst specialising in US, Canadian, "
            "and Latin American financial regulation including SEC, FINRA, CFTC, OCC, "
            "Federal Reserve, FDIC, OSFI (Canada), CVM (Brazil), CNBV (Mexico), "
            "CMF (Chile), SFC (Colombia), BCRA (Argentina), AML/BSA compliance, "
            "FATF and GAFILAT standards, and cross-border financial regulations. "
            "Provide concise, factual regulatory guidance. "
            "Focus on compliance requirements, enforcement priorities, and regulatory frameworks. "
            "Format: 2-4 bullet points of key findings, then list sources."
        )
        uk_pref = False
    elif region == "Asia":
        system_prompt = (
            "You are a financial regulatory intelligence analyst specialising in Asia-Pacific "
            "financial regulation including MAS (Singapore), HKMA/SFC (Hong Kong), "
            "FSA (Japan), NFRA/CSRC/PBOC (China), SEBI/RBI (India), ASIC/APRA (Australia), "
            "and the Asia/Pacific Group on Money Laundering (APG). "
            "Provide concise, factual regulatory guidance. "
            "Focus on compliance requirements, enforcement priorities, and regulatory frameworks. "
            "Format: 2-4 bullet points of key findings, then list sources."
        )
        uk_pref = False
    elif region == "Africa":
        system_prompt = (
            "You are a financial regulatory intelligence analyst specialising in African "
            "financial regulation including South Africa's Twin Peaks model (PA/SARB + FSCA), "
            "Nigeria's Central Bank (CBN), Kenya's CBK and CMA, "
            "and the regional FATF-style bodies: GIABA (West Africa), ESAAMLG (East/Southern Africa), "
            "and GABAC (Central Africa). "
            "Provide concise, factual regulatory guidance. "
            "Focus on compliance requirements, supervisory priorities, and enforcement actions. "
            "Format: 2-4 bullet points of key findings, then list sources."
        )
        uk_pref = False
    else:
        system_prompt = (
            "You are a UK financial regulatory intelligence analyst specialising in FCA rules, "
            "CASS (Client Assets Sourcebook), SM&CR, and operational resilience. "
            "Provide concise, factual updates about regulatory developments. "
            "Focus on the most recent and material changes. "
            "Cite sources with URLs where available. "
            "Format: 2-4 bullet points of key findings, then list sources."
        )
        uk_pref = True

    year = date.today().year
    query = topic.format(year=year) if "{year}" in topic else topic

    result = chat_regulatory(
        messages=[{"role": "user", "content": query}],
        system_prompt=system_prompt,
        max_tokens=600,
        prefer_web_search=True,
        uk_preferred=uk_pref,
        provider_hint=provider_hint,
    )

    return {
        "topic": query,
        "summary": result["content"],
        "citations": result["citations"],
        "provider": result["provider"],
        "model": result["model"],
        "scanned_date": date.today().isoformat(),
        "error": result["error"],
    }


def get_status_for_api() -> dict:
    """Return provider status dict for the /api/status endpoint."""
    status = get_provider_status()
    configured = get_configured_providers()
    return {
        "providers": status,
        "any_ai_configured": any(status.values()),
        "web_search_available": bool(os.getenv("PERPLEXITY_API_KEY")),
        "uk_hosted_available": bool(os.getenv("LLM7_API_KEY")),
        "fallback_chain": [p.name for p in configured],
    }
