# Tradeify attended release — Packet 0 feasibility and freeze

Recorded 2026-09-15 UTC (2026-09-14 America/New_York).

**Contract:** [TB-S3 rev9](../spec/2026-09-14-tb-s3-halt-resume-contract.md).
**Execution plan:** [attended release](../superpowers/plans/2026-09-14-tradeify-attended-release.md).
**Owner:** coordinating agent; Joshua owns platform intervention and operational decisions.

## Authority and scope

Joshua requested “freeze the attended contract” and an execution plan for review, then directed “execute the first slice” after receiving that plan. This records approval to freeze its section 2 amendment and execute Packet 0. Later implementation packets, provider selection/spend, merge, transmitted tests, deployment and arming retain their separate gates. The earlier rev8 execution/schedule and first P2 approvals stand; the schedule formula and risk laws are unchanged.

The reviewed original plan is preserved in the primary checkout at `docs/superpowers/plans/2026-09-14-tradeify-attended-release.md`, SHA-256 `c8ec090cb12dd04dd23a11220901e891e996646f855fa4a6e7e0b6ba0c386734`. This branch updates its execution status; the normative frozen contract is rev9. Provider-side actor accounting and the explicit deadline/calendar dispatch transition clarify the reviewed local-fence and incident behavior without waiving evidence or changing the schedule.

The approved change is specific: incidents stop further runtime mutations and require attended platform intervention. Normal strategy execution, protective semantics, Aegis takeover and scheduled flatten remain qualified automation requirements. Acknowledgment records attendance only. Resumption retains its evidence standard and separate authenticated decision. No outage loss bound is inferred from the acknowledgment target.

## Baseline and branch disposition

- Refreshed `origin/main`: `089f0a0765d1dd011f05c6a1ae0253ab2e44297a`, PR #391. Created isolated `codex/tradeify-attended-release` at this base under `.worktrees/tradeify-attended-release`; initial tree clean. Primary checkout/private inputs preserved.
- Newer dependency tip: `39f47682208b21c28dd7abda9baac73e99e6be6b`, branch `codex/stage2-runtime-owner`, clean at inspection. Its five commits after main are `0141441` recovery owner, `c37ca7c` producer blockers, `b23b8cf` capability probe, `ed1c187` support-free continuation, `39f4768` collector.
- Read the committed recovery and observer review/verification records. They report independent bounded review and focused tests, not Stage 2 acceptance. No runtime tests were rerun for this documentation slice.
- `gh pr list --head codex/stage2-runtime-owner --state all` returned `[]`. The branch is not included in refreshed main. No PR or merge acceptance is inferred. Integrate that existing work once through its normal reviewed merge path before a dependent runtime packet; do not duplicate/rewrite it in Packet 0. This narrows the plan's “integrate accepted work” step to inventory and explicit dependency disposition because code/merge acceptance is distinct from contract acceptance.
- Current main blocks book entry/add but leaves legacy exit/flat routing. `0141441` extends configured book refusal to exit/flat and binds the real handler to `RecoveryOwner`. Thus the bypass is fixed in the newer bounded dependency, not in main or a qualified deployed release. Rev9 requires every future mutation route to share the intervention fence.

Pinned dependency sources remain available through `git show <full-tip>:<path>`; no private bodies were copied. The probe is `docs/notes/2026-09-14-crosstrade-evidence-capability-probe.md`; bounded records are `docs/superpowers/plans/2026-09-14-recovery-owner-implementation.md` and `2026-09-14-crosstrade-observer.md` at that tip. Their historical host observations are not fresh host attestations.

## Verdict

**READY:** contract-first engineering; bundle intake/parity, provider-neutral calendar/replay preparation and focused design of durable intervention. These activities do not require a fictional broker evidence producer.

**BLOCKED:** live four-leg release and production resumption. Normal-route qualification is incomplete; E1 coherence, E2 complete history/protection accounting, E3 account-wide unresolved-request fencing and provider-side intervention safety have no accepted production producer in the inspected evidence.

This is a bounded feasibility verdict about inspected interfaces, not proof that the provider can never support the book. Documentation and existing observations were sufficient to establish the present gaps; no additional authenticated account reads, broker writes, support contact or live configuration changes were made.

