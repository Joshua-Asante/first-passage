"""Deterministic joint-ledger and Monday-start weekly-block tests."""

from decimal import Decimal

import pandas as pd
import pytest

from research_utils.joint_trade_blocks import (
    build_joint_events,
    build_weekly_exit_blocks,
)


def _event_frame(
    strategy_id: str,
    instrument: str,
    rows: list[tuple[int, str, int]],
    *,
    utc: bool = False,
) -> pd.DataFrame:
    records = []
    for source_row, timestamp, quantity in rows:
        naive = pd.Timestamp(timestamp)
        records.append(
            {
                "strategy_id": strategy_id,
                "encoded_instrument": instrument,
                "source_row_number": source_row,
                "timestamp_naive": naive,
                "timestamp_utc": naive.tz_localize("UTC") if utc else pd.NaT,
                "quantity": quantity,
            }
        )
    return pd.DataFrame(records)


def _trade_frame(
    strategy_id: str,
    rows: list[tuple[str, str, Decimal]],
) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "strategy_id": strategy_id,
                "exit_timestamp_naive": pd.Timestamp(naive),
                "exit_timestamp_utc": (
                    pd.Timestamp(utc).tz_localize("UTC") if utc else pd.NaT
                ),
                "net_pnl_usd": pnl,
            }
            for naive, utc, pnl in rows
        ]
    )


def test_joint_events_have_stable_cross_strategy_ties_and_micro_equivalents():
    left = _event_frame("zeta", "6J", [(2, "2026-01-05 10:00", 2)])
    right = _event_frame("alpha", "MNQ", [(7, "2026-01-05 10:00", 3)])

    joint = build_joint_events({"zeta": left, "alpha": right})

    assert joint[["strategy_id", "source_row_number"]].values.tolist() == [
        ["alpha", 7],
        ["zeta", 2],
    ]
    assert joint["micro_equivalent_quantity"].tolist() == [3, 20]
    assert joint["concurrent_cross_strategy"].tolist() == [True, True]
    assert joint["timestamp_domain"].tolist() == [
        "SOURCE_NAIVE_AMERICA_NEW_YORK",
        "SOURCE_NAIVE_AMERICA_NEW_YORK",
    ]


def test_joint_events_use_utc_only_when_every_row_has_utc():
    alpha = _event_frame("alpha", "MNQ", [(1, "2026-01-05 10:00", 1)], utc=True)
    zeta = _event_frame("zeta", "MGC", [(2, "2026-01-05 09:00", 1)])

    mixed = build_joint_events({"alpha": alpha, "zeta": zeta})
    all_utc = build_joint_events({"alpha": alpha})

    assert mixed["strategy_id"].tolist() == ["zeta", "alpha"]
    assert set(mixed["timestamp_domain"]) == {"SOURCE_NAIVE_AMERICA_NEW_YORK"}
    assert set(all_utc["timestamp_domain"]) == {"UTC"}


def test_joint_events_reject_mapping_key_mismatch():
    frame = _event_frame("different", "MNQ", [(1, "2026-01-05 10:00", 1)])

    with pytest.raises(ValueError, match="strategy_id mismatch"):
        build_joint_events({"alpha": frame})


def test_weekly_blocks_include_empty_calendar_weeks_and_joint_totals():
    blocks = build_weekly_exit_blocks(
        {
            "alpha": _trade_frame(
                "alpha",
                [
                    ("2026-01-05 10:00", "", Decimal("10.00")),
                    ("2026-01-19 10:00", "", Decimal("-2.00")),
                ],
            ),
            "zeta": _trade_frame(
                "zeta",
                [("2026-01-06 10:00", "", Decimal("3.00"))],
            ),
        }
    )

    assert blocks["week_start"].astype(str).tolist() == [
        "2026-01-05",
        "2026-01-12",
        "2026-01-19",
    ]
    assert blocks["alpha_net_pnl_usd"].tolist() == [
        Decimal("10.00"),
        Decimal("0.00"),
        Decimal("-2.00"),
    ]
    assert blocks["zeta_trade_count"].tolist() == [1, 0, 0]
    assert blocks["joint_net_pnl_usd"].tolist() == [
        Decimal("13.00"),
        Decimal("0.00"),
        Decimal("-2.00"),
    ]
    assert blocks["joint_trade_count"].tolist() == [2, 0, 1]
    assert set(blocks["timestamp_domain"]) == {"SOURCE_NAIVE_AMERICA_NEW_YORK"}


def test_weekly_blocks_use_utc_when_every_exit_has_utc():
    blocks = build_weekly_exit_blocks(
        {
            "alpha": _trade_frame(
                "alpha",
                [("2026-01-04 19:30", "2026-01-05 00:30", Decimal("1.00"))],
            )
        }
    )

    assert blocks["week_start"].astype(str).tolist() == ["2026-01-05"]
    assert blocks["timestamp_domain"].tolist() == ["UTC"]
