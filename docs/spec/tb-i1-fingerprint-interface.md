# TB-I1 fingerprint interface and engineering evidence

This is the consumer contract for [policy_fingerprint.py](../../ops/c1_rail/policy_fingerprint.py),
implementing [TB-P2's serialization contract](../adr/2026-09-12-tradeify-book-protection-instance-admission.md#fingerprint-serialization-contract-owned-implementation-frozen-before-tb-f1).
It records engineering interfaces, not policy ratification, admission, FBR, EF or
activation authority. The [active delivery plan](../superpowers/plans/2026-09-13-tb-i1-through-deployment.md)
owns the remaining gates.

## Producer and verifier use

All helpers are pure: callers supply observed bytes and receive bytes, digests or
validation results. Every invalid input raises `ValueError`; callers must halt the
dependent operation. No helper reads private data, loads source as executable
code, writes configuration, submits an order or authenticates an approval.

| Interface | Input and result |
|---|---|
| `canonical_policy_bytes(row)` | Exactly `instance_key`, `reference_mode`, `scale`, `trigger`, all strings. Numeric strings have no exponent, plus, leading/redundant trailing zero or whitespace; trigger is in (0,1), scale in [0,1]. Returns sorted compact UTF-8 JSON, no BOM/newline. |
| `normalized_geometry_bytes(source)` | UTF-8 source bytes, including an optional UTF-8 encoding declaration. Exactly one top-level simple registry `Assign` or `AnnAssign`; annotated form is `dict[str, ProtectionPolicy]`. Only literal dictionary rows with constant `ProtectionPolicy` keyword values are excluded. Returns the required `ast.dump` bytes after removing that node. |
| `validate_registry(source, expected_rows=...)` | Exact complete registry comparison, including provenance. Each expected row has `reference_mode`, `trigger`, `scale` and `provenance`; numeric fields are canonical strings. `{}` enforces pre-admission. Expected rows must come from independently authenticated authority. |
| `canonical_config_bytes(config)` | JSON object; nested string-keyed dictionaries, lists, strings, finite numbers, booleans and null. Sorted compact UTF-8, no excluded fields. Integer, float and boolean representations remain distinct. |
| `validate_initial_arm_delta(before, after, authorized_deadline=...)` | Both byte strings must already be canonical. Requires explicitly disarmed baseline with `armed_until`; target changes only `dry_run` to false and `armed_until` to the new, exact timezone-aware authorized deadline string. Returns no activation authority. |
| `sha256_bytes(data)` | SHA-256 of full bytes with no transformations. |
| `build_shared_manifest(...)` | Builds the complete supplied inventory using the schema below. |
| `verify_shared_manifest(expected, **observed)` | Rebuilds the manifest from observed bytes and compares the entire canonical representation with the trusted frozen manifest. Missing/extra components, fields, recipe labels, runtime, tool/dependency or source drift fail. |

Policy conversion is explicit: for the existing candidate `ProtectionPolicy`, use
its `reference_mode`, `str(policy.trigger)` and `str(policy.scale)` plus the fixed
instance key. The manifest builder also requires an admitted registry's selected
row to equal those planned policy bytes. The provenance comparison remains separate
and mandatory even though its change cannot alter the normalized policy digest.

Geometry parsing uses `ast.parse(..., mode="exec", type_comments=True)` followed by
`ast.dump(..., annotate_fields=True, include_attributes=False, indent=None)`.
Repeated/nested bindings, aliases, mutation/escape of the registry reference,
indirect named access, nonliteral registry expressions and executable annotations
are refused. The current module's indexed reads and `sorted` diagnostic are
allowed. This is a restricted source-shape contract, not a general Python sandbox.
All unexcluded code still requires digest equality and review. Ordinary comments
and whitespace are not represented by this AST recipe; docstrings, type comments,
type-ignore records and other AST fields remain represented.

## Complete manifest schema

`build_shared_manifest` takes these keyword arguments:

- `policy_row`: the canonical four-field row.
- `geometry_source`: observed `core/dd_geometry.py` bytes.
- `registry_rows`: independently verified expected complete registry, including provenance.
- `components`: mapping from canonical relative artifact names to observed full bytes.
- `tool_source`: observed bytes of the actual loaded `policy_fingerprint.py` source.
- `dependency_artifacts`: nonempty mapping of canonical artifact names to observed bytes.

The returned JSON object has exactly these fields and nested shapes:

```json
{
  "schema": "tb-i1-shared-manifest-v1",
  "toolchain": {
    "recipe": "tb-i1-canonical-v1",
    "runtime": {"implementation": "CPython", "version": "MAJOR.MINOR.PATCH"},
    "source_sha256": "64 lowercase hex characters",
    "dependencies": {"relative/artifact-name": "64 lowercase hex characters"}
  },
  "shared_components": {
    "policy_row": {"recipe": "canonical-policy", "sha256": "64 lowercase hex characters"},
    "core/dd_geometry.py": {"recipe": "geometry-ast", "sha256": "64 lowercase hex characters"},
    "relative/artifact-name": {"recipe": "full-bytes", "sha256": "64 lowercase hex characters"}
  }
}
```

`components` must include `core/dd_protection.py`, `core/firm_rules.py`,
`core/lifecycle.py`, `ops/c1_rail/book_policy.py`,
`ops/c1_rail/book_sizing_context.py`, `ops/c1_rail/book_capacity.py` and
`ops/c1_signal_daemon/book_protocol.py`. This is the minimum foundation inventory.
TB-F1 must additionally supply every shared port, adapter, rule table, allocation,
calendar/overlay, configuration and other transitive shared dependency required by
its actual replay/execution contract. The helper cannot discover missing private
artifacts or prove an inventory complete by itself.

The geometry path, `policy_row` and tool path cannot be supplied again as full-byte
components. Every other component uses full bytes, including comments and line
endings. Artifact names use `/`, without absolute paths, backslashes, colons,
empty segments, `.` or `..`. The tool has no third-party imports. TB-F1 freezes
the full runtime/distribution and dependency inventory; exact Python patch identity
alone does not identify a native build. The tool digest sits outside the tool
source it hashes. Conformance-vector digests likewise belong in an external
freeze/engineering envelope, never inside the bytes they identify.

Callers must bind `tool_source` and dependencies to the code actually executing,
and obtain `expected` from the authenticated FBR/EF freeze, not regenerate it from
the input under examination. `verify_shared_manifest` checks the current CPython
patch, the recipe constant and every observed digest through exact comparison.
It does not verify a running container image, locate files, validate provenance
ratification dates or authenticate an account seal. TB-D0/TB-I3/TB-T1 retain those
obligations. A different patch or dependency inventory is refused even when its
normalized AST happens to match.

## Consumer migration and boundary

| Owner | Required use and remaining work |
|---|---|
| E1 / F1 | Freeze the exact recipe, runtime, tool/dependencies, vector digests and complete shared manifest. No qualification artifact is produced by this packet. |
| D0 | Authenticate both ratifications and the provenance chain; validate exactly the admitted row; compare its canonical identity and geometry against FBR. |
| T1 / B7 / D2 | Gather actual bytes under their approved private/public boundary, authenticate expected manifests and account evidence, and invoke this serializer/verifier. GO image-layer/reseal proof remains separate. |
| I2 / I3 | Gather and authenticate runtime inputs; invoke the same implementation under the frozen runtime; feed the verified policy digest into the typed sizing binding/context. Integrate journal ownership and fail-closed boot/arm checks separately. |
| Initial activation | Apply only the byte-validated config delta; independently check GO, time, seal, fresh boot/request-bound no-activity evidence and durable acknowledgment before risk-add admission. |

The new integration test demonstrates actual source/config bytes → manifest →
verification → canonical policy digest → real sizing host → operation capacity
reducer → admission/refusal using synthetic account and runtime-owner inputs.
Its successful decisions remain `submit=False`. Existing typed host code compares
the owner-provided digests; it cannot itself authenticate their source. No new
listener route, deployment or production collection of artifacts is supplied.

## Local evidence record

The [engineering manifest](../../tests/ops/fixtures/policy_fingerprint_engineering_manifest.json)
is an explicitly unqualified local CPython 3.14.3 record. It pins the observed
source/tool/dependency bytes and conformance vectors for this engineering run.
It is not portable FBR/EF evidence: raw file line endings and Windows runtime
artifacts are retained, and future replay/rail/calendar/private-port inventories
remain incomplete. The integration test's synthetic runtime artifact is distinct
from the observed runtime inventory in that record.

The [literal vectors](../../tests/ops/fixtures/policy_fingerprint_vectors.json)
include both CPython AST dump forms: 3.11/3.12 include the empty `type_ignores`
field; 3.13/3.14 omit it. Tests select the relevant literal vector; manifests still
pin an exact patch, never a range. Byte strings were specified independently of
the implementation and their hashes cross-checked with .NET SHA-256.

Combined acceptance status, test results, base revisions and outstanding gates
are recorded in the delivery plan's appendix after verification.
