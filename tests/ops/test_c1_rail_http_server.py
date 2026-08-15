"""Tests for ops/c1_rail/c1_rail_http_server.py §2.5 pure helpers.

Socket wiring + real urllib GET remain untested-by-design (same split as
crosstrade_payload._urllib_sender). These tests cover the frozen contract:
  - §2.5(A) path-token gate (authorized path only)
  - §2.5(B) equity parse + source dispatch (file / crosstrade via injected getter)
  - load_config validation (path_token length, equity_source, crosstrade keys)
"""
from __future__ import annotations

import json
import logging
from pathlib import Path

import pytest

from c1_rail_http_server import (
    PATH_TOKEN_MIN_LEN,
    EquityReadError,
    build_parsed_fields,
    fetch_crosstrade_equity,
    is_authorized_sizing_path,
    load_config,
    parse_crosstrade_account_equity,
    read_current_equity,
    redact_token,
    resolve_current_equity,
    sizing_post_path,
    startup_log_line,
)

TOKEN = "a" * PATH_TOKEN_MIN_LEN  # exactly the floor


def _future_iso(hours=1.0):
    """A still-open arming deadline. Computed, never hardcoded — a literal
    date would pass until it arrived and then fail the suite spuriously."""
    from datetime import datetime, timedelta, timezone
    return (datetime.now(timezone.utc) + timedelta(hours=hours)).isoformat()


