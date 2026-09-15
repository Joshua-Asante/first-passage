# Packet 1 Step 5 — attended settlement owner (producer to consumer)

Status: **IMPLEMENTED against the approved contract; producer QUALIFIED on the operator's actual
reports (2026-09-15); operator key ENROLLED; independent review still owed.** Base: PR #394 head plus
Step 4. Owner: Packet 1 coordinator (TB-T1 ongoing) → TB-I3 integration. No production close
has been accepted, and nothing here grants activation, resumption or deployment.

Contract: [attended settlement contract](../spec/2026-09-15-tradeify-attended-settlement-contract.md)
(operator-approved 2026-09-15). This record implements it; it does not amend it.

## What was built

| Component | Role |
|---|---|
| `ops/c1_rail/ed25519_verify.py` | RFC 8032 Ed25519 verification in the standard library only, because the rail image ships no crypto dependency. Verification only; it cannot sign. Pinned to the RFC test vectors and cross-checked against `cryptography` signatures. |
| `ops/c1_rail/book_settlement.py` | The durable account-close owner: `SettlementStore` (SQLite, FULL synchronous, `BEGIN IMMEDIATE` single writer, account-bound, boot-fenced, hash-chained rows), `verify_package` (every contract check as a named refusal), challenge issuance, signed submission, B7 bootstrap, record-only catch-up, revision invalidation, restart reconciliation and read-only status. |
| `tests/ops/test_book_settlement.py` | 49 tests. `tests/ops/test_ed25519_verify.py`: 8 tests. `tests/ops/test_account_close_assembler.py`: 12 tests. |

## Protocol as implemented

1. **Enrolment.** `SettlementStore.boot` takes the enrolled operator public keys (32-byte hex)
   with their scopes, the ratified calendar digest and the policy digest. Changing any of them
   across a restart refuses to boot. Every boot is a new fenced owner; open challenges are voided
   and the store is `restore_pending` until `reconcile_restore` verifies the hash chain.
