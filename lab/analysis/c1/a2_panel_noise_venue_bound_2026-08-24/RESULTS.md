**Theme:** c1

# A2 panel-draw noise + the size-invariant venue bound

**Status:** ACTIVE — the A2 map's dominant uncertainty is the single 520-week DGP panel each cell sits on, not the MC path count its `se_bust` bars measure (49 of 63 cadence groups exceed their own 2σ bar, median 4.3×); §13.2's Growth headline is the grid's most extreme panel draw (z=+3.12, 1.50× intended drift) and flips `FEASIBLE`→`INFEASIBLE` at a 10× panel, so §7.2 stands as written — while §13.1/§13.3's **paired** rope finding replicates (33/282/0 vs 38/277/0) and should be read as it stands. Separately: the eval's requirement collapses to a **size-invariant** bound `T_min(yr) = (target/rope)·(ln(1/0.03)/2)/annSR²` (validated 230/232 against A2's own cells), under which the corpus maximum ever published (annSR +1.28) is 2.1× short of a six-month pass and the four live TNEC lanes are an order of magnitude further; and `pol_cushion`'s bust-elimination needs **sub-integer micro contracts** — rounded to whole contracts it is identical to flat k=1.

**Date:** 2026-08-24 · **Spend:** **$0.00 · K=0 · no manifest · no Cap seat · nothing armed.**
**Live effect:** none. No `core/`, `dd_protection`, allocation, Pine, lifecycle, `firm_rules`, or rail
surface is touched. No candidate is proposed, admitted, unparked, demoted, or retired. This is a
measurement + derivation pass over already-committed artifacts.

**Parent artifacts under examination:**
[`shape_feasibility_map_2026-08/RESULTS.md`](../shape_feasibility_map_2026-08/RESULTS.md) (A2) ·
[`orbmnq1_cushion_sizing_probe_2026-08-20`](../orbmnq1_cushion_sizing_probe_2026-08-20/) ·
[`Q-ORBSURV-1 closure`](../../../../docs/briefs/closures/Q-ORBSURV-1-closure-falsified.md) ·
[`ORB re-park ADR`](../../../../docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md)

---

## §0 — Rule 0 reads (production source, this session)

| Source | What it grounds |
|---|---|
| `lab/analysis/c1/shape_feasibility_map_2026-08/shape_generator.py` (`build_panel`, `N_WEEKS`, `DGP_MASTER_SEED`, `tuple_index`) | The panel is **one** 520-week realisation per tuple, seeded `DGP_MASTER_SEED + tuple_index(...)`. §1 rests on this. |
| `lab/analysis/c1/shape_feasibility_map_2026-08/run_region_sweep.py` (`score_cell`, `_run_with_days`, `se_of_proportion`, `gate_status`) | `se_bust = sqrt(p(1-p)/n_total_paths)` — path-sampling noise **from a fixed panel**. Reused unmodified by this campaign's probe. |
| `lab/discovery/prop_survivor_scoring.py` (`paired_blocks_from_daily`, `load_scoring_thresholds`) | No panel-length cap: the index is `pd.bdate_range("2020-01-06", periods=pnl.size)`, so a 5,200-week panel is accepted unchanged. Frozen seeds `(42,123,2026)`, horizon `1500`, ceiling `0.03`, floor `0.50`. |
| `core/mc/simulation.py` (`simulate_path`, `run_seed`) | `for day in range(horizon)` — **horizon is business days**. 1500 bdays = 5.95 years (§3). Engine reused unmodified; never re-implemented. |
| `lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/run_evalseq_orb_intraday.py` (`pol_cushion`, `day_loop_intraday`, `build_k_panel`) | `m = 0.75·min(1, cushion/DD)`; `d = pnl_at_base_k · m`; `base_k ∈ {1,2}`. §4 rests on this. |
| `core/firm_rules.py` — all five `Tradeify_*` blocks + both `MFFU_Rapid_*` | `max_dd_pct` / `profit_target_pct` per tier. The 25K/50K rows carry **4.0%** DD against a 6.0% target; 100K/150K carry **3.0%**. §5 rests on this. |
| `lab/analysis/c1/eval_inverse_requirements_2026-08-03/RESULTS.md` §2/§2a | Prior art for the inverse question, in (edge, trades/day) space. Its 0.139R row is used in §2 as an **independent** corroboration of the bound derived here. |
| `docs/adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md` | The 0.85R cell is a phantom; ORB-MNQ-1's realised edge is **+0.0626R**. Every edge figure below uses the corrected cohort. |

---

## §1 — The A2 map's dominant uncertainty is unreported

### §1.1 — Mechanism

