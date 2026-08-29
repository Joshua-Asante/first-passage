# SSOT / Data-Lineage Remediation Program — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Governance note (repo-specific):** this repo requires ADR ratification for any decision that "creates or amends doctrine — a rule, gate, falsifier threshold, or convention that binds future work" (limb-4 tier test, `docs/adr/2026-08-08-adr-ceremony-tiering.md`). Phase 0 of this plan therefore ends in an ADR, authored per the `brief-authoring` skill's `adr.md` template, not a bare code diff. Do not skip straight to Phase 1 code without an operator GO on the Phase 0 ADR — that GO is this program's ratification gate.

**Goal:** Close the concrete, already-identified single-source-of-truth (SSOT) and data-lineage gaps in First Passage's governance/tracking surfaces (STATE.md, `lab/CATALOG.md`, the rejection registers, the skill-deploy pipeline, the ADR-falsifier corpus) using the repo's own proven "generator, do-not-hand-edit" pattern and its existing coherence-campaign audit methodology — not a new framework invented from scratch.

**Architecture:** Extend three things the repo already has working, rather than build new infrastructure: (1) the generator-script pattern already proven by `archive_lab_analysis.py` (CATALOG), `check_adr_graph.py` (ADR INDEX), and `gate_manifest.py` (gate roster); (2) the `gates.yml` / `gate_manifest.py` wiring path, which is the one mechanism that actually makes a check *bound* rather than merely *authored*; (3) the coherence-campaign audit format (`docs/notes/audits/2026-08-21-coherence-campaign.md`) — findings-first, three finding classes (inconsistency/ambiguity/trap), five dispositions (link/simplify/delete/leave-historical/name-Q), audit hooks, explicit OWED/NAMED/LEFT leftover tracking.

