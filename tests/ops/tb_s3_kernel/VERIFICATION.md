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

### Codex follow-up to `2eb6c12`

Codex reported seven findings on the pushed redesign. Six were reproduced and repaired:
fill-entry remainder ownership, timestamp regression after position-only evidence,
sizing loss across harness restart, unowned orphan cancellation, daemon loosening
gate bypass, and interrupted multi-order cancellation planning. The seventh proposed
deferring a gap for a broker-pending first attachment; both source review and an
independent reviewer confirmed that this conflicts with rev 5.6 I7 and the recorded
contract. A concrete characterization retains the specified recovery behavior.

`test_tb_s3_kernel_review_round3.py` adds 30 cases. The first run against `2eb6c12`
produced 22 failures and three passing controls. Further composed cases were also
observed failing before repair: orphan fill/cancel recovery, consumed amendments,
partial unallocated recovery, and residual exposure first observed after dispatch.
The final kernel run passed all 262 cases, independently repeated by the reviewer,
who accepted the bounded offline code with no blocking findings. Final full-ops:
839 passed, 13 skipped, two existing seaborn warnings. Focused lint across the model
and all eight suites: 9.87/10, exit 0. Check-tier gates passed (normal private-data
skips); pre-commit and push hooks are run when integrating the repairs.

The isolated mutation runner passed its 262-test control and detected all five
semantic mutations again: owner overwrite 77 failures, ignored working remainder 3,
timestamp without causality 1, ignored protection parameters 3, omitted disarm 9.
Repository-wide lint and other remote checks for this follow-up are tracked on the
PR; the earlier 8.49/10 local result applies to the initial redesign, not this diff.

### Codex follow-up to `ea8a5db`

Codex reported five further findings: admission combining different acquisitions,
obsolete planned effects reviving completed operations, restart trusting arbitrary
orders linked to known lots, intermediate store writes losing command suffixes,
and a fake-broker partial budget applied independently to each lot. All five were
reproduced and repaired. The first new regression run had 17 failures and two controls.

Caller review reproduced the same coherence defect in orphan cancellation and close
retry. Independent review also found durable prefixes that stranded orphan cancels,
retained phantom entry reservations (ordinary admission and takeover settlement),
and saved an immediate attachment-rejection gap without its required recovery close.
Each was observed failing before repair. The shared planning boundary now commits
the whole transition before dispatch, with synchronous Decision results constructed
after the effect driver returns. Outcome recording does not drain during restart.

`test_tb_s3_kernel_review_round4.py` adds 28 cases. Store cuts interrupt actual atomic
writes, independently of the number of calls to `persist`. Scope completion tests
deliver the covering scope read before resuming planned dispatch. Broker quantity
expectations use literal totals across multiple lots and independently cap the
request quantity. The complete local kernel suite passes 290 cases.

Independent review accepted the bounded offline model after inspecting the complete
repair diff and independently running all nine kernel suites: 290 passed. Full-ops
verification: 867 passed, 13 skipped, two existing seaborn warnings. Check-tier gates
passed with the normal public-worktree/private-data skips. Focused lint passed at
9.82/10. The isolated mutation runner passed its 290-test control and detected every
mutation: owner overwrite 77 failures, ignored working remainder 3, timestamp without
causality 1, ignored protective parameters 3, omitted disarm 11. `git diff --check`
passed. GitHub CI and the next Codex review are separate checks on the pushed commit.

### Codex follow-up to `e46a4fa`

The next Codex review found four issues: fresh unowned orders were ignored by live
admission; multi-component amendments published only their first effect; amendment
classification combined mismatched acquisitions; and first trailing attachment did
not require `L2(g)`. All 14 initial round5 cases failed before repair.

The shared fixes retain each unowned order and unallocated position as an account
obligation; stage every amendment component atomically; pause unknown attempts until
covering evidence then resume never-sent siblings; require coherent classification
and dispatch; and reject unsupported first trailing attachments before definition.
Additional controls cover both owner-resolution orders, position-only uncertainty,
and reported unknown outcomes with and without broker execution.

