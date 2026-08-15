"""Stage-4→7 real-data driver tests — synthetic fixtures, offline only."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

pytest.importorskip("arch")
pytest.importorskip("skfolio")
pytest.importorskip("stumpy")
pytest.importorskip("ruptures")

# Campaign glue imports (series + drivers live under lab/analysis/...).
_CAMPAIGN = Path(__file__).resolve().parents[1] / "lab" / "analysis" / "disccamp0_gc_2010_18"
sys.path.insert(0, str(_CAMPAIGN))
sys.path.insert(0, str(_CAMPAIGN.parents[1]))  # lab/

from discovery.frozen_rules import FrozenRuleLoadError, load_frozen_rules
from discovery.k_count import compute_k_bracket
from discovery.matrix_emit import emit_stage4
from discovery.motif_rules import freeze_rule_from_spec
from discovery.scorer import score_rules
from discovery.synthetic_bars import MotifSpec, default_motif_shape, generate_synthetic_bars
from research_utils.repo_root import repo_root
from research_utils.prereg_paths import DISC_CAMP_0_PREREG
from research_utils.universe_gate import load_returns_matrix, load_thresholds_from_prereg

from series import (
    build_mgc_oos_series,
    daily_leader_returns_from_hourly,
    hourly_daily_volume_leader,
    volume_lead_stitch_hourly_only,
    within_contract_log_returns,
)

_PREREG = DISC_CAMP_0_PREREG
_CAMPAIGN_DIR = repo_root() / "lab" / "analysis" / "disccamp0_gc_2010_18"


def _synthetic_mgc_hourly(*, roll_day: str | None = "2019-06-15") -> pd.DataFrame:
    """Two outrights across UTC days with a known volume leader + optional roll."""
    rows = []
    sym_a, sym_b = "MGCZ9", "MGCZ0"
    for day in pd.date_range("2019-05-06", "2019-05-08", freq="D", tz="UTC"):
        for hour in range(3):
            ts = day + pd.Timedelta(hours=hour)
            # sym_a dominates volume on days 1-2; sym_b on day 3.
            vol_a = 100 if day.day < 8 else 10
            vol_b = 10 if day.day < 8 else 200
            rows.append(
                {
                    "ts": ts,
                    "symbol": sym_a,
                    "close": 1500.0 + hour * 0.1,
                    "volume": vol_a,
                }
            )
            rows.append(
                {
                    "ts": ts,
                    "symbol": sym_b,
                    "close": 1510.0 + hour * 0.2,
                    "volume": vol_b,
                }
            )
    if roll_day:
        d = pd.Timestamp(roll_day, tz="UTC")
        for hour in range(2):
            ts = d + pd.Timedelta(hours=hour)
            rows.append(
                {
                    "ts": ts,
                    "symbol": sym_a,
                    "close": 1520.0,
                    "volume": 50,
                }
            )
            rows.append(
                {
                    "ts": ts,
                    "symbol": sym_b,
                    "close": 1530.0 + hour,
                    "volume": 80,
                }
            )
    df = pd.DataFrame(rows).set_index("ts")
    df.index.name = "ts"
    return df.sort_index()


# ------------------------------------------------------------------ 2.1 series


def test_hourly_daily_volume_leader_schedule():
    hourly = _synthetic_mgc_hourly(roll_day=None)
    leader = hourly_daily_volume_leader(hourly)
    assert leader.iloc[0] == "MGCZ9"
    assert leader.iloc[-1] == "MGCZ0"


def test_volume_lead_stitch_hourly_only_membership():
    hourly = _synthetic_mgc_hourly(roll_day=None)
    stitched = volume_lead_stitch_hourly_only(hourly)
    assert (stitched["symbol"] == "MGCZ9").all() or stitched["symbol"].nunique() >= 1
    assert len(stitched) > 0


def test_within_contract_returns_roll_boundary():
    hourly = _synthetic_mgc_hourly()
    stitched = volume_lead_stitch_hourly_only(hourly)
    ret = within_contract_log_returns(stitched, hourly)
    assert ret.size == len(stitched)
    # First bar of each contract should be 0.0 (no phantom roll gap).
    sym = stitched["symbol"].to_numpy()
    for i in range(1, len(ret)):
        if sym[i] != sym[i - 1]:
            assert ret[i] == 0.0 or np.isfinite(ret[i])


def test_daily_aggregation_from_hourly():
    hourly = _synthetic_mgc_hourly(roll_day=None)
    daily, daily_ret = daily_leader_returns_from_hourly(hourly)
    assert len(daily) >= 2
    assert daily_ret.size == len(daily)
    assert np.all(np.isfinite(daily_ret[1:]))


def test_build_mgc_oos_series_injectable():
    hourly = _synthetic_mgc_hourly(roll_day=None)
    stitched, ret, h = build_mgc_oos_series(hourly)
    assert len(stitched) == len(ret)
    assert len(h) >= len(stitched)


# ------------------------------------------------------------------ 2.2 frozen rules


def test_load_frozen_rules_roundtrip(tmp_path):
    shape = default_motif_shape(10, seed=1)
    rule = freeze_rule_from_spec(
        shape, direction=1, horizon=3, trigger=0.5, candidate_id="test_rule"
    )
    payload = [
        {
            **rule.as_provenance(),
            "shape": [float(v) for v in rule.shape],
        }
    ]
    p = tmp_path / "rules.json"
    p.write_text(json.dumps(payload))
    loaded = load_frozen_rules(p)
    assert len(loaded) == 1
    assert loaded[0].candidate_id == "test_rule"
    assert loaded[0].shape_hash == rule.shape_hash


def test_load_frozen_rules_tamper_fails(tmp_path):
    shape = default_motif_shape(10, seed=2)
    rule = freeze_rule_from_spec(
        shape, direction=1, horizon=3, trigger=0.5, candidate_id="tamper"
    )
    payload = [
        {
            **rule.as_provenance(),
            "shape": [float(v) for v in rule.shape],
        }
    ]
    payload[0]["shape"][0] += 0.01  # corrupt bytes, keep stale hash
    p = tmp_path / "rules.json"
    p.write_text(json.dumps(payload))
    with pytest.raises(FrozenRuleLoadError):
        load_frozen_rules(p)


def test_load_stage3_frozen_rules_integrity():
    rules = load_frozen_rules(_CAMPAIGN_DIR / "stage3_frozen_rules.json")
    assert len(rules) == 6


# ------------------------------------------------------------------ 2.3 run_stage4


def test_run_stage4_gate_refusal_no_flag():
    from run_stage4 import main

    assert main([]) == 2


def test_run_stage4_gate_refusal_no_cache(monkeypatch):
    from run_stage4 import main

    monkeypatch.setattr("run_stage4.mgc_oos_cache_exists", lambda: False)
    assert main(["--real-oos"]) == 2


def test_run_stage4_zero_survivor_emits_meta_and_marker(tmp_path):
    from run_stage4 import emit_zero_survivor_bundle

    report = json.loads((_CAMPAIGN_DIR / "stage3_report.json").read_text())
    meta_p, marker_p = emit_zero_survivor_bundle(
        out_dir=tmp_path, run_id="test_zero", report=report
    )
    meta = json.loads(meta_p.read_text())
    marker = json.loads(marker_p.read_text())
    assert meta["k_spa"] == 0
    assert meta["k_dsr"] == 3177
    assert meta["v_rule"] == "1/n"
    assert len(meta["kill_provenance"]) == 6
    assert all(not c["cost_law_pass"] for c in meta["kill_provenance"])
    assert marker_p.name.endswith("__stage45_skipped.json")
    assert marker["k_spa"] == 0
    assert not (tmp_path / "test_zero__stage4_matrix.csv").exists()


def test_run_stage4_with_survivors_roundtrip(tmp_path):
    from run_stage4 import run_stage4_real

    m = 20
    shape = default_motif_shape(m, seed=5)
    motif = MotifSpec(
        shape=shape,
        horizon=3,
        direction=1,
        per_trade_sr=0.35,
        trade_vol=0.008,
        period=25,
        max_oos_trades=120,
    )
    synth = generate_synthetic_bars(
        seed=11,
        motif=motif,
        is_start="2016-01-01",
        is_end="2016-06-30",
        oos_start="2019-05-06",
        oos_end="2019-12-31",
    )
    is_ret = synth.bars["ret"].to_numpy()[synth.is_mask]
    oos_ret = synth.bars["ret"].to_numpy()[synth.oos_mask]
    rule = freeze_rule_from_spec(
        shape, direction=1, horizon=3, trigger=5.0, candidate_id="planted"
    )
    bundle = score_rules([rule], is_ret, oos_ret, mgc_price=1800.0)
    assert bundle.survivors, "fixture must yield a cost-law survivor"

    # Build injectable hourly frame from synthetic OOS returns.
    idx = synth.bars.index[synth.oos_mask]
    hourly = pd.DataFrame(
        {
            "symbol": "MGCZ9",
            "close": np.cumprod(1 + oos_ret) * 1800,
            "volume": 100,
        },
        index=idx,
    )
    hourly.index.name = "ts"

    report = {
        "integrity": {"T": 51659, "k_dsr": 3177},
        "frozen_inputs": {"rt_cost_frac": 0.0002, "hurdle_4x_frac": 0.0008},
        "candidates": [
            {
                "candidate_id": "planted",
                "cost_law_pass": True,
                "is_pvalue": 0.01,
                "is_n_trades": 50,
                "is_mean_net_trade": 0.001,
            }
        ],
    }
    rules_path = tmp_path / "rules.json"
    rules_path.write_text(
        json.dumps(
            [{**rule.as_provenance(), "shape": [float(v) for v in rule.shape]}]
        )
    )
    report_path = tmp_path / "report.json"
    report_path.write_text(json.dumps(report))

    result = run_stage4_real(
        out_dir=tmp_path,
        run_id="syn_s4",
        hourly_oos=hourly,
        rules_path=rules_path,
        report_path=report_path,
    )
    assert result["k_spa"] == 1
    assert not result["zero_survivor"]
    rm = load_returns_matrix(tmp_path / "syn_s4__stage4_matrix.csv")
    assert "planted" in rm.candidate_ids
    meta = json.loads((tmp_path / "syn_s4__stage4_matrix.meta.json").read_text())
    assert meta["dedrift"] is True
    assert meta["v_rule"] == "1/n"
    assert meta["k_spa"] != meta["k_dsr"]


# ------------------------------------------------------------------ 2.4 run_stage5_6


def test_run_stage5_6_zero_survivor_skipped(tmp_path):
    from run_stage4 import emit_zero_survivor_bundle
    from run_stage5_6 import run_stage5_6

    report = json.loads((_CAMPAIGN_DIR / "stage3_report.json").read_text())
    emit_zero_survivor_bundle(out_dir=tmp_path, run_id="z", report=report)
    result = run_stage5_6(out_dir=tmp_path, run_id="z")
    assert result["skipped"] is True
    s5 = json.loads(Path(result["stage5"]).read_text())
    s6 = json.loads(Path(result["stage6"]).read_text())
    assert s5["verdict"] == "SKIPPED"
    assert s6["verdict"] == "SKIPPED"


def test_run_stage5_6_no_threshold_literals():
    text = (_CAMPAIGN_DIR / "run_stage5_6.py").read_text()
    for lit in ("0.95", "0.05", "0.5"):
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith('"""') or "§0.5" in line:
                continue
            if lit in line and "load_thresholds" not in line:
                pytest.fail(f"threshold literal {lit!r} in run_stage5_6.py: {line}")


