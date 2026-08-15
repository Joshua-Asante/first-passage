# FXIFY DXTrade overnight swap rates — 2026-05-25

**Source:** FXIFY DXTrade Instrument Details modals (4 instruments), screenshotted by Joshua 2026-05-25.

**Calibration anchor:** 2026-05-25 Guardian XAUUSD live trade (Trade Journal page `36cdc0b5-3c11-8197-a85e-d309859ca393`). 0.69 lot × -$57.49/lot/night × 1 rollover = **-$39.67** — matches DXTrade Net-vs-gross delta exactly (Net Closed P&L -$733.12 minus gross Closed P&L -$693.45 = -$39.67). This is the empirical calibration that ties the screenshot pip values to actual USD swap costs.

**Convention:** All rates from the Monday-row of the Instrument Details modal's "Overnight Rates" panel; FXIFY DXTrade timezone declared as America/New_York. Triple-rollover (Wed/Fri convention for metals/forex) not modeled in first-pass — naive day-counting sums cumulative carry correctly over weekends.

**Screenshot storage:** Source images held in Joshua's chat session 2026-05-25. Repo-pinned provenance available if images are dropped into `docs/external/fxify_swap_rates_2026-05-25/`. Until then, this markdown record is the canonical Tier-1 citation per `brief-authoring` §0 sub-rule (verbatim quotes of constants).

---

## Per-instrument rates (verbatim from screenshots)

| Instrument | Asset Type | Lot Size | Precision | Currency | Long swap | Short swap |
|---|---|---:|---:|---|---:|---:|
| XAUUSD.XX (Gold)        | CFD              |     100 | 0.01  | USD | **-57.49 pips** | **+43.84 pips** |
| USDJPY.x                | Foreign Exchange | 100,000 | 0.001 | JPY | **+0.005 pips** | **-0.01 pips** |
| DJ30.x (US Top 30)      | CFD              |      10 | 0.01  | USD | **-9.69 pips**  | **+1.94 pips**  |
| USTEC.x (Nasdaq 100)    | CFD              |      10 | 0.01  | USD | **-5.23 pips**  | **+1.05 pips**  |

All four screens show "Trade & Holiday Schedule (America/New_York)" with the Monday row highlighted.

---

## Per-lot-per-night USD conversion

Convention: `pip_value_USD_per_lot = Precision × Lot_Size × (1 / quote_currency_USDrate)`. For USD-quoted instruments (XAUUSD, DJ30, USTEC), the FX conversion is the identity. For JPY-quoted USDJPY, divide by USDJPY rate (flat 150 used as first-pass; per-trade exit price would be more precise but the magnitude makes the approximation error sub-dollar).

| Instrument | Pip value per lot | Long swap per lot per night | Short swap per lot per night |
|---|---:|---:|---:|
| XAUUSD  | $1.00     (= 0.01 × 100)              | **-$57.49**  | +$43.84  |
| USDJPY  | ¥100 ≈ $0.67 (= 0.001 × 100,000 / 150) | **+$0.0033** | -$0.0067 |
| DJ30    | $0.10     (= 0.01 × 10)               | **-$0.969**  | +$0.194  |
| NAS100  | $0.10     (= 0.01 × 10)               | **-$0.523**  | +$0.105  |

**Magnitude ranking (long, per lot per night):**
1. XAUUSD: -$57.49 (dominant; ~10× DJ30, ~100× NAS100, ~17,400× USDJPY)
2. DJ30: -$0.969
3. NAS100: -$0.523
4. USDJPY: **+$0.0033 (positive carry)**

---

## Use sites

- `guardian_swap_impact.py` (deleted; Q-SWAP domain retired 2026-06-05) — Guardian-only sizing (2026-05-25)
- `portfolio_swap_impact.py` (deleted; Q-SWAP domain retired 2026-06-05) — 4-strategy aggregate sizing (2026-05-25)
- [`docs/ltm/briefs/Q-SWAP-1-portfolio-swap-impact.md`](../ltm/briefs/Q-SWAP-1-portfolio-swap-impact.md) — Pre-Q §0 Tier-1 citation anchor

---

## Limitations of the first-pass sizing

- **Flat rate, no triple-rollover (Wed/Fri) modeling.** Cumulative carry over weekends still sums correctly under naive day-counting (3 nights of carry charged as 3× somewhere, vs 1× three times — the SUM matches). Brokers vary on which day applies the 3× rate; rates here may need refinement when modeling specific trades against actual broker swap-day convention.
- **FXIFY rates applied to Pepperstone CSV lot sizes** (cross-broker substitution flagged in Q-SWAP-1 §3). Pepperstone's actual swap rates may differ, but typical broker spread on these instruments is within ±20%.
- **USDJPY uses flat USDJPY = 150 conversion.** Per-trade exit price would be more precise; Aegis swap magnitude (~$1 across 124 trades) makes the flat-rate approximation error sub-dollar.
- **Monday rates only.** Other days' rates not screenshotted; assumed equal to Monday for first-pass. If FXIFY's rates vary materially day-of-week, refine when modeling the full portfolio MC.
