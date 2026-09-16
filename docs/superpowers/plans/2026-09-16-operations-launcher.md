# Operations launcher implementation plan

> **For agentic workers:** Execute with superpowers:executing-plans. Preserve the behavioral contract and integration owner.

**Goal:** One local command selects the locked operations environment and keeps nested Python commands on it.

**Architecture:** `fp.ps1` forwards arguments to a standard-library Python bootstrap at `scripts/fp.py`. The bootstrap locates the operations venv, checks installed versions against this checkout's lockfile, and starts the requested command with a child-only environment. The coordinator owns integration.

**Tech stack:** PowerShell, Python standard library, existing pytest.

**Contract:** User-approved launcher from the current task. Existing gate composition stays in `scripts/gates.yml`.

## Acceptance

- Resolve explicit `--env`, then `FP_OPS_ENV`, then checkout `tmp/ops-env`, then the main checkout's `tmp/ops-env` for linked worktrees. Explicit invalid selections fail without fallback.
- Use the checkout containing the launcher as the command working directory.
- Require a working isolated venv and exact lockfile versions; never install packages automatically.
- Prepend the selected interpreter's directory to PATH, set VIRTUAL_ENV, and remove inherited PYTHONHOME/PYTHONPATH for child processes. Do not mutate the caller's environment. Windows testing demonstrated that bare Python subprocess names bypass PATH via the base interpreter's directory; the gate runner must bind manifest Python commands to `sys.executable`. Arbitrary user scripts must likewise use `sys.executable` or an explicitly resolved executable.
- Preserve arguments and exit status; do not run commands through a shell.
- Support doctor, python, test, test-ops, and check. Existing gate runner remains the sole gate owner.
- Test interpreter inheritance, actual gate-child execution, wrong/missing environment, package mismatch, paths/arguments with spaces, linked-worktree resolution, and PowerShell forwarding.

## Execution

- [x] Write behavioral subprocess tests and record the expected failing baseline.
- [x] Implement the bootstrap and PowerShell wrapper; document commands and selection.
- [x] Run launcher and gate-runner regressions in the verified operations environment.
- [x] Exercise doctor and focused real project tests through the launcher.
- [x] Inspect final changes and make the launcher available in the main checkout without overwriting unrelated work.

Base: `133f043c683e66095aa06800c099f691a9d4294c`. Worktree: `.worktrees/operations-launcher`. The subsequent user instruction authorizes committing the launcher together with root `AGENTS.md` on the main checkout; no push or PR was requested.

## Verification record

- Initial stub: 14 failed, 1 passed. First implementation: 3 failed, 12 passed; failures exposed Windows executable resolution and PowerShell multiple command matches.
- Final launcher and gate tests through `fp.ps1 python -m pytest`: 34 passed. Fixture-only path precedence was subsequently corrected and verified under a global runner.
- Global Python 3.13 runner (`sys.prefix == sys.base_prefix`) with offline fixture dependencies: 17 launcher tests passed. The test fixture creates its own venv, so CI need not run pytest inside one.
- Empty explicit environment and inherited PowerShell native-error-preference regressions reproduced before correction.
- Real doctor: 62 locked packages matched; optional cryptography 50.0.1. `pip check` passed. Focused pylint score 8.50, above the repository's 8.0 threshold; style warnings remain. `git diff --check` passed.
- Real `fp.ps1 check` ran children with the operations interpreter, including 72 evidence-store tests (3 skipped), then stopped at pre-existing `state-currency`: weekly deadline 2026-09-11 is overdue. The identical failure was reproduced in untouched main. Do not claim the full check tier passed.
- Independent reviewer accepted the code after the three findings were repaired; reviewer did not independently rerun final tests.
- No research dependencies, global PATH, default Python, PR #409 code, or Docker configuration changed.
- Main-checkout integration verified: `fp.ps1 doctor` matched all 62 packages; final launcher and gate tests passed **34/34 in 19.85 seconds**. The isolated implementation worktree retains the earlier local implementation snapshot.
- Root `AGENTS.md` now directs future agents to the launcher and its setup documentation. No Claude instructions were added or changed.
