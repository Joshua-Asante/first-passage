**Theme:** c1
**Status:** ACTIVE — Tradeify Select Flex 50K bust-cut Tests 1+2

> ## ⛔ SUPERSEDED 2026-07-22 (config-hygiene note added 2026-08-04) — Select Flex 50K figures below are computed on a DEFECTIVE input
>
> This run's Tradeify Select Flex 50K geometry carried `dd_lock_offset_usd: 100`, giving the
> simulated **evaluation** a drawdown-locking cushion Tradeify does not apply in eval
> (verbatim: *"Evaluation accounts do not have drawdown locking"* —
> [article 10495897](https://help.tradeify.co/en/articles/10495897-rules-trailing-max-drawdowns),
> re-verified 2026-07-22). The error is **optimistic** — the `bust<=5%` acceptance line below
> reads more favorably than the real eval geometry supports.
>
> This run additionally predates the R6 futures-prop NO-GO (2026-07-10, stated in the banner
> above the panel — this diagnostic never overturned it) and the current c1 2-leg book (this is
> the superseded 3-leg Aegis+Striker+Striker-NAS100 configuration). Both facts make the numbers
> below historical record, not a live gate.
>
> The numbers are **retained unedited as the historical record** of what was run on 2026-07-11.
> Do not cite them as current. Measurement of the defect's magnitude:
> [`../tradeify_eval_lock_correction_2026-07-22/RESULTS.md`](../tradeify_eval_lock_correction_2026-07-22/RESULTS.md) ·
> source-level fix: [`docs/adr/2026-08-04-firm-rules-eval-lock-fix-applied.md`](../../../../docs/adr/2026-08-04-firm-rules-eval-lock-fix-applied.md)

```
============================================================================================================
TRADEIFY SELECT FLEX 50K — bust-cut Tests 1+2 (2026-07-11) — DIAGNOSTIC ONLY
Governance: R6 futures-prop NO-GO stands; this run does not overturn it.
Sims: 10,000 x 3 seeds | dd-protection OFF (C2-off) | inactivity DISABLED | horizon 1500d
Arm: Select Flex 50K geometry-only only
Acceptance (pre-reg, not lock): A bust<=5%+p99<=5% | B Aegis attr<=55% or dropped | C med<=150d
============================================================================================================

### AEGIS INVENTORY  5274c (new) vs ae744 (prior remc)
  ae744 (old): N=152  PF=2.042  WR=34.87%  Net_static@200K=$70,817  init~$100,000  span=2020-02-24->2026-07-01  bytes=34824
             file=Aegis_JPY-Futures_v0.3_BEPAD-TEST_(MJY_6J)_CME_6J1!_2026-07-11_ae744.csv
  5274c (new): N=152  PF=2.212  WR=34.87%  Net_static@200K=$49,122  init~$100,000  span=2020-02-24->2026-07-01  bytes=34430
             file=Aegis_JPY-Futures_v0.3_BEPAD-TEST_(MJY_6J)_CME_6J1!_2026-07-11_5274c.csv
  delta: N=+0  PF=+0.170  Net_static=$-21,696  span_same=True
  material_change: YES

------------------------------------------------------------------------------------------------------------
### TEST 1 — Drop Aegis → 2-leg MYM+MNQ
STRATS=('striker', 'striker_nas100')  risk=striker=0.70% / striker_nas100=0.37%
PANEL  2020-01-06->2026-06-30  (1692 bdays)  book_net_scaled@200K=$89,400
  striker          N=267  risk=0.70%  1R=$2,535.61  scale=0.5521  net=$37,181
                  file=Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-11_15d8b.csv
  striker_nas100   N=284  risk=0.37%  1R=$5,899.32  scale=0.1254  net=$52,219
                  file=Striker_NAS100_v1_CME_MINI_MNQ1!_2026-07-11_beabf.csv

  50K geometry-only  pass=99.24%  bust=0.76%  p99=3.86%  med=222d
  bust_attr: striker=52.6%  striker_nas100=47.4%  (trailing=0.76% horizon=0.00%)
  Screen: A=PASS  B=PASS  C=FAIL  ALL=FAIL
  vs baseline 50K full-Aegis 1.50% (ae744): bust 10.33%→0.76% (-9.57pp)  p99 5.06%→3.86%  med 106→222d

------------------------------------------------------------------------------------------------------------
### TEST 2 — Aegis risk 1.50%→0.75% (0.5×), keep 3 legs
STRATS=('striker', 'striker_nas100', 'aegis')  risk=striker=0.70% / striker_nas100=0.37% / aegis=0.75%
PANEL  2020-01-06->2026-07-01  (1693 bdays)  book_net_scaled@200K=$531,772
  striker          N=267  risk=0.70%  1R=$2,535.61  scale=0.5521  net=$37,181
                  file=Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-11_15d8b.csv
  striker_nas100   N=284  risk=0.37%  1R=$5,899.32  scale=0.1254  net=$52,219
                  file=Striker_NAS100_v1_CME_MINI_MNQ1!_2026-07-11_beabf.csv
  aegis            N=152  risk=0.75%  1R=$166.56  scale=9.0056  net=$442,372  [WARN]
                  file=Aegis_JPY-Futures_v0.3_BEPAD-TEST_(MJY_6J)_CME_6J1!_2026-07-11_5274c.csv

  50K geometry-only  pass=60.57%  bust=39.43%  p99=9.82%  med=21d
  bust_attr: striker=1.7%  striker_nas100=1.4%  aegis=96.9%  (trailing=39.43% horizon=0.00%)
  Screen: A=FAIL  B=FAIL  C=PASS  ALL=FAIL
  vs baseline 50K full-Aegis 1.50% (ae744): bust 10.33%→39.43% (+29.10pp)  p99 5.06%→9.82%  med 106→21d

============================================================================================================
DECISION TABLE — Select Flex 50K geometry-only (pre-reg acceptance)
============================================================================================================
Test   Config                                        Pass    Bust     p99   Med  AegAttr  A  B  C  ALL
------------------------------------------------------------------------------------------------------------
base   3-leg Aegis 1.50% (ae744 prior)             89.67%  10.33%   5.06%   106    71.2%  -- -- --  --
1      Drop Aegis → 2-leg MYM+MNQ                  99.24%   0.76%   3.86%   222  dropped  P  P  F  FAIL
2      Aegis risk 1.50%→0.75% (0.5×), keep 3 legs  60.57%  39.43%   9.82%    21    96.9%  F  F  P  FAIL

NOTES:
  * Diagnostic only — no lock / ADR / ACTIVE_FIRM change
  * Test 2 uses new Aegis 5274c; Test 1 has no Aegis leg
  * MYM/MNQ files unchanged from prior futures3 remc (15d8b / beabf)
  * Baseline bust 10.33% is prior remc 50K geom with ae744 @ Aegis 1.50%

============================================================================================================
SENSITIVITY (Test 2 pin-fallback artifact) — DIAGNOSTIC
============================================================================================================
5274c has 0 full-stops after decompound (|L|>$2k); pin falls back to median loss $166.56 -> scale~9x. Primary Test 2 is NOT a clean 0.5x cut.
Exit qty mean: ae744=11.36  5274c=7.29  ratio=0.642  (5274c already ~half-sized vs ae744)

2b ae744 @ 0.75%: pass=97.98% bust=2.02% p99=4.10% med=152d  aegAttr=47.8%  A=PASS B=PASS C=FAIL ALL=FAIL
2c 5274c @ 0.75% size-adj 1R=$1869: pass=98.72% bust=1.28% p99=4.01% med=151d  aegAttr=42.1%  A=PASS B=PASS C=FAIL ALL=FAIL
```
