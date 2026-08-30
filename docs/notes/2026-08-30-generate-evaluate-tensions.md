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
confirm stage. The route was ultimately retired because its promotion design
did not target a tradeable object and its own empirical falsifier therefore
could not become reachable.

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
round-trip cost and the required per-trade move. They returned
`SHAPE-UNSCREENABLE`; no confirm stages ran. The later diagnosis required any
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
| **Delete** Route B as a reusable template | The route is retired, but its historical checklist can still look like a pattern to copy | Keep the dated record for provenance; exclude it from active templates and do not revive its G/C structure by renaming it | Historical integrity and the lessons from four failed campaigns |
| **Merge** generation charter and admission manifest | G0, seed manifests, and later preregistrations can restate instrument, K, windows, costs, and feature definitions | Create one immutable candidate contract at generation open; later stages append results and hashes rather than copying fields | Pre-registration, auditability, and selection accounting |
| **Merge** early economic gates | Cost reachability, payoff-shape pre-check, latency, and basic firm geometry can be separate stops over the same arithmetic | Use one `TRADEABLE-REACHABLE` pre-gate that computes all four from the candidate contract and returns typed failure reasons | Every underlying threshold remains sourced from its current owner |
| **Simplify** operator approvals | Separate permission points can make the operator the throughput scheduler rather than the risk owner | Approve one campaign envelope up front: maximum spend, schemas, windows, K, and confirm attempts; require another GO only to exceed the envelope or cross into sandbox/capital | No unbudgeted spend and no autonomous risk addition |
| **Simplify** evaluation order | Expensive robustness work can be scheduled before a candidate is economically viable | Run a minimum ordered battery: contract integrity → tradeable reachability → untouched confirm → temporal robustness → portfolio/venue fit | Later gates remain unchanged but run only for candidates capable of reaching them |
| **Defer** portfolio composition | A candidate may be rejected early for book coordinates before it has an independently confirmed edge | Compute composition only after confirm, except for a cheap structural dominance pre-kill that is provably independent of edge | Variance dominance and firm-level aggregate constraints |
| **Add one** channel-liveness gate | Candidate tests can be rigorous while the channel never produces a confirm | At channel open, freeze a maximum number of generation attempts or elapsed research sessions without a confirm; reaching it retires or redesigns the channel | Prevents indefinite honest-but-unproductive research |
| **Use one** terminal taxonomy | `FALSIFIED`, `STOP`, `VOID`, shape failures, and venue failures can blur what was actually rejected | Emit one primary terminal class: `MARKET-NULL`, `EXPRESSION-FAIL`, `EVIDENCE-VOID`, `VENUE-FAIL`, or `CHANNEL-FAIL`, with existing detailed reason codes beneath it | No failed candidate is revived; the classification only improves routing |

### Proposed lean generate phase

1. **Choose a mechanism and a tradeable template.** A candidate begins with a
   causal or evidence-robustness prior plus a complete trade object—not a
   predictive feature alone.
2. **Freeze one candidate contract.** Record instrument, feature catalogue,
   entry/exit object, exploration and confirm windows, K, costs, schema ladder,
   and the campaign envelope once.
3. **Run the combined `TRADEABLE-REACHABLE` pre-gate.** Failures stop before a
   data pull. Passing only licenses generation.
4. **Explore within the envelope.** Score every declared cell and select at most
   the frozen confirm budget. No separate seed document is produced.
5. **Apply the channel-liveness bound.** Too many empty generations retires the
   channel or requires a redesigned contract; it does not license broader
   fishing.

This removes proxy promotion, duplicate declarations, repeated approval
ceremonies inside an already approved budget, and channels without an exit.

### Proposed lean evaluate phase

1. **Contract-integrity check:** confirm that code/data hashes, K, selected cell,
   and holdout match the frozen candidate contract.
2. **One untouched confirm run:** produce `CONFIRMED`, `MARKET-NULL`, or
   `EVIDENCE-VOID`; do not run alternative expressions on the holdout.
3. **Temporal robustness only for confirmed candidates:** run the minimum frozen
   temporal battery, with no new feature choice.
4. **Portfolio and venue evaluation last:** score composition, activity,
   drawdown, session/slot legality, and sizing only after an edge exists. A
   failure here is `VENUE-FAIL`, not evidence that the market effect is false.
5. **Single append-only disposition:** update the candidate contract with the
   terminal class and detailed reason, then route once to reject, cold-store, or
   productionization.

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
