# Tradable-anomalies T3 — scanner calibration + admission tooling (ready-to-execute-on-GO)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**AUTHORIZATION: PENDING OPERATOR GO.** Owning ADR [`2026-07-11-tradable-anomalies-statistics-adoption.md`](../../adr/2026-07-11-tradable-anomalies-statistics-adoption.md) §7 T3. Do not execute without GO. Prefer T2 landed first (null hygiene) unless the GO says otherwise.

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

- [ ] **Step 1:** Read Q-NEFF-1 closure + current `breadth.py`. List functions already present vs owed.
- [ ] **Step 2:** Stop for GO.

### Task 2: On GO — test-first

- [ ] **Step 1:** Surrogate test: null series false-positive rate within a pre-registered band.
- [ ] **Step 2:** ENB / downside-corr / marginal-delta tests against a tiny fixture.
- [ ] **Step 3:** Implement. Commit a calibration RESULTS under `lab/analysis/` only if a new slug is needed — grep `lab/CATALOG.md` first (sub-rule 8).

## Forbidden moves

- Executing T3 from Tranche-1 Accept.
- Silent null-swap on corpus-FDR.
- `portfolio_mc` extraction.
- New `lab/analysis/` slug without catalog grep.
