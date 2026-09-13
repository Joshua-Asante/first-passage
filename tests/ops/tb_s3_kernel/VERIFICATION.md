# PR 365 bounded redesign — verification record

Implementation checkout: `C:/Users/joshu/multi_firm_operations/.worktrees/pr365-babysit`.
Local branch: `codex/pr365-babysit`; PR branch: `claude/tb-s3-kernel-model`.
The redesign was implemented and verified against starting HEAD
`dfa185c974b8b2def1591831bbeb0f314bb9b42d`. Before committing, the checkout was
fast-forwarded to the collaborator's documentation-only merge
`8aef391e9df3e7451526845a945a48524f44a97b`; no Python or test inputs changed.
The redesign adds the model contract, durable records, rules, effect driver,
mutation runner and tests. No production `ops/` or `core/` files changed.
The operator authorized committing, pushing and repeated Codex review on PR #365.
No PR merge or live action is authorized by this verification record.

## Requirements and evidence

| Requirement | Implementation | Representative verification |
|---|---|---|
| Individual outstanding obligations | `(reason, owner)` records; derived account blocks; queued requests preserve scope and quantity | `test_retried_rejection_still_owns_its_block_after_another_owner_completes`, `test_two_rejected_owners_on_one_symbol_do_not_overwrite_each_other`, `test_later_full_fill_exit_does_not_collapse_into_a_pending_bounded_exit` |
| Shared flatness, remainder and protection rules | Shared quiescence and exact component matcher; cancellation owns residual reservations; component dispatch records | `test_flat_position_with_rejected_cancel_does_not_complete_feed_obligation`, `test_unknown_component_does_not_whitelist_an_unsent_sibling`, `test_bounded_close_requires_the_same_residual_protection_contract`, mixed-outcome and trail tables |
| Explicit evidence order | Acquisition cursor, prepare/dispatch boundaries, request fence, pending requests and execution outcomes | Cached/replayed/future/unordered evidence cases; separate deferred acceptance, execution and delivery; unknown/rejected execution recovery |
| Completion-driven actions; pure reporting | Planned/dispatched/recorded effect journal; whole-request persistence; automatic disarm; pure status | Four crash boundaries on close, kill, attach and takeover; never-dispatched risk-add cancellation; status snapshots after every generated delivery |
| Independent sequence expectations | Named external events, literal allocations and independent unresolved-owner sets | 96 delivery/restart permutations, eight partial-remainder cancellation sequences, two same-symbol owner cases and isolated mutation tests |

Original R1–R8 are retained in `test_tb_s3_kernel_review_round2.py` and supplemented
by `test_tb_s3_kernel_redesign.py` and `test_tb_s3_kernel_sequences.py`. All previous
AC-1–AC-10 and regression suites run together. Three old fixtures were corrected:
backdated commands no longer invent causal evidence; a position-only helper preserves
the acquisition metadata; external exposure is supplied by broker evidence instead of
editing a derived listener view. These changes preserve the behavioral requirements.

## Commands and results

Runtime: existing Python 3.11 virtual environment at
`C:/Users/joshu/multi_firm_operations/.venv/Scripts/python.exe`. Commands ran from the
implementation checkout with `PYTHONDONTWRITEBYTECODE=1` and pytest cache disabled.

| Check | Result |
|---|---|
| Baseline five kernel suites at starting HEAD | 58 passed |
| Initial redesign traces before implementation | 12 failed, 1 passed; failures reproduced the stated defects |
| `python -m pytest tests/ops -q -k tb_s3_kernel -p no:cacheprovider` | 232 passed, 590 deselected after final cleanup |
| `python -m pytest tests/ops -q -p no:cacheprovider` | 809 passed, 13 skipped, two existing seaborn deprecation warnings |
| `python scripts/gate_manifest.py --tier check` | Exit 0; public-worktree skips/warnings for absent private artifacts remain visible |
| Focused pylint, all model modules and seven test suites, `--fail-under=8.0` | Exit 0; 9.86/10 with repository and layer roots on `PYTHONPATH` |
| Repository-wide pylint, tracked and untracked Python files, `--jobs=4 --fail-under=8.0` | Exit 0; 8.49/10 |
| `git diff --check` | Exit 0 |

For check-tier gate subprocesses on this Windows host, PATH included the existing
virtual environment's Scripts directory and PYTHONPATH included its site-packages.
The Python base interpreter requires the tool's supported sandbox escalation; no
production packaging or test configuration was changed to hide that constraint.

The first repository-wide lint run encountered a Windows cp1252 encoding error
while printing the duplicate-code report. The same checks passed on retry with
`PYTHONIOENCODING=utf-8` and `python -X utf8 -m pylint`; no checks were disabled.

`python tests/ops/tb_s3_kernel/mutation_check.py` ran in disposable copies with an
unmodified 232-test control. All five mutations caused behavioral assertion failures:

| Mutation | Failed tests |
|---|---:|
| Overwrite another owner of the same reason | 77 |
| Treat zero position as flat despite working remainder | 4 |
| Trust timestamps without acquisition causality | 1 |
| Ignore protective parameter mismatches | 3 |
| Omit completion-driven disarm | 9 |

Independent review accepted the bounded offline code after reproducing and closing
its findings. The reviewer independently ran all seven kernel suites: 232 passed.
The final nonfunctional cleanup removed unused helpers/imports and normalized line
endings; the coordinator repeated the kernel suite and focused lint afterwards.

## Disposition

The local offline redesign is implemented and reviewed. The production-reference
acceptance hold remains pending operator disposition; this record does not approve
the current GitHub PR or merge it. Remote CI and Codex review results are recorded
on PR #365 against each pushed head; the results above are local verification.
Live L-1 equivalent evidence/request ordering, L-2 validation, production disarm
acknowledgment and the existing feed-loss ratification are still explicit dependencies.
`CONTRACT.md` states the model refinements that the owning spec and TB-I3 must carry.
