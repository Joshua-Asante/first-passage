# CC handoff — O-4 Slice A: intraday-honest channel through `score_candidate`

**Date:** 2026-10-02.
**Status:** FROZEN for build by coordinator (3), 2026-10-02. Slice A only. Slice B (§8) is conditional and **not authorized**; nothing in this card dispatches it.
**Brief type:** CC handoff, bounded build (worker card).
**Authority:** Coordinator (3) authorizes Slice A. The requirement is the operator ruling of 2026-10-02 (O-3 RESOLVED): the intraday-honest clock is mandatory on every gating tier read; EOD-clock reads may be reported, never gate a clear (prereg I-12).
**Requirement owner:** four-firm dated re-MC prereg, PR #616, branch `claude/four-firm-remc-prereg-draft` at `4c09f33`, file `docs/briefs/pre-registration/2026-10-02-four-firm-dated-remc-prereg-DRAFT.md` (I-12 adopted; I-13/O-4, O-6 open; §7 blocker 4; §8 step 2). That prereg is not on `main` at this card's base.
**Rule:** synthetic inputs only. No candidate, calibration reference or venue data goes through any tier, replay or MC before the prereg reads `FROZEN` (prereg §R).
**Selected outcome:** `score_candidate` accepts a paired `intraday_low` series, threads it into every G4 run on every tier that reaches G4, runs the frozen non-vacuity guard per such tier, and labels the report `breach_clock` / `gate_grade`; the EOD path keeps every existing figure.
**Return boundary:** a reviewed synthetic build plus launcher evidence, or a precise blocker. No real-candidate run, no prereg/ADR/STATE edit, no Slice B work.

## §0 — Production reads

Read at `main` `d5d559b` (2026-10-02), the base of branch `claude/remc-o4-slice-a`. The draft's anchors (taken at `4c09f33`) were re-checked; every line number below is verified at `d5d559b`. Re-read at dispatch and report any drift before editing.

