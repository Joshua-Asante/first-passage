"""Call-1 σ-harness — synthetic-fixture coverage for Steps 2.1–2.6."""
from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pytest

from discovery.lifecycle_call1.baselines import (
    BaselineDataUnavailable,
    load_baseline_pfs,
)
from discovery.lifecycle_call1.breach_tracker import (
    load_breach_state,
    save_breach_state,
    update_consecutive,
)
from discovery.lifecycle_call1.demote_writer import apply_confirmed_demotion
from discovery.lifecycle_call1.evaluate import MIN_TRADE_COUNT, evaluate_window
from discovery.lifecycle_call1.harness import StrategyInput, run_call1_harness
from discovery.lifecycle_call1.pf_sigma import pf_from_daily_pnl, pf_sigma_from_panel
from lifecycle import STRATEGY_KEYS, autonomous_demote, load_lifecycle_state

REPO = Path(__file__).resolve().parents[1]
BASELINES = (
    REPO / ".claude/skills/trade-csv-reconcile/references/baselines.md"
)
PKG = REPO / "lab/discovery/lifecycle_call1"


# ── Step 2.1 — baselines.md PF loader ─────────────────────────────────────────


def _require_live_baselines():
    """Skip when the public tree holds the redacted placeholder, not PF rows."""
    try:
        return load_baseline_pfs(BASELINES)
    except BaselineDataUnavailable as exc:
        pytest.skip(str(exc))


def test_loader_parses_live_baselines():
    got = _require_live_baselines()
    assert set(got) == set(STRATEGY_KEYS)
    assert sorted(got) == sorted(STRATEGY_KEYS)
    assert got["Guardian"].pf == pytest.approx(3.750)
    assert got["Striker"].pf == pytest.approx(3.373)
    assert got["Striker NAS100"].pf == pytest.approx(3.717)
    assert got["Aegis"].pf == pytest.approx(4.188)
    assert got["Guardian"].line_number >= 1
    assert "baselines.md" in got["Guardian"].source_path


