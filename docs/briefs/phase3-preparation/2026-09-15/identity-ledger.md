# Phase 3 preparation identity ledger — 2026-09-15

Status: PREPARATION ONLY. This read-only byte audit records accepted historical evidence; it neither freezes F1 nor accepts Phase 2, actual close, full-book parity, qualification or activation. No replay was executed.

Private references below are relative to the ignored primary evidence root: `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/inputs/private_overrides/op1/2026-09-14-seven/`. Runtime and calendar references are relative to the isolated Phase 3 worktree at `c86a0a0a17b433e690b700914662868c0d5f7ece`. No private source, market data, settings values or account values are copied.

## Admission and Step 3 records

| Relative artifact | SHA-256 (fresh byte hash) |
|---|---|
| `step6-admission/phase1-accepted/accepted-run.json` | `8ddf727b38b3044ad2c0e8cb05330933f94b9fb8c9f21be38dbeff41d7ad75e0` |
| `step6-admission/phase1-accepted/admission-contract.json` | `4f027af56f18c119c18b24f6f867ecb0a64188085ea7a8a95c18b0a77d0e9dde` |
| `step6-admission/phase1-accepted/independent-review.json` | `dd9c5e7296535a934b973df7ec0ff8b87c6c3554fc092822820f633588654cfd` |
| `step6-admission/phase1-accepted/run.py` | `2ea9e16911214ebac0eaba840b6aab90b784cf2623d937ce91be91261053ff2b` |
| `step3-coverage/step3-evidence-admission-contract.json` | `acfa7920fe025443dd321057f4e1c192d8bc7ccbabd66c94bb25bef6233b6e6d` |
| `step3-coverage/step3-evidence-index-v4.json` | `95ac6dcb18c37a2e5809c567cd1795f86fc324b21690b45108501505f06e7538` |
| `step3-coverage/step3-independent-acceptance.json` | `ebcb2efb73042d2e86f46db146246a6a84ff04230b37a47f77d5951994c14f1e` |

## Seven admitted manifests and bound artifacts

All rows below were hashed afresh and match their manifest or formal contract pin. Port/panel/export triples also match the accepted Step 3 contract. The coverage artifact is the older retained initializer reference; the separate independent review and accepted Step 3 records supply the supplementary binding. Warmup is `cold_at_panel_origin`, first bar `2022-09-01T00:00:00+00:00`, coverage verdict PASS for every bundle. No arbitrary warm restart is certified.

