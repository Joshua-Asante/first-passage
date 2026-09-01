# Design — three-speed alpha research: Vet → Generate → Confirm (v3, corrected against the ratified 2026-08-30 owners)

**Status:** `Proposed` — design specification only; no standing methodology, gate, K rule,
candidate status, or execution authority changes until a separate ratification decision. Where
this spec touches ground the six 2026-08-30 ADRs own, those ADRs are **already `Accepted` and
govern today** — this spec cites them and adds nothing to their scope.
**Date:** 2026-09-01 (v3)
**Authors:** Joshua + Codex (v1) · Claude Code (v2 reconciliation, v3 correction)
**Scope:** tradeable-alpha research only. Structural, safety, governance, and measurement-method
questions continue to use ordinary INQHIORI without being forced through this funnel.
**Related — ratified owners this spec composes with (all `Accepted` 2026-08-30):**
[`candidate-contract`](../../adr/2026-08-30-candidate-contract.md) ·
[`terminal-taxonomy`](../../adr/2026-08-30-terminal-taxonomy.md) ·
[`evaluation-order`](../../adr/2026-08-30-evaluation-order.md) ·
[`tradeable-reachable-gate`](../../adr/2026-08-30-tradeable-reachable-gate.md) ·
[`operator-approvals-campaign-envelope`](../../adr/2026-08-30-operator-approvals-campaign-envelope.md) ·
[`channel-liveness-gate`](../../adr/2026-08-30-channel-liveness-gate.md)
**Related — context:** [`INQHIORI canon`](../../methodology/inqhiori-canon.md) ·
[`strategy harvest`](../../methodology/strategy_harvest.md) ·
[`generate→confirm historical route`](../../methodology/avenue_a_generate_confirm.md) ·
[`Q-GATECAL-1`](../../briefs/Q-GATECAL-1-mechanism-gate-false-negative-rate.md) ·
[`objective composition map`](../../methodology/objective_composition_map.md) ·
[`generate/evaluate tensions note`](../../notes/2026-08-30-generate-evaluate-tensions.md)

## Review — lineage and why v3 exists

