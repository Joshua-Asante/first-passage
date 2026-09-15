# Attended account evidence and settled-close contract

Status: OPERATOR-APPROVED DESIGN, 2026-09-15 UTC. Owner: Packet 1 coordinator (TB-T1/TB-C1);
integration owner: TB-I3 account owner. No runtime authority is granted by this
document. Joshua approved this design: “yes, i approve the design.” Implementation
and actual source qualification remain open. This extends ongoing settlement; it does not replace
the initial [B7 snapshot contract](2026-09-12-tradeify-account-snapshot-seal-contract.md).

## Grounding and resolved distinctions

Inspected at `821ee9044712a766f03cb798fed32f29153d064c` plus the existing Packet 1
working changes: `ops/c1_rail/book_policy.py` (`BookProtectionClock`),
`ops/c1_rail/book_sizing_context.py` (`SettledClose`, `_session_mode`),
`core/firm_rules.py`, TB-S1 section 3, and the B7 C1–C10 contract.
Actual report headers and access are retained in the
[producer probe](../notes/2026-09-15-packet1-producer-feasibility.md).

1. **Initial peak:** B7 derives it from the Tradeify dashboard threshold and the
   kernel width. Statements never reconstruct that initial peak (D23).
2. **Subsequent peak:** apply the existing `BookProtectionClock` EOD ratchet,
   `max(previous accepted peak, accepted close equity)`. Do not reset it from
   intraday equity or a later lower dashboard threshold. Dashboard evidence is
   a cross-check; disagreement blocks acceptance.
3. **Account close is not an instrument settlement price.** Neither CME settlement
   prices nor a sum of observed fills can supply a missing venue account close.
4. **Effective time is not capture time.** `SettledClose.as_of` means the verified
   effective account-close instant. Retain source publication time when supplied,
   capture time, operator signing time and server receipt time separately. Never
   backdate receipt or invent a publication timestamp.
5. **Trading day is not always CME trade date.** Tradeify describes independent
   18:00–17:00 ET account days, including holiday half-days. The retained CME
   September 7 product rows instead bear September 8 business trade dates. A
   broker CSV `Date` cannot be copied blindly into the portfolio session key.

The approved clarification of TB-S1's “exchange-session order” wording is:
use a source-backed account session key
for protection, with explicit CME business-date mappings per product/matching
interval. Retain every mapping in the calendar digest. This is not permission to
infer weekday sessions or collapse holiday intervals.

