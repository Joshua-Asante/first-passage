# D-MON options packet: alert channels against the halt/resume contract (2026-10-02)

**Status: PROPOSED. Options for the operator; nothing is selected.** The channel choice is Joshua's ([deployment checklist, six cuts item 5, D-MON bullet](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-10-01--first-session-simplification-rulings-six-cuts), :598). This note creates no account, contacts no provider, stores no credential, spends nothing, changes no code and edits no owner. Every option below uses a $0 tier. Opening any provider account is still the operator's act.

**Ticket.** Coordinator ticket M, item 1 (T13 preparation). Line numbers are on origin/main `bd30646` unless a PR head is named. The ticket's "about :596" for the D-MON ruling is :599 (on main 10b3929) (:596 is the T13 bullet).

**Ruling being applied** (checklist :599): check the existing channels against the halt/resume contract; fill any gap with a no-cost external provider, not an in-house build; the alternate-channel escalation stays.

## 1. What the contract requires

Halt/resume contract ([HR](../spec/2026-09-14-tb-s3-halt-resume-contract.md)), §3 *Attendance and notification*, :55–61, with its two restatements.

| # | Requirement | Source |
|---|---|---|
| N1 | Before arming, Joshua verifies access to the platform and the alert channels | HR :57; [ARMING_PROCEDURE](rail_build/ARMING_PROCEDURE.md) :13 |
| N2 | Phone and desktop alarms identify the same incident | ARMING_PROCEDURE :8; [attended-release plan](../superpowers/plans/2026-09-14-tradeify-attended-release.md) :95 |
| N3 | Acknowledgment target: under 60 s after notification | HR :59 |
| N4 | Detection, notification attempts and provider acceptance, delivery evidence, and authenticated attendance are each persisted separately | HR :59 |
| N5 | With no acknowledgment, escalate through an alternate configured channel 60 s after the first attempt | HR :59 |
| N6 | Delivery failures route to the remaining channels immediately | HR :59 |
| N7 | No acknowledgment never restores send authority. Acknowledgment only appends attendance identity and time; an identical repeat is idempotent and conflicting reuse is rejected | HR :59, :61 |
| N8 | Notification retries carry the same incident identity and cannot dispatch broker commands | HR :61 |
| N9 | Independent missed-heartbeat monitoring covers a silent runtime. A local outbox is not assumed durable when storage fails; storage failure is exposed through independent monitoring | HR :61, :34 |
| N10 | Provider channels and heartbeat thresholds are qualified before live use. Better Stack remains unselected | HR :59 |

