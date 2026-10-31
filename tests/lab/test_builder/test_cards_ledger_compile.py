"""Strategy builder v1, build steps 1-2: card schema, ledger and compiler on synthetic bars."""
from __future__ import annotations

import json

import pandas as pd
import pytest

from builder import cards, compile as C, ledger

BASE = """
id: t-001
family: orb
instrument: MCL
entry: {type: breakout, range: first_n_bars, side: both, order: stop}
exit: {stop: range_opposite, target: none, flat_at: "10:30"}
params: {n_bars: {value: 2, step: 1}}
"""


def card(text: str = BASE) -> cards.Card:
    return cards.parse(text)


def bars(day: str = "2024-03-05", overrides: dict | None = None, px: float = 70.0) -> pd.DataFrame:
    """Flat 15m bars 03:00-11:45 ET with a 0.10 range each; overrides map HH:MM -> (o, h, l, c)."""
    t = pd.date_range(f"{day} 03:00", f"{day} 11:45", freq="15min", tz="America/New_York")
    rows = {s.strftime("%H:%M"): (px, px + 0.05, px - 0.05, px) for s in t}
    rows.update(overrides or {})
    o, h, l, c = zip(*(rows[s.strftime("%H:%M")] for s in t))
    return pd.DataFrame({"open": o, "high": h, "low": l, "close": c}, index=t)


# Range bars 09:00 and 09:15 span 69.90-70.20, so the long level is 70.21 and the short 69.89.
RANGE = {"09:00": (70.0, 70.2, 69.9, 70.1), "09:15": (70.1, 70.2, 70.0, 70.1)}


# --- cards ---------------------------------------------------------------------------------

def test_hash_ignores_formatting_and_key_order():
    alt = BASE.replace("params: {n_bars: {value: 2, step: 1}}", "params:\n  n_bars: {step: 1, value: 2}")
    assert card().sha256 == card(alt).sha256 and len(card().sha256) == 64


@pytest.mark.parametrize("old,new,msg", [
    ("stop: range_opposite", "stop: trailing", "outside the library"),
    ('flat_at: "10:30"', "flat_at: 10:30", "quoted HH:MM"),
    ("{n_bars: {value: 2, step: 1}}", "{n_bars: {value: 2, step: 1}, stop_atr: {value: 1, step: 1}}", "params must be exactly"),
    ("{value: 2, step: 1}", "{value: 2, step: 0}", "positive step"),
    ("family: orb", "family: trend", "orb family only"),
    ("instrument: MCL", "instrument: ES", "not in builder.instruments"),
])
def test_rejects_cards_outside_the_library(old, new, msg):
    with pytest.raises(cards.CardError, match=msg):
        card(BASE.replace(old, new))


def test_day_of_week_needs_days_and_vice_versa():
    with pytest.raises(cards.CardError, match="day_of_week"):
        card(BASE + "filters: [day_of_week]\n")
    assert card(BASE + "filters: [day_of_week]\ndays: [0, 1]\n").days == (0, 1)


def test_neighbours_skip_invalid_values():
    one = card(BASE.replace("value: 2", "value: 1"))
    assert [(n, s, c.p("n_bars")) for n, s, c in one.neighbours()] == [("n_bars", 1, 2)]


# --- ledger --------------------------------------------------------------------------------

def test_ledger_counts_distinct_cards_per_instrument(tmp_path):
    p = tmp_path / "ledger.jsonl"
    a, b = card(), card(BASE.replace("value: 2", "value: 3"))
    ledger.append_cards(p, "run-1", [a, b])
    ledger.append_cards(p, "run-2", [a])
    assert ledger.k(p, "MCL") == 2 and ledger.k(p, "M2K") == 0 and ledger.contains(p, a.sha256)


def test_ledger_detects_edit_and_deletion(tmp_path):
    p = tmp_path / "ledger.jsonl"
    ledger.append_cards(p, "run-1", [card(), card(BASE.replace("value: 2", "value: 3"))])
    lines = p.read_text().splitlines()
    e = json.loads(lines[0]); e["instrument"] = "M2K"
    p.write_text(json.dumps(e) + "\n" + lines[1] + "\n")
    with pytest.raises(ledger.LedgerError):
        ledger.read(p)
    p.write_text(lines[1] + "\n")
    with pytest.raises(ledger.LedgerError):
        ledger.k(p, "MCL")


