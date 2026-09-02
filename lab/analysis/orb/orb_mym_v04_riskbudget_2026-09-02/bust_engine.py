"""Stage C — canonical bust/pass engine on the common scorable window.
Mirrors lab/analysis/orb/orb_mnq_recon_v3_2026-08-31/bust_pass_sim.py
(core/mc/simulation.py verbatim; firm_kwargs; 5-day blocks; intraday-honest MAE proxy).
Cells frozen in PREREG_filters.md. seeds (1,2,3) x N_SIMS."""
from __future__ import annotations
import json, os, sys, time
from pathlib import Path
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "core"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from mc.simulation import HORIZON_CAP, run_seed, simulate_path  # noqa: E402
from mc.preflight import firm_kwargs, summarize_outcomes  # noqa: E402
from mc.ingest import build_week_blocks  # noqa: E402
from feat_lib import day_frame  # noqa: E402

OUT = Path(__file__).resolve().parent
SEEDS = (1, 2, 3)
N_SIMS = int(os.environ.get("N_SIMS", "4000"))
TIERS = {"Select": ("Tradeify_Select_100K", 0.40), "Growth": ("Tradeify_Growth_100K", None)}

m = day_frame()
s = m[m.scorable].sort_index().copy()
pnl = s["pnl_pc"]; mae = s["mae_pc"]
hot = s["hot"].to_numpy(int); wide = s["orr_wide"].to_numpy(int)
bt = s["base_time_min"].to_numpy(float); vt = s["or0930_vol_tod"].to_numpy(float)
ones = np.ones(len(s))

# size vectors (contracts per leg on each traded day)
CELLS = {
    "base_q1": ones * 1.0,
    "base_q2": ones * 2.0,
    "P1_q1_skip_after_1100": np.where(bt <= 660, 1.0, 0.0),
    "P1_q2_skip_after_1100": np.where(bt <= 660, 2.0, 0.0),
    "P2_hot1_calm2": np.where(hot == 1, 1.0, 2.0),
    "P3_wide1_narrow2": np.where(wide == 1, 1.0, 2.0),
    # exploratory
    "X_vol_tod_gt1_q1": np.where(vt > 1, 1.0, 0.0),
    "X_hot_only_q1": np.where(hot == 1, 1.0, 0.0),
    "X_hot_only_q2": np.where(hot == 1, 2.0, 0.0),
    "X_nothot_only_q1": np.where(hot == 0, 1.0, 0.0),
    "X_nothot_only_q2": np.where(hot == 0, 2.0, 0.0),
    "X_P2_inverse_hot2_calm1": np.where(hot == 1, 2.0, 1.0),
    "X_P3_inverse_wide2_narrow1": np.where(wide == 1, 2.0, 1.0),
    "X_P2andP3_q1_if_hot_or_wide": np.where((hot == 1) | (wide == 1), 1.0, 2.0),
}


def build(size: np.ndarray):
    # Monday-anchored, non-overlapping 5-business-day blocks (core/mc/ingest.py::
    # build_week_blocks, the canonical construction) -- fixed 2026-09-02 (Codex
    # review, PR #265): a naive p[:u].reshape(n_weeks,5,1) chunks from whatever
    # the panel's first row happens to be (here a Thursday), pairing Thu/Fri with
    # the FOLLOWING week's Mon-Wed instead of the same calendar week, and drops
    # the tail via truncation rather than an explicit incomplete-week policy.
    idx = pd.bdate_range(s.index.min(), s.index.max())
    p = (pnl * size).reindex(idx, fill_value=0.0)
    q = np.minimum((mae * size).reindex(idx, fill_value=0.0), 0.0)
    blocks = build_week_blocks(p.to_frame())
    iblocks = build_week_blocks(q.to_frame())
    return p.to_numpy(float).reshape(-1, 1), q.to_numpy(float), blocks, iblocks