`build_panel(win_rate, shape, cadence, risk)` draws **one** 520-week realisation, seeded only by the
tuple's own coordinates. `run_seed` then block-bootstraps 300 week-blocks *with replacement* **from
that one panel**. The bootstrap cannot escape the panel's realised mean — it *is* the drift every one
of the 1,500 (or 30,000) MC paths inherits.

At cadence 1 that panel contains **520 trades**. The standard error of its realised mean is
`σ_R/√(520·cadence)`, which for `symmetric`/`wr=0.55` is **±89% of the intended drift at 2 SE**:

| cadence | trades in panel | intended mean R | SE of panel mean | 2-SE band on drift | as % of intended |
|---:|---:|---:|---:|---|---:|
| 1 | 520 | 0.1000 | 0.0443 | [+0.0114, +0.1886] | **89%** |
| 2 | 1,040 | 0.1000 | 0.0313 | [+0.0374, +0.1626] | 63% |
| 3 | 1,560 | 0.1000 | 0.0256 | [+0.0489, +0.1511] | 51% |
| 5 | 2,600 | 0.1000 | 0.0198 | [+0.0604, +0.1396] | 40% |
| 8 | 4,160 | 0.1000 | 0.0157 | [+0.0687, +0.1313] | 31% |

**`se_bust` does not contain any of this.** It is `sqrt(p(1-p)/N)` over MC paths drawn from the fixed
panel — it measures re-sampling, not re-drawing.

### §1.2 — Measured on the committed grid

Within a `(win_rate, shape, risk)` group the per-trade edge is **identical by construction**; only
cadence differs. So the spread across those five cells is an upper bound on how much cadence plus
noise can move a verdict:

| group | bust range across cadence | spread | max reported 2·se_bust | ratio |
|---|---|---:|---:|---:|
| wr0.55 `symmetric` $275 | 0.355 – 0.882 | 0.527 | 0.0258 | **20.5×** |
| wr0.50 `bounded_clustered` $250 | 0.497 – 0.920 | 0.423 | 0.0258 | 16.4× |
| wr0.55 `symmetric` $250 | 0.360 – 0.688 | 0.328 | 0.0258 | 12.7× |
| wr0.45 `mild_right_skew` $250 | 0.329 – 0.590 | 0.261 | 0.0258 | 10.1× |
| wr0.50 `mild_right_skew` $250 | 0.029 – 0.236 | 0.207 | 0.0219 | 9.5× |

Over **all 63** comparable groups (7 win rates × 3 shapes × 3 risk levels), **49 (78%)** have a
cadence spread exceeding their own reported 2σ bar — median exceedance **4.3×** among those, max
**20.5×**. Direction reverses along the cadence axis in **120 of 189** adjacent pairs (**63%**) — the
signature of noise, not of a lever, and the reason A2 §7.4's *"cadence is a second-order lever"*
cannot be read off this grid either way.

### §1.3 — Reproduced directly from the panels

Rebuilding each committed panel and comparing its realised drift to the DGP's intended drift:

* median |z| of the realised panel mean = **0.68** (a well-behaved standard-normal draw — the
  generator is fine; 520 weeks is simply too short),
* **96 of 315 (30%)** panels sit more than 1 SE from their intended drift,
* the single most extreme draw in the grid is **`wr0.50_mild_right_skew_cd2_rk250`** at
  **z = +3.12**, realised drift **1.50×** intended.

That cell is **exactly** the one A2 §13.2 uses to falsify §7.2 and to headline the Growth tier.

The second-most relevant outlier is `wr0.55_symmetric_cd1_rk275` at **z = −2.48**, realised drift
**−0.10×** intended (a panel that is flat-to-negative despite a +0.10R intended edge) — which is why
that cell reads bust 88.2% where its own edge implies ~12%.

### §1.4 — Re-scored at a 10× panel (same code, same seed, same engine)

Nothing changes except `N_WEEKS`: same DGP, same tuple seed, same frozen seeds/horizon/`sims_per_seed`,
same intraday-honest limb, `simulate_path`/`run_seed` untouched. The probe first reproduces all six
committed cells **bit-exactly** at 520 weeks before any long-panel number is read.

| cell | 520wk verdict | 5,200wk verdict | bust 520 → 5,200 |
|---|---|---|---|
| wr0.50 `mild_right_skew` cd2 $250 — **Growth** | **FEASIBLE** | **INFEASIBLE** | 0.0093 → 0.0927 |
| wr0.50 `mild_right_skew` cd2 $250 — Select | MARGINAL | **INFEASIBLE** | 0.0287 → 0.1627 |
| wr0.60 `bounded_clustered` cd3 $275 — Select | MARGINAL | **INFEASIBLE** | 0.0360 → 0.0627 |
| wr0.55 `symmetric` cd1 $275 — Select | INFEASIBLE | INFEASIBLE | 0.8820 → 0.4167 |
| wr0.70 `mild_right_skew` cd8 $325 — Select *(clean control)* | FEASIBLE | FEASIBLE | 0.0040 → 0.0027 |
| wr0.40 `symmetric` cd8 $325 — Select *(clean control)* | INFEASIBLE | INFEASIBLE | 0.9993 → 0.9993 |

