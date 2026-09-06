"""Synthetic expected-value tests for opt-in strict BAR EXPORT v0.2 validation."""
from __future__ import annotations

import hashlib
import importlib.util
import os
import sys
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
_SPEC = importlib.util.spec_from_file_location(
    "validate_bar_export_v2", REPO / "scripts" / "validate_bar_export_v2.py"
)
mod = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
sys.modules["validate_bar_export_v2"] = mod
_SPEC.loader.exec_module(mod)

ExpectedBarExportV2 = mod.ExpectedBarExportV2
BarExportValidationReceipt = mod.BarExportValidationReceipt
validate_bar_export_v2 = mod.validate_bar_export_v2
receipt_to_json_bytes = mod.receipt_to_json_bytes
main = mod.main

E0 = 1_700_000_000_000
E1 = E0 + 15 * 60_000
E2 = E1 + 15 * 60_000
TF_MS = 15 * 60_000

META = {
    "ticker": "TEST:AABB",
    "type": "forex",
    "quote_currency": "USD",
    "base_currency": "AAA",
    "mintick": "0.001",
    "pointvalue": "1000",
    "timezone": "UTC",
    "timeframe": "15",
}


def _sig(
    epoch: int,
    o: str,
    h: str,
    l: str,
    c: str,
    v: int,
    *,
    close_ms: int,
    dow: str = "2",
    sess: str = "M",
    mintick: str | None = None,
    pointvalue: str | None = None,
    base: str | None = None,
    timeframe: str | None = None,
    ticker: str | None = None,
    typ: str | None = None,
    quote: str | None = None,
    tz: str | None = None,
) -> str:
    return "|".join(
        [
            str(epoch),
            o,
            h,
            l,
            c,
            str(v),
            str(close_ms),
            dow,
            sess,
            ticker if ticker is not None else META["ticker"],
            typ if typ is not None else META["type"],
            quote if quote is not None else META["quote_currency"],
            META["base_currency"] if base is None else base,
            mintick if mintick is not None else META["mintick"],
            pointvalue if pointvalue is not None else META["pointvalue"],
            tz if tz is not None else META["timezone"],
            timeframe if timeframe is not None else META["timeframe"],
        ]
    )


def _csv(rows: list[tuple], *, price_col: str = "Price USD") -> str:
    lines = [f"Trade #,Type,Date and time,Signal,{price_col}"]
    for trade, typ, when, signal, price in rows:
        lines.append(f"{trade},{typ},{when},{signal},{price}")
    return "\n".join(lines) + "\n"


def _write(path: Path, text: str, *, bom: bool = False) -> bytes:
    data = text.encode("utf-8")
    if bom:
        data = b"\xef\xbb\xbf" + data
    path.write_bytes(data)
    return data


def _dt(ms: int) -> datetime:
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc)


def _expected(**overrides) -> ExpectedBarExportV2:
    base = dict(
        price_column="Price USD",
        ticker=META["ticker"],
        instrument_type=META["type"],
        quote_currency=META["quote_currency"],
        base_currency=META["base_currency"],
        mintick=Decimal(META["mintick"]),
        pointvalue=Decimal(META["pointvalue"]),
        timezone=META["timezone"],
        timeframe_minutes=15,
        expected_unique_bars=2,
        expected_first_open_utc=_dt(E0),
        expected_last_open_utc=_dt(E1),
    )
    base.update(overrides)
    return ExpectedBarExportV2(**base)


def _row(
    trade: int,
    epoch: int,
    o: str,
    h: str,
    l: str,
    c: str,
    v: int,
    *,
    close_ms: int | None = None,
    **sig_kw,
) -> tuple:
    close = epoch + TF_MS - 1 if close_ms is None else close_ms
    return (
        trade,
        "Entry long",
        "2023-11-14 22:13",
        _sig(epoch, o, h, l, c, v, close_ms=close, **sig_kw),
        c,
    )


