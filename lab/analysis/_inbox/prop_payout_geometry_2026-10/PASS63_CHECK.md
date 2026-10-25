# PASS63 check: Select 100K pass within 63 trading days vs true Sharpe (2026-10-25)

**Verdict:** The claim is reproduced. Two independent engines match the coordinator's curve within 1.0 pp at every Sharpe; no gap from the claim exceeds 3 pp. Research input only, on synthetic Gaussian strategies; no decision is made here.

**Question.** For a fresh Tradeify Select 100K evaluation, what is P(pass within 63 trading days) as a function of the strategy's true annualised net Sharpe (SR), at the daily σ that maximises it? This checks the requirement curve the coordinator's portfolio decision leans on.

**Budget.** One grid run plus one identical re-run to check reproducibility; $0; K = 0 (synthetic strategies, no candidate tested).

## Engines

- **A:** `core.mc.simulation.simulate_path` with `firm_kwargs("Tradeify_Select_100K", consistency=0.40)` and `horizon=63`. Protection is inert (`dd_trigger=1`, `dd_scale=1`) and the inactivity barrier is off (the `firm_kwargs` default). The path generator is new and written here:
  - daily close X = SR·σ/√252 + σZ;
  - `intraday_low` is the exact Brownian-bridge minimum given X, m = (X − √(X² − 2σ² ln U))/2.
  - Self-check against the closed form for drifted Brownian motion: P(low ≤ −1σ | μ = 0.1σ) = 0.2861 simulated vs 0.2864 exact (SE 0.0005).
- **B:** `payout_sim.run_phase` on `tradeify(100)["TFY Select Flex 100K"].ev`: $6K target, $3K end-of-day trailing floor, 40% consistency, 3 minimum days. Single attempt, no resets, no stop or take, `days_left = 63`, 26 discrete intraday steps.
- **Both:**
  - σ is searched from $200 to $1,800 in $100 steps, with common random numbers across σ within each engine.
  - 20,000 paths per cell; SE = √(p(1−p)/N).

## 63 days

P(pass) at the best σ (σ in brackets):

| SR | Claim | A: simulate_path | B: payout_sim | A − claim | B − claim |
|---|---|---|---|---|---|
| 0 | 0.151 (900) | 0.150 ± 0.003 (1,000) | 0.157 ± 0.003 (800) | −0.001 | +0.006 |
| 1.0 | 0.248 (700) | 0.248 ± 0.003 (700) | 0.258 ± 0.003 (700) | +0.000 | +0.010 |
| 1.5 | 0.312 (600) | 0.308 ± 0.003 (600) | 0.319 ± 0.003 (600) | −0.004 | +0.007 |
| 2.0 | 0.388 (600) | 0.384 ± 0.003 (600) | 0.392 ± 0.003 (600) | −0.005 | +0.004 |
| 2.5 | 0.465 (600) | 0.462 ± 0.004 (600) | 0.470 ± 0.004 (600) | −0.003 | +0.005 |
| 3.0 | 0.542 (600) | 0.544 ± 0.004 (600) | 0.552 ± 0.004 (600) | +0.002 | +0.010 |
| 4.0 | 0.699 (500) | 0.698 ± 0.003 (500) | 0.703 ± 0.003 (500) | −0.001 | +0.004 |

Outcome split at that σ, and the σ range within 1 pp of the best:

| SR | A pass / bust / running | A σ within 1 pp | B pass / bust / running | B σ within 1 pp |
|---|---|---|---|---|
| 0 | 0.150 / 0.850 / 0.000 | 700–1,200 | 0.157 / 0.841 / 0.002 | 700–1,200 |
| 1.0 | 0.248 / 0.741 / 0.011 | 600–800 | 0.258 / 0.730 / 0.012 | 600–800 |
| 1.5 | 0.308 / 0.639 / 0.053 | 600–700 | 0.319 / 0.621 / 0.060 | 600–700 |
| 2.0 | 0.384 / 0.564 / 0.053 | 600 | 0.392 / 0.551 / 0.057 | 600–700 |
| 2.5 | 0.462 / 0.488 / 0.050 | 600 | 0.470 / 0.476 / 0.053 | 600 |
| 3.0 | 0.544 / 0.414 / 0.042 | 600 | 0.552 / 0.402 / 0.046 | 600 |
| 4.0 | 0.698 / 0.202 / 0.100 | 500 | 0.703 / 0.189 / 0.108 | 500–600 |

**Selection bias.** Re-estimating each engine at its chosen σ on a fresh seed moves A by −0.001 to +0.006 and B by −0.002 to +0.004. Picking the maximum over the grid therefore shows no upward bias.
- A's fresh-seed values are slightly higher (mean +0.3 pp). That fits one shared grid draw (common random numbers across every SR) landing slightly low.

## Gaps and their causes

No engine differs from the claim by more than 1.0 pp. The differences below are smaller than 3 pp, apart from the end-of-day-only model, which is a different model rather than a disagreement.

