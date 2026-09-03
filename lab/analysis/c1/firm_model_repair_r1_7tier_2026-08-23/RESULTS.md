**Theme:** c1
# R1 — 7-tier intraday-honest re-run (Bulenox / BluSky, W1 pattern extended) — RESULTS

> ⚠ **Reader-intercept 2026-09-03 — the gate scored against below was raised.** Every PASS/FAIL
> label here is against v1's **3.0%** Part A ceiling; the live ceiling is **5.0%** since 2026-08-26
> ([`prereg v2`](../../../../docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md) §3). **No verdict in this file flips:** the 1.00× honest-clock
> figures (Bulenox 26.77%, BluSky 32.26%) fail at either ceiling, and the 0.50× figures (0.59%)
> pass at either. The measured numbers are unaffected. Recorded because CLAUDE.md routes readers
> here as the honest-clock RESULTS of record for these two tiers, so "3.0%" gets quoted onward.
> Frozen body unedited.

**Status:** ACTIVE — W1 pattern extended to all 7 Bulenox/BluSky `dd_type="trailing"` tiers (Q-FIRMEOD-1 successor); all 7 flip CLOCK on direct `simulate_path` diff; no verdict flips on the 2 tiers with a published figure on the live book but 1.00x deepens ~7.6x (Bulenox 3.51%→26.77%, BluSky 4.44%→32.26%); 0.50x WATCH-1 both 0.08%→0.59% (still PASS, 2.41pp headroom); BluSky_Premium_50K alone carries no published figure — the other 4 Bulenox tiers DO (closed/NO-GO'd archived book, §2/§4b; 2026-08-23 fix-pass corrected a false "5 tiers none" claim)
`MEASURED — WITH NAMED RESIDUAL (2026-08-23 fix-pass correction)` — CLOCK re-run
complete on the two tiers carrying a published figure on the **live candidate book** (Bulenox_100K,
BluSky_Premium_100K, Class-S candidate #1). The original claim that "the other 5 tiers carry no
published bust/pass figure" was **false for 4 of them** — a separate, CLOSED/NO-GO'd,
Pepperstone-sourced archived campaign (`lab/archive/bulenox_futures_remc_2026-07-01/`) publishes
EOD-clock bust/pass figures for Bulenox_25K/50K/100K/150K/250K under three sizing configurations.
The miss and its correction are recorded in §2/§4b — most cells are already-FAIL and
monotonicity-disposed; a small, explicitly-named PASS-side residual (chiefly Bulenox_25K/50K) is
**not re-run this pass**, for stated reasons, rather than silently left implying "resolved."
BluSky_Premium_50K is the only tier of the 7 that genuinely carries no published figure anywhere
(re-confirmed under a corrected search methodology — §2/§6).
**Date:** 2026-08-23
**Task:** [`docs/superpowers/plans/2026-08-23-viable-strategy-parallel-s4-firm-repair.md`](../../../../docs/superpowers/plans/2026-08-23-viable-strategy-parallel-s4-firm-repair.md)
Task R1
**Predecessor:** [`Q-FIRMEOD-1` closure `FALSIFIED`](../../../../docs/briefs/closures/Q-FIRMEOD-1-closure-falsified.md)
— entry packet (i): the CLOCK evidence + explicit instruction that a successor "re-runs the
intraday-honest fix (`intraday_low`) across all 7 tiers per the W1 ADR pattern and reports whether
any published figure flips."
**Method owner:** [`docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md`](../../../../docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md)
(`Accepted`) — this campaign extends that method's scope from Tradeify/MFFU to Bulenox/BluSky; it
does not re-open or amend the ADR itself.
**Runner / raw:** [`run_r1_bulenox_blusky_intraday.py`](run_r1_bulenox_blusky_intraday.py) ·
[`r1_bulenox_blusky_intraday_report.json`](r1_bulenox_blusky_intraday_report.json)
**Gate (frozen, unedited):** bust ≤ 3.0% ∧ P(pass) ≥ 50% —
[`2026-07-13 survivor-scoring prereg`](../../../../docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md)
**Cost:** $0 / K=0 — reused committed engine fixtures + gitignored vendor CSVs already present
locally (byte-verified against the tracked `SHA256SUMS` manifests before use; none re-fetched or
re-purchased).

---

## §0 — Rule 0 reads (this session)

- `core/firm_rules.py` — `grep -n '"dd_type": "trailing"'` re-run this session: **122, 134, 146,
  158, 170, 538, 554** (7 hits — Bulenox_25K/50K/100K/150K/250K + BluSky_Premium_50K/100K). The
  Q-FIRMEOD-1 closure's own pin (92,104,116,128,140,508,524) has **shifted by a constant +30**
  since it was recorded — confirmed stale-but-consistent (same 7 tiers, same relative order), not
  a changed tier set.
  **2026-08-24 currency:** still 7 hits; BluSky pair moved again (now 122, 134, 146, 158, 170,
  600, 616). Durable hook: `grep -c '"dd_type": "trailing"' core/firm_rules.py` expected `7`.
  Closure §10 carries the same note.
- `core/mc/simulation.py` (`simulate_path`, full function) — the `equity_test = min(equity_new,
  equity + intraday_low[day]*scale)` construction (L131-134) and the `dd_type=="trailing"` branch
  (L141-151).
- `core/mc/preflight.py` (`firm_kwargs`, full function) — confirms `dd_type="trailing"` never
  threads `dd_lock_offset_usd` (only `"trailing_locking"` does, L172-180), so Bulenox/BluSky need
  no lock-unreachable patch.
- `lab/discovery/prop_survivor_scoring.py` (full file) — `run_tier_remc`, `firm_kwargs`-based,
  confirmed tier-agnostic (no Tradeify/MFFU special-casing); `load_scoring_thresholds`,
  `paired_blocks_from_daily`, `assert_intraday_channel_nonvacuous`.
- `lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/run_w1_intraday_both_halves.py` (full
  file) + its `RESULTS_INTRADAY_W1.md` — the template this campaign extends. **Defect found**:
  its own `sys.path` setup points at `class_s_candidate1_scoring_2026-07-15/` for
  `run_class_s_c1_scoring.py`, which the Great Prune (commit `283d1de`, 2026-08-08) removed from
  that directory — the module now lives only in `geofit_iid_sufficiency_power_2026-08-15/`
  (vendored copy, byte-identical per that probe's own README). Confirmed empirically:
  `python -c "import run_w1_intraday_both_halves"` raises `ModuleNotFoundError` today with the
  path as originally written. Not repaired in the frozen script (Trap #12); this campaign's own
  runner points at the live location instead (see its docstring).
- `tests/core/test_mc_intraday_barrier.py` (full file) — `9 passed`; reproduced verbatim.
- `docs/briefs/closures/Q-FIRMEOD-1-closure-falsified.md`, `docs/notes/audits/2026-08-23-bulenox-lock-scope-resolution.md`
  (R2, already landed this session at commit `65dc17b` before this task started — the Bulenox
  Master-lock does **not** reach the modeled horizon, so no `dd_lock_offset_usd`-shaped patch is
  needed for either Bulenox or BluSky in this campaign).
- Candidate published-figure sources read in full: `lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/RESULTS.md`,
  `lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/RESULTS.md`,
  `lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/CORRECTED_FULLPANEL.md`,
  `lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/run_corrected_haircut_fullpanel.py`,
  `lab/archive/class_s_candidate2_scoring_2026-07-15/RESULTS.md`, `lab/archive/q_compose_1_2026-07/RESULTS.md`,
  `lab/analysis/c1/band_quantization_2026-08-02/RESULTS.md`,
  `lab/analysis/c1/f3_cadence_successor_venues_2026-08-05/RESULTS.md`,
  `lab/analysis/c1/venuegeo_dp3_bustceiling_2026-08-05/RESULTS.md`,
  `lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md` (§5 — confirms that campaign carries
  **zero** Bulenox/BluSky scoring calls, structurally blocked pending this repair),
  `docs/briefs/pre-registration/2026-08-02-sub100k-realizable-book-scoring-prereg.md` (`SIGNED /
  FROZEN`, never executed — no RESULTS/closure exists anywhere in the tree).

---

## §1 — CLOCK sanity check (reproduced before the full run, per task brief)

`pytest tests/core/test_mc_intraday_barrier.py -q` → `9 passed`.

Reproduced the closure's own Bulenox_100K diff **independently**, against the real
`firm_kwargs('Bulenox_100K')` output (not the test's hand-built fixture):

```
firm_kwargs(Bulenox_100K) = {'starting_equity': 100000.0, 'daily_loss_pct': None,
  'profit_target': 106000.0, 'min_trading_days': 0, 'inactivity_limit': 1501,
  'consistency_frac': None, 'dd_type': 'trailing', 'trailing_dd_pct': -0.03}
no-intraday: ('horizon_cap', 1, 0.001, None)
intraday:    ('bust_trailing', 1, 0.001, 0)
```

Byte-identical flip to the closure's §1 citation, confirmed on production `firm_kwargs`, not a
test fixture.

**BluSky, run through the same direct diff (not assumed clean by analogy or by its own "EOD
trailing drawdown" language, per the task brief's explicit instruction):** all 7 `dd_type="trailing"`
tiers' real `firm_kwargs()` output was diffed directly against a common-shape excursion
(1.5× each tier's own dollar trail width, closing back to a small loss):

| Tier | Trail width ($) | No-intraday | Intraday (excursion) | Flips |
|---|---:|---|---|:---:|
| Bulenox_25K | $1,500 | `horizon_cap` | `bust_trailing` (−$2,250) | YES |
| Bulenox_50K | $2,500 | `horizon_cap` | `bust_trailing` (−$3,750) | YES |
| Bulenox_100K | $3,000 | `horizon_cap` | `bust_trailing` (−$4,500) | YES |
| Bulenox_150K | $4,500 | `horizon_cap` | `bust_trailing` (−$6,750) | YES |
| Bulenox_250K | $5,500 | `horizon_cap` | `bust_trailing` (−$8,250) | YES |
| BluSky_Premium_50K | $2,000 | `horizon_cap` | `bust_trailing` (−$3,000) | YES |
| BluSky_Premium_100K | $3,000 | `horizon_cap` | `bust_trailing` (−$4,500) | YES |

All 7 tiers flip under direct `simulate_path` diff on their own real `firm_kwargs()` — the CLOCK
defect is structural (engine-generic across every `dd_type="trailing"` branch), not a Bulenox-only
coincidence, and BluSky's own textual "EOD" framing does **not** exempt it. This block satisfies
the task's explicit "run BluSky through the same direct `simulate_path` diff Bulenox got" —
BluSky's two tiers were diffed directly here, not inferred.

---

## §2 — Per-tier disposition

**Gate (R1):** `RESOLVED` when all 7 tiers carry an honest-clock figure, an explicit
none-to-re-measure line, or (new, this fix-pass) an explicit named disposition for a published
figure this campaign declines to re-run — verdict below.

> ⚠ **Correction (2026-08-23 fix-pass, reviewer-flagged):** the table below originally read "none
> — zero repo hits" for Bulenox_25K/50K/150K/250K. **That was false.** A separate archived campaign,
> `lab/archive/bulenox_futures_remc_2026-07-01/` (CLOSED — R6 NO-GO, futures-prop program closed
> 2026-07-10, per `lab/CATALOG.md`), publishes EOD-clock trailing-DD bust/pass figures for all five
> Bulenox tiers across three RESULTS docs (`RESULTS_C4_forceflat_2026-07-03.md`,
> `RESULTS_C5_integer_2026-07-03.md`, `RESULTS_DJ30only_1leg_2026-07-03.md`). The miss had two
> independent causes, both fixed in this pass's search methodology (§6):
> 1. **`.rgignore`** (repo root) deliberately excludes `lab/archive/` (+ `docs/ltm/`,
>    `core/strategies/_archive/`) from the default `rg`/Grep-tool search surface — by design, per
>    its own header comment, as a "cold corpus... still Readable by path," with a documented
>    force-search escape hatch (`rg --no-ignore`) that neither the original pass nor the first
>    fix-pass's "independent" repo-wide grep used. This is why a plain, **unscoped** (repo-root, no
>    path filter) grep for these tier names returns **zero** hits under
>    `lab/archive/bulenox_futures_remc_2026-07-01/`, even though the 5 files there are git-tracked
>    and directly `Read`-able (an explicit path/single-file grep bypasses the exclusion — only an
>    unscoped, repo-root sweep is affected, exactly the search shape both prior passes used — §6).
> 2. The tier-name grep pattern itself (`Bulenox_25K` etc.) does not match citations that name a
>    tier by dollar amount only (e.g. "the C4 25K gate number") — missing a citing surface
>    (`lab/analysis/legacy/futures_conversion_2026-07-01/B0_GATE_2026-07-03.md`, `ACTIVE`/hot,
>    outside `lab/archive/` and thus unaffected by cause 1) that quotes the same figures in its own
>    prose findings.
>
> Corrected disposition below; full accounting (including why this pass does not re-run the
> PASS-side cells) in §4b.

| Tier | Published bust/pass figure(s) to re-run | Disposition |
|---|---|---|
| **Bulenox_100K** | 1.00×: 3.51%/96.49% ([`class_s_candidate1_scoring_2026-07-15/RESULTS.md`](../class_s_candidate1_scoring_2026-07-15/RESULTS.md), reproduced [`tradeify_eval_lock_correction_2026-07-22/RESULTS.md`](../tradeify_eval_lock_correction_2026-07-22/RESULTS.md)) · 0.50× WATCH-1: 0.08%/99.82% ([`CORRECTED_FULLPANEL.md`](../class_s_c1_haircut_regime_remc_2026-07-16/CORRECTED_FULLPANEL.md)) | **MEASURED — §3** (live candidate book) |
| **BluSky_Premium_100K** | 1.00×: 4.44%/95.54% (same sources) · 0.50× WATCH-1: 0.08%/99.80% (same source) | **MEASURED — §3** (live candidate book) |
| Bulenox_25K | `bulenox_futures_remc_2026-07-01` (different, closed book): C4 0.40% · C5 0.50% · DJ30-only CAPPED 0.00% (VOID, 0-contract) · DJ30-only FULL 0.05% — **all PASS vs the 3.0% ceiling** | **NAMED RESIDUAL, not re-run — §4b** (was wrongly "none") |
| Bulenox_50K | same source: C4 1.13% · C5 2.81% · DJ30-only CAPPED 0.02% (VOID) · DJ30-only FULL 0.19% — **all PASS** | **NAMED RESIDUAL, not re-run — §4b** (was wrongly "none") |
| Bulenox_150K | same source: C4 8.54% FAIL · C5 8.74% FAIL · DJ30-only CAPPED 0.29% PASS · DJ30-only FULL 3.29% FAIL | **FAIL cells monotonicity-disposed; 0.29% PASS cell is a named residual — §4b** (was wrongly "none") |
| Bulenox_250K | same source: C4 18.50% FAIL · C5 21.16% FAIL · DJ30-only CAPPED 2.41% PASS · DJ30-only FULL 10.69% FAIL | **FAIL cells monotonicity-disposed; 2.41% PASS cell is a named residual — §4b** (was wrongly "none") |
| BluSky_Premium_50K | none | **none to re-measure** — re-confirmed under the corrected search methodology (§6, `rg --no-ignore`): `band_quantization_2026-08-02/RESULTS.md` is arithmetic/sizing only (own banner: "no MC, no gate scored, no verdict claimed"); the sub-100K realizable-book scoring pre-reg (`docs/briefs/pre-registration/2026-08-02-sub100k-realizable-book-scoring-prereg.md`) is `SIGNED/FROZEN` but was **never executed**; the archived Bulenox campaign does not model BluSky at all (Bulenox-tier-rules-only, per its own module docstring) — this tier's "none" claim holds |

**Bulenox_100K note:** the archived `bulenox_futures_remc_2026-07-01` campaign ALSO publishes a
Bulenox_100K figure (C4 8.54% FAIL, C5 12.42% FAIL, DJ30-only CAPPED 0.83% PASS, DJ30-only FULL
3.29% FAIL, bucketed with 150K) for a **different book** (2-leg DJ30-force-flat + NAS100,
%-equity/integer sizing) than the MEASURED Class-S candidate #1 figure above. Same disposition as
150K/250K: FAIL cells monotonicity-disposed, the 0.83% PASS cell is part of the named residual —
§4b.

**Also considered, disposed by monotonicity rather than re-run (§4):**
`class_s_candidate2_scoring_2026-07-15` (Bulenox_100K 7.38%/92.62% FAIL, BluSky_Premium_100K
8.76%/91.24% FAIL) and `q_compose_1_2026-07` (Bulenox_100K 44.75% FAIL, BluSky_Premium_100K
51.91% FAIL) — both closed/FALSIFIED books, both already deep FAIL (7–52pp over the 3.0%
ceiling) on the EOD clock.

---

## §3 — Honest-clock re-run (Bulenox_100K / BluSky_Premium_100K)

**Method:** identical construction to W1 — `intraday_low` derived from the same MYM/MNQ 15m bars
(`core/data/bar_data/MYM_M15.csv`, `MNQ_M15.csv`) and the same static×1R trade panel
(`Striker_DJ30_v4.5_MYM…15d8b.csv`, `Striker_NAS100_v1…beabf.csv`), reused verbatim via
`W1.build_book_intraday_low` (imported as a library, not re-derived — see §0 defect note).
Thresholds/seeds/sims/horizon from `load_scoring_thresholds()` reading the same frozen
2026-07-13 pre-reg W1 read: seeds 42/123/2026, 10,000 sims/seed, horizon 1500. Both tiers are
`dd_type="trailing"`, so no `dd_lock_offset_usd` patch applies (that kwarg is
`trailing_locking`-only). Bulenox_100K has no `consistency_rule_pct` (Run-1/degenerate, matching
its published figure's own `gated_on: "run1_degenerate"`); BluSky_Premium_100K's is 34.0%
(Run-2), matching its own `gated_on: "run2"`.

**Non-vacuity guard, per target tier** (not inherited from Tradeify's W1 proof — each tier's own
`dd_type="trailing"` %-of-peak branch was independently checked to prove the channel is
load-bearing for it specifically; horizon 400, 200 sims/seed, 1.00× book):

| Tier | EOD bust | Real (intraday) bust | Zeros-arm reproduces EOD? |
|---|---:|---:|:---:|
| Bulenox_100K | 1.83% | 26.17% | OK (asserted in-script) |
| BluSky_Premium_100K | 2.17% | 30.17% | OK (asserted in-script) |

(Non-vacuity guard runs at horizon=400/200 sims — a short-horizon proxy to keep the guard cheap, not
the production headline; the production headline is §3's main table below.)

**Results — full-panel, both published arms:**

| Tier | Arm | EOD-clock (published) | Honest-clock (this run) | Δ bust (pp) | Verdict flip (PASS→FAIL)? |
|---|---|---:|---:|---:|:---:|
| Bulenox_100K | 1.00× | 3.51% / 96.49% | **26.77% / 73.23%** FAIL | **+23.26pp** | No — already FAIL both clocks |
| Bulenox_100K | 0.50× WATCH-1 | 0.08% / 99.82% | **0.59% / 99.33%** PASS | **+0.51pp** | No — PASS both clocks |
| BluSky_Premium_100K | 1.00× | 4.44% / 95.54% | **32.26% / 67.74%** FAIL | **+27.82pp** | No — already FAIL both clocks |
| BluSky_Premium_100K | 0.50× WATCH-1 | 0.08% / 99.80% | **0.59% / 99.31%** PASS | **+0.51pp** | No — PASS both clocks |

**No verdict flips against the 3.0%/50% floor on either measured tier at either arm.** The
magnitude moves are large regardless — proportionally ~7.4× at 0.50× (0.08%→0.59% on both tiers,
essentially identical honest-clock outcomes for Bulenox and BluSky at this arm) and an order of
magnitude at 1.00× (3.51%→26.77%, 4.44%→32.26%, ~7.6–7.7× worse in absolute percentage points).
Both tiers' `dd_type="trailing"` %-of-peak trail (F2 caveat) interacts with the intraday barrier far
more severely than Tradeify/MFFU's fixed-$ `trailing_locking` trail did under the identical fix
(W1's own 0.50× delta was +0.61pp off a 0.11% published base — a ~6.5× proportional move, in the
same order as this campaign's ~7.4×, but off a published base that started at essentially the same
absolute level). This is consistent with — not contradicted by — the pre-existing repo note that
Bulenox's `trailing` branch is "doubly optimistic" (F2 + no venue-native intraday accounting), now
measured rather than asserted. At the WATCH-1 0.50× rung specifically (the only rung with live
decision relevance today, per CLAUDE.md's live-execution posture — no strategy is currently
deployed at either firm), both tiers clear the 3.0% ceiling with **2.41pp of headroom**, not a
knife's-edge PASS.

Raw floats: [`r1_bulenox_blusky_intraday_report.json`](r1_bulenox_blusky_intraday_report.json).

---

## §4 — Monotonicity disposition (candidate #2, Q-COMPOSE-1 — not independently re-run)

`simulate_path`'s intraday barrier check is `equity_test = min(equity_new, equity +
intraday_low[day]*scale)` (`core/mc/simulation.py:131-134`) — literally a `min()` against the
close-only value, so `equity_test <= equity_new` on every day, for every path, whenever
`intraday_low` is populated. The trailing-bust condition `(equity_test - peak)/peak <=
trailing_dd_pct` (or the `trailing_locking` equivalent) can therefore only become *easier* to
trigger as `equity_test` falls, never harder. Since `simulate_path` returns at the first day a
bust condition fires, any path that busts on the EOD-only clock busts on the honest clock too (same
day or earlier) — so, on the **same seeds/blocks**, `bust_rate(honest) >= bust_rate(EOD)` and
`pass_rate(honest) <= pass_rate(EOD)` always. This is a property of the engine code, not an
assumption about the data.

`class_s_candidate2_scoring_2026-07-15` (Bulenox_100K 7.38%, BluSky_Premium_100K 8.76%) and
`q_compose_1_2026-07` (Bulenox_100K 44.75%, BluSky_Premium_100K 51.91%) are both **already FAIL**
on the EOD clock, by 4.4–49pp over the 3.0% ceiling. By the monotonicity property above, their
honest-clock bust rate is provably `>=` those EOD figures — the verdict cannot flip FAIL→PASS, and
no re-run changes that disposition. Both candidates are closed (FALSIFIED); re-running them would
spend K to reconfirm an engine-forced conclusion, which this campaign declines to do. This is
recorded explicitly rather than silently skipped, per the task's own "record 'none to re-measure'
rather than manufacturing" instruction extended to the FAIL-side case: there is nothing to
manufacture here because the direction is already forced.

---

## §4b — Archived Bulenox force-flat/integer campaign (added this fix-pass, 2026-08-23)

**Source:** `lab/archive/bulenox_futures_remc_2026-07-01/` — CLOSED, R6 NO-GO, futures-prop program
closed 2026-07-10 (`lab/CATALOG.md`). A 2-leg DJ30-force-flat(17:00 ET) + clean-NAS100 book under
each Bulenox tier's own trailing-DD rules, across three RESULTS docs dated 2026-07-03:
`RESULTS_C4_forceflat` (%-equity sizing, `PRE_SHOCK_1R`-pinned), `RESULTS_C5_integer` (integer
CME-micro-contract sizing, Bulenox contract caps, $2.22/contract costs), `RESULTS_DJ30only_1leg`
(DJ30-only, one-legged variant, both a CAPPED and a FULL-risk arm). **Not** the Class-S candidate #1
book §3 measures — a different strategy composition and sizing basis entirely.

**Engine-equivalence check (Rule 0, this session):** all three drivers (`run_bulenox_remc.py`,
`c5_integer_remc.py`, `dj30_only_remc.py`) import `run_seed` from `portfolio_mc` (the compatibility
facade `core/portfolio_mc.py` forwards from `core/mc/modes.py`/`core/mc/simulation.py`). Verified
directly, this session:

```
python -c "import sys; sys.path.insert(0,'core'); import portfolio_mc as pm; import mc.simulation as sim; print(pm.run_seed is sim.run_seed)"
# True — literally the same function object as the one §3/§4 measure against.
```

None of the three drivers' `firm_kwargs` dicts pass `intraday_low`/`intraday_blocks` (confirmed by
reading each driver in full) — every cell in all three tables is a pure EOD-only-clock run on the
**current, live** engine, not a frozen/superseded one. This is exactly the class of figure R1 exists
to repair, and the §4 monotonicity property (`equity_test = min(equity_new, equity +
intraday_low[day]*scale)` can only make a trailing-DD bust condition easier to trigger, never
harder) applies to it identically.

**Monotonicity-disposed (already FAIL vs. the frozen 3.0% ceiling on the EOD clock — honest-clock
bust rate can only be `>=` these, so the verdict cannot flip FAIL→PASS and no re-run changes it):**

| Tier | Book | Cited EOD-clock bust | 
|---|---|---:|
| Bulenox_100K (archived book) | C4 %-equity | 8.54% |
| Bulenox_100K (archived book) | C5 integer+cost | 12.42% |
| Bulenox_150K | C4 %-equity | 8.54% |
| Bulenox_150K | C5 integer+cost | 8.74% |
| Bulenox_150K | DJ30-only FULL (bucketed w/100K) | 3.29% |
| Bulenox_250K | C4 %-equity | 18.50% |
| Bulenox_250K | C5 integer+cost | 21.16% |
| Bulenox_250K | DJ30-only FULL | 10.69% |

**Named residual — NOT re-run this pass (published, PASSES the 3.0% ceiling on the EOD clock,
genuinely unresolved by monotonicity):**

| Tier | Book | Cited EOD-clock bust |
|---|---|---:|
| Bulenox_25K | C4 · C5 · DJ30-only CAPPED (VOID, 0-contract) · DJ30-only FULL | 0.40% · 0.50% · 0.00% · 0.05% |
| Bulenox_50K | C4 · C5 · DJ30-only CAPPED (VOID, 0-contract) · DJ30-only FULL | 1.13% · 2.81% · 0.02% · 0.19% |
| Bulenox_100K (archived book) | DJ30-only CAPPED | 0.83% |
| Bulenox_150K | DJ30-only CAPPED | 0.29% |
| Bulenox_250K | DJ30-only CAPPED | 2.41% |

A published PASS cannot be monotonicity-disposed (only FAIL survives the "can only get worse"
direction) — R1's own §3 shows deepening as large as ~7.6× at 1.00× on a *different* book, but
borrowing that multiplier onto this book to declare these cells "probably still PASS" would bind a
metric to the wrong cohort. **Why this pass does not re-run them instead, stated rather than
silently skipped, per three independent reasons:**

1. **The primary vendor feed is retired.** All three drivers read Pepperstone US30/NAS100 CFD
   exports (`RAW_DJ30_CSV = PEPPERSTONE_PANELS["striker"]`). CLAUDE.md's canonical-feed policy:
   "Canonical feed = CME futures TV exports... OANDA and Pepperstone are retired." Reproducing this
   exact book on its original data source runs against current data policy, not merely a missing
   file.
2. **The entry point is provably broken today, not just data-blocked.** `run_bulenox_remc.py`'s own
   import line (`from portfolio_mc import (..., BASELINE_BALANCE, PEPPERSTONE_PANELS, ...)`) raises
   `ImportError` on the current `core/portfolio_mc.py` facade — verified directly this session:
   ```
   python -c "import sys; sys.path.insert(0,'core'); from portfolio_mc import (ALLOCATIONS, BASELINE_BALANCE, PEPPERSTONE_PANELS, SEEDS, SIMS_PER_SEED, build_daily_panel, build_week_blocks, load_trades, run_seed)"
   # ImportError: cannot import name 'BASELINE_BALANCE' from 'portfolio_mc'
   ```
   `run_seed`/`simulate_path` migrated cleanly (engine-equivalence check above);
   `BASELINE_BALANCE`/`PEPPERSTONE_PANELS` did not. Re-running needs a migration fix first, not
   just `intraday_low` wiring.
3. **The program is dead.** CLOSED — R6 NO-GO, 2026-07-10. No live capital-allocation or §4-discharge
   decision depends on this book today (the operative candidate is the Class-S candidate #1 book §3
   measures). Spending fresh compute + a migration fix to resurrect a NO-GO'd, retired-feed program
   absent an operator GO would run against Rule 2 (budget before acting).

**Disposition:** named explicitly, not silently dropped — reader-intercept banners added at the
source (table below) so a reader landing on these figures directly is warned rather than misled; no
further action taken or owed unless an operator explicitly revisits this archived program.

**Reader-intercept banners added this fix-pass** (frozen bodies left otherwise unedited, Trap #12
discipline — same convention as §6's original three):

| Surface | Why bannered |
|---|---|
| `lab/archive/bulenox_futures_remc_2026-07-01/RESULTS_C4_forceflat_2026-07-03.md` | Reviewer-flagged source of the 4-tier false claim; the primary %-equity gate table |
| `lab/archive/bulenox_futures_remc_2026-07-01/RESULTS_C5_integer_2026-07-03.md` | Same campaign, integer-sizing gate table (own PASS/FAIL cells) |
| `lab/archive/bulenox_futures_remc_2026-07-01/RESULTS_DJ30only_1leg_2026-07-03.md` | Same campaign, DJ30-only variant (own PASS/FAIL cells) |
| `lab/analysis/legacy/futures_conversion_2026-07-01/B0_GATE_2026-07-03.md` | `ACTIVE`/hot (not archived), directly quotes "the C4 25K gate number (99.60%)" and "C4's 91.46% gate pass" in its own prose findings |

**Scoped out, disclosed rather than silently skipped:** `lab/archive/tradeify_selectflex_remc_2026-07-10/{RESULTS_tradeify_remc_2026-07-10.md,RESULTS_tradeify_integer_2026-07-10.md,NOTES.md}`
also cite these same C4/C5 figures, as an inert "xref" comparison column in their own gate tables.
Not bannered: that campaign is itself archived/`FALSIFIED` (`lab/CATALOG.md`), and its own verdict
in every cited row already fails on the p99-DD dimension under its own stricter gate, independent
of the bust-side CLOCK question this repair concerns — the more precise honest-clock bust number
would not change that campaign's own conclusion. Judgment call, disclosed per this repo's own
precedent (§6 of the audit note), not a mechanical rule.

---

## §5 — What this does NOT license

- Does not edit `dd_type`, `trailing_dd_pct`, or any `firm_rules.py` numeric field — the forbidden
  move both the parent plan and the Q-FIRMEOD-1 closure name explicitly.
- Does not resolve the Bulenox lock-scope question — already resolved separately by R2
  ([`docs/notes/audits/2026-08-23-bulenox-lock-scope-resolution.md`](../../../../docs/notes/audits/2026-08-23-bulenox-lock-scope-resolution.md)),
  landed before this task started; this campaign only carries CLOCK.
- Does not touch the F2 fixed-$-vs-%-of-peak faithfulness caveat — `dd_type="trailing"` still
  models Bulenox/BluSky's real fixed-$ trail as a %-of-peak trail that **widens** as the peak
  rises, which is a **separate, still-open** optimism source layered underneath the CLOCK fix this
  campaign makes. The honest-clock figures below are still labeled `optimistic-lower-bound` for
  that reason — CLOCK-honest is not the same claim as F2-faithful.
- Does not re-litigate the LOCK-defect (`dd_lock_offset_usd`) correction chain — that is a
  Tradeify/MFFU-only, already-closed issue (W1 ADR §2), orthogonal to this campaign.
- Does not license citing any Bulenox/BluSky bust-rate figure in a cross-firm capital-allocation
  comparison beyond what is reported here — Task R3 (survivor §4 scoring) is a separate,
  downstream task this campaign does not perform.
- Does not open or amend the W1 ADR, the survivor-scoring pre-reg, or any frozen threshold.
- Does not license citing Bulenox_25K/50K's (or 100K/150K/250K's DJ30-only-CAPPED) archived
  PASS-side figures (§4b) as an honest-clock bound — they are a named, disclosed residual, not a
  resolved one. Does not re-run or migrate the `bulenox_futures_remc_2026-07-01` drivers, or
  restore Pepperstone vendor data for them — §4b's three reasons stand until an operator GO says
  otherwise.

---

## §6 — Reproduction

```bash
python -m pytest tests/core/test_mc_intraday_barrier.py -q
# Expected: 9 passed

python lab/analysis/c1/firm_model_repair_r1_7tier_2026-08-23/run_r1_bulenox_blusky_intraday.py
# Requires gitignored vendor CSVs present locally (core/data/bar_data/{MYM,MNQ}_M15.csv,
# core/data/tv_exports/cme/Striker_DJ30_v4.5_MYM…15d8b.csv,
# core/data/tv_exports/cme/Striker_NAS100_v1…beabf.csv — sha256-pinned in
# lab/analysis/c1/geofit_iid_sufficiency_power_2026-08-15/run_class_s_c1_scoring.py PANEL_FILES).
# ~24 min wall on this machine (4 x 10k-sim x 3-seed runs at horizon 1500 + 2 non-vacuity
# guards at horizon 400; per-call: Bulenox 1.00x 235s, BluSky 1.00x 302s, Bulenox 0.50x 386s,
# BluSky 0.50x 348s -- consistency-gated (Run-2) tiers/arms run longer on average since a
# profit-target hit that fails the consistency check does not exit early).

grep -n '"dd_type": "trailing"' core/firm_rules.py
# Expected: 122, 134, 146, 158, 170, 538, 554 (re-confirm before citing — these shift when
# firm_rules.py grows above the Bulenox block, as they already have once since Q-FIRMEOD-1)

# Corrected search methodology (this fix-pass) -- reaches the .rgignore-excluded cold corpus
# (lab/archive/, docs/ltm/, core/strategies/_archive/) that an UNSCOPED repo-root grep silently
# skips (an explicit path/single-file grep is unaffected -- only the "search the whole repo" shape
# both prior passes used is blind to it). Path-separator-agnostic filename match, not a total file
# count (which drifts as more surfaces cite these tier names, including this fix-pass's own prose):
rg -l "Bulenox_25K|Bulenox_50K|Bulenox_150K|Bulenox_250K|BluSky_Premium_50K" -g '!.git' | grep -c "bulenox_futures_remc_2026-07-01"
# Expected: 0 -- plain rg cannot see lab/archive/bulenox_futures_remc_2026-07-01/ at all.
rg --no-ignore -l "Bulenox_25K|Bulenox_50K|Bulenox_150K|Bulenox_250K|BluSky_Premium_50K" -g '!.git' | grep -c "bulenox_futures_remc_2026-07-01"
# Expected: 5 -- --no-ignore surfaces all 5 files in that directory that reference these tiers.

# Engine-equivalence check backing §4b's monotonicity argument:
python -c "import sys; sys.path.insert(0,'core'); import portfolio_mc as pm; import mc.simulation as sim; print(pm.run_seed is sim.run_seed)"
# Expected: True

# The archived campaign's own entry-point import is broken today (data-independent defect):
python -c "import sys; sys.path.insert(0,'core'); from portfolio_mc import (ALLOCATIONS, BASELINE_BALANCE, PEPPERSTONE_PANELS, SEEDS, SIMS_PER_SEED, build_daily_panel, build_week_blocks, load_trades, run_seed)"
# Expected: ImportError: cannot import name 'BASELINE_BALANCE' from 'portfolio_mc'
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-23 | Initial. CLOCK sanity reproduced (test + independent firm_kwargs diff, all 7 tiers incl. both BluSky tiers directly diffed); honest-clock re-run for the two tiers carrying a published figure; monotonicity disposition for the two FALSIFIED candidates; 5 tiers recorded none-to-re-measure. | Claude Code (Sonnet 5) |
| 2026-08-23 | **Fix-pass correction** (reviewer-flagged false claim). §2's "none — zero repo hits" for Bulenox_25K/50K/150K/250K was false: `lab/archive/bulenox_futures_remc_2026-07-01/` (CLOSED, R6 NO-GO) publishes EOD-clock bust/pass figures for all 5 Bulenox tiers across 3 RESULTS docs, missed by both the original pass and the first fix-pass's re-verification because `.rgignore` silently excludes `lab/archive/` from default `rg`/Grep-tool search. Added §4b: engine-equivalence-verified monotonicity disposal for already-FAIL cells; explicit named residual (not re-run, 3 stated reasons) for PASS-side cells; 4 reader-intercept banners added at source. Corrected the Gate/Status framing, CLAUDE.md's mirrored claim, and the CATALOG one-liner. See `docs/notes/audits/2026-08-23-r1-bulenox-blusky-clock-repair.md` §13. | Claude Code (Sonnet 5) |
