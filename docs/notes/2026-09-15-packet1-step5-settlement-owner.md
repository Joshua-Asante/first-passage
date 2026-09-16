# Settlement owner: retained operator enrollment record

This record preserves the enrollment provenance from PR #395 at `bd41cb6`.
The component extraction omitted the original note while retaining its reference
in `ops/c1_rail/operator_keys.json`. Restoring this record does not enroll a new
key, expand its scopes, or repeat the operator action.

## Operator key enrolled — 2026-09-15

The original record states that the operator generated an Ed25519 keypair on
their own device and confirmed the public key in chat ("confirm"). The private
key remained on that device, outside the repository and runtime.

The public key is
`1f75cea0c36941f8964d393490b6886bcbcdb010b4bc67dd45e925d1a04604aa`.
The tracked enrollment timestamp is `2026-09-15T12:05:00Z`; scopes are
`submit_account_close` and `record_only`, with account binding at runtime.
The append-only enrollment/revocation registry remains
[`operator_keys.json`](../../ops/c1_rail/operator_keys.json).

## Current implementation and qualification

The [owner component record](2026-09-15-account-close-owner-component.md) and
[invariant table](2026-09-15-packet1-step5-invariant-table.md) describe current
behavior. Earlier synthetic or private-report qualification in the original PR
does not establish acceptance of this revised protocol. Actual source
qualification, listener integration and combined Step 6 acceptance remain open.
