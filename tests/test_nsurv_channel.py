"""N-SURV candidate-P&L channel — unit + W1 known-answer pin proof."""
from __future__ import annotations

import json
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pytest

from discovery.prop_survivor_scoring import load_scoring_thresholds
from research_utils import nsurv_channel as ns

REPO = Path(__file__).resolve().parents[1]
# v1 — CLOSED 2026-08-26 (its own head banner), superseded by
# 2026-08-26-prop-survivor-scoring-prereg-v2.md: the LIVE Part A eval bust
# ceiling is 5.0%, not the 3.0% pinned below. This fixture deliberately stays on
# v1 so the loader keeps regression-testing v1's frozen 3.0% text forever,
# independent of whichever file DEFAULT_PREREG points at (Trap #12 — v1's own
# numbers are never edited in place, so this pin never needs to change). The
# StaleGateWarning these calls emit is expected and is the point.
PREREG_V1 = REPO / "docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md"
W1_DIR = REPO / "lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16"
W1_REPORT = W1_DIR / "w1_intraday_both_halves_report.json"
W1_RESULTS_MD = W1_DIR / "RESULTS_INTRADAY_W1.md"

_TEST_SIMS = 40
_TEST_HORIZON = 400


def _thr():
    return replace(load_scoring_thresholds(PREREG_V1), horizon=_TEST_HORIZON)


