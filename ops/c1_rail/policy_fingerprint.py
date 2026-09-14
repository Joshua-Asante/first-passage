"""Pure TB-I1 fingerprint recipe, owned by TB-P2's serialization contract.

These helpers perform no I/O, admission, seal authentication or activation.
Owners supply observed artifact bytes and independently trusted frozen manifests
and registry rows. Never derive expected registry provenance from the source being
verified. A manifest proves identity only for its enumerated artifacts; TB-F1
owns the complete inventory (including private ports, calendars and configs).
"""
from __future__ import annotations

import ast
import hashlib
import io
import json
import math
import re
import sys
import tokenize
from collections.abc import Mapping
from datetime import datetime
from decimal import Decimal


RECIPE = "tb-i1-canonical-v1"
MANIFEST_SCHEMA = "tb-i1-shared-manifest-v1"
TOOL_PATH = "ops/c1_rail/policy_fingerprint.py"
GEOMETRY_PATH = "core/dd_geometry.py"
POLICY_FIELDS = frozenset({"instance_key", "reference_mode", "scale", "trigger"})
REQUIRED_COMPONENTS = frozenset({
    "core/dd_protection.py", "core/firm_rules.py", "core/lifecycle.py",
    "ops/c1_rail/book_policy.py", "ops/c1_rail/book_sizing_context.py",
    "ops/c1_rail/book_capacity.py", "ops/c1_signal_daemon/book_protocol.py",
})
_REGISTRY = "POLICY_REGISTRY"
_DECIMAL = re.compile(r"(?:0|[1-9][0-9]*)(?:\.[0-9]*[1-9])?\Z")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _text(value: object) -> bool:
    return (type(value) is str and bool(value) and value == value.strip()
            and not any(ord(c) < 32 or 0xD800 <= ord(c) <= 0xDFFF for c in value))


def _object(value: object, fields: frozenset | set, label: str) -> None:
    _require(isinstance(value, Mapping) and set(value) == fields, f"invalid {label} fields")


def _json_bytes(value: object) -> bytes:
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (TypeError, ValueError, UnicodeError, RecursionError) as exc:
        raise ValueError("not canonical JSON data") from exc


def sha256_bytes(data: bytes) -> str:
    """Hash observed bytes, without newline or encoding transformations."""
    _require(type(data) is bytes, "hash input must be bytes")
    return hashlib.sha256(data).hexdigest()


def canonical_policy_bytes(row: Mapping[str, str]) -> bytes:
    """Exactly four string fields; provenance is a separate governance check."""
    _object(row, POLICY_FIELDS, "policy")
    _require(all(_text(value) for value in row.values()), "policy fields must be nonempty strings")
    _require(row["reference_mode"] in {"static", "trailing", "locking"}, "invalid reference_mode")
    parts = row["instance_key"].split("@")
    _require(len(parts) == 2 and all(_text(part) for part in parts), "invalid instance_key")
    for field in ("trigger", "scale"):
        _require(_DECIMAL.fullmatch(row[field]) is not None, f"noncanonical {field}")
    _require(0 < Decimal(row["trigger"]) < 1, "trigger outside (0, 1)")
    _require(0 <= Decimal(row["scale"]) <= 1, "scale outside [0, 1]")
    return _json_bytes(dict(row))


def _source_tree(source: bytes) -> ast.Module:
    _require(type(source) is bytes, "geometry source must be UTF-8 bytes")
    try:
        encoding, _ = tokenize.detect_encoding(io.BytesIO(source).readline)
        _require(encoding == "utf-8", "geometry must declare UTF-8 without BOM")
        return ast.parse(source.decode("utf-8"), mode="exec", type_comments=True)
    except (UnicodeError, SyntaxError, ValueError) as exc:
        raise ValueError("invalid UTF-8 geometry source") from exc


def _registry_rows(node: ast.Assign | ast.AnnAssign) -> dict:
    if isinstance(node, ast.AnnAssign):
        # The removed node must not hide executable annotation expressions.
        annotation = ast.parse("dict[str, ProtectionPolicy]", mode="eval").body
        _require(ast.dump(node.annotation) == ast.dump(annotation), "invalid registry annotation")
    _require(isinstance(node.value, ast.Dict), "registry must be a literal dict")
    rows = {}
    for key, value in zip(node.value.keys, node.value.values):
        _require(isinstance(key, ast.Constant) and _text(key.value), "nonliteral registry key")
        _require(key.value not in rows, "duplicate registry key")
        _require(isinstance(value, ast.Call) and isinstance(value.func, ast.Name)
                 and value.func.id == "ProtectionPolicy" and not value.args,
                 "registry values must be literal ProtectionPolicy calls")
        fields = {}
        for item in value.keywords:
            _require(item.arg is not None and item.arg not in fields
                     and isinstance(item.value, ast.Constant), "nonliteral/duplicate policy field")
            fields[item.arg] = item.value.value
        _object(fields, {"reference_mode", "trigger", "scale", "provenance"}, "registry row")
        _require(_text(fields["provenance"]), "missing registry provenance")
        for name in ("trigger", "scale"):
            val = fields[name]
            _require(type(val) in (int, float) and (type(val) is int or math.isfinite(val)),
                     "invalid registry number")
            decimal = format(Decimal(str(val)), "f")
            fields[name] = decimal.rstrip("0").rstrip(".") if "." in decimal else decimal
        canonical_policy_bytes({"instance_key": key.value,
                                **{k: fields[k] for k in ("reference_mode", "trigger", "scale")}})
        rows[key.value] = fields
    return rows


