# H9 checkpoint R1 tooling: the R1 workflow mode, evidence scope and selector (worker build card)

**Type:** cc_handoff (worker build card)

**Status:** FROZEN for build by coordinator (3), 2026-10-02. Coordinator (3) resolved D1–D5 on 2026-10-02 (§9); the card was frozen with those resolutions applied and committed under the committed-handoff rule. The dispatch revision is the commit that carries this file on `claude/r1-tooling`; the coordinator records its SHA in its dispatch note before the first ticket. Line citations are to `origin/main@d716106`; every cited code, test, workflow and owner file is unchanged from the drafting base `6ead3df` (§9).

**Executor:** one implementation worker (a `glm_agent` ticket series run by the coordinator, or one Claude Code worker), the single writer of `claude/r1-tooling`. It builds on top of the commit that carries this card.

**Coordinator:** deployment coordinator (3), "Coordinating parallel Claude sessions (3)". It owns the freeze, the diff review, the CI-approval request to Joshua, every Linux dispatch, the PR, and the ledger.

**Owners this card narrows. It changes none of them.**
- R1 broadening, operator ruling 5 ("broaden R1"): `docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md:1998-2006`. The R1 grant: `:2030`. The three qualification-path items owed before R1: `:2033-2036`. The residual citation rule: `:2022-2026`. The re-measurement before R1: `:2120-2124`.
- H9 checkpoint R1: `docs/briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md:535-551` (gates and the C′ case list), `:561` (the R1 work line), `:577-579` (evidence retained), `:584` (grants: the coordinator holds `ci.dispatch`).
- Who builds the tooling, and the CI-approval rule: the C′ card in PR #614 (`claude/dispatch-cards-2026-10-02`), `docs/briefs/handoffs/2026-10-02-h9-cprime-runtime-identity-build-DRAFT.md:195` (tooling gap D6) and `:249` (D6 resolution: a `.github/workflows` change needs Joshua's CI-configuration approval); coordinator (3)'s queue item 4.

```yaml authority
seat: worker
parent: docs/briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push]
constraints:
  - no_main_write
  - no_merge
  - no_pr_open
  - no_linux_or_ci_dispatch
  - no_ci_configuration_commit
  - workflow_change_as_patch_file_only
  - card_section5_files_only
  - no_invariant_manifest_registration
  - no_boundary_test_or_fixture_edit
  - no_qualification_runtime_edit
  - no_private_bytes_committed
  - single_writer
  - stop_at_coordinator_return
acceptance:
  - tests/test_qualification_boundary_verification.py
  - tests/test_s2_run_evidence.py
  - tests/test_s2_evidence_tooling_acceptance.py
  - tests/test_s2_evidence_tooling_followups.py
  - tests/test_guard_s2_runs.py
  - tests/test_guard_s2_runs_acceptance.py
  - tests/test_guard_s2_runs_revision2.py
```

The workflow's static test (§4 G8) is a new file that travels **inside the workflow patch** (§5), so it is outside this committed acceptance list.

## 0. Phase 0: premise check, then Rule 0 reads, before any edit

The first act is the §10 premise check, reported before any edit. Any failure is a stop (§7). A contradiction between this card and what the executor reads is returned as `NEEDS_CONTEXT`; the executor does not choose a reading itself.

**Test 0 (secrets and private sources).** The build reads and writes only public repository code, tests and documentation. It reads no `.env`, credential, Pine source, runtime port, account figure or private evidence. A `glm_agent` workdir is the worktree `C:/Users/joshu/multi_firm_operations/.claude/worktrees/r1-tooling` (no `.env`, checked at freeze), never the primary checkout.

**Rule 0 reads (at `d716106`, the branch base; re-checked 2026-10-02):**
- `scripts/qualification_boundary_verification.py` in full: the tuples `:21-47`, `cases_refusal` `:76-100`, the mode group `:105-111`, the host check `:121-123`, the required-set derivation `:146-158`, the scope metadata `:159-171`, the environment `:177-188`, the selection and collection `:189-212`.
- `scripts/s2_run_evidence.py` in full: the docstring `:1-68`, the scope tuples `:87-113`, `_file_set_refusals` `:194-215`, the SR-8 export `:217-268`, `evaluate` `:270-338`, `main` `:340-`.
- `scripts/guard_s2_runs.py`: the module docstring `:1-60`, `_TITLE_MODE` `:97`, the redundancy and diagnostic advice `:176-207`.
- `scripts/pytest_qualification_collection.py`: `collected.json` is a sorted JSON list of node IDs (`:20-23`).
- `.github/workflows/qualification-s2-supervision.yml`: `:16-27`, `:43`, `:60-71`, `:82-101`, `:130-140`, `:172-179`.
- `AGENTS.md`, "Python environment and local checks".