Both clean controls hold in both directions. Every flip is in the near-gate population, and every
flip is **optimistic→pessimistic** — the short panel understates bust where verdicts are decided,
because a 520-week panel cannot contain the deep adverse week-runs the bootstrap needs to reassemble.

### §1.5 — What this does and does not disturb

**Disturbed (absolute boundary):** §6.3's per-shape win-rate floors, the `MARGINAL` population,
§7.2's scoping amendment, §7.4's "cadence is a second-order lever", and §13.2's Growth headline.

**Not disturbed (relative comparisons):** Select and Growth were scored on the **same panels** (the
DGP seed does not include the firm), so §13.1's *38 improve / 277 unchanged / 0 degrade* and §13.3's
rope-benefit-by-win-rate curve are **paired** — panel noise cancels. **Checked, not assumed:** re-run
at 5,200 weeks the paired result is **33 improve / 282 unchanged / 0 degrade** (§6.1). The rope
finding replicates; the feasibility boundary does not. §6.1 of A2 (Select≡MFFU bit-identity) is
paired in the same way and stands.

**Why all three existing validation batteries miss this.** §4 (corner cases), §4.1 (MARGINAL band)
and §13.4 (Growth) each re-run **more paths** at `sims_per_seed=10,000` from the **same panel**.
`build_panel` does not read `sims_per_seed`. None of the three can detect panel-draw error, by
construction — which is why §4.1's two cells "stayed MARGINAL while their point estimates crossed the
gate line" is better read as panel noise surfacing than as calibration working.

**The fix is free.** `N_WEEKS` is a synthetic-DGP knob, not a data constraint, and
`paired_blocks_from_daily` has no length cap. Ten× the panel costs ~1.5 s of extra panel build per
cell and **nothing** in engine time. (For a *real* campaign the panel is the actual history and this
noise is irreducible; for a synthetic coverage map it is avoidable and was not avoided.)

---

## §2 — The venue requirement is size-invariant

For a construct with per-trade edge `μ` and dispersion `σ` (in R), traded at `r` dollars of risk per
trade, against a trailing rope `D` and a profit target `T`:

```
P(max drawdown from running peak ≥ D)  ≈  exp(−2·μ·D / (σ²·r))          [drifting random walk]
trades needed to reach the target       =  T / (μ·r)
```

Set the first equal to the frozen bust ceiling `b` and **eliminate `r`**:

```
n_min       = (T/D) · (ln(1/b)/2) · (σ/μ)²
T_min (yr)  = (T/D) · (ln(1/b)/2) / annSR²        annSR = (μ/σ)·√(trades per year)
```

**Position size cancels.** This is the formal content of the NAS100 ORB-30 finding that *"no risk
level is both safe and passes the challenge usefully"*
([`orb_universe_2026-06-22/RESULTS.md`](../../orb/orb_universe_2026-06-22/RESULTS.md) §3) — that is a
theorem about the ratio `T/D`, not an empirical accident of one sizing sweep. Sizing down trades bust
for timeout at constant quality; it never buys pass rate.

**Validation against the A2 map's own cells** (conditional on `bust ≤ 3%`, since over-risked cells
reach the target faster precisely *because* they breach the ceiling):

| tier | bust-compliant cells honouring the bound | violations |
|---|---:|---:|
| `Tradeify_Select_100K` | 105 | **1** |
| `Tradeify_Growth_100K` | 125 | **1** |

The bound is **tight exactly where it should bind** — for cells with bust in (2%, 3%], the measured
median-days-to-pass sits 1.04–1.29× above `T_min`. The two violations are the **same tuple** on both
firms, and it is `wr0.50_mild_right_skew_cd2_rk250` — §1.3's z=+3.12 outlier. A cell that passes
faster than a validated theoretical floor allows, whose panel is the grid's most over-drifted draw,
is a panel artifact.

**Independent corroboration from prior art.** `eval_inverse_requirements_2026-08-03` §2a's thin-edge
row (`w=0.349, b=2.27`, edge 0.139R, 8 trades/day) has `μ/σ = 0.0904`, annSR **4.06** on a separate
harness → predicted `T_min` = **54 days**. That study's own measured median is **54 days**.

---

## §3 — The frozen gate's horizon is a six-year eval

