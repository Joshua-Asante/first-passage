# Seed target spec re-derived at the RATIFIED gate — what can seed the live Tradeify eval

> ## ⚠ Reader-intercept 2026-09-03 — two figures below have since moved, one of them in the headline
>
> **1. The Part A ceiling is now 5.0%, not 3.0%** ([`prereg v2`](../../../../docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md)
> §3, 2026-08-26). Every "ratified gate" figure below is scored against v1's superseded 3.0%.
> The gate's *shape* (pass floor 50%, intraday-honest clock, ≥1 `trailing_locking`) is unchanged.
>
> **2. "96.9% account deletion" is an ENGINE figure, not a venue probability.** It is a
> `bust_inactivity` rate from `core/mc/simulation.py`'s **rolling** consecutive-idle-business-day
> counter. Tradeify's actual rule (art. 10468318) is a **per-Mon–Fri-week bucket**: ≥1 trade per
> week. The two are not the same predicate — a calendar trading Mon-wk1 / Fri-wk2 / Mon-wk3 /
> Fri-wk4 satisfies the venue in every week and still returns `bust_inactivity` on day 6 (measured
> 2026-09-03). Every real breach does trip the counter, so **96.9% is a conservative UPPER BOUND on
> venue deletion risk, not an estimate of it**; the true bucket-rule rate is unmeasured. The same
> caution applies to the §-level venue-rules table below, which lists the engine's 5-idle-bday proxy
> in a row of article-cited venue facts.
>
> **What this does NOT change:** the study's actual finding — that the weekly activity rule is the
> binding constraint for a low-duty seed construct, and that the ~$24/yr token trade is
> load-bearing — survives both corrections, and the second one only makes the barrier-ON arm
> *less* severe. Body unedited (Trap #12); banner upstream per
> [`operational_rules.md`](../../../../docs/operational_rules.md) §14.

**Status:** ACTIVE — at the ratified Part A gate the eval's binding constraint for a seed construct is the **weekly activity rule and nothing else**. Duty cycle is irrelevant to passing once a token trade is delivered (pass ~99.4% from duty 1.00 down to 0.15); without one, pass collapses to **3.0%** at the incumbent book's 0.22 duty with **96.9% account deletion** — a **+96.3pp** swing bought by an instrument costing ~$24/yr. Target-spec limbs **T1, T2 and T7 are each materially tighter than the gate they feed**.

**Scope:** measurement only. **$0 spent · K=0 consumed · no manifest opened · no `core/`, Pine, allocation, `dd_protection`, lifecycle-state or rail change.** ⚠ **F2 dependency (2026-08-06 / LAB-4):** S7 "unoccupied" reading in §7 is **pending fork F2** — symbols retained-not-released; see amendment under §7 table. No candidate is proposed, admitted, demoted or retired here. This maps a **venue acceptance region**; it scores no strategy.

**Run date:** 2026-08-04 · **Harness:** [`run_seed_spec.py`](run_seed_spec.py) · **Raw:** [`RESULTS.json`](RESULTS.json)
**Repo anchor:** HEAD `b812667`, worktree clean at run time.
**Engine cross-check:** `python run_seed_spec.py --verify` reproduces `core/mc/simulation.py::simulate_path` to **0.000pp** on both bust and pass (n=3,000). See §6.

**Siblings.** [`eval_inverse_requirements_2026-08-03`](../eval_inverse_requirements_2026-08-03/RESULTS.md) solved the same inverse problem at a **chosen ≤1.0%** tolerance and explicitly excluded duty cycle and the inactivity rule. MNQBASE-1 froze that output as target spec **T1–T7**. This study re-derives those limbs at the **ratified** gate and adds the missing calendar axis.

---

## §0 — Geometry and gate held fixed

Eval geometry, Tradeify Select 100K **evaluation** phase, from [`core/firm_rules.py:321`](../../../../core/firm_rules.py):

| | |
|---|---|
| Rope | floor = running EOD peak − **$3,000**, ratchets up only, breach tested **intraday** |
| Target | **+$6,000** |
| Min days | 3 · Consistency best day ≤ **40%** of total profit at pass |
| Activity | ≥1 trade per Mon–Fri week; **5 consecutive idle business days ⇒ irreversible account deletion** (art. 10468318 + 12268494) |
| Drawdown lock | **none** — `dd_lock_offset_usd: 100` encodes a mechanism the eval does not have (art. 10495897; that row carries its own OPEN DEFECT block) |

The gate is **not** this study's choice. Parsed live by `lab/discovery/prop_survivor_scoring.py::load_scoring_thresholds` from [`the 2026-07-13 prereg`](../../../../docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md):

> `eval_bust_ceiling = 0.03` · `pass_floor = 0.50` · `horizon = 1500` · **inactivity disabled**

That last word is load-bearing and is examined directly in §3.

**Model.** A strategy is `(w, b, r, k, d)` — win rate, payoff ratio, risk/trade in dollars, trades per **active** day, and duty cycle (fraction of business days active). Trades are independent and hard-stopped, so the within-day running minimum of cumulative realized P&L is the correct intraday proxy. Identical to the sibling's model so the numbers are directly comparable.

---

## §1 — T2 re-derived: "3–8 independent trades/day" is a speed preference, not a bar

MNQBASE-1 §5.1 already flagged this against itself — no tier in `core/firm_rules.py` encodes an evaluation **time limit**, so T2 could only ever have been a speed statement. It was never measured. Measured now, at `w=0.55 b=2.0 r=$275`, token trade delivered:

| trades/day | pass | bust | median days-to-pass |
|---|---|---|---|
| **1** | **99.2%** | **0.81%** | 32 bdays (~1.5 mo) |
| 2 | 99.3% | 0.74% | 16 bdays |
| 3 | 99.4% | 0.60% | 12 bdays |
| 4 | 99.5% | 0.47% | 8 bdays |
| 6 | 99.6% | 0.41% | 6 bdays |
| 8 | 99.6% | 0.44% | 5 bdays |

**A single trade per day clears the ratified gate with 3.7× headroom on the bust limb (0.81% vs 3.0%) and 2.0× on the pass limb (99.2% vs 50%).** Across k=1→8 the pass rate moves 0.4pp and the bust rate 0.37pp; the *median time to pass* moves **6.4×**. Frequency is a pure speed lever.

> **T2 as written excludes constructs that clear the gate it was derived from.** The 3–8/day band describes a 3-to-12-day pass; it is not an admissibility requirement.

---

## §2 — T7 re-derived: $275 is 1.27–1.55× tighter than the ratified ceiling

T7 fixes risk ≤$275/trade "at ≤1% failure". The ratified Part A ceiling is **3.0%**. Both limbs of the gate applied (bust ≤ceiling **and** pass ≥50%), `w=0.55 b=2.0`:

| trades/day | max risk @ 1.0% (spec) | max risk @ 3.0% (ratified) | widening |
|---|---|---|---|
| 1 | $275 | **$350** | 1.27× |
| 2 | $275 | **$350** | 1.27× |
| 3 | $275 | **$425** | 1.55× |
| 4 | $275 | **$375** | 1.36× |
| 6 | $325 | **$425** | 1.31× |
| 8 | $325 | **$425** | 1.31× |

The sibling flagged its own tolerance-dependence ("the $275 figure is tolerance-dependent … at a 5% tolerance it rises materially"). Quantified: at the gate that actually governs, the size cap is **$350–$425**, i.e. 0.35–0.43% of account rather than 0.275%.

---

## §3 — The load-bearing result: the activity rule is the entire eval blocker

Neither sibling carried the duty-cycle axis. `w=0.55 b=2.0 r=$275 k=3`, sweeping duty against the inactivity barrier ON (no token trade) and OFF (R8 delivered):

| duty cycle | **token trade delivered** |  | **no token trade** |  |  | Δ pass |
|---|---|---|---|---|---|---|
| | pass | median | pass | deleted | median | |
| 1.00 | 99.4% | 12 bd | 99.4% | 0.0% | 12 bd | +0.0pp |
| 0.60 | 99.5% | 20 bd | 87.3% | 12.3% | 19 bd | +12.1pp |
| 0.40 | 99.5% | 29 bd | 37.7% | 62.1% | 22 bd | +61.8pp |
| 0.30 | 99.4% | 39 bd | 12.8% | 87.1% | 22 bd | +86.6pp |
| **0.22** ← incumbent book | **99.3%** | **53 bd (~2.5 mo)** | **3.0%** | **96.9%** | 21 bd | **+96.3pp** |
| 0.15 | 99.5% | 78 bd (~3.7 mo) | 0.5% | 99.5% | 18 bd | +99.0pp |

Two facts, both clean:

1. **With the token trade, duty cycle does not affect whether you pass — only how long it takes.** Pass sits at 99.3–99.5% across a 6.7× range of cadence. Time-to-pass stretches 12 → 78 business days; even the sparsest column resolves in under four months, well inside the frozen 1,500-day horizon.
2. **Without it, cadence is fatal and the cause is deletion, not drawdown.** At the incumbent book's measured 0.22 duty, 96.9% of paths die by account deletion while the bust rate stays under 1%. The failure mode is administrative, not financial.

> The eval-phase blocker that the venue de-scope rested on is worth **+96.3pp of pass probability**, and the instrument that discharges it (R8, ~13 maintenance trades/yr at ~$1.82 RT ≈ **$24/yr**) is the cheapest unblock in the estate. [`ADR 2026-08-04 §6`](../../../../docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md) named this as a live risk — *"the eval half of this de-scope was purchased against a blocker that had a $24/year fix"* — and set it as the cheapest §4 trigger (T1). This is that risk, priced.

---

## §4 — T1 re-derived: 0.40R is the inversion threshold, not the admissibility floor

Lowest edge still clearing **both** ratified limbs, token trade on:

| w | b | edge | k=1 max risk / pass | k=3 max risk / pass |
|---|---|---|---|---|
| 0.55 | 2.0 | +0.650R | $350 / 97.7% | $425 / 97.9% |
| 0.50 | 2.0 | +0.500R | $250 / 97.7% | $275 / 97.7% |
| 0.45 | 2.0 | +0.350R | $175 / 98.1% | $175 / 98.6% |
| 0.55 | 1.2 | +0.210R | $175 / 98.2% | $175 / 98.2% |
| 0.40 | 2.0 | +0.200R | $100 / 97.2% | $100 / 98.0% |
| **0.50** | **1.2** | **+0.100R** | **$75 / 96.3%** | **$75 / 98.7%** |
| 0.35 | 2.0 | +0.050R | — none — | — none — |
| 0.45 | 1.2 | −0.010R | — none — | — none — |

Admissibility reaches down to roughly **+0.10R**, four times below T1's stated 0.40R — at much smaller size. The sibling's 0.40R finding is real but is a different claim: it is the level below which *extra frequency stops helping* (k=1 and k=3 max risk converge from +0.35R down). **0.40R is where the frequency lever dies, not where admissibility dies.**

---

## §5 — What this does NOT establish

1. **Independence is assumed, and the error is optimistic.** Trades and days are drawn independently; real strategies cluster losses. Every pass rate above is an upper bound. **The §3 duty-cycle finding is the exception** — the inactivity barrier is P&L-independent, so the +96.3pp is robust to clustering in a way the 99% pass rates are not.
2. **It is a model of a strategy *class*, not a measurement of any construct.** Fixed-fractional risk, hard stops, independent non-overlapping entries. The incumbent c1 legs violate all three (ATR-sized, pyramided, overlapping); nothing here re-measures them.
3. **Clearing the eval ≠ having edge.** These are independent bars and the gap between them is the whole point of the validation apparatus — a construct meeting this shape still owes cost-law, the DSR floor at its family's `k_intrinsic`, and the both-halves regime gate. This says what the **eval** requires.
4. **No candidate is admitted, and the sourcing bottleneck is untouched.** MNQBASE-1 closed `FALSIFIED` (intake-dry) at **mechanism admissibility** (Req 1a/1b) — the fifth consecutive pass to die there, *"never on edge size, cost, venue, or data access."* Widening the target spec does not manufacture a mechanism. See §7.
5. **Single-tier only.** `discharges_falsifier` requires ≥2 firms clearing Part A; nothing here can discharge the four-firms §4 falsifier, and §4's arithmetic is untouched.

---

## §6 — Engine cross-check (why the numbers are trustworthy)

The vectorised harness is validated against the canonical engine rather than trusted:

```
cross-check vs core/mc/simulation.simulate_path (n=3000, w=0.55 b=2.0 r=$275 k=3, horizon=400):
  bust  engine   0.57%   harness   0.57%
  pass  engine  99.43%   harness  99.43%
  max abs delta: 0.000pp
```

`dd_protection` is disabled (trigger 10.0 — the `prop_survivor_scoring` idiom) so the engine applies scale 1.0 throughout; `dd_lock_offset_usd` is set unreachable, which **is** the true eval geometry and is the device `tests/core/test_trailing_locking_boundary.py` uses for the same purpose.

**The check earned its place.** Its first run failed at 4.8pp because the verification passed `intraday_low` measured from the day's *close* rather than its *open*, inflating engine bust 9×. The engine's contract (`simulation.py` docstring: excursion "measured from that day's OPENING equity") is easy to misread and the assertion caught it. Recorded because the same misreading would silently bias any future harness that supplies this argument.

---

## §7 — Reading this against the standing record

Four constraints on a Tradeify seed construct loosened, three of them **on 2026-08-04**, and none has been screened against:

| Constraint | Was | Now |
|---|---|---|
| **S7 order-symbol occupancy** | `MNQ1!` Mon+Tue, `MYM1!` Tue+Fri occupied by the incumbent legs — killed ORB-as-cadence-leg and SLR-MYM at zero spend | Both symbols **unoccupied** — the Striker legs are withdrawn from the eval deployment |
| **Family K bank** | `K_banked(MNQ)=2` ⇒ DSR floor 0.980 against Cap 1.0, "one seat left" | [`ADR 2026-08-04`](../../../../docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md) severed `k_banked` → `k_eff`; bank is **disclosure-only**. A single pre-registered hypothesis screens at floor **0.65** |
| **T2 frequency** | 3–8 independent trades/day | **k=1 clears** (§1) |
| **T7 size** | ≤$275/trade | **$350–$425** at the ratified ceiling (§2) |


> ⚠ **Amendment 2026-08-05 — the S7 row overstates its "Now" cell.** `MNQ1!` and
> `MYM1!` are **not** released. `ops/instruments/MYM.md`'s dated 2026-08-04
> ruling (commit `62115a6`, twenty hours before this study) holds that the
> incumbent's `MYM1!` Tue+Fri claim *"is **not** thereby released — the legs are
> withdrawn from a venue, not parked, and `LEG_MAP` is untouched; any candidate
> reasoning from a freed `MYM1!` must first get fork **F2** (rail disposition)
> ruled."* `ops/instruments/MNQ.md` carries the parallel constraint for `MNQ1!`
> and rules that a future ORB-MNQ re-open *"must clear S7, not argue bank
> headroom."* Read the row as **S7 status pending F2 (2026-08-08)**, not
> "unoccupied". The §7 caveat below covers finding *rate*; it does not cover this
> admissibility claim.

**But the widening does not resolve the bottleneck, and should not be read as doing so.** Every one of the last five sourcing passes died on Requirement 1 — a named counterparty class under mandate, or evidence-robustness in lieu of one. None died on frequency, size, K, venue, or symbol occupancy. Loosening four limbs that were never the proximate cause of a single closure changes what would be *admissible if found*; it does not change the finding rate. MNQBASE-1's own scope line stands: the well is dry *on the operator's timeline, via the channels declared* — and **H-MNQBASE-1 remains unresolved, not refuted** (L1 never fired, L4 was never reached).

The one thing here that is immediately actionable is **R8**, and it is not a research item.

---

## §8 — Reproduce

```bash
cd lab/analysis/c1/tradeify_seed_target_spec_2026-08-04
python run_seed_spec.py --verify   # engine cross-check, ~20s
python run_seed_spec.py            # full run, ~3 min, writes RESULTS.json
python run_seed_spec.py --quick    # smoke check
```

Stdlib + numpy only. Deterministic under the pinned seeds. No vendor data, no repo panels, no network. The `--verify` path imports `core/mc/simulation.py` and is the only repo dependency.
