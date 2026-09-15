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
and umbrella O-4 · the per-session GO clause.

---

## §0 — Rule 0 reads

Anchors are `git log -1 --format=%h origin/main -- <path>` at `242992b`, read 2026-09-15.

| Source | Anchor | What it pins for this note |
|---|---|---|
| [TB-S3 rail extension spec](../spec/2026-09-12-c1-multi-leg-rail-extension-spec.md) | `6a282f1` | L2(c) per-bar AMEND; L2(f) ATTACH after Striker's bare entry bar; L2(g) native trails on ORB stop entries; takeover = cancel-confirm plus close-confirm of whole legs |
| [TB-S3 rev9 halt/resume](../spec/2026-09-14-tb-s3-halt-resume-contract.md) | `7c3ace8` | §1 an incident revokes NORMAL and SCHEDULED_EXIT; [§2](../spec/2026-09-14-tb-s3-halt-resume-contract.md#2-trigger-decisions) "source explicitly unhealthy" enters INTERVENTION; [§5](../spec/2026-09-14-tb-s3-halt-resume-contract.md#5-exact-schedule-rule) `D = min(16:00, V − 15)` |
| [S2b build ADR](../adr/2026-08-08-s2b-signal-daemon-build.md) | `7c3ace8` | §2 second Fly app, listener B1 unchanged; §4 limb 1 tears back a shared volume; O-4 feed deferral, option A′ shortlisted |
| [S2 fork ADR](../adr/2026-08-07-loop-s2-signal-host-fork.md) | `b448e2b` | Python-native origin; Pine is research/export only |
| [TB-P2 admission ADR](../adr/2026-09-12-tradeify-book-protection-instance-admission.md) | `55c9d96` | §2a T8 sole n3 bound to FBR and S; [§2b](../adr/2026-09-12-tradeify-book-protection-instance-admission.md#2b--the-deployment-go-artifact-and-the-go-reseal-definition) GO baked into image v2 with a layer-equality reseal; [§3](../adr/2026-09-12-tradeify-book-protection-instance-admission.md#3--alternatives-considered) rejects a volume GO on mutability |
| [TB-T1 seal contract](../spec/2026-09-12-tradeify-account-snapshot-seal-contract.md) | `a51d988` | C10 `valid_until`; no fill, order or adjustment between S and the arm |
| [Attended settlement contract](../spec/2026-09-15-tradeify-attended-settlement-contract.md) | `4f000c6` | operator-signed one-use 300 s challenge per accepted close; balance substitutes for equity only with flatness evidence at the same boundary |
| [TB-S1 protection/capacity spec](../spec/2026-09-12-tradeify-book-protection-capacity-spec.md) | `4f000c6` | [§3](../spec/2026-09-12-tradeify-book-protection-capacity-spec.md#3-settled-close-state-machine) settled-close state machine; [§4](../spec/2026-09-12-tradeify-book-protection-capacity-spec.md#4-capacity-and-reconciliation) 80-micro cap, refuse-never-clip, Aegis-only takeover |
| [TB-S2 replay spec](../spec/2026-09-12-tradeify-synchronized-replay-spec.md) | — | RC-4 fill model; RC-5 takeover modelled natively; RC-8 scheduled flatten as an operational overlay |
| [Attended release plan](../superpowers/plans/2026-09-14-tradeify-attended-release.md) | `1cdfafe` | Packets 0–6; [Packet 4](../superpowers/plans/2026-09-14-tradeify-attended-release.md#packet-4--qualify-the-actual-data-and-execution-route) qualifies the route after Packets 2–3 |
| [Packet 0 feasibility](2026-09-14-tradeify-attended-feasibility.md) | `7c3ace8` | [capability matrix](2026-09-14-tradeify-attended-feasibility.md#capability-to-consumer-matrix): E1/E2/E3 have no accepted producer; every L2 row unqualified; route capability named the largest uncertainty |
| [Track A plan §3.2](../superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md#32-a9--production-feed-verification-record-and-funding-checkpoint-added-2026-09-11) | `84216f3` | A9 vendor table; credential-boundary correction; six vendor questions "near the actual feed gate" |
| [M1 ADR](../adr/2026-07-22-c1-venue-native-monitoring-maturity.md) | `a3be3f4` | arm interlock; item 5 discharged 2026-09-14 |
| [Track B umbrella](../briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md) | `6a282f1` | [§0.8](../briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md#08--open-items-recorded-not-folded-owned-by-the-named-packet) O-4; wave gates; D-B4 K=1; D-B15 dry-run window |
| [Acceptance record](2026-09-10-tradeify-protection-selection.md) | `ea6d584` | selection evidence class; the Tradeify portfolio alias |
| [`ops/c1_rail/book_policy.py`](../../ops/c1_rail/book_policy.py) | `5b0dc5b` | `MICRO_EQUIVALENT` 6J=10; `BOOK_LEGS` Aegis normal base 8, priority 1 |
| [`ops/c1_rail/crosstrade_payload.py`](../../ops/c1_rail/crosstrade_payload.py) | `b448e2b` | existing commands: `place` with optional SL/TP, `closeposition`; no stop entry, no cancel |
| [`ops/c1_rail/c1_rail_arm.py`](../../ops/c1_rail/c1_rail_arm.py) | `b448e2b` | boot gate refuses a stale future `armed_until`; `--status` prints `dry_run` and `armed_until` |
| [`ops/c1_rail/c1_rail_listener.py`](../../ops/c1_rail/c1_rail_listener.py) | `7bf243c` | legacy exit/flat routing; book entry/add refusal without a halt store |
| [`ops/c1_signal_daemon/book_protocol.py`](../../ops/c1_signal_daemon/book_protocol.py) | `85a025e` | `BookStrategy.on_bar / on_execution / set_mode / checkpoint`; `BracketAmend` "re-issue the bracket every bar exactly as Pine re-calls" |
| [`core/firm_rules.py`](../../core/firm_rules.py) | `7369675` | `Tradeify_Select_100K`: EOD trailing drawdown, 80-micro aggregate cap, 40 % eval consistency gate |
| [`STATE.md`](../../STATE.md) · [`CLAUDE.md`](../../CLAUDE.md) | `84216f3` · `51609a4` | weekly operator trade; monthly subscription reconfirm; "every armed session needs its own GO"; disarm before `armed_until` |
| [PR #395](https://github.com/Joshua-Asante/first-passage/pull/395) head `f29ee06` (not on main) | — | `ops/c1_rail/ed25519_verify.py::verify`, `operator_keys.json`, `book_settlement.py`, `book_session_calendar.py` |

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

Each proposal states the current choice with its source, the simpler choice, what it removes,
what it costs, what it preserves, the owner and the ruling asked for, the window in which the
change is still cheap, and how acceptance would be verified. Numbering P1–P9 is this note's;
the conversation's item 1 was the excluded proposal in §1.

### P1 — Static broker-side protection at entry; logic exits as bar-close market orders

**Current.** The ports reproduce Pine's per-bar `strategy.exit` re-call at the broker. Striker
enters bare and attaches protection one bar later (ATTACH, L2(f)); every leg re-issues its exit
levels each closed bar (AMEND, L2(c)); ORB carries native trailing brackets on stop entries
(L2(g)). None of (c), (f) or (g) has an accepted route producer.

**Proposed.** Every entry and add carries one static stop, and a target where the port defines
one, attached at fill using the `stop_dist_pts` the B1 payload already carries. Trail and all
other exit logic stays in the Python port. When a completed bar crosses the port's exit level,
the daemon emits `exit` or `flat` and the listener sends a market close. The broker never
receives an amend or a late attach. The live mutation set becomes: stop or market `place` with an
attached static bracket, scoped or full `closeposition`, and `cancel` of a working order.

**Removes.** L2(c), L2(f) and L2(g) from the capability rows; the protection-gap class (a lot
bare for a bar; an amend racing a fill); per-bar broker traffic; sibling exit orders carrying
independent trailing state.

**Costs.** Trail exits fill at the next bar's open plus slippage instead of intrabar at the
level, bounded above by the static stop. Striker's first bar becomes protected where Pine leaves
it bare, a deliberate safety-side deviation. Book semantics change, so this is a pre-registered
operational overlay in the same class as RC-8: parity to the exports remains the proof of the
port, the overlay applies after it, and scheduler-affected ledgers and parity are regenerated
before TB-F1.

**Preserves.** Takeover (cancel and close are in the set); reserve before send; release on
terminal evidence only; every leg's entry logic.

**Owner and ruling.** TB-S3 (primitive set and L2 rows), TB-S2 (RC-4 overlay), TB-P1/TB-F1
(freeze). Proposed text: "Adopt {stop or market place with attached static bracket, scoped or
full close, cancel working order} as the only live mutations. Trail logic exits at bar close as a
pre-registered operational overlay. Regenerate affected replay evidence before F1."

**Window.** Before TB-F1 freezes.

**Verification.** The TB-S3 L2 table lists only place-with-bracket, close and cancel; no AMEND or
ATTACH action reaches the listener from `book_protocol`; the regenerated ledgers carry the overlay
digest inside FBR.

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

**Removes.** The barrier and watchdog as distributed-failure handlers; the source-health
authentication protocol; daemon-loss recovery; one always-on machine and its volume; the B1
listener client on the strategy path.

**Costs.** Supersedes S2b §2 "Second Fly app" and reinterprets §4 limb 1, so it needs a
superseding ADR or dated revision. M1 acceptance pins are image-bound, so a merged image needs
pin re-verification or a re-bake; whether a new attended ceremony is owed is the M1 owner's call.
The daemon's `GET /` health merges into the listener's.

**Preserves.** Fail-closed on a stale source; listener-owned permission, now module-owned; the
B1 field contract for any external client.

**Owner and ruling.** S2b build ADR §2 and §4; S2 fork ADR unchanged (the origin is still
Python); M1 ADR (pins); attended release plan Packet 2 (wiring). Proposed text: "Packet 2 wires
the evaluation loop into the listener process; the second app is retired when the merged image
passes M1 pin verification."

**Window.** Before Packet 2 wires daemon to listener. After that the split is effectively
permanent.

**Verification.** One app under `deploy/`; no `listener_client` POST on the strategy path;
source health is in-process state rather than an authenticated report.

### P3 — Sign the deployment GO; keep it off the image

**Current.** TB-P2 §2b bakes the GO artifact into image v2 through an artifact-only commit, then
proves every non-GO layer digest identical to v1 and reseals EF2; R1c voids on any deviation. §3
rejected a volume-resident GO because "a mutable volume file lets the gate be satisfied by editing
the thing being gated on."

**Proposed.** The GO is a signed envelope over the v1 image digest, FBR, EF1, the seal digest S,
the n3 result digest, `valid_until`, the operator identity and the recording time, produced with
the operator signing key introduced for settlement and verified in-image by
`ed25519_verify.verify` against a public key baked into v1. The envelope rests on the volume or is
supplied at arm time. Forging it requires the private key, so mutability no longer satisfies the
gate. `--arm` refuses on a missing or invalid signature, a digest that does not match the running
image, or an expired `valid_until`.

**Removes.** Image v2, the artifact-only commit, EF2, the layer-by-layer manifest equality proof,
the image half of R1c, and a rebuild inside the seal window.

**Costs.** Key custody becomes load-bearing, which settlement already made true. The public key
is pinned in the image, so key rotation means a new image, the same as today's pins. Depends on
the verifier landing through PR #395.

**Preserves.** n3 bound to FBR and S; B7; every other T-stage; GO never written on a failed
qualification.

**Owner and ruling.** TB-P2 §2b and §3 (dated revision); `c1_rail_arm.py` interlock; TB-O1
procedure. Proposed text: "The deployment GO is a signed envelope verified in-image; the B7 image
is the release image; the reseal proof is retired."

**Window.** Any time before TB-D2; cleanest before Packet 6.

**Verification.** `test -f docs/notes/rail_build/DEPLOYMENT_GO.json` is no longer part of the
arm gate; arm tests refuse unsigned, foreign-key and expired envelopes; the procedure has no image
rebuild between B7 and the arm.

### P4 — Scheduled flatten survives a source fault

**Current.** Rev9 §2 routes "required source explicitly unhealthy, control read fails, or bar
barrier expires" into INTERVENTION, and §1 says INTERVENTION revokes SCHEDULED_EXIT. A feed
outage near the close therefore leaves own-flat to the operator.

**Proposed.** Split the incident classes. SOURCE_FAULT (stale or unhealthy source, expired
barrier, missing control read) halts new risk and keeps SCHEDULED_EXIT: the cutoff cancels and the
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

**Proposed.** TB-F1 pre-registers an initial-state grid: starting drawdown from peak in fixed
steps from zero to the trigger plus a margin, both mode states, and the carried-peak convention.
TB-E1 runs the four n3 conditions per cell on the frozen n3 stream within the frozen budget.
TB-E2 becomes: capture S, verify the live state lies inside a passing cell, seal. No replay runs
at arm time.

**Removes.** The seal-validity race; the sole-n3 timing constraint; the interaction with the
weekly trade; the replay half of R1c.

**Costs.** Compute multiplied by cells inside the frozen budget. Under D-B4 this is one
pre-registered attempt with a larger frozen contract, not an extra sample, but the operator must
rule that reading. A live state outside every passing cell is BLOCKED, never a new draw.

**Preserves.** The fresh-stream property (the grid runs on the n3 stream); one attempt; failure
terminal; the row admitted only after TB-E1.

**Owner and ruling.** TB-P2 §2a T8 and §4 H; TB-P1/TB-F1 contract; TB-T1 C10 (the seal binds
envelope membership, not a result). Proposed text: "TB-E2 is an envelope-membership check on the
sealed live state against the pre-registered cells passed in TB-E1; no arm-time replay."

**Window.** Before TB-F1.

**Verification.** The F1 contract lists the grid and per-cell verdict fields; the TB-E2 record
shows a membership check and no replay; C10 no longer voids a "dependent n3 result".

### P6 — Automated settled-close producer; attestation only on disagreement

**Current.** The settlement contract approved 2026-09-15 requires an operator-signed one-use
challenge for every accepted close; missing or stale evidence blocks the next session. The rail
already reads net liquidation through the configured CrossTrade equity source.

**Proposed.** After RC-8 own-flat is confirmed and the account day has closed, the settlement
owner reads net liquidation from the existing equity source and the captured Tradeify dashboard
balance and threshold, requires flatness evidence at that boundary from the reconciled state, and
accepts the close automatically when the two balances agree within a frozen dollar tolerance and
the mode decision is identical under both values. The signed challenge is required only when the
tolerance is exceeded, a source is missing or stale, flatness is unproven, or a correction or
revision arrives.

**Removes.** The daily ceremony on ordinary days; the "missed attestation blocks tomorrow"
stoppage class.

**Costs.** The tolerance becomes a frozen F1 parameter. The dashboard capture still needs an
automated or attended source; where none exists, P6 reduces to attestation on those days. B7's
initial-peak derivation is unchanged (D23).

**Preserves.** The single-writer chain; duplicate and out-of-order halts; never backdating; mode
selected once per session; a block on disagreement.

**Owner and ruling.** Attended settlement contract (dated amendment); TB-S1 §3;
`book_settlement.py` on PR #395. Proposed text: "A settled close is auto-accepted when the
equity-source and dashboard balances agree within the frozen tolerance with flatness evidence at
the boundary; the signed challenge is the escalation path, not the daily path."

**Window.** Before Packet 5; cheapest while PR #395's Step 5 is under review.

**Verification.** Settlement tests cover auto-accept within tolerance, refusal beyond it, refusal
without flatness, and escalation to the signed challenge; the integration scenario consumes no
challenge on a clean day.

### P7 — Collapse standing operator obligations

**Current, all documented.** A daily signed close (P6's target); a per-session arm GO ("every
armed session needs its own GO"); disarm before `armed_until`; a monthly session-calendar
extension with operator digest ratification where missing or expired rows refuse risk (PR #395
Step 4 covers 2026-09-03 to 2026-09-30); a monthly subscription reconfirm; the weekly
preservation trade, which strategy fills discharge once the book trades; incident attendance.

**Proposed.** (a) After the first N attended sessions with clean reconciliation, N frozen in the
procedure, a standing weekly GO arms a bounded window with an explicit `armed_until`; each day
the listener writes disarm through the config owner at own-flat confirmation, and the next day's
activation needs only the fresh boot, identity and no-activity checks rather than a new GO.
(b) The calendar horizon becomes three months, authored and ratified once a quarter, with the
missing-coverage refusal retained. (c) The subscription reconfirm folds into that quarterly
ratification.

**Removes.** Most scheduled human stoppages; the manual daily disarm step (the boot gate already
refuses a stale future `armed_until`, so the crash-loop cause is fixed).

**Costs.** Amends the posture line and the rail GO ADR's per-session GO, an operator authority
choice. A quarter-long calendar needs source-backed early-close rows for the horizon.

**Preserves.** An explicit `armed_until` at all times; fresh activation checks each day;
incident attendance; no agent trade.

**Owner and ruling.** Rail GO ADR (per-session GO clause); M1 ADR arm interlock; `CLAUDE.md`
posture mirror; calendar owner on PR #395; STATE monthly rows. Proposed text: "(b) and (c) now;
(a) after N clean attended sessions, with N and the auto-disarm step written into the arming
procedure in advance."

**Window.** (b) and (c) now; (a) ruled now, effective after the initial sessions.

**Verification.** STATE's forward triggers show one quarterly row in place of two monthly ones;
the arming procedure has a standing-GO stage with N and the auto-disarm step; arm tests cover
auto-disarm at own-flat.

### P8 — Data-only feed vendor; send vendor diligence now

**Current.** O-4 is deferred. Option A′, a personal live Tradovate data account with parked
capital and a brokerage-backed secret, is shortlisted. Data-only vendors are marked "safe
fallback, not cost leader" because their run-rate equals the retired Databento plan. The six
vendor questions are to be sent "near the actual feed gate."

**Proposed.** Send the six questions to every shortlist candidate now, at zero spend, since
answers take weeks. Amend the decision rule so a data-only credential is preferred at equal
capability and a run-rate matching a retired plan is not a disqualifier. Funding still waits for
the checkpoint.

**Removes.** Vendor lead time from behind the qualification gates; a credential able to place
orders on the data path.

**Costs.** None now. The run-rate against A′ remains the operator's call at the checkpoint.

**Preserves.** No signup or spend before the checkpoint; TB-I5 equivalence; the provider-neutral
`BarSource` contract.

**Owner and ruling.** Track A plan §3.2 (decision rule and timing); umbrella O-4; the S2b §2 row
at selection. Proposed text: "Vendor diligence is decoupled from the funding checkpoint and starts
now; the decision rule prefers a data-only credential at equal capability."

**Window.** Now.

**Verification.** The Track A plan carries a dated record of questions sent and answers received
per vendor; the decision-rule text is amended.

### P9 — Front-load a bounded route spike using the reduced primitive set

**Current.** Packet 4 qualifies the route after Packets 2 and 3, and the feasibility record names
route capability the largest uncertainty. Canned payloads have filled on this account before, and
the operator already places one venue-required trade each week.

**Proposed.** Before Packet 2 completes, a separately authorized, operator-executed spike on the
incumbent eval at minimum size exercises exactly P1's set: stop and market `place` with an
attached bracket, including partial-fill and rejection observation; scoped and full
`closeposition`; `cancel` of a resting stop entry; and read-back of order-level evidence through
CrossTrade's history and lifecycle endpoints. Where the venue allows, the weekly preservation
trade is the vehicle, so no trades are added. Each primitive returns SUPPORTED, UNSUPPORTED or
AMBIGUOUS with evidence digests. UNSUPPORTED on a required primitive stops Packet 2's dependent
slices and routes to a concrete alternate contract under the plan's "only if capability fails"
checkpoint.

**Removes.** Building Packets 2 and 3 around a fence the route cannot provide; the ordering that
tests the invalidating assumption last.

**Costs.** A few dollars of commission and slippage inside the spend ceiling; one attended
operator session. The operator confirms the effect on the eval's 40 % consistency gate is
negligible at minimum size.

**Preserves.** No agent places a trade; the rail stays disarmed; no strategy signal is sent;
Packet 4's full qualification remains owed.

**Owner and ruling.** Attended release plan (a bounded slice of Packet 4 moves ahead of Packet
2's acceptance); TB-S3 L2 rows receive the verdicts; a separate operator GO for the session.
Proposed text: "A bounded route spike on P1's primitive set precedes Packet 2 acceptance; its
per-primitive verdicts are recorded in TB-S3's L2 rows."

**Window.** The next weekly trade window after P1 is ruled.

**Verification.** A dated evidence record with per-primitive verdicts and digests; TB-S3 L2 rows
move from unqualified to the observed verdict; Packet 2 slice gates cite it.

---

## §3 — Not simplified

These stay as written; each has already paid for itself in this account's history or is a
governance invariant.

- Reserve before send; release capacity only on terminal broker evidence.
- Fail closed on any doubt for new risk.
- An explicit `armed_until` at all times and disarm before it expires.
- No agent places a trade; separate operator GO for spend, deployment and the arm.
- K=1, one attempt, failure terminal, no runner-up.
- Private evidence stays private; public records carry digests and verdict labels only.
- Frozen `dd_protection` constants; registry admission only through TB-E1 and TB-D0.
- Whole-leg Aegis takeover in D-B8 priority order (§1).

---

## §4 — Decision sheet

Rulings are ACCEPT, DEFER (with a wake condition) or REJECT (with the reason). Record each at
the owner as a dated addendum; update the Status column here afterwards.

| # | Proposal | Owner to amend | Window | Depends on | Status |
|---|---|---|---|---|---|
| P1 | Static protection at entry; bar-close logic exits | TB-S3, TB-S2, TB-P1/F1 | before F1 | — | PROPOSED |
| P2 | One process | S2b ADR, M1 ADR, release plan Packet 2 | before Packet 2 wiring | — | PROPOSED |
| P3 | Signed GO off the image | TB-P2 §2b/§3, `c1_rail_arm.py`, TB-O1 | before TB-D2 | PR #395 verifier merged | PROPOSED |
| P4 | Scheduled flatten survives a source fault | TB-S3 rev9 §1–§2, arming procedure | before Packet 2 halt slices | — | PROPOSED |
| P5 | Initial-state envelope replaces sole n3 | TB-P2 T8/§4, TB-P1/F1, TB-T1 C10 | before F1 | D-B4 reading | PROPOSED |
| P6 | Automated settled close; attest on disagreement | settlement contract, TB-S1 §3, `book_settlement.py` | before Packet 5 | PR #395 Step 5 | PROPOSED |
| P7 | Collapse standing obligations | rail GO ADR, M1 ADR, CLAUDE.md mirror, calendar owner, STATE | (b),(c) now; (a) after N sessions | P6 | PROPOSED |
| P8 | Data-only vendor; diligence now | Track A §3.2, umbrella O-4 | now | — | PROPOSED |
| P9 | Front-loaded route spike | release plan Packet 4 slice, TB-S3 L2 | next weekly trade after P1 | P1 ruling | PROPOSED |

Ordering that follows from the dependencies: rule P1 first, because P9 tests its primitive set;
rule P2 before any Packet 2 wiring lands; P3 and P6 wait on PR #395; P5 needs the D-B4 reading
stated in the same ruling.

---

## §5 — Verification

```bash
# Link liveness for this note (strict: exit 1 on any dead relative link)
python scripts/check_md_relative_links.py --glob docs/notes/2026-09-15-tradeify-simplification-review.md --strict

# §0 anchors reproduce at the recorded base
git log -1 --format=%h origin/main -- docs/spec/2026-09-14-tb-s3-halt-resume-contract.md     # 7c3ace8
git log -1 --format=%h origin/main -- docs/adr/2026-09-12-tradeify-book-protection-instance-admission.md   # 55c9d96
git log -1 --format=%h origin/main -- ops/c1_rail/book_policy.py                                # 5b0dc5b

# Cited facts
grep -n '"6J": 10' ops/c1_rail/book_policy.py                                   # micro-equivalents
grep -n 'normal_base_values=(8,)' ops/c1_rail/book_policy.py                    # Aegis normal 8
grep -n 'command=closeposition\|command=place' ops/c1_rail/crosstrade_payload.py # existing primitives
grep -n 'Halt the whole book into INTERVENTION' docs/spec/2026-09-14-tb-s3-halt-resume-contract.md
grep -n 'mutable volume file' docs/adr/2026-09-12-tradeify-book-protection-instance-admission.md
git ls-tree -r --name-only origin/claude/pr-394-tradeify-deployment-d9ee8c | grep ed25519_verify.py

# The exclusion is recorded once, here
grep -n 'Aegis takeover is a key part' docs/notes/2026-09-15-tradeify-simplification-review.md
```
