"""Tests for scripts/cost_geometry_pregate.py — the instrument-ledger Phase-0
cost-geometry pre-gate (ADR 2026-06-22).

The gate makes L-COST-GEOMETRY mechanical: cost_R = round_trip_cost / stop_dist,
PASS iff cost_R < ceiling. These tests pin it against the two documented anchors
the gate is paid for by:

  * USOIL spike-fader (docs/adr/2026-06-14-reject-usoil-rdm-spike-fader.md /
    lab/analysis/usoil_rdm/RESULTS.md): realized round-trip cost ~0.090R on a
    sub-ATR confirmation stop -> FAIL.
  * USDCAD 15m cost law (ops/instruments/USDCAD.md durable finding #1):
    0.097R round-trip at a 1.42xATR stop; 0.055R at 2.5xATR -> both FAIL @0.05.

Stdlib-only (no numpy/pandas/pytest hard dep) so it runs on a public clone.
"""
from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

_CGP_PATH = Path(__file__).resolve().parent.parent / "scripts" / "cost_geometry_pregate.py"
_spec = importlib.util.spec_from_file_location("cost_geometry_pregate", _CGP_PATH)
cgp = importlib.util.module_from_spec(_spec)
# Register before exec so dataclass annotation resolution (PEP 563 strings +
# Optional[...] fields) can find the module in sys.modules.
sys.modules["cost_geometry_pregate"] = cgp
_spec.loader.exec_module(cgp)


def _flat_bars(true_range: float, close: float = 1.0, n: int = 60) -> "cgp.Bars":
    """Synthetic OHLC with a constant true range so median(ATR) == true_range
    exactly: close held flat, high = close + tr, low = close => H-L = tr,
    |H-Cprev| = tr, |L-Cprev| = 0 => TR = tr on every bar."""
    return cgp.Bars(
        high=[close + true_range] * n,
        low=[close] * n,
        close=[close] * n,
        spread=None,
    )


# ── geometry primitives ────────────────────────────────────────

def test_cost_r_basic():
    assert cgp.cost_r(0.00012, 0.002) == 0.06          # 1.2 pip / (2xATR=20pip)
    assert math.isinf(cgp.cost_r(0.001, 0.0))          # sub-tick stop -> inf
    assert math.isnan(cgp.cost_r(0.001, float("nan")))


def test_round_trip_cost_doubles_per_side_terms():
    # spread is already round-trip; slippage + commission are per-side (x2).
    c = cgp.round_trip_cost_price(spread=0.0001, slippage_per_side=0.00001,
                                  commission_bps_per_side=0.5, ref_price=100.0)
    # 0.0001 + 2*0.00001 + 2*(0.5/1e4)*100 = 0.0001 + 0.00002 + 0.01
    assert math.isclose(c, 0.0001 + 0.00002 + 0.01, rel_tol=1e-12)


def test_band_thresholds_match_costlaw():
    assert cgp.classify_band(0.02) == "comfortable"
    assert cgp.classify_band(0.05) == "acceptable"
    assert cgp.classify_band(0.09) == "marginal"
    assert cgp.classify_band(0.15) == "crippling"


def test_wilder_atr_constant_true_range():
    bars = _flat_bars(0.0010, n=40)
    med, n = cgp.median_atr(bars, period=14)
    assert math.isclose(med, 0.0010, rel_tol=1e-9)
    assert n == 40 - 14  # defined from index `period` onward


# ── documented anchors (the lesson made mechanical) ─────────────

def test_usoil_spike_fader_fails_on_realized_substop():
    """USOIL: x_price ~0.08, realized confirmation stop ~0.9 (sub-ATR at 4H
    ATR~3.0) -> ~0.089R, the ~0.090R kill. FAILS, sub-ATR flagged."""
    bars = _flat_bars(3.0, close=90.0, n=60)  # 4H ATR ~ 3.0
    r = cgp.evaluate(bars, spread=0.08, stop_atr=None, realized_stop=0.9,
                     ceiling=0.05, symbol="USOIL")
    assert r.verdict == "FAIL"
    assert math.isclose(r.cost_r, 0.08 / 0.9, rel_tol=1e-6)
    assert 0.088 < r.cost_r < 0.091          # ~0.090R documented
    assert r.realized_stop_in_atr < 1.0      # the sub-ATR trap is visible
    assert r.band == "marginal"


