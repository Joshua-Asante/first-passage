from pathlib import Path

import pandas as pd
import pytest

from tv_schema import (
    COL_NET_PNL_USD,
    COL_TRADE_NO,
    iter_tv_trade_pairs,
    normalize_tv_columns,
    split_aligned_tv_rows,
)


FIXTURES = Path(__file__).parent / "fixtures"


@pytest.mark.parametrize(
    "fixture_name",
    ["tradingview_legacy.csv", "tradingview_current.csv"],
)
def test_normalizes_legacy_and_current_aliases_to_one_contract(fixture_name):
    raw = pd.read_csv(FIXTURES / fixture_name)

    normalized = normalize_tv_columns(raw)

    assert COL_TRADE_NO in normalized.columns
    assert COL_NET_PNL_USD in normalized.columns
    assert "Net P&L %" in normalized.columns
    assert normalized[COL_TRADE_NO].tolist() == [2, 2, 1, 1]
    assert normalized[COL_NET_PNL_USD].tolist() == [20, 20, 10, 10]


def test_canonical_columns_are_not_clobbered_by_aliases():
    raw = pd.DataFrame(
        {
            "Trade #": [7],
            "Trade number": [99],
            "Net P&L USD": [12.0],
            "Net PnL USD": [34.0],
        }
    )

    normalized = normalize_tv_columns(raw)

    assert normalized["Trade #"].tolist() == [7]
    assert normalized["Net P&L USD"].tolist() == [12.0]


@pytest.mark.parametrize(
    "fixture_name",
    ["tradingview_legacy.csv", "tradingview_current.csv"],
)
def test_strict_pairing_preserves_entry_order_and_alignment(fixture_name):
    raw = pd.read_csv(FIXTURES / fixture_name)

    entries, exits = split_aligned_tv_rows(raw, source_label=fixture_name)

    assert entries.index.tolist() == [2, 1]
    assert exits.index.tolist() == [2, 1]
    assert entries["Signal"].tolist() == ["Long Add", "Long"]
    assert exits["Signal"].tolist() == ["Exit Long", "Exit Long"]


def test_strict_pairing_rejects_misaligned_trade_indexes():
    raw = pd.DataFrame(
        {
            "Trade number": [1, 2],
            "Type": ["Entry long", "Exit long"],
        }
    )

    with pytest.raises(
        AssertionError,
        match="Trade # index mismatch between entry and exit rows",
    ):
        split_aligned_tv_rows(raw, source_label="misaligned.csv")


@pytest.mark.parametrize(
    "fixture_name",
    ["tradingview_legacy.csv", "tradingview_current.csv"],
)
def test_group_pairing_preserves_sorted_trade_group_semantics(fixture_name):
    raw = pd.read_csv(FIXTURES / fixture_name)

    pairs = list(iter_tv_trade_pairs(raw))

    assert [trade_no for trade_no, _, _ in pairs] == [1, 2]
    assert [entry["Signal"] for _, entry, _ in pairs] == ["Long", "Long Add"]
    assert [exit["Net P&L USD"] for _, _, exit in pairs] == [10, 20]