**Tech Stack:** Python 3 (repo's existing `scripts/*.py` checker convention, no new dependencies), pytest, `gate_manifest.py`/`gates.yml`, git, this repo's Markdown ADR/closure/brief conventions.

## Global Constraints

- No agent may place a trade; nothing in this program touches Pine, `dd_protection.py`, `firm_rules.py`, or allocations (out of scope by definition — this is governance/doc tooling, not risk-control code).
- Every new or extended checker must be **mutation-tested before being trusted** — plant the exact bad condition it claims to catch, confirm a non-zero/FAIL actually propagates, per this program's own founding lesson (`lesson_discrete_vs_continuous_execution_reality`'s sibling insight, and the repo's own `check_falsifier_reachability.py` precedent of self-disclosing coverage limits).
- No hand-editing of a file that already has a declared generator (`lab/CATALOG.md`, `docs/adr/INDEX.md`). If a phase needs to change one, it changes the generator.
- Follow Rule 0 (`docs/rule_0.md`): every task's first step is reading the current production file(s) it touches, not trusting this plan's description of them — this plan was scoped 2026-08-27 and some cited facts (schema shapes, exact line numbers) will decay before every phase lands.
- Retention test applies to any new artifact this program creates (`docs/operational_rules.md` §Retention) — don't create a doc that duplicates what an existing owner already carries.
- Plans in this program are saved under `docs/superpowers/plans/`, matching the repo's existing convention (see `docs/superpowers/plans/2026-08-23-viable-strategy-sequence-overview.md` for a worked precedent of a multi-phase overview + per-phase plan files).

---

## Why this program, and why now

A cross-repo mining pass (2026-08-27, see the published "Recurrence Ledger" artifact) found that unverified-claim-propagation, gate-reachability defects, and missing-single-source-of-truth axes were three of the four most-recurring research-methodology problem classes in this repo's post-pivot record (8–9 confirmed instances each). This plan operationalizes the fix for the lineage/SSOT half of that finding.

**What changed between that report and this plan (found during this plan's own Rule-0 pass — see below):**

| Report's cited defect | Current state (verified 2026-08-27) |
|---|---|
| CATALOG conflates `hot` and `disposition` into one status word | **Already fixed.** `docs/adr/2026-08-22-catalog-hot-vs-disposition.md` — Accepted, Phase 1 (parser Verdict-wins rewrite, C2 retarget, `hot` column) landed the same day. Only the §4 falsifier re-check needs periodic re-confirmation. |
| Three competing, unowned rejection registers | **Ownership already ruled.** `docs/adr/2026-08-09-rejection-register-topology-and-bar-wiring.md` D3 assigns each of the three registers a distinct scope with `instrument_profiles.py` as the machine consult. **But D4 — the enforcement instrument that checks every terminal-negative closure naming an instrument actually has a ledger DEAD row — was explicitly deferred ("dispatched as a separate packet, not built here") and is still unbuilt**, against a hard 2026-11-08 falsifier date. |
| Two divergent `check_brief.py` implementations | **Already ruled** (`docs/adr/2026-08-09-check-brief-canon-ruling.md`: skill-side is canonical). **But the skill-side file does not exist on disk right now** — `~/.claude/skills/brief-authoring/` has no `scripts/` directory at all, so every ADR's `Verification` section that pastes `python ~/.claude/skills/brief-authoring/scripts/check_brief.py ...` currently fails with "No such file or directory" if actually run. This is a live, undiagnosed instance of the exact "unverified claim propagates because nobody re-ran the verification block" pattern the report named. |
| Coverage gaps in gate tooling | `check_falsifier_reachability.py` already exists and is a genuinely good example — it self-reports its own coverage eroding (28%→25% over one week in its own docstring) — but it is WARN-tier, **not wired into `gates.yml`**, and not run on any cadence. It is the closest thing this repo has to a standing decay-audit for the whole ADR corpus, sitting unused. |

**Non-goals:** this program does not re-litigate CATALOG's schema (done), does not reopen the rejection-register topology ruling (done), does not touch Pine/risk constants, and does not attempt a second Great-Prune-style bulk deletion pass. It closes what's already been named and ratified, then generalizes the recurring "hand-synced mirror" micro-pattern once Phase 0's audit confirms its current shape.

---

## Phase 0 — Confirm current state, then ratify the program

**Files:**
- Create: `docs/adr/2026-08-27-ssot-data-lineage-remediation-program.md`
- Read (production-source verification, do not trust this plan's descriptions above): `docs/adr/2026-08-09-rejection-register-topology-and-bar-wiring.md`, `docs/adr/2026-08-22-catalog-hot-vs-disposition.md`, `docs/adr/2026-08-09-check-brief-canon-ruling.md`, `docs/notes/audits/2026-08-21-coherence-campaign.md`, `scripts/check_falsifier_reachability.py`, `scripts/gates.yml`, `.claude/skills/brief-authoring/` (in-repo source), `~/.claude/skills/brief-authoring/` (deployed target), `docs/methodology/rejected_signals.md`, `ops/instruments/MNQ.md`

**Interfaces:**
- Produces: the ADR at `docs/adr/2026-08-27-ssot-data-lineage-remediation-program.md`, `Status: Accepted`, which every later phase in this plan cites as its authorizing decision. Phase 1+ tasks may not begin implementation until this ADR's Status is `Accepted` (operator GO).

- [ ] **Step 1: Re-verify the in-repo skill source for check_brief.py**

```bash
find .claude/skills/brief-authoring -type f
```

Expected: confirms whether `scripts/check_brief.py` exists in-repo (the source of truth per `sync_skills.py`'s one-way contract) even though it's missing from the deployed `~/.claude/skills/brief-authoring/` bundle. Record the exact result — this determines whether Phase 1's fix is "redeploy" (file exists in-repo, sync is stale) or "author" (file never existed in-repo either, so the 2026-08-09 canon ruling was never actually implemented).

- [ ] **Step 2: Run the sync-skills drift check**

```bash
python scripts/sync_skills.py --check
```

Expected: non-zero exit and a diff line naming `brief-authoring` (or: confirms drift is elsewhere). Record actual output — do not assume.

- [ ] **Step 3: Get a fresh falsifier-reachability census**

```bash
python scripts/check_falsifier_reachability.py --stats
```

Expected: a current coverage percentage and count, superseding this plan's stale 2026-08-05 figure (25%, 21/83). Record it in the ADR's §0 reads — this is a live, decaying number and the plan must cite today's, not last week's.

- [ ] **Step 4: Confirm D4's current owed status**

```bash
grep -n "D4\|per-direction feed" docs/adr/2026-08-09-rejection-register-topology-and-bar-wiring.md
grep -rn "2026-08-09-rejection-register-topology" docs/adr/ | grep -v "2026-08-09-rejection-register-topology-and-bar-wiring.md"
```

Expected: confirms no superseding/addendum ADR has already dispatched D4's enforcement instrument since 2026-08-09. If one has, Phase 1 Task 2 below is already done — skip it and record why.

- [ ] **Step 5: Confirm the three rejection registers' current row counts**

```bash
grep -c "^###" docs/rejected_candidates.md
grep -c "" docs/methodology/rejected_signals.md
grep -c "^|" ops/instruments/MNQ.md
```

Record actual counts in the ADR — needed to size Phase 1 Task 2's enforcement instrument correctly (it has to walk every terminal-negative closure since 2026-08-09, whatever that count now is).

- [ ] **Step 6: Author the ADR**

Create `docs/adr/2026-08-27-ssot-data-lineage-remediation-program.md` using the `brief-authoring` skill's `adr.md` template (§0 Rule-0 reads = Steps 1–5 above, verbatim commands + actual output; §2 Decision = ratify this phased program and name Phase 1's four tasks as the immediately-authorized scope, Phases 2–4 as named-but-not-yet-scoped follow-on work; §4 falsifiable hypothesis = "if this program is load-bearing, then by the next quarterly programme audit the four Phase 1 items are closed and re-verified clean, and no new instance of the same four defect classes has been found since"; §5 forbidden moves = do not reopen CATALOG/rejection-register-topology rulings, do not bulk-delete, do not touch Pine/risk constants; §7 implementation plan = point at this file; §10 audit hooks = the four verification blocks from Phase 1 tasks below).

- [ ] **Step 7: Get operator ratification**

Present the ADR for `Accepted` status per this repo's standing ratification convention (operator GO, in-session or explicit). Do not proceed to Phase 1 execution before this.

---

## Phase 1 — Close the four already-identified, high-leverage gaps

*Authorized by the Phase 0 ADR. Each task below is independently shippable and independently testable — land them as separate commits/PRs, in any order, though Task 1 is cheapest and should go first.*

### Task 1: Redeploy (or author) the skill-side `check_brief.py`

**Files:**
- Modify or create: `.claude/skills/brief-authoring/scripts/check_brief.py` (in-repo source — exact action depends on Phase 0 Step 1's finding)
- Modify: `scripts/gates.yml` (add a new gate, see Step 4 below)
- Create: `scripts/check_skill_deploy_sync.py`
- Test: `tests/scripts/test_check_skill_deploy_sync.py`

**Interfaces:**
- Consumes: `scripts/sync_skills.py`'s existing `--check` mode (already implements repo-vs-deployed diffing; do not reimplement diffing logic).
- Produces: `check_skill_deploy_sync.py` — a thin gate wrapper with signature `main(argv: list[str]) -> int`, exit 0 if `sync_skills.py --check` is clean for every skill under `.claude/skills/` that has a `Verification` block anywhere in `docs/adr/**/*.md` citing `~/.claude/skills/<name>/scripts/*.py`, exit 1 otherwise, printing which skill(s) drifted.

- [ ] **Step 1: If Phase 0 Step 1 found the file missing in-repo too, write it before anything else**

If `.claude/skills/brief-authoring/scripts/check_brief.py` does not exist in-repo, this is a bigger gap than "stale sync" — the 2026-08-09 canon ruling ("skill-side check_brief.py is canonical") was never actually implemented. In that case, before doing Step 2 below, copy `scripts/check_brief.py` (the repo-side implementation, which does exist) into `.claude/skills/brief-authoring/scripts/check_brief.py` as the starting point, then diff it against the canon-ruling ADR's decision text (`docs/adr/2026-08-09-check-brief-canon-ruling.md` §Decision: skill-side must NOT decline `lock`/`notice`/`lesson`/`audit`/`light`-tier types the way repo-side does, and must accept every canonical falsifier framing, not just `H:`+`falsifi*`). Patch accordingly. This step has no fixed diff here because it depends on Phase 0's finding — do not guess at content Phase 0 hasn't confirmed.

- [ ] **Step 2: Deploy it**

```bash
python scripts/sync_skills.py
python scripts/sync_skills.py --check
```

Run: expect exit 0 on the second command, and `find ~/.claude/skills/brief-authoring -name check_brief.py` to now return a match.

- [ ] **Step 3: Write the failing test for the new gate**

```python
# tests/scripts/test_check_skill_deploy_sync.py
import subprocess
import sys


def test_clean_deploy_passes(tmp_path, monkeypatch):
    # After a successful sync_skills.py run, the gate must exit 0.
    subprocess.run([sys.executable, "scripts/sync_skills.py"], check=True)
    result = subprocess.run(
        [sys.executable, "scripts/check_skill_deploy_sync.py"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_missing_deployed_file_fails(monkeypatch, tmp_path):
    # Simulate the exact defect this gate exists to catch: a skill script
    # cited in an ADR Verification block that is absent from the deployed target.
    fake_home_skills = tmp_path / "home_skills"
    (fake_home_skills / "brief-authoring").mkdir(parents=True)
    # deliberately do NOT create scripts/check_brief.py under it
    monkeypatch.setenv("HOME_SKILLS_DEPLOY_TARGET_OVERRIDE", str(fake_home_skills))
    result = subprocess.run(
        [sys.executable, "scripts/check_skill_deploy_sync.py"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "brief-authoring" in result.stdout
```

- [ ] **Step 4: Run the test to verify it fails (no gate script exists yet)**

Run: `pytest tests/scripts/test_check_skill_deploy_sync.py -v`
Expected: FAIL — `scripts/check_skill_deploy_sync.py` not found / ModuleNotFoundError equivalent for a subprocess call.

- [ ] **Step 5: Write the gate script**

```python
#!/usr/bin/env python3
"""check_skill_deploy_sync.py -- do skills cited in an ADR Verification block
actually exist at their deployed path?

Root cause this gate closes: docs/adr/2026-08-09-check-brief-canon-ruling.md
names ~/.claude/skills/brief-authoring/scripts/check_brief.py as canonical,
and every ADR's own Verification block runs it -- but the deployed bundle can
silently fall behind the in-repo source (sync_skills.py's own docstring: the
one-way contract "cannot be fully enforced from this script -- the sync layer
can still clobber"). This gate makes that drift visible instead of letting the
Verification block fail silently or not get run at all.

Scope: greps docs/adr/**/*.md for `~/.claude/skills/<name>/scripts/<file>.py`
citations, resolves each against $HOME (or
HOME_SKILLS_DEPLOY_TARGET_OVERRIDE for tests), and checks existence.
Does not check content/hash equivalence -- that is sync_skills.py --check's
job; this gate only asks "does the cited path exist at all", the same floor
check_falsifier_reachability.py applies to falsifier commands.
"""
import os
import re
import sys
from pathlib import Path

CITATION_RE = re.compile(r"~/\.claude/skills/([\w-]+)/scripts/([\w.]+\.py)")


def find_cited_skill_scripts(adr_dir: Path) -> set[tuple[str, str]]:
    cited = set()
    for path in adr_dir.glob("*.md"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for skill, script in CITATION_RE.findall(text):
            cited.add((skill, script))
    return cited


def main(argv: list[str]) -> int:
    repo_root = Path(__file__).resolve().parent.parent
    adr_dir = repo_root / "docs" / "adr"
    home_skills = Path(
        os.environ.get("HOME_SKILLS_DEPLOY_TARGET_OVERRIDE")
        or (Path.home() / ".claude" / "skills")
    )

    cited = find_cited_skill_scripts(adr_dir)
    if not cited:
        print("No ~/.claude/skills/*/scripts/*.py citations found in docs/adr/ -- nothing to check.")
        return 0

    missing = []
    for skill, script in sorted(cited):
        target = home_skills / skill / "scripts" / script
        if not target.exists():
            missing.append((skill, script, target))

    if missing:
        print(f"DRIFT: {len(missing)} ADR-cited skill script(s) missing from deployed bundle:")
        for skill, script, target in missing:
            print(f"  {skill}/scripts/{script} -- expected at {target}")
        print("Run: python scripts/sync_skills.py")
        return 1

    print(f"OK: {len(cited)} ADR-cited skill script(s) present in deployed bundle.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

- [ ] **Step 6: Run the test to verify it passes**

Run: `pytest tests/scripts/test_check_skill_deploy_sync.py -v`
Expected: PASS (both cases)

- [ ] **Step 7: Wire it into the gate roster**

Add to `scripts/gates.yml` (match the existing entry shape seen in `gate_manifest.py --list`'s output, e.g. the `skill-refs` entry):

```yaml
  skill-deploy-sync:
    tier: always
    command: python scripts/check_skill_deploy_sync.py
```

(Confirm the exact YAML key names against `scripts/gates.yml`'s current schema before landing — Rule 0: read the file, don't guess its shape from the `--list` text rendering.)

- [ ] **Step 8: Run the full gate list to confirm no regression**

```bash
python scripts/gate_manifest.py --list
python scripts/check_skill_deploy_sync.py
```

Expected: new gate appears in the roster; second command exits 0.

- [ ] **Step 9: Commit**

```bash
git add .claude/skills/brief-authoring/scripts/check_brief.py scripts/check_skill_deploy_sync.py scripts/gates.yml tests/scripts/test_check_skill_deploy_sync.py
git commit -m "fix(skills): redeploy skill-side check_brief.py, add deploy-sync gate

Closes the check_brief canon ruling's silent implementation gap: the
2026-08-09 ADR names ~/.claude/skills/brief-authoring/scripts/check_brief.py
canonical, but the deployed bundle had no scripts/ dir at all, so every
ADR's Verification block citing it has been failing silently (or not
being run). New gate makes this class of drift visible going forward."
```

### Task 2: Build the D4 enforcement instrument (rejection-register ledger coverage)

**Files:**
- Create: `scripts/check_instrument_rejection_coverage.py`
- Test: `tests/scripts/test_check_instrument_rejection_coverage.py`
- Modify: `scripts/gates.yml`

**Interfaces:**
- Consumes: `docs/adr/2026-08-09-rejection-register-topology-and-bar-wiring.md` D3's ownership table (per-direction/instrument-scoped kills belong in `ops/instruments/<SYM>.md` DEAD tables); `docs/briefs/closures/*.md` (the corpus of terminal-negative closures to check); whatever exact DEAD-table column schema Phase 0 Step 5 confirmed.
- Produces: exit 0 if every terminal-negative closure (`*-closure-falsified.md`, `*-closure-*-dead*.md`, or equivalent — confirm exact naming convention against the actual closures directory before coding the matcher) naming a specific instrument has a corresponding DEAD row in that instrument's `ops/instruments/<SYM>.md`; exit 1 with a list of gaps otherwise. This is the exact instrument the 2026-08-09 ADR's own §4 falsifier needs at the 2026-11-08 quarterly gate.

- [ ] **Step 1: Read the current DEAD-table schema and closure-naming convention (do not assume)**

```bash
sed -n '90,110p' ops/instruments/MNQ.md
ls docs/briefs/closures/ | grep -iE "falsif|dead|nsurv"
```

Record the actual column headers and the actual closure-filename suffix vocabulary — this plan's earlier phases only saw sampled evidence, not the full current schema. Do not write Step 4's matcher against a guessed schema.

- [ ] **Step 2: Write the failing test**

```python
# tests/scripts/test_check_instrument_rejection_coverage.py
import subprocess
import sys
from pathlib import Path


def test_flags_a_closure_with_no_dead_row(tmp_path, monkeypatch):
    closures = tmp_path / "docs" / "briefs" / "closures"
    closures.mkdir(parents=True)
    (closures / "Q-FAKE-1-closure-falsified.md").write_text(
        "# Q-FAKE-1\n\n**Instrument:** MNQ\n\n**Closure basis:** FALSIFIED.\n"
    )
    instruments = tmp_path / "ops" / "instruments"
    instruments.mkdir(parents=True)
    (instruments / "MNQ.md").write_text("# MNQ\n\n## DEAD / REJECTED\n\n| date | mechanism |\n|---|---|\n")

    monkeypatch.setenv("REPO_ROOT_OVERRIDE", str(tmp_path))
    result = subprocess.run(
        [sys.executable, "scripts/check_instrument_rejection_coverage.py"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "Q-FAKE-1" in result.stdout
    assert "MNQ" in result.stdout
```

- [ ] **Step 3: Run test to verify it fails**

Run: `pytest tests/scripts/test_check_instrument_rejection_coverage.py -v`
Expected: FAIL — script does not exist yet.

- [ ] **Step 4: Write the implementation**

Base the closure-metadata parse and instrument-name extraction on whatever Step 1 actually found (the `**Instrument:**` field format above is illustrative from this plan's sampled evidence — confirm the real field name/format against 3–4 real closure files before coding the regex). Follow the same "explicit gap list, not silent pass" shape as `check_falsifier_reachability.py` — this gate should self-report its own coverage the same honest way that script does (e.g. "N of M in-window closures checked; K instruments have no `ops/instruments/<SYM>.md` file at all and were skipped, not silently passed").

- [ ] **Step 5: Run test to verify it passes**

Run: `pytest tests/scripts/test_check_instrument_rejection_coverage.py -v`
Expected: PASS

- [ ] **Step 6: Run against the full real corpus and record the actual coverage number**

```bash
python scripts/check_instrument_rejection_coverage.py
```

This is the number the 2026-08-09 ADR's §4 falsifier needs at 2026-11-08 ("ledger-coverage rate for in-window instrument-scoped terminal-negative closures is below 100% with no dated exception" = FALSIFIED). Record it in this program's tracking, whatever it is — do not round up or assume 100%.

- [ ] **Step 7: Wire into gates.yml at WARN tier initially**

```yaml
  instrument-rejection-coverage:
    tier: warn
    command: python scripts/check_instrument_rejection_coverage.py
```

Start WARN, not hard-fail — per the same M-22 lesson `check_falsifier_reachability.py`'s own docstring cites ("a hard gate here would block commits on ADRs nobody is touching"). Promote to hard-fail only after Step 6's real-corpus run is clean or has dated, named exceptions.

- [ ] **Step 8: Commit**

```bash
git add scripts/check_instrument_rejection_coverage.py tests/scripts/test_check_instrument_rejection_coverage.py scripts/gates.yml
git commit -m "feat(gates): build the D4 enforcement instrument for rejection-register coverage

Discharges docs/adr/2026-08-09-rejection-register-topology-and-bar-wiring.md
D4, deferred as a separate packet at ratification. Answers the ADR's own
2026-11-08 falsifier question: does every terminal-negative closure naming
an instrument have a ledger DEAD row. WARN-tier pending a clean baseline."
```

### Task 3: Wire Q-M1WIRE-1's tree-skew checker into `gates.yml`

**Files:**
- Read: `scripts/validate_c1_monitoring_acceptance.py` (confirm the skew-checker function's actual name/signature — the earlier mining pass cited it but did not record the exact call site)
- Modify: `scripts/gates.yml`
- Test: `tests/scripts/test_gates_yml_wiring.py` (or extend an existing gate-roster test if one exists — check first)

**Interfaces:**
- Consumes: `validate_c1_monitoring_acceptance.py`'s existing skew-check function (do not rewrite it — this task is purely a wiring/binding fix, per the report's own "reachability vs. bindingness" distinction: the checker already works correctly in isolation).

- [ ] **Step 1: Confirm the checker's current invocation form**

```bash
grep -n "def.*skew\|skew_check\|def main" scripts/validate_c1_monitoring_acceptance.py
```

Record the actual CLI form (flag-based? subcommand? importable function only?) before writing the gates.yml entry — do not guess.

- [ ] **Step 2: Add the gates.yml entry, tier and path-conditional trigger matching the existing convention**

Model on the `instrument-profiles` entry's shape (`tier: always`) already in `gates.yml`, since like that gate this one guards a hard safety-relevant path (the M1 arming interlock) — confirm this tier choice is appropriate given Q-M1WIRE-1's own closure disposition before committing to `always` vs `path-conditional`.

- [ ] **Step 3: Run `gate_manifest.py --list` and confirm the new entry appears**

```bash
python scripts/gate_manifest.py --list | grep -i skew
```

- [ ] **Step 4: Run the gate directly against the current worktree and record whether it passes**

If the closure that named this gap (`Q-M1WIRE-1-closure-falsified.md`) is accurate that live drift exists on pinned files, this gate may legitimately fail on first run — that is expected and correct (it means the gate now sees what it's supposed to). Do not suppress a real failure to make Task 3 look done; file it as a separate, explicitly-named follow-up if so.

- [ ] **Step 5: Commit**

```bash
git add scripts/gates.yml
git commit -m "fix(gates): wire the M1 tree-skew checker into gates.yml

Discharges Q-M1WIRE-1 / C-P4-08 (named, not opened, at the 2026-08-21
coherence campaign). The checker itself was already correct in isolation;
it was simply never called by the gate roster it was built for."
```

### Task 4: Put `check_falsifier_reachability.py` on a standing cadence

**Files:**
- Modify: `docs/operational_rules.md` (the section documenting the quarterly programme-audit checklist)
- Modify: `scripts/gates.yml` (WARN tier, informational)

**Interfaces:**
- Consumes: `check_falsifier_reachability.py --stats` (already exists; do not modify the script itself — it is well-designed and self-documenting).

- [ ] **Step 1: Confirm the quarterly programme-audit checklist's current location and format**

```bash
grep -n "quarterly\|programme.audit" docs/operational_rules.md | head -20
```

- [ ] **Step 2: Add a line to that checklist**

Add: "Run `python scripts/check_falsifier_reachability.py --stats` and record the coverage trend (not just the point figure — the script's own docstring shows coverage eroding as the corpus grows faster than anchored falsifiers)." Do not add it as a hard gate — the script's own docstring explains why (M-22 lesson, blocks commits on ADRs nobody is touching).

- [ ] **Step 3: Add it to `gates.yml` at WARN/informational tier so `make validate` surfaces the trend without blocking anything**

```yaml
  falsifier-reachability-census:
    tier: warn
    command: python scripts/check_falsifier_reachability.py --stats
```

- [ ] **Step 4: Commit**

```bash
git add docs/operational_rules.md scripts/gates.yml
git commit -m "docs(governance): put falsifier-reachability census on the quarterly cadence

check_falsifier_reachability.py already self-reports eroding coverage
(28pct to 25pct over one week per its own docstring) but was run on no
schedule at all. This is the closest thing the repo has to a standing
decay-audit for the ADR corpus; give it one."
```

---

## Phase 2 — Consolidate the repeated hand-rolled canonical/mirror micro-pattern

**Status:** scoped 2026-08-29. Recon (a)(b)(c) answered. Bite-sized steps live in
[`2026-08-29-ssot-phase-2-running-count-mirror.md`](2026-08-29-ssot-phase-2-running-count-mirror.md).
Do not re-derive them here.

**Why (unchanged):** three ADRs each independently invented "this ADR's own running-count
line is canonical, STATE.md is a mirror only," enforced by nothing but a sentence. One
already lagged its mirrors by 8 days.

**Recon answers (2026-08-29, `87afe00`):** (a) `check_adr_graph.py` does **not** check
running-count freshness (A1–A7 only). (b) no fourth instance. (c) a shared HTML-comment
schema is **not** cheaper than three prose conventions; a STATE-mirror join is the wrong
check (STATE deletes closed rows by design). Authorized design is A8 — intra-ADR
table-vs-line / deep-lane-abandoned-vs-cited-preregs consistency.

## Phase 3 — Instrument-profile / cost-model closed-world completeness audit

**Status:** scoped 2026-08-29. Recon (a)(b)(c) answered. Bite-sized steps live in
[`2026-08-29-ssot-phase-3-cost-model-closed-world.md`](2026-08-29-ssot-phase-3-cost-model-closed-world.md).
Do not re-derive them here.

**Why (unchanged):** the 2026-07-25 profile ADR and Q-CAPBAND-1 both named
closed-world gaps. Recon (this phase's plan) confirmed the bars *class* is still
ungated (instance already fixed; no prose parser) and the cost-model named-set
drift is the live SSOT hole.

**Recon answers (2026-08-29, `d276076`):** (a) bars class still open, still
review-discipline; commission raise still live and SPECS outgrew the named
no-row set. (b) no fourth hole that is this packet — ledger⋈SPECS is the wrong
join. (c) cheapest check is the intra-`cost_model` partition, not a harvest
rewrite and not a bars parser.

## Phase 4 — Extend the coherence-campaign cadence to explicitly include a lineage/SSOT pass (scoped, not yet detailed)

**Why:** the 2026-08-21 coherence campaign's own recurrence trigger is "next quarterly programme audit, or any session that edits PIPELINES/INDEX/S7" — general pipeline coherence, not lineage/SSOT specifically. This program's Phase 0–1 work should feed back into that cadence rather than create a second, competing audit ritual.

**What must happen first:** Phases 0–1 need to actually land and get their own falsifier-review cycle before it's honest to claim this pattern is "handled going forward" — writing Phase 4's detail now would be prescribing a victory lap before the win.

---

## Self-Review

**Spec coverage:** every SSOT/lineage gap this session verified as currently open (skill-deploy drift, D4 enforcement, Q-M1WIRE-1 wiring, falsifier-reachability cadence) has a Phase 1 task. The two gaps that were "confirm before detailing" at authoring (running-count pattern; instrument-profile/cost-model completeness) now have scoped 2026-08-29 plan files (Phases 2 and 3). Phase 4 remains the unpaid confirm-before-detailing follow-on.

**Placeholder scan:** Phases 2 and 3 now have their own plan files (2026-08-29). Phase 4 still deliberately does not contain complete code — it names exactly what to read first. That remains a Rule-0 gate, not a vague hand-wave.

**Type consistency:** `check_skill_deploy_sync.py`'s `main(argv)` and `check_instrument_rejection_coverage.py`'s CLI shape both follow the exit-code convention already used by every other `scripts/check_*.py` gate in this repo (0 = clean, non-zero = findings), confirmed against `gate_manifest.py --list`'s existing roster.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-27 | Initial plan, scoped from the "Recurrence Ledger" mining pass + a fresh Rule-0 re-verification of every cited defect's current state | Claude Code |
| 2026-08-29 | Phase 2 scoped — recon (a)(b)(c) answered; pointer at `2026-08-29-ssot-phase-2-running-count-mirror.md` (A8 intra-ADR consistency; no HTML-comment schema; no STATE join) | Cursor Cloud Agent |
| 2026-08-29 | Phase 3 scoped — recon (a)(b)(c) answered; pointer at `2026-08-29-ssot-phase-3-cost-model-closed-world.md` (cost-model partition; bars checker voided; no ledger join) | Cursor Cloud Agent |
