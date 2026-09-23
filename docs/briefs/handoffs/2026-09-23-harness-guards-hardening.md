# GLM handoff: shell and write guards stop missing real bypasses and stop asking on data (F29, A1–A7, B1–B3)

**Type:** cc_handoff (frozen-spec implementation against a coordinator-authored acceptance suite)
**Date:** 2026-09-23
**Status:** FROZEN. **Queued behind [card 1](2026-09-23-guard-s2-runs-hardening.md).** Both cards write `scripts/guard_shell_command.py` and `.claude/settings.json`, so under the single-writer rule this card starts only after card 1's return is accepted. Dispatch it to the same GLM session as a follow-on.
**Dispatch, 2026-09-23 (operator: fan out, no GLM):** executed by a Claude Code worker agent on branch `claude/harness-guards-hardening`, cut from card 1's Revision 1 head `f09399e` (#470), where the single-writer conflict with card 1 has closed. Base counts re-measured there: **52 failed / 36 passed** of 88 (record `20260923T171233Z-c7694c3c0b6b`); the frozen hash is unchanged. Wherever this card says GLM or `glm/harness-guards-hardening`, read the worker and this branch.
**Executor:** GLM (Z Code), the single writer for the files in §2. **Coordinator:** Claude, who wrote the acceptance suite and rules on the return. **Operator:** Joshua, who alone merges.
**Base:** the accepted head of `glm/guard-s2-hardening` (card 1). Worker branch **`glm/harness-guards-hardening`**, cut from that head after `git merge origin/claude/guard-s2-hardening-card` if this card's commit is not already in it.
**Authority:** the files in §2 and nothing else. `DONE` gives no permission to merge.

## 0. Phase 0: read, then report before code (repository `Joshua-Asante/first-passage`)
Run the [`handoff-verify`](../../../.claude/skills/handoff-verify/SKILL.md) checklist. Report the anchors and the three facts below before the first edit. If anything contradicts the code, return `NEEDS_CONTEXT`.

**Workdir:** reuse card 1's worktree (for example `C:\Users\joshu\mfo-guard-wt`) or make a fresh one. **Never** use `C:\Users\joshu\multi_firm_operations`, which holds a `.env`.
**Test 0:** no vendor data, credentials or secrets. The tests build throwaway git repos under `tmp_path`.

**How this card was found.** Round 2 of the review stalled for about 8 hours. Its background agents ran Bash commands that contained destructive-looking text only as data: a heredoc probe file and a scratch cleanup. `guard_shell_command.py` answered `ask`, and a background agent has nobody to approve a prompt, so the tool call never returned. The audit then found the reverse problem as well: the guard lets through real bypasses that git accepts. Every A-item below was reproduced against git 2.43 in a repository whose pre-commit hook exits 1.

