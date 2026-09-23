# GLM handoff: make the S2 artifact read bind scope, nodes and bytes, and fail bad diagnostic inputs early (G1–G8)

**Type:** cc_handoff (frozen-spec implementation against a coordinator-authored acceptance suite)
**Date:** 2026-09-23
**Status:** FROZEN. **Queued behind [card 1](2026-09-23-guard-s2-runs-hardening.md).** Both cards edit `.claude/skills/s2-linux-run/SKILL.md`, and card 1 forbids workflow changes, so this card starts only after card 1's return is accepted. It shares no file with [card 2](2026-09-23-harness-guards-hardening.md), so it may run alongside card 2 in a second worktree.
**Executor:** GLM (Z Code), the single writer for the files in §2. **Coordinator:** Claude (wrote the acceptance suite; rules on the return). **Operator:** Joshua (the only one who merges).
**Base:** the accepted head of `glm/guard-s2-hardening`. Worker branch: **`glm/s2-evidence-tooling`**.
**Authority:** only the files in §2. `DONE` does not grant permission to merge.

## 0. Phase 0: read, then report before writing code (repository `Joshua-Asante/first-passage`)
Run the [`handoff-verify`](../../../.claude/skills/handoff-verify/SKILL.md) checklist. Report the anchors and the three facts listed below, then start editing. If anything contradicts the code, return `NEEDS_CONTEXT`.

**Workdir.** Use a fresh worktree, for example `C:\Users\joshu\mfo-evidence-wt`. **Never** use `C:\Users\joshu\multi_firm_operations`, which contains a `.env`.

**Test 0.** No vendor data, credentials or secrets are involved. The tests replace the reader's two gh seams and build synthetic artifacts.

**Why this card exists.** The S2 artifact read is the acceptance instrument that the coordinator handoff (`2026-09-22-full-e1-coordinator-handoff.md` §3–4) and the S3/S4/S5 packets rely on. `scripts/s2_run_evidence.py` exits 0 in three cases where it should not:
- a `mode=s2` run (15 nodes, scope `S2_DIAGNOSTIC_SUPERVISION`), even though the workflow names s3 as the acceptance-grade set;
- an `S3_N1_CAPTURE` artifact that lists a single required node;
- an artifact whose recorded `before.commit` differs from the head it is read against.

`--expect-head ""` skips the head check, and any one-character prefix passes it. The s2-linux-run skill's run lookup (`--branch <b> --limit 1`) can return the pull_request run on the same SHA instead of the dispatch you just started. Real run data shows the PR run is sometimes the newer of the two.

On the input side, a whitespace-only or malformed `cases` value is not caught until after the 6–8 minute provisioning step. `--host-only --cases x` runs the entire host suite and only then refuses. Each item was reproduced by an independent verifier (probe `scratchpad/r2c/verify-diag/probe_evidence.py`).

Reads:
1. `scripts/s2_run_evidence.py` (the whole file): `run_head`, `download`, `evaluate`, `main`.
2. `scripts/record_verification.py:40–52` (`snapshot()`: `before.commit` is the output of `git rev-parse HEAD`) and `:132–134`.
3. `scripts/qualification_boundary_verification.py:60–150`: `main`, the mode group, `--cases`, and the order of the prerequisite checks.
4. `.github/workflows/qualification-s2-supervision.yml`: the inputs, the `pull_request.paths` filter, the steps in order, and the env-only input handling in the "Doctor and targeted boundary run" step.
5. `.claude/skills/s2-linux-run/SKILL.md` §1–§2 and §5, and `tools/qualification_verification/README.md` lines 150–200.
6. `tests/test_s2_run_evidence.py`, `tests/test_qualification_boundary_verification.py`, and `tests/test_s2_evidence_tooling_acceptance.py` (the whole file).

**Report before code:**
- (a) `sha256sum tests/test_s2_evidence_tooling_acceptance.py` equals `e24936ebab9ac0bd8ded6996cdb089a016a1beec746bb04288dc74cfab7aff10`.
- (b) On card 1's base the suite gives **48 failed / 5 passed** of 53 (coordinator record `20260923T152255Z-a92fae550e6f`, Linux).
- (c) `tests/test_s2_run_evidence.py` and `tests/test_qualification_boundary_verification.py` pass on the base: 18 passed (record `20260923T152256Z-24210a09f960`).

## 0.5. Frozen design decisions (constraints, not options)
- **G1. Scope.** `evaluate(dest, *, expect_scope="S3_N1_CAPTURE", head=None)` and `main --expect-scope {S3_N1_CAPTURE,S2_DIAGNOSTIC_SUPERVISION}` (default `S3_N1_CAPTURE`).
  - A scope other than the expected one is not ok, and the output names the expected scope.
  - `DIAGNOSTIC_SUBSET` and `N1_ONLY_TEST_ONLY` are never ok, whatever is requested.
