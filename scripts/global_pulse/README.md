# Global Pulse observation bridge (packet v1)

Explicit inputs → immutable local capture → editable Notice → supplied routing.
This records observations for research triage; it does not test or admit them.
The [Notice template](../../.claude/skills/brief-authoring/references/notice_log.md)
owns narrative routing. The [asset registry](../research_asset_registry.py) checks
configuration/dataset identity and locator integrity; the
[evidence store](../evidence_store/README.md) preserves explicitly captured sources.
Neither is a research-admission gate.

## Watchlist integration dependency

At implementation, GitHub PR searches for `Global Pulse`, `pulse` and `watchlist`,
the latest 30 updated PRs, and default-branch code search returned no Global Pulse
registry or PR. Main was `2cfb3d728076cce7ede31c916eb5b2f214aeedd4`.
The other session's symbol-map/watchlist work remains the production authority;
no production symbols are defined here. Compatibility is **pending**, not assumed.

The only adapter currently accepts the explicitly synthetic registry schema
`global-pulse-synthetic-registry/v1` in
[fixtures/registry.json](../../tests/global_pulse/fixtures/registry.json).
Production-shaped or non-synthetic registries fail with an actionable error.
This keeps the bridge independently testable without silently adopting unmerged
definitions. Before production use, link the watchlist PR in the bridge PR,
replace `registry_rows()` with an adapter for its approved schema/path and stable
IDs, and add tests against its exact approved revision. Carry its units,
transformation, proxy, roll, timing and age policies through unchanged. Do not
turn this fixture schema into a competing symbol registry. The binding resolver
already accepts exact file-content SHA-256 pins, retaining the original bytes;
it does not fetch Git revisions or infer approval from a digest.

## Packet contract

[packet.json](../../tests/global_pulse/fixtures/packet.json) is a complete synthetic
input. `bridge.validate()` is the executable v1 schema: all listed fields are
required, extra fields and duplicate JSON keys fail. Optional values use explicit
`null` or empty arrays. Schema evolution requires another version.

| Field | Contract |
|---|---|
| `schema_version`, `observation_id` | Integer 1; `GP-YYYY-MM-DD-slug`, unique and immutable within the capture root. The ID date is a label, never a substitute for availability. |
| `author`, `source`, `captured_at` | Named author/process, source context, explicitly supplied capture timestamp with timezone. Actual evidence-store recorded time stays separate. |
| `watchlist` | Relative `path` under `--input-root` and exact raw-file `sha256`; source bytes retained verbatim. |
| `measurements` | Unique measurement `id`, stable `series_id`, finite numeric `value`, output `unit`, `convention_id`, exact registry `definition`, `window_start`, `window_end`, `observed_at`, nullable `published_at`/`available_at`, and nonempty `evidence_ids`. Values may be levels or changes; the pinned convention defines the transformation and output units. |
| `evidence` | Unique `id`, native asset-registry `kind` (e.g. `bar_dataset` or `evidence`), relative local `path`, `sha256`, `provider`, `source_reference`, nullable `evidence_store_version`. Every supplied file is checked and retained. |
| `interpretation` | Separate plain `observation`, stated `baseline`, measured `departure`, `why_stands_out`, and optional `candidate_explanations` array. These are authored statements, not computed findings. |
| `limitations` | Explicit missing inputs, delays, proxy/coverage concerns and uncertainty. Validator adds timing, proxy, roll and age disclosures without assigning quality scores. |
| `prior_exposure` | `status`: `unknown`, `none`, or `declared`; explanation `note`; `windows` with timezone-aware `start`, `end`, `activity`, `series_ids` for declared exposure. `none` and `unknown` have empty windows. Describe partial knowledge in the note rather than claiming untouched history. |
| `lineage` | Arrays `observations`, `notices`, `investigations`; supplied references only, not inferred dependency edges. |
| `correction` | Null, or `predecessor_id`, SHA-256 of retained canonical `packet.json` in `predecessor_sha256`, and nonempty `changes` array identifying corrections. New ID required; predecessor must exist and verify in the same root. |

Times describe completed observations: window start ≤ window end ≤ observation
time ≤ capture time. When known, observation ≤ publication ≤ availability ≤
capture; either unknown time remains `null`. Forecast/future-period measurements
need a later schema with distinct target time. Daily and live observations keep
their individual times. Age is measured at the supplied capture time, not now.
Declared series-specific maximum ages produce limitations, never universal
staleness rejection. Without a policy, age and uncertainty are reported.

Validation proves structure, declared conventions and retained-byte identity.
It does not independently recalculate measurements, authenticate a vendor,
prove timing claims or establish statistical independence. Baseline input values,
transform parameters and source rows must be supplied in definitions/evidence for
reconstruction. Missing historical availability permits capture but remains a
limitation for downstream testing. Unknown exposure is not an untouched holdout;
systematic scans still need their owners' trial accounting. No trial count is
assigned here.

## CLI and synthetic end-to-end example

From the repository root, run the required launcher (`.\fp.ps1` on PowerShell;
portable form below). The fixture is entirely invented, with two series rather
than a substitute for the production 20-series watchlist.

