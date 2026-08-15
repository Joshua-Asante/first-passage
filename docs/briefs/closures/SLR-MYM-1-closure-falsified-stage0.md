# SLR-MYM-1 — CLOSURE: `FALSIFIED (as scoped)` at Stage 0

**Verdict:** **`FALSIFIED (as scoped)`** — closed at Stage 0 on **two independent gates**, before any
data purchase, any pre-registration, or any K spend.
**Closed:** 2026-07-29 (operator: *"close SLR-MYM and write the closure record"*)
**Opened:** 2026-07-28
**Brief:** [`docs/briefs/rnd-pipeline/SLR-MYM-1-liquidity-sweep-reclaim-scoping.md`](../rnd-pipeline/SLR-MYM-1-liquidity-sweep-reclaim-scoping.md)
**Mechanism class:** `ict-liquidity` (existing vocabulary; **no new class minted** — a `NEW` entry must
land in the same commit as a pre-registration, and none was ever authored)
**Cost:** **$0.00 spent · 0 K consumed · 0 rows pulled · 0 live-constant changes.**
**Recommendation artifact:** none (correct per the sentinel convention — no `recommendation.md` for a
non-PROMOTE verdict).

---

## §1 — What was proposed

A long-only liquidity-**sweep-and-reclaim** entry in the first 30 minutes of the MYM regular session,
gated by the ICT cascade's RESOLVED weekly structure vote (`vStruct` = close vs EMA(20)) plus a
parameter-free daily analog, stop below the sweep extreme, fixed **+1.5R** target, flat by 13:00 ET —
proposed as a **third leg on the existing Tradeify Select 100K eval**, alongside the incumbent
Striker DJ30→MYM and Striker NAS100→MNQ legs.

---

## §2 — Gates fired, against their pre-registered thresholds

| Gate | Pre-registered trigger | Measured / determined | Fired |
|---|---|---|---|
| **0-A admissibility** | Cannot name a constraint-based WHO for Path 1a **and** will not fund a Path-1b evidence pass | Two constraint framings drafted to ADR 2026-07-26 §2-A's specificity standard; **both fail the delete-test and the flip-test** | **YES** |
| **0-B raised bar** | Operator rules the domain bar binding (route 1 rejected) | Route 1 **clears** — the bar's scope is broader than its evidence | **NO** |
| **0-C day set (S5 + S3)** | No day set satisfies S5 **and** S3 **and** projects IS N ≥ 120 | Best compliant set (Mon+Wed+Thu) = **81 IS entries** vs a **120** floor, on a deliberately *generous* proxy | **YES** |
| 0-D §7.1 screen | Any of S1–S6 fails | S5 fails as first drafted; **S3 is the binding limb** and is structural | subsumed by 0-C |
| 0-E K disclosure | `S-MYM-ORC-02` K=2 ruled bankable ⇒ floor 1.06 > Cap | not reached | — |
| 1 – 4 | census / IS run / confirm / survivor scoring | **never reached** | — |

**Two independent kills.** Either alone closes the campaign. Neither required a data purchase.

---

## §3 — What §4 predicted vs what happened

**H-SLR-MYM-1 predicted** that if Stage-0 cleared and the census projected IS N ≥ 120, the frozen
expression would clear cost-law, the MYM DSR floor (0.85 at `K_eff=2`), Clause-N power, the
both-halves regime gate, and composed bust ≤3.0%.

**The hypothesis was never reached.** It is falsified at its own antecedent — Stage-0 did not clear —
so **nothing is learned about the mechanism's edge.** That distinction is load-bearing for §6.

Two sub-predictions the brief made about *itself* were both wrong, in opposite directions:

1. **The brief predicted power would be the binding risk.** Wrong — the mechanism fires at **17.96%
   of sessions** full-panel (**16.63%** IS, 143 entries across all five weekdays). On an unconstrained
   panel it clears the floor comfortably. **The brief's self-identified long pole was refuted.**
2. **The brief predicted the venue screen was satisfied.** Wrong — it had never actually *scored*
   S1–S6, and the design failed **S5** on the same ground the ratified spec fails its own negative
   control (ORB-MNQ: "trades daily, so requires Tuesday — 0 cap available Tue"). A second constraint,
   **S3**, was not identified until adversarial review.

---

## §4 — The two findings worth keeping

### F1 — Order-symbol occupancy (S3): a same-account second leg on an occupied instrument is structurally impossible

Both the incumbent Striker DJ30→MYM leg and SLR-MYM resolve to the **same order symbol `MYM1!`**, and
the venue holds **one net position per symbol per account**. On the days the incumbent leg can fire —
**Tuesday and Friday** — a second MYM strategy cannot hold an independent position **regardless of how
much contract cap is allocated to it.**

