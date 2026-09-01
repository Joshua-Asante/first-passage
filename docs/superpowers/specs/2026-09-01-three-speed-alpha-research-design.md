# Design — three-speed alpha research: Vet → Generate → Confirm (v2, reconciled)

**Status:** `Proposed` — design specification only; no standing methodology, gate, K rule,
candidate status, or execution authority changes until a separate ratification decision.
**Date:** 2026-09-01 (v2, same day — see Review block)
**Authors:** Joshua + Codex (v1) · Claude Code (v2 reconciliation)
**Scope:** tradeable-alpha research only. Structural, safety, governance, and measurement-method
questions continue to use ordinary INQHIORI without being forced through this funnel.
**Related:** [`INQHIORI canon`](../../methodology/inqhiori-canon.md) ·
[`strategy harvest`](../../methodology/strategy_harvest.md) ·
[`generate→confirm historical route`](../../methodology/avenue_a_generate_confirm.md) ·
[`Q-GATECAL-1`](../../briefs/Q-GATECAL-1-mechanism-gate-false-negative-rate.md) ·
[`objective composition map`](../../methodology/objective_composition_map.md) ·
[`generate/evaluate tensions note`](../../notes/2026-08-30-generate-evaluate-tensions.md) (v2 parent) ·
[`rejected-candidate patterns`](../../adr/2026-06-14-rejected-candidate-patterns.md) ·
[`rejection-register topology`](../../adr/2026-08-09-rejection-register-topology-and-bar-wiring.md) ·
[`venue-binding axis`](../../adr/2026-08-05-strategy-venue-binding-axis.md)

## Review — why v2 exists

