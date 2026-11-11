"""
Unit tests for tools/report_base.py — rag_counts, reg_id_label, redact_dict,
and start_document.
"""
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Ensure tools/ and shared/ are on the path (also done in conftest.py)
_TOOLS = Path(__file__).parent.parent.parent / "tools"
_SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(_TOOLS))
sys.path.insert(0, str(_SHARED))


# ---------------------------------------------------------------------------
# rag_counts
# ---------------------------------------------------------------------------

class TestRagCounts:
    def test_empty_findings(self):
        from report_base import rag_counts
        result = rag_counts([])
        assert result == {"RED": 0, "AMBER": 0, "GREEN": 0}

    def test_all_green(self):
        from report_base import rag_counts
        findings = [{"status": "GREEN"}, {"status": "GREEN"}]
        result = rag_counts(findings)
        assert result["GREEN"] == 2
        assert result["RED"] == 0
        assert result["AMBER"] == 0

    def test_mixed_statuses(self):
        from report_base import rag_counts
        findings = [
            {"status": "RED"},
            {"status": "AMBER"},
            {"status": "GREEN"},
            {"status": "RED"},
        ]
        result = rag_counts(findings)
        assert result["RED"] == 2
        assert result["AMBER"] == 1
        assert result["GREEN"] == 1

    def test_only_red(self):
        from report_base import rag_counts
        findings = [{"status": "RED"}, {"status": "RED"}, {"status": "RED"}]
        result = rag_counts(findings)
        assert result["RED"] == 3
        assert result["GREEN"] == 0
        assert result["AMBER"] == 0


# ---------------------------------------------------------------------------
# reg_id_label
# ---------------------------------------------------------------------------

class TestRegIdLabel:
    def test_uk_slug_returns_fca_frn(self):
        from report_base import reg_id_label
        assert reg_id_label({"region": "uk"}) == "FCA FRN"

    def test_uk_case_insensitive(self):
        from report_base import reg_id_label
        assert reg_id_label({"region": "UK"}) == "FCA FRN"

    def test_north_america_returns_bodie_ref(self):
        from report_base import reg_id_label
        assert reg_id_label({"region": "north-america"}) == "Bodie Ref:"

    def test_latin_america_returns_bodie_ref(self):
        from report_base import reg_id_label
        assert reg_id_label({"region": "latin-america"}) == "Bodie Ref:"

    def test_asia_pacific_returns_bodie_ref(self):
        from report_base import reg_id_label
        assert reg_id_label({"region": "asia-pacific"}) == "Bodie Ref:"

    def test_europe_returns_bodie_ref(self):
        from report_base import reg_id_label
        assert reg_id_label({"region": "europe"}) == "Bodie Ref:"

    def test_africa_returns_bodie_ref(self):
        from report_base import reg_id_label
        assert reg_id_label({"region": "africa"}) == "Bodie Ref:"

    def test_unknown_region_defaults_to_fca_frn(self):
        from report_base import reg_id_label
        assert reg_id_label({"region": "unknown-region"}) == "FCA FRN"

    def test_empty_region_defaults_to_fca_frn(self):
        from report_base import reg_id_label
        assert reg_id_label({}) == "FCA FRN"


# ---------------------------------------------------------------------------
# redact_dict (from pii_guard — imported via report_base)
# ---------------------------------------------------------------------------

class TestRedactDict:
    def test_firm_name_is_masked(self):
        from pii_guard import redact_dict
        result = redact_dict({"firm_name": "Acme Financial Ltd", "region": "uk"})
        assert result["firm_name"] == "[REDACTED]"

    def test_non_pii_field_unchanged(self):
        from pii_guard import redact_dict
        result = redact_dict({"firm_name": "Acme Ltd", "region": "uk"})
        assert result["region"] == "uk"

    def test_email_field_is_masked(self):
        from pii_guard import redact_dict
        result = redact_dict({"email": "ceo@acme.com", "status": "active"})
        assert result["email"] == "[REDACTED]"

    def test_frn_field_is_masked(self):
        from pii_guard import redact_dict
        result = redact_dict({"frn": "814207", "region": "uk"})
        assert result["frn"] == "[REDACTED]"

    def test_non_pii_string_value_unchanged_when_no_pii_content(self):
        from pii_guard import redact_dict
        result = redact_dict({"cass_category": "small"})
        assert result["cass_category"] == "small"

    def test_deep_nested_dict(self):
        from pii_guard import redact_dict
        data = {"metadata": {"firm_name": "Secret Corp", "score": 42}}
        result = redact_dict(data)
        assert result["metadata"]["firm_name"] == "[REDACTED]"
        assert result["metadata"]["score"] == 42


# ---------------------------------------------------------------------------
# start_document
# ---------------------------------------------------------------------------

class TestStartDocument:
    def test_returns_document_object(self):
        from docx import Document
        from report_base import start_document
        data = {"firm_name": "Test Firm", "frn": "123456", "region": "uk"}
        doc = start_document("Test Report Title", data, "test_client")
        assert isinstance(doc, Document)

    def test_document_has_title_paragraph(self):
        from report_base import start_document
        data = {"firm_name": "Test Firm", "frn": "123456", "region": "uk"}
        doc = start_document("My Report Title", data, "test_client")
        # The heading (level=0) is the first paragraph
        headings = [p.text for p in doc.paragraphs if p.text]
        assert any("My Report Title" in h for h in headings)

    def test_document_contains_firm_name(self):
        from report_base import start_document
        data = {"firm_name": "Acme Bank", "frn": "999888", "region": "uk"}
        doc = start_document("CASS Health Check", data, "acme_bank")
        text = "\n".join(p.text for p in doc.paragraphs)
        assert "Acme Bank" in text

    def test_document_contains_confidential_notice(self):
        from report_base import start_document
        data = {"firm_name": "Acme Bank", "frn": "999888", "region": "uk"}
        doc = start_document("CASS Health Check", data, "acme_bank")
        text = "\n".join(p.text for p in doc.paragraphs)
        assert "CONFIDENTIAL" in text