This is a *position-netting* fact, not a sizing fact, and it is what defeats the cap-reallocation
rider: donating cap from the Striker legs cannot manufacture a second independent position. It closes
Friday (which free cap alone would have left open at 11 micros) on top of Tuesday (cap 0).

**Generalizes beyond this candidate:** any future same-account leg must either take an **unoccupied
symbol**, or accept **calendar-disjointness from the incumbent on that symbol** — which is precisely
what collapses the available session count. The third-leg spec's Slot-1/Slot-2 framing is about *cap*;
this adds an orthogonal and stricter *symbol* constraint the spec does not currently state.

### F2 — A mechanism story can name a real, measured effect and still fail admission

The operator's ruling — that this is "more sophisticated than 'stops get hunted'" — was **correct on
its own terms**, and the stronger of the two framings (overnight Globex inventory rebalancing at the
RTH open) names an effect **this repo has measured**: H-OD-1 confirmed dealer overnight inventory-risk
premium on ES at **+1.444 bp** against the published +1.5 bp, t≈5.0, 9/9 IS years positive.

It still fails ADR 2026-07-26 §2-A, because §2-A does not test sophistication — it tests whether the
constraint **selects the trade**. Two cheap discriminators settle it:

- **DELETE test** — remove the constraint paragraph entirely. Does any trading rule change? **No.**
- **FLIP test** — assert the constraint runs the other way (overnight desks were net *short*, so the
  class must **buy** at 09:30). Does the trade change? **No** — the rule still only buys reclaims.

The constraint supplies *volatility*; the OHLCV pattern supplies direction, level choice, gate, stop
and target. Dressing the pattern's direction-selection in the constraint's vocabulary is §5 laundering.

The forced-liquidation framing fails for a cleaner and more reusable reason: **every mechanical rule in
that population is account-equity-triggered.** It governs *whether* a position closes, never *where*.
All the price content still comes from traders *choosing* to place stops at prior-session extremes,
which is the preference §2-A excludes.

---

## §5 — Lesson candidates

