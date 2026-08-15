"""Tests for the Gen-2 §8 universe-gate orchestrator
.claude/skills/strategy-validation/scripts/universe_gate.py.

Research-venv-only module (imports arch + skfolio, per the databento-research-stack
ADR isolation rule). These tests `importorskip` those libs so they SKIP cleanly in
the ops venv / CI and RUN in .venv-research — the same skip-if-missing posture the
vendor-data tests use. Load-bearing test = `test_self_test_discriminates`: the gate
must REJECT the planted-noise control and PROMOTE the planted-edge control, else it
is miscalibrated and must not land (gate-orchestrator handoff §2 self-test wiring).
"""
from __future__ import annotations

import numpy as np
import pytest

pytest.importorskip("arch")
pytest.importorskip("skfolio")

# Canonical lab module (lab is on pytest pythonpath); imports arch/skfolio lazily.
import research_utils.universe_gate as ug  # noqa: E402
from research_utils.prereg_paths import DISC_CAMP_0_PREREG  # noqa: E402

_PREREG = DISC_CAMP_0_PREREG


def _thr() -> ug.Thresholds:
    """DISC-CAMP-0 thresholds. Public clones may lack the LTM prereg body;
    fall back to the frozen numbers the parser would have read (α=0.05,
    DSR=0.95, PBO=0.5, 5/7) so R5 default tests still run."""
    if _PREREG.exists():
        return ug.load_thresholds_from_prereg(_PREREG)
    return ug.Thresholds(
        alpha=0.05, dsr_min=0.95, pbo_max=0.5,
        consistency_min=5, consistency_years=7,
    )


# ---------------------------------------------------------------- thresholds

def test_thresholds_read_from_prereg_not_hardcoded():
    """Thresholds come from the campaign pre-registration file, never from
    literals baked into the gate (forbidden-move + §10 audit hook)."""
    thr = ug.load_thresholds_from_prereg(_PREREG)
    assert thr.alpha == 0.05
    assert thr.dsr_min == 0.95
    assert thr.pbo_max == 0.5
    # Consistency = 5/7 also parsed for the sibling battery to consume.
    assert thr.consistency_min == 5
    assert thr.consistency_years == 7


def test_thresholds_missing_file_errors_no_silent_default(tmp_path):
    """A missing / malformed pre-reg must ERROR, not silently fall back to a
    hardcoded default (that is exactly the drift the read-from-file rule prevents)."""
    bad = tmp_path / "nope.md"
    bad.write_text("no thresholds here\n")
    with pytest.raises(ValueError):
        ug.load_thresholds_from_prereg(bad)


# ---------------------------------------------------------------- block size

def test_acf_block_size_is_not_sqrt_t():
    """block_size is ACF-derived, and the module refuses the sqrt(T) heuristic."""
    rng = np.random.default_rng(0)
    # AR(1)-ish autocorrelated series so the ACF scale is a real, non-trivial lag.
    n = 400
    e = rng.normal(0, 1, n)
    x = np.zeros(n)
    for i in range(1, n):
        x[i] = 0.6 * x[i - 1] + e[i]
    bs = ug.acf_block_size(x)
    assert isinstance(bs, int)
    assert bs >= 1
    assert bs != int(np.sqrt(n))


def test_acf_block_size_rejects_sqrt_t_default_sentinel():
    """The helper never returns the arch sqrt(T) default silently; an iid series
    yields a SMALL ACF-derived block (a few lags at most), decisively below the
    sqrt(T) heuristic it replaces."""
    rng = np.random.default_rng(1)
    x = rng.normal(0, 1, 300)  # iid -> ACF enters the white-noise band within a few lags
    bs = ug.acf_block_size(x)
    assert 1 <= bs < int(np.sqrt(300))  # not the sqrt(300)=17 default


# ---------------------------------------------------------------- matrix I/O

def test_load_returns_matrix_roundtrip(tmp_path):
    """Stage-4 contract: CSV with a timestamp index, one column per candidate, and
    a `benchmark` column -> (T,K) returns matrix + (T,) benchmark + candidate ids."""
    csv = tmp_path / "run_returns.csv"
    csv.write_text(
        "timestamp,cand_0000,cand_0001,benchmark\n"
        "2019-05-06,0.01,-0.02,0.0\n"
        "2019-05-07,0.00,0.03,0.001\n"
        "2019-05-08,-0.01,0.01,0.0\n"
    )
    rm = ug.load_returns_matrix(csv)
    assert rm.returns.shape == (3, 2)
    assert rm.benchmark.shape == (3,)
    assert rm.candidate_ids == ["cand_0000", "cand_0001"]
    np.testing.assert_allclose(rm.returns[:, 1], [-0.02, 0.03, 0.01])
    np.testing.assert_allclose(rm.benchmark, [0.0, 0.001, 0.0])


def test_load_returns_matrix_requires_benchmark_column(tmp_path):
    csv = tmp_path / "nobench.csv"
    csv.write_text("timestamp,cand_0000\n2019-05-06,0.01\n")
    with pytest.raises(ValueError):
        ug.load_returns_matrix(csv)


# ---------------------------------------------------------------- self-test

def test_self_test_discriminates():
    """THE load-bearing calibration gate: planted noise REJECTED, planted edge
    PROMOTED. A gate that cannot tell them apart is miscalibrated."""
    thr = ug.load_thresholds_from_prereg(_PREREG)
    result = ug.self_test(thresholds=thr)
    assert result["negative"].promote is False
    assert result["positive"].promote is True


