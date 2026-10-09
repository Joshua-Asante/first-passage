# Q-SFGROWTH-1 — Verdict pre-registration

**Status:** FROZEN 2026-10-09 (operator: "freeze the plan"), before any export is read or any scorer exists. The freeze commit is recorded in the [parent brief §8](../Q-SFGROWTH-1-self-funded-growth-portfolio-selection.md#8--verdict-pre-registration). A verdict computed after any constant below moves is void; a changed constant is a new pre-registration. Corrections from the freeze review land before Phase 0 reads data, as a dated amendment and re-freeze (see §E). The original freeze text is immutable at `121e2acf`.

## A — Pool

Legs with an accepted CME trade list, at their locked parameters. Export pins: the four book legs in `lab/analysis/c1/four_firm_remc_2026-10/run_four_firm_remc.py`; the NAS100 MNQ edition at `strategies[3].export_sha256` (`striker_nas100_mnq_dow_wed_excluded`) in `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/phase1_config.json`:

| Leg | Instrument | Minimum lot |
|---|---|---|
| Aegis 6J | 6J (full size; no micro on Tradovate) | 1 contract |
| Striker DJ30 MYM p250 | MYM | 1 micro |
| Vanguard Gold MGC v0.4 | MGC | 1 micro |
| ORB MNQ v7 reconstruction | MNQ | 1 micro |
| Striker NAS100 MNQ, DOW-excluded | MNQ | 1 micro — included by operator ruling 2026-10-09 ("include it"); scoped to this personal-account selection, the Tradeify withdrawal stands |

## B — Grid and K

- Each leg gets a multiplier `k_i ∈ {0, 1/8, 1/4, 1/2, 1, 2}` applied to its accepted per-trade quantity `q` (the export's `Size (qty)`).
- Scaled quantity: `n = floor(k_i · q)`. Per-trade gross P&L, adverse excursion and favorable excursion scale by `n / q`; sides scale to the scaled quantity. A trade with `n = 0` is dropped with its costs.
- A configuration is one multiplier vector `(k_1 … k_5)`, legs in §A table order, with at least one non-zero entry. Vectors are **not** deduplicated, even when two produce identical historical trade lists: each is a distinct prospective sizing rule, and the selected vector becomes the live binding.
- **K = 6^5 − 1 = 7,775**, written to the `register_search` manifest before any Explore read.

## C — Statistic

**Series.** Per configuration and cost multiple `c ∈ {1, 1.5}`, on the calendar below, three daily channels from `remc_series_builder`'s per-trade rows, with trades assigned to their session date:
- `d_t` = Σ scaled gross P&L − c · cost_t, where cost_t = Σ scaled sides × the verified personal-Tradovate all-in rate per side for that instrument (commission + exchange + NFA); an unverified rate ⇒ VOID
- `l_t` = 0 − Σ |scaled adverse excursion| − c · cost_t (coincident-sum low, ≤ 0)
- `h_t` = Σ |scaled favorable excursion| (coincident-sum high, ≥ 0; no cost deduction, so the peak is overstated, which is conservative). An export without a favorable-excursion column ⇒ VOID.

**Calendar and windows.** One calendar for every configuration: the builder's weekday calendar (every Monday–Friday, no-trade days zero) from the latest first session date to the earliest last session date across the **full trade lists of all five §A legs**, independent of which legs a configuration uses. With W = its length in weekdays, Explore = weekdays 1 … ⌊2W/3⌋ and Confirm = weekdays ⌊2W/3⌋ + 1 … W.

**Paths.** For each seed `s ∈ {42, 123, 2026}` and each window of length `W_w` (VOID if `W_w < 20`):
- `rng = numpy.random.default_rng(s)` (PCG64)
- `starts = rng.integers(0, W_w − 20 + 1, size=(10_000, 13))` — one call, rows are paths 0 … 9,999 in order; blocks are non-circular, starts may overlap
- path p's day sequence = concatenate `range(starts[p, j], starts[p, j] + 20)` for j = 0 … 12, truncated to its first H = 252 days
- the same `starts` array is used for every configuration and both cost multiples (common random numbers)

**Per path, start equity E_0 = $10,000, P_0 = E_0; for t = 1 … 252 (day index i = the path's t-th day):**
- intraday peak `P*_t = max(P_{t-1}, E_{t-1} + h_i)` (the high is assumed to come before the low, which is conservative)
- intraday trough `T_t = E_{t-1} + l_i`
- **hit** if `(P*_t − T_t) / P*_t ≥ 0.15`; the path stops and its terminal equity is `T_t`
- otherwise `E_t = E_{t-1} + d_i` and `P_t = max(P*_t, E_t)`
- terminal equity = `E_252` if never hit

**Clears** (per configuration, window and cost multiple): hits ≤ 100 of 10,000 on **every** seed.
**Growth** = median terminal equity over the 30,000 pooled paths (`numpy.median`, the average of the two middle values).
**Rank** (Explore, c = 1 only): among configurations that clear with growth > $10,000, highest growth first; ties go to (i) fewer pooled hits, (ii) the smaller sum of scaled quantities `n` over Explore-window trades, (iii) the lexicographically smallest multiplier vector in §A leg order.

### Worked example (synthetic, two days, one path)

E_0 = P_0 = 10,000. Day 1: d = +200, l = −300, h = +400. Day 2: d = −1,400, l = −1,600, h = 0.

- Day 1: P*_1 = max(10,000, 10,000 + 400) = 10,400; T_1 = 9,700; drawdown 700 / 10,400 = 6.73% → no hit; E_1 = 10,200; P_1 = max(10,400, 10,200) = 10,400.
- Day 2: P*_2 = max(10,400, 10,200 + 0) = 10,400; T_2 = 10,200 − 1,600 = 8,600; drawdown 1,800 / 10,400 = 17.31% ≥ 15% → **hit**; terminal equity 8,600.

## D — Verdict table

| Verdict | Trigger | Disposition |
|---|---|---|
| RESOLVED | (1) ≥ 1 configuration clears on Explore at c = 1 with growth > $10,000; (2) the top-ranked one clears on Confirm at c = 1; (3) it clears on Confirm at c = 1.5; (4) its Confirm growth > $10,000 at c = 1 **and** at c = 1.5 | INTEGRATE |
| FALSIFIED | condition (1) fails | STOP |
| AMBIGUOUS-HOLD | (1) holds and any of (2)–(4) fails | ITERATE (operator; no second pick) |
| VOID | an export hash mismatches its pin, run K ≠ manifest K (7,775), a cost input is unverified, an export lacks a favorable-excursion column, or a window is shorter than 20 weekdays | ITERATE (fix input, rerun unchanged) |

Only the top-ranked Explore configuration is scored on Confirm.

## E — Amendment log

- **2026-10-09, Codex freeze review (PR #743, review on `d90eae8`), before any export was read or any scorer existed.** Changes from `121e2acf`:
  1. One calendar for all configurations, from the full five-leg pool; the builder's weekday calendar; the Explore/Confirm cut stated as a function of W.
  2. The 1.5× cost limb also requires Confirm growth > $10,000, matching H-SFGROWTH-1.
  3. An intraday-high channel `h_t` feeds the running peak, so the statistic is genuinely intraday peak-to-trough; missing favorable-excursion data ⇒ VOID.
  4. Multiplier vectors are not deduplicated; K = 7,775 exactly; a final lexicographic tie-break makes the selected vector unique.
  5. The bootstrap is pinned: generator, start-index range, array shape and order, concatenation and truncation, window boundaries, and shared draws across configurations.
