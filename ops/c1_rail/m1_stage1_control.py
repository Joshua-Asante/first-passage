"""Operator-only M1 state tooling. No POST/sender, no arming, no acceptance write.

Migration defaults to a redacted plan. Applying it is a separately attended
operation, after canonical flatness/disarm/recovery checks. Preflight reads
equity only when explicitly invoked; it never ratchets DD or appends events.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from uuid import UUID, uuid4

_ROOT = Path(__file__).resolve().parents[2]
for _path in (_ROOT / "core", Path(__file__).resolve().parent):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from lib.file_lock import exclusive_file_lock
from c1_sizing_host_reference import C1SizingHostReference
from firm_rules import FIRM_RULES
import m1_stage1_contract as contract


def _read(path) -> dict:
    def invalid_constant(value):
        raise ValueError("non-finite JSON")
    value = json.loads(Path(path).read_text(encoding="utf-8"), parse_constant=invalid_constant)
    if not isinstance(value, dict):
        raise ValueError("expected JSON object")
    return value


def _digest(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _disarmed(config):
    if config.get("dry_run") is not True or config.get("armed_until") is not None:
        raise ValueError("explicit disarm with no deadline required")


def atomic_write(path: Path, data: dict) -> None:
    """Same-filesystem durable replacement; a failed write never truncates state."""
    path = Path(path)
    raw = (json.dumps(data, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()
    temp = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
            temp = Path(stream.name)
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
        if os.name != "nt":
            fd = os.open(path.parent, os.O_RDONLY)
            try:
                os.fsync(fd)
            finally:
                os.close(fd)
    finally:
        if temp is not None and temp.exists():
            temp.unlink()


def _sizing_payload() -> dict:
    # Price-independent sizing probe, not a market bar and never a B1 POST.
    return {"leg_id": contract.LEG_ID, "signal_type": "entry",
            "bar_time": "sizing-only-not-evidence", "close": 2.,
            "stop_dist_pts": contract.STOP_DIST_PTS}


def plan_migration(config: dict, *, enabled: bool, release_withdrawn: bool = False) -> dict:
    _disarmed(config)
    if type(enabled) is not bool or type(release_withdrawn) is not bool:
        raise ValueError("Boolean migration flags required")
    paths = {"constants": Path(config["constants_path"]),
             "lifecycle": Path(config["lifecycle_state_path"])}
    if paths["constants"].resolve() == paths["lifecycle"].resolve():
        raise ValueError("state paths must be distinct")
    before = {key: _digest(path) for key, path in paths.items()}
    constants, lifecycle = (_read(paths[key]) for key in ("constants", "lifecycle"))
    rows = constants.get("leg_map")
    if not isinstance(rows, dict):
        raise ValueError("invalid constants leg_map")
    if release_withdrawn:
        # Accepted 2026-08-26 release, explicitly requested, never inferred.
        for leg, old in (("dj30_mym", 69), ("nas100_mnq", 11)):
            if not isinstance(rows.get(leg), dict) or rows[leg].get("cap_alloc") not in (0, old):
                raise ValueError("withdrawn allocation changed; reconcile separately")
            rows[leg]["cap_alloc"] = 0
    rows[contract.LEG_ID] = contract.constants_row(enabled=enabled)
    lifecycle[contract.LEG_KEY] = "AUTHORIZED" if enabled else "RETIRED"
    firm = FIRM_RULES[contract.TIER]
    contract.validate_sizing_inputs(constants, _sizing_payload(), 1.,
        expected_equity=firm["starting_balance"], expected_cap=firm["micro_contract_cap"])
    return {"schema_version": 1, "enabled": enabled, "release_withdrawn": release_withdrawn,
            "before": before, "after": {"constants": constants, "lifecycle": lifecycle},
            "contract_sha256": contract.contract_sha256()}


def apply_migration(config_path: Path, plan: dict, *, flat_verified: bool = False) -> None:
    if flat_verified is not True:
        raise ValueError("operator-verified flatness required")
    config_path = Path(config_path)
    with exclusive_file_lock(config_path.with_name("c1_m1_migration")):
        config = _read(config_path)
        _disarmed(config)
        constants_path = Path(config["constants_path"])
        lifecycle_path = Path(config["lifecycle_state_path"])
        fresh = plan_migration(config, enabled=plan["enabled"],
                               release_withdrawn=plan["release_withdrawn"])
        if fresh != plan:
            raise ValueError("migration inputs changed since reviewed plan")
        # Immutable private backups; no overwrite of prior rollback material.
        suffix = ".m1-backup-" + str(uuid4())
        for path in (constants_path, lifecycle_path):
            with path.with_name(path.name + suffix).open("xb") as stream:
                stream.write(path.read_bytes())
                stream.flush()
                os.fsync(stream.fileno())
        disabled = copy.deepcopy(plan["after"]["constants"])
        disabled["leg_map"][contract.LEG_ID]["cap_alloc"] = 0
        atomic_write(constants_path, disabled)
        atomic_write(lifecycle_path, plan["after"]["lifecycle"])
        if plan["enabled"]:
            atomic_write(constants_path, plan["after"]["constants"])


def preflight(config: dict, current_equity: float) -> dict:
    """Read-only calculation through the SAME host. Returns no private amounts."""
    _disarmed(config)
    fields = ("constants_path", "lifecycle_state_path", "dd_state_path")
    before = {key: _digest(config[key]) for key in fields}
    host = C1SizingHostReference(*(Path(config[k]) for k in
                                 ("lifecycle_state_path", "dd_state_path", "constants_path")))
    decision = host.process_signal(_sizing_payload(), current_equity)
    after = {key: _digest(config[key]) for key in fields}
    if before != after:
        raise ValueError("state changed during preflight")
    if decision.halt or decision.qty_out != 1 or not decision.submit:
        raise ValueError("expected nonzero one-micro sizing not available")
    receipt = {"schema_version": 1, "expected_qty": decision.qty_out,
               "contract_sha256": contract.contract_sha256(), "state_sha256": before,
               "dry_run": True, "armed_until": None, "sizing_only": True}
    receipt["preflight_sha256"] = hashlib.sha256(
        json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return receipt


def _json_digest(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True,
        separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def project_evidence(records: list[dict], state: dict, ceremony_id: str | None = None) -> dict:
    """Join the durable daemon ceremony to the genuine listener event, allowlisted.

    The HTTP response has no event UUID. Select it uniquely from the ledger by
    exact request digest and deterministic order identity, never from user input.
    Raw bar/equity data remains private. This does not assert broker CHAIN_OK.
    """
    try:
        ident = ceremony_id or state["active"]
        if state["schema_version"] != 1 or state["enabled"] is not False:
            raise ValueError("ceremony must be disabled")
        item = state["ceremonies"][ident]
        manifest, bar = item["manifest"], item["bar"]
        if (item["state"] != "CLOSED" or manifest["ceremony_id"] != ident
                or item.get("previous_state") != "RESPONSE_RECORDED"
                or manifest["contract_sha256"] != contract.contract_sha256()
                or type(manifest["expected_qty"]) is not int or manifest["expected_qty"] != 1
                or _json_digest(manifest) != item["manifest_sha256"]):
            raise ValueError("closed ceremony contract mismatch")
        response = item.get("response", {})
        allowed_bodies = {hashlib.sha256(body.encode()).hexdigest() for body in
                         ("dry_run: computed, not sent", "dry_run: computed, not sent\n")}
        if (type(response.get("http_status")) is not int or response["http_status"] != 200
                or response.get("response_kind") != "dry_run_computed"
                or response.get("body_sha256") not in allowed_bodies):
            raise ValueError("recorded dry-run response required")
        event = "m1-" + _json_digest({k: manifest[k] for k in
                                    ("ceremony_id", "target", "contract_sha256", "source")})
        if (item["event_identity"] != event
                or state["tombstones"][ident]["event_identity"] != event
                or _json_digest({"bar": bar, "source": manifest["source"]}) != item["bar_sha256"]):
            raise ValueError("daemon event/bar identity mismatch")
        from datetime import datetime
        if datetime.fromisoformat(bar["timestamp"]) != datetime.fromisoformat(manifest["target"]):
            raise ValueError("bar timestamp mismatch")
        source = manifest["source"]
        if source != contract.OFFLINE_SOURCE:
            raise ValueError("feed binding mismatch")
        for key in ("request_sha256", "bar_sha256"):
            if not re.fullmatch(r"[0-9a-f]{64}", item[key]):
                raise ValueError("invalid proof fingerprint")
        order_id = contract.LEG_ID + "-entry-" + event
        requests = [r for r in records if r.get("kind") == "request_received"
                    and r.get("body_sha256") == item["request_sha256"]]
        if len(requests) != 1 or requests[0].get("order_id") != order_id:
            raise ValueError("missing or ambiguous request")
        eid = str(UUID(requests[0]["event_id"]))
    except (KeyError, TypeError, AttributeError) as exc:
        raise ValueError("incomplete daemon or listener evidence") from exc
    matched = [r for r in records if r.get("event_id") == eid]
    def one(kind):
        found = [r for r in matched if r.get("kind") == kind]
        if len(found) != 1:
            raise ValueError("missing or ambiguous evidence")
        if found[0].get("order_id") != order_id:
            raise ValueError("order identity mismatch")
        return found[0]
    request, decision, transport = (one(k) for k in
                                    ("request_received", "decision", "transport_result"))
    if (request.get("auth_ok") is not True or request.get("body_category") != "b1_json"
            or request.get("body_sha256") != item["request_sha256"]
            or request.get("parsed", {}).get("leg_id") != contract.LEG_ID
            or request["parsed"].get("signal_type") != "entry"
            or request["parsed"].get("bar_time") != event
            or request["parsed"].get("close") != bar["close"]
            or request["parsed"].get("stop_dist_pts") != contract.STOP_DIST_PTS):
        raise ValueError("request evidence mismatch")
    if (decision.get("leg_id") != contract.LEG_ID or decision.get("signal_type") != "entry"
            or type(decision.get("qty_out")) is not int or decision["qty_out"] != 1
            or decision.get("halt") is not False or decision.get("dry_run") is not True
            or decision.get("test_only") is not True or decision.get("sender_invoked") is not False
            or decision.get("test_contract_sha256") != contract.contract_sha256()
            or transport.get("transport_state") != "not_attempted" or transport.get("dry_run") is not True):
        raise ValueError("dry-run decision/transport evidence mismatch")
    return {"schema_version": 1, "listener_event_id": eid,
            "offline_test_only": True, "qualifying_live_source": False,
            "ceremony_sha256": _json_digest(ident), "leg_id": contract.LEG_ID,
            "request_sha256": item["request_sha256"], "signal_id": event,
            "bar_sha256": item["bar_sha256"], "expected_qty": 1, "observed_qty": 1,
            "dry_run": True, "sender_invoked": False, "post_test_emit_enabled": False}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    migrate = sub.add_parser("migrate")
    migrate.add_argument("--config", type=Path, required=True)
    migrate.add_argument("--enable-test", action="store_true")
    migrate.add_argument("--release-withdrawn", action="store_true")
    migrate.add_argument("--apply", action="store_true")
    migrate.add_argument("--flat-verified", action="store_true")
    migrate.add_argument("--expect-constants")
    migrate.add_argument("--expect-lifecycle")
    probe = sub.add_parser("preflight")
    probe.add_argument("--config", type=Path, required=True)
    evidence = sub.add_parser("evidence")
    evidence.add_argument("--events", type=Path, required=True)
    evidence.add_argument("--daemon-state", type=Path, required=True)
    evidence.add_argument("--ceremony-id", required=True)
    args = ap.parse_args(argv)
    try:
        if args.command == "migrate":
            plan = plan_migration(_read(args.config), enabled=args.enable_test,
                                  release_withdrawn=args.release_withdrawn)
            if args.apply:
                if plan["before"] != {"constants": args.expect_constants,
                                      "lifecycle": args.expect_lifecycle}:
                    raise ValueError("reviewed preimage hashes required")
                apply_migration(args.config, plan, flat_verified=args.flat_verified)
            result = {"applied": args.apply, "enabled": plan["enabled"],
                      "before": plan["before"], "contract_sha256": plan["contract_sha256"]}
        elif args.command == "preflight":
            # Explicit operator invocation; only the existing read-only equity GET.
            from c1_rail_http_server import EquityReadError, resolve_current_equity
            cfg = _read(args.config)
            _disarmed(cfg)
            try:
                result = preflight(cfg, resolve_current_equity(cfg))
            except EquityReadError:
                raise ValueError("equity unavailable") from None
        else:
            rows = [json.loads(line) for line in args.events.read_text().splitlines() if line.strip()]
            result = project_evidence(rows, _read(args.daemon_state), args.ceremony_id)
        print(json.dumps(result, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError):
        # Underlying parse/equity exceptions may contain private values or paths.
        print("M1 control refused: invalid, changed, unavailable or unapproved inputs", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