Sources: [Tradeify trading day](https://help.tradeify.co/en/articles/10468225-what-is-a-trading-day),
[permitted times](https://help.tradeify.co/en/articles/10495876-rules-permitted-times-to-trade),
[dashboard update behavior](https://help.tradeify.co/en/articles/12268494-common-faqs),
[Tradovate report definitions](https://partner.tradovate.com/resources/admin-dashboards/reports).
These establish source semantics, not completeness of the captured account history.

## Evidence package

Every package binds the exact private account identity and venue, contract version,
accepted calendar digest, account-session key and predecessor key, predecessor
settlement digest, source files and computed hashes. Preserve original bytes.

| Evidence | Initial B7 | Each subsequent close |
|---|---|---|
| Tradeify dashboard | Existing E1 fields and capture rules | Balance, trailing threshold and account identity, captured after the relevant update; discrepancy blocks |
| Tradovate positions and working orders | Existing E2: flat and no working orders | Current complete account-wide view; also disclose all unresolved requests in the runtime journal |
| Balance/equity history | Corroborates E1; does not supply initial peak | Source-backed equity at the effective account close; balance may substitute only with evidence of flatness at that same boundary |
| Cash history | E3 from established evaluation inception through capture | First-release protocol re-queries inception through current capture in bounded ranges, comparing previously retained records to expose later corrections |
| Query evidence | Account, selected range, timezone and completion/result state | Same, including empty result ranges; a missing CSV row is not proof of no activity |

Establish inception from account lifecycle evidence; the first zero-P&L balance
row alone is insufficient (“usually” an opening date in the report documentation).
Initial nominal account funding must be identified as establishment of the frozen
basis, not silently excluded as a deposit. Any ambiguity requires adjudication;
later deposits, resets, withdrawals or adjustments are outside this kernel.

Use bounded cash-history queries: the observed 14-day request worked; the annual
request was rejected. A production collection protocol must demonstrate its
chosen range limit and endpoints. Adjacent queries overlap for verification;
identical transaction IDs and contents are deduplicated **during collection**.
Same ID with changed contents is retained as a revision and blocks acceptance.
An added or removed historical transaction also requires reconciliation; unchanged
IDs alone do not establish an unchanged history.
This does not weaken TB-S1's duplicate/out-of-order settlement refusal.

Record the displayed report timezone and retain both raw and normalized timestamps.
Reject ambiguous or nonexistent local times unless the source resolves the offset.
Account-wide evidence includes all instruments and manual activity, not only book
legs. An instrument filter cannot establish a complete cash ledger.

A later flat snapshot cannot establish effective-close flatness. If positions
were carried or their boundary state is uncertain, require venue-backed equity
at that close, including its valuation basis; otherwise refuse. The report samples
observed so far do not establish such a historical-equity capability. Do not
reconstruct it from current marks or assume the daily flatten succeeded.

### Trading costs versus cash adjustments

The venue's [all-in commission schedule](https://help.tradeify.co/en/articles/10468315-trading-commission-fees)
includes commissions, exchange, clearing and NFA fees. Approved C8 clarification:
these identifiable transaction-linked trading costs are included once in net
account equity; they are not external capital adjustments merely because the
CSV records separate fee types. Never subtract them again from an already-net
balance. The B7 owner records this same classification; its zero-adjustment rule remains.

Deposits, withdrawals, manual corrections, account resets, subscription charges
debited to trading cash and unclassified fees remain adjustments/unknowns. Sum
absolute amounts, not signed net; a nonzero adjustment or unknown classification
refuses production. An unlinked “fee” is not automatically a commission. Verify
ledger continuity with decimal currency arithmetic and reconcile to the reported
balance; arithmetic agreement alone does not prove source completeness.

## What counts as an accepted close

The allowed evidence class is **operator-attested, evidence-backed account close**,
not machine-certified broker finality. The operator reviews a complete package
for a finished, explicitly mapped account session and signs that the source
reflects that close, includes its costs/adjustments, and has no known pending
correction or conflicting observation. The verifier must check identities, source
hashes, coverage, arithmetic, prior-state chain, timestamps and the attested fields.
It cannot infer an absent fact from the signature.

No elapsed-time rule creates finality. In particular, two equal polls, a flat
snapshot, successful HTTP response, “after 8 PM,” or a generic dashboard update
window is insufficient. If the source cannot distinguish the relevant account
close or resolve pending corrections, no `SettledClose` is produced. Qualification
must demonstrate this evidence protocol on the actual account before deployment.

The current consumer requires the effective close to precede the next session's
open. Later capture/receipt is represented honestly and cannot retroactively
authorize orders. A session cannot admit risk until its exact preceding close
has been accepted and ordinary activation/resume gates pass. Late submission
does not replay missed signals or switch an already-active session's mode.
This contract does not amend B7's stricter capture-boundary/expiry or n3 gates.

Both submission scopes below require newly captured supporting reports and
current account views no more than 30 minutes old at server receipt, with capture
times not in the future. Historical effective-close times remain historical;
retained old files support provenance but cannot replace the fresh full-history
query. This is the approved ongoing-evidence freshness bound, distinct from the B7
capture-to-seal rules and the runtime's tighter live account-observation limits.
Clock uncertainty that prevents verification refuses acceptance.

## Authenticated submission and durable acceptance

Approved first-release mechanism: a dedicated operator signing key, with the
public key enrolled in the runtime's trusted configuration and scoped to
`submit_account_close` for this account. Provisioning remains a separate setup
action. No webhook/broker secret or caller-supplied `operator_id` authenticates a
submission. The private key stays on the operator device, outside the daemon,
repository and evidence files.

The runtime issues a short-lived, one-use challenge bound to account, owner boot
epoch, current halt generation, proposed session/predecessor, contract/calendar/
policy digests and evidence-package digest. The operator signs that exact envelope.
Approved challenge lifetime is 300 seconds from server issue time (a new protocol
choice, not an existing runtime setting or a claim about source freshness).
For a current-session submission, `target_session_id` identifies the next session
whose mode will consume the close; expiry is also capped by its risk-add cutoff.
Refuse unknown key/scope, changed evidence,
expired challenge, wrong account/boot/generation or replay.

For historical catch-up, use a distinct signed `record_only` scope while HALTED.
`target_session_id` is absent; the close's historical account-session key remains
explicit. Its fresh challenge expires 300 seconds after current server issue time,
not at a historical cutoff. Accept missing sessions individually in predecessor
order with full source evidence. Update only the recorded close chain and derived
next-mode candidate; never active mode, activation authority or missed signals.
Return remains HALTED. Once caught up, current evidence and a separate fresh
activation/resumption approval are still required. This path cannot repair a
corrected accepted close by submitting it as a duplicate.

Under the account owner's single-writer transaction:

1. Verify signature, challenge, source bytes and all package checks.
2. Compare predecessor digest and session against durable state and the accepted
   calendar. Missing intervening account sessions must be resolved individually;
   no fabricated flat-day settlement.
3. Append the immutable package and acceptance/refusal event; atomically consume
   the challenge and update the accepted-close chain on success.
4. Derive peak and next mode from the existing shared policy. Persist the complete
   verified `SettledClose`; supply that exact record to `BookSizingBinding`.
5. Return a durable receipt. Lost receipt does not permit another acceptance;
   the client uses a read-only status query. A fresh duplicate or out-of-order
   settlement submission follows TB-S1's halt rule.

Settlement acceptance cannot acknowledge an incident, clear a halt, release an
uncertain reservation or authorize risk. Those remain the separately authenticated
activation/resume and qualified reconciliation gates.

### Corrections and restore

Never overwrite accepted evidence or feed an old corrected session through the
normal forward-only settlement path. A changed prior record invalidates dependent
settlements, modes and unused activation/resume approvals and halts new risk.
Preserve both versions and the dependency chain. Resolution needs reviewed
reconciliation and separate resumption; it does not rewrite historical actions.
A restore begins halted and must reconcile its durable chain and challenge state
before accepting another close. No second account writer is permitted.

## Required acceptance traces

| Trace | Required result |
|---|---|
| Complete regular close; valid signature; exact predecessor | One durable accepted record; shared-law next mode; no risk authorization |
| Holiday half-day whose cash CSV business date is next day | Explicit account-session mapping; no invented close or weekday key |
| Initial B7 and later close | B7 initial peak retained; subsequent peak ratchets only on accepted closes |
| Fee split across commission/exchange/clearing/NFA rows | Net equity reconciles without double deduction; unknown/unlinked fee refuses |
| Offsetting deposits/withdrawals | Refusal despite zero net |
| Empty history or missing day | Require query coverage and source close; do not copy previous balance |
| Current flat view but uncertain exposure at effective close | Refuse balance-as-equity; require effective-close equity/flatness evidence |
| Several missed sessions with expired historical cutoffs | Fresh record-only challenges, individual predecessor order, remain HALTED; no expired-session authority |
| Late report or dashboard disagreement | Block until actual evidence resolves; no stale-mode trading |
| Same transaction ID revised; accepted close corrected | Both versions retained; dependencies invalidated; halt |
| Wrong key/account/boot/calendar, expired/reused challenge | Refuse; no state advance |
| Concurrent submissions, crash around commit, lost receipt, restore | Exactly one acceptance, durable history, no duplicate authority |
| Valid settlement while halted | Remains halted; acknowledgment/resume are separate |

## Remaining implementation and qualifications

The approved account-session mapping, C8 trading-cost classification and
authenticated submission design are reconciled into TB-S1, B7 and the umbrella.
They change no sizing constant or accepted strategy. Implement and test this
protocol through the real durable account owner before accepting any close.
Actual account inception/complete-history and close-update evidence remain required;
today's sample reports do not discharge them. A reviewed contract is not a qualified
producer, and a qualified producer is not deployment approval.
