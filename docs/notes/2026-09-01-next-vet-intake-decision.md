# Next Vet intake decision — B1 strategy and source pursuits closed

**Date:** 2026-09-01
**Status:** `CLOSED — DROP B1 strategy pursuit; STOP B1 source pursuit`
**Spend / K:** $0 / K=0 — repository evidence only; no outcome comparison run.
**Operator decision:** close both B1 pursuits. Vet screens for candidates with a confidently high
positive-expectancy prior; B1 supplies none, and source liveness cannot create one.

## 1. What B1 actually is

B1 is a **mechanism-and-signal sketch**, not a complete proposal:

- observe a same-day signed S&P 500 closing-auction imbalance around 15:50 ET;
- hypothesize that dealers/arbitrageurs normalize inventory after the cash close;
- fade a positive imbalance by shorting MES, or fade a negative imbalance by buying MES;
- use the proposed 16:01–16:45 ET wake window; and
- remain flat by the venue deadline.

The corpus does **not** supply the remaining complete-expression fields Vet requires: a verified
live signal source, an imbalance threshold or all-events rule backed by evidence, exact order and
fill semantics, hard stop, target/exit behavior beyond a clock sketch, sizing/risk geometry, or a
powered exploration/Confirm partition. Those are not clerical blanks; several determine payoff
shape and cost reachability.

## 2. What its positive expectancy is

**Unknown. No positive expectancy has been measured or credibly sourced.** The B1 literature
search found no citable effect size for post-close, signed-imbalance-conditioned index-futures
reversal. The earlier F1 ruling states the same evidentiary state more directly: no δ, no cohort,
no measurement, plus unvalidated transmission from a cash-equity imbalance to a micro future.

The numbers currently attached to B1 are **requirements, not forecasts**:

- gross mean capture must exceed approximately **3.46 MES points/trade** to clear the standing 4×
  Tradeify crossing-cost hurdle;
- a `bounded_clustered`, risk=$275 expression needs approximately **65% win rate** at the relevant
  2–3/week cadence for a clean venue-shape clearance; and
- the estate has **zero measured B1 win-rate or payoff-ratio evidence**.

It is therefore incorrect to describe B1 as having positive expectancy. Its economic hypothesis
is merely that post-close normalization is opposite the published imbalance sign. Whether that
effect is positive after costs—and whether it has a survivable stop/target shape—is precisely the
missing evidence.

## 3. Closure of both pursuits

1. **B1 MOC→MES strategy pursuit: `DROP`.** No credible high-positive-expectancy prior, no complete
   expression, and no realistic evidence that further work is the shortest path to a viable
   strategy. This is an intake/economic-prior closure, not a market-null claim.
2. **B1 source-liveness pursuit: `STOP`.** Even a perfect five-session source result would prove
   only operational availability. Because the strategy pursuit is closed, the source check has no
   decision-changing consumer and must not run as research activity for its own sake.

No row was logged, no MES outcome was read, and no K was consumed by either proposed log.

## 4. Correct next action

The number-one objective is a viable trading strategy. Source/Assemble should now prioritize ideas
that arrive with a credible, large, net-positive effect prior and a complete trade expression—not
another diagnostic route whose best case is “data exists.” The current Vet output is
`NO CANDIDATE`; a dry queue is not a reason to lower the expectancy bar.

**Re-proposal bar:** independently credible evidence of a large positive **net** expectancy for a
signed closing-imbalance fade in index futures, sufficient to clear the 3.46-point MES hurdle and
venue shape, plus a complete frozen signal/entry/stop/exit/sizing expression. A live source alone,
a longer paper log, a new aggregator, a different index micro, or an imbalance-threshold retune
does not qualify.

## 5. Phase-A calibration retained, not a sourcing blocker

Treat `GAPCOND-ORB-1`'s false-`PASS` and corrected `DROP` as one case. A fresh reader passes the
calibration only by independently finding the lock-grade gap×ORB prior cell and binding forbidden
move, then reaching `DROP` without copying the corrected card's label. This process calibration may
run alongside high-expectancy sourcing; it does not displace the number-one strategy objective.

## 6. Source map

- B1 evidence and explicit zero-measurement finding:
  [`2026-08-23-phase-b-lane-b1-falsifier-results.md`](research/2026-08-23-phase-b-lane-b1-falsifier-results.md).
- B1 source-liveness instrument, now closed:
  [`2026-08-24-phase-b-lane-b1-paper-log-tracker.md`](research/2026-08-24-phase-b-lane-b1-paper-log-tracker.md).
- Phase-B lane owner:
  [`2026-08-23-viable-strategy-phase-b-mechanism-supply.md`](../superpowers/plans/2026-08-23-viable-strategy-phase-b-mechanism-supply.md).
- Accepted Phase-A pair:
  [`2026-09-01-gapcond-orb-1-vet-card.md`](2026-09-01-gapcond-orb-1-vet-card.md).
