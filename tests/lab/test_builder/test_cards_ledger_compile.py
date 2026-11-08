"""Strategy builder v1, build steps 1-2: card schema (I-D*), ledger (I-L*) and compiler (I-G1, I-G2)."""
from __future__ import annotations

import json
import multiprocessing as mp
import threading
import time
from pathlib import Path

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


# --- head anchor: rollback detection (#1134) and atomic check-and-append (#1141) ----------------

def _anchored(tmp_path):
    """Two cards, then a holdout look for the first: (path, lines, anchor path)."""
    p, _ = _two(tmp_path)
    ledger.append_holdout_look(p, "run-1", card())
    return p, p.read_text().splitlines(), ledger.head_path(p)


def test_append_writes_the_head_anchor_after_the_ledger(tmp_path):
    p, lines, hp = _anchored(tmp_path)
    last = json.loads(lines[-1])
    assert json.loads(hp.read_text()) == {"seq": 3, "entry_sha256": last["entry_sha256"]} == ledger.head(p)
    assert len(ledger.read(p)) == 3


def test_tail_truncation_to_a_valid_prefix_is_refused_and_cannot_respend_a_look(tmp_path):
    p, lines, _ = _anchored(tmp_path)
    p.write_text(lines[0] + "\n" + lines[1] + "\n")  # the look is gone; the chain alone reads clean
    with pytest.raises(ledger.LedgerError, match="rolled back"):
        ledger.read(p)
    with pytest.raises(ledger.LedgerError, match="rolled back"):
        ledger.append_holdout_look(p, "run-2", card())
    assert p.read_text() == lines[0] + "\n" + lines[1] + "\n"


def test_k_cannot_shrink_under_rollback(tmp_path):
    p, lines = _two(tmp_path)
    assert ledger.k(p, "MCL") == 2
    p.write_text(lines[0] + "\n")
    with pytest.raises(ledger.LedgerError, match="rolled back"):
        ledger.k(p, "MCL")


def test_restoring_an_older_copy_is_refused(tmp_path):
    p = tmp_path / "ledger.jsonl"
    ledger.append_cards(p, "run-1", [card()])
    older = p.read_bytes()
    ledger.append_holdout_look(p, "run-1", card())
    p.write_bytes(older)
    with pytest.raises(ledger.LedgerError, match="rolled back"):
        ledger.read(p)
    p.unlink()  # deleting the ledger outright is the same rollback
    with pytest.raises(ledger.LedgerError, match="rolled back"):
        ledger.read(p)


def test_a_different_history_of_the_same_length_is_refused(tmp_path):
    p = tmp_path / "ledger.jsonl"
    ledger.append_cards(p, "run-1", [card()])
    other = tmp_path / "other" / "ledger.jsonl"
    ledger.append_cards(other, "run-9", [card(BASE.replace("value: 2", "value: 3"))])
    p.write_bytes(other.read_bytes())
    with pytest.raises(ledger.LedgerError, match="does not hold its head anchor"):
        ledger.read(p)


def test_missing_anchor_is_refused_and_never_created_by_a_read(tmp_path):
    p, _ = _two(tmp_path)
    ledger.head_path(p).unlink()
    for _ in range(2):
        with pytest.raises(ledger.LedgerError, match="no head anchor"):
            ledger.read(p)
    assert not ledger.head_path(p).exists()
    empty = tmp_path / "empty.jsonl"
    empty.write_text("")
    assert ledger.read(empty) == [] and ledger.read(tmp_path / "absent.jsonl") == []
    assert ledger.read(tmp_path / "no-dir" / "l.jsonl") == [] and not (tmp_path / "no-dir").exists()


@pytest.mark.parametrize("anchor", ["not json", "[]", '{"seq": 0, "entry_sha256": "' + "0" * 64 + '"}',
                                    '{"seq": true, "entry_sha256": "' + "0" * 64 + '"}',
                                    '{"seq": 1, "entry_sha256": "x"}'])
def test_malformed_anchor_is_refused(tmp_path, anchor):
    p, _ = _two(tmp_path)
    ledger.head_path(p).write_text(anchor)
    with pytest.raises(ledger.LedgerError):
        ledger.read(p)


def test_an_append_interrupted_before_its_anchor_is_refused_until_adopted(tmp_path, capsys):
    p, _ = _two(tmp_path)
    hp = ledger.head_path(p)
    before = hp.read_text()
    ledger.append_holdout_look(p, "run-1", card())
    hp.write_text(before)  # the crash window: ledger line fsynced, anchor not yet replaced
    with pytest.raises(ledger.LedgerError, match="1 entries past its head anchor"):
        ledger.read(p)
    head = json.loads(p.read_text().splitlines()[-1])["entry_sha256"]
    assert ledger.main(["adopt-head", str(p)]) == 0  # prints only
    shown = json.loads(capsys.readouterr().out)
    assert shown["head"] == {"seq": 3, "entry_sha256": head} and not shown["written"] and hp.read_text() == before
    with pytest.raises(ledger.LedgerError, match="is not the head"):
        ledger.adopt_head(p, "f" * 64)
    assert ledger.main(["adopt-head", str(p), "--confirm", head]) == 0
    assert json.loads(capsys.readouterr().out)["written"] and len(ledger.read(p)) == 3


