"""regenerate_return_series: reproducibility index over FrozenRule pointers."""
from __future__ import annotations

import json
from argparse import Namespace

import numpy as np
import pandas as pd
import pytest

from discovery import register_search as rs
from discovery.motif_rules import evaluate_rule, freeze_rule_from_spec
from discovery.return_series_index import regenerate_return_series
from discovery.synthetic_bars import MotifSpec, default_motif_shape, generate_synthetic_bars


@pytest.fixture
def ledger(tmp_path, monkeypatch):
    d = tmp_path / "discovery_manifests"
    monkeypatch.setattr(rs, "LEDGER", d)
    return d


def _open_close_with_provenance(ledger, tmp_path, *, candidate_id: str, provenance_path: str):
    rs.open_run(
        Namespace(
            run_id="rs_idx_run",
            tool="catch22",
            search_space_size=10,
            alpha=0.05,
            data_window="2016-01-01:2016-06-30",
            hypothesis="h",
            params="",
            params_file=None,
            lane="blind",
            reachability_attestation=None,
            profile_cell="MNQ:motif",
            profile_consult=None,
            admission_file=None,
            prereg=None,
            cost_law_instrument=None,
            cost_law_firm_key=None,
            cost_law_panel_price=None,
            cost_law_cohort_delta_bp=None,
            cost_law_slip_ticks=None,
            cost_law_slip_convention=None,
        )
    )
    # Blind lane ignores profile_cell for gates, but open_run only records it on
    # mechanism-first. Force-record the cell for series_loader tag coverage.
    man_path = ledger / "rs_idx_run.json"
    man = json.loads(man_path.read_text(encoding="utf-8"))
    man["profile_cell"] = "MNQ:motif"
    man_path.write_text(json.dumps(man, indent=2), encoding="utf-8")

    pv = tmp_path / "pvals.csv"
    pv.write_text(f"{candidate_id},0.001\nother,0.01\n", encoding="utf-8")
    mapping = tmp_path / "prov_map.json"
    mapping.write_text(json.dumps({candidate_id: provenance_path}), encoding="utf-8")
    rs.close_run(
        Namespace(
            run_id="rs_idx_run",
            pvalues=None,
            pvalues_file=str(pv),
            operator_stopped=False,
            executed_k=None,
            stop_reason=None,
            executed_looks=None,
            rule_provenance_file=str(mapping),
        )
    )


def _planted_fixture(tmp_path, candidate_id="planted"):
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
    series = synth.bars["ret"]
    rule = freeze_rule_from_spec(
        shape, direction=1, horizon=3, trigger=5.0, candidate_id=candidate_id
    )
    payload = [{**rule.as_provenance(), "shape": [float(v) for v in rule.shape]}]
    prov = tmp_path / "rules.json"
    prov.write_text(json.dumps(payload), encoding="utf-8")
    return series, rule, str(prov)


def test_regenerate_matches_evaluate_rule_numerically(ledger, tmp_path):
    series, rule, prov_path = _planted_fixture(tmp_path)
    _open_close_with_provenance(
        ledger, tmp_path, candidate_id=rule.candidate_id, provenance_path=prov_path
    )

    def loader(tag, data_window):
        assert tag == "MNQ"
        assert data_window == "2016-01-01:2016-06-30"
        return series

    out = regenerate_return_series(
        "rs_idx_run",
        rule.candidate_id,
        ledger_dir=ledger,
        series_loader=loader,
    )
    direct = evaluate_rule(rule, series.to_numpy(), cost_frac_per_rt=0.0)
    assert out.name == rule.candidate_id
    assert isinstance(out.index, pd.DatetimeIndex)
    np.testing.assert_allclose(out.to_numpy(), direct.bar_returns, rtol=0, atol=1e-15)


def test_missing_provenance_path_raises_actionable_error(ledger, tmp_path):
    rs.open_run(
        Namespace(
            run_id="no_prov",
            tool="catch22",
            search_space_size=10,
            alpha=0.05,
            data_window="2016-01-01:2016-06-30",
            hypothesis="h",
            params="",
            params_file=None,
            lane="blind",
            reachability_attestation=None,
            profile_cell=None,
            profile_consult=None,
            admission_file=None,
            prereg=None,
            cost_law_instrument=None,
            cost_law_firm_key=None,
            cost_law_panel_price=None,
            cost_law_cohort_delta_bp=None,
            cost_law_slip_ticks=None,
            cost_law_slip_convention=None,
        )
    )
    pv = tmp_path / "pvals.csv"
    pv.write_text("orphan,0.001\n", encoding="utf-8")
    rs.close_run(
        Namespace(
            run_id="no_prov",
            pvalues=None,
            pvalues_file=str(pv),
            operator_stopped=False,
            executed_k=None,
            stop_reason=None,
            executed_looks=None,
            rule_provenance_file=None,
        )
    )

    def loader(tag, data_window):
        return np.zeros(10)

    with pytest.raises(ValueError) as excinfo:
        regenerate_return_series(
            "no_prov", "orphan", ledger_dir=ledger, series_loader=loader
        )
    msg = str(excinfo.value)
    assert "no recorded rule_provenance_path" in msg
    assert "orphan" in msg


def test_provenance_file_without_matching_candidate_raises(ledger, tmp_path):
    series, rule, _ = _planted_fixture(tmp_path, candidate_id="wanted")
    # Provenance file holds a different id.
    other = freeze_rule_from_spec(
        default_motif_shape(20, seed=5),
        direction=1,
        horizon=3,
        trigger=5.0,
        candidate_id="other_id",
    )
    prov = tmp_path / "wrong_rules.json"
    prov.write_text(
        json.dumps([{**other.as_provenance(), "shape": [float(v) for v in other.shape]}]),
        encoding="utf-8",
    )
    _open_close_with_provenance(
        ledger, tmp_path, candidate_id="wanted", provenance_path=str(prov)
    )

    def loader(tag, data_window):
        return series

    with pytest.raises(ValueError) as excinfo:
        regenerate_return_series(
            "rs_idx_run", "wanted", ledger_dir=ledger, series_loader=loader
        )
    msg = str(excinfo.value)
    assert "no FrozenRule with candidate_id='wanted'" in msg
    assert "other_id" in msg


def test_series_loader_is_required_keyword():
    with pytest.raises(TypeError):
        regenerate_return_series("r", "c")  # type: ignore[call-arg]
