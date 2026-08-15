# Objective composition map

**Status:** standing reference, established by [`Q-OBJCOHERE-1`](../briefs/Q-OBJCOHERE-1-objective-coherence-audit.md) → [`FALSIFIED-COHERENT`](../briefs/closures/Q-OBJCOHERE-1-closure-falsified-coherent.md), 2026-07-30.
**Purpose:** a single place to look up which objective instrument governs a given decision class, and — where more than one instrument touches the same class — the precedence rule between them. This is **not** a new gate, registry, or tracked metric layer (see the retired 2026-05-11 Objective-Map, a different mechanism — a Notion goal-tracking registry — retired 2026-07-12 for unrelated reasons). This map is inert: it records what the estate already ratifies; it does not decide anything new.
**Maintenance:** update this file when a new Accepted ADR, RATIFIED spec, or FROZEN pre-registration adds or changes a decision-class/precedence clause. No recurring review cadence is created — this is documentation, not a standing audit.

---

## How to read this

For each decision class below: the governing instrument(s), each one's denomination (survival / expectancy / cost / structural / hybrid), and — where two instruments touch the same class — the precedence rule that resolves any apparent overlap, quoted from its ratified source.

---

## Candidate admission (new, unproven strategies/candidates)

**Governing instrument:** survivor-scoring Part A gate — `docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md` (FROZEN 2026-07-13). Survival-denominated: bust ≤3.0% ∧ pass ≥50%, discharged iff both hold on ≥2 firms.

**Does NOT govern:** rung selection of an already-admitted book (see below) — the fork-B ADR states this is forbidden to conflate: "Extending the EV objective to candidate ADMISSION" (`2026-07-23-c1-rung-selection-ev-objective.md`, §5 forbidden moves).

**Layered pre-screens feeding this gate (necessary, not sufficient — never a substitute for it):**
- Stage-8 variance-dominance/risk-breadth screen (`ops/prop_envelope_default.md` §2 item 6 / `docs/adr/2026-07-20-stage8-variance-dominance-risk-neff-gate.md`) — "gate[s] composition-into-the-book only. They do not gate lifecycle admission." Necessary-not-sufficient is stated redundantly in the canonical Stage-8 doctrine row, methodology lesson M-21, and the third-leg spec's own R4 row.
- Third-leg target spec §7 (`docs/spec/2026-07-27-third-leg-target-spec.md`, RATIFIED) — a further screening standard, explicitly "not an admission" (§6.2).
- Q-BUSTGATE-1's fee/upside re-derivation (`docs/briefs/closures/Q-BUSTGATE-1-closure-falsified.md`) tested whether the 3.0% figure itself is economically justified, found it is not an economic quantity, and — via the fork-B ADR it produced — **retained the figure unedited** for admission purposes. The third-leg spec's T5 row cites "the ratified criterion," the same 3.0% figure, without naming Q-BUSTGATE-1 (a documentation cross-reference gap, not a live divergence — both currently agree the number is 3.0%).

## Rung selection (sizing among admissible rungs, already-admitted c1 book only)

**Governing instrument:** fork-B EV-per-dollar-day objective — `docs/adr/2026-07-23-c1-rung-selection-ev-objective.md` (Accepted). Hybrid: expectancy-optimizing (point-optimum) among rungs that clear a hard survival precondition (both-halves regime-robustness PASS).

**Explicit scope (verbatim, L46):** "the c1 book's rung selection only. Not candidate admission; not the locked strategies' parameters; not `dd_protection` constants; not any other firm/account."

**Precedence with the admission gate:** the two instruments never adjudicate the same decision — one sizes an admitted book, the other admits new candidates. Corroborated by an already-executed scoring record (`lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/G8_INTAKE.md`) showing this exact split — Part-A admission discharged independent of a later both-halves regime-gate result on the same book — was standing practice before the fork-B ADR existed, not a post-hoc carve-out.

**Pinned rung (historical — no live c1 book since 2026-08-04 de-scope):** the GO ADR held the deployed book at WATCH-1 0.50× because 1.00× failed the both-halves regime gate (figures + owner: [`GO ADR`](../adr/2026-07-17-c1-rail-build-account-registration-go.md) · regime evidence under `lab/analysis/c1/`). A higher rung still requires a fresh both-halves PASS + admitting ADR — not the EV-objective ADR's acceptance alone. Venue de-scope: [`2026-08-04`](../adr/2026-08-04-tradeify-venue-descope-eval-included.md).

## Book composition (combining admitted legs into one account's book)

**Governing instrument:** Part-A composed-bust ceiling, applied via the account-segregation requirement for a joint MC — `docs/adr/2026-07-13-prop-account-book-segregation.md` + the survivor-scoring Part A gate. Survival-denominated.

**Pre-screen (necessary, never sufficient):** Stage-8 `n_eff_risk_delta > 0` (risk-breadth, not dependence-breadth — methodology lesson M-21). ORB-MNQ-1 is the negative control: cleared the pre-screen at +0.003, still took composed bust from 2.65% to 38.75% (`Q-COMPOSE-1`, `CLOSED-FALSIFIED`). The pre-screen's own ratifying ADR and its 2026-07-13 sibling predate ORB-MNQ-1 by three days and already frame it as necessary-context, never the grant.

