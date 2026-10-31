"""Strategy builder v1, build steps 1-2: card schema (I-D*), ledger (I-L*) and compiler (I-G1, I-G2)."""
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
DAY = "2024-03-05"


def card(text: str = BASE) -> cards.Card:
    return cards.parse(text)


def bars(day: str = DAY, overrides: dict | None = None, px: float = 70.0, end: str = "11:45") -> pd.DataFrame:
    """Flat 15m bars 03:00-end ET with a 0.10 range each; overrides map HH:MM -> (o, h, l, c)."""
    t = pd.date_range(f"{day} 03:00", f"{day} {end}", freq="15min", tz="America/New_York")
    rows = {s.strftime("%H:%M"): (px, px + 0.05, px - 0.05, px) for s in t}
    rows.update(overrides or {})
    o, h, l, c = zip(*(rows[s.strftime("%H:%M")] for s in t))
    return pd.DataFrame({"open": o, "high": h, "low": l, "close": c}, index=t)


def sim(c: cards.Card, b: pd.DataFrame, dates=(DAY,)):
    return C.simulate(c, b, list(dates))


# Range bars 09:00 and 09:15 span 69.90-70.20, so the long level is 70.21 and the short 69.89.
RANGE = {"09:00": (70.0, 70.2, 69.9, 70.1), "09:15": (70.1, 70.2, 70.0, 70.1)}


# --- cards (I-D1, I-D2) ----------------------------------------------------------------------

def test_hash_ignores_formatting_and_key_order():
    alt = BASE.replace("params: {n_bars: {value: 2, step: 1}}", "params:\n  n_bars: {step: 1, value: 2}")
    assert card().sha256 == card(alt).sha256 and len(card().sha256) == 64


def test_hash_is_unchanged_from_pr_1003():
    # The R1 pre-registration pins card hashes computed by #1003's parser; the rebuild must agree.
    assert card().sha256 == "5beb04119f6068090a3aaa66538153cbfefa5a567a0c994ae3cce2b4bbddbb6a"


@pytest.mark.parametrize("old,new,msg", [
    ("stop: range_opposite", "stop: trailing", "outside the library"),
    ('flat_at: "10:30"', "flat_at: 10:30", "quoted HH:MM"),
    ("{n_bars: {value: 2, step: 1}}", "{n_bars: {value: 2, step: 1}, stop_atr: {value: 1, step: 1}}", "params must be exactly"),
    ("{value: 2, step: 1}", "{value: 2, step: 0}", "positive step"),
    ("{value: 2, step: 1}", "{value: 2.5, step: 1}", "invalid value"),
    ("{value: 2, step: 1}", "{value: true, step: 1}", "numeric value"),
    ("family: orb", "family: trend", "orb family only"),
    ("instrument: MCL", "instrument: ES", "not in builder.instruments"),
    ("id: t-001", "id: ../escape", "card id must match"),
    ("id: t-001", "id: 7", "card id must match"),
    ("id: t-001", "id: t-001\nextra: 1", "unknown card keys"),
])
def test_I_D1_rejects_cards_outside_the_library(old, new, msg):
    with pytest.raises(cards.CardError, match=msg):
        card(BASE.replace(old, new))


@pytest.mark.parametrize("old,new", [
    ("order: stop}", 'order: stop, entry_cutoff: "10:00"}'),         # cutoff in the wrong block
    ('flat_at: "10:30"}', 'flat_at: "10:30", entry_cutoff: "10:00"}'),
    ("side: both,", "side: both, sides: long,"),
])
def test_I_D1_rejects_unknown_entry_and_exit_keys(old, new):
    with pytest.raises(cards.CardError, match="unknown (entry|exit) keys"):
        card(BASE.replace(old, new))


@pytest.mark.parametrize("old,new", [
    ("{value: 2, step: 1}", "{value: 2, step: .nan}"),
    ("{value: 2, step: 1}", "{value: 2, step: .inf}"),
    ("{value: 2, step: 1}", "{value: .inf, step: 1}"),
])
def test_I_D1_rejects_non_finite_int_param_values_and_steps(old, new):
    with pytest.raises(cards.CardError, match="param n_bars"):
        card(BASE.replace(old, new))


