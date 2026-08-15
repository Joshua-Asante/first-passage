# Inverse eval requirements — what a portfolio must PRODUCE to pass Tradeify Select 100K

**Status:** ACTIVE — max risk/trade is ~flat in trades/day ($275 at a 0.65R edge, k=1 through 4), so daily profit scales linearly with FREQUENCY but is capped in SIZE; the 3-day archetype needs ~8 trades/day and the 12-day archetype ~3, against the c1 book's 1.6 per active day at a 22% duty cycle

**Scope:** measurement only. **$0 spent · K=0 consumed · no manifest opened · no `core/`, Pine, allocation, `dd_protection`, lifecycle-state, or rail change.** No candidate is proposed, admitted, demoted, or retired by this study.

> ⚠ **COHORT CORRECTED 2026-08-08 (banner only; frozen body unedited —
> [ADR](../../../docs/adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md)).** §5's two-cell table ("Edge per
> trade: MNQ **0.85R** / MYM **0.49R**, measured from the 2026-08-03 venue-edition exports") is the estate's **origin** of
> the 0.85R figure. The cited sibling (`c1_cadence_coverage_2026-08-03`) publishes no per-trade R derivation, and the
> cohort is the **withdrawn, pyramided Striker venue editions** (NAS100→MNQ / DJ30→MYM; correlated adds, ~0.35
> trades/cal-day — [MNQBASE-1 §1.3](../../../docs/briefs/rnd-pipeline/MNQBASE-1-tradeify-shaped-base-construct-harvest-scoping.md)).
> Downstream artifacts re-attributed these to "N1 / ORB-MNQ-1's realized edge" (**+0.0626R** actual). Quote either figure
> only with this cohort binding attached.

**Run date:** 2026-08-03 · **Harness:** [`run_inverse.py`](run_inverse.py) · **Raw:** [`RESULTS.json`](RESULTS.json)
**Repo anchor:** HEAD `1dcde85`, worktree clean at run time.
**Sibling (forward problem):** [`c1_cadence_coverage_2026-08-03`](../c1_cadence_coverage_2026-08-03/RESULTS.md) — that study asks "does this book pass?"; this one holds the geometry fixed and solves for the strategy properties that would.

---

## §0 — Geometry held fixed

Tradeify Select 100K, **evaluation** phase, from [`core/firm_rules.py:321`](../../../../core/firm_rules.py) (`89a069a`):

| | |
|---|---|
| Rope | floor = running EOD peak − **$3,000**, ratchets up only, breach tested **intraday** |
| Target | **+$6,000** (6%) |
| Min days | 3 |
| Consistency | best single day ≤ **40%** of total profit at the moment of pass |
| Drawdown lock | **none** — `dd_lock_offset_usd: 100` encodes a mechanism the eval does not have (venue art. 10495897; that row carries its own OPEN DEFECT block) |

Frontier is defined at **≤1.0% failure**. That tolerance is a choice, not a venue fact — every "max risk" figure below moves if it changes.

---

## §1 — Exact boundaries (arithmetic, no simulation)

**B1 — Target line.** Required mean per **active** day:

> ⚠ **LABEL 2026-08-06 (EM §7 row 6):** the **3 d / 5 d / 8 d** cells ($2,000 / $1,200 / $750)
> encode a retired **speed preference**, not a venue duration requirement (eval has no time
> limit — Pin 6 / MNQ **N13**). They remain arithmetically correct measurements. **Do not quote
> them as binding-on-speed** or re-derive a trades/day floor from them. Standing cadence screen
> is **EM4** (weekly, uncorrelated) in
> [`docs/spec/2026-08-05-eval-mechanism-shape-screen.md`](../../../../docs/spec/2026-08-05-eval-mechanism-shape-screen.md)
> (`RATIFIED 2026-08-06`). Slower cells (12 d+) are unaffected by this label.

| Pass in | 3 d | 5 d | 8 d | 12 d | 20 d | 32 d | 50 d |
|---|---|---|---|---|---|---|---|
| μ needed | $2,000 | $1,200 | $750 | **$500** | $300 | $188 | $120 |

**B2 — Consistency line.** Effective target is `max($6,000, 2.5 × best day)`:

| Best day | $2,400 | $3,000 | $4,000 | $6,000 |
|---|---|---|---|---|
| Must reach | $6,000 | $7,500 | $10,000 | $15,000 |

⌈1 ÷ 0.40⌉ = 3, which is **why** `min_trading_days: 3` exists — it is the arithmetic shadow of the 40% rule, not an independent constraint.

**B3 — Rope line.** Max risk/trade, measured at ≤1% failure: **$275** at a 0.65R edge. That is **0.275% of account** — roughly an order of magnitude below the 1–2% most sizing conventions assume, because the binding quantity is the depth of a losing *run* against a fixed $3,000 rope.

---

## §2 — The load-bearing finding: frequency is free, size is not

`w=0.55, b=2.0` (edge 0.65R), max risk/trade at ≤1% failure:

| trades/day | max risk/trade | μ_max/day | μ per trade/day |
|---|---|---|---|
| 1 | $275 | $179 | $179 |
| 2 | $275 | $358 | $179 |
| 3 | $275 | $536 | $179 |
| 4 | $275 | $715 | $179 |
| 6 | $325 | $1,268 | $211 |
| 8 | $325 | $1,690 | $211 |