| Surface | Finding at `d5d559b` |
|---|---|
| `lab/discovery/prop_survivor_scoring.py::score_candidate` (:632) | Keyword-only; no `intraday_low` argument. Builds `blocks_from_daily_pnl(candidate_daily_pnl)` (:671) and calls `run_tier_remc` for Run-1 (:700) and Run-2 (:708) without `intraday_blocks`, so every tier read is EOD-clock. When a tier has no consistency rule, Run-2 is Run-1 (`gated_on="run1_degenerate"`), one call only. G2-killed tiers get a `TierScore` with `gated_on="g2_killed"` and no run. G1 halt (`envelope_verdict == "NO"`) returns before G2. |
| same, `run_tier_remc` (:557) | Accepts `intraday_blocks` and forwards it to `run_seed`; result dict carries `"intraday_low": intraday_blocks is not None`. Kwargs: `firm_kwargs(firm_key, inactivity_off=True, consistency=consistency)`. |
| same, `paired_blocks_from_daily` (:397) | Returns `(pnl_blocks, low_blocks)`, each `(n_weeks, 5, 1)`, on the same `pd.bdate_range("2020-01-06", …)` index. Raises `ValueError` on length mismatch, fewer than 5 days, or any `low > 0`. **Does not reject NaN/inf** (`NaN > 0` is False). |
| same, `blocks_from_daily_pnl` (:378) | Uses `core.mc.ingest.build_week_blocks` (`core/mc/ingest.py:191`), whose Monday-anchor comprehension is the same as the one in `paired_blocks_from_daily`; the P&L blocks are therefore element-equal. |
| same, `assert_intraday_channel_nonvacuous` (:477) | Frozen Phase-4 §1 guard. Runs three arms (EOD, zeros, real) over `thresholds.seeds` with `n_sims` (required) and `thresholds.horizon`; default kwargs `firm_kwargs(firm_key, inactivity_off=True, consistency=_consistency_frac(firm_key))`, the Run-2 setting. Raises `AssertionError` if zeros ≠ EOD or if real == EOD on both `headline_bust` and `pass_rate`. |
| same, `ScoringReport` (:137), `to_dict` (:151), `TierScore` (:124), `main` (:777) | `to_dict` emits 10 keys: `strategy_label, g1, g2_by_tier, tiers, routing, funded_ruin_tier_count, discharges_falsifier, halted_at, thresholds_source, regime_robustness_gate`. CLI reads `--daily-pnl-csv`, `--trades-csv`, `--envelope`, `--out`, `--prereg`, `--n-sims`; no intraday input. |
| `core/mc/simulation.py` `simulate_path` (:309), `run_seed` (:475) | Engine supports the channel. `intraday_low=None` is byte-identical legacy. Floor still ratchets on EOD equity; only the tested equity becomes `min(equity_new, equity + low*scale)`. `run_seed` draws one index set per sim and applies it to both channels, so RNG use does not change. `intraday_low` inside `firm_kwargs` is rejected (:500). Daily-loss check and `max_dd` stay EOD (docstring); all four frozen tiers have `daily_loss_pct=None` at this base. **No core change is needed.** |
| `core/mc/preflight.py` `firm_kwargs` (:131), `summarize_outcomes` (:268), `BUST_KEYS` (:70) | Per-tier kwargs for all four tiers; `headline_bust` = daily+static+trailing. |
| `tests/test_prop_survivor_scoring.py` (393 lines), `tests/test_prop_survivor_intraday_channel.py` (224 lines) | Existing coverage of the loader, G1–G8, F1/F2, e2e (`_TEST_SIMS = 40`, v2 prereg), and of the channel primitives. `test_no_ceiling_literals_outside_loader_and_tests` (:104) forbids `"0.03" "0.01" "0.50" "0.5)" "10000" "10_000" "3.0%" "50%"` anywhere after `def reduce_to_deployable` in the module. |
| Other importers | `lab/research_utils/book_score.py`, `tests/test_book_score.py`, `tests/test_msl_score.py`, `tests/test_nsurv_channel.py`, `lab/analysis/c1/…` scripts. A new keyword with a default is non-breaking. |
| `lab/discovery/grow0_red_patch.py` :24-30 | A docstring calls `prop_survivor_scoring.py` "locked production code". No hash pin, test or gate enforces that (searched `tests/`, `scripts/`, manifests). Coordinator (3)'s authorization covers this edit; the stale docstring is routed in §8, not edited by the worker. |
| Layering | `lab → core` only; `lab↔ops` forbidden (`scripts/check_boundaries.py`, OK at `d5d559b`). |

Baseline at `d5d559b` (this freeze session): `python -I scripts/fp.py doctor` OK (ops-env, Python 3.13.2, 62 locked packages matched). `python -I scripts/fp.py python -m pytest tests/test_prop_survivor_scoring.py tests/test_prop_survivor_intraday_channel.py tests/test_book_score.py tests/test_msl_score.py tests/test_nsurv_channel.py -q` → 49 passed, 2 skipped; record `.cache/fp-verification/20261003T011717Z-670287b595dc/record.json` (`status: completed`, `verification_exit_code: 0`, `source_stable: true`), worktree-local. `check_boundaries.py` OK.

## §0.5 — Clarifications resolved at freeze

(A) Guard depth is the gating depth (`n_sims`, else `thr.sims_per_seed`). O-6 may change depth later through the prereg; Slice A adds no depth parameter.
(B) A vacuous channel is reported, not raised: `gate_grade=False` with reasons (prereg INSUFFICIENT). An invalid channel (length, sign, non-finite) raises `ValueError`.
(C) When no tier reaches G4, a supplied channel gives `gate_grade=True`, because G1 and G2 are clock-independent.
(D) `discharges_falsifier` is not gated inside the module; consumers read it together with `gate_grade` (I-12).
(E) The only existing function whose behaviour changes is `paired_blocks_from_daily`, which now also rejects non-finite input.

## §1 — Goal