- **Path granularity (B − A = +0.5 to +1.1 pp at 63 days; positive in all 11 SR × horizon cells).**
  - `run_phase` tests the floor at 26 points a day and misses crossings between them. Engine A sees the exact bridge minimum.
  - The standard discrete-monitoring correction is 0.5826·σ·√(1/26) ≈ 0.11σ, about $70 at σ = $600. In effect B runs on a $3,070 rope.
  - At 390 steps a day (fresh seed, at A's σ), B falls to +0.1 to +0.6 pp above A; the SE of that difference is about 0.5 pp.
  - So the claim agrees with the continuous engine (A). B reads about 1 pp optimistic.
- **Consistency handling.** Identical in both engines: the best close-to-close day must be ≤ 40% of profit, tested at each close. It can only delay a pass.
  - Turned off in A at the same σ, it adds 0.7 pp at SR 0, where at σ = $1,000 a single day above $2,400 (2.4σ) is plausible.
  - It adds 0.000 at every SR ≥ 1.
- **Floor arithmetic.**
  - `simulate_path` rounds: a breach fires within about $0.05 of the floor, and the target needs $106,000.01.
  - `payout_sim` compares exactly.
  - The difference is immaterial at this precision.
- **Best σ.**
  - It matches the claim at every SR ≥ 1. For SR 2.0 to 3.0 the optimum is sharp at $600 in A.
  - At SR 0 the claim gives $900, A $1,000 and B $800. The curve is flat within 1 pp from $700 to $1,200, so a $100 grid cannot separate them.
- **End-of-day-only breach** (engine A, `intraday_low=None`):

  | SR | Same σ | Own σ search |
  |---|---|---|
  | 0 | 0.195 (+0.044) | 0.195 at $1,000 (+0.044) |
  | 1.0 | 0.291 (+0.043) | 0.294 at $800 (+0.046) |
  | 1.5 | 0.343 (+0.035) | 0.361 at $700 (+0.053) |
  | 2.0 | 0.424 (+0.040) | 0.437 at $700 (+0.054) |
  | 2.5 | 0.510 (+0.048) | 0.511 at $700 (+0.049) |
  | 3.0 | 0.594 (+0.050) | 0.594 at $600 (+0.050) |
  | 4.0 | 0.722 (+0.024) | 0.741 at $600 (+0.043) |

  With its own σ search, end-of-day-only reads +4.3 to +5.4 pp high. That matches the coordinator's "roughly +4–6 pp".

## 126 days

| SR | A: P ± SE (σ) | A pass / bust / running | B: P ± SE (σ) | B pass / bust / running | B − A |
|---|---|---|---|---|---|
| 0 | 0.153 ± 0.003 (900) | 0.153 / 0.847 / 0.000 | 0.156 ± 0.003 (800) | 0.156 / 0.844 / 0.000 | +0.003 |
| 1.0 | 0.291 ± 0.003 (500) | 0.291 / 0.703 / 0.006 | 0.296 ± 0.003 (500) | 0.296 / 0.697 / 0.007 | +0.005 |
| 2.0 | 0.511 ± 0.004 (400) | 0.511 / 0.434 / 0.055 | 0.523 ± 0.004 (400) | 0.523 / 0.416 / 0.060 | +0.012 |
| 3.0 | 0.718 ± 0.003 (400) | 0.718 / 0.250 / 0.032 | 0.725 ± 0.003 (400) | 0.725 / 0.242 / 0.033 | +0.007 |

- σ within 1 pp of the best, in A:
  - $500–1,100 at SR 0;
  - $400–500 at SR 1;
  - exactly $400 at SR 2 and 3.
- Fresh-seed re-estimates move A by −0.005 to +0.003 and B by −0.007 to +0.002.
- Doubling the horizon raises P at SR 2 from 0.38 to 0.51, and the best σ falls from $600 to $400.
- Zero edge barely moves (0.150 → 0.153), because high-σ paths resolve within a few weeks.
- The 200-day figures in the [metrics memo §3](../../../../docs/notes/research/2026-10-21-q-prop-trader-metrics-1-memo.md#3-implications-for-tradeify-select-100k) were not re-run here.

## Limits

Both engines share the claim's model, so this checks the implementation, not the model:
- i.i.d. Gaussian days (no fat tails, autocorrelation or regimes);
- the day opens at the prior close, with continuous trading through the session;
- fixed σ, with no sizing response to distance from the floor;
- the inactivity barrier is off;
- no costs outside the Sharpe.

The [RESULTS.md limit](RESULTS.md#known-limits) applies: the i.i.d. Gaussian assumption favours high σ more than fat tails would.

## Reproduce

`python -I scripts/fp.py python lab/analysis/_inbox/prop_payout_geometry_2026-10/pass63_check.py` prints every table above. It took 5.5 minutes on 4 workers, with fixed seeds, and the worker count does not change the results.
- First run: base `86995cf` plus this script, interpreter `tmp/ops-env` Python 3.12.3, `fp doctor` reporting 62 locked packages matched; exit 0.
- An identical second run produced byte-identical output.
- Plain `python3 -I lab/analysis/_inbox/prop_payout_geometry_2026-10/pass63_check.py` on system Python 3.13.17 (numpy 2.5.3) also produced byte-identical output; exit 0.
