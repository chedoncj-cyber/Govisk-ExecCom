"""
CASS Intelligence Reports — FastAPI Gateway
Serves the portal and handles report generation with live SSE progress.
Run: uvicorn api.gateway:app --reload --port 8080
"""

import asyncio
import json
import os
import re
import subprocess
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import AsyncGenerator

from fastapi import Body, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from dotenv import load_dotenv

_SAFE_NAME_RE = re.compile(r"[^A-Za-z0-9 _\-]")
_MAX_PAYLOAD_BYTES = 64 * 1024  # 64 KB hard limit

# ── Shared observability ───────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "shared"))
from observability import get_logger, metrics, set_request_id

_gw_log = get_logger("cass.gateway", log_file=Path(__file__).parent.parent / ".tmp" / "cass.log")

# ── Web-shell / script extension probe blocker ───────────────────────────────
_BLOCKED_EXTS = re.compile(
    r"\.(php\d*|phtml|phar|asp|aspx|ashx|asmx|jsp|jspx|cfm|cgi|pl|sh|bash"
    r"|exe|dll|bat|cmd|htaccess|htpasswd|shtml|xml\.php)\b",
    re.IGNORECASE,
)

# ── Path traversal / injection patterns ──────────────────────────────────────
_SUSPICIOUS_PATH = re.compile(
    r"(\.\.[/\\]|%2e%2e|%252e%252e|/etc/passwd|/proc/self"
    r"|cmd\.exe|powershell|base64_decode|eval\s*\(|system\s*\(|passthru\s*\("
    r"|shell_exec\s*\(|exec\s*\(|phpinfo\s*\()",
    re.IGNORECASE,
)

# ── Known scanner / exploit-framework user-agent fragments ───────────────────
_BLOCKED_UA = re.compile(
    r"(sqlmap|nikto|nmap|masscan|zgrab|nuclei|dirsearch|gobuster|ffuf|wfuzz"
    r"|acunetix|nessus|openvas|burp\s?suite|havij|hydra|metasploit"
    r"|python-requests/[01]\.|curl/[0-6]\.)",
    re.IGNORECASE,
)

# ── Simple in-memory rate limiter (per IP, per 60 s window) ─────────────────
_RATE_STORE: dict[str, list[float]] = defaultdict(list)
_RATE_WINDOW = 60   # seconds
_RATE_LIMIT  = 40   # max requests per IP per window

# ── Security headers added to every response ─────────────────────────────────
_SEC_HEADERS = {
    "X-Frame-Options":        "DENY",
    "X-Content-Type-Options": "nosniff",
    "X-XSS-Protection":       "1; mode=block",
    "Referrer-Policy":        "strict-origin-when-cross-origin",
    "Permissions-Policy":     "geolocation=(), microphone=(), camera=()",
    "Content-Security-Policy": (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src https://fonts.gstatic.com; "
        "connect-src 'self'; "
        "img-src 'self' data:; "
        "frame-ancestors 'none';"
    ),
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
}


class SecurityMiddleware(BaseHTTPMiddleware):
    """Block web-shell probes, path traversal, scanner UAs; add security headers; rate-limit."""

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        raw  = str(request.url)
        ua   = request.headers.get("user-agent", "")

        # Block PHP / web-shell extension probes
        if _BLOCKED_EXTS.search(path):
            return JSONResponse({"detail": "Forbidden"}, status_code=403)

        # Block path traversal and injection attempts in the full URL
        if _SUSPICIOUS_PATH.search(raw):
            return JSONResponse({"detail": "Forbidden"}, status_code=403)

        # Block known scanning / attack-tool user agents
        if _BLOCKED_UA.search(ua):
            return JSONResponse({"detail": "Forbidden"}, status_code=403)

        # Rate limit per client IP
        ip  = (request.client.host if request.client else "unknown")
        now = time.monotonic()
        _RATE_STORE[ip] = [t for t in _RATE_STORE[ip] if now - t < _RATE_WINDOW]
        if len(_RATE_STORE[ip]) >= _RATE_LIMIT:
            return JSONResponse({"detail": "Too Many Requests"}, status_code=429)
        _RATE_STORE[ip].append(now)

        # Assign a request ID and log the incoming request
        rid = set_request_id()
        _gw_log.info(
            "request",
            extra={
                "rid": rid,
                "method": request.method,
                "path": path,
                "ip": request.client.host if request.client else "unknown",
            },
        )
        metrics.inc("http_requests_total", method=request.method, path=path.split("?")[0])

        response = await call_next(request)
        response.headers["X-Request-Id"] = rid

        for k, v in _SEC_HEADERS.items():
            response.headers[k] = v
        return response