Make `score_candidate` able to produce a gate-grade, intraday-honest read on every tier that reaches G4, and make an EOD or vacuous read impossible to mistake for one. This is design-neutral under O-4: design (i) consumes it directly; design (ii) could emit `(daily_pnl, intraday_low)` arrays for it to score.

## §2 — Build contract

**Branch:** one writer, proposed `claude/remc-o4-slice-a-build`, cut from this card's frozen commit.

**Allowed files (exactly):**
- `lab/discovery/prop_survivor_scoring.py` (modify)
- `tests/test_prop_survivor_score_candidate_intraday.py` (new)

Existing test files are read-only: they must pass **unchanged**, which is part of the EOD-identity proof.

**Changes:**
1. `paired_blocks_from_daily`: also raise `ValueError` if either channel contains a non-finite value (NaN or ±inf). Existing checks and messages stay.
2. `score_candidate(..., intraday_low: np.ndarray | None = None)` (keyword-only, like every other argument).
   - If `intraday_low` is given, call `paired_blocks_from_daily(candidate_daily_pnl, intraday_low)` **before G1**, so invalid input raises even when G1 would halt. Use the returned P&L blocks as `blocks` and the low blocks as `intraday_blocks`.
   - For every tier that passes G2 and G3: run `assert_intraday_channel_nonvacuous(blocks, intraday_blocks, thresholds=thr, firm_key=firm_key, n_sims=sims)`, where `sims` is `n_sims` if given, else `thr.sims_per_seed`. No new depth parameter (O-6 owns depth). Catch `AssertionError` only when its message starts with `"non-vacuity FAIL"` and record `f"{firm_key}: non-vacuity failed: {exc}"` in the reasons list; re-raise any other `AssertionError` (for example the `summarize_outcomes` bucket-sum invariant), which is an engine fault and not a vacuity finding. Then run Run-1 and Run-2 with `intraday_blocks=intraday_blocks` regardless of the guard outcome; the figures stay reportable.
   - If `intraday_low` is `None`: the code path is unchanged. `blocks_from_daily_pnl` is used, `run_tier_remc` is called exactly as today, and the guard is not called.
3. `ScoringReport` gains three fields, with defaults so existing constructors still work: `breach_clock: str` (`"eod"` or `"intraday_honest"`), `gate_grade: bool`, `gate_grade_reasons: list[str]`. `to_dict` adds exactly these three keys. `TierScore` is unchanged.
   - No channel: `breach_clock="eod"`, `gate_grade=False`, reasons hold one entry that says no `intraday_low` was supplied and the EOD-clock read is reportable, never gating (I-12).
   - Channel given: `breach_clock="intraday_honest"`; `gate_grade = not reasons`. When no tier reaches G4 (G1 halt, or every tier G2-killed) no breach-clock read exists, so `gate_grade=True`. Both fields are set on every return path, including the G1 early return.
4. `discharges_falsifier`, G1–G8 logic, the v2 thresholds and the loader are unchanged. A gate-grade discharge reads `discharges_falsifier and gate_grade`; the module does not combine them.
5. CLI: optional `--intraday-low-csv`. Read the column named `intraday_low` if present, else the first column. Pass it as `intraday_low`. A row-count mismatch raises the `paired_blocks_from_daily` `ValueError`. Append `breach_clock=… gate_grade=…` to the existing summary print line; the JSON comes from `to_dict`.
6. No new literal from the forbidden list in §0 after `def reduce_to_deployable`; no public name added to `__all__` (private helpers use a `_` prefix).

**EOD byte-identity requirement:** with `intraday_low=None`, every value in `g1`, `g2_by_tier`, `tiers` (all `run1`/`run2` figures and rates), `routing`, `funded_ruin_tier_count`, `discharges_falsifier`, `halted_at`, `thresholds_source` and `regime_robustness_gate` is identical to `d5d559b`, and the `run_tier_remc` call sequence and arguments are identical. The only `to_dict` difference is the three added keys. Proven by test 6 plus the unchanged existing suites.

