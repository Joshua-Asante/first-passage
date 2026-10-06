# CC handoff — four-firm re-MC §8 step 2(c): per-tier series through `score_candidate`

**Date:** 2026-10-06.
**Status:** FROZEN for build, 2026-10-06. Joshua directly: "GO", given in this worker's chat and also to coordinator (4).
**Brief type:** CC handoff, bounded build (worker card); a code PR.
**Authority:** operator go, 2026-10-06. Requirement owner: the four-firm dated re-MC prereg ([PR #616](https://github.com/Joshua-Asante/first-passage/pull/616)), I-19 (each tier netted at its own cost), §7 blocker 4 and §8 step 2(c). The finding behind it is #616 re-check 6007340149 P2.
**Rule:** synthetic inputs only. The existing single-series call is unchanged. One call produces one run and one report.
**Return boundary:** a code PR with red-first tests and launcher records, or a precise blocker. Codex reviews pushes on its own; do not post `@codex review`. No force-push.

## §0 — Production reads (`main@f04d1e5`, 2026-10-06)

Read at `main` `f04d1e5` on 2026-10-06.

| Surface | Finding |
|---|---|
| `lab/discovery/prop_survivor_scoring.py` `score_candidate` | It takes one `candidate_daily_pnl` (plus an optional `intraday_low`) and reuses the same blocks for every tier. The `tiers=` override is for unit tests only. |
| `lab/discovery/remc_series_builder.py` (#702, `e3da7e2`) | It emits per-tier `normal_pnl`/`normal_low`/`protected_pnl`/`protected_low`, already cost-netted per tier. |
| #708 (open) | Adds `protected_blocks`/`protected_intraday_blocks`/`mode_trigger` to `run_tier_remc` and the guard. Prereg I-17 fixes its merge-by-10-25 fallback. |

## §0.5 — Clarifications resolved at freeze

1. **New `TierSeries`:** `daily_pnl`, plus optional `intraday_low`, `protected_pnl` and `protected_low`.
2. **New keywords on `score_candidate`:** `tier_series: Mapping[str, TierSeries]` and `mode_trigger`.
3. **Fail closed** on any of these:
   - the mapping's keys are not exactly the scored tiers;
   - the series lengths differ;
   - `intraday_low` is given on some tiers but not all;
   - the protected channels are given on some tiers, or one without the other, or without intraday lows;
   - `mode_trigger` is given without the protected channels, or the channels without the trigger;
   - `tier_series` is combined with the single `intraday_low`.
4. **Mode-switching** is forwarded only when the kernel has it (`run_tier_remc` accepts `protected_blocks`, i.e. after #708). Before that, protected inputs raise; they are never dropped. This works under both I-17 branches with no second edit.
5. G1 still reads `candidate_daily_pnl`. G4 and the guard read each tier's own series.

## §1 — Goal

Implement §0.5 in `lab/discovery/prop_survivor_scoring.py`, with the new test file `tests/test_score_candidate_per_tier.py`.

## §4 — Hypothesis and falsifier

**H:** each tier's G4 and guard runs use exactly that tier's paired blocks. Every misuse in §0.5 item 3 raises. The legacy call is unchanged.

**Falsified by** any of the tests below failing, or any existing scoring test changing.

## §5 — Constraints and forbidden moves

- Edit only `score_candidate` and new helpers in `prop_survivor_scoring.py`; add the new test file.
- No `core/` or `ops/` edit. No threshold or guard change. No real input. No MC on real data.

## §6 — Acceptance and return taxonomy

Tests in `tests/test_score_candidate_per_tier.py`:
- `test_each_tier_runs_on_its_own_series`
- `test_missing_or_extra_tier_fails_closed`
- `test_tier_series_excludes_the_single_intraday_argument`
- `test_mixed_or_mismatched_channels_fail_closed`
- `test_protected_channels_fail_closed_without_kernel_support_or_when_incomplete`
- `test_protected_channels_must_pair_and_need_intraday`
- `test_legacy_single_series_call_unchanged`

Plus the existing `tests/test_prop_survivor_*` and `tests/test_remc_series_builder.py`, and `check_boundaries`.

Return labels: **DONE**, **DONE_WITH_CONCERNS**, **NEEDS_CONTEXT**, or **BLOCKED**.

```yaml authority
seat: worker
parent: docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push, pr.open]
constraints:
  - no_main_write
  - no_merge
  - synthetic_inputs_only
  - no_core_or_ops_edit
  - no_existing_test_edit
  - no_threshold_or_guard_change
  - no_force_push
  - no_codex_review_comment
acceptance:
  - tests/test_score_candidate_per_tier.py
```

## §7 — Return

**DONE (2026-10-06).** The coordinator (4) worker wrote it directly; this is gate-harness integration work.

- **Red:** `20261006T012159Z-686bfc86cfce`. Collection failed because `TierSeries` was absent.
- **Green:** `20261006T012402Z-4963b08bbd90`, 63 passed. That covers the new file, `test_prop_survivor_scoring`, `test_prop_survivor_intraday_channel`, `test_prop_survivor_score_candidate_intraday` and `test_remc_series_builder`.
- `check_boundaries` OK; LF line endings.

## §10 — Audit hooks

```bash
python -I scripts/fp.py python -m pytest -q tests/test_score_candidate_per_tier.py tests/test_prop_survivor_scoring.py
```
