"""Synthetic evidence only: exercise the offline TB-T1 command boundary."""
import hashlib
import json
import shutil
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/seal_account_snapshot.py"


@pytest.fixture
def case(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / ".gitignore").write_text("private/\n", encoding="utf-8")
    (tmp_path / "scripts").mkdir()
    shutil.copyfile(SCRIPT, tmp_path / "scripts/seal_account_snapshot.py")
    evidence = {}
    for role in ("E1", "E2", "E3"):
        path = tmp_path / f"{role}.txt"
        path.write_text(f"SYNTHETIC {role} fixture", encoding="utf-8")
        evidence[role] = path
    manifest = {
        "values": {
            "balance": 102000, "equity": 102000, "trailing_threshold": 99000,
            "prior_trade_days": 4, "prior_max_day_profit": 600,
            "consistency_display_pct": 30, "profit_target_display": 6000,
            "cash_adjustments_total": 0, "token_trade_fill_dates": [],
            "positions_export_shows_flat": True, "working_orders_count": 0,
        },
        "captured_at": {role: "2026-09-14T17:10:00-04:00" for role in evidence},
    }
    return tmp_path, manifest, evidence


def run(case, *, seal="2026-09-14T17:20:00-04:00", output="private/seal.json", cwd=None, extra=(),
        raw_manifest=None):
    root, manifest, evidence = case
    manifest_path = root / "manifest.json"
    manifest_path.write_text(json.dumps(manifest) if raw_manifest is None else raw_manifest,
                             encoding="utf-8")
    # The production CLI has no clock override. Inject a synthetic clock only
    # in this subprocess test harness, keeping stdout/stderr behavior intact.
    harness = (
        "import runpy,sys; from datetime import datetime; "
        "ns=runpy.run_path(sys.argv[1]); clock=datetime.fromisoformat(sys.argv[2]); "
        "ns['main'].__globals__['utc_now']=lambda: clock; "
        "sys.exit(ns['main'](sys.argv[3:]))"
    )
    command = [sys.executable, "-c", harness, str(root / "scripts/seal_account_snapshot.py"),
               seal, "--manifest", str(manifest_path), "--output", str(root / output)]
    for role, path in evidence.items():
        command.extend([f"--{role.lower()}", str(path)])
    command.extend(extra)
    result = subprocess.run(command, cwd=cwd or root, capture_output=True, text=True, check=False)
    return result, root / output


def refuses(case, check, **kwargs):
    result, output = run(case, **kwargs)
    assert result.returncode == 2, result.stderr
    assert not result.stdout
    assert result.stderr.strip() == check
    assert not output.exists()


