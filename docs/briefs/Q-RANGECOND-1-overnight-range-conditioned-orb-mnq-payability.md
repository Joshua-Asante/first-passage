# Q-RANGECOND-1 — Does the presence-verified overnight-range conditioner change ORB-MNQ-1's realized payoff shape enough to matter for Tradeify payability?

**Status:** `CLOSED — RESOLVED` 2026-08-30 (with a disclosed panel-vintage caveat — see §11; operator ruled Route ① satisfied same day, "I rule Route ① satisfied, proceed with Phase 1," then Phase 1-3 executed and cleared all four pre-registered limbs)
**Authored:** 2026-08-30
**Closed:** 2026-08-30
**Authors:** Claude Code (D-S-A gate + Rule-0 reads; adversarially reviewed pre-commit — a 5-lens workflow found and this draft corrects: a load-bearing raised-bar citation error, 8 self-violations of the brief's own "never call it certified" rule, a §6/pre-reg §C gate-table gap, a missed same-mechanism prior finding on NAS100, an uncited exploratory p_upper=0.785 signal, a regime-concept conflation, and a power-estimate error — see corrections marked inline); operator-directed continuation of the closed Q-RANGEXFER-1 thread ("Continue with solution shaped hypothesis you suggested, authored as a fresh Q")
**Parent question:** N/A — forks off the closed `Q-RANGEXFER-1` thread's own presence-verified finding, but is scored as an independent construct-level question, not a sub-question of it
**Sub-questions opened:** none yet
**Loop:** Inquire-phase Pre-Q — gates whether the presence-verified overnight-range conditioner is worth a full Tradeify re-MC on `ORB-MNQ-1`, or whether the parked pursuit stands unchanged
**Artifact path:** `docs/briefs/Q-RANGECOND-1-overnight-range-conditioned-orb-mnq-payability.md`

---

## Pre-Q gate (D-S-A, data domain — `inqhiori` §3)

```
D: Deleted every OTHER candidate conditioning variable this brief could have tested (gap
   magnitude, the day-history predictor, volume regime) — test: only H-RANGEXFER-1's own
   MNQ-parent presence-verified statistic (overnight-range, min-stratified over day-history,
   L1-L3 PASS) is in scope. Testing multiple conditioners and reporting the one that looks
   best would be exactly the P&L-mining class F2 GUARD already bars on this instrument, one
   layer up (mining over CONDITIONERS instead of over ORB's own filter slices).
D: Deleted the idea of retuning ORB-MNQ-1's own frozen entry/exit parameters in response to
   this test's outcome — test: parameters are LOCKED per the strategy-lifecycle axis
   (docs/methodology/strategy_lifecycle.md); only an EXTERNAL day-selection gate is in scope,
   analogous to how dd_protection's DD_SCALE or the lifecycle authorization multiplier sit
   orthogonal to locked parameters, never inside them.
S: Reduced the question to the single lowest-dimension test that could tell us anything: split
   ORB-MNQ-1's own already-computed trade log by whether the day would have cleared
   H-RANGEXFER-1's own already-presence-verified predictor, and compare win rate / mean win on each
   side against the Tradeify payoff-shape floor (WR>=55-60%, large mean win) already measured
   for this exact venue. Anything more elaborate (a full re-MC, a Pine wire-up) is premature
   before this cheap split says whether there is anything to elaborate.
A: The trade log this Q needs is producible at $0 by reusing `orb_lib.orb_backtest` verbatim
   (the same arbiter ORB-MNQ-1's own G8 admission and R3 payability runs already used) against
   the same hash-verified `MNQ_M15.csv` this worktree already has, and the conditioner is
   reused verbatim from Q-RANGEXFER-1's own already-reviewed `data_lib.py` /
   `candidate2_overnight_rth_transfer.py` functions — no new backtest engine, no new
   conditioner definition, only a join on `trading_day`.
```

---

## §0 — Rule 0 reads (production-source verification)

- `docs/briefs/closures/Q-RANGEXFER-1-closure-ambiguous-design.md` — anchor `e7a7bcb` (verified
  `git log -1`, 2026-08-30). H-RANGEXFER-1 (MNQ parent, overnight-range) closed
  `AMBIGUOUS-DESIGN`: presence limbs L1-L3 PASS (adversarially verified, `TRUSTWORTHY_AS_IS`),
  L4 by-year floor AMBIGUOUS, mechanism-attribution (L5) design-blocked by a measured 26%
  Type-I inflation on the one design that looked viable. **This brief inherits the
  presence-verified predictive claim only, never the mechanism-attribution claim** — §5 below
  makes this an explicit forbidden move.
- `docs/briefs/pre-registration/Q-RANGEXFER-1-verdict-preregistration.md` §A/§H — anchor
  `e7a7bcb`. Frozen conditioner definition: `bias_overnight_d = 1{ON_range_d >= P80(ON_range_{d-60..d-1})}`,
  `WINDOW=60, Q_BIAS=0.80`, strictly-prior trailing window. This is the EXACT predictor reused
  below, unmodified.
- `lab/analysis/_inbox/rangexfer_presence_battery_2026-08-30/presence_l1_l3_results.json` —
  anchor `e7a7bcb`. H-RANGEXFER-1's own presence figures: n_scored=1487, L2 CI on the
  min-stratified lift `[+0.300, +0.473]`, both chronological halves positive. The
  presence-verified floor this brief's own conditioner reuse rests on.
- `lab/analysis/orb/orb_mnq_2026-07/ADMISSION.md` — anchor `fc95425` (verified `git log -1`,
  2026-08-30). ORB-MNQ-1 lifecycle `CANDIDATE @ 1.00×` (2026-07-16 G8 intake): cost-law PASS
  5.31×/8.10×, DSR full 0.9754, annSR +0.890, placebo p=0.0040, temporal 2021+ PASS, realized
  N_eff 1.99→2.95. **Standing caveat 1 corrected on adversarial review**: `ADMISSION.md`'s own
  text reads "post-2020/**trend**-regime" (not bare "regime-conditional"), and `RESULTS_stage8.md`
  makes the trend/chop framing explicit and load-bearing ("dead in 2020... the whole pre-2021
  period... trend-loving, chop-fragile... weak in the chop (2020)"). This is a DIFFERENT regime
  axis than the overnight-range-magnitude conditioner tested below — trend-vs-chop is a
  multi-year macro regime; the conditioner is a trailing-60-day P80 flag that fires on ~20% of
  days in every era BY CONSTRUCTION, including inside 2019-2020, and cannot by itself distinguish
  which macro-year a day falls in. These two regime concepts are not shown to be the same thing
  and could plausibly compound rather than one fixing the other — 2020 (the COVID crash) is a
  concrete case in this repo's own record where realized range was extreme AND the strategy was
  in its own "chop" era, the opposite pairing this brief's mechanism story would want. This
  brief does NOT claim the conditioner addresses ORB-MNQ-1's own trend/chop caveat — that claim is
  withdrawn; the two are tested as independent, potentially-compounding axes, not as one
  explaining the other.
- `docs/pursuits/b3-orb-mnq-payability-line.md` — anchor `08b0336` (verified `git log -1`,
  2026-08-26). ORB-MNQ-1 is `PARKED`, expiry **2026-11-08**, re-entry clause: "new payability /
  cost-geometry evidence at an admissible venue." Standalone: busts the 3.0% trailing DD ceiling
  at every tested contract size, at ALL FOUR `AUTOMATION_FRIENDLY_PROP_FIRMS` — two differently-
  scoped measurements, neither clearing: Bulenox/BluSky/MFFU R3 FAIL 2026-08-24 (k∈{1,2,3}, bust
  62-82% vs the 3% ceiling) and Tradeify's own solo re-measurement in the 2026-08-26 combined-book
  addendum (k∈{1..8}, T2 originally FIRED 2026-08-03). The only surviving overlay evidence (a 0.18-0.40
  contract sliver inside a combined book with Aegis-6J1) **reversed at its own §10**: both
  regime halves now fail under full-compounded corrections. **Standalone ORB-MNQ-1 has no
  currently-surviving Tradeify-clearing configuration at any tested size.**
- `ops/instruments/MNQ.md` F2 GUARD + N1 row — anchor `e7a7bcb`. F2 GUARD bars the ORB
  filter-slice class discovered by looking at which days ORB-MNQ-1's OWN P&L "looks better"
  (Friday/Monday/OR-hi/same_bar) from ever appearing outside the DEAD list. **The conditioner
  tested here is not in that class** — it was derived on an entirely separate data object
  (the daily overnight-range/RTH-range series across every trading day, independent of whether
  ORB-MNQ-1 traded or won that day) via a months-long, adversarially-reviewed, pre-registered
  investigation that never once touched ORB-MNQ-1's own trade log. §5 states this distinction
  explicitly and names the residual risk it does NOT fully retire.
- **⚠ Raised-bar status: BINDING, mechanically confirmed, and NOT resolved by this brief —
  Phase 1 is gated on an operator ruling, not merely "the next step."** Corrected during
  adversarial review; an earlier draft of this bullet cited `docs/rejected_candidates.md`'s
  MSL-S2B entry ("Candidate A ... clears MR-at-level *filter* only") as establishing a blanket
  filter-role exemption. On direct re-read, that closure's own basis states **"Composite
  clearance forbidden"** — Candidate A needed its own Route ① argument even for its filter-only
  role. That citation supports the opposite of what it was used for and is withdrawn. Two
  actually-governing texts, neither cited in the withdrawn draft:
  - [`docs/adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md`](../adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md)
    — anchor `027a729` (verified `git log -1`, 2026-08-30; this ADR, not MSL-S2B, is what actually governs
    within-instrument temporal-selectivity constructs on this raised bar). §2-A reads the bar's
    "instrument-selection" lever as CROSS-instrument only, leaving within-instrument temporal
    selectivity — "which moment of a session to take," which a day-level skip/keep gate plainly
    is — outside the mapped set and Route ① generally OPEN to it, but §2-B calls this exact
    construct class "the single highest-risk laundering shape in this estate" and opens it only
    under three conditions: (1) the selection criterion is causally named a priori, frozen before
    G0, never read off a scored list; (2) every axis charges `K_intrinsic`; (3) nothing downstream
    is weakened. §2-D additionally wires a mechanical gate:
    `python scripts/instrument_profiles.py cell <SYM> <mechanism-id>`, which "exits nonzero when a
    prior binds," with "every `BINDING BAR` line answered in the brief's own §0 by naming the
    route that clears it" as a precondition for any G0 freeze.
  - **Mechanical consult, run this session:** `python scripts/instrument_profiles.py cell MNQ
    overnight-range-transmission` → `BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21`,
    exit 1. The bar genuinely binds on this mechanism id. Condition (1) above is independently
    satisfiable on the facts already in this brief's own §0 (the conditioner was frozen 2026-08-18
    for an unrelated cross-instrument screening class, well before this pairing existed —
    verified, not asserted); condition (2) is declared at §8 (`K_intrinsic=1`); condition (3) is
    the substance of §5's own forbidden-move list.
  - **But `Q-RANGEXFER-1`'s own closure §3 — cited elsewhere in this very §0 — states, in its
    "What this closure does NOT license" section: "No entry, sizing, or timing construct on any
    surviving conditioner. All four `AMBIGUOUS-DESIGN` hypotheses stay conditioner-role research,
    not tradeable findings."** A day-selection gate on `ORB-MNQ-1`'s entries is, in plain
    language, a timing construct built on this exact surviving conditioner. This is a direct
    textual conflict between two governing documents — one of them authored the same day, in this
    same session, by the same author now proposing to read past it. This brief did not resolve
    that conflict by argument; the argument above (the 2026-08-10 ADR's own conditions plausibly
    being satisfied) was offered as a candidate Route ① case, not a self-certified clearance,
    pending an explicit operator ruling.
  - **⚖ RULED, 2026-08-30:** "I rule Route ① satisfied, proceed with Phase 1." Route ① is open on
    this brief's own facts (conditioner frozen 2026-08-18, well before this pairing existed;
    `K_intrinsic=1` declared at §8; §5's forbidden moves keep nothing downstream weakened),
    reconciled with `Q-RANGEXFER-1` §3 by operator ruling rather than by this brief's own
    self-certification. Phase 1 is GO'd. This does not retroactively license a future construct
    on this conditioner without its own ruling — the ruling is scoped to this brief's own
    day-selection-gate construct on `ORB-MNQ-1`, not a general reading that all conditioner-based
    timing constructs on the `Q-RANGEXFER-1` family are now open.
- `core/firm_rules.py` — anchor `5829e5e` (verified `git log -1`, 2026-08-24). Tradeify
  `cost_per_side_usd: 0.91` (line 350, index micros MNQ/MYM/MES), matching the `rt_pt=1.41`
  round-trip basis cited throughout `MNQ.md`.
- `~/.claude/projects/.../memory/project_tradeify_consistency_payoff_shape_constraint_2026_08_22.md`
  (Claude-project memory, dated 2026-08-22, scope-corrected 2026-08-24 — assistive-only per this
  repo's own MEMORY.md convention, cited here as a routing pointer, not as a repo-authoritative
  source; the authoritative figure lives at `lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md`
  §7, cross-checked at Phase 0 of §7 below before this brief's own gate criteria are finalized
  against it). Measured floor: the **$3,000 trailing rope** binds, not the 40% consistency rule;
  no cell at `win_rate <= 50%` is FEASIBLE at any shape/cadence/risk level; the floor sits at
  55-70% depending on payoff shape; **mean win size**, not skew, is the second axis that matters.
- `docs/methodology/strategy_lifecycle.md` — anchor `edd68e6` (verified `git log -1`, 2026-08-23)
  · `docs/adr/2026-07-10-strategies-never-locked-lifecycle-governance.md` — anchor `572781c`
  (verified `git log -1`, 2026-08-23; a different commit than the methodology doc — the two were
  not touched in the same commit, cited separately here rather than under one shared anchor).
  Confirms the parameter axis (SL/TP/ATR/entry rule) is immutable and the authorization axis is
  separately revocable — the conditioner tested here operates entirely on the
  authorization/filter axis, never touching ORB-MNQ-1's own locked parameters.
- Sub-rule 8 paste-search (executed 2026-08-30, this session): `python scripts/check_advisor_dedup.py
  --keywords "range conditioned breakout ORB entry Tradeify payoff"` — no prior-art hit on this
  exact construct (a range/volatility-regime filter applied to ORB-MNQ-1's own signal); nearest
  neighbors are `MNQBASE-1` (Tradeify-shaped base-construct harvest, closed dry, unrelated
  construct family) and the instrument ledgers themselves (expected, both instruments are
  directly named). `grep -ni "orb.mnq\|range.condition" lab/CATALOG.md docs/briefs/INDEX.md` —
  no hit on a prior range-conditioned-ORB campaign against `ORB-MNQ-1` specifically — the exact
  construct pairing is genuinely novel. **The underlying mechanism CLAIM is not novel and was
  missed by this search**, corrected on adversarial review — see §2's NAS100 disclosure below;
  the original dedup search (lab/CATALOG.md, docs/briefs/INDEX.md) never reached
  `ops/instruments/NAS100.md`, a different instrument's own ledger, which is why this specific
  prior test didn't surface.
- **Amendment-first (sub-rule 10):** no existing owner artifact holds this exact question. The
  parked pursuit (`b3-orb-mnq-payability-line.md`) owns ORB-MNQ-1's own standing PARK status and
  is amended (an Addendum, not a rewrite) once this brief reaches a verdict — see §9. The closed
  `Q-RANGEXFER-1` owns the conditioner's own certification status and is not reopened or amended
  by this brief; it is cited, not touched.

---

## §1 — Context & motivation

`STATE.md`'s own operator queue item `#1` ("Acceptable strategy on the ruled host") has stood as
the estate's top priority since 2026-08-23. `ORB-MNQ-1` is the only lifecycle-admitted candidate
on MNQ with a real, cost-law-passing, DSR-passing edge (`ADMISSION.md` §0) — its standing blocker
is specifically Tradeify payability, not edge existence: it busts the $3,000 trailing rope at
every tested contract size, at all four `AUTOMATION_FRIENDLY_PROP_FIRMS`, standalone (§0 above).
This is a payoff-SHAPE problem (per the Tradeify memory), not an edge problem — the exact class
of problem a genuine win-rate/mean-win-improving filter could plausibly fix. `Q-RANGEXFER-1`
closed 2026-08-30 with a presence-verified (adversarially reviewed, `TRUSTWORTHY_AS_IS`) finding
that MNQ's own overnight range predicts elevated same-day RTH-range magnitude. An opening-range
breakout is structurally a bet on RTH range magnitude — bigger range means more room for a
genuine breakout to run; calmer, choppier days are where false breakouts and whipsaws concentrate.
**This mechanism story is plausible but not uniquely predicted**: a wide range can equally come
from a whipsaw-prone, choppy day (which would stop `ORB-MNQ-1` out) as from a clean trend day —
the brief does not have an a priori argument that rules out the opposite direction, and a
directly contrary same-mechanism-claim test already exists in this repo on a sibling instrument
(§2 below). What distinguishes this pairing from a P&L-mined coincidence is provenance, not
mechanism confidence: the conditioner was derived on an entirely separate dataset, never touching
`ORB-MNQ-1`'s own trade log, months before this pairing was proposed. That provenance claim is
what §5's forbidden-move discharge rests on — the mechanism story itself is a reasonable prior
worth testing cheaply, not a settled explanation.

---

## §2 — Prior art / lineage

- [`Q-RANGEXFER-1`](Q-RANGEXFER-1-overnight-range-gap-magnitude-transfer.md) — closed
  `MIXED (AMBIGUOUS-DESIGN` on the MNQ parent)`, owner of the conditioner definition and its own
  presence-verification. Cited, not reopened.
- `ORB-MNQ-1`'s own pipeline: [`ADMISSION.md`](../../lab/analysis/orb/orb_mnq_2026-07/ADMISSION.md)
  (G8 intake) · [`b3-orb-mnq-payability-line.md`](../pursuits/b3-orb-mnq-payability-line.md)
  (PARK, re-entry clause) · [`RESULTS_stage7.md`](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_stage7.md)
  (firm×slip realism) · [`RESULTS_bulenox_blusky_payability.md`](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_bulenox_blusky_payability.md)
  (4-firm FAIL) · [`aegis_orbmnq_combined_book_2026-08-26/RESULTS.md`](../../lab/analysis/c1/aegis_orbmnq_combined_book_2026-08-26/RESULTS.md)
  (combined-overlay evidence, reversed at §10).
- `ops/instruments/MNQ.md` F2 GUARD — governs the class of move this brief must NOT repeat
  (P&L-mined ORB filter slices) and is the reason §5 below draws the distinction explicitly.
- [`docs/adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md`](../adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md)
  — the actually-governing raised-bar text for this construct class (§0's ⚠ bullet); MSL-S2B is
  cited in §0 only as a withdrawn, weaker analogy.
- `docs/briefs/closures/Q-RANGEXFER-1-closure-ambiguous-design.md` §3 — the direct textual
  conflict with this brief's own premise, disclosed (not resolved) in §0's ⚠ bullet.
- `ops/instruments/NAS100.md` N6/N8/N9 + 2026-06-24 "ORB improvement audit" — a distinguished,
  same-mechanism-claim prior finding on a sibling instrument, missed by the original dedup pass
  and added on adversarial review (see below).
- Beyond the above, genuine: no prior Q-brief, ADR, or closure in this repo has tested a
  range/volatility-regime conditioner against `ORB-MNQ-1`'s own trade log specifically. But the
  identical mechanism CLAIM — overnight realized range regime-gating an index-future ORB — was
  already tested once, on the sibling CFD-era NAS100 ORB-30
  (`ops/instruments/NAS100.md`, 2026-06-24 "ORB improvement audit" session entry), as a single
  pre-registered median-split cut (not a separately presence-verified, independently-derived
  predictor joined post-hoc, the construction this brief uses). **It FAILED, in the direction OPPOSITE this
  brief's own §1 mechanism story** — the high-overnight-range half was the WORSE half (meanR
  +0.0666 vs +0.1093 for the low-range complement, label-perm fw-p 0.747) — **and collapsed once
  orthogonalized against the already-falsified `\|gap\|` signal** (indicator-t → −0.56 after
  partialling `\|gap\|` out; corr(overnight-range, `\|gap\|`)=+0.721). Distinguished, not
  dismissed: different instrument (NAS100 CFD vs MNQ native futures), different data feed
  (Pepperstone vs Databento), different construction (direct P&L-conditioning cut vs. this
  brief's own independently-derived-then-joined predictor), and NAS100's own overnight-range
  variable was never adversarially reviewed or presence-verified the way `Q-RANGEXFER-1`'s was.
  It does not refute H-RANGECOND-1. It does mean §1's "mechanism-motivated, not a P&L-mined
  coincidence" framing is stated with more confidence than the record supports — a directly
  contrary same-claim finding already exists in this repo, uncited in the original draft. §1 is
  corrected below to carry this caveat explicitly.

---

## §3 — Question (Q-RANGECOND-1)

**Q-RANGECOND-1:** What is `ORB-MNQ-1`'s own realized win-rate and mean-win shape, split by
whether `Q-RANGEXFER-1`'s own already-presence-verified overnight-range predictor would have
flagged that trading day — and does either side of that split clear Tradeify's measured
payability floor where the unconditioned population does not?

Symptom-shaped (what is true about `ORB-MNQ-1`'s own trades, sliced by an already-existing,
independently-derived variable), not solution-shaped (this brief does not propose building or
wiring anything — a favorable split is evidence for a re-entry decision, not the decision itself).

---

## §4 — Falsifiable hypothesis (H-RANGECOND-1)

**H-RANGECOND-1:** If `ORB-MNQ-1`'s trades on days `bias_overnight_d = 1` (the presence-verified
overnight-range-elevated predictor) show a win rate materially closer to or above the measured
Tradeify payability floor (55-60%, per `shape_feasibility_map_2026-08/RESULTS.md` §7) AND a mean
win materially larger than the unconditioned population's own mean win, with the difference
outside a block-bootstrap CI's noise band, then the conditioner is legitimate new
payability/cost-geometry evidence under the parked pursuit's own re-entry clause and warrants a
full re-MC; otherwise the conditioner does not change `ORB-MNQ-1`'s payoff shape in a way that
matters for Tradeify, and the park stands unchanged with no re-entry evidence added.

**Reject H-RANGECOND-1 if:** the conditioned subset's win rate and mean win are statistically
indistinguishable from the unconditioned population (block-bootstrap CI on the difference
includes 0), OR the conditioned subset shows a WORSE win rate / mean win than unconditioned, OR
the conditioner's own day-elevation flag correlates so weakly with `ORB-MNQ-1`'s own entry-day
population (the two are keyed on the same calendar but not the same triggering event — an ORB
entry requires its own opening-range breakout condition, which may or may not co-occur with an
overnight-range-elevated day) that the split has too few conditioned trades to say anything
(n < 30 on either side, the exact floor `Q-ORBCUSH-1` already used on `ORB-MNQ-1` itself — "primary
classifier structurally unreliable at n < 30 trades in a pre-registered window" — reused verbatim
as the correctly-scoped precedent, not the day-history-persistence per-calendar-year convention,
which is a different statistic for a different purpose).
**Accept H-RANGECOND-1 if:** the conditioned subset clears win rate ≥55% (the measured floor's
own lower bound) AND its mean win exceeds the unconditioned population's own mean win by an
amount the block-bootstrap CI confirms is not attributable to noise (CI on the difference
excludes 0), with n ≥ 30 on the conditioned side.
**Ambiguous-hold if:** the split is directionally favorable (conditioned WR and/or mean win both
higher) but n is too thin to trust (n < 30 conditioned trades) — re-test window tied to more data
becoming available (the panel is already fixed at ~6 years; this would mean waiting for genuinely
new bars, not a re-test date), or a design that pools across a coarser conditioner threshold
(disclosed as a genuinely different look, not a free re-slice of this one).

---

## §5 — Forbidden moves

- **Retuning `ORB-MNQ-1`'s own frozen entry/exit parameters (or_bars, stop, target, session
  window) in response to this test's outcome.** Ruled out — the parameter axis is locked per
  `strategy_lifecycle.md`; only the external conditioner (a new, separate day-selection gate) is
  in scope. A favorable result licenses proposing a filter LAYER, never a parameter edit.
- **Treating this as the same forbidden class the F2 GUARD bars, without distinguishing it.**
  The F2-barred filters (Friday/Monday/OR-hi/same_bar) were discovered by looking at
  `ORB-MNQ-1`'s OWN P&L history for slices that "look better." This conditioner was derived on an
  entirely separate data object — the daily overnight-range/RTH-range series across every trading
  day — via a months-long, pre-registered, adversarially-reviewed investigation that never once
  consulted `ORB-MNQ-1`'s own trade log. This is the leading-indicator/constraint-selects-the-
  trade distinction, not the P&L-gate-rationalization one. **What this does NOT retire:** the
  DECISION to test THIS SPECIFIC conditioner against `ORB-MNQ-1` was itself motivated by wanting
  a Tradeify-viable candidate to exist — a second-order version of the same risk. The mitigation
  is procedural, not evidentiary: exactly one, already-presence-verified conditioner is tested,
  once, pre-registered before the join runs (§8), with no post-hoc search over conditioners or
  thresholds if this one comes back unfavorable (next forbidden move).
- **Searching over multiple conditioning variables, thresholds, or `or_bars`/session windows
  after seeing this test's result.** Only `H-RANGEXFER-1`'s own frozen, already-presence-verified
  definition (`WINDOW=60, Q_BIAS=0.80`, strictly-prior) is tested. A FALSIFIED verdict here does
  not license trying gap-magnitude, volume-regime, or a different threshold next — any such
  attempt is a fresh Q with its own pre-registration, not a re-slice of this one.
- **Treating a presence-verified conditioner as a certified causal mechanism, or omitting the one
  concrete signal pointing the other way.** `Q-RANGEXFER-1` closed `AMBIGUOUS-DESIGN` on mechanism
  attribution — the incremental predictive relationship is presence-verified (L1-L3, adversarially
  reviewed) but the joint-surrogation null that would certify it as a genuine mechanism (not a
  shared-regime artifact) never certified (measured 26% Type-I inflation, hard-stopped). **Beyond
  that generic uncertified status, one concrete, disclosed, EXPLORATORY-ONLY finding exists and
  points toward the artifact reading specifically**: `joint_surrogation_null_2026-08-30/RESULTS.md`'s
  Round 2 ran the leading (uncertified) ARFIMA-copula design once against the real data and found
  `p_upper=0.785` — the observed stage-1 incremental lift sits comfortably inside (slightly below
  the mean of) that null's own distribution once shared long-memory regime dynamics are modeled,
  i.e. it does not look unusual under a null that already accounts for the shared-regime confound.
  That closure's own text calls this "the single most concrete, actionable number this entire
  two-round exploration produced" and warns the eventual certified verdict "could plausibly land
  FALSIFIED rather than the stage-1-suggested GRADUATE." This brief tests whether the
  presence-level predictive relationship is USEFUL for `ORB-MNQ-1`'s payoff shape, which does not
  require mechanism certification — but any write-up must carry BOTH caveats forward explicitly
  (uncertified status, AND the specific 0.785 lead), never quote the
  conditioner as "certified" or "resolved."
- **Reading an ACCEPT verdict here as re-entry authorization, or as a green light for a full
  re-MC, Pine wiring, or any spend.** This brief gathers evidence toward the parked pursuit's own
  re-entry clause; the re-entry decision itself, and any full re-MC that would follow, are
  separate, operator-gated steps (mirrors `b3-orb-mnq-payability-line.md`'s own language for the
  Aegis-6J1 overlay evidence: "on point for this document's own re-entry clause... but ...
  re-entry / re-scoping this pursuit... is an operator call, not made here").
- **Treating the raised-bar question as self-certified rather than operator-gated.** Resolved —
  see §0's ⚠/⚖ bullet. The mechanical consult confirmed the bar binds; the brief itself declined
  to self-certify past the conflict with `Q-RANGEXFER-1`'s own closure §3, and the operator ruled
  Route ① satisfied 2026-08-30. Recorded here as discharged, not as a still-open forbidden move.
- **Reproducing `ORB-MNQ-1`'s scoring pipeline from memory or by guessing its parameters,
  rather than reading the actual production code.** `orb_lib.py`'s shared `INSTRUMENTS` dict has
  no MNQ entry — `ORB-MNQ-1`'s own run script (`run_orb_mnq_bulenox_blusky.py`) constructs an
  ad-hoc `Instrument` inline (`or_bars=2`, `open_tod=09:30 ET`, `close_tod=15:45 ET`,
  `tick=0.25`, `spread_pt=0.25`) and calls `orb_lib.orb_backtest` verbatim. Phase 1 of §7 reuses
  this exact construction, read fresh from that file, not reconstructed from `ADMISSION.md`'s
  prose summary.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` | Conditioned subset clears WR ≥55% AND mean win exceeds unconditioned by an amount the block-bootstrap CI confirms (excludes 0), n≥30 conditioned trades | `INTEGRATE — file a re-entry addendum on b3-orb-mnq-payability-line.md citing this brief as new payability/cost-geometry evidence per its own re-entry clause; name (not authorize) a full Tradeify re-MC as the natural next step, gated on a separate operator GO + fresh K declaration. No Pine, no rail, no spend from this brief alone.` |
| `FALSIFIED` | Conditioned subset's WR/mean-win indistinguishable from or worse than unconditioned (CI includes 0 or wrong-signed), **OR** the CI on both differences clears (excludes 0, correctly signed) but the conditioned WR still falls below the 55% floor (L4 fails while L2/L3 pass) | `STOP — re-proposal bar: a genuinely different conditioning variable or construct pairing, its own fresh pre-registration — not a retuned threshold or or_bars on this exact test. The park (b3-orb-mnq-payability-line.md) stands unchanged; no addendum filed beyond a disclosure note that this evidence class did not pan out.` |
| `AMBIGUOUS-HOLD` | Directionally favorable split but n < 30 conditioned trades | `ITERATE — return target: this exact panel is fixed at ~6 years (no new bars pending); a coarser conditioner threshold or a longer trailing window would be a genuinely different, freshly pre-registered look, not a free re-slice. Disclose the directional read without treating it as evidence either way.` |

---

## §7 — Execution plan

- **Phase 0 — Rule-0 reads.** Complete (§0 above), with one item explicitly deferred to Phase 1
  rather than rushed at authoring time: a full, unhurried read of
  `lab/analysis/orb/orb_mnq_2026-07/run_orb_mnq_bulenox_blusky.py`'s complete import chain
  (`discovery.prop_survivor_scoring`, `orb_lib.session_panel`/`orb_backtest`) before any new code
  is written, per §5's own forbidden-move on guessing this construct's parameters.
- **Phase 1 — Build the per-day trade log.** Reuse `orb_lib.orb_backtest` verbatim against
  `core/data/bar_data/MNQ_M15.csv` (hash-verified in this worktree against `SHA256SUMS`), with
  the exact `Instrument` construction read fresh from `run_orb_mnq_bulenox_blusky.py::make_inst`
  (`or_bars=2`, `open_tod=09:30 ET`, `close_tod=15:45 ET`). **Sanity-check before trusting
  anything downstream:** the reproduced cost-law ratio and DSR should land close to
  `ADMISSION.md`'s own cited 5.31×/8.10× and 0.9754 — a material mismatch means the
  reproduction is wrong and Phase 2 does not proceed until it's fixed. No cached `_mnq_15m.pkl`
  is present in this worktree (heavy artifact absent); the panel is built fresh from the
  hash-verified CSV via `orb_lib.session_panel`, not read from the primary checkout's own
  gitignored cache (the run script's own `_PRIMARY` fallback path is a different checkout and is
  not used here).
- **Phase 2 — Join against the conditioner.** Reuse `bias_overnight` verbatim from
  `candidate2_overnight_rth_transfer.py` / `candidate24_joint_gate.py` (same `WINDOW=60,
  Q_BIAS=0.80`, strictly-prior), computed on the same `MNQ_M15.csv`. Join on `trading_day`.
- **Phase 3 — Compute conditioned vs unconditioned WR/mean-win.** Block-bootstrap CI (frozen
  scheme, matching the presence-battery's own convention: circular day-block, `block=20,
  draws=4000, seed=42` — reused for consistency, not re-derived) on the WR and mean-win
  differences.
- **Phase 4 — Verdict assertion.** Run §6 against the actual numbers; produce the closure
  artifact per §9.

---

## §8 — Verdict pre-registration (mandatory before Phase 1)

Filed at [`docs/briefs/pre-registration/Q-RANGECOND-1-verdict-preregistration.md`](pre-registration/Q-RANGECOND-1-verdict-preregistration.md),
committed in the same commit as this brief (Phase 1 has not run; no analysis-order violation).

Pre-registration date: 2026-08-30.

---

## §9 — Closure record format

Per `references/closure_record.md` when the §6 gate fires:
- **If RESOLVED:** `docs/briefs/closures/Q-RANGECOND-1-closure-resolved.md` + an Addendum on
  `docs/pursuits/b3-orb-mnq-payability-line.md` citing it (per this Q's own §6 INTEGRATE
  disposition).
- **If FALSIFIED:** `docs/briefs/closures/Q-RANGECOND-1-closure-falsified.md` (no addendum on the
  parked pursuit beyond a one-line disclosure that this evidence class was tested and did not
  pan out).
- **If AMBIGUOUS-HOLD:** `docs/briefs/closures/Q-RANGECOND-1-closure-ambiguous.md`.

**K / spend:** $0 disclosure only — Phase 1-4 reuse already-hash-verified vendor bars and
already-reviewed, frozen conditioner/backtest code; no new pull, no new manifest. `K_intrinsic=1`
(disclosure; Cap not claimed), matching this repo's own convention for a single $0 exploratory
look that does not touch a closed harvest manifest. MNQ family K-bank (currently 22, per
`MNQ.md` row 9) is NOT incremented by this brief — it is not a Notice-phase candidate-screening
manifest spend, same distinction the repo already draws for disclosure-only rows.

---

## §10 — Audit hooks (runnable)

```bash
# Confirm the conditioner definition this brief reuses is unchanged since Q-RANGEXFER-1's own close
grep -n "WINDOW, Q_BIAS, Q_REF = 60, 0.80, 0.50" lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate2_overnight_rth_transfer.py
# Expected: one match

# Confirm ORB-MNQ-1's exact Instrument construction this brief's Phase 1 reuses
grep -n "or_bars=2\|open_tod=ol.OPEN_TOD_US\|close_tod=CLOSE_TOD_CORRECT" lab/analysis/orb/orb_mnq_2026-07/run_orb_mnq_bulenox_blusky.py
# Expected: matches confirming or_bars=2, 09:30 open, 15:45 close

# Confirm the F2 GUARD text this brief's §5 distinguishes itself from
grep -n "F2 GUARD" ops/instruments/MNQ.md

# Confirm the raised-bar filter-role exemption precedent
grep -n "unbound for continuation" docs/rejected_candidates.md

# Confirm the parked pursuit's own re-entry clause and expiry
grep -n "re-entry:\|expiry:" docs/pursuits/b3-orb-mnq-payability-line.md

# Confirm the Tradeify payability floor this brief's §4/§6 gate against
grep -n "win_rate .= 50%\|\\$3,000" lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md
# Expected: "no cell at `win_rate <= 50%` is `FEASIBLE`" and "$3,000 trail" hits (the file's own
# prose, not the brief's paraphrase — verified 2026-08-30 that neither "win_rate >= 55-60%" nor
# "trailing rope" appears verbatim in this file)

# Hash-verify the vendor bars Phase 1 reads
python -c "
import hashlib
h = hashlib.sha256(open('core/data/bar_data/MNQ_M15.csv','rb').read()).hexdigest()
print(h[:16])
"
# Expected: 6c86f41a17b7dfce (matches core/data/bar_data/SHA256SUMS)
```

---

## Verification

```bash
$ python .claude/skills/brief-authoring/scripts/check_brief.py docs/briefs/Q-RANGECOND-1-overnight-range-conditioned-orb-mnq-payability.md --type inquire
# Expected: RESULT: well-formed

$ git log -1 -- docs/briefs/closures/Q-RANGEXFER-1-closure-ambiguous-design.md
# Expected: e7a7bcb

$ git log --oneline docs/briefs/pre-registration/Q-RANGECOND-1-verdict-preregistration.md
# Expected: pre-registration commit == this brief's own commit (both filed together, before Phase 1)
```

---

## §11 — Phase 1-3 execution record

**2026-08-30 — Phase 1-3 executed same day as the Route ① ruling. Verdict: `RESOLVED`, with one
disclosed panel-vintage caveat.** Full record:
[`rangecond_1_2026-08-30/RESULTS.md`](../../lab/analysis/_inbox/rangecond_1_2026-08-30/RESULTS.md).
Reused `orb_lib.orb_backtest`/`session_panel` and the exact `ORB-MNQ-1` `Instrument` construction
verbatim, and the frozen `bias_overnight` conditioner verbatim, joined on `trading_day`/`day` (no
adjustment needed — `orb_lib`'s own plain ET calendar date and `data_lib.py`'s own Globex-cutover
`trading_day` are equivalent for RTH-scoped sessions, since the cutover only affects overnight
bars `session_panel` already discards). One real bug found and fixed during the run (a known
pandas-2.x `datetime64[us]`-vs-`[ns]` trap, already documented once in this repo at Q-ICTEXP-1) —
disclosed in `RESULTS.md`, not silently patched. **Headline:** conditioned-subset win rate
66.47% vs unconditioned 41.72% (+24.75pp, CI `[+18.30pp,+31.31pp]`); mean win (winners only)
+1.571R vs +0.860R (+0.711R, CI `[+0.543R,+0.887R]`). n_conditioned=340 (≫ the 30-trade floor).
All four pre-registered limbs (L1-L4) clear → `RESOLVED` per pre-reg §C. **Caveat, disclosed not
hidden:** this run's own unconditioned-population summary stats are computed on `MNQ_M15.csv`
(2020-07→2026-07, 1,548 RTH sessions) — a ~300-day-shorter, more-recent-starting panel than
`ORB-MNQ-1`'s own original G8 admission pipeline used (`RESULTS.md`'s own cited "2019-05-06→
present," 1,857 sessions). This does not affect the conditioned-vs-unconditioned comparison
itself (both measured on the identical panel, differing only in the conditioner split), but means
the absolute headline figures are a fresh measurement on the current canonical panel, not an
exact reproduction of the original admission numbers — any future full re-MC should standardize
explicitly on one panel vintage rather than blend them. Closure filed per §9:
[`Q-RANGECOND-1-closure-resolved.md`](closures/Q-RANGECOND-1-closure-resolved.md). No `core/`,
Pine, allocation, `dd_protection`, or rail change; no live spend; `K_intrinsic=1` per §8.
— Claude Code, executing Phase 1-3 under the operator's Route ① ruling
