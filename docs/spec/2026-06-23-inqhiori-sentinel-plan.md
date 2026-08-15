# INQHIORI Sentinel (Tier-1) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the deterministic Tier-1 of the INQHIORI Sentinel — a zero-token `ops/sentinel/` scanner that surfaces doc/code skew, near/past dated obligations, and unmet obligation-preconditions into a committed proposal queue, never acting.

**Architecture:** A small `ops/`-layer Python package (`python -m sentinel`) with three pure scan functions over file contents, a markdown report renderer, and a CLI that appends a run block to `docs/notes/sentinel/queue.md`. Scanners **fail-open** (a parse miss yields no finding, never a false positive) because the quarterly LLM probe is the general backstop. Tiers 2–3 (LLM gate + adversarial) are not built here — they are the saved probe workflow, documented as the quarterly procedure.

**Tech Stack:** Python 3.11+, stdlib only (`re`, `dataclasses`, `datetime`, `pathlib`, `argparse`), pytest with `tmp_path`. No first-party imports (boundary-clean: `ops` imports nothing from `lab`/`core`).

**Spec:** `docs/spec/2026-06-23-inqhiori-sentinel-design.md`

---

## File Structure

- Create `ops/sentinel/__init__.py` — package exports.
- Create `ops/sentinel/scan.py` — `Finding` dataclass, the three scanners, module constants.
- Create `ops/sentinel/report.py` — `render_run(asof, findings) -> str`, `QUEUE_PATH`.
- Create `ops/sentinel/__main__.py` — CLI: `--asof`, run scans, append queue, print summary, exit 0.
- Create `tests/test_sentinel.py` — TDD tests (use `tmp_path`, no committed fixtures).
- Modify `Makefile` — add `sentinel` target.
- Create `docs/notes/sentinel/queue.md` — queue header.
- Create `docs/notes/sentinel/README.md` — weekly (`make sentinel`) + quarterly (workflow) usage.
- Create `docs/notes/audits/sentinel-gate-audit.md` — forbidden-D audit-trail stub (written by the quarterly LLM pass, created now so the path exists).

---

## Task 1: Scaffold package + `Finding` + smoke test

**Files:**
- Create: `ops/sentinel/__init__.py`, `ops/sentinel/scan.py`
- Test: `tests/test_sentinel.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_sentinel.py
from datetime import date
from pathlib import Path

from sentinel.scan import Finding, ROUTING


def test_finding_shape():
    f = Finding(id="X", category="skew", routing="Action", summary="s", source="CLAUDE.md:1", next_step="n")
    assert f.routing in ROUTING
    assert f.category == "skew"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_sentinel.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'sentinel'`

- [ ] **Step 3: Write minimal implementation**

```python
# ops/sentinel/scan.py
"""INQHIORI Sentinel — Tier-1 deterministic scanners (no LLM, report-only).

Reads repo files and emits Findings. Fails open: a parse miss yields no finding,
never a false positive. The quarterly LLM probe is the general backstop.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

ROUTING = ("Action", "Forward", "Closed")


@dataclass(frozen=True)
class Finding:
    id: str
    category: str       # "skew" | "obligation" | "precondition"
    routing: str        # one of ROUTING
    summary: str
    source: str         # "path:line" or "path"
    next_step: str


def _read(root: Path, rel: str) -> str:
    p = root / rel
    return p.read_text(encoding="utf-8") if p.exists() else ""


def _line_of(text: str, needle: str) -> int:
    for i, line in enumerate(text.splitlines(), 1):
        if needle in line:
            return i
    return 0
```

```python
# ops/sentinel/__init__.py
from sentinel.scan import Finding, ROUTING, skew_scan, obligation_scan, precondition_scan
from sentinel.report import render_run, QUEUE_PATH

__all__ = [
    "Finding", "ROUTING",
    "skew_scan", "obligation_scan", "precondition_scan",
    "render_run", "QUEUE_PATH",
]
```

