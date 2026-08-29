#!/usr/bin/env python3
"""Predicate: should this PR auto-request a Codex judgment review?

Owner: ``docs/adr/2026-07-14-cc-cursor-surface-allocation.md`` addendum
2026-08-23 (automatic judgment review), retargeted from Claude to Codex by
the 2026-08-29 addendum. Review-only — never merge.

Exit 0 on a valid decision (trigger is an output, not a failure).
Exit 2 on usage / I/O errors.

Prints ``TRIGGER=yes|no``, ``REASON=<token>``, and ``ADVERSARIAL=yes|no``.
When ``GITHUB_OUTPUT`` is set, also writes ``trigger``, ``reason``, and
``adversarial`` for workflow consumption.

``ADVERSARIAL=yes`` (label ``adversarial-review`` or body token
``codex-review: adversarial``, 2026-08-29 addendum follow-up) asks the
workflow to hand Codex the fable-judge skill as its review prompt instead
of the default judgment-review pass — for a high-stakes PR where an
adversarial second look is worth the extra scrutiny. Same review-only,
read-only-sandbox contract either way; fable-judge's own rule applies
("judging changes nothing" — findings route to Cursor via notify-cursor.yml
to implement, Codex never gets write access here, per operator ruling).
"""
from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass
from pathlib import Path

LABEL = "codex-review"
BODY_TOKEN = "codex-review: judgment"
ADVERSARIAL_LABEL = "adversarial-review"
ADVERSARIAL_BODY_TOKEN = "codex-review: adversarial"
MARKER = "<!-- codex-judgment-review -->"
CURSOR_PREFIX = "cursor/"

# Cursor-first PRs that touch any of these get an automatic review request.
# Tests-only / lab-harness / chore diffs on cursor/* do not.
JUDGMENT_EXACT = frozenset(
    {
        "CLAUDE.md",
        "PIPELINES.md",
        "README.md",
        "REPO_MAP.md",
        "STATE.md",
        "core/dd_geometry.py",
        "core/dd_protection.py",
        "core/firm_rules.py",
        "core/lifecycle.py",
        "core/portfolio_mc.py",
        "docs/SESSIONS.md",
        "docs/operational_rules.md",
        "scripts/gate_manifest.py",
        "scripts/gates.yml",
    }
)

JUDGMENT_PREFIXES = (
    ".claude/skills/",
    ".cursor/rules/",
    ".github/workflows/",
    "core/mc/",
    "docs/adr/",
    "docs/briefs/",
    "docs/methodology/",
    "docs/notes/",
    "docs/personas/",
    "docs/pursuits/",
    "docs/spec/",
    "docs/superpowers/",
    "ops/c1_rail/",
    "ops/instruments/",
)

JUDGMENT_SUFFIXES = (".pine",)


@dataclass(frozen=True)
class Decision:
    trigger: bool
    reason: str
    adversarial: bool = False

    @property
    def trigger_word(self) -> str:
        return "yes" if self.trigger else "no"

    @property
    def adversarial_word(self) -> str:
        return "yes" if self.adversarial else "no"


def normalize_path(path: str) -> str:
    norm = path.replace("\\", "/")
    while norm.startswith("./"):
        norm = norm[2:]
    return norm


def is_judgment_path(path: str) -> bool:
    norm = normalize_path(path)
    if norm in JUDGMENT_EXACT:
        return True
    if any(norm.startswith(prefix) for prefix in JUDGMENT_PREFIXES):
        return True
    return any(norm.endswith(suffix) for suffix in JUDGMENT_SUFFIXES)


def _truthy(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _parse_labels(raw: str) -> set[str]:
    return {part.strip() for part in raw.split(",") if part.strip()}


def should_request_review(
    *,
    head_branch: str,
    draft: bool,
    labels: set[str],
    body: str,
    changed_files: list[str],
    existing_comments: str,
    event_action: str = "",
    event_label: str = "",
) -> Decision:
    if draft:
        return Decision(False, "draft")
    if MARKER in existing_comments:
        return Decision(False, "already_requested")
    if event_action == "labeled" and event_label not in {LABEL, ADVERSARIAL_LABEL}:
        return Decision(False, "labeled_other")
    if ADVERSARIAL_LABEL in labels:
        return Decision(True, "adversarial_label", adversarial=True)
    if LABEL in labels:
        return Decision(True, "label")
    lowered_body = body.lower()
    if ADVERSARIAL_BODY_TOKEN in lowered_body:
        return Decision(True, "adversarial_body_token", adversarial=True)
    if BODY_TOKEN in lowered_body:
        return Decision(True, "body_token")
    if head_branch.startswith(CURSOR_PREFIX) and any(
        is_judgment_path(path) for path in changed_files
    ):
        return Decision(True, "cursor_judgment_surface")
    return Decision(False, "no_match")


def _read_optional(path: Path | None) -> str:
    if path is None:
        return ""
    return path.read_text(encoding="utf-8")


def _read_lines(path: Path | None) -> list[str]:
    if path is None:
        return []
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _write_github_output(decision: Decision) -> None:
    dest = os.environ.get("GITHUB_OUTPUT")
    if not dest:
        return
    with open(dest, "a", encoding="utf-8") as handle:
        handle.write(f"trigger={decision.trigger_word}\n")
        handle.write(f"reason={decision.reason}\n")
        handle.write(f"adversarial={decision.adversarial_word}\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--head-branch", required=True)
    parser.add_argument("--draft", default="false")
    parser.add_argument("--labels", default="")
    parser.add_argument("--body", default="")
    parser.add_argument("--body-file", type=Path)
    parser.add_argument("--changed-files-file", type=Path)
    parser.add_argument("--existing-comments-file", type=Path)
    parser.add_argument("--event-action", default="")
    parser.add_argument("--event-label", default="")
    args = parser.parse_args(argv)
    try:
        body = args.body
        if args.body_file is not None:
            body = _read_optional(args.body_file)
        decision = should_request_review(
            head_branch=args.head_branch,
            draft=_truthy(args.draft),
            labels=_parse_labels(args.labels),
            body=body,
            changed_files=_read_lines(args.changed_files_file),
            existing_comments=_read_optional(args.existing_comments_file),
            event_action=args.event_action,
            event_label=args.event_label,
        )
    except OSError as exc:
        print(f"codex-judgment-review: FAIL — {exc}", file=sys.stderr)
        return 2
    print(f"TRIGGER={decision.trigger_word}")
    print(f"REASON={decision.reason}")
    print(f"ADVERSARIAL={decision.adversarial_word}")
    _write_github_output(decision)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
