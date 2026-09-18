"""Literal TB-P2 vectors and fail-closed fingerprint consumer checks."""
import copy
import ast
import importlib.util
import json
import sys
from pathlib import Path

import pytest


MODULE = "c1_rail.policy_fingerprint"
VECTORS = Path(__file__).parent / "fixtures/policy_fingerprint_vectors.json"
POLICY = {"instance_key": "tradeify_portfolio@Tradeify_Select_100K",
          "reference_mode": "trailing", "scale": "0.4", "trigger": "0.01"}
PRE = b'"geometry"\nfrom dataclasses import dataclass\nPOLICY_REGISTRY: dict[str, ProtectionPolicy] = {}\nVALUE = 1 # type: int\n'
POST = PRE.replace(b"= {}", b'= {"tradeify_portfolio@Tradeify_Select_100K": ProtectionPolicy(reference_mode="trailing", trigger=0.01, scale=0.40, provenance="synthetic sealed provenance")}')
ROWS = {POLICY["instance_key"]: {"reference_mode": "trailing", "trigger": "0.01",
                                 "scale": "0.4", "provenance": "synthetic sealed provenance"}}
SOURCES = ("core/dd_protection.py", "core/firm_rules.py", "core/lifecycle.py",
           "ops/c1_rail/book_policy.py", "ops/c1_rail/book_sizing_context.py",
           "ops/c1_rail/book_capacity.py", "ops/c1_signal_daemon/book_protocol.py")


@pytest.fixture
def fp():
    return importlib.import_module(MODULE) if importlib.util.find_spec(MODULE) is not None else None


@pytest.fixture
def vectors():
    return json.loads(VECTORS.read_text(encoding="utf-8"))


def packet_inputs():
    # Synthetic artifact bytes; these are not qualification or runtime pins.
    return dict(policy_row=POLICY, geometry_source=PRE, registry_rows={},
                components={name: b"synthetic component\n" for name in SOURCES},
                tool_source=b"synthetic tool\n",
                dependency_artifacts={"runtime/distribution": b"synthetic runtime\n"})


def test_literal_policy_bytes_and_hash(fp, vectors):
    assert fp is not None, "shared fingerprint implementation missing"
    expected = vectors["policy"]
    for row in (POLICY, dict(reversed(list(POLICY.items())))):
        data = fp.canonical_policy_bytes(row)
        assert data == expected["utf8"].encode("utf-8")
        assert fp.sha256_bytes(data) == expected["sha256"]
    assert fp.canonical_policy_bytes({**POLICY, "instance_key": "café@tier"}).startswith(
        b'{"instance_key":"caf\xc3\xa9@tier"')


@pytest.mark.parametrize("change", [
    {"scale": 0.4}, {"scale": True}, {"trigger": None}, {"scale": "0.40"},
    {"trigger": "1e-2"}, {"trigger": "+0.01"}, {"trigger": ".01"},
    {"trigger": "00.01"}, {"scale": "-0"}, {"scale": "NaN"},
    {"scale": "Infinity"}, {"scale": " 0.4"}, {"trigger": "0"},
    {"trigger": "1"}, {"scale": "1.1"}, {"reference_mode": "unknown"},
    {"instance_key": ""}, {"instance_key": "x\n@y"}, {"provenance": "extra"},
])
def test_policy_rejects_ambiguous_or_wrong_fields(fp, change):
    with pytest.raises(ValueError):
        fp.canonical_policy_bytes({**POLICY, **change})


@pytest.mark.parametrize("key", POLICY)
def test_policy_rejects_missing_field(fp, key):
    with pytest.raises(ValueError):
        fp.canonical_policy_bytes({k: v for k, v in POLICY.items() if k != key})


def test_literal_geometry_and_independent_registry_checks(fp, vectors):
    expected = vectors["geometry" if sys.version_info >= (3, 13) else "geometry_pre_313"]
    for source, rows in ((PRE, {}), (POST, ROWS)):
        fp.validate_registry(source, expected_rows=rows)
        data = fp.normalized_geometry_bytes(source)
        assert data == expected["utf8"].encode("utf-8")
        assert fp.sha256_bytes(data) == expected["sha256"]
    assert fp.normalized_geometry_bytes(PRE + b"# ordinary comment\n") == data
    assert fp.normalized_geometry_bytes(PRE.replace(b"\n", b"\r\n")) == data
    with pytest.raises(ValueError):
        fp.validate_registry(POST, expected_rows={})
    with pytest.raises(ValueError):
        fp.validate_registry(POST.replace(b"sealed provenance", b"forged provenance"), expected_rows=ROWS)
    extra = POST.replace(b'provenance")}', b'provenance"), "extra@tier": ProtectionPolicy(reference_mode="trailing", trigger=0.01, scale=0.4, provenance="extra")}')
    with pytest.raises(ValueError):
        fp.validate_registry(extra, expected_rows=ROWS)


