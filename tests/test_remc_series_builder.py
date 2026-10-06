"""Four-firm re-MC series builder — card §6 acceptance suite.

Card: docs/briefs/handoffs/2026-10-05-four-firm-remc-series-builder-card.md
(FROZEN 2026-10-05). Every input below is a *synthetic* TradingView trade-list
CSV written to ``tmp_path``; no private export, Pine source or CSV under
``core/data/`` is read, hashed or named. Every expected number is hand-computed
in this file from the card's arithmetic (§0.5 items 4-7).

Hand-copied cost law (core/firm_rules.py ``cost_per_side_usd``), so the expected
values below are independent of the module under test:
    Bulenox_100K 0.61 · Tradeify_Select_100K 0.91 · MFFU_Rapid_100K 0.95 ·
    BluSky_Premium_100K 0.95
"""
from __future__ import annotations

import copy
import csv
import json
from datetime import date
from pathlib import Path

import numpy as np
import pytest

from discovery.prop_survivor_scoring import paired_blocks_from_daily
from discovery.remc_series_builder import (
    DEFAULT_QUANTITY_SPEC,
    InputIdentityError,
    MODES,
    OutputPathError,
    TIERS,
    TRADE_LIST_COLUMNS,
    build_series,
    load_trade_table,
    main,
    parse_trade_list_csv,
    sha256_file,
)

EXPORT_TZ = "America/New_York"
REPO = Path(__file__).resolve().parents[1]
CPS = {
    "Bulenox_100K": 0.61,
    "Tradeify_Select_100K": 0.91,
    "MFFU_Rapid_100K": 0.95,
    "BluSky_Premium_100K": 0.95,
}


# ── synthetic trade-list writer ──────────────────────────────────────────


def _row(n, entry, exit_, qty, net, comm, ae):
    """One synthetic trade: (number, entry wall time, exit wall time, qty, net, commission, |AE|)."""
    return {"n": n, "entry": entry, "exit": exit_, "qty": qty, "net": net, "comm": comm, "ae": ae}


def _cells(row, kind, *, scale, blank):
    """Build one 17-cell TV row.

    ``scale`` multiplies the money columns so the Entry row deliberately carries
    different (wrong) values than the Exit row: TV puts trade-level values on the
    Exit row, so the parser must read the Exit cells, not the Entry ones.
    """
    values = {
        "Trade number": str(row["n"]),
        "Type": f"{kind} long",
        "Date and time": row["entry"] if kind == "entry" else row["exit"],
        "Signal": "synthetic",
        "Price USD": "1.0000",
        "Size (qty)": str(row["qty"]),
        "Size (value)": "0",
        "Net PnL USD": repr(row["net"] * scale),
        "Return %": "0",
        "Commission USD": repr(row["comm"] * scale),
        "Favorable excursion USD": "0",
        "Favorable excursion %": "0",
        "Adverse excursion USD": repr(row["ae"] * scale),
        "Adverse excursion %": "0",
        "Cumulative PnL USD": "0",
        "Cumulative PnL %": "0",
        "Duration (bars)": "3",
    }
    return ["" if column in blank else values[column] for column in TRADE_LIST_COLUMNS]


def write_csv(
    path,
    rows,
    *,
    bom=False,
    pairs=True,
    blank_exit_columns=(),
    header=None,
):
    """Write a synthetic trade list; ``pairs=False`` emits Entry rows only (unpaired)."""
    lines = [list(TRADE_LIST_COLUMNS) if header is None else header]
    for row in rows:
        lines.append(_cells(row, "entry", scale=7.0, blank=frozenset()))
        if pairs:
            lines.append(
                _cells(row, "exit", scale=1.0, blank=frozenset(blank_exit_columns))
            )
    payload = "\r\n".join(",".join(cell for cell in line) for line in lines) + "\r\n"
    blob = ("\ufeff" if bom else "") + payload
    Path(path).write_text(blob, encoding="utf-8", newline="")


def write_table(directory, key, rows, **kwargs):
    path = Path(directory) / f"{key[0]}__{key[1]}.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    write_csv(path, rows, **kwargs)
    return path, sha256_file(path)


def build(tmp_path, tables, *, export_tz=EXPORT_TZ, quantity_spec=None, tag="tables"):
    """Write + hash-verify + parse the synthetic tables, then build the series."""
    root = Path(tmp_path) / tag
    parsed = {}
    for key, rows in tables.items():
        path, digest = write_table(root, key, rows)
        parsed[key] = load_trade_table(path, digest, leg=key[0], export_tz=export_tz)
    return build_series(parsed, export_tz=export_tz, quantity_spec=quantity_spec)