Reads:
1. `scripts/guard_shell_command.py`: the docstring (the two classes it claims to cover; the warn-class posture; the `--force-with-lease` divergence), and `NO_VERIFY`, `DESTRUCTIVE` and `classify()`. Both regexes are `re.search` over the raw command string, with no parsing.
2. `scripts/guard_s2_runs.py` as card 1 left it: its quote-aware and heredoc-aware tokenizer (card 1 D14). **Reuse it.** Move it to a shared module if that is cleaner, but do not keep two tokenizers.
3. `scripts/guard_open_verification_record.py`: `RECORDS_DIR`, `_open_records`, `decide`, `_targets`.
4. `scripts/record_verification.py`: `__init__` persists `status='not_started', before=None, finished_at=None`; `begin()` persists the `before` snapshot (lines 132–134); `execute()` sets `status='running'` (line 178). `scripts/fp.py:257–325` and `scripts/docker_verification.py:127–160` do real work between `begin()` and `execute()`, including `docker build` for up to 900 s. `docker_verification.py:127` writes records to `.cache/fp-docker-verification/<id>`.
5. `.claude/settings.json` (the write guard's matcher is `Edit|Write|MultiEdit`), `tests/scripts/test_guard_shell_command.py`, `tests/test_guard_open_verification_record.py`, and `tests/test_harness_guards_acceptance.py` (the whole file).

**Report before code:**
- (a) `sha256sum tests/test_harness_guards_acceptance.py` equals `6f60feaa32d3cb55243c2e194cb441d0b6546207ba8700281c0dcccc20d66813`.
- (b) On card 1's base the suite gives **52 failed / 36 passed** of 88 (coordinator record `20260923T151928Z-44cc7f00310e`, Linux). Report your count on card 1's accepted head.
- (c) The existing suites `tests/scripts/test_guard_shell_command.py` and `tests/test_guard_open_verification_record.py` pass on that head.

## 0.5. Frozen design decisions (constraints, not options)
- **E1. Classify commands, not text.** `classify(cmd)` tokenizes with card 1's tokenizer.
  - Destructive or bypass words count only in **command position**: the words of a segment after wrappers are stripped (`sudo`, `env` with its assignments, `command`, `exec`, `nohup`, `time`, `timeout <dur>`), and inside the string argument of `bash -c`/`sh -c`, which is re-parsed.
  - These are data, never commands: heredoc bodies, quoted arguments of other programs (`grep`, `rg`, `echo`, `printf`, `git log --grep`, `git commit -m`), and `python -c` strings.
  - The body of a `$(…)` substitution is re-parsed as commands. A heredoc inside it stays data.
  - **If tokenizing fails**, fall back to the current raw-string regexes. An unparsable command that contains destructive text still asks.
- **E2. Hook and signing bypass → `ask`, with the existing `NO_VERIFY_AGENT_MSG`.** It applies to `commit`, `merge`, `push`, `am`, `rebase`, `cherry-pick` and `revert` (whichever accept the flags) when any of these holds:
  - an argument is a prefix of `--no-verify` or `--no-gpg-sign` at least 6 characters long (git accepts unambiguous prefixes);
  - for `commit` only, `n` appears in a short-option cluster (`-n`, `-nm`, `-anm`). `-n` means `--dry-run` for push and `--no-stat` for merge;
  - a `-c core.hooksPath=…` global option is given (the key is case-insensitive).
- **E3. Destructive → `ask`, with the existing `DESTRUCTIVE_AGENT_MSG`.** Skip git global options before the subcommand (`-C <dir>`, `-c <k=v>`, `--no-pager`, `--git-dir=…`, `--work-tree=…`). Then:
  - `reset`: an argument that is a prefix of `--hard`, at least 4 characters.
  - `clean`: `f` in a short cluster, or `--force`. `-n` alone is a dry run and is allowed.
  - `checkout`: `--` anywhere, or `-f`/`--force`.
  - `restore`: any invocation, unless the only target is the index (`--staged`/`-S` without `--worktree`/`-W`).
  - `switch`: `-f`, `--force` or `--discard-changes`.
  - `push`: `f` in a short cluster, or `--force` (never `--force-with-lease`, bare or `=…`), or a refspec starting with `+`.
  - `branch`: `D` in a short cluster, or delete (`d`/`--delete`) together with force (`f`/`--force`) across arguments.
  - `rm` (any path to the binary): a recursive flag (`r`/`R`/`--recursive`) together with a force flag (`f`/`--force`) across arguments.
- **E4. The existing contracts stand.** `classify()` still returns `(permission, agent_msg, user_msg)`, and `main()` keeps card 1's D15 behavior. This card changes only which commands ask; it never denies.
- **E5. Open records (B1, B2).** `_open_records` scans `.cache/fp-verification/*/record.json` **and** `.cache/fp-docker-verification/*/record.json`. A record is open while `started_at` is within `STALE_AFTER_SECONDS` and either condition holds:
  - `status == "running"`, or
  - `status == "not_started"` and `before` is not null and `finished_at` is null. `begin()` has measured the tree, and a write now voids the record.

  Records written outside the checkout (`qualification_boundary_verification.py` on Linux CI) stay out of scope. Say so in the module docstring.
- **E6. NotebookEdit (B3).** `_targets` also reads `tool_input.notebook_path`. The write guard's settings entry must match `NotebookEdit` as well as `Edit`, `Write` and `MultiEdit`, and must not match `Bash`. Change only that entry's `matcher`.
- **E7. No recorder change.** `scripts/record_verification.py` is read-only for this card. E5 needs only fields it already persists.

## 1. Outcome and return boundary
**Outcome.** The shell guard asks on every spelling git and rm accept for the operations it claims to guard, and stops asking on text that is only data. That stops the unanswerable prompts that stall background agents. The write guard covers Docker records, the measured window before `running`, and notebook edits.
**Return boundary.** Done when:
- `tests/test_harness_guards_acceptance.py` passes **unedited** (SHA-256 unchanged);
- the existing suites pass, with the only changes being the ones §2 allows;
- §4 is green;
- a PR is open against `main`, or against `glm/guard-s2-hardening` while card 1's PR is open.

## 2. Files (single writer)
- `scripts/guard_shell_command.py`: `classify()` and its helpers; update the docstring to describe command-position matching and the data carve-outs. `main()` is unchanged from card 1.
- `scripts/guard_s2_runs.py`, or a new shared module such as `scripts/_shell_tokens.py`: move the tokenizer here only if you share it; behavior must not change (card 1's suite must stay green).
- `scripts/guard_open_verification_record.py`: `_open_records`, `_targets`, docstring.
- `.claude/settings.json`: the write guard entry's `matcher` only.
- `tests/scripts/test_guard_shell_command.py` and `tests/test_guard_open_verification_record.py`: add cases if you wish, and do not weaken any. If a case contradicts the acceptance suite, list it in §7 with the acceptance test that supersedes it.
- `REPO_MAP.md`: only through its generator, and only if a new module is added.
- **Frozen, never edit:** `tests/test_harness_guards_acceptance.py` and card 1's `tests/test_guard_s2_runs_acceptance.py`.

## 3. Findings (acceptance basis = the named tests)
| ID | Sev | Defect | Required | Acceptance tests |
|---|---|---|---|---|
| F29 | P2 | Destructive text inside heredocs, quotes, patterns or messages asks, which stalls background agents indefinitely | E1 | `test_f29_*` (two, one parametrised ×11) |
| A1 | **P1** | `commit -n`/`-nm`/`-anm`, `--no-verif`, `--no-gpg` and `-c core.hooksPath=…` skip hooks or signing without a prompt | E2 | `test_a1_hook_and_signing_bypass_asks[*]`, `test_a1_short_n_is_a_bypass_only_for_commit[*]` |
| A2 | P2 | Git global options before the subcommand (`-C`, `--no-pager`, `-c`) defeat every git pattern | E3 | `test_a2_a7_destructive_commands_ask[git -C …, git --no-pager …, git -c …]` |
| A3 | P2 | `reset -q --hard`, `reset HEAD~1 --hard`, `reset --har`, `clean -d -f`, `clean --force` | E3 | same test, A3 rows |
| A4 | P2 | `checkout HEAD -- .`, `checkout -f`, `restore .`, `switch -f/--discard-changes` | E3 | same test, A4 rows |
| A5 | P2 | `push origin +main`, `push -uf`/`-fu` | E3 | same test, A5 rows |
| A6 | P2 | `branch --delete --force`, `-d -f`, `-fD` | E3 | same test, A6 rows |
| A7 | P2 | `rm -fr`, `-r -f`, `-Rf`, `--recursive --force` | E3 | same test, A7 rows |
| B1 | P2 | Docker verification records never lock the tree | E5 | `test_b1_*` (two) |
| B2 | P2 | Writes allowed between `begin()` and `execute()` still void the record | E5 | `test_b2_*` (four, including the real `RunRecord`) |
| B3 | P3 | NotebookEdit is not matched, and `notebook_path` is ignored | E6 | `test_b3_*` (two) |
| — | — | Neighbours that must stay allowed | E2/E3 | `test_non_destructive_neighbours_are_allowed[*]` |

## 4. Verification (falsifier-first)
**H:** after this card, the shell guard asks exactly on the command-position bypasses and destructive operations listed in E2/E3, and on nothing that is only data; the write guard locks the tree from `begin()` for both record roots and for notebook edits. **Reject if** any item below fails; **accept if** all hold on one frozen head.
- **Acceptance:** `./fp.ps1 python -m pytest tests/test_harness_guards_acceptance.py` gives 88 passed / 0 failed / 0 skipped, and the SHA-256 is unchanged. *Falsified by* any failure, skip or edit.
- **No regression:** `./fp.ps1 --workers 2 python -m pytest tests/scripts/test_guard_shell_command.py tests/test_guard_open_verification_record.py tests/test_guard_s2_runs_acceptance.py tests/test_guard_s2_runs.py tests/test_git_hooks.py tests/test_harness_guards_acceptance.py` exits 0. Card 1's suite must stay green: a shared tokenizer that breaks it falsifies the return.
- **Gates:** `./fp.ps1 check` exits 0. Whole-repo Pylint must be at least 8.00: add docstrings rather than disables.
- **Live smoke:** pipe `{"tool_input":{"command":"cat > p.py <<'EOF'\nx = 'rm -rf /'\nEOF"}}` into `python scripts/guard_shell_command.py`. It must print nothing. The same payload with `git commit -n -m x` must print an `ask` JSON.
- **Evidence:** a `record.json` for each run (`status: completed`, exit 0, `source_stable: true`), plus the interpreter and head SHA.

## 5. Forbidden
- Editing either frozen acceptance file, or adding a conftest, plugin or monkeypatch that changes them.
- Making `classify()` return `deny`.
- Removing the `--force-with-lease` carve-out.
- Changing `scripts/record_verification.py`, `fp.py`, `docker_verification.py`, any workflow, or any file outside §2.
- Loosening a case the existing suites pin.
- `git stash`; committing without `git diff --stat`; `git commit --no-verify`.
- Merging, or claiming acceptance.
- Using the main checkout as the workdir.

## 6. Return (status taxonomy)
Push `glm/harness-guards-hardening`, open a PR (§1), and return one of:
- `DONE`: §4 holds.
- `DONE_WITH_CONCERNS`: §4 holds, plus a named concern.
- `NEEDS_CONTEXT`: a §0 contradiction or a test you believe is wrong. Name it, give evidence, and stop.
- `BLOCKED`: an environment failure. Give the command, the interpreter and the output.

The coordinator's verdict is RESOLVED, FALSIFIED or AMBIGUOUS against §4. Worker tests are extra evidence only.

## 7. Executor return
_Pending._ Report:
- the Phase-0 report;
- the head and `git diff --stat <base>...HEAD`;
- the §4 record IDs and counts;
- the Pylint score;
- the live-smoke output;
- any superseded existing cases;
- the PR link;
- the status.

## 10. Launch (after card 1 is accepted)
```powershell
git -C C:\Users\joshu\mfo-guard-wt fetch origin
git -C C:\Users\joshu\mfo-guard-wt switch -c glm/harness-guards-hardening glm/guard-s2-hardening
# then tell the same glm_agent session:
# "Execute docs/briefs/handoffs/2026-09-23-harness-guards-hardening.md. Phase 0 first; report before code."
```
