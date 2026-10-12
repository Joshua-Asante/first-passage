# Q-SFCLEAR-2 run path E: chronology, scoring composition and publication (worker build card)

**Type:** cc_handoff (worker build card)

**Status:** **DRAFT, not frozen, not dispatchable.** Drafted 2026-10-12 for the Deployment Coordinator. Freezing is the coordinator's act, and only after Joshua's rulings ([decision packet](../../notes/2026-10-12-q-sfclear-2-run-path-decision-packet.md) items 1, 5, 7).

**Base:** `origin/main` `92bfca7` for every `file:line`; the build cuts from a base containing #752's `lab/analysis/c1/sfclear_2026-10/` folder, B and C (§0(a)).

**Parent scope:** [run-path scope note](../../notes/2026-10-12-q-sfclear-2-run-path-code-scope.md) §1 item 5, §2 packet E.

**Study (governs):** the FROZEN Q-SFCLEAR-2 [pre-registration at F `83867f0`][prereg] §4 items 1–9 (series, fees, calendar and windows, drawdown, growth, margin, gates, Striker trip = NOT CLEARED, residual reports), §3 B2 and G1-D/G3-D, §5 (no run without a run record; no outputs under the repo), §6 (verdict order FREEZE INVALID → VOID → RESOLVED / NOT CLEARED; nonce rule; public disclosure), §7 run record, §10 hook 4.

