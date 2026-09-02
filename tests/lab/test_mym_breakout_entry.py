from __future__ import annotations

import json
import unittest
from pathlib import Path

import pandas as pd

from lab.analysis.mym_breakout_entry_2026_09.run_research import (
    assign_period,
    bootstrap_expectancy_ci,
    build_sessions,
    evaluate_position,
    simulate_session,
    summarize_trades,
    validate_config,
    validate_inputs,
)


class ExecutionAccountingTests(unittest.TestCase):
    def test_stop_wins_when_stop_and_target_touch_same_bar(self) -> None:
        bars = pd.DataFrame(
            [{"time": "2025-01-02T15:00:00Z", "open": 1000, "high": 1310, "low": 690, "close": 1000}]
        )

        trade = evaluate_position(
            side="long",
            entry_price=1000,
            bars=bars,
            stop_points=300,
            target_points=300,
            tick_size=1,
            point_value=0.5,
            commission_per_side=0.91,
            slippage_ticks_per_side=1,
        )

        self.assertEqual(trade["exit_reason"], "stop")
        self.assertEqual(trade["exit_price_raw"], 700)
        self.assertAlmostEqual(trade["net_pnl_usd"], -152.82)
        self.assertAlmostEqual(trade["net_r"], -152.82 / 150.0)

    def test_gap_through_stop_uses_worse_open_for_short(self) -> None:
        bars = pd.DataFrame(
            [{"time": "2025-01-02T15:00:00Z", "open": 1350, "high": 1360, "low": 1340, "close": 1350}]
        )

        trade = evaluate_position(
            side="short",
            entry_price=1000,
            bars=bars,
            stop_points=300,
            target_points=300,
            tick_size=1,
            point_value=0.5,
            commission_per_side=0.91,
            slippage_ticks_per_side=0,
        )

        self.assertEqual(trade["exit_price_raw"], 1350)
        self.assertAlmostEqual(trade["gross_pnl_usd"], -175.0)
        self.assertAlmostEqual(trade["net_pnl_usd"], -176.82)

    def test_time_exit_charges_commission_and_adverse_slippage_both_sides(self) -> None:
        bars = pd.DataFrame(
            [{"time": "2025-01-02T15:00:00Z", "open": 1000, "high": 1010, "low": 990, "close": 1020}]
        )

        trade = evaluate_position(
            side="long",
            entry_price=1000,
            bars=bars,
            stop_points=300,
            target_points=300,
            tick_size=1,
            point_value=0.5,
            commission_per_side=0.91,
            slippage_ticks_per_side=1,
        )

        self.assertEqual(trade["exit_reason"], "time")
        self.assertAlmostEqual(trade["gross_pnl_usd"], 10.0)
        self.assertAlmostEqual(trade["net_pnl_usd"], 7.18)


