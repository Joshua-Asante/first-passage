# M6E European-morning breakout: fixed exploratory record

**Date:** 2026-11-04.
**Theme:** fx
**Status:** CLOSED — one fixed exploratory run recorded; independent review pending; reserved returns untouched.

One operator-approved expression, K=1, was registered before outcomes. No candidate was submitted to validation. This local checkpoint is not independently reviewed acceptance, a builder-gate verdict, or evidence of Tradeify account success.

## Publication boundary

The current AGENTS.md derived-output rule keeps private-export performance figures private. It supersedes the frozen plan's broader publication wording without changing its prospective rules or hashes. The full report and aggregate results were preserved byte-for-byte in this worktree before preparing this count-only record:

- `local_artifacts/m6e-fixed-20261104/RESULTS.md`, SHA-256 `3fe0fc989633c86ce26f1445019c4b94edb0b1ae78d932a86e3d7516ec538525`.
- `local_artifacts/m6e-fixed-20261104/summary.json`, SHA-256 `d6867faf32dc7f8c78dc07b8c21bb6b6948e7f1dd1df7d9511cd6cec7125844b`.

These ignored files retain net results, uncertainty intervals, yearly/directional performance and geometry diagnostics. They are indexed in `docs/evidence/PRIVATE_EVIDENCE.sha256`. Publication changed; the original run and outcome did not. The frozen experiment, tests, plan, registration and K remain unchanged. No new return test ran during commit preparation.

## Sample and counts

The [registration](registration.json) pins 18 annual M6E1! M15 input files; exactly nine files, 2016–2024, were scored. Source files remain private under `core/data/tv_exports/cme/`; their hashes are also registered in that directory's `SHA256SUMS`.

The window was 2016-01-04 through 2024-12-31: 1,742 trades, comprising 910 long and 832 short trades. All 2025–2026 returns were excluded, conservatively protecting R2 D9's final approximately 378 sessions. No date-pinned M6E R2 split was found in the inspected owner. Earlier structural inspection covered metadata/coverage, not signals or returns.

| Year | Long trades | Short trades | Total trades |
|---|---:|---:|---:|
| 2016 | 95 | 98 | 193 |
| 2017 | 100 | 95 | 195 |
| 2018 | 103 | 83 | 186 |
| 2019 | 105 | 91 | 196 |
| 2020 | 98 | 95 | 193 |
| 2021 | 109 | 97 | 206 |
| 2022 | 110 | 89 | 199 |
| 2023 | 103 | 89 | 192 |
| 2024 | 87 | 95 | 182 |

Counts bind to the registration's input hashes and the full aggregate evidence hash above. [summary.json](summary.json) is a publication extract, not the original execution output.

## Rules and limits

[The frozen plan](../../../../docs/superpowers/plans/2026-11-04-m6e-fixed-exploration.md) owns the unchanged trading rules, the operator's $6.60 round-trip cost assumption and the prospectively fixed uncertainty method: 10,000 circular moving-block bootstrap replicates, 20 eligible-day blocks, seed 20261104, percentile 95% intervals. Daily outcomes include no-trade days; resamples divide total net by trade count. Intervals are conditional on the sample and fill model, not simultaneous, selection-adjusted or calibrated probabilities for the next 5–10 days.

Continuous-series bars cannot establish executable fills, spread/depth, expiry-specific roll identity, causal London order flow, independent confirmation or account pass probability. Direction/year splits were diagnostic, not separately selected strategies. MCL ORB R1 and the EIA audit are unchanged.

## Provenance and verification

- [Execution evidence](execution_evidence.json), [search trace](search_log.json), and [K ledger](../../../../discovery_manifests/m6e_european_breakout_fixed_20261104.json).
- Base `dba5b9424a74f77c9897192f5cd4ebc6280c8e4a`; branch `codex/m6e-fixed-exploration`. Source/test/plan hashes were pinned before outcomes. Python 3.13.2 ran through this checkout's fp launcher and the validated operations environment.
- `fp.ps1 python -m pytest lab/analysis/fx/m6e_european_breakout_2026_11/test_experiment.py -q`: 14 passed; `.cache/fp-verification/20261105T025656Z-64b549016fc9/record.json`, completed, exit 0, stable source.
- `fp.ps1 python -m pytest tests/test_archive_lab_analysis.py -q`: 100 passed; `.cache/fp-verification/20261105T032638Z-91d62b9dec9c/record.json`, completed, exit 0, stable source. The catalog fix adds the `fx` theme and a nested-study regression only.
- The single empirical command exited 0 with stable selected inputs and frozen sources. All 18 input hashes were rechecked. Arithmetic, costs, direction/year partitions and dates reconciled. The primary checkout's broad manifest check has 97 unrelated EXTRA files; targeted M6E hashes pass. Absent-tree skips here are not byte-integrity proof.
- Original execution and LF-normalized full-summary hashes remain in execution evidence. The public summary is now a deliberate count-only extract; it is not content-identical to the execution summary.

## Review and local checkpoint

Claude review did not complete: the CLI attempt failed authentication and no browser review was submitted. The operator then directed a local commit and notification to the Codex chat **Inspect market regime questions**. Independent review remains pending; this local checkpoint does not waive cross-agent review for subsequent acceptance or merge.

Commit-preparation budget: one publication correction, existing valid test evidence, normal local commit gates, zero new empirical looks or purchases.