Note: `__init__.py` imports names not yet defined (`skew_scan`, `render_run`, …). Leave the `__init__.py` import line for `scan`'s `Finding`/`ROUTING` only for now, OR create stub modules. To keep Step 4 green, replace `__init__.py` with the minimal version below until later tasks add the rest:

```python
# ops/sentinel/__init__.py  (minimal until Tasks 2-5 land)
from sentinel.scan import Finding, ROUTING

__all__ = ["Finding", "ROUTING"]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_sentinel.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add ops/sentinel/__init__.py ops/sentinel/scan.py tests/test_sentinel.py
git commit -m "feat(sentinel): scaffold Tier-1 package + Finding dataclass"
```

---

## Task 2: `skew_scan` — doc/code skew (C1 regression)

**Files:**
- Modify: `ops/sentinel/scan.py`
- Test: `tests/test_sentinel.py`

- [ ] **Step 1: Write the failing tests**

```python
# append to tests/test_sentinel.py
from sentinel.scan import skew_scan


def _write(root: Path, rel: str, text: str) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def test_skew_detects_headroom_retraction(tmp_path):
    _write(tmp_path, "CLAUDE.md", "anchor: 99.83% pass; p99 DD 0.63pp headroom; tighter than prior.\n")
    _write(tmp_path, "docs/mc_anchor_history.md",
           "Q-SWAP-2 ... provisionally retracted ... under fixed-1R modeling (0.45pp).\n")
    findings = skew_scan(tmp_path)
    assert len(findings) == 1
    assert findings[0].id == "SKEW-headroom-fixed1r"
    assert findings[0].category == "skew"
    assert findings[0].routing == "Action"
    assert findings[0].source.startswith("CLAUDE.md:")


def test_skew_clean_when_caveat_present(tmp_path):
    # The headroom line itself carries the fixed-1R caveat -> already remediated -> no finding.
    _write(tmp_path, "CLAUDE.md",
           "anchor: 99.83% pass; p99 DD 0.63pp headroom (under fixed-1R per M-SWAP-1: 0.45pp).\n")
    _write(tmp_path, "docs/mc_anchor_history.md",
           "Q-SWAP-2 ... provisionally retracted ... under fixed-1R modeling.\n")
    assert skew_scan(tmp_path) == []


def test_skew_clean_when_no_retraction_in_history(tmp_path):
    _write(tmp_path, "CLAUDE.md", "anchor: p99 DD 0.63pp headroom.\n")
    _write(tmp_path, "docs/mc_anchor_history.md", "no retraction here.\n")
    assert skew_scan(tmp_path) == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_sentinel.py -k skew -v`
Expected: FAIL — `ImportError: cannot import name 'skew_scan'`

- [ ] **Step 3: Write minimal implementation**

```python
# append to ops/sentinel/scan.py

# Registry of "retraction skews": a canonical claim whose source-of-truth has
# superseded/retracted it but whose canonical line carries no caveat token.
# v1 ships the one proven case (C1); add entries here (<=6) as new skews are found.
_RETRACTION_CHECKS = (
    {
        "id": "SKEW-headroom-fixed1r",
        "canonical_needle": "p99 DD 0.63pp headroom",
        "history_needles": ("provisionally retracted", "fixed-1R"),
        "caveat_token": "fixed-1R",
        "summary": (
            "CLAUDE.md asserts 'p99 DD 0.63pp headroom' with no fixed-1R caveat, but "
            "docs/mc_anchor_history.md (Q-SWAP-2) provisionally retracted that margin to "
            "0.45pp under fixed-1R modeling (M-SWAP-1). Lock criterion still passes (4.55% < 5%)."
        ),
        "next_step": (
            "Append a fixed-1R caveat + Q-SWAP-2 cross-ref to the headroom line at CLAUDE.md, "
            "mirroring the regime (line 62) and gross-of-swap (line 54) caveats already inline."
        ),
    },
)


def skew_scan(root: Path) -> list[Finding]:
    """Detect canonical claims whose source-of-truth retracted them, uncaveated."""
    findings: list[Finding] = []
    claude = _read(root, "CLAUDE.md")
    history = _read(root, "docs/mc_anchor_history.md")
    lines = claude.splitlines()
    for chk in _RETRACTION_CHECKS:
        needle = chk["canonical_needle"]
        if needle not in claude:
            continue
        if not all(h in history for h in chk["history_needles"]):
            continue
        ln = _line_of(claude, needle)
        canonical_line = lines[ln - 1] if 0 < ln <= len(lines) else ""
        if chk["caveat_token"] in canonical_line:
            continue  # already caveated on the claim line -> remediated
        findings.append(Finding(
            id=chk["id"], category="skew", routing="Action",
            summary=chk["summary"], source=f"CLAUDE.md:{ln}", next_step=chk["next_step"],
        ))
    return findings
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_sentinel.py -k skew -v`
Expected: PASS (3 tests)

