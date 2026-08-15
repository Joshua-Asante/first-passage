"""Render a Sentinel run as a markdown block appended to the proposal queue."""
from __future__ import annotations

from datetime import date

from sentinel.scan import Finding

QUEUE_PATH = "docs/notes/sentinel/queue.md"
QUEUE_MARKER = "<!-- runs:newest-first -->"
_ORDER = ("Action", "Forward", "Closed")


def render_run(
    asof: date,
    findings: list[Finding],
    *,
    status_lines: list[str] | None = None,
) -> str:
    """Deterministic markdown block for a single run."""
    lines = [f"## Run {asof.isoformat()}", ""]
    if status_lines:
        for s in status_lines:
            lines.append(s)
        lines.append("")
    if not findings:
        lines += ["_No findings — repo clean for skew / obligations / preconditions._", ""]
        return "\n".join(lines)
    for routing in _ORDER:
        bucket = [f for f in findings if f.routing == routing]
        if not bucket:
            continue
        lines.append(f"### {routing}")
        for f in sorted(bucket, key=lambda x: x.id):
            lines.append(f"- **{f.id}** [{f.category}] — {f.summary}")
            lines.append(f"  - source: `{f.source}`")
            lines.append(f"  - next: {f.next_step}")
        lines.append("")
    return "\n".join(lines)