def test_two_pages_identical_overlap_receipt(tmp_path: Path):
    page_a = _csv(
        [
            _row(1, E0, "156.64", "156.806", "156.572", "156.574", 3915),
            _row(2, E1, "156.57", "156.60", "156.50", "156.580", 2000),
        ]
    )
    page_b = _csv(
        [
            _row(1, E1, "156.57", "156.60", "156.50", "156.580", 2000),
            _row(2, E2, "156.99", "157.00", "156.90", "156.950", 1500),
        ]
    )
    pa = tmp_path / "a.csv"
    pb = tmp_path / "b.csv"
    ba = _write(pa, page_a)
    bb = _write(pb, page_b, bom=True)

    exp = _expected(expected_unique_bars=3, expected_last_open_utc=_dt(E2))
    receipt = validate_bar_export_v2([pa, pb], expected=exp)
    assert isinstance(receipt, BarExportValidationReceipt)
    assert receipt.schema == "bar_export_v2_validation_v1"
    assert receipt.status == "PASS"
    assert receipt.page_count == 2
    assert receipt.input_sha256 == (
        hashlib.sha256(ba).hexdigest(),
        hashlib.sha256(bb).hexdigest(),
    )
    assert receipt.entry_row_count == 4
    assert receipt.unique_bar_count == 3
    assert receipt.identical_cross_page_overlap_count == 1
    assert receipt.first_open_utc == _dt(E0)
    assert receipt.last_open_utc == _dt(E2)
    assert dict(receipt.metadata) == META
    with pytest.raises(TypeError):
        receipt.metadata["ticker"] = "MUTATE"  # type: ignore[index]
    assert validate_bar_export_v2([pa, pb], expected=exp) == receipt


def test_rejects_bad_blank_v1_mixed_signal_and_headers(tmp_path: Path):
    p = tmp_path / "good.csv"
    _write(p, _csv([_row(1, E0, "1", "1", "1", "1", 1)]))
    validate_bar_export_v2(
        [p], expected=_expected(expected_unique_bars=1, expected_last_open_utc=_dt(E0))
    )

    for i, text in enumerate(
        [
            _csv([(1, "Entry long", "t", "not-a-signal", "1")]),
            _csv([(1, "Entry long", "t", "", "1")]),
            _csv([(1, "Entry long", "t", f"{E0}|1|1|1|1|1", "1")]),
        ]
    ):
        path = tmp_path / f"bad{i}.csv"
        _write(path, text)
        with pytest.raises(ValueError):
            validate_bar_export_v2(
                [path],
                expected=_expected(expected_unique_bars=1, expected_last_open_utc=_dt(E0)),
            )

    text = "\n".join(
        [
            "Trade #,Type,Date and time,Signal,Comment,Price USD",
            f"1,Entry long,t,,{_sig(E0, '1', '1', '1', '1', 1, close_ms=E0 + TF_MS - 1)},1",
            "",
        ]
    )
    _write(tmp_path / "nofallback.csv", text)
    with pytest.raises(ValueError):
        validate_bar_export_v2(
            [tmp_path / "nofallback.csv"],
            expected=_expected(expected_unique_bars=1, expected_last_open_utc=_dt(E0)),
        )

    _write(
        tmp_path / "duph.csv",
        "Trade #,Type,Type,Date and time,Signal,Price USD\n"
        f"1,Entry long,x,t,{_sig(E0, '1', '1', '1', '1', 1, close_ms=E0 + TF_MS - 1)},1\n",
    )
    with pytest.raises(ValueError, match="(?i)duplicate|header"):
        validate_bar_export_v2(
            [tmp_path / "duph.csv"],
            expected=_expected(expected_unique_bars=1, expected_last_open_utc=_dt(E0)),
        )

    _write(
        tmp_path / "wide.csv",
        "Trade #,Type,Date and time,Signal,Price USD\n1,Entry long,t,sig,1,EXTRA\n",
    )
    with pytest.raises(ValueError, match="(?i)width|column|field"):
        validate_bar_export_v2(
            [tmp_path / "wide.csv"],
            expected=_expected(expected_unique_bars=1, expected_last_open_utc=_dt(E0)),
        )

    _write(tmp_path / "empty.csv", "Trade #,Type,Date and time,Signal,Price USD\n")
    with pytest.raises(ValueError):
        validate_bar_export_v2(
            [tmp_path / "empty.csv"],
            expected=_expected(expected_unique_bars=1, expected_last_open_utc=_dt(E0)),
        )
    with pytest.raises(ValueError):
        validate_bar_export_v2(
            [], expected=_expected(expected_unique_bars=1, expected_last_open_utc=_dt(E0))
        )


