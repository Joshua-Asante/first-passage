# Cursor Handoff — `lab/research_utils/axis_screen.py`: promote the Q-KBUDGET floor scan to a reusable, manifest-driven intake screen

**Date:** 2026-07-15
**Status:** **IMPLEMENTED — PR #393** (`cursor/axis-screen-module-5808`, 2026-07-16). Cleared by harvest-intake ADR `Accepted` 2026-07-15; Cursor returned **DONE** (21/21 tests; fixture reproduces 6 FAIL / 1 PASS / RESOLVED).
**Parent session:** Claude Code operator session (Joshua + Claude) — harvest-intake codification.
**Spawn target:** Cursor (frozen-spec implementation — [`docs/adr/2026-07-14-cc-cursor-surface-allocation.md`](../../adr/2026-07-14-cc-cursor-surface-allocation.md)). Pure arithmetic, stdlib + `lab/research_utils/deflated_sharpe.py` only — runs in the **ops venv** (no `.venv-research` dependency; the Q-KBUDGET harness already proves this import path works there).
**Repo:** `multi_firm_operations`
**Brief type:** Cursor handoff (multi-step)
**Parent question:** harvest-intake ADR §6 downstream — "promote `floor_scan.py`'s arithmetic to a manifest-consuming reusable module," so a new harvested seed screens by **adding a data row, never by writing new screen code**.
**Authority:** Joshua (CEO). Claude Code authored this brief; Cursor executes. No commit/merge without Joshua's go. **Locked surfaces Cursor must NOT touch (this task):** the frozen screen pre-reg (`docs/briefs/pre-registration/Q-KBUDGET-1-screen-preregistration.md`), the Q-KBUDGET campaign directory (`lab/archive/q_kbudget_1_2026-07/`). **Note (2026-07-16):** this directory is no longer literally byte-identical to its 2026-07-15 state — PR #391 (a separate, legitimate task) synced `RESULTS.md`/`d5_clause_n_rescreen.md`'s status prose to match the already-ratified D5 decision (commit `5a8713f`); the underlying arithmetic and verdict (RESOLVED, 6 FAIL/1 PASS/0 UNSCREENABLE, D5 floor/power values) are unchanged and remain the regression-fixture target below. The instruction for *this* task is unchanged: this build must not be the one touching that directory. `lab/research_utils/deflated_sharpe.py` (consumed, not edited), any `core/*` file, `dd_protection` / allocations / MC-anchor constants / `ACTIVE_FIRM`, and Pine are likewise off-limits.

> **Build-ahead-of-seed (read first).** No seed beyond D5 has been admitted; D5 already completed its screen via the campaign-local harness. This module is intake infrastructure that must exist and be proven correct **before** the next harvested seed arrives. Build + test entirely against (a) the historical Q-KBUDGET rows as a regression fixture and (b) synthetic manifest rows. Do not wait for or reference a live new seed.

---

## §0 — Rule 0 reads (PHASE 0 — execute BEFORE any code)

Cursor: read each item and post a read-report in your first response **before** writing a line of code. If any repo fact contradicts a §2 assumption, return `NEEDS_CONTEXT` with the discrepancy quoted — do not resolve unilaterally.

