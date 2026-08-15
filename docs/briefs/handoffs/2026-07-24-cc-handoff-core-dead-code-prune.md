# CC Handoff — core dead-code prune (modes.py sweep modes, core/lib relocation, tv_export_loader reduction)

**Date:** 2026-07-24
**Parent session:** Claude Code operator session — Algorithm repo review (umbrella: `docs/notes/2026-07-24-algorithm-repo-review-handoff-series.md`).
**Spawn target:** **Claude Code** — NOT Cursor-eligible: routing test 1 of `docs/adr/2026-07-14-cc-cursor-surface-allocation.md` sends any `core/mc/*` / `portfolio_mc` edit to CC, full stop.
**Repo:** `multi_firm_operations`
**Brief type:** CC handoff (multi-step)
**Parent question:** N/A — executes an operator-authorized Delete/Simplify slate on the locked-layer's dead strata.
**Authority:** Joshua (CEO). **DO NOT EXECUTE UNTIL THE OPERATOR RECORDS GO ON THIS BRIEF** (deletions are user-gated at D). No commit/merge without Joshua's go. **The MC engine's regression surface must survive byte-green: `tests/core/test_mc_synthetic_engine.py` + `tests/core/test_mc_module_facade.py` are the acceptance boundary. Zero behavior change to any retained mode.**

**OPERATOR GO LINE (fill before execution):** `GO recorded: ________ (date, initials)`

---

## §0 — Rule 0 reads (PHASE 0 — read-report before any edit)

Anchors verified at `33356ea` (2026-07-24). Re-read each in the executing session; `NEEDS_CONTEXT` on contradiction.

- `core/mc/modes.py` (1,527 lines) — read in full. Report: the closed-investigation strata to delete — `mode_alloc_sweep` (line ~651, Q-SWAP-3) + `SWEEP_CONFIGS` + its gate constants; `mode_boundary_sweep` (~850, Q-REGIME-1 FALSIFIED) + `_run_half_panel` + `BOUNDARY_SWEEP_DATES` + `GA4_ALLOCATIONS`; `mode_pine_shrink_sweep` (~1169, Q-SWAP-4) + `_load_guardian_with_shrink` + `_load_all_with_pine_shrink` + `_run_pine_shrink_cell` + `PINE_SHRINK_*`; `GUARDIAN_V56_CSV` (line 94, zero consumers); and their `--alloc-sweep`/`--boundary-sweep`/`--pine-shrink-sweep`/`--ga4` argparse plumbing + mutual-exclusion blocks. Report the KEEP set: `PRE_SHOCK_1R`, `mode_default`, `mode_historical`, `mode_sensitivity`, the `panels_override` machinery, the empty-registry `SystemExit` guard (~1400–1408), and everything `tests/core/test_mc_module_facade.py` + `tests/core/test_mc_synthetic_engine.py` import.
- **Consumer sweeps (re-run; the parent found zero external consumers of the delete set):**
  ```bash
  rg --no-ignore -n "mode_alloc_sweep|mode_boundary_sweep|mode_pine_shrink_sweep|_run_half_panel|GUARDIAN_V56_CSV|PINE_SHRINK|GA4_ALLOCATIONS|SWEEP_CONFIGS|BOUNDARY_SWEEP_DATES" --type py
  ```
  Every hit must be inside `core/mc/modes.py` itself. ANY external hit → `NEEDS_CONTEXT`.