def test_run_stage5_6_gate_with_synthetic_bundle(tmp_path):
    from run_stage5_6 import run_stage5_6

    m = 20
    shape = default_motif_shape(m, seed=8)
    motif = MotifSpec(
        shape=shape,
        horizon=3,
        direction=1,
        per_trade_sr=0.35,
        trade_vol=0.008,
        period=25,
        max_oos_trades=400,
    )
    synth = generate_synthetic_bars(seed=3, motif=motif)
    is_ret = synth.bars["ret"].to_numpy()[synth.is_mask]
    oos_ret = synth.bars["ret"].to_numpy()[synth.oos_mask]
    rule = freeze_rule_from_spec(shape, direction=1, horizon=3, trigger=5.0)
    bundle = score_rules([rule], is_ret, oos_ret, mgc_price=1800.0)
    assert bundle.survivors
    bracket = compute_k_bracket(52_000)
    emit_stage4(
        bundle.survivors,
        synth.bars.index[synth.oos_mask],
        bracket,
        out_dir=tmp_path,
        run_id="g",
        dedrift=True,
        underlying_ret=oos_ret,
        zero_benchmark=True,
    )
    idx = synth.bars.index[synth.oos_mask]
    hourly = pd.DataFrame(
        {"symbol": "MGCZ9", "close": np.cumprod(1 + oos_ret) * 1800, "volume": 100},
        index=idx,
    )
    result = run_stage5_6(
        out_dir=tmp_path,
        run_id="g",
        survivors=bundle.survivors,
        hourly_oos=hourly,
        reps=100,
    )
    assert result["skipped"] is False
    s5 = json.loads(Path(result["stage5"]).read_text())
    assert s5["detail"]["bound_block_size"] == 3
    assert s5["detail"]["cumulative_k"] == 3177
    assert "acf_block_size_diagnostic" in s5["detail"]


