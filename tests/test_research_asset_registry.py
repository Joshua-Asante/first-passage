"""Synthetic integrity tests for scripts/research_asset_registry.py.

Fixtures use tempfile, hashlib and JSON only. No private inventory is read.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "research_asset_registry.py"
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from research_asset_registry import render_index, validate_registry  # noqa: E402

SYNTHETIC_BYTES = b"synthetic source"
FINDING_KEYS = ("code", "asset_id", "member_key", "message")


class ResearchAssetRegistryTests(unittest.TestCase):
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

    def write_inventory(
        self,
        assets_doc: dict,
        locations_doc: dict | None = None,
        files: dict[str, bytes] | None = None,
    ) -> tuple[Path, Path | None, Path]:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        for relative, payload in (files or {}).items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
        assets_path = root / "assets.json"
        assets_path.write_text(json.dumps(assets_doc), encoding="utf-8")
        locations_path = None
        if locations_doc is not None:
            if "roots" in locations_doc and "test" not in locations_doc["roots"]:
                locations_doc = {
                    **locations_doc,
                    "roots": {"test": str(root), **locations_doc["roots"]},
                }
            elif "roots" not in locations_doc:
                locations_doc = {**locations_doc, "roots": {"test": str(root)}}
            else:
                locations_doc = {
                    **locations_doc,
                    "roots": {
                        name: (str(root) if name == "test" else value)
                        for name, value in locations_doc["roots"].items()
                    },
                }
            locations_path = root / "locations.local.json"
            locations_path.write_text(json.dumps(locations_doc), encoding="utf-8")
        return assets_path, locations_path, root

    def source_asset(self, **overrides):
        payload = SYNTHETIC_BYTES
        asset = {
            "id": "example-source-v1",
            "kind": "source",
            "label": "Synthetic source",
            "privacy": "private",
            "members": [{"key": "body", "sha256": hashlib.sha256(payload).hexdigest()}],
            "parents": [],
            "supersedes": [],
            "claims": [],
            "limitations": ["Synthetic fixture only"],
        }
        asset.update(overrides)
        return asset

    def evidence_asset(self, asset_id: str = "example-test-log-v1", **overrides):
        payload = b"synthetic evidence"
        asset = {
            "id": asset_id,
            "kind": "evidence",
            "label": "Synthetic evidence",
            "privacy": "private",
            "members": [{"key": "body", "sha256": hashlib.sha256(payload).hexdigest()}],
            "parents": [],
            "supersedes": [],
            "claims": [],
            "limitations": ["Synthetic evidence fixture"],
        }
        asset.update(overrides)
        return asset

    def locations_for(self, *entries: tuple[str, str, str]):
        return {
            "schema_version": 1,
            "roots": {},
            "locations": [
                {
                    "asset_id": asset_id,
                    "member_key": member_key,
                    "root": "test",
                    "relative_path": relative_path,
                }
                for asset_id, member_key, relative_path in entries
            ],
        }

    def codes(self, findings: list[dict[str, str]]) -> set[str]:
        return {item["code"] for item in findings}

    def assert_findings_shape(self, findings: list[dict[str, str]], root: Path | None = None) -> None:
        blob = json.dumps(findings)
        if root is not None:
            self.assertNotIn(str(root), blob)
        for item in findings:
            self.assertEqual(tuple(item), FINDING_KEYS)
            for key in FINDING_KEYS:
                self.assertIsInstance(item[key], str)

    def test_mutated_member_is_reported(self):
        assets_path, locations_path, member_path = self.make_registry()
        self.assertEqual(validate_registry(assets_path, locations_path), [])
        member_path.write_bytes(b"changed")
        findings = validate_registry(assets_path, locations_path)
        self.assertIn("HASH_MISMATCH", {item["code"] for item in findings})

    def test_valid_minimal_registry_has_no_findings(self):
        assets_path, locations_path, member_path = self.make_registry()
        findings = validate_registry(assets_path, locations_path)
        self.assertEqual(findings, [])
        self.assertEqual(member_path.read_bytes(), SYNTHETIC_BYTES)

    def test_duplicate_ids_are_reported(self):
        asset = self.source_asset()
        assets_path, locations_path, root = self.write_inventory(
            {"schema_version": 1, "assets": [asset, dict(asset)]},
            self.locations_for(("example-source-v1", "body", "source.txt")),
            {"source.txt": SYNTHETIC_BYTES},
        )
        findings = validate_registry(assets_path, locations_path)
        self.assertIn("DUPLICATE_ID", self.codes(findings))
        self.assert_findings_shape(findings, root)

    def test_duplicate_member_keys_are_reported(self):
        digest = hashlib.sha256(SYNTHETIC_BYTES).hexdigest()
        asset = self.source_asset(
            members=[
                {"key": "body", "sha256": digest},
                {"key": "body", "sha256": digest},
            ]
        )
        assets_path, locations_path, root = self.write_inventory(
            {"schema_version": 1, "assets": [asset]},
            self.locations_for(("example-source-v1", "body", "source.txt")),
            {"source.txt": SYNTHETIC_BYTES},
        )
        findings = validate_registry(assets_path, locations_path)
        self.assertIn("DUPLICATE_MEMBER", self.codes(findings))
        self.assert_findings_shape(findings, root)

    def test_duplicate_location_tuples_are_reported(self):
        assets_path, locations_path, root = self.write_inventory(
            {"schema_version": 1, "assets": [self.source_asset()]},
            {
                "schema_version": 1,
                "roots": {},
                "locations": [
                    {
                        "asset_id": "example-source-v1",
                        "member_key": "body",
                        "root": "test",
                        "relative_path": "source.txt",
                    },
                    {
                        "asset_id": "example-source-v1",
                        "member_key": "body",
                        "root": "test",
                        "relative_path": "source.txt",
                    },
                ],
            },
            {"source.txt": SYNTHETIC_BYTES},
        )
        findings = validate_registry(assets_path, locations_path)
        self.assertIn("DUPLICATE_LOCATION", self.codes(findings))
        self.assert_findings_shape(findings, root)

    def test_invalid_hash_type_and_enum_are_schema_errors(self):
        cases = [
            self.source_asset(members=[{"key": "body", "sha256": "not-a-hash"}]),
            self.source_asset(members=[{"key": "body", "sha256": "A" * 64}]),
            self.source_asset(members="body"),
            self.source_asset(kind="strategy"),
            self.source_asset(privacy="secret"),
            self.source_asset(id=""),
            self.source_asset(label=""),
        ]
        for asset in cases:
            with self.subTest(asset=asset):
                assets_path, locations_path, root = self.write_inventory(
                    {"schema_version": 1, "assets": [asset]},
                    self.locations_for(("example-source-v1", "body", "source.txt")),
                    {"source.txt": SYNTHETIC_BYTES},
                )
                findings = validate_registry(assets_path, locations_path)
                self.assertIn("INVALID_SCHEMA", self.codes(findings))
                self.assert_findings_shape(findings, root)

    def test_malformed_top_level_inventory_is_invalid_schema(self):
        assets_path, locations_path, root = self.write_inventory(
            {"schema_version": 1},
            {"schema_version": 1, "roots": {}, "locations": []},
        )
        findings = validate_registry(assets_path, locations_path)
        self.assertIn("INVALID_SCHEMA", self.codes(findings))
        self.assert_findings_shape(findings, root)

    def test_missing_evidence_reference_is_reported(self):
        asset = self.source_asset(
            claims=[{
                "scope": "synthetic_tests",
                "result": "passed",
                "evidence_ids": ["missing-evidence-v1"],
                "limitations": ["Synthetic fixture only"],
            }]
        )
        assets_path, locations_path, root = self.write_inventory(
            {"schema_version": 1, "assets": [asset]},
            self.locations_for(("example-source-v1", "body", "source.txt")),
            {"source.txt": SYNTHETIC_BYTES},
        )
        findings = validate_registry(assets_path, locations_path)
        self.assertIn("MISSING_REFERENCE", self.codes(findings))
        self.assert_findings_shape(findings, root)

    def test_evidence_id_must_point_at_evidence_kind(self):
        other = self.source_asset(id="other-source-v1", label="Other")
        asset = self.source_asset(
            claims=[{
                "scope": "synthetic_tests",
                "result": "passed",
                "evidence_ids": ["other-source-v1"],
                "limitations": ["Synthetic fixture only"],
            }]
        )
        assets_path, locations_path, root = self.write_inventory(
            {"schema_version": 1, "assets": [asset, other]},
            self.locations_for(
                ("example-source-v1", "body", "source.txt"),
                ("other-source-v1", "body", "other.txt"),
            ),
            {"source.txt": SYNTHETIC_BYTES, "other.txt": SYNTHETIC_BYTES},
        )
        findings = validate_registry(assets_path, locations_path)
        self.assertIn("MISSING_REFERENCE", self.codes(findings))
        self.assert_findings_shape(findings, root)

    def test_empty_claim_evidence_is_invalid_schema(self):
        asset = self.source_asset(
            claims=[{
                "scope": "synthetic_tests",
                "result": "pending",
                "evidence_ids": [],
                "limitations": ["No evidence recorded"],
            }]
        )
        assets_path, locations_path, root = self.write_inventory(
            {"schema_version": 1, "assets": [asset]},
            self.locations_for(("example-source-v1", "body", "source.txt")),
            {"source.txt": SYNTHETIC_BYTES},
        )
        findings = validate_registry(assets_path, locations_path)
        self.assertIn("INVALID_SCHEMA", self.codes(findings))
        self.assert_findings_shape(findings, root)

    def test_self_link_is_a_relationship_cycle(self):
        asset = self.source_asset(parents=["example-source-v1"])
        assets_path, locations_path, root = self.write_inventory(
            {"schema_version": 1, "assets": [asset]},
            self.locations_for(("example-source-v1", "body", "source.txt")),
            {"source.txt": SYNTHETIC_BYTES},
        )
        findings = validate_registry(assets_path, locations_path)
        self.assertIn("RELATIONSHIP_CYCLE", self.codes(findings))
        self.assert_findings_shape(findings, root)

    def test_parent_cycle_is_reported(self):
        first = self.source_asset(parents=["other-source-v1"])
        second = self.source_asset(
            id="other-source-v1",
            label="Other",
            parents=["example-source-v1"],
        )
        assets_path, locations_path, root = self.write_inventory(
            {"schema_version": 1, "assets": [first, second]},
            self.locations_for(
                ("example-source-v1", "body", "source.txt"),
                ("other-source-v1", "body", "other.txt"),
            ),
            {"source.txt": SYNTHETIC_BYTES, "other.txt": SYNTHETIC_BYTES},
        )
        findings = validate_registry(assets_path, locations_path)
        self.assertIn("RELATIONSHIP_CYCLE", self.codes(findings))
        self.assert_findings_shape(findings, root)

    def test_supersedes_cycle_is_reported(self):
        first = self.source_asset(supersedes=["other-source-v1"])
        second = self.source_asset(
            id="other-source-v1",
            label="Other",
            supersedes=["example-source-v1"],
        )
        assets_path, locations_path, root = self.write_inventory(
            {"schema_version": 1, "assets": [first, second]},
            self.locations_for(
                ("example-source-v1", "body", "source.txt"),
                ("other-source-v1", "body", "other.txt"),
            ),
            {"source.txt": SYNTHETIC_BYTES, "other.txt": SYNTHETIC_BYTES},
        )
        findings = validate_registry(assets_path, locations_path)
        self.assertIn("RELATIONSHIP_CYCLE", self.codes(findings))
        self.assert_findings_shape(findings, root)

    def test_missing_parent_reference_is_reported(self):
        asset = self.source_asset(parents=["missing-parent-v1"])
        assets_path, locations_path, root = self.write_inventory(
            {"schema_version": 1, "assets": [asset]},
            self.locations_for(("example-source-v1", "body", "source.txt")),
            {"source.txt": SYNTHETIC_BYTES},
        )
        findings = validate_registry(assets_path, locations_path)
        self.assertIn("MISSING_REFERENCE", self.codes(findings))
        self.assert_findings_shape(findings, root)

    def test_unknown_root_is_reported(self):
        assets_path, locations_path, root = self.write_inventory(
            {"schema_version": 1, "assets": [self.source_asset()]},
            {
                "schema_version": 1,
                "roots": {},
                "locations": [{
                    "asset_id": "example-source-v1",
                    "member_key": "body",
                    "root": "missing-root",
                    "relative_path": "source.txt",
                }],
            },
            {"source.txt": SYNTHETIC_BYTES},
        )
        findings = validate_registry(assets_path, locations_path)
        self.assertIn("UNKNOWN_ROOT", self.codes(findings))
        self.assert_findings_shape(findings, root)

    def test_missing_location_and_missing_file_are_reported(self):
        assets_path, locations_path, root = self.write_inventory(
            {
                "schema_version": 1,
                "assets": [
                    self.source_asset(),
                    self.source_asset(id="second-source-v1", label="Second"),
                ],
            },
            self.locations_for(("example-source-v1", "body", "absent.txt")),
            {"source.txt": SYNTHETIC_BYTES},
        )
        findings = validate_registry(assets_path, locations_path)
        self.assertIn("MISSING_LOCATION", self.codes(findings))
        self.assertIn("MISSING_FILE", self.codes(findings))
        self.assert_findings_shape(findings, root)

    def test_unknown_member_location_is_missing_reference(self):
        assets_path, locations_path, root = self.write_inventory(
            {"schema_version": 1, "assets": [self.source_asset()]},
            self.locations_for(("example-source-v1", "sidecar", "source.txt")),
            {"source.txt": SYNTHETIC_BYTES},
        )
        findings = validate_registry(assets_path, locations_path)
        self.assertIn("MISSING_REFERENCE", self.codes(findings))
        self.assertIn("MISSING_LOCATION", self.codes(findings))
        self.assert_findings_shape(findings, root)

    def test_absolute_and_parent_traversal_paths_are_unsafe(self):
        for relative_path in ("/tmp/source.txt", "../source.txt", "foo/../../source.txt"):
            with self.subTest(relative_path=relative_path):
                assets_path, locations_path, root = self.write_inventory(
                    {"schema_version": 1, "assets": [self.source_asset()]},
                    self.locations_for(("example-source-v1", "body", relative_path)),
                    {"source.txt": SYNTHETIC_BYTES},
                )
                findings = validate_registry(assets_path, locations_path)
                self.assertIn("UNSAFE_PATH", self.codes(findings))
                self.assert_findings_shape(findings, root)

    def test_multiple_valid_locations_for_one_member_succeed(self):
        digest = hashlib.sha256(SYNTHETIC_BYTES).hexdigest()
        assets_path, locations_path, root = self.write_inventory(
            {"schema_version": 1, "assets": [self.source_asset()]},
            {
                "schema_version": 1,
                "roots": {},
                "locations": [
                    {
                        "asset_id": "example-source-v1",
                        "member_key": "body",
                        "root": "test",
                        "relative_path": "source.txt",
                    },
                    {
                        "asset_id": "example-source-v1",
                        "member_key": "body",
                        "root": "test",
                        "relative_path": "copy/source.txt",
                    },
                ],
            },
            {
                "source.txt": SYNTHETIC_BYTES,
                "copy/source.txt": SYNTHETIC_BYTES,
            },
        )
        findings = validate_registry(assets_path, locations_path)
        self.assertEqual(findings, [])
        self.assertEqual(hashlib.sha256(SYNTHETIC_BYTES).hexdigest(), digest)
        self.assertTrue((root / "source.txt").is_file())
        self.assertTrue((root / "copy/source.txt").is_file())

    def test_symlink_escape_is_unsafe_or_skipped(self):
        assets_path, locations_path, root = self.write_inventory(
            {"schema_version": 1, "assets": [self.source_asset()]},
            self.locations_for(("example-source-v1", "body", "link.txt")),
        )
        outside = root.parent / f"{root.name}-outside.txt"
        self.addCleanup(lambda: outside.unlink(missing_ok=True))
        outside.write_bytes(SYNTHETIC_BYTES)
        link = root / "link.txt"
        try:
            link.symlink_to(outside)
        except OSError as exc:
            self.skipTest(f"symlink creation disallowed: {exc}")
        findings = validate_registry(assets_path, locations_path)
        self.assertIn("UNSAFE_PATH", self.codes(findings))
        self.assert_findings_shape(findings, root)

    def test_in_root_symlink_is_allowed_or_skipped(self):
        assets_path, locations_path, root = self.write_inventory(
            {"schema_version": 1, "assets": [self.source_asset()]},
            self.locations_for(("example-source-v1", "body", "link.txt")),
            {"source.txt": SYNTHETIC_BYTES},
        )
        link = root / "link.txt"
        try:
            link.symlink_to(root / "source.txt")
        except OSError as exc:
            self.skipTest(f"symlink creation disallowed: {exc}")
        self.assertEqual(validate_registry(assets_path, locations_path), [])

    def test_unreadable_file_is_reported_or_skipped(self):
        assets_path, locations_path, member_path = self.make_registry()
        original_mode = member_path.stat().st_mode
        member_path.chmod(0)
        self.addCleanup(lambda: member_path.chmod(original_mode))
        try:
            with member_path.open("rb"):
                readable = True
        except OSError:
            readable = False
        if readable:
            self.skipTest("process can still read chmod-0 files")
        findings = validate_registry(assets_path, locations_path)
        self.assertIn("UNREADABLE_FILE", self.codes(findings))
        self.assert_findings_shape(findings)

    def test_directory_member_is_unreadable(self):
        assets_path, locations_path, root = self.write_inventory(
            {"schema_version": 1, "assets": [self.source_asset()]},
            self.locations_for(("example-source-v1", "body", "not-a-file")),
        )
        (root / "not-a-file").mkdir()
        findings = validate_registry(assets_path, locations_path)
        self.assertIn("UNREADABLE_FILE", self.codes(findings))
        self.assert_findings_shape(findings, root)

    def test_index_is_sorted_by_kind_then_id_and_escapes_markdown(self):
        assets_path, _, _ = self.write_inventory({
            "schema_version": 1,
            "assets": [
                self.source_asset(
                    id="zeta-source-v1",
                    label="See *this* <script> and [link](x)",
                ),
                self.evidence_asset(asset_id="alpha-evidence-v1"),
                self.source_asset(id="alpha-source-v1", label="Alpha source"),
            ],
        })
        rendered = render_index(assets_path)
        evidence_at = rendered.index("alpha-evidence-v1")
        alpha_source_at = rendered.index("alpha-source-v1")
        zeta_at = rendered.index("zeta-source-v1")
        self.assertLess(evidence_at, alpha_source_at)
        self.assertLess(alpha_source_at, zeta_at)
        self.assertIn("\\*this\\*", rendered)
        self.assertIn("\\<script\\>", rendered)
        self.assertNotIn("<script>", rendered)
        self.assertIn("\\[link\\]", rendered)
        self.assertNotIn(str(assets_path.parent), rendered)
        self.assertIn("not admission or source parity", rendered.lower())

    def test_passed_synthetic_tests_claim_is_shown_only_as_that_scope(self):
        evidence = self.evidence_asset()
        source = self.source_asset(
            claims=[
                {
                    "scope": "synthetic_tests",
                    "result": "passed",
                    "evidence_ids": ["example-test-log-v1"],
                    "limitations": ["Does not establish source parity"],
                },
                {
                    "scope": "review",
                    "result": "pending",
                    "evidence_ids": ["example-test-log-v1"],
                    "limitations": ["Review not complete"],
                },
                {
                    "scope": "source_parity",
                    "result": "failed",
                    "evidence_ids": ["example-test-log-v1"],
                    "limitations": ["Bytes differ"],
                },
            ]
        )
        assets_path, _, _ = self.write_inventory(
            {"schema_version": 1, "assets": [source, evidence]}
        )
        rendered = render_index(assets_path)
        self.assertIn("synthetic_tests", rendered)
        self.assertIn("passed", rendered)
        self.assertIn("pending", rendered)
        self.assertIn("failed", rendered)
        self.assertIn("review", rendered)
        self.assertIn("source_parity", rendered)
        self.assertIn("example-test-log-v1", rendered)
        self.assertNotRegex(
            rendered,
            r"(?i)(qualified for admission|ready for live|overall readiness)",
        )
        claim_block = rendered[rendered.index("synthetic_tests"):]
        self.assertNotRegex(
            claim_block.split("review", 1)[0],
            r"(?i)source parity established",
        )

    def test_identical_inputs_render_identical_output(self):
        assets_doc = {
            "schema_version": 1,
            "assets": [self.source_asset(), self.evidence_asset()],
        }
        first, _, _ = self.write_inventory(assets_doc)
        second, _, _ = self.write_inventory(assets_doc)
        self.assertEqual(render_index(first), render_index(second))
        self.assertEqual(render_index(first), render_index(first))

    def test_render_index_rejects_malformed_inventory(self):
        assets_path, _, _ = self.write_inventory(
            {"schema_version": 1, "assets": [self.source_asset(parents=["missing"])]}
        )
        with self.assertRaises(ValueError):
            render_index(assets_path)

    def test_cli_success_integrity_failure_and_unreadable_json(self):
        assets_path, locations_path, member_path = self.make_registry()
        before = {
            assets_path: assets_path.read_bytes(),
            locations_path: locations_path.read_bytes(),
            member_path: member_path.read_bytes(),
        }

        success = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "validate",
                "--assets",
                str(assets_path),
                "--locations",
                str(locations_path),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(success.returncode, 0, success.stderr)
        payload = json.loads(success.stdout)
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(payload["findings"], [])

        index = subprocess.run(
            [sys.executable, str(SCRIPT), "index", "--assets", str(assets_path)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(index.returncode, 0, index.stderr)
        self.assertIn("example-source-v1", index.stdout)
        self.assertIn("Synthetic source", index.stdout)

        member_path.write_bytes(b"changed")
        integrity = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "validate",
                "--assets",
                str(assets_path),
                "--locations",
                str(locations_path),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(integrity.returncode, 1, integrity.stderr)
        integrity_payload = json.loads(integrity.stdout)
        self.assertEqual(integrity_payload["schema_version"], 1)
        self.assertIn(
            "HASH_MISMATCH",
            {item["code"] for item in integrity_payload["findings"]},
        )
        member_path.write_bytes(before[member_path])

        assets_path.write_text("{not json", encoding="utf-8")
        unreadable = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "validate",
                "--assets",
                str(assets_path),
                "--locations",
                str(locations_path),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(unreadable.returncode, 2)
        assets_path.write_bytes(before[assets_path])

        malformed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "index",
                "--assets",
                str(assets_path.parent / "missing-assets.json"),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(malformed.returncode, 2)

        after = {
            assets_path: assets_path.read_bytes(),
            locations_path: locations_path.read_bytes(),
            member_path: member_path.read_bytes(),
        }
        self.assertEqual(before, after)

    def test_cli_usage_without_paths_exits_two(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "validate"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