- **G2. Nodes.** The run is ok only if `len(required_nodeids) > 0` and junit `tests >= len(required_nodeids)`.
- **G3. Bytes.**
  - `run_head` asks gh for `event` in addition to the existing fields.
  - `facts["tested_commit"]` is `record.before.commit`. If it is missing, the run is not ok.
  - For `event == "workflow_dispatch"` (and any event other than `pull_request`), `tested_commit` must equal `headSha`, compared lowercase. `facts["tested_commit_kind"] = "head"`. A mismatch is not ok, and the output names both commits.
  - For `pull_request`, `facts["tested_commit_kind"] = "pull_request_merge"`. The checkout tested `refs/pull/N/merge`, so equality is not required, but the tested commit is always printed.
- **G4. `--expect-head`.** Check the value at argument parsing, before any gh call, using argparse's `type=` or `parser.error`, which exits non-zero.
  - It must be 7 to 40 hexadecimal characters; anything else is refused.
  - It is compared case-insensitively as a prefix of `headSha`.
- **G5. `--cases`.** Validate in `qualification_boundary_verification.main` right after `parse_args` and **before** the platform, root and manifest prerequisites. On failure, return 2 and print a message naming `--cases` to stderr. The following are refused:
  - `--cases` with any mode other than `--s3`;
  - a value that is empty after `strip()`;
  - an expression pytest cannot compile. Use `_pytest.mark.expression.Expression.compile`, a private API pinned by the ops lock. If the import fails, return 2 with a message naming `--cases`.

  A valid expression proceeds to the existing prerequisites unchanged.
- **G6. Workflow input validation before provisioning.** Add a step named exactly **`Validate inputs`** between checkout and `Provision protected TEST_ONLY host`. It receives `BOUNDARY_MODE: ${{ inputs.mode || 's3' }}` and `BOUNDARY_CASES: ${{ inputs.cases || '' }}` through `env` only; its `run` script must contain no `${{`. It exits non-zero in three cases:
  - the mode is not `s2` or `s3`;
  - `cases` is non-empty but whitespace-only;
  - `cases` is non-empty and the mode is not `s3`.

  An empty `cases` is valid for both modes. The existing step's `case "$mode"` check may stay.
- **G7. Path filter.** Add the run's real inputs to `pull_request.paths`: `scripts/pytest_qualification_collection.py`, `tools/local_verification/requirements-extra.txt`, `scripts/fp.py`, `pyproject.toml`, `tests/conftest.py`, `core/lib/file_lock.py`, `ops/c1_rail/book_policy.py`, `ops/c1_rail/book_schedule.py` and `ops/c1_rail/policy_fingerprint.py`. They are imported or locked by the qualification package, the host lock (`tools/qualification_verification/host.py:32`) or the collection plugin (`qualification_boundary_verification.py:141`). Use exact paths or narrow globs; do not add a catch-all.
- **G8. Docs.**
  - In SKILL.md §1 step 2 and README ~line 174, the post-dispatch lookup becomes `gh run list --workflow=qualification-s2-supervision.yml --event workflow_dispatch --commit <sha> --json databaseId,headSha,displayTitle,status,createdAt`. Poll it until a run created after your dispatch appears, instead of using a fixed `sleep 15`, and never use `--limit 1`.
  - Both docs state that the default mode is s3, which runs the files named by `S3_CASES`. S2 is the subset named by `S2_CASES`.
  - Both docs name `invariants.json`'s `required_nodeids`, the selection's required nodes (currently 15 for s2 and 19 for s3), instead of "`required` = every registered node".
  - Both docs say, on one line, that a diagnostic run always ends red (exit 2), even when every selected case passed, and that two diagnostics on one ref cancel each other.
  - Also document `--expect-scope` and the `tested_commit` fields in the reader's docstring and in SKILL §2.

## 1. Outcome and return boundary
**Outcome.** The artifact read exits 0 only for:
- the expected scope;
- a non-empty node set that actually ran;
- the bytes the host measured.

For a pull_request run, it reports that the host tested a merge commit. Bad diagnostic inputs fail in seconds, not after provisioning. The skill's lookup finds the dispatch run.

**Return boundary.** All of these hold:
- `tests/test_s2_evidence_tooling_acceptance.py` passes **unedited**;
- the existing suites pass, apart from the edits §2 allows;
- §4 is green;
- a PR is open.

## 2. Files (single writer)
- `scripts/s2_run_evidence.py`.
- `scripts/qualification_boundary_verification.py`: argument validation only (G5). Do not change selection, recording, invariants or cleanup.
- `.github/workflows/qualification-s2-supervision.yml`: the `Validate inputs` step (G6) and `pull_request.paths` (G7). Nothing else.
- `.claude/skills/s2-linux-run/SKILL.md` and `tools/qualification_verification/README.md`: the G8 text only.
- `tests/test_s2_run_evidence.py` changes:
  - `test_full_selection_scopes_are_evidence[S2_DIAGNOSTIC_SUPERVISION]` must now pass `expect_scope="S2_DIAGNOSTIC_SUPERVISION"`;
  - its `artifact()` helper needs a `before.commit`, and junit/required counts that satisfy G2.

  Record each change in §7.
