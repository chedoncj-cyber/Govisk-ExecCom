"""Local dev server for Govisk ExecCom portal — maps clean URLs to .html files."""
import http.server, os, json, time, urllib.parse

PORTAL_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_FILE = os.path.join(PORTAL_DIR, "api", "reports.json")

ROUTES = {
    "/":                          "home.html",
    "/home":                      "home.html",
    "/portal":                    "index.html",

    # API — regulatory feeds
    "/api/fatf-blacklist":                              "api/fatf-blacklist.json",
    "/api/fatf-blacklist/refresh":                      "api/fatf-blacklist.json",
    "/api/fca-updates":                                 "api/fca-updates.json",
    "/api/regional-updates/north-america":              "api/regional-updates-north-america.json",
    "/api/regional-updates/latin-america":              "api/regional-updates-latin-america.json",
    "/api/regional-updates/asia-pacific":               "api/regional-updates-asia-pacific.json",
    "/api/regional-updates/africa":                     "api/regional-updates-africa.json",
    "/api/regional-updates/europe":                     "api/regional-updates-europe.json",
    "/api/daily-briefing":                              "api/daily-briefing.json",
    "/api/status":                                      "api/status.json",

    # API — reports list
    "/api/reports":                                     "api/reports.json",

    # API — enforcement panels
    "/api/enforcement":                                 "api/enforcement.json",
    "/api/enforcement/region/uk":                       "api/enforcement/region/uk.json",
    "/api/enforcement/region/north-america":            "api/enforcement/region/north-america.json",
    "/api/enforcement/region/latin-america":            "api/enforcement/region/latin-america.json",
    "/api/enforcement/region/asia-pacific":             "api/enforcement/region/asia-pacific.json",
    "/api/enforcement/region/africa":                   "api/enforcement/region/africa.json",
    "/api/enforcement/region/europe":                   "api/enforcement/region/europe.json",

    # Regional MI pages (all served by region.html — JS reads the slug from the URL)
    "/region/uk":                 "region.html",
    "/region/north-america":      "region.html",
    "/region/latin-america":      "region.html",
    "/region/asia-pacific":       "region.html",
    "/region/africa":             "region.html",
    "/region/europe":             "region.html",

    # Main pages
    "/about":         "about.html",
    "/services":      "services.html",
    "/case-studies":  "case-studies.html",
    "/contact":       "contact.html",
    "/request-demo":  "request-demo.html",
    "/region":        "region.html",
    "/blacklist":     "blacklist.html",
    "/grc-templates": "grc-templates.html",
    "/grc_dashboard": "grc_dashboard.html",
    "/privacy-policy":"privacy-policy.html",
    "/terms":         "terms.html",
    "/cookie-policy": "cookie-policy.html",
    "/refund-policy": "refund-policy.html",
    "/faq":           "faq.html",
    "/404":           "404.html",
}

# Report type display names
REPORT_NAMES = {
    "cass_health_check":        "CASS Health Check",
    "cass_resolution_pack":     "CASS Resolution Pack",
    "client_money_segregation": "Client Money Segregation Audit",
    "cass_breach_log":          "CASS Breach Log & Remediation",
    "cass_oversight":           "CASS Oversight (COOF)",
    "governance_control_ops":   "Governance & Control Operations",
    "policy_governance":        "Policy Governance",
    "risk_operations":          "Risk Operations",
    "incident_oversight":       "Incident Oversight",
    "identity_data_risk":       "Identity, Data & Third-Party Risk",
    "threat_intelligence":      "Threat Intelligence",
    "cyber_threat_assessment":  "Cyber Threat Assessment",
    "fca_incident_response":    "FCA Incident Response",
    "due_diligence":            "Due Diligence",
    "country_risk":             "Country Risk",
    "executive_protection":     "Executive Protection (SM&CR)",
    "physical_security_audit":  "Physical Security Audit",
    "grc_report":               "GRC Intelligence Report",
    "blacklist_report":         "FATF Blacklist Report",
}

