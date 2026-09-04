#!/usr/bin/env python3
"""WARN-tier gate: do standing ADR falsifiers still have inputs that exist?

Operational-rules Rule 11 says a falsifier whose input can no longer accrue is not
"in force" regardless of unchanged threshold text. Rule 11 is prose plus a hookify
nudge; nothing mechanical checks it. `check_adr_graph.py` validates header grammar,
edge reciprocity, stub shape and INDEX freshness -- it never asks whether a §4
clause's inputs still exist.

This script asks exactly that, using the only non-semantic anchor available:
**does the file/command a falsifier names still exist on disk?** It reads no intent.

SCOPE AND ITS LIMITS:

  * COVERAGE IS A MINORITY OF FALSIFIERS, AND ERODING. Run `--stats` for the
    current census — do **not** hand-maintain figures here. Evidence for
    "eroding": 2026-08-02 read **69 sections / 19 runnable = 28%**; 2026-08-05
    read **83 / 21 = 25%** — the corpus added falsifier sections while anchored
    coverage rose by 2. A green run means "no NAMED input is missing", never
    "all falsifiers are in force".

  * BLIND TO RETIREMENT. Path existence catches DELETION, not REVOCATION OF DUTY.
    Worked example: 2026-05-23-allocation-refresh-2 limb 1 runs
    `lab/analysis/time_to_pass.py --regime-check`. The file exists, so this script
    scores it reachable -- but the duty was retired 2026-07-22 (D2) and the harness
    now raises ValueError on the retired Pepperstone panel. Retirement is this
    repo's DOMINANT darkening mode, and this script cannot see it. It is a floor.

  * WARN-TIER BY DESIGN. Always exits 0 unless --strict. A hard gate here would
    block commits on ADRs nobody is touching -- the M-22 failure mode (a gate that
    hard-failed every commit from any worktree). Wired into `gates.yml` id
    `falsifier-reachability-census` (`tier: audit`, `--stats` only), run via
    `make audit` -- not pre-commit/`make check`/required CI (W5 governance-diet
    2026-09-04 addendum: a command that cannot fail a commit is not a merge gate).
    "WARN-tier" here means the script never returns non-zero without `--strict`,
    not that it is unwired.

EXEMPTIONS (both non-semantic, both measured to suppress real false positives):

  1. SELF-DELETION. An ADR that retires a surface naturally names what it deleted.
     A missing path is exempt if the ADR mentions it near deletion/retirement
     language. Suppresses e.g. 2026-07-11-fxify-ops-surface-retirement (`accounts.py`).

  2. RECORDED DORMANCY. An ADR that already carries a Rule 11 dormancy record has
     complied; re-flagging it is noise. Suppresses e.g. 2026-07-03-hardcore-p3,
     whose existence-bar dormancy was correctly back-propagated by the R6 NO-GO.

Usage:
    python scripts/check_falsifier_reachability.py            # WARN report, exit 0
    python scripts/check_falsifier_reachability.py --strict   # exit 1 if any finding
    python scripts/check_falsifier_reachability.py --stats    # coverage census
    python scripts/check_falsifier_reachability.py --all      # show exempted too
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADR_DIR = ROOT / "docs" / "adr"
EXCLUDE_TOP = {".git", ".venv-research", ".venv", "node_modules",
               "__pycache__", ".pytest_cache", ".mypy_cache"}

# --------------------------------------------------------------------------- universe

def build_universe() -> set[str]:
    """Git-tracked UNION on-disk (minus sibling worktrees, venvs, caches).

    The union matters: Pine sources and vendor CSVs are gitignored but present
    locally, and a falsifier may legitimately name one.
    """
    rel: set[str] = set()
    try:
        out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True,
                             text=True, check=True).stdout
        rel |= {ln.strip().replace("\\", "/") for ln in out.splitlines() if ln.strip()}
    except Exception:
        pass
    for dirpath, dirnames, filenames in os.walk(ROOT):
        rp = Path(dirpath).relative_to(ROOT)
        rs = str(rp).replace("\\", "/")
        if (rp.parts and rp.parts[0] in EXCLUDE_TOP) or rs.startswith(".claude/worktrees"):
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_TOP]
        for f in filenames:
            rel.add(str(rp / f).replace("\\", "/").lstrip("./"))
    return {p for p in rel if not p.startswith(".claude/worktrees")}


# --------------------------------------------------------------------------- sections

FALS_HEAD = re.compile(
    r"^#{1,4}\s+.*(falsifier|revert trigger|revert / re-baseline|revert/re-baseline"
    r"|falsifiable hypothesis|success bar|revert target)", re.I)
ANY_HEAD = re.compile(r"^(#{1,6})\s+\S")
FENCE = re.compile(r"^\s*```")
DORMANCY = re.compile(r"\bdormant\b|\bdormancy\b|\bre-arm\b|cannot (currently )?accrue"
                      r"|no longer accrue|unaccruab", re.I)
DELETION_NEAR = re.compile(r"delet|retir|removed|`?git rm`?|wipe|excis|tombstone", re.I)


def falsifier_sections(lines: list[str]) -> list[tuple[str, list[str]]]:
    """Return (heading, body) for falsifier-ish sections, fence-aware.

    Fence tracking matters: §10 audit-hook blocks are full of `# comment` lines
    that would otherwise parse as markdown headings.
    """
    in_fence = False
    heads: list[tuple[int, int, str, bool]] = []
    for i, ln in enumerate(lines):
        if FENCE.match(ln):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = ANY_HEAD.match(ln)
        if m:
            heads.append((i, len(m.group(1)), ln.strip(), bool(FALS_HEAD.match(ln))))
    out = []
    for n, (i, lvl, text, is_f) in enumerate(heads):
        if not is_f:
            continue
        end = len(lines)
        for j, l2, _, _ in heads[n + 1:]:
            if l2 <= lvl:
                end = j
                break
        out.append((text, lines[i + 1:end]))
    return out


# --------------------------------------------------------------------------- inputs

P_PY_TICK = re.compile(r"`([A-Za-z0-9_./\-]+\.py)`")
P_PY_LINK = re.compile(r"\]\(([A-Za-z0-9_./\-]+\.py)\)")
P_CMD_TICK = re.compile(r"`((?:python3?|py)\s+(?:-m\s+)?[A-Za-z0-9_./\-]+[^`]*"
                        r"|make\s+[a-z][a-z0-9\-]*|pytest\s+[A-Za-z0-9_./\-]+)`")
P_CMD_FENCE = re.compile(r"^\s*((?:python3?|py)\s+(?:-m\s+)?[A-Za-z0-9_./\-]+.*"
                         r"|make\s+[a-z][a-z0-9\-]*|pytest\s+[A-Za-z0-9_./\-]+.*)$", re.M)


def _fenced(body: list[str]) -> list[str]:
    out, cur, inb = [], [], False
    for ln in body:
        if FENCE.match(ln):
            if inb:
                out.append("\n".join(cur))
                cur = []
            inb = not inb
        elif inb:
            cur.append(ln)
    if cur:
        out.append("\n".join(cur))
    return out


def extract_inputs(body: list[str]) -> tuple[set[str], set[str]]:
    text = "\n".join(body)
    paths, cmds = set(), set()
    for rx in (P_PY_TICK, P_PY_LINK):
        for m in rx.finditer(text):
            v = m.group(1).strip().replace("\\", "/").lstrip("./")
            if v and "..." not in v:
                paths.add(v)
    for m in P_CMD_TICK.finditer(text):
        cmds.add(" ".join(m.group(1).split()))
    for blk in _fenced(body):
        for m in P_CMD_FENCE.finditer(blk):
            cmds.add(" ".join(m.group(1).split()))
    return paths, cmds


# --------------------------------------------------------------------------- resolve

class Resolver:
    def __init__(self, universe: set[str]):
        self.u = universe
        self.dirs = {str(Path(p).parent).replace("\\", "/") for p in universe}
        self.by_base: dict[str, list[str]] = {}
        for p in universe:
            self.by_base.setdefault(p.split("/")[-1], []).append(p)
        mk = ROOT / "Makefile"
        self.make_targets = set(re.findall(
            r"^([a-zA-Z][\w\-]*):", mk.read_text(encoding="utf-8", errors="replace"), re.M
        )) if mk.exists() else set()

    def path(self, p: str, adr_dir: str = "docs/adr") -> tuple[str, str]:
        cands = [p, os.path.normpath(os.path.join(adr_dir, p)).replace("\\", "/")]
        cands += [f"{pre}/{p}" for pre in ("lab", "core", "ops", "docs", "scripts", "tests")]
        for c in cands:
            c = c.lstrip("./")
            if c in self.u or c in self.dirs or (ROOT / c).exists():
                return "EXISTS", c
        hits = self.by_base.get(p.split("/")[-1], [])
        if len(hits) == 1:
            return "MOVED", hits[0]
        if len(hits) > 1:
            return "AMBIGUOUS", f"{len(hits)} candidates"
        return "MISSING", p

    def cmd(self, c: str) -> tuple[str, str]:
        toks = c.split()
        if toks[0] == "make":
            return ("EXISTS" if len(toks) > 1 and toks[1] in self.make_targets
                    else "MISSING"), c
        if toks[0] == "pytest":
            return self.path(toks[1])[0], c
        rest = toks[2:] if len(toks) > 1 and toks[1] == "-m" else toks[1:]
        if not rest:
            return "MISSING", c
        tgt = rest[0]
        if len(toks) > 1 and toks[1] == "-m" and "/" not in tgt:
            mod = tgt.replace(".", "/")
            for cand in (f"{mod}.py", f"{mod}/__init__.py", mod):
                if cand in self.u or cand in self.dirs:
                    return "EXISTS", c
                for pre in ("ops", "lab", "core", "scripts"):
                    if f"{pre}/{cand}" in self.u or f"{pre}/{cand}" in self.dirs:
                        return "EXISTS", c
            return "MISSING", c
        return self.path(tgt)[0], c


# --------------------------------------------------------------------------- exemptions

def exempt_self_deletion(full_text: str, token: str) -> bool:
    """The ADR that retires a surface naturally names what it deleted."""
    base = token.split("/")[-1].split()[0]
    for m in re.finditer(re.escape(base), full_text):
        window = full_text[max(0, m.start() - 400): m.end() + 400]
        if DELETION_NEAR.search(window):
            return True
    return False


def exempt_recorded_dormancy(full_text: str) -> bool:
    """The ADR already carries a Rule 11 dormancy record -> already compliant."""
    return bool(DORMANCY.search(full_text))


# --------------------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 on findings (default: WARN-tier, always exit 0)")
    ap.add_argument("--stats", action="store_true", help="print the coverage census")
    ap.add_argument("--all", action="store_true", help="also list exempted findings")
    args = ap.parse_args()

    if not ADR_DIR.is_dir():
        print("check_falsifier_reachability: no docs/adr -- skipped")
        return 0

    r = Resolver(build_universe())
    n_adr = n_sec = n_anchored = 0
    findings: list[tuple[str, str, str]] = []
    exempted: list[tuple[str, str, str]] = []

    for f in sorted(ADR_DIR.glob("*.md")):
        if f.name.upper() == "INDEX.MD":
            continue
        n_adr += 1
        text = f.read_text(encoding="utf-8", errors="replace")
        secs = falsifier_sections(text.splitlines())
        if not secs:
            continue
        n_sec += 1
        paths, cmds = set(), set()
        for _, body in secs:
            p, c = extract_inputs(body)
            paths |= p
            cmds |= c
        if not (paths or cmds):
            continue
        n_anchored += 1

        dormant = exempt_recorded_dormancy(text)
        for tok in sorted(paths):
            if r.path(tok)[0] != "MISSING":
                continue
            # Dormancy is checked FIRST: an ADR carrying a Rule 11 record has actually
            # complied, which is a stronger and more accurate reason than the
            # deletion-language heuristic (which also fires on the dormancy note itself).
            if dormant:
                exempted.append((f.name, tok, "dormancy recorded"))
            elif exempt_self_deletion(text, tok):
                exempted.append((f.name, tok, "self-deletion"))
            else:
                findings.append((f.name, tok, "path missing"))
        for tok in sorted(cmds):
            if r.cmd(tok)[0] != "MISSING":
                continue
            # Dormancy is checked FIRST: an ADR carrying a Rule 11 record has actually
            # complied, which is a stronger and more accurate reason than the
            # deletion-language heuristic (which also fires on the dormancy note itself).
            if dormant:
                exempted.append((f.name, tok, "dormancy recorded"))
            elif exempt_self_deletion(text, tok):
                exempted.append((f.name, tok, "self-deletion"))
            else:
                findings.append((f.name, tok, "command target missing"))

    if args.stats:
        pct = 100.0 * n_anchored / n_sec if n_sec else 0.0
        print(f"ADRs scanned              : {n_adr}")
        print(f"carrying a falsifier      : {n_sec}")
        print(f"with a runnable anchor    : {n_anchored} ({pct:.0f}%)")
        print(f"  -> {n_sec - n_anchored} falsifiers are prose-only and UNCHECKABLE here")
        print(f"findings                  : {len(findings)}")
        print(f"exempted                  : {len(exempted)}")
        print()

    if args.all and exempted:
        print("Exempted (no action needed):")
        for adr, tok, why in exempted:
            print(f"  - {adr}: {tok}  [{why}]")
        print()

    if not findings:
        print(f"check_falsifier_reachability: OK "
              f"({n_anchored} anchored falsifier(s), 0 findings, "
              f"{len(exempted)} exempted)")
        print("  NOTE: green != all falsifiers in force. Prose-only limbs and "
              "retired-duty limbs are invisible to this check (see module docstring).")
        return 0

    print("check_falsifier_reachability: WARN -- standing falsifier(s) name a "
          "missing input\n")
    for adr, tok, why in findings:
        print(f"  {adr}")
        print(f"    missing: {tok}  ({why})")
    print(f"\n  {len(findings)} finding(s). Rule 11: append a dated dormancy + re-arm "
          "addendum to the affected ADR;")
    print("  never edit the falsifier text in place.")
    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
