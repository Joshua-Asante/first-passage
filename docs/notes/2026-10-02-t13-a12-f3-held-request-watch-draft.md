# Held-request watch for incident ADR §A12 F3 (T13 owner text) — 2026-10-02, adoption text 2026-10-05

**Status: ADOPTION TEXT (2026-10-05).** Coordinator (4), as the attended-operations (T13) owner, adopts this text when the PR that carries it merges after the scoped refute-first review and the Codex review (Joshua's Q2 ruling, [D1/T13 packet](2026-10-04-d1-t13-evidence-packet.md) addendum). Adoption is not Joshua's §A12 D1 acceptance, which stays his separate act. *Before 2026-10-05:* DRAFT, PROPOSED as T13 owner text. §A12 is itself PROPOSED ([`docs/adr/2026-09-17-bounded-platform-protection-incident-contract.md`](../adr/2026-09-17-bounded-platform-protection-incident-contract.md) on main, as merged from PR #584 at `368f366`). *Citations refreshed 2026-10-02 from PR #584 `e57bd98` and PR #593 `8d253c9` to main (operator ruling 2026-10-02 (sitting 2), A12-D1).* Nothing here takes effect until §A12 and this text are both accepted. This note does not edit the incident ADR or the halt/resume contract. Its cadence and policy rows are proposals for the operator.

**Traces to** (incident ADR and acceptance-packet line numbers on main `1a350ec`; the ADR changed later on main, so cite by text):

| §A12 text | What it asks | Here |
|---|---|---|
| F3, *Watching a held request* (:460) | While any request is held, a check for unexplained effects at each session open or at another cadence the owner names. Disarm does not satisfy it. Owner: attended operations (checklist T13), with the D-MON channels | W1–W5 |
| §A12.4 (now in the [A12 acceptance packet](2026-10-02-a12-acceptance-packet.md); removed from the ADR by the 2026-10-02 narrowing), row *Attended-operations contract (checklist T13) and D-MON* (packet :30) | Cadence, channels and binding owner, plus alert-channel loss with no incident (D5). Required before §A12's acceptance or in the same act | W2, W5–W7 |
| §A12.5, row *Held-request watch and monitoring loss* (:534) | HR :61's attendance sentence is ambiguous for a disarmed account with a live unknown | W1 |
| §A12.6 D1, third bullet (now in the [A12 acceptance packet](2026-10-02-a12-acceptance-packet.md); D1's prerequisite list is in ADR §A12.5, :540–549) | The attended-operations owner adopts the watch before or with acceptance | *Adoption* |
| §A12.6 D5 (now in the [A12 acceptance packet](2026-10-02-a12-acceptance-packet.md)) | Alert-channel loss with no incident and the late-effect watch go to D-MON and T13 | W5, W6 |

It also takes the hand-off from the C-a selection register ([`docs/notes/2026-09-26-close-semantics-c-a.md`](2026-09-26-close-semantics-c-a.md#addendum-2026-10-02--c-a-selection-register-proposed-for-operator-acceptance) on main, as merged from PR #593 at `550bc74`; accepted as written by operator ruling 2026-10-02 (sitting 2)): outcomes O0 and O5–O8 hold the reservation (REG §R.3), and row S-X3's recovery hands any request still retained to this watch ([S-X3 draft](2026-10-02-t13-c-a-attended-recovery-draft.md) §8).

**Abbreviations.** HR: the [halt/resume contract](../spec/2026-09-14-tb-s3-halt-resume-contract.md). DP: the [drill plan](2026-09-26-tradeify-route-drill-plan-draft.md). REST: the [REST route assessment](../briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md). REG: the C-a selection register addendum in the close-semantics note (on main). Main-branch line numbers are on origin/main `bd30646`, except HR line numbers, which were refreshed to `9c2a153` at adoption (the HR owner readings at :67–75 shifted them).

## Definitions

- **Held request.** A request whose outcome has become unknown (§A12 F1) and that no accepted F2 class has released. It keeps its worst-case reservation (F1(b)).
- **Late effect.** Any position, working order, fill, child, sibling or coverage-repair effect on any symbol of the account that neither an owned operation nor a recorded operator action explains (F2, last bullet; F5).

## W1 — Start, and the attendance reading

- The watch starts when the incident session's recovery ends with at least one held request ([S-X3 draft](2026-10-02-t13-c-a-attended-recovery-draft.md) §8).
- **Attendance reading of HR :61 for this case** (*ruled:* Joshua, 2026-10-04T20:30:58Z, "approve the recommendations", Q1 as revised; OQ-1). With a request held, attendance for the session ends once all of these are done and read back: (1) the operator stop (HR :98, O-6); (2) intervention: every position and working order the reads show is managed by Joshua on the platform (HR :53); (3) the disarm, persisted and read back (`dry_run=true`, `armed_until=null`), with HALTED kept (HR :61); (4) the closing check (W2 item 1) recorded (W7), with the first G1 due time scheduled (W5 item 1). Any flatten made against a held close or flatten request falls under Joshua's C-a residual-risk decision (ADR `:532`), because a manual flatten followed by a late close can leave an opposite position (ADR `:474-479`). *Earlier proposed wording, kept for the record:* Attendance for the session ends once stop, intervention and disarm are done and read back, and the watch is scheduled. The held request does not keep the session attended indefinitely: the watch carries it. HR :61 requires stop, intervention and disarm before leaving. F3 says disarm does not end the watch; it does not say disarm cannot end attendance.
- The account stays HALTED. No later session may activate while any request is held (F3; HR :79, "unresolved owner cannot be overridden").

## W2 — Cadence (proposal; the operator decides)

*Ruled, operator ruling 2026-10-02 (sitting 2), D-MON-5:* the W2 cadence as drafted. Broker-platform fill notifications are added only if free and they pass qualification (UNVERIFIED). A missed check pings the D-MON dead-man check (W5 item 1).

1. **Closing check** in the incident's own session, before the ~17:00 ET list reset. It is the last chance for same-session correlation (REST §6.4; §A12 :462).
2. **A check at each session open** while any request is held, before any other activity on the account, including the weekly preservation trade (W5, item 3).
3. **A check just before any later-session activation.** Activation is blocked anyway while a request is held (F3).

Stated, not hidden:
- **Between checks, nothing watches the account.** A late fill is found only at the next check. Its exposure is bounded only by the held request's quantity and whatever protection it carries. *Optional no-cost detector:* broker-platform fill notifications on the operator's phone, if the platform offers them. **[UNVERIFIED]**; it would need qualification (OQ-5).
- **The watch has no time-based end.** It ends only by F2 transfer (W4). Cross-session recovery is UNESTABLISHED (R-2 closure, DP :224–236), so a request not correlated within its own session is likely to stay held (§A12 :462), and the watch may run indefinitely. The operator accepted indefinite suspension on 2026-09-26 (ADR §A11 item 2).

## W3 — What each check reads

Fresh reads, each with its local time, on the same read set as the [S-X3 draft](2026-10-02-t13-c-a-attended-recovery-draft.md) §4:
- fill-reconciled positions on all symbols;
- working orders on all symbols;
- fills since the previous check. In the same session, the session fills list. In a later session, CrossTrade's durable fills history (`GET /v1/api/tv/fills/history`), a periodic capture whose completeness is unverified; a miss there is not evidence of no fill (DP :200, R-2 step 3);
- for each held request whose order id was learned, its lifecycle and status by id. Cross-session reads have returned HTTP 400 (R-2 closure, DP :226–236), and a failed read is recorded as failed, never as absence.

Read authority is the same open question as S-X3's P3 (OQ-2).
*Ruled, operator ruling 2026-10-02 (sitting 2), D-MON-2:* the watch reads use the same read-only, operator-performed scope as the S-X3 recovery read set.

## W4 — Classifying a check

| Finding | Class | Action |
|---|---|---|
| Nothing new | "No unexplained effect observed at time T with reads R." **Not a release:** absence never releases (F2; closure plan row 3) | Record; schedule the next check |
| An effect that an accepted F2 class uniquely correlates to a held request | Transfer under F2. This needs the operator's D2 and D3 dispositions (§A12.6, now in the [A12 acceptance packet](2026-10-02-a12-acceptance-packet.md)) | Hand to attended recovery (S-X3 draft §4–§8). The halt stays (F3) |
| An effect not uniquely correlated | Incident (F5). It is an additional identified exposure, and the held request stays held; the double count is deliberate | Alert on the D-MON channels (W5). The operator manages exposure on the platform (HR :53; S-X3 draft §5) |
| Reads fail, or the platform is unavailable | Check **missed**, not passed | Retry. If exposure is suspected, Joshua flattens directly on Tradovate (D-MON-3); if Tradovate itself is unavailable, see the S-X3 draft §7 step-3 GAP |

## W5 — Channels (D-MON)

1. **A missed check alerts (G1; specified 2026-10-05, not built).**
   - **Due times.** While any request is held, a check is due at each account-session open: 18:00 America/New_York, Sunday to Thursday (the Tradeify 6 PM–5 PM ET account day; [ops/calendars](../../ops/calendars/README.md)), whatever the session's permission. This is W2 item 2 as a fixed schedule. Item 1 (closing check) and item 3 (pre-activation) happen inside attended sessions and need no dead-man. A due time on a day with no account session is still due: the schedule may over-cover, never under-cover.
   - **Grace.** 60 minutes after each due time (*ruled:* Joshua, 2026-10-04T20:30:58Z, Q3, confirmed here now that the due time is defined). A check not recorded complete by due + 60 min pages.
   - **Mechanism.** A schedule-based dead-man at a no-cost external provider (deployment checklist `:601`: no in-house build). Its schedule is the due times above, in America/New_York, with the 60-minute grace. On a missed ping it notifies the existing Grafana IRM integration, so the page runs the configured Important chain (SMS and push, then a call at +1 min; [Grafana IRM binding card](../briefs/handoffs/2026-10-03-dmon-grafana-irm-binding-card-DRAFT.md) §0.5; Q7 PASS, §6.3). Grafana IRM's own heartbeat takes one fixed interval ([IRM integrations, heartbeat monitoring](https://grafana.com/docs/grafana-cloud/alerting-and-irm/irm/integrations/configure-integrations/)), so on its own it cannot express this schedule: a 25 h interval pages every Friday evening, and a 73 h interval detects a weekday miss up to three days late. **Provider binding: OPEN, Joshua's channel choice** (checklist `:601`). Recommended: Healthchecks.io Hobbyist, already named in the ruled D-MON-1 fallback B (checklist `:601`), used only as this cron-schedule dead-man (America/New_York; 60-minute grace), with its failure notification posting to the IRM integration. Fallback B's trigger (A lacking SMS, phone or the 1-minute step) does not apply here, so this use is a new, narrow channel choice. Joshua configures both ends; no agent sees either URL.
   - **Pinger.** Joshua pings the provider when a check is recorded complete (W7), never before. A check classed missed (W4, last row) does not ping.
   - **Missed check.** The page is the signal. Joshua runs the check as soon as he can. The check stays owed until recorded complete, and its record names the due time it answers and marks it late. Each further missed due time pages again. A missed check is not a pass and releases nothing (W4). If exposure is suspected, D-MON-3 applies (W4, last row).
   - **Start and end.** The schedule is enabled when the watch starts (W1) and paused only when the watch ends by F2 transfer of the last held request (W4). Pausing it while any request is held is forbidden.
   - **Arming preconditions:** see *Arming preconditions* under Adoption.
2. **An F5 finding** goes out on the primary channel, with the 60 s alternate escalation (HR :63).
3. **Operator trades on book symbols confound W4.** F5 does not classify operator platform actions; HR §4.1 O-5 leaves them OPEN (HR :124). Proposal: while any request is held, the weekly preservation trade uses a symbol outside the four. DP :137 already offers that treatment. Operator decision (OQ-4).
   *Ruled, operator ruling 2026-10-02 (sitting 2), D-MON-7:* W5 item 3 is adopted as a narrow exception: outside the four while any request is held. F-5 stays the general rule (B–D packet GC-7 addendum).

## W6 — Alert-channel loss with no incident (§A12 D5)

This is not a halt/resume §2 trigger (acceptance packet §A12.6 D5, :48). Proposal, by state:

| State | Loss | Proposed response |
|---|---|---|
| Before arming | Any channel fails its test | Do not arm (HR :61) |
| Armed | Primary lost, alternate working | Continue. Delivery failures already route to the remaining channel (HR :63). Record it |
| Armed | All channels lost, or the monitoring provider lost | Operator stop. It is an incident and ends automation for the session (HR :98, O-6), because the 60 s acknowledgment target can no longer be met |
| Disarmed, request held | Any | No session effect. The watch continues on its calendar, and a missed W5 ping is itself the signal. Record it |

These rows are policy, so the operator rules on them (OQ-3).

*Ruled, operator ruling 2026-10-02 (sitting 2), D-MON-6:* the W6 table as drafted. The cell 'Armed / all channels lost, or the monitoring provider lost → operator stop' was ruled earlier on 2026-10-02 (coordinator (3) sheet, item E). Neither ruling reclassifies refusals: HR-ADOPT decides which refusals are incidents, and every incident notifies.

## W7 — Binding owner and records

- **Obligation:** the attended-operations contract (checklist T13). **Performer:** Joshua, who holds platform and credential access. **Recorder:** the coordinator.
- **On adoption,** STATE.md gains a scheduled-forward-trigger row: "held-request watch due at each session open while any request is held". STATE owns durable obligations (AGENTS.md); this note does not edit it.
- **Each check's record (G3; specified 2026-10-05).** One JSON line per check in `local_artifacts/t13-watch/<watch start UTC>/checks.jsonl` in the operator's primary checkout (gitignored; never a worktree, whose files are deleted with it). Fields: `due_utc` (the G1 due time it answers, or `closing` / `pre_activation`), `started_utc`, `completed_utc`, each read's kind, local time and `ok` or `failed` with the SHA-256 of its private bytes, the W4 class, `complete` or `missed`, `late` (completed after due + 60 min) and `ping_utc`. The original read bytes are kept beside it, private, never committed (public repository). The recorder (coordinator) writes the line from Joshua's report, or Joshua writes it. The provider's ping log is the external corroboration.

## Adoption

§A12 D1 makes adoption by the attended-operations owner a precondition of §A12's acceptance, or part of the same act. The inputs are in hand: OQ-1 to OQ-5 ruled (below), the D-MON channel choice (provider A, Grafana IRM; options packet `:124`), and Joshua's 2026-10-04T20:30:58Z rulings on the packet's Q1–Q4. Coordinator (4) adopts this text as T13 owner on the merge named in the status line. STATE gains the W7 trigger row and the deployment checklist gains the arming preconditions in the same PR. The open G1 provider binding does not block adoption or D1: under Q4 as narrowed, G1 needs only to be specified before adoption; its provider binding and build are arming preconditions.

### Arming preconditions (Q4 as narrowed)

Before the first armed session, all of these hold. They are not D1 gates: no request can be held before the first armed session, and D1 grants no arm (ADR `:567`). The arm helper does not check them, so they are carried in the deployment checklist (`:601`) and STATE.
1. The G1 provider binding (Joshua's channel choice) and the G1 build (configuration only: schedule, grace and the IRM notification).
2. **G10**, the end-to-end qualification of the watch dead-man: in an attended run under Joshua's explicit go, a scheduled ping is deliberately omitted and the page is recorded arriving through the IRM chain, with the due time, the page time and the SMS-to-call offset.
3. The channel qualifications: Q7 (PASS 2026-10-05, binding card §6.3) and HB-L1/L2 ([missed-heartbeat card](../briefs/handoffs/2026-10-03-dmon-missed-heartbeat-monitor-card-DRAFT.md)).

## Open questions

- **OQ-1** (halt/resume owner). W1's reading of HR :61.
  *Ruled, Joshua 2026-10-04T20:30:58Z (packet Q1 as revised):* the W1 attendance reading above.
- **OQ-2** (operator). Read authority for watch reads (DP :174).
  *Ruled, operator ruling 2026-10-02 (sitting 2), D-MON-2:* the watch reads use the same read-only, operator-performed scope as the S-X3 recovery read set.
- **OQ-3** (operator). W6's policy rows, especially "all channels lost while armed means an operator stop".
  *Ruled, operator ruling 2026-10-02 (sitting 2), D-MON-6:* the W6 table as drafted. The cell 'Armed / all channels lost, or the monitoring provider lost → operator stop' was ruled earlier on 2026-10-02 (coordinator (3) sheet, item E). Neither ruling reclassifies refusals: HR-ADOPT decides which refusals are incidents, and every incident notifies.
- **OQ-4** (operator). Preservation trades on a symbol outside the four while a request is held. *Coordinator note, 2026-10-02:* this proposal conflicts with the F-5 ruling ("automation fenced, then reconciled"), which the operator confirmed on 2026-10-02 as discharging S-X2. F-5 reasons that moving symbols removes no account-wide effect. **F-5 is the default.** This item stays only in case the operator chooses to revisit it.
  *Ruled, operator ruling 2026-10-02 (sitting 2), D-MON-7:* W5 item 3 is adopted as a narrow exception: outside the four while any request is held. F-5 stays the general rule (B–D packet GC-7 addendum).
- **OQ-5** (operator). The W2 cadence, and whether a broker-platform fill notification is wanted as a detector between checks.
  *Ruled, operator ruling 2026-10-02 (sitting 2), D-MON-5:* the W2 cadence as drafted. Broker-platform fill notifications are added only if free and they pass qualification (UNVERIFIED). A missed check pings the D-MON dead-man check (W5 item 1).
