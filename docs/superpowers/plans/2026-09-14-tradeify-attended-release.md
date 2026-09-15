# Tradeify Attended Release Execution Plan

> **For agentic workers:** Joshua authorized Packet 0 by directing “execute the first slice” after review, then authorized its commit/push and Packet 1 with “commit, push and continue to the next slice.” Execute Packet 1 using superpowers:executing-plans; later packets and operational actions retain their gates. Preserve one coordinator-owned contract and combined acceptance. Independent review follows the requesting-code-review skill.

**Goal:** Qualify and deploy the fixed four-leg Tradeify portfolio with durable execution controls, broker observations and operator-owned incident recovery.

**Architecture:** The Python daemon synchronizes strategy decisions; the listener alone authorizes and serializes broker dispatch. On an incident, the listener durably stops further automated order changes and retains outstanding requests. Joshua manages exposure through the trading platform. Observations support diagnosis; separately verified reconciliation and fresh authenticated approval are required to resume.

**Tech Stack:** Existing Python rail/daemon, shared book components, SQLite journals, Fly deployment, CrossTrade/Tradovate observation collector, a small recovery interface and one notification integration.

**Spec:** The section 2 design is now frozen in [TB-S3 rev9](../../spec/2026-09-14-tb-s3-halt-resume-contract.md), the authoritative contract. Section 2 below preserves the reviewed design; consult rev9 for its exact reconciled semantics, including provider-side actors. Retained authorities: TB-S1/TB-S2/TB-S3, TB-P2 and its dated ratification, Track B umbrella and final-validation preregistration.

**Review status:** PACKET 0 COMPLETE — contract frozen, feasibility assessed and independently accepted after corrections. Approval, checks and release blockers are recorded in [Packet 0 evidence](../../notes/2026-09-14-tradeify-attended-feasibility.md). No later implementation, merge or live GO is implied.

## 1. Ground truth and constraints

Planning reads used local `origin/main` at `089f0a0765d1dd011f05c6a1ae0253ab2e44297a` and the newer `.worktrees/stage2-runtime-owner` at `39f47682208b21c28dd7abda9baac73e99e6be6b`. The primary checkout is `133f043`; do not implement from it or overwrite its untracked work. Remote currency and live host state were not checked in this planning task.

Production reads: `book_policy.py`, `book_sizing_context.py`, `book_capacity.py`, `book_recovery.py`, handler boot/routing, `book_protocol.py`, observer collector and README; historical `core/dd_protection.py` was read earlier in this task. Governing reads include rev8, current four-stage plan, recovery-owner design, observer design/probe and STATE.

| Item | Evidence-backed starting point | Remaining boundary |
|---|---|---|
| M1/A7/A8 | Recorded complete and disarmed deployment accepted | Preserve acceptance; do not reopen the completed ceremony. It does not establish four-leg readiness. |
| Shared policy/sizing/capacity/fingerprint | Bounded TB-I1 accepted; real pure functions exist | Need trusted producers, durable orchestration and actual dispatch/feedback integration. A sizing decision is not send permission. |
| Recovery owner | Durable scopes, operations, attempts and account serialization implemented in newer worktree | Production recovery sender and resume API absent. Confirm branch integration/review disposition before reuse. |
| Collector | Real read-only collection and revision retention exist | E1/E2/E3 remain unproven; collection completion is not recovery completion. |
| Seven bundles | Latest intake record: collected 7/7, accepted 0/7 | Verify private bodies and intake record before asserting any later progress; perform acceptance and parity. |
| Data source | Unselected; funding deferred to source-independent gates | Provider-neutral preparation may proceed; selection/spend/connection retain their checkpoint. |
| Calendar, settlement, full book and release | Interfaces/plans exist | Accepted producers and combined qualification remain necessary. |

Global constraints:

- Fixed book: Aegis 6J, Striker MYM p250, Vanguard MGC, ORB MNQ. No replacement book or parameter search.
- Preserve accepted per-leg quantity, lifecycle, capacity and protection laws. Reuse `entry_quantities`, `add_quantity`, `size_book_request` and `apply_event`; do not independently reimplement them in replay/UI/daemon.
- Candidate policy remains separate from historical `dd_protection.py`; policy registry admission remains TB-D0 after TB-E1. Positive production bindings follow TB-V1.
- Preserve single-process qualification, frozen streams/sizes/criteria, both required P2 decisions and the sole final n3. No opportunistic replacement samples.
- No agent places trades. Joshua retains merge decisions, funding/provider selection, separately authorized live ceremonies, deployment GO and each armed-session GO.
- Private Pine/ports, vendor exports, credentials and account evidence remain in approved ignored roots. Public artifacts contain permitted identities/digests/verdicts only.
- Preserve the recorded support-free continuation: use documented capabilities and authorized observations; no provider contact is part of this plan.
- One runtime integration owner: the coordinating agent. Independent review is required at material integration boundaries; separate contributor work does not prove combined acceptance.

## 2. Reviewed attended design — frozen in TB-S3 rev9

### 2.1 Scope and attendance

Joshua explicitly accepts attendance for each bounded armed session, has access to the trading platform, and verifies the alert path before arming. Attendance lasts until the account and outstanding requests are reconciled and the runtime is disarmed, including an incident beyond the intended session end. To leave early, stop new risk and complete the intervention/disarm procedure first.

Target acknowledgment is under 60 seconds after notification. This is an operating target, not a guaranteed loss bound or proof of receipt. Record incident detection, notification attempts/provider acceptance, any available delivery evidence, and acknowledgment separately. At 60 seconds after the first notification attempt without acknowledgment, escalate through the configured alternate channel; delivery failure alerts immediately through remaining channels. Failure to acknowledge never restores automation or authorizes emergency sends.

No continuous operator-presence detection is claimed. Local browser/desktop connectivity alone does not establish attendance. Missed runtime heartbeat monitoring is external to the trading host.

### 2.2 Normal operation versus incident intervention

Normal qualified strategy execution retains entries, adds, exits, required protection handling, accepted Aegis takeover and the ratified scheduled cutoff/flatten overlay. These features require their actual route semantics to qualify. Dropping any of them would be a book/execution-contract change, not an implementation shortcut.

**Approved change from rev8:** an incident stops new runtime broker mutations, including automatic emergency cancel/close, late strategy exits and protective amendments. The listener publishes HALTED and intervention-required ownership durably and fences all future sends, not merely entry/add. Existing broker-resident orders may still execute; they are displayed as live obligations. Previously transmitted or ambiguous requests remain owned and are never blindly retried. Joshua handles cancellation/closure in the platform. Provider-managed work is outside the local fence and requires separate intervention/quiescence evidence, as clarified in rev9.

This replaces rev8's general incident-triggered automatic flatten obligation with attended intervention. It does not cancel existing protective orders or promise flatness. The normal scheduled flatten remains automatic under its narrow schedule authority until an incident or manual takeover revokes that authority. A normal entry cutoff is distinct from an incident even though both deny new risk.

Operator stop, unexpected restart, source/account-evidence failure, unknown request outcome, protection fault, identity fault, storage fault and unscheduled authorization expiry enter attended intervention. Preserve rev8's detector thresholds and calendar formulas; do not replace them with new guessed timeouts. Expiry at the scheduled cutoff retains rev8's scheduled sequence. Ordinary sizing/capacity/recognized-duplicate refusals remain request-level refusals.

If a fault arrives during transport, serialize the transition against the active send. The UI may say “intervention requested; fence not confirmed” until the local sender is fenced. Transport must be bounded; an unresponsive process is handled by the operator runbook, not a stolen lock or a false fence acknowledgment. A confirmed local fence means no further local sends, not that earlier remote requests cannot execute. Urgent operator intervention remains possible while the display retains this uncertainty.