- [ ] **Step 5: Commit**

```bash
git add ops/sentinel/scan.py tests/test_sentinel.py
git commit -m "feat(sentinel): skew_scan with C1 headroom-retraction regression check"
```

---

## Task 3: `obligation_scan` — near/past dated obligations (C2 part 1)

**Files:**
- Modify: `ops/sentinel/scan.py`
- Test: `tests/test_sentinel.py`

- [ ] **Step 1: Write the failing tests**

```python
# append to tests/test_sentinel.py
from sentinel.scan import obligation_scan


def test_obligation_surfaces_near_date(tmp_path):
    _write(tmp_path, "CLAUDE.md",
           "Forward revert trigger: run regime-check quarterly (next dates: 2026-08-08, 2026-11-08).\n")
    findings = obligation_scan(tmp_path, asof=date(2026, 6, 23), horizon_days=60)
    ids = {f.id for f in findings}
    assert any("2026-08-08" in f.summary for f in findings)
    assert all(f.category == "obligation" for f in findings)
    assert all(f.routing in ("Action", "Forward") for f in findings)


def test_obligation_ignores_far_date(tmp_path):
    _write(tmp_path, "CLAUDE.md", "review trigger next: 2026-11-08.\n")
    assert obligation_scan(tmp_path, asof=date(2026, 6, 23), horizon_days=60) == []


def test_obligation_requires_keyword(tmp_path):
    # A bare date with no obligation keyword on the line must not fire (avoids ADR-date noise).
    _write(tmp_path, "CLAUDE.md", "The lock landed on 2026-08-08 after testing.\n")
    assert obligation_scan(tmp_path, asof=date(2026, 6, 23), horizon_days=60) == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_sentinel.py -k obligation -v`
Expected: FAIL — `ImportError: cannot import name 'obligation_scan'`

- [ ] **Step 3: Write minimal implementation**

```python
# append to ops/sentinel/scan.py

# Files where dated obligations legitimately live. Curated to avoid ADR-date noise.
_OBLIGATION_FILES = (
    "CLAUDE.md",
    "ops/reference/regime_calendar.md",
    "docs/notes/audits/rule-2-trip-log.md",
)
_OBLIGATION_KW = ("next", "trigger", "review", "due", "slate", "audit", "gate", "quarterly")
_ISO_DATE = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")


def obligation_scan(root: Path, asof: date, horizon_days: int = 60) -> list[Finding]:
    """Flag dated obligations within `horizon_days` of `asof`, or already past."""
    findings: list[Finding] = []
    horizon = asof + timedelta(days=horizon_days)
    seen: set[tuple[str, str]] = set()
    for rel in _OBLIGATION_FILES:
        text = _read(root, rel)
        for ln, line in enumerate(text.splitlines(), 1):
            low = line.lower()
            if not any(kw in low for kw in _OBLIGATION_KW):
                continue
            for m in _ISO_DATE.finditer(line):
                try:
                    d = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
                except ValueError:
                    continue
                if not (asof <= d <= horizon):
                    continue
                key = (rel, d.isoformat())
                if key in seen:
                    continue
                seen.add(key)
                days = (d - asof).days
                findings.append(Finding(
                    id=f"OBLIG-{d.isoformat()}",
                    category="obligation", routing="Action" if days <= 14 else "Forward",
                    summary=f"Dated obligation {d.isoformat()} is {days}d out — \"{line.strip()[:100]}\"",
                    source=f"{rel}:{ln}",
                    next_step="Confirm the obligation is scheduled and its inputs are ready (see precondition findings).",
                ))
    return findings
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_sentinel.py -k obligation -v`
Expected: PASS (3 tests)

