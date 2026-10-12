# Q-SFCLEAR-2: G1/G3 calculator and G4 roll-date generator, v3 (worker build card)

**Type:** cc_handoff (worker build card)

**Status:** **FROZEN 2026-10-12** at the commit that adds this file. The Deployment Coordinator authored and froze it under the committed-handoff rule. It is dispatchable on the coordinator's dispatch record (§11).

**Supersedes:** [v2](2026-10-12-q-sfclear-2-calculator-and-roll-dates-card-v2.md), whose worker stopped under §7. One capture row failed: MGCZ27 last trade, because Saturday 1 Jan 2028's observed Friday shift does not apply at CME. v3 changes only the business-day line; the coordinator re-ran the 36-vector check with it and got 0 mismatches. v2 superseded [v1](2026-10-12-q-sfclear-2-calculator-and-roll-dates-card.md). The v1 worker stopped at Phase 0 under §7 (BLOCKED, no code) for three reasons:
- three capture rows failed under v1's business-day rule;
- Vanguard's distance-cap formula lives in its port, which v1 barred;
- v1 named the wrong panel paths.

**Base:** branch `claude/sfgrowth-phase0-sizing-classification` (PR #752) at the commit that adds this card. Every `file:line` below is at that commit.

**Parent:** [Q-SFCLEAR-2 pre-registration](../pre-registration/Q-SFCLEAR-2-verdict-preregistration.md) (DRAFT): §3 (the G1/G3 bound, held-bar set, calculator line and G4), §11 items 5 and 15, and §12 steps 3–4.

**Rulings consumed:** §12 step 1 (a)–(k): Joshua, 2026-10-12, "(d)-1, (f) binding, (g) keep, (j) accept, (k)-1" and "(a)(b)(c)(h) yes". Also "rule-generated roll dates OK" and "business days: federal + Good Friday + D19" and "Saturday New Year's not observed" (Joshua, 2026-10-12, directly to the Deployment Coordinator).

**Executor:** a Claude worker, the single writer of `claude/sfclear2-calculator-v3`. Not GLM, not Codex: the worker reads private method text and the vendor panels in place.

**Coordinator:** the Deployment Coordinator. It owns review, integration into #752, binding the calculator's sha256 on the §3 line, and every private record.

```yaml authority
seat: worker
parent: docs/briefs/pre-registration/Q-SFCLEAR-2-verdict-preregistration.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push]
constraints:
  - no_run_of_the_calculator_on_real_panels_or_the_real_tuple
  - no_g1_g3_value_computed_printed_or_written
  - no_read_of_e0_private_txt_contents
  - no_read_of_one_contract_risk_json_prescreen_calc_json_or_vanguard_upper_json
  - no_read_of_t00_replay_screen_or_mc_output
  - no_strategy_parameter_value_in_committed_files
  - no_pine_access
  - vanguard_port_read_in_place_only_formula_no_value_recorded
  - calculator_private_route_required
  - no_import_of_one_contract_risk_py
  - no_edit_outside_section2_files
  - no_main_write
  - no_merge
  - no_pr_open
  - no_glm
  - single_writer
  - stop_at_coordinator_return
acceptance:
  - tests/lab/test_sfclear2_roll_dates.py
  - tests/lab/test_sfclear2_g1g3_calculator.py
```

## 0. Phase 0: premise, Rule-0 reads and findings returned before code

Read the sources below, then report your findings. If anything contradicts this card, **stop** (§7).

**Repo sources:**
- The Q-SFCLEAR-2 pre-registration (path above): §3, §4 item 7, §5, §6, §10 hook 4 and §12.
- `lab/analysis/c1/sfclear_2026-10/build_historical_schedule.py` and its output, the bound schedule (sha256 `ab44fada0c059c0d286798239a87c82331d8500ef075bf4cb1180ed552d5d473`). Copy its `--check` pattern.
- `ops/calendars/cme_holiday_calendar_2022_2026.json` (D19) and `ops/calendars/README.md`. These define business days.

**Private files, read in place.** Read text and code only, and record no values.
- `C:\Users\joshu\t00-step3-console\personal-prescreen-20261011\one_contract_risk_FREEZE.md`: the frozen method, including its window, its item 5 filters and its item 8 exclusions.
- `one_contract_risk.py` in the same folder: the T1/T3 implementation (code only).
- `C:\Users\joshu\t00-step3-console\sfclear-facts-20261011T174256Z\vanguard_upper.py`: the calculator seed (code only). Its held-bar window differs from H_ℓ (§3).
- `R1_TUPLE.json`: key structure only.
- Vanguard's accepted runtime port, read in place in the primary checkout (`C:\Users\joshu\multi_firm_operations`; path from `core/strategies/BOOK_SOURCES.sha256`), under AGENTS.md's private read surface. Read the distance-cap formula only. Record no value, and never copy, quote or commit its body.

**Public data:**
- The CME capture: `C:\Users\joshu\t00-step3-console\sfclear2-g4-sources-20261012T153100Z\cme_calendar_capture.tsv` (sha256 `1afbcd9fe42b5237466837ed95e67a477ebb4a3b47812e8fc3b7fdc9e287efa6`).
- The 6J, MYM and MGC panels the frozen method names, : `C:\Users\joshu\multi_firm_operations\core\data\bar_data\{6J,MGC,MYM}_M15.csv`. Read headers and structure only; compute no statistic.
- The roll-seam rule: `docs/spec/2026-09-27-cme-execution-feed-equivalence-test-DRAFT.md` OPEN-11 (§16.2, §16.4) and OPEN-3.

**Return these findings:**
- (i) The frozen method's T1/T3 terms per leg, in words, with no values.
- (ii) Whether T1/T3, H_ℓ's item-5 filters and n_ℓ can all be read from private inputs at run time, so that no strategy value enters committed code.
- (iii) How each panel's roll seams are identified. Cite the repo's TradingView `1!` convention source. Say so if seams can only be found by a price heuristic.
- (iv) The test convention under `tests/lab/`.
- (v) Whether the `bar_data` panels are the captures OPEN-11's switch evidence was checked against (by hash or provenance, without reading prices). If they are not, that is a disclosed residual, not a stop.

## 0.5. Routing and clarifying questions

This is a private-reading, offline task for a Claude worker.

**The calculator is private (required).** Its parameters come from the port and the effective inputs at run time.
- Place it under `C:\Users\joshu\t00-step3-console\sfclear2-calc-<UTC>\` with a nonce file and a `SHA256SUMS`.
- Keep its tests public and synthetic. They locate the calculator through an environment variable (`SFCLEAR2_CALCULATOR`) and skip when it is absent, as vendor-dependent tests do.
- Report it. The coordinator adds the `PRIVATE_EVIDENCE.sha256` row.

Roll seams follow OPEN-11 by rule. Use no price heuristic (for example `lab/analysis/legacy/futures_conversion_2026-07-01/roll_mask.py`). Reimplement the frozen method rather than importing `one_contract_risk.py`: it has no main guard and reads E_0 on import.

## 1. Goal

Build the two tools the Q-SFCLEAR-2 freeze needs (§11 items 5 and 15). Neither tool computes any G1/G3 value or verdict before ratification ((d)-1).

1. **Roll-date generator.** Generates the G4 list by rule: the 6J and MGC contract dates, plus the panels' roll seams.
2. **G1/G3 calculator.** Computes G1, G3, G1-D and G3-D exactly as §3 defines them, at p95 and at the window maximum.

## 2. Scope

Create only these files:
- `lab/analysis/c1/sfclear_2026-10/schedule/build_roll_dates.py`, with `--check`. The check regenerates the output byte-identically and prints its sha256, then `MATCH`.
- `lab/analysis/c1/sfclear_2026-10/schedule/roll_dates_6J_MGC_2022-09-01_2026-09-02.json`.
- `lab/analysis/c1/sfclear_2026-10/schedule/sources/cme_calendar_capture_20261012.tsv`: a byte copy of the capture, which holds public CME calendar facts.
- the private calculator under `C:\Users\joshu\t00-step3-console\sfclear2-calc-<UTC>\` (§0.5).
- `tests/lab/test_sfclear2_roll_dates.py`.
- `tests/lab/test_sfclear2_g1g3_calculator.py`.

## 3. Method

**Roll dates** (rules ruled 2026-10-12). A business day is a weekday that is none of these:
- a US federal holiday, generated by rule: the 5 U.S.C. 6103 dates with observed-day shifts (Saturday to Friday, Sunday to Monday), including Juneteenth from 2021. **Exception:** a New Year's Day that falls on a Saturday is not observed on the Friday before;
- Good Friday, computed from Easter;
- a D19 FULL_CLOSURE day for the product's group.

This definition applies to contract dates and seams only. The G0 session schedule is unchanged.
- **MGC:** first notice is the last business day of the month before the contract month. Last trade is the third-last business day of the contract month.
- **6J:** there is no first notice. Last trade is the second business day before the third Wednesday of the contract month.
- **Contracts covered:** every listed month whose G4 window intersects 2022-09-01..2026-09-02. For MGC that is the even-month cycle the capture shows; for 6J, the quarterly and serial months.
- **G4 window:** starts at the start of the business day before min(first notice, last trade).
- **Seams (OPEN-11, using this business-day definition):** each switch happens at the 18:00 ET open.
  - 6J: one business day before last trade, quarterly contracts only.
  - MGC: one business day before first notice, on its listed cycle.
  - MYM: three business days before its last trading day. Generate that last trading day by its CME rule, and cite the rule's source.
- **Test vectors:** every row in the capture is a test vector, so extend the generator to the capture's horizon. That means each MGC first notice and last trade, and each 6J last trade. A mismatch fails the build. Never adjust a rule to fit a row; stop instead (§7).
- **Output metadata:** the output names each source's sha256 (D19 and the capture).

**Calculator** (pre-registration §3 terms, verbatim):
- **Inputs:** each given by path plus expected sha256, refusing on mismatch. They are the bound schedule, the panels, R1_TUPLE.json, the frozen-method parameter source (private), the E_0 file, and the E_p multiple m\* (default 1).
- **G1, per ON leg:** T1 + 2·gap. Vanguard's T1 uses its distance cap at E_p = m\* × paper capital.
- **G3:** Σ over ON legs of [T3 + n·2·gap], where:
  - Striker uses its total-risk bound, not multiplied by n;
  - Vanguard uses its cap at n contracts;
  - Aegis uses n × its one-contract risk.
- **gap:** |open − previous close| × point value, over the held-bar set H_ℓ.
- **H_ℓ (exactly as §3):** PERMITTED rows only. It runs from the bar after the first entry-eligible bar through the 15:55 ET flatten-start bar, and keeps roll seams.
- **Statistics:** report p95 and the window maximum for each term. Use one documented percentile definition, the same one `one_contract_risk.py` uses.
- **Units:** results in rope units (0.15·E_0).
- **Output:** a JSON file under a private output root, carrying a nonce of at least 128 bits. Stdout carries only that file's sha256.
- **Arguments:** `--self-test` runs the synthetic suite. No default path points at real data.

## 4. Acceptance checks (falsifier-first)

**H:** if the ruled rules and the §3 terms are implemented faithfully, then every capture row regenerates and every mutant below is killed. **Falsifier:** any capture row mismatch, or any surviving mutant, rejects the build (reject-if).

**Roll dates:**
- Every capture row regenerates exactly.
- One mutated rule fails a test: the MGC first-notice offset, and the 6J third-Wednesday offset.
- `--check` prints `MATCH`, and the output names its source hashes.
- A D19 holiday, a federal holiday and Good Friday each move the computed date.
- All 36 capture vectors pass. Named tests cover the three rows that failed under v1 (MGCM27 first notice; J1F27 and J1G27 last trade) and the one that failed under v2 (MGCZ27 last trade).

**Calculator** (synthetic panels and tuple only):
- Hand-computed G1, G3, G1-D and G3-D on a constructed two-week panel, exact to 1e-9.
- Each of these mutants is caught:
  - gap counted once instead of twice;
  - Striker's bound multiplied by n;
  - H_ℓ including a DENIED row;
  - H_ℓ including a bar after 15:55;
  - m\* ignored.
- A sha256 mismatch on any input refuses with a non-zero exit.
- A test asserts that stdout never contains an input value.

Each acceptance file must fail before its implementation exists and pass after. Record both runs through the launcher.

## 5. Forbidden

Everything in the authority block. In particular:
- Running the calculator on the real panels or tuple, or computing any G1/G3 statistic on real data. That would breach (d)-1 and the pre-registration's §5.
- Printing or committing E_0, rope, n_ℓ, any leg parameter, or any part of the port body.
- Editing the pre-registration, the schedule, its generator or any calendar file.

## 6. Return (status taxonomy)

Return one status: `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED` or `NEEDS_CONTEXT`. The coordinator maps them: `DONE` with every §4 check passing is RESOLVED; a falsifier hit is FALSIFIED; anything else is AMBIGUOUS. Include:
- the Phase 0 findings;
- `git diff --stat`;
- the pushed head SHA;
- the private calculator folder's `SHA256SUMS` sha256 and of the roll-date JSON;
- each acceptance command, with exact counts and its fp `record.json` path, status and exit code;
- any deviation from this card.

## 7. Stop conditions and parent review

Stop and return if any of these happens:
- Phase 0 contradicts this card.
- A capture row cannot be reproduced by the ruled rules.
- Roll seams need a price heuristic.
- A strategy value would have to be committed and the private route also fails.
- Any step would require computing on real data.

After the return, the coordinator reviews the diff, integrates it into #752, and writes the calculator sha256 on the §3 line before ratification step 3.

## 8. Out of scope and decision unlocked

**Out of scope:**
- Running either tool for the freeze record. That is §12 step 4, after Joshua's ratify words.
- The personal replay path, P0 and FG.

**Unlocks:** §11 items 5 and 15, and so ratification step 3.

## 9. Sequencing and file collisions

This card creates new files only. No other writer touches `lab/analysis/c1/sfclear_2026-10/` while it runs.

## 10. Audit hooks (runnable)

```bash
python -I scripts/fp.py python lab/analysis/c1/sfclear_2026-10/schedule/build_roll_dates.py --check   # expect <sha256> MATCH
python -I scripts/fp.py python -m pytest tests/lab/test_sfclear2_roll_dates.py tests/lab/test_sfclear2_g1g3_calculator.py -q   # expect all passed
git diff --stat origin/claude/sfgrowth-phase0-sizing-classification...HEAD   # expect only §2 files
```

## 11. Gates

- **G-1 (freeze):** the commit that adds this file.
- **G-2 (dispatch):** the coordinator's dispatch record. The authorizing words are Joshua's "rule-generated roll dates OK" and his (a)–(k) rulings.

## 12. Open decisions (coordinator at freeze)

None. The private-calculator fallback in §0.5 is pre-authorized.

## Pre-mortem

- **The capture covers only live contracts.** A rule that holds for 2026–2028 could have been different for older contracts. Disclose any CME rule-change notice found during Phase 0.
- **TradingView's `1!` roll can differ from the live rail's roll.** Report the difference; the replay's G4 check depends on it.
- **Holidays the vectors don't test:** no capture vector falls on Columbus Day, Veterans Day or Juneteenth, so their business-day status is a disclosed residual. In the window, Juneteenth moves only the June 2023 6J last trade.
