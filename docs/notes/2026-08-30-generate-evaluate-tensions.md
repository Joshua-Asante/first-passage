# Generate/evaluate tensions in the strategy lifecycle

**Date:** 2026-08-30  
**Scope:** Interpretive note. This records tensions already visible in the
ratified methodology; it changes no gate, threshold, lifecycle state, venue
binding, or deployment authority.

## Executive finding

The repository does not have one simple disagreement between "generate" and
"evaluate." It has a set of deliberate safeguards that become counterforces
when combined. Generation needs breadth, iteration, inexpensive data, and a
reachable success path. Evaluation needs a small declared search, untouched
holdouts, venue-realistic economics, and asymmetric evidence. Those goals are
individually sensible, but the current design can make a discovery channel
honest yet unable to produce anything evaluable.

The Route B history is the clearest observed instance: its generate/confirm
firewall was statistically careful, but none of four campaigns reached the
confirm stage. The operator retired the route on its 0-for-4 lifetime record
and a citation-drift incident it had already caused, "regardless of the
un-tripped falsifier" (`docs/adr/2026-08-24-sourcing-phase-channel-retirement.md`
§1) — not because the falsifier fired. In retrospect, the promotion design
never targeted a tradeable object, so that falsifier could not have become
reachable even had the route continued; that is a design lesson the
retirement surfaced, not the retirement's stated cause.

## The tensions

### 1. Search breadth vs. multiplicity control

Generation benefits from examining many feature, horizon, side, and schema
combinations. Evaluation treats every available choice as selection: skipped
cells still count, the explored catalogue determines `K_intrinsic`, and a
multi-candidate confirm budget needs its own multiplicity adjustment. The
harvest intake then makes `K_intrinsic <= 3` the admissible band.

This is the central statistical tension: a catalogue large enough to discover
an unfamiliar structure can price itself out of evaluation before the
structure is tested. Reducing the catalogue preserves power and DSR
reachability, but transfers more discretion into the generator's choice of
which three ideas deserve to exist.

### 2. Iterative learning vs. the exploration/confirmation firewall

Feature engineering normally learns by plotting, revising a horizon, changing
a cleaning rule, and trying a sibling expression. The withdrawn Route B made
those moves new campaigns after G0: the catalogue and windows could not grow,
the confirm feature had to be copied byte-faithfully, and a confirm run allowed
no threshold sweep, alternate horizon, or sibling cell.

That firewall is the protection against holdout leakage and post-hoc stories.
It also makes the handoff brittle: a promising but slightly misspecified
generated object cannot be repaired inside evaluation. The system must choose
between an honest `STOP` and another K-bearing campaign, even when evaluation
has taught the researcher exactly how the object was misspecified.

### 3. Cheap/recent exploration data vs. independent, powered confirmation

Order-flow entitlements made recent exploration inexpensive, while deep
MBP/MBO history remained costly. But a reserved confirm slice must be both
untouched and large enough for the declared coverage/power rule. Splitting a
short, recent entitlement makes both halves thinner and often substitutes a
nearby temporal slice for genuine regime diversity.

Thus `$0` helps the spending constraint without solving the evidence-shape
constraint. The route explicitly recognized narrow-regime exploration and thin
confirm power, but its remedy (`VOID-POWER`, never stretch the window) protects
honesty by lowering throughput.

### 4. Predictive proxies vs. tradeable, venue-shaped objects

Generation can cheaply rank correlations, order-flow aggregates, or future
mid-return responses. Evaluation needs an executable entry/exit object whose
R-distribution clears round-trip costs, latency, stop integrity, sizing, drawdown,
activity, and firm-law constraints. A statistically interesting proxy need not
map to such an object.

