"""W5 gate-manifest runner — composition loads and selects without dropping gates."""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "gate_manifest.py"
MANIFEST = REPO / "scripts" / "gates.yml"
_SPEC = importlib.util.spec_from_file_location("gate_manifest", SCRIPT)
gm = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = gm
_SPEC.loader.exec_module(gm)

EXPECTED_ALWAYS = {
    "skills-no-constants",
    "skill-refs",
    "pine-manifest",
    "pine-pin-provenance",
    "boundaries",
    # 2026-08-15 (governance-belt audit action 3): reverted from
    # path-conditional -- both gates detect dead links, and a link target
    # can be moved/deleted without touching the file that points at it, so
    # no staged_regex correctly scopes "when this violation can occur".
    "path-liveness",
    "root-doc-liveness",
    # Task 3 (docs/adr/2026-08-27-ssot-data-lineage-remediation-program.md
    # Phase 1) — Q-M1WIRE-1 tree-skew checker wiring; report-only, cheap.
    "m1-tree-skew",
    # Task 1 (same ADR) — ADR-cited skill-script deploy-drift check; cheap
    # (grep + existence check), so `always` rather than path-conditional.
    # 2026-08-28 review fix: this entry was missing here even though the
    # gate had already landed in gates.yml (commit ef7df14 added
    # m1-tree-skew to this set but not this one, landed the same window) —
    # a membership-only test let the drift go unnoticed; see the
    # set-equality assertion added to test_manifest_lists_all_always_gates
    # below to guard against a repeat.
    "skill-deploy-sync",
    # Task 4 (same ADR) — falsifier-reachability coverage census, report-only
    # (`--stats` alone always exits 0 per the script's own docstring).
    "falsifier-reachability-census",
}

EXPECTED_PATH_CONDITIONAL = {
    "status-consistency",
    "adr-graph",
    "lab-catalog",
    "instrument-profiles",
    "sessions-order",
    "sessions-append-only",
    "sessions-queue-bind",
    "supersession-placement",
    "closure-disposition",
    "governance-prose-control-chars",
    "sync-liveness",
    "docs-runtime-inventory",
    "repo-map-layers",
    "lifecycle-consistency",
    # Task 2 (same ADR) — D4 rejection-ledger-coverage instrument
    # (commit 4472abb) landed this gate without adding it here, which left
    # test_path_conditional_gates_are_reachable failing on this worktree
    # before this Task 3 edit touched the same file; folded in alongside
    # Task 3's own addition rather than leaving a known-red test in a file
    # this commit already modifies.
    "instrument-rejection-coverage",
}


def test_manifest_lists_all_always_gates():
    out = subprocess.check_output(
        [sys.executable, str(SCRIPT), "--list"],
        cwd=REPO,
        text=True,
    )
    for gid in EXPECTED_ALWAYS | EXPECTED_PATH_CONDITIONAL:
        assert gid in out, f"missing gate {gid}"
    assert "data-manifests" in out
    assert "path-conditional" in out

    # 2026-08-28 review fix: set-equality, not just membership. Membership
    # alone lets a NEW always-tier gate land in gates.yml without this list
    # ever being updated — gates.yml grew from 8 to 10 always-tier gates
    # (skill-deploy-sync, falsifier-reachability-census) while EXPECTED_ALWAYS
    # silently stayed at 8. Mirrors the set-equality style
    # test_path_conditional_gates_are_reachable already applies below to
    # EXPECTED_PATH_CONDITIONAL.
    data = gm.load_manifest(MANIFEST)
    always_ids = {g["id"] for g in data["gates"] if g.get("tier") == "always"}
    assert always_ids == EXPECTED_ALWAYS, (
        "an always-tier gate was added/removed in gates.yml without updating "
        "EXPECTED_ALWAYS in this test"
    )


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
        "check_path_liveness.py",
        "check_root_doc_liveness.py",
    ):
        assert gid_cmd_fragment in out


def test_pre_commit_skips_path_conditional_when_index_empty(monkeypatch):
    monkeypatch.setattr(gm, "staged_names", lambda: [])
    data = gm.load_manifest(MANIFEST)
    selected = {g["id"] for g in gm.select_gates(data["gates"], "pre-commit")}
    assert EXPECTED_ALWAYS <= selected
    assert selected.isdisjoint(EXPECTED_PATH_CONDITIONAL)


def test_pre_commit_includes_path_conditional_on_matching_paths(monkeypatch):
    monkeypatch.setattr(gm, "staged_names", lambda: ["docs/briefs/INDEX.md"])
    data = gm.load_manifest(MANIFEST)
    selected = {g["id"] for g in gm.select_gates(data["gates"], "pre-commit")}
    assert "closure-disposition" in selected
    assert "sync-liveness" in selected
    assert "sessions-order" not in selected


