# Tradeify Select Flex — 3-leg futures remc (2026-07-11)

**DIAGNOSTIC ONLY.** R6 futures-prop NO-GO stands. No change to `ACTIVE_FIRM`,
locked params, or ADRs.

## Tier choice

**Tradeify Select Flex** (`Tradeify_Select_{25,50,100,150}K` in `core/firm_rules.py`),
`dd_type="trailing_locking"`. Same tier family as
`lab/analysis/tradeify_selectflex_remc_2026-07-10/`. Select DD column (not Growth):
$1,000 / $2,000 / $3,000 / $4,500; target 6%; no daily loss; lock offset $100;
`min_trading_days=3`.

## What changed vs 2026-07-10 Tradeify remc

| | 2026-07-10 | This run |
|---|---|---|
| Hosts | Pepperstone CFD DJ30 (force-flat) + NAS100 + 6J prototype | CME MYM + MNQ + 6J **BEPAD-TEST** |
| Panel | `load_trades` + pinned CFD/6J 1R | decompounded static $200K (roe) + `pin_r_basis` scale to locked risk% |
| Book net @200K scaled | (different panel) | **$162,333** (matches prior decompound diagnostic) |
| Window | 2022-01→2026-07 (1172 bdays) | **2020-01→2026-07 (1693 bdays)** — includes 2020-22 chop |

Longer / earlier window + true futures hosts make this **not** a drop-in
numeric twin of the 2026-07-10 3-strat row; directionally comparable only.

## Headline

**No Select Flex tier clears bust&lt;1% AND p99 DD&lt;5%.** Geometry-only bust
10.3–17.7%; Aegis dominates bust attribution (~71%). See [`RESULTS.md`](RESULTS.md).

Driver: [`run_tradeify_futures3_remc.py`](run_tradeify_futures3_remc.py).
