# `scripts/` — gates and discipline CLIs

## Local operations launcher

For slow local hosts, set `FP_QUALIFICATION_CHILD_TIMEOUT_S` to an integer from 3600 through 14400 seconds (default 3600); invalid or empty values fail, and CI leaves it unset.
Use the launcher from the checkout you intend to test. In PowerShell 7.3+:

```powershell
.\fp.ps1 doctor
.\fp.ps1 test-ops -q
.\fp.ps1 test -q -k gate_manifest
.\fp.ps1 check
.\fp.ps1 python -m pytest tests/test_fp_launcher.py -q
.\fp.ps1 python -m pip check
```

The portable equivalent is `python -I scripts/fp.py doctor` (or any command
above). Bootstrap Python needs only its standard library. Tasks use the selected
operations virtual environment, not bootstrap Python. The launcher always runs
tasks from its own checkout root, even when invoked by absolute path elsewhere.

Environment selection, in order:

1. `--env PATH` before the command, e.g. `.\fp.ps1 --env C:\envs\fp-ops doctor`.
2. `FP_OPS_ENV`, if set.
3. This checkout's `tmp/ops-env`.
4. For a linked Git worktree without a local environment, the main checkout's
   `tmp/ops-env`.

Relative explicit paths resolve from the invoking directory. Invalid explicit
or existing local environments fail rather than falling back. The launcher does
not use `.venv`, install packages, or modify global PATH. Create a separate venv
with a supported Python and install `requirements-ops.lock` with `--require-hashes`
if an environment is missing. Select it with `--env` or `FP_OPS_ENV`. Full test runs
(`test`, `test-ops`) also need the shared verification supplements in
`tools/local_verification/requirements-extra.txt`, which CI's `tests.yml` installs on
top of the lock. Without its `cryptography`, signed settlement tests skip. Whole-suite
runs leave out the retired qualification suite (`tests/ops/conftest.py`).

Before each command, the launcher checks that the interpreter starts, the venv
excludes system site-packages, and all locked distribution versions match this
checkout. `doctor` reports the interpreter, matched package count, and optional
signing dependency. This is a version check, not a package-file integrity check,
full import test, or guarantee of matching CI's operating system/Python version.

Child processes receive the venv executable directory first on PATH, VIRTUAL_ENV,
and disabled user site-packages; inherited PYTHONHOME/PYTHONPATH are removed.
The caller's shell remains unchanged. Python gates explicitly use the gate
runner's `sys.executable`, because Windows may resolve bare `python` subprocess
names to a base installation before consulting PATH. Custom Python scripts
should also use `sys.executable` for nested Python, or resolve an executable
explicitly with `shutil.which`; the launcher cannot rewrite arbitrary scripts.

`test` runs `tests/`, `test-ops` runs `tests/ops/`, and `check` invokes the existing
manifest runner with `--tier check`. Subsequent arguments pass through unchanged;
use `python -m pytest <paths>` for an exact test selection. Child exit status is
returned; launcher setup failures return 2. Environment version mismatches block
execution, so use the selected interpreter directly to repair its dependencies.

### Automatic verification evidence

`test`, `test-ops`, `python -m pytest ...`, and `check` automatically create a
unique ignored `.cache/fp-verification/<timestamp-id>/` directory. Output streams
remain visible and are retained alongside `record.json`. The record identifies
the exact command, interpreter, locked versions, commit, dirty diff, hashes of
tracked/nonignored untracked files, before/after source state, duration and exit
status. Pytest adds `junit.xml` with counts, failures and skip reasons. An explicit
user JUnit destination is preserved and its bytes are also retained in the evidence
directory. Expected reports must exist, be refreshed by the run, parse correctly,
and have counts consistent with testcase outcomes. `test_summary` contains collected,
passed, failed, error and skipped counts; report errors prevent acceptance.
Gate results remain in the full stdout/stderr logs and do not require JUnit.

