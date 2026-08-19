# End-to-End Validation Implementation Plan (Phase 3 of 3)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prove the persona-panel mechanism actually works end-to-end — real independent output, real
well-formed logs, and a checker that genuinely catches malformed entries rather than passing
vacuously — using an already-closed decision as a zero-risk rehearsal target.

**Architecture:** A real (paid, non-simulated) Workflow invocation against the already-ratified
GSUB-1 inventory, followed by executing Phase 2's documented log-append procedure for real, followed
by extending the Phase-1 checker to validate log structure and proving that extension isn't vacuous
via a deliberately planted defect.

**Tech Stack:** Same as Phase 1/2 — Python 3 stdlib, Workflow-tool JS, no new dependencies.

## Global Constraints

- **Depends on Phase 1** (roster exists) **and Phase 2** (persona-mode panel + log-append procedure
  exist) being merged first.
- Task 1 spends **real tokens** (a 4-persona panel run: review + verify + synthesis stages) — this is
  flagged for explicit operator acknowledgment before running, not something to fire automatically.
- This rehearsal reviews an **already-closed, already-ratified decision** (GSUB-1). It cannot change
  a ratified outcome and therefore does **not** count as a real data point toward the design spec
  §10 falsifier ("does panel input ever change a ratified outcome") — every log entry this plan
  produces is explicitly tagged `**Rehearsal:** yes` so this is never later mistaken for a real review.
- Per the repo's own standing lesson (`lesson_discipline_guards_need_adversarial_tests` — "vacuous
  asserts pass empty"), the new log-validation check must be proven to actually fail on a real defect,
  not just proven to pass on well-formed input.

## File Structure

```
docs/personas/cio-log.md    <- new (Task 1, first real entry)
docs/personas/coo-log.md    <- new (Task 1, first real entry)
docs/personas/cfo-log.md    <- new (Task 1, first real entry)
docs/personas/cro-log.md    <- new (Task 1, first real entry)
scripts/check_personas.py   <- modify (Task 2, add check_logs())
docs/superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md   <- modify (Task 3, append §13)
```

---

### Task 1: Retroactive dry run + first real persona logs

**Files:**
- Create: `docs/personas/cio-log.md`, `docs/personas/coo-log.md`, `docs/personas/cfo-log.md`,
  `docs/personas/cro-log.md`

**Interfaces:**
- Consumes: the persona-mode workflow from Phase 2 (`.claude/workflows/pre-ratification-adversarial-panel.js`)
  and the log-append procedure documented in that plan's Task 3 Step 4.
- Produces: 4 real log files, each with exactly one entry — the input Task 2 validates against.

- [ ] **Step 1: Confirm operator go-ahead, then run the panel**

**Cost flag:** this step spends real tokens across a 4-persona review+verify+synthesis pipeline.
Confirm before running.

Call:
```
Workflow({
  scriptPath: '.claude/workflows/pre-ratification-adversarial-panel.js',
  args: {
    targetPath: 'docs/briefs/GSUB-1-inventory-and-dispositions.md',
    tier: 'GRAND',
    personas: ['cio', 'coo', 'cfo'],
  },
})
```
Expected: `result.personaMode === true`, `result.personaSlugs` has 4 entries (`cio`, `coo`, `cfo`, and
`cro` auto-added per the mandatory-GRAND-CRO rule), `result.lensResults.length === 4`, and
`result.synthesis` is a non-empty string covering all 4 personas.

- [ ] **Step 2: Verify the mandatory-CRO auto-add fired**

Check: `result.personaSlugs.includes('cro')` is `true` even though `'cro'` was not in the `personas`
array passed in Step 1. This is the concrete proof that design spec §4's "CRO on every GRAND decision,
no exceptions" rule is mechanically enforced, not just documented.

- [ ] **Step 3: Execute the log-append procedure for real, for each of the 4 personas**

Following Phase 2's documented procedure, for each slug in `['cio', 'coo', 'cfo', 'cro']`: no prior
log exists yet (first-ever run for every one of these personas), so create
`docs/personas/<slug>-log.md` with exactly one entry using this template (extending Phase 2's base
template with the rehearsal tag this plan's Global Constraints require):

```markdown
# <Role Name> — Decision Log

Append-only. One entry per review. See
[design spec §6.4](../superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md) for the format
contract and [`INDEX.md`](INDEX.md) for this persona's definition.

## 2026-08-18 — docs/briefs/GSUB-1-inventory-and-dispositions.md

**Verdict:** <fill in from result.synthesis for this persona's lens key>
**Confirmed findings:** <count from result.lensResults for this persona, or "none">
**Ratified as recommended:** Pending -- rehearsal only, not submitted for real ratification
**Rehearsal:** yes -- retroactive dry run against an already-closed decision, not a real
ratification-influencing review; does not count toward the design spec §10 falsifier
**CRO hard block fired:** <yes, with the note from result.croHardBlock -- or "no">
```

Replace `<Role Name>` with the exact H1 heading from that persona's definition file (e.g. `CIO`,
`COO`, `CFO`, `CRO`) and fill every `<...>` placeholder from the actual `result` object returned in
Step 1 — do not leave any bracketed placeholder in the committed file.

- [ ] **Step 4: Commit**

```bash
git add docs/personas/cio-log.md docs/personas/coo-log.md docs/personas/cfo-log.md docs/personas/cro-log.md
git commit -m "chore(personas): first real panel rehearsal against GSUB-1 -- 4 logs created"
```

---

