#!/usr/bin/env python3
"""
breadth.py — incremental-breadth 5th-column N_eff (discovery-campaign Stage 8).

Given the locked 4-strategy weekly panel (the SAME joint Mon-anchored week-block
frame core/mc/ingest.py builds for the production MC), computes N_eff via the
participation ratio of eigenvalues:

    PR(M) = (sum(eigvals))**2 / sum(eigvals**2)

applied to the weekly correlation matrix (dependence breadth) and the weekly
covariance matrix (risk-weighted breadth). Optionally injects a candidate's
daily return series as a 5th column and reports the correlation/N_eff delta
vs the 4-leg baseline (discovery-campaign-template.md Stage 8).

Zero core/mc engine change — build_daily_panel/build_week_blocks are imported
unmodified. Sanity anchor: on the 4 legs alone (no candidate), this must
reproduce Q-NEFF-1's N_eff ~= 3.98 (dependence) / ~= 3.09 (risk) — see
docs/briefs/Q-NEFF-1-closure-resolved-benign.md. Run `--self-test` to check.

Candidate input contract (Stage-4 ratified shape): a CSV with a timestamp
index, one column per candidate, and a `benchmark` column (excluded from
breadth injection — context only). Each non-benchmark column is evaluated
independently: Stage 8 asks what ONE survivor does to the book, not what
all open candidates would do simultaneously.

Design: docs/superpowers/specs/2026-07-12-track-c-incremental-breadth-design.md
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from research_utils.repo_root import repo_root

_CORE = repo_root() / "core"
if str(_CORE) not in sys.path:
    sys.path.insert(0, str(_CORE))

from mc.ingest import build_daily_panel, build_week_blocks, load_trades  # noqa: E402
from mc.modes import (  # noqa: E402
    ALLOCATIONS,
    EXPECTED_SYMBOLS_BY_BROKER,
    EXPECTED_VERSIONS_BY_BROKER,
    PANELS_BY_BROKER,
    STRATEGY_FILENAME_TOKEN,
)
from lib.mvd import assert_tv_export  # noqa: E402

# Q-NEFF-1 anchor (docs/briefs/Q-NEFF-1-closure-resolved-benign.md), reproduced
# against the real Pepperstone panel in the design doc §3. Historical 4-leg
# CFD/Pepperstone record -- retired feed, not comparable to any other panel.
NEFF_DEPENDENCE_ANCHOR = 3.98
NEFF_RISK_ANCHOR = 3.09
ANCHOR_TOLERANCE = 0.02
EXPECTED_N_BDAYS = 1141
EXPECTED_N_BLOCKS = 227

# "cme" 2-leg anchor (ADR 2026-08-19-cme-broker-panel-admission-for-breadth-revival),
# first measured 2026-08-19 against Striker DJ30/MYM (2026-07-11_15d8b.csv) +
# Striker NAS100/MNQ (2026-08-19_3ad92.csv) -- this run's own output IS the anchor
# being established, not an independently-verified target, same epistemic status
# Q-NEFF-1's own anchor had at first measurement.
CME_NEFF_DEPENDENCE_ANCHOR = 1.9988
CME_NEFF_RISK_ANCHOR = 1.0871
CME_EXPECTED_N_BDAYS = 1711
CME_EXPECTED_N_BLOCKS = 341

MIN_OVERLAP_BLOCKS = 30  # ~7 months; below this, thin_overlap fires (design §6)
# --self-test exits: 0 PASS / 1 FAIL (universe_gate, temporal_consistency);
# 2 SKIP when the vendor panel is absent (pine_lint missing-fixture convention).
SELF_TEST_SKIP = 2


def participation_ratio(matrix: np.ndarray) -> float:
    """Effective number of independent components: (sum(eigvals))^2 / sum(eigvals^2).

    Scale-invariant (PR(cM) == PR(M) for any positive scalar c), so this is
    unaffected by np.cov's ddof convention. docs/briefs/Q-NEFF-1-closure-
    resolved-benign.md calls this "participation ratio of eigenvalues" — the
    canonical N_eff figure (headline over the ENB corroboration below).
    """
    eigvals = np.clip(np.linalg.eigvalsh(matrix), 0, None)
    return float(eigvals.sum() ** 2 / (eigvals ** 2).sum())


def effective_number_of_bets(matrix: np.ndarray) -> float:
    """Entropy-based effective-number-of-bets: a corroborating cross-check for
    participation_ratio, not the gated metric (Q-NEFF-1 headlines PR)."""
    eigvals = np.clip(np.linalg.eigvalsh(matrix), 1e-12, None)
    p = eigvals / eigvals.sum()
    entropy = -np.sum(p * np.log(p))
    return float(np.exp(entropy))


def baseline_panel_available(panel_name: str = "pepperstone") -> bool:
    """True iff panel_name is registered and every canonical CSV exists locally."""
    try:
        panels = PANELS_BY_BROKER[panel_name]
    except KeyError:
        return False
    if not panels:
        return False
    return all(p.exists() for p in panels.values())


def load_baseline_panel(panel_name: str = "pepperstone") -> pd.DataFrame:
    """Load + risk-normalize the canonical 4-leg daily panel (MVD identity-gated,
    same rigor as core/mc/modes.py's private _load_all)."""
    if panel_name not in PANELS_BY_BROKER:
        raise KeyError(
            f"panel {panel_name!r} is not registered in PANELS_BY_BROKER "
            f"(substrate Phase 3 retired the Pepperstone executable anchor; "
            f"registry is empty until a panel is admitted via ADR)"
        )
    panels = PANELS_BY_BROKER[panel_name]
    if not panels:
        raise ValueError(
            f"panel {panel_name!r} has no registered CSV paths "
            f"(PANELS_BY_BROKER[{panel_name!r}] is empty)"
        )
    expected_symbols = EXPECTED_SYMBOLS_BY_BROKER[panel_name]
    expected_versions = EXPECTED_VERSIONS_BY_BROKER[panel_name]
    trades_by_strat = {}
    for strategy, path in panels.items():
        if panel_name == "cme":
            # CME TV-exports don't follow OANDA/Pepperstone's strict 7-field
            # pattern -- see _assert_cme_export's own docstring for why.
            _assert_cme_export(
                path,
                expected_strategy_token=STRATEGY_FILENAME_TOKEN[strategy],
                expected_symbol=expected_symbols[strategy],
            )
        else:
            assert_tv_export(
                path,
                expected_strategy=STRATEGY_FILENAME_TOKEN[strategy],
                expected_version=expected_versions[strategy],
                expected_broker=panel_name.upper(),
                expected_symbol=expected_symbols[strategy],
            )
        trades_by_strat[strategy] = load_trades(path, strategy=strategy)
    panel, _scale_info = build_daily_panel(trades_by_strat, ALLOCATIONS)
    return panel


def _assert_cme_export(csv_path, *, expected_strategy_token: str, expected_symbol: str) -> None:
    """Lighter identity check for CME TV-exports (2026-08-19, ADR
    2026-08-19-cme-broker-panel-admission-for-breadth-revival).

    `lib.mvd.assert_tv_export`/`parse_tv_export_filename` expect a strict
    7-field `<Strategy>_<Instrument>_<Version>_<Broker>_<Symbol>_<Date>_<hash>`
    pattern built for the OANDA/Pepperstone convention. CME TV-exports do not
    follow one consistent positional pattern -- verified against this repo's
    own manifest: Guardian's export has 9 underscore-delimited fields, Striker
    DJ30's has 9 in a different shape, Striker NAS100's has 8 with no version
    token, and Aegis's carries parentheses/hyphens. Forcing a second rigid
    positional pattern would be brittle and need re-patching per file.

    This checks only that the expected strategy and symbol tokens both appear
    in the filename -- no position, no field count. The actual integrity
    guarantee for these files is the SHA256 pin in
    `core/data/tv_exports/cme/SHA256SUMS` (`scripts/check_data_manifests.py
    --check`); this is a secondary sanity check against a wrong-file-in-slot
    mistake, not the security boundary.
    """
    filename = Path(csv_path).name
    if expected_strategy_token not in filename:
        raise AssertionError(
            f"CME TV-export identity fail (strategy): expected "
            f"{expected_strategy_token!r} to appear in {filename!r}"
        )
    if expected_symbol not in filename:
        raise AssertionError(
            f"CME TV-export identity fail (symbol): expected "
            f"{expected_symbol!r} to appear in {filename!r}"
        )


def _align_candidate(panel: pd.DataFrame, candidate: pd.Series) -> tuple[pd.DataFrame, dict]:
    """Trim panel+candidate to their overlapping business-day window; zero-fill
    non-trading days within that window only. Never zero-fill the candidate
    across dates outside its own real window (manufactures fake co-silence
    correlation — design doc §6)."""
    candidate_name = candidate.name or "candidate"
    if candidate_name in panel.columns:
        raise ValueError(
            f"candidate name {candidate_name!r} collides with an existing panel column"
        )
    candidate = candidate.dropna()
    if candidate.empty:
        raise ValueError("candidate series is empty after dropping NaNs")

    start = max(panel.index.min(), candidate.index.min())
    end = min(panel.index.max(), candidate.index.max())
    if start > end:
        raise ValueError(
            "candidate date range does not overlap the panel window: "
            f"candidate=[{candidate.index.min()}, {candidate.index.max()}], "
            f"panel=[{panel.index.min()}, {panel.index.max()}]"
        )

    window = pd.bdate_range(start, end)
    trimmed = panel.reindex(window).fillna(0.0)
    trimmed[candidate_name] = candidate.reindex(window).fillna(0.0)
    n_blocks = len(build_week_blocks(trimmed))
    if n_blocks < 2:
        raise ValueError(
            f"candidate overlap window too short for weekly breadth: only "
            f"{n_blocks} weekly block(s) between {start.date()} and {end.date()} "
            f"(need at least 2)"
        )
    window_info = {
        "start": str(start.date()),
        "end": str(end.date()),
        "n_bdays": len(window),
        "n_blocks": n_blocks,
        "thin_overlap": n_blocks < MIN_OVERLAP_BLOCKS,
    }
    return trimmed, window_info


def _weekly(panel: pd.DataFrame) -> np.ndarray:
    blocks = build_week_blocks(panel)
    return blocks.sum(axis=1)


def compute_breadth(panel: pd.DataFrame, candidate: pd.Series | None = None) -> dict:
    """N_eff (dependence + risk) on the weekly-aggregated panel. If `candidate`
    is given, injects it as a 5th column (see _align_candidate) and adds
    candidate-specific keys: candidate_vs_composite_corr, candidate_vs_leg_corr,
    n_eff_dependence_delta, n_eff_risk_delta (vs the same-window 4-leg baseline)."""
    baseline_columns = list(panel.columns)

    if candidate is None:
        working_panel = panel
        window_info = {
            "start": str(panel.index.min().date()),
            "end": str(panel.index.max().date()),
            "n_bdays": len(panel),
            "n_blocks": len(build_week_blocks(panel)),
            "thin_overlap": False,
        }
    else:
        working_panel, window_info = _align_candidate(panel, candidate)

    weekly = _weekly(working_panel)
    corr = np.corrcoef(weekly, rowvar=False)
    cov = np.cov(weekly, rowvar=False)

    result = {
        "columns": list(working_panel.columns),
        "n_bdays": window_info["n_bdays"],
        "n_blocks": window_info["n_blocks"],
        "n_eff_dependence": participation_ratio(corr),
        "n_eff_risk": participation_ratio(cov),
        "enb_dependence": effective_number_of_bets(corr),
        "window": window_info,
    }

    if candidate is not None:
        candidate_name = candidate.name or "candidate"
        col_index = list(working_panel.columns).index(candidate_name)
        composite = working_panel[baseline_columns].sum(axis=1).rename("composite")
        weekly_candidate = weekly[:, col_index]
        weekly_composite = _weekly(composite.to_frame())[:, 0]

        result["candidate_vs_composite_corr"] = float(
            np.corrcoef(weekly_candidate, weekly_composite)[0, 1]
        )
        result["candidate_vs_leg_corr"] = {
            leg: float(np.corrcoef(weekly_candidate, weekly[:, i])[0, 1])
            for i, leg in enumerate(baseline_columns)
        }

        baseline_result = compute_breadth(working_panel[baseline_columns])
        result["n_eff_dependence_delta"] = (
            result["n_eff_dependence"] - baseline_result["n_eff_dependence"]
        )
        result["n_eff_risk_delta"] = result["n_eff_risk"] - baseline_result["n_eff_risk"]

    return result


def _print_report(result: dict, label: str = "") -> None:
    prefix = f"[{label}] " if label else ""
    print(f"{prefix}n_bdays={result['n_bdays']}  n_blocks={result['n_blocks']}")
    print(f"{prefix}N_eff dependence (PR corr) = {result['n_eff_dependence']:.4f}")
    print(f"{prefix}N_eff risk       (PR cov)  = {result['n_eff_risk']:.4f}")
    print(f"{prefix}ENB corroboration (corr)   = {result['enb_dependence']:.4f}")
    if result["window"]["thin_overlap"]:
        print(
            f"{prefix}** THIN OVERLAP: only {result['n_blocks']} weekly blocks "
            f"({result['window']['start']} -> {result['window']['end']}) — "
            f"low-confidence delta **"
        )
    if "n_eff_dependence_delta" in result:
        print(f"{prefix}candidate vs composite corr = {result['candidate_vs_composite_corr']:.4f}")
        for leg, corr in result["candidate_vs_leg_corr"].items():
            print(f"{prefix}  vs {leg:16} corr = {corr:.4f}")
        print(f"{prefix}N_eff dependence delta = {result['n_eff_dependence_delta']:+.4f}")
        print(f"{prefix}N_eff risk delta       = {result['n_eff_risk_delta']:+.4f}")


# Per-panel self-test anchors. "pepperstone" is the historical 4-leg CFD
# record (retired feed, kept for regression continuity of the math itself);
# "cme" is the 2-leg AUTHORIZED-only futures panel (ADR 2026-08-19-cme-broker-
# panel-admission-for-breadth-revival). Adding a future panel means adding a
# row here, not overloading the Pepperstone constants.
_SELF_TEST_ANCHORS = {
    "pepperstone": {
        "n_bdays": EXPECTED_N_BDAYS,
        "n_blocks": EXPECTED_N_BLOCKS,
        "dependence": NEFF_DEPENDENCE_ANCHOR,
        "risk": NEFF_RISK_ANCHOR,
        "label": "Q-NEFF-1",
    },
    "cme": {
        "n_bdays": CME_EXPECTED_N_BDAYS,
        "n_blocks": CME_EXPECTED_N_BLOCKS,
        "dependence": CME_NEFF_DEPENDENCE_ANCHOR,
        "risk": CME_NEFF_RISK_ANCHOR,
        "label": "cme-2026-08-19",
    },
}


def _self_test(panel_name: str) -> int:
    """Reproduce this panel's own recorded anchor. Exit: 0 PASS, 1 FAIL,
    2 SKIP (panel absent). Unregistered panel names fail loudly rather than
    silently comparing against the wrong anchor."""
    if not baseline_panel_available(panel_name):
        print(
            f"[self-test] SKIP: vendor CSVs for panel {panel_name!r} not present "
            f"locally (gitignored; see core/data/tv_exports/{panel_name}/SHA256SUMS)."
        )
        # Not a pass: SKIP must be distinguishable from PASS (0) and FAIL (1).
        return SELF_TEST_SKIP

    if panel_name not in _SELF_TEST_ANCHORS:
        sys.exit(
            f"ABORT: no self-test anchor registered for panel {panel_name!r} "
            f"(registered: {sorted(_SELF_TEST_ANCHORS)}). Measure once, then add "
            f"a row to _SELF_TEST_ANCHORS -- do not guess an anchor."
        )
    anchor = _SELF_TEST_ANCHORS[panel_name]

    panel = load_baseline_panel(panel_name)
    result = compute_breadth(panel)
    _print_report(result, label="self-test")

    ok = True
    if result["n_bdays"] != anchor["n_bdays"] or result["n_blocks"] != anchor["n_blocks"]:
        print(
            f"[self-test] FAIL: panel shape {result['n_bdays']}/{result['n_blocks']} "
            f"!= expected {anchor['n_bdays']}/{anchor['n_blocks']} — the frame is "
            f"being consumed wrong."
        )
        ok = False
    if abs(result["n_eff_dependence"] - anchor["dependence"]) > ANCHOR_TOLERANCE:
        print(
            f"[self-test] FAIL: N_eff dependence {result['n_eff_dependence']:.4f} "
            f"does not reproduce the {anchor['label']} anchor {anchor['dependence']} "
            f"(tolerance {ANCHOR_TOLERANCE})."
        )
        ok = False
    if abs(result["n_eff_risk"] - anchor["risk"]) > ANCHOR_TOLERANCE:
        print(
            f"[self-test] FAIL: N_eff risk {result['n_eff_risk']:.4f} does not "
            f"reproduce the {anchor['label']} anchor {anchor['risk']} "
            f"(tolerance {ANCHOR_TOLERANCE})."
        )
        ok = False

    print(f"[self-test] {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def _load_candidates(path: Path, benchmark_col: str | None) -> dict:
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    candidates = {}
    for col in df.columns:
        if benchmark_col and col == benchmark_col:
            continue
        candidates[col] = df[col].rename(col)
    return candidates


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Incremental-breadth 5th-column N_eff (discovery-campaign Stage 8)."
    )
    ap.add_argument(
        "--self-test", action="store_true",
        help="Reproduce the Q-NEFF-1 anchor on the 4-leg baseline; print PASS/FAIL.",
    )
    ap.add_argument(
        "--candidates-csv",
        help="Stage-4 return-matrix CSV: timestamp index, one col/candidate, "
             "optional benchmark col.",
    )
    ap.add_argument(
        "--benchmark-col", default="benchmark",
        help="Column name to exclude from breadth injection. Default: benchmark.",
    )
    ap.add_argument(
        "--panel", default="pepperstone",
        help="Broker panel to load (default: pepperstone, which is unregistered. "
             "Use --panel cme for the 2-leg breadth baseline).",
    )
    ap.add_argument("--json", action="store_true", help="Emit JSON instead of a printed report.")
    args = ap.parse_args()

    if args.self_test:
        return _self_test(args.panel)

    if not args.candidates_csv:
        sys.exit("Provide --self-test or --candidates-csv.")

    if not baseline_panel_available(args.panel):
        sys.exit(f"ABORT: vendor CSVs for panel {args.panel!r} not present locally.")

    panel = load_baseline_panel(args.panel)
    baseline = compute_breadth(panel)
    candidates = _load_candidates(Path(args.candidates_csv), args.benchmark_col)

    reports = {"baseline": baseline}
    for name, series in candidates.items():
        reports[name] = compute_breadth(panel, candidate=series)

    if args.json:
        print(json.dumps(reports, indent=2, default=str))
    else:
        _print_report(baseline, label="baseline")
        for name in candidates:
            print()
            _print_report(reports[name], label=name)

    return 0


if __name__ == "__main__":
    sys.exit(main())
