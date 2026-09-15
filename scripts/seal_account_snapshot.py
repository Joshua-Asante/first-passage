#!/usr/bin/env python3
"""Offline TB-T1 evidence attestation. Does not read a broker or authorize risk.

Input JSON has ``values`` (the contract's typed fields) and ``captured_at``
(E1/E2/E3 offset-bearing timestamps). Evidence paths are separate CLI arguments.
The caller authenticates the operator and later binds account/session identity;
this tool does not turn an evidence attestation into an authenticated live close.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "core"))

from firm_rules import FIRM_RULES  # noqa: E402
from lib.validation import dump_strict_json, require_finite_number  # noqa: E402
from mc.preflight import firm_kwargs  # noqa: E402
from mc.simulation import EvaluationState, _drawdown_outcome  # noqa: E402

FRESHNESS_WINDOW_MINUTES = 30
SEAL_WITHIN_HOURS = 24
CONTRACT = "docs/spec/2026-09-12-tradeify-account-snapshot-seal-contract.md"
ATTESTATION = "Attested by evidence; not machine-verified against the broker."
CHECKS = tuple(f"C{i}" for i in range(1, 11))
ET = ZoneInfo("America/New_York")
UTC = timezone.utc


class Refusal(ValueError):
    """Only a public check ID is safe to print."""


def require(condition, check):
    if not condition:
        raise Refusal(check)


def number(values, name, check, *, positive=False, minimum=None):
    try:
        return require_finite_number(values[name], field=name,
                                     strictly_positive=positive, minimum=minimum)
    except (KeyError, TypeError, ValueError, OverflowError) as exc:
        raise Refusal(check) from exc


def timestamp(value, check):
    try:
        parsed = datetime.fromisoformat(value)
        require(parsed.tzinfo is not None and parsed.utcoffset() is not None, check)
        return parsed.astimezone(UTC)
    except (TypeError, ValueError, OverflowError) as exc:
        raise Refusal(check) from exc


def utc_now():
    """Actual sealing time. Tests inject a clock; the CLI cannot backdate seals."""
    return datetime.now(UTC)


def boundary(at):
    """The contract's weekday/weekend window; no holiday-hours inference."""
    local = at.astimezone(ET)
    day = local.date()
    weekday = day.weekday()
    if weekday >= 5:
        friday = day - timedelta(days=weekday - 4)
        return (datetime.combine(friday, time(17), ET),
                datetime.combine(friday + timedelta(days=2), time(18), ET))
    require(local.hour >= 17, "C5")
    reopen = day + timedelta(days=2) if weekday == 4 else day
    return datetime.combine(day, time(17), ET), datetime.combine(reopen, time(18), ET)


def evidence_records(paths, captures):
    records = {}
    try:
        canonical = {role: path.resolve(strict=True) for role, path in paths.items()}
        require(len(set(canonical.values())) == 3, "C1")
        for role, path in canonical.items():
            content = path.read_bytes()
            require(bool(content), "C1")
            records[role] = {"path": path.name, "sha256": hashlib.sha256(content).hexdigest(),
                             "captured_at": captures[role]}
        require(len({record["sha256"] for record in records.values()}) == 3, "C1")
    except (OSError, KeyError, TypeError) as exc:
        raise Refusal("C1") from exc
    return records, canonical


def validate_values(values):
    require(isinstance(values, dict), "C2")
    rules = FIRM_RULES["Tradeify_Select_100K"]
    basis = rules["starting_balance"]
    width = basis * rules["max_dd_pct"] / 100
    equity = number(values, "equity", "C2", positive=True)
    balance = number(values, "balance", "C3", positive=True)
    threshold = number(values, "trailing_threshold", "C2")
    peak = threshold + width
    require(peak >= balance, "C4")
    best = number(values, "prior_max_day_profit", "C2", minimum=0)
    try:
        days = values["prior_trade_days"]
        require(type(days) is int and days >= 0, "C2")
        EvaluationState(basis, equity, peak, days, best)
        geometry = firm_kwargs("Tradeify_Select_100K")
        require(_drawdown_outcome(equity, peak, **{
            key: geometry.get(key) for key in ("starting_equity", "dd_type", "static_dd_pct",
                                              "trailing_dd_pct", "dd_lock_offset_usd")
        }) is None, "C2")
        dates = values["token_trade_fill_dates"]
        require(isinstance(dates, list), "C2")
        for item in dates:
            require(isinstance(item, str) and date.fromisoformat(item).isoformat() == item, "C2")
    except (KeyError, TypeError, ValueError, OverflowError) as exc:
        raise Refusal("C2") from exc
    require(equity == balance and values.get("positions_export_shows_flat") is True
            and type(values.get("working_orders_count")) is int
            and values["working_orders_count"] == 0, "C3")
    display = number(values, "consistency_display_pct", "C6", minimum=0)
    require(display <= 100, "C6")
    if balance > basis:
        ratio_pct = best / (balance - basis) * 100
        require(abs(min(ratio_pct, 100) - display) <= 1, "C6")
    require(number(values, "profit_target_display", "C7") ==
            basis * rules["profit_target_pct"] / 100, "C7")
    require(number(values, "cash_adjustments_total", "C8", minimum=0) == 0, "C8")
    return {"original_basis": basis, "historical_eod_peak": peak,
            "at_high_water_mark": peak == balance, "carried_drawdown": peak - balance}