Recorded local and Docker pytest commands load `scripts.pytest_junit_subtests`.
The locked pytest 9.1.1 producer counts subtests but otherwise reuses their
parent's XML node. This adapter emits separate, uniquely named testcase elements
for those outcomes and retains ordinary parent/setup/teardown reporting. The
recorder still rejects mismatched counts and contradictory outcomes. Its summary
counts JUnit testcases, including subtests; pytest's terminal summary reports
parent tests and subtests separately. Custom JUnit destinations remain supported.
The adapter uses the pinned pytest producer API; run its process regressions when
updating pytest. Reports are retained as produced, not repaired after validation.

Agent-handoff and image fault-injection process tests opt into `isolated_home`.
Their Python and shell children share temporary home/cache storage outside the
worker workspace. This changes test environments only; production receipts and
locks still use the real home directory. Fixture environment overrides are
restored afterward, and the launcher owns temporary-tree cleanup.

Schema version 2 reserves `record.json` before environment checks, then atomically
replaces it as the run advances through `not_started`, `running`, and a final
`completed`, `failed`, or `interrupted` state. A setup failure stays `not_started`
with its error and nonzero verification result. A hard kill can leave `running`
with a null result; that is incomplete evidence. A missing bootstrap interpreter
or unwritable evidence directory cannot produce a record and fails visibly.

The printed record path is the evidence to cite. Child failure codes are retained;
a successful child with source drift returns 3, and incomplete output capture
returns 4. Invalid expected reports return 5, failed Docker cleanup returns 6,
and interruption returns 130. Only `completed` with verification exit zero is
acceptance. Pipe draining stops three seconds after the direct child exits if a
descendant retains its handles; the record then rejects acceptance. The recorder
does not kill unrelated/background descendants. Keep files, index and HEAD stable
while checking. Ignored inputs and external services are not fingerprinted;
records describe the selected run, not all repository behavior. These local
artifacts are not committed or uploaded automatically. `doctor` and arbitrary
Python commands do not create verification records.

For faster focused feedback, use the existing pytest-xdist installation:

```powershell
.\fp.ps1 --workers 2 python -m pytest tests/test_record_verification.py tests/test_fp_launcher.py -q
```

Workers are opt-in, bounded from 0 through 8, and use `loadscope` to group each
module/class on one worker. Use 0 for serial execution. Startup overhead and
imbalanced modules can outweigh parallelism; measure the same selection before
choosing workers. Tests with shared resources may need serial execution.

### Detached runs

Long recorded suites (for example `tests/ops/qualification`, over 90 minutes) get
hard-killed when they are started from an agent tool that imposes a time limit on
its own command, which leaves the record `running` and unusable. `--detach`
starts the same recorded run as an independent background process and returns at
once:

```powershell
.\fp.ps1 --detach python -m pytest tests/ops/qualification -q
```

It is a launcher-level option given before the command, like `--workers`, and it
applies only to recorded commands (a pytest task or `check`); anything else is a
usage error. The parent creates no record of its own and never waits. It prints
exactly two lines, `record: <absolute evidence directory>` and `pid: <child pid>`,
and writes `<identity>.detach.json` (child pid, record directory, log path, child
argv, UTC start time) plus `<identity>.detach.log` (the child's combined stdout
and stderr) in `.cache/fp-verification/` beside the evidence directories. On
Windows the child starts in a new process group without a window and breaks away
from the caller's job when that job permits; if the breakaway is refused the
launcher warns that the run may end with the caller. On POSIX the child starts a
new session. The detached child reuses the reserved record identity through
`FP_VERIFICATION_ID`, which is removed from the environment handed to the task's
own children; a launcher run honors it only as an unused reservation (its
`.detach.log` exists and its record directory does not), and refuses a nested
`--detach`. The child's arguments are rebuilt from the parsed options, with a
relative `--env`/`FP_OPS_ENV` resolved against the caller's directory; launcher
options are never abbreviated. Completion is still judged only from `record.json` as before: poll
it, and accept nothing but `completed` with verification exit zero.

### Azure VM deallocation watcher

Standing rules: [Azure compute VM policy](../docs/governance/azure-compute-vm-policy.md).

