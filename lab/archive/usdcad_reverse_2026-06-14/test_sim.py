"""Synthetic-bar unit tests for the breakout simulator (look-ahead-free, STOP-FIRST)."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import usdcad_harness as H  # noqa: E402

ATR = 0.0010          # 10 pips
K = 2.0               # stop_dist = 0.0020 (20 pips)
COST_R = H.RT_COST_PIP * H.PIP / (K * ATR)   # 0.8pip / 20pip = 0.04R


def make_bars(o, h, l, c, *, et_hour=9, contig=None):
    n = len(o)
    o, h, l, c = (np.array(x, float) for x in (o, h, l, c))
    if contig is None:
        contig = np.array([False] + [True] * (n - 1))
    return H.Bars(
        open=o, high=h, low=l, close=c,
        atr=np.full(n, ATR), et_hour=np.full(n, et_hour, int),
        et_min=np.zeros(n, int), et_date=np.zeros(n, int),
        contig=np.array(contig, bool), don_high={}, don_low={},
        volfloor_ok=np.ones(n, bool), n=n,
    )


def long_at0(n):
    s = np.zeros(n, bool); s[0] = True
    return s, np.zeros(n, bool)


def approx(a, b, tol=1e-9):
    assert abs(a - b) < tol, f"{a} != {b}"


def test_long_tp_hit():
    # entry at open[1]=1.0000, tp=+2R=1.0040 hit on bar1
    o = [1.0, 1.0000, 1.0, 1.0]; h = [1.0, 1.0050, 1.0, 1.0]
    l = [1.0, 0.9990, 1.0, 1.0]; c = [1.0, 1.0030, 1.0, 1.0]
    ls, ss = long_at0(4)
    r = H.simulate(make_bars(o, h, l, c), ls, ss, K, "tp", 2.0)
    assert len(r) == 1
    approx(r[0], 2.0 - COST_R)


def test_long_stop_hit():
    # entry 1.0000, stop=0.9980 hit on bar1
    o = [1.0, 1.0000, 1.0, 1.0]; h = [1.0, 1.0010, 1.0, 1.0]
    l = [1.0, 0.9975, 1.0, 1.0]; c = [1.0, 0.9985, 1.0, 1.0]
    ls, ss = long_at0(4)
    r = H.simulate(make_bars(o, h, l, c), ls, ss, K, "tp", 2.0)
    approx(r[0], -1.0 - COST_R)


def test_stop_first_when_both_touched():
    # bar1 touches both tp(1.0040) and stop(0.9980) -> STOP taken (conservative)
    o = [1.0, 1.0000, 1.0, 1.0]; h = [1.0, 1.0050, 1.0, 1.0]
    l = [1.0, 0.9970, 1.0, 1.0]; c = [1.0, 1.0000, 1.0, 1.0]
    ls, ss = long_at0(4)
    r = H.simulate(make_bars(o, h, l, c), ls, ss, K, "tp", 2.0)
    approx(r[0], -1.0 - COST_R)


def test_entry_is_next_open_not_signal_close():
    # signal bar close is 1.05 but entry must be open[1]=1.0000 (no look-ahead)
    o = [1.05, 1.0000, 1.0, 1.0]; h = [1.05, 1.0050, 1.0, 1.0]
    l = [1.05, 0.9990, 1.0, 1.0]; c = [1.05, 1.0030, 1.0, 1.0]
    ls, ss = long_at0(4)
    r = H.simulate(make_bars(o, h, l, c), ls, ss, K, "tp", 2.0)
    # if it had used 1.05 as entry, R would be wildly different; 2R confirms entry=1.0000
    approx(r[0], 2.0 - COST_R)


def test_short_tp_hit():
    s_long = np.zeros(4, bool)
    s_short = np.zeros(4, bool); s_short[0] = True
    # entry 1.0000, short tp = -2R = 0.9960 hit
    o = [1.0, 1.0000, 1.0, 1.0]; h = [1.0, 1.0010, 1.0, 1.0]
    l = [1.0, 0.9950, 1.0, 1.0]; c = [1.0, 0.9970, 1.0, 1.0]
    r = H.simulate(make_bars(o, h, l, c), s_long, s_short, K, "tp", 2.0, side_mode="both")
    approx(r[0], 2.0 - COST_R)


def test_trailing_locks_gain():
    # rises to ratchet stop up, then reverses into trailed stop at 1.0030 -> +1.5R
    o = [1.0, 1.0000, 1.0040, 1.0030, 1.0, 1.0]
    h = [1.0, 1.0035, 1.0060, 1.0035, 1.0, 1.0]
    l = [1.0, 0.9990, 1.0040, 1.0020, 1.0, 1.0]   # bar3 low 1.0020 <= trailed stop 1.0030
    c = [1.0, 1.0030, 1.0050, 1.0025, 1.0, 1.0]
    ls, ss = long_at0(6)
    r = H.simulate(make_bars(o, h, l, c), ls, ss, K, "trail", 2.0)
    # trail dist = 2*ATR = 0.0020. bar1 close 1.0030 -> stop max(0.9980,1.0010)=1.0010
    # bar2 close 1.0050 -> stop max(1.0010,1.0030)=1.0030 ; bar3 low<=1.0030 -> exit 1.0030
    approx(r[0], (1.0030 - 1.0000) / (K * ATR) - COST_R)


def test_no_fill_across_gap():
    o = [1.0, 1.0, 1.0]; h = [1.0, 1.0, 1.0]; l = [1.0, 1.0, 1.0]; c = [1.0, 1.0, 1.0]
    ls, ss = long_at0(3)
    bars = make_bars(o, h, l, c, contig=[False, False, True])  # bar1 not contiguous
    r = H.simulate(bars, ls, ss, K, "tp", 2.0)
    assert len(r) == 0


def test_weekend_flat_forced_exit():
    # no stop/tp; gap before bar2 forces exit at close[1]
    o = [1.0, 1.0000, 1.0]; h = [1.0, 1.0010, 1.0]; l = [1.0, 0.9995, 1.0]; c = [1.0, 1.0005, 1.0]
    ls, ss = long_at0(3)
    bars = make_bars(o, h, l, c, contig=[False, True, False])  # gap before bar2
    r = H.simulate(bars, ls, ss, K, "tp", 2.0)
    approx(r[0], (1.0005 - 1.0000) / (K * ATR) - COST_R)


def test_reversion_control_flips_side():
    # long breakout signal, reversion mode trades SHORT; price falls -> short profits
    o = [1.0, 1.0000, 1.0, 1.0]; h = [1.0, 1.0010, 1.0, 1.0]
    l = [1.0, 0.9950, 1.0, 1.0]; c = [1.0, 0.9970, 1.0, 1.0]
    ls, ss = long_at0(4)
    r = H.simulate(make_bars(o, h, l, c), ls, ss, K, "tp", 2.0, side_mode="reversion")
    approx(r[0], 2.0 - COST_R)


def test_stopentry_long_fills_at_level():
    # level 1.0000, open below it, high triggers -> entry == level (not open)
    o = [1.0, 0.9990, 1.0, 1.0]; h = [1.0, 1.0005, 1.0050, 1.0]
    l = [1.0, 0.9985, 1.0030, 1.0]; c = [1.0, 1.0000, 1.0040, 1.0]
    ll = np.array([np.nan, 1.0000, np.nan, np.nan])
    sl = np.full(4, np.nan); valid = np.array([False, True, False, False])
    r = H.simulate_stop_entry(make_bars(o, h, l, c), ll, sl, valid, K, "tp", 2.0)
    assert len(r) == 1
    approx(r[0], 2.0 - COST_R)   # 2R from entry=1.0000


def test_stopentry_gap_fills_at_open():
    # open 1.0010 gaps above level 1.0000 -> entry==open; stop 0.9990 hit on entry bar
    o = [1.0, 1.0010, 1.0, 1.0]; h = [1.0, 1.0020, 1.0, 1.0]
    l = [1.0, 0.9985, 1.0, 1.0]; c = [1.0, 1.0000, 1.0, 1.0]
    ll = np.array([np.nan, 1.0000, np.nan, np.nan])
    sl = np.full(4, np.nan); valid = np.array([False, True, False, False])
    r = H.simulate_stop_entry(make_bars(o, h, l, c), ll, sl, valid, K, "tp", 2.0)
    # entry=1.0010, stop=0.9990, low 0.9985<=stop -> -1R (proves entry=open not level)
    approx(r[0], -1.0 - COST_R)


def test_stopentry_no_trigger():
    o = [1.0, 0.999, 1.0]; h = [1.0, 0.9995, 1.0]; l = [1.0, 0.998, 1.0]; c = [1.0, 0.999, 1.0]
    ll = np.array([np.nan, 1.0000, np.nan])  # high never reaches 1.0000
    sl = np.full(3, np.nan); valid = np.array([False, True, False])
    r = H.simulate_stop_entry(make_bars(o, h, l, c), ll, sl, valid, K, "tp", 2.0)
    assert len(r) == 0


def _pull_bars(high, low, close, ef, es):
    n = len(high)
    return H.Bars(
        open=np.zeros(n), high=np.array(high, float), low=np.array(low, float),
        close=np.array(close, float), atr=np.full(n, 0.001),
        et_hour=np.full(n, 9, int), et_min=np.zeros(n, int), et_date=np.zeros(n, int),
        contig=np.array([False] + [True] * (n - 1)), don_high={}, don_low={},
        volfloor_ok=np.ones(n, bool), n=n,
        ema={2: np.array(ef, float), 3: np.array(es, float)},
    )


def test_pullback_long_signal():
    nan = np.nan
    bars = _pull_bars(
        high=[1.0, 1.0, 1.0, 1.0020, 1.0020, 1.0020],
        low=[1.0, 1.0, 1.0, 1.0012, 1.0005, 1.0012],   # only t=4 dips to/below ef
        close=[1.0, 1.0, 1.0, 1.0015, 1.0015, 1.0008],
        ef=[nan, nan, 1.0010, 1.0010, 1.0010, 1.0010],
        es=[nan, nan, nan, 1.0000, 1.0000, 1.0000],    # ef>es => uptrend at t>=3
    )
    ls, ss = H.build_signals(bars, "pullback", (2, 3), None, False)
    assert ls[4] and not ls[3] and ss.sum() == 0, (ls.tolist(), ss.tolist())


def test_pullback_short_signal():
    nan = np.nan
    bars = _pull_bars(
        high=[1.0, 1.0, 1.0, 0.9990, 0.9995, 0.9990],
        low=[1.0, 1.0, 1.0, 0.9980, 0.9980, 0.9980],
        close=[1.0, 1.0, 1.0, 0.9985, 0.9985, 0.9985],
        ef=[nan, nan, 0.9990, 0.9990, 0.9990, 0.9990],
        es=[nan, nan, nan, 1.0000, 1.0000, 1.0000],    # ef<es => downtrend
    )
    ls, ss = H.build_signals(bars, "pullback", (2, 3), None, False)
    assert ss[4] and ls.sum() == 0, (ls.tolist(), ss.tolist())


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for fn in fns:
        try:
            fn(); print(f"PASS {fn.__name__}"); passed += 1
        except AssertionError as ex:
            print(f"FAIL {fn.__name__}: {ex}")
        except Exception as ex:
            print(f"ERROR {fn.__name__}: {type(ex).__name__}: {ex}")
    print(f"\n{passed}/{len(fns)} passed")