# ── the standard six-table fixture ───────────────────────────────────────
# Window: every table first trades 2026-01-05 and last trades 2026-01-12, so the
# window is [2026-01-05, 2026-01-12] = six weekdays (Jan 10/11 are a weekend).
# Aegis is exported at a 1..8 ladder and rescaled per contract (8 normal / 3
# protected); every other leg is used as exported.

STANDARD = {
    ("aegis_6j", "normal"): [
        _row(1, "2026-01-05 09:35", "2026-01-05 10:20", 4, 100.0, 1.00, 25.0),
        _row(2, "2026-01-07 09:40", "2026-01-07 11:00", 2, -60.0, 0.50, 40.0),
        _row(3, "2026-01-12 10:00", "2026-01-12 10:30", 8, 160.0, 2.00, 10.0),
    ],
    ("dj30_mym_p250", "normal"): [
        _row(1, "2026-01-05 10:00", "2026-01-05 10:30", 1, 200.0, 2.00, 10.0),
        _row(2, "2026-01-06 09:35", "2026-01-06 10:00", 3, -90.0, 6.00, 30.0),
        _row(3, "2026-01-12 11:00", "2026-01-12 11:30", 2, 40.0, 4.00, 20.0),
    ],
    ("dj30_mym_p250", "protected"): [
        _row(1, "2026-01-05 09:35", "2026-01-05 10:00", 1, 30.0, 2.00, 4.0),
        _row(2, "2026-01-07 09:35", "2026-01-07 10:00", 1, 50.0, 2.00, 5.0),
        _row(3, "2026-01-12 10:00", "2026-01-12 10:45", 1, -20.0, 2.00, 15.0),
    ],
    ("vanguard_mgc", "normal"): [
        _row(1, "2026-01-05 09:35", "2026-01-05 10:00", 2, 80.0, 1.60, 8.0),
        _row(2, "2026-01-08 09:35", "2026-01-08 10:00", 2, 80.0, 1.60, 8.0),
        _row(3, "2026-01-12 09:40", "2026-01-12 10:10", 1, -25.0, 0.80, 12.0),
    ],
    ("orb_mnq_v7", "normal"): [
        _row(1, "2026-01-05 09:30", "2026-01-05 09:45", 1, -30.0, 1.00, 12.0),
        _row(2, "2026-01-08 10:00", "2026-01-08 10:30", 1, 45.0, 1.00, 9.0),
        _row(3, "2026-01-12 10:00", "2026-01-12 10:20", 1, 10.0, 1.00, 3.0),
    ],
    ("orb_mnq_v7", "protected"): [
        _row(1, "2026-01-05 10:00", "2026-01-05 10:30", 1, 5.0, 1.00, 2.0),
        _row(2, "2026-01-09 10:00", "2026-01-09 10:30", 1, 15.0, 1.00, 6.0),
        _row(3, "2026-01-12 10:05", "2026-01-12 10:40", 1, -8.0, 1.00, 7.0),
    ],
}

DATES = [
    date(2026, 1, 5),
    date(2026, 1, 6),
    date(2026, 1, 7),
    date(2026, 1, 8),
    date(2026, 1, 9),
    date(2026, 1, 12),
]

# Normal mode, all legs summed, after the Aegis rescale to 8 contracts
# (factors 8/4=2, 8/2=4, 8/8=1 — all exact in binary64):
#   01-05  aegis 200+2.00 · striker 200+2.00 · vanguard 80+1.60 · orb -30+1.00
#   01-06  striker -90+6.00
#   01-07  aegis -240+2.00
#   01-08  vanguard 80+1.60 · orb 45+1.00
#   01-09  (no normal trade)
#   01-12  aegis 160+2.00 · striker 40+4.00 · vanguard -25+0.80 · orb 10+1.00
NORMAL_GROSS = [456.60, -84.00, -238.00, 127.60, 0.0, 192.80]
NORMAL_SIDES = [24.0, 6.0, 16.0, 6.0, 0.0, 24.0]
NORMAL_AE = [80.00, 30.00, 160.00, 17.00, 0.00, 45.00]

# Protected mode: aegis rescaled to 3 (factors 0.75, 1.5, 0.375 — exact),
# striker and orb as exported, vanguard ZERO.
#   01-05  aegis 75+0.75 · striker 30+2.00 · orb 5+1.00
#   01-06  (none)
#   01-07  aegis -90+0.75 · striker 50+2.00
#   01-08  (none)
#   01-09  orb 15+1.00
#   01-12  aegis 60+0.75 · striker -20+2.00 · orb -8+1.00
PROTECTED_GROSS = [113.75, 0.0, -37.25, 0.0, 16.00, 35.75]
PROTECTED_SIDES = [10.0, 0.0, 8.0, 0.0, 2.0, 10.0]
PROTECTED_AE = [24.75, 0.00, 65.00, 0.00, 6.00, 25.75]