def test_trade_id_and_epoch_ordering(tmp_path: Path):
    r0 = _row(1, E0, "156.64", "156.806", "156.572", "156.574", 3915)
    r1 = _row(2, E1, "156.57", "156.60", "156.50", "156.580", 2000)
    _write(tmp_path / "rev.csv", _csv([r1, r0]))
    validate_bar_export_v2([tmp_path / "rev.csv"], expected=_expected())

    bad = [
        _row(1, E1, "156.57", "156.60", "156.50", "156.580", 2000),
        _row(2, E0, "156.64", "156.806", "156.572", "156.574", 3915),
    ]
    _write(tmp_path / "desc.csv", _csv(bad))
    with pytest.raises(ValueError, match="(?i)epoch|increasing|order"):
        validate_bar_export_v2([tmp_path / "desc.csv"], expected=_expected())

    _write(
        tmp_path / "dupid.csv",
        _csv([r0, _row(1, E1, "156.57", "156.60", "156.50", "156.580", 2000)]),
    )
    with pytest.raises(ValueError, match="(?i)trade|duplicate"):
        validate_bar_export_v2([tmp_path / "dupid.csv"], expected=_expected())

    _write(
        tmp_path / "badid.csv",
        _csv(
            [
                (
                    "-1",
                    "Entry long",
                    "t",
                    _sig(E0, "1", "1", "1", "1", 1, close_ms=E0 + TF_MS - 1),
                    "1",
                )
            ]
        ),
    )
    with pytest.raises(ValueError):
        validate_bar_export_v2(
            [tmp_path / "badid.csv"],
            expected=_expected(expected_unique_bars=1, expected_last_open_utc=_dt(E0)),
        )


def test_expected_binding_and_metadata_drift(tmp_path: Path):
    p = tmp_path / "p.csv"
    _write(
        p,
        _csv(
            [
                _row(1, E0, "156.64", "156.806", "156.572", "156.574", 3915),
                _row(2, E1, "156.57", "156.60", "156.50", "156.580", 2000),
            ]
        ),
    )
    validate_bar_export_v2([p], expected=_expected())

    for kwargs in [
        {"ticker": "OTHER:TICK"},
        {"instrument_type": "index"},
        {"quote_currency": "JPY"},
        {"base_currency": "ZZZ"},
        {"mintick": Decimal("0.01")},
        {"pointvalue": Decimal("1")},
        {"timezone": "America/New_York"},
        {"timeframe_minutes": 5},
        {"price_column": "Price JPY"},
    ]:
        with pytest.raises(ValueError):
            validate_bar_export_v2([p], expected=_expected(**kwargs))

    with pytest.raises(ValueError):
        validate_bar_export_v2([p], expected=_expected(mintick=Decimal("0")))
    with pytest.raises(ValueError):
        validate_bar_export_v2([p], expected=_expected(timeframe_minutes=True))  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        validate_bar_export_v2(
            [p],
            expected=_expected(expected_first_open_utc=datetime(2023, 11, 14, 22, 13)),
        )

    _write(
        tmp_path / "drift.csv",
        _csv(
            [
                _row(1, E0, "156.64", "156.806", "156.572", "156.574", 3915),
                _row(2, E1, "156.57", "156.60", "156.50", "156.580", 2000, ticker="TEST:DRIFT"),
            ]
        ),
    )
    with pytest.raises(ValueError, match="(?i)meta|ticker|drift|identical"):
        validate_bar_export_v2([tmp_path / "drift.csv"], expected=_expected())