def _sanitise_client_name(raw: str) -> str:
    """Strip dangerous characters and normalise to a safe filesystem token."""
    cleaned = _SAFE_NAME_RE.sub("", raw).strip()
    return cleaned[:80] or "Client"

# Inject tools dir so fca_reference is importable
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

load_dotenv()

BASE_DIR = Path(__file__).parent.parent
TMP_DIR = BASE_DIR / ".tmp"
TMP_DIR.mkdir(exist_ok=True)
PORTAL_DIR = BASE_DIR / "portal"
TOOLS_DIR = BASE_DIR / "tools"

app = FastAPI(title="CASS Intelligence Reports", version="1.0.0")

# Tighten CORS — read allowed origins from env (comma-separated).
# Default: localhost dev only. Override via ALLOWED_ORIGINS in .env for prod.
_ALLOWED_ORIGINS = [
    o.strip()
    for o in os.getenv("ALLOWED_ORIGINS", "http://localhost:8080,http://localhost:3000").split(",")
    if o.strip()
]

app.add_middleware(SecurityMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=_ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.mount("/assets", StaticFiles(directory=str(PORTAL_DIR / "assets")), name="assets")

REPORT_CONFIG = {
    "cass_health_check":         {"prefix": "cass_hc",      "script": "generate_cass_health_check.py",         "label": "CASS Health Check"},
    "cass_resolution_pack":      {"prefix": "cass_rp",      "script": "generate_cass_resolution_pack.py",      "label": "CASS Resolution Pack"},
    "client_money_segregation":  {"prefix": "cms_audit",    "script": "generate_client_money_segregation.py",  "label": "Client Money Segregation Audit"},
    "cass_breach_log":           {"prefix": "cass_bl",      "script": "generate_cass_breach_log.py",           "label": "CASS Breach Log & Remediation"},
    "cass_oversight":            {"prefix": "coof",         "script": "generate_cass_oversight.py",            "label": "CASS Oversight (COOF)"},
    "threat_intelligence":       {"prefix": "threat_intel", "script": "generate_threat_intelligence_banking.py","label": "Threat Intelligence — Banking"},
    "cyber_threat_assessment":   {"prefix": "cyber_ta",     "script": "generate_cyber_threat_assessment.py",   "label": "Cyber Threat Assessment"},
    "fca_incident_response":     {"prefix": "fca_ir",       "script": "generate_fca_incident_response.py",     "label": "FCA Incident Response"},
    "due_diligence":             {"prefix": "dd",           "script": "generate_due_diligence.py",             "label": "Due Diligence"},
    "country_risk":              {"prefix": "country_risk", "script": "generate_country_risk.py",              "label": "Country Risk"},
    "executive_protection":      {"prefix": "exec_prot",    "script": "generate_executive_protection.py",      "label": "Executive Protection (SM&CR)"},
    "physical_security_audit":   {"prefix": "phys_audit",   "script": "generate_physical_security_audit.py",   "label": "Physical Security Audit"},
    "grc_report":                {"prefix": "grc",          "script": "generate_grc_report.py",                "label": "GRC Intelligence Report"},
    "blacklist_report":          {"prefix": "blacklist",    "script": "generate_blacklist_report.py",           "label": "FATF Blacklist Intelligence Report"},
}


def _serve_html(name: str) -> HTMLResponse:
    path = PORTAL_DIR / name
    if path.exists():
        return HTMLResponse(content=path.read_text(encoding="utf-8"))
    return HTMLResponse(f"<h1>{name} not found</h1>", status_code=404)


@app.get("/", response_class=HTMLResponse)
async def serve_home():
    return _serve_html("home.html")


@app.get("/portal", response_class=HTMLResponse)
async def serve_portal():
    return _serve_html("index.html")


@app.get("/about", response_class=HTMLResponse)
async def serve_about():
    return _serve_html("about.html")


@app.get("/services", response_class=HTMLResponse)
async def serve_services():
    return _serve_html("services.html")


@app.get("/case-studies", response_class=HTMLResponse)
async def serve_case_studies():
    return _serve_html("case-studies.html")


@app.get("/contact", response_class=HTMLResponse)
async def serve_contact():
    return _serve_html("contact.html")


@app.get("/request-demo", response_class=HTMLResponse)
async def serve_request_demo():
    return _serve_html("request-demo.html")


@app.get("/health")
async def health_check():
    """Liveness / readiness probe endpoint."""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


@app.get("/metrics")
async def prometheus_metrics():
    """Prometheus-compatible metrics endpoint."""
    from fastapi.responses import PlainTextResponse
    return PlainTextResponse(metrics.prometheus_text(), media_type="text/plain; version=0.0.4")


@app.get("/api/status")
async def get_status():
    try:
        from ai_connector import get_status_for_api
        ai_status = get_status_for_api()
    except Exception:
        ai_status = {
            "providers": {
                "openai":     bool(os.getenv("OPENAI_API_KEY")),
                "gemini":     bool(os.getenv("GEMINI_API_KEY")),
                "groq":       bool(os.getenv("GROQ_API_KEY")),
            },
            "fallback_chain": [],
        }
    return {
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "reports_available": len(REPORT_CONFIG),
        "ai_connectors": ai_status.get("providers", {}),
        "ai_fallback_chain": ai_status.get("fallback_chain", []),
        "web_search_available": ai_status.get("web_search_available", False),
        "uk_hosted_available": ai_status.get("uk_hosted_available", False),
        "reports_generated": len(list(TMP_DIR.glob("*_draft.docx"))),
    }


@app.get("/api/reports")
async def list_reports():
    reports = []
    for f in sorted(TMP_DIR.glob("*_draft.docx"), key=lambda x: x.stat().st_mtime, reverse=True):
        reports.append({
            "filename": f.name,
            "size_kb": round(f.stat().st_size / 1024, 1),
            "generated": datetime.fromtimestamp(f.stat().st_mtime).strftime("%d %b %Y %H:%M"),
        })
    return reports


@app.get("/api/download/{filename}")
async def download_report(filename: str):
    # Prevent path traversal: only allow safe filename characters and .docx extension
    # Use \Z (not $) to reject strings with trailing newlines
    if not re.match(r"^[\w\- ]+\.docx\Z", filename):
        raise HTTPException(status_code=400, detail="Invalid filename")
    path = TMP_DIR / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    return FileResponse(
        path=str(path),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=filename,
    )


async def generate_stream(report_type: str, client_name: str, data: dict, no_scan: bool) -> AsyncGenerator[str, None]:
    config = REPORT_CONFIG.get(report_type)
    if not config:
        yield f"data: {json.dumps({'type': 'error', 'message': f'Unknown report type: {report_type}'})}\n\n"
        return

    prefix = config["prefix"]
    script = config["script"]
    label = config["label"]
    safe_name = client_name.replace(" ", "_")

    yield f"data: {json.dumps({'type': 'progress', 'step': 1, 'message': f'Preparing {label} for {client_name}...'})}\n\n"
    await asyncio.sleep(0.3)

    # Save input JSON
    input_path = TMP_DIR / f"{prefix}_{safe_name}_input.json"
    with open(input_path, "w") as f:
        json.dump(data, f, indent=2)
    yield f"data: {json.dumps({'type': 'progress', 'step': 2, 'message': 'Client data saved.'})}\n\n"
    await asyncio.sleep(0.2)

    # Routing intelligence scan
    yield f"data: {json.dumps({'type': 'progress', 'step': 3, 'message': 'Running Routing Intelligence Scan — verifying live regulatory signals...', 'ai': 'routing'})}\n\n"
    await asyncio.sleep(0.2)

    # Run generator script
    yield f"data: {json.dumps({'type': 'progress', 'step': 4, 'message': f'Running {label} generator...'})}\n\n"

    script_path = TOOLS_DIR / script
    cmd = [sys.executable, str(script_path), "--client", safe_name]
    if no_scan:
        cmd.append("--no-scan")

    env = os.environ.copy()
    env["PYTHONPATH"] = str(TOOLS_DIR)

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(BASE_DIR),
            env=env,
        )
        stdout_bytes, stderr_bytes = await proc.communicate()
        for line in stdout_bytes.decode(errors="replace").splitlines():
            if line.strip():
                yield f"data: {json.dumps({'type': 'log', 'message': line.strip()})}\n\n"
        if proc.returncode != 0 and stderr_bytes:
            lines = stderr_bytes.decode(errors="replace").strip().splitlines()
            # Strip last line if it looks like an internal path (starts with / or drive letter)
            err_text = next(
                (l for l in reversed(lines) if l.strip() and not re.match(r"^\s*(File |/|[A-Za-z]:\\)", l)),
                "Report generation failed. Check server logs.",
            )
            yield f"data: {json.dumps({'type': 'error', 'message': err_text})}\n\n"
            return

        # Accept standard filename or timestamped fallback (when file was locked)
        output_path = TMP_DIR / f"{prefix}_{safe_name}_draft.docx"
        if not output_path.exists():
            candidates = sorted(
                TMP_DIR.glob(f"{prefix}_{safe_name}_*_draft.docx"),
                key=lambda x: x.stat().st_mtime,
                reverse=True,
            )
            if candidates:
                output_path = candidates[0]

        if output_path.exists():
            yield f"data: {json.dumps({'type': 'complete', 'message': f'{label} generated successfully!', 'filename': output_path.name})}\n\n"
        else:
            yield f"data: {json.dumps({'type': 'error', 'message': 'Report file not found after generation. Check logs.'})}\n\n"
    except Exception as e:
        yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"


