#!/usr/bin/env python3
"""track_b_register.py — Track B status register: check, digest, table.

The register (`docs/governance/track_b_register.yml`) holds one row per Track B
item: a gate, packet, slice, checkpoint, drill or defect. Each row gives the
item's status now, the next permitted action and who takes it. It cites the dated
ruling or acceptance that set that status. The ledgers keep the reasoning and
evidence; a row only routes to them. During the pilot the register is a derived
mirror under Rule 7 (`role: derived-mirror`), and its owners govern wherever the
two differ.

Subcommands:
  check   (default) exit 0 when the register is well formed and in step with its
          watched owner documents; exit 1 with one line per finding otherwise.
  digest  a short plain-text summary for a session start: next actions by actor,
          blocked items and approvals expiring within --days (default 7). Read-only;
          always exits 0 when the register parses.
  table   a Markdown table of the open rows (no fixed-file output; the pilot
          generates no mirror in place).

`check` is content-deterministic: it never compares against the clock, so the
required CI status cannot turn red on a date alone. Expiry appears only in
`digest`. Its findings:
  R1  schema: required keys, types, status enum, id/alias shape.
  R2  identity: ids and aliases unique across the register; no alias equals an id.
  R3  references: every `blocked_by` / `checkpoint` id exists; no self-reference;
      no cycle in `blocked_by`.
  R4  links: every `owner` / `evidence` link resolves to a tracked file and, when it
      carries a fragment, to a heading anchor in that file (GitHub slug rules).
  R5  coverage: every heading dated on or after `covers_from` in a `watch` file is
      cited by some row's `owner` or `evidence`, or listed under `noted`. A new
      ruling or acceptance therefore lands with its register row in the same change.
  R6  `reconciled_at` and `as_of` are present and well formed.
  R7  no inline comment after a value: YAML reads an unquoted ` #` as the start of a
      comment and silently cuts the value there (quote any text holding `#`).

Owner: the register itself (pilot); proposal and rationale are in its PR.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTER = ROOT / "docs" / "governance" / "track_b_register.yml"

SCHEMA = "track_b_register/v1"
STATUSES = (
    "NOT_STARTED",
    "OPEN",
    "IN_PROGRESS",
    "AWAITING_OPERATOR",
    "BLOCKED",
    "ACCEPTED",
    "ACCEPTED_LIMITED",
    "CLOSED",
    "PARKED",
)
TERMINAL = frozenset({"ACCEPTED", "ACCEPTED_LIMITED", "CLOSED"})
ACTORS = ("operator", "coordinator", "worker", "none")
KINDS = ("packet", "slice", "gate", "work", "checkpoint", "drill", "defect", "t00", "adapter", "parked")

ID_RE = re.compile(r"^[a-z0-9]+(?:\.[A-Za-z0-9][A-Za-z0-9+-]*)+$")
ALIAS_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ./+-]*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SHA_RE = re.compile(r"^[0-9a-f]{7,40}$")
HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$")
FENCE_RE = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})")
DATED_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
MD_LINK_RE = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")
HTML_ANCHOR_RE = re.compile(r"""<a\s+(?:id|name)=["']([^"']+)["']""")

ROW_KEYS = {"id", "kind", "title", "status", "since", "owner", "next", "next_actor"}
ROW_OPTIONAL = {"aliases", "blocked_by", "checkpoint", "expires", "evidence", "refs", "note"}
TOP_KEYS = {"schema", "role", "as_of", "reconciled_at", "covers_from", "watch", "items"}
TOP_OPTIONAL = {"noted"}


# ---------------------------------------------------------------- anchors

def slugify(heading: str) -> str:
    """GitHub's heading anchor for `heading` (before duplicate suffixes)."""
    text = MD_LINK_RE.sub(lambda m: m.group(1), heading)
    text = text.replace("`", "").replace("*", "")
    text = text.strip().lower()
    out = []
    for ch in text:
        cat = unicodedata.category(ch)
        if ch in (" ", "-") or cat[0] in ("L", "M", "N") or cat == "Pc":
            out.append("-" if ch == " " else ch)
    return "".join(out)


def headings(text: str) -> list[tuple[int, str]]:
    """(line number, heading text) for every ATX heading outside a code fence."""
    found: list[tuple[int, str]] = []
    fence: str | None = None
    for n, line in enumerate(text.splitlines(), 1):
        m = FENCE_RE.match(line)
        if m:
            marker = m.group(1)
            if fence is None:
                fence = marker[0] * len(marker)
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            continue
        if fence is not None:
            continue
        h = HEADING_RE.match(line)
        if h:
            found.append((n, h.group(2)))
    return found


