# TB-S3 rev9 — attended incident recovery and operator resume


> **Ratified 2026-09-14 UTC:** Joshua approved rev8 execution and schedule plus the separate first P2 decision. See the [exact revision/approval record](../briefs/handoffs/2026-09-14-track-b-ratifications.md) and dated S2b/P2 addenda. Pre-approval wording below describes the reviewed design; those first-decision gates are now satisfied. Implementation, calendar/route evidence, exact-depth approval and live gates remain distinct.

Status: ATTENDED AMENDMENT APPROVED FOR PACKET 0 — Joshua directed “execute the first slice” after reviewing the [attended-release plan](../superpowers/plans/2026-09-14-tradeify-attended-release.md). Recorded 2026-09-15 UTC (2026-09-14 America/New_York). This authorizes the contract freeze and feasibility work, not later implementation, merge, live operation or a weaker evidence standard. [Packet 0 evidence and review](../notes/2026-09-14-tradeify-attended-feasibility.md).

Base: merged TB-I1 PR #379, `d53a06e3fa6018c6c36eb63771e5ad6d1ae961cf`. This document owns the replacement halt/resume and schedule choices for [TB-S3](2026-09-12-c1-multi-leg-rail-extension-spec.md), [TB-S2](2026-09-12-tradeify-synchronized-replay-spec.md) and the [operating procedure](../notes/rail_build/ARMING_PROCEDURE.md). Their retained order primitives, evidence contracts and strategy rules continue to apply. Formal execution ratification binds the exact reviewed revision and lands the S2b addendum; it is distinct from approving this design edit.

## 1. One permission, one recovery owner

The listener alone owns a durable `HALTED` / `RUNNING` permission state. Recovery progress is recorded separately as outstanding operations and evidence; HALTED does not mean flat. All startup paths begin HALTED. The daemon cannot grant permission. A new halt invalidates the running authorization and increments a durable generation; duplicate reports of the same incident do not create duplicate recovery operations.

Every risk-add admission and dispatch rechecks permission, generation, authorization expiry, schedule, health and existing policy/capacity gates under the same serialized owner. A halt fences pending dispatch: a request already sent or of uncertain outcome remains owned and reconciled; no system can retract a broker send by changing a local flag.

HALTED refuses all entries, adds, protection loosening and other risk increases. Dispatch ownership is separate: NORMAL permits qualified ordinary operations while RUNNING; SCHEDULED_EXIT permits only the retained cutoff/exit/flatten sequence while new risk is HALTED; INTERVENTION permits no new runtime broker mutations. An incident or manual takeover revokes both NORMAL and SCHEDULED_EXIT authority, including exits, amendments and emergency cancel/close. Startup has no send authority. Existing `dry_run=true` suppresses all sends; a config write is neither an account fence nor proof of flatness. SIM/dry-run never acquires real-send permission. Initial live authority retains all deployment gates.

Every mutation path must pass the same account serializer and boot/generation/authority checks, including legacy exit/flat. A mutation already in its transport critical section may finish; the incident records that attempt and confirms the local fence only after the old sender cannot invoke transport again. An unresponsive sender leaves fence status unconfirmed, not forcibly stolen. The operator may intervene urgently while the interface displays that uncertainty. Even a confirmed local fence cannot retract an earlier remote request.

Provider-side protection managers, queued work, scheduled cancels and copiers are additional actors, not covered by the local fence. Normal route qualification must inventory them and establish the supported intervention/quiescence procedure and residual request accounting. No claim that manual action is race-free is allowed without that evidence. This is a retained route-capability obligation, not authorization to turn off protective services blindly.

## 2. Trigger decisions

