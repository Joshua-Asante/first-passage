"""W5 gate-manifest runner — composition loads and selects without dropping gates."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "gate_manifest.py"
MANIFEST = REPO / "scripts" / "gates.yml"

EXPECTED_ALWAYS = {
    "skills-no-constants",
    "skill-refs",
    "pine-manifest",
    "pine-pin-provenance",
    "boundaries",
    "path-liveness",
    "root-doc-liveness",
    "status-consistency",
    "adr-graph",
    "lab-catalog",
    "instrument-profiles",
    "sessions-order",
    "sessions-append-only",
    "supersession-placement",
    "closure-disposition",
}


def test_manifest_lists_all_always_gates():
    out = subprocess.check_output(
        [sys.executable, str(SCRIPT), "--list"],
        cwd=REPO,
        text=True,
    )
    for gid in EXPECTED_ALWAYS:
        assert gid in out, f"missing gate {gid}"
    assert "data-manifests" in out


def test_pre_commit_dry_run_includes_always_gates():
    out = subprocess.check_output(
        [sys.executable, str(SCRIPT), "--tier", "pre-commit", "--dry-run"],
        cwd=REPO,
        text=True,
    )
    for gid_cmd_fragment in (
        "check_skills_no_constants.py",
        "check_skill_refs.py",
        "check_pine_manifest.py",
        "check_boundaries.py",
        "check_adr_graph.py",
        "check_closure_disposition.py",
    ):
        assert gid_cmd_fragment in out


def test_validate_tier_is_data_plus_pine():
    out = subprocess.check_output(
        [sys.executable, str(SCRIPT), "--tier", "validate", "--dry-run"],
        cwd=REPO,
        text=True,
    )
    assert "check_data_manifests.py" in out
    assert "check_pine_manifest.py" in out
    assert "check_boundaries.py" not in out


def test_manifest_file_present():
    assert MANIFEST.is_file()


def test_reindented_gate_fails_closed(tmp_path):
    """A re-indented `- id:` must abort the run, not silently shrink the battery.

    Regression for the fail-open parse found 2026-08-08: `_parse_gates_yml` matches
    `^  - id:` exactly, so one extra space dropped a gate AND its argv while the
    runner still exited 0 — enforcing less than gates.yml declares, invisibly.

    Adversarial control below: the same manifest with correct indentation must PASS,
    so the test cannot pass vacuously on an unrelated parse error.
    """
    good = (
        "version: 1\n"
        "gates:\n"
        "  - id: alpha\n"
        "    tier: always\n"
        "    cmd:\n"
        "      - python\n"
        "      - -c\n"
        "      - pass\n"
        "  - id: beta\n"
        "    tier: always\n"
        "    cmd:\n"
        "      - python\n"
        "      - -c\n"
        "      - pass\n"
    )
    # One stray leading space on the SECOND gate — the shape that bit us.
    bad = good.replace("  - id: beta", "   - id: beta")

    good_path = tmp_path / "gates_good.yml"
    good_path.write_text(good, encoding="utf-8")
    bad_path = tmp_path / "gates_bad.yml"
    bad_path.write_text(bad, encoding="utf-8")

    def run(manifest: Path) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--list", "--manifest", str(manifest)],
            capture_output=True, text=True, cwd=REPO,
        )

    ok = run(good_path)
    assert ok.returncode == 0, f"control manifest should load cleanly: {ok.stderr}"
    assert "beta" in ok.stdout

    bad = run(bad_path)
    assert bad.returncode != 0, "re-indented gate was silently dropped (fail-open)"
    combined = bad.stdout + bad.stderr
    assert "mismatch" in combined.lower(), combined
