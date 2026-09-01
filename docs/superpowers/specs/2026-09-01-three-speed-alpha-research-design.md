# Design — three-speed alpha research: Triage → Generate → Confirm

**Status:** `Proposed` — design specification only; no standing methodology, gate, K rule,
candidate status, or execution authority changes until a separate ratification decision.
**Date:** 2026-09-01
**Authors:** Joshua + Codex
**Scope:** tradeable-alpha research only. Structural, safety, governance, and measurement-method
questions continue to use ordinary INQHIORI without being forced through this funnel.
**Related:** [`INQHIORI canon`](../../methodology/inqhiori-canon.md) ·
[`strategy harvest`](../../methodology/strategy_harvest.md) ·
[`generate→confirm historical route`](../../methodology/avenue_a_generate_confirm.md) ·
[`Q-GATECAL-1`](../../briefs/Q-GATECAL-1-mechanism-gate-false-negative-rate.md) ·
[`objective composition map`](../../methodology/objective_composition_map.md)

---

## 1. Decision

Adopt a three-speed research funnel named exactly:

1. **Triage** — establish that the proposal is economically reachable, testable, and capable of
   changing a named trading decision.
2. **Generate** — run a bounded, selection-accounted exploration on an exploration panel and freeze
   one exact candidate expression.
3. **Confirm** — score that expression once on untouched data with the full decision-relevant
   validation battery.

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
  withdrawn after 0/4 campaigns reached Confirm; its promotion design was not productive;
- the mechanism-first gate's false-negative rate is explicitly unmeasured (`Q-GATECAL-1`), so the
  programme cannot yet claim that its low candidate supply is an optimal rejection frontier.

The answer is not to weaken Confirm. It is to make Triage cheaper and more economic, make Generate
productive but selection-honest, and reserve maximum rigor for the few candidates that earn it.

---

## 2. Common vocabulary and invariants

### 2.1 Candidate states

`candidate` is the generic object moving through the funnel. Its state is always explicit:

```text
PROPOSAL
  → TRIAGE-PASS
  → GENERATED
  → CONFIRMED
  → normal lifecycle / composition / deployment governance
```

Terminal and non-promoting states are:

```text
DROP · PARK · FALSIFIED · VOID · AMBIGUOUS-HOLD
```

`CONFIRMED` means only that the frozen trade expression survived Confirm. It is not synonymous with
`AUTHORIZED`, composition-compatible, deployable, armed, or live.

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
change restarts at Triage.

### 2.3 Evidence-isolation invariant

The three speeds use distinct evidence scopes:

| Speed | Permitted evidence | Forbidden evidence |
|---|---|---|
| Triage | prior literature, prior closed campaigns, instrument/venue facts, coarse non-outcome arithmetic | ranking fresh candidate P&L, reading the reserved Confirm panel |
| Generate | the frozen exploration panel and declared catalogue only | any Confirm observation, aggregate, timestamp-derived score, or post-result catalogue growth |
| Confirm | the frozen untouched Confirm panel, once | retuning, alternate windows, sibling rescue, threshold movement, second one-shot |

### 2.4 K and search accounting

- Triage uses `K=0` only while it performs no fresh outcome-bearing comparison. A return, P&L,
  direction, or predictive-score look opens K before the look.
- Generate declares `K_intrinsic` as every expression that could be selected from the frozen
  catalogue. Skipped-but-available expressions still count.
- Confirm declares `M`, the number of generated candidates allowed to touch Confirm. Default `M=1`.
  `M>1` requires a frozen multiplicity adjustment before Generate results are read.
- `K_banked` remains disclosure-only under standing doctrine; it is never silently added to the
  candidate's intrinsic search count.

### 2.5 No tradeability laundering

An observation that predicts range, volatility, state, or another diagnostic quantity is not
tradeable alpha until it names an executable decision bridge. “It may be useful as a filter” is not
a bridge. A valid bridge specifies:

```text
observable → frozen decision changed → executable expression → economic quantity improved
```

Conditioner-only observations may be retained in the mechanism library without advancing through
the alpha funnel.

---

## 3. Speed 1 — Triage

### 3.1 Purpose

Triage answers one question:

> **Is this proposal sufficiently reachable, decision-relevant, and testable to deserve an
> outcome-bearing Generate campaign?**

Triage is intentionally cheap. It rejects impossibilities and category errors before statistical
craftsmanship is spent on them.

### 3.2 Required Triage card

One compact artifact records the following fields:

| Field | Required content |
|---|---|
| Candidate ID | stable slug and version |
| Observation / source | what produced the proposal; no strength inflation |
| Decision bridge | exact decision that changes if the candidate works |
| Trade expression | instrument, side rule, entry clock, exit/hold, and initial risk geometry |
| Role | entry, exit, execution, sizing, conditioner, or portfolio-composition |
| Venue legality | target venue/account and known structural constraints |
| Data route | available source, span, fidelity, and estimated acquisition cost |
| Cost reachability | effect-scale or payoff-scale hurdle in the gate's own units |
| Payoff-shape reachability | whether the proposed win/loss shape can survive the target envelope |
| Power / cadence | expected independent N and minimum detectable effect |
| Economic prior | WHO/WHEN/WHY-survives/HOW-dies when known; otherwise explicitly `UNATTRIBUTED` |
| Prior-art consult | instrument cell, rejected registry, manifests, and adjacent candidates |
| Search declaration | proposed Generate catalogue, `K_intrinsic`, exploration window, Confirm reserve |
| Kill conditions | exact Triage failures and re-proposal bar |

### 3.3 Triage gates

All six must clear:

1. **Decision gate** — a named executable decision changes. Conditioner-only findings without a
   decision bridge route to the mechanism library, not Generate.
2. **Structural gate** — instrument, venue, session, data, latency, and product constraints do not
   make the expression illegal or impossible.
3. **Cost gate** — the conservative effect/payoff estimate can reach the standing cost-law hurdle
   in the units and price basis the eventual trade will face. Missing inputs route to a bounded
   measurement probe, never invented arithmetic.
4. **Shape gate** — the hypothesized win rate, payoff ratio, cadence, and barrier exposure occupy a
   feasible region for the target venue. A statistically plausible but venue-impossible shape dies.
5. **Power gate** — the reserved panels can discriminate a useful effect at the declared N. A test
   that can only return underpowered ambiguity does not open.
6. **Novelty gate** — the candidate is not a relabeled dead cell. A prior kill requires its recorded
   re-proposal bar to be satisfied by new evidence.

Economic attribution is disclosed at Triage but is not an absolute alpha-admission gate in this
proposed design. An `UNATTRIBUTED` candidate may pass only when it has a precise decision bridge and
accepts the stricter Confirm posture in §5.4. This is the design's deliberate relief valve pending
`Q-GATECAL-1`; it does not amend standing doctrine unless this design is separately ratified.

### 3.4 Triage outputs

| Output | Meaning | Next action |
|---|---|---|
| `TRIAGE-PASS` | all six gates clear | freeze and commit Generate charter |
| `DROP` | a permanent or currently binding impossibility | registry/ledger entry with re-proposal bar |
| `PARK` | one named missing input could change the answer | wake only when that input exists |
| `MECHANISM-ONLY` | observation is credible but has no decision bridge | retain finding; no alpha campaign |
| `VOID` | Triage consumed forbidden outcome evidence | rebuild with a fresh panel or stop |

### 3.5 Effort ceiling

Default Triage effort is **no more than 10% of the candidate's expected total research effort** and
normally one artifact. If Triage requires a bespoke model, extensive simulation, or multi-round
method-design review, the proposal has not yet shown that it belongs in the alpha funnel.

---

## 4. Speed 2 — Generate

### 4.1 Purpose

Generate answers:

> **Within a bounded, economically coherent catalogue, is there one exact expression that earns a
> single untouched confirmation attempt?**

Generate is allowed to search. It is not allowed to disguise searching as confirmation.

### 4.2 Generate charter — committed before any exploration score

The charter freezes:

- candidate family and Triage-card hash;
- exploration and Confirm windows, non-overlapping and immutable;
- full expression catalogue with stable IDs;
- `K_intrinsic` and Confirm budget `M`;
- data cleaning, roll, session, missing-bar, and duplicate rules;
- executable cost model;
- primary promotion statistic;
- minimum economic effect, not merely statistical significance;
- null/placebo and uncertainty method;
- selection rule when more than one expression clears;
- minimum cell N and `VOID-POWER` rule;
- one deterministic promotion threshold;
- output schema and seeds.

