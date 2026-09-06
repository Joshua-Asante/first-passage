#!/usr/bin/env python3
"""Read-only research asset inventory validator and index renderer.

Contract v1: UTF-8 JSON assets + explicit member locations. This tool records
locator integrity only. It does not admit an asset, certify a strategy, write
evidence, or change campaign admission.

Usage:
    python scripts/research_asset_registry.py validate --assets PATH --locations PATH
    python scripts/research_asset_registry.py index --assets PATH
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
HASH_CHUNK_SIZE = 1024 * 1024
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

ALLOWED_KINDS = frozenset(
    {
        "source",
        "configuration",
        "trade_export",
        "bar_dataset",
        "component",
        "evidence",
    }
)
ALLOWED_PRIVACY = frozenset({"private", "public"})
ALLOWED_SCOPES = frozenset(
    {
        "identity",
        "capture_completeness",
        "coverage",
        "accounting_reconciliation",
        "synthetic_tests",
        "source_parity",
        "review",
    }
)
ALLOWED_RESULTS = frozenset({"passed", "failed", "partial", "pending", "unknown"})
ASSET_FIELDS = (
    "id",
    "kind",
    "label",
    "privacy",
    "members",
    "parents",
    "supersedes",
    "claims",
    "limitations",
)
MEMBER_FIELDS = ("key", "sha256")
CLAIM_FIELDS = ("scope", "result", "evidence_ids", "limitations")
LOCATION_FIELDS = ("asset_id", "member_key", "root", "relative_path")
FINDING_CODES = (
    "INVALID_SCHEMA",
    "DUPLICATE_ID",
    "DUPLICATE_MEMBER",
    "DUPLICATE_LOCATION",
    "MISSING_REFERENCE",
    "RELATIONSHIP_CYCLE",
    "MISSING_LOCATION",
    "UNKNOWN_ROOT",
    "UNSAFE_PATH",
    "MISSING_FILE",
    "HASH_MISMATCH",
    "UNREADABLE_FILE",
)

_MD_SPECIALS = str.maketrans(
    {
        "\\": "\\\\",
        "`": "\\`",
        "*": "\\*",
        "_": "\\_",
        "[": "\\[",
        "]": "\\]",
        "(": "\\(",
        ")": "\\)",
        "#": "\\#",
        "<": "\\<",
        ">": "\\>",
        "|": "\\|",
    }
)

INDEX_DISCLAIMER = (
    "An integrity pass is not admission or source parity. "
    "This index does not assign qualification or readiness."
)

JSON_READ_ERRORS = (OSError, UnicodeError, json.JSONDecodeError)


def _finding(
    code: str,
    asset_id: str = "",
    member_key: str = "",
    message: str = "",
) -> dict[str, str]:
    if code not in FINDING_CODES:
        raise ValueError(f"unknown finding code {code}")
    return {
        "code": code,
        "asset_id": asset_id,
        "member_key": member_key,
        "message": message,
    }


def _is_int(value: object) -> bool:
    return type(value) is int


def _nonempty_str(value: object) -> str | None:
    if isinstance(value, str) and value != "":
        return value
    return None


def _str_list(value: object) -> list[str] | None:
    if not isinstance(value, list):
        return None
    items: list[str] = []
    for item in value:
        text = _nonempty_str(item)
        if text is None:
            return None
        items.append(text)
    return items


def _looks_absolute_relative(relative_path: str) -> bool:
    posix = relative_path.replace("\\", "/")
    if Path(relative_path).is_absolute():
        return True
    if posix.startswith("/") or posix.startswith("~"):
        return True
    if posix.startswith("//"):
        return True
    if len(posix) >= 2 and posix[1] == ":":
        return True
    return False


def _has_parent_traversal(relative_path: str) -> bool:
    posix = relative_path.replace("\\", "/")
    return any(part == ".." for part in Path(posix).parts)


def _unsafe_relative(relative_path: str) -> bool:
    return _looks_absolute_relative(relative_path) or _has_parent_traversal(
        relative_path
    )


def _contained(root: Path, candidate: Path) -> bool:
    try:
        candidate.relative_to(root)
    except ValueError:
        return False
    return True


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(HASH_CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _cyclic_ids(nodes: Sequence[str], edges: Mapping[str, Sequence[str]]) -> set[str]:
    white, gray, black = 0, 1, 2
    color = {node: white for node in nodes}
    cyclic: set[str] = set()

    for start in nodes:
        if color[start] != white:
            continue
        stack: list[tuple[str, int]] = [(start, 0)]
        path: list[str] = []
        while stack:
            node, child_i = stack[-1]
            if child_i == 0:
                color[node] = gray
                path.append(node)
            children = edges.get(node, ())
            if child_i < len(children):
                stack[-1] = (node, child_i + 1)
                dest = children[child_i]
                if dest not in color:
                    continue
                if color[dest] == gray:
                    cyclic.update(path[path.index(dest) :])
                elif color[dest] == white:
                    stack.append((dest, 0))
            else:
                stack.pop()
                path.pop()
                color[node] = black
    return cyclic


def _load_json(path: Path) -> object:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _parse_member(raw: object, asset_id: str) -> tuple[dict[str, str] | None, list[dict[str, str]]]:
    findings: list[dict[str, str]] = []
    if not isinstance(raw, dict):
        findings.append(
            _finding(
                "INVALID_SCHEMA",
                asset_id,
                "",
                "member must be an object with key and sha256",
            )
        )
        return None, findings
    missing = [field for field in MEMBER_FIELDS if field not in raw]
    if missing:
        findings.append(
            _finding(
                "INVALID_SCHEMA",
                asset_id,
                _nonempty_str(raw.get("key")) or "",
                "member missing " + ", ".join(missing),
            )
        )
        return None, findings
    key = _nonempty_str(raw.get("key"))
    digest = _nonempty_str(raw.get("sha256"))
    if key is None or digest is None or SHA256_RE.fullmatch(digest) is None:
        findings.append(
            _finding(
                "INVALID_SCHEMA",
                asset_id,
                key or "",
                "member key must be nonempty and sha256 must be lowercase 64-hex",
            )
        )
        return None, findings
    return {"key": key, "sha256": digest}, findings


def _parse_claim(raw: object, asset_id: str) -> tuple[dict[str, Any] | None, list[dict[str, str]]]:
    findings: list[dict[str, str]] = []
    if not isinstance(raw, dict):
        findings.append(
            _finding("INVALID_SCHEMA", asset_id, "", "claim must be an object")
        )
        return None, findings
    missing = [field for field in CLAIM_FIELDS if field not in raw]
    if missing:
        findings.append(
            _finding(
                "INVALID_SCHEMA",
                asset_id,
                "",
                "claim missing " + ", ".join(missing),
            )
        )
        return None, findings
    scope = _nonempty_str(raw.get("scope"))
    result = _nonempty_str(raw.get("result"))
    evidence_ids = raw.get("evidence_ids")
    limitations = _str_list(raw.get("limitations"))
    if scope not in ALLOWED_SCOPES or result not in ALLOWED_RESULTS:
        findings.append(
            _finding(
                "INVALID_SCHEMA",
                asset_id,
                "",
                "claim scope or result is not an allowed value",
            )
        )
        return None, findings
    if not isinstance(evidence_ids, list) or limitations is None:
        findings.append(
            _finding(
                "INVALID_SCHEMA",
                asset_id,
                "",
                "claim evidence_ids and limitations must be arrays of strings",
            )
        )
        return None, findings
    if len(evidence_ids) == 0:
        findings.append(
            _finding(
                "INVALID_SCHEMA",
                asset_id,
                "",
                "claim evidence_ids must be nonempty",
            )
        )
        return None, findings
    parsed_ids = _str_list(evidence_ids)
    if parsed_ids is None:
        findings.append(
            _finding(
                "INVALID_SCHEMA",
                asset_id,
                "",
                "claim evidence_ids must be nonempty strings",
            )
        )
        return None, findings
    return {
        "scope": scope,
        "result": result,
        "evidence_ids": parsed_ids,
        "limitations": limitations,
    }, findings


def _parse_asset(raw: object) -> tuple[dict[str, Any] | None, list[dict[str, str]]]:
    findings: list[dict[str, str]] = []
    if not isinstance(raw, dict):
        findings.append(_finding("INVALID_SCHEMA", "", "", "asset must be an object"))
        return None, findings
    asset_id = _nonempty_str(raw.get("id")) or ""
    missing = [field for field in ASSET_FIELDS if field not in raw]
    if missing:
        findings.append(
            _finding(
                "INVALID_SCHEMA",
                asset_id,
                "",
                "asset missing " + ", ".join(missing),
            )
        )
        return None, findings
    kind = _nonempty_str(raw.get("kind"))
    label = _nonempty_str(raw.get("label"))
    privacy = _nonempty_str(raw.get("privacy"))
    if asset_id == "" or kind not in ALLOWED_KINDS or label is None or privacy not in ALLOWED_PRIVACY:
        findings.append(
            _finding(
                "INVALID_SCHEMA",
                asset_id,
                "",
                "asset id, kind, label or privacy is invalid",
            )
        )
        return None, findings
    if not isinstance(raw.get("members"), list):
        findings.append(
            _finding("INVALID_SCHEMA", asset_id, "", "members must be an array")
        )
        return None, findings
    parents = _str_list(raw.get("parents"))
    supersedes = _str_list(raw.get("supersedes"))
    limitations = _str_list(raw.get("limitations"))
    if parents is None or supersedes is None or limitations is None:
        findings.append(
            _finding(
                "INVALID_SCHEMA",
                asset_id,
                "",
                "parents, supersedes and limitations must be arrays of strings",
            )
        )
        return None, findings
    if not isinstance(raw.get("claims"), list):
        findings.append(
            _finding("INVALID_SCHEMA", asset_id, "", "claims must be an array")
        )
        return None, findings

    members: list[dict[str, str]] = []
    seen_keys: set[str] = set()
    for item in raw["members"]:
        parsed, member_findings = _parse_member(item, asset_id)
        findings.extend(member_findings)
        if parsed is None:
            continue
        if parsed["key"] in seen_keys:
            findings.append(
                _finding(
                    "DUPLICATE_MEMBER",
                    asset_id,
                    parsed["key"],
                    "member key is repeated on this asset",
                )
            )
            continue
        seen_keys.add(parsed["key"])
        members.append(parsed)

    claims: list[dict[str, Any]] = []
    for item in raw["claims"]:
        parsed_claim, claim_findings = _parse_claim(item, asset_id)
        findings.extend(claim_findings)
        if parsed_claim is not None:
            claims.append(parsed_claim)

    if any(item["code"] == "INVALID_SCHEMA" for item in findings):
        return None, findings
    return {
        "id": asset_id,
        "kind": kind,
        "label": label,
        "privacy": privacy,
        "members": members,
        "parents": parents,
        "supersedes": supersedes,
        "claims": claims,
        "limitations": limitations,
    }, findings


def inspect_assets(raw: object) -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    """Return schema/reference findings and normalized assets."""
    findings: list[dict[str, str]] = []
    if not isinstance(raw, dict) or raw.get("schema_version") != SCHEMA_VERSION or not _is_int(
        raw.get("schema_version")
    ):
        return [
            _finding(
                "INVALID_SCHEMA",
                "",
                "",
                "assets document must be an object with schema_version 1",
            )
        ], []
    if not isinstance(raw.get("assets"), list):
        return [
            _finding("INVALID_SCHEMA", "", "", "assets must be an array")
        ], []

    assets: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    by_id: dict[str, dict[str, Any]] = {}
    for item in raw["assets"]:
        parsed, asset_findings = _parse_asset(item)
        findings.extend(asset_findings)
        if parsed is None:
            continue
        if parsed["id"] in seen_ids:
            findings.append(
                _finding(
                    "DUPLICATE_ID",
                    parsed["id"],
                    "",
                    "asset id is repeated",
                )
            )
            continue
        seen_ids.add(parsed["id"])
        assets.append(parsed)
        by_id[parsed["id"]] = parsed

    if assets:
        _reference_findings(assets, by_id, findings)
    return findings, assets


def _reference_findings(
    assets: Sequence[Mapping[str, Any]],
    by_id: Mapping[str, Mapping[str, Any]],
    findings: list[dict[str, str]],
) -> None:
    parent_edges: dict[str, list[str]] = {asset["id"]: [] for asset in assets}
    supersede_edges: dict[str, list[str]] = {asset["id"]: [] for asset in assets}
    for asset in assets:
        asset_id = asset["id"]
        for field, edges in (("parents", parent_edges), ("supersedes", supersede_edges)):
            for target in asset[field]:
                if target not in by_id:
                    findings.append(
                        _finding(
                            "MISSING_REFERENCE",
                            asset_id,
                            "",
                            f"{field} id is not an asset",
                        )
                    )
                    continue
                edges[asset_id].append(target)
        for claim in asset["claims"]:
            for evidence_id in claim["evidence_ids"]:
                target = by_id.get(evidence_id)
                if target is None or target["kind"] != "evidence":
                    findings.append(
                        _finding(
                            "MISSING_REFERENCE",
                            asset_id,
                            "",
                            "claim evidence_ids must reference an evidence asset",
                        )
                    )

    ids = [asset["id"] for asset in assets]
    for relation, edges in (("parents", parent_edges), ("supersedes", supersede_edges)):
        for asset_id in sorted(_cyclic_ids(ids, edges)):
            findings.append(
                _finding(
                    "RELATIONSHIP_CYCLE",
                    asset_id,
                    "",
                    f"{relation} relationship forms a cycle",
                )
            )


def inspect_locations(
    raw: object,
) -> tuple[list[dict[str, str]], dict[str, str], list[dict[str, str]]]:
    findings: list[dict[str, str]] = []
    if not isinstance(raw, dict) or raw.get("schema_version") != SCHEMA_VERSION or not _is_int(
        raw.get("schema_version")
    ):
        return [
            _finding(
                "INVALID_SCHEMA",
                "",
                "",
                "locations document must be an object with schema_version 1",
            )
        ], {}, []
    roots_raw = raw.get("roots")
    locations_raw = raw.get("locations")
    if not isinstance(roots_raw, dict) or not isinstance(locations_raw, list):
        return [
            _finding(
                "INVALID_SCHEMA",
                "",
                "",
                "roots must be an object and locations must be an array",
            )
        ], {}, []

    roots: dict[str, str] = {}
    for name, value in roots_raw.items():
        root_name = _nonempty_str(name)
        root_value = _nonempty_str(value)
        if root_name is None or root_value is None or not Path(root_value).is_absolute():
            findings.append(
                _finding(
                    "INVALID_SCHEMA",
                    "",
                    "",
                    "root names map to nonempty absolute local paths",
                )
            )
            continue
        roots[root_name] = root_value

    rows: list[dict[str, str]] = []
    seen_tuples: set[tuple[str, str, str, str]] = set()
    for item in locations_raw:
        if not isinstance(item, dict):
            findings.append(
                _finding("INVALID_SCHEMA", "", "", "location must be an object")
            )
            continue
        missing = [field for field in LOCATION_FIELDS if field not in item]
        if missing:
            findings.append(
                _finding(
                    "INVALID_SCHEMA",
                    _nonempty_str(item.get("asset_id")) or "",
                    _nonempty_str(item.get("member_key")) or "",
                    "location missing " + ", ".join(missing),
                )
            )
            continue
        asset_id = _nonempty_str(item.get("asset_id"))
        member_key = _nonempty_str(item.get("member_key"))
        root_name = _nonempty_str(item.get("root"))
        relative_path = _nonempty_str(item.get("relative_path"))
        if None in (asset_id, member_key, root_name, relative_path):
            findings.append(
                _finding(
                    "INVALID_SCHEMA",
                    asset_id or "",
                    member_key or "",
                    "location fields must be nonempty strings",
                )
            )
            continue
        key = (asset_id, member_key, root_name, relative_path)
        if key in seen_tuples:
            findings.append(
                _finding(
                    "DUPLICATE_LOCATION",
                    asset_id,
                    member_key,
                    "location tuple is repeated",
                )
            )
            continue
        seen_tuples.add(key)
        rows.append(
            {
                "asset_id": asset_id,
                "member_key": member_key,
                "root": root_name,
                "relative_path": relative_path,
            }
        )
    return findings, roots, rows


def _member_index(
    assets: Sequence[Mapping[str, Any]],
) -> dict[tuple[str, str], str]:
    index: dict[tuple[str, str], str] = {}
    for asset in assets:
        for member in asset["members"]:
            index[(asset["id"], member["key"])] = member["sha256"]
    return index


def _location_integrity(
    assets: Sequence[Mapping[str, Any]],
    roots: Mapping[str, str],
    rows: Sequence[Mapping[str, str]],
) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    members = _member_index(assets)
    located: set[tuple[str, str]] = set()
    resolved_jobs: list[tuple[str, str, Path, str]] = []

    for row in rows:
        asset_id = row["asset_id"]
        member_key = row["member_key"]
        member_id = (asset_id, member_key)
        if member_id not in members:
            findings.append(
                _finding(
                    "MISSING_REFERENCE",
                    asset_id,
                    member_key,
                    "location does not name an asset member",
                )
            )
        else:
            located.add(member_id)

        root_name = row["root"]
        relative_path = row["relative_path"]
        if root_name not in roots:
            findings.append(
                _finding(
                    "UNKNOWN_ROOT",
                    asset_id,
                    member_key,
                    "location root is not declared",
                )
            )
            continue
        if _unsafe_relative(relative_path):
            findings.append(
                _finding(
                    "UNSAFE_PATH",
                    asset_id,
                    member_key,
                    "relative path is absolute, traverses parents, or escapes the declared root",
                )
            )
            continue

        root_path = Path(roots[root_name])
        member_path = root_path.joinpath(relative_path)
        try:
            resolved_root = root_path.resolve()
            resolved_member = member_path.resolve()
        except (OSError, RuntimeError):
            findings.append(
                _finding(
                    "UNSAFE_PATH",
                    asset_id,
                    member_key,
                    "path could not be resolved inside the declared root",
                )
            )
            continue
        if not _contained(resolved_root, resolved_member):
            findings.append(
                _finding(
                    "UNSAFE_PATH",
                    asset_id,
                    member_key,
                    "resolved path escapes the declared root",
                )
            )
            continue
        expected = members.get(member_id)
        if expected is None:
            continue
        resolved_jobs.append((asset_id, member_key, resolved_member, expected))

    for asset in assets:
        for member in asset["members"]:
            member_id = (asset["id"], member["key"])
            if member_id not in located:
                findings.append(
                    _finding(
                        "MISSING_LOCATION",
                        asset["id"],
                        member["key"],
                        "member has no location",
                    )
                )

    hash_cache: dict[str, str] = {}
    for asset_id, member_key, resolved_member, expected in resolved_jobs:
        if not resolved_member.exists():
            findings.append(
                _finding(
                    "MISSING_FILE",
                    asset_id,
                    member_key,
                    "listed member file is missing",
                )
            )
            continue
        if not resolved_member.is_file():
            findings.append(
                _finding(
                    "UNREADABLE_FILE",
                    asset_id,
                    member_key,
                    "listed member path is not a readable file",
                )
            )
            continue
        cache_key = str(resolved_member)
        if cache_key not in hash_cache:
            try:
                hash_cache[cache_key] = _sha256_file(resolved_member)
            except OSError:
                findings.append(
                    _finding(
                        "UNREADABLE_FILE",
                        asset_id,
                        member_key,
                        "listed member file could not be read",
                    )
                )
                continue
        actual = hash_cache[cache_key]
        if actual != expected:
            findings.append(
                _finding(
                    "HASH_MISMATCH",
                    asset_id,
                    member_key,
                    "member digest does not match recorded sha256",
                )
            )
    return findings


def _sort_findings(findings: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    return sorted(
        findings,
        key=lambda item: (
            item["code"],
            item["asset_id"],
            item["member_key"],
            item["message"],
        ),
    )


def validate_registry(assets_path: Path, locations_path: Path) -> list[dict[str, str]]:
    """Return integrity findings. Empty means the listed members match."""
    assets_raw = _load_json(assets_path)
    locations_raw = _load_json(locations_path)
    findings, assets = inspect_assets(assets_raw)
    location_findings, roots, rows = inspect_locations(locations_raw)
    findings.extend(location_findings)
    findings.extend(_location_integrity(assets, roots, rows))
    return _sort_findings(findings)


def _escape_md(text: str) -> str:
    return text.translate(_MD_SPECIALS)


def _code_span(text: str) -> str:
    longest = 0
    run = 0
    for char in text:
        if char == "`":
            run += 1
            longest = max(longest, run)
        else:
            run = 0
    fence = "`" * (longest + 1)
    if longest:
        return f"{fence} {text} {fence}"
    return f"{fence}{text}{fence}"


def _join_ids(values: Sequence[str]) -> str:
    if not values:
        return "none"
    return ", ".join(_code_span(value) for value in values)


def _render_claim(claim: Mapping[str, Any]) -> str:
    evidence = ", ".join(_code_span(item) for item in claim["evidence_ids"])
    limitations = "; ".join(_escape_md(item) for item in claim["limitations"]) or "none"
    return (
        f"scope={_code_span(claim['scope'])}; "
        f"result={_code_span(claim['result'])}; "
        f"evidence={evidence}; "
        f"limitations: {limitations}"
    )


def render_assets(assets: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# Research asset inventory",
        "",
        INDEX_DISCLAIMER,
        "",
    ]
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for asset in assets:
        grouped.setdefault(asset["kind"], []).append(asset)
    for kind in sorted(grouped):
        lines.append(f"## {kind}")
        lines.append("")
        for asset in sorted(grouped[kind], key=lambda item: item["id"]):
            lines.append(f"### {_code_span(asset['id'])}")
            lines.append("")
            lines.append(f"- Label: {_escape_md(asset['label'])}")
            lines.append(f"- Privacy: {_code_span(asset['privacy'])}")
            if asset["members"]:
                lines.append("- Members:")
                for member in sorted(asset["members"], key=lambda item: item["key"]):
                    lines.append(
                        f"  - {_code_span(member['key'])}: {_code_span(member['sha256'])}"
                    )
            else:
                lines.append("- Members: none")
            lines.append(f"- Parents: {_join_ids(asset['parents'])}")
            lines.append(f"- Supersedes: {_join_ids(asset['supersedes'])}")
            if asset["claims"]:
                lines.append("- Claims:")
                for claim in asset["claims"]:
                    lines.append(f"  - {_render_claim(claim)}")
            else:
                lines.append("- Claims: none")
            if asset["limitations"]:
                lines.append("- Limitations:")
                for item in asset["limitations"]:
                    lines.append(f"  - {_escape_md(item)}")
            else:
                lines.append("- Limitations: none")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_index(assets_path: Path) -> str:
    """Return deterministic Markdown. Raises ValueError on a malformed graph."""
    findings, assets = inspect_assets(_load_json(assets_path))
    blocking = {
        item["code"]
        for item in findings
        if item["code"]
        in {
            "INVALID_SCHEMA",
            "DUPLICATE_ID",
            "DUPLICATE_MEMBER",
            "MISSING_REFERENCE",
            "RELATIONSHIP_CYCLE",
        }
    }
    if blocking:
        raise ValueError("malformed inventory or reference graph")
    return render_assets(assets)


def _cmd_validate(assets_path: Path, locations_path: Path) -> int:
    try:
        findings = validate_registry(assets_path, locations_path)
    except JSON_READ_ERRORS:
        print("unreadable JSON inventory", file=sys.stderr)
        return 2
    json.dump(
        {"schema_version": SCHEMA_VERSION, "findings": findings},
        sys.stdout,
        indent=2,
    )
    sys.stdout.write("\n")
    return 0 if not findings else 1


def _cmd_index(assets_path: Path) -> int:
    try:
        sys.stdout.write(render_index(assets_path))
    except JSON_READ_ERRORS:
        print("unreadable JSON inventory", file=sys.stderr)
        return 2
    except ValueError:
        print("malformed inventory", file=sys.stderr)
        return 2
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate a research asset inventory or render a private index.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate_parser = subparsers.add_parser(
        "validate",
        help="check schema, references and listed member hashes",
    )
    validate_parser.add_argument("--assets", type=Path, required=True)
    validate_parser.add_argument("--locations", type=Path, required=True)
    index_parser = subparsers.add_parser(
        "index",
        help="print a deterministic Markdown index to stdout",
    )
    index_parser.add_argument("--assets", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "validate":
        return _cmd_validate(args.assets, args.locations)
    if args.command == "index":
        return _cmd_index(args.assets)
    return 2


if __name__ == "__main__":
    sys.exit(main())