def test_check_tier_dry_run_includes_path_conditional():
    """make check still runs path-conditional gates — diet is when, not whether."""
    out = subprocess.check_output(
        [sys.executable, str(SCRIPT), "--tier", "check", "--dry-run"],
        cwd=REPO,
        text=True,
    )
    for gid_cmd_fragment in (
        "check_skills_no_constants.py",
        "check_closure_disposition.py",
        "check_adr_graph.py",
        "check_data_manifests.py",
    ):
        assert gid_cmd_fragment in out


def test_check_tier_selects_ci_composition_ids():
    """CI gate-manifest.yml calls --tier check; every always/path-conditional
    id plus forced data-manifests must be selected. pursuit-records was
    retired from gates.yml entirely 2026-08-24 (Rule 16 R5 — the underlying
    check always exits 0 as invoked, so it could never fail regardless of
    tier); this assertion now holds vacuously and is kept as a regression
    guard against re-adding it as a --tier check member.
    """
    data = gm.load_manifest(MANIFEST)
    selected = {g["id"] for g in gm.select_gates(data["gates"], "check")}
    assert EXPECTED_ALWAYS <= selected
    assert EXPECTED_PATH_CONDITIONAL <= selected
    assert "data-manifests" in selected
    assert "pursuit-records" not in selected


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


# 2026-08-15 (governance-belt audit action 3): reachability, not just
# selector shape. path-liveness/root-doc-liveness were path-conditional with
# regexes that never matched lab/|core/|ops/ -- the LINK could be edited
# without tripping the gate, but the link TARGET could be moved or deleted
# out from under it and the gate never ran. For each gate still
# path-conditional, assert that staging a path whose edit can actually cause
# the violation the gate detects is enough to select it -- not merely that
# the selector runs without crashing.
REACHABILITY_PROBES = {
    "status-consistency": "lab/CATALOG.md",
    "adr-graph": "docs/adr/2026-01-01-example.md",
    "lab-catalog": "lab/analysis/harvest/new_slug_2026-08/RESULTS.md",
    "instrument-profiles": "ops/instruments/MNQ.md",
    "sessions-order": "docs/SESSIONS.md",
    "sessions-append-only": "docs/SESSIONS.md",
    "sessions-queue-bind": "docs/SESSIONS.md",
    "supersession-placement": "lab/analysis/harvest/new_slug_2026-08/RESULTS.md",
    "closure-disposition": "docs/briefs/closures/Q-EXAMPLE-closure-falsified.md",
    "governance-prose-control-chars": "docs/rejected_candidates.md",
    "sync-liveness": "docs/briefs/INDEX.md",
    "docs-runtime-inventory": "ops/c1_rail/c1_rail_arm.py",
    "repo-map-layers": "scripts/check_boundaries.py",
    "lifecycle-consistency": "core/lifecycle.py",
    "instrument-rejection-coverage": "docs/briefs/closures/Q-EXAMPLE-closure-falsified.md",
}


def test_path_conditional_gates_are_reachable(monkeypatch):
    data = gm.load_manifest(MANIFEST)
    conditional_ids = {
        g["id"] for g in data["gates"] if g.get("tier") == "path-conditional"
    }
    assert conditional_ids == EXPECTED_PATH_CONDITIONAL, (
        "a path-conditional gate was added/removed without updating this "
        "test's reachability probe table"
    )
    for gate_id, probe_path in REACHABILITY_PROBES.items():
        monkeypatch.setattr(gm, "staged_names", lambda p=probe_path: [p])
        selected = {g["id"] for g in gm.select_gates(data["gates"], "pre-commit")}
        assert gate_id in selected, (
            f"{gate_id}'s staged_regex does not match {probe_path!r} -- a "
            "change there cannot trigger this gate at pre-commit"
        )


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


def test_m1_tree_skew_stays_report_only():
    """Pins the deliberate report-only design choice gates.yml's own comment
    above `m1-tree-skew` documents: `--check-tree-skew`, never
    `--require-tree-current` (whose own --help text says it is "never a
    commit gate", because the pinned-fixture-vs-main drift it would flag is
    normal, not a defect — this worktree shows real drift on 6/6 pinned files
    today). An accidental future flip to the hard-fail flag would recreate
    the exact class of Critical bug fixed alongside this test: a `tier:
    always` gate that hard-fails every commit on a condition the running
    environment cannot satisfy."""
    data = gm.load_manifest(MANIFEST)
    gate = next(g for g in data["gates"] if g["id"] == "m1-tree-skew")
    assert "--check-tree-skew" in gate["cmd"]
    assert "--require-tree-current" not in gate["cmd"]