def test_seals_synthetic_high_water_mark_with_private_output(case):
    result, output = run(case)
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    sealed = json.loads(output.read_text())
    assert result.stdout.splitlines() == [
        hashlib.sha256(output.read_bytes()).hexdigest(),
        "C1 C2 C3 C4 C5 C6 C7 C8 C9 C10",
        "2026-09-14T18:00:00-04:00",
        "Attested by evidence; not machine-verified against the broker.",
    ]
    assert sealed["derived"]["at_high_water_mark"] is True
    values = case[1]["values"]
    peak = Fraction(values["trailing_threshold"]) + Fraction(100000) * Fraction(3, 100)
    ratio = Fraction(values["prior_max_day_profit"], values["balance"] - 100000) * 100
    assert sealed["derived"]["historical_eod_peak"] == peak
    assert values["consistency_display_pct"] == ratio
    assert sealed["derived"]["valid_until"] == result.stdout.splitlines()[2]
    assert set(sealed["checks"]) == {f"C{i}" for i in range(1, 11)}
    for role, path in case[2].items():
        assert sealed["evidence"][role]["sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()


def test_carried_drawdown(case):
    case[1]["values"].update(balance=101000, equity=101000, consistency_display_pct=60)
    result, output = run(case)
    assert result.returncode == 0, result.stderr
    derived = json.loads(output.read_text())["derived"]
    assert derived["carried_drawdown"] == 1000
    assert derived["at_high_water_mark"] is False


@pytest.mark.parametrize("variant", [
    "values", "captured_at", "balance", "capture", "escaped_balance", "identical_balance",
])
@pytest.mark.parametrize("existing_output", [False, True])
def test_duplicate_manifest_keys_refuse_without_writing_or_leaking(case, variant, existing_output):
    raw = json.dumps(case[1])
    replacements = {
        "values": ('"values":', '"values": "SYNTHETIC_PRIVATE_TEXT", "values":'),
        "captured_at": ('"captured_at":', '"captured_at": "SYNTHETIC_PRIVATE_TEXT", "captured_at":'),
        "balance": ('"balance":', '"balance": 0, "balance":'),
        "capture": ('"E1":', '"E1": "2099-01-01T00:00:00Z", "E1":'),
        "escaped_balance": ('"balance":', '"\\u0062alance": 0, "balance":'),
        "identical_balance": ('"balance":', '"balance": 102000, "balance":'),
    }
    target, replacement = replacements[variant]
    assert raw.count(target) == 1
    raw = raw.replace(target, replacement, 1)
    # Every payload would otherwise pass under last-key-wins parsing.
    assert json.loads(raw) == case[1]
    output = case[0] / 'private/seal.json'
    previous = b'SYNTHETIC EXISTING SEAL'
    if existing_output:
        output.parent.mkdir()
        output.write_bytes(previous)
    evidence_before = {role: path.read_bytes() for role, path in case[2].items()}
    result, _ = run(case, raw_manifest=raw)
    assert result.returncode == 2
    assert result.stdout == ''
    assert result.stderr == 'C2\n'
    assert output.read_bytes() == previous if existing_output else not output.exists()
    assert {role: path.read_bytes() for role, path in case[2].items()} == evidence_before
    assert (case[0] / 'manifest.json').read_text(encoding='utf-8') == raw


@pytest.mark.parametrize("variant", ["missing", "empty", "alias", "identical"])
def test_c1_distinct_nonempty_evidence(case, variant):
    if variant == "missing":
        case[2]["E3"].unlink()
    elif variant == "empty":
        case[2]["E3"].write_bytes(b"")
    elif variant == "alias":
        case[2]["E3"] = case[2]["E1"].parent / "." / "E1.txt"
    else:
        case[2]["E3"].write_bytes(case[2]["E1"].read_bytes())
    refuses(case, "C1")


@pytest.mark.parametrize("change", [
    {"trailing_threshold": 96000, "balance": 98000, "equity": 98000},
    {"prior_trade_days": 0},
    {"balance": 99000, "equity": 99000},
    {"balance": 98999, "equity": 98999},
    {"balance": 99000.01, "equity": 99000.01},
    {"prior_trade_days": True}, {"equity": float("nan")},
])
def test_c2_kernel_and_rounded_floor(case, change):
    case[1]["values"].update(change)
    refuses(case, "C2")


def test_c2_safely_above_floor(case):
    case[1]["values"].update(balance=99000.10, equity=99000.10)
    result, _ = run(case)
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("change", [
    {"balance": 101999}, {"positions_export_shows_flat": False},
    {"positions_export_shows_flat": 1}, {"working_orders_count": 1},
    {"working_orders_count": False},
])
def test_c3_flat_and_no_orders(case, change):
    case[1]["values"].update(change)
    refuses(case, "C3")


def test_c4_peak_below_balance(case):
    # Equity remains constructor-valid; C3 also fails, but C4 is evaluated first.
    case[1]["values"]["balance"] = 102001
    refuses(case, "C4")


@pytest.mark.parametrize("capture,seal,check", [
    ("2026-09-14T17:41:00-04:00", "2026-09-14T17:50:00-04:00", "C5"),
    ("2026-09-14T17:21:00-04:00", "2026-09-14T17:20:00-04:00", "C5"),
    ("2026-09-14T14:00:00-04:00", "2026-09-14T17:20:00-04:00", "C5"),
    ("2026-09-14T17:10:00", "2026-09-14T17:20:00-04:00", "C5"),
    ("0001-01-01T00:00:00+14:00", "2026-09-14T17:20:00-04:00", "C5"),
    ("0001-01-01T00:00:00Z", "2026-09-14T17:20:00-04:00", "C5"),
    ("2026-09-14T17:10:00-04:00", "2026-09-14T18:00:00-04:00", "C10"),
    ("2026-09-14T17:10:00-04:00", "2026-09-14T18:01:00-04:00", "C10"),
])
def test_c5_c10_boundary_and_capture_order(case, capture, seal, check):
    case[1]["captured_at"]["E3"] = capture
    refuses(case, check, seal=seal)


def test_c5_seal_more_than_24h_late_in_weekend_boundary(case):
    case[1]["captured_at"] = dict.fromkeys(case[2], "2026-09-11T17:10:00-04:00")
    refuses(case, "C5", seal="2026-09-12T18:11:00-04:00")


@pytest.mark.parametrize("capture,seal,expiry", [
    ("2026-03-07T17:10:00-05:00", "2026-03-08T17:00:00-04:00", "2026-03-08T18:00:00-04:00"),
    ("2026-10-31T17:10:00-04:00", "2026-11-01T16:00:00-05:00", "2026-11-01T18:00:00-05:00"),
])
def test_weekend_and_dst(case, capture, seal, expiry):
    case[1]["captured_at"] = dict.fromkeys(case[2], capture)
    result, output = run(case, seal=seal)
    assert result.returncode == 0, result.stderr
    assert json.loads(output.read_text())["derived"]["valid_until"] == expiry


@pytest.mark.parametrize("field,value,check", [
    ("consistency_display_pct", 28, "C6"),
    ("profit_target_display", 6001, "C7"),
    ("cash_adjustments_total", 200, "C8"),
    ("cash_adjustments_total", -1, "C8"),
    ("cash_adjustments_total", False, "C8"),
    ("token_trade_fill_dates", ["invalid"], "C2"),
])
def test_display_adjustments_and_fields(case, field, value, check):
    case[1]["values"][field] = value
    refuses(case, check)


def test_capped_consistency_display(case):
    case[1]["values"].update(balance=100500, equity=100500, consistency_display_pct=100)
    result, _ = run(case)
    assert result.returncode == 0, result.stderr


def test_c9_output_must_be_ignored(case):
    refuses(case, "C9", output="public.json")


def test_c9_ignore_policy_comes_from_sealer_repo_not_caller(case, tmp_path):
    caller = tmp_path.parent / (tmp_path.name + "-caller")
    caller.mkdir()
    subprocess.run(["git", "init", "-q", str(caller)], check=True)
    (caller / ".gitignore").write_text("*\n", encoding="utf-8")
    result, output = run(case, cwd=caller)
    assert result.returncode == 0, result.stderr
    assert output.exists()
    refuses(case, "C9", output=caller / "not-private.json", cwd=caller)


def test_c9_output_cannot_replace_evidence(case):
    original = case[2]["E1"].read_bytes()
    result, _ = run(case, output="E1.txt")
    assert result.returncode == 2 and result.stderr.strip() == "C9"
    assert not result.stdout
    assert case[2]["E1"].read_bytes() == original


def test_missing_field_is_not_defaulted(case):
    del case[1]["values"]["working_orders_count"]
    refuses(case, "C3")


@pytest.mark.parametrize("extra,check", [
    (("--freshness-minutes", "SYNTHETIC_PRIVATE_TEXT"), "C5"),
    (("--freshness-minutes", "31"), "C5"),
    (("--seal-hours", "25"), "C5"),
    (("--seal-hours", "nan"), "C5"),
    (("--seal-time", "2026-09-14T17:20:00-04:00"), "C2"),
])
def test_cli_cannot_relax_freshness_or_leak_input(case, extra, check):
    refuses(case, check, extra=extra)