def _netted(cps, gross, sides):
    return [g - s * cps for g, s in zip(gross, sides)]


def _lowed(cps, adverse, sides):
    return [0.0 - a - s * cps for a, s in zip(adverse, sides)]


# ── §6 table ─────────────────────────────────────────────────────────────


def test_pairs_entry_exit_rows(tmp_path):
    """Trade-number pairing, Exit-row precedence, empty-cell fallback, tz conversion."""
    rows = [_row(1, "2026-01-05 09:35", "2026-01-05 10:20", 4, 100.0, 1.25, 25.0)]
    path, digest = write_table(tmp_path, ("aegis_6j", "normal"), rows, bom=True)
    trades = parse_trade_list_csv(path, leg="aegis_6j", export_tz=EXPORT_TZ)
    assert len(trades) == 1
    trade = trades[0]
    # Trade-level values come from the Exit row (the Entry row carries them x7).
    assert trade.trade_number == 1
    assert trade.qty == 4
    assert trade.net_usd == pytest.approx(100.0)
    assert trade.commission_usd == pytest.approx(1.25)
    assert trade.adverse_excursion_usd == pytest.approx(25.0)
    assert trade.gross_usd == pytest.approx(101.25)
    assert trade.sides == pytest.approx(8.0)
    assert trade.entry_ny.isoformat() == "2026-01-05T09:35:00-05:00"
    assert trade.session_date == date(2026, 1, 5)
    # The pinned digest is accepted by the loading seam.
    assert load_trade_table(path, digest, leg="aegis_6j", export_tz=EXPORT_TZ) == trades

    # An empty Exit cell falls back to the Entry row (x7 there ⇒ 8.75).
    fallback, _ = write_table(
        tmp_path / "fallback",
        ("aegis_6j", "normal"),
        rows,
        blank_exit_columns=("Commission USD",),
    )
    fallback_trade = parse_trade_list_csv(
        fallback, leg="aegis_6j", export_tz=EXPORT_TZ
    )[0]
    assert fallback_trade.commission_usd == pytest.approx(1.25 * 7.0)
    assert fallback_trade.net_usd == pytest.approx(100.0)  # still the Exit cell

    # export_tz is honoured: 21:00 UTC is 16:00 America/New_York the same day.
    utc_rows = [_row(1, "2026-01-06 13:35", "2026-01-06 21:00", 1, 10.0, 0.5, 2.0)]
    utc_path, _ = write_table(tmp_path / "utc", ("orb_mnq_v7", "normal"), utc_rows)
    utc_trade = parse_trade_list_csv(
        utc_path, leg="orb_mnq_v7", export_tz="UTC"
    )[0]
    assert (utc_trade.entry_ny.hour, utc_trade.entry_ny.minute) == (8, 35)
    assert (utc_trade.exit_ny.hour, utc_trade.exit_ny.minute) == (16, 0)
    assert utc_trade.session_date == date(2026, 1, 6)

    # Unpaired rows are refused: an Entry with no Exit, and an Exit with no Entry.
    entry_only = tmp_path / "entry_only.csv"
    write_csv(entry_only, rows, pairs=False)
    with pytest.raises(ValueError, match="no exit row"):
        parse_trade_list_csv(entry_only, leg="aegis_6j", export_tz=EXPORT_TZ)

    lines = [list(TRADE_LIST_COLUMNS)]
    lines.append(_cells(rows[0], "exit", scale=1.0, blank=frozenset()))
    exit_only = tmp_path / "exit_only.csv"
    exit_only.write_text("\r\n".join(",".join(c) for c in lines) + "\r\n", encoding="utf-8")
    with pytest.raises(ValueError, match="no entry row"):
        parse_trade_list_csv(exit_only, leg="aegis_6j", export_tz=EXPORT_TZ)

    # A duplicated Exit row for the same trade number is refused too.
    duplicate = tmp_path / "duplicate.csv"
    doubled = [list(TRADE_LIST_COLUMNS)]
    doubled.append(_cells(rows[0], "entry", scale=7.0, blank=frozenset()))
    doubled.append(_cells(rows[0], "exit", scale=1.0, blank=frozenset()))
    doubled.append(_cells(rows[0], "exit", scale=1.0, blank=frozenset()))
    duplicate.write_text(
        "\r\n".join(",".join(c) for c in doubled) + "\r\n", encoding="utf-8"
    )
    with pytest.raises(ValueError, match="more than one Exit row"):
        parse_trade_list_csv(duplicate, leg="aegis_6j", export_tz=EXPORT_TZ)

    # A foreign header is refused before any row is read.
    foreign = tmp_path / "foreign.csv"
    write_csv(foreign, rows, header=["Trade number", "Type", "Date and time"])
    with pytest.raises(ValueError, match="17-column"):
        parse_trade_list_csv(foreign, leg="aegis_6j", export_tz=EXPORT_TZ)


