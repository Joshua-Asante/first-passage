# GLM handoff: harden the S2 run guard and stop the PreToolUse hooks from auto-approving (F1–F28)

**Type:** cc_handoff (frozen-spec implementation against a coordinator-authored acceptance suite)
**Date:** 2026-09-23
**Status:** FROZEN (re-frozen 2026-09-23 before dispatch; see the amendment at the end of §0.5). Ready to dispatch. The operator launches GLM locally (`glm_agent` / Z Code runs only on the operator's Windows machine).
**Executor:** GLM (Z Code). It is the single writer for the files in §2. **Coordinator:** Claude (this session). It authored the acceptance suite and rules on every return. **Operator:** Joshua. Only he merges, and he may overrule D15 before dispatch.
**Base:** the tip of `claude/guard-s2-hardening-card`, which is PR #462's head `2ee26c9` plus the commit that adds this card and `tests/test_guard_s2_runs_acceptance.py`. Worker branch: **`glm/guard-s2-hardening`**, cut from that tip.
**Authority:** the files in §2 and nothing else. A `DONE` status gives no permission to merge.

## 0. Phase 0: read before writing code, then report (repository `Joshua-Asante/first-passage`)
Run the [`handoff-verify`](../../../.claude/skills/handoff-verify/SKILL.md) checklist as Phase 0. Report the anchors (`git log -1 --format='%h %as' -- <path>`) and the three facts at the end of this section **before the first edit**. If anything below contradicts the code, return `NEEDS_CONTEXT` rather than choosing a reading yourself.

**Workdir.** Make a fresh worktree, for example `git worktree add C:\Users\joshu\mfo-guard-wt -b glm/guard-s2-hardening origin/claude/guard-s2-hardening-card`. **Never** use the main checkout `C:\Users\joshu\multi_firm_operations` as the `glm_agent` workdir, because it holds a `.env`.

**Test 0 (vendor data and secrets).** Nothing here reads a gitignored vendor-data path, a credential or a secret. The guard calls `gh` and `git` at runtime, but every test fakes both at the `_run` seam, so no `gh` authentication is needed. Nothing needs to be staged for this dispatch.

Reads:
1. `scripts/guard_s2_runs.py`, the whole file (286 lines at `2ee26c9`): `_segments`, `_git_push_branches`, `_gh_dispatch`, `push_refusal`, `dispatch_refusal`, `COVERAGE`, `_run_mode`, `_default_branch`, `refusal_for_command`, `claude_hook`, `pre_push`, `_run`.
2. `scripts/guard_shell_command.py`, `main`/`_emit`/`classify`. `main` emits `allow` when parsing fails, and `classify` returns `allow` for every benign command.
3. `scripts/guard_open_verification_record.py`, `main`. It emits `allow` for every Edit/Write/MultiEdit that it does not refuse (the lines after `for target in _targets(data)`).
4. `.claude/settings.json`, the `hooks.PreToolUse` entries, and `scripts/githooks/pre-push`.
5. `.github/workflows/qualification-s2-supervision.yml`: `run-name` (lines 16–20), the `mode`/`cases` inputs, and `concurrency` (line 50: `group: qualification-s2-${{ github.ref }}-(diagnostic|full)`, `cancel-in-progress: true`). The group key contains **no mode and no SHA**. A `pull_request` run's `github.ref` is `refs/pull/N/merge`, and its title ends `(N/merge)`.
6. `tests/integration/qualification_boundary/conftest.py:60–63` and `fixture_install.py:58–66`. Under `--s3` the harness installs `--dispatch`, which means profile/release v5. `--s2` installs v4. **The same S2 nodes therefore run on different installs, so an s2 run and an s3 run never substitute for each other (F5).** The comment at `scripts/qualification_boundary_verification.py:30` ("strictly larger mode") describes node selection only. It does not say the runs are equivalent.
7. `.claude/skills/s2-linux-run/SKILL.md` §1 (the enforcement paragraph) and §5.
8. `tests/test_guard_s2_runs_acceptance.py`, the whole file: the `FakeShell` contract, the helpers and every test. Also `tests/test_guard_s2_runs.py`, `tests/scripts/test_guard_shell_command.py`, `tests/test_guard_open_verification_record.py`, and the `hook_checkout` fixture in `tests/test_git_hooks.py`.
9. The Claude Code PreToolUse contract. `permissionDecision: "allow"` **bypasses the permission system**: the tool runs without a prompt. Exiting 0 with no stdout defers to the normal permission flow. `deny` blocks the call and shows the reason to the model.

**Report before code:** (a) `sha256sum tests/test_guard_s2_runs_acceptance.py` equals `c1d0509b11a8f65941cc3ecf1bac4e4190eb5ef6195ab5d346ae35f10c1cab8e`. (b) On the base, the acceptance suite gives **138 failed / 7 passed** of 145. The coordinator's record for this is `20260923T150626Z-3b9114f33078` on Linux, where most failures are the missing `cwd` keyword. Through a `cwd` shim the result is 92 failed / 53 passed, and every failure maps to a row in §3. (c) The pre-existing suites pass on the base: `tests/test_guard_s2_runs.py`, `tests/scripts/test_guard_shell_command.py`, `tests/test_guard_open_verification_record.py` and `tests/test_git_hooks.py` give **115 passed / 1 skipped** (record `20260923T150709Z-c0996fd36abb`).

## 0.5. Frozen design decisions (ruled by the coordinator; these are constraints, not options)
- **D1. The seam.** `_run(cmd: list[str], cwd: str | None = None) -> str | None` is the module's only process boundary. It calls `subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=20, check=False)`. It returns stdout on exit 0 and `None` otherwise. It catches `OSError`, `subprocess.SubprocessError` and `ValueError` (`UnicodeDecodeError` is a subclass) and returns `None`. Every `gh` and `git` call goes through `_run`, and the module makes no other subprocess call.
- **D2. The entry points.**
  - `refusal_for_command(command: str, cwd: str | None = None) -> str | None`.
  - `claude_hook(stdin) -> int` reads `tool_name`, `tool_input` and `cwd` from the payload and always returns 0. Its stdout is **empty unless it denies**. A deny is exactly `{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": <reason>}}`. Any exception, including bad JSON, gives silent exit 0.
  - `pre_push(stdin) -> int` returns 1 only when it refuses, and prints a reason containing `FP_S2_GUARD=off` to stderr.
- **D3. A push is refused only when it would cancel a run.** A push to branch B is refused when both hold:
  - an in-flight `pull_request` run of this workflow exists on B (status `queued`, `in_progress`, `waiting`, `requested` or `pending`);
  - that run belongs to a PR that is **open** with head B, meaning its title ends `(N/merge)` and N appears in `gh pr list --head B --state open`. A PR run whose title has no `(N/merge)` counts while any PR on B is open.

  Failure handling:
  - If `gh pr list` fails, fall back to the unfiltered answer and keep refusing.
  - If `gh run list` fails, allow the push.

  Exceptions:
  - A tip commit carrying `[skip ci]`, `[ci skip]`, `[no ci]`, `[skip actions]`, `[actions skip]` or a `skip-checks: true` trailer is allowed, **unless an earlier segment of the same command runs a git command that can move the tip** (`commit`, including `--amend`; `pull`, `merge`, `rebase`, `cherry-pick`, `revert`, `am`, `reset`). The new tip's message is unknown at PreToolUse time.
  - Dispatch runs never block a push, because they run in their own concurrency group.
- **D4. Cancellation (F3, F4).** A full dispatch on ref R is refused, with `cancel` in the reason, while **any** full (non-diagnostic) `workflow_dispatch` run of this workflow is queued or in progress on R. Its mode, SHA and tag do not matter. A diagnostic dispatch is refused in the same way while a diagnostic dispatch is live on R. Full and diagnostic runs never block each other, and `pull_request` runs never block a dispatch.
- **D5. Redundancy (F2, F5, F22).** Consider only **completed `workflow_dispatch`** runs of this workflow on the dispatch's SHA that carry the **same** bracketed mode tag (`[s2]`/`[s3]`) and are not diagnostic. The newest definitive run among them decides:
  - `success`: refuse, with `passed` in the reason.
  - `failure`: refuse, with `re-roll` in the reason. The advice names `-f mode=s3 -f cases=` and `FP_S2_GUARD=off gh workflow run`.

  These are never coverage: `cancelled`/`skipped` runs, untagged or unbracketed titles, other SHAs, and `pull_request` runs (they tested `refs/pull/N/merge`, which is not the head alone). **s2 and s3 are incomparable.**
- **D6. Push, then dispatch, in one command (F1).** When an earlier segment pushes R, a later dispatch on R cannot know its SHA. Skip the redundancy check and keep the cancellation check.
- **D7. Default branch (F26).** With no `--ref`, try `gh repo view [OWNER/REPO] --json defaultBranchRef` (the repository is positional; `gh repo view` has no `-R`), then `git symbolic-ref refs/remotes/origin/HEAD` (short or long form), and otherwise allow. **Never** use the local branch.
- **D8. `-R/--repo` (F9).** Pass the flag to every `gh` call except two: `gh api` takes no `-R`, so its path must be `repos/<owner>/<repo>/…`, and `gh repo view` takes the repository positionally. Do not call `git ls-remote` when `-R` names the repository; get the SHA through `gh api`.
- **D9.** A `cases` dispatch in `mode=s2` is refused, and the reason names `s3`, because the workflow accepts `cases` only in s3 and the run would fail at setup (F23).
- **D10.** When `--json` supplies the dispatch inputs, they are unknown, so allow the dispatch (F13).
- **D11. `gh run rerun <id> [--failed|--job J]` (F10).** Read the run with `gh run view <id> --json …`.
  - Refuse when it is a full run of this workflow that concluded `success` or `failure`.
  - Refuse when rerunning it would cancel a live run in the same concurrency group: same ref and kind, or for `pull_request` runs, the same PR.
  - Allow `cancelled` runs, diagnostic runs and other workflows. Allow when the view fails.
- **D12. MCP tools (F20).** Route PreToolUse for `mcp__github__(push_files|create_or_update_file|delete_file|update_pull_request_branch|actions_run_trigger)` to `guard_s2_runs.py claude-hook`, and map each one's `tool_input`:
  - `branch` means a push to that branch. A `message` carrying a skip-ci marker is allowed.
  - `pullNumber` means a push to that PR's `headRefName`.
  - `run_workflow` means a dispatch (`workflow_id`, `ref`, `inputs`).
  - `rerun_workflow_run` / `rerun_failed_jobs` mean a rerun (`run_id`).

  `owner`/`repo` name the repository exactly as `-R owner/repo` would (D8). Add these tools as a **separate** PreToolUse entry: leave the `Bash` entry's matcher byte-identical, because `tests/scripts/test_guard_shell_command.py::test_guard_is_actually_wired` requires `matcher == "Bash"` and `guard_shell_command.py` must not run on MCP calls. `mcp__github__get_file_contents` must not match. Any other `tool_name` gets no output.
- **D13. The override.** `FP_S2_GUARD=off` counts in three places: as a leading assignment on the push or dispatch segment itself, in an earlier `export FP_S2_GUARD=off` segment, or in the process environment for the pre-push layer. The advice text reads `FP_S2_GUARD=off git push …` / `FP_S2_GUARD=off gh workflow run …`.
- **D14. Parsing (F7, F8, F13–F19, F27).** Use one quote-aware and heredoc-aware tokenizer:
  - join `\`-newline continuations; treat newline, `;`, `&&`, `||`, `|`, `&`, `(` and `)` as separators;
  - drop redirections with their targets;
  - strip wrapper words (`env` with its assignments and flags, `command`, `builtin`, `exec`, `nohup`, `time`, `timeout <dur>`, `sudo`, `if/then/elif/while/until/do/!`), and re-parse the string argument of `bash -c`/`sh -c`;
  - a `$(…)` or backquote destination or `--ref` resolves to the current branch of the directory where the segment runs; a bare `$VAR` is unknown, so allow;
  - track `cd <dir>` (relative to the hook's `cwd`) and `git -C <dir>`;
  - read flags as pflag does (`-rX`, `-r=X`, `-fK=V`, `-f=K=V`, `--field=K=V`, `--raw-field=K=V`, `-F K=V`; `-F` overrides `-f`), and strip a `refs/heads/` prefix;
  - accept the workflow selector anywhere after `run`: file basename, `.github/workflows/…` path, name compared casefolded, or ID `362153971`; accept `gh.exe` too;
  - `--delete/-d/:dst/--tags/--dry-run/-n` update no branch;
  - `--all/--branches/--mirror` update every local branch (`git for-each-ref`).
- **D15. The permission bypass (F24, F28).** `guard_shell_command.main` and `guard_open_verification_record.main` stop emitting `allow`, so benign or unparsable input produces no output. `ask` and `deny` are unchanged, and the internal `classify()`/`decide()` may keep returning `"allow"`. *This changes behavior:* benign commands and file writes will go through the operator's normal permission rules and will no longer be auto-approved. The coordinator ruled it because a hook `allow` silently overrides the operator's permission settings. The operator may overrule this before dispatch.
- **D16. Fail-open posture.** Every lookup failure allows the action, except the pr-list refinement in D3, as the module docstring requires ("never blocks on its own failure").

- **The fake's contract.** `FakeShell` honours `gh run list --branch/--workflow/--event/--commit/--status/--limit/--json`, `gh pr list --head/--state/--json`, `gh run view <id> --json`, `gh repo view --json/--jq`, and `gh api` (raw JSON per endpoint; `--jq` takes dotted paths on objects only). Read lists with `--json` and parse them in Python. Runs carry `workflowName`, `name` and `workflowDatabaseId`. Directory arguments are compared as POSIX paths with any drive letter dropped, so the suite behaves the same under `./fp.ps1` on Windows.

**Amendment 2026-09-23, before dispatch (coordinator).** An independent audit of the suite found five problems:
- One test path could not pass on Windows: `FakeShell` used `os.path.normpath`, which turns `/repo` into `\repo`.
- `gh api` answered as a table instead of JSON.
- Every `gh api` endpoint returned the same shape.
- `git symbolic-ref` answered the long form with the short name.
- Four card rules were wrong or silent: D3 (only `git commit` counted as moving the tip), D7/D8 (`gh repo view` has no `-R`), and D12 (a merged matcher would break the shell guard's wiring test).

The suite was fixed and re-frozen. Fifteen cases were added to pin requirements no test covered: tip-moving commands before a skip-ci push, the hook using the payload's `cwd`, a push to another branch before a dispatch, `rerun_failed_jobs`, `owner`/`repo` mapped to `-R`, and four more wrappers. **The earlier hash `4bba3f47…e041` is void.**

## 1. Outcome and return boundary
**Outcome.** The run guard refuses exactly the actions that would cancel a live S2 run or re-roll a definitive one. It recognises every spelling an agent actually types and every harness path (Bash, MCP, git pre-push). The three PreToolUse hooks never approve anything.
**Return boundary.** You are done when:
- all of `tests/test_guard_s2_runs_acceptance.py` passes **unedited**, with the SHA-256 unchanged;
- the pre-existing suites pass, except that cases §2 lets you retire may be removed;
- the gates in §4 are green;
- the PR is open against `main`, or against `claude/time-sink-guards` while #462 is still open (say which in the PR body).

**Out of scope.** Changing the workflow; changing `scripts/githooks/pre-push`, where F11's wiring already passes; any qualification code; any other hook.

## 2. Files (you are the single writer for each)
- `scripts/guard_s2_runs.py`: the implementation. Correct the module docstring's "`s3` covers `s2`" and "covers every harness" claims.
- `scripts/guard_shell_command.py`: `main` only, for D15.
- `scripts/guard_open_verification_record.py`: `main` only, for D15.
- `.claude/settings.json`: the `hooks.PreToolUse` matchers only, for D12. Leave `permissions` and every other hook byte-identical.
- `tests/test_guard_s2_runs.py`: the pre-hardening unit suite. It encodes behavior that is now superseded. Rewrite or delete these cases:
  - the `pull_request`-default rows of `test_full_dispatch_refused_only_on_same_sha_live_or_definitive`;
  - the whole `test_dispatch_coverage_compares_requested_mode_with_prior_mode` matrix (s3⊇s2, PR events);
  - `test_claude_hook_allows` and `test_claude_hook_fails_open_without_gh` (the `allow` JSON and the one-argument `_run`);
  - `test_hook_passes_requested_mode_through`;
  - any monkeypatch of private helpers that no longer exist.

  List every removed or changed case in §7, with the acceptance test that supersedes it.
- `tests/scripts/test_guard_shell_command.py`: change `test_malformed_stdin_fails_open` to expect no output. Change `test_emits_claude_not_cursor_decision_shape` so it exercises a command that asks, such as `rm -rf /tmp/x`. Keep the `classify()` cases.
- `tests/test_guard_open_verification_record.py`: add a no-output case for `main` if you want one. Keep the `decide()` cases.
- `.claude/skills/s2-linux-run/SKILL.md` §1: fix the enforcement paragraph. It is the one that says `[s3]` covers `[s2]`, which is now false. Also fix `scripts/README.md` and `REPO_MAP.md` if their guard wording is now false. Regenerate `REPO_MAP.md` with its generator, never by hand.
- **Not yours:** `tests/test_guard_s2_runs_acceptance.py` is **frozen**. If a test in it looks wrong, return `NEEDS_CONTEXT` and name the test. Do not edit it.

## 3. The findings (acceptance basis = the named tests; the rows state what each must prove)
| F | Sev | Defect at `2ee26c9` | Required behavior | Acceptance tests (fail on base, pass after) |
|---|---|---|---|---|
| 1 | P2 | `git push && gh workflow run --ref <same>` is judged against the pre-push remote SHA | D6 | `test_f1_dispatch_after_a_push_in_the_same_command_skips_the_stale_sha`, `test_f1_a_push_to_another_branch_leaves_the_dispatchs_sha_known` |
| 2 | P2 | PR runs (`refs/pull/N/merge`) count as the head's bytes and block a head-only dispatch | D4, D5 | `test_f2_live_pr_run_does_not_block_a_dispatch`, `test_f2_pr_runs_never_count_as_the_dispatchs_bytes` |
| 3 | P2 | An allowed dispatch cancels a live run in the same concurrency group (regression from `2ee26c9`) | D4 | `test_f3_f4_full_dispatch_refused_while_a_full_dispatch_run_is_live_on_the_ref[*]`, `test_f3_diagnostic_and_full_dispatches_are_separate_groups` |
| 4 | P2 | An untagged live run is dropped, so a cancelling duplicate is allowed | D4 (a live run blocks whatever its tag), D5 (an untagged completed run is not coverage) | `test_f3_f4_…[live2]`, `test_untagged_or_other_sha_completed_runs_are_not_coverage` |
| 5 | P2 | "s3 covers s2" is false (v5 install vs v4) | D5, modes incomparable | `test_f5_modes_are_incomparable[*]` |
| 6 | P2 | Live PR runs of closed PRs block pushes | D3 | `test_push_refused_while_open_prs_run_is_live`, `test_f6_*` (four), `test_f6_pre_push_allows_when_the_pr_is_closed` |
| 7 | P2 | Separators are split before quotes and heredocs are read | D14 | `test_commands_that_do_not_update_a_live_branch_are_allowed[*quoted*, *grep*, *rg*, *log*, *heredoc*]` |
| 8 | P2 | Redirections are read as refspecs | D14 | `test_pushes_that_update_a_live_branch_are_refused[*2>&1*, *> /tmp*]` |
| 9 | P2 | The workflow selector is recognised only at `tokens[3]`, in exact spellings | D8, D14 | `test_f9_every_selector_spelling_is_recognised[*]`, `test_f9_repo_flag_is_passed_to_every_gh_query`, `test_other_workflows_are_ignored` |
| 10 | P2 | `gh run rerun` is never checked | D11 | `test_f10_*` (three) |
| 11 | P2 | The pre-push wiring is untested | passes on base; keep it green | `test_f11_pre_push_hook_feeds_git_refs_to_the_guard_and_honours_its_exit[*]` |
| 12 | P2 | Fixtures ignore branch/ref arguments | the `FakeShell` seam answers only flags gh honours | every hook-level test; `test_f12_pre_push_checks_the_remote_ref_not_the_local_one` |
| 13 | P3 | pflag forms misread | D10, D14 | `test_f13_*` |
| 14 | P3 | Non-updating pushes are refused; `--all`/`--mirror` checks only one branch | D14 | the `--delete/-d/:feat/--tags/--dry-run/-n` allow cases, `test_f14_push_all_checks_every_local_branch` |
| 15 | P3 | `cd`/`-C` are ignored | D14; the hook reads the payload's `cwd` | `test_f15_*` (three) |
| 16 | P3 | The override applies to the whole compound command | D13 | `test_f16_override_counts_only_on_the_push_segment_itself` |
| 17 | P3 | A `$(…)` destination is looked up as a literal | D14 | refused cases `"$(git branch --show-current)"`, `$(git rev-parse …)`; allowed `"$BRANCH"` |
| 18 | P3 | Backslash-newline continuations are skipped | D14 | refused `\`-newline push and dispatch cases |
| 19 | P3 | Wrappers hide git/gh | D14 | refused `env`, `command`, `timeout`, `/usr/bin/git`, `bash -c`, `sh -c`, `if`, subshell, `&`, `out=$(…)`, `sudo`, `nohup`, `time`, `!` cases |
| 20 | P3 | Server-side pushes and dispatches bypass both layers | D12; `gh pr update-branch` is a push to the PR head | `test_f20_*` (eight) |
| 21 | P3 | A `[skip ci]` tip is refused | D3 | `test_f21_*` (four, one parametrised over seven tip-moving commands) |
| 22 | P3 | A stale failure outranks a newer pass | D5 (newest definitive decides) | `test_f22_the_newest_definitive_same_mode_run_decides` |
| 23 | P3 | The advice suggests an s2 diagnostic that cannot run | D5 advice, D9 | `test_failure_advice_names_a_runnable_diagnostic`, `test_f23_s2_diagnostic_is_refused_because_it_cannot_run` |
| 24 | **P1** | The Bash hooks emit `allow`, which bypasses the operator's permission rules on every command | D2, D15 | `test_f24_*` (five) |
| 25 | P3 | A cp1252 decode error crashes the Windows pre-push, and so refuses the push | D1 | `test_f25_undecodable_output_fails_open`, `test_run_passes_cwd_to_subprocess` |
| 26 | P3 | The default-branch test mocks the helper it tests | D7 | `test_f26_*` (two) |
| 27 | P3 | Parser tests pass for the wrong reason | D14 | refused `-c k=v`, `+feat`, `wip:feat`, `wip feat`, newline, `GIT_TRACE=`, diagnostic-then-push cases |
| 28 | **P1** | The Edit/Write hook emits `allow` for every write, including writes outside the checkout | D15 | `test_f28_write_guard_does_not_approve_writes`, `test_f28_write_guard_still_denies_while_a_record_is_open` |

## 4. Verification (falsifier-first: each item names what would make the return false)
**H:** the guard refuses only cancelling or re-rolling actions, recognises every listed spelling and harness path, and no PreToolUse hook approves anything. **Reject if** any item below is falsified; **accept if** all hold on one frozen head.
- **Acceptance.** `./fp.ps1 python -m pytest tests/test_guard_s2_runs_acceptance.py` gives 145 passed / 0 failed / 0 skipped, and the file's SHA-256 is still `c1d0509b…ab8e`. *Falsified by* any failure or skip, a changed hash, or an `xfail`/`skip`/`importorskip` added anywhere that affects these tests.
- **F11 on Windows.** `test_f11_*` needs Git Bash at the path the `shell` fixture expects. If it skips there, return `BLOCKED` (environment) with the fixture's skip reason. A skip is not a pass, and the test itself is not defective.
- **Regression.** `./fp.ps1 --workers 2 python -m pytest tests/test_guard_s2_runs.py tests/scripts/test_guard_shell_command.py tests/test_guard_open_verification_record.py tests/test_git_hooks.py tests/test_guard_s2_runs_acceptance.py` exits 0. *Falsified by* a removed case missing from the §7 supersession list.
- **Gates.** `./fp.ps1 check` exits 0, or name any pre-existing failure together with its record on the base. Whole-repo Pylint `pylint --fail-under=8.0 $(git ls-files '*.py')` scores at least 8.00. The base with the acceptance file scored about 8.07, so new code must not pull the score down: add docstrings, and do not disable checks for whole modules.
- **Live smoke (read-only).** From the worktree, pipe three payloads into `python scripts/guard_s2_runs.py claude-hook`: `ls`, then a push to a branch with no runs, then a dispatch of `tests.yml`. Each must print nothing. *Falsified by* any output.
- **Evidence.** Cite each `record.json` from `.cache/fp-verification/` (`status: completed`, exit 0, `source_stable: true`). Report the interpreter and the head SHA. A record that is `running`, `failed` or `interrupted` is not acceptance.

## 5. Forbidden
- Editing `tests/test_guard_s2_runs_acceptance.py`, or adding a `conftest.py`, plugin or monkeypatch that changes how it behaves.
- Changing `.github/workflows/qualification-s2-supervision.yml`, `scripts/githooks/pre-push`, any qualification code, or any file outside §2.
- Loosening a refusal the acceptance suite does not require you to loosen.
- Adding a network call that is not routed through `_run`.
- Running `gh workflow run`, `gh run rerun` or any real dispatch; pushing to any branch but `glm/guard-s2-hardening`.
- Changing `permissions` in `.claude/settings.json`.
- `git stash`; committing without `git diff --stat` first; `git commit --no-verify`.
- Merging, or claiming acceptance.
- Using the main checkout `C:\Users\joshu\multi_firm_operations` as your workdir.

## 6. Return (status taxonomy)
Push `glm/guard-s2-hardening` and open a PR (§1). Return exactly one status:
- `DONE`: everything in §4 holds.
- `DONE_WITH_CONCERNS`: §4 holds, and you name a concern the coordinator must adjudicate before merge.
- `NEEDS_CONTEXT`: a §0 contradiction, or an acceptance test you believe is wrong. Name it, give the evidence, and stop.
- `BLOCKED`: an environment failure you could not diagnose. Give the command, the interpreter and the output.

Worker tests are extra evidence only. The acceptance basis is §3. The coordinator's verdict on the return is RESOLVED (every §4 item holds on the returned head, re-run by the coordinator), FALSIFIED (an item fails) or AMBIGUOUS (the evidence cannot decide, e.g. a record not `completed`).

## 7. Executor return
_Pending._ Report:
- the Phase-0 report (anchors, hash, base counts);
- the head SHA and `git diff --stat <base>...HEAD`;
- each §4 record ID with its counts;
- the Pylint score;
- the supersession list for `tests/test_guard_s2_runs.py` and `tests/scripts/test_guard_shell_command.py`;
- the live-smoke output;
- the PR link;
- the status.

## 10. Launch (operator, Windows)
```powershell
git -C C:\Users\joshu\multi_firm_operations fetch origin claude/guard-s2-hardening-card
git -C C:\Users\joshu\multi_firm_operations worktree add C:\Users\joshu\mfo-guard-wt -b glm/guard-s2-hardening origin/claude/guard-s2-hardening-card
# then start glm_agent with workdir C:\Users\joshu\mfo-guard-wt and this prompt:
# "Execute docs/briefs/handoffs/2026-09-23-guard-s2-runs-hardening.md. Phase 0 first; report before code."
```