| Bundle | Artifact kind | Relative artifact | SHA-256 |
|---|---|---|---|
| O-N | manifest | `step6-admission/manifests/O-N.json` | `945b7aa54d24046940380bc4df7e5ee2d99937c182a4b2ba4a7c44287ad3adbb` |
| O-N | pine | `step6-admission/pine/orb_mnq_7_reconstruction_venue_bound.pine` | `176c4f70c67d58053c4d3b8170d0a9be3733bc6b76b1e2f928bd7a877be052a3` |
| O-N | port | `step3-coverage/corrected-ports/orb_mnq_v7.py` | `b1f4e573009e62b976013e08e7ef2784497d840f490f04e3878fdaef553f317d` |
| O-N | csv | `step6-admission/exports/O-N.csv` | `8e4902c3ee6224f57e29c8e1e0491c5c70695978d38036cfdc380eaded15e861` |
| O-N | inputs | `O-N-corrected-inputs.txt` | `0d84a1f5cd7cfb3a269a3734e2eaf4f8c37a4314a9a42a6b7dcdd54c51c32f28` |
| O-N | properties | `O-N-corrected-properties.txt` | `f1837364564f32fad8f4a6de050ad9741e6ed2bb5eb4f6000c355f6b47a8f827` |
| O-N | panel | `step6-admission/panels/MNQ_M15.csv` | `cceaac41a9b5029676cbc36f4d2be7e975723a7aa00610e86f63d7980eb27fc8` |
| O-N | margin | `step6-admission/margin/O-N-margin.json` | `81097bcfa615268a2058531ea56a584fb32f5fc2a0993427bf19eae23dec4310` |
| O-N | attestation | `packet1-source-history-attestation.json` | `7c58510aeb8fe924798e54c464f9daea92b042ea6f65508af092252a6d0a568f` |
| O-N | normalization | `packet1-normalization-diagnostic.json` | `10680786b54622106956354b9f3e03020b7c18f7b1cfe9c1773f5f908e7c2246` |
| O-N | reconciliation | `step2-orb/seven-summary-reconciliation.json` | `e3883d1fcf57a442da748f4ba5da569d644699d82e8b1b1b4fd7568b1ff2cff9` |
| O-N | coverage | `step3-coverage/full-initialization-and-interval.json` | `c1aa67c0fd93d62b423918493b16996cc507aab9de993b47e9c6fcb484eb7da8` |
| O-P | manifest | `step6-admission/manifests/O-P.json` | `abf5b1530f0324259ba962a93535c3f143a610fbef4114107e47ed9b6f6396d9` |
| O-P | pine | `step6-admission/pine/orb_mnq_7_reconstruction_venue_bound.pine` | `176c4f70c67d58053c4d3b8170d0a9be3733bc6b76b1e2f928bd7a877be052a3` |
| O-P | port | `step3-coverage/corrected-ports/orb_mnq_v7.py` | `b1f4e573009e62b976013e08e7ef2784497d840f490f04e3878fdaef553f317d` |
| O-P | csv | `step6-admission/exports/O-P.csv` | `2cb58fb6b0ec81f5859db527821a1701675ba6305553369d9096d5ee2bd93e40` |
| O-P | inputs | `O-P-1000x-inputs.txt` | `cbd5de1fb8023566a8ca65979b8f4cd7147e340976cbe50e28caee33cddcc0d4` |
| O-P | properties | `O-P-1000x-properties.txt` | `d85d948a2c056df5205cf05913ac088f8304baf2f1703cdb56d7d980f297c7f5` |
| O-P | panel | `step6-admission/panels/MNQ_M15.csv` | `cceaac41a9b5029676cbc36f4d2be7e975723a7aa00610e86f63d7980eb27fc8` |
| O-P | margin | `step6-admission/margin/O-P-margin.json` | `30d2535bf7046b7093f3b1e66b7f6ad412e66138ea2974ffd1c9e0d64c3c0110` |
| O-P | attestation | `packet1-source-history-attestation.json` | `7c58510aeb8fe924798e54c464f9daea92b042ea6f65508af092252a6d0a568f` |
| O-P | normalization | `packet1-normalization-diagnostic.json` | `10680786b54622106956354b9f3e03020b7c18f7b1cfe9c1773f5f908e7c2246` |
| O-P | reconciliation | `step2-orb/seven-summary-reconciliation.json` | `e3883d1fcf57a442da748f4ba5da569d644699d82e8b1b1b4fd7568b1ff2cff9` |
| O-P | coverage | `step3-coverage/full-initialization-and-interval.json` | `c1aa67c0fd93d62b423918493b16996cc507aab9de993b47e9c6fcb484eb7da8` |
| S-P | manifest | `step6-admission/manifests/S-P.json` | `13f766bca453a4fae6089ce3190108afbe6e60f7e27dde83a9e8a44f921a2fae` |
| S-P | pine | `step6-admission/pine/striker_dj30_v4.5_mym_pyramid_250_cap100k.pine` | `712cf395396568ce22ae43f1f15b085eaba23acf1b85502abb92129f277fffd7` |
| S-P | port | `step3-coverage/corrected-ports/dj30_mym_p250.py` | `efd479b6b4c7eeaa7d8df3f40f36593f87d96b9d5f512dc79c4dd9b0520211f4` |
| S-P | csv | `step6-admission/exports/S-P.csv` | `0373f211f5e44fe89976d7bcea2b7252724dc717541116dccb59932dfabc710a` |
| S-P | inputs | `S-P-chrome-inputs.txt` | `67f28d8610792beacb81a98e850d8f200e48de26d7b08bfdb0b1c872f601a2f8` |
| S-P | properties | `S-P-chrome-properties.txt` | `f28d1370bfc98fc75a7e38b5a087f7879f23e627f407c476c0cf57f10ffb97a3` |
| S-P | panel | `step6-admission/panels/MYM_M15.csv` | `15b34615ef7793ad73d08691713e2f386e2eb05debea5169a58ede1ff4a6b156` |
| S-P | margin | `step6-admission/margin/S-P-margin.json` | `8bb71492957b4e3d521d42e66d22c56192210f0cd44b3474118d0f9c58f6f02f` |
| S-P | attestation | `packet1-source-history-attestation.json` | `7c58510aeb8fe924798e54c464f9daea92b042ea6f65508af092252a6d0a568f` |
| S-P | normalization | `packet1-normalization-diagnostic.json` | `10680786b54622106956354b9f3e03020b7c18f7b1cfe9c1773f5f908e7c2246` |
| S-P | reconciliation | `step2-orb/seven-summary-reconciliation.json` | `e3883d1fcf57a442da748f4ba5da569d644699d82e8b1b1b4fd7568b1ff2cff9` |
| S-P | coverage | `step3-coverage/full-initialization-and-interval.json` | `c1aa67c0fd93d62b423918493b16996cc507aab9de993b47e9c6fcb484eb7da8` |
| S-W1 | manifest | `step6-admission/manifests/S-W1.json` | `ab72f039da3d7856d98be3e03e2cea1dd22ad82c3b5bca78cbaed7f86fd9d0c3` |
| S-W1 | pine | `step6-admission/pine/striker_dj30_v4.5_mym_pyramid_250_cap100k.pine` | `712cf395396568ce22ae43f1f15b085eaba23acf1b85502abb92129f277fffd7` |
| S-W1 | port | `step3-coverage/corrected-ports/dj30_mym_p250.py` | `efd479b6b4c7eeaa7d8df3f40f36593f87d96b9d5f512dc79c4dd9b0520211f4` |
| S-W1 | csv | `step6-admission/exports/S-W1.csv` | `1996a88569828fa7790306320709c0c0b9eab0586ead5dec03b5acb6435a4add` |
| S-W1 | inputs | `S-W1-inputs.txt` | `0a2c8dc301f428c79929838a3a08b756088ac6f583ce3af5cb72e4082b2256f6` |
| S-W1 | properties | `S-W1-properties.txt` | `2ddf3baa6466740fbf9688c2483780cbd3ca4bc58b44f847e9e69f9ce2e4f90a` |
| S-W1 | panel | `step6-admission/panels/MYM_M15.csv` | `15b34615ef7793ad73d08691713e2f386e2eb05debea5169a58ede1ff4a6b156` |
| S-W1 | margin | `step6-admission/margin/S-W1-margin.json` | `05cb341487ffc1f30ffe836eda1bd0025ff468d5fa798eb36d7a9e5e7533b3d5` |
| S-W1 | attestation | `packet1-source-history-attestation.json` | `7c58510aeb8fe924798e54c464f9daea92b042ea6f65508af092252a6d0a568f` |
| S-W1 | normalization | `packet1-normalization-diagnostic.json` | `10680786b54622106956354b9f3e03020b7c18f7b1cfe9c1773f5f908e7c2246` |
| S-W1 | reconciliation | `step2-orb/seven-summary-reconciliation.json` | `e3883d1fcf57a442da748f4ba5da569d644699d82e8b1b1b4fd7568b1ff2cff9` |
| S-W1 | coverage | `step3-coverage/full-initialization-and-interval.json` | `c1aa67c0fd93d62b423918493b16996cc507aab9de993b47e9c6fcb484eb7da8` |
| S-W1P | manifest | `step6-admission/manifests/S-W1P.json` | `ddcc42c6db36ad16b2c7312abefe38cea0c843ece8813d89e2fdcbd03e618ed9` |
| S-W1P | pine | `step6-admission/pine/striker_dj30_v4.5_mym_pyramid_250_cap100k.pine` | `712cf395396568ce22ae43f1f15b085eaba23acf1b85502abb92129f277fffd7` |
| S-W1P | port | `step3-coverage/corrected-ports/dj30_mym_p250.py` | `efd479b6b4c7eeaa7d8df3f40f36593f87d96b9d5f512dc79c4dd9b0520211f4` |
| S-W1P | csv | `step6-admission/exports/S-W1P.csv` | `ce5e5c879942c3b339220c43b8f66a27d8e1b89389ae95e5b3f1d54c7b8ec9ff` |
| S-W1P | inputs | `S-W1P-inputs.txt` | `6042420b3c4d1f0d1290a09a4f971a390c64e0ff39d5fa8f50bb826fc9d40aca` |
| S-W1P | properties | `S-W1P-properties.txt` | `b1b233acd8e2151f53db159cbe7ee36ae1cfdef79dadf1708a945436dbd4733e` |
| S-W1P | panel | `step6-admission/panels/MYM_M15.csv` | `15b34615ef7793ad73d08691713e2f386e2eb05debea5169a58ede1ff4a6b156` |
| S-W1P | margin | `step6-admission/margin/S-W1P-margin.json` | `e1b2b03fcaa0456521d1bbafe44acf0873069c1950f1405b1c02b59b85fe7a8d` |
| S-W1P | attestation | `packet1-source-history-attestation.json` | `7c58510aeb8fe924798e54c464f9daea92b042ea6f65508af092252a6d0a568f` |
| S-W1P | normalization | `packet1-normalization-diagnostic.json` | `10680786b54622106956354b9f3e03020b7c18f7b1cfe9c1773f5f908e7c2246` |
| S-W1P | reconciliation | `step2-orb/seven-summary-reconciliation.json` | `e3883d1fcf57a442da748f4ba5da569d644699d82e8b1b1b4fd7568b1ff2cff9` |
| S-W1P | coverage | `step3-coverage/full-initialization-and-interval.json` | `c1aa67c0fd93d62b423918493b16996cc507aab9de993b47e9c6fcb484eb7da8` |
| S-W2 | manifest | `step6-admission/manifests/S-W2.json` | `8c037496c1ae3ac80244b999befe570d6b6c9e42756eb046c49a3e848af77690` |
| S-W2 | pine | `step6-admission/pine/striker_dj30_v4.5_mym_pyramid_250_cap100k.pine` | `712cf395396568ce22ae43f1f15b085eaba23acf1b85502abb92129f277fffd7` |
| S-W2 | port | `step3-coverage/corrected-ports/dj30_mym_p250.py` | `efd479b6b4c7eeaa7d8df3f40f36593f87d96b9d5f512dc79c4dd9b0520211f4` |
| S-W2 | csv | `step6-admission/exports/S-W2.csv` | `8c18f1d82f2b82a804973dbc5b77ab1347c48f8328445509a9f82424bf3870aa` |
| S-W2 | inputs | `S-W2-inputs.txt` | `03106b2047e9034c6937388237bd5b1cb7caccfd874784db5bce98bb19eb6d07` |
| S-W2 | properties | `S-W2-properties.txt` | `a3089eaba696a44531e2dd4ac31d92870066fa207d9a416cbebcaee653527af9` |
| S-W2 | panel | `step6-admission/panels/MYM_M15.csv` | `15b34615ef7793ad73d08691713e2f386e2eb05debea5169a58ede1ff4a6b156` |
| S-W2 | margin | `step6-admission/margin/S-W2-margin.json` | `4923fb3b6e38727f82c07632cb98da41d9168a0615371c2633e20191d3aba152` |
| S-W2 | attestation | `packet1-source-history-attestation.json` | `7c58510aeb8fe924798e54c464f9daea92b042ea6f65508af092252a6d0a568f` |
| S-W2 | normalization | `packet1-normalization-diagnostic.json` | `10680786b54622106956354b9f3e03020b7c18f7b1cfe9c1773f5f908e7c2246` |
| S-W2 | reconciliation | `step2-orb/seven-summary-reconciliation.json` | `e3883d1fcf57a442da748f4ba5da569d644699d82e8b1b1b4fd7568b1ff2cff9` |
| S-W2 | coverage | `step3-coverage/full-initialization-and-interval.json` | `c1aa67c0fd93d62b423918493b16996cc507aab9de993b47e9c6fcb484eb7da8` |
| S-W2P | manifest | `step6-admission/manifests/S-W2P.json` | `45fd5cd61512d666b463e3a115d023ae14cc997687c2de0f6b62248602d6dbe1` |
| S-W2P | pine | `step6-admission/pine/striker_dj30_v4.5_mym_pyramid_250_cap100k.pine` | `712cf395396568ce22ae43f1f15b085eaba23acf1b85502abb92129f277fffd7` |
| S-W2P | port | `step3-coverage/corrected-ports/dj30_mym_p250.py` | `efd479b6b4c7eeaa7d8df3f40f36593f87d96b9d5f512dc79c4dd9b0520211f4` |
| S-W2P | csv | `step6-admission/exports/S-W2P.csv` | `d2077b1c4bdcad2a17f84eab62ecb24a518b16b2aca185e5409f0191896fb09e` |
| S-W2P | inputs | `S-W2P-inputs.txt` | `e5b3720628b0e6351ee8f2e24be53f0bffcabc127ae73966b8bcff99e7e26aaa` |
| S-W2P | properties | `S-W2P-properties.txt` | `ec8c86ba49557c49336fd4c3f112db6a8fc368e872caf929eca4a501587e463b` |
| S-W2P | panel | `step6-admission/panels/MYM_M15.csv` | `15b34615ef7793ad73d08691713e2f386e2eb05debea5169a58ede1ff4a6b156` |
| S-W2P | margin | `step6-admission/margin/S-W2P-margin.json` | `77143897ef14f39da50cff636eff6fb931ab116714abeb0b68a440b639f62cf2` |
| S-W2P | attestation | `packet1-source-history-attestation.json` | `7c58510aeb8fe924798e54c464f9daea92b042ea6f65508af092252a6d0a568f` |
| S-W2P | normalization | `packet1-normalization-diagnostic.json` | `10680786b54622106956354b9f3e03020b7c18f7b1cfe9c1773f5f908e7c2246` |
| S-W2P | reconciliation | `step2-orb/seven-summary-reconciliation.json` | `e3883d1fcf57a442da748f4ba5da569d644699d82e8b1b1b4fd7568b1ff2cff9` |
| S-W2P | coverage | `step3-coverage/full-initialization-and-interval.json` | `c1aa67c0fd93d62b423918493b16996cc507aab9de993b47e9c6fcb484eb7da8` |

