"""Synthetic cost scenarios: distinct toy rates, never private strategy exports."""
import copy
import csv
import hashlib
import json
from datetime import datetime

import pytest

from discovery import remc_series_builder as rsb


def pin(path, value):
    path.write_text(json.dumps(value), encoding="utf-8")
    return path, hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture
def case(tmp_path):
    stamp = datetime(2026, 1, 5, 10, tzinfo=rsb.NY_TZ)
    tables = {key: [rsb.Trade(key[0], 1, stamp, stamp, 1, 100, 2, 5)]
              for key in rsb.FILE_TABLES}
    hashes = {key: hashlib.sha256(str(key).encode()).hexdigest() for key in tables}
    schedule, sha = pin(tmp_path / "schedule.json", {"rows": [
        {"symbol": s, "round_trip_usd": rate * 2}
        for s, rate in (("6J", 2), ("MYM", 3), ("MGC", 5), ("MNQ", 7))]})
    data = {"version": 1, "tier": "Tradeify_Select_100K",
            "commission_schedule": {"path": schedule.name, "sha256": sha},
            "symbols": {s: {"cost_per_side_usd": rate, "tick_value_usd": tick}
                        for s, rate, tick in (("6J", 2, 1), ("MYM", 3, 2),
                                              ("MGC", 5, 3), ("MNQ", 7, 4))},
            "inputs": {":".join(key): {"sha256": digest,
                         "embedded_slippage_ticks_per_side": "unknown"}
                       for key, digest in hashes.items()}, "fills": []}
    types = [("aegis_6j", "normal", "market", "limit"),
             ("dj30_mym_p250", "normal", "stop", "stop"),
             ("vanguard_mgc", "normal", "limit", "limit"),
             ("orb_mnq_v7", "normal", "unknown", None),
             ("dj30_mym_p250", "protected", "limit", "market"),
             ("orb_mnq_v7", "protected", "limit", "limit")]
    data["fills"] = [dict(leg=leg, mode=mode, trade_number=1,
                          entry_order_type=entry, exit_order_type=exit_)
                     for leg, mode, entry, exit_ in types]
    return tables, hashes, data, tmp_path


def build(case, ticks=None, **kwargs):
    tables, hashes, data, root = case
    source = pin(root / "costs.json", data)
    return rsb.build_series(tables, export_tz="America/New_York", input_hashes=hashes,
                            corrected_cost_inputs=source,
                            additional_slippage_ticks_per_side=ticks, **kwargs)


@pytest.mark.parametrize("ticks,pnl,low,protected,protected_low", [
    (0, 1060, -117, 478, -57), (1, 1040, -137, 473, -62),
    (2, 1020, -157, 468, -67)])
def test_per_symbol_costs_and_incremental_fill_scenarios(case, ticks, pnl, low,
                                                      protected, protected_low):
    bundle = build(case, ticks)
    assert tuple(bundle.tiers) == ("Tradeify_Select_100K",)
    channels = bundle.tiers["Tradeify_Select_100K"]
    assert channels["normal_pnl"] == pytest.approx([pnl])
    assert channels["normal_low"] == pytest.approx([low])
    assert channels["protected_pnl"] == pytest.approx([protected])
    assert channels["protected_low"] == pytest.approx([protected_low])
    costs = bundle.manifest["cost_scenario"]
    assert costs["additional_slippage_ticks_per_side"] == ticks
    assert costs["default_classified_fills"] == {"normal": 2, "protected": 0}
    assert costs["interpretation"] == "incremental_scenario_not_bound"
    assert bundle.manifest["cost_basis"] == "per_symbol_tradeify"
    assert costs["inputs"]["aegis_6j:normal"]["embedded_slippage_ticks_per_side"] == "unknown"


def test_absent_fill_metadata_is_charged_and_counted(case):
    case[2]["fills"] = []
    bundle = build(case, 1)
    assert bundle.tiers["Tradeify_Select_100K"]["normal_pnl"] == pytest.approx([1026])
    assert bundle.tiers["Tradeify_Select_100K"]["protected_pnl"] == pytest.approx([460])
    assert bundle.manifest["cost_scenario"]["default_classified_fills"] == {
        "normal": 8, "protected": 6}


def test_legacy_default_is_labeled_and_not_changed(case):
    tables, _, _, _ = case
    bundle = rsb.build_series(tables, export_tz="America/New_York")
    assert tuple(bundle.tiers) == rsb.TIERS
    assert bundle.manifest["cost_basis"] == "legacy_flat_tier"
    assert "cost_scenario" not in bundle.manifest


