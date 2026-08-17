"""Pre-data unit tests for MNQ-SIZEDIV-1 (run green BEFORE any pull; see DESIGN_FREEZE §9)."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from research_utils.camp_import import load_camp_sibling

S = load_camp_sibling("sizediv_lib", __file__)
ET, combine_stats, load_calendar, load_slot_returns, rth_mask, session_stats, sizediv = (
    S.ET, S.combine_stats, S.load_calendar, S.load_slot_returns, S.rth_mask,
    S.session_stats, S.sizediv,
)


def _trades(rows):
    """rows: (iso_utc_ts, price, size, side)."""
    df = pd.DataFrame(rows, columns=["ts_event", "price", "size", "side"])
    df["ts_event"] = pd.to_datetime(df["ts_event"], utc=True)
    return df


def test_sizediv_known_values():
    # Session 2024-03-05 (EST): buys 10+30 @ sizes, sells 5+5. All RTH (15:00Z=10:00 ET).
    t = _trades([
        ("2024-03-05T15:00:00Z", 18000.00, 10, "B"),
        ("2024-03-05T15:01:00Z", 18000.25, 30, "B"),
        ("2024-03-05T15:02:00Z", 18000.00, 5, "A"),
        ("2024-03-05T15:03:00Z", 17999.75, 5, "A"),
        ("2024-03-05T15:04:00Z", 18000.00, 7, "N"),  # unsignable, excluded
    ])
    s = sizediv(combine_stats([session_stats(t)]))
    assert len(s) == 1
    row = s.iloc[0]
    assert row["V_B"] == 40 and row["V_A"] == 10
    assert row["N_B"] == 2 and row["N_A"] == 2
    assert row["n_prints"] == 5 and row["n_signable"] == 4
    assert row["I_vw"] == pytest.approx(30 / 50)
    assert row["I_cw"] == pytest.approx(0.0)
    assert row["A"] == pytest.approx(0.6)


def test_tick_rule_tallies():
    # up-move on B (agree), down-move on A (agree), up-move on A (disagree), flat dropped
    t = _trades([
        ("2024-03-05T15:00:00Z", 100.00, 1, "B"),
        ("2024-03-05T15:00:01Z", 100.25, 1, "B"),  # +1 vs B => agree
        ("2024-03-05T15:00:02Z", 100.00, 1, "A"),  # -1 vs A => agree
        ("2024-03-05T15:00:03Z", 100.25, 1, "A"),  # +1 vs A => disagree
        ("2024-03-05T15:00:04Z", 100.25, 1, "B"),  # 0 => dropped
    ])
    s = combine_stats([session_stats(t)]).iloc[0]
    assert s["tick_agree"] == 2 and s["tick_disagree"] == 1


def test_rth_mask_dst_boundary():
    # 2024-03-08 (EST, UTC-5): 14:30Z == 09:30 ET => RTH. 2024-03-11 (EDT, UTC-4): 14:30Z == 10:30 ET => RTH,
    # and 13:29Z == 09:29 ET => pre-RTH.
    ts = pd.Series(pd.to_datetime([
        "2024-03-08T14:30:00Z", "2024-03-08T13:30:00Z",
        "2024-03-11T13:29:00Z", "2024-03-11T13:30:00Z", "2024-03-11T20:00:00Z",
    ], utc=True)).dt.tz_convert(ET)
    m = rth_mask(ts)
    assert list(m) == [True, False, False, True, False]  # 20:00Z EDT == 16:00 ET => excluded


def _panel_csv(days):
    """Synthetic M15 panel: for each date, full 26-bar RTH ladder (+2 non-RTH bars)."""
    rows = []
    for d, px in days:
        base = pd.Timestamp(f"{d}T09:30:00", tz=ET)
        rows.append((base - pd.Timedelta(minutes=15), px, px, px, px, 1))  # 09:15 non-RTH
        for i in range(26):
            t = base + pd.Timedelta(minutes=15 * i)
            o = px + i
            rows.append((t, o, o + 1, o - 1, o + 0.5, 10))
        rows.append((base + pd.Timedelta(hours=6, minutes=45), px, px, px, px, 1))  # 16:15
    df = pd.DataFrame(rows, columns=["time", "open", "high", "low", "close", "volume"])
    df["time"] = df["time"].apply(lambda t: t.tz_convert("UTC").strftime("%Y-%m-%dT%H:%M:%SZ"))
    return df.to_csv(index=False)


def test_calendar_and_slots(tmp_path):
    p = tmp_path / "panel.csv"
    p.write_text(_panel_csv([("2024-03-05", 18000.0), ("2024-03-11", 18100.0)]))  # spans DST switch
    cal = load_calendar(p)
    assert cal["full"].all() and len(cal) == 2 and (cal["rth_bars"] == 26).all()
    slots = load_slot_returns(p)
    assert len(slots) == 2
    # r1 = ln(open_1245/open_0930): open ladder is px + i, bar 13 (12:45) opens px+13
    r1_expect = np.log((18000 + 13) / 18000) * 1e4
    r2_expect = np.log((18000 + 25 + 0.5) / (18000 + 13)) * 1e4
    row = slots[slots["date"] == pd.Timestamp("2024-03-05").date()].iloc[0]
    assert row["r1_bp"] == pytest.approx(r1_expect, abs=1e-6)
    assert row["r2_bp"] == pytest.approx(r2_expect, abs=1e-6)


def test_combine_across_chunks_and_degeneracy_guard():
    a = _trades([("2024-03-05T15:00:00Z", 100.00, 10, "B")])
    b = _trades([("2024-03-05T18:00:00Z", 100.25, 40, "A"),
                 ("2024-03-06T15:00:00Z", 100.00, 5, "B")])
    s = sizediv(combine_stats([session_stats(a), session_stats(b)]))
    d1 = s[s["date"] == pd.Timestamp("2024-03-05").date()].iloc[0]
    assert d1["V_B"] == 10 and d1["V_A"] == 40 and d1["N_B"] == 1 and d1["N_A"] == 1
    assert d1["A"] == pytest.approx((10 - 40) / 50 - 0.0)
    d2 = s[s["date"] == pd.Timestamp("2024-03-06").date()].iloc[0]
    assert d2["I_vw"] == 1.0 and d2["I_cw"] == 1.0 and d2["A"] == 0.0
