**Theme:** legacy
**Status:** ACTIVE — US500 widest-net edge discovery results
# US500 widest-net edge discovery — RESULTS (2026-06-22)

**Mandate (operator-directed):** design a US500 strategy tailored to the bar data that
exploits edge within FXIFY's firm rules; *disregard prior attempts / portfolio fit; find
edge in the given data.* Deliverable = "both as a frontier" (best durable edge + how far
the structure pushes pure pass-rate), widest-net search.

**Data:** `BAR_EXPORT_v0.1_PEPPERSTONE_US500_2026-06-22_f9fa5.csv` — 15m OHLCV, Pepperstone
US500 CFD, 2022-01-03 → 2026-06-21, **105,473 bars / 1,151 RTH days**. Step-0 integrity
**PASS** (balanced {0,15,30,45} minute census; no dups; no bad OHLC; tick 0.1pt; price
3499.8→7621.3; daily 75-min maintenance halt + weekend/holiday gaps expected). epoch=UTC,
ET-converted DST-aware. Harness: `harness.py`; characterization: `characterize.py`;
probes: `probes.py`; verification: workflow `wf_c5fd6ce6-b11` (5 agents).

## Verdict — NO ROBUST STANDALONE EDGE

The wide net reproduces the instrument's heavy negative prior. The single structurally-real
survivor (opening-range breakout) is **not tradeable** once realistic entry fills and honest
multiplicity are charged. No first-passage MC on a deployable edge is warranted.

| Family | Mechanism | Result | Killer |
|---|---|---|---|
| Overnight close→open | overnight risk premium | **DEAD** | +1.35bps gross → **−4.6bps net (t=−2.36)**; asymmetric long swap (−1.4pt/night) taxes it away |
| Intraday drift | RTH open→close long | weak | +2.5bps gross / **+0.5bps net (t=0.20)**; not standalone |
| Intraday momentum (GHLZ) | first-30m → last-30m | **FAILS** | −0.027R, perm p=0.83 |
| Intraday reversion | morn→aft fade | **FAILS** | negative, unstable |
| Gap fade / continuation | overnight gap | **FAILS** | halves sign-flip; rho_gap_id −0.077 not tradeable |
| Morning→afternoon continuation | intraday momentum tilt | MARGINAL | +0.047R but ~half-beta (down-mornings barely reverse, +0.019R) |
| VWAP reversion | fade midday stretch | **FAILS (anti-edge)** | −0.33R, all 5 yrs negative — midday stretch *continues* |
| VWAP trend / volume-confirm | hold above rising VWAP / vol gate | **FAILS** | trend = 2022 artifact (halves-flip); volume-confirm destructive (U-shaped volume) |
| Trend-day Donchian / CLV / range-exp | momentum/trend capture | **DEAD** | best +0.139R but t=0.80, Bonferroni→1.0; 2024-bear/short-side artifact, *negative* 2025+2026 |
| **Opening-range breakout (ORB-30)** | first-30m range break, stop=opp extreme, exit@close | **MARGINAL→not tradeable** | see below |

## The ORB-30 story (the one that looked real)

Touch-fill backtest (cost-net 1pt RT, risk=range, exit@close → no swap): n=1149, **meanR
+0.0580, t +1.35**, WR 0.419, PF 1.107, skew +1.76; **all 5 years positive** (22:+.125
23:+.067 24:+.012 25:+.041 26:+.031); **both sides positive** (long +.069 / short +.047 →
direction-agnostic, *not* beta — the short side makes money fighting a bull market). The
within-day **placebo null clears (p=0.0123)**: the *opening* range is genuinely special vs
arbitrary intraday windows. Regime-robust (hi/lo trailing-vol both +). This is a **real
structural effect.**

It is nonetheless **not a tradeable edge:**
1. **Fill cliff (decisive).** The whole +0.058R lives in the 1-point band between the OR
   level and level+1pt on an 18.8pt median range. Cost-net meanR vs entry slippage:
   `+0.058 / +0.042 / +0.026 / +0.010 / −0.006 / −0.037` at slip `0 / .25 / .5 / .75 / 1.0 / 1.5`pt.
   **Crosses zero at ~0.9pt** — less than one realistic tick of stop-order slippage. (`us500_orb_verdict.png` panel B.)