`simulate_path` iterates `for day in range(horizon)` and the frozen horizon is **1500 business days
= 5.95 years**. So the frozen survivor-scoring limb *"P(pass) ≥ 50%"* means **"at least a coin-flip
chance of passing within six years"** — the pre-registration's own gloss is *"finite median-days-to-
target inside a practical horizon"*, and nothing in the estate states that horizon in calendar terms.

Rearranging §2: an `annSR = 0.768` construct has `T_min` = 5.95 years on `Tradeify_Select_100K`. The
repo's frozen Stage-6 admission gate is **annSR ≥ 0.85**. **The two gates are calibrated to each
other** — the pipeline admits, coherently, at the edge of a six-year eval.

What the venue asks for if the eval is meant to finish in a business-relevant time:

| target time to pass | `Select_100K` | `Growth_100K` | `Select_50K` / `25K` |
|---|---:|---:|---:|
| ~3 months | **3.75** | 3.47 | 3.24 |
| ~6 months | **2.65** | 2.45 | 2.29 |
| 1 year | **1.87** | 1.73 | 1.62 |
| 2 years | 1.32 | 1.23 | 1.15 |

Against the corpus. Every construct that publishes an annualised Sharpe — the ORB/ICT ledger's own
scope **plus the four live TNEC construct lanes**, which already report `annSR` in their G0/G2
headline tables and are therefore screenable for free at intake (corrected cohort throughout):

| construct | annSR | `T_min` Select_100K | Growth_100K | Select_50K |
|---|---:|---:|---:|---:|
| ORB-MNQ-1, 2021+ best cell — **corpus maximum** | **1.280** | 2.1 y | 1.8 y | 1.6 y |
| NAS100 ORB-30 CFD 2020-26 (t +2.94, n 1663) | 1.154 | 2.6 y | 2.3 y | 2.0 y |
| ORB-MNQ-1, 2021+ @ Tradeify cost | 1.140 | 2.7 y | 2.3 y | 2.0 y |
| ORB-MNQ-1, best admissible `close_tod` 13:45 | 0.934 | 4.0 y | 3.4 y | 3.0 y |
| ORB-MNQ-1, full window @ Bulenox cost | 0.890 | 4.4 y | 3.8 y | 3.3 y |
| ORB-MNQ-1, full window @ Tradeify cost | 0.835 | 5.0 y | 4.3 y | 3.8 y |
| `Q-TNEC-CON-3` HTF native break, long — best live lane | 0.405 | 21.4 y | 18.3 y | 16.0 y |
| `Q-TNEC-CON-4` PDH/PDL break, short | 0.085 | 485 y | 416 y | 364 y |
| ICT raid→FVG chain at its frozen DOL target | ~0 | never | never | never |
| `Q-TNEC-CON-4` PDH/PDL break, long | −0.128 | never | never | never |
| `Q-TNEC-CON-2` compression break, long | −0.404 | never | never | never |
| `Q-TNEC-CON-5` impulse/pullback/VWAP, long | −0.532 | never | never | never |

**The highest annualised Sharpe ever published anywhere in this estate is +1.28** (ORB-MNQ-1, 2021+,
the most favourable Stage-7 cost/slip cell). That is short of even a **one-year** Select pass (1.87),
and 2.1× short of a six-month one.

**Nothing in the corpus is within 2.1× (in Sharpe) of a six-month Select pass.** This is not a
multiplicity, regime, or measurement failure — those were all real and all separately diagnosed. It
is an edge-magnitude gap, and it is the same gap at every tier. The four live TNEC lanes are one to
two orders of magnitude further away than the parked ORB construct is; the screen would have said so
at each lane's own G0 disclosure table, for $0.

**Breadth, quantified.** The rope and the 80-micro cap are per **account**, not per leg, so a book on
one account gets no extra rope; its only lever is portfolio Sharpe. For `k` independent legs of equal
Sharpe, `annSR → annSR·√k`, so `T_min` divides by `k`:

| tier | 6-month pass needs | legs at ORB-MNQ-1 **2021+** quality (1.140) | legs at **full-window** quality (0.835) |
|---|---:|---:|---:|
| `Select_100K` | annSR 2.65 | **5.4** | 10.1 |
| `Select_50K` | annSR 2.29 | **4.0** | 7.5 |

Stage-8 measured `corr(ORB-MNQ, Striker MNQ)` = **+0.15** over 339 overlapping weeks
([`RESULTS_stage8_neff.md`](../../orb/orb_mnq_2026-07/RESULTS_stage8_neff.md)), so near-independence
is genuinely available on this instrument family — the binding constraint on a book is **supply of
legs**, not correlation between them.

---