- [ ] **Step 5: Commit**

```bash
git add ops/sentinel/scan.py tests/test_sentinel.py
git commit -m "feat(sentinel): obligation_scan for near/past dated obligations"
```

---

## Task 4: `precondition_scan` — unmet inputs for the slate (C2 part 2)

**Files:**
- Modify: `ops/sentinel/scan.py`
- Test: `tests/test_sentinel.py`

- [ ] **Step 1: Write the failing tests**

```python
# append to tests/test_sentinel.py
from sentinel.scan import precondition_scan, SLATE_DATE


def test_precondition_flags_unverified_calendar(tmp_path):
    _write(tmp_path, "ops/reference/regime_calendar.md",
           "| 2025 | ... | [M] |\n| 2026 | ... | [L] |\n"
           "Maintenance: one verification pass on [M]/[L] cells is due before the 2026-08-08 slate.\n")
    findings = precondition_scan(tmp_path, asof=date(2026, 6, 23), horizon_days=60)
    ids = {f.id for f in findings}
    assert "PRECOND-regime-calendar-unverified" in ids
    assert all(f.category == "precondition" for f in findings)


def test_precondition_flags_empty_trip_log(tmp_path):
    _write(tmp_path, "docs/notes/audits/rule-2-trip-log.md",
           "| Date | Loop class | ... |\n|---|---|---|\n| 2026-06-16 | OUTER | baseline |\n")
    findings = precondition_scan(tmp_path, asof=date(2026, 6, 23), horizon_days=60)
    assert "PRECOND-rule2-triplog-starved" in {f.id for f in findings}


def test_precondition_clean_when_met(tmp_path):
    _write(tmp_path, "ops/reference/regime_calendar.md", "| 2025 | ... | [H] |\n| 2026 | ... | [H] |\n")
    _write(tmp_path, "docs/notes/audits/rule-2-trip-log.md",
           "|---|\n| 2026-06-16 | OUTER | a |\n| 2026-06-20 | INNER | b |\n")
    assert precondition_scan(tmp_path, asof=date(2026, 6, 23), horizon_days=60) == []


def test_precondition_dormant_far_from_slate(tmp_path):
    # More than horizon before the slate -> dormant, no finding even if inputs unmet.
    _write(tmp_path, "ops/reference/regime_calendar.md", "| 2026 | ... | [L] |\nverification due before 2026-08-08.\n")
    assert precondition_scan(tmp_path, asof=date(2026, 1, 1), horizon_days=60) == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_sentinel.py -k precondition -v`
Expected: FAIL — `ImportError: cannot import name 'precondition_scan'`

- [ ] **Step 3: Write minimal implementation**

