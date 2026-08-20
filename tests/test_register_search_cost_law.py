"""Optional Requirement-5/§2.2 cost-law pre-flight at register_search open.

ADR 2026-07-16 §4/§6 "optional later handoff". All-or-nothing opt-in: supply
all five --cost-law-* flags, or none. Paired positive/negative fixtures are
mandatory per this repo's own house style (test_register_search_admission.py).
"""
from __future__ import annotations

import json
from argparse import Namespace

import pytest

from discovery import register_search


@pytest.fixture
def ledger(tmp_path, monkeypatch):
    d = tmp_path / "discovery_manifests"
    monkeypatch.setattr(register_search, "LEDGER", d)
    return d


def _attestation(tmp_path, text="reachability attested at the panel basis"):
    p = tmp_path / "attestation.md"
    p.write_text(text, encoding="utf-8")
    return str(p)


def _consult_file(tmp_path):
    p = tmp_path / "consult.txt"
    p.write_text(
        "=== MNQ x opening-range-continuation ===\nverdict: PASS (2026-08-19)\n",
        encoding="utf-8",
    )
    return str(p)


def _admission_file(tmp_path, catalogue_k=2):
    p = tmp_path / "admission.json"
    p.write_text(
        json.dumps(
            {
                "catalogue_k": catalogue_k,
                "em1_edge_r": 0.65,
                "em2_risk_usd": 275.0,
                "em2_measured_edge_r": 0.65,
                "em3_independence_and_stops": True,
                "em4_weekly_cadence": True,
                "em5_session_slot_legal": True,
                "n_events": 1000,
                "delta_over_sigma": 0.113,
            }
        ),
        encoding="utf-8",
    )
    return str(p)


def _open_args(**kw):
    base = dict(
        run_id="test_run",
        tool="catch22",
        search_space_size=2,
        alpha=0.05,
        data_window="2010-01-01:2020-01-01",
        hypothesis="h",
        params="",
        params_file=None,
        lane="mechanism-first",
        reachability_attestation=None,
        profile_cell="MNQ:opening-range-continuation",
        profile_consult=None,
        admission_file=None,
        prereg="docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md",
        cost_law_instrument=None,
        cost_law_firm_key=None,
        cost_law_panel_price=None,
        cost_law_cohort_delta_bp=None,
        cost_law_slip_ticks=None,
        cost_law_slip_convention=None,
    )
    base.update(kw)
    return Namespace(**base)


def _mf_ready(tmp_path, **overrides):
    base = dict(
        lane="mechanism-first",
        reachability_attestation=_attestation(tmp_path),
        profile_cell="MNQ:opening-range-continuation",
        profile_consult=_consult_file(tmp_path),
        admission_file=_admission_file(tmp_path),
    )
    base.update(overrides)
    return base


def test_omitted_entirely_is_a_noop():
    """Supplying none of the five flags returns None -- today's status quo."""
    result = register_search._require_cost_law(_open_args())
    assert result is None


def test_partial_flags_abort_all_or_nothing():
    with pytest.raises(SystemExit) as exc:
        register_search._require_cost_law(
            _open_args(cost_law_instrument="MNQ", cost_law_firm_key="Tradeify_Select_100K")
        )
    assert "all-or-nothing" in str(exc.value)


def test_declared_delta_clears_hurdle_admits():
    """MNQ @ Tradeify_Select_100K, price 20000: hurdle is small in bp terms;
    a generous declared delta clears it."""
    result = register_search._require_cost_law(
        _open_args(
            cost_law_instrument="MNQ",
            cost_law_firm_key="Tradeify_Select_100K",
            cost_law_panel_price=20000.0,
            cost_law_cohort_delta_bp=5.0,
            cost_law_slip_ticks=1.0,
            cost_law_slip_convention="per_side",
        )
    )
    assert result is not None
    assert result["cohort_delta_bp"] == 5.0
    assert result["margin_bp"] > 0
    assert result["hurdle_4x_bp"] < 5.0


def test_declared_delta_below_hurdle_aborts():
    result_exc = None
    with pytest.raises(SystemExit) as exc:
        register_search._require_cost_law(
            _open_args(
                cost_law_instrument="MNQ",
                cost_law_firm_key="Tradeify_Select_100K",
                cost_law_panel_price=20000.0,
                cost_law_cohort_delta_bp=0.0001,
                cost_law_slip_ticks=1.0,
                cost_law_slip_convention="per_side",
            )
        )
    result_exc = exc
    assert "REFUSE" in str(result_exc.value)
    assert "Requirement 5" in str(result_exc.value)


def test_unknown_instrument_aborts_with_pricing_error():
    with pytest.raises(SystemExit) as exc:
        register_search._require_cost_law(
            _open_args(
                cost_law_instrument="NOT_A_REAL_SYMBOL",
                cost_law_firm_key="Tradeify_Select_100K",
                cost_law_panel_price=20000.0,
                cost_law_cohort_delta_bp=5.0,
                cost_law_slip_ticks=1.0,
                cost_law_slip_convention="per_side",
            )
        )
    assert "could not price" in str(exc.value)


def test_positive_open_records_cost_law_preflight_on_manifest(ledger, tmp_path):
    register_search.open_run(
        _open_args(
            **_mf_ready(
                tmp_path,
                cost_law_instrument="MNQ",
                cost_law_firm_key="Tradeify_Select_100K",
                cost_law_panel_price=20000.0,
                cost_law_cohort_delta_bp=5.0,
                cost_law_slip_ticks=1.0,
                cost_law_slip_convention="per_side",
            )
        )
    )
    manifest = json.loads((ledger / "test_run.json").read_text(encoding="utf-8"))
    assert "cost_law_preflight" in manifest
    assert manifest["cost_law_preflight"]["instrument"] == "MNQ"
    assert manifest["cost_law_preflight"]["margin_bp"] > 0


def test_negative_open_refused_below_hurdle_no_manifest_written(ledger, tmp_path):
    with pytest.raises(SystemExit) as exc:
        register_search.open_run(
            _open_args(
                **_mf_ready(
                    tmp_path,
                    cost_law_instrument="MNQ",
                    cost_law_firm_key="Tradeify_Select_100K",
                    cost_law_panel_price=20000.0,
                    cost_law_cohort_delta_bp=0.0001,
                    cost_law_slip_ticks=1.0,
                    cost_law_slip_convention="per_side",
                )
            )
        )
    assert "REFUSE" in str(exc.value)
    assert not (ledger / "test_run.json").exists()


def test_open_without_cost_law_flags_unaffected(ledger, tmp_path):
    """Omitting the pre-flight entirely does not change existing behavior."""
    register_search.open_run(_open_args(**_mf_ready(tmp_path)))
    manifest = json.loads((ledger / "test_run.json").read_text(encoding="utf-8"))
    assert "cost_law_preflight" not in manifest


def test_cli_parser_cost_law_flags_default_none():
    parser = register_search.build_parser()
    base = [
        "open", "--tool", "catch22", "--search-space-size", "2",
        "--data-window", "2010-01-01:2020-01-01", "--hypothesis", "h",
    ]
    ns = parser.parse_args(base)
    assert ns.cost_law_instrument is None
    assert ns.cost_law_firm_key is None
    assert ns.cost_law_panel_price is None
    assert ns.cost_law_cohort_delta_bp is None
    assert ns.cost_law_slip_ticks is None
    assert ns.cost_law_slip_convention is None
