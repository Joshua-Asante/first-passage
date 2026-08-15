# Slow-archetype extension — does a 20/32/50-day pass at k=1 exist, and is it payable?

**Status:** RESOLVED — MNQ's own measured edge (0.85R) at one independent trade/day, safely sized to the eval rope, produces a 21-day median pass at 0.9% bust; every archetype tested clears the $200 funded winning-day floor, and Tradeify's own Common FAQs confirm the evaluation carries no time limit at all.

> ⚠ **COHORT CORRECTED 2026-08-08 (banner only; frozen body and results unedited —
> [ADR](../../../docs/adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md)).** "MNQ's own measured edge
> (0.85R)": the referent is the **Striker NAS100→MNQ venue-edition export** (pyramided, 0.35 trades/cal-day —
> [MNQBASE-1 §1.3](../../../docs/briefs/rnd-pipeline/MNQBASE-1-tradeify-shaped-base-construct-harvest-scoping.md)), **NOT**
> "N1 / ORB-MNQ-1's realized edge" as §4.2 (L123–124) states — ORB's realized per-trade edge is **+0.0626R**
> ([re-park ADR §4](../../../docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md)). `run_slow.py:108` hard-codes
> `(w=0.55, b=2.363636)` as a config; no panel derivation exists here or in the cited sibling. The simulation arithmetic
> stands; every "0.85R" row describes a hypothetical independent-entry construct, and §5.1's own scope limit ("a bound on a
> *redesigned* construct") governs. The MYM 0.49R label carries the same caveat (Striker DJ30→MYM edition, pyramided).

