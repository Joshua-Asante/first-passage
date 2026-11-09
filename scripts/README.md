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

### Running tests

`test`, `test-ops`, `python -m pytest ...` and `check` run in the foreground and
return the child's exit status; they write no record. The launcher adds
`-c <checkout>/pyproject.toml` and `--rootdir=<checkout>` to pytest commands, so a
test path outside the checkout still uses this checkout's configuration. Later
arguments and `PYTEST_ADDOPTS` reach pytest unchanged. Records already under
`.cache/fp-verification/` stay on disk; those pinned in
[`docs/evidence/PRIVATE_EVIDENCE.sha256`](../docs/evidence/PRIVATE_EVIDENCE.sha256)
remain evidence.

For faster focused feedback, use the existing pytest-xdist installation:

```powershell
.\fp.ps1 --workers 2 python -m pytest tests/test_fp_launcher.py -q
```

Workers are opt-in, bounded from 0 through 8, and use `loadscope` to group each
module/class on one worker. Use 0 for serial execution. Startup overhead and
imbalanced modules can outweigh parallelism; measure the same selection before
choosing workers. Tests with shared resources may need serial execution.

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

## The Order gates

[`check_order.py`](check_order.py) enforces [The Order](../docs/framework/the-order.md)
from [`order-state.json`](../docs/framework/order-state.json). As the `order-gates`
always-tier gate (so inside the required `skills (3.12)` job) it fails when a
registration's file no longer matches its recorded sha256, when a started
registration is changed or removed, when an active quarantine is removed, moved or
shortened, and, during a quarantine active on the base, when a change adds a
registration, alters the contract, carries a commit not prefixed `closure:`, or
changes a path outside the closure allowlist (`closure_paths` in the state, else results,
`docs/notes/`, the ledger, retrospectives and the state file; fixed while the quarantine
runs).
Hashes are of the committed blob: `git show HEAD:<path> | sha256sum`.

To register a test, add `{"id", "path", "sha256", "started": null}`; set `started`
to the date in the same change that starts the test. To STOP, set `quarantine` to
`{"start", "until"}` at least 14 days apart, in a `closure:` commit. The same script
runs as the SessionStart hook (`--session-start`, prints the state into every Claude
Code session) and as a best-effort PreToolUse hook (`--pre-tool-use`, refuses edits
to frozen registrations).

## Gate composition and admission

Composition authority is [`gates.yml`](gates.yml) via
[`gate_manifest.py`](gate_manifest.py).
Do not hand-maintain a parallel list.

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

All three hooks bootstrap through `python -I scripts/fp.py` from the checkout
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
  copy is safe only once pushed. The printed push names `origin` and the branch
  the clone's current branch tracks there. `--pinned` hashes each pinned path
  present in this checkout once and archives it only when those bytes match one
  of that path's pinned digests. Each pinned digest the file does not hold is
  reported as `path present, pinned bytes differ (have <prefix>, pins <prefixes>)`;
  the rest still run and `put` then exits 1. Explicit files are archived under
  their current hash.
- `put` refuses a clone unless every fetch and push URL of its `origin` is
  `github.com/joshua-asante/first-passage-archive` (https, `git@github.com:` or
  `ssh://` form; case, `.git` and a trailing slash ignored), and refuses one whose
  current branch does not track a branch on `origin`. A same-named repository on
  another owner, host or local path (including a relative path spelled
  `github.com/joshua-asante/first-passage-archive`) is not the archive. There is no environment
  variable or option to widen the accepted identity.
- `python scripts/evidence_archive.py audit` reports each pinned digest as ARCHIVED, UNPUSHED or MISSING; `--verify` re-hashes.
  A non-archived pin says `bytes present here` only when the local file hashes to
  its digest, else `path exists, pinned bytes differ`.
  Without an archive clone, or with a clone whose origin is not the archive, it
  prints UNVERIFIED and exits 0.

Pins are read from tracked `*SHA256SUMS` / `*MANIFEST.sha256` files and from
[`docs/evidence/PRIVATE_EVIDENCE.sha256`](../docs/evidence/PRIVATE_EVIDENCE.sha256),
where a record pinning any other private file registers it in the same commit.
The archive clone is `--archive`, `$FP_EVIDENCE_ARCHIVE`, or a
`first-passage-archive` directory beside this checkout.

## Agent CLI dispatch

`dispatch_codex.ps1` reaches Codex through the app's bundled CLI, with the agent's own token:

```powershell
.\scripts\dispatch_codex.ps1 -Worktree <worktree> -Prompt '<prompt>' -OutputFile <scratch>\last.txt [-Sandbox read-only]
.\scripts\dispatch_codex.ps1 -Worktree <worktree> -ReviewBase origin/main -OutputFile <scratch>\review.txt
```

It selects the credential and environment; it is not a sandbox. Requires PowerShell 7. Guarded:

- **Environment.** Codex starts with a fresh environment: only the allowlisted variables
  Windows, git and the Codex CLI need (`$EnvAllowlist` in the script, including `CODEX_HOME`),
  plus `GH_TOKEN` set from `FP_AGENT_GH_TOKEN`. No other caller variable reaches it
  (`GITHUB_TOKEN`, Fly or broker tokens, `OPENAI_API_KEY`, `FP_*`). It refuses with no agent
  token, or one that is not a fine-grained PAT (`github_pat_`). Codex authenticates from its
  own login in `CODEX_HOME`.
- **Location.** The worktree must be a Git worktree under `<repo>\.claude\worktrees\`, with no
  `.env` at its root.

Not guarded: reads are not confined. Codex runs as the same Windows user as every agent, so it
can still open the primary checkout and gh's stored credential files. Prompts and worktree
contents are not screened: Codex may read what Claude reads. Secret values never go in a prompt.
`-DryRun` runs every check and prints the command and the child's variable names, never values.
Tests: `tests/scripts/test_dispatch_codex.py` (dry-run, plus a stub `-Codex` that records the
child environment).

## Independent review

Review is cross-agent: Codex reviews Claude's work and Claude reviews Codex's. The merge
rule and what a reviewer treats as blocking are in
[AGENTS.md](../AGENTS.md#review-and-merge) (Review and merge, Code Review Rules).
A same-agent review may inform the author but is not the review.

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

Use unique owned paths, and invoke each checkout's own launcher from that checkout:

```powershell
.\fp.ps1 doctor
.\fp.ps1 --workers 2 python -m pytest tests/test_fp_launcher.py -q --tb=short
```

Each doctor must validate that checkout's lock. A shared validated environment is
allowed only while unchanged throughout both runs; dependency changes require
separate environments. Start with the affected baseline selection. Run a broad
baseline only to resolve a concrete attribution question. Baseline work can run
while implementation proceeds in the other tree, if CPU/memory contention permits.
Never edit the measured checkout during a run. During development, run affected
tests; after edits stop, run planned regressions and required gates. A baseline
result applies only to its revision, inputs and environment.

Before removing a baseline, make sure no run is live and its tree is clean
(including ignored resources you care about). Then use
`git worktree remove <exact registered path>`. Never force-remove dirty or unowned
worktrees.
