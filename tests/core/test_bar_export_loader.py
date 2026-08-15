"""Tests for core/bar_export_loader.py (BAR EXPORT v0.1 producer)."""
import pandas as pd
import pytest

from bar_export_loader import decode_bar_signal


def test_decode_bar_signal_pipe():
    enc = decode_bar_signal("1772409600000|156.64|156.806|156.572|156.574|3915")
    assert enc["epoch_ms"] == 1772409600000.0
    assert enc["o"] == 156.64
    assert enc["h"] == 156.806
    assert enc["l"] == 156.572
    assert enc["c"] == 156.574
    assert enc["v"] == 3915.0


def test_decode_bar_signal_legacy_comment():
    enc = decode_bar_signal("BAR|o=1.25|h=1.26|l=1.24|c=1.255|v=100")
    assert "epoch_ms" not in enc
    assert enc["o"] == 1.25
    assert enc["c"] == 1.255
    assert enc["v"] == 100.0


def test_decode_bar_signal_rejects_garbage():
    with pytest.raises(ValueError):
        decode_bar_signal("not a bar signal")


from bar_export_loader import parse_bar_export


def _make_tv_csv(path, price_col, rows):
    """rows: list of (trade_num, type, date_and_time, signal, price)."""
    df = pd.DataFrame(rows, columns=["Trade #", "Type", "Date and time", "Signal", price_col])
    df.to_csv(path, index=False, encoding="utf-8-sig")
    return path


def test_parse_bar_export_single(tmp_path):
    rows = [
        (1, "Entry long", "2026-03-02 00:00", "1772409600000|156.64|156.806|156.572|156.574|3915", 156.574),
        (2, "Entry long", "2026-03-02 00:15", "1772410500000|156.57|156.60|156.50|156.58|2000", 156.58),
    ]
    p = _make_tv_csv(tmp_path / "USDJPY_M15_pep.csv", "Price JPY", rows)
    df = parse_bar_export(p, symbol="USDJPY")
    assert list(df.columns) == ["time", "open", "high", "low", "close", "volume"]
    assert len(df) == 2
    assert df.iloc[0]["close"] == 156.574
    assert str(df.iloc[0]["time"]) == "2026-03-02 00:00:00+00:00"  # epoch_ms -> UTC bar-open


def test_parse_bar_export_rejects_price_mismatch(tmp_path):
    rows = [
        (1, "Entry long", "2026-03-02 00:00", "1772409600000|156.64|156.806|156.572|156.574|3915", 999.0),
    ]
    p = _make_tv_csv(tmp_path / "USDJPY_M15_pep.csv", "Price JPY", rows)
    with pytest.raises(ValueError, match="Cross-check fail"):
        parse_bar_export(p, symbol="USDJPY")


def test_parse_bar_export_unknown_symbol(tmp_path):
    rows = [(1, "Entry long", "2026-03-02 00:00", "1772409600000|1|1|1|1|1", 1.0)]
    p = _make_tv_csv(tmp_path / "ZZZ_M15_pep.csv", "Price USD", rows)
    with pytest.raises(ValueError, match="price column"):
        parse_bar_export(p, symbol="ZZZ")


from bar_export_loader import write_bar_data


def test_parse_bar_export_multipage_dedup(tmp_path):
    rows_a = [
        (1, "Entry long", "2026-03-02 00:00", "1772409600000|156.64|156.806|156.572|156.574|3915", 156.574),
        (2, "Entry long", "2026-03-02 00:15", "1772410500000|156.57|156.60|156.50|156.58|2000", 156.58),
    ]
    rows_b = [  # page B re-exports the 00:15 bar (different close) and adds 00:30
        (1, "Entry long", "2026-03-02 00:15", "1772410500000|156.57|156.60|156.50|156.99|2222", 156.99),
        (2, "Entry long", "2026-03-02 00:30", "1772411400000|156.99|157.00|156.90|156.95|1500", 156.95),
    ]
    pa = _make_tv_csv(tmp_path / "pageA.csv", "Price JPY", rows_a)
    pb = _make_tv_csv(tmp_path / "pageB.csv", "Price JPY", rows_b)
    df = parse_bar_export([pa, pb], symbol="USDJPY")
    assert len(df) == 3  # 00:00, 00:15 (deduped), 00:30
    bar_0015 = df[df["time"] == pd.Timestamp("2026-03-02 00:15", tz="UTC")]
    assert bar_0015.iloc[0]["close"] == 156.99  # keep='last' -> page B


