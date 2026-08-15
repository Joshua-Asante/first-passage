"""Tests for ops/c1_rail/c1_rail_arm.py — the validated arm/disarm config editor.

Split follows the repo's standing pattern: the config TRANSFORM is pure and
fully tested here; the fly-ssh transport around it is operator-run and
deliberately not simulated (same split as c1_rail_listener vs its HTTP adapter).

The load-bearing properties:
  - arming produces a config the rail's OWN gate accepts (no drift between
    this tool and c1_rail_listener.arming_expiry_reason)
  - arming is refused when it would produce a config the host would reject
  - disarm CLEARS the deadline, so a later bare dry_run=false cannot inherit
    a window nobody granted
  - no secret ever reaches stdout
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

import pytest

import c1_rail_arm
from c1_rail_arm import (
    ArmError,
    describe,
    describe_m1_gate,
    m1_acceptance_reason,
    main,
    plan_arm,
    plan_disarm,
)
from c1_rail_listener import arming_expiry_reason

SECRETS = {
    "secret_key": "SECRET-43-CHAR-VALUE-must-never-be-printed",
    "webhook_secret": "WEBHOOK-SECRET-VALUE",
    "path_token": "PATH-TOKEN-VALUE-0123456789abcdef0123",
    "crosstrade_api_token": "BEARER-TOKEN-VALUE",
}

# Must match scripts/validate_c1_monitoring_acceptance.REQUIRED_DRILLS — the
# arm path now invokes that validator, so fixtures that only set status=RESOLVED
# are the defect under test, not a usable default.
_REQUIRED_DRILLS = (
    "transport_unknown",
    "partial_fill_confirmed_base",
    "rejected_entry_no_add",
    "exit_on_equity_failure",
    "restart_confirmed_base",
    "b6_wrong_secret_shape",
)


def _valid_acceptance_doc(status: str) -> dict:
    """Minimal artifact that clears validate() for the given status."""
    doc = {
        "schema_version": 1,
        "status": status,
        "adr": "2026-07-22-c1-venue-native-monitoring-maturity.md",
        "code_commit_or_branch": "test-fixture",
        "offline_tests_note": "fixture for tests/ops/test_c1_rail_arm.py",
        "secrets_present": False,
    }
    if status == "RESOLVED":
        doc.update(
            {
                "fixture_hashes": {
                    "tests/ops/test_c1_rail_arm.py": "a" * 64,
                },
                "dry_run_strategy_signal_event_id":
                    "00000000-0000-4000-8000-000000000001",
                "sim_chain_ok_event_id":
                    "00000000-0000-4000-8000-000000000002",
                "reconcile_verdict": "CHAIN_OK",
                "notification_alert_id":
                    "00000000-0000-4000-8000-000000000003",
                "notification_acked": True,
                "drills": {name: True for name in _REQUIRED_DRILLS},
                "operator_signoff": {"operator": "test-fixture"},
            }
        )
    return doc


@pytest.fixture(autouse=True)
def _m1_resolved(tmp_path_factory, monkeypatch):
    """Point the M1 interlock at a *validator-passing* RESOLVED artifact.

    Rationale: every pre-existing test here is about the CONFIG TRANSFORM, not
    about the M1 gate. Without this they would all fail on the real repo
    artifact (status CODE_LANDED) and their failure would say nothing about the
    thing they test. The gate itself is covered by the dedicated tests below,
    which pass `acceptance_path=` explicitly and therefore ignore this default.

    The fixture must clear `validate(..., require_resolved=True)` — a bare
    `{"status":"RESOLVED"}` is the forged-pass defect, not a usable default.
    """
    path = tmp_path_factory.mktemp("m1") / "M1_MONITORING_ACCEPTANCE.json"
    path.write_text(json.dumps(_valid_acceptance_doc("RESOLVED")),
                    encoding="utf-8")
    monkeypatch.setattr(c1_rail_arm, "DEFAULT_ACCEPTANCE_PATH", path)
    return path


def _acceptance(tmp_path, status):
    """Write a validator-honest acceptance artifact; return its path."""
    p = tmp_path / "M1_MONITORING_ACCEPTANCE.json"
    p.write_text(json.dumps(_valid_acceptance_doc(status)), encoding="utf-8")
    return p


def _forged_resolved_only(tmp_path):
    """Status-only forged pass — no drill/signoff fields (audit §5.4 shape)."""
    p = tmp_path / "M1_MONITORING_ACCEPTANCE.json"
    raw = '{"status":"RESOLVED"}'
    assert "status" in json.loads(raw)
    assert len(raw.encode("utf-8")) < 32  # tiny; not a real acceptance record
    p.write_text(raw, encoding="utf-8")
    return p


def _cfg(**overrides):
    cfg = dict(
        bind_host="0.0.0.0", bind_port=8080,
        account="TEST_ACCT_000000000", equity_source="crosstrade",
        equity_field="balance.netLiq", destination="tradovate",
        dry_run=True, armed_until=None,
        events_log_path="/data/c1_rail_events.jsonl",
        **SECRETS,
    )
    cfg.update(overrides)
    return cfg


# ── arming produces something the rail itself accepts ─────────────────────

def test_arm_produces_config_the_rail_gate_accepts():
    """No drift: the tool validates with the gate's own predicate."""
    armed = plan_arm(_cfg(), hours=4)
    assert armed["dry_run"] is False
    assert arming_expiry_reason(armed) is None