v1 (merged via PR #246, renamed via #247) and the interpretive note
[`2026-08-30-generate-evaluate-tensions.md`](../../notes/2026-08-30-generate-evaluate-tensions.md)
were authored one day apart, diagnose the identical Route B failure from the same evidence, and
proposed **unreconciled architectures** — v1 a three-artifact speed chain, the note a single
append-only candidate contract. Neither cited the other. v2 merges them, revised in place per
amendment-first (the spec is `Proposed`; no dated-decision constraint binds). The resolution, in
one line each:

1. **Object model** — the note wins: one append-only candidate contract per candidate (§2.6);
   v1's three artifacts become sections of it; v1's three handoff packets become append events.
2. **Cost/shape gates** — the note wins: every economic gate delegates to a pinned existing
   authority; this spec forks no arithmetic (§3.3).
3. **Terminal states** — the note wins for evidence verdicts (two-axis record, mapped to the
   ratified rejection taxonomy and §D3 registers); v1's process states survive as process states
   (§2.1).
4. **Vocabulary** — v1 wins: Vet/Generate/Confirm is the surface vocabulary; the note's
   generate/evaluate phrasing is crosswalked once (§7) and never used unqualified again.
5. **Multiplicity mechanics** — the note wins: Bonferroni/Holm identity frozen at charter,
   p = 1 placeholders, succession rule (§4.2, §5.5).
6. **Role/composition timing** — the note wins: class-level structural screens at Vet ($0,
   pre-catalogue), zero-K state-drift re-check before Confirm, edge-sized composition after
   Confirm (§3.3, §5.2, §5.6).
7. **Spend bounding** — both: v1's effort percentages stay as non-binding attention guidance;
   the note's single campaign envelope is the binding control (§4.2).
8. **UNATTRIBUTED admission** — v1 wins, with the note's HARV-lane carve-out made explicit:
   the relief valve is funnel-general for non-HARV lanes and pends `Q-GATECAL-1`; HARV-lane
   candidates keep their lane's hard attestation gate in full (§3.3).
9. **Channel liveness** — the note wins: a binding trigger, not just a metric (§9).
10. **Mechanism discriminator + expression ladder** — the note wins: the discriminator's full
    adjudication rule freezes at charter; `EXPRESSION-FAIL` is bounded by an `N_expr` ladder
    keyed to the mechanism's ledger row (§4.2, §5.5).

v1's distinctive contributions all survive: the three speeds and their gates, the monotone-rigor
and evidence-isolation invariants, the tradeability-laundering rule, the promotion-floor
calibration requirement, the worked Q-VOLREGIME-1 routing, and the Phase A–D adoption plan.
The note's tensions analysis (§1–8 there) remains the standing diagnosis; its recommendations
table is absorbed here and bannered there.

---

## 1. Decision

Adopt a three-speed research funnel named exactly:

1. **Vet** — establish that the proposal is economically reachable, testable, and capable of
   changing a named trading decision.
2. **Generate** — run a bounded, selection-accounted exploration on an exploration panel and freeze
   one exact candidate expression.
3. **Confirm** — score that expression once on untouched data with the full decision-relevant
   validation battery.

And one object model:

4. **One candidate contract per candidate** — a single append-only artifact that every speed
   writes into. No stage restates another stage's fields; no separate charter, prereg, or
   handoff-packet documents exist (§2.6).

The governing principle is:

> **A candidate earns rigor by surviving cheaper evidence. Rigor increases as the candidate set
> shrinks. No candidate reaches an expensive gate merely because the preceding finding is
> scientifically interesting.**

This is an escalation wrapper around INQHIORI, not a replacement for it. Each speed may contain an
INQHIORI question, but the funnel determines how much research expense and evidentiary weight that
question has earned.

### 1.1 Why this design exists

The estate is strong at falsification, data-defect discovery, selection accounting, cost realism,
and portfolio safety. It is weaker at converting observations into executable candidates at useful
throughput. Two facts motivate a redesign rather than a relaxation:

- the historical generate→confirm route preserved untouched confirmation correctly, but was
  withdrawn after 0/4 campaigns reached Confirm; its promotion design was not productive —
  the generated statistic was never economically connected to a tradeable object, and the
  channel's own success falsifier depended on a state the channel could not reach;
- the mechanism-first gate's false-negative rate is explicitly unmeasured (`Q-GATECAL-1`), so the
  programme cannot yet claim that its low candidate supply is an optimal rejection frontier.

The answer is not to weaken Confirm. It is to make Vet cheaper and more economic, make Generate
productive but selection-honest, and reserve maximum rigor for the few candidates that earn it.

---

## 2. Common vocabulary and invariants

### 2.1 Candidate states — two axes plus process states

The promoting path is unchanged:

```text
PROPOSAL → VET-PASS → GENERATED → CONFIRMED → normal lifecycle / composition / deployment governance
```

Terminal and non-promoting states are typed on **two axes**, mapped to the ratified rejection
taxonomy ([`2026-06-14-rejected-candidate-patterns`](../../adr/2026-06-14-rejected-candidate-patterns.md)
§A) rather than minted fresh:

**Evidence axis** (verdicts about the candidate; each names its taxonomy class and its
[§D3](../../adr/2026-08-09-rejection-register-topology-and-bar-wiring.md) register at write time):

| Verdict | Meaning | Taxonomy class | Register |
|---|---|---|---|
| `CONFIRMED` | frozen expression survived Confirm | n/a (not a rejection) | n/a |
| `MARKET-NULL` | powered, adjudicated no — mechanism discriminator cleanly failed, or no discriminator dispute exists | edge-failure (add-back: genuinely new mechanism, never a re-tune) | per §D3 scope key |
| `EXPRESSION-FAIL` | discriminator cleanly **passed** while the specific entry/exit implementation failed | **expression-failure** — proposed fifth class; requires its own amending ADR before first live use (§12) | per §D3 scope key |
| `EVIDENCE-VOID` | integrity, power, coverage, or discriminator-adjudication failure prevented a verdict | none — exhausts the attempt, never evidence against the candidate; no register entry | none |

**Edition axis** (filled only for a `CONFIRMED` candidate, per the ratified
[venue-binding axis](../../adr/2026-08-05-strategy-venue-binding-axis.md)): placement-clear, or
`VENUE-FAIL(edition)`. A candidate that confirms and then fails venue evaluation is
`CONFIRMED · VENUE-FAIL(edition)` — neither fact overwrites the other; it routes to cold-store
for a different venue, never to reject. (This replaces v1's `CONFIRMED-NONDEPLOYABLE` compound
state.)

**Process states** (routing, never evidence): `PARK` (one named missing input; wake only when it
exists) · `MECHANISM-ONLY` (credible observation, no decision bridge; retained in the mechanism
library) · `ROLE-BLOCKED` (role unfit under the recorded compliance snapshot; re-screenable on
state change; never a register entry) · `VOID-*` (Generate-side integrity failures, §4.4) ·
`DROP` (Vet-side impossibility; its register entry carries the taxonomy class the failed gate
implies and a re-proposal bar).

### 2.2 Monotone-rigor invariant

Every promotion must satisfy all gates at its current speed. Later evidence cannot retroactively
waive an earlier failed gate. A later-stage failure cannot be rescued by returning to an earlier
stage and redefining the candidate.

Any change to the following creates a new candidate at `PROPOSAL`:

- entry or side rule;
- feature definition or threshold;
- holding period or exit;
- stop, target, or sizing logic;
- instrument or venue;
- conditioning state;
- data window chosen because of a seen result.

A mechanical defect repair may resume at the affected speed only when the repair restores the
already-frozen intended expression and the contaminated result is discarded. A semantic or economic
change restarts at Vet. Repeated expression restarts against a surviving mechanism are bounded by
the `N_expr` ladder (§5.5).

### 2.3 Evidence-isolation invariant

The three speeds use distinct evidence scopes:

| Speed | Permitted evidence | Forbidden evidence |
|---|---|---|
| Vet | prior literature, prior closed campaigns, instrument/venue facts, coarse non-outcome arithmetic | ranking fresh candidate P&L, reading the reserved Confirm panel |
| Generate | the frozen exploration panel and declared catalogue only | any Confirm observation, aggregate, timestamp-derived score, or post-result catalogue growth |
| Confirm | the frozen untouched Confirm panel, once | retuning, alternate windows, sibling rescue, threshold movement, second one-shot |

### 2.4 K and search accounting

- Vet uses `K=0` only while it performs no fresh outcome-bearing comparison. A return, P&L,
  direction, or predictive-score look opens K before the look.
- Generate declares `K_intrinsic` as every expression that could be selected from the frozen
  catalogue. Skipped-but-available expressions still count.
- Confirm declares `M`, the number of generated candidates allowed to touch Confirm. Default `M=1`.
  `M>1` requires the frozen multiplicity configuration of §4.2 before Generate results are read.
- `K_banked` remains disclosure-only under standing doctrine; it is never silently added to the
  candidate's intrinsic search count.
- **Lane rules ride along.** A harvest-lane candidate remains bound by its lane's own Clause-K
  screen (`K_eff ≤ 3`, floors 0.65/0.85/0.98 —
  [`strategy_harvest.md`](../../methodology/strategy_harvest.md) Clause K); that band is
  lane-scoped, not a funnel ceiling. Non-harvest lanes price selection through the DSR-at-K floor
  at their declared catalogue size, exactly as standing doctrine already requires. Whether a
  unified K band should ever replace per-lane bands is a separate ratification question (§12).

### 2.5 No tradeability laundering

An observation that predicts range, volatility, state, or another diagnostic quantity is not
tradeable alpha until it names an executable decision bridge. "It may be useful as a filter" is not
a bridge. A valid bridge specifies:

```text
observable → frozen decision changed → executable expression → economic quantity improved
```

Conditioner-only observations may be retained in the mechanism library without advancing through
the alpha funnel. (This is the same rule the tensions note states as "delete proxy-only
promotion" — a proxy statistic may win exploration diagnostics but can never consume a Confirm
holdout or claim candidate status.)

### 2.6 The candidate contract

One append-only artifact owns each candidate's entire funnel state. Sections are appended at each
speed; **no section restates another section's fields** — later sections reference earlier ones by
heading and commit hash. The contract accumulates:

1. **Vet section** — the Vet card (§3.2) and six-gate verdict.
2. **Charter section** — the Generate charter (§4.2), appended only on `VET-PASS`; its freeze is
   the commit that lands it.
3. **Selection freeze** — appended when Generate execution closes (§4.3 step 9): the full scored
   ranking and selected expression(s), hash-pinned before any Confirm access.
4. **Confirm prereg section** — appended before any Confirm access (§5.2); references the frozen
   expression by selection-freeze hash instead of copying it.
5. **Verdict appendices** — Confirm verdicts (both axes), `ROLE-BLOCKED` dispositions,
   `TRADEABLE-REACHABLE`-style pre-explore kills, each separately keyed, appended and never
   edited.

Freeze integrity is auditable from git history: each phase's opening line records the commit hash
of the prior section's freeze, and any edit to a frozen section is visible in `git log -p`. A
contract whose frozen sections were edited after their recorded freeze commit is
integrity-invalid; the attempt voids.

This dissolves v1's three handoff packets: the Vet→Generate, Generate→Confirm, and
Confirm→lifecycle packets are the contract's own sections 2–5, plus the lifecycle handoff
appendix (§6). It also answers v1's open decisions 1 and 6 — the Vet card's owner is the
contract's opening section, and funnel state needs no second registry (an index file may list
contracts; it owns nothing).

