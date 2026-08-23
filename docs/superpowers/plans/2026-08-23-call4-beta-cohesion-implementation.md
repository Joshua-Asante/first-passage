# Call-4 beta-cohesion diagnostic (historical panels)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**AUTHORIZATION:** Accepted ADR [`2026-07-10-strategies-never-locked-lifecycle-governance.md`](../../adr/2026-07-10-strategies-never-locked-lifecycle-governance.md) — executable as a **diagnostic**. It does **not** authorize live-fill Call-1 σ-source wiring (fill-gated; see [`STATE.md`](../../../STATE.md) "gated on first strategy-signal fill").

**Goal:** Land a transfer-entropy / lead-lag **read** across the four locked-book legs + parents that the Call-4 soft flag can invoke. Report-only. No `lifecycle_state.json` write. No `BASE_RISK` / ladder / Pine edit.

**Architecture:** One pure module + CLI. Inputs = existing CME TV export panels (skip-if-missing). Output = a dated markdown/JSON report: pairwise lead-lag, a cohesion flag vs the ratified 2-of-4 soft-flag *context* (this diagnostic informs the interim review; `beta_death_assessment` already implements 2/4 and 3/4). Do not re-implement `beta_death_assessment`.

**Tech Stack:** Python 3.11+, numpy/pandas already in lockfile. Prefer a simple lagged-correlation / Granger-style lead-lag first; do not add a new heavy dependency for transfer-entropy unless `arch`/`statsmodels` already covers it.

## Global Constraints

- No live book. Diagnostic on historical panels only.
- Do not write `lifecycle_state.json`.
- Do not touch `TIER_MULTIPLIER`, `_validate_ladder`, `BASE_RISK`, `DD_SCALE`, Pine.
- Call-1 σ-source is **out of scope**.
- First-eval date 2026-08-08 is historical; this plan does not back-date a missed review.

## Rule 0 (verified 2026-08-23)

| Source | Anchor | What it pins |
|---|---|---|
| Lifecycle ADR header + §7 | `027a729` | Pending = beta-cohesion diagnostic only |
| `docs/methodology/strategy_lifecycle.md` Call 4 + Implementation status | `0723587` | Soft flag 2/4; beta-death 3/4 already coded; diagnostic "design in flight" |
| `core/lifecycle.py` `beta_death_assessment` | `027a729` | Do not duplicate |

## File Structure

| File | Responsibility |
|---|---|
| `lab/research_utils/beta_cohesion.py` | Pure pairwise lead-lag / cohesion stats |
| `scripts/beta_cohesion_read.py` | CLI: four-leg + parent panel paths → report |
| `tests/test_beta_cohesion.py` | Synthetic series: known lead recovered; missing CSV skips |
| `docs/methodology/strategy_lifecycle.md` Implementation status | Flip "design in flight" → landed path |

---

### Task 1: Failing tests

- [ ] **Step 1:** Synthetic two-series test: Y lagged copy of X → reported lag matches. Independent noise → no cohesion flag.
- [ ] **Step 2:** Tests red.

### Task 2: Module + CLI

- [ ] **Step 1:** Implement. Missing vendor CSV → skip with a clear message (public-clone posture).
- [ ] **Step 2:** Tests green.

### Task 3: Status honesty

- [ ] **Step 1:** Update `strategy_lifecycle.md` Implementation status item (b) to the new path. Do not claim Call-1 σ-source done.

### Task 4: Verification

```bash
PYTHONPATH=lab pytest tests/test_beta_cohesion.py -q
git diff --stat -- core/lifecycle.py core/dd_protection.py
# expect empty
```

- [ ] **Step 1:** Run the block.

## Forbidden moves

- Writing demotions.
- Touching locked constants.
- Claiming a live 2026-08-08 review executed.
- Bundling Call-1 σ-source.
