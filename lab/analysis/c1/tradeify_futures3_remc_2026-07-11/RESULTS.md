**Theme:** c1
**Status:** ACTIVE — Tradeify Select Flex 3-leg futures remc panel

> ## ⛔ SUPERSEDED 2026-07-22 (config-hygiene note added 2026-08-04) — `Tradeify_Select_*` figures below are computed on a DEFECTIVE input
>
> This run's `Tier: Tradeify_Select_*` rows carried `dd_lock_offset_usd: 100`, giving the
> simulated **evaluation** a drawdown-locking cushion Tradeify does not apply in eval
> (verbatim: *"Evaluation accounts do not have drawdown locking"* —
> [article 10495897](https://help.tradeify.co/en/articles/10495897-rules-trailing-max-drawdowns),
> re-verified 2026-07-22). The error is **optimistic** — the `bust<1%` gate below reads
> more favorably than the real eval geometry supports.
>
> This run additionally predates the R6 futures-prop NO-GO (2026-07-10 already stood at run
> time and is stated in the banner above the panel — this diagnostic never overturned it) and
> the current c1 2-leg book (this is the superseded 3-leg Aegis+Striker+Striker-NAS100
> configuration). **Both** facts make the numbers below historical record, not a live gate.
>
> The numbers are **retained unedited as the historical record** of what was run on 2026-07-11.
> Do not cite them as current. Measurement of the defect's magnitude:
> [`../tradeify_eval_lock_correction_2026-07-22/RESULTS.md`](../tradeify_eval_lock_correction_2026-07-22/RESULTS.md) ·
> source-level fix: [`docs/adr/2026-08-04-firm-rules-eval-lock-fix-applied.md`](../../../../docs/adr/2026-08-04-firm-rules-eval-lock-fix-applied.md)

```
============================================================================================================
TRADEIFY SELECT FLEX remc — 3-leg FUTURES book (2026-07-11) — DIAGNOSTIC ONLY
Governance: R6 futures-prop NO-GO stands; this run does not overturn it.
Sims: 10,000 x 3 seeds | dd-protection OFF (C2-off) | inactivity DISABLED | horizon 1500d
Book: Aegis->6J (BEPAD-TEST) + DJ30->MYM + NAS->MNQ | no Guardian | risk 1.50%/0.70%/0.37%
Panel: decompounded static $200K via roe, scaled to locked risk via pin_r_basis(full_stop_mean)
Tier: Tradeify_Select_* (trailing_locking, Select DD column) | Gates: bust<1% AND p99 DD<5%
============================================================================================================

### PANEL  2020-01-06->2026-07-01  (1693 bdays)  book_net_scaled@200K=$162,333
  striker          N=267  init~$200,000  1R=$2,535.61 (full-stop mean (|loss| > 1% acct, n=8))  scale=0.5521  net=$37,181
                  file=Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-11_15d8b.csv
  striker_nas100   N=284  init~$200,000  1R=$5,899.32 (full-stop mean (|loss| > 1% acct, n=19))  scale=0.1254  net=$52,219
                  file=Striker_NAS100_v1_CME_MINI_MNQ1!_2026-07-11_beabf.csv
  aegis            N=152  init~$100,000  1R=$2,912.96 (full-stop mean (|loss| > 1% acct, n=11))  scale=1.0299  net=$72,934
                  file=Aegis_JPY-Futures_v0.3_BEPAD-TEST_(MJY_6J)_CME_6J1!_2026-07-11_ae744.csv

    Size   Config                                 Pass     Bust   p99 DD  Median  Gate
    ----------------------------------------------------------------------------------------------------
    25K    Tradeify (lock, geometry-only)       89.42%   10.58%    5.00%     106  FAIL (bust>=1% p99>=5%)
           bust_attr: striker=16.9%  nas=12.3%  aegis=70.8%  (trailing=10.58% horizon=0.00%)
    25K    Tradeify (lock, +40% consistency)    89.17%   10.83%    5.25%     126  FAIL (bust>=1% p99>=5%)

    50K    Tradeify (lock, geometry-only)       89.67%   10.33%    5.06%     106  FAIL (bust>=1% p99>=5%)
           bust_attr: striker=16.5%  nas=12.2%  aegis=71.2%  (trailing=10.33% horizon=0.00%)
    50K    Tradeify (lock, +40% consistency)    89.44%   10.56%    5.31%     126  FAIL (bust>=1% p99>=5%)

    100K   Tradeify (lock, geometry-only)       82.30%   17.70%    4.72%     100  FAIL (bust>=1% p99<5%)
           bust_attr: striker=17.4%  nas=11.8%  aegis=70.7%  (trailing=17.70% horizon=0.00%)
    100K   Tradeify (lock, +40% consistency)    82.12%   17.88%    5.15%     118  FAIL (bust>=1% p99>=5%)

    150K   Tradeify (lock, geometry-only)       82.39%   17.61%    4.75%     100  FAIL (bust>=1% p99<5%)
           bust_attr: striker=17.6%  nas=11.4%  aegis=71.1%  (trailing=17.61% horizon=0.00%)
    150K   Tradeify (lock, +40% consistency)    82.21%   17.79%    5.16%     120  FAIL (bust>=1% p99>=5%)

============================================================================================================
VERDICT vs FXIFY-inherited gates (bust<1% AND p99 DD<5%) — DIAGNOSTIC
============================================================================================================
  25K   Tradeify geom  pass=89.42% bust=10.58% p99=5.00% med=106d  -> FAIL
  50K   Tradeify geom  pass=89.67% bust=10.33% p99=5.06% med=106d  -> FAIL
  100K  Tradeify geom  pass=82.30% bust=17.70% p99=4.72% med=100d  -> FAIL
  150K  Tradeify geom  pass=82.39% bust=17.61% p99=4.75% med=100d  -> FAIL

CLEARS GATE: NO — no Tradeify Select tier clears both inherited gates

CONTEXT (not this panel — prior published numbers):
  Prior Tradeify 3-strat geom (2026-07-10, CFD hosts+6J prototype):
    25K bust 7.57%/p99 4.86% | 50K 7.40%/4.89% | 100K 13.37%/4.51% | 150K 13.29%/4.52%
  Locked CFD 4-strat FXIFY static anchor: 99.83% pass / 0.17% bust / p99 DD 4.37% / med 26d

REMAINING BLOCKERS (governance / edge — independent of this remc):
  * R6 futures-prop NO-GO (2026-07-10) — standing; this is diagnostic only
  * Aegis file is BEPAD-TEST, not of-record PROTOTYPE
  * P2 edge-preservation vs CFD still FALSIFIED (MYM absolute PF~2 does not overturn)
  * MNQ absolute PF does not overturn P2 KILL
  * Tradeify EOD force-flat is operational constraint (these exports: 0% overnight holds)
  * bust<1% gate is FXIFY one-shot economics; Tradeify cheap-retry may warrant different EV gate
```