def test_gross_net_per_tier(tmp_path):
    """Hand-computed daily gross and per-tier net for the four frozen tiers."""
    bundle = build(tmp_path, STANDARD)
    assert bundle.daily["normal"]["gross"] == pytest.approx(NORMAL_GROSS)
    assert bundle.daily["normal"]["sides"] == pytest.approx(NORMAL_SIDES)
    assert bundle.daily["protected"]["gross"] == pytest.approx(PROTECTED_GROSS)
    assert bundle.daily["protected"]["sides"] == pytest.approx(PROTECTED_SIDES)

    for tier in TIERS:
        cps = CPS[tier]
        assert bundle.tiers[tier]["normal_pnl"] == pytest.approx(
            _netted(cps, NORMAL_GROSS, NORMAL_SIDES)
        ), tier
        assert bundle.tiers[tier]["protected_pnl"] == pytest.approx(
            _netted(cps, PROTECTED_GROSS, PROTECTED_SIDES)
        ), tier

    # Spot literals (independent of the helper above), one per tier and mode.
    # 01-05: gross 456.60, 24 sides; 01-07 protected: gross -37.25, 8 sides.
    assert bundle.tiers["Bulenox_100K"]["normal_pnl"][0] == pytest.approx(
        456.60 - 24 * 0.61
    )  # 441.96
    assert bundle.tiers["Tradeify_Select_100K"]["normal_pnl"][0] == pytest.approx(
        434.76
    )
    assert bundle.tiers["MFFU_Rapid_100K"]["normal_pnl"][5] == pytest.approx(
        192.80 - 24 * 0.95
    )  # 170.00
    assert bundle.tiers["BluSky_Premium_100K"]["protected_pnl"][0] == pytest.approx(
        113.75 - 10 * 0.95
    )  # 104.25
    assert bundle.tiers["Bulenox_100K"]["protected_pnl"][2] == pytest.approx(
        -37.25 - 8 * 0.61
    )  # -42.13
    assert bundle.tiers["Tradeify_Select_100K"]["protected_pnl"][4] == pytest.approx(
        16.00 - 2 * 0.91
    )  # 14.18
    assert bundle.tiers["MFFU_Rapid_100K"]["normal_pnl"][2] == pytest.approx(
        -238.00 - 16 * 0.95
    )  # -253.20
    # Costs are read from core/firm_rules.py, not restated here.
    assert bundle.manifest["tiers"]["Bulenox_100K"]["cost_per_side_usd"] == 0.61


def test_intraday_low_coincident_sum(tmp_path):
    """low = -Σ|Adverse excursion| - day cost; every entry ≤ 0 and finite."""
    bundle = build(tmp_path, STANDARD)
    assert bundle.daily["normal"]["adverse_excursion"] == pytest.approx(NORMAL_AE)
    assert bundle.daily["protected"]["adverse_excursion"] == pytest.approx(
        PROTECTED_AE
    )
    for tier in TIERS:
        cps = CPS[tier]
        assert bundle.tiers[tier]["normal_low"] == pytest.approx(
            _lowed(cps, NORMAL_AE, NORMAL_SIDES)
        ), tier
        assert bundle.tiers[tier]["protected_low"] == pytest.approx(
            _lowed(cps, PROTECTED_AE, PROTECTED_SIDES)
        ), tier
        for mode in MODES:
            low = bundle.tiers[tier][f"{mode}_low"]
            assert np.all(np.isfinite(low)) and np.all(low <= 0.0)
            pnl = bundle.tiers[tier][f"{mode}_pnl"]
            assert np.all(np.isfinite(pnl))
            # The coincident |AE| sum is independent of the day's net: a day may
            # lose less at the close than its worst excursion (and vice versa).
            assert np.all(low <= 0.0)

    # Spot literals: 01-07 normal has Σ|AE| 160 and 16 sides.
    assert bundle.tiers["Bulenox_100K"]["normal_low"][2] == pytest.approx(
        -(160.00 + 16 * 0.61)
    )  # -169.76
    assert bundle.tiers["Tradeify_Select_100K"]["normal_low"][2] == pytest.approx(
        -174.56
    )
    assert bundle.tiers["MFFU_Rapid_100K"]["protected_low"][2] == pytest.approx(
        -(65.00 + 8 * 0.95)
    )  # -72.60
    # A no-trade day is exactly zero, never -0.0 and never a cost-only row.
    assert bundle.tiers["BluSky_Premium_100K"]["normal_low"][4] == 0.0
    assert str(bundle.tiers["BluSky_Premium_100K"]["normal_low"][4]) == "0.0"


