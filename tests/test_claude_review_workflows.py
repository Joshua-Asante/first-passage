"""Pin the Claude review hop: git-read tools stay quoted, no bot scope creeps back.

Re-targeted 2026-09-15 with the Cursor retirement
(`docs/adr/2026-07-14-cc-cursor-surface-allocation.md`, Revision 2026-09-15).
The previous edition pinned `allowed_bots: "cursor"` as present and
`notify-cursor.yml` as disabled-but-present. Both artifacts are gone, so those
assertions are inverted rather than deleted: the file must stay absent and the
bot allow-list must stay empty. A retired lane that quietly comes back is the
thing worth failing CI over, and nothing else in the repo would notice.
"""
from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
WORKFLOWS = REPO / ".github" / "workflows"
CLAUDE_YML_PATH = WORKFLOWS / "claude.yml"
CLAUDE_YML = CLAUDE_YML_PATH.read_text(encoding="utf-8")

# Action system prompt tells Claude to Bash(git diff/log/status). Default Bash
# allowlist is only git add|commit|push|rm. Patterns must stay quoted.
REQUIRED_GIT_READ_TOOLS = (
    "Bash(git diff:*)",
    "Bash(git log:*)",
    "Bash(git status:*)",
)


def _uncommented_lines(text: str) -> list[str]:
    return [ln for ln in text.splitlines() if not ln.lstrip().startswith("#")]


def test_claude_yml_allows_quoted_git_read_tools() -> None:
    assert "--allowedTools" in CLAUDE_YML
    quoted = next(
        line.strip()
        for line in CLAUDE_YML.splitlines()
        if "--allowedTools" in line and not line.lstrip().startswith("#")
    )
    assert quoted.startswith("--allowedTools \"")
    assert quoted.endswith('"')
    for tool in REQUIRED_GIT_READ_TOOLS:
        assert tool in quoted


def test_no_bot_is_allow_listed() -> None:
    """allowed_bots is absent by design; a wildcard is a forbidden move.

    Checked against uncommented lines only — the file carries a comment block
    explaining why the key is gone, and that prose must not trip the test.
    """
    live = _uncommented_lines(CLAUDE_YML)
    assert not any("allowed_bots" in ln for ln in live), (
        "allowed_bots is deliberately absent since the 2026-09-15 Cursor "
        "retirement; re-add only with a real bot-originated @claude caller."
    )
    for wildcard in ('allowed_bots: "*"', "allowed_bots: '*'", "allowed_bots: *"):
        assert wildcard not in CLAUDE_YML


def test_cursor_notify_workflow_stays_deleted() -> None:
    """The auto-`@cursor` ping workflow retired with the lane; it must not return."""
    assert not (WORKFLOWS / "notify-cursor.yml").exists()


def test_no_workflow_dispatches_cursor() -> None:
    """No workflow may mention @cursor or the deleted dispatch script.

    Historical citations live in docs/adr/, docs/SESSIONS.md and docs/notes/ and
    are deliberately out of scope — this pins the executable surface only.
    """
    offenders = []
    for path in sorted(WORKFLOWS.glob("*.yml")) + sorted(WORKFLOWS.glob("*.yaml")):
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith("#"):
                continue  # a comment recording why the lane is gone is not a dispatch
            if "@cursor" in line or "dispatch_cursor" in line or "cursor[bot]" in line:
                offenders.append(f"{path.name}:{lineno}: {line.strip()}")
    assert not offenders, "Cursor dispatch surface reappeared:\n" + "\n".join(offenders)
