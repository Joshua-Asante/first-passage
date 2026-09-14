# TB-S3 rev8 — durable halt and operator resume


> **Ratified 2026-09-14 UTC:** Joshua approved rev8 execution and schedule plus the separate first P2 decision. See the [exact revision/approval record](../briefs/handoffs/2026-09-14-track-b-ratifications.md) and dated S2b/P2 addenda. Pre-approval wording below describes the reviewed design; those first-decision gates are now satisfied. Implementation, calendar/route evidence, exact-depth approval and live gates remain distinct.

Status: RATIFIED CONTRACT — execution and schedule approved 2026-09-14 UTC. No runtime change, operational GO or retrospective qualification is recorded.

Base: merged TB-I1 PR #379, `d53a06e3fa6018c6c36eb63771e5ad6d1ae961cf`. This document owns the replacement halt/resume and schedule choices for [TB-S3](2026-09-12-c1-multi-leg-rail-extension-spec.md), [TB-S2](2026-09-12-tradeify-synchronized-replay-spec.md) and the [operating procedure](../notes/rail_build/ARMING_PROCEDURE.md). Their retained order primitives, evidence contracts and strategy rules continue to apply. Formal execution ratification binds the exact reviewed revision and lands the S2b addendum; it is distinct from approving this design edit.

## 1. One permission, one recovery owner

The listener alone owns a durable `HALTED` / `RUNNING` permission state. Recovery progress is recorded separately as outstanding operations and evidence; HALTED does not mean flat. All startup paths begin HALTED. The daemon cannot grant permission. A new halt invalidates the running authorization and increments a durable generation; duplicate reports of the same incident do not create duplicate recovery operations.

Every risk-add admission and dispatch rechecks permission, generation, authorization expiry, schedule, health and existing policy/capacity gates under the same serialized owner. A halt fences pending dispatch: a request already sent or of uncertain outcome remains owned and reconciled; no system can retract a broker send by changing a local flag.

HALTED refuses all entries, adds, protection loosening and other risk increases. It admits only verified risk-reducing work through the retained CLOSE/AMEND/ATTACH rules. Recovery operates independently of new-risk permission. Existing `dry_run=true` suppresses all sends; do not implement this halt by switching that flag before recovery. SIM/dry-run never acquires real-send permission. A previously authorized live runtime retains only its scoped recovery authority during halt; initial live authority still requires the existing deployment gates.

## 2. Trigger decisions

| Trigger | Action |
|---|---|
| Operator stop, loss of required broker/account evidence, uncertain transport/order outcome, protection fault, invalid runtime identity, or unavailable/corrupt safety state | Halt immediately when detected; publish recovery ownership, reconcile, cancel risk-add remainders and safely flatten the whole controlled book. If durable storage or route evidence is unavailable, stop new sends and alert for attended recovery. |
| Required source explicitly unhealthy, control read fails, or bar barrier expires | Halt the whole book. No healthy-strategy continuation mode. Detector/report failure locally suppresses daemon risk-adds; listener independently enforces freshness and its watchdog. |
| Missing source bars | Preserve the existing source timeout: `2 * bar_period + 30 seconds` since the last required bar boundary; 30 minutes 30 seconds for this 15-minute book. Do not count periods outside the source's required session coverage as missing bars. |
| Missing daemon control reads | Preserve the existing watchdog: more than `2 * bar_period + 30 seconds` since the last authenticated read. Missing/unparseable restored time is expired. A read older than one bar prevents daemon risk-add emission. |
| Incomplete bar barrier | Preserve timeout `bar_period + 30 seconds` after its expected completion boundary. No risk-add dispatch from that bar; expiry starts the durable halt. |
| Scheduled entry cutoff | Halt and cancel resting risk-adds immediately. Existing positions retain valid protection and may exit; mandatory whole-book closure starts at the scheduled flatten time. |
| Authorization expiry | If earlier than scheduled cutoff, halt and begin whole-book recovery immediately. Expiry exactly at cutoff follows the scheduled cutoff/flatten sequence; it never grants a grace period for new risk. An incident during that interval still forces immediate recovery. |
| Process restart | Halt, restore and reconcile original operation identities, then recover to flat. Never reuse a pre-restart running authorization. |
| Valid sizing/capacity refusal, duplicate signal, or stale individual signal with otherwise healthy state | Refuse that request only. Do not invent an account incident for an ordinary valid refusal. |

