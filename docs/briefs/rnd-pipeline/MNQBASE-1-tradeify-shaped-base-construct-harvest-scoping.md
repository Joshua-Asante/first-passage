# `MNQBASE-1` — Tradeify-shaped base construct: harvest intake (scoping)

**Status:** `SCOPED` — intake filter only. **No candidate admitted, no manifest opened, no K bound,
$0 committed.** Screening a candidate against §2 consumes nothing; each *admitted* candidate pays
its own `K_intrinsic` at its own pre-registration.
**Live target:** **Tradeify Select 100K evaluation — ACTIVE** (operator clarification 2026-08-04; see §1 ⚠).
**Deadline pressure:** operator intends a deployable construct **within the week**, so §7 is ordered
by information-per-hour, not by completeness.
**Loop:** Inquire-phase, harvest intake. **Authored:** 2026-08-04 · Claude Code (Opus 5), operator-directed.

> ⚠ **READER INTERCEPT 2026-08-06 — §2.1 T2 / T6-rider / T7 reuse RETIRED or SUPERSEDED.**
> The standing Tradeify Select 100K **mechanism-shape screen** is now
> [`docs/spec/2026-08-05-eval-mechanism-shape-screen.md`](../../spec/2026-08-05-eval-mechanism-shape-screen.md)
> (`RATIFIED 2026-08-06`, EM0–EM5). Per that spec's §7 ruling:
> **T2** ("3–8 independent trades/day") — **RETIRE** reuse (replaced by **EM4** weekly cadence);
> **T6** "trivially satisfied by T2" rider — **RETIRE** (idle clock is the binding cadence limb);
> **T7** flat "$275/trade" — **SUPERSEDE** by **EM2** edge-indexed frontier;
> **T1 / T3 / T4 / T5** — **CARRY**. Frozen body below is historical; do not quote T2/T6-rider/T7
> as live screening requirements. Closure STOP / intake-dry verdict unchanged.

---

## §0 — Rule-0 reads (verified this session 2026-08-04)

