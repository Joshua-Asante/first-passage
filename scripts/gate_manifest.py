#!/usr/bin/env python3
"""gate_manifest.py — single owner for pre-commit / Make gate composition (W5).

Reads scripts/gates.yml and runs the selected tier. Blocking checks run at
pre-commit/CI; report-only diagnostics run only when explicitly audited.

ADR: docs/adr/2026-08-07-w5-governance-diet.md
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = Path(__file__).resolve().parent / "gates.yml"

# Every tier gates.yml's own header declares. Validated in load_manifest() because
# an unrecognized tier is selected by NO selector below -- the gate is silently
# disabled, not merely deferred. That trap used to be documented as a prose warning
# against the dead `soft` tier; the 2026-09-04 addendum retired `soft` and added
# `audit`, so it is enforced here instead of narrated.
KNOWN_TIERS = frozenset({"always", "path-conditional", "data-conditional", "audit"})


def _parse_gates_yml(text: str) -> dict:
    """Stdlib parse of the committed gates.yml shape (no PyYAML required)."""
    gates: list[dict] = []
    version = 1
    cur: dict | None = None
    staged_regex: str | None = None
    in_cmd = False
    cmd_parts: list[str] = []
    in_when = False

    def flush() -> None:
        nonlocal cur, staged_regex, in_cmd, cmd_parts, in_when
        if cur is not None:
            if cmd_parts:
                cur["cmd"] = cmd_parts
            if staged_regex:
                cur["when"] = {"staged_regex": staged_regex}
            gates.append(cur)
        cur = None
        staged_regex = None
        in_cmd = False
        in_when = False
        cmd_parts = []

    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("version:"):
            version = int(raw.split(":", 1)[1].strip())
            continue
        if raw == "gates:":
            flush()
            continue
        m = re.match(r"^  - id:\s*(.+)$", raw)
        if m:
            flush()
            cur = {"id": m.group(1).strip(), "tier": "always"}
            continue
        if cur is None:
            continue
        if raw.startswith("    tier:"):
            cur["tier"] = raw.split(":", 1)[1].strip()
            in_cmd = False
            in_when = False
            continue
        if raw.startswith("    when:"):
            in_when = True
            in_cmd = False
            continue
        if in_when and "staged_regex:" in raw:
            staged_regex = raw.split("staged_regex:", 1)[1].strip().strip("'\"")
            continue
        if raw.startswith("    cmd:"):
            in_when = False
            in_cmd = True
            continue
        if in_cmd and raw.startswith("      - "):
            cmd_parts.append(raw[len("      - "):].strip())
            continue
    flush()
    return {"version": version, "gates": gates}


def load_manifest(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    data = _parse_gates_yml(text)
    if not data.get("gates"):
        raise SystemExit(f"invalid or empty gate manifest: {path}")

    # Fail CLOSED on a silent composition drop (added 2026-08-08).
    # _parse_gates_yml matches `^  - id:` exactly, so one stray space re-indents a
    # gate out of existence: it is skipped, `cur` stays None, its argv is swallowed,
    # and the runner still exits 0 having enforced less than gates.yml declares.
    #
    # The declared-count pattern below is DELIBERATELY LOOSER than the parser's
    # (`\s*` vs two literal spaces). Pinning it to the parser's own literal would
    # make both counts miss the same re-indented line and agree — the exact failure
    # this guard exists to catch. Looser here is what makes the comparison load-bearing.
    declared = len(re.findall(r"^\s*- id:", text, re.M))
    parsed = len(data["gates"])
    if parsed != declared:
        raise SystemExit(
            f"gate manifest parse mismatch in {path}: parsed {parsed} gate(s) but "
            f"{declared} '- id:' line(s) are declared. A gate is being dropped "
            f"silently — check indentation (the parser requires exactly two spaces "
            f"before '- id:'). Refusing to run a partial battery."
        )

    unknown = sorted(
        {g["id"]: g.get("tier") for g in data["gates"] if g.get("tier") not in KNOWN_TIERS}.items()
    )
    if unknown:
        listed = ", ".join(f"{gid} (tier: {tier})" for gid, tier in unknown)
        raise SystemExit(
            f"unknown gate tier(s) in {path}: {listed}. No selector claims an "
            f"unrecognized tier, so the gate would run in no tier at all — silently "
            f"disabled, not deferred. Known tiers: {', '.join(sorted(KNOWN_TIERS))}."
        )
    return data


def staged_names() -> list[str]:
    try:
        out = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only"],
            cwd=REPO_ROOT,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    return [ln.strip() for ln in out.splitlines() if ln.strip()]


def data_conditional_active(gate: dict, *, force: bool) -> bool:
    if force:
        return True
    pattern = (gate.get("when") or {}).get("staged_regex")
    if not pattern:
        return False
    rx = re.compile(pattern)
    return any(rx.search(p) for p in staged_names())


def run_cmd(cmd: list[str], *, dry_run: bool) -> int:
    print("+", " ".join(cmd), flush=True)
    if dry_run:
        return 0
    return subprocess.call(cmd, cwd=REPO_ROOT)


def select_gates(gates: list[dict], tier: str) -> list[dict]:
    if tier == "audit":
        return [g for g in gates if g.get("tier") == "audit"]
    if tier == "validate":
        # Historical `make validate`: data manifests (always) + pine manifest.
        want = {"data-manifests", "pine-manifest"}
        out = []
        for g in gates:
            if g["id"] in want:
                out.append({**g, "_force": g["id"] == "data-manifests"})
        return out
    if tier == "check":
        # Full battery: always + path-conditional (unconditional here) +
        # data manifests forced. Path-conditional is a pre-commit diet, not
        # a drop — make check still sees every gate (W5).
        out = [
            g for g in gates
            if g.get("tier") in ("always", "path-conditional")
        ]
        for g in gates:
            if g.get("id") == "data-manifests":
                out.append({**g, "_force": True})
                break
        return out
    # pre-commit: always + path/data-conditional when staged
    out = []
    for g in gates:
        t = g.get("tier", "always")
        if t == "always":
            out.append(g)
        elif t in ("data-conditional", "path-conditional") and data_conditional_active(
            g, force=False
        ):
            out.append(g)
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    ap.add_argument(
        "--tier",
        choices=("pre-commit", "check", "validate", "audit"),
        default="pre-commit",
    )
    ap.add_argument(
        "--list", action="store_true",
        help="print the hard-gate roster (blocking tiers only; pass --all-tiers "
             "to also include audit-tier diagnostics)",
    )
    ap.add_argument(
        "--all-tiers", action="store_true",
        help="with --list, include audit-tier (report-only) gates",
    )
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    data = load_manifest(args.manifest)
    gates: list[dict] = list(data["gates"])

    if args.list:
        for g in gates:
            if g.get("tier") == "audit" and not args.all_tiers:
                continue
            when = g.get("when") or {}
            extra = f" when={when.get('staged_regex')}" if when else ""
            print(f"{g['id']:28s} tier={g.get('tier')}{extra}")
            print(f"  {' '.join(g.get('cmd') or [])}")
        return 0

    selected = select_gates(gates, args.tier)
    seen: set[str] = set()
    ordered: list[dict] = []
    for g in selected:
        if g["id"] in seen:
            continue
        seen.add(g["id"])
        ordered.append(g)

    for g in ordered:
        cmd = list(g.get("cmd") or [])
        if not cmd:
            print(f"ERROR: gate {g.get('id')} has empty cmd", file=sys.stderr)
            return 1
        if g.get("tier") == "data-conditional" and not g.get("_force"):
            if not data_conditional_active(g, force=False):
                continue
        rc = run_cmd(cmd, dry_run=args.dry_run)
        if rc != 0:
            return rc
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
