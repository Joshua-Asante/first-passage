# ORB lifecycle and account fence: disposition after §59 Ruling 6 (2026-09-27)

**Status:** RETURNED for coordinator acceptance. This is work item 1 of [handoff H3](../briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md#h3--orb-lifecycle-and-fence-disposition-owner-text-for-ruling-6-h4-card). For every item returned by #519's ORB lifecycle note and four-state fence trace, it records whether [§59 Ruling 6](../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#ruling-6--orb-resting-entry-lifecycle-l1-and-the-account-fence-classification-contract-2026-09-27) resolves it or it stays open, and who owns it. It changes no code. It accepts, qualifies, freezes or authorizes nothing, and it does not redo #519's analysis.

**Executor:** subagent (Claude Code, Opus 5.5), branch `claude/clever-wozniak-bx0u95`, dispatch revision `521d8f2` (HEAD equals it).

**Inputs, read at their owners:**
- Ruling 6, verbatim, at the campaign record.
- The #519 returns, read at the pinned head with `git show 8c15f18:<path>`, both "ACCEPTED AS INPUT" (`8c15f18:docs/briefs/handoffs/2026-09-26-orb-lifecycle-and-fence-trace.md:99-109`):
  - lifecycle note `8c15f18:docs/notes/2026-09-26-orb-lifecycle-evidence.md`, cited below as **LC**;
  - fence trace `8c15f18:docs/notes/2026-09-26-account-fence-four-state-trace.md`, cited below as **FT**.
- The [B–D packet](2026-09-26-tradeify-bd-decision-packet.md): the fence row, B-13, the four-state table and the §5 T09 hold.
- The [ORB edition production handoff](../briefs/handoffs/2026-09-26-orb-striker-edition-production.md).

**Line anchors:** LC and FT cite line numbers at `62c956f`. That commit is not an ancestor of HEAD (it sits on the #519 branch). However, `git diff 62c956f 521d8f2` is empty for every cited code, test and specification file (§6), so the #519 line numbers hold at HEAD. Anchors below without a commit prefix are at HEAD. **Rail-spec anchors are at `521d8f2`, before the header callout this handoff adds.** In the amended working-tree file each of them sits 17 lines later; for example the `pending` row moves from `:27` to `:44`. **Replay-spec anchors are likewise at `521d8f2`,** and sit 8 lines later after this handoff's callout (RC-9 moves from `:47` to `:55`). Pre-registration anchors do not move, because its markers sit within existing lines. **Halt/resume anchors are also at `521d8f2`.** A concurrent, uncommitted H5 amendment to that contract (not this handoff's) inserts text above them in the working tree: §2 row 1 moves from `:26` to `:32` and the §5 schedule rule from `:67` to `:107` (`git diff -U0` hunks `@@ -2,0 +3,6 @@` and `@@ -63 +69,35 @@`). Where it matters they are also named by section and row.

## Answer in brief

1. **Ruling 6(a) settles the lifecycle conflicts C1–C5 at the contract level.** L1 is adopted. C1 and C4 close in implementation only when H4's replay correction (checkpoint R) is accepted. The AC-3 inconsistency inside C3 is not decided and stays with the rail-spec owner.
2. **Ruling 6(b) settles the spec reading of state (i)** that FT §2 left OPEN. Every state-(i) verdict FT marked "defect only under the proposed reading" is now a defect, repaired synthetically by H4 checkpoint F. FT's first-bar takeover defect was a defect under either reading and still is.
3. **The boundary follows the ruling's words, not FT §6.2** (§3 below). Evidence is fresh only while its age at evaluation is less than one bar period. At an age of exactly one bar period it is stale.
4. **Four things stay open for their owners, as Ruling 6 leaves them:**
   - the rev9 halt for ordinary unknowns and the real evidence producer, both T09/TB-I3, which the ruling retains;
   - positive-lookup (iii)→(i), explicitly "separately held";
   - the rail-spec ambiguities FT §6.7 lists as separate items;
   - four questions this note returns (§5).
5. **Owner text applied under H3 item 2:**
   - [rail spec](../spec/2026-09-12-c1-multi-leg-rail-extension-spec.md): header callout; markers at the §1 `pending` row, S2, S4 and AC-8; a Change history row;
   - [replay spec](../spec/2026-09-12-tradeify-synchronized-replay-spec.md): header callout and an RC-9 marker;
   - [edition pre-registration](../briefs/pre-registration/2026-09-25-tradeify-route-native-editions-prereg.md): ORB-1 marker and the "Open before freeze" marker.

## 1. Ruling 6, as recorded

The owner is the campaign record at `docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md:3985-4010`. The words this note relies on are quoted below. The labels (b1)–(b5) are this note's own, numbering the record's (b) bullets in order. The record's "consequences recorded from the lifecycle evidence, not added rules" are cited as such.
- **(a)** "place the base entry once and let it remain working until it fills or an applicable cancellation ends it. No one-bar expiry and no periodic reissue. The earlier operational cutoff still applies." · "Authorize the corresponding specification/replay correction as a bounded change, with verification before freeze. No historical late-fill count is needed before this decision."
- **(b1)** "A request positively identified as working or partially filled by fresh, qualifying order-level evidence is known working. Retain its capacity reservation; do not block unrelated admission solely because the order is old."
- **(b2)** "Stale evidence blocks further admission. Treat evidence as stale at one bar, explicitly pinning that boundary in tests."
- **(b3)** "A genuinely unknown dispatch blocks immediately. For this slice, retain the conservative terminal-resolution rule; positive-lookup resolution remains separately held."
- **(b4)** "Terminal evidence resolves only the request it demonstrably covers."
- **(b5)** "Refreshed evidence never automatically restores permission after an incident halt."
- **Retained:** "The real evidence producer, route integration and the ordinary-unknown halt (packet CC-3) remain required before the whole fence obligation is accepted."

## 2. Lifecycle conflicts (LC §2) and LC §4 questions

| Item | Status after Ruling 6 | Resolving words, or owner | Where applied / what remains |
|---|---|---|---|
| **C1** strategy and parity basis vs qualification replay (`LC:40`) | **RESOLVED (contract) by 6(a).** Implementation **OPEN** until H4 (R) is accepted | (a): "No one-bar expiry and no periodic reissue"; "Replay-spec RC-9 and rail S2's one-bar sentence are amended so that the one-bar cancel does not end ORB's base entry" (consequences list) | RC-9 and S2 markers (this H3). `replay.py:507-509` and its pin `test_replay.py:214-223`: H4 (R). The size of C1 is not needed: "No historical late-fill count is needed before this decision" |
| **C2** RC-4 vs RC-9 inside the replay spec (`LC:42`) | **RESOLVED by 6(a)** for the accepted book | Same consequence; RC-4's parity basis is kept (H3 card) | RC-9 marker. RC-9's one-bar sentence stays in force for other resting entries or adds. Per `LC:36`, none of the other accepted ports leaves an order resting past the age check. How narrowly the replay correction is scoped is returned as Q3 (§5) |
| **C3** inside the rail contract: S2 vs AC-8, the §5 cutoff and S4 (`LC:44-47`) | **RESOLVED by 6(a)** for S2, S4 and AC-8. The §5 cutoff is unchanged ("The earlier operational cutoff still applies") | (a) as above | S2 sentence struck with a dated marker; S4 "stale resting entries" annotated; AC-8 annotated as the L1 case (no change to its expected outcome) |
| **C3 (separate): AC-3 vs S1** (resting ORB add vs the port's market add; `LC:49`) | **STILL OPEN** | Not decided by Ruling 6. Owner: rail spec (FT §6.7; LC §4 Q5) | Not amended here |
| **C4** qualified vs executed lifecycle (`LC:51`) | **RESOLVED (contract) by 6(a)**: both are L1 with the §5 overlay. Implementation **OPEN** until H4 (R) is accepted | (a); I8 (rail spec `:50`) is unchanged | The live path already has no age-based cancel (`LC:32`, row 11). The replay is corrected by H4 (R). That is an E1 freeze-inventory change (`trust_domain.py:142`, `replay_kernel`) |
| **C5** the ORB pre-registration inherits C1–C3 (`LC:53`) | **RESOLVED by 6(a)** | (a) consequences: "ORB-1 … states the lifecycle in words" | ORB-1 dated marker (this H3). The file stays DRAFT; no OWED row changed |
| LC §4 Q1: L1, L2 or L3 | **RESOLVED**: L1 | (a) | — |
| LC §4 Q2: amend RC-9/S2; authorize the replay change; cutoff first on the rail | **RESOLVED**: yes, yes, yes | (a) consequences; "Authorize the corresponding specification/replay correction as a bounded change, with verification before freeze"; "The earlier operational cutoff still applies" | H3 text; H4 (R) |
| LC §4 Q3, Q4 (L2, L3 follow-ups) | **Not applicable** | L1 chosen | — |
| LC §4 Q5: ORB-1 in words; AC-8/S4 wording | **RESOLVED** | (a); the H3 card directs the AC-8/S4 alignment | Markers only; no new rule |
| LC §4 Q5 (separate): AC-3 correction | **STILL OPEN** | Rail spec | As C3 (separate) above |
| LC §4 Q6: a count of late ORB fills | **RESOLVED: not needed** | (a): "No historical late-fill count is needed before this decision" | No private port run is authorized or needed |
| LC §5 side observation: RC-9 duplicate key `(leg, kind, bar_time)` vs `path_time` in the replay (`replay.py:349`) | **STILL OPEN** | Not a lifecycle item. Owner: replay spec | Not amended here |
| LC §5: broker day-order expiry on the route (`LC:97`; allocation map C08, `docs/notes/2026-09-25-tradeify-capability-allocation-deletion-map.md:95`, "Day-order expiry: `UNVERIFIED`") | **STILL OPEN**, and more material under L1, because the entry now rests for hours | **Owner assigned by the coordinator at acceptance (cross-handoff critic X-12):** the commissioning packet's §3.7 documentary step (primary checkout) also names the `orders/place` time-in-force default, and X-4's step 4 read records the resting entry's time-in-force | Not decided by Ruling 6 |
| B–D packet GC-4: a cancel of a resting stop entry ends its Suspended children | **STILL OPEN** | Operator decision for ORB (packet §1.2 GC-4). Under L1 the cutoff and session-end cancels exercise it | Not decided by Ruling 6 |

**The practical end of the entry on the rail** is the earlier of the port's own session-end cancel and the §5 cutoff (`LC:55`; halt/resume §5 `docs/spec/2026-09-14-tb-s3-halt-resume-contract.md:67`). This is unchanged, and the replay spec already pins it (`early_close_cancellation`, replay spec `:68`).

## 3. The one-bar boundary: FT §6.2 against Ruling 6(b)

**The divergence:**
- **FT §6.2** (i) defines a known working request by evidence that "is at most one bar old at evaluation" (`FT:176`). Under that wording, evidence exactly one bar old is still fresh.
- **Ruling 6(b2)** says "Treat evidence as stale at one bar". Under that wording, evidence reaching one bar of age is stale.
- **FT §6.3** left the choice open: "choose 'older than one bar' (strict) or inclusive" (`FT:186`).

**The ruling's words govern.** Their plain reading is that staleness begins *at* one bar. The boundary is therefore pinned as follows. Let `a` be the `as_of` of the latest qualifying acquisition and `t` the evaluation instant, with `BAR_PERIOD` = 15 minutes (`ops/c1_signal_daemon/book_protocol.py:39`):
- the evidence is fresh when `t − a < BAR_PERIOD`;
- it is stale when `t − a ≥ BAR_PERIOD`.

H4 pins both sides with tests (case 11).

**Consistent, not changed:**
- **The first-bar grace** for an accepted request that has *no* qualifying evidence. It is an existing rule: the S1 cut, "no evidence within one bar" (rail spec `:54`), and the `pending` row timeout (`:27`). Ruling 6 does not restate it. Today's code counts such a request at exactly one bar after preparation (`book_account_owner.py:793`, `now < prepared + BAR_PERIOD`), and `test_book_feedback_journal.py:42-55` pins that at `+15 min`. That is the same inclusive boundary, so the pin stays.
- **The test reference kernel** times out strictly after one bar (`tests/ops/tb_s3_kernel/kernel.py:1326`). It is an unaccepted reference (rail spec §2e) and does not govern. H4 does not change it.

**Different wording, not amended here:** the rail spec's `W` row degrades a snapshot "older than" one bar (`:26`, strict), and `AMEND` requires a target `W` "within one bar" (`:47`). Ruling 6(b) is a fence-classification contract. Whether those rows follow its boundary is returned as Q1 (§5).

## 4. Fence trace items (FT §1–§3, §6)

States: (i) known working with fresh evidence; (ii) evidence stale; (iii) unknown dispatch; (iv) terminal. "H4 (F)" means the synthetic repair checkpoint; its node IDs are in the [H4 card](../briefs/handoffs/2026-09-27-h4-fence-classification-orb-l1-repair.md).

### 4.1 Spec reading and classification

| FT item | FT verdict | Status after Ruling 6 | Resolving words, or owner |
|---|---|---|---|
| §2 spec reading of (i) (`FT:33-52`) | OPEN | **RESOLVED by (b1)**: known working, not `UNKNOWN`; the reservation is retained | Rail spec `pending` row marker (this H3) |
| §6.1 proposed `pending` clarification (`FT:168-170`) | Proposal | **Superseded by the ruling's own words.** The marker quotes (b1)–(b5) in quotation marks and labels each reading it adds as a reading, with its source (FT §4 `FT:146` for "qualifying"; FT §6.2(iii) `FT:178` for the conservative terminal-resolution rule). It does **not** adopt FT's sentence "the one-bar outcome timeout runs from the latest such evidence"; it states (b2) instead | Rail spec marker |
| §1 boundary: code inclusive, kernel strict (`FT:31`) | Minor; pin it | **RESOLVED by (b2)**: stale at one bar, pinned (§3) | H4 (F) case 11 |
| §1 never-sent request classified (iii) on the no-route path (`book_account_owner.py:1682-1684`; `FT:30`) | Fails closed; T09 must not inherit it | **STILL OPEN** | T09 outcome classifier / never-dispatched journal (FT §6.2, §6.7). Not ordered by Ruling 6 |
| §6.2 (iii) positive lookup (iii)→(i) (UB-7, EVIDENCE-PENDING; Gate A A1/A3) | OPEN | **STILL HELD**: (b3) "positive-lookup resolution remains separately held" | Incident ADR UB-7; T09 |
| B–D packet §3 table (iii): the spec waits for the one-bar timeout, the code blocks at once | Timing question | **RESOLVED by (b3)**: "blocks immediately", which matches the code (`book_account_owner.py:793`) | Rail spec marker |
| B–D packet §3 table (iv): a rejection is terminal only where Gate A A3 admits it | Owed to T09 | **STILL OPEN** for a real route. (b4) is consistent with the code's identity-matched resolution (`:795`) | T09 outcome classifier. The `REJECTED` shortcut (`:791-792`) stays synthetic-seam only |

### 4.2 Consumers (FT §3 matrix)

| Consumer × state | FT verdict | Status after Ruling 6 | Resolving words, or owner |
|---|---|---|---|
| **Admission (i)** (`:1608`) | Spec-ambiguous; defect under the proposed reading | **RESOLVED (spec) by (b1).** Code defect confirmed | H4 (F) cases 1, 5 |
| **Admission (ii)** | Correct. Clearing on fresh evidence spec-ambiguous; impossible in code | **Blocking RESOLVED by (b2).** Reclassification to (i) on fresh qualifying evidence follows from (b1). After an incident halt, (b5) bounds permission, not classification | H4 (F) cases 2 (classification only), 9 (permission). Whether staleness is itself a rev9 halt is Q2 (§5) |
| **Admission (iii)** | Classification correct; no halt (CC-3) | **Classification RESOLVED (retained) by (b3).** Halt **STILL OPEN** (retained by the ruling) | T09/TB-I3 (packet CC-3) |
| **Admission (iv)** | Correct | **Confirmed by (b4)** | H4 (F) case 7 re-pins it |
| **Loosening amend (i)** (`book_protection_owner.py:492`) | Spec-ambiguous; defect under the proposed reading | **RESOLVED by (b1).** A loosening amend is risk-adding (rail spec `:39`), so it is an admission under I1/I6. Code defect confirmed | H4 (F) case 1 |
| **Loosening amend (ii), (iv)** | Correct | Unchanged | — |
| **Loosening (iii); tightening/attach under (iii)** | Loosening correct; tightening follows from the missing halt | **STILL OPEN** (halt) | T09/TB-I3 (CC-3) |
| **Close, same leg, (i)–(iii)** (`:1296-1301`) | Spec-ambiguous; not a fence question | **STILL OPEN** | Rail spec: S5/matrix vs K1/S10/§5 (FT §6.7) |
| **Close, other legs; (iv)** | Correct | Unchanged | — |
| **Cancel (i), (ii), (iv)** | Correct | Unchanged | — |
| **Cancel (iii)** | Correct under S4; rev9 follows from the halt | **STILL OPEN** (halt) | T09/TB-I3 (CC-3) |
| **Recovery / deadline, all states** (`:1789-1797`) | Correct. For (iv), the owner decides from its own accounting; the producer is T09 | Unchanged. The producer is **STILL OPEN** | T09. H4 (F) case 10 re-pins it |
| **Resume gate, all states** | Correct (fails closed); not built | **Confirmed by (b5)**; no resume path is added | H4 (F) case 9. The production resume implementation stays owed (halt/resume §4) |
| **Takeover (i), displaced leg** | Correct | Unchanged | H4 (F) case 8 re-pins it |
| **Takeover (i), non-displaced, within the first bar** (`book_takeover_owner.py:621-622`) | **Defect under either reading** | **Defect stands** (S10 `:72`, K1 `:112`); not contingent on Ruling 6 | H4 (F) case 8 |
| **Takeover (i), non-displaced, after one bar** (`:558-559`, `:621-622`) | Spec-ambiguous; defect under the proposed reading | **RESOLVED by (b1)**: an unrelated leg's known working order does not block Aegis's admission. Code defect confirmed | H4 (F) case 8 |
| **Takeover (ii), (iii), (iv)** | Correct | Unchanged; (b2), (b3) | H4 (F) case 8 |
| **Capacity, all states** | Correct | **Confirmed by (b1)**: "Retain its capacity reservation" | H4 (F) case 1 asserts the reservation |
| **Close orders (3.8): admission and takeover** | Correct | Unchanged | — |
| **Close orders (3.8): cross-leg loosening during an accepted, unresolved close** | Spec-ambiguous | **STILL OPEN** | Rail spec, CLOSE bullet (FT §6.7) |

### 4.3 FT §6 repair specification

| FT item | Status after Ruling 6 | Note |
|---|---|---|
| §6.2 classification (i)–(iv), never-dispatched | (i) RESOLVED by (b1), with the (b2) boundary replacing "at most one bar old". (ii) RESOLVED by (b2). (iii) retained by (b3). (iv) (b4); the `REJECTED` rederivation stays T09's. Never-dispatched: **OPEN**, owned by T09 | H4 implements (i)–(iv) on the synthetic seam only |
| §6.3 consumers after the repair | Adopted as the H4 scope: admission, loosening amends and the takeover fence count (ii) and (iii) only. Takeover quiescence counts unresolved requests and displaced-leg non-terminal orders. Close, cancel, cutoff, flatten, deadline and capacity are unchanged | The boundary sentence (`FT:186`) is replaced by §3 |
| §6.4 cases 1–12 | Adopted as H4 (F)'s test set, worded to (b1)–(b5) | Case 11 follows §3. Case 6 includes a positive lookup of the same order among the evidence that must **not** clear (iii), under (b3) |
| §6.5 freeze-inventory effect | Stands | `trust_domain.py:146` binds `book_account_owner` as `listener_account_owner`; `:158-164` list the runtime dependencies, including `book_protection_owner` and `book_takeover_owner` |
| §6.6 dependence on the lifecycle ruling | **Discharged by 6(a).** Under L1, state (i) must be sustained from range completion to the earlier of the cutoff and the port's session-end cancel. Case 1 with a multi-bar ORB entry is representative | The refresh cadence and polling load (Gate A A7) are **STILL OPEN**, owned by T09 |
| §6.7 rev9 halt for ordinary unknowns | **STILL OPEN**, retained by the ruling | TB-I3/T09 (packet CC-3) |
| §6.7 T09 outcome classifier (Gate A A3; `REJECTED` shortcut; never-dispatched journal) | **STILL OPEN** | T09 |
| §6.7 same-leg close refusal | **STILL OPEN** | Rail spec |
| §6.7 cross-leg loosening during an unresolved close | **STILL OPEN** | Rail spec, CLOSE bullet |
| §6.7 AC-3 vs S1 | **STILL OPEN** | Rail spec |

## 5. Questions returned (Ruling 6 does not decide them)

- **Q1: the boundary in other rows** (rail-spec owner). Ruling 6(b2) pins staleness at one bar for fence classification. Three passages word the one-bar window differently: the `W` row (`:26`) degrades a snapshot only when it is "older than" one bar; `AMEND` requires a target `W` "within one bar" (`:47`); and the §1 evidence-currency paragraph (`:41`) says "the one-bar freshness window is an upper bound on age", which, read inclusively, would keep an exactly-one-bar read fresh. The amended `pending` marker (1) reads "qualifying" against that paragraph and states that for fence classification the boundary in (2) governs. Do the other rows adopt the same boundary, or keep their wording for their own consumers? H3 does not amend them. H4 changes no `W`/`AMEND` behavior.
- **Q2: stale evidence as a block or a halt** (halt/resume owner). Ruling 6(b2) says stale evidence "blocks further admission". Halt/resume §2 row 1 (`docs/spec/2026-09-14-tb-s3-halt-resume-contract.md:26`) halts on "loss of required broker/account evidence". Is a known working entry whose evidence goes stale a block only, or also that halt? If it is a halt, (b5) means that fresh evidence never restores (i) automatically.
  - **H4 implements the block only**, which is the ruling's word, and adds no halt.
  - The answer bears on T09 and TB-I3.
  - A concurrent, unaccepted H5 amendment to the halt/resume contract records the same question as its O-1 (working-tree §4.1, "O-1. Stale order-level evidence"). One answer should serve both.
- **Q3: how narrowly the replay correction is scoped** (coordinator). The ruling says the one-bar cancel "does not end ORB's base entry". It says nothing about the replay's one-bar cancel for other resting entries or adds (none among the accepted ports, `LC:36`).
  - **The H4 card's default:** exempt ORB's base entry only, and keep RC-9's one-bar cancel for any other resting entry or add, since that is what RC-9 as amended says.
  - **Stop:** H4 stops and returns if the exemption cannot be expressed inside `replay.py` without touching another file.
  - The coordinator may instead direct a broader removal. That would need its own RC-9 wording.

- **Q4: change control for the relaxation** (rail-spec owner; coordinator). **RESOLVED 2026-09-27 by the operator** (§59 Ruling 6, operator answers): a dated §5 addendum entry is added to the rail spec. The original question follows. The rail spec's Boundary line (`:187`) reads "no B1 field change or fail-closed change without the §5 addendum". The `pending` marker, and H4's admission change, relax a fail-closed default: a known working request is no longer blocked as `UNKNOWN` after the one-bar timeout. The amendment rests on the operator's words in Ruling 6: "Authorize the bounded synthetic repair and corresponding specification/replay corrections". The §5 (S2b) addendum text (`:169`) addresses B1 fields, daemon source health and INTERVENTION fencing; the amendment changes none of those. Whether the Boundary line's "fail-closed change" nevertheless requires a §5 addendum entry is not settled by the source. Returned rather than assumed; H3 made no §5 entry.

**Also returned (definitional, not blocking H4):**
- **"Unrelated admission" in (b1).** The H4 cases use other-leg admissions, which are plainly unrelated. A same-leg risk-add while that leg's own request is known working is not addressed by the ruling. H4 adds and removes no same-leg rule, so the daemon's `BookLegExecution.admit` refusal of a second entry on a non-empty leg and the capacity rules keep governing.
- **The `pending` row's non-event resolution path** ("a postdating `W` snapshot showing the order absent together with a postdating `P` consistent with no fill", `:27`) versus (b3)'s terminal-only rule for genuinely unknown dispatches "for this slice". The marker records the slice rule and leaves the path's text in place. Whether the path survives for the real route is T09's (Gate A A1: absence proves nothing on this route; `FT:64`).

## 6. Verification of this note

Commands actually run, read-only:
- `git show 8c15f18:docs/notes/2026-09-26-orb-lifecycle-evidence.md`, `git show 8c15f18:docs/notes/2026-09-26-account-fence-four-state-trace.md` and `git show 8c15f18:docs/briefs/handoffs/2026-09-26-orb-lifecycle-and-fence-trace.md` (read in full).
- `git merge-base --is-ancestor 62c956f HEAD`: exit 1 (not an ancestor). `git diff --stat 62c956f HEAD -- <files>`: empty for:
  - the owner code: `book_account_owner.py`, `book_protection_owner.py`, `book_takeover_owner.py`, `book_capacity.py`, `qualification/replay.py`, `qualification/trust_domain.py`;
  - the tests: `tests/ops/qualification/test_replay.py`, `tests/ops/test_book_feedback_journal.py`, `tests/ops/test_pr409_review4.py`, `tests/ops/tb_s3_kernel/kernel.py`;
  - the specifications: rail, replay and halt/resume specs, and the edition pre-registration.
- `sed -n` / `grep -n` spot-checks at HEAD:
  - `book_account_owner.py:768-798`, `:1296-1301`, `:1573-1584`, `:1608-1612`, `:1665-1705`, `:1760-1798`;
  - `book_protection_owner.py:488-496`;
  - `book_takeover_owner.py:539-559`, `:615-623`;
  - `replay.py:349`, `:407`, `:499`, `:508-509`, `:543`;
  - `trust_domain.py:142`, `:146`, `:158-164`;
  - `test_replay.py:214-223`, `test_book_feedback_journal.py:41-69`, `test_pr409_review4.py:52-126`, `kernel.py:1319-1329`, `book_protocol.py:39`.

  Each matched the #519 citation.
- Rail spec `:26-27`, `:39-54`, `:56-60`, `:76-97`, `:186-213`; replay spec `:1-10`, `:23`, `:45-47`, `:68`; halt/resume `:20-36`, `:41-45`, `:55-67`; campaign record `:3985-4010`; B–D packet §3 and §5; checklist addendum §0–§5.
- `python3 scripts/check_handoff_authority.py --all`: at the fix round `2 card(s) with an authority block, 0 violation(s)`, exit 0 (the H4 card and another handoff's concurrently written card). The authoring-time run's output was reported only in the H3 return and is not restated here.
- Relative-link and anchor check of the five H3 files (a scratchpad script resolving each relative link and `#anchor` from the file's own directory): `bad 0`, exit 0. `python3 scripts/check_md_relative_links.py` (repository-wide, warn-only): none of its unresolved links is in the five H3 files.
- `python3 scripts/check_path_liveness.py`: `OK`, exit 0. It does not cover `docs/**`, so it is recorded only because it was run.
- At the fix round HEAD had moved to `c991d2d`. `git log 521d8f2..HEAD` shows one commit, and `git diff --stat 521d8f2 HEAD -- ops tests docs/spec docs/briefs/pre-registration docs/briefs/programs` is empty, so the `521d8f2` anchors hold.

**Not run:** no tests and no gate suite, per the H3 limits and the dispatch instruction.

**Not read:** no private source.

**UNVERIFIED:**
- Whether `replay.py` can express the ORB-base-entry exemption without a change outside it (Q3). The H4 worker establishes this.
- Broker day-order expiry on the route.

**Not granted:** freeze, edition file production (gate D), replay or E1 dispatch, a count run of the private port, gate B–D acceptance, T09 dispatch, H4 dispatch, deployment, arming or GO. The fence obligation is not resolved by this note, by the owner text or by H4's synthetic half.

## Review and fix round (2026-09-27)

Two review passes returned findings with overlapping ids; they are labelled **A-** (first pass) and **B-** (second pass). Each was re-verified against its cited source before it was applied.

| Finding | Outcome | Why, and what changed |
|---|---|---|
| A-F1 marker "quotes" (b1)–(b5) but paraphrases and adds glosses | **Applied** | Verified: the marker had no quotation marks, and its "qualifying" and terminal-only clauses come from FT §4 (`FT:146`) and FT §6.2(iii) (`FT:178`). The rail-spec `pending` marker now quotes each ruling bullet in quotation marks and labels each added reading with its source. §4.1's row says so |
| A-F2 "demonstrably" dropped | **Applied** | Verified against Ruling 6(b). Restored in the rail-spec header callout and the Change history entry |
| A-F3 session-end cancel attributed to "this contract" | **Applied** | Verified: S4 at `521d8f2` (`:60`) names no session-end cancel. S2 and RC-9 markers now give a non-exhaustive example list; the S2, S4 and RC-9 markers cite `LC:23` and allocation map C08 (`:95`) |
| A-F4 day-order expiry owner invented | **Applied** | Verified: only C08 (`:95`) and `LC:97` mention it; neither names an owner. §2 row now reads "Owner UNVERIFIED; proposed: route commissioning (H2)", returned to the coordinator |
| A-F5 citation drifts in the H4 card | **Applied** | Verified: `:1760` is the retired-action update and the cutoff loop starts at `:1768`; trace §7 does not list `test_book_takeover_phases.py`; `test_book_feedback_journal.py:41` is blank. The card now cites `:1768-1797`, labels the suite additions as H3's, and uses `:42-55` (noting the H3 card's `:41-55`). This note's §3 uses `:42-55` too |
| A-F6 halt/resume anchor shift undisclosed | **Applied, with corrected offsets** | The concurrent amendment's hunks are `@@ -2,0 +3,6 @@` and `@@ -63 +69,35 @@`, so §2 row 1 moves `:26`→`:32` but the §5 rule moves `:67`→`:107`, not +6. The anchor paragraph records both |
| A-F7 RC-9 duplicate-key owner misstated in the H3 return | **Applied (return only)** | Verified: `LC:100` cites the replay spec and this note's §2 names the replay spec. The note is unchanged; the corrected owner is carried in this fix round's return |
| B-F1 case-2 node pins open Q2 | **Applied** | Verified: "while RUNNING only" assumes staleness is not a halt (Q2) and conflicts with case 9. The node is renamed `test_fresh_working_evidence_after_staleness_reclassifies_known_working` in the authority block and §2, and asserts classification only. §4.2's admission (ii) row is reworded to match |
| B-F2 untraced consumers; shared-helper risk | **Applied** | Verified by `grep -rn` over `ops/`: `book_account_owner.py:757`, `:810` and `book_takeover_owner.py:55`, `:547` are consumers the trace does not cite. The card lists them as unchanged, directs a new predicate at `:621`, and rewords the first stop |
| B-F3 "applicable cancellation" treated as a closed set | **Applied** (with A-F3) | Ruling 6(a) does not define the term. The markers now say so and add incident handling (`LC:59`, `:68`). Mode handling was not added: `LC:23` says the port's PROTECTED-mode switch never cancels the base entry |
| B-F4 Q1 misses the evidence-currency sentence | **Applied** | Verified at HEAD `:41`. Q1 now includes it, and marker (1) states that for fence classification the boundary in (2) governs |
| B-F5 Boundary line's "fail-closed change without the §5 addendum" not addressed | **Applied as a returned question (Q4)** | The source does not settle whether that Boundary clause reaches this relaxation, so it is returned, not assumed. H4 §4 carries Q4 |
| B-F6 "first-bar refusal" misnamed; "re-pinned" without nodes | **Applied** | Verified: `_unresolved_attempt_rows` (`:760-766`) counts `reserved`/`attempted` at any age. Case 8 now names the account-wide quiescence refusal. §1 now says only cutoff and deadline are re-pinned (case 10); the rest are covered by §6's related suites |
| B-F7 checker results deferred to the return | **Applied** | §6 above and the card's verification section record the commands and outputs |

Rejected: none. Nothing in this round changes a ruling's words, a Status line, an OWED row or the H4 authority block's shape beyond the one node rename.

---

## Coordinator acceptance (2026-09-27)

**ACCEPTED**, together with H3's owner text: the rail spec, replay spec and edition pre-registration amendments. The [H4 card](../briefs/handoffs/2026-09-27-h4-fence-classification-orb-l1-repair.md) is accepted separately in its own file.

- **Reviewer:** the coordinating session.
- **Artifact:** the executor draft plus the fix round, which applied all 14 findings of two refute-first reviews.
- **Read:** the rail-spec diff in full; the replay-spec and pre-registration diffs; §1–§5 of this note.

**Operator answers applied (2026-09-27, §59 Ruling 6, operator answers):**
- **Q4 (critic X-04): resolved.** The dated §5 addendum entry is added.
- **The one-bar boundary (critic X-11): confirmed inclusive.** Age at evaluation ≥ one bar period is stale. §3's reading now stands as the operator's.

**Coordinator dispositions:**
- **Q3 (replay correction scope):** the default is accepted. Only ORB's base entry is exempt; RC-9's one-bar cancel stays for any other resting entry or add.
- **Day-order expiry (critic X-12):** owner assigned (§2 row).
- **Q1 (other rows' one-bar wording) and Q2 (stale as a block or a halt):** these stay OPEN with the rail-spec owner and TB-I3. H4 implements the block only.

**Not granted:** freeze, edition file production, replay or E1 dispatch, T09 dispatch, deployment or GO.