- `tests/test_qualification_boundary_verification.py`: add cases if you like; weaken none.
- **Frozen:** `tests/test_s2_evidence_tooling_acceptance.py`, and the card 1 and card 2 suites.

## 3. Findings (acceptance basis = the named tests)
| ID | Sev | Defect | Required | Acceptance tests |
|---|---|---|---|---|
| G1 | P2 | An s2-mode run reads as acceptance (exit 0) | G1 | `test_g1_*` (five) |
| G2 | P2 | A one-node or short run reads as acceptance | G2 | `test_g2_*` |
| G3 | P2 | The measured commit is never bound to the head; PR runs test a merge commit silently | G3 | `test_g3_*` (five) |
| G4 | P3 | `--expect-head ""` skips the check; one character passes; uppercase is refused | G4 | `test_g4_*` (three) |
| G5 | P3 | `--host-only/--s2/--test-only --cases` and bad expressions are caught late or not at all | G5 | `test_g5_*` (two) |
| G6 | P3 | Whitespace-only or s2 `cases` wastes a provisioned run | G6 | `test_g6_*` (two) |
| G7 | P3 | PRs that change run inputs outside the filter get no PR run | G7 | `test_g7_*` |
| G8 | P2 | The skill's lookup can return the PR run; docs name the wrong selection, wrong key, no red-diagnostic warning | G8 | `test_g8_*` (three) |

## 4. Verification (falsifier-first)
**H:** after this card, `s2_run_evidence.py` exits 0 only for the expected scope, a non-empty node set that ran, and the measured bytes. Bad diagnostic inputs fail before provisioning. **Reject if** any item below fails; **accept if** all hold on one frozen head.
- **Acceptance.** `./fp.ps1 python -m pytest tests/test_s2_evidence_tooling_acceptance.py` gives 53 passed / 0 skipped, with the SHA-256 unchanged. `test_g6_*` needs Git Bash through the `shell` fixture; a skip there is `BLOCKED` (environment).
- **No regression.** `./fp.ps1 --workers 2 python -m pytest tests/test_s2_run_evidence.py tests/test_qualification_boundary_verification.py tests/test_s2_evidence_tooling_acceptance.py tests/test_guard_s2_runs_acceptance.py` exits 0.
- **Gates.** `./fp.ps1 check` exits 0. Whole-repo Pylint is at least 8.00.
- **No Linux run is required or allowed from this card.** The coordinator dispatches one diagnostic run after merge to observe the `Validate inputs` step: once with `cases="   "` (it must fail in under a minute) and once with a valid expression.
- **Evidence.** Cite the record IDs, the interpreter and the head SHA.

## 5. Forbidden
- Editing any frozen acceptance file.
- Changing what the boundary run selects, records or requires.
- Interpolating `${{ inputs.* }}` into any `run` script.
- Relaxing `DIAGNOSTIC_SUBSET` refusal.
- Dispatching any workflow run.
- Touching files outside §2.
- `git stash`; committing without `git diff --stat`; `git commit --no-verify`.
- Merging, or claiming acceptance.
- Using the main checkout as the workdir.

## 6. Return (status taxonomy)
Push `glm/s2-evidence-tooling`, open a PR, and return one of these statuses:
- `DONE`: §4 holds.
- `DONE_WITH_CONCERNS`: §4 holds, and you name a concern.
- `NEEDS_CONTEXT`: something in §0 contradicts the code, or a test looks wrong. Name it, give the evidence, and stop.
- `BLOCKED`: the environment failed. Give the command, the interpreter and the output.

The coordinator rules RESOLVED, FALSIFIED or AMBIGUOUS against §4.

## 7. Executor return
_Pending._ Report:
- the Phase-0 report;
- the head, and `git diff --stat <base>...HEAD`;
- the §4 record IDs and counts;
- the Pylint score;
- the `tests/test_s2_run_evidence.py` edits;
- the PR link;
- the status.

## 10. Launch (after card 1 is accepted)
```powershell
git -C C:\Users\joshu\multi_firm_operations fetch origin
git -C C:\Users\joshu\multi_firm_operations worktree add C:\Users\joshu\mfo-evidence-wt -b glm/s2-evidence-tooling origin/glm/guard-s2-hardening
# start glm_agent with workdir C:\Users\joshu\mfo-evidence-wt and:
# "Execute docs/briefs/handoffs/2026-09-23-s2-evidence-tooling-hardening.md. Phase 0 first; report before code."
```