---

## 3. Speed 1 — Vet

### 3.1 Purpose

Vet answers one question:

> **Is this proposal sufficiently reachable, decision-relevant, and testable to deserve an
> outcome-bearing Generate campaign?**

Vet is intentionally cheap. It rejects impossibilities and category errors before statistical
craftsmanship is spent on them.

### 3.2 Required Vet card

The contract's opening section records:

| Field | Required content |
|---|---|
| Candidate ID | stable slug and version |
| Observation / source | what produced the proposal; no strength inflation |
| Decision bridge | exact decision that changes if the candidate works |
| Trade expression | instrument, side rule, entry clock, exit/hold, and initial risk geometry |
| Role | entry, exit, execution, sizing, conditioner, or portfolio-composition |
| Venue legality | target venue/account and known structural constraints |
| Mechanism discriminator (named) | the observable that will later separate `EXPRESSION-FAIL` from `MARKET-NULL`; its full adjudication rule freezes at charter (§4.2) |
| Data route | available source, span, fidelity, and estimated acquisition cost |
| Cost reachability | scored by the pinned cost authority (§3.3 gate 3), in that gate's own units |
| Payoff-shape reachability | scored against the venue's measured binding constraint, from citable shape priors or a declared extraction probe (§3.3 gate 4) |
| Power / cadence | expected independent N and minimum detectable effect |
| Economic prior | WHO/WHEN/WHY-survives/HOW-dies when known; otherwise explicitly `UNATTRIBUTED` |
| Prior-art consult | instrument cell, rejected registry, manifests, and adjacent candidates |
| Search declaration | proposed Generate catalogue, `K_intrinsic`, exploration window, Confirm reserve |
| Kill conditions | exact Vet failures and re-proposal bar |

### 3.3 Vet gates

All six must clear:

1. **Decision gate** — a named executable decision changes. Conditioner-only findings without a
   decision bridge route to the mechanism library, not Generate.
2. **Structural gate** — instrument, venue, session, data, latency, and product constraints do not
   make the expression illegal or impossible. This gate **absorbs the class-level structural role
   screens** where the candidate class is subject to the eval-mechanism-shape screen
   ([spec](../../spec/2026-08-05-eval-mechanism-shape-screen.md) §2.0a places them pre-catalogue,
   pre-data, at zero evidentiary cost, and prices late application to a scored list as a K
   charge): EM0 catalogue, EM3 independence arithmetic, EM4 activity-by-construction, and
   EM5/N-SHAPE's imported Product-Group/sign, session-law, and S7 occupancy limbs. Pruning
   role-impossible cells here shrinks the catalogue **before** `K_intrinsic` is set.
