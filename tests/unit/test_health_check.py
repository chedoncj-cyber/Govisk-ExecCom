"""
Unit tests for tools/generate_cass_health_check.py — score_checks().
"""
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

_TOOLS = Path(__file__).parent.parent.parent / "tools"
_SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(_TOOLS))
sys.path.insert(0, str(_SHARED))

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def uk_data():
    """Minimal UK CASS health check data dict."""
    return {
        "firm_name": "Test Bank Plc",
        "frn": "814207",
        "region": "uk",
        "cass_category": "small",
        "last_cm_reconciliation_date": "2026-10-26",
        "acknowledgement_letters_in_place": True,
        "max_single_institution_percentage": 15,
        "client_money_calculation_method": "standard",
        "custody_assets_segregated": True,
        "last_custody_reconciliation_date": "2026-10-20",
        "cass_breaches_last_12_months": False,
    }


@pytest.fixture()
def north_america_data():
    """Minimal North America data dict."""
    return {
        "firm_name": "US Broker LLC",
        "frn": "US-BR-001",
        "region": "north-america",
        "cass_category": "small",
    }


# ---------------------------------------------------------------------------
# score_checks — North America
# ---------------------------------------------------------------------------

class TestScoreChecksNorthAmerica:
    def test_returns_non_empty_list(self, north_america_data):
        from generate_cass_health_check import score_checks
        with patch("generate_cass_health_check.score_regional_health_check") as mock_fn:
            mock_fn.return_value = [
                {
                    "area": "SEC Rule 15c3-3",
                    "rule": "SEC Rule 15c3-3",
                    "description": "Customer protection rule",
                    "status": "GREEN",
                    "commentary": "Compliant.",
                }
            ]
            findings = score_checks(north_america_data)
        assert len(findings) > 0


# ---------------------------------------------------------------------------
# score_checks — UK
# ---------------------------------------------------------------------------

class TestScoreChecksUK:
    def test_returns_list(self, uk_data):
        from generate_cass_health_check import score_checks
        findings = score_checks(uk_data)
        assert isinstance(findings, list)
        assert len(findings) > 0

    def test_all_findings_have_status(self, uk_data):
        from generate_cass_health_check import score_checks
        findings = score_checks(uk_data)
        for f in findings:
            assert "status" in f, f"Finding missing 'status' key: {f}"
            assert f["status"] in ("RED", "AMBER", "GREEN"), (
                f"Invalid status '{f['status']}' in finding: {f}"
            )

    def test_all_findings_have_required_keys(self, uk_data):
        from generate_cass_health_check import score_checks
        required = {"rule", "description", "status", "commentary"}
        findings = score_checks(uk_data)
        for f in findings:
            missing = required - set(f.keys())
            assert not missing, f"Finding missing keys {missing}: {f}"

    def test_daily_recon_green_when_recent(self, uk_data):
        from generate_cass_health_check import score_checks
        findings = score_checks(uk_data)
        recon_findings = [f for f in findings if f.get("rule") == "CASS 7.13.4R"]
        assert recon_findings, "No finding for CASS 7.13.4R"
        assert recon_findings[0]["status"] == "GREEN"

    def test_daily_recon_red_when_stale(self, uk_data):
        from generate_cass_health_check import score_checks
        uk_data["last_cm_reconciliation_date"] = "2026-01-01"
        findings = score_checks(uk_data)
        recon_findings = [f for f in findings if f.get("rule") == "CASS 7.13.4R"]
        assert recon_findings
        assert recon_findings[0]["status"] == "RED"

    def test_no_recon_date_gives_red(self):
        from generate_cass_health_check import score_checks
        data = {
            "region": "uk",
            "cass_category": "small",
        }
        findings = score_checks(data)
        recon_findings = [f for f in findings if f.get("rule") == "CASS 7.13.4R"]
        assert recon_findings
        assert recon_findings[0]["status"] == "RED"

    def test_uses_uk_cass_scoring_not_regional(self, uk_data):
        """UK region should NOT delegate to score_regional_health_check."""
        from generate_cass_health_check import score_checks
        with patch("generate_cass_health_check.score_regional_health_check") as mock_fn:
            mock_fn.return_value = []
            findings = score_checks(uk_data)
            mock_fn.assert_not_called()
        assert len(findings) > 0