## Evidence classes

**CODE:** actual local interfaces. **DOC:** official provider description, freshly inspected during Packet 0. **OBS:** earlier authenticated probe/collector evidence at the pinned dependency. **QUAL:** accepted evidence for this account/route/version under retained S3 requirements. DOC and OBS do not automatically become QUAL.

OBS establishes account-bound reads, bounded history pagination and retained fill revisions. Earlier snapshot/order/position samples were flat/empty; historical order/lifecycle reads failed. The collector retains incomplete/timezone/cache/revision limitations and reports E1/E2/E3 unproven. No new nonempty order/protection trace is claimed.

## Capability-to-consumer matrix

All rows below are unqualified for production unless stated otherwise. Test descriptions are required acceptance evidence, not tests executed in Packet 0.

| Requirement | Actual or candidate producer; evidence | Missing guarantee / consumer | Acceptance needed |
|---|---|---|---|
| R-B2 four-symbol identity and routing | CODE book bindings; DOC Tradovate symbol grammar; OBS prior account route | Per-symbol exact-contract verification and active-leg binding; daemon registry, host and arm verifier | Verify each of 6J/MYM/MGC/MNQ against actual account/route, pin mapping/roll and active-leg digest; reject mismatches |
| L2(a/b) entry and bracket/partial fills | CODE legacy payload emits market PLACE with optional SL/TP; DOC bracketed entries and partial-fill handling | Complete four-leg order types, per-fill gross quantity/protection linkage and nonempty confirmation; owner and adapter feedback | Each used order form plus partial fill/protective rejection through actual route; no fabricated protection completeness |
| L2(c) protection amendment | DOC CHANGE and CANCELREPLACE are distinct workflows | Retained atomic component/anchor semantics and confirmed result; protection owner | Accepted/rejected mixed amendment, stale version, concurrent fill and unknown result; no unqualified cancel/replace substituted for AMEND |
| L2(d/e) scoped/full CLOSE and remaining protection | DOC close-position API supports full/partial demand | Actual quantity/FIFO/protection transition and delayed-result semantics; normal strategy, scheduled close and takeover | Scoped/full close, partial fill, protective-fill race, orphan prevention, rejected/unknown request; reservations released only on accepted terminal evidence |
| L2(f) first ATTACH to an allowed bare lot | DOC CANCELANDBRACKET validates live side then cancels/places protection | Required first-attach semantics and gap behavior, not established by command name; protection owner | Bare-lot attach success/rejection/partial outcome; rejection enters durable attended intervention without invented emergency recovery |
| L2(g) trail activation/offset/anchor | DOC native trails plus managed trigger services | Equivalence to each used Pine activation/anchor rule, amendment/restart semantics and ownership; adapter/protection owner | Active/inactive trail, anchor persistence, loosening rejection and provider restart; identify all autonomous actors |
| E1 coherent current acquisition | DOC snapshot and separate order/position reads; OBS account match and changing timestamps | Single causally covering gross/order/protection boundary after relevant effects; account context and reconciliation verifier | Nonempty acquisitions across concurrent fill, delayed response, stale read and restart; reject facts outside the accepted boundary |
| E2 complete execution/history and protection accounting | DOC session fills/durable stored history/per-order lifecycle; CODE version-retaining collector | Complete capture/history, gross/FIFO/protection identities and revision handling; capacity and reconciliation verifier | Session rollover, missed capture, backdated economic changes, fee revision, partial lifecycle and protective fills; incomplete evidence retains blocks |
| E3 account-wide unresolved-request fence | CODE local operation/attempt store only; DOC order-specific workflow protections | Earlier external/manual/provider requests may still act; no accepted global producer; resume and terminal release | Delayed order after flat read, external request, lost response, provider restart and complete request-to-order/lot/quarantine accounting |
| Local all-mutation fence | CODE newer RecoveryOwner/account lock plus configured exit refusal | Future normal/scheduled authority integration and exclusive process/account routing; listener | Pause transport, enqueue incident, crash/reboot, reject stale handle and further sends; display unconfirmed until fence established |
| Provider-side intervention safety | DOC managed protection/replay, copier and scheduled work | Local halt cannot quiesce these actors; operational takeover and E3 | Inventory enabled services/queued work, accepted quiescence/control procedure, delayed manager action after manual close; if unavailable, retain live block |
| Account/session/activation inputs | CODE BookSession/SettledClose/context types; existing config writer | Qualified settlement producer, calendar coverage, host identity and durable effective activation; sizing and resume | Stale/missing seal, early close/DST, wrong boot/image/config, failed config readback and approval replay |

