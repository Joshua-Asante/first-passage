"""Real manifest membership, explicit roll acceptance and source-byte boundaries."""

from dataclasses import FrozenInstanceError
from hashlib import sha256
import json

import pytest

from research_utils import tv_trade_ledger as ledger
from research_utils.trade_reconciliation import analyze_venue, reconstruct_trades
from test_tv_trade_ledger import _spec_dict, _FEE_PATH, _unresolved_roll_policy
from test_trade_reconciliation import _event
import pandas as pd


OBLIGATIONS = [
    "Phase 3 pre-registration states back-adjustment seam risk as a limitation of every campaign claim: fills cannot be attributed to a contract month, and a seam crossing is indistinguishable from a price move.",
    "A Phase 6 seam-sensitivity check is pre-registered with its severity frozen alongside the other Phase 6 cutoffs.",
]
RULING_REF = "Operator ruling 2026-09-03; docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md §6 D13(b)."


def accepted_policy():
    return {"disposition": "ACCEPTED_UNMODELED", "ruling_date": "2026-09-03",
            "ruling_ref": RULING_REF, "obligations": OBLIGATIONS.copy()}


def configuration(tmp_path, *, policy=False):
    payload = {"claim_class": "EXPLORATORY", "platform": "synthetic TV export",
               "strategies": [_spec_dict("fixture", "source.csv", "source.pine")],
               "dropped_sources": [], "continuous_contract_roll_policy": _unresolved_roll_policy()}
    payload["strategies"][0]["source_timezone"] = "America/New_York"
    if policy:
        payload["continuous_contract_roll_policy"] = accepted_policy()
    path = tmp_path / "config.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path, payload


def pinned_configuration(tmp_path, monkeypatch, *, target="core/strategies/candidates/source.pine"):
    path, payload = configuration(tmp_path)
    payload["strategies"][0].update(pine_pin_status="PINNED_RESEARCH_VARIANT",
                                    pin_ref=f"core/strategies/PORT_MANIFEST.sha256:{target}",
                                    pin_divergence="synthetic changed parameter")
    path.write_text(json.dumps(payload), encoding="utf-8")
    manifest = tmp_path / "PORT_MANIFEST.sha256"
    manifest.write_text(f"# synthetic pins\n\n{sha256(b'pine').hexdigest()}  {target}\n", encoding="utf-8")
    monkeypatch.setattr(ledger, "_PORT_MANIFEST_PATH", manifest, raising=False)
    return path, payload, manifest


def test_manifest_owns_directory_placement_not_candidates_prefix(tmp_path, monkeypatch):
    path, _, _ = pinned_configuration(tmp_path, monkeypatch, target="core/research/body/source.pine")
    assert ledger.load_source_inventory(path).specs[0].pin_ref.endswith("core/research/body/source.pine")


@pytest.mark.parametrize("mutation, message", [
    ("dangling", "not found in PORT_MANIFEST"),
    ("hash", "pin hash mismatch"),
    ("malformed", "invalid PORT_MANIFEST row"),
    ("duplicate", "duplicate PORT_MANIFEST path"),
    ("conflicting", "duplicate PORT_MANIFEST path"),
    ("traversal", "safe normalized repo-relative"),
    ("absolute", "safe normalized repo-relative"),
    ("backslash", "safe normalized repo-relative"),
    ("dot", "safe normalized repo-relative"),
    ("basename", "pin basename mismatch"),
])
def test_manifest_membership_fails_closed(tmp_path, monkeypatch, mutation, message):
    path, payload, manifest = pinned_configuration(tmp_path, monkeypatch)
    assert ledger.load_source_inventory(path).specs[0].strategy_id == "fixture"
    original = manifest.read_text(encoding="utf-8")
    if mutation == "dangling": manifest.write_text("# no pin\n", encoding="utf-8")
    elif mutation == "hash": manifest.write_text(original.replace(sha256(b"pine").hexdigest(), "a" * 64), encoding="utf-8")
    elif mutation == "malformed": manifest.write_text(original + "not a hash row\n", encoding="utf-8")
    elif mutation in {"duplicate", "conflicting"}:
        repeated = original if mutation == "duplicate" else original.replace(sha256(b"pine").hexdigest(), "a" * 64)
        manifest.write_text(original + repeated, encoding="utf-8")
    else:
        targets = {"traversal": "core/../source.pine", "absolute": "/core/source.pine",
                   "backslash": "core\\source.pine", "dot": ".", "basename": "core/strategies/candidates/other.pine"}
        target = targets[mutation]
        payload["strategies"][0]["pin_ref"] = f"core/strategies/PORT_MANIFEST.sha256:{target}"
        path.write_text(json.dumps(payload), encoding="utf-8")
        manifest.write_text(f"{sha256(b'pine').hexdigest()}  {target}\n", encoding="utf-8")
    with pytest.raises(ValueError, match=message):
        ledger.load_source_inventory(path)


def test_modified_body_requires_existing_ancestor_without_claiming_equal_hash(tmp_path, monkeypatch):
    path, payload, manifest = pinned_configuration(tmp_path, monkeypatch)
    payload["strategies"][0].update(pine_pin_status="UNPINNED_MODIFIED", pine_sha256="f" * 64)
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert ledger.load_source_inventory(path).specs[0].pine_sha256 == "f" * 64
    manifest.write_text("", encoding="utf-8")
    with pytest.raises(ValueError, match="not found in PORT_MANIFEST"):
        ledger.load_source_inventory(path)


