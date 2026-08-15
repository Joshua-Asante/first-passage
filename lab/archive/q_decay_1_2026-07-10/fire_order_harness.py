#!/usr/bin/env python3
"""
Q-DECAY-1 synthetic fire-order harness (FEASIBILITY-LIMITED).
=============================================================
Compares, per scope, the fire-order of two detectors under injected edge decay:
  (A) CANDIDATE = the Guardian decay-gate CUSUM (real ``DecayGate``, run
      UNCONDITIONED so the reachable state is WATCH — the PnL-only limb; DECAYED
      is classifier-interlocked OFF by DP-4). Detects an EXPECTANCY shift.
  (B) REFERENCE ("expensive detector") = dd_protection engaging on portfolio
      drawdown-from-peak, using the REAL DD_TRIGGER / DD_SCALE constants and the
      exact production engage rule from ``_simulate_path``. Detects a LOSS.

FEASIBILITY LIMIT (§0.5-B): the locked Pepperstone panels are gitignored and
ABSENT in this worktree (Rule 9) -> build_envelope.py hits NEEDS_DATA. So this
drives the REAL machinery with SYNTHETIC per-trade R streams calibrated to the
DOCUMENTED per-leg summary stats (baselines.md: WR / PF / 1R / N / active days).
Fire-ORDER and structural conclusions are calibration-robust; absolute sim-week
magnitudes are illustrative. Panel-calibrated numbers: run build_envelope.py
locally where the panels exist.

NOT a detector; NOT wired to execution; core/ imported READ-ONLY.
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve()
for p in [REPO] + list(REPO.parents):
    if (p / "core" / "portfolio_mc.py").exists():
        REPO_ROOT = p
        break
else:
    REPO_ROOT = Path(r"C:\Users\joshu\multi_firm_operations\.claude\worktrees\q-decay-1-detector-78c5fc")

sys.path.insert(0, str(REPO_ROOT / "core"))
from dd_protection import DD_TRIGGER, DD_SCALE  # noqa: E402  (REAL production constants)


def _load_by_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


GATE_DIR = REPO_ROOT / "lab" / "analysis" / "guardian_decay_gate_2026-06-25"
DecayGate = _load_by_path("decay_gate", GATE_DIR / "decay_gate.py").DecayGate
calibrate_cusum = _load_by_path("build_envelope", GATE_DIR / "build_envelope.py").calibrate_cusum

# ── documented per-leg calibration (baselines.md) ───────────────────────────
# E0 (mean R, full-stop normalized, avg_loss=-1R) = (1-WR)(PF-1); reproduces
# Guardian's documented +2.14R. 1R$ = alloc x $200K (implied_1r target).
ACCOUNT = 200_000.0
LEGS = {
    #                 WR      PF     alloc    N    active weekdays (0=Mon)
    "guardian":       dict(wr=0.2217, pf=3.750, alloc=0.0034, n=203, days=(0, 1, 3)),
    "striker":        dict(wr=0.7294, pf=3.373, alloc=0.0070, n=218, days=(1, 4)),
    "striker_nas100": dict(wr=0.5561, pf=3.717, alloc=0.0037, n=196, days=(0, 1)),
    "aegis":          dict(wr=0.6048, pf=4.188, alloc=0.0150, n=124, days=(0, 1, 2)),
}
N_WEEKS = 228
DECAY_ONSET_WK = 100
RAMP_WEEKS = 40
# win-haircut endpoints per shock (positive-R mass scaled by g):
SHOCK_G = {"step50": 0.50, "ramp50": 0.50, "kill": 0.06, "none": 1.0}
# g=0.06 drives Guardian E0 ~ +2.14R -> ~ -0.5R (genuine edge death: portfolio erodes)


def leg_stats(cfg):
    wr, pf = cfg["wr"], cfg["pf"]
    return wr, pf * (1.0 - wr) / wr, cfg["alloc"] * ACCOUNT  # wr, avg_win_R, 1R$


def gen_trades(cfg, rng):
    """Exactly N documented trades, each placed on a random active (week, day).
    Returns arrays sorted chronologically: week, day, R, is_win."""
    wr, avg_win_R, _ = leg_stats(cfg)
    n = cfg["n"]
    is_win = rng.random(n) < wr
    R = np.where(is_win, rng.exponential(avg_win_R, n), -(0.6 + 0.8 * rng.random(n)))
    wk = rng.integers(0, N_WEEKS, n)
    day = np.array([cfg["days"][i] for i in rng.integers(0, len(cfg["days"]), n)])
    order = np.lexsort((day, wk))
    return wk[order], day[order], R[order], is_win[order]


def decayed_R(wk, R, is_win, shock):
    if shock == "none":
        return R.copy()
    g_end = SHOCK_G[shock]
    out = R.copy()
    for i in range(len(R)):
        if wk[i] < DECAY_ONSET_WK or not is_win[i]:
            continue
        if shock == "step50" or shock == "kill":
            g = g_end
        else:  # ramp
            frac = min(1.0, (wk[i] - DECAY_ONSET_WK) / RAMP_WEEKS)
            g = 1.0 - frac * (1.0 - g_end)
        out[i] = R[i] * g
    return out


def build_envelope(rng):
    # Calibrate on a LARGE synthetic reference so E0_hat -> analytic E0 and the
    # reference k is stable across seeds. (The real build_envelope.py calibrates
    # and measures on the SAME 203-trade panel, so k is internally consistent
    # there; a single 203-draw here would instead decouple calibration from the
    # fresh eval draws and make the reference k -- hence the WATCH false-positive
    # baseline -- seed-fragile. Q-DECAY-1 quality review C1.)
    cfg = {**LEGS["guardian"], "n": 20000}
    R_is = gen_trades(cfg, rng)[2]
    E0 = float(R_is.mean())               # -> analytic (1-WR)(PF-1) = +2.14R
    cal = calibrate_cusum(R_is, E0, E0 * 0.5, n_paths=3000, horizon=200)
    return {"cusum_calibration": cal,
            "r_distribution_null_H0": {"E0_mean_R": E0},
            "degraded_alternative_H1": {"E1_chosen_R": E0 * 0.5}}


def one_path(shock, scope, envelope, rng):
    daily = np.zeros(N_WEEKS * 5)
    guard_stream = []  # chronological (week, R) for the CUSUM
    for name, cfg in LEGS.items():
        wk, day, R, is_win = gen_trades(cfg, rng)
        decays = (scope == "common") or (scope == "perleg" and name == "guardian")
        Rd = decayed_R(wk, R, is_win, shock if decays else "none")
        r1 = leg_stats(cfg)[2]
        for i in range(len(R)):
            daily[wk[i] * 5 + day[i]] += Rd[i] * r1
            if name == "guardian":
                guard_stream.append((int(wk[i]), float(Rd[i])))

    # single dd_protection'd equity walk (REAL rule + REAL constants) ----------
    eq = peak = ACCOUNT
    ddp_week = None
    weekly_dd = np.zeros(N_WEEKS)
    max_dd = 0.0
    for day_i, base in enumerate(daily):
        dd_from_peak = (eq - peak) / peak if peak > 0 else 0.0
        engaged = round(dd_from_peak, 6) <= -DD_TRIGGER
        if engaged and ddp_week is None and day_i >= DECAY_ONSET_WK * 5:
            ddp_week = day_i // 5
        eq += base * (DD_SCALE if engaged else 1.0)
        if eq > peak:
            peak = eq
        cur_dd = (peak - eq) / peak if peak > 0 else 0.0
        max_dd = max(max_dd, cur_dd)
        weekly_dd[day_i // 5] = cur_dd

    # Guardian CUSUM (real DecayGate, UNCONDITIONED -> max state WATCH) ---------
    gate = DecayGate(envelope, classifier_validated=False)
    watch_week = None
    for wk, r in guard_stream:
        prev = gate.s.state
        gate.update(r, favorable=True, when=str(wk))
        if prev == "ARMED" and gate.s.state == "WATCH" and watch_week is None and wk >= DECAY_ONSET_WK:
            watch_week = wk

    return dict(
        watch_week=watch_week,
        watch_dd=(weekly_dd[watch_week] if watch_week is not None else None),
        ddp_week=ddp_week,
        ddp_dd=(weekly_dd[ddp_week] if ddp_week is not None else None),
        max_dd=max_dd,
        final_eq=eq,
    )


def med(xs):
    xs = [x for x in xs if x is not None]
    return float(np.median(xs)) if xs else None


def summarize(res, label, control_watch_rate=None):
    n = len(res)
    watch = [r for r in res if r["watch_week"] is not None]
    ddp = [r for r in res if r["ddp_week"] is not None]
    both = [r for r in res if r["watch_week"] is not None and r["ddp_week"] is not None]
    cusum_first = np.mean([r["watch_week"] < r["ddp_week"] for r in both]) if both else None
    print(f"\n=== {label}  (n={n}) ===")
    wr_rate = len(watch) / n
    lift = f"  (control {control_watch_rate:.0%}; lift {wr_rate-control_watch_rate:+.0%})" if control_watch_rate is not None else ""
    print(f"  [A] CUSUM->WATCH : fired {wr_rate:.0%}{lift}; "
          f"median wk onset+{med([r['watch_week'] for r in watch])-DECAY_ONSET_WK if watch else 'NA'}; "
          f"portfolio DD at crossing = {100*med([r['watch_dd'] for r in watch]):.2f}%" if watch
          else f"  [A] CUSUM->WATCH : fired {wr_rate:.0%}{lift}")
    if ddp:
        print(f"  [B] dd_protection: engaged {len(ddp)/n:.0%} of paths post-onset; "
              f"median wk onset+{med([r['ddp_week'] for r in ddp])-DECAY_ONSET_WK}; "
              f"portfolio DD at engage = {100*med([r['ddp_dd'] for r in ddp]):.2f}% (~{DD_TRIGGER:.1%} trigger)")
    else:
        print(f"  [B] dd_protection: engaged 0% of paths post-onset (never reached -{DD_TRIGGER:.1%} portfolio DD)")
    print(f"  P(CUSUM-WATCH before dd_protection | both fire) = {round(float(cusum_first),3) if cusum_first is not None else 'NA (dd_protection never fired)'}")
    print(f"  median max portfolio DD over path = {100*med([r['max_dd'] for r in res]):.2f}%; "
          f"median final equity = ${med([r['final_eq'] for r in res]):,.0f}")
    return wr_rate


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paths", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)

    print("Q-DECAY-1 fire-order harness (FEASIBILITY-LIMITED / synthetic inputs, REAL machinery)")
    print(f"Real dd_protection constants: DD_TRIGGER={DD_TRIGGER}  DD_SCALE={DD_SCALE}")
    env = build_envelope(rng)
    c = env["cusum_calibration"]
    print(f"CUSUM (synthetic-Guardian calibrated): k={c['k_reference_R']:+.3f} "
          f"h_watch={c['h_watch']:.1f} h_decay={c['h_decay']:.1f} "
          f"decay-power(200-trade horizon)={c['power_decay_within_horizon']:.0%}")
    print(f"Onset week {DECAY_ONSET_WK}/{N_WEEKS}; shocks: step50 / ramp50(over {RAMP_WEEKS}wk) / kill(g={SHOCK_G['kill']})")

    ctrl = [one_path("none", "perleg", env, rng) for _ in range(args.paths)]
    ctrl_rate = summarize(ctrl, "CONTROL (no decay) — WATCH false-positive baseline")

    for scope in ("perleg", "common"):
        for shock in ("step50", "ramp50", "kill"):
            res = [one_path(shock, scope, env, rng) for _ in range(args.paths)]
            summarize(res, f"scope={scope}  shock={shock}", control_watch_rate=ctrl_rate)


if __name__ == "__main__":
    main()