**v1** (PR #246/#247) proposed the three-speed funnel. **v2** (this PR, first commit) reconciled
it with the [tensions note](../../notes/2026-08-30-generate-evaluate-tensions.md) — but was
authored without enumerating `docs/adr/2026-08-30-*`: the note's recommendations had **already
been ratified the same day as six Accepted ADRs**, and v2 restated (and in places contradicted)
standing doctrine it believed was still proposed. The miss was v2's own amendment-first sweep —
it searched for funnel vocabulary, not for the note's ratified owners. Codex's review of this PR
caught it (eight findings, plus four more in the operator-relayed meta-review).

**v3's correction, finding by finding:**

1. **Contract cardinality** — fixed: one contract per generation-open campaign and fixed trade
   template; selected cells are hash-pinned sub-entries (cites `candidate-contract` §2 verbatim
   intent; v2's "one contract per candidate" wording is gone).
2. **Confirm truth table** — fixed: the `terminal-taxonomy` table is cited whole, including the
   branch v2 left undefined (discriminator clean-fail + payoff pass → `MARKET-NULL` regardless).
3. **`EXPRESSION-FAIL` "pending"** — fixed: it is ratified, with `N_expr` default 2; v2's open
   decision 5 is deleted.
4. **Universal channel-liveness default** — fixed: no funnel-imposed number; each channel's own
   declared ceiling governs (`channel-liveness-gate` §2 forbids re-deriving calibrated bounds in
   reconciliation).
5. **No-counterparty deferred-cost exception** — fixed: preserved explicitly in the Vet cost
   gate; it does not generalize.
6. **Confirm reservation before any shape-extraction probe** — fixed: the reservation is an
   early commit on the draft contract, before the probe reads any data (`evaluation-order` step
   2; v2 reserved at charter freeze, too late).
7. **Probe-tranche accounting** — fixed: realized probe spend and K become an already-spent
   sub-line inside the inclusive campaign ceiling, never "subsumed by citation"
   (`operator-approvals-campaign-envelope` §2).
8. **`FALSIFIED-FAMILY` typed as `MARKET-NULL`** — fixed: Generate-stage closes are process
   dispositions; `MARKET-NULL` is reserved for a powered, untouched-confirm discriminator
   failure.
- **(A)** `AMBIGUOUS-HOLD` removed from the Confirm verdict table — the confirm-phase evidence
  vocabulary is closed at four; a hosting Q may still close `AMBIGUOUS-HOLD` at the Q layer.
- **(B)** Venue change no longer creates a new candidate — a venue retarget of a `CONFIRMED`
  candidate is an edition-axis event; only a changed trade expression opens a new contract.
- **(C)** Venue survivor scoring removed from the Confirm battery — bust/pass MC and edition
  clearance run post-`CONFIRMED` (`evaluation-order` step 10).
- **(D)** The pilot budget is no longer wall-clock-denominated.

v1's surviving contributions: the three-speed vocabulary and speed boundaries, the six-gate Vet
front door, the promotion-floor calibration requirement, the effort-percentage guidance, the
worked Q-VOLREGIME-1 routing, and the Phase A–D adoption plan. v2's surviving contribution: the
single-artifact object model and pinned-authority delegation — which turned out to be the
ratified owners' design; v3 keeps the composition and drops the restatement.

---

## 1. Decision

Adopt a three-speed vocabulary over the already-ratified candidate pipeline:

1. **Vet** — establish that the proposal is economically reachable, testable, and capable of
   changing a named trading decision, before a contract opens.
2. **Generate** — run the bounded, selection-accounted exploration the frozen contract declares.
3. **Confirm** — score the selected expression once on untouched data.

The pipeline itself — contract, ordering, gates, envelope, verdicts — is owned by the six
2026-08-30 ADRs and is **not re-decided here**. What this spec adds, and what ratifying it would
newly bind:

- the **three-speed vocabulary** and the speed-boundary map onto the ratified pipeline (§7);
- the **six-gate Vet front door** as the named discipline for what happens *before* a contract
  opens (§3) — the ratified owners begin at the contract; Vet is the funnel's cheap pre-contract
  kill layer;
- the **promotion-floor calibration requirement** (§4.2) — a Generate promotion rule must
  demonstrate false-promotion behavior *and* useful power on synthetic nulls and planted
  economically meaningful effects before the real exploration score is read;
- the **`UNATTRIBUTED` relief valve** (§3.3, non-HARV lanes, pending `Q-GATECAL-1`);
- the **effort-percentage guidance** and the **Phase A–D adoption plan** (§10).

The governing principle is unchanged from v1:

> **A candidate earns rigor by surviving cheaper evidence. Rigor increases as the candidate set
> shrinks. No candidate reaches an expensive gate merely because the preceding finding is
> scientifically interesting.**

This is an escalation wrapper around INQHIORI, not a replacement for it.

### 1.1 Why this design exists

The estate is strong at falsification, data-defect discovery, selection accounting, cost realism,
and portfolio safety. It is weaker at converting observations into executable candidates at useful
throughput. Two facts motivate a redesign rather than a relaxation:

- the historical generate→confirm route preserved untouched confirmation correctly, but was
  withdrawn after 0/4 campaigns reached Confirm; its promotion design was not productive — the
  generated statistic was never economically connected to a tradeable object, and the channel's
  own success falsifier depended on a state the channel could not reach;
- the mechanism-first gate's false-negative rate is explicitly unmeasured (`Q-GATECAL-1`), so the
  programme cannot yet claim that its low candidate supply is an optimal rejection frontier.

The answer is not to weaken Confirm. It is to make the pre-contract layer cheaper and more
economic, make exploration productive but selection-honest, and reserve maximum rigor for the few
candidates that earn it. The 2026-08-30 ADRs built the contract-to-verdict machinery; this spec
names the speeds, adds the pre-contract front door, and requires the promotion floor to be proven
functional before it is trusted.

---

## 2. Vocabulary and invariants

### 2.1 States and verdicts — cited, not minted

**Promoting path:**

```text
PROPOSAL → VET-PASS → (contract opens) → GENERATED → CONFIRMED → lifecycle / composition / deployment governance
```

**Confirm-phase evidence verdicts** are the closed vocabulary of
[`terminal-taxonomy`](../../adr/2026-08-30-terminal-taxonomy.md) §2 — exactly four:
`CONFIRMED` · `MARKET-NULL` · `EXPRESSION-FAIL` · `EVIDENCE-VOID`, adjudicated by the
contract-frozen mechanism discriminator per that ADR's truth table (§5.4 below). The **edition
axis** (placement-clear / `VENUE-FAIL(edition)`, `CONFIRMED` candidates only) and all registry
routing are that ADR's, unmodified. `AMBIGUOUS-HOLD` is **not** a confirm-phase verdict; a Q
hosting a funnel campaign may still close `AMBIGUOUS-HOLD` at the Q layer under its own
pre-registered gate.

**Pre-contract (Vet) outputs** are this spec's own process states: `VET-PASS` · `DROP` · `PARK` ·
`MECHANISM-ONLY` · `VOID` (§3.4). A `DROP` whose failed limb is economic routes its registry
entry per `terminal-taxonomy`'s pre-explore mapping (venue/cost-constraint, "priors-derived, no
mechanism test run"); other `DROP`s follow standing §D3 conventions.

**Generate-stage closes** are process dispositions, never evidence verdicts (§4.4).

### 2.2 Monotone-rigor invariant

Every promotion must satisfy all gates at its current speed. Later evidence cannot retroactively
waive an earlier failed gate. A later-stage failure cannot be rescued by returning to an earlier
stage and redefining the candidate.

Any change to the **trade expression** — entry or side rule, feature definition or threshold,
holding period or exit, stop/target/sizing logic, instrument, conditioning state, or a data
window chosen because of a seen result — opens a **new contract** (a genuinely distinct template
is never a new cell of an existing one — `candidate-contract` §2), and a post-`EXPRESSION-FAIL`
successor additionally rides the ratified `N_expr` ladder (default 2, mechanism-ledger-keyed —
`terminal-taxonomy` §2).

**Venue is the exception, by design:** a venue retarget of a `CONFIRMED` candidate is an
edition-axis event (`evaluation-order` step 10 — new cost and firm-geometry scoring, possibly a
new edition), never automatically a new candidate. A new contract is required only if the new
venue forces the expression itself to change (session semantics, execution clock, order type).

A mechanical defect repair may resume at the affected speed only when the repair restores the
already-frozen intended expression and the contaminated result is discarded. A semantic or
economic change restarts at Vet.

### 2.3 Evidence-isolation invariant

The three speeds use distinct evidence scopes:

| Speed | Permitted evidence | Forbidden evidence |
|---|---|---|
| Vet | prior literature, prior closed campaigns, instrument/venue facts, coarse non-outcome arithmetic | ranking fresh candidate P&L, reading the reserved Confirm panel |
| Generate | the frozen exploration panel and declared catalogue only | any Confirm observation, aggregate, timestamp-derived score, or post-result catalogue growth |
| Confirm | the frozen untouched Confirm panel, once | retuning, alternate windows, sibling rescue, threshold movement, second one-shot |

### 2.4 K, M, and spend — cited

- Vet uses `K=0` only while it performs no fresh outcome-bearing comparison. A return, P&L,
  direction, or predictive-score look opens K before the look.
- From contract open onward, K/α/window binding, the multiplicity configuration (`α`, `M`,
  Bonferroni-or-Holm procedure identity), the campaign envelope, and probe-tranche accounting
  (realized probe spend and K as an already-spent sub-line inside the inclusive campaign
  ceiling; a probe that kills its candidate stands alone as its own closed spend) are owned by
  [`candidate-contract`](../../adr/2026-08-30-candidate-contract.md) and
  [`operator-approvals-campaign-envelope`](../../adr/2026-08-30-operator-approvals-campaign-envelope.md) —
  cited, not restated.
- `K_banked` remains disclosure-only under standing doctrine.
- **Lane rules ride along.** A harvest-lane candidate remains bound by its lane's own Clause-K
  screen (`K_eff ≤ 3` — [`strategy_harvest.md`](../../methodology/strategy_harvest.md) Clause K);
  that band is lane-scoped, not a funnel ceiling. Whether a unified K band should ever replace
  per-lane bands is a separate ratification question (§12).

### 2.5 No tradeability laundering — cited

A conditioner, correlation, or response statistic with no defined trade is a diagnostic, not a
candidate. The hard form of this rule is already a ratified contract-admission gate: a candidate
missing any of signal, entry clock, stop, exit/target, holding horizon, or costed payoff unit
"is not yet a candidate and cannot be admitted" (`candidate-contract` §2). Vet's Decision gate
(§3.3) applies the same test earlier and cheaper, as:

```text
observable → frozen decision changed → executable expression → economic quantity improved
```

Conditioner-only observations may be retained in the mechanism library without advancing.

### 2.6 The candidate contract — cited

One contract per generation-open campaign and fixed trade template, opened once, before Explore;
up to `M` selected cells as hash-pinned sub-entries of its append-only selection freeze; no
separate seed-manifest, G0, or preregistration document may restate its fields
(`candidate-contract` §2, as amended by `tradeable-reachable-gate`, `evaluation-order`, and
`operator-approvals-campaign-envelope`). The Vet card (§3.2) is the funnel's pre-contract
artifact; on `VET-PASS` its content seeds the contract's founding freeze **without forking the
schema** — where the ratified contract schema defines a field, the contract's definition governs
and the card simply carries the draft value forward.

---

## 3. Speed 1 — Vet

### 3.1 Purpose

Vet answers one question, before any contract opens and at `K=0`:

> **Is this proposal sufficiently reachable, decision-relevant, and testable to deserve a
> generation-open campaign?**

Vet is intentionally cheap. It rejects impossibilities and category errors before statistical
craftsmanship is spent on them. The ratified pipeline begins at the contract; Vet is the funnel's
front door in the space before it.

### 3.2 Required Vet card

One compact artifact records:

| Field | Required content |
|---|---|
| Candidate ID | stable slug and version |
| Observation / source | what produced the proposal; no strength inflation |
| Decision bridge | exact decision that changes if the candidate works |
| Trade expression (draft) | instrument, side rule, entry clock, exit/hold, initial risk geometry — the complete-object fields the contract's admission gate will require |
| Role | entry, exit, execution, sizing, conditioner, or portfolio-composition |
| Venue legality | target venue/account and known structural constraints |
| Mechanism discriminator (named) | the observable whose full adjudication rule the contract will freeze (`terminal-taxonomy` §2) |
| Data route | available source, span, fidelity, estimated acquisition cost |
| Cost reachability | per gate 3 below — pinned authority, or the named channel exception |
| Payoff-shape reachability | per gate 4 below |
| Power / cadence | expected independent N and minimum detectable effect |
| Economic prior | WHO/WHEN/WHY-survives/HOW-dies when known; otherwise explicitly `UNATTRIBUTED` |
| Prior-art consult | instrument cell, rejected registry (incl. any `N_expr` ledger row), manifests, adjacent candidates |
| Search declaration | proposed catalogue, `K_intrinsic`, exploration window, Confirm reserve proposal |
| Kill conditions | exact Vet failures and re-proposal bar |

### 3.3 Vet gates

All six must clear:

1. **Decision gate** — a named executable decision changes (§2.5). Conditioner-only findings
   route to the mechanism library, not to a contract.
2. **Structural gate** — instrument, venue, session, data, latency, and product constraints do
   not make the expression illegal or impossible. Where the candidate class is subject to the
   eval-mechanism-shape screen, this gate is discharged by `evaluation-order` step 1's
   class-level structural screening (EM0/EM3/EM4/EM5-N-SHAPE, pre-catalogue, pre-K, $0) — run
   here, cited there.
3. **Cost gate** — **delegated, never rederived**: the `TRADEABLE-REACHABLE` cost limb's pinned
   authority and void-and-refreeze rule
   ([`tradeable-reachable-gate`](../../adr/2026-08-30-tradeable-reachable-gate.md) §2) applied to
   the draft values, with the full gate re-run pre-Explore at its ratified position
   (`evaluation-order` step 5). **The no-counterparty-statistical/geometric channel's named
   exception is preserved exactly**: for that channel only, the cost limb is satisfied by citing
   the channel's own ratified deferred order, with its post-confirm cost-law check remaining the
   operative discipline; the exception does not generalize.
4. **Shape gate** — the hypothesized win rate, payoff ratio, cadence, and barrier exposure occupy
   a feasible region for the target venue's **measured** binding constraint. Shape inputs follow
   the ratified discipline (citable priors under harvest-Requirement-2 handling, or a declared
   pre-freeze extraction probe under its own approved probe envelope — `tradeable-reachable-gate`
   §2). **Ordering is the ratified one:** the Confirm-window reservation is committed on the
   draft contract **before** any probe reads data (`evaluation-order` step 2), so a probe can
   never influence which interval becomes the holdout.
5. **Power gate** — the reserved panels can discriminate a useful effect at the declared N. A
   test that can only return underpowered ambiguity does not open.
6. **Novelty gate** — the candidate is not a relabeled dead cell. A prior kill requires its
   recorded re-proposal bar satisfied by new evidence; a mechanism with an `EXPRESSION-FAIL`
   history requires its `N_expr` ledger row cited and its ordinal declared
   (`terminal-taxonomy` §2).

Economic attribution is disclosed at Vet but is not an absolute alpha-admission gate in this
proposed design — **for non-HARV lanes**. An `UNATTRIBUTED` candidate may pass only when it has a
precise decision bridge and accepts the stricter Confirm posture in §5.5. This is the design's
deliberate relief valve pending `Q-GATECAL-1` (Phase B, §10); it does not amend standing doctrine
unless this design is separately ratified. **HARV-lane candidates are carved out**: their lane's
hard pre-freeze attestation
([ratification](../../adr/2026-07-13-harv-discovery-lane-ratification.md) §2 as strengthened by
the [same-units supersession](../../adr/2026-07-16-harv-attestation-same-units-supersession.md))
continues to bind in full, unrelieved.

### 3.4 Vet outputs

| Output | Meaning | Next action |
|---|---|---|
| `VET-PASS` | all six gates clear | open the candidate contract (`candidate-contract` §2) |
| `DROP` | a permanent or currently binding impossibility | registry entry per §2.1's routing, with re-proposal bar |
| `PARK` | one named missing input could change the answer | wake only when that input exists |
| `MECHANISM-ONLY` | observation is credible but has no decision bridge | retain finding; no contract |
| `VOID` | Vet consumed forbidden outcome evidence | rebuild with a fresh panel or stop |

### 3.5 Effort ceiling

Default Vet effort is **no more than 10% of the candidate's expected total research effort** and
normally one artifact. If Vet requires a bespoke model, extensive simulation, or multi-round
method-design review, the proposal has not yet shown that it belongs in the alpha funnel.
(Percentages here and in §4.5/§5.6 are attention guidance; the binding spend control is the
campaign envelope — cited, §2.4.)

---

## 4. Speed 2 — Generate

### 4.1 Purpose

Generate answers:

> **Within the bounded, economically coherent catalogue the frozen contract declares, is there
> one exact expression that earns a single untouched confirmation attempt?**

Generate is allowed to search. It is not allowed to disguise searching as confirmation.

### 4.2 Contract freeze and the calibration requirement

The contract's founding freeze, the reservation commit, the pinned cost authority, the
discriminator's full adjudication rule, the multiplicity configuration and succession rule, the
campaign envelope, and the single operator GO that approves it are all owned by the ratified
schema (`candidate-contract` §2 plus its three Amends-in-part) — this spec adds no field and
restates none.

It adds one requirement at this boundary, the direct fix for the historical 0/4 failure:

**The promotion rule must be calibrated before the real exploration score is read.** Calibration
may use synthetic nulls, planted effects, or prior closed panels that cannot enter the campaign.
It must demonstrate both false-promotion behavior and useful power. A promotion floor that
produces no candidates under economically meaningful planted effects is itself invalid — a dead
floor is not "rigorous"; it is nonfunctional. The discriminator's adjudication rule is calibrated
the same way, in the same pass (§10 Phase C).

### 4.3 Generate execution — cited

Execution is `evaluation-order` step 6, whole: K-ledger bind before any exploration read; every
declared cell scored once; costs under the pinned model; at most the frozen `M` cells selected by
the frozen ordering; the append-only, hash-pinned **selection freeze** committed before any
holdout access. Exploration train/validation subdivision, if the contract froze it, never becomes
Confirm; hyperparameter choices count toward selection accounting.

### 4.4 Generate closes — process dispositions only

| Close | Meaning | Next action |
|---|---|---|
| `GENERATED` | ≥1 cell clears; ≤ `M` selected | proceed to Confirm entry (`evaluation-order` steps 7–8) |
| `STOP-NONE` | no cell clears the calibrated floor | campaign closes; no threshold relaxation; registry/board writes per the channel's standing conventions |
| `VOID-SELECTION` | catalogue/window/K changed, or Confirm was touched | no result; fresh campaign required |
| `VOID-POWER` | realized valid N misses the frozen floor | park or redesign prospectively |

No Generate-stage close is an evidence verdict. `MARKET-NULL` and `EXPRESSION-FAIL` exist only at
Confirm, discriminator-adjudicated (`terminal-taxonomy` §2) — an exploration-stage family failure
is a `STOP-NONE`-class process close at the scope the contract froze, and any registry entry it
owes follows the standing per-channel and §D3 conventions, never the confirm vocabulary.

### 4.5 Effort ceiling

Generate receives **approximately 20–30% of expected total candidate effort** (guidance). Its job
is to select and freeze — not to prove durability exhaustively. Expensive attribution models,
full portfolio MC, production Pine, rail wiring, and deployment packaging are forbidden here.

---

## 5. Speed 3 — Confirm

### 5.1 Purpose

Confirm answers:

> **Does the exact generated expression survive once, on untouched evidence, at sufficient
> economic and statistical strength to enter ordinary lifecycle and composition review?**

Confirm receives the majority of rigor because few candidates reach it and its errors are costly.

### 5.2 Entry — cited

Confirm entry is `evaluation-order` steps 7–8, whole: the contract-integrity check first
(integrity-only — a mismatch voids or stops the attempt, never a rejection), then the zero-K role
state-drift re-check against the current compliance snapshot (`ROLE-BLOCKED` is a fit-for-scope
disposition, never a candidate rejection; slots follow the contract's frozen succession rule;
forfeited or unfilled slots enter Holm adjudication at the frozen placeholder p = 1).

### 5.3 The battery — implementation adjudication only

One atomic step (`evaluation-order` step 9): the confirm statistic and the frozen minimum
temporal-consistency battery run together, and a single verdict is emitted only once both have
run. The battery adjudicates the **frozen expression**: provenance and implementation integrity;
net economic result under the pinned cost model; selection-aware inference under the frozen
K/M/procedure; temporal durability (no pooled rescue of a required failing slice); execution
fidelity (bar/tick semantics, latency, session boundaries, order type, Pine/Python parity where
TradingView is on the path); payoff and tail geometry **of the expression**; and the frozen
mechanism discriminator.

**Not in the battery:** venue bust/pass survivor MC, composition, activity, drawdown, and sizing
— those are `evaluation-order` step 10, run post-`CONFIRMED` only (v2 wrongly placed venue
survivor scoring inside the battery). A test is included only if its result can change the frozen
verdict; everything venue-fit-shaped waits for the edition axis.

### 5.4 Verdicts — cited truth table

Per [`terminal-taxonomy`](../../adr/2026-08-30-terminal-taxonomy.md) §2, exactly four, no fifth
combination undefined:

| Discriminator | Payoff/temporal | Verdict |
|---|---|---|
| Pass | Pass | `CONFIRMED` |
| Pass | Fail | `EXPRESSION-FAIL` (ratified fifth WHY-rejected class; `N_expr` ladder, default 2) |
| Clean fail (powered, adjudicated no) | Pass **or** fail | `MARKET-NULL` — a payoff pass without its mechanism is the exact spurious-selection shape this discipline exists to prevent |
| Cannot adjudicate (own coverage/power unmet) | any | `EVIDENCE-VOID` — attempt exhausted, never evidence against the candidate |

Registry routing, add-backs, the `N_expr` ledger mechanics, and the ladder's terminus (migration
to venue/cost-constraint only when cost/geometry limbs actually fired) are that ADR's, cited.

No Confirm outcome authorizes arming, live spend, or autonomous promotion.

### 5.5 Attribution recording

Causal/mechanism attribution is **not** a universal Confirm limb. It becomes mandatory when the
candidate's claimed durability depends on a specific counterparty constraint; when the feature is
a proxy whose confounding could reverse the executable decision; when the result would determine
monitoring or capacity limits; or when attribution machinery is intended for reuse across a
declared class. Otherwise Confirm tests incremental out-of-sample decision value and records
attribution as `MECHANISM`, `EVIDENCE-ROBUST`, or `SURVIVAL-ONLY/UNATTRIBUTED`; unattributed
confirmed candidates inherit the standing tighter lifecycle treatment. (The discriminator of
§5.4 is the mechanism-level *predictive* observable, frozen for verdict adjudication — not a
causal-attribution requirement; the two remain typed separately.)

### 5.6 Post-verdict — cited

`evaluation-order` step 10, whole: portfolio and venue fit last, `CONFIRMED` candidates only,
landing on the edition axis (placement-clear / `VENUE-FAIL(edition)`). A failure there rejects
the placement, never the confirmed status, and is never evidence the market effect is false.
Confirm effort guidance: **60–70%** of candidate research effort, conditional on the candidate
having earned it — adversarial review, independent reproduction, expensive simulation, and
native-platform parity belong here.

---

## 6. Handoffs

There are no handoff packets: the contract's own sections and appendices are the handoffs
(`candidate-contract` §2). The one boundary artifact this funnel still owes is the
**Confirm → lifecycle appendix** for a `CONFIRMED` candidate — intended role and venue,
durability-source tag (§5.5), the step-10 edition-axis outcome, the monitoring observable and
decay-trigger design obligation, and every caveat that survived confirmation. Lifecycle,
composition, capital allocation, Pine productionization, rail wiring, and arming retain their own
standing authority; the funnel collapses none of those layers.

---

## 7. Speed-boundary map, INQHIORI mapping, and vocabulary crosswalk

**Speeds onto the ratified pipeline** ([`evaluation-order`](../../adr/2026-08-30-evaluation-order.md) §2):

| Speed | Pipeline steps | Boundary events |
|---|---|---|
| Vet | pre-contract + step 1 (class-level structural screening); draft-contract reservation commit (step 2, first half) | `VET-PASS` → contract opens |
| Generate | steps 2–6 (shape priors/probe · attestation · contract freeze · `TRADEABLE-REACHABLE` · K-bind + Explore + selection freeze) | selection freeze → Confirm entry |
| Confirm | steps 7–9 (integrity · role drift · atomic confirm) | verdict → step 10 (post-verdict venue/composition) |

**INQHIORI mapping:**

| INQHIORI work | Vet | Generate | Confirm |
|---|---|---|---|
| Identify / Notice | source observation and decision context | exploration-only data | frozen candidate + untouched panel |
| D-S-A | delete impossible expressions; compress to Vet card | freeze/index catalogue | freeze executable packet and audit hooks |
| Question | is this reachable and decision-relevant? | which bounded expression earns Confirm? | does the frozen expression survive? |
| Hypothesis | economic reachability hypothesis | promotion hypothesis | final executable hypothesis |
| Investigate | arithmetic and source verification | bounded exploration | one-shot full battery |
| Observe / Reflect | PASS/DROP/PARK/MECHANISM-ONLY | GENERATED/STOP/VOID | the four verdicts |
| Iterate | new evidence only | new campaign; fresh K/window | new expression = new contract, on the `N_expr` ladder |

**Crosswalk to the tensions note's phrasing:** the note's "lean generate phase" steps 1–6 ≈ Vet
plus contract freeze; its step 7 ≈ Generate execution; its step 8 ≈ the channel-liveness gate
(now its own ratified ADR); its "lean evaluate phase" ≈ Confirm entry, battery, verdicts, and
step 10. The note's "generate/evaluate" is never a synonym for this spec's Generate speed.

The canon's bounded-acceleration rule applies at every speed: tooling must be cheaper than the
future queries it enables, and its reuse class and expected consumers must be named before
construction.

---

## 8. Worked routing — Q-VOLREGIME-1

This example is diagnostic and does not change that Q's standing authorization.

### Vet read

The finding has strong presence evidence: elevated same-slot M15 volume predicts elevated next-bar
range within both trigger-range strata on MNQ and MYM. Its current role is `conditioner`; it does
not specify direction, favorable excursion, an entry, or a venue-native non-directional volatility
trade.

Under this design it would therefore route:

```text
credible observation
  → Vet Decision gate asks for a precise trade bridge
  → absent bridge: MECHANISM-ONLY (retain; no contract)
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

## 9. Programme metrics

The funnel is not successful merely because each artifact is internally correct. Report quarterly:

| Metric | Purpose |
|---|---|
| Proposals entering Vet | observation supply |
| Vet PASS/DROP/PARK/MECHANISM-ONLY counts | front-door selectivity |
| Median time and research cost to Vet disposition | cheap-kill performance |
| Contracts opened and catalogue K | search breadth actually paid |
| Fraction producing `GENERATED` | promotion calibration |
| Confirm attempts and pass rate | exploration quality |
| Median time from proposal to Confirm verdict | research velocity |
| Confirmed candidates reaching lifecycle/composition | trade-expression relevance |
| Candidates surviving venue and composition | operational conversion |
| Defects found at each speed | placement of review effort |
| Sampled false-negative rate of early gates | over-correction risk |
| Research hours per decision-changing result | total programme efficiency |
| **Each channel's position against its own declared liveness ceiling** | channel liveness — per [`channel-liveness-gate`](../../adr/2026-08-30-channel-liveness-gate.md): the ceiling, yield unit, and consequence are the channel charter's own declarations; this funnel imposes **no universal number** and reports against each channel's clause as declared |

Do not target a high Confirm pass rate. Target calibrated flow: enough candidates reach Confirm
to learn, while untouched Confirm remains difficult to pass. Promotion-rate targets must be set
by a separate calibration exercise, not inferred post hoc from the first cohort.

---

## 10. Adoption plan and required calibration

This design must not become standing doctrine from prose approval alone. (The six 2026-08-30
ADRs are already Accepted and are not gated on this plan — the phases below validate what this
spec itself adds.)

### Phase A — historical shadow routing (`K=0`)

Apply Vet retrospectively to a frozen sample of closed candidates without changing their recorded
verdicts. The sample must include cost-law kills; power/cadence kills; evidence/direction kills;
the ORB-MNQ survivor; at least one later-discovered implementation defect; and conditioner-only
findings such as Q-VOLREGIME-1. Measure whether Vet would have killed known impossibilities
earlier, preserved the known survivor, routed scientific-but-nontradeable findings out of the
alpha queue, and exposed ambiguous mechanism-gate cases rather than silently dropping them. This
is process validation, not a re-verdict of any historical candidate.

### Phase B — gate false-negative read

Read `Q-GATECAL-1` or an explicitly superseding calibration before ratifying the proposed
`UNATTRIBUTED` relief valve. A nonzero false-negative finding informs the design; it does not
automatically abolish mechanism grounding.

### Phase C — promotion and discriminator calibration

Before the first live campaign, validate the promotion rule family — and the mechanism
discriminators' adjudication-rule families alongside it — on synthetic nulls and planted
economically meaningful effects. Freeze acceptable false-promotion and power bands prospectively.
The old 0/4 route is the negative control.

### Phase D — bounded pilot

Run the first three-speed cohort under a predeclared **candidate count, K ceiling, data/spend
ceiling, and iteration count, with a calendar review trigger and a no-mid-pilot-rule-change
condition** (no wall-clock-denominated budget — neither client meters wall-clock reliably). At
cohort close, compare funnel metrics with the historical baseline. Ratification or amendment
follows; no silent extension.

---

## 11. Forbidden moves

- **Weakening Confirm to improve throughput.** Throughput is repaired at Vet/Generate; Confirm
  remains untouched and one-shot.
- **Calling `VET-PASS` evidence of alpha.** It means only that testing is worth its cost.
- **Running outcome-bearing "Vet arithmetic" at K=0.** Any fresh return/predictive look opens K.
- **Treating a mechanism story as a substitute for net expectancy, or net expectancy as proof of
  attribution.** The two remain typed separately.
- **Letting Generate inspect Confirm coverage or aggregates.** Even knowing which period "looks
  complete" after reservation can influence selection.
- **Moving a promotion floor after 0 candidates.** Calibrate before the campaign (§4.2); a dead
  campaign closes.
- **Recording a Generate-stage close in Confirm vocabulary.** `MARKET-NULL`/`EXPRESSION-FAIL`
  exist only at a powered, untouched confirm (§4.4).
- **Rescuing a failed Confirm with a sibling, filter, alternate exit, or new instrument.** Every
  such expression is a new contract at Vet, on the `N_expr` ladder.
- **Building production Pine or rail code during Generate.** Productionization is earned only
  after Confirm and remains separately governed.
- **Using low correlation as composition admission.** Risk breadth, variance dominance, and joint
  barrier geometry remain required at step 10.
- **Turning the funnel into ceremony.** One Vet artifact, one contract; addenda only for genuine
  prospective corrections or typed defects.
- **Optimizing programme metrics.** Counts diagnose the funnel; they are not quotas and cannot
  justify threshold movement.
- **Restating a ratified owner's content.** This spec cites the six 2026-08-30 ADRs; any future
  amendment of their ground lands on them, never here. A restatement that drifts is a
  source-of-truth fracture.

---

## 12. Open decisions before ratification

1. What frozen historical sample sizes the Phase-A shadow route?
2. Does `Q-GATECAL-1` execute unchanged or require a successor aligned to this funnel's Vet gate?
3. Which promotion-statistic (and discriminator) families receive synthetic calibration first?
4. What candidate count, K ceiling, spend ceiling, and iteration count bind the Phase-D pilot?
5. Whether a unified K band should ever replace per-lane bands (§2.4) — named, not proposed.
6. Whether ratification of this spec lands as its own thin ADR (the vocabulary, the Vet front
   door, the calibration requirement, the relief valve) or folds into a future amendment of one
   of the six owners.

Until these are decided and a ratifying instrument lands, this spec authorizes no campaign, data
pull, K spend, status change, Pine build, lifecycle change, or deployment action — while the six
2026-08-30 ADRs it composes with remain in force on their own authority, unaffected by this
spec's status.
