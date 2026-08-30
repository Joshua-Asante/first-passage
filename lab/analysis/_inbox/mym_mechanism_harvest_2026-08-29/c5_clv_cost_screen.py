"""$0 cost-law pre-screen for MYM candidate 5 (CLV closing-location autocorrelation),
per docs/adr/2026-08-29-clv-autocorrelation-admission-route-scope.md 2-C.

Same design as the MNQ sibling script
(`lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate5_clv_cost_screen.py`)
-- see that file's docstring for the full connecting-arithmetic rationale
(forward real-return conditioning, not a CLV-to-CLV proxy; data-set fade
direction, not assumed; unconditional whole-sample deciles, $0-screen only).

M6 basis note: MYM's own #M6 cost hurdle is already labeled "bp/event" in
MYM.md (basis: 4x Tradeify hurdle) -- no unit-relabeling ambiguity the way
MNQ's "bp/session"-labeled N6 had. Per the admission-route ADR's own 2-C,
this hurdle is explicitly PROVISIONAL (Tradeify was de-scoped 2026-08-04;
pending re-pricing against whatever successor venue F3 eventually rules) --
a pass or fail here is read "against the last-known basis," not final.

Reuses MYM's own `load_sessions.load_bars` (same loader every other MYM
candidate script in this batch uses), trimming the trailing truncated
session the same way `c3_volume_regime.py` / `c5_closing_location.py` do.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from load_sessions import load_bars

HERE = Path(__file__).resolve().parent
M6_HURDLE_BP = 6.57
M6_PROVISIONAL = True  # Tradeify de-scoped 2026-08-04; pending F3 re-pricing
DECILE = 0.10
CI_BLOCK, CI_DRAWS, SEED = 96, 4000, 20260830


def block_bootstrap_mean_ci(x, block, draws, seed):
    rng = np.random.default_rng(seed)
    n = len(x)
    if n == 0:
        return float("nan"), float("nan"), float("nan")
    nblocks = int(np.ceil(n / block))
    means = []
    for _ in range(draws):
        st = rng.integers(0, n, size=nblocks)
        idx = (st[:, None] + np.arange(block)[None, :]) % n
        idx = idx.ravel()[:n]
        means.append(float(x[idx].mean()))
    means = np.asarray(means)
    lo, hi = np.percentile(means, [2.5, 97.5])
    return float(lo), float(hi), float(means.mean())


def main():
    bars = load_bars()
    bars = bars[bars["session"] < bars["session"].max()]  # drop trailing truncated day, matches c3/c5 siblings
    h, l, c = bars["high"].to_numpy(), bars["low"].to_numpy(), bars["close"].to_numpy()
    n_full = len(bars)
    rng_bar = h - l
    degenerate = rng_bar == 0
    print(f"bars: {n_full}  degenerate H==L: {int(degenerate.sum())}")
    clv = np.where(~degenerate, (c - l) / np.where(~degenerate, rng_bar, 1.0), np.nan)

    fwd_ret_bp = np.full(n_full, np.nan)
    fwd_ret_bp[:-1] = (c[1:] - c[:-1]) / c[:-1] * 10000.0

    ok = (~np.isnan(clv)) & (~np.isnan(fwd_ret_bp))
    x_clv = clv[ok]
    r = fwd_ret_bp[ok]
    n = len(r)
    print(f"scored bars (CLV_t and fwd return both defined): {n}")

    p10, p90 = np.percentile(x_clv, [DECILE * 100, (1 - DECILE) * 100])
    print(f"CLV_t deciles: P10={p10:.4f}  P90={p90:.4f}")

    top_mask = x_clv >= p90
    bot_mask = x_clv <= p10
    mu_base = float(r.mean())
    mu_top = float(r[top_mask].mean())
    mu_bot = float(r[bot_mask].mean())
    n_top, n_bot = int(top_mask.sum()), int(bot_mask.sum())
    lift_top = mu_top - mu_base
    lift_bot = mu_bot - mu_base
    print(f"base rate mean fwd return: {mu_base:+.4f} bp (n={n})")
    print(f"top-decile (CLV>=P90, n={n_top}): mean fwd return {mu_top:+.4f} bp  lift={lift_top:+.4f} bp")
    print(f"bottom-decile (CLV<=P10, n={n_bot}): mean fwd return {mu_bot:+.4f} bp  lift={lift_bot:+.4f} bp")

    top_dir = -1.0 if lift_top < 0 else 1.0
    bot_dir = 1.0 if lift_bot > 0 else -1.0
    top_trade_bp = top_dir * (r[top_mask] - mu_base)
    bot_trade_bp = bot_dir * (r[bot_mask] - mu_base)
    combined = np.concatenate([top_trade_bp, bot_trade_bp])
    n_events = len(combined)
    freq = n_events / n
    mean_edge = float(combined.mean())
    lo, hi, boot_mean = block_bootstrap_mean_ci(combined, CI_BLOCK, CI_DRAWS, SEED)
    print(f"\nfade-rule direction: top_dir={top_dir:+.0f} (short if -1) bot_dir={bot_dir:+.0f} (long if +1)")
    print(f"combined implied gross edge: mean={mean_edge:+.4f} bp/event  "
          f"95% CI=[{lo:+.4f},{hi:+.4f}]  n_events={n_events}  event_freq={freq:.4f} of bars")
    print(f"\nM6 cost hurdle (MYM, 4x Tradeify hurdle, PROVISIONAL={M6_PROVISIONAL}): {M6_HURDLE_BP} bp")
    clears = mean_edge > M6_HURDLE_BP and lo > 0
    print(f"CLEARS M6 floor (mean edge > hurdle AND CI lower bound > 0): {clears}")

    out = dict(
        n_scored=n, p10=float(p10), p90=float(p90),
        mu_base=mu_base, mu_top=mu_top, mu_bot=mu_bot, n_top=n_top, n_bot=n_bot,
        lift_top_bp=lift_top, lift_bot_bp=lift_bot,
        fade_rule=dict(top_dir=top_dir, bot_dir=bot_dir),
        implied_gross_edge_bp_per_event=dict(mean=mean_edge, ci=[lo, hi], n_events=n_events,
                                              event_freq=freq, block=CI_BLOCK, draws=CI_DRAWS, seed=SEED),
        m6_hurdle_bp=M6_HURDLE_BP, m6_provisional=M6_PROVISIONAL,
        clears_m6_floor=bool(clears),
        note="necessary-condition cost-FLOOR check only, per ADR 2-C -- does not by itself "
             "license a Pre-Q; full Route 3 comparison needs an actual entry/exit construct's own R; "
             "M6 basis is provisional (Tradeify de-scoped) per that ADR",
    )
    (HERE / "c5_clv_cost_screen_results.json").write_text(json.dumps(out, indent=2, default=str))
    print(f"\nWrote c5_clv_cost_screen_results.json")


if __name__ == "__main__":
    main()
