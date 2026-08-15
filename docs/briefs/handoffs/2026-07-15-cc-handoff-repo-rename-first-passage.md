# CC Handoff — Execute the First Passage identity rename (ADR 2026-07-15)

**Date:** 2026-07-15
**Parent session:** claude.ai advisor (Joshua + Claude)
**Spawn target:** Claude Code (Tactical Ops). Halt-and-ask §0.5 form (not the Cursor variant).
**Repo:** `multi_firm_operations` (renaming to First Passage — that is this task). Path `C:/Users/joshu/multi_firm_operations` (folder NOT renamed in this handoff).
**Brief type:** CC handoff (multi-step)
**Parent question:** ADR-2026-07-15 (repo identity rename) — executing a locked decision, no hypothesis under test.
**Authority:** Joshua (CEO). claude.ai authored this brief; CC executes on a branch. No commit to `main`, no PR merge, no GitHub settings change without Joshua's go.

---

## §0 — Rule 0 reads (PHASE 0 — execute BEFORE any §2 edit)

CC: read each file below, report the current lines that mention the old identity, **and report each file's git-tracking status** (`git log -1 -- <path>` empty ⇒ UNTRACKED). Do not edit anything, do not create the branch, until this read-report is delivered and Joshua has resolved §0.5.

Per SKILL.md: when the parent (advisor) environment cannot commit to the repo, §0 lives in the handoff and CC executes the read as Phase 0.

- `pyproject.toml` — report L6 `name = …` + the `[tool.setuptools]` block (`packages`, `py-modules`) + `[tool.pytest.ini_options] pythonpath`. Confirm there is no `import`-able package (expected: `packages = []`, `py-modules = []`).
- `.claude/skills/code-defect-debugging/SKILL.md` — report every line matching `multi.firm.operations` (expected ~4: description, §Overview, "component boundaries", audit-hook). Also report the sibling-skill line that names `prop-firm-challenge` (context only; NOT edited here).
- `.agents/skills/code-defect-debugging/SKILL.md` — report tracking status (expected UNTRACKED) + matching lines. This is the mirror.
- `.claude/skills/brief-authoring/references/cc_handoff.md` — report L6 `**Repo:**` line.
- `README.md`, `CLAUDE.md`, `AGENTS.md`, `STATE.md` — report each identity/brand line matching `multi.firm.operations` or "Multi-firm operations". Report tracking status of `AGENTS.md` (expected UNTRACKED).
- `ops/cli.py` — report L2 + L152. `Makefile` — report L1.
- `.claude/settings.local.json` — report L6–L7 (abs-path allowlist) + tracking status (expected UNTRACKED). **Read-only confirmation** — this file is NOT edited in this handoff (folder not renamed).
- `git worktree list`, `git remote -v`, `git rev-parse --short HEAD`, `git branch --show-current` — report verbatim (baseline for §10).
- **Grep-gate baseline (BLOCKING):** run and report the count, so we can prove history is untouched afterward:
  ```bash
  git grep -cE 'multi.firm.operations' -- 'docs/adr/**' 'docs/ltm/**' 'docs/briefs/**' | awk -F: '{s+=$2} END{print "HISTORY-BASELINE:", s}'
  ```

After Phase 0: post the read-report + the HISTORY-BASELINE number. Wait for Joshua's go / §0.5 resolution before §2.

---

## §0.5 — Clarifying questions (HALT-ON-AMBIGUITY required)

CC: this is your license to halt. Do not default to a guess on any of these.

- **Slug form.** ADR §2 recommends GitHub slug `first-passage` (kebab) and dist name `first-passage` (kebab, matching the existing dist-name convention). The *current* GitHub slug uses an underscore (`multi_firm_operations`). Confirm: new slug **`first-passage`** (kebab) or **`first_passage`** (underscore, for continuity)? The dist name should stay kebab (`first-passage`) regardless. → ASK; do not pick.
- **Branch.** Default: create `rename/first-passage` off current HEAD (`7c86db2`, branch `claude/update-repo-docs-9ea48d`). Confirm branch off current HEAD vs off `main`. → default to off current HEAD unless told otherwise; state which you used.
- **Mirror handling.** `.agents/skills/…` and `AGENTS.md` are expected UNTRACKED (confirm in Phase 0). If UNTRACKED: edit them in place but do NOT `git add`; regenerate via the normal sync if one exists. If Phase 0 finds them TRACKED, that contradicts the ADR §0 finding — bounce `NEEDS_CONTEXT` with the tracking output quoted.
- **Brand string in code.** For `ops/cli.py` L152 and the `Makefile`/`README` brand lines, use display form **"First Passage"** (not `first-passage`/`first_passage`). Confirm the human-readable brand is "First Passage".

