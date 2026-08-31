from __future__ import annotations

import importlib.util
import re
from pathlib import Path
from types import SimpleNamespace

import pandas as pd
import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPT = (
    REPO
    / "lab"
    / "analysis"
    / "_inbox"
    / "volregime_l3_2026-08-31"
    / "l3_halves.py"
)
SPEC = importlib.util.spec_from_file_location("volregime_l3", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def frame(*, second_half_negative: bool = False) -> pd.DataFrame:
    rows = []
    timestamp = pd.Timestamp("2026-01-01", tz="UTC")
    # Deliberately append reverse-chronologically: score_l3 must sort first.
    for half in (0, 1):
        for stratum in (0, 1):
            for volume, outcome in ((0, 0), (0, 0), (1, 1), (1, 1)):
                if second_half_negative and half == 1 and stratum == 1:
                    outcome = 1 - outcome
                rows.append(
                    {
                        "time_utc": timestamp,
                        "bias_volume": volume,
                        "bias_range": stratum,
                        "outcome": outcome,
                    }
                )
                timestamp += pd.Timedelta(minutes=15)
    return pd.DataFrame(rows).sort_values("time_utc", ascending=False).reset_index(drop=True)


def test_midpoint_boundary_and_positive_halves_pass() -> None:
    result = MODULE.score_l3(frame())

    assert result["split_index_zero_based_second_half_start"] == 8
    assert result["split_boundary_utc"] == "2026-01-01T02:00:00+00:00"
    assert result["halves"]["first"]["n_scored"] == 8
    assert result["halves"]["second"]["n_scored"] == 8
    assert result["l3"]["verdict"] == "PASS"


def test_one_negative_stratum_fails_the_half_and_l3() -> None:
    result = MODULE.score_l3(frame(second_half_negative=True))

    assert result["halves"]["first"]["passes"] is True
    assert result["halves"]["second"]["minimum_stratum_lift"] == -1.0
    assert result["halves"]["second"]["passes"] is False
    assert result["l3"]["verdict"] == "FAIL"


def test_missing_required_column_is_rejected() -> None:
    with pytest.raises(ValueError, match="missing required columns: outcome"):
        MODULE.score_l3(frame().drop(columns="outcome"))


def test_invalid_rows_are_excluded_before_midpoint() -> None:
    invalid = pd.DataFrame(
        [
            {
                "time_utc": pd.Timestamp("2025-12-31T23:45:00Z"),
                "bias_volume": 1,
                "bias_range": 0,
                "outcome": float("nan"),
            },
            {
                "time_utc": pd.Timestamp("2026-01-02T00:00:00Z"),
                "bias_volume": 2,
                "bias_range": 1,
                "outcome": 1,
            },
        ]
    )

    result = MODULE.score_l3(pd.concat([invalid, frame()], ignore_index=True))

    assert result["split_index_zero_based_second_half_start"] == 8
    assert result["halves"]["first"]["n_scored"] == 8
    assert result["halves"]["second"]["n_scored"] == 8
    assert result["l3"]["verdict"] == "PASS"


def test_empty_stratum_lift_formats_without_crashing() -> None:
    assert MODULE.format_lift(None) == "None"
    assert MODULE.format_lift(0.125) == "+0.125000"


def test_collect_results_preflights_all_panels_before_scoring(tmp_path: Path) -> None:
    (tmp_path / "MNQ_M15.csv").write_bytes(b"mnq")
    (tmp_path / "MYM_M15.csv").write_bytes(b"wrong-mym")
    prepare_calls: list[str] = []

    def prepare(symbol: str):
        prepare_calls.append(symbol)
        return frame(), {"csv": f"{symbol}_M15.csv"}

    fake_l4 = SimpleNamespace(
        DATA=tmp_path,
        EXPECTED={
            "MNQ": MODULE.file_sha256(tmp_path / "MNQ_M15.csv"),
            "MYM": "0" * 64,
        },
        sha256=MODULE.file_sha256,
        prepare=prepare,
    )

    with pytest.raises(RuntimeError, match="MYM hash mismatch"):
        MODULE.collect_results(fake_l4, ("MNQ", "MYM"))

    assert prepare_calls == []


def test_load_l4_module_reports_missing_builder(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    missing = tmp_path / "missing_builder.py"
    monkeypatch.setattr(MODULE, "L4_SCRIPT", missing)

    message = re.escape(f"cannot load scored-frame builder: {missing}")
    with pytest.raises(RuntimeError, match=message):
        MODULE._load_l4_module()
