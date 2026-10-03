# Book-route incident notification (H5(b) ABSENT row) — build card

**Date:** 2026-10-02.
**Status:** FROZEN for build by coordinator (3). The coordinator's resolutions of C-1 to C-3 and the halt/resume question P3 (deployment coordinator (3), 2026-10-02), and Joshua's operator defaults (direct, 2026-10-02, "all recommended") are recorded in §0.5 and §9. The dispatch record is §12.
**Base:** dispatch revision origin/main `d716106`. The draft was read at `6ead3df`; `git diff 6ead3df d716106` touches one unrelated vendor-question note, so every `file:line` below holds at both. Draft inputs were read with `git show` at PR #606 (`origin/claude/t13-dmon-prep`, head `7b5cb52`) and PR #615 (`origin/claude/t13-first-session-card`, head `06efb2e`). At dispatch both are unmerged, still at those heads, and PROPOSED.
**Brief type:** CC handoff, code build (TDD) behind a named file boundary.
**Parent:** deployment checklist T13 (`docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md:266-276`), bullet "Verify real notification delivery, failure/escalation, external heartbeat and durable acknowledgment" (`:271`). The T13 first-session card draft names this gap as uncarded: "the publisher, the attendance record and binding the heartbeat to rail progress are TB-I3 / Phase 5 WP2 build work, not yet carded" (PR #615 `06efb2e`, `2026-10-02-t13-first-session-attended-procedure-DRAFT.md:95`). This card covers the publisher only.
**Finding being closed:** H5(b) recorded "Incident → notification: **ABSENT**; owed to Phase 5 WP2 / T13". No book owner emits anything when it halts (`docs/notes/2026-09-27-h5b-attended-incident-rehearsal.md:63`). The 60 s alternate-channel escalation is also ABSENT (`:65`); it stays out of this build (C-2). The H5(b) card forbade building either (`docs/briefs/handoffs/2026-09-27-h5b-attended-incident-rehearsal.md:152`, `:154`).
**Selected outcome:** A channel-agnostic, durable incident-notification component for the book route. It turns every committed `incidents` row of `BookAccountOwner` into a notification job, records detection, each attempt, provider acceptance and delivery separately from dispatch authority, and publishes through a `Channel` protocol tested with local fakes. **The channel binding is OWED** to Joshua's D-MON choice.
**Ownership:** One Opus/CC worker builds it (§11). The coordinator accepts it. Joshua merges.
**Return boundary:** A pushed `claude/*` branch that touches only the §5 allowed files, or a precise blocker.

```yaml authority
seat: worker
parent: docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push]
constraints:
  - no_main_write
  - no_merge
  - no_pr_unless_coordinator_records_it
  - allowed_files_section_5_only
  - no_owner_record_edit
  - no_rail_deploy
  - no_rail_arm
  - no_account_traffic
  - no_broker_vendor_firm_or_provider_contact
  - no_external_send
  - no_provider_account_or_spend
  - no_credentials_or_private_data_in_repo
  - no_concrete_channel_binding
  - no_operator_decision_taken
acceptance:
  - "Every red-first test in §6 fails at the base revision (or is absent) and passes at the returned head; the failing-first run is recorded"
  - "Regression set in §7 passes unchanged"
  - "git diff --stat origin/main...HEAD lists only §5 allowed files"
  - "python -I scripts/fp.py check: status completed, exit 0, source stable; or a pre-existing failure disclosed with its reproduction on unmodified origin/main"
  - "No module added by this card imports a broker, dispatch, arm or config-write path, and none holds a writable owner reference (§6 T9)"
```

## §0 — Read first (report before writing code; otherwise `NEEDS_CONTEXT`)

| Input | Where | Read |
|---|---|---|
| Halt/resume contract rev9 + 2026-09-27 amendment (HR; accepted) | `docs/spec/2026-09-14-tb-s3-halt-resume-contract.md` | §2 `:30-45`; §3 `:47-61`, mainly *Attendance and notification* `:55-61`; §4.1 `:73-114`; §7 `:141-145` |
| Incident ADR §A11, §A11.2, §A12 (§A12 PROPOSED) | `docs/adr/2026-09-17-bounded-platform-protection-incident-contract.md` | §A11 `:353-364`; §A11.2 `:382-394`; §A12 F1(c) `:436`; F3 watch `:460`; §A12.5 monitoring row `:534`, D1 prerequisites `:540-552` |
| §A12 acceptance packet (working note) | `docs/notes/2026-10-02-a12-acceptance-packet.md` | T13/D-MON row `:30`; D5 `:48` |
| Phase 5 plan (PROPOSED planning) | `docs/superpowers/plans/2026-09-16-phase5-attended-operations.md` | status `:19`; constraints `:24-25`; roles `:34`; WP2 `:63-76` |
| Checklist | as Parent | T13 `:266-276`; item 4 (#571 parked) `:588`; item 5 T13 `:597` and D-MON `:599` |
| H5(b) card and return | `docs/briefs/handoffs/2026-09-27-h5b-attended-incident-rehearsal.md` `:142-163`, `:333-337`; `docs/notes/2026-09-27-h5b-attended-incident-rehearsal.md:59-65` | |
| D-MON options packet (PROPOSED, unmerged) | PR #606, `git show 7b5cb52:docs/notes/2026-10-02-d-mon-channel-options-packet.md` | N1-N10 `:13-24`; gap check `:43-55`; constraints `:97-106`; qualification `:108-118`; OQ-1 to OQ-5 `:126-131` |
| F3 watch draft (PROPOSED, unmerged) | PR #606, `.../2026-10-02-t13-a12-f3-held-request-watch-draft.md` | W5 `:59-63`; W6 `:65-76` |
| Code: book owner | `ops/c1_rail/book_account_owner.py` | `incidents` schema `:296-297`; `_transaction` (BEGIN IMMEDIATE) `:520-532`; `incidents` property `:794-801`; `halt` `:1294-1306`; `_halt_db` `:2071-2087`; cutoff transition without an incident `:1950-1951`; `ordinary-unknown` halt `:1889` (CC-3, `b9b72f9`) |
| Code: legacy notifiers | `ops/c1_rail/c1_rail_telemetry.py` | `assert_no_secrets` `:127-144`; `OperatorNotifier`/`LoggingNotifier` `:159-175`; `FileAckNotifier` `:222-` |
| Tests to mirror | `tests/ops/test_attended_incident_rehearsal.py` (e.g. `:231`, `:331`, `:360`, `:463-519`); `tests/ops/test_book_ordinary_unknown_halt.py` (`:87`, `:282`); `tests/ops/test_book_owner_settlement_integration.py:269-282` (a failing notifier callback leaves the halt durable); `tests/ops/test_c1_rail_telemetry.py:345-440` | |
| Rules | `AGENTS.md` *Configuration as code* `:229-238`; launcher `:222-226`; `scripts/seat_authority.yml:36-63` | |

**The report states:** the dispatch revision; whether PR #606 and #615 are merged, amended or still at the heads above; whether D-MON D-1 has been recorded; and every anchor that moved.

## §0.5 — Clarifications and recorded decisions

Recorded at freeze. They bind the build; §9 gives the provenance and what stays open.

1. **Seam (C-1 = a).** One additive read-only accessor on `BookAccountOwner`. It opens the owner DB with `?mode=ro`, takes no `BEGIN IMMEDIATE` and no serializer, and changes no existing method, transaction or schema. Test T3 proves a halt commits while the notifier reads.
2. **Escalation (C-2 = out).** The 60 s alternate-channel escalation is OUT of this build. It belongs to the channel binding after Joshua's D-MON choice. The core records detection, each attempt, provider acceptance and delivery as separate durable records. Delivery-failure routing to the next channel at once (HR `:59`) stays in-repo, because it reacts to the local publish result.
3. **Dedup / idempotency key (C-3 = plain digest).** Plain SHA-256 over a domain-separated `incident_id`, with no new secret. The payload carries the opaque key and never the raw id.
4. **Outbox.** The notifier keeps its own durable journal keyed by the incident key, and every publish is bounded (timeout) and carries the idempotency key. **Whether this satisfies HR `:61`'s "notification outbox" wording stays OPEN for the halt/resume owner** (P3). This build does not claim it does.
5. **Operator defaults (Joshua, direct, 2026-10-02, "all recommended").** (OQ-1) Correctly handled refusals do NOT notify. (OQ-3) Losing every channel while armed is an operator-stop condition; this build only detects and durably records an `ALL_CHANNELS_LOST` condition and takes no rail action. (OQ-2) Retries continue with backoff until delivered, with no retry cap.
6. **Channels shipped.** The `Channel` protocol, a test fake and a local-file channel only. Secrets are referenced, never inline: config validation rejects inline values.
7. **Forbidden files** are §5's list.

A contradicted default, a missing producer or a necessary edit outside §5 returns NEEDS_CONTEXT. Frozen behavior is not permission to resolve a new contract choice.

## §1 — Goal, scope, prerequisites

**Goal.** When the book owner commits an incident, Joshua is notified through whichever channels D-MON binds. The local records then show detection, each attempt, provider acceptance, any delivery evidence and the outcome separately. None of this can change permission, generation, incidents or dispatch.

**What exists (seams, verified by reading):**
- **Detection is durable.** Every book-route halt goes through `_halt_db`, which inserts `incidents(incident_id, reason, at, generation)` with `INSERT OR IGNORE` (`book_account_owner.py:2074-2075`). A duplicate report creates no new row and no new generation (`:2076-2077`). There are about 45 call sites in `ops/c1_rail/book_*.py`, plus `book_runtime.py` calling `owner.halt` (`ops/c1_signal_daemon/book_runtime.py:165`, `:352-384`, `:448`, `:500`, `:527`). The D-MON packet reads the same way: "Detection is durable on the book route (incidents table)" (PR #606 `:48`).
- **A scheduled cutoff writes no incident row.** It sets `HALTED`/`SCHEDULED_EXIT` directly (`:1950-1951`). That matches HR §4.1 "Scheduled entry cutoff: Not an incident" (`:89`).
- **No notifier is attached to the book route.** `OperatorNotifier`, `LoggingNotifier` and `FileAckNotifier` serve only the legacy listener and HTTP server (`c1_rail_listener.py:214-227`, `:333`, `:383`, `:421`; `c1_rail_http_server.py:430`, `:506`, `:557`, `:612-629`). The only book-side callback, `on_halt` on settlement, defaults to `None` (`book_account_owner.py:650-686`).
- **No production host instantiates `BookAccountOwner`.** `rg 'BookAccountOwner\(' ops` matches only the class definition (`:347`). Host wiring is therefore out of this card (§8).

**The seam hazard (load-bearing).** The existing `incidents` property opens the owner DB with `BEGIN IMMEDIATE` (`:526`, via `:795-801`), which is a write lock with a 5 s busy timeout (`:523`). A poller that used it could make a concurrent `_halt_db` wait and then fail. A failed halt write suppresses sends but leaves no durable incident (`:2085-2087`). That would breach the WP2 acceptance line "Notification failure cannot enable or block the durable halt itself" (`phase5…:76`). **The notifier must never take the owner's write lock** (C-1; test T3).

**Prerequisites.**

| ID | Item | State at dispatch | Blocks |
|---|---|---|---|
| P1 | Coordinator decisions C-1 (seam), C-2 (escalation home), C-3 (dedup key) | **Recorded** (§0.5, §9) | Nothing |
| P2 | Operator D-MON D-1 (provider and media) | Open; "The channel choice is still the operator's" (checklist `:599`) | Only the channel binding (OWED). The core is built and accepted without it |
| P3 | HR owner reading of D-MON OQ-1: does a bounded publish with the idempotency key meet HR `:61`'s "notification outbox"? | **OPEN** for the halt/resume owner (§0.5 item 4) | Only the final form of §4 G8. This card builds a local durable journal either way |
| P4 | CC-3 acceptance | Accepted in synthetic scope (CC-3 card §7) | Nothing here. The `ordinary-unknown` row already exists on main (`b9b72f9`), and the card consumes rows without classifying them |

## §2 — Which incidents must notify (from the owners, nothing invented)

**Rule for this card:** every committed `incidents` row produces exactly one notification job, keyed by the incident key derived from `incident_id`. The card does not classify rows. It carries `reason` through to the record, and HR §4.1 owns the classification.

| Owner text | Says |
|---|---|
| HR §2 row 1 (`:34`) | Operator stop, loss of required broker/account evidence, uncertain transport/order outcome, protection fault, invalid runtime identity, or unavailable/corrupt safety state: publish the halt "and alert Joshua for platform intervention" |
| HR §2 auth-expiry row (`:40`) | "An incident during that interval revokes scheduled-exit authority and alerts for manual recovery" |
| HR §2 own-flat/calendar row (`:42`) | "retain sent/unknown close attempts and alert for manual recovery" |
| HR §3 (`:49`) | On halt: "Fence new runtime mutations, notify Joshua and continue read-only collection" |
| HR §4.1 table (`:81-93`) and qualifications (`:95-103`) | Classifies the §2 rows. Incidents: row 1, operator stop (O-6), source/control/barrier expiry, missing bars at timeout, own-flat and calendar, late completed bar, omitted required slot. **Not incidents:** scheduled cutoff, incomplete barrier before expiry, correctly handled refusals (`:93`) |
| Incident ADR §2 (Proposed) `:49`, `:53`, `:55` | "The bridge may observe and alert"; "retain observations and alert for attended intervention"; "Immediate attended intervention/escalation" |
| §A12 F1(c) (PROPOSED) `:436` | An unknown request halts the account, and "An alert goes out for attended intervention (§3)" |
| §A12 F5 (PROPOSED) `:480` | An unexplained effect "is an incident". Notification follows only if an owner writes it as an `incidents` row; no detector exists today (F3 watch draft W4/W5, PR #606) |

**Recorded or still OPEN:**
- **Refusals** (HR `:43`) are not incidents. Operator default OQ-1: **no notification** (§0.5 item 5). No job is created.
- **Authorization expiry before cutoff** (O-3, HR `:108`) and **restart with no prior incident** (O-4, `:109`). If the owner writes an `incidents` row, the card notifies; the class stays OPEN.
- **Storage failure, where no row can be written.** HR `:34` says "expose failure through independent monitoring". HR `:61`: "failure of local storage cannot be solved by assuming the local outbox is durable." That is the external heartbeat, outside this card (§8).
- **Alert-channel loss with no incident.** It "is not a §2 trigger" (acceptance packet `:48`). Operator default OQ-3: losing every channel while armed is an operator-stop condition. This build records `ALL_CHANNELS_LOST` durably and takes no rail action; acting on it belongs to D-MON/T13 (§A12.5 `:534`; F3 draft W6, PR #606 `:65-76`).

## §3 — Design (channel-agnostic)

1. **Source of jobs (C-1 a).** The owner's `incidents` table, read through one new read-only accessor on `BookAccountOwner` that opens the DB with `?mode=ro`, takes no `BEGIN IMMEDIATE` and no serializer. It is additive in `book_account_owner.py` and changes no existing method, transaction or schema. The notifier receives only a read callable bound to the owner's path, never an owner instance (T9).
   - **Journal-mode caveat.** The owner DB uses the default rollback journal (no `journal_mode` pragma in the owner), so even a read-only reader briefly holds SHARED. T3 shows that a halt committing during notifier reads still commits.
2. **Journal (outbox, §0.5 item 4).** A separate SQLite file owned by the notifier, never the owner DB. One `jobs` row per incident key (reason, detected-at copied from the owner's `incidents.at` rather than re-stamped, generation, resolved-config digest, state, next attempt time) and an append-only `events` table whose kinds keep detection, each attempt, provider acceptance, delivery, delivery failure and the `ALL_CHANNELS_LOST` condition separate. Basis: WP2 "Persist notification work separately from dispatch authority" (`:71`) and HR "Persist detection, notification attempts/provider acceptance, available delivery evidence and authenticated attendance separately" (`:59`).
3. **Channel protocol.** `Channel.publish(idempotency_key, payload)` returns accepted, rejected or unknown, optionally with delivery evidence, and is bounded by the configured timeout (a timeout or a raise records as a delivery failure). The card ships only `FakeChannel` (tests) and `LocalFileChannel`, which is local evidence only and **not delivery** (H5(b) note `:64`). Concrete providers (Grafana IRM, PagerDuty, Healthchecks, ntfy, Telegram; PR #606 §4) are **OWED** to D-MON.
4. **Payload (C-3).** It carries the opaque idempotency key, a plain SHA-256 over a domain-separated `incident_id`, plus `reason` and `detected_at`. It carries no `incident_id` text, because ids embed internal attempt and fact identifiers such as `"ordinary-unknown:" + attempt_id` (`:1889`) and `"unknown-fact:" + fact.fact_id` (`:2129`). It carries no account, order, strategy or figure. Every payload passes `assert_no_secrets` (`c1_rail_telemetry.py:127`). Basis: D-MON packet constraint "incident id and minimal status only, with no account, order or strategy detail" (PR #606 `:102`; PROPOSED) and the public-repo posture (AGENTS.md).
5. **Config as code** (AGENTS.md `:229-238`). One frozen `NotifierConfig`: shared settings (publish timeout, retry backoff) and an ordered channel list where each entry is `{name, kind, secret_ref}`. `secret_ref` names an environment variable or secret store entry, never a value. The config is validated where it is loaded and rejects inline secret-shaped values and unknown keys. The resolved config's digest is recorded on each job. **No instance binding is committed** (`no_concrete_channel_binding`).
6. **Delivery routing and retry (C-2, OQ-2).** In a round, channels are tried in order and a delivery failure routes to the next channel at once. Retries keep the same idempotency key and continue with capped exponential backoff until delivery evidence is recorded, with no retry cap. A round in which every channel fails records `ALL_CHANNELS_LOST` once per transition, and takes no rail action. No 60 s escalation timer is built.
7. **Isolation.** The notifier runs outside the owner's serializer and transaction, holds no writable owner reference, and imports no broker, dispatch, arm or config-write module. Basis: HR `:61` "cannot dispatch broker commands"; Phase 5 `:34` "Notification and UI components cannot change permission"; H5(b) note `:64`.

## §4 — Hypothesis, falsifier and delivery guarantees

**H:** A notifier that reads committed `incidents` rows through a read-only seam and keeps its own journal turns every incident, and nothing else, into exactly one durable notification job whose attempts, provider acceptance and delivery are recorded separately, without ever changing or blocking the owner's halt, permission, generation or dispatch.
**Falsifier:** Any committed incident with no job or with two jobs; a job for a refusal or a scheduled cutoff; a halt that fails, waits past the owner's busy timeout or changes generation differently because the notifier was reading; any owner status or incident change caused by a channel or journal failure; a raw `incident_id`, account or secret-shaped value in a payload; a retry with a different idempotency key; or any import or reference path from the notifier to a broker, dispatch, arm, config-write or owner-mutation surface.

| # | Property | Status | Owner |
|---|---|---|---|
| G1 | Notification failure cannot enable or block the durable halt | **CITED** (PROPOSED plan) | Phase 5 WP2 acceptance `:76`; precedent test `test_book_owner_settlement_integration.py:269-282` |
| G2 | Retries carry the same incident identity; journal retries and acknowledgment cannot send broker commands | **CITED** (accepted) | HR `:61`; WP2 `:71`, `:76` |
| G3 | Attempt, provider acceptance, delivery evidence and attendance are persisted separately | **CITED** (accepted) | HR `:59`; WP2 `:71` |
| G4 | Route delivery failures to remaining channels immediately; escalate to an alternate channel 60 s after the first attempt without acknowledgment | **CITED** (accepted). Failure routing is in-repo here; **60 s escalation is OUT** (C-2: channel binding) | HR `:59`; Phase 5 `:25` |
| G5 | No acknowledgment never restores send authority; acknowledgment only appends attendance | **CITED** (accepted) | HR `:59`, `:61` |
| G6 | Original identities are retained across redelivery and restart | **CITED** (accepted, for incidents) | HR `:49`; applied here to jobs (T12) |
| G7 | Retry terminal condition | **Operator default** (OQ-2): retry with backoff until delivered, no cap. "At-least-once" as a formal guarantee is still stated by no owner | §0.5 item 5; WP2 `:72` freezes provider-specific thresholds only after drills |
| G8 | Deduplication | **Partly cited.** A duplicate incident report creates no duplicate recovery operation (HR `:20`), and the owner's `INSERT OR IGNORE` yields one row; the journal keys jobs by the incident key. Whether a bounded publish with the idempotency key is HR `:61`'s "notification outbox" is **OPEN** (P3) | P3 |
| G9 | Loss of every channel | **Operator default** (OQ-3): an operator-stop condition while armed. This build records `ALL_CHANNELS_LOST` only; acting on it is D-MON/T13 | §0.5 item 5; F3 draft W6 |
| G10 | Local storage failure | **CITED as out of scope here**: independent monitoring, not the local journal | HR `:34`, `:61` |
| G11 | Authenticated attendance (acknowledgment record) | **CITED requirement, OWED elsewhere**: TB-I3 owns authenticated attendance (HR `:143`). Two acknowledgments (provider vs rail) are OPEN (PR #606 OQ-2 `:128`) | OQ-4 |

## §5 — Files

**Allowed (new unless stated):**
- `ops/c1_rail/book_incident_notifier.py`: journal, `Channel` protocol, `FakeChannel`, `LocalFileChannel`, `NotifierConfig`, dispatcher with an injectable clock.
- `tests/ops/test_book_incident_notifier.py`.
- `ops/c1_rail/book_account_owner.py`: **only** the C-1 (a) accessor. Additive, one read-only accessor (`?mode=ro`, no `BEGIN IMMEDIATE`, no serializer). No change to `_transaction`, `_halt_db`, `halt`, the schema, dispatch or any existing method.
- This card (`docs/briefs/handoffs/2026-10-02-book-incident-notifier-build-card.md`), for the freeze commit and the executor return only.
- `scripts/check_durable_store_pragmas.py`: **only** the one-line `DURABLE_STORES` entry `"ops/c1_rail/book_incident_notifier.py"`.

Amended 2026-10-02 by coordinator (3): the notifier's own journal is a durable outbox store, so it is registered in `DURABLE_STORES` and issues `synchronous=FULL` and `BEGIN IMMEDIATE` on that journal only, never on the owner DB (review P3, ruling ACCEPT).

**Forbidden (stop and return if a change seems needed):**
- T00/P7 closure: `docs/briefs/handoffs/2026-09-24-tradeify-t00-p7-closure.md`; `ops/c1_rail/qualification/p7_driver.py`, `p7_evidence.py`; `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/**`.
- S5 / qualification measured closure: `ops/c1_rail/qualification/**`, `tests/ops/qualification/**`, `docs/notes/2026-09-29-s5-c3-record/**`.
- Risk controls and locked surfaces: `core/dd_protection.py`, `core/firm_rules.py`, `core/strategies/**`, every `*.pine`, `ops/c1_signal_daemon/ports/**` (never read; AGENTS.md *Private read surface* `:197`).
- Arming and config: `ops/c1_rail/c1_rail_arm.py`, `ops/c1_rail/write_volume_config.py`, `deploy/**`, `fly.toml`, `.env*`, `ops/c1_rail/operator_keys.json`.
- Legacy notifier path (#571 parked, checklist `:588`): `c1_rail_listener.py`, `c1_rail_http_server.py`, `c1_rail_telemetry.py`, `book_halt.py`. Import `assert_no_secrets` only.
- Other owners: `book_runtime.py`, `book_takeover_owner.py`, `book_protection_owner.py`, `book_settlement.py`, `book_bootstrap.py`. Existing tests are not edited.
- Docs and governance: STATE, the checklist, HR, the incident ADR, the acceptance packet, the PR #606/#615 drafts, ARMING_PROCEDURE.
- `.claude/settings.json`, `scripts/gates.yml`.

## §6 — Red-first tests and return taxonomy

Tests live in `tests/ops/test_book_incident_notifier.py`. Each uses a real `BookAccountOwner` on synthetic inputs, as `test_attended_incident_rehearsal.py` does, and a synthetic clock. Run the file first at the base revision, record the failure (the module is absent), then implement.

| ID | Test | Basis |
|---|---|---|
| T1 | `test_each_committed_incident_yields_one_job_keyed_by_incident_id`: operator, protection (`:331` pattern), feed-silence (`:200`), ordinary-unknown (`test_book_ordinary_unknown_halt.py:87`), barrier expiry | HR `:34`, `:49`; §2 |
| T2 | `test_scheduled_cutoff_and_refusals_yield_no_job`: capacity, zero-size, duplicate, incomplete barrier before expiry (`test_attended_incident_rehearsal.py:463-519`), cutoff (`:1950`) | HR `:43`, `:89`, `:93`; OQ-1 default |
| T3 | `test_halt_commits_while_notifier_reads`: notifier reads interleaved with `_halt_db` (threaded); every halt commits and the generation increments. Plus `test_notifier_never_opens_owner_with_begin_immediate`, which is the **binding guard**; the threaded test is supplementary (review 2026-10-02: a reader holding a read transaction still passes the threaded test and fails the trace test) | G1; seam hazard §1 |
| T4 | `test_channel_failure_leaves_owner_status_and_incidents_equal`: `status()` and `incidents` compare equal before and after raise, timeout, reject and unknown | G1; H5(b) note `:64` method |
| T5 | `test_duplicate_incident_report_yields_no_second_job` | G8; owner `:2074-2077` |
| T6 | `test_retry_reuses_dedup_key_and_appends_attempt` (retries continue with capped backoff, no cap on count) | G2; G7 default |
| T7 | `test_attempt_acceptance_delivery_recorded_as_separate_events` | G3 |
| T8 | `test_primary_delivery_failure_routes_to_next_channel_at_once`, and `test_all_channels_failing_records_all_channels_lost` (no rail action). No 60 s escalation test: C-2 puts escalation in the channel binding | G4; G9 default |
| T9 | `test_notifier_has_no_broker_or_owner_mutation_path`: an import/AST check that the module imports no broker, dispatch, arm, config-write, owner or `crosstrade` module; the dispatcher holds no reference exposing `halt`, `dispatch` or a bootstrap path | G2, G5; Phase 5 `:34` |
| T10 | `test_payload_has_no_incident_id_text_account_or_secret`: the payload omits the raw `incident_id` and passes `assert_no_secrets` | §3.4; PR #606 `:102` |
| T11 | `test_config_requires_secret_refs_and_rejects_inline_values`; `test_job_records_resolved_config_digest` | AGENTS.md `:236-238` |
| T12 | `test_restart_resumes_pending_jobs_with_same_identity` | G6 |
| T13 | `test_notifier_store_unavailable_does_not_touch_owner`: the journal path is unwritable; the owner halts normally; the notifier error surfaces locally | G1, G10 |

**Return taxonomy.**
- DONE: every red-first test recorded red at base and green at head; §7 regression, `test-ops` and `check` green with records cited; diff inside §5.
- DONE_WITH_CONCERNS: the selected outcome is established, with a disclosed baseline limitation unrelated to this patch, reproduced on unmodified origin/main.
- NEEDS_CONTEXT: a missing input, a contradicted default or conflicting owner text; name it.
- BLOCKED: a necessary edit outside §5, or an environment failure the launcher cannot repair.

A failed required acceptance criterion is not DONE_WITH_CONCERNS. Nothing returned here is RESOLVED for T13: real delivery, acknowledgment and the external heartbeat remain owed (§8).

## §7 — Acceptance checks (worker runs; coordinator re-runs at the returned head)

```
python -I scripts/fp.py doctor
python -I scripts/fp.py python -m pytest tests/ops/test_book_incident_notifier.py          # red at base (absent/failing), green at head
python -I scripts/fp.py python -m pytest tests/ops/test_attended_incident_rehearsal.py tests/ops/test_book_ordinary_unknown_halt.py tests/ops/test_book_owner_settlement_integration.py tests/ops/test_c1_rail_telemetry.py tests/ops/test_four_leg_runtime.py tests/ops/test_book_halt.py
python -I scripts/fp.py test-ops
python -I scripts/fp.py check
git diff --stat origin/main...HEAD                                                          # §5 allowed files only
```

Report the command, interpreter, head, and each printed `record.json` (`status: completed`, exit 0, `source_stable`). Disclose any pre-existing failure, with its reproduction on unmodified origin/main (AGENTS.md `:222-226`).

## §8 — Out of scope

- **Channel binding.** No provider module, account, credential, API call or test message (D-MON D-1/D-2 are the operator's; PR #606 `:123-124`). Real delivery, acknowledgment timing and the D-MON §7 qualification list are T13 operator rehearsals (PR #615 RH2/RH3).
- **60 s alternate-channel escalation** (C-2): the channel binding's.
- **Acting on `ALL_CHANNELS_LOST`** (operator stop while armed): D-MON/T13. This build records it only.
- **External heartbeat** and binding it to rail progress (HR `:61`; PR #606 `:104`). A separate card.
- **Authenticated attendance** and the acknowledgment API (TB-I3, HR `:143`), the incident view (WP2 `:65-67`), and the F3 held-request watch detector (§A12 `:460`).
- **Host wiring.** Starting the dispatcher in any process, `deploy/**`, `fly deploy`, arming, `dry_run` changes, or any legacy-path change (#571 parked).
- Any account, broker, vendor, firm or provider traffic; spend; any message to an external party; any MC, replay, screen or candidate code.
- Classifying any OPEN case (O-1 to O-5), or writing a provider-specific cadence or threshold as settled.

## §9 — Decisions and open questions

**Coordinator (deployment coordinator (3), 2026-10-02) — recorded.**
- **C-1 (seam): (a).** One read-only accessor on `BookAccountOwner` that opens the DB read-only (no `BEGIN IMMEDIATE`, no write lock), plus test T3 proving a halt commits while the notifier reads. Rejected: (b) notifier-side read (schema-coupled); (c) a callback in `_halt_db` (about 45 paths, runs in the transaction).
- **C-2 (escalation home): out of this build.** The 60 s alternate belongs to the channel binding after Joshua's D-MON choice. The core records detection, each attempt, provider acceptance and delivery separately. (If D-MON option C is chosen, in-repo escalation still needs an inbound ack path; PR #606 `:80`, `:128`.)
- **C-3 (dedup key): plain SHA-256** over a domain-separated `incident_id`; no new secret. The payload carries the opaque key, never the raw id.
- **Outbox:** the notifier keeps its own durable journal keyed by the incident key; publish is bounded and carries the idempotency key.

**Operator (Joshua, direct, 2026-10-02, "all recommended": E defaults) — recorded.**
- **OQ-1:** correctly handled refusals do NOT notify.
- **OQ-2:** retries continue with backoff until delivered; no cap.
- **OQ-3:** losing every channel while armed is an operator-stop condition. This build only detects and durably records `ALL_CHANNELS_LOST`; no rail action.

**Still OPEN.**
- **D-MON D-1 / D-2.** Provider and media; account opening is Joshua's act (checklist `:599`; PR #606 `:123-124`).
- **OQ-4.** Provider acknowledgment vs rail attendance (PR #606 OQ-2 `:128`).
- **Halt/resume owner, P3.** Does the notifier's own journal plus a bounded publish with the idempotency key satisfy HR `:61`'s "notification outbox" (PR #606 OQ-1 `:127`)? Left to that owner; this card does not claim it.

## §10 — Audit hooks

```bash
python -I scripts/fp.py python scripts/check_handoff_brief_form.py
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-02-book-incident-notifier-build-card.md
git ls-remote origin refs/heads/claude/t13-dmon-prep refs/heads/claude/t13-first-session-card   # 7b5cb52… / 06efb2e…
rg -n 'BookAccountOwner\(' ops            # Expected at dispatch: class definition only (no host wiring)
python -I scripts/fp.py python -m pytest tests/ops/test_book_incident_notifier.py -k never_opens_owner   # Expected: pass (owner accessor mode=ro, no BEGIN)
rg -n 'book_incident_notifier' scripts/check_durable_store_pragmas.py   # Expected: one DURABLE_STORES entry
git diff --stat origin/main...HEAD
```

Amended 2026-10-02 by coordinator (3): the hook "no `BEGIN IMMEDIATE` in `book_incident_notifier.py`" is replaced. The owner accessor `BookAccountOwner.read_incidents` opens `?mode=ro` and issues no `BEGIN` (pinned by T3's binding test `test_notifier_never_opens_owner_with_begin_immediate`, which asserts both on the accessor source and by SQL trace), and the notifier journal is registered in `scripts/check_durable_store_pragmas.py` `DURABLE_STORES`.

## §11 — GLM eligibility

**Not GLM-eligible. Opus/CC builds it.** By `C:\Users\joshu\.claude\CLAUDE.md:15`, a task stays with Opus "when architecture, API contracts or data models are open; for security, secrets … or production incidents". This card has an incident-path seam, secret references (§3.5) and incident-path code. The data-safety rules also apply (`CLAUDE.md` *Data safety*: no `workdir` containing `.env`; AGENTS.md `:197`, never pass ports).

## §12 — Dispatch record

- **Frozen revision:** this file as committed on `claude/book-incident-notifier` (cut from origin/main `d716106`).
- **Decisions:** C-1 (a); C-2 out (channel binding); C-3 plain SHA-256; outbox wording OPEN for the halt/resume owner (§9).
- **Executor:** one Claude Code (Opus) worker session, seat worker, worktree `.claude/worktrees/incident-notifier`.
- **Branch:** `claude/book-incident-notifier`, pushed; **no PR** unless the coordinator records one.
- **Pre-dispatch checks:** `check_brief.py --type handoff` and `check_handoff_authority.py` on this file; results are in the executor return.
