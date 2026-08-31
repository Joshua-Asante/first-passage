# orb_mnq_recon_v3 — bust/pass rope walk at Tradeify_Select_100K

**Status:** EXPLORATORY. Not pre-registered, not a Rule-0 discovery campaign. First
account-level bust/pass measurement ever run against `orb_mnq_recon_v3.pine`
(`core/strategies/candidates/orb_mnq_recon_v3.pine`, `MANIFEST.sha256`
`be800cb4…`) — a chart-only DD-reduction research reconstruction that diverges
from the LOCKED `ORB-MNQ-1` construct (see that file's MANIFEST provenance
note). Answers "does this specific config clear the live survivor-scoring
gate" — it does not touch the frozen construct's own `PARKED` disposition
([`2026-08-03-orb-mnq-repark-payability-falsified.md`](../../../docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md)),
and does not by itself authorize anything.

## 0 — Source, panel integrity, reduction

- **Source:** operator-supplied TradingView "List of Trades" export,
  `ORB-MNQ-1_recon_v3_CME_MINI_MNQ1!_2026-08-31_70648.csv` (913 trades,
  664 distinct trade-days, span 2022-01-03→2026-08-28). Not committed
  (vendor-sourced), same posture as `core/data/tv_exports/`.
- **Step-0 battery** (`lab/research_utils/step0_battery.py`): clean pass —
  timeframe (15m, all entry minutes multiples of 15), session window
  (09:15–16:55 ET), day-filter (Wed absent, matches the script's own
  `tradeWed=false` default), n=913, date-span coverage all hold.
  **Tool-usage note:** the script's own comment assumes export timestamps
  are UTC ("TV standard"); Joshua's TradingView chart displays
  `America/New_York` (DST-aware), not UTC — confirmed by prior measurement
  (`reference_platform_display_tz_edt.md`, 96–97% bar-containment match at
  `America/New_York` vs 0.8–1.1% at naive UTC on a comparable panel). Ran
  with `--tz UTC` so the script's `tz_localize('UTC').tz_convert(tz)` step
  becomes a no-op and the already-ET timestamps are compared directly
  against the ET session bounds. Without this, 865/913 entries spuriously
  fail the session check.
