# D-MON-1: bind the book incident notifier to Grafana Cloud IRM (build card)

**Date:** 2026-10-03.
**Status:** **DRAFT — coordinator (3) freezes after #628 merges.** Nothing here is dispatched. At freeze, coordinator (3) re-reads every anchor against the merged #628 and records the freeze in §12. **Folded 2026-10-03:** OQ-2 and OQ-3 RULED; OQ-1 proposal then pending Joshua (§9). **Second fold 2026-10-03** (hyper's OQ-1 findings, via coordinator (3)): the in-flight window and safe-resolve step (§3.6, §3.7, OA-7), the CLI's journal and channel refusals (§3.7), U13-U15 (§6.1) and the refined OQ-1 (§9); #628 re-anchored to `6e57fda`. **Ruling and third fold 2026-10-03:** OQ-1 RULED YES (Joshua, directly to coordinator (3), 2026-10-03 at about 17:19Z: "I approve your recommendations"; §9), so the §3.7 CLI is in scope; the review of `1dd7aee` is folded (the provider-side residual of the safe-resolve step, §3.7 and OQ-6; the CLI's key prefix, wait bound and import test; U8, U12-U15; the Q7 resolve order).
**Base:** origin/main `a5ca41e`. #628 is read at `origin/claude/book-incident-notifier` head `6e57fda` (OPEN, unmerged; re-anchored from `60ba482` on 2026-10-03). **Every #628 anchor must be re-confirmed at the #628 merge commit before freeze.** PR #606 is read at `origin/claude/t13-dmon-prep` head `4d64e21` (OPEN, PROPOSED). PR #615 is read at `06efb2e` (OPEN, PROPOSED). Line anchors on those branches hold only at those heads.
**Brief type:** CC handoff, code build (TDD) behind a named file boundary, plus one operator-performed live qualification run.
**Parent:** deployment checklist T13 (`docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md:266-276`), bullet "Verify real notification delivery, failure/escalation, external heartbeat and durable acknowledgment" (`:271`); D-MON (`:599`). This card covers delivery and escalation for the book route only.
**Finding being closed:** #628 shipped the channel-agnostic core with "the channel binding OWED to Joshua's D-MON choice" (#628 card `6e57fda:9`; §0.5 item 6 `:69`; §8 `:303`) and left the 60 s escalation to the binding (C-2). D-MON D-1 is ruled: Grafana Cloud IRM (PR #606 packet §8, `4d64e21:124`). D-2 is done: Joshua opened the account himself (§0.5 item 1).
**Selected outcome:** A `grafana_irm` delivering channel kind that publishes each notifier job to a Grafana IRM **Formatted webhook** integration as an **important** alert, with the incident key as `alert_uid`. The 60 s escalation runs provider-side through Joshua's Important notification rules. Joshua's Important chain fires SMS and an important mobile-app push together at step 1. Qualified by unit tests, six synthetic-incident tests against a loopback fake, and one attended live page.
**Ownership:** One Opus/CC worker builds it (§11). Joshua performs the §0.6 operator acts, including the live page. Coordinator (3) accepts. Joshua merges.
**Return boundary:** A pushed `claude/*` branch touching only §5 allowed files, or a precise blocker. The Q7 live page is not part of the worker's return; it is a separate attended run (§6.3).

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
  - no_secret_value_seen_or_handled_by_agent
  - no_credentials_or_private_data_in_repo
  - live_page_is_operator_performed_with_go_per_run
  - no_operator_decision_taken
acceptance:
  - "Every red-first test in §6.1 and §6.2 (U1-U15, Q1-Q6) fails at the base revision (or is absent) and passes at the returned head; the failing-first run is recorded"
  - "tests/ops/test_book_incident_notifier.py and the §7 regression set pass unchanged"
  - "git diff --stat origin/main...HEAD lists only §5 allowed files"
  - "python -I scripts/fp.py check: status completed, exit 0, source stable; or a pre-existing failure disclosed with its reproduction on unmodified origin/main"
  - "No token-shaped integration URL, service-account token, stack name, phone number or account identifier appears in the diff (§10 hook)"
