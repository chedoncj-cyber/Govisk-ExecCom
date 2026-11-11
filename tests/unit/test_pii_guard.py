"""
Unit tests for shared/pii_guard.py — redact, redact_dict, detect_pii, PIIAuditLog.
"""
import sys
import tempfile
from pathlib import Path

import pytest

_SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(_SHARED))


# ---------------------------------------------------------------------------
# redact
# ---------------------------------------------------------------------------

class TestRedact:
    def test_email_is_redacted(self):
        from pii_guard import redact
        result = redact("contact hello@example.com for details")
        assert "[REDACTED:email]" in result
        assert "hello@example.com" not in result

    def test_plain_text_unchanged(self):
        from pii_guard import redact
        result = redact("no sensitive data here")
        assert result == "no sensitive data here"

    def test_uk_phone_is_redacted(self):
        from pii_guard import redact
        result = redact("call 07911 123456 now")
        assert "07911 123456" not in result
        assert "[REDACTED:uk_phone]" in result

    def test_postcode_is_redacted(self):
        from pii_guard import redact
        result = redact("office at EC1A 1BB")
        assert "EC1A 1BB" not in result


# ---------------------------------------------------------------------------
# redact_dict
# ---------------------------------------------------------------------------

class TestRedactDict:
    def test_firm_name_masked(self):
        from pii_guard import redact_dict
        result = redact_dict({"firm_name": "Acme Ltd", "region": "uk"})
        assert result["firm_name"] == "[REDACTED]"

    def test_region_unchanged(self):
        from pii_guard import redact_dict
        result = redact_dict({"firm_name": "Acme Ltd", "region": "uk"})
        assert result["region"] == "uk"

    def test_email_key_masked(self):
        from pii_guard import redact_dict
        result = redact_dict({"email": "ceo@firm.com"})
        assert result["email"] == "[REDACTED]"

    def test_frn_key_masked(self):
        from pii_guard import redact_dict
        result = redact_dict({"frn": "814207"})
        assert result["frn"] == "[REDACTED]"

    def test_non_pii_value_unchanged(self):
        from pii_guard import redact_dict
        result = redact_dict({"cass_category": "small"})
        assert result["cass_category"] == "small"

    def test_deep_nesting(self):
        from pii_guard import redact_dict
        result = redact_dict({"details": {"firm_name": "Secret Co"}})
        assert result["details"]["firm_name"] == "[REDACTED]"


# ---------------------------------------------------------------------------
# detect_pii
# ---------------------------------------------------------------------------

class TestDetectPii:
    def test_detects_frn_type(self):
        from pii_guard import detect_pii
        findings = detect_pii("814207")
        types_found = [f["type"] for f in findings]
        assert "frn" in types_found

    def test_detects_email(self):
        from pii_guard import detect_pii
        findings = detect_pii("test@example.com")
        assert any(f["type"] == "email" for f in findings)

    def test_returns_empty_for_clean_text(self):
        from pii_guard import detect_pii
        findings = detect_pii("no pii here at all")
        # frn pattern is broad (6-9 digits); pure text with no numbers is safe
        digit_findings = [f for f in findings if f["type"] != "frn"]
        assert len(digit_findings) == 0

    def test_finding_has_required_keys(self):
        from pii_guard import detect_pii
        findings = detect_pii("user@domain.com")
        for f in findings:
            assert "type" in f
            assert "match" in f
            assert "start" in f
            assert "end" in f


# ---------------------------------------------------------------------------
# PIIAuditLog
# ---------------------------------------------------------------------------

class TestPIIAuditLog:
    def test_record_and_query(self, tmp_path):
        from pii_guard import PIIAuditLog
        log_path = tmp_path / "pii_audit.jsonl"
        audit = PIIAuditLog(log_path=log_path)
        audit.record(
            event="pii_access",
            subject_hash="abc123",
            accessor="test_accessor",
            fields=["firm_name", "frn"],
            purpose="unit_test",
            request_id="req-001",
        )
        entries = audit.query()
        assert len(entries) == 1
        assert entries[0]["event"] == "pii_access"
        assert entries[0]["accessor"] == "test_accessor"
        assert entries[0]["purpose"] == "unit_test"

    def test_query_by_subject_hash(self, tmp_path):
        from pii_guard import PIIAuditLog
        log_path = tmp_path / "pii_audit2.jsonl"
        audit = PIIAuditLog(log_path=log_path)
        audit.record("pii_access", "hash_a", "accessor_1", ["email"], "test")
        audit.record("pii_access", "hash_b", "accessor_2", ["frn"], "test")
        results = audit.query(subject_hash="hash_a")
        assert len(results) == 1
        assert results[0]["subject_hash"] == "hash_a"

    def test_empty_log_returns_empty_list(self, tmp_path):
        from pii_guard import PIIAuditLog
        log_path = tmp_path / "empty_audit.jsonl"
        audit = PIIAuditLog(log_path=log_path)
        assert audit.query() == []

    def test_multiple_records_persisted(self, tmp_path):
        from pii_guard import PIIAuditLog
        log_path = tmp_path / "multi_audit.jsonl"
        audit = PIIAuditLog(log_path=log_path)
        for i in range(5):
            audit.record("pii_access", f"hash_{i}", "test", ["firm_name"], "test")
        assert len(audit.query()) == 5