@pytest.mark.parametrize("spec", ["{value: 1, step: .nan}", "{value: 1, step: .inf}", "{value: .inf, step: 0.5}",
                                  "{value: .nan, step: 0.5}"])
def test_I_D1_rejects_non_finite_float_param_values_and_steps(spec):
    atr = BASE.replace("stop: range_opposite", "stop: atr_multiple").replace(
        "{n_bars: {value: 2, step: 1}}", "{n_bars: {value: 2, step: 1}, stop_atr: %s}" % spec)
    with pytest.raises(cards.CardError, match="param stop_atr: finite"):
        card(atr)


@pytest.mark.parametrize("extra,msg", [("time: 5\n", "time block"), ("filters: [day_of_week]\ndays: 3\n", "day_of_week"),
    ("filters: [day_of_week]\ndays: [true]\n", "day_of_week")])
def test_I_D1_rejects_wrongly_typed_time_and_days(extra, msg):
    with pytest.raises(cards.CardError, match=msg):
        card(BASE + extra)


def test_I_D1_day_of_week_needs_days_and_vice_versa():
    with pytest.raises(cards.CardError, match="day_of_week"):
        card(BASE + "filters: [day_of_week]\n")
    assert card(BASE + "filters: [day_of_week]\ndays: [0, 1]\n").days == (0, 1)


@pytest.mark.parametrize("old,new", [
    ("value: 2, step: 1", "value: 6, step: 1"),                          # range ends 10:30, at flat/cutoff
    ('flat_at: "10:30"', 'flat_at: "17:30"'),                           # past the trading day
    ('flat_at: "10:30"}', 'flat_at: "10:30"}\ntime: {entry_cutoff: "11:00"}'),  # cutoff after flat
    ('flat_at: "10:30"}', 'flat_at: "10:30"}\ntime: {entry_cutoff: "09:30"}'),  # cutoff at range end
])
def test_I_D2_card_timing_is_refused_at_parse_not_skipped_per_day(old, new):
    with pytest.raises(cards.CardError, match="timing"):
        card(BASE.replace(old, new))


def test_I_D2_neighbours_with_invalid_value_or_timing_are_none():
    one = card(BASE.replace("value: 2", "value: 1"))
    assert [(n, s, nb and nb.p("n_bars")) for n, s, nb in one.neighbours()] == [("n_bars", -1, None), ("n_bars", 1, 2)]
    five = card(BASE.replace("value: 2", "value: 5"))  # n=6 would end the range at the 10:30 flat
    assert [(s, nb is None) for _, s, nb in five.neighbours()] == [(-1, False), (1, True)]


# --- ledger (I-L1, I-L2, I-L3, I-L5) ---------------------------------------------------------

def test_ledger_counts_distinct_cards_per_instrument(tmp_path):
    p = tmp_path / "ledger.jsonl"
    a, b = card(), card(BASE.replace("value: 2", "value: 3"))
    ledger.append_cards(p, "run-1", [a, b])
    ledger.append_cards(p, "run-2", [a])
    assert ledger.k(p, "MCL") == 2 and ledger.k(p, "M2K") == 0 and ledger.contains(p, a.sha256)


def _two(tmp_path):
    p = tmp_path / "ledger.jsonl"
    ledger.append_cards(p, "run-1", [card(), card(BASE.replace("value: 2", "value: 3"))])
    return p, p.read_text().splitlines()


@pytest.mark.parametrize("text", ["{L0}\n\n{L1}\n", "{L0}\n{L1}", "{L0}\nnot json\n", "{L0}\n[1]\n",
                                  "{L0}\n" + '{"seq": 2}' + "\n"])
def test_I_L1_blank_truncated_or_non_object_lines_abort(tmp_path, text):
    p, lines = _two(tmp_path)
    p.write_text(text.replace("{L0}", lines[0]).replace("{L1}", lines[1]))
    with pytest.raises(ledger.LedgerError):
        ledger.read(p)


