"""Gate-manifest runner: composition loads and selects without dropping gates."""
from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "gate_manifest.py"
MANIFEST = REPO / "scripts" / "gates.yml"
_SPEC = importlib.util.spec_from_file_location("gate_manifest", SCRIPT)
gm = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = gm
_SPEC.loader.exec_module(gm)

# 2026-11 governance cut: gates.yml keeps only gates that protect code, data
# integrity or the money controls. Set-equality below catches any drift.
EXPECTED_ALWAYS = {
    "pine-manifest",
    "pine-pin-provenance",
    "card-pins",
    "boundaries",
    # Blanket-add rejection for local-only roots and oversize blobs; always,
    # because the violating change is an unrelated add no staged_regex selects.
    "staged-debris",
    # Structural M1 artifact validation (corrupt JSON, bad fields, secrets).
    "m1-artifact-structure",
}

EXPECTED_PATH_CONDITIONAL = {
    "evidence-store",
    "cost-model-closed-world",
    "durable-store-pragmas",
}

EXPECTED_AUDIT: set[str] = set()


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

    # --list is documented (Makefile, AGENTS.md) as the "hard-gate roster" —
    # audit-tier (report-only) diagnostics must not appear by default, or an
    # operator reading that roster sees non-gates mixed into merge enforcement.
    for gid in EXPECTED_AUDIT:
        assert gid not in out, f"audit-tier gate {gid} leaked into default --list"

    all_out = subprocess.check_output(
        [sys.executable, str(SCRIPT), "--list", "--all-tiers"],
        cwd=REPO,
        text=True,
    )
    for gid in EXPECTED_ALWAYS | EXPECTED_PATH_CONDITIONAL | EXPECTED_AUDIT:
        assert gid in all_out, f"missing gate {gid} from --list --all-tiers"

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
        "check_pine_manifest.py",
        "check_boundaries.py",
        "validate_c1_monitoring_acceptance.py",
        "check_staged_debris.py",
    ):
        assert gid_cmd_fragment in out


def test_pre_commit_skips_path_conditional_when_index_empty(monkeypatch):
    monkeypatch.setattr(gm, "staged_names", lambda: [])
    data = gm.load_manifest(MANIFEST)
    selected = {g["id"] for g in gm.select_gates(data["gates"], "pre-commit")}
    assert EXPECTED_ALWAYS <= selected
    assert selected.isdisjoint(EXPECTED_PATH_CONDITIONAL)


def test_pre_commit_includes_path_conditional_on_matching_paths(monkeypatch):
    monkeypatch.setattr(gm, "staged_names", lambda: ["ops/recall/index.py"])
    data = gm.load_manifest(MANIFEST)
    selected = {g["id"] for g in gm.select_gates(data["gates"], "pre-commit")}
    assert "durable-store-pragmas" in selected
    assert "evidence-store" not in selected
    assert "cost-model-closed-world" not in selected


def test_check_tier_dry_run_includes_path_conditional():
    """make check still runs path-conditional gates — diet is when, not whether."""
    out = subprocess.check_output(
        [sys.executable, str(SCRIPT), "--tier", "check", "--dry-run"],
        cwd=REPO,
        text=True,
    )
    for gid_cmd_fragment in (
        "check_boundaries.py",
        "check_durable_store_pragmas.py",
        "check_cost_model_closed_world.py",
        "check_data_manifests.py",
    ):
        assert gid_cmd_fragment in out


@pytest.mark.parametrize("path", [
    "core/instrument_specs.py",
    "lab/discovery/cost_model.py",
    "tests/test_cost_model.py",
    "scripts/check_cost_model_closed_world.py",
])
def test_instrument_owners_trigger_partition_gate(monkeypatch, path):
    monkeypatch.setattr(gm, "staged_names", lambda: [path])
    data = gm.load_manifest(MANIFEST)
    selected = {g["id"] for g in gm.select_gates(data["gates"], "pre-commit")}
    assert "cost-model-closed-world" in selected


def test_check_tier_selects_ci_composition_ids():
    """CI calls --tier check; every always/path-conditional id plus forced
    data-manifests must be selected."""
    data = gm.load_manifest(MANIFEST)
    selected = {g["id"] for g in gm.select_gates(data["gates"], "check")}
    assert EXPECTED_ALWAYS <= selected
    assert EXPECTED_PATH_CONDITIONAL <= selected
    assert "data-manifests" in selected
    assert selected.isdisjoint(EXPECTED_AUDIT)


def test_audit_tier_contains_only_report_only_diagnostics():
    data = gm.load_manifest(MANIFEST)
    selected = {g["id"] for g in gm.select_gates(data["gates"], "audit")}
    assert selected == EXPECTED_AUDIT


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