@pytest.mark.parametrize("old,new", [
    (b'"geometry"', b'"changed"'), (b"import dataclass", b"import field"),
    (b"VALUE = 1", b"VALUE = 2"), (b"type: int", b"type: str"),
])
def test_unexcluded_ast_mutations_change_identity(fp, old, new):
    assert fp.normalized_geometry_bytes(PRE.replace(old, new)) != fp.normalized_geometry_bytes(PRE)


def test_every_unexcluded_production_top_level_node_is_bound(fp):
    source = (Path(__file__).resolve().parents[2] / "core/dd_geometry.py").read_bytes()
    baseline = fp.sha256_bytes(fp.normalized_geometry_bytes(source))
    tree = ast.parse(source.decode("utf-8"), type_comments=True)
    for index, node in enumerate(tree.body):
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "POLICY_REGISTRY":
            continue
        changed = copy.deepcopy(tree)
        del changed.body[index]
        assert fp.sha256_bytes(fp.normalized_geometry_bytes(ast.unparse(changed).encode("utf-8"))) != baseline


@pytest.mark.parametrize("extra", [
    b"POLICY_REGISTRY = {}\n", b"del POLICY_REGISTRY\n",
    b"alias = POLICY_REGISTRY\n", b"POLICY_REGISTRY.update({})\n",
    b"POLICY_REGISTRY['other'] = None\n", b"POLICY_REGISTRY |= {}\n",
    b"globals()['POLICY_REGISTRY'] = {}\n", b"setattr(module, 'POLICY_REGISTRY', {})\n",
    b"def bad():\n    global POLICY_REGISTRY\n    POLICY_REGISTRY = {}\n",
    b"def bad(POLICY_REGISTRY): pass\n", b"import x as POLICY_REGISTRY\n",
    b"class POLICY_REGISTRY: pass\n", b"def POLICY_REGISTRY(): pass\n",
])
def test_geometry_refuses_registry_rebinding_and_escape(fp, extra):
    with pytest.raises(ValueError):
        fp.normalized_geometry_bytes(PRE + extra)


@pytest.mark.parametrize("source", [
    b"VALUE = 1\n", b"if True:\n    POLICY_REGISTRY = {}\n",
    b"POLICY_REGISTRY = alias = {}\n", b"POLICY_REGISTRY = dict()\n",
    b"POLICY_REGISTRY = {**{}}\n", b"POLICY_REGISTRY = dangerous()\n",
    POST.replace(b"trigger=0.01", b"trigger=True"),
    POST.replace(b"trigger=0.01", b"trigger=" + b"9" * 400),
    POST.replace(b'provenance="synthetic sealed provenance"', b"provenance=run()"),
    PRE.replace(b"dict[str, ProtectionPolicy]", b"side_effect()"),
    b'# coding: latin-1\n"caf\xc3\xa9"\nPOLICY_REGISTRY = {}\n',
    b"\xef\xbb\xbfPOLICY_REGISTRY = {}", b"\xff", b"syntax error!",
])
def test_geometry_rejects_nonliteral_or_invalid_registry(fp, source):
    with pytest.raises(ValueError):
        fp.normalized_geometry_bytes(source)


def test_config_literal_transition(fp, vectors):
    before, after = (vectors[name] for name in ("config_before", "config_after"))
    for vector in (before, after):
        data = vector["utf8"].encode()
        assert fp.canonical_config_bytes(json.loads(data)) == data
        assert fp.sha256_bytes(data) == vector["sha256"]
    fp.validate_initial_arm_delta(before["utf8"].encode(), after["utf8"].encode(),
                                 authorized_deadline="2026-09-14T20:00:00+00:00")


@pytest.mark.parametrize("mutate", [
    lambda c: c.update(cap_alloc=1), lambda c: c.update(account="changed"),
    lambda c: c.update(extra=True), lambda c: c.pop("account"),
    lambda c: c.update(dry_run=0), lambda c: c.update(armed_until="2026-09-15T20:00:00+00:00"),
    lambda c: c["nested"].update(quantity=True), lambda c: c["nested"].update(quantity=1.0),
])
def test_arm_rejects_every_unapproved_change(fp, vectors, mutate):
    before = vectors["config_before"]["utf8"].encode()
    after = json.loads(vectors["config_after"]["utf8"])
    mutate(after)
    with pytest.raises(ValueError):
        fp.validate_initial_arm_delta(before, fp.canonical_config_bytes(after),
                                     authorized_deadline="2026-09-14T20:00:00+00:00")


