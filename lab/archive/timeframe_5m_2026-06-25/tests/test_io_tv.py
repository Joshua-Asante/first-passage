import pandas as pd
import io_tv

_HEADER = "Trade #,Type,Date and time,Net P&L USD,Net P&L %\n"

def _make_csv(tmp_path, n_pairs=60):
    # n_pairs entry+exit rows = 2*n_pairs raw rows (>100 to clear min-rows floor)
    rows = []
    for i in range(1, n_pairs + 1):
        d = f"2025-01-{(i % 27) + 1:02d} 10:00"
        rows.append(f"{i},Entry long,{d},{i*1.0},{i*0.001}")
        rows.append(f"{i},Exit long,{d},{i*1.0},{i*0.001}")
    p = tmp_path / "x.csv"
    p.write_text(_HEADER + "\n".join(rows) + "\n", encoding="utf-8")
    return p

def test_load_exits_shape_and_count(tmp_path):
    p = _make_csv(tmp_path, n_pairs=60)
    out = io_tv.load_exits(p)
    assert list(out.columns) == ["exit_ts", "exit_date", "net_pnl_usd", "net_pnl_pct"]
    assert len(out) == 60                      # exit rows only
    assert out["exit_ts"].is_monotonic_increasing
    assert pd.api.types.is_datetime64_any_dtype(out["exit_ts"])
