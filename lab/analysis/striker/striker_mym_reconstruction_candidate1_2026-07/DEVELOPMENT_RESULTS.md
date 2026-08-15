# S-MYM-ORC-02 development results

Development-only verdict: **FALSIFIED**

No reserved-holdout P&L was read or computed by this run.

## Step-0

- panel SHA256: `298ab8c8900f1144b450537f14e356681aec7448b4787ebc770de88c83f9059c`
- rows: 141471
- span: `2020-07-01T00:00:00Z` → `2026-07-02T00:00:00Z`

## Headline metrics

- completed base trades: 403
- gross expectancy: 0.047313 R
- net expectancy: -0.020966 R
- mean actual cost: 0.068279 R
- net profit factor: 0.951373
- max closed-equity drawdown: 6.624996%
- D5 ACF block size: 1
- D5 95% CI: [-0.12207470921977549, 0.0805699492231894]
- opening-anchor placebo p: 0.214379
- D3 gross/cost ratio: 0.692933

## Stability and concentration

- Year net expectancy R: {"2020": -0.0799202755075269, "2021": 0.060410255556336445, "2022": -0.04445616071625577, "2023": -0.03493027808051582}
- first-half net expectancy: -0.036698 R
- second-half net expectancy: -0.005157 R
- drop-top-five net expectancy: -0.067273 R

## Execution diagnostics

- maximum contracts: 34
- quantity-zero skips / signals / rate: 0 / 403 / 0.000000
- signals suppressed by scheduled force-flat: 0
- fills after scheduled force-flat: 0
- force-flat trades: 12
- seam-tagged trades: 0
- standard-session trades: 387
- allowlisted early-close trades: 16

## Frozen gates

- D0: PASS
- D1: PASS
- D2: FAIL
- D3: FAIL
- D4: FAIL
- D5: FAIL
- D6: FAIL
- D7: FAIL
- D8: FAIL
- D9: PASS

## Fingerprints

```json
{
  "actual_candidate_trials": "1",
  "candidate_offline_sha256": "a3e25d72845f08c3d8096b7c5be443d5503b4192115f8f3c2bc5d9234aa14acd",
  "k_reconstruction": "2",
  "panel_sha256": "298ab8c8900f1144b450537f14e356681aec7448b4787ebc770de88c83f9059c",
  "run_development_sha256": "896b03cd71ed89feff804581937ab4b49a3f617ea6bd71756055e5e56d8bfd82",
  "runspec_sha256": "a55a6b5d9eab85800a9cd33f25b6ae10410a4f0d19ad29985ec8bf9840843d0d",
  "session_calendar_sha256": "7ff65ef4b0bdceb620f077708e55075f5f4295ae6fd594a56595282e72a8a3bd"
}
```
