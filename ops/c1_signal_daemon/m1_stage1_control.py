"""Private prepare/enable/close/status CLI; this module never sends a signal."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

from c1_rail.m1_stage1_contract import contract_sha256
from c1_signal_daemon.m1_stage1_state import CeremonyError, CeremonyStore, atomic_json, require


def utc(value):
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.utcoffset() is None or parsed.utcoffset().total_seconds() != 0:
            raise ValueError
        return parsed
    except (ValueError, AttributeError, TypeError):
        raise CeremonyError("timestamp must be explicit UTC") from None


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                    allow_nan=False).encode()).hexdigest()


def validate_manifest(value, now=None):
    try:
        require(set(value) == {"ceremony_id", "target", "expires", "contract_sha256",
                              "expected_qty", "preflight_sha256", "source"})
        require(re.fullmatch(r"[A-Za-z0-9_-]{1,80}", value["ceremony_id"]))
        target, expires = utc(value["target"]), utc(value["expires"])
        require(target.second == 0 and target.microsecond == 0)
        require(60 < (expires - target).total_seconds() <= 150)
        if now is not None:
            require(target > now)
        require(value["contract_sha256"] == contract_sha256())
        require(type(value["expected_qty"]) is int and value["expected_qty"] == 1)
        require(re.fullmatch("[0-9a-f]{64}", value["preflight_sha256"]))
        source = value["source"]
        require(set(source) == {"dataset", "schema", "raw_symbol", "instrument_id", "publisher_id"})
        require(source["dataset"] == "GLBX.MDP3" and source["schema"] == "ohlcv-1m")
        require(re.fullmatch(r"MYM[HMUZ][0-9]{1,2}", source["raw_symbol"]))
        require(type(source["instrument_id"]) is int and source["instrument_id"] > 0)
        require(type(source["publisher_id"]) is int and source["publisher_id"] > 0)
    except (TypeError, KeyError):
        raise CeremonyError("ceremony manifest incomplete or invalid") from None
    return value


def _cfg(path):
    from c1_signal_daemon.daemon import load_config
    return load_config(Path(path))


def prepare(store, config_path, manifest, *, boot_id, now):
    manifest = json.loads(json.dumps(validate_manifest(manifest, now)))
    with store.locked():
        obj = store._read()
        if obj["boot_id"] != boot_id:
            raise CeremonyError("current daemon boot required")
        ident = manifest["ceremony_id"]
        if ident in obj["ceremonies"] or ident in obj["tombstones"]:
            raise CeremonyError("ceremony identity already used")
        unresolved = {"EVALUATED", "SEND_RESERVED", "EMITTED", "TRANSPORT_UNKNOWN"}
        for prior in obj["ceremonies"].values():
            checkpoint = (prior.get("previous_state") if prior["state"] == "CLOSED"
                          else prior["state"])
            if checkpoint in unresolved:
                # Neither a fresh ID, close, nor restart reconciles an uncertain send.
                raise CeremonyError("unresolved prior attempt; reconciliation required")
        if obj["active"] and obj["ceremonies"][obj["active"]]["state"] == "READY":
            raise CeremonyError("close current ceremony before preparing another")
        # Disable the durable gate before touching configuration.
        obj["enabled"] = False
        atomic_json(store.path, obj)
        cfg = _cfg(config_path)
        cfg["emit_enabled"] = False
        cfg["strategy"] = "m1_stage1_test"
        cfg["bar_period_s"] = 60
        obj["generation"] += 1
        cfg["m1_test"].update(enabled=False, ceremony_id=ident, boot_id=boot_id,
                              generation=obj["generation"], manifest_sha256=digest(manifest))
        atomic_json(Path(config_path), cfg)
        obj["active"] = ident
        obj["ceremonies"][ident] = dict(state="READY", boot_id=boot_id,
                                         generation=obj["generation"], manifest=manifest,
                                         manifest_sha256=digest(manifest), event_identity=None,
                                         request_sha256=None, response=None, listener_id=None)
        atomic_json(store.path, obj)


def enable(store, config_path, ceremony_id, *, boot_id, reviewed, now):
    validate_manifest(reviewed, now)
    with store.locked():
        obj = store._read()
        item = obj["ceremonies"].get(ceremony_id)
        if (obj["boot_id"] != boot_id or obj["active"] != ceremony_id or not item
                or item["boot_id"] != boot_id or item["state"] != "READY"
                or ceremony_id in obj["tombstones"] or item["manifest"] != reviewed):
            raise CeremonyError("current boot and exact reviewed READY ceremony required")
        obj["enabled"] = False
        atomic_json(store.path, obj)
        cfg = _cfg(config_path)
        gate = cfg["m1_test"]
        if (gate.get("generation") != obj["generation"]
                or gate.get("manifest_sha256") != digest(reviewed)
                or gate.get("boot_id") != boot_id or gate.get("ceremony_id") != ceremony_id
                or cfg["strategy"] != "m1_stage1_test" or cfg["bar_period_s"] != 60):
            raise CeremonyError("configuration/state generation mismatch")
        cfg["emit_enabled"] = True
        gate["enabled"] = True
        atomic_json(Path(config_path), cfg)
        obj["enabled"] = True
        atomic_json(store.path, obj)


def close(store, config_path, ceremony_id):
    with store.locked():
        obj = store._read()
        obj["enabled"] = False
        atomic_json(store.path, obj)
        cfg = _cfg(config_path)
        cfg["emit_enabled"] = False
        cfg["m1_test"]["enabled"] = False
        atomic_json(Path(config_path), cfg)
        item = obj["ceremonies"].get(ceremony_id)
        if item is None:
            raise CeremonyError("ceremony does not exist")
        if item["state"] != "CLOSED":
            item["previous_state"] = item["state"]
            item["state"] = "CLOSED"
        obj["tombstones"].setdefault(ceremony_id, {"reason": "operator_closed"})
        atomic_json(store.path, obj)


def safe_status(store, config_path=None):
    obj = store.read()
    item = obj["ceremonies"].get(obj["active"], {})
    effective = False
    if config_path is not None:
        from c1_signal_daemon.m1_stage1 import M1Coordinator
        coordinator = M1Coordinator(store, config_path, boot_id=obj["boot_id"])
        try:
            effective = coordinator._active(obj, datetime.now(timezone.utc)) is not None
        except (OSError, ValueError, KeyError, TypeError, SystemExit):
            pass
    return dict(boot_id=obj["boot_id"], ceremony_id=obj["active"],
                state=item.get("state", "DISABLED"), effective_emit=effective)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "enable", "close", "status"))
    parser.add_argument("--state", type=Path, default=Path("/data/c1_m1_stage1_state.json"))
    parser.add_argument("--config", type=Path)
    parser.add_argument("--boot-id")
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--ceremony-id")
    args = parser.parse_args(argv)
    store = CeremonyStore(args.state)
    try:
        if args.action == "status":
            print(json.dumps(safe_status(store, args.config)))
            return 0
        if args.config is None:
            raise CeremonyError("config path required")
        if args.action == "close":
            close(store, args.config, args.ceremony_id)
        else:
            if args.manifest is None or not args.boot_id:
                raise CeremonyError("reviewed manifest and current boot required")
            value = json.loads(args.manifest.read_text(encoding="utf-8"))
            if args.action == "prepare":
                prepare(store, args.config, value, boot_id=args.boot_id,
                        now=datetime.now(timezone.utc))
            else:
                enable(store, args.config, args.ceremony_id, boot_id=args.boot_id,
                       reviewed=value, now=datetime.now(timezone.utc))
        print(json.dumps(safe_status(store, args.config)))
        return 0
    except (CeremonyError, OSError, ValueError, SystemExit):
        print("ceremony control failed closed")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
