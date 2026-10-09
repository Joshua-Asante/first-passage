# Q-SFGROWTH-1 — Verdict pre-registration

**Status:** DRAFT 2026-10-09 — not frozen. Freezing requires the operator's GO and the commit hash recorded in the [parent brief §8](../Q-SFGROWTH-1-self-funded-growth-portfolio-selection.md#8--verdict-pre-registration). A verdict computed after any constant below moves is void; a changed constant is a new pre-registration.

## A — Pool

Legs with an accepted CME trade list, at their locked parameters, exports pinned by hash in `lab/analysis/c1/four_firm_remc_2026-10/run_four_firm_remc.py`:

| Leg | Instrument | Minimum lot |
|---|---|---|
| Aegis 6J | 6J (full size; no micro on Tradovate) | 1 contract |
| Striker DJ30 MYM p250 | MYM | 1 micro |
| Vanguard Gold MGC v0.4 | MGC | 1 micro |
| ORB MNQ v7 reconstruction | MNQ | 1 micro |
| *Striker NAS100 MNQ, DOW-excluded* | MNQ | 1 micro — **in the pool only if the operator rules it in before freeze** |

## B — Grid and K

- Each leg gets a multiplier `k_i ∈ {0, 1/8, 1/4, 1/2, 1, 2}` applied to its accepted per-trade quantity `q`.
- Scaled quantity: `n = floor(k_i · q)`. Per-trade P&L and adverse excursion scale by `n / q`. A trade with `n = 0` is dropped with its costs.
- A configuration is one vector `(k_1 … k_L)` with at least one non-zero leg. Configurations whose scaled trade lists are identical are deduplicated.
- **K = the count of distinct configurations after deduplication**, computed mechanically from the exports' quantities and written to the `register_search` manifest before any Explore read. Upper bound: 6^4 − 1 = 1,295 (four legs) or 6^5 − 1 = 7,775 (five).

## C — Statistic

**Series.** Per configuration, daily P&L `d_t` and intraday low `l_t ≤ 0` on the joint trading calendar, built by `remc_series_builder` (coincident-sum low), net of costs. Cost per side per instrument = the verified personal-Tradovate all-in rate (commission + exchange + NFA); unverified ⇒ VOID.

**Windows.** Common calendar span of the included legs' exports. Explore = earliest ⌊2/3⌋ of trading days; Confirm = the remainder.

**Paths.** Moving-block bootstrap of whole trading days (all legs resampled together), block = 20 days, horizon H = 252 days, N = 10,000 paths per seed, seeds {42, 123, 2026}. Start equity E_0 = $10,000.

**Per path, for t = 1…H:**
- running peak `P_{t-1} = max(E_0, E_1, …, E_{t-1})`
- intraday trough `T_t = E_{t-1} + l_t`
- **hit** if `(P_{t-1} − T_t) / P_{t-1} ≥ 0.15`; the path stops and its terminal equity is `T_t`
- otherwise `E_t = E_{t-1} + d_t`
- terminal equity = `E_H` if never hit

**Clears** (per configuration, per window, per cost multiple): hits ≤ 100 of 10,000 on **every** seed.
**Growth** = median terminal equity, pooled over the three seeds (30,000 paths).
**Rank** (Explore only): among configurations that clear with growth > $10,000, highest growth first; ties go to the lower pooled hit count, then the smaller total contract count.

### Worked example (synthetic, two days, one path)

E_0 = 10,000. Day 1: d = +200, l = −300. Day 2: d = −1,400, l = −1,600.

- Day 1: P_0 = 10,000; T_1 = 9,700; drawdown 300 / 10,000 = 3.0% → no hit; E_1 = 10,200.
- Day 2: P_1 = 10,200; T_2 = 10,200 − 1,600 = 8,600; drawdown 1,600 / 10,200 = 15.69% ≥ 15% → **hit**; terminal equity 8,600.

## D — Verdict table

| Verdict | Trigger | Disposition |
|---|---|---|
| RESOLVED | (1) ≥ 1 configuration clears on Explore at 1× cost with growth > $10,000; (2) the top-ranked one clears on Confirm at 1× cost; (3) it clears on Confirm at 1.5× cost; (4) its Confirm growth at 1× cost > $10,000 | INTEGRATE |
| FALSIFIED | condition (1) fails | STOP |
| AMBIGUOUS-HOLD | (1) holds and any of (2)–(4) fails | ITERATE (operator; no second pick) |
| VOID | an export hash mismatches its pin, run K ≠ manifest K, or a cost input is unverified | ITERATE (fix input, rerun unchanged) |

Only the top-ranked Explore configuration is scored on Confirm.