def _past_iso(hours=1.0):
    from datetime import datetime, timedelta, timezone
    return (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()


def _base_cfg(tmp_path: Path, **overrides) -> dict:
    equity = tmp_path / "c1_current_equity.json"
    equity.write_text(json.dumps({"current_equity": 100_000.0}), encoding="utf-8")
    cfg = {
        "bind_host": "127.0.0.1",
        "bind_port": 8787,
        "lifecycle_state_path": str(tmp_path / "lifecycle_state.json"),
        "dd_state_path": str(tmp_path / "c1_dd_state.json"),
        "constants_path": str(tmp_path / "c1_sizing_constants.json"),
        "equity_path": str(equity),
        "path_token": TOKEN,
        "account": "TDFYSL100642026",
        "secret_key": "test-secret",
        "webhook_id": "abc",
        "webhook_secret": "xyz",
        "dry_run": True,
        "equity_source": "file",
    }
    cfg.update(overrides)
    return cfg


def _write_cfg(tmp_path: Path, **overrides) -> Path:
    path = tmp_path / "c1_rail_config.json"
    path.write_text(json.dumps(_base_cfg(tmp_path, **overrides)), encoding="utf-8")
    return path


# ── §2.5(A) path-token gate ───────────────────────────────────────────────

def test_sizing_post_path_shape():
    assert sizing_post_path(TOKEN) == f"/c1/{TOKEN}"


def test_authorized_path_exact_match():
    assert is_authorized_sizing_path(f"/c1/{TOKEN}", TOKEN) is True


def test_authorized_path_ignores_query_string():
    assert is_authorized_sizing_path(f"/c1/{TOKEN}?x=1", TOKEN) is True


def test_wrong_path_rejected():
    assert is_authorized_sizing_path("/", TOKEN) is False
    assert is_authorized_sizing_path("/c1/", TOKEN) is False
    assert is_authorized_sizing_path(f"/c1/{TOKEN}x", TOKEN) is False
    assert is_authorized_sizing_path(f"/c1/{TOKEN}/", TOKEN) is False
    assert is_authorized_sizing_path("/webhook", TOKEN) is False


def test_wrong_token_rejected():
    other = "b" * PATH_TOKEN_MIN_LEN
    assert is_authorized_sizing_path(f"/c1/{other}", TOKEN) is False


# ── §2.5(A) log redaction (path_token must never reach the logs) ──────────

def test_redact_token_replaces_all_occurrences():
    t = "SECRET123"
    assert redact_token(f"/c1/{t}/x {t}", t) == "/c1/<redacted>/x <redacted>"


def test_redact_token_noop_when_absent():
    assert redact_token("/c1/other", "SECRET123") == "/c1/other"


def test_redact_token_empty_token_is_noop():
    # never replace the empty string (would corrupt every message)
    assert redact_token("/c1/anything", "") == "/c1/anything"


def test_redact_token_scrubs_nearmiss_path():
    # a trailing-slash near-miss still embeds the real token verbatim
    t = "a" * PATH_TOKEN_MIN_LEN
    assert t not in redact_token(f"/c1/{t}/", t)


def test_startup_log_line_never_contains_token(tmp_path):
    t = "b" * PATH_TOKEN_MIN_LEN
    cfg = _base_cfg(tmp_path, path_token=t)
    line = startup_log_line(cfg)
    assert t not in line               # the secret never appears
    assert "<redacted>" in line        # but the route shape is still shown
    assert "127.0.0.1:8787" in line    # operational facts preserved
    assert "dry_run" in line and "equity_source" in line
    assert "keep bind_host" not in line   # stale same-box-proxy advice removed


def test_load_config_armed_requires_events_log_path(tmp_path):
    path = _write_cfg(tmp_path, dry_run=False)
    with pytest.raises(ValueError, match="events_log_path"):
        load_config(path)

    # armed_until is supplied here so this test isolates the events_log_path
    # gate; the arming-expiry boot gate is exercised on its own below.
    path = _write_cfg(
        tmp_path, dry_run=False,
        events_log_path=str(tmp_path / "events.jsonl"),
        armed_until=_future_iso(),
    )
    cfg = load_config(path)
    assert cfg["events_log_path"].endswith("events.jsonl")


# ── arming expiry: boot gate (2026-07-27 forgotten-disarm failure class) ──

def _armed_cfg(tmp_path, **overrides):
    base = dict(dry_run=False, events_log_path=str(tmp_path / "events.jsonl"))
    base.update(overrides)
    return _write_cfg(tmp_path, **base)


# --- Implicit disarm at boot (2026-07-31 self-brick fix) -------------------
#
# These four cases previously asserted `pytest.raises(ValueError)` — the rail
# refused to boot on any invalid arming window. That behaviour bricked the host
# on 2026-07-31: the deadline lapsed while the volume still said dry_run=false,
# the boot gate raised, Fly stopped the machine at max restart count, and the
# documented remedy (edit /data, restart) was unreachable because editing /data
# needs `fly ssh` and `fly ssh` needs a booted machine.
#
# The assertions are REPLACED rather than preserved: keeping them would keep
# the defect. Coverage is unchanged — each case still pins a distinct invalid
# shape — but the expected outcome is now "boots DISARMED", which is what the
# per-request gate already enforced anyway.


@pytest.mark.parametrize("armed_until,shape", [
    (None, "absent"),
    ("__PAST__", "expired"),
    ("2099-01-01T00:00:00", "timezone-naive"),
    ("tomorrow-ish", "unparseable"),
])
def test_boot_implicitly_disarms_on_invalid_window(tmp_path, armed_until, shape):
    """Every invalid arming window boots DISARMED instead of refusing."""
    kwargs = {} if armed_until is None else {
        "armed_until": _past_iso() if armed_until == "__PAST__" else armed_until}
    path = _armed_cfg(tmp_path, **kwargs)

    cfg = load_config(path)

    assert cfg["dry_run"] is True, f"{shape}: must boot disarmed, not armed"
    assert cfg["armed_until"] is None, f"{shape}: stale deadline must be cleared"


def test_implicit_disarm_is_loud(tmp_path, caplog):
    """A silent implicit disarm would be worse than the brick — the operator
    must be told, since the on-disk config still says dry_run=false."""
    path = _armed_cfg(tmp_path, armed_until=_past_iso())
    with caplog.at_level(logging.WARNING, logger="c1_rail_http"):
        load_config(path)
    assert any("IMPLICIT DISARM" in r.message or "IMPLICIT DISARM" in r.getMessage()
               for r in caplog.records), "expected a WARNING naming the implicit disarm"


def test_implicit_disarm_does_not_rewrite_the_config_file(tmp_path):
    """In-memory only. load_config is called by tooling and tests; a write
    side-effect would surprise, and the volume may be read-only. The safe
    direction holds either way — the PROCESS runs disarmed."""
    path = _armed_cfg(tmp_path, armed_until=_past_iso())
    before = path.read_text(encoding="utf-8")
    load_config(path)
    assert path.read_text(encoding="utf-8") == before
    assert json.loads(before)["dry_run"] is False  # on-disk state genuinely unchanged


def test_boot_still_refuses_armed_without_events_log_path(tmp_path):
    """Negative control: the implicit-disarm path must not swallow the OTHER
    armed-boot gate. A missing events_log_path is a config defect, not an
    expired window, and still raises."""
    path = _write_cfg(tmp_path, dry_run=True, armed_until=_future_iso())
    cfg = json.loads(path.read_text(encoding="utf-8"))
    cfg["dry_run"] = False
    cfg.pop("events_log_path", None)
    path.write_text(json.dumps(cfg), encoding="utf-8")
    with pytest.raises(ValueError, match="events_log_path"):
        load_config(path)


def test_boot_accepts_armed_with_future_deadline(tmp_path):
    """Positive control — the gate must not reject a correct arming."""
    path = _armed_cfg(tmp_path, armed_until=_future_iso())
    cfg = load_config(path)
    assert cfg["dry_run"] is False


def test_boot_ignores_armed_until_when_disarmed(tmp_path):
    """A disarmed rail boots regardless of a stale/absent deadline —
    otherwise a forgotten armed_until would block the SAFE state."""
    path = _write_cfg(tmp_path, dry_run=True, armed_until=_past_iso())
    cfg = load_config(path)
    assert cfg["dry_run"] is True


def test_startup_log_line_shows_armed_until(tmp_path):
    """The boot line is what the operator reads to confirm state."""
    cfg = _base_cfg(tmp_path, dry_run=False, armed_until="2099-01-01T00:00:00+00:00")
    assert "armed_until=2099-01-01T00:00:00+00:00" in startup_log_line(cfg)
    disarmed = _base_cfg(tmp_path, dry_run=True)
    assert "armed_until=-" in startup_log_line(disarmed)


# ── load_config ───────────────────────────────────────────────────────────

def test_load_config_rejects_replace_path_token(tmp_path):
    path = _write_cfg(
        tmp_path,
        path_token="REPLACE_WITH_GE_32_CHAR_RANDOM_TOKEN________________",
    )
    with pytest.raises(ValueError, match="REPLACE"):
        load_config(path)


def test_load_config_defaults_equity_source_file(tmp_path):
    path = _write_cfg(tmp_path)
    # omit equity_source from file
    obj = json.loads(path.read_text(encoding="utf-8"))
    del obj["equity_source"]
    path.write_text(json.dumps(obj), encoding="utf-8")
    cfg = load_config(path)
    assert cfg["equity_source"] == "file"
    assert cfg["dry_run"] is True


def test_load_config_rejects_short_path_token(tmp_path):
    path = _write_cfg(tmp_path, path_token="too-short")
    with pytest.raises(ValueError, match="path_token"):
        load_config(path)


def test_load_config_crosstrade_requires_token_and_field(tmp_path):
    path = _write_cfg(tmp_path, equity_source="crosstrade")
    with pytest.raises(ValueError, match="crosstrade_api_token"):
        load_config(path)

    path = _write_cfg(
        tmp_path, equity_source="crosstrade",
        crosstrade_api_token="REPLACE_ME", equity_field="netLiquidation",
    )
    with pytest.raises(ValueError, match="crosstrade_api_token"):
        load_config(path)

    path = _write_cfg(
        tmp_path, equity_source="crosstrade",
        crosstrade_api_token="real-token-value",
        equity_field="REPLACE_AFTER_B6_VERIFY",
    )
    with pytest.raises(ValueError, match="equity_field"):
        load_config(path)


def test_load_config_crosstrade_accepts_real_keys(tmp_path):
    path = _write_cfg(
        tmp_path, equity_source="crosstrade",
        crosstrade_api_token="real-token-value",
        equity_field="netLiquidation",
    )
    cfg = load_config(path)
    assert cfg["equity_source"] == "crosstrade"
    assert cfg["equity_field"] == "netLiquidation"


# ── §2.5(B) equity parse / dispatch ───────────────────────────────────────

def test_read_current_equity_file(tmp_path):
    p = tmp_path / "eq.json"
    p.write_text(json.dumps({"current_equity": 98500.0}), encoding="utf-8")
    assert read_current_equity(p) == 98500.0


def test_read_current_equity_missing_fails_closed(tmp_path):
    with pytest.raises(EquityReadError, match="missing"):
        read_current_equity(tmp_path / "nope.json")


def test_parse_crosstrade_account_equity_happy():
    payload = {"success": True, "data": {"netLiquidation": 100_000.0, "name": "x"}}
    assert parse_crosstrade_account_equity(payload, "netLiquidation") == 100_000.0


def test_parse_crosstrade_rejects_success_false():
    with pytest.raises(EquityReadError, match="success"):
        parse_crosstrade_account_equity(
            {"success": False, "data": {"netLiquidation": 1}}, "netLiquidation")


def test_parse_crosstrade_rejects_missing_field():
    with pytest.raises(EquityReadError, match="missing"):
        parse_crosstrade_account_equity(
            {"success": True, "data": {"balance": 1}}, "netLiquidation")


def test_parse_crosstrade_rejects_nonpositive():
    with pytest.raises(EquityReadError, match="invalid"):
        parse_crosstrade_account_equity(
            {"success": True, "data": {"netLiquidation": 0}}, "netLiquidation")


def test_parse_crosstrade_account_equity_nested_dotted_path():
    # Live CrossTrade Tradovate shape (B6 verify 2026-07-19): net-liq is nested
    # under data.balance.netLiq — a dotted equity_field must navigate into it.
    payload = {"success": True, "data": {
        "accountId": "58", "name": "TDFYSL1",
        "balance": {"netLiq": 100_000.0, "netLiqSOD": 100_000.0, "cashUSD": 99_000.0}}}
    assert parse_crosstrade_account_equity(payload, "balance.netLiq") == 100_000.0


def test_parse_crosstrade_nested_missing_leaf():
    with pytest.raises(EquityReadError, match="missing"):
        parse_crosstrade_account_equity(
            {"success": True, "data": {"balance": {"cashUSD": 1}}}, "balance.netLiq")


def test_parse_crosstrade_nested_intermediate_not_dict():
    with pytest.raises(EquityReadError, match="missing"):
        parse_crosstrade_account_equity(
            {"success": True, "data": {"balance": 5}}, "balance.netLiq")


def test_fetch_crosstrade_equity_uses_injected_getter():
    calls = []

    def getter(url, headers):
        calls.append({"url": url, "headers": headers})
        return 200, {"success": True, "data": {"netLiquidation": 99_500.0}}

    eq = fetch_crosstrade_equity(
        account="acct-1", api_token="tok", equity_field="netLiquidation",
        getter=getter,
    )
    assert eq == 99_500.0
    assert len(calls) == 1
    assert calls[0]["url"].endswith("/v1/api/tv/accounts/acct-1")
    assert calls[0]["headers"]["Authorization"] == "Bearer tok"


def test_fetch_crosstrade_equity_http_error_fails_closed():
    def getter(url, headers):
        return 500, {"success": False}

    with pytest.raises(EquityReadError, match="HTTP 500"):
        fetch_crosstrade_equity(
            account="a", api_token="t", equity_field="netLiquidation",
            getter=getter)


def test_resolve_current_equity_file_dispatch(tmp_path):
    cfg = _base_cfg(tmp_path, equity_source="file")
    assert resolve_current_equity(cfg) == 100_000.0


def test_resolve_current_equity_crosstrade_dispatch(tmp_path):
    cfg = _base_cfg(
        tmp_path, equity_source="crosstrade",
        crosstrade_api_token="tok", equity_field="netLiquidation",
    )

    def getter(url, headers):
        return 200, {"success": True, "data": {"netLiquidation": 101_000.0}}

    assert resolve_current_equity(cfg, getter=getter) == 101_000.0

# ── request_received parsed fields (B7 slippage-capture prerequisite) ─────

def test_build_parsed_fields_well_formed_b1():
    payload = {
        "leg_id": "dj30_mym",
        "signal_type": "add",
        "bar_time": "2026-07-24T14:00:00Z",
        "close": 52737.0,
        "stop_dist_pts": 80.0,
    }
    parsed = build_parsed_fields(payload, "add")
    assert set(parsed) == {
        "leg_id", "signal_type", "bar_time", "close", "stop_dist_pts",
    }
    assert parsed["leg_id"] == "dj30_mym"
    assert parsed["signal_type"] == "add"
    assert parsed["bar_time"] == "2026-07-24T14:00:00Z"
    assert parsed["close"] == 52737.0
    assert parsed["stop_dist_pts"] == 80.0


def test_build_parsed_fields_missing_price_keys_yield_none():
    payload = {
        "leg_id": "nq_mnq",
        "signal_type": "entry",
        "bar_time": "2026-07-24T15:00:00Z",
    }
    parsed = build_parsed_fields(payload, "entry")
    assert parsed["close"] is None
    assert parsed["stop_dist_pts"] is None
    assert parsed["leg_id"] == "nq_mnq"


def test_build_parsed_fields_verbatim_no_coercion():
    payload = {
        "leg_id": "dj30_mym",
        "signal_type": "add",
        "bar_time": "t",
        "close": "52737",
        "stop_dist_pts": "80",
    }
    parsed = build_parsed_fields(payload, "add")
    assert parsed["close"] == "52737"
    assert isinstance(parsed["close"], str)
    assert parsed["stop_dist_pts"] == "80"
    assert isinstance(parsed["stop_dist_pts"], str)


def test_build_parsed_fields_uses_classified_signal_type():
    payload = {
        "leg_id": "dj30_mym",
        "signal_type": "entry",  # raw echo must NOT win
        "bar_time": "t",
        "close": 1.0,
        "stop_dist_pts": 2.0,
    }
    parsed = build_parsed_fields(payload, "add")
    assert parsed["signal_type"] == "add"