results = {}
t0 = time.time()
for name, size in CELLS.items():
    path, low, blocks, iblocks = build(size)
    results[name] = {"n_traded_days": int((size > 0).sum()), "avg_contracts_on_traded": float(size[size > 0].mean())}
    for tier, (fk, cons) in TIERS.items():
        fkw = firm_kwargs(fk, consistency=cons)
        real_i = simulate_path(path, 1.0, 1.0, path.shape[0], intraday_low=low, **fkw)
        boot_i = summarize_outcomes([run_seed(sd, N_SIMS, blocks, 1.0, 1.0, horizon=HORIZON_CAP,
                                              firm_kwargs=fkw, intraday_blocks=iblocks) for sd in SEEDS], N_SIMS)
        cell = {"realized_intraday": [real_i[0], int(real_i[1]), round(real_i[2] * 100, 2)],
                "bust_intraday": round(boot_i["headline_bust"] * 100, 2),
                "pass_intraday": round(boot_i["pass_rate"] * 100, 2)}
        if name.startswith("base"):
            boot_e = summarize_outcomes([run_seed(sd, N_SIMS, blocks, 1.0, 1.0, horizon=HORIZON_CAP,
                                                  firm_kwargs=fkw) for sd in SEEDS], N_SIMS)
            cell["bust_eod"] = round(boot_e["headline_bust"] * 100, 2)
            cell["pass_eod"] = round(boot_e["pass_rate"] * 100, 2)
        results[name][tier] = cell
        print(f"[{time.time()-t0:6.0f}s] {name:28s} {tier:6s} bust={cell['bust_intraday']:6.2f}%  pass={cell['pass_intraday']:6.2f}%"
              + (f"  (EOD bust {cell['bust_eod']}% pass {cell['pass_eod']}%)" if 'bust_eod' in cell else ""), flush=True)
    (OUT / "bust_engine_results.json").write_text(json.dumps(results, indent=2))

# ---------------------------------------------------------------------------
# Inactivity-barrier check (Codex review, PR #265, P1): every cell above ran
# with firm_kwargs's default inactivity_off=True (repo convention, matching
# every other qty-scaling bust/pass measurement in this repo -- see
# core/mc/preflight.py's own INACTIVITY_OFF docstring). That convention was
# established for constructs that ALWAYS trade, just at different size; it is
# untested for a construct that SKIPS entire days, which can run a real risk of
# breaching Tradeify's actual 5-business-day inactivity limit
# (firm_rules.py: inactivity_max_idle_days=5, sourced, not a placeholder).
# Re-score the day-skipping cells with the barrier ON to measure the gap.
# ---------------------------------------------------------------------------
BARRIER_CHECK = ("base_q1", "base_q2", "P1_q1_skip_after_1100",
                  "X_hot_only_q1", "X_hot_only_q2")
print("\n=== inactivity-barrier check (Codex PR #265 P1): barrier ON vs repo-convention OFF ===", flush=True)
barrier = {}
for name in BARRIER_CHECK:
    size = CELLS[name]
    path, low, blocks, iblocks = build(size)
    barrier[name] = {}
    for tier, (fk, cons) in TIERS.items():
        fkw_on = firm_kwargs(fk, consistency=cons, inactivity_off=False)
        boot_on = summarize_outcomes([run_seed(sd, N_SIMS, blocks, 1.0, 1.0, horizon=HORIZON_CAP,
                                               firm_kwargs=fkw_on, intraday_blocks=iblocks) for sd in SEEDS], N_SIMS)
        off = results[name][tier]
        on = {"bust_intraday": round(boot_on["headline_bust"] * 100, 2),
              "pass_intraday": round(boot_on["pass_rate"] * 100, 2),
              "bust_inactivity_rate": round(boot_on["rates"]["bust_inactivity"] * 100, 2)}
        barrier[name][tier] = {"barrier_off": off, "barrier_on": on}
        print(f"  {name:26s} {tier:6s} OFF bust={off['bust_intraday']:6.2f}%  "
              f"ON bust={on['bust_intraday']:6.2f}%  (of which pure-inactivity {on['bust_inactivity_rate']:5.2f}%)"
              f"  pass OFF={off['pass_intraday']:6.2f}% ON={on['pass_intraday']:6.2f}%", flush=True)
(OUT / "inactivity_barrier_check.json").write_text(json.dumps(barrier, indent=2))
print("done", flush=True)