def anchors(text: str) -> dict[str, int]:
    """anchor -> line, with GitHub's -1, -2 suffixes for repeated slugs."""
    seen: dict[str, int] = {}
    result: dict[str, int] = {}
    for n, title in headings(text):
        base = slugify(title)
        count = seen.get(base, 0)
        seen[base] = count + 1
        result[base if count == 0 else f"{base}-{count}"] = n
    for n, line in enumerate(text.splitlines(), 1):
        for m in HTML_ANCHOR_RE.finditer(line):
            result.setdefault(m.group(1), n)
    return result


# ---------------------------------------------------------------- loading

class Finding(Exception):
    pass


def load(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise Finding(f"R1 {path.name}: unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise Finding(f"R1 {path.name}: top level must be a mapping")
    return data


def _date(value: Any) -> dt.date | None:
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    if isinstance(value, str) and DATE_RE.match(value):
        return dt.date.fromisoformat(value)
    return None


def _expiry(value: Any) -> dt.datetime | None:
    if isinstance(value, dt.datetime):
        return value if value.tzinfo else value.replace(tzinfo=dt.timezone.utc)
    if isinstance(value, str):
        try:
            parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
        return parsed if parsed.tzinfo else None
    return None


def _links(row: dict[str, Any]) -> list[str]:
    links = [row["owner"]] if isinstance(row.get("owner"), str) else []
    evidence = row.get("evidence") or []
    if isinstance(evidence, list):
        links.extend(e for e in evidence if isinstance(e, str))
    return links


# ---------------------------------------------------------------- check

QUOTED_RE = re.compile(r'"(?:[^"\\]|\\.)*"|\'(?:[^\']|\'\')*\'')


def lint(text: str) -> list[str]:
    """R7: a value line whose unquoted part holds ` #` lost text to a comment."""
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("#"):
            continue
        if re.search(r"\s#", QUOTED_RE.sub('""', line)):
            out.append(f"R7 line {n}: inline comment after a value; quote text that holds '#'")
    return out


def check(data: dict[str, Any], root: Path = ROOT, text: str | None = None) -> list[str]:
    out: list[str] = lint(text) if text is not None else []

    # R1/R6 top level
    if data.get("schema") != SCHEMA:
        out.append(f"R1 schema must be {SCHEMA!r}")
    for key in sorted(TOP_KEYS - data.keys()):
        out.append(f"R1 missing top-level key {key!r}")
    for key in sorted(data.keys() - TOP_KEYS - TOP_OPTIONAL):
        out.append(f"R1 unknown top-level key {key!r}")
    if data.get("role") != "derived-mirror":
        out.append("R1 role must be 'derived-mirror' during the pilot")
    if _date(data.get("as_of")) is None:
        out.append("R6 as_of must be YYYY-MM-DD")
    if not (isinstance(data.get("reconciled_at"), str) and SHA_RE.match(data["reconciled_at"])):
        out.append("R6 reconciled_at must be a commit sha (7-40 hex)")
    covers_from = _date(data.get("covers_from"))
    if covers_from is None:
        out.append("R1 covers_from must be YYYY-MM-DD")
    watch = data.get("watch")
    if not (isinstance(watch, list) and all(isinstance(w, str) for w in watch)):
        out.append("R1 watch must be a list of repository paths")
        watch = []
    items = data.get("items")
    if not isinstance(items, list) or not items:
        out.append("R1 items must be a non-empty list")
        return out

    # R1 rows
    rows: list[dict[str, Any]] = []
    for i, row in enumerate(items):
        where = f"items[{i}]"
        if not isinstance(row, dict):
            out.append(f"R1 {where}: must be a mapping")
            continue
        where = f"{row.get('id', where)}"
        for key in sorted(ROW_KEYS - row.keys()):
            out.append(f"R1 {where}: missing {key!r}")
        for key in sorted(row.keys() - ROW_KEYS - ROW_OPTIONAL):
            out.append(f"R1 {where}: unknown key {key!r}")
        if not (isinstance(row.get("id"), str) and ID_RE.match(row["id"])):
            out.append(f"R1 {where}: id must be <kind>.<name>, e.g. slice.S5")
        elif row["id"].split(".", 1)[0] != row.get("kind"):
            out.append(f"R1 {where}: id prefix must equal kind {row.get('kind')!r}")
        if row.get("kind") not in KINDS:
            out.append(f"R1 {where}: kind must be one of {', '.join(KINDS)}")
        if row.get("status") not in STATUSES:
            out.append(f"R1 {where}: status must be one of {', '.join(STATUSES)}")
        if row.get("next_actor") not in ACTORS:
            out.append(f"R1 {where}: next_actor must be one of {', '.join(ACTORS)}")
        if _date(row.get("since")) is None:
            out.append(f"R1 {where}: since must be YYYY-MM-DD")
        for key in ("title", "owner"):
            if not (isinstance(row.get(key), str) and row[key].strip()):
                out.append(f"R1 {where}: {key} must be a non-empty string")
        nxt = row.get("next")
        if nxt is not None and not (isinstance(nxt, str) and nxt.strip()):
            out.append(f"R1 {where}: next must be text or null")
        if row.get("status") in TERMINAL and nxt is None and row.get("next_actor") != "none":
            out.append(f"R1 {where}: a row with no next action takes next_actor 'none'")
        if nxt is not None and row.get("next_actor") == "none":
            out.append(f"R1 {where}: a next action needs an actor")
        for key in ("aliases", "blocked_by", "evidence", "refs"):
            val = row.get(key)
            if val is not None and not (isinstance(val, list) and all(isinstance(v, str) for v in val)):
                out.append(f"R1 {where}: {key} must be a list of strings")
        for alias in row.get("aliases") or []:
            if isinstance(alias, str) and not ALIAS_RE.match(alias):
                out.append(f"R1 {where}: alias {alias!r} has disallowed characters")
        if "expires" in row and _expiry(row["expires"]) is None:
            out.append(f"R1 {where}: expires must be an ISO datetime with a zone, e.g. 2026-10-09T01:52:19Z")
        rows.append(row)

    # R2 identity
    names: dict[str, str] = {}
    ids = {r["id"] for r in rows if isinstance(r.get("id"), str)}
    for row in rows:
        rid = row.get("id")
        for name in [rid, *(row.get("aliases") or [])]:
            if not isinstance(name, str):
                continue
            key = unicodedata.normalize("NFKC", name).casefold()
            if key in names and names[key] != rid:
                out.append(f"R2 {rid}: name {name!r} already used by {names[key]}")
            elif key in names and name != rid:
                out.append(f"R2 {rid}: alias {name!r} repeats its own id")
            names.setdefault(key, rid)

    # R3 references and cycles
    graph: dict[str, list[str]] = {}
    for row in rows:
        rid = row.get("id")
        deps = [d for d in row.get("blocked_by") or [] if isinstance(d, str)]
        for dep in deps:
            if dep == rid:
                out.append(f"R3 {rid}: blocked_by names itself")
            elif dep not in ids:
                out.append(f"R3 {rid}: blocked_by {dep!r} is not a register id")
        cp = row.get("checkpoint")
        if cp is not None and (cp not in ids or not str(cp).startswith("checkpoint.")):
            out.append(f"R3 {rid}: checkpoint {cp!r} is not a checkpoint.* id")
        if isinstance(rid, str):
            graph[rid] = [d for d in deps if d in ids and d != rid]
    state: dict[str, int] = {}

    def visit(node: str, trail: list[str]) -> None:
        state[node] = 1
        for nxt in graph.get(node, []):
            if state.get(nxt) == 1:
                cycle = trail[trail.index(nxt):] + [nxt] if nxt in trail else [node, nxt]
                out.append(f"R3 blocked_by cycle: {' -> '.join(cycle)}")
            elif state.get(nxt) is None:
                visit(nxt, trail + [nxt])
        state[node] = 2

    for node in sorted(graph):
        if state.get(node) is None:
            visit(node, [node])

    # R4 links
    register_dir = root / "docs" / "governance"
    cache: dict[Path, dict[str, int] | None] = {}

    def resolve(link: str) -> tuple[Path, str]:
        path_part, _, frag = link.partition("#")
        return (register_dir / path_part).resolve(), frag

    def anchor_map(path: Path) -> dict[str, int] | None:
        if path not in cache:
            try:
                cache[path] = anchors(path.read_text(encoding="utf-8"))
            except OSError:
                cache[path] = None
        return cache[path]

    cited: set[tuple[Path, str]] = set()
    noted = data.get("noted") or []
    if not (isinstance(noted, list) and all(isinstance(n, dict) for n in noted)):
        out.append("R1 noted must be a list of {link, reason} mappings")
        noted = []
    link_owners = [(row.get("id"), link) for row in rows for link in _links(row)]
    for n in noted:
        if not (isinstance(n.get("link"), str) and isinstance(n.get("reason"), str) and n["reason"].strip()):
            out.append("R1 noted entries need a link and a non-empty reason")
            continue
        link_owners.append(("noted", n["link"]))
    for rid, link in link_owners:
        if re.match(r"^[a-z]+:", link):
            out.append(f"R4 {rid}: owner/evidence links must be repository-relative, not {link!r}")
            continue
        path, frag = resolve(link)
        try:
            path.relative_to(root.resolve())
        except ValueError:
            out.append(f"R4 {rid}: {link!r} leaves the repository")
            continue
        amap = anchor_map(path)
        if amap is None:
            out.append(f"R4 {rid}: {link!r}: file not found")
            continue
        if frag and frag not in amap:
            out.append(f"R4 {rid}: {link!r}: no heading with that anchor")
            continue
        cited.add((path, frag))

    # R5 coverage of dated headings in watched owners
    if covers_from is not None:
        for rel in watch:
            path = (root / rel).resolve()
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                out.append(f"R5 watch {rel!r}: file not found")
                continue
            seen: dict[str, int] = {}
            for n, title in headings(text):
                base = slugify(title)
                count = seen.get(base, 0)
                seen[base] = count + 1
                anchor = base if count == 0 else f"{base}-{count}"
                m = DATED_RE.search(title)
                if not m:
                    continue
                try:
                    when = dt.date.fromisoformat(m.group(1))
                except ValueError:
                    continue
                if when < covers_from:
                    continue
                if (path, anchor) not in cited:
                    out.append(
                        f"R5 {rel}:{n}: dated heading not cited by any row or noted entry: "
                        f"#{anchor}"
                    )
    return out


# ---------------------------------------------------------------- views

def _open(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [r for r in rows if r.get("status") not in TERMINAL and r.get("status") != "PARKED"]


def digest(data: dict[str, Any], today: dt.datetime, days: int) -> str:
    rows = data["items"]
    by_id = {r["id"]: r for r in rows}
    lines = [
        f"Track B register (derived mirror; owners govern) as_of {data['as_of']} "
        f"@ {data['reconciled_at']}"
    ]
    horizon = today + dt.timedelta(days=days)
    expiring = []
    for r in rows:
        exp = _expiry(r.get("expires"))
        if exp is None or r.get("status") in TERMINAL:
            continue
        if exp <= today:
            expiring.append(f"  EXPIRED {exp:%Y-%m-%dT%H:%MZ} {r['id']}: {r['title']}")
        elif exp <= horizon:
            hours = int((exp - today).total_seconds() // 3600)
            expiring.append(f"  {exp:%Y-%m-%dT%H:%MZ} (~{hours}h) {r['id']}: {r['title']}")
    if expiring:
        lines.append(f"Expiring within {days}d:")
        lines.extend(expiring)
    for actor in ("operator", "coordinator", "worker"):
        todo = [
            r for r in _open(rows)
            if r.get("next_actor") == actor and r.get("next")
            and all(by_id.get(d, {}).get("status") in TERMINAL for d in r.get("blocked_by") or [])
        ]
        if todo:
            lines.append(f"Next ({actor}):")
            lines.extend(f"  {r['id']}: {r['next']}" for r in todo)
    blocked = [
        r for r in _open(rows)
        if any(by_id.get(d, {}).get("status") not in TERMINAL for d in r.get("blocked_by") or [])
    ]
    if blocked:
        lines.append("Blocked:")
        for r in blocked:
            waiting = [d for d in r["blocked_by"] if by_id.get(d, {}).get("status") not in TERMINAL]
            lines.append(f"  {r['id']} <- {', '.join(waiting)}")
    lines.append(f"Register: docs/governance/track_b_register.yml ({len(rows)} rows)")
    return "\n".join(lines)


def table(data: dict[str, Any]) -> str:
    def cell(text: Any) -> str:
        return str(text or "—").replace("|", "\\|").replace("\n", " ")

    lines = ["| Item | Status | Next | Actor | Blocked by | Owner |", "|---|---|---|---|---|---|"]
    for r in _open(data["items"]):
        name = r["id"] + (f" ({', '.join(r['aliases'])})" if r.get("aliases") else "")
        lines.append(
            f"| {cell(name)} | {r['status']} | {cell(r.get('next'))} | {r['next_actor']} | "
            f"{cell(', '.join(r.get('blocked_by') or []))} | [owner]({r['owner']}) |"
        )
    return "\n".join(lines)


# ---------------------------------------------------------------- cli

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument("command", nargs="?", default="check", choices=("check", "digest", "table"))
    parser.add_argument("--register", type=Path, default=DEFAULT_REGISTER)
    parser.add_argument("--days", type=int, default=7)
    args = parser.parse_args(argv)
    try:
        data = load(args.register)
    except Finding as exc:
        print(exc)
        return 1
    text = args.register.read_text(encoding="utf-8")
    if args.command == "check":
        findings = check(data, text=text)
        for f in findings:
            print(f)
        if findings:
            print(f"track_b_register: {len(findings)} finding(s)")
            return 1
        print(f"track_b_register: OK ({len(data['items'])} rows)")
        return 0
    findings = check(data, text=text)
    if any(f.startswith(("R1", "R7")) for f in findings):
        print("track_b_register: register is malformed; run `check`")
        return 1
    if args.command == "digest":
        print(digest(data, dt.datetime.now(dt.timezone.utc), args.days))
    else:
        print(table(data))
    return 0


if __name__ == "__main__":
    sys.exit(main())
