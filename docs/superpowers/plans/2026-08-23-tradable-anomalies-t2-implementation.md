# Tradable-anomalies T2 — event-study harness + cheap detector kit (ready-to-execute-on-GO)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**AUTHORIZATION: GO 2026-08-23.** Owning ADR [`2026-07-11-tradable-anomalies-statistics-adoption.md`](../../adr/2026-07-11-tradable-anomalies-statistics-adoption.md) §7 T2. Does not restore `guardian_signal.py`.

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

- [x] **Step 1:** Pre-GO inventory: no VR/LB/HAC helpers under `lab/`.
- [x] **Step 2:** GO 2026-08-23.

### Task 2: On GO — failing tests then kit

- [x] **Step 1:** `tests/test_detector_kit.py` + `tests/test_event_study.py`.
- [x] **Step 2:** `lab/research_utils/{detector_kit,event_study}.py` + `scripts/event_study_read.py`.

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
