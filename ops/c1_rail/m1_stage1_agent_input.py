"""Shared validation of declared attended capture provenance; not authentication."""
from datetime import datetime, timezone
import re


def aware_time(value):
    if not isinstance(value, str):
        raise ValueError("timestamp required")
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None or result.utcoffset() is None:
        raise ValueError("timezone required")
    return result.astimezone(timezone.utc)


def validate_authorization(manifest):
    value = manifest.get("operator_authorization_sha256")
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        raise ValueError("operator authorization required")


def validate_capture(capture, manifest, now):
    keys = {"actor", "captured_at", "chart_timestamp", "venue_contract", "bar_period_s"}
    if (not isinstance(capture, dict) or set(capture) != keys
            or capture["actor"] != "codex"
            or capture["venue_contract"] != manifest["venue_contract"]
            or type(capture["bar_period_s"]) is not int or capture["bar_period_s"] != 60):
        raise ValueError("capture binding required")
    target = aware_time(manifest["target"])
    captured = aware_time(capture["captured_at"])
    if (aware_time(capture["chart_timestamp"]) != target
            or not 60 <= (captured-target).total_seconds() <= 120 or captured > now):
        raise ValueError("closed target capture required")


def validate_evidence(item):
    manifest = item["manifest"]
    validate_authorization(manifest)
    evidence = item["agent_evidence"]
    if set(evidence) != {"enable", "inject", "capture", "bar_sha256"}:
        raise ValueError("complete agent evidence required")
    for action in ("enable", "inject"):
        if set(evidence[action]) != {"actor", "at"} or evidence[action]["actor"] != "codex":
            raise ValueError("agent actor required")
    enabled = aware_time(evidence["enable"]["at"])
    injected = aware_time(evidence["inject"]["at"])
    target = aware_time(manifest["target"])
    if not enabled < target or not 60 <= (injected-target).total_seconds() <= 120:
        raise ValueError("agent action timing mismatch")
    validate_capture(evidence["capture"], manifest, injected)
    if evidence["bar_sha256"] != item["bar_sha256"]:
        raise ValueError("capture digest mismatch")
    return evidence
