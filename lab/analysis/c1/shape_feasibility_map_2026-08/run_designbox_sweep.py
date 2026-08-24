"""Design-box extension -- region sweep driver.

Disclosed COVERAGE EXTENSION of A2's feasibility map (run_region_sweep.py),
NEVER merged into A2's own frozen 630-cell grid or region_data.jsonl (a
separate output file, designbox_region_data.jsonl, is written here). Extends
the map to the slate-2 design-box geometry (design_box_shape.py) -- see
RESULTS_DESIGNBOX_EXT.md for the full disclosure.

Reuses run_region_sweep.py's own scoring/gating primitives BYTE-IDENTICALLY
by importing them directly (`se_of_proportion`, `gate_status`,
`combine_verdict`, `firm_consistency`, `_run_with_days`, `DD_GATE`,
`PASS_GATE`) -- never re-typed. `_run_with_days` is where the actual engine
call sequence lives (`assert_engine_ready` -> `firm_kwargs` -> `run_seed` per
frozen seed -> `summarize_outcomes`); importing it directly means this
harness calls the identical function A2 calls, not a re-implementation of it.
Only `score_cell`/`cell_id`/`all_cells` are written fresh here, because they
take design_box_shape's own 3-axis `(win_rate, cadence, risk)` tuple rather
than A2's 4-axis `(win_rate, shape, cadence, risk)` tuple.

FIRM_KEYS below is this dispatch's own pre-registration (Tradeify_Select_100K,
MFFU_Rapid_100K) -- deliberately NOT imported from run_region_sweep.py's own
FIRM_KEYS, which as of 2026-08-24 also carries Tradeify_Growth_100K (a
same-day, separate extension, out of scope for this dispatch's pre-registered
2-firm grid -- see RESULTS_DESIGNBOX_EXT.md).

Full frozen `sims_per_seed=10,000` x 3 seeds for EVERY cell (dispatch
instruction) -- no reduced-N deviation, unlike A2's own primary sweep (Sec4).

Sharded execution, same convention as run_region_sweep.py: pass
`--shard-index i --n-shards N` to score only cells `i, i+N, i+2N, ...` of the
fixed enumeration. Each shard appends to its own JSONL as it goes -- safe to
resume (existing cell_ids are not re-computed on re-invocation).
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

from discovery.prop_survivor_scoring import (  # noqa: E402
    load_scoring_thresholds,
    paired_blocks_from_daily,
)

import design_box_shape as dbs  # noqa: E402
from run_region_sweep import (  # noqa: E402 -- byte-identical reuse, never re-typed
    DD_GATE,
    PASS_GATE,
    _run_with_days,
    combine_verdict,
    firm_consistency,
    gate_status,
    se_of_proportion,
)

# Dispatch pre-registration -- deliberately NOT run_region_sweep.FIRM_KEYS (now 3-firm
# as of 2026-08-24; Growth is a separate, same-day extension, out of scope here).
FIRM_KEYS: Tuple[str, ...] = ("Tradeify_Select_100K", "MFFU_Rapid_100K")


def all_cells() -> List[Tuple[float, int, float, str]]:
    """Fixed enumeration: design_box_shape's 40 tuples x 2 firms = 80 cells."""
    out: List[Tuple[float, int, float, str]] = []
    for t in dbs.all_tuples():
        for firm in FIRM_KEYS:
            out.append((*t, firm))
    return out


def cell_id(win_rate: float, cadence: int, risk: float, firm: str) -> str:
    return f"wr{win_rate:.2f}_designbox_cd{cadence}_rk{risk:g}_{firm}"


def score_cell(
    win_rate: float,
    cadence: int,
    risk: float,
    firm: str,
    *,
    n_sims: int,
    thr,
    panel_cache: Dict[Tuple[float, int, float], Tuple[np.ndarray, np.ndarray]],
) -> dict:
    key = (win_rate, cadence, risk)
    if key not in panel_cache:
        panel_cache[key] = dbs.build_panel(win_rate, cadence, risk)
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

    is_frontier = risk not in dbs.EM2_RISK_USD

    return {
        "cell_id": cell_id(win_rate, cadence, risk, firm),
        "win_rate": win_rate,
        "shape": dbs.SHAPE_NAME,
        "cadence": cadence,
        "risk_usd": risk,
        "risk_source": "frontier_r" if is_frontier else "em2_axis",
        "firm": firm,
        "firm_consistency_pct": None if cons is None else cons * 100.0,
        "expectancy_r": dbs.expectancy_r(win_rate),
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
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)

    thr = load_scoring_thresholds()
    assert abs(thr.eval_bust_ceiling - DD_GATE) < 1e-9, thr.eval_bust_ceiling
    assert abs(thr.pass_floor - PASS_GATE) < 1e-9, thr.pass_floor

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    done = _load_done_ids(out_path)

    full = all_cells()
    cells = full[args.shard_index :: args.n_shards]
    n_sims = thr.sims_per_seed  # FULL frozen N -- dispatch instruction, no reduction

    panel_cache: Dict[Tuple[float, int, float], Tuple[np.ndarray, np.ndarray]] = {}
    print(
        f"[designbox-sweep] shard={args.shard_index}/{args.n_shards} cells={len(cells)} "
        f"n_sims/seed={n_sims} out={out_path}",
        flush=True,
    )
    n_done_now = 0
    with out_path.open("a", encoding="utf-8") as fh:
        for win_rate, cadence, risk, firm in cells:
            cid = cell_id(win_rate, cadence, risk, firm)
            if cid in done:
                continue
            rec = score_cell(
                win_rate, cadence, risk, firm,
                n_sims=n_sims, thr=thr, panel_cache=panel_cache,
            )
            fh.write(json.dumps(rec) + "\n")
            fh.flush()
            n_done_now += 1
            print(
                f"[designbox-sweep] {rec['cell_id']} bust={rec['bust']:.4f}({rec['bust_status']}) "
                f"pass={rec['pass_rate']:.4f}({rec['pass_status']}) verdict={rec['verdict']} "
                f"({rec['elapsed_s']:.1f}s) [{n_done_now}/{len(cells)} this invocation]",
                flush=True,
            )
    print(f"[designbox-sweep] done. wrote {n_done_now} new rows to {out_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
