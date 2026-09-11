"""Private prepare/enable/close/status CLI; this module never sends a signal."""
from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sys

# Standalone-run bootstrap (mirror c1_rail_http_server).
_REPO_ROOT = Path(__file__).resolve().parents[2]
_DAEMON_DIR = Path(__file__).resolve().parent
for _p in (str(_REPO_ROOT / "ops"), str(_DAEMON_DIR), str(_REPO_ROOT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from c1_rail.m1_stage1_contract import contract_sha256, OFFLINE_SOURCE, OPERATOR_INPUT_SOURCE
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


def _third_friday(year, month):
    first = date(year, month, 1)
    first_friday = first + timedelta(days=(4 - first.weekday()) % 7)
    return first_friday + timedelta(days=14)


def _valid_venue_contract(value, target):
    match = re.fullmatch(r"MYM([HMUZ])(\d)", value or "")
    if not match:
        return False
    month = {"H": 3, "M": 6, "U": 9, "Z": 12}[match.group(1)]
    years = [year for year in range(target.year - 1, target.year + 2)
             if year % 10 == int(match.group(2))]
    if len(years) != 1:
        return False
    expiry = _third_friday(years[0], month)
    upcoming = sorted(_third_friday(year, quarter)
                      for year in range(target.year, target.year + 3)
                      for quarter in (3, 6, 9, 12)
                      if _third_friday(year, quarter) >= target.date())
    return expiry >= target.date() and expiry <= upcoming[1]


def validate_manifest(value, now=None):
    try:
        require(set(value) == {"ceremony_id", "target", "expires", "contract_sha256",
                              "expected_qty", "preflight_sha256", "source", "venue_contract"})
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
        require(source in (OPERATOR_INPUT_SOURCE, OFFLINE_SOURCE))
        require(_valid_venue_contract(value["venue_contract"], target))
    except (TypeError, KeyError):
        raise CeremonyError("ceremony manifest incomplete or invalid") from None
    return value


def _cfg(path):
    from c1_signal_daemon.daemon import load_config
    return load_config(Path(path))


def _require_ceremony_interval(cfg):
    interval = cfg.get("poll_interval_s")
    if (type(interval) not in (int, float) or not math.isfinite(interval)
            or not 0 < interval <= 1):
        raise CeremonyError("ceremony poll interval required")


def active_ceremony(obj, cfg, boot_id, now):
    gate = cfg["m1_test"]
    ident = obj.get("active")
    item = obj["ceremonies"].get(ident)
    if (not item or obj["boot_id"] != boot_id or item["boot_id"] != boot_id
            or obj["enabled"] is not True or item["state"] != "READY"
            or ident in obj["tombstones"] or cfg["emit_enabled"] is not True
            or gate["enabled"] is not True or cfg["strategy"] != "m1_stage1_test"
            or cfg["bar_period_s"] != 60 or gate.get("boot_id") != boot_id
            or gate.get("ceremony_id") != ident
            or gate.get("generation") != obj["generation"]
            or item["generation"] != obj["generation"]
            or gate.get("manifest_sha256") != item["manifest_sha256"]
            or digest(item["manifest"]) != item["manifest_sha256"]):
        return None
    validate_manifest(item["manifest"])
    if now >= utc(item["manifest"]["expires"]):
        return None
    return item


def prepare(store, config_path, manifest, *, boot_id, now):
    manifest = json.loads(json.dumps(validate_manifest(manifest, now)))
    cfg = _cfg(config_path)
    _require_ceremony_interval(cfg)
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
    cfg = _cfg(config_path)
    _require_ceremony_interval(cfg)
    with store.locked():
        obj = store._read()
        item = obj["ceremonies"].get(ceremony_id)
        if (obj["boot_id"] != boot_id or obj["active"] != ceremony_id or not item
                or item["boot_id"] != boot_id or item["state"] != "READY"
                or ceremony_id in obj["tombstones"] or item["manifest"] != reviewed):
            raise CeremonyError("current boot and exact reviewed READY ceremony required")
        obj["enabled"] = False
        atomic_json(store.path, obj)
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
        for name in (f"m1_upload_{ceremony_id}.json", f"m1_bar_{ceremony_id}.json",
                     f"m1_claim_{ceremony_id}"):
            (store.path.parent / name).unlink(missing_ok=True)


def inject(store, config_path, *, ceremony_id, boot_id, contract, time, bar_file, now):
    expected_upload = store.path.parent / f"m1_upload_{ceremony_id}.json"
    try:
        candidate = Path(bar_file)
        bad_path = candidate.is_symlink() or candidate.resolve() != expected_upload.resolve()
    except (OSError, TypeError, ValueError):
        bad_path = True
    if bad_path:
        raise CeremonyError("bad upload path")
    upload = candidate.resolve()
    try:
        with store.locked():
            obj = store._read()
            cfg = _cfg(config_path)
            current = obj["ceremonies"].get(obj.get("active"))
            if (obj.get("active") != ceremony_id or not current
                    or current.get("boot_id") != boot_id or obj.get("boot_id") != boot_id
                    or current.get("state") != "READY" or ceremony_id in obj["tombstones"]):
                raise CeremonyError("not active")
            if current.get("manifest", {}).get("source") != OPERATOR_INPUT_SOURCE:
                raise CeremonyError("not active")
            gate = cfg.get("m1_test", {})
            if (obj.get("enabled") is not True or cfg.get("emit_enabled") is not True
                    or gate.get("enabled") is not True):
                raise CeremonyError("not enabled")
            try:
                item = active_ceremony(obj, cfg, boot_id, now)
            except (CeremonyError, KeyError, TypeError, ValueError):
                item = None
            if item is None:
                raise CeremonyError("not active")
            manifest = item["manifest"]
            if contract != manifest["venue_contract"]:
                raise CeremonyError("contract mismatch")
            if utc(time) != utc(manifest["target"]):
                raise CeremonyError("time mismatch")
            elapsed = (now - utc(manifest["target"])).total_seconds()
            if elapsed < 60:
                raise CeremonyError("before window")
            if elapsed > 120:
                raise CeremonyError("after window")
            try:
                bar = json.loads(upload.read_text(encoding="utf-8"))
                keys = {"open", "high", "low", "close", "volume"}
                if not isinstance(bar, dict) or set(bar) != keys:
                    raise ValueError
                numbers = [bar[key] for key in ("open", "high", "low", "close", "volume")]
                if not all(type(number) in (int, float) and math.isfinite(number) and number > 0
                           for number in numbers):
                    raise ValueError
                open_, high, low, close_, volume = numbers
                if not low <= min(open_, close_) <= max(open_, close_) <= high:
                    raise ValueError
            except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
                raise CeremonyError("bad bar file") from None
            claim = store.path.parent / f"m1_claim_{ceremony_id}"
            try:
                fd = os.open(claim, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            except FileExistsError:
                raise CeremonyError("already injected") from None
            try:
                os.close(fd)
                timestamp = utc(manifest["target"]).isoformat()
                canonical_bar = {"timestamp": timestamp, "open": float(open_),
                                 "high": float(high), "low": float(low),
                                 "close": float(close_), "volume": float(volume),
                                 "venue_contract": manifest["venue_contract"]}
                bar_sha256 = digest({"bar": canonical_bar, "source": manifest["source"]})
                record = {"schema_version": 1, "ceremony_id": ceremony_id,
                          "boot_id": boot_id, **canonical_bar, "bar_sha256": bar_sha256}
                atomic_json(store.path.parent / f"m1_bar_{ceremony_id}.json", record)
            except Exception:
                raise CeremonyError("publication uncertain") from None
        return {"action": "inject", "ceremony_id": ceremony_id,
                "venue_contract": contract, "target": utc(manifest["target"]).isoformat(),
                "bar_sha256": bar_sha256, "published_at": now.astimezone(timezone.utc).isoformat()}
    finally:
        upload.unlink(missing_ok=True)


def safe_status(store, config_path=None):
    obj = store.read()
    item = obj["ceremonies"].get(obj["active"], {})
    effective = False
    published = bool(obj["active"] and
                     (store.path.parent / f"m1_bar_{obj['active']}.json").is_file())
    return dict(boot_id=obj["boot_id"], ceremony_id=obj["active"],
                state=item.get("state", "DISABLED"), effective_emit=effective,
                source_status="bar_published" if published else "disconnected")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "enable", "inject", "close", "status"))
    parser.add_argument("--state", type=Path, default=Path("/data/c1_m1_stage1_state.json"))
    parser.add_argument("--config", type=Path)
    parser.add_argument("--boot-id")
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--ceremony-id")
    parser.add_argument("--contract")
    parser.add_argument("--time")
    parser.add_argument("--bar-file", type=Path)
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
        elif args.action == "inject":
            result = inject(store, args.config, ceremony_id=args.ceremony_id,
                            boot_id=args.boot_id, contract=args.contract, time=args.time,
                            bar_file=args.bar_file, now=datetime.now(timezone.utc))
            print(json.dumps(result, sort_keys=True))
            return 0
        else:
            if args.manifest is None or not args.boot_id:
                raise CeremonyError("reviewed manifest and current boot required")
            value = json.loads(args.manifest.read_text(encoding="utf-8"))
            if value.get("source") != OPERATOR_INPUT_SOURCE:
                raise CeremonyError("operator input source required")
            if args.action == "prepare":
                prepare(store, args.config, value, boot_id=args.boot_id,
                        now=datetime.now(timezone.utc))
            else:
                enable(store, args.config, args.ceremony_id, boot_id=args.boot_id,
                       reviewed=value, now=datetime.now(timezone.utc))
        print(json.dumps(safe_status(store, args.config)))
        return 0
    except (CeremonyError, OSError, ValueError, SystemExit) as exc:
        if args.action == "inject" and str(exc) in {
                "bad upload path", "not active", "not enabled", "contract mismatch",
                "time mismatch", "before window", "after window", "bad bar file",
                "already injected", "publication uncertain"}:
            print(f"inject refused: {exc}")
            return 2
        print("ceremony control failed closed")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
