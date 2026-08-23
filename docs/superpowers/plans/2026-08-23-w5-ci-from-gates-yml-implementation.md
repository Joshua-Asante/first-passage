# W5 — derive CI jobs from `scripts/gates.yml`

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**AUTHORIZATION:** Accepted ADR [`2026-08-07-w5-governance-diet.md`](../../adr/2026-08-07-w5-governance-diet.md) — this plan is executable. It **is** the dedicated CI-composition commit that ADR §5 forbids doing casually. It is **not** a branch-protection / required-checks GO ([`Q-GATESTACK-1`](../../briefs/closures/Q-GATESTACK-1-closure-falsified.md) Limb-A stands).

**Goal:** Adding or removing a hard gate is a `gates.yml` edit (plus tests). GitHub Actions runs that same composition instead of a second hand-list in `.github/workflows/skills-check.yml`.

**Architecture:** One new (or retargeted) workflow job calls `python scripts/gate_manifest.py --tier check`. Companion jobs that are **not** gates stay: pytest, pylint, lab `validation-controls`, pine-pin-provenance (`--base`), SHA256SUMS format, no-vendor-csv. Do not invent a `--tier ci` unless `--tier check` is proven insufficient.

**Tech Stack:** GitHub Actions, existing `gate_manifest.py` (stdlib YAML subset), pytest for composition tests.

## Global Constraints

- **No gate dropped.** Every `id` in [`scripts/gates.yml`](../../../scripts/gates.yml) must run in CI via the runner (or a named, dated exception in this plan).
- Do **not** use `tier: soft` (dead — no caller; `gates.yml` header).
- Do **not** collapse `check_brief.py` (ADR: later).
- Do **not** add required status checks / branch protection.
- Do **not** change pre-commit or Make behavior except deleting a now-duplicate hand-list.

## Rule 0 (verified 2026-08-23)

| Source | Anchor | What it pins |
|---|---|---|
| Owning ADR + addenda | `91e6caa` / later | CI-from-`gates.yml` owed; `make check` = always + path-conditional + forced `data-manifests` |
| `scripts/gates.yml` | `d48f7de` 2026-08-17 | Composition authority |
| `scripts/gate_manifest.py` `select_gates` | `91e6caa` | `--tier check` already is the full battery |
| `.github/workflows/skills-check.yml` | `027a729` | Hand-duplicates skill-refs, skills-no-constants, path-liveness, status-consistency, adr-graph, lab-catalog, instrument-profiles |
| `.github/workflows/tests.yml` | `91e6caa` | Extra `check_boundaries.py` + pytest; 3.11-only |
| `.github/workflows/validation-controls.yml` | (lab pytest) | Path-filtered companion — **not** a `gates.yml` drop |
| `.github/workflows/manifest-check.yml` | | Format-only SHA256SUMS + pine-pin-provenance `--base` — CI-only, keep |

`--tier check` does **not** run `pursuit-records` (data-conditional, not forced). Name that as a dated exception: keep `check_pursuit_records.py` on `docs/pursuits/` path filter, or add a forced include. Do not silently drop it.

## File Structure

| File | Change |
|---|---|
| `.github/workflows/gate-manifest.yml` | **Create.** `python scripts/gate_manifest.py --tier check` on PR + push-to-main. Install `requirements-ops.lock` + ripgrep (some gates may need `rg`). |
| `.github/workflows/skills-check.yml` | Replace duplicated gate steps with a pointer comment **or** delete the overlapping job once `gate-manifest.yml` is green. |
| `.github/workflows/tests.yml` | Drop the standalone `check_boundaries.py` step (now inside `--tier check`). Keep pytest. |
| `tests/test_gate_manifest.py` | Add: CI mapping test — every `always`/`path-conditional`/`data-manifests` id is selected by `--tier check`; document `pursuit-records` disposition. |
| Owning ADR Change History | One line: CI composition landed. |

---

### Task 1: Failing composition test

- [ ] **Step 1:** Add a test that `select_gates(..., "check")` contains every gate id with `tier in {always, path-conditional}` plus `data-manifests`, and that a new fixture id would fail if omitted from that set.
- [ ] **Step 2:** Run `pytest tests/test_gate_manifest.py -q` — red until Task 2 if you assert a workflow file exists.

### Task 2: Workflow that calls the runner

- [ ] **Step 1:** Land `.github/workflows/gate-manifest.yml` (read permissions, pinned actions matching siblings, Python 3.11, `pip install --require-hashes -r requirements-ops.lock`, `rg` if needed).
- [ ] **Step 2:** Trigger on `pull_request` and `push` to `main` (same A-rule as `skills-check.yml` — docs PRs **must** still run this job).

### Task 3: Retire the hand-list

- [ ] **Step 1:** Remove duplicated steps from `skills-check.yml`. If the file has no remaining job, delete the workflow.
- [ ] **Step 2:** Remove `check_boundaries.py` from `tests.yml` (pytest stays).
- [ ] **Step 3:** Decide `pursuit-records`: path-filtered companion **or** force-include in `--tier check`. Record the choice in the ADR Change History.

### Task 4: Verification

```bash
python scripts/gate_manifest.py --list
python scripts/gate_manifest.py --tier check --dry-run
# every always + path-conditional + data-manifests must appear
pytest tests/test_gate_manifest.py -q
```

- [ ] **Step 1:** Run the block. Confirm no `gates.yml` id vanished from CI.

## Forbidden moves

- Dropping a hard gate under “diet.”
- `tier: soft`.
- Branch protection / required checks.
- Collapsing `check_brief.py`.
- Making `make validate` equal `make check` (Addendum 2026-08-21).