| # | Lesson | Anchor |
|---|---|---|
| **L1** | **Design the cheap proxy to be *generous*, so a failure is conclusive.** Phase 0.5 counted a sweep at *any* hour where the rule requires 09:30–10:00, making every count an **upper bound**. A day set failing at the upper bound cannot pass on real data — so a $0 15-minute proxy conclusively killed a campaign whose confirmation would have needed a paid 1-minute pull. A *tight* proxy would have been inconclusive and the pull would have been spent. | 2026-07-29; killed at **$0** what the pipeline would otherwise price at a databento 1m pull + Phases 2–4 |
| **L2** | **Symbol occupancy is a distinct constraint from contract cap, and it is stricter.** Cap is divisible; a net position is not. Any same-account multi-strategy proposal must check symbol occupancy *before* cap arithmetic — the cap table can look permissive on a day the symbol is already taken. | 2026-07-29; F1. Would have saved the entire §2.5 day-set analysis, which was run on cap grounds alone and reached the wrong day set |
| **L3** | **"Sophisticated" is not the admission test — "does the constraint select the trade" is.** The delete-test and flip-test are two-minute, reusable discriminators that catch constraint-laundering regardless of how well-evidenced the underlying effect is. | 2026-07-29; F2. Note the operator's ruling was *substantively right* and the claim still failed — the gap between "real effect" and "admissible warrant" is the thing these tests measure |
| **L4** | Reinforces [`lesson_borrowed_numbers_need_connecting_arithmetic`] — the same session produced a second transcription-boundary error (Tradeify's 40-micro tier belonging to two other table rows). Errors cluster at the boundary where a number is copied out of its source table. | 2026-07-29; [`2026-07-24-tradeify-rulepin-verification.md`](../../notes/2026-07-24-tradeify-rulepin-verification.md) |
| **L5** | **Two sessions verified the same three Tradeify pins independently, the same day, and agreed on all three.** Corroboration is real and welcome — but the duplicated effort is not. `origin/main` had already landed the verification (PR #545) and the four-step ladder implementation (PR #546) while this branch was working. Reinforces [`feedback_check_origin_main_before_multistep_build`]: fetch and read `origin/main` **before** starting a multi-step build, not at PR time. | 2026-07-29; this branch's rule-pin note was written, then deleted as a duplicate at merge |

**The resource actually preserved.** Closing at Stage 0 leaves **MYM's family K bank at 1** (floor
**0.85**, headroom 0.15 under the Cap 1.0). Had this run to a pre-registration, `K_intrinsic=1` would
have taken the bank to 2 ⇒ floor **0.98** — the same "at the cap, one seed only" position MNQ now
occupies. **MYM's runway is the widest remaining on any venue-live index micro, and it is unspent.**
That, not the dollar figure, is the material saving.

---

## §6 — Which nulls remain alive (do NOT over-read this closure)

> ⚠ **READER INTERCEPT — 2026-08-04. One bullet below is superseded; the rest stand.** This
> section is a *nulls-alive ledger* and is read as current state, so the correction is placed
> here rather than only at the foot of the file. **Bullet 2's "ground 1 stands independently"
> is REFUTED** — 0/247 is no longer an instrument-general entry-mechanism finding. See
> [§9 Addendum](#9--addendum-2026-08-04--ground-1-refuted-appended-post-closure) below. The
> body text of §6 is left byte-intact as the frozen record of what was believed on 2026-07-29.
>
> ⚠ **Extended 2026-08-06 (claim-alignment M38):** F1's *rule* remains conditional on its own
> face ("on an **occupied** instrument"; "calendar-disjointness from **the incumbent** on that
> symbol") — L2 (check symbol occupancy before cap arithmetic) is durable. **Only the factual
> premise is dead** — *"On the days the incumbent leg can fire — **Tuesday and Friday**"* —
> because no incumbent is deployed post-de-scope (symbols retained-not-released pending F2).
> §8's "c1 book — two legs, 69/11, disarmed" row is a **no-change attestation** about what this
> closure did and is **not** corrected here.
>
> ⚠ **Operator flag:** the S7 screen that killed ORB-MNQ's cadence role descends from F1 —
> **do not silently reopen ORB**; its payability target is independently FALSIFIED (2026-08-03).

**The mechanism was never tested.** No edge estimate exists, in either direction. Specifically:

- **NOT established:** that sweep-and-reclaim has no edge on MYM, on index futures, or anywhere.
- **NOT established:** that the ICT cascade's 1M execution layer is dead. It remains
  `INSUFFICIENT-N` on ground 2 (the TV data wall, now removable) — while **ground 1 stands
  independently**: 0/247 limit fills, an entry-mechanism finding logged at HIGH confidence and
  characterized as instrument-general.
- **NOT established:** anything about `vStruct`'s per-entry transfer. PREREG-W fixes **leg (a) only**;
  leg (b) was never opened.
- **Route 1 of the domain raised bar was ruled CLEAR** (§2 gate 0-B) and that ruling **survives** this
  closure — a future mean-reversion-class candidate does not re-inherit that objection.

**Re-proposal bar.** A successor needs **both**: (i) a Path-1a four-clause claim that passes the
delete- and flip-tests, **or** a funded Path-1b evidence pass (≥3 decades, ≥3 independent cohorts,
≥1 replication ≥10 yr post-discovery, no known sign-reversal — all four); **and** (ii) an
**unoccupied order symbol**, or a session-disjointness argument that survives F1 *and* still reaches
the power floor. Neither a re-tuned day set, a different level menu, nor a wider panel clears (i).

**Not appended to [`docs/rejected_candidates.md`](../../rejected_candidates.md), deliberately.** That
registry records directions *investigated and rejected as portfolio additions*, and its entries carry
evidentiary weight. This candidate produced **no evidence about its own mechanism** — it failed at
admission and venue fit. Recording it there would imply a falsification the run does not support. The
instrument-level record in [`ops/instruments/MYM.md`](../../../ops/instruments/MYM.md) is the correct
granularity, and MYM.md is a mandatory session-start read for any MYM work, so coverage is not lost.

---

## §7 — Audit hooks (runnable)

```bash
# This closure exists and names both fired gates
grep -n "0-A admissibility\|0-C day set" docs/briefs/closures/SLR-MYM-1-closure-falsified-stage0.md

# The measured census is reproducible (primary checkout only -- vendor data gitignored)
python lab/archive/slr_mym_phase05_2026-07-29/phase05_census.py   # expect 81 for Mon+Wed+Thu

# F1: the incumbent MYM leg's days are what S3 collides with -- cap table unchanged
grep -n "Tuesday is closed" docs/spec/2026-07-27-third-leg-target-spec.md
grep -n "69/11" ops/c1_rail/c1_sizing_host_reference.py

# F2: the §2-A clause this failed against must still read as it does
grep -n "stops get hunted" docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md

# K bank preserved -- MYM must still be 1 (ST-EH-1 executed look only)
python -c "import json,glob;[print(json.load(open(f))['run_id'], json.load(open(f))['status'], json.load(open(f))['K']) for f in glob.glob('discovery_manifests/*.json')]"

# No manifest was ever opened for this campaign (expect no slr/sweep manifest)
ls discovery_manifests/ | grep -i "slr\|sweep" || echo "OK - no manifest, no K consumed"

# Ledger cell landed
grep -n "sweep-reclaim\|SLR-MYM" ops/instruments/MYM.md
```

---

## §8 — Disposition summary

| Item | State |
|---|---|
| Campaign | **CLOSED — `FALSIFIED (as scoped)` at Stage 0** |
| Spend | $0.00 |
| K consumed | 0 — **MYM family bank stays 1, floor 0.85** |
| Manifest | never opened |
| Pre-registration | never authored |
| Live constants (`firm_rules.py`, rail, Pine, allocations, `dd_protection`) | **untouched** |
| c1 book | unchanged — two legs, 69/11, disarmed |
| Third-leg spec §6.1 verdict | **does not fire** — no candidate reached a composed re-MC |
| Domain raised-bar route-1 ruling | **CLEAR**, and survives this closure |

---

## §9 — Addendum 2026-08-04 — ground 1 REFUTED (appended post-closure)

**Appended, not rewritten.** The closure verdict, its two Stage-0 gates, the §8 disposition, the
$0.00/0-K accounting, and the MYM family bank (still **1**, floor 0.85) are all **unchanged** —
nothing in this addendum reopens `SLR-MYM-1` or alters what it consumed. Only one factual claim
inside the §6 nulls-alive ledger is superseded.

**What §6 bullet 2 said (2026-07-29):** the ICT cascade's 1M execution layer *"remains
`INSUFFICIENT-N` on ground 2 (the TV data wall, now removable) — while **ground 1 stands
independently**: 0/247 limit fills, an entry-mechanism finding logged at HIGH confidence and
characterized as instrument-general."*

**What is now measured:** ground 1's instrument-general basis is **false**. `Q-ICT-MNQ-1` Parts B
and C measured the same frozen `limit-on-return / mid / retraceK=6` mechanism on native databento
1-minute data:

| Measurement | Result |
|---|---|
| MNQ displacement FVGs retracing to mid within `retraceK=6` | **59.06%** (n=128,089); **58–60% in every year 2019–2026**, incl. the 2020 crash and 2022 bear |
| ES, full era | **59.88%** (n=124,748); per-year 58.8–61.6% |
| Rate required to produce 0-of-247 at the 5% level | **≤ 1.2%** |
| Raid-conditioned subpopulation (the "post-sweep FVGs continue" out) | **59.01%** — indistinguishable from unconditioned |
| Armed 8 bars late (the "fast retrace, late order" out) | **55.91%** — the arm-delay curve is nearly flat; mid-touches recur |
| ES in the **exact** 2026-06-24→26 US500 window (the "that regime" out) | **62.33%** (n=223, order-matched to the 247 arms) |

Every measured cell sits at **45× or more** the rate the 0/247 fact requires, on two instruments,
across eight years each, including the specific calendar window in question.

**Consequence for this closure's ledger, stated precisely:**

- **Ground 1 no longer stands independently.** 0/247 is localized **platform-side by elimination** —
  the deployed (now lost) `ict_1m_execution_DRAFT.pine`, TV's strategy-tester fill handling, or the
  retired Pepperstone US500 CFD feed. These are not further separable and the residual is recorded
  as such, never as "bug X."
- **The 0/247 *observation* is untouched.** 247 orders were armed and 0 filled on US500. What is
  refuted is the *price-law explanation* and the *instrument-general characterization*, not the count.
- **Ground 2 is unchanged** — the TV 1m history cap is real, and remains removable at $0.00 via databento.
- **SLR-MYM-1's own §2.1 reasoning is strengthened, not weakened.** It argued its bar-close reclaim
  with a market order at next open *structurally avoided* the resting-limit mechanism that returned
  0/247, and explicitly flagged that as *"a reason to expect fills, not evidence of an edge."* That
  caution was right and still binds; the ground-1 refutation simply removes an objection that was
  never load-bearing for this campaign's own verdict.
- **§6 bullets 1, 3, and 4 are unaffected** — in particular bullet 3 (`vStruct` leg (b) never
  opened) is **re-confirmed**: the leg-(b) gate-transfer probe (`TEST_PLAN.md:179`) needs per-entry
  records under a bias-gate on/off split, and its `netBias` formula survives only in the lost
  `.pine`, so it is permanently `BLOCKED`, not merely un-run.

**Sources:** [`RESULTS_1H_1M.md`](../../../lab/analysis/_inbox/ict_mnq_2026-08/RESULTS_1H_1M.md) §2 ·
[`RESULTS_1M_DIAG.md`](../../../lab/analysis/_inbox/ict_mnq_2026-08/RESULTS_1M_DIAG.md) ·
[`ops/instruments/MNQ.md`](../../../ops/instruments/MNQ.md) W3 ·
companion corrections in [`MECHANISMS.md`](../../../ops/instruments/MECHANISMS.md) `ict-liquidity`
and [`SPX500.md`](../../../ops/instruments/SPX500.md) **F9**.

**Not changed by this addendum:** no `core/`, lock, allocation, `dd_protection`, Pine, rail,
`LEG_MAP`, K-ledger, or manifest change. MYM family bank stays **1**; MNQ stays **2**.
