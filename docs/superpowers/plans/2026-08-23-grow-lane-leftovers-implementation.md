# Grow-lane leftovers — `burned_segments` → `open_run` and named slices

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**AUTHORIZATION:** Accepted ADR [`2026-08-22-grow-lane-build-authorization.md`](../../adr/2026-08-22-grow-lane-build-authorization.md) — this plan is executable. That ADR already licenses per-slice commits. It does **not** open a GROW-1 campaign.

**Goal:** Wire the existing standalone `burned_segments` checker into `register_search.open_run` (disclosure + refuse-on-overlap for deep lane), then land the remaining named forward slices that still have no plan. **Skip GROW-0** — [`2026-08-22-grow0-harness-implementation.md`](2026-08-22-grow0-harness-implementation.md) already exists and ran to `RESOLVED`.

**Architecture:** Reuse `lab/discovery/burned_segments.py` (`is_window_burned`, `consultation_count`, `consultation_history`). Call it from `open_run` **before** `_save`. Absence of a window is neither burned nor clean — do not auto-pass (ADR §5).

**Tech Stack:** Python 3.11+, existing `tests/test_discovery_burned_segments.py`, `PYTHONPATH=lab`.

## Global Constraints

- `$0 / K=0`. No Databento pull. No campaign open.
- Do not treat an unlisted window as safe.
- Charter §2.2(iv) is disclosure-only — consultation count must be written onto the manifest, not used as a refuse.
- Overlap with a burned segment **refuses** a `--lane deep` open (GROW spec Boundary / finding B1). Other lanes: disclose only unless a later slice says otherwise.
- Do not re-derive `floor_at_k` / admission arithmetic.

## Rule 0 (verified 2026-08-23)

| Source | Anchor | What it pins |
|---|---|---|
| Build ADR §2 item 2 + §7 log | `70029e6` | Checker landed; `open_run` wiring named forward work |
| `lab/discovery/burned_segments.py` | `fcb4ac7` | `consultations` list; standalone; not wired |
| `lab/discovery/register_search.py` `open_run` | `a5ee05e` | `--lane deep` exists; no burned-segment call |
| `discovery_manifests/burned_segments.json` | `fcb4ac7` | Seed MNQ 2025-09-01→2026-08-05 |
| Two-ledger K ADR | `fcb4ac7` | §2.2(iv) disclosure-only |

## File Structure

| File | Change |
|---|---|
| `lab/discovery/register_search.py` | Before `_save`: load window from args; if `--lane deep` and `is_window_burned` → ABORT no write; always write `burned_consultation` disclosure block onto deep (and optionally all) manifests |
| `tests/test_discovery_burned_segments.py` or new `tests/test_register_search_burned.py` | Overlap refuses deep open; unlisted window opens and records `consultation_count=0`; no silent pass |
| Build ADR §7 log | Date the wiring slice |

Named leftover slices (each is its own later commit under this ADR; specify in Task 5 only as follow-on, do not build in the first wiring PR unless already trivial):

1. Charter §4 streak checker
2. `gates.yml` door-check limb
3. LOCKED-leg denylist
4. Rule-0 anchor checker
5. `universe_gate` exit-code propagation

---

### Task 1: Failing tests for `open_run` wiring

- [ ] **Step 1:** Write a test that `open_run --lane deep` against the seed MNQ window ABORTs and writes **no** manifest.
- [ ] **Step 2:** Write a test that an unlisted (instrument, window) opens and the manifest carries `consultation_count == 0` plus empty history — not a "clean" boolean.
- [ ] **Step 3:** Run tests — red.

### Task 2: Wire `open_run`

- [ ] **Step 1:** Parse confirm/train window args already required for `--lane deep` (do not invent a second window flag if `confirm` dates already exist). If dates are missing, ABORT with the existing deep-admission message, not a new silent default.
- [ ] **Step 2:** Call `is_window_burned` / `consultation_history`. Refuse deep on overlap. Always attach disclosure fields.
- [ ] **Step 3:** Tests green.

### Task 3: Docstring honesty

- [ ] **Step 1:** Update `burned_segments.py` module docstring: no longer "NOT yet wired".
- [ ] **Step 2:** Append a §7 log row on the build ADR.

### Task 4: Verification

```bash
PYTHONPATH=lab pytest tests/test_discovery_burned_segments.py tests/test_register_search_burned.py -q
grep -n "is_window_burned\|consultation_count" lab/discovery/register_search.py
```

- [ ] **Step 1:** Run the block.

### Task 5: Follow-on slices (separate commits)

For each leftover name above, before scaffolding: `git fetch origin && git log --oneline origin/main ^HEAD | head -20` and grep the build ADR §7 log. Skip any slice that already has a dated commit. Each slice gets its own commit against this ADR — no new ADR unless doctrine changes.

- [ ] **Step 1:** After Task 4, stop unless the operator asked to continue slices in the same PR.

## Forbidden moves

- Silent auto-pass on unlisted windows.
- Using `consultation_count` as a refuse.
- Opening GROW-1 / spending K.
- Re-implementing GROW-0.
- Changing charter §4 counters.
