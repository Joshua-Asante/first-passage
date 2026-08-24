**Theme:** c1

# Payoff-shape feasibility map (Phase A Task A2 — the target spec)

**Status:** **ACTIVE** — 945-cell region published (Tradeify Select / MFFU / **Tradeify Growth**, the last added 2026-08-24); Select≡MFFU bit-identical; 8/8 corner-case + 3/5 MARGINAL-band validation tuples resolve clean at full N (2/5 stay MARGINAL, 0 confident-verdict flips). §4 `sims_per_seed` reduction **operator-accepted 2026-08-24** (published region's N; not a frozen-N re-sweep; not a Phase B GO). ⚠ **§7.2's "no cell at win_rate ≤ 50% is FEASIBLE" is scoped to the $3,000 rope and does NOT hold for Growth's $3,500 rope — see §13.** Screens shape, not mechanisms.

**What this is not:** not a strategy, not a candidate, not a backtest of anything real. It is a
coverage map over a *synthetic* trade-generating process, scored through the production
survivor-MC engine, so Phase B can source a mechanism against a quantified target instead of an
open search
([`sequence overview`](../../../../docs/superpowers/plans/2026-08-23-viable-strategy-sequence-overview.md),
[`Phase A plan`](../../../../docs/superpowers/plans/2026-08-23-viable-strategy-phase-a-target-derivation.md)
Task A2).

---

## §0 — Rule 0 reads (production source, this session, 2026-08-23)

| Source | Anchor (`git log -1`, per-file) | What it grounds |
|---|---|---|
| `core/mc/simulation.py` (`simulate_path`, `run_seed`) | `027a729` 2026-08-14 | The engine itself — intraday-honest limb (`intraday_low`), consistency gate (`consistency_frac`, L188-196), barrier geometry. Reused unmodified; never re-implemented. |
| `core/mc/preflight.py` (`firm_kwargs`, `assert_engine_ready`, `summarize_outcomes`) | `027a729` 2026-08-14 | None-safe firm threading, `dd_type` dispatch, the F1 bucket-sum headline-bust assertion. Reused unmodified. |
| `core/firm_rules.py` `Tradeify_Select_100K` / `MFFU_Rapid_100K` blocks | `65dc17b` 2026-08-23 | Geometry: `$3,000` trail (both), `dd_lock_offset_usd` unreachable (both, fixed 2026-08-04), `consistency_rule_pct` 40.0 / 50.0, `min_trading_days` 3 / 2, `inactivity_max_idle_days` 5 (both), `micro_contract_cap` 80 (both). |
| `lab/discovery/prop_survivor_scoring.py` (`load_scoring_thresholds`, `paired_blocks_from_daily`, `run_tier_remc`'s own primitive call sequence) | `027a729` 2026-08-14 | Frozen seeds `(42, 123, 2026)`, frozen horizon `1500`, frozen `eval_bust_ceiling=0.03`, frozen `pass_floor=0.50` — parsed from the pre-registration, never hand-transcribed; the paired-block-bootstrap idiom this harness's own scoring loop mirrors exactly. |
| `docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md` | (parsed at runtime by `load_scoring_thresholds`, not hand-copied) | Source of the frozen ceiling/seeds/horizon values above — this harness's own `main()` asserts `thr.eval_bust_ceiling == 0.03` and `thr.pass_floor == 0.50` at every invocation, so a future prereg edit fails loudly rather than silently. |
| `docs/spec/2026-08-05-eval-mechanism-shape-screen.md` EM2 row + 2026-08-08 amendment banner | `027a729` 2026-08-14 | EM2's edge-indexed frontier — `$250 @ 0.49R` / `$275 @ 0.65R` / `$325 @ 0.85R`, "interpolate down, never up." |
| `docs/adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md` | `027a729` 2026-08-14 | EM2's cell **arithmetic** stands; the cells' **edge labels** (which R a real construct achieves) are void as provenance — read as hypothetical independent-entry edges only. This harness follows that ruling: the three EM2 dollar figures are used purely as $-per-trade coverage levels, never as a claim about any real mechanism's R. |
| `docs/briefs/closures/Q-FIRMEOD-1-closure-falsified.md` | `50396fc` 2026-08-23 | Bulenox's own `trailing` CLOCK flips intraday-honest (bust_trailing 0→1) and carries unresolved LOCK-language on its Master Account primary source; BluSky's CLOCK is untested. **Stop rule: no Bulenox/BluSky bust-rate figure may be cited in a cross-firm comparison** until a successor lands. This harness's §5 BLOCKED columns implement that bar directly. |
| `docs/briefs/closures/Q-STATVALID-1-closure-falsified.md` | `50396fc` 2026-08-23 | The SE-of-proportion / 2-sigma noise-floor convention this harness's `gate_status()` implements, at the same `N` semantics (proportion out of total MC paths) Q-STATVALID-1 itself used. |
| `docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md` + `lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/run_w1_intraday_both_halves.py` | ADR `56663b2` 2026-08-22 · harness `027a729` 2026-08-14 | The citable prior art for "intraday-honest limb": pair `daily_pnl` with `intraday_low` via `paired_blocks_from_daily`, thread both through `run_tier_remc(..., intraday_blocks=...)`, never let the intraday channel be silently vacuous. This harness's `score_cell` follows the identical call shape. |
| `docs/adr/2026-08-13-implied-sr-report-only-fade-reopen.md` | `027a729` 2026-08-14 | First-consumer check (i) input — the reopened Tradeify-native fade design-region (§8 below). |
| `docs/superpowers/plans/2026-08-23-viable-strategy-phase-b-mechanism-supply.md` | `3ea7988` 2026-08-23 | First-consumer check (ii) input — Phase-B live card-precheck rows B1.4 / B2.3 (§8 below). B3 KILL at A1 (same day, earlier); not a live pre-check. |
| `lab/CATALOG.md` header + Active›c1 table | `c42e7e7` 2026-08-23 | Row format for this campaign's CATALOG entry. |

**Full-corpus search for the 2026-08-22 consistency-constraint quantification harness** (memory:
`project_tradeify_consistency_payoff_shape_constraint_2026_08_22`) — see §9 below for the
disclosed negative result; not repeated here.

---

## §1 — Parameter axes (coverage, not selection)

Four independent axes, pre-registered as coverage, not selection — no cell is pruned, ranked, or
selected as a recommendation anywhere in this document.

| Axis | Values | Source |
|---|---|---|
| Win rate | 40%, 45%, 50%, 55%, 60%, 65%, 70% | Task brief, literal |
| R-multiple shape | `symmetric`, `mild_right_skew`, `bounded_clustered` | Task brief, literal (§2 has the full generative definition) |
| Trades/week | 1, 2, 3, 5, 8 | Task brief, literal |
| Per-trade risk (1R, $) | $250, $275, $325 | **EM2's edge-indexed frontier, verbatim** (`docs/spec/2026-08-05-eval-mechanism-shape-screen.md` EM2 row) — never above the top published cell ($325), satisfying "interpolate down, never up." Used strictly as $-coverage levels; **not** a claim any real mechanism achieves 0.49R/0.65R/0.85R (that provenance is void per the 2026-08-08 ADR — see §0). |

7 × 3 × 5 × 3 = **315 tuples**, scored against **2 firms** (§5) = **630 cells**.

---

## §2 — Shape generative process (full disclosure)

`shape_generator.py` builds a synthetic per-trade R-multiple stream, places trades on fixed
weekdays, and composes a paired `(daily_pnl, intraday_low)` panel — **not** a strategy backtest;
a coverage instrument only.

**Per-trade R-multiple** (deterministic RNG per tuple, seed = `20260823 + tuple_index(...)`,
reproducible byte-for-byte):

| Shape | Win R | Loss R |
|---|---|---|
| `symmetric` | Uniform(0.7, 1.3) | −Uniform(0.7, 1.3) |
| `mild_right_skew` | 1.0 + Exponential(0.5) (mean 1.5R, right tail) | −Uniform(0.7, 1.3) |
| `bounded_clustered` | Uniform(0.9, 1.1) (tight) | **−1.0 exactly** (hard bound) |

**Intraday MAE** (the intraday-honest limb — never close-only): losing trades are modeled as
reaching, not slipping past, their hard stop (`MAE == realized loss`; no gap-through-stop tail is
modeled — a disclosed limitation, §11). Winning trades give back a shape-dependent fraction of one
stop before closing favorably: `symmetric` Uniform(0.20, 0.60)R, `mild_right_skew` Uniform(0.30,
0.80)R (wider — a "let it run" shape spends longer exposed), `bounded_clustered` Uniform(0.10,
0.30)R (tighter — the bounded-duration profile). A day with multiple trades (cadence=8) composes
its excursion **sequentially** across the day's trades (running cumulative P&L + each trade's own
MAE), never a naive independent sum — verified in `test_shape_generator.py`.

**Weekly placement** (deterministic, guarantees the activity floor structurally — §5.2):
cadence 1→Mon; 2→Mon,Wed; 3→Mon,Wed,Fri; 5→Mon–Fri; 8→Mon×2,Tue×2,Wed×2,Thu×1,Fri×1. Every
calendar week has ≥1 trade for every cadence tested, by construction.

**Base panel:** 520 synthetic weeks (2,600 business days) per tuple — the engine's own
block-bootstrap then draws 300 week-blocks (with replacement) per simulated 1,500-day path from
those 520, exactly the same mechanism `paired_blocks_from_daily` / `run_seed` use for a real
campaign's panel.

**Disclosed limitations (scope boundary, not a defect):** (1) gross of commission — `cost_per_side_usd`
is not netted into these R-multiples; cost-law (≥4× round-trip, EM1/Req-5) is a **separate,
already-existing gate** a real mechanism candidate must clear on its own measured cost basis, not
something this shape map folds in. (2) No gap-through-stop tail (EM3's own "5% of losses gap 5×"
finding is out of this generator's scope). (3) The DGP is not calibrated to any real instrument's
volatility or session structure — it is a payoff-shape abstraction, deliberately.

---

## §3 — Scoring methodology

Each of the 630 `(win_rate, shape, cadence, risk, firm)` cells is scored by:

1. `sg.build_panel(...)` → `(daily_pnl, intraday_low)`.
2. `paired_blocks_from_daily(...)` → paired week-blocks (frozen Phase-4 §1 invariant: both channels
   share one RNG draw at bootstrap time — never re-sampled independently).
3. The **identical primitive call sequence** `run_tier_remc` itself uses (`assert_engine_ready` →
   `firm_kwargs(firm, inactivity_off=True, consistency=<firm's own consistency_rule_pct/100>)` →
   `run_seed` per frozen seed → `summarize_outcomes`) — reimplemented at this one level only so
   `days_to_pass` (discarded by `run_tier_remc`'s own return dict) can be surfaced for §6's
   disclosure column. `simulate_path` / `run_seed` themselves are never touched.

**Gates, jointly, per cell:**

- **Trailing-DD bust ≤ 3.0%** — `summarize_outcomes`'s `headline_bust` (daily+static+trailing),
  on the **intraday-honest limb** (`intraday_blocks` threaded, never close-only).
- **P(pass) ≥ 50%** — `pass_rate`. The venue's **consistency rule is already embedded here**, not
  a separate column: `simulate_path` (L188-196) only returns `"pass"` once
  `max_day_profit ≤ consistency_frac × total_profit` — exactly the soft-gate "effective target
  `max($6,000, 2.5×best day)`" mechanic the EM screen doc describes (§0), including the
  early-path case (checked fresh, using the *current*, still-small `total_profit`, every day
  equity first crosses the nominal target).
- **Activity ≥1 trade/week** — satisfied **structurally**, by the weekly placement in §2, for
  **every** cadence value tested (1 through 8 all place ≥1 trade every calendar week). The
  operator token-trade path is not exercised or needed anywhere in this map; engine calls run
  `inactivity_off=True` (barrier-off), matching `prop_survivor_scoring.py`'s own convention.
- **Time-to-target** — `median_days_to_pass`, disclosure only, computed over the paths that
  actually passed (`n_passes_observed`); `None` where too few/no passes occurred.

**Statistical discipline (Q-STATVALID-1, binding):** each gate's proportion carries an
SE-of-proportion bar, `SE = sqrt(p(1-p)/N)`, at the **N actually used** for that cell
(`n_total_paths` = `sims_per_seed × 3` — never the abstract frozen 30,000 for cells run at the
reduced sweep N, §4). A cell is flagged `MARGINAL` on a gate if the gate line falls within `±2·SE`
of the measured proportion — **never reported as a clean PASS** in that case. The combined cell
verdict is `INFEASIBLE` if either gate clearly fails, `MARGINAL` if neither clearly fails but at
least one is within its 2σ band, else `FEASIBLE`. **No best cell is selected, reported, or ranked**
anywhere below.

---

## §4 — Compute budget (disclosed deviation from the frozen sims_per_seed)

**Operator acceptance (2026-08-24):** the disclosed `sims_per_seed=500` (N=1,500) reduction is accepted as the published region's N. Seeds `(42, 123, 2026)` and horizon `1500` stay frozen. This is not a frozen-N re-sweep and not a Phase B GO.

Measured this session, on this machine, at the frozen `sims_per_seed=10,000` (3 seeds × 10,000 =
30,000 paths, horizon 1,500), **uncontended** (isolated single-process timing, before any parallel
sweep was launched): **294.2s (`Tradeify_Select_100K`) and 309.7s (`MFFU_Rapid_100K`)**, same
tuple — a near-zero-edge corner (`win_rate=50%`, `symmetric`, cadence=1, risk=$275). A full
630-cell grid at ~300s/cell is **≈52.5 CPU-hours** — even at full 7-way parallelism across this
machine's 8 cores, **≈7.5 wall-clock hours**, outside this task's responsible compute budget
(Rule 2, `docs/adr/2026-06-16-rule-2-budget-before-acting.md`, CLAUDE.md §INQHIORI canon §15).
(For reference, the **same** cell re-measured later, under real 7-way contention from this
session's own parallel sweep, took 516.4s — contention roughly doubled the wall-clock cost of an
individual full-N call, which is exactly why the reduced-N sweep below still uses the isolated
figure as its budget baseline, not the contended one, when explaining the original 52.5 CPU-hour
estimate — CPU-hours, unlike wall-clock, are contention-invariant.)

**Decision (disclosed, not silent):** the frozen **seeds** `(42, 123, 2026)` and frozen **horizon**
`1500` are kept byte-identical to `load_scoring_thresholds()` throughout — untouched. The **only**
axis that moves is `sims_per_seed`, reduced to **500/seed (N=1,500 total)** for the primary
630-cell sweep — full axis coverage is preserved (zero cells dropped; "coverage, not selection" is
not narrowed), and every row discloses its own `n_total_paths` so the reader always knows which N
produced it. The consequence of the smaller N is **wider, honestly-computed** SE-of-proportion
bars (more cells legitimately land `MARGINAL`) — the opposite of the risk the frozen-N instruction
guards against (seed/N shopping for a favorable result): this is a uniform, symmetric,
pre-committed reduction applied to every cell alike, not a selective one.

**Cross-validation at the full frozen N:** a fixed 4-tuple × 2-firm reference subset (chosen for
corner coverage — near-zero-edge, expected-fast-pass, expected-fast-bust, mid-grid positive-skew —
**before** seeing sweep results, never for favorable agreement) was independently re-scored at the
full frozen `sims_per_seed=10,000` (`N=30,000`):

| Cell | Reduced-N sweep (`N=1,500`) | Full-N validation (`N=30,000`) | Verdict agree? |
|---|---|---|---|
| `wr0.50_symmetric_cd1_rk275` — both firms | bust 92.93%, pass 6.07% → `INFEASIBLE` | bust 92.93%, pass 5.93% → `INFEASIBLE` | **yes** |
| `wr0.70_bounded_clustered_cd8_rk250` — both firms | bust 0.07%, pass 99.93% → `FEASIBLE` | bust 0.07%, pass 99.93% → `FEASIBLE` | **yes** |
| `wr0.40_symmetric_cd8_rk325` — both firms | bust 99.93%, pass 0.07% → `INFEASIBLE` | bust 99.94%, pass 0.06% → `INFEASIBLE` | **yes** |
| `wr0.65_mild_right_skew_cd3_rk275` — both firms | bust 0.67%, pass 99.33% → `FEASIBLE` | bust 0.54%, pass 99.46% → `FEASIBLE` | **yes** |

**All 8 of 8 validation cells complete; all 8 agree with their sweep-N verdict** (4 tuples × 2
firms — firms agree with each other too, per §6.1). The reduced-N sweep's bust/pass point
estimates land within a few tenths of a percentage point of the full-N re-score in every case —
well inside the reduced-N SE bars themselves. This is the concrete evidence behind §4's claim that
the sweep-N reduction is a precision cost (wider bars), not an accuracy cost (the point estimates
track the frozen-N standard closely).

### §4.1 — MARGINAL-band cross-check (review fix, added 2026-08-23)

**Why this exists:** a reviewer pass on the initial publication noted that the 4-tuple/8-cell
`VALIDATION_CELLS` above are all far-from-gate corner cases, chosen for coverage diversity *before*
the sweep ran — none of them tested whether a cell landing `MARGINAL` under the reduced sweep-N
(`sims_per_seed=500`) would resolve to a clear `PASS`/`FAIL` (or stay `MARGINAL`) at the frozen full
N, which is exactly the risk the N-reduction introduces. This subsection closes that gap.

**Selection (post-sweep, by gate proximity, not by outcome):** of the 630 committed cells, 19
tuples (38 cells, identical across both firms per §6.1) landed `MARGINAL` — every one of them on
the **bust** gate specifically (`pass` is never within 2·SE of the 50% floor anywhere in this grid,
§6 throughout). 5 of the 19 were selected for full-N re-scoring, spanning all three shapes and both
sides of `DD_GATE=0.03` (reduced-N bust point estimate in parentheses): `symmetric` (2.27%),
`bounded_clustered` ×2 (2.40%, 3.60%), `mild_right_skew` ×2 (2.87%, 3.60%) — recorded in
`run_region_sweep.py`'s `MARGINAL_VALIDATION_CELLS` list and its own comment, re-stated here per the
same "checkable against the code's git history" discipline the paragraph above uses for
`VALIDATION_CELLS`. Re-scored via a new `--marginal-validation` CLI mode that mirrors
`--validation`'s call shape exactly (`simulate_path`/`run_seed` untouched, same as every other path
in this harness); raw output committed at
[`marginal_validation_data.jsonl`](marginal_validation_data.jsonl) (10 rows: 5 tuples × 2 firms).

| Cell | Reduced-N sweep (`N=1,500`) | Full-N validation (`N=30,000`) | Resolution |
|---|---|---|---|
| `wr0.65_symmetric_cd8_rk325` — both firms | bust 2.27% (`MARGINAL`) | bust 1.88% (`FEASIBLE`) | `MARGINAL` → `FEASIBLE` |
| `wr0.60_bounded_clustered_cd1_rk250` — both firms | bust 2.40% (`MARGINAL`) | bust 3.00% (`MARGINAL`) | stays `MARGINAL` (point estimate crosses the line — see below) |
| `wr0.50_mild_right_skew_cd2_rk250` — both firms | bust 2.87% (`MARGINAL`) | bust 3.04% (`MARGINAL`) | stays `MARGINAL` (point estimate crosses the line — see below) |
| `wr0.55_mild_right_skew_cd5_rk275` — both firms | bust 3.60% (`MARGINAL`) | bust 3.79% (`INFEASIBLE`) | `MARGINAL` → `INFEASIBLE` |
| `wr0.60_bounded_clustered_cd3_rk275` — both firms | bust 3.60% (`MARGINAL`) | bust 3.83% (`INFEASIBLE`) | `MARGINAL` → `INFEASIBLE` |

**Both firms remain bit-identical at full N on every one of these 5 tuples too** (verified directly
on the raw JSONL — e.g. `wr0.60_bounded_clustered_cd3_rk275`: both firms `bust=0.03826666666666667`
to full float precision) — the same pattern §6.1 already reports, not a separate new instance of it.
**Median days-to-pass also matched exactly between the reduced-N and full-N re-score for all 5
tuples** (33.0/33.0, 476.0/476.0, 146.0/146.0, 50.0/50.0, 146.0/146.0) — noted as an observation,
not chased further here (the mechanism was not separately verified and no claim is made about it).

**Reading, stated precisely:** 3 of the 5 `MARGINAL` tuples resolved to a clear verdict at full N
(1 `FEASIBLE`, 2 `INFEASIBLE`), each consistent with which side of the gate its own reduced-N point
estimate already leaned toward. 2 of the 5 remained `MARGINAL` at full N — and for those two, the
bust point estimate actually **crossed** the exact `0.03` line between the reduced-N and full-N
re-score (2.40%→3.00% and 2.87%→3.04%). That is not glossed over here: **2 of 5 point estimates
did land on the opposite side of the gate at full N than at reduced N.** What did not happen is a
*confident*-verdict flip — `gate_status()`'s own SE-of-proportion band correctly kept both cells
`MARGINAL` at both N's rather than reporting a false confident `FEASIBLE`/`INFEASIBLE` on either
side. This is the calibration working as intended: a point estimate this close to a gate line is
expected to wobble across it between two different finite-N draws, and the honest response is
exactly what happened — stay `MARGINAL`, not report a coin-flip as a verdict.

**Scope, stated plainly:** because every tuple in this subset was selected *for* landing `MARGINAL`
at reduced N, this check cannot — by construction — test the specific failure mode of "a confident
`FEASIBLE`/`INFEASIBLE` verdict at reduced N flips to the opposite confident verdict at full N."
That is what the original 8-cell corner-case subset above already tests (8/8 agree, unchanged by
this addition). What this subsection adds: no clearly-`FEASIBLE` or clearly-`INFEASIBLE` reduced-N
cell in this grid has now been shown to hide a `MARGINAL`-band full-N surprise near a gate boundary
— the region most at risk from the N-reduction was checked, not just asserted safe by analogy to
the corner cases.

---

## §5 — Firms scored

- **`Tradeify_Select_100K`** — deployment venue. Model repaired: W1 intraday-honest method
  (`docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md`) + the 2026-08-04 eval-lock fix
  (`dd_lock_offset_usd` unreachable, the production default this harness never overrides).
- **`MFFU_Rapid_100K`** — engine-faithful `trailing_locking` (same barrier code path as Tradeify;
  identical $3,000/$100K trail geometry, different consistency 50.0% and `min_trading_days` 2).
- **`Bulenox_100K` / `BluSky_Premium_100K` — BLOCKED, not silently absent.** Per the
  `Q-FIRMEOD-1` closure (`FALSIFIED`, §0): Bulenox's own `trailing` CLOCK flips intraday-honest
  and carries an unresolved LOCK-language finding; BluSky's CLOCK is untested. **No Bulenox/BluSky
  bust-rate figure may be produced for this cross-firm map** until the named successor (a
  W1-pattern intraday-honest re-run across all 7 tiers, and/or resolution of the Bulenox
  lock-scope question) lands. This harness contains **zero** Bulenox/BluSky scoring calls — the
  block is structural, not a redacted column.

---

## §6 — Region tables

Full raw data (all 630 rows, one JSON object per line): [`region_data.jsonl`](region_data.jsonl).
Every row carries `n_total_paths`, `se_bust`, `se_pass`, `bust_status`, `pass_status`, `verdict`,
`expectancy_r` (disclosure-only MC estimate of the tuple's own per-trade R edge),
`median_days_to_pass`.

### §6.1 — Verdict counts by shape × firm

**`Tradeify_Select_100K` and `MFFU_Rapid_100K` are bit-identical on every one of the 315 tuples
tested** — verified directly on the raw JSONL (e.g. `wr0.55_mild_right_skew_cd2_rk275`: both firms
`pass_rate=0.9866666666666667` to full float precision). This is a real, checked finding, not a
harness bug: the two tiers' geometry differs only in `consistency_rule_pct` (40.0 vs 50.0) and
`min_trading_days` (3 vs 2) — bust never depends on consistency at all (§3), `min_trading_days`
is already satisfied for every tuple in this grid by the time any path is near its profit target
(the grid's own minimum median days-to-pass is **16.0** — `wr0.70_mild_right_skew_cd8_rk325`, both
firms tied at that value — computed directly from `region_data.jsonl`'s 590 non-null
`median_days_to_pass` rows, not eyeballed from a heatmap; §6.2's tables carry bust/pass % only, not
days-to-pass, so that number is never itself a §6.2 citation. 16.0 is still comfortably above
`min_trading_days` 3 (Tradeify) / 2 (MFFU) — the argument this parenthetical supports holds at the
correct number, it just isn't "~30"), and **none of this map's three shape archetypes
ever produces a single day whose profit share falls in the narrow (40%, 50%] band** that would be
the only way the two firms' consistency thresholds could diverge. Put differently: **this map's
own numbers show the consistency rule is not the binding constraint for any of the three shapes
tested here** — it would plausibly start to matter for a *more* concentrated/pyramided shape than
any tested (consistent with, and now independently quantifying from scratch, the qualitative
pattern the un-locatable 2026-08-22 session's real-backtest finding described — §9). Counts below
are therefore reported once per shape (identical for both firms):

| Shape | `FEASIBLE` | `MARGINAL` | `INFEASIBLE` | (of 105 cells: 7 win rates × 5 cadences × 3 risk levels) |
|---|---:|---:|---:|---|
| `symmetric` | 23 | 4 | 78 | |
| `mild_right_skew` | 45 | 8 | 52 | |
| `bounded_clustered` | 26 | 7 | 72 | |

`mild_right_skew` clears roughly double the `symmetric`/`bounded_clustered` share of the grid —
see §7 for why.

### §6.2 — Heatmaps at risk = $275 (the middle EM2 cell)

Cell = `verdict (bust%, pass%)`. `MARGINAL` means within 2σ of a gate line — **not** a pass. One
table per shape (firms identical, §6.1).

#### `symmetric` (risk=$275)

| win rate \ cadence(/wk) | 1 | 2 | 3 | 5 | 8 |
|---|---|---|---|---|---|
| 40% | INFEASIBLE (100.0%, 0.0%) | INFEASIBLE (100.0%, 0.0%) | INFEASIBLE (99.9%, 0.1%) | INFEASIBLE (100.0%, 0.0%) | INFEASIBLE (100.0%, 0.0%) |
| 45% | INFEASIBLE (99.5%, 0.4%) | INFEASIBLE (99.7%, 0.3%) | INFEASIBLE (99.3%, 0.7%) | INFEASIBLE (97.6%, 2.4%) | INFEASIBLE (99.1%, 0.9%) |
| 50% | INFEASIBLE (92.9%, 6.1%) | INFEASIBLE (83.5%, 16.5%) | INFEASIBLE (78.7%, 21.3%) | INFEASIBLE (81.9%, 18.1%) | INFEASIBLE (87.5%, 12.5%) |
| 55% | INFEASIBLE (88.2%, 9.9%) | INFEASIBLE (39.3%, 60.7%) | INFEASIBLE (35.5%, 64.5%) | INFEASIBLE (52.7%, 47.3%) | INFEASIBLE (44.7%, 55.3%) |
| 60% | INFEASIBLE (27.2%, 71.7%) | INFEASIBLE (21.8%, 78.2%) | INFEASIBLE (8.8%, 91.2%) | INFEASIBLE (12.7%, 87.3%) | INFEASIBLE (11.1%, 88.9%) |
| 65% | INFEASIBLE (4.1%, 95.9%) | INFEASIBLE (4.5%, 95.5%) | **FEASIBLE** (1.7%, 98.3%) | **FEASIBLE** (1.1%, 98.9%) | MARGINAL (2.7%, 97.3%) |
| 70% | **FEASIBLE** (0.3%, 99.7%) | **FEASIBLE** (0.2%, 99.8%) | **FEASIBLE** (0.6%, 99.4%) | **FEASIBLE** (0.0%, 100.0%) | **FEASIBLE** (0.2%, 99.8%) |

#### `mild_right_skew` (risk=$275)

| win rate \ cadence(/wk) | 1 | 2 | 3 | 5 | 8 |
|---|---|---|---|---|---|
| 40% | INFEASIBLE (84.8%, 15.2%) | INFEASIBLE (74.9%, 25.1%) | INFEASIBLE (86.7%, 13.3%) | INFEASIBLE (90.4%, 9.6%) | INFEASIBLE (84.7%, 15.3%) |
| 45% | INFEASIBLE (42.2%, 57.7%) | INFEASIBLE (44.2%, 55.8%) | INFEASIBLE (49.7%, 50.3%) | INFEASIBLE (51.9%, 48.1%) | INFEASIBLE (40.3%, 59.7%) |
| 50% | INFEASIBLE (8.8%, 91.2%) | INFEASIBLE (23.1%, 76.9%) | INFEASIBLE (26.2%, 73.8%) | INFEASIBLE (15.3%, 84.7%) | INFEASIBLE (20.7%, 79.3%) |
| 55% | INFEASIBLE (7.6%, 92.4%) | **FEASIBLE** (1.3%, 98.7%) | MARGINAL (2.6%, 97.4%) | MARGINAL (3.6%, 96.4%) | MARGINAL (2.4%, 97.6%) |
| 60% | **FEASIBLE** (1.1%, 98.9%) | **FEASIBLE** (2.1%, 97.9%) | **FEASIBLE** (1.6%, 98.4%) | **FEASIBLE** (1.4%, 98.6%) | **FEASIBLE** (0.6%, 99.4%) |
| 65% | **FEASIBLE** (0.3%, 99.7%) | **FEASIBLE** (0.1%, 99.9%) | **FEASIBLE** (0.7%, 99.3%) | **FEASIBLE** (0.1%, 99.9%) | **FEASIBLE** (0.1%, 99.9%) |
| 70% | **FEASIBLE** (0.0%, 100.0%) | **FEASIBLE** (0.1%, 99.9%) | **FEASIBLE** (0.1%, 99.9%) | **FEASIBLE** (0.0%, 100.0%) | **FEASIBLE** (0.0%, 100.0%) |

#### `bounded_clustered` (risk=$275)

| win rate \ cadence(/wk) | 1 | 2 | 3 | 5 | 8 |
|---|---|---|---|---|---|
| 40% | INFEASIBLE (100.0%, 0.0%) | INFEASIBLE (99.9%, 0.1%) | INFEASIBLE (100.0%, 0.0%) | INFEASIBLE (100.0%, 0.0%) | INFEASIBLE (99.9%, 0.1%) |
| 45% | INFEASIBLE (99.9%, 0.1%) | INFEASIBLE (99.7%, 0.3%) | INFEASIBLE (99.6%, 0.4%) | INFEASIBLE (99.9%, 0.1%) | INFEASIBLE (98.7%, 1.3%) |
| 50% | INFEASIBLE (82.9%, 14.1%) | INFEASIBLE (95.4%, 4.6%) | INFEASIBLE (85.1%, 14.9%) | INFEASIBLE (84.3%, 15.7%) | INFEASIBLE (93.2%, 6.8%) |
| 55% | INFEASIBLE (27.9%, 71.3%) | INFEASIBLE (38.3%, 61.7%) | INFEASIBLE (35.5%, 64.5%) | INFEASIBLE (31.0%, 69.0%) | INFEASIBLE (34.5%, 65.5%) |
| 60% | INFEASIBLE (5.6%, 94.3%) | INFEASIBLE (5.9%, 94.1%) | MARGINAL (3.6%, 96.4%) | INFEASIBLE (10.5%, 89.5%) | INFEASIBLE (5.1%, 94.9%) |
| 65% | **FEASIBLE** (2.0%, 98.0%) | **FEASIBLE** (1.6%, 98.4%) | **FEASIBLE** (1.0%, 99.0%) | **FEASIBLE** (0.7%, 99.3%) | **FEASIBLE** (0.9%, 99.1%) |
| 70% | **FEASIBLE** (0.1%, 99.9%) | **FEASIBLE** (0.3%, 99.7%) | **FEASIBLE** (0.1%, 99.9%) | **FEASIBLE** (0.3%, 99.7%) | **FEASIBLE** (0.1%, 99.9%) |

### §6.3 — Risk sensitivity ($250 vs $325)

Lowest win rate on the axis with **at least one** `FEASIBLE` cell (any cadence), by shape and risk
— monotonic in the expected direction (lower $-risk ⇒ more R's fit inside the fixed $3,000 rope ⇒
a lower win rate can still clear it):

| Shape | $250 | $275 | $325 |
|---|---|---|---|
| `symmetric` | 65% | 65% | 65% |
| `mild_right_skew` | 55% | 55% | 60% |
| `bounded_clustered` | 60% | 65% | 70% |

`bounded_clustered` is the **most risk-sensitive** shape (its floor moves a full 10 points across
the EM2 range) — consistent with §7's reading that its tight win-clustering only helps DD survival
at the margin; it has no larger-mean-win cushion to absorb a bigger `$`/trade. `mild_right_skew`
is the **least** risk-sensitive (only symmetric's floor is flatter, and only because it is already
pinned at 65% by cadence 3+ at every risk level tested).

---

## §7 — One-page reading: what shape must a mechanism produce

**1. The trailing-DD bust gate binds harder than the pass floor through most of the grid's
transition zone** — many cells clear `P(pass)≥50%` comfortably while still failing the bust
ceiling by a wide margin (e.g. `symmetric`/`win_rate=55%`/cadence=3/risk=$275: pass 64.5%, bust
35.5%). A mechanism aimed only at "will it eventually reach the target more often than not" is
answering the wrong question for this venue — the $3,000 fixed rope, not the $6,000 target, is
what a real candidate has to survive first.

**2. No cell at win_rate ≤ 50% is `FEASIBLE`, for any shape, cadence, or EM2 risk level tested.**
⚠ **SCOPED 2026-08-24 — true for the $3,000 Select/MFFU rope only.** `Tradeify_Growth_100K`'s $3,500 rope makes `mild_right_skew`/cd2/$250 `FEASIBLE` at `win_rate=50%` (bust 1.17% at the full frozen N). Read this claim as a property of the rope, not of the venue class — see §13.2.
The floor sits at 55%–70% depending on shape (§6.3). A mechanism whose own measured edge implies a
win rate at or below breakeven-ish territory cannot be rescued by this venue's activity/consistency
mechanics alone, regardless of how it trades cadence or sizes within the EM2 frontier.

**3. Mean per-trade edge, not "low skew" per se, is what separates the shapes.** `mild_right_skew`
clears the most cells (45/105 vs 26/105 `bounded_clustered` and 23/105 `symmetric`) and at the
lowest win-rate floor (55% vs 60–70%) — **because its mean win (1.5R) is larger at every matched
win rate, not because it is "skewed."** `bounded_clustered`'s tight win-clustering and hard-capped
loss give a real but **secondary** DD-survival benefit (visible at the margin — e.g. it reaches
`MARGINAL` at 60%/cadence=3 where `symmetric` is still clearly `INFEASIBLE` at the same win
rate/cadence) — but tightness alone, without also raising the mean win size, does **not** unlock a
materially lower win-rate requirement than `symmetric` carries. **Caveat, stated plainly**: none of
this map's three shapes tests a *more* extreme skew than `mild_right_skew`'s (mean win 1.5R, one
Exponential(0.5) tail) — this region says nothing about whether a strongly pyramided, "let it run
to 5R+" shape (closer to the real Striker legs the 2026-08-22 memory examined) would keep climbing
or start losing ground to the consistency/DD interaction at some point past what was tested here.

**4. Cadence is a second-order lever inside this map, not the primary one.** Within any fixed
(shape, win_rate, risk) row, moving from 1 to 8 trades/week shifts bust/pass by single-digit-to-
low-double-digit percentage points, rarely enough by itself to flip a clearly-`INFEASIBLE` cell to
`FEASIBLE` — the dominant axis is win rate (§6.2 tables read almost entirely by row, not by
column). Practically: **a mechanism does not buy its way to this venue's feasible region mainly by
trading more often** — activity above the structural 1/week floor (§3) has real but modest
leverage here.

**5. Per-trade risk (the EM2 axis) matters, but less than win rate.** Moving the full EM2 range
($250→$325) shifts a shape's win-rate floor by 0–10 points (§6.3) — real, and worth a mechanism
sizing conservatively where it can, but not a substitute for edge.

**Bottom line for Phase B:** source for a mechanism whose own measured win rate is comfortably
above ~55–60% (higher if its average win is not clearly larger than its average loss), with a
per-trade dollar risk sized at or below the EM2 frontier for its own measured edge — cadence and
shape-tightness help at the margin but cannot substitute for that win-rate floor on this venue's
$3,000-rope / $6,000-target geometry.

---

## §8 — First consumers (run immediately, per task brief)

### (i) Re-check the reopened Tradeify-native fade geometry

`docs/adr/2026-08-13-implied-sr-report-only-fade-reopen.md` reopened the Tradeify-native fade
design-region (`CONFIG-B-MCL`, `rr ∈ {0.66, 1.0}`, pinned `p=0.65`, `n=4–6` trades **per day** —
`lab/analysis/c1/tradeify_fade_stage0_2026-07-30/RESULTS.md` §1) as **geometry-open, not an
admitted mechanism**.

The fade's two published `rr` cells, at its own pinned `p=0.65`, read very differently against
this region:

- **`rr=1.0`** (win ≈ loss magnitude) structurally matches this map's `bounded_clustered` shape
  (win R centered at 1.0, loss capped at exactly −1.0). At `win_rate=65%`, risk=$275,
  `bounded_clustered` is **`FEASIBLE` at every cadence tested (1 through 8/week)** — bust 0.7–2.0%,
  pass 98.0–99.3% (§6.2 table). A comfortable clearance.
- **`rr=0.66`** has no direct shape/win-rate match in this grid (no tested shape has a mean win
  below 1.0R with the loss still capped at exactly −1.0R), but its **expectancy** (`0.65×0.66 −
  0.35×1 ≈ +0.079R`) sits close to `bounded_clustered`'s own `win_rate=55%` cell
  (`expectancy_r ≈ +0.0999R`, computed by `shape_generator.expectancy_r`) — using edge, not the
  win-rate/shape label, as the comparable quantity. At **that** expectancy level, this map's own
  `bounded_clustered@55%` row is **solidly `INFEASIBLE` at every cadence** (bust 27.9–38.3%, ~10×
  over the ceiling) **despite comfortably clearing the pass floor** (61.7–71.3% pass) — the same
  "bust gate binds harder than pass floor" pattern from §7.1, concretely illustrated: the *same*
  0.65 win rate, differing only in whether the average win is 0.66R or a full 1.0R, is the
  difference between comfortably-`FEASIBLE` and solidly-`INFEASIBLE` in this region.

**Cadence caveat, stated plainly:** the fade's own real cadence (`n=4–6` trades **per day** — i.e.
roughly 20–30/week if traded daily) sits entirely outside this map's tested range (max 8/week);
this check cannot literally score that density. §7 finding 4 (cadence is a second-order lever
relative to win-rate/shape inside this map) suggests the reading above is unlikely to be
overturned by cadence alone, but that is an **extrapolation past the tested range, not a measured
result** — disclosed as such, not silently assumed.

**Net:** consistent with the ADR's own framing (a reopened design-**region**, not an admitted
mechanism), this check does not admit or reject the fade geometry — it locates its two published
`rr` cells against a now-quantified region and finds they sit on opposite sides of this venue's DD
gate at the *same* win rate, for the reason §7 already names (mean edge, not win rate alone).

### (ii) Confirm legibility for Phase-B candidate pre-checks

`docs/superpowers/plans/2026-08-23-viable-strategy-phase-b-mechanism-supply.md` names each *live*
lane's own card-precheck row (B1.4 / B2.3) as the point where a candidate's predicted shape is
checked against this region — **that check is each lane's own job, not this document's**; the
brief for A2 asks only that the region's axes be legible/usable for that purpose. Confirmed:

- **B1 (MOC-imbalance wake, MES)** — its own row already commits to a predicted shape: *"bounded
  window, clustered wins, ~2–4 events/week."* That maps directly onto this map's axes:
  `shape=bounded_clustered`, `cadence∈{2,3}` (the nearest grid points to "2–4/week"). **Legible: a
  direct grid lookup is possible once B1 also commits to a win-rate assumption** (not yet stated in
  the plan doc) — see §6.2's `bounded_clustered` tables. Concretely, at risk=$275 those two columns
  already show the floor B1's own eventual win-rate measurement will be read against: cadence=2
  needs `win_rate≥65%` to clear `FEASIBLE`; cadence=3 needs `≥65%` clean or `60%` `MARGINAL`.
- **B2 (London-fix wake)** — its row states only *"shape pre-check against the A2 region"*, without
  yet committing to a shape adjective or a win-rate assumption. **Legible but not yet actionable**:
  this map's three shape buckets and 7-point win-rate axis are ready to receive B2's own
  precheck once B2.0/B2.1 clear and a predicted shape is named — A2 does not supply that
  assumption on B2's behalf.
- **B3 (buyback-blackout abstention) — KILL, not a live pre-check.** A1 audit §6 (2026-08-23,
  earlier the same day this RESULTS was authored) ruled B3 **KILL** (POWER class, category-inherited
  from F5/D3). Phase B proceeds with B1/B2 only. The cadence observation below is **historical** —
  it is not a live card-precheck. The plan's own sleeve note ("clustered frequency cannot satisfy
  the activity rule alone") was **consistent with** (not contradicted by) this map's cadence axis
  starting at 1/week; that consistency does not reopen the kill. Re-proposal: a materially different
  magnitude argument than F5's three failed instances — [`A1 §6`](../../../../docs/notes/audits/2026-08-23-kill-register-attribution-audit.md).

---

## §9 — AMBIGUOUS-HOLD disclosure: 2026-08-22 committed harness not located

Per the task brief's own named condition (Gate A2: *"AMBIGUOUS-HOLD if the consistency-engine
harness cannot be located and would need re-derivation"*), a real search was run for a committed
harness from the 2026-08-22 session that quantified (against real Striker DJ30/MYM and
NAS100/MNQ backtests) why pyramided/skewed payoffs structurally fail Tradeify's 40%-per-day
consistency rule (memory: `project_tradeify_consistency_payoff_shape_constraint_2026_08_22`):

- `grep -ri "consistency_frac"` across the repo — every hit is either this harness, `core/mc/*`,
  or an unrelated pre-existing campaign (list in the audit note, §0).
- Content search for the memory's own specific numbers (`17 months`, `13 months`, `8.3 months`,
  `39.1%`, `47.8%`, `rolling eval-start`) — **zero hits anywhere in the tracked tree.**
- `lab/analysis/c1/` directory listing — **no slug dated `2026-08-21` or `2026-08-22` exists at
  all** (dates jump `..._2026-08-20` → `..._2026-08-23`).
- `docs/SESSIONS.md` 2026-08-22 entries — none reference a Striker rolling-eval-start consistency
  study.

**Disposition:** the harness does not exist as a committed artifact — it was very likely a
one-off, uncommitted script (exactly the scenario the task brief itself anticipated). This is
reported as the AMBIGUOUS-HOLD condition for that **narrow** sub-question, per
`lesson_unpriced_branch_search_the_corpus` (escalate the absence, do not silently rebuild it).
**It does not block the rest of A2**: the task's own "Engine reuse" bullet separately names three
other, independently-confirmed-present reuse targets (`simulate_path`, `firm_kwargs`,
`load_scoring_thresholds`), which are exactly what §3 above builds on. The 2026-08-22 session's
specific numbers are **not cited anywhere in this document** as a result (per the task brief's own
instruction) — they were used only as informal background while choosing the three shape
archetypes in §2 (a pyramided/skewed shape should score worse against the consistency-embedded
pass gate than a clustered/low-skew one; §6/§7 report whether this map's own, independently-run
numbers show that same qualitative pattern).

---

## §10 — Forbidden-moves self-check

| Forbidden move (task brief) | Compliance |
|---|---|
| Selecting/ranking cells | No ranking anywhere; §6 reports the full grid, unfiltered |
| Treating `MARGINAL` as `PASS` | `gate_status()` returns `MARGINAL` explicitly; `combine_verdict` never collapses it into `FEASIBLE` |
| Quoting any Bulenox/BluSky number | Zero scoring calls against those firm keys anywhere in the harness |
| Re-picking seeds/horizon | `seeds`/`horizon` asserted against `load_scoring_thresholds()` at every invocation (§3); only `sims_per_seed` moves, disclosed §4 |
| Letting the synthetic process become a strategy pitch | No mechanism, instrument, or entry rule is named anywhere in this document — the process prices *shapes*, not signals |

---

## §11 — Limitations (restated, consolidated)

1. Gross of commission (§2). 2. No gap-through-stop tail (§2). 3. DGP not calibrated to any real
instrument (§2). 4. Reduced-N sweep (§4) — wider SE bars than the frozen 30,000-path standard;
mitigated by the full-N corner-case validation subset (§4) **and** the full-N MARGINAL-band
validation subset (§4.1) — 2 of the 19 MARGINAL tuples in the committed sweep remain `MARGINAL`
even at the frozen full N (§4.1), which is the honest, expected behavior for a point estimate
genuinely close to the gate line, not an unmitigated gap. 5. EM2's $ cells are frontier
**arithmetic**, not a provenance claim about any real R (§0/§1). 6. B1/B2 first-consumer checks
(§8) are only as complete as those lanes' own not-yet-fully-specified predicted shapes. 7. The
original 8-cell corner-case validation subset's raw per-path output (§4) was never committed as a
JSONL — only narrated in its table — unlike §4.1's `marginal_validation_data.jsonl`; not
re-run/backfilled by the review-fix pass (§12) since the finding it addresses was scoped to
MARGINAL-band coverage, not corner-case reproducibility.

---

## §12 — Fix report — review response (2026-08-23)

A reviewer pass on the initial publication (commits `22c57a1` + `702f19a`) surfaced three findings.
All three are addressed **in place**, at the point the reader encounters the original claim — not
as a disconnected addendum — per this repo's own standing lesson that corrections belong where they
are read. Summary; full narrative lives at each fix's own location:

1. **§6.1's days-to-pass claim was false, not just imprecise.** The initial text read "median
   days-to-pass is never below ~30, §6.2." The actual minimum, computed directly from the committed
   `region_data.jsonl`, is **16.0** (`wr0.70_mild_right_skew_cd8_rk325`, both firms). §6.1 is
   corrected in place to state 16.0, with the correct citation (the raw JSONL — §6.2's own tables
   carry bust/pass % only, never days-to-pass) and a re-check that the underlying argument
   (`min_trading_days` clears well before any path nears its target) still holds at the correct
   number — it does, by a wide margin (16.0 vs. `min_trading_days` 2–3).
2. **The full-N validation subset never tested a `MARGINAL` cell.** §4's original 8 cells were all
   far-from-gate corner cases, chosen for coverage diversity before the sweep ran, so none tested
   whether a `MARGINAL` verdict under the reduced sweep-N would resolve differently at full N — the
   specific risk the N-reduction introduces. New §4.1 re-scores 5 additional tuples (10 cells),
   selected by gate proximity from the sweep's own 19 `MARGINAL` tuples, at the full frozen
   `sims_per_seed=10,000`, committed at `marginal_validation_data.jsonl`. Result: 3/5 resolve to a
   clear verdict consistent with their reduced-N lean, 2/5 remain honestly `MARGINAL` (their point
   estimates cross the exact gate line between N's, and the SE-of-proportion band correctly keeps
   both `MARGINAL` rather than reporting a false confident verdict), 0/5 show a confident-verdict
   flip. Harness change: `run_region_sweep.py` gained a `MARGINAL_VALIDATION_CELLS` list and a
   `--marginal-validation` CLI mode mirroring `--validation`'s call shape exactly
   (`simulate_path`/`run_seed` untouched).
3. **The audit note quoted the plan's `AUTHORIZATION` line incompletely and overclaimed independent
   corroboration.** `docs/notes/audits/2026-08-23-shape-feasibility-map-audit.md` omitted the plan
   doc's "not yet given" clause and treated a sibling artifact's self-reported byline as independent
   operator confirmation of a GO — neither holds up. Self-review item 1 is corrected to quote the
   line in full and to state plainly that no first-party evidence in this tree confirms a GO for
   A1/A2; the same correction is promoted to a new Concerns item 1 for prominence. This RESULTS.md
   never itself quoted the `AUTHORIZATION` line (confirmed by direct grep of the pre-fix text — no
   `AUTHORIZATION`/`GO` reference existed here), so no separate RESULTS.md edit was needed for this
   finding beyond this entry.

**Considered and not done:** re-running the original 8-cell corner-case subset to backfill a
committed raw JSONL for it (§11 item 7) — out of scope for the findings above, which concerned
MARGINAL-band coverage and two text-accuracy defects, not that subset's own reproducibility;
flagged rather than done silently.

**Verification of this fix pass:** `test_shape_generator.py` re-run 14/14 passing (unaffected — no
change to `shape_generator.py`); `run_region_sweep.py` re-compiled clean
(`python -m py_compile`) and its new `--marginal-validation` CLI path was not merely written but
**actually executed** for all 10 new cells (raw output in `marginal_validation_data.jsonl`, greppable
against §4.1's table); the corrected minimum days-to-pass (16.0) and the AUTHORIZATION full-line
quote were each independently re-derived from source (the committed JSONL; the plan doc itself) in
this fix pass, not copied from the reviewer's own finding text. See the Verification section below
for the exact commands.

---

## Gate (A2)

**`RESOLVED`** — per the task brief's own criteria: the region is published with SE-of-proportion
bars (§3/§6) and both first-consumer checks are recorded (§8). The `FALSIFIED (design)` disjunct
does not fire — the region is **not** empty at every tuple; it is `FEASIBLE` at every cadence and
risk level tested once win rate reaches ~65–70% (§6.2). The narrow AMBIGUOUS-HOLD condition (§9)
fired on one sub-question only (a possible prior committed harness) and, per the task brief's own
framing plus this repo's own precedent for exactly this shape of finding (`Q-STATVALID-1`'s
closure: *"an unlocatable-data limb converts that limb to an absence-finding; it does not override
a decisive [verdict] already reached [elsewhere]"*), does not override the top-level `RESOLVED`
disposition — it is carried forward as its own disclosed, non-blocking finding.

---

## Verification

```bash
# Harness invariant tests
python -m pytest lab/analysis/c1/shape_feasibility_map_2026-08/test_shape_generator.py --import-mode=importlib -q

# Frozen-value self-check (fails loudly if the pre-reg's ceiling/floor ever drifts)
python lab/analysis/c1/shape_feasibility_map_2026-08/run_region_sweep.py --shard-index 0 --n-shards 630 --n-sims 10 --out /tmp/smoke.jsonl

# Row count == 630, zero duplicate cell_ids, zero missing cells
python lab/analysis/c1/shape_feasibility_map_2026-08/analyze_region.py --shards-dir <shards-dir> --out-merged lab/analysis/c1/shape_feasibility_map_2026-08/region_data.jsonl

# Bulenox/BluSky are structurally absent, not redacted
grep -c "Bulenox\|BluSky" lab/analysis/c1/shape_feasibility_map_2026-08/run_region_sweep.py
# Expected: 0 (both firm keys never appear in the scoring code)

# --- Review-fix pass (§12), re-run this session ---

# Corrected minimum median_days_to_pass (§6.1) -- computed fresh from the committed JSONL
python -c "import json; vals=[json.loads(l).get('median_days_to_pass') for l in open('lab/analysis/c1/shape_feasibility_map_2026-08/region_data.jsonl', encoding='utf-8')]; vals=[v for v in vals if v is not None]; print(min(vals), len(vals))"
# Expected: 16.0 590

# MARGINAL-band validation subset (§4.1) -- row count == 10, all from MARGINAL_VALIDATION_CELLS
python -c "import json; rows=[json.loads(l) for l in open('lab/analysis/c1/shape_feasibility_map_2026-08/marginal_validation_data.jsonl', encoding='utf-8')]; print(len(rows)); print(sorted(r['verdict'] for r in rows))"
# Expected: 10 ['FEASIBLE', 'FEASIBLE', 'INFEASIBLE', 'INFEASIBLE', 'INFEASIBLE', 'INFEASIBLE', 'MARGINAL', 'MARGINAL', 'MARGINAL', 'MARGINAL']

# --marginal-validation CLI mode compiles and is wired (does not itself re-run the full-N sims)
python -m py_compile lab/analysis/c1/shape_feasibility_map_2026-08/run_region_sweep.py
python lab/analysis/c1/shape_feasibility_map_2026-08/run_region_sweep.py --help | grep -A1 "marginal-validation"

# AUTHORIZATION line -- confirm the audit note now quotes it in full
grep -c "not yet given" docs/notes/audits/2026-08-23-shape-feasibility-map-audit.md
# Expected: >= 1
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-23 | Initial authoring — harness, 630-cell region sweep, validation subset, first-consumer checks | Claude Code (Sonnet 5) |
| 2026-08-23 | Review-fix pass (§12): corrected the false §6.1 days-to-pass minimum (~30 → verified 16.0); added §4.1 MARGINAL-band full-N validation subset (`--marginal-validation` CLI mode, `marginal_validation_data.jsonl`, 10 new cells); updated Status line, §11 Limitations, Verification | Claude Code (Sonnet 5) |
| 2026-08-24 | §8 (ii) / §0: B3 dropped as a live card-precheck (A1 KILL same day, earlier); cadence note kept as historical. B1.4 / B2.3 remain the live pre-check rows | Cursor (surface-consistency Packet 2) |
| 2026-08-24 | §4 N-reduction operator-accepted as the published region's N (Packet 0). Status + §4 point-of-read note. Sweep bytes unchanged | Cursor (surface-consistency Packet 0) |

---

<!-- GROWTH-SECTION-START -->

## §13 — Growth-tier re-score (2026-08-24): the rope, isolated

**What changed:** `Tradeify_Growth_100K` added to `core/firm_rules.py` (primary source:
help.tradeify.co art. 10495915, article-dated 2026-06-05, read in-browser 2026-08-24) and to this
harness's `FIRM_KEYS`. The 315 tuples were re-scored against it at the same reduced
`sims_per_seed=500`, same frozen seeds `(42, 123, 2026)`, same frozen horizon `1500`, same
intraday-honest limb. **Select and MFFU were not re-run** — their 630 committed rows are carried
forward byte-identically and re-verified below.

**Why this tier:** Growth is a controlled contrast to Select. Same $6,000 target, same 80-micro
cap, same $0.91/side, same fixed-$ EOD-ratcheting trail geometry. Three things differ:
**$3,500 rope vs $3,000** (+16.7%), **no consistency rule** (vs 40%), and **min_trading_days 1**
(vs 3). §7.1 identified the rope as the binding gate and §6.1 found the consistency rule never
binds — so this tier is close to a clean isolation of the rope term.

### §13.1 — Verdict counts and transitions (315 paired cells)

| Firm | FEASIBLE | MARGINAL | INFEASIBLE |
|---|---:|---:|---:|
| `Tradeify_Select_100K` | 94 | 19 | 202 |
| `Tradeify_Growth_100K` | 120 | 12 | 183 |

| Transition (Select → Growth) | cells |
|---|---:|
| INFEASIBLE → INFEASIBLE | 183 |
| FEASIBLE → FEASIBLE | 94 |
| MARGINAL → FEASIBLE **(better)** | 19 |
| INFEASIBLE → MARGINAL **(better)** | 12 |
| INFEASIBLE → FEASIBLE **(better)** | 7 |

**38 cells improve, 277 unchanged, 0 degrade.** The monotonicity is a sanity check, not a
finding: a strictly wider rope on otherwise identical geometry cannot make any path worse, and
the engine agrees on all 315 cells.

### §13.2 — The win-rate floor moves 5 points for two of three shapes

| Shape | Select floor | Growth floor |
|---|---|---|
| `symmetric` | **65%** | **60%** |
| `mild_right_skew` | **55%** | **50%** |
| `bounded_clustered` | **60%** | **60%** |

⚠ **This falsifies §7.2's claim as written.** §7.2 states: *"No cell at win_rate ≤ 50% is
`FEASIBLE`, for any shape, cadence, or EM2 risk level tested."* That held for the two firms then
scored. It does **not** hold for Growth: `mild_right_skew` / cadence 2 / $250 is `FEASIBLE` at
`win_rate=50%` with bust **0.93%** (reduced N) / **1.17%** (full frozen N=30,000) against the
3.0% ceiling — the same cell where Select sits at **2.87%** / **3.04%** (`MARGINAL`).
The §7.2 sentence should be read as scoped to the $3,000 rope, not to the venue class.

### §13.3 — Where the rope buys the most (mean bust by win rate)

| win_rate | n | Select bust | Growth bust | delta |
|---:|---:|---:|---:|---:|
| 40% | 45 | 0.9468 | 0.9306 | -0.0162 |
| 45% | 45 | 0.8281 | 0.7916 | -0.0366 |
| 50% | 45 | 0.6230 | 0.5663 | -0.0567 |
| 55% | 45 | 0.2976 | 0.2201 | -0.0775 |
| 60% | 45 | 0.0791 | 0.0431 | -0.0361 |
| 65% | 45 | 0.0151 | 0.0056 | -0.0095 |
| 70% | 45 | 0.0022 | 0.0005 | -0.0017 |

The benefit is **non-monotone and peaks in the transition zone** (`win_rate=55%`), which is the
expected shape: below it almost every path busts regardless of rope width, above it almost none
do. A wider rope is worth most exactly where a real candidate would sit.

### §13.4 — Full-N validation of the Growth cells

The five pre-registered `MARGINAL_VALIDATION_CELLS` (selected in the original sweep, **not**
re-chosen here) re-scored for Growth at the full frozen `sims_per_seed=10,000` (N=30,000).
Three of the five are among the 26 Growth flips, including the `win_rate=50%` cell above.

| Cell | Growth N=1,500 | Growth N=30,000 | agree? |
|---|---|---|---|
| wr50% `mild_right_skew` cd2 $250 | 0.0093 FEASIBLE | 0.0117 FEASIBLE | **yes** |
| wr55% `mild_right_skew` cd5 $275 | 0.0133 FEASIBLE | 0.0162 FEASIBLE | **yes** |
| wr60% `bounded_clustered` cd1 $250 | 0.0127 FEASIBLE | 0.0117 FEASIBLE | **yes** |
| wr60% `bounded_clustered` cd3 $275 | 0.0107 FEASIBLE | 0.0141 FEASIBLE | **yes** |
| wr65% `symmetric` cd8 $325 | 0.0060 FEASIBLE | 0.0072 FEASIBLE | **yes** |

**5 of 5 agree** (0 disagree). Growth's flipped cells sit further from the 3.0% gate than
Select's marginal population (bust ≈0.7–1.6% vs a 3.0% ceiling), so they are structurally less
N-sensitive — which is what the table shows.

**Not validated, disclosed:** Growth has its own near-gate population (12 `MARGINAL` cells) that
the pre-registered five do not cover. Selecting fresh Growth-specific validation cells *after*
seeing the sweep would be exactly the post-hoc selection the original §4 was careful to avoid, so
it was not done. A Growth-specific marginal battery is its own pre-registration.

### §13.5 — What Growth does NOT buy

**Speed — no gain.** Growth's `min_trading_days=1` ("can pass immediately") is worth nothing at
EM2 risk levels. Median-of-medians days-to-pass over `FEASIBLE` cells: Select **78 days**
(n=94, min 16) vs Growth **78 days** (n=120, min 16). The binding factor is accumulating
$6,000 at $250–$325 of risk per trade, not the day-count floor. The venue's headline "pass in 1
day" is reachable only by a mechanism that can make $6,000 in a day — nothing in this grid can.

**Consistency — nothing, because it never bound.** §6.1 already established Select (40%) and MFFU
(50%) score bit-identically. Growth removes the rule entirely and the effect is still zero. All of
Growth's measured advantage is the rope.

### §13.6 — Two-sided bound on every Growth figure here

Growth's **daily loss limit is a soft breach** — art. 10495915 verbatim: *"If you hit this limit,
trading is stopped for the day but your account is not failed."* `simulate_path` has no lockout
representation (its `daily_loss_pct` branch returns `bust_daily`, a hard fail), so the tier carries
`daily_loss_pct: None` and **the model omits the lockout entirely**. Consequences, both directions:

* **Upper bound w.r.t. the missing lockout.** The venue truncates a losing day near −$2,500; the
  model does not, so modeled daily left tails are fatter than the venue's. Every Growth bust
  figure above is therefore *pessimistic* on this axis.
* **Lower bound w.r.t. the clock.** Same two-clock geometry as Select (floor ratchets EOD, breach
  enforced intraday). The intraday-honest limb is on, but the standing
  [`Q-FIRMEOD-1`](../../../../docs/briefs/closures/Q-FIRMEOD-1-closure-falsified.md) caveat applies.

**Neither bound is quantified.** These are not point estimates. A faithful soft-DLL limb is an
engine change with its own ADR + re-MC. ⚠ Re-verification of art. 10495897 *for Growth
specifically* is **owed** — the 2026-08-24 in-browser pass could not reload it, so the clock
reading rests on the dated 2026-07-30 read quoted in `core/mc/simulation.py::simulate_path`.
Art. 10495915's "intraday fluctuations won't affect the drawdown level" describes the floor's
*ratchet*, not the breach test — but that sentence deserves a direct re-read before any Growth
figure is used for a spend decision.

### §13.7 — What this licenses, and what it does not

**Licensed:** sourcing a Phase-B mechanism against a **~5-point lower win-rate floor** if Growth is
the target tier, and treating the rope — not the consistency rule, not the target, not cadence —
as the single lever worth shopping across Tradeify products.

**Not licensed:** (1) This is still a *shape* map over a synthetic generating process. It admits no
mechanism and no candidate. (2) **UPDATE 2026-08-24 (same day):** `Tradeify_Growth_100K` was
promoted to `AUTOMATION_FRIENDLY_PROP_FIRMS['tradeify']` by operator GO, ratifying
[`2026-08-24-tradeify-growth-tier-scoring-only.md`](../../../../docs/adr/2026-08-24-tradeify-growth-tier-scoring-only.md).
Only the $100K tier is defined; 25K/50K/150K need their own `FIRM_RULES` rows before joining it.
(3) The funded-phase rules differ (Growth has a fixed payout policy and a 35% payout-stage
consistency rule); **nothing here measures the funded phase.** (4) No K consumed, $0 spent,
nothing armed, no gate moved.

<!-- GROWTH-SECTION-END -->
