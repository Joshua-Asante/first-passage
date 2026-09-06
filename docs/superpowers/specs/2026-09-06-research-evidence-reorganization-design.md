# Research evidence reorganization — approved design

Approved by the operator on 2026-09-06: three ownership lanes, one inventory pass, minimal tools, one integrated review. This document records that approval; the accompanying plans supply execution details.

## Outcome

A new session can locate exact strategy versions, evidence, limitations and current campaign instructions without reconstructing chat history. Reuse existing catalog conventions. Add a private asset inventory beneath the existing study, not a new root-level catalog or a replacement research platform.

## Boundaries

- Preserve original files, frozen manifests, receipts and historical decisions.
- No source moves, deletions, baseline regeneration, replay implementation, search, final validation, merge or deployment.
- No changes to strategy membership, risk criteria, statistical budgets or campaign admission policy.
- Private sources, settings, datasets, paths and populated records stay local/private.
- Public tooling and fixtures contain synthetic data only.
- One owner per mutable output; no worker changes another lane's files.
- Validation checks record integrity; it never admits an asset or certifies a strategy.
- One inventory pass, one tooling pass and one integrated review; one bounded correction pass for concrete acceptance failures. A new service, new dependency or broader migration requires an explicit scope decision.
- Existing PR monitoring remains paused. User retains merges.
- Record missing backup protection honestly; local retention is not a verified backup.

## Ownership

Codex: contract, current campaign instructions, read-only integration checks, privacy review, admission references, final acceptance and backup coordination.
Claude (local): populated private inventory and evidence coverage report.
Cursor: source-neutral validator, generated index renderer and synthetic tests.
Claude and Cursor work concurrently only after reading this exact contract. No alternate schemas.

## Storage and authority

The study audit directory is:
`.superpowers/sdd/2026-09-02-seven-strategy-tradeify-select-configuration/`.

Add only `reorganization/assets.json`, `locations.local.json`, `inventory-report.md`, `INDEX.generated.md`, `integration-report.md` and `backup-receipt.json` beneath it during execution. The existing directory's ignored status must be verified before writes.

Stable IDs identify immutable logical versions and do not contain drive paths. SHA-256 identifies bytes, not semantic equivalence. Two exports with different settings are distinct versions even when their bytes happen to match; identical copies can share a file asset and have multiple locations. Never delete duplicates.

Keep original evidence authoritative. The inventory is a locator and claim index, not a replacement verdict. The current campaign instructions remain in the existing campaign-state document; its new current section identifies superseded operational instructions explicitly. Preserve historical rulings in place. STATE and CATALOG retain their existing roles. Do not edit generated CATALOG by hand.

## Record contract v1

UTF-8 JSON, standard-library compatible, no database or external dependency.

assets.json:
```json
{
  "schema_version": 1,
  "assets": [{
    "id": "example-source-v1",
    "kind": "source",
    "label": "Synthetic source version",
    "privacy": "private",
    "members": [{"key": "body", "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}],
    "parents": [],
    "supersedes": [],
    "claims": [],
    "limitations": ["Synthetic example only"]
  }]
}
```

Allowed kinds: source, configuration, trade_export, bar_dataset, component, evidence.
Allowed privacy: private, public.
Required fields shown above; strings nonempty, IDs unique, member keys unique per asset, hashes lowercase 64-character hex, arrays explicit.
A bundle may contain multiple file members. No directory hashing or implicit recursive membership.
Relationships use asset IDs. Self-links, missing references and cycles in parents or supersedes are errors.
An evidence file is itself an asset with kind evidence and an exact hash.
A claim is:
```json
{
  "scope": "synthetic_tests",
  "result": "passed",
  "evidence_ids": ["example-test-log-v1"],
  "limitations": ["Does not establish source parity"]
}
```
Allowed scopes: identity, capture_completeness, coverage, accounting_reconciliation, synthetic_tests, source_parity, review.
Allowed results: passed, failed, partial, pending, unknown.
Claims require nonempty evidence_ids referencing evidence assets, including pending/unknown claims if explicitly recorded. If no evidence exists, omit the claim and state the gap in limitations.
These are descriptive observations. They are not a new campaign terminal taxonomy. A passed review or test does not imply parity, qualification or admission.

locations.local.json:
```json
{
  "schema_version": 1,
  "roots": {"private_store": "C:/synthetic/example"},
  "locations": [{
    "asset_id": "example-source-v1",
    "member_key": "body",
    "root": "private_store",
    "relative_path": "source.txt"
  }]
}
```

Every member needs at least one location. Multiple copies are permitted; every listed copy is checked. Location tuples must be unique.
Roots are explicit absolute local paths. Relative paths must not be absolute, contain parent traversal, or resolve outside the declared root, including through symlinks/junctions. Paths are held only in the private location file. No downloads or filesystem scans outside listed members.
A missing file, hash mismatch or unknown root is an error. The tool does not repair it.
Use at most one streaming hash read per resolved file per run.

## Campaign view

The current campaign section links the private inventory by local reference and identifies:
objective; accepted decisions and their authority; assets used and admission references; blockers; owner; acceptance check; next milestone; stopping conditions.
Do not copy private parameter values into tracked documents.
Unresolved decisions remain unresolved. Apparent contradictions are reported, not silently adjudicated by workers.

## Verification and stopping point

Integrity tests cover malformed schema, duplicate IDs, missing references, cycles, missing locations/files, mismatched hashes and unsafe paths. A deterministic Markdown index groups assets by kind and displays claims, evidence IDs, limitations and relationships without local absolute paths. It has no overall readiness score.

Integration must answer: exact configuration-to-export binding; old versus complete Aegis candidate; ORB demonstrated capability and reached blocker; how to resume. Hashes and source files remain unchanged.

Private backup: identify an operator-approved destination, verify it is outside the source worktree, copy without overwriting originals, hash-check the copy and restore representative registry/evidence files into a separate temporary directory. Do not purchase storage or upload private data without destination authorization. If no destination is established, mark backup pending and do not claim durable preservation. Inventory/tooling can still be accepted separately.

