# MES MOC-fade — Table-mode replay on real MES bars (2026-09-02)

**Data:** Databento GLBX.MDP3 `MES.v.0` ohlcv-1m (volume-rolled = TV `MES1!`), 2025-03-02..2026-09-01, $0.00 pull, 532,738 bars. Interval-start stamps verified; one instrument_id per session inside 16:00-16:45 ET (no roll in-window). 45-46 one-minute bars per session in the window.

**Signal:** FinancialJuice S&P 500 MOC imbalance. 342 sessions scraped; **235 usable** (see the sign caveat below).

**Execution modelled on the Pine, 5m bars:** entry = market at the OPEN of the bar stamped 16:05 (order placed at the 16:05 close of the 16:00 bar); stop/target first fillable on the bar stamped 16:10 (entry bar unprotected, the repo's standing rule); flatten at the OPEN of the bar stamped 16:40; adverse-first on same-bar stop+target; a gapped stop fills at the worse of level and next open. Costs $0.91/side; a 1-tick/side slippage variant reported.

## Shape, verified-sign sessions only (n=143 after the $0.5bn filter)

| cell | n | WR net | mean R net | PF net | t net | mean R gross | t gross |
|---|---:|---:|---:|---:|---:|---:|---:|
| 5m pess target | 143 | 51.7% | -0.1195 | 0.685 | -1.72 | -0.0589 | -0.84 |
| 5m pess no-target | 143 | 45.5% | -0.1262 | 0.694 | -1.49 | -0.0656 | -0.78 |
| 5m optim target | 143 | 53.8% | -0.0356 | 0.885 | -0.63 | +0.0251 | +0.44 |
| 5m optim no-target | 143 | 44.8% | -0.0953 | 0.745 | -1.28 | -0.0347 | -0.47 |
| 1m pess target | 143 | 58.0% | -0.0164 | 0.951 | -0.27 | +0.0443 | +0.72 |
| 1m pess no-target | 143 | 49.7% | -0.0018 | 0.995 | -0.02 | +0.0589 | +0.71 |
| 1m optim target | 143 | 60.1% | +0.0294 | 1.097 | +0.49 | +0.0900 | +1.51 |
| 1m optim no-target | 143 | 49.7% | +0.0072 | 1.019 | +0.09 | +0.0679 | +0.83 |

## The decisive reads

| test | result |
|---|---|
| Raw window return, faded, no stop/target/filter (n=234) | **+0.449 pts = +0.075R**, t=+0.82 |
| 95% CI on that edge | **[-0.104R, +0.254R]** — spans zero AND spans the 0.10R minimum |
| 4x cost-law pre-screen (needs gross >= 1.46 pts on commission alone; 3.46 pts on B1.0's own Tradeify crossing model) | **FAIL** at +0.449 pts |
| Scales with imbalance size? (a dealer-inventory mechanism must) | **No.** 0-500 +0.73 / 500-1000 +0.42 / 1000-2000 -0.35 / 2000+ +1.10 pts; corr(abs imb, return) +0.025 |
| corr(signed imbalance, window return) | **-0.036** (right sign, indistinguishable from zero; CI half-width 0.129) |
| Both halves (faded, raw) | H1 -0.218 pts (t=-0.45) / H2 +1.115 pts (t=+1.14) — **sign flips** |
| Sessions needed for 80% power at 0.10R | **~1,524**; we have 234 |
| corr with the MNQ recon leg's daily P&L (n=133 shared days) | **+0.069** — the one attribute it passes |

**Verdict: underpowered non-result that fails the cost-law pre-screen — not a clean kill, and not a candidate.** The gross point estimate (+0.075R) sits below the 0.10R minimum the third-leg grid requires and below the 4x cost hurdle; after real costs every one of the 8 configurations lands between -0.13R and +0.03R. The mechanism-level check is the strongest evidence against it: the effect does not grow with imbalance size, which a forced dealer-unwind must.

**K disclosed:** 27 looks total (16 cells on the contaminated table, 8 clean cells, 2 directional tests, 1 size-bucket read). Best t anywhere = 1.51 gross. No multiplicity correction changes the reading.

## Sign caveat (load-bearing)

FinancialJuice posts in two formats: inline-sign, and colour-coded where bare absolute magnitudes carry their side in a red/green marker. **The Telegram mirror renders that marker as a plain exclamation mark**, so 107 of 342 days have an unrecoverable sign. My first pass assumed bare = buy-side; that is falsified by the X original for **2025-04-30** (status 1917668077795238199), which is red (sell-side) with digits identical to the row stored as buy-side. Those 107 days are flagged in the CSV and **excluded from the Pine table** (now 235 rows). Recovering them needs the X originals or FinancialJuice Elite.
