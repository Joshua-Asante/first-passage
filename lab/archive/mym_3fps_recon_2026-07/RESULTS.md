# MYM-3FPS-1 Phase-0 RESULTS

**Verdict: `FALSIFIED`**

## Frozen construct

Short MYM at 09:30 ET on each calendar third Friday; cover at 12:00 ET.
Native-micro panel: 2019-05-06 through 2026-07-21. K=0 delta extraction.

## Measurements

| Quantity | Value |
|---|---:|
| Event coverage | 84/87 (96.6%) |
| Overnight spike | +1.536 bp; sigma 59.929; delta/sigma 0.0256; power 0.042 |
| Open-to-noon short reversal | +2.676 bp; sigma 53.550; delta/sigma 0.0500; power 0.067 |
| Required delta/sigma | 0.2139 |
| Tradeify RT / 4x hurdle | 1.644 / 6.575 bp |
| MFFU RT / 4x hurdle | 1.690 / 6.761 bp |

## Gates

| Gate | Result |
|---|---|
| P0.0 coverage >= 90% | PASS |
| P0.1 positive, powered overnight spike | FAIL |
| P0.2 positive, powered open-to-noon reversal | FAIL |
| P0.3 reversal >= 4x Tradeify RT cost | FAIL |

## Disposition

`RESOLVED` licenses a separately frozen K-bearing confirmation campaign only.
`FALSIFIED` closes this construct without K spend. `AMBIGUOUS` means data
coverage failed and no return verdict is valid.
