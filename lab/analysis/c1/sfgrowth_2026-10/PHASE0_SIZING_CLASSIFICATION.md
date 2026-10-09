# Q-SFGROWTH-1 Phase 0 — sizing-input classification (DRAFT, for review)

**Status:** DRAFT 2026-10-09. First step of [brief §7 Phase 0](../../../../docs/briefs/Q-SFGROWTH-1-self-funded-growth-portfolio-selection.md#7--execution-plan) under [pre-registration §B](../../../../docs/briefs/pre-registration/Q-SFGROWTH-1-verdict-preregistration.md#b--grid-exports-and-k). No export has been produced, read or scored. Exports wait for review of this table.

**Scope of this file:** identifiers, classes and Pine line references only. No Pine text, no input values, no account figures ([AGENTS.md private read surface](../../../../AGENTS.md#public-clone-posture)). Values for each (leg, k) export go in the private manifest under `private/` (gitignored here), which is written only after this review.

## Pins verified (primary checkout, 2026-10-09)

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

Only inputs on the size path or that read capital/equity are listed; every other input is **neither**.

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

Properties-panel margin, commission and slippage are **neither** for every leg. Default-quantity Properties are unused: every entry passes an explicit `qty`.

## Where reference values are read from (no values here)

| Leg | Reference export | Input and capital values |
|---|---|---|
| 1, 2, 3, 5 | 2026-09-03 exports pinned in `run_four_firm_remc.py` `SERIES_INPUTS` (normal) and `phase1_config.json` `strategies[3]` | pinned body defaults, overlaid by the chart-override snapshot `inputs/private_overrides/<strategy_id>.json` pinned by `phase1_config.json` `pine_input_overrides_sha256`; initial capital from that snapshot's `run.initial_capital` — **see C3** |
| 4 | `step6-admission/exports/O-N.csv` | `step6-admission/manifests/O-N.json` (`adapter_overrides.qty`, `emulator_overrides.initial_capital`), with captures `O-N-corrected-inputs.txt` and `O-N-corrected-properties.txt` in `op1/2026-09-14-seven/`; the manifest's Pine hash equals the book pin |

## Concerns for review

- **C1 — the leg 1 baseline maps to a cap, not a fixed count.** §A sets `Q_1 = 8` and §B gives leg 1 as `floor(k × 8)`. The 8 comes from `DEFAULT_QUANTITY_SPEC` and is applied after export by `rescale_per_contract`. The Aegis Pine instead sizes off `strategy.equity` and caps the result at `max_contracts`. The reference chart overrode `max_contracts`, and the recovered snapshot (C3) shows that override equals §A's baseline. So `floor(k × 8)` maps onto `max_contracts`. A size-k export still carries risk-sized quantities wherever the cap does not bind, and whether it binds on every trade can't be known without reading an export. If §A's "8 contracts" has to mean a fixed count, that needs a dated §E amendment from the operator.
- **C2 — leg 1's fixed-dollar rails: resolved as inert.** `trail_dd_usd` and `daily_loss_usd` fit neither class, and they gate entries only when `backtestMode` is off. The recovered snapshot has no chart override of `backtestMode`, so it sits at the body default, under which the rails never gate (`canTrade`, line 637). Hold it at the reference value in every export.
- **C3 — reference snapshots.** Leg 1's snapshot (`aegis_6j1.json`, `460f40fa…`) was restored to `inputs/private_overrides/` on 2026-10-09 from the 2026-09-24 recovery copy, and its hash was verified. The snapshots for legs 2, 3 and 5 are in neither `first-passage-archive` (all branches and the `evidence/sha256` store) nor the recovery set. That matches the [2026-09-24 recovery record](../../../../docs/briefs/handoffs/2026-09-24-seven-strategy-evidence-recovery.md), which recovered 1 of 5. Their reference values can't be distinguished from body defaults, and §D26 shows that chart overrides were load-bearing on both Strikers. Before exports, the operator needs to choose a reference for these legs.
- **C4 — equity-sized legs 1 and 3.** For these legs the initial capital is the account-size lever, through `strategy.equity`, so §B's capital rule already scales their size. Their contract caps scale as contract-count. Confirm that this reading of "every sizing input" is intended.
- **C5 — leg 5 body vs export body.** The pinned candidate (`d18c2699…`) differs from the body that produced the reference export (`fa6a70cd…`) only in its `strategy()` initial-capital default ([D15](../../../../docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md)). The classification is unaffected, and the reference capital comes from the export's Properties.
- **C6 — floors at small k.** `floor(k × ref)` on a cap or a count can reach 0. Per §B, a leg with no trades at that k contributes nothing. The adds in legs 3 and 4 use `max(1, round(…))` and do not scale proportionally. That is locked behavior, and the size-specific exports capture it.
