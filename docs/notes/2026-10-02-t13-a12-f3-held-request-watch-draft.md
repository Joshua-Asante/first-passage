# Draft: held-request watch for incident ADR §A12 F3 (T13 preparation) — 2026-10-02

**Status: DRAFT. PROPOSED as attended-operations (T13) owner text.** §A12 is itself PROPOSED ([PR #584](https://github.com/Joshua-Asante/first-passage/pull/584), head `e57bd98`). Nothing here takes effect until §A12 and this text are both accepted. This note does not edit the incident ADR or the halt/resume contract. Its cadence and policy rows are proposals for the operator.

**Traces to** (incident ADR on PR #584 head `e57bd98`; line numbers on that head):

| §A12 text | What it asks | Here |
|---|---|---|
| F3, *Watching a held request* (:460) | While any request is held, a check for unexplained effects at each session open or at another cadence the owner names. Disarm does not satisfy it. Owner: attended operations (checklist T13), with the D-MON channels | W1–W5 |
| §A12.4 (now in the [A12 acceptance packet](2026-10-02-a12-acceptance-packet.md); removed from the ADR by the 2026-10-02 narrowing), row *Attended-operations contract (checklist T13) and D-MON* (:540) | Cadence, channels and binding owner, plus alert-channel loss with no incident (D5). Required before §A12's acceptance or in the same act | W2, W5–W7 |
| §A12.5, row *Held-request watch and monitoring loss* (:554) | HR :57's attendance sentence is ambiguous for a disarmed account with a live unknown | W1 |
| §A12.6 D1, third bullet (now in the [A12 acceptance packet](2026-10-02-a12-acceptance-packet.md); D1's prerequisite list is in ADR §A12.5) | The attended-operations owner adopts the watch before or with acceptance | *Adoption* |
| §A12.6 D5 (now in the [A12 acceptance packet](2026-10-02-a12-acceptance-packet.md)) | Alert-channel loss with no incident and the late-effect watch go to D-MON and T13 | W5, W6 |

It also takes the hand-off from the C-a selection register ([PR #593](https://github.com/Joshua-Asante/first-passage/pull/593), head `8d253c9`): outcomes O0 and O5–O8 hold the reservation (REG §R.3), and row S-X3's recovery hands any request still retained to this watch ([S-X3 draft](2026-10-02-t13-c-a-attended-recovery-draft.md) §8).

**Abbreviations.** HR: the [halt/resume contract](../spec/2026-09-14-tb-s3-halt-resume-contract.md). DP: the [drill plan](2026-09-26-tradeify-route-drill-plan-draft.md). REST: the [REST route assessment](../briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md). REG: the register addendum on PR #593. Main-branch line numbers are on origin/main `bd30646`.

## Definitions

- **Held request.** A request whose outcome has become unknown (§A12 F1) and that no accepted F2 class has released. It keeps its worst-case reservation (F1(b)).
- **Late effect.** Any position, working order, fill, child, sibling or coverage-repair effect on any symbol of the account that neither an owned operation nor a recorded operator action explains (F2, last bullet; F5).

## W1 — Start, and the attendance reading

- The watch starts when the incident session's recovery ends with at least one held request ([S-X3 draft](2026-10-02-t13-c-a-attended-recovery-draft.md) §8).
- **Proposed reading of HR :57 for this case** (the halt/resume owner decides; OQ-1). Attendance for the session ends once stop, intervention and disarm are done and read back, and the watch is scheduled. The held request does not keep the session attended indefinitely: the watch carries it. HR :57 requires stop, intervention and disarm before leaving. F3 says disarm does not end the watch; it does not say disarm cannot end attendance.
- The account stays HALTED. No later session may activate while any request is held (F3; HR :65, "unresolved owner cannot be overridden").

## W2 — Cadence (proposal; the operator decides)

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

## W4 — Classifying a check

| Finding | Class | Action |
|---|---|---|
| Nothing new | "No unexplained effect observed at time T with reads R." **Not a release:** absence never releases (F2; closure plan row 3) | Record; schedule the next check |
| An effect that an accepted F2 class uniquely correlates to a held request | Transfer under F2. This needs the operator's D2 and D3 dispositions (§A12.6, now in the [A12 acceptance packet](2026-10-02-a12-acceptance-packet.md)) | Hand to attended recovery (S-X3 draft §4–§8). The halt stays (F3) |
| An effect not uniquely correlated | Incident (F5). It is an additional identified exposure, and the held request stays held; the double count is deliberate | Alert on the D-MON channels (W5). The operator manages exposure on the platform (HR :49; S-X3 draft §5) |
| Reads fail, or the platform is unavailable | Check **missed**, not passed | Retry. If exposure is suspected, use the firm fallback (S-X3 draft §7) |

## W5 — Channels (D-MON)

1. **A missed check alerts.** Proposal: a dead-man check at the chosen D-MON provider ([options packet](2026-10-02-d-mon-channel-options-packet.md) §4), scheduled to match W2 with a grace the operator sets. The operator, or the read tool, pings it when a check completes. A missing ping alerts both channels. This uses the provider's heartbeat feature at no cost and builds nothing in-house.
2. **An F5 finding** goes out on the primary channel, with the 60 s alternate escalation (HR :59).
3. **Operator trades on book symbols confound W4.** F5 does not classify operator platform actions; HR §4.1 O-5 leaves them OPEN (HR :110). Proposal: while any request is held, the weekly preservation trade uses a symbol outside the four. DP :137 already offers that treatment. Operator decision (OQ-4).

## W6 — Alert-channel loss with no incident (§A12 D5)

This is not a halt/resume §2 trigger (§A12 :572). Proposal, by state:

| State | Loss | Proposed response |
|---|---|---|
| Before arming | Any channel fails its test | Do not arm (HR :57) |
| Armed | Primary lost, alternate working | Continue. Delivery failures already route to the remaining channel (HR :59). Record it |
| Armed | All channels lost, or the monitoring provider lost | Operator stop. It is an incident and ends automation for the session (HR :84, O-6), because the 60 s acknowledgment target can no longer be met |
| Disarmed, request held | Any | No session effect. The watch continues on its calendar, and a missed W5 ping is itself the signal. Record it |

These rows are policy, so the operator rules on them (OQ-3).

## W7 — Binding owner and records

- **Obligation:** the attended-operations contract (checklist T13). **Performer:** Joshua, who holds platform and credential access. **Recorder:** the coordinator.
- **On adoption,** STATE.md gains a scheduled-forward-trigger row: "held-request watch due at each session open while any request is held". STATE owns durable obligations (AGENTS.md); this note does not edit it.
- **Each check's record:** its time, the reads, the results and the W4 class, marked complete or missed. Original read bytes stay private and are never committed (public repository).

## Adoption

§A12 D1 makes adoption by the attended-operations owner a precondition of §A12's acceptance, or part of the same act. This draft is the candidate text. Adopting it needs the coordinator's acceptance as owner text, the operator's rulings on OQ-1 to OQ-4, and the D-MON channel choice.

## Open questions

- **OQ-1** (halt/resume owner). W1's reading of HR :57.
- **OQ-2** (operator). Read authority for watch reads (DP :174).
- **OQ-3** (operator). W6's policy rows, especially "all channels lost while armed means an operator stop".
- **OQ-4** (operator). Preservation trades on a symbol outside the four while a request is held. *Coordinator note, 2026-10-02:* this proposal conflicts with the F-5 ruling ("automation fenced, then reconciled"), which the operator confirmed on 2026-10-02 as discharging S-X2. F-5 reasons that moving symbols removes no account-wide effect. **F-5 is the default.** This item stays only in case the operator chooses to revisit it.
- **OQ-5** (operator). The W2 cadence, and whether a broker-platform fill notification is wanted as a detector between checks.