def test_zero_rows_and_window(tmp_path):
    """Weekday calendar inside the computed window, zero rows on no-trade days."""
    bundle = build(tmp_path, STANDARD)
    assert bundle.dates == DATES  # Jan 10/11 (Sat/Sun) are not rows
    assert bundle.window == (date(2026, 1, 5), date(2026, 1, 12))
    zero_normal = DATES.index(date(2026, 1, 9))
    zero_protected = DATES.index(date(2026, 1, 6))
    for tier in TIERS:
        assert bundle.tiers[tier]["normal_pnl"][zero_normal] == 0.0
        assert bundle.tiers[tier]["normal_low"][zero_normal] == 0.0
        assert bundle.tiers[tier]["protected_pnl"][zero_protected] == 0.0
        assert bundle.tiers[tier]["protected_low"][zero_protected] == 0.0
    assert bundle.daily["normal"]["gross"][zero_normal] == 0.0
    assert bundle.daily["normal"]["sides"][zero_normal] == 0.0

    # Window = max(first session) .. min(last session) over the six inputs, and
    # trades outside it are dropped: aegis trades 01-05 and 01-16 only, the other
    # five tables 01-07 .. 01-12, so the window is [2026-01-07, 2026-01-12].
    def _stamp(day, hour, minute):
        return f"2026-01-{day:02d} {hour:02d}:{minute:02d}"

    staggered = {
        ("aegis_6j", "normal"): [
            _row(1, _stamp(5, 9, 35), _stamp(5, 10, 20), 8, 99_999.0, 0.0, 1.0),
            _row(2, _stamp(16, 9, 35), _stamp(16, 10, 20), 8, 99_999.0, 0.0, 1.0),
        ],
        ("dj30_mym_p250", "normal"): [
            _row(1, _stamp(7, 9, 35), _stamp(7, 10, 0), 1, 10.0, 1.00, 2.0),
            _row(2, _stamp(12, 9, 35), _stamp(12, 10, 0), 1, 10.0, 1.00, 2.0),
        ],
        ("dj30_mym_p250", "protected"): [
            _row(1, _stamp(7, 10, 0), _stamp(7, 10, 30), 1, 5.0, 1.00, 1.0),
            _row(2, _stamp(12, 10, 0), _stamp(12, 10, 30), 1, 5.0, 1.00, 1.0),
        ],
        ("vanguard_mgc", "normal"): [
            _row(1, _stamp(7, 11, 0), _stamp(7, 11, 30), 1, 20.0, 1.00, 3.0),
            _row(2, _stamp(12, 11, 0), _stamp(12, 11, 30), 1, 20.0, 1.00, 3.0),
        ],
        ("orb_mnq_v7", "normal"): [
            _row(1, _stamp(7, 12, 0), _stamp(7, 12, 30), 1, -5.0, 1.00, 4.0),
            _row(2, _stamp(12, 12, 0), _stamp(12, 12, 30), 1, -5.0, 1.00, 4.0),
        ],
        ("orb_mnq_v7", "protected"): [
            _row(1, _stamp(7, 13, 0), _stamp(7, 13, 30), 1, 2.0, 1.00, 1.0),
            _row(2, _stamp(12, 13, 0), _stamp(12, 13, 30), 1, 2.0, 1.00, 1.0),
        ],
    }
    narrowed = build(tmp_path / "staggered", staggered, tag="staggered")
    assert narrowed.window == (date(2026, 1, 7), date(2026, 1, 12))
    assert narrowed.dates == [
        date(2026, 1, 7),
        date(2026, 1, 8),
        date(2026, 1, 9),
        date(2026, 1, 12),
    ]
    # The out-of-window aegis trades (rescaled to 8 ⇒ ~1.6M gross) never appear;
    # the kept days carry exactly the three in-window legs.
    assert narrowed.daily["normal"]["gross"] == pytest.approx([28.0, 0.0, 0.0, 28.0])
    assert narrowed.daily["normal"]["sides"] == pytest.approx([6.0, 0.0, 0.0, 6.0])
    assert narrowed.daily["normal"]["adverse_excursion"] == pytest.approx(
        [9.0, 0.0, 0.0, 9.0]
    )
    assert narrowed.daily["protected"]["gross"] == pytest.approx([9.0, 0.0, 0.0, 9.0])