This was not hypothetical in Route B. The four campaigns used a promotion floor
around a correlation target whose implied move was much smaller than the
round-trip cost and the required per-trade move. Their G0 EM1/EM2 attestations
were `SHAPE-UNSCREENABLE` — a correlation-on-mid-return target is not itself a
tradeable stop/target object — but that is a pre-registration attestation, not
each campaign's disposition: the four closures actually recorded
`VOID-COVERAGE`, `FALSIFIED`, `FALSIFIED`, and `AMBIGUOUS-HOLD`. No confirm
stages ran in any of them. The later diagnosis required any
future catalogue to start from a tradeable first-passage/stop-target object and
derive its promotion floor from cost arithmetic. In other words, evaluation
requirements must partially constrain generation up front, or the interface is
not reachable.

### 5. General alpha evidence vs. firm-specific feasibility

The research process seeks durable futures effects, but the target is not a
generic futures portfolio. Evaluation is bound to an automation-friendly prop
venue: weekly activity, survivor scoring on the honest clock, positive net edge
with CI and DSR-at-K, independence/stop/session legality, and candidate-derived
sizing. The standing radar also performs a venue-shape pre-check before a seed
is manifested.

This creates a real classification tension. A generated hypothesis may be a
valid market effect yet be rejected as an implementation for the current firm;
conversely, optimizing generation too tightly around one firm's feasibility
region risks producing venue-specific artifacts rather than durable alpha. The
repository partly manages this with a separate venue-binding axis, but the
evaluation geometry necessarily reaches backward into sourcing.

### 6. Efficient early killing vs. false-negative and monoculture risk

The intake is intentionally asymmetric: a generous-input failure is treated as
strong, while a pass merely licenses further work. Cost reachability and payoff
shape are moved ahead of data pulls, and sourcing prioritizes low-frequency,
large-per-event mechanisms while placing intraday microstructure on
"graveyard-watch."

This saves K, data spend, and operator time after repeated cost-wall failures.
The countercost is path dependence: the generator increasingly searches in the
classes the evaluator already knows how to admit. Novel mechanisms with weak
published priors, awkward expressions, or value that emerges only at book level
can be screened away before they receive the richer evaluation that could
distinguish them.

### 7. Automation throughput vs. human risk and evidence gates

An automation-friendly lifecycle wants machines to generate, test, and route
many candidates. The methodology requires operator ratification before a
campaign, distinct cost/run approvals for exploration and confirmation, and no
automatic promotion from a passing screen into deployment. On the authorization
axis, automation is deliberately asymmetric: it may de-risk automatically, but
risk-adding moves are human-gated except for one bounded sandbox lane.

That is appropriate for capital safety, but it means the end-to-end pipeline is
not symmetrically automatable. Generation can scale faster than approvals and
independent holdouts can be provisioned; evaluation therefore becomes both the
statistical bottleneck and the governance bottleneck.

### 8. A clean two-stage theory vs. reachable process falsifiers

Route B's governing hypothesis was about the later stability of candidates that
first passed confirmation. Because no campaign reached confirmation, that
empirical falsifier could never fire. The process could continue producing
honest nulls without ever testing whether the two-stage mechanism did its job.

This is a meta-evaluation tension: strict candidate-level gates do not guarantee
that the generator/evaluator interface itself is testable. A pipeline needs
channel-level liveness criteria (promotion yield, confirm reachability, cost per
confirm, and time to a decisive verdict), not only rigorous tests for candidates
that happen to arrive.

## What is fundamental, and what was a design defect?

The first, second, third, fifth, sixth, and seventh tensions are fundamental
trade-offs. They can be priced and monitored but not eliminated. The fourth and
eighth became concrete design defects in Route B: the generated statistic was
not economically connected to a tradeable object, and the channel's success
falsifier depended on a state the channel could not reach.

The repository's retirement decision is therefore best read neither as
"generation failed" nor as "evaluation was too strict." The interface contract
was wrong. Generation optimized an upstream proxy; evaluation asked a downstream
question the proxy could not answer.

## Recommended deletions and simplifications

The pipeline should not respond by weakening holdouts or removing cost and firm
constraints. It should remove duplicated ceremony and make the object crossing
the generate/evaluate boundary smaller and more concrete.