- [`lab/archive/q_kbudget_1_2026-07/floor_scan.py`](../../../lab/archive/q_kbudget_1_2026-07/floor_scan.py) @ `936a9e0` — report in full: `floor_at_k()` (the scan loop: `expected_max_sharpe(k, 1/n)` → scan annualized SR upward in 0.005 steps until `deflated_sharpe(...) ≥ 0.95`, most-permissive across `FREQS=(0.5,1,2,4)`, `YEARS=6.5`); the module constants `CAP=1.0`, `DSR_MIN=0.95`; the hardcoded `AXES` list-of-dicts schema (`axis, family, k_banked, k_intrinsic=(lo,hi), clause_n`); `screen()`'s verdict branching (`FAIL (Clause K)` / `FAIL (Clause N, inherited)` / `FAIL (Clause N)` / `UNSCREENABLE` / `PASS`) — **note the range semantics: a row PASSES Clause K only if its BEST (lowest-K) end passes**; and `main()`'s outputs (results.json + markdown table + §D verdict line).
- [`lab/archive/q_kbudget_1_2026-07/d5_power.py`](../../../lab/archive/q_kbudget_1_2026-07/d5_power.py) and [`d7_power.py`](../../../lab/archive/q_kbudget_1_2026-07/d7_power.py) @ `4a2471e` — report the Clause-N power computation each uses (normal-CDF via `math.erf`; `power = Φ(√N·|δ|/σ − 1.96)`) and their exact published outputs (D5: power=0.947 at N=1000, δ/σ=0.113; D7: power≈0.303 at N≈100, δ/σ=0.144) — these become regression pins.
- [`docs/briefs/pre-registration/Q-KBUDGET-1-screen-preregistration.md`](../pre-registration/Q-KBUDGET-1-screen-preregistration.md) §B (freeze `b304f2c`) — report the frozen clause definitions verbatim: Clause K (K_eff = K_intrinsic + K_banked; floor ≤ Cap 1.0 ⇔ K_eff ≤ 3; DSR ≥ 0.95 at V=1/n) and Clause N (power ≥ 0.50; z ≈ 1.96 two-sided default; N = full declared OOS event count; δ cohort-cited central; no citable prior ⇒ UNSCREENABLE, never patched). **These constants are frozen inputs to this build — the module hardcodes them with citation comments and exposes NO CLI/env override** (harvest-intake ADR §5 forbidden move: tuning constants to admit a marginal seed).
- [`lab/research_utils/deflated_sharpe.py`](../../../lab/research_utils/deflated_sharpe.py) @ `48b8cef` — report the signatures of `expected_max_sharpe` and `deflated_sharpe` actually called by `floor_scan.py`, and confirm the import block is ops-venv-safe (no arch/skfolio import at module top).
- [`docs/methodology/strategy_harvest.md`](../../methodology/strategy_harvest.md) §5 — report the seed-manifest field list; the module's JSON row schema (§0.5-A) must be a strict subset mapping of it (field names may be snake_cased but must be 1:1 traceable).
- Repo test conventions: report how [`tests/test_universe_gate.py`](../../../tests/test_universe_gate.py) resolves imports (`PYTHONPATH` root, skip conditions) and confirm whether plain `pytest tests/test_<new>.py` runs research_utils imports in the ops venv.
- `git log -1 --format='%h %cs' -- lab/archive/q_kbudget_1_2026-07/floor_scan.py lab/research_utils/deflated_sharpe.py` — report as build anchors.

---

## §0.5 — Clarifying questions (HALT-ON-AMBIGUITY)

Parent-recommended defaults; **confirm or challenge each in the Phase-0 response** — bounce `NEEDS_CONTEXT` on conflict, never resolve silently.