def test_adopt_head_bootstraps_an_unanchored_ledger_but_never_launders_a_rollback(tmp_path):
    p, lines, hp = _anchored(tmp_path)
    p.write_text(lines[0] + "\n")  # rolled back past the anchor
    first = json.loads(lines[0])["entry_sha256"]
    with pytest.raises(ledger.LedgerError, match="will not overwrite"):
        ledger.adopt_head(p, first)
    hp.unlink()  # a pre-anchor ledger: the operator verifies the printed head, then confirms it
    assert ledger.adopt_head(p, None)["anchor"] is None and not hp.exists()
    assert ledger.adopt_head(p, first)["written"] and ledger.head(p) == {"seq": 1, "entry_sha256": first}


def _look_after_a_slow_read(path: str, run_id: str, barrier, results) -> None:
    """One caller (a spawned process): meet the other at the barrier, then spend the look with a
    slowed locked read, so an unlocked check-then-append would let both callers pass the check."""
    real = ledger._read_locked

    def slow(p):
        entries = real(p)
        time.sleep(0.3)
        return entries
    ledger._read_locked = slow
    barrier.wait(timeout=60)
    try:
        ledger.append_holdout_look(Path(path), run_id, card())
        results.put("ok")
    except ledger.LedgerError as e:
        results.put(str(e))


def test_concurrent_holdout_looks_across_processes_have_exactly_one_winner(tmp_path):
    p = tmp_path / "ledger.jsonl"
    ledger.append_cards(p, "run-1", [card()])
    ctx = mp.get_context("spawn")
    barrier, results = ctx.Barrier(2), ctx.Queue()
    procs = [ctx.Process(target=_look_after_a_slow_read, args=(str(p), f"proc-{i}", barrier, results))
             for i in (1, 2)]
    for pr in procs:
        pr.start()
    out = sorted(results.get(timeout=120) for _ in procs)
    for pr in procs:
        pr.join(timeout=60)
        assert pr.exitcode == 0
    assert out[1] == "ok" and "already had its one holdout look" in out[0]
    assert [e["kind"] for e in ledger.read(p)] == ["card", "holdout_look"]


def test_concurrent_card_appends_keep_one_chain(tmp_path):
    p = tmp_path / "ledger.jsonl"
    cs = [card(BASE.replace("id: t-001", f"id: t-{i:03d}")) for i in range(1, 9)]
    barrier = threading.Barrier(len(cs))

    def append(c):
        barrier.wait(timeout=60)
        ledger.append_cards(p, c.id, [c])
    ts = [threading.Thread(target=append, args=(c,)) for c in cs]
    for t in ts:
        t.start()
    for t in ts:
        t.join(timeout=60)
    assert ledger.k(p, "MCL") == len(cs) and ledger.head(p)["seq"] == len(cs)


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


def test_early_halt_leaves_the_trade_unresolved_not_filled_at_the_evening_or_last_close():
    # #1003 exited at the 18:00 reopen; #1004 at the last day bar's close, a hindsight price.
    day = bars(overrides={**RANGE, "09:45": (70.15, 70.30, 70.10, 70.28)}, end="10:00")
    t = pd.date_range(f"{DAY} 18:00", f"{DAY} 23:45", freq="15min", tz="America/New_York")
    evening = pd.DataFrame({"open": 80.0, "high": 80.05, "low": 79.95, "close": 80.0}, index=t)
    [tr] = sim(card(), pd.concat([day, evening]))
    assert (tr.reason, tr.exit_i, tr.exit_px, tr.unresolved) == ("unresolved", None, None, True)
    with pytest.raises(ValueError, match="no exit price"):
        tr.points


def test_entry_decision_depends_only_on_bars_up_to_entry():
    # Paired fixture: identical bars through the 09:45 entry; afterwards one day runs to 11:45 with
    # a different path, the other halts at 10:00, before the 10:30 flat_at.
    common = {**RANGE, "09:45": (70.15, 70.30, 70.10, 70.28)}
    full = bars(overrides={**common, "10:00": (70.3, 70.6, 70.25, 70.5), "10:30": (70.6, 70.7, 70.5, 70.6)})
    cut = bars(overrides=common, end="10:00")
    assert (full.loc[:f"{DAY} 09:45"] == cut.loc[:f"{DAY} 09:45"]).all().all()
    [a], [b] = sim(card(), full), sim(card(), cut)
    assert (a.side, a.entry_i, a.entry_px) == (b.side, b.entry_i, b.entry_px) == (1, 3, 70.21)
    assert (a.reason, a.exit_px) == ("flat", 70.6) and b.reason == "unresolved"