### 2.3 State, ownership and acknowledgment

Keep the listener-owned permission state HALTED/RUNNING. Keep incident attendance and dispatch ownership separate from permission; HALTED does not mean flat or no pending orders.

| Event | Durable result | Permitted runtime activity |
|---|---|---|
| Initial boot/restart | HALTED; original obligations retained; new boot/generation invalidates prior authority | Read observations, alert and verify; no broker mutations |
| Healthy, approved session | RUNNING with bounded authorization | Qualified normal strategy operations under existing controls |
| Scheduled cutoff | HALTED for new risk; narrow scheduled-exit authority retained | Qualified cancellation/exit/flatten per schedule, unless incident/manual intervention occurs |
| Incident/manual intervention request | HALTED; intervention-required; all automatic send authority revoked | Observe, alert, record; already-sent requests remain unresolved until proved otherwise |
| Own-flat deadline breach / calendar becomes invalid while active | HALTED; INTERVENTION revokes scheduled-exit authority; original attempts retained | Observe/alert for manual recovery; no further scheduled sends |
| Acknowledge | Attendance identity/time appended | Same observation-only incident posture |
| Reconciliation accepted | Reconciliation evidence recorded; ordinary disarm write/readback completed | Remain HALTED |
| Fresh valid resume request | One-use authorization and activation acknowledgment durably recorded | Next eligible complete bar only; never replay halted-period intents |

Status reads do not advance the state machine. Repeated reports/acknowledgments are idempotent; conflicting identities are rejected. Failed durable writes stop sends; independent monitoring covers inability to persist an incident.

### 2.4 Evidence and resumption

Retain rev8's evidence standard for release of uncertainty and resumption: complete account scope, zero gross positions, no working/protective orphan orders, no unresolved requests and accounted-for relevant history, with fresh causal coverage after the last potentially effective request/intervention. Retain the E1/E2/E3 obligations until an explicitly reviewed alternative replaces a particular obligation.

The collector is an observation producer only. Repeated empty reads, end of pagination, elapsed time, local sequence numbers, screenshots and operator acknowledgment do not become proof that an old request cannot still execute. Operator intervention records describe actions; the accepted evidence verifier establishes their consequences.

**Capability gate:** before implementing production resume, identify an actually available producer for every required fact. If the documented route cannot provide the necessary evidence, resume stays unavailable and live-release readiness remains blocked. Any alternative protocol must name how it resolves old requests and account completeness, carry executable/route evidence, and return as a concrete amendment for review. This plan does not authorize an operator checkbox to waive uncertainty.

Same-session resume remains possible only when the retained gates are satisfied. The authenticated request binds account, boot, halt generation, evidence digest, image/config/policy/active-leg/calendar identities, session and expiry. Expiry cannot exceed the cutoff. Concurrent halt wins. Restored connectivity, observed flatness, acknowledgment, midnight or restart never rearm. Initial activation still follows B7 -> n3 -> GO/reseal -> fresh activation acknowledgment.

### 2.5 Interface and alerts

Build a small incident console: permission, reason/time, local fence status, observation age/limitations, positions/orders as observed, uncertain requests, attendance, intervention notes and resume eligibility with blocking reasons. Provide separate authenticated acknowledge and resume controls. It is not an order-entry terminal.

Desktop alarm and mobile channels refer to the same incident identity. Use a durable notification outbox separate from dispatch authority; notification retries cannot produce broker sends or duplicate incident ownership. Better Stack is a candidate, not a selection. Freeze provider-specific delivery/escalation and external heartbeat thresholds after documented capability review and measured drills, before operational acceptance.

### 2.6 Amendment footprint

After approval, reconcile rev8 sections 1–4/7, retained S3 recovery clauses, S2b fault-report addendum, ARMING_PROCEDURE, Stage 2 acceptance and replay incident tests. Preserve rev8 section 5's schedule formula and P2 economics/admission rules. Explicitly describe the new human-response dependency; do not present unchanged outage guarantees. Record which old automated-recovery tests become deferred and which invariants remain mandatory. Normal close/protection/takeover tests stay required.

