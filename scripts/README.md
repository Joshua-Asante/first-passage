# `scripts/` — gates and discipline CLIs

## Local operations launcher

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
if an environment is missing. Select it with `--env` or `FP_OPS_ENV`.

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
`m1-tree-skew` uses `--check-tree-skew` as a report-only audit; ordinary deployed
versus main drift does not fail a commit. Neither check substitutes for arm-time
validation or grants permission. The [M1 owner](../docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md)
and [arm implementation](../ops/c1_rail/c1_rail_arm.py) govern the separate execution
boundary, including the recorded attended-override path for a structurally valid
unresolved artifact; invalid/forged artifacts cannot use that path. The
[item-5 test-strategy license](../docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md#addendum-2026-08-24--test-strategy-licensed-for-item-5-dated-08-24)
does not grant arm authority.

```text
python scripts/gate_manifest.py --list
python scripts/gate_manifest.py --list --all-tiers
make check          # same runner, check tier
make audit          # report-only diagnostics
make validate       # data manifests + pine
```

Install hooks once per clone: `bash scripts/install_hooks.sh`. Install the
check dependencies first; see
[Installing the check dependencies](#installing-the-check-dependencies).

Per-script layer classification is owned by `scripts_layer` in
[`repo_map_layers.yml`](repo_map_layers.yml) (fallback **governance**), the
single layer-map definition `check_boundaries.py` loads. The human-readable
table in [`REPO_MAP.md`](../REPO_MAP.md) §2.1 is generated from that file +
[`gates.yml`](gates.yml) + `git ls-files 'scripts/*.py'`:

```text
python scripts/check_repo_map_scripts_table.py --write
python scripts/check_repo_map_scripts_table.py --check
```

Do not hand-edit the table. `--check` is not wired into `gates.yml`.

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

## Skill lifecycle

Project-authored skills are canonical in [`.claude/skills/`](../.claude/skills/).
Publication is an explicit release from a primary `main` checkout, with both a
reviewed revision and a chosen destination. The operator approved this policy on
2026-09-06 (recorded 2026-09-08); the [source record](../docs/adr/TOMBSTONES.md#2026-09-08-brief-and-skill-governance)
preserves that approval. The policy and a successful check do not themselves
authorize an actual release. Calling the publisher attests review; Git proves
revision identity, not that review occurred. No home/AppData target is implicit.

[`sync_skills.py`](sync_skills.py) requires `--revision <reviewed-sha> --target
<explicit-destination>` for publication (`make sync-skills REVISION=... TARGET=...`).
It refuses linked worktrees regardless of folder name, non-main/detached sources,
submodules, separate Git directories and unknown source identity. HEAD must equal
the named revision; releasable on-disk skill membership and content must match it,
including ignored/untracked payload and index-hidden edits. Generated caches are
excluded; unrelated dirty notes are permitted. `--force` bypasses none of these checks.

Both reference and no-constants validators are loaded from the named revision,
run against the source checkout, and run again after staging. Missing or failing
validators refuse release. Publication stages exact revision bytes; it checks all
staged files/directories against that inventory, derives installation names from
the verified inventory, rechecks source identity/payload and the target snapshot,
and refuses source/target overlap, Git metadata and symlinks/junctions/reparse paths.
Successful installation requires a final byte/inventory check. It replaces only
released skills, retaining predecessor backups and unrelated deployed skills,
including separately owned `rule-0`.

Install failure attempts rollback. Rollback must not overwrite concurrent target
changes; failed recovery or installed-byte mismatch reports an incomplete release
with the target/staging/backup locations for manual recovery. Preserve those
materials. Success and clean rollback remove staging; backups remain available.
An error is not a promise that the target is unchanged. External cloud sync can
still rewrite bundles; local checks do not enforce external ownership.

`--check` is read-only from any checkout and creates no destination or release
artifacts. Only this diagnostic retains default target resolution: the primary
bundle (environment override when set) plus `~/.claude/skills/`; explicit `--target`
selects one. It reports missing/differing/extra content, ignoring generated caches
and normalizing supported UTF-8 text newlines. Binary/invalid UTF-8 bytes compare
exactly. A diagnostic result supplies no release permission. Exit codes: 0 success
or no diagnostic drift; 1 drift/preparation/install/recovery error; 2 invalid source
or CLI input; 3 source/target/release-policy refusal.

[`gates.yml`](gates.yml) owns composition. `skill-refs` and `skills-no-constants`
remain `always` gates. [`check_skill_refs.py`](check_skill_refs.py) checks eligible
repository references with its documented exceptions.
[`check_skills_no_constants.py`](check_skills_no_constants.py) scans only `SKILL.md`
of `inqhiori`, `ooda-loop`, `programme-audit` and `brief-authoring`;
operational-reference skills and `pinescript-v6` remain exempt.

The [PostToolUse skill hook](sync_skills_hook.py), registered in
[settings](../.claude/settings.json), runs both validators on skill edits and
reports their actual outcomes and a pending explicit release. It never publishes
or creates backups, including from worktrees. Missing/failing validators exit 2,
surfaced directly by that registration while remaining fail-open for the completed
edit. Malformed/unrelated hook input is benign. (A Cursor `afterFileEdit` adapter
previously forwarded this for that surface; it retired with the Cursor lane —
[worker-surface allocation](../docs/adr/2026-07-14-cc-cursor-surface-allocation.md),
Revision 2026-09-15.)

[`import_skill_from_cache.py`](import_skill_from_cache.py) remains a missing-source
recovery exception: copy one named skill byte-for-byte only when its repository
destination is absent and the source has `SKILL.md`. No overwrite option exists.
After import, repository ownership and gates apply; it is not reverse sync or a
release. Deployed-only extras need triage, not automatic deletion/import;
`notion-mcp-api-patterns` remains [archived](../docs/pursuits/d6-notion-mcp-api-patterns-user-skill.md).

[`check_skill_deploy_sync.py`](check_skill_deploy_sync.py) checks existence of
literal ADR-cited deployed scripts, not equality. It is `SKIP` / `NOT CHECKED`
when there is no deployment root, or when the root holds none of this repo's
skill directories, cited or not, directly under it (a managed remote
container's harness-owned `~/.claude/skills/`, for example); nested
marketplace copies do not count as the bundle. A root that has any repo
skill's directory but lacks a cited script fails, including a bundle that
lost the cited skill itself, and a partial bundle is drift, not a skip. Re-running
this check against an existing bundle requires no publication. Any repair
release requires the explicit reviewed-revision/target procedure above.

The June 4 quarterly expected-10-skills / old-name reread is retired, not passed
([record](../docs/adr/TOMBSTONES.md#2026-09-08-brief-and-skill-governance)). Live
reference/no-constants failure tests, release refusal/recovery tests and deployed
script existence checks remain. This does not reopen retired skill migrations.

## Validation maintenance

### Brief checker ownership

The [brief-authoring skill](../.claude/skills/brief-authoring/SKILL.md#checker-ownership)
owns the canonical checker source, type contracts and repo-subset limits. Follow
the artifact's verification contract; a `NOT CHECKED` or delegation notice is not
a full validation pass. Checker/template unification remains unresolved and is
not commissioned here. Neither brief checker is in the gate manifest.

The separate unresolved 26-letter session-label ceiling remains with the
[SESSIONS header](../docs/SESSIONS.md) and [`roll_sessions.py`](roll_sessions.py).

## Closure enforcement

`check_closure_disposition.py` enforces the accepted closure standard as
HARD in repository mode: missing Iterate heading/Next/Board-write tokens,
missing required Registry token, or an applicable terminal campaign claim
without a hot/LTM closure record returns 1. Each limb acts independently.
Historical ADR Status tokens do not configure these checks.

Revision 2026-09-08 — the approved ADR-pruning migration replaces the
former M-22 downgrade on missing/unparseable Status owners with this
fixed code contract. The prior accepted arrangement is preserved at
`502a8fb4717e8caaa7d183a0a010998cfd7a30c2:scripts/check_closure_disposition.py`
and the August 4 Iterate / August 12 coverage ADRs at that revision.
Future severity changes require a reviewed code and operating-contract change.
This document is not a machine-readable arming dependency.

The checker retains the exact grandfather boundaries, Registry NA/debt
partition, hot/LTM filename joins and no-joinable-LTM public-seed waiver.
Explicit paths check Iterate and Registry tokens without running coverage;
`--list-debt` remains report-only. Existing unreadable-content warnings
remain warnings. The [closure template](../.claude/skills/brief-authoring/references/closure_record.md)
owns authoring detail; this gate does not enforce Lane/Closed fields,
semantic completeness, or successor authorization.

## Independent review

[The pre-ratification workflow](../.claude/workflows/pre-ratification-adversarial-panel.js)
owns its review mechanics. Reviewers assess the source independently of the proposer's
reasoning; synthesis is advisory and cannot supply operator ratification or execution
authority. Reviewer/delegate assignment never grants permission to edit locked surfaces.

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
