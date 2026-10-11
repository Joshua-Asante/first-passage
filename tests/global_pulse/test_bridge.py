"""Synthetic bridge contracts; no market data, empirical tests or admission."""
from copy import deepcopy
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

from scripts.evidence_store.store import Store
from scripts.global_pulse import bridge as b
from scripts.global_pulse.__main__ import main
from scripts.research_asset_registry import validate_registry

FIXTURES = Path(__file__).parent / "fixtures"
REPO = Path(__file__).resolve().parents[2]


@pytest.fixture
def inputs(tmp_path):
    root = tmp_path / "input"
    shutil.copytree(FIXTURES, root)
    return b.decode((root / "packet.json").read_bytes()), root, tmp_path / "captures"


def test_daily_live_unknown_timing_and_limits(inputs):
    p, root, output = inputs
    bundle = b.capture(p, root, output)
    retained = b.verify_bundle(bundle)
    daily, live = retained["measurements"]
    assert daily["observed_at"] != live["observed_at"]
    assert daily["published_at"] is daily["available_at"] is None
    assert live["published_at"] is live["available_at"] is None
    warnings = b.validate(p, root)["limitations"]
    assert any("Prior data exposure is unknown" in s for s in warnings)
    assert any("no declared age policy" in s for s in warnings)
    assert not any("EXCEEDED" in s for s in warnings)


@pytest.mark.parametrize("field,value,error", [
    ("series_id", "unknown", "unknown series"),
    ("unit", "percent", "incorrect units"),
    ("definition", "change", "ambiguous measurement"),
    ("convention_id", "daily-change", "unknown measurement convention"),
    ("value", True, "finite value"),
    ("value", float("nan"), "finite value"),
    ("observed_at", "2026-10-09T16:00:00", "timezone-aware"),
    ("observed_at", "2026-10-11T16:00:00Z", "impossible measurement"),
    ("window_start", "2026-10-10T16:00:00Z", "impossible measurement"),
    ("window_end", "2026-10-10T16:00:00Z", "impossible measurement"),
    ("published_at", "2026-10-09T15:59:59Z", "impossible published_at"),
    ("available_at", "2026-10-11T00:00:00Z", "impossible available_at"),
    ("evidence_ids", ["missing"], "unknown/missing evidence"),
])
def test_measurement_failures(inputs, field, value, error):
    p, root, _ = inputs
    p["measurements"][0][field] = value
    with pytest.raises(ValueError, match=error):
        b.validate(p, root)


@pytest.mark.parametrize("field,value", [
    ("schema_version", True), ("captured_at", "2026-10-10T14:30:00"),
    ("observation_id", "../escape"), ("measurements", []), ("evidence", []),
    ("prior_exposure", None), ("limitations", "none"),
])
def test_packet_structure(inputs, field, value):
    p, root, _ = inputs
    p[field] = value
    with pytest.raises(ValueError):
        b.validate(p, root)


def test_unknown_and_duplicate_fields_rejected(inputs):
    p, root, _ = inputs
    p["trial_count"] = 0
    with pytest.raises(ValueError, match="expected fields"):
        b.validate(p, root)
    with pytest.raises(ValueError, match="duplicate JSON key"):
        b.decode('{"schema_version": 1, "schema_version": 2}')


def test_impossible_availability(inputs):
    p, root, _ = inputs
    p["measurements"][0].update(published_at="2026-10-09T17:00:00Z", available_at="2026-10-09T16:30:00Z")
    with pytest.raises(ValueError, match="availability precedes publication"):
        b.validate(p, root)


@pytest.mark.parametrize("target", ["registry.json", "synthetic.csv"])
@pytest.mark.parametrize("failure", ["missing", "corrupt"])
def test_references_must_resolve(inputs, target, failure):
    p, root, _ = inputs
    if failure == "missing":
        (root / target).unlink()
    else:
        (root / target).write_text("corrupt")
    with pytest.raises(ValueError, match="missing local file|hash mismatch"):
        b.validate(p, root)


def test_production_registry_is_not_silently_adopted(inputs):
    p, root, _ = inputs
    registry = b.decode((root / "registry.json").read_bytes())
    registry["synthetic"] = False
    (root / "registry.json").write_bytes(b.encoded(registry))
    p["watchlist"]["sha256"] = b.digest(b.encoded(registry))
    with pytest.raises(ValueError, match="production registry adapter pending"):
        b.validate(p, root)