# ---------------------------------------------------------------- verdict AND

def test_verdict_requires_all_gates():
    """promote iff SPA rejects AND DSR>=min AND PBO<max. Force a DSR failure with a
    real-but-tiny edge under a huge cumulative K and confirm the verdict flips to
    reject even if SPA sees signal."""
    rng = np.random.default_rng(3)
    n, k = 250, 40
    drifts = np.linspace(0.0, 0.004, k)
    returns = np.column_stack([rng.normal(drifts[i], 0.01, n) for i in range(k)])
    benchmark = np.zeros(n)
    thr = ug.load_thresholds_from_prereg(_PREREG)
    # Inflate cumulative K so SR0 (selection benchmark) is high -> DSR must fail.
    verdict = ug.run_universe_gate(
        returns=returns, benchmark=benchmark,
        candidate_ids=[f"c{i}" for i in range(k)],
        cumulative_k=5_000_000, thresholds=thr, seed=7,
    )
    assert verdict.dsr < thr.dsr_min
    assert verdict.promote is False


def test_gate_verdict_carries_nulls_alive_ledger():
    """The verdict records which gates a candidate survived (the 'which nulls remain
    alive' ledger the brief requires), not just a boolean."""
    thr = ug.load_thresholds_from_prereg(_PREREG)
    result = ug.self_test(thresholds=thr)
    v = result["positive"]
    assert set(v.gate_results) >= {"spa", "dsr", "pbo"}
    assert all(isinstance(x, bool) for x in v.gate_results.values())


# ---------------------------------------------------------------- var_trials default (R5)
# Gate-stack audit R5 / 2026-08-15: module default is 1/n on the selected
# candidate's finite OOS trade count. The empirical Var(col_sr) estimator is
# no longer the default (it collapsed to 0.0 at K_SPA=1). An explicit pin
# still overrides.

def _edge_matrix(n_candidates, n_trades, true_edge_sr, seed):
    rng = np.random.default_rng(seed)
    vol = 0.01
    cols = [rng.normal((true_edge_sr * vol if i == 0 else 0.0), vol, size=n_trades)
            for i in range(n_candidates)]
    return np.column_stack(cols), np.zeros(n_trades)


def test_var_trials_default_is_one_over_n():
    """Omitting var_trials pins V = 1/n on the selected column's finite trade count."""
    thr = _thr()
    returns, bench = _edge_matrix(5, 500, 0.20, seed=101)
    ids = [f"c{i}" for i in range(5)]
    v_default = ug.run_universe_gate(returns=returns, benchmark=bench, candidate_ids=ids,
                                     cumulative_k=3200, thresholds=thr, seed=101,
                                     run_pbo=False)
    assert v_default.detail["var_trials"] == pytest.approx(1.0 / 500)


def test_var_trials_override_is_used():
    """An explicit pin must actually be USED, not silently replaced by 1/n."""
    thr = _thr()
    returns, bench = _edge_matrix(5, 500, 0.20, seed=101)
    ids = [f"c{i}" for i in range(5)]
    v_default = ug.run_universe_gate(returns=returns, benchmark=bench, candidate_ids=ids,
                                     cumulative_k=3200, thresholds=thr, seed=101,
                                     run_pbo=False)
    v_pinned = ug.run_universe_gate(returns=returns, benchmark=bench, candidate_ids=ids,
                                    cumulative_k=3200, thresholds=thr, seed=101,
                                    var_trials=0.05, run_pbo=False)
    assert v_pinned.detail["var_trials"] == 0.05
    assert v_default.detail["var_trials"] != v_pinned.detail["var_trials"]


def test_var_trials_default_guards_the_ksp1_degenerate_case():
    """At K_SPA=1 the retired empirical estimator collapsed to var_trials=0 -> SR0~=0
    -> DSR trivially ~1. The 1/n default must not reproduce that degeneracy."""
    thr = _thr()
    noise, bench = _edge_matrix(1, 500, 0.0, seed=104)
    ids = ["only_candidate"]

    default_verdict = ug.run_universe_gate(returns=noise, benchmark=bench,
                                           candidate_ids=ids, cumulative_k=3200,
                                           thresholds=thr, seed=104, run_pbo=False)
    assert default_verdict.detail["var_trials"] == pytest.approx(1.0 / 500)

    vacuous = ug.run_universe_gate(returns=noise, benchmark=bench,
                                   candidate_ids=ids, cumulative_k=3200,
                                   thresholds=thr, seed=104, run_pbo=False,
                                   var_trials=0.0)
    # Vacuous V=0 produces a near-1 DSR on noise; 1/n must sit strictly below it.
    assert default_verdict.dsr < vacuous.dsr


def test_self_test_var_trials_forwarded():
    """self_test() forwards var_trials through to run_universe_gate so a campaign can
    calibrate its FROZEN V-rule, not just the module's out-of-the-box default."""
    thr = _thr()
    default_res = ug.self_test(thresholds=thr)
    pinned_res = ug.self_test(thresholds=thr, var_trials=1.0 / 100)
    assert pinned_res["negative"].detail["var_trials"] == 1.0 / 100
    assert pinned_res["positive"].detail["var_trials"] == 1.0 / 100
    assert pinned_res["negative"].promote is False
    assert pinned_res["positive"].promote is True
    # self_test controls use n_trades=300, so the default is 1/300.
    assert default_res["positive"].detail["var_trials"] == pytest.approx(1.0 / 300)
