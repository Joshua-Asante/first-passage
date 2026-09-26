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
