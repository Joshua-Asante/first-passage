# `MNQFLOW-1` — does ORB-MNQ-1's trigger boundary carry an order-book signature at all?

**Status:** `FROZEN — PULL NOT AUTHORIZED.` This is the artifact Avenue A §6 requires before any
order-flow pull. It clears the qualifying triple (§3) and carries the cost dry-run (§4). **The
remaining gate is an operator sign-off, which this document does not grant and I do not self-issue.**
Frozen before any book-state quantity has been computed for this construct anywhere.
**Date:** 2026-08-05 · **Authorization to design:** operator, *"re-aim the probe at ORB-MNQ-1."*
**Cost of everything so far:** **$0.00** (estimates only; `metadata.get_cost` does not bill).
**Cost if authorized:** **$0.00** — the pull sits inside the subscription's rolling entitlement (§4).
**K_intrinsic = 0** — reasoned in §6, not asserted.

---

## §0 — Rule-0 reads (executed this session, at the line level)

| Source | What it pins |
|---|---|
| [`docs/briefs/programs/2026-07-24-avenue-a-microstructure-scoping.md`](../../../../docs/briefs/programs/2026-07-24-avenue-a-microstructure-scoping.md) **read in full** | §6 qualifying triple (verbatim in §3). ⚠ **§2's fork table killed my first design before I wrote it**: "Execution-microstructure — MBP-10 depth to model ORB-MNQ fills more finely → **low marginal value, the data answers a question already answered**." Any slippage/fill-validation framing is that fork and fails condition 2 |
| [`ops/instruments/MNQ.md`](../../../../ops/instruments/MNQ.md) F2 GUARD (L93) | Verbatim: ORB filter slices *"may appear **ONLY** inside this DEAD list, never in a findings or edge tier… **Highest-risk laundering move on this instrument**."* Binds §5 FM-1 |
| same, N1 + Stage-7 rider | ORB-MNQ-1: annSR **+0.890** (Bulenox) / **+0.835** (Tradeify), DSR 0.9754, `K_eff=2`. Four conditioning gates (N6/N8/N9/N10) **all FALSIFIED** |
| [`lab/analysis/orb/orb_mnq_2026-07/RESULTS_decay_monitor.md`](../../orb/orb_mnq_2026-07/RESULTS_decay_monitor.md) | **The edge-side monitor already exists and is calibrated** — PF-CUSUM, 2021+ baseline PF 1.1691, floor 1.0855, `block_size=2`. It is a *seed*: it fires on realized P&L, i.e. **after** decay has already been paid for. No structural observable accompanies it |
| [`lab/analysis/orb/orb_universe_2026-06-22/orb_lib.py`](../../orb/orb_universe_2026-06-22/orb_lib.py) L248-273 | The frozen construct, read at the function level: OR = first `or_bars=2` session bars (15m ⇒ **09:30–10:00 ET**); entry on the **first subsequent bar** breaking OR hi/lo (touch-fill); stop = opposite OR extreme; exit at session close. **The trigger can fire any time from 10:00 to the close** — this killed the "ORB hour" window and forced the §4 session-scope arithmetic |
| [`lab/analysis/orb/orb_mnq_2026-07/RESULTS_tv_export_realism.md`](../../orb/orb_mnq_2026-07/RESULTS_tv_export_realism.md) (via N2) | The 07-21 audit measured **tick penetration** (median 81 ticks through the trigger, 0.7% ≤1 tick, zero non-traded levels). It is silent on **book geometry**. This is the boundary this probe must not cross (§3 condition 2) |
| [`docs/notes/2026-08-05-order-flow-probe-governance-question.md`](../../../../docs/notes/2026-08-05-order-flow-probe-governance-question.md) | The governance question this design answers by construction rather than by ruling |

**Profile consult (executed):** `python scripts/instrument_profiles.py cell MNQ ict-liquidity` →
binding bar `index-intraday-ohlcv-directional-timing-2026-07-21`, addressed in §3.

**Dedup attestation (executed).** `rg --no-ignore -il "tbbo|queue imbalance|order.flow"` over
`rejected_candidates.md`, `rejected_signals.md`, `discovery_manifests/` → one file, and **every hit
is supportive rather than adverse**: L176/L189 name *"a genuine intraday 0DTE order-flow series"* and
L303 names *"true order-flow or **absorption** measures"* as **valid re-proposal routes**. **No entry
rejects a book-geometry diagnostic at an ORB boundary.** Nearest adverse prior is the a4 fork
(category-splitting is non-identifying) — this construct splits no categories (§3.1).

