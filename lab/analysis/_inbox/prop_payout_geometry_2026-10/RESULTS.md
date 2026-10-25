# Prop payout geometry: path-to-first-payout simulator (2026-10-21)

**Verdict:** ACTIVE — research input only. 50K tiers (target/drawdown 1.5) beat 100K (2.0) on fees per first payout at every Sharpe tested; no capital or deployment decision is made here.

Write-ups (owners of the findings):
- [Q-PROP-TRADER-METRICS-1 memo](../../../../docs/notes/research/2026-10-21-q-prop-trader-metrics-1-memo.md): published pass/payout statistics and the single-attempt objective.
- [Q-PATH-TO-PAYOUT-1 memo](../../../../docs/notes/research/2026-10-21-q-path-to-payout-1-memo.md): program ranking and the strategy/deployment shape.

## Model

i.i.d. Gaussian daily edge at annualised Sharpe `S` and daily σ `sd`, with intraday Brownian paths (13–26 sub-steps), so drawdowns are breached intraday. Program rules (target, drawdown type and lock, DLL, consistency, minimum days, payout gate, cap, split, price, reset, monthly billing) are set in `programs.py` from firm help-centre pages read on 2026-10-21; each entry's comment labels its source. Payouts and fees are simulated, not observed.

## Files

| File | Purpose |
|---|---|
| `payout_sim.py` | General simulator: eval → funded → first payout, with resets and re-buys |
| `programs.py` | Tradeify (50/100/150K) and other firms' 50K rule sets |
| `eval_barrier_sim.py`, `run_funded_sweep.py`, `run_resets.py` | Tradeify Select 100K single-attempt, funded and resets runs (metrics memo §3) |
| `run_tradeify.py` → `tradeify_output.txt` | Tradeify program grid (payout memo, early pass) |
| `run_ranking.py` → `ranking_output.txt`, `ranking_results.json` | Cross-firm 50K ranking, first payout ≥ $1,000 net within 120 trading days (payout memo §2) |
| `run_zero_edge.py` | Zero/low-edge calibration (payout memo §2) |
| `pass63_check.py` → [`PASS63_CHECK.md`](PASS63_CHECK.md) | Independent check of the Select 100K pass-within-63-days curve, plus 126 days |

Reproduce: `python -I lab/analysis/_inbox/prop_payout_geometry_2026-10/run_ranking.py` (about 5 minutes; fixed seeds).

## Known limits

- The i.i.d. Gaussian assumption favours high variance more than fat tails would.
- FundedNext Flex's funded rules were corrected on 2026-10-21 against its help centre (payout memo §5); zero-edge expected net is now negative, as for every other program.
- The Tradeify Select eval has no drawdown lock (verified 2026-10-21, payout memo §5), as modelled.
- Subscription programs (Topstep, TradeDay Fast Pass, Alpha Standard) are charged a reset fee per failed attempt *and* the monthly fee for every 21 eval days beyond the first (`payout_sim.py` cost line; `programs.py` `monthly=`). Where a reset also renews or replaces the subscription, this double-counts, so their fee and $/payout figures may be overstated.