def test_aegis_per_contract_rescale(tmp_path):
    """A 1..8 Aegis ladder rescaled per contract to 8 (normal) and 3 (protected)."""
    ladder = [
        _row(
            n,
            f"2026-01-05 09:{30 + n:02d}",
            f"2026-01-05 10:{30 + n:02d}",
            n,
            10.0 * n,
            0.25 * n,
            2.0 * n,
        )
        for n in range(1, 9)
    ]
    tables = {key: [] for key in STANDARD}
    tables[("aegis_6j", "normal")] = ladder
    bundle = build(tmp_path, tables)
    assert bundle.dates == [date(2026, 1, 5)]

    # Every exported trade carries 10.00 net + 0.25 commission and 2.00 |AE| per
    # contract, so at target 8 each trade is gross 8 x 10.25 and 16 sides.
    assert bundle.daily["normal"]["gross"] == pytest.approx([8 * 8 * 10.25])
    assert bundle.daily["normal"]["sides"] == pytest.approx([8 * 2 * 8.0])
    assert bundle.daily["normal"]["adverse_excursion"] == pytest.approx([8 * 8 * 2.0])
    # The derived protected channel is the SAME export at target 3.
    assert bundle.daily["protected"]["gross"] == pytest.approx([8 * 3 * 10.25])
    assert bundle.daily["protected"]["sides"] == pytest.approx([8 * 2 * 3.0])
    assert bundle.daily["protected"]["adverse_excursion"] == pytest.approx(
        [8 * 3 * 2.0]
    )
    # Per-tier net and low follow the rescaled quantities.
    assert bundle.tiers["Bulenox_100K"]["normal_pnl"] == pytest.approx(
        [656.00 - 128 * 0.61]
    )  # 577.92
    assert bundle.tiers["Bulenox_100K"]["normal_low"] == pytest.approx(
        [-(128.00 + 128 * 0.61)]
    )  # -206.08
    assert bundle.tiers["Tradeify_Select_100K"]["normal_pnl"] == pytest.approx(
        [539.52]
    )
    assert bundle.tiers["MFFU_Rapid_100K"]["protected_pnl"] == pytest.approx(
        [246.00 - 48 * 0.95]
    )  # 200.40
    assert bundle.tiers["BluSky_Premium_100K"]["protected_low"] == pytest.approx(
        [-(48.00 + 48 * 0.95)]
    )  # -93.60
    # The spec is what carries the two Aegis targets.
    assert DEFAULT_QUANTITY_SPEC["aegis_6j"] == {"normal": 8, "protected": 3}


def test_vanguard_protected_zero(tmp_path):
    """The ``zero`` spec gives Vanguard protected zero P&L and zero low."""
    tables = copy.deepcopy(STANDARD)
    # A large Vanguard normal loss on 01-08, a day with no protected trade at all.
    tables[("vanguard_mgc", "normal")][1] = _row(
        2, "2026-01-08 09:35", "2026-01-08 10:00", 2, -500.0, 1.60, 250.0
    )
    bundle = build(tmp_path, tables)
    assert DEFAULT_QUANTITY_SPEC["vanguard_mgc"]["protected"] == "zero"
    position = DATES.index(date(2026, 1, 8))
    # Normal mode still carries the leg: -500 + 1.60 plus orb's 45 + 1.00.
    assert bundle.daily["normal"]["gross"][position] == pytest.approx(-452.40)
    assert bundle.daily["normal"]["sides"][position] == pytest.approx(6.0)
    assert bundle.daily["normal"]["adverse_excursion"][position] == pytest.approx(
        259.00
    )
    assert bundle.tiers["Bulenox_100K"]["normal_pnl"][position] == pytest.approx(
        -452.40 - 6 * 0.61
    )  # -456.06
    # Protected mode on the same day is exactly zero: no Vanguard entry exists.
    for tier in TIERS:
        assert bundle.tiers[tier]["protected_pnl"][position] == 0.0
        assert bundle.tiers[tier]["protected_low"][position] == 0.0
    # ... and the protected channel is alive on days the other legs do trade, so
    # the zeros come from the spec, not from an empty protected fixture.
    assert bundle.tiers["Bulenox_100K"]["protected_pnl"][0] == pytest.approx(107.65)
    assert bundle.tiers["Tradeify_Select_100K"]["protected_low"][5] == pytest.approx(
        -34.85
    )


