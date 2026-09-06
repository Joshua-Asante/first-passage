#!/usr/bin/env python3
"""Bind the living SESSIONS header to STATE's operator queue.

The header, before the first rendered dated entry, must contain a relative
Markdown link that resolves to the supplied STATE file. Historical entries are
not current-state mirrors and are deliberately ignored.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt
from markdown_it.token import Token

REPO = Path(__file__).resolve().parent.parent
DEFAULT_STATE = REPO / "STATE.md"
DEFAULT_SESSIONS = REPO / "docs" / "SESSIONS.md"

MARKDOWN = MarkdownIt("commonmark").enable("table")
DATED_ENTRY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}[a-z]?\b")
QUEUE_HEADING_RE = re.compile(r"^OPERATOR QUEUE\b")


def inline_content(tokens: list[Token], heading_index: int) -> str:
    inline_index = heading_index + 1
    if inline_index >= len(tokens) or tokens[inline_index].type != "inline":
        return ""
    return tokens[inline_index].content.strip()


def validate_operator_queue(state_text: str) -> None:
    tokens = MARKDOWN.parse(state_text)
    in_queue = False
    in_queue_table = False
    for index, token in enumerate(tokens):
        if (
            token.type == "heading_open"
            and token.tag == "h2"
            and token.level == 0
        ):
            heading = inline_content(tokens, index)
            if in_queue:
                break
            in_queue = QUEUE_HEADING_RE.match(heading) is not None
            continue
        if token.type == "table_open":
            in_queue_table = in_queue and token.level == 0
            continue
        if token.type == "table_close":
            in_queue_table = False
            continue
        if not in_queue_table or token.type != "tr_open":
            continue

        row_end = index + 1
        while row_end < len(tokens) and tokens[row_end].type != "tr_close":
            row_end += 1
        for cell_index in range(index + 1, row_end):
            if tokens[cell_index].type != "td_open":
                continue
            value = inline_content(tokens, cell_index)
            if value.isdigit():
                return
            break

    if not in_queue:
        raise ValueError("STATE file has no OPERATOR QUEUE section")
    raise ValueError("OPERATOR QUEUE table has no numbered rows")


def living_header_destinations(sessions_text: str) -> list[str]:
    tokens = MARKDOWN.parse(sessions_text)
    cutoff = len(tokens)
    for index, token in enumerate(tokens):
        if (
            token.type == "heading_open"
            and token.tag == "h2"
            and token.level == 0
            and DATED_ENTRY_RE.match(inline_content(tokens, index))
        ):
            cutoff = index
            break

    destinations: list[str] = []
    for token in tokens[:cutoff]:
        if token.type != "inline" or token.children is None:
            continue
        for child in token.children:
            if child.type == "link_open":
                destination = child.attrGet("href")
                if destination is not None:
                    destinations.append(destination)
    return destinations


def link_destination_path(destination: str, *, sessions_file: Path) -> Path | None:
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
    return any(
        link_destination_path(destination, sessions_file=sessions_file) == expected
        for destination in living_header_destinations(sessions_text)
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