def test_decimal_precision_and_geometry(tmp_path: Path):
    precise = "156.5740123456789012345"
    p = tmp_path / "precise.csv"
    _write(p, _csv([_row(1, E0, "156.64", "156.806", "156.572", precise, 10)]))
    validate_bar_export_v2(
        [p], expected=_expected(expected_unique_bars=1, expected_last_open_utc=_dt(E0))
    )

    bad_price = precise[:-1] + ("0" if precise[-1] != "0" else "1")
    _write(
        tmp_path / "mismatch.csv",
        _csv(
            [
                (
                    1,
                    "Entry long",
                    "t",
                    _sig(E0, "156.64", "156.806", "156.572", precise, 10, close_ms=E0 + TF_MS - 1),
                    bad_price,
                )
            ]
        ),
    )
    with pytest.raises(ValueError, match="(?i)price|close|entry"):
        validate_bar_export_v2(
            [tmp_path / "mismatch.csv"],
            expected=_expected(expected_unique_bars=1, expected_last_open_utc=_dt(E0)),
        )

    p3 = tmp_path / "trail.csv"
    _write(p3, _csv([_row(1, E0, "1.0", "1.0", "1.0", "1.0", 1, mintick="0.00100")]))
    rec = validate_bar_export_v2(
        [p3],
        expected=_expected(
            mintick=Decimal("0.001"),
            expected_unique_bars=1,
            expected_last_open_utc=_dt(E0),
        ),
    )
    assert rec.metadata["mintick"] == "0.00100"

    _write(tmp_path / "ohlc.csv", _csv([_row(1, E0, "10", "9", "8", "10", 1)]))
    with pytest.raises(ValueError, match="(?i)ohlc|geometry|high|low"):
        validate_bar_export_v2(
            [tmp_path / "ohlc.csv"],
            expected=_expected(expected_unique_bars=1, expected_last_open_utc=_dt(E0)),
        )

    getcontext().prec = 5
    try:
        validate_bar_export_v2(
            [p], expected=_expected(expected_unique_bars=1, expected_last_open_utc=_dt(E0))
        )
    finally:
        getcontext().prec = 28


def test_duration_bounds_and_overlap_rules(tmp_path: Path):
    def one(close_ms: int, path: Path):
        _write(path, _csv([_row(1, E0, "1", "1", "1", "1", 1, close_ms=close_ms)]))
        return validate_bar_export_v2(
            [path],
            expected=_expected(expected_unique_bars=1, expected_last_open_utc=_dt(E0)),
        )

    one(E0 + TF_MS, tmp_path / "full.csv")
    one(E0 + TF_MS - 1, tmp_path / "short1.csv")
    one(E0 + 1, tmp_path / "session.csv")
    with pytest.raises(ValueError):
        one(E0, tmp_path / "atopen.csv")
    with pytest.raises(ValueError):
        one(E0 + TF_MS + 1, tmp_path / "beyond.csv")

    _write(
        tmp_path / "withindup.csv",
        _csv([_row(1, E0, "1", "1", "1", "1", 1), _row(2, E0, "1", "1", "1", "1", 1)]),
    )
    with pytest.raises(ValueError, match="(?i)duplicate|timestamp|epoch"):
        validate_bar_export_v2(
            [tmp_path / "withindup.csv"],
            expected=_expected(expected_unique_bars=1, expected_last_open_utc=_dt(E0)),
        )

    a = tmp_path / "oa.csv"
    b = tmp_path / "ob.csv"
    _write(a, _csv([_row(1, E0, "156.64", "156.806", "156.572", "156.574", 3915)]))
    _write(b, _csv([_row(9, E0, "156.64", "156.806", "156.572", "156.574", 3915)]))
    validate_bar_export_v2(
        [a, b], expected=_expected(expected_unique_bars=1, expected_last_open_utc=_dt(E0))
    )

    _write(b, _csv([_row(9, E0, "156.64", "157.000", "156.572", "156.999", 3915)]))
    with pytest.raises(ValueError, match="(?i)overlap|conflict|disagree"):
        validate_bar_export_v2(
            [a, b], expected=_expected(expected_unique_bars=1, expected_last_open_utc=_dt(E0))
        )

    _write(
        b,
        _csv(
            [
                _row(
                    9,
                    E0,
                    "156.64",
                    "156.806",
                    "156.572",
                    "156.574",
                    3915,
                    close_ms=E0 + TF_MS - 2,
                )
            ]
        ),
    )
    with pytest.raises(ValueError, match="(?i)overlap|conflict|disagree|close"):
        validate_bar_export_v2(
            [a, b], expected=_expected(expected_unique_bars=1, expected_last_open_utc=_dt(E0))
        )

    c = tmp_path / "oc.csv"
    simple = _row(1, E0, "1", "1", "1", "1", 1)
    for path in (a, b, c):
        _write(path, _csv([simple]))
    rec = validate_bar_export_v2(
        [a, b, c], expected=_expected(expected_unique_bars=1, expected_last_open_utc=_dt(E0))
    )
    assert rec.entry_row_count == 3
    assert rec.unique_bar_count == 1
    assert rec.identical_cross_page_overlap_count == 2


