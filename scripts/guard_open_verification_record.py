"""guard_open_verification_record.py — refuse tree writes while a verification record is open.

Why: `scripts/record_verification.py` hashes the measured source tree before and
after the command it wraps and voids the record (`source_stable=false`) if any
tracked or untracked byte changed. On 2026-09-20 two 50-minute Windows
verification sequences were voided because a session wrote a docs draft into
the worktree while a record was open. A Write/Edit into the measured tree while
a record is `running` can never be right, so refuse it at the harness instead of
discovering it 50 minutes later.

Wiring (`.claude/settings.json`):

    {"matcher": "Edit|Write|MultiEdit",
     "hooks": [{"type": "command",
                "command": "python \\"$CLAUDE_PROJECT_DIR/scripts/guard_open_verification_record.py\\""}]}

Contract: Claude Code PreToolUse — read the tool payload on stdin, write a
`hookSpecificOutput.permissionDecision` JSON on stdout (see
`scripts/guard_shell_command.py` for the shape). Fail-open on any parse error
or if no record can be located. A record counts as open only while its
`record.json` says `status == "running"` AND it was started less than
`STALE_AFTER_SECONDS` ago — a recorder that died without closing its record must
not lock the tree forever. `decide()` is the pure function the tests pin.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

RECORDS_DIR = ".cache/fp-verification"
STALE_AFTER_SECONDS = 4 * 3600  # longest legitimate sequence seen: ~3 h (line 3 + check)
EXEMPT_PARTS = {".cache", ".git"}


def _measured_root(path: Path) -> Path | None:
    """The checkout that would measure `path`: nearest ancestor holding `.git`."""
    for candidate in (path, *path.parents):
        if (candidate / ".git").exists():
            return candidate
    return None


def _open_records(root: Path, now: datetime) -> list[Path]:
    found = []
    records = root / RECORDS_DIR
    if not records.is_dir():
        return found
    for record in records.glob("*/record.json"):
        try:
            data = json.loads(record.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if data.get("status") != "running":
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
    tool_input = data.get("tool_input") or {}
    targets = [str(tool_input.get("file_path", ""))]
    for edit in tool_input.get("edits", []) or []:
        targets.append(str(edit.get("file_path", "")))
    return [t for t in targets if t]


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        _emit("allow")
        return 0
    for target in _targets(data):
        decision = decide(target)
        if decision[0] != "allow":
            _emit(*decision)
            return 0
    _emit("allow")
    return 0


if __name__ == "__main__":
    sys.exit(main())