def test_loader_refuses_missing_pepperstone_pf(tmp_path: Path):
    bad = tmp_path / "bad.md"
    bad.write_text(
        "## Guardian Gold v5.5\n\nNo table here.\n\n"
        "## Striker DJ30 v4.5\n\n| Pepperstone | 1 | 2.0 |\n\n"
        "## Striker NAS100 v1\n\n| Pepperstone | 1 | 2.0 |\n\n"
        "## Aegis-Reversion v4.3\n\n| Pepperstone | 1 | 2.0 |\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="refusing to guess"):
        load_baseline_pfs(bad)


def test_loader_signals_skip_on_redacted_placeholder(tmp_path: Path):
    redacted = tmp_path / "redacted.md"
    redacted.write_text(
        "## Guardian Gold v5.5\n\n"
        "Baseline PF/WR/Net/DD/N table: redacted from the public tree.\n\n"
        "## Striker DJ30 v4.5\n\nredacted from the public tree\n\n"
        "## Striker NAS100 v1\n\nredacted from the public tree\n\n"
        "## Aegis-Reversion v4.3\n\nredacted from the public tree\n",
        encoding="utf-8",
    )
    with pytest.raises(BaselineDataUnavailable, match="redacted"):
        load_baseline_pfs(redacted)


def test_loader_refuses_incomplete_keyset(tmp_path: Path):
    bad = tmp_path / "partial.md"
    bad.write_text(
        "## Guardian Gold v5.5\n\n| Pepperstone | 203 | 3.750 |\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="baseline keyset"):
        load_baseline_pfs(bad)


def test_no_baseline_pf_literals_outside_loader_and_tests():
    """§10 audit: PF literals must not appear in harness production code."""
    for path in PKG.rglob("*.py"):
        if path.name.startswith("test") or path.name == "__init__.py":
            continue
        text = path.read_text(encoding="utf-8")
        for lit in ("3.750", "3.373", "3.717", "4.188"):
            assert lit not in text, f"{lit} found in {path.relative_to(REPO)}"


# ── Step 2.2 — pf_sigma computer ──────────────────────────────────────────────


def _mixed_panel(seed: int = 0) -> np.ndarray:
    """Synthetic (n_blocks, days) panel with both wins and losses."""
    rng = np.random.default_rng(seed)
    return rng.normal(loc=5.0, scale=40.0, size=(12, 5))


def test_pf_sigma_deterministic_on_synthetic_panel():
    panel = _mixed_panel(7)
    a = pf_sigma_from_panel(panel, n_draws=40, seed=123)
    b = pf_sigma_from_panel(panel, n_draws=40, seed=123)
    assert a == pytest.approx(b)
    assert a > 0.0


def test_pf_from_daily_all_wins_returns_none_not_inf():
    wins = np.array([10.0, 5.0, 1.0])
    assert pf_from_daily_pnl(wins) is None
    losses = np.array([10.0, -5.0, 1.0])
    assert pf_from_daily_pnl(losses) == pytest.approx(11.0 / 5.0)


def test_pf_sigma_raises_when_all_draws_zero_loss():
    # All-positive panel → every draw skipped → insufficient finite PFs.
    panel = np.ones((6, 4), dtype=float) * 10.0
    with pytest.raises(ValueError, match="insufficient finite PF draws"):
        pf_sigma_from_panel(panel, n_draws=10, seed=1)


def test_pf_sigma_module_does_not_import_mc_state():
    src = (PKG / "pf_sigma.py").read_text(encoding="utf-8")
    # Import lines only — docstrings may discuss the design constraint.
    import_lines = [
        line for line in src.splitlines() if line.lstrip().startswith(("import ", "from "))
    ]
    joined = "\n".join(import_lines)
    for forbidden in ("portfolio_mc", "mc.modes", "mc.simulation", "modes", "simulation"):
        assert forbidden not in joined


# ── Step 2.3 — decay evaluator + AMBIGUOUS ────────────────────────────────────


def test_strict_less_than_boundary_is_clear_not_breach():
    # floor = baseline - k*sigma = 3.0 - 1.0*0.5 = 2.5; sitting on floor → CLEAR
    ev = evaluate_window(rolling_pf=2.5, trade_count=100, baseline_pf=3.0, pf_sigma=0.5)
    assert ev.outcome == "CLEAR"
    assert ev.breached is False
    assert ev.floor == pytest.approx(2.5)


def test_clear_breach_below_floor():
    ev = evaluate_window(rolling_pf=2.49, trade_count=100, baseline_pf=3.0, pf_sigma=0.5)
    assert ev.outcome == "BREACH"
    assert ev.breached is True


def test_thin_trade_count_ambiguous():
    ev = evaluate_window(
        rolling_pf=0.1,
        trade_count=MIN_TRADE_COUNT - 1,
        baseline_pf=3.0,
        pf_sigma=0.5,
    )
    assert ev.outcome == "AMBIGUOUS"
    assert ev.breached is False


def test_none_rolling_pf_ambiguous():
    ev = evaluate_window(rolling_pf=None, trade_count=100, baseline_pf=3.0, pf_sigma=0.5)
    assert ev.outcome == "AMBIGUOUS"
    assert ev.breached is False


def test_evaluator_calls_decay_breach_not_inlined():
    src = (PKG / "evaluate.py").read_text(encoding="utf-8")
    assert "decay_breach(" in src
    # Breach predicate must not be reimplemented (floor display math is fine).
    assert not re.search(r"rolling_pf\s*<", src)
    harness_src = "\n".join(
        p.read_text(encoding="utf-8")
        for p in PKG.glob("*.py")
        if p.name != "__init__.py"
    )
    assert not re.search(r"rolling_pf\s*<\s*\(?\s*baseline", harness_src)


# ── Step 2.4 — consecutive-window tracker ─────────────────────────────────────


def test_two_breaches_reach_count_2():
    state: dict[str, int] = {}
    state = update_consecutive(state, "Guardian", "BREACH")
    state = update_consecutive(state, "Guardian", "BREACH")
    assert state["Guardian"] == 2


def test_breach_clear_breach_resets_then_one():
    state = update_consecutive({}, "Guardian", "BREACH")
    state = update_consecutive(state, "Guardian", "CLEAR")
    state = update_consecutive(state, "Guardian", "BREACH")
    assert state["Guardian"] == 1


def test_breach_ambiguous_breach_ambiguous_is_inert():
    state = update_consecutive({}, "Guardian", "BREACH")
    assert state["Guardian"] == 1
    state = update_consecutive(state, "Guardian", "AMBIGUOUS")
    assert state["Guardian"] == 1
    state = update_consecutive(state, "Guardian", "BREACH")
    assert state["Guardian"] == 2


def test_breach_state_roundtrip(tmp_path: Path):
    path = tmp_path / "breach_state.json"
    save_breach_state({"Guardian": 1, "Aegis": 0}, path)
    assert load_breach_state(path) == {"Guardian": 1, "Aegis": 0}


def test_tracker_never_mentions_lifecycle_state_write():
    src = (PKG / "breach_tracker.py").read_text(encoding="utf-8")
    assert "lifecycle_state.json" not in src or "NOT" in src
    assert "autonomous_demote" not in src


# ── Step 2.5 — tier-demotion writer + WATCH-2 floor ───────────────────────────


def test_authorized_demotes_to_watch1(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    life = tmp_path / "lifecycle_state.json"
    result = apply_confirmed_demotion("Guardian", state_file=life)
    assert result.tier_before == "AUTHORIZED"
    assert result.tier_after == "WATCH-1"
    assert result.demoted is True
    raw = json.loads(life.read_text(encoding="utf-8"))
    assert raw == {"Guardian": "WATCH-1"}


def test_watch2_autonomous_floor_never_auto_retire(tmp_path: Path):
    life = tmp_path / "lifecycle_state.json"
    life.write_text(json.dumps({"Striker": "WATCH-2"}) + "\n", encoding="utf-8")
    result = apply_confirmed_demotion("Striker", state_file=life)
    assert result.tier_before == "WATCH-2"
    assert result.tier_after == "WATCH-2"
    assert result.demoted is False
    assert autonomous_demote("WATCH-2") == "WATCH-2"
    raw = json.loads(life.read_text(encoding="utf-8"))
    assert raw["Striker"] == "WATCH-2"
    assert "RETIRED" not in raw.values()


def test_written_state_roundtrips_load_lifecycle_state(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    import lifecycle as lc

    life = tmp_path / "lifecycle_state.json"
    monkeypatch.setattr(lc, "STATE_FILE", life)
    apply_confirmed_demotion("Aegis", state_file=life)
    reloaded = load_lifecycle_state()
    assert reloaded["Aegis"] == "WATCH-1"


def test_writer_calls_autonomous_demote_applies_no_multiplier():
    src = (PKG / "demote_writer.py").read_text(encoding="utf-8")
    assert "autonomous_demote(" in src
    # No sizing / haircut application.
    assert "* multiplier" not in src
    assert "* lifecycle" not in src
    # TIER_MULTIPLIER may appear for validation only — must not index into sizing.
    assert "TIER_MULTIPLIER[" not in src
    assert "scaled_risk" not in src


# ── Step 2.6 — end-to-end driver ──────────────────────────────────────────────


def _panel_map() -> dict[str, np.ndarray]:
    rng = np.random.default_rng(99)
    return {k: rng.normal(10.0, 40.0, size=(10, 5)) for k in STRATEGY_KEYS}


def test_e2e_two_consecutive_breaches_demotes_one_tier(tmp_path: Path):
    breach = tmp_path / "breach_state.json"
    life = tmp_path / "lifecycle_state.json"
    panel = _panel_map()
    # Drive Guardian well below any plausible floor; others AMBIGUOUS.
    baselines = _require_live_baselines()
    # First window breach (count → 1, no demotion).
    inputs1 = {
        "Guardian": StrategyInput(rolling_pf=0.01, trade_count=100),
        "Striker": StrategyInput(rolling_pf=None, trade_count=0),
        "Aegis": StrategyInput(rolling_pf=None, trade_count=0),
        "Striker NAS100": StrategyInput(rolling_pf=None, trade_count=0),
    }
    r1 = run_call1_harness(
        inputs1,
        panel,
        n_draws=30,
        seed=7,
        baselines_path=BASELINES,
        breach_state_path=breach,
        lifecycle_state_path=life,
    )
    assert r1.strategies["Guardian"].window_result == "BREACH"
    assert r1.strategies["Guardian"].demoted is False
    assert r1.state_file_written is False
    assert not life.exists() or life.read_text(encoding="utf-8").strip() in ("", "{}")

    r2 = run_call1_harness(
        inputs1,
        panel,
        n_draws=30,
        seed=7,
        baselines_path=BASELINES,
        breach_state_path=breach,
        lifecycle_state_path=life,
    )
    assert r2.strategies["Guardian"].demoted is True
    assert r2.strategies["Guardian"].tier_before == "AUTHORIZED"
    assert r2.strategies["Guardian"].tier_after == "WATCH-1"
    assert r2.state_file_written is True
    assert r2.lifecycle_state_delta == {"Guardian": "WATCH-1"}
    raw = json.loads(life.read_text(encoding="utf-8"))
    assert raw["Guardian"] == "WATCH-1"
    # Floor used the parsed baseline, not a harness literal.
    assert r2.strategies["Guardian"].baseline_pf == pytest.approx(baselines["Guardian"].pf)


def test_e2e_all_ambiguous_writes_no_lifecycle_state(tmp_path: Path):
    _require_live_baselines()
    breach = tmp_path / "breach_state.json"
    life = tmp_path / "lifecycle_state.json"
    panel = _panel_map()
    inputs = {
        k: StrategyInput(rolling_pf=None, trade_count=0) for k in STRATEGY_KEYS
    }
    report = run_call1_harness(
        inputs,
        panel,
        n_draws=20,
        seed=3,
        baselines_path=BASELINES,
        breach_state_path=breach,
        lifecycle_state_path=life,
    )
    assert report.state_file_written is False
    assert report.lifecycle_state_delta == {}
    assert not life.exists()
    for s in STRATEGY_KEYS:
        assert report.strategies[s].window_result == "AMBIGUOUS"
        assert report.strategies[s].demoted is False


def test_e2e_watch2_floor_via_harness(tmp_path: Path):
    _require_live_baselines()
    breach = tmp_path / "breach_state.json"
    life = tmp_path / "lifecycle_state.json"
    life.write_text(json.dumps({"Guardian": "WATCH-2"}) + "\n", encoding="utf-8")
    panel = _panel_map()
    inputs = {
        "Guardian": StrategyInput(rolling_pf=0.01, trade_count=100),
    }
    run_call1_harness(
        inputs,
        panel,
        n_draws=20,
        seed=1,
        baselines_path=BASELINES,
        breach_state_path=breach,
        lifecycle_state_path=life,
    )
    run_call1_harness(
        inputs,
        panel,
        n_draws=20,
        seed=1,
        baselines_path=BASELINES,
        breach_state_path=breach,
        lifecycle_state_path=life,
    )
    raw = json.loads(life.read_text(encoding="utf-8"))
    assert raw["Guardian"] == "WATCH-2"
