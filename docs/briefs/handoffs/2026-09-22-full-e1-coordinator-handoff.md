# Coordinator handoff — Protected Full E1 after S3 (S4 in flight), 2026-09-22

**Type:** coordinator handoff (session boundary; the successor coordinator continues the Full E1 roadmap)
**From:** coordinator session of 2026-09-21/22 (Claude). **To:** the next coordinator session. **Operator:** Joshua.
**Authority:** this handoff routes work; it grants nothing. Rulings, acceptance and merges stay with the coordinator and operator as the execution-slices plan assigns them. Per the [handoffs README](README.md) routing rule, this is the latest specifically assigned coordinator handoff.

## 0. Read first (in this order)
1. [Execution-slices ledger](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md) — every entry from "Coordinator checkpoint C1 — S3 interface freeze ACCEPTED" to the end, especially **"Coordinator acceptance — S3 …, 2026-09-22"** and **"T05 follow-up …"**.
2. [S4 packet](2026-09-21-full-e1-s4-joint-n2-part-b-DRAFT.md) — FROZEN despite the filename; §0 anchors pinned at `a8a983e`, ten binding lessons, four ruled decisions (S4-D1..D4).
3. [T05 packet](2026-09-21-full-e1-t05-result-and-seal.md) §7 (C-R, S7, the integration carry-forward) and the [S5 packet](2026-09-21-full-e1-s5-part-a-DRAFT.md) (drafted, three decisions ruled; freezes on S4's merge).
4. The amended [deployment checklist](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md) and its [2026-09-21 amendment](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md) (ratified by PR #448; §4 decisions adopted by PR #454).

## 1. State at handoff
| Item | State |
|---|---|
| `main` | `e50aa38` — PR #455 merged (S3). `e50aa38` = `a8a983e` (S3 code) + `docs/SESSIONS.md` only. |
| S1, S2, S3 (T01, T02) | **ACCEPTED and merged.** S3 evidence: three clean 19-node Linux runs (35781007681, 35781002126 on `a8a983e`; 35786085417 on the merge candidate `3b37f6e`), Windows lines 1–3 + `check` on `a8a983e`. |
| S4 (T03) | **In flight** — a GLM session, dispatched 2026-09-22 off `a8a983e`; worktree `C:\Users\joshu\mfo-s4-wt`, branch `claude/s4-joint-n2` (not yet pushed at handoff). Allowed so far: Phase 0, tests-first, C2 freeze, Windows, Linux `DIAGNOSTIC_SUBSET`. |
| T05 (S6–S7) | **Build complete, frozen** at `claude/t05-result-seal@c3cea75` (C-R accepted; S7 accepted as a build; settlement-rule follow-up accepted). Integration + acceptance after T04 (S5). |
| S5 (T04) | Packet drafted, decisions ruled; freezes on S4's merge (re-pin anchors at the S4 merge head). |
| T10 (external) | Phase 1 done on `claude/t10-source-freeze` (rulings R1/R2/R5 recorded; hold item (i) closed pending the operator's F1 confirmation). Step 4 and phase 2 undispatched. |
| T07, T08 (external) | Packets on `main`; undispatched. T08 step 1 (R3 go/no-go) needs a browser — not a `glm_agent` task. |
| PR #449 | **Open** — carries every packet and ledger entry since the S2 merge (docs only). Merge it early; the S4 session reads its packets from that branch until then. |

## 2. Immediate actions for the successor (in order)
1. **Release S4's gate.** Relay to the S4 session: *"#455 merged at `e50aa38` (= `a8a983e` + `docs/SESSIONS.md`). Rebase `claude/s4-joint-n2` onto `origin/main`; the rebase is mechanical and the §0 anchors are unchanged — re-verify them with one `grep -n` pass and record the result in §7. Acceptance-grade Linux runs are now allowed, after checkpoint C2 is ruled."*
2. **Rule checkpoint C2** when S4 returns it (packet §5): the widened layout at DB v9, the `/v7` snapshot diff, the checkpoint-keyed field sets, `run_n2_compute`'s exact request, the continuation-policy delta and fingerprint, the predecessor binding, the E-case ownership. Read the diff, not the summary; compare every commit message against its diff (two S3 commits claimed changes they lacked).
3. **Accept S4** only against the bar in §3; then re-pin and freeze the S5 packet at the S4 merge head and dispatch S5.
4. **After S5 is accepted:** integrate T05 (rebase onto the S5 merge head; apply the seam table — 19 rows at C-R + 2a/6a/11a/20/21 at S7; the two integration items in the ledger's "T05 follow-up" entry; the seal principal is a host-provisioning change, seam 11/11a), then T05's Linux acceptance, then T06 (S8).
5. **Merge PR #449** as soon as the operator agrees (docs only).

## 3. Acceptance bar for S4 (the S3 lessons, made checkable)
- [ ] Two clean acceptance-grade Linux runs on the **identical final head**: one dispatched and read with `python scripts/s2_run_evidence.py <run> --expect-head <sha>`, plus the PR's own S2-supervision run; if the branch is then updated from `main`, confirm the delta touches no tested/imported file, and read the PR's re-run on the merge candidate too.
- [ ] Every required node green (S2's fifteen + S3's four + the new N2 nodes); `cleanup_ok` true on **both** runs (a single green `cleanup_ok` was a coin flip in S3).
- [ ] The PR's own required checks green, including both `Qualification execution boundary` jobs (`--test-only` must require only nodes outside the S3/S4 file set) and Pylint ≥ 8.00 whole-repo.
- [ ] Windows lines 1–3 + `check` on the final head (line 3 is required whenever a store/service file changed).
- [ ] The committing N2_G5 work settles after T2: a post-commit overrun ends authority from `PART_A_READY`/`N2_FAILED` (extend `CHECKPOINT_PROGRESSION_STATES`), and the committing work completes in its own progression — with Windows reproductions (within-budget completes; overrun blocks) and a Linux assertion that the committing work reaches `COMPLETED`.
- [ ] The two asymmetric failure cases (FULL fails / halves pass; halves fail / FULL passes) — one batch, both decisions, no Part A work.
- [ ] One independent review at return (Codex on the PR); every finding verified against the code before ruling.

## 4. Coordinator toolkit (all read-only unless stated)
- Artifact read: `python scripts/s2_run_evidence.py <run-id> --dest <scratch> --expect-head <sha>` — exits 0 only if record/invariants/junit/cleanup hold. **A `DIAGNOSTIC_SUBSET` run always concludes "failure" by design — read its junit, not the badge.**
- Journal forensics: each artifact carries `boundary/journal.sqlite`; `full_campaign_budget_events` (event chain) and `full_campaign_objects` (supervision events; the `FAILURE` event's `reason` carries the worker's traceback tail).
- Dispatch: `gh workflow run qualification-s2-supervision.yml --ref <branch> -f mode=s3 [-f cases=<k-expr>]`. The PR run and a dispatch run are in different concurrency groups and can overlap; a push cancels the PR run on that ref.
- Windows: `./fp.ps1 [--workers 2] python -m pytest <paths>` from the checkout under test; cite the printed `record.json`; line 1 = the 16 execution files (see the S3 acceptance entry), line 2 = 4 files, line 3 = `tests/ops/qualification` + `tests/ops/test_phase3_provenance_acceptance.py`.
- Commits on Windows: `PATH=/c/Python314:$PATH`; `git diff --stat` before every commit; never bare `git stash`; if the state-currency gate fires, take `main`'s roll (merge `origin/main`), never a fresh one.
- `gh` fetch pitfall: a `git fetch` that names a non-existent ref aborts every ref in it — fetch refs separately.

## 5. Open operator items
- Merge PR #449 (packets + ledger).
- T10: confirm hold item (i) at F1 (Step 3 suffices for the corrected Striker port); decide when to dispatch step 4 (paragraph C of 2026-09-22) and phase 2.
- T08 step 1 (R3 unknown-request closure) — a browser read; decide executor.
- T07 — account-side operator inputs (S5 answer, original exports) before it can start.

## 6. Workspaces at handoff
| Path | Branch / head | Owner / disposition |
|---|---|---|
| `.claude/worktrees/pr-363-babysit-671b91` | `claude/s2-enforcement-gaps-fab5e6` → pushes to `claude/s2-merge-record` (PR #449) | coordinator docs worktree; keep until #449 merges |
| `.claude/worktrees/s3-finish` | `claude/s3-coordinator-finish` @ `a8a983e` | spent (S3 merged); safe to remove |
| `.claude/worktrees/t10-source-freeze` | `claude/t10-source-freeze` | T10 executor |
| `C:\Users\joshu\mfo-s3n1-wt` | `claude/s3-n1-genuine-capture` (merged) | spent GLM S3 worktree; its `.cache/fp-verification` holds S3 records — keep until the successor no longer needs them |
| `C:\Users\joshu\mfo-t05-wt` | `claude/t05-result-seal` @ `c3cea75` | T05 executor (idle until integration) |
| `C:\Users\joshu\mfo-s4-wt` | `claude/s4-joint-n2` | S4 executor (active) |
Never pass the main checkout (`C:\Users\joshu\multi_firm_operations`, has a `.env`) as a `glm_agent` workdir.
