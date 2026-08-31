"""Chronological-halves L3 presence limb for Q-VOLREGIME-1.

The split is the observation midpoint after the frozen scored-frame exclusions.
Each half passes only when volume-conditioned next-bar-range lift is strictly
positive in both own-range strata. Vendor bytes are verified by ``prepare``
before any result is calculated.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
L4_SCRIPT = (
    REPO
    / "lab"
    / "analysis"
    / "_inbox"
    / "volregime_byyear_l4_2026-08-31"
    / "byyear_l4.py"
)


def _load_l4_module():
    spec = importlib.util.spec_from_file_location("volregime_byyear_l4", L4_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load scored-frame builder: {L4_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _iso(value: object) -> str:
    return pd.Timestamp(value).isoformat()


def score_half(frame: pd.DataFrame) -> dict:
    """Score one already-ordered chronological half."""
    strata: dict[str, dict] = {}
    for stratum in (0, 1):
        selected = frame.loc[frame["bias_range"] == stratum]
        cond = selected.loc[selected["bias_volume"] == 1, "outcome"]
        ref = selected.loc[selected["bias_volume"] == 0, "outcome"]
        lift = float(cond.mean() - ref.mean()) if len(cond) and len(ref) else None
        strata[str(stratum)] = {
            "n_cond": int(len(cond)),
            "n_ref": int(len(ref)),
            "rate_cond": float(cond.mean()) if len(cond) else None,
            "rate_ref": float(ref.mean()) if len(ref) else None,
            "lift": lift,
        }

    lifts = [strata[str(stratum)]["lift"] for stratum in (0, 1)]
    minimum = min(lifts) if all(value is not None for value in lifts) else None
    return {
        "n_scored": int(len(frame)),
        "span_utc": [_iso(frame["time_utc"].iloc[0]), _iso(frame["time_utc"].iloc[-1])],
        "strata": strata,
        "minimum_stratum_lift": minimum,
        "passes": bool(minimum is not None and minimum > 0),
    }


def score_l3(frame: pd.DataFrame) -> dict:
    """Apply the frozen midpoint split and both-halves-positive rule."""
    required = {"time_utc", "bias_volume", "bias_range", "outcome"}
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"missing required columns: {', '.join(missing)}")
    if len(frame) < 2:
        raise ValueError("at least two scored rows are required")

    ordered = frame.sort_values("time_utc", kind="stable").reset_index(drop=True)
    midpoint = len(ordered) // 2
    first = ordered.iloc[:midpoint].copy()
    second = ordered.iloc[midpoint:].copy()
    halves = {"first": score_half(first), "second": score_half(second)}
    return {
        "split_rule": "observation midpoint after frozen scored-frame exclusions",
        "split_index_zero_based_second_half_start": midpoint,
        "split_boundary_utc": _iso(second["time_utc"].iloc[0]),
        "halves": halves,
        "l3": {
            "verdict": "PASS" if all(half["passes"] for half in halves.values()) else "FAIL",
            "rule": "minimum within-own-range-stratum lift > 0 in both chronological halves",
        },
    }


def main() -> None:
    l4 = _load_l4_module()
    results = {
        "method": "Q-VOLREGIME-1 L3 chronological-halves presence limb",
        "script_sha256": file_sha256(Path(__file__)),
        "instruments": {},
    }
    for symbol in ("MNQ", "MYM"):
        frame, metadata = l4.prepare(symbol)
        result = {"input": metadata, **score_l3(frame)}
        results["instruments"][symbol] = result
        print(
            f"{symbol}: split={result['split_boundary_utc']} "
            f"first_min={result['halves']['first']['minimum_stratum_lift']:+.6f} "
            f"second_min={result['halves']['second']['minimum_stratum_lift']:+.6f} "
            f"L3={result['l3']['verdict']}"
        )

    output = HERE / "l3_results.json"
    output.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
