"""Migration/preflight are state tools, never a substitute for a real POST."""
import importlib
import json
import hashlib
from uuid import uuid4

import pytest

from c1_sizing_host_reference import generate_constants

LEG = "m1_stage1_test"
KEY = "M1 Stage1 Test"


def control():
    return importlib.import_module("m1_stage1_control")


@pytest.fixture
def inputs(tmp_path):
    cfg = {"dry_run": True, "armed_until": None}
    data = {
        "constants_path": generate_constants("Tradeify_Select_100K"),
        "lifecycle_state_path": {"Striker": "AUTHORIZED"},
        "dd_state_path": {"peak_equity": 100000.},
    }
    for key, value in data.items():
        p = tmp_path / (key + ".json")
        p.write_text(json.dumps(value))
        cfg[key] = str(p)
    cp = tmp_path / "config.json"
    cp.write_text(json.dumps(cfg))
    return cp, cfg


def test_plan_is_readonly_and_apply_only_changes_authorized_rows(inputs):
    mod = control()
    cp, cfg = inputs
    before = cp.read_bytes()
    plan = mod.plan_migration(cfg, enabled=True)
    assert cp.read_bytes() == before
    assert plan["after"]["constants"]["leg_map"][LEG]["cap_alloc"] == 1
    assert plan["after"]["lifecycle"][KEY] == "AUTHORIZED"
    assert plan["after"]["lifecycle"]["Striker"] == "AUTHORIZED"
    with pytest.raises(ValueError, match="flat"):
        mod.apply_migration(cp, plan, flat_verified=False)
    mod.apply_migration(cp, plan, flat_verified=True)
    result = mod.preflight(cfg, 98000.)
    assert result["expected_qty"] == 1
    assert "98000" not in json.dumps(result)
    assert "100000" not in json.dumps(result)
    assert cp.read_bytes() == before
    mod.apply_migration(cp, mod.plan_migration(cfg, enabled=False), flat_verified=True)
    assert json.loads(open(cfg["constants_path"]).read())["leg_map"][LEG]["cap_alloc"] == 0
    assert json.loads(open(cfg["lifecycle_state_path"]).read())[KEY] == "RETIRED"
    with pytest.raises(ValueError, match="nonzero"):
        mod.preflight(cfg, 100000.)


def test_stale_preimage_and_armed_config_refuse_write(inputs):
    mod = control()
    cp, cfg = inputs
    plan = mod.plan_migration(cfg, enabled=True)
    cp.write_text(json.dumps({**cfg, "dry_run": False}))
    with pytest.raises(ValueError):
        mod.apply_migration(cp, plan, flat_verified=True)
    cp.write_text(json.dumps(cfg))
    from pathlib import Path
    Path(cfg["lifecycle_state_path"]).write_text('{}')
    with pytest.raises(ValueError, match="changed"):
        mod.apply_migration(cp, plan, flat_verified=True)


def test_release_is_explicit_not_silent(inputs):
    mod = control()
    _, cfg = inputs
    from pathlib import Path
    p = Path(cfg["constants_path"])
    c = json.loads(p.read_text())
    c["leg_map"]["dj30_mym"]["cap_alloc"] = 69
    c["leg_map"]["nas100_mnq"]["cap_alloc"] = 11
    p.write_text(json.dumps(c))
    with pytest.raises(ValueError, match="cap"):
        mod.plan_migration(cfg, enabled=True)
    plan = mod.plan_migration(cfg, enabled=True, release_withdrawn=True)
    assert sum(r["cap_alloc"] for r in plan["after"]["constants"]["leg_map"].values()) == 1
    assert json.loads(p.read_text()) == c


def test_interrupted_migration_does_not_activate_test(inputs, monkeypatch):
    mod = control()
    cp, cfg = inputs
    plan = mod.plan_migration(cfg, enabled=True)
    original = mod.atomic_write
    n = 0
    def interrupt(path, data):
        nonlocal n
        n += 1
        if n == 2:
            raise OSError("interrupted")
        return original(path, data)
    monkeypatch.setattr(mod, "atomic_write", interrupt)
    with pytest.raises(OSError):
        mod.apply_migration(cp, plan, flat_verified=True)
    from pathlib import Path
    assert json.loads(Path(cfg["constants_path"]).read_text())["leg_map"][LEG]["cap_alloc"] == 0


