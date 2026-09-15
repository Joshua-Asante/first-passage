"""Synthetic independently pinned admission contracts, never private sources."""
import hashlib
import json
from dataclasses import replace

import pytest

from c1_signal_daemon.book_bundle_intake import admit_bundle, run_bundle_parity
from c1_signal_daemon.book_adapters import ADAPTER_BY_LEG


def digest(data):
    return hashlib.sha256(data).hexdigest()


@pytest.fixture
def candidate(tmp_path, monkeypatch):
    artifacts = {}
    for name in ("pine", "port", "csv", "inputs", "properties", "attestation",
                 "normalization", "reconciliation", "coverage", "panel", "margin"):
        path = tmp_path / name
        path.write_text("synthetic " + name, encoding="utf-8")
        artifacts[name] = {"path": name, "sha256": digest(path.read_bytes())}
    monkeypatch.setitem(ADAPTER_BY_LEG, "orb_mnq_v7", replace(
        ADAPTER_BY_LEG["orb_mnq_v7"], pine_sha256=artifacts["pine"]["sha256"]))
    manifest = {
        "schema": "book-bundle-v1", "bundle_id": "O-N", "leg_id": "orb_mnq_v7",
        "artifacts": artifacts,
        "adapter_overrides": {"qty": 1, "use_scale_in": True},
        "emulator_overrides": {"initial_capital": 100000, "margin_pct": .1,
                               "commission_per_side": .91, "slippage_ticks": 1,
                               "orders_on_close": True},
        "sizing": {"mode": "normal", "lifecycle_tier": "AUTHORIZED", "cap_alloc": 3,
                   "risk_dollars": 0, "pointvalue": 2},
        "chart_timezone": "America/New_York", "normalization_version": "tv_trade_ledger-v1",
        "window": {"start": "2022-09-01T00:00:00+00:00", "end": "2026-09-03T00:00:00+00:00"},
        "startup": {"kind": "cold_at_panel_origin", "first_bar": "2022-09-01T00:00:00+00:00",
                    "coverage_verdict": "PASS"},
        "verdicts": {"source_state": "PASS", "normalization": "PASS",
                     "reconciliation": "PASS", "coverage": "PASS", "margin": "PASS"},
        "approved_deviations": [],
    }
    return tmp_path, manifest


def pin(candidate):
    root, manifest = candidate
    path = root / "candidate.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    contract = root / "trusted.json"
    contract.write_text(json.dumps({"schema": "book-bundle-admissions-v1", "reviewed_by": "synthetic-reviewer",
                                    "bundles": {manifest["bundle_id"]: digest(path.read_bytes())}}), encoding="utf-8")
    return path, contract, digest(contract.read_bytes())


def admit(candidate, pins):
    path, contract, contract_sha = pins
    return admit_bundle(path, trusted_contract_path=contract,
                        trusted_contract_sha256=contract_sha, evidence_root=candidate[0])


def test_only_separately_pinned_manifest_is_admitted(candidate):
    pins = pin(candidate)
    bundle = admit(candidate, pins)
    assert bundle.bundle_id == "O-N"
    assert bundle.manifest_sha256 == digest(pins[0].read_bytes())
    candidate[1]["adapter_overrides"]["qty"] = 2
    pins[0].write_text(json.dumps(candidate[1]))
    with pytest.raises(ValueError, match="manifest_not_admitted"):
        admit(candidate, pins)


@pytest.mark.parametrize("artifact", ["pine", "port", "csv", "inputs", "properties", "panel", "attestation"])
def test_changed_evidence_cannot_use_old_admission(candidate, artifact):
    pins = pin(candidate)
    (candidate[0] / artifact).write_text("changed")
    with pytest.raises(ValueError, match="artifact_identity"):
        admit(candidate, pins)


def test_candidate_cannot_supply_its_own_approval(candidate):
    pins = pin(candidate)
    pins[1].write_text(json.dumps({"schema": "book-bundle-admissions-v1", "bundles": {"O-N": "0" * 64}}))
    with pytest.raises(ValueError, match="trusted_contract_identity"):
        admit(candidate, pins)


@pytest.mark.parametrize("mutation", ["warmup", "reconciliation", "timezone", "margin", "traversal"])
def test_incomplete_or_invalid_even_if_digest_pinned(candidate, mutation):
    manifest = candidate[1]
    if mutation == "warmup":
        del manifest["startup"]
    elif mutation == "timezone":
        manifest["chart_timezone"] = "UTC"
    elif mutation == "traversal":
        manifest["artifacts"]["csv"]["path"] = "../outside.csv"
    else:
        manifest["verdicts"][mutation] = "UNPROVEN"
    with pytest.raises(ValueError):
        admit(candidate, pin(candidate))


