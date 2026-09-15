# Account-close evidence component

Part of the operator-approved PR 395 split. This component has no calendar,
signing, policy, or database dependency. It neither proposes nor accepts a close.

## Contract

`ops/c1_rail/account_close_evidence.py` owns `SourceFile`, cash/balance parsing,
source manifest validation and history-window coverage validation.

- `SourceFile.account_id` is transcribed from the account identity displayed in
  that particular retained view or query capture. Missing/foreign identities
  refuse; do not fill this field from the requested account or a filename.
  Cash and balance CSV account columns are also checked by their parsers.
- Opaque dashboard, position/order, inception and close-equity captures still
  need operator extraction. These interfaces do not perform OCR or establish
  machine-certified source finality. Qualification must demonstrate that each
  transcription is supported by its retained original capture.
- All input event times must be timezone-aware before UTC normalization. Each
  cash row must exist by its own source capture, including duplicated rows.
- The supported collection contract binds UI date labels to transaction
  timestamps in the displayed report timezone, matching the assembler's UTC
  coverage intervals. Rows outside those labels refuse; the CSV business `Date`
  does not override them. Actual venue query-filter semantics must be demonstrated
  during source qualification. If the venue filters on another date basis, this
  collector must refuse until a reviewed explicit coverage mapping is supplied;
  this component does not claim that capability already exists.
- Each history window names its retained source `file`. Every cash source is
  bound exactly once; a dashboard cannot stand in for a cash query. Coverage
  reaches continuously from inception to the terminal cash capture and no
  window extends beyond its own capture.
- The window limit counts local calendar dates in `report_timezone`; an
  exclusive midnight endpoint does not add another date. Autumn DST therefore
  does not turn a valid 14-date query into an oversized one.
- Sources require account-bound manifests and original bytes matching their
  SHA-256. A historical close-equity artifact must be distinct from every other
  artifact, regardless of manifest order. Separate cash queries may have
  identical empty CSV bytes; their file names and query metadata remain distinct.

`verify_source_manifest` returns a role-to-source mapping or a refusal string.
`verify_history_coverage` returns None or a refusal string. They verify structural
consistency of the submitted evidence; matching hashes do not prove that a view
contains the operator's asserted values or that a query was actually complete.
The existing attended evidence contract and real-source qualification remain
required. P6 in PR 397 does not authorize automatic acceptance.

## Integration

The calculation/assembler component consumes this module. Package source rows
gain `account_id`; coverage rows gain `file`. The calculation component labels
that stronger input contract `account_close_package/v2` and refuses v1 submissions
instead of inventing the missing bindings. Existing historical evidence is not
rewritten by this component.

## Verification

Standalone tests cover source identity, role/file binding, digest independence,
identical empty cash exports, DST/date limits and per-file capture chronology.
Producer-to-verifier and durable-owner integration are tested in the dependent
calculation/integration workspace. No live source collection or trading occurred.
