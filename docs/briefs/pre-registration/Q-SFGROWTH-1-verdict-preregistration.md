# Q-SFGROWTH-1 — Verdict pre-registration

**Status:** FROZEN 2026-10-09 (operator: "freeze the plan"), before any export is read or any scorer exists. The freeze commit is recorded in the [parent brief §8](../Q-SFGROWTH-1-self-funded-growth-portfolio-selection.md#8--verdict-pre-registration). A verdict computed after any constant below moves is void; a changed constant is a new pre-registration. Corrections from the freeze review land before Phase 0 reads data, as a dated amendment and re-freeze (see §E). The original freeze text is immutable at `121e2acf`.

## A — Pool

Legs with an accepted CME trade list, at their locked parameters, **normal mode** (no Tradeify protection; the only protection modeled is the 15% halt in §C):

| # | Leg | Instrument | Accepted size baseline `Q_i` |
|---|---|---|---|
| 1 | Aegis 6J | 6J (full size) | 8 contracts (`remc_series_builder.DEFAULT_QUANTITY_SPEC["aegis_6j"]["normal"]`) |
| 2 | Striker DJ30 MYM p250 | MYM | as exported |
| 3 | Vanguard Gold MGC v0.4 | MGC | as exported |
| 4 | ORB MNQ v7 reconstruction | MNQ | as exported |
| 5 | Striker NAS100 MNQ, DOW-excluded | MNQ | as exported — included by operator ruling 2026-10-09 ("include it"), scoped to this selection; the Tradeify withdrawal stands |

The pinned Tradeify exports are the reference for each leg's locked inputs, not scoring inputs: legs 1–4 in `lab/analysis/c1/four_firm_remc_2026-10/run_four_firm_remc.py` (normal-mode pins only), leg 5 at `strategies[3].export_sha256` in `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/phase1_config.json`. Leg 1 trades full-size 6J because no micro-yen edition has an accepted trade list; this is a pool limit, not a claim that Tradovate lists no micro yen.

## B — Grid, exports and K

- Each leg gets a multiplier `k_i ∈ {0, 1/8, 1/4, 1/2, 1, 2}`.
- **Size-specific exports, no linear rescaling.** For each leg and each non-zero `k` (k = 1 included), the leg's series comes from its own TradingView export of the locked Pine with every sizing input multiplied by `k` and all other inputs equal to the reference export's:
  - a **contract-count** input is set to `floor(k × its reference value)` (leg 1: `floor(k × 8)`);
  - an **account-size** input used only to compute position size (the Striker legs' static `accountSize` read by `calcSize`, [campaign §D15](../programs/2026-09-03-seven-strategy-select-campaign-state.md)) is set to `k × its reference value`, unrounded; the Pine rounds the resulting quantity itself;
  - the Properties-panel **initial capital** is set to `k × the reference export's initial capital`, so capital-anchored controls (the Striker day soft-stop) keep their locked ratio to position size.

  If a leg ends up with no trades at some `k`, it contributes none at that `k`. Each export's per-trade `Size (qty)` is used as exported. The $10,000 account exists only in the simulator (`E_0`, §C), not in TradingView. Reason: the Striker legs carry size- and capital-dependent state, so a rescaled list from another size can contain trades the smaller strategy would never take.
- Before any export is produced, Phase 0 reads each leg's Pine in the operator checkout (not quoted, not copied) and records in the manifest which inputs are contract-count, account-size and neither. That classification is reviewed before exports are made.
- Before any export is read for scoring, Phase 0 commits a manifest listing every (leg, k) export with its SHA-256, the inputs changed and their values. A missing or hash-mismatched export ⇒ VOID.
- **Excluded combinations:** legs 4 and 5 both non-zero (the rail flattens by account and instrument, so two MNQ legs cannot hold independent positions).
- **Margin exclusion:** a configuration is excluded if `Σ_i max_n_i × IM_i > $10,000`, where `max_n_i` is the largest per-trade quantity in leg i's size-k export over the full calendar and `IM_i` is Tradovate's published initial margin per contract for that instrument in a dated snapshot recorded in the Phase-0 manifest. This assumes every leg's largest position is open at once, which is conservative.
- Multiplier vectors are not deduplicated: each is a distinct prospective sizing rule.
- **K = 2,375** = 6^5 − 1 vectors minus the 5,400 with legs 4 and 5 both non-zero, written to the `register_search` manifest before any Explore read. K does not depend on data; margin-excluded vectors count in K.

## C — Statistic

**Costs.** One all-in rate per side per instrument = commission (the account's Tradovate plan at Phase 0) + exchange + clearing + NFA, from a dated Tradovate rate snapshot recorded in the Phase-0 manifest before any export is read. Cost multiple `c ∈ {1, 1.5}` multiplies the whole all-in rate. A missing component ⇒ VOID.

**Series.** Per configuration and `c`, trades parsed by `remc_series_builder.parse_trade_list_csv` (session-contained, flat each session) and assigned to their session date:
- `d_t` = Σ gross P&L − c · cost_t, where cost_t = Σ sides × all-in rate
- `l_t` = 0 − Σ |adverse excursion| − c · cost_t (coincident-sum low, ≤ 0)
- `h_t` = Σ |favorable excursion| (coincident-sum high, ≥ 0, no cost deduction; overstating the peak is conservative). An export without a favorable-excursion column ⇒ VOID.

**Calendar and windows.** One calendar for every configuration: every Monday–Friday (no-trade days zero) from the latest first session date to the earliest last session date across the **k = 1 size-specific exports of all five legs** (a k = 1 export with no trades ⇒ VOID). With W its length, Explore = weekdays 1 … ⌊2W/3⌋, Confirm = weekdays ⌊2W/3⌋ + 1 … W. Trades outside the calendar are ignored.

**Paths.** For each seed `s ∈ {42, 123, 2026}` and each window of length `W_w` (VOID if `W_w < 20`):
- `rng = numpy.random.default_rng(s)` (PCG64)
- `starts = rng.integers(0, W_w − 20 + 1, size=(10_000, 13))` in one call; rows are paths 0 … 9,999 in order; non-circular blocks, starts may overlap
- path p's days = concatenate `range(starts[p, j], starts[p, j] + 20)` for j = 0 … 12, truncated to the first H = 252
- the same `starts` array serves every configuration and both cost multiples

**Per path, E_0 = P_0 = $10,000; for t = 1 … 252 (i = the path's t-th day):**
- intraday peak `P*_t = max(P_{t-1}, E_{t-1} + h_i)` (the high is assumed to come before the low, which is conservative)
- intraday trough `T_t = E_{t-1} + l_i`
- **hit** if `(P*_t − T_t) / P*_t ≥ 0.15`; the path stops with terminal equity `T_t`
- otherwise `E_t = E_{t-1} + d_i` and `P_t = max(P*_t, E_t)`
- terminal equity = `E_252` if never hit

**Clears** (per configuration, window, `c`): hits ≤ 100 of 10,000 on **every** seed.
**Growth** = `numpy.median` of the 30,000 pooled terminal equities (the average of the two middle values).
**Rank** (Explore, c = 1, non-excluded configurations only): among those that clear with growth > $10,000, highest growth first; ties go to (i) fewer pooled hits, (ii) the smaller sum of per-trade quantities over Explore-window trades, (iii) the lexicographically smallest multiplier vector in §A leg order.

**Roll-seam limitation and sensitivity.** Every export is from a continuous `1!` chart. Trades are session-contained, so a back-adjustment seam cannot enter a trade's own P&L, but signals computed across sessions can still differ near a seam. Phase 0 records, per instrument and before any export is read, the session dates on which the continuous series changed contract. The sensitivity re-scores the top configuration on Confirm at c = 1 with every trade whose session date lies within 10 weekdays (either side, inclusive) of such a date removed.

### Worked example (synthetic, two days, one path)

E_0 = P_0 = 10,000. Day 1: d = +200, l = −300, h = +400. Day 2: d = −1,400, l = −1,600, h = 0.

- Day 1: P*_1 = max(10,000, 10,000 + 400) = 10,400; T_1 = 9,700; drawdown 700 / 10,400 = 6.73% → no hit; E_1 = 10,200; P_1 = max(10,400, 10,200) = 10,400.
- Day 2: P*_2 = max(10,400, 10,200 + 0) = 10,400; T_2 = 10,200 − 1,600 = 8,600; drawdown 1,800 / 10,400 = 17.31% ≥ 15% → **hit**; terminal equity 8,600.

## D — Verdict table

Evaluate VOID first; the other rows apply only when no VOID condition holds.

| Verdict | Trigger | Disposition |
|---|---|---|
| VOID | an export is missing or mismatches its manifest hash; run K ≠ manifest K (2,375); the cost snapshot, margin snapshot or roll-date list is missing a component; an export lacks a favorable-excursion column or a k = 1 export has no trades; or a window is shorter than 20 weekdays | ITERATE (fix input, rerun unchanged) |
| RESOLVED | (1) ≥ 1 non-excluded configuration clears on Explore at c = 1 with growth > $10,000; (2) the top-ranked one clears on Confirm at c = 1; (3) it clears on Confirm at c = 1.5; (4) its Confirm growth > $10,000 at c = 1 and at c = 1.5; (5) it clears the roll-seam sensitivity | INTEGRATE |
| FALSIFIED | condition (1) fails | STOP |
| AMBIGUOUS-HOLD | (1) holds and any of (2)–(5) fails | ITERATE (operator; no second pick) |

Only the top-ranked Explore configuration is scored on Confirm.

## E — Amendment log

- **2026-10-09, Codex freeze review (PR #743, review on `d90eae8`), before any export was read or any scorer existed.** Changes from `121e2acf`:
  1. One calendar for all configurations, from the full five-leg pool; the builder's weekday calendar; the Explore/Confirm cut stated as a function of W.
  2. The 1.5× cost limb also requires Confirm growth > $10,000, matching H-SFGROWTH-1.
  3. An intraday-high channel `h_t` feeds the running peak, so the statistic is genuinely intraday peak-to-trough; missing favorable-excursion data ⇒ VOID.
  4. Multiplier vectors are not deduplicated (final K in item 8); a final lexicographic tie-break makes the selected vector unique.
  5. The bootstrap is pinned: generator, start-index range, array shape and order, concatenation and truncation, window boundaries, and shared draws across configurations.
  6. Normal mode only; leg 1's baseline is the accepted 8 contracts; "no micro on Tradovate" removed (pool limit, not broker fact).
  7. Size-specific exports per (leg, k) replace linear rescaling (the Striker day soft-stop depends on size and capital); the quantity baseline is the export itself.
  8. Legs 4 and 5 may not both be non-zero (one MNQ position per account on the rail); K = 2,375, data-independent, so the K manifest no longer requires reading exports.
  9. Conservative initial-margin exclusion against $10,000 from a dated Tradovate snapshot.
  10. Cost = commission + exchange + clearing + NFA from a dated snapshot of the account's plan; 1.5× multiplies the whole rate.
  11. `numpy.median` fixed; VOID evaluated before every payoff row.
  12. Roll-seam limitation carried, with a frozen ±10-weekday sensitivity as RESOLVED condition (5).
- **2026-10-09, independent re-review on `fec6ad2` (PR #743), before any export was read or produced.** Change from `c208bde9`:
  13. The k-mapping now covers risk-sized legs: account-size inputs scale by `k` (unrounded), initial capital scales by `k` (replacing the fixed $10,000 of item 7, which would have tightened the Striker soft-stop tenfold against unchanged positions), contract-count inputs stay `floor(k × reference)`; Phase 0 classifies every sizing input from the Pine before producing exports.

