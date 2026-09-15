# Packet 1 Step 5 — attended settlement owner (producer to consumer)

Status: **REBUILT 2026-09-15 against an explicit invariant table after five Codex review rounds;
producer QUALIFIED on the operator's actual reports; operator key ENROLLED; independent review owed.** Base: PR #394 head plus
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
| Session 09-14 | no activity; flat at the close by the no-later-fills rule with flat positions and zero working orders at capture; settled on the `NO_ACTIVITY_DASHBOARD_CORROBORATED` basis (no venue balance row exists for the day; the latest venue row and the dashboard both equal the reconciled equity) |
| `verify_package` | no refusal |
| Store path | qualification head seated, challenge issued, signed submission accepted, `mode_next = normal` |
| Consumer | `size_book_request` for session 09-15 with the produced `SettledClose`: no halt |

Package SHA-256 `ee6ed065e3d5` prefix (re-run after the rebuild; earlier packages `72b0c65d…`,
`261b4578…` and `c239fd35…` predate transaction provenance, the scope/basis fields and the single
chronology invariant); outputs and
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

## Review fold — 2026-09-15 (Codex on PR #395)

- **B7 seal authenticated before seating.** `bootstrap_b7` now requires the seal's exact
  SHA-256 and the sealer's tool digest out of band, the seal contract path, exactly the ten
  checks in order all passed, three distinct evidence digests with capture times, the full
  sealer value set, and re-derives C3 (balance equals equity, flat, no working orders), C4
  (`peak = trailing_threshold + width`, peak at or above balance) and C8 (zero adjustments,
  original basis equal to the tier constant).
- **Small-order keys refused.** The verifier and the enrollment loader reject any public key or
  signature point that is the identity or another torsion point, and require the key to lie in
  the prime-order subgroup; the identity key with `R = identity` and `S = 0` no longer verifies.
- **Flatness basis requires flat evidence.** Under `DAILY_FLATTEN_CONFIRMED_NO_LATER_FILLS`
  the positions view must show zero open positions and zero working orders.
- **Package bytes are part of the chain.** Every chain row's retained package bytes must be
  present and hash to the row's digest; a modified or deleted package refuses every read, and a
  missing predecessor package can no longer silently skip the retained-history comparison.
- **Capture times bound to sources.** The dashboard and positions capture times in the package
  must equal the freshness-checked source rows.
- **Late-added history refused.** Transactions carry their account-session id; any transaction
  not retained from the predecessor must belong to the proposed session.
- **Key rotation across restart.** A changed enrolment no longer refuses boot: the chain is
  preserved, the change is recorded as an audited `trusted_keys_rotated` event, and only
  currently enrolled keys can sign afterwards.
- **Balance history bound to the account** by its Account Name column, with a single venue id.
- **Cash rows outside any session refuse** (the 17:00–18:00 ET break, Friday evening, the
  weekend before the Sunday reopen) instead of being attributed to a neighbouring session.
- **Venue balance row required** for any session with activity; a no-activity session settles
  only when the latest venue row and the dashboard both agree with the reconciled equity, and the
  basis is recorded.

Re-qualification on the operator's reports after the fold: every verdict in the table above
holds; no real cash row fell outside a session.

## Review fold, round two — 2026-09-15 (Codex on PR #395)

- **Orders evidence required**: the account-wide orders export is a required source role, so a
  zero working-order claim is always backed by its own capture.
- **Close-sensitive captures at or after the effective close**: dashboard, positions, orders,
  balance history and every cash window must be captured at or after `effective_close_utc`.
- **Historical catch-up reconciles against the current dashboard**: under `record_only` the
  dashboard may show a peak at or above the historical one; equality is required only for a
  current-session submission, and the assembler requires the venue balance row for historical closes.
- **B7 session metadata bound**: the effective close must be a weekday 17:00 ET on the date named
  by the session id, inside the seal window.
- **Calendar and policy digests rotate across restart** as audited `digests_rotated` events; the
  chain is preserved and every later challenge binds the new digests.
- **Append-only key revocation**: a later enrollment row with `revoked_utc` removes the key; a full
  revocation leaves no active key and refuses boot until a replacement is enrolled.
- **Source bytes retained**: every accepted package stores its evidence bytes, verified by digest
  on every chain read.
- **Transaction ids and digests** must be short printable identifiers and 64-hex digests.
- **Query completion attested**: each cash window carries an operator-typed completion flag from
  the retained query capture; an unattested window refuses.
- **Calendar**: the first row's predecessor must be the immediately preceding account day, and
  admission waits for every qualified product's matching interval (`admits_from`; refusal
  `before_product_open`).

Re-qualification after the fold: unchanged verdicts, same package digest `261b4578…`; all six
cash windows are attested complete from the collection record.

## Review fold, round three — 2026-09-15 (Codex on PR #395)

- **Revoked keys stay revoked**: the enrollment loader keeps a permanent revoked set and refuses
  any later enrollment row for a revoked key id.
- **Distinct evidence**: filenames are unique across every source, and digests are unique across
  the required roles; several empty cash windows may legitimately share bytes.
- **Session rows cite the venue sources**: every row must include the venue's declared source ids.
- **Scope bound to the package**: the package carries `scope` and `settlement_basis`; the verifier
  requires the package scope to equal the signed challenge scope and, for `record_only`, the
  `VENUE_ROW` basis. The assembler takes the scope explicitly and derives the historical rule from it.