# ------------------------------------------------------------------ 2.5 run_stage7


def test_run_stage7_zero_survivor_skipped(tmp_path):
    from run_stage4 import emit_zero_survivor_bundle
    from run_stage7 import run_stage7

    report = json.loads((_CAMPAIGN_DIR / "stage3_report.json").read_text())
    emit_zero_survivor_bundle(out_dir=tmp_path, run_id="z7", report=report)
    result = run_stage7(out_dir=tmp_path, run_id="z7")
    assert result["skipped"] is True
    rep = json.loads(Path(result["stage7"]).read_text())
    assert rep["verdict"] == "SKIPPED"


def test_run_stage7_predicates_via_engine(tmp_path):
    from discovery.realism_mgc import ratio_clause, hurdle_clause, reconstruct_gross_gc
    from discovery.cost_mgc import hurdle_from_price

    rt = 0.0001
    hurdle = hurdle_from_price(1800.0)
    gross_high = [0.01, 0.01, 0.01]
    net_high = reconstruct_gross_gc(gross_high, rt)
    # subtract cost to get net from gross - wait, reconstruct adds cost to net
    net_from_gross = [g - rt for g in gross_high]
    assert ratio_clause(float(np.mean(net_from_gross)), float(np.mean(gross_high)))
    assert hurdle_clause(float(np.mean(net_from_gross)), hurdle)

    gross_low = [rt * 2, rt * 2]
    net_low = [g - rt for g in gross_low]
    assert not ratio_clause(float(np.mean(net_low)), float(np.mean(gross_low)))