def test_holdout_look_once_and_only_for_ledgered_cards(tmp_path):
    p = tmp_path / "ledger.jsonl"
    with pytest.raises(ledger.LedgerError, match="unledgered"):
        ledger.append_holdout_look(p, "run-1", card())
    ledger.append_cards(p, "run-1", [card()])
    ledger.append_holdout_look(p, "run-1", card())
    with pytest.raises(ledger.LedgerError, match="already"):
        ledger.append_holdout_look(p, "run-1", card())
    assert ledger.k(p, "MCL") == 1


# --- compiler ------------------------------------------------------------------------------

def test_long_breakout_fills_one_tick_over_and_exits_at_flat():
    b = bars(overrides={**RANGE, "09:45": (70.15, 70.30, 70.10, 70.28)})
    [t] = C.simulate(card(), b)
    assert (t.side, t.entry_px, t.reason, t.exit_px) == (1, 70.21, "flat", 70.0)


def test_gap_through_level_fills_at_open():
    b = bars(overrides={**RANGE, "09:30": (70.40, 70.45, 70.35, 70.40)})
    [t] = C.simulate(card(), b)
    assert t.entry_px == 70.40


def test_stop_counts_in_the_entry_bar_but_target_does_not():
    tgt = BASE.replace("target: none", "target: r_multiple").replace(
        "{n_bars: {value: 2, step: 1}}", "{n_bars: {value: 2, step: 1}, target_r: {value: 0.1, step: 0.1}}")
    b = bars(overrides={**RANGE, "09:30": (70.15, 70.40, 69.85, 70.0)})
    trades = C.simulate(card(tgt), b)
    assert (trades[0].side, trades[0].reason, trades[0].exit_px) == (1, "stop", 69.89)


def test_stop_first_when_a_later_bar_reaches_both():
    tgt = BASE.replace("stop: range_opposite", "stop: fixed_ticks").replace("target: none", "target: r_multiple").replace(
        "{n_bars: {value: 2, step: 1}}",
        "{n_bars: {value: 2, step: 1}, stop_ticks: {value: 10, step: 1}, target_r: {value: 1, step: 0.5}}")
    b = bars(overrides={**RANGE, "09:30": (70.15, 70.22, 70.15, 70.2), "09:45": (70.2, 70.40, 70.0, 70.2)})
    [t] = C.simulate(card(tgt), b)
    assert (t.reason, t.exit_px) == ("stop", pytest.approx(70.11))


def test_bar_touching_both_levels_fills_the_side_nearer_its_open():
    b = bars(overrides={**RANGE, "09:30": (69.92, 70.25, 69.85, 70.0)})
    assert C.simulate(card(BASE.replace("side: both", "side: both")), b)[0].side == -1


def test_side_long_ignores_downside_breaks():
    b = bars(overrides={**RANGE, "09:30": (70.0, 70.05, 69.80, 69.85)})
    assert C.simulate(card(BASE.replace("side: both", "side: long")), b) == []


def test_min_range_atr_filter_blocks_narrow_ranges():
    f = BASE.replace("{n_bars: {value: 2, step: 1}}",
                     "{n_bars: {value: 2, step: 1}, min_range_atr: {value: 50, step: 1}}") + "filters: [min_range_atr]\n"
    b = bars(overrides={**RANGE, "09:45": (70.15, 70.30, 70.10, 70.28)})
    assert C.simulate(card(f), b) == [] and len(C.simulate(card(), b)) == 1


def test_bars_after_the_exit_do_not_change_the_trade():
    b1 = bars(overrides={**RANGE, "09:45": (70.15, 70.30, 70.10, 70.28)})
    b2 = bars(overrides={**RANGE, "09:45": (70.15, 70.30, 70.10, 70.28), "11:30": (90.0, 95.0, 50.0, 60.0)})
    assert C.simulate(card(), b1) == C.simulate(card(), b2)


def test_day_without_full_range_is_skipped():
    b = bars(overrides={**RANGE, "09:45": (70.15, 70.30, 70.10, 70.28)}).drop(
        pd.Timestamp("2024-03-05 09:15", tz="America/New_York"))
    assert C.simulate(card(), b) == []


def test_max_trades_rearms_after_a_stop():
    m = BASE.replace("{n_bars: {value: 2, step: 1}}",
                     "{n_bars: {value: 2, step: 1}, max_trades_per_day: {value: 2, step: 1}}") + "filters: [max_trades_per_day]\n"
    b = bars(overrides={**RANGE, "09:30": (70.15, 70.25, 70.15, 70.2), "09:45": (70.2, 70.2, 69.85, 69.86),
                            "10:00": (69.9, 69.95, 69.80, 69.85)})
    trades = C.simulate(card(m), b)
    assert [(t.side, t.reason) for t in trades] == [(1, "stop"), (-1, "flat")]