- **Publication time** must not be later than receipt.

Re-qualification after the fold: unchanged verdicts; package digest `c239fd35…`.

## Review fold, round four — 2026-09-15 (Codex on PR #395)

- **Historical catch-up with later fills**: under `record_only` the fresh full history may contain
  fills from later missed sessions; the assembler no longer treats them as failed flatness. The
  venue's balance row for the settled trade date is the venue-backed equity at that close
  (`flatness_basis = VENUE_EQUITY_AT_CLOSE`, valuation basis naming the row). Fills inside the
  17:00–18:00 ET break are still refused as outside any session.
- **Key account binding**: an enrollment row's `account_binding` must be `BOUND_AT_RUNTIME` or the
  literal account the runtime boots for; anything else refuses the record.
- **Whole-minute boundaries**: session opens, closes and deadlines must fall on a whole minute.

Re-qualification after the fold (report 2026-09-15T15:18:54Z): unchanged verdicts and package
digest `c239fd35…`.

## Rebuild — 2026-09-15

Five Codex rounds on PR #395 (12, 11, 5, 3, 9 findings) showed the folds were fixing examples,
not the rules behind them (Codex root-cause read, endorsed by the operator: evidence labels
treated as proof; related fields validated separately; an incomplete durable-state lifecycle;
over-generalized calendar assumptions). The owner was rebuilt from the
[invariant table](2026-09-15-packet1-step5-invariant-table.md): `verify_package` is an ordered
list of thirteen named invariants over the whole record (one chronology invariant covers every
timestamp the package and challenge carry, refusals `chronology:<detail>`); `SettlementStore`
has a phased, integrity-hashed state row with one transition function (EMPTY → SEATED →
ACCEPTING; any → INVALIDATED on revision; INVALIDATED → re-seated only through
`resolve_invalidation` under a reviewed reconciliation, with superseded rows retained);
enrolment rotation and digest rotation across restart are audited events; retained package and
source bytes are re-verified on every read.

Decisions delegated by the operator and taken here:

- **Historical close equity.** No venue report seen so far shows account equity at a past close
  (balance history and cash history are cash figures; "Client Statements" is absent from the
  report menu). A historical close therefore requires a separately captured `close_equity`
  source and the operator-typed value it shows, equal to the reconciled equity; `record_only`
  refuses without it. Historical catch-up is blocked by design until such a producer exists.
- **Calendar evidence schema.** Source captures gain schema v2 with per-capture `products`; under
  v2 every product row, permitted or denied, must cite a capture covering that product. The
  ratified September file stays under v1 and every decision on it carries the warning
  `evidence_schema_v1_no_product_coverage`; the October extension is authored under v2.

Verification after the rebuild: `tests/ops` 1834 passed, 15 skipped; boundaries OK; real-report
qualification re-passes (verifier clean, signed submission accepted, consumer no halt) with the
September 14 no-activity session on the corroborated basis. The earlier review-fold sections
above are historical; the invariant table is the current statement of what is enforced.

## Post-rebuild review repair — 2026-09-15

Starting revision: `f29ee061fd410fa8ab5e4c9f03245cf107210fa7` (PR #395).
The six findings on that rebuild were reproduced and repaired. An independent
review of the repairs exposed four related gaps, which were also reproduced,
repaired and accepted on focused re-review.

The changes consolidate authority instead of adding separate recovery paths:

- The minimum outstanding revision sequence lives in checked owner state;
  resolution archives the entire affected suffix in one SQL statement, preserves
  the unchanged prefix, and leaves restore reconciliation required. Rehashing that
  prefix and selecting the newest audit event are removed.
- One history digest binds active and superseded rows, correction payloads and
  reconciliation links. Both kinds of accepted close use the same retained-evidence
  verifier, deriving source identities from the hash-bound package. Edits and
  suffix/whole-history deletion refuse reads and restart.
- Challenge issue/expiry come from the verified signed envelope, not duplicate
  database columns. Non-inception captures must precede challenge issuance; B7
  requires aware close/capture/seal timestamps in order through receipt.
- The verifier rejects later-session transactions in a current close even when
  its predecessor is B7. Historical submissions require the venue-equity basis
  at the verifier boundary, matching the assembler's existing requirement.
- Calendar ratification timestamps preserve second precision; trading boundaries
  retain their whole-minute rule. Ratified artifact bytes are unchanged.

Verification: Python 3.13, `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, `python -m pytest
tests/ops -q`: **1889 passed, 15 skipped** (two upstream seaborn deprecation warnings).
The initial focused baseline passed 172 tests; 36 new failing cases reproduced
the original findings, then 13 failing cases reproduced the independent follow-up
findings. Positive controls cover earlier inception history, repeated revisions,
multiple correction cycles, and complete historical inventory across catch-up.
The older-schema regression verifies refusal leaves the database bytes unchanged.
The independent reviewer reran 40 focused cases and accepted the repaired code.
The repository boundary checker passed.

Internal store schema is now version 2; older stores require reviewed migration
and are refused without modification. No automatic migration or deletion is
provided for previously unanchored history. Historical catch-up still requires a
qualified venue close-equity producer, which the rebuild did not establish. No
live evidence was recaptured and no live close, enrollment, activation or resumption
was performed. These results establish code repairs, not renewed private-report
qualification or Step 6 admission.

