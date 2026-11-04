**Theme:** c1

# Firm feasibility atlas — RESULTS

**Status:** ACTIVE — synthetic pass/bust/time-to-pass atlas over 540 shapes × 19 tier configs; T3 lookup in `atlas.py`
**Design:** [DESIGN.md](DESIGN.md), frozen at `a59a94f` before any run. **Run record:** [run_record.json](run_record.json). **Data:** [atlas.csv](atlas.csv).
**K = 0.** Every figure is from synthetic trade streams. No strategy, vendor or account data was read.

## How T3 uses it

```python
from research_utils.camp_import import load_camp_sibling
atlas = load_camp_sibling("atlas", "lab/analysis/c1/firm_feasibility_atlas_2026-11/atlas.py")
atlas.lookup("Tradeify_Select_100K", expectancy_r=0.08, win_rate=0.45,
             trades_per_session=0.6, risk_frac=0.12, mae="mid")
```

The function brackets each axis between its grid neighbours and returns the worst corner. For
MEDIUM tiers it also takes the worst over the sensitivity configs. It refuses off-grid shapes and
EXCLUDED tiers. `risk_frac` is 1R divided by the tier's drawdown allowance. `expectancy_r` is
net of costs.

## Run

All 540 shapes × 19 configs (10,260 cells, 1,000 paths each, horizon 1,500 business days) ran
through `scripts/fp.py python` in 3,707 s on 4 workers. The tracked tree was clean at `b7591a1`.
`run_record.json` pins the sha256 of the engine, the firm rules and the data. The bucket-sum
invariant held in every cell. Its `run_atlas.py` hash is of the run revision `b7591a1`; a later edit
(Codex review on #1069) changed only `--smoke`/`--out` argument handling, not the computation.

**Slow cells:** 104 of the 597 FEASIBLE cells leave more than 1% of paths unresolved at 1,500
days, and up to 45%. All of them have λ = 0.25 and f = 0.05. The label follows the frozen design
(bust and pass only), so for these shapes read the lookup's `bust_upper_at_horizon`
(bust + unresolved) as well.

## Tier coverage and exclusions

- **Read (14 of 15 listed tiers via the lookup):** Tradeify Select 25K/50K/100K/150K and Growth
  100K (HIGH); MFFU Rapid 50K/100K and BluSky Premium 50K/100K (MEDIUM, worst over their
  sensitivity configs); FXIFY Flex 150K (PROVISIONAL).
- **Excluded, Bulenox (all five tiers):** the venue trails the intraday high including open
  positions, while the engine ratchets on the EOD close (register A1.1, severity H). Every Bulenox
  bust below is a **lower bound** of unknown size. The tables keep them for completeness. The
  lookup refuses them unless the caller asks for the lower bound. `Bulenox_250K` may not exist
  (A1.2).
- **Sensitivities (paired on identical paths):**
  - MFFU at consistency 0.30 (A2.1) raises bust by 3–5 pp on average and up to 22 pp, with no
    label flips.
  - BluSky as a fixed-$ trail (F2) raises bust by ~1.3 pp on average and up to 5 pp, and flips
    1–2 shapes to not FEASIBLE.
  - The lookup takes the worse of each pair.

## Reading: which shapes suit which firm (INFERENCE, synthetic)

1. **The ratio of profit target to drawdown sets feasibility; the firm's name barely does.** With
   risk scaled to the drawdown allowance, tiers with the same ratio give near-identical maps.
   - Select 25K = 50K and 100K = 150K are bit-identical. Select 100K, MFFU 100K and BluSky 100K
     agree within noise. Their consistency rules (40/50/34%) almost never bind.
   - Ordered by ratio, best first: Bulenox 25K (1.0, lower bound) → Bulenox 50K (1.2) → the 1.5
     tiers (Select 25K/50K, MFFU 50K, BluSky 50K) → Growth (1.71) → the 2.0 tiers → Bulenox 250K
     (2.73).
   - At E = 0.10, f = 0.10, bust runs 43% at ratio 1.5, 48% at 1.71, 53% at 2.0.
2. **Bust, not pass, binds.** No tier clears the bust ceiling at E ≤ 0.05 R at any grid size. At
   E = 0.10 only f = 0.05 at p = 0.65 clears. At E = 0.20, f = 0.05 clears at p ≥ 0.50 (18 of 27
   (p, λ, MAE) combinations at every tier), and f = 0.10 clears only at p = 0.65. This repeats A2's finding that the rope binds.
   It now holds across every firm.
3. **At fixed expectancy, win rate is the strongest shape lever.** Low-p, high-payoff shapes carry
   more per-trade variance: at Select 100K, E = 0.10, f = 0.15, bust is 70% at p = 0.35 and 42%
   at p = 0.65. Deep winner excursions add 4–7 pp, because the intraday breach sees them.
4. **Trades per session sets the clock, not the risk.** At the same E and f, bust is flat across
   λ = 0.25 / 1 / 3, while median days to pass falls 206 → 51 → 19 (Select 100K, E = 0.10,
   f = 0.15). Any 30-day access window
   (Bulenox, D14) needs high-frequency shapes. At FEASIBLE sizes, P(pass ≤ 22 bdays) is about 0.
5. **FXIFY's lock at the starting balance** cuts bust by ~6 pp against an equal-ratio unlocked
   tier at f = 0.05, at the cost of slower passes. Provisional row, so treat this as direction
   only.
6. **For D10 (which family suits which firm), on this evidence:**
   - Prefer the 1.5-ratio tiers (Select 25K/50K, MFFU 50K, BluSky 50K) for any family, and a
     high-win-rate, shallow-excursion family wherever the ratio is 2.0.
   - A low-win-rate breakout family needs E ≥ 0.20 R net to clear anywhere.
   - These are feasibility statements only. They say nothing about which mechanisms exist at those
     edges.

**Reading limits:**
- E is net of costs and fills. At f = 0.05 of a $3,000 allowance, 1R is $150, so a micro round
  trip plus a tick of slippage is already a visible fraction of R (register D9, E-4).
- No gap-through-stop and no contract-cap binding are modelled.
- Inactivity is off (Tradeify T1 conflict).
- Eval stage only.

<!-- GENERATED:BEGIN (report.py) -->

Feasibility label: bust ≤ 0.05 and pass ≥ 0.50, parsed at render time from `2026-08-26-prop-survivor-scoring-prereg-v2.md` (+ 1 addendum) by `load_scoring_thresholds()`. Every figure is synthetic; MEDIUM tiers read worst over their sensitivity configs.

### Coverage

| Tier | Mark | DD $ | Target / DD | Consistency | Min days | Configs | FEASIBLE shapes / 540 |
|---|---|---|---|---|---|---|---|
| `Bulenox_25K` | EXCLUDED | 1,500 | 1.00 | — | 0 | 1 | 36 (bust is a lower bound) |
| `Bulenox_50K` | EXCLUDED | 2,500 | 1.20 | — | 0 | 1 | 36 (bust is a lower bound) |
| `Bulenox_100K` | EXCLUDED | 3,000 | 2.00 | — | 0 | 1 | 29 (bust is a lower bound) |
| `Bulenox_150K` | EXCLUDED | 4,500 | 2.00 | — | 0 | 1 | 29 (bust is a lower bound) |
| `Bulenox_250K` | EXCLUDED | 5,500 | 2.73 | — | 0 | 1 | 25 (bust is a lower bound) |
| `Tradeify_Select_25K` | HIGH | 1,000 | 1.50 | 40.0 | 3 | 1 | 34 |
| `Tradeify_Select_50K` | HIGH | 2,000 | 1.50 | 40.0 | 3 | 1 | 34 |
| `Tradeify_Select_100K` | HIGH | 3,000 | 2.00 | 40.0 | 3 | 1 | 28 |
| `Tradeify_Select_150K` | HIGH | 4,500 | 2.00 | 40.0 | 3 | 1 | 28 |
| `Tradeify_Growth_100K` | HIGH | 3,500 | 1.71 | — | 1 | 1 | 33 |
| `MFFU_Rapid_50K` | MEDIUM | 2,000 | 1.50 | 50.0 | 2 | 2 | 34 |
| `MFFU_Rapid_100K` | MEDIUM | 3,000 | 2.00 | 50.0 | 2 | 2 | 28 |
| `BluSky_Premium_50K` | MEDIUM | 2,000 | 1.50 | 34.0 | 0 | 2 | 34 |
| `BluSky_Premium_100K` | MEDIUM | 3,000 | 2.00 | 34.0 | 0 | 2 | 28 |
| `FXIFY_Futures_Flex_150K` | PROVISIONAL | 4,500 | 2.00 | 50.0 | 2 | 1 | 34 |

### Largest FEASIBLE risk fraction `f` by expectancy

Cell: largest FEASIBLE `f` over all (p, λ, MAE), then in brackets how many of the 27 (p, λ, MAE) combinations have any FEASIBLE `f`.

| Tier | E=0.00 | E=0.05 | E=0.10 | E=0.20 |
|---|---|---|---|---|
| `Bulenox_25K` | none | none | 0.05 (9/27) | 0.10 (18/27) |
| `Bulenox_50K` | none | none | 0.05 (9/27) | 0.10 (18/27) |
| `Bulenox_100K` | none | none | 0.05 (7/27) | 0.10 (18/27) |
| `Bulenox_150K` | none | none | 0.05 (7/27) | 0.10 (18/27) |
| `Bulenox_250K` | none | none | 0.05 (6/27) | 0.10 (18/27) |
| `Tradeify_Select_25K` | none | none | 0.05 (9/27) | 0.10 (18/27) |
| `Tradeify_Select_50K` | none | none | 0.05 (9/27) | 0.10 (18/27) |
| `Tradeify_Select_100K` | none | none | 0.05 (7/27) | 0.10 (18/27) |
| `Tradeify_Select_150K` | none | none | 0.05 (7/27) | 0.10 (18/27) |
| `Tradeify_Growth_100K` | none | none | 0.05 (9/27) | 0.10 (18/27) |
| `MFFU_Rapid_50K` | none | none | 0.05 (9/27) | 0.10 (18/27) |
| `MFFU_Rapid_100K` | none | none | 0.05 (7/27) | 0.10 (18/27) |
| `BluSky_Premium_50K` | none | none | 0.05 (9/27) | 0.10 (18/27) |
| `BluSky_Premium_100K` | none | none | 0.05 (7/27) | 0.10 (18/27) |
| `FXIFY_Futures_Flex_150K` | none | none | 0.05 (7/27) | 0.10 (18/27) |

### Cross-tier at one shape (E = 0.10, p = 0.50, λ = 1, MAE mid)

| Tier | Mark | f | pass % | bust % | unresolved % | median / p90 days | P(pass ≤ 22) % | P(pass ≤ 63) % |
|---|---|---|---|---|---|---|---|---|
| `Bulenox_25K` | EXCLUDED | 0.05 | 91.4 | 8.6 | 0.0 | 150 / 313 | 0.0 | 9.3 |
| `Bulenox_50K` | EXCLUDED | 0.05 | 89.7 | 10.3 | 0.0 | 183 / 354 | 0.0 | 3.1 |
| `Bulenox_100K` | EXCLUDED | 0.05 | 83.3 | 16.7 | 0.0 | 314 / 532 | 0.0 | 0.0 |
| `Bulenox_150K` | EXCLUDED | 0.05 | 83.3 | 16.7 | 0.0 | 314 / 532 | 0.0 | 0.0 |
| `Bulenox_250K` | EXCLUDED | 0.05 | 78.0 | 22.0 | 0.0 | 436 / 688 | 0.0 | 0.0 |
| `Tradeify_Select_25K` | HIGH | 0.05 | 86.5 | 13.5 | 0.0 | 234 / 421 | 0.0 | 0.7 |
| `Tradeify_Select_50K` | HIGH | 0.05 | 86.5 | 13.5 | 0.0 | 234 / 421 | 0.0 | 0.7 |
| `Tradeify_Select_100K` | HIGH | 0.05 | 81.8 | 18.2 | 0.0 | 310 / 521 | 0.0 | 0.0 |
| `Tradeify_Select_150K` | HIGH | 0.05 | 81.8 | 18.2 | 0.0 | 310 / 521 | 0.0 | 0.0 |
| `Tradeify_Growth_100K` | HIGH | 0.05 | 84.2 | 15.8 | 0.0 | 271 / 456 | 0.0 | 0.1 |
| `MFFU_Rapid_50K` | MEDIUM | 0.05 | 86.5 | 13.5 | 0.0 | 234 / 421 | 0.0 | 0.7 |
| `MFFU_Rapid_100K` | MEDIUM | 0.05 | 81.8 | 18.2 | 0.0 | 310 / 521 | 0.0 | 0.0 |
| `BluSky_Premium_50K` | MEDIUM | 0.05 | 86.5 | 13.5 | 0.0 | 236 / 425 | 0.0 | 0.7 |
| `BluSky_Premium_100K` | MEDIUM | 0.05 | 81.8 | 18.2 | 0.0 | 314 / 532 | 0.0 | 0.0 |
| `FXIFY_Futures_Flex_150K` | PROVISIONAL | 0.05 | 87.9 | 12.0 | 0.1 | 325 / 583 | 0.0 | 0.0 |
| `Bulenox_25K` | EXCLUDED | 0.10 | 70.1 | 29.9 | 0.0 | 50 / 111 | 10.8 | 44.5 |
| `Bulenox_50K` | EXCLUDED | 0.10 | 66.1 | 33.9 | 0.0 | 61 / 128 | 4.7 | 34.6 |
| `Bulenox_100K` | EXCLUDED | 0.10 | 49.3 | 50.7 | 0.0 | 102 / 183 | 0.0 | 8.3 |
| `Bulenox_150K` | EXCLUDED | 0.10 | 49.3 | 50.7 | 0.0 | 102 / 183 | 0.0 | 8.3 |
| `Bulenox_250K` | EXCLUDED | 0.10 | 38.1 | 61.9 | 0.0 | 141 / 219 | 0.0 | 1.3 |
| `Tradeify_Select_25K` | HIGH | 0.10 | 57.0 | 43.0 | 0.0 | 77 / 149 | 0.6 | 21.4 |
| `Tradeify_Select_50K` | HIGH | 0.10 | 57.0 | 43.0 | 0.0 | 77 / 149 | 0.6 | 21.4 |
| `Tradeify_Select_100K` | HIGH | 0.10 | 47.3 | 52.7 | 0.0 | 100 / 177 | 0.0 | 8.3 |
| `Tradeify_Select_150K` | HIGH | 0.10 | 47.3 | 52.7 | 0.0 | 100 / 177 | 0.0 | 8.3 |
| `Tradeify_Growth_100K` | HIGH | 0.10 | 52.1 | 47.9 | 0.0 | 88 / 163 | 0.2 | 13.4 |
| `MFFU_Rapid_50K` | MEDIUM | 0.10 | 56.6 | 43.4 | 0.0 | 77 / 150 | 0.6 | 21.2 |
| `MFFU_Rapid_100K` | MEDIUM | 0.10 | 47.3 | 52.7 | 0.0 | 100 / 177 | 0.0 | 8.3 |
| `BluSky_Premium_50K` | MEDIUM | 0.10 | 57.0 | 43.0 | 0.0 | 78 / 150 | 0.6 | 21.3 |
| `BluSky_Premium_100K` | MEDIUM | 0.10 | 47.3 | 52.7 | 0.0 | 102 / 183 | 0.0 | 8.3 |
| `FXIFY_Futures_Flex_150K` | PROVISIONAL | 0.10 | 57.9 | 42.1 | 0.0 | 111 / 219 | 0.0 | 8.3 |

### Per tier at the reference slice (p = 0.5, λ = 1.0, MAE mid)

Cell: pass % / bust % / median business days to pass. **Bold** = FEASIBLE.

**`Bulenox_25K`** (EXCLUDED; bust is a LOWER BOUND)

| f \ E | 0.00 | 0.05 | 0.10 | 0.20 |
|---|---|---|---|---|
| 0.05 | 38.4 / 61.6 / 237 | 73.8 / 26.2 / 205 | 91.4 / 8.6 / 150 | **99.2 / 0.8 / 90** |
| 0.10 | 38.5 / 61.5 / 62 | 56.8 / 43.2 / 57 | 70.1 / 29.9 / 50 | 89.0 / 11.0 / 38 |
| 0.15 | 38.6 / 61.4 / 32 | 53.9 / 46.1 / 28 | 63.3 / 36.7 / 26 | 75.2 / 24.8 / 20 |
| 0.25 | 42.2 / 57.8 / 10 | 43.6 / 56.4 / 12 | 51.6 / 48.4 / 10 | 62.8 / 37.2 / 9 |
| 0.33 | 30.0 / 70.0 / 10 | 44.3 / 55.7 / 7 | 46.9 / 53.1 / 7 | 58.2 / 41.8 / 6 |

**`Bulenox_50K`** (EXCLUDED; bust is a LOWER BOUND)

| f \ E | 0.00 | 0.05 | 0.10 | 0.20 |
|---|---|---|---|---|
| 0.05 | 32.8 / 67.1 / 286 | 69.4 / 30.6 / 246 | 89.7 / 10.3 / 183 | **99.1 / 0.9 / 107** |
| 0.10 | 32.0 / 68.0 / 78 | 51.7 / 48.3 / 69 | 66.1 / 33.9 / 61 | 85.5 / 14.5 / 45 |
| 0.15 | 34.3 / 65.7 / 37 | 48.7 / 51.3 / 35 | 58.1 / 41.9 / 31 | 72.5 / 27.5 / 24 |
| 0.25 | 32.7 / 67.3 / 13 | 38.8 / 61.2 / 14 | 47.1 / 52.9 / 12 | 57.6 / 42.4 / 11 |
| 0.33 | 30.0 / 70.0 / 10 | 37.2 / 62.8 / 10 | 42.6 / 57.4 / 7 | 53.5 / 46.5 / 8 |

**`Bulenox_100K`** (EXCLUDED; bust is a LOWER BOUND)

| f \ E | 0.00 | 0.05 | 0.10 | 0.20 |
|---|---|---|---|---|
| 0.05 | 14.1 / 85.9 / 556 | 54.7 / 45.3 / 430 | 83.3 / 16.7 / 314 | **98.6 / 1.4 / 187** |
| 0.10 | 16.3 / 83.7 / 131 | 34.8 / 65.2 / 129 | 49.3 / 50.7 / 102 | 76.0 / 24.0 / 76 |
| 0.15 | 15.9 / 84.1 / 70 | 31.7 / 68.3 / 57 | 41.8 / 58.2 / 54 | 61.0 / 39.0 / 41 |
| 0.25 | 16.9 / 83.1 / 23 | 21.1 / 78.9 / 22 | 31.1 / 68.9 / 21 | 44.3 / 55.7 / 17 |
| 0.33 | 13.7 / 86.3 / 18 | 21.2 / 78.8 / 16 | 28.2 / 71.8 / 13 | 39.2 / 60.8 / 11 |

**`Bulenox_150K`** (EXCLUDED; bust is a LOWER BOUND)

| f \ E | 0.00 | 0.05 | 0.10 | 0.20 |
|---|---|---|---|---|
| 0.05 | 14.1 / 85.9 / 556 | 54.7 / 45.3 / 430 | 83.3 / 16.7 / 314 | **98.6 / 1.4 / 187** |
| 0.10 | 16.3 / 83.7 / 131 | 34.8 / 65.2 / 129 | 49.3 / 50.7 / 102 | 76.0 / 24.0 / 76 |
| 0.15 | 15.9 / 84.1 / 70 | 31.7 / 68.3 / 57 | 41.8 / 58.2 / 54 | 61.0 / 39.0 / 41 |
| 0.25 | 16.9 / 83.1 / 23 | 21.1 / 78.9 / 22 | 31.1 / 68.9 / 21 | 44.3 / 55.7 / 17 |
| 0.33 | 13.7 / 86.3 / 18 | 21.2 / 78.8 / 16 | 28.2 / 71.8 / 13 | 39.2 / 60.8 / 11 |

**`Bulenox_250K`** (EXCLUDED; bust is a LOWER BOUND)

| f \ E | 0.00 | 0.05 | 0.10 | 0.20 |
|---|---|---|---|---|
| 0.05 | 7.4 / 92.4 / 682 | 42.5 / 57.3 / 601 | 78.0 / 22.0 / 436 | **97.7 / 2.3 / 263** |
| 0.10 | 6.6 / 93.4 / 186 | 23.2 / 76.8 / 175 | 38.1 / 61.9 / 141 | 69.4 / 30.6 / 104 |
| 0.15 | 8.6 / 91.4 / 86 | 20.3 / 79.7 / 85 | 31.1 / 68.9 / 73 | 52.1 / 47.9 / 56 |
| 0.25 | 9.4 / 90.6 / 33 | 12.9 / 87.1 / 34 | 21.1 / 78.9 / 28 | 31.7 / 68.3 / 24 |
| 0.33 | 8.1 / 91.9 / 24 | 12.2 / 87.8 / 20 | 19.4 / 80.6 / 17 | 29.9 / 70.1 / 16 |

**`Tradeify_Select_25K`** (HIGH)

| f \ E | 0.00 | 0.05 | 0.10 | 0.20 |
|---|---|---|---|---|
| 0.05 | 22.6 / 77.4 / 372 | 63.1 / 36.9 / 312 | 86.5 / 13.5 / 234 | **98.7 / 1.3 / 140** |
| 0.10 | 23.9 / 76.1 / 93 | 43.4 / 56.6 / 88 | 57.0 / 43.0 / 77 | 79.9 / 20.1 / 56 |
| 0.15 | 26.7 / 73.3 / 48 | 41.1 / 58.9 / 45 | 50.0 / 50.0 / 38 | 66.1 / 33.9 / 30 |
| 0.25 | 22.6 / 77.4 / 18 | 27.0 / 73.0 / 19 | 35.2 / 64.8 / 16 | 43.8 / 56.2 / 15 |
| 0.33 | 19.5 / 80.5 / 12 | 23.2 / 76.8 / 13 | 25.0 / 75.0 / 13 | 35.6 / 64.4 / 12 |

**`Tradeify_Select_50K`** (HIGH)

| f \ E | 0.00 | 0.05 | 0.10 | 0.20 |
|---|---|---|---|---|
| 0.05 | 22.6 / 77.4 / 372 | 63.1 / 36.9 / 312 | 86.5 / 13.5 / 234 | **98.7 / 1.3 / 140** |
| 0.10 | 23.9 / 76.1 / 93 | 43.4 / 56.6 / 88 | 57.0 / 43.0 / 77 | 79.9 / 20.1 / 56 |
| 0.15 | 26.7 / 73.3 / 48 | 41.1 / 58.9 / 45 | 50.0 / 50.0 / 38 | 66.1 / 33.9 / 30 |
| 0.25 | 22.6 / 77.4 / 18 | 27.0 / 73.0 / 19 | 35.2 / 64.8 / 16 | 43.8 / 56.2 / 15 |
| 0.33 | 19.5 / 80.5 / 12 | 23.2 / 76.8 / 13 | 25.0 / 75.0 / 13 | 35.6 / 64.4 / 12 |

**`Tradeify_Select_100K`** (HIGH)

| f \ E | 0.00 | 0.05 | 0.10 | 0.20 |
|---|---|---|---|---|
| 0.05 | 13.4 / 86.6 / 540 | 52.6 / 47.4 / 424 | 81.8 / 18.2 / 310 | **98.1 / 1.9 / 186** |
| 0.10 | 15.2 / 84.8 / 127 | 33.1 / 66.9 / 126 | 47.3 / 52.7 / 100 | 73.8 / 26.2 / 75 |
| 0.15 | 15.9 / 84.1 / 70 | 30.4 / 69.6 / 56 | 40.2 / 59.8 / 51 | 59.3 / 40.7 / 41 |
| 0.25 | 16.9 / 83.1 / 23 | 20.3 / 79.7 / 22 | 28.1 / 71.9 / 22 | 39.9 / 60.1 / 18 |
| 0.33 | 12.2 / 87.8 / 18 | 18.4 / 81.6 / 17 | 22.7 / 77.3 / 15 | 32.9 / 67.1 / 13 |

**`Tradeify_Select_150K`** (HIGH)

| f \ E | 0.00 | 0.05 | 0.10 | 0.20 |
|---|---|---|---|---|
| 0.05 | 13.4 / 86.6 / 540 | 52.6 / 47.4 / 424 | 81.8 / 18.2 / 310 | **98.1 / 1.9 / 186** |
| 0.10 | 15.2 / 84.8 / 127 | 33.1 / 66.9 / 126 | 47.3 / 52.7 / 100 | 73.8 / 26.2 / 75 |
| 0.15 | 15.9 / 84.1 / 70 | 30.4 / 69.6 / 56 | 40.2 / 59.8 / 51 | 59.3 / 40.7 / 41 |
| 0.25 | 16.9 / 83.1 / 23 | 20.3 / 79.7 / 22 | 28.1 / 71.9 / 22 | 39.9 / 60.1 / 18 |
| 0.33 | 12.2 / 87.8 / 18 | 18.4 / 81.6 / 17 | 22.7 / 77.3 / 15 | 32.9 / 67.1 / 13 |

**`Tradeify_Growth_100K`** (HIGH)

| f \ E | 0.00 | 0.05 | 0.10 | 0.20 |
|---|---|---|---|---|
| 0.05 | 17.8 / 82.2 / 448 | 58.7 / 41.3 / 365 | 84.2 / 15.8 / 271 | **98.3 / 1.7 / 160** |
| 0.10 | 18.3 / 81.7 / 113 | 39.2 / 60.8 / 106 | 52.1 / 47.9 / 88 | 76.1 / 23.9 / 64 |
| 0.15 | 20.6 / 79.4 / 56 | 36.2 / 63.8 / 50 | 46.6 / 53.4 / 44 | 62.8 / 37.2 / 34 |
| 0.25 | 20.1 / 79.9 / 20 | 25.9 / 74.1 / 19 | 35.2 / 64.8 / 17 | 47.7 / 52.3 / 15 |
| 0.33 | 17.3 / 82.7 / 14 | 25.8 / 74.2 / 13 | 32.6 / 67.4 / 11 | 43.8 / 56.2 / 10 |

**`MFFU_Rapid_50K`** (MEDIUM)

| f \ E | 0.00 | 0.05 | 0.10 | 0.20 |
|---|---|---|---|---|
| 0.05 | 22.6 / 77.4 / 372 | 63.1 / 36.9 / 312 | 86.5 / 13.5 / 234 | **98.7 / 1.3 / 140** |
| 0.10 | 23.7 / 76.3 / 93 | 42.9 / 57.1 / 88 | 56.6 / 43.4 / 77 | 79.3 / 20.7 / 57 |
| 0.15 | 25.7 / 74.3 / 49 | 37.7 / 62.3 / 47 | 46.8 / 53.2 / 42 | 62.5 / 37.5 / 33 |
| 0.25 | 17.1 / 82.9 / 23 | 20.2 / 79.8 / 22 | 25.7 / 74.3 / 22 | 33.8 / 66.2 / 19 |
| 0.33 | 11.2 / 88.8 / 17 | 14.1 / 85.9 / 18 | 17.3 / 82.7 / 15 | 27.5 / 72.5 / 16 |

**`MFFU_Rapid_100K`** (MEDIUM)

| f \ E | 0.00 | 0.05 | 0.10 | 0.20 |
|---|---|---|---|---|
| 0.05 | 13.4 / 86.6 / 540 | 52.6 / 47.4 / 424 | 81.8 / 18.2 / 310 | **98.1 / 1.9 / 186** |
| 0.10 | 15.2 / 84.8 / 127 | 32.9 / 67.1 / 126 | 47.3 / 52.7 / 100 | 73.8 / 26.2 / 75 |
| 0.15 | 15.7 / 84.3 / 70 | 29.8 / 70.2 / 58 | 39.4 / 60.6 / 52 | 57.9 / 42.1 / 42 |
| 0.25 | 14.4 / 85.6 / 26 | 17.7 / 82.3 / 24 | 24.8 / 75.2 / 23 | 32.3 / 67.7 / 21 |
| 0.33 | 10.3 / 89.7 / 19 | 12.2 / 87.8 / 20 | 15.4 / 84.6 / 16 | 25.4 / 74.6 / 17 |

**`BluSky_Premium_50K`** (MEDIUM)

| f \ E | 0.00 | 0.05 | 0.10 | 0.20 |
|---|---|---|---|---|
| 0.05 | 22.6 / 77.4 / 380 | 63.1 / 36.9 / 319 | 86.5 / 13.5 / 236 | **98.7 / 1.3 / 140** |
| 0.10 | 23.9 / 76.1 / 98 | 43.1 / 56.9 / 90 | 57.0 / 43.0 / 78 | 79.6 / 20.4 / 57 |
| 0.15 | 26.1 / 73.9 / 49 | 40.1 / 59.9 / 46 | 49.1 / 50.9 / 41 | 64.5 / 35.5 / 32 |
| 0.25 | 21.6 / 78.4 / 20 | 24.5 / 75.5 / 20 | 29.8 / 70.2 / 20 | 38.5 / 61.5 / 18 |
| 0.33 | 14.4 / 85.6 / 14 | 18.3 / 81.7 / 17 | 19.8 / 80.2 / 15 | 30.8 / 69.2 / 14 |

**`BluSky_Premium_100K`** (MEDIUM)

| f \ E | 0.00 | 0.05 | 0.10 | 0.20 |
|---|---|---|---|---|
| 0.05 | 13.4 / 86.6 / 556 | 52.6 / 47.4 / 430 | 81.8 / 18.2 / 314 | **98.1 / 1.9 / 187** |
| 0.10 | 15.2 / 84.8 / 131 | 33.1 / 66.9 / 129 | 47.3 / 52.7 / 102 | 73.8 / 26.2 / 76 |
| 0.15 | 15.9 / 84.1 / 70 | 30.4 / 69.6 / 57 | 40.1 / 59.9 / 54 | 59.0 / 41.0 / 42 |
| 0.25 | 15.8 / 84.2 / 24 | 18.7 / 81.3 / 24 | 26.4 / 73.6 / 23 | 37.2 / 62.8 / 19 |
| 0.33 | 11.1 / 88.9 / 19 | 16.7 / 83.3 / 19 | 18.0 / 82.0 / 16 | 28.3 / 71.7 / 16 |

**`FXIFY_Futures_Flex_150K`** (PROVISIONAL)

| f \ E | 0.00 | 0.05 | 0.10 | 0.20 |
|---|---|---|---|---|
| 0.05 | 17.2 / 81.5 / 614 | 62.7 / 37.2 / 472 | 87.9 / 12.0 / 325 | **98.9 / 1.1 / 187** |
| 0.10 | 20.3 / 79.7 / 151 | 42.1 / 57.9 / 141 | 57.9 / 42.1 / 111 | 82.6 / 17.4 / 79 |
| 0.15 | 20.3 / 79.7 / 77 | 37.5 / 62.5 / 66 | 49.6 / 50.4 / 60 | 68.3 / 31.7 / 43 |
| 0.25 | 21.4 / 78.6 / 27 | 27.6 / 72.4 / 27 | 38.8 / 61.2 / 24 | 50.8 / 49.2 / 19 |
| 0.33 | 18.2 / 81.8 / 21 | 26.9 / 73.1 / 18 | 33.9 / 66.1 / 16 | 45.5 / 54.5 / 14 |

### Axis effects on `Tradeify_Select_100K` (E = 0.10, f = 0.15): bust % by win rate × MAE, then by trades per session

| p \ MAE | tight | mid | deep |
|---|---|---|---|
| 0.35 | 71.8 | 70.1 | 76.2 |
| 0.50 | 60.1 | 59.8 | 63.7 |
| 0.65 | 42.2 | 42.0 | 49.1 |

| λ | bust % | pass % | median days | P(pass ≤ 22 bdays) % |
|---|---|---|---|---|
| 0.25 | 60.8 | 39.2 | 206 | 0.0 |
| 1.0 | 59.8 | 40.2 | 51 | 2.0 |
| 3.0 | 61.3 | 38.7 | 19 | 24.9 |

### Sensitivity configs vs their row (paired over all 540 shapes)

| Sensitivity | Mean Δbust (pp) | Max Δbust (pp) | Mean Δpass (pp) | Shapes whose label flips |
|---|---|---|---|---|
| `BluSky_Premium_100K@fixed$` | +1.26 | +4.20 | -1.18 | 1 |
| `BluSky_Premium_50K@fixed$` | +1.32 | +4.70 | -1.26 | 2 |
| `MFFU_Rapid_100K@cons0.30` | +3.10 | +19.10 | -3.10 | 0 |
| `MFFU_Rapid_50K@cons0.30` | +5.38 | +21.70 | -5.38 | 0 |

### Same-geometry tiers (paired, same paths)

| Pair | Max |Δpass| (pp) | Max |Δbust| (pp) |
|---|---|---|
| `Tradeify_Select_25K` vs `Tradeify_Select_50K` | 0.00 | 0.00 |
| `Tradeify_Select_100K` vs `Tradeify_Select_150K` | 0.00 | 0.00 |
| `Bulenox_100K` vs `Bulenox_150K` | 0.00 | 0.00 |

<!-- GENERATED:END -->
