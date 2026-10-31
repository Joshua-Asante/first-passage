#!/usr/bin/env python3
"""Check tracked Markdown link paths and anchors, optionally against a shrink-only baseline.

Links and headings come from a CommonMark parse (markdown-it-py, tables enabled), so
code spans, fences, indented code, HTML comments, blockquotes, reference links and
angle-bracket destinations follow the renderer rather than line regexes.
"""
from __future__ import annotations

import argparse
from collections import Counter
from html.parser import HTMLParser
import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote

from markdown_it import MarkdownIt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from link_policy import HISTORICAL_LINE_RE, link_target

REPO_ROOT = Path(__file__).resolve().parent.parent
PINNED_RE = re.compile(r"(?:^|/)(?:blob|tree)/[0-9a-f]{7,40}(?:/|$)", re.I)
URL_RE = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//)", re.I)
FRONT_MATTER_RE = re.compile(r"\A---\n.*?\n(?:---|\.\.\.)\n", re.S)
PARSER = MarkdownIt("commonmark").enable(["table", "strikethrough"])


class ExplicitAnchors(HTMLParser):
    def __init__(self):
        super().__init__()
        self.anchors: set[str] = set()

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.anchors.update(value.lower() for key, value in attrs
                                if key in {"id", "name"} and value is not None)


def parse(text: str):
    """Parse Markdown; YAML front matter renders as a table on GitHub, never a heading."""
    front = FRONT_MATTER_RE.match(text)
    if front:
        text = "\n" * front.group(0).count("\n") + text[front.end():]
    return PARSER.parse(text)


def heading_slug(inline) -> str:
    """GitHub slug of a heading's rendered text: link labels and code spans literal, HTML tags dropped."""
    text = "".join(child.content for child in inline.children or []
                   if child.type in {"text", "code_inline"}).lower()
    return "".join(char for char in text
                   if char in "-_ " or unicodedata.category(char)[0] in "LNM").replace(" ", "-")


def anchors(text: str) -> set[str]:
    generated: set[str] = set()
    explicit: set[str] = set()
    tokens = parse(text)
    for index, token in enumerate(tokens):
        if token.type == "heading_open":
            base = slug = heading_slug(tokens[index + 1])
            suffix = 0
            while slug in generated:
                suffix += 1
                slug = f"{base}-{suffix}"
            generated.add(slug)
        for html in [token] + list(token.children or []):
            if html.type in {"html_block", "html_inline"}:
                parser = ExplicitAnchors()
                parser.feed(html.content)
                parser.close()
                explicit |= parser.anchors
    return generated | explicit


def document_links(text: str):
    """Yield (1-based line, href) for each rendered link or image, in source order."""
    source = text.split("\n")
    for token in parse(text):
        if token.type != "inline" or not token.map:
            continue
        line = token.map[0]
        for child in token.children or []:
            if child.type in {"softbreak", "hardbreak"}:
                line += 1
            elif child.type in {"link_open", "image"}:
                href = child.attrs.get("href" if child.type == "link_open" else "src") or ""
                if href and not HISTORICAL_LINE_RE.search(source[min(line, len(source) - 1)]):
                    yield line + 1, href


def read_markdown(path: Path, repo: Path) -> str:
    """Match existing Markdown scanners' replacement policy, with visible evidence."""
    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        print(f"{path.relative_to(repo).as_posix()}: invalid UTF-8; replacing malformed bytes",
              file=sys.stderr)
        text = data.decode("utf-8", errors="replace")
    return text.replace("\r\n", "\n").replace("\r", "\n")


def scan(repo_root: Path) -> list[str]:
    repo = repo_root.resolve()
    result = subprocess.run(["git", "ls-files", "-z", "--", "*.md"], cwd=repo,
                            check=True, stdout=subprocess.PIPE)
    documents = sorted(Path(repo / name) for name in result.stdout.decode("utf-8").split("\0") if name)
    if not documents:
        # Rule 38: empty input is never green, and must not erase a baseline.
        raise ValueError("no tracked Markdown files to check")
    cache: dict[Path, set[str]] = {}
    misses: list[str] = []
    for doc in documents:
        # Resolve scope before reading: tracked symlinks must not escape the repo.
        if not doc.resolve().is_relative_to(repo):
            continue
        for number, target in document_links(read_markdown(doc, repo)):
            if URL_RE.match(target):
                continue
            raw_path, _, fragment = target.partition("#")
            path = unquote(raw_path.split("?", 1)[0])
            if PINNED_RE.search(path):
                continue
            candidate = link_target(doc, repo, path, "document") if path else doc.resolve()
            if doc.relative_to(repo).parts[0] == ".claude" and not candidate.exists():
                fallback = (repo / path).resolve()
                if fallback.is_relative_to(repo) and fallback.exists():
                    candidate = fallback
            if not candidate.is_relative_to(repo):
                continue
            fragment = unquote(fragment)
            reason = ""
            if not candidate.exists():
                reason = "missing-file"
            elif fragment and candidate.suffix.lower() == ".md" and candidate.is_file():
                if candidate not in cache:
                    cache[candidate] = anchors(read_markdown(candidate, repo))
                if fragment.lower() not in cache[candidate]:
                    reason = "missing-anchor"
            if reason:
                destination = candidate.relative_to(repo).as_posix()
                if "#" in target:
                    destination += "#" + fragment
                misses.append(f"{doc.relative_to(repo).as_posix()}:{number} -> {destination} [{reason}]")
    return sorted(misses)


def main(argv=None, *, repo_root: Path = REPO_ROOT) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--baseline", type=Path)
    modes.add_argument("--update-baseline", type=Path)
    args = parser.parse_args(argv)
    try:
        misses = scan(repo_root)
        baseline = args.baseline or args.update_baseline
        if baseline is None:
            for miss in misses:
                print(miss)
            return int(bool(misses))
        current = Counter()
        for miss in misses:
            source, destination = miss.split(" -> ", 1)
            current[f"{source.rsplit(':', 1)[0]} -> {destination}"] += 1
        existed = baseline.exists()
        old = Counter()
        if existed:
            for entry in baseline.read_text(encoding="utf-8").splitlines():
                identity, count = entry.rsplit("\t", 1)
                if identity in old or int(count) <= 0:
                    raise ValueError(f"Invalid baseline entry: {entry}")
                old[identity] = int(count)
        if args.baseline and not existed:
            raise FileNotFoundError(f"Baseline does not exist: {baseline}")
        grown = sorted(identity for identity in current if current[identity] > old[identity])
        if args.update_baseline:
            if existed and grown:
                print("Refusing baseline growth:", file=sys.stderr)
                for identity in grown:
                    print(f"{identity} (current={current[identity]}, baseline={old[identity]})",
                          file=sys.stderr)
                return 2
            baseline.write_text("".join(f"{identity}\t{current[identity]}\n" for identity in sorted(current)),
                                encoding="utf-8", newline="\n")
            print(f"Baseline occurrences: {sum(current.values())}; identities: {len(current)}")
            return 0
        for identity in grown:
            print(f"{identity} (current={current[identity]}, baseline={old[identity]})")
        fixed = old - current
        for identity in sorted(fixed):
            print(f"{identity} (fixed={fixed[identity]}, current={current[identity]}, baseline={old[identity]})")
        print(f"Baseline occurrences now fixed: {sum(fixed.values())}")
        return int(bool(grown))
    except (OSError, UnicodeError, ValueError, subprocess.SubprocessError) as error:
        print(f"check_md_anchors: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