| Action | Current friction | Recommended change | What remains protected |
|---|---|---|---|
| **Delete** proxy-only promotion | A correlation or response statistic can win generation without defining a trade | Do not admit a generated candidate unless it already specifies signal, entry clock, stop, exit/target, holding horizon, and costed payoff unit | Exploratory proxy work may continue as diagnostics, but cannot consume a confirm holdout or claim candidate status |
| **(Already enforced)** Route B excluded as a reusable template | The route is retired; a naive read of this note could imply exclusion from templates is still-open work | No new action: `docs/adr/2026-08-24-sourcing-phase-channel-retirement.md` §5 already forbids reopening the route informally or reviving its G/C structure by renaming, and `docs/methodology/avenue_a_generate_confirm.md` already carries a withdrawal banner excluding it from active use | Historical integrity and the lessons from four failed campaigns — already protected, not a pending recommendation |
| **Merge** generation charter and admission manifest | G0, seed manifests, and later preregistrations can restate instrument, K, windows, costs, and feature definitions | Create one immutable candidate contract at generation open; later stages append results and hashes rather than copying fields | Pre-registration, auditability, and selection accounting |
| **Merge** early economic gates | Cost reachability, payoff-shape pre-check, latency, and basic firm geometry can be separate stops over the same arithmetic | Compute a `TRADEABLE-REACHABLE` verdict from the candidate contract by delegating each limb to its existing named authority rather than deriving new arithmetic. Cost delegates to whichever authority the eval-mechanism-shape screen's EM1 currently points at (`docs/methodology/strategy_harvest.md` Requirement 5, per `docs/spec/2026-08-05-eval-mechanism-shape-screen.md` §3a) — `scripts/cost_geometry_pregate.py`'s Phase-0 role stays additive alongside it (`docs/adr/2026-06-22-cost-geometry-pregate.md` §2, different quantity, not a competing one); `TRADEABLE-REACHABLE` re-points if the open G3 board item re-points EM1, but must never fork a competing cost formula. The shape limb sources prior win-rate/mean-win/mean-loss inputs the contract must freeze explicitly; a candidate with no citable shape priors routes to a **pre-freeze shape-extraction probe** (the same pattern as harvest Requirement 2's δ-extraction probe: declared on the draft contract, its data spend and K accounted, never touching the reserved CONFIRM window) and freezes only after the limb is scored — there is no deferred-until-after-freeze branch | Every underlying threshold remains sourced from its current owner; `TRADEABLE-REACHABLE` is a pure orchestrator, never a third cost authority; no candidate is scored on a guessed payoff shape, and no contract freezes with an unscored kill gate |
| **Simplify** operator approvals | Separate permission points can make the operator the throughput scheduler rather than the risk owner | Approve one campaign envelope up front: maximum spend, schemas, windows, and K. Confirm attempts are not a spendable envelope item — they stay bound to the frozen multi-candidate confirm count `M`, Bonferroni/Holm-adjusted and set at contract freeze, and any `VOID-*` result exhausts that attempt and requires a fresh campaign with a fresh holdout, never a retry inside the same envelope. Require another GO only to exceed the envelope or cross into sandbox/capital | No unbudgeted spend, no autonomous risk addition, and no silent multiplicity inflation from repeatedly consulting confirm data within one approved envelope |
| **Simplify** evaluation order | Expensive robustness work can be scheduled before a candidate is economically viable | Run one ordered battery: class-level shape/role screen (EM0-EM5 on the draft catalogue, pre-K, pre-pull) → shape priors or pre-freeze extraction probe → all-clause reachability attestation, same-units/per-gate (pre-freeze, HARV-lane candidates) → contract freeze → `TRADEABLE-REACHABLE` (pre-explore, delegates to each limb's existing authority) → explore → contract integrity → role state-drift re-check (zero-K) → untouched confirm (including temporal robustness, one atomic verdict) → portfolio/venue fit post-confirm | Later gates remain unchanged but run only for candidates capable of reaching them |
| **Defer** portfolio composition | A candidate may be rejected early for book coordinates before it has an independently confirmed edge | The class-level role limbs (Product-Group/sign, session, S7 order-symbol occupancy, instrument-class) run **before Explore**, inside the EM0-EM5 screen on the draft catalogue — `docs/spec/2026-08-05-eval-mechanism-shape-screen.md` §2.0a requires the screen before any data is examined and prices late application to a scored list as a K charge. The pre-confirm evaluate step is then only a zero-K **state-drift re-check** of the selected candidates against the current compliance snapshot (occupancy and cap state move between scoping and confirm), plus variance dominance/risk-N_eff-delta where a book context exists — every limb scored as fit for the *currently scoped* account/book, never candidate-lifecycle admission (`docs/methodology/objective_composition_map.md:42-50`, `docs/spec/2026-07-27-third-leg-target-spec.md` §7.1, `docs/adr/2026-07-20-stage8-variance-dominance-risk-neff-gate.md` §2). Defer only the scoring that needs a known edge size — activity, drawdown, remaining sizing — to after confirm | Class-level screening happens where §2.0a puts it (pre-catalogue, at zero evidentiary cost); the late re-check cannot act as a free selection filter because its only consequence is the frozen `ROLE-BLOCKED` + succession semantics; a role rejection never becomes a candidate-lifecycle rejection; edge-sized scoring stays post-confirm |
| **Add one** channel-liveness gate | Candidate tests can be rigorous while the channel never produces a confirm | At channel open, freeze a maximum number of generation attempts or elapsed research sessions without a confirm; reaching it retires or redesigns the channel | Prevents indefinite honest-but-unproductive research |
| **Use one** terminal taxonomy | `FALSIFIED`, `STOP`, `VOID`, shape failures, and venue failures can blur what was actually rejected | Two of the three terminal candidate-rejection classes map losslessly onto the ratified 4-class WHY-rejected taxonomy (`docs/adr/2026-06-14-rejected-candidate-patterns.md` §A): `MARKET-NULL` → edge-failure (its add-back — a genuinely new mechanism, never a re-tune — carries over unchanged); `VENUE-FAIL` → venue-cost-constraint or portfolio-fit-tail depending on which limb fired, each keeping its existing add-back. `EXPRESSION-FAIL` maps onto **none** of the four losslessly — the mechanism observable survived, so forcing edge-failure's "new mechanism" add-back would be wrong in both directions — and the amending ADR must instead add it as a **fifth class, expression-failure**, with its own binary add-back and escalation terminus (defined in the lean evaluate phase, step 5). Separately preserve the scope/register key `docs/adr/2026-08-09-rejection-register-topology-and-bar-wiring.md` §D3 already rules (per-direction/instrument-scoped → instrument ledger; domain/cross-instrument → `rejected_candidates.md`; meta-layer → `rejected_signals.md`) — the WHY class alone cannot select an owning register. `EVIDENCE-VOID` and `ROLE-BLOCKED` are excluded from the mapping entirely — both are nonterminal for the candidate, and §D3 already excludes power-voids and non-rejections from every register. `CHANNEL-FAIL` is excluded too — a channel-level process disposition, not evidence against any candidate. This is an amendment to both ADRs (a fifth §A row plus the two lossless mappings), not a routing-only relabeling | No failed candidate is revived, no non-rejection is forced into a rejection register, no existing class's add-back condition changes, and the one genuinely new class arrives with its own binary add-back rather than borrowing a wrong one |

### Proposed lean generate phase

1. **Choose a mechanism and a tradeable template.** A candidate begins with a
   causal or evidence-robustness prior plus a complete trade object—not a
   predictive feature alone. Define the complete adjudication rule for the
   mechanism-level discriminator that will later separate `EXPRESSION-FAIL`
   from `MARKET-NULL` — the observable, its test statistic, null hypothesis,
   direction, threshold, and coverage/power requirement — measured
   independently of the specific entry/exit implementation's payoff (e.g.,
   the raw signal's pre-specified association test against the target
   series, scored on the same holdout). The rule is fixed now; it is never
   chosen or interpreted after the holdout is read.
2. **Run the class-level shape/role screen on the draft catalogue.** Where
   the candidate class is subject to the eval-mechanism-shape screen, apply
   EM0-EM5 — which imports Product-Group/sign, session law, and S7
   order-symbol occupancy by reference — to the class/catalogue here, before
   any data is examined, per that spec's own §2.0a placement rule. Pruning
   shape-dead or role-impossible cells at this stage removes them from the
   catalogue **before** `K_intrinsic` is set, at zero evidentiary cost;
   §2.0a prices the same screen applied to a scored list after Explore as a
   K charge, which is why it can never run only late.
3. **Supply payoff-shape priors, or run a pre-freeze shape-extraction
   probe.** A HARV-lane candidate must carry cohort-derived
   win-rate/mean-win/mean-loss estimates at admission, under the same
   discipline harvest Requirement 2 applies to δ/σ (conservative central
   reading, publication-decay haircut, never an invented number). A
   candidate with no citable shape inputs is UNSCREENABLE on that limb and
   routes to a **pre-freeze extraction probe** — the same funded route as
   Requirement 2's δ-extraction probe: declared on the draft contract
   (instrument, window, exactly which statistics), its data spend and K
   accounted, never touching the reserved CONFIRM window — or the candidate
   drops. No contract freezes with the shape limb unscored.
4. **Run the all-clause reachability attestation on the draft contract,
   before freeze.** For mechanism-first (HARV-lane) candidates, per
   `docs/adr/2026-07-13-harv-discovery-lane-ratification.md` §2 as
   strengthened by `docs/adr/2026-07-16-harv-attestation-same-units-supersession.md`
   §2: simulate every gate the draft contract can die at — Stage-2 cost-law
   (`cohort δ (bp/event) ≥ 4 × RT_frac` at the adjudication-panel basis,
   commissions included, never waived as negligible), Stage-6 confirm,
   placebo, the payoff-shape limb (now carrying real inputs from step 3),
   and any bundled temporal battery — each in that gate's own units, never
   a convenience basis, before the contract is frozen. Checking the
   primary/Sharpe-space limb alone missed exactly this in the D5 and
   H-OD-1 closures, which froze on an unreachable Stage-2 cost-law gate the
   attestation failed to flag. A candidate outside the HARV/mechanism-first
   lane is not bound by this HARD gate absent a separate ratifying decision.
   Failures here stop before freeze and before any exploration pull.
5. **Freeze one candidate contract.** Record instrument, feature catalogue,
   entry/exit object, the mechanism-level discriminator's adjudication rule
   from step 1, exploration and confirm windows, K, the multi-candidate
   confirm count `M` with its Bonferroni/Holm adjustment, the succession
   rule for a role-blocked confirm slot (forfeit by default, or mechanical
   next-ranked succession — the choice is made here, never after
   exploration results are visible; see the lean evaluate phase, step 2),
   costs, schema ladder, the scored payoff-shape inputs from step 3, the
   scoped account/book identifier plus the compliance-state snapshot
   (occupancy map, cap state) the role screens were and will be scored
   against, and the campaign envelope once.
6. **Run the `TRADEABLE-REACHABLE` pre-gate.** Covers cost/latency/firm
   geometry, delegating each limb to its existing named authority, scoring
   the payoff-shape limb from the contract's frozen inputs. Every limb is
   scorable by construction — step 3 guarantees the inputs exist — so this
   gate has no deferral branch. A failure on any limb stops before the
   exploration pull.
7. **Explore within the envelope.** Score every declared cell and select at most
   the frozen confirm count `M`. No separate seed document is produced.
8. **Apply the channel-liveness bound.** Too many empty generations retires the
   channel or requires a redesigned contract; it does not license broader
   fishing.

This removes proxy promotion, duplicate declarations, repeated approval
ceremonies inside an already approved budget, and channels without an exit.

### Proposed lean evaluate phase

1. **Contract-integrity check, first:** confirm that code/data hashes, K, the
   frozen confirm count `M` and its Bonferroni/Holm-adjusted per-candidate
   bar, selected cell, and holdout match the frozen candidate contract
   before any other check runs. A mismatch voids or stops the attempt on
   its own — it must not be recorded as a structural or evidentiary
   rejection.
2. **Role state-drift re-check, zero-K:** before any holdout is consumed,
   re-validate each selected candidate against the *current* compliance
   snapshot versus the one frozen in the contract — Product-Group/sign, cap,
   session, and S7 order-symbol occupancy
   (`docs/methodology/objective_composition_map.md:42-50`,
   `docs/spec/2026-07-27-third-leg-target-spec.md` §7.1 S1-S7), plus variance
   dominance / risk-N_eff-delta where a book context exists
   (`docs/adr/2026-07-20-stage8-variance-dominance-risk-neff-gate.md` §2).
   The class-level application of these limbs already ran pre-Explore
   (generate-phase step 2), so an instance failing here means the *state*
   moved — occupancy or cap changed between scoping and confirm — not that
   a screen was skipped. None of these are candidate-lifecycle absolute —
   every one gates only the candidate's proposed role, never the candidate
   outright. Cap, session, and S7 occupancy are scoped to the single
   account/book currently in scope: a rejection there may still clear on a
   different, non-affiliated account. Product-Group/sign is scoped wider —
   absolute, no exceptions, across *any* account under the same control,
   not just the current one (`ops/prop_envelope_default.md` §4a) — so a
   Product-Group/sign rejection clears only outside that whole
   controlled-account group, never merely by picking a different account
   under the same operator.
   A failure here emits a separately keyed **`ROLE-BLOCKED`** disposition —
   naming the limb that fired and the compliance snapshot it was scored
   against — appended to the candidate contract and nowhere else: it is a
   role verdict, not a rejection, so it never enters any §D3 register.
   Its confirm slot follows the succession rule frozen in the contract:
   **forfeit by default** (the slot goes unread; the Bonferroni/Holm
   divisor stays at `M`, which is conservative), or, if the contract
   pre-declared it, **mechanical succession** — the next-ranked candidate
   from the frozen exploration ordering takes the slot, the divisor stays
   at `M`, and no discretion is exercised after exploration results are
   visible. Both options keep holdout reads at most `M` and keep the set
   of read candidates a pre-committed function of exploration output plus
   external compliance state; role-blocking consults no holdout data, so
   neither option leaks confirm information into selection.
3. **One untouched confirm run per selected candidate, including temporal
   robustness, as one atomic step:** for each of the `M` candidates in the
   frozen, multiplicity-adjusted confirm budget, run the confirm statistic
   and the minimum frozen temporal-consistency battery together (per the
   canonical Stage 6 definition, no new feature choice) and emit a single,
   separately keyed verdict only once both clear — `CONFIRMED`,
   `MARKET-NULL`, `EXPRESSION-FAIL`, or `EVIDENCE-VOID`. Do not run
   alternative expressions on the holdout, and do not emit `CONFIRMED` from
   the untouched run alone before temporal robustness has cleared.
   `EXPRESSION-FAIL` applies only when the frozen discriminator's complete
   adjudication rule (generate-phase step 1 — statistic, null, direction,
   threshold, coverage/power) returns a clean pass while the specific
   entry/exit implementation is rejected. If the discriminator itself
   cannot adjudicate — its own frozen coverage or power requirement is
   unmet — that takes precedence over any payoff verdict and the candidate
   is `EVIDENCE-VOID`, never `MARKET-NULL`: an underpowered discriminator is
   not evidence against the mechanism. Only a discriminator that cleanly
   fails (a powered, adjudicated no) lets a rejected implementation default
   to `MARKET-NULL`. The rule was fixed before the holdout was read, never
   chosen after. `EVIDENCE-VOID` also covers ordinary coverage/power/
   holdout-integrity failure of the confirm run itself — either way it
   exhausts this confirm attempt but is not evidence against the candidate.
4. **Portfolio and venue evaluation last:** for a `CONFIRMED` candidate,
   re-run step 2's role state-drift re-check if the deployment target has
   changed since scoping, and always re-check S7 order-symbol occupancy
   specifically regardless of target — occupancy is dynamic and can change
   independently of the deployment target between scoping and placement.
   Then score remaining composition, firm-level aggregate constraints,
   activity, drawdown, and sizing — only after an edge exists. A role or
   composition failure here rejects that book-leg placement, not the
   candidate's standalone confirmed status; a `VENUE-FAIL` here is not
   evidence that the market effect is false.
5. **Per-candidate append-only disposition:** for each selected candidate,
   append its own separately keyed class and detailed reason to the
   candidate contract. `CONFIRMED`, `MARKET-NULL`, `EXPRESSION-FAIL`, and
   `VENUE-FAIL` route once to reject, cold-store, or productionization.
   `EVIDENCE-VOID` routes instead to "attempt exhausted, eligible for a
   fresh campaign with a fresh holdout" — never a terminal
   reject/cold-store/productionization destination on its own.
   `ROLE-BLOCKED` (step 2) routes to "role unfit under the recorded
   snapshot; re-screenable when the scoped account/book or its occupancy
   changes" — also never terminal, and never a register entry.
   `EXPRESSION-FAIL`'s re-entry follows its proposed fifth-class add-back
   (the taxonomy row above): the barred object is the **expression**, not
   the mechanism. Add-back is binary — a materially new expression class of
   the same mechanism, differing on a declared structural axis (stop logic,
   exit family, or holding-horizon class; never a parameter re-tune of the
   failed expression), admitted as a **new** candidate contract with fresh
   K and a fresh holdout, citing the failed entry. The failed expression
   itself stays frozen and barred, exactly as the `VENUE-FAIL` rule below
   already treats a venue-failed expression. And the ladder terminates: the
   contract freezes an expression-attempt bound `N_expr` (default 2) per
   mechanism — once `N_expr` independent expression classes have each
   produced `EXPRESSION-FAIL` while the discriminator kept passing, the
   mechanism entry migrates to the ratified **venue/cost-constraint** class
   and its existing add-back (a geometry clearing the cost-law pre-flight
   with margin, or a materially lower-cost venue): a real effect that no
   declared expression captures net of this venue's costs is, for this
   estate's purposes, uncapturable — not an invitation to a third
   expression.

This retains the untouched holdout, multiplicity accounting, cost realism,
robustness, and prop-firm rules. It deletes repeated restatement and avoids
spending evaluation effort on an object that was never tradeable.

### What I would not simplify

- Do not merge exploration and confirmation data.
- Do not reset K when a generated winner is renamed or moved into evaluation.
- Do not let a venue-compatible backtest substitute for an independent confirm.
- Do not automate size-up or deployment merely because the research envelope
  was pre-approved.
- Do not turn a `VENUE-FAIL` into permission to retune the same candidate; it may
  be cold-stored for a different venue, but the evaluated expression stays
  frozen.
- Do not turn an `EXPRESSION-FAIL` into permission to retune the failed
  expression: the add-back demands a materially new expression class under a
  new contract with fresh K and a fresh holdout, and the `N_expr` bound
  terminates the ladder into venue/cost-constraint — an alive discriminator
  is never a standing license to keep buying expression attempts.

## Practical review questions

Before opening another generate/evaluate channel, ask:

1. **Tradeable target:** Does generation rank the same economic object that
   evaluation will cost and score?
2. **Reachable promotion floor:** Does a threshold pass imply at least plausible
   cost, latency, and venue-shape reachability?
3. **Selection budget:** Is there enough catalogue breadth to learn anything
   while keeping K and confirm multiplicity admissible?
4. **Holdout budget:** Is the reserved data independently useful and powered,
   rather than merely untouched?
5. **Learning rule:** Which evaluation failures permit a new hypothesis, and
   which require stopping the class, without retuning the failed candidate?
6. **Channel liveness:** How many generate attempts may occur without a confirm,
   and what decision fires when that bound is reached?
7. **Venue/generalization split:** Is a rejection evidence against the market
   mechanism, the expression, or only the current firm's geometry?
8. **Automation boundary:** Which steps are machine-executable, which require an
   operator, and is the expected candidate rate compatible with that capacity?

These questions preserve the repository's anti-overfitting and safety posture
while making explicit that the generator itself is a component requiring
evaluation.