---

## §1 — The question, and why it is the honest one

The four conditioning gates on ORB-MNQ-1 all failed, and F2 forbids a fifth. The unasked question
underneath them: **is there a microstructural substrate at the trigger boundary at all?** Every prior
attempt assumed one existed and searched for a *filter*; none asked whether the book at ORB's
breakout level looks any different from an arbitrary moment in the same session.

That question is diagnostic rather than generative. **A null is the more useful outcome**: it would
mean the four falsifications share a single cause (no substrate to condition on), which is a real
finding about the survivor and directly informs its standing at the 2026-08-08 decay review. A
positive is a *monitoring* observable — and per `lesson_leading_indicator_pnl_gate_rationalization`
it routes to a **watchlist + forward tripwire**, never an overlay.

**H-MNQFLOW-1.** At ORB-MNQ-1's own frozen trigger moments, the L1 order book on MNQ exhibits a size
asymmetry distinguishable from matched non-trigger moments in the same sessions.

---

## §2 — The frozen construct

| # | Element | Frozen value | Source |
|---|---|---|---|
| S1 | Instrument / schema / window | `MNQ.v.0`, **`tbbo`**, 2025-08-06 → 2026-08-04 (1 yr) | §4 (schema choice reasoned, not defaulted) |
| S2 | Event set | ORB-MNQ-1's trigger timestamps, reconstructed by running the **existing committed `orb_lib.orb_backtest` unmodified** (`or_bars=2`, filters off) on the free on-disk MNQ 1m panel | orb_lib L248-273 |
| S3 | Feature | **L1 size asymmetry** `A = (bid_sz − ask_sz) / (bid_sz + ask_sz)` at the touch, signed toward the breakout direction (so an upside and a downside break are comparable), averaged over the **60 s preceding** the trigger timestamp | book geometry; direction-normalized so the test is about structure, not direction |
| S4 | Control | For each trigger, **k=5 matched control moments** drawn from the *same session*, at least 15 min from the trigger, sampled to match the trigger's time-of-day distribution across the panel | matched design; controls the intraday liquidity U-shape, which is the obvious confound |
| S5 | Statistic | Mean `A_trigger` − mean `A_control`, with a **session-block bootstrap** 95% CI (10,000 reps, seed 20260805; blocks = sessions, since all of a session's moments share its regime) | inherited bootstrap idiom |
| S6 | Placebo | Sign-shuffle: permute the trigger/control labels **within session**, 1,000 reps, same seed → p95 threshold | the WLEGB discipline — the limb that caught a false positive there |
| S7 | Coverage guard | Report the fraction of ORB triggers with ≥1 TBBO quote in the 60 s window; if < 90%, the coverage limitation is the headline, not the effect | honesty limb |

**Outputs (closed list):** trigger count, coverage fraction, `A_trigger` / `A_control` means, the
difference with CI, the placebo p, and the by-half split (H1/H2 of the 1-yr panel). **Nothing else** —
in particular **no per-trade table, no win/loss split, no MFE/MAE surface** (§5 FM-1/FM-2).

---

## §3 — The Avenue A §6 qualifying triple, cleared condition by condition

> *"1. Depth-shape, not category … 2. Not fill-trivial … 3. Survivor-tied — improves or **monitors**
> ORB-MNQ-1 … not blind discovery."*

**1 — Depth-shape, not category. ✓** `A` is resting-size geometry at the touch. It attributes nothing
to participant class, so the a4 prior (*"net imbalance only → non-identifying"* for **categories**)
does not reach it. Avenue A §5 explicitly forbids over-reading a4 as killing all microstructure;
this construct is on the identifiable side of that line.

**2 — Not fill-trivial. ✓, and this is the condition I nearly failed.** My first design was slippage
validation; Avenue A §2 already ruled that fork *"low marginal value — answers a question already
answered."* **This construct makes no fill, slippage, or execution claim and its output cannot inform
one**: it never touches fill price, never compares to the 1-tick model, and is measured on a 60 s
*pre-trigger* window — before any fill exists. The 07-21 audit measured tick penetration; `A`
measures book asymmetry. Disjoint quantities, disjoint questions.

**3 — Survivor-tied. ✓** Measured **at ORB-MNQ-1's own frozen trigger timestamps**, generated by its
own committed backtest. It is the *"monitors"* limb, not *"improves"*: the deliverable is a structural
diagnostic of the named survivor, feeding its 08-08 decay review and (if positive) accompanying the
existing PF-CUSUM as the constraint observable that monitor lacks. Nothing here is blind discovery —
without ORB-MNQ-1 there are no events to measure.

**F2 guard — the compliance argument, stated as the load-bearing one.** The guard bars ORB filter
slices from any findings tier. This construct **cannot become a filter by construction**, because it
**never conditions on outcome**: triggers are compared to *non-trigger moments*, never winners to
losers. There is no cell in the output that says "trades with high `A` did better," because trade
results are not read at all. §5 FM-1 makes that a forbidden move rather than merely an omission.

**Domain bar (2026-07-21), route 2.** Order-flow modality, per its own text and the two supportive
`rejected_candidates` entries (§0 dedup). The parenthesised rider — *"don't buy explanatory data
before a survivor"* — is satisfied on both limbs: **there is a survivor tie** (condition 3) **and
nothing is bought** (§4, $0.00 inside entitlement).

---

## §4 — Cost dry-run, and a defect in the gate's own premise

All estimates executed this session (`metadata.get_cost`, free, zero pulls):

| Schema | Window | Cost | Bytes | ORB events reachable |
|---|---|---|---|---|
| `mbp-10` | 1 RTH day (billable era) | **$3.97** | 8.52 GB | ~1 |
| `mbp-10` | whole **$125 credit** | $125.00 | ~270 GB | **~31** |
| **`tbbo`** | **1 year, 2025-08-06→2026-08-04** | **$0.0000** | **20.73 GB** | **~250** |

⚠ **Avenue A §6 assumed "a few-day MBP-10 pull" inside the $125 credit. Measured, a few days of
MBP-10 is 3–5 ORB triggers, and the *entire* credit buys ~31.** The gate is **reachable on cost but
not on power** for MBP-10 — a defect in its premise, surfaced by measurement, recorded here rather
than worked around silently. `tbbo` reaches ~250 events at **$0.00**, an 8× larger sample for no
spend, and is therefore the schema this pre-registration names.

**Two honest consequences of that substitution, neither hidden:**

1. **TBBO is L1 only.** This tests the **top-of-book** version of H. A null does **not** exclude a
   signature deeper in the book; §7's disposition says so explicitly.
2. **The gate's letter says "MBP-10."** I am applying it to a **TBBO** pull deliberately — the
   governance concern is the *modality*, not the schema, and holding a cheaper schema to the same
   triple is the conservative reading. Flagged so the operator can reject the substitution if they
   read §6 narrowly.

**Transport risk, declared:** 20.73 GB. A 156 MB stream previously died mid-transfer on this link.
The pull may need day-chunking; that is an operational detail, not a cost or governance one.

---

## §5 — Forbidden moves

- **FM-1 — Reading ORB trade outcomes at any point.** No win/loss split, no PnL join, no
  outcome-conditioned cell. **This is the F2 guard's operative content here**; violating it converts
  a diagnostic into a fifth conditioning gate wearing a new label.
- **FM-2 — Emitting any per-trade or excursion surface** a successor could tune a filter on.
- **FM-3 — Re-framing a positive as tradeable.** It routes to watchlist + forward tripwire
  (`lesson_leading_indicator_pnl_gate_rationalization`), never an overlay or gate.
- **FM-4 — Any second cell**: no MBP-10 arm, no alternate window/threshold/normalization sweep, no
  second instrument. Each is a new axis needing fresh authorization.
- **FM-5 — Pulling before operator sign-off.** Avenue A §6's final clause. Not mine to waive.
- **FM-6 — Adjusting any §7 threshold, the seed, the control design, or the placebo after data.**

---

## §6 — Why `K_intrinsic = 0` (reasoned, not asserted)

Same posture as the Step-1 event-ceiling study (K=0): this measures a **structural property**, not a
strategy, and **cannot emit a tradeable rule** — FM-1 removes outcome data from the design, so no
edge estimate exists to be selection-inflated. `K_banked(MNQ) = 4` is disclosed (not summed;
ADR 2026-08-04). ⚠ **If a positive result is ever converted into a gate or filter, that conversion is
a fresh K-bound axis** requiring its own pre-registration — it does not inherit this K=0.

---

## §7 — Verdict gates (frozen; precedence as listed)

| # | Condition | Verdict | Disposition |
|---|---|---|---|
| W4 | coverage < 90% (S7) | `VOID-COVERAGE` | Report coverage only; no effect quoted. Not re-cut to chase coverage |
| W3 | CI includes 0 | **`FALSIFIED`** | **The likely branch (§8).** No L1 substrate at the boundary — the four gate falsifications plausibly share one cause. Feeds the 08-08 decay review; does **not** by itself demote ORB-MNQ-1 (lifecycle moves are operator GO) |
| W2 | CI excludes 0 but effect ≤ placebo p95 | `AMBIGUOUS-CONFOUND` | Same disposition as W3; the asymmetry is the intraday liquidity shape, not the boundary |
| W1 | CI excludes 0 ∧ effect > placebo p95 | `RESOLVED` | A structural observable exists → **watchlist + forward tripwire**, named as a candidate companion to the existing PF-CUSUM. **Opens nothing**; any gate use is a fresh K-bound axis (§6) |

A W1 that fails the by-half split reports `RESOLVED-NONSTATIONARY` with W1's disposition plus the
instability flagged. **Board write owed in every branch.**

## §8 — Pre-registered expectation

**W3 (null) is the most likely single branch.** Four independent conditioning gates already failed on
this construct; the simplest explanation consistent with that record is that the boundary carries no
conditionable structure, and L1 asymmetry is a thin instrument for detecting one if it exists deeper.
Recorded now so a null reads as a discharged prediction and a positive cannot be retrofitted as
expected. **A null is genuinely informative here** — it converts four separate falsifications into
one explanation.

---

## §9 — Protocol order (violations void the run)

1. This file committed (**freeze**) — done before any book quantity exists.
2. **OPERATOR SIGN-OFF on the pull** — Avenue A §6's remaining clause, and the TBBO-for-MBP-10
   substitution (§4). **Not granted here.**
3. Harness + hand-computed unit tests; all pass before the runner reads a real quote.
4. Single run. RESULTS discharges exactly one §7 branch. Boards written.

## §10 — Audit hooks

```bash
# Freeze ordering
git log --oneline -- lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/PREREG.md | tail -1

# The triple this clears, and the fork that killed the first design
grep -n "Survivor-tied" docs/briefs/programs/2026-07-24-avenue-a-microstructure-scoping.md
grep -n "answers a question already answered" docs/briefs/programs/2026-07-24-avenue-a-microstructure-scoping.md

# The F2 guard FM-1 exists to satisfy
grep -n "F2 GUARD" ops/instruments/MNQ.md

# The frozen construct's OR definition (expect or_bars=2, first subsequent break)
grep -n "or_bars=2" lab/analysis/orb/orb_universe_2026-06-22/orb_lib.py

# Cost dry-run reproduction (FREE; never add `pull`)
python lab/databento_fetch/db_fetch.py estimate --symbols MNQ.v.0 --stype continuous \
  --schema tbbo --start 2025-08-06 --end 2026-08-04
# Expect: cost $0.0000, ~20.73 GB, ~259M records
```

---

## Amendment log (append-only — the frozen §§1–9 above are never edited, Trap #12)

- **2026-08-05 — FROZEN.** Authored and committed before any book-state quantity existed for this
  construct. Pull **not** authorized at freeze time.
- **2026-08-05 — OPERATOR SIGN-OFF GRANTED; §9 step 2 DISCHARGED.** Operator, in session:
  *"approved, we will run the probe in the next session."* This discharges Avenue A §6's final
  clause (*"AND an operator sign-off"*) and, explicitly, **the §4 TBBO-for-MBP-10 schema
  substitution**, which was flagged for rejection and was not rejected. **What is now authorized:**
  the single `tbbo` pull named in S1 (`MNQ.v.0`, 2025-08-06 → 2026-08-04, estimated **$0.0000**).
  **What is still NOT authorized and needs its own decision:** any MBP-10 pull, any second cell or
  arm (§5 FM-4), any window beyond S1's, and any conversion of a positive result into a gate or
  filter (§6 — a fresh K-bound axis). **Execution deferred to the next session by operator
  election.** §9 steps 3–4 (unit tests before the runner reads a real quote; single run; one §7
  branch) remain owed and are unchanged.
- **2026-08-05 — RECONCILED.** The sign-off above was recorded in a session (`claude/parallel-
  workstreams-followups`, commit `5c8ecfc`) whose branch had already been merged (PR #644) by the
  time it was pushed — it never reached `origin/main`. A separate, later session ([PR #645
  governance ruling](../../../../docs/notes/2026-08-05-order-flow-probe-governance-question.md) §7)
  worked from `origin/main` without it and independently re-stated this clause as outstanding
  (STATE.md queue item 1). Surfaced by the daily repo-truth sync; operator reconfirmed the same day
  that the sign-off stands. No change to what is authorized — this entry lands the record, not a
  new grant.
- **2026-08-05 — RUN EXECUTED; §9 steps 3–4 DISCHARGED; verdict `RESOLVED` (W1).** 27
  hand-computed unit tests green before the runner read a real quote; single run; exactly one §7
  branch discharged. Difference **−0.009367**, CI95 **[−0.013430, −0.005354]**, placebo |.| p95
  **0.004166** (p_emp 0.000), coverage **100%** (255/255); halves agree, so the
  `RESOLVED-NONSTATIONARY` rider does not fire. **§8's pre-registered expectation (W3 null) was
  WRONG** — recorded as a failed prediction, not retrofitted. Cost **$0.00**; `K_intrinsic=0`
  unchanged; `K_banked(MNQ)=5` disclosed. Disposition per §7 W1: **watchlist + forward tripwire;
  opens nothing.** [`RESULTS.md`](RESULTS.md)
- **2026-08-05 — RECORDED INTERPRETATION (operator may reject): the S1/S2 panel-vintage conflict.**
  S1 freezes the window to 2026-08-04; the "free on-disk MNQ 1m panel" S2 names ended
  **2026-07-15**, a 14-session shortfall — two frozen elements in conflict, surfaced rather than
  silently resolved. Read taken: S2's emphasis is the *engine* ("the existing committed
  `orb_lib.orb_backtest` unmodified") and the *cost posture* ("free"), while S1 owns the window; so
  the 1m panel was refreshed across S1's exact window (`ohlcv-1m`, cheapest schema, **$0.0000**,
  same symbology, strictly inside S1 and never beyond it). This makes the run match its frozen
  design rather than shrink it, but it **is a second pull the sign-off did not name**. Flagged so
  it can be rejected; rejecting it re-scopes the run to 2025-08-06 → 2026-07-15.
- **2026-08-05 — DECLARED BEFORE DATA (recorded for audit; neither was chosen after seeing a
  result).** (i) **Trigger-timestamp resolution:** the engine resolves a breakout to a 15m bar and
  S3 measures "at the touch", so the touch is localized to the 1m bar inside the engine's entry bar
  that first crosses the OR level, with the window `[t−60s, t)` — strictly before the touch minute,
  so no look-ahead. The coarser 15m reading was **not** also computed (FM-4). (ii) **Two-sidedness:**
  the CI limb is two-sided, so the placebo limb is taken two-sided too (|observed| vs p95 of
  |placebo|).
- **2026-08-05 — PANEL-REFRESH INTERPRETATION RATIFIED; the rejection branch is CLOSED.** Operator,
  in session: *"the panel refresh is fine, keep it."* The `ohlcv-1m` refresh across S1's exact
  window is **accepted as within the sign-off's scope**, so the run's event set stands at its full
  frozen window **2025-08-06 → 2026-08-04** (255 triggers). The alternative branch flagged two
  entries above — re-scoping to 2025-08-06 → 2026-07-15 — is **not taken and is now closed**;
  the `RESOLVED` (W1) verdict and every number in [`RESULTS.md`](RESULTS.md) are unaffected,
  because they were computed on the accepted window. **What this does NOT extend to** (unchanged
  from the original sign-off): any MBP-10 pull, any second cell or arm (FM-4), any window beyond
  S1's, and any conversion of the positive result into a gate or filter (§6 — a fresh K-bound
  axis). Ratifies a *transport/substrate* reading, not a widening of the authorization.