def test_mffu_flag(tmp_path):
    """An exit at 16:15 ET flags; an exit at 16:00 does not."""
    clean = build(tmp_path, STANDARD)
    assert clean.mffu_admissible is True
    assert clean.mffu_flagged_days == 0
    assert clean.manifest["mffu_admissible"] is True

    def _with_aegis_exit(exit_time):
        tables = copy.deepcopy(STANDARD)
        tables[("aegis_6j", "normal")][1] = _row(
            2, "2026-01-07 09:40", f"2026-01-07 {exit_time}", 2, -60.0, 0.50, 40.0
        )
        return tables

    late = build(tmp_path / "late", _with_aegis_exit("16:15"), tag="late")
    assert late.mffu_admissible is False
    assert late.mffu_flagged_days == 1  # one session date, both modes
    assert late.manifest["mffu_admissible"] is False
    assert late.manifest["mffu_flagged_days"] == 1

    early = build(tmp_path / "early", _with_aegis_exit("16:00"), tag="early")
    assert early.mffu_admissible is True
    assert early.mffu_flagged_days == 0


def test_late_exit_raises(tmp_path):
    """An exit after 16:45 ET raises (the export does not match the venue bound)."""
    tables = copy.deepcopy(STANDARD)
    tables[("orb_mnq_v7", "normal")][1] = _row(
        2, "2026-01-08 10:00", "2026-01-08 16:50", 1, 45.0, 1.00, 9.0
    )
    with pytest.raises(ValueError, match="16:45"):
        build(tmp_path, tables)

    # A trade spanning two CME trade dates (18:00 ET roll) raises as well.
    overnight = copy.deepcopy(STANDARD)
    overnight[("dj30_mym_p250", "normal")][0] = _row(
        1, "2026-01-05 15:00", "2026-01-06 09:00", 1, 200.0, 2.00, 10.0
    )
    with pytest.raises(ValueError, match="different CME trade dates"):
        build(tmp_path / "overnight", overnight, tag="overnight")


def test_cme_trade_date_rollover(tmp_path):
    """A Globex-evening entry belongs to the next trade date; an 18:00+ exit is not late."""
    path = tmp_path / "evening.csv"
    write_csv(path, [
        _row(1, "2026-01-05 22:00", "2026-01-06 09:00", 1, 50.0, 1.00, 5.0),
        _row(2, "2026-01-06 18:05", "2026-01-06 19:30", 1, -20.0, 1.00, 30.0),
    ])
    trades = parse_trade_list_csv(path, leg="aegis_6j", export_tz=EXPORT_TZ)
    assert [t.session_date for t in trades] == [date(2026, 1, 6), date(2026, 1, 7)]
    assert not any(t.flags_mffu() for t in trades)


def test_hash_mismatch_raises(tmp_path):
    """A wrong pin raises before any row is parsed."""
    rows = [_row(1, "2026-01-05 09:35", "2026-01-05 10:20", 4, 100.0, 1.00, 25.0)]
    # The file is unparseable (Entry row only), yet the hash error must come first.
    entry_only = tmp_path / "entry_only.csv"
    write_csv(entry_only, rows, pairs=False)
    wrong_pin = "f" * 64
    with pytest.raises(InputIdentityError, match="SHA-256 mismatch"):
        load_trade_table(entry_only, wrong_pin, leg="aegis_6j", export_tz=EXPORT_TZ)
    assert issubclass(InputIdentityError, ValueError)

    # The correct pin parses the same bytes without error.
    path, digest = write_table(tmp_path / "ok", ("aegis_6j", "normal"), rows)
    assert (
        load_trade_table(path, digest, leg="aegis_6j", export_tz=EXPORT_TZ)[0].net_usd
        == pytest.approx(100.0)
    )
    with pytest.raises(InputIdentityError):
        load_trade_table(path, "0" * 64, leg="aegis_6j", export_tz=EXPORT_TZ)


def test_feeds_paired_blocks(tmp_path):
    """The output passes ``paired_blocks_from_daily`` unchanged in shape."""
    bundle = build(tmp_path, STANDARD)
    for tier in TIERS:
        for mode in MODES:
            pnl = bundle.tiers[tier][f"{mode}_pnl"]
            low = bundle.tiers[tier][f"{mode}_low"]
            blocks_pnl, blocks_low = paired_blocks_from_daily(pnl, low)
            assert blocks_pnl.shape == blocks_low.shape == (1, 5, 1)
            assert np.array_equal(blocks_pnl[:, :, 0], pnl[:5].reshape(1, 5))
            assert np.array_equal(blocks_low[:, :, 0], low[:5].reshape(1, 5))
            assert np.all(blocks_low <= 0.0)


