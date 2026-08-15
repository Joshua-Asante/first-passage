import numpy as np
import pandas as pd
import portfolio_mc as pmc
import remc

def test_to_mc_trades_shape():
    exits = pd.DataFrame({
        "exit_ts": pd.to_datetime(["2025-01-02","2025-01-03"]),
        "exit_date": pd.to_datetime(["2025-01-02","2025-01-03"]),
        "net_pnl_usd": [100.0, -50.0],
        "net_pnl_pct": [0.05, -0.025],
    })
    out = remc.to_mc_trades(exits)
    assert list(out.columns) == ["exit_date", "pnl"]
    assert list(out["pnl"]) == [100.0, -50.0]

def test_aggregate_keys_and_values():
    fake = [{"outcomes": {"pass": 9000, "bust_daily": 100, "bust_static": 50},
             "max_dds": list(np.linspace(0.0, 0.05, 1000))} for _ in range(3)]
    agg = remc.aggregate(fake)
    assert set(agg) == {"pass_rate", "bust_rate", "p99_dd"}
    assert abs(agg["pass_rate"] - 0.9) < 1e-9
    assert abs(agg["bust_rate"] - 0.015) < 1e-9     # (100+50)/10000

def _write_tv_csv(path, rows):
    # rows: list of (date_str, net_pnl_usd, net_pnl_pct); each -> Entry+Exit pair
    header = "Trade #,Type,Date and time,Net P&L USD,Net P&L %\n"
    lines = []
    for i, (d, usd, pct) in enumerate(rows, start=1):
        lines.append(f"{i},Entry long,{d},{usd},{pct}")
        lines.append(f"{i},Exit long,{d},{usd},{pct}")
    path.write_text(header + "\n".join(lines) + "\n", encoding="utf-8")

def test_run_5m_remc_smoke(tmp_path, monkeypatch):
    # Reduce sims so the real build_daily_panel -> build_week_blocks -> _run_seeds
    # chain runs fast. _run_seeds and aggregate both read pmc.SIMS_PER_SEED.
    monkeypatch.setattr(pmc, "SIMS_PER_SEED", 50)
    bdays = pd.bdate_range("2025-01-06", periods=60)  # starts on a Monday
    csvs = {}
    for s in ("guardian", "striker", "aegis", "striker_nas100"):
        rows = [(bdays[i].strftime("%Y-%m-%d %H:%M"),
                 (100.0 if i % 3 else -200.0),
                 (0.05 if i % 3 else -0.10)) for i in range(60)]
        p = tmp_path / f"{s}.csv"
        _write_tv_csv(p, rows)
        csvs[s] = p
    out = remc.run_5m_remc(csvs)
    for k in ("pass_rate", "bust_rate", "p99_dd", "spans", "fell_back", "n_blocks"):
        assert k in out
    assert 0.0 <= out["pass_rate"] <= 1.0
    assert 0.0 <= out["bust_rate"] <= 1.0
    assert out["n_blocks"] >= 1
    assert set(out["spans"].keys()) == {"guardian", "striker", "aegis", "striker_nas100"}

def test_run_5m_remc_rejects_empty_stream(tmp_path):
    # A file with >=100 raw rows but NO Exit rows -> 0 trades -> named ValueError,
    # raised before any simulation runs.
    import pytest
    good_rows = [("2025-01-%02d 10:00" % ((i % 27) + 1), 100.0, 0.05) for i in range(60)]
    bad_path = tmp_path / "empty.csv"
    header = "Trade #,Type,Date and time,Net P&L USD,Net P&L %\n"
    # 60 Entry-only pairs duplicated to clear the 100 raw-row floor, zero Exit rows
    lines = [f"{i},Entry long,2025-02-03 10:00,100.0,0.05" for i in range(1, 121)]
    bad_path.write_text(header + "\n".join(lines) + "\n", encoding="utf-8")
    csvs = {"guardian": bad_path}
    with pytest.raises(ValueError, match="0 exit rows"):
        remc.run_5m_remc(csvs)
