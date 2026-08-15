import pandas as pd
import window_match

def _frame(dates):
    ts = pd.to_datetime(dates)
    return pd.DataFrame({"exit_ts": ts, "exit_date": ts.normalize(),
                         "net_pnl_usd": 1.0, "net_pnl_pct": 0.001})

def test_clips_baseline_to_proto_span():
    baseline = _frame(["2022-01-03","2023-06-01","2024-06-01","2025-06-01","2026-05-01"])
    proto    = _frame(["2024-07-01","2025-12-01"])
    clipped, span = window_match.match(baseline, proto)
    assert list(clipped["exit_ts"].dt.year) == [2025]       # only 2025-06-01 falls inside
    assert span["proto_n"] == 2
    assert span["baseline_in_window_n"] == 1
    assert span["start"] == pd.Timestamp("2024-07-01")
    assert span["end"] == pd.Timestamp("2025-12-01")
