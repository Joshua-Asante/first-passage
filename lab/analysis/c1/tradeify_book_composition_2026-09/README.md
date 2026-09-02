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
- **Third-leg fit rule:** positive net edge is non-negotiable — a zero-edge leg makes the book's
  bust worse at *every* win rate and size tested (+2.4 to +35 pp). Given edge, the leg must clear a
  break-even win rate that falls as edge rises and as the stop shrinks:

  | net edge per trade | break-even WR at a $200 stop | at a $100 stop |
  |---:|---:|---:|
  | 0.05R | above 75% | 62% |
  | 0.10R | 62% | 42% |
  | 0.15R | 52% | ≤ 35% |
  | 0.20R | 46% | ≤ 35% |

  Time saved tracks drift (edge × stop × trades/yr): ~$2.5K/yr ≈ −30 days. Correlation with MNQ at
  or below zero is worth about one win-rate step.
- **The MOC fade is an underpowered non-result that fails the cost-law pre-screen** — gross
  +0.075R (95% CI −0.104R to +0.254R), below the 4× cost hurdle, and it does **not scale with
  imbalance size**, which a forced dealer-unwind must. Not a candidate; not a clean kill either.

## Reproduce

```bash
cd lab/analysis/c1/tradeify_book_composition_2026-09
python book_grid.py --stage smoke                  # 1 cell, ~12 s, plumbing check
python book_grid.py --stage screen --jobs 7        # 88 cells, ~11 min
python book_grid.py --stage final --jobs 3 --finalists '[{"mnq":1,"mym":0,"aegis":2}, ...]'
python controls.py                                 # shuffled-Aegis + excluded-regime + co-movement
python third_leg_shape.py --stage characterize     # what kills/slows the base book
python third_leg_shape.py --stage minimum --jobs 7 # exact-edge minimum-attribute grid
python render_results.py && python render_minimum.py && python render_third_leg.py
python moc_fade_replay.py                          # reads inputs/, needs the Databento cache below
```

⚠ **Keep `--jobs` low on the finals stage.** It runs four bootstraps per cell (intraday, EOD and
both halves) at 10,000 sims × 3 seeds, ~50× the per-cell work of the screen stage, and on a 16 GB
machine it will not survive high parallelism: at `--jobs 4` two of four loky workers died and
joblib blocked on them forever (8/12 cells, no traceback, no output), and at `--jobs 6` the parent
died at ~9 minutes. `--jobs 3` is what the committed figures were produced at. The stage now runs
in chunks and appends each finished cell to `data/grid_final.json.partial.jsonl`, so a crash costs
one chunk and re-running the same command resumes; the sidecar is deleted only once the real
output is on disk. Within one configuration a cell is deterministic — seeded from `SEEDS`,
depending only on its own argument tuple — so a resumed cell is identical to a cold one, and
results are returned in job order regardless of completion order.

**A resume is only honoured when the configuration is unchanged.** The sidecar's first record is a
fingerprint of everything that feeds a cell without appearing in its argument tuple: `SEEDS`,
`HORIZON_CAP`, the eval prices, the micro-equivalent caps, the tier consistency fractions and
`FIRM_RULES` entries in play, and content hashes of the session calendar, each vendor export used,
`book_grid.py` itself and `core/mc/simulation.py` / `core/mc/preflight.py` / `core/firm_rules.py`.
On any mismatch — or if the sidecar predates the fingerprint — it is discarded whole and every cell
recomputed. Being strict is cheap here: a false mismatch costs one re-run, whereas a false match
would splice stale cells into a grid whose header advertises the new configuration, which is the
same "artifacts do not match the code" failure this checkpointing exists to prevent. Guarded by
`tests/lab/test_book_grid_checkpointing.py`.

`data/cme_equity_sessions.json` (1,011 CME equity-index sessions, 13 weekday closures in the
window) is committed so `third_leg_shape.py` never schedules a synthetic trade on a closed market.
It was derived from MES hourly bars: daily bars are **wrong** for this, because `ohlcv-1d` buckets
by UTC day and manufactures phantom weekend bars (`lesson_databento_ohlcv1d_weekend_bars`) — which
showed up immediately as 206 fake Friday "closures".

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
- **Fixed, was a real hole: P&L booked on a non-session date used to be dropped.**
  `daily_per_contract` buckets by the trade's own exit date and `build_cell` reindexes onto
  `pd.bdate_range`, so a position carried through a weekend or a closure booked onto a date the
  path could not hold and vanished — **6 trades, −210.92 per contract of real losses**, which made
  the book look safer than it was. `roll_to_session` now maps every booking (P&L series *and* both
  legs of the intraday floor) onto the next real CME session. Effect, in the honest direction:
  MNQ's in-window P&L falls from +$27,954.7 to +$27,759.2 per contract, MYM's from +$11,399.9 to
  +$11,384.5, Aegis unchanged; zero weekend-dated buckets remain. Found 2026-09-02 while verifying
  the first Codex review and initially only disclosed; fixed after the second review correctly
  pushed back that a committed grid must not omit real losses. Guarded by
  `tests/lab/test_book_grid_session_rolling.py`. The related exit-day carry fix stays inert on this
  data for the same underlying reason: every multi-day trade here exits on a Sunday.
- K disclosed inline in each results file; nothing here consumes a pre-registration.

## Corrections after review

Two rounds of Codex review on [PR #260](https://github.com/Joshua-Asante/first-passage/pull/260),
10 findings total, every one verified against the code and artifacts before being accepted. None
was a false positive. No verdict in this campaign changed in either round.

**Round 1 — 7 findings (2 P1, 5 P2).** Unverified-sign rows no longer reach any replay (they were
reaching the committed artifacts while the report quoted clean numbers — the two had diverged
because the clean run was ad-hoc and never fed back); the flatten bar is the bar *after* the
`close_all` submit bar, not the submit bar itself, so time exits are no longer priced 5 minutes
early; cadence is measured over the observation span rather than over traded days, where it was
identically 5.0/week; multi-day trades stay open on their exit day; synthetic legs trade only real
CME sessions; the shuffled-Aegis control is a true derangement; the signal path resolves from the
script's own directory. `MOC_FADE_REPLAY.md` §Corrections carries the before/after numbers.

**Round 2 — 3 findings (all P2), all on the round-1 work rather than the original.** The verdict
prose hard-coded the control figures while the same function claimed a re-run could not make it
stale — both data sources now feed it. The final-print cutoff compared a fixed UTC time, so every
winter print fell outside the candidate set; now compared in Eastern time. Latent only: verified
across all 72 EST days and the 3 days carrying two non-early posts, **0 selections changed**,
because the empty-candidate fallback happened to rescue the right post. And the non-session P&L
hole above, which round 1 disclosed and this round fixes.