The promotion rule must be calibrated before the real exploration score is read. Calibration may use
synthetic nulls, planted effects, or prior closed panels that cannot enter the campaign. It must show
both false-promotion behavior and useful power. A promotion floor that produces no candidates under
economically meaningful planted effects is itself invalid; this explicitly corrects the historical
0/4-never-reached-Confirm failure rather than reviving that route unchanged.

### 4.3 Generate execution

1. Verify data hashes/provenance and the exploration/Confirm partition.
2. Open the K record before computing any outcome-bearing score.
3. Score every declared catalogue expression once on exploration.
4. Apply costs and the frozen promotion rule.
5. Select at most `M` expressions using the frozen ordering.
6. Freeze each promoted expression byte-faithfully: no parameter remains open.
7. Emit a compact result table for every expression, including failures.
8. Do not load, summarize, count, or inspect Confirm data.

Generate may use train/validation subdivision inside exploration when the charter freezes it, but
that subdivision does not become Confirm. Hyperparameters chosen inside exploration are part of the
selected expression and their available choices count toward selection accounting.

### 4.4 Generate outputs

| Output | Meaning | Next action |
|---|---|---|
| `GENERATED` | one or more expressions clear; no more than `M` selected | author Confirm prereg without looking at Confirm |
| `STOP-NONE` | no expression clears | close campaign; no threshold relaxation |
| `FALSIFIED-FAMILY` | frozen family-level criterion fails | close at the scope frozen by the charter |
| `VOID-SELECTION` | catalogue/window/K changed or Confirm was touched | no result; fresh campaign required |
| `VOID-POWER` | realized valid N misses the frozen floor | park or redesign prospectively |

### 4.5 Effort ceiling

Generate receives **approximately 20–30% of expected total candidate effort**. Its job is to select
and freeze—not to prove durability exhaustively. Expensive attribution models, full portfolio MC,
production Pine, rail wiring, and deployment packaging are forbidden here.

---

## 5. Speed 3 — Confirm

### 5.1 Purpose

Confirm answers:

> **Does the exact generated expression survive once, on untouched evidence, at sufficient economic
> and statistical strength to enter ordinary lifecycle and composition review?**

Confirm receives the majority of rigor because few candidates reach it and its errors are costly.

### 5.2 Confirm prereg — committed before any Confirm access

The prereg copies rather than re-describes:

- the exact generated expression and its artifact hash;
- the reserved Confirm window from the Generate charter;
- the primary net outcome statistic;
- the economic floor and verdict map;
- `K_intrinsic`, `M`, and the frozen multiplicity adjustment;
- the full decision-relevant validation battery;
- defect, missingness, power, and void handling;
- the one-shot execution command and seeds;
- downstream routing for every verdict.

If any Confirm metric was observed before this commit, the confirmation is void.

### 5.3 Mandatory Confirm battery

Every candidate receives:

1. **Provenance and implementation integrity** — source hashes, causal clocks, duplicate/missing-data
   rules, independent feature/label spot checks, and reproduction of the frozen expression.
2. **Net economic result** — commissions, spread, slippage, and venue-specific constraints applied
   at the relevant historical basis.
3. **Selection-aware inference** — declared K/M adjustment, uncertainty interval, and null/placebo
   appropriate to the statistic.
4. **Temporal durability** — frozen halves and regime/year slices with minimum N; no pooled rescue of
   a required failing slice.
5. **Execution fidelity** — bar/tick semantics, latency, session boundaries, order type, and
   Pine/Python parity when TradingView is part of the intended path.
6. **Payoff and tail geometry** — expectancy, MFE/MAE or relevant path statistics, drawdown, and
   candidate-level survivor scoring for the target venue.
7. **Composition relevance** — variance dominance, risk breadth, common-regime exposure, and joint
   MC when the proposed use is inside a book. Low correlation alone never clears composition.

Not every scientifically imaginable test belongs in Confirm. A test is included only if its result
can change the frozen verdict, candidate role, sizing ceiling, venue, composition, or monitoring
obligation.

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

