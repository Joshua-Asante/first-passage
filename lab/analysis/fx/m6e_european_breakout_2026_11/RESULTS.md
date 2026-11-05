# M6E European-morning breakout: fixed exploratory record

**Date:** 2026-11-04.
**Theme:** fx
**Status:** CLOSED — negative fixed-expression result preserved; independent code/evidence review clean; reserved returns untouched.

One operator-approved expression, K=1, was registered before outcomes. Reject this fixed expression under the stated cost/fill model: overall, both directions and every tested year were net-negative. No candidate was submitted to validation. This is an exploratory rejection, not a builder-gate verdict or a conclusion about every FX breakout or Tradeify account success.

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

[The frozen plan](../../../../docs/superpowers/plans/2026-11-04-m6e-fixed-exploration.md) owns the unchanged trading rules, the operator's $6.60 round-trip cost assumption and the prospectively fixed uncertainty method: 10,000 circular moving-block bootstrap replicates, 20 eligible-day blocks, seed 20261104, percentile 95% intervals. Daily outcomes include no-trade days; resamples divide total net by trade count. Intervals are conditional on the sample and fill model, not simultaneous or selection-adjusted.

Continuous-series bars cannot establish executable fills, spread/depth, expiry-specific roll identity, causal London order flow, independent confirmation or account pass probability. Direction/year splits were diagnostic, not separately selected strategies. MCL ORB R1 and the EIA audit are unchanged.

## Provenance and verification

- [Execution evidence](execution_evidence.json), [search trace](search_log.json), and [K ledger](../../../../discovery_manifests/m6e_european_breakout_fixed_20261104.json).
- Base `dba5b9424a74f77c9897192f5cd4ebc6280c8e4a`; branch `codex/m6e-fixed-exploration`. Source/test/plan hashes were pinned before outcomes. Python 3.13.2 ran through this checkout's fp launcher and the validated operations environment.
- `fp.ps1 python -m pytest lab/analysis/fx/m6e_european_breakout_2026_11/test_experiment.py -q`: 14 passed; `.cache/fp-verification/20261105T025656Z-64b549016fc9/record.json`, completed, exit 0, stable source.
- `fp.ps1 python -m pytest tests/test_archive_lab_analysis.py -q`: 100 passed; `.cache/fp-verification/20261105T032638Z-91d62b9dec9c/record.json`, completed, exit 0, stable source. The catalog fix adds the `fx` theme and a nested-study regression only.
- The single empirical command exited 0 with stable selected inputs and frozen sources. All 18 input hashes were rechecked. Arithmetic, costs, direction/year partitions and dates reconciled. The primary checkout's broad manifest check has 97 unrelated EXTRA files; targeted M6E hashes pass. Absent-tree skips here are not byte-integrity proof.
- Original execution and LF-normalized full-summary hashes remain in execution evidence. The public summary is now a deliberate count-only extract; it is not content-identical to the execution summary.

## Independent review — 2026-11-05

Claude reviewed checkpoint `3b236bbbc34254cd0b7ebfcb91f39a7f6b30a91f` from a bounded packet of code, tests, registration, aggregate results and provenance. Verdict: **clean, no blocking findings; the negative conclusion holds for this exact expression under its stated model.** The review traced the fixed rule, cost units/deduction, selected files, pre-decode year fence and bootstrap pairing. It was an independent code/evidence review, not a raw-data reproduction; Claude did not run the cited tests. The subsequent integration delta reconciles main's independently landed M6E ledger and adds this review record; it changes no experiment code, parameters, scored inputs or outcomes.

Non-blocking limits retained:

- The decoder was not separately listed in the prospective source hash table. It is unchanged from the recorded base (`055048b0c922dda763ffdcf3fb9eeb9b777ab739`, Git blob); its execution SHA-256 was recorded. No retrospective freeze is represented as prospective.
- Success flags in the execution record describe guards having passed, not independent operating-system file-access telemetry.
- Incomplete mornings are excluded before bootstrapping, so blocks can bridge gaps; zero-trade resamples are omitted. Intervals remain descriptive. Zero-volume bars would be accepted; the run reported none in its required windows.
- Continuous-series roll identity and executable spread/depth remain unresolved. The gross result provides no demonstrated cushion for costs; it is not proof of a statistically negative gross edge.

The author rechecked nine scored-file hashes (all match) and parsed equality of original versus LF registration/full-summary copies. The public summary is deliberately count-only; it is not merely a line-ending conversion. The 2025–2026 files were not reopened in this follow-up. Their metadata/hashes were inspected in the original structural audit; the fixed experiment neither decoded their prices nor computed their signals or returns.

Private review and verification records, indexed in `docs/evidence/PRIVATE_EVIDENCE.sha256`:
- `local_artifacts/m6e-fixed-20261104/review/claude-review-R1-summary.txt`, SHA-256 `b8cb7e1a694f020b63344961a26b4cc39be35f791064c7d33b1903cd01e1bb53`.
- `local_artifacts/m6e-fixed-20261104/review/provenance-check-20261105.json`, SHA-256 `c5d7b974e8a924d061d830cd22c69d80d5dc1d6a799c118b9e52317e12c8e0dc`.

Registry: [m6e_european_breakout_fixed_20261104](../../../../discovery_manifests/m6e_european_breakout_fixed_20261104.json), closed K=1, no candidate submitted. No new empirical look, tuning, reserved-sample use, MCL ORB R1 change or EIA work.

Integration verification: the same checkout launcher ran both affected test files together, with two workers: **114 passed**. Record `.cache/fp-verification/20261105T054532Z-8dcb1cfe6d58/record.json` is completed, exit 0, verification exit 0, source stable. The first attempt stopped before tests on Windows temporary-directory permissions (failed record in execution evidence); the identical check succeeded outside the sandbox. Main's canonical manifest is retained byte-for-byte, including all 18 registered M6E inputs.

CI follow-up, 2026-11-05: [the first full CI test run](https://github.com/Joshua-Asante/first-passage/actions/runs/41976397233) found one failure: the catalog generator recognized `fx` but the paired status checker did not. The existing equality regression reproduced locally (`.cache/fp-verification/20261105T055926Z-db2e08a070c1/record.json`, failed). The checker now recognizes the same theme; its regex/set consumers derive from that list. Both catalog/status test files plus the unchanged experiment tests passed together: **150 passed**, Python 3.13.2, record `.cache/fp-verification/20261105T060017Z-15ea4a6bebbc/record.json`, completed, exit 0, verification exit 0, source stable. The closed manifest's generic promotion wording was corrected to the actual rejection, explicitly identifying unused multiplicity defaults. This is integration/publication repair only; no new empirical look or change to frozen rules, registration or outcomes. Current-head CI and independent review are recorded on [PR #1088](https://github.com/Joshua-Asante/first-passage/pull/1088).
