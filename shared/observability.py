"""
Shared observability — structured JSON logging, Prometheus-compatible metrics,
request tracing, and operation timing decorators.

Usage in any project:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent / "shared"))
    from observability import get_logger, metrics, trace_op, set_request_id
"""

import json
import logging
import sys
import threading
import time
import uuid
from collections import defaultdict, deque
from contextlib import contextmanager
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path
from typing import Any, Dict, Optional


# ── JSON Log Formatter ────────────────────────────────────────────────────────

class _JSONFormatter(logging.Formatter):
    """Emit every record as a single JSON line with timestamp and level."""

    _SKIP = frozenset(logging.LogRecord.__dict__.keys()) | {
        "message", "asctime", "args", "msg", "exc_text", "stack_info",
        "created", "msecs", "relativeCreated", "thread", "threadName",
        "processName", "process", "pathname", "filename", "module",
        "funcName", "lineno", "levelno",
    }

    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "ts":     datetime.now(timezone.utc).isoformat(),
            "level":  record.levelname,
            "logger": record.name,
            "msg":    record.getMessage(),
            "rid":    _ctx.get("request_id", "-"),
        }
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        for k, v in record.__dict__.items():
            if k not in self._SKIP and not k.startswith("_"):
                payload[k] = v
        return json.dumps(payload, default=str)


def get_logger(name: str, log_file: Optional[Path] = None) -> logging.Logger:
    """
    Return a structured JSON logger writing to stderr and optionally a file.
    Idempotent — calling twice with the same name returns the same logger.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    fmt = _JSONFormatter()
    sh = logging.StreamHandler(sys.stderr)
    sh.setFormatter(fmt)
    logger.addHandler(sh)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    return logger


# ── Request Context ───────────────────────────────────────────────────────────

_ctx: Dict[str, Any] = {}
_ctx_lock = threading.local()


def set_request_id(req_id: Optional[str] = None) -> str:
    """Set (or generate) a request ID for the current logical operation."""
    rid = req_id or str(uuid.uuid4())[:8]
    _ctx["request_id"] = rid
    return rid


def get_request_id() -> str:
    return _ctx.get("request_id", "-")


@contextmanager
def request_scope(req_id: Optional[str] = None):
    """Context manager that sets a request ID and clears it on exit."""
    rid = set_request_id(req_id)
    try:
        yield rid
    finally:
        _ctx.pop("request_id", None)


# ── Trace / Operation Decorator ───────────────────────────────────────────────

def trace_op(operation: str = "", logger_name: str = "trace"):
    """
    Decorator that records duration, success/failure, and request_id.

        @trace_op("score_health_check")
        def score_checks(data): ...
    """
    def decorator(fn):
        _op = operation or fn.__qualname__
        _log = get_logger(logger_name)

        @wraps(fn)
        def wrapper(*args, **kwargs):
            t0 = time.perf_counter()
            rid = get_request_id()
            try:
                result = fn(*args, **kwargs)
                dur_ms = round((time.perf_counter() - t0) * 1000, 2)
                _log.info("op_ok", extra={"op": _op, "dur_ms": dur_ms, "rid": rid})
                metrics.observe("op_duration_ms", dur_ms, op=_op)
                metrics.inc("op_total", op=_op, status="ok")
                return result
            except Exception as exc:
                dur_ms = round((time.perf_counter() - t0) * 1000, 2)
                _log.error(
                    "op_err",
                    extra={"op": _op, "dur_ms": dur_ms, "rid": rid, "err": str(exc)},
                    exc_info=True,
                )
                metrics.inc("op_total", op=_op, status="error")
                raise

        return wrapper
    return decorator


# ── Metrics Registry ──────────────────────────────────────────────────────────

def _lkey(name: str, labels: dict) -> str:
    if not labels:
        return name
    parts = ",".join(f'{k}="{v}"' for k, v in sorted(labels.items()))
    return f"{name}{{{parts}}}"


def _pct(data: list, p: float) -> float:
    if not data:
        return 0.0
    return data[int((len(data) - 1) * p)]


class MetricsRegistry:
    """
    Thread-safe in-process metrics store.
    Compatible with the SORFIX monitoring.py interface — drop-in replacement.
    Exports Prometheus text format at .prometheus_text().
    """

    def __init__(self):
        self._counters:   Dict[str, float] = defaultdict(float)
        self._gauges:     Dict[str, float] = defaultdict(float)
        self._histograms: Dict[str, deque] = defaultdict(lambda: deque(maxlen=10_000))
        self._lock = threading.Lock()

    def inc(self, name: str, value: float = 1.0, **labels):
        key = _lkey(name, labels)
        with self._lock:
            self._counters[key] += value

    def set_gauge(self, name: str, value: float, **labels):
        key = _lkey(name, labels)
        with self._lock:
            self._gauges[key] = value

    def observe(self, name: str, value: float, **labels):
        key = _lkey(name, labels)
        with self._lock:
            self._histograms[key].append(value)

    def percentile(self, name: str, p: float, **labels) -> float:
        key = _lkey(name, labels)
        with self._lock:
            dq = self._histograms.get(key)
            raw = list(dq) if dq else []
        return _pct(sorted(raw), p)

    def prometheus_text(self) -> str:
        with self._lock:
            counters = list(self._counters.items())
            gauges   = list(self._gauges.items())
            hist_raw = {k: list(dq) for k, dq in self._histograms.items()}

        lines: list = []
        seen: set = set()

        for k, v in counters:
            base = k.split("{")[0]
            if base not in seen:
                lines.append(f"# TYPE {base} counter")
                seen.add(base)
            lines.append(f"{k} {v}")

        for k, v in gauges:
            base = k.split("{")[0]
            if base not in seen:
                lines.append(f"# TYPE {base} gauge")
                seen.add(base)
            lines.append(f"{k} {v}")

        for k, raw in hist_raw.items():
            base = k.split("{")[0]
            lbl  = k[len(base):]
            data = sorted(raw)
            if data:
                if base not in seen:
                    lines.append(f"# TYPE {base} histogram")
                    seen.add(base)
                lines.append(f"{base}_count{lbl} {len(data)}")
                lines.append(f"{base}_p50{lbl}   {_pct(data, .50)}")
                lines.append(f"{base}_p95{lbl}   {_pct(data, .95)}")
                lines.append(f"{base}_p99{lbl}   {_pct(data, .99)}")

        return "\n".join(lines)

    def snapshot(self) -> dict:
        with self._lock:
            c = dict(self._counters)
            g = dict(self._gauges)
            h = {k: list(dq) for k, dq in self._histograms.items()}
        return {
            "counters": c,
            "gauges":   g,
            "histograms": {
                k: {
                    "count": len(v),
                    "p50":   _pct(sorted(v), .50),
                    "p95":   _pct(sorted(v), .95),
                    "p99":   _pct(sorted(v), .99),
                }
                for k, v in h.items()
            },
        }

    def reset(self):
        """Clear all metrics — useful in tests."""
        with self._lock:
            self._counters.clear()
            self._gauges.clear()
            self._histograms.clear()


# Global singleton
metrics = MetricsRegistry()