**Sequencing with the hedging-compliance rule (§4a below):** hard-structural/compliance screens (hedging, cap, session, instrument-class) run **first** and absolutely; risk-breadth scoring only reaches a candidate that survives them. Made mechanical in the third-leg spec's §6.2 adjudication table: `SCREEN-FAIL` on any S-requirement closes the candidate before R4 (risk-breadth) is ever scored.

## Hedging / same-Product-Group compliance

**Governing instrument:** `ops/prop_envelope_default.md` §4a (venue-derived; hard structural, no discretion) + `docs/adr/2026-07-17-c1-rail-build-account-registration-go.md` §5 forbidden-move addendum (2026-07-22) + third-leg spec §7.1 S4 (RATIFIED).

**Absolute, no exceptions:** a short-capable or opposing-sign Equity Index Product Group leg cannot coexist with a long Equity Index leg on the same account **or any account under the same control** — regardless of what the risk-breadth gate would otherwise reward.

**Precedence with the decorrelation/risk-breadth admission gate:** hard-structural — Product Group + sign screen before risk-breadth scoring. Named in three places that now agree: `ops/prop_envelope_default.md` §4a (design-consequence precedence clause, updated 2026-07-30 from the prior unresolved "note this interacts" wording — T4 residual of [`Q-OBJCOHERE-1`](../briefs/closures/Q-OBJCOHERE-1-closure-falsified-coherent.md)), the GO ADR's 2026-07-22 addendum ("Decorrelation candidates must now be screened for **Product Group + sign** before scoring"), and the third-leg spec's mechanical adjudication order (S4 kills the candidate before R4 ever runs).

## Protection sizing (dd_protection trigger/scale)

**Governing instrument:** per-instance `(trigger, scale, reference_mode)` objective template — `docs/adr/2026-07-13-dd-protection-concept-not-constant.md` (Accepted): "minimize P(bust against THAT firm's live barrier) at least sizing intervention, subject to a productivity floor." Survival-denominated. Frozen literals live in `core/dd_protection.py` (human summary: [`CLAUDE.md`](../../CLAUDE.md) §Protection); consumed by c1; new instances require pre-registered re-MC + both-halves regime gate + admitting ADR.

**Does not overlap** with rung selection, cap allocation, or candidate admission — each is a distinct, explicitly-scoped decision class with its own owning ADR chain (DD trigger/scale calibration → C2 relock → ULP-rounding companion → concept-not-constant, an explicit linear supersession lineage, never a competing pair).

## Cap allocation (per-leg contract-cap split, MYM/MNQ)

**Governing instrument:** `docs/adr/2026-07-17-c1-rail-build-account-registration-go.md` Addendum 2026-07-22 (Accepted) — a compliance fix (contract-cap correctness), not a pricing objective.

**No standing EV/survival pricing requirement governs this decision class today.** Q-CAPALLOC-1 (`docs/briefs/pre-registration/Q-CAPALLOC-1-verdict-preregistration.md`, FROZEN, closed `AMBIGUOUS (d)`) is the only instrument that prices this tradeoff, but it explicitly disclaims mandating authority over live sizing ("Scope: measurement only. No LEG_MAP edit") and its own best-case outcome routes to "operator + amending ADR" — an instrument that does not yet exist. **This is a genuine process gap, flagged by Q-OBJCOHERE-1's audit of T3**, not a contradiction between two live instruments: no pricing objective existed at the 2026-07-22 decision's own time, and none self-executes today. Recommendation for the operator (not self-executed by this map): any future compliance-driven cap/LEG_MAP change might usefully require an ex-ante EV/survival pricing check, closing the gap Q-CAPALLOC-1 can currently only measure ex post.

## Program-level success

**Governing instrument:** four-firms ADR §4 falsifier — `docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md` (Accepted). Survival-denominated: ≥2 of four `FRIENDLY` firm tiers clear the bust-rate ceiling by 2026-11-08, else demote to research-only.

**Current status:** discharge WITHDRAWN 2026-07-22 (eval-lock geometry correction; zero tiers currently clear at the frozen $100K band under corrected geometry) — the frozen gate itself is untouched; only the discharge claim was retracted. Two 50K-tier Part-A clearers were found under a 2026-07-24 band re-score, defeating the demotion clause's own terms without discharging §4. See `docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md` for the canonical record — this map does not restate its narrative, only its decision class.

---

## What this map is not

- **Not a charter.** No new operation-level objective was ratified or is proposed. The audit that produced this map (`Q-OBJCOHERE-1`) found the scoped instruments already compose without a charter — see its closure for the full per-tension reasoning.
- **Not exhaustive.** It covers the decision classes the 2026-07-30 audit's 105-row inventory surfaced as load-bearing. A new ADR that opens a genuinely new decision class is not automatically wrong for not appearing here — add it when it lands.
- **Not a gate.** Nothing here blocks, licenses, or scores anything. It is a lookup table.