- **(A) Input format — JSON rows, stdlib-only.** Manifest file = a JSON array of seed rows: `{"axis": str, "family": str, "k_banked": int, "k_intrinsic": [lo, hi], "n_events": int|null, "delta_over_sigma": float|null, "delta_citation": str|null, "unscreenable_reason": str|null}`. No YAML (avoids a dep); the human-readable manifest in `strategy_harvest.md` §5 remains the prose artifact — this JSON is its machine row. Confirm.
- **(B) Clause-N computed, not prose.** Unlike `floor_scan.py` (which carried Clause N as pre-written strings), the module **computes** power from `(n_events, delta_over_sigma)` when both are present; emits `UNSCREENABLE` (with `unscreenable_reason` mandatory) when either is null; and accepts an optional `clause_n_inherited: {"verdict": "FAIL", "citation": str}` field for inherited verdicts (the D3 shape) which short-circuits computation. Confirm.
- **(C) Verdict vocabulary identical to `floor_scan.py`:** `PASS` / `FAIL (Clause K)` / `FAIL (Clause N)` / `FAIL (Clause N, inherited)` / `UNSCREENABLE`, plus the aggregate §D line (RESOLVED / FALSIFIED / AMBIGUOUS-HOLD). Confirm.
- **(D) Regression fixture = the historical Q-KBUDGET table.** Ship `tests/fixtures/qkbudget_2026_07_axes.json` transcribing the seven D1–D7 rows (from `floor_scan.py`'s `AXES` + the computed D5/D7 Clause-N numbers) and pin the test to the published outcomes: floors 0.65/0.85/0.98/1.835/2.05 at their K values; 6 FAIL / 1 PASS / 0 UNSCREENABLE; verdict RESOLVED. The fixture is a **copy** — `lab/archive/q_kbudget_1_2026-07/` itself is not touched. Confirm.
- **(E) Placement + CLI.** Module at `lab/research_utils/axis_screen.py`; CLI `python -m research_utils.axis_screen <manifest.json> [--out results.json]` with `PYTHONPATH=lab` (mirrors the `register_search` invocation convention); prints the markdown table + verdict line to stdout. Confirm.
- **(F) Constants exposure for tests only.** Tests may need `floor_at_k` directly (pure function) — export it; but `CAP`, `DSR_MIN`, `POWER_MIN=0.50`, `Z=1.96`, `YEARS`, `FREQS` stay module-level constants with citation comments and no override path. A test asserting "constants match the frozen pre-reg values" is part of the deliverable. Confirm.

---

## §1 — Context

The harvest-intake ADR (on acceptance) makes the two-clause screen the standing admission gate for externally-published mechanisms. Today the screen's arithmetic lives in a campaign-local harness with a hardcoded axis list — correct as a frozen historical artifact, wrong as standing infrastructure (every new seed would mean editing analysis code, which is both rework and a drift surface). This build separates the frozen arithmetic (module) from the per-seed data (JSON manifest rows).

**What Cursor is asked to produce:**
- `lab/research_utils/axis_screen.py` — `floor_at_k()` (ported verbatim from `floor_scan.py`), `clause_n_power()` (the d5/d7 erf-CDF computation), `screen_rows(rows) -> list[dict]` (verdict branching per §0.5-B/C), manifest-JSON loader with schema validation (unknown keys rejected; `unscreenable_reason` mandatory when inputs null), CLI per §0.5-E.
- `tests/test_axis_screen.py` — (a) floor regression pins (K=1→0.65, 2→0.85, 3→0.98, 4→1.06, 450→1.835, 3178→2.05); (b) power regression pins (D5 0.947, D7 ≈0.303); (c) the full Q-KBUDGET fixture reproduces 6-FAIL/1-PASS/RESOLVED; (d) verdict branching unit cases incl. UNSCREENABLE-without-reason → hard error; (e) constants-match-frozen-pre-reg assertion; (f) schema rejection cases. All green in the **ops venv**.

---

## §2 — Execution plan

TDD; every step offline, ops-venv.

1. **Port `floor_at_k` + constants** with citation comments → floor regression pins green (test a).
2. **`clause_n_power`** (erf-CDF) → power pins green (test b).
3. **Row schema + loader** (strict validation) → rejection cases green (test f).
4. **`screen_rows` verdict branching** (range semantics: best-end K PASS; inherited short-circuit; UNSCREENABLE handling) → unit cases green (test d).
5. **Fixture + end-to-end**: Q-KBUDGET fixture file → full-table reproduction green (test c) + constants assertion (test e).
6. **CLI + `--out`** → manual smoke: fixture in, markdown table + RESOLVED line out, results.json written.

**Per-step gate:** `python scripts/check_boundaries.py` clean (module lives in `lab/`, imports nothing from `ops/`); full existing test suite untouched-green.

---

## §4 — Hypothesis (binary, adjudicated by the regression fixture)

**H-port:** the frozen screen arithmetic is separable from its per-seed data — i.e. a data-driven module reproduces the historical Q-KBUDGET table **exactly** (floors 0.65/0.85/0.98/1.835/2.05 at their K values; D5 power 0.947; D7 power ≈0.303; 6 FAIL / 1 PASS / RESOLVED) from a JSON fixture alone.

- **RESOLVED:** all regression pins green in the ops venv → the module is the standing intake harness.
- **FALSIFIED:** any pin cannot be reproduced without editing the frozen constants or the ported arithmetic → STOP, return the divergence; do not "fix" it by tuning — the divergence itself is the finding (either `floor_scan.py` had a latent defect or the port is unfaithful; parent adjudicates which).
- **AMBIGUOUS:** pins pass only under research-venv, not ops-venv → report the import chain that breaks; placement decision returns to parent.

---

## §5 — Forbidden moves

- **Editing anything under `lab/archive/q_kbudget_1_2026-07/`** — it is a closed historical artifact; the fixture is a *copy*. Tempting because the AXES list is *right there*; still forbidden.
- **Adding CLI/env overrides for `CAP` / `DSR_MIN` / `POWER_MIN` / `Z`** — the obvious "flexibility" refactor is exactly the harvest-intake ADR §5 forbidden move (tuning constants to admit a marginal seed). Constants change only by superseding the upstream frozen artifacts.
- **"Improving" the floor scan** (finer step, different frequency grid, analytic inversion) — any numeric change breaks byte-agreement with the published table; port verbatim, optimize never.
- **Wiring `register_search` or dedup logic into this module** — scope creep into separate decisions; screen only.
- **Adding a dependency** (yaml, numpy, scipy) — stdlib + `deflated_sharpe` only; `math.erf` covers the CDF.
- **Weakening a failing regression pin to green the suite** — that is Known-Trap-#12 at the code layer; bounce per §4 FALSIFIED instead.

---

## §6 — Return status (four-state taxonomy, mandatory in the closure report)

Report exactly one:

- **DONE** — all §2 steps complete, all tests green in ops venv, §4 RESOLVED, no locked-surface diffs (`git status` clean on `lab/archive/q_kbudget_1_2026-07/`, the frozen pre-reg, `core/`).
- **DONE_WITH_CONCERNS** — deliverables complete but something material surfaced (e.g. a floor value reproduces only to ±0.005 due to step-boundary sensitivity; an ops-venv import quirk worked around). Name each concern; parent adjudicates.
- **NEEDS_CONTEXT** — a §0 read contradicts a §2/§0.5 assumption, or a §0.5 default is wrong on inspection. Quote the conflict; make no unilateral call.
- **BLOCKED** — cannot proceed; classify the sub-case: **context-problem** (a needed fact isn't in the brief or the repo — name what's missing), **capability-problem** (environment/tooling can't do it — broken venv, permission, missing file), **scope-problem** (the task is bigger than the brief scoped — name the boundary hit), or **plan-itself-wrong** (a §2 step is incoherent against the code as read — quote the contradiction). Name the sub-case; stop.

Closure report contents (with the status): files added; test counts; the reproduced Q-KBUDGET table pasted verbatim; any §0.5 default challenged and its resolution; locked-surface `git status` confirmation.

---

## §7 — Parent-review (spec-compliance pass + quality pass; runs AFTER Cursor returns)

Parent (CC) reviews before any merge recommendation to Joshua — two distinct passes:

**Spec-compliance pass:**
1. Every §2 step's per-step gate evidenced in the closure report; §0.5 defaults either confirmed or explicitly re-resolved; four-state §6 status present and consistent with the evidence.
2. **Regression honesty:** re-run `PYTHONPATH=lab python -m research_utils.axis_screen tests/fixtures/qkbudget_2026_07_axes.json` parent-side and diff against `lab/archive/q_kbudget_1_2026-07/RESULTS.md` — do not trust the pasted table.
3. **Forbidden-move sweep:** `git diff --stat` shows no touch on the §5 locked surfaces; grep the module for argparse/env hooks on the frozen constants (expect none).

**Quality pass:**
4. **Consolidated read:** read the final module top-to-bottom once as a whole (not per-step diffs) — the multi-step trap is per-step-correct/whole-incoherent.
5. Naming/idiom matches `lab/research_utils/` siblings (`universe_gate.py`, `deflated_sharpe.py`); docstring carries the frozen-constant citations; tests are readable as the module's spec.

---

## §10 — Audit hooks (runnable post-merge)

```bash
PYTHONPATH=lab python -m research_utils.axis_screen tests/fixtures/qkbudget_2026_07_axes.json
# Expected: 6 FAIL / 1 PASS (D5) / RESOLVED — matches lab/archive/q_kbudget_1_2026-07/RESULTS.md

python -m pytest tests/test_axis_screen.py -q          # all green, ops venv
git diff --stat -- lab/archive/q_kbudget_1_2026-07/   # empty
grep -n "CAP = 1.0\|DSR_MIN = 0.95\|POWER_MIN = 0.50" lab/research_utils/axis_screen.py  # frozen constants present
```
