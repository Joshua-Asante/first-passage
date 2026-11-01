# Builder run R1, MCL two-sided opening-range breakout: committed registration

**Status:** `REGISTERED 2026-11-01`. Rule 23 requires this before any R1 card produces a result.

| Item | Value |
|---|---|
| Pre-registration | Builder R1 draft v3 (private): `local_artifacts/strategy-builder-2026-10/prereg-r1/PREREG-BUILDER-R1-DRAFT-v3.md`, sha256 `f82abc1c539a7321adf457098e7380c93a460df4ad2121245d8c14748cf56e8a` |
| Review log | `local_artifacts/strategy-builder-2026-10/prereg-r1/PREREG-BUILDER-R1-REVIEW-LOG-v1.md`, sha256 `07436ed9b33a7f55e62bc8b53ffb85e0e73ed24bffcd3c20f7338699787a3c7f`. Codex round 2: no blocking findings; two non-blocking findings carried |
| Freeze record | `local_artifacts/strategy-builder-2026-10/prereg-r1/PREREG-BUILDER-R1-FREEZE-v1.json`, sha256 `20eb461979bbd86926275f24f9be53c748615aa4887902e17d321b461b1a939a`. It pins the cards, book series, run spec and data |
| Run spec | `local_artifacts/strategy-builder-2026-10/prereg-r1/run-r1.yaml`, sha256 `8f41090d6153c080531f0d3cc35a04f36c6209b9fb322c79980c31e362025527` |
| Engine | [`lab/builder/`](../../../lab/builder/) at `a0d33b6` (PR #1004 plus `bbc4d24`); `gates.engine_version()` `a7d5375fba0522c039f63f1e09af4a432f43412ce5b4c8d31ad70b90bbfb450b` |
| Data | `core/data/tv_exports/cme/BAR_EXPORT_v0.2_NYMEX_MCL1_2026-08-13_3fd7c.csv`, pinned in its `SHA256SUMS` |
| K | 8 (the MCL count in R1's new ledger) |
| Authority | Joshua, 2026-11-01: "Yes, freeze MCL R1" |
| Hash index | All private files above are registered in [`docs/evidence/PRIVATE_EVIDENCE.sha256`](../../evidence/PRIVATE_EVIDENCE.sha256) |

**Engine check.** Before freezing, the coordinator compared the merged engine with the draft's gates, data split and book rules, and ran the engine's own parser and loaders on the pinned inputs. Card hashes, costs, the 812/348 development/holdout split and the 640-session book overlap all match the draft. No card outcome was read.

**Rule 26.** Rule 26 was amended on 2026-10-30, so earlier rejections are advisory. The draft's Rule 26 reasons for leaving M2K, MGC and MYM out of R1 are now disclosure only. R1's MCL-only scope rests on Joshua's ruling; M2K and MGC go to later rounds, each with its own registration and K.

**Binding.** Changing a criterion needs a new version, a new review and a new registration. The holdout is looked at once per survivor, before the MCL-1 pilot reads any MCL bar dated 2025-02-25 or later. A survivor goes to Joshua for the forward GO with gate 5h (venue MC) still outstanding.