## §4 — `pol_cushion`'s bust-elimination needs sub-integer micro contracts

`pol_cushion` returns `m = 0.75 · min(1, max(cushion,0)/DD)` and the day loop applies
`d = pnl_at_base_k · m` with `base_k ∈ {1,2}`. So the policy's exposure is `m·base_k` **contracts**,
ranging over `[0, 0.75]` at `base_k=1` and `[0, 1.5]` at `base_k=2`.

**At full cushion, `base_k=1` asks for three-quarters of one micro contract.** The smallest position
the venue can express is one micro.

**Bust = 0.0000% is an identity, not a measurement.** To breach, a single day's 1-lot loss must reach
`DD/0.75 = $4,000`; ORB-MNQ-1's 1R is **$153.8** per micro (`net_1lot / n / meanR`, from the probe's
own committed Control G). `ops/instruments/MNQ.md` N17 already calls this *"mathematically
derivable"*. What is **not** on the record is that the **pass-rate lift** lives in the same
sub-integer regime.

Rounding the policy to whole micro contracts with a ≥1 floor, on panels calibrated to ORB-MNQ-1's own
published Control-G moments (5 independent draws):

| policy | bust % (mean [min,max]) | pass % (mean [min,max]) |
|---|---|---|
| flat k=1 | 47.72 [42.13, 51.72] | 52.28 [48.28, 57.87] |
| flat k=2 | 67.61 [64.23, 69.65] | 32.39 [30.35, 35.77] |
| `pol_cushion` k=1 — **fractional, as modelled** | **0.00** [0.00, 0.00] | 66.39 [62.42, 70.18] |
| `pol_cushion` k=2 — fractional | **0.00** [0.00, 0.00] | 68.77 [63.18, 73.75] |
| `pol_cushion` k=1 — **→ whole contracts** | **47.72** [42.13, 51.72] | **52.28** [48.28, 57.87] |
| `pol_cushion` k=2 — → whole contracts | 49.25 [44.73, 53.33] | 50.75 [46.67, 55.27] |

**The integer arm reproduces flat k=1 to the last digit on every draw** — as it must: every value of
`m ∈ [0, 0.75]` maps to exactly one contract under `max(1, round(·))`. The integer-rounded cushion
policy *is* flat k=1, the configuration the 2026-08-03 ADR already records `FALSIFIED` at 67.67% bust.

No re-parameterised integer ladder rescues it. `contracts = max(1, floor(f·cushion/1R))` over
`f ∈ {0.02 … 0.50}`: bust **75.6% → 92.2%** (rising with `f`, since the 1-contract floor keeps the
downside while `f` only adds upside size), pass **24.4% → 7.8%** — no cell clears either limb. Replacing
the 1-contract floor with a **stand-down** below a cushion threshold drives bust to 0.00% but pass to
**8.0–19.6%** — §2's size-invariance exactly: bust converts to timeout, never to pass.

**Consequence for `Q-ORBSURV-1`.** Its comfortable post-break clears (k=1 **81.35%** pass, k=2
**64.11%** pass, both at 0.0000% bust) — the corpus's single most deployment-shaped pair of numbers —
are **not reachable at MNQ micro granularity**. The closure's own framing ("configuration-dependent",
"does not establish that cushion sizing is a bad mechanism generally") is correct as far as it goes;
this adds the constraint that decides it, and the constraint is the contract multiple, not the regime.

**Scope limit, stated plainly.** The vendor panel is gitignored and absent from this clone, so the
table above uses a synthetic panel calibrated to the campaign's published Control-G moments; its
**absolute** levels do not reproduce the published 67.67% (this reconstruction runs benign at ~47.7%).
The **identity** — integer `pol_cushion` ≡ flat k=1 — is provable from `run_evalseq_orb_intraday.py`
alone and needs no simulation; the table is corroboration, not the argument. Re-running the real
harness with a `max(1, round(·))` wrapper would settle the pass-rate magnitudes and is the named
follow-on if anyone wants them.

---

## §5 — The tier axis A2 never scored

A2 scored three `$100K` tiers. `core/firm_rules.py` carries **five** Tradeify tiers, and the small
ones have a **structurally easier geometry**: Select 25K/50K run a **4.0%** drawdown against the same
**6.0%** target, where 100K/150K run **3.0%**.

