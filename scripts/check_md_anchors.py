#!/usr/bin/env python3
"""Check tracked Markdown paths and anchors, optionally against a shrink-only baseline."""
from __future__ import annotations

import argparse
from collections import Counter
import html
from html.parser import HTMLParser
import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from link_policy import HISTORICAL_LINE_RE, LINK_RE, link_target, markdown_links

REPO_ROOT = Path(__file__).resolve().parent.parent
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
HEADING_RE = re.compile(r"^ {0,3}#{1,6}(?:[ \t]+(.*?)|[ \t]*)$")
PINNED_RE = re.compile(r"(?:^|/)(?:blob|tree)/[0-9a-f]{7,40}(?:/|$)", re.I)
URL_RE = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//)", re.I)


class ExplicitAnchors(HTMLParser):
    def __init__(self):
        super().__init__()
        self.anchors: set[str] = set()

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.anchors.update(value.lower() for key, value in attrs
                                if key in {"id", "name"} and value is not None)


def heading_slug(heading: str) -> str:
    """Slug rendered heading text, preserving spaces and consecutive hyphens."""
    heading = LINK_RE.sub(lambda match: match.group(0).split("]", 1)[0].lstrip("!["), heading)
    heading = html.unescape(re.sub(r"<[^>]*>", "", heading)).lower()
    return "".join(char for char in heading
                   if char in "-_ " or unicodedata.category(char)[0] in "LNM").replace(" ", "-")


def anchors(text: str) -> set[str]:
    parser = ExplicitAnchors()
    generated: set[str] = set()
    fence = ""
    previous = ""
    for line in text.splitlines():
        marker = FENCE_RE.match(line)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = ""
            previous = ""
            continue
        if marker and (marker[1][0] != "`" or "`" not in marker[2]):
            fence = marker[1]
            previous = ""
            continue
        parser.feed(line + "\n")
        match = HEADING_RE.match(line)
        heading = None
        if match:
            heading = re.sub(r"[ \t]+#+[ \t]*$", "", match[1] or "").strip()
        elif previous.strip() and re.fullmatch(r" {0,3}(?:=+|-+)[ \t]*", line):
            heading = previous.strip()
        if heading is not None:
            base = heading_slug(heading)
            slug = base
            suffix = 0
            while slug in generated:
                suffix += 1
                slug = f"{base}-{suffix}"
            generated.add(slug)
        previous = "" if heading is not None else line
    return generated | parser.anchors


def document_links(text: str):
    """Use the shared policy, supplementing its deliberately omitted bare fragments."""
    yield from markdown_links(text)
    for number, line in enumerate(text.splitlines(), 1):
        if HISTORICAL_LINE_RE.search(line):
            continue
        for match in LINK_RE.finditer(line):
            target = match[1].strip().split(" ", 1)[0]
            if target.startswith("#"):
                yield number, target, ""


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
    cache: dict[Path, set[str]] = {}
    misses: list[str] = []
    for doc in documents:
        # Resolve scope before reading: tracked symlinks must not escape the repo.
        if not doc.resolve().is_relative_to(repo):
            continue
        text = read_markdown(doc, repo)
        for match, target, path in document_links(text):
            if URL_RE.match(target):
                continue
            path = unquote(path.split("?", 1)[0])
            if PINNED_RE.search(path):
                continue
            candidate = link_target(doc, repo, path, "document") if path else doc.resolve()
            if doc.relative_to(repo).parts[0] == ".claude" and not candidate.exists():
                fallback = (repo / path).resolve()
                if fallback.is_relative_to(repo) and fallback.exists():
                    candidate = fallback
            if not candidate.is_relative_to(repo):
                continue
            fragment = target.partition("#")[2]
            reason = ""
            if not candidate.exists():
                reason = "missing-file"
            elif fragment and candidate.suffix.lower() == ".md" and candidate.is_file():
                if candidate not in cache:
                    cache[candidate] = anchors(read_markdown(candidate, repo))
                if unquote(fragment).lower() not in cache[candidate]:
                    reason = "missing-anchor"
            if reason:
                number = match if isinstance(match, int) else text.count("\n", 0, match.start()) + 1
                destination = candidate.relative_to(repo).as_posix()
                if "#" in target:
                    destination += "#" + fragment
                misses.append(f"{doc.relative_to(repo).as_posix()}:{number} -> {destination} [{reason}]")
    return sorted(misses)


def main(argv=None, *, repo_root: Path = REPO_ROOT) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
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
