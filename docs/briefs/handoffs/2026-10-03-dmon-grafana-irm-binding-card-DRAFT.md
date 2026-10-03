# D-MON-1: bind the book incident notifier to Grafana Cloud IRM (build card)

**Date:** 2026-10-03.
**Status:** **DRAFT — coordinator (3) freezes after #628 merges.** Nothing here is dispatched. At freeze, coordinator (3) re-reads every anchor against the merged #628 and records the freeze in §12. **Folded 2026-10-03:** OQ-2 and OQ-3 RULED; OQ-1 proposal pending Joshua (§9).
**Base:** origin/main `a5ca41e`. #628 is read at `origin/claude/book-incident-notifier` head `60ba482` (OPEN, unmerged). PR #606 is read at `origin/claude/t13-dmon-prep` head `4d64e21` (OPEN, PROPOSED). PR #615 is read at `06efb2e` (OPEN, PROPOSED). Line anchors on those branches hold only at those heads.
**Brief type:** CC handoff, code build (TDD) behind a named file boundary, plus one operator-performed live qualification run.
**Parent:** deployment checklist T13 (`docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md:266-276`), bullet "Verify real notification delivery, failure/escalation, external heartbeat and durable acknowledgment" (`:271`); D-MON (`:599`). This card covers delivery and escalation for the book route only.
**Finding being closed:** #628 shipped the channel-agnostic core with "the channel binding OWED to Joshua's D-MON choice" (#628 card §0.5 item 6, §8) and left the 60 s escalation to the binding (C-2). D-MON D-1 is ruled: Grafana Cloud IRM (PR #606 packet §8, `4d64e21:124`). D-2 is done: Joshua opened the account himself (§0.5 item 1).
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
  - "Every red-first test in §6.1 and §6.2 (U1-U11, U12 if §3.7 is built, Q1-Q6) fails at the base revision (or is absent) and passes at the returned head; the failing-first run is recorded"
  - "tests/ops/test_book_incident_notifier.py and the §7 regression set pass unchanged"
  - "git diff --stat origin/main...HEAD lists only §5 allowed files"
  - "python -I scripts/fp.py check: status completed, exit 0, source stable; or a pre-existing failure disclosed with its reproduction on unmodified origin/main"
  - "No token-shaped integration URL, service-account token, stack name, phone number or account identifier appears in the diff (§10 hook)"