def test_write_bar_data_and_feed_loader_round_trip(tmp_path):
    rows = [
        (1, "Entry long", "2026-03-02 00:00", "1772409600000|156.64|156.806|156.572|156.574|3915", 156.574),
        (2, "Entry long", "2026-03-02 00:15", "1772410500000|156.57|156.60|156.50|156.58|2000", 156.58),
    ]
    p = _make_tv_csv(tmp_path / "USDJPY_M15_pep.csv", "Price JPY", rows)
    df = parse_bar_export(p, symbol="USDJPY")
    out = write_bar_data(df, symbol="USDJPY", out_dir=tmp_path)
    assert out.name == "USDJPY_M15.csv"

    # Header is ISO-8601 'Z'; load through the unchanged sweep consumer.
    written = out.read_text(encoding="utf-8").splitlines()
    assert written[0] == "time,open,high,low,close,volume"
    assert written[1].startswith("2026-03-02T00:00:00Z,")

    import pandas as pd

    df = pd.read_csv(out)
    assert list(df.columns) == ["time", "open", "high", "low", "close", "volume"]
    assert len(df) == 2
    assert df.loc[0, "close"] == 156.574


# ============================================================================
# BAR EXPORT v0.2 — appended instrument + per-bar metadata (full-capture)
# ============================================================================
from bar_export_loader import decode_bar_meta, parse_bar_export_with_meta, write_bar_meta

# epoch|O|H|L|C|V | time_close|dow|sess | ticker|type|qCcy|bCcy|mintick|pointval|tz|tf
V2_SIGNAL = (
    "1772409600000|156.64|156.806|156.572|156.574|3915"
    "|1772410499999|2|M"
    "|PEPPERSTONE:USDJPY|forex|JPY|USD|0.001|1000|America/New_York|15"
)
V1_SIGNAL = "1772409600000|156.64|156.806|156.572|156.574|3915"


def test_decode_bar_signal_v2_prefix_is_backward_compatible():
    """A v0.2 row still decodes to the exact same 6 numeric OHLCV keys."""
    v1 = decode_bar_signal(V1_SIGNAL)
    v2 = decode_bar_signal(V2_SIGNAL)
    assert v2 == v1  # appended metadata must not perturb the OHLCV decode


def test_decode_bar_meta_v2_returns_instrument_and_bar_fields():
    meta = decode_bar_meta(V2_SIGNAL)
    assert meta["ticker"] == "PEPPERSTONE:USDJPY"
    assert meta["type"] == "forex"
    assert meta["quote_currency"] == "JPY"
    assert meta["base_currency"] == "USD"
    assert meta["mintick"] == 0.001
    assert meta["pointvalue"] == 1000.0
    assert meta["timezone"] == "America/New_York"
    assert meta["timeframe"] == "15"
    assert meta["_bar"] == {"time_close_ms": 1772410499999, "dayofweek": 2, "session": "M"}


def test_decode_bar_meta_v1_returns_none():
    assert decode_bar_meta(V1_SIGNAL) is None


def test_decode_bar_meta_empty_base_currency_allowed():
    """Index/CFD symbols have no base currency — the empty field must parse."""
    sig = (
        "1772409600000|1|1|1|1|1|1772410499999|3|M"
        "|PEPPERSTONE:NAS100|index|USD||0.1|1|America/New_York|15"
    )
    meta = decode_bar_meta(sig)
    assert meta["base_currency"] == ""
    assert meta["type"] == "index"
    assert meta["pointvalue"] == 1.0


def test_decode_bar_signal_rejects_malformed_v2_metadata():
    """Drift detector: a v0.2-shaped row with a bad session flag is rejected,
    not silently truncated to its OHLCV prefix."""
    bad = V2_SIGNAL.replace("|2|M|", "|2|BOGUS|")
    with pytest.raises(ValueError):
        decode_bar_signal(bad)


