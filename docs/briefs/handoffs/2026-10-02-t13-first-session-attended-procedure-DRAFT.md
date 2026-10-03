# T13 — first-session attended operating procedure — worker card (DRAFT)

**Date:** 2026-10-02.
**Status:** DRAFT. Not frozen, not dispatched. The coordinator freezes a committed revision, records the §9 choices and dispatches.
**Brief type:** CC handoff, documentary assembly with an operator rehearsal plan.
**Parent:** [deployment checklist T13](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md) (`:266–276`), narrowed for the first release by its [2026-10-01 addendum](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-10-01--first-session-simplification-rulings-six-cuts) item 5 (`:597`): "T13's T16 acceptance covers the first session only, which is the initial activation." The checklist carries no authority block, so it bounds nothing beyond this card's seat checks.
**Selected outcome:** One written first-session attended operating procedure, assembled from the inputs in §1 and linking them rather than restating them, that the coordinator can accept as T13 owner text. Its acceptance discharges C-a register row S-X3 (once the register is accepted) and is the attended-operations owner's adoption of the §A12 F3 held-request watch, which §A12 D1 requires before or with its acceptance.
**Ownership:** One worker drafts. The coordinator accepts the text. The operator performs every rehearsal in §6 and rules on §7. Joshua merges.
**Return boundary:** A pushed `claude/*` branch with the §3 file, or a precise blocker. Out of scope: code, T09, T16, later-session activation and backup-restore (§5).

```yaml authority
seat: worker
parent: docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push]
constraints:
  - no_main_write
  - no_merge
  - no_pr_unless_coordinator_records_it
  - docs_only_section_3_file
  - no_code_change
  - no_owner_record_edit
  - link_inputs_do_not_restate
  - no_rail_deploy
  - no_rail_arm
  - no_account_traffic
  - no_broker_vendor_or_firm_contact
  - no_external_send
  - no_provider_account_or_spend
  - no_credentials_or_private_data_in_repo
  - no_operator_decision_taken
acceptance:
  - "Every procedure step P1-P8 (§2) cites its owner by file, section and pinned revision; each step resting on a PROPOSED input is marked PROPOSED with the input ID (I1-I7)"
  - "Every step no input carries is a GAP row naming its nearest owner; the file states no new rule"
  - "Each halt/resume §4.1 incident class and each PROPOSED §4.2 C-a outcome (O0-O8, R-T9) maps to a recovery path, or to a GAP"
  - "The rehearsal table carries RH1-RH8 with performer, prerequisite, authorization and evidence; no row is order-producing"
  - "The decision list carries every §7 item, undecided, with its owner"
  - "git diff --stat origin/main...HEAD lists the §3 file only"
  - "python -I scripts/fp.py check: status completed, exit 0, source stable; or a pre-existing failure disclosed with its reproduction on unmodified origin/main"
```

## §0 — Read first (report before writing; otherwise `NEEDS_CONTEXT`)

Read at the dispatch revision. Drafted against origin/main `10b3929` (2026-10-02), PR #606 head `63dcf87` and PR #604 head `3747a17`.