### 5.5 Confirm outputs

| Output | Meaning | Next action |
|---|---|---|
| `CONFIRMED` | all frozen gates clear | lifecycle candidate intake; composition/deployment still separate |
| `FALSIFIED` | a valid gate fails | close exact expression; new expression restarts at Triage |
| `AMBIGUOUS-HOLD` | valid test lands in a predeclared uncertainty state | wake only on named information trigger |
| `VOID-*` | integrity, power, method, or execution failure prevents scoring | repair instrument; never call market negative |
| `CONFIRMED-NONDEPLOYABLE` | edge is real but venue/composition cannot use it | retain finding; no risk authorization |

No Confirm outcome authorizes arming, live spend, or autonomous promotion.

### 5.6 Effort allocation

Confirm receives the remaining **60–70% of candidate research effort**, conditional on the candidate
having earned it. This is where adversarial review, independent reproduction, expensive simulation,
and native-platform parity belong.

---

## 6. Gate handoffs

### 6.1 Triage → Generate handoff packet

Minimum contents:

- Triage card;
- exact six-gate verdict table;
- proposed catalogue and K;
- frozen exploration/Confirm window proposal;
- data cost estimate;
- named operator decision if spend is nonzero.

Generate may not silently repair an incomplete Triage card.

### 6.2 Generate → Confirm handoff packet

Minimum contents:

- Generate charter hash;
- full catalogue results;
- selected expression artifact and hash;
- K/M accounting;
- proof Confirm remained untouched;
- Confirm prereg draft containing no new feature or parameter choice.

### 6.3 Confirm → lifecycle handoff packet

Minimum contents:

- Confirm prereg and execution hashes;
- complete verdict battery;
- exact candidate implementation;
- intended role and venue;
- durability-source tag;
- composition requirements;
- monitoring observable and decay trigger design obligation;
- all caveats that survived confirmation.

Lifecycle, composition, capital allocation, Pine productionization, rail wiring, and arming retain
their own standing authority. The three-speed funnel does not collapse those layers.

---

## 7. INQHIORI mapping

The three speeds preserve the loop while preventing every observation from receiving maximum-cost
investigation immediately:

| INQHIORI work | Triage | Generate | Confirm |
|---|---|---|---|
| Identify / Notice | source observation and decision context | exploration-only data | frozen candidate + untouched panel |
| D-S-A | delete impossible expressions; compress to Triage card | freeze/index catalogue | freeze executable packet and audit hooks |
| Question | is this reachable and decision-relevant? | which bounded expression earns Confirm? | does the frozen expression survive? |
| Hypothesis | economic reachability hypothesis | promotion hypothesis | final executable hypothesis |
| Investigate | arithmetic and source verification | bounded exploration | one-shot full battery |
| Observe / Reflect | PASS/DROP/PARK | GENERATED/STOP/VOID | CONFIRMED/FALSIFIED/HOLD/VOID |
| Iterate | new evidence only | new campaign; fresh K/window | new expression restarts at Triage |

The canon's bounded-acceleration rule applies at every speed: tooling must be cheaper than the future
queries it enables. A reusable method may justify more investment than a one-off candidate, but its
reuse class and expected consumers must be named before construction.

---

## 8. Worked routing — Q-VOLREGIME-1

This example is diagnostic and does not change that Q's standing authorization.

### Triage read

The finding has strong presence evidence: elevated same-slot M15 volume predicts elevated next-bar
range within both trigger-range strata on MNQ and MYM. Its current role is `conditioner`; it does not
specify direction, favorable excursion, an entry, or a venue-native non-directional volatility trade.

Under this design it would therefore route:

```text
credible observation
  → Triage Decision gate asks for a precise trade bridge
  → absent bridge: MECHANISM-ONLY (retain; no alpha Generate)
```

Possible future bridges must be separate proposals, for example:

- one frozen existing directional signal whose MFE/MAE changes under the state;
- one execution choice whose realized cost changes under the state;
- one venue-legal volatility expression.

Each bridge starts at Triage with fresh K/window accounting. L5 attribution may still proceed as a
methodology investment if it names a reusable consumer class, but it is not represented as the
fastest path to tradeable alpha merely because L1–L4 are strong.

---

## 9. Programme metrics