@pytest.mark.parametrize("bad", ["missing_rate", "foreign_tier", "wrong_rate",
                                 "wrong_export", "missing_basis", "duplicate_fill",
                                 "foreign_trade", "invalid_tick_value"])
def test_bad_cost_evidence_refuses(case, bad):
    data = case[2]
    if bad == "missing_rate":
        del data["symbols"]["6J"]
    elif bad == "foreign_tier":
        data["tier"] = "Bulenox_100K"
    elif bad == "wrong_rate":
        data["symbols"]["6J"]["cost_per_side_usd"] = 99
    elif bad == "wrong_export":
        data["inputs"]["aegis_6j:normal"]["sha256"] = "0" * 64
    elif bad == "missing_basis":
        del data["inputs"]["aegis_6j:normal"]["embedded_slippage_ticks_per_side"]
    elif bad == "duplicate_fill":
        data["fills"].append(copy.deepcopy(data["fills"][0]))
    elif bad == "foreign_trade":
        data["fills"][0]["trade_number"] = 99
    else:
        data["symbols"]["6J"]["tick_value_usd"] = -1
    with pytest.raises(ValueError):
        build(case, 1)


def test_unsupplied_tier_refuses_in_corrected_mode(case):
    with pytest.raises(ValueError):
        build(case, 1, tiers=("Bulenox_100K",))


@pytest.mark.parametrize("ticks", [-1, 3, True, 1.0, "1"])
def test_only_integer_zero_one_two_scenarios(case, ticks):
    with pytest.raises(ValueError):
        build(case, ticks)


def test_raw_hash_tampering_refuses(case):
    tables, hashes, data, root = case
    path, sha = pin(root / "costs.json", data)
    path.write_text(path.read_text() + " ")
    with pytest.raises(rsb.InputIdentityError):
        rsb.build_series(tables, export_tz="America/New_York", input_hashes=hashes,
                         corrected_cost_inputs=(path, sha))


def test_scenario_without_corrected_inputs_refuses(case):
    with pytest.raises(ValueError):
        rsb.build_series(case[0], export_tz="America/New_York",
                         additional_slippage_ticks_per_side=1)


def test_schedule_tampering_refuses(case):
    (case[3] / "schedule.json").write_text("{}")
    with pytest.raises(rsb.InputIdentityError):
        build(case, 1)


def test_duplicate_json_keys_refuse(case):
    tables, hashes, _, root = case
    path = root / "duplicate.json"
    path.write_text('{"version": 1, "version": 1}')
    with pytest.raises(ValueError, match="duplicate"):
        rsb.build_series(tables, export_tz="America/New_York", input_hashes=hashes,
                         corrected_cost_inputs=(path, rsb.sha256_file(path)))


def test_inconsistent_excursion_refuses_in_corrected_mode(case):
    from dataclasses import replace
    key = ("aegis_6j", "normal")
    case[0][key] = [replace(case[0][key][0], net_usd=-100)]
    with pytest.raises(ValueError, match="low exceeds"):
        build(case, 1)


def test_cli_pins_exports_and_emits_only_corrected_tier(case, capsys):
    _, _, data, root = case
    args = ["--export-tz", "America/New_York", "--out", str(root / "output")]
    for leg, mode in rsb.FILE_TABLES:
        path = root / f"{leg}-{mode}.csv"
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=rsb.TRADE_LIST_COLUMNS)
            writer.writeheader()
            for kind in ("Entry long", "Exit long"):
                row = dict.fromkeys(rsb.TRADE_LIST_COLUMNS, "0")
                row.update({"Trade number": "1", "Type": kind,
                            "Date and time": "2026-01-05 10:00", "Size (qty)": "1",
                            "Net PnL USD": "100", "Commission USD": "2",
                            "Adverse excursion USD": "5", "Signal": "limit"})
                writer.writerow(row)
        sha = rsb.sha256_file(path)
        data["inputs"][f"{leg}:{mode}"]["sha256"] = sha
        args.extend(["--input", f"{leg}:{mode}={path}@{sha}"])
    costs, digest = pin(root / "costs.json", data)
    args += ["--corrected-cost-inputs", f"{costs}@{digest}",
             "--additional-slippage-ticks-per-side", "1"]
    assert rsb.main(args) == 0
    manifest = json.loads((root / "output" / "manifest.json").read_text())
    assert set(manifest["outputs"]) == {"Tradeify_Select_100K.csv"}
    with (root / "output" / "Tradeify_Select_100K.csv").open() as handle:
        row = next(csv.DictReader(handle))
    assert float(row["normal_pnl"]) == 1040
    assert float(row["normal_low"]) == -137
    assert manifest["cost_scenario"]["metadata_sha256"] == digest
    assert "tiers=1" in capsys.readouterr().out
