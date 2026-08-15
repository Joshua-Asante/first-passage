"""Realistic-granularity EOD-vs-intraday-honest extension of this study.

harness.py / run_validation.py validate simulate_path against g_d(h,mu,sigma,T)
in the FINE-grid limit -- n_steps=2000-5000 substeps standing in for the
horizon, i.e. they test whether the engine's discrete barrier-crossing
arithmetic converges to continuous theory as step count grows. That is an
engine-fidelity check, and it passes (RESULTS.md: all four grid cells AGREE,
mean_signed_err +0.0048).

This script asks a different, complementary question: at the granularity the
repo ACTUALLY uses for reporting bust rates -- one barrier test per real
BUSINESS DAY, horizon ~20-60 days, not 2000-5000 fine substeps -- how much of
a lower bound is the EOD-only convention relative to (a) Tradeify's own
documented rule (EOD-anchored floor, continuously-tested breach -- exactly
what simulate_path's `intraday_low` parameter models) and (b) g_d itself
(pure continuous-peak drawdown, a looser upper-bound reference)?

`intraday_low` is fed an EXACT sample of each day's continuous-time minimum
via the Brownian-bridge reflection formula: given a day's realized P&L x
(diffusion sigma, any drift -- conditioning on the endpoint removes the
bridge's drift-dependence, a standard fact), the minimum over that day has
CDF P(min <= y) = exp(-2y(y-x)/sigma^2) for y <= min(0,x). Inverting gives an
exact sample, not a fine-grid approximation:
  y = [x - sqrt(x^2 - 2*sigma^2*ln(U))] / 2,  U ~ Uniform(0,1)
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from closed_form import g_d  # noqa: E402
from harness import S0, firm_kwargs_absolute_trail  # noqa: E402

_ROOT = Path(__file__).resolve().parents[4]
for _p in (_ROOT, _ROOT / "core"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
from mc.simulation import simulate_path  # noqa: E402

OUT_JSON = _HERE / "intraday_realistic_grid_raw.json"


def sample_bridge_min(x: np.ndarray, sigma: float, rng: np.random.Generator) -> np.ndarray:
    """Exact sample of min_{0<=s<=1} of a diffusion-sigma path from 0 to x
    over one day. Returns values <= min(0, x), i.e. <= 0 always -- matches
    simulate_path's `intraday_low` contract (excursion below opening equity).
    """
    u = rng.uniform(1e-300, 1.0, size=x.shape)
    disc = x**2 - 2.0 * (sigma**2) * np.log(u)
    disc = np.maximum(disc, 0.0)
    return (x - np.sqrt(disc)) / 2.0


def run_case(mu: float, sigma: float, h: float, horizon: int, n_sims: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    kwargs_common = firm_kwargs_absolute_trail(h, S0)

    bust_eod = 0
    bust_continuous = 0
    for _ in range(n_sims):
        pnl_path = rng.normal(mu, sigma, size=horizon)
        path = pnl_path.reshape(horizon, 1)

        outcome_eod, *_ = simulate_path(path, 999.0, 1.0, horizon, **kwargs_common)
        if outcome_eod == "bust_trailing":
            bust_eod += 1

        intraday_low = sample_bridge_min(pnl_path, sigma, rng)
        outcome_cont, *_ = simulate_path(
            path, 999.0, 1.0, horizon, intraday_low=intraday_low, **kwargs_common
        )
        if outcome_cont == "bust_trailing":
            bust_continuous += 1

    p_eod = bust_eod / n_sims
    p_cont = bust_continuous / n_sims
    g_theory = g_d(h, mu, sigma, float(horizon))

    def ci95(p: float) -> float:
        return 1.96 * np.sqrt(p * (1 - p) / n_sims)

    return {
        "mu": mu, "sigma": sigma, "h": h, "horizon": horizon, "n_sims": n_sims,
        "p_eod": p_eod, "p_eod_ci95": ci95(p_eod),
        "p_continuous_mc": p_cont, "p_continuous_mc_ci95": ci95(p_cont),
        "g_theory": g_theory,
        "eod_over_continuous_mc": p_eod / p_cont if p_cont > 0 else float("nan"),
        "continuous_mc_over_theory": p_cont / g_theory if g_theory > 0 else float("nan"),
    }


CASES = [
    ("no edge, 20d", 0.0, 400.0, 20),
    ("no edge, 40d", 0.0, 400.0, 40),
    ("modest edge, 20d", 40.0, 400.0, 20),
    ("modest edge, 40d", 40.0, 400.0, 40),
    ("modest edge, 60d", 40.0, 400.0, 60),
]
H = 3_000.0  # Tradeify Select 100K's real trail (core/firm_rules.py Tradeify_Select_100K)
N_SIMS = 40_000
SEED = 20260813


def main() -> int:
    t0 = time.perf_counter()
    print("=== Realistic-granularity EOD vs intraday-honest-MC vs g_d(theory) ===", flush=True)
    print(f"{'case':<20}{'horizon':>8}{'P(EOD)':>10}{'P(cont-MC)':>12}{'g_theory':>10}"
          f"{'EOD/cont':>10}{'cont/theory':>13}", flush=True)
    rows = []
    for label, mu, sigma, horizon in CASES:
        r = run_case(mu, sigma, H, horizon, N_SIMS, SEED)
        r["label"] = label
        rows.append(r)
        print(f"{label:<20}{horizon:>8}{r['p_eod']:>10.4%}{r['p_continuous_mc']:>12.4%}"
              f"{r['g_theory']:>10.4%}{r['eod_over_continuous_mc']:>10.2%}"
              f"{r['continuous_mc_over_theory']:>13.2%}", flush=True)

    ratios = [r["eod_over_continuous_mc"] for r in rows]
    payload = {
        "cases": rows,
        "eod_over_continuous_mc_range": [min(ratios), max(ratios)],
        "elapsed_s": time.perf_counter() - t0,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nEOD/continuous-MC range: {min(ratios):.1%} - {max(ratios):.1%}", flush=True)
    print(f"wrote {OUT_JSON} ({payload['elapsed_s']:.1f}s total)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