@pytest.mark.parametrize("data", [b'{"dry_run":true,"dry_run":false}',
                                       b'{"value":NaN}', b'{}\n', b'{ "a":1}',
                                       b'\xef\xbb\xbf{}'])
def test_config_verification_requires_exact_canonical_bytes(fp, data):
    with pytest.raises(ValueError):
        fp.validate_initial_arm_delta(data, b"{}", authorized_deadline="2026-09-14T20:00:00+00:00")


@pytest.mark.parametrize("value", [float("nan"), float("inf"), (1,), {1: "not string"}])
def test_config_rejects_lossy_types(fp, value):
    with pytest.raises(ValueError):
        fp.canonical_config_bytes({"value": value})


def test_complete_manifest_verifier(fp):
    inputs = packet_inputs()
    manifest = fp.build_shared_manifest(**inputs)
    fp.verify_shared_manifest(manifest, **inputs)
    assert set(manifest["shared_components"]) == set(SOURCES) | {"policy_row", "core/dd_geometry.py"}
    assert "ops/c1_rail/policy_fingerprint.py" not in manifest["shared_components"]
    assert manifest["toolchain"]["source_sha256"] == fp.sha256_bytes(inputs["tool_source"])
    post = {**inputs, "geometry_source": POST, "registry_rows": ROWS}
    assert fp.build_shared_manifest(**post) == manifest
    fp.verify_shared_manifest(manifest, **post)


def test_manifest_refuses_a_different_admitted_policy(fp):
    inputs = packet_inputs()
    inputs.update(geometry_source=POST.replace(b"trigger=0.01", b"trigger=0.02"),
                  registry_rows={POLICY["instance_key"]: {**ROWS[POLICY["instance_key"]], "trigger": "0.02"}})
    with pytest.raises(ValueError):
        fp.build_shared_manifest(**inputs)


@pytest.mark.parametrize("field", ["recipe", "runtime", "source_sha256", "dependencies"])
def test_manifest_rejects_runtime_recipe_tool_and_dependency_drift(fp, field):
    inputs = packet_inputs()
    manifest = fp.build_shared_manifest(**inputs)
    manifest["toolchain"][field] = "wrong"
    with pytest.raises(ValueError):
        fp.verify_shared_manifest(manifest, **inputs)


@pytest.mark.parametrize("source", SOURCES)
def test_unexcluded_full_source_bytes_are_bound(fp, source):
    inputs = packet_inputs()
    manifest = fp.build_shared_manifest(**inputs)
    inputs["components"][source] += b"# comment changes full bytes\n"
    with pytest.raises(ValueError):
        fp.verify_shared_manifest(manifest, **inputs)


def test_inventory_cannot_silently_omit_or_reclassify_a_component(fp):
    inputs = packet_inputs()
    manifest = fp.build_shared_manifest(**inputs)
    missing = copy.deepcopy(inputs)
    missing["components"].pop("ops/c1_rail/book_capacity.py")
    with pytest.raises(ValueError):
        fp.build_shared_manifest(**missing)
    bad = copy.deepcopy(manifest)
    bad["shared_components"]["ops/c1_rail/book_policy.py"]["recipe"] = "geometry-ast"
    with pytest.raises(ValueError):
        fp.verify_shared_manifest(bad, **inputs)
    inputs["components"]["../alias"] = b"x"
    with pytest.raises(ValueError):
        fp.build_shared_manifest(**inputs)


def test_actual_geometry_full_source_manifest_and_candidate(fp):
    from c1_rail.book_policy import candidate_book_protection_policy

    root = Path(__file__).resolve().parents[2]
    policy = candidate_book_protection_policy()
    row = {"instance_key": POLICY["instance_key"], "reference_mode": policy.reference_mode,
           "trigger": str(policy.trigger), "scale": str(policy.scale)}
    assert row == POLICY
    inputs = packet_inputs()
    inputs.update(policy_row=row, geometry_source=(root / "core/dd_geometry.py").read_bytes(),
                  components={name: (root / name).read_bytes() for name in SOURCES},
                  tool_source=(root / "ops/c1_rail/policy_fingerprint.py").read_bytes())
    manifest = fp.build_shared_manifest(**inputs)
    fp.verify_shared_manifest(manifest, **inputs)
