#!/usr/bin/env python3
"""check_lab_path_relocation.py — relocation-rot gate (WARN / report-only).

Flags a ``docs/**/*.md`` citation of a ``lab/analysis/…`` or ``lab/archive/…``
path that does **not** exist on disk, but whose path *tail* (everything after
``lab/<bucket>/``) exists elsewhere under ``lab/``. That is the failure mode
left by the 2026-08-03 theme-nest move and the Wave-1 archive move.

Pruned-by-design paths (Great Prune harnesses — see
``docs/adr/2026-08-08-great-prune.md``) have no live twin and must NOT flag.
Ambiguous multi-match tails are reported separately and are never rewrite
candidates.

Default mode is WARN-only (exit 0 even with findings) so the gate can land
without belt-churn while the 2026-08-08 quarterly audit still carries a YELLOW
watch on gate composition. Pass ``--strict`` to exit 1 on findings.

Not wired into ``scripts/gates.yml`` — gate composition is doctrine
(``CLAUDE.md`` §Gate composition authority). Propose a tier in the landing
report; do not hand-edit the manifest from this script.

Sibling of ``check_path_liveness.py`` (pine-manifest parent dirs only — its
own success string says it does NOT cover docs/ lab citations) and
``check_md_relative_links.py`` (Makefile-only, all dead links).

Exit codes:
  0 — default (warn-only), or zero findings
  1 — ``--strict`` and one or more relocated/ambiguous findings
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Path literals — markdown links, backticks, bare prose, shell fences.
LAB_PATH_RE = re.compile(
    r"(?<![\w/])lab/(?:analysis|archive)/[A-Za-z0-9_\-./]+"
)

# Audit artifacts that *document* the stale path as evidence. Rewriting them
# (or letting the gate nag on them forever) destroys the finding record.
# C12(c) / 08-hooks prescribe the repair elsewhere; 03-agent-facing A38/A45
# name the pre-theme-nest prefix as the finding subject.
INTENTIONAL_STALE_DOCS = frozenset(
    {
        "docs/notes/audits/programme-audit/2026-08-05-claim-alignment/03-agent-facing.md",
        "docs/notes/audits/programme-audit/2026-08-05-claim-alignment/05-cosmetic.md",
        "docs/notes/audits/programme-audit/2026-08-05-claim-alignment/08-hooks.md",
    }
)

# Stale path is the *subject* of a sentence (not a navigation reference).
_SUBJECT_NEAR = re.compile(
    r"no longer resolves|pre-theme-nest prefix|theme nest vacated|"
    r"theme-nest vacated|pins a path the .{0,40}vacated",
    re.IGNORECASE | re.DOTALL,
)
# Recorded before/after citation-repair diff inside an evidence fence.
_DIFF_BEFORE_LINE = re.compile(r"^#\s+-\s+")

_SKIP_DIR_NAMES = frozenset(
    {".git", "__pycache__", ".venv", "venv", "node_modules", ".claude", ".worktrees"}
)


@dataclass(frozen=True)
class Finding:
    doc: str
    cited: str
    kind: str  # "relocated" | "ambiguous"
    targets: tuple[str, ...]
    lineno: int


def path_tail(cited: str) -> str:
    """Everything after ``lab/<bucket>/`` (analysis|archive)."""
    parts = cited.rstrip("/").replace("\\", "/").split("/")
    if len(parts) < 3:
        return ""
    return "/".join(parts[2:])


def build_lab_index(repo_root: Path) -> set[str]:
    """All files and directories under ``lab/`` as posix repo-relative paths."""
    import os

    lab = repo_root / "lab"
    out: set[str] = set()
    if not lab.is_dir():
        return out
    for root, dirs, files in os.walk(lab):
        dirs[:] = [d for d in dirs if d not in _SKIP_DIR_NAMES]
        rel_root = Path(root).relative_to(repo_root).as_posix()
        for fn in files:
            out.add(f"{rel_root}/{fn}")
        for d in dirs:
            out.add(f"{rel_root}/{d}")
    return out


def find_tail_matches(cited: str, index: set[str]) -> list[str]:
    """Paths in ``index`` whose posix form endswith ``/<tail>``."""
    tail = path_tail(cited)
    if not tail:
        return []
    needle = "/" + tail
    hits: list[str] = []
    cited_norm = cited.rstrip("/").replace("\\", "/")
    for entry in index:
        er = entry.rstrip("/")
        if er == cited_norm:
            continue
        if er.endswith(needle) or er == tail:
            hits.append(er)
    return sorted(set(hits))


def classify_citation(
    cited: str, repo_root: Path, index: set[str] | None = None
) -> tuple[str | None, list[str]]:
    """Return ``(kind, targets)``.

    kind is ``\"relocated\"``, ``\"ambiguous\"``, or ``None`` (live or pruned).
    """
    cited_norm = cited.rstrip("/").replace("\\", "/")
    if (repo_root / cited_norm).exists():
        return None, []
    idx = index if index is not None else build_lab_index(repo_root)
    matches = find_tail_matches(cited_norm, idx)
    if len(matches) == 1:
        return "relocated", matches
    if len(matches) > 1:
        return "ambiguous", matches
    return None, []


def unique_target_or_none(cited: str, repo_root: Path) -> str | None:
    """Rewrite candidate only when exactly one live twin exists."""
    kind, targets = classify_citation(cited, repo_root)
    if kind == "relocated" and len(targets) == 1:
        return targets[0]
    return None


def is_subject_context(text: str, start: int, end: int) -> bool:
    """True when the citation documents staleness rather than navigating to a file."""
    line_start = text.rfind("\n", 0, start) + 1
    line_end = text.find("\n", end)
    if line_end < 0:
        line_end = len(text)
    line = text[line_start:line_end]
    if _DIFF_BEFORE_LINE.match(line.lstrip(" ")):
        return True
    lo = max(0, start - 180)
    hi = min(len(text), end + 120)
    return bool(_SUBJECT_NEAR.search(text[lo:hi]))


def _iter_docs(repo_root: Path) -> list[Path]:
    docs = repo_root / "docs"
    if not docs.is_dir():
        return []
    import os

    out: list[Path] = []
    for root, dirs, files in os.walk(docs):
        dirs[:] = [d for d in dirs if d not in _SKIP_DIR_NAMES]
        for fn in files:
            if fn.endswith(".md"):
                out.append(Path(root) / fn)
    return sorted(out)


def scan_docs(repo_root: Path) -> list[Finding]:
    """Scan ``docs/**/*.md`` for relocation rot (and ambiguous multi-matches)."""
    index = build_lab_index(repo_root)
    findings: list[Finding] = []
    for doc in _iter_docs(repo_root):
        rel = doc.relative_to(repo_root).as_posix()
        if rel in INTENTIONAL_STALE_DOCS:
            continue
        text = doc.read_text(encoding="utf-8", errors="replace")
        seen_in_file: set[str] = set()
        for m in LAB_PATH_RE.finditer(text):
            raw = m.group(0).rstrip(".,);:`")
            if raw in seen_in_file:
                continue
            if is_subject_context(text, m.start(), m.end()):
                continue
            seen_in_file.add(raw)
            kind, targets = classify_citation(raw, repo_root, index)
            if kind is None:
                continue
            lineno = text.count("\n", 0, m.start()) + 1
            findings.append(
                Finding(
                    doc=rel,
                    cited=raw,
                    kind=kind,
                    targets=tuple(targets),
                    lineno=lineno,
                )
            )
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="repository root (default: inferred from this script)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit 1 on findings (default: WARN-tier, always exit 0)",
    )
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve()

    findings = scan_docs(repo_root)
    relocated = [f for f in findings if f.kind == "relocated"]
    ambiguous = [f for f in findings if f.kind == "ambiguous"]

    if not findings:
        print(
            "check_lab_path_relocation: OK — 0 relocation-rot finding(s) "
            "(pruned-by-design paths intentionally ignored)."
        )
        return 0

    print(
        "check_lab_path_relocation: WARN — docs cite lab/ paths that moved "
        "but were not re-pointed\n"
    )
    for f in findings:
        arrow = ", ".join(f.targets)
        print(f"  {f.doc}:{f.lineno}: [{f.kind}] {f.cited}")
        print(f"    -> {arrow}")
    print(
        f"\n  {len(relocated)} relocated, {len(ambiguous)} ambiguous "
        f"({len(findings)} finding(s) total)."
    )
    print(
        "  Repoint unique-match citations; leave ambiguous alone; "
        "do NOT invent live paths for pruned harnesses "
        "(git show pre-prune-2026-08-08:<path>)."
    )
    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