**Red-first tests** in `tests/test_prop_survivor_score_candidate_intraday.py`. Write all eight, run them, and record the failing launcher record **before** any production edit. Shared fixtures: `thr = load_scoring_thresholds()` (v2 default), `n_sims=40`, `pnl = np.full(260, 80.0)`, `trades = [80.0] * 120`, `gross_edge_usd=50_000.0`, `envelope_verdict="YES"`, and the planted channel `low = np.zeros(260); low[::35] = -10_000.0` (deeper than any frozen tier's drawdown; the EOD path never busts).

1. `test_intraday_blocks_reach_every_g4_run` — wrap `discovery.prop_survivor_scoring.run_tier_remc` with a delegating spy and replace `assert_intraday_channel_nonvacuous` with a recording no-op (monkeypatch). With `intraday_low=low`: every `run_tier_remc` call has `intraday_blocks` that is not `None` and is `np.array_equal` to `paired_blocks_from_daily(pnl, low)[1]`; every `blocks` argument is `np.array_equal` to `blocks_from_daily_pnl(pnl)`. The call count per tier is 2 where `_consistency_frac(tier)` is not `None`, else 1. The guard is called exactly once per non-G2-killed tier with that tier's `firm_key` and `n_sims=40`.
2. `test_breach_clock_and_gate_grade_labels` — no channel: `breach_clock == "eod"`, `gate_grade is False`, one reason. Planted channel: `"intraday_honest"`, `gate_grade is True`, `gate_grade_reasons == []`. G1 halt (`envelope_verdict="NO"`): with channel, `gate_grade is True` and `halted_at == "G1"`; without channel, `gate_grade is False`.
3. `test_vacuous_channel_reports_not_gate_grade` — `intraday_low=np.zeros(260)`: no exception escapes; `breach_clock == "intraday_honest"`, `gate_grade is False`, and every tier key appears in a reason that contains `"non-vacuity"`. Tier figures are still present.
4. `test_invalid_intraday_low_raises` — parametrized `ValueError` cases: length mismatch (259 vs 260); one entry `+1.0`; one `NaN`; one `+inf`; one `-inf`; one `NaN` in `candidate_daily_pnl` with a valid channel. Each also raises with `envelope_verdict="NO"`, which shows validation happens before G1.
5. `test_intraday_bust_not_below_eod_per_tier` — the same inputs with and without the planted channel (same seeds, same `n_sims`). For every tier: Run-1 and Run-2 `headline_bust` with the channel is ≥ EOD, `pass_rate` with the channel is ≤ EOD, and Run-2 `headline_bust` with the channel is strictly greater than EOD.
6. `test_eod_path_identical` — `intraday_low=None`, with the guard monkeypatched to raise if called. For every tier, `run1`/`run2` `headline_bust`, `pass_rate` and `rates` equal (exact `==`) a direct `run_tier_remc(tier, blocks_from_daily_pnl(pnl), thr, n_sims=40, consistency=None / _consistency_frac(tier))`. `set(report.to_dict())` equals the 10 keys listed in §0 plus `{"breach_clock", "gate_grade", "gate_grade_reasons"}`.
7. `test_cli_intraday_low_csv_round_trip` — write `pnl`, `trades` and `intraday_low` CSVs to `tmp_path`; `main([... "--n-sims", "40", "--intraday-low-csv", path])` returns 0, and the JSON has `breach_clock == "intraday_honest"` and a bool `gate_grade`. Without the flag: `"eod"` and `False`. A 259-row intraday CSV raises `ValueError`.
8. `test_discharge_rule_unchanged_on_intraday_path` — for the planted and the all-zero channels: `report.discharges_falsifier == discharges_falsifier(report.tiers, thr)`. For the all-zero channel, `report.discharges_falsifier and report.gate_grade` is `False`. Existing `test_discharge_requires_trailing_locking` and `test_discharge_needs_two_firms` stay green unchanged.

## §3 — Method

Read §0's anchors and report drift → write the eight tests → run them and keep the failing record (red) → edit the module → run §6's commands → `git diff --stat` before each commit → push the build branch → return.

## §4 — Hypothesis and falsifier

**H:** with a paired `intraday_low`, every G4 run on every tier that reaches G4 tests the barrier against the intraday excursion, a vacuous channel can never yield `gate_grade=True`, and EOD callers get identical figures.
**Falsifier:** an engine-invariant `AssertionError` swallowed as a vacuity reason; any `run_tier_remc` call in channel mode with `intraday_blocks=None`; any EOD-path figure or call argument differing from `d5d559b`; `gate_grade=True` for an all-zero channel or for no channel; NaN/inf accepted; an existing test needing an edit to pass.

## §5 — Constraints and forbidden moves

- Edit only the two §2 files. Forbidden: `core/**` (including `core/firm_rules.py`, `core/mc/**`, `core/dd_protection.py`); `ops/**`; all of `docs/**` (prereg, ADRs, STATE, this card); `scripts/**`; other `lab/**` files (including `grow0_red_patch.py`); existing test files; `pyproject.toml`, `.claude/**`.
- No change to v2 prereg numbers, the loader, the tier set, seeds, horizon, `discharges_falsifier` or the guard's logic.
- Synthetic inputs only. No real candidate, calibration reference, TV export, vendor CSV, Pine, port, `effective_inputs.json`, private data, account identifier or P&L.
- No `glm_agent` dispatch with a `workdir` containing `.env`. No `git stash`. No merge, no push to `main`, no operator act.

## §6 — Acceptance and return taxonomy

From the build worktree (Git Bash):

```bash
python -I scripts/fp.py doctor
python -I scripts/fp.py python -m pytest tests/test_prop_survivor_score_candidate_intraday.py -q   # red first, before the module edit; then green
python -I scripts/fp.py python -m pytest tests/test_prop_survivor_scoring.py tests/test_prop_survivor_intraday_channel.py tests/test_prop_survivor_score_candidate_intraday.py tests/test_book_score.py tests/test_msl_score.py tests/test_nsurv_channel.py -q
python -I scripts/fp.py python scripts/check_boundaries.py
python -I scripts/fp.py check
git diff --exit-code d5d559b -- tests/test_prop_survivor_scoring.py tests/test_prop_survivor_intraday_channel.py core ops docs
git diff --stat d5d559b...HEAD
git diff --check d5d559b...HEAD
```

Cite each launcher `record.json` path with `status`, `verification_exit_code`, `source_stable` and pass/skip counts. The green regression run must have `status: completed`, exit 0 and `source_stable: true`, with at least the baseline's 49 passed / 2 skipped plus the new tests. Disclose any pre-existing `check` failure with its record; never call the gate suite passing if it is not.

Return measurement (for O-6, synthetic only, not a test): wall-clock of one `score_candidate` call on the planted fixture at default depth (`n_sims=None`, i.e. the prereg depth) on one tier, which covers the guard's three arms plus Run-1 and Run-2.

The coordinator marks Slice A **RESOLVED** (synthetic scope) only when all eight tests and the regression run pass on records that meet the standard above and the diff touches only §2's files. A failed criterion is **FALSIFIED**; missing evidence is **AMBIGUOUS**, not acceptance.

Return exactly one status:
- DONE: every criterion established, no unresolved concern.
- DONE_WITH_CONCERNS: established, with disclosed unrelated baseline limitations.
- NEEDS_CONTEXT: an anchor drifted, owner text conflicts, or the work needs a file outside §2. Name it.
- BLOCKED: context-problem, capability-problem, scope-problem or plan-itself-wrong, with the exact obstruction.

## §7 — Coordinator record (2026-10-02)

```yaml authority
seat: worker
parent: docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push, pr.open]
constraints:
  - no_main_write
  - no_merge
  - section_2_footprint_only
  - no_core_or_ops_edit
  - no_docs_edit
  - no_existing_test_edit
  - synthetic_inputs_only
  - no_private_source_read
  - no_threshold_or_guard_change
  - no_slice_b_work
  - no_owner_record_edit
acceptance:
  - tests/test_prop_survivor_score_candidate_intraday.py::test_intraday_blocks_reach_every_g4_run
  - tests/test_prop_survivor_score_candidate_intraday.py::test_breach_clock_and_gate_grade_labels
  - tests/test_prop_survivor_score_candidate_intraday.py::test_vacuous_channel_reports_not_gate_grade
  - tests/test_prop_survivor_score_candidate_intraday.py::test_invalid_intraday_low_raises
  - tests/test_prop_survivor_score_candidate_intraday.py::test_intraday_bust_not_below_eod_per_tier
  - tests/test_prop_survivor_score_candidate_intraday.py::test_eod_path_identical
  - tests/test_prop_survivor_score_candidate_intraday.py::test_cli_intraday_low_csv_round_trip
  - tests/test_prop_survivor_score_candidate_intraday.py::test_discharge_rule_unchanged_on_intraday_path
```

The PR body states "synthetic inputs only". Codex PR review is the independent review; Joshua retains the merge. Executor returns go to coordinator (3), which records acceptance here.

## §8 — Out of scope, routed findings and Slice B

- **Slice B (CONDITIONAL, NOT AUTHORIZED).** Per-tier parameterization of the T00 replay path, `ops/c1_rail/qualification/runner.py::evaluate_replay` (:20), whose kernel call hard-codes `firm_kwargs('Tradeify_Select_100K', inactivity_off=True, consistency=.40, …)` (:27). It triggers only if the operator rules O-4 design (ii) **and** O-5 "parameterize per tier", and then only through its own frozen card. Per-firm own-flat deadlines are not in code; encoding them in `core/firm_rules.py` would be a separately authorized core change.
- **Routed to coordinator (3); the worker does not act on these:**
  1. The guard compares only `headline_bust` and `pass_rate`. A tier that is saturated under EOD (bust 1.0, pass 0.0), or whose real excursions never cross the floor, fails non-vacuity, so the report reads `gate_grade=False` (prereg INSUFFICIENT) and not FAIL. Whether §4 should map that case differently belongs to the prereg owner (O-13 / §4), not to Slice A.
  2. `gate_grade` is report-level: one vacuous tier makes the whole report non-gate-grade. This is consistent with prereg INSUFFICIENT ("missing synchronized `intraday_low` for a gating tier").
  3. Cost: per gating tier, intraday mode runs five `run_seed` loops (three guard arms, Run-1, Run-2). The guard's real arm uses the same kwargs, seeds, depth and horizon as Run-2, so it duplicates Run-2. Reusing that result is an O-6 budget option, not part of Slice A.
  4. `lab/discovery/grow0_red_patch.py` :24-30 calls the module "locked" and describes the EOD default gap; after merge the second clause is stale. The fix is a separate lab edit.
  5. The source of a paired `intraday_low` for any real candidate is not established (Databento retired; the T00 producer is Tradeify-only). Without it every gating read is INSUFFICIENT.

## Pre-mortem

- **Loop cost:** single build loop; the test file runs about 10 `score_candidate` calls at 40 sims. The baseline suite took about 3 min.
- **Decisions the executor will hit:** none open. The G1-halt `gate_grade`, the guard depth, the CLI column choice and the vacuity handling are fixed in §2.
- **What makes it moot:** an O-4 ruling that no daily-block design is used and design (ii) never emits arrays for lab scoring. Slice A is still the only lab path that can label a read gate-grade.
- **Evidence binding:** records count only at the build branch head with `source_stable: true`; any later production edit invalidates them.

## §10 — Audit hooks

```bash
python -I scripts/fp.py python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-10-02-remc-o4-slice-a-build-card.md
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-02-remc-o4-slice-a-build-card.md
grep -n "def score_candidate\|def run_tier_remc\|def paired_blocks_from_daily\|def assert_intraday_channel_nonvacuous\|def main" lab/discovery/prop_survivor_scoring.py
grep -n "def simulate_path\|def run_seed" core/mc/simulation.py
grep -n "Tradeify_Select_100K" ops/c1_rail/qualification/runner.py
```
