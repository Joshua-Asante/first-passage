# Account-close calculation component

Part of the approved PR 395 split; depends on the calendar and evidence components.
The current attended-settlement contract remains authoritative. P6 in PR 397 is
still a proposal and no automated acceptance route is added here.

## Ownership

- `account_close_evidence.py`: source identity, original bytes, parsing and coverage.
- `account_close_ledger.py`: shared decimal reconstruction and account-session
  mapping used by both producer and verifier.
- `account_close_assembler.py`: evidence package production from source reports.
  It imports no store.
- `account_close_calculation.py`: the V1–V13 package invariants, numeric limits and
  shared-policy result. It imports no signing or SQLite code.
- `book_settlement.py` (separate integration/durable-owner work): authorization,
  single-writer transaction, original evidence retention and acceptance receipt.

`calculate_close` produces immutable `ProposedClose(equity, peak, mode_next)` or
`Refusal`. `verify_package` remains available as reason-or-None. Both use the same
invariant pipeline; the store consumes the proposal rather than recalculating it.
A proposal has no receipt or activation authority. The durable owner must verify
against its current predecessor under its own transaction before accepting it.

## Corrected behavior

Fresh full history can include later missed sessions during `record_only` catch-up
after an ordinary accepted close or a B7 head with independently retained inventory.
Missing predecessor inventory refuses; the first new package cannot establish its
own baseline. The retained report timezone must match. Retained transaction IDs, contents
and session labels must remain unchanged. A newly discovered transaction belonging
to an already-settled session refuses as changed history. Later observations do
not skip settlement steps: each proposed close must still name the exact next
calendar predecessor. Current-session submissions still reject future inventory.

The verifier reparses bound cash and balance CSVs and compares the original
inventory, window row counts, classifications and derived economics with package
claims. Actual historical corrections are checked before count/span discrepancies
so stale claims cannot suppress a required halt. Historical dashboard balance
must equal the full-history ending equity; accepted peak still advances only
through the target close. Publication precedes dependent captures/signing.

`Refusal.halt_required` carries correction and ordering obligations to the owner.
This component cannot invalidate storage itself; the owner must retain the
correction evidence and enforce the halt/recovery contract.

All monetary inputs used in ledger arithmetic must remain finite when converted
to the shared policy's float representation. Equity and positive peak receive the
same check before policy evaluation. Unsupported ranges produce `numeric_range`,
not an exception misreported as storage failure. Policy constants and formulas
are unchanged.

The package schema is `account_close_package/v2`: source manifests require
per-source `account_id`, and every history window requires its source `file`.
The assembler validates aware input event times and source-account bindings
before producing the package. Legacy v1 submissions refuse; there is no implicit
upgrade or rewrite of retained history.

## Acceptance limits

The retained evidence class is operator-attested. Original source bytes and
transcribed source identities are bound, but opaque images are not automatically
interpreted or certified as final by these modules.

PR #400 owns retained B7 E3 inventory, correction quarantine and the signed
acceptance flow. It advances packages to v3 by moving signing time into the
challenge response. Live evidence qualification remains owed, including the
actual E3 format/timezone and historical close-equity capability.

The current review repairs and dependency merges pass 168 focused tests.
Independent review additionally reproduced a historical deletion hidden by stale
row counts; the added regression now returns a halt-required history refusal.
Combined owner validation and hosted checks are recorded separately.
