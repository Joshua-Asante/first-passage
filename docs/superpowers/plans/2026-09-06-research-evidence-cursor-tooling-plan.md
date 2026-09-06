# Cursor evidence validator and index Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Validate the asset inventory and render a private readable index.
**Architecture:** One standard-library command-line module reads contract-v1 JSON and explicit file members. Synthetic unittest fixtures exercise integrity checks; the tool never modifies source evidence.
**Tech Stack:** Markdown, JSON and Python 3.11+ standard library.
**Spec:** ../specs/2026-09-06-research-evidence-reorganization-design.md

## Global constraints

All boundaries in the linked approved design apply verbatim. No strategy/risk changes, private publication, source moves/deletions, baseline regeneration, replay/search/final validation, merges or deployment. User owns merges. Existing monitoring stays paused. This file is a plan, not evidence that execution has occurred.

## Task 1 — Implement and test the contract

**Create:**
- scripts/research_asset_registry.py
- tests/test_research_asset_registry.py

**Read:** linked design, scripts/check_data_manifests.py and scripts/archive_lab_analysis.py for existing conventions. Do not modify existing catalog generation or its disposition rules.

**Public interfaces:**
- `validate_registry(assets_path: Path, locations_path: Path) -> list[dict[str, str]]`: findings contain code, asset_id, member_key and message; empty means integrity checks passed. Malformed inventory yields INVALID_SCHEMA; JSON decoding/read failures are handled by the CLI as exit 2.
- `render_index(assets_path: Path) -> str`: deterministic Markdown; raises ValueError on malformed inventory/reference graph.
CLI:
```text
python scripts/research_asset_registry.py validate --assets PATH --locations PATH
python scripts/research_asset_registry.py index --assets PATH
```
Validate prints a JSON object with schema_version equal to 1 and findings containing the returned array; exit 0 when empty, 1 for integrity findings, 2 for usage/unreadable JSON. Index prints Markdown to stdout; exit 2 on malformed inventory. Only the caller redirects output to an explicitly chosen private destination. Neither command writes evidence or changes admission.

- [ ] Write synthetic unittest fixtures with tempfile.TemporaryDirectory, hashlib and JSON. Start with a minimal asset whose member contains the bytes b"synthetic source". Use the contract's required fields and a root pointing to the temporary directory.
- [ ] Add the concrete hash-mutation regression below before implementing the tool; run it and record the expected import/missing-function failure.
```python
def test_mutated_member_is_reported(self):
    assets_path, locations_path, member_path = self.make_registry()
    self.assertEqual(validate_registry(assets_path, locations_path), [])
    member_path.write_bytes(b"changed")
    findings = validate_registry(assets_path, locations_path)
    self.assertIn("HASH_MISMATCH", {item["code"] for item in findings})
```
Use this concrete fixture method in the unittest class (imports: tempfile, hashlib, json and pathlib.Path):
```python
def make_registry(self):
    temporary = tempfile.TemporaryDirectory()
    self.addCleanup(temporary.cleanup)
    root = Path(temporary.name)
    member = root / "source.txt"
    payload = b"synthetic source"
    member.write_bytes(payload)
    assets = root / "assets.json"
    assets.write_text(json.dumps({"schema_version": 1, "assets": [{
        "id": "example-source-v1", "kind": "source",
        "label": "Synthetic source", "privacy": "private",
        "members": [{"key": "body", "sha256": hashlib.sha256(payload).hexdigest()}],
        "parents": [], "supersedes": [], "claims": [],
        "limitations": ["Synthetic fixture only"]
    }]}), encoding="utf-8")
    locations = root / "locations.local.json"
    locations.write_text(json.dumps({
        "schema_version": 1, "roots": {"test": str(root)},
        "locations": [{"asset_id": "example-source-v1", "member_key": "body",
                       "root": "test", "relative_path": "source.txt"}]
    }), encoding="utf-8")
    return assets, locations, member
```
- [ ] Add cases for duplicate IDs/member keys/location tuples, invalid hash/type/enum, missing evidence references, self-links/cycles, unknown roots, missing members/files, absolute or parent-traversal paths and empty claim evidence. Prove that multiple valid locations for one member succeed.
- [ ] Implement schema/reference validation first, then explicit path resolution and streaming SHA-256. Resolve roots and members before checking containment; reject paths escaping through symlinks/junctions. Test symlink behavior where permitted and report an explicit skip where the OS disallows creation.
- [ ] Use stable finding codes: INVALID_SCHEMA, DUPLICATE_ID, DUPLICATE_MEMBER, DUPLICATE_LOCATION, MISSING_REFERENCE, RELATIONSHIP_CYCLE, MISSING_LOCATION, UNKNOWN_ROOT, UNSAFE_PATH, MISSING_FILE, HASH_MISMATCH, UNREADABLE_FILE. Findings must identify the affected asset/member without exposing absolute paths.
- [ ] Implement deterministic index output sorted by kind then ID. Show IDs, labels, privacy, member hashes, parent/supersedes IDs, claims/evidence IDs and limitations. Escape Markdown labels; do not interpolate HTML or machine-specific paths. State that an integrity pass is not admission or source parity.
- [ ] Add tests proving a passed synthetic_tests claim is displayed only as that scope; pending/failed claims stay visible; the renderer does not invent qualification/readiness. Verify identical inputs render identical output.
- [ ] Add subprocess CLI tests for success, integrity failure and unreadable JSON, checking exit codes and parseable output. Check input bytes before and after both commands are unchanged.
- [ ] Run the focused suite:
```text
python -m unittest discover -s tests -p test_research_asset_registry.py -v
```
Use the repository-supported Python 3.11+ interpreter. Record its actual version, command, counts and exit code. No package installation is needed.
- [ ] Review only the two intended files, then commit those exact paths on an isolated implementation branch:
```text
git add scripts/research_asset_registry.py tests/test_research_asset_registry.py
git commit -m "Add read-only research asset inventory validation"
```
Do not publish private inventory or change unrelated tests/tooling.
- [ ] Return commit, file list, test evidence and any explicit platform test skips for Codex integration.

## Acceptance and stop

Synthetic fixtures pass the specified integrity and non-mutation checks. No private input is necessary. No database, web UI, dependency installation, downloader, directory crawler, automatic status promotion, backup automation or new catalog. One tooling pass and one focused correction pass for acceptance defects.
