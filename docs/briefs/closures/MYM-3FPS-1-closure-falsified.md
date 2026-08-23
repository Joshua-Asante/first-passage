# MYM-3FPS-1 closure — FALSIFIED

**Closed:** 2026-07-21
**Verdict:** `FALSIFIED at Phase-0`
**Pre-registration:** [`MYM-3FPS-1-verdict-preregistration.md`](../pre-registration/MYM-3FPS-1-verdict-preregistration.md), frozen at commit `9bf8002` before the pull and result.
**Results:** [`lab/archive/mym_3fps_recon_2026-07/RESULTS.md`](../../../lab/archive/mym_3fps_recon_2026-07/RESULTS.md)

## Gate return

| Gate | Threshold | Result | Verdict |
|---|---:|---:|---|
| Coverage | ≥90% | 84/87 = 96.6% | PASS |
| Overnight settlement spike | positive and `delta/sigma ≥ 0.2139` | +1.54 bp; `delta/sigma=0.0256`; power 0.042 | FAIL |
| Open-to-noon short reversal | positive and `delta/sigma ≥ 0.2139` | +2.68 bp; `delta/sigma=0.0500`; power 0.067 | FAIL |
| Tradeify cost law | reversal ≥6.57 bp | +2.68 bp | FAIL |

The native MYM cohort does not reproduce the published DJIA effect at useful magnitude. The point estimate is correctly signed, but it is approximately 2.5× below the 4× cost hurdle and about 4.3× below the required standardized effect. Year signs are unstable, with the tradable limb negative in 2019, 2024, 2025, and 2026.

## Disposition

- Close this exact MYM third-Friday 09:30→12:00 short.
- K=0 consumed; MYM family bank remains 0.
- No timing, quarterly-expiry, MNQ, overnight, or pooled rescue is licensed.
- Re-proposal requires new target-instrument mechanism evidence, not a window or expiry-subtype change.
- No Pine, rail, account, allocation, lifecycle, or live-trading change.

- **Registry:** rejected_candidates.md — ### Third-Friday derivative-settlement reversal on MYM
