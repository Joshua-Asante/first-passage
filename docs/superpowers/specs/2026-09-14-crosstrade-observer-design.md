# CrossTrade read-only observation collector

Approved by Joshua in this task after the support-free capability investigation.
This implements the approved collector scope, not a relaxation of E1–E3.

One-shot CLI runs collect snapshots, account orders/positions/fills, and bounded
paginated durable history through fixed CrossTrade HTTPS GET routes. A private
SQLite journal retains each response, collection state, and fill revisions.
Repeated invocation uses the same account-bound journal. No daemon, WebSocket,
order mutation, RecoveryOwner conversion, deployment or resume API is added.

Use Python 3.11+ standard library. The collector owns observation persistence;
CrossTrade owns source facts. A local run/observation ID is not a broker cursor.
`E1`, `E2`, and `E3` always remain `unproven` in exported summaries.

HTTP errors, malformed/oversized JSON, redirects, partial/unavailable sections,
account mismatches, cached snapshots, repeated cursors and bounded truncation must
be visible. Optional null fields never become zero. Exhausted history pagination
means only the end of currently stored rows. No automatic retry of failed reads.

Retain timestamped raw JSON observations (with the credential removed) separately
from fill revision classification. Stable execution IDs deduplicate observations;
fee-only changes are revisions; changed economic facts are conflicts. Preserve
both versions. A completed run means collection finished, never recovery complete.
Interrupted runs remain identifiable after restart and are not resumed as if
complete. SQLite transactions commit each observation and its revisions together.

CLI consumes a local config path with `account`, `destination=tradovate`, and
`secret_key`; prints redacted counts/status/limitations only. Never print config,
tokens, account IDs, response bodies, URLs containing account names, or exception
messages. Store private databases in an ignored `.crosstrade-observer/` directory;
back up the database. Do not put credentials in command-line arguments.

Validation covers real SQLite reopening, page cursors, duplicate/conflicting
identities, fee revisions, malformed envelopes, missing coverage, bounded failure,
redirect prevention and credential redaction. Transport fixtures are synthetic,
not E1–E3 qualification. A read-only live smoke may reuse the existing credential
in place and return a private journal locally without writing the production host.
