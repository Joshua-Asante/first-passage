```
============================================================================================================
TRADEIFY SELECT FLEX re-MC (2026-07-10) — barrier-geometry test vs Bulenox
Sims: 10,000 x 3 seeds | dd-protection OFF (C2-off) | inactivity DISABLED | horizon 1500d
1R pinned: striker=$4,229 nas100=$3,940 aegis(6J)=$1,385.74 | Gates: bust<1% AND p99 DD<5%
============================================================================================================

### BOOK: 2-strat (DJ30+NAS100, canonical Bulenox book)   (2 legs: striker, striker_nas100)
    panel: 2022-01-04 -> 2026-04-17  (1119 bdays)

    Size   Config                                 Pass     Bust   p99 DD  Median  Gate
    ------------------------------------------------------------------------------------------------
    25K    Tradeify (lock, geometry-only)       96.91%    3.09%    4.29%      71  FAIL (bust>=1% p99<5%)
    25K    Tradeify (lock, +40% consistency)    96.83%    3.17%    4.90%     162  FAIL (bust>=1% p99<5%)
    25K    Bulenox matched (fixed-$, no lock)   99.55%    0.45%    5.13%      72  FAIL (bust<1% p99>=5%)
    25K    Bulenox shipped (%-of-peak, C4 xref)   99.60%    0.40%    5.13%      72  FAIL (bust<1% p99>=5%)

    50K    Tradeify (lock, geometry-only)       96.97%    3.03%    4.31%      71  FAIL (bust>=1% p99<5%)
    50K    Tradeify (lock, +40% consistency)    96.92%    3.08%    4.92%     162  FAIL (bust>=1% p99<5%)
    50K    Bulenox matched (fixed-$, no lock)   98.71%    1.29%    4.95%      72  FAIL (bust>=1% p99<5%)
    50K    Bulenox shipped (%-of-peak, C4 xref)   98.87%    1.13%    5.03%      72  FAIL (bust>=1% p99>=5%)

    100K   Tradeify (lock, geometry-only)       92.96%    7.04%    3.90%      67  FAIL (bust>=1% p99<5%)
    100K   Tradeify (lock, +40% consistency)    92.91%    7.09%    4.85%     157  FAIL (bust>=1% p99<5%)
    100K   Bulenox matched (fixed-$, no lock)   90.89%    9.11%    3.51%      67  FAIL (bust>=1% p99<5%)
    100K   Bulenox shipped (%-of-peak, C4 xref)   91.46%    8.54%    3.55%      67  FAIL (bust>=1% p99<5%)

    150K   Tradeify (lock, geometry-only)       92.99%    7.01%    3.90%      67  FAIL (bust>=1% p99<5%)
    150K   Tradeify (lock, +40% consistency)    92.94%    7.06%    4.85%     157  FAIL (bust>=1% p99<5%)
    150K   Bulenox matched (fixed-$, no lock)   90.89%    9.11%    3.51%      67  FAIL (bust>=1% p99<5%)
    150K   Bulenox shipped (%-of-peak, C4 xref)   91.46%    8.54%    3.55%      67  FAIL (bust>=1% p99<5%)


### BOOK: 3-strat (+ Aegis/6J, PROVISIONAL)   (3 legs: striker, striker_nas100, aegis)
    panel: 2022-01-04 -> 2026-07-01  (1172 bdays)

    Size   Config                                 Pass     Bust   p99 DD  Median  Gate
    ------------------------------------------------------------------------------------------------
    25K    Tradeify (lock, geometry-only)       92.43%    7.57%    4.86%      46  FAIL (bust>=1% p99<5%)
    25K    Tradeify (lock, +40% consistency)    92.15%    7.85%    5.80%      91  FAIL (bust>=1% p99>=5%)
    25K    Bulenox matched (fixed-$, no lock)   98.13%    1.87%    6.11%      48  FAIL (bust>=1% p99>=5%)
    25K    Bulenox shipped (%-of-peak, C4 xref)   98.29%    1.71%    6.18%      48  FAIL (bust>=1% p99>=5%)

    50K    Tradeify (lock, geometry-only)       92.60%    7.40%    4.89%      46  FAIL (bust>=1% p99<5%)
    50K    Tradeify (lock, +40% consistency)    92.36%    7.64%    5.84%      91  FAIL (bust>=1% p99>=5%)
    50K    Bulenox matched (fixed-$, no lock)   95.86%    4.14%    5.38%      47  FAIL (bust>=1% p99>=5%)
    50K    Bulenox shipped (%-of-peak, C4 xref)   96.26%    3.74%    5.46%      47  FAIL (bust>=1% p99>=5%)

    100K   Tradeify (lock, geometry-only)       86.63%   13.37%    4.51%      43  FAIL (bust>=1% p99<5%)
    100K   Tradeify (lock, +40% consistency)    86.42%   13.58%    5.79%      86  FAIL (bust>=1% p99>=5%)
    100K   Bulenox matched (fixed-$, no lock)   82.94%   17.06%    4.00%      42  FAIL (bust>=1% p99<5%)
    100K   Bulenox shipped (%-of-peak, C4 xref)   83.79%   16.21%    4.02%      42  FAIL (bust>=1% p99<5%)

    150K   Tradeify (lock, geometry-only)       86.71%   13.29%    4.52%      43  FAIL (bust>=1% p99<5%)
    150K   Tradeify (lock, +40% consistency)    86.51%   13.49%    5.79%      86  FAIL (bust>=1% p99>=5%)
    150K   Bulenox matched (fixed-$, no lock)   82.94%   17.06%    4.00%      42  FAIL (bust>=1% p99<5%)
    150K   Bulenox shipped (%-of-peak, C4 xref)   83.79%   16.21%    4.02%      42  FAIL (bust>=1% p99<5%)

============================================================================================================
§4 VERDICT — does the lock geometry move >=1 size within the gates that Bulenox failed?
============================================================================================================

2-strat (DJ30+NAS100, canonical Bulenox book):
  25K   Tradeify bust 3.09%/p99 4.29% -> FAIL   |  Bulenox-matched bust 0.45%/p99 5.13% -> FAIL
  50K   Tradeify bust 3.03%/p99 4.31% -> FAIL   |  Bulenox-matched bust 1.29%/p99 4.95% -> FAIL
  100K  Tradeify bust 7.04%/p99 3.90% -> FAIL   |  Bulenox-matched bust 9.11%/p99 3.51% -> FAIL
  150K  Tradeify bust 7.01%/p99 3.90% -> FAIL   |  Bulenox-matched bust 9.11%/p99 3.51% -> FAIL

3-strat (+ Aegis/6J, PROVISIONAL):
  25K   Tradeify bust 7.57%/p99 4.86% -> FAIL   |  Bulenox-matched bust 1.87%/p99 6.11% -> FAIL
  50K   Tradeify bust 7.40%/p99 4.89% -> FAIL   |  Bulenox-matched bust 4.14%/p99 5.38% -> FAIL
  100K  Tradeify bust 13.37%/p99 4.51% -> FAIL   |  Bulenox-matched bust 17.06%/p99 4.00% -> FAIL
  150K  Tradeify bust 13.29%/p99 4.52% -> FAIL   |  Bulenox-matched bust 17.06%/p99 4.00% -> FAIL
```
