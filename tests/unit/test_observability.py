"""
Unit tests for shared/observability.py — get_logger, MetricsRegistry, trace_op,
prometheus_text.
"""
import logging
import sys
from pathlib import Path

import pytest

_SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(_SHARED))


# ---------------------------------------------------------------------------
# get_logger
# ---------------------------------------------------------------------------

class TestGetLogger:
    def test_returns_logger_instance(self):
        from observability import get_logger
        logger = get_logger("test.logger_a")
        assert isinstance(logger, logging.Logger)

    def test_idempotent_same_name(self):
        from observability import get_logger
        logger1 = get_logger("test.logger_idem")
        logger2 = get_logger("test.logger_idem")
        assert logger1 is logger2

    def test_logger_name_matches(self):
        from observability import get_logger
        logger = get_logger("test.named_logger")
        assert logger.name == "test.named_logger"

    def test_creates_log_file(self, tmp_path):
        from observability import get_logger
        log_file = tmp_path / "test.log"
        logger = get_logger("test.file_logger_unique", log_file=log_file)
        logger.info("hello from test")
        assert log_file.exists()
        content = log_file.read_text(encoding="utf-8")
        assert "hello from test" in content


# ---------------------------------------------------------------------------
# MetricsRegistry
# ---------------------------------------------------------------------------

class TestMetricsRegistry:
    def setup_method(self):
        """Use a fresh registry for each test to avoid cross-test pollution."""
        from observability import MetricsRegistry
        self.m = MetricsRegistry()

    def test_inc_adds_to_counter(self):
        self.m.inc("test_counter")
        snap = self.m.snapshot()
        assert "test_counter" in snap["counters"]
        assert snap["counters"]["test_counter"] == 1.0

    def test_inc_with_labels(self):
        self.m.inc("http_requests", method="GET", path="/health")
        snap = self.m.snapshot()
        assert any("http_requests" in k for k in snap["counters"])

    def test_inc_accumulates(self):
        self.m.inc("hits")
        self.m.inc("hits")
        self.m.inc("hits")
        snap = self.m.snapshot()
        assert snap["counters"]["hits"] == 3.0

    def test_reset_clears_all(self):
        self.m.inc("some_metric")
        self.m.reset()
        snap = self.m.snapshot()
        assert snap["counters"] == {}
        assert snap["gauges"] == {}

    def test_set_gauge(self):
        self.m.set_gauge("queue_depth", 42.0)
        snap = self.m.snapshot()
        assert snap["gauges"]["queue_depth"] == 42.0

    def test_observe_adds_histogram(self):
        self.m.observe("latency_ms", 100.0, op="score")
        snap = self.m.snapshot()
        assert any("latency_ms" in k for k in snap["histograms"])


# ---------------------------------------------------------------------------
# trace_op
# ---------------------------------------------------------------------------

class TestTraceOp:
    def setup_method(self):
        from observability import MetricsRegistry
        # We use the global metrics singleton for trace_op; reset it before each test
        import observability
        observability.metrics.reset()

    def test_decorated_function_returns_result(self):
        from observability import trace_op
        @trace_op("test_op_ok")
        def add(a, b):
            return a + b
        assert add(2, 3) == 5

    def test_error_increments_error_counter(self):
        import observability
        from observability import trace_op
        @trace_op("test_op_fail")
        def explode():
            raise ValueError("boom")
        with pytest.raises(ValueError):
            explode()
        snap = observability.metrics.snapshot()
        # Should have an op_total counter with status=error for this op
        error_keys = [k for k in snap["counters"] if "error" in k and "test_op_fail" in k]
        assert error_keys, f"No error counter found. Counters: {list(snap['counters'].keys())}"

    def test_success_increments_ok_counter(self):
        import observability
        from observability import trace_op
        @trace_op("test_op_success")
        def noop():
            return True
        noop()
        snap = observability.metrics.snapshot()
        ok_keys = [k for k in snap["counters"] if "ok" in k and "test_op_success" in k]
        assert ok_keys, f"No ok counter found. Counters: {list(snap['counters'].keys())}"

    def test_exception_is_reraised(self):
        from observability import trace_op
        @trace_op("reraise_test")
        def raise_runtime():
            raise RuntimeError("expected")
        with pytest.raises(RuntimeError, match="expected"):
            raise_runtime()


# ---------------------------------------------------------------------------
# prometheus_text
# ---------------------------------------------------------------------------

class TestPrometheusText:
    def setup_method(self):
        from observability import MetricsRegistry
        self.m = MetricsRegistry()

    def test_contains_type_comment(self):
        self.m.inc("prom_counter_test")
        text = self.m.prometheus_text()
        assert "# TYPE" in text

    def test_counter_appears_in_output(self):
        self.m.inc("my_counter_x", value=5)
        text = self.m.prometheus_text()
        assert "my_counter_x" in text

    def test_gauge_type_annotation(self):
        self.m.set_gauge("my_gauge_y", 99.0)
        text = self.m.prometheus_text()
        assert "# TYPE my_gauge_y gauge" in text

    def test_histogram_type_annotation(self):
        self.m.observe("my_hist", 200.0)
        text = self.m.prometheus_text()
        assert "# TYPE my_hist histogram" in text

    def test_empty_registry_returns_empty_string(self):
        text = self.m.prometheus_text()
        assert text == ""