## 3. Execution order and review gates

This is a gated program plan. Fully design the next independently deliverable slice once its producers and base are known; do not fabricate production APIs for missing broker guarantees. The first slice below is contract/feasibility work. Later rows give concrete outcomes, dependency gates and acceptance cases; code-level plans are written against their execution revisions.

### Packet 0 — Freeze the amendment and prove feasibility

**Outcome:** approved attended semantics, one current integration baseline and an evidence-to-capability matrix with an explicit READY/BLOCKED release verdict.

**Files:** this document; `docs/spec/2026-09-14-tb-s3-halt-resume-contract.md`; `docs/spec/2026-09-12-c1-multi-leg-rail-extension-spec.md`; dated S2b addendum; `docs/notes/rail_build/ARMING_PROCEDURE.md`; existing Stage 2 plan; `docs/notes/2026-09-14-crosstrade-evidence-capability-probe.md`.

- [x] Record Joshua's review and exact approved changes; preserve existing ratifications rather than reopening them.
- [x] Refresh remote and create isolated `codex/tradeify-attended-release` at `089f0a0`. Inventory the five newer recovery/observer commits and bounded review records. No corresponding PR/main integration exists; record the dependency for its normal merge path rather than importing runtime code into this documentation slice. Private roots/other worktrees remain untouched.
- [x] Map every required normal broker primitive and E1/E2/E3 fact to actual/candidate producer, documented/observed evidence, limitation, consumer and acceptance case. Reuse the probe; no fresh authenticated reads.
- [x] Trace entry/incident, scheduled-close/incident, manual intervention during UNKNOWN and restart. Identify that the legacy bypass is fixed on `0141441` but not main; require that existing fix in the eventual runtime integration.
- [x] Publish deltas and READY for source-independent work / BLOCKED for live release and production resume, including provider-side actors.
- [x] Independent review accepted the amendment/matrix after clarifying deadline/calendar transition ownership and correcting two labels. No guarantee was weakened. Actual E1–E3/provider-side gaps remain live-release blocks; no runtime implementation began.

**Acceptance:** every transition in section 2 has an owner, persisted record, confirmed outcome or explicit unresolved block. No notification, observation or attestation is incorrectly promoted to execution evidence.

### Packet 1 — Accept the seven bundles and shared session inputs

**Execution checkpoint:** [intake progress and bounded emulator correction](../../notes/2026-09-15-tradeify-packet1-intake-progress.md). Corrected O-N collected under Joshua's decision to preserve the pinned source; seven diagnostic comparisons match. Formal admission/shared-law parity and calendar/settlement acceptance remain open.

**Outcome:** admitted strategy inputs and a common source-backed calendar/settlement contract suitable for replay and runtime consumers.

**Files/components:** existing seven-bundle intake ledger/interface proposal; private parity harness and pinned ports; `ops/c1_signal_daemon/book_protocol.py`; TB-C1 calendar/overlay artifacts under `ops/calendars/`; TB-T1 snapshot/sealer consumers; `book_sizing_context.py`.

- [ ] Verify existing bundle bodies/digests, Inputs/Properties, normalization, dates and warm-up. Ask Joshua only for precisely identified deficient evidence; do not recollect all seven by default.
- [ ] Run required protected/lifecycle parity and ORB adds-off cases against the shared quantity law. Retain source-parity verdicts separately from schedule-overlay replay differences.
- [ ] Freeze calendar provenance, session IDs, cutoff/flatten/deadline rows, closure overlays and settled-close identity/freshness. Supply a named authenticated settlement producer; an operator-assisted producer is acceptable only under the reviewed seal contract.
- [ ] Test early closes, DST, missing coverage, duplicate/out-of-order settlement and stale seals. Ensure missing inputs refuse permission rather than select a default mode/session.