3. **Cost gate** — **delegated, never rederived.** The conservative effect/payoff estimate is
   scored against the standing cost-law hurdle by the authority the eval-mechanism-shape screen's
   EM1 currently points at ([`strategy_harvest.md`](../../methodology/strategy_harvest.md)
   Requirement 5), with [`cost_geometry_pregate.py`](../../adr/2026-06-22-cost-geometry-pregate.md)'s
   Phase-0 quantity additive alongside — this spec forks no cost formula. The **pin** (authority,
   revision, formula, adjudication basis) is recorded in the Vet card and re-pinned at charter
   freeze; if the authority is later re-pointed, an already-frozen campaign **voids and refreezes
   under the new authority** — it is never silently re-scored. Missing inputs route to a bounded
   measurement probe under its own pre-approved probe envelope (§4.2), never invented arithmetic.
4. **Shape gate** — the hypothesized win rate, payoff ratio, cadence, and barrier exposure occupy a
   feasible region for the target venue's **measured** binding constraint (for the incumbent eval:
   the shape-feasibility map, not an assumed rule). Shape inputs must be citable priors carried
   under harvest-Requirement-2 discipline (conservative central reading, decay haircut, never an
   invented number) or produced by a declared pre-freeze extraction probe run outside the reserved
   Confirm window. A statistically plausible but venue-impossible shape dies. No contract freezes
   with this limb unscored.
5. **Power gate** — the reserved panels can discriminate a useful effect at the declared N. A test
   that can only return underpowered ambiguity does not open.
6. **Novelty gate** — the candidate is not a relabeled dead cell. A prior kill requires its recorded
   re-proposal bar to be satisfied by new evidence; a prior `EXPRESSION-FAIL` mechanism additionally
   requires its `N_expr` ledger row consulted and cited (§5.5).

Economic attribution is disclosed at Vet but is not an absolute alpha-admission gate in this
proposed design — **for non-HARV lanes**. An `UNATTRIBUTED` candidate may pass only when it has a
precise decision bridge and accepts the stricter Confirm posture in §5.4. This is the design's
deliberate relief valve pending `Q-GATECAL-1` (Phase B, §10); it does not amend standing doctrine
unless this design is separately ratified. **HARV-lane candidates are carved out**: their lane's
hard pre-freeze attestation
([ratification](../../adr/2026-07-13-harv-discovery-lane-ratification.md) §2 as strengthened by
the [same-units supersession](../../adr/2026-07-16-harv-attestation-same-units-supersession.md))
continues to bind in full, unrelieved.

### 3.4 Vet outputs

| Output | Meaning | Next action |
|---|---|---|
| `VET-PASS` | all six gates clear | append and freeze the Generate charter |
| `DROP` | a permanent or currently binding impossibility | register entry (taxonomy class per the failed gate) with re-proposal bar |
| `PARK` | one named missing input could change the answer | wake only when that input exists |
| `MECHANISM-ONLY` | observation is credible but has no decision bridge | retain finding; no alpha campaign |
| `VOID` | Vet consumed forbidden outcome evidence | rebuild with a fresh panel or stop |

### 3.5 Effort ceiling

Default Vet effort is **no more than 10% of the candidate's expected total research effort** and
normally one contract section. If Vet requires a bespoke model, extensive simulation, or
multi-round method-design review, the proposal has not yet shown that it belongs in the alpha
funnel. (Effort percentages here and in §4.5/§5.7 are attention guidance, not the binding spend
control — that is the campaign envelope, §4.2.)

---

## 4. Speed 2 — Generate

### 4.1 Purpose

Generate answers:

> **Within a bounded, economically coherent catalogue, is there one exact expression that earns a
> single untouched confirmation attempt?**

Generate is allowed to search. It is not allowed to disguise searching as confirmation.

### 4.2 Generate charter — appended and frozen before any exploration score

The charter section freezes:

- candidate family (by reference to the Vet section — no restatement);
- exploration and Confirm windows, non-overlapping and immutable — the Confirm reservation is
  committed **here, before any exploration data is read**, so no later step can influence which
  interval becomes the holdout;
- full expression catalogue with stable IDs;
- `K_intrinsic` and Confirm budget `M`;
- **the multiplicity configuration**: `α`, `M`, and the named procedure — Bonferroni (the fixed
  per-candidate bar `α/M` freezes here) or Holm step-down (the **algorithm identity** freezes;
  its per-candidate thresholds `α/(M−i+1)` attach only after observed Confirm p-values are
  ordered and cannot be pre-assigned);
- **the succession rule** for a blocked or forfeited Confirm slot: forfeit by default (slot
  unread; divisor stays `M`, conservative), or pre-declared mechanical succession (next-ranked
  from the frozen exploration ordering; divisor stays `M`; no discretion after exploration
  results are visible);
- **the mechanism discriminator's full adjudication rule** (from the Vet card's named
  observable): statistic, null, direction, threshold, and coverage/power requirement — measured
  independently of the specific implementation's payoff, fixed now, never chosen or interpreted
  after the holdout is read;
