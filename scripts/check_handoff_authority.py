#!/usr/bin/env python3
"""check_handoff_authority.py — a card's authority block may only narrow.

Owner of the rule: `docs/adr/2026-07-14-cc-cursor-surface-allocation.md` §Decision,
"Action classes and the authority block" (2026-09-25 revision). Registry of capability
names, risk classes and per-seat grants: `scripts/seat_authority.yml` (the one canonical
source; this checker holds no capability names of its own).

A card (a `docs/briefs/**` brief or handoff) opts in by carrying exactly one fenced block
whose info string is ``yaml authority``:

    ```yaml authority
    seat: worker
    parent: docs/briefs/handoffs/<umbrella>.md
    max_risk: medium
    capabilities: [repository.read, tests.run, worktree.write, branch.push, pr.open]
    constraints: [no_main_write, reserved_files_untouched]
    acceptance: [tests/scripts/test_x.py::test_rejects_widened_grant]
    ```

HARD checks (exit 1), each the property the ADR states:

  A1  the block parses, names a known seat and a known ``max_risk``;
  A2  every capability is registered, and none is forbidden;
  A3  no capability is an operator act (risk ``high``) — a card never delegates one;
  A4  every capability's risk <= the card's ``max_risk`` <= the seat's ``max_risk``;
  A5  every capability is grantable to the seat;
  A6  a worker card names its acceptance tests (handoff contract item 5);
  A7  when ``parent`` is given the file exists, and when the parent carries a block:
      capabilities ⊆ parent's, ``max_risk`` <= parent's, and every parent constraint is
      restated (a child may add constraints; it may not drop one silently).

Files without a block are not checked: the block is required of new worker cards by the
ADR and verified at the coordinator's pre-dispatch read, and historical cards are not
retrofitted. ``--all`` scans ``docs/briefs/**/*.md``.

Exit codes: 0 clean · 1 a HARD violation · 2 usage / unreadable registry.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY = REPO_ROOT / "scripts" / "seat_authority.yml"
SCAN_ROOT = Path("docs") / "briefs"

_FENCE_OPEN = re.compile(r"^(?P<fence>`{3,}|~{3,})[ \t]*yaml[ \t]+authority[ \t]*$")


@dataclass(frozen=True)
class Registry:
    risk_order: tuple[str, ...]
    capabilities: dict[str, str]          # capability -> risk
    forbidden: frozenset[str]
    seats: dict[str, tuple[str, frozenset[str]]]  # seat -> (max_risk, grantable)

    def rank(self, risk: str) -> int:
        return self.risk_order.index(risk)


def load_registry(path: Path = REGISTRY) -> Registry:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    order = tuple(data["risk_order"])
    caps = {name: spec["risk"] for name, spec in data["capabilities"].items()}
    for name, risk in caps.items():
        if risk not in order:
            raise ValueError(f"registry: capability {name!r} has unknown risk {risk!r}")
    forbidden = frozenset(data.get("forbidden") or {})
    overlap = forbidden & caps.keys()
    if overlap:
        raise ValueError(f"registry: forbidden and grantable at once: {sorted(overlap)}")
    seats = {}
    for seat, spec in data["seats"].items():
        grant = frozenset(spec["grantable"])
        unknown = grant - caps.keys()
        if unknown:
            raise ValueError(f"registry: seat {seat!r} grants unknown {sorted(unknown)}")
        seats[seat] = (spec["max_risk"], grant)
    return Registry(order, caps, forbidden, seats)


def extract_blocks(text: str) -> list[str]:
    """Bodies of every ``yaml authority`` fence in `text`."""
    blocks: list[str] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        m = _FENCE_OPEN.match(lines[i])
        if not m:
            i += 1
            continue
        fence = m.group("fence")
        body: list[str] = []
        i += 1
        while i < len(lines) and not lines[i].startswith(fence):
            body.append(lines[i])
            i += 1
        blocks.append("\n".join(body))
        i += 1
    return blocks


def _as_list(value, field: str, errors: list[str]) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
        errors.append(f"A1 `{field}` must be a list of strings")
        return []
    return value


def parse_block(body: str) -> tuple[dict | None, list[str]]:
    try:
        data = yaml.safe_load(body)
    except yaml.YAMLError as exc:
        return None, [f"A1 authority block is not valid YAML: {exc}"]
    if not isinstance(data, dict):
        return None, ["A1 authority block must be a mapping"]
    return data, []


def check_card(path: Path, reg: Registry, *, root: Path = REPO_ROOT,
               _seen: frozenset[Path] = frozenset()) -> list[str]:
    """HARD violations for the card at `path` (empty when clean or not opted in)."""
    blocks = extract_blocks(path.read_text(encoding="utf-8"))
    if not blocks:
        return []
    if len(blocks) > 1:
        return ["A1 more than one `yaml authority` block; a card has exactly one"]
    data, errors = parse_block(blocks[0])
    if data is None:
        return errors

    seat = data.get("seat")
    max_risk = data.get("max_risk")
    caps = _as_list(data.get("capabilities"), "capabilities", errors)
    constraints = _as_list(data.get("constraints"), "constraints", errors)
    acceptance = _as_list(data.get("acceptance"), "acceptance", errors)
    if seat not in reg.seats:
        errors.append(f"A1 unknown seat {seat!r}; registry seats: {sorted(reg.seats)}")
        return errors
    if max_risk not in reg.risk_order:
        errors.append(f"A1 unknown max_risk {max_risk!r}; one of {list(reg.risk_order)}")
        return errors
    if not caps:
        errors.append("A1 `capabilities` is empty; a card grants at least one")

    seat_max, grantable = reg.seats[seat]
    if reg.rank(max_risk) > reg.rank(seat_max):
        errors.append(f"A4 max_risk {max_risk!r} exceeds seat {seat!r} ceiling {seat_max!r}")
    for cap in caps:
        if cap in reg.forbidden:
            errors.append(f"A2 {cap!r} is forbidden to every seat; no card can grant it")
            continue
        if cap not in reg.capabilities:
            errors.append(f"A2 {cap!r} is not a registered capability")
            continue
        risk = reg.capabilities[cap]
        if risk == reg.risk_order[-1]:
            errors.append(f"A3 {cap!r} is an operator act; a card never delegates it")
            continue
        if reg.rank(risk) > reg.rank(max_risk):
            errors.append(f"A4 {cap!r} is {risk!r}, above the card's max_risk {max_risk!r}")
        if cap not in grantable:
            errors.append(f"A5 {cap!r} is not grantable to seat {seat!r}")
    if seat == "worker" and not acceptance:
        errors.append("A6 a worker card names its acceptance tests before the worker starts")

    parent = data.get("parent")
    if parent is not None:
        if not isinstance(parent, str):
            errors.append("A7 `parent` must be a repo-relative path")
            return errors
        ppath = (root / parent).resolve()
        if not ppath.is_file():
            errors.append(f"A7 parent {parent!r} does not exist")
            return errors
        if ppath in _seen or ppath == path.resolve():
            errors.append(f"A7 parent chain loops at {parent!r}")
            return errors
        pblocks = extract_blocks(ppath.read_text(encoding="utf-8"))
        if len(pblocks) == 1:
            pdata, perr = parse_block(pblocks[0])
            if pdata is None:
                errors.extend(f"A7 parent {parent}: {e}" for e in perr)
                return errors
            pcaps = set(_as_list(pdata.get("capabilities"), "parent capabilities", errors))
            pcons = set(_as_list(pdata.get("constraints"), "parent constraints", errors))
            prisk = pdata.get("max_risk")
            widened = sorted(set(caps) - pcaps)
            if widened:
                errors.append(f"A7 widens parent {parent}: {widened} not granted there")
            if prisk in reg.risk_order and reg.rank(max_risk) > reg.rank(prisk):
                errors.append(f"A7 max_risk {max_risk!r} exceeds parent's {prisk!r}")
            dropped = sorted(pcons - set(constraints))
            if dropped:
                errors.append(f"A7 drops parent constraints {dropped}; restate them")
    return errors


def _cards(root: Path) -> list[Path]:
    return sorted((root / SCAN_ROOT).rglob("*.md"))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("paths", nargs="*", type=Path, help="cards to check")
    ap.add_argument("--all", action="store_true", help=f"scan {SCAN_ROOT}/**/*.md")
    args = ap.parse_args(argv)
    if not args.paths and not args.all:
        ap.error("give card paths or --all")
    try:
        reg = load_registry()
    except (OSError, KeyError, TypeError, ValueError, yaml.YAMLError) as exc:
        print(f"ERROR: cannot load {REGISTRY.relative_to(REPO_ROOT)}: {exc}", file=sys.stderr)
        return 2
    paths = _cards(REPO_ROOT) if args.all else args.paths
    failed = checked = 0
    for path in paths:
        if not path.is_file():
            print(f"ERROR: {path} not found", file=sys.stderr)
            return 2
        if extract_blocks(path.read_text(encoding="utf-8")):
            checked += 1
        for err in check_card(path, reg):
            failed += 1
            print(f"HARD {path}: {err}")
    print(f"check_handoff_authority: {checked} card(s) with an authority block, "
          f"{failed} violation(s)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