**Acceptance:** seven accepted bundles and all required mode/quantity parity PASS; source-backed schedule and accepted settlement interface. Calendar data is reverified from official sources at execution, not assumed from policy examples.

### Packet 2 — One complete offline four-leg execution path

**Outcome:** completed bars -> all four adapters -> deterministic barrier -> shared sizing/capacity -> durable simulated dispatch -> confirmed feedback -> checkpoints, with schedule and incident semantics integrated.

**Existing interfaces:** `BookStrategy.on_bar(bar)`, `set_mode(mode)`, `on_execution(event)`, `checkpoint()`; `size_book_request(request, *, context, binding, policy, now)`; `book_capacity.apply_event` and `project_capacity`. Preserve exact types at execution. `ExecutionEvent` means confirmed outcome, not HTTP acceptance.

**Files/components:** daemon/feed/barrier and registry; `book_protocol.py`; shared policy/context/capacity/fingerprint; listener/HTTP handler; persistent halt/account lock/recovery modules; synchronized replay engine and private ports. Add focused integration suites under `tests/ops/`.

- [ ] Define the production account-owner event boundary with boot/generation, operation/attempt IDs, fact provenance and reservation state before writing dispatch code.
- [ ] Write and observe failing cross-boundary cases; implement durable reserve-before-send and fill/terminal accounting through real components with a labeled synthetic broker.
- [ ] Route every automatic order mutation through the same owner, including legacy exit/flat, scheduled closure, amendments and takeover. No independent sender survives the intervention fence.
- [ ] Persist adapter checkpoints and confirmed feedback coherently. Rebuild after restart while HALTED; discard obsolete intents, never blindly resend.
- [ ] Apply the common schedule in continuous replay, including close feedback, costs, capacity conflict ordering and deadline failures. Verify scheduler-affected results before F1.

**Acceptance cases:** same-bar conflicting signals are independent of arrival order; partial base fill sizes adds from confirmed base; cancel/fill race retains capacity; only terminal evidence releases reservations; protected ORB resting adds block transition until resolved; ordinary refusal is not an incident; stale source halts the whole book; restart at each dispatch boundary preserves uncertainty; status reads are pure; incident during normal/scheduled close prevents subsequent local mutations.

**Boundary:** this packet proves integrated implementation using synthetic broker facts. It cannot close route capability or resume evidence gaps.

### Packet 3 — Freeze and qualify the fixed book

**Outcome:** TB-F1 complete, prescribed TB-E1 run adjudicated, fixed replay identity sealed, and permitted policy admission completed.

**Owners/files:** existing TB-F1/P1/P2/S2 campaign artifacts, replay harness and fingerprint module; TB-D0 registry/admission record and TB-D1 ORB decision.

- [ ] Fill the accepted freeze from Packet 1/2: exact ports, panel/warm-up/calendar/overlay identities, quantity/capacity laws, costs/fill assumptions, initial state, streams, sample sizes and measured compute budget.
- [ ] Present the separate exact Part A depth/budget decision to Joshua after F1 and before any decision-bearing run. Reuse the already accepted first P2 decision.
- [ ] Execute only the prescribed legality/n1/n2/Part A/Part B sequence; preserve failure/void disposition and permitted output privacy. No substitute portfolio or extra draw.
- [ ] On PASS, seal the fixed-book replay fingerprint; complete TB-D0 and prepare the specific TB-D1 approval packet.

**Acceptance:** frozen criteria satisfied under the existing preregistration, with revision-bound evidence. Failure stops this attempt under its accepted rules.

### Packet 4 — Qualify the actual data and execution route

**Outcome:** an approved source and the exact four-symbol route demonstrably support the accepted book.

Provider-neutral test preparation and documented route analysis start earlier. Provider-specific work begins only after the standing source-independent/funding checkpoint; separately transmitted tests retain their authorization gates.

