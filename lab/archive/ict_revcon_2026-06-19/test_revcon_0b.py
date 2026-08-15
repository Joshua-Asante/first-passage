"""Synthetic-fixture unit tests for revcon_0b.py (Q-ICT-1H-REVCON-1 / Phase 0b).

CONFIRMATORY bias-conditioned discriminator. Per PREREG-0B (RATIFIED): the SOLE partition
is the prior-week weekly structBias sign; the family is {prem,disc}x{bias +1,-1}x{rev,cont}
at the fixed gate anchor (60/0.05). Data path = BAR_EXPORT v0.1 1H OHLC -> offline zone
(zone_series, validated 100% vs Pine) -> offline structBias (close vs weekly EMA-20, [1]-lag,
the Pine-confirmed gate definition).

These pin the NEW composition + gate logic on synthetic fixtures (no vendor data). The
underlying rate/CI/placebo/penalty primitives are REUSED from the audit-verified
harness_1h.py and revcon_probe_0a.py and are not re-tested here.

Run: python -m pytest lab/analysis/ict_revcon_2026-06-19/test_revcon_0b.py -q
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_CASCADE = _HERE.parent / "ict_cascade_2026-06-18"
_CORE = _HERE.parent.parent.parent / "core"
sys.path.insert(0, str(_CORE))
sys.path.insert(0, str(_CASCADE))
sys.path.insert(0, str(_HERE))
import revcon_0b as B  # noqa: E402
import harness_1h as H  # noqa: E402

H1_MS = 3_600_000
BASE_MS = int(pd.Timestamp("2024-01-01T00:00:00Z").value // 1_000_000)


def hour_epochs(n, start=BASE_MS, step=H1_MS):
    return np.array([start + i * step for i in range(n)], dtype="int64")


def _bar_csv(tmp_path, df, name="bar.csv"):
    """Write a BAR_EXPORT v0.1 List-of-Trades CSV: Entry rows carry the OHLCV in Signal."""
    rows = []
    for i, r in df.iterrows():
        sig = f"{int(r.epoch)}|{r.o}|{r.h}|{r.l}|{r.c}|{int(r.v)}"
        rows.append({"Trade number": i + 1, "Type": "Entry long",
                     "Date and time": pd.to_datetime(int(r.epoch), unit="ms", utc=True),
                     "Signal": sig, "Price USD": r.c})
        rows.append({"Trade number": i + 1, "Type": "Exit long",
                     "Date and time": pd.to_datetime(int(r.epoch), unit="ms", utc=True),
                     "Signal": "Close position order", "Price USD": r.c})
    p = tmp_path / name
    pd.DataFrame(rows).to_csv(p, index=False)
    return p


# =============================================================================
# BAR_EXPORT PAGE LOADING
# =============================================================================
def test_load_bar_pages_decodes_and_sorts(tmp_path):
    n = 50
    epoch = hour_epochs(n)
    close = np.arange(n, dtype=float) + 5000.0
    df = pd.DataFrame({"epoch": epoch, "o": close, "h": close + 2, "l": close - 2,
                       "c": close, "v": np.arange(n) + 1})
    # shuffle rows so the loader must sort
    p = _bar_csv(tmp_path, df.sample(frac=1.0, random_state=1).reset_index(drop=True))
    out = B.load_bar_pages(p)
    assert len(out) == n
    assert list(out["epoch"]) == sorted(out["epoch"])      # sorted ascending
    assert np.allclose(out["c"].values, close)


def test_load_bar_pages_multi_page_dedups(tmp_path):
    n = 30
    epoch = hour_epochs(n)
    close = np.arange(n, dtype=float) + 5000.0
    df = pd.DataFrame({"epoch": epoch, "o": close, "h": close + 1, "l": close - 1,
                       "c": close, "v": np.ones(n)})
    p1 = _bar_csv(tmp_path, df.iloc[:20], "p1.csv")
    p2 = _bar_csv(tmp_path, df.iloc[10:], "p2.csv")   # overlaps p1 on [10:20]
    out = B.load_bar_pages([p1, p2])
    assert len(out) == n                               # overlap deduped on epoch


# =============================================================================
# OFFLINE STRUCTBIAS ([1]-prior-week lag; the Pine-confirmed gate definition)
# =============================================================================
def test_load_weekly_gatebias_sorts_and_prior_week_lags(tmp_path):
    # AUDIT data-faithfulness: a real weekly gateBias export must be sorted ascending +
    # deduped BEFORE the [1] prior-week lag, regardless of export row order.
    weeks = pd.date_range("2022-01-03", periods=6, freq="7D", tz="UTC")
    g = [1, 1, -1, -1, 1, -1]                          # current-week structBias per week
    df = pd.DataFrame({"time": weeks, "gateBias": g}).sample(frac=1.0, random_state=2)  # shuffle rows
    p = tmp_path / "wk.csv"
    df.to_csv(p, index=False)
    epoch, lagged = B.load_weekly_gatebias(p)
    assert list(epoch) == sorted(epoch)               # sorted ascending despite shuffled input
    assert lagged[0] == 0                              # week 0 has no prior week
    assert list(lagged[1:]) == [float(x) for x in g[:-1]]   # prior-week sign


def test_structbias_offline_is_prior_week_lagged():
    # rising series over many ISO weeks -> each week's prior-week sign is +1; week 0 = 0.
    n = 2000
    epoch = hour_epochs(n)
    close = np.arange(n, dtype=float) + 5000.0
    wb_epoch, wb_val = B.structbias_offline(epoch, close, ema_len=3)
    assert wb_val[0] == 0          # no prior week
    assert wb_val[-1] == 1         # prior-week sign on a rising series


# =============================================================================
# CELL RATES (per zone x bias bucket; reversion + continuation)
# =============================================================================
def test_cell_rates_structure_and_floor():
    n = 1200
    epoch = hour_epochs(n)
    close = 5000.0 + 50.0 * np.sin(2 * np.pi * np.arange(n) / 24.0)
    ex = B.hour_export_from_ohlc(pd.DataFrame(
        {"epoch": epoch, "o": close, "h": close + 1, "l": close - 1, "c": close,
         "v": np.ones(n)}))
    sb = B.structbias_offline(epoch, close, ema_len=20)
    cells = B.cell_rates(ex, sb)
    # 4 (zone x bias) cells, each with rev + cont stride/block + n_floor
    for zone in ("prem", "disc"):
        for bias in (1, -1):
            c = cells[(zone, bias)]
            assert "rev" in c and "cont" in c and "n_floor" in c
            assert "rate" in c["rev"] and "clears" in c["rev"]


# =============================================================================
# PENALTY (8-way max-stat over the directional family)
# =============================================================================
def test_penalty_rejects_coinflip_winner():
    # all 8 directional rates near 0.5 -> winner must FAIL the deflated max-stat penalty.
    cells = {}
    for zone in ("prem", "disc"):
        for bias in (1, -1):
            cells[(zone, bias)] = {
                "rev": {"rate": 0.505, "n_eff": 60, "ci_lo": 0.44, "clears": False},
                "cont": {"rate": 0.495, "n_eff": 60, "ci_lo": 0.43, "clears": False},
                "n_floor": 60,
            }
    pen = B.penalty_8way(cells)
    assert pen["pass_dsr"] is False


def test_penalty_passes_strong_winner():
    cells = {}
    for zone in ("prem", "disc"):
        for bias in (1, -1):
            cells[(zone, bias)] = {
                "rev": {"rate": 0.51, "n_eff": 80, "ci_lo": 0.49, "clears": False},
                "cont": {"rate": 0.49, "n_eff": 80, "ci_lo": 0.41, "clears": False},
                "n_floor": 80,
            }
    # plant one strong cell (prem|-1 reversion)
    cells[("prem", -1)]["rev"] = {"rate": 0.86, "n_eff": 80, "ci_lo": 0.78, "clears": True}
    pen = B.penalty_8way(cells)
    assert pen["pass_dsr"] is True
    assert pen["winner"]["zone"] == "prem" and pen["winner"]["bias"] == -1
    assert pen["winner"]["direction"] == "rev"


def test_penalty_uses_floor_n_not_stride_n():
    # AUDIT F1 regression: the deflated max-stat variance/e_max must use the FLOOR n
    # (floor(N/fwdK), the n-floor gate basis), NOT stride_rate_ci's inflated greedy-kept
    # count. Here n_floor=30 but the cells carry stride n_eff=138 (~4.6x). A winner ci_lo
    # 0.60 would PASS under the stride-n e_max (~0.56) but must FAIL under the floor-n
    # e_max (~0.63) -- the false-positive direction PREREG-0B's Estimator PIN forbids.
    cells = {}
    for zone in ("prem", "disc"):
        for bias in (1, -1):
            cells[(zone, bias)] = {
                "rev": {"rate": 0.51, "n_eff": 138, "ci_lo": 0.49, "clears": False},
                "cont": {"rate": 0.49, "n_eff": 138, "ci_lo": 0.41, "clears": False},
                "n_floor": 30,
            }
    cells[("prem", -1)]["rev"] = {"rate": 0.66, "n_eff": 138, "ci_lo": 0.60, "clears": True}
    pen = B.penalty_8way(cells)
    assert pen["e_max"] > 0.60          # floor-n (30) threshold, not the stride-n (138) one
    assert pen["pass_dsr"] is False     # 0.60 < floor-n e_max -> rejected (stride-n would pass)


def test_penalty_winner_restricted_to_eligible():
    # AUDIT F2 regression: the winner must be the argmax-rate among ELIGIBLE (candidate)
    # cells, not the global argmax -- so a spurious high-rate non-candidate cannot steal
    # the verdict-bearing slot.
    cells = {}
    for zone in ("prem", "disc"):
        for bias in (1, -1):
            cells[(zone, bias)] = {
                "rev": {"rate": 0.50, "n_eff": 80, "ci_lo": 0.42, "clears": False},
                "cont": {"rate": 0.50, "n_eff": 80, "ci_lo": 0.42, "clears": False},
                "n_floor": 80,
            }
    cells[("prem", 1)]["cont"] = {"rate": 0.95, "n_eff": 80, "ci_lo": 0.88, "clears": True}  # spurious
    cells[("disc", -1)]["rev"] = {"rate": 0.70, "n_eff": 80, "ci_lo": 0.63, "clears": True}  # genuine
    elig = {("disc", -1, "rev")}        # only the genuine cell is a full candidate
    pen = B.penalty_8way(cells, eligible=elig)
    assert pen["winner"]["zone"] == "disc" and pen["winner"]["direction"] == "rev"
    assert pen["pass_dsr"] is True      # genuine cell clears the floor-n e_max


# --- verdict-level F2/F4 regression (inject cells; the gate logic is pure over cells) ---
def _mk_cell(rev_kw, cont_kw, n_floor):
    base = dict(ci_hi=0.9, n_eff=n_floor, block_rate=0.6, placebo=0.5,
                beats_placebo=True, halves_flips=False)
    return {"rev": {**base, **rev_kw}, "cont": {**base, **cont_kw},
            "n_floor": n_floor, "n_scored": n_floor * 12}


def _dead(n_floor=40):
    nc = dict(rate=0.50, ci_lo=0.42, clears=False, block_clears=False)
    return _mk_cell(nc, nc, n_floor)


def test_verdict_resolved_not_stolen_by_block_failing_cell(monkeypatch):
    # AUDIT F2 end-to-end: a genuine fully-clearing candidate (disc|-1 rev) must RESOLVE
    # even when a spurious higher-RATE cell (prem|+1 cont) clears stride but FAILS block
    # (so it is NOT a candidate). The spurious cell must not demote the verdict to AMBIGUOUS.
    cells = {
        ("prem", 1): _mk_cell(dict(rate=0.05, ci_lo=0.0, clears=False, block_clears=False),
                              dict(rate=0.95, ci_lo=0.85, clears=True, block_clears=False), 40),
        ("prem", -1): _dead(40),
        ("disc", 1): _dead(40),
        ("disc", -1): _mk_cell(dict(rate=0.70, ci_lo=0.63, clears=True, block_clears=True),
                               dict(rate=0.30, ci_lo=0.2, clears=False, block_clears=False), 150),
    }
    monkeypatch.setattr(B, "cell_rates", lambda ex, sb: cells)
    res = B.verdict_0b(None, None)
    assert res["verdict"] == "RESOLVED", res["verdict"]
    assert res["winner"]["zone"] == "disc" and res["winner"]["bias"] == -1
    assert res["winner"]["direction"] == "rev"


def test_verdict_ambiguous_on_stride_only_clear(monkeypatch):
    # AUDIT F4: a stride-clears/block-fails near-miss (the only signal) -> AMBIGUOUS (HOLD),
    # NOT the terminal FALSIFIED "close the campaign" disposition.
    cells = {
        ("prem", 1): _mk_cell(dict(rate=0.90, ci_lo=0.82, clears=True, block_clears=False),
                              dict(rate=0.10, ci_lo=0.0, clears=False, block_clears=False), 40),
        ("prem", -1): _dead(40), ("disc", 1): _dead(40), ("disc", -1): _dead(40),
    }
    monkeypatch.setattr(B, "cell_rates", lambda ex, sb: cells)
    res = B.verdict_0b(None, None)
    assert res["verdict"] == "AMBIGUOUS", res["verdict"]


def test_verdict_falsified_only_when_no_stride_clear(monkeypatch):
    # FALSIFIED is reserved for the clean case: NO cell clears stride in any direction.
    cells = {("prem", 1): _dead(40), ("prem", -1): _dead(40),
             ("disc", 1): _dead(40), ("disc", -1): _dead(40)}
    monkeypatch.setattr(B, "cell_rates", lambda ex, sb: cells)
    res = B.verdict_0b(None, None)
    assert res["verdict"] == "FALSIFIED", res["verdict"]


def test_verdict_ambiguous_when_only_starved_cell_clears(monkeypatch):
    # RE-AUDIT F4-1: all POWERED cells dead, but a STARVED cell (n_floor < 30) clears the
    # stride CI. PREREG-0B mandates AMBIGUOUS-HOLD for a starved candidate bucket -- NOT the
    # terminal FALSIFIED. any_stride_clear must be evaluated over ALL cells, not just powered.
    cells = {
        ("prem", 1): _mk_cell(dict(rate=0.90, ci_lo=0.80, clears=True, block_clears=True),
                              dict(rate=0.10, ci_lo=0.0, clears=False, block_clears=False), 10),  # starved clearer
        ("prem", -1): _dead(40), ("disc", 1): _dead(40), ("disc", -1): _dead(40),
    }
    monkeypatch.setattr(B, "cell_rates", lambda ex, sb: cells)
    res = B.verdict_0b(None, None)
    assert res["verdict"] == "AMBIGUOUS", res["verdict"]   # NOT FALSIFIED (the starved clearer exists)


def test_bucket_fwd_floor_reflects_regime_drift():
    # RE-AUDIT P-1: the placebo floor is the UNCONDITIONAL forward-direction rate within the
    # bias bucket (controls for regime drift), NOT the base-rate-deflated random_eq no-op.
    n = 300
    close = np.arange(n, dtype=float) + 1000.0   # strong uptrend
    mask = np.ones(n, bool)
    up = B.bucket_fwd_floor(close, mask, down=False, fwd_k=12)
    dn = B.bucket_fwd_floor(close, mask, down=True, fwd_k=12)
    assert up > 0.95 and dn < 0.05               # in an uptrend, up-rate ~1, down-rate ~0


def test_load_bar_pages_crosscheck_detects_drift(tmp_path):
    # RE-AUDIT L-2: the entry-price == encoded-close format-drift detector (from the core
    # loader) must be present -- a corrupted page where Price USD != encoded close raises.
    n = 20
    epoch = hour_epochs(n)
    close = np.arange(n, dtype=float) + 5000.0
    rows = []
    for i in range(n):
        sig = f"{int(epoch[i])}|{close[i]}|{close[i]+1}|{close[i]-1}|{close[i]}|1"
        px = close[i] + (50.0 if i == 7 else 0.0)   # bar 7 price drifts from encoded close
        rows.append({"Trade number": i + 1, "Type": "Entry long",
                     "Date and time": pd.to_datetime(int(epoch[i]), unit="ms", utc=True),
                     "Signal": sig, "Price USD": px})
    p = tmp_path / "drift.csv"
    pd.DataFrame(rows).to_csv(p, index=False)
    try:
        B.load_bar_pages(p)
    except ValueError as ex:
        assert "cross-check" in str(ex).lower() or "drift" in str(ex).lower()
    else:
        raise AssertionError("expected a format-drift ValueError on Price != encoded close")


# =============================================================================
# VERDICT (PREREG-0B sec-6 discriminator gate)
# =============================================================================
def test_verdict_insufficient_n_on_tiny():
    n = 200
    epoch = hour_epochs(n)
    close = 5000.0 + np.cumsum(np.random.default_rng(0).normal(0, 1, n))
    ex = B.hour_export_from_ohlc(pd.DataFrame(
        {"epoch": epoch, "o": close, "h": close + 1, "l": close - 1, "c": close,
         "v": np.ones(n)}))
    sb = B.structbias_offline(epoch, close, ema_len=20)
    res = B.verdict_0b(ex, sb)
    assert res["verdict"] == "INSUFFICIENT-N"


def test_verdict_falsified_on_coinflip():
    # large random walk -> bias buckets populated, but no cell carries direction -> FALSIFIED.
    rng = np.random.default_rng(11)
    n = 5000
    epoch = hour_epochs(n)
    close = 5000.0 + np.cumsum(rng.normal(0, 1, n))
    ex = B.hour_export_from_ohlc(pd.DataFrame(
        {"epoch": epoch, "o": close, "h": close + 1, "l": close - 1, "c": close,
         "v": np.ones(n)}))
    sb = B.structbias_offline(epoch, close, ema_len=20)
    res = B.verdict_0b(ex, sb)
    assert res["verdict"] in ("FALSIFIED", "INSUFFICIENT-N"), res["verdict"]
    # on a pure random walk the directional cells must not clear the penalized gate
    assert res["verdict"] != "RESOLVED"


# =============================================================================
# ORCHESTRATOR (skip-clean)
# =============================================================================
def test_run_0b_skips_when_absent(tmp_path, capsys):
    res = B.run_0b(bar_paths=[str(tmp_path / "nope.csv")])
    assert res is None
    assert "[SKIP]" in capsys.readouterr().out


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for fn in fns:
        try:
            import inspect
            kwargs = {}
            if "tmp_path" in inspect.signature(fn).parameters:
                import tempfile
                kwargs["tmp_path"] = Path(tempfile.mkdtemp())
            if "capsys" in inspect.signature(fn).parameters:
                continue
            fn(**kwargs)
            print(f"PASS {fn.__name__}"); passed += 1
        except AssertionError as ex:
            print(f"FAIL {fn.__name__}: {ex}")
        except Exception as ex:
            print(f"ERROR {fn.__name__}: {type(ex).__name__}: {ex}")
    print(f"\n{passed} passed")