class MetricsAndValidationTests(unittest.TestCase):
    def test_metrics_use_net_r_and_report_drawdown_profit_factor(self) -> None:
        trades = pd.DataFrame(
            {
                "side": ["long", "short", "long"],
                "gross_r": [1.0, -1.0, 0.5],
                "net_r": [0.9, -1.1, 0.4],
                "net_pnl_usd": [135.0, -165.0, 60.0],
            }
        )

        got = summarize_trades(trades)

        self.assertEqual(got["trade_count"], 3)
        self.assertAlmostEqual(got["win_rate"], 2 / 3)
        self.assertAlmostEqual(got["gross_expectancy_r"], 1 / 6)
        self.assertAlmostEqual(got["net_expectancy_r"], 1 / 15)
        self.assertAlmostEqual(got["profit_factor"], 195 / 165)
        self.assertAlmostEqual(got["max_drawdown_r"], 1.1)
        self.assertEqual(got["long"]["trade_count"], 2)
        self.assertEqual(got["short"]["trade_count"], 1)

    def test_period_assignment_is_chronological_at_boundaries(self) -> None:
        self.assertEqual(assign_period(pd.Timestamp("2022-12-31T23:59:59Z")), "development")
        self.assertEqual(assign_period(pd.Timestamp("2023-01-01T00:00:00Z")), "validation")
        self.assertEqual(assign_period(pd.Timestamp("2025-01-01T00:00:00Z")), "holdout")

    def test_input_validation_rejects_duplicate_time_and_wrong_metadata(self) -> None:
        bars = pd.DataFrame(
            {
                "time": pd.to_datetime(["2025-01-02T15:00:00Z", "2025-01-02T15:00:00Z"]),
                "open": [1000, 1000],
                "high": [1010, 1010],
                "low": [990, 990],
                "close": [1000, 1000],
                "volume": [1, 1],
            }
        )
        metadata = {"symbol": "MNQ", "ticker": "MNQ1!", "mintick": 0.25, "pointvalue": 2.0, "timeframe": "15"}

        with self.assertRaisesRegex(ValueError, "metadata"):
            validate_inputs(bars, metadata)

        metadata = {"symbol": "MYM", "ticker": "MYM1!", "mintick": 1.0, "pointvalue": 0.5, "timeframe": "15"}
        with self.assertRaisesRegex(ValueError, "duplicate"):
            validate_inputs(bars, metadata)

    def test_input_validation_rejects_unsorted_time_and_invalid_ohlc(self) -> None:
        metadata = {"symbol": "MYM", "ticker": "MYM1!", "mintick": 1.0, "pointvalue": 0.5, "timeframe": "15"}
        bars = pd.DataFrame(
            {
                "time": pd.to_datetime(["2025-01-02T15:15:00Z", "2025-01-02T15:00:00Z"]),
                "open": [1000, 1000], "high": [1010, 1010], "low": [990, 990],
                "close": [1000, 1000], "volume": [1, 1],
            }
        )
        with self.assertRaisesRegex(ValueError, "chronological"):
            validate_inputs(bars, metadata)
        bars = bars.sort_values("time").reset_index(drop=True)
        bars.loc[0, "low"] = 1005
        with self.assertRaisesRegex(ValueError, "OHLC"):
            validate_inputs(bars, metadata)

    def test_bootstrap_confidence_interval_is_deterministic(self) -> None:
        values = pd.Series([1.0, -1.0, 0.5, -0.5, 1.0, -1.0])

        first = bootstrap_expectancy_ci(values, samples=500, seed=20260902)
        second = bootstrap_expectancy_ci(values, samples=500, seed=20260902)

        self.assertEqual(first, second)
        self.assertLessEqual(first[0], 0.0)
        self.assertGreaterEqual(first[1], 0.0)


