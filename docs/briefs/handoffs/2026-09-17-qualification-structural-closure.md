# Qualification structural closure — implementation handoff

Implement the [nine-task plan](../../superpowers/plans/2026-09-17-qualification-structural-closure.md) against its [design](../../superpowers/specs/2026-09-17-qualification-structural-closure-design.md). Read both completely, plus the linked N1 boundary and Linux environment documents. The new design's explicit amendments take precedence over the earlier proposals. The [assessment](../../notes/audits/2026-09-17-pr415-structural-assessment.md) explains the recurring failure families.

**Starting state:** Last inspected PR415 head was `bfad2f187e05980369dbf0e8f75801f621ba998d`; acceptance remains held. This task produced documents, not implementation. The design/plan are uncommitted in the main checkout and must be carried into the implementation worktree. Refresh PR/main and inspect existing prototypes before choosing the base; preserve all unrelated changes and worktrees. Use an isolated `codex/` branch and the executing-plans workflow. The next implementation instruction governs authorization; planning-only banners record the earlier drafting scope.

**Sequence:**

1. Tasks 1–2: canonical product/stage/artifact policy and real retained-source legality checks.
2. Tasks 3–4: role-specific evidence reconstruction and acyclic logical journal snapshots.
3. Tasks 5–7: signed v2 admission, protected N1 execution/capture, G5 verification and atomic commit.
4. Task 8: real interruption, restart, retry and VOID/concurrency conformance.
5. Task 9: invariant coverage gate, targeted mutation checks and independent integration review.

One coordinator owns combined acceptance. Start with Task 1; track completion in the plan. Preserve existing replay, RNG, exact statistical decisions and risk policy. Re-read canonical production code before touching risk-related semantics. Shared policy/configuration must have one owner.

**Critical contracts:** LEGALITY requires the actual registry check and source admission. Matching hashes do not prove execution. G5 artifacts must represent the captured observations it adjudicates. Commit compares the logical precommit snapshot under the writer lock. Exact retries return the original receipt with current validity/eligibility—even after expiry or VOID—without issuing new authority or signatures. Changed authentication conflicts. Retire active v1 bypasses at v2 cutover.

**Verification:** Run the selected checkout's `./fp.ps1 doctor` before Python; use its launcher for all checks. Follow each task's rejection/positive tests and require real Linux UID/process/container evidence for isolation. Missing infrastructure blocks that milestone, not independent library work. Report revision, interpreter, commands, actual results, recorder validity and unresolved limitations.

**Acceptance ceiling:** First protected release is synthetic N1_ONLY: terminal FAIL or PARTIAL/CONTINUE, never full E1 PASS/seal or OPERATOR execution. Full-campaign execution, production keys, qualification, provisioning spend, deployment and merge are not implied by this handoff.
