# Tradable-anomalies T2 — event-study harness + cheap detector kit (ready-to-execute-on-GO)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**AUTHORIZATION: PENDING OPERATOR GO.** Owning ADR [`2026-07-11-tradable-anomalies-statistics-adoption.md`](../../adr/2026-07-11-tradable-anomalies-statistics-adoption.md) parked T2 on the forward board. Tranche 1 doctrine already landed. This plan is not a GO and does not restore `guardian_signal.py`.

**Goal:** After GO, land a reusable event-study harness (constraint/flow family first) and a cheap detector kit: Lo–MacKinlay VR (already-installed `arch`/`statsmodels` path), Ljung-Box on r vs |r|, HAC-t, autocorrelation-corrected n_eff.

**Architecture:** `lab/research_utils/` library functions + thin CLI. No locked-constant writes. Skip-if-missing vendor CSVs.

**Tech Stack:** Python 3.11+, `statsmodels`, `arch`, pandas/numpy.

## Global Constraints

- No execution without GO.
- Do not touch `dd_protection` / Pine / allocations.
- Do not restore `guardian_signal.py` as a drive-by.
- First family = constraint/flow (JPY month-end is the named prior) — do not start with a new family.

## Rule 0 (verified 2026-08-23)

| Source | Anchor | What it pins |
|---|---|---|
| Adoption ADR §7 T2 | `027a729` | Deferred board item |
| `docs/methodology/references/statistics-of-tradable-anomalies.md` | Tranche 1 | REFERENCE, not canonical |

---

### Task 1: Pre-GO inventory

- [ ] **Step 1:** Grep `lab/` for existing VR / Ljung-Box / HAC helpers so this plan does not duplicate.
- [ ] **Step 2:** Stop for GO.

### Task 2: On GO — failing tests then kit

- [ ] **Step 1:** Synthetic tests: white-noise VR ≈ 1; known-AR n_eff < n; event-study recovers a planted mean shift.
- [ ] **Step 2:** Implement. CLI writes a JSON report, not a lock decision.

### Task 3: Verification

```bash
PYTHONPATH=lab pytest tests/test_event_study.py tests/test_detector_kit.py -q
git diff --stat -- core/dd_protection.py core/firm_rules.py
# empty
```

## Forbidden moves

- Executing T2 because Tranche 1 Accepted.
- Restoring `guardian_signal.py`.
- Promoting a detector into a LOCK CANDIDATE.