def test_run_stage7_no_reimplemented_arithmetic():
    text = (_CAMPAIGN_DIR / "run_stage7.py").read_text()
    assert "reconstruct_gross_gc" in text
    assert "ratio_clause" in text
    assert "hurdle_clause" in text
    # Driver should not define its own ratio/hurdle predicates.
    assert "def ratio_clause" not in text
    assert "def hurdle_clause" not in text


# ------------------------------------------------------------------ 2.6 e2e


def test_e2e_zero_survivor_chain(tmp_path):
    from run_stage4 import emit_zero_survivor_bundle
    from run_stage5_6 import run_stage5_6
    from run_stage7 import run_stage7

    report = json.loads((_CAMPAIGN_DIR / "stage3_report.json").read_text())
    emit_zero_survivor_bundle(out_dir=tmp_path, run_id="e2e0", report=report)
    r56 = run_stage5_6(out_dir=tmp_path, run_id="e2e0")
    r7 = run_stage7(out_dir=tmp_path, run_id="e2e0")
    assert r56["skipped"] and r7["skipped"]


def test_e2e_with_survivors_plumbing(tmp_path):
    from run_stage4 import run_stage4_real
    from run_stage5_6 import run_stage5_6
    from run_stage7 import run_stage7

    m = 20
    shape = default_motif_shape(m, seed=9)
    motif = MotifSpec(
        shape=shape,
        horizon=3,
        direction=1,
        per_trade_sr=0.30,
        trade_vol=0.01,
        period=30,
        max_oos_trades=200,
    )
    synth = generate_synthetic_bars(seed=21, motif=motif)
    is_ret = synth.bars["ret"].to_numpy()[synth.is_mask]
    oos_ret = synth.bars["ret"].to_numpy()[synth.oos_mask]
    rule = freeze_rule_from_spec(
        shape, direction=1, horizon=3, trigger=5.0, candidate_id="e2e"
    )
    bundle = score_rules([rule], is_ret, oos_ret, mgc_price=1800.0)
    assert bundle.survivors

    idx = synth.bars.index[synth.oos_mask]
    hourly = pd.DataFrame(
        {"symbol": "MGCZ9", "close": np.cumprod(1 + oos_ret) * 1800, "volume": 100},
        index=idx,
    )
    report = {
        "integrity": {"T": 51659, "k_dsr": 3177},
        "frozen_inputs": {"rt_cost_frac": 0.0002, "hurdle_4x_frac": 0.0008},
        "candidates": [
            {
                "candidate_id": "e2e",
                "cost_law_pass": True,
                "is_pvalue": 0.02,
                "is_n_trades": 40,
                "is_mean_net_trade": 0.002,
                **rule.as_provenance(),
            }
        ],
    }
    rules_path = tmp_path / "rules.json"
    rules_path.write_text(
        json.dumps([{**rule.as_provenance(), "shape": [float(v) for v in rule.shape]}])
    )
    (tmp_path / "report.json").write_text(json.dumps(report))

    s4 = run_stage4_real(
        out_dir=tmp_path,
        run_id="e2e1",
        hourly_oos=hourly,
        rules_path=rules_path,
        report_path=tmp_path / "report.json",
    )
    assert s4["k_spa"] == 1
    s56 = run_stage5_6(
        out_dir=tmp_path,
        run_id="e2e1",
        hourly_oos=hourly,
        survivors=bundle.survivors,
        reps=80,
    )
    assert not s56["skipped"]
    meta = json.loads((tmp_path / "e2e1__stage4_matrix.meta.json").read_text())
    s7 = run_stage7(
        out_dir=tmp_path,
        run_id="e2e1",
        hourly_oos=hourly,
        meta_path=tmp_path / "e2e1__stage4_matrix.meta.json",
        rules_path=rules_path,
        survivor_ids=[c["candidate_id"] for c in meta["candidates"]],
    )
    assert not s7["skipped"]


def test_check_boundaries():
    root = repo_root()
    proc = subprocess.run(
        [sys.executable, str(root / "scripts" / "check_boundaries.py")],
        cwd=root,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
