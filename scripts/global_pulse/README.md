# Global Pulse observation bridge (packets v1/v2)

Explicit inputs → immutable local capture → editable Notice → supplied routing.
This records observations for research triage; it does not test or admit them.
The [Notice template](../../.claude/skills/brief-authoring/references/notice_log.md)
owns narrative routing. The [asset registry](../research_asset_registry.py) checks
configuration/dataset identity and locator integrity; the
[evidence store](../evidence_store/README.md) preserves explicitly captured sources.
Neither is a research-admission gate.

## Watchlist integration dependency

[PR #787](https://github.com/Joshua-Asante/first-passage/pull/787) owns the
production schema and definitions at `ops/global_market_map/registry.json`.
The adapter supports exactly revision
`107fe97cdba6f2b6b5c0f1939bfe93b3924b3ceb`, SHA-256
`ae0af9795931524faecc53d00ac63864caf41e68949d28f83d719970783b2b9c`.
This dependency was **unmerged** when compatibility was implemented; recognition
of its bytes does not claim approval or merge. Any new revision/content fails
closed until its pin and compatibility tests are deliberately updated.

The immutable
[compatibility snapshot](../../tests/global_pulse/fixtures/global-market-map-107fe97.json)
is byte-for-byte metadata from that Git blob, not a competing registry. It includes
real definitions and the original audit transcription, **no market-value evidence**.
`production.py` projects the native schema without importing the ops layer or
altering its owner files. The original
[synthetic registry](../../tests/global_pulse/fixtures/registry.json) and packet-v1
fixtures remain supported.

Production recognition requires schema/registry identity, exact bytes/hash and
the exact Git revision together. Only that path removes the synthetic-registry
warning. Packet `data_kind: synthetic` still produces a separate SYNTHETIC VALUES
warning even with real registry definitions. The resolver reads explicitly
supplied local bytes, never fetches or adopts the latest branch implicitly.

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

### Packet v2 for production definitions

V2 retains the fields above and requires these additions:

| Field | Contract |
|---|---|
| `watchlist.revision` | Full exact Git revision for production; null for synthetic registries. The original path can be a local compatibility snapshot; the retained context identifies the canonical upstream path. |
| `data_kind` | `synthetic` or `real`, independent of registry identity. Real inputs require the identified production registry. |
| `attendance` | Null for synthetic values. Real captures require `observer`, `method`, timezone-aware `attended_at` no later than capture, and nonempty retained `evidence_ids`. This is an explicit attestation, not independent proof of attendance. |
| `missing_inputs` | Array of `{series_id, reason}`. Must include every unavailable registry concept, including `funding_basis`. A missing/unavailable concept cannot be a measurement or have a fabricated value/proxy. Other available concepts can also be explicitly missing. |
| Measurement `delivery` | `live_label`, `delayed`, or `daily`, matching the pinned entitlement status. A closed-market live label does not establish moving-tick latency. |
| Measurement `observation_date`, `bar_time` | Nullable ISO date and timezone-aware bar-label timestamp, separate from actual `observed_at`, publication, availability and capture. Future bar labels fail. |
| Measurement `timing_basis`, `source_timezone`, `contract_ids` | Required timing explanation, nullable source-session timezone and array of known actual futures contract IDs. Unknown contract mapping is a limitation, never inferred. |

A dated daily level may have null `observed_at`, `window_start` and `window_end`
when its exact clock is unestablished; `observation_date` and `timing_basis` are
then required. Its age is unknown, not zero. Such an input cannot express a
change requiring timestamped endpoints. A bar label must not be substituted for
a completed observation time. Known clock values retain the ordering checks below.
Only daily delivery permits this unknown-clock path; live-label and delayed
intraday measurements require observation/window timestamps. Non-futures inputs
must leave contract IDs empty.
Publication/receipt remains null unless established by the observation evidence.
Registry delay minutes are historical entitlement metadata, not a formula for
manufacturing publication or receipt times.

Each production capture additionally retains hash-checked `registry-context.json`:
all 20 series, the explicit funding gap, providers/aliases, conventions and scale,
proxy distinctions, futures settings/unknown maps, observation/publication notes,
entitlement findings, chart settings, history limitations, source references and
verification evidence. Verification regenerates and compares this context against
the pinned raw registry. Notices disclose measured-series delay/publication,
proxy/futures limitations and the original closed-market verification qualification.

## Demonstration A — synthetic values, real definitions

[production-packet.json](../../tests/global_pulse/fixtures/production-packet.json)
uses invented values and clocks only. The ID date identifies the example, not a
claim that capture occurred that day. No source market values were collected.

| Input | Invented value | Preserved distinction |
|---|---|---|
| `mchi` / NASDAQ:MCHI, loaded BATS:MCHI | 100 USD/share | Live label; Cboe One alternative feed, entitlement not verified, ETF proxy |
| `spx` / SP:SPX, loaded SP_DLY:SPX | 5000 index points | 10-minute delayed; not promoted to live |
| `dfii10` / FRED:DFII10 | 2 percent | Daily date 2026-10-08; exact observation/window clock unknown |
| `brent` / ICEEUR:BRN1! | 70 USD/barrel | 10-minute delayed; B-ADJ off, settlement closes, actual contract mapping unknown |
| `funding_basis` | unavailable, no value | Explicit missing concept, no proxy substitution |

Publication and availability are null for every value. The synthetic capture time
is 2026-10-09T20:30:00Z; it does not supply any missing clock. The baseline equals
the invented levels, so numerical departures are zero. This tests timing/coverage
preservation rather than inventing a market anomaly.

```sh
python -I scripts/fp.py python -m scripts.global_pulse capture --packet tests/global_pulse/fixtures/production-packet.json --input-root tests/global_pulse/fixtures --output local_artifacts/global-pulse-production-demo
python -I scripts/fp.py python -m scripts.global_pulse draft --bundle local_artifacts/global-pulse-production-demo/GP-2026-10-11-synthetic-real-definitions
python -I scripts/fp.py python -m scripts.global_pulse verify --bundle local_artifacts/global-pulse-production-demo/GP-2026-10-11-synthetic-real-definitions
```

The Notice remains OPEN, routing pending. Do not reuse the old fixture's HOLD
decision as an approved decision for this example or a real observation.

## Demonstration B — attended real capture PENDING

No attended real observation or routing decision has been supplied. Neither the
registry coverage/audit report nor synthetic fixtures are real market-value evidence.
The signed-in local TradingView session must manually collect one observation and
retain its evidence in the approved private storage location. No TradingView login,
scraping or collection is automated by this bridge.

Return to this adapter's session:

- Evidence file path and SHA-256; exact symbols/loaded aliases, values and units.
- Each value's actual observation time and capture time, with timezones; preserve
  observation date and bar label separately. Unknown exact clocks remain unknown.
- Publication and first usable availability times only when established, otherwise
  null; feed delays, session/coverage/roll/proxy limitations and prior exposure.
- Observer, attended time, collection method and evidence references.
- Plain observation, comparison baseline and why it stands out.

Then supply packet-v2 `data_kind: real` with that attendance/evidence, retain
`funding_basis` in `missing_inputs`, capture and generate an **OPEN Notice draft**.
Any proposed routing decision goes to review as a proposal; do not call `finalize`
until an explicit routing decision is supplied. No approved HOLD condition, DROP
reason or GRADUATE reference exists for the pending capture. A routing proposal
cannot be justified from the absent real observation yet.

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
new correction ID. `verify` works after the original inputs disappear. Correction
verification also rechecks every retained predecessor and its bound packet hash,
rejects cycles, and preserves capture-time ordering. The complete predecessor
chain must remain beside the successor. Keep the
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
Public measurement fixtures must remain synthetic; the compatibility snapshot
contains public registry metadata only. No automatic Git add, commit or upload.

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