## Current official documentation and limits

The following are concise source findings; broader implications above are inferences against S3, not provider promises.

- [Account snapshots](https://crosstrade.io/docs/api/accounts/get-accounts-summary): cached for three seconds; order-version enrichment has a bounded lookup budget and can reflect rejected modifications. A refreshed snapshot is not an accepted S3 causal fence.
- [Fill history](https://crosstrade.io/docs/api/tradovate/get-fill-history): durable captured rows, periodic capture without guaranteed deadlines, and no earlier-session backfill through this endpoint. Pagination completion does not certify complete capture.
- [Order lifecycle](https://crosstrade.io/docs/api/orders/get-order-lifecycle): order/version/command reads are concurrent; reports cover a bounded set of commands, and optional reads can be partial. Version existence does not prove modification success.
- [WebSocket](https://crosstrade.io/docs/api/websocket-api): a live stream, not a durable log; gaps/reconnects require resynchronization. This is a useful candidate input, not proof of E1–E3.
- [Close position](https://crosstrade.io/docs/api/positions/post-close-position): full/partial close routes exist and use the shared dispatcher, including Account Manager and copier behavior. This does not by itself qualify S3's scope/protection contract.
- [Mutation safety](https://crosstrade.io/docs/api/tradovate/overview): CANCELREPLACE has a durable owner-fenced workflow and ambiguous outcomes require reconciliation. CHANGE restores omitted fields; FLATPLACE has a settlement barrier. These are meaningful operation-specific guarantees, not an account-wide request fence or proof of the retained atomic AMEND primitive.
- [Execution internals](https://crosstrade.io/docs/webhooks/tradovate-advanced): managed trigger replay and protection repair can act outside the Python runtime; partial-fill protection can have uncovered intervals. Prop-account scheduled cancellations can depend on CrossTrade enforcement. These behaviors require explicit normal-operation and intervention qualification; a local halt cannot suppress them.

## Four end-to-end contract traces

| Trace / actual initiating boundary | Persisted owner and expected result | What confirms it / missing capability |
|---|---|---|
| T1: entry send in progress when authenticated fault arrives | Account serializer orders attempt and intervention; persist HALTED, generation, incident scope and original attempt. No later local mutation, including exit/flat. UNKNOWN remains UNKNOWN. UI differentiates requested from confirmed local fence. | Local process-death/transport-barrier tests establish fencing; E1–E3 are still needed to resolve remote effects. No claim that event arrival retracts a send. |
| T2: scheduled close in progress when incident occurs | Before incident, SCHEDULED_EXIT alone authorizes the qualified close. Incident revokes that authority; current sent attempt persists and the next close is refused. Manual intervention handles remaining exposure. | Handler/scheduler/owner test proves no next send; actual close/protection outcomes and delayed manager work remain route evidence. |
| T3: Joshua closes in the platform while an old request is unknown | Acknowledge appends attendance only. Manual action note and later observations attach to the same incident; old request reservation survives a flat-looking snapshot. A late fill reopens observed exposure without erasing history. | Reconciliation verifier must cover runtime/manual/provider work. No current E3 producer; resume and release remain blocked, even after elapsed time or next session. |
| T4: restart after intervention, before reconciliation/resume completes | Restore original incidents/requests; boot increments authority identity and begins HALTED/no send authority. Old acknowledgment stays history. Prior resume approval cannot activate new boot. | Restore and real handler tests; missing/corrupt state refuses. Fresh qualified evidence, ordinary disarm readback and new authenticated activation are required; current resume producer/API absent. |

T2 boundary extension: if the own-flat deadline arrives with exposure/orders/uncertainty, or the calendar becomes invalid while active, the listener enters INTERVENTION and revokes SCHEDULED_EXIT. The sent close remains owned, the next scheduled send is refused, and the operator is alerted. Subsequent valid calendar data or a late flat observation cannot restore authority. This clarifies ownership without changing the section 5 schedule formula.

Concrete state ownership: listener persists permission/generation/dispatch ownership and request graph; notification worker persists delivery attempts without permission; Joshua produces authenticated attendance/manual action records; collector persists observations and revisions; qualified verifier alone may certify reconciliation; config owner supplies write/readback and effective-activation acknowledgment. Neither daemon nor UI synthesizes missing evidence.

## Contract reconciliation and test disposition

- Rev9 sections 1–4 replace incident automatic recovery; section 5 schedule is byte-preserved. Section 6 retains the historical approval record; section 7 maps acceptance to attended outcomes.
- Retained S3 S6–S9, R-G/R-H/R-K, protection-gap and AC incident branches use rev9 intervention rather than emergency dispatch. Normal/scheduled primitive branches retain their existing evidence and outcomes. No old test name silently grants automatic recovery authority.
- S2b sends authenticated source-health faults, not a B1 flat. Sources recovering do not grant permission. Operator procedure separates acknowledgment, intervention, verified reconciliation and resume.
- TB-S2 keeps schedule overlays and costs; outage/intervention traces are integration scenarios, not invented qualification frequencies. Existing P2 economics/admission and F1 sampling gates remain.
- Deferred: production incident-triggered automatic emergency cancel/close/attach/amend. Retained: durable ownership, no duplicate effects, partial/unknown accounting, normal/scheduled close/protection/takeover, source and permission gates, restore, evidence rejection and authenticated activation.
- Later production suites must include third-party late action, hung transport with unconfirmed local fence, manual close followed by a delayed old order, alert failure and duplicate acknowledgment. Packet 0 adds no runtime test claims.

## Next work released by this finding

Packet 1's private-bundle acceptance and calendar/settlement interface work can be planned/executed when requested. Provider-neutral tests and pure replay work may proceed under their existing gates. Production resume and live qualification cannot proceed on diagnostic reads alone.

No weaker alternative is selected. If a route change or reduced evidence guarantee is proposed later, present its exact old-request resolution, provider-side authority, consequence for replay/qualification and retained failure behavior before asking Joshua to approve it. More identical flat snapshots are not a path to clearing this blocker.

## Verification and review record

**Packet 0 complete — contract/feasibility scope only.** Joshua subsequently directed commit, push and continuation to Packet 1. This record travels in the Packet 0 commit on `codex/tradeify-attended-release`, based on `089f0a0765d1dd011f05c6a1ae0253ab2e44297a`. Dependency merge and live actions remain separate; publication does not establish them.

- Independent reviewer `packet0_review` inspected all six modified and two new documents plus relevant unchanged evidence definitions and pinned dependency interfaces. Initial review found ambiguous scheduled authority at deadline/calendar failure and two minor labels. All were corrected; follow-up verdict: **Accepted for Packet 0 documentation/contract scope; no open findings**. The correction was propagated through trigger table, plan state table, operating procedure and T2 trace.
- `git diff --check` passed. Relative-link checks across all eight changed documents found zero missing targets. Exact section extraction confirmed schedule section 5 unchanged from base (Git-normalized text); runtime/config/risk files have no diff.
- `python scripts/gate_manifest.py --tier check` passed with exit 0 under repository CPython 3.11.9. Included evidence-store suite: 72 tests, 3 skipped. Existing absent-private-data and advisory notices remained visible; they do not establish export parity. The sandbox could not launch the installed base interpreter; the approved elevated retry ran the same check with existing venv dependencies, not new installations.
- The full check tier ran before the final prose clarification; affected artifact/link/schedule/whitespace checks were repeated afterward. No runtime implementation suite, new authenticated broker probe or host inspection was performed. Final record/status edits do not change the accepted behavior.

Next authorized work is Packet 1 bundle acceptance and calendar/settlement preparation. Production resume/live release remain BLOCKED on the matrix's named guarantees; no weaker contract is silently approved.
