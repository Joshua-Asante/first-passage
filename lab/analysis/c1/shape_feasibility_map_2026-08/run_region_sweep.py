"""A2 payoff-shape feasibility map -- region sweep driver.

Parameterizes the EXISTING survivor-MC machinery (core/mc/simulation.py via
lab/discovery/prop_survivor_scoring.py -- never reimplemented) over the
synthetic payoff-shape grid in shape_generator.py, and scores each
(win_rate, shape, trades/week, risk, firm) tuple jointly against the eval
bust ceiling, the pass floor (which already embeds the venue's consistency
rule -- see RESULTS.md) and the intraday-honest limb.

Compute-budget disclosure (RESULTS.md "Compute budget" section has the full
numbers): the frozen survivor-scoring sims_per_seed (10,000, from
load_scoring_thresholds()) measured at ~300s per (tuple, firm) cell on this
machine. A full 630-cell grid at that N is ~52 CPU-hours -- outside this
task's responsible compute budget (Rule 2, CLAUDE.md). This harness therefore
runs the FULL 630-cell grid (zero cells dropped -- coverage is not narrowed)
at a reduced `--n-sims` per seed, keeping the frozen SEEDS (42/123/2026) and
frozen HORIZON (1500) byte-identical to load_scoring_thresholds() -- the only
axis that moves is sims_per_seed, disclosed on every output row via
`n_total_paths`, with SE-of-proportion bars computed at the N actually used.
A separate `--validation` pass re-scores a small reference subset at the full
frozen sims_per_seed=10,000 to cross-check the reduced-N sweep's verdicts.

Sharded execution: pass --shard-index i --n-shards N to score only cells
i, i+N, i+2N, ... of the fixed 630-cell enumeration (deterministic, so shards
partition the grid exactly once with no overlap and no gap). Each shard
appends to its own JSONL as it goes -- safe to inspect mid-run, safe to
resume (existing rows are not re-computed on a re-invocation with the same
--out path, keyed by cell_id).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[3]
for _p in (_ROOT / "core", _ROOT / "lab"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from firm_rules import FIRM_RULES  # noqa: E402
from mc.preflight import assert_engine_ready, firm_kwargs, summarize_outcomes  # noqa: E402
from mc.simulation import run_seed  # noqa: E402
from discovery.prop_survivor_scoring import (  # noqa: E402
    CANDIDATE_STRAT,
    DD_SCALE,
    NO_PROTECTION_TRIGGER,
    load_scoring_thresholds,
    paired_blocks_from_daily,
)

import shape_generator as sg  # noqa: E402

FIRM_KEYS: Tuple[str, ...] = ("Tradeify_Select_100K", "MFFU_Rapid_100K")
DD_GATE = 0.03  # eval_bust_ceiling, also independently confirmed == thr.eval_bust_ceiling below
PASS_GATE = 0.50  # pass_floor, also independently confirmed == thr.pass_floor below

# Fixed reference cells for the --validation pass (full frozen N). Chosen for
# CORNER coverage (fast-pass, fast-bust, near-zero-edge already measured in
# this session's own timing probe), never for favorable results.
VALIDATION_CELLS: List[Tuple[float, str, int, float]] = [
    (0.50, "symmetric", 1, 275.0),  # near-zero edge, already run this session
    (0.70, "bounded_clustered", 8, 250.0),  # expected fast-pass corner
    (0.40, "symmetric", 8, 325.0),  # expected fast-bust corner
    (0.65, "mild_right_skew", 3, 275.0),  # mid-grid, positive skew
]


def firm_consistency(firm_key: str) -> float | None:
    raw = FIRM_RULES[firm_key].get("consistency_rule_pct")
    return None if raw is None else float(raw) / 100.0


def all_cells() -> List[Tuple[float, str, int, float, str]]:
    """Fixed 630-cell enumeration: 315 tuples x 2 firms, tuple-major order."""
    out = []
    for t in sg.all_tuples():
        for firm in FIRM_KEYS:
            out.append((*t, firm))
    return out


def cell_id(win_rate: float, shape: str, cadence: int, risk: float, firm: str) -> str:
    return f"wr{win_rate:.2f}_{shape}_cd{cadence}_rk{int(risk)}_{firm}"


def se_of_proportion(p: float, n: int) -> float:
    if n <= 0:
        return float("nan")
    return float(np.sqrt(max(p * (1.0 - p), 0.0) / n))


def gate_status(p: float, se: float, gate: float, *, direction: str) -> str:
    """direction='le' -> gate is an upper bound (bust); 'ge' -> lower bound (pass)."""
    lo, hi = p - 2.0 * se, p + 2.0 * se
    if direction == "le":
        if hi <= gate:
            return "PASS"
        if lo > gate:
            return "FAIL"
        return "MARGINAL"
    if direction == "ge":
        if lo >= gate:
            return "PASS"
        if hi < gate:
            return "FAIL"
        return "MARGINAL"
    raise ValueError(direction)


def combine_verdict(bust_status: str, pass_status: str) -> str:
    if bust_status == "FAIL" or pass_status == "FAIL":
        return "INFEASIBLE"
    if bust_status == "MARGINAL" or pass_status == "MARGINAL":
        return "MARGINAL"
    return "FEASIBLE"


def _run_with_days(
    firm: str,
    blocks: np.ndarray,
    thr,
    *,
    n_sims: int,
    consistency: float | None,
    intraday_blocks: np.ndarray,
) -> Tuple[dict, List[int]]:
    """Mirrors prop_survivor_scoring.run_tier_remc's own call sequence exactly
    (same primitives, same order, same arguments) but also surfaces
    per-path days-to-pass, which run_tier_remc's return dict discards.
    Never reimplements simulate_path/run_seed -- both are the unmodified
    production engine, called the same way run_tier_remc calls them."""
    assert_engine_ready(firm)  # G3 gate, same as run_tier_remc
    kw = firm_kwargs(firm, inactivity_off=True, consistency=consistency)
    seeds_results = [
        run_seed(
            seed, n_sims, blocks, NO_PROTECTION_TRIGGER, DD_SCALE,
            horizon=thr.horizon, strats=CANDIDATE_STRAT, firm_kwargs=kw,
            intraday_blocks=intraday_blocks,
        )
        for seed in thr.seeds
    ]
    summary = summarize_outcomes(seeds_results, n_sims)
    days = [d for r in seeds_results for d in r["days_to_pass"]]
    return summary, days


def score_cell(
    win_rate: float,
    shape: str,
    cadence: int,
    risk: float,
    firm: str,
    *,
    n_sims: int,
    thr,
    panel_cache: Dict[Tuple[float, str, int, float], Tuple[np.ndarray, np.ndarray]],
) -> dict:
    key = (win_rate, shape, cadence, risk)
    if key not in panel_cache:
        panel_cache[key] = sg.build_panel(win_rate, shape, cadence, risk)
    daily, intraday = panel_cache[key]
    blocks_p, blocks_l = paired_blocks_from_daily(daily, intraday)

    cons = firm_consistency(firm)
    t0 = time.time()
    summary, days_to_pass = _run_with_days(
        firm, blocks_p, thr, n_sims=n_sims, consistency=cons, intraday_blocks=blocks_l,
    )
    dt = time.time() - t0

    bust = float(summary["headline_bust"])
    passr = float(summary["pass_rate"])
    n_total = n_sims * len(thr.seeds)
    se_bust = se_of_proportion(bust, n_total)
    se_pass = se_of_proportion(passr, n_total)
    bust_status = gate_status(bust, se_bust, DD_GATE, direction="le")
    pass_status = gate_status(passr, se_pass, PASS_GATE, direction="ge")

    return {
        "cell_id": cell_id(win_rate, shape, cadence, risk, firm),
        "win_rate": win_rate,
        "shape": shape,
        "cadence": cadence,
        "risk_usd": risk,
        "firm": firm,
        "firm_consistency_pct": None if cons is None else cons * 100.0,
        "expectancy_r": sg.expectancy_r(win_rate, shape),
        "n_sims_per_seed": n_sims,
        "n_total_paths": n_total,
        "seeds": list(thr.seeds),
        "horizon": thr.horizon,
        "bust": bust,
        "se_bust": se_bust,
        "bust_status": bust_status,
        "pass_rate": passr,
        "se_pass": se_pass,
        "pass_status": pass_status,
        "verdict": combine_verdict(bust_status, pass_status),
        "rates": summary["rates"],
        "n_passes_observed": len(days_to_pass),
        "median_days_to_pass": (
            float(np.median(days_to_pass)) if days_to_pass else None
        ),
        "elapsed_s": dt,
    }


def _load_done_ids(out_path: Path) -> set:
    done = set()
    if out_path.is_file():
        for line in out_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                done.add(json.loads(line)["cell_id"])
            except (json.JSONDecodeError, KeyError):
                continue
    return done


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--shard-index", type=int, default=0)
    ap.add_argument("--n-shards", type=int, default=1)
    ap.add_argument("--n-sims", type=int, default=500, help="sims_per_seed (frozen seeds/horizon untouched)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--validation", action="store_true", help="run VALIDATION_CELLS at full frozen N instead")
    args = ap.parse_args(argv)

    thr = load_scoring_thresholds()
    assert abs(thr.eval_bust_ceiling - DD_GATE) < 1e-9, thr.eval_bust_ceiling
    assert abs(thr.pass_floor - PASS_GATE) < 1e-9, thr.pass_floor

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    done = _load_done_ids(out_path)

    if args.validation:
        cells = [(*t, firm) for t in VALIDATION_CELLS for firm in FIRM_KEYS]
        n_sims = thr.sims_per_seed
    else:
        full = all_cells()
        cells = full[args.shard_index :: args.n_shards]
        n_sims = args.n_sims

    panel_cache: Dict[Tuple[float, str, int, float], Tuple[np.ndarray, np.ndarray]] = {}
    print(
        f"[sweep] shard={args.shard_index}/{args.n_shards} cells={len(cells)} "
        f"n_sims/seed={n_sims} validation={args.validation} out={out_path}",
        flush=True,
    )
    n_done_now = 0
    with out_path.open("a", encoding="utf-8") as fh:
        for win_rate, shape, cadence, risk, firm in cells:
            cid = cell_id(win_rate, shape, cadence, risk, firm)
            if cid in done:
                continue
            rec = score_cell(
                win_rate, shape, cadence, risk, firm,
                n_sims=n_sims, thr=thr, panel_cache=panel_cache,
            )
            fh.write(json.dumps(rec) + "\n")
            fh.flush()
            n_done_now += 1
            print(
                f"[sweep] {rec['cell_id']} bust={rec['bust']:.4f}({rec['bust_status']}) "
                f"pass={rec['pass_rate']:.4f}({rec['pass_status']}) verdict={rec['verdict']} "
                f"({rec['elapsed_s']:.1f}s) [{n_done_now}/{len(cells)} this invocation]",
                flush=True,
            )
    print(f"[sweep] done. wrote {n_done_now} new rows to {out_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