def test_inventory_reads_real_manifest_exactly_once(tmp_path, monkeypatch):
    path, _, manifest = pinned_configuration(tmp_path, monkeypatch)
    from pathlib import Path
    real_read = Path.read_bytes
    manifest_reads = []

    def counted_read(candidate):
        if candidate == manifest:
            manifest_reads.append(candidate)
        return real_read(candidate)

    monkeypatch.setattr(Path, "read_bytes", counted_read)
    assert ledger.load_source_inventory(path).specs[0].pine_sha256 == sha256(b"pine").hexdigest()
    assert len(manifest_reads) == 1


def test_dropped_pin_metadata_checked_without_opening_dropped_sources(tmp_path, monkeypatch):
    path, payload, manifest = pinned_configuration(tmp_path, monkeypatch)
    payload["dropped_sources"] = [{"strategy_id_as_named_before": "striker_dj30_dropped",
        "export_filename": "absent.csv", "export_sha256": "a" * 64,
        "pine_filename": "absent.pine", "pine_sha256": "b" * 64,
        "pin_ref": "core/strategies/PORT_MANIFEST.sha256:core/research/absent.pine",
        "reason": "SWAP_PORT_BODY_POINT_VALUE_NOT_OVERRIDDEN"}]
    path.write_text(json.dumps(payload), encoding="utf-8")
    with manifest.open("a", encoding="utf-8") as handle:
        handle.write(f"{'b' * 64}  core/research/absent.pine\n")
    assert len(ledger.load_source_inventory(path).dropped_sources) == 1
    manifest.write_text(manifest.read_text().replace("b" * 64, "c" * 64))
    with pytest.raises(ValueError, match="pin hash mismatch"):
        ledger.load_source_inventory(path)


def test_accepted_roll_policy_is_immutable_and_downgrades_only_roll(tmp_path):
    path, _ = configuration(tmp_path, policy=True)
    inventory = ledger.load_source_inventory(path)
    policy = inventory.continuous_contract_roll_policy
    with pytest.raises(FrozenInstanceError):
        policy.disposition = "UNRESOLVED"
    assert policy.obligations == tuple(OBLIGATIONS)
    spec = inventory.specs[0]
    events = pd.DataFrame([_event(1, "ENTRY", row=1), _event(1, "EXIT", row=2, timestamp="2026-01-05 17:00")])
    trades = reconstruct_trades(events, spec).trades
    fees = ledger.load_fee_schedule(_FEE_PATH)
    default = analyze_venue(trades, spec, fees)
    accepted = analyze_venue(trades, spec, fees, continuous_contract_roll_policy=policy)
    original = next(i for i in default.issues if i.code == "CONTINUOUS_CONTRACT_ROLL_UNRESOLVED")
    roll = next(i for i in accepted.issues if i.code == original.code)
    assert original.severity == "BLOCKER"
    assert roll.severity == "WARNING"
    assert roll.detail["disposition"] == "ACCEPTED_UNMODELED"
    assert roll.detail["ruling_ref"] == RULING_REF
    assert roll.detail["obligations"] == tuple(OBLIGATIONS)
    assert accepted.contract_month_attribution_status == accepted.roll_seam_attribution_status == "UNAVAILABLE"
    assert [(i.code, i.severity) for i in accepted.issues if i.code != roll.code] == [
        (i.code, i.severity) for i in default.issues if i.code != roll.code]
    assert any(i.code == "FORCE_FLAT_VIOLATION" and i.severity == "BLOCKER" for i in accepted.issues)


@pytest.mark.parametrize("mutation", ["missing_object", "extra_key", "bad_date", "empty_ref", "missing_obligation", "changed_obligation", "duplicate_obligation", "wrong_disposition"])
def test_roll_policy_rejects_incomplete_acceptance(tmp_path, mutation):
    path, payload = configuration(tmp_path, policy=True)
    assert ledger.load_source_inventory(path).continuous_contract_roll_policy.disposition == "ACCEPTED_UNMODELED"
    policy = payload["continuous_contract_roll_policy"]
    if mutation == "missing_object": payload.pop("continuous_contract_roll_policy")
    elif mutation == "extra_key": policy["extra"] = True
    elif mutation == "bad_date": policy["ruling_date"] = "2026-02-30"
    elif mutation == "empty_ref": policy["ruling_ref"] = " "
    elif mutation == "missing_obligation": policy["obligations"].pop()
    elif mutation == "changed_obligation": policy["obligations"][0] = "We may test later"
    elif mutation == "duplicate_obligation": policy["obligations"][1] = policy["obligations"][0]
    else: policy["disposition"] = "RESOLVED"
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError):
        ledger.load_source_inventory(path)


@pytest.mark.parametrize("kind", ["export", "pine"])
def test_correct_source_hash_cannot_override_wrong_byte_length(tmp_path, kind):
    path, _ = configuration(tmp_path)
    spec = ledger.load_source_inventory(path).specs[0]
    (tmp_path / "source.csv").write_bytes(b"export")
    (tmp_path / "source.pine").write_bytes(b"pine")
    from dataclasses import replace
    spec = replace(spec, **{f"{kind}_bytes": getattr(spec, f"{kind}_bytes") + 1})
    with pytest.raises(ledger.SourceIdentityError, match=r"byte length mismatch: expected .*observed"):
        ledger.verify_source_pair(tmp_path, spec)
