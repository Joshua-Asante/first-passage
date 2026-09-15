# Packet 1 Step 6 — evidence assembly and PROVISIONAL seven-bundle run

Status: **ASSEMBLED and PROVISIONALLY EXECUTED 7/7 PASS; independent admission contract NOT
issued; Packet 1 NOT closed.** Base: PR #394 head plus Steps 4–5. Owner: Packet 1 coordinator.
This record prepares the independent admission decision; it is not that decision. No bundle
is admitted, and nothing here grants activation, deployment or resumption.

## What was assembled

A private evidence root under the retained op1 tree, `step6-admission/` (gitignored), built
by the retained tool `build_and_run.py` (SHA-256
`c84985a37a3bccebc1f29a4939fc6c1d0310b87e4f05ec5d8386e4cbea683eb5`). It copies exact bytes
from their retained locations and refuses on any digest drift:

| Slot | Source | Identity |
|---|---|---|
| `pine` (Striker) | retained Pine body | `712cf395396568ce22ae43f1f15b085eaba23acf1b85502abb92129f277fffd7` (registry pin) |
| `pine` (ORB) | retained Pine body | `176c4f70c67d58053c4d3b8170d0a9be3733bc6b76b1e2f928bd7a877be052a3` (registry pin) |
| `port` (Striker) | Step 3 corrected generation `step3-coverage/corrected-ports/dj30_mym_p250.py` | `efd479b6…` (reviewed candidate, not the frozen `c81aa59c…`) |
| `port` (ORB) | `step3-coverage/corrected-ports/orb_mnq_v7.py` | `b1f4e573…` (identical to frozen) |
| `panel` MYM / MNQ | `core/data/bar_data/*_M15.csv`, 2022-09-01 00:00Z → 2026-09-03 00:00Z | `15b34615…` / `cceaac41…` |
| `csv` × 7 | pinned collection-manifest v2 digests; O-N is the corrected export `8e4902c3…` | see manifests |
| `inputs`, `properties` | the reviewed per-case Inputs/Properties captures (S-P: chrome captures; O-N: corrected captures; O-P: 1000x captures) | per manifest |
| `attestation` | `packet1-source-history-attestation.json` (operator: pinned bodies ran unchanged) | per manifest |
| `normalization` | `packet1-normalization-diagnostic.json` (seven PASS) | per manifest |
| `reconciliation` | `step2-orb/seven-summary-reconciliation.json` (seven PASS under D17/D32) | per manifest |
| `coverage` | `step3-coverage/full-initialization-and-interval.json` (Step 3 accepted) | per manifest |
| `margin` × 7 | new, panel/port/export-bound finite-margin and shared-law evidence (below) | per manifest |

Execution settings per bundle follow the retained shared-law diagnostic exactly: Striker
`account_size` 40000 / 50000 / 20000 / 25000 / 10000 (S-P, S-W1, S-W1P, S-W2, S-W2P),
`micro_cap` 20, `backtest_mode` false, cap 20, risk 700 dollars, margin 0; ORB `qty` 1 with
scale-in on (O-N) or off (O-P), cap 3, margin 0.1% (the O-7 finite substitute, recorded as an
approved deviation); emulator capital 100000, commission 0.91 per side, slippage 1 tick,
orders on close. Window and cold start at the panel origin.

## Pre-admission margin and shared-law evidence

Produced with the same components the admission runner uses (`book_bundle_intake`
`fdea76cf…`, `book_bundle_execution` `de667940…`, `tv_broker_emulator` `6b6c4cb3…`,
`book_parity` `42df0ffa…`, `book_policy` `ffcd3aab…`), on the corrected Striker port:

| Bundle | Matched / export | Margin phase checks | Final state | Verdict |
|---|---|---|---|---|
| O-N | 1,595 / 1,595 | 283,509 | resolved | PASS |
| O-P | 573 / 573 | 283,509 | resolved | PASS |
| S-P | 203 / 203 | 0 (margin 0) | resolved | PASS |
| S-W1 | 203 / 203 | 0 | resolved | PASS |
| S-W1P | 203 / 203 | 0 | resolved | PASS |
| S-W2 | 203 / 203 | 0 | resolved | PASS |
| S-W2P | 193 / 193 | 0 | resolved | PASS |

Zero excluded, missing or extra trades in every case. Striker cases carry no finite-margin
envelope by construction (margin 0); their artifact records shared-law parity only.

## Candidate manifests (exact bytes for the reviewer)

| Bundle | Manifest SHA-256 |
|---|---|
| O-N | `945b7aa54d24046940380bc4df7e5ee2d99937c182a4b2ba4a7c44287ad3adbb` |
| O-P | `abf5b1530f0324259ba962a93535c3f143a610fbef4114107e47ed9b6f6396d9` |
| S-P | `13f766bca453a4fae6089ce3190108afbe6e60f7e27dde83a9e8a44f921a2fae` |
| S-W1 | `ab72f039da3d7856d98be3e03e2cea1dd22ad82c3b5bca78cbaed7f86fd9d0c3` |
| S-W1P | `ddcc42c6db36ad16b2c7312abefe38cea0c843ece8813d89e2fdcbd03e618ed9` |
| S-W2 | `8c037496c1ae3ac80244b999befe570d6b6c9e42756eb046c49a3e848af77690` |
| S-W2P | `45fd5cd61512d666b463e3a115d023ae14cc997687c2de0f6b62248602d6dbe1` |

## Provisional run

`contract-provisional.json` (`cf0d72df7c57c83621b0d49997b21d7df21579a8518d9beee3481ee2ed9d99af`,
`reviewed_by` = "PROVISIONAL coordinator dry run … NOT an independent admission") pins the
seven digests. `admit_bundle` and `run_bundle_parity` executed all seven with `FP_PORT_ROOT`
at the corrected-ports generation and the legacy panel/export directories pointed at absent
paths: **7/7 passed**, 3,173 matched trades, zero exclusions, resolved final state,
94,503 (MNQ) and 94,499 (MYM) bars each. Result: `provisional-run.json`
`645131636cebab66f64ecd64b0d3153c528b78d66cd997c71a24a63b65f05d31`.

A provisional contract proves the manifests are executable and the evidence root is complete.
It admits nothing. The candidate cannot approve itself.

## Remaining to close Step 6 and Packet 1

1. **Independent review** of the seven manifests, the `margin` artifacts, this record and the
   Steps 4–5 records, then issuance of the real `book-bundle-admissions-v1` contract naming the
   reviewer and pinning the seven digests above, with the contract's SHA-256 supplied out of
   band. Re-run `run_bundle_parity` under that contract and record the result.
2. Final combined review of Packet 1 (Steps 1–6) and the Packet 1 acceptance items, including
   the calendar ratification row and the settlement owner's pending live qualification.
3. Packet 2 and every live gate remain separate.