Incident ADR §A12 ([PR #584](https://github.com/Joshua-Asante/first-passage/pull/584), head `e57bd98`, PROPOSED) also sends two items to D-MON: the channels for the held-request watch (F3) and alert-channel loss with no incident (D5). The companion [F3 watch draft](2026-10-02-t13-a12-f3-held-request-watch-draft.md) covers both.

## 2. Existing channels (read on `bd30646`)

| Channel | What it does | Source |
|---|---|---|
| `LoggingNotifier` | Writes to the process log. It is the default when no alert path is configured | [`c1_rail_telemetry.py`](../../ops/c1_rail/c1_rail_telemetry.py) :164–175; [`c1_rail_http_server.py`](../../ops/c1_rail/c1_rail_http_server.py) :612 |
| `FileAckNotifier` | Appends alert JSONL on the host volume; the operator writes an ack file. It discharged M1 item 10 on 2026-07-28 (one WARNING alert, acknowledged) | `c1_rail_telemetry.py` :222–255; `c1_rail_http_server.py` :624–627; [M1 acceptance](rail_build/M1_MONITORING_ACCEPTANCE.json) :43–44, :57 |
| Book-route incident record | A halt writes a durable `incidents` row. No notifier is attached: `ops/c1_rail/book_*.py` contains no notify or alert call, and the one halt callback found (`on_halt`, settlement) defaults to `None` with no caller wiring it | [`book_account_owner.py`](../../ops/c1_rail/book_account_owner.py) :296, :650–686, :1294–1306 |
| Daemon status | `GET /` liveness snapshot. Pull only | [`heartbeat.py`](../../ops/c1_signal_daemon/heartbeat.py) |
| Fly health checks | HTTP `GET /` every 30 s on both apps. Nothing in the repo routes a failure to a person. Both apps run in Fly region `iad` | [`deploy/c1_rail/fly.toml`](../../deploy/c1_rail/fly.toml) :24–30; [`deploy/c1_signal_daemon/fly.toml`](../../deploy/c1_signal_daemon/fly.toml) :15–20 |
| Authenticated attendance | None found (`git grep -i attendance -- ops` is empty) | — |

The two notifier classes serve the legacy c1 listener ([`c1_rail_listener.py`](../../ops/c1_rail/c1_rail_listener.py) :214–227). The book route uses CC-3's durable halt instead (checklist item 4, :587).

## 3. Gap check

| Req | Status | Why |
|---|---|---|
| N1 | **GAP** | There is no push channel to verify |
| N2 | **GAP** | Alerts reach a file and a log, not a phone or a desktop alarm |
| N3, N5, N6 | **GAP** | No acknowledgment timer, no second channel, no delivery report |
| N4 | **PARTLY** | Detection is durable on the book route (incidents table). Attempts, provider acceptance, delivery and attendance are recorded nowhere |
| N7, N8 | Not a channel gap | Met by construction if the alert path holds no broker credential. The attendance record is TB-I3 work (HR :143) |
| N9 | **GAP** | Fly's checks run with the host's provider and region, and notify no one |
| N10 | Open by definition | Every choice needs qualification |

**Result: the existing channels do not meet the contract.** Push (N2), timed alternate escalation (N3, N5, N6), delivery evidence (N4) and an external heartbeat (N9) are missing. Under the ruling, a no-cost external provider fills them.

**What a provider cannot fill.** Detection, the incident identity, the authenticated attendance record (N4, N7) and the bounded call that hands an incident to the provider stay in the rail (TB-I3; [Phase 5 plan](../superpowers/plans/2026-09-16-phase5-attended-operations.md) work package 2, :62–76). With no outbox, that call is a bounded publish that carries the incident id as the provider's deduplication key, and a retry repeats the same key. Whether that meets HR :61's "notification outbox" sentence is the halt/resume owner's reading (OQ-1).

## 4. Options (all $0 tiers)

**[page]** means the fact was read on the cited public page on 2026-10-02 (§8). **[UNVERIFIED]** means it was not found on a captured page and must be checked during qualification.

### Option A — Grafana Cloud IRM free tier (one provider)

- **Cost.** Free tier, limited to 3 active IRM users a month **[page: Grafana pricing]**.
- **Push and escalation.** Personal "important" notification rules. The documented example is mobile push at once, SMS after 1 minute, then a phone call **[page: personal notification rules]**. That maps directly to N5.
- **Heartbeat.** An incoming Webhook integration can act as a heartbeat receiver: IRM opens an alert group when pings stop within the configured interval **[page: configure integrations]**. The minimum interval is **[UNVERIFIED]**.
- **SMS and phone.** There is no fixed rate limit, but delivery may be throttled at abnormal volume; free orgs have extra limits on phone-number verification **[page: IRM rate limits]**. Whether the free tier delivers SMS and phone calls at all is **[UNVERIFIED]**.
- **Acknowledgment stops the sequence:** **[UNVERIFIED]**. Expected, but it must be shown in qualification.
- **Fit.** N2, N3, N5, N6 (as far as free-tier SMS and phone exist) and N9, in one account outside Fly.

### Option B — Healthchecks.io Hobbyist (heartbeat) with PagerDuty Free (paging)

- **Healthchecks.io Hobbyist.** $0 a month, 20 checks, no SMS, WhatsApp or phone credits **[page: Healthchecks pricing]**. Period and grace are each at least 60 s **[page: management API]**. A `/fail` signal marks a check down at once **[page: pinging API]**. More than 5 pings a minute on one check may be ignored. Some failures still return HTTP 200 (`OK (not found)`, `OK (rate limited)`), so the publisher must read the response body **[page: pinging API]**.
- **PagerDuty Free.** $0, 5 users, 1 escalation policy, limited email, push, SMS and phone notifications, and 100 SMS or phone notifications a month **[page: PagerDuty pricing]**. Each personal notification rule takes a delay in minutes per contact method; 0 sends at once **[page: notification rules]**. Push at 0 and SMS or a phone call at 1 gives N5. Unacknowledging an incident resumes escalation and sends notifications again **[page: incidents]**; that acknowledgment stops them is an inference from this. Whether the Free plan accepts Events API incidents is **[UNVERIFIED]**: the pricing page's Events row belongs to another plan family.
- **Joining them.** Healthchecks' own PagerDuty integration (**[UNVERIFIED]**: its integrations page returned 404), or the rail sends incidents to PagerDuty directly (needs the Events API on Free).
- **Fit.** As A, but with two providers. The heartbeat and the pager fail independently. That is a gain (one can report the other's silence) and a cost (two accounts, two credentials, two dependency reviews).

### Option C — Healthchecks.io Hobbyist with two free push apps, no paging product

- **Media.** The ntfy app: the hosted service can be used without an account, subject to rate limits **[page: ntfy terms]**; priority 5 gives long vibration bursts and a pop-over **[page: ntfy publish]**. A Telegram bot: bots are free within per-chat rate limits **[page: Telegram bot FAQ]**. That Healthchecks alerts both at once is **[UNVERIFIED]**.
- **Contract gap.** Nothing is acknowledged, so nothing escalates "without acknowledgment". Both channels fire at t = 0, and there is no SMS or phone. Whether simultaneous fan-out meets N5 is the halt/resume owner's reading, and it probably needs an owner amendment (OQ-3).
- **Use** only if neither A nor B qualifies.

### Not proposed

| Candidate | Reason |
|---|---|
| Pushover | $4.99 one-time purchase per platform after a 30-day trial **[page]**. Not no-cost |
| Healthchecks SMS or phone credits | Business plan, $20 a month **[page]** |
| ntfy paid tiers (phone calls) | From $6 a month **[page]** |
| Better Stack | "Better Stack remains unselected" (HR :59). Not evaluated here |
| Any monitor hosted on Fly | Same failure domain as the host (N9) |

## 5. Author's lean (not a selection)

**A, then B, then C.** A covers push, 1-minute alternate escalation, acknowledgment and the heartbeat in one free account outside Fly. Its free-tier SMS and phone delivery is the first thing to verify. B is the fallback if A's free tier lacks SMS or phone, or the 1-minute wait. C does not meet N5 as written.

## 6. Constraints on whichever is chosen

Carried from #570's pre-ruling D-MON analysis (retrievable at `564b239`, §2), which the ruling did not withdraw.

- The publish call is bounded and stays off the order and protection path. A provider timeout cannot delay a protective action.
- The payload carries the incident id and minimal status only, with no account, order or strategy detail. This is also the public-repo posture.
- Credentials stay outside version control. Provider settings are configuration as code with secret references (AGENTS.md, *Configuration as code*).
- The heartbeat is tied to observed rail and daemon progress, not a free-running timer, so a live timer cannot mask a dead component. A failed durable incident write stops the heartbeat or sends a failure signal (HR :34, :61).
- Heartbeat recovery never clears a latched incident. Provider acknowledgment never clears an incident or restores authority (N7).
- A silent host is detected only after the heartbeat threshold: period plus grace, at least 2 minutes on Healthchecks. That threshold is separate from the 60 s escalation, which runs from the first notification attempt. Both are qualified (N10).

## 7. Qualification evidence owed (T13)

Checklist T13 (:270) owes real delivery, failure and escalation, an external heartbeat and durable acknowledgment. With synthetic incident data only, before any armed session:

1. A killed publisher alerts the primary channel within the qualified heartbeat threshold.
2. A synthetic rail incident reaches the primary channel, and the time to acknowledgment is measured.
3. With no acknowledgment, the alternate channel fires 60 s after the first attempt (the measured offset is recorded).
4. A primary delivery failure routes to the remaining channel at once.
5. Detection, attempt, provider acceptance, delivery and attendance are recorded separately, with times.
6. After a restart, the acknowledgment stays attached to its incident, and nothing re-arms.
7. A test alert is acknowledged before each arming (N1).

## 8. Decisions and open questions

**For Joshua:**
- **D-1.** Choose A, B or C (or another no-cost provider), and the primary and alternate media.
- **D-2.** If he chooses, open the provider account or accounts himself. Account creation is his act.

**Open:**
- **OQ-1** (halt/resume owner). Does a bounded publish with provider-side deduplication meet HR :61's "notification outbox"?
- **OQ-2** (T13). There are two acknowledgments: the provider's, which stops paging, and the rail's authenticated attendance (HR :61). Proposal: keep both, with the provider's only silencing pages. Feeding one into the other needs an inbound webhook, which is an in-house build.
- **OQ-3** (halt/resume owner; option C only). Does simultaneous fan-out meet N5?
- **OQ-4** (qualification). Grafana free-tier SMS and phone delivery; Grafana's minimum heartbeat interval; PagerDuty Free's Events API; Healthchecks' PagerDuty integration; acknowledgment stopping notifications on A and B.
- **OQ-5** (T13). The monitoring provider itself fails with no incident (§A12 D5). See the [F3 watch draft](2026-10-02-t13-a12-f3-held-request-watch-draft.md), W6.

## 9. Sources

Public pages, each HTTP 200, captured 2026-10-02 between 19:45 and 19:54 UTC. The bytes went to the session scratchpad and are not retained; the SHA-256 prefixes identify what was read. Dynamic pages hash differently on re-capture.

| Page | URL | SHA-256 prefix |
|---|---|---|
| Healthchecks pricing | https://healthchecks.io/pricing/ | `9f1780f8d48fa062` |
| Healthchecks management API | https://healthchecks.io/docs/api/ | `ccacc3806c4a8142` |
| Healthchecks pinging API | https://healthchecks.io/docs/http_api/ | `6720b422ff144396` |
| PagerDuty pricing | https://www.pagerduty.com/pricing/incident-management/ | `8483c23d8f5316ce` |
| PagerDuty notification rules | https://support.pagerduty.com/main/docs/notification-rules | `44d02ac15ffe96db` |
| PagerDuty incidents | https://support.pagerduty.com/main/docs/incidents | `950caea418dac399` |
| PagerDuty escalation policies | https://support.pagerduty.com/main/docs/escalation-policies | `f221ad4f3314a495` |
| Grafana pricing | https://grafana.com/pricing/ | `09618e927c6f77de` |
| Grafana IRM personal notification rules | https://grafana.com/docs/grafana-cloud/alerting-and-irm/irm/notify-responders/personal-notification-rules.md | `0ad703e9bc49a812` |
| Grafana IRM configure integrations | https://grafana.com/docs/grafana-cloud/alerting-and-irm/irm/integrations/configure-integrations.md | `ab2774856d8a523d` |
| Grafana IRM rate limits | https://grafana.com/docs/grafana-cloud/alerting-and-irm/irm/reference/rate-limits.md | `444fc8bacd87b5fd` |
| ntfy terms | https://docs.ntfy.sh/terms/ | `119132ad1a60d640` |
| ntfy publish | https://docs.ntfy.sh/publish/ | `140c05a63f7e06dd` |
| ntfy home (paid tiers) | https://ntfy.sh/ | `dd78bbaaa047fc9b` |
| Pushover pricing | https://pushover.net/pricing | `e1e2575b202a9153` |
| Telegram bot FAQ | https://core.telegram.org/bots/faq | `935cc8bad3ba1e61` |

Not reachable: `https://healthchecks.io/integrations/` (404). Not searched: Better Stack, by HR :59.