def test_a_stop_before_an_early_halt_is_still_resolved():
    b = bars(overrides={**RANGE, "09:45": (70.15, 70.30, 70.10, 70.28), "10:00": (70.2, 70.2, 69.8, 69.85)},
             end="10:00")
    [t] = sim(card(), b)
    assert (t.reason, t.exit_px) == ("stop", 69.89)


def test_calendar_exception_day_is_not_traded_and_counted():
    skipped = {}
    b = bars(overrides={**RANGE, "09:45": (70.15, 70.30, 70.10, 70.28)})
    assert C.days(card(), b, [DAY], skipped, frozenset({DAY})) == [] and skipped == {"calendar_exception": 1}
    assert C.simulate(card(), b, [DAY], frozenset({DAY})) == [] and len(sim(card(), b)) == 1


def test_I_G1_atr_is_never_computed_across_a_gap():
    atr_card = card(BASE.replace("stop: range_opposite", "stop: atr_multiple").replace(
        "{n_bars: {value: 2, step: 1}}", "{n_bars: {value: 2, step: 1}, stop_atr: {value: 1, step: 0.5}}"))
    b = bars(overrides={**RANGE, "09:45": (70.15, 70.30, 70.10, 70.28)})
    hole = b.drop(pd.Timestamp(f"{DAY} 07:00", tz="America/New_York"))  # overnight gap inside the ATR window
    skipped = {}
    assert C.days(atr_card, hole, [DAY], skipped) == [] and skipped == {"atr_window_gap": 1}
    assert len(sim(atr_card, b)) == 1 and len(sim(card(), hole)) == 1  # ATR not needed: the day trades


# --- missing bars (W1 contract v5 §3) -------------------------------------------------------

def drop(b: pd.DataFrame, *hhmm: str) -> pd.DataFrame:
    return b.drop([pd.Timestamp(f"{DAY} {x}", tz="America/New_York") for x in hhmm])


@pytest.mark.parametrize("slot", ["09:00", "09:15"])
def test_missing_range_slot_skips_the_day_for_the_card_and_its_neighbours(slot):
    b = drop(bars(overrides={**RANGE, "09:45": (70.15, 70.30, 70.10, 70.28)}), slot)
    skipped = {}
    assert C.days(card(), b, [DAY], skipped) == [] and skipped == {"range_gap": 1}
    n1 = card(BASE.replace("value: 2", "value: 1"))
    assert len(sim(n1, b)) == (slot == "09:15")  # a 1-bar neighbour's own range is 09:00 only


def test_offset_range_uses_clock_slots_not_bar_positions():
    # A missing pre-range bar must not shift the range: positions would move it to 09:15-09:30.
    b = drop(bars(overrides={**RANGE, "09:45": (70.15, 70.30, 70.10, 70.28)}), "08:00")
    [t] = sim(card(), b)
    assert (t.side, t.entry_px) == (1, 70.21)


def test_missing_bar_after_the_range_is_a_no_trade_interval():
    # The 09:30 bar would have broken out; without it the entry waits for the next real bar.
    b = drop(bars(overrides={**RANGE, "09:30": (70.15, 70.30, 70.10, 70.28),
                             "09:45": (70.15, 70.30, 70.10, 70.28)}), "09:30")
    [t] = sim(card(), b)
    assert t.entry_i == 2 and b.index[b.index.get_loc(pd.Timestamp(f"{DAY} 09:00", tz="America/New_York")) + t.entry_i]         .strftime("%H:%M") == "09:45"


def test_flat_on_a_missing_bar_exits_at_the_next_real_bar_open():
    b = drop(bars(overrides={**RANGE, "09:45": (70.15, 70.30, 70.10, 70.28), "10:45": (70.4, 70.45, 70.35, 70.4)}),
             "10:30")
    [t] = sim(card(), b)
    assert (t.reason, t.exit_px) == ("flat", 70.4)


def test_flat_on_a_missing_bar_with_no_later_bar_is_unresolved():
    b = bars(overrides={**RANGE, "09:45": (70.15, 70.30, 70.10, 70.28)}, end="10:15")
    [t] = sim(card(), b)
    assert t.reason == "unresolved"


def test_I_G2_every_skipped_day_is_counted_by_reason():
    dow = card(BASE + "filters: [day_of_week]\ndays: [0]\n")  # Mondays only; DAY is a Tuesday
    skipped = {}
    assert C.days(dow, bars(), [DAY], skipped) == [] and skipped == {"day_of_week": 1}
    skipped = {}
    assert C.days(card(), bars(end="09:15"), [DAY], skipped) == [] and skipped == {"short_session": 1}
