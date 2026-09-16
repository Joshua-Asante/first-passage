# Revision-bound offline owner fixtures

These are logical SQLite exports created with each revision's original public owner, broker, protection and takeover APIs. `manifests.json` records the recognized schema revisions; each fixture repeats its exact source SHA and includes a SHA-256 over canonical sorted-key compact JSON of its `tables` object. Original bodies remain strings, preserving their bytes. BLOBs use a tagged `sqlite_blob_hex` object and are restored as bytes.

Sources:

- Schema 1: `fc7cdc7`, original owner/dispatch/observe and completed-takeover APIs.
- Schema 2: `567a583`, original occurrence-aware APIs and `ProtectionScenario`.
- Schema 3: `b5fdde8`, committed Slice C and `TakeoverScenario`/`ready_without_attempt`.

The export process used `git archive` to isolate each source's `ops`, `core`, and `tests/ops` trees, then a separate Python process with only those source layer paths. No current owner opened the source databases. The `test_book_bootstrap_migration.restore_fixture` loader recreates SQL and rows directly before calling the explicit converter.

`amend_accepted`/`amend_unknown` exercise actual legacy command outcomes in schema 1. Under schemas 2/3 these represent prepared amendments awaiting independent evidence; the `consumed_pending_accepted`/`consumed_pending_unknown` fixtures cover actual attempted B amendments, followed by a protection execution that consumed the owner while retaining the separate pending mutation and deadline. `attached_settlement` comes from the original signed synthetic close integration test and contains synthetic settlement sources, not live account data.

Never regenerate these fixtures from the current owner or silently alter their source hashes to make conversion pass. Add an explicitly recognized source manifest for a different historical layout.

`2-live_pending_unknown` adds a nonconsumed, actually attempted schema-2 amendment. Its `resolution_snapshot` metadata is produced by the original broker after applying that command. The conversion test observes it, observes a later snapshot with no repeated operation outcomes, and restarts without losing the earlier proof or gaining send authority.
