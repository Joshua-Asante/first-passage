# MES MOC-fade — Table-mode replay on real MES bars

**Corrected 2026-09-02** after Codex review of [PR #260](https://github.com/Joshua-Asante/first-passage/pull/260): the first version of this file quoted clean numbers while the committed artifacts were generated with unverified-sign rows included, and every time exit was priced one bar early. Both are fixed; the verdict is unchanged. See §Corrections.

**Data:** Databento GLBX.MDP3 `MES.v.0` `ohlcv-1m` (volume-rolled = TV `MES1!`, per `lesson_roll_rule_changes_bar_existence`), 2025-03-02→2026-09-01, **$0.0000** pull, 532,738 bars. Decoded `map_symbols=False`; interval-START stamps verified; one `instrument_id` per session inside 16:00–16:45 ET, so no contract roll falls in-window; 45–46 one-minute bars per session in the window.

**Signal:** FinancialJuice S&P 500 MOC imbalance. **342 sessions scraped, 235 used** — the other 107 carry their side in a colour marker the Telegram mirror destroys (see `scrape/README.md`). Every figure below is verified-sign only.

**Execution, matched to the Pine on 5m bars** (bar stamped T covers T..T+5, closes at T+5): signal bar = first bar closing ≥ 16:01 (stamped 16:00); entry = market at the **OPEN of the bar stamped 16:05**; stop/target generated at the close of the bar the entry executes on, so first fillable on the bar stamped 16:10 (pessimistic, `lesson_tv_exit_cannot_fill_on_entry_bar`) — an optimistic variant is reported alongside; `close_all` submitted at the close of the bar stamped 16:35 and **filled at the OPEN of the bar stamped 16:40**; adverse-first when one bar holds both stop and target; a gapped stop fills at the worse of its level and that bar's open. Costs $0.91/side ($1.82 RT = 0.364 pts); a 1-tick/side slippage variant is carried throughout. MES $5/point, tick 0.25; stop 6.0 pts = $30/contract = 1R.

## All 16 configurations (verified-sign sessions only)

| cell | n | trades/wk | WR net | mean R net | PF net | t net | mean R gross | t gross | mean R net+slip |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `tf5m_pess_tgt_flt500` | 143 | 1.87 | 46.9% | -0.1137 | 0.699 | -1.63 | -0.0530 | -0.76 | -0.1828 |
| `tf5m_pess_tgt_flt0` | 234 | 3.05 | 49.1% | -0.1045 | 0.72 | -2.00 | -0.0438 | -0.84 | -0.1736 |
| `tf5m_pess_notgt_flt500` | 143 | 1.87 | 39.2% | -0.1079 | 0.738 | -1.24 | -0.0472 | -0.54 | -0.1912 |
| `tf5m_pess_notgt_flt0` | 234 | 3.05 | 42.7% | -0.0379 | 0.906 | -0.46 | +0.0228 | +0.28 | -0.1212 |
| `tf5m_optim_tgt_flt500` | 143 | 1.87 | 49.0% | -0.0295 | 0.904 | -0.52 | +0.0312 | +0.55 | -0.0977 |
| `tf5m_optim_tgt_flt0` | 234 | 3.05 | 51.3% | -0.0315 | 0.9 | -0.70 | +0.0292 | +0.65 | -0.0997 |
| `tf5m_optim_notgt_flt500` | 143 | 1.87 | 38.5% | -0.0712 | 0.808 | -0.92 | -0.0105 | -0.14 | -0.1545 |
| `tf5m_optim_notgt_flt0` | 234 | 3.05 | 42.3% | -0.0089 | 0.976 | -0.11 | +0.0518 | +0.67 | -0.0922 |
| `tf1m_pess_tgt_flt500` | 143 | 1.87 | 55.9% | -0.0187 | 0.944 | -0.30 | +0.0420 | +0.68 | -0.0849 |
| `tf1m_pess_tgt_flt0` | 234 | 3.05 | 55.1% | -0.0352 | 0.897 | -0.72 | +0.0255 | +0.52 | -0.1020 |
| `tf1m_pess_notgt_flt500` | 143 | 1.87 | 47.6% | -0.0108 | 0.972 | -0.13 | +0.0498 | +0.61 | -0.0942 |
| `tf1m_pess_notgt_flt0` | 234 | 3.05 | 47.0% | +0.0390 | 1.1 | +0.50 | +0.0997 | +1.28 | -0.0443 |
| `tf1m_optim_tgt_flt500` | 143 | 1.87 | 58.0% | +0.0270 | 1.089 | +0.45 | +0.0877 | +1.47 | -0.0382 |
| `tf1m_optim_tgt_flt0` | 234 | 3.05 | 56.8% | +0.0034 | 1.011 | +0.07 | +0.0641 | +1.37 | -0.0626 |
| `tf1m_optim_notgt_flt500` | 143 | 1.87 | 47.6% | -0.0018 | 0.995 | -0.02 | +0.0589 | +0.72 | -0.0851 |
| `tf1m_optim_notgt_flt0` | 234 | 3.05 | 47.0% | +0.0517 | 1.137 | +0.67 | +0.1124 | +1.46 | -0.0316 |

No configuration reaches the 0.10R minimum the third-leg grid requires. Best of 16 is `tf1m_optim_notgt_flt0` at +0.0517R — the most forgiving execution assumption with no size filter.

## The decisive reads

| test | result |
|---|---|
| Raw window return, faded, no stop/target/filter (n=234) | **+0.4487 pts = +0.0748R**, t=+0.82 |
| 95% CI on that edge | **[-0.1039R, +0.2535R]** — spans zero *and* spans the 0.10R minimum |
| 4× cost-law pre-screen | needs ≥ 1.46 pts on commission alone, or 3.46 pts on lane B1.0's own Tradeify crossing model. Measured +0.4487 pts → **FAIL** |
| Scales with imbalance size? (a forced dealer unwind must) | **No.** 0-500 $mln: +0.734 pts (n=91) / 500-1000 $mln: +0.417 pts (n=51) / 1000-2000 $mln: -0.353 pts (n=58) / 2000-inf $mln: +1.103 pts (n=34); corr(abs imbalance, faded) +0.0248 |
| corr(signed imbalance, window return) | **-0.0363** — right sign, indistinguishable from zero |
| Both halves (faded, raw) | H1 2025-03-14..2026-01-21 -0.218 pts (t=-0.45) / H2 2026-01-22..2026-09-01 +1.115 pts (t=+1.14) — **sign flips** |
| Sessions needed for 80% power at 0.10R | **~1,524**; we have 234 |
| Cadence | **1.87 trades/week** filtered, 3.05 unfiltered, over a 383-weekday span |
| corr with the MNQ recon leg's daily P&L | **+0.087** on days both traded — the one attribute it passes |

**Verdict: an underpowered non-result that fails the cost-law pre-screen — not a clean kill, and not a candidate.** The gross point estimate sits below the 0.10R minimum and below the cost hurdle; after real costs every configuration lands between −0.11R and +0.05R. The mechanism-level check is the strongest evidence against it: the effect does not grow with imbalance size, which is the one thing a forced dealer unwind must do. Reaching 80% power at 0.10R needs about 1,500 sessions and the mirror retains 235, so 18 months of this signal cannot settle the edge question — what it settles is the cost question and the mechanism question.

**K disclosed:** 16 configurations + 1 directional test + 1 size-bucket read + 1 halves split = 19 looks on this candidate. Best t anywhere is +0.82 gross. No multiplicity correction changes the reading.

## Corrections (2026-09-02, Codex review of PR #260)

| Finding | Effect on this file |
|---|---|
| **P1** `replay()` defaulted to `explicit_only=False`, so `main()` traded unverified-sign rows; the committed headline CSV held 239 trades of which 96 were `bare-positive`, while the text quoted the clean 143 | Default is now `True`; artifacts regenerated. Headline moved −0.1195R → −0.1137R net |
| **P1** the flatten bucket resolved to the bar at whose *close* `close_all` is submitted, and priced the exit at that bar's *open* — one bar (5 min) early on every time exit, and it dropped that bar from the stop/target window | Corrected to submit-bar + 1. Best-of-16 moved +0.029R → +0.052R |
| **P2** `per_week` was `n / (unique days / 5)`, identically 5.0 since there is one row per traded day | Now measured over the observation span: **1.87/week** filtered, not 5 |
| **P2** the signal path resolved from the caller's cwd, not the documented `inputs/` | Resolved from the script's own directory |

None of the corrections changes the verdict. Two reported numbers did change: cadence (5.0 → 1.87/week) and the MNQ correlation (+0.069 on 133 shared days → +0.087 on 83), the latter because the clean run trades fewer sessions.
