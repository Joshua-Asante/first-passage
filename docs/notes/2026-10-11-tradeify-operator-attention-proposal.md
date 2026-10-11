# Tradeify: reduce recurring operator attention

**Status: PROPOSED for operator and deployment-coordinator review.** Requested by
Joshua on 2026-10-11: review the recommendations, sharpen them, and post a PR
detailing what must change to save operator attention within risk and safety
guidelines. This is a proposal, not an implementation card or a change to trading
authority. Evidence baseline: `main@b6fff029`. No live host or account was inspected.

**Recommendation:** automate preparation, collection, verification and recording;
retain the current substantive operator decisions. First deliver a guided close
and next-session workflow using the existing account owner. Then automate watch
collection and consolidate incident handling. Treat reduced attendance hours as
a separate, qualified change to the trading window or operating policy.

## 1. What the review changed

The earlier recommendation list understated these constraints:

| Earlier formulation | Sharpened recommendation and evidence |
|---|---|
| Two brief interactions per day | Target two routine **decision points**, not two clicks or a guaranteed two visits. Shutdown/disarm and settlement availability can occur at different times. Settlement needs fresh evidence and a current challenge; never keep trading or leave authority active to combine visits. [Settlement contract](../spec/2026-09-15-tradeify-attended-settlement-contract.md) |
| Automate daily settlement | Reuse the assembler, but distinguish importing available reports from automatically obtaining qualified source evidence. The assembler does not fetch, sign, submit or accept. Historical catch-up requires an equity source its code says is not presently known. [Assembler](../../ops/c1_rail/account_close_assembler.py) |
| Collect evidence once | Reuse a capture only when its identity, scope, causal coverage and freshness meet each consumer's requirements. Initial account evidence, live observations, settlement and watch checks are not interchangeable. |
| Reuse the existing evidence exporter | The [exporter](../../ops/c1_rail/export_session_evidence.py) copies legacy c1 files; it is not a coherent snapshot of the book owner's SQLite state or a qualified broker evidence collector. Build the missing book export through its owners. |
| One acknowledgment action | The [CLI](../../ops/c1_rail/book_incident_operator_cli.py) records operator-reported delivery, not authenticated attendance. Consolidation must implement the missing authentication/binding, not label a provider acknowledgment as attendance. |
| Automate the held-request watch | Automate evidence work only under amended performer/access rules. A completed check cannot prove an absent order never existed or will never execute. The watch may continue indefinitely. [Watch W1–W7](2026-10-02-t13-a12-f3-held-request-watch-draft.md) |
| More monitoring enables less attendance | Monitoring reduces checking effort, not the current obligation to respond. No claim that a page, heartbeat or native stop makes unattended operation acceptable. [Halt/resume contract §3](../spec/2026-09-14-tb-s3-halt-resume-contract.md) |

These are source-based design findings. Benefits below are predictions, not measured
savings. This self-review is not independent implementation acceptance.

## 2. Objective, boundaries and desired operator experience

Measure four separate costs: active operator minutes, interruptions, required
availability hours, and engineering/maintenance burden. Minimize recurring work
without moving it into hidden incident exposure or a bespoke service that needs
more care than it saves. Availability remains the main limit of an attended release.

The desired normal flow is:

1. **Prepare automatically:** gather current facts, validate them and show a concise
   readiness decision with exact blockers. Joshua reviews and supplies the bounded
   session authorization. Existing distinct grants remain distinct even when the
   interface presents them together.
2. **Operate with exception alerts:** no recurring manual health approval. Joshua
   remains available under the attendance contract. Correctly handled refusals go
   into the digest; incidents page immediately under the qualified policy.
3. **Close automatically within existing authority:** execute the scheduled sequence,
   collect causal outcome evidence, confirm disarm and prepare the settlement review.
   Joshua signs only when the complete package is ready. If it is not ready, leave
   disarmed and notify once when actionable; incomplete settlement blocks next risk.
4. **Prepare the next session:** consume the accepted close and reconciliation,
   generate a new authorization subject, and await fresh GO. No automatic rearm.

Preserve these boundaries in every implementation:

