# aegis_orbmnq_combined_book_2026-08-26

Aegis-6J1 x ORB-MNQ-1 **combined-book** Tradeify_Select_100K passability sweep (2026-08-26),
built from five operator-supplied TradingView "List of Trades" CSV exports. See
[`RESULTS.md`](RESULTS.md) — **read §0 first**: this is evidence that a specific small-weight
*combination* of the two legs clears the eval ceiling in bootstrap, not that either leg is
independently viable (both fail Tradeify solo on this repo's own prior record).

## Status

**EXPLORATORY** — not pre-registered, not a Rule-0 discovery campaign, no Pine-header baseline to
reconcile against. Adversarially spot-checked (independent reimplementation of the drawdown logic
+ correlation arithmetic), not adversarially verified end-to-end. Every bust/pass figure is a
single-path replay or 5-day-block bootstrap over end-of-day equity only — an EOD-clock lower bound
per this repo's own standing posture. Several open hypotheses remain (`RESULTS.md` §8 H2-H4/H7/H8/H10).

## Layout

- [`RESULTS.md`](RESULTS.md) — full write-up: data reconciliation, solo sizing sweeps, combined-book
  naive/cushion sizing, mutual-exclusion timing test, correlation/diversification, regime robustness,
  adversarial verification, third-leg synthetic sensitivity + in-repo instrument survey, ranked
  hypotheses.
- [`combined_sim.py`](combined_sim.py) — reusable simulator module. Reuses
  `core/mc/simulation.py::simulate_path`/`run_seed` and `core/mc/preflight.py::firm_kwargs`/
  `summarize_outcomes` verbatim; ports the cushion-proportional sizing formula from
  `lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/run_evalseq_orb_intraday.py::pol_cushion`
  as a faithful parallel implementation (single-leg -> N-leg). Portable from a fresh clone (path
  fixed on landing here, see file header).
- [`data/`](data/) — derived per-trade tables (`*_trades.csv`) and daily per-contract P&L panels
  (`daily_pnl/*.json`) reduced from the operator's raw TradingView exports, plus raw sweep-result
  JSONs backing every figure in `RESULTS.md`. **Raw CSVs are not committed** (TradingView "List of
  Trades" exports are vendor-sourced, same posture as `core/data/tv_exports/`) — only these derived
  panels, matching the `tradeify_book_composition_2026-07-23/out/daily_panel.csv` precedent.

## Cross-references

- Solo Aegis-6J1 Tradeify precedent: [`lab/analysis/aegis/aegis_6j_trail_tradeify_2026-07-29/`](../../aegis/aegis_6j_trail_tradeify_2026-07-29/)
- ORB-MNQ payability record (fails at every `AUTOMATION_FRIENDLY_PROP_FIRMS` venue tested,
  including Tradeify): [`docs/pursuits/b3-orb-mnq-payability-line.md`](../../../../docs/pursuits/b3-orb-mnq-payability-line.md)
  (addendum filed 2026-08-26 pointing here)
- Third-leg instrument survey cross-references: [`ops/instruments/MGC.md`](../../../../ops/instruments/MGC.md),
  [`ops/instruments/6J.md`](../../../../ops/instruments/6J.md), [`ops/instruments/M6A.md`](../../../../ops/instruments/M6A.md),
  [`ops/instruments/MCL.md`](../../../../ops/instruments/MCL.md)