@app.post("/api/generate/{report_type}")
async def generate_report(
    report_type: str,
    request: Request,
    payload: dict = Body(default_factory=dict),
):
    if report_type not in REPORT_CONFIG:
        raise HTTPException(status_code=400, detail=f"Unknown report type: {report_type}")
    content_length = int(request.headers.get("content-length", 0))
    if content_length > _MAX_PAYLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Payload too large")
    raw_name = payload.get("firm_name") or payload.get("subject_name") or payload.get("country") or "Client"
    client_name = _sanitise_client_name(str(raw_name))
    no_scan = payload.pop("_no_scan", False)
    data = payload

    return StreamingResponse(
        generate_stream(report_type, client_name, data, no_scan),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/api/fca-updates")
async def fca_updates():
    try:
        from fca_reference import FCA_NEWS, get_new_rules, CONSUMER_DUTY_CASS, SOURCED_DATE
        return {
            "sourced_date": SOURCED_DATE,
            "news": FCA_NEWS,
            "new_rules": get_new_rules("2024-01-01"),
            "consumer_duty_obligations": CONSUMER_DUTY_CASS,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/region/{slug}", response_class=HTMLResponse)
async def serve_region_page(slug: str):
    """Serve the regional MI intelligence page for any valid region slug."""
    valid = {"uk", "north-america", "latin-america", "asia-pacific", "africa", "europe"}
    if slug not in valid:
        return HTMLResponse("<h1>Unknown region</h1>", status_code=404)
    html_path = PORTAL_DIR / "region.html"
    if html_path.exists():
        return HTMLResponse(content=html_path.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>Region page not found</h1>", status_code=404)


@app.get("/api/regional-updates/{region}")
async def regional_updates(region: str):
    """Return static regulatory reference updates for a given region slug."""
    try:
        from regional_reference import REGIONAL_NEWS, REGION_META, SOURCED_DATE
        if region not in REGIONAL_NEWS:
            raise HTTPException(status_code=404, detail=f"Unknown region '{region}'. Valid: north-america, latin-america, asia-pacific, africa, europe")
        return {
            "sourced_date": SOURCED_DATE,
            "region": region,
            "meta": REGION_META[region],
            "news": REGIONAL_NEWS[region],
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/rule/{rule_ref:path}")
async def get_rule(rule_ref: str):
    try:
        from fca_reference import CASS_RULES
        rule = CASS_RULES.get(rule_ref)
        if not rule:
            raise HTTPException(status_code=404, detail=f"Rule '{rule_ref}' not found")
        return {"ref": rule_ref, **rule}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/enforcement")
async def get_all_enforcement():
    """Return all enforcement cases deduped and flattened for the portal panel."""
    try:
        from fca_reference import ENFORCEMENT_CASES
        seen = set()
        result = []
        for cases in ENFORCEMENT_CASES.values():
            for c in cases:
                key = (c["firm"], c["year"])
                if key not in seen:
                    seen.add(key)
                    result.append(c)
        result.sort(key=lambda x: x["year"], reverse=True)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/blacklist", response_class=HTMLResponse)
async def serve_blacklist():
    return _serve_html("blacklist.html")


@app.get("/grc-templates", response_class=HTMLResponse)
async def serve_grc_templates():
    return _serve_html("grc-templates.html")


@app.get("/api/fatf-blacklist")
async def get_fatf_blacklist():
    """Return cached FATF blacklist / grey list data (last run of fatf_blacklist.py)."""
    path = TMP_DIR / "fatf_blacklist.json"
    if not path.exists():
        # Generate on first request using the baseline in the tool
        try:
            import subprocess
            script_path = TOOLS_DIR / "fatf_blacklist.py"
            subprocess.run(
                [sys.executable, str(script_path)],
                cwd=str(BASE_DIR),
                timeout=30,
                capture_output=True,
            )
        except Exception:
            pass
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    raise HTTPException(
        status_code=404,
        detail="FATF blacklist data not available. Run tools/fatf_blacklist.py to initialise.",
    )


@app.post("/api/fatf-blacklist/refresh")
async def refresh_fatf_blacklist():
    """Re-run fatf_blacklist.py and stream progress via SSE."""
    script_path = TOOLS_DIR / "fatf_blacklist.py"

    async def _stream():
        yield f"data: {json.dumps({'type': 'progress', 'message': 'Fetching FATF blacklist from fatf-gafi.org…'})}\n\n"
        try:
            proc = await asyncio.create_subprocess_exec(
                sys.executable, str(script_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(BASE_DIR),
            )
            stdout_bytes, _ = await proc.communicate()
            for line in stdout_bytes.decode(errors="replace").splitlines():
                if line.strip():
                    yield f"data: {json.dumps({'type': 'log', 'message': line.strip()})}\n\n"
            if proc.returncode == 0:
                yield f"data: {json.dumps({'type': 'complete', 'message': 'FATF blacklist refreshed.'})}\n\n"
            else:
                yield f"data: {json.dumps({'type': 'error', 'message': 'FATF refresh failed.'})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(
        _stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/api/daily-briefing")
async def get_daily_briefing():
    """Return cached daily intelligence briefing (last run of daily_update.py)."""
    path = TMP_DIR / "daily_intelligence.json"
    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail="No daily briefing yet. POST /api/daily-update to generate one.",
        )
    with open(path, encoding="utf-8") as f:
        return json.load(f)


@app.post("/api/daily-update")
async def run_daily_update(request: Request):
    """Stream a live daily regulatory intelligence update via SSE."""
    no_scan = False
    try:
        body = await request.json()
        no_scan = body.get("no_scan", False)
    except Exception:
        pass

    script_path = TOOLS_DIR / "daily_update.py"
    cmd = [sys.executable, str(script_path)]
    if no_scan:
        cmd.append("--no-scan")

    env = os.environ.copy()
    env["PYTHONPATH"] = str(TOOLS_DIR)

    async def _stream():
        yield f"data: {json.dumps({'type': 'progress', 'step': 1, 'message': 'Starting daily regulatory intelligence update…'})}\n\n"
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(BASE_DIR),
                env=env,
            )
            stdout_bytes, stderr_bytes = await proc.communicate()
            for line in stdout_bytes.decode(errors="replace").splitlines():
                if line.strip():
                    yield f"data: {json.dumps({'type': 'log', 'message': line.strip()})}\n\n"
            if proc.returncode == 0:
                yield f"data: {json.dumps({'type': 'complete', 'message': 'Daily briefing updated successfully.'})}\n\n"
            else:
                lines = stderr_bytes.decode(errors="replace").strip().splitlines()
                err_text = next(
                    (l for l in reversed(lines) if l.strip() and not re.match(r"^\s*(File |/|[A-Za-z]:\\)", l)),
                    "Daily update failed. Check server logs.",
                )
                yield f"data: {json.dumps({'type': 'error', 'message': err_text})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(
        _stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/api/enforcement/region/{slug}")
async def get_enforcement_by_region(slug: str):
    """Return enforcement actions for a specific region slug."""
    from tools.regional_reference import REGIONAL_ENFORCEMENT
    data = REGIONAL_ENFORCEMENT.get(slug)
    if data is None:
        raise HTTPException(status_code=404, detail=f"No enforcement data for region '{slug}'")
    return data


@app.get("/api/enforcement/{report_type}")
async def get_enforcement_for_report(report_type: str):
    """Return enforcement cases relevant to a specific report type."""
    try:
        from fca_reference import ENFORCEMENT_CASES
        if report_type not in ENFORCEMENT_CASES:
            raise HTTPException(status_code=404, detail=f"No enforcement data for '{report_type}'")
        return ENFORCEMENT_CASES[report_type]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.gateway:app", host="0.0.0.0", port=8080, reload=True)