## Supplementary runtime identity (19 files)

Each fresh worktree byte hash matches the supplementary independent-review pin. This is the historical c86a0a0 runtime; changed Phase 2/F1 runtime needs its own complete identity and acceptance.

| Repository-relative runtime | SHA-256 |
|---|---|
| `core/dd_geometry.py` | `2195f93501758a8a0366e333c57522a243dd200ad752fd97df88920bdf5fac60` |
| `core/dd_protection.py` | `b05f50ef572c2df8a289be1c4a411fa5aea8c0089885658952724913d0f76470` |
| `core/firm_rules.py` | `aea6abaa175d2da8352be63bd603c82f28e9d1df1c8956f5fb9a37598f09f49b` |
| `core/historical_challenge.py` | `53ab52e1b6313f61f30a961e76d32b6caff99ea1fd2879c240e9ab48bb5a487f` |
| `core/lib/atomic_io.py` | `8d5aa7dc46aec5b267cffb14de810757b330af20bd0684646426a1fb453481f7` |
| `core/lib/mvd.py` | `57d35c97c8afbc9f037f07d9472421f92d4da1e4ace0941e8046f124280b3b51` |
| `core/lib/validation.py` | `02aa8d6eb58a14d724567f2b03d46af990820899b436e5083a395b65505eba75` |
| `core/lifecycle.py` | `0a70785dada705b6ea1e6b0951ad0caaa00944bd8a3b49b5d9d3a365c83eaf87` |
| `ops/c1_rail/__init__.py` | `6bec736a516af7ea223e23dab31740cb44353144accd0b79efb209c3a7a7e1ed` |
| `ops/c1_rail/book_policy.py` | `ffcd3aab3e74235e60c711f266f884f96874072c3d84d0b3e1d25d67abd8567a` |
| `ops/c1_signal_daemon/__init__.py` | `a7a7421aeeb83075b70a28b21f857f001859c082a4aa5d4d83e58f4f2989efd7` |
| `ops/c1_signal_daemon/book_adapters.py` | `83830d5e10e50c06a2ebd37511146d5f0e47f0fd467155693279a704a17beec5` |
| `ops/c1_signal_daemon/book_bundle_execution.py` | `de6679403838668f8addcccb4d976c70f275a1515ded3b7cb86d015339c0a657` |
| `ops/c1_signal_daemon/book_bundle_intake.py` | `fdea76cf974157780484bd81c638f6415a6afa7a001e731a738eb2924f340a06` |
| `ops/c1_signal_daemon/book_parity.py` | `42df0ffab3ef2121c464c7b5dcc0cfc9c7bebb2d236ee8c0e81f261d2cac556a` |
| `ops/c1_signal_daemon/book_protocol.py` | `37d1cd7885604f198c88fe6ae3d792e0b42416b37caf7bfc0afa53a8475375e8` |
| `ops/c1_signal_daemon/feed.py` | `b94e43c0e3410a82d9a25c05f4e3f84e278a3840e7eddc8452ceb4e038148e35` |
| `ops/c1_signal_daemon/pine_ta.py` | `7816638aec5a456e4fc8bbde7e52120466686e58465f3a7f1d0a0d311753d69c` |
| `ops/c1_signal_daemon/tv_broker_emulator.py` | `6b6c4cb30639b1a32ec733565894563f42a29d3be30c898a25031dc7bc4a7b7c` |