| tier | rope $ | target $ | target/rope | `C` | annSR for a 6-month pass | micro cap | rope ÷ 1R at 1 micro (MNQ ORB) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `Tradeify_Select_25K` | 1,000 | 1,500 | **1.500** | 2.630 | **2.29** | 10 | 6.5 R |
| `Tradeify_Select_50K` | 2,000 | 3,000 | **1.500** | 2.630 | **2.29** | 40 | 13.0 R |
| `MFFU_Rapid_50K` | 2,000 | 3,000 | **1.500** | 2.630 | **2.29** | 50 | 13.0 R |
| `Tradeify_Growth_100K` | 3,500 | 6,000 | 1.714 | 3.006 | 2.45 | 80 | 22.7 R |
| `Tradeify_Select_100K` | 3,000 | 6,000 | 2.000 | 3.507 | 2.65 | 80 | 19.5 R |
| `Tradeify_Select_150K` | 4,500 | 9,000 | 2.000 | 3.507 | 2.65 | 120 | 29.2 R |

**On the bound's own term the 50K tier is a larger improvement than the entire Growth tier** — 25%
off the `T_min` constant versus Growth's 14% — and it has been in `firm_rules.py` since 2026-07-10,
unscored.

**But that advantage is conditional, and §6.3 measures the condition.** `T_min` is size-invariant only
at each tier's *own* optimal size. A construct that carries a fixed dollar risk to a smaller tier gets
a shallower rope in R and loses far more than the ratio gives back: at the map's own `$275`, the 50K's
rope is **7.3 R** and it scores **44 `FEASIBLE` against Select_100K's 97**, with 68 cells degrading
and none improving. The discount is only collectable by re-sizing down with the rope (`× 2/3`), and
`rope ÷ 1R at one micro` is what says whether a given construct can:

* 25K → **6.5 R**: too coarse for an MNQ construct to express at all.
* 50K → **13.0 R**: workable, but MNQ ORB's 1R is `$153.8`/micro, so at the 50K's proportional risk
  (`$167–$217`) it is pinned at one contract with no sizing room left.
* Growth 100K → **22.7 R**: the most granular of the five, and the only tier whose improvement needs
  **no** re-sizing at all (§6.3).

**Third counterweight:** funded-phase rules, payout policy, and eval purchase price differ per tier
and **none of that is measured here.** This is a geometry comparison, not a tier recommendation.

`§6` below reports the full 315-tuple grid re-scored at a 5,200-week panel against all four tiers.

---

## §6 — Full-grid re-score: 315 tuples × 4 tiers at a 5,200-week panel

All 315 committed tuples, re-scored at a 5,200-week panel against four tiers — the two A2 scored plus
the two Select tiers it did not. Same generator, same tuple seeds, same engine, same frozen
seeds/horizon/`sims_per_seed`, same intraday-honest limb.

**Two risk conventions, kept strictly apart.** Conflating them would misread the result, so both are
reported:

* **Matched risk** — the map's own `$250/$275/$325`, unchanged. This is A2 §13.1's convention and the
  one an operator faces: *given a construct with a fixed dollar risk, which tier is kindest?* A wider
  rope helps on **two** axes at once here (more R of rope **and** a better `target/rope`).
* **Rope-matched risk** — risk scaled `× rope/3000` so `rope ÷ risk` is **identical** across tiers and
  the *only* thing varying is `target/rope`. This isolates §2's ratio term, and is the right
  convention for comparing tiers each sized at its own optimum.

### §6.1 — Matched risk: A2 §13.1's paired rope finding replicates

Select_100K and Growth_100K, both at the map's own risk levels, both on 5,200-week panels — directly
comparable to §13.1's *"38 improve, 277 unchanged, 0 degrade"*:

| paired Select → Growth | unchanged | improve | degrade |
|---|---:|---:|---:|
| committed, 520-week panels | 277 | **38** | **0** |
| this pass, 5,200-week panels | 282 | **33** | **0** |

**It replicates.** 33 improve against 38, still zero degrade. This is the empirical confirmation of
§1.5's argument that paired Select-vs-Growth comparisons are immune to panel noise, and it means
**A2 §13.1 and §13.3 should be read as they stand.** The rope's benefit is real, and it is the size
§13 measured.

Committed-vs-long-panel stability at matched risk is likewise unremarkable for **both** tiers —
Select 290 / 12 / 13 (unchanged / degrade / improve), Growth 296 / 12 / 7. It is not the tier-level
counts that move under a longer panel. It is the **near-gate boundary**, which is where §13.2 lives.

### §6.2 — Matched risk: the win-rate floor, and §7.2

Lowest win rate carrying **any** `FEASIBLE` cell:

| tier / panel | `symmetric` | `mild_right_skew` | `bounded_clustered` |
|---|---:|---:|---:|
| `Select_100K` — committed 520wk | 65% | 55% | 60% |
| `Select_100K` — **5,200wk** | 65% | 55% | **65%** |
| `Growth_100K` — committed 520wk | 60% | 50% | 60% |
| `Growth_100K` — **5,200wk** | **65%** | **55%** | 60% |