### Task 2: Extend `check_personas.py` with log validation + adversarial planted-defect test

**Files:**
- Modify: `scripts/check_personas.py` (append `check_logs()`, call it from `main()`)

**Interfaces:**
- Consumes: the 4 real log files from Task 1 as the well-formed-input test case.
- Produces: `check_logs(errors)` — appends to the same `errors` list the roster check already uses,
  so one script, one exit code, one report.

- [ ] **Step 1: Add the log-entry format constants and `check_logs()` function**

Insert immediately after the `EXPECTED_COUNT = 19` line from Phase 1's version of the script:

```python
LOG_ENTRY_HEADER = re.compile(r"^##\s+(\d{4}-\d{2}-\d{2})\s+—\s+(.+)$", re.MULTILINE)
LOG_REQUIRED_SUBFIELDS = ["Verdict", "Confirmed findings", "Ratified as recommended"]


def check_logs(errors):
    log_files = sorted(PERSONAS_DIR.glob("*-log.md"))
    for path in log_files:
        text = path.read_text(encoding="utf-8")
        headers = list(LOG_ENTRY_HEADER.finditer(text))
        if not headers:
            errors.append(f"{path.name}: exists but has no entries matching '## YYYY-MM-DD — <path>'")
            continue
        for i, m in enumerate(headers):
            start = m.end()
            end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
            block = text[start:end]
            missing = [f for f in LOG_REQUIRED_SUBFIELDS if f"**{f}:**" not in block]
            if missing:
                errors.append(
                    f"{path.name}: entry dated {m.group(1)} missing required field(s): {', '.join(missing)}"
                )
```

- [ ] **Step 2: Wire it into `main()`**

Find the line `if errors:` near the end of `main()` (the final report block) and insert
`check_logs(errors)` on the line immediately before it:

```python
    check_logs(errors)

    if errors:
        print(f"FAIL: {len(errors)} issue(s) found:")
```

- [ ] **Step 3: Run against the real Task-1 logs — verify PASS**

Run: `python scripts/check_personas.py`
Expected: `check_personas: OK -- 19 persona files, all required fields present, INDEX.md in sync`
(the 4 real logs from Task 1 are well-formed, so `check_logs` appends nothing to `errors`)

- [ ] **Step 4: Adversarial test — prove the check actually fails on a real defect**

This is the check on the checker itself. Create a throwaway scratch file with a deliberately missing
field, confirm the checker catches it, then remove the scratch file so it never pollutes the real
roster:

```bash
cat > docs/personas/_adversarial-scratch-log.md << 'EOF'
# Scratch — Decision Log

## 2026-08-18 — scratch-target.md

**Verdict:** CLEAR
**Confirmed findings:** none
EOF
python scripts/check_personas.py
```
Expected: `FAIL` with a line reading
`_adversarial-scratch-log.md: entry dated 2026-08-18 missing required field(s): Ratified as recommended`

Then clean up and confirm the real roster is unaffected:
```bash
rm docs/personas/_adversarial-scratch-log.md
python scripts/check_personas.py
```
Expected: `check_personas: OK -- 19 persona files, all required fields present, INDEX.md in sync`
(back to green — the adversarial file is gone, the real logs from Task 1 are untouched)

- [ ] **Step 5: Commit**

```bash
git add scripts/check_personas.py
git commit -m "feat(personas): extend checker with log validation, adversarially tested"
```

---

### Task 3: Rehearsal record in the design spec

**Files:**
- Modify: `docs/superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md` (append new §13 — do
  not edit any existing section, per this repo's addenda-not-silent-edits convention already
  followed in Phase 2's §12 addition)

**Interfaces:**
- Consumes: nothing new.
- Produces: a durable, dated record distinguishing this rehearsal from a real falsifier data point —
  the next person reading `docs/personas/*-log.md` needs this context without re-deriving it.

- [ ] **Step 1: Append §13 to the design spec**

```markdown
## 13. Rehearsal record (added during Phase 3 implementation)

**2026-08-18 — retroactive dry run, NOT a real falsifier data point.** Ran the persona-mode panel
(GRAND tier, personas `cio`/`coo`/`cfo` + auto-added `cro`) against the already-closed GSUB-1
inventory (`docs/briefs/GSUB-1-inventory-and-dispositions.md`) purely to prove the mechanism produces
sensible independent output and writes well-formed logs. Because GSUB-1 was already ratified and
closed before this mechanism existed, this run **cannot** change a ratified outcome and therefore
does not count toward the §10 falsifier ("does panel input ever change a ratified outcome"). The
first real data point toward that falsifier can only come from a genuine future GRAND or strict-D2
STRATEGIC-tier decision reviewed *before* ratification. Every log entry this rehearsal wrote carries
an explicit `**Rehearsal:** yes` line for exactly this reason -- so a future reader of
`docs/personas/*-log.md` never mistakes rehearsal output for a real review.
```

- [ ] **Step 2: Commit**

```bash
git add docs/superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md
git commit -m "docs(personas): record Phase 3 rehearsal, explicitly not a §10 falsifier data point"
```

---

## Out of scope for this plan

- Any real (non-rehearsal) GRAND or STRATEGIC-tier decision review — the mechanism is now proven to
  work mechanically; using it for real is a standing operational choice from here on, not a plan task.
- Wiring an automatic trigger (e.g., a hook that fires the panel automatically at ratification time)
  — every invocation so far, rehearsal included, is explicitly operator-initiated. Automating the
  trigger itself is a future decision, not assumed by this plan.