- data cleaning, roll, session, missing-bar, and duplicate rules;
- executable cost model **by pin** (§3.3 gate 3 — authority, revision, basis);
- primary promotion statistic;
- minimum economic effect, not merely statistical significance;
- null/placebo and uncertainty method;
- selection rule when more than one expression clears;
- minimum cell N and `VOID-POWER` rule;
- one deterministic promotion threshold;
- output schema and seeds;
- **the campaign envelope** — the binding spend control, approved by one operator GO at this
  freeze: maximum data spend, schemas, windows, and K. Within the envelope no further spend
  approvals are owed; a fresh GO is required only to exceed it or to cross into sandbox/capital.
  Confirm attempts are never an envelope item — they stay bound to the frozen multiplicity
  configuration, and any `VOID-*` exhausts the attempt (fresh campaign, fresh holdout, never a
  retry inside the same envelope). A pre-freeze shape-extraction probe (§3.3 gate 4) runs under
  its own smaller pre-approved probe envelope, which this envelope then subsumes by citation.

The promotion rule must be calibrated before the real exploration score is read. Calibration may use
synthetic nulls, planted effects, or prior closed panels that cannot enter the campaign. It must show
both false-promotion behavior and useful power. A promotion floor that produces no candidates under
economically meaningful planted effects is itself invalid; this explicitly corrects the historical
0/4-never-reached-Confirm failure rather than reviving that route unchanged. The discriminator's
adjudication rule is calibrated the same way, in the same pass (§10 Phase C).

### 4.3 Generate execution

1. Verify data hashes/provenance and the exploration/Confirm partition.
2. Open the K record before computing any outcome-bearing score.
3. Score every declared catalogue expression once on exploration.
4. Apply costs (pinned model) and the frozen promotion rule.
5. Select at most `M` expressions using the frozen ordering.
6. Freeze each promoted expression byte-faithfully: no parameter remains open.
7. Emit a compact result table for every expression, including failures.
8. Do not load, summarize, count, or inspect Confirm data.
9. **Close with the selection freeze**: append the full scored ranking and the selected
   expression(s) to the contract, hash-pinned, before any Confirm access. The selected set cannot
   be edited afterward; Confirm's integrity check (§5.2) compares against exactly this commit.
   Without it, "the selected cell matches the frozen contract" would be unverifiable, since
   selection necessarily post-dates the charter freeze.

Generate may use train/validation subdivision inside exploration when the charter freezes it, but
that subdivision does not become Confirm. Hyperparameters chosen inside exploration are part of the
selected expression and their available choices count toward selection accounting.

### 4.4 Generate outputs

| Output | Meaning | Next action |
|---|---|---|
| `GENERATED` | one or more expressions clear; no more than `M` selected | append Confirm prereg without looking at Confirm |
| `STOP-NONE` | no expression clears | close campaign; no threshold relaxation |
| `FALSIFIED-FAMILY` | frozen family-level criterion fails | close at the scope frozen by the charter; register entry typed `MARKET-NULL`/edge-failure at that scope |
| `VOID-SELECTION` | catalogue/window/K changed or Confirm was touched | no result; fresh campaign required |
| `VOID-POWER` | realized valid N misses the frozen floor | park or redesign prospectively |

### 4.5 Effort ceiling

Generate receives **approximately 20–30% of expected total candidate effort** (guidance; the
envelope binds). Its job is to select and freeze — not to prove durability exhaustively. Expensive
attribution models, full portfolio MC, production Pine, rail wiring, and deployment packaging are
forbidden here.

---

## 5. Speed 3 — Confirm

### 5.1 Purpose

Confirm answers:

> **Does the exact generated expression survive once, on untouched evidence, at sufficient economic
> and statistical strength to enter ordinary lifecycle and composition review?**

Confirm receives the majority of rigor because few candidates reach it and its errors are costly.

### 5.2 Confirm entry — two checks before any holdout access

**Integrity check, first.** Code/data hashes, K, the frozen multiplicity configuration, the
selected candidates against the hash-pinned selection freeze, and the holdout against the
charter's reservation must all match the contract. A mismatch voids or stops the attempt on its
own — it is never recorded as a structural or evidentiary rejection. If any Confirm metric was
observed before the prereg section's commit, the confirmation is void.

**Role state-drift re-check, zero-K.** Before any holdout is consumed, re-validate each selected
candidate against the *current* compliance snapshot versus the one recorded at Vet —
Product-Group/sign, cap, session, S7 order-symbol occupancy
([`objective_composition_map.md`](../../methodology/objective_composition_map.md)). The
class-level screens already ran at Vet (§3.3 gate 2); a failure here means the **state moved**
(occupancy or cap changed between scoping and Confirm), not that a screen was skipped. A failure
emits a separately keyed `ROLE-BLOCKED` appendix — naming the limb and the snapshot — and the
slot follows the charter's frozen succession rule. A succession candidate takes the slot only
after itself passing both checks in this section; role-blocking consults no holdout data, so
neither succession option leaks Confirm information into selection. Scope inherits standing
doctrine: cap/session/S7 are scoped to the account/book in scope; Product-Group/sign is absolute
across the controlled-account group. The variance-dominance limb is report-only while its
producer is tombstoned ([W4 dormancy](../../adr/2026-08-07-w4-minimal-gate-set-dormancy.md));
it blocks again only under a re-arm.

The prereg section itself **references rather than copies**: the frozen expression by
selection-freeze hash, the reserved window by charter reference, plus the primary net outcome
statistic, the economic floor and verdict map, the battery composition, defect/missingness/power
handling, the one-shot execution command and seeds, and downstream routing for every verdict.

