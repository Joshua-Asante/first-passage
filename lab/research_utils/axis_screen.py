#!/usr/bin/env python3
"""axis_screen.py — manifest-driven two-clause intake screen (harvest-intake ADR).

Promotes the Q-KBUDGET-1 campaign-local floor scan to standing infrastructure:
new harvested seeds screen by adding a JSON row, never by editing screen code.

Frozen constants (no CLI/env override — harvest-intake ADR §5):
  Cap 1.0 / DSR ≥ 0.95 / power ≥ 0.50 / z = 1.96
  Source: docs/briefs/pre-registration/Q-KBUDGET-1-screen-preregistration.md §B
  (freeze b304f2c); Cap resolved by Q-GATECART-1 2026-07-14.

Arithmetic ported from lab/analysis/q_kbudget_1_2026-07/floor_scan.py +
d5_power.py / d7_power.py (erf-CDF Clause N). Stdlib + deflated_sharpe only.

Usage:
  PYTHONPATH=lab python -m research_utils.axis_screen <manifest.json> [--out results.json]
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

from research_utils.deflated_sharpe import deflated_sharpe, expected_max_sharpe

# Frozen screen constants — citation: Q-KBUDGET-1-screen-preregistration.md §B
# (freeze b304f2c). Do NOT add CLI/env overrides (harvest-intake ADR §5).
CAP = 1.0
DSR_MIN = 0.95
POWER_MIN = 0.50
Z = 1.96
YEARS = 6.5
FREQS = (0.5, 1.0, 2.0, 4.0)

_REQUIRED_KEYS = frozenset({
    "axis", "family", "k_banked", "k_intrinsic",
    "n_events", "delta_over_sigma", "delta_citation", "unscreenable_reason",
})
_OPTIONAL_KEYS = frozenset({"clause_n_inherited"})
_ALLOWED_KEYS = _REQUIRED_KEYS | _OPTIONAL_KEYS


def floor_at_k(
    k: int,
    years: float = YEARS,
    freqs=FREQS,
    t: float = DSR_MIN,
) -> float:
    """Min annualized Sharpe clearing DSR ≥ t at (K, V=1/n), most-permissive f.

    Ported verbatim from lab/analysis/q_kbudget_1_2026-07/floor_scan.py.
    """
    best = None
    for f in freqs:
        n = int(round(252 * f * years))
        sr0 = expected_max_sharpe(k, 1.0 / n)
        s = 0.01
        while s < 6.0:
            if deflated_sharpe(s / math.sqrt(252 * f), n, 0.0, 3.0, sr0) >= t:
                break
            s += 0.005
        best = s if best is None else min(best, s)
    return round(best, 3)


def clause_n_power(
    n_events: int,
    delta_over_sigma: float,
    z: float = Z,
) -> float:
    """Confirm-gate power: Φ(√N · |δ|/σ − z). erf-CDF, same as d5/d7_power.py."""
    x = math.sqrt(n_events) * abs(delta_over_sigma) - z
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _validate_row(row: dict[str, Any], index: int) -> None:
    unknown = set(row) - _ALLOWED_KEYS
    if unknown:
        raise ValueError(f"row[{index}]: unknown keys {sorted(unknown)}")
    missing = _REQUIRED_KEYS - set(row)
    if missing:
        raise ValueError(f"row[{index}]: missing keys {sorted(missing)}")

    if not isinstance(row["axis"], str) or not row["axis"]:
        raise ValueError(f"row[{index}]: axis must be a non-empty string")
    if not isinstance(row["family"], str) or not row["family"]:
        raise ValueError(f"row[{index}]: family must be a non-empty string")
    if not isinstance(row["k_banked"], int) or isinstance(row["k_banked"], bool):
        raise ValueError(f"row[{index}]: k_banked must be an int")
    ki = row["k_intrinsic"]
    if (
        not isinstance(ki, list)
        or len(ki) != 2
        or not all(isinstance(x, int) and not isinstance(x, bool) for x in ki)
        or ki[0] > ki[1]
    ):
        raise ValueError(
            f"row[{index}]: k_intrinsic must be [lo, hi] ints with lo <= hi"
        )

    n_events = row["n_events"]
    delta = row["delta_over_sigma"]
    reason = row["unscreenable_reason"]
    citation = row["delta_citation"]

    if n_events is not None and (
        not isinstance(n_events, int) or isinstance(n_events, bool) or n_events <= 0
    ):
        raise ValueError(f"row[{index}]: n_events must be a positive int or null")
    if delta is not None and not isinstance(delta, (int, float)):
        raise ValueError(f"row[{index}]: delta_over_sigma must be a number or null")
    if citation is not None and not isinstance(citation, str):
        raise ValueError(f"row[{index}]: delta_citation must be a string or null")
    if reason is not None and not isinstance(reason, str):
        raise ValueError(f"row[{index}]: unscreenable_reason must be a string or null")

    if n_events is None or delta is None:
        if not reason:
            raise ValueError(
                f"row[{index}]: unscreenable_reason is mandatory when "
                "n_events or delta_over_sigma is null"
            )

    inherited = row.get("clause_n_inherited")
    if inherited is not None:
        if not isinstance(inherited, dict):
            raise ValueError(f"row[{index}]: clause_n_inherited must be an object")
        if inherited.get("verdict") != "FAIL":
            raise ValueError(
                f"row[{index}]: clause_n_inherited.verdict must be 'FAIL'"
            )
        if not isinstance(inherited.get("citation"), str) or not inherited["citation"]:
            raise ValueError(
                f"row[{index}]: clause_n_inherited.citation must be a non-empty string"
            )


def load_manifest(path: str | Path) -> list[dict[str, Any]]:
    """Load + schema-validate a JSON array of seed rows."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("manifest must be a JSON array of seed rows")
    for i, row in enumerate(raw):
        if not isinstance(row, dict):
            raise ValueError(f"row[{i}]: must be an object")
        _validate_row(row, i)
    return raw


