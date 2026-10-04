# D1 / T13 evidence packet: §A12 acceptance and the F3 held-request watch (2026-10-04)

**Status:** Evidence packet for Joshua's D1 decision — prepared by coordinator (4) (halt/resume owner and T13 watch owner by succession from coordinator (2)); not an acceptance, adoption or GO.

**Read at:** origin/main `9c2a153` (the #575 merge). PR #667 head `30d35e1`. Review receipts read with `gh api` on 2026-10-04. Abbreviations: **ADR** = [incident ADR](../adr/2026-09-17-bounded-platform-protection-incident-contract.md); **W** = [F3 watch draft](2026-10-02-t13-a12-f3-held-request-watch-draft.md); **HR** = [halt/resume contract](../spec/2026-09-14-tb-s3-halt-resume-contract.md); **PK** = [A12 acceptance packet](2026-10-02-a12-acceptance-packet.md) (main); **PK667** = the same file at #667 `30d35e1`; **OPT** = [D-MON options packet](2026-10-02-d-mon-channel-options-packet.md); **GB** = [Grafana IRM binding card](../briefs/handoffs/2026-10-03-dmon-grafana-irm-binding-card-DRAFT.md) (#635); **HB** = [missed-heartbeat card](../briefs/handoffs/2026-10-03-dmon-missed-heartbeat-monitor-card-DRAFT.md) (#637); **DOT** = [dot intake card](../briefs/handoffs/2026-10-03-dmon-dot-incident-intake-card-DRAFT.md) (#636); **NC** = [notifier round/job cap card](../briefs/handoffs/2026-10-03-notifier-round-job-cap-card-DRAFT.md); **T13C** = [T13 first-session card](../briefs/handoffs/2026-10-02-t13-first-session-attended-procedure-DRAFT.md). Line numbers are at `9c2a153`.

Settled rulings are cited, not reopened: D2–D7 and the stale-evidence choice (ADR:548, :552, :554, :557), D8 (ADR:561), W2 cadence (D-MON-5, W:32), W3 read authority (D-MON-2, W:51), W6 channel loss (D-MON-6, W:82), W5 item 3 outside-four (D-MON-7, W:67).

## §1 W1 attendance

**W1 text (W:26–28):**

> - The watch starts when the incident session's recovery ends with at least one held request ([S-X3 draft](2026-10-02-t13-c-a-attended-recovery-draft.md) §8).
> - **Proposed reading of HR :57 for this case** (the halt/resume owner decides; OQ-1). Attendance for the session ends once stop, intervention and disarm are done and read back, and the watch is scheduled. The held request does not keep the session attended indefinitely: the watch carries it. HR :57 requires stop, intervention and disarm before leaving. F3 says disarm does not end the watch; it does not say disarm cannot end attendance.
> - The account stays HALTED. No later session may activate while any request is held (F3; HR :65, "unresolved owner cannot be overridden").

W's HR citations are anchored at `bd30646` (W:17). At `9c2a153` the attendance sentence is HR:61 and "unresolved owner cannot be overridden" is HR:79.

**Proposed owner reading, for Joshua's confirmation.** HR:61 says "Attendance continues until reconciled/disarmed, including incidents beyond the planned end. To leave early, complete stop/intervention/disarm first." While a request is held, "reconciled" cannot happen: recovery needs "no unresolved requests" (HR:55; ADR:453). The reading is that the "/" is an "or". Attendance for an incident session with a held request ends when all of these are done and read back:
1. the operator stop (HR:98, O-6);
2. intervention: every position and working order the reads show is managed by Joshua on the platform (HR:53). *Proposed addition:* closed or cancelled and read back, so the exposure left is only what the held request itself can still produce;
3. the disarm, persisted and read back (`dry_run=true`, `armed_until=null`), with HALTED kept (HR:57);
4. the closing check (W:34) is recorded, and the next W2 check is scheduled with its missed-check ping armed (W:64).

HALTED, the activation block (HR:79; ADR:453) and the watch carry the held request after that. This does not read HR:61 as ending the watch (ADR:460: "Disarm does not satisfy it"). Disarm stops new runtime risk. It does not stop the held request from acting.

**Remaining exposure between checks** (a check is due at each session open and before any activation, W:35–36):

| # | What can happen while a request is held | How long | Worst case | Existing bound (source) |
|---|---|---|---|---|
| E1 | A held entry or add fills late | Until the next check: overnight, longer over a weekend or holiday (W:35) | A position up to the request's quantity, protected only by whatever it carried. If nothing was attached, or protection failed, it is unprotected | Reservation held as bookkeeping only; it does not prevent a fill (ADR:435). HALTED: no runtime mutation, so nothing reacts (ADR:436). W:39: "Between checks, nothing watches the account … bounded only by the held request's quantity and whatever protection it carries." **GAP** between-check detector: broker fill notifications are "only if free and they pass qualification (UNVERIFIED)" (W:32). Owner: T13 (coordinator (4)); qualification by Joshua |
| E2 | A resting entry whose cancel was unknown stays working and fills | As E1 | As E1 | "An unknown cancel of a resting entry leaves that entry's reservation held under F2" (ADR:468). Same bounds and GAP as E1 |
| E3 | A child, sibling or coverage-repair effect (bracket/OCO leg) acts | As E1 | An unexpected order or position on any symbol | The request "stays unresolved while any child, sibling or coverage-repair effect is unexplained" (ADR:443). At the next check, F5 makes it an incident (ADR:480; W:59) |
| E4 | A held close or flatten executes late after Joshua flattened by hand | As E1 | An opposite-direction position of up to the close quantity | C-a M1–M9 all OPEN (ADR:532). No control between checks. Proposed step 2 above does not remove it. **GAP**: the close-semantics owner (R-CLOSE, coordinator) owns the evidence; T13 owns detection |
| E5 | A scheduled check is missed and nobody notices | Unbounded | E1–E4 run on with no end | Ruled: "A missed check pings the D-MON dead-man check (W5 item 1)" (W:32). **GAP**: no card binds that check (§2) |
| E6 | A check's reads fail, or the platform is unavailable | Until a retry succeeds | Exposure unknown | "Check **missed**, not passed. Retry. If exposure is suspected, Joshua flattens directly on Tradovate (D-MON-3)" (W:60). Existing **GAP**: Tradovate itself unavailable (S-X3 draft:114) |
| E7 | A cross-session read misses a late fill | Until a later read finds it | A fill that goes unseen | Fills-history completeness is unverified, and "a miss there is not evidence of no fill" (W:47). Cross-session recovery UNESTABLISHED (ADR:462). Mitigated only by the order-state and position reads (W:45–46) |
| E8 | An operator preservation trade is mistaken for a late effect | Until the trade is recorded and its fills are reconciled. Closing it does not end this: the next check reads fills since the previous check (W:47), so a completed round trip still appears | Misclassification | Outside the four while any request is held (D-MON-7, W:67). An unrecorded operator action is an incident (ADR:480). **GAP**: the record form is routed, not defined (A-3, §3); owner T13 / O-5 (HR:124) |

## §2 Watch mechanics

### Bound in merged text (ruled, or in a merged card)

| Piece | Text | Status | Owner |
|---|---|---|---|
| Provider and chain | OPT:124: "A, with media as A describes … *Done 2026-10-03:* … the configured chain is push and SMS at t=0, then a phone call at 1 minute (OQ-3)." GB:62: "**Important** rules: step 1 = SMS **and** Mobile push important, then a 1-minute wait, then a phone call." | Ruled and configured. GB is **DRAFT, not frozen**: "freezes after #628 merges" (GB:3). #628 merged at `6e679cc`, and GB §12 records no freeze (GB:289). Live qualification Q7 is still owed (GB:178). Free-tier SMS and calls after 2026-10-16 are UNVERIFIED (GB:85) | Joshua (account, OA acts); coordinator (4) (freeze, by the 10-03 handoff) |
| 60 s escalation | HR:63: "Escalate through an alternate configured channel at 60 seconds after the first notification attempt without acknowledgment". GB:261: "OQ-2 RULED YES … ≤ 90 s passes, > 90 s fails" | Ruled; qualification owed (Q7) | HR owner; GB |
| Silent runtime and notifier | HB:9: "Two `HeartbeatPinger` instances … the book runtime's loop progress, the other by the #628 notifier's loop progress". NC:217: on a stalled round, "#637's notifier heartbeat stops marking, and the dead-man check pages once no mark has arrived for T_n" | HB is **DRAFT** (HB:4). T and P are **OWED** (HB:100). NC is **FROZEN 2026-10-04** (NC:4). Neither covers watch checks | coordinator (4) |
| Cadence | W:34–36: a closing check, a check at each session open, and one before any activation | Ruled (D-MON-5, W:32) | Joshua performs; T13 |
| Read set | W:51: "the same read-only, operator-performed scope as the S-X3 recovery read set" | Ruled (D-MON-2) | Joshua |
| Channel loss | W:73–78, table | Ruled (D-MON-6, W:82) | Joshua; T13 |
| Missed check alerts | W:32: "A missed check pings the D-MON dead-man check (W5 item 1)." | Ruled **as policy only**: no integration, interval or grace is specified | see GAP G1, G2 |

### Proposed (W text, not yet adopted)

- **Start and attendance:** W1 (W:26–28) and the owner reading in §1 (OQ-1, W:96).
- **Classification:** W4 table (W:55–60). "Nothing new" is "**Not a release**: absence never releases".
- **Dead-man design:** "a dead-man check at the chosen D-MON provider …, scheduled to match W2 with a grace the operator sets. The operator, or the read tool, pings it when a check completes" (W:64).
- **F5 alert:** "on the primary channel, with the 60 s alternate escalation" (W:65).
- **Owner and records:** "**Obligation:** the attended-operations contract (checklist T13). **Performer:** Joshua … **Recorder:** the coordinator" (W:86). STATE trigger row on adoption (W:87). "**Each check's record:** its time, the reads, the results and the W4 class, marked complete or missed. Original read bytes stay private" (W:88).

### GAP

| ID | Gap | Nearest owner |
|---|---|---|
| G1 | No card binds the watch's dead-man check: which IRM heartbeat integration, its interval, who pings it, and how an irregular per-session-open cadence (weekends, holidays) maps to a fixed heartbeat interval. GB covers incident publish, HB covers the runtime and notifier, and DOT covers issue intake (DOT:8). None mentions the held-request watch | coordinator (4), as T13 watch owner (an HB addendum or a new small card) |
| G2 | Grace not set ("a grace the operator sets", W:64) | Joshua (§5 Q3) |
| G3 | Completion record: contents are proposed (W:88), but no location or form is named. Today nothing proves a check happened except the dead-man ping, which is itself unbound (G1) | coordinator (4) (T13 recorder, W:86) |
| G4 | No between-check detector (E1–E4); broker notifications UNVERIFIED (W:32) | T13; Joshua qualifies |
| G5 | Operator-action record form (A-3) | T13 with O-5 (HR:124) |
| G6 | STATE has no watch row (STATE.md:61 onward); owed on adoption (W:87) | coordinator |
| G7 | Tradovate unavailable during a check (S-X3 draft:114) | T13 (existing GAP) |
| G8 | Grafana IRM itself down: "**nothing**" detects it (HB:124) | D-MON (OPT OQ-5); out of HB scope |
| G9 | OQ-1 owner reading unruled (W:96); §1 proposes one | coordinator (4) as halt/resume owner, with Joshua's confirmation |
| G10 | No qualification exercises the watch's dead-man check: an end-to-end run that deliberately omits a scheduled watch ping and records that the page arrives. Q7 qualifies the incident integration (GB:113); HB-L1/L2 qualify the runtime and notifier heartbeats (HB:9). Owed before the first armed session, where D-MON qualification sits (deployment checklist:601). §5 Q4's proviso names Q7 and HB-L1/L2, not this | coordinator (4) specifies it with G1; Joshua runs it |

## §3 Exact-text reconciliation

**Text drift since the reviews.** The step-4 reviews read §A12 at `7928327`. The ADR then changed at `5d285f7` (narrowing: §A12.4 and §A12.6 moved to PK; stale-evidence row added), at `4a2a136` (sitting-2 dispositions) and at `a87497e` (change-history pointer). `git diff a87497e 9c2a153` is empty for the ADR.

| Item | Review / receipt text | Current owner text (path:line) | Carries? | Remains before D1 |
|---|---|---|---|---|
| Step-4 (a), refute-first (ADR:565) | #584 c.5939229092 at `7928327`: "### Verdict: **CLEAN_WITH_ACCEPTANCE_ITEMS**" … "**There are no MERGE-BLOCKING findings.**" | ADR:565: "(a) a separate-session refute-first review, under D-codex (a), spawned by the coordinator and not by the author" | **Partial.** It covers `7928327` only. The `5d285f7`, `4a2a136` and `a87497e` changes had no refute-first review. Carry 5962662335 is a carry of the Codex relay CLEAN at `5d285f7`, not of this review | A scoped separate-session refute-first review of the `7928327..a87497e` §A12 delta and the integrated watch text, or Joshua's explicit carry (§5 Q2). PK667:24 agrees: "final integrated D1/watch text still need scoped review" |
| Step-4 (b), Codex on the PR (ADR:565) | Bot c.5939067414 at `7928327`: "Didn't find any major issues." Relay c.5960733525 at `5d285f7`: "CLEAN", carried to `368f366` by 5962662335: "PR diff byte-identical". #638 c.5966073018 at `a87497e`: "CLEAN (whole 28-file documentary review)" | ADR:565: "(b) a cross-vendor Codex review on the pull request" | **Yes for the ADR text** (`a87497e` = current). Caveats: #638 is "documentary scope" and "byte identity rests on reconstructed evidence" (5966073018). The watch draft and PK667 are not covered | Nothing for the ADR. A Codex review on #667 and on the watch adoption text, if those are part of the D1 act |
| A-1 | "§A12.2 item 2 assumes D2(ii) is 'no'." Fix: "Make `:487` conditional on D2(ii)" | ADR:489: "This item's attended-recovery release holds because D2(ii) is answered 'no' (operator ruling 2026-10-02 (sitting 2), §A12.5; effective with D1)" | **Yes.** D2(ii) has been answered "no" (ADR:548), so the conditional is discharged | None. UB-7 producer evidence stays owed (ADR:529; PK667:13) |
| A-2 | "`:422`'s list of what §A12 adds leaves out the held-request watch". Fix: "Add the watch to `:422`'s list." | ADR:424: "… the F3 held-request watch, which no accepted owner carries until the attended-operations owner adopts it (a D1 precondition, §A12.5)" | **Yes** (fold). ADR:419's "already carried by an accepted owner" becomes true only on T13 adoption | T13 adoption (§4 row 6) |
| A-3 | "'A recorded operator action' has no defined record or owner." Fix: "Route it with O-5 … or T13 before an operator preservation trade happens during a held request." | ADR:480: "Who records an operator action, in what form, and whether before or after it, is routed with O-5 … and to the attended-operations contract (checklist T13). It must be settled before an operator preservation trade is placed while a request is held" | **Partial.** Routed as asked. The form is still undefined, though HR:124 (armed sessions: no book-symbol trade without an operator stop) and D-MON-7 (W:67) narrow it | T13 defines the record before any preservation trade while a request is held (G5). Not a D1 precondition on ADR:542's list |
| A-4 | "It should name §A2, §A8 and §A10"; "Consider moving [revision notes] to the change history at acceptance"; ":597 still says 'decisions D1–D6'" | ADR:417: "The text of §A2, §A8 and §A10 stays preserved"; ADR:587: "decisions D1–D6 (D7 and D8 were added later; see §A12.5 …)" | **Yes** for the antecedent and the history row. The optional note move is not done (ADR:411–417 still interleaves notes) | Optional editorial step at acceptance; not a precondition |

## §4 D1 readiness checklist

D1 ruling (ADR:542): accept "in one act once all of these hold". List items are at ADR:544–557.

| # | Prerequisite | Source | Status | Owner |
|---|---|---|---|---|
| 1 | #575 merged | ADR:542 | **Met.** MERGED 2026-10-04T17:03:23Z at `9c2a153800c14a45e4f0f835d765c6643e9aae43`. PK667:59 still says "still open at `aa20360`"; correcting that belongs to #667's author | — |
| 2 | Both step-4 reviews clean | ADR:544, :565 | **Partial** (§3): (b) met for the ADR; (a) predates three ADR revisions | coordinator (4) dispatches; Joshua (§5 Q2) |
| 3 | D2–D7 recorded | ADR:545–554 | **Met** (sitting 2; effective with D1) | — |
| 4 | Stale-evidence choice recorded | ADR:556–557 | **Met.** The TB-I3 latch implementation is owed but is not a D1 precondition | TB-I3 |
| 5 | A-1–A-4 folded | ADR:542 | **Met** as folds (§3). A-3's record form stays owed to T13 | T13 |
| 6 | T13 adopts the F3 watch, before or in the same act | ADR:542, :555; PK:30 | **Owed.** Inputs: OQ-1 (§1, unruled); G1–G3 unbound; coordinator acceptance of W as T13 owner text (W:92); STATE row (G6) | coordinator (4); Joshua confirms OQ-1 and the grace |
| 7 | D-MON channels for the watch | ADR:534; PK:30 | **Partial.** The channel choice is ruled and the Grafana chain configured (OPT:124), the input adoption names (W:92). Watch dead-man unbound (G1). Arming readiness, not a D1 gate: provider qualification runs before any armed session (deployment checklist:601), including Q7 and G10. HB (runtime and notifier liveness, HB:9) and DOT (issue intake, DOT:8) do not supply the watch's channels | coordinator (4); Joshua (OA acts, Q7) |
| 8 | D8 | ADR:559 | Not a precondition; deferred (ADR:561) | — |
| — | Context, not a D1 gate | ADR:567 | D1 grants no dispatch, drill, arm, deployment or spend. Live release stays held | — |

## §5 Decisions Joshua would make (not already ruled)

1. **Q1 — Attendance reading (OQ-1).** With a request held, does session attendance end once stop, intervention (every visible position and order closed or cancelled and read back), disarm read-back and the closing check are done, with the watch carrying the request? **Recommended: yes.** Consequence: no indefinite attended session. Exposure E1–E4 between checks is accepted as W:39 already states; E4 is the residual that flattening by hand cannot remove.
2. **Q2 — Step-4 review (a).** Before D1, run one scoped separate-session refute-first review of the §A12 changes `7928327..a87497e` plus the watch adoption text, or accept the `7928327` verdict as carried? **Recommended: run the scoped review** (one focused reviewer). Consequence: one review before D1. Carrying instead means D1 rests on a refute-first review of an earlier text, with only Codex covering the delta.
3. **Q3 — Missed-check grace.** How long after a scheduled watch check may its dead-man ping be late before it pages? **Recommended: 60 minutes.** Consequence: a skipped check pages within about an hour. A late fill is still found only at the check itself (E1).
4. **Q4 — Adoption before the detector is built.** May T13 adopt the watch, and D1 proceed, with the missed-check detector (G1) and channel qualification (Q7, HB-L1/L2) specified but not yet built, provided both are an arming precondition before the first armed session? **Recommended: yes.** Consequence: D1 is not blocked on build work. No held request can exist before the first armed session, and D1 grants no arm (ADR:567).

## Source contradictions found

- PK667:59 calls #575 open. It merged at `9c2a153` (correction: #667's author).
- W cites HR at `bd30646` lines (:49, :57, :59, :65, :84, :110). At `9c2a153` they are :53, :61, :63, :79, :98, :124. The HR owner readings inserted at HR:67–75 shifted them. Correct at adoption.
- T13C:72 and :175 still treat W5 item 3 versus F-5 as an open conflict, and I5/I6 as "unmerged (#606)" (T13C:90–91). D-MON-7 (W:67) ruled the conflict, and #606 has merged. Refresh at T13C freeze.
- The OPT:124 ruling text ("push, SMS at 1 minute, then a phone call") differs from the configured chain (SMS and push at t=0, call at 1 minute; OPT:124 "Done" note; GB:62, :262). The later OQ-3 ruling governs; no action beyond noting it.