def test_I_L2_edit_deletion_and_reorder_break_the_chain(tmp_path):
    p, lines = _two(tmp_path)
    e = json.loads(lines[0]); e["run_id"] = "run-9"
    for text in (json.dumps(e) + "\n" + lines[1] + "\n", lines[1] + "\n", lines[1] + "\n" + lines[0] + "\n"):
        p.write_text(text)
        with pytest.raises(ledger.LedgerError, match="chain broken"):
            ledger.k(p, "MCL")


def _forge(p, entry: dict):
    """Append a well-chained entry with arbitrary content, as a careless writer could."""
    prev = ledger.read(p)
    entry = {"seq": len(prev) + 1, "prev": prev[-1]["entry_sha256"], "ts": "t", "run_id": "r", **entry}
    entry["entry_sha256"] = ledger._digest(entry)
    with open(p, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(entry) + "\n")


@pytest.mark.parametrize("entry,msg", [
    ({"kind": "note", "text": "x"}, "unknown kind"),
    ({"kind": "card", "card_sha256": "0" * 64, "card_yaml": BASE, "family": "orb", "instrument": "MCL"}, "do not match"),
    ({"kind": "card", "card_sha256": "x", "card_yaml": "id: [", "family": "orb", "instrument": "MCL"}, "no longer parses"),
    ({"kind": "holdout_look", "card_sha256": "f" * 64, "instrument": "MCL"}, "unledgered"),
])
def test_I_L3_entry_content_is_verified_not_just_chained(tmp_path, entry, msg):
    p, _ = _two(tmp_path)
    _forge(p, entry)
    with pytest.raises(ledger.LedgerError, match=msg):
        ledger.read(p)


def test_I_L5_holdout_look_once_and_only_for_ledgered_cards(tmp_path):
    p = tmp_path / "ledger.jsonl"
    with pytest.raises(ledger.LedgerError, match="unledgered"):
        ledger.append_holdout_look(p, "run-1", card())
    ledger.append_cards(p, "run-1", [card()])
    ledger.append_holdout_look(p, "run-1", card())
    with pytest.raises(ledger.LedgerError, match="already"):
        ledger.append_holdout_look(p, "run-1", card())
    _forge(p, {"kind": "holdout_look", "card_sha256": card().sha256, "instrument": "MCL"})  # a second look by hand
    with pytest.raises(ledger.LedgerError, match="second look"):
        ledger.k(p, "MCL")


# --- compiler --------------------------------------------------------------------------------

def test_long_breakout_fills_one_tick_over_and_exits_at_flat():
    [t] = sim(card(), bars(overrides={**RANGE, "09:45": (70.15, 70.30, 70.10, 70.28)}))
    assert (t.side, t.entry_px, t.reason, t.exit_px) == (1, 70.21, "flat", 70.0)


def test_gap_through_level_fills_at_open():
    [t] = sim(card(), bars(overrides={**RANGE, "09:30": (70.40, 70.45, 70.35, 70.40)}))
    assert t.entry_px == 70.40


def test_stop_counts_in_the_entry_bar_but_target_does_not():
    tgt = BASE.replace("target: none", "target: r_multiple").replace(
        "{n_bars: {value: 2, step: 1}}", "{n_bars: {value: 2, step: 1}, target_r: {value: 0.1, step: 0.1}}")
    trades = sim(card(tgt), bars(overrides={**RANGE, "09:30": (70.15, 70.40, 69.85, 70.0)}))
    assert (trades[0].side, trades[0].reason, trades[0].exit_px) == (1, "stop", 69.89)


def test_stop_first_when_a_later_bar_reaches_both():
    tgt = BASE.replace("stop: range_opposite", "stop: fixed_ticks").replace("target: none", "target: r_multiple").replace(
        "{n_bars: {value: 2, step: 1}}",
        "{n_bars: {value: 2, step: 1}, stop_ticks: {value: 10, step: 1}, target_r: {value: 1, step: 0.5}}")
    [t] = sim(card(tgt), bars(overrides={**RANGE, "09:30": (70.15, 70.22, 70.15, 70.2), "09:45": (70.2, 70.40, 70.0, 70.2)}))
    assert (t.reason, t.exit_px) == ("stop", pytest.approx(70.11))