def screen_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Screen each row: Clause K then Clause N. Best (lowest-K) end gates Clause K.

    Verdict vocabulary matches floor_scan.py:
      PASS / FAIL (Clause K) / FAIL (Clause N) / FAIL (Clause N, inherited) / UNSCREENABLE
    """
    out: list[dict[str, Any]] = []
    for a in rows:
        lo, hi = a["k_intrinsic"]
        # ADR 2026-08-04 (Accepted): K_eff counts WITHIN-SEARCH selection only.
        # `k_banked` is retained as a REQUIRED key and reported in every row/table
        # (mandatory disclosure), but is deliberately NOT summed into k_eff -- the
        # DSR correction prices E[max of K trials], which a pre-registered single
        # hypothesis never takes. A grid still pays in full: every axis a design
        # varies belongs in k_intrinsic. Do not "restore" the sum without
        # superseding that ADR.
        k_lo, k_hi = lo, hi
        f_lo, f_hi = floor_at_k(k_lo), floor_at_k(k_hi)
        clause_k = "PASS" if f_lo <= CAP else "FAIL"

        power = None
        clause_n_note = None

        if clause_k == "FAIL":
            verdict = "FAIL (Clause K)"
            clause_n_note = "n/a — Clause K kills first"
        elif a.get("clause_n_inherited") is not None:
            verdict = "FAIL (Clause N, inherited)"
            clause_n_note = a["clause_n_inherited"]["citation"]
        elif a["n_events"] is None or a["delta_over_sigma"] is None:
            verdict = "UNSCREENABLE"
            clause_n_note = a["unscreenable_reason"]
        else:
            power = clause_n_power(a["n_events"], float(a["delta_over_sigma"]))
            if power >= POWER_MIN:
                verdict = "PASS"
                clause_n_note = (
                    f"PASS: power={power:.3f} at N={a['n_events']}, "
                    f"delta/sigma={a['delta_over_sigma']}"
                    + (f" ({a['delta_citation']})" if a.get("delta_citation") else "")
                )
            else:
                verdict = "FAIL (Clause N)"
                clause_n_note = (
                    f"FAIL (N): power={power:.3f} < {POWER_MIN} at N={a['n_events']}, "
                    f"delta/sigma={a['delta_over_sigma']}"
                    + (f" ({a['delta_citation']})" if a.get("delta_citation") else "")
                )

        out.append({
            "axis": a["axis"],
            "family": a["family"],
            "k_banked": a["k_banked"],
            "k_intrinsic": list(a["k_intrinsic"]),
            "k_eff": [k_lo, k_hi],
            "floor": [f_lo, f_hi],
            "clause_k": clause_k,
            "clause_n": clause_n_note,
            "power": power,
            "verdict": verdict,
        })
    return out


def aggregate_verdict(screened: list[dict[str, Any]]) -> str:
    """pre-reg §D aggregate line."""
    unscreenable = [r for r in screened if r["verdict"] == "UNSCREENABLE"]
    scored = [r for r in screened if r["verdict"] != "UNSCREENABLE"]
    passing = [r for r in screened if r["verdict"] == "PASS"]
    if not passing and unscreenable:
        return (
            "AMBIGUOUS-HOLD (all screened fail; >=1 verdict-relevant UNSCREENABLE)"
        )
    if not passing:
        return "FALSIFIED (fundable set empty; zero UNSCREENABLE)"
    return "RESOLVED (fundable set non-empty)"


def format_table(screened: list[dict[str, Any]]) -> str:
    # K_banked is a MANDATORY DISCLOSURE (ADR 2026-08-04): it no longer gates, so it
    # must stay visible in the human-readable output or it decays to ceremony -- that
    # decay is the ADR's own section-4 trigger 2.
    lines = [
        f"| Axis | Family | K_banked (disclosure) | K_eff | floor(K_eff) | "
        f"Clause K (Cap {CAP}) | Clause N | Screen |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in screened:
        k_lo, k_hi = r["k_eff"]
        f_lo, f_hi = r["floor"]
        k = f"{k_lo}" if k_lo == k_hi else f"{k_lo}-{k_hi}"
        fl = f"{f_lo}" if f_lo == f_hi else f"{f_lo}-{f_hi}"
        lines.append(
            f"| {r['axis']} | {r['family']} | {r['k_banked']} | {k} | {fl} | "
            f"{r['clause_k']} | {r['clause_n']} | **{r['verdict']}** |"
        )
    scored = [r for r in screened if r["verdict"] != "UNSCREENABLE"]
    unscreenable = [r for r in screened if r["verdict"] == "UNSCREENABLE"]
    passing = [r for r in screened if r["verdict"] == "PASS"]
    lines.append("")
    lines.append(
        f"Screened FAIL: {len(scored) - len(passing)}/{len(scored)} · "
        f"PASS: {len(passing)} · UNSCREENABLE: {len(unscreenable)}"
    )
    lines.append(f"Verdict per pre-reg §D: {aggregate_verdict(screened)}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Manifest-driven two-clause intake screen (harvest-intake ADR)."
    )
    ap.add_argument("manifest", help="JSON array of seed rows")
    ap.add_argument("--out", help="Write results JSON to this path")
    args = ap.parse_args(argv)

    rows = load_manifest(args.manifest)
    screened = screen_rows(rows)
    print(format_table(screened))

    if args.out:
        payload = {
            "cap": CAP,
            "dsr_min": DSR_MIN,
            "power_min": POWER_MIN,
            "z": Z,
            "verdict": aggregate_verdict(screened),
            "rows": screened,
        }
        Path(args.out).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
