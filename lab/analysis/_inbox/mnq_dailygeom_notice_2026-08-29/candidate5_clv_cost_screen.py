"""$0 cost-law pre-screen for MNQ candidate 5 (CLV lag-1 autocorrelation),
per docs/adr/2026-08-29-clv-autocorrelation-admission-route-scope.md 2-C.

Converts rho into a decile-conditioned implied gross edge, expressed directly
in bp/event using REAL forward price returns (not a CLV-to-CLV proxy, which
would need an extra, undisclosed assumption about how a next-bar CLV value
maps to price direction -- see this script's own docstring note below).
Checks the result against MNQ's own N6 cost hurdle.

Design (connecting arithmetic, not borrowed): CLV_t in an extreme decile is
the entry signal; the forward 1-bar return close_t -> close_{t+1} is the
thing actually priced in bp -- not CLV_{t+1}'s own value, which describes
WHERE bar t+1 closed within ITS OWN range, not whether close_{t+1} is above
or below close_t. Measuring forward RETURN directly, conditioned on CLV_t's
decile, is the correct (and simpler) translation of "does this bar-shape
statistic carry economically actionable information" -- it sidesteps needing
an assumption to bridge CLV_{t+1} back to a price level.

Fade-rule construction: whichever direction the DATA shows (top-decile
excess return sign, bottom-decile excess return sign) sets the trade
direction for that decile -- not assumed from candidate5's rho sign a
priori (that would be a D-test: assuming the sign that makes the strategy
work before looking, per this repo's own D-S-A discipline).

Deciles are UNCONDITIONAL (whole-sample percentile thresholds on CLV_t),
not a rolling causal reference -- appropriate for a $0 screening tool per
the standing lesson `lesson_cost_law_pre_screen_mr_fade` ("a 5-minute
geometry calculation kills it before any harness is built"), not a
deployable backtest. A future full construct would need a causal
(look-ahead-free) percentile reference; this pre-screen does not license
skipping that step if it proceeds to Route 1/3.

N6 basis check (unit note, load-bearing): MNQ's own N6 cost hurdle is
labeled "bp/session" in MNQ.md, but `cost_mnq.py`'s own `hurdle_from_price`
computes it as `4 x (one round-trip's commission+slippage) / notional` --
a per-TRADE figure that happens to be called "/session" only because the
original Baltussen momentum construct it was built for trades once per
session (D5-RECOST-1 scoping doc, re-verified this session). Since this
screen's own fade rule is also exactly one round-trip per qualifying event,
N6 is unit-comparable to this script's bp/event figure directly -- no
frequency rescaling needed for the necessary-condition floor check itself.
Event FREQUENCY (qualifying bars/session) is disclosed separately because a
real multi-times-per-day construct's aggregate daily cost would scale with
it -- that is a full-construct question, out of scope for this floor check.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from data_lib import load_raw  # noqa: E402

N6_HURDLE_BP = 3.01
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
    df = load_raw().reset_index(drop=True)
    hi_, lo_, cl, op = (df["high"].to_numpy(), df["low"].to_numpy(),
                        df["close"].to_numpy(), df["open"].to_numpy())
    rng_bar = hi_ - lo_
    degenerate = rng_bar == 0
    print(f"degenerate H==L bars: {int(degenerate.sum())} / {len(df)}")
    clv = np.where(~degenerate, (cl - lo_) / np.where(~degenerate, rng_bar, 1.0), np.nan)

    # forward 1-bar return close_t -> close_{t+1}, in bp
    fwd_ret_bp = np.full(len(df), np.nan)
    fwd_ret_bp[:-1] = (cl[1:] - cl[:-1]) / cl[:-1] * 10000.0

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

    # fade-rule direction set BY THE DATA (not assumed): short top decile if
    # its excess return is negative, long bottom decile if its excess return
    # is positive -- i.e., trade the sign that would have made money.
    top_dir = -1.0 if lift_top < 0 else 1.0
    bot_dir = 1.0 if lift_bot > 0 else -1.0
    # Fixed 2026-08-30 (Codex review, PR #219): concatenating all top-decile
    # events followed by all bottom-decile events destroyed their original
    # chronological order before block-bootstrapping -- for serially
    # dependent M15 bars, a block=96 window drawn from either half no longer
    # approximates any real time span (most of a block shares one signal
    # type; neighboring elements can be years apart). Building one
    # chronologically-ordered signed-event series (boolean masking preserves
    # original array order) instead means block=96 now spans 96 consecutive
    # QUALIFYING EVENTS in their real occurrence order, not 96 consecutive
    # bars -- a real semantic shift, disclosed here rather than silently
    # kept: at ~20% event frequency, 96 events span roughly 480 real bars
    # (~5 sessions), not the ~1-session span the block size was originally
    # chosen to approximate on a full bar-indexed series.
    event_mask = top_mask | bot_mask
    signed_dir = np.zeros(n, dtype=float)
    signed_dir[top_mask] = top_dir
    signed_dir[bot_mask] = bot_dir
    combined = signed_dir[event_mask] * (r[event_mask] - mu_base)
    n_events = len(combined)
    freq = n_events / n
    mean_edge = float(combined.mean())
    lo, hi, boot_mean = block_bootstrap_mean_ci(combined, CI_BLOCK, CI_DRAWS, SEED)
    print(f"\nfade-rule direction: top_dir={top_dir:+.0f} (short if -1) bot_dir={bot_dir:+.0f} (long if +1)")
    print(f"combined implied gross edge: mean={mean_edge:+.4f} bp/event  "
          f"95% CI=[{lo:+.4f},{hi:+.4f}]  n_events={n_events}  event_freq={freq:.4f} of bars")
    print(f"\nN6 cost hurdle (MNQ, 4x round-trip cost, unit-comparable per this script's own "
          f"docstring): {N6_HURDLE_BP} bp")
    clears = mean_edge > N6_HURDLE_BP and lo > 0
    print(f"CLEARS N6 floor (mean edge > hurdle AND CI lower bound > 0): {clears}")

    out = dict(
        n_scored=n, p10=float(p10), p90=float(p90),
        mu_base=mu_base, mu_top=mu_top, mu_bot=mu_bot, n_top=n_top, n_bot=n_bot,
        lift_top_bp=lift_top, lift_bot_bp=lift_bot,
        fade_rule=dict(top_dir=top_dir, bot_dir=bot_dir),
        implied_gross_edge_bp_per_event=dict(mean=mean_edge, ci=[lo, hi], n_events=n_events,
                                              event_freq=freq, block=CI_BLOCK, draws=CI_DRAWS, seed=SEED),
        n6_hurdle_bp=N6_HURDLE_BP,
        clears_n6_floor=bool(clears),
        note="necessary-condition cost-FLOOR check only, per ADR 2-C -- does not by itself "
             "license a Pre-Q; full Route 3 comparison needs an actual entry/exit construct's own R",
    )
    (HERE / "candidate5_clv_cost_screen_results.json").write_text(json.dumps(out, indent=2, default=str))
    print(f"\nWrote candidate5_clv_cost_screen_results.json")


if __name__ == "__main__":
    main()
