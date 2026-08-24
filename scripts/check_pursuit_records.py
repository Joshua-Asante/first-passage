#!/usr/bin/env python3
"""check_pursuit_records.py — GRAND-tier pursuit-record limbs (ADR 2026-08-09).

RETIRED FROM scripts/gates.yml 2026-08-24 (Rule 16 R5 — docs/operational_rules.md;
see docs/adr/2026-08-24-validation-battery-k-tiering-and-gate-retirement.md): every
reachable exit path in main() below returns 0, so as invoked by the gate this check
could never fail regardless of tier. Retained on disk and still runnable manually
(`python scripts/check_pursuit_records.py`); no longer wired into any gate tier.

THE FAILURE MODE (docs/adr/2026-08-09-grand-tier-quintessentials-binding.md
§2.3 / §2.5 / §10; first firing corrected during GSUB-1 — trap M-AHF):

  Pursuit parks lacked re-entry conditions and expiries; KEEP intake had no
  entry-record fields; an unscoped `grep -rL "re-entry:" docs/pursuits/` flagged
  every KEEP/SUBTRACT/MERGE record that correctly lacks the field. Hooks were
  tested against the author's mental form, not the artifact's stored form.

THE MECHANICAL RULE (deliberately narrow — M-8):

  1. park-completeness — every record whose Standing is PARK must carry both a
     named `re-entry:` condition and an `expiry:` date (scoped by standing).
  2. expiry-enforcement — a PARK whose `expiry:` date is strictly before --asof
     is reported (ADR §2.3: converts to SUBTRACT absent operator renewal).
  3. entry-record — every KEEP must carry Aim served, Measure, Survive bound,
     and a Review date (§2.5).
  4. standing-vocabulary — Standing must open with KEEP / PARK / MERGE /
     SUBTRACT (optional qualifier) or the e2 terminal form `no action`.
  5. ledger-pointer — every KEEP whose Class is (d) meta-belt (subscription) or
     (d) meta-belt (venue account) must reference SUBSCRIPTION_LEDGER.md
     somewhere in its body (§2.5-adjacent; added 2026-08-21 per the CFO's
     C-1-closure recommendation, docs/adr/2026-08-21-cfo-subscription-
     ledger-consolidation.md D2).

SEVERITY:

  Default every limb to WARN / report-only (exit 0). Do NOT silently HARD-gate —
  the 2026-08-08 quarterly audit graded belt-churn YELLOW; gate composition is
  owned by scripts/gates.yml via gate_manifest.py. Wiring is an operator
  decision, proposed in the landing report, not landed here.

SCOPE:
  docs/pursuits/*.md  (one markdown file per pursuit; created by GSUB-1 Phase 4)

Exit 0 always on scan completion (WARN-tier). Exit 2 only on CLI misuse
(e.g. malformed --asof).
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PURSUITS_DIR = REPO / "docs" / "pursuits"
OWNING_ADR = (
    REPO / "docs" / "adr" / "2026-08-09-grand-tier-quintessentials-binding.md"
)

STANDING_BLOCK = re.compile(
    r"\*\*Standing:\*\*\s*(?P<body>.+?)(?=\n\*\*[A-Za-z]|\Z)",
    re.DOTALL,
)
STANDING_TOKEN = re.compile(
    r"^(?P<tok>KEEP|PARK|MERGE|SUBTRACT(?:-complete)?|no\s+action)\b",
    re.IGNORECASE,
)

RE_ENTRY_FIELD = re.compile(r"(?im)^\*\*re-entry:\*\*\s*\S|^re-entry:\s*\S")
EXPIRY_FIELD = re.compile(r"(?im)^\*\*expiry:\*\*|^expiry:")
EXPIRY_DATE = re.compile(
    r"(?im)(?:^\*\*expiry:\*\*|^expiry:)\s*[^\n]*?(?P<d>\d{4}-\d{2}-\d{2})"
)
CLASS_LEDGER_TRACKED = re.compile(
    r"(?m)^\*\*Class:\*\*.*\(d\)\s*meta-belt\s*\((subscription|venue account)",
    re.IGNORECASE,
)
LEDGER_POINTER = re.compile(r"SUBSCRIPTION_LEDGER\.md")
LEDGER_FILENAME = "SUBSCRIPTION_LEDGER.md"

KEEP_FIELDS = (
    ("Aim served", re.compile(r"(?m)^\*\*Aim served:\*\*")),
    ("Measure", re.compile(r"(?m)^\*\*Measure:\*\*")),
    ("Survive bound", re.compile(r"(?m)^\*\*Survive bound:\*\*")),
    ("Review date", re.compile(r"(?im)^\*\*Review date:\*\*")),
)


class Finding:
    """WARN finding. Plain class (not dataclass) so importlib-loaded tests on
    Python 3.14 do not trip dataclasses' sys.modules lookup."""

    __slots__ = ("severity", "limb", "path", "message")

    def __init__(self, severity: str, limb: str, path: Path, message: str) -> None:
        self.severity = severity
        self.limb = limb
        self.path = path
        self.message = message

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Finding):
            return NotImplemented
        return (
            self.severity == other.severity
            and self.limb == other.limb
            and self.path == other.path
            and self.message == other.message
        )

    def render(self) -> str:
        try:
            shown = self.path.relative_to(REPO)
        except ValueError:
            shown = self.path
        return f"{self.severity} pursuit-records[{self.limb}]: {shown}: {self.message}"


