# Packet 1 Step 5 — attended settlement owner (producer to consumer)

Status: **IMPLEMENTED against the approved contract, tests green on synthetic values;
actual producer qualification on the live account NOT started.** Base: PR #394 head plus
Step 4. Owner: Packet 1 coordinator (TB-T1 ongoing) → TB-I3 integration. No close has been
accepted, no key is enrolled, and nothing here grants activation, resumption or deployment.

Contract: [attended settlement contract](../spec/2026-09-15-tradeify-attended-settlement-contract.md)
(operator-approved 2026-09-15). This record implements it; it does not amend it.

## What was built

| Component | Role |
|---|---|
| `ops/c1_rail/ed25519_verify.py` | RFC 8032 Ed25519 verification in the standard library only, because the rail image ships no crypto dependency. Verification only; it cannot sign. Pinned to the RFC test vectors and cross-checked against `cryptography` signatures. |
| `ops/c1_rail/book_settlement.py` | The durable account-close owner: `SettlementStore` (SQLite, FULL synchronous, `BEGIN IMMEDIATE` single writer, account-bound, boot-fenced, hash-chained rows), `verify_package` (every contract check as a named refusal), challenge issuance, signed submission, B7 bootstrap, record-only catch-up, revision invalidation, restart reconciliation and read-only status. |
| `tests/ops/test_book_settlement.py` | 41 tests. `tests/ops/test_ed25519_verify.py`: 8 tests. |

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
- `tests/ops/test_ed25519_verify.py`: 8 passed. `tests/ops`: 1766 passed, 15 skipped.
  `scripts/check_boundaries.py`: OK.

## What this does not do

- No live account was read. No operator key is enrolled. The package assembly from the venue's
  actual reports (cash history windows, dashboard capture, positions view, balance history,
  inception evidence) is not built; the verifier consumes an already-assembled package.
- No HTTP route exists yet. The listener's TB-I3 account owner integrates `issue_challenge`,
  `submit` and `status` under its authenticated control surface (Packet 2/5).
- No activation or resumption: receipts and status carry `grants_activation: false` and
  `grants_resume: false`; a valid settlement while halted remains halted.

## Remaining to close Step 5

1. **Operator evidence** (requested 2026-09-15): the signing public key; cash history from
   inception in windows of at most 14 days with query notes and the report timezone; inception
   evidence; a fresh dashboard capture with the matching balance/equity history; the account-wide
   positions and working-orders view.
2. Build the package assembler from those actual report formats, retaining raw bytes and
   normalized timestamps, and qualify it on the account: inception, full-history re-query,
   close finality and correction semantics, effective-close equity or boundary flatness.
3. Independent review of this implementation against the contract's acceptance-trace table,
   then the TB-I3 integration under the halt owner's permission state.