```python
# append to ops/sentinel/scan.py

# The next dated slate whose preconditions v1 tracks explicitly (C2). Generalizing
# precondition discovery from obligation_scan output is future work (spec §9).
SLATE_DATE = date(2026, 8, 8)


def precondition_scan(root: Path, asof: date, horizon_days: int = 60) -> list[Finding]:
    """Check known inputs for the next slate are ready, when the slate is within horizon."""
    findings: list[Finding] = []
    if not (asof <= SLATE_DATE <= asof + timedelta(days=horizon_days)):
        return findings  # slate dormant -> preconditions not yet load-bearing

    cal = _read(root, "ops/reference/regime_calendar.md")
    if cal and ("[M]" in cal or "[L]" in cal):
        ln = _line_of(cal, "[L]") or _line_of(cal, "[M]")
        findings.append(Finding(
            id="PRECOND-regime-calendar-unverified", category="precondition", routing="Action",
            summary=f"regime_calendar.md still has unverified [M]/[L] cells; a verification pass is due before the {SLATE_DATE.isoformat()} slate.",
            source=f"ops/reference/regime_calendar.md:{ln}",
            next_step="Verify the [M]/[L] regime-calendar cells (2025, 2026) before the slate date.",
        ))

    log = _read(root, "docs/notes/audits/rule-2-trip-log.md")
    if log:
        data_rows = [l for l in log.splitlines() if re.match(r"\s*\|\s*\d{4}-\d{2}-\d{2}\s*\|", l)]
        if len(data_rows) < 2:
            findings.append(Finding(
                id="PRECOND-rule2-triplog-starved", category="precondition", routing="Action",
                summary=f"rule-2-trip-log.md has {len(data_rows)} data row(s); the {SLATE_DATE.isoformat()} programme audit's Rule-2 graduation check needs >=1 entry per active loop class.",
                source="docs/notes/audits/rule-2-trip-log.md",
                next_step="Decide the Rule-2 first-wire / trip-log policy before the slate so the graduation check runs on real inputs.",
            ))
    return findings
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_sentinel.py -k precondition -v`
Expected: PASS (4 tests)

- [ ] **Step 5: Commit**

```bash
git add ops/sentinel/scan.py tests/test_sentinel.py
git commit -m "feat(sentinel): precondition_scan for slate input-readiness"
```

---

## Task 5: `report.render_run` + CLI + queue files

**Files:**
- Create: `ops/sentinel/report.py`, `ops/sentinel/__main__.py`, `docs/notes/sentinel/queue.md`, `docs/notes/sentinel/README.md`, `docs/notes/audits/sentinel-gate-audit.md`
- Modify: `ops/sentinel/__init__.py`
- Test: `tests/test_sentinel.py`

- [ ] **Step 1: Write the failing tests**

```python
# append to tests/test_sentinel.py
from sentinel.report import render_run


def test_render_run_empty_is_no_findings(tmp_path):
    out = render_run(asof=date(2026, 6, 23), findings=[])
    assert "2026-06-23" in out
    assert "no findings" in out.lower()


def test_render_run_lists_findings_grouped(tmp_path):
    f = Finding(id="SKEW-x", category="skew", routing="Action", summary="s", source="CLAUDE.md:80", next_step="n")
    out = render_run(asof=date(2026, 6, 23), findings=[f])
    assert "SKEW-x" in out and "Action" in out and "CLAUDE.md:80" in out


def test_render_run_is_deterministic(tmp_path):
    f = Finding(id="OBLIG-2026-08-08", category="obligation", routing="Forward", summary="s", source="CLAUDE.md:82", next_step="n")
    assert render_run(date(2026, 6, 23), [f]) == render_run(date(2026, 6, 23), [f])
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_sentinel.py -k render -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'sentinel.report'`

- [ ] **Step 3: Write minimal implementation**

```python
# ops/sentinel/report.py
"""Render a Sentinel run as a markdown block appended to the proposal queue."""
from __future__ import annotations

from datetime import date

from sentinel.scan import Finding

QUEUE_PATH = "docs/notes/sentinel/queue.md"
_ORDER = ("Action", "Forward", "Closed")


def render_run(asof: date, findings: list[Finding]) -> str:
    lines = [f"## Run {asof.isoformat()}", ""]
    if not findings:
        lines += ["_No findings — repo clean for skew / obligations / preconditions._", ""]
        return "\n".join(lines)
    for routing in _ORDER:
        bucket = [f for f in findings if f.routing == routing]
        if not bucket:
            continue
        lines.append(f"### {routing}")
        for f in sorted(bucket, key=lambda x: x.id):
            lines.append(f"- **{f.id}** [{f.category}] — {f.summary}")
            lines.append(f"  - source: `{f.source}`")
            lines.append(f"  - next: {f.next_step}")
        lines.append("")
    return "\n".join(lines)
```

