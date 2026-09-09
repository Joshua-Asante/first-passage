# Durable Cursor and Claude handoffs

Use `dispatch_cursor.ps1` or `dispatch_claude.ps1` for local CLI dispatches.
Both use the standard-library-only `agent_handoff.py` runner (Python 3.11+).
Existing authorization, provider permissions and hooks continue to apply.
The runner does not grant permission, auto-approve a plan, or independently verify
the worker's claimed tests. Local CLI execution still sends context to the provider.

## Dispatch and receive

```powershell
# Existing workspace; include the expected outputs and named acceptance checks.
./scripts/dispatch_cursor.ps1 -Workspace C:/work/project -Pointer C:/work/task.md `
  -ExpectedOutput reports/result.md -RequiredCheck unit-tests -TimeoutSeconds 900

# Claude retains its session and captures its ID; no --no-session-persistence.
./scripts/dispatch_claude.ps1 -Workspace C:/work/project -Pointer C:/work/task.md `
  -ExpectedOutput reports/result.md -RequiredCheck unit-tests

# Review-only tasks can return their findings in the captured response.
./scripts/dispatch_claude.ps1 -Workspace C:/work/project -Pointer C:/work/review.md -Mode ask
```

Cursor also accepts `-Slug name` to create/reuse this repository's
`.worktrees/name` on `cursor/name`. `-Workspace` supports existing workspaces,
including local maintenance outside a Git repository. An existing slug directory
must be the intended Git worktree and branch. `-Copy source::destination` stages
inputs without overwriting different bytes; on later calls supply those staged
paths using `-InputFile` instead. Pointer paths are resolved explicitly, not copied
to a potentially colliding basename. `-DryRun` makes no changes.

Use `-InputFile` for immutable dependencies that must be pinned on resume.
The packet identity includes the pointer path/hash, input paths/hashes, additional
workspace roots, expected outputs, and required check names. It does not hash every
file the packet mentions; declare load-bearing immutable inputs explicitly. Do not
declare files the worker is meant to edit as immutable inputs.

Declare outputs and checks before planning and supply the same contract when
resuming execution. Plan/ask returns are captured without requiring implementation
artifacts to exist. Execute-mode DONE returns require each declared output to exist
with the worker's reported SHA256 and each required check to report `passed` with
evidence. The parent still needs to evaluate that evidence and run appropriate
verification. Review text belongs in the return's `summary`.

Every launch prints its request ID, receipt path and local child PID. Evidence is
stored in `<workspace>/.agent-handoffs/<request-id>/`:

- `record.json`: durable lifecycle, provider/session IDs, packet identity, parent
  request, process IDs, exit status, before/after artifact hashes and timestamps.
- `prompt.txt`: exact outgoing message, including any `-MessageFile` follow-up.
- `stdout.jsonl` / `stderr.txt`: raw provider stream and errors.
- `return.json`: only written when the terminal response passes the return contract.

These files can contain private context and are gitignored in First Passage. In
other repositories, keep this directory out of commits as well. No evidence is
automatically deleted. Legacy `CURSOR_RETURN.md` and `CURSOR_PLAN.json` files are
never adopted as receipts; old sessions without a receipt cannot be blindly resumed.

The worker echoes the request ID and packet hash in its final JSON, alongside
`status`, `summary`, `artifacts` and `checks`. The runner generates this instruction.
Each continuation gets a new request ID linked to its parent. Provider request IDs
are distinct from these local handoff IDs.

## Status, cancellation and recovery

```powershell
python scripts/agent_handoff.py status --workspace C:/work/project --request-id <UUID>
python scripts/agent_handoff.py cancel --workspace C:/work/project --request-id <UUID>

# After inspecting stdout/stderr, file changes and any surviving processes:
python scripts/agent_handoff.py reconcile --workspace C:/work/project --request-id <UUID> `
  --resolution resume --note "Local worker stopped; inspected partial edits and remaining work."

./scripts/dispatch_cursor.ps1 -Workspace C:/work/project -Pointer C:/work/task.md `
  -ExpectedOutput reports/result.md -RequiredCheck unit-tests -ResumeRequestId <UUID>
```