The funnel is not successful merely because each artifact is internally correct. Report quarterly:

| Metric | Purpose |
|---|---|
| Proposals entering Triage | observation supply |
| Triage PASS/DROP/PARK/MECHANISM-ONLY counts | front-door selectivity |
| Median time and research cost to Triage disposition | cheap-kill performance |
| Generate campaigns and catalogue K | search breadth actually paid |
| Fraction producing `GENERATED` | promotion calibration |
| Confirm attempts and pass rate | exploration quality |
| Median time from proposal to Confirm verdict | research velocity |
| Confirmed candidates reaching lifecycle/composition | trade-expression relevance |
| Candidates surviving venue and composition | operational conversion |
| Defects found at each speed | placement of review effort |
| Sampled false-negative rate of early gates | over-correction risk |
| Research hours per decision-changing result | total programme efficiency |

Do not target a high Confirm pass rate. Target calibrated flow: enough candidates reach Confirm to
learn, while untouched Confirm remains difficult to pass. Promotion-rate targets must be set by a
separate calibration exercise, not inferred post hoc from the first cohort.

---

## 10. Adoption plan and required calibration

This design must not become standing doctrine from prose approval alone.

### Phase A — historical shadow routing (`K=0`)

Apply Triage retrospectively to a frozen sample of closed candidates without changing their recorded
verdicts. The sample must include:

- cost-law kills;
- power/cadence kills;
- evidence/direction kills;
- the ORB-MNQ survivor;
- at least one later-discovered implementation defect;
- conditioner-only findings such as Q-VOLREGIME-1.

Measure whether Triage would have:

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

Before the first live campaign, validate the promotion rule family on synthetic nulls and planted
economically meaningful effects. Freeze acceptable false-promotion and power bands prospectively.
The old 0/4 route is a negative control: a floor that cannot promote realistic planted effects is not
“rigorous”; it is nonfunctional.

### Phase D — bounded pilot

Run the first three-speed cohort under a predeclared candidate count, time budget, and no-mid-pilot
rule changes. At cohort close, compare funnel metrics with the historical baseline. Ratification or
amendment follows; no silent extension.

---

## 11. Forbidden moves

- **Weakening Confirm to improve throughput.** Throughput is repaired in Triage/Generate; Confirm
  remains untouched and one-shot.
- **Calling Triage PASS evidence of alpha.** It means only that testing is worth its cost.
- **Running outcome-bearing “Triage arithmetic” at K=0.** Any fresh return/predictive look opens K.
- **Treating a mechanism story as a substitute for net expectancy.** WHO/WHY improves a prior; it
  does not pay spread or commission.
- **Treating net expectancy as proof of attribution.** Predictive evidence and causal attribution
  remain typed separately.
- **Letting Generate inspect Confirm coverage or aggregates.** Even knowing which period “looks
  complete” after reservation can influence selection.
- **Moving a promotion floor after 0 candidates.** Calibrate before the campaign; a dead campaign
  closes.
- **Rescuing a failed Confirm with a sibling, filter, alternate exit, or new instrument.** Every such
  expression restarts at Triage.
- **Building production Pine or rail code during Generate.** Productionization is earned only after
  Confirm and remains separately governed.
- **Using low correlation as composition admission.** Risk breadth, variance dominance, and joint
  barrier geometry remain required.
- **Turning the funnel into ceremony.** One artifact per speed by default; addenda only for genuine
  prospective corrections or typed defects.
- **Optimizing programme metrics.** Counts diagnose the funnel; they are not quotas and cannot justify
  threshold movement.

---

## 12. Open decisions before ratification

1. Which existing artifact format becomes the Triage card owner: a new compact template or a
   shortened Pre-Q subtype?
2. What frozen historical sample sizes the Phase-A shadow route?
3. Does `Q-GATECAL-1` execute unchanged or require a successor aligned to this funnel's Triage gate?
4. Which Generate promotion-statistic families receive synthetic calibration first?
5. What candidate-count and wall-clock budget bind the Phase-D pilot?
6. Which single index owns funnel state without creating a second candidate registry?

Until these are decided and a ratifying instrument lands, this spec authorizes no campaign, data
pull, K spend, status change, Pine build, lifecycle change, or deployment action.
