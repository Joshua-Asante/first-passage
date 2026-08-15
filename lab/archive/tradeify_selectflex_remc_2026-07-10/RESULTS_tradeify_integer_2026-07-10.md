**Disposition:** FALSIFIED — Tradeify Select Flex integer-micro re-MC gates fail under costs

```
================================================================================================================
TRADEIFY SELECT FLEX — INTEGER-MICRO re-MC (2026-07-10)  [pessimistic-bound arm; C5 sizing model]
Sims: 10,000 x 3 seeds | dd-protection OFF | inactivity DISABLED | RESERVE cap policy | RT cost $2.22/ctr (PROXY)
1R pinned striker=$4,229 nas=$3,940 | Gates bust<1% AND p99 DD<5% | book: DJ30-MYM + NAS100-MNQ (2-strat)
================================================================================================================

    Size   Config                                       Pass     Bust   p99 DD  Median  Gate
    ----------------------------------------------------------------------------------------------------
    25K    Tradeify int (lock, +costs) [PRIMARY]      98.95%    1.05%    3.96%     152  FAIL (bust>=1% p99<5%)
    25K    Tradeify int (lock, +40% consistency)      98.94%    1.06%    4.05%     256  FAIL (bust>=1% p99<5%)
    25K    Tradeify int (lock, NO costs)              99.94%    0.06%    2.68%     131  PASS (bust<1% p99<5%)
    25K    Tradeify int matched (fixed-$, no lock)    99.92%    0.08%    4.07%     155  PASS (bust<1% p99<5%)
    25K    Bulenox int C5 xref (%-peak, Bx caps)      99.50%    0.50%    5.30%     136  FAIL (bust<1% p99>=5%)
           caps micro=20 | DJ base_int_cap=2 r_base=0.45 skip=0/191 | NAS base_int_cap=1 r_base=0.44 skip=71/163

    50K    Tradeify int (lock, +costs) [PRIMARY]      98.89%    1.11%    3.98%     137  FAIL (bust>=1% p99<5%)
    50K    Tradeify int (lock, +40% consistency)      98.89%    1.11%    4.08%     221  FAIL (bust>=1% p99<5%)
    50K    Tradeify int (lock, NO costs)              99.91%    0.09%    2.78%     117  PASS (bust<1% p99<5%)
    50K    Tradeify int matched (fixed-$, no lock)    99.67%    0.33%    4.11%     140  PASS (bust<1% p99<5%)
    50K    Bulenox int C5 xref (%-peak, Bx caps)      97.19%    2.81%    5.25%     107  FAIL (bust>=1% p99>=5%)
           caps micro=40 | DJ base_int_cap=4 r_base=0.45 skip=0/191 | NAS base_int_cap=3 r_base=0.73 skip=10/163

    100K   Tradeify int (lock, +costs) [PRIMARY]      95.41%    4.59%    3.50%     120  FAIL (bust>=1% p99<5%)
    100K   Tradeify int (lock, +40% consistency)      95.40%    4.60%    4.08%     211  FAIL (bust>=1% p99<5%)
    100K   Tradeify int (lock, NO costs)              99.20%    0.80%    2.99%     105  PASS (bust<1% p99<5%)
    100K   Tradeify int matched (fixed-$, no lock)    93.74%    6.26%    3.22%     117  FAIL (bust>=1% p99<5%)
    100K   Bulenox int C5 xref (%-peak, Bx caps)      87.58%   12.42%    3.53%      95  FAIL (bust>=1% p99<5%)
           caps micro=80 | DJ base_int_cap=9 r_base=0.50 skip=0/191 | NAS base_int_cap=7 r_base=0.86 skip=3/163

    150K   Tradeify int (lock, +costs) [PRIMARY]      94.98%    5.02%    3.56%     112  FAIL (bust>=1% p99<5%)
    150K   Tradeify int (lock, +40% consistency)      94.95%    5.05%    4.20%     205  FAIL (bust>=1% p99<5%)
    150K   Tradeify int (lock, NO costs)              99.08%    0.92%    3.01%     100  PASS (bust<1% p99<5%)
    150K   Tradeify int matched (fixed-$, no lock)    93.18%    6.82%    3.25%     111  FAIL (bust>=1% p99<5%)
    150K   Bulenox int C5 xref (%-peak, Bx caps)      91.24%    8.76%    3.40%     101  FAIL (bust>=1% p99<5%)
           caps micro=120 | DJ base_int_cap=14 r_base=0.52 skip=0/191 | NAS base_int_cap=10 r_base=0.90 skip=1/163

================================================================================================================
§4 (integer arm) — does the lock geometry bring any Tradeify tier within the gates?
================================================================================================================
  25K   Tradeify integer(+costs) bust 1.05% / p99 3.96% -> FAIL
  50K   Tradeify integer(+costs) bust 1.11% / p99 3.98% -> FAIL
  100K  Tradeify integer(+costs) bust 4.59% / p99 3.50% -> FAIL
  150K  Tradeify integer(+costs) bust 5.02% / p99 3.56% -> FAIL

VERDICT: NO tier passes both gates — integer arm confirms FALSIFIED, stricter than %-equity
```