| Trigger | Action |
|---|---|
| Operator stop, loss of required broker/account evidence, uncertain transport/order outcome, protection fault, invalid runtime identity, or unavailable/corrupt safety state | Publish the durable halt and intervention scope, fence further runtime mutations and alert Joshua for platform intervention. Retain transmitted/unknown requests. If storage fails, stop new sends and expose failure through independent monitoring; do not claim a durable record or confirmed fence that was not written. |
| Required source explicitly unhealthy, control read fails, or bar barrier expires | Halt the whole book into INTERVENTION. No healthy-strategy continuation or daemon emergency-flat mode. Detector/report failure locally suppresses daemon risk-adds; listener independently enforces freshness and its watchdog. |
| Missing source bars | Preserve the existing source timeout: `2 * bar_period + 30 seconds` since the last required bar boundary; 30 minutes 30 seconds for this 15-minute book. Do not count periods outside the source's required session coverage as missing bars. |
| Missing daemon control reads | Preserve the existing watchdog: more than `2 * bar_period + 30 seconds` since the last authenticated read. Missing/unparseable restored time is expired. A read older than one bar prevents daemon risk-add emission. |
| Incomplete bar barrier | Preserve timeout `bar_period + 30 seconds` after its expected completion boundary. No risk-add dispatch from that bar; expiry starts the durable halt. |
| Scheduled entry cutoff | Halt and cancel resting risk-adds immediately. Existing positions retain valid protection and may exit; mandatory whole-book closure starts at the scheduled flatten time. |
| Authorization expiry | If earlier than scheduled cutoff, enter INTERVENTION immediately. Expiry exactly at cutoff follows the scheduled cutoff/flatten sequence; no grace period for new risk. An incident during that interval revokes scheduled-exit authority and alerts for manual recovery. |
| Process restart | Halt, restore original operation identities and require reconciliation/attended intervention as needed. No automatic broker mutations or reuse of pre-restart running authorization. |
| Own-flat deadline breach, or calendar coverage becomes invalid while active | Enter INTERVENTION and revoke SCHEDULED_EXIT authority; retain sent/unknown close attempts and alert for manual recovery. Section 5 still defines the exact deadline and missing-coverage rules. No post-deadline automated retry or holding extension is authorized. |
| Valid sizing/capacity refusal, duplicate signal, or stale individual signal with otherwise healthy state | Refuse that request only. Do not invent an account incident for an ordinary valid refusal. |

The listener must receive authenticated source-health reports and validate their source/session identity and sequence. A recovered report updates health only; it grants no trading permission. Control GET proves daemon contact, not source health. Unknown order identity is an incident, unlike a recognized duplicate signal.

## 3. Attended incident recovery

Atomically persist the halt and account-wide intervention scope, retaining original identities across redelivery/restart. Cover controlled products and observed external locations; missing complete inventory remains an explicit obligation. Fence new runtime mutations, notify Joshua and continue read-only collection. Joshua inspects and manages positions, resting/partially filled risk-add remainders and protection through the trading platform. The runtime performs no incident-triggered CLOSE/AMEND/ATTACH/CANCEL and does not accept late strategy exits as recovery authority. Ordinary qualified strategy operations, Aegis takeover and scheduled flatten remain required outside INTERVENTION.

Recovery is complete only on fresh coherent E1–E3/K1 evidence causally covering the last potentially effective runtime, operator or provider-side request: zero gross positions, no working orders or protective orphans, no unresolved requests, and all locations/history accounted for. Cached flatness, net zero, repeated empty reads, elapsed time, exhausted history pagination and operator acknowledgment are insufficient. Manual-action notes are claims awaiting outcome evidence. Missing evidence leaves the original uncertainty blocked; no retry or release credit is inferred from collector completion.

On proven recovery completion, persist/read back ordinary disarm (`dry_run=true`, `armed_until=null`) through the config owner. A failed write remains outstanding. Keep HALTED. Daemon stop acknowledgment is diagnostic, not an additional safety authority or condition for proving broker flatness. No feed recovery, day change, daily reset or status query clears permission.

### Attendance and notification

Joshua accepts attendance for each bounded armed session and verifies access to the platform and alert channels before arming. Attendance continues until reconciled/disarmed, including incidents beyond the planned end. To leave early, complete stop/intervention/disarm first. No UI connection or periodic runtime heartbeat is proof of operator presence.