2. **Initial state.** `bootstrap_b7` seats the chain head once from the sealed B7 snapshot
   (all ten checks pass, balance equals equity, peak at or above equity, seal not expired, the
   effective close inside the seal's boundary window). Its origin is `B7`; it is distinct from
   every later close and grants no activation.
3. **Challenge.** `issue_challenge` returns a one-use envelope bound to account, boot id, halt
   generation, scope, proposed and target sessions, predecessor session and package digest,
   contract, calendar and policy digests and the evidence-package digest. Lifetime is 300 seconds
   from server issue; for `submit_account_close` it is also capped by the target session's
   risk-add cutoff; `record_only` takes no target and is issued only while HALTED.
4. **Submission.** `submit` verifies, in order: enrolled key and scope, Ed25519 signature over
   the canonical envelope bytes, challenge identity/state/expiry, boot/generation/digest binding,
   evidence bytes unchanged, predecessor unchanged, proposed session, duplicate session (halt),
   then the full package (below). One transaction appends the package and event, consumes the
   challenge, appends the chain row with equity, ratcheted peak and `mode_next` from the shared
   policy, and returns a receipt. A refused submission advances nothing and leaves the challenge
   issued; a consumed challenge cannot be reused; four concurrent writers yield one receipt.
5. **Package checks** (`verify_package`): schema and contract, account and venue, calendar and
   policy digests, session in the ratified calendar with the chain head as its prior (else
   `out_of_order_settlement`, halt), effective close equal to the session's account close and
   after the predecessor, operator signing time not in the future, IANA report timezone,
   inception before the close, every source file present with matching bytes, no future capture,
   every non-inception source no more than 30 minutes old at receipt, all five roles present
   (dashboard, positions, balance history, cash history, inception), net equity on the
   `NET_OF_TRADING_COSTS` basis, flatness basis either daily-flatten-confirmed with no unresolved
   runtime requests or venue equity at the close with its valuation basis, ledger continuity
   `predecessor + gross − commission − exchange − clearing − nfa = net` in decimal arithmetic,
   absolute adjustments exactly zero, no unknown or unlinked rows, no duplicate transaction ids,
   no revisions, every previously retained transaction present with an identical hash, bounded
   history windows (limit at most 14 days) overlapping from inception to the capture, dashboard
   balance equal to net equity and `trailing_threshold + width = ratcheted peak` with the width
   from the tier rules, and all four attestations true.
6. **Corrections.** `record_revision` retains both versions, marks the revised row and every
   later row `INVALIDATED`, voids open challenges, sets the store invalidated and demands a halt.
   No forward acceptance or `SettledClose` is possible until a reviewed reconciliation re-seats
   the chain; nothing is rewritten.
7. **Consumer.** `settled_close()` returns the exact `SettledClose(session_id, as_of, equity,
   peak, seal_digest=package_sha256)` and `mode_next`. The test feeds it, with the ratified
   calendar's `BookSession`, through the real `size_book_request` and the consumer accepts.

## Verification

- `tests/ops/test_book_settlement.py`: 41 passed. Covers the happy path into the consumer,
  PROTECTED derivation on the ratcheted peak, chaining and retained-history refusal, unknown key,
  wrong scope, bad signature, tampered envelope, expiry, generation and evidence binding, cutoff
  cap, unavailable target, four-way concurrent submission, duplicate and out-of-order halts,
  revision invalidation, restart with voided challenges and fenced old handle, tampered chain row,
  changed digests or keys across restart, B7 bootstrap refusals and PROTECTED seating, record-only
  catch-up in predecessor order while HALTED, a 26-case package refusal matrix with the challenge
  left issued, venue-equity basis acceptance, and offsetting adjustments refused despite zero net.
- `tests/ops/test_ed25519_verify.py`: 8 passed. `tests/ops`: 1778 passed, 15 skipped.
  `scripts/check_boundaries.py`: OK.

## Producer qualification on the actual account reports — 2026-09-15

The operator collected the venue reports into the private folder
`producer-qualification-2026-09-15/` under the op1 evidence root (six cash-history windows
of at most 14 calendar dates including one empty window, the account-balance history, the
Tradeify dashboard summary and objectives captures with a detail text, the Tradovate
positions and orders views, the activation email as inception evidence, capture times and
a collection status). Originals remain in Downloads; copies were verified byte-for-byte.

`ops/c1_rail/account_close_assembler.py` (12 tests on synthetic exports in the exact
column shapes) turned them into the package for account session
`tradeify-account-day:2026-09-14` with predecessor `2026-09-11`. Figures stay private; the
verdicts:

| Check | Result |
|---|---|
| Cash windows | 6 windows, 100 raw rows, 91 distinct transactions, 9 boundary duplicates removed, 0 revisions |
| Classification | Fund Transaction 1 (nominal basis, equal to the tier starting balance); Commission, Exchange, Clearing and NFA fee rows all contract-linked; Trade Paired rows; 0 unknown, 0 unlinked, adjustments exactly zero |
| Running balance | every row's reported amount equals the reconciled running net |
| Balance history | 25 rows, 0 mismatches against the reconciled equity at each trade date |
| Dashboard | balance equals the reconciled net equity; trailing threshold plus the 3,000 width equals the EOD peak from the ledger |
| Session 09-14 | no activity; flat at the close by the no-later-fills rule with flat positions and zero working orders at capture |
| `verify_package` | no refusal |
| Store path | qualification head seated, challenge issued, signed submission accepted, `mode_next = normal` |
| Consumer | `size_book_request` for session 09-15 with the produced `SettledClose`: no halt |

Package SHA-256 `72b0c65dff701d08b77b360b76be2092f1c30d44fcf8279bf52df01d232f4885`; outputs and
the figures-free `qualification-report.json` are retained under the same private folder.

Limits recorded with the run: the store head was seated from the reconciled predecessor
state, not the B7 seal (a Packet 6 gate); the four attestations were placeholders that the
operator supplies by signing a real challenge; CSV capture instants are the Downloads file
times, operator-side rather than server evidence; the qualification receipt instant was the
last capture plus three minutes, so a live acceptance needs captures within 30 minutes of
receipt; the policy digest is a placeholder pending TB-I3's shared fingerprint; the
report timezone is the UI's Central label, which the CSV itself does not declare.

## Operator key enrolled — 2026-09-15

The operator generated an Ed25519 keypair on their own device (private key under their
home `.signing` folder, never in the repository) and confirmed the public key in chat
("confirm"). `ops/c1_rail/operator_keys.json` records key id
`1f75cea0c36941f8964d393490b6886bcbcdb010b4bc67dd45e925d1a04604aa` with scopes
`submit_account_close` and `record_only`; `book_settlement.load_operator_keys` refuses any
record that is malformed, non-operator, revoked-only or not a curve point, and the store
boots from its result. The account binding happens at runtime.

## What this does not do

- No live close has been accepted by a production owner; the qualification store is a private
  artifact. The listener does not yet host the challenge/submit/status routes.
- No HTTP route exists yet. The listener's TB-I3 account owner integrates `issue_challenge`,
  `submit` and `status` under its authenticated control surface (Packet 2/5).
- No activation or resumption: receipts and status carry `grants_activation: false` and
  `grants_resume: false`; a valid settlement while halted remains halted.

## Remaining to close Step 5

1. Independent review of this implementation and the qualification against the contract's
   acceptance-trace table.
2. TB-I3 integration: host challenge/submit/status under the listener's authenticated control
   surface and the halt owner's permission state; bind the real policy digest and account.
3. First live acceptance only after the B7 seal seats the chain head (Packet 6), with fresh
   captures within 30 minutes of receipt and the operator's real signature.
