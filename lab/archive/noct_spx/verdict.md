# NOCT-SPX-001 — Stage 1+2 verdict: **FALSIFIED**

**Concept:** CONCEPT-NOCT-SPX-001 — Nocturnal inventory-reversal harvest on SPX500
(European-open window 02:00–05:30 ET return claimed to be carried *specifically* by
days following a US-session sell-off; dealer inventory-reversal / Grossman–Miller
immediacy premium).
**Date:** 2026-06-07. **Run:** `lab/analysis/noct_spx/gate.py` → `gate_result.json`.
**Status:** `DONE_WITH_CONCERNS` (verdict unambiguous; one flagged concern — sample window).

> **Overall gate = Stage 1 PASS ∧ Stage 2 PASS → FALSIFIED.** The conditional
> inventory-reversal channel does **not** separate from the unconditional
> European-open drift — and, on the corrected sample, the bottom-tercile EU return
> is not even significantly positive on its own. The concept does **not** advance to
> Stage 3.

## Data provenance

- **Dukascopy `USA500IDXUSD` m15** via `core/lib/dukascopy.py` (point_factor **1e3**,
  verified empirically vs OANDA + S&P 500 historical levels). UTC bars; DST-aware
  UTC→ET map. Panel: `core/data/bar_data/USA500IDXUSD_M15.csv` — 142,478 bars,
  2020-01-02 → 2026-06-05, 1,464 closed-hour skips.
- **Sample: 2020-01-07 → 2026-06-05** (operator-scoped). **1,587** usable analysis
  days full / **1,347** post-2020. Trigger (bottom-tercile prior-US) days: **529**
  full / **449** post-2020 (both ≫ the 200 / 100 floors).
- **Cost:** round-trip spread on R_EU, swept {0,1,2,3,5} bps (no recorded FXIFY/Alchemy
  SPX500 spread → breakeven reported). **Swap = 0** — the 02:00–05:30 ET window is
  intraday, after the 17:00 ET prior rollover and before the next; no financing event.

## DST verification (mandatory spot-check) — PASS

| date | regime | 02:00 ET = | London |
|---|---|---|---|
| 2022-07-15 | summer (EDT) | 06:00 UTC (−04:00) | 07:00 BST |
| 2022-01-14 | winter (EST) | 07:00 UTC (−05:00) | 07:00 GMT |
| 2022-03-16 | US-EU mismatch | 06:00 UTC (−04:00) | **06:00 GMT** |
| 2023-03-15 | US-EU mismatch | 06:00 UTC (−04:00) | **06:00 GMT** |

DST handling is correct: 02:00 ET → 06:00 UTC (summer) vs 07:00 UTC (winter), and the
EU window is 07:00 London normally but **06:00 London during the US-EU DST-mismatch
weeks** — the load-bearing shift the brief flagged, captured not ignored.

## Conditioning (causal lag) + a fixed sampling bug

EU window on day *t* is conditioned on the **most recent prior trading day's** US
session (strictly < *t*). The 02:00–05:30 ET window precedes that day's 09:30 US open,
so same-day conditioning would be look-ahead; the mechanism ("days *following* a US
sell-off") fixes the one-session lag.

**Bug caught + fixed before the verdict:** the first implementation used
`R_US.shift(1)` on a frame that included weekend/partial dates (NaN `R_US`), which
mapped every **Monday** EU window to the empty Sunday row and silently dropped it —
a biased ~420-day loss (1,167 vs 1,587 usable days) precisely on weekend-spanning
inventory days. Replaced with an as-of map to the most recent valid prior US session.
The fix **recovered the Mondays and made the falsification more decisive** (the
pre-fix borderline (a) t=2.13 was itself the artifact). Figures below are post-fix.

## Stage 1 (full sample 2020–2026) — FAIL

EU-window mean returns by prior-US tercile (gross): **all-days 0.0148%**, bottom
(largest sell-off) **0.0198%**, complement 0.0123%, top 0.0107%.

| condition | result | gate | verdict |
|---|---|---|---|
| **(a)** bottom mean > 0, t≥2, n≥200 | mean 0.0198%, **t=1.06**, n=529 | t<2 | **FAIL** (not significant even gross) |
| **(b)** separation (bottom − all-days), t≥2 | D=0.0050%, **t=0.34** | t<2 | **FAIL** (≈ no separation) |
| **(c)** bottom > top | 0.0198% > 0.0107% | — | PASS (sign only) |

- **(b) is cost-invariant** (a flat spread subtracts equally from bottom and all-days,
  leaving D and its t unchanged at every swept cost). The conditional channel is
  inseparable from the unconditional drift **at any spread assumption**.
- **(b) overlap-correct SE** = bottom-vs-complement Welch t = **0.344** (the
  `((n−n_B)/n)` scaling cancels). Cross-check bottom-vs-top t = **0.339**. Both agree —
  no sign/significance disagreement.
- **Stage 1 = FALSIFIED.** There is a faint unconditional EU drift (0.015%); the
  bottom tercile (0.020%) is neither significantly positive (a) nor separable (b).
  Breakeven round-trip spread **1.976 bps**, at/ below realistic SPX500 round-trip
  cost — so even the faint gross tilt is gone after cost.

## Stage 2 (2021–2026) — FAIL

| spread (bps) | (a) mean | (a) t | (b) t | bot>top | Sharpe_ann | n_trig |
|---|---|---|---|---|---|---|
| 0 | 0.0135% | 0.76 | 0.56 | ✓ | **0.325** | 449 |
| 1 | 0.0035% | 0.19 | 0.56 | ✓ | 0.084 | 449 |
| 2 | −0.0065% | −0.37 | 0.56 | ✓ | −0.157 | 449 |
| 3 | −0.0165% | −0.93 | 0.56 | ✓ | −0.399 | 449 |

- Conditional net Sharpe is **0.325 even at zero cost** (< the 0.5 gate) and goes
  negative by 2 bps; breakeven 1.348 bps. (a)/(b) t-stats <2 even gross.
- Annualization: per-trade Sharpe × √(trades/yr=83); convention pre-registered in `gate.py`.
- **Stage 2 = FAIL.**

## Robustness (NOT a pass route, brief §5 #4)

Last-90-min US proxy @ 2 bps: (a) t=1.01, (b) t=1.67, (c) ✓ — also fails. The
alternative US proxy does not rescue the channel. Consistent FALSIFIED.

## Concern (for parent §7 review — does not change the verdict)

**Sample-window deviation (operator-scoped):** 2020–2026 (~6.4yr) vs the brief's
pre-registered **≥8 years** (§4). The full Dukascopy history exists back to 2011-09;
this gate was scoped to 2020+ by Joshua. The FALSIFIED is robust on this window
(cost-invariant (b)≈0; (a) insignificant even gross; both US proxies fail; Stage 2
fails at zero cost), so an 8+yr re-run is very unlikely to flip it — but the
pre-registration was not met, and a confirmatory 2011–2026 run is one command away
(`fetch_panel.py --start 2011-09-18` then `gate.py`) if the parent wants it. Note also
Stage 1/Stage 2 windows overlap ~85% on this sample, weakening the decay-isolation
design; both fail consistently.

## Disposition

FALSIFIED → logged to `docs/rejected_candidates.md` via
`validation/concept_intake/feedback.py` (composite key
`inventory-reversal-immediacy-premium × SPX500`); re-running the intake gate now
returns DUPLICATE (loop closed). No Pine/strategy built (brief §5).
