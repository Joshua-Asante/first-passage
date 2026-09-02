# tradeify_book_composition_2026-09

Three questions asked in sequence, one campaign, 2026-09-01/02, operator-directed:

1. **Does any integer-size combination of the three live candidate constructs pass a Tradeify
   eval?** — ORB-MNQ recon × ORB-MYM v0.4 × Aegis-6J1, 88 screen cells + 6 finalists at 30,000
   bootstrap paths, `Tradeify_Select_100K` and `Tradeify_Growth_100K`. → [`RESULTS.md`](RESULTS.md)
2. **What shape would a third leg need to fit beside the best pair?** — a synthetic leg with
   controlled edge / win rate / stop size / cadence / correlation, added to the *real* base book on
   the real date index. → [`THIRD_LEG_MINIMUM.md`](THIRD_LEG_MINIMUM.md) (reference) and
   [`THIRD_LEG.md`](THIRD_LEG.md) (first pass, **superseded**, see its banner)
3. **Does the one real candidate matching that shape have an edge?** — the closing-auction
   (MOC) imbalance fade on MES, replayed on real MES bars over 235 verified-sign sessions.
   → [`MOC_FADE_REPLAY.md`](MOC_FADE_REPLAY.md)

## Status

**EXPLORATORY.** Not pre-registered, no K ledger entry, no candidate contract opened, nothing
admitted, nothing armed. No `core/`, Pine, allocation, `dd_protection`, lifecycle or rail change.
$0 spend (the Databento pull metered at $0.0000).

Every barrier/bust figure comes from `core/mc/simulation.py::simulate_path`/`run_seed` and
`core/mc/preflight.py::firm_kwargs`/`summarize_outcomes` reused verbatim — no barrier logic is
reimplemented anywhere in this directory.

## Headline findings

- **No configuration is a clear winner.** There is a real bust-versus-speed frontier; the Pareto
  set has four members on each tier. `RESULTS.md` §Verdict has the ranked picks.
- **Any leg at 2 contracts is out** (40–66% bust everywhere). Sizing dominates composition, and
  tier dominates both: the same books read ~40% relative lower bust on Growth's $3,500 rope.
- **ORB-MYM v0.4 hurts every book it joins** (+9–11 pp bust for 40–50 days saved); its losses
  coincide with MNQ's 25% more often than independence.
- **Aegis×2 beside MNQ×1 improves all three axes, but the gain is drift, not diversification** —
  a shuffled-Aegis control (dates permuted within year) matches or beats the real book. On the
  2020-02→2022-07 window the grid cannot see, Aegis×2 passes 0.03% of paths.
- **Third-leg fit rule:** positive net edge is non-negotiable (a zero-edge leg adds +2 to +37 pp of
  bust), and the win rate must clear roughly `85% − 2pp per 0.01R of edge` at a $200 stop
  (`−4pp` at $100). Time saved tracks drift: ~$2.5K/yr ≈ −30 days.
- **The MOC fade is an underpowered non-result that fails the cost-law pre-screen** — gross
  +0.075R (95% CI −0.104R to +0.254R), below the 4× cost hurdle, and it does **not scale with
  imbalance size**, which a forced dealer-unwind must. Not a candidate; not a clean kill either.

## Reproduce

```bash
cd lab/analysis/c1/tradeify_book_composition_2026-09
python book_grid.py --stage smoke                  # 1 cell, ~12 s, plumbing check
python book_grid.py --stage screen --jobs 7        # 88 cells, ~11 min
python book_grid.py --stage final --jobs 4 --finalists '[{"mnq":1,"mym":0,"aegis":2}, ...]'
python controls.py                                 # shuffled-Aegis + excluded-regime + co-movement
python third_leg_shape.py --stage characterize     # what kills/slows the base book
python third_leg_shape.py --stage minimum --jobs 7 # exact-edge minimum-attribute grid
python render_results.py && python render_minimum.py && python render_third_leg.py
python moc_fade_replay.py                          # needs the Databento cache below
```

**Inputs are local and deliberately not committed** (vendor TradingView exports, same posture as
`core/data/tv_exports/`). `book_grid.py`'s docstring names each file; they live in `~/Downloads`:

| Leg | File | Basis |
|---|---|---|
| MNQ | `ORB-MNQ-1_recon_v7_..._70648.csv` | qty 2 constant; v8 byte-identical, v8.1 differs only in Signal labels |
| MYM | `ORB-MYM-1_v0.4_..._74611.csv` | both directions, base 3 + add 3, from 2022-08-01 |
| MYM (reference) | `ORB-MYM-1_v0.3_..._f7482.csv` | long-only qty 2 — the export `ops/instruments/MYM.md` M9 measured |
| Aegis | `Aegis_6J1_..._2026-08-02_76620.csv` | the **sanctioned 1-tick/side** panel (`ops/instruments/6J.md` J12) |

⚠ `Aegis_6J1_..._2026-08-28_cbcc9.csv` and `..._2026-08-26_c59e9.csv` fill **one tick better than
`76620` on every shared trade** — re-verified this campaign — so they are on the barred
zero-slippage basis and are not used.

MES bars for the replay: Databento `GLBX.MDP3` `MES.v.0` `ohlcv-1m`, 2025-03-01→2026-09-02,
estimated and pulled at **$0.0000** (532,738 records). `.v.0` not `.c.0`, per
`lesson_roll_rule_changes_bar_existence`. Cache key
`ohlcv-1m_continuous_4421daf2a29d7cd8.dbn`; re-pull with
`PYTHONPATH=lab python -m databento_fetch.db_fetch pull --symbols MES.v.0 --stype continuous
--schema ohlcv-1m --start 2025-03-01 --end 2026-09-02 --max-cost 1.00`.

The MOC signal table is in [`inputs/`](inputs/) (gitignored) — see [`scrape/README.md`](scrape/README.md)
for how it was collected and, more importantly, **why 107 of its 342 rows carry an unusable sign**.

## Disclosed limits

- **Bootstrap breaks the realized sequence and is the pessimistic read**: every finalist's realized
  path passes (day 79–156, max drawdown 1.9–2.2%) and rolling starts never bust.
- **The intraday channel is a trade-level sweep-line** from each leg's own TradingView
  adverse-excursion figures (ported from `aegis_orbmnq_combined_book_2026-08-26/followup_s10`,
  generalised to N legs), **not** a bar-level replay. The MOC replay is the one exception — it is
  bar-level, on real 1m MES data.
- **Window starts 2022-08-01** because MYM v0.4 does. MNQ's 2020–2021 and Aegis's 2020–2022 sit
  outside it; both are known-adverse (`controls.py` measures the Aegis half directly).
- **The ORB lineages are tuned charts with no untouched holdout** (~85 informal cells on MNQ, ~40+
  on MYM per the operator's own session records). Treat every ORB figure as in-sample.
- **Growth's soft $2,500 daily lockout is not modelled** (`core/firm_rules.py` says so explicitly):
  pessimistic on the rope, so Growth figures are two-sided bounds, not point estimates.
- **Synthetic third-leg outcomes are independent draws** — no regime clustering — so a real leg
  with the same summary statistics will do worse than the grid says.
- K disclosed inline in each results file; nothing here consumes a pre-registration.
