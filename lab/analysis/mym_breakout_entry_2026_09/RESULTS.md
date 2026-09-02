# MYM breakout-entry study — 2026-09

**Verdict:** **NO ROBUST CANDIDATE.** None of the five predeclared entry families reaches both
`net expectancy >= 0.10R/trade` and `win rate >= 45%` on validation. A holdout-protocol deviation
then consumed all predeclared holdout cells despite selecting no candidate. Those values are
exploratory only: their best fixed-spec point estimate is close-confirmed at **+0.025R**, well below
the expectancy floor, with a 95% bootstrap interval of **[-0.045R, +0.095R]**. There is **no
holdout-confirmed conclusion**.

## Data audit

The source was
`BAR_EXPORT_v0.2_CBOT_MINI_MYM1!_2026-09-01_1b59b.csv`, parsed only through
`scripts/parse_bar_export.py`. The canonical output has **170,417** unique chronological M15 bars
from **2019-05-05 22:15 UTC** through **2026-07-31 20:45 UTC**. The v0.2 sidecar says `MYM1!`,
`futures`, USD quote, `mintick=1.0`, `pointvalue=0.5`, `America/Chicago`, timeframe 15. Those
constants match `ops/instruments/MYM.md`: one point/tick is $0.50 per MYM contract.

There are no duplicate timestamps, invalid OHLC rows, negative volumes, or ordering defects.
167,995 intervals are exactly 15 minutes; 2,421 are irregular, chiefly the expected daily Globex
maintenance/weekend breaks plus missing bars. The exact 27-timestamp RTH grid yields **1,804
complete sessions**; 64 short/holiday sessions are excluded. Six other similarly named Downloads files were
audited by encoded timestamp range: they overlap this history or are 378-row diagnostic exports,
and none extends beyond 2026-07-31, so they are not adjacent pages.

Limitations matter: `MYM1!` is an unadjusted rolling continuous contract, OHLC cannot identify the
intrabar path, the file ends a month before its filename date, and spread/slippage is modeled rather
than reconstructed from quotes. Full audit fields are in `data_audit.json`.

## Frozen hypotheses and method

The transparent baseline is an **immediate stop entry** at the 08:30–09:00 Chicago opening-range
boundary. Alternatives were frozen before outcome evaluation:

1. immediate boundary touch;
2. first close beyond the boundary, next-bar-open entry;
3. immediate touch with a fixed 10-point buffer;
4. close breakout plus first retest within 25 points, next-bar-open entry;
5. two consecutive closes beyond the boundary, next-bar-open entry.

Every cell uses one MYM, at most one trade/session, a hard 1R target, and force-flat by 15:00.
Headline initial price risk is **300 points × $0.50 = $150**; 250/$125 and 350/$175 are the declared
neighbors. Headline round-trip costs are **$1.82 commission/fees** (`$0.91/side`, repository
Tradeify Select configuration) plus **one adverse tick per side**, $2.82 total. Sensitivities use
0/1/2/4 adverse ticks per side. Both stop and target touched in one bar means stop first; gap-through
stops fill at the worse of stop or open; same-bar long+short entry touches produce no trade.

Development is 2019–2022, validation 2023–2024, and the intended holdout is 2025–2026-07-31.
Catalogue selection uses validation only and selected nothing. The implementation nevertheless
computed all intended-holdout cells before enforcing that gate. `results.json` therefore labels
them `consumed_exploratory_not_confirmatory`; they are reported for disclosure, never as Confirm
evidence. Confidence intervals are deterministic 2,000-sample trade-level bootstrap intervals.
Every one of the **60 declared cells** (5 families × 3 stops × 4 slippages) is retained in
`results.json`; there was no best-cell suppression.

## Existing baseline context

The repository's prior frozen MYM opening-range-continuation result remains the authoritative
historical baseline: `S-MYM-ORC-02` reported n=403, net -0.0210R and PF 0.951. Its exact executable
body is unavailable in this public checkout and its pinned vendor panel is stale, so reproducing it
from prose would be false precision. This study therefore does **not** claim reproduction or revival
of that dead mechanism; it tests the fully disclosed baseline above on the newly supplied bars.

## Fixed-spec chronological results

All figures include $2.82 round-trip cost and use the $150 initial stop risk.