`cancel` requests cancellation from the running controller; it does not kill a PID
read from a stale receipt. Wait for the receipt to change before assuming a stop.
At the deadline (default 900 seconds), or on cancellation, the controller attempts
to stop its owned local process tree and preserves all evidence. Detached workers
or provider-side work may outlive local cancellation; timeout never proves rollback.

The workspace lock prevents concurrent dispatch through this runner. It cannot
detect workers started directly in other tools. A crash releases the OS lock but
leaves an unresolved receipt, which prevents an automatic relaunch. Status reports
whether recorded PIDs may still be alive; PID reuse can produce a conservative
false positive. Reconciliation refuses a possibly live unfinished local process.

| State | Meaning / next step |
|---|---|
| STARTING / RUNNING | Launch in progress, or interrupted controller; inspect status. |
| RETURNED | Correlated return accepted. Read `worker_status`; BLOCKED/NEEDS_CONTEXT are not completion. |
| UNKNOWN / FAILED | Missing/invalid response or process failure. Inspect effects and reconcile. |
| TIMED_OUT / CANCELLED | Local stop attempted; inspect partial effects and reconcile. |
| RECONCILED | Parent recorded a disposition and inspection note. |

`--resolution resume` enables continuing the captured session after inspection.
`--resolution closed` closes an abandoned request so a replacement may be launched.
Neither supplies additional authority. A changed packet/provider/workspace is
refused on resume; review the change, close the old request if appropriate, and
dispatch a new packet. Missing Cursor session IDs cannot be invented: reconcile
and close the uncertain request before a replacement. Claude preallocates its
session ID; an early launch failure may mean no provider session was actually saved.

`-ResumeSessionId` on Cursor remains available only when it resolves to one latest
local receipt matching the current packet. Prefer `-ResumeRequestId`.
Use `-MessageFile` for follow-up instructions; these are saved and hashed as part
of the outgoing prompt. This carries a message, not authorization to widen scope.

## Permissions and invocation

Cursor `-Plan` / `-Ask` selects read-only provider modes. `-ForceCommands` is explicit
and execution-only. Claude `-Mode plan` uses plan permissions; `-Mode ask` exposes
Read/Glob/Grep. Execution uses existing permissions, optionally `-AllowedTools`.
No launcher disables hooks or passes bypass-permission options. A permission
failure remains an error to inspect, not a reason to change launchers.

Native executables use argument arrays with `shell=False`. On Windows, an installed
PowerShell launcher is invoked using an encoded argument array so quotes, newlines,
backticks, `$()` and percent signs survive literally. A `.cmd` path requires its
`.ps1` sibling; otherwise supply a verified native command. `-AgentCmd` overrides
the executable; the Python runner's `--command-json '["exe", "prefix-arg"]'` supports
verified runtime/entrypoint pairs and test doubles. No CLI is auto-installed.

Provider stream contracts: [Cursor output format](https://cursor.com/docs/cli/reference/output-format)
and [Claude programmatic usage](https://code.claude.com/docs/en/headless).
Changes in a provider's format fail visibly and retain raw evidence.

## Verification

Staged copies are confined using resolved paths and written only after workspace
lock acquisition and receipt admission. The packet and pinned inputs are rehashed
before launch and before accepting a return. Snapshot failures are retained in the
terminal receipt rather than leaving a misleading running state.

Cursor wrapper dry runs preview worktree preparation without calling the runner;
Claude dry runs validate through the runner. Neither proves provider acceptance.

```powershell
python -m pytest --noconftest tests/test_agent_handoff.py -q
pwsh -NoProfile -File scripts/test_dispatch_cursor.ps1
```

The protocol tests use local fake workers. `--noconftest` avoids unrelated trading
fixtures/dependencies; no provider calls or model costs are involved. The PowerShell
checks exercise wrapper validation and dry runs. Provider acceptance of a real task
remains a separate integration check; a simulated return does not prove that a
specific installed provider will follow the response instructions.