The listener must receive authenticated source-health reports and validate their source/session identity and sequence. A recovered report updates health only; it grants no trading permission. Control GET proves daemon contact, not source health. Unknown order identity is an incident, unlike a recognized duplicate signal.

## 3. Common recovery

Atomically persist the halt and account-wide recovery scope before dispatch. Cover all controlled symbols and newly observed account orders/locations; an unknown order is retained for attended reconciliation, never blindly cancelled. Use original identities across redelivery and restart. Cancel resting and partially filled risk-add remainders; preserve protection for any unclosed position. Run the existing qualified CLOSE primitive for each owned symbol and reconcile partial, rejected and uncertain outcomes. Never blindly retry an uncertain send or substitute an unsupported cancel/close sequence.

Recovery is complete only on fresh coherent E1–E3/K1 evidence after preparation/latest dispatch: zero gross positions, no working orders or protective orphans, no unresolved requests, and all locations/history accounted for. Cached flatness and net zero are insufficient. A failed close stays pending and alerts; operator acknowledgment alone cannot mark it complete. Late exits or protection tightening may join the serialized recovery owner if their identity and scope are valid; they cannot race a second close.

On proven recovery completion, persist/read back ordinary disarm (`dry_run=true`, `armed_until=null`) through the config owner. A failed write remains outstanding. Keep HALTED. Daemon stop acknowledgment is diagnostic, not an additional safety authority or condition for proving broker flatness. No feed recovery, day change, daily reset or status query clears permission.

## 4. Resume decision

Resume is a new authenticated operator action, never a standing consent. It is valid only after flat/reconciled recovery, healthy qualified sources and route, complete warm-up/current synchronized bar, settled policy/lifecycle state, valid calendar coverage and the existing identity/admission/deployment checks. A still-active fault or unresolved owner cannot be overridden.

The one-use request names account, candidate image/config/policy/active-leg/calendar digests, current boot identifier, halt generation, current evidence digest, permitted session and an explicit expiry. Maximum duration is the remainder of the current permitted trading window; expiry cannot exceed the entry cutoff. No future-session preapproval. Reject stale, replayed or mismatched requests. Persist the authorization and effective-activation acknowledgment before allowing risk-add dispatch; failure remains HALTED. A concurrent halt wins and invalidates the approval. Do not replay signals produced while halted: begin with the next complete eligible bar.

Same-session resumption after an incident is allowed when every condition passes and the operator explicitly approves. Scheduled cutoff/closure cannot be overridden. Resume is not a bypass around TB-P2: initial activation still requires the full B7/n3/GO path, and later-session approval requires its own current operational evidence rather than reusing the initial no-activity attestation. No new n3 is authorized by resume. If required evidence/GO becomes invalid, follow P2's stop-and-adjudicate rule.

## 5. Exact schedule rule

All times use `America/New_York` with source-backed, per-session and per-symbol calendar rows. Let `V` be the earliest mandatory flat deadline across the selected venue/symbols for that session. Define own-flat deadline `D = min(16:00 ET, V - 15 minutes)`, entry cutoff `D - 15 minutes`, and mandatory flatten start/operator evidence check `D - 5 minutes`. No entries or resting risk-add orders at/after cutoff; cancellation is initiated at cutoff and late fills remain recovery-owned. At/after D, any exposure, working order or unconfirmed state is a deadline breach with a retained halt and attended alert, never permission to extend holding.