- One durable account owner controls sends, halt state, reservations and transitions.
  A presentation layer, collector, notifier or agent cannot create trading authority.
- Per-session GO, M1, release identity, freshness and account binding remain enforced.
  Startup remains halted; day change, recovered feed and acknowledgment do not resume.
- An incident ends automated trading for that session under the first-release rule.
  In INTERVENTION the runtime sends no CLOSE, CANCEL, AMEND or ATTACH. Operator
  platform recovery and its second-close race remain explicit.
- Unknown or possibly transmitted orders retain ownership and reservations. No retry
  based on timeout, elapsed time, empty lists or a reused order tag.
- Settlement attestation/signing stays on the operator device. No hosted signing key,
  pre-signed package, fabricated no-trade close or stale-evidence substitution.
- Retain independently monitored runtime, notifier and watch obligations, with
  qualified delivery/escalation. A successful HTTP call alone is not completion.
- Keep account data and credentials private. Public reports contain redacted evidence
  references; grant collectors the narrowest available access, with a structural
  no-order path where the vendor cannot issue read-only credentials.

## 3. Ranked implementation recommendations

### R1 — One guided settlement workflow; largest routine saving

**Observed cost:** T07 calls for manual exports and a timed daily procedure. The
[assembler](../../ops/c1_rail/account_close_assembler.py),
[signing-envelope helper](../../ops/c1_rail/settlement_signing.py) and
[settlement store](../../ops/c1_rail/book_settlement.py) are reusable components,
not an end-to-end operator workflow.

**Change:** provide one local workflow: import/collect → validate source coverage →
assemble → reconcile → show changes/exceptions → review → obtain fresh challenge →
sign → submit → read durable receipt. Keep evidence under the private primary-checkout
location or an explicitly approved successor. Show fees, unexplained adjustments,
history changes, close-time evidence and predecessor identity; do not ask Joshua to
recompute totals. Collect fresh supporting evidence near actual submission so the
contract's freshness bound is met. If review runs long, refresh/revalidate and
obtain a fresh challenge instead of extending its lifetime.

**Delivery stages:** first automate all deterministic work after manual import. Then
qualify supported report/API collection. If dashboard evidence or source finality
cannot be obtained automatically, retain one precise operator capture/attestation
step. Do not promise a fully automated producer before T07 establishes its semantics.
Keep required fresh full-history queries; incremental-only history is a separate
future amendment requiring proof that corrections, deletions and late fees are found.

**Owner/dependencies:** T07 source and procedure owner; TB-I3/account-close owner for
integration; Joshua for key custody, reads and attestation. Existing T07 acceptance,
report timezone/DST and pre-T16 conditions remain.

**Acceptance:** actual-source ordinary and no-trade closes; missing range/row,
changed historical transaction, unknown fee, stale source, wrong account/calendar,
expired challenge and lost receipt. A lost receipt triggers a status lookup, not
duplicate acceptance. Missing historical equity stays blocked. Time the complete
operator path, including report retrieval and failures.

### R2 — One readiness decision and reusable later-session activation

**Observed cost:** readiness is spread across release, feed, settlement, route,
monitoring and calendar owners. [Phase 5 WP4](../superpowers/plans/2026-09-16-phase5-attended-operations.md)
already specifies later-session activation; its deferral is recorded in the
[deployment checklist](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md).

**Change:** generate one live readiness view and exact authorization subject from
those owners. Separate release-level acceptance (reused while its identity remains
valid) from facts that must be fresh each session. Retain machine checks on every
activation; remove repeated manual proof-gathering of unchanged release facts.
Bind the GO to account, session, release/config/policy/calendar, boot, halt generation,
evidence and expiry. Show what changed and why activation is blocked. Recheck at
commit/dispatch so a green preview cannot survive a concurrent halt or stale fact.

Build the approved later-session path rather than repeating B7/n3 as daily ritual.
Initial activation keeps its full gates; material invalidation follows the governing
stop/adjudicate path. Resolve WP4's un-deferral at the existing post-first-session
decision unless Joshua explicitly elects earlier preparation. Authorizing this
proposal does not itself activate that path.