### 5.3 Mandatory Confirm battery — one atomic verdict

Every candidate receives, as **one atomic step** whose single verdict is emitted only when all
limbs have run:

1. **Provenance and implementation integrity** — source hashes, causal clocks, duplicate/missing-data
   rules, independent feature/label spot checks, and reproduction of the frozen expression.
2. **Net economic result** — commissions, spread, slippage, and venue-specific constraints applied
   at the relevant historical basis, under the pinned cost model.
3. **Selection-aware inference** — the frozen K/M adjustment, uncertainty interval, and
   null/placebo appropriate to the statistic. Under Holm, adjudication runs jointly across all `M`
   observed p-values after the runs complete; verdicts are still per-candidate. A slot with no
   adjudicable statistic — forfeited `ROLE-BLOCKED`, voided, or never filled — enters the
   step-down as the frozen conservative placeholder **p = 1**: the family stays size `M` and a
   missing test can only make remaining rejections harder, never easier.
4. **Temporal durability** — frozen halves and regime/year slices with minimum N; no pooled rescue
   of a required failing slice. Part of the atomic verdict — `CONFIRMED` is never emitted from the
   untouched run alone before temporal robustness has cleared.
5. **Execution fidelity** — bar/tick semantics, latency, session boundaries, order type, and
   Pine/Python parity when TradingView is part of the intended path.
6. **Payoff and tail geometry** — expectancy, MFE/MAE or relevant path statistics, drawdown, and
   candidate-level survivor scoring for the target venue.
7. **Mechanism discriminator** — the charter's frozen adjudication rule, run as frozen.

Not every scientifically imaginable test belongs in Confirm. A test is included only if its result
can change the frozen verdict, candidate role, sizing ceiling, venue, composition, or monitoring
obligation. Edge-sized composition scoring is **not** in this battery — it runs after the verdict
(§5.6).

### 5.4 Attribution rule

Causal/mechanism attribution is **not a universal Confirm limb**. It becomes mandatory when:

- the candidate's claimed durability depends on a specific counterparty constraint;
- the feature is a proxy whose confounding could reverse the executable decision;
- the result would determine monitoring or capacity limits;
- attribution machinery is intended for reuse across a declared class of future candidates.

Otherwise, Confirm tests incremental out-of-sample decision value and records attribution as
`MECHANISM`, `EVIDENCE-ROBUST`, or `SURVIVAL-ONLY/UNATTRIBUTED`. Unattributed confirmed candidates
inherit the standing tighter lifecycle treatment; they are not barred solely for lacking a complete
story.

### 5.5 Confirm verdicts — evidence axis, discriminator-adjudicated

| Verdict | Trigger | Next action |
|---|---|---|
| `CONFIRMED` | all frozen gates clear, temporal limb included | lifecycle candidate intake; §5.6 then the edition axis |
| `MARKET-NULL` | implementation fails AND the discriminator cleanly fails (powered, adjudicated no) — or no discriminator dispute exists | close mechanism at the frozen scope; edge-failure register entry; re-proposal bar = new mechanism evidence |
| `EXPRESSION-FAIL` | implementation fails while the discriminator **cleanly passes** | the expression closes and stays barred; the mechanism survives — see the `N_expr` ladder below |
| `EVIDENCE-VOID` | the discriminator's own frozen coverage/power is unmet (takes precedence over any payoff verdict — an underpowered discriminator is never evidence against the mechanism), or the confirm run itself fails coverage/power/integrity | attempt exhausted; eligible for a fresh campaign with a fresh holdout; never terminal on its own |
| `AMBIGUOUS-HOLD` | valid test lands in a predeclared uncertainty state | wake only on named information trigger |

**The `N_expr` expression ladder.** `EXPRESSION-FAIL`'s add-back is binary: a materially new
expression class of the same mechanism, differing on a declared structural axis (stop logic, exit
family, or holding-horizon class — never a parameter re-tune of the failed expression), admitted
as a **new contract** with fresh K and a fresh holdout, citing the failed entry. The ladder
terminates: the attempt bound `N_expr` (default 2, ratified with the fifth-class ADR, §12) and
the running attempt history are keyed to the **mechanism** on its own ledger row — never merely
declared inside a contract — and every new expression contract must declare its ordinal (attempt
`k` of `N_expr`, naming each prior failed class); a contract that omits or contradicts the
ledger's count is integrity-invalid at §5.2. Once `N_expr` independent expression classes have
each produced `EXPRESSION-FAIL` while the discriminator kept passing: if the recorded failures
include a cost or execution-geometry limb, the mechanism entry migrates to the ratified
venue/cost-constraint class and its existing add-back; if they fired on non-cost limbs, no cost
claim may be fabricated — the entry stays in expression-failure with the ladder closed, reopenable
only by operator ratification citing the full failure history.

No Confirm outcome authorizes arming, live spend, or autonomous promotion.

### 5.6 Post-verdict: composition, venue, and the edition axis

Only for a `CONFIRMED` candidate, and only now that an edge size exists: score composition and
venue fit — variance dominance, risk breadth, common-regime exposure, joint MC when the proposed
use is inside a book (low correlation alone never clears composition), activity, drawdown, and
remaining sizing; re-run the §5.2 role re-check if the deployment target changed, and always
re-check S7 occupancy (it moves independently of the target). The outcome lands on the **edition
axis**: placement-clear, or `VENUE-FAIL(edition)`. A role or composition failure here rejects
that placement, not the candidate's standalone confirmed status; it is not evidence the market
effect is false, and it enters no rejection register.

