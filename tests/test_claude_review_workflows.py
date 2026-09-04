"""Pin the Claude review hop so git-read tools stay quoted and notify-cursor stays off."""
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


def _on_block(text: str) -> str:
    lines: list[str] = []
    in_on = False
    for line in text.splitlines():
        if line.startswith("on:"):
            in_on = True
            continue
        if in_on:
            if line and not line[0].isspace():
                break
            lines.append(line)
    return "\n".join(lines)


def test_notify_cursor_auto_ping_is_disabled() -> None:
    on_text = _on_block(NOTIFY_YML)
    assert "workflow_dispatch" in on_text
    assert "issue_comment" not in on_text
    assert "pull_request_review" not in on_text
    assert "if: false" in NOTIFY_YML
    assert "@cursor the review above is complete" not in NOTIFY_YML