```python
# ops/sentinel/__main__.py
"""Sentinel CLI — Tier-1 deterministic run. Report-only; always exits 0."""
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from sentinel.report import QUEUE_PATH, render_run
from sentinel.scan import obligation_scan, precondition_scan, skew_scan


def _repo_root() -> Path:
    # ops/sentinel/__main__.py -> repo root is three parents up.
    return Path(__file__).resolve().parents[2]


def main() -> int:
    ap = argparse.ArgumentParser(prog="sentinel", description="INQHIORI Sentinel — Tier-1 hygiene scan (report-only).")
    ap.add_argument("--asof", default=None, help="YYYY-MM-DD (default: today)")
    ap.add_argument("--horizon-days", type=int, default=60)
    ap.add_argument("--root", default=None, help="repo root (default: inferred)")
    args = ap.parse_args()

    asof = date.fromisoformat(args.asof) if args.asof else date.today()
    root = Path(args.root) if args.root else _repo_root()

    findings = (
        skew_scan(root)
        + obligation_scan(root, asof=asof, horizon_days=args.horizon_days)
        + precondition_scan(root, asof=asof, horizon_days=args.horizon_days)
    )
    block = render_run(asof, findings)

    queue = root / QUEUE_PATH
    queue.parent.mkdir(parents=True, exist_ok=True)
    prior = queue.read_text(encoding="utf-8") if queue.exists() else "# Sentinel proposal queue\n\n_Reverse-chron. Report-only; the operator authorizes every item._\n"
    # Prepend newest run under the header (reverse-chron).
    head, _, rest = prior.partition("\n\n")
    queue.write_text(f"{head}\n\n{block}\n{rest}", encoding="utf-8")

    print(f"sentinel: {len(findings)} finding(s) at asof {asof.isoformat()} -> {QUEUE_PATH}")
    for f in findings:
        print(f"  [{f.routing}] {f.id} ({f.source})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Update `ops/sentinel/__init__.py` to the full export set:

```python
# ops/sentinel/__init__.py
from sentinel.scan import Finding, ROUTING, skew_scan, obligation_scan, precondition_scan, SLATE_DATE
from sentinel.report import render_run, QUEUE_PATH

__all__ = [
    "Finding", "ROUTING", "SLATE_DATE",
    "skew_scan", "obligation_scan", "precondition_scan",
    "render_run", "QUEUE_PATH",
]
```

Create the queue + docs stubs:

```markdown
<!-- docs/notes/sentinel/queue.md -->
# Sentinel proposal queue

_Reverse-chron. Report-only; the operator authorizes every item (Action = do it, Forward = schedule it, Closed = log it)._
```

```markdown
<!-- docs/notes/sentinel/README.md -->
# INQHIORI Sentinel

Periodic methodology-hygiene + obligation-readiness loop. Proposes, never acts. Design: `docs/spec/2026-06-23-inqhiori-sentinel-design.md`.

- **Weekly (Tier-1, deterministic, zero-token):** `make sentinel` — appends a run block to `queue.md`.
- **Quarterly (full LLM probe):** operator-invoked workflow (the saved `inqhiori-probe-iteration-1` script), co-scheduled with the 2026-08-08 regime slate. Forbidden-D flags log to `docs/notes/audits/sentinel-gate-audit.md`.

Steady-state is a near-empty queue. A burst of "new directions" is a degeneration signal, not a win.
```

```markdown
<!-- docs/notes/audits/sentinel-gate-audit.md -->
# Sentinel gate-audit — forbidden-D-test log

