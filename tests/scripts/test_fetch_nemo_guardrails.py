"""Pin-consistency tests for scripts/fetch_nemo_guardrails.py (no network)."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def _load():
    spec = importlib.util.spec_from_file_location(
        "fetch_nemo_guardrails", REPO / "scripts" / "fetch_nemo_guardrails.py"
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_fetch_reads_live_pin():
    fetch = _load()
    pin = fetch.load_inventory(fetch.DEFAULT_INVENTORY)["nemo_pin"]
    assert pin["commit"] == "dc046e4e1db894893214ffab487c35f451f5baad"
    assert pin["tag"] == "v0.23.0"
    assert pin["runtime"] == "not-adopted"


def test_fetch_refuses_mismatched_existing_dest(tmp_path: Path):
    fetch = _load()
    dest = tmp_path / "clone"
    dest.mkdir()
    (dest / ".git").mkdir()
    # dest exists, is not the pin, and --force is false
    rc = fetch.fetch(dest, fetch.DEFAULT_INVENTORY, force=False)
    assert rc == 1
