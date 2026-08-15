# Run spec — EOD-OFF counterfactual (measurement, one run)

**Date authored:** 2026-07-05 · **Parent:** `CC-HANDOFF-AEGIS-6J-2026-07-05` §2.4 · **Owner:** Joshua (TV run) → CC (analysis)
**Type:** measurement with a pre-stated read — **no adoption decision attaches to this run.** It quantifies the venue tax on `max_hold=40`; the result feeds the 2.5 trail-MC assumptions and `ops/instruments/6J.md`.

## Configuration (ONE deviation from the panel of record)

- Script: `aegis_jpy_futures_v0_3_prototype.pine` (sha256 `30d35028…`, pinned in `core/strategies/PORT_MANIFEST.sha256`)
- Symbol/TF: CME:6J1! 15m, back-adjusted ("Adjust for contract changes" ON)
- Mode: TV Deep Backtesting, same deep window as the panel of record (start default 2022-01-01; panel prints 2022-01-12 → 2026-07-01 under ON)
- **`EOD Force-Flat` = OFF** ← the only change
- Every other input at v0.3 defaults (the Q-AEGIS-6J-BEPAD-1 §Frozen-config table is the reference list; early-close calendar stays at defaults — it only gates the EOD path, which is off)
- Export: CSV → `Downloads` or directly to `lab/analysis/aegis_6j_transfer_2026-07-05/inputs/`; CC lands + sha256-pins it in `NOTES.md`

## Pre-stated read (written before the run)

Under EOD-ON, 15 exits are `EOD Flat` and banked **+$23,427.80** (60.0% of the $39,056 panel net). The counterfactual is **censored**: we cannot know from the ON panel whether those truncated holds would have gone on to TP (basis reversion target), stop, or 40-bar stale-exit at better/worse prices. **The ON/OFF delta signs the censoring:**

- **OFF > ON** → the force-flat is cutting winners short; `max_hold=40`'s designed hold is worth money the venue confiscates. Expected direction per design intent (a 13:30 ET entry gets ~12 of its 40 designed bars to the 16:30 ET cutoff; the Pine header's "~14 bars" figure is stale v0.1-era text from the retired 16:55 default — see NOTES.md staleness note).
- **OFF < ON** → the force-flat is accidentally protective on 6J (overnight adverse drift/gaps exceed the truncated-winner cost); the "venue tax" is negative.
- Magnitude read: |delta| as % of panel net = the venue tax on max_hold. Also read per-trade: the same 15 trade IDs' exit prices/timing OFF vs ON.

Interpretation guard: the OFF run holds **overnight and across maintenance breaks** — fills on thin 18:00+ bars are less reliable than RTH fills, and Bulenox would never permit these holds. OFF is a *diagnostic bound*, not a tradeable configuration.

## Analysis contract (CC, after export lands)

1. Ingest gate: `reconcile.py --strategy aegis --account 100000 --pointvalue 12500000 --tick 0.0000005 --commission 1.30` — identity must pass; N may legitimately differ from 129 (longer holds absorb later signals via `max 1/day` + position-open gating; report the N delta, don't force it).
2. Delta table: Net / PF / maxDD / expectancy(R=$1,385.74) OFF vs ON; the 15 EOD-Flat trade IDs traced individually.
3. Land the read in `ops/instruments/6J.md` (venue-tax row) and thread the assumption into `RESULTS_trail_mc.md` §caveats (2.5 uses the ON sequence; the OFF delta bounds how conservative that is).

**Gate (binary):** run accepted iff window matches, identity check passes, and `enforce_eod` is the sole non-default input. Otherwise re-export; no partial reads.