**Owner/dependencies:** T17 launch/activation owner, TB-I3, T13 and deployment
coordinator. Route code changes through the existing account-owner single-writer queue.
The interface must consume host-side admission checks, not rely on a checklist or
the legacy arm helper as the sole enforcement point.

**Acceptance:** wrong/stale/replayed GO; changed release, boot or settlement; concurrent
halt; missing monitoring acceptance; held request; same-session incident; expired
calendar; interrupted activation/receipt recovery. An eligible later session starts
at the next eligible complete bar, without replaying missed signals.

### R3 — Automatic closing evidence and disarm, separate from settlement timing

**Change:** extend the accepted scheduled-close path with a durable closure record:
capture positions, working orders, fills and outstanding requests; establish causal
coverage of the last possible effect; perform normal disarm through the config owner
and verify read-back. Record close-boundary evidence while available instead of
trying to reconstruct it next morning. Export a consistent book-state snapshot using
the owner's supported database snapshot mechanism, not copies of live SQLite files.

Keep the published entry cutoff, flatten start and own-flat deadline, including early
closes. Explicitly schedule disarm before absolute arming expiry. An incident revokes
scheduled-exit authority; the automation must hand over rather than keep closing.
If evidence is uncertain or disarm fails, alert and preserve the obligation. Never
label a local disarm as broker flatness or automatically end attendance with unknown
exposure. The held-request handoff follows W1, separately from ordinary completion.

**Owner/dependencies:** T09 qualified close/reconciliation, TB-I3 config/account owner,
T13 and T07. Automated disarm needs acceptance of this transition in the owner procedure.

**Acceptance:** partial/unknown close, orphan child, late fill, another leg losing its
stop, own-flat deadline breach, disarm-write failure, crash during capture and source
correction. A normal closure produces an auditable receipt; an incomplete one never
produces an all-clear. Test early-close/DST chronology against the bound calendar.

### R4 — One actionable incident view and authenticated acknowledgment

**Change:** reuse [Phase 5 WP2](../superpowers/plans/2026-09-16-phase5-attended-operations.md)
and the notifier rather than adding a general trading dashboard. Present incident
identity, time, account, exposure/protection, working orders, uncertain requests,
evidence age, fence uncertainty and the next recovery step in one view. Automatically
assemble fresh read evidence under authorized access; link to the relevant platform
and runbook without adding an order terminal.

Replace IRM acknowledgment → local `record-delivery` command → provider resolution
with a reviewed authenticated flow. Keep delivery, attendance acknowledgment, incident
recovery completion and provider resolution as separate durable events. Qualify a
provider callback if used; a callback without verified actor/account/incident binding
cannot assert attendance. Stop reminders only under the accepted provider rules;
an acknowledged incident can still require attention and recovery.

**Owner/dependencies:** T13, TB-I3 attendance boundary, notifier owner and the existing
Grafana/Healthchecks integrations. Reuse the qualifications that actually apply;
the watch records G10 PASS with limitations, not blanket monitoring readiness.
Its 2026-10-07 record also requires confirming SMS/voice availability when the
Grafana trial ends about 2026-10-17. Carry that obligation into the readiness view;
do not assume the free tier supplies the qualified channels indefinitely.

**Acceptance:** duplicate/forged/replayed callback, wrong incident, provider outage,
dead notifier beside live rail, failed local storage, missed acknowledgment and
delivery failure. One incident remains one incident across retry/restart; silence
cannot resolve it or grant permission. No notification code can reach a broker send.

### R5 — Automate held-request observations; do not automate uncertainty away

**Observed cost:** [W7](2026-10-02-t13-a12-f3-held-request-watch-draft.md) names Joshua
as performer; he runs the reads, records the result and pings the scheduled dead-man.
W1 permits attendance to end after its prescribed intervention/disarm/closing check
and watch setup. W2 explicitly leaves between-check late effects undetected.

**Change:** authorize a narrow machine collector for the existing W3 read set and
specified accounts. At each required due time, collect fresh evidence, compare it
with the prior record, retain originals and classifications, then ping only after a
durable completed check. Failure to read or record is a missed check. Distinguish
automated completion from human acknowledgment in the record. Keep the independent
missed-check monitor and its separate alert identities for successive missed days.