2. **Cliff, not plateau.** Only OR=30min is all-years-positive; 15min is *negative*, 45/60/75
   decay and lose year-robustness. The "more range filters false breaks" mechanism is falsified.
   30min is a hand-landed needle.
3. **Best-of-K.** t=1.35 is rank-1 of 10 ORB configs, but a zero-edge panel yields best-of-10
   t≥1.35 **31% of the time** (p=0.31). The magnitude is selection noise.
4. **Standalone first-passage ceiling ~58%** at 0.75% risk (even on the optimistic touch fill),
   with 31–45% bust and p99 DD 7–13% — a coin-flip-plus, nowhere near lock quality
   (bust<1%, p99 DD<5%). (`us500_orb_verdict.png` panel A.)

## Frontier deliverable (as requested)

- **Durable edge:** none clears the bar. ORB is the best candidate and it is MARGINAL-real
  but fails realistic-fill + multiplicity. Not deployable, not lockable.
- **Pure pass-rate:** the structure can be pushed to ~80% pass (give-back-33% exit, fair
  vol-normalized sizing to the 2% 1R cap) — **but only on the touch-fill assumption.** With
  realistic fills the entry is negative, so the true standalone pass-rate is ~50%. The frontier
  exists only on the optimistic side of the fill cliff.

## Transferable findings (the positive yield of a null)

- **F-US500-A — FXIFY is a Sharpe race with a deadline, not a symmetric first-passage.** Exit
  sweep: a give-back-33%-of-open-profit trailing exit (WR 0.755, PF 1.56, std 0.49) dominates
  a max-skew lottery exit (breakeven@+0.5R, skew +2.52) for the 120-day-capped challenge —
  information ratio + speed beat right-tail skew. Applies to any challenge strategy incl. the
  locked legs. (`orb30_exit_sweep.py`)
- **F-US500-B — the overnight equity-risk-premium is dead-by-swap on FXIFY US500.** The
  asymmetric long financing (−1.4pt/night) erases the (already-insignificant) overnight drift.
  Any long-biased multi-session US500 design carries this tax; short overnight earns +0.28pt but
  fights the drift. Standing negative prior.
- **F-US500-C — volume confirmation is destructive on US500** (intraday volume is strongly
  U-shaped; trailing-median gates select only open bars). Re-proposal needs same-tod-normalized z-scores.
- **F-US500-D — cost is NOT the binding constraint** (1pt RT on a 9.9pt ATR → hurdle ~0.07R).
  The binding constraint is edge scarcity. Unlike USDCAD, US500 intraday is cheap to trade.
- **F-US500-E — the opening-range structure is real but sub-cost** (placebo p=0.012). A genuine
  micro-effect that the 1pt cost/slip band swamps; not resurrectable by OR-length re-tuning.

## What a real US500 edge would require (re-proposal bar)

Consistent with the prior catalog closures (Q-SPX-F09 / Q-NAS-4 / D1-D3): the OHLC-only
intraday/daily anomaly space is now broadly exhausted (10+ families across 2 sessions). A
re-proposal should bring **exogenous state not in the OHLC** — VIX term-structure / options
flow / dealer-gamma, a macro-event calendar (FOMC/CPI day conditioning, untested here because
no event calendar is in the bar data), or **cross-sectional / multi-instrument** structure
(US500 vs DJ30/NAS100 dispersion) to beat the single-setup frequency-starvation that caps
standalone first-passage. A re-tuned OHLC parameter search returns the same null.

## Disposition

US500/SPX500: **6th distinct family-null context** (overnight-premium · intraday-momentum ·
intraday-reversion · gap · VWAP/volume · trend-day) added to the prior 4. ORB recorded as
MARGINAL-real-but-not-tradeable (fill-cliff + best-of-K), **not** a powered directional null but
a closed candidate. No `core/` change, no lock/allocation/dd_protection change, no Pine authored.
