# RESULTS — Tradeify size-feasibility check (public return)

**Pre-registration:** [`2026-10-08-tradeify-size-feasibility-prereg-DRAFT.md`](../../../../docs/briefs/pre-registration/2026-10-08-tradeify-size-feasibility-prereg-DRAFT.md) (`FROZEN 2026-10-08`, freeze commit `103c5ea`; §11 addendum via #738). Return format per its §8.3: labels, hashes and readers only. No rates, medians, dollar figures or counts appear here.
**Run:** 2026-10-08, on Joshua's GO in chat to the Deployment Coordinator. The executor was a fresh Opus session. It launched at 21:59:45Z and ended at about 02:52Z on 2026-10-09.
**Code:** `main` `0cf32a55185913e896e8583f606f5fab78cde6ce`, which contains the wrapper (`run_size_feasibility.py`, #737). The checkout was clean before and after, and the prereg blob was `1c959fc5`.

## Verdict

**FEASIBLE** (§6, read under §11).

| Item | Value |
|---|---|
| Clearing k | 0.5, 0.4, 0.33, 0.25, 0.2 |
| Largest clearing k | 0.5 |
| Not clearing | 1.0, 0.75 |
| `vacuity-read` k | 0.4, 0.33, 0.25, 0.2 |
| GRID-GAP midpoint | not triggered |
| INVALID or INSUFFICIENT reasons | none |
| Reproduction (a) | matched: report `4076857777e67cedd5755ba637693ce45638357a8a5b1fb17077e63ac28ec2ed`, depth record `87a66d8e9d2baf3b474feb7e69e1e2cdb4138f27e911f666d9b57d0118e483f2` |
| Reproduction (b) | matched |
| Arms | 22, run serially, all exit 0; the cap was not reached |

## Branch selected (T00 card §8 tree, step 1)

FEASIBLE routes to **step 2**:
- lift the hold: new H, P7 re-run and Tier-2 source approval;
- Tier 2 picks one successor configuration;
- R1/R2 resolution may be built in parallel.

Joshua had already chosen to start the R1/R2 build on 2026-10-08.

## Limitations (§11, §1)

- **FEASIBLE is not a successor result.** It sets only a target range for Tier 2 and for one pre-registered successor screen.
- **The rescale is fractional.** Executable successors have integer sizing, admissions and internal state that this harness does not model, and fixed one-contract legs cannot be halved. Every §1 omission is unsigned.
- **Sampled grid only.** There is no monotonicity or interval guarantee between grid points.
- **No intrabar ordering.** The harness does not resolve R1/R2 and is not the successor-screen trigger of the #734 stopping rule.
- **k = 1 reproduction** validates this harness against its own run of record, not against T00.
- **Trial count.** The grid is K = 7 trials. Any successor pre-registration must disclose this run and its readers.

## Private artifacts (gitignored; cited by SHA-256)

Root: `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts/size-feasibility-2026-10-08/`

| File | SHA-256 |
|---|---|
| `verdict.json` (lists every per-call file hash) | `cbd0c96ad63a6878cf7da953ab6f20d97ba306210124bf90c34ee7d56028a558` |
| `run.json` | `35b377137addd0f777c712e9fb18d464f05184a740acc411d258a71387f484dd` |
| `launcher.stdout.txt` | `76e931d4809c4063cc642cfee6f8a577384bb55fd9ea3f7aed87fb39c874fa76` |
| `launcher.stderr.txt` (empty) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

Per-call `report.json`:

| k | FULL | H1 | H2 |
|---|---|---|---|
| 1.0 | `0125aee4118cd54f441bbdd35f0412c701a2d793b2d57a1fe97c759d550fc05c` | `160769826040a35498664d7679a452ae81ccc04d68af9147d734be01ca6e549f` | `dd877b67714fffef813a119aaa58d133af6bba5d285a0ae3de4b29de0c74fb25` |
| 0.75 | `d0283d1e4afc34cc8808d7f6300ad960d762abdcea0d99c97a21a4f7c30b031f` | `f1a6f20077bbea196e1e198d587f1888d34e185051f957c91e168102403e04fc` | `bf9c589df592cb16baf782f315bb0f4787441bdec40ff1e8f9b628252616b670` |
| 0.5 | `ceb4433383737a665d5e6fa110f7767405fa40ece08c41abb2aa8b61acaa8a09` | `cb17947a1fddce48edc43d1e7bf3b9c9326f49e107e03e09b403e69b4c88e5b0` | `267901efe3b1986cacf3c64c006dcc80d5bf653ae45d59239e5c628b2f460dde` |
| 0.4 | `1546803dd5e94c5d91162610812f2dee722568336465c5e46212e129775d9ccc` | `0c586f8956a872c7d8961dc65c058ceabdee41372284904af5de8798635c80e1` | `6ec5ce601892cc4ea59838b4ddde7d69cb7db73065e692f663c3fd4948d090a4` |
| 0.33 | `b02ccec07a4cd735887413c8bc982966ae86bf856f9b5eae3063683f22b88557` | `a375b483affb61cc5aca50da49075d3c9a0f67696d466cc5a33d823d71d083df` | `85fe67403a0d294128d43ab935b61eeb1577d8c450805df0f52721431753a2b4` |
| 0.25 | `994d6203c07c69d99e98b45cfcf02a7e5ffda0430b25a82f1526cd02ec2e1ec5` | `3cf93c5324d6a571b1e6bfa57503a0b857d89bc28e740ab8fdbaca9948b32aa8` | `9607a470db1689b9b02e050804d56fcc0bc2608cbb3ce4df84497033f9c6e523` |
| 0.2 | `d3d03594493079036df3bfe1e4682317fda3c2697cb3ad31a60d423b2cf6b3b5` | `a105ed3bc5e38158c8dccaa8a5ac69104f5ea89820f178760edcb3611cd29672` | `964b68f0454aa836c405ab6637689a03bc05d1d609dfb48ee0bea6393f5a9724` |

## Readers

1. **Executor session:** progress lines during the run, then full results.
2. **Deployment Coordinator:** per-k results from the executor's return, 2026-10-09 ~02:55Z.
3. **Joshua:** per-k results in chat with the Deployment Coordinator, 2026-10-09 ~03:00Z.
