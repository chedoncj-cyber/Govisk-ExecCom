"""
Integration tests for end-to-end report generation.
These tests call score_checks() and build_report() with real data but mock any
external API calls (Anthropic, Perplexity).
"""
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

_TOOLS = Path(__file__).parent.parent.parent / "tools"
_SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(_TOOLS))
sys.path.insert(0, str(_SHARED))

pytestmark = pytest.mark.integration

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def uk_client_data():
    """Minimal but complete data dict for a UK small CASS firm."""
    return {
        "firm_name": "Integration Test Bank Ltd",
        "frn": "814207",
        "region": "uk",
        "cass_category": "small",
        "last_cm_reconciliation_date": "2026-10-26",
        "acknowledgement_letters_in_place": True,
        "max_single_institution_percentage": 15,
        "client_money_calculation_method": "standard",
        "custody_assets_segregated": True,
        "last_custody_reconciliation_date": "2026-10-20",
        "has_retail_clients": True,
        "retail_interest_paid": True,
        "cass_breaches_last_12_months": False,
        "is_payment_or_emoney_firm": False,
        "assessment_period": "Last 12 months",
    }


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestHealthCheckReportGeneration:
    def test_score_checks_returns_findings(self, uk_client_data):
        from generate_cass_health_check import score_checks
        findings = score_checks(uk_client_data)
        assert isinstance(findings, list)
        assert len(findings) > 0

    def test_findings_have_valid_statuses(self, uk_client_data):
        from generate_cass_health_check import score_checks
        findings = score_checks(uk_client_data)
        for f in findings:
            assert f["status"] in ("RED", "AMBER", "GREEN"), (
                f"Unexpected status '{f['status']}' in finding: {f}"
            )

    def test_build_report_returns_document(self, uk_client_data):
        from docx import Document
        from generate_cass_health_check import score_checks, build_report
        findings = score_checks(uk_client_data)
        doc = build_report(uk_client_data, findings, "test_client")
        assert isinstance(doc, Document)

    def test_document_has_paragraphs(self, uk_client_data):
        from generate_cass_health_check import score_checks, build_report
        findings = score_checks(uk_client_data)
        doc = build_report(uk_client_data, findings, "test_client")
        assert len(doc.paragraphs) > 0

    def test_document_can_be_saved(self, uk_client_data, tmp_path):
        from generate_cass_health_check import score_checks, build_report
        findings = score_checks(uk_client_data)
        doc = build_report(uk_client_data, findings, "test_client")
        save_path = tmp_path / "cass_hc_test_client_draft.docx"
        doc.save(str(save_path))
        assert save_path.exists()
        assert save_path.stat().st_size > 0

    def test_document_contains_firm_name(self, uk_client_data):
        from generate_cass_health_check import score_checks, build_report
        findings = score_checks(uk_client_data)
        doc = build_report(uk_client_data, findings, "test_client")
        all_text = "\n".join(p.text for p in doc.paragraphs)
        assert "Integration Test Bank Ltd" in all_text

    def test_intel_param_none_does_not_crash(self, uk_client_data):
        from docx import Document
        from generate_cass_health_check import score_checks, build_report
        findings = score_checks(uk_client_data)
        doc = build_report(uk_client_data, findings, "test_client", intel=None)
        assert isinstance(doc, Document)

    def test_save_report_helper(self, uk_client_data, tmp_path, monkeypatch):
        """Test that save_report() saves to .tmp and returns the path."""
        import report_base
        from generate_cass_health_check import score_checks, build_report
        # Redirect TMP_DIR to tmp_path for this test
        monkeypatch.setattr(report_base, "TMP_DIR", tmp_path)
        findings = score_checks(uk_client_data)
        doc = build_report(uk_client_data, findings, "test_save")
        path = report_base.save_report(doc, "cass_hc", "test_save")
        assert path.exists()
        assert path.suffix == ".docx"