### 5.7 Effort allocation

Confirm receives the remaining **60–70% of candidate research effort** (guidance), conditional on
the candidate having earned it. This is where adversarial review, independent reproduction,
expensive simulation, and native-platform parity belong.

---

## 6. Contract lifecycle (replaces v1's handoff packets)

There are no handoff packets. The contract's own sections are the handoffs (§2.6). One appendix
remains owed at the boundary this funnel does not govern:

**Confirm → lifecycle appendix**, appended for a `CONFIRMED` candidate: intended role and venue;
durability-source tag (§5.4); composition requirements and the §5.6 edition-axis outcome;
monitoring observable and decay-trigger design obligation; all caveats that survived
confirmation.

Lifecycle, composition, capital allocation, Pine productionization, rail wiring, and arming retain
their own standing authority. The three-speed funnel does not collapse those layers.

---

## 7. INQHIORI mapping and vocabulary crosswalk

The three speeds preserve the loop while preventing every observation from receiving maximum-cost
investigation immediately:

| INQHIORI work | Vet | Generate | Confirm |
|---|---|---|---|
| Identify / Notice | source observation and decision context | exploration-only data | frozen candidate + untouched panel |
| D-S-A | delete impossible expressions; compress to Vet card | freeze/index catalogue | freeze executable packet and audit hooks |
| Question | is this reachable and decision-relevant? | which bounded expression earns Confirm? | does the frozen expression survive? |
| Hypothesis | economic reachability hypothesis | promotion hypothesis | final executable hypothesis |
| Investigate | arithmetic and source verification | bounded exploration | one-shot full battery |
| Observe / Reflect | PASS/DROP/PARK | GENERATED/STOP/VOID | CONFIRMED/NULL/FAIL/VOID/HOLD |
| Iterate | new evidence only | new campaign; fresh K/window | new expression restarts at Vet, on the `N_expr` ladder |

**Crosswalk to the tensions note's phrasing** (so the two vocabularies never blur again): the
note's "lean generate phase" steps 1–6 ≈ Vet plus charter authoring; its step 7 ≈ Generate
execution; its step 8 ≈ this spec's §9 liveness trigger; its "lean evaluate phase" ≈ Confirm
entry, battery, verdicts, and §5.6. The note's "generate/evaluate" is never a synonym for this
spec's Generate speed.

The canon's bounded-acceleration rule applies at every speed: tooling must be cheaper than the future
queries it enables. A reusable method may justify more investment than a one-off candidate, but its
reuse class and expected consumers must be named before construction.

---

## 8. Worked routing — Q-VOLREGIME-1

This example is diagnostic and does not change that Q's standing authorization.

### Vet read

The finding has strong presence evidence: elevated same-slot M15 volume predicts elevated next-bar
range within both trigger-range strata on MNQ and MYM. Its current role is `conditioner`; it does not
specify direction, favorable excursion, an entry, or a venue-native non-directional volatility trade.

Under this design it would therefore route:

```text
credible observation
  → Vet Decision gate asks for a precise trade bridge
  → absent bridge: MECHANISM-ONLY (retain; no alpha Generate)
```

Possible future bridges must be separate proposals, for example:

- one frozen existing directional signal whose MFE/MAE changes under the state;
- one execution choice whose realized cost changes under the state;
- one venue-legal volatility expression.

Each bridge starts at Vet with fresh K/window accounting. L5 attribution may still proceed as a
methodology investment if it names a reusable consumer class, but it is not represented as the
fastest path to tradeable alpha merely because L1–L4 are strong.

