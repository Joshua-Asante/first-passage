# ORB resting-entry lifecycle evidence and the four-state account-fence trace — bounded handoff

**Status:** DISPATCHED 2026-09-26 by the coordinating session (Claude Code, Opus 5.5) on the operator's instruction "start the close semantics, S5 measurement and ORB trace handoffs". **Dispatch revision:** the commit that adds this card; the executor verifies its `HEAD` descends from it. **Executor:** one assessor subagent in its own worktree. **Coordinator** accepts or corrects the return.

**Authority (operator ruling 2026-09-26, §4):** "Resolve ORB's one-bar versus session-end cancellation from source and replay before requesting the lifecycle ruling. Keep that decision separate from the four-state account-fence correctness trace." The packet treats the fence as a **required correctness repair**, not a policy choice. Neither lifecycle may be chosen merely to make the fence stop blocking.

This card has **two separate deliverables**. Each has its own result file and must not rely on the other's conclusion.

## Deliverable 1 — ORB lifecycle evidence (for the operator's lifecycle ruling)

**Question:** when does the accepted ORB definition cancel or re-issue its resting stop entry, and how do the replay and the rail spec treat it?

**Sources:**
- **The accepted ORB Pine and runtime port.** Read them in place in the primary checkout (`C:\Users\joshu\multi_firm_operations`) under [campaign §60](../programs/2026-09-03-seven-strategy-select-campaign-state.md#60--agent-read-access-to-the-accepted-books-pine-and-runtime-ports-2026-09-25). First check each SHA-256 against `core/strategies/BOOK_SOURCES.sha256`. Never copy them, quote bodies or values, or send them anywhere; state findings as behavior.
- The ORB edition pre-registration (ORB rows) and packet B-13.
- The replay spec's RC-9, the qualification replay (`ops/c1_rail/qualification/replay.py`) and `ops/c1_signal_daemon/tv_broker_emulator.py`.
- Rail spec S2 and the `pending` row; allocation map C08.
- The Phase 1 / TradingView export parity record, where it states resting-entry behavior.

**Deliverable:** `docs/notes/2026-09-26-orb-lifecycle-evidence.md`. It contains:
1. A table with one row per source: Pine, port, emulator, qualification replay, rail spec S2, RC-9. Each row gives the cancel and re-issue behavior, where it is stated (`file:line` for public files; behavior only for private ones) and which environment it governs.
2. The exact conflict or conflicts.
3. For each candidate lifecycle, its consequence for strategy behavior, for replay and export parity, for how long capacity stays reserved, and for the ORB edition pre-registration.
4. The questions the operator's ruling must answer.

No recommendation may turn on the fence.

## Deliverable 2 — four-state account-fence correctness trace

**Question:** does the account fence classify each order state correctly, from source to every consumer? The four states are:
1. a known working order with fresh evidence;
2. an order whose evidence has become stale;
3. a genuinely unknown dispatch outcome;
4. a terminal order.

**Sources:**
- `ops/c1_rail/book_account_owner.py`: `_ordinary_unknown_orders_db` (:768–798), admission (:1590–1622), close and `close_unreconciled` paths, attempt journal (:1665–1705).
- `ops/c1_rail/book_protection_owner.py` (:492 and the evidence rows).
- `ops/c1_rail/book_capacity.py` (terminal acceptance).
- The rail spec's `pending` row, S1 cut, S2, AC-5 and E3; halt/resume §2–§4.
- The test reference kernel `tests/ops/tb_s3_kernel/kernel.py`: its `_sweep_timeouts` evidence-refresh model.
- The fence tests: `tests/ops/test_book_feedback_journal.py`, `tests/ops/test_book_close_reconciliation.py` and `tests/ops/tb_s3_cases/**`.

**Deliverable:** `docs/notes/2026-09-26-account-fence-four-state-trace.md`. It contains:
1. **A four-state × consumer matrix.** The consumers are admission, protection amend, close, recovery and the resume gate. Each cell gives:
   - today's code behavior, with `file:line`;
   - the spec behavior, or OPEN where the spec is ambiguous, quoting the conflicting rows;
   - a verdict: correct, defect or spec-ambiguous.
2. **The evidence inputs each state depends on:** what counts as fresh order-level evidence, and who produces it. Mark producers that are not built yet (T09) as such.
3. **Test coverage per cell.**
4. **A proposed repair specification,** stated as behavior, not code. It covers:
   - the fault cases and tests it needs;
   - its effect on the E1 freeze inventory (the account owner is a qualification-bound module);
   - any dependence on the Deliverable 1 lifecycle ruling, stated explicitly and not resolved.

You may run existing tests (`.\fp.ps1 python -m pytest <paths>`) to confirm current behavior, citing the record. **No code change.**

## Output rules

Write only the two result notes, plus an executor-return section appended to this card. No edits to code, contracts, pre-registrations or owners. No order or account action, no `.env`, no GLM or external service.

## Executor return (2026-09-26)

**Status:** DONE_WITH_CONCERNS. The concerns are listed under "Unverified and not measured". **Executor:** assessor subagent (Claude Code, Opus 5.5), worktree `.claude/worktrees/orb-fence-trace`, branch `claude/orb-fence-trace`. HEAD was `62c956f538dfa53f31eaec5951efc3ffa1dce53b` (the dispatch revision) before the result commit. **Nothing here accepts, authorizes, qualifies or releases anything.**

**Files written:** [`docs/notes/2026-09-26-orb-lifecycle-evidence.md`](../../notes/2026-09-26-orb-lifecycle-evidence.md) (Deliverable 1), [`docs/notes/2026-09-26-account-fence-four-state-trace.md`](../../notes/2026-09-26-account-fence-four-state-trace.md) (Deliverable 2) and this section. No other file was changed.

**Deliverable 1 — ORB lifecycle (recommends no lifecycle):**
- **Strategy sources and parity basis: rest until session end.** The accepted Pine and port place one buy-stop entry per day, when the range completes. Neither cancels it by age or places it again; only the session-end bar cancels it. Both SHA-256 digests matched `BOOK_SOURCES.sha256`; the files were read in place and nothing was copied or quoted. The emulator and parity harness have no age-based cancel, and the 681-of-681 ORB export parity rests on that lifecycle.
- **Qualification replay and its specs: one bar.** The replay cancels any resting entry one bar after admission (`replay.py:507-509`, RC-9). The port never re-issues, so qualification gives ORB's entry exactly one bar to fill.
- **Rail contract: conflicted.** S2 adopts the one-bar cancel, while AC-8, S4 and the §5 cutoff assume long-resting entries. No live-path code cancels by age. AC-3's resting add does not match the port's market add; it is recorded as a separate inconsistency, not as support for either lifecycle.
- **Candidates and questions.** Three candidate lifecycles (L1 rest until session end, L2 one bar, L3 one bar re-issued) are compared on strategy behavior, replay and export parity, reservation time and the ORB pre-registration. §4 of the note lists the questions the ruling must answer.

**Deliverable 2 — four-state fence trace:**
- **(i) and (ii) are indistinguishable to the fence.** Its only resolving input is an accepted terminal; the owner has no working-order evidence input for entries. So a known working order with fresh evidence is fenced like a stale one after one bar, for admission, loosening amends and takeover.
- **The spec reading of (i) is OPEN.** The `pending` row (rail spec `:27`) and the consistency matrix (`:78`) read (i) as unknown after one bar; the S1 cut (`:54`), the `W` row (`:26`), E3 (`:111`) and other rows read it as not unknown. §2 and §6.1 of the note propose a clarification for the rail-spec owner. It is proposed, not settled, and the state-(i) defect verdicts hold only under it.
- **Takeover also over-blocks** on any non-terminal order anywhere, from the send onward (`book_takeover_owner.py:621`). During the order's first bar that is a defect under either reading (S10, K1, the `pending` row); after one bar it is a defect only under the proposed reading.
- **(iii) is fenced correctly, but the rev9 halt for ordinary unknowns is not implemented** (already recorded, packet CC-3).
- **(iv) resolves correctly,** apart from the transport-`REJECTED` shortcut, which Gate A A3 constrains for a real route.
- **The rest is correct or fail-closed.** Close, cancel, recovery, the resume gate and capacity do not read the fence and are correct or fail-closed, with two spec ambiguities: same-leg close refusal, and loosening during an accepted, unresolved close.
- **The producer of fresh order-level evidence is T09, which is not built.**
- **Repair.** A behavior-level repair specification is given, with its fault cases and tests. It changes the E1 freeze inventory, so it should land before the freeze. It is required under every lifecycle; its dependence on the lifecycle ruling is stated and not resolved.

**Verification:**
- **Existing tests only, no code change:** 139 passed (record `.cache/fp-verification/20260926T232158Z-591119cf168f/record.json`) and 170 passed (record `.cache/fp-verification/20260926T232629Z-44105170d04d/record.json`), both at `62c956f`, `status: completed`, exit 0, `source_stable: true`.
- **Gates:** `.\fp.ps1 check` was run on the final tree before the result commit. Its record path and result are in the commit message and the coordinator return.

**Unverified and not measured:**
- **The state-(i) defect is shown by code reading, not by a failing test.** The card allows running existing tests only, and no production test supplies working evidence.
- **The size of the one-bar behavior change was not measured.** It is the number of ORB entries that fill later than the first bar after placement, and measuring it needs an authorized run of the private port.
- **Broker day-order expiry on the route is unverified** (C08).

**Return for the coordinator (not written into any owner record):**
- **Spec owners:** the proposed rail-spec `pending` clarification; the RC-4/RC-9, S2 and AC-8 inconsistencies; AC-3's resting add versus the port's market add and S1; RC-9's `bar_time` versus the replay's `path_time` duplicate key.
- **T09:** the never-dispatched attempt journal (`book_account_owner.py:1682-1684` leaves a never-sent request `UNKNOWN`).

**Fix pass (2026-09-26, coordinator review findings; executor-return section only):** six minor findings applied to both notes. State-(i) Spec cells now read OPEN with the conflicting rows named, and the reading is labeled a proposal. The takeover (i) non-displaced verdict is split at the first bar. AC-3 is no longer cited as support for a multi-bar lifecycle. The §6.1 kernel claim is narrowed to the no-timeout precondition. Line citations were corrected at `62c956f`: `test_pr409_review4.py`, `trust_domain.py:142`, and runtime dependencies `:158-164`. No code change and no new test. The fix commit message records the `.\fp.ps1 check` record path and result.

**Coordinator review (2026-09-26): ACCEPTED AS INPUT.** Reviewer: the coordinating session. Artifacts: `8fc0c63` and the fix round `6f76e1c`. Refute-first reviews found no separation or authority defects and six citation defects, all fixed. The coordinator spot-checked `replay.py:507-509` (the one-bar cancel), `book_account_owner.py:791-797` (accepted-without-terminal is fenced after one bar) and `book_takeover_owner.py:621` (takeover refuses on any unresolved attempt).

**Deliverable 1:** the Pine, port, emulator and export parity keep the entry until the session ends. The qualification replay (RC-9) and rail S2 cancel it after one bar. It lists five conflicts and three candidate lifecycles, with no recommendation. It goes to the operator for the lifecycle ruling. *Pointer 2026-09-26: the operator ruled L1 in session ([campaign §59 Ruling 6](../programs/2026-09-03-seven-strategy-select-campaign-state.md#ruling-6--orb-resting-entry-lifecycle-l1-2026-09-26)): one placement, no age-based expiry or periodic re-issue, with the earlier scheduled cutoff kept. Amendments to ORB-1, RC-9, rail S2 and the qualification replay are to be prepared and returned for acceptance before edition freeze. The Deliverable 2 fence repair stays separate.*

**Deliverable 2:**
- A known working order with fresh evidence is fenced like a stale one. That is a defect under the proposed spec reading, and the spec's reading of this state is itself OPEN.
- Takeover over-blocks on non-displaced legs.
- An unknown dispatch is fenced but raises no halt; that gap is already in the packet (CC-3).
- The repair is specified as behavior. It changes the E1 freeze inventory, so it should land before the freeze. It is needed under every lifecycle.

The spec clarification is for the rail-spec owner and is not applied.
