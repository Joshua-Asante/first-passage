# D-MON-1: missed-heartbeat monitor for the book runtime (build card)

**Date:** 2026-10-03.
**Status:** **DRAFT — coordinator (3) freezes it after #628 merges and the D-MON-1 binding card is frozen.** Nothing here is dispatched. At freeze, coordinator (3) re-reads every anchor and records the freeze in §12.
**Base:** origin/main `a5ca41e`. Other revisions read: #628 at `origin/claude/book-incident-notifier` `60ba482` (OPEN); the binding card at `origin/claude/dmon-grafana-binding-card` `d54972f` (DRAFT); PR #606 at `4d64e21` (PROPOSED); PR #615 at `06efb2e` (PROPOSED); #633 (TB-I3 card) at `origin/claude/tb-i3-card` `4dce572` (DRAFT); the dot intake card at `origin/claude/dmon-dot-intake-card` `aaee242` (DRAFT). Line anchors on those branches hold only at those heads.
**Brief type:** CC handoff. A code build (TDD) inside a named file boundary, plus one live check that Joshua runs while attending.
**Parent:** deployment checklist T13, bullet "Verify real notification delivery, failure/escalation, external heartbeat and durable acknowledgment" (`docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md:271`); D-MON (`:599`). D-MON-1 scope is "rail-side bounded publish plus heartbeat (TB-I3 scope)". The binding card covers the publish; this card covers the heartbeat.
**Finding being closed:** HR `:61`: "Independent missed-heartbeat monitoring covers a silent runtime". HR `:34`: on a storage failure, "expose failure through independent monitoring". Nothing built meets either. The daemon's `heartbeat.py` serves a `GET /` snapshot that someone has to pull. It is not an external monitor (H5(b) note `docs/notes/2026-09-27-h5b-attended-incident-rehearsal.md:67`). The book loop has no host, no pinger and no threshold.
**Folded (2026-10-03):** the four heartbeat P2s of coordinator (3)'s review r03 (§3.3 (b), §3.5, §3.6, §0.5 item 7 and P7); and the HR `:61` halt/resume owner ruling by coordinator (2), condition 4: the missed-heartbeat monitor covers the **notifier's** liveness as well as the runtime's, owed before any armed session (§0.5 item 8, §3.9).
**Selected outcome:** Two `HeartbeatPinger` instances. One is driven by the book runtime's loop progress, the other by the #628 notifier's loop progress (its liveness hook). Each pings its **own** Grafana IRM heartbeat integration, separate from the incident integration and from each other, and IRM pages Joshua through his Important chain when either one's pings stop. Qualified by unit tests, synthetic silent-runtime and silent-notifier tests against loopback fake receivers, and attended live checks (HB-L1, HB-L2).
**Ownership:** One Opus/CC worker builds it (§11). Joshua performs the §0.6 operator acts and runs HB-L1. Coordinator (3) accepts the build. Joshua merges.
**Return boundary:** A pushed `claude/*` branch that touches only the §5 allowed files, or a precise blocker. HB-L1 is not part of the worker's return.

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
  - no_host_wiring
  - no_rail_deploy
  - no_rail_arm
  - no_account_traffic
  - no_broker_vendor_firm_or_provider_contact
  - no_external_send
  - no_provider_account_or_spend
  - no_secret_value_seen_or_handled_by_agent
  - no_credentials_or_private_data_in_repo
  - live_check_is_operator_performed_with_go_per_run
  - no_operator_decision_taken
acceptance:
  - "Every red-first test in §6.1 and §6.2 (H1-H12, HQ1-HQ9) fails at the base revision (or is absent) and passes at the returned head; the failing-first run is recorded"
  - "The §7 regression set passes unchanged"
  - "git diff --stat origin/main...HEAD lists only §5 allowed files"
  - "python -I scripts/fp.py check: status completed, exit 0, source stable; or a pre-existing failure disclosed with its reproduction on unmodified origin/main"
  - "No token-shaped heartbeat URL, service-account token, stack name, phone number or account identifier appears in the diff (§10 hook)"