**Max risk/trade does not fall as trades/day rises** — it is flat at $275 across k=1→4 and *improves* to $325 by k=6. So:

> μ_max = k × r_max × E — **linear in frequency, capped in size.**

Mechanism: the rope constrains how deep a losing *run* goes (streak × r), which is a property of risk-per-trade and win rate. It does not care how many independent trades a session contains. Daily profit does. Adding trades/day at constant r buys linear return at ~constant drawdown risk; adding risk/trade does not.

**Independence is load-bearing.** Perfectly correlated k trades at risk r are arithmetically identical to one trade at risk k·r, which collapses to the k=1 row — the worst in the table. A pyramid add is a correlated add, which is why this result does not transfer to the incumbent book.

### §2a — The result INVERTS below an edge threshold

"Frequency is free" holds at edge ≳ **0.40R**. Below it the sign flips — max risk/trade *falls* as trades/day rises:

| edge | k=1 | k=2 | k=4 | k=6 | k=8 |
|---|---|---|---|---|---|
| 0.65R (w55/b2.0) | $275 | $275 | $275 | $325 | $325 |
| **0.139R** (w34.9/b2.27) | **$100** | **$75** | **$75** | **$50** | **$50** |

At a thin edge, extra trades widen the daily distribution faster than they move it right, so the rope binds harder and the size cap collapses. The 0.139R row tops out at **μ = $56/day even at 8 trades/day** — a 54-day median and a 6.8% pass rate.

**Consequence:** frequency is a *multiplier* on an edge that already clears the bar, not a substitute for one. A construct below ~0.40R cannot be rescued by trading it more often, and attempting to do so makes its rope geometry worse rather than better.

---

## §3 — What each archetype demands

| Archetype | Config | μ/day | Pass | Fail | Median |
|---|---|---|---|---|---|
| **Even grind** | 60% win / 2R, **8 trades/day**, $400 risk | $2,560 | 99.2% | 0.8% | **4 d** |
| **Tight grind** | 55% win / 2R, **3 trades/day**, $250 risk | $488 | 99.7% | 0.3% | **12 d** |
| **Tight grind (alt)** | 60% win / 2R, **2 trades/day**, $300 risk | $480 | 99.7% | 0.3% | **12 d** |

Neither requires an exotic edge. The tight grind runs on **0.65R per trade — below what MNQ already achieves (0.85R)**.

Win rate is close to irrelevant across the band: at k=4, a 40%-win/2.7R construct (edge 0.48R) passes 99.1% with a 21-day median.

---

## §4 — Hard stops are load-bearing

Same config (55%/2R, 3 trades/day, $275), varying how often a stop is jumped:

| Stop behaviour | Failure rate |
|---|---|
| Hard stops hold | **0.6%** |
| 2% of losses gap 3× | 1.0% |
| 5% of losses gap 3× | 2.1% |
| 2% of losses gap 5× | 2.7% |
| 5% of losses gap 5× | **8.0%** |

A 13× increase in failure from a tail that never appears in mean/variance. This is the assumption most likely to break in live trading, and it rules out overnight holds, illiquid instruments, and anything that can jump a stop.

---

## §5 — Where the incumbent book sits (calendar, not just per-day)

Measured from the 2026-08-03 venue-edition exports (see the sibling study):

| | MNQ | MYM |
|---|---|---|
| Edge per trade | **0.85R** | **0.49R** |
| Trades per active day | 1.38 | 1.37 |

**The per-trade edge is not the problem.** MNQ's 0.85R is better than any configuration simulated here. The gap is frequency, and it compounds twice:

- **1.6 trades per active day** (combined book) against 3–8 needed
- **22% duty cycle** — 55 active days/yr out of ~252

Net: **0.35 trades per calendar trading day against 3–8 needed.**

Calendar translation (`active days × 252 ÷ active days per year`):

| Cadence | 12 active d | 20 active d | 32 active d |
|---|---|---|---|
| c1 book as-is (55/yr) | 55 cd | 92 cd | 147 cd |
| 3 days/week (156/yr) | 19 cd | 32 cd | 52 cd |
| daily (252/yr) | 12 cd | 20 cd | 32 cd |

---

## §6 — What this does NOT establish

1. **It is a model, not a re-description of the book.** Fixed-fractional risk, hard stops, independent trades. The c1 legs violate all three (ATR-sized, pyramided, overlapping holds). The model describes a strategy *class*; it does not re-measure the incumbents.
2. **No serial correlation.** Real strategies cluster losses across days; this draws days independently. Direction of error is optimistic.
3. **The $275 figure is tolerance-dependent** (≤1% failure). At a 5% tolerance it rises materially.
4. **Frequency ≠ admissibility.** A construct that fires 8×/day still has to clear the cost-law screen, the DSR floor at its family's banked K, and the regime gate. This study says what the *eval* requires; it says nothing about whether a candidate meeting that shape has durable edge, and the two bars are independent.
5. **Not a venue-fit or lifecycle verdict on any strategy.** §5 locates the incumbent book on a frequency axis. It does not measure any alternative construct, and no candidate's admissibility is decided here.

---

## §7 — Reproduce

```bash
cd lab/analysis/c1/eval_inverse_requirements_2026-08-03
python run_inverse.py           # ~2 min, writes RESULTS.json
python run_inverse.py --quick   # smoke check
```

Stdlib + numpy only. Deterministic under the pinned seeds; no vendor data, no repo panels, no network.