Target acknowledgment is under 60 seconds after notification. Persist detection, notification attempts/provider acceptance, available delivery evidence and authenticated attendance separately. Escalate through an alternate configured channel at 60 seconds after the first notification attempt without acknowledgment; route delivery failures to remaining channels immediately. No acknowledgment never restores send authority. Provider-specific channels and heartbeat thresholds require qualification before live use; Better Stack remains unselected.

Acknowledge only appends attendance identity/time; duplicate identical acknowledgment is idempotent and conflicting reuse rejects. Incident console shows local fence status, observed exposure/orders, observation age/limitations, uncertain requests, intervention notes and blocking reasons. Notification outbox retries carry the same incident identity and cannot dispatch broker commands. Independent missed-heartbeat monitoring covers a silent runtime; failure of local storage cannot be solved by assuming the local outbox is durable.

## 4. Resume decision

Resume is a new authenticated operator action, never a standing consent. It is valid only after flat/reconciled recovery, healthy qualified sources and route, complete warm-up/current synchronized bar, settled policy/lifecycle state, valid calendar coverage and the existing identity/admission/deployment checks. A still-active fault or unresolved owner cannot be overridden.

No production resume implementation is released until a named accepted producer supplies each retained E1/E2/E3 fact, including manual/external and provider-side work. Current collector observations do not supply those guarantees. If unavailable, live-release readiness remains BLOCKED; a different evidence/route protocol requires a concrete separately reviewed amendment, never an operator waiver checkbox.

The one-use request names account, candidate image/config/policy/active-leg/calendar digests, current boot identifier, halt generation, current evidence digest, permitted session and an explicit expiry. Maximum duration is the remainder of the current permitted trading window; expiry cannot exceed the entry cutoff. No future-session preapproval. Reject stale, replayed or mismatched requests. Persist the authorization and effective-activation acknowledgment before allowing risk-add dispatch; failure remains HALTED. A concurrent halt wins and invalidates the approval. Do not replay signals produced while halted: begin with the next complete eligible bar.

Same-session resumption after an incident is allowed when every condition passes and the operator explicitly approves. Scheduled cutoff/closure cannot be overridden. Resume is not a bypass around TB-P2: initial activation still requires the full B7/n3/GO path, and later-session approval requires its own current operational evidence rather than reusing the initial no-activity attestation. No new n3 is authorized by resume. If required evidence/GO becomes invalid, follow P2's stop-and-adjudicate rule.

## 5. Exact schedule rule

All times use `America/New_York` with source-backed, per-session and per-symbol calendar rows. Let `V` be the earliest mandatory flat deadline across the selected venue/symbols for that session. Define own-flat deadline `D = min(16:00 ET, V - 15 minutes)`, entry cutoff `D - 15 minutes`, and mandatory flatten start/operator evidence check `D - 5 minutes`. No entries or resting risk-add orders at/after cutoff; cancellation is initiated at cutoff and late fills remain recovery-owned. At/after D, any exposure, working order or unconfirmed state is a deadline breach with a retained halt and attended alert, never permission to extend holding.

For a covered regular session whose V is at least 16:15, this gives 15:45 cutoff, 15:55 flatten start/check and 16:00 own-flat. For a calendar row with V=12:59, the derived times are 12:29, 12:39 and 12:44. These are policy calculations, not assertions that a particular venue/date has those deadlines. 16:30 is reconciliation/reporting only; it is never the first flatten action or a holding allowance.

An overlay closure blocks the whole session. If any required calendar/deadline is missing, contradictory, expired or leaves no valid trading window, do not arm or invent a fallback time. If invalidity appears while active, halt and recover immediately. Calendar provenance/attestation remains external evidence; frozen D19 bytes are not edited. No arbitrary news blackout is introduced: any later blackout needs an explicit schedule amendment.