```

## §0 — Read first (report before writing code; otherwise `NEEDS_CONTEXT`)

| Input | Where | Read |
|---|---|---|
| #628 card (FROZEN) | `docs/briefs/handoffs/2026-10-02-book-incident-notifier-build-card.md` (on main once #628 merges) | §0.5 `:60-72`; §3 `:116-125`; §4 G1-G11 `:132-144`; §5 `:146-165`; §8 `:208-217`; §9 `:219-235` |
| #628 code | `ops/c1_rail/book_incident_notifier.py` | `CHANNEL_KINDS`, `_SECRET_REF`; `PublishResult`; `Channel` protocol; `ChannelSpec` and `NotifierConfig.secret_ref`; `_publish_round`, `_close_round`, `_bounded_publish`, `record_delivery` |
| #628 tests | `tests/ops/test_book_incident_notifier.py` | incident builders `_operator`, `_protection`, `_feed_silence`, `_ordinary_unknown`, `_barrier_expiry`; T9 `_reachable` and `_ALLOWED_IMPORTS` |
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
6. **Delivery receipt.** The docs do not state the success status code or body [S1]. HTTP 2xx is provider acceptance only, never delivery (#628 §3.3). This card has no delivery-evidence producer (OQ-1).
7. **Rate limits** [S3]. 300 alerts per integration and 900 per org per 5 minutes; over the limit IRM returns `429`. SMS and calls have no fixed limit, but Grafana "reserves the right to throttle or stop delivery when volume is abnormally high". Free and trial orgs have extra phone-verification limits.
8. **#628 decisions carried unchanged:** C-1 read-only seam; C-2 (escalation belongs to the binding, i.e. this card); C-3 plain SHA-256 key; operator defaults OQ-1 (refusals do not notify), OQ-2 (retry with backoff until delivered, no cap) and OQ-3 (`ALL_CHANNELS_LOST` while armed is an operator-stop condition; recorded only). P3 (HR `:61` outbox wording) stays OPEN for the HR owner.

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
| OA-7 | **Each Q7 run:** an explicit go in chat for that run. Attended, phone at hand. He runs the driver command himself and reports SMS, push and call receipt times only. He then acknowledges in IRM, runs `record-delivery` if OQ-1's proposal is chosen (§3.7), and resolves the alert group. | Q7 |
| OA-8 | After the trial ends (2026-10-16) and the stack falls back to free: a **new** go and a Q7 re-run, because free-tier SMS and calls are UNVERIFIED. | Free-tier qualification |

## §1 — Goal, scope, prerequisites

**Goal.** Every committed book incident pages Joshua by SMS and important mobile push at once, and by phone call 60 s later unless he acknowledges, through Grafana IRM with the incident key as the provider's dedup key. The #628 journal keeps detection, attempts, provider acceptance and (later) delivery separate.

**Scope.** The `grafana_irm` channel kind, its secret-reference resolution, its response mapping, the unit and synthetic-incident tests, an operator-run live-page driver and, if OQ-1's proposal is chosen, the `record-delivery` operator CLI (§3.7). No host wiring. Notifying Joshua's dot is a separate card (§8).

| ID | Prerequisite | State at draft | Blocks |
|---|---|---|---|
| P1 | #628 merged (core, `CHANNEL_KINDS`, `NotifierConfig.secret_ref`) | **OPEN** (PR open at `60ba482`) | Freeze and build |
| P2 | App paired and push added (OA-0b); integration created and referenced by Joshua (OA-1 to OA-6) | **OPEN** ("No integration, URL or API token exists yet") | Q7 only; U1-U12 and Q1-Q6 use a loopback fake |
| P3 | Coordinator (3) freeze after P1 | OPEN | Dispatch |
| P4 | Joshua's explicit go for each Q7 run | Not requested | Each Q7 run |

## §2 — Escalation mapping against the halt/resume contract

The 60 s escalation stays provider-side (C-2). IRM's Important rule set (SMS + push → 1-minute wait → call) is the escalation. HR `:59` owns the requirement.

| HR requirement (`:57-61`) | How the binding meets it | Evidence | Status |
|---|---|---|---|
| "Escalate through an alternate configured channel at 60 seconds after the first notification attempt without acknowledgment" | SMS and push first; the phone call is the alternate medium, after the 1-minute wait, unless acknowledged | Q7: rail attempt time (journal); SMS, push and call times (operator-reported) | **Met (OQ-2 RULED).** Nominal 60 s from the SMS step to the call; Q7 records the measured SMS → call lag; ≤ 90 s passes, > 90 s fails |
| "route delivery failures to remaining channels immediately" | Rail side: a publish that is not accepted routes to the next configured channel at once (#628 core). With IRM as the only delivering channel, the round records `ALL_CHANNELS_LOST` (operator default OQ-3). Provider side: the important push fires in parallel with the SMS at step 1, so one failed medium is already covered; the call at +60 s is the third | Q5; Q7 (a); U11 | **Met (OQ-3 RULED).** The fan-out is Grafana-side; the rail still sends one webhook per round (U11) |
| "Persist detection, notification attempts/provider acceptance, available delivery evidence and authenticated attendance separately" | #628 journal events; IRM gives acceptance (2xx) only | Q4 | Acceptance mapped; delivery evidence OWED (OQ-1); attendance is TB-I3 (HR `:143`) |
| "Target acknowledgment is under 60 seconds after notification" | Joshua acknowledges in IRM | PR #615 RH2. Not Q7, which must not acknowledge before the call | Not measured here |
| "No acknowledgment never restores send authority" | The channel has no broker, dispatch, arm or owner path | U8 | Met by construction |
| "Notification outbox retries carry the same incident identity and cannot dispatch broker commands" | `alert_uid` = incident key on every retry | Q3, Q6, U8 | Met; the outbox wording (P3) stays OPEN |
| "Provider-specific channels and heartbeat thresholds require qualification before live use" | Q1-Q7, plus a Q7 re-run after the free-tier fallback (OA-8) | §6 | The heartbeat is a separate card |

## §3 — Design

1. **Kind registration.** One entry only in `book_incident_notifier.py`: `CHANNEL_KINDS["grafana_irm"] = (True, True)` (needs a secret reference; delivers). The core stays provider-agnostic and does not import the channel module.
2. **`GrafanaIRMChannel`**, in a new module `ops/c1_rail/book_incident_grafana_irm.py`, satisfies the #628 `Channel` protocol (`name`, `kind = "grafana_irm"`, `publish(idempotency_key, payload) -> PublishResult`).
   - **Body** (Formatted webhook): `alert_uid` = the idempotency key. `state` = `"alerting"` always; the rail never sends `ok`, because recovery is attended (HR §3). `severity` = `"critical"` always, a module constant with no constructor or config override (**the important marker**, §0.5 item 3). `title` = `"First Passage book incident: " + reason`. `message` = reason, `detected_at` and the first 12 hex digits of the key. No `image_url`, `link_to_upstream_details`, raw `incident_id`, account, order, strategy or figure. The body passes `assert_no_secrets`.
   - **Transport:** stdlib `urllib.request`, with no new dependency. HTTPS only, default certificate verification, **redirects never followed**, a per-request timeout strictly below `NotifierConfig.publish_timeout_s` (construction refuses otherwise), and the response read capped at 64 KiB.
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
6. **Retry interaction (known hazard, OQ-1).** After IRM accepts, the job stays `pending` (there is no delivery evidence), and the core republishes with backoff and no cap (OQ-2 default). While the alert group is open, each retry joins it. **Once Joshua resolves the group in IRM, the next retry opens a new group and pages him again.** This card does not change core semantics; OQ-1 decides (§3.7 is the proposal).
7. **`record-delivery` operator CLI (OQ-1 proposal: PROPOSED, PENDING OPERATOR CHOICE; built only if Joshua picks it).** New `ops/c1_rail/book_incident_operator_cli.py`: `record-delivery <incident_key> --journal <path> --config <path>`. It loads the `NotifierConfig`, binds an inert, non-publishing channel object for each spec (so it resolves no secret reference, needs no URL and makes no request), and calls #628's `IncidentNotifier.record_delivery(key, channel, evidence_digest)` once, for the single delivering IRM channel. The digest is SHA-256 over a domain-separated record of the key, channel and local recording time, labelled operator-reported acknowledgment; it is not authenticated attendance (TB-I3, HR `:143`). It **refuses an unknown key** (exit non-zero; core `ValueError`), is **idempotent** (an already-delivered job exits 0 with no second `delivered` event; core behavior), never calls `run` or `publish`, and has no broker, dispatch, arm or owner path. A running notifier sharing the journal must tolerate the second writer; if #628's journal does not, return NEEDS_CONTEXT. Operating sequence: acknowledge in IRM → `record-delivery` → resolve in IRM. The closed job is not retried, so resolving opens no new group.

## §4 — Hypothesis and falsifier

**H:** A `grafana_irm` channel that sends every job as a Formatted-webhook alert, with `alert_uid` equal to the incident key and the fixed `severity: critical` marker, routed by Joshua to an Important-notification chain, pages him by SMS and then by phone call about 60 s later without acknowledgment, groups every retry of one incident into one alert group while that group is open, and never exposes the integration URL or changes the owner.
**Falsifier:** any publish without `severity: critical` or `state: alerting`, or with an `alert_uid` other than the incident key; two alert groups for one incident while the first is open; a Q7 run where the call does not fire without acknowledgment; the URL in any repo file, journal row, event, payload, log capture, `repr` or exception text; a followed redirect; a publish outliving `publish_timeout_s`; any owner status, incident or generation change caused by a provider outcome; or an import path from the new modules to a broker, dispatch, arm, config-write or owner-mutation surface.

## §5 — Files

**Allowed:**
- `ops/c1_rail/book_incident_grafana_irm.py` (new): `GrafanaIRMChannel`, `GrafanaIRMTransportError`, secret-reference resolution, URL validation, response mapping.
- `ops/c1_rail/book_incident_notifier.py`: **only** the `CHANNEL_KINDS["grafana_irm"]` entry and its comment.
- `ops/c1_rail/book_incident_irm_live_page.py` (new): the Q7 operator-run driver.
- `ops/c1_rail/book_incident_operator_cli.py` (new): **only if Joshua picks OQ-1's proposal** (§3.7).
- `tests/ops/test_book_incident_grafana_irm.py` (new): U1-U11 (U12 if §3.7 is built) and Q1-Q6.
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

**Gate:** the worker build passes only when U1-U11 (U12 if §3.7 is built) and Q1-Q6 are red at base and green at head (DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED, below). D-MON-1 is qualified only when Q7 also passes, during the trial and again on the free tier. Each Q7 run's verdict: **RESOLVED** (every §6.3 pass item holds); **FALSIFIED** (no call without acknowledgment, an SMS → call lag above 90 s, a second alert group, or the URL exposed); **AMBIGUOUS** (anything else, e.g. the SMS or push missing while the call fires, or throttled delivery), which needs a new go to re-run.

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
| U8 | `test_irm_modules_have_no_broker_or_owner_mutation_path`: an AST import allowlist for both new modules, as in #628 T9 |
| U9 | `test_grafana_irm_kind_needs_secret_ref_and_delivers`: `CHANNEL_KINDS["grafana_irm"] == (True, True)`; a spec without `secret_ref` is refused |
| U10 | `test_live_page_driver_refuses_without_confirmation_or_reference`: without `--confirm-live-page`, or with a missing env reference, the driver exits non-zero, makes no request and prints no URL |
| U11 | `test_one_webhook_per_round_fan_out_is_grafana_side`: across first publish, retries and restart, the loopback fake sees exactly one POST per round for the IRM channel; no SMS, push or call target appears in the body or config (OQ-3 ruling) |
| U12 | (only if §3.7 is built) `test_record_delivery_cli_refuses_unknown_key_and_is_idempotent`: an unknown key exits non-zero with no event; a pending key gets one `delivered` event and is not republished; a second call adds no event; no request is made and no secret reference is resolved |

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

**Procedure:** the §3.5 driver commits one synthetic `operator` incident on a scratch owner and publishes at t0. Joshua does **not** acknowledge until the call rings. At about t0 + 90 s the driver republishes once with the same `alert_uid`. Joshua then acknowledges in IRM, runs `record-delivery` if §3.7 is built, and resolves the alert group. The driver exits, and nothing keeps retrying.

**Pass (all):** (a) the SMS **and** the important push both arrive at step 1, and their receipt times are recorded; (b) **the phone call fires** without acknowledgment, which proves the Important rule set ran; (c) the call follows the SMS by about 60 s (nominal 60 s; **pass ≤ 90 s**, fail > 90 s; OQ-2 ruling), and the attempt-to-SMS, attempt-to-push and SMS-to-call offsets are recorded; (d) the republish creates no second alert group and no second SMS, push or call; (e) the journal shows the attempt and `provider_accepted` with times, and the actual 2xx status is recorded.

**Evidence:** the journal in the `local_artifacts/` directory Joshua chose (private), with times labelled operator-reported. No phone number, URL, stack name or region host is recorded.

**Owners:** HR `:59` (60 s escalation; qualification before live use); D-MON packet §7 items 2-3 (PR #606 `4d64e21:113-114`); PR #615 RH2 (`06efb2e:155`); coordinator (3), 2026-10-03 (the call step is asserted); OQ-2 and OQ-3 rulings, 2026-10-03 (lag bound; push at step 1). **Re-run** under a new go after the 2026-10-16 free-tier fallback (OA-8).

### Return taxonomy (worker build: U1-U11, U12 if §3.7 is built, Q1-Q6)

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
- An automated delivery-evidence producer (reading IRM alert-group state into `record_delivery`; OQ-1's alternative), and any change to the core retry semantics.
- The bearer-token requirement on the integration (OQ-4).
- Host wiring: starting the notifier in any process, `fly secrets`, `deploy/**`, arming, `dry_run`.
- The external heartbeat (PR #615 RH3), authenticated attendance and the acknowledgment API (TB-I3, HR `:143`), and acting on `ALL_CHANNELS_LOST`.
- Any provider account, spend, card or message to an external party by an agent.

## §9 — Decisions and open questions

**Recorded:** D-MON D-1 = Grafana Cloud IRM (packet `4d64e21:124`); D-2 done by Joshua; notification rules as in §0.5 item 2; every incident is sent as important (coordinator (3), 2026-10-03).
- **OQ-2 RULED YES** (HR owner coordinator (2); Joshua "this is perfect", 2026-10-03). A call about 60 s after the SMS step meets HR `:59`'s "at 60 seconds after the first notification attempt". Nominal 60 s; Q7 records the measured SMS → call lag; ≤ 90 s passes, > 90 s fails (§6.3 (c)).
- **OQ-3 RULED** (same owner and date). HR `:59`'s "route delivery failures to remaining channels immediately" is met by a **parallel step-1 channel**: Mobile push important fires with the SMS (OA-0b; §0.5 item 2), with the call at +60 s behind both. Q7 (a) asserts both step-1 media; U11 asserts the rail still sends one webhook per round.

**OPEN:**
- **OQ-1** (Joshua). The retry-after-resolve re-page (§3.6). **Coordinator (3) recommendation, PROPOSED, PENDING OPERATOR CHOICE:** build the `record-delivery <incident_key>` operator CLI (§3.7, U12): acknowledge in IRM, record delivery locally, then resolve. **Alternative:** acknowledge-only in IRM (never resolve while the rail job is pending), with an IRM API read-back card later (a second, read-only token feeding `record_delivery`). Treating IRM 2xx as terminal changes #628 semantics and the OQ-2 retry default, and is not recommended.
- **OQ-4** (Joshua). Require the service-account bearer token? It adds a second secret and needs a second `secret_ref` per channel, which is a core change. **Lean: off for this build.**
- **OQ-5** (coordinator (3) / Joshua). **Secret store convention: OWED.** The repo names none for local secrets. `.env*` and `/local_artifacts/` are gitignored, and rail secrets sit on the Fly volume, with `fly secrets set` → env as the documented hardening path (`deploy/c1_rail/README.md:97`). Interim: a process-scoped environment variable, for Q7 only.
- **OQ-6** (Q7). Unverified provider behavior: the 2xx status and body; the default Grouping Id template for Formatted webhook; whether a payload joining an open group re-notifies; whether an acknowledgment before 60 s suppresses the call (packet OQ-4; an optional second attended run under its own go); free-tier SMS and calls after 2026-10-16.
- **P3** (HR owner, from #628). Is the journal plus a bounded publish keyed by `alert_uid` HR `:61`'s "notification outbox"?

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
