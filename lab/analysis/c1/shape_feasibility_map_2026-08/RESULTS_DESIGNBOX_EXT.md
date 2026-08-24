**Theme:** c1

# Design-box vs A2-region reconciliation (2026-08-24)

**Status:** `RESOLVED` — 80/80 cells scored at full frozen N; **0 `FEASIBLE`, 0 `MARGINAL`, 80 `INFEASIBLE`**. No design-box cell tested (spanning its own WR floor 30–40%, A2's cadence/EM2-risk axis, and the closed-form's own computed frontier-R) clears the venue's bust≤3.0% gate. Closest cell: WR=35%/cd=1/frontier-R($124.21), bust=5.05% (confident FAIL, lower-2σ bound 4.80% — not `MARGINAL`). Falsifies the flat reading of the supply audit's conjunct (iii) ("the design box... is itself the venue-compatible shape") as a **sufficiency** claim — see §10.

**What this is:** a **disclosed COVERAGE EXTENSION** of the A2 payoff-shape feasibility map
([`RESULTS.md`](RESULTS.md)) — **never** merged into A2's own frozen 630-cell grid or
`region_data.jsonl`. This document resolves a same-day contradiction between two independent
2026-08-23 artifacts: the deep-iteration lane supply audit's conjunct (iii)
([`docs/notes/audits/programme-audit/2026-08-23-deep-lane-supply-audit.md`](../../../../docs/notes/audits/programme-audit/2026-08-23-deep-lane-supply-audit.md))
and A2's own region map. Operator-GO'd this session ("run the design box vs A2 reconciliation").

---

## §0 — Rule-0 reads (this session, 2026-08-24)

