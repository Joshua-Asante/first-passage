"""SPEC S6 + TNEC-1 — EM0/EM2–EM5 + N-EDGE + DSR-cap refusal at register_search open.

Paired positive/negative fixtures are mandatory: a corridor-clear open must
succeed, and Cap/EM0 + power refusals must abort with no manifest write.
EM1 / D1 / D2 are disclosure-only (never refuse); N-EDGE gates when supplied.
"""
from __future__ import annotations

import json
from argparse import Namespace
import pytest

from discovery import register_search
from discovery.admission_schema import (
    EM1_EDGE_FLOOR_R,
    REASON_CAP_EM0,
    REASON_D1,
    REASON_D2,
    REASON_EM1,
    REASON_N_EDGE,
    REASON_POWER,
    evaluate_admission,
)
from research_utils.axis_screen import CAP, POWER_MIN, floor_at_k


@pytest.fixture
def ledger(tmp_path, monkeypatch):
    d = tmp_path / "discovery_manifests"
    monkeypatch.setattr(register_search, "LEDGER", d)
    return d


def _admission_payload(catalogue_k=2, **overrides):
    row = {
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
    row.update(overrides)
    return row


def _admission_file(tmp_path, payload=None, name="admission.json"):
    p = tmp_path / name
    p.write_text(json.dumps(payload or _admission_payload()), encoding="utf-8")
    return str(p)


def _consult_file(tmp_path, text=None):
    p = tmp_path / "consult.txt"
    p.write_text(
        text
        or "=== MYM x opening-range-continuation ===\nverdict: DEAD (2026-07-16)\n",
        encoding="utf-8",
    )
    return str(p)


def _attestation(tmp_path, text="reachability attested at the panel basis"):
    p = tmp_path / "attestation.md"
    p.write_text(text, encoding="utf-8")
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
        profile_cell="MYM:opening-range-continuation",
        profile_consult=None,
        admission_file=None,
        prereg="docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md",
    )
    base.update(kw)
    return Namespace(**base)


def _mf_ready(tmp_path, catalogue_k=2, **adm_overrides):
    """Mechanism-first open inputs that clear attestation + profile + admission."""
    return dict(
        search_space_size=catalogue_k,
        lane="mechanism-first",
        reachability_attestation=_attestation(tmp_path),
        profile_cell="MYM:opening-range-continuation",
        profile_consult=_consult_file(tmp_path),
        admission_file=_admission_file(
            tmp_path, _admission_payload(catalogue_k=catalogue_k, **adm_overrides)
        ),
    )


def test_evaluate_admission_admits_corridor_clear_k2_with_power():
    from discovery.admission_schema import EMAdmission

    adm = EMAdmission(**_admission_payload(catalogue_k=2))
    result = evaluate_admission(adm, registered_k=2)
    assert result.admitted
    assert result.decision == "ADMIT"
    assert result.reasons == ()
    assert result.summary["floor_at_k"] == floor_at_k(2)
    assert result.summary["floor_at_k"] <= CAP
    assert result.summary["power"] >= POWER_MIN


def test_evaluate_admission_refuses_k4_cap_em0():
    from discovery.admission_schema import EMAdmission

    adm = EMAdmission(**_admission_payload(catalogue_k=4))
    result = evaluate_admission(adm, registered_k=4)
    assert not result.admitted
    assert REASON_CAP_EM0 in result.reasons
    assert floor_at_k(4) > CAP


def test_evaluate_admission_refuses_low_power():
    from discovery.admission_schema import EMAdmission

    adm = EMAdmission(
        **_admission_payload(
            catalogue_k=1, n_events=50, delta_over_sigma=0.05
        )
    )
    result = evaluate_admission(adm, registered_k=1)
    assert not result.admitted
    assert REASON_POWER in result.reasons
    assert REASON_CAP_EM0 not in result.reasons


def test_positive_mechanism_first_open_records_admission(ledger, tmp_path):
    """POSITIVE: K=1–2, EM clear, power≥0.50 → opens and records admission."""
    register_search.open_run(_open_args(**_mf_ready(tmp_path, catalogue_k=2)))

    path = ledger / "test_run.json"
    assert path.is_file()
    manifest = json.loads(path.read_text(encoding="utf-8"))
    assert manifest["lane"] == "mechanism-first"
    assert manifest["K"] == 2
    assert manifest["admission"]["decision"] == "ADMIT"
    assert manifest["admission"]["reasons"] == []
    assert manifest["admission"]["power"] >= POWER_MIN


@pytest.mark.parametrize("k", [1, 2])
def test_positive_open_at_working_budget_k(ledger, tmp_path, k):
    register_search.open_run(
        _open_args(run_id=f"k{k}", **_mf_ready(tmp_path, catalogue_k=k))
    )
    assert (ledger / f"k{k}.json").is_file()


def test_negative_k4_aborts_cap_em0_no_file(ledger, tmp_path):
    """NEGATIVE: K=4 → ABORT Cap/EM0, no manifest written."""
    with pytest.raises(SystemExit) as exc:
        register_search.open_run(_open_args(**_mf_ready(tmp_path, catalogue_k=4)))
    message = str(exc.value)
    assert message.startswith("ABORT:")
    assert REASON_CAP_EM0 in message
    assert not (ledger / "test_run.json").exists()


