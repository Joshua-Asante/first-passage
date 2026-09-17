# Phase 5 Attended Operations Implementation Plan

> **Design amendment, 2026-09-17 UTC:** Read the [bounded platform-protection incident contract](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md) before implementing this plan. Its operator-directed authority split replaces the blanket platform-pause objective below: new strategy commands stay fenced; specifically qualified pre-existing protection may continue through isolated signal/control faults. Unknown orders stay blocked and same-session strategy reactivation remains prohibited. Full governing-contract propagation and route qualification are pending; the older acceptance wording below is not an implementation-ready reconciled contract.

> **For agentic workers:** Execute with superpowers:executing-plans; use superpowers:subagent-driven-development when bounded delegation is useful and authorized. Preserve the behavioral contract and integration owner. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the qualified candidate operable for attended sessions, with durable incident fencing, reliable notification, evidence-backed intervention/disarm and authenticated activation only in a permitted later session after an incident.

**Architecture:** Extend the existing listener/account owner, incident journal and config owner; retain one authority for broker mutations. Provide one small incident view and durable acknowledgment, a notification outbox and independently monitored heartbeat. An incident ends automated trading for its account session; recovery closes obligations but never clears that session restriction.

**Tech Stack:** Existing Python daemon/listener, durable SQLite journals, qualified observation and settlement producers, existing authentication/config boundaries, one notification integration with alternate-channel escalation, external heartbeat monitoring and pytest.