Replay applies the same cutoff, cancellation and scheduled flatten start, with market fill at that instant under its existing cost/slippage model; live completion must be evidenced by D. Pine exits retain their semantics while a position exists; a prior scheduler close is fed back to the adapter and supersedes later duplicate exit intents. This earlier close is an explicit operational overlay that changes replay outcomes; regenerate scheduler-affected ledgers/parity before F1. Deadline failures count as path failures, not excluded samples. Replay may model a permitted session deterministically; synthetic operator approval is labeled as simulation and never constitutes real approval. Outage/approval scenarios belong in integration tests; do not invent incident frequencies for qualification.

## 6. Ratification choices completed

The following table is the historical rev8 approval record. Rev9 replaces incident-triggered automatic recovery with sections 1–4 above, retaining section 5 verbatim and the P2 decisions. Approval of this Packet 0 amendment does not accept runtime implementation or route feasibility.

| Decision | Exact scope | Retained gate |
|---|---|---|
| Execution contract | TB-S3 rev8, this halt/recovery/resume contract, account-wide outage recovery, retained primitives/evidence/quantity laws and B1 extensions | Production implementation and actual broker/source capability evidence remain required. |
| Schedule | The formula and boundaries in §5, identical in replay/rail/procedure, including the earlier scheduled flatten overlay | Date-specific source-backed calendar and parity evidence before F1/live use. |
| S2b amendment | One authenticated fault-report path to listener-owned recovery; unhealthy sources emit no ordinary strategy signal until valid bars return; retained five-field M1 compatibility | Land the dated addendum on explicit execution ratification; preserve M1/source/build/emission gates. |
| Resume | Fresh bounded operator approval after recovery; no automatic session clearing or restart rearm | Approval cannot waive unresolved evidence, initial activation, policy or deployment gates. |
| TB-P2 first decision | Retain rev9 fixed-policy selection, scoped supersessions, retained Part A construction, B1/B2 rules, two-stage admission, shared fingerprints, GO reseal and effective activation requirements | Separate dated policy ratification; exact positive Part A depth and measured budget require the second post-F1 decision. |

The requested design simplification does not ratify TB-P2 by implication. Nothing here changes candidate sizing, admits a registry row, grants a deployment GO or authorizes trades. No Part A number is guessed before the required budget evidence exists.

## 7. Implementation boundary and verification

TB-I3 owns durable permission, serialized normal/scheduled dispatch, the all-mutation intervention fence, source-health reports, watchdogs, authenticated attendance/resume, evidence verification and host activation/config acknowledgment. Joshua owns incident platform mutations. The observation collector supplies diagnostic records only. TB-C1 owns the shared schedule artifact; TB-I2 consumes it; TB-T1/P2 own applicable seal evidence. Reuse TB-I1 quantities/capacity/fingerprints. Existing best-effort exits and the arm CLI do not establish the new capability.

Replace old automatic-session-clear tests. Required cases: each trigger; ordinary refusal without halt; cutoff/flatten/deadline ordering; early-close/DST/missing coverage; feed recovery without resume; day rollover without resume; every crash cut; in-flight send at halt; cancellation racing a fill; uncertain/partial close and orphan protection; conflicting/duplicate fault reports; unavailable listener/storage; stale/replayed approval; halt racing approval/dispatch; expiry; no buffered-signal replay; confirmed flatness with failed disarm write; dry-run never sending; replay/rail schedule equality. Carry retained primitive/producer/account tests forward. Design checks are not runtime acceptance.

Rev9 acceptance mapping: incident-triggered automatic close/attach/amend outcome assertions are deferred for this release, not passed or deleted as historical model evidence. Replace their production obligations with durable intervention, no further runtime mutations, retained uncertainty and resume rejection. Keep normal/scheduled CLOSE, partial-fill/protection, cancellation-race, takeover and capacity invariants. Add notification/attendance idempotency, failed delivery, silent host, incident during scheduled close, unconfirmed fence during hung transport, delayed provider-side effect after local fencing, manual-action evidence changes, and restore without rearming. See the four concrete Packet 0 traces in the feasibility record.