**§13.2's headline does not reproduce.** At a proper panel Growth's `symmetric` and
`mild_right_skew` floors are **the same as Select's** (65% / 55%); only `bounded_clustered` keeps a
genuine 5-point advantage (60% vs 65%) — so the claim is one shape of three, not "two of three", and
the shapes it holds for are swapped.

Decisively: **zero cells at `win_rate ≤ 50%` are `FEASIBLE` on Growth**, at either risk convention.
**§7.2 as originally written stands** — and stands more strongly than when it was authored, since it
now holds on the wider rope too.

### §6.3 — The small tiers: a real advantage that is **conditional on re-sizing**

This is the part that most needs both conventions, because they disagree — and the disagreement is
the finding.

**Rope-matched risk** (each tier sized at comparable R-geometry, so only `target/rope` moves):

| tier | `target/rope` | `C` | `FEASIBLE` / `MARGINAL` / `INFEASIBLE` |
|---|---:|---:|---|
| `Tradeify_Select_25K` | 1.500 | 2.630 | **104** / 12 / 199 |
| `Tradeify_Select_50K` | 1.500 | 2.630 | **104** / 12 / 199 |
| `Tradeify_Growth_100K` | 1.714 | 3.006 | **101** / 12 / 202 |
| `Tradeify_Select_100K` | 2.000 | 3.507 | **97** / 15 / 203 |

Monotone in `target/rope` exactly as §2 predicts, and the two identical-geometry tiers (25K, 50K)
score **bit-identically** — a clean internal consistency check on the harness.

**Matched risk** (the map's own `$250/$275/$325`, i.e. a construct that does *not* re-size):

| tier | rope ÷ risk at $275 | `FEASIBLE` / `MARGINAL` / `INFEASIBLE` | paired vs Select_100K |
|---|---:|---|---|
| `Tradeify_Growth_100K` | 12.7 R | **115** / 15 / 185 | 33 improve, **0 degrade** |
| `Tradeify_Select_100K` | 10.9 R | 97 / 15 / 203 | — |
| `Tradeify_Select_50K` | **7.3 R** | **44** / 22 / 249 | **0 improve, 68 degrade** |

**At a fixed dollar risk the 50K tier is much worse, not better** — 44 `FEASIBLE` against 97, with
68 cells degrading and none improving; its floors move to 70% / 65% / 70%. The reason is in §2's own
scope: `$275` against a `$2,000` rope is **7.3 R**, and the bound's diffusion argument needs a rope
many R deep. The better `target/rope` ratio cannot pay for a rope that shallow.

**So the two conventions are both right, about different things.** The 50K's 25% geometric advantage
is real, and it is **only accessible to a construct that re-sizes down with the rope** — to roughly
`× 2/3` the dollar risk. That is a hard constraint, not a formality: MNQ ORB's 1R at one micro is
**$153.8**, so at the 50K's proportional risk (`$167–$217`) it is pinned at one contract with no room
to size at all. **A construct only collects the small-tier discount if its natural 1R is small enough
to express there** — which favours a tighter-stop construct, or MES, over MNQ ORB.

**Growth is the exception, and it is unconditional.** A wider rope at the *same* dollar risk improves
both terms at once — more R of rope **and** a better `target/rope` — which is why it is the one tier
move that is free: **33 improve, 0 degrade, no re-sizing required.** §13's rope finding was right; it
is §13.2's *boundary* claim that does not survive.

### §6.4 — The §13.2 headline cell, under both conventions

| tier | committed (520wk) | 5,200wk, matched risk | 5,200wk, rope-matched risk |
|---|---|---|---|
| `Tradeify_Growth_100K` | `FEASIBLE` (bust 0.0093) | **`INFEASIBLE`** (0.0927) | **`INFEASIBLE`** (0.1393) |
| `Tradeify_Select_100K` | `MARGINAL` (bust 0.0287) | **`INFEASIBLE`** (0.1627) | **`INFEASIBLE`** (0.1627) |

Same verdict under both conventions, so the flip is not an artifact of §6.3's scaling choice.

---

## §7 — R2 trigger check (recorded, not self-executed)

The ORB re-park ADR's **R2** reads: *"Tradeify venue geometry materially loosens at the $100K band —
a tier change (static DD, larger trail, or a documented trail mechanism other than the $3,000
intraday-enforced one) under which k=1 clears **both** frozen limbs on the unedited survivor-scoring
protocol"*, with the trigger check scheduled *"on any Tradeify rule-pin re-verification."*

`Tradeify_Growth_100K` landed **2026-08-24** with a **larger trail** ($3,500) at the $100K band, off a
rule-pin re-verification. That is R2's scheduled check, and it is due.

**Answer: R2 does not fire.** A2 §13.3 measures the rope's benefit at **−1.6 pp (wr 40%)** to
**−3.7 pp (wr 45%)** — the win-rate band in which ORB-MNQ-1's edge sits — and ORB-MNQ-1 at k=1 is
**67.67%** bust against a **3.0%** ceiling. §2's bound says the same thing without a simulation: the
rope moves `C` from 3.507 to 3.006 (−14%), against ORB-MNQ-1's own 2.3× gap in Sharpe. R2 requires k=1 to clear
**both** limbs; it clears neither, at either rope.

Recording the check as discharged is the point. **This ADR is not amended, no unpark is proposed, and
R3 is untouched** — a tier move to 50K would be an R3 proposal requiring its own operator GO,
pre-registration, and a survivor-scoring pass *before* unparking, exactly as R3 specifies.

---

## §8 — Limitations

1. §2's bound is a **diffusion approximation**: it assumes the rope spans enough R for a
   drifting-random-walk argument (it is loose below ~5 R of rope) and treats trades as i.i.d. It is
   validated as a **floor** — 230 of 232 bust-compliant A2 cells honour it — not as a predictor of
   bust level. It never blesses a candidate; it kills one.
2. §1's long-panel re-score is at `sims_per_seed=500` (the committed sweep's own reduced N), so its
   cells carry the same path-noise bars A2's do. That is not the axis under test.
