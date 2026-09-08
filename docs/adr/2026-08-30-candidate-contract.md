# Candidate contract — fields, freezes, campaign authority and confirm family

**Status:** `Accepted` — operator ratified 2026-08-30; ownership consolidated 2026-09-08.
**Decision date:** 2026-08-30
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Format:** concise
**Layer:** methodology

This owns the complete candidate object, append-only freezes, campaign envelope,
and frozen multiplicity configuration. [Evaluation order](2026-08-30-evaluation-order.md)
owns sequencing, TRADEABLE-REACHABLE and terminal taxonomy;
[rejection patterns](2026-06-14-rejected-candidate-patterns.md#expression-ladder-and-register-routing)
owns the N_expr expression ladder; [channel liveness](../methodology/strategy_harvest.md#channel-liveness-contract)
owns the cross-channel requirement and routes to each channel's own ceilings.
These accepted rules do not establish that every checker or channel migration exists.

## Decision

**Effective:** new generation-open candidates after 2026-08-30, across the five
channels and future channels. Already-frozen candidates keep their records. The
channel artifact adoptions under Current owner remain separately owed; pending adoption does not
suspend evaluation order for contracts frozen after 2026-08-30.

### Contract fields and freezes

At generation-open, before any exploration data is examined, freeze exactly one
hash-addressed candidate contract per campaign, fixed trade template and catalogue.
Its founding fields are:

- Instrument and full feature/parameter catalogue; signal, entry clock, stop,
  exit/target, holding horizon and costed payoff unit. Missing any element means
  no candidate admission. Proxy diagnostics may continue, but cannot open a
  contract, consume a Confirm holdout or claim candidate status.
- Explore and Confirm windows; K declaration and manifest run_id; costs, schema
  ladder, and the approved campaign envelope.
- Citable payoff-shape priors (win rate, mean win and mean loss) or completed
  extraction-probe results; the cost authority and revision; the early Confirm
  reservation commit. Conservative priors/probe requirements and their scope are
  in [Reachability](2026-08-30-evaluation-order.md#reachability).
- Scoped account/book identifier and compliance snapshot (including occupancy
  and cap state); ROLE-BLOCKED succession rule, forfeit by default or prospectively
  declared mechanical succession from the full frozen exploration ranking.
- Complete independent mechanism-discriminator rule: observable and statistic,
  null hypothesis, expected direction, threshold, coverage and power requirements.
  It is measured independently of the expression's payoff; its meaning cannot be
  chosen after Explore or a holdout read.
- Family-wise alpha, confirm count M and named Bonferroni or Holm procedure.
  Their full semantics are below. A structurally new expression also cites the
  mechanism's complete rejection history and ordinal under the [N_expr ladder](2026-06-14-rejected-candidate-patterns.md#expression-ladder-and-register-routing).

**Cardinality:** Explore may select at most M parameter cells of that same template,
each a hash-pinned subentry inside the contract. Catalogue, selection ranking and
multiplicity configuration remain campaign-level. A different signal, stop family
or holding-horizon class needs a separately opened contract; it cannot be smuggled
in as another parameter cell.

**Distinct immutable freezes:** reserve Confirm by an append-only commitment on
the draft contract before any pre-freeze probe reads data. The founding freeze
follows completed priors/probe work and precedes Explore. At Explore close, append
the full scored ranking and selected set in a separate hash-pinned selection
freeze before any holdout access. Later reachability attestations, results,
confirmation and dispositions append typed entries, never rewrite founding facts.
One contract is a chain of separately committed freezes, not one mutable file.
After a channel adopts this format, its seed/slate/G0/Stage-0 steps append at their
existing freeze points instead of restating founding fields in separate documents.

**K authority:** `discovery_manifests/*.json`, written by `register_search.py`,
remains the sole machine K ledger. Contract K is a declaration that must agree with
that manifest, never a competing authority. K binds before exploration reads or
scoring; a check afterward cannot recover unregistered trials. Full contract-to-
manifest agreement checking remains implementation debt (Current owner).

### Campaign authority

Approve one campaign envelope before Explore: maximum data/compute spend, schemas,
Explore/Confirm windows and K. Work within it needs no repeated permission ask.
Exceeding any bound requires a fresh explicit operator GO. Sandbox promotion and
capital-facing actions retain their own authority under [S5](2026-08-07-loop-s5-bounded-promotion-lane.md).
[Rule 2](2026-06-16-rule-2-budget-before-acting.md) effort/iteration limits apply
independently; being inside the spend envelope does not satisfy the effort axis.

A pre-freeze extraction probe requires its own operator-approved spend/schema/
window/K ceiling before any data access, with instrument and exact statistics
declared on the draft contract. It may read only outside the already-reserved
Confirm window. If the campaign proceeds, cite actual probe spend and K as an
already-spent sub-line, counted exactly once within the campaign's inclusive
ceiling; never silently top up the ceiling. If no campaign freezes, close the
approved probe on the mechanism record as stand-alone spend, neither orphaned nor
charged to a nonexistent campaign.

An EVIDENCE-VOID exhausts that Confirm attempt. Further testing requires a fresh
campaign with a fresh holdout; neither the old envelope nor another informal ask
licenses re-consulting the same Confirm data.

Decisions and field changes are recorded prospectively with their owning spec,
campaign, plan, PR or ADR as appropriate. Required evidence and operator elections
remain binding; they do not require an ADR for every field, amendment or election
([ADR admission rule](2026-08-08-adr-ceremony-tiering.md)).

### Confirm family

Freeze alpha (family-wise significance), M (maximum catalogue cells advanced to
Confirm), and exactly one procedure for the life of the envelope. Bonferroni freezes
the fixed per-cell bar alpha/M. Holm freezes the step-down algorithm identity;
thresholds alpha/(M-i+1) attach after the Confirm p-values are ordered, not as
candidate-specific numbers selected beforehand. A missing procedure is integrity-invalid.

Forfeited ROLE-BLOCKED, EVIDENCE-VOID and unfilled slots carry conservative p=1.
M never shrinks under either procedure, even if Explore selects fewer cells.
Catalogue-selection correction under the K ledger (Bonferroni/BH triage at close)
and this later confirm-family correction are sequential and cumulative; neither
substitutes for the other or for any additional campaign-frozen evidence gate.

## Grounds

The shared object prevents seed, slate, G0 and confirmation records from drifting
and keeps proxy statistics from acquiring candidate status. Distinct immutable freezes
preserve prospective evidence boundaries without creating a second K ledger. Channel
gates retain their own scopes: complete fields alone do not pass them. A mutable all-stage
record would lose those boundaries; a universal channel replacement would erase real
differences in admission. Moving multiplicity fields to evaluation order would split
their definition from the contract that owns them.

## First review and unresolved obligations

**Trigger check schedule:** initial consolidated review 2026-11-08.

Inspect actual freeze chains for founding/Confirm leakage; whether two or more channels
need duplicate side-records because these fields cannot express real candidates; inclusive
probe accounting; fixed confirm families; and same-envelope retries after EVIDENCE-VOID.
Any such failure requires an explicit correction at the owner before relying on the
affected control, preserving the evidence and authority boundaries above.

Review the five artifact adoptions and [liveness reconciliations](../methodology/strategy_harvest.md#channel-liveness-contract)
still owed. For any ceiling that has fired, test whether it was UNREACHABLE or UNBINDING,
or needed an ad hoc override to enact its already-declared consequence. Correct the
affected control if so. If none has fired, retain the question for the first programme
audit following a channel's first firing. Missing examples are inconclusive, not PASS
or automatic revocation.

This replaces the candidate/envelope/channel carriers' redundant recurring document
reviews; useful unresolved commitments and each channel's own clocks remain.

## Current owner

The doctrine is Accepted; the complete contract schema, contract/K/ordinal
integrity checks, frozen M/procedure enforcement and probe bookkeeping are not
implemented by that status. `admission_schema.py` checks its narrower supplied
admission fields; `frozen_rules.py` verifies motif-shape hashes. Neither validates
this whole contract. `register_search.py` has lane-scoped prereg/attestation/
admission checks and catalogue K triage, not this complete freeze chain. The
generic blind CLI permits omitted prereg/admission while the named blind channel
requires prospective prereg and its K ceiling. That gap is not permission.

Each channel still owes a dated, approved artifact-adoption amendment with its
freeze points and owning files reconciled. Until then its existing artifact chain
remains live practice; there is no retroactive migration in this consolidation.

| Channel | Adoption owners |
|---|---|
| HARV | [intake](2026-07-15-external-mechanism-harvest-intake.md), [ratification](2026-07-13-harv-discovery-lane-ratification.md), [procedure §5–6](../methodology/strategy_harvest.md#5-seed-manifest-declaration-template) |
| Dense1m/TNEC | [lane spec](../spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md) |
| MSL | [charter](../spec/2026-08-12-msl-manual-sourcing-loop-charter.md), [ratification](2026-08-12-msl-sourcing-channel-ratification.md) |
| No-counterparty statistical/geometric | [blind channel](2026-08-15-no-counterparty-statistical-sourcing-channel.md) |
| Deep-iteration | [charter](2026-08-16-deep-iteration-lane-charter.md); GROW is tooling within it |

The [evaluation owner](2026-08-30-evaluation-order.md#current-owner)
retains sequencing/reachability/verdict tooling debt. [STATE](../../STATE.md#2026-11-08)
tracks review and unresolved work. No checker build, channel audit, campaign,
research read, cost increase or deployment is authorized by this consolidation.

Grounding at `502a8fb4717e8caaa7d183a0a010998cfd7a30c2`: `lab/discovery/register_search.py`
(`open_run`, `close_run`), `lab/discovery/admission_schema.py`,
`lab/discovery/frozen_rules.py`, the five channel owners linked above, and all six
August 30 records including their amendments. The [original candidate body](https://github.com/Joshua-Asante/first-passage/blob/4fb2b88f3b7d56d77463c43ba45c87ffadff6a31/docs/adr/2026-08-30-candidate-contract.md)
and [campaign-envelope body](https://github.com/Joshua-Asante/first-passage/blob/4fb2b88f3b7d56d77463c43ba45c87ffadff6a31/docs/adr/2026-08-30-operator-approvals-campaign-envelope.md)
preserve the ratification record. Removed carriers and blob identities are in [TOMBSTONES](TOMBSTONES.md).

Verification uses the canonical `.claude/skills/brief-authoring/scripts/check_brief.py`
with `--type adr`, `scripts/check_adr_graph.py` and `scripts/check_state_currency.py`.
Those checks do not establish adoption or evidence integrity: inspect each dated channel
amendment, pinned freeze chain and manifest agreement. A citation alone proves no adoption.
