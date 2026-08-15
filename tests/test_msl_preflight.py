"""Acceptance anchors for MSL P2 W-A msl_preflight (evidence-only CLI)."""
from __future__ import annotations

import json
import math
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

from research_utils import msl_preflight as mp

REPO = Path(__file__).resolve().parents[1]
FIXTURES = REPO / "lab" / "research_utils" / "fixtures" / "msl_preflight"


def _run_cli(card: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    roots = [str(REPO / d) for d in ("core", "lab", "ops", "governance")]
    prev = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = os.pathsep.join(roots + ([prev] if prev else []))
    return subprocess.run(
        [sys.executable, "-m", "research_utils.msl_preflight", str(card), *extra],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        check=False,
    )


def test_formula_pin_fade_region_2_98():
    """Umbrella section 0 / 0.5 q8: p=0.654, rr=0.66, n=3 -> round(implied, 2) == 2.98."""
    implied = mp.implied_annualized_sr(0.654, 0.66, 3)
    assert round(implied, 2) == pytest.approx(2.98, abs=0.01)


def test_registry_hit_surfaces_in_dedup():
    card = FIXTURES / "registry_hit.yaml"
    report = mp.preflight(card, repo_root=REPO)
    blob = "\n".join(report.dedup_hits)
    assert "Guardian-on-XAGUSD" in blob
    text = mp.format_report(report)
    assert "Guardian-on-XAGUSD" in text
    assert "--- dedup ---" in text


def test_mes_barred_emits_binding_bar():
    card = FIXTURES / "mes_barred.yaml"
    report = mp.preflight(card, repo_root=REPO)
    assert "BINDING BAR:" in report.cell_stdout
    text = mp.format_report(report)
    assert "BINDING BAR:" in text


def test_fade_region_implied_sr_in_arithmetic_table():
    card = FIXTURES / "fade_region.yaml"
    report = mp.preflight(card, repo_root=REPO)
    implied = report.arithmetic["implied_annualized_sr"]
    assert implied == pytest.approx(2.98, abs=0.01)
    text = mp.format_report(report)
    assert re.search(r'"implied_annualized_sr":\s*2\.98', text)


def test_clean_card_round_trip_structured_keys():
    card = FIXTURES / "clean_card.yaml"
    report = mp.preflight(card, repo_root=REPO)
    assert report.card_id == "clean-card-roundtrip"
    assert report.disclaimer == mp.TOOLING_DISCLAIMER
    assert "implied_annualized_sr" in report.arithmetic
    assert report.arithmetic["payability"] is not None
    assert report.arithmetic["worst_day"] is not None
    assert report.arithmetic["sigma_d"] is not None
    text = mp.format_report(report)
    for key in ("--- dedup ---", "--- instrument cell ---", "--- arithmetic ---"):
        assert key in text


def test_cli_exits_zero_even_when_bars_present():
    """Surfacing is not killing: MES bars make cell returncode 1; CLI still exits 0."""
    proc = _run_cli(FIXTURES / "mes_barred.yaml")
    assert proc.returncode == 0, proc.stderr
    assert "BINDING BAR:" in proc.stdout


def test_cli_json_mode_round_trip():
    proc = _run_cli(FIXTURES / "fade_region.yaml", "--json")
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["arithmetic"]["implied_annualized_sr"] == pytest.approx(2.98, abs=0.01)
    assert payload["disclaimer"] == mp.TOOLING_DISCLAIMER


def test_module_has_no_adjudication_api():
    """Fleet audit hook: no PASS/KILL/route_verdict/adjudicat in the module source."""
    src = (REPO / "lab" / "research_utils" / "msl_preflight.py").read_text(encoding="utf-8")
    for needle in ("PASS", "KILL", "route_verdict", "adjudicat"):
        assert needle not in src, f"forbidden adjudication token {needle!r} in module"


def test_expectancy_and_sharpe_helpers_match_design_law():
    p, rr, n = 0.654, 0.66, 3
    exp = mp.expectancy_r(p, rr)
    assert exp == pytest.approx(p * rr - (1.0 - p))
    pts = mp.per_trade_sharpe(p, rr)
    assert pts == pytest.approx(exp / (math.sqrt(p * (1.0 - p)) * (1.0 + rr)))
    assert mp.implied_annualized_sr(p, rr, n) == pytest.approx(
        pts * math.sqrt(n) * math.sqrt(252)
    )
