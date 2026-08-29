"""Candidate 1 -- daily-range-state-persistence x MYM (conditioner-role, no entry claim).

Does session TR sitting in the trailing top quintile (P80, strictly prior 60 sessions)
predict elevated NEXT-session TR (> trailing median, through-today 60 sessions)?
Same series, same construction as the frozen GC/CL battery (S1 role) -- reused verbatim
in shape, run at M=200 (see iaaft_battery.py header for the disclosed lighter-weight
deviation from the frozen M=1000).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from load_sessions import load_bars, session_ohlc, wilder_tr
import iaaft_battery as B

HERE = Path(__file__).resolve().parent
WINDOW, Q_BIAS, Q_REF = 60, 0.80, 0.50
CI_BLOCK, CI_DRAWS, CI_SEED = 60, 4000, 42
N_FLOOR_POP, N_FLOOR_COND = 400, 100
M, SEED_BASE, CODE = 200, 20260829, 3  # MYM code=3 (GC=1,CL=2 burned in the frozen spec)


def main():
    bars = load_bars()
    full = session_ohlc(bars)
    full = full[full["n_bars"] >= 20]  # drop the trailing truncated partial session
    tr = wilder_tr(full).dropna().to_numpy()
    n = len(tr)
    print(f"sessions: {len(full)}  valid TR: {n}")

    obs, bias, y, scored = B.conditional_hit_rate_next(tr, tr, WINDOW, Q_BIAS, Q_REF)
    n_cond = int(np.nansum(bias[scored] == 1)) if scored.any() else 0
    b_s, y_s = bias[scored].astype(int), y[scored].astype(int)
    n_cond = int((b_s == 1).sum())
    n_pop = int(scored.sum())
    print(f"population n={n_pop}  conditional n={n_cond}  obs(P(y=1|bias=1))={obs:.4f}")

    lo, hi, n_valid_boot = B.block_bootstrap_ci(b_s, y_s, CI_BLOCK, CI_DRAWS, CI_SEED)
    h1, h2 = B.halves(b_s, y_s)
    print(f"CI=[{lo:.4f},{hi:.4f}]  halves=({h1:.4f},{h2:.4f})")

    surrogates, diag = B.generate_surrogates(tr, M, SEED_BASE, CODE)
    print(f"diagnostic gate: {diag['gate']}  med={diag['med']:.4f} p95={diag['p95']:.4f}")

    out = dict(candidate=1, n_pop=n_pop, n_cond=n_cond, obs=obs, ci=[lo, hi],
               halves=[h1, h2], diagnostics=diag)

    if diag["gate"] != "PASS":
        out["VERDICT"] = "VOID (diagnostic gate FAIL)"
        (HERE / "c1_results.json").write_text(json.dumps(out, indent=2))
        print("VERDICT:", out["VERDICT"])
        return

    rates = []
    for s in surrogates:
        r, _, _, _ = B.conditional_hit_rate_next(s, s, WINDOW, Q_BIAS, Q_REF)
        rates.append(r)
    rates = np.array(rates)
    p_upper = (1 + int((rates >= obs).sum())) / (M + 1)
    p_lower = (1 + int((rates <= obs).sum())) / (M + 1)
    pct = float((rates < obs).mean() * 100)
    print(f"surrogate band: mean={rates.mean():.4f} p5={np.percentile(rates,5):.4f} "
          f"p50={np.percentile(rates,50):.4f} p95={np.percentile(rates,95):.4f}")
    print(f"p_upper={p_upper:.4f}  p_lower={p_lower:.4f}  obs at {pct:.1f}th pct of band")

    l1 = n_pop >= N_FLOOR_POP and n_cond >= N_FLOOR_COND
    l2 = lo > 0.50
    l3 = h1 > 0.50 and h2 > 0.50
    presence = l1 and l2 and l3
    if presence:
        verdict = "SIGNAL-EXCESS" if p_upper <= 0.05 else "SIGNAL-GENERIC"
    else:
        driving = [k for k, v in (("L1", l1), ("L2", l2), ("L3", l3)) if not v]
        verdict = f"NULL (driving: {','.join(driving)})"
    flags = []
    if p_lower <= 0.05:
        flags.append("SUB-LINEAR")
    if 0.03 <= p_upper <= 0.07:
        flags.append("ATTRIBUTION-FRAGILE")

    out.update(dict(
        band=dict(mean=float(rates.mean()), pct=[float(np.percentile(rates, q)) for q in (2.5, 5, 50, 95, 97.5)]),
        p_upper=p_upper, p_lower=p_lower, obs_percentile=pct,
        limbs=dict(L1_n_floor=l1, L2_ci_lb=l2, L3_halves=l3),
        VERDICT=verdict, flags=flags,
    ))
    (HERE / "c1_results.json").write_text(json.dumps(out, indent=2))
    print("VERDICT:", verdict, flags)


if __name__ == "__main__":
    main()