def test_bar_touching_both_levels_fills_the_side_nearer_its_open():
    assert sim(card(), bars(overrides={**RANGE, "09:30": (69.92, 70.25, 69.85, 70.0)}))[0].side == -1


def test_side_long_ignores_downside_breaks():
    assert sim(card(BASE.replace("side: both", "side: long")), bars(overrides={**RANGE, "09:30": (70.0, 70.05, 69.80, 69.85)})) == []


def test_min_range_atr_filter_blocks_narrow_ranges():
    f = BASE.replace("{n_bars: {value: 2, step: 1}}",
                     "{n_bars: {value: 2, step: 1}, min_range_atr: {value: 50, step: 1}}") + "filters: [min_range_atr]\n"
    b = bars(overrides={**RANGE, "09:45": (70.15, 70.30, 70.10, 70.28)})
    assert sim(card(f), b) == [] and len(sim(card(), b)) == 1


def test_bars_after_the_exit_do_not_change_the_trade():
    b1 = bars(overrides={**RANGE, "09:45": (70.15, 70.30, 70.10, 70.28)})
    b2 = bars(overrides={**RANGE, "09:45": (70.15, 70.30, 70.10, 70.28), "11:30": (90.0, 95.0, 50.0, 60.0)})
    assert sim(card(), b1) == sim(card(), b2)


def test_max_trades_rearms_after_a_stop():
    m = BASE.replace("{n_bars: {value: 2, step: 1}}",
                     "{n_bars: {value: 2, step: 1}, max_trades_per_day: {value: 2, step: 1}}") + "filters: [max_trades_per_day]\n"
    b = bars(overrides={**RANGE, "09:30": (70.15, 70.25, 70.15, 70.2), "09:45": (70.2, 70.2, 69.85, 69.86),
                        "10:00": (69.9, 69.95, 69.80, 69.85)})
    assert [(t.side, t.reason) for t in sim(card(m), b)] == [(1, "stop"), (-1, "flat")]


def test_early_halt_exits_at_the_last_day_bar_not_the_evening_session():
    # #1003 kept a date's bars after 17:00, so a day with no flat bar exited at the 18:00 reopen.
    day = bars(overrides={**RANGE, "09:45": (70.15, 70.30, 70.10, 70.28)}, end="10:00")
    t = pd.date_range(f"{DAY} 18:00", f"{DAY} 23:45", freq="15min", tz="America/New_York")
    evening = pd.DataFrame({"open": 80.0, "high": 80.05, "low": 79.95, "close": 80.0}, index=t)
    [tr] = sim(card(), pd.concat([day, evening]))
    assert (tr.reason, tr.exit_px) == ("flat", 70.0)


def test_I_G1_atr_is_never_computed_across_a_gap():
    atr_card = card(BASE.replace("stop: range_opposite", "stop: atr_multiple").replace(
        "{n_bars: {value: 2, step: 1}}", "{n_bars: {value: 2, step: 1}, stop_atr: {value: 1, step: 0.5}}"))
    b = bars(overrides={**RANGE, "09:45": (70.15, 70.30, 70.10, 70.28)})
    hole = b.drop(pd.Timestamp(f"{DAY} 07:00", tz="America/New_York"))  # overnight gap inside the ATR window
    skipped = {}
    assert C.days(atr_card, hole, [DAY], skipped) == [] and skipped == {"atr_window_gap": 1}
    assert len(sim(atr_card, b)) == 1 and len(sim(card(), hole)) == 1  # ATR not needed: the day trades


def test_I_G2_every_skipped_day_is_counted_by_reason():
    dow = card(BASE + "filters: [day_of_week]\ndays: [0]\n")  # Mondays only; DAY is a Tuesday
    skipped = {}
    assert C.days(dow, bars(), [DAY], skipped) == [] and skipped == {"day_of_week": 1}
    skipped = {}
    assert C.days(card(), bars(end="09:15"), [DAY], skipped) == [] and skipped == {"short_session": 1}