## Calendar identity and scope

| Repository-relative artifact | SHA-256 (fresh byte hash) |
|---|---|
| `ops/calendars/book_session_calendar_2026-09.json` | `650e8aab4166f74a988675a3f3dfa2dbd21c1c1b342777ac37d65aacea9d6f2f` |
| `ops/calendars/book_closure_overlay.json` | `483f2324b85548e60429b823454641a0ee6e34c8ef2a9cadc7dcc6555f7def5b` |
| `ops/calendars/evidence/2026-09-15-forward-session-source-captures.json` | `56951e1527af20966dea64130bf8d0a1dccb9bc011bd6e0501282faa549fcba5` |
| `ops/calendars/cme_holiday_calendar_2022_2026.json` | `2698f2688cce582b08df58516fd770fa4a71a18de04870d9c14511731ea181e9` |
| `ops/calendars/RATIFIED.json` | `c30bf64e6c839fb230120c5a814a55d4030ce11a7dbe272a7f240a29c379c604` |
| `docs/notes/2026-09-15-calendar-coverage-inventory.json` | `e2841b6273fab0f890a6f906e436b1e786124533e5b6607acd55445fa2fb6fae` |

Ratification covers September 3–30 account sessions, from 2026-09-02T22:00:00Z through 2026-09-30T21:00:00Z. September 7 and 8 remain denied. Review due September 24; schema-v1 product-coverage warning remains. Historical D19 date membership and the incomplete archival coverage inventory do not establish historical exchange legality or full F1 calendar parity. The original Step 4 note has a historical pending-review heading; later Phase 1 handoff accepts the inherited ratified September calendar component only.