| Family | Development n / WR / net R | Validation n / WR / net R | Consumed holdout (exploratory) n / WR / net R (95% CI) |
|---|---:|---:|---:|
| Immediate baseline | 899 / 49.7% / -0.023 | 485 / 47.0% / -0.027 | 387 / 52.2% / +0.008 [-0.063,+0.082] |
| Close-confirmed | 889 / 49.4% / -0.019 | 475 / 49.5% / +0.000 | 380 / 53.2% / +0.025 [-0.045,+0.095] |
| Buffer 10 | 894 / 49.4% / -0.018 | 483 / 47.8% / -0.033 | 386 / 52.1% / -0.008 [-0.082,+0.068] |
| Retest 25 | 762 / 49.7% / -0.028 | 413 / 46.5% / -0.018 | 296 / 50.7% / -0.022 [-0.094,+0.049] |
| Two-close momentum | 845 / 48.9% / -0.024 | 451 / 46.6% / -0.016 | 359 / 49.6% / -0.023 [-0.087,+0.045] |

The closest family, close-confirmed, has validation PF 1.001 and max drawdown 10.31R; holdout PF
1.094 and max drawdown 8.28R. Holdout average win/loss are +0.560R/-0.581R.

## Long/short and stability

Close-confirmed is asymmetric in validation: longs are n=237, WR 52.3%, +0.050R, PF 1.262;
shorts are n=238, WR 46.6%, -0.049R, PF 0.810. The holdout reverses that concern rather than
confirming a stable long-only edge: longs are n=202, +0.011R, while shorts are n=178, +0.042R.
No directional sleeve reaches +0.10R, and direction selection was not predeclared, so neither is a
candidate.

Close-confirmed annual net expectancy is -0.033R (2019), +0.013R (2020), -0.059R (2021), -0.004R
(2022), -0.001R (2023), +0.001R (2024), +0.026R (2025), and +0.025R (2026 partial). Every annual
95% interval contains zero. This is flat/noisy behavior, not a stable 0.10R process.

## Cost, stop-risk, and neighborhood robustness

Close-confirmed is the best validation family, but even its **zero-slippage** validation results are
only +0.012R/$125, +0.007R/$150, and -0.002R/$175. At the headline one-tick model they are
+0.004R, +0.000R, and -0.008R. Four ticks per side reduce them to -0.020R, -0.020R, and -0.025R.
No parameter neighbor approaches +0.10R. All stops stay inside the requested $100–$200 price-risk
band; execution costs add $1.82–$5.82 round trip depending on sensitivity.

## Conclusion and next step

The honest conclusion is **no candidate**. Sample sizes are adequate for screening, but uncertainty
still spans modest positive and negative expectancy; critically, even optimistic point estimates
are far below +0.10R. The closest result is close-confirmed, whose benefit is only avoiding some
bad intrabar touches, not establishing a tradable edge.

Do not tune another buffer, stop, target, or confirmation count on the consumed holdout. A defensible next
step needs genuinely new information: forward MYM bars collected after 2026-07-31 and a newly
predeclared mechanism/conditioner (for example independently justified volume-regime work), or
tick/quote data that can test whether the conservative OHLC fill model is materially too harsh.
The current catalogue should remain closed unless such evidence changes the mechanism, not merely
the parameters.

## Reproduction

```powershell
python scripts\parse_bar_export.py --symbol MYM --in workspace_inputs\BAR_EXPORT_v0.2_CBOT_MINI_MYM1!_2026-09-01_1b59b.csv --out workspace_outputs\mym_breakout_entry\MYM_M15.csv
python -m lab.analysis.mym_breakout_entry_2026_09.run_research --bars workspace_outputs\mym_breakout_entry\MYM_M15.csv --meta workspace_outputs\mym_breakout_entry\MYM_M15.meta.json --out-dir lab\analysis\mym_breakout_entry_2026_09 --trades-out workspace_outputs\mym_breakout_entry\all_declared_trades.csv
python -m unittest tests.lab.test_mym_breakout_entry -v
```

The local-only complete ledger has 100,848 rows and SHA-256
`f881a9c60da0e40f206f2048764f777c66a296cae31deab8b06337ddda2ae4f7`. It is not committed
because it contains vendor-derived timestamps and prices; the hash and row count are also stored in
`results.json`.