def test_negative_low_power_aborts_no_file(ledger, tmp_path):
    """NEGATIVE: power < 0.50 → ABORT, no manifest written."""
    with pytest.raises(SystemExit) as exc:
        register_search.open_run(
            _open_args(
                **_mf_ready(
                    tmp_path,
                    catalogue_k=1,
                    n_events=50,
                    delta_over_sigma=0.05,
                )
            )
        )
    message = str(exc.value)
    assert message.startswith("ABORT:")
    assert REASON_POWER in message
    assert not (ledger / "test_run.json").exists()


def test_mechanism_first_requires_admission_file(ledger, tmp_path):
    with pytest.raises(SystemExit) as exc:
        register_search.open_run(
            _open_args(
                reachability_attestation=_attestation(tmp_path),
                profile_consult=_consult_file(tmp_path),
                admission_file=None,
            )
        )
    assert "--admission-file" in str(exc.value)
    assert not (ledger / "test_run.json").exists()


def test_explicit_blind_lane_keeps_eleven_key_schema(ledger):
    """Explicit lane=blind still works with the frozen 11-key schema."""
    register_search.open_run(
        _open_args(
            lane="blind",
            search_space_size=100,
            reachability_attestation=None,
            profile_cell=None,
            profile_consult=None,
            admission_file=None,
            prereg=None,   # blind opens name no prereg (11-key schema)
        )
    )
    manifest = json.loads((ledger / "test_run.json").read_text(encoding="utf-8"))
    assert len(manifest) == 11
    assert set(manifest.keys()) == {
        "run_id", "status", "opened_at", "tool", "K", "alpha",
        "data_window", "hypothesis", "params", "closed_at", "results",
    }
    assert "lane" not in manifest
    assert "admission" not in manifest


def test_cli_parser_lane_defaults_to_mechanism_first():
    parser = register_search.build_parser()
    base = [
        "open", "--tool", "catch22", "--search-space-size", "2",
        "--data-window", "2010-01-01:2020-01-01", "--hypothesis", "h",
    ]
    ns_default = parser.parse_args(base)
    assert ns_default.lane == "mechanism-first"
    assert ns_default.admission_file is None

    ns_blind = parser.parse_args(base + ["--lane", "blind"])
    assert ns_blind.lane == "blind"


def test_em1_floor_constant_matches_screen():
    assert EM1_EDGE_FLOOR_R == 0.40


def test_em1_below_inversion_floor_is_disclosure_only_not_refuse():
    """TNEC-1: 0.40R is disclosure (frequency inversion), never an intake kill."""
    from discovery.admission_schema import EMAdmission

    adm = EMAdmission(
        **_admission_payload(
            catalogue_k=2,
            em1_edge_r=0.10,  # below EM1_EDGE_FLOOR_R
        )
    )
    result = evaluate_admission(adm, registered_k=2)
    assert result.admitted
    assert REASON_EM1 not in result.reasons
    assert result.summary["disclosures"]["em1_edge_r"] == 0.10
    assert result.summary["disclosures"]["em1_below_inversion_floor"] is True


def test_d1_d2_false_are_disclosure_only_not_refuse():
    """TNEC-1: ex-D1/D2 are recorded preferences — report, never gate."""
    from discovery.admission_schema import EMAdmission

    adm = EMAdmission(**_admission_payload(catalogue_k=2, d1=False, d2=False))
    result = evaluate_admission(adm, registered_k=2)
    assert result.admitted
    assert REASON_D1 not in result.reasons
    assert REASON_D2 not in result.reasons
    assert result.summary["disclosures"]["d1"] is False
    assert result.summary["disclosures"]["d2"] is False


def test_n_edge_refuses_nonpositive_net_expectancy():
    from discovery.admission_schema import EMAdmission

    adm = EMAdmission(
        **_admission_payload(
            catalogue_k=2,
            n_edge_net_expectancy=0.0,
            n_edge_ci_excludes_zero=True,
            n_edge_dsr=0.90,
        )
    )
    result = evaluate_admission(adm, registered_k=2)
    assert not result.admitted
    assert REASON_N_EDGE in result.reasons


def test_n_edge_refuses_ci_not_excluding_zero():
    from discovery.admission_schema import EMAdmission

    adm = EMAdmission(
        **_admission_payload(
            catalogue_k=2,
            n_edge_net_expectancy=0.12,
            n_edge_ci_excludes_zero=False,
            n_edge_dsr=0.90,
        )
    )
    result = evaluate_admission(adm, registered_k=2)
    assert not result.admitted
    assert REASON_N_EDGE in result.reasons


def test_n_edge_refuses_dsr_below_floor_at_k():
    from discovery.admission_schema import EMAdmission

    floor = floor_at_k(2)
    adm = EMAdmission(
        **_admission_payload(
            catalogue_k=2,
            n_edge_net_expectancy=0.12,
            n_edge_ci_excludes_zero=True,
            n_edge_dsr=floor - 0.01,
        )
    )
    result = evaluate_admission(adm, registered_k=2)
    assert not result.admitted
    assert REASON_N_EDGE in result.reasons


def test_n_edge_admits_when_necessity_limbs_clear():
    from discovery.admission_schema import EMAdmission

    floor = floor_at_k(2)
    adm = EMAdmission(
        **_admission_payload(
            catalogue_k=2,
            em1_edge_r=0.05,  # disclosure-only; must not refuse
            d1=False,
            d2=False,
            n_edge_net_expectancy=0.12,
            n_edge_ci_excludes_zero=True,
            n_edge_dsr=floor,
        )
    )
    result = evaluate_admission(adm, registered_k=2)
    assert result.admitted
    assert result.reasons == ()
    assert result.summary["disclosures"]["em1_below_inversion_floor"] is True