For a covered regular session whose V is at least 16:15, this gives 15:45 cutoff, 15:55 flatten start/check and 16:00 own-flat. For a calendar row with V=12:59, the derived times are 12:29, 12:39 and 12:44. These are policy calculations, not assertions that a particular venue/date has those deadlines. 16:30 is reconciliation/reporting only; it is never the first flatten action or a holding allowance.

An overlay closure blocks the whole session. If any required calendar/deadline is missing, contradictory, expired or leaves no valid trading window, do not arm or invent a fallback time. If invalidity appears while active, halt and recover immediately. Calendar provenance/attestation remains external evidence; frozen D19 bytes are not edited. No arbitrary news blackout is introduced: any later blackout needs an explicit schedule amendment.

Replay applies the same cutoff, cancellation and scheduled flatten start, with market fill at that instant under its existing cost/slippage model; live completion must be evidenced by D. Pine exits retain their semantics while a position exists; a prior scheduler close is fed back to the adapter and supersedes later duplicate exit intents. This earlier close is an explicit operational overlay that changes replay outcomes; regenerate scheduler-affected ledgers/parity before F1. Deadline failures count as path failures, not excluded samples. Replay may model a permitted session deterministically; synthetic operator approval is labeled as simulation and never constitutes real approval. Outage/approval scenarios belong in integration tests; do not invent incident frequencies for qualification.

## 6. Ratification choices completed

| Decision | Exact scope | Retained gate |
|---|---|---|
| Execution contract | TB-S3 rev8, this halt/recovery/resume contract, account-wide outage recovery, retained primitives/evidence/quantity laws and B1 extensions | Production implementation and actual broker/source capability evidence remain required. |
| Schedule | The formula and boundaries in §5, identical in replay/rail/procedure, including the earlier scheduled flatten overlay | Date-specific source-backed calendar and parity evidence before F1/live use. |
| S2b amendment | One authenticated fault-report path to listener-owned recovery; unhealthy sources emit no ordinary strategy signal until valid bars return; retained five-field M1 compatibility | Land the dated addendum on explicit execution ratification; preserve M1/source/build/emission gates. |
| Resume | Fresh bounded operator approval after recovery; no automatic session clearing or restart rearm | Approval cannot waive unresolved evidence, initial activation, policy or deployment gates. |
| TB-P2 first decision | Retain rev9 fixed-policy selection, scoped supersessions, retained Part A construction, B1/B2 rules, two-stage admission, shared fingerprints, GO reseal and effective activation requirements | Separate dated policy ratification; exact positive Part A depth and measured budget require the second post-F1 decision. |

The requested design simplification does not ratify TB-P2 by implication. Nothing here changes candidate sizing, admits a registry row, grants a deployment GO or authorizes trades. No Part A number is guessed before the required budget evidence exists.

## 7. Implementation boundary and verification

TB-I3 owns durable permission, serialized admission/dispatch/recovery, source-health reports, watchdogs, operator command authentication, replay-resistant approvals and host activation/config acknowledgment. TB-C1 owns the shared schedule artifact; TB-I2 consumes it; TB-T1/P2 own applicable seal evidence. Reuse TB-I1 quantities/capacity/fingerprints. The existing listener's best-effort exits and arm CLI do not establish the new durable recovery/resume capability.

Replace old automatic-session-clear tests. Required cases: each trigger; ordinary refusal without halt; cutoff/flatten/deadline ordering; early-close/DST/missing coverage; feed recovery without resume; day rollover without resume; every crash cut; in-flight send at halt; cancellation racing a fill; uncertain/partial close and orphan protection; conflicting/duplicate fault reports; unavailable listener/storage; stale/replayed approval; halt racing approval/dispatch; expiry; no buffered-signal replay; confirmed flatness with failed disarm write; dry-run never sending; replay/rail schedule equality. Carry retained primitive/producer/account tests forward. Design checks are not runtime acceptance.