## Transfer limits and pending identity reconciliation

- Historical Step 6 result: seven PASS bundles, 3,173 matched trades, 661,501 bars, zero exclusions, resolved terminal positions/pending orders. ORB has 567,018 finite-margin phase checks; captured Striker uses zero margin. These are retained evidence counts, not a newly executed run.
- Accepted Step 3 covers nine captured references, 3,632 trades and 851,011 ordered bar calls with full-origin cold replay. It does not establish arbitrary restart or live settlement behavior.
- All five accepted historical Striker manifest ports hash to `efd479b6b4c7eeaa7d8df3f40f36593f87d96b9d5f512dc79c4dd9b0520211f4`. The initial Phase 2 handoff named original runtime Striker `c81aa59c811dd2f318bf2f6b51e9df32fca20315ffab0885ec1d4ec6a2ab5379`; these are distinct byte identities. The owner correction below resolves registry selection, without asserting semantic equivalence or changing either preserved artifact.
- Actual CSV/query timezone semantics, September 14 boundary equity/flatness and correction-status evidence remain missing. Phase 2's bounded offline commit/review is reported below; no merged combined F1 runtime acceptance is established here. Historical admission is not combined Phase 1 acceptance or full-book F1 parity.

## Aegis and Vanguard retained Step 3 evidence

