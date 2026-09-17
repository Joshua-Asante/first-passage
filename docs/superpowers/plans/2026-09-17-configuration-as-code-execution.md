# Configuration completion execution

Base: `6a3d4b37c9ce24e3726765d01a6804cae1976f59` (merged PR 417).
Isolated branch: `codex/configuration-as-code-completion`, at
`C:/Users/joshu/multi_firm_operations/.worktrees/configuration-as-code-completion`.
Implementation remains uncommitted. Original checkout and unrelated local work
are preserved. The supplied plan and requirements were copied byte-for-byte;
their SHA256 values are respectively
`6DA54A4E06160785474853F7988C945EFD96457DB975B3607A6D0D3D42E46B44` and
`39EE8452E967B6D6A56BD15C2E2C1CD9A6CF25C0651A25D5CC830CF409283DFB`.
This record supplies execution dispositions without rewriting those documents.
AGENTS combines local configuration guidance with merged verification guidance.
No deployment, skill publication, commit, PR or merge was performed.

## Bounded designs and dispositions

| Packet | Disposition | Net bytes, including packet tests/design |
|---|---|---:|
| 1 Retrieval | Implemented; ownership improvement | +790 |
| 2 Link policies | Root/nested sharing implemented; skill sharing deferred | +1704 |
| 3 Instrument facts | Implemented; ownership improvement; full shell qualification pending | +2523 |
| 4 Test factories | Deferred after measured feasibility | 0 |
| 5 Scan profiles | Deferred after measured feasibility | 0 |
| 6 Hook matcher | Implemented; byte saving | -88 |
| 7 Image-test profiles | Implemented; ownership improvement | +1886 |
| 8 Brief validators | Designed and implemented; byte saving | -4484 |

1. **Retrieval:** ordered frozen `CorpusSource` objects live in the existing
   module. Mode/limit validation occurs when collected. The dispatcher preserves
   catalog ACTIVE/HOLD special rows, source order, overlapping brief-index
   chunks, session and header limits, missing files and cold exclusions. Removed
   unused hand-maintained HOT_FILES after searching callers. Synthetic markers,
   real SQLite rebuild/query and full-corpus differential comparison pass.
   **Requirements discrepancy:** base compares `name.upper()` with `INDEX.md`
   and `TOMBSTONES.md`, so neither exclusion matches. Preserve actual ADR
   membership; repairing that pre-existing bug is a separate behavior change.

2. **Link policies:** a small scripts-local helper owns equivalent Markdown
   extraction, path-shape primitives, root/document target resolution and
   Git-ignore invocation. Consumers retain traversal, cache scope, fallback
   probes, counting/history differences and messages. External-cwd isolated
   root CLI and existing file-spec imports pass. The skill checker is restored
   exactly to base: revision-release validation stages that script by itself.
   Sharing its two constants would require additional staging machinery and
   tests for roughly 61 saved bytes. That boundary is explicitly deferred;
   skill-specific fences/templates/tombstones/fallbacks remain independent.

3. **Instrument facts:** production cost resolver, fee rows and slippage were
   inspected before design. `core/instrument_specs.py` owns unchanged frozen
   geometry records; the existing mutable mapping seam and exact numeric types
   remain. Explicit commission-category bindings replace two authored sets;
   compatibility views are derived, and production checks consume the binding.
   Invalid categories and missing geometry/classification still fail closed.
   The now-impossible overlap synchronization check becomes an invalid-category
   mutation test. Slippage maps leg IDs to MYM/MNQ geometry without changing
   offsets, thresholds or firm fees. Docker COPY, context allow-list, listener
   exact inventory and pre-commit gate trigger include the new source. Numerical
   and packaging expectations remain independently authored. Actual Linux image
   inventory/import qualification passed; the complete original listener shell
   lifecycle was not run (environment boundary below).

4. **Test factories:** inspected the four designated suites and their existing
   local factories. The bounded candidate separates transport rail and daemon
   schemas, requires clocks/arming and scenario flags, replaces nested values
   whole, and deep-copies caller state. HTTP/file-backed configuration stays
   distinct; malformed and omitted-field tests stay literal. Only 1035 setup
   bytes are removable, versus 988 factory bytes plus 794 isolation-test bytes:
   **+747 before consumer wiring/documentation**. The isolation probe passed.
   Retain existing local factories; no speculative abstraction is shipped.

5. **Scan profiles:** audited boundary component exclusions, Markdown directory
   parts and falsifier prefix rules plus its tracked/local union. A differential
   membership matrix includes root/nested caches, research environment,
   `.worktrees`, `.claude/worktrees`, ordinary `.claude`, near-prefix siblings,
   tracked caches and ignored local vendor inputs. Preserve asymmetries, including
   the falsifier's existing leading-dot stripping behavior. The removable lists
   total 430 bytes; the validated immutable profile/composition candidate is
   1363 bytes: **+933 before wiring/tests/documentation**. Keep local constants;
   no profile module or ignore-file generator is shipped.