```

## §0 — Read first (report before writing code; otherwise `NEEDS_CONTEXT`)

| Input | Where | Read |
|---|---|---|
| Halt/resume contract (HR; accepted) | `docs/spec/2026-09-14-tb-s3-halt-resume-contract.md` | §2 `:34` (storage failure → independent monitoring), `:35`, `:36` (source timeout `2 * bar_period + 30 seconds`); §3 `:49`; *Attendance and notification* `:57` (the operator verifies alert channels before arming; "No UI connection or periodic runtime heartbeat is proof of operator presence"), `:59` ("heartbeat thresholds require qualification before live use"), `:61`; §7 `:143` (TB-I3 owns watchdogs) |
| Phase 5 plan WP2 | `docs/superpowers/plans/2026-09-16-phase5-attended-operations.md` | `:67` ("heartbeat monitoring outside the trading host's failure domain"), `:72`, `:73`, `:74`, `:76` |
| Timing owners | `ops/c1_signal_daemon/book_protocol.py:10-11` (`BAR_PERIOD`, `BAR_SLACK`); `ops/c1_signal_daemon/book_evaluate_loop.py:3-5`, `:29-58` (`step`; the source-silence call at `:33`); `ops/c1_signal_daemon/book_runtime.py:351`, `:439`, `:483` (barrier window); `ops/c1_rail/book_protection_owner.py:24`, `:156`, `:177-187` (`PROTECTION_PERIOD`, protection deadlines) | constants and call sites only |
| Owner read surface | `ops/c1_rail/book_account_owner.py` | `status()` `:982`; `authority` `:791`; `check_source_silence` `:1029` |
| Legacy daemon heartbeat (not edited) | `ops/c1_signal_daemon/heartbeat.py`, `http_status.py`, `daemon.py:116-151` | the `GET /` snapshot and `poll_interval_s`; S2b build ADR `docs/adr/2026-08-08-s2b-signal-daemon-build.md:51` |
| Loop test fixtures | `tests/ops/test_book_loop_continuation.py:9-25`, `tests/ops/test_book_ingress_validation.py:245-251` | how a `FourLegEvaluateLoop` is built on synthetic sources |
| #628 notifier (independence and liveness) | `git show 60ba482:ops/c1_rail/book_incident_notifier.py` | module docstring `:1-16` (the heartbeat is out of #628's scope); `NotifierStoreError` `:61`; `_journal` `:239-256`; `run_once` `:326`; `_bounded_publish` `:392-410` (the bounded-thread pattern). The liveness hook (P8) is not at `60ba482`; read it at the amended head |
| Dot intake card (DRAFT) | `git show aaee242:docs/briefs/handoffs/2026-10-03-dmon-dot-incident-intake-card-DRAFT.md` | OA-D3 `:69` (integrations filter); §3.6 `:118` (the single hyper addendum); §8 `:197` |
| TB-I3 card #633 (DRAFT) | `git show 4dce572:docs/briefs/handoffs/2026-10-03-tb-i3-synthetic-interlock-card-DRAFT.md` | §5 Forbidden `:212` (`ops/c1_signal_daemon/**`) |
| Binding card (DRAFT) | `git show d54972f:docs/briefs/handoffs/2026-10-03-dmon-grafana-irm-binding-card-DRAFT.md` | §0.5 items 2-4; §0.6 OA-2, OA-3, OA-5; §3.2 transport; §3.3 secret reference; §9 OQ-5 |
| D-MON packet (PROPOSED) | `git show 4d64e21:docs/notes/2026-10-02-d-mon-channel-options-packet.md` | N9, N10 `:23-24`; option A heartbeat `:65`; constraints §6 `:99-106`; qualification §7 item 1 `:112`; OQ-4, OQ-5 `:131-132` |
| T13 procedure (PROPOSED) | `git show 06efb2e:docs/briefs/handoffs/2026-10-02-t13-first-session-attended-procedure-DRAFT.md` | `:95` (heartbeat binding to rail progress is uncarded TB-I3 work); RH3 `:156`; RH6 `:159` |
| Dot charter | `docs/notes/2026-10-02-dot-deployment-responsibility.md` | `:19`, `:57`, `:61` |
| Rules | `AGENTS.md` | launcher `:222`; *Configuration as code* `:229-238` (credentials `:236`) |

**The report states:** the dispatch revision; whether #628 merged and at which commit; whether the binding card is frozen; whether #628's liveness hook landed, with its name, return type, clock and anchor; every anchor above that moved; whether Joshua has reported operator acts OA-H1 to OA-H5 done (only HB-L1 needs them).

## §0.5 — Clarifications and recorded facts

1. **Provider behaviour (public docs, §13).** Heartbeat monitoring is set per integration under **More options → Heartbeat Settings**. Joshua sets the interval there and copies the endpoint URL; **Reset** turns it off [H1] and has no automatic restore, so no planned stop uses it (§3.5). It is available on several integration types, among them "Webhook / Formatted Webhook" [H1]. The timeout ranges from "1 minute and 24 hours"; "If no request arrives within the timeout, IRM creates an alert"; "When heartbeat resumes, the alert auto-resolves". The docs' tip is to set the timeout longer than the ping interval [H2]. The alert from a missed heartbeat goes through that integration's routes and escalation [H1]. The documented URL pattern is `…/integrations/v1/alertmanager/<id>/heartbeat/`, and the heartbeat is sent by POST [H3]. **UNVERIFIED:** the exact URL path for a Formatted Webhook integration, whether GET is also accepted, the success status code and body, the payload of the alert that a missed heartbeat raises, which interval values the UI actually offers, whether the UI shows the time of the last heartbeat received (§3.5 check (iii)), and whether the plan limits the number of integrations (this card adds two). HB-L1 confirms each of these. WebFetch returns a model's summary of each page, so the quoted phrases are reader-summary quotes.
2. **Maintenance mode [H1, H2].** An integration can be put into maintenance as "Silence escalations", "Group alerts" or "Disable alerts" for a set duration. It ends by itself when the duration runs out. This is how a planned stop avoids a page (§3.5).
3. **Notification chain (binding card §0.5 item 2, coordinator (3) 2026-10-03).** Default rules send SMS only. Important rules send SMS, wait 1 minute, then place a call. **Operator rulings via coordinator (2), 2026-10-03 ("this is perfect"):** OQ-2: nominal 60 s; the measured SMS-to-call lag is recorded, and a lag over 90 s fails. OQ-3: an IRM mobile-app "important" push is added as a **parallel** step-1 channel that fires with the SMS. Joshua pairs the app by QR code (Profile → Mobile app), and coordinator (2) adds the push to his Important chain after pairing. A heartbeat page inherits this chain as long as the heartbeat integration routes to it (OA-H2).
4. **The book loop has no host.** `FourLegEvaluateLoop` "deliberately has no config constructor, HTTP endpoint, sender, or daemon CLI registration" (`book_evaluate_loop.py:3-5`). The owner and the dispatch call run inside the loop's process (`book_runtime.py:17-18` imports `BookAccountOwner` and `handle_book_action`). So this card builds the component and a wrapper the host will call. **Host wiring is TB-I3** (HR `:143`; PR #615 `:95`), and silent-runtime coverage is not live until a host calls the wrapper.
5. **Constraints carried from the D-MON packet §6 (`4d64e21:99-106`).** "The heartbeat is tied to observed rail and daemon progress, not a free-running timer". "A failed durable incident write stops the heartbeat or sends a failure signal". "Heartbeat recovery never clears a latched incident". The detection threshold is separate from the 60 s escalation, and both are qualified (N10).
6. **Operator direction (Joshua via coordinator (2), 2026-10-03; recorded as direction, not a gate change):** "broad autonomy, robust error handling and alerts … in addition to notifying me, it can notify my dot and it can start working on it so that we get to a solution faster, i merely need to review and approve." The dot is `hyper` (charter `docs/notes/2026-10-02-dot-deployment-responsibility.md`; a scoped coordinator seat). The dot can be contacted through the Codex coordinator (2) chat; incident traffic goes only through that chat, never public PR comments (dot card §3.6 items 5, 7). These still stand: the first session is attended (T13); every armed session needs its own GO; the dot never merges, ratifies, spends, arms or trades (charter `:61`); every order and recovery act stays Joshua's (D-MON-2/3/4). Applied in §3.6.
7. **Independence (coordinator (3) direction, 2026-10-03; reworded per review r03).** What this card enforces: neither heartbeat module imports the notifier or the IRM channel module (H8), the pinger has no journal and never touches the notifier's journal or the owner DB, and the heartbeats use their own references and integrations, never the incident integration's. What it cannot enforce, because host placement is out of scope: **a constraint carried to TB-I3** — the notifier never runs on the runtime loop thread, so a slow publish or a `NotifierStoreError` cannot delay `step`; and the notifier heartbeat is marked from the notifier's own loop, never from the runtime loop thread (§3.9). TB-I3 states how its wiring meets this; #633 as drafted does not cover it (P7).
8. **HR `:61` ruling, condition 4 (halt/resume owner via coordinator (2), 2026-10-03).** The missed-heartbeat monitor covers the notifier's liveness as well as the runtime's; a dead notifier beside a live runtime is otherwise silent. Owed before any armed session. #628 is being amended to expose a liveness hook (a last-loop timestamp) on `claude/book-incident-notifier` (P8). A lost incidents store is also a heartbeat case (§3.9).

A contradicted fact, a missing producer or a needed edit outside §5 returns NEEDS_CONTEXT.

## §0.6 — Operator acts (Joshua only; the agent never sees or handles the URL)

| ID | Act | Needed by |
|---|---|---|
| OA-H1 | In his Grafana stack, create **two** more IRM integrations of type Formatted Webhook (or Webhook), one named for the runtime heartbeat and one for the notifier heartbeat. In each, open **More options → Heartbeat Settings**, set the interval to that side's frozen T (§3.3, §3.9) and copy the heartbeat endpoint URL [H1]. Nothing ever sends alerts to either integration's alert URL. | HB-L1, HB-L2 |
| OA-H2 | Point each heartbeat integration's catch-all route at the same escalation chain that the binding card's OA-2 creates: one step that notifies Joshua with **Important notifications**. The alert from a missed heartbeat carries no `severity` marker, so the catch-all route has to reach the Important set, or the call never fires. | HB-L1, HB-L2 |
| OA-H3 | Store the runtime heartbeat URL under the reference **`FP_DMON_GRAFANA_IRM_HEARTBEAT_URL`** and the notifier heartbeat URL under **`FP_DMON_GRAFANA_IRM_NOTIFIER_HEARTBEAT_URL`**. Config holds only the `env:` references. The store convention is OWED (binding card OQ-5). For HB-L1 in the meantime, Joshua sets a process-scoped environment variable in his own terminal. Neither URL ever goes into chat, git, a card, a PR, a log, an agent prompt or `glm_agent`. | HB-L1, HB-L2 |
| OA-H4 | Tell the coordinator only "heartbeat integrations created; routes and references set; T runtime = <value>, T notifier = <value>". No URL, stack name, region host or phone number. | HB-L1, HB-L2 |
| OA-H5 | **Each HB-L1 or HB-L2 run:** an explicit go in chat for that run. He attends with the phone at hand, runs the driver himself and reports only the times the push, SMS and call arrived. Afterwards he acknowledges and resolves the alert group, then puts the drilled integration into maintenance **with a duration** (§3.5); never Reset. | HB-L1, HB-L2 |
| OA-H6 | Pair the IRM mobile app (QR, Profile → Mobile app). Coordinator (2) adds the parallel push step after pairing (§0.5 item 3). | HB-L1 push item |

## §1 — Goal, scope, prerequisites

**Goal.** When the book runtime goes silent, or the notifier dies while the runtime lives, Joshua is paged within a qualified threshold, by push and SMS at once and by a call 60 s later unless he acknowledges. Silent here means the process died, the host went down, the network was lost, the loop hung, or owner storage failed. The page goes through a monitor outside the trading host's failure domain (Phase 5 WP2 `:67`). It does not depend on the notifier, the owner DB or the runtime being able to say anything. The page names which side went silent (§3.9).

**Scope.** `HeartbeatPinger`; a `step_with_heartbeat` wrapper around `FourLegEvaluateLoop.step`; a `notifier_round_with_heartbeat` wrapper around the notifier's `run_once` and liveness hook (§3.9); secret-reference resolution and URL validation; a bounded, non-blocking transport; unit and synthetic tests; an operator-run live-check driver. No host wiring, no edit to the loop or the owner, no deploy.

| ID | Prerequisite | State at draft | Blocks |
|---|---|---|---|
| P1 | #628 merged (independence tests in H8 name its module) | **OPEN** (`60ba482`) | Freeze |
| P2 | Binding card frozen; its OA-2 chain exists (OA-H2 reuses it) | **OPEN** (DRAFT `d54972f`) | HB-L1 |
| P3 | Heartbeat integration and reference created by Joshua (OA-H1 to OA-H4) | **OPEN** | HB-L1 only; tests use a loopback fake |
| P4 | T and P frozen for both heartbeats (§3.3, §3.9). Inputs owed to TB-I3: the runtime's `max_step_interval` and `max_step_duration`, and the notifier's loop interval and round duration | **OWED** | Freeze |
| P5 | Coordinator (3) freeze | OPEN | Dispatch |
| P6 | Joshua's go for each HB-L1 run | Not requested | Each HB-L1 run |
| P7 | TB-I3 host wiring calls `step_with_heartbeat` and meets the §0.5 item 7 placement constraint | **Uncarded.** PR #615 `:95`. #633 (TB-I3 synthetic-interlock card, DRAFT `4dce572`) forbids `ops/c1_signal_daemon/**` (`:212`), so it does not cover heartbeat wiring; a separate card or a #633 amendment is owed | Coverage of any armed session |
| P8 | #628 amended to expose the notifier liveness hook (`claude/book-incident-notifier`; `60ba482` at draft, amendment pending) | **OPEN** | Freeze (HQ6-HQ9 name it) |
| P9 | The notifier's host wiring calls `notifier_round_with_heartbeat` from the notifier's own loop | **Uncarded** (same gap as P7) | Any armed session (§0.5 item 8) |

## §2 — What "silent runtime" covers

| Failure | Pings | Detected by | Notes |
|---|---|---|---|
| Process dead (crash, OOM, kill) | stop | heartbeat expiry | |
| Host down or rebooting | stop | heartbeat expiry | Grafana Cloud sits outside the host's failure domain (WP2 `:67`) |
| Outbound network lost | fail | heartbeat expiry | The notifier cannot publish either, so this is the only path that pages |
| Loop hung (deadlock, blocked call) | stop | heartbeat expiry | Covered only because pings are tied to progress (§0.5 item 5); a free-running timer would hide this |
| Owner storage unavailable (HR `:34`) | stop | heartbeat expiry | `step` raises or `status()` fails, so no progress mark is set (§3.1) |
| Runtime alive in HALTED/INTERVENTION | continue | the notifier pages the incident | The runtime keeps collecting read-only (HR §3). A heartbeat page here would only add noise |
| Feed silent while the runtime is alive | continue | owner source-silence incident (`book_evaluate_loop.py:33`; HR `:36`) | The notifier's path, not this one |
| Notifier process dead, or its loop hung, while the runtime is alive | runtime: continue; notifier: stop | notifier heartbeat expiry | §3.9; §0.5 item 8 |
| Incidents store or notifier journal lost or unreadable | notifier: stop | notifier heartbeat expiry | `run_once` raises (`NotifierStoreError`, or `read_incidents` raises), so no mark (§3.9) |
| Incidents store silently replaced by an empty, readable one | continue | **nothing** | Not a heartbeat case; OQ-H6 |
| Grafana IRM itself down | n/a | **nothing** | D-MON packet OQ-5 (`4d64e21:132`); out of scope |
| Another process pinging with the URL | continue | **nothing** | Prevented only by secret custody (OA-H3) |

## §3 — Design

1. **Progress seam, with no edit to the loop.** New module `ops/c1_signal_daemon/book_heartbeat.py`:
   `step_with_heartbeat(loop, pinger, *, now, read_status)` calls `loop.step(now=now)`, then `read_status()` (the host binds it to the owner's `status()`), then `pinger.mark_progress()`. It returns the step result unchanged. If `step` or `read_status` raises, the exception propagates unchanged and no mark is set. The pinger never catches a loop error. A HALTED or INTERVENTION authority still counts as progress (§2).
2. **`HeartbeatPinger`: progress-driven, with no timer thread.** `mark_progress()` returns at once. It records a monotonic progress time. It starts **one** short-lived daemon thread for **one** bounded send only when no send is in flight and the last send began at least P ago. Otherwise it does nothing; nothing is queued. When marks stop, sends stop, so no send can outlive progress. A send failure (timeout, refusal, 3xx/4xx/5xx, DNS or TLS failure) increments an in-memory counter and logs the exception class only. It never raises into the loop and never delays `mark_progress`. The pinger has no journal and no persisted state, and nothing touches the owner DB.
3. **Thresholds (P4, OWED).** Values the owners give:
   - The runtime's shortest in-process deadline, which a dead runtime can no longer enforce, is `PROTECTION_PERIOD` = 15 min (`book_protection_owner.py:24`, `:156`). The barrier window, `BAR_PERIOD + BAR_SLACK` = 15 min 30 s (`book_protocol.py:10-11`; `book_runtime.py:351`), and the source timeout, 30 min 30 s (HR `:36`), are longer.
   - The provider's minimum timeout is 1 minute [H2].
   - The book loop has no step cadence. It has no config constructor (`book_evaluate_loop.py:3-5`), so `max_step_interval` (the longest gap between step starts on a healthy host) is **OWED to TB-I3**. The legacy daemon's `poll_interval_s` (S2b ADR `:51`) does not apply to it.

   **Constraints the freeze must satisfy:** (a) `ping_timeout < P`; (b) `P + max_step_interval + max_step_duration + ping_timeout < T`, so a healthy loop never expires. P is only a minimum spacing between pings; a mark just before P has passed defers the send by one more gap between marks, at most `max_step_interval + max_step_duration` (example: P = 50 s, steps every 30 s, T = 60 s, timeout 5 s passes the max form but sends at 0 s and 60 s and arrives up to 65 s). `max_step_interval` and `max_step_duration` are **OWED to TB-I3** (P4); the duration includes any bounded dispatch call inside `step`; (c) worst-case page latency, `T` + IRM ingestion + the chain (push and SMS at once, the call at +60 s, fail above 90 s), stays below `PROTECTION_PERIOD`, so a silent runtime pages no later than the earliest deadline it would have enforced.

   **Proposal (for coordinator (3) to freeze, and qualified under HR `:59`):** T = 1 minute, the provider floor. P comes from the TB-I3 `max_step_interval` and constraint (b); if `max_step_interval` leaves no room under 1 minute, T rises to the smallest value that meets (b), subject to (c). The docs' 1-minute interval with a 50 s repeat [H3] is a provider example, not a selection. The trade-off: a short T can raise false pages on transient network blips, and each false page is a push, an SMS and a call. OQ-H1.
4. **Secret and transport.** The pinger is constructed with `secret_ref` and resolves it once. `env:NAME` reads the environment, and a missing variable raises a config error that names the reference. `secret:` is refused until a store convention exists. Validation rules, which name the failed rule and never the URL: `https`, no userinfo, host ending `.grafana.net`, path ending `/heartbeat/`. The path rule is UNVERIFIED for Formatted Webhook; HB-L1 confirms it, and a mismatch means NEEDS_CONTEXT. A `http://127.0.0.1` allowance for tests is a constructor flag, off by default. The URL lives in one private attribute and never appears in `repr`, `str`, exception text, logs or counters. Transport: stdlib `urllib.request`, method `POST` with an empty body [H3]; an HTTPS error is mapped, never propagated; redirects are never followed; the response read is capped at 64 KiB. The transport is **written in this module and is not imported from the IRM channel module** (§0.5 item 7). The duplication of about 20 lines is deliberate.
5. **When it pings: whenever the bound loop runs, not only while armed (recommended).** Reasons: (i) the risk is just as real in INTERVENTION, which can outlast the arm (HR §3; disarm comes only after proven recovery); (ii) a pinger gated on arming would have to read the arming config, a forbidden surface, and a misread would silence the monitor; (iii) HR `:57` requires the alert channels to be verified **before** arming, which takes live pings before the arm. **Operating bracket (for PR #615 / T13, not built here):**
   - *Pre-arm check (both heartbeat integrations):* Joshua confirms (i) maintenance is off; (ii) the heartbeat is enabled at the frozen T; (iii) a heartbeat arrived within the last T. "No open heartbeat alert" alone is not enough: it also holds while the integration is in maintenance ("Disable alerts" ignores incoming alerts) or after a Reset. If the UI does not show (iii) (UNVERIFIED, §0.5 item 1), HB-L1 records the substitute read.
   - *Planned stop:* only after the disarm read-back and proven flatness (HR §3). Joshua puts both heartbeat integrations into maintenance **with a duration** covering the stop [H1, H2], which ends by itself, and then stops the processes. Never Reset: it has no automatic restore. The incident integration stays out of maintenance, so incident pages are never muted.
   - *Next session:* if maintenance is still running, he ends it, then runs the pre-arm check.

   *Alternative:* ping only while armed. Not recommended, for reasons (i) to (iii) above.
6. **Dot notification (Joshua's 2026-10-03 direction; designed here, not built).** A heartbeat page means the side that went silent cannot report, so Joshua checks the platform himself. Notifying the dot never replaces his attendance, the 60 s acknowledgment target (HR `:59`) or any recovery act. **The dot card's §3.6 (`aaee242:118`, as folded) is the single hyper addendum;** this card adds no permissions of its own and no separate permitted-response list. Proposed paths, for OQ-H4:
   - (a) **Manual forward, no build.** Joshua acknowledges in IRM and then tells the dot "heartbeat page (runtime | notifier) at <time>" through the Codex coordinator (2) chat. Proposed for the first attended session.
   - (b) **Add both heartbeat integrations to OA-D3's integrations filter** (dot card `:69`), as its §8 (`:197`) anticipates. The intake then arrives through the dot card's path under its §3.6; no new token or card.
   - (c) **Read-only IRM API polling by the dot.** Needs a second, read-only token: Joshua's act, and a separate card.
7. **Config as code (AGENTS.md `:229-238`).** Instance bindings: runtime `{"secret_ref": "env:FP_DMON_GRAFANA_IRM_HEARTBEAT_URL", "period_s": P, "timeout_s": <ping_timeout>}`; notifier `{"secret_ref": "env:FP_DMON_GRAFANA_IRM_NOTIFIER_HEARTBEAT_URL", "period_s": P_n, "timeout_s": <ping_timeout>}`. `build_pingers(runtime_binding, notifier_binding)` refuses equal references or equal resolved URLs (one live side would otherwise mask the other), naming the rule and never the URL. It lives in the driver's arguments and in tests. **No instance file is committed** (host wiring is TB-I3).
8. **Live-check driver**, new `ops/c1_signal_daemon/book_heartbeat_live_check.py` (HB-L1 only). `--side runtime|notifier` selects the reference. It builds the pinger from that environment reference and calls `mark_progress()` on a fixed loop for a duration Joshua chooses. Then it stops pinging and keeps the process alive for a second chosen duration. It prints the times of the last ping and of each send outcome (no URL). It refuses to run without `--confirm-live-check` or with a missing reference. It never builds an owner or a notifier and never touches account, arm or broker surfaces. For HB-L2, Joshua runs two driver processes, one per side.
9. **Notifier heartbeat (HR `:61` ruling condition 4).**
   - **Choice: two separate heartbeats, not one combined.** A combined ping (only when both the runtime step and the notifier loop advanced in their windows) was considered and rejected: (i) the alert cannot say which side died, and the responses differ (silent runtime: check the host and process; dead notifier: the runtime may still trade while incidents go unpaged); (ii) one process would have to observe the other's progress, coupling them against §0.5 item 7, and the combined pinger would share the failure domain of whichever thread hosts it; (iii) one T must cover the slower cadence of the two, so the faster side is detected later. Cost: one more integration, one more reference and one more drill, all Joshua's acts.
   - **Seam.** `notifier_round_with_heartbeat(notifier, pinger)` calls `notifier.run_once()`, then reads the notifier's liveness hook (P8), then calls `pinger.mark_progress()` only if the last-loop timestamp **advanced** since this wrapper's previous call. If `run_once` or the hook raises, the exception propagates unchanged and no mark is set. It is duck-typed: the module still imports nothing from the notifier (H8). The host calls it from the notifier's own loop, never from the runtime loop thread (§0.5 item 7; P9).
   - **Store loss.** If the incidents store (`read_incidents`) or the notifier's journal is lost or unreadable, `run_once` raises (`NotifierStoreError` or the reader's exception), so the notifier heartbeat stops and pages. A store silently replaced by an empty, readable one is not detectable this way (OQ-H6).
   - **Threshold rule (P4, OQ-H1).** Same form as §3.3: (a) `ping_timeout < P_n`; (b) `P_n + max_notifier_loop_interval + max_round_duration + ping_timeout < T_n`, where `max_round_duration` includes every bounded publish in one `run_once` (the `_bounded_publish` timeout times the channels published per round); (c) `T_n` + IRM ingestion + the chain stays below `PROTECTION_PERIOD`. The loop interval and round duration are **OWED** to the notifier's host-wiring owner (P9). Lean: T_n = 1 minute if (b) allows it.

## §4 — Hypothesis and falsifier

**H:** A pinger that sends only on loop progress, through a separate IRM heartbeat integration routed to Joshua's Important chain, keeps a healthy loop free of heartbeat alerts. It pages within T plus the measured chain latency when the loop stops, hangs or loses storage or network. A second pinger on the notifier's loop progress pages within T_n when the notifier dies, hangs or loses its store while the runtime lives, and the two alerts are distinguishable. Neither blocks or alters the loop, the owner or the notifier.
**Falsifier:** any of the following.
- A ping sent after progress stopped, or sent when `step` or `read_status` raised.
- `mark_progress` or a failing send delaying a step by more than a bounded constant, or raising into it.
- A healthy synthetic loop expiring the fake receiver.
- A stalled notifier beside a live runtime with no notifier-side expiry, or either side's stall expiring the other side's receiver.
- An expiry that clears or changes any owner incident, status or generation.
- An import path to the notifier, the IRM channel module, a broker, dispatch, arm, config-write or owner-mutation surface.
- The URL in any file, log, `repr` or exception.
- An HB-L1 or HB-L2 run where stopping the pings brings no call without acknowledgment.

## §5 — Files

**Allowed:**
- `ops/c1_signal_daemon/book_heartbeat.py` (new): `HeartbeatPinger`, `step_with_heartbeat`, `notifier_round_with_heartbeat`, `build_pingers`, reference resolution, URL validation, transport.
- `ops/c1_signal_daemon/book_heartbeat_live_check.py` (new): the HB-L1/HB-L2 driver.
- `tests/ops/test_book_heartbeat.py` (new): H1-H12 and HQ1-HQ9. Tests may import #628's `IncidentNotifier` and `FakeChannel`; the H8 allowlist covers the two new modules only.
- This card: the §12 freeze record and the executor return only.

**Forbidden (stop and return if a change seems needed):**
- T00/P7 closure: `docs/briefs/handoffs/2026-09-24-tradeify-t00-p7-closure.md`; `ops/c1_rail/qualification/p7_driver.py`, `p7_evidence.py`; `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/**`.
- Qualification: `ops/c1_rail/qualification/**`, `tests/ops/qualification/**`, `docs/notes/2026-09-29-s5-c3-record/**`.
- Risk controls and locked surfaces: `core/dd_protection.py`, `core/firm_rules.py`, `core/strategies/**`, every `*.pine`, and `ops/c1_signal_daemon/ports/**` (never read, AGENTS.md `:197`).
- Arming and deploy: `ops/c1_rail/c1_rail_arm.py`, `ops/c1_rail/write_volume_config.py`, `ops/c1_rail/operator_keys.json`, `deploy/**`, `fly.toml`, `.env*`. No deploy edit is needed: the card wires no host. A host or deploy change belongs to the TB-I3 card, for Joshua.
- The loop and its owners: `book_evaluate_loop.py`, `book_runtime.py`, `daemon.py`, `heartbeat.py`, `http_status.py`, `evaluate_loop.py`, `book_account_owner.py` and every other `ops/c1_rail/book_*.py`.
- The notifier path: `book_incident_notifier.py`, `book_incident_grafana_irm.py`, `book_incident_irm_live_page.py`, `c1_rail_listener.py`, `c1_rail_http_server.py`, `c1_rail_telemetry.py` (import `assert_no_secrets` only, if needed), `book_halt.py`. Existing tests are not edited.
- Governance docs: `AGENTS.md`, `STATE.md`, `PIPELINES.md`, `REPO_MAP.md`, `docs/adr/**`, `docs/spec/**` (HR included), the checklist, the Phase 5 plan, the #628 card, the binding card, and the PR #606 and #615 drafts.
- `.claude/settings.json`, `scripts/gates.yml`, `scripts/check_durable_store_pragmas.py`.
- `local_artifacts/**`: never committed, and never read for secrets.

## §6 — Tests, qualification and return taxonomy

**Gate:** the worker build passes only when H1-H12 and HQ1-HQ9 are red at base and green at head. The worker returns DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT or BLOCKED, as defined under *Return taxonomy* below. The runtime heartbeat is qualified only when HB-L1 also passes, and the notifier heartbeat only when HB-L2 passes, with both T and P frozen. HB-L1 and HB-L2 run during the trial and again on the free tier after 2026-10-16 (binding card OA-8). Each HB-L1 or HB-L2 run's verdict:
- **RESOLVED:** every §6.3 pass item holds.
- **FALSIFIED:** no page after pings stop, no call without acknowledgment, or the URL exposed.
- **AMBIGUOUS:** anything else, such as a missing SMS while the call fires, throttling, or an unconfirmed URL or method. A new go is needed to re-run.

### §6.1 Unit tests (fake clock; loopback fake receiver on 127.0.0.1 with the fixture token `fake-token`; no other network)

| ID | Test |
|---|---|
| H1 | `test_ping_only_after_step_and_status_succeed` |
| H2 | `test_no_mark_when_step_or_status_raises`: the exception propagates unchanged; no send |
| H3 | `test_intervention_and_halted_still_mark_progress` |
| H4 | `test_rate_limited_to_one_send_per_period`: steps every second; sends at most one per P; none queued while a send is in flight |
| H5 | `test_sends_stop_when_progress_stops`: no send more than P after the last mark (no free-running timer) |
| H6 | `test_send_failure_never_blocks_or_raises`: a hanging endpoint, 3xx/4xx/5xx, refused connection; `mark_progress` returns within a bounded constant; the counter increments; the log holds the class name only |
| H7 | `test_secret_ref_resolution_and_url_never_exposed`: `env:` resolves; a missing variable names the reference only; `secret:` is refused; the URL is absent from `repr`, `str`, exceptions, logs and counters |
| H8 | `test_heartbeat_modules_import_allowlist`: an AST allowlist over both new modules. They import nothing from `book_incident_notifier`, `book_incident_grafana_irm`, broker, dispatch, arm, config-write or owner-mutation modules, and no `sqlite3` |
| H9 | `test_no_arming_state_read`: no reference to `dry_run`, `armed_until` or the arm/config modules |
| H10 | `test_url_validation_and_no_redirect`: plain http without the flag, userinfo, a foreign host, a non-`/heartbeat/` path; a 302 is not followed |
| H11 | `test_live_check_refuses_without_confirmation_or_reference`: exits non-zero, sends nothing, prints no URL |
| H12 | `test_build_pingers_refuses_shared_reference_or_url`: equal references or equal resolved URLs refused; the error names the rule, not the URL |

### §6.2 Synthetic silent-runtime and silent-notifier qualification (a real `FourLegEvaluateLoop` on synthetic sources, as in `test_book_loop_continuation.py`, → `step_with_heartbeat` → loopback fake receiver R; for HQ6-HQ9 also a real #628 `IncidentNotifier` with `FakeChannel` → `notifier_round_with_heartbeat` → a second fake receiver N; each expires after its T on a fake clock)

| ID | Test | Pass | Owners |
|---|---|---|---|
| HQ1 | `test_hq1_stopped_loop_expires_and_resume_restores` | Steady stepping: no expiry. Steps stop: expiry after T. Steps resume: restored. Owner `incidents` and `status()` are equal across expiry and restore | HR `:61`; packet §6 ("recovery never clears a latched incident"); [H2] auto-resolve |
| HQ2 | `test_hq2_hung_step_expires`: `step` blocks on a held lock | Expiry after T | packet §6 (progress, not a timer) |
| HQ3 | `test_hq3_owner_storage_failure_expires`: the owner DB is made unreadable | `step` or `status()` raises; no send; expiry after T | HR `:34`; WP2 `:76` |
| HQ4 | `test_hq4_receiver_unreachable_leaves_loop_timing_unchanged` | Step durations stay within a bounded constant of the baseline; no exception reaches the loop | WP2 `:76` ("Notification failure cannot enable or block the durable halt") |
| HQ5 | `test_hq5_runtime_pinger_independent_of_notifier`: no notifier exists, or its journal is unavailable | The runtime pinger is unaffected | §0.5 item 7 |
| HQ6 | `test_hq6_notifier_stalled_runtime_alive_pages_notifier_only`: `run_once` stops being called, or blocks, while the loop steps | N expires after T_n; R does not expire | §0.5 item 8 |
| HQ7 | `test_hq7_runtime_stalled_notifier_alive_pages_runtime_only` | R expires after T; N does not expire | HR `:61` |
| HQ8 | `test_hq8_both_alive_no_page`: both stepping at their cadences over several T | Neither receiver expires, including a cadence where P is just above a multiple of the step interval (P = 50 s, steps every 30 s) | §3.3 (b), §3.9 (b) |
| HQ9 | `test_hq9_incidents_store_lost_pages_notifier`: `read_incidents` raises, or the notifier journal is made unavailable; and separately, the liveness timestamp stops advancing while `run_once` returns | No mark; N expires after T_n; R unaffected | §3.9; §0.5 item 8 |

### §6.3 HB-L1: live silent-runtime page (outward-facing: a real push, SMS and call to Joshua's phone)

**Authorization:** Joshua's explicit go in chat **for each run**. He attends, and **he runs the driver himself**, so the agent never holds the URL. Prerequisites P2, P3, P4 and P6. The account is disarmed, no runtime is involved, and there is no account traffic.

**Procedure:** He runs the driver with pings for at least 2T, then stops the pings. He does not acknowledge until the call rings. He then restarts pings and watches for auto-resolve. Afterwards he acknowledges or resolves if needed, then puts the integration into maintenance with a duration (never Reset).

**Pass (all):**
- (a) No heartbeat alert while pinging.
- (b) A page arrives after the last ping, and the offset from the last ping to the page is recorded. The offset falls within T plus the measured ingestion latency, and constraint §3.3(c) holds.
- (c) The SMS arrives, and the push arrives with it once OA-H6 pairing is done. Before pairing, the push is recorded N/A and a re-run is owed.
- (d) **The call fires** without acknowledgment. The SMS-to-call lag is recorded and is at most 90 s (§0.5 item 3).
- (e) Resuming pings auto-resolves the alert group [H2], or the actual behaviour is recorded.
- (f) The URL path, the method, the 2xx status, the UI's interval options and the last-heartbeat display (§3.5 (iii)) are recorded (§0.5 item 1 UNVERIFIED items).

**HB-L2 (notifier heartbeat; same authorization, attendance and evidence rules).** Joshua runs two driver processes, `--side runtime` and `--side notifier`, both for at least 2·max(T, T_n), then stops only the notifier side. Pass (all): (a) the page comes from the notifier integration and its title identifies it; (b) the runtime integration raises no alert throughout; (c) the call fires without acknowledgment and the SMS-to-call lag is at most 90 s; (d) resuming the notifier pings auto-resolves, or the behaviour is recorded. Afterwards both integrations go into maintenance with a duration.

**Evidence:** private, under a `local_artifacts/` directory Joshua chooses. Times are labelled operator-reported. No URL, phone number, stack name or region host. **Owners:** HR `:59`; D-MON packet §7 item 1 (`4d64e21:112`); PR #615 RH3 (`06efb2e:156`).

### Return taxonomy (worker build: H1-H12, HQ1-HQ9)

- DONE: every red-first test recorded red at base and green at head; the §7 regression, `test-ops` and `check` are green with records cited; the diff stays inside §5.
- DONE_WITH_CONCERNS: the outcome is established, with a disclosed baseline limitation unrelated to the patch and reproduced on unmodified origin/main.
- NEEDS_CONTEXT: a missing input, a contradicted fact (for example a moved anchor or a public-doc fact that no longer holds) or conflicting owner text. Name it.
- BLOCKED: a needed edit outside §5, or an environment failure the launcher cannot repair.

A failed required criterion is never DONE_WITH_CONCERNS. The worker's DONE is not qualification: HB-L1, HB-L2, the P4 freeze, the P8 hook and the P7/P9 host wiring remain.

## §7 — Acceptance checks (the worker runs them; the coordinator re-runs them at the returned head)

```
python -I scripts/fp.py doctor
python -I scripts/fp.py python -m pytest tests/ops/test_book_heartbeat.py                # red at base, green at head
python -I scripts/fp.py python -m pytest tests/ops/test_book_loop_continuation.py tests/ops/test_book_ingress_validation.py tests/ops/test_c1_signal_daemon_evaluate_loop.py tests/ops/test_book_incident_notifier.py
python -I scripts/fp.py test-ops
python -I scripts/fp.py check
git diff --stat origin/main...HEAD                                                         # §5 allowed files only
```

Report the command, interpreter, head and each printed `record.json` (`status: completed`, exit 0, `source_stable`). Disclose any pre-existing failure with its reproduction on unmodified origin/main (AGENTS.md `:222`).

## §8 — Out of scope

- Host wiring of the wrapper, the step cadence, and the placement of the notifier's process (TB-I3, P7).
- Host wiring of the notifier heartbeat (P9); a heartbeat for the legacy listener or for the daemon Fly apps.
- Monitoring the monitor (D-MON packet OQ-5).
- Building the dot path, options (b) and (c) in §3.6; any change to Joshua's personal notification rules.
- Authenticated attendance and the acknowledgment API (TB-I3, HR `:143`).
- Any provider account, spend, or message to an external party by an agent.

## §9 — Decisions and open questions

**Recorded:** D-MON D-1 is Grafana Cloud IRM (`4d64e21:124`). OQ-2 and OQ-3 operator rulings (§0.5 item 3). The 2026-10-03 dot direction (§0.5 item 6). Independence (§0.5 item 7). HR `:61` ruling condition 4: the notifier's liveness is covered, by a second, separate heartbeat (§0.5 item 8, §3.9); this closes the former OQ-H3.

**OPEN:**
- **OQ-H1** (coordinator (3), qualified under HR `:59`). Freeze T and P (§3.3) and T_n and P_n (§3.9). Owed inputs: the runtime's `max_step_interval` and `max_step_duration` (TB-I3), the notifier's loop interval and round duration (P9). **Lean:** T = T_n = 1 min, the provider floor, with P and P_n set under constraint (b). The alternative is a longer T with fewer false pages, as long as constraint (c) holds.
- **OQ-H2** (Joshua / PR #615 owner). Should the heartbeat ping whenever the loop runs, with a maintenance-mode bracket at planned stops (§3.5), or only while armed? **Lean:** whenever the loop runs.
- **OQ-H3** CLOSED by the HR `:61` ruling, condition 4 (§9 Recorded).
- **OQ-H4** (Joshua). The dot path (§3.6). **Lean:** (a) manual forward for the first session; then (b), adding both heartbeat integrations to OA-D3's integrations filter.
- **OQ-H5** (HB-L1). Unverified provider facts: the Formatted Webhook heartbeat path, the method, the success status, the alert payload, the UI interval options, and whether auto-resolve re-pages.
- **OQ-H6** (HR owner). Does a provider-side heartbeat that alerts only on silence meet HR `:34` "expose failure through independent monitoring" for a storage failure the runtime survives without raising? H2 and HQ3 assume that every storage failure surfaces as an exception from `step` or `status()`; HQ9 assumes the same of `run_once`. An incidents store silently replaced by an empty, readable one (§2) is not detected by either heartbeat.

## §10 — Audit hooks

```bash
python -I scripts/fp.py python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-10-03-dmon-missed-heartbeat-monitor-card-DRAFT.md
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-03-dmon-missed-heartbeat-monitor-card-DRAFT.md
gh pr view 628 --json state,mergeCommit,headRefOid                         # P1
rg -n 'book_incident|sqlite3|dry_run|armed_until' ops/c1_signal_daemon/book_heartbeat.py   # Expected: no match
rg -n -i 'heartbeat/[A-Za-z0-9]{8,}|formatted_webhook/[A-Za-z0-9]{8,}|glsa_[A-Za-z0-9]|grafana\.net/' ops tests docs   # Expected: no match
git diff --stat origin/main...HEAD
```

## §11 — GLM eligibility

**Not GLM-eligible. Opus/CC builds it.** Under `C:\Users\joshu\.claude\CLAUDE.md:15`, work stays with Opus "for security, secrets … or production incidents". This card handles a secret reference and the silent-runtime incident path. Nothing under `local_artifacts/` is passed anywhere.

## §12 — Dispatch record

- **Status:** DRAFT. After P1, P2 and P8, coordinator (3) freezes the card. It records here the frozen revision, the #628 merge commit and liveness-hook anchor (P8), the frozen T, P, T_n and P_n (P4) and any moved anchor.
- **Executor (planned):** one Claude Code (Opus) worker, seat worker, a worktree under `.claude/worktrees/`, a `claude/*` branch, pushed. No PR unless the coordinator records one.
- **Pre-dispatch checks:** the first two §10 hooks, run on the frozen file.

## §13 — Public sources (read 2026-10-03 with WebFetch/WebSearch; no login)

The worker re-reads [H1] and [H2] before building and returns NEEDS_CONTEXT on a contradiction.

| Ref | Page | URL |
|---|---|---|
| H1 | Configure integrations (heartbeat settings, supported types, maintenance mode) | https://grafana.com/docs/grafana-cloud/observe-and-act/respond-to-incidents/irm/integrations/configure-integrations.md |
| H2 | IRM integration best practices (timeout range, auto-resolve, maintenance duration) | https://grafana.com/docs/grafana-cloud/alerting-and-irm/irm/guides/best-practices/integrations.md |
| H3 | OnCall Alertmanager integration reference (heartbeat URL pattern, POST, interval example) | https://grafana.com/docs/oncall/latest/configure/integrations/references/alertmanager/ |