- **[`core/firm_rules.py`](../../../core/firm_rules.py) `Tradeify_Select_100K` L321-333 @ `2345095`** — the live target geometry, read directly rather than from prose: `dd_type: trailing_locking`, `starting_balance: 100_000`, `max_dd_pct: 3.0` (**$3,000**), `profit_target_pct: 6.0` (**$6,000**), `min_trading_days: 3`, `weekend_holds: False`, **`inactivity_max_idle_days: 5`** (*"VENUE FACT: >=1 trade/week eval+funded (art. 10468318); not absorbing"*), `micro_contract_cap: 80`, **`cost_per_side_usd: 0.91`**, `consistency_rule_pct: 40.0`. **Eval carries no drawdown lock** — `dd_lock_offset_usd: 100` encodes a mechanism the evaluation does not have ([`lock-correction ADR`](../../adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md)); the eval is a pure EOD fixed-$ trail, breach tested **intraday**.
- **[`lab/analysis/c1/eval_inverse_requirements_2026-08-03/RESULTS.md`](../../../lab/analysis/c1/eval_inverse_requirements_2026-08-03/RESULTS.md) @ `1dcde85`** — the shape spec, **computed on exactly the geometry above**, so it is directly on-point rather than a borrowed proxy. §2: `μ_max = k × r_max × E` — **linear in frequency, capped in size**; max risk/trade is flat at **$275** across k=1→4. §2a: **the result INVERTS below ~0.40R** — at 0.139R (the Aegis→6J profile, n=152) max risk/trade *falls* from $100 to $50 as k rises. §4: hard stops are load-bearing — failure goes **0.6% → 8.0%** when 5% of losses gap 5×. §5: the incumbent book sat at **0.35 trades/calendar-day against 3–8 needed**.
- **[`ops/instruments/MNQ.md`](../../../ops/instruments/MNQ.md) @ `55adcaa`** — read in full. **N1** ORB cleared the full Gen-2 pipeline but at ~**0.09R/trade** gross; **N3** both ORB exit-redesign spaces are pre-killed by an order-free counterfactual; **N5** Baltussen intraday momentum is statistically ABSENT on modern MNQ (OOS **−0.327 bp**); **N6** modern cost hurdle **3.01 bp/session**; **N8** (as narrowed today) the ICT weekly bias is a **weekly-bar fact only**; **N9** liquidity pools are anti-attractors on three instruments; **N10** (as superseded today) the K arithmetic. **The DEAD list is the search-space constraint** and is quoted in §2.3. **F2 GUARD** binds §5.
- **[`ops/instruments/MECHANISMS.md`](../../../ops/instruments/MECHANISMS.md) @ `55adcaa`** — 17 registered classes, enumerated for the §2.3 dedup: opening-range-continuation · opening-range-breakout · intraday-momentum · opening-pressure · event-window-reversal · turn-of-month · trend-following · naive-direction-mirror · compression-gated-breakout · regime-overlay · band-pierce-continuation · ict-liquidity · index-dispersion · venue-transfer · mean-reversion-fade · day-of-week-selection-gate · commodity-carry-term-structure.
- **[`docs/methodology/strategy_harvest.md`](../../methodology/strategy_harvest.md) @ `2ef7405`** — the five admission Requirements **as amended today**: Req 1a's four clauses (WHO = a *constraint* not a preference; WHEN declared ex ante; WHY it survives; HOW it dies), Req 1b's four-limb evidence bar, Req 2 δ/σ cohort-cited, **Req 3 now a DISCLOSURE not a gate**, Req 4 UNSCREENABLE routing, Req 5 cost-law. Clause K now reads `K_eff = K_intrinsic`.
- **[`docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md`](../../adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md) §2-A @ `0f36c3a`** — *"Preference/behavioral stories ('retail chases', 'stops get hunted') no longer satisfy 1a — they route to 1b or die."* This is the single most common way a fast-timeline candidate will fail, and it fails **before** any data is read.
- **[`docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md`](../../adr/2026-08-04-family-k-bank-disclosure-not-gate.md) @ `2ef7405`** (`Accepted`) — `K_eff = K_intrinsic`; a single pre-registered hypothesis screens at floor **0.650**. `K_banked(MNQ) = 2`, **disclosed here per Req 3 and not gating**.
- **[`ops/prop_envelope_default.md`](../../../ops/prop_envelope_default.md) @ `cd8b617`** — E1 build target **16:00 ET**; Tradeify's own deadline is **16:45 ET** (12:59 holiday-short). Building to 16:00 keeps the construct portable across all four friendly firms at no cost.
- **[`docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md`](../../adr/2026-08-04-tradeify-venue-descope-eval-included.md) @ `62115a6`** — read in full. **⚠ This ADR's text diverges from the live premise of this brief — see §1.**

---

## §1 — Context

### ⚠ 1.1 A recorded divergence, flagged before anything is built on it

The operator clarified in session (2026-08-04) that the **Select 100K evaluation is still live** —
the Striker strategies were de-scoped from the eval, not the eval itself — and intends to deploy a
Tradeify-compatible construct this week. **This brief proceeds on that reading**, which is the
operator's to set.

**Read against the ADR body rather than its headline, the divergence is narrow and specific.** Its
**Decision** (§2, first clause) is *already* Striker-scoped and matches the clarification exactly:

> *"`Tradeify_Select_100K` is no longer a deployment destination **for the locked Striker book**;
> the two Striker legs are withdrawn from the c1 eval deployment…"*

The conflict is with the **third clause of that same sentence** — *"…and no further work is
authorized whose sole justification is reaching, holding, or passing a Tradeify account"* — which,
read literally, bars this brief. The ADR's **title** ("evaluation included") and its decision-driver
sentence carry the same venue-wide framing. **Everything else in the ADR is compatible with the
operator's reading**, and its **§5 forbidden moves bar none of what this brief does** (they bar
lifecycle demotion, pre-empting §4, tearing down the rail or account, widening to unmeasured firms,
and erasing the 08-02 measurements — none of which occur here).

**Recommended: a narrow ADR addendum amending Decision clause 3 and the title from "venue +
evaluation" to "the locked Striker book at this venue"** — leaving the funded-phase de-scope, the
§4/F1 fork, and every §5 move intact. Not authored here; it is an operator decision artifact, and §7
does not wait on it. Recorded rather than absorbed silently because several live artifacts inherit
the wider reading: `STATE.md`'s queue-reset note (*"B7-REFIRE Stage 1 stays permanently owed and
permanently undischargeable at this venue"*), `MNQ.md`'s status line (*"no longer a live c1
leg…now has no venue"*), and forks **F2** / **F3**.

