#!/usr/bin/env python3
"""archive_strategy.py — Phase A cold-store helper for strategy Pine + docs.

Moves files under ``core/strategies/_archive/<family>/``, rewrites pine-manifest
path columns (hash digests unchanged), and emits ≤40-line hot CARD stubs.

Operator-fired only. Design: docs/superpowers/specs/2026-08-04-strategy-coldstore-retirement-design.md
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

# Same shape as scripts/check_pine_manifest.LINE_RE — path column only is rewritten.
LINE_RE = re.compile(r"^([0-9a-f]{64})\s+(\S.*?)\s*$")
_SEP_RE = re.compile(r"^([0-9a-f]{64})(\s+)")

DISPOSITIONS = frozenset(
    {
        "VENUE_LESS_CFD",
        "VENUE_WITHDRAWN",
        "PARKED_PROTOTYPE",
        "FALSIFIED_PARKED",
    }
)

ARCHIVE_REL = "core/strategies/_archive"


def rewrite_manifest_path(
    manifest_text: str,
    old_rel: str,
    new_rel: str,
    *,
    require_present: bool = True,
) -> str:
    """Replace the path column for ``old_rel``; leave digests untouched."""
    found = False
    out_lines: list[str] = []
    ends_with_nl = manifest_text.endswith("\n")
    for line in manifest_text.splitlines():
        m = LINE_RE.match(line)
        if m and m.group(2) == old_rel:
            sep_m = _SEP_RE.match(line)
            sep = sep_m.group(2) if sep_m else "  "
            out_lines.append(f"{m.group(1)}{sep}{new_rel}")
            found = True
        else:
            out_lines.append(line)
    if require_present and not found:
        raise ValueError(f"manifest path not found: {old_rel}")
    result = "\n".join(out_lines)
    if ends_with_nl:
        result += "\n"
    return result


def move_to_archive(repo_root: Path, rel_src: str, family: str) -> Path:
    """Move ``rel_src`` to ``core/strategies/_archive/<family>/<basename>``."""
    src = (repo_root / rel_src).resolve()
    dest = (repo_root / ARCHIVE_REL / family / Path(rel_src).name).resolve()
    if not src.is_file():
        raise FileNotFoundError(f"source missing: {rel_src}")
    if dest.exists():
        raise FileExistsError(f"archive destination exists: {dest.relative_to(repo_root.resolve()).as_posix()}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dest))
    return dest


def write_card(
    path: Path,
    *,
    slug: str,
    family: str,
    disposition: str,
    body_rel: str,
    pin_lines: list[str],
    adr_links: list[str],
) -> None:
    """Emit a ≤40-line hot CARD stub at ``path``."""
    if disposition not in DISPOSITIONS:
        raise ValueError(f"unknown disposition: {disposition}")
    pin_block = "\n".join(f"- `{line}`" for line in pin_lines) if pin_lines else "- _(none)_"
    adr_block = "\n".join(f"- `{link}`" for link in adr_links) if adr_links else "- _(none)_"
    text = (
        f"# {slug}\n"
        f"\n"
        f"**Family:** {family}\n"
        f"**Disposition:** {disposition}\n"
        f"**Body:** `{body_rel}`\n"
        f"\n"
        f"## Hash pins\n"
        f"\n"
        f"{pin_block}\n"
        f"\n"
        f"## ADR\n"
        f"\n"
        f"{adr_block}\n"
    )
    lines = text.splitlines()
    if len(lines) > 40:
        raise ValueError(f"CARD exceeds 40 lines: {len(lines)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _archive_rel(family: str, rel_src: str) -> str:
    return f"{ARCHIVE_REL}/{family}/{Path(rel_src).name}"


def _collect_pin_lines(manifest_texts: list[str], rel_paths: list[str]) -> list[str]:
    wanted = set(rel_paths)
    pins: list[str] = []
    seen: set[str] = set()
    for text in manifest_texts:
        for line in text.splitlines():
            m = LINE_RE.match(line)
            if not m or m.group(2) not in wanted:
                continue
            digest, path = m.group(1), m.group(2)
            key = f"{digest}:{path}"
            if key in seen:
                continue
            seen.add(key)
            pins.append(f"{digest}  {Path(path).name}")
    return pins


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Cold-store strategy Pine/docs under core/strategies/_archive/."
    )
    p.add_argument("--repo-root", type=Path, default=Path("."))
    p.add_argument("--family", required=True)
    p.add_argument("--disposition", required=True, choices=sorted(DISPOSITIONS))
    p.add_argument("--slug", required=True)
    p.add_argument("--files", nargs="+", required=True, metavar="REL_PATH")
    p.add_argument(
        "--manifest",
        action="append",
        default=[],
        metavar="REL_PATH",
        help="Manifest to path-rewrite (repeatable). Hash digests are not changed.",
    )
    p.add_argument("--card-out", required=True, metavar="REL_PATH")
    p.add_argument(
        "--adr",
        action="append",
        default=[],
        metavar="REL_PATH",
        help="ADR path to list on the CARD (repeatable).",
    )
    return p.parse_args(argv)


def _preflight(
    repo_root: Path,
    files: list[str],
    family: str,
    manifests: list[str],
    card_out: str,
) -> list[str]:
    """Return error messages; empty list means safe to move."""
    errors: list[str] = []
    for f in files:
        if not (repo_root / f).is_file():
            errors.append(f"source missing: {f}")
    for manifest_rel in manifests:
        if not (repo_root / manifest_rel).is_file():
            errors.append(f"manifest missing: {manifest_rel}")
    for rel_src in files:
        new_rel = _archive_rel(family, rel_src)
        if (repo_root / new_rel).exists():
            errors.append(f"archive destination exists: {new_rel}")
    card_parent = (repo_root / card_out).parent
    if card_parent.exists() and not os.access(card_parent, os.W_OK):
        errors.append(f"card-out parent not writable: {card_parent.relative_to(repo_root).as_posix()}")
    return errors


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    repo_root = args.repo_root.resolve()
    family: str = args.family
    disposition: str = args.disposition
    files: list[str] = [Path(f).as_posix() for f in args.files]
    manifests: list[str] = [Path(m).as_posix() for m in args.manifest]

    preflight_errors = _preflight(
        repo_root, files, family, manifests, Path(args.card_out).as_posix()
    )
    if preflight_errors:
        for msg in preflight_errors:
            print(f"ERROR: {msg}", file=sys.stderr)
        return 1

    moves: list[tuple[str, str]] = []
    for rel_src in files:
        new_rel = _archive_rel(family, rel_src)
        dest = move_to_archive(repo_root, rel_src, family)
        print(f"{rel_src} -> {new_rel}")
        moves.append((rel_src, new_rel))
        assert dest.is_file()

    pin_source_texts: list[str] = []
    for manifest_rel in manifests:
        manifest_path = repo_root / manifest_rel
        text = manifest_path.read_text(encoding="utf-8")
        for old_rel, new_rel in moves:
            text = rewrite_manifest_path(
                text, old_rel, new_rel, require_present=False
            )
        manifest_path.write_text(text, encoding="utf-8")
        pin_source_texts.append(text)

    new_rels = [new for _, new in moves]
    pin_lines = _collect_pin_lines(pin_source_texts, new_rels)
    body_rel = f"{ARCHIVE_REL}/{family}/"
    write_card(
        repo_root / args.card_out,
        slug=args.slug,
        family=family,
        disposition=disposition,
        body_rel=body_rel,
        pin_lines=pin_lines,
        adr_links=list(args.adr),
    )
    print(f"CARD -> {Path(args.card_out).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