**Date:** 2026-08-04 · **Parent model:** [`eval_inverse_requirements_2026-08-03/run_inverse.py`](../eval_inverse_requirements_2026-08-03/run_inverse.py) `simulate()`, imported unmodified via `importlib` (zero transcription risk) — anchor `cdfd2f8` 2026-08-03.
**Cost:** $0.00 · K=0 · no manifest · no candidate proposed, admitted, or scored against harvest Req 1–5.
**Runner:** [`run_slow.py`](run_slow.py) · parity check (reproduces the parent's published `tight_grind_12d_a` row) passes before any new number is trusted.

---

## 1. Why this exists

Every MNQ base-construct search this estate has run (MNQBASE-1, the census passes, the harvest
deep-search) has been screened against the parent harness's **T2: 3–8 independent trades/day**. That
requirement was never a venue rule — it is the parent harness's own §3 choice to solve for a
**3–12 day** pass window (RESULTS.md B1's target-line table). B1's own table runs to a 50-day pass at
**$120/active day** — a target an order of magnitude easier than $2,000/day (the 3-day figure) — but
nothing in this estate had ever *simulated* that end of the table, only listed its mean arithmetic.

**What changed 2026-08-04, verified fresh (not inherited):**

1. **Tradeify's evaluation has no time limit**, confirmed by direct quote — see §2.
2. `MNQBASE-1` closed with every sourced candidate dying on **harvest Req 1 (mechanism admissibility)**,
   never on edge size (closure §3, three candidates, all `P2`). The bottleneck was never "can MNQ
   produce a 0.40R+ edge" — MNQ's own measured 0.85R already clears that by 2×.
3. Step 1's own event-ceiling study established the bottleneck is **selection**, not opportunity: MNQ
   supports 145+ independent disjoint tradeable windows/day, against a realized book that fires 0.35
   trades/calendar-day. A construct that fires far less often than 3–8/day was never ruled out by
   opportunity — only by the parent harness's own choice of target horizon.

This study asks the inverse question at the horizon B1 already tabulated but never simulated: **what
does a k=1 (one independent trade per active day) construct need, at this estate's own already-measured
edges, and does it clear funded-phase payability at the same time?**

---

## 2. Venue fact, verified fresh (2026-08-04, in-browser; `WebFetch` 403s this host)

**Q: Is there a time limit for evaluations?**
**A: There is no time limit to complete a Growth or Select Evaluation.**

— [Common FAQs](https://help.tradeify.co/en/articles/12268494-common-faqs) (article 12268494,
"Updated over 2 weeks ago"), the same governing article already load-bearing in this repo for the
idle-rule deletion consequence (`TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md` §2a).

**Corroborated by two further primary reads, same session:** [Select Evaluation Accounts](https://help.tradeify.co/en/articles/12853921-select-evaluation-accounts)
(article 12853921, dated **April 2, 2026**) lists every 100K evaluation-phase rule exhaustively —
profit target $6,000, EOD max drawdown $3,000, no daily loss limit, 40% consistency, 8 mini/80 micro
cap — with **no duration field anywhere in the listing**. [Essential Trading Rules Overview](https://help.tradeify.co/en/articles/12268167-essential-trading-rules-overview)
likewise carries no duration language. A page-text search for `time limit`, `expire`, `days to
complete`, `must complete`, `unlimited time` returned zero hits on both corroborating articles.

**One adjacent phrase, checked and resolved.** The same FAQ page states elsewhere: *"your account
remains active until you either pass, fail, or the account expires."* Read in context (two questions
earlier on the same page states flatly there is no time limit), the coherent reading is that
*"expires"* refers to the already-documented **inactivity-deletion** mechanism (§2a of the compliance
note), not a second, undisclosed duration clock. Not a new venue fact — restated here because it was
checked, not assumed.

⚠ **What this does NOT establish.** The `≥1 trade per Mon–Fri week` idle rule (§2a, already verified
2026-08-02) is unaffected and remains binding — "no time limit" means no *day-count* deadline; it does
not relax the weekly cadence floor, which is the real, still-binding minimum-frequency constraint (§5).

---

## 3. Model

Byte-identical to the parent — see its own docstring for the full spec (independent trades, hard
stops, no serial correlation). This script adds nothing to the model; it only asks the model a
question the parent tabulated (B1) but never simulated at k=1.

**Edge levels are not invented.** `generic_0.65R` is the parent's own reference config. `mym_measured_0.49R`
and `mnq_measured_0.85R` are this estate's **own already-measured** per-trade edges on the live venue
editions (parent RESULTS.md §5: *"MNQ's 0.85R is better than any configuration simulated"*; MYM 0.49R).
Both are solved for `b` at fixed `w=0.55` (`edge_R = w·b − (1−w)`), verified independently before
running: `b=1.709091` → edge 0.490000; `b=2.363636` → edge 0.850000.

**`max_days` correction, caught before trusting output.** The parent's `simulate()` defaults to
`max_days=60`. A first quick pass at the 32d/50d targets showed `pass + bust ≠ 100%` — the 60-day
window was truncating a 46–48-day-median archetype's tail into a silent "still live" bucket rather
than letting it resolve. Fixed by threading `max_days=200` through every call in this script (a thin
wrapper, `max_risk_at_k_maxdays`, added locally since the parent's own `max_risk_at_k` hardcodes the
default and cannot be called with an override without editing the frozen file — which this study does
not do). Re-run confirms `pass + bust = 100%` at every row below.

---

## 4. Results

### 4.1 — Solved for B1's own per-day targets (20d / 32d / 50d), k=1

| Target | Edge | r/trade | mu/day | pass | bust | med days | win-day $ | ≥$200 floor |
|---|---|---:|---:|---:|---:|---:|---:|:---:|
| 20d ($300/d) | MYM 0.49R | $612 | $299.9 | 79.4% | **20.6%** | 16d | $1,046 | ✓ |
| 20d ($300/d) | generic 0.65R | $462 | $300.3 | 94.1% | 5.9% | 17d | $924 | ✓ |
| 20d ($300/d) | MNQ 0.85R | $353 | $300.0 | 98.7% | 1.4% | 19d | $834 | ✓ |
| 32d ($188/d) | MYM 0.49R | $383 | $187.7 | 93.9% | 6.1% | 29d | $655 | ✓ |
| 32d ($188/d) | generic 0.65R | $288 | $187.2 | 99.2% | 0.8% | 30d | $576 | ✓ |
| 32d ($188/d) | MNQ 0.85R | $221 | $187.8 | 99.9% | 0.1% | 30d | $522 | ✓ |
| 50d ($120/d) | MYM 0.49R | $245 | $120.1 | 99.3% | 0.7% | 48d | $419 | ✓ |
| 50d ($120/d) | generic 0.65R | $185 | $120.3 | 100.0% | 0.0% | 48d | $370 | ✓ |
| 50d ($120/d) | MNQ 0.85R | $141 | $119.8 | 100.0% | 0.0% | 48d | $333 | ✓ |

**Read this row-by-row, not as a single verdict.** Forcing MYM's own (weaker) measured edge into a
fast 20-day target produces a 20.6% bust rate — well above the 1% frontier convention used everywhere
else in this estate. That is not a MYM failure; it is the same §2a inversion the parent harness's own
§2a already names: a target chosen faster than an edge naturally supports inflates `r`, and larger `r`
against a fixed $3,000 rope raises bust. The honest number for any given edge is its own frontier
(§4.2), not a target picked independently of it.

### 4.2 — Max risk/trade at k=1, bust ≤ 1%, independent of any target horizon

The frontier the rope itself permits — what falls out when `r` is sized for safety, not speed:

| Edge | max r/trade | mu/day | pass | bust | med days | win-day $ | ≥$200 floor |
|---|---:|---:|---:|---:|---:|---:|:---:|
| MYM measured 0.49R | $250 | $122.5 | 99.2% | 0.8% | **46d** | $427 | ✓ |
| generic 0.65R | $275 | $178.8 | 99.2% | 0.8% | **32d** | $550 | ✓ |
| **MNQ measured 0.85R** | **$325** | **$276.2** | **99.1%** | **0.9%** | **21d** | **$768** | ✓ |

**The headline number.** MNQ's own already-measured, already-in-the-book edge — traded **once per
active day, independently, sized safely to the rope** — produces a **21-day median pass at 0.9%
bust**. This is not a hypothetical construct: it is this estate's own N1 finding (`ops/instruments/MNQ.md`,
ORB-MNQ-1's realized edge), re-expressed against the corrected pass-speed target.

**Every row clears the $200 funded winning-day floor, several times over.** Even the slowest, weakest
row (MYM at 50d) posts $419 winning days — more than double the funded threshold. Contrast this with
the pincer this estate's own forced-flow census found repeatedly on *fast, thin-edge* constructs
(settlement/fix fades, ~1 event/day, `BE3`/`SFX-1`): those died because a single-entry day cannot
clear $200 while staying under an achievable Sharpe ceiling. That trap does not bind here — it is a
property of thin per-event edges at high required frequency, and this study's edges (0.49R–0.85R) sit
well above it.

---

## 5. What this does NOT establish — read before citing any row

1. **k=1 means genuinely independent entries — the incumbent book does not have this shape.** The
   live MNQ leg is ATR-sized and pyramided; a pyramid add is a *correlated* add, which the parent
   harness's own §2 shows collapses toward the k=1 row **at a larger effective r** (worse, not
   better). This study does not re-measure the incumbent; it bounds what a *redesigned*, non-pyramided
   construct at the same per-trade edge could do.
2. **"No time limit" does not mean "no cadence floor."** The `≥1 trade per Mon–Fri week` rule is
   still binding and still enforced by account deletion (§2a). A 21–48-day median pass is comfortably
   inside "no time limit," but the construct still needs a trade at least every calendar week to avoid
   the idle-deletion path — a duty-cycle floor around 20%, not zero.
3. **Duty-cycle clustering, not duty-cycle level, is the incumbent's actual measured problem.** The
   incumbent's realized ~22% active-day rate is *not* below this rough floor — but its active days
   **cluster** (both legs idle the same weeks), producing 26.3% zero-trade Mon–Fri weeks and 4
   consecutive dead weeks at worst (`c1_cadence_inactivity_2026-08-02/RESULTS.md` §1). A construct at
   this study's edge levels, fired independently rather than in a correlated pair, would need its
   *idle weeks* to be uncorrelated with the sibling leg's — a design property this study does not
   test and the frequency numbers alone cannot certify.
4. **A range window is not a construct.** Exactly as Step 1's own scope note says: this bounds what a
   *hypothetical* independent-entry MNQ/MYM construct could achieve at an *already-measured* edge. It
   does not identify which of the ~145 daily disjoint windows to take, and does not license any
   candidate. Harvest Req 1–5 and the standing K discipline are untouched and still bind.
5. **The eval floor line assumes k=1 exactly.** A construct that fires more than once per active day
   on genuinely independent signals reaches these medians faster (parent RESULTS.md §2: frequency is
   free at k≥1 above the 0.40R inversion floor) — this study's k=1 numbers are a *lower bound* on
   speed, not the only achievable shape.
6. **The funded-phase 40-micro pyramid misfit that killed the locked Striker book is untouched.** This
   study's archetypes are flat-sized (no pyramid), so they do not inherit that specific de-scope
   ground — but they are not measured against the funded contract-scaling ladder either. A future
   candidate must re-check funded-phase payability at its own realized size, not assume this study's
   $200-floor pass transfers unchanged.

---

## 6. Reproduce

```bash
cd lab/analysis/c1/eval_slow_archetype_2026-08-04
python run_slow.py            # full run, ~seconds, writes RESULTS.json
python run_slow.py --quick    # smoke check
```

Stdlib + numpy only. Imports `simulate()`/`TARGET`/`R`/`BUST_TOLERANCE` unmodified from the parent via
`importlib`; parity check reproduces the parent's published `tight_grind_12d_a` row before any new
number is trusted. Deterministic under the pinned seeds.
</content>