def test_arm_deadline_is_absolute_and_offset_aware():
    now = datetime(2026, 7, 28, 13, 0, tzinfo=timezone.utc)
    armed = plan_arm(_cfg(), hours=4, now=now)
    assert armed["armed_until"] == "2026-07-28T17:00:00+00:00"
    parsed = datetime.fromisoformat(armed["armed_until"])
    assert parsed.tzinfo is not None, "must carry an explicit offset"


def test_arm_self_check_uses_the_instant_that_built_the_deadline():
    """Regression 2026-07-28: the self-check re-read the real clock, so any
    test pinning an instant began failing the moment wall-time passed the
    pinned deadline. A pinned-instant arm must hold indefinitely."""
    long_past = datetime(2020, 1, 1, 9, 30, tzinfo=timezone.utc)
    armed = plan_arm(_cfg(), hours=4, now=long_past)
    assert armed["armed_until"] == "2020-01-01T13:30:00+00:00"
    assert arming_expiry_reason(armed, now=long_past) is None
    # The real-clock reading of that same config is still EXPIRED — a pinned
    # instant buys determinism here, never a usable window on the live rail.
    assert arming_expiry_reason(armed) is not None


def test_arm_still_refuses_a_window_that_truncates_backward():
    """The self-check must not become a tautology now that it shares the clock.

    `.replace(microsecond=0)` truncates BACKWARD, so a sub-second window lands
    a deadline at or before `now` — the one case where hours>0 still yields an
    already-expired config, and the reason this limb stays load-bearing.
    """
    now = datetime(2026, 7, 28, 13, 0, 0, 500_000, tzinfo=timezone.utc)
    with pytest.raises(ArmError, match="expired"):
        plan_arm(_cfg(), hours=1e-6, now=now)


def test_arm_refuses_without_events_log_path():
    """Mirrors the boot gate — better to fail here than at boot."""
    with pytest.raises(ArmError, match="events_log_path"):
        plan_arm(_cfg(events_log_path=None), hours=4)


@pytest.mark.parametrize("hours", [0, -1, -0.5])
def test_arm_refuses_non_positive_window(hours):
    with pytest.raises(ArmError, match="must be positive"):
        plan_arm(_cfg(), hours=hours)


def test_arm_does_not_mutate_input():
    original = _cfg()
    snapshot = json.dumps(original, sort_keys=True)
    plan_arm(original, hours=4)
    assert json.dumps(original, sort_keys=True) == snapshot


# ── disarm ────────────────────────────────────────────────────────────────

def test_disarm_sets_dry_run_and_clears_deadline():
    armed = plan_arm(_cfg(), hours=4)
    disarmed = plan_disarm(armed)
    assert disarmed["dry_run"] is True
    assert disarmed["armed_until"] is None