def test_runner_requires_the_external_trust_digest(candidate):
    bundle = admit(candidate, pin(candidate))
    with pytest.raises(ValueError, match="execution_trust_mismatch"):
        run_bundle_parity(bundle, trusted_contract_sha256="0" * 64)


def test_runner_does_not_fall_back_to_an_unadmitted_port(candidate, monkeypatch):
    bundle = admit(candidate, pin(candidate))
    monkeypatch.setenv("FP_PORT_ROOT", str(candidate[0] / "different-ports"))
    with pytest.raises(ValueError, match="admitted_port_path_mismatch"):
        run_bundle_parity(bundle, trusted_contract_sha256=bundle.trusted_contract_sha256)


@pytest.fixture
def replay_candidate(candidate, monkeypatch):
    root, manifest = candidate
    source = '''from c1_signal_daemon.book_protocol import OrderIntent, Side, FillTiming
LEG_ID = "orb_mnq_v7"
PINE_SHA256 = "PIN"
class Adapter:
    leg_id = LEG_ID
    def __init__(self):
        self.calls = 0
        self.fills = 0
    def on_bar(self, bar):
        self.calls += 1
        if self.calls == 1:
            return [OrderIntent("entry", LEG_ID, "entry", Side.BUY, 1, timing=FillTiming.THIS_CLOSE)]
        assert self.fills == 1
        return [OrderIntent("exit", LEG_ID, "flat", Side.SELL, None, timing=FillTiming.THIS_CLOSE)]
    def on_execution(self, event):
        assert event.event == "fill"
        self.fills += 1
    def checkpoint(self):
        return {"fills": self.fills}
def build(**kwargs):
    return Adapter()
'''.replace('"PIN"', '"' + manifest["artifacts"]["pine"]["sha256"] + '"')
    files = {
        "port": source,
        "panel": "time,open,high,low,close,volume\n2022-09-01T00:00:00Z,100,101,99,100,1\n"
                 "2022-09-01T00:15:00Z,101,102,100,101,1\n",
        "csv": "Trade number,Type,Date and time,Signal,Price USD,Size (qty),Net PnL USD,Commission USD\n"
               "1,Entry long,2022-08-31 20:00,entry,100.25,1,-0.82,1.82\n"
               "1,Exit long,2022-08-31 20:15,exit,100.75,1,-0.82,1.82\n",
    }
    for key, content in files.items():
        name = "orb_mnq_v7.py" if key == "port" else key
        (root / name).write_text(content, encoding="utf-8")
        manifest["artifacts"][key] = {"path": name, "sha256": digest((root / name).read_bytes())}
    manifest["window"]["end"] = "2022-09-01T00:15:00+00:00"
    monkeypatch.setenv("FP_PORT_ROOT", str(root))
    monkeypatch.setenv("FP_BAR_DATA_DIR", str(root / "wrong-panel"))
    monkeypatch.setenv("FP_TV_EXPORT_DIR", str(root / "wrong-export"))
    return candidate


def test_admitted_replay_uses_exact_bytes_and_confirmed_fills(replay_candidate):
    bundle = admit(replay_candidate, pin(replay_candidate))
    result = run_bundle_parity(bundle, trusted_contract_sha256=bundle.trusted_contract_sha256)
    assert result["passed"]
    assert result["parity"]["matched"] == 1
    assert result["phases"] == {"bars": 2, "margin_phase_checks": 6}


@pytest.mark.parametrize("change,reason", [("open", "incomplete_export"),
                                           ("fractional", "invalid_export_quantity"),
                                           ("truncated", "panel_end_mismatch"),
                                           ("outside", "excluded_export_trades")])
def test_admitted_replay_cannot_hide_incomplete_evidence(replay_candidate, change, reason):
    root, manifest = replay_candidate
    key = "panel" if change == "truncated" else "csv"
    path = root / manifest["artifacts"][key]["path"]
    text = path.read_text()
    if change in ("open", "truncated"):
        text = "\n".join(text.splitlines()[:-1]) + "\n"
    elif change == "fractional":
        text = text.replace(",1,-0.82", ",1.5,-0.82")
    else:
        text = text.replace("2022-08-31 20:00", "2022-08-30 20:00")
    path.write_text(text)
    manifest["artifacts"][key]["sha256"] = digest(path.read_bytes())
    bundle = admit(replay_candidate, pin(replay_candidate))
    with pytest.raises(ValueError, match=reason):
        run_bundle_parity(bundle, trusted_contract_sha256=bundle.trusted_contract_sha256)