| Input | Where | Read |
|---|---|---|
| Incident ADR | [`docs/adr/2026-09-17-bounded-platform-protection-incident-contract.md`](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md) (§A12 merged PROPOSED, #584 at `4161fa9`) | §A11 items 1, 2, 4 (`:357–360`); §A11.2 with O-6/O-7 (`:382–394`); §A11.3 (`:396`); §A12 F1–F6 (`:426–482`); §A12.5 incl. D1 prerequisites (`:525–552`) |
| §A12 acceptance packet | [`docs/notes/2026-10-02-a12-acceptance-packet.md`](../../notes/2026-10-02-a12-acceptance-packet.md) (#603 at `6de8949`) | §A12.4 T13/D-MON row (`:30`); §A12.6 D1–D8 (`:35–51`); carried Codex findings (`:9–15`) |
| C-a selection register | [`docs/notes/2026-09-26-close-semantics-c-a.md`](../../notes/2026-09-26-close-semantics-c-a.md) addendum 2026-10-02 (merged PROPOSED, #593 at `c5bd051`) | §R.3 O0–O9 (`:404–420`); S-X1–S-X3 (`:466–472`); R-5 (`:502`); R-T9 (`:492`); 2026-09-27 addendum item 5 (`:302`) |
| S-X3 recovery draft | `docs/notes/2026-10-02-t13-c-a-attended-recovery-draft.md` on PR #606 (`git show 63dcf87:<path>`) | All |
| F3 held-request watch draft | `docs/notes/2026-10-02-t13-a12-f3-held-request-watch-draft.md` on PR #606 | All |
| D-MON options packet | `docs/notes/2026-10-02-d-mon-channel-options-packet.md` on PR #606 | §1 N1–N10, §3, §6, §7, §8 |
| Halt/resume contract (HR) | [`docs/spec/2026-09-14-tb-s3-halt-resume-contract.md`](../../spec/2026-09-14-tb-s3-halt-resume-contract.md); PROPOSED §4.2/§4.3 on PR #604 (`git show 3747a17:<path>`) | §2 (`:34`, `:43`); §3 (`:47–61`); §4 (`:63–71`); §4.1 incl. O-5 (`:84`, `:110`); #604 §4.2, §4.3 |
| Checklist | as Parent | T13 (`:266–276`); H5 row (`:483`); attended row (`:534`); item 5 T13 and D-MON (`:597`, `:599`); item 7.2 attended recovery excluded from C-a (`:612`) |
| Phase 5 plan | [`docs/superpowers/plans/2026-09-16-phase5-attended-operations.md`](../../superpowers/plans/2026-09-16-phase5-attended-operations.md) | Global Constraints; WP2 (`:63–76`); WP3 (`:78–90`) |
| H5(b) return | [`docs/briefs/handoffs/2026-09-27-h5b-attended-incident-rehearsal.md`](2026-09-27-h5b-attended-incident-rehearsal.md) | Return acceptance (`:314–343`): incident→notification emission ABSENT; real delivery OWED to T13 |
| Commissioning packet | [`docs/notes/2026-09-27-route-commissioning-session-packet.md`](../../notes/2026-09-27-route-commissioning-session-packet.md) | F-5 ruling (`:89`); §2.2 actor inventory; §3.4 recovery |
| Drill plan | [`docs/notes/2026-09-26-tradeify-route-drill-plan-draft.md`](../../notes/2026-09-26-tradeify-route-drill-plan-draft.md) | Actors and firm constraints (`:135–150`); read authorization and known order (`:170–176`) |
| Arming procedure | [`docs/notes/rail_build/ARMING_PROCEDURE.md`](../../notes/rail_build/ARMING_PROCEDURE.md) | Track B incident sequence (`:5–13`) |
| STATE | [`STATE.md`](../../../STATE.md) | Account-preservation trigger (`:66–69`) |

**The report states:** the dispatch revision; for each of I1–I7 (§1) its state at dispatch (accepted, amended or still PROPOSED) and pinned head; and every anchor that moved.

**Known re-pins (found while drafting).**
- The #606 drafts cite §A12.4 and §A12.6 as ADR sections at `e57bd98`. On main they live in the acceptance packet (moved by the coordinator's 2026-10-02 narrowing). Cite the packet.
- The D-MON packet cites the D-MON ruling at checklist `:598` (`bd30646`). On `10b3929` it is `:599`.

## §0.5 — Clarifications and recommended defaults

- **An input still PROPOSED at dispatch.** Assemble against its pinned head and mark each dependent step PROPOSED with the input ID. Never present it as accepted.
- **Two inputs conflict.** Record both readings in a GAP row and return the conflict; do not choose. Known now: the F3 draft's W5 item 3 proposes moving the preservation trade outside the four symbols while a request is held, but the operator's F-5 ruling (commissioning packet `:89`) is "automation fenced, then reconciled", on the ground that moving symbols removes no account-wide effect (§7 F).
- **Link, do not restate** (Rule 7). The procedure is a session-level sequence. For recovery and watch detail it points to the S-X3 and F3 texts by section. It adds only the frame those texts lack (P1–P3, P8, and the non-C-a recovery map in P4).
- **Home of the file.** Coordinator decision C-1 (§7). Until it is recorded, write the §3 file; moving accepted text into ARMING_PROCEDURE is the coordinator's later act, not this card's.

## §1 — Goal, scope and prerequisites

**Goal.** Joshua can run the first attended session from one procedure: readiness before arming, monitoring, incident detection, platform recovery, the watch over any request still held, channel loss, preservation trades while a request is held, and completion with disarm.

**Scope (checklist item 5, `:597`).** The first session only, which is the initial activation. Kept: disarmed fail-closed restart, no restart within a session (§A11.2), the durable unknown-request block. Deferred: later-session activation machinery (Phase 5 WP4) and backup-restore rehearsals (WP3).

**Prerequisites.** Drafting may start now against the pinned heads. Acceptance of the procedure waits as shown.

| ID | Input consumed | State at drafting | Acceptance it waits on | What the procedure takes from it |
|---|---|---|---|---|
| I1 | Incident ADR §A12 F1–F6 | PROPOSED (merged `4161fa9`) | **D1** (§A12.5 `:540–550`): both step-4 reviews clean; dispositions for D2–D7; the held-request watch adopted by the attended-operations owner, or in the same act; the stale-evidence choice recorded. D8 is not a precondition | F1(c) halt and alert; F2 release by unique correlation only; F3 duration and watch obligation; F4 per-type presumptions; F5 unexplained effects |
| I2 | §A12 acceptance packet | Working note (`6de8949`) | None itself; it carries the D2–D8 drafts and three Codex findings that bite at D1 | The §A12.4 T13/D-MON row; D5's routing of channel loss and the late-effect watch to T13 |
| I3 | C-a selection register | PROPOSED (merged `c5bd051`) | Operator acceptance of the register. S-X3 is discharged by the coordinator accepting this procedure as owner text. R-5 (T13 final acceptance through actual consumers) is not this card's | §R.3 outcome model; S-X1 inventory; S-X2 (discharged 2026-10-02 by F-5); R-T9 guard |
| I4 | S-X3 attended-recovery draft | PROPOSED, unmerged (#606, `63dcf87`) | Coordinator acceptance as owner text; its OQ-1 to OQ-6 | Quiescence, residual request accounting, exposure by outcome, the second-close race, firm fallback, completion |
| I5 | F3 held-request watch draft | PROPOSED, unmerged (#606) | Coordinator acceptance; operator rulings on its OQ-2 to OQ-5; halt/resume owner reading on OQ-1; the D-MON choice. Adoption can be the same act as D1 | W1 start, W2 cadence, W3 reads, W4 classes, W5 channels, W6 channel loss, W7 owner and records |
| I6 | D-MON channel options | PROPOSED, unmerged (#606) | Operator D-1 (provider and media) and D-2 (opens the accounts); qualification of its OQ-4 facts | Primary and alternate channels; dead-man heartbeat; the §7 qualification list |
| I7 | Halt/resume §4.2 and §4.3 | PROPOSED, unmerged (#604, `3747a17`) | Halt/resume owner acceptance; FD-1 | C-a incident triggers and the flatten-deadline rule; commissioning reconciliation; first release has no resume; who records the review |
| I8 | Accepted, no wait | — | — | HR rev9 §2–§4 with the 2026-09-27 amendment and §4.1; §A11, §A11.2 (O-6, O-7), §A11.3; checklist item 5 (T13 scope, D-MON) and item 7.2 (incident recovery stays on the attended-platform path, never REST C-a); F-5 (2026-09-28) and its 2026-10-02 confirmation; X-3/X-4 fills count toward weekly preservation; H5(b) accepted PARTIAL (#521) |

**Code dependencies this card does not cover.** Incident→notification emission is ABSENT in the book owners (H5(b) return); the publisher, the attendance record and binding the heartbeat to rail progress are TB-I3 / Phase 5 WP2 build work, not yet carded. CC-3's halt-on-unknown is demonstrated synthetically and not accepted (TB-I3/T09). The procedure states where it depends on each.

## §2 — Procedure scope (what the §3 file must contain)

| Step | Content | Owners to cite |
|---|---|---|
| **P1 Readiness, before arming** | Attendance accepted for the bounded session; platform access and every alert channel tested and acknowledged; GC-7 actor inventory taken, with non-disableable firm actors and their action times; own-flat deadline D and the ~17:00 ET list reset known; recovery read authority in hand or screen-only declared; firm contact path recorded or its absence recorded; no request held (F3 blocks activation while one is) | HR `:57`; D-MON N1, §7 item 7; S-X1; S-X3 draft §2 P1–P5; F3 |
| **P2 Attended monitoring** | Who watches what while armed; 60 s acknowledgment target; alternate escalation at 60 s; failure routing; external heartbeat; acknowledgment is never permission | HR `:59–61`; checklist T13 bullet 4 (`:273`); Phase 5 WP2; I6 |
| **P3 Incident detection and classification** | The HR §2 triggers as HR §4.1 sorts them; I7 §4.2 C-a triggers (O2b, O5–O8, R-T9) marked PROPOSED; a deliberate operator stop is an incident (O-6); correctly handled refusals are not (HR `:43`); every incident ends automation for the session (§A11.2); operator platform actions per F-5 for preservation trades, other O-5 cases OPEN | HR §4.1; I7 §4.2; I1 F1, F5; F-5 |
| **P4 Platform recovery** | A map from each incident class to its recovery: the generic sequence (HR §3; ARMING_PROCEDURE `:5–13`) for every class, and the S-X3 steps for C-a close outcomes. Non-close classes (unknown entry, stale fact, feed gap, restart during halt, protection fault, operator stop) get the S-X3 quiescence and request-accounting steps where they apply and a GAP row where they do not. No REST C-a in recovery | HR §3; I4 §3–§8; I1 F4 table; checklist item 7.2 |
| **P5 Held-request watch** | Start, cadence, reads, classification, channels, records and owner, by reference to I5; the STATE trigger row it needs on adoption (the coordinator's edit) | I1 F3; I5 W1–W7 |
| **P6 Channel-loss policy** | The four states (before arming, armed with primary lost, armed with all lost, disarmed with a request held) and their responses, marked as operator policy pending ruling | I5 W6; I2 D5; HR `:57`, `:59` |
| **P7 Preservation trades while a request is held** | Order: watch check, then the trade (rail disarmed, account HALTED), then reconciliation reads; the trade is a recorded operator action awaiting outcome evidence; the weekly deadline; the F-5 versus W5 item 3 conflict as an open decision | STATE `:66–69`; F-5; I5 W5; HR `:51`; §A11 item 4 |
| **P8 Completion, disarm, review** | Completion only on fresh coherent evidence; disarm read back; stay HALTED; no restart in the session; if a request is still held, disarm before leaving and hand to P5; review before another session, with §4.3's proposed reviewer marked PROPOSED | HR `:51–57`, `:71`; I1 F3; I7 §4.3 |

Each step also lists its evidence (what is recorded, where; original bytes stay private in the primary checkout) and its rehearsal ID from §6.

## §3 — Files

- **New:** `docs/notes/<dispatch-date>-t13-first-session-attended-procedure.md`. Status line PROPOSED as T13 owner text. Sections: P1–P8; a GAP table; the rehearsal table (§6) with an empty log; the decision list (§7).
- **Nothing else.** Every other file, including the inputs, the ADR, the halt/resume contract, the register, the checklist and STATE, is out of scope (§8).

## §4 — Hypothesis and falsifier

**H:** the inputs I1–I8 carry every step of a first-session attended procedure, so the procedure can be written as a sequence of links without a new rule.

**Falsifier.** If a step in P1–P8 needs behavior that no input carries, accepted or PROPOSED, then H fails for that step: the worker writes a GAP row naming the nearest owner and returns it, and does not write the rule. If a step contradicts an accepted owner (I8), then stop and return (§8). Accept the return if every step traces or is a named GAP; reject it if any step states a rule without an owner.

## §5 — Forbidden moves and out of scope

- Code of any kind, including the notification publisher, attendance record, heartbeat binding, incident view and any `ops/` change (TB-I3 / Phase 5 WP2).
- T09 (R-T1 to R-T9, CC-3 acceptance, the rail-spec amendment) and T16 (binding and combined acceptance).
- Later-session activation (WP4), backup-restore (WP3 restore steps) and R-5's actual-consumer traces.
- Editing any owner or input: the incident ADR, the acceptance packet, the register, the halt/resume contract, the #604/#606 drafts, the checklist, ARMING_PROCEDURE, STATE or the campaign record. Contradictions return.
- Deciding any §7 item, or writing a cadence, threshold, channel or policy row as settled.
- Account, broker, vendor, firm or provider traffic; opening a provider account; spend; any message to an external party.
- Credentials, account identifiers, figures or original read bytes in any committed file.
- A merge, a push to `main`, or a PR the coordinator has not recorded in §9.

## §6 — Acceptance and return

**Worker return (coordinator accepts).**

The `acceptance` entries in the authority block. The coordinator re-runs the §10 hooks at the returned head.

**Return status:**
- `DONE`: the §3 file meets every acceptance entry.
- `DONE_WITH_CONCERNS`: as DONE, with GAP rows or input conflicts listed for the coordinator.
- `NEEDS_CONTEXT`: an input moved or was replaced since drafting and the §0 report cannot pin it.
- `BLOCKED`: a step contradicts an accepted owner, or a §8 stop fired.

**Return contents:** branch and head; the §0 report; the GAP list with nearest owners; the input conflicts; the `record.json` path of the `check` run.

**Procedure acceptance: operator-performed rehearsals, after the coordinator accepts the text.**

None is order-producing. Reads use the operator's credential under the drill plan's read-authorization rule (`:174`): written authorization per read set, the known-order definition confirmed, and entitlement confirmed. An agent performs a read only when that written authorization names the agent, the reads and the target. Original bytes stay private.

| ID | Rehearsal | Performer | Needs | Evidence | Supports |
|---|---|---|---|---|---|
| RH1 | Tabletop: walk each HR §4.1 incident class and each I7 §4.2 outcome through P3–P8 on paper | Operator with the coordinator | The accepted text | Dated log row: classes walked, steps that held, gaps found | S-X3 discharge; P3–P8 |
| RH2 | Channel test: provider test alert acknowledged; no acknowledgment escalates to the alternate at 60 s; a primary delivery failure routes at once | Operator | D-MON D-1, D-2; synthetic content; $0 tier | Measured times, labelled operator-reported | D-MON §7 items 3, 4, 7; P1, P2 |
| RH3 | Dead-man heartbeat: manual pings, then none; both channels alert within the qualified threshold | Operator | As RH2 | Threshold and alert times | D-MON §7 item 1 (manual form); P5 W5 item 1 |
| RH4 | Platform access: log in; find positions, working orders and the single-instrument exit per symbol; place nothing | Operator | — | Dated attestation | P1; P4 |
| RH5 | Recovery read set: the S-X3 §4 first reads against a known order the operator places anyway (§A11.3), such as the weekly preservation trade or an X-3/X-4 order | Operator, or a named agent under written authorization | §7 G1 authorization; known-order definition confirmed (drill plan `:176`) | Read times and outcomes; bytes private | P4; S-X3 §4 |
| RH6 | Watch-check dry run: one W3 check on a flat account, W4 class recorded, dead-man ping sent; includes the cross-session fills-history read to see what it returns | As RH5 | As RH5; RH3 | Check record per W7 | P5 |
| RH7 | Firm fallback path: Tradeify's route for flattening an evaluation position, its hours and how it identifies the account | Operator; any message to Tradeify is the operator's | §7 G4 | Path recorded, or the gap accepted by the operator | P4; S-X3 §7 |
| RH8 | GC-7 inventory taken once on the commissioning packet's §2.2 form | Operator | — | Inventory record, private | P1; S-X1 |

**Owed elsewhere:** a synthetic rail incident reaching the channels, separately persisted detection/attempt/delivery/attendance, and acknowledgment surviving restart (D-MON §7 items 2, 5, 6) need the publisher and are the T13 build's; real delivery and intervention through actual consumers is R-5, after T09. Any order-producing recovery rehearsal (a platform flatten, the second-close race) is an individual drill decision (§A11.1 item 5).

## §7 — Decisions the procedure needs (listed, not decided)

**Operator.**
- **A. §A12 acceptance.** D1 accept, amend or reject (order: #575 merged, then this text, then gate B); D2 (i) the runtime class and (ii) whether §59 Ruling 7(b)(3) reaches attended recovery; D3; D4; D5; D6; D7; the stale-evidence choice (an explicit no-auto-resume rule for the refusal path, or stale evidence as an incident).
- **B. Register.** Accept the C-a selection register, within which S-X3's discharge counts.
- **C. Halt/resume (#604).** Accept HR §4.2; FD-1, (a) cap the flatten window at the time left to D or (b) keep D as the bound; accept HR §4.3 reconciliation and its reviewer reading.
- **D. D-MON.** D-1, provider (A, B or C) and primary and alternate media; D-2, opening the accounts.
- **E. Watch (I5).** Cadence and the optional platform fill notification (OQ-5); the channel-loss rows, especially "all channels lost while armed is an operator stop" (OQ-3); read authority for watch reads (OQ-2).
- **F. Preservation trades while a request is held.** Keep F-5 (fenced, then reconciled, on the book's symbols), or adopt W5 item 3 (a symbol outside the four). F-5's stated ground argues against W5 item 3.
- **G. Recovery (I4).** G1, a recovery read set authorized at session GO, or screen-only reads with no original bytes (OQ-2); G2, the second-close race choice when the liquidation cannot be identified (OQ-3); G3, whether Manual Lockout is ever a recovery tool (OQ-4); G4, establishing Tradeify's contact path (OQ-5).
- **H. Rehearsals.** Which of RH1–RH8 run before the first session; written authorization for RH5 and RH6, naming the performer; whether any order-producing recovery rehearsal is wanted.

**Coordinator.**
- **C-1.** Home of the accepted procedure: the §3 note as T13 owner text, or folded into ARMING_PROCEDURE's Track B incident sequence (S-X3 draft OQ-1).
- **C-2.** Accept I4 and I5 as owner text, after the §0 re-pins.
- **C-3 (halt/resume owner).** The HR `:57` attendance reading for a disarmed account with a held request (I5 OQ-1); whether a bounded publish with provider deduplication meets HR `:61`'s outbox (I6 OQ-1); for option C only, whether fan-out meets the 60 s escalation (I6 OQ-3).
- **C-4 (propagation, at acceptance).** §A12 F5 and HR §4.1 O-5 still list operator-placed preservation trades as OPEN; F-5 now answers that case for the register (S-X2). The owners record it when they next amend.

## §8 — Stop conditions (return; do not work around)

- A step contradicts an accepted owner (I8).
- An input was merged, amended or closed after drafting in a way that changes a step, and the §0 report cannot pin it.
- A needed change falls outside the §3 file.
- A step can be written only by deciding a §7 item.
- Two failed corrections of the same issue (AGENTS.md).

## §9 — Dispatch record

Empty while DRAFT. At dispatch the coordinator records: the frozen revision; the executor; the branch, cut from `origin/main`; C-1; whether a PR is opened; and the pre-dispatch `check_handoff_authority` result.

## §10 — Audit hooks

```bash
# Card form and authority (Expected: well-formed; 0 violations; exit 0)
python -I scripts/fp.py python scripts/check_handoff_brief_form.py
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-02-t13-first-session-attended-procedure-DRAFT.md

# Inputs still at their drafting heads (a moved head is a §0 report item)
git ls-remote origin refs/heads/claude/t13-dmon-prep refs/heads/claude/haltresume-ca-proposed   # 63dcf87… / 3747a17…

# Scope at return: the §3 file only
git diff --stat origin/main...HEAD

# Gates
python -I scripts/fp.py check
```