**Purpose.** The safety audit trail for the Sentinel's quarterly LLM gate. One row per forbidden-D-test the gate was tempted by and refused (e.g. "signal-to-noise is high", "fits my model", "known mechanism"). Mirrors `rule-2-trip-log.md` — one table, not a subsystem.

| Date | Run | Forbidden D-test tempted | What it would have deleted | Disposition (retained + routing) |
|---|---|---|---|---|
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_sentinel.py -k render -v`
Expected: PASS (3 tests)

- [ ] **Step 5: Commit**

```bash
git add ops/sentinel/ tests/test_sentinel.py docs/notes/sentinel/ docs/notes/audits/sentinel-gate-audit.md
git commit -m "feat(sentinel): render_run + CLI + queue/audit scaffolding"
```

---

## Task 6: Makefile target + real-repo acceptance + green gates

**Files:**
- Modify: `Makefile`
- Test: real-repo run + full suite + boundary check

- [ ] **Step 1: Add the Makefile target**

Add to `.PHONY` line and append a target (mirrors the `ecr` idiom):

```makefile
.PHONY: sentinel
sentinel:
	@PYTHONPATH=ops python -m sentinel --asof $(or $(ASOF),$(shell python -c "import datetime;print(datetime.date.today())"))
```

- [ ] **Step 2: Acceptance — run on the real repo at the verified asof**

Run: `PYTHONPATH=ops python -m sentinel --asof 2026-06-23 --root .`
Expected: stdout lists at least:
- `[Action] SKEW-headroom-fixed1r (CLAUDE.md:80)`
- `[Forward] OBLIG-2026-08-08 (CLAUDE.md:82)` (or `:80`-region line carrying the date)
- `[Action] PRECOND-regime-calendar-unverified (ops/reference/regime_calendar.md:…)`
- `[Action] PRECOND-rule2-triplog-starved (docs/notes/audits/rule-2-trip-log.md)`

And `docs/notes/sentinel/queue.md` gains a `## Run 2026-06-23` block listing them. This is the §10 acceptance criterion (surfaces C1 + C2).

- [ ] **Step 3: Boundary + full test suite green**

Run: `python scripts/check_boundaries.py && python -m pytest tests/test_sentinel.py -v && python -m pytest tests/ -q`
Expected: boundaries OK (ops imports no lab); sentinel tests PASS; full suite no new failures.

- [ ] **Step 4: Commit**

```bash
git add Makefile docs/notes/sentinel/queue.md
git commit -m "feat(sentinel): make sentinel target + real-repo acceptance run"
```

- [ ] **Step 5: (operator-gated) C1 remediation is a queue item, not part of this build**

Do NOT auto-edit `CLAUDE.md` here. The `SKEW-headroom-fixed1r` finding is delivered to the queue for the operator to authorize. Once the operator applies the caveat, re-running `make sentinel` must show the finding cleared (regression closed) — that is the live proof the scanner tracks remediation.

---

## Self-Review

- **Spec coverage:** §3 Tier-1 → Tasks 1–5; §4.1 three scanners → Tasks 2–4; §4.2 queue + gate-audit → Task 5; §6 Makefile/cadence → Task 6; §8 tests (C1/C2 fixtures) → Tasks 2–4 tests; §10 acceptance → Task 6 Step 2. Tiers 2–3 are explicitly out of build scope (reuse workflow) per §3 — covered by the `README.md` + `sentinel-gate-audit.md` stub in Task 5, no code task. ✓
- **Placeholder scan:** every code step contains complete, runnable code; no TBD/TODO. ✓
- **Type consistency:** `Finding(id, category, routing, summary, source, next_step)` identical across scan.py, report.py, __main__.py, and all tests; `skew_scan(root)`, `obligation_scan(root, asof, horizon_days)`, `precondition_scan(root, asof, horizon_days)`, `render_run(asof, findings)`, `SLATE_DATE` consistent throughout. ✓
- **Fail-open:** every scanner returns `[]` on missing/unparseable inputs (no exceptions thrown to the CLI). ✓