- [ ] Present one concrete provider choice, cost and qualification protocol at the funding checkpoint; implement only the selected source adapter.
- [ ] Apply frozen TB-I5 overlap/session/roll/correction/backfill/timing criteria for all four symbols. Run with emission disabled; failure blocks live use.
- [ ] Verify actual order-symbol formats and each used entry/bracket/modify/attach/trail/close/takeover behavior. Use separately authorized operator-executed tests where documentation is insufficient; no agent-generated trades.
- [ ] Qualify real feedback identity, partial fills, terminal cancellation, protection ownership and the evidence required by Packet 0. Do not infer them from a successful transport response.
- [ ] Implement/accept TB-I4 dedupe under its existing gates and bind the exact four-leg set under TB-V1 after E1/D0/D1 and symbol prerequisites.

**Acceptance:** source-equivalence PASS; used route capabilities proven or explicitly blocked; all symbol bindings verified; dedupe accepted; trusted account/settlement/feedback producers present. A missing guarantee is a finding to adjudicate, never supplied by a fake adapter.

### Packet 5 — Complete attended recovery, alerts and resume

**Outcome:** a real incident reaches Joshua, survives restart, supports observation and intervention, and cannot resume without sufficient evidence and new approval.

**Files/components:** `book_halt.py`, `book_recovery.py`, account serializer and HTTP/listener control surface; `ops/crosstrade_observer/`; proposed small `ops/c1_recovery_ui/`; notification outbox/adapter; config activation owner; Fly volume/deployment files. Prefer the existing service lifecycle over another execution service.

- [ ] Specify separate operator authentication, read-only incident projection, acknowledgment command and one-use resume command. Proposed command fields are those in section 2.4; authentication is not supplied by an adapter payload or webhook secret alone.
- [ ] Wire collector runs into incident observations without changing their unproven qualification flags. Show stale, cached, partial, revised and unfinished data explicitly. Respect the collector's five-second minimum batch interval and finite pagination budget; establish accepted freshness thresholds from the qualified route before operational acceptance.
- [ ] Build the minimal console and notification outbox. After provider selection, prove desktop alarm, mobile delivery/escalation and missed-runtime heartbeat through actual operator drills; provider acceptance is not receipt.
- [ ] Integrate the qualified reconciliation verifier from Packet 4. Refuse absent facts, mismatched account/boot/evidence, old approvals and unresolved requests. Require ordinary disarm readback and subsequent effective-activation acknowledgment.
- [ ] Exercise backup/restore with coherent SQLite backups: incident/request identities survive, restored runtime begins HALTED, and no second writer is started against the same account. Document private storage access and retention.

**Acceptance cases:** notification service down; desktop closed; runtime silent; no acknowledgment; repeated acknowledgment; manual close racing a prior request; delayed fill after flat observation; corrupt/missing journal; restart during intervention; changed evidence between review and resume; concurrent halt/resume; expired session; failed config write; new bar after resume without stale-signal replay. Run through real handler/store/UI command boundaries. Actual broker and alert drills remain separately labeled evidence.

### Packet 6 — Combined acceptance, seal and launch

**Outcome:** exact candidate release has engineering, route, account and operator acceptance.

- [ ] Independently review combined behavior and run the repository-required checks plus cross-component acceptance, on the pinned candidate revision. Reuse unaffected evidence; rerun affected checks when identity/behavior changes.
- [ ] Build digest-pinned rail/daemon images and verify exclusive account routing, persistent storage, credentials, source identity, calendar coverage, recovery interface and independent alarms. Keep disarmed until its explicit operational gate.
- [ ] Execute the separately authorized integrated qualification ceremony on the release image, including normal operation and attended fault handling. Do not repurpose M1 evidence as four-leg live evidence.
- [ ] Seal B7 account state and execution fingerprint, proving shared-component equality with the TB-E1 replay seal. Run the sole prescribed TB-E2/n3 and adjudicate under P2.
- [ ] Prepare deployment GO and its permitted reseal, current no-activity/identity evidence and operator runbook. Joshua authorizes deployment and the specific initial session; preserve the arm-expiry discipline.
- [ ] At activation, verify fresh boot/request-bound authority and durable effective-activation acknowledgment before admitting new risk. Start the frozen forward clock at actual deployment and retain existing monitoring/down-only rules.