def test_endpoints_and_non_utc_fail(tmp_path: Path):
    p = tmp_path / "p.csv"
    _write(
        p,
        _csv(
            [
                _row(1, E0, "156.64", "156.806", "156.572", "156.574", 3915),
                _row(2, E1, "156.57", "156.60", "156.50", "156.580", 2000),
            ]
        ),
    )
    with pytest.raises(ValueError):
        validate_bar_export_v2([p], expected=_expected(expected_unique_bars=99))
    with pytest.raises(ValueError):
        validate_bar_export_v2([p], expected=_expected(expected_first_open_utc=_dt(E1)))
    with pytest.raises(ValueError):
        validate_bar_export_v2([p], expected=_expected(expected_last_open_utc=_dt(E0)))


def test_cli_receipt_alias_and_duplicate_inputs(tmp_path: Path):
    p1 = tmp_path / "p1.csv"
    p2 = tmp_path / "p2.csv"
    _write(
        p1,
        _csv(
            [
                _row(1, E0, "156.64", "156.806", "156.572", "156.574", 3915),
                _row(2, E1, "156.57", "156.60", "156.50", "156.580", 2000),
            ]
        ),
    )
    _write(
        p2,
        _csv(
            [
                _row(1, E1, "156.57", "156.60", "156.50", "156.580", 2000),
                _row(2, E2, "156.99", "157.00", "156.90", "156.950", 1500),
            ]
        ),
    )
    receipt_path = tmp_path / "receipt.json"
    receipt_path.write_text("OLD_RECEIPT_BYTES\n", encoding="utf-8")

    def base_args(receipt: Path) -> list[str]:
        return [
            "--in",
            str(p1),
            str(p2),
            "--price-column",
            "Price USD",
            "--expected-ticker",
            META["ticker"],
            "--expected-type",
            META["type"],
            "--expected-quote-currency",
            META["quote_currency"],
            "--expected-base-currency",
            META["base_currency"],
            "--expected-mintick",
            META["mintick"],
            "--expected-pointvalue",
            META["pointvalue"],
            "--expected-timeframe-minutes",
            "15",
            "--expected-timezone",
            META["timezone"],
            "--expected-unique-bars",
            "3",
            "--expected-first-open-utc",
            _dt(E0).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "--expected-last-open-utc",
            _dt(E2).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "--receipt",
            str(receipt),
        ]

    assert main(base_args(receipt_path)) == 0
    written = receipt_path.read_bytes()
    assert written.endswith(b"\n")
    exp = _expected(expected_unique_bars=3, expected_last_open_utc=_dt(E2))
    assert written == receipt_to_json_bytes(validate_bar_export_v2([p1, p2], expected=exp))

    bad = base_args(receipt_path)
    bad[bad.index("--expected-unique-bars") + 1] = "1"
    assert main(bad) == 2
    assert receipt_path.read_bytes() == written

    assert main(base_args(p1)) == 2
    assert b"Entry long" in p1.read_bytes()

    dup = ["--in", str(p1), str(p1), *base_args(tmp_path / "r2.json")[3:]]
    assert main(dup) == 2

    if hasattr(os, "symlink"):
        link = tmp_path / "link.csv"
        try:
            link.symlink_to(p1)
        except OSError:
            pytest.skip("symlink not permitted")
        link_args = ["--in", str(p1), str(link), *base_args(tmp_path / "r3.json")[3:]]
        assert main(link_args) == 2


def test_permissive_loader_regression_unchanged(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    sys.path.insert(0, str(REPO / "core"))
    import bar_export_loader as bel

    monkeypatch.setitem(bel.PRICE_COL_BY_INSTRUMENT, "SYNTH", "Price USD")

    page_a = _csv(
        [
            (1, "Entry long", "2023-11-14 22:13", "NOT_DECODABLE", "156.574"),
            _row(2, E1, "156.57", "156.60", "156.50", "156.580", 2000),
        ]
    )
    page_b = _csv(
        [
            _row(1, E1, "156.57", "156.60", "156.50", "156.999", 2222),
            _row(2, E2, "156.99", "157.00", "156.90", "156.950", 1500),
        ]
    )
    pa = tmp_path / "la.csv"
    pb = tmp_path / "lb.csv"
    _write(pa, page_a)
    _write(pb, page_b)

    df, _meta = bel.parse_bar_export_with_meta([pa, pb], symbol="SYNTH")
    assert len(df) == 2
    assert list(df["close"])[0] == 156.999
    assert list(df["close"])[1] == 156.950