Post ambiguities under `## §0.5 Response`. Set `Status: NEEDS_CONTEXT` until resolved.

---

## §1 — Context

Executing ADR 2026-07-15 — rename the operation identity `multi_firm_operations` / `multi-firm-operations` → First Passage across three name-forms (GitHub slug, Python dist name, brand), touching **only** the live identity surface: ~6 tracked files + 3 untracked mirrors. The 999-match scan is almost entirely worktree duplication + immutable history + a non-existent import namespace (ADR §1); the load-bearing surface is small.

**Decision being executed:** ADR-2026-07-15 — see it for the full rationale, the DO/DON'T surface table (§2), and the forbidden moves.

**What CC is being asked to produce:**
- A branch (`rename/first-passage`) with the ~6 tracked file edits + 3 untracked mirror edits per §2.
- A regenerated `first_passage.egg-info` (via `pip install -e .`) and passing smoke tests.
- A closure report (§6) including the grep-gate output proving the live surface is clean **and** the HISTORY-BASELINE count is unchanged.

**What CC is NOT being asked to do:**
- NOT rename the local folder `C:/Users/joshu/multi_firm_operations` (deferred — worktree hazard).
- NOT touch any history/evidence file (ADRs, `docs/ltm/**`, `docs/briefs/**` except creating nothing new here, SESSIONS logs, archived notes, `lab/archive/**`, `lab/analysis/<dated>/**`, run-outputs) or any `.claude/worktrees/*` duplicate.
- NOT change the GitHub slug or `git remote` (operator/settings step, Phase 3).
- NOT edit `.claude/settings.local.json` (only stale if the folder is renamed, which it is not).
- NOT touch `core/`, any Pine, any locked constant, the MC anchor, or any allocation.
- NOT reconcile the `fxify-challenge → prop-firm-challenge` skill drift (separate rename — surface as a concern, do not fix).
- NOT commit to `main` or merge.

---

## §2 — Execution plan