def _geometry(source: bytes) -> tuple[ast.Module, ast.Assign | ast.AnnAssign, dict]:
    tree = _source_tree(source)
    assignments = []
    for node in tree.body:
        if (isinstance(node, ast.AnnAssign) and node.simple == 1
                and isinstance(node.target, ast.Name) and node.target.id == _REGISTRY):
            assignments.append(node)
        elif (isinstance(node, ast.Assign) and len(node.targets) == 1
              and isinstance(node.targets[0], ast.Name) and node.targets[0].id == _REGISTRY):
            assignments.append(node)
    _require(len(assignments) == 1, "expected one simple top-level registry assignment")
    assignment = assignments[0]
    rows = _registry_rows(assignment)
    excluded = set(ast.walk(assignment))
    parents = {child: node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
    for node in ast.walk(tree):
        if node in excluded:
            continue
        if isinstance(node, ast.Name) and node.id == _REGISTRY:
            parent = parents[node]
            # Only current read-only lookup/diagnostic forms may retain a reference.
            lookup = (isinstance(parent, ast.Subscript) and parent.value is node
                      and isinstance(parent.ctx, ast.Load))
            diagnostic = (isinstance(parent, ast.Call) and isinstance(parent.func, ast.Name)
                          and parent.func.id == "sorted" and parent.args == [node]
                          and not parent.keywords)
            _require(isinstance(node.ctx, ast.Load) and (lookup or diagnostic),
                     "ambiguous or indirect registry binding/escape")
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            _require(node.name != _REGISTRY, "registry definition rebinding")
        if isinstance(node, ast.arg):
            _require(node.arg != _REGISTRY, "registry argument rebinding")
        if isinstance(node, ast.alias):
            _require((node.asname or node.name.split(".")[0]) != _REGISTRY, "registry import rebinding")
        if isinstance(node, (ast.Global, ast.Nonlocal)):
            _require(_REGISTRY not in node.names, "indirect registry scope binding")
        if isinstance(node, ast.Attribute):
            _require(node.attr != _REGISTRY, "indirect registry attribute")
        if isinstance(node, ast.Constant) and node.value == _REGISTRY:
            _require(False, "indirect registry name access")
        if isinstance(node, (ast.MatchAs, ast.MatchStar, ast.ExceptHandler)):
            _require(node.name != _REGISTRY, "registry capture rebinding")
        if isinstance(node, ast.MatchMapping):
            _require(node.rest != _REGISTRY, "registry capture rebinding")
    return tree, assignment, rows


def normalized_geometry_bytes(source: bytes) -> bytes:
    """Exclude exactly the literal registry node; retain all other AST fields.

    Ordinary comments/whitespace are absent from this recipe. This is not a
    Python sandbox; unexcluded code remains subject to the frozen digest/review.
    Registry shape is validated here; contents/provenance require validate_registry.
    """
    tree, assignment, _ = _geometry(source)
    tree.body.remove(assignment)
    return ast.dump(tree, annotate_fields=True, include_attributes=False, indent=None).encode("utf-8")


def validate_registry(source: bytes, *, expected_rows: Mapping[str, Mapping[str, str]]) -> None:
    """Compare every row and provenance to independently approved expected rows.

    An empty expectation enforces pre-admission. This cannot ratify an ADR or
    verify its evidence chain: D0/T11 must authenticate the expected row first.
    """
    _require(isinstance(expected_rows, Mapping), "expected registry must be a mapping")
    expected = {}
    for key, row in expected_rows.items():
        _object(row, {"reference_mode", "trigger", "scale", "provenance"}, "expected registry row")
        _require(_text(row["provenance"]), "missing expected provenance")
        canonical_policy_bytes({"instance_key": key,
                                **{k: row[k] for k in ("reference_mode", "trigger", "scale")}})
        expected[key] = dict(row)
    _require(_geometry(source)[2] == expected, "registry contents or provenance mismatch")


def canonical_config_bytes(config: Mapping) -> bytes:
    """Sorted compact UTF-8 JSON, preserving numeric/bool types and array order.

    No key is excluded. Use the same pinned CPython recipe for producer/verifier.
    Floats must be finite; decimals needing exact lexical identity belong in strings.
    """
    def check(value):
        if type(value) is dict:
            _require(all(type(k) is str for k in value), "config keys must be strings")
            for item in value.values():
                check(item)
        elif type(value) is list:
            for item in value:
                check(item)
        else:
            _require(type(value) in (str, int, float, bool, type(None)), "invalid config type")
            if type(value) is float:
                _require(math.isfinite(value), "nonfinite config number")
    _require(isinstance(config, Mapping), "config must be a mapping")
    try:
        plain = dict(config)
        check(plain)
        return _json_bytes(plain)
    except RecursionError as exc:
        raise ValueError("cyclic or too-deep config") from exc


def _load_config(data: bytes) -> dict:
    def pairs(items):
        result = {}
        for key, value in items:
            _require(key not in result, "duplicate config key")
            result[key] = value
        return result
    _require(type(data) is bytes, "config must be bytes")
    try:
        config = json.loads(data.decode("utf-8"), object_pairs_hook=pairs)
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise ValueError("invalid config JSON") from exc
    _require(canonical_config_bytes(config) == data, "config bytes are not canonical")
    return config


def validate_initial_arm_delta(before: bytes, after: bytes, *, authorized_deadline: str) -> None:
    """Validate only T11's exact config delta; never write/arm or validate a GO.

    The owner verifies authorization, current seal/time and effective activation.
    A successful byte comparison is not an activation acknowledgment.
    """
    _require(_text(authorized_deadline), "missing authorized deadline")
    try:
        deadline = datetime.fromisoformat(authorized_deadline)
    except ValueError as exc:
        raise ValueError("invalid authorized deadline") from exc
    _require(deadline.tzinfo is not None and deadline.utcoffset() is not None,
             "authorized deadline must be timezone-aware")
    original, actual = _load_config(before), _load_config(after)
    _require(original.get("dry_run") is True and "armed_until" in original,
             "baseline must be explicitly disarmed with armed_until")
    _require(original["armed_until"] != authorized_deadline, "deadline must be a new explicit arm delta")
    expected = {**original, "dry_run": False, "armed_until": authorized_deadline}
    _require(canonical_config_bytes(expected) == canonical_config_bytes(actual),
             "unapproved initial-arm config change")


def _artifact_digests(artifacts: Mapping[str, bytes]) -> dict[str, str]:
    _require(isinstance(artifacts, Mapping) and bool(artifacts), "missing artifact inventory")
    result = {}
    for path, data in artifacts.items():
        _require(_text(path) and "\\" not in path and ":" not in path
                 and all(part not in ("", ".", "..") for part in path.split("/")),
                 "artifact names must be canonical relative paths")
        result[path] = sha256_bytes(data)
    return result


def build_shared_manifest(*, policy_row: Mapping[str, str], geometry_source: bytes,
                          registry_rows: Mapping[str, Mapping[str, str]],
                          components: Mapping[str, bytes], tool_source: bytes,
                          dependency_artifacts: Mapping[str, bytes]) -> dict:
    """Build an explicit inventory; owners supply observed, never claimed bytes.

    Dependencies are full-byte artifacts (runtime distribution/executable, stdlib
    and any other tool dependencies) selected and frozen by F1. The seven required
    source files are a minimum, not the complete future replay/execution inventory.
    The tool's own digest is outside all payloads from which it is computed.
    """
    _require(sys.implementation.name == "cpython" and sys.version_info.releaselevel == "final",
             "fingerprint recipe requires a final CPython runtime")
    component_hashes = _artifact_digests(components)
    _require(REQUIRED_COMPONENTS <= component_hashes.keys(), "incomplete shared foundation inventory")
    _require(not ({GEOMETRY_PATH, TOOL_PATH, "policy_row"} & component_hashes.keys()),
             "reserved component identity")
    validate_registry(geometry_source, expected_rows=registry_rows)
    policy_bytes = canonical_policy_bytes(policy_row)
    if registry_rows:
        _require(policy_row["instance_key"] in registry_rows, "planned policy absent from admitted registry")
        admitted = registry_rows[policy_row["instance_key"]]
        _require(canonical_policy_bytes({"instance_key": policy_row["instance_key"],
                 **{k: admitted[k] for k in ("reference_mode", "trigger", "scale")}}) == policy_bytes,
                 "admitted policy differs from planned policy")
    shared = {path: {"recipe": "full-bytes", "sha256": digest}
              for path, digest in component_hashes.items()}
    shared["policy_row"] = {"recipe": "canonical-policy", "sha256": sha256_bytes(policy_bytes)}
    shared[GEOMETRY_PATH] = {"recipe": "geometry-ast", "sha256": sha256_bytes(normalized_geometry_bytes(geometry_source))}
    return {"schema": MANIFEST_SCHEMA,
            "toolchain": {"recipe": RECIPE,
                          "runtime": {"implementation": "CPython", "version": ".".join(map(str, sys.version_info[:3]))},
                          "source_sha256": sha256_bytes(tool_source),
                          "dependencies": _artifact_digests(dependency_artifacts)},
            "shared_components": shared}


def verify_shared_manifest(expected: Mapping, **observed) -> None:
    """Recompute every component and reject any inventory, recipe or byte drift.

    expected must come from the authenticated freeze, never the current source.
    Exact comparison also rejects missing/extra fields and changed recipe labels.
    """
    actual = build_shared_manifest(**observed)
    _require(canonical_config_bytes(expected) == canonical_config_bytes(actual),
             "shared fingerprint manifest mismatch")