```sh
python -I scripts/fp.py doctor
python -I scripts/fp.py python -m scripts.global_pulse validate --packet tests/global_pulse/fixtures/packet.json --input-root tests/global_pulse/fixtures
python -I scripts/fp.py python -m scripts.global_pulse capture --packet tests/global_pulse/fixtures/packet.json --input-root tests/global_pulse/fixtures
python -I scripts/fp.py python -m scripts.global_pulse draft --bundle local_artifacts/global-pulse/GP-2026-10-10-synthetic-divergence
```

Exit 0 means valid (including limited evidence); JSON `limitations` remains
visible. Malformed inputs or integrity failures exit 2 with a JSON error on
stderr. `validate` is read-only. Capture writes below the existing ignored
`local_artifacts/global-pulse/` by default; `--output` explicitly selects another
approved private root. Capture retains:

- Canonical `packet.json`, exact `registry.json`, `artifact-N.bin` in packet
  evidence-array order, and `validation.json` limitations.
- Native `assets.json` and `locations.json`: configuration, dataset and packet
  identities with hashes, no claims or inferred parents/dependencies.
- `notice-draft.md` only when `draft` is requested.

Capture writes a temporary directory then publishes it under a writer lock.
Identical same-ID capture is idempotent; different content fails and requires a
new correction ID. `verify` works after the original inputs disappear. Keep the
whole directory backed up. Locations are absolute private locators: after moving
a capture root, deliberately update `locations.json` to the approved new root
and verify it. Existing snapshots and their hashes remain unchanged. A stale
`writer.lock` requires confirming no writer is active before manual removal.
Local file/directory publication is not a distributed-store or signed audit-log
guarantee; interruptions during Notice writes can leave a partial file that must
be reviewed, never automatically overwritten.

Edit the Notice draft, preserving its identity, status and routing markers.
Finalization preserves edits outside the marked routing block; that block is
replaced with the explicitly supplied decision. The fixture's
[hold.json](../../tests/global_pulse/fixtures/hold.json) provides a condition-based
HOLD, with no invented date or reminder:

```sh
python -I scripts/fp.py python -m scripts.global_pulse finalize --bundle local_artifacts/global-pulse/GP-2026-10-10-synthetic-divergence --routing tests/global_pulse/fixtures/hold.json --notice-dir local_artifacts/global-pulse/notices
python -I scripts/fp.py python -m scripts.global_pulse verify --bundle local_artifacts/global-pulse/GP-2026-10-10-synthetic-divergence
python -I scripts/fp.py python .claude/skills/brief-authoring/scripts/check_brief.py local_artifacts/global-pulse/notices/N-2026-10-10-synthetic-divergence.md --type notice
```

The public narrative convention is `docs/notes/notice/N-YYYY-MM-DD-slug.md`.
Choose `--notice-dir docs/notes/notice` only for a Notice reviewed for publication;
licensed data, sensitive observations and artifacts stay in approved private
storage. This example intentionally leaves the synthetic Notice local.
Public fixtures must remain synthetic. No automatic Git add, commit or upload.

Routing requires a reason for every decision. HOLD needs `reconsider_on` (ISO
date), `reconsider_when` (condition), or both. DROP retains its reason.
GRADUATE needs a specific `Q-...` investigation ID or literal `PENDING`, rendered
as investigation creation pending. No Q brief, campaign, test or reminder is
created. A `notice-finalization.json` reservation binds the decision and target
path; repeat finalization refuses to overwrite the Notice or create it elsewhere.
Subsequent narrative/routing changes are manual Notice edits under the existing
convention. `draft` always preserves an existing draft, including edits.

## Explicit provenance handoff

The asset-registry validator is called during capture and verification. It also
works independently:

```sh
python -I scripts/fp.py python scripts/research_asset_registry.py validate --assets local_artifacts/global-pulse/GP-2026-10-10-synthetic-divergence/assets.json --locations local_artifacts/global-pulse/GP-2026-10-10-synthetic-divergence/locations.json
python -I scripts/fp.py python -m scripts.evidence_store --repo . --store local_artifacts/global-pulse/evidence-store capture global-pulse:GP-2026-10-10-synthetic-divergence local_artifacts/global-pulse/GP-2026-10-10-synthetic-divergence/packet.json --kind observation
```

The second command is a deliberate, visible evidence-store write. Its returned
`version_id` is the provenance reference. Inspect it with the native `source
VERSION_ID` command using the same `--repo`/`--store`. Repeat explicit captures
can preserve `registry.json`, retained artifacts or a reviewed Notice; this
bridge never creates another evidence database. A supplied packet
`evidence_store_version` is retained as an **unverified reference**; use native
`source` to check it. It cannot replace local file/hash verification. A future
adapter may verify these references automatically after its storage contract is
agreed. Record/assessment/dependency commands remain with their existing owners;
capture does not label a claim supported, assign confidence, or infer edges.

## Verification

```sh
python -I scripts/fp.py --workers 2 python -m pytest tests/global_pulse -q
python -I scripts/fp.py check
```

Tests cover invalid identity/units/conventions/timing, missing and corrupt inputs,
unknown availability, mixed daily/live times, proxy and roll preservation,
declared age/exposure, duplicate capture, correction lineage, edited Notice
protection, explicit routing, native Notice validation, and opt-in evidence-store
source capture without belief/registration writes. The draft PR records the
tested revision, interpreter, exact commands, verification records and any
blocked checks. No lab↔ops imports or research/execution-policy changes.