@pytest.mark.parametrize("damage", ["missing", "corrupt", "replacement"])
def test_verification_rechecks_correction_lineage(inputs, damage):
    p, root, output = inputs
    original = b.capture(p, root, output)
    current = p
    for suffix in ("correction", "successor"):
        changed = deepcopy(current)
        changed["observation_id"] = p["observation_id"] + "-" + suffix
        changed["correction"] = dict(
            predecessor_id=current["observation_id"],
            predecessor_sha256=b.digest((output / current["observation_id"] / "packet.json").read_bytes()),
            changes=["interpretation corrected"])
        successor = b.capture(changed, root, output)
        current = changed
    assert b.verify_bundle(successor) == current
    if damage == "corrupt":
        (original / "packet.json").write_bytes(b"corrupt")
    else:
        original.rename(output / "retired-original")
        if damage == "replacement":
            replacement = deepcopy(p)
            replacement["interpretation"]["observation"] = "Replacement with a different hash."
            b.capture(replacement, root, output)
    with pytest.raises((ValueError, OSError)):
        b.verify_bundle(successor)


@pytest.mark.parametrize("command", ["validate", "finalize"])
def test_cli_invalid_utf8_returns_json_error(tmp_path, capsys, command):
    from scripts.global_pulse.__main__ import main

    bad = tmp_path / "bad.json"
    bad.write_bytes(b'{"bad": "\xff"}')
    args = (["validate", "--packet", str(bad), "--input-root", str(tmp_path)]
            if command == "validate" else
            ["finalize", "--bundle", str(tmp_path), "--routing", str(bad),
             "--notice-dir", str(tmp_path / "notices")])
    assert main(args) == 2
    captured = capsys.readouterr()
    assert not captured.out
    error = b.decode(captured.err)
    assert error["valid"] is False and "decode" in error["error"]


@pytest.mark.parametrize("alter_packet", [False, True])
def test_copied_bundle_must_bind_its_own_root(inputs, tmp_path, alter_packet):
    p, root, output = inputs
    original = b.capture(p, root, output)
    copied = tmp_path / "copy" / original.name
    shutil.copytree(original, copied)
    if alter_packet:
        changed = deepcopy(p)
        changed["author"] = "Changed in copy only"
        (copied / "packet.json").write_bytes(b.encoded(changed))
    with pytest.raises(ValueError, match="capture root"):
        b.verify_bundle(copied)
    locations = b.decode((copied / "locations.json").read_bytes())
    locations["roots"]["capture"] = str(copied.resolve())
    (copied / "locations.json").write_bytes(b.encoded(locations))
    if alter_packet:
        with pytest.raises(ValueError, match="HASH_MISMATCH"):
            b.verify_bundle(copied)
    else:
        assert b.verify_bundle(copied) == p


@pytest.mark.skipif(sys.platform != "win32", reason="NTFS junction regression")
def test_input_junction_cannot_escape_root(tmp_path):
    root = tmp_path / "input"
    outside = tmp_path / "outside"
    root.mkdir()
    outside.mkdir()
    (outside / "evidence.txt").write_text("test", encoding="utf-8")
    junction = root / "junction"
    subprocess.run(["cmd", "/c", "mklink", "/J", str(junction), str(outside)],
                   check=True, capture_output=True)
    try:
        with pytest.raises(ValueError, match="escapes input root"):
            b.local_file(root, "junction/evidence.txt")
    finally:
        junction.rmdir()


def test_packet_locator_cannot_borrow_another_file_hash(inputs):
    p, root, output = inputs
    bundle = b.capture(p, root, output)
    original = (bundle / "packet.json").read_bytes()
    (bundle / "original-packet.json").write_bytes(original)
    changed = deepcopy(p)
    changed["author"] = "Altered packet with redirected locator"
    (bundle / "packet.json").write_bytes(b.encoded(changed))
    locations = b.decode((bundle / "locations.json").read_bytes())
    locations["locations"][0]["relative_path"] = "original-packet.json"
    (bundle / "locations.json").write_bytes(b.encoded(locations))
    with pytest.raises(ValueError, match="capture locations"):
        b.verify_bundle(bundle)


def test_unsafe_paths(inputs):
    p, root, _ = inputs
    p["evidence"][0]["path"] = "../synthetic.csv"
    with pytest.raises(ValueError, match="unsafe local path"):
        b.validate(p, root)


def test_symlinks(inputs):
    p, root, _ = inputs
    p["evidence"][0]["path"] = "link.csv"
    try:
        (root / "link.csv").symlink_to(root / "synthetic.csv")
    except OSError as exc:
        if getattr(exc, "winerror", None) == 1314:
            pytest.skip("Windows symlink creation privilege is unavailable")
        raise
    with pytest.raises(ValueError, match="symlink"):
        b.validate(p, root)


@pytest.mark.parametrize("body_fails", [False, True])
def test_writer_releases_owned_lock_and_preserves_competing_lock(tmp_path, body_fails):
    lock = tmp_path / "writer.lock"

    def use_writer():
        with b.writer(tmp_path):
            assert lock.exists()
            with pytest.raises(FileExistsError):
                with b.writer(tmp_path):
                    pytest.fail("competing writer entered")
            assert lock.exists()
            if body_fails:
                raise ValueError("body failure")

    if body_fails:
        with pytest.raises(ValueError, match="body failure"):
            use_writer()
    else:
        use_writer()
    assert not lock.exists()
    with b.writer(tmp_path):
        assert lock.exists()