**Two scopes, kept apart:**
- **The build** (this card's authority block) writes code and **synthetic-root tests only**: temporary directories and temporary git repositories. It never writes a run record, a `PRIVATE_EVIDENCE.sha256` row or any file under the real private root.
- **The coordinator-run publication step** (§13) is the only step granted the exact §7 publication paths. It is not part of the build.

**Authority (build):** G-1, G-2, G-3 (§11).

**Executor (build, proposed):** Codex local, single writer of `codex/sfclear2-e-run-record`, in a fresh worktree. Not GLM.

**Coordinator:** the Deployment Coordinator. Claude owns private execution and evidence custody.

```yaml authority
seat: worker
parent: docs/notes/2026-10-12-q-sfclear-2-run-path-code-scope.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push]
constraints:
  - not_dispatchable_until_section_11_gates_recorded
  - offline_synthetic_only
  - synthetic_root_tests_only
  - no_real_data_run
  - no_private_read
  - no_run_record_or_private_evidence_write
  - no_edit_to_frozen_prereg_schedule_roll_list_or_generators
  - no_new_selection_grid
  - no_copy_of_scorer_or_margin_code
  - card_section2_files_only
  - no_core_edit
  - no_ops_edit
  - no_dd_protection_or_frozen_constant_edit
  - no_lab_ops_import
  - no_existing_test_or_fixture_edit
  - no_pine_or_port_access
  - no_main_write
  - no_merge
  - no_pr_open
  - no_glm
  - single_writer
  - stop_at_coordinator_return
acceptance:
  - tests/lab/test_sfclear_run_record.py
  - tests/lab/test_sfclear_score_r1.py
  - tests/lab/test_sfgrowth_acceptance.py
  - tests/lab/test_sfgrowth_margin.py
  - tests/lab/test_sfclear_tradovate_fees.py
  - tests/lab/test_sfclear2_g1g3_calculator.py
  - tests/lab/test_sfclear2_roll_dates.py
```

The first two files are new; the rest exist at the §0(a) base (the third-to-last from C, the last two from #752) and stay green with no edit.

## 0. Phase 0: premise, Rule-0 reads and findings returned before code

- **(a) Base.** The cut contains #752's folder byte-equal to F for the pre-registration, `schedule/` and `build_historical_schedule.py` (`git diff --quiet 83867f0 HEAD -- <those paths>`), plus B and C. Missing any is a **stop**.
- **(b) Reused primitives.** `lab/discovery/sfgrowth_acceptance.py:53` (`strict_object`), `:74` (`resolve_manifest`), `:192` (`daily_series`), `:218` (`common_calendar`), `:236` (`bootstrap_indices`: seeds 42, 123, 2026; `starts` (10,000, 13); 20-day non-circular blocks; 252), `:270` (`_halted`, exact), `:305` (`score`), `:394` (`validate_evidence`); `lab/research_utils/sfgrowth_margin.py:115` (`check_concurrent_margin`).
- **(c) Window trap.** `sfgrowth_acceptance.py:229` `split_calendar` cuts at two thirds. Pre-registration §4 item 3 defines H1 = weekdays 1…⌊W/2⌋ and H2 = the rest. E must not call `split_calendar`; confirm and report.
- **(d) Hook 4.** Pre-registration §10 hook 4 at F: the run record's keys, ancestry from F, the frozen-file set and the `PRIVATE_EVIDENCE.sha256` row form `<sha256>  <name>`.
- **(e) Inputs.** B's `sfclear_route_output/v1` and C's `sfclear_tradovate_fees/v1` schemas as merged.

## 0.5. Routing and clarifying questions

- **(A) Process boundary.** The wrapper runs replay (ops, B) and scoring (lab) as separate processes via the launcher and `sys.executable`, exchanging only serialized artifacts under the private root. No `lab↔ops` import.
- **(B) Private root.** Passed explicitly; refused if inside the repository or any git work tree.
- **(C) Verdict cells.** G1 and G3 are read from the freeze record (by the hash pinned at F). G1-D and G3-D are computed after the run by the bound calculator (sha256 `2333844d…97bf`, private) from the run's `E_p` path only. The build tests use a synthetic stub calculator with a test hash.
- **(D) `D_t` (§4 item 1).** `d_t = Σg − c·fees_t − D_t` and `l_t = −Σ|MAE| − c·fees_t − D_t`. `daily_series` (`sfgrowth_acceptance.py:192`) takes no `D_t` argument, so `score_r1.py` adds a wrapper: it subtracts each day's `D_t` from the `d` and `l` channels of `daily_series`'s result, once per day for the account (not per leg), and never touches `h`. `sfgrowth_acceptance.py` is not edited. `D_t` has no input file: D7 fixes it at 0 on every day. If open fact 6 (pre-registration §11) finds that Tradovate debits the account, a nonzero `D_t` needs its own dated operator ruling before any run, and the wrapper takes it only with that ruling's reference. A run that applies a nonzero `D_t` without that ruling is a defect and refuses.
- **(E) Calendar (§4 item 3).** One weekday calendar, from the latest first session date to the earliest last session date across **all four legs' admitted panels** (book `data_window` 2022-09-01..2026-09-02). It is fixed whatever a leg's OFF status: ORB, OFF at R1, still contributes its admitted panel's span, and a leg with no trades still counts. DENIED schedule rows are zero days. FULL = all W weekdays; H1 = weekdays 1…⌊W/2⌋; H2 = the rest. VOID if any window < 20 weekdays.
- **(F) B2 (§3).** `u` = peak concurrent intraday margin from `check_concurrent_margin` on route output × the dated intraday margin per contract, ÷ `E_0` (the private `E_0` file, by hash). `g = 0.15 × G3`, with G3 in rope units read from the freeze record. `f` = one month of fixed costs Tradovate debits from the trading account ÷ `E_0` (the pre-screen's debited-case value if open fact 6 is still open at the run). `u_max = (0.85 − g − f) / 1.5`; headroom = `(u_max − u) × E_0`, compared privately in dollars against one 6J contract's dated intraday margin: PASS if headroom ≥ that margin, MARGINAL if 0 ≤ headroom < it, FAIL if headroom < 0. Only PASS clears. The margin snapshot is used only if its hash equals the freeze record's; otherwise VOID.
- **(G) No ranking.** One fixed R1 verdict. `nominal_grid`, `rank` and `verdict` (`sfgrowth_acceptance.py:339`–`:357`) are not called.

## 1. Goal

A scoring run is unusable unless its frozen inputs, FG result and clean start revision are bound, and its private output manifest is paired with the public record. The composition produces the fixed §4 cells and the §6 verdict mechanically.

**Not asked:** the real run, any private record, any publication (§13).

## 2. Scope

### 2.1 The change

- `run_record.py`: clean 40-hex HEAD recorded before work (empty `git status --porcelain`); aware UTC start; F ancestry and frozen files unchanged against F; FG PASS reference required before replay starts; private root outside the repo; nonce file of at least 128 bits listed in `SHA256SUMS`; hash of exact completed bytes; a publication candidate of exactly `run_head`, `started_utc`, `private_sha256sums_sha256` plus the matching `PRIVATE_EVIDENCE.sha256` row, staged together; refuse overwrite and name collision; an interrupted publication leaves no usable output and is recoverable.
- `score_r1.py`: §4 composition. Per leg, `g = Net PnL + Commission` once; `daily_series` per instrument with C's rate; `D_t` subtracted per §0.5 (D); the calendar per §0.5 (E); B2 per §0.5 (F); DENIED rows zero days; FULL, H1, H2 by §4 item 3; VOID if any window < 20 weekdays; `bootstrap_indices` and `score` for the 18 drawdown cells; pooled median of 30,000 terminals for the 3 growth cells; `check_concurrent_margin` for B2 (PASS / MARGINAL / FAIL); G1, G3, G1-D, G3-D; G0/G4 breach or missing MAE/MFE is VOID; a Striker total-DD trip is NOT CLEARED; residual reports and sensitivities written privately, never verdict inputs.

### 2.2 Files

| File | Bound | Edit |
|---|---|---|
| `lab/analysis/c1/sfclear_2026-10/run_record.py` | not in either inventory; audit imports | new |
| `lab/analysis/c1/sfclear_2026-10/score_r1.py` | not in either inventory; audit imports | new |
| `tests/lab/test_sfclear_run_record.py` | — | new |
| `tests/lab/test_sfclear_score_r1.py` | — | new |

**Forbidden files:** the pre-registration, brief, `schedule/`, `build_historical_schedule.py`, `build_roll_dates.py`, the calculator; `lab/analysis/c1/sfclear_2026-10/run_records/`; `docs/evidence/PRIVATE_EVIDENCE.sha256`; `STATE.md`; `sfgrowth_acceptance.py` and `sfgrowth_margin.py` (reused, not edited or copied); every `ops/` and `core/` file; any existing test; Pine, ports, private files.

## 3. Method

1. Phase 0; post findings.
2. Fresh worktree; cut `codex/sfclear2-e-run-record`.
3. §4 rows red; build; green; acceptance list; `fp test`; `fp check`; cite records.
4. Stage only §2.2; push; return the public-safe publication candidate format.

## 4. Acceptance checks (falsifier-first)

**Hypothesis:** `N/A`. This executes scope note §2 packet E.

| Row | Test (synthetic roots, temporary git repos) | Fails if |
|---|---|---|
| E1 | Dirty HEAD at start refuses | Run starts dirty |
| E2 | Source changed during the run: record unusable | Change undetected |
| E3 | HEAD not descended from F, or a frozen file changed against F | Ancestry not enforced |
| E4 | FG reference missing or FAIL: replay never starts | Scoring without FG |
| E5 | Private root inside the repo or a work tree refuses | In-repo outputs |
| E6 | Missing nonce, missing output, or manifest mismatch refuses | Unbound outputs |
| E7 | Public record keys exactly the three; extra key or non-40-hex `run_head` or naive `started_utc` refuses | Leaky record |
| E8 | Half-publication (record without row, or row without record) is detected and recovered without advertising usable output; overwrite and collision refuse | Unpaired publication |
| E9 | Windows: on a synthetic calendar of W weekdays, H1 has ⌊W/2⌋; W < 40 makes a half < 20 and VOID | Two-thirds split used |
| E10 | 18 drawdown cells (3 seeds × 2 c × 3 windows) and 3 growth cells (c = 1.5) computed; each binding cell's failure gives NOT CLEARED | A cell missing or not binding |
| E11 | Synthetic Striker total-DD trip gives NOT CLEARED even with every cell passing | Trip ignored |
| E12 | Verdict order: a FREEZE INVALID input outranks VOID; VOID outranks NOT CLEARED | Order wrong |
| E13 | B2 bands: synthetic headroom ≥ one 6J margin PASS; between 0 and that MARGINAL (not clearing); below 0 FAIL; exact-boundary cases at headroom = 0 and = one margin | B2 misclassified |
| E13a | B2 composition on synthetic inputs: `u` = peak concurrent margin ÷ `E_0`; the factor is exactly 1.5; `g = 0.15 × G3` with G3 read from a synthetic freeze record (not recomputed); `f` = monthly debited fixed costs ÷ `E_0`; `u_max = (0.85 − g − f)/1.5`; headroom = `(u_max − u) × E_0`. Each term changed alone moves headroom as the formula predicts | A term missing, recomputed or mis-scaled |
| E13b | Margin snapshot whose hash differs from the freeze record's: VOID before scoring | Unfrozen margins used |
| E16 | `D_t`: by default every `D_t` is 0 and outputs equal `daily_series`'s; a nonzero `D_t` without a ruling reference refuses; with a synthetic ruling reference, `d` and `l` fall by `D_t` once per account day and `h` is unchanged | `D_t` dropped, doubled per leg, or applied to `h` |
| E17 | Calendar span: four synthetic panels with different endpoints and one leg OFF with no trades; the span is latest first to earliest last across all four admitted panels | Span taken from legs with output only |
| E14 | Residual and sensitivity outputs never change the verdict | Residual promoted |
| E15 | No log line or public field carries a synthetic `E_0`, tuple value, cell value or private path beyond the row form | Leak |

**Named mutants:** M-E1 skip the clean-HEAD check (E1); M-E2 call `split_calendar` (E9); M-E3 skip FG (E4); M-E4 write the record without the row (E8); M-E5 drop the trip rule (E11); M-E6 treat MARGINAL as PASS (E13); M-E7 add an `e0` key to the record (E7, E15); M-E8 build the calendar span from legs with output only (E17); M-E9 use a factor other than 1.5, or recompute G3 instead of reading it (E13a); M-E10 accept a mismatched margin snapshot (E13b); M-E11 apply `D_t` per leg (E16); M-E12 apply a nonzero `D_t` with no operator-ruling reference (E16).

**Revert trigger:** any listed existing suite changes outcome.

## 5. Forbidden

- No real-data run, private read, run record or `PRIVATE_EVIDENCE.sha256` write in the build.
- No edit to the frozen pre-registration, schedule, roll list, generators or calculator.
- No selection grid, ranking or rung walk; no copied scorer or margin code.
- No `lab↔ops` import; no edit to frozen constants or `dd_protection`.
- GLM, a push to `main`, a merge, or opening a PR.

## 6. Return (status taxonomy)

| Status | When |
|---|---|
| `DONE` | Rows red then green; mutants killed; suites and `fp check` completed exit 0; footprint equals §2.2 |
| `DONE_WITH_CONCERNS` | As DONE, with an observation |
| `NEEDS_CONTEXT` | §0(c) or §0(e) contradicted |
| `BLOCKED — context-problem` / `capability-problem` / `scope-problem` / `plan-itself-wrong` | As named |

**Gate verdict (coordinator, at review):** **RESOLVED** when `DONE` and both §7 passes reproduce it; **FALSIFIED** when a row cannot be made red or a mutant survives; **AMBIGUOUS** on `DONE_WITH_CONCERNS`.

## 7. Stop conditions and parent review

**Stop and return:** §0(a) base incomplete; any need to edit a frozen file or reused scorer; hook 4 at F disagrees with the record format.

**Parent review:** Pass 1, footprint, no publication path written, record keys; Pass 2, re-run rows and mutants from a clean worktree, and run hook 4 against a synthetic record in a temporary clone.

## 8. Out of scope and decision unlocked

**Out of scope:** §13; the closure; FG evidence (D §13).

**Unlocks:** the coordinator-run scoring and publication step.

## 9. Sequencing and file collisions

- After B, C and #752's merge. E writes no `ops/` file, so it holds no slot in the `production_source.py` writer (B) or the owner queue.
- Publication paths collide with #752 and calculator evidence publication; Claude is their one publication owner (§13).

## 10. Audit hooks (runnable)

```bash
python -I scripts/check_brief.py docs/briefs/handoffs/2026-10-12-q-sfclear-2-run-path-e-run-record-card-DRAFT.md --type cc_handoff
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-12-q-sfclear-2-run-path-e-run-record-card-DRAFT.md
git diff --name-only <cut>..HEAD   # expect exactly §2.2; no run_records/ or PRIVATE_EVIDENCE path
grep -n "split_calendar" lab/analysis/c1/sfclear_2026-10/score_r1.py   # expect no output
python -I scripts/fp.py python -m pytest <the authority-block acceptance list>
python -I scripts/fp.py check
```

## 11. Gates (the build is NOT DISPATCHABLE until all three hold)

- **G-1.** No bound-code admission if the import audit keeps both modules outside the trust domain; otherwise Joshua's admission (item 1). **Not recorded.**
- **G-2. Coordinator freeze.** **Not done.**
- **G-3. Dispatch.** **Not done.**

## 12. Open decisions (coordinator at freeze; Joshua where marked)

- **D-1.** Confirm the route-output and fee schemas consumed (B, C returns).
- **D-2 (Joshua, item 7).** Under the frozen reading (b), E scores the series as it stands and adds no latch rule. If Joshua rules (a), E adds one row mapping a latch record to NOT CLEARED, disclosed as a post-freeze addition. Under (c), E waits for the new pre-registration. The card is not frozen until item 7 is settled.

## 13. Coordinator-run publication step (not in the build)

The only step granted the exact §7 paths, and only for a real run after FG PASS, under a separate dispatch record:
- `lab/analysis/c1/sfclear_2026-10/run_records/<UTC>.json` with exactly `run_head`, `started_utc`, `private_sha256sums_sha256`;
- one added row in `docs/evidence/PRIVATE_EVIDENCE.sha256`, `<sha256>  t00-step3-console/sfclear2-run-<UTC>/SHA256SUMS`;
- both in one commit descending from F, then §10 hook 4 prints nothing.

Private outputs stay under `C:\Users\joshu\t00-step3-console\sfclear2-run-<UTC>\`. Committing the record is separate from the run's `run_head`. The closure is a separate act.

## Pre-mortem

- **Loop cost.** One targeted run, one `fp test`, one `fp check`.
- **Likely failure.** E9: reusing the scorer's calendar helpers pulls in the two-thirds split.
- **What would make this moot:** none; the study cannot score without a run record.
- **Evidence binding:** records at the returned head only.

[prereg]: https://github.com/Joshua-Asante/first-passage/blob/83867f0d362931c2a516a62b990bb1c209372527/docs/briefs/pre-registration/Q-SFCLEAR-2-verdict-preregistration.md