class EntryTimingTests(unittest.TestCase):
    @staticmethod
    def session_bars(rows: list[tuple[str, float, float, float, float]]) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {"time": pd.Timestamp(time), "open": open_, "high": high, "low": low, "close": close, "volume": 1}
                for time, open_, high, low, close in rows
            ]
        )

    def test_close_confirmation_enters_next_bar_open(self) -> None:
        bars = self.session_bars(
            [
                ("2025-01-02T14:30:00Z", 1000, 1010, 990, 1000),
                ("2025-01-02T14:45:00Z", 1000, 1020, 995, 1010),
                ("2025-01-02T15:00:00Z", 1010, 1030, 1000, 1025),
                ("2025-01-02T15:15:00Z", 1040, 1050, 1035, 1045),
                ("2025-01-02T15:30:00Z", 1045, 1050, 1040, 1048),
            ]
        )

        trade = simulate_session(bars, family="close_confirmed", stop_points=300, slippage_ticks_per_side=1)

        self.assertIsNotNone(trade)
        self.assertEqual(trade["signal_time"], pd.Timestamp("2025-01-02T15:00:00Z"))
        self.assertEqual(trade["entry_time"], pd.Timestamp("2025-01-02T15:15:00Z"))
        self.assertEqual(trade["entry_price_raw"], 1040)

    def test_immediate_two_sided_break_on_same_bar_is_skipped(self) -> None:
        bars = self.session_bars(
            [
                ("2025-01-02T14:30:00Z", 1000, 1010, 990, 1000),
                ("2025-01-02T14:45:00Z", 1000, 1020, 995, 1010),
                ("2025-01-02T15:00:00Z", 1010, 1030, 980, 1010),
                ("2025-01-02T15:15:00Z", 1010, 1015, 1000, 1005),
            ]
        )

        trade = simulate_session(bars, family="immediate", stop_points=300, slippage_ticks_per_side=1)

        self.assertIsNone(trade)

    def test_unknown_family_is_rejected(self) -> None:
        bars = self.session_bars(
            [
                ("2025-01-02T14:30:00Z", 1000, 1010, 990, 1000),
                ("2025-01-02T14:45:00Z", 1000, 1020, 995, 1010),
            ]
        )

        with self.assertRaisesRegex(ValueError, "family"):
            simulate_session(bars, family="searched_best", stop_points=300, slippage_ticks_per_side=1)

    def test_long_stop_entry_gap_fills_at_worse_open(self) -> None:
        bars = self.session_bars(
            [
                ("2025-01-02T14:30:00Z", 1000, 1010, 990, 1000),
                ("2025-01-02T14:45:00Z", 1000, 1020, 995, 1010),
                ("2025-01-02T15:00:00Z", 1050, 1060, 1040, 1050),
                ("2025-01-02T15:15:00Z", 1050, 1055, 1045, 1050),
            ]
        )

        trade = simulate_session(bars, family="immediate", stop_points=300, slippage_ticks_per_side=1)

        self.assertEqual(trade["entry_price_raw"], 1050)

    def test_short_stop_entry_gap_fills_at_worse_open(self) -> None:
        bars = self.session_bars(
            [
                ("2025-01-02T14:30:00Z", 1000, 1010, 990, 1000),
                ("2025-01-02T14:45:00Z", 1000, 1005, 980, 990),
                ("2025-01-02T15:00:00Z", 950, 960, 940, 950),
                ("2025-01-02T15:15:00Z", 950, 955, 945, 950),
            ]
        )

        trade = simulate_session(bars, family="immediate", stop_points=300, slippage_ticks_per_side=1)

        self.assertEqual(trade["entry_price_raw"], 950)

    def test_long_gap_resolves_later_two_sided_bar_to_known_long_fill(self) -> None:
        bars = self.session_bars(
            [
                ("2025-01-02T14:30:00Z", 1000, 1010, 990, 1000),
                ("2025-01-02T14:45:00Z", 1000, 1020, 980, 1000),
                ("2025-01-02T15:00:00Z", 1050, 1060, 970, 990),
                ("2025-01-02T15:15:00Z", 990, 1000, 980, 995),
            ]
        )

        trade = simulate_session(bars, family="immediate", stop_points=300, slippage_ticks_per_side=1)

        self.assertEqual(trade["side"], "long")
        self.assertEqual(trade["entry_price_raw"], 1050)

    def test_short_gap_resolves_later_two_sided_bar_to_known_short_fill(self) -> None:
        bars = self.session_bars(
            [
                ("2025-01-02T14:30:00Z", 1000, 1010, 990, 1000),
                ("2025-01-02T14:45:00Z", 1000, 1020, 980, 1000),
                ("2025-01-02T15:00:00Z", 950, 1030, 940, 1010),
                ("2025-01-02T15:15:00Z", 1010, 1020, 1000, 1005),
            ]
        )

        trade = simulate_session(bars, family="immediate", stop_points=300, slippage_ticks_per_side=1)

        self.assertEqual(trade["side"], "short")
        self.assertEqual(trade["entry_price_raw"], 950)


class SessionAndConfigurationTests(unittest.TestCase):
    @staticmethod
    def full_session() -> pd.DataFrame:
        times = pd.date_range("2025-01-02T14:30:00Z", "2025-01-02T21:00:00Z", freq="15min")
        return pd.DataFrame(
            {"time": times, "open": 1000, "high": 1010, "low": 990, "close": 1000, "volume": 1}
        )

    def test_complete_sessions_require_every_rth_timestamp(self) -> None:
        full = self.full_session()
        missing_interior = full.drop(index=10).reset_index(drop=True)

        sessions, excluded = build_sessions(
            pd.concat([full, missing_interior.assign(time=lambda d: d.time + pd.Timedelta(days=1))]),
            minimum_bars=20,
        )

        self.assertEqual(len(sessions), 1)
        self.assertEqual(excluded["incomplete_grid"], 1)

    def test_config_validation_rejects_missing_catalogue_family(self) -> None:
        config = json.loads(
            Path("lab/analysis/mym_breakout_entry_2026_09/config.json").read_text(encoding="utf-8")
        )
        config["catalogue"] = [{"family": "immediate"}]

        with self.assertRaisesRegex(ValueError, "catalogue"):
            validate_config(config)

    def test_config_validation_rejects_missing_decision_thresholds(self) -> None:
        config = json.loads(
            Path("lab/analysis/mym_breakout_entry_2026_09/config.json").read_text(encoding="utf-8")
        )
        del config["decision_thresholds"]

        with self.assertRaisesRegex(ValueError, "configuration"):
            validate_config(config)


if __name__ == "__main__":
    unittest.main()
