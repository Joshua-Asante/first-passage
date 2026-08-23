"""Adversarial tests for scripts/check_agent_rails.py."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parents[2]
_SPEC = importlib.util.spec_from_file_location(
    "check_agent_rails", REPO / "scripts" / "check_agent_rails.py"
)
car = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
sys.modules[_SPEC.name] = car
_SPEC.loader.exec_module(car)


PINNED_COMMIT = "dc046e4e1db894893214ffab487c35f451f5baad"


def _minimal_inventory(**overrides):
    data = {
        "schema_version": 1,
        "nemo_pin": {
            "repo": "https://github.com/NVIDIA-NeMo/Guardrails",
            "tag": "v0.23.0",
            "commit": PINNED_COMMIT,
            "license": "Apache-2.0",
            "runtime": "not-adopted",
        },
        "stages": {
            "input": [{
                "id": "in",
                "hardness": "soft",
                "owner": "owner.md",
                "anchors": [{"path": "owner.md", "must_contain": "INPUT"}],
            }],
            "dialog": [{
                "id": "di",
                "hardness": "soft",
                "owner": "owner.md",
                "anchors": [{"path": "owner.md", "must_contain": "DIALOG"}],
            }],
            "retrieval": [{
                "id": "re",
                "hardness": "soft",
                "owner": "owner.md",
                "anchors": [{"path": "owner.md", "must_contain": "RETRIEVAL"}],
            }],
            "execution": [{
                "id": "ex",
                "hardness": "hard",
                "owner": "owner.md",
                "anchors": [{"path": "owner.md", "must_contain": "EXEC"}],
            }],
            "output": [{
                "id": "ou",
                "hardness": "soft",
                "owner": "owner.md",
                "anchors": [{"path": "owner.md", "must_contain": "OUTPUT"}],
            }],
        },
    }
    data.update(overrides)
    return data


def _write_fixture(tmp_path: Path, inventory: dict, body: str = "") -> Path:
    (tmp_path / "owner.md").write_text(
        body or "INPUT DIALOG RETRIEVAL EXEC OUTPUT\n", encoding="utf-8",
    )
    inv = tmp_path / "rails.yml"
    inv.write_text(yaml.safe_dump(inventory), encoding="utf-8")
    return inv


def test_live_inventory_is_clean():
    inventory = car.load_inventory(car.DEFAULT_INVENTORY)
    errors = car.check_inventory(REPO, inventory)
    assert errors == []


def test_live_pin_is_v0230_not_adopted():
    inventory = car.load_inventory(car.DEFAULT_INVENTORY)
    pin = inventory["nemo_pin"]
    assert pin["tag"] == "v0.23.0"
    assert pin["commit"] == PINNED_COMMIT
    assert pin["runtime"] == "not-adopted"


def test_main_live_exits_zero():
    assert car.main(["--inventory", str(car.DEFAULT_INVENTORY)]) == 0


def test_compliant_fixture_passes(tmp_path: Path):
    inv = _write_fixture(tmp_path, _minimal_inventory())
    errors = car.check_inventory(tmp_path, car.load_inventory(inv))
    assert errors == []


def test_missing_path_fails(tmp_path: Path):
    inventory = _minimal_inventory()
    inventory["stages"]["input"][0]["anchors"][0]["path"] = "gone.md"
    inv = _write_fixture(tmp_path, inventory)
    errors = car.check_inventory(tmp_path, car.load_inventory(inv))
    assert any("missing path gone.md" in e for e in errors)


def test_missing_needle_fails(tmp_path: Path):
    inv = _write_fixture(tmp_path, _minimal_inventory(), body="nope\n")
    errors = car.check_inventory(tmp_path, car.load_inventory(inv))
    assert any("missing 'INPUT'" in e or 'missing "INPUT"' in e or
               "missing 'INPUT'" in e.replace('"', "'") for e in errors)
    assert any("INPUT" in e for e in errors)


def test_empty_stages_fail(tmp_path: Path):
    inventory = _minimal_inventory(stages={})
    inv = _write_fixture(tmp_path, inventory)
    errors = car.check_inventory(tmp_path, car.load_inventory(inv))
    assert any("stages" in e for e in errors)


def test_missing_stage_fails(tmp_path: Path):
    inventory = _minimal_inventory()
    del inventory["stages"]["output"]
    inv = _write_fixture(tmp_path, inventory)
    errors = car.check_inventory(tmp_path, car.load_inventory(inv))
    assert any("missing output" in e for e in errors)


def test_no_hard_execution_rail_fails(tmp_path: Path):
    inventory = _minimal_inventory()
    inventory["stages"]["execution"][0]["hardness"] = "soft"
    inv = _write_fixture(tmp_path, inventory)
    errors = car.check_inventory(tmp_path, car.load_inventory(inv))
    assert any("hardness=hard" in e for e in errors)


def test_runtime_adoption_fails(tmp_path: Path):
    inventory = _minimal_inventory()
    inventory["nemo_pin"]["runtime"] = "adopted"
    inv = _write_fixture(tmp_path, inventory)
    errors = car.check_inventory(tmp_path, car.load_inventory(inv))
    assert any("not-adopted" in e for e in errors)


def test_bad_commit_fails(tmp_path: Path):
    inventory = _minimal_inventory()
    inventory["nemo_pin"]["commit"] = "not-a-sha"
    inv = _write_fixture(tmp_path, inventory)
    errors = car.check_inventory(tmp_path, car.load_inventory(inv))
    assert any("commit" in e for e in errors)


def test_unreadable_inventory_exits_one(tmp_path: Path):
    missing = tmp_path / "absent.yml"
    assert car.main(["--inventory", str(missing), "--repo", str(tmp_path)]) == 1
