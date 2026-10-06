# CC handoff — four-firm re-MC §8 step 2(c′): mode-switching kernel path

**Date:** 2026-10-05.
**Status:** FROZEN for build, 2026-10-05. Joshua directly: "go on the mode-switching code card".
**Brief type:** CC handoff, bounded build (worker card); a code PR.
**Authority:** operator go, 2026-10-05, to a coordinator (4) worker. The requirement owner is the four-firm dated re-MC prereg, [PR #616](https://github.com/Joshua-Asante/first-passage/pull/616) at `678b5d7`, I-17. Operator rulings 2026-10-05 set mode-switching, retired the `dd_scale` parity test, and fixed a fallback: "mode-switching merged on `origin/main` by 2026-10-25T23:59 ET → ON; otherwise → OFF (disclosed)". **This code may implement only the I-17 text.** Inputs are built by the series builder ([PR #702](https://github.com/Joshua-Asante/first-passage/pull/702)).
**Rule:** synthetic inputs only. Every existing call is byte-identical when the new keywords are absent. No threshold, guard or protection constant changes.
**Return boundary:** a reviewed code PR (Codex reviews exact-head pushes on its own; do not post `@codex review`), or a precise blocker. No real run. No `score_candidate` per-tier wiring: that is step 2(c).

## §0 — Production reads (`main@bf46e8f`, 2026-10-05)

Read at `main` `bf46e8f` on 2026-10-05. Re-read at dispatch and report any drift.

| Surface | Finding |
|---|---|
| `core/mc/simulation.py` `simulate_path` (:309) | At the start of each day it computes `dd_from_peak = (equity - peak) / peak` from the prior close and the running EOD `peak`, which starts at `starting_equity` and ratchets only at EOD. A day scales by `dd_scale` when `round(dd_from_peak, 6) <= -dd_trigger` (:409-410). `intraday_low[day] * scale` is added to the opening equity for the barrier test. The inactivity count and `had_activity` read the day's `strategy_pnls`. |
| same, `run_seed` (:475) | One `indices` draw per sim, applied to `blocks` and `intraday_blocks`, so both channels share block indices. |
| same, `_validate_historical_fixture` (:590) | Keyword-only parameters outside `_NON_FIRM_KEYWORDS` must mirror `HISTORICAL_CHALLENGE_FIRM_KWARGS`. Path keywords belong in `_NON_FIRM_KEYWORDS`. |
| `ops/c1_rail/book_policy.py` `is_protected` (:124), `BookProtectionClock` (:405-465) | `protected = round((peak - equity) / peak, 6) >= 0.01`, evaluated on the settled close against the EOD peak ratchet. The mode governs the next session; there is no latch. |
| `lab/discovery/prop_survivor_scoring.py` `run_tier_remc` (:577), `assert_intraday_channel_nonvacuous` (:497) | `run_tier_remc` passes `NO_PROTECTION_TRIGGER` and `DD_SCALE`, so no continuous scaling. The guard runs EOD, zeros and real arms. |

## §0.5 — Clarifications resolved at freeze

1. **Kernel surface (`simulate_path`):** new keyword-only `protected_path`, `protected_intraday_low` and `mode_trigger`, all defaulting to `None`. They are path keywords, added to `_NON_FIRM_KEYWORDS`.
   - `protected_path` and `mode_trigger` are given together or not at all.
   - `protected_intraday_low` is required exactly when `intraday_low` is given and `protected_path` is given.
   - When `protected_path` is given, `dd_trigger` must be at least 1.0, so continuous scaling is inactive. Otherwise raise `ValueError`: one protection mechanism only.
2. **Day mode:** protected when `round((equity - peak) / peak, 6) <= -mode_trigger`, using the same `equity`/`peak` the loop already holds at day start. The day then uses `protected_path[day]` and `protected_intraday_low[day]` in place of the normal channel. `scale` stays 1.0. Every other rule reads the selected channel unchanged: daily-loss, barrier, inactivity, trade days, consistency and pass. No latch.
3. **`run_seed`:** new keyword-only `protected_blocks` and `protected_intraday_blocks` (validated for the same length as `blocks`) and `mode_trigger`. They are drawn with the same `indices` as `blocks`.
4. **`run_tier_remc`:** threads the same three keywords through to `run_seed`; they default to absent.
5. **Non-vacuity guard:** given protected channels, the zeros arm zeros both lows and the real arm uses both. The guard's assertions are unchanged.
6. **Value of `mode_trigger`:** the executor passes `0.01`. A parity test in `tests/` asserts the kernel's mode sequence against `book_policy.BookProtectionClock`.

## §1 — Goal

Implement §0.5 in `core/mc/simulation.py` and `lab/discovery/prop_survivor_scoring.py`, with new tests only.

## §4 — Hypothesis and falsifier

**H:** with the new keywords absent, every existing test and output is byte-identical. With them present on synthetic paths:

- (a) the per-day mode sequence equals `BookProtectionClock`'s, settling each simulated close;
- (b) a path that never draws down 1% equals the normal-only run;
- (c) a path held at or below −1% from day 2 uses the protected channel from day 2;
- (d) equality at exactly −1.000000% (after rounding) is protected;
- (e) every misuse in §0.5 item 1 raises.

**Falsified by** any of these failing, or any existing `tests/core/test_mc_*`, `tests/test_prop_survivor_*` or seal test changing.

## §5 — Constraints and forbidden moves

- Allowed edits: `core/mc/simulation.py` (`simulate_path`, `run_seed`, `_NON_FIRM_KEYWORDS`) and `lab/discovery/prop_survivor_scoring.py` (`run_tier_remc`, `assert_intraday_channel_nonvacuous`).
- New tests: `tests/core/test_mc_mode_switching.py` and `tests/test_mode_switching_book_parity.py`.
- No other file. No existing test edited. No change to `DD_TRIGGER`, `DD_SCALE`, `NO_PROTECTION_TRIGGER`, `book_policy`, `firm_rules` or any threshold.
- `lab` does not import `ops`; only the parity test does.
- Synthetic inputs only. No private input, no MC on real data.

## §6 — Acceptance and return taxonomy

Evidence via `.\fp.ps1 python -m pytest`, cited by `record.json`:
- the new files;
- `tests/core/test_mc_intraday_barrier.py`, `test_mc_initial_state.py`, `test_mc_synthetic_engine.py`, `test_mc_module_facade.py`, `test_planted_defects.py`;
- `tests/test_prop_survivor_scoring.py`, `test_prop_survivor_intraday_channel.py`, `test_remc_series_builder.py` (if merged);
- every `tests/**/test_seal*.py`;
- `scripts/check_boundaries.py`.

Return labels: **DONE**, **DONE_WITH_CONCERNS**, **NEEDS_CONTEXT** (anchor drift or owner conflict), or **BLOCKED**.

```yaml authority
seat: worker
parent: docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push, pr.open]
constraints:
  - no_main_write
  - no_merge
  - section_5_footprint_only
  - synthetic_inputs_only
  - no_private_source_read
  - no_existing_test_edit
  - no_threshold_or_guard_change
  - no_lab_ops_import
  - default_path_byte_identical
  - no_codex_review_comment
acceptance:
  - tests/core/test_mc_mode_switching.py
  - tests/test_mode_switching_book_parity.py
```

## §7 — Return

**DONE (2026-10-06).** Built through `glm_agent` (GLM hit its iteration cap). The coordinator-side worker reviewed the full diff and added one fix: `run_seed` now fails closed when `protected_intraday_blocks` or `mode_trigger` arrives without `protected_blocks`, or `protected_intraday_blocks` without `intraday_blocks`, instead of ignoring them silently. A test was added for that.

**Files:** edits to `core/mc/simulation.py` and `lab/discovery/prop_survivor_scoring.py`; new `tests/core/test_mc_mode_switching.py` and `tests/test_mode_switching_book_parity.py`.

**Evidence (launcher records `completed`, exit 0):**
- New tests, engine suites, scoring and intraday-channel suites, and `test_seal_account_snapshot`: 248 passed (`.cache/fp-verification/20261006T000044Z-877fa287cdd9`).
- `tests/ops/qualification/test_seal.py`, `test_seal_ordering.py`, `test_replay.py` and `test_runner.py`, run as their own batch: 133 passed.
- `check_boundaries` OK; no lab→ops import.

**Disclosed:** the qualification seal suite failed 15 tests when run in one mixed selection with the core suites, and passes when run alone. That fits the documented child-bridge isolation behaviour, not this change.

## §10 — Audit hooks

```bash
# Default path unchanged: the existing engine suites pass.
python -I scripts/fp.py python -m pytest -q tests/core/test_mc_intraday_barrier.py tests/core/test_mc_synthetic_engine.py tests/test_prop_survivor_intraday_channel.py
# New acceptance.
python -I scripts/fp.py python -m pytest -q tests/core/test_mc_mode_switching.py tests/test_mode_switching_book_parity.py
# No lab→ops import (absence exits 0).
! grep -nE '^\s*(from|import)\s+(ops|c1_rail|c1_signal_daemon)' lab/discovery/prop_survivor_scoring.py
```
