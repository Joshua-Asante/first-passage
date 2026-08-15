"""
build_envelope.py — Guardian-only decay-gate envelope builder
==============================================================

Resolves DP-7 of Q-GUARDIAN-DECAY-1 (the Guardian-only MC envelope, Joshua's
§0.5 Q1 call) AND the stopgap empirical envelope (option 2), and pins the
CUSUM boundaries the live gate consumes.

This is a RESEARCH-LAYER harness (lab/). It imports core/portfolio_mc's own
functions and drives them with a single-strategy dict {"guardian": ...} so the
Guardian-only MC is byte-faithful to the canonical 4-strategy machinery:
  - same 1R→(0.34%×$200K) scaling (build_daily_panel / implied_1r),
  - same Mon-anchored week-block bootstrap (build_week_blocks / run_seed),
  - same dd_protection C2 (DD_TRIGGER 1.5% / DD_SCALE 0.40×),
  - same FXIFY-correct pass/bust/timeout semantics (_simulate_path),
  - same seeds (42, 123, 2026).
The only difference vs the canonical run is the panel has ONE column, so the
pass/bust/DD distribution is Guardian-solo — exactly the per-strategy envelope
portfolio_mc explicitly scopes out (portfolio_mc.py:7).

NO core/ file is modified. NO locked parameter is touched. Read-only.

Vendor data (the locked Pepperstone Guardian CSV) is gitignored, so on a public
clone / remote container this script SKIPS with a NEEDS_DATA notice and exits 0.
Run it locally where core/data/tv_exports/pepperstone/ is populated; it writes
envelope.json next to this file, which decay_gate.py then consumes.

Usage:
    python lab/analysis/guardian_decay_gate_2026-06-25/build_envelope.py
    python lab/analysis/guardian_decay_gate_2026-06-25/build_envelope.py --out envelope.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

# ── locate repo root + import core/portfolio_mc ─────────────────────────────
# repo_root/lab/analysis/guardian_decay_gate_2026-06-25/build_envelope.py
REPO_ROOT = Path(__file__).resolve().parents[3]
CORE = REPO_ROOT / "core"
if str(CORE) not in sys.path:
    sys.path.insert(0, str(CORE))

try:
    import portfolio_mc as mc  # noqa: E402  (path-injected core module)
except Exception as e:  # pragma: no cover - import-environment dependent
    print(f"NEEDS_DATA: could not import core/portfolio_mc ({e}). "
          "Run from a clone with core/ present.")
    sys.exit(0)

HERE = Path(__file__).resolve().parent

# Calibration RNG seed — reuse the canonical MC's first seed for provenance.
CALIB_SEED = mc.SEEDS[0]

# CUSUM boundary calibration (DP-3) — by FINITE-HORIZON false-alarm probability,
# NOT mean ARL. A mean-ARL target false-alarms on Guardian's normal losing
# streaks (22% WR + fat right tail → 15-20-loss runs spike the CUSUM before a
# big win resets it). Calibrating h to the (1-alpha) quantile of the in-sample
# running-max CUSUM makes "cannot fire inside the in-sample envelope" (§5) true
# BY CONSTRUCTION: a false DECAYED has probability exactly ALPHA_DECAY over the
# evaluation horizon. The in-sample bootstrap is BLOCK-based (preserve win
# clustering) so realistic streaks are reflected in h.
EVAL_HORIZON_IR = 200     # in-regime trades the false-alarm prob is controlled over (~4 yr)
ALPHA_DECAY = 0.01        # ≤1% chance of a false DECAYED over the horizon (asymmetric: a
                          # false retirement kills a good strategy)
ALPHA_WATCH = 0.20        # WATCH is reversible → allowed to trip more readily
BLOCK_LEN = 10            # moving-block length (trades) to preserve serial win-clustering

# Degradation model (DP-2): right-tail thinning (a trend-rider decays by
# ceasing to capture big trends). We scale positive R by g<1 until the
# Guardian-SOLO MC bust-rate crosses the lock gate (1%), and ALSO require E1 to
# sit at/below the in-sample windowed-R 1st percentile. The binding (higher-bar)
# of the two defines H1, guaranteeing the DECAYED region is OUTSIDE the
# in-sample envelope (Q-GUARDIAN-DECAY-1 §4.2 hard constraint / §5).
LOCK_BUST_GATE = 0.01
WINDOW_FOR_P1 = 40    # window (in-regime trades) for the in-sample windowed-R p1


def load_guardian():
    """Return (trades_df, r1, R_series) or None if the locked panel is absent."""
    path = mc.PEPPERSTONE_PANELS["guardian"]
    if not path.exists():
        return None
    # load_trades + the MVD identity gate via the same code path the anchor uses.
    trades = mc.load_trades(path, strategy="guardian")
    r1, fell_back = mc.implied_1r(trades["pnl"], "guardian")
    if fell_back or r1 <= 0:
        raise RuntimeError(f"Guardian implied_1r fell back or non-positive (r1={r1}).")
    R = (trades["pnl"] / r1).to_numpy(dtype=float)
    return trades, float(r1), R


def guardian_solo_mc(trades_df, win_scale: float = 1.0) -> dict:
    """Run a Guardian-SOLO MC, optionally thinning wins by win_scale (<1 = decay).

    Faithful to the canonical machinery: build_daily_panel → build_week_blocks →
    run_seed across the canonical seeds, dd_protection C2. Returns aggregated
    pass/bust/DD metrics for Guardian alone.
    """
    df = trades_df.copy()
    if win_scale != 1.0:
        pos = df["pnl"] > 0
        df.loc[pos, "pnl"] = df.loc[pos, "pnl"] * win_scale

    trades_by_strat = {"guardian": df}
    allocs = {"guardian": mc.ALLOCATIONS["guardian"]}
    panel, scale_info = mc.build_daily_panel(trades_by_strat, allocs)
    blocks = mc.build_week_blocks(panel)
    if len(blocks) == 0:
        raise RuntimeError("No week-blocks built — panel too short / misaligned.")

    seed_results = [
        mc.run_seed(seed, mc.SIMS_PER_SEED, blocks, mc.DD_TRIGGER, mc.DD_SCALE,
                    strats=("guardian",))
        for seed in mc.SEEDS
    ]
    n = mc.SIMS_PER_SEED * len(mc.SEEDS)
    agg = {"pass": 0, "bust_daily": 0, "bust_static": 0,
           "bust_inactivity": 0, "horizon_cap": 0}
    all_dds: list[float] = []
    days: list[int] = []
    for r in seed_results:
        for k, v in r["outcomes"].items():
            agg[k] += v
        all_dds.extend(r["max_dds"])
        days.extend(r["days_to_pass"])
    dds = np.array(all_dds)
    bust = (agg["bust_daily"] + agg["bust_static"] + agg["bust_inactivity"]) / n
    return {
        "n_sims": n,
        "win_scale": win_scale,
        "pass_rate": agg["pass"] / n,
        "bust_rate": bust,
        "bust_daily": agg["bust_daily"] / n,
        "bust_static": agg["bust_static"] / n,
        "p50_dd": float(np.percentile(dds, 50)),
        "p95_dd": float(np.percentile(dds, 95)),
        "p99_dd": float(np.percentile(dds, 99)),
        "median_days_to_pass": float(np.median(days)) if days else None,
        "scale_info": {k: float(v) if isinstance(v, (int, float)) else v
                       for k, v in scale_info["guardian"].items()},
    }


def r_distribution(R: np.ndarray) -> dict:
    """Per-trade R distribution = the null H0 the sequential test sits on."""
    wins = R[R > 0]
    losses = R[R < 0]
    return {
        "N": int(R.size),
        "E0_mean_R": float(R.mean()),
        "std_R": float(R.std(ddof=1)),
        "win_rate": float((R > 0).mean()),
        "avg_win_R": float(wins.mean()) if wins.size else 0.0,
        "avg_loss_R": float(losses.mean()) if losses.size else 0.0,
        "pct": {p: float(np.percentile(R, p)) for p in (1, 5, 25, 50, 75, 95, 99)},
    }


# ── CUSUM calibration (DP-1 statistic + DP-3 boundaries) ────────────────────
def _block_bootstrap(R: np.ndarray, length: int, rng, block_len: int = BLOCK_LEN) -> np.ndarray:
    """Circular moving-block bootstrap — preserves serial win-clustering."""
    n = R.size
    out = np.empty(length, dtype=float)
    filled = 0
    while filled < length:
        start = int(rng.integers(0, n))
        take = min(block_len, length - filled)
        idx = (start + np.arange(take)) % n
        out[filled:filled + take] = R[idx]
        filled += take
    return out


def _cusum_path(seq: np.ndarray, k: float):
    """Yield the running-max CUSUM and the first-cross index for given seq.
    Returns (running_max, dict of {h: first_cross_index_or_None})."""
    C = 0.0
    running_max = 0.0
    crossings = {}
    for i, r in enumerate(seq, start=1):
        C = max(0.0, C + (k - r))
        if C > running_max:
            running_max = C
        crossings[i] = C
    return running_max, crossings


def _first_cross(seq: np.ndarray, k: float, h: float):
    C = 0.0
    for i, r in enumerate(seq, start=1):
        C = max(0.0, C + (k - r))
        if C >= h:
            return i
    return None


def calibrate_cusum(R: np.ndarray, E0: float, E1: float, *,
                    n_paths: int = 5000, horizon: int = EVAL_HORIZON_IR) -> dict:
    """Pin k (reference) and h_watch / h_decay by finite-horizon false-alarm
    probability, and report DETECTION POWER under the degraded alternative.

    k = (E0+E1)/2 is the standard CUSUM reference for a shift E0→E1.
    h_alpha = (1-alpha) quantile of the in-sample running-max CUSUM over a
    `horizon`-trade block-bootstrap path. By construction P(false alarm within
    horizon) = alpha → the DECAYED region sits strictly outside the in-sample
    envelope (§5). Detection power = P(degraded path crosses h within horizon).
    """
    rng = np.random.default_rng(CALIB_SEED)
    k = 0.5 * (E0 + E1)

    # in-control running-max CUSUM distribution (block bootstrap of observed R)
    inctrl_max = np.array([
        _cusum_path(_block_bootstrap(R, horizon, rng), k)[0] for _ in range(n_paths)
    ])
    h_watch = float(np.quantile(inctrl_max, 1.0 - ALPHA_WATCH))
    h_decay = float(np.quantile(inctrl_max, 1.0 - ALPHA_DECAY))

    # degraded alternative: thin wins by g so the pool mean ≈ E1
    wins_mass = R[R > 0].sum()
    losses_sum = R[R < 0].sum()
    g = (E1 * R.size - losses_sum) / wins_mass if wins_mass > 0 else 1.0
    g = float(max(0.0, min(1.0, g)))

    rng2 = np.random.default_rng(CALIB_SEED + 7)
    cross_watch = cross_decay = 0
    detect_idx = []
    for _ in range(n_paths):
        seq = _block_bootstrap(R, horizon, rng2)
        seq = seq.copy()
        seq[seq > 0] *= g
        iw = _first_cross(seq, k, h_watch)
        idc = _first_cross(seq, k, h_decay)
        if iw is not None:
            cross_watch += 1
        if idc is not None:
            cross_decay += 1
            detect_idx.append(idc)
    return {
        "statistic": "lower-CUSUM on regime-conditional per-trade R; "
                     "C_i=max(0,C_{i-1}+(k-r_i)); alarm C>=h",
        "k_reference_R": float(k),
        "h_watch": h_watch,
        "h_decay": h_decay,
        "eval_horizon_in_regime_trades": horizon,
        "alpha_watch": ALPHA_WATCH,
        "alpha_decay": ALPHA_DECAY,
        "block_len": BLOCK_LEN,
        "degraded_win_scale_g": g,
        "power_watch_within_horizon": cross_watch / n_paths,
        "power_decay_within_horizon": cross_decay / n_paths,
        "median_trades_to_decay": float(np.median(detect_idx)) if detect_idx else None,
    }


def find_degraded_E1(trades_df, R: np.ndarray) -> dict:
    """DP-2: locate H1 = the degraded expectancy whose DECAYED region is
    strictly outside the in-sample envelope.

    Primary anchor: win_scale g* where the Guardian-SOLO MC bust-rate first
    crosses the lock gate (1%). Floor anchor: the in-sample windowed-R p1
    (a degradation no milder than the worst in-sample window). H1 takes the
    BINDING (lower-expectancy) of the two.
    """
    # in-sample windowed-R p1 (over WINDOW_FOR_P1-trade windows)
    w = WINDOW_FOR_P1
    if R.size >= w:
        win_means = np.array([R[i:i + w].mean() for i in range(R.size - w + 1)])
        windowed_p1 = float(np.percentile(win_means, 1))
    else:
        windowed_p1 = float(R.mean())

    # scan win_scale downward to find the lock-gate breach
    lock_E1 = None
    lock_g = None
    grid = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15, 0.1]
    bust_curve = []
    for g in grid:
        res = guardian_solo_mc(trades_df, win_scale=g)
        bust_curve.append({"win_scale": g, "bust_rate": res["bust_rate"],
                           "p99_dd": res["p99_dd"], "pass_rate": res["pass_rate"]})
        if res["bust_rate"] >= LOCK_BUST_GATE and lock_E1 is None:
            # expectancy at this g
            wins = R[R > 0]
            lock_E1 = float((g * wins.sum() + R[R < 0].sum()) / R.size)
            lock_g = g
    E0 = float(R.mean())
    candidates = {"windowed_p1_R": windowed_p1,
                  "lockgate_E1_R": lock_E1, "lockgate_win_scale": lock_g}
    # binding = the lower expectancy that still sits below in-sample tail
    chosen = windowed_p1 if lock_E1 is None else min(windowed_p1, lock_E1)
    return {"E0_mean_R": E0, "E1_chosen_R": float(chosen),
            "candidates": candidates, "bust_curve": bust_curve}


def main():
    ap = argparse.ArgumentParser(description="Build Guardian-only decay-gate envelope.")
    ap.add_argument("--out", default=str(HERE / "envelope.json"))
    args = ap.parse_args()

    loaded = load_guardian()
    if loaded is None:
        print("NEEDS_DATA: locked Guardian Pepperstone CSV not present at\n"
              f"  {mc.PEPPERSTONE_PANELS['guardian']}\n"
              "This is expected on a public clone / remote container (vendor data is\n"
              "gitignored). Run locally where core/data/tv_exports/pepperstone/ is\n"
              "populated; envelope.json will be written and decay_gate.py can consume it.")
        sys.exit(0)

    trades, r1, R = loaded
    print(f"Loaded Guardian: N={R.size}, 1R=${r1:,.2f}")

    dist = r_distribution(R)
    print(f"E0 (mean R) = {dist['E0_mean_R']:+.3f}  WR={dist['win_rate']:.2%}  "
          f"avg_win={dist['avg_win_R']:+.2f}R  avg_loss={dist['avg_loss_R']:+.2f}R")

    print("Guardian-solo MC envelope (this may take a minute)...")
    base = guardian_solo_mc(trades, win_scale=1.0)
    print(f"  pass={base['pass_rate']:.4f}  bust={base['bust_rate']:.4f}  "
          f"p99_dd={base['p99_dd']:.4f}")

    print("Locating degraded alternative H1 (DP-2)...")
    h1 = find_degraded_E1(trades, R)
    print(f"  E1_chosen = {h1['E1_chosen_R']:+.3f}R  "
          f"(windowed_p1={h1['candidates']['windowed_p1_R']:+.3f}, "
          f"lockgate_E1={h1['candidates']['lockgate_E1_R']})")

    print("Calibrating CUSUM boundaries (DP-1/DP-3)...")
    cal = calibrate_cusum(R, dist["E0_mean_R"], h1["E1_chosen_R"])
    print(f"  k={cal['k_reference_R']:+.3f}  h_watch={cal['h_watch']:.2f}  "
          f"h_decay={cal['h_decay']:.2f}  "
          f"decay-power={cal['power_decay_within_horizon']:.2%} over "
          f"{cal['eval_horizon_in_regime_trades']} in-regime trades  "
          f"(median detect {cal['median_trades_to_decay']})")

    envelope = {
        "_meta": {
            "brief": "Q-GUARDIAN-DECAY-1",
            "panel": mc.PEPPERSTONE_PANELS["guardian"].name,
            "implied_1r_dollars": r1,
            "dd_protection": {"trigger": mc.DD_TRIGGER, "scale": mc.DD_SCALE},
            "seeds": list(mc.SEEDS),
            "sims_per_seed": mc.SIMS_PER_SEED,
            "note": "Guardian-SOLO MC via core/portfolio_mc machinery; no core/ edits.",
        },
        "r_distribution_null_H0": dist,
        "mc_envelope_in_sample": base,
        "degraded_alternative_H1": h1,
        "cusum_calibration": cal,
    }
    out = Path(args.out)
    out.write_text(json.dumps(envelope, indent=2))
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
