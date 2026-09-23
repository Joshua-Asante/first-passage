"""guard_open_verification_record.py — refuse tree writes while a verification record is open.

Why: `scripts/record_verification.py` hashes the measured source tree before and
after the command it wraps and voids the record (`source_stable=false`) if any
tracked or untracked byte changed. On 2026-09-20 two 50-minute Windows
verification sequences were voided because a session wrote a docs draft into
the worktree while a record was open. A Write/Edit into the measured tree while
a record is open can never be right, so refuse it at the harness instead of
discovering it 50 minutes later.

Wiring (`.claude/settings.json`):

    {"matcher": "Edit|Write|MultiEdit|NotebookEdit",
     "hooks": [{"type": "command",
                "command": "python \\"$CLAUDE_PROJECT_DIR/scripts/guard_open_verification_record.py\\""}]}

The targets are `tool_input.file_path`, each `tool_input.edits[].file_path`
(MultiEdit) and `tool_input.notebook_path` (NotebookEdit).

Contract: Claude Code PreToolUse — read the tool payload on stdin, write a
`hookSpecificOutput.permissionDecision` JSON on stdout (see
`scripts/guard_shell_command.py` for the shape). Fail-open on any parse error
or if no record can be located. `decide()` is the pure function the tests pin.

Which records lock the tree (`_open_records`, card
`docs/briefs/handoffs/2026-09-23-harness-guards-hardening.md` E5): every
`record.json` under the checkout's `.cache/fp-verification/*/` (`scripts/fp.py`)
and `.cache/fp-docker-verification/*/` (`scripts/docker_verification.py`) that
was started less than `STALE_AFTER_SECONDS` ago — a recorder that died without
closing its record must not lock the tree forever — and either

  * has `status == "running"` (its command is executing), or
  * has `status == "not_started"` with a `before` snapshot and no
    `finished_at`: `RunRecord.begin()` has measured the tree, and the launcher
    is still doing work (environment checks, a `docker build` of up to 900 s)
    before `execute()` marks it running — a write now voids the record just
    the same.

Out of scope: records written outside the checkout, such as the ones
`scripts/qualification_boundary_verification.py` writes on Linux CI; this hook
only looks under the measured checkout's own `.cache/`.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

RECORDS_DIR = ".cache/fp-verification"
DOCKER_RECORDS_DIR = ".cache/fp-docker-verification"
STALE_AFTER_SECONDS = 4 * 3600  # longest legitimate sequence seen: ~3 h (line 3 + check)
EXEMPT_PARTS = {".cache", ".git"}


def _measured_root(path: Path) -> Path | None:
    """The checkout that would measure `path`: nearest ancestor holding `.git`."""
    for candidate in (path, *path.parents):
        if (candidate / ".git").exists():
            return candidate
    return None


def _is_open(data: dict) -> bool:
    """Whether a record's fields say its measured window is open (E5)."""
    status = data.get("status")
    if status == "running":
        return True
    return (status == "not_started" and data.get("before") is not None
            and data.get("finished_at") is None)


def _open_records(root: Path, now: datetime) -> list[Path]:
    found = []
    for folder in (RECORDS_DIR, DOCKER_RECORDS_DIR):
        records = root / folder
        if not records.is_dir():
            continue
        for record in sorted(records.glob("*/record.json")):
            try:
                data = json.loads(record.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if not isinstance(data, dict) or not _is_open(data):
                continue
            try:
                started = datetime.fromisoformat(str(data.get("started_at")))
            except (TypeError, ValueError):
                continue
            if started.tzinfo is None:
                started = started.replace(tzinfo=timezone.utc)
            if now - started > timedelta(seconds=STALE_AFTER_SECONDS):
                continue  # abandoned recorder; do not lock the tree
            found.append(record)
    return found


def decide(target: str, *, now: datetime | None = None) -> tuple[str, str, str]:
    """Return (permission, agent_message, user_message) for a write to `target`."""
    if not target:
        return ("allow", "", "")
    path = Path(target)
    if not path.is_absolute():
        return ("allow", "", "")
    root = _measured_root(path)
    if root is None:
        return ("allow", "", "")
    relative = path.relative_to(root).parts if path.is_relative_to(root) else ()
    if relative and relative[0] in EXEMPT_PARTS:
        return ("allow", "", "")
    open_records = _open_records(root, now or datetime.now(timezone.utc))
    if not open_records:
        return ("allow", "", "")
    names = ", ".join(r.parent.name for r in open_records)
    user = (
        f"Refused: a verification record is open in {root} ({names}); writing into the "
        f"measured tree now would void it (source_stable=false). Wait for the record to "
        f"close, or write drafts to the session scratchpad instead."
    )
    agent = (
        "Verification record open — the recorder hashes this tree before and after its "
        "command. Do not edit any file under the checkout until record.json reports a "
        "terminal status. Put drafts (§7, ledger text, notes) in the scratchpad directory."
    )
    return ("deny", agent, user)


def _emit(permission: str, agent_msg: str = "", user_msg: str = "") -> None:
    block: dict = {"hookEventName": "PreToolUse", "permissionDecision": permission}
    if user_msg:
        block["permissionDecisionReason"] = user_msg
    if agent_msg:
        block["additionalContext"] = agent_msg
    sys.stdout.write(json.dumps({"hookSpecificOutput": block}))


def _targets(data: dict) -> list[str]:
    """Every path a write payload names; malformed parts are skipped, not fatal."""
    tool_input = data.get("tool_input") if isinstance(data, dict) else None
    if not isinstance(tool_input, dict):
        return []
    targets = [str(tool_input.get("file_path", "")), str(tool_input.get("notebook_path", ""))]
    edits = tool_input.get("edits")
    for edit in edits if isinstance(edits, list) else []:
        if isinstance(edit, dict):
            targets.append(str(edit.get("file_path", "")))
    return [t for t in targets if t]


def main() -> int:
    """Emit a decision only when a write must be denied.

    A hook ``allow`` bypasses the operator's permission rules outright, so an
    allowed (or unparsable) write produces no output and defers to the normal
    permission flow; ``decide()`` still returns ``allow`` internally.
    """
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    for target in _targets(data):
        decision = decide(target)
        if decision[0] != "allow":
            _emit(*decision)
            return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