| Source | What it grounds |
|---|---|
| [`docs/adr/2026-08-13-msl-slate-2-design-box.md`](../../../../docs/adr/2026-08-13-msl-slate-2-design-box.md) | The ratified design box under test: `rr`∈[2,3] · target WR 0.30–0.42 · `R` at the bust-≤3.0% diffusion frontier (provisional) · hard stop mandatory · k=1 · no pyramiding. `Accepted` 2026-08-13, still the live decision. |
| [`docs/notes/notice/N-2026-08-13-msl-design-box-rederivation.md`](../../../../docs/notes/notice/N-2026-08-13-msl-design-box-rederivation.md) §7/§9 | §7 gives the box's own geometry statement; §9 is the load-bearing find — an **executable, verbatim, reproducible closed-form formula** for the bust≤3% diffusion frontier-R (`m0`/`K`/`disc`/`R`), stated as a stdlib Python audit hook and independently re-run in this session (below) — it reproduces the notice's own published table to the cent. §8 discloses the bound's own approximation layers (i.i.d. trades, continuous diffusion, infinite horizon) — carried forward as a disclosed limitation here, not re-litigated. |
| `lab/analysis/c1/shape_feasibility_map_2026-08/{shape_generator.py, run_region_sweep.py, analyze_region.py, test_shape_generator.py}` | The A2 harness being extended. §2 below states exactly which conventions are reused verbatim (loss-side hard-stop convention, MAE-band mechanics, weekly placement, engine-call sequence) and which are new. `run_region_sweep.py`'s gating primitives (`se_of_proportion`, `gate_status`, `combine_verdict`, `firm_consistency`, `_run_with_days`, `DD_GATE`, `PASS_GATE`) are **imported directly**, not re-typed — `_run_with_days` is where `assert_engine_ready → firm_kwargs → run_seed → summarize_outcomes` actually get called, so importing it means this extension calls the identical function A2 calls. |
| [`RESULTS.md`](RESULTS.md) §2 (shape generative process), §3 (scoring methodology) | Full disclosure of A2's three existing shapes' win/loss/MAE conventions and the joint bust≤3.0%/pass≥50% gating discipline (SE-of-proportion, 2σ MARGINAL band, no best-cell selection) — reused byte-identically here (§5 below). |
| `lab/discovery/prop_survivor_scoring.py::load_scoring_thresholds` | Frozen seeds `(42, 123, 2026)`, horizon `1500`, `sims_per_seed=10,000`, `eval_bust_ceiling=0.03`, `pass_floor=0.50` — parsed at runtime from the pre-registration, asserted at every invocation (`run_designbox_sweep.py` carries the identical `assert abs(thr.eval_bust_ceiling - DD_GATE) < 1e-9` guard A2's own runner uses). None re-picked. |
| `docs/notes/audits/programme-audit/2026-08-23-deep-lane-supply-audit.md` §3.5 conjunct (iii) | The claim under test: *"the MSL design box rr∈[2,3] / WR 0.30–0.42 / hard-stop / k=1 / no-pyramiding is itself the venue-compatible shape."* Quoted in full in §9 below before adjudication. |
| `core/mc/simulation.py::simulate_path`, `core/mc/preflight.py::firm_kwargs` | The production engine — reused unmodified via the imported `_run_with_days`, never re-implemented. Confirmed directly (not via a description) that `Tradeify_Select_100K` and `MFFU_Rapid_100K` share `max_dd_pct=3.0` ($3,000/$100K, `dd_type="trailing_locking"`), `profit_target_pct=6.0` ($6,000), differing only in `consistency_rule_pct` (40.0/50.0), `min_trading_days` (3/2), and `cost_per_side_usd` (0.91/0.95) — `core/firm_rules.py` read directly this session. |

---

## §1 — The contradiction, restated precisely

The [deep-iteration lane charter](../../../../docs/adr/2026-08-16-deep-iteration-lane-charter.md)
§2.1 targets candidates inside the slate-2 design box (rr∈[2,3] · WR 0.30–0.42 · R-at-frontier ·
hard stop · k=1 · no pyramiding). The 2026-08-23 supply audit's §3.5 conjunct (iii) asserted this
box "is itself the venue-compatible shape" — i.e., that satisfying the box's own geometry is
*sufficient* for venue survival, deferring only per-candidate construction-time screening.

A2's own region map, published the **same day**, found every tested cell at win_rate ≤ 50%
`INFEASIBLE` for both `Tradeify_Select_100K` and `MFFU_Rapid_100K` (97.6–100% bust at WR=40%,
[`RESULTS.md`](RESULTS.md) §6.2/§7.2) — but A2's own grid (a) never went below WR=40%, (b) never
tested a 2–3R-win shape class (its strongest skew, `mild_right_skew`, is a mean-1.5R exponential
tail — a materially different, smaller-mean shape than the box's 2–3R span), and (c) its risk axis
floors at $250, above the box's own frontier-R for two of the three win rates tested below. Neither
artifact actually tested the design box's own geometry. This document does.

---

## §2 — New shape archetype: `design_box` (full disclosure)

Implemented in [`design_box_shape.py`](design_box_shape.py), a **sibling module** to
`shape_generator.py` (never edits it). Full generative disclosure, condensed from the module's own
docstring:

| Axis | Choice | Rationale |
|---|---|---|
| Win R | **Uniform(2, 3)** | The ADR's own `rr` range, taken literally as a maximally-uncertain (uniform) prior across it — no free parameter beyond "trust the box's own stated span." Mean win = exactly 2.5R. |
| Loss R | **−1.0 exactly** (hard stop, no jitter) | Reuses `shape_generator`'s `bounded_clustered` loss convention, **not** `symmetric`/`mild_right_skew`'s jittered `−Uniform(0.7,1.3)` — the ADR mandates "hard stop mandatory," and `bounded_clustered`'s exact `−1.0` is the one A2 shape that actually models a hard stop with no slippage. |
| Losing-trade MAE | `MAE == realized loss` exactly | Same convention as **all three** existing A2 shapes (hard stop reached, not slipped past) — no gap-through-stop tail, same disclosed limitation as `RESULTS.md` §2/§11. |
| Winning-trade MAE | **Uniform(0.30, 0.80)R** of one stop | Reuses `mild_right_skew`'s band **verbatim**, not an invented one. A trade held to a 2–3R target spends materially longer exposed than a ~1R takeout — the same "let it run" reasoning `RESULTS.md` §2 gives for `mild_right_skew`'s wider band vs `symmetric`'s tighter one. |
| Cadence axis | **A2's own (1,2,3,5,8)/week, unchanged** | Dispatch instruction. Includes `WEEKDAY_PATTERN[8]`'s same-calendar-day doubling (Mon×2/Tue×2/...) — see the k=1 caveat below. |
| Weekly placement, panel length | Reused unchanged from `shape_generator` (`N_WEEKS=520`, `WEEKDAY_PATTERN`) | Guarantees the activity floor structurally, identically to A2. |
| k=1 / no pyramiding | k=1 is a **real-mechanism entry-rule mandate**, not literally re-derived here | This DGP draws one scalar R-multiple per trade (no pyramiding, structurally satisfied). Testing across A2's cadence axis — including cadence=8's same-day doubling — is coverage of trade *frequency*, not a claim that a literal k=1-compliant mechanism fires twice in a day. A2's own three shapes never made a k=1 claim for their cadence sweep either; this extension inherits that same coverage-not-claim status. **Disclosed as a limitation (§12), not silently smoothed over.** |

**Win rates tested: {30%, 35%, 40%}** — the design box's own span, floored at the shared row
against A2's own grid floor (40%), per dispatch instruction. (42% — the box's stated ceiling — is
not tested; 40% is the pre-registered stopping point.)

---

## §3 — Frontier-R: computed, not assumed

Rule-0 read #1 requires: if the notice's §7 defines a *computable* frontier-R, compute it and
include that risk level in the grid; if genuinely underspecified, say so and fall back to A2's own
axis plus one disclosed downward interpolation. **§9 of the notice is computable** — it is a
complete, executable, stdlib-only closed form (`m0 = p·rr − (1−p)`; `K = (2D/X)/((rr+1)²p(1−p))`;
`R = (K·m0 + √(K²m0² − 4Kc))/2`, `X = −ln(0.03)`), and this session independently re-ran it verbatim
(reproduced in `test_design_box_shape.py::test_frontier_formula_reproduces_notice_sec9_table`):

| p | rr | c | Notice's own published R | This session's re-run | Match |
|---:|---:|---:|---:|---:|---|
| 0.461 | 1 | 2.82 | infeasible | `None` | ✓ |
| 0.55 | 1 | 2.82 | $137 | $137.35 | ✓ |
| 0.60 | 1 | 2.82 | $342 | $341.77 | ✓ |
| 0.42 | 2 | 2.82 | $191 | $191.42 | ✓ |
| 0.30 | 3 | 2.82 | $85 | $84.94 | ✓ |
| 0.35 | 3 | 2.82 | $181 | $180.69 | ✓ |
| 0.40 | 3 | 2.82 | $262 | $262.57 | ✓ |
| 0.35 | 3 | 4.12 (MGC) | $177 | $177.09 | ✓ |

Formula transcription confirmed byte-faithful (every row matches to the dollar or better).

**Applying it to `design_box`'s own geometry.** The `design_box` shape's wins span Uniform(2,3)R,
not a fixed `rr`. Since `m0 = p·E[win_R] − (1−p)` is **exact** under the substitution
`rr → E[win_R] = 2.5` when losses are point-mass at −1R, this session uses **`rr=2.5`** (this
shape's own mean win) as the effective `rr` for the frontier computation — the correct value for the
formula's drift term. The formula's *variance* term technically assumes a point-mass win side (fixed
`rr·R`); the true variance for a Uniform(2,3) win side is ≈1% higher (extra spread beyond the
point-mass approximation), which makes this frontier-R **very slightly optimistic** relative to a
fully-exact closed form for this precise DGP — second-order next to the note's own already-disclosed
approximation layers (§8 item 2: i.i.d., diffusion, infinite horizon). `c=2.82` is the notice's own
published "index micros" round-trip figure (§9), reused verbatim; `D=3000` (the rope) is confirmed
directly from `core/firm_rules.py` for both firms (§0).

**Result, at `rr=2.5, c=2.82`:**

| Win rate | m₀ (gross edge, R) | Frontier-R | vs. EM2 $250 floor |
|---:|---:|---:|---|
| 30% | 0.05 | **`None`** — discriminant negative; cost exceeds any bust-compliant R at this thin an edge | n/a — genuinely infeasible by the closed form itself at this WR/rr pair |
| 35% | 0.225 | **$124.21** | downward — **added** to the grid |
| 40% | 0.40 | **$225.52** | downward — **added** to the grid |

Per dispatch instruction ("downward only," never above $250, and the EM2 spec's own "interpolate
down, never up" rule), the frontier-R is added to the risk axis only where finite and below $250.
$325 is never tested at any win rate in this extension — the box's own R-sizing logic points down,
not up. **The closed form itself already predicts WR=30% is not rescuable by any risk level at
`rr=2.5`** — this is stated here as a pre-registered expectation, checked against the actual MC
engine result in §6, not assumed.

---

## §4 — The extension grid (pre-registered before scoring)

| Axis | Values |
|---|---|
| Win rate | 30%, 35%, 40% |
| Shape | `design_box` (one shape) |
| Cadence | 1, 2, 3, 5, 8 /week (A2's axis, unchanged) |
| Risk (WR=30%) | $250, $275 |
| Risk (WR=35%) | **$124.21 (frontier)**, $250, $275 |
| Risk (WR=40%) | **$225.52 (frontier)**, $250, $275 |
| Firms | `Tradeify_Select_100K`, `MFFU_Rapid_100K` (dispatch pre-registration — **not** `run_region_sweep.py`'s own now-3-firm `FIRM_KEYS`; `Tradeify_Growth_100K` was added to A2 the same day by a separate, unrelated extension and is out of scope here, §12) |

**40 (win_rate, cadence, risk) tuples × 2 firms = 80 cells.** Full frozen `sims_per_seed=10,000` ×
3 seeds (`N=30,000` paths) for **every** cell — no reduced-N deviation (dispatch instruction; A2's
own primary sweep used a reduced N, disclosed in its own §4). Gates byte-identical to A2: bust≤3.0%
intraday-honest ∧ P(pass)≥50%; SE-of-proportion at the actual N; cells within 2σ of a gate line are
`MARGINAL`, never `PASS`; no best cell selected, reported, or ranked anywhere below.

---

## §5 — Compute budget

Measured this session, full frozen N=30,000, on this machine: a transition-zone cell (WR=40%,
cadence=3, frontier-R $225.52, `Tradeify_Select_100K`) took **99.2s**; a high-bust corner (WR=30%,
cadence=1, $250, `MFFU_Rapid_100K`) took **214.1s** — average **156.7s/cell**, giving a serial
estimate of **≈3.5 CPU-hours** for the full 80-cell grid, comfortably under the ~8 CPU-hour
disclosure ceiling. **No risk-axis trimming was needed.** The real sweep was run sharded 8-way in
parallel (`--shard-index i --n-shards 8`, matching A2's own 8-core disclosure).

**Realized total (disclosed, not the initial estimate): 4.004 CPU-hours** (14,414s across 80 cells,
avg 180.2s/cell). Mid-run, the running average climbed as high as ≈5.2 CPU-hours-projected once the
WR=35%/40% positive-edge cells (which survive longer before resolving bust/pass, hence cost more
per path) began dominating the sample — WR=35% cells alone averaged 250.6s/cell (max 890.9s, the
single slowest cell in the grid: WR=35%/cd=1/frontier-R, the cell with the *lowest* bust of the
whole run, consistent with "cells near the gate are the slowest" per A2's own §4). The realized
total settled at 4.00 CPU-hours because the WR=40%/cd≥5 cells (fast, high-cadence, quicker
resolution) and the WR=30% cells (fast, high-bust, early termination) balanced the slower middle —
**no risk-axis trimming was triggered**, and none would have been warranted in hindsight.

| Win rate | n cells | total CPU-s | avg s/cell | min s | max s |
|---:|---:|---:|---:|---:|---:|
| 30% | 20 | 2,961 | 148.1 | 59.3 | 342.0 |
| 35% | 30 | 7,519 | 250.6 | 55.2 | 890.9 |
| 40% | 30 | 3,934 | 131.1 | 36.2 | 386.5 |
| **Total** | **80** | **14,414** | **180.2** | **36.2** | **890.9** |

---

## §6 — Results: the full extension grid

Full raw data (80 rows, one JSON object per line, `Tradeify_Select_100K` and `MFFU_Rapid_100K`
both present): [`designbox_region_data.jsonl`](designbox_region_data.jsonl) (merged from
[`designbox_shards/`](designbox_shards/)). **`Tradeify_Select_100K` and `MFFU_Rapid_100K` are
bit-identical on every one of the 40 tuples** (verified directly: `bust` and `pass_rate` match to
full float precision on all 40 firm-pairs, 0 divergent) — so the table below shows one firm; see
§8 for the disclosed divergence check this was pre-registered to test.

**Headline: 80/80 cells `INFEASIBLE`. 0 `FEASIBLE`. 0 `MARGINAL`.** Every cell's bust rate is a
*confident* fail — the closest cell's own 2σ lower bound (4.80%, below) still clears the 3.0% gate
line by 1.8 points, so nothing here is a coin-flip call obscured by insufficient N.

#### win_rate = 30%

| cadence/wk | $250 | $275 |
|---|---|---|
| 1 | INFEASIBLE (bust 79.44%, pass 20.56%) | INFEASIBLE (bust 74.67%, pass 25.33%) |
| 2 | INFEASIBLE (bust 70.64%, pass 29.36%) | INFEASIBLE (bust 82.04%, pass 17.96%) |
| 3 | INFEASIBLE (bust 68.73%, pass 31.27%) | INFEASIBLE (bust 78.89%, pass 21.11%) |
| 5 | INFEASIBLE (bust 76.49%, pass 23.51%) | INFEASIBLE (bust 77.28%, pass 22.72%) |
| 8 | INFEASIBLE (bust 72.23%, pass 27.77%) | INFEASIBLE (bust 73.54%, pass 26.46%) |

No cell close to the gate — matches the frontier-R closed form's own prediction (§3: no finite
frontier-R exists at `rr=2.5, p=0.30`; cost exceeds any bust-compliant R at this thin an edge).

#### win_rate = 35%

| cadence/wk | $124.21 (frontier) | $250 | $275 |
|---|---|---|---|
| 1 | INFEASIBLE (bust **5.05%**, pass 89.96%) | INFEASIBLE (bust 58.13%, pass 41.87%) | INFEASIBLE (bust 29.83%, pass 70.17%) |
| 2 | INFEASIBLE (bust 16.63%, pass 83.12%) | INFEASIBLE (bust 53.27%, pass 46.73%) | INFEASIBLE (bust 48.31%, pass 51.69%) |
| 3 | INFEASIBLE (bust 20.25%, pass 79.74%) | INFEASIBLE (bust 30.07%, pass 69.93%) | INFEASIBLE (bust 41.28%, pass 58.72%) |
| 5 | INFEASIBLE (bust 12.73%, pass 87.27%) | INFEASIBLE (bust 34.54%, pass 65.46%) | INFEASIBLE (bust 46.78%, pass 53.22%) |
| 8 | INFEASIBLE (bust 12.13%, pass 87.87%) | INFEASIBLE (bust 42.65%, pass 57.35%) | INFEASIBLE (bust 37.42%, pass 62.58%) |

**The single closest cell in the entire 80-cell grid.** The frontier-R column is dramatically
better than the EM2 axis at this win rate (e.g. cadence=1: 5.05% vs 58.13% vs 29.83%) — the
closed-form risk sizing is doing real, measurable work here, just not enough.

#### win_rate = 40%

| cadence/wk | $225.52 (frontier) | $250 | $275 |
|---|---|---|---|
| 1 | INFEASIBLE (bust 24.31%, pass 75.68%) | INFEASIBLE (bust 16.40%, pass 83.60%) | INFEASIBLE (bust 22.32%, pass 77.68%) |
| 2 | INFEASIBLE (bust 11.94%, pass 88.06%) | INFEASIBLE (bust 11.83%, pass 88.17%) | INFEASIBLE (bust 29.67%, pass 70.33%) |
| 3 | INFEASIBLE (bust 8.14%, pass 91.86%) | INFEASIBLE (bust 19.49%, pass 80.51%) | INFEASIBLE (bust 18.16%, pass 81.84%) |
| 5 | INFEASIBLE (bust 9.35%, pass 90.65%) | INFEASIBLE (bust 10.89%, pass 89.11%) | INFEASIBLE (bust 9.71%, pass 90.29%) |
| 8 | INFEASIBLE (bust **7.94%**, pass 92.06%) | INFEASIBLE (bust 15.77%, pass 84.23%) | INFEASIBLE (bust 17.27%, pass 82.73%) |

**Disclosed, not smoothed over: risk is not monotonic within this row** — e.g. at cadence=1 the
frontier-R ($225.52) shows *higher* bust (24.31%) than the plain EM2 $250 cell (16.40%), the
opposite of the naive "less $ risk ⇒ less bust" intuition. This is a real feature of the harness's
seeding convention, shared with A2's own shapes: each `(win_rate, cadence, risk)` tuple draws an
**independent** 520-week synthetic panel (seed = master seed + `tuple_index(...)`), not a shared
baseline perturbed by risk — so neighboring risk levels are genuinely different finite draws, not
smooth rescalings of one another. At `cadence=1` the underlying panel has only 520 total trades
(one path through the DGP, before the engine's own 30,000-path block-bootstrap resamples from it),
which is the thinnest sample in the grid — exactly where single-draw variance is most visible. The
**overall** 30% → 35% → 40% trend (bust falling from ~70–80% to single digits) is real and
monotonic in aggregate; the specific ordering of adjacent risk cells within one row is not.

**The single closest WR=40% cell (cd=8, frontier-R): bust 7.94%**, still 2.6× the 3.0% ceiling.

### §6.1 — Closest-to-gate cells, ranked

| Rank | Cell | Bust | 2σ lower bound | vs. 3.0% gate |
|---:|---|---:|---:|---|
| 1 | WR=35% cd=1 frontier-R($124.21) | 5.05% | 4.80% | 1.68× |
| 2 | WR=40% cd=8 frontier-R($225.52) | 7.94% | 7.63% | 2.65× |
| 3 | WR=40% cd=3 frontier-R($225.52) | 8.14% | 7.82% | 2.71× |
| 4 | WR=40% cd=5 frontier-R($225.52) | 9.35% | 9.02% | 3.12× |
| 5 | WR=40% cd=5 $275 | 9.71% | 9.36% | 3.24× |

The closed-form frontier was solved to hit **exactly** 3.0% bust under the diffusion approximation
(§3, `disc`/`R` solved for that target). The real block-bootstrap engine's *closest* realization
across the whole grid still misses by 68% (rank 1). This is a direct, quantified confirmation of
the notice's own §8 item 2 disclosure — *"i.i.d. makes it optimistic where real trades cluster"* —
playing out in practice, not merely a theoretical caveat.

---

## §7 — Shared-row comparison at WR=40% (design_box vs. A2's three shapes)

At the row both maps share (WR=40%, risk ∈ {$250, $275}, the EM2 axis both use):

| Shape | Bust range (10 cells: 5 cadences × 2 risk) |
|---|---|
| `design_box` (this extension) | **9.71%–29.67%** |
| A2 `mild_right_skew` (mean win 1.5R) | 73.33%–90.40% |
| A2 `symmetric` (mean win ≈1.0R) | 99.87%–100.00% |
| A2 `bounded_clustered` (mean win ≈1.0R, tight) | 99.87%–100.00% |

**This is the extension's second load-bearing finding.** At the identical win rate and identical
$-risk levels, `design_box`'s 2–3R wins cut bust by **3× to 10×** relative to A2's *best* shape
(`mild_right_skew`) and by roughly an order of magnitude relative to `symmetric`/`bounded_clustered`.
The design box's own directional premise — that a larger, asymmetric win size is what the trailing-DD
barrier actually rewards, more than skew or win-clustering per se (matching A2's own §7 point 3
reading, extended here to a materially larger win size than A2 ever tested) — is **strongly
corroborated** by this comparison. What it does not do, at WR=40%/EM2-risk, is cross the 3.0% line:
`design_box`'s own closest EM2-axis cell at WR=40% (9.71%, cd=5/$275) is still more than 3× the
ceiling, even though it is the best-surviving shape either map has tested.

---

## §8 — Firm-divergence check (pre-registered)

The dispatch explicitly flagged this as worth checking fresh, not inherited from A2: a 2–3R-win,
low-win-rate shape concentrates profit into fewer, larger days — exactly the geometry where
`Tradeify_Select_100K`'s 40% consistency rule and `MFFU_Rapid_100K`'s 50% rule could plausibly
diverge for the first time (A2's own three shapes never produced a day inside the (40%,50%] profit
share band, §6.1 there).

**Result: they still do not diverge.** All 40 `(win_rate, cadence, risk)` tuples were checked
directly against both firms' raw `bust`/`pass_rate` figures: **40/40 identical to full float
precision, 0 divergent.** `min_trading_days` (3 vs 2) is cleared well before any path nears its
target at this grid's cadences (matching A2's own §6.1 reasoning), and — as this extension's own
raw data confirms — not one of the 80 cells' underlying paths ever produces a single day's profit
share landing inside the (40%, 50%] band, even with 2–3R wins concentrating P&L into fewer days
than any of A2's three shapes. **This is a real, checked, disclosed negative finding**, exactly the
kind the dispatch asked to be stated plainly if it recurred: the consistency-rule divergence
hypothesis is not confirmed by this shape either, and the two firms remain functionally identical
for bust/pass purposes across every shape tested to date (A2's three plus this one).

---

## §9 — One-page reading

**1. No design-box cell tested is venue-feasible.** Across the box's own WR span (30–40%, floored
at the shared row with A2 — 42% itself was not tested, see §12), A2's own cadence axis (1–8/week),
A2's own EM2 risk axis ($250/$275), and the closed-form's own computed bust≤3% frontier-R for each
win rate tested — **0 of 80 cells clear the bust gate**, and every failure is confident (no cell
sits within 2σ of the 3.0% line). The nearest cell (WR=35%, cd=1, frontier-R $124.21) posts 5.05%
bust — 68% over the ceiling the closed form solved it to hit exactly.

**2. The design box's own R-at-frontier logic helps, measurably, but is not sufficient.** Where the
frontier-R is finite (WR=35%/40%), it usually — though not perfectly monotonically, §6 — beats the
EM2 $250/$275 levels by a wide margin (e.g. WR=35%/cd=1: 5.05% vs 58.13%/29.83%). The closed-form's
diffusion approximation is doing real, directionally-correct work; it is simply optimistic in
magnitude relative to the production block-bootstrap engine, consistent with the source notice's
own disclosed limitation (§8 item 2 there; quantified here for the first time against the real
engine).

**3. The design box's *shape* (2–3R wins) is a real, large improvement over anything A2 tested —**
**just not, on its own, enough.** §7's shared-row comparison shows `design_box` beating A2's best
shape by 3–10× in bust rate at the identical win rate and risk. The box is pointed in the correct
direction; it has not yet been shown to reach the destination at the win rates this extension
covers.

**4. The trend across WR is real but not fully explored.** Best-cell bust falls from ~69% (WR=30%)
to 5.05% (WR=35%) — and then, non-monotonically, back up to 7.94% at the best WR=40% cell (§6's own
disclosed non-monotonicity). This extension's pre-registered grid stops at WR=40% (the shared row
with A2), one full 2-point step short of the box's own stated 42% ceiling. **Whether WR=41–42%
would cross the gate is not answered here** — the trend from 30%→35% is steeply favorable, but the
35%→40% step was not (best cell got worse, not better), so extrapolating to 42% either direction
would be speculation, not measurement. This is a named, bounded follow-up (§12), not a finding.

**5. Firms do not diverge (§8).** The consistency-rule-divergence hypothesis this dispatch
pre-registered to test is not confirmed. `Tradeify_Select_100K` and `MFFU_Rapid_100K` remain
functionally identical for feasibility purposes across all four shapes tested to date (A2's three,
plus `design_box`).

---

## §10 — What this means for conjunct (iii) and the charter's §2.1 targeting

**Conjunct (iii), quoted in full** (`docs/notes/audits/programme-audit/2026-08-23-deep-lane-supply-audit.md`
§3.5): *"Shape is determined at construction, and the estate already owns the screen for it (EM0–EM5
mechanism-shape spec, ratified 2026-08-06; **the MSL design box rr∈[2,3] / WR 0.30–0.42 / hard-stop
/ k=1 / no-pyramiding is itself the venue-compatible shape**). The constraint genuinely kills daily
hold-to-close reversal shapes ... and pyramided/high-skew shapes — it does not pre-kill an intraday
order-flow-derived construct. Conjunct (iii) is satisfiable but per-candidate, at construction time,
through the existing screen."*

**The bolded clause, read as a sufficiency claim — "landing inside the box's stated geometry is
itself enough to be venue-compatible" — is contradicted by this measurement.** 80/80 cells spanning
the box's own WR floor to the shared-row ceiling, at both A2's risk axis and the box's own computed
frontier-R, fail the venue's bust gate. Box-membership alone does not clear N-SURV.

**What survives, and is in fact reinforced:** the audit's own *final* sentence — "conjunct (iii) is
satisfiable but **per-candidate**, at construction time, **through the existing screen**" — already
correctly declined to claim automatic clearance. This measurement is consistent with that qualifier
and sharpens it: the existing screen (bust≤3.0% ∧ P(pass)≥50%) is not merely a formality a
box-shaped candidate is expected to pass — at the specific win rates this extension covers, it is a
**high bar that no tested point inside the box clears**, even at the box's own frontier-sized risk.
A future candidate genuinely inside the box still needs its own full N-SURV run, not a pass-by-membership
inference from the box's own ADR.

**Charter §2.1** (`docs/adr/2026-08-16-deep-iteration-lane-charter.md` §2 item 1) targets new
families "inside the slate-2 design-box geometry ... on non-index CME micros first." The charter's
own §2 item 5 already makes N-SURV an unconditional downstream gate ("byte-unedited") — so the
charter's *process* is not broken by this finding; it never claimed box-membership was sufficient on
its own. What this finding does supply is a **quantified expectation**: a family landing inside the
box, at the win rates this extension covers, should expect to need to clear a materially higher bar
than "beat A2's shapes" (§7) — it needs to clear bust≤3.0% outright, which no coverage-map point has
yet done at this geometry.

**Neither the charter nor the design-box ADR is edited by this document** (both are ratified
decision artifacts) — see §11 for the owed reader-intercepts.

---

## §11 — Owed reader-intercepts (not edited by this task; listed for operator authorization)

1. **`docs/adr/2026-08-16-deep-iteration-lane-charter.md` §2 item 1 ("§2.1").** Targets candidates
   "inside the slate-2 design-box geometry." This finding does not require a text change (N-SURV is
   already unconditional there), but the operator may want a pointer to this extension alongside
   that clause so a future campaign author reads the quantified expectation in §10 before freezing
   a prereg against this geometry.
2. **`docs/adr/2026-08-13-msl-slate-2-design-box.md`** and its source,
   `docs/notes/notice/N-2026-08-13-msl-design-box-rederivation.md`. The ADR's own "R at the
   bust-≤3.0% diffusion frontier (**provisional**)" language flagged the frontier as unresolved
   pending a closed-form re-derivation (the spawned Magdon-Ismail task, notice §8 item 2/§10). This
   extension is the first direct check of the *existing* diffusion frontier against the production
   engine, and finds it optimistic by ~1.7–8× at the cells tested (§6.1). Whether the Magdon-Ismail
   exact closed form (once it lands) narrows or confirms this gap is unanswered here — named as a
   natural next check, not run by this task (out of scope; no Magdon-Ismail artifact was read or
   relied on).
3. **Supply audit conjunct (iii)** — corrected in place, dated, directly in
   `docs/notes/audits/programme-audit/2026-08-23-deep-lane-supply-audit.md` itself (an inline
   annotation at conjunct (iii)'s own paragraph, plus a Change-history row there — done by this
   dispatch, per its own instruction that the audit note is in scope for a dated correction; not
   merely listed here as owed).

---

## §12 — Limitations (consolidated)

1. **Effective `rr=2.5` substitution** in the frontier-R closed form (§3) — the formula's variance
   term technically assumes a point-mass win side; this shape's actual Uniform(2,3) spread adds
   ≈1% extra true variance beyond that approximation, a second-order effect next to the note's own
   disclosed approximation layers.
2. **k=1 / cadence=8 coverage-not-claim caveat** (§2) — this extension's cadence axis (reused from
   A2 unchanged) includes cadence=8's same-calendar-day trade doubling, which is coverage of trade
   *frequency*, not a claim that a literal k=1-compliant mechanism fires twice in one day.
3. **Gross of commission** — like all three A2 shapes, no `cost_per_side_usd` is netted into this
   shape's R-multiples; cost-law is a separate, already-existing gate a real candidate must clear on
   its own measured basis.
4. **No gap-through-stop tail** — losing trades reach, never slip past, their hard stop (same
   disclosed limitation as A2, RESULTS.md §2/§11).
5. **DGP not calibrated to any real instrument** — a payoff-shape abstraction, deliberately, same as
   A2. The design-box notice's own §7 instrument preference (non-index: MGC/MCL/M6A) is not
   represented here at all — cost and volatility characteristics of any specific instrument are out
   of scope for this shape-only coverage map.
6. **Firms tested: `Tradeify_Select_100K`, `MFFU_Rapid_100K` only** — the dispatch's own
   pre-registration. `Tradeify_Growth_100K` (added to A2's own harness the same day, 2026-08-24, by
   an unrelated extension — RESULTS.md §13) is out of scope here; not run, flagged as a natural
   follow-up given its wider $3,500 rope might behave differently against this shape.
7. **WR ceiling 42% (the box's own stated max) not tested** — the grid stops at 40% (dispatch's
   shared-row floor against A2). §9 point 4 states plainly that the 35%→40% trend does not license
   extrapolating to 42%.
8. **`rr` represented as one Uniform(2,3) shape, not swept as an independent axis** — the design
   box's own `rr∈[2,3]` and `WR∈[0.30,0.42]` are two distinct axes; this extension collapses `rr`
   into a single blended shape (§2) rather than testing `rr=2` and `rr=3` as separate point-mass
   archetypes (mirroring `bounded_clustered`'s exact-payoff convention). A natural follow-up, not
   run here (would be scope creep beyond the dispatch's pre-registered single-shape grid).
9. **Single synthetic-panel draw per tuple** (inherited from A2's own convention, §6's own disclosed
   non-monotonicity at WR=40% is a direct, observed consequence) — no repeated/averaged panel draws
   per cell; the production engine's own 30,000-path block-bootstrap is the source of statistical
   confidence for each individual cell's own bust/pass estimate, not repeated panel draws.

---

## Gate (this extension)

**`RESOLVED`** — the pre-registered grid (§4) was scored in full at the full frozen N (§5/§6), the
shared-row comparison (§7) and firm-divergence check (§8) both ran as pre-registered, and a
one-page reading (§9) plus the conjunct (iii) reconciliation (§10) are both stated. The finding is
decisive (0/80 `FEASIBLE` or `MARGINAL` — every cell a confident `INFEASIBLE`), not an
`AMBIGUOUS-HOLD`. No best cell was selected, reported, or ranked as a recommendation anywhere above
— §6.1's ranking is diagnostic (which cells came closest to the gate), not a nomination.

---

## Verification

```bash
# Harness invariant tests (26 tests, no engine calls)
python -m pytest lab/analysis/c1/shape_feasibility_map_2026-08/test_design_box_shape.py --import-mode=importlib -q
# Expected: 26 passed

# A2's own test suite unaffected (shape_generator.py untouched by this extension)
python -m pytest lab/analysis/c1/shape_feasibility_map_2026-08/test_shape_generator.py --import-mode=importlib -q
# Expected: 14 passed

# Frontier-R closed form reproduces the notice's own Sec9 table to the cent (8 rows)
python -m pytest "lab/analysis/c1/shape_feasibility_map_2026-08/test_design_box_shape.py::test_frontier_formula_reproduces_notice_sec9_table" -q
# Expected: 8 passed

# Row count == 80, zero duplicate cell_ids, zero missing cells, firm bit-identity check
python -c "
import json, glob
rows = {}
for p in sorted(glob.glob('lab/analysis/c1/shape_feasibility_map_2026-08/designbox_shards/shard*.jsonl')):
    for line in open(p, encoding='utf-8'):
        line = line.strip()
        if line:
            r = json.loads(line)
            rows[r['cell_id']] = r
print(len(rows))
from collections import Counter
print(Counter(r['verdict'] for r in rows.values()))
"
# Expected: 80
# Expected: Counter({'INFEASIBLE': 80})

# Merged region file matches the shard sum
python -c "
import json
rows = [json.loads(l) for l in open('lab/analysis/c1/shape_feasibility_map_2026-08/designbox_region_data.jsonl', encoding='utf-8')]
print(len(rows), sum(1 for r in rows if r['verdict']=='INFEASIBLE'))
"
# Expected: 80 80
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-24 | Initial authoring — harness (`design_box_shape.py`, `test_design_box_shape.py`, `run_designbox_sweep.py`), frontier-R computation, grid pre-registration, full 80-cell sweep at full frozen N, results, one-page reading, conjunct (iii) reconciliation | Claude Code (Sonnet 5) |