Evaluate an additional broker event detector or bounded read polling to reduce
between-check blindness; qualify rate limits, disconnect/gap recovery, history
coverage, session resets and detector heartbeat first. This is a detection upgrade,
not permission to relax the required cadence or end attendance differently. Feed
detector results into the existing incident path; no automatic recovery mutations.

**Owner/dependencies:** T13 watch owner; Joshua must amend performer/access authority
and rule on response obligations outside attended hours. Prefer this after R1–R4
unless an actual held request makes the recurring watch the dominant burden.

**Acceptance:** delayed entry/cancel/close effects, reversal after manual flatten,
missing history at reset, unrelated manual trade, missed/failed reads, crash before
record/ping and two consecutive missed days. Preserve reservations and HALTED until
the existing F2 transfer evidence is satisfied. Do not stop or pause the watch merely
because an order disappears, no activity is seen, or a timer expires.

### R6 — Batch administration and prevent avoidable operator escalations

**Change:** generate the daily digest from accepted receipts/journals and one periodic
decision packet from existing owners. Include fills/costs/slippage, incidents,
evaluation progress, weekly activity, upcoming calendar/contract coverage and
credential/entitlement expiry where the source supports it. Escalate impending
deadlines before they become urgent; uncertainty is visible, not counted as success.
The [weekly activity reporter](../../ops/sentinel/activity_week.py) can inform this
view but remains report-only. A preservation trade needs its own operator direction;
the workflow may prepare its decision, not place it automatically.

Separate required live checks from periodic maintenance: retain automated freshness,
identity and health checks every session; reuse accepted release evidence until an
actual invalidator changes it. Route routine implementation/review decisions to their
existing owners and send Joshua only concrete operator decisions with evidence,
options and a recommendation. No daily agent-generated approval checklist on top of
the runtime's existing one. Calendar edits, entitlement renewals and changed evidence
keep their applicable approvals; batch presentation does not silently approve them.

**Owner/dependencies:** T13/T17 with existing calendar and activity owners. Low effort
relative to new broker integrations. Adopt only reports that replace a named manual
task; delete the replaced duplicate procedure after owner acceptance.

**Acceptance:** no extra health pages; correctly handled refusals stay in the digest;
incidents, channel loss and imminent mandatory deadlines retain immediate routing.
Missing activity data cannot trigger an automatic trade or a false compliance claim.

## 4. Changes that can reduce availability hours

| Option | What must change | Recommendation |
|---|---|---|
| Shorter trading window or operationally simpler portfolio | Pre-register the exact behavioral change and evaluate economics, execution/cutoff effects and risk through the applicable qualification owners. Measure incidents and attendance as operational outcomes; do not infer them from P&L backtests. | Best first investigation if availability, rather than active minutes, dominates. No new screen/replay is authorized by this PR. |
| Delegated human coverage | Establish whether venue/platform permissions permit another operator; amend named performer and attendance contracts, access scope, training, explicit handover and escalation. Never share credentials or presume third-party trading is permitted. | Contingent option. It reallocates human attention rather than reducing total work; assess costs and restrictions before design. |
| Unattended release | Demonstrate protection surviving host/route failure, reliable terminal/cancel evidence, bounded safe handling of unknown sends, an accepted exit path during platform outage, independent monitoring and recovery without stale authority. Amend incident mutation and attendance rules; qualify the exact replacement architecture and residual risks. | Defer build. Current route uncertainty and the Tradovate-unavailable fallback gap prevent claiming an equivalent safety envelope. A watchdog or broker stop alone is insufficient. |

Do not start by widening response times, suppressing real incidents, retrying uncertain
orders, auto-resuming after a restart, reducing settlement frequency, caching source
history indefinitely or moving the operator signing key onto the host. These remove
checks or transfer risk before replacing the facts/controls they provide. The
[previous simplification review](2026-09-30-tradeify-simplification-decision-packet.md)
also does not establish TradingView as a cheaper equivalent replacement host.

## 5. Sequence, benefit test and rollback

