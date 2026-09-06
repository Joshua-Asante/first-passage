#!/usr/bin/env python3
"""Bind the living SESSIONS header to STATE's operator queue.

The header, before the first dated entry, must contain a relative Markdown
link that resolves to the supplied STATE file. Historical entries are not
current-state mirrors and are deliberately ignored.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

REPO = Path(__file__).resolve().parent.parent
DEFAULT_STATE = REPO / "STATE.md"
DEFAULT_SESSIONS = REPO / "docs" / "SESSIONS.md"

QUEUE_SECTION_RE = re.compile(
    r"^## OPERATOR QUEUE\b.*?(?=^## |\Z)",
    re.M | re.S,
)
ROW_RE = re.compile(r"^\| (\d+) \|", re.M)
DATED_ENTRY_RE = re.compile(r"(?m)^## \d{4}-\d{2}-\d{2}[a-z]?\b")
MARKDOWN_LINK_RE = re.compile(
    r"(?<!!)\[[^\]\n]+\]\(\s*"
    r"(?P<destination><[^>\n]+>|[^\s)\n]+)"
    r"(?:\s+(?:\"[^\"\n]*\"|'[^'\n]*'|\([^\n)]*\)))?\s*\)"
)
HTML_COMMENT_RE = re.compile(r"<!--.*?(?:-->|\Z)", re.S)
FENCE_LINE_RE = re.compile(
    r"^[ \t]{0,3}(?P<fence>`{3,}|~{3,})(?P<rest>[^\n]*)(?:\n|\Z)"
)
INDENTED_CODE_RE = re.compile(r"^(?: {4}|\t).*?(?:\n|\Z)", re.M)
INLINE_CODE_RE = re.compile(r"(?P<ticks>`+).*?(?P=ticks)", re.S)
REFERENCE_LINK_RE = re.compile(
    r"(?<!!)\[(?P<label>[^\]\n]+)\]\[(?P<reference>[^\]\n]*)\]"
)
REFERENCE_DEFINITION_RE = re.compile(
    r"^[ \t]{0,3}\[(?P<reference>[^\]\n]+)\]:[ \t]*"
    r"(?P<destination><[^>\n]+>|[^\s\n]+)",
    re.M,
)


def validate_operator_queue(state_text: str) -> None:
    section = QUEUE_SECTION_RE.search(state_text)
    if section is None:
        raise ValueError("STATE file has no OPERATOR QUEUE section")
    if ROW_RE.search(section.group(0)) is None:
        raise ValueError("OPERATOR QUEUE table has no numbered rows")


def living_header(sessions_text: str) -> str:
    first_entry = DATED_ENTRY_RE.search(sessions_text)
    if first_entry is None:
        return sessions_text
    return sessions_text[: first_entry.start()]


def without_fenced_code(markdown: str) -> str:
    rendered_lines: list[str] = []
    open_fence: tuple[str, int] | None = None
    for line in markdown.splitlines(keepends=True):
        match = FENCE_LINE_RE.match(line)
        if open_fence is None:
            if match is None:
                rendered_lines.append(line)
                continue
            fence = match.group("fence")
            open_fence = (fence[0], len(fence))
            continue
        if match is None:
            continue
        fence = match.group("fence")
        if (
            fence[0] == open_fence[0]
            and len(fence) >= open_fence[1]
            and not match.group("rest").strip()
        ):
            open_fence = None
    return "".join(rendered_lines)


def rendered_markdown_source(markdown: str) -> str:
    without_comments = HTML_COMMENT_RE.sub("", markdown)
    without_fences = without_fenced_code(without_comments)
    without_indented_code = INDENTED_CODE_RE.sub("", without_fences)
    return INLINE_CODE_RE.sub("code", without_indented_code)


def normalized_reference(reference: str) -> str:
    return " ".join(reference.split()).casefold()


def markdown_destinations(markdown: str) -> list[str]:
    destinations = [
        match.group("destination") for match in MARKDOWN_LINK_RE.finditer(markdown)
    ]
    definitions = {
        normalized_reference(match.group("reference")): match.group("destination")
        for match in REFERENCE_DEFINITION_RE.finditer(markdown)
    }
    for match in REFERENCE_LINK_RE.finditer(markdown):
        reference = match.group("reference") or match.group("label")
        destination = definitions.get(normalized_reference(reference))
        if destination is not None:
            destinations.append(destination)
    return destinations


def link_destination_path(destination: str, *, sessions_file: Path) -> Path | None:
    if destination.startswith("<") and destination.endswith(">"):
        destination = destination[1:-1]
    parsed = urlsplit(destination)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    path = Path(unquote(parsed.path))
    if path.is_absolute():
        return None
    return (sessions_file.parent / path).resolve()


def header_links_to_state(
    sessions_text: str, *, sessions_file: Path, state_file: Path
) -> bool:
    expected = state_file.resolve()
    rendered_header = living_header(rendered_markdown_source(sessions_text))
    return any(
        link_destination_path(destination, sessions_file=sessions_file) == expected
        for destination in markdown_destinations(rendered_header)
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--file", type=Path, default=DEFAULT_SESSIONS)
    args = parser.parse_args(argv)
    try:
        state_text = args.state.read_text(encoding="utf-8")
        sessions_text = args.file.read_text(encoding="utf-8")
        validate_operator_queue(state_text)
        if not header_links_to_state(
            sessions_text, sessions_file=args.file, state_file=args.state
        ):
            raise ValueError(
                "SESSIONS header has no relative Markdown link to the supplied STATE file"
            )
    except (OSError, ValueError) as exc:
        print(f"sessions-queue-bind: FAIL — {exc}", file=sys.stderr)
        return 1

    print("sessions-queue-bind: OK — living header routes to STATE operator queue")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