def test_disarm_clears_deadline_so_it_cannot_be_inherited():
    """A stale future deadline left behind would let a later bare
    dry_run=false edit inherit a window nobody consciously granted."""
    armed = plan_arm(_cfg(), hours=8)
    disarmed = plan_disarm(armed)
    resurrected = dict(disarmed)
    resurrected["dry_run"] = False          # someone flips only the flag
    assert arming_expiry_reason(resurrected) is not None, (
        "a bare dry_run=false must NOT inherit a usable window")


# ── secret hygiene ────────────────────────────────────────────────────────

def test_describe_never_emits_secrets():
    text = describe(plan_arm(_cfg(), hours=4))
    for name, value in SECRETS.items():
        assert value not in text, f"{name} value leaked into describe()"


def test_cli_output_never_emits_secrets(tmp_path, capsys):
    path = tmp_path / "c1_rail_config.json"
    path.write_text(json.dumps(_cfg()), encoding="utf-8")

    assert main(["--config", str(path), "--arm", "--hours", "4"]) == 0
    captured = capsys.readouterr()
    combined = captured.out + captured.err
    for name, value in SECRETS.items():
        assert value not in combined, f"{name} value leaked to CLI output"


# ── CLI round-trip on disk ────────────────────────────────────────────────

def test_cli_arm_then_disarm_round_trip(tmp_path, capsys):
    path = tmp_path / "c1_rail_config.json"
    path.write_text(json.dumps(_cfg()), encoding="utf-8")

    assert main(["--config", str(path), "--arm", "--hours", "4"]) == 0
    armed = json.loads(path.read_text(encoding="utf-8"))
    assert armed["dry_run"] is False
    assert arming_expiry_reason(armed) is None
    # secrets survive the rewrite untouched
    for name, value in SECRETS.items():
        assert armed[name] == value

    assert main(["--config", str(path), "--disarm"]) == 0
    disarmed = json.loads(path.read_text(encoding="utf-8"))
    assert disarmed["dry_run"] is True
    assert disarmed["armed_until"] is None


def test_cli_arm_writes_backup(tmp_path):
    path = tmp_path / "c1_rail_config.json"
    path.write_text(json.dumps(_cfg()), encoding="utf-8")
    main(["--config", str(path), "--arm", "--hours", "4"])
    backup = path.with_suffix(path.suffix + ".prev")
    assert backup.exists()
    assert json.loads(backup.read_text(encoding="utf-8"))["dry_run"] is True


def test_cli_warns_restart_required(tmp_path, capsys):
    """The edit is inert until restart; that must be impossible to miss."""
    path = tmp_path / "c1_rail_config.json"
    path.write_text(json.dumps(_cfg()), encoding="utf-8")
    main(["--config", str(path), "--arm", "--hours", "4"])
    out = capsys.readouterr().out
    assert "NOT YET IN EFFECT" in out
    assert "fly apps restart" in out


def test_cli_refuses_and_leaves_file_untouched_on_bad_arm(tmp_path):
    path = tmp_path / "c1_rail_config.json"
    path.write_text(json.dumps(_cfg(events_log_path=None)), encoding="utf-8")
    before = path.read_text(encoding="utf-8")
    assert main(["--config", str(path), "--arm", "--hours", "4"]) == 1
    assert path.read_text(encoding="utf-8") == before, "refused write must be a no-op"


def test_cli_status_is_read_only(tmp_path):
    path = tmp_path / "c1_rail_config.json"
    path.write_text(json.dumps(_cfg()), encoding="utf-8")
    before = path.read_text(encoding="utf-8")
    assert main(["--config", str(path), "--status"]) == 0
    assert path.read_text(encoding="utf-8") == before


def test_cli_status_flags_an_expired_window(tmp_path, capsys):
    stale = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    path = tmp_path / "c1_rail_config.json"
    path.write_text(json.dumps(_cfg(dry_run=False, armed_until=stale)),
                    encoding="utf-8")
    main(["--config", str(path), "--status"])
    assert "EXPIRED" in capsys.readouterr().out