def _synthetic_frame(n: int = 80, *, seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2020-01-06", periods=n)
    pnl = rng.normal(20.0, 180.0, size=n)
    deep = pnl - np.abs(rng.normal(350.0, 150.0, size=n))
    low = np.minimum(0.0, deep)
    return pd.DataFrame(
        {
            "date": dates,
            "pnl_usd": pnl.astype(float),
            "intraday_low": low.astype(float),
        }
    )


# ── threshold edges (frozen prereg inequality directions) ─────────────────────


def test_threshold_edges_non_strict_bust_le_and_pass_ge():
    """**v1**'s frozen Part A: bust ≤ 3.0% ∧ P(pass) ≥ 50% — both bounds
    inclusive. 3.0% is v1's HISTORICAL ceiling; the live Part A ceiling is **5.0%**
    (prereg v2, 2026-08-26). What this test pins is the inequality *direction* and
    inclusivity, which v2 did not change — not the number itself."""
    thr = load_scoring_thresholds(PREREG_V1)
    assert thr.eval_bust_ceiling == pytest.approx(0.03)
    assert thr.pass_floor == pytest.approx(0.50)

    # Exact ceiling / floor → PASS
    assert ns.clears_nsurv_floor(0.03, 0.50, thr) is True
    # Just inside → PASS
    assert ns.clears_nsurv_floor(0.029999, 0.500001, thr) is True
    # Bust strict-over → FAIL even with strong pass
    assert ns.clears_nsurv_floor(0.0300001, 0.99, thr) is False
    # Pass strict-under → FAIL even with tiny bust
    assert ns.clears_nsurv_floor(0.0, 0.499999, thr) is False


# ── load / split / shape ──────────────────────────────────────────────────────


def test_load_csv_and_json_roundtrip(tmp_path: Path):
    frame = _synthetic_frame(20)
    csv_path = tmp_path / "c.csv"
    json_path = tmp_path / "c.json"
    frame.to_csv(csv_path, index=False)
    json_path.write_text(
        json.dumps(
            [
                {
                    "date": r.date.date().isoformat(),
                    "pnl_usd": float(r.pnl_usd),
                    "intraday_low": float(r.intraday_low),
                }
                for r in frame.itertuples(index=False)
            ]
        ),
        encoding="utf-8",
    )
    a = ns.load_candidate_daily_pnl(csv_path)
    b = ns.load_candidate_daily_pnl(json_path)
    assert len(a) == len(b) == 20
    assert list(a.columns) == ["date", "pnl_usd", "intraday_low"]
    assert np.allclose(a["pnl_usd"], b["pnl_usd"])


def test_split_at_boundary_h1_before_h2_from():
    frame = _synthetic_frame(10)
    boundary = frame["date"].iloc[5]
    h1, h2 = ns.split_at_boundary(frame, boundary)
    assert len(h1) == 5 and len(h2) == 5
    assert h1["date"].max() < pd.Timestamp(boundary)
    assert h2["date"].min() == pd.Timestamp(boundary)


def test_score_requires_intraday_low():
    frame = _synthetic_frame(40).drop(columns=["intraday_low"])
    with pytest.raises(ValueError, match="intraday_low"):
        ns.score_nsurv(
            frame,
            half_boundary_date=frame["date"].iloc[20],
            thresholds=_thr(),
            n_sims=_TEST_SIMS,
        )


# ── engine invocation + output shape (synthetic, mocked remc) ─────────────────


def test_synthetic_invokes_engine_three_partitions_and_output_shape(monkeypatch):
    """Channel must call the W1 engine path (run_tier_remc) once per partition."""
    frame = _synthetic_frame(60)
    boundary = frame["date"].iloc[30]
    calls: list[dict[str, Any]] = []

    def _fake_remc(firm_key, blocks, thresholds, *, n_sims=None, consistency=None, intraday_blocks=None):
        calls.append(
            {
                "firm_key": firm_key,
                "blocks_shape": getattr(blocks, "shape", None),
                "intraday": intraday_blocks is not None,
                "consistency": consistency,
                "n_sims": n_sims,
            }
        )
        # Distinct rates so floor_ok differs if we want; keep all clearing.
        return {
            "firm_key": firm_key,
            "consistency": consistency,
            "n_sims": n_sims or thresholds.sims_per_seed,
            "headline_bust": 0.01,
            "pass_rate": 0.80,
            "intraday_low": intraday_blocks is not None,
        }

    monkeypatch.setattr(ns, "run_tier_remc", _fake_remc)
    # paired_blocks_from_daily must still run for real shape; leave it.

    report = ns.score_nsurv(
        frame,
        half_boundary_date=boundary,
        thresholds=_thr(),
        n_sims=_TEST_SIMS,
    )
    assert len(calls) == 3
    assert all(c["firm_key"] == ns.DEFAULT_FIRM_KEY for c in calls)
    assert all(c["intraday"] is True for c in calls)
    assert all(c["consistency"] == pytest.approx(0.40) for c in calls)

    assert report.nsurv == "PASS"
    assert report.nsurv_line == "N-SURV PASS"
    assert report.full.floor_ok and report.h1.floor_ok and report.h2.floor_ok
    assert report.full.intraday_low is True
    d = report.to_dict()
    assert set(d) >= {
        "firm_key",
        "full",
        "H1",
        "H2",
        "nsurv",
        "nsurv_line",
        "eval_bust_ceiling",
        "pass_floor",
    }
    block = report.format_block()
    assert "N-SURV PASS" in block
    assert "full:" in block and "H1:" in block and "H2:" in block


def test_nsurv_fail_when_any_half_misses(monkeypatch):
    frame = _synthetic_frame(60)
    boundary = frame["date"].iloc[30]
    busts = iter([0.01, 0.01, 0.05])  # H2 busts over ceiling

    def _fake_remc(firm_key, blocks, thresholds, *, n_sims=None, consistency=None, intraday_blocks=None):
        return {
            "firm_key": firm_key,
            "consistency": consistency,
            "n_sims": n_sims or 40,
            "headline_bust": next(busts),
            "pass_rate": 0.90,
            "intraday_low": True,
        }

    monkeypatch.setattr(ns, "run_tier_remc", _fake_remc)
    report = ns.score_nsurv(
        frame,
        half_boundary_date=boundary,
        thresholds=_thr(),
        n_sims=_TEST_SIMS,
    )
    assert report.nsurv == "FAIL"
    assert report.h2.floor_ok is False
    assert report.full.floor_ok is True


def test_live_synthetic_engine_path_smoke():
    """Unmocked tiny remc — proves channel → paired_blocks → run_tier_remc wiring."""
    frame = _synthetic_frame(40)
    # Amplify excursions so the honest clock is non-vacuous under Tradeify geometry.
    frame = frame.copy()
    frame["intraday_low"] = np.minimum(frame["intraday_low"], -3_500.0)
    boundary = frame["date"].iloc[20]
    report = ns.score_nsurv(
        frame,
        half_boundary_date=boundary,
        thresholds=_thr(),
        n_sims=_TEST_SIMS,
    )
    assert report.firm_key == "Tradeify_Select_100K"
    assert report.full.n_sims == _TEST_SIMS
    assert report.full.intraday_low is True
    assert report.nsurv in ("PASS", "FAIL")
    assert "N-SURV" in report.nsurv_line


# ── W1 known-answer pin proof ─────────────────────────────────────────────────


def _quote_w1_tradeify_pins() -> dict:
    """Targets = artifact's own numbers (RESULTS_INTRADAY_W1 / report JSON)."""
    assert W1_RESULTS_MD.is_file()
    text = W1_RESULTS_MD.read_text(encoding="utf-8")
    # Sanity: RESULTS table still carries the published Tradeify line.
    assert "Tradeify_Select_100K" in text
    assert "0.72%" in text and "99.20%" in text
    pins = ns.w1_published_pins("Tradeify_Select_100K")
    # Cross-check report floats against the RESULTS display rounding.
    assert pins["full"]["headline_bust"] == pytest.approx(0.007233333333333334)
    assert pins["full"]["pass_rate"] == pytest.approx(0.992)
    assert pins["H1"]["headline_bust"] == pytest.approx(0.0177)
    assert pins["H1"]["pass_rate"] == pytest.approx(0.9507666666666666)
    assert pins["H2"]["headline_bust"] == pytest.approx(0.0028333333333333335)
    assert pins["H2"]["pass_rate"] == pytest.approx(0.9971666666666666)
    return pins


_DEPTH_RELATIVE_ROOT = "_ROOT = _HERE.parents[3]"


def _pin_materialized_repo_root(path: Path) -> None:
    """Rewrite depth-relative ``_ROOT`` so a tmp_path copy still finds the repo.

    The historical harness is correct at ``lab/analysis/c1/<slug>/`` (parents[3]
    = repo). Under pytest tmp_path that index no longer reaches the repo, so
    ``from reconcile import …`` and the ``_ROOT``-derived prereg / ``CME_DIR``
    paths all miss. Injecting ``sys.path`` in the test process would clear the
    import but leave ``phase0_verify`` / ``resolve_panel_path`` pointed at the
    wrong tree — pin ``_ROOT`` itself at materialization time.
    """
    text = path.read_text(encoding="utf-8")
    if _DEPTH_RELATIVE_ROOT not in text:
        raise AssertionError(
            f"{path.name} missing {_DEPTH_RELATIVE_ROOT!r}; "
            "materialized _ROOT pin is stale"
        )
    pinned = f"_ROOT = Path({str(REPO)!r})"
    path.write_text(
        text.replace(_DEPTH_RELATIVE_ROOT, pinned, 1), encoding="utf-8"
    )


def _materialize_pruned_scoring_helpers(tmp_path: Path) -> Path:
    """W1 rebuild needs pruned campaign helpers; pull bytes from git history only."""
    import subprocess

    dest = tmp_path / "w1_rebuild_helpers"
    dest.mkdir()
    scoring_dir = "lab/analysis/c1/class_s_candidate1_scoring_2026-07-15"
    # Parent of the great-prune commit that dropped the harnesses.
    # The public seed starts at the initial-release commit — that ancestry
    # (and the deleted harness blob) lives only in first-passage-archive.
    try:
        tip = subprocess.check_output(
            [
                "git",
                "log",
                "-1",
                "--format=%H",
                "--diff-filter=D",
                "--",
                f"{scoring_dir}/run_class_s_c1_scoring.py",
            ],
            cwd=REPO,
            text=True,
        ).strip()
    except subprocess.CalledProcessError as exc:
        pytest.skip(
            "pruned W1 harness not in git ancestry "
            f"(public seed has no pre-transition history): {exc}"
        )
    if not tip:
        pytest.skip(
            "pruned W1 harness not in git ancestry "
            "(public seed has no pre-transition history)"
        )
    try:
        parent = subprocess.check_output(
            ["git", "rev-parse", f"{tip}^"],
            cwd=REPO,
            text=True,
        ).strip()
    except subprocess.CalledProcessError:
        pytest.skip(
            "not enough git ancestry to materialize pruned W1 helpers "
            "(public seed starts at the initial release commit)"
        )
    for name in (
        "run_class_s_c1_scoring.py",
        "run_class_s_c1_regime_gate.py",
    ):
        try:
            blob = subprocess.check_output(
                ["git", "show", f"{parent}:{scoring_dir}/{name}"],
                cwd=REPO,
            )
        except subprocess.CalledProcessError as exc:
            pytest.skip(
                f"pruned W1 helper {name} not in git ancestry: {exc}"
            )
        dest_file = dest / name
        dest_file.write_bytes(blob)
        _pin_materialized_repo_root(dest_file)
    return dest


def test_materialized_w1_helpers_bind_real_repo_root(tmp_path: Path):
    """tmp_path copy must import against the real repo, not __file__.parents[3]."""
    import importlib.util

    helpers = _materialize_pruned_scoring_helpers(tmp_path)
    pinned = f"_ROOT = Path({str(REPO)!r})"
    for name in ("run_class_s_c1_scoring.py", "run_class_s_c1_regime_gate.py"):
        text = (helpers / name).read_text(encoding="utf-8")
        assert pinned in text
        assert _DEPTH_RELATIVE_ROOT not in text

    spec = importlib.util.spec_from_file_location(
        "w1_materialized_scoring_probe", helpers / "run_class_s_c1_scoring.py"
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert Path(mod._ROOT) == REPO
    assert (mod._RECONCILE / "reconcile.py").is_file()
    assert callable(mod.load_csv) and callable(mod.pin_r_basis)


def _rebuild_w1_arm_series(helpers_dir: Path) -> tuple[pd.DataFrame, str]:
    """Rebuild the 0.50× daily + intraday series W1 scored (campaign inputs)."""
    # Import W1 runner pieces without editing the campaign dir.
    sys.path.insert(0, str(helpers_dir))
    sys.path.insert(0, str(W1_DIR))
    try:
        import run_class_s_c1_scoring as S  # type: ignore  # noqa: WPS433
        import run_w1_intraday_both_halves as W1  # type: ignore  # noqa: WPS433
    finally:
        # Leave paths for subsequent imports in this process; tests are process-local.
        pass

    S.phase0_verify()
    for leg in S.C1_STRATS:
        S.resolve_panel_path(leg)
    panel, meta, _ = S.build_scaled_panel(
        S.C1_STRATS, S.C1_ALLOCS, expect_1r=dict(S.EXPECTED_1R)
    )
    daily = S.book_daily_at_100k(panel)
    intraday, _cov = W1.build_book_intraday_low(panel, meta)
    assert len(intraday) == len(daily)
    # Lifecycle haircut co-moves both channels (W1 ARM_MULT); not dd_scale.
    dh = np.asarray(daily, dtype=float) * float(W1.ARM_MULT)
    ih = np.asarray(intraday, dtype=float) * float(W1.ARM_MULT)
    # Calendar from panel index (business days); boundary = mid date (H2 starts).
    bdays = pd.DatetimeIndex(panel.index).tz_localize(None).normalize()
    mid = len(bdays) // 2
    boundary = bdays[mid].date().isoformat()
    frame = pd.DataFrame(
        {
            "date": bdays,
            "pnl_usd": dh,
            "intraday_low": ih,
        }
    )
    return frame, boundary


def test_w1_pin_reproduction_known_answer(tmp_path: Path):
    """Drive the channel with W1's own inputs; reproduce published pins EXACTLY.

    Skip when gitignored vendor panels / 15m bars are absent (repo convention).
    """
    pins = _quote_w1_tradeify_pins()
    ok, missing = ns.w1_panel_inputs_present()
    if not ok:
        pytest.skip(
            "W1 vendor panels/bars absent (gitignored); pin reproduction not executed. "
            f"missing={missing}"
        )

    helpers = _materialize_pruned_scoring_helpers(tmp_path)
    frame, boundary = _rebuild_w1_arm_series(helpers)
    assert len(frame) == pins["panel_n_bdays"]

    # Full frozen prereg sims/horizon — exact pin match requires production posture.
    thr = load_scoring_thresholds(PREREG_V1)
    report = ns.score_nsurv(
        frame,
        half_boundary_date=boundary,
        firm_key="Tradeify_Select_100K",
        thresholds=thr,
        n_sims=None,
    )

    assert report.full.headline_bust == pins["full"]["headline_bust"]
    assert report.full.pass_rate == pins["full"]["pass_rate"]
    assert report.h1.headline_bust == pins["H1"]["headline_bust"]
    assert report.h1.pass_rate == pins["H1"]["pass_rate"]
    assert report.h2.headline_bust == pins["H2"]["headline_bust"]
    assert report.h2.pass_rate == pins["H2"]["pass_rate"]
    assert report.nsurv == "PASS"
    assert pins["gate_pass_full_and_halves"] is True
