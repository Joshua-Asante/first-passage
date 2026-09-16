# First Passage agent instructions

## Python environment and local checks

- Before project Python work, run `.\fp.ps1 doctor` from the checkout being tested.
- Run operations Python commands through `.\fp.ps1 python ...`.
- Use `.\fp.ps1 test`, `.\fp.ps1 test-ops`, and `.\fp.ps1 check` for the standard suites and gates. For selected tests, use `.\fp.ps1 python -m pytest <paths>`.
- Without PowerShell 7.3+, use `python -I scripts/fp.py <command>`. This bootstrap selects and validates the operations environment before running the task.
- Use the launcher belonging to the checkout being tested; it runs commands from its own checkout root.
- If validation fails, diagnose the reported environment problem. Do not silently fall back to system Python or bypass validation. Follow [launcher setup and usage](scripts/README.md#local-operations-launcher) to create or select the required environment.
- Keep the separately pinned research environment separate. The operations launcher does not replace it.
- When project Python starts another Python process, use `sys.executable` rather than a bare `python` command, especially on Windows.
- Report the command, interpreter, tested revision or working-tree state, and actual results. A pre-existing gate failure must be disclosed; do not describe the complete gate suite as passing.