def test_cli_status_reports_m1_gate(tmp_path, capsys):
    """`--status` must surface whether `--arm` would clear the M1 interlock.

    Config fields alone cannot answer that — the gate lives in a separate
    artifact — so an operator previously had to attempt an arm to find out.
    """
    path = tmp_path / "c1_rail_config.json"
    path.write_text(json.dumps(_cfg()), encoding="utf-8")

    assert main(["--config", str(path), "--status",
                 "--acceptance", str(_acceptance(tmp_path, "CODE_LANDED"))]) == 0
    out = capsys.readouterr().out
    assert "m1_gate:" in out
    assert "status='CODE_LANDED'" in out
    assert "result=FAIL" in out

    assert main(["--config", str(path), "--status",
                 "--acceptance", str(_acceptance(tmp_path, "RESOLVED"))]) == 0
    out = capsys.readouterr().out
    assert "status='RESOLVED'" in out
    assert "result=PASS" in out

    # Forged status-only artifact must NOT report PASS (audit 2026-08-08 §5.4).
    forged_dir = tmp_path / "forged_status"
    forged_dir.mkdir()
    forged = _forged_resolved_only(forged_dir)
    assert main(["--config", str(path), "--status",
                 "--acceptance", str(forged)]) == 0
    out = capsys.readouterr().out
    assert "status='RESOLVED'" in out
    assert "result=FAIL" in out


def test_describe_m1_gate_unreadable_is_fail(tmp_path):
    """FAIL-SAFE mirror of m1_acceptance_reason — absence never reads as PASS."""
    line = describe_m1_gate(tmp_path / "missing.json")
    assert "result=FAIL" in line
    assert "status=None" in line


# ── M1 acceptance interlock (ADR Addendum 2026-07-31b) ─────────────────────
#
# The gate is SOFT by design: the operator keeps the ability to arm against an
# unresolved M1. What it removes is the ability to do so SILENTLY — which is
# the failure mode of 2026-07-28 and 2026-07-31, where each deviation recorded
# "with the amendment to be written after the fact" and neither was written.

def test_arm_refused_when_m1_not_resolved(tmp_path):
    with pytest.raises(ArmError, match="validation|RESOLVED|CODE_LANDED"):
        plan_arm(_cfg(), hours=4,
                 acceptance_path=_acceptance(tmp_path, "CODE_LANDED"))


def test_arm_allowed_when_m1_resolved(tmp_path):
    """Positive control — a validator-passing RESOLVED gate must not block."""
    armed = plan_arm(_cfg(), hours=4,
                     acceptance_path=_acceptance(tmp_path, "RESOLVED"))
    assert armed["dry_run"] is False


def test_arm_allowed_when_acknowledged(tmp_path):
    """Escape hatch: structurally valid but unresolved artifact + reason."""
    armed = plan_arm(_cfg(), hours=4,
                     acceptance_path=_acceptance(tmp_path, "CODE_LANDED"),
                     acknowledge_unresolved="attended B7 Stage 2, operator GO")
    assert armed["dry_run"] is False


def test_forged_status_only_resolved_does_not_arm(tmp_path):
    """Audit 2026-08-08 §5 item 4 — the 24-byte forged pass must FAIL CLOSED.

    `{"status":"RESOLVED"}` clears the old status-only read, while
    `scripts/validate_c1_monitoring_acceptance.py --require-resolved` rejects
    those same bytes (~19 errors). The arm path must invoke that validator.
    """
    forged = _forged_resolved_only(tmp_path)
    assert m1_acceptance_reason(forged) is not None
    with pytest.raises(ArmError, match="validation"):
        plan_arm(_cfg(), hours=4, acceptance_path=forged)


def test_forged_resolved_cannot_be_acknowledged_past(tmp_path):
    """Acknowledgement bypasses *unresolved*, never *invalid/forged*."""
    forged = _forged_resolved_only(tmp_path)
    with pytest.raises(ArmError, match="validation|Acknowledgement|invalid|forged"):
        plan_arm(
            _cfg(), hours=4, acceptance_path=forged,
            acknowledge_unresolved="trying to launder a forged RESOLVED",
        )


def test_malformed_json_acceptance_does_not_arm(tmp_path):
    p = tmp_path / "M1_MONITORING_ACCEPTANCE.json"
    p.write_text("{not json", encoding="utf-8")
    with pytest.raises(ArmError):
        plan_arm(_cfg(), hours=4, acceptance_path=p)