6. **Hook matcher:** combine identical PostToolUse matchers into one record with
   both complete, independent handler objects. PowerShell JSON comparison
   confirms matchers, all handler fields and every other section, including
   PreToolUse and permissions, are unchanged. Installed Claude Code is 2.1.263.
   The official hook-handler reference supports independent matching handlers
   in one array; array order is not an execution-order promise. Static
   compatibility only: no live hooks fired. Reference checked 2026-09-17:
   https://code.claude.com/docs/en/hooks#hook-handler-fields.

7. **Image-test profiles:** frozen service profiles share COPY parsing and graph
   traversal. Each service retains its import-name extractor, module resolver,
   entrypoints and path-normalization behavior. Daemon package-relative imports
   and initializers are tested with an independently specified miniature graph;
   missing COPY coverage remains a negative assertion. Existing nonempty closure
   and historical missing-module pins, isolated packaged-book test and shell
   inventory check remain. The slippage isolated-import test added for Packet 3
   is counted here once because it lives in the listener image-test file. This
   consolidation improves ownership but does not save total bytes.

8. **Brief validators:** the explicit matrix and standalone import design were
   written before extraction in
   `docs/superpowers/specs/2026-09-17-brief-validator-sharing.md`. The skill-local
   engine owns equivalent parsing and numbered checks; profiles accept the
   wrappers' distinct empty-body predicates and required-section tuples.
   Nonidentical checks, aliases, inference precedence, output formatting, exit
   codes, NOT CHECKED and closure DELEGATED behavior stay local. Absolute file
   loading uses the repo-local engine for the repo wrapper and sibling engine
   for standalone skills, never an installed home copy or ambient PYTHONPATH.
   Standalone temporary copies exercise all seven templates, list-checks,
   self-test and input errors with isolated Python. Old/new API and CLI outputs
   match across synthetic documents, templates, accepted types and format
   variants. No generic rule language, extra generated copy or publication.

Preserved program deferrals: dispatch wrappers; Fly/packaging generators;
frozen research costs, manifests and results; policy authority; independent
numeric and packaging checks. No account, secret, arming or live-service edits.

## Environment and verification evidence

Both execution and clean comparison checkouts passed their own `fp.ps1 doctor`.
Windows PowerShell 7.6.6; operations Python 3.13.2 at
`C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`, 62 locked
packages. Each record includes its exact command, interpreter and before/after
working-tree fingerprint. Source and Git state remained unchanged during each
recorded run. Record paths below are relative to `.cache/fp-verification/`
unless explicitly qualified. The records retain stdout/stderr and JUnit where
applicable; the ignored probes and raw records are local evidence, not added
source bytes.

| Evidence | Record | Actual result |
|---|---|---|
| Focused baseline, all packet suites | `20260917T141600Z-c47c80b4eb53/record.json` | 332 passed, 1 skipped |
| Baseline `fp.ps1 check` | `20260917T141716Z-5efbd6b03b9b/record.json` | completed, exit 0 |
| Retrieval | `20260917T142047Z-0f43a33c382d/record.json` | 11 passed |
| Root/nested/skill link contracts | `20260917T142221Z-0313014c4492/record.json` | 37 passed; broader staging defect corrected below |
| Image profiles | `20260917T142505Z-f1b391adde12/record.json` | 10 passed |
| Cost/slippage/image suites | `20260917T142750Z-3b1acfc8eede/record.json` | 71 passed |
| Both brief contract suites | `20260917T143056Z-5ba3a833ee0a/record.json` | 96 passed |
| Old/new retrieval, links, briefs and scan membership | `20260917T143222Z-f8190bdfe08c/record.json` | 4 passed |
| Factory feasibility/isolation | `20260917T143411Z-04e4d3ce7899/record.json` | 1 passed |
| Integrated check before review fixes | `20260917T143928Z-ef5ac5b1dc85/record.json` | completed, exit 0 |
| Review gate-trigger regression before fix | `20260917T145252Z-f7883bd53a55/record.json` | expected 1 failed, 3 passed |
| Review fixes: skill release, links, gate selection, cost model | `20260917T145333Z-a7a16db9a73d/record.json` | 177 passed, 4 skipped |

All passing rows were inspected for completed status, verification exit 0,
stable source, complete capture and empty report errors. Exact selected pytest
paths are in each record's requested_command; all used the checkout launcher.
Execution probes: `.cache/test_compare_contracts.py`,
`.cache/test_factory_candidate.py`; feasibility counts:
`.cache/feasibility.json`. Final aggregate selected-suite/check records and
results are indexed in `.cache/configuration-final-verification.json` after
this documentation is finalized.