def _sse(obj):
    return ("data: " + json.dumps(obj) + "\n\n").encode()


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=PORTAL_DIR, **kw)

    def translate_path(self, path):
        path = urllib.parse.urlparse(path).path.rstrip("/") or "/"
        if path in ROUTES:
            path = "/" + ROUTES[path]
        return super().translate_path(path)

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path.rstrip("/")

        # POST /api/generate/{report_id}
        if path.startswith("/api/generate/"):
            report_id = path[len("/api/generate/"):]
            self._handle_generate(report_id)
            return

        self.send_error(404, "Not found")

    def _handle_generate(self, report_id):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b"{}"
        try:
            data = json.loads(body)
        except Exception:
            data = {}

        firm = data.get("firm_name", data.get("subject_name", "Unknown Firm"))
        region = data.get("region_label", "Global")
        report_name = REPORT_NAMES.get(report_id, report_id.replace("_", " ").title())
        ts = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{report_id}_{ts}_draft.docx"

        # Send headers FIRST — before any file I/O that could raise
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "close")
        self.end_headers()
        self.close_connection = True

        def emit(obj):
            try:
                self.wfile.write(_sse(obj))
                self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError, OSError):
                pass

        try:
            emit({"type": "progress", "step": 1, "message": f"Initialising {report_name} for {firm}..."})
            time.sleep(0.4)
            emit({"type": "progress", "step": 2, "message": f"Pulling regulatory intelligence — {region} feeds..."})
            time.sleep(0.4)
            emit({"type": "progress", "step": 2, "message": "Scoring compliance posture against CASS 6, 7, 10 and SM&CR..."})
            time.sleep(0.4)
            emit({"type": "progress", "step": 3, "message": "Drafting executive summary and findings narrative..."})
            time.sleep(0.4)
            emit({"type": "progress", "step": 3, "message": "Applying RAG risk ratings and remediation recommendations..."})
            time.sleep(0.4)

            # Create downloads directory and write the file
            dl_dir = os.path.join(PORTAL_DIR, "api", "downloads")
            os.makedirs(dl_dir, exist_ok=True)
            report_path = os.path.join(dl_dir, filename)

            emit({"type": "progress", "step": 4, "message": "Formatting report document..."})
            time.sleep(0.3)

            content = "\n".join([
                f"GOVISK INTELLIGENCE -- {report_name.upper()}",
                "=" * 60,
                f"Firm:      {firm}",
                f"Region:    {region}",
                f"Generated: {time.strftime('%Y-%m-%d %H:%M UTC')}",
                f"Type:      {report_id}",
                "",
                "This draft was generated by the Govisk ExecCom local portal server.",
                "Full AI-generated content requires the CASS Intelligence API backend.",
            ])
            with open(report_path, "wb") as f:
                f.write(content.encode("utf-8"))

            emit({"type": "progress", "step": 4, "message": "Running final quality checks..."})
            time.sleep(0.3)
            emit({"type": "progress", "step": 5, "message": "Saving report to library..."})
            time.sleep(0.2)

            size_kb = max(1, round(os.path.getsize(report_path) / 1024, 1))

            # Update reports.json
            try:
                with open(REPORTS_FILE, "r", encoding="utf-8") as f:
                    reports = json.load(f)
                if not isinstance(reports, list):
                    reports = []
            except Exception:
                reports = []
            reports.insert(0, {
                "filename": filename,
                "generated": time.strftime("%d %b %Y %H:%M"),
                "size_kb": size_kb,
                "report_type": report_id,
                "firm": firm,
            })
            with open(REPORTS_FILE, "w", encoding="utf-8") as f:
                json.dump(reports[:50], f, indent=2)

            emit({
                "type": "complete",
                "message": f"{report_name} draft ready for {firm}",
                "filename": filename,
            })

        except Exception as e:
            emit({"type": "error", "message": f"Generation failed: {e}"})

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path.rstrip("/") or "/"

        # GET /api/download/{filename}
        if path.startswith("/api/download/"):
            filename = path[len("/api/download/"):]
            filepath = os.path.join(PORTAL_DIR, "api", "downloads", filename)
            if os.path.isfile(filepath):
                self.send_response(200)
                self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
                self.send_header("Content-Length", str(os.path.getsize(filepath)))
                self.end_headers()
                with open(filepath, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "Report not found")
            return

        super().do_GET()

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, fmt, *args):
        print(f"  {self.address_string()} {fmt % args}")


if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 8181))
    with http.server.HTTPServer(("0.0.0.0", PORT), Handler) as srv:
        print(f"Govisk ExecCom portal → http://0.0.0.0:{PORT}/")
        print(f"  /         → home.html")
        print(f"  /portal   → index.html (dashboard)")
        print(f"  /region/uk, /north-america, /latin-america, /asia-pacific, /africa, /europe")
        print(f"  POST /api/generate/{{report_id}} → streams SSE progress + writes draft .docx")
        print(f"  GET  /api/download/{{filename}}  → serves generated report files")
        print(f"  Ctrl+C to stop")
        srv.serve_forever()
