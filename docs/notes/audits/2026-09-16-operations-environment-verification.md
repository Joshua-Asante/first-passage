# Operations environment verification

Verified on 2026-09-16 for First Passage PR #409.

## Environment

- Interpreter: `C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`
- Python 3.13.2, Windows, isolated virtual environment; shared site-packages disabled.
- Reused the existing operations environment rather than replacing the project's broken root `.venv` or the general Codex runtime.
- All 62 distributions declared in `requirements-ops.lock` have exactly matching installed versions; none missing.
- Main checkout and PR #409 lockfiles are identical: SHA-256 `cedbcfb14f91edf73f98872734341445d41e8bb01662c130e16c40d179267fc7`.
- All 16 base and optional dependency declarations in the PR's `pyproject.toml` are satisfied.
- SciPy 1.17.1, pylint 3.3.9, setuptools 80.10.2, pytest 9.1.1, pytest-xdist 3.8.0, PyYAML 6.0.3.
- Added optional local `cryptography==50.0.1`, using the already locked cffi 2.1.0 and pycparser 3.0. This supplement is not in the repository lockfile.
- Sandboxed `pip check`: no broken requirements. Sandboxed Ed25519 signing/verification round trip passed.

## Revision-bound test evidence

Published PR revision: `17aa7ecb94f27fd9690391977af7c7f8f8fa7206`.

Clean detached verification worktree:
`C:/Users/joshu/multi_firm_operations/.worktrees/pr409-env-verification`.

From that directory:

```powershell
& 'C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe' -m pytest tests/ops/test_book_account_owner.py tests/ops/test_four_leg_runtime.py tests/ops/test_account_close_calculation.py tests/ops/test_book_settlement.py tests/ops/test_book_owner_settlement_integration.py -q -p no:cacheprovider --tb=short --basetemp C:/Users/joshu/multi_firm_operations/tmp/pytest-pr409-env-baseline-20260916
```

Result: **232 passed, zero skipped**, exit 0, 26.30 seconds. Basetemp is dedicated disposable pytest scratch; choose a separate directory for concurrent runs.

This verifies a usable local testing environment and the named existing tests. It does not close the latest review findings: their new regressions are owned by the separate active task **Fix root issues in PR 409**. Its uncommitted code, tests, and evidence in the phase2 worktree were inspected but not modified. No PR update, commit, push, merge, or deployment was performed here.

The PR's pytest CI runs Python 3.11 on Ubuntu. This Windows/Python 3.13 result is not an exact CI reproduction. The full suite and new repair regressions were not run in this verification task.

Usage and recreation instructions: `tmp/ops-env/README.md` in the main checkout.