def test_usdcad_15m_cost_law_anchor():
    """USDCAD finding #1: 0.097R at 1.42xATR, 0.055R at 2.5xATR. With the
    measured spread/ATR ratio ~0.1377 both stop choices FAIL @0.05."""
    atr = 0.0009
    ratio = 0.1377
    spread = ratio * atr
    bars = _flat_bars(atr, close=1.35, n=60)

    tight = cgp.evaluate(bars, spread=spread, stop_atr=1.42, realized_stop=None,
                         ceiling=0.05, symbol="USDCAD")
    assert tight.verdict == "FAIL"
    assert math.isclose(tight.cost_r, ratio / 1.42, rel_tol=1e-6)
    assert 0.096 < tight.cost_r < 0.098      # ~0.097R documented

    wide = cgp.evaluate(bars, spread=spread, stop_atr=2.5, realized_stop=None,
                        ceiling=0.05, symbol="USDCAD")
    assert wide.verdict == "FAIL"            # 0.055R still > 0.05 ceiling
    assert 0.054 < wide.cost_r < 0.056


def test_range_fx_cross_class_flag():
    """The EURGBP/EURCHF failure mode the 5th-leg search keeps surfacing: a
    1.2-pip spread on a 10-pip 15m ATR at a 2xATR stop = 0.06R -> FAIL."""
    bars = _flat_bars(0.0010, close=0.86, n=60)   # ~10 pip ATR
    r = cgp.evaluate(bars, spread=0.00012, stop_atr=2.0, realized_stop=None,
                     ceiling=0.05, symbol="EURGBP")
    assert r.verdict == "FAIL"
    assert math.isclose(r.cost_r, 0.06, rel_tol=1e-9)
    assert math.isclose(r.cost_ratio_1x_atr, 0.12, rel_tol=1e-9)


def test_clean_instrument_passes():
    """Wide ATR relative to spread + a generous stop clears the gate."""
    bars = _flat_bars(0.0012, close=1.10, n=60)
    r = cgp.evaluate(bars, spread=0.00006, stop_atr=3.0, realized_stop=None,
                     ceiling=0.05, symbol="EURUSD")
    assert r.verdict == "PASS"
    assert r.cost_r < 0.05
    assert r.band in ("comfortable", "acceptable")


def test_spread_column_median_used():
    bars = cgp.Bars(
        high=[1.0 + 0.001] * 30, low=[1.0] * 30, close=[1.0] * 30,
        spread=[0.0001, 0.0002, 0.0003] * 10,   # median 0.0002
    )
    r = cgp.evaluate(bars, spread=None, stop_atr=2.0, realized_stop=None, ceiling=0.05)
    assert math.isclose(r.round_trip_spread, 0.0002, rel_tol=1e-9)


# ── feed parsing (canonical M15 + BAR EXPORT v0.1) ──────────────

def test_parse_canonical_m15(tmp_path):
    p = tmp_path / "EURGBP_M15.csv"
    rows = ["time,open,high,low,close,volume"]
    for i in range(20):
        rows.append(f"2024-01-01T0{i%10}:00:00Z,0.86,0.861,0.86,0.8605,{100+i}")
    p.write_text("\n".join(rows) + "\n", encoding="utf-8")
    bars = cgp.parse_ohlc(p)
    assert len(bars.close) == 20
    assert bars.high[0] == 0.861


def test_parse_bar_export_signal(tmp_path):
    p = tmp_path / "panel.csv"
    rows = ["Trade #,Type,Date and time,Signal"]
    for i in range(20):
        epoch = 1_700_000_000_000 + i * 900_000
        rows.append(f"{i},Entry long,2024-01-01,{epoch}|90.0|90.5|89.8|90.1|123")
    p.write_text("\n".join(rows) + "\n", encoding="utf-8")
    bars = cgp.parse_ohlc(p)
    assert len(bars.close) == 20
    assert bars.high[0] == 90.5
    assert bars.low[0] == 89.8


# Stdlib runner so the suite is verifiable without pytest (deps absent on some
# clones). Skips the tmp_path fixtures (run those under pytest).
if __name__ == "__main__":
    import tempfile

    passed = 0
    for name, fn in sorted(globals().items()):
        if not (name.startswith("test_") and callable(fn)):
            continue
        if "tmp_path" in fn.__code__.co_varnames[: fn.__code__.co_argcount]:
            with tempfile.TemporaryDirectory() as d:
                fn(Path(d))
        else:
            fn()
        passed += 1
        print(f"  PASS {name}")
    print(f"\n{passed} tests passed")