def test_declared_age_policy_is_limitation_not_invalidity(inputs):
    p, root, _ = inputs
    p["captured_at"] = "2026-10-10T15:00:00Z"
    assert any("EXCEEDED" in s for s in b.validate(p, root)["limitations"])


def test_transformation_and_known_availability_are_preserved(inputs):
    p, root, output = inputs
    registry = b.decode((root / "registry.json").read_bytes())
    convention = dict(definition="100 * (last / first - 1); first=100, last=101; synthetic endpoints.",
                      output_unit="percent")
    registry["series"][0]["conventions"]["percent_change"] = convention
    (root / "registry.json").write_bytes(b.encoded(registry))
    p["watchlist"]["sha256"] = b.digest(b.encoded(registry))
    p["measurements"][0].update(value=1, unit="percent", convention_id="percent_change",
                                definition=convention["definition"], window_start="2026-10-08T16:00:00Z",
                                published_at="2026-10-09T16:01:00Z", available_at="2026-10-09T16:02:00Z")
    bundle = b.capture(p, root, output)
    assert b.verify_bundle(bundle)["measurements"][0] == p["measurements"][0]
    assert convention["definition"] in b.draft(bundle).read_text(encoding="utf-8")


def test_missing_draft_markers_and_changed_identity_fail(inputs):
    p, root, output = inputs
    bundle = b.capture(p, root, output)
    path = b.draft(bundle)
    original = path.read_text(encoding="utf-8")
    hold = b.decode((root / "hold.json").read_bytes())
    path.write_text(original.replace(b.ROUTE_START, ""), encoding="utf-8")
    with pytest.raises(ValueError, match="routing markers"):
        b.finalize(bundle, hold, output / "notices")
    path.write_text(original.replace(b.notice_id(p), "N-2026-10-10-other"), encoding="utf-8")
    with pytest.raises(ValueError, match="identity was edited"):
        b.finalize(bundle, hold, output / "notices")


def test_forged_limitations_fail_even_with_updated_inventory(inputs):
    p, root, output = inputs
    bundle = b.capture(p, root, output)
    changed = b.encoded({"limitations": []})
    (bundle / "validation.json").write_bytes(changed)
    assets = b.decode((bundle / "assets.json").read_bytes())
    for asset in assets["assets"]:
        if asset["label"] == "validation.json":
            asset["members"][0]["sha256"] = b.digest(changed)
    (bundle / "assets.json").write_bytes(b.encoded(assets))
    with pytest.raises(ValueError, match="retained limitations differ"):
        b.verify_bundle(bundle)


def test_declared_exposure_survives(inputs):
    p, root, output = inputs
    p["prior_exposure"] = dict(status="declared", note="Synthetic manual scan; no trial count assigned.",
                               windows=[dict(start="2026-09-01T00:00:00Z", end="2026-09-30T00:00:00Z",
                                             activity="Systematic scan already inspected", series_ids=["SYNTH-DAILY"])])
    bundle = b.capture(p, root, output)
    assert "Systematic scan already inspected" in b.draft(bundle).read_text(encoding="utf-8")


def test_capture_duplicate_and_correction_preserve_predecessor(inputs):
    p, root, output = inputs
    bundle = b.capture(p, root, output)
    original = (bundle / "packet.json").read_bytes()
    assert b.capture(p, root, output) == bundle
    assert len(list(output.iterdir())) == 1
    changed = deepcopy(p)
    changed["interpretation"]["observation"] = "Corrected synthetic description."
    with pytest.raises(ValueError, match="already captured"):
        b.capture(changed, root, output)
    changed["observation_id"] += "-correction"
    changed["correction"] = dict(predecessor_id=p["observation_id"], predecessor_sha256=b.digest(original),
                                 changes=["interpretation.observation: corrected description"])
    successor = b.capture(changed, root, output)
    assert (bundle / "packet.json").read_bytes() == original
    assert b.verify_bundle(successor)["correction"]["predecessor_id"] == p["observation_id"]
    assert "corrected description" in b.draft(successor).read_text(encoding="utf-8")