The session that starts the Azure compute VM verifies `VM deallocated` before its
turn ends (Joshua, 2026-10-24). For runs of up to 12 hours, keep the PC plugged in
and this watcher running for the whole allocation, started before or right after
the VM starts (with Joshua's `az login`):

```powershell
.\fp.ps1 python scripts/azure_vm_watch.py --hours 6
```

It only reads power state and calls `az vm deallocate`. It deallocates at the
deadline, at the weekly dollar cap (default $125 at $2.90/h, counting only time
it watched, by UTC week from Monday), when the VM is stopped but still allocated,
or after 10 minutes of unreadable power state. It keeps the PC awake while it
runs, exits 0 once the VM is verified deallocated or has not started within the
grace period, and exits 2 with `.cache/azure-vm-watch/ALARM.txt` if deallocation
cannot be verified. Run one watcher per VM; it never prints the subscription ID.

## Agent CLI dispatch

`dispatch_claude.ps1` (receipts and return validation; see `agent_handoff.md`) and
`dispatch_codex.ps1` (thin Codex wrapper):

```powershell
.\scripts\dispatch_codex.ps1 -Worktree <worktree> -Prompt 'Read TICKET.md and execute it.' -OutputFile <scratch>\last.txt [-Sandbox read-only] [-Model gpt-6.1-sol] [-DryRun]
```

It runs the Codex app's bundled `app\resources\codex.exe` (the `.sandbox-bin` copy cannot run tools),
passes `FP_AGENT_GH_TOKEN` as `GH_TOKEN` to the child only, and refuses a directory containing `.env`.
Tests: `tests/scripts/test_dispatch_codex.py` (dry-run).

### Merge train

`merge_train.py` is the read-only gate and watcher used by the [merge-train skill](../.claude/skills/merge-train/SKILL.md), which owns how to use it:

```powershell
.\fp.ps1 python scripts/merge_train.py gate 912 913      # READY / WAIT / HOLD; exit 0 only if all READY
.\fp.ps1 python scripts/merge_train.py watch --min 911   # NEW / CHANGED / CLOSED / STALLED lines
```

`dispatch_codex.ps1 -ReviewBase origin/main` runs the read-only Codex CLI review fallback. Tests: `tests/scripts/test_merge_train.py` (a fake `gh`; no network) and `tests/scripts/test_dispatch_codex.py`.

## Gate composition and admission

Composition authority is [`gates.yml`](gates.yml) via
[`gate_manifest.py`](gate_manifest.py).
Do not hand-maintain a parallel list.

[Evidence store](evidence_store/README.md) provides opt-in source preservation,
decision history and declared-dependency correction queries:
`python -m scripts.evidence_store --help`. It is advisory governance tooling.

The manifest's complete tier set is `always`, `path-conditional`,
`data-conditional`, and `audit`. The runner refuses unknown tiers (including the
retired `soft`) and declared/parsed gate-count mismatches, so bad indentation or
an unclaimed tier cannot silently remove a gate.

| Entry point | Selection |
|---|---|
| pre-commit | `always`, plus path/data-conditional gates whose staged-path regex matches |
| `make check` / `--tier check` | All `always` and `path-conditional` gates, plus forced `data-manifests` |
| `make validate` / `--tier validate` | `data-manifests` (forced) and `pine-manifest` only |
| `make audit` / `--tier audit` | `audit` diagnostics only |

[`pre-commit`](githooks/pre-commit), [Make](../Makefile) and the
[CI workflow](../.github/workflows/gate-manifest.yml) call the runner. H6's CI
composition work was discharged on 2026-08-23; CI invokes `--tier check`.
Separate CI checks and the public clone's absent-data handling remain with their
workflows/checkers; composition is not a claim about every merge requirement.

A blocking commit/required-CI gate must protect executable correctness,
non-regenerable evidence, a live-money invariant or the integrity of a changed
artifact; the violating change must select the check; and a finding must return
non-zero and change the verdict. A report-only command belongs in `audit`, however
important its subject. Audit promotion requires a clean baseline, a non-zero
failure mode and a reachable trigger; a gate that becomes report-only moves back
to audit. The original W5 no-gate-dropped landing criterion is completed history,
not a permanent requirement to retain every gate.

Reachability includes every path class that can introduce the violation, including
moving/deleting a referenced target. Matching only the file containing its link
is insufficient. Before a path-conditional re-tier, add the relevant probes to
[`test_path_conditional_gates_are_reachable`](../tests/test_gate_manifest.py).

`m1-artifact-structure` stays blocking (`always`): the
[acceptance validator](validate_c1_monitoring_acceptance.py) rejects unreadable or
invalid artifacts, missing required fields, invalid status and secret violations.
It does not grant arm authority.

```text
python scripts/gate_manifest.py --list
python scripts/gate_manifest.py --list --all-tiers
make check          # same runner, check tier
make audit          # report-only diagnostics
make validate       # data manifests + pine
```

Install or refresh hooks using `bash scripts/install_hooks.sh` (Git Bash on
Windows), or `scripts/install_hooks.bat` on Windows. Shell hook templates and
the shell installer are LF-pinned for fresh Windows checkouts.

All four hooks bootstrap through `python -I scripts/fp.py` from the checkout
where Git invoked them. Bootstrap Python needs only stdlib; check consumers use
that checkout's validated operations environment. Run `fp.ps1 doctor` first and
see [Local operations launcher](#local-operations-launcher) for environment
selection. Blocking hooks refuse an invalid environment. Advisory post-merge
prints an explicit warning and makes no repair when its environment preflight
fails; it cannot undo an already completed merge.

Installed hooks live in the common Git directory and affect linked worktrees.
Updating templates does not silently overwrite installed hooks. Before
refreshing them, ensure active checkouts contain the launcher and have a valid
environment; older checkouts without it will fail explicitly. Installation
tests use disposable repositories and do not change your shared installed hooks.

Per-script layer classification is owned by `scripts_layer` in
[`repo_map_layers.yml`](repo_map_layers.yml), which `check_boundaries.py` loads.

### Installing the check dependencies

Local clones and CI install the hash-pinned lock with:

```text
python -m pip install --require-hashes -r requirements-ops.lock
```

On a Debian-based remote container, such as Claude Code on the web, that
command can abort before it installs anything (observed 2026-09-15):

```text
ERROR: Cannot uninstall PyYAML 6.0.1, RECORD file not found. Hint: The package was installed by debian.
```

Apt-owned packages in `/usr/lib/python3/dist-packages` carry no pip RECORD, so
pip cannot uninstall one whose version differs from a lock pin, and the whole
run stops. `markdown_it` then stays missing and the check tier cannot run.
PyYAML is only the first collision; a per-package fix does not hold. Use this
once per fresh container:

```text
python -m pip install --require-hashes --ignore-installed -r requirements-ops.lock
```

Hash checking stays on. Every pin is written to
`/usr/local/lib/python3.X/dist-packages`, which precedes the apt copies on
`sys.path`; no apt-owned file is touched. Add `--break-system-packages` only if
pip reports `externally-managed-environment`. After one such run the plain
command is a no-op on that container; after a lock bump on a reused container,
use the plain command. Do not change the lock pins to match the apt versions.
GitHub Actions runners use `setup-python` and never see this. If the install
should be automatic on Claude Code on the web, it belongs in that environment's
setup script, which runs once and is cached, not in a SessionStart hook in
[`settings.json`](../.claude/settings.json).

## Private evidence archive

A public record may pin a private file's SHA-256 (vendor CSVs, Pine source,
private receipts); the pin proves which bytes were used but keeps no copy
([M-41](../docs/methodology/lessons/methodology_lessons.md#m-41--private-artifacts-inside-a-worktree-die-with-the-worktree)).
[`evidence_archive.py`](evidence_archive.py) keeps the second copy in the private
`first-passage-archive` repository, content-addressed under `evidence/sha256/`.

- `python scripts/evidence_archive.py put <file>...` copies and verifies each file
  into a local clone of the archive, then prints the commit/push commands; the
  copy is safe only once pushed. `--pinned` archives every pinned file present in
  this checkout. It refuses a clone whose `origin` is not the archive.
- `python scripts/evidence_archive.py audit` reports each pinned digest as ARCHIVED, UNPUSHED or MISSING; `--verify` re-hashes.
  Without an archive clone it prints UNVERIFIED and exits 0.

Pins are read from tracked `*SHA256SUMS` / `*MANIFEST.sha256` files and from
[`docs/evidence/PRIVATE_EVIDENCE.sha256`](../docs/evidence/PRIVATE_EVIDENCE.sha256),
where a record pinning any other private file registers it in the same commit.
The archive clone is `--archive`, `$FP_EVIDENCE_ARCHIVE`, or a
`first-passage-archive` directory beside this checkout.

## Independent review

Review is cross-agent: Codex reviews Claude's work and Claude reviews Codex's (Rule 5;
[surface-allocation ADR Addendum 2026-10-26](../docs/adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-10-26--operator-ruling-cross-agent-review)).
The merge rule and review limit are
[Addendum 2026-10-24b A](../docs/adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-10-24b--operator-rulings-conditioned-merge-go-and-credential-custody),
applied by `merge_train.py gate`; requesting reviews is [merge-train](../.claude/skills/merge-train/SKILL.md) step 3.

[The pre-ratification workflow](../.claude/workflows/pre-ratification-adversarial-panel.js)
owns its review mechanics. Reviewers assess the source independently of the proposer's
reasoning; synthesis is advisory and cannot supply operator ratification or execution
authority. A Claude panel on Claude work is optional author input, not the independent
review: the other agent owns that (Rule 5). Reviewer/delegate assignment never grants permission to edit locked surfaces.

Its existing GRAND-only safety scan reads committed target text. A safety-invariant
citation flags a hard block on synthesis; missing text flags a coverage failure, also
blocked. Keep its fail-closed, deliberately sensitive behavior; STRATEGIC calls do not
gain this scan. The implementation owns the matching rules. This review check does not
replace [M1 acceptance validation](validate_c1_monitoring_acceptance.py), live execution
authorization, or the [production protection checks](../core/dd_protection.py).

Risk/sizing, validation, gate composition, brief compliance, research dedup and operational
oversight remain with their existing code/skill/rule owners. Removing a review mechanism
does not weaken those controls or commission new reviewer roles. New functions need
demonstrated coverage; do not assume every judgment can be reduced to a mechanical check.

### Checkout configuration and external tests

All launcher pytest routes (`test`, `test-ops`, `python -m pytest`) supply
`-c <selected checkout>/pyproject.toml` and `--rootdir=<selected checkout>`.
Equivalent explicit split/equals options are accepted and normalized; conflicting
options fail before pytest starts. Relative options resolve from that checkout,
even when invoked from another directory. `PYTEST_ADDOPTS` is expanded into the
recorded command and subject to the same checks. Deliberate `-o` overrides remain
available and recorded. This selects pytest configuration/import roots; it does
not sandbox imports or prohibit deliberate import-path overrides.

Explicit external test files, including `file.py::test_name` selections, have
SHA-256 hashes recorded before and after execution. A changed or missing file
prevents acceptance (exit 3). External supporting imports/data and directory
contents are outside that inventory unless separately captured. Existing custom
JUnit destinations are outputs, not source inputs. An unchanged scratch test does
not establish an unchanged dependency closure.

### Advisory progress

The recorder prints a heartbeat every 30 seconds while a child is running. Missing,
invalid or stale observations say `test activity unavailable`. Observed active IDs,
completed count, collected count and observation age describe pytest activity;
completed does not mean passed, and elapsed time never triggers termination.
`--progress-interval` on the generic recorder can change the positive finite
interval; the launcher uses the recorder's canonical default.

The launcher explicitly loads `scripts.pytest_progress` and passes its unique run
identity/evidence directory. Each xdist worker atomically writes its own
`progress-gw*.json`. The controller aggregates distinct node IDs from forwarded
pytest hooks into `progress.json`; it never needs competing worker writes to that
file. Completion is observed after teardown, including setup failures and skips.
Worker crashes can leave active/incomplete worker snapshots. Counts and IDs are
advisory, never acceptance evidence. Snapshots retain at most 64 active and 64
completed IDs, 200 characters each, with a truncation flag; exact final outcomes
still come from validated JUnit. Supervisor heartbeats are excluded from retained
child stdout/stderr. Existing pipe draining, interruption and cleanup rules remain.

### Separate baseline and implementation checkouts

Resolve and verify an exact baseline before creating isolation. Prefer native
worktree tooling when available; otherwise, from the parent repository:

```powershell
$baseline = git rev-parse --verify 'origin/main^{commit}'
git show --no-patch --format=fuller $baseline
git check-ignore .worktrees
git worktree add --detach .worktrees/test-baseline $baseline
git worktree add -b codex/my-change .worktrees/my-change $baseline
```

Use unique owned paths. Register each baseline's absolute path, commit, owning
run and evidence directory in the task's retained evidence ledger. Invoke each
checkout's own launcher from that checkout:

```powershell
.\fp.ps1 doctor
.\fp.ps1 --workers 2 python -m pytest tests/test_fp_launcher.py tests/test_record_verification.py -q --tb=short
```

Each doctor must validate that checkout's lock. A shared validated environment is
allowed only while unchanged throughout both runs; dependency changes require
separate environments. Start with the affected baseline selection. Run a broad
baseline only to resolve a concrete attribution question. Baseline work can run
while implementation proceeds in the other tree, if CPU/memory contention permits.
Never edit the measured checkout, its index or HEAD during a run. During development,
run affected tests; after edits stop, run planned regressions and required gates.
Baseline evidence applies only to its recorded revision, inputs and environment;
it is never candidate acceptance evidence.

Before removing a baseline, require a terminal run, no live child, retained
finalized evidence outside the worktree and a clean owned tree (including review
of ignored resources). Then use `git worktree remove <exact registered path>`.
Never force-remove dirty or unowned worktrees. Reconcile interrupted/uncertain
runs first; retaining an owned baseline with its evidence is safe.

Caller inventory for this migration: `fp.ps1` delegates to `scripts/fp.py`;
`tools/local_verification/run.ps1` delegates to `scripts/docker_verification.py`,
which invokes pytest directly. Make test targets and GitHub test workflows also
invoke pytest directly and retain their existing environment contracts. The generic
recorder continues to accept arbitrary commands without pytest argument injection.
No maintained launcher config workaround or older progress plugin was found to
remove. Ambient launcher root discovery is retired; direct pytest callers, the
JUnit adapter, Docker ownership/cleanup, suite defaults and historical records
are retained. Rollback reverts code while retaining old/new evidence; records
with the original root-selection defect remain unsuitable for their claimed scope.

Argument files (`@path`, including nested files and `PYTEST_ADDOPTS`) are expanded
before checkout validation and external-file inventory. They follow pytest's
one-argument-per-line convention and resolve relative paths from the selected
checkout. The recorded child command contains expanded arguments, and external
argument files are also inventoried. Cycles, more than 16 nesting levels, files
over 1,000,000 characters and expansion over 100,000 arguments fail before launch.
Equivalent `--rootdir` values use pytest's environment-variable expansion before
comparison. A JUnit destination overlapping a selected file (including symlink
or hardlink aliases) is rejected before it can overwrite source. External-file
identities retain the lexical selection, link/ancestor-link targets, resolved
path and content digest; retargeting or deleting a selected link rejects acceptance.

Configured `addopts` (including `-o addopts=...`) is materialized once, using
pytest's precedence, into the validated recorded command. The launcher clears
pytest's later implicit addopts expansion to prevent hidden file selections.
JUnit paths use pytest's variable/home expansion. Existing `--log-file` values
are treated as outputs too, with the same source-overlap rejection.