## 0.5. Routing (task-routing checklist, re-applied at dispatch)

`Routing: local`.
- **Verification uses the Windows operations launcher** (`python -I scripts/fp.py`) on committed bytes; records land under `.cache/fp-verification/`.
- **GLM-eligible.** The work is bounded implementation from this frozen spec with a fixed file list, so the coordinator may run it as sequential `glm_agent` tickets with `workdir` = the `r1-tooling` worktree and `dry_run: true` on the first ticket. Suggested split: (1) selector and its tests; (2) reader scope, `--expect-selection` and its tests; (3) guard and its tests; (4) the workflow patch and its static test, written to the patch file only. Each ticket quotes the card sections it implements and names its files and tests. After each ticket the coordinator reads the actual diff and runs the named tests. A ticket that fails twice leaves GLM for the escalation lane.
- **No Linux or CI run falls in this card** (§5).

## 1. Selected outcome

The R1 tooling on branch `claude/r1-tooling`, pushed, with **no PR** (the coordinator opens it after §8's CI approval). It lets the coordinator dispatch, and acceptance-read, the **combined** R1 Linux run that ruling 5 defines (`:1998-2006`):
1. **A selector:** an `--r1` mode in `scripts/qualification_boundary_verification.py`, with its own ordered file tuple, record scope and installation variable.
2. **An evidence scope:** `T05_R1_COMBINED` in `scripts/s2_run_evidence.py`, bound to the selector's tuple, plus `--expect-selection` (D3).
3. **A guard tag:** `[r1]` recognition in `scripts/guard_s2_runs.py`.
4. **A workflow mode:** `r1` in `.github/workflows/qualification-s2-supervision.yml`, delivered **only as a patch file** for Joshua's CI approval, never committed by the worker.

The tooling does not run R1, register any node or change any boundary test. It is safe on `main` before the integrated candidate exists: while any R1 file or manifest row is missing, a full `--r1` refuses in seconds (D5).

**Why it is needed.** The workflow offers only `s2`–`s5` (`qualification-s2-supervision.yml:23-27`). The selector stops at `S5_CASES` (`qualification_boundary_verification.py:46-47`, modes `:105-111`). The reader accepts four scopes (`s2_run_evidence.py:101-102`, `:108-113`). The guard parses only `[s2]`–`[s5]` (`guard_s2_runs.py:97`). The result/seal Linux file is selected by no mode (`codex/h9-t05-integration@f237178`, `tests/integration/qualification_boundary/test_campaign_result_seal_linux.py:5-7`, skip text `:74`).

## 2. The selector

**Order (D1).** Ruling 5 and H9 (`:561`, `:578`) fix service, N1, N2, Part A, result/seal, supervision last, plus the C′ and VALID→VOID cases. D1 places the C′ file immediately before supervision, after result/seal:

| # | File (`tests/integration/qualification_boundary/…`) | Status at `d716106` |
|---|---|---|
| 1 | `test_campaign_service_linux.py` | on `main` |
| 2 | `test_campaign_n1_linux.py` | on `main` |
| 3 | `test_campaign_n2_linux.py` | on `main` |
| 4 | `test_campaign_part_a_linux.py` | on `main` |
| 5 | `test_campaign_result_seal_linux.py` (`RESULT_SEAL_CASE`) | **absent**: on `codex/h9-t05-integration@f237178`, 6 tests, 0 manifest rows; lands with H9 |
| 6 | `test_runtime_identity_linux.py` (`CPRIME_CASE`, **placeholder entry**, D5) | **absent**: written by the C′ build (#614 card `:52`, `:113`) |
| 7 | `test_campaign_supervision_linux.py`, **last** (its final case contaminates the common memory group) | on `main` |

**Build exactly:**
- `RESULT_SEAL_CASE` and `CPRIME_CASE` as module constants with the paths above, and `R1_CASES = (*S5_CASES[:-1], RESULT_SEAL_CASE, CPRIME_CASE, S5_CASES[-1])`, with a comment in the S5 style naming the supervision-last constraint, D1 and the D5 placeholder. No node ID is hard-coded.
- `--r1` joins the mutually exclusive mode group, help text "S5 plus the result/seal and C′ Linux files (H9 checkpoint R1), never full E1 acceptance by itself". It sets `FP_QUALIFICATION_S2`, `S3`, `S4` and `S5` exactly as `--s5` does, plus `FP_QUALIFICATION_R1=1`. Every other mode pops `FP_QUALIFICATION_R1`. The fixture seam that reads it is H9's (OWED, §9).
- Required nodes: the registered nodes of `tests/ops/qualification/invariant_manifest.json` inside `R1_CASES`, derived like `--s5` (`:146-148`). Collection and `require_invariants` run for `--r1` as for `--s5`.
- `metadata.acceptance_scope = 'T05_R1_COMBINED'`, with `qualification_acceptance='coordinator_review_required'` and `invariant_manifest_sha256` as today.
- `--cases` is accepted with `--r1`; the record becomes `DIAGNOSTIC_SUBSET` and the run exits non-zero (extend `:86-87`, `:167-171`).
- **Refusal in seconds, before the Linux/root check** (`:121-123`): a new `r1_refusal(args)` (or an extension of `cases_refusal`) returns exit 2 with `Failed prerequisite: …` when, for a full or subset `--r1`, either holds: (a) any `R1_CASES` file is absent from the tree; (b) any `R1_CASES` file contributes zero registered nodes to the invariant manifest. The message names every missing file and every zero-row file. Paths resolve against `ROOT`, and the manifest path is the module constant, so a test can monkeypatch both.
- **`--test-only` ignores every `R1_CASES` file** and excludes them from its required set (`:153-158`, `:193-195`), replacing the `S5_CASES` exclusion with `R1_CASES` (a strict superset). This keeps N1_ONLY green once H9 lands file 5 and C′ lands file 6.

## 3. Evidence scope

**Reader scope `T05_R1_COMBINED`** in `scripts/s2_run_evidence.py`, appended to `ACCEPTANCE_SCOPES` (the default stays `S4_JOINT_N2`, `:103`). `SCOPE_FILES['T05_R1_COMBINED'] = R1_CASES`, **imported** from the selector, never duplicated. It reads ok only when all hold:
- every record fact the S5 read requires (`:5-27`): `status=completed`, `exit_code=0`, `verification_exit_code=0`, `source_stable`, `capture_complete`, `cleanup.ok`, `acceptance_scope == T05_R1_COMBINED`, `invariants.passed`, junit tests ≥ required with 0 failures, 0 errors and **0 skips**, and for a dispatch run `tested_commit == headSha`;
- the required nodes cover exactly `R1_CASES` (`_file_set_refusals`, `:194-215`);
- the SR-8 Part A export (`:217-268`): the gate at `:333-334` changes from `expect_scope == S5_SCOPE` to "the scope's file set includes `PART_A_CASE`";
- **D3, the frozen selection:** `--expect-selection PATH` is **required** for `T05_R1_COMBINED` and refused (argparse/usage error, exit 2) with any other scope. `PATH` is a committed JSON the coordinator writes at the R1 dispatch, of exactly this shape: `{"schema": "r1-dispatch-selection/1", "acceptance_scope": "T05_R1_COMBINED", "node_count": <int>, "node_ids": [<str>, …]}`. The reader refuses (not ok, with a named reason) when the file is missing or unparsable, has another key set, `schema` or scope, a duplicate node ID, `node_count != len(node_ids)`, or `set(node_ids) != set(collected.json)` (collected.json under `<record-id>/`; missing = refused), and it requires `len(collected) == node_count`. Facts gain `expected_selection_sha256` (SHA-256 of the file bytes) and `expected_selection_count`. The tooling never writes or commits a selection file outside test temp directories;
- **C′ coverage export (freeze-time rule, coordinator may override):** its schema is owed by the C′ build (ledger `:2019`; H9 `:549`). Until a follow-up defines it, `T05_R1_COMBINED` is **fail-closed**: an R1 record that passes every other check is still refused with the single named reason `cprime_coverage_export_check_owed`. The worker does not invent a schema and does not stop for this (it replaces the draft's NEEDS_CONTEXT stop).
- Cross-scope refusals: an S5 record read as R1 is refused, and an R1 record read as S5 is refused.
- The module docstring, usage line and `--expect-scope` choices name the new scope and flag.

**Run artifact** (unchanged): name `qualification-s2-supervision`, 14-day retention (`qualification-s2-supervision.yml:172-179`), carrying `<record-id>/record.json`, `invariants.json`, `junit.xml`, `collected.json`, `boundary/` with `journal.sqlite` and `part_a_observations.json`, and the host logs (`:113-122`, `:143-171`).

**Retention of acceptance evidence** (coordinator, not worker): archive the artifact within its 14-day life into private `local_artifacts/r1-runs-<date>/` with `SHA256SUMS` (ledger `:2050`, `:2073`); record the fresh-download `record.json` hash and the selection file's SHA-256 in the acceptance entry; the R1 packet cites the residual "T05 C′ first-release host environment drift", the expected identity contract and the observed coverage (`:2026`; H9 `:551`). H9's Windows lines and `check` (`:579`) belong to the R1 executor.

**Guard (`scripts/guard_s2_runs.py`):** `_TITLE_MODE` gains `r1` (`:97`); `r1` is incomparable with every other mode for redundancy (`:22-28`); the redundancy advice prints `--expect-scope T05_R1_COMBINED --expect-selection <frozen-selection.json>` for r1 (`:191-196`); the diagnostic advice uses `-f mode=r1` (`:199-206`); `S2_CASES_NOTE` (`:93`) names r1 among the modes that accept `cases`. `DEFAULT_MODE` stays `s4`.

## 4. Verification (falsifier-first)

**H:** the tooling selects, refuses and reads R1 exactly as §2–§3 state, without changing any s2–s5, `--test-only` or `--host-only` behavior. **Falsifier:** any red item below that passes on the base, or any green item that fails on the pushed head. Every run goes through the launcher and cites its `record.json` with `status`, exit code and `source_stable`; a missing or non-`completed` record is not evidence.

**Red, on the base commit with only the new tests applied** (each must fail):
- R1. `main(['--r1', …])` exits 2 from argparse (no such mode).
- R2. The reader rejects `--expect-scope T05_R1_COMBINED` (not a choice, `:348-350`).
- R3. The guard does not parse `[r1]` as a mode.
- R4. `--test-only`, on a tree fixture containing file 5, does not ignore it.

**Green, on the branch head:**
- G1. `R1_CASES` equals the §2 seven-tuple in order, supervision last; a strict superset of `S5_CASES` preserving S5's order.
- G2. `--r1` requires exactly the registered nodes inside `R1_CASES`; scope `T05_R1_COMBINED`; environment has `FP_QUALIFICATION_S2/S3/S4/S5/R1` set; every other mode leaves `FP_QUALIFICATION_R1` unset.
- G3. `--r1 --cases=<expr>` yields `DIAGNOSTIC_SUBSET` and a non-zero exit.
- G4. A full `--r1` exits 2 before the Linux/root check (runs on Windows) when an R1 file is absent, and when an R1 file has zero registered nodes; on the real base tree it refuses naming files 5 and 6.
- G5. `--test-only` ignores every `R1_CASES` file and excludes them from its required set.
- G6. Reader: `SCOPE_FILES['T05_R1_COMBINED'] is R1_CASES`; S5-as-R1 and R1-as-S5 refused; R1 requires the SR-8 export; a skip, a missing file or a foreign node is refused; `--expect-selection` missing with R1, or given with another scope, exits 2; each selection defect in §3 is refused by name; a complete record with a matching selection is refused only for `cprime_coverage_export_check_owed`.
- G7. Guard: `[r1]` parses; an s5 run never counts as r1 coverage and vice versa; the redundancy and diagnostic advice name r1.
- G8 (inside the patch). A static test reading the YAML: the `r1` option is present; both `case` lists accept `r1`; `cases` is allowed with `r1`; the default is still `s4`; `timeout-minutes` is 180 (D4). It passes with the patch applied to the branch head.
- G9. Every existing test in the acceptance list passes unchanged in meaning; `python -I scripts/fp.py check` exits 0 (any pre-existing failure disclosed, not called a pass); `git diff --check` is clean; `git apply --check` of the patch on the pushed head succeeds.

**Selection:**
```
python -I scripts/fp.py --workers 2 python -m pytest tests/test_qualification_boundary_verification.py tests/test_s2_run_evidence.py tests/test_s2_evidence_tooling_acceptance.py tests/test_s2_evidence_tooling_followups.py tests/test_guard_s2_runs.py tests/test_guard_s2_runs_acceptance.py tests/test_guard_s2_runs_revision2.py tests/scripts/test_shell_tokens_modes.py tests/test_git_hooks.py -q
```

**No Linux evidence is claimed or produced by this card.**

## 5. Files and the workflow patch

**Allowed (committed):**
- `scripts/qualification_boundary_verification.py`
- `scripts/s2_run_evidence.py` (including docstring and usage line)
- `scripts/guard_s2_runs.py`
- the seven acceptance-list test files, each extended in place, never replaced
- `scripts/README.md`: entry-point lines only

**The workflow patch (never committed):** the worker edits `.github/workflows/qualification-s2-supervision.yml` and writes the new static test file `tests/test_qualification_s2_supervision_workflow.py`, then writes `git diff` of exactly those two paths (the new file via `git add -N` or `git diff --no-index`) to `C:/Temp/claude/C--Users-joshu-multi-firm-operations/30e01f1b-9cfa-417f-9a01-f66ad9cc662c/scratchpad/r1-workflow.patch`, then restores both paths so the worktree is clean. The patch changes only:
- `on.workflow_dispatch.inputs.mode.options`: `[s2, s3, s4, s5, r1]`, with an r1 clause in the description; **default stays `s4`**;
- both mode `case` statements (`:84`, `:134`) accept `r1`, and their error text names it; the `cases` allow-list (`:98-101`) includes `r1`;
- `timeout-minutes: 180` (D4), with the comment updated to cite the ~90 min s5 run 36936558798 plus files 5 and 6;
- nothing else: `run-name` (`:16-19`), concurrency (`:60-63`), triggers, permissions, secrets and artifacts are unchanged. R1 is dispatch-only (`gh workflow run qualification-s2-supervision.yml --ref <branch> -f mode=r1`).

**Forbidden:** any commit or push touching `.github/**`; `tests/integration/qualification_boundary/**`; `tests/ops/qualification/invariant_manifest.json`; `scripts/check_qualification_invariants.py`; `ops/**`, `deploy/**`, `tools/qualification_verification/**`; `.claude/**` (settings, hooks, skills, including `s2-linux-run`); `core/`, `lab/`, Pine, and any private file; draft #609's branch.

**Out of scope:** any R1 or S8 Linux run or workflow dispatch; registering nodes; writing or changing boundary tests or fixtures, including the `FP_QUALIFICATION_R1` fixture seam (H9); the C′ build and its coverage-export schema; lane D step 3 (term 8); #611; the S5 re-measurement; R2; changes to #609; writing the dispatch-frozen selection file (coordinator, at dispatch); the `s2-linux-run` skill update (it still names `s3` as the default; a follow-up through the skill-authoring path); any production use.

## 6. Output and return (status taxonomy)

The return contains: branch, head and base (the card commit); `git diff --stat <card-commit>...HEAD` and files touched; per §4 item the red and green `record.json` paths with status, exit code and `source_stable`; the `check` record; the patch path, its SHA-256 and its full text; concerns.

**Status.** Exactly one:
- `DONE`: every §4 item holds on the pushed head, the patch is written, the worktree is clean.
- `DONE_WITH_CONCERNS`: as `DONE`, plus a named concern for the coordinator.
- `NEEDS_CONTEXT`: a §7 stop that is an ambiguity or contradiction, named with evidence.
- `BLOCKED`: any other §7 stop, named.

The coordinator either accepts the return (verdict RESOLVED: every §4 item holds on re-run) or corrects it (verdict FALSIFIED: an item fails, named and returned).

## 7. Stop conditions (return to the coordinator; do not work around)

- The §10 premise check fails, or a Rule 0 anchor in §0 does not match the base.
- Any forbidden file would have to change, or the patch would need a change beyond §5's list.
- The R1 order conflicts with supervision-last.
- Any step would need a Linux run, CI dispatch, PR, merge or production value.
- Two failed corrections of the same issue (AGENTS.md), or one GLM ticket failing twice.
- More than three review rounds each returning two or more P1/P2 findings: the coordinator adjudicates.
- A second writer appears on `claude/r1-tooling`.

## 8. Decision unlocked, and the CI-approval step

A `DONE` return opens the coordinator's diff review, then:
1. The coordinator presents `r1-workflow.patch` to Joshua **verbatim** in chat, with: mode `r1` is dispatch-only; the default stays `s4`; timeout 180 min; no new secret, permission, trigger or artifact.
2. The approval is valid only as a **direct yes from Joshua for that patch** (a relayed yes does not count). The coordinator records it and the patch's SHA-256 in the ledger.
3. Only then is the patch applied and committed on the branch (by the coordinator or a re-dispatched worker), pushed, and the PR opened. Any later change to the workflow needs a fresh approval. **Merging stays Joshua's act.**

**#609 (S8).** #609 will be rebuilt later as R1 plus the full-campaign file; owner coordinator (3). This card does not touch #609; whichever lands second rebases. R1 tooling lands first because R1 precedes T06/S8 (H9 `:582`).

**Not granted:** any Linux or CI run; R1 itself; node registration; any production value, qualification, activation, arm, deployment or trade.

**Before R1 itself** (not gates on this tooling, which must not pre-empt them): H9 integration on `main` with file 5 and its seams (0 skips under `FP_QUALIFICATION_R1`); result/seal and C′ nodes registered; C′ RESOLVED with the C′ and VALID→VOID cases folded in (C′ card `:187`); lane D step 3 / term 8 (ledger `:693`); #611 and the three qualification-path items (`:2033-2036`); T00-first integration; one fresh S5 Part A measurement after the last closure change (`:2124`); independent review; the selection file frozen and committed by the coordinator; the C′ coverage-export check landed; **Joshua's express R1 Linux grant** (`:2030`).

## 9. Dispatch record

- **2026-10-02 (drafted):** draft for coordinator (3) against `origin/main@6ead3df`, with decisions D1–D5 open.
- **2026-10-02 (resolved and frozen):** coordinator (3)'s resolutions, applied:
  - **D1 yes:** the C′ Linux file sits immediately before supervision, after result/seal.
  - **D2 yes:** mode `r1`, flag `--r1`, scope `T05_R1_COMBINED`, environment `FP_QUALIFICATION_R1` (tuple `R1_CASES`).
  - **D3 yes:** the reader mechanically checks a committed dispatch-frozen node-ID list and count via `--expect-selection` (§3).
  - **D4:** `timeout-minutes: 180`.
  - **D5:** build now with the six files plus a C′ placeholder entry; a full `--r1` refuses within seconds while any R1 file or manifest row is missing.
  - **OWED to H9 (lane D step 3 / H9 integration):** the VALID→VOID file (whether `test_void_orderings_against_result_and_seal` in file 5 or a separate file; a separate file adds its `R1_CASES` entry then), the `FP_QUALIFICATION_R1` fixture seam, and the manifest registration of the result/seal (and VALID→VOID) nodes.
  - **OWED to the C′ build:** file 6, its manifest rows, and the coverage-export schema; the reader's fail-closed `cprime_coverage_export_check_owed` is replaced by a real check in a follow-up once the schema lands.
  - **Workflow:** delivered as `r1-workflow.patch` for Joshua's CI approval, not committed (§5, §8).
  - **Freeze-time choices** (beyond D1–D5; the coordinator may override before dispatch): the C′ export is fail-closed rather than a NEEDS_CONTEXT stop; `--expect-selection` is required for, and limited to, `T05_R1_COMBINED`; the worker opens no PR (`pr.open` removed from the grant).
  - **Anchor re-check:** `git diff --stat 6ead3df d716106` over every cited script, test, workflow, manifest, boundary directory and owner file is empty, so `:line` citations taken at `6ead3df` hold at `d716106`.

## 10. Audit hooks (runnable)

```bash
# Card form and authority block. Expected: RESULT: well-formed; exit 0.
python -I scripts/fp.py python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-10-02-r1-tooling-build-card.md
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-02-r1-tooling-build-card.md

# Premise check (Git Bash), in the r1-tooling worktree. Set CARD to the commit that carries this card.
CARD=$(git log -1 --format=%H -- docs/briefs/handoffs/2026-10-02-r1-tooling-build-card.md)
git merge-base --is-ancestor "$CARD" HEAD && echo "builds on the card commit" || echo "FAIL: not on the card commit"
test ! -e .env && echo "no .env in the workdir" || echo "FAIL: .env present"
git diff --quiet d716106 "$CARD" -- scripts tests .github ops && echo "no code drift since the anchor base" || echo "FAIL: code drift; re-check anchors, NEEDS_CONTEXT"

# Scope at return: only §5 committed files; no .github path.
git diff --stat "$CARD"...HEAD
git diff --name-only "$CARD"...HEAD | grep -E '^(\.github|\.claude|tests/integration|tests/ops|ops|core|lab)/' && echo "FAIL: forbidden path" || echo "scope ok"
git apply --check C:/Temp/claude/C--Users-joshu-multi-firm-operations/30e01f1b-9cfa-417f-9a01-f66ad9cc662c/scratchpad/r1-workflow.patch && echo "patch applies" || echo "FAIL: patch"
```