def _v2_row(trade_num, signal, price):
    return (trade_num, "Entry long", "2026-03-02 00:00", signal, price)


def test_parse_bar_export_v2_canonical_output_identical_to_v1(tmp_path):
    """Full-capture must NOT churn the canonical CSV: a v0.2 export and a v0.1
    export of the same bars produce byte-identical bar_data output."""
    v1_rows = [_v2_row(1, V1_SIGNAL, 156.574)]
    v2_rows = [_v2_row(1, V2_SIGNAL, 156.574)]
    p1 = _make_tv_csv(tmp_path / "v1_USDJPY_M15_pep.csv", "Price JPY", v1_rows)
    p2 = _make_tv_csv(tmp_path / "v2_USDJPY_M15_pep.csv", "Price JPY", v2_rows)

    df1 = parse_bar_export(p1, symbol="USDJPY")
    df2 = parse_bar_export(p2, symbol="USDJPY")
    pd.testing.assert_frame_equal(df1, df2)

    o1 = write_bar_data(df1, symbol="USDJPY", out_dir=tmp_path / "a")
    o2 = write_bar_data(df2, symbol="USDJPY", out_dir=tmp_path / "b")
    assert o1.read_bytes() == o2.read_bytes()


def test_parse_bar_export_with_meta_returns_constants_no_per_bar(tmp_path):
    rows = [_v2_row(1, V2_SIGNAL, 156.574)]
    p = _make_tv_csv(tmp_path / "USDJPY_M15_pep.csv", "Price JPY", rows)
    df, meta = parse_bar_export_with_meta(p, symbol="USDJPY")
    assert list(df.columns) == ["time", "open", "high", "low", "close", "volume"]
    assert meta["pointvalue"] == 1000.0
    assert meta["timezone"] == "America/New_York"
    assert "_bar" not in meta  # file-level meta carries instrument constants only


def test_parse_bar_export_with_meta_is_none_for_v1(tmp_path):
    rows = [_v2_row(1, V1_SIGNAL, 156.574)]
    p = _make_tv_csv(tmp_path / "USDJPY_M15_pep.csv", "Price JPY", rows)
    _, meta = parse_bar_export_with_meta(p, symbol="USDJPY")
    assert meta is None


def test_parse_bar_export_rejects_instrument_meta_drift(tmp_path):
    """Two rows of one export disagreeing on instrument constants = format
    drift = hard fail (the v0.2 extension of the existing drift detector)."""
    drifted = V2_SIGNAL.replace("|1000|", "|9999|")  # pointvalue changed mid-file
    rows = [
        _v2_row(1, V2_SIGNAL, 156.574),
        (2, "Entry long", "2026-03-02 00:15",
         "1772410500000|156.57|156.60|156.50|156.58|2000|1772411399999|2|M"
         "|PEPPERSTONE:USDJPY|forex|JPY|USD|0.001|9999|America/New_York|15", 156.58),
    ]
    p = _make_tv_csv(tmp_path / "USDJPY_M15_pep.csv", "Price JPY", rows)
    with pytest.raises(ValueError, match="meta drift"):
        parse_bar_export_with_meta(p, symbol="USDJPY")


def test_write_bar_meta_writes_sidecar(tmp_path):
    meta = decode_bar_meta(V2_SIGNAL)
    const = {k: v for k, v in meta.items() if not k.startswith("_")}
    out = write_bar_meta(const, symbol="USDJPY", out_dir=tmp_path)
    assert out.name == "USDJPY_M15.meta.json"
    import json
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["schema"] == "BAR_EXPORT_meta_v0.2"
    assert payload["symbol"] == "USDJPY"
    assert payload["pointvalue"] == 1000.0
    assert "_bar" not in payload


def test_write_bar_meta_none_writes_nothing(tmp_path):
    assert write_bar_meta(None, symbol="USDJPY", out_dir=tmp_path) is None
    assert not (tmp_path / "USDJPY_M15.meta.json").exists()
