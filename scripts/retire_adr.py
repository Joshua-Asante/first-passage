#!/usr/bin/env python3
"""retire_adr.py \u2014 ADR lifecycle retire helper.

Moves a fully superseded / withdrawn / retired ADR's body to
`docs/ltm/adr/`, rewrites its relative links for the new depth, writes a
hot CARD-shape stub at `docs/adr/<file>`, then regenerates
`docs/adr/INDEX.md` in-process via the loaded `check_adr_graph` module.

`check_adr_graph.py` verifies the graph but never mutates ADR bodies;
this script is the one place that performs the retire-time move + link
rewrite + Status/Superseded-by flip (D1/\u00a73 of the design).

Design: docs/superpowers/specs/2026-07-17-adr-lifecycle-graph-design.md
"""
from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_CAG_PATH = REPO_ROOT / "scripts" / "check_adr_graph.py"


def _load_check_adr_graph():
    spec = importlib.util.spec_from_file_location("check_adr_graph", _CAG_PATH)
    mod = importlib.util.module_from_spec(spec)
    sys.modules.setdefault(spec.name, mod)
    spec.loader.exec_module(mod)
    return mod


cag = _load_check_adr_graph()

_INDEX_RECOVERY_CMD = (
    "python scripts/check_adr_graph.py --regenerate-index --repo-root {repo_root}"
)


def _regenerate_index(repo_root: Path) -> None:
    """Write docs/adr/INDEX.md from current hot stubs (in-process)."""
    adr_dir = repo_root / "docs" / "adr"
    headers = cag.load_adr_headers(adr_dir)
    (adr_dir / "INDEX.md").write_text(cag.render_index(headers), encoding="utf-8")


REASON_TOKEN = {
    "superseded": "Superseded",
    "withdrawn": "Withdrawn",
    "retired": "Retired",
}

_MD_LINK_RE = re.compile(r"(!?\[[^\]]*\]\()([^)\s]+)(\))")
_SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
# Light-tier ADRs carry `**Tier:** light` in the header (ceremony-tiering ADR).
# Full / pre-tiering ADRs omit the field; do not invent a value on retire.
_TIER_RE = re.compile(r"^\*\*Tier:\*\*\s*(.+?)\s*$", re.M)


class RetireError(Exception):
    """Refused retire operation (precondition failure)."""


def _resolve_filename(value: str) -> str:
    name = Path(value.strip()).name
    if not name.endswith(".md"):
        name += ".md"
    return name


def _field_pattern(field: str) -> re.Pattern[str]:
    return re.compile(rf"^\*\*{re.escape(field)}:\*\*.*$", re.M)


def set_header_field(text: str, field: str, value: str) -> str:
    """Replace the first (header-region) `**field:** ...` line in text."""
    new_text, n = _field_pattern(field).subn(f"**{field}:** {value}", text, count=1)
    if n == 0:
        raise RetireError(f"header field not found: {field}")
    return new_text


def _rewrite_link_target(target: str) -> str:
    path_part, sep, frag = target.partition("#")
    if not path_part or _SCHEME_RE.match(path_part) or path_part.startswith("/"):
        return target
    if path_part.startswith("../"):
        new_path = "../" + path_part
    elif path_part.startswith("./"):
        new_path = "../../adr/" + path_part[2:]
    else:
        new_path = "../../adr/" + path_part
    return new_path + sep + frag


def rewrite_relative_links(text: str) -> str:
    """Rebase `docs/adr/`-relative markdown links for `docs/ltm/adr/` depth."""

    def repl(m: re.Match[str]) -> str:
        return f"{m.group(1)}{_rewrite_link_target(m.group(2))}{m.group(3)}"

    return _MD_LINK_RE.sub(repl, text)