(A first prospective bridge of exactly this family — a GRADUATEd range predictor gating a frozen
construct — was Vetted 2026-09-01: `GAPCOND-ORB-1`, card at
`docs/notes/2026-09-01-gapcond-orb-1-vet-card.md` via
[PR #249](https://github.com/Joshua-Asante/first-passage/pull/249), authored under v1 ahead of
Phase A and disclosed as such.)

---

## 9. Programme metrics and the channel-liveness trigger

The funnel is not successful merely because each artifact is internally correct. Report quarterly:

| Metric | Purpose |
|---|---|
| Proposals entering Vet | observation supply |
| Vet PASS/DROP/PARK/MECHANISM-ONLY counts | front-door selectivity |
| Median time and research cost to Vet disposition | cheap-kill performance |
| Generate campaigns and catalogue K | search breadth actually paid |
| Fraction producing `GENERATED` | promotion calibration |
| Confirm attempts and pass rate | exploration quality |
| Median time from proposal to Confirm verdict | research velocity |
| Confirmed candidates reaching lifecycle/composition | trade-expression relevance |
| Candidates surviving venue and composition | operational conversion |
| Defects found at each speed | placement of review effort |
| Sampled false-negative rate of early gates | over-correction risk |
| Research hours per decision-changing result | total programme efficiency |

**One row is a trigger, not a metric.** Each candidate-source channel carries a liveness bound —
default **4 consecutive campaigns or 2 consecutive quarters without a single Confirm attempt,
whichever comes first**, pre-declarable per channel at its first campaign — and reaching it forces
a mandatory retire-or-redesign disposition decision, never a silent continuation. The default is
Route B's own lifetime record (0-for-4): the failure mode this trigger exists to catch is a
channel that stays honest while never becoming testable, which candidate-level gates cannot
detect. A dead channel closes or is redesigned; the bound never licenses broader fishing.

Do not target a high Confirm pass rate. Target calibrated flow: enough candidates reach Confirm to
learn, while untouched Confirm remains difficult to pass. Promotion-rate targets must be set by a
separate calibration exercise, not inferred post hoc from the first cohort.

---

## 10. Adoption plan and required calibration

This design must not become standing doctrine from prose approval alone.

### Phase A — historical shadow routing (`K=0`)

Apply Vet retrospectively to a frozen sample of closed candidates without changing their recorded
verdicts. The sample must include:

- cost-law kills;
- power/cadence kills;
- evidence/direction kills;
- the ORB-MNQ survivor;
- at least one later-discovered implementation defect;
- conditioner-only findings such as Q-VOLREGIME-1.

Measure whether Vet would have:

- killed known impossibilities earlier;
- preserved the known survivor;
- routed scientific-but-nontradeable findings out of the alpha queue;
- exposed ambiguous mechanism-gate cases rather than silently dropping them.

This is process validation, not a re-verdict of any historical candidate.

### Phase B — gate false-negative read

Read `Q-GATECAL-1` or an explicitly superseding calibration before ratifying the proposed
`UNATTRIBUTED` relief valve. A nonzero false-negative finding informs the design; it does not
automatically abolish mechanism grounding.

### Phase C — Generate promotion calibration

Before the first live campaign, validate the promotion rule family — and the mechanism
discriminators' adjudication-rule families alongside it — on synthetic nulls and planted
economically meaningful effects. Freeze acceptable false-promotion and power bands prospectively.
The old 0/4 route is a negative control: a floor that cannot promote realistic planted effects is
not "rigorous"; it is nonfunctional.

### Phase D — bounded pilot

Run the first three-speed cohort under a predeclared candidate count, time budget, and no-mid-pilot
rule changes. At cohort close, compare funnel metrics with the historical baseline. Ratification or
amendment follows; no silent extension.

---

## 11. Forbidden moves

- **Weakening Confirm to improve throughput.** Throughput is repaired in Vet/Generate; Confirm
  remains untouched and one-shot.
- **Calling Vet PASS evidence of alpha.** It means only that testing is worth its cost.
- **Running outcome-bearing "Vet arithmetic" at K=0.** Any fresh return/predictive look opens K.
- **Treating a mechanism story as a substitute for net expectancy.** WHO/WHY improves a prior; it
  does not pay spread or commission.
- **Treating net expectancy as proof of attribution.** Predictive evidence and causal attribution
  remain typed separately.
- **Letting Generate inspect Confirm coverage or aggregates.** Even knowing which period "looks
  complete" after reservation can influence selection.
- **Moving a promotion floor after 0 candidates.** Calibrate before the campaign; a dead campaign
  closes.
- **Rescuing a failed Confirm with a sibling, filter, alternate exit, or new instrument.** Every
  such expression restarts at Vet, on the `N_expr` ladder, under a new contract.
- **Building production Pine or rail code during Generate.** Productionization is earned only after
  Confirm and remains separately governed.
- **Using low correlation as composition admission.** Risk breadth, variance dominance, and joint
  barrier geometry remain required.
- **Turning the funnel into ceremony.** One contract per candidate; one section per speed by
  default; addenda only for genuine prospective corrections or typed defects.
- **Optimizing programme metrics.** Counts diagnose the funnel; they are not quotas and cannot
  justify threshold movement.
- **Restating contract fields across artifacts or sections.** Later sections reference earlier
  freezes by heading and hash; a parallel copy is a divergence surface and voids nothing except
  the reader's trust — do not create one.
- **Minting a new terminal state.** Every terminal rejection maps to the ratified taxonomy (plus
  the pending fifth class) and names its §D3 register; a state invented mid-campaign is a
  taxonomy fork.
- **Silently re-scoring a frozen campaign under a re-pointed authority.** Void and refreeze under
  the new pin (§3.3 gate 3), never re-score.

---

## 12. Open decisions before ratification

1. What frozen historical sample sizes the Phase-A shadow route?
2. Does `Q-GATECAL-1` execute unchanged or require a successor aligned to this funnel's Vet gate?
3. Which Generate promotion-statistic (and discriminator) families receive synthetic calibration
   first?
4. What candidate-count and wall-clock budget bind the Phase-D pilot?
5. **The taxonomy-amendment ADR** — the fifth rejection class (`expression-failure`, with its
   binary add-back and `N_expr` default) and the two lossless mappings (§2.1) amend the ratified
   2026-06-14 and 2026-08-09 ADRs; that amending instrument must land at or before ratification
   of this spec, and `EXPRESSION-FAIL` is unusable until it does.
6. Whether a unified K band should ever replace per-lane bands (§2.4) — named, not proposed.

(v1's open decisions 1 and 6 — Vet-card owner format and funnel-state index — are answered by the
candidate contract, §2.6.)

Until these are decided and a ratifying instrument lands, this spec authorizes no campaign, data
pull, K spend, status change, Pine build, lifecycle change, or deployment action.
