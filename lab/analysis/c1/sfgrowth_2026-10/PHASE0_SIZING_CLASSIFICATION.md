# Q-SFGROWTH-1 Phase 0 — sizing-input classification (DRAFT, for review)

**Status:** DRAFT 2026-10-09. First step of [brief §7 Phase 0](../../../../docs/briefs/Q-SFGROWTH-1-self-funded-growth-portfolio-selection.md#7--execution-plan) under [pre-registration §B](../../../../docs/briefs/pre-registration/Q-SFGROWTH-1-verdict-preregistration.md#b--grid-exports-and-k). No export has been produced, read or scored. Export readiness is HOLD; see the input-range check and approved rulings and pending amended freeze below.

**Scope of this file:** identifiers, classes, source references, hashes and sanitized findings. No Pine text, no input values, no account figures ([AGENTS.md private read surface](../../../../AGENTS.md#public-clone-posture)). Values for each (leg, k) export go in the private manifest under `private/` (gitignored here), which is written only after this review. The committed private identity and public repository/commit/path/digest binding are mandatory under [preregistration F6](../../../../docs/briefs/pre-registration/Q-SFGROWTH-1-verdict-preregistration.md#f6---committed-private-manifest-identity); an ignored local copy alone cannot admit scoring.

## Pins verified (primary checkout, 2026-10-09; rechecked 2026-10-10)

| # | Leg | Pine (primary checkout) | Pin source | SHA-256 match |
|---|---|---|---|---|
| 1 | Aegis 6J | `core/strategies/book/aegis_6J1_venue_bound.pine` | `BOOK_SOURCES.sha256` (`db78ecba…`) | yes |
| 2 | Striker DJ30 MYM p250 | `core/strategies/book/striker_dj30_v4.5_mym_pyramid_250_cap100k.pine` | `BOOK_SOURCES.sha256` (`712cf395…`) | yes |
| 3 | Vanguard Gold MGC v0.4 | `core/strategies/book/Vanguard_Gold_MGC_v0.4_venue_bound.pine` | `BOOK_SOURCES.sha256` (`af26899c…`) | yes |
| 4 | ORB MNQ v7 recon | `core/strategies/book/orb_mnq_7_reconstruction_venue_bound.pine` | `BOOK_SOURCES.sha256` (`176c4f70…`) | yes |
| 5 | Striker NAS100 MNQ, DOW-excl. | `core/strategies/candidates/striker_nas100_v1_mnq_dow_wed_excluded.pine` | `phase1_config.json` `strategies[3].pin_ref` → `PORT_MANIFEST.sha256` (`d18c2699…`) | yes |

## Classes

- **contract-count**: export value `floor(k × reference)`.
- **account-size**: input used only to compute size; export value `k × reference`, unrounded.
- **capital**: the Properties-panel initial capital; `k × reference` for every leg (§B). Marked separately where it also sets size through `strategy.equity`.
- **neither**: held at the reference export's value.

Inputs on the size path, capital/equity reads, and the leg-5 lineage-sensitive weekdays are listed; every other input is **neither**.

## Table

| Leg | Identifier | Class | Pine line(s) | Role |
|---|---|---|---|---|
| 1 | Properties initial capital | capital (**sets size**) | 3; read 539, 551, 561–582 | `strategy.equity × risk_pct` sets the risk budget per trade |
| 1 | `max_contracts` | contract-count | 281; used 545 | cap on the risk-sized quantity |
| 1 | `risk_pct` | neither | 271; used 539 | ratio |
| 1 | `sizing_mode`, `quote_conv`, `use_symbol_pv`, `manual_pv` | neither | 276, 247, 252, 256; used 538–548 | mode and point-value selection |
| 1 | `trail_dd_usd`, `daily_loss_usd` | neither — **see C2** | 292, 306; used 580–585, gate 637 | fixed-dollar rails vs equity; gate entries only when `backtestMode` is off |
| 1 | `cap_floor_at_start`, `dd_basis`, `backtestMode` | neither | 302, 297, 227; used 561–589, 637 | rail switches; floor anchored to initial capital |
| 2 | `accountSize` | account-size | 58; used 189 (`calcSize` 188–193) | risk budget per trade |
| 2 | `microCap` | contract-count | 59; used 192 | cap on base quantity, reserved for the add |
| 2 | `riskPerTrade`, `pyramidSize`, `mymPointValue` | neither | 44, 126, 60; used 189–192, 340 | ratios / instrument constant |
| 2 | Properties initial capital | capital | 11; read 198–205, 231 | day soft-stop (231) and `ddHit` (205) are % of initial capital |
| 2 | `strikerDayStopPct`, `maxDailyDD`, `maxTotalDD`, `backtestMode` | neither | 51, 46, 48, 34 | percentages; `backtestMode` gates `ddHit` only |
| 3 | Properties initial capital | capital (**sets size**) | 3; read 374–379, 419 | `strategy.equity × riskPerTrade` sets the risk budget (`calcSize` 418–422) |
| 3 | `maxContracts` | contract-count | 157; used 443, 422 | cap on the risk-sized quantity |
| 3 | `riskPerTrade`, `regimeWeakRiskMult`, `regimeStrongRiskMult`, `regimeWeakCapMult`, `regimeStrongCapMult`, `useRegimeSizing`, `useStreakFade`, `streakFadeFloor`, `streakFadeFullDays` | neither | 151, 260, 262, 256, 258, 250, 217, 223, 221; used 324, 443–445 | ratios and switches |
| 3 | `scaleInQtyPct`, `maxScaleIns`, `useScaleIn` | neither | 246, 244, 242; used 489 | add = `max(1, round(base × pct))` |
| 3 | `maxDailyDD`, `maxTotalDD`, `backtestMode` | neither | 153, 154; used 378–395 | % of day-start equity / initial capital |
| 4 | `qty` | contract-count | 67; used 179, 234, 237 | fixed contracts per entry |
| 4 | `scaleInQtyPct`, `maxScaleIns`, `useScaleIn` | neither | 114, 112, 110; used 179, 265–269 | add = `max(1, round(qty × pct))` |
| 4 | Properties initial capital | capital | 32 | no read of `strategy.equity`, `netprofit` or initial capital in the body |
| 5 | `accountSize` | account-size | 88; used 238 (`calcSize` 237–242) | risk budget per trade |
| 5 | `microCap` | contract-count | 89; used 241 | cap on base quantity, reserved for the add |
| 5 | `riskPerTrade`, `pyramidSize`, `mnqPointValue` | neither | 72, 163, 90; used 238–241, 390 | ratios / instrument constant |
| 5 | Properties initial capital | capital | 3; read 247–254, 281 | day soft-stop (281) and `ddHit` (254) are % of initial capital |
| 5 | `strikerDayStopPct`, `maxDailyDD`, `maxTotalDD`, `backtestMode` | neither | 80, 74, 76, 62 | percentages; `backtestMode` gates `ddHit` only |
| 5 | `allowMon`, `allowTue`, `allowWed`, `allowThu`, `allowFri` | neither | 184-188 (candidate pin) | preserve the reference schedule; distinguish the admitted candidate from its older locked ancestor (C5) |

Properties-panel margin, commission and slippage are **neither** for every leg. Default-quantity Properties are unused: every entry passes an explicit `qty`.

## Where reference values are read from (no values here)

| Leg | Reference export | Input and capital values |
|---|---|---|
| 1 | Normal reference in `run_four_firm_remc.py` `SERIES_INPUTS` | Pinned body plus recovered original snapshot `P/aegis_6j1.json`; capital from `run.initial_capital`. C3 defines `P` and the exact archive retrieval. |
| 2, 3, 5 | Normal references in `run_four_firm_remc.py` `SERIES_INPUTS`; leg 5 at `phase1_config.json` `strategies[3]` | Reference body state plus the separately identified October recaptures (C3); captured input values in `inputs`, capital in `properties.initial_capital`. These are not the original pinned snapshots. For leg 5, preserve the weekday state verified in C5. |
| 4 | `step6-admission/exports/O-N.csv` | `step6-admission/manifests/O-N.json` (`adapter_overrides.qty`, `emulator_overrides.initial_capital`), with captures `O-N-corrected-inputs.txt` and `O-N-corrected-properties.txt` in `op1/2026-09-14-seven/`; the manifest's Pine hash equals the book pin |

## Concerns and disposition (2026-10-10 correction)

- **C1 - the leg 1 baseline maps to a cap, not a fixed count; ruling approved; amended freeze pending.** The frozen baseline maps to `max_contracts`; the recovered chart override agrees with that baseline. The Pine still sizes from equity and caps the resulting quantity. Neither the matching baseline nor scaling capital proves that the cap binds on every trade. Keep the baseline fixed as specified in §B; do not replace it with a newly chosen snapshot value. Joshua approved the cap interpretation; record it under the reviewed amendment before exports.
- **C2 - leg 1's fixed-dollar rails: resolved as inert.** The recovered snapshot does not override `backtestMode`; at the pinned default, `trail_dd_usd` and `daily_loss_usd` do not gate entries (`canTrade`, line 637). Preserve the reference switch; do not change the rails to solve sizing.
- **C3 - original pins and recaptures are different evidence.** The original Aegis snapshot is restored and hash-verified. The original snapshots for legs 2, 3 and 5 have not been recovered by this audit. Their October transcriptions have distinct hashes, with operator-attested historical chart identity under [campaign §52](../../../../docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#52--completed-capture-intake-and-export-provenance-2026-09-05), not independent reproduction or original-byte identity. Retrieval and coverage are recorded below. Vanguard's transcription still has two unpopulated display controls. Their historical values remain unknown; Joshua approved only those two cosmetic controls' exemption from exact reference reproduction (section F). Do not claim their values were recovered. Do not overwrite the original `pine_input_overrides_sha256` pins with transcription hashes.
- **C4 - capital is also the size lever for legs 1 and 3.** The pinned source reads `strategy.equity` in the size calculation. §B already scales Properties initial capital for every leg and separately floors contract caps. Applying those two rules, holding risk ratios and other inputs at reference, is the existing mapping; no extra risk-percentage multiplier is warranted. This does not promise exactly proportional quantities as equity evolves. C1's cap interpretation is now approved, pending the amended freeze.
- **C5 - leg 5 requires a three-source distinction.** `phase1_config.json` `lineage_notes` / `pin_divergence` compare the reference (`fa6a70cd…`) with the older locked ancestor (`bb921399…`): `allowThu` and `allowFri` differ, as well as the capital basis described there. The admitted candidate (`d18c2699…`) already carries those weekday defaults. Local comparison of the hash-verified candidate and recovered reference found only initial-capital and comment-line differences; their weekday inputs agree. The recovered reference is `local_artifacts/recovery-2026-09-24/surviving-inputs/striker_nas100_v1_mnq_dow_wed_excluded_cap100k.pine` in the primary checkout. The October recapture and its weekday screenshot also agree with the reference. Thus “no overrides” is relative to the admitted candidate, never permission to use the ancestor's schedule. Preserve all five weekday inputs at the reference state for every multiplier; no Pine edit is needed.
- **C6 - a zero floor is not an executable TradingView configuration; disabled-leg ruling approved; amended freeze pending.** The contract-count range audit below finds both ORB and Vanguard inputs below their declared minimum at positive multipliers. The existing sentence about a leg ending with no trades applies to a valid export, not an invalid input. Do not clamp to the minimum, change another switch, omit a required export, or manufacture an empty export. Size-specific exports retain locked add behavior only for admissible inputs. The approved typed-artifact amendment must be reviewed and re-frozen before exports.

- **C7 - Striker MYM native-guard conflict: unresolved.** Its captured trading setting activates the pinned daily/total drawdown guard, which blocks entries and closes positions. Preserving that setting under §B conflicts with §A's protection-free wording. [Preregistration F7](../../../../docs/briefs/pre-registration/Q-SFGROWTH-1-verdict-preregistration.md#f7---native-drawdown-guard-conflict-unresolved-before-re-freeze) owns the required new ruling. The table is a source classification, not authorization to export this inconsistent mode; do not flip the switch or assume the guard is inert. Re-freeze, exports and scoring remain held.

## Reference evidence reconciliation

Paths in this section are relative to the primary checkout. `P` means
`lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/inputs/private_overrides/`.
The original digests remain owned by `phase1_config.json`. The recapture/admission
paths below identify provisional local evidence, not replacements for those
originals. Their new public pins and registry entries are deferred until scoped
archive authorization, preservation and verified retrieval are complete (M-41).
The exact path/digest inventory stays local; none is admitted merely by this table.

| Leg | Original snapshot pin prefix | Current retrievable evidence | Coverage / binding |
|---|---|---|---|
| 1 | `460f40fa…` | `P/aegis_6j1.json`; also private `first-passage-archive` commit `28eb2c7d3545558ceceb27e16b7be17a0bbdd1e7`, path `evidence/sha256/46/460f40fa079c00a97711d743aa0a5acee62f1c8f2cc33972b8a92b7948e42d08` | Local file and archive blob both match the original digest. |
| 2 | `b7369ee3…` | `P/recaptured-2026-10-09/striker_dj30_mym_pyramid_250.json` (provisional local evidence; public pin deferred) | 31/31 captured; `backtestMode` differs from the admitted body default. Historical binding is §52's attestation. |
| 3 | `3bacd6f1…` | `P/recaptured-2026-10-09/vanguard_mgc_v04.json` (provisional local evidence; public pin deferred) | 57/59 captured; `showEmas` and `showDashboard` have no captured values. No differences among the checked scalar defaults. Approved cosmetic exemption: mark both historical values unknown; do not fill from defaults by inference. |
| 4 | separate O-N admission | `P/op1/2026-09-14-seven/step6-admission/manifests/O-N.json` (provisional local evidence; public pin deferred) | The referenced corrected Inputs and Properties text hashes match; its Pine hash matches the book. The historical Phase-1 ORB snapshot is not this reference. |
| 5 | `ba59219a…` | `P/recaptured-2026-10-09/striker_nas100_mnq_dow_wed_excluded.json` (provisional local evidence; public pin deferred) | 36/36 captured; no differences among checked scalar defaults of the admitted candidate. Weekday comparison independently checked against the reference body and screenshot (C5). |

All 19 screenshot files named by the three recaptures were located and hashed.
The decisive NAS100 weekday capture is `Screenshot 2026-09-04 190624.png`; its
actual absolute source path and digest are retained in the local inventory. It
lives outside this repository today. Before a future public registry entry, stage
an authorized copy under an ignored primary-checkout evidence directory and use
only its real repo-relative path; descriptive annotations belong in comments.
No annotated filename or unarchived new digest is registered by this amendment.
Hashes and scalar-default comparisons do not independently validate every screenshot
transcription. §52 expressly records no fresh re-export and limits its attestation
to the historical intake. A reviewed Phase-0 private manifest must retain that
provenance and the recapture identities, with complete reference values; it must
not claim a new hash match to a lost original or a reproduced historical export.

## Input-range check (no exports)

The five contract-count inputs were checked against their pinned input bounds at
every positive frozen multiplier, using the recovered reference values. The two
Striker `accountSize` inputs also admit every mapped value. These are static
input-range results, not TradingView execution or performance results.

| Leg / input | Positive multipliers below the declared minimum | Disposition |
|---|---|---|
| 1 / `max_contracts` | none | Declared bounds admit the mapped values; Cap ruling approved; re-freeze pending. |
| 2 / `microCap` | none | Declared bounds admit the mapped values. |
| 3 / `maxContracts` (line 157) | `1/8`, `1/4` | Floor is zero; input excludes zero. Typed-artifact contract review/re-freeze required. |
| 4 / `qty` (line 67) | `1/8`, `1/4`, `1/2` | Floor is zero; input excludes zero. Typed-artifact contract review/re-freeze required. |
| 5 / `microCap` | none | Declared bounds admit the mapped values. |

## Approved rulings and export readiness (2026-10-10)

Joshua approved all three scoped rulings at approximately 20:20 UTC, message
`Sentinel_7915fcd79e948191a0248d3bc3fe0b3d`: Aegis retains equity-risk sizing with
the frozen contract cap; the five inadmissible ORB/Vanguard rows become typed
disabled-leg cases; and only Vanguard `showEmas` / `showDashboard` are exempted
from exact historical reproduction, with their historical values marked unknown.
The unchanged transcript remains in the private local handoff.

The exact schema, scorer treatment, provenance exception and validation design
are owned by [preregistration section F](../../../../docs/briefs/pre-registration/Q-SFGROWTH-1-verdict-preregistration.md#f---phase-0-amendment-approved-scope-pending-contract-review-and-re-freeze).
The rulings settle the three choices; the prepared technical contract still needs
the existing selection owner's review and an amended freeze. These are semantic
amendments, not a claim that the current Pine can execute an inadmissible input.

**Readiness: HOLD before exports.** Next, the existing #752/selection owner
reconciles and reviews this patch against their current branch, then records the
amended freeze. The old freeze identifier is not approval of the new schema.
Scorer implementation waits for reconciled ownership and that freeze. Thereafter
the existing Phase-0 manifest/source gates and synthetic scorer verification/review
remain prerequisites to real scoring. No structural-zero artifact was generated.
The nominal grid, K, exclusions, tie-breaks and growth/drawdown objective are
unchanged; the portfolio remains unselected.