The accepted Step 3 contract and independent acceptance above also cover Aegis and Vanguard; the seven Step 6 manifest table does not enumerate these older references. The rows below identify retained evidence, without copying source bodies, settings values or panel data. `E/` denotes the private evidence root above, `R/` the primary checkout, and `D/` the operator Downloads directory. Every listed byte hash was freshly computed; port/panel/export hashes were checked against the accepted Step 3 contract. Installed-body capture byte hashes are distinct from registry source identity hashes and must not be conflated.

| Leg | Kind | Relative reference | SHA-256 (fresh byte hash) |
|---|---|---|---|
| aegis_6j | installed source capture | `E/step3-coverage/Aegis-installed-body.pine` | `db78ecba95ae78aca14501a5eaccfda2a42164d83cac12321cb7f293a9adca7c` |
| aegis_6j | input settings capture | `E/step3-coverage/Aegis-current-inputs.txt` | `5338c678a55ef67adfc4eb9b6edf4feaa9560d86b67143b6b2a490911aabfacd` |
| aegis_6j | port | `E/step3-coverage/corrected-ports/aegis_6j.py` | `11763740bc3fdcc8b9e94cb0b465823aec202cd8333379c46878185db5e9e84f` |
| aegis_6j | panel (attested prefix derivative) | `E/step3-coverage/6J_M15-with-attested-prefix.csv` | `8ae083d07b6870aa427dc69009434da0f3cab2d6818ca356e441ad40f3648fd2` |
| aegis_6j | export | `D/Aegis_6J1_VB_CME_6J1!_2026-09-03_cc310.csv` | `71e732fc92d28a56fbc1e4aa358e10b68f317a110f3facc95ed34508fad96eaa` |
| vanguard_mgc | installed source capture | `E/step3-coverage/Vanguard-installed-body.pine` | `546718c6f2c0080ffc7286ff4a206fc79b058dd219e14a7a60db528cdf58b5ed` |
| vanguard_mgc | input settings capture | `E/step3-coverage/Vanguard-current-inputs.txt` | `4424a5f413e0ca5877b78259bbe373f5c71d0a49b3354d441a6e776491efd522` |
| vanguard_mgc | port | `E/step3-coverage/corrected-ports/vanguard_mgc.py` | `e6a03d04c65a19e7fde71103560a229630c3663f445676f06622feec4e9157a3` |
| vanguard_mgc | panel | `R/core/data/bar_data/MGC_M15.csv` | `c5487470a5a9c8c69303587e5a598f9c66eb28d614695d7d78a4aee918fa6aad` |
| vanguard_mgc | properties capture | `E/step3-coverage/Vanguard-current-properties.txt` | `88c797e5b1b4ca2c7183a3a9e0c65838051f0741927052b9d0fb4f8ec1fd556f` |
| vanguard_mgc | export | `D/Vanguard_Gold_Futures_v0.4_VB_(MGC)_COMEX_MINI_MGC1!_2026-09-03_0e3e3.csv` | `7b9cc65c98945055f35d55cdd43f049efc4b5924e2caa59f36d50b3eb872f9f2` |
| shared | retained evidence | `E/step3-coverage/full-initialization-and-interval.json` | `c1aa67c0fd93d62b423918493b16996cc507aab9de993b47e9c6fcb484eb7da8` |
| shared | retained evidence | `E/step3-coverage/candidate-initializer-binding.json` | `49ed40f1c11f92f612dad13e0baa7d89fe3bf6b08973b893cf2da3c5cb0d32b4` |
| shared | retained evidence | `E/step3-coverage/corrected-state-replay.json` | `45cc38ab2793b30f6d64c0201f2fbcf5ed482c83f8de6819c6dca3b97a4af2d7` |
| shared | retained evidence | `E/step3-coverage/6J-prefix-assembly.json` | `12e8541f88f0e441ae67c96a29a18f6d1c62653caba0a5ab6044d422f6159942` |
| shared | retained evidence | `E/step3-coverage/6J-prefix-provenance-attestation.json` | `b85e6b70be5c729b29dc086daee913de8da1c7ad77e3d4a39d6e4eac8e118177` |
| shared | retained evidence | `E/step3-coverage/original-capture-provenance-attestation.json` | `2b54e1bdc03d44f7dff8238dc05ccd4403bc71734caabb4a8440f75171778d42` |