3. §4's cushion table uses a **reconstructed** panel (vendor data gitignored/absent); absolute levels
   do not reproduce the published figures. The identity it demonstrates is provable without it.
4. No funded-phase rule, eval purchase price, or payout policy is measured anywhere here. §5 is a
   geometry comparison, not a tier recommendation.
5. Every Growth figure inherits A2 §13.6's two-sided bound (soft-DLL omitted → pessimistic; intraday
   clock → `Q-FIRMEOD-1` lower bound), and the owed re-verification of art. 10495897 *for Growth
   specifically* is still owed.

---

## Verification

```bash
# The probe reproduces the committed A2 cells bit-exactly before any long-panel number is read
python lab/analysis/c1/a2_panel_noise_venue_bound_2026-08-24/panel_noise_probe.py --mode reproduce
# Expected: MATCH on all six cells

# The 10x-panel re-score (section 1.4)
python lab/analysis/c1/a2_panel_noise_venue_bound_2026-08-24/panel_noise_probe.py --mode longpanel
# Expected: the three near-gate cells flip; both clean controls hold

# The bound + its validation against the committed A2 JSONL (section 2, 3, 5)
python lab/analysis/c1/a2_panel_noise_venue_bound_2026-08-24/venue_bound.py
# Expected: 105 and 125 cells honour the bound; 1 violation each, the same tuple

# Integer-contract granularity (section 4)
python lab/analysis/c1/a2_panel_noise_venue_bound_2026-08-24/cushion_integer_granularity.py
# Expected: "pol_cushion base_k=1 -> integer" reproduces "flat k=1" exactly

# Full-grid re-scores (section 6). Raw output is committed; these regenerate it (~5 min each, 3 procs).
python lab/analysis/c1/a2_panel_noise_venue_bound_2026-08-24/longpanel_tier_sweep.py       # rope-matched, 4 tiers
python lab/analysis/c1/a2_panel_noise_venue_bound_2026-08-24/longpanel_matchedrisk_sweep.py # matched risk, one tier
python lab/analysis/c1/a2_panel_noise_venue_bound_2026-08-24/analyze_longpanel.py           # reads the committed JSONL

# The two risk conventions are NOT interchangeable -- the analyzer prints its own warning.
# Committed raw: longpanel_ropematched.jsonl (1,260 rows, 4 tiers, risk x rope/3000)
#                longpanel_growth_matchedrisk.jsonl   (315 rows, map's own risk)
#                longpanel_select50k_matchedrisk.jsonl (315 rows, map's own risk)

# The claim that pol_cushion never asks for one whole contract at base_k=1
grep -n "return 0.75 \* np.minimum" lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/run_evalseq_orb_intraday.py
# Expected: m <= 0.75, and build_k_panel supplies base_k in {1,2}

# The horizon is business days (section 3)
grep -n "for day in range(horizon)" core/mc/simulation.py
# Expected: one hit -- 1500 bdays = 5.95 years

# The small tiers carry a 4% rope against a 6% target (section 5)
grep -n "max_dd_pct" core/firm_rules.py | sed -n '1,20p'
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-24 | Initial authoring — panel-draw noise diagnosis + 10× re-score, size-invariant venue bound + validation, integer-granularity test of `pol_cushion`, tier-geometry table, R2 check | Claude Code |