**Spec:** [Phase 4 plan](2026-09-16-phase4-real-capability-qualification.md); approved settlement/order-feasibility design in [PR 411](https://github.com/Joshua-Asante/first-passage/pull/411); accepted successors of `docs/spec/2026-09-14-tb-s3-halt-resume-contract.md`, the rail-extension and attended-settlement contracts, and `docs/notes/rail_build/ARMING_PROCEDURE.md`.

## Global Constraints

- **PROPOSED — planning only, 2026-09-16.** No implementation, provider purchase, notification to others, host change, platform action or armed-session authorization is issued here.
- Propagate the approved no-same-session-reactivation amendment before accepting dependent runtime behavior. The inspected rev9 still permits same-session resume; it is not the final reconciled contract.
- Preserve normal qualified protection, exits, takeover and scheduled cutoff/flatten. Incident intervention fences all new runtime broker mutations, including closes, cancels and protective changes. Previously transmitted and provider-side work remains an obligation.
- No same-account-session reactivation after an incident, even after reconciliation, restart, restore or date rollover. A later session requires its own current evidence and fresh bounded authorization.
- Ordinary valid refusal is request-level; do not turn a sizing/capacity refusal or recognized duplicate into a session-ending incident.
- Attendance continues until the account and all potentially effective requests are reconciled and the runtime is disarmed. Acknowledgment is neither proof of recovery nor permission to trade.
- Preserve the current acknowledgment target and alternate-channel escalation at 60 seconds after the first notification attempt without acknowledgment; delivery failure escalates immediately through remaining channels. This is not a loss bound.
- Use Phase 4's qualified producers and existing ownership laws. Do not infer quiescence from flatness, elapsed time, exhausted pagination or local process shutdown.
- Private account/evidence/authorization data remains in approved ignored primary-checkout roots. Public reports contain permitted identities and verdicts.
- Phase 6 owns the final combined release acceptance, B7/n3/GO and initial activation. Phase 5 rehearsals grant none of these.

---

## Design and state contract

The coordinating agent owns combined acceptance. The listener/account owner serializes permission, halt generation, dispatch and outstanding operations. The config owner persists/read-backs disarm and activation changes. Qualified producers supply observations; Joshua performs incident platform actions and signs bounded authorization. Notification and UI components cannot change permission.

| Event | Durable outcome | Permitted next action |
|---|---|---|
| Incident or unexpected trading-runtime restart | HALTED/intervention, incident identity and account-session restriction, retained original operations/attempts | Read-only collection, alert, authenticated acknowledgment and operator intervention |
| Acknowledgment | Attendance identity/time appended idempotently | Intervention continues; permission unchanged |
| Qualified reconciliation complete | Evidence digest bound to the incident/operations; ordinary disarm requested and read back | Remain HALTED; same-session activation still refused |
| Session changes | New calendar session observed; old incidents and unresolved work retained | Evaluate current settlement/reconciliation/identity gates; no automatic activation |
| Fresh eligible later-session authorization | One-use boot/generation/evidence/session-bound authority plus durable effective-activation acknowledgment | Next complete eligible bar only, within the bounded window |
| Concurrent new halt | New generation and invalidated authority | Halt wins; no stale activation or dispatch |

Use the accepted account-session identifier and calendar mapping, not civil midnight. Persist incident restrictions alongside the existing owner; do not add a competing permissions ledger. Restore cannot erase a restriction or resurrect an old token.

Distinguish a planned, disarmed initial-activation boot from an unexpected restart during automated trading. Phase 6's prescribed post-restart initial activation must remain possible with full B7/n3/GO checks. This distinction cannot be inferred merely from a caller's `planned` label: the accepted transition must bind the preceding disarmed state, authorized operation and current boot. An existing incident-session restriction always wins. If restored state cannot establish the distinction, remain HALTED for adjudication.

## Work package 1: Reconcile the contract and accept the all-mutation fence

**Outcome:** Every sender obeys one durable intervention fence, and incident-session ineligibility survives restart and migration.

**Files:** Accepted halt/resume contract sections 4/7, rail-extension cross-references, arming procedure, runtime/account/config owners and their integration tests. Inspected `ops/c1_rail/book_halt.py` exposes `BookHaltStore.boot(...)` and is explicitly halt-only; it rejects RUNNING. Reuse the final accepted PR 409 successor and inspect its actual interfaces before designing the activation extension. Do not treat that older halt-only class as a ready resume API.

- [ ] Pin accepted Phase 4 candidate, contracts and upstream acceptance evidence. Reuse accepted fencing/ownership tests; identify the remaining delta without reopening completed work.
- [ ] Propagate PR 411's approved session restriction and the planned-initial-boot distinction through governing contracts and duplicated acceptance lists. Preserve ordinary scheduled-exit authority and all retained evidence gates.
- [ ] Trace each sender through the owner's serialized permission check and durable send claim. Cover entries/adds, exits, protection changes, takeover, scheduled closure and legacy bypass paths.
- [ ] Specify the incident-session field and migration in the existing durable owner against the selected schema. Preserve account, incident, halt generation and original operation/attempt identities. Missing/malformed history refuses activation.
- [ ] Add failing integration cases before each necessary repair; implement the smallest owner-level changes, then run the existing halt/recovery/account suites and required repository checks.

**Acceptance traces:** halt racing send claim; in-flight send with lost response; incident during scheduled flatten; two unknown attempts with only one resolved; ordinary refusal without incident; late provider action; calendar/session rollover; duplicate/conflicting incident; corrupt storage; restart and older-schema migration. After the fence takes effect, no new runtime mutation is dispatched. Already possibly effective requests remain owned. A hung or uncertain transport cannot produce a false “remote work stopped” claim.

## Work package 2: Deliver one incident view, acknowledgment and alert path

**Outcome:** Joshua receives actionable incident information and can acknowledge attendance without accidentally granting execution authority.

**Components:** Existing incident/authentication boundary plus a minimal view; durable notification outbox referencing the existing incident ID; a qualified primary and alternate delivery channel; heartbeat monitoring outside the trading host's failure domain. Provider-specific modules and thresholds are selected only after capability review and the required spending/configuration authority.

- [ ] Display permission/reason/time, local fence confirmation or uncertainty, observed positions/orders, observation age and limitations, outstanding requests, intervention notes and exact blockers. Show a clear same-session-ineligible state; provide no same-session resume button or order-entry terminal.
- [ ] Bind authenticated acknowledgment to account/incident/actor/time. Identical retries are idempotent; conflicting reuse rejects. Append manual-action notes as claims awaiting outcome evidence.
- [ ] Persist notification work separately from dispatch authority. Retry with the same incident identity; distinguish attempted send, provider acceptance, any confirmed delivery and operator acknowledgment.
- [ ] Qualify the selected channels and escalation procedure. Retain the 60-second rule and immediate delivery-failure escalation; freeze provider-specific retry and heartbeat thresholds from documented capability and measured drills before acceptance.
- [ ] Configure the external monitor only under its applicable authority. A fresh authenticated runtime heartbeat is a liveness signal, not proof of operator presence or broker safety.
- [ ] Rehearse primary failure, alternate delivery, duplicate notification, missing acknowledgment, silent host, failed local storage and stale/missing heartbeat. Actual delivery tests need named recipients and authorization; mocks prove only the local consumer behavior.

**Acceptance:** Notification failure cannot enable or block the durable halt itself. Neither outbox retry nor acknowledgment can send broker commands. If local storage cannot persist an alert, the external monitor detects host/liveness failure according to the accepted threshold; no claim of durable local delivery is made. The operator can determine what requires action without reconciling several dashboards.

## Work package 3: Prove intervention, disarm and restoration

**Outcome:** Qualified evidence closes original obligations and disarm is confirmed; restoration preserves uncertainty and never rearms.

**Inputs:** Phase 4's S1–S5/R1–R5/N1 producers and actor inventory; original journal/checkpoint/observation bytes; config owner read-back; existing backup mechanism. Reuse one capture across compatible consumers without weakening coverage or freshness.

- [ ] Assemble one operator procedure: inspect incident; acknowledge; use the platform for necessary intervention; collect outcomes covering all possibly effective runtime/manual/provider actions; reconcile; verify ordinary disarm.
- [ ] Pass actual qualified evidence through isolated consumer rehearsals. Require zero gross positions, no working/protective orphan orders, complete relevant history and no unresolved requests. A platform close or note is not completion evidence by itself.
- [ ] On proved completion, request ordinary `dry_run=true`, `armed_until=null` through the config owner and verify durable read-back. A failed write remains outstanding; attendance is not declared finished.
- [ ] Restore an isolated candidate from the supported backup procedure, with outbound order transport disabled. Verify account binding, coherent journal/checkpoint boundaries, incidents, request ownership, settlement chain and source evidence retention.
- [ ] Exercise a backup older than the last dispatch/incident. Establish missing events through the qualified reconciliation procedure or remain blocked; an empty restored database cannot establish no activity.

**Acceptance:** Interrupted reconciliation and lost acknowledgment can be retried only under their idempotent contracts; they never resend uncertain orders. Original identities survive partial restoration. Old authorization is invalid under the new boot. Restoration claims stop at demonstrated coverage; inability to reconstruct the post-backup interval is a blocker, not a reason to reset the account owner.

## Work package 4: Accept later-session activation and the attended rehearsal

**Outcome:** Same-session activation is refused; an eligible later session requires current evidence and fresh authentication through the existing permission/config owners.

- [ ] Build the authorization subject from actual account, permitted session, image/config/policy/active-leg/calendar digests, current boot, halt generation, current evidence digest and bounded expiry. Retain the contract's one-use/current-session rule; no future-session preapproval.
- [ ] Require complete reconciliation, accepted settlement, healthy qualified source/route, warmup/current synchronization, calendar coverage and existing admission/deployment identity checks. No UI override or defaulted fact.
- [ ] Serialize effective activation with halt and dispatch ownership. Persist authorization and acknowledgment before risk admission; any mismatch, expiry, replay, failed write or concurrent halt leaves HALTED.
- [ ] Start only at the next complete eligible bar; discard eligibility of buffered halted-period signals. Do not rerun n3 for ordinary later-session activation.
- [ ] Rehearse incident → alert → acknowledgment → intervention evidence → reconciliation → disarm → same-session refusal → eligible later-session authorization on the accepted candidate. Use synthetic time/session transitions for boundary tests; do not manufacture real account incidents.
- [ ] Obtain independent combined review and record exact candidate/evidence identities, measured notification and operator timings, and unproven limitations. Prepare the concise operating procedure and Phase 6 handoff.

**Required rejection cases:** wrong account/boot/session/generation; expired/replayed token; same-session incident despite flatness; missing settlement or warmup; revised history; stale image/config; pending remote request; activation acknowledgment lost; halt concurrent with activation; planned initial-boot path used to evade an incident restriction.

## Completion and operator overhead

Successful exit requires the reconciled governing amendment, accepted incident/restore/activation behavior, actual qualified alert delivery and external heartbeat detection, and the combined attended procedure on the identified candidate. An unselected notification service or mock acknowledgment is not operational acceptance.

Routine operator actions are one pre-session readiness/attendance check and bounded authorization; incident acknowledgment and platform intervention when needed; and evidence-backed close/disarm review. The agent assembles facts, checks identities and prepares decision subjects. No regular “still healthy” approval or same-session recovery negotiation is added. Attendance and necessary intervention remain real obligations.

This is a phase-level plan. Implementation packets must pin the final schema, authenticated endpoints and executable boundary tests before code changes; this document deliberately does not invent a production resume CLI. No implementation or operational drill was performed while drafting it.
