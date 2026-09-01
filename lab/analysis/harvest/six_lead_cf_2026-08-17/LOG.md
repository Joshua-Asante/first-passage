# P1-CF / P2-CF — six-lead pursuit plan cheap falsifiers — LOG

**Date:** 2026-08-17
**Authority:** [`docs/briefs/programs/2026-08-17-six-lead-pursuit-plan.md`](../../../../docs/briefs/programs/2026-08-17-six-lead-pursuit-plan.md)
§4 (asymmetric-by-declaration) + §Phase-0-findings §4-design-freeze; operator GO on P1/P2 recorded
same day.
**Runner:** [`run_cf.py`](run_cf.py). **Trades:** `trades_{P1,P2}_{MGC,6J}.csv`. **Summary:** `SUMMARY.csv`.
**Cost:** $0 · K=0 — panels already on hand (`core/data/bar_data/MGC_M15.csv`,
`core/data/bar_data/6J_M15.csv`, both pre-existing/frozen), no pull, no `register_search open`,
no Cap claim.

## Verdict: FAIL — all four legs

| Construct | Symbol | n | win% | mean gross $/trade | mean net $/trade | t (net) | gross vs 4×RT hurdle |
|---|---|---:|---:|---:|---:|---:|---:|
| P1 (L3=L6, overnight fade) | MGC | 1,000 | 47.7% | **−$13.22** | −$16.04 | −1.19 | −1.17× |
| P1 (L3=L6, overnight fade) | 6J | 551 | 46.6% | +$23.68 | +$15.61 | 0.64 | **0.73×** |
| P2 (L1, prior-session fade) | MGC | 1,025 | 51.1% | **−$9.22** | −$12.04 | −0.91 | −0.82× |
| P2 (L1, prior-session fade) | 6J | 1,517 | 42.8% | **−$5.49** | −$13.56 | −0.97 | −0.17× |

Three of four legs are gross-negative outright. The fourth (P1×6J) is gross-positive but (a)
statistically indistinguishable from zero (t=0.64, nowhere near the ≥2 convention used throughout
this repo) and (b) fails the standing 4× round-trip cost hurdle at 0.73× — the same
gross/(4×RT)-style test used elsewhere in this estate (e.g. MECHANISMS.md CON-4: "gross/(4×RT)
≈0.27×"). **No leg clears both significance and the cost hurdle.**

## Diagnostic: not a stop-mechanism artifact

Stop-trigger rate is low across all four legs (3.3–4.7%), so the intrabar hard-stop is not driving
the result. Splitting by direction shows a consistent asymmetry — one side near-breakeven, the
other clearly losing — which tracks each instrument's own trend over the sample window (MGC's
2022–2026 uptrend punishes the short-the-up-move leg; the sign flips on 6J). This is the textbook
"fade fights the trend" failure mode, not a construction bug — it *raises* confidence in the null
rather than casting doubt on it.

| Leg | long n / mean $ | short n / mean $ |
|---|---|---|
| P1×MGC | 452 / +$3.18 | 548 / **−$31.90** |
| P1×6J | 295 / **−$20.69** | 256 / +$57.45 |
| P2×MGC | 485 / +$3.48 | 540 / **−$25.97** |
| P2×6J | 852 / **−$42.91** | 665 / +$24.05 |

## Construction (per the frozen design, unmodified)

Session bucketing: bars from 18:00 ET onward belong to the next calendar date's trade-date
(CME Globex reopen after the daily maintenance halt); session close = last bar with ET hour < 16
(the E1 16:00 ET flat default). Holiday-short (12:59 ET) handling **not applied** — flagged in the
design freeze as unchecked against a current CME calendar; this leaves a small number of
early-close sessions using a slightly-late close print, immaterial at this sample size. Roll days
detected as overnight-return outliers (|z|>5 on each instrument's own distribution) rather than a
calendar rule — 9/1,040 MGC sessions and 19/1,765 6J sessions excluded on this basis.

P1 fades the overnight gap (`session_close[D-1] → session_open[D]`); P2 fades the prior session's
full open-to-close move (the "venue-expressible" prior-day-reversal slice, not raw close-to-close
autocorrelation). Both enter at the reopen bar's own open, exit at session close or a
1.5×ATR(20-session) hard stop, whichever first. Cost: commission $0.91/side (reused from the
M6A/MGC third-leg-map figure, not invented fresh) + 1 tick total slippage — MGC $2.82/RT, 6J
$8.07/RT.

## What this does NOT license

Per the plan's asymmetric-by-declaration rule: this FAIL kills the P1/P2 sleeves **as constructed**
(this session-boundary, this stop, these two instruments) — it does not foreclose a differently-
constructed test of the same papers' mechanism, and it says nothing about MCL (already excluded,
pre-killed by arithmetic — see the plan §2) or about any instrument/window not tested here.

## Open — not resolved by this LOG

**The harvest §4 limb-2 counter question is still unmarked by the operator** (six-lead pursuit
plan §13). This FAIL is exactly the case that question governs — whether it counts toward the
0/2. Recorded here as an explicit precondition for closing this out on all four required surfaces,
not decided unilaterally.