@pytest.mark.parametrize("failure", ["missing", "hash", "earlier"])
def test_correction_invalid_predecessor(inputs, failure):
    p, root, output = inputs
    original = b.capture(p, root, output)
    changed = deepcopy(p)
    changed["observation_id"] += "-correction"
    changed["correction"] = dict(predecessor_id=p["observation_id"],
                                 predecessor_sha256=b.digest((original / "packet.json").read_bytes()), changes=["description"])
    if failure == "missing":
        changed["correction"]["predecessor_id"] += "-missing"
    elif failure == "hash":
        changed["correction"]["predecessor_sha256"] = "0" * 64
    else:
        changed["captured_at"] = "2026-10-10T14:29:00Z"
    with pytest.raises((ValueError, OSError)):
        b.capture(changed, root, output)
    assert not (output / changed["observation_id"]).exists()


def test_retained_evidence_integrity_after_input_disappears(inputs):
    p, root, output = inputs
    bundle = b.capture(p, root, output)
    shutil.rmtree(root)
    assert b.verify_bundle(bundle) == p
    (bundle / "artifact-0.bin").write_text("corrupt")
    with pytest.raises(ValueError, match="HASH_MISMATCH"):
        b.draft(bundle)


def test_edited_notice_protected_and_explicit_route_required(inputs):
    p, root, output = inputs
    bundle = b.capture(p, root, output)
    draft = b.draft(bundle)
    original = draft.read_text(encoding="utf-8")
    assert "Decision: PENDING" in original
    assert "GRADUATED to" not in original
    assert "Synthetic daily proxy" in original
    assert "Synthetic continuous future" in original
    edited = "Manually edited observation — 日本."
    draft.write_text(original.replace(p["interpretation"]["observation"], edited), encoding="utf-8")
    assert "Manually edited" in b.draft(bundle).read_text(encoding="utf-8")
    hold = b.decode((root / "hold.json").read_bytes())
    notice = b.finalize(bundle, hold, output / "notices")
    assert edited in notice.read_text(encoding="utf-8")
    assert "Decision: HOLD" in notice.read_text(encoding="utf-8")
    notice.write_text(notice.read_text(encoding="utf-8") + "\nEdited final Notice.\n", encoding="utf-8")
    with pytest.raises(ValueError, match="already exists"):
        b.finalize(bundle, hold, output / "notices")
    with pytest.raises(ValueError, match="different destination"):
        b.finalize(bundle, hold, output / "other-notices")
    assert notice.read_text(encoding="utf-8").endswith("Edited final Notice.\n")


@pytest.mark.parametrize("choice,investigation", [("DROP", None), ("GRADUATE", "PENDING"), ("GRADUATE", "Q-SYNTH-1")])
def test_explicit_routing(inputs, choice, investigation):
    p, root, output = inputs
    bundle = b.capture(p, root, output)
    b.draft(bundle)
    route = dict(decision=choice, reason="Synthetic supplied reason.", reconsider_on=None,
                 reconsider_when=None, investigation=investigation)
    notice = b.finalize(bundle, route, output / "notices")
    assert f"Decision: {choice}" in notice.read_text(encoding="utf-8")
    assert not (output / "discovery_manifests").exists()
    assert not (output / ".evidence").exists()


@pytest.mark.parametrize("choice,investigation", [("HOLD", None), ("GRADUATE", None), ("PENDING", None)])
def test_incomplete_routing_rejected(choice, investigation):
    with pytest.raises(ValueError):
        b.routing(dict(decision=choice, reason="A reason", reconsider_on=None, reconsider_when=None,
                       investigation=investigation))


def test_end_to_end_native_provenance_and_notice_checker(inputs):
    p, root, output = inputs
    bundle = b.capture(p, root, output)
    assert not validate_registry(bundle / "assets.json", bundle / "locations.json")
    b.draft(bundle)
    notice = b.finalize(bundle, b.decode((root / "hold.json").read_bytes()), output / "notices")
    checked = subprocess.run([sys.executable, str(REPO / ".claude/skills/brief-authoring/scripts/check_brief.py"),
                              str(notice), "--type", "notice"], capture_output=True, text=True)
    assert checked.returncode == 0, checked.stdout + checked.stderr
    store = Store(output, output / ".evidence")
    captured = store.capture("global-pulse:" + p["observation_id"],
                             str((bundle / "packet.json").relative_to(output)), "observation")
    assert captured["sha256"] == b.digest(b.encoded(p))
    assert store.source(captured["version_id"])
    graph = store.export()
    assert all(node["label"] in ("Source", "SourceVersion") for node in graph["nodes"])
    assert not graph["edges"] or all(edge["type"] == "VERSION_OF" for edge in graph["edges"])


def test_cli_separates_limitations_and_errors(inputs, capsys):
    p, root, output = inputs
    assert main(["validate", "--packet", str(root / "packet.json"), "--input-root", str(root)]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["valid"] and result["limitations"]
    (root / "registry.json").unlink()
    assert main(["capture", "--packet", str(root / "packet.json"), "--input-root", str(root),
                 "--output", str(output)]) == 2
    assert json.loads(capsys.readouterr().err)["valid"] is False
    assert not output.exists()
