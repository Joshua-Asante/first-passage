# Cursor Handoff — gate-estate repairs (check_skill_refs class gap, stale CI comment, manifest-gate worktree parity)

**Date:** 2026-07-24
**Status:** **DISCHARGED 2026-08-02 — DO NOT RE-DISPATCH.** Landed on `cursor/gate-estate-repairs-3f96` (PR pending merge). All five §2 steps executed; fixture matrix green; `--all` exit 0; bare-worktree `check_data_manifests` WARN+exit 0.
**Parent session:** Claude Code operator session — Algorithm repo review (umbrella: `docs/notes/2026-07-24-algorithm-repo-review-handoff-series.md`).
**Spawn target:** Cursor
**Repo:** `multi_firm_operations`
**Brief type:** Cursor handoff (multi-step)
**Parent question:** N/A — gate hardening ahead of substrate Phases 4–6; no Pre-Q.
**Authority:** Joshua (CEO). No commit/merge without Joshua's go. **Gate scripts + CI comment + tests only; no `core/` touch; failure semantics change ONLY where §2 enumerates.**
**Dispatch order:** AFTER the agent-surface sync (brief #2) — the extended gate built here must go green against the repaired skill set; its detection power is proven by fixture tests, not by leaving `main` red.

---

## Routing-test self-check (per `docs/adr/2026-07-14-cc-cursor-surface-allocation.md`)

- **Test 0:** no vendor bytes, no secrets. NOTE: the Step 2.3 soft-degrade behavior can only be *end-to-end* observed in an environment WITHOUT vendor CSVs (a worktree/cloud checkout) and hard-fail behavior only WITH them — so both behaviors are proven by unit tests with tmp-dir fixtures, not by environment luck. Cloud or local eligible.
- **Test 1:** No locked surface. Files: `scripts/check_skill_refs.py`, `scripts/check_data_manifests.py`, `.github/workflows/tests.yml` (comment only), plus new tests under `tests/`. Governance-layer scripts are not in ADR test 1's enumerated locked set; precedent: gate scripts have been Cursor-built before (status-consistency gate class).
- **Test 2:** Yes — behavior changes enumerated with exact conditions below.
- **Test 3:** Clears (~5 files + tests).

---

## §0 — Rule 0 reads (PHASE 0 — read-report before code)

Anchors verified at `33356ea` (2026-07-24). Report each; `NEEDS_CONTEXT` on contradiction.

- `scripts/check_skill_refs.py` — report `REPO_NAV_DIRS` (anchored lines 70–74: `docs/`, `config/`, `data/`, `tests/`, `.claude/`, `archive/`, `analysis/`, `strategies/` — note `ops/`, `core/`, `lab/`, `scripts/` absent), `KNOWN_TOP_DIRS` (line 83), the gitignored-vendor-subtree exemption comment below it, `_is_repo_nav_link` (~line 139), and `check_skill()` (~line 192 — confirm it reads SKILL.md only, never `references/*.md`). Report how `--all` currently exits (expect: OK — i.e., the gate is blind to dead `ops/` references).
- `scripts/check_data_manifests.py` — report its manifest-dir list (the six dirs), its behavior when a manifest dir's data files are absent (expect: hard-fail — no absent-tree tolerance), and its `--regenerate`/`--dry-run` modes.
- `scripts/check_pine_manifest.py` — report the warn-only-when-Pine-absent pattern (the parity model for Step 2.3).
- Commit `39838ad` (`git show 39838ad --stat`) — report how the CATALOG `--check` gate was made worktree-tolerant (the second parity model).
- `.github/workflows/tests.yml` — report the COVERAGE BOUNDARY comment (anchored lines 36–46; names `lab/analysis/time_to_pass.py --regime-check` as a live quarterly manual duty, "next: 2026-08-08") and confirm `STATE.md` records that check RETIRED 2026-07-22 ("Harness retained on disk; do not schedule", owned by `docs/adr/2026-07-11-challenge-era-claims-rescope.md` §Addendum 2026-07-22). The decompound `regime_gate.py` clause in the same comment stays TRUE (live §4 limb-2 obligation).
- `scripts/githooks/pre-commit` + `Makefile` — report where both gate scripts are wired (pre-commit steps, `make validate` / `make check` targets) so latency and failure-path changes are understood.

---

## §0.5 — Clarifying questions (Cursor variant — parent-recommended defaults)

- **(A) New REPO_NAV_DIRS entries create new failure surface.** **Recommended default:** add `"ops/"`, `"core/"`, `"lab/"`, `"scripts/"` to `REPO_NAV_DIRS`, run `--all`, and triage: (i) genuinely dead path → fix the skill text in this PR ONLY if the fix is a pure path correction (file moved/renamed); (ii) dead path that is a deliberate **tombstone** reference → see (A-bis), which is now the known instance; (iii) anything needing posture judgment → report as §6 concern, do not fix.

- **(A-bis) The one CERTAIN hard-fail, verified 2026-07-24 — resolve it this way, do not "fix" the posture text.** `.claude/skills/prop-firm-challenge/SKILL.md:24` reads *"The continuous-lot multiplier spine (`ops/accounts.py` + account CLI) is DELETED (substrate Phase 2)"*. That is a **deliberate tombstone**: the sentence's whole point is that the path no longer exists, and the text landed on `main` days ago as the corrected posture block (this series' brief #2, now DISCHARGED). The moment `ops/` joins `REPO_NAV_DIRS` it becomes a MISSING hard-fail. It is **already backticked**, so the (ii) "wrap in backticks" remedy does not apply. **Recommended default:** teach the checker to recognise tombstones rather than edit the prose — accept an explicit inline marker (e.g. a trailing `(deleted)` / `(retired)` token adjacent to the backticked path, or a `# skill-refs: tombstone` allowlist entry keyed by `skill:path`), implement it with a fixture test proving (a) a tombstone-marked dead path PASSES and (b) an unmarked dead path still FAILS, then mark this one instance. **Forbidden here:** deleting or rewording the `ops/accounts.py` sentence to make the gate green — that would degrade a just-corrected posture statement to satisfy a linter, which is the tail wagging the dog. If the tombstone mechanism looks like more than ~30 lines, return `NEEDS_CONTEXT` with a recommendation rather than improvising a broader allowlist design.
- **(B) `references/*.md` scanning scope.** **Recommended default:** scan `references/*.md` with the same link-extraction rules as SKILL.md but report-only (warn) in the first release — hard-fail stays SKILL.md-only. Rationale: reference files carry many historical citations; flipping them straight to hard-fail risks a noisy gate. The warn output gives the operator the inventory to decide a later hard-fail flip.
- **(C) Soft-degrade trigger condition for check_data_manifests.** **Recommended default:** per-directory — for each of the six manifest dirs: if the dir's `SHA256SUMS` exists but ZERO of its listed data files exist on disk → WARN + treat that dir as skipped (public-clone/worktree posture, mirroring check_pine_manifest); if ≥1 listed file exists → current full hard-fail semantics for that dir (partial presence is exactly the M-9 drift case the gate exists for). `--regenerate` behavior unchanged (never soft-degrades).

---

## §1 — Context

Three verified gate defects from the Algorithm review: (1) `check_skill_refs.py` cannot see skill references into `ops/ core/ lab/ scripts/` — precisely the trees substrate Phases 4–6 will delete from — so it green-lights dead references today; (2) `tests.yml` carries a stale comment asserting a retired quarterly duty (a future session could reschedule the retired check off it); (3) `check_data_manifests.py` hard-fails every bare worktree, unlike all its sibling gates, making `make check` unusable exactly where doc-only work happens (standing quirk, memory `reference_worktree_commit_gate_quirk`).

**Deliverable:** one `cursor/*` PR: two gate scripts hardened with unit tests, one CI comment corrected.
**NOT asked:** resolving the skills-check-vs-tests.yml CI duplication (operator QUESTION in the umbrella note), touching any skill content beyond §0.5(A)(i)/(ii) mechanical repairs, changing pre-commit wiring.

---

## §2 — Execution plan

### Step 2.1 — `check_skill_refs.py` class-gap closure

- **Action:** add the four dirs to `REPO_NAV_DIRS`; add `references/*.md` scanning per §0.5(B) (warn-only); extend the docstring's convention notes; add `tests/test_check_skill_refs_navdirs.py` with fixtures proving (a) a SKILL.md citing a nonexistent `ops/x.py` now FAILS, (b) a nonexistent `core/x.py` FAILS, (c) the gitignored vendor-subtree exemption still passes, (d) a dead link in `references/*.md` WARNS without failing.
- **Per-step gate:** fixture tests green; `python scripts/check_skill_refs.py --all` exit 0 against the post-brief-#2 tree (report full output; triage per §0.5(A)).

### Step 2.2 — `tests.yml` comment correction

- **Action:** rewrite the COVERAGE BOUNDARY comment to name ONLY the decompound `regime_gate.py` quarterly duty (next 2026-08-08, owned by `docs/adr/2026-06-07-decompound-remc-hold.md` §4); state explicitly that the former `time_to_pass.py --regime-check` duty was RETIRED 2026-07-22 (D2 resolved — harness retained on disk, do not schedule).
- **Per-step gate:** comment-only diff (no workflow steps changed); `grep -n "time_to_pass" .github/workflows/tests.yml` hits only inside the retirement sentence.

### Step 2.3 — `check_data_manifests.py` absent-tree parity

- **Action:** implement §0.5(C) exactly; add `tests/test_check_data_manifests_worktree.py` with tmp-dir fixtures proving (a) all-absent dir → WARN + exit 0, (b) partial presence → hard-fail unchanged, (c) full presence + hash mismatch → hard-fail unchanged, (d) `--regenerate` unaffected.
- **Per-step gate:** fixture tests green; on THIS (bare) checkout `python scripts/check_data_manifests.py` now exits 0 with WARN lines naming each skipped dir.

### Step 2.4 — `skills-check.yml` duplication collapse (operator ruling #5, 2026-07-24 — pre-authorized)

- **Inputs:** `.github/workflows/skills-check.yml` + `.github/workflows/tests.yml` (Phase-0 read both; parent-verified at `33356ea`: identical `[push, pull_request]` triggers, identical 3.11/3.12 matrix, and tests.yml's `pytest tests/ -v` already runs all 7 files named in skills-check's "Skills tests" step — so those tests execute 4× per push).
- **Action:** in `skills-check.yml`: (a) DELETE the "Skills tests" step (the `pytest tests/test_check_skill_refs.py … test_retire_adr.py -v` step) — tests.yml owns test execution; (b) reduce `matrix.python-version` to `["3.12"]` — the 6 gate-script steps are version-insensitive file checks, and tests.yml retains the 2-version matrix for the suite; (c) KEEP all six gate-script steps unchanged — they are the CI backstop for the `--no-verify`-bypassable pre-commit chain and must run exactly once per push. Add a 2-line comment at the top of the jobs block recording this division ("gate scripts once in CI as the pre-commit backstop; test execution lives in tests.yml — operator ruling 2026-07-24").
- **Per-step gate:** workflow YAML parses (CI run on the PR is the proof); `grep -n "pytest" .github/workflows/skills-check.yml` → zero hits; all six gate-script steps still present.

### Step 2.5 — Closure

Report per §6; PR body includes the full `--all` triage table from 2.1, the WARN output from 2.3, and the skills-check diff summary from 2.4.

---

## §4 — Falsifiable hypothesis

**H (premise, not an investigation):** the three §0-anchored gate defects exist as described. **Falsified if** any Phase-0 read contradicts its anchor (e.g. REPO_NAV_DIRS already extended) — bounce `NEEDS_CONTEXT`; a partially-falsified premise shrinks scope to the surviving defects only.

---

## §5 — Forbidden moves

- **Weakening any hard-fail path while adding tolerance.** The M-9 lesson is the reason this gate exists; §0.5(C)'s partial-presence hard-fail is non-negotiable. If implementation pressure suggests relaxing it, `BLOCKED — plan-itself-wrong`.
- **Flipping `references/*.md` to hard-fail in this PR** (tempting for symmetry) — warn-only first release, per §0.5(B).
- **Editing workflow STEPS in tests.yml** while "in there" — comment only.
- **Fixing posture-judgment skill text surfaced by the new gate** — report, don't fix (§0.5(A)(iii)).
- **Re-scheduling or deleting `lab/analysis/time_to_pass.py`** — deliberately retained by operator decision ("retire, but do not over-retire").

---

## §6 — Gate + status return

Report EXACTLY one of `DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT` / `BLOCKED — <sub-case>` per `references/cc_handoff.md` §6, with the standard closure-report format (status, per-step gates, diff list, concerns, next action). This handoff produces no investigation verdict (no RESOLVED / FALSIFIED / AMBIGUOUS claim) — the four-state return plus the per-step gates is the entire closure.

---

## §7 — Parent-session review (after return)

Pass 1: diff = the two scripts, the workflow comment, the two new test files, plus only §0.5(A)(i)/(ii) skill repairs (each listed in the PR body). Pass 2: fixture matrix covers all enumerated behaviors; no hard-fail path weakened (read the diff hunks, not just tests). Pass 3: run `make check` on a bare worktree AND confirm CI green on the PR — both environments must pass with the new semantics.

---

## §10 — Audit hooks (runnable)

```bash
python - <<'EOF'
import re,sys
src=open('scripts/check_skill_refs.py').read()
assert all(d in src for d in ('"ops/"','"core/"','"lab/"','"scripts/"')), "REPO_NAV_DIRS gap reopened"
print("nav-dirs OK")
EOF
grep -n "time_to_pass" .github/workflows/tests.yml        # expect: retirement sentence only
python scripts/check_data_manifests.py; echo "exit=$?"    # on a bare worktree: WARN + exit=0
pytest tests/test_check_skill_refs_navdirs.py tests/test_check_data_manifests_worktree.py -q
```

---

## Verification (parent-side)

```bash
python scripts/check_brief.py docs/briefs/handoffs/2026-07-24-cursor-handoff-gate-estate-repairs.md
git log -1 --format='%h %ci' -- scripts/check_skill_refs.py scripts/check_data_manifests.py .github/workflows/tests.yml
```
