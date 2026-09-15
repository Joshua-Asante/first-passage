# Tradeify attended system — simplification review (proposals for operator ruling)

**Status:** PROPOSAL PACKET · authorizes nothing · each accepted item lands as a dated
addendum at its named owner, after which this note is a derived mirror of those owners
([Rule 7](../operational_rules.md)).
**Recorded:** 2026-09-15 UTC. Base `origin/main` `242992b`.
**Authority:** Joshua directed the architecture review of the operator-attended automated
trading system and asked for this record ("draft them into an artifact, commit it and we will
review the pr"). Astra retains Tradeify coordination under the
[campaign ownership direction](../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#57--astra-tradeify-contract-ownership-and-closeout-routing-2026-09-13);
this note was drafted in a Claude Code session at the operator's direct instruction and does
not change that routing.
**Boundary:** documentation only. No code, configuration, strategy, allocation, registry,
`dd_protection` constant, deployment or arming change. No private figure is quoted.
**Owners this note proposes to amend:** TB-S3 rev9 · S2b build ADR · TB-P2 admission ADR ·
attended settlement contract · TB-T1 seal contract · attended release plan · Track A plan §3.2
and umbrella O-4 · the per-session GO clause · Rule 7 STATE currency and its checker/tests
(only if the proposed cadence migration is separately accepted).

---

## §0 — Rule 0 reads

Local source anchors are `git log -1 --format=%h 242992b -- <path>`, read 2026-09-15.
They are path heads at the fixed base, not claim-specific commits. PR references identify
separate reviewed revisions. §5 checks every local row, including rows added during review.

| Source | Anchor | What it pins for this note |
|---|---|---|
| [TB-S3 rail extension spec](../spec/2026-09-12-c1-multi-leg-rail-extension-spec.md) | `6a282f1` | L2(c) per-bar AMEND; L2(f) ATTACH after Striker's bare entry bar; L2(g) native trails on ORB stop entries; takeover = cancel-confirm plus close-confirm of whole legs |
| [TB-S3 rev9 halt/resume](../spec/2026-09-14-tb-s3-halt-resume-contract.md) | `7c3ace8` | §1 an incident revokes NORMAL and SCHEDULED_EXIT; [§2](../spec/2026-09-14-tb-s3-halt-resume-contract.md#2-trigger-decisions) "source explicitly unhealthy" enters INTERVENTION; [§5](../spec/2026-09-14-tb-s3-halt-resume-contract.md#5-exact-schedule-rule) `D = min(16:00, V − 15)` |
| [S2b build ADR](../adr/2026-08-08-s2b-signal-daemon-build.md) | `7c3ace8` | §2 second Fly app, listener B1 unchanged; §4 limb 1 tears back a shared volume; O-4 feed deferral, option A′ shortlisted |
| [S2 fork ADR](../adr/2026-08-07-loop-s2-signal-host-fork.md) | `770413b` | Python-native origin; Pine is research/export only |
| [TB-P2 admission ADR](../adr/2026-09-12-tradeify-book-protection-instance-admission.md) | `55c9d96` | §2a T8 sole n3 bound to FBR and S; [§2b](../adr/2026-09-12-tradeify-book-protection-instance-admission.md#2b--the-deployment-go-artifact-and-the-go-reseal-definition) GO baked into image v2 with a layer-equality reseal; [§3](../adr/2026-09-12-tradeify-book-protection-instance-admission.md#3--alternatives-considered) rejects a volume GO on mutability |
| [TB-T1 seal contract](../spec/2026-09-12-tradeify-account-snapshot-seal-contract.md) | `a51d988` | C10 `valid_until`; no fill, order or adjustment between S and the arm |
| [Attended settlement contract](../spec/2026-09-15-tradeify-attended-settlement-contract.md) | `4f000c6` | operator-signed one-use 300 s challenge per accepted close; balance substitutes for equity only with flatness evidence at the same boundary |
| [TB-S1 protection/capacity spec](../spec/2026-09-12-tradeify-book-protection-capacity-spec.md) | `4f000c6` | [§3](../spec/2026-09-12-tradeify-book-protection-capacity-spec.md#3-settled-close-state-machine) settled-close state machine; [§4](../spec/2026-09-12-tradeify-book-protection-capacity-spec.md#4-capacity-and-reconciliation) 80-micro cap, refuse-never-clip, Aegis-only takeover |
| [TB-S2 replay spec](../spec/2026-09-12-tradeify-synchronized-replay-spec.md) | `7c3ace8` | RC-4 fill model; RC-5 takeover modelled natively; RC-8 scheduled flatten as an operational overlay |
| [Attended release plan](../superpowers/plans/2026-09-14-tradeify-attended-release.md) | `1cdfafe` | Packets 0–6; [Packet 4](../superpowers/plans/2026-09-14-tradeify-attended-release.md#packet-4--qualify-the-actual-data-and-execution-route) qualifies the route after Packets 2–3 |
| [Packet 0 feasibility](2026-09-14-tradeify-attended-feasibility.md) | `7c3ace8` | [capability matrix](2026-09-14-tradeify-attended-feasibility.md#capability-to-consumer-matrix): E1/E2/E3 have no accepted producer; every L2 row unqualified; route capability named the largest uncertainty |
| [Track A plan §3.2](../superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md#32-a9--production-feed-verification-record-and-funding-checkpoint-added-2026-09-11) | `84216f3` | A9 vendor table; credential-boundary correction; six vendor questions "near the actual feed gate" |
| [M1 ADR](../adr/2026-07-22-c1-venue-native-monitoring-maturity.md) | `a3be3f4` | arm interlock; item 5 discharged 2026-09-14 |
| [Track B umbrella](../briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md) | `6a282f1` | [§0.8](../briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md#08--open-items-recorded-not-folded-owned-by-the-named-packet) O-4; wave gates; D-B4 K=1; D-B15 dry-run window |
| [Acceptance record](2026-09-10-tradeify-protection-selection.md) | `ea6d584` | selection evidence class; the Tradeify portfolio alias |
| [`ops/c1_rail/book_policy.py`](../../ops/c1_rail/book_policy.py) | `5b0dc5b` | `MICRO_EQUIVALENT` 6J=10; `BOOK_LEGS` Aegis normal base 8, priority 1 |
| [`ops/c1_rail/crosstrade_payload.py`](../../ops/c1_rail/crosstrade_payload.py) | `027a729` | existing commands: `place` with optional SL/TP, `closeposition`; no stop entry, no cancel |
| [`ops/c1_rail/c1_rail_arm.py`](../../ops/c1_rail/c1_rail_arm.py) | `027a729` | config writes require apply/restart and confirmation; `--status` prints persisted `dry_run` and `armed_until`, not effective runtime permission |
| [`ops/c1_rail/c1_rail_listener.py`](../../ops/c1_rail/c1_rail_listener.py) | `7bf243c` | legacy exit/flat routing; book entry/add refusal without a halt store |
| [`ops/c1_signal_daemon/book_protocol.py`](../../ops/c1_signal_daemon/book_protocol.py) | `85a025e` | `BookStrategy.on_bar / on_execution / set_mode / checkpoint`; `BracketAmend` "re-issue the bracket every bar exactly as Pine re-calls" |
| [`core/firm_rules.py`](../../core/firm_rules.py) | `7369675` | `Tradeify_Select_100K`: EOD trailing drawdown, 80-micro aggregate cap, 40 % eval consistency gate |
| [`STATE.md`](../../STATE.md) | `84216f3` | weekly operator trade; monthly subscription reconfirm |
| [`CLAUDE.md`](../../CLAUDE.md) | `2cb980d` | "every armed session needs its own GO"; disarm before `armed_until` |
| [STATE currency rule](../operational_rules.md) | `502a8fb` | Rule 7 requires Weekly/Monthly recurring headings within 7/31 days |
| [Currency checker](../../scripts/check_state_currency.py) | `502a8fb` | exact Weekly/Monthly headings and next-occurrence horizons are enforced |
| [Currency tests](../../tests/test_state_currency.py) | `b916070` | cadence boundary, duplicate/missing heading and stale-date rejection |
| [Broker emulator](../../ops/c1_signal_daemon/tv_broker_emulator.py) | `18b37bb` | THIS_CLOSE versus NEXT_OPEN execution; captured exit scope; gap-stop fills |
| [Arming procedure](rail_build/ARMING_PROCEDURE.md) | `7c3ace8` | persisted disarm must be applied and verified in the running service |
| [PR #395](https://github.com/Joshua-Asante/first-passage/pull/395) reviewed `bd41cb6` (integration reference) | — | Settlement component split; `operator_keys.json` scopes `submit_account_close` and `record_only`; verifier reuse does not grant deployment authority |
| [PR #396](https://github.com/Joshua-Asante/first-passage/pull/396) reviewed `7e83e1b` | — | Extracted calendar; explicit coverage bounds and `schedule_for`; schedule lookup does not authorize dispatch |

Review correction source refresh at PR head `00b1d20`: re-read `core/dd_protection.py`,
`ops/c1_rail/book_policy.py` (mode thresholds and quantity floors), `c1_rail_arm.py::plan_disarm`
(clears the deadline), TB-P2 T8–T11, TB-T1 C10, TB-S2 RC-4, TB-S3 rev9, and the settlement
contract's evidence, finality and key-scope sections. These sources support the corrections
below. Also checked the enrolled scopes at `bd41cb6`, calendar interface at `7e83e1b`, and
`tv_broker_emulator.py::_at_open` at `00b1d20` (stop gaps fill at open with slippage).
These are revision-bound references, not a current readiness claim.

The [coordinator review](https://github.com/Joshua-Asante/first-passage/pull/397#issuecomment-5685825040)
records the approved split into calendar, evidence ingestion, pure settlement calculation,
durable settlement owner and qualification. Keep #396 independently reviewable and continue
evidence/calculation repairs. P1/P5 rulings stay outside those component PRs; P6's acceptance
contract must be decided before implementing a replacement authorization path.

---

## §1 — Ruled exclusion (2026-09-15)

**Static per-leg capacity caps replacing the shared 80-micro cap and Aegis takeover: EXCLUDED
by the operator.** Ruling, verbatim: "Aegis takeover is a key part of this book's edge."

Consequence for every proposal below: whole-leg takeover in D-B8 priority order stays. Any
reduced order-primitive set must still support cancel-confirm of lower-priority working risk and
close-confirm of whole lower-priority legs, and the replay keeps modelling takeover natively
(TB-S2 RC-5). Do not re-propose static per-leg allocations for this book.

---

## §2 — Proposals

### Review correction — separate the decisions from the missing contracts

The two review rounds expose a repeated error: the packet treats a label such as "GO",
"disarm", "market close" or "route spike" as a complete operation. Its proposed benefit
then exceeds the cases actually specified or checked. The first correction named retained
guarantees but did not fully trace their consumers, later transitions or verification coverage.
For example, checking a fresh boot did not check reuse after initial activation; checking
persisted disarm did not check the running listener; checking three anchors did not verify
the source table. These are distinct, testable failures, not proof that simplification itself
is unsound.

This note is a decision map. It cannot substitute for the missing execution, activation,
cadence or qualification contracts. §4 decomposes that work into bounded tasks with owners,
dependencies and counterexample traces. A benefit is conditional on its task's acceptance;
an unimplemented replacement leaves the existing operation and gate in force. No number of
clean sessions, passing document links or successful command responses discharges that work.

Each proposal states the current choice with its source, the simpler choice, what it removes,
what it costs, what it preserves, the owner and the ruling asked for, the window in which the
change is still cheap, and how acceptance would be verified. Numbering P1–P9 is this note's;
the conversation's item 1 was the excluded proposal in §1.

### P1 — Static broker-side protection at entry; logic exits as bar-close market orders

**Current.** The ports reproduce Pine's per-bar `strategy.exit` re-call at the broker. Striker
enters bare and attaches protection one bar later (ATTACH, L2(f)); every leg re-issues its exit
levels each closed bar (AMEND, L2(c)); ORB carries native trailing brackets on stop entries
(L2(g)). None of (c), (f) or (g) has an accepted route producer.

**Proposed.** Every entry and add carries one static safety stop only, attached at fill using
the `stop_dist_pts` the B1 payload already carries. No profit target rests at the broker:
an initial target could become stale and fill intrabar before the port updates it. Targets, trail and all
other exit logic stays in the Python port. The proposed overlay evaluates logic exits on a
completed bar and emits a market-close intent with the port's declared timing and confirmed
fill scope. "Completed-bar evaluation" alone does not define a trigger: the semantic task below
must specify close-only versus high/low touch, the applicable level before/after its bar update,
trailing activation and precedence when protection, a logic exit and an add coincide. Until
those fields are frozen, this is a design direction, not an executable overlay. The broker never
receives an amend or a late attach. The live mutation set becomes: stop or market `place` with an
attached static safety stop, scoped or full `closeposition`, and `cancel` of a working order,
including attached protection. P9 must qualify protection cleanup on every close path.

**Removes, after qualification.** Dynamic AMEND, late ATTACH and native-trail requirements
(L2(c)/(f)/(g)) may be retired only after their replacement rows, including attached-stop
creation and cleanup, pass. Intended benefits are fewer broker mutations and no deliberate
bare entry bar; placement/partial-fill failures can still leave uncertain protection and must
retain their halt/recovery handling.

**Costs.** Target/trail exits become market exits instead of intrabar level fills. Retain the
protocol's per-port market timing in replay; do not add a universal next-bar delay:

| Event | Replay execution rule | Boundary retained |
|---|---|---|
| ORB and Striker logic market exit | `THIS_CLOSE`: generating bar's close plus adverse slippage | Evaluate at the completed bar; retain explicit confirmed-fill scope |
| Aegis and Vanguard logic market exit | `NEXT_OPEN`: next bar's open plus adverse slippage | Capture scope when the exit is issued; a subsequent add is not silently included |
| Static safety stop triggered intrabar or through a gap | Retained RC-4 stop-fill model | Gap fills use the open plus adverse slippage; protection-owner/FIFO accounting remains explicit |
| Scheduled flatten | RC-8 scheduled instant | Not delayed by a port's `NEXT_OPEN` setting |

These are replay conventions, not a promise that live orders fill at an already observed
close. Live dispatch and acknowledgment latency require separate route evidence/stress costing;
a changed timing convention would be an additional explicit overlay, not assumed parity.
The safety stop does not bound loss: a gap through it fills at the next available price
plus adverse slippage (RC-4 gap-through-stop replay uses the bar open). Delayed logic exits can
also suffer gaps or transport delay. Striker's first bar becomes protected where Pine leaves
it bare, a deliberate safety-side deviation. Book semantics change, so this is a pre-registered
operational overlay in the same class as RC-8: parity to the exports remains the proof of the
port, the overlay applies after it, and affected overlay ledgers are regenerated separately
before TB-F1. The overlay must cost target exits as completed-bar market exits too, including
a touch of the old target before a later target update, gap-through-stop, and delayed-close cases.

**Preserves.** Whole-leg takeover remains required, conditional on P9 proving the complete
cancel/close/protection lifecycle; reserve before send; release on terminal evidence only;
every leg's entry logic.

**Owner and ruling.** TB-S3 (primitive set and L2 rows), TB-S2 (RC-4 overlay), TB-P1/TB-F1
(freeze), including TB-S3 K2 protection ownership. Proposed text: "Develop and freeze a
safety-stop-only execution overlay with the per-port timing above. Specify trigger/update
ordering, captured scope, FIFO/protection ownership, confirmed feedback and collision
precedence for every exit class; explicitly cost any changed allocation semantics. Qualify
the replacement lifecycle rows before retiring L2(c)/(f)/(g) or freezing F1."

**Window.** Before TB-F1 freezes.

**Verification.** The accepted overlay's TB-S3 L2 table lists place-with-safety-stop, close and cancel; no AMEND or
ATTACH action reaches the listener from `book_protocol`; the regenerated ledgers carry the overlay
digest inside FBR. Replay traces show no broker fill at an obsolete target and include adverse
gap fills beyond the safety-stop level. Required traces distinguish a bar closing at 100 from
a next open at 90, target touch without close crossing, exit plus same-bar add, and triggering
protection owner versus FIFO-allocated fills. Preserve the appropriate port timing and scope;
an explicit scoped close is not interchangeable with a protection-triggered FIFO exit.
Baseline parity remains separately evidenced; route evidence meets P9's lifecycle checks.

### P2 — One process for strategy evaluation, sizing and dispatch

**Current.** The daemon, a second Fly app, evaluates strategies and POSTs B1 JSON to the
listener. DD-locality argued the split when Pine alerts were the origin. In rev9 the hop generates
the bar-barrier timeout, the control-read watchdog, authenticated source-health reports,
daemon-loss recovery and the "daemon cannot grant permission" invariant.

**Proposed.** Fold the evaluation loop into the listener image, which already hosts
`book_policy`, capacity, the halt store and the arm interlock: feed, four adapters, barrier,
shared sizing and capacity, dispatch and the SQLite journals in one service, with module
boundaries in place of HTTP. DD-locality becomes "only the account-owner module reads or writes
peak state."

**Removes, after equivalent local supervision is accepted.** The network form of the barrier
and watchdog; the source-health
authentication protocol; daemon-loss recovery; one always-on machine and its volume; the B1
listener client on the strategy path.

**Costs.** Supersedes S2b §2 "Second Fly app" and reinterprets §4 limb 1, so it needs a
superseding ADR or dated revision. M1 acceptance pins are image-bound, so a merged image needs
pin re-verification or a re-bake; whether a new attended ceremony is owed is the M1 owner's call.
The daemon's `GET /` health merges into the listener's.

**Preserves.** Fail-closed on a stale source; listener-owned permission, now module-owned; the
B1 field contract for any external client.
Co-location removes the network hop, not synchronized-bar completeness, feed freshness,
evaluation timeout supervision or the serialized dispatch fence. A hung evaluation loop must
not prevent the owner from halting new risk or enforcing the retained schedule; Packet 2 must
specify and test that scheduling boundary before the distributed handlers are retired.

**Owner and ruling.** S2b build ADR §2 and §4; S2 fork ADR unchanged (the origin is still
Python); M1 ADR (pins); attended release plan Packet 2 (wiring). Proposed text: "Packet 2 wires
the evaluation loop into the listener process; the second app is retired when the merged image
passes M1 pin verification."

**Window.** Before Packet 2 wires daemon to listener. After that the split is effectively
permanent.

**Verification.** One app under `deploy/`; no `listener_client` POST on the strategy path;
source health is in-process state rather than an authenticated report. These structural checks
are insufficient alone: an incomplete barrier, stale source and hung evaluator must still halt
risk without starving the serialized owner or its retained scheduled-exit checks.

### P3 — Sign the deployment GO; keep it off the image

**Current.** TB-P2 §2b bakes the GO artifact into image v2 through an artifact-only commit, then
proves every non-GO layer digest identical to v1 and reseals EF2; R1c voids on any deviation. §3
rejected a volume-resident GO because "a mutable volume file lets the gate be satisfied by editing
the thing being gated on."

**Proposed.** The GO is a signed envelope over a schema version, purpose `deployment_go`,
account identity, initial deployment identity, v1 image digest, FBR, EF1, seal digest S, qualification variant and digest,
`valid_until`, operator identity and recording time. Without P5, qualification is the sole n3
result bound to FBR and S. With P5, it is the globally passing envelope result bound to FBR,
plus the TB-E2 membership record binding S to that envelope and its coverage proof; all those
digests are signed and checked. A result from one variant cannot satisfy the other.

The settlement key currently has `submit_account_close` and `record_only` authority, neither
of which permits deployment. Reuse requires an
explicit settlement-contract/key-enrollment amendment authorizing `deployment_go` for this
account, or a separately enrolled deployment key. `ed25519_verify.verify` checks the signature;
the in-image authorization gate also checks the signed purpose and account against the baked-in
trusted key's allowed actions. Settlement authority alone never grants deployment authority.
The envelope rests on the volume or is
supplied at arm time. Forging it requires the private key, so mutability no longer satisfies the
gate. `--arm` refuses on a missing or invalid signature, a digest that does not match the running
image, or an expired `valid_until`. T11 repeats the applicable checks at effective activation
and records its boot-bound acknowledgment before enabling risk; a successful config write is
not activation.

**Initial activation only.** P3 replaces packaging/authentication of the initial TB-B10 GO;
it does not supersede TB-P2's one-use T11 boundary. The activation owner must durably consume
the initial deployment identity and S together with the request/boot-bound acknowledgment
before enabling risk. A different serialization or re-signed envelope for the same deployment
cannot reset consumption. A repeated request may retrieve its receipt but cannot enable a
new boot. After completed activation, restart starts disarmed even before GO expiry and even
with no intervening account activity. Ongoing/restart authority requires the separately defined
and ratified TB-P2/TB-S3 contract; P7 cannot inherit it from this envelope.

The consumption store is part of safety state, not the mutable GO file. Missing, corrupt or
unverifiably restored consumption history blocks activation. The owned lifecycle task must
resolve concurrent requests, crash cuts between persistence/acknowledgment/enable, and rollback
of stored state. Until it is implemented and verified, valid signature checks alone do not
establish the proposed replacement gate.

**Removes.** Image v2, the artifact-only commit, EF2, the layer-by-layer manifest equality proof,
the image half of R1c, and a rebuild inside the seal window.

**Costs.** Key custody becomes load-bearing, which settlement already made true. The public key
is pinned in the image, so key rotation means a new image, the same as today's pins. Depends on
the reviewed signature utility landing, which can be extracted independently of PR #395's
settlement integration, and the GO authorization contract being accepted.

**Preserves.** Qualification bound to FBR and sealed live state through the selected variant
above; S freshness and no-activity checks; B7 and the retained T-stage gates under the chosen
qualification variant; GO never written on a failed
qualification.

**Owner and ruling.** TB-P2 §2b and §3 (dated revision); `c1_rail_arm.py` interlock; TB-O1
procedure; TB-I3 effective-activation owner; attended settlement contract key scope and trusted-key enrollment. Proposed text:
"The deployment GO is a purpose-scoped signed envelope verified in-image, binding either the
sole n3/S result or P5's global envelope plus S membership record; the B7 image
is the release image. Retire the reseal proof only after the one-use initial-activation
replacement is accepted. Later-session and restart authorization are outside this change."

**Window.** Any time before TB-D2; cleanest before Packet 6.

**Verification.** `test -f docs/notes/rail_build/DEPLOYMENT_GO.json` is no longer part of the
arm gate; arm tests refuse unsigned, foreign-key and expired envelopes, settlement-only keys,
wrong purposes/accounts, and substitution between qualification variants. A deployment signature
cannot submit a settled close. Tests cover both P3 alone and P3+P5, including mismatched S,
FBR, envelope or membership digests. Replay after activation acknowledgment refuses even
before expiry with unchanged account state; concurrent or re-signed requests cannot activate
twice. Missing consumption history and each crash/restore cut fail closed without a new boot
gaining permission. The procedure has no image rebuild between B7 and the initial arm.

### P4 — Scheduled flatten survives a source fault

**Current.** Rev9 §2 routes "required source explicitly unhealthy, control read fails, or bar
barrier expires" into INTERVENTION, and §1 says INTERVENTION revokes SCHEDULED_EXIT. A feed
outage near the close therefore leaves own-flat to the operator.

**Proposed.** Split the incident classes. SOURCE_FAULT (stale or unhealthy source, expired
barrier, missing daemon heartbeat/control poll only) halts new risk and keeps SCHEDULED_EXIT:
the account owner's authority, identity, safety storage, calendar and broker evidence must all
remain valid. Failure to read authoritative control state is INTERVENTION, not SOURCE_FAULT.
The cutoff cancels and the
`D − 5` flatten still run from the schedule clock and resting protection, confirmed from broker
evidence rather than from the daemon, and the operator is alerted. INTERVENTION is reserved for
uncertain transport or order outcome, a protection fault, invalid runtime identity, corrupt safety
state, operator stop and an own-flat breach.

**Removes.** The operator as the only path to own-flat during a feed outage; one class of
"attended alert with live exposure" events.

**Costs.** The flatten runs without fresh bars, so its confirmation must come from broker
evidence; if that evidence is itself unavailable the case is already INTERVENTION. Amends rev9 §1
and §2 (rev10), the arming procedure and the replay's incident scenarios; RC-8 is unchanged.

**Preserves.** No daemon emergency-flat; no automatic recovery from an uncertain order state; the
envelope rule never to design to the venue's auto-flatten.

**Owner and ruling.** TB-S3 rev9 §1 and §2; [arming procedure](rail_build/ARMING_PROCEDURE.md);
TB-S2 incident scenarios. Proposed text: "A source fault halts new risk and retains scheduled
exit authority; INTERVENTION is entered only on the enumerated order-state, identity, storage and
operator triggers."

**Window.** Before Packet 2's halt and recovery slices are accepted.

**Verification.** A test where source health goes stale shortly before cutoff still produces the
cutoff cancel and the `D − 5` flatten from the listener and ends flat by D; an uncertain-order
incident at the same instant does not.

### P5 — Qualify an initial-state envelope instead of a sole n3 bound to a live seal

**Current.** T8 runs the sole n3 replay from S's initial state, started before `valid_until`;
any fill, order or adjustment between S and the arm voids S and the dependent n3 result (C10,
R1c). The weekly operator trade and the arm window must be choreographed around it.

**Proposed.** TB-F1 pre-registers the entire deployable initial-state envelope, its disjoint
cells and exact boundary ownership, both mode states, and the carried-peak convention. Each
cell specifies every replay-relevant initial field, including equity, peak, remaining venue
drawdown headroom and strategy state; drawdown percentage alone is insufficient.
Before any n3 outcome is exposed, each cell requires an accepted conservative-boundary proof
or equivalence/monotonicity proof covering all four n3 conditions over every state in that cell.
Representative-point results do not cover intervals. Mode thresholds and quantity floors must
be partitioned or covered by the proof; unproved cells block the proposal before n3.

After the retained n1/n2/Part A gates pass, TB-E1 runs the pre-registered cases on the frozen
n3 stream within the frozen budget, with no outcome used to alter the contract, and
produces one global verdict: ALL deployable cells must pass ALL four conditions. One failed or
indeterminate cell fails the envelope terminally; no dropping cells, moving boundaries, rerun,
or selection of a passing subset after results. TB-E2 captures S and checks membership in that
unchanged, globally passing envelope using the frozen predicate, recording S, FBR, envelope,
coverage-proof and result digests. No replay runs at arm time.

**Removes.** Replay from the live seal window. The seal itself still expires and is invalidated
by activity before arm; a changed S requires fresh sealing and membership evidence, never a
new qualification draw. Weekly activity cannot select a successful subset of outcomes.

**Costs.** Compute multiplied by cells inside the frozen budget. Under D-B4 this is one
pre-registered attempt with a larger frozen contract, not an extra sample, but the operator must
rule that reading and accept the coverage proofs before n3. A live state outside the frozen
envelope is BLOCKED, never a new draw. If coverage cannot be proved within budget, defer P5
and retain the sole n3/S contract; do not infer interval coverage from a grid.

**Preserves.** The fresh-stream property (the grid runs on the n3 stream); one attempt; failure
terminal; the row admitted only after TB-E1.

**Owner and ruling.** TB-P2 §2a T8 and §4 H; TB-P1/TB-F1 contract; TB-T1 C10 (the seal binds
envelope membership to a global result). Proposed text: "TB-E2 binds S to the unchanged,
pre-registered, whole-envelope PASS and accepted coverage proofs; no arm-time replay or
post-result cell selection. S freshness and no-activity requirements remain."

**Window.** Before TB-F1.

**Verification.** F1 contains exact predicates, coverage proofs, budget and the all-cells gate.
Traces cover a state between representatives, threshold/floor boundaries and different absolute
headroom at the same drawdown. A passing representative without a coverage proof refuses;
one failing cell refuses deployment even when S lands in a passing cell. Post-result activity
cannot change that verdict. TB-E2 records membership without replay and rejects stale/changed S;
when P3 is accepted its signed GO binds this record and the global result.

### P6 — Automate settled-close collection; acceptance waits for finality evidence

**Current.** The settlement contract approved 2026-09-15 requires an operator-signed one-use
challenge for every accepted close; missing or stale evidence blocks the next session. The rail
already reads net liquidation through the configured CrossTrade equity source.

**Proposed.** Automate collection and reconciliation of the settlement contract's full package:
account/session identity, effective-close equity (or balance with flatness at that boundary),
complete account-wide positions/orders and unresolved requests, and inception-through-capture
cash/balance history with verified query coverage and comparison to retained records for later
corrections. Retain cost classification, decimal arithmetic, prior-state continuity and refusal
of adjustments/unknowns. Current CrossTrade observations remain diagnostic.

Automatic acceptance additionally requires a qualified, owner-accepted finality signal tied
to that account/session and complete source revision, establishing that costs/adjustments are
included and pending corrections resolved. Agreeing current balances, repeated polls, flatness
and elapsed time cannot supply it. No such producer is established by the demonstrated reports:
the recommendation is to DEFER automatic acceptance until its capability and correction
handling are proved. Until then the existing evidence-backed signed challenge remains required each day;
even a signature cannot supply missing source completeness or finality facts.

After that dependency is discharged, frozen-tolerance agreement and identical mode decisions
are additional cross-checks, never substitutes for the package or finality gate. Missing/stale
evidence, unresolved fees or revisions block next-session use. The accepted equity must be the
exact effective-close value from the qualified balance/equity-history source, with provenance;
dashboard/current-equity values only corroborate it. Never average, select the more favorable
value, or substitute a same-mode observation. The pure calculation ratchets the prior accepted
peak using that one accepted equity under the existing policy; tolerance does not hide an
unknown authoritative value. Automated and signed paths use identical evidence validation,
calculation and atomic durable acceptance; only submission authorization differs.
A correction follows the owner's
halt/adjudication protocol; it cannot silently rewrite an accepted close or active mode.

**Removes.** Manual collection work once the collector is qualified. Removal of the daily
attestation is conditional on an accepted finality producer; it is not presently established.

**Costs.** Any tolerance becomes a frozen F1 parameter. Dashboard capture still needs an
automated or attended source; if neither exists, settlement is blocked. B7's
initial-peak derivation is unchanged (D23).

**Preserves.** The single-writer chain; duplicate and out-of-order halts; never backdating; mode
selected once per session; a block on disagreement.

**Owner and ruling.** Attended settlement contract (dated amendment); TB-S1 §3;
`book_settlement.py` on PR #395. Proposed text: "Automate complete evidence collection; retain
attended acceptance until a separately qualified finality producer and correction protocol
support automatic acceptance. Balance agreement alone never authorizes a close."

**Window.** Before Packet 5; cheapest while PR #395's Step 5 is under review.

**Verification.** Equal balances with a pending fee, missing query range, unresolved correction,
or no accepted finality signal produce no automatic close. A later flat snapshot cannot prove
effective-close flatness. Test revision arrival against an already accepted record. Automatic
acceptance requires real producer evidence plus tests of the complete package and finality gate;
until then a clean day still consumes the signed challenge under the existing contract.

### P7 — Separate ongoing consent, effective disarm and calendar cadence

**Current, all documented.** A daily signed close (P6's target); a per-session arm GO ("every
armed session needs its own GO"); disarm before `armed_until`; a monthly session-calendar
extension with operator digest ratification where missing or expired rows refuse risk (PR #395
Step 4 covers 2026-09-03 to 2026-09-30); a monthly subscription reconfirm; the weekly
preservation trade, which strategy fills discharge once the book trades; incident attendance.

**Proposed.** Separate four decisions; do not accept them as one obligation-reduction bundle:

- **(a-consent), recommend DEFER:** weekly consent needs an ongoing activation contract from
  TB-P2/TB-S3/TB-I3 covering current-state evidence, fingerprints, per-session deadlines,
  revocation, restart and one-use resume. P3 authorizes initial activation only. The former
  "after N clean sessions" condition cannot supply a missing authority contract. Existing
  per-session consent and explicit operator arm remain until that contract is ratified.
- **(a-disarm), separate capability task:** own-flat must revoke permission in the running
  account owner, fence queued/concurrent mutations and account for already-sent/unknown work,
  persist `dry_run=true`/`armed_until=None`, and prove the runtime applied the disarmed state.
  `plan_disarm` only constructs those config values; the current helper writes them and warns
  that restart/apply plus confirmation is still required. A future accepted contract must
  define the ordered revoke/persist/apply/acknowledge transition. No successful file write or
  persisted `--status` may report effective disarm; a failed or unknown runtime apply remains
  incomplete and alerts the operator. Keep attended disarm/apply/verification until accepted.
- **(b), independently proposed:** author and ratify a three-month calendar with missing-coverage
  refusal retained. #396's loader already accepts explicit coverage bounds. The authoring tool
  still needs qualified source rows, explicit holiday CME trade-date mapping and a fresh digest
  ratification; calendar horizon does not grant any session's trading authority.
- **(c), separately proposed cadence migration:** fold subscription reconfirm into a quarterly
  review only after amending Rule 7 STATE currency, its checker and tests as well as STATE.
  The current gate requires exactly one Monthly recurring heading within 31 days. It cannot
  validate a quarterly replacement. Until the coordinated migration is accepted, retain the
  genuine monthly subscription deadline; never add a dummy monthly row to satisfy the parser.

**Removes, conditionally.** (a-consent) could reduce repeated consent; (a-disarm) could remove
manual disarm/apply steps; neither benefit exists today. (b) reduces calendar authoring cadence
after qualified coverage is ratified. (c) reduces subscription reconfirm cadence after the
governance/enforcement migration. Daily settlement remains while P6 is deferred.

**Costs.** Ongoing authority and effective disarm are distinct runtime contracts, not a calendar
setting. Calendar coverage and subscription cadence require separate decisions. Moving the
last monthly obligation changes a repository-enforced rule and must update its consumers.

**Preserves.** An explicit `armed_until` whenever armed; restart starts disarmed; incidents need
fresh attended recovery/resume; no agent trade. None of these proposals grants automatic rearm.

**Owner and ruling.** (a) TB-P2/TB-S3/TB-I3, rail GO ADR, M1 interlock and arming procedure;
`CLAUDE.md` follows the owner. (b) calendar owner/#396. (c) subscription owner/STATE plus
[operational_rules.md Rule 7](../operational_rules.md),
[`check_state_currency.py`](../../scripts/check_state_currency.py) and
[`test_state_currency.py`](../../tests/test_state_currency.py). Proposed text: "Defer ongoing
weekly consent pending its contract; develop effective disarm separately; decide calendar
coverage independently; change subscription cadence only with the currency-rule migration."

**Window.** No session-count shortcut for (a). (b) when source-backed coverage is ready;
(c) when the coordinated rule/checker/test proposal is reviewable.

**Verification.** Disarm tests must observe both active permission and persisted configuration,
including successful persistence with failed runtime apply, queued dispatch, crash/restart,
unknown in-flight outcomes and expiry. Ongoing consent requires its own replay/revocation tests.
For (c), run the currency checker on the proposed STATE and test missing/duplicate cadence
headings, stale dates, quarter boundaries and retained weekly obligations. The current checker
rejects simply renaming Monthly to Quarterly; that is a prerequisite failure, not a waived gate.

### P8 — Data-only feed vendor; send vendor diligence now

**Current.** O-4 is deferred. Option A′, a personal live Tradovate data account with parked
capital and a brokerage-backed secret, is shortlisted. Data-only vendors are marked "safe
fallback, not cost leader" because their run-rate equals the retired Databento plan. The six
vendor questions are to be sent "near the actual feed gate."

**Proposed.** Send the six questions to every shortlist candidate now, at zero spend, since
answers take weeks. Amend the decision rule so a data-only credential is preferred at equal
capability and a run-rate matching a retired plan is not a disqualifier. Funding still waits for
the checkpoint.

**Removes, conditionally.** Sending diligence earlier can reduce vendor lead time. An
order-capable credential leaves the data path only if the selected vendor supplies technically
enforced data-only scope or an enforced account/API-user restriction. Preference at equal
capability does not guarantee that outcome. Any order-capable finalist must disclose its
residual authority for the operator's separate selection decision and cannot claim this benefit.

**Costs.** None now. The run-rate against A′ remains the operator's call at the checkpoint.

**Preserves.** No signup or spend before the checkpoint; TB-I5 equivalence; the provider-neutral
`BarSource` contract.

**Owner and ruling.** Track A plan §3.2 (decision rule and timing); umbrella O-4; the S2b §2 row
at selection. Proposed text: "Vendor diligence is decoupled from the funding checkpoint and starts
now; the decision rule prefers a data-only credential at equal capability."

**Window.** Now.

**Verification.** The Track A plan carries a dated record of questions sent and answers received
per vendor; the decision-rule text is amended. The selected credential's enforced scope has
vendor evidence; an application promise to avoid order endpoints is not proof. Compare an
equal-capability data-only candidate and an order-capable candidate with different capabilities:
the preference alone must not classify the latter as data-only or waive existing eligibility gates.

### P9 — Separate early route reconnaissance from full qualification

**Current.** Packet 4 qualifies the route after Packets 2 and 3, and the feasibility record names
route capability the largest uncertainty. Canned payloads have filled on this account before, and
the operator already places one venue-required trade each week.

**Proposed.** Use the next separately authorized, operator-placed preservation trade as an
optional reconnaissance opportunity, only if venue rules and that trade's authorization allow
the chosen scenario. Predeclare the one observed entry/close lifecycle and its evidence scope.
This lane adds no trades and does not claim to cover both stop and market entry, full and scoped
closure, partials, rejection, takeover or cancellation races. Record the exact observed case and
evidence limitations; absence of another case leaves it unqualified.

Full qualification is a separate task owned by Packet 4 and dependent on P1's frozen semantic
matrix. Move the required capability-qualification slice ahead of acceptance of the Packet 2
slices that depend on it; it does not wait for the rest of Packet 4 or for those Packet 2
slices to be accepted. Source-independent Packet 2 implementation/offline tests may proceed,
but are not evidence of qualified live capability. Before any additional live action, its
owner must map each required lifecycle case to accepted
source documentation, offline simulation/injection and/or separately authorized live evidence,
without treating those evidence classes as interchangeable. A live plan must state actual
scenario prerequisites, maximum order/trade count, per-order and aggregate exposure, spend and
session bounds, account/consistency impact, evidence producers, terminal criteria, stop conditions
and attended recovery. Those bounds are not established in this note. Partial fills and races
cannot be guaranteed on demand; unobserved required cases remain blocked at the budget limit,
not retried without bound. One successful trade is not a qualification plan.

In that full qualification task, the verdict is per lifecycle case, not merely per command name.
For a filled entry/add carrying
protection, verify full close, scoped whole-leg close and Aegis takeover remove all child orders
for the closed exposure, using causally postdating broker-confirmed positions and working-order
evidence. Whole-account closure requires zero gross positions, no working orders/protective
orphans and no unresolved requests; scoped closure must preserve unrelated legs' valid protection.
Partial close/fill cases require protection sized to the confirmed remainder and no orphan or
over-sized child; if the static primitive set cannot accomplish that, record UNSUPPORTED.
Race cancellation against a stop fill and retain any uncertain request for intervention; a
successful cancel response alone earns no release credit. Missing causal evidence is AMBIGUOUS
and blocks dependent slices just as UNSUPPORTED does. Unexercised cases remain unqualified.

**Removes, conditionally.** Reconnaissance can expose an unsupported assumption earlier.
It cannot remove any qualification gate beyond the exact case and evidence class accepted by
the owner. A successful command response or eventual clean snapshot does not prove atomicity.

**Costs.** Reconnaissance shares only an already authorized trade's budget. Full coverage may
need multiple trades/sessions and sufficient quantity for partial cases; no negligible-cost or
consistency-impact claim is made. Its concrete budget and impact calculation precede separate
operator approval. The standing spend ceiling alone does not authorize the test sequence.

**Preserves.** No agent places a trade; the rail stays disarmed; no strategy signal is sent;
Packet 4's full qualification remains owed.

**Owner and ruling.** Attended release plan Packet 4 and TB-S3 lifecycle/evidence rows;
operator owns any live session. Proposed text: "Permit planning for early reconnaissance on a
separately authorized preservation trade; retain all unexercised lifecycle gates. Require a
separate bounded full-qualification plan before any added live trades; move its required
capability slice before dependent Packet 2 acceptance while permitting offline preparation."

**Window.** Reconnaissance at a compatible authorized trade window; full qualification after
P1's semantic matrix and the scenario/budget plan are accepted.

**Verification.** A coverage matrix records observed scenario, quantity, order type, close scope,
evidence class and digest. A one-contract market entry/full close leaves stop-entry, partial,
scoped-close and takeover cases unqualified. A TB-S3 capability row reaches SUPPORTED only when
all of its required cases meet the owner's evidence criteria; dependent Packet 2 slices remain
blocked otherwise. A route that cancels resting entries but leaves a protective child after
closure cannot receive SUPPORTED. No unobserved case inherits a command-level verdict.

---

## §3 — Not simplified

These stay as written; each has already paid for itself in this account's history or is a
governance invariant.

- Reserve before send; release capacity only on terminal broker evidence.
- Fail closed on any doubt for new risk.
- An explicit `armed_until` whenever armed and effective disarm before it expires.
- No agent places a trade; separate operator GO for spend, deployment and the arm.
- K=1, one attempt, failure terminal, no runner-up.
- Private evidence stays private; public records carry digests and verdict labels only.
- Frozen `dd_protection` constants; registry admission only through TB-E1 and TB-D0.
- Whole-leg Aegis takeover in D-B8 priority order (§1).

---

## §4 — Decision sheet

Rulings are ACCEPT, DEFER (with a wake condition) or REJECT (with the reason). Record each at
the owner as a dated addendum; update the Status column here afterwards. An accepted direction
does not make its dependent capability ready. The bounded tasks below close those dependencies;
this map neither executes them nor authorizes their live steps.

| # | Proposal | Owner to amend | Window | Depends on | Status |
|---|---|---|---|---|---|
| P1 | Static protection; per-port logic-exit timing | TB-S3/K2, TB-S2, TB-P1/F1 | before F1 | Execution matrix and replacement lifecycle qualification | PROPOSED; contract owed |
| P2 | One process | S2b ADR, M1 ADR, release plan Packet 2 | before Packet 2 wiring | — | PROPOSED |
| P3 | Signed initial GO off the image | TB-P2 §2b/§3, key-scope owner, TB-I3, TB-O1 | before TB-D2 | Signature utility, enrollment, qualification binding and durable one-use activation | PROPOSED; initial-only |
| P4 | Scheduled flatten survives a source fault | TB-S3 rev9 §1–§2, arming procedure | before Packet 2 halt slices | — | PROPOSED |
| P5 | Globally qualified initial-state envelope | TB-P2 T8/§4, TB-P1/F1, TB-T1 C10; P3 GO binding if accepted | before F1 | D-B4 ruling, coverage proofs and all-cells gate before n3 | PROPOSED; proof owed |
| P6 | Automated collection; conditional automatic acceptance | settlement contract, TB-S1 §3, settlement components | acceptance contract before authorization implementation | Complete history, authoritative equity and qualified finality/correction producer | PROPOSED; recommend DEFER automatic acceptance pending producer evidence |
| P7(a-consent) | Weekly consent | TB-P2/TB-S3/TB-I3, rail GO ADR | after ongoing contract acceptance | Current-state/restart/revocation contract; not P3 initial GO | Recommend DEFER |
| P7(a-disarm) | Effective automatic disarm | TB-I3 runtime/config owner, M1/arming procedure | after runtime transition qualification | Revocation, persistence, apply and acknowledgment; crash/in-flight cases | PROPOSED capability task |
| P7(b) | Quarterly calendar | Calendar owner/#396 | after coverage qualification | Source-backed rows, holiday mappings, digest ratification | Independently PROPOSED |
| P7(c) | Quarterly subscription review | Subscription owner, STATE, operational Rule 7, currency checker/tests | after coordinated cadence migration | Current real monthly trigger remains until migration | Independently PROPOSED |
| P8 | Data-only vendor; diligence now | Track A §3.2, umbrella O-4 | now | — | PROPOSED |
| P9 | Early reconnaissance; separate full qualification | release plan Packet 4, TB-S3 L2/K2 | compatible authorized trade; then bounded qualification plan | P1 semantic matrix for full qualification; separate live bounds/GO | PROPOSED; no full-coverage claim |

### Bounded work decomposition

| Task | Owner and deliverable | Prerequisite / decisive verification |
|---|---|---|
| Execution semantics (P1) | TB-S2/TB-S3: event matrix for trigger, update order, decision/fill time, price, captured scope, FIFO/protection ownership and feedback | Before F1; THIS_CLOSE/NEXT_OPEN gap, target-touch, exit/add and protection-allocation traces; baseline parity separate from overlay results |
| Route coverage (P9) | Packet 4-owned capability slice moved before dependent Packet 2 acceptance: case-to-evidence matrix and separately bounded live plan | Consumes execution matrix; offline Packet 2 work may proceed; reconnaissance cannot promote unobserved cases; quantity/order/exposure/spend/session bounds and recovery before live GO |
| Initial authorization (P3) | TB-P2/TB-I3: scoped envelope plus one-use request/boot/consumption lifecycle | Independent verifier allowed; test second boot before expiry, re-signing, concurrency and missing/restored consumption state; no ongoing authority |
| Ongoing authority (P7 a-consent) | TB-P2/TB-S3: later-session/current-state/restart/revocation contract | Separately ratified; initial S/no-activity acknowledgment cannot authorize another session; clean-session count is not acceptance |
| Effective disarm (P7 a-disarm) | TB-I3: live permission fence, durable config, apply/acknowledgment and restart behavior | Successful disk write with failed runtime apply must remain incomplete; test queued/in-flight work, expiry and every crash boundary |
| Cadence migration (P7 b/c) | Calendar coverage independently; Rule 7/STATE/checker/tests together for subscription cadence | Quarterly coverage never grants arm; run real checker against proposed STATE, retain weekly freshness and reject missing/stale cadence rows |
| Envelope qualification (P5) | TB-P1/F1/TB-P2: frozen predicates, proofs, budget and global verdict | Before any n3 result; all deployable cells covered; match P3 qualification variant without changing initial-only authority |
| Settled-close acceptance (P6) | Evidence/calculation/settlement owners: complete history, authoritative value and finality/correction producer | Preserve the approved component split; auto-acceptance waits on producer evidence, not signature utility or matching balances |
| Runtime consolidation/fault split (P2/P4) | S2b/TB-I3: scheduling, supervision and dispatch authority contract | Stalled evaluator/source-only outage versus unreadable safety state; apply retained schedule and intervention boundaries |

The coordinator integrates owner contracts and updates this decision map. Tasks sharing a
transition must be reviewed together before acceptance: execution semantics with route coverage,
and initial authorization with ongoing authority/disarm boundaries. Calendar work and signature
utility extraction can proceed independently. No owner contract or runtime is amended by this PR.

---

## §5 — Verification

```bash
# Link liveness for this note (strict: exit 1 on any dead relative link)
python scripts/check_md_relative_links.py --glob docs/notes/2026-09-15-tradeify-simplification-review.md --strict

# Audit EVERY local source-table row, not a sample (run from repository root).
python - <<'PY'
import re
import subprocess
from pathlib import Path

root = Path.cwd().resolve()
note = root / 'docs/notes/2026-09-15-tradeify-simplification-review.md'
source = note.read_text(encoding='utf-8').split('## §0 — Rule 0 reads', 1)[1]
source = source.split('Review correction source refresh', 1)[0]
checked, failures = 0, []
for row in source.splitlines():
    if not row.startswith('| ['):
        continue
    fields = row.split('|')
    targets = re.findall(r'\]\(([^)]+)\)', fields[1])
    local = [p.split('#', 1)[0] for p in targets if not p.startswith('https://')]
    if not local:  # PR references carry their own reviewed revision, outside the base.
        continue
    anchors = re.findall(r'`([0-9a-f]{7,40})`', fields[2])
    if len(local) != 1 or len(anchors) != 1:
        failures.append('Require one local source and one anchor per row: ' + fields[1])
        continue
    path = (note.parent / local[0]).resolve().relative_to(root).as_posix()
    actual = subprocess.check_output(
        ['git', 'log', '-1', '--format=%h', '242992b', '--', path], text=True).strip()
    checked += 1
    if not actual or actual != anchors[0]:
        failures.append(f'{path}: recorded {anchors[0]}, actual {actual or "ABSENT"}')
print(f'Source anchors: {checked} checked, {len(failures)} failures')
for failure in failures:
    print(failure)
raise SystemExit(1 if failures or not checked else 0)
PY

# Cited facts
grep -n '"6J": 10' ops/c1_rail/book_policy.py                                   # micro-equivalents
grep -n 'normal_base_values=(8,)' ops/c1_rail/book_policy.py                    # Aegis normal 8
grep -n 'command=closeposition\|command=place' ops/c1_rail/crosstrade_payload.py # existing primitives
grep -n 'Halt the whole book into INTERVENTION' docs/spec/2026-09-14-tb-s3-halt-resume-contract.md
grep -n 'mutable volume file' docs/adr/2026-09-12-tradeify-book-protection-instance-admission.md
git ls-tree -r --name-only bd41cb6 | grep ed25519_verify.py

# The exclusion is recorded once, here
grep -n 'Aegis takeover is a key part' docs/notes/2026-09-15-tradeify-simplification-review.md
```

Document validation checks provenance and links, not runtime readiness. Before an owner accepts
one of §4's tasks, its concrete counterexample traces and affected enforcement gates must pass
on the proposed implementation. This revision adds no runtime or live-route qualification.
