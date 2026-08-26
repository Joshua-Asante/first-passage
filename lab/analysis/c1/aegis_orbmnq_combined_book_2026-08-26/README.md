# aegis_orbmnq_combined_book_2026-08-26

Aegis-6J1 x ORB-MNQ-1 **combined-book** Tradeify_Select_100K passability sweep (2026-08-26),
built from five operator-supplied TradingView "List of Trades" CSV exports. See
[`RESULTS.md`](RESULTS.md) — **read §0 and §9 first**: §0 is why this is evidence that a specific
small-weight *combination* of the two legs clears the eval ceiling in bootstrap, not that either
leg is independently viable (both fail Tradeify solo on this repo's own prior record); §9 is a
same-day follow-up pass that **materially revises the headline** — the 1yr flagship fails a proper
both-halves regime bootstrap, and the 3yr flagship's margin shrinks or fails outright once
tail-risk-consistent sizing and a trade-level intraday-honest proxy are applied together.

## Status

**EXPLORATORY** — not pre-registered, not a Rule-0 discovery campaign, no Pine-header baseline to
reconcile against. Adversarially spot-checked (independent reimplementation of the drawdown logic
+ correlation arithmetic), not adversarially verified end-to-end. Every bust/pass figure through
`RESULTS.md` §8 is a single-path replay or 5-day-block bootstrap over end-of-day equity only — an
EOD-clock lower bound per this repo's own standing posture; §9's intraday figures are a disclosed
trade-level MAE proxy, not a bar-level remeasure. H1/H5/H6/H7/H8/H9 are resolved; H2/H3/H10 are
partially resolved (real direction/magnitude, proxy not ground truth); H4 needs a native
TradingView re-export and is handed off (`RESULTS.md` §9.4) — not computable in this container.

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
- [`followup_h7_h8_regime.py`](followup_h7_h8_regime.py) — H7 (bootstrap-95th-percentile sizing
  ratio), H8 (correlation-null at the real flagship sizing), and a proper both-halves
  regime-robustness bootstrap. Builds on `combined_sim.py`.
- [`followup_intraday_mae_proxy.py`](followup_intraday_mae_proxy.py) — H2/H3/H10 trade-level
  MAE-proxy intraday-honest remeasure, using `simulate_path`'s `intraday_low` /
  `run_seed`'s `intraday_blocks` (the same mechanism ORB-MNQ-1's own W1/T2 studies used). See the
  file's own docstring for the disclosed approximation and why it is not a bar-level reconstruction.
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
