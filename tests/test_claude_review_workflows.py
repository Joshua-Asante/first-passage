"""Pin the Claude review hop so git-read tools and notify-cursor do not regress."""
from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CLAUDE_YML = (REPO / ".github" / "workflows" / "claude.yml").read_text(encoding="utf-8")
NOTIFY_YML = (REPO / ".github" / "workflows" / "notify-cursor.yml").read_text(
    encoding="utf-8"
)

# Action system prompt tells Claude to Bash(git diff/log/status). Default Bash
# allowlist is only git add|commit|push|rm. Patterns must stay quoted.
REQUIRED_GIT_READ_TOOLS = (
    "Bash(git diff:*)",
    "Bash(git log:*)",
    "Bash(git status:*)",
)


def test_claude_yml_allows_quoted_git_read_tools() -> None:
    assert "--allowedTools" in CLAUDE_YML
    assert 'allowed_bots: "cursor"' in CLAUDE_YML
    assert "allowed_bots: \"*\"" not in CLAUDE_YML
    assert "allowed_bots: '*'" not in CLAUDE_YML
    quoted = next(
        line.strip()
        for line in CLAUDE_YML.splitlines()
        if "--allowedTools" in line and not line.lstrip().startswith("#")
    )
    assert quoted.startswith("--allowedTools \"")
    assert quoted.endswith('"')
    for tool in REQUIRED_GIT_READ_TOOLS:
        assert tool in quoted


def test_notify_cursor_skips_in_progress_ack() -> None:
    assert "claude[bot]" in NOTIFY_YML
    assert "!contains(github.event.comment.body, 'Claude Code review — in progress')" in (
        NOTIFY_YML
    )
