# CC handoff — four-firm re-MC §8 step 2(b): daily series builder

**Date:** 2026-10-05.
**Status:** FROZEN for build, 2026-10-05. Joshua directly: "go on the series builder card".
**Brief type:** CC handoff, bounded build (worker card).
**Authority:** operator go, 2026-10-05, to a coordinator (4) worker. Requirement owner: the four-firm dated re-MC prereg ([PR #616](https://github.com/Joshua-Asante/first-passage/pull/616) at `d90a885`). This card implements:
- I-13: design (i), the lab series built from the TV exports;
- I-17: mode-switching inputs;
- I-19: per-tier cost netting;
- I-24: the MFFU 16:10 flag;
- §7 blocker 4 and §8 step 2(b).

Inputs and pins come from the availability check, [PR #698](https://github.com/Joshua-Asante/first-passage/pull/698) §7.
**Rule:** synthetic inputs only. The builder is public `lab/` code. It reads the private exports only at run time (after #616 freezes) and writes only to a gitignored private root. No real export is read, run or hashed by this build.
**Return boundary:** merged-ready code and tests with launcher evidence, or a precise blocker. No real-input run, no scoring or MC call, no prereg edit, and no step-3c′ mode-switching kernel work.

## §0 — Production reads (`main@716c876`)

| Surface | Finding |
|---|---|
| `lab/discovery/prop_survivor_scoring.py` `paired_blocks_from_daily` (:407), `score_candidate` (:652) | The consumer takes consecutive business-day arrays: a daily P&L and an `intraday_low` (≤ 0, finite, same length), blocked Monday-anchored on `pd.bdate_range("2020-01-06", …)`. The calendar is positional, so the builder must emit every weekday in its window, with zero rows on no-trade days. |
| `core/mc/simulation.py` (:325-345, :409-410) | `intraday_low` is the day's minimum-equity excursion from the day's opening equity: entries ≤ 0, unscaled. |
| `ops/c1_rail/book_policy.py` (:18-29, :169-200, :229-318) | Book quantities:<br>• Aegis is a fixed base of 8, protected `floor(8 × 0.40) = 3`.<br>• Striker is risk-scaled: S-P captures the protected size.<br>• Vanguard: base 1 or 2, protected `floor(b × 0.40) = 0`, so no entries.<br>• ORB: base 1; protected keeps the base and refuses adds (O-P). |
| [Track B scaling read](../../notes/2026-09-12-track-b-scaling-faithfulness-read.md) :100-110 | A-0 is the captured Aegis ladder at cap 8 (its quantities vary). The book's fixed-8 rule is verified against A-0 by timing invariance, so Aegis P&L is rescaled per contract. S-0, V-0 and O-N are faithful at the captured size; S-P and O-P are the protected captures. |
| `core/firm_rules.py` | `cost_per_side_usd` per tier (:135, :321, :378, :464). MFFU 16:10 ET auto-liquidation (:365-367). |
| `core/mc/ingest.py` `build_week_blocks` (:191) | Monday-anchored 5-day blocks. |
| Layering (`scripts/check_boundaries.py`) | `lab` may import `core`, never `ops`. |

## §0.5 — Clarifications resolved at freeze

1. **Book quantities enter as data, not as an import.** `lab` cannot import `book_policy`, so the builder takes a per-leg quantity spec as an argument:
   - Aegis: `{normal: 8, protected: 3}`, per-contract rescale.
   - Striker, ORB, Vanguard normal: `as_exported`.
   - Vanguard protected: `zero`.

   A parity test under `tests/`, which may import both layers, asserts the spec equals `book_policy.entry_quantities` for those legs. That keeps one source.
2. **Export timezone:** a required `export_tz` argument, with no default. Its value is a #616 freeze input, routed (§8). The builder also asserts at run time that no trade's exit falls after 16:45 ET on its session date; the venue-bound editions flatten earlier (campaign D11). A failure raises, and the run reads INSUFFICIENT.
3. **Session date:** the exit timestamp's date in America/New_York. Every leg is flat each day (venue-bound editions), so no position spans two sessions; an entry and exit on different NY dates raises. *Executor correction 2026-10-05:* "date" means the CME trade date, i.e. the NY time rolled at 18:00 ET. A calendar date would reject a legal Globex-evening entry such as 6J's. Exits in [16:45, 18:00) ET are late, and the MFFU flag covers [16:10, 18:00) ET.
4. **Window:** the latest first-trade session to the earliest last-trade session across the six inputs, computed at run time. Every weekday inside it is a row.
5. **`intraday_low` construction (conservative coincident sum):** for each day and mode, the low is minus the sum of `|Adverse excursion USD|` over every trade with that session date, all legs together, after the Aegis rescale. Per tier it also subtracts the day's full cost.
6. **Costs:**
   - `gross = Net PnL USD + Commission USD` per trade, after the Aegis rescale.
   - `sides = 2 × qty` per trade.
   - Tier net: `gross − sides × cost_per_side_usd[tier]`, read from `core/firm_rules.py`.
7. **I-24 flag:** `mffu_admissible = False` if any trade, in either mode, has its NY-time interval `(entry, exit]` containing 16:10 on that session date, or its exit after 16:10. The builder records the boolean only, plus the count of flagged days.
8. **Input identity:** each input path is passed with its expected SHA-256. A mismatch raises before any row is parsed.

## §1 — Goal

Add `lab/discovery/remc_series_builder.py` with:

- `build_series(...) -> SeriesBundle`, a pure function over parsed trade tables;
- a CLI (`--input LEG:MODE=PATH@SHA256` six times, `--quantity-spec JSON`, `--export-tz`, `--out DIR`).

The output per tier holds:
- the business-day index;
- `normal_pnl`, `normal_low`, `protected_pnl` and `protected_low`;
- the bundle-level `mffu_admissible` flag;
- a manifest JSON with input hashes, the window, the tz, the spec and the output hashes.

Inputs are parsed from TradingView's 17-column trade-list header (#698 §7), pairing each trade number's Entry and Exit rows.

## §4 — Hypothesis and falsifier

**H:** on synthetic exports with hand-computed answers, the builder reproduces exactly:
- per-tier daily gross, net and low;
- zero rows on no-trade weekdays;
- the Aegis rescale;
- Vanguard protected = 0;
- the MFFU flag.

The output feeds `paired_blocks_from_daily` without error.

**Falsified by** any test below failing.

## §5 — Constraints and forbidden moves

- Synthetic inputs only. No file under `E/`, `D/`, `core/data/tv_exports/` or any Pine or port is read, hashed or named in a test fixture.
- No `ops` import in `lab/`. No edit to `core/`, `ops/`, `prop_survivor_scoring.py`, the prereg or any existing test.
- No MC, no `score_candidate` call on real data, no metric printed from real data.
- Outputs go to a caller-given directory, and the CLI refuses a path that is tracked by git.

## §6 — Acceptance and return taxonomy

Tests in a new `tests/test_remc_series_builder.py`, each on synthetic CSVs written to `tmp_path`:

| Test | Asserts |
|---|---|
| `test_pairs_entry_exit_rows` | trade-number pairing; rejects unpaired rows |
| `test_gross_net_per_tier` | hand-computed gross and per-tier net for the four tiers |
| `test_intraday_low_coincident_sum` | low = −Σ\|AE\| − day cost; ≤ 0; finite |
| `test_zero_rows_and_window` | the weekday calendar inside the computed window, with zero rows |
| `test_aegis_per_contract_rescale` | a ladder of 1..8 rescaled to 8 (normal) and 3 (protected) |
| `test_vanguard_protected_zero` | the zero spec gives zero P&L and zero low |
| `test_mffu_flag` | an exit at 16:15 ET flags; an exit at 16:00 does not |
| `test_late_exit_raises` | an exit after 16:45 ET raises |
| `test_hash_mismatch_raises` | raises before parsing |
| `test_feeds_paired_blocks` | the output passes `paired_blocks_from_daily` |
| `test_cli_refuses_tracked_out` | the CLI refuses a git-tracked output path |

Plus `tests/test_remc_series_quantity_parity.py::test_spec_matches_book_policy` (§0.5 item 1).

Evidence: `.\fp.ps1 python -m pytest` on both files, plus `scripts/check_boundaries.py`, cited by `record.json`.

Return labels:
- **DONE** / **DONE_WITH_CONCERNS** (with disclosures);
- **NEEDS_CONTEXT** (anchor drift, a header unlike #698's, or an owner conflict);
- **BLOCKED** (with the exact obstruction).

```yaml authority
seat: worker
parent: docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push, pr.open]
constraints:
  - no_main_write
  - no_merge
  - synthetic_inputs_only
  - no_private_source_read
  - no_core_or_ops_edit
  - no_existing_test_edit
  - no_prereg_or_owner_record_edit
  - no_lab_ops_import
  - no_mc_or_scoring_run
acceptance:
  - tests/test_remc_series_builder.py
  - tests/test_remc_series_quantity_parity.py::test_spec_matches_book_policy
```

## §7 — Return

**DONE_WITH_CONCERNS (2026-10-05).** Built through `glm_agent` (GLM hit its iteration cap). The coordinator-side worker reviewed the full diff and made one correction: the CME trade date (§0.5 item 3).

**Files (new only):**
- `lab/discovery/remc_series_builder.py`
- `tests/test_remc_series_builder.py`: the 11 §6 tests plus `test_cme_trade_date_rollover`
- `tests/test_remc_series_quantity_parity.py`

**Evidence:**
- `.p.ps1 python -m pytest` over the two new files plus `tests/test_prop_survivor_intraday_channel.py`: 19 passed, launcher record `completed`, exit 0.
- `check_boundaries` OK; the §10 grep hooks are clean.
- Synthetic inputs only. No real export was read.

**Concerns:**
1. `export_tz` is still a #616 freeze input (§8).
2. The parser fails closed on any timestamp other than `YYYY-MM-DD HH:MM`. A real export in another format reads NEEDS_CONTEXT at run time, not a silent misparse.
3. `manifest.json` stores the daily gross, sides and adverse-excursion arrays. It is written only to the gitignored private root.

## §8 — Routed, not done here

- **`export_tz`:** the TradingView trade-list timezone is not established in a public owner (the identity ledger :154 leaves CSV timezone semantics open). #616 needs its value as a freeze input before the run; coordinator (4) routes it.
- **Capacity and takeover** between legs are not modeled, per the O-4 named risk.
- **Step 3c′ (mode-switching kernel) and step 3e (reference reassembly)** have their own cards.

## §10 — Audit hooks

```bash
c=docs/briefs/handoffs/2026-10-05-four-firm-remc-series-builder-card.md
# Boundary held: no ops import in the builder (absence exits 0).
! grep -nE '^\s*(from|import)\s+(ops|c1_rail|c1_signal_daemon)' lab/discovery/remc_series_builder.py
# No private input in tests (absence exits 0).
! grep -nE 'private_overrides|Downloads|tv_exports' tests/test_remc_series_builder.py
# Acceptance suite.
python -I scripts/fp.py python -m pytest -q tests/test_remc_series_builder.py tests/test_remc_series_quantity_parity.py
```
