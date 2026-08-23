# Tradable-anomalies T3 — scanner calibration + admission tooling (ready-to-execute-on-GO)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**AUTHORIZATION: GO 2026-08-23.** Owning ADR [`2026-07-11-tradable-anomalies-statistics-adoption.md`](../../adr/2026-07-11-tradable-anomalies-statistics-adoption.md) §7 T3. T2 landed first in the same GO.

**Goal:** After GO: GARCH-fitted-null / surrogate-data calibration (also upgrades corpus-FDR IID-Gaussian null); promote ENB + downside-correlation + with/without-candidate marginal-delta into committed tools. Recover Q-NEFF-1 computation into the ENB breadth column (operator Track C).

**Architecture:** Extend existing `lab/research_utils/breadth.py` rather than a third breadth owner. Surrogate pipeline is a library + tests; no live-risk surface.

**Tech Stack:** `arch` GARCH, numpy RNG for surrogates, existing breadth helpers.

## Global Constraints

- No execution without GO.
- Do not change IID-Gaussian defaults silently — calibration is additive, with a dated RESULTS note.
- Do not extract `portfolio_mc` (ADR: confirmed unnecessary).
- No locked-constant writes.

## Rule 0 (verified 2026-08-23)

| Source | Anchor | What it pins |
|---|---|---|
| Adoption ADR §7 T3 | `027a729` | Deferred |
| `lab/research_utils/breadth.py` | (living) | Existing ENB / participation |

---

### Task 1: Pre-GO

- [x] **Step 1:** Pre-GO inventory: ENB/PR present; GARCH/surrogate/downside-corr owed.
- [x] **Step 2:** GO 2026-08-23.

### Task 2: On GO — test-first

- [x] **Step 1:** `tests/test_breadth_t3.py` FPR band `[0.01, 0.15]`.
- [x] **Step 2:** Downside-corr + `marginal_admission_delta` fixture.
- [x] **Step 3:** Extended `breadth.py`. Dated note under `docs/notes/research/` (no new `lab/analysis/` slug).

## Forbidden moves

- Executing T3 from Tranche-1 Accept.
- Silent null-swap on corpus-FDR.
- `portfolio_mc` extraction.
- New `lab/analysis/` slug without catalog grep.