def test_cli_refuses_tracked_out(tmp_path):
    """The CLI writes to an untracked directory and refuses a git-tracked one."""
    root = tmp_path / "inputs"
    inputs = []
    for key, rows in STANDARD.items():
        path, digest = write_table(root, key, rows)
        inputs.append(f"{key[0]}:{key[1]}={path}@{digest}")
    # argparse needs one --input flag per table (action="append").
    argv = [part for token in inputs for part in ("--input", token)]

    out = tmp_path / "out"
    assert main([*argv, "--export-tz", EXPORT_TZ, "--out", str(out)]) == 0
    assert sorted(p.name for p in out.iterdir()) == [
        "BluSky_Premium_100K.csv",
        "Bulenox_100K.csv",
        "MFFU_Rapid_100K.csv",
        "Tradeify_Select_100K.csv",
        "manifest.json",
    ]
    manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    for name, record in manifest["outputs"].items():
        assert record["sha256"] == sha256_file(out / name)
    assert manifest["export_tz"] == EXPORT_TZ
    assert manifest["window"] == {"start": "2026-01-05", "end": "2026-01-12"}
    assert manifest["inputs"]["aegis_6j:protected"]["derived"] is True
    assert manifest["inputs"]["vanguard_mgc:protected"]["derived"] is True
    assert manifest["inputs"]["aegis_6j:protected"]["sha256"] == manifest["inputs"][
        "aegis_6j:normal"
    ]["sha256"]
    with (out / "Bulenox_100K.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert [row["date"] for row in rows] == [day.isoformat() for day in DATES]
    assert float(rows[0]["normal_pnl"]) == pytest.approx(441.96)
    assert float(rows[2]["normal_low"]) == pytest.approx(-169.76)
    assert float(rows[0]["protected_pnl"]) == pytest.approx(107.65)
    assert float(rows[5]["protected_low"]) == pytest.approx(-31.85)
    assert float(rows[4]["normal_pnl"]) == 0.0

    # An explicit --quantity-spec JSON equal to the default changes nothing.
    spec_path = tmp_path / "spec.json"
    spec_path.write_text(json.dumps(DEFAULT_QUANTITY_SPEC), encoding="utf-8")
    out_spec = tmp_path / "out_spec"
    assert (
        main(
            [
                *argv,
                "--quantity-spec",
                str(spec_path),
                "--export-tz",
                EXPORT_TZ,
                "--out",
                str(out_spec),
            ]
        )
        == 0
    )
    assert (out_spec / "Bulenox_100K.csv").read_text(encoding="utf-8") == (
        out / "Bulenox_100K.csv"
    ).read_text(encoding="utf-8")

    # Refusals: the repo root and a tracked directory inside it.
    for tracked in (REPO, REPO / "core"):
        with pytest.raises(OutputPathError):
            main([*argv, "--export-tz", EXPORT_TZ, "--out", str(tracked)])
    # Nothing was written by the refused runs.
    assert not (REPO / "core" / "manifest.json").exists()


def test_exit_at_1645_is_late(tmp_path):
    """16:45 ET itself is inside the forbidden [16:45, 18:00) exit interval."""
    tables = copy.deepcopy(STANDARD)
    tables[("orb_mnq_v7", "normal")][1] = _row(
        2, "2026-01-08 10:00", "2026-01-08 16:45", 1, 45.0, 1.00, 9.0
    )
    with pytest.raises(ValueError, match="16:45"):
        build(tmp_path, tables)


@pytest.mark.parametrize("missing", [
    ("dj30_mym_p250", "protected"),
    ("orb_mnq_v7", "protected"),
    ("aegis_6j", "normal"),
    ("vanguard_mgc", "normal"),
])
def test_missing_required_table_fails_closed(tmp_path, missing):
    """Only Aegis protected and Vanguard protected are derived; every other table is required."""
    tables = copy.deepcopy(STANDARD)
    del tables[missing]
    with pytest.raises(ValueError, match="required"):
        build(tmp_path, tables)


def test_derived_cell_supplied_as_table_is_rejected(tmp_path):
    """A table for a derived cell (Aegis protected) is refused, not silently preferred."""
    tables = copy.deepcopy(STANDARD)
    tables[("aegis_6j", "protected")] = copy.deepcopy(STANDARD[("aegis_6j", "normal")])
    with pytest.raises(ValueError, match="derived"):
        build(tmp_path, tables)