**The two readings are less far apart than they look, which is why the pivot is coherent rather than
contradictory.** One of the ADR's stated eval-phase grounds was `inactivity_max_idle_days=5` priced
at **92.6–97.6% path death**, with *"the only ≥90%-of-weeks cadence candidate screen-dead."* That is
a measurement about **the book we had** — Striker at a 22% duty cycle, 0.35 trades/calendar-day —
not about the venue. A construct meeting §2's frequency requirement satisfies a 5-day inactivity
rule ~40× over. **The de-scope measured that our strategies did not fit; this brief attacks that
premise instead of the venue.**

### 1.2 What changed the moment the eval came back into scope

| | Under "eval de-scoped" | **Under the live eval** |
|---|---|---|
| Cost basis | unanchored pending F3 | **Tradeify $0.91/side**, `rt_pt` 1.41 — pinned |
| Target geometry | none | **Select 100K**, and the shape spec was computed on it |
| Research gating | behind F3 (2026-08-08) | **not gated** — this is the operator's "do not let the board slow research" |
| **`MNQ1!` occupancy (S7)** | Striker leg occupied it | **UNOCCUPIED** — the Striker legs are withdrawn |

**That last row is the largest and least obvious unlock.** Order-symbol occupancy (S7 / `SLR-MYM-1`
F1) is a *position-netting* fact: one net position per symbol per account. It terminated
`ORB-MNQ-1`'s cadence role on 2026-08-04 — *"the property that clears the ≥90%-of-weeks floor (fires
MNQ daily) is the SAME property that fails S7 (occupies `MNQ1!` on every session the incumbent can
fire)."* **With the Striker legs withdrawn, that collision no longer exists.** A new MNQ construct
has the full 80-micro eval cap and an empty symbol. This is not an argument to revive ORB — its
~0.09R edge fails §2a independently, on arithmetic S7 never touched — but it removes a structural
constraint from *every* future MNQ candidate.

### 1.3 The gap, stated precisely

The corpus has repeatedly measured **per-trade edge** and repeatedly found the same failure axis:

| | edge/trade | trades/calendar-day | independent? |
|---|---|---|---|
| **Spec (§2)** | **≥ 0.40R** | **3–8** | **required** |
| Striker NAS100→MNQ | **0.85R** — 2× the bar | 0.35 | ✗ pyramid = correlated add |
| ORB-MNQ-1 | ~0.09R — 4× *below* the inversion | ~1 | ✓ |
| D5 intraday momentum | OOS negative | high | ✓ |

**Nothing measured on MNQ has ever cleared both axes at once.** Striker has the edge and not the
frequency; ORB has the frequency and not the edge. The search target is the intersection, and it has
never been searched for directly — every prior MNQ campaign optimized edge and treated frequency as
whatever fell out.

---

## §2 — The intake filter

### 2.1 Target spec (a candidate must plausibly meet ALL)