**Acceptance:** no open release-blocking contract, parity, feed, route, reconciliation, restore, identity or review findings; B7/n3/GO/activation chain intact. A passing test count alone is not readiness.

## 4. Verification pattern and illustrative regression

Each code packet follows failing behavioral test -> minimal implementation -> focused regression -> review -> permitted integration. Keep every result bound to revision, private input digests, command/environment and evidence class (synthetic, recorded, actual route or operator).

Existing API regression illustrating why observations cannot confer recovery permission:

```python
from ops.crosstrade_observer.journal import Journal

def assert_observation_not_qualification(journal_path, account, run_id):
    # Inputs name an existing retained collector run in a private test fixture.
    with Journal(journal_path, account) as journal:
        result = journal.report(run_id)
    assert result['qualification'] == {
        'E1': 'unproven', 'E2': 'unproven', 'E3': 'unproven'
    }
```

Use the actual fixture conventions at the execution base. This assertion supplements, not replaces, Packet 5's real command-boundary resume rejection test. The resume API does not exist yet; its implementation plan must specify the authenticated producer and verified evidence interface before test/implementation code is written.

Typical retained checks, run from the isolated execution root with its verified interpreter:

```powershell
python -m pytest tests/ops/test_book_policy.py tests/ops/test_book_halt.py tests/ops/test_crosstrade_observer.py -q
python -m pytest tests/ops -q
python scripts/gate_manifest.py --tier check
git diff --check
```

Add each packet's actual new suites and configured lint to its code-level plan. Full ops/check-tier runs belong at meaningful integration boundaries, not after every document edit. Private-input skips are visible limitations; they never count as parity PASS.

## 5. Operator checkpoints and critical path

| Checkpoint | Joshua reviews/does | Coordinator prepares first |
|---|---|---|
| Packet 0 approval completed | Authorized first-slice execution after plan review | Contract frozen; independent review and final evidence recorded separately |
| Only if capability fails | Review a concrete alternate evidence/route contract | Missing guarantee, available alternatives and effect on release/qualification |
| F1 complete | Exact Part A depth/budget approval | Frozen construction and measured budget |
| Source-independent gates passed | Provider/funding choice; notification service choice as needed | Concrete cost/capability/acceptance packet |
| Route/alerts ceremony | Separately approve and perform required live actions and receipt checks | Script, expected evidence, stop conditions and teardown |
| Release | Required ORB/merge/deployment/session decisions at their proper gates | Complete evidence packets; no repeat questions for existing approvals |

Critical path: approved amendment -> evidence/route feasibility -> accepted inputs and integrated replay -> F1/E1 -> policy admission/ORB approval + approved feed and route qualification -> complete attended acceptance -> B7/n3 -> deployment GO/activation.

Source-independent intake, calendar preparation and provider-neutral tests may overlap logically with feasibility work. This does not authorize subagents or provider spending. Basic alert/UI plumbing may be built after the contract is accepted, but production resume and substantial UI investment wait for the evidence feasibility result.

No reliable calendar estimate is claimed before Packet 0 and bundle acceptance expose the real gaps. Report progress by accepted packet and remaining blocking producer, not files changed. The largest uncertainty is whether the available route can satisfy the retained normal-execution and resume evidence requirements; attendance alone does not resolve it.

## 6. Planning completion record

Original draft prepared from local source and owning records. Packet 0 subsequently refreshed main, isolated the documentation changes, froze rev9 and reconciled S3/S2/S2b/procedure/Stage 2 consumers. Official documentation was reread; no runtime source, private data, live account/host, notification service, registry or active configuration was changed. See the Packet 0 evidence record for final checks/review and the release-blocking dependencies. Later packets were not executed.