Linux Docker focused command:
`tools/local_verification/run.ps1 -Workers 2 -TestPath` with cost-model, slippage
and both image-manifest suites. Record:
`.cache/fp-docker-verification/20260917T143447Z-6e322d643e7f/record.json`.
Python 3.11.16: **71 passed**, completed, verification exit 0, source stable,
capture complete, report errors empty and Docker cleanup successful. Its
coverage warning concerns an unexecuted default coverage target; no coverage
percentage is asserted.

Actual listener recipe build and isolated exact-inventory/slippage-import probe:
`fp.ps1 python .cache/verify_listener_image.py`, recorded at
`listener-image-75a75f25a34c/record.json`. Python 3.12.14 in Linux; exact inventory
52 files; MYM/MNQ tick sizes 1.0/0.25. Completed, verification exit 0, stable
source, complete capture, no report errors; test container and unique image tag
removed successfully. Image ID:
`sha256:fc5f234683064af9386ce0bde67de550d583c8c7420f5c530ab1d4a6454fc2c7`.
This was local qualification with no deployment or live-service mounts.
**Unverified boundary:** `scripts/c1_image_validation.sh listener` in full was
not run. Installed Ubuntu WSL has no enabled Docker integration. The supported
repository Docker runner and Windows Docker Desktop could qualify the focused
suites and actual recipe, but those do not constitute the entire shell lifecycle.

## Full-suite result and review closure

`fp.ps1 --workers 2 test -q`:
`20260917T143503Z-f9205b516e7b/record.json`. Pytest stdout reports **5953 passed,
76 failed, 70 skipped, 48 subtests passed**. The recorder correctly reports
failed/exit 1, stable source and complete capture, and additionally rejects the
JUnit aggregate because its count does not match testcase outcomes. This is
not a passing verification record; its zero parsed summary is not a zero-test
result. Full-suite acceptance remains non-green.

Twenty-four failures exposed the added skill-parser dependency at the staged
revision-release boundary. Restore the skill checker exactly to base instead
of extending release machinery. Clean-base `tests/test_sync_skills.py` passed
86 tests with 4 skipped in the separate untouched baseline worktree, record
`.worktrees/configuration-as-code-baseline/.cache/fp-verification/20260917T144513Z-75ef2745623e/record.json`
(relative to the original checkout). The corrected candidate is covered by the
review-fix run above; no actual skill publication occurred.

The other **52 failures reproduce on untouched 6a3d4b3**, with exact equality of
failed node IDs: 46 agent-handoff tests denied writes under the user's external
`.cache/agent-handoffs`, and 6 image-validation fault-injection tests fail when
Git Bash cannot create `/c/Users/joshu` during cleanup. Comparison command:
`fp.ps1 --workers 2 python -m pytest tests/test_agent_handoff.py tests/scripts/test_c1_image_validation.py -q`.
Result: 52 failed, 34 passed, 6 skipped, stable source; baseline record:
`.worktrees/configuration-as-code-baseline/.cache/fp-verification/20260917T145203Z-6c4e0f00309b/record.json`.
These environment failures and the aggregate report mismatch remain disclosed;
neither unrelated runtime code nor the evidence recorder was changed to hide
them. The full suite was not rerun after the bounded review fixes; affected
suites were rerun instead.

Independent read-only review found two defects: the skill staging dependency
and omitted `core/instrument_specs.py` gate trigger. Both are resolved. The
reviewer verified the skill script has no Git diff and actual pre-commit
selection now includes all four relevant paths. No outstanding actionable
review findings. Standard check advisories still include absent private/Pine
inputs and historical notices; a gate exit 0 does not validate absent inputs.

## Exact byte accounting

Compared base Git blob bytes with candidate Git-clean bytes, verified against
`git hash-object --path` without staging. Added source/test/documentation files
count in full, including both originally untracked carried documents. Windows
CRLF expansion, worktree copies, ignored caches and runtime evidence are excluded.
No generated or packaged duplicate source files are introduced. Reproduce with
`fp.ps1 python .cache/account_bytes.py`; per-file blob IDs and byte counts are
in `.cache/configuration-byte-accounting.json`.

| Category | Net bytes |
|---|---:|
| Production/configuration | -11134 |
| Tests/fixtures | +10107 |
| Documentation/records | +63190 |
| Generated/packaged copies | 0 |
| **All changed candidate files** | **+62163** |

Packet changes total **+2331 bytes** including Packet 8's design. Program-level
documentation and AGENTS add **+59832 bytes**. Of that, the carried plan
and requirements alone add **43638 bytes**. Gross reductions across shrinking
files are **24402 bytes** (sum of negative per-file deltas, not a claim that all
deleted lines were duplicate code). Tests and documentation are not omitted to
make savings appear larger. Packet 6 and Packet 8 save bytes; the overall change
does not. Independent expectations and historical artifacts were retained.