| # | Requirement | Source | Why it binds |
|---|---|---|---|
| T1 | **edge ≥ 0.40R/trade** net of $0.91/side | shape spec §2a | below this the rope binds *harder* as frequency rises — frequency is a multiplier, never a substitute |
| T2 | **3–8 independent trades/day**, or a book of independent legs summing to it | §2, §3 | `μ_max = k × r_max × E`; the only free axis |
| T3 | **independence** — no pyramiding, no correlated adds | §2 | correlated k at risk r ≡ one trade at k·r, which collapses to the k=1 row, the worst in the table |
| T4 | **hard stops that hold** | §4 | 0.6% → 8.0% failure when stops gap; rules out illiquid instruments and gap-exposed events |
| T5 | **intraday-complete, flat by 16:00 ET** | E1 | 16:00 (not Tradeify's 16:45) keeps the construct portable across all four firms for free |
| T6 | **≥1 trade / 5 calendar days** | `inactivity_max_idle_days: 5` | trivially satisfied by T2 — recorded because it killed the prior book |
| T7 | **risk ≤ $275/trade** at ≤1% failure | §1 B3 | 0.275% of account — an order of magnitude under conventional sizing |

### 2.2 Admissibility (harvest Requirements, unchanged)

Req **1a** four clauses *or* Req **1b** four limbs · Req **2** cohort-cited δ/σ · Req **3**
`K_banked(MNQ) = 2` **disclosed, not gating** · Req **4** UNSCREENABLE never patched · Req **5**
cost-law at the Tradeify basis. Clause K at `K_eff = K_intrinsic` → floor **0.650** for a single
pre-registered hypothesis.

### 2.3 Pre-filters — kill before any data is read

A candidate is **rejected at intake**, at zero cost, if any holds:

- **P1 — edge < 0.40R.** Dead by §2a arithmetic; no frequency, sizing, or firm basis rescues it. *This alone kills ORB for this role.*
- **P2 — the mechanism is a preference/behavioral story.** "Stops get hunted", "retail chases", "the market seeks liquidity" — inadmissible under Req 1a per ADR 2026-07-26 §2-A. Routes to 1b (≥3 decades × ≥3 independent cohorts × replication ≥10yr post-discovery × no sign-reversal) or dies. **Expect most fast candidates to die here.**
- **P3 — correlated adds.** Pyramids, scale-ins, same-signal multi-entry. T3.
- **P4 — the family is already dead on MNQ.** From the ledger, not memory: `intraday-momentum` (D5, OOS −0.327 bp) · `opening-pressure` (OPENPRESS-1) · `ict-liquidity` (pools 3×, 1H 2×, 1M expectancy ≈0, **leg (b) 2026-08-04**) · `opening-range-breakout` **for this role** (ORB, P1) · the four ORB conditioning gates · end-of-day adversity (`Q-SESSCONF-1`/`Q-EODADV-1`/`Q-DRIFTEX-1`). Re-proposal requires new *mechanism* evidence, not new parameters.
- **P5 — overnight or gap-exposed.** T4/T5.
- **P6 — needs data we do not have at $0.** Databento MNQ 1m/1h/1d is free and on disk; anything requiring order-book, options, or vendor-licensed exogenous data is *scoped-not-procured* under the standing "don't buy explanatory data before a survivor justifies it" rule.

### 2.4 Dedup attestation (executed this session, pasted)

    $ grep -n "^## " ops/instruments/MECHANISMS.md        -> 17 classes, enumerated in §0
    $ (MNQ.md DEAD list read in full; families quoted in P4)

A candidate declares its **nearest existing class** or explicitly declares `NEW`; a `NEW` id lands
in `MECHANISMS.md` in the **same commit** as its pre-registration (growth rule). No class is
declared by this brief — it is an intake filter, not a candidate.

---

## §3 — Question

**Every MNQ construct measured to date fails the live eval on the same axis, and it is not the axis
the research has been optimizing.** Per-trade edge has been measured repeatedly and is sometimes
twice what the geometry needs; independent trade frequency has never been measured directly on this
instrument at all, and is where every candidate dies. **What is the actual ceiling on independent,
tradeable events per day on MNQ — and does any admissible mechanism class reach it without the
per-trade edge collapsing below the 0.40R inversion threshold?**

Symptom-only: *we keep building things that do not fit, and they miss in the same direction every
time.* The question names no construct, no gate, and no instrument substitution.

---

## §4 — Falsifiable hypothesis

**H-MNQBASE-1.** An admissible construct exists on MNQ that simultaneously clears **T1** (≥0.40R/trade
net at $0.91/side) and **T2** (≥3 independent trades/day), on databento MNQ data available at $0.

**Falsifier — frozen trigger table. §7 Step 1 is designed to fire L1 cheaply if it is going to fire.**

| # | Trigger | Threshold | Verdict |
|---|---|---|---|
| L1 | measured ceiling on independent tradeable events/day on MNQ (§7 Step 1), at any edge | **< 3/day** | **`FALSIFIED` for a single-instrument construct.** The eval is unreachable on MNQ alone and the answer is a **multi-instrument book** — which the four-firm program already wants. Routes to a book-composition question, not a better MNQ strategy |
| L2 | every candidate surviving §2.3 fails Req 1a **and** Req 1b | — | **`FALSIFIED` at intake** — the admissible-mechanism well is dry on the timeline; re-proposal needs a new sourcing channel, not more search |
| L3 | a candidate clears intake but measures edge **< 0.40R** at the Tradeify basis | — | **that candidate** is dead by P1; the campaign continues |
| L4 | a candidate clears T1 **and** T2 | — | **`RESOLVED`** — it earns a K-bound Stage-0 pre-registration of its own. **This brief does not open it** |

**Pre-registered expectation.** The corpus's own numbers say frequency is the hard axis: the
incumbent book ran at **0.35 trades/calendar-day** against 3–8 needed — an order of magnitude, not a
tuning gap. **L1 firing is the single most likely outcome**, and it is recorded here so that a
multi-leg-book conclusion reads as a pre-registered branch rather than a consolation prize.

---

## §5 — Forbidden moves

- **FM-1 — Reviving ORB for this role because S7 was relieved.** §1.2 removes a *structural* blocker; it does not touch **P1**. ORB's ~0.09R fails the inversion threshold on arithmetic that never involved S7, and its four conditioning gates and both exit redesigns are independently falsified. Tempting precisely because the S7 news is fresh.
- **FM-2 — Conditioning any candidate on `vStruct`, ICT structure, or another falsified layer** to manufacture selectivity. `Q-WLEGB-1` closed leg (b) on 2026-08-04: the weekly bias licenses *being less long*, never *being short*, and does not transfer below the weekly close.
- **FM-3 — Any ORB filter slice entering a findings tier.** Standing **F2 guard**; the highest-risk laundering move on this instrument. Friday/Monday/OR-hi/same_bar may appear only in the DEAD list.
- **FM-4 — Relaxing T1 because a candidate is "close".** 0.40R is not a preference; below it §2a *inverts* and added frequency makes the rope geometry worse. A 0.35R construct traded more often is worse than the same construct traded less often.
- **FM-5 — Letting the week's deadline lower the intake bar.** Timeline pressure is the classic reason Req 1a gets waived for a behavioral story. If nothing clears intake, **L2 is the answer** and it is a legitimate one.
- **FM-6 — Treating the shape spec's $275 / 3–8 as venue-neutral.** They are Select-100K-derived. Porting the construct to another firm requires re-running the inverse harness at that firm's geometry (~2 min, $0) — cheap, but not free of the obligation.
- **FM-7 — Spending data budget before a survivor justifies it.** P6.
- **FM-8 — Any `core/`, lock, allocation, `dd_protection`, lifecycle, Pine, rail, or `LEG_MAP` change** under this brief. It is an intake filter; it changes nothing operational. The rail stays **disarmed** and arming remains a separate operator GO under the standing M1 interlock.

---

## §6 — Gate criteria and typed dispositions

Per [ADR 2026-08-04 Iterate-closure-exit](../../adr/2026-08-04-iterate-closure-exit-mandatory.md) §2 item 2.

| Verdict | Trigger | **Disposition (pre-registered)** |
|---|---|---|
| `FALSIFIED` (single-instrument) | L1 | **ITERATE → Identify.** Entry packet: the measured event ceiling, the per-edge curve, and T1–T7. Successor question is **book composition across instruments**, not a better MNQ construct. Names, does not open |
| `FALSIFIED` (intake dry) | L2 | **STOP.** Re-proposal bar: a new *sourcing channel* (Req 1b-grade published cohort, or a constraint-based WHO not yet enumerated) — not another pass over the same classes |
| `AMBIGUOUS` | ceiling ∈ [3, 8) but only at edge < 0.40R | **ITERATE → Investigate.** The two axes are individually reachable and jointly not; packet carries both curves and the frontier between them |
| `RESOLVED` | L4 | **ITERATE → dated packet / operator decision item.** The candidate earns its own K-bound Stage-0 pre-registration at `K_intrinsic` ≥ 1, floor 0.650. **This brief opens nothing** |

**Board write** owed at closure in all four branches.

---

## §7 — Execution plan (ordered by information per hour)

**Step 1 — the reachability pre-flight, and it is the whole gate. $0, K=0, order-free.**
Measure the **ceiling on independent tradeable events per day** on MNQ: how many non-overlapping,
hard-stoppable, intraday-complete setups exist per session at each candidate edge level, using only
bar geometry (no mechanism, no signal, no P&L). This bounds the entire search **before** any
candidate is sourced: if the ceiling is < 3/day, **L1 fires** and the answer is a multi-leg book
regardless of which mechanism anyone proposes. It is the same instrument as `Q-ICTEXP-1`'s ceiling
limb — a strict upper bound that no construct can beat — and it needs its own frozen
pre-registration before it runs.

**Step 2 — intake pass.** Apply §2.3 P1–P6 to the candidate set, sourced per `strategy_harvest.md`
§2.3's ranked channels. Record every rejection and its clause; a dry well is **L2**, a legitimate
verdict.

**Step 3 — per survivor:** its own Stage-0 pre-registration, `K_intrinsic` enumerated honestly
(**the only remaining brake on selection inflation** under ADR 2026-08-04), cost-law at $0.91/side,
then the Gen-2 stages.

**Step 4 — deployment is a separate operator GO** and inherits the standing c1 interlock: `dry_run`
stays `true`, and `dry_run=false` may not be set while **M1 is not `RESOLVED`**.

---

## §10 — Audit hooks (runnable)

```bash
# The live target geometry this brief is pinned to (expect 3.0 / 6.0 / 5 / 0.91):
python -c "import sys;sys.path.insert(0,'.');from core import firm_rules as F;r=F.FIRM_RULES['Tradeify_Select_100K'];print(r['max_dd_pct'],r['profit_target_pct'],r['inactivity_max_idle_days'],r['cost_per_side_usd'])"

# The 0.40R inversion threshold that T1 and FM-4 rest on:
grep -n "0.40R" lab/analysis/c1/eval_inverse_requirements_2026-08-03/RESULTS.md

# The Req-1a clause that kills most fast candidates (expect the behavioral-stories sentence):
grep -n "stops get hunted" docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md

# Clause K must read K_intrinsic only (ADR 2026-08-04), and k_banked must NOT be summed:
grep -n "K_eff = K_intrinsic" docs/methodology/strategy_harvest.md
grep -n "k_lo, k_hi = lo" lab/research_utils/axis_screen.py

# No manifest opened and no K bound by THIS brief (expect 0):
ls discovery_manifests/ | grep -icE "mnqbase"

# The §1.1 divergence, both halves. Clause 1 is Striker-scoped (matches the operator);
# clause 3 is the one that conflicts. If the ADR is amended, update §1.1 rather than deleting it.
# (An earlier draft grepped "EVALUATION INCLUDED" -- that phrase is in the COMMIT MESSAGE, not the
#  ADR body, so the hook returned 0. Trap M-AHF: hooks must match the stored form.)
grep -n "for the locked Striker book" docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md
grep -n "no further work is authorized" docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md
```

---

## Amendment log (append-only)

- **2026-08-04 — SCOPED.** Intake filter only; no candidate admitted, no manifest, no K, $0.
  Authored at operator direction, on the operator's clarification that the **Select 100K evaluation
  remains live** (§1.1 records the divergence from the ratified ADR text rather than absorbing it).
  §1.2's S7 relief and §2's firm-pinned spec both follow from that clarification and would need
  re-reading if it is later reversed.
- **2026-08-04 — Step 1 RUN → `RESOLVED`; L1 does NOT fire.** Independent-event ceiling 145–1,172/day
  against a target of 3 (1,672 scored sessions). §4's pre-registered expectation — *"L1 firing is the
  single most likely outcome"* — was **wrong, and was corrected in the Step-1 pre-registration before
  the measurement ran** (`1eeb35c`). Bottleneck relocated from opportunity to **selection**.
  [`RESULTS`](../../../lab/analysis/c1/mnq_event_ceiling_2026-08-04/RESULTS.md)
- **2026-08-04 — Step 2 RUN → `FALSIFIED` (intake dry, L2). THIS BRIEF IS CLOSED; disposition STOP.**
  Three candidates survived P1/P3/P4/P5/P6; all three failed Req 1a **and** Req 1b — i.e. they died at
  **P2**, which §2.3 had pre-registered as the likely killer. Fifth consecutive zero-seed sourcing pass.
  Two defects in this brief's own spec are recorded in the closure §5 and were deliberately **not** used
  to move the verdict: **T2 is not venue-mandated** (no tier in `firm_rules.py` encodes an eval time
  limit, so "3–8 trades/day" is a speed preference inherited from the shape spec's 3–12-day framing),
  and **P1–P6 contain no frequency limb**, so Step 2 could not screen on T2 at all. Per Trap #12 the
  frozen text above is unedited; a successor must resolve both before re-deriving T2.
  [`closure`](../closures/MNQBASE-1-closure-intake-dry.md)