# Reachability, not just selector shape: for each path-conditional gate, staging a
# path whose edit can cause the violation it detects must select it.
REACHABILITY_PROBES = {
    "evidence-store": "scripts/evidence_store/store.py",
    "cost-model-closed-world": "lab/discovery/cost_model.py",
    "durable-store-pragmas": "ops/recall/index.py",
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
    assert set(REACHABILITY_PROBES) == EXPECTED_PATH_CONDITIONAL
    for gate_id, probe_path in REACHABILITY_PROBES.items():
        monkeypatch.setattr(gm, "staged_names", lambda p=probe_path: [p])
        selected = {g["id"] for g in gm.select_gates(data["gates"], "pre-commit")}
        assert gate_id in selected, (
            f"{gate_id}'s staged_regex does not match {probe_path!r} -- a "
            "change there cannot trigger this gate at pre-commit"
        )


def _top_level_alternatives(pattern: str) -> list[str]:
    """Split ``^(a|b)$`` into ``[^a$, ^b$]``; any other shape stays whole."""
    suffix = "$" if pattern.endswith("$") else ""
    if not (pattern.startswith("^(") and pattern[: len(pattern) - len(suffix)].endswith(")")):
        return [pattern]
    body = pattern[2 : len(pattern) - len(suffix) - 1]
    parts, cur, depth, in_class, escaped = [], "", 0, False, False
    for ch in body:
        if escaped:
            escaped = False
        elif ch == "\\":
            escaped = True
        elif in_class:
            in_class = ch != "]"
        elif ch == "[":
            in_class = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth < 0:  # `^(a)(b)`: the outer parens are not one group
                return [pattern]
        elif ch == "|" and depth == 0:
            parts.append(cur)
            cur = ""
            continue
        cur += ch
    parts.append(cur)
    return [f"^{p}{suffix}" for p in parts]


def test_top_level_alternatives_split():
    assert _top_level_alternatives("^(a[.]md|b/(c|d)/|e[|]f)$") == [
        "^a[.]md$", "^b/(c|d)/$", "^e[|]f$",
    ]
    assert _top_level_alternatives("^lab/x[.]md$") == ["^lab/x[.]md$"]
    assert _top_level_alternatives("^(a)(b|c)") == ["^(a)(b|c)"]


def test_every_staged_regex_alternative_selects_a_tracked_file():
    """A trigger keyed on a retired or absent file can never fire, so edits to
    its live successor go unchecked at pre-commit (2026-10-15: CLAUDE.md after
    the AGENTS.md successor; *DESK_CARD* notes kept out of the public seed)."""
    tracked = subprocess.run(
        ["git", "ls-files"], cwd=REPO, capture_output=True, text=True, check=True
    ).stdout.splitlines()
    data = gm.load_manifest(MANIFEST)
    dead = [
        f"{g['id']}: {alt}"
        for g in data["gates"]
        if g.get("tier") == "path-conditional"
        and (g.get("when") or {}).get("staged_regex")
        for alt in _top_level_alternatives(g["when"]["staged_regex"])
        if not any(re.search(alt, p) for p in tracked)
    ]
    assert dead == [], (
        "staged_regex alternatives that match no tracked file (retarget them at "
        "the live successor or drop them):\n" + "\n".join(dead)
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


TIER_PROBE_MANIFEST = """version: 1

gates:
  - id: alpha
    tier: {tier}
    cmd:
      - python
      - scripts/noop.py
"""


def test_unknown_tier_fails_closed(tmp_path):
    """A tier no selector claims must reject the manifest, not silently disable the gate.

    `soft` was declared in gates.yml's header for months while `select_gates` dropped
    it from every tier — a gate landing as `tier: soft` ran nowhere and nothing said
    so. The 2026-09-04 W5 addendum retired `soft` and added `audit`; this pins the
    trap shut rather than re-narrating it in a comment nobody has to read.
    """
    good_path = tmp_path / "gates_good.yml"
    good_path.write_text(TIER_PROBE_MANIFEST.format(tier="audit"), encoding="utf-8")
    bad_path = tmp_path / "gates_bad.yml"
    bad_path.write_text(TIER_PROBE_MANIFEST.format(tier="soft"), encoding="utf-8")

    def run(manifest: Path) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--list", "--all-tiers", "--manifest", str(manifest)],
            capture_output=True, text=True, cwd=REPO,
        )

    ok = run(good_path)
    assert ok.returncode == 0, f"audit is a known tier: {ok.stderr}"
    assert "alpha" in ok.stdout

    bad = run(bad_path)
    assert bad.returncode != 0, "gate with an unselectable tier loaded (fail-open)"
    combined = (bad.stdout + bad.stderr).lower()
    assert "unknown gate tier" in combined, combined


def test_m1_artifact_structure_stays_blocking():
    """Structural validation (corruption/secrets) must still reject a commit.

    validate_c1_monitoring_acceptance.py's main() runs validate() unconditionally,
    before any --check-tree-skew branch — so the structural half must stay in a
    blocking tier even though the tree-skew drift report (above) does not.
    """
    data = gm.load_manifest(MANIFEST)
    gate = next(g for g in data["gates"] if g["id"] == "m1-artifact-structure")
    assert gate["tier"] == "always"
    assert "--check-tree-skew" not in gate["cmd"]
    assert "scripts/validate_c1_monitoring_acceptance.py" in gate["cmd"]

    selected_check = {g["id"] for g in gm.select_gates(data["gates"], "check")}
    selected_precommit = {g["id"] for g in gm.select_gates(data["gates"], "pre-commit")}
    assert "m1-artifact-structure" in selected_check
    assert "m1-artifact-structure" in selected_precommit
