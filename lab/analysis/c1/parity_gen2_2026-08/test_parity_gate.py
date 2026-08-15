"""Unit tests for Gen-2 parity gate — synthetic series only (no vendor CSV)."""
from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

import parity_gate as G  # noqa: E402


def _write_csv(path: Path, rows: list[dict[str, object]]) -> Path:
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


def _monotonic_pair(n: int = 40, noise: float = 0.0) -> tuple[list[float], list[float]]:
    """Engine and TV PnL that share rank order (high ρ) with optional noise."""
    eng = [float(i) - n / 2.0 for i in range(n)]
    tv = [x + noise * (1.0 if i % 2 == 0 else -1.0) for i, x in enumerate(eng)]
    return eng, tv


def test_spearman_perfect_monotone():
    x = list(range(10))
    y = [2 * v for v in x]
    assert G.spearman_rho(x, y) == pytest.approx(1.0)


def test_spearman_perfect_inverse():
    x = list(range(10))
    y = list(reversed(x))
    assert G.spearman_rho(x, y) == pytest.approx(-1.0)


def test_profit_factor_and_net():
    pnls = [10.0, -5.0, 20.0, -5.0]
    assert G.net_pnl(pnls) == pytest.approx(20.0)
    assert G.profit_factor(pnls) == pytest.approx(30.0 / 10.0)


def test_evaluate_admit_on_near_identical_series():
    eng, tv = _monotonic_pair(n=40, noise=0.01)
    result = G.evaluate(eng, tv)
    assert result.verdict == "ADMIT"
    assert result.n_trades == 40
    assert result.spearman_rho >= G.RANK_RHO_FLOOR
    assert result.net_rel <= G.NET_REL_BAND
    assert result.pf_rel <= G.PF_REL_BAND
    assert result.reasons == ()


def test_evaluate_fail_on_rank_inversion():
    eng = [float(i) for i in range(40)]
    tv = list(reversed(eng))
    result = G.evaluate(eng, tv)
    assert result.verdict == "FAIL"
    assert any("spearman_rho" in r for r in result.reasons)


def test_evaluate_fail_underpowered():
    eng, tv = _monotonic_pair(n=10, noise=0.0)
    result = G.evaluate(eng, tv)
    assert result.verdict == "FAIL"
    assert any("MIN_TRADES" in r for r in result.reasons)


def test_evaluate_fail_net_band():
    eng = [1.0] * 40
    tv = [10.0] * 40  # same ranks, huge net gap
    result = G.evaluate(eng, tv)
    assert result.verdict == "FAIL"
    assert any("net_rel" in r for r in result.reasons)


def test_run_gate_pass_fixture(tmp_path: Path):
    eng, tv = _monotonic_pair(n=40, noise=0.0)
    eng_rows = [
        {"trade_id": f"t{i}", "pnl": eng[i]} for i in range(len(eng))
    ]
    tv_rows = [
        {"trade_id": f"t{i}", "pnl": tv[i]} for i in range(len(tv))
    ]
    eng_path = _write_csv(tmp_path / "engine.csv", eng_rows)
    tv_path = _write_csv(tmp_path / "tv.csv", tv_rows)
    result = G.run_gate(eng_path, tv_path)
    assert result.verdict == "ADMIT"
    assert G.main(["--engine", str(eng_path), "--tv-anchor", str(tv_path)]) == G.EXIT_ADMIT


def test_run_gate_fail_fixture(tmp_path: Path):
    eng = [float(i) for i in range(40)]
    tv = list(reversed(eng))
    eng_rows = [{"pnl": v} for v in eng]
    tv_rows = [{"pnl": v} for v in tv]
    eng_path = _write_csv(tmp_path / "engine.csv", eng_rows)
    tv_path = _write_csv(tmp_path / "tv.csv", tv_rows)
    result = G.run_gate(eng_path, tv_path)
    assert result.verdict == "FAIL"
    assert G.main(["--engine", str(eng_path), "--tv-anchor", str(tv_path)]) == G.EXIT_FAIL


def test_align_trade_id_mismatch_fails(tmp_path: Path):
    eng_path = _write_csv(
        tmp_path / "engine.csv",
        [{"trade_id": "a", "pnl": 1.0}, {"trade_id": "b", "pnl": 2.0}]
        + [{"trade_id": f"x{i}", "pnl": float(i)} for i in range(38)],
    )
    tv_path = _write_csv(
        tmp_path / "tv.csv",
        [{"trade_id": "a", "pnl": 1.0}, {"trade_id": "c", "pnl": 2.0}]
        + [{"trade_id": f"x{i}", "pnl": float(i)} for i in range(38)],
    )
    result = G.run_gate(eng_path, tv_path)
    assert result.verdict == "FAIL"
    assert any("align:" in r for r in result.reasons)


def test_bands_match_prereg_literals():
    """Pin harness constants to the FROZEN-PRE-RUN table (no silent drift)."""
    assert G.RANK_RHO_FLOOR == 0.75
    assert G.NET_REL_BAND == 0.02
    assert G.PF_REL_BAND == 0.02
    assert G.MIN_TRADES == 30
    assert not math.isnan(G.EPS_DENOM)