`test_tb_s3_kernel_review_round5.py` adds 26 cases. A final source check also reproduced
an unknown-kind cancellation being admitted through the protective-orphan path;
unknown kinds now refuse while fresh known entry/add orders remain cancelable beside
existing allocated exposure. Their terminal cancellation does not close the existing
lot; raced external fills retain separate unallocated-exposure ownership. Independent
review caught the need to preserve that known-kind path, and its flat/nonflat and
restart race cases are retained. The older unsent-sibling protection
test now cuts the automatic resumed dispatch at its planned boundary and delivers
the adversarial scope evidence first, preserving its original guarantee that a
never-attempted value cannot explain working protection. Automatic resumption means
the former fixture no longer left that component unsent after reconciliation.
The complete local kernel suite passes 316 cases.

Independent review accepted the complete round5 repair, independently running all
309 then-current cases. It separately accepted the final cancellation-classification
follow-up after running 31 affected cancellation/orphan cases, including preserved
allocated exposure and fill races across restart. Final coordinator validation:
893 ops passed, 13 skipped, two existing seaborn warnings; focused lint 9.80/10;
mutation control 316 passed, with all five mutations detected (81, 3, 1, 3 and 11
failures respectively). The final check-tier run passed, with normal public-worktree
skips for private artifacts. Integration hooks and the requested remote review are
tracked against the pushed revision in the babysit ledger and PR conversation.

### Codex follow-up to `bafdd97`

Codex reported five comments representing four distinct findings: retained MODIFY
used pre-restart evidence, first ATTACH published a durable prefix, incomplete
trailing fields were accepted, and familiar entry references bypassed risk-field
validation. All were reproduced before repair (initial run: 20 failures, 3 passes).
The round6 suite now contains 46 cases with literal accounting and broker outcomes.

The provenance repair checks the persisted original PLACE authority against actual
order fields and immutable broker-origin execution records before crediting a fill.
Each order must fund its own executions. Terminal orders remain checked, and lot
reads cannot grow allocation. A persistent quarantine owns mismatches without
fabricating adapter fills. It retains reserve until coherent terminal evidence and
retains ambiguous verified allocation until consumption. `CONTRACT.md` explicitly
records the new offline L-1 guarantees, global order-location registry and schema 3;
these are not claims about the current live telemetry producer.

Independent review reproduced and closed related issues in foreign-symbol absence,
contradictory terminal/working facts, conflicting execution histories, and mixed
side/symbol lot recovery. Added regressions cover each, including a conflict arriving
after earlier quarantine and surviving restart. Broker lots preserve actual execution
identity; mixed-side bounded, fill-scoped or partial close execution refuses before
mutation, while full atomic symbol recovery can consume the scope. Conflicting
immutable identities remain subject to attended resolution.

Independent review accepted the complete bounded offline candidate and independently
ran all eleven kernel suites: 362 passed. Coordinator full-ops verification: 939
passed, 13 skipped, two existing seaborn warnings. Focused pylint: 9.73/10, exit 0.
`git diff --check` and final check-tier gates passed, with normal public-worktree
skips for private artifacts. The isolated mutation control passed 362 tests; all
five mutations were detected (81, 3, 1, 3 and 11 failures respectively). Integration
hooks are tracked in the babysit ledger. Remote CI and the requested Codex review
apply separately to the pushed revision.

### Production disposition

The local offline redesign is implemented and reviewed. The production-reference
acceptance hold remains pending operator disposition; this record does not approve
the current GitHub PR or merge it. Remote CI and Codex review results are recorded
on PR #365 against each pushed head; the results above are local verification.
Live L-1 equivalent evidence/request ordering, L-2 validation, production disarm
acknowledgment and the existing feed-loss ratification are still explicit dependencies.
`CONTRACT.md` states the model refinements that the owning spec and TB-I3 must carry.
