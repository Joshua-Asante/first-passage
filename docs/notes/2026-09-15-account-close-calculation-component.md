# Account-close calculation component

Part of the approved PR 395 split; depends on the calendar and evidence components.
The current attended-settlement contract remains authoritative. P6 in PR 397 is
still a proposal and no automated acceptance route is added here.

## Ownership

- `account_close_evidence.py`: source identity, original bytes, parsing and coverage.
- `account_close_assembler.py`: decimal ledger reconstruction from source reports,
  account-session mapping and evidence package production. It imports no store.
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
after either B7 or an ordinary accepted close. Retained transaction IDs, contents
and session labels must remain unchanged. A newly discovered transaction belonging
to an already-settled session refuses as changed history. Later observations do
not skip settlement steps: each proposed close must still name the exact next
calendar predecessor. Current-session submissions still reject future inventory.

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

The integration workspace exercises the existing durable store calling this
calculator. That adapter is retained for the later owner slice, not presented as
a finished owner. Three known durable-owner findings remain: revised source-byte
retention, the signing timestamp's pre-challenge dependency cycle, and B7's
weekday-specific reopen boundary. Live evidence qualification remains owed.