def _title_from_body(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def extract_tier(text: str) -> str | None:
    """Return the ADR header Tier value, or None if the field is absent."""
    m = _TIER_RE.search(text)
    if m is None:
        return None
    value = m.group(1).strip()
    return value or None


def build_stub(
    filename: str,
    title: str,
    status_token: str,
    decision_date: str,
    superseded_by: str,
    disposition: str,
    tier: str | None = None,
) -> str:
    tier_line = f"**Tier:** {tier}\n" if tier is not None else ""
    return (
        f"# {title}\n"
        f"\n"
        f"**Status:** `{status_token}`\n"
        f"**Decision date:** {decision_date}\n"
        f"**Supersedes:** none\n"
        f"**Superseded-by:** {superseded_by}\n"
        f"**Superseded-in-part-by:** none\n"
        f"**Retain-until:** none\n"
        f"{tier_line}"
        f"**Body:** `docs/ltm/adr/{filename}`\n"
        f"**Disposition:** {disposition}\n"
        f"\n"
        f"> Open [`INDEX.md`](INDEX.md). Re-read the body path, not this stub.\n"
    )


def _validate_supersede_precondition(
    adr_dir: Path, retiree_filename: str, by_filename: str
) -> None:
    by_path = adr_dir / by_filename
    if not by_path.is_file():
        raise RetireError(f"successor not found: docs/adr/{by_filename}")
    by_header = cag.parse_adr_header(
        f"docs/adr/{by_filename}",
        by_path.read_text(encoding="utf-8", errors="replace"),
    )
    if by_header.status != "Accepted":
        raise RetireError(
            f"--by {by_filename} must be Status Accepted (found {by_header.status!r})"
        )
    has_edge = any(
        e.kind == "adr" and e.target == retiree_filename and e.scope == "full"
        for e in by_header.supersedes
    )
    if not has_edge:
        raise RetireError(
            f"--by {by_filename} must declare "
            f"Supersedes: `{retiree_filename}` full"
        )


def _print_inbound_hints(repo_root: Path, filename: str) -> None:
    self_path = repo_root / "docs" / "adr" / filename
    self_resolved = self_path.resolve()
    pattern = cag._inbound_ref_pattern(filename)
    hits: list[Path] = []
    for fp in cag.iter_a5_surfaces(repo_root):
        if not fp.is_file() or fp.resolve() == self_resolved:
            continue
        if fp.name.upper() == "INDEX.MD" and fp.parent.name == "adr":
            continue
        if pattern.search(fp.read_text(encoding="utf-8", errors="replace")):
            hits.append(fp)
    if hits:
        print(f"inbound refs to {filename} (review manually, not rewritten):")
        for fp in hits:
            print(f"  {fp.relative_to(repo_root)}")


def retire(
    repo_root: Path,
    slug: str,
    reason: str,
    by: str | None = None,
    today: str | None = None,
) -> Path:
    if reason not in REASON_TOKEN:
        raise RetireError(
            f"unknown --reason {reason!r}; expected one of {sorted(REASON_TOKEN)}"
        )
    filename = _resolve_filename(slug)
    adr_dir = repo_root / "docs" / "adr"
    ltm_dir = repo_root / "docs" / "ltm" / "adr"
    hot_path = adr_dir / filename
    if not hot_path.is_file():
        raise RetireError(f"missing ADR: docs/adr/{filename}")

    token = REASON_TOKEN[reason]
    by_filename = _resolve_filename(by) if by else None

    if reason == "superseded":
        if not by_filename:
            raise RetireError("--reason superseded requires --by <successor-filename>")
        _validate_supersede_precondition(adr_dir, filename, by_filename)
    else:
        by_filename = None

    original = hot_path.read_text(encoding="utf-8", errors="replace")
    header = cag.parse_adr_header(f"docs/adr/{filename}", original)
    decision_date = header.decision_date.isoformat() if header.decision_date else "none"
    superseded_by_value = (
        f"`{by_filename}`" if reason == "superseded" and by_filename else "none"
    )

    updated = set_header_field(original, "Status", f"`{token}`")
    if reason == "superseded" and by_filename:
        updated = set_header_field(updated, "Superseded-by", superseded_by_value)

    today_str = today or dt.date.today().isoformat()
    banner = f"<!-- relocated from docs/adr/; relative links rewritten {today_str} -->"
    ltm_text = banner + "\n\n" + rewrite_relative_links(updated)

    ltm_dir.mkdir(parents=True, exist_ok=True)
    ltm_path = ltm_dir / filename
    ltm_path.write_text(ltm_text, encoding="utf-8")

    title = _title_from_body(original, filename)
    if reason == "superseded":
        disposition = f"Fully superseded by `{by_filename}` on {today_str}."
    elif reason == "withdrawn":
        disposition = f"Withdrawn on {today_str}."
    else:
        disposition = f"Retired on {today_str}."

    stub_text = build_stub(
        filename,
        title,
        token,
        decision_date,
        superseded_by_value,
        disposition,
        tier=extract_tier(original),
    )
    hot_path.write_text(stub_text, encoding="utf-8")

    try:
        _regenerate_index(repo_root)
    except OSError as exc:
        recovery = _INDEX_RECOVERY_CMD.format(repo_root=repo_root)
        raise RetireError(
            f"index regeneration failed after stub/LTM writes ({exc}); "
            f"recover with: {recovery}"
        ) from exc

    _print_inbound_hints(repo_root, filename)
    return ltm_path


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("slug", help="ADR filename (or slug) under docs/adr/")
    ap.add_argument("--reason", required=True, choices=sorted(REASON_TOKEN))
    ap.add_argument(
        "--by", default=None,
        help="successor ADR filename (required for --reason superseded)",
    )
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    ap.add_argument(
        "--today", default=None, help="YYYY-MM-DD override for the banner (tests)"
    )
    args = ap.parse_args(argv)
    try:
        ltm_path = retire(
            args.repo_root, args.slug, args.reason, by=args.by, today=args.today
        )
    except RetireError as exc:
        print(f"retire_adr: {exc}", file=sys.stderr)
        return 1
    print(f"retired -> {ltm_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
