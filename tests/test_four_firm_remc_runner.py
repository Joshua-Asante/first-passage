"""#715 executor fixes (Codex 4199556582, 4199556590): synthetic inputs only."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "four_firm_runner", REPO / "lab/analysis/c1/four_firm_remc_2026-10/run_four_firm_remc.py")
runner = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(runner)

from discovery.prop_survivor_scoring import load_scoring_thresholds  # noqa: E402

THR = load_scoring_thresholds()
CONSISTENCY = ("Tradeify_Select_100K", "MFFU_Rapid_100K", "BluSky_Premium_100K")


def _run(bust):
    return {"headline_bust": bust, "pass_rate": 1.0 - bust, "rates": {}}


def _report(bust1=0.30, bust2=0.35):
    tiers = {}
    for t in THR.tier_keys:
        if t in CONSISTENCY:
            tiers[t] = {"gated_on": "run2", "run1": _run(bust1), "run2": _run(bust2), "clears_part_a": False}
        else:
            tiers[t] = {"gated_on": "run1_degenerate", "run1": _run(bust1), "run2": _run(bust1), "clears_part_a": False}
    return {"tiers": tiers, "gate_grade": True, "halted_at": None,
            "thresholds_source": "docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md"}


PREP = {"g2_killed_tiers": [], "mffu_admissible": False}


def _verdict(cand, ref, prep=PREP):
    return runner.derive_verdict(prep, cand, ref, THR)


def test_complete_reports_give_early_fail_twin():
    v = _verdict(_report(), _report(0.55, 0.70))
    assert v["verdict"] == "FALSIFIED — early-fail"
    assert v["insufficient_reasons"] == []


def test_missing_candidate_run1_is_insufficient():
    cand = _report()
    cand["tiers"]["Tradeify_Select_100K"]["run1"] = {}
    v = _verdict(cand, _report(0.55, 0.70))
    assert v["verdict"] == "INSUFFICIENT"
    assert any("Tradeify_Select_100K" in r and "run1" in r for r in v["insufficient_reasons"])


def test_missing_candidate_run2_is_insufficient_not_substituted():
    cand = _report()
    cand["tiers"]["MFFU_Rapid_100K"]["run2"] = {}
    v = _verdict(cand, _report(0.55, 0.70))
    assert v["verdict"] == "INSUFFICIENT"
    assert any("MFFU_Rapid_100K" in r and "run2" in r for r in v["insufficient_reasons"])


def test_missing_reference_gating_reads_never_count_toward_ambiguous():
    ref = _report(0.01, 0.70)  # Run-1 busts look clearing; Run-2 is the gating read
    for t in ("Tradeify_Select_100K", "MFFU_Rapid_100K"):
        ref["tiers"][t]["run2"] = {}
    v = _verdict(_report(), ref)
    assert v["ambiguous"] is False
    assert v["verdict"] == "INSUFFICIENT"


def test_reference_ambiguous_twin_uses_run2_bust():
    ref = _report(0.70, 0.70)
    for t in ("Tradeify_Select_100K", "MFFU_Rapid_100K"):
        ref["tiers"][t]["run2"] = _run(0.01)
    v = _verdict(_report(), ref)
    assert v["ambiguous"] is True and v["verdict"] == "AMBIGUOUS"


def test_bulenox_gates_on_run1_and_consistency_tier_on_run2():
    ref = _report(0.70, 0.70)
    ref["tiers"]["Bulenox_100K"]["run1"] = _run(0.01)
    ref["tiers"]["Bulenox_100K"]["run2"] = _run(0.01)
    ref["tiers"]["Tradeify_Select_100K"]["run1"] = _run(0.01)  # diagnostic only
    v = _verdict(_report(), ref)
    assert v["reference_bust"]["Bulenox_100K"] == 0.01
    assert v["reference_bust"]["Tradeify_Select_100K"] == 0.70
    assert v["ambiguous"] is False


def test_wrong_gated_on_label_is_insufficient():
    cand = _report()
    cand["tiers"]["BluSky_Premium_100K"]["gated_on"] = "run1_degenerate"
    v = _verdict(cand, _report(0.55, 0.70))
    assert v["verdict"] == "INSUFFICIENT"


# ── re-hash: the manifest bytes validated are the bytes parsed (Codex 4199556590) ──

def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _primary(tmp_path):
    root = tmp_path / "primary"
    lines = []
    for i in range(8):
        rel = f"src/file{i}.txt"
        (root / "src").mkdir(parents=True, exist_ok=True)
        data = f"source {i}".encode()
        (root / rel).write_bytes(data)
        lines.append(f"{_sha(data)}  {rel}")
    manifest = ("# header\n" + "\n".join(lines) + "\n").encode()
    (root / "core/strategies").mkdir(parents=True)
    (root / "core/strategies/BOOK_SOURCES.sha256").write_bytes(manifest)
    return root, _sha(manifest)


def _other_inputs(tmp_path, n):
    out = {}
    for i in range(n):
        p = tmp_path / f"in{n}_{i}.csv"
        p.write_bytes(f"input {n} {i}".encode())
        out[(f"leg{i}", "normal") if n == 6 else p] = (p, _sha(p.read_bytes())) if n == 6 else _sha(p.read_bytes())
    return out


def _rehash(root, manifest_sha, tmp_path):
    bp = b"book policy"
    return runner.rehash(primary=root, manifest_sha=manifest_sha,
                         series_inputs=_other_inputs(tmp_path, 6), reference_inputs=_other_inputs(tmp_path, 4),
                         book_policy_bytes=bp, book_policy_sha=_sha(bp))


def test_rehash_twin_passes_with_consistent_manifest(tmp_path):
    root, msha = _primary(tmp_path)
    assert _rehash(root, msha, tmp_path) == {"n": 20, "all_match": True}


def test_rehash_blocks_when_primary_manifest_and_source_drift_together(tmp_path):
    root, msha = _primary(tmp_path)
    (root / "src/file0.txt").write_bytes(b"drifted")
    m = root / "core/strategies/BOOK_SOURCES.sha256"
    text = m.read_text().splitlines()
    text[1] = f"{_sha(b'drifted')}  src/file0.txt"
    m.write_text("\n".join(text) + "\n")
    with pytest.raises(runner.Blocked, match="manifest"):
        _rehash(root, msha, tmp_path)
