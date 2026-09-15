# Packet 1 Step 5 — settlement owner invariant table

Status: authored 2026-09-15 for the rebuild of the settlement owner after five Codex review
rounds on PR #395 folded findings by example. Each row below is one claim the
[attended settlement contract](../spec/2026-09-15-tradeify-attended-settlement-contract.md)
makes, the single named refusal that enforces it, and where it is checked. A finding that
does not map to a row is a missing row, not a patch. Tests violate exactly one row each.

## Verifier invariants (`book_settlement.verify_package`)

| Id | Claim (contract) | Refusal | Checked with |
|---|---|---|---|
| V1 | The record is this contract's package: exact schema, contract path, exact key set | `package_schema`, `package_keys` | package |
| V2 | The package is for this account and venue | `wrong_account` | owner account |
| V3 | The package's declared scope is the signed scope; its settlement basis is typed; a historical close (`record_only`) rests on the venue balance row | `scope_mismatch`, `settlement_basis`, `historical_close_needs_venue_row` | challenge scope |
| V4 | Calendar and policy digests are the owner's | `digest_mismatch` | owner state |
| V5 | The session is a ratified calendar row whose prior is the chain head; the predecessor package digest is the head's | `session_id`, `session_not_in_calendar`, `predecessor_mismatch`, `out_of_order_settlement` (halt) | calendar, head |
| V6 | The effective close is that session's account close and follows the predecessor's | `effective_close_not_session_close`, `effective_close_not_after_predecessor` | calendar, head |
| V7 | One chronology holds across every timestamp: inception < effective close ≤ every close-sensitive capture ≤ challenge issue ≤ operator signing ≤ receipt; publication (if any) ≤ receipt; every non-inception capture within 30 minutes of receipt; embedded dashboard and positions times equal their source rows; history windows overlap from inception and end exactly at the cash capture | `chronology:<detail>` | package, envelope (`issued_utc`), receipt |
| V8 | Evidence is complete and independent: string roles and files, every required role present, unique files, unique digests across required roles, bytes present and matching | `source_row`, `source_role_missing`, `source_not_distinct`, `source_bytes_mismatch` | sources |
| V9 | Ledger continuity in decimal arithmetic from the predecessor's equity; zero adjustments; no unknown or unlinked rows; non-negative transaction-linked costs | `predecessor_equity_mismatch`, `ledger_arithmetic`, `cash_adjustments_present`, `unclassified_ledger_rows`, `trading_costs` | head |
| V10 | Transaction provenance: typed ids and digests, unique, no revisions; every retained transaction keeps its digest and session; every new transaction belongs to the proposed session | `transactions`, `duplicate_transaction_id`, `transaction_revision_detected`, `history_changed` | previous package |
| V11 | Equity at the effective close is established: under the daily-flatten basis the account is flat at capture with no fills after the close and no unresolved requests; under the venue-equity basis a `close_equity` source is present and its typed value equals the reconciled equity | `flatness_uncertain`, `venue_equity_at_close` | sources |
| V12 | The dashboard corroborates: balance equals net equity and threshold plus width equals the ratcheted peak for a current close; for a historical close the current threshold plus width is at or above the ratcheted peak | `dashboard_disagreement` | head, tier width |
| V13 | The operator attested every required fact | `attestation_incomplete` | package |

## Owner invariants (`book_settlement.SettlementStore`)

| Id | Claim | Enforcement |
|---|---|---|
| O1 | One durable state row, integrity-hashed over every field that grants authority or marks safety (account, boot, digests, enrolled keys, restore-pending, invalidated, phase) | `_state` verifies the hash; every mutation goes through `_transition` |
| O2 | The chain is a strict sequence whose rows are hash-chained and whose package and source bytes are retained and re-verified on every read | `_chain` |
| O3 | Phases: `EMPTY` → `SEATED` (B7 seal) → `ACCEPTING`; any phase → `INVALIDATED` on a revision; `INVALIDATED` → `SEATED`/`ACCEPTING` only through `resolve_invalidation` under a reviewed reconciliation; `restore_pending` is set on every restart and cleared only by `reconcile_restore` | `_transition` refuses illegal moves |
| O4 | Every boot is a new fenced owner; enrolment, calendar and policy changes across restart are audited events, never silent | boot events `trusted_keys_rotated`, `digests_rotated` |
| O5 | The B7 seal is authenticated by out-of-band seal and tool digests, the seal contract, ordered checks, distinct evidence, and re-derived C3/C4/C8; its session id names the weekday whose 17:00 ET close is the effective close | `bootstrap_b7` |
| O6 | A challenge is one-use, 300 s, bound to account, boot, halt generation, scope, sessions, predecessor digest, contract, digests and package digest; a `submit_account_close` challenge is capped by the target's cutoff; `record_only` only while HALTED | `issue_challenge`, `submit` |
| O7 | Acceptance is exactly once under one transaction; refusal advances nothing; a duplicate or out-of-order close demands a halt | `submit` |
| O8 | Only a strong, enrolled, unrevoked key with the challenge's scope and a binding for this account may sign | `load_operator_keys`, `submit` |

## Assembler invariants (`account_close_assembler.assemble`)

| Id | Claim | Enforcement |
|---|---|---|
| A1 | Every cash window is operator-attested complete from the retained query capture | `query completion not attested` |
| A2 | Rows dedupe by transaction id; same id with different content is a revision and refuses | `changed contents` |
| A3 | Every cash row maps to exactly one account session; the break, Friday evening and the weekend before the Sunday reopen map to none and refuse | `outside any account session` |
| A4 | The nominal funding row establishes the basis; any later funding, unknown type or unlinked fee refuses production | `adjustment`, `unknown`, `unlinked` |
| A5 | The running balance re-derives every reported amount | `running balance disagrees` |
| A6 | Balance history belongs to the account (Account Name) with one venue id and agrees at every row; a traded session needs its own venue row; a no-activity session settles only when the latest venue row and the dashboard agree | `different account`, `disagrees`, `lacks the venue row`, `no venue balance observation` |
| A7 | Flatness or close equity follows the verifier's V11 with the same evidence | `flatness not established`, `historical close equity evidence required` |
| A8 | Transactions carry their session id; the package carries its scope and basis | package fields |

## Calendar invariants (`book_session_calendar`)

| Id | Claim | Enforcement |
|---|---|---|
| C1 | Every Monday–Friday account day in the horizon has its own row; predecessors are exact, including the first row | `account day … missing`, `sessions[0]` |
| C2 | Every product row, permitted or denied, cites captured sources that cover that product; qualified rows also cite the product's declared spec sources; session rows cite the venue's sources | `source_ids` refusals; evidence schema v2 declares `products` per capture, v1 loads with warning `evidence_schema_v1_no_product_coverage` |
| C3 | Stored deadlines equal the section 5 formula; boundaries fall on whole minutes; admission waits for every qualified product's open | `disagree with the section 5 formula`, `whole minute`, `before_product_open` |
| C4 | Holiday facts (halts, sources, CME trade date) are explicit inputs, never inferred from another holiday | authoring tool refuses |
