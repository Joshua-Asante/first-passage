# First Passage agent instructions

## Configuration as code

- Default to configuration as code for new or changed configuration, especially configuration used more than once.
- Define reusable configuration objects once in a canonical source; consumers reference or compose those objects rather than repeat their values or maintain copied configurations.
- Separate shared configuration, product or environment variants, and instance-specific bindings. Make overrides explicit and validate the resolved configuration at its consumption boundary.
- Keep secrets outside versioned configuration; configuration objects should reference credentials rather than embed them.
- For deployment configurations, preserve the identity/version of the resolved configuration so validation and activation refer to the same configuration.
- Apply this default as work touches configuration; it does not by itself authorize a repository-wide migration or changes to accepted policy behavior.

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
- Launcher pytest and `check` commands automatically retain evidence under `.cache/fp-verification/`; cite the printed `record.json` when reporting verification. Check `verification_exit_code`, `source_stable`, and actual test/gate results. Keep source and Git state unchanged while a recorded check runs.
- A verification claim requires `status: completed`, exit zero, stable source, complete capture, valid expected reports, and successful Docker cleanup where applicable. `not_started`, `running`, `failed`, and `interrupted` are not acceptance; a hard-killed run may remain `running`. Never infer a pass from a record merely existing.
- For independent pytest cases, opt into the installed xdist runner with `--workers 2` before the launcher command. Select the affected tests first; worker count is not a substitute for related-case coverage. Docker sequence checks use `tools/local_verification/run.ps1` and record evidence automatically too.
