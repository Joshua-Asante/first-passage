"""Governance-class membership for the two push/session guards.

Both `scripts/check_push_collision.py` and `scripts/session_divergence_hook.py`
carry their own copy of the governance class **on purpose** — the SessionStart hook
must not depend on another module's import graph. Duplication needs a test that
pins them together, which is what this file is.

Widened 2026-08-08: the frozen pre-registration estate lives in five stores while
only `docs/briefs/pre-registration/` was guarded, so 0 of 18 campaign-resident
bodies were covered. The negative controls below are the load-bearing half — a
naive `lab/analysis/` prefix would cover the bodies *and* sweep in every RESULTS
file, harness script and data artifact beside them.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, REPO / rel)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


PUSH = _load("_push_collision", "scripts/check_push_collision.py")
SESSION = _load("_session_divergence", "scripts/session_divergence_hook.py")
GUARDS = pytest.mark.parametrize("guard", [PUSH, SESSION], ids=["push_collision", "session_divergence"])

IN_CLASS = [
    "STATE.md",
    "CLAUDE.md",
    "docs/SESSIONS.md",
    "docs/adr/2026-08-07-w4-minimal-gate-set-dormancy.md",
    "docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md",
    "docs/ltm/briefs/pre-registration/Q-SWAP-2-verdict-preregistration.md",
    "docs/spec/PREREG-NAS-ECR-1-live-edge-capture.md",
    "lab/analysis/c1/mnq_tnec_con2_compression_break_2026-08/PREREG_G0.md",
    "lab/analysis/c1/mnq_ofchan_routeb_2026-08/PREREG_G0.md",
]

OUT_OF_CLASS = [
    # Beside a frozen body, but not one — these are why the match is by basename
    # and not by a `lab/analysis/` prefix.
    "lab/archive/mnq_sr_structure_2026-08-06/RESULTS.md",
    "lab/archive/mnq_r2vbuck_routeb_2026-08/r2vbuck_lib.py",
    "lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/run_probe.py",
    # PREREG in the name but not a markdown body.
    "lab/analysis/regime/NOTES_PREREG_ideas.txt",
    # docs/spec is only in-class under the PREREG- filename prefix.
    "docs/spec/2026-08-07-loop-s1-environment-ratification-spec.md",
    "docs/briefs/INDEX.md",
    "README.md",
]


@GUARDS
@pytest.mark.parametrize("path", IN_CLASS)
def test_in_governance_class(guard, path):
    assert guard._is_governance(path), f"{path} should be governance-class"


@GUARDS
@pytest.mark.parametrize("path", OUT_OF_CLASS)
def test_out_of_governance_class(guard, path):
    assert not guard._is_governance(path), f"{path} must NOT be governance-class"


@GUARDS
def test_twins_agree_on_every_tracked_file(guard):
    """The two copies must classify the whole repo identically, or they have drifted."""
    tracked = subprocess.run(
        ["git", "ls-files"], cwd=REPO, capture_output=True, text=True, check=True
    ).stdout.splitlines()
    disagreements = [
        p for p in tracked
        if PUSH._is_governance(p.strip()) != SESSION._is_governance(p.strip())
    ]
    assert not disagreements, f"guards disagree on {len(disagreements)}: {disagreements[:5]}"


def test_every_live_campaign_prereg_is_covered():
    """Regression for the measured gap: 0 of 18 campaign bodies were guarded."""
    tracked = subprocess.run(
        ["git", "ls-files"], cwd=REPO, capture_output=True, text=True, check=True
    ).stdout.splitlines()
    bodies = [
        p.strip() for p in tracked
        if p.startswith("lab/analysis/")
        and p.strip().endswith(".md")
        and p.strip().rsplit("/", 1)[-1].startswith("PREREG")
    ]
    assert bodies, "no campaign PREREG bodies found — has the layout moved?"
    uncovered = [p for p in bodies if not PUSH._is_governance(p)]
    assert not uncovered, f"{len(uncovered)} campaign prereg bodies unguarded: {uncovered[:5]}"