- **Reduction** (`reduce_trades.py`): qty constant at 2 throughout (verified,
  hard-fails otherwise). Daily net PnL summed across all exit rows sharing
  a calendar day (scale-in adds get their own trade-number row sharing the
  day's exit — confirmed both by the 2026-08-25 session's own finding and
  by this reduction's own re-derived total: qty-normalized sum = **$65,704.68**,
  exact match to the TradingView panel's own "Total PnL" figure. 664 unique
  trade-days out of 913 exit rows ⇒ 249 scale-in days, 37.5% — consistent
  with the 2026-08-25 session's independently-measured ~38%.
  `data/daily_pnl.json` (664 days) / `data/daily_mae.json` (664 days,
  worst per-contract Adverse Excursion USD that day) — a disclosed
  trade-level MAE proxy, not a true bar-level intraday reconstruction (same
  caveat as `aegis_orbmnq_combined_book_2026-08-26/followup_intraday_mae_proxy.py`,
  whose own proxy reading was later reversed by a more careful
  timestamp-sequenced remeasure — read the numbers below with that in mind).

## 1 — Method

`bust_pass_sim.py` reuses `core/mc/simulation.py::simulate_path`/`run_seed`
and `core/mc/preflight.py::firm_kwargs`/`summarize_outcomes` verbatim — same
engine as the 2026-08-03 T2 measurement and the 2026-08-26 combined-book
study. `k ∈ {1,2,3}` (T2 ADR's own admissible-contract grid). Bootstrap:
5-day block resample, 10,000 sims/seed × 3 seeds (matches the T2 ADR's own
stated methodology). Two clock readings per cell: **EOD-clock** (closed-trade
daily PnL only — a lower bound, cannot see an intraday breach that recovers
by the close) and **intraday-honest** (adds the MAE-proxy `intraday_low`).
Two consistency readings: **Run-2** (`consistency=0.40`, Tradeify's actual
rule — the deployable expression the live pre-registration scores) and
**Run-1** (consistency off, for continuity — byte-identical to Run-2 here
since bust is decided before the consistency check ever matters).

**Ceiling:** live gate is bust ≤ **5.0%** ∧ P(pass) ≥ **50%**
([prereg v2](../../../docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md)
§3, raised from 3.0% on 2026-08-26 — both quoted below).

## 2 — Results (Run-2, the deployable-expression reading)

| k | realized-panel outcome (EOD / intraday) | bootstrap bust% EOD-clock | bootstrap bust% intraday-honest | bootstrap pass% intraday-honest | vs 5.0% ceiling | vs 3.0% (original) |
|---|---|---:|---:|---:|---|---|
| 1 | pass / pass (max DD 1.72%) | 17.69% | **20.78%** | 79.22% | **FAIL, 4.2×** | FAIL, 6.9× |
| 2 | pass / bust_trailing day 77 (max DD 2.79%) | 44.21% | **53.70%** | 46.30% | **FAIL, 10.7×** | FAIL, 17.9× |
| 3 | bust_trailing day 15 (both clocks) | 56.54% | **64.11%** | 35.89% | **FAIL, 12.8×** | FAIL, 21.4× |

Run-1 (consistency off) is numerically identical at k=1 and differs only in
the third decimal at k=2/k=3 (bust is decided on the barrier alone; the
consistency check only ever matters for trades that already pass) — see
`data/bust_pass_sim_results.json` for both readings in full.

**Verdict: FAILS at every tested k, both clock readings, both consistency
readings.** k=1 does not bust on the single realized historical path at
either clock (max DD 1.72%, well inside the $3,000/3.0% trail) — but the
bootstrap, which resamples the same trade-blocks in different 5-day-block
orders, busts 1 path in 5 (intraday-honest). The realized ordering was not
representative of the construct's own risk.

## 3 — Comparison to the frozen construct

| | k=1 bust (intraday-honest) | vs 5.0% ceiling |
|---|---:|---|
| Frozen `ORB-MNQ-1` (2026-08-03 ADR) | 67.67% | FAIL, 13.5× |
| `orb_mnq_recon_v3` (this measurement) | 20.78% | FAIL, 4.2× |

The DD-reduction tuning lineage (v1→v7, see `MANIFEST.sha256` provenance)
measurably worked — k=1 bust dropped from 67.67% to 20.78%, a real ~3.25×
improvement, not noise. It is not close to enough: even the best cell here
is more than 4× over the current (already-raised) ceiling. This is a single
data point on a single construct, not a re-run of the frozen ADR's own
falsifier (R1) — see that ADR's 2026-08-30 dormancy addendum for why R1
itself is currently unexercised.

## 4 — What this does and doesn't establish

- **Does not clear the gate.** No re-entry, no ADR, no lifecycle change is
  warranted by this measurement alone.
- **Does not touch `ORB-MNQ-1`'s own `PARKED` disposition** — `orb_mnq_recon_v3`
  is a distinct, divergent-parameter candidate (see its `MANIFEST.sha256`
  provenance note); this is evidence about that candidate, not a re-run of
  the frozen construct's falsifier.
- **Selection/overfitting risk is still uncorrected.** This config is the
  product of an iterative single-lineage tuning session (v1→v7) with no
  pre-registration, no held-out data, no K accounting, no DSR/permutation/PBO
  pass. The true out-of-sample bust rate could be worse than 20.78% even
  before considering the intraday-honest/MAE-proxy caveat below.
- **Intraday-honest reading is a disclosed proxy, not a bar-level
  reconstruction** (§0). The EOD-clock-only bust (17.69% at k=1) is the more
  defensible lower bound; either way the gap to the 5.0% ceiling is wide
  enough that this specific caveat does not change the verdict.

## 5 — Reproduce

```bash
cd lab/analysis/orb/orb_mnq_recon_v3_2026-08-31
python reduce_trades.py "<path to the TV export>"
python bust_pass_sim.py
```