Multi-step. §7 requires a final consolidated read across all diffs (Discipline Check #10).

### Step 2.1 — Branch
- **Action:** `git switch -c rename/first-passage` (off current HEAD unless §0.5 says otherwise). Record the pre-edit commit hash.
- **Per-step gate:** clean working tree before edits (or note any pre-existing dirty state and stop if it overlaps the target files).

### Step 2.2 — Packaging (`pyproject.toml`)
- **Action:** `name = "multi-firm-operations"` → `name = "first-passage"`. If `description` embeds "Multi-firm", update the brand phrase; leave the technical description otherwise intact. Do NOT touch `pythonpath`, `packages`, `py-modules`, deps, or the `analysis`/`dev` pins.
- **Expected output:** one-line `name` change (+ optional description brand tweak).
- **Per-step gate:** `git diff pyproject.toml` shows only the name/brand lines.

### Step 2.3 — Live skill anchors
- **Action:** In `.claude/skills/code-defect-debugging/SKILL.md`, replace the identity references (`multi_firm_operations` as the stack name) with `first_passage` (or the prose "the First Passage stack") — the description trigger, §Overview, "component boundaries", and audit-hook lines. Mirror the identical edit into `.agents/skills/code-defect-debugging/SKILL.md` (do NOT `git add` if UNTRACKED). **Leave** the `prop-firm-challenge` sibling line exactly as-is (out of scope).
- **Per-step gate:** the 4 identity refs updated in both copies; the `prop-firm-challenge` line unchanged; `git diff` for `.agents/…` shows the file is untracked (appears under "Untracked" / not staged).

### Step 2.4 — Forward-propagating template
- **Action:** `.claude/skills/brief-authoring/references/cc_handoff.md` L6 → `**Repo:** \`first-passage\` (or specific repo path)`.
- **Per-step gate:** single-line diff.

### Step 2.5 — Branding (cosmetic)
- **Action:** Update the identity/brand strings to "First Passage" in `README.md`, `CLAUDE.md`, `STATE.md`, `ops/cli.py` (L2 docstring, L152 argparse `description`), `Makefile` (L1 comment). Regenerate/patch the UNTRACKED `AGENTS.md` mirror from `CLAUDE.md` via the normal sync (do NOT `git add`).
- **Per-step gate:** each diff touches only identity/brand lines; no functional code changed in `ops/cli.py` beyond the description string.

### Step 2.6 — Editable-install regen + smoke test
- **Action:**
  ```bash
  rm -rf multi_firm_operations.egg-info   # stale
  pip install -e .                          # regenerates first_passage.egg-info
  pip show first-passage
  python ops/cli.py --help
  python -c "import sys; sys.path[:0]=['core','ops','lab']; import portfolio_mc, accounts" 2>&1 | tail -5   # pythonpath modules still resolve
  ```
- **Expected output:** `pip show first-passage` returns metadata; `--help` exits 0; layer-root modules import.
- **Per-step gate:** all three succeed. Any failure → `BLOCKED — plan-itself-wrong` (a name-form mismatch) or `NEEDS_CONTEXT`.

### Step 2.7 — Closure artifact
- **Action:** run the §10 grep-gate; record post-edit live-surface (expect EMPTY) and HISTORY-count (expect == baseline from Phase 0). Write the closure report (§6 format) to this handoff's return.
- **Sentinel:** no `main` commit, no PR, no GitHub/remote change — those are Phase 3 (operator).

---

## §4 — Falsifiable hypothesis
`N/A — executing ADR-2026-07-15, no hypothesis under test.` The ADR's §4 live-reference falsifier governs post-execution (checked in §10).

---

## §5 — Forbidden moves

- **Editing any history/evidence file or `.claude/worktrees/*` duplicate.** If a match tempts you there, it stays. History is a record (ADR §5).
- **The "while I was in there" fix — especially the `fxify-challenge → prop-firm-challenge` rename.** Log it under `DONE_WITH_CONCERNS`; do not touch it.
- **`git add`-ing untracked mirrors** (`.agents/**`, `AGENTS.md`, `.claude/settings.local.json`). Edit in place where §2 says; never stage them.
- **Renaming the local folder** or running `git worktree` mutations. Out of scope; worktree hazard.
- **Touching `core/`, Pine, any locked constant (`dd_protection`/`firm_rules`/`portfolio_mc`), the MC anchor, or allocations.** Integrity failure if you do.
- **Any GitHub settings change, `git remote set-url`, `main` commit, or PR merge.** Phase 3, operator-only.
- **Amending §2 or the ADR mid-run.** If a target line isn't where §0 said, return `NEEDS_CONTEXT` with the discrepancy; don't improvise.

---

## §6 — Gate + status return taxonomy

Report back with EXACTLY one status.

| Status | Meaning | Parent action |
|---|---|---|
| `DONE` | All 2.1–2.7 done; live-surface grep EMPTY; HISTORY-count == baseline; smoke tests green; no scope creep. | Review, PR (operator), ratify. |
| `DONE_WITH_CONCERNS` | Completed but flagged something (e.g., the `prop-firm-challenge` drift, an unexpected extra match, an untracked-vs-tracked surprise). | Parent reviews concerns before accepting. |
| `NEEDS_CONTEXT` | §0.5 unresolved, a §0 target line not where expected, or a name-form ambiguity. | Parent supplies; re-dispatch. |
| `BLOCKED` | Structural obstruction — sub-case required. | Escalate/decompose. |

`BLOCKED` sub-cases: `context-problem` / `capability-problem` / `scope-problem` / `plan-itself-wrong`.

**Closure report format:**
```
Status: <…>
Slug form used (dist): first-passage   | GitHub slug confirmed for Phase 3: <first-passage|first_passage>
Branch: rename/first-passage @ <pre-hash> → <post-hash>
Per-step gates: 2.1 […] 2.2 […] 2.3 […] 2.4 […] 2.5 […] 2.6 […] 2.7 […]
Diffs (files touched): <list; mark each TRACKED/UNTRACKED>
Live-surface grep (expect EMPTY): <output>
HISTORY count: baseline=<n> post=<n>  (MUST match)
Smoke tests: pip show=<ok> cli --help=<ok> module import=<ok>
Concerns surfaced: <e.g. fxify→prop drift; …>
Next action recommended: <one sentence — typically "operator: GitHub slug rename + remote set-url + PR">
```

---

## §7 — Parent-session review (after CC returns)

**Pass 1 — Spec-compliance.**
- [ ] Diff list contains ONLY the ~6 tracked files + the 3 untracked mirrors named in §2 — no history file, no `core/`, no worktree path.
- [ ] No `fxify-challenge → prop-firm-challenge` edit slipped in.
- [ ] Untracked mirrors edited but NOT staged (`git ls-files` shows them absent).
- [ ] No GitHub/remote/`main` change.

**Pass 2 — Quality.**
- [ ] `pip show first-passage` + `ops/cli.py --help` + module import all green.
- [ ] Live-surface grep EMPTY; `first_passage.egg-info` present; stale egg-info gone.
- [ ] HISTORY count == baseline (history provably untouched).

**Pass 3 — Consolidated read (multi-step).** Read all diffs together: is the identity coherent across pyproject + skills + template + branding (no half-renamed surface, no brand string reading `first-passage` where it should read "First Passage")?

Only after all three passes does claude.ai recommend the operator proceed to Phase 3 (GitHub slug rename, `git remote set-url`, PR, ratify, flip ADR to `Accepted`).

---

## §10 — Audit hooks (runnable)

```bash
cd "C:/Users/joshu/multi_firm_operations"

# Live identity surface clean (expect EMPTY)
git grep -nE 'multi.firm.operations' -- pyproject.toml ops/cli.py Makefile README.md CLAUDE.md STATE.md \
  .claude/skills/code-defect-debugging/SKILL.md .claude/skills/brief-authoring/references/cc_handoff.md

# New identity in place
grep -n 'name = "first-passage"' pyproject.toml
pip show first-passage >/dev/null && echo "dist OK"
python ops/cli.py --help >/dev/null && echo "cli OK"
ls -d first_passage.egg-info 2>/dev/null && ! ls -d multi_firm_operations.egg-info 2>/dev/null && echo "egg-info swapped"

# History NOT rewritten (expect post == baseline)
git grep -cE 'multi.firm.operations' -- 'docs/adr/**' 'docs/ltm/**' 'docs/briefs/**' | awk -F: '{s+=$2} END{print "HISTORY-POST:", s}'

# core/Pine/constants untouched (expect EMPTY)
git diff --name-only rename/first-passage -- core/ '*.pine' core/config/params.toml core/dd_protection.py

# Untracked mirrors not staged (expect EMPTY)
git ls-files .claude/settings.local.json .agents AGENTS.md

# Worktrees intact (folder not renamed → no errors)
git worktree list
```

---

## Verification (parent-side)

```bash
# Mechanical discipline check on THIS handoff
python scripts/check_brief.py docs/briefs/handoffs/2026-07-15-cc-handoff-repo-rename-first-passage.md --type cc_handoff
# Expected: all 6 general + 7–10 PASS

# Confirm CC's return used the four-state taxonomy
grep -E "^Status: (DONE|DONE_WITH_CONCERNS|NEEDS_CONTEXT|BLOCKED)" <cc-return-path>

# Confirm HISTORY baseline == post in the closure report
grep -E "HISTORY count: baseline=([0-9]+) post=\1" <cc-return-path>
```

If CC returns `NEEDS_CONTEXT`/`BLOCKED`, re-dispatch per §6. Do not proceed to Phase 3 until `DONE` (or `DONE_WITH_CONCERNS` with concerns resolved).