def test_missing_acceptance_file_does_not_arm(tmp_path):
    with pytest.raises(ArmError):
        plan_arm(_cfg(), hours=4,
                 acceptance_path=tmp_path / "does-not-exist.json")


@pytest.mark.parametrize("write,label", [
    (lambda p: None, "missing file"),
    (lambda p: p.write_text("{not json", encoding="utf-8"), "malformed JSON"),
    (lambda p: p.write_text('["a list"]', encoding="utf-8"), "not an object"),
    (lambda p: p.write_text("{}", encoding="utf-8"), "no status key"),
    (lambda p: p.write_text('{"status": null}', encoding="utf-8"), "null status"),
    (lambda p: p.write_text('{"status": "resolved"}', encoding="utf-8"), "wrong case"),
])
def test_unreadable_acceptance_is_treated_as_unresolved(tmp_path, write, label):
    """FAIL-SAFE: absence must never read as permission. This is the one
    direction the interlock exists to prevent — an agent or a bad deploy that
    loses the artifact must NOT thereby gain the ability to arm."""
    p = tmp_path / "M1_MONITORING_ACCEPTANCE.json"
    write(p)
    reason = m1_acceptance_reason(p)
    assert reason is not None, f"{label} must read as NOT RESOLVED"
    with pytest.raises(ArmError):
        plan_arm(_cfg(), hours=4, acceptance_path=p)


def test_acknowledged_arm_writes_a_deviation_record(tmp_path):
    """The record is the whole point of the escape hatch."""
    events = tmp_path / "events.jsonl"
    cfg_path = tmp_path / "cfg.json"
    cfg_path.write_text(json.dumps(_cfg(events_log_path=str(events))),
                        encoding="utf-8")

    rc = main(["--config", str(cfg_path), "--arm", "--hours", "1",
               "--acceptance", str(_acceptance(tmp_path, "CODE_LANDED")),
               "--acknowledge-m1-unresolved", "attended session, operator GO"])

    assert rc == 0
    assert json.loads(cfg_path.read_text(encoding="utf-8"))["dry_run"] is False
    records = [json.loads(line) for line in
               events.read_text(encoding="utf-8").splitlines() if line.strip()]
    dev = [r for r in records if r["kind"] == "arming_deviation"]
    assert len(dev) == 1
    assert dev[0]["operator_reason"] == "attended session, operator GO"
    assert "CODE_LANDED" in dev[0]["gate_reason"]


def test_arm_refused_if_the_deviation_cannot_be_recorded(tmp_path):
    """No record, no arm. If the ledger is unwritable the escape hatch closes
    — otherwise the acknowledgement path would be a way to arm with NO trace,
    which is strictly worse than the gate it bypasses."""
    cfg_path = tmp_path / "cfg.json"
    unwritable = tmp_path / "nodir"
    unwritable.write_text("i am a file, not a directory", encoding="utf-8")
    cfg_path.write_text(
        json.dumps(_cfg(events_log_path=str(unwritable / "events.jsonl"))),
        encoding="utf-8")

    rc = main(["--config", str(cfg_path), "--arm", "--hours", "1",
               "--acceptance", str(_acceptance(tmp_path, "CODE_LANDED")),
               "--acknowledge-m1-unresolved", "attempt"])

    assert rc == 1
    assert json.loads(cfg_path.read_text(encoding="utf-8"))["dry_run"] is True, \
        "config must be UNTOUCHED when the deviation could not be recorded"


def test_disarm_never_consults_the_m1_gate(tmp_path):
    """The SAFE direction must never be blocked by the gate — including when
    the artifact is missing entirely."""
    cfg_path = tmp_path / "cfg.json"
    cfg_path.write_text(json.dumps(_cfg(dry_run=False, armed_until="2099-01-01T00:00:00+00:00")),
                        encoding="utf-8")
    rc = main(["--config", str(cfg_path), "--disarm",
               "--acceptance", str(tmp_path / "does-not-exist.json")])
    assert rc == 0
    assert json.loads(cfg_path.read_text(encoding="utf-8"))["dry_run"] is True