def parse_standing(text: str) -> str | None:
    """Return the canonical standing token, or None if the field is absent."""
    m = STANDING_BLOCK.search(text)
    if not m:
        return None
    body = " ".join(m.group("body").split())
    tok = STANDING_TOKEN.match(body)
    if not tok:
        return body.split()[0] if body.strip() else None
    raw = tok.group("tok")
    if raw.lower() == "no action":
        return "no action"
    if raw.upper().startswith("SUBTRACT"):
        return "SUBTRACT" if raw.upper() == "SUBTRACT" else raw.upper()
    return raw.upper()


def standing_vocabulary_ok(text: str) -> bool:
    m = STANDING_BLOCK.search(text)
    if not m:
        return False
    body = " ".join(m.group("body").split())
    return STANDING_TOKEN.match(body) is not None


def parse_expiry(text: str) -> date | None:
    m = EXPIRY_DATE.search(text)
    if not m:
        return None
    try:
        return date.fromisoformat(m.group("d"))
    except ValueError:
        return None


def scan_file(path: Path, asof: date) -> list[Finding]:
    """Return WARN findings for one pursuit record."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"WARN pursuit-records: cannot read {path}: {exc}")
        return []

    findings: list[Finding] = []

    if not standing_vocabulary_ok(text):
        m = STANDING_BLOCK.search(text)
        shown = (
            " ".join(m.group("body").split())[:80]
            if m
            else "(missing **Standing:** field)"
        )
        findings.append(
            Finding(
                "WARN",
                "standing-vocabulary",
                path,
                f"Standing must be KEEP/PARK/MERGE/SUBTRACT (optional qualifier) "
                f"or 'no action'; got {shown!r}",
            )
        )

    standing = parse_standing(text)

    if standing == "PARK":
        if not RE_ENTRY_FIELD.search(text):
            findings.append(
                Finding(
                    "WARN",
                    "park-completeness",
                    path,
                    "PARK missing named re-entry: condition (ADR §2.3 / §10)",
                )
            )
        if not EXPIRY_FIELD.search(text):
            findings.append(
                Finding(
                    "WARN",
                    "park-completeness",
                    path,
                    "PARK missing expiry: date (ADR §2.3 / §10)",
                )
            )
        else:
            exp = parse_expiry(text)
            if exp is None:
                findings.append(
                    Finding(
                        "WARN",
                        "park-completeness",
                        path,
                        "PARK expiry: present but no YYYY-MM-DD date parsed",
                    )
                )
            elif exp < asof:
                findings.append(
                    Finding(
                        "WARN",
                        "expiry-enforcement",
                        path,
                        f"PARK expired on {exp.isoformat()} (asof {asof.isoformat()}); "
                        f"converts to SUBTRACT absent explicit operator renewal "
                        f"(ADR §2.3)",
                    )
                )

    if standing == "KEEP":
        for label, pat in KEEP_FIELDS:
            if not pat.search(text):
                findings.append(
                    Finding(
                        "WARN",
                        "entry-record",
                        path,
                        f"KEEP missing **{label}:** (ADR §2.5 intake rule)",
                    )
                )
        if CLASS_LEDGER_TRACKED.search(text) and not LEDGER_POINTER.search(text):
            findings.append(
                Finding(
                    "WARN",
                    "ledger-pointer",
                    path,
                    "subscription/venue-account-class KEEP missing a SUBSCRIPTION_LEDGER.md "
                    "pointer (CFO 2026-08-21 recommendation — $/mo tracked at row-creation "
                    "time, not backfilled later; see docs/adr/2026-08-21-"
                    "cfo-subscription-ledger-consolidation.md D2)",
                )
            )

    return findings


def in_scope(pursuits_dir: Path = PURSUITS_DIR) -> list[Path]:
    if not pursuits_dir.is_dir():
        return []
    return sorted(
        p for p in pursuits_dir.glob("*.md")
        if p.name not in {LEDGER_FILENAME, "README.md"}
    )


def scan_paths(paths: list[Path], asof: date) -> list[Finding]:
    out: list[Finding] = []
    for p in paths:
        out.extend(scan_file(p, asof))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="check_pursuit_records",
        description=(
            "GRAND-tier pursuit-record limbs (park completeness, expiry, "
            "KEEP entry-record, standing vocabulary). Report-only WARN; exit 0."
        ),
    )
    ap.add_argument(
        "--asof",
        default=None,
        help="YYYY-MM-DD for PARK expiry enforcement (default: today)",
    )
    ap.add_argument(
        "paths",
        nargs="*",
        help="optional explicit pursuit files (default: docs/pursuits/*.md)",
    )
    args = ap.parse_args(None if argv is None else argv)

    try:
        asof = date.fromisoformat(args.asof) if args.asof else date.today()
    except ValueError:
        print(f"ERROR: --asof must be YYYY-MM-DD, got {args.asof!r}", file=sys.stderr)
        return 2

    paths = [Path(p) for p in args.paths] if args.paths else in_scope()
    findings = scan_paths(paths, asof)

    if findings:
        for f in findings:
            print(f.render())
        print(
            f"check_pursuit_records: {len(findings)} warning(s) at asof "
            f"{asof.isoformat()} — WARN-tier (report-only); gate wiring is an "
            f"operator decision (see {OWNING_ADR.name} §10)."
        )
        return 0

    print(
        f"check_pursuit_records: OK — {len(paths)} pursuit record(s) clean at "
        f"asof {asof.isoformat()}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