```

## §0 — Read first (report before writing code; otherwise `NEEDS_CONTEXT`)

| Input | Where | Read |
|---|---|---|
| #628 card (FROZEN) | `docs/briefs/handoffs/2026-10-02-book-incident-notifier-build-card.md` (on main once #628 merges) | At `6e57fda`: §0.5 `:60-72`; §0.6 outbox conditions `:74-90`; §0.7 bounded publishes `:92-109`; §0.8 J0-J5 and residual `:111-146`; §3 `:193-202`; §4 G1-G11 `:211-221`; §5 `:223-242`; §8 `:301-310`; §9 `:312-329` |
| #628 code | `ops/c1_rail/book_incident_notifier.py` | At `6e57fda`: `CHANNEL_KINDS` `:70`, `_SECRET_REF` `:71`; `_JOURNAL` `:76-84`, `_journal_schema` `:88-92`, `_JOURNAL_SCHEMA` `:102`; `NotifierStoreError` `:105`; `PublishResult` `:120-133`; `Channel` protocol `:136-140`; `ChannelSpec.secret_ref` `:187-202`; `NotifierConfig` `:205-256`; `IncidentNotifier.__init__` `:266-291`; `_journal` `:295-319`; `_journal_fault` `:321-341`; `_move_aside` `:343-361`; `publish_due` `:447-461`; `_publish_round` `:463-499`; `_pending` `:501-506`; `_transition` `:508-534`; `_bounded_publish` `:554-580`; `_record_late` `:590-610`; `record_delivery` `:612-626`; `events` `:638-645`. `_deliver` and `_close_round` are removed (#628 card `:121`) |
| #628 tests | `tests/ops/test_book_incident_notifier.py` | At `6e57fda`: `_notifier` `:80-89`; incident builders `_operator`, `_protection`, `_feed_silence`, `_ordinary_unknown`, `_barrier_expiry` `:102-130`; T9 `_ALLOWED_IMPORTS` `:459`, `_reachable` `:466` |
| Halt/resume contract (HR; accepted) | `docs/spec/2026-09-14-tb-s3-halt-resume-contract.md` | §2 `:34`, `:43`; §3 `:49`; *Attendance and notification* `:55-61` (escalation `:59`, outbox `:61`); §4.1 `:89`, `:93`; §7 `:143` |
| Phase 5 plan WP2 | `docs/superpowers/plans/2026-09-16-phase5-attended-operations.md` | `:71`, `:76` |
| D-MON packet (PROPOSED) | PR #606, `git show 4d64e21:docs/notes/2026-10-02-d-mon-channel-options-packet.md` | N1-N10 `:15-24`; constraints §6 `:97-106`; qualification §7 `:108-118`; D-1 ruling `:124`; OQ-1 to OQ-4 `:128-131` |
| T13 first-session draft (PROPOSED) | PR #615, `git show 06efb2e:docs/briefs/handoffs/2026-10-02-t13-first-session-attended-procedure-DRAFT.md` | RH2 `:155`; RH3 `:156` |
| Operator record (private, gitignored) | `local_artifacts/sitting2-2026-10-03/rulings-followup.md` in the primary checkout | `:21-24` (D-MON-1/D-2 done) |
| Rules | `AGENTS.md` | launcher `:222`; *Configuration as code* `:229-238` (credentials `:236`); *Private read surface* `:197` |
| Secret precedents | `.gitignore` `:35-36` (`.env`, `.env.*`) and `:291` (`/local_artifacts/`); `deploy/c1_rail/README.md:97` (rail secrets on the volume; hardening path `fly secrets set` → env) | |

**The report states:** the dispatch revision; whether #628 merged and at which commit; every #628 anchor that moved in the merge; and whether OA-0b and OA-1 to OA-6 are reported done (only Q7 needs them).

## §0.5 — Clarifications and recorded facts

1. **Operator facts** (coordinator (2), 2026-10-03; private record `rulings-followup.md:21-24`). Joshua opened the Grafana Cloud account himself and verified his phone. At draft the mobile app was not connected; OQ-3's ruling now adds it at step 1 (item 2, OA-0b). IRM is free for 3 active users with no card; free SMS and calls are **UNVERIFIED** by test. The trial ends **2026-10-16**; no card is added, so the stack falls back to the free tier. **No integration, URL or API token exists yet.** The stack name lives only in Joshua's browser and stays out of git.
2. **Notification rules, as updated** (coordinator (3), 2026-10-03; supersedes the record's `:21` line for the default set; step 1 amended by the OQ-3 ruling). **Default** rules: SMS only. **Important** rules: step 1 = SMS **and** Mobile push important, then a 1-minute wait, then a phone call. Public docs list Mobile push important as an Important-rule step that can override Do Not Disturb [S7]; they show rule steps running in order, so "together" means two step-1 entries with no wait between them [S6]. Q7 measures the gap. So **every incident must reach Joshua through the Important rule set**, or neither the push nor the call fires.
3. **What "important" is in Grafana IRM** (public docs, §13). Importance is a property of the escalation step: a notify step uses "Default notifications or Important notifications" [S4]. No public page read for this card documents a payload field that marks an alert important [S1, S4]. Routes choose the escalation chain from the payload with Jinja2 templates; the first `True` wins; the documented example is `{{ payload.severity == "critical" }}` [S5]. **Binding:** the channel always sends the fixed marker `"severity": "critical"` (code, §3.2), **and** Joshua routes both the marker route and the catch-all route to an escalation chain whose notify step uses Important notifications (OA-2, OA-3). The Q7 live page proves it, because the call fires only under the Important set.
4. **Integration type: Formatted webhook** [S1]. `POST` JSON to the integration URL. Recognized fields: `alert_uid` ("A unique alert ID for grouping"), `title`, `message`, `state` (`ok` or `alerting`), `image_url`, `link_to_upstream_details`. The documented path is `/integrations/v1/formatted_webhook/<token>/`: **the URL embeds the integration token, so the whole URL is the secret.** An integration can optionally require a bearer token (`Authorization: Bearer glsa_…`, a Grafana service-account token). It is off by default; when it is on, a request without a valid token gets `403` [S1].
5. **Dedup / idempotency key = `alert_uid`.** A payload whose Grouping Id matches an **open** alert group (Firing, Acknowledged or Silenced) joins it. A resolved group accepts no new payloads; a matching payload then opens a **new** alert group [S2]. The docs do not say whether a payload joining an open group re-notifies [S2] (OQ-6).
6. **Delivery receipt.** The docs do not state the success status code or body [S1]. HTTP 2xx is provider acceptance only, never delivery (#628 card §3 item 3, `6e57fda:198`). This card has no provider delivery-evidence producer; the §3.7 CLI records Joshua's operator-reported acknowledgment instead (OQ-1 RULED).
7. **Rate limits** [S3]. 300 alerts per integration and 900 per org per 5 minutes; over the limit IRM returns `429`. SMS and calls have no fixed limit, but Grafana "reserves the right to throttle or stop delivery when volume is abnormally high". Free and trial orgs have extra phone-verification limits.
8. **#628 decisions carried unchanged** (#628 card `6e57fda:64-68`): C-1 read-only seam; C-2 (escalation belongs to the binding, i.e. this card); C-3 plain SHA-256 key; operator defaults OQ-1 (refusals do not notify), OQ-2 (retry with backoff until delivered, no cap) and OQ-3 (`ALL_CHANNELS_LOST` while armed is an operator-stop condition; recorded only). P3 (HR `:61` outbox wording) is **RULED** YES with conditions 1–4 (halt/resume owner, 2026-10-03; #628 card `6e57fda:74-90`, `:166`); condition 3's rebuild residual (`:86-90`) is OQ-1 risk (ii) (§9).

A contradicted fact, a missing producer or a necessary edit outside §5 returns NEEDS_CONTEXT.

## §0.6 — Operator acts (Joshua only; the agent never sees or handles the URL or any token)

| ID | Act | Needed by |
|---|---|---|
| OA-0a | Open the Grafana Cloud account and verify his phone. **Done** (§0.5 item 1). | — |
| OA-0b | Install the Grafana IRM mobile app and pair it to his IRM user (QR code, Profile → Mobile app, per coordinator (2)'s relay; the docs read for this card do not describe the pairing screen [S7]). After pairing, **coordinator (2)** adds **Mobile push important** at step 1 of his Important rules, beside the SMS and before the 1-minute wait (OQ-3 ruling). Joshua reports only "app paired"; coordinator (2) reports "push added". | Q7 |
| OA-1 | In his Grafana stack, create one IRM integration of type **Formatted webhook**. Leave "Require a Grafana service account token" **off** for this build (OQ-4). | Q7 |
| OA-2 | Create one escalation chain whose only step notifies **his own user** with **Important notifications**. Add no wait or repeat step: the personal Important rules already run SMS + push → 1 min → call. | Q7 |
| OA-3 | On the integration, add a route `{{ payload.severity == "critical" }}` → that chain, and point the catch-all (default) route at the **same** chain, so a missing marker still pages through the Important set. | Q7 |
| OA-4 | Confirm the integration's Grouping Id template groups on `alert_uid`; set `{{ payload.alert_uid }}` if it does not. Leave auto-resolve unused (the rail never sends `state: ok`). | Q7 |
| OA-5 | Put the integration URL in the private secret store under the reference name **`FP_DMON_GRAFANA_IRM_URL`**; config holds only `env:FP_DMON_GRAFANA_IRM_URL`. **Store convention: OWED** (OQ-5). Interim for Q7: a process-scoped environment variable that Joshua sets in his own terminal for the run; no agent persists it. The URL never goes into chat, git, a card, a PR, a log, an agent prompt or `glm_agent`. | Q7 |
| OA-6 | Tell the coordinator only "integration created; routes and reference set". No URL, stack name, region host or phone number. | Q7 |
| OA-7 | **Each Q7 run:** an explicit go in chat for that run. Attended, phone at hand. He runs the driver command himself and reports SMS, push and call receipt times only. He may acknowledge in IRM once the call has rung. **Only after the driver has exited** does he run `record-delivery` (§3.7; OQ-1 RULED), and he resolves the alert group only after it prints `safe to resolve` (the last attempt for the key on the delivering channel has a close event; never a clock bound). Resolving while the driver runs could let its republish open a second group (§6.3 (d)). | Q7 |
| OA-8 | After the trial ends (2026-10-16) and the stack falls back to free: a **new** go and a Q7 re-run, because free-tier SMS and calls are UNVERIFIED. | Free-tier qualification |

## §1 — Goal, scope, prerequisites

**Goal.** Every committed book incident pages Joshua by SMS and important mobile push at once, and by phone call 60 s later unless he acknowledges, through Grafana IRM with the incident key as the provider's dedup key. The #628 journal keeps detection, attempts, provider acceptance and (later) delivery separate.

**Scope.** The `grafana_irm` channel kind, its secret-reference resolution, its response mapping, the unit and synthetic-incident tests, an operator-run live-page driver and the `record-delivery` operator CLI (§3.7; OQ-1 RULED). No host wiring. Notifying Joshua's dot is a separate card (§8).

| ID | Prerequisite | State at draft | Blocks |
|---|---|---|---|
| P1 | #628 merged (core, `CHANNEL_KINDS`, `ChannelSpec.secret_ref`, `record_delivery`) | **OPEN** (PR open at `6e57fda`) | Freeze and build |
| P2 | App paired and push added (OA-0b); integration created and referenced by Joshua (OA-1 to OA-6) | **OPEN** ("No integration, URL or API token exists yet") | Q7 only; U1-U15 and Q1-Q6 use a loopback fake |
| P3 | Coordinator (3) freeze after P1 | OPEN | Dispatch |
| P4 | Joshua's explicit go for each Q7 run | Not requested | Each Q7 run |

## §2 — Escalation mapping against the halt/resume contract

The 60 s escalation stays provider-side (C-2). IRM's Important rule set (SMS + push → 1-minute wait → call) is the escalation. HR `:59` owns the requirement.

| HR requirement (`:57-61`) | How the binding meets it | Evidence | Status |
|---|---|---|---|
| "Escalate through an alternate configured channel at 60 seconds after the first notification attempt without acknowledgment" | SMS and push first; the phone call is the alternate medium, after the 1-minute wait, unless acknowledged | Q7: rail attempt time (journal); SMS, push and call times (operator-reported) | **Met (OQ-2 RULED).** Nominal 60 s from the SMS step to the call; Q7 records the measured SMS → call lag; ≤ 90 s passes, > 90 s fails |
| "route delivery failures to remaining channels immediately" | Rail side: a publish that is not accepted routes to the next configured channel at once (#628 core). With IRM as the only delivering channel, the round records `ALL_CHANNELS_LOST` (operator default OQ-3). Provider side: the important push fires in parallel with the SMS at step 1, so one failed medium is already covered; the call at +60 s is the third | Q5; Q7 (a); U11 | **Met (OQ-3 RULED).** The fan-out is Grafana-side; the rail still sends one webhook per round (U11) |
| "Persist detection, notification attempts/provider acceptance, available delivery evidence and authenticated attendance separately" | #628 journal events; IRM gives acceptance (2xx) only | Q4 | Acceptance mapped; the §3.7 CLI records operator-reported acknowledgment as delivery (OQ-1 RULED); provider delivery evidence OWED; attendance is TB-I3 (HR `:143`) |
| "Target acknowledgment is under 60 seconds after notification" | Joshua acknowledges in IRM | PR #615 RH2. Not Q7, which must not acknowledge before the call | Not measured here |
| "No acknowledgment never restores send authority" | The channel and the §3.7 CLI have no broker, dispatch, arm or owner path | U8 | Met by construction |
| "Notification outbox retries carry the same incident identity and cannot dispatch broker commands" | `alert_uid` = incident key on every retry | Q3, Q6, U8 | Met; the outbox wording (P3) is RULED under conditions 1–4 (#628 card `6e57fda:74-84`) |
| "Provider-specific channels and heartbeat thresholds require qualification before live use" | Q1-Q7, plus a Q7 re-run after the free-tier fallback (OA-8) | §6 | The heartbeat is a separate card |

## §3 — Design

1. **Kind registration.** One entry only in `book_incident_notifier.py`: `CHANNEL_KINDS["grafana_irm"] = (True, True)` (needs a secret reference; delivers). The core stays provider-agnostic and does not import the channel module.
2. **`GrafanaIRMChannel`**, in a new module `ops/c1_rail/book_incident_grafana_irm.py`, satisfies the #628 `Channel` protocol (`name`, `kind = "grafana_irm"`, `publish(idempotency_key, payload) -> PublishResult`).
   - **Body** (Formatted webhook): `alert_uid` = the idempotency key. `state` = `"alerting"` always; the rail never sends `ok`, because recovery is attended (HR §3). `severity` = `"critical"` always, a module constant with no constructor or config override (**the important marker**, §0.5 item 3). `title` = `"First Passage book incident: " + reason`. `message` = reason, `detected_at` and the first 12 hex digits of the key. No `image_url`, `link_to_upstream_details`, raw `incident_id`, account, order, strategy or figure. The body passes `assert_no_secrets`.
   - **Transport:** stdlib `urllib.request`, with no new dependency. HTTPS only, default certificate verification, **redirects never followed**, a socket timeout (each connect and read, not the whole request) strictly below `NotifierConfig.publish_timeout_s` (construction refuses otherwise), and the response read capped at 64 KiB.
   - **Acceptance mapping:**

     | Outcome | `PublishResult` |
     |---|---|
     | 2xx | `accepted`, `delivered=False`, `evidence_digest` = SHA-256 of the status code and capped body (acceptance, never delivery) |
     | 3xx (not followed); 400, 401, 403, 404, 405, 410, 413, 422 and other 4xx | `rejected` |
     | 408, 429, 5xx | `unknown` |
     | Timeout, connection, DNS or TLS failure | raise `GrafanaIRMTransportError` with no arguments, `from None` (the core journals the class name only) |

     `urllib.error.HTTPError` carries the URL (`.filename`, `.url`), so it is caught and mapped and never propagated.
3. **Secret reference.** Resolved once, at channel construction. `env:NAME` reads the process environment; a missing variable raises `NotifierConfigError` naming the reference, never a value. `secret:NAME` is refused until a store convention exists (OQ-5). The URL must be `https`, carry no userinfo, have a host ending in `.grafana.net` and have a path containing `/integrations/v1/formatted_webhook/`; a refusal names the failed rule, never the URL. The URL lives only in a private attribute: never in `repr`, `str`, exception text, `NotifierConfig.resolved()`, the digest, the journal, events or the payload. A loopback-only test allowance (`http://127.0.0.1`) is a constructor flag, off by default and unreachable from `NotifierConfig`.
4. **Config as code** (AGENTS.md `:229-238`). The instance binding is `{"name": "irm", "kind": "grafana_irm", "secret_ref": "env:FP_DMON_GRAFANA_IRM_URL"}` plus the existing `local_file` evidence channel. It lives in the Q7 driver's arguments and in tests; **no instance binding file is committed** (host wiring is out of scope).
5. **Live-page driver** (Q7 only), new `ops/c1_rail/book_incident_irm_live_page.py`. It builds a scratch `BookAccountOwner` on synthetic inputs in a directory Joshua names (for example under `local_artifacts/`), commits one `operator` halt, runs the notifier with the IRM channel from the env reference, waits, republishes once with the same key after the call step, and prints the journal events (times and kinds only). It refuses to run without `--confirm-live-page` or with a missing reference. It labels the title `[QUALIFICATION TEST]` through a constructor argument (not config), never prints the URL and starts no background process.
6. **Retry interaction (known hazard, OQ-1).** After IRM accepts, the core writes `provider_accepted`, closes the round as accepted and keeps the job `pending` (there is no delivery evidence), with backoff 5, 10, 20, then 30 s (#628 `book_incident_notifier.py` `6e57fda:486-499`, `:522-534`); `publish_due` re-selects it with no cap (`:447-461`; OQ-2 default). While the alert group is open, each retry joins it. **Once Joshua resolves the group in IRM, the next retry opens a new group and pages him again.** **In-flight window:** recording delivery cannot recall a publish already admitted. Admission commits `attempt` (`:470-477`), and only then does the publish run, outside any transaction (`:480`); a delivery recorded after that commit leaves the publish's outcome as evidence only (#628 card `6e57fda:146`, J3). So an attempt admitted before `record-delivery` commits can still POST after it and, if the group is resolved by then, open a new group. At most one publish per (job, channel) is live (#628 card `:99`), and its close event is written even for a closed job (`:486-492`, `:598-608`), so the journal shows when the rail-side window has closed (§3.7). This card does not change core semantics; OQ-1 is RULED for the §3.7 CLI, which closes the job before the resolve.
7. **`record-delivery` operator CLI (OQ-1 RULED YES, §9; built by the D-MON-1 worker after #628 merges and this card freezes).** New `ops/c1_rail/book_incident_operator_cli.py`: `record-delivery <key> --journal <path> --config <path> [--channel <name>] [--wait-s <seconds>]`. `<key>` is the full 64-hex incident key (the `alert_uid` in the IRM alert payload) or a prefix of at least 12 hex digits (the IRM `message` carries the first 12, §3.2). The CLI resolves a prefix against the journal's jobs in the read-only pre-check; no match, or more than one, exits non-zero with no event. Anchors below are #628 `book_incident_notifier.py` at `6e57fda`.
   - **Journal pre-check (default; before any `IncidentNotifier` is built).** The constructor creates a journal at a missing path (`_journal` `:303-304`; tables `:287-289`) and moves a faulty one aside (`:284-286`; `_move_aside` `:343-361`). Run from the CLI, that would rename the live journal under a running notifier, whose next poll re-owes and re-pages every committed incident (#628 card `6e57fda:86-90`). So the CLI first opens the path read-only (`file:<path>?mode=ro`, URI open), requires `PRAGMA integrity_check` = `ok` and `_journal_schema(db) == _JOURNAL_SCHEMA` (`:88-102`), and otherwise exits non-zero naming the failed check, having created, written or moved nothing. A missing path, an empty file and a hot rollback journal (which a read-only open cannot roll back) are all refused. **Residual:** the pre-check and the constructor's own `_journal_fault` (`:321-341`) are separate opens, so a journal that turns faulty between them would still be moved aside. **Alternative:** a small additive no-rebuild open in core (for example a constructor flag that raises `NotifierStoreError` instead of creating or moving aside) closes that gap, but it edits core beyond the `CHANNEL_KINDS` line, so §5 must be widened at freeze (coordinator (3) decides).
   - **Construction and record.** It loads the `NotifierConfig` and binds an inert, non-publishing channel object for each spec, with the spec's name and kind (the constructor checks both, `:271-274`, which is why `CHANNEL_KINDS["grafana_irm"]` is needed), so it resolves no secret reference, needs no URL and makes no request. `--channel` names the delivering channel; without it the CLI uses the single delivering channel and refuses (exit non-zero, no event) when more than one is configured (a later B fallback would add a second). It calls `IncidentNotifier.record_delivery(key, channel, evidence_digest)` once (`:612-626`). The digest is SHA-256 over a domain-separated record of the key, channel and local recording time, labelled operator-reported acknowledgment; it is not authenticated attendance (TB-I3, HR `:143`). It **refuses an unknown key** (exit non-zero; core `ValueError`, `:623-624`), is **idempotent** (an already-delivered job gets no second `delivered` event; J5, `:625-626`), never calls `run_once`, `poll`, `publish_due` or `publish`, and has no broker, dispatch, arm or owner path (U8).
   - **Second writer.** Every journal access is a fresh connection with `BEGIN IMMEDIATE`, a 5 s busy timeout and the default rollback journal (`:302-319`), and every job write re-reads `_pending` in its transaction under an `UPDATE … AND state='pending'` guard (`:501-534`; J2-J5), so a record from a second process is serialized and cannot regress a job. `_round_lock` holds within one process only (`:282`); the CLI runs no rounds and needs no J0. A lock held past 5 s raises `NotifierStoreError`: the CLI exits non-zero and its transaction writes nothing. No #628 test runs a second process on one journal, so U13 tests it; if #628's journal fails U13, return NEEDS_CONTEXT.
   - **Safe-to-resolve check.** After the record commits (or finds the job already delivered), the CLI re-reads the key's events read-only and finds the last `attempt` on the channel in sequence order; J2 admits none after `delivered`. It prints `safe to resolve` (rail side only; see the residual below) only when that attempt has a later close event: `provider_accepted`, a `delivery_failed` whose outcome is not `timeout`, or `late_outcome`. A `delivery_failed` with outcome `timeout` is not a close: that publish keeps running until its `late_outcome` (`:575-579`, `:598-608`). The check is never a clock bound: the transport timeout bounds each socket operation, not the whole request, and an attempt's `at` is its round's start (`:454`, `:475`). The CLI waits at most `--wait-s` (default 120 s; a usability bound, not a safety bound), then exits non-zero without printing `safe` (U14), and Joshua leaves the group acknowledged. A re-run prints `safe` only if a close has since been journaled. If none can come (the notifier exited with the publish live, or `_record_late` swallowed a journal error, `:609-610`), the delivered job admits no new attempt, so no re-run ever prints `safe`: that key stays **acknowledged-only** and is never resolved.
   - **Operating sequence:** acknowledge in IRM → `record-delivery` → the CLI prints `safe to resolve` → resolve in IRM. The closed job is not retried and no admitted publish is still live **on the rail side**. **Residual (provider side):** a close event marks the end of the rail's request, not of IRM's processing. A POST that IRM received but whose response was lost (a transport timeout, or `408`/`429`/`5xx`) is closed as `delivery_failed`, yet IRM may still group it after the resolve and open a new group; a 2xx is acceptance only (§0.5 item 6), so grouping may also complete after it. Q7 checks for it (OQ-6). Joshua may add a wait before resolving; it narrows the window and is not a guarantee.

## §4 — Hypothesis and falsifier

**H:** A `grafana_irm` channel that sends every job as a Formatted-webhook alert, with `alert_uid` equal to the incident key and the fixed `severity: critical` marker, routed by Joshua to an Important-notification chain, pages him by SMS and then by phone call about 60 s later without acknowledgment, groups every retry of one incident into one alert group while that group is open, and never exposes the integration URL or changes the owner.
**Falsifier:** any publish without `severity: critical` or `state: alerting`, or with an `alert_uid` other than the incident key; two alert groups for one incident while the first is open; a Q7 run where the call does not fire without acknowledgment; the URL in any repo file, journal row, event, payload, log capture, `repr` or exception text; a followed redirect; a round waiting on a publish past `publish_timeout_s` (a drip-fed publish may outlive it and close as `late_outcome`, U14); any owner status, incident or generation change caused by a provider outcome; or an import path from the new modules to a broker, dispatch, arm, config-write or owner-mutation surface.

## §5 — Files

**Allowed:**
- `ops/c1_rail/book_incident_grafana_irm.py` (new): `GrafanaIRMChannel`, `GrafanaIRMTransportError`, secret-reference resolution, URL validation, response mapping.
- `ops/c1_rail/book_incident_notifier.py`: **only** the `CHANNEL_KINDS["grafana_irm"]` entry and its comment.
- `ops/c1_rail/book_incident_irm_live_page.py` (new): the Q7 operator-run driver.
- `ops/c1_rail/book_incident_operator_cli.py` (new): the `record-delivery` CLI (§3.7; OQ-1 RULED).
- `tests/ops/test_book_incident_grafana_irm.py` (new): U1-U15 and Q1-Q6.
- This card: the freeze record (§12) and the executor return only.

**Forbidden (stop and return if a change seems needed):**
- T00/P7 closure: `docs/briefs/handoffs/2026-09-24-tradeify-t00-p7-closure.md`; `ops/c1_rail/qualification/p7_driver.py`, `p7_evidence.py`; `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/**`.
- Qualification: `ops/c1_rail/qualification/**`, `tests/ops/qualification/**`, `docs/notes/2026-09-29-s5-c3-record/**`.
- Risk controls and locked surfaces: `core/dd_protection.py`, `core/firm_rules.py`, `core/strategies/**`, every `*.pine`, `ops/c1_signal_daemon/ports/**` (never read; AGENTS.md `:197`).
- Arming and deploy: `ops/c1_rail/c1_rail_arm.py`, `ops/c1_rail/write_volume_config.py`, `ops/c1_rail/operator_keys.json`, `deploy/**`, `fly.toml`, `.env*`.
- Other code: `book_account_owner.py` and every other `ops/c1_rail/book_*.py` owner; `book_runtime.py`; the legacy notifier path (`c1_rail_listener.py`, `c1_rail_http_server.py`, `c1_rail_telemetry.py`, `book_halt.py`; import `assert_no_secrets` only). Existing tests, including `tests/ops/test_book_incident_notifier.py`, are not edited.
- Governance docs: `AGENTS.md`, `STATE.md`, `PIPELINES.md`, `REPO_MAP.md`, `docs/adr/**`, `docs/spec/**` (including HR), the checklist, the Phase 5 plan, `ARMING_PROCEDURE.md`, the #628 card, and the PR #606 and #615 drafts.
- `.claude/settings.json`, `scripts/gates.yml`, `scripts/check_durable_store_pragmas.py`.
- `local_artifacts/**`: written only by Joshua's Q7 run; never committed, and never read for secrets.

## §6 — Tests, qualification and return taxonomy

**Gate:** the worker build passes only when U1-U15 and Q1-Q6 are red at base and green at head (DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED, below). D-MON-1 is qualified only when Q7 also passes, during the trial and again on the free tier. Each Q7 run's verdict: **RESOLVED** (every §6.3 pass item holds); **FALSIFIED** (no call without acknowledgment, an SMS → call lag above 90 s, a second alert group, or the URL exposed); **AMBIGUOUS** (anything else, e.g. the SMS or push missing while the call fires, or throttled delivery), which needs a new go to re-run.

### §6.1 Unit tests (loopback fake HTTP endpoint only; fixture token `fake-token`; no network beyond 127.0.0.1)

| ID | Test |
|---|---|
| U1 | `test_body_is_formatted_webhook_with_incident_key_as_alert_uid`: fields as in §3.2; no raw `incident_id`, account or secret-shaped value; passes `assert_no_secrets` |
| U2 | `test_every_publish_carries_the_important_marker`: `severity == "critical"` on the first publish, every retry and a malformed-row job; no constructor or config path can change it (coordinator (3), 2026-10-03) |
| U3 | `test_response_mapping`: each §3.2 row, including `delivered=False` on 2xx and the evidence digest |
| U4 | `test_redirect_is_never_followed`: a 302 to a second loopback path; the second path is never hit; the result is `rejected` |
| U5 | `test_timeout_bounded_below_publish_timeout`: a hanging endpoint returns within the bound; construction refuses a timeout at or above `publish_timeout_s` |
| U6 | `test_secret_ref_resolution_and_url_never_exposed`: `env:` resolves; a missing variable names the reference only; `secret:` is refused; the URL is absent from `repr`, `str`, exception text, `resolved()`, the digest, journal rows and events |
| U7 | `test_url_validation_refuses_without_echo`: plain http (without the loopback flag), userinfo, a foreign host, a non-formatted-webhook path |
| U8 | `test_irm_modules_have_no_broker_or_owner_mutation_path`: an AST import allowlist for every new module (the channel, the live-page driver and the §3.7 CLI), as in #628 T9; the CLI's allowlist includes `book_incident_notifier` and nothing on a broker, dispatch, arm or owner-mutation path |
| U9 | `test_grafana_irm_kind_needs_secret_ref_and_delivers`: `CHANNEL_KINDS["grafana_irm"] == (True, True)`; a spec without `secret_ref` is refused |
| U10 | `test_live_page_driver_refuses_without_confirmation_or_reference`: without `--confirm-live-page`, or with a missing env reference, the driver exits non-zero, makes no request and prints no URL |
| U11 | `test_one_webhook_per_round_fan_out_is_grafana_side`: across first publish, retries and restart, the loopback fake sees exactly one POST per round for the IRM channel; no SMS, push or call target appears in the body or config (OQ-3 ruling) |
| U12 | `test_record_delivery_cli_refuses_unknown_key_and_is_idempotent`: an unknown key exits non-zero with no event; a unique 12-hex prefix resolves to its job; a prefix matching no job, or two jobs (rows inserted directly into a test journal), exits non-zero with no event; a pending key gets one `delivered` event and is not republished; a second call adds no event; no request is made and no secret reference is resolved |
| U13 | `test_record_delivery_cli_with_a_running_notifier`: a notifier loops `run_once` against a loopback fake returning 2xx (so the job stays `pending`) while the CLI runs as a `sys.executable` subprocess on the same journal. **Forced interleaving:** the fake holds one admitted publish's response (inside `publish_timeout_s`) until the CLI subprocess has exited, so the CLI's `delivered` commit lands between that admission and its close. Then: CLI exit 0; exactly one `delivered` event for the key; the held publish's `provider_accepted` follows `delivered` and changes no job state; no `attempt` for the key after `delivered` in sequence order; the job's `rounds` equals the number of `provider_accepted` events sequenced before `delivered` (the CLI adds none); no move-aside (no `*.corrupt-*` file). With the test holding `BEGIN IMMEDIATE` on the journal for more than 5 s, the CLI exits non-zero and writes nothing |
| U14 | `test_record_delivery_cli_safe_to_resolve_waits_for_the_in_flight_close`: the loopback fake drip-feeds the response to a publish admitted before the record (each socket read inside the transport timeout, the whole response beyond `publish_timeout_s`), so the round records `delivery_failed` {`timeout`} and the publish later records `late_outcome`; the CLI does not print `safe to resolve` until that `late_outcome`; the fake sees no POST after `safe` prints; with no attempt in flight, `safe` prints right after the record; when the drip outlasts `--wait-s`, the CLI exits non-zero without printing `safe` |
| U15 | `test_record_delivery_cli_refuses_missing_or_faulty_journal`: a missing path exits non-zero and creates no file or directory; an empty file, unreadable bytes, a failed integrity check, a foreign schema and a hot rollback journal beside a valid file (left by an interrupted writer) each exit non-zero, leave the journal and any `-journal` file byte-identical and move nothing aside; a config with two delivering channels and no `--channel` exits non-zero with no event |

### §6.2 Synthetic-incident qualification Q1-Q6

Each runs a real `BookAccountOwner` on synthetic inputs → `IncidentNotifier` → the real `GrafanaIRMChannel` → a loopback fake IRM that groups by `alert_uid` while a group is open.

| ID | Test | Pass | Owners |
|---|---|---|---|
| Q1 | `test_q1_each_incident_class_pages_once_as_important`: operator, protection, feed-silence, ordinary-unknown and barrier-expiry incidents | One POST each, with `alert_uid` = incident key, `severity: critical`, `state: alerting` | HR §2 `:34`, §3 `:49` ("notify Joshua"); #628 card §2, T1; coordinator (3) important-marker update, 2026-10-03 |
| Q2 | `test_q2_cutoff_and_refusals_page_nothing` | Zero POSTs for the scheduled cutoff and for capacity, zero-size, duplicate and incomplete-barrier-before-expiry refusals | HR `:43`, §4.1 `:89`, `:93`; operator default OQ-1 (#628 §0.5 item 5) |
| Q3 | `test_q3_retries_reuse_alert_uid_and_one_group`: 503, then a hang past the timeout, then 200 | Three POSTs with identical `alert_uid`; one fake alert group; attempt, failure and acceptance events kept separate | HR `:61`; #628 G2, T6; §0.5 item 5 [S2] |
| Q4 | `test_q4_acceptance_is_not_delivery` | A 2xx records `provider_accepted` with a digest and no `delivered` event; the job stays `pending`; the next retry after backoff carries the same `alert_uid` | HR `:59`; #628 §3.3, G3, T7 |
| Q5 | `test_q5_provider_failure_isolated_and_channel_loss_recorded`: 403, 404, 429, 500, connection refused, hang | Owner `status()` and `incidents` are equal before and after; a concurrent halt commits; with IRM as the only delivering channel, a failed round records `ALL_CHANNELS_LOST` once per transition; `local_file` evidence is still written; no rail action | Phase 5 WP2 `:76`; HR `:59`; operator default OQ-3; #628 G1, G9, T4, T8 |
| Q6 | `test_q6_restart_keeps_identity_and_hides_url`: stop after a failed round, then restart on the same journal and config | Same `alert_uid` and config digest; the URL is absent from every journal row, event, payload, captured log and exception | HR `:49`; #628 G6, T12; AGENTS.md `:236` |

### §6.3 Q7: end-to-end live page (outward-facing: a real SMS and call to Joshua's phone)

**Authorization:** Joshua's explicit go in chat **for each run**; attended; **Joshua runs the command himself**, so the agent never holds the URL. No agent sends it. Prerequisites P1, P2 and P4.

**Procedure:** the §3.5 driver commits one synthetic `operator` incident on a scratch owner and publishes at t0. Joshua does **not** acknowledge until the call rings. At about t0 + 90 s the driver republishes once with the same `alert_uid`. The driver then exits, and nothing keeps retrying. Joshua may acknowledge in IRM once the call has rung; only after the driver has exited does he run `record-delivery`, and he resolves the alert group only after it prints `safe to resolve` (§3.7). Resolving while the driver runs could let its republish open a second group, which (d) scores FALSIFIED. Q7 records any alert group that opens after the resolve (OQ-6).

**Pass (all):** (a) the SMS **and** the important push both arrive at step 1, and their receipt times are recorded; (b) **the phone call fires** without acknowledgment, which proves the Important rule set ran; (c) the call follows the SMS by about 60 s (nominal 60 s; **pass ≤ 90 s**, fail > 90 s; OQ-2 ruling), and the attempt-to-SMS, attempt-to-push and SMS-to-call offsets are recorded; (d) the republish creates no second alert group and no second SMS, push or call; (e) the journal shows the attempt and `provider_accepted` with times, and the actual 2xx status is recorded.

**Evidence:** the journal in the `local_artifacts/` directory Joshua chose (private), with times labelled operator-reported. No phone number, URL, stack name or region host is recorded.

**Owners:** HR `:59` (60 s escalation; qualification before live use); D-MON packet §7 items 2-3 (PR #606 `4d64e21:113-114`); PR #615 RH2 (`06efb2e:155`); coordinator (3), 2026-10-03 (the call step is asserted); OQ-2 and OQ-3 rulings, 2026-10-03 (lag bound; push at step 1). **Re-run** under a new go after the 2026-10-16 free-tier fallback (OA-8).

### Return taxonomy (worker build: U1-U15, Q1-Q6)

- DONE: every red-first test recorded red at base and green at head; the §7 regression, `test-ops` and `check` green with records cited; the diff inside §5.
- DONE_WITH_CONCERNS: the outcome is established, with a disclosed baseline limitation unrelated to this patch and reproduced on unmodified origin/main.
- NEEDS_CONTEXT: a missing input, a contradicted fact (for example a moved #628 anchor or a public-doc fact that no longer holds) or conflicting owner text; name it.
- BLOCKED: a necessary edit outside §5, or an environment failure the launcher cannot repair.

A failed required acceptance criterion is not DONE_WITH_CONCERNS. The worker's DONE is not qualification: Q7 (twice, per OA-8) remains.

## §7 — Acceptance checks (the worker runs them; the coordinator re-runs them at the returned head)

```
python -I scripts/fp.py doctor
python -I scripts/fp.py python -m pytest tests/ops/test_book_incident_grafana_irm.py      # red at base, green at head
python -I scripts/fp.py python -m pytest tests/ops/test_book_incident_notifier.py tests/ops/test_attended_incident_rehearsal.py tests/ops/test_book_ordinary_unknown_halt.py tests/ops/test_book_owner_settlement_integration.py tests/ops/test_c1_rail_telemetry.py
python -I scripts/fp.py test-ops
python -I scripts/fp.py check
git diff --stat origin/main...HEAD                                                         # §5 allowed files only
```

Report the command, interpreter, head and each printed `record.json` (`status: completed`, exit 0, `source_stable`). Disclose any pre-existing failure with its reproduction on unmodified origin/main (AGENTS.md `:222`).

## §8 — Out of scope

- Paging policy beyond IRM: a second provider (the B fallback), schedules, repeat steps, team notification, and any change to Joshua's personal rules.
- Any mobile-app push change beyond the OA-0b step-1 entry.
- **Dot fan-out:** notifying Joshua's dot (hyper) and letting it start work on an incident is a separate card, branch `claude/dmon-dot-intake-card`. The operator direction behind it (2026-10-03, via coordinator (2)) changes no gate here; any order or recovery act stays Joshua's.
- An automated delivery-evidence producer (reading IRM alert-group state into `record_delivery`; OQ-1's unchosen alternative), and any change to the core retry semantics.
- The bearer-token requirement on the integration (OQ-4).
- Host wiring: starting the notifier in any process, `fly secrets`, `deploy/**`, arming, `dry_run`.
- The external heartbeat (PR #615 RH3), authenticated attendance and the acknowledgment API (TB-I3, HR `:143`), and acting on `ALL_CHANNELS_LOST`.
- Any provider account, spend, card or message to an external party by an agent.

## §9 — Decisions and open questions

**Recorded:** D-MON D-1 = Grafana Cloud IRM (packet `4d64e21:124`); D-2 done by Joshua; notification rules as in §0.5 item 2; every incident is sent as important (coordinator (3), 2026-10-03); P3 (HR `:61` outbox) RULED YES with conditions 1–4 by the halt/resume owner, 2026-10-03 (#628 card `6e57fda:74-90`, `:166`).
- **OQ-2 RULED YES** (HR owner coordinator (2); Joshua "this is perfect", 2026-10-03). A call about 60 s after the SMS step meets HR `:59`'s "at 60 seconds after the first notification attempt". Nominal 60 s; Q7 records the measured SMS → call lag; ≤ 90 s passes, > 90 s fails (§6.3 (c)).
- **OQ-3 RULED** (same owner and date). HR `:59`'s "route delivery failures to remaining channels immediately" is met by a **parallel step-1 channel**: Mobile push important fires with the SMS (OA-0b; §0.5 item 2), with the call at +60 s behind both. Q7 (a) asserts both step-1 media; U11 asserts the rail still sends one webhook per round.
- **OQ-1 RULED YES** (Joshua, directly to coordinator (3), 2026-10-03 at about 17:19Z: "I approve your recommendations", answering "OQ-1: build the record-delivery CLI. I recommend yes, with the safe-resolve order."). The retry-after-resolve re-page (§3.6) is handled by the `record-delivery` operator CLI (§3.7, U12-U15), operated as: acknowledge in IRM → `record-delivery` → the CLI confirms that the last attempt for (key, delivering channel) has a close event (never a clock bound) → resolve. It closes the rail-side window only; the provider-side residual stays (§3.7, OQ-6). In scope for the D-MON-1 worker after #628 merges (P1) and this card freezes (P3). **Not chosen:** acknowledge-only in IRM (never resolve while the rail job is pending) with a later IRM API read-back card (§8); treating IRM 2xx as terminal, which changes #628 semantics and the OQ-2 retry default. **Risks recorded.** (i) Under acknowledge-only no job closes, so pending jobs accumulate and each re-POSTs about every 30 s (`retry_max_s`), about 10 times per 5 min; at IRM's quoted limit of 300 alerts per integration per 5 min (§0.5 item 7, a reader summary of [S3]), about 30 open incidents reach it. Past that, IRM refuses the POSTs over the limit, old and new alike (`429` → `unknown`), and OQ-2's no-cap retry keeps resending them: new pages are delayed, not lost outright, and refusals grow as the open set grows. This is an estimate inferred from the code's cadence, not measured. (ii) Under the ruling, delivery recorded in the journal does not survive losing the journal: a rebuild treats every committed incident as owed (#628 card `6e57fda:86-90`), and because their groups are resolved, every recorded incident re-pages once, until TB-I3 records attendance in the owner store.
- **TB-I3-HOST RULED YES** (same reply and pointer, answering "TB-I3-HOST: a new, synthetic-only card for heartbeat host wiring. I recommend yes; no daemon.py, deploy or arming."). That card is written separately on branch `claude/tb-i3-host-card` and changes nothing here (§8).

**OPEN:**
- **OQ-4** (Joshua). Require the service-account bearer token? It adds a second secret and needs a second `secret_ref` per channel, which is a core change. **Lean: off for this build.**
- **OQ-5** (coordinator (3) / Joshua). **Secret store convention: OWED.** The repo names none for local secrets. `.env*` and `/local_artifacts/` are gitignored, and rail secrets sit on the Fly volume, with `fly secrets set` → env as the documented hardening path (`deploy/c1_rail/README.md:97`). Interim: a process-scoped environment variable, for Q7 only.
- **OQ-6** (Q7). Unverified provider behavior: the 2xx status and body; the default Grouping Id template for Formatted webhook; whether a payload joining an open group re-notifies; whether an acknowledgment before 60 s suppresses the call (packet OQ-4; an optional second attended run under its own go); free-tier SMS and calls after 2026-10-16; whether a POST that IRM received but whose response was lost (a transport timeout, or `408`/`429`/`5xx`), or one answered 2xx, can still be grouped after the resolve and open a new group (§3.7 residual; Q7 records any group that opens after the resolve).

## §10 — Audit hooks

```bash
python -I scripts/fp.py python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-10-03-dmon-grafana-irm-binding-card-DRAFT.md
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-03-dmon-grafana-irm-binding-card-DRAFT.md
gh pr view 628 --json state,mergeCommit,headRefOid              # P1: merged before freeze
rg -n 'grafana_irm' ops/c1_rail/book_incident_notifier.py         # Expected: the one CHANNEL_KINDS entry
rg -n 'severity' ops/c1_rail/book_incident_grafana_irm.py         # Expected: one module constant "critical", no parameter
rg -n -i 'formatted_webhook/[A-Za-z0-9]{8,}|glsa_[A-Za-z0-9]|grafana\.net/' ops tests docs   # Expected: no match (tests use the fixture token fake-token)
git diff --stat origin/main...HEAD
```

## §11 — GLM eligibility

**Not GLM-eligible. Opus/CC builds it.** Per `C:\Users\joshu\.claude\CLAUDE.md:15`, work stays with Opus "for security, secrets … or production incidents". This card handles a secret reference, a provider-credential path and the incident path. The data-safety rules also apply: no `workdir` containing `.env`, and nothing under `local_artifacts/` is passed anywhere.

## §12 — Dispatch record

- **Status:** DRAFT. After #628 merges, coordinator (3) freezes the card and records here the frozen revision, the #628 merge commit and any moved anchor.
- **Executor (planned):** one Claude Code (Opus) worker, seat worker, worktree under `.claude/worktrees/`, branch `claude/*`, pushed; no PR unless the coordinator records one.
- **Pre-dispatch checks:** §10's first two hooks, run on the frozen file.

## §13 — Public sources (read 2026-10-03 with WebFetch/WebSearch; no login)

WebFetch returns a model summary of each page, not its bytes, so the quoted phrases are reader-summary quotes. The worker re-reads [S1] and [S2] before building and returns NEEDS_CONTEXT on a contradiction.

| Ref | Page | URL |
|---|---|---|
| S1 | Configure OnCall incoming webhooks | https://grafana.com/docs/grafana-cloud/alerting-and-irm/irm/integrations/custom-integrations/incoming-webhooks/oncall-webhooks.md |
| S2 | Configure alert grouping | https://grafana.com/docs/grafana-cloud/alerting-and-irm/irm/escalation-and-routing/alert-grouping/ |
| S3 | IRM rate limits | https://grafana.com/docs/grafana-cloud/alerting-and-irm/irm/reference/rate-limits.md |
| S4 | Configure escalation chains | https://grafana.com/docs/grafana-cloud/alerting-and-irm/irm/escalation-and-routing/escalation-chains/ |
| S5 | Routing rules | https://grafana.com/docs/grafana-cloud/alerting-and-irm/irm/escalation-and-routing/routing-rules.md |
| S6 | Personal notification rules | https://grafana.com/docs/grafana-cloud/alerting-and-irm/irm/notify-responders/personal-notification-rules.md |
| S7 | Mobile app push notifications | https://grafana.com/docs/grafana-cloud/alerting-and-irm/irm/mobile-app/push-notifications/ |