- **`PRE_SHOCK_1R` live consumers (must survive):** `lab/analysis/regime/decompound_remc_2026-06-07/findings.py:23` (`from portfolio_mc import PRE_SHOCK_1R`) + archived `lab/archive/bulenox_futures_remc_2026-07-01/c5_integer_remc.py:39`. Report the `core/portfolio_mc.py` facade's export mechanism (star-export means deleted names vanish from the facade — the KEEP set must remain exported).
- `docs/adr/2026-07-22-challenge-era-substrate-retirement.md` §2-E + Phase 4 scope (~lines 200–203) — confirm Phase 4 touches modes.py only for "import-time derivation of challenge target globals"; the sweep-mode strata are in NO phase's enumerated scope (this prune is separable dead code, not a Phase-4 jump; the Phase-4 hard stop is untouched). Report the §2-E preserve list to confirm nothing here intersects it.
- `core/lib/correlation.py` + `core/lib/nonlinear.py` — report contents + the consumer sweep (`rg --no-ignore -n "pearson_daily|load_exit_date_daily_net|align_two_daily_series|hurst_rs" --type py`): expected consumers are only their own tests (`tests/test_correlation.py`, `tests/test_regime_bootstrap.py` docstring-level, `tests/core/test_nonlinear.py`) + one archived study. Contrast keepers: `core/lib/file_lock.py` (c1 telemetry) and `core/lib/regime_bootstrap.py` (standing regime gate) are NOT in scope.
- `core/tv_export_loader.py` — report the two zero-active-consumer public loaders (`load_tv_export`, `pair_tv_export_dataframe`) vs the live piece: `PRICE_COL_BY_INSTRUMENT`, imported by `core/bar_export_loader.py:34` (R2-live BAR EXPORT producer).
- `docs/mc_anchor_history.md` — confirm Q-SWAP-3/Q-SWAP-4/Q-REGIME-1 results are recorded there (the R4 record that replaces re-run capability — which is already dead regardless: the panel registry is empty post-Phase-3 and the sweep modes' REG byte-identity gates reference the four deleted anchor CSVs).
- `REPO_MAP.md` + `docs/ltm` references — `rg -n "mc_user\|alloc-sweep\|boundary-sweep\|pine-shrink" REPO_MAP.md PIPELINES.md docs/ --glob '!docs/ltm/**'` — report doc rows needing same-commit pointer updates.

---

## §0.5 — Clarifying questions (parent-recommended defaults; this is a CC spawn — halt-and-ask remains available)

- **(A) core/lib relocation vs deletion.** **Recommended default:** RELOCATE `correlation.py` + `nonlinear.py` to `lab/research_utils/` (with their tests moved to matching test paths) rather than delete — `nonlinear.py` encodes the recorded R/S-Hurst-on-log-prices trap-guard lesson, and `correlation.py` encodes Q-CORR gate semantics that future breadth work may reuse. Boundary-legal (lab imports nothing from them; they import core-nothing). `check_boundaries.py` must stay green.
- **(B) tv_export_loader shape.** **Recommended default:** delete `load_tv_export` + `pair_tv_export_dataframe` + their dedicated tests; KEEP the module in place with `PRICE_COL_BY_INSTRUMENT` (zero import churn for `bar_export_loader`). Do not relocate the map into `bar_export_loader` (that edits an R2-live producer for cosmetic gain).
- **(C) Deletion mechanics for ~700 lines.** **Recommended default:** delete whole functions/constants + their argparse wiring; do NOT restructure retained code (no reordering, no docstring rewrites beyond removing dead `--mode` mentions). The diff should be pure-removal plus minimal seam lines.

---

## §1 — Context

Post-substrate-Phase-3, ~700 of `core/mc/modes.py`'s 1,527 lines are single-investigation CLI modes for investigations closed in May–June 2026 (Q-SWAP domain RETIRED on SNAG exhaustion 2026-06-05; Q-REGIME-1 FALSIFIED) — doubly dead because every mode requires a registered panel and `PANELS_BY_BROKER` is permanently empty. Their R4 record lives in `docs/mc_anchor_history.md`. Two lab-only helpers sit in the locked core sink with zero non-test consumers, and `tv_export_loader`'s public API has no active callers beyond its constant map. The adversarial cross-check confirmed: no ADR phase owns this prune (separable from the gated Phases 4–6), and no consumer refutes it.

**Deliverable:** one `claude/*` branch PR: modes.py prune, core/lib relocation, tv_export_loader reduction, same-commit doc-row updates, full test suite green.
**NOT asked:** anything in substrate Phases 4–6 scope (FXIFY defaults, challenge globals), `dd_geometry`/`dd_protection`/`firm_rules`/`lifecycle` (untouchable here), `csv_parser`/tearsheet (ADR §2-D owns), any Pine or manifest.

---

## §2 — Execution plan

### Step 2.1 — modes.py prune

- **Action:** delete the §0-enumerated strata per §0.5(C).
- **Per-step gate:** `pytest tests/core/ -q` fully green — `test_mc_module_facade.py` (pins `load_trades`/`build_daily_panel`/`build_week_blocks`/`_simulate_path`/`run_seed`/`report_default`/`_run_seeds`) and `test_mc_synthetic_engine.py` (imports `ALLOCATIONS`, `SEEDS`, `_run_seeds`, preflight + simulation names) must pass unmodified — the test files themselves are NOT edited. `python -c "from portfolio_mc import PRE_SHOCK_1R"` (with core on path) succeeds.

### Step 2.2 — core/lib relocation

- **Action:** `git mv core/lib/correlation.py lab/research_utils/correlation.py`; `git mv core/lib/nonlinear.py lab/research_utils/nonlinear.py`; move their tests; update the moved tests' imports; update the one archived-study reference note ONLY if it is a live import (expected: archive is non-runnable — leave archived bytes untouched, note it).
- **Per-step gate:** `python scripts/check_boundaries.py` green; moved tests green; `rg -n "core.lib.correlation|core/lib/nonlinear|from lib.correlation|from lib.nonlinear" --type py` → zero live hits outside `lab/archive/`.

### Step 2.3 — tv_export_loader reduction

- **Action:** per §0.5(B).
- **Per-step gate:** `pytest tests/ -q` green; `core/bar_export_loader.py` untouched; its import of `PRICE_COL_BY_INSTRUMENT` still resolves.

### Step 2.4 — Doc-row updates + closure

- **Action:** update the §0-enumerated REPO_MAP/PIPELINES rows (retirement-pointer style); append the one-line records to the umbrella note's execution log; SESSIONS entry.
- **Per-step gate:** `make check` green (or the documented worktree sub-gates if executed from a worktree); closure report per §6.

---

## §4 — Falsifiable hypothesis

**H (premise, not an investigation):** the delete strata have zero external consumers and sit outside every substrate-ADR phase scope. **Falsified if** any Phase-0 sweep finds an external consumer or a phase-scope intersection — bounce `NEEDS_CONTEXT`; the regression tests (unmodified) are the standing falsifier for any behavior change.

---

## §5 — Forbidden moves

- **Touching anything in substrate Phase 4–6 enumerated scope** (FXIFY defaults, challenge-target globals, fixtures) — the hard stop before Phase 4 is an operator decision this brief must not erode from below.
- **Editing the two MC regression test files** to make the prune pass — the tests are the acceptance boundary; if they fail, the prune is wrong (`BLOCKED — plan-itself-wrong`).
- **Deleting `PRE_SHOCK_1R` or narrowing the facade exports** — live consumer in the decompound study; archived harness re-runnability preserved deliberately.
- **"While I was in there" cleanup of retained modes** (refactor temptation is real at this file size) — pure removal only, per §0.5(C).
- **Extending scope to `csv_parser`/tearsheet/`dd_geometry`** — each has a standing deliberate-retention decision.

---

## §6 — Gate + status return

Report EXACTLY one of `DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT` / `BLOCKED — <sub-case>` per `references/cc_handoff.md` §6, with the standard closure-report format (status, per-step gates, diff list, concerns, next action). This handoff produces no investigation verdict (no RESOLVED / FALSIFIED / AMBIGUOUS claim) — the four-state return plus the per-step gates is the entire closure.

---

## §7 — Parent-session review (after return)

Pass 1: diff = modes.py (pure removal), the two moved lib files + tests, tv_export_loader, enumerated doc rows — nothing else. Pass 2: full `pytest` green with UNMODIFIED regression tests; `check_boundaries` green; facade import probe green. Pass 3: read modes.py's retained body end-to-end once — argparse help must not reference any deleted mode; no orphaned constant remains.

---

## §10 — Audit hooks (runnable)

```bash
rg -n "mode_alloc_sweep|mode_boundary_sweep|mode_pine_shrink_sweep|GUARDIAN_V56_CSV" --type py   # expect: zero
python -c "import sys; sys.path.insert(0,'core'); from portfolio_mc import PRE_SHOCK_1R; print('facade OK')"
git ls-files lab/research_utils/correlation.py lab/research_utils/nonlinear.py                    # expect: both present
pytest tests/core/test_mc_synthetic_engine.py tests/core/test_mc_module_facade.py -q
git log -1 --format='%h' -- tests/core/test_mc_synthetic_engine.py tests/core/test_mc_module_facade.py
# Expected: predates this PR (tests unmodified).
```

---

## Verification (parent-side)

```bash
python scripts/check_brief.py docs/briefs/handoffs/2026-07-24-cc-handoff-core-dead-code-prune.md
grep -n "GO recorded" docs/briefs/handoffs/2026-07-24-cc-handoff-core-dead-code-prune.md  # must be filled before execution
```