Both accepted references replay cold from `2022-09-01T00:00:00Z` through `2026-09-03T00:00:00Z` inclusive (initializer record expresses the same endpoints as August 31 20:00 and September 2 20:00, America/New_York). Aegis consumes 94,893 bars including the separately attested 88-bar prefix; Vanguard consumes 94,617 bars. The original unprefixed 6J panel starts September 1 at 23:00Z and is not a substitute for the accepted derivative. Full-origin recursive history is retained; no shortened warmup or arbitrary restart certification follows.

The initializer record identifies registry Pine hashes Aegis `db78ecba95ae78aca14501a5eaccfda2a42164d83cac12321cb7f293a9adca7c` and Vanguard `af26899ca94bb0e9ee26d09e0176b6b94bba2f5da252399ce4d899fe7e3bad15`. These are recorded identity claims from the accepted evidence, not a fresh hash assertion about the installed-body capture bytes. Source/settings acceptance relies on the accepted Step 3 contract, prior source-body attestations, capture provenance and bound active-path replay. A new F1 manifest must explicitly bind those references and its effective settings; this ledger does not create that admission. No separate Aegis current-properties capture was identified in the Step 3 directory; do not infer its nonexistence elsewhere or invent a pin.

## Phase 2 owner refresh — committed corrected registry

The Phase 2 owner acknowledged `c81aa59c...` as the stale original Striker identity and committed corrected registry `efd479b6b4c7eeaa7d8df3f40f36593f87d96b9d5f512dc79c4dd9b0520211f4` in `d107ebdfaec194ac4b4448d1d121331ff7128e1a`. Read-only `git show` of that commit and `ops/c1_signal_daemon/book_adapters.py` confirms the corrected registry and explicit rejection comment for the original. This resolves the registry-selection discrepancy noted above; it does not turn the historical supplementary runtime hashes into hashes for the changed Phase 2 runtime. The owner reports bounded offline review complete. No main merge, combined F1 acceptance, actual-close acceptance or live activation is established by this refresh.