| Stage | Concrete result | Start condition / stop condition |
|---|---|---|
| A — Baseline and minimal workflow | Observe one normal rehearsal and one incident rehearsal; inventory actual clicks, commands, report delays and handoffs. Prototype R1 after manual import and R2's read-only view. | Coordinator approves bounded cards. Stop adding interface scope once each replaces a named manual task. No production reads without their authority. |
| B — Routine operation | R1/R3 accepted through actual source and owner consumers; R2 activation accepted under the existing timing decision. | T07 source facts and T09 transitions qualified. Missing source semantics block dependent automation, not local import/validation work. |
| C — Exceptions | R4 acknowledgment/evidence flow; R5 automated watch after performer/access ruling. | Existing notifier/watch qualifications plus changed-path tests. Failed collection returns to the accepted manual procedure with an explicit operator handoff. |
| D — Availability | Decision on the §4 options using measured availability burden and operational evidence. | No numerical savings or unattended claim without applicable measured/qualified evidence. |

The deployment coordinator reconciles these stages with T07/T09/T13/T17 and the
account-owner writer queue; this proposal creates no competing dispatch or extra
release gate. Development estimates belong in bounded cards after interface/source
discovery. Expected benefit ranking: R1–R3 high recurring saving; R4 high incident
saving; R5 conditional high recurring saving; R6 moderate administrative saving.

**Measurement:** log active minutes by task, number of manual commands/captures and
context switches, unnecessary versus actionable interruptions, scheduled availability
hours, after-hours recovery/watch work, settlement readiness latency and maintenance
time. Compare the same normal-day and failure scenarios before/after, including a
no-trade day, early close, lost receipt, missing report and held request. Include
time spent troubleshooting the new automation. Keep private traces private.

**Adopt only if:** all existing safety/authority outcomes remain correct, failed
automation cannot create an all-clear or permit risk, measured operator work is
lower for the target scenario, and new maintenance has an identified owner. A slower
but safer refusal is acceptable and must be disclosed rather than excluded from
timings. Report both ordinary and incident costs; do not extrapolate an incident
frequency from a rehearsal. Two routine decision points remains a target.

**Rollback:** disable the new workflow/collector and return to the accepted manual
path while retaining all journals, receipts, held requests and settlement continuity.
Removing a watch worker requires restoring its named performer and due checks first.
UI/collector failure never bypasses readiness, retries a broker send or resets state.

## 6. Decisions for Joshua

These are proposed decisions, not recorded approvals. Merge of this proposal alone
does not amend the cited contracts; each accepted policy change must land with its
owner and be qualified before use.

| Decision | Options and consequence | Recommendation / without decision |
|---|---|---|
| O1 — Scope of the next improvement milestone | R1–R4 preparation through existing owners; or defer attention work until after the first session. Preparation exposes producer/interface gaps sooner; deferral avoids near-term engineering diversion. | Prepare R1's local import workflow and R2's read-only readiness view first, with baseline measurement. No implementation dispatch without the corresponding approved scope/card. |
| O2 — Later-session machinery | Keep the existing post-first-session timing decision; or explicitly un-defer WP4 preparation earlier. | Keep its existing checkpoint and make the recurring operating cost an explicit input. No automatic activation either way. |
| O3 — Automated private reads and watch performer | Retain manual collection; or authorize a reviewed, least-privilege collector for named accounts, operations, storage and schedules, with human escalation. | Authorize only against the concrete collector/access proposal after source qualification. Until then Joshua remains the watch performer and manual import is the fallback. |
| O4 — Primary optimization goal | Reduce active work under current attendance; or also commission a qualified shorter-window investigation. | Start with active work; investigate a shorter window if measured availability remains unacceptable. No portfolio/window change without its own approval. |

**Unresolved:** supported automatic report access and close finality; timing of report
availability; historical-equity/catch-up evidence; authenticated acknowledgment
integration; collector privileges/rate limits; outside-session response obligations;
and the technical recovery path when Tradovate cannot be used. Owners and evidence
are linked above. No numerical saving is asserted and no independent reviewer has
accepted this proposal yet. No runtime, broker action, account read, provider setup,
policy amendment or qualification execution was performed for this document.
