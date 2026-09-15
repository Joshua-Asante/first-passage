"""Read-only, independently pinned source-admission boundary for new bundles.

The integration owner supplies the reviewed contract's digest from outside the
candidate. A candidate cannot approve itself. Review establishes semantic facts
(source attestation, capture interpretation, reconciliation and coverage); this
module binds those reviewed facts to exact immutable bytes and checks required
fields. It cannot discover missing history or authenticate an operator by itself.
No historical export lookup, quantity scaling, file writing or broker access.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from c1_signal_daemon.book_adapters import ADAPTER_BY_LEG
from c1_rail.book_policy import ACCOUNT_MICRO_CAP

REQUIRED_ARTIFACTS = frozenset({"pine", "port", "csv", "inputs", "properties", "attestation",
                                "normalization", "reconciliation", "coverage", "panel", "margin"})
VERDICTS = frozenset({"source_state", "normalization", "reconciliation", "coverage", "margin"})
FIELDS = frozenset({"schema", "bundle_id", "leg_id", "artifacts", "adapter_overrides",
                   "emulator_overrides", "sizing", "chart_timezone", "normalization_version",
                   "window", "startup", "verdicts", "approved_deviations"})


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def is_digest(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def strict_json(payload):
    def reject(_):
        raise ValueError("invalid_json_number")

    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "duplicate_json_key")
            result[key] = value
        return result

    try:
        return json.loads(payload, parse_constant=reject, object_pairs_hook=unique)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("invalid_json") from exc


def artifact_path(root, artifact):
    require(isinstance(artifact, dict) and set(artifact) == {"path", "sha256"}, "invalid_artifact")
    require(is_digest(artifact["sha256"]), "invalid_artifact_digest")
    name = artifact["path"]
    require(isinstance(name, str) and name and not Path(name).is_absolute(), "invalid_artifact_path")
    target = (root / name).resolve()
    require(target.is_relative_to(root), "artifact_outside_root")
    return target


def instant(value):
    require(isinstance(value, str), "invalid_window")
    try:
        parsed = datetime.fromisoformat(value)
        require(parsed.tzinfo is not None and parsed.utcoffset() is not None, "invalid_window")
        return parsed
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("invalid_window") from exc


def validate(manifest, root):
    require(isinstance(manifest, dict) and set(manifest) == FIELDS, "manifest_fields")
    require(manifest["schema"] == "book-bundle-v1", "manifest_schema")
    require(manifest["leg_id"] in ("dj30_mym_p250", "orb_mnq_v7"), "unsupported_bundle_leg")
    require(isinstance(manifest["bundle_id"], str) and manifest["bundle_id"], "missing_bundle_id")
    require(manifest["chart_timezone"] == "America/New_York", "unsupported_chart_clock")
    require(manifest["normalization_version"] == "tv_trade_ledger-v1", "unsupported_normalization")
    require(isinstance(manifest["verdicts"], dict) and set(manifest["verdicts"]) == VERDICTS
            and all(v == "PASS" for v in manifest["verdicts"].values()), "unresolved_evidence")
    require(isinstance(manifest["approved_deviations"], list) and all(
        isinstance(v, str) and v.strip() for v in manifest["approved_deviations"]), "invalid_deviations")
    window, startup = manifest["window"], manifest["startup"]
    require(isinstance(window, dict) and set(window) == {"start", "end"}, "invalid_window")
    require(isinstance(startup, dict) and set(startup) == {"kind", "first_bar", "coverage_verdict"}
            and startup["kind"] == "cold_at_panel_origin" and startup["coverage_verdict"] == "PASS",
            "missing_startup_evidence")
    require(instant(startup["first_bar"]) == instant(window["start"]) < instant(window["end"]),
            "startup_window_mismatch")
    for field in ("adapter_overrides", "emulator_overrides", "sizing"):
        require(isinstance(manifest[field], dict) and bool(manifest[field]), "missing_execution_inputs")
    emulator = manifest["emulator_overrides"]
    require(set(emulator) == {"initial_capital", "margin_pct", "commission_per_side",
                              "slippage_ticks", "orders_on_close"}, "incomplete_emulator_inputs")
    for field in ("initial_capital", "margin_pct", "commission_per_side", "slippage_ticks"):
        value = emulator[field]
        require(type(value) in (int, float) and math.isfinite(value) and value >= 0,
                "invalid_emulator_number")
    require(emulator["initial_capital"] > 0 and type(emulator["slippage_ticks"]) is int
            and emulator["orders_on_close"] is True, "unsupported_emulator_settings")
    sizing = manifest["sizing"]
    require(set(sizing) == {"mode", "lifecycle_tier", "cap_alloc", "risk_dollars", "pointvalue"},
            "incomplete_sizing_inputs")
    require(sizing["mode"] in ("normal", "protected") and sizing["lifecycle_tier"] in
            ("AUTHORIZED", "WATCH-1", "WATCH-2"), "unsupported_mode_or_lifecycle")
    require(type(sizing["cap_alloc"]) is int and 0 < sizing["cap_alloc"] <= ACCOUNT_MICRO_CAP,
            "invalid_comparison_allocation")
    require(type(sizing["risk_dollars"]) in (int, float) and math.isfinite(sizing["risk_dollars"])
            and sizing["risk_dollars"] >= 0, "invalid_risk_input")
    require(sizing["pointvalue"] == ADAPTER_BY_LEG[manifest["leg_id"]].pointvalue,
            "pointvalue_mismatch")
    artifacts = manifest["artifacts"]
    require(isinstance(artifacts, dict) and set(artifacts) == REQUIRED_ARTIFACTS, "missing_artifacts")
    require(artifacts["pine"]["sha256"] == ADAPTER_BY_LEG[manifest["leg_id"]].pine_sha256,
            "pine_registry_mismatch")
    for artifact in artifacts.values():
        target = artifact_path(root, artifact)
        try:
            content = target.read_bytes()
        except OSError as exc:
            raise ValueError("artifact_unavailable") from exc
        require(bool(content) and sha(content) == artifact["sha256"], "artifact_identity")


@dataclass(frozen=True)
class AdmittedBundle:
    bundle_id: str
    manifest_sha256: str
    trusted_contract_sha256: str
    trusted_contract_bytes: bytes
    manifest_bytes: bytes
    evidence_root: Path

    def revalidate(self):
        """Fresh evidence check before use; returned dict cannot mutate this identity."""
        require(sha(self.manifest_bytes) == self.manifest_sha256, "admission_identity")
        require(sha(self.trusted_contract_bytes) == self.trusted_contract_sha256, "admission_identity")
        contract = strict_json(self.trusted_contract_bytes)
        require(contract["bundles"].get(self.bundle_id) == self.manifest_sha256, "admission_identity")
        manifest = strict_json(self.manifest_bytes)
        require(manifest["bundle_id"] == self.bundle_id, "admission_identity")
        validate(manifest, self.evidence_root)
        return manifest


def admit_bundle(candidate_manifest_path, *, trusted_contract_path,
                 trusted_contract_sha256, evidence_root):
    """Refuse unless the independent reviewed pin and every artifact agree."""
    try:
        contract_bytes = Path(trusted_contract_path).read_bytes()
        require(is_digest(trusted_contract_sha256) and sha(contract_bytes) == trusted_contract_sha256,
                "trusted_contract_identity")
        contract = strict_json(contract_bytes)
        require(isinstance(contract, dict) and set(contract) == {"schema", "reviewed_by", "bundles"}
                and contract["schema"] == "book-bundle-admissions-v1"
                and isinstance(contract["reviewed_by"], str) and contract["reviewed_by"].strip()
                and isinstance(contract["bundles"], dict), "invalid_trusted_contract")
        payload = Path(candidate_manifest_path).read_bytes()
        manifest = strict_json(payload)
        require(isinstance(manifest, dict) and isinstance(manifest.get("bundle_id"), str),
                "missing_bundle_id")
        digest = sha(payload)
        require(contract["bundles"].get(manifest["bundle_id"]) == digest, "manifest_not_admitted")
        root = Path(evidence_root).resolve(strict=True)
        validate(manifest, root)
        return AdmittedBundle(manifest["bundle_id"], digest, trusted_contract_sha256, contract_bytes, payload, root)
    except (OSError, KeyError, TypeError) as exc:
        raise ValueError("invalid_admission_input") from exc


def run_bundle_parity(bundle, *, trusted_contract_sha256):
    """Replay exact reviewed bytes; never search historical exports or panels.

    The caller supplies the independently approved digest again at execution.
    Port code is compiled from its verified snapshot, avoiding stale bytecode or
    a second path read. This offline result does not grant live permission.
    """
    import csv
    import io
    import sys
    import types
    from dataclasses import asdict

    from c1_rail.book_policy import candidate_book_protection_policy
    from c1_signal_daemon.book_adapters import port_path
    from c1_signal_daemon.book_bundle_execution import BundleExecution, SizingInputs, run_sized_adapter
    from c1_signal_daemon.book_parity import ET, compare, load_export_bytes, port_trades
    from c1_signal_daemon.book_protocol import Mode
    from c1_signal_daemon.feed import Bar
    from c1_signal_daemon.tv_broker_emulator import TVBrokerEmulator

    require(isinstance(bundle, AdmittedBundle) and is_digest(trusted_contract_sha256)
            and bundle.trusted_contract_sha256 == trusted_contract_sha256, "execution_trust_mismatch")
    manifest = bundle.revalidate()
    leg_id = manifest["leg_id"]
    artifacts = manifest["artifacts"]
    path = artifact_path(bundle.evidence_root, artifacts["port"])
    require(port_path(leg_id).resolve() == path, "admitted_port_path_mismatch")

    def snapshot(name):
        data = artifact_path(bundle.evidence_root, artifacts[name]).read_bytes()
        require(sha(data) == artifacts[name]["sha256"], "artifact_identity")
        return data

    source, panel, export = (snapshot(name) for name in ("port", "panel", "csv"))
    start, end = (instant(manifest["window"][key]) for key in ("start", "end"))
    bars = []
    for row in csv.DictReader(io.StringIO(panel.decode("utf-8-sig"))):
        ts = instant(row["time"].replace("Z", "+00:00"))
        values = [float(row[key]) for key in ("open", "high", "low", "close", "volume")]
        opening, high, low, close, volume = values
        require(all(math.isfinite(v) for v in values) and volume >= 0
                and 0 < low <= min(opening, close) <= max(opening, close) <= high,
                "invalid_panel_prices")
        require(start <= ts <= end and (not bars or bars[-1].ts < ts), "invalid_panel_window")
        bars.append(Bar(ts, opening, high, low, close, volume))
    require(bool(bars) and bars[0].ts == start, "startup_panel_mismatch")
    require(bars[-1].ts == end, "panel_end_mismatch")

    # The legacy parser intentionally omits open trades. Admission execution
    # rejects incomplete/duplicate pairs and fractional quantities explicitly.
    pairs = {}
    for row in csv.DictReader(io.StringIO(export.decode("utf-8-sig"))):
        kind = row["Type"].split()[0]
        number = int(row["Trade number"])
        require(kind in ("Entry", "Exit") and kind not in pairs.setdefault(number, {}),
                "invalid_export_pair")
        qty = float(row["Size (qty)"])
        require(math.isfinite(qty) and qty > 0 and qty.is_integer(), "invalid_export_quantity")
        pairs[number][kind] = qty
    require(bool(pairs) and all(set(pair) == {"Entry", "Exit"}
                               and pair["Entry"] == pair["Exit"] for pair in pairs.values()),
            "incomplete_export")
    expected = load_export_bytes(export)
    ws, we = (value.astimezone(ET).replace(tzinfo=None) for value in (start, end))
    require(all(ws <= trade.entry_time <= trade.exit_time <= we for trade in expected),
            "excluded_export_trades")

    name = "fp_admitted_" + bundle.manifest_sha256
    module = types.ModuleType(name)
    module.__file__ = str(path)
    previous = sys.modules.get(name)
    sys.modules[name] = module
    try:
        exec(compile(source, str(path), "exec"), module.__dict__)
        spec = ADAPTER_BY_LEG[leg_id]
        require(getattr(module, "LEG_ID", None) == leg_id
                and getattr(module, "PINE_SHA256", None) == spec.pine_sha256, "port_declaration_mismatch")
        sizing = dict(manifest["sizing"])
        sizing["mode"] = Mode(sizing["mode"])
        settings = dict(manifest["adapter_overrides"])
        require("quantity_rule" not in settings and "mode" not in settings, "sizing_override")
        adapter = module.build(**settings, mode=sizing["mode"])
        execution = BundleExecution(adapter, SizingInputs(leg_id=leg_id, **sizing),
                                    policy=candidate_book_protection_policy())
        emulator = TVBrokerEmulator(leg_id=leg_id, mintick=spec.mintick, pointvalue=spec.pointvalue,
                                    **manifest["emulator_overrides"])
        phases = run_sized_adapter(execution, bars, emulator)
        require(execution.open_quantity == 0 and not execution.checkpoint()["pending"]
                and not emulator._pending_market and not emulator._pending_stop, "unresolved_final_state")
        actual = port_trades(emulator)
        require(all(ws <= trade.entry_time <= trade.exit_time <= we for trade in actual),
                "excluded_port_trades")
        report = compare(leg_id, expected, actual, price_tol=spec.mintick / 4,
                         window_start=ws, window_end=we, qty_scale=1, pnl_tol=.011)
        return {"bundle_id": bundle.bundle_id, "manifest_sha256": bundle.manifest_sha256,
                "trusted_contract_sha256": trusted_contract_sha256, "phases": phases,
                "passed": report.passed, "parity": asdict(report)}
    finally:
        if previous is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = previous
