"""Pytest configuration and shared fixture loaders."""

import os
from pathlib import Path

import pandas as pd
import pytest

# Monorepo layer roots on PYTHONPATH so test-spawned subprocesses (which run repo
# scripts as `python <script>`) resolve the relocated flat modules
# (core/portfolio_mc.py, core/tv_export_loader.py, …). In-process imports use
# [tool.pytest.ini_options].pythonpath; this propagates the same roots to subprocess.run.
_REPO_ROOT = Path(__file__).resolve().parent.parent
_LAYER_ROOTS = [str(_REPO_ROOT / d) for d in ("core", "lab", "ops", "governance")]
os.environ["PYTHONPATH"] = os.pathsep.join(
    _LAYER_ROOTS + ([os.environ["PYTHONPATH"]] if os.environ.get("PYTHONPATH") else [])
)

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def usdjpy_fixtures() -> pd.DataFrame:
    path = FIXTURES_DIR / "usdjpy_pnl_fixtures.csv"
    return pd.read_csv(path)


@pytest.fixture
def valid_tag_record():
    """Factory fixture: call with field overrides to build a valid tag record dict.

    `valid_tag_record()` returns a record that passes validate_tag_record()
    unmodified; `valid_tag_record(mechanism_tier="B")` overrides one field.
    Overriding "provenance" replaces the whole sub-dict (pass a complete one).
    """

    def _make(**overrides):
        record = {
            "mechanism_tier": "A",
            "sourcing_channel_rank": "3",
            "target_instrument_family": "MNQ",
            "outcome": "SURVIVED",
            "provenance": {
                "source_path": "docs/rejected_candidates.md",
                "source_ref": "entry-1",
                "tagged_at": "2026-08-20",
            },
        }
        record.update(overrides)
        return record

    return _make