def proof(operator=False):
    from m1_stage1_contract import OPERATOR_INPUT_SOURCE, contract_sha256
    def digest(value):
        return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    eid = str(uuid4())
    cid = str(uuid4())
    source = (OPERATOR_INPUT_SOURCE if operator else
              {"kind": "offline_fixture", "schema": "ohlcv-1m", "symbol": "MYM1!"})
    manifest = {"ceremony_id": cid, "target": "2026-09-10T14:00:00+00:00",
                "expires": "2026-09-10T14:02:00+00:00", "source": source,
                "contract_sha256": contract_sha256(), "preflight_sha256": "e" * 64,
                "expected_qty": 1, "venue_contract": "MYMZ6"}
    event = "m1-" + digest({k: manifest[k] for k in ("ceremony_id", "target", "contract_sha256", "source")})
    bar = {"timestamp": manifest["target"], "open": 44000., "high": 44002.,
           "low": 43999., "close": 44001., "volume": 7., "venue_contract": "MYMZ6"}
    parsed = {"leg_id": LEG, "signal_type": "entry", "bar_time": event,
              "close": bar["close"], "stop_dist_pts": 1.}
    request_hash = hashlib.sha256(json.dumps(parsed, separators=(",", ":")).encode()).hexdigest()
    item = {"state": "CLOSED", "previous_state": "RESPONSE_RECORDED",
            "manifest": manifest, "manifest_sha256": digest(manifest), "event_identity": event,
            "response": {"http_status": 200, "response_kind": "dry_run_computed",
                         "body_sha256": hashlib.sha256(b"dry_run: computed, not sent\n").hexdigest()},
            "request_sha256": request_hash, "bar": bar,
            "bar_sha256": digest({"bar": bar, "source": source})}
    receipt = {"schema_version": 1, "active": cid, "enabled": False,
               "ceremonies": {cid: item}, "tombstones": {cid: {"event_identity": event}}}
    order_id = LEG + "-entry-" + event
    rows = [
        {"kind": "request_received", "event_id": eid, "order_id": order_id,
         "auth_ok": True, "body_category": "b1_json", "body_sha256": request_hash,
         "parsed": parsed},
        {"kind": "decision", "event_id": eid, "order_id": order_id,
         "leg_id": LEG, "signal_type": "entry", "qty_out": 1, "halt": False,
         "dry_run": True, "sender_invoked": False, "test_only": True,
         "test_contract_sha256": contract_sha256(),
         "current_equity": 123456.789, "secret_key": "DO_NOT_EXPORT"},
        {"kind": "transport_result", "event_id": eid, "order_id": order_id,
         "transport_state": "not_attempted", "dry_run": True},
    ]
    return rows, receipt


def test_evidence_allowlist_and_exact_join():
    mod = control()
    rows, receipt = proof()
    public = mod.project_evidence(rows, receipt)
    assert public["listener_event_id"] == rows[0]["event_id"]
    assert public["observed_qty"] == public["expected_qty"] == 1
    assert public["offline_test_only"] is True and public["qualifying_live_source"] is False
    assert "dry_run_strategy_signal_event_id" not in public
    assert "DO_NOT_EXPORT" not in json.dumps(public)
    assert "123456" not in json.dumps(public)
    assert "order_id" not in public  # needn't publish arbitrary request strings
    rows.append(rows[1])
    with pytest.raises(ValueError):
        mod.project_evidence(rows, receipt)


def test_operator_evidence_reports_attended_source_and_venue_contract():
    rows, receipt = proof(operator=True)
    public = control().project_evidence(rows, receipt)
    assert public["operator_attended_input"] is True
    assert public["offline_test_only"] is False
    assert public["qualifying_live_source"] is False
    assert public["venue_contract"] == "MYMZ6"
    assert "44001" not in json.dumps(public)


@pytest.mark.parametrize("which,field,value", [(0,"body_sha256","wrong"),
    (1,"qty_out",0), (1,"sender_invoked",True), (1,"dry_run",False),
    (2,"transport_state","accepted"), (1,"halt",True)])
def test_invalid_proof_never_creates_acceptance(which, field, value):
    rows, receipt = proof()
    rows[which][field] = value
    with pytest.raises(ValueError):
        control().project_evidence(rows, receipt)


def test_preflight_cli_redacts_equity_errors(inputs, monkeypatch, capsys):
    import c1_rail_http_server
    cp, _ = inputs
    def broken(*args, **kwargs):
        raise c1_rail_http_server.EquityReadError("private amount 123456.789")
    monkeypatch.setattr(c1_rail_http_server, "resolve_current_equity", broken)
    assert control().main(["preflight", "--config", str(cp)]) == 1
    output = capsys.readouterr()
    assert "123456" not in output.err + output.out


@pytest.mark.parametrize("operator", [False, True])
@pytest.mark.parametrize("mutation", ["missing_order", "wrong_ceremony", "wrong_bar", "wrong_signal",
    "wrong_contract", "wrong_close", "enabled", "unclaimed", "no_request"])
def test_proof_cannot_relabel_a_real_listener_event(mutation, operator):
    rows, state = proof(operator=operator)
    cid = state["active"]
    item = state["ceremonies"][cid]
    if mutation == "missing_order":
        for row in rows:
            row.pop("order_id")
    elif mutation == "wrong_ceremony":
        item["manifest"]["ceremony_id"] = str(uuid4())
    elif mutation == "wrong_bar":
        item["bar_sha256"] = "f" * 64
    elif mutation == "wrong_signal":
        item["event_identity"] = "m1-" + "f" * 64
    elif mutation == "wrong_contract":
        rows[1]["test_contract_sha256"] = "f" * 64
    elif mutation == "wrong_close":
        rows[0]["parsed"]["close"] = 44002.
    elif mutation == "enabled":
        state["enabled"] = True
    elif mutation == "unclaimed":
        state["tombstones"] = {}
    else:
        rows.pop(0)
    with pytest.raises(ValueError):
        control().project_evidence(rows, state)


@pytest.mark.parametrize("prior", ["SEND_RESERVED", "TRANSPORT_UNKNOWN", "EMITTED", None])
def test_closed_unresolved_transport_cannot_project_success(prior):
    rows, state = proof()
    state["ceremonies"][state["active"]]["previous_state"] = prior
    with pytest.raises(ValueError):
        control().project_evidence(rows, state)