def validate_times(captures, sealed_at, freshness_minutes, seal_hours):
    require(0 < freshness_minutes <= FRESHNESS_WINDOW_MINUTES and
            0 < seal_hours <= SEAL_WITHIN_HOURS, "C5")
    try:
        times = [timestamp(captures[role], "C5") for role in ("E1", "E2", "E3")]
    except (KeyError, TypeError) as exc:
        raise Refusal("C5") from exc
    require(max(times) <= sealed_at, "C5")
    try:
        start, end = boundary(min(times))
    except (OverflowError, ValueError) as exc:
        raise Refusal("C5") from exc
    require(sealed_at < end, "C10")
    require(all(start <= at < end for at in times) and start <= sealed_at, "C5")
    require(max(times) - min(times) <= timedelta(minutes=freshness_minutes), "C5")
    require(sealed_at - max(times) <= timedelta(hours=seal_hours), "C5")
    return end.isoformat()


def write_private(output, canonical_evidence, document, manifest_path):
    try:
        target = output.resolve()
        # Also protect the input manifest, though it is not one of E1/E2/E3.
        require(target not in {*canonical_evidence.values(), manifest_path.resolve()}, "C9")
        if target.exists():
            require(not any(os.path.samefile(target, path)
                            for path in canonical_evidence.values()), "C9")
        ignored = subprocess.run(["git", "check-ignore", "-q", "--", str(target)],
                                 cwd=REPO_ROOT, capture_output=True, check=False)
        require(ignored.returncode == 0, "C9")
        payload = (dump_strict_json(document) + "\n").encode("utf-8")
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(dir=target.parent, prefix=".seal-", delete=False) as file:
                temporary = Path(file.name)
                file.write(payload)
                file.flush()
                os.fsync(file.fileno())
            os.replace(temporary, target)
        finally:
            if temporary is not None and temporary.exists():
                temporary.unlink()
        return hashlib.sha256(payload).hexdigest()
    except (OSError, TypeError, ValueError) as exc:
        raise Refusal("C9") from exc


def seal(args):
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "C2")
            result[key] = value
        return result

    try:
        # Numeric NaN/Infinity are rejected by the owning check rather than echoed.
        # Reject ambiguous keys in every object, including decoded escape aliases.
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"),
                              object_pairs_hook=unique_object)
        require(isinstance(manifest, dict), "C2")
        values, captures = manifest["values"], manifest["captured_at"]
    except (OSError, KeyError, TypeError, ValueError) as exc:
        raise Refusal("C2") from exc
    records, canonical = evidence_records({"E1": args.e1, "E2": args.e2, "E3": args.e3}, captures)
    derived = validate_values(values)
    sealed_at = timestamp(utc_now().isoformat(), "C5")
    derived["valid_until"] = validate_times(captures, sealed_at, args.freshness_minutes, args.seal_hours)
    document = {"values": values, "derived": derived, "evidence": records,
                "checks": dict.fromkeys(CHECKS, "pass"), "seal_timestamp": sealed_at.isoformat(),
                "tool_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "contract": CONTRACT}
    digest = write_private(args.output, canonical, document, args.manifest)
    return digest, derived["valid_until"]


def main(argv=None):
    class PrivateParser(argparse.ArgumentParser):
        def error(self, message):
            self.exit(2, "C2\n")

    parser = PrivateParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    for role in ("e1", "e2", "e3"):
        parser.add_argument(f"--{role}", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path(
        "lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts/account_snapshots/seal.json"))
    parser.add_argument("--freshness-minutes", default=FRESHNESS_WINDOW_MINUTES)
    parser.add_argument("--seal-hours", default=SEAL_WITHIN_HOURS)
    args = parser.parse_args(argv)
    try:
        try:
            args.freshness_minutes = float(args.freshness_minutes)
            args.seal_hours = float(args.seal_hours)
        except (ValueError, TypeError, OverflowError) as exc:
            raise Refusal("C5") from exc
        digest, valid_until = seal(args)
    except Refusal as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(digest)
    print(" ".join(CHECKS))
    print(valid_until)
    print(ATTESTATION)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
