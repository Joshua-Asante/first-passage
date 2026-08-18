"""ECON EXPORT v0.1 parser — synthetic List-of-Trades only."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
_SPEC = importlib.util.spec_from_file_location(
    "parse_econ_export", REPO / "scripts" / "parse_econ_export.py"
)
parse = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
sys.modules["parse_econ_export"] = parse
_SPEC.loader.exec_module(parse)

# 2024-01-11 00:00 UTC — RATES CPI pin
CPI_EPOCH = 1704931200000
# 2024-01-10 00:00 UTC — adjacent day
CPI_ADJ_EPOCH = 1704844800000
# 2024-01-05 00:00 UTC — RATES NFP pin
NFP_EPOCH = 1704412800000


def _lot(rows: list[tuple[str, str, str, str]]) -> str:
    lines = ["Trade #,Type,Date and time,Signal,Price USD"]
    for trade, typ, when, signal in rows:
        lines.append(f"{trade},{typ},{when},{signal},100")
    return "\n".join(lines) + "\n"


def test_decode_signal_utc_and_et():
    sig = f"{CPI_EPOCH}|US|CPI|308.5|America/New_York|D"
    d = parse.decode_econ_signal(sig)
    assert d["field"] == "CPI"
    assert d["country"] == "US"
    assert d["utc_date"] == "2024-01-11"
    assert d["et_date"] == "2024-01-10"  # 00:00 UTC is still 19:00 ET prior evening


def test_parse_entry_rows_only(tmp_path: Path):
    csv = tmp_path / "ECON_EXPORT_v0.1_TV_USCPI_2026-08-18_abcde.csv"
    csv.write_text(
        _lot(
            [
                ("1", "Entry long", "2024-01-11 00:00", f"{CPI_EPOCH}|US|CPI|308.5|America/New_York|D"),
                ("1", "Exit long", "2024-01-11 00:00", "ignore"),
                ("2", "Entry long", "2024-01-05 00:00", f"{NFP_EPOCH}|US|NFP|200.0|America/New_York|D"),
            ]
        ),
        encoding="utf-8",
    )
    by = parse.parse_econ_export([csv])
    assert by["CPI"] == {"2024-01-11"}
    assert by["NFP"] == {"2024-01-05"}


def test_rejects_ohlcv_bar_export_signal():
    with pytest.raises(parse.EconExportError):
        parse.decode_econ_signal("1772409600000|156.64|156.806|156.572|156.574|3915")


def test_cli_missing_file_exits_2():
    assert parse.main(["--in", "/no/such/econ.csv"]) == 2
