"""#715 executor: verdict derivation rebuilt from invariants I1-I6 (escalation lane); synthetic inputs only."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
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
BULENOX, TRADEIFY, MFFU = "Bulenox_100K", "Tradeify_Select_100K", "MFFU_Rapid_100K"
CSHA, RSHA = "c" * 64, "r" * 64
PREP = {"g2_killed_tiers": [], "mffu_admissible": False}
KILLED = {"g2_killed_tiers": [TRADEIFY], "mffu_admissible": False}


def _run(bust):
    return {"headline_bust": bust, "pass_rate": 1 - bust, "rates": {"bust_trailing": bust, "pass": 1 - bust}}


def _report(bust1=0.30, bust2=0.35):
    tiers = {}
    for t in THR.tier_keys:
        if t in CONSISTENCY:
            tiers[t] = {"gated_on": "run2", "run1": _run(bust1), "run2": _run(bust2), "clears_part_a": False}
        else:
            tiers[t] = {"gated_on": "run1_degenerate", "run1": _run(bust1), "run2": _run(bust1), "clears_part_a": False}
    return {"tiers": tiers, "gate_grade": True, "gate_grade_reasons": [], "halted_at": None,
            "breach_clock": "intraday_honest",
            "thresholds_source": "docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md"}


def _with(report, tier, **fields):
    report["tiers"][tier].update(fields)
    return report


def _g1_halted():
    r = _report()
    r.update(tiers={}, halted_at="G1")
    return r


def _killed_tradeify_cand():
    return _with(_report(), TRADEIFY, gated_on="g2_killed", run1={}, run2={})


def _ref_two_clearing_gating_reads():
    return _with(_with(_report(0.70, 0.70), TRADEIFY, run2=_run(0.01)), MFFU, run2=_run(0.01))


def _arm(n_sims=None, seeds=None, horizon=None):
    return {"n_sims": THR.sims_per_seed if n_sims is None else n_sims,
            "seeds": list(THR.seeds if seeds is None else seeds),
            "horizon": THR.horizon if horizon is None else horizon}


def _record(sha, tiers=THR.tier_keys):
    arms = {t: {"run1": _arm(), **({"run2": _arm()} if t in CONSISTENCY else {})} for t in tiers}
    return {"report_sha256": sha, "arms": arms, "guard": {t: "pass" for t in tiers}}


def _set(rec, tier, run, **kw):
    rec = copy.deepcopy(rec)
    rec["arms"][tier][run] = _arm(**kw)
    return rec


def _drop(rec, tier, run):
    rec = copy.deepcopy(rec)
    del rec["arms"][tier][run]
    return rec


def _guard(rec, tier, value):
    rec = copy.deepcopy(rec)
    rec["guard"][tier] = value
    return rec


def _derive(cand=None, ref=None, prep=PREP, cand_rec="full", ref_rec="full"):
    cand = _report() if cand is None else cand
    ref = _report(0.55, 0.70) if ref is None else ref
    cand_rec = _record(CSHA) if cand_rec == "full" else cand_rec
    ref_rec = _record(RSHA) if ref_rec == "full" else ref_rec
    return runner.derive_verdict(prep, cand, ref, THR, cand_sha=CSHA, ref_sha=RSHA,
                                 cand_depth=cand_rec, ref_depth=ref_rec)


EARLY = "FALSIFIED — early-fail"
# (id, _derive kwargs, expected verdict, substrings each found in some reason, or None = no reasons at all)
MATRIX = [
    ("all_arms_full_decisive", {}, EARLY, None),
    ("candidate_arm_n_sims_40_r4200174057", {"cand_rec": _set(_record(CSHA), TRADEIFY, "run1", n_sims=40)},
     "INSUFFICIENT", ["candidate Tradeify_Select_100K run1", "n_sims=40"]),
    ("candidate_arm_wrong_seeds", {"cand_rec": _set(_record(CSHA), BULENOX, "run1", seeds=(1, 2, 3))},
     "INSUFFICIENT", ["candidate Bulenox_100K run1", "seeds"]),
    ("candidate_arm_wrong_horizon", {"cand_rec": _set(_record(CSHA), MFFU, "run2", horizon=500)},
     "INSUFFICIENT", ["candidate MFFU_Rapid_100K run2", "horizon"]),
    ("reference_arm_shallow", {"ref_rec": _set(_record(RSHA), MFFU, "run2", n_sims=40)},
     "INSUFFICIENT", ["reference MFFU_Rapid_100K run2", "n_sims=40"]),
    ("reference_arm_entry_missing", {"ref_rec": _drop(_record(RSHA), TRADEIFY, "run1")},
     "INSUFFICIENT", ["reference Tradeify_Select_100K run1", "no depth entry"]),
    ("honest_g1_halt_r4200174064", {"cand": _g1_halted(), "cand_rec": {"report_sha256": CSHA, "arms": {}, "guard": {}}},
     EARLY, None),
    ("honest_g1_halt_without_any_record", {"cand": _g1_halted(), "cand_rec": None}, EARLY, None),
    ("g2_killed_tier_shallow_arm", {"prep": KILLED, "cand": _killed_tradeify_cand(),
                                    "cand_rec": _set(_record(CSHA), TRADEIFY, "run2", n_sims=40)}, EARLY, None),
    ("g2_killed_tier_missing_arms_and_guard",
     {"prep": KILLED, "cand": _killed_tradeify_cand(),
      "cand_rec": _record(CSHA, tiers=[t for t in THR.tier_keys if t != TRADEIFY])}, EARLY, None),
    ("record_sha_mismatch", {"cand_rec": _record("x" * 64)}, "INSUFFICIENT", ["candidate", "report_sha256"]),
    ("record_missing", {"ref_rec": None}, "INSUFFICIENT", ["reference Bulenox_100K run1", "no bound depth record"]),
    ("guard_fail_on_read_tier", {"cand_rec": _guard(_record(CSHA), TRADEIFY, "fail")},
     "INSUFFICIENT", ["candidate Tradeify_Select_100K", "guard"]),
    ("guard_fail_on_g2_killed_tier_not_required",
     {"prep": KILLED, "cand": _killed_tradeify_cand(), "cand_rec": _guard(_record(CSHA), TRADEIFY, "fail")}, EARLY, None),
    ("ambiguous_precedes_insufficient",
     {"ref": _ref_two_clearing_gating_reads(), "cand_rec": _set(_record(CSHA), TRADEIFY, "run1", n_sims=40)},
     "AMBIGUOUS", ["candidate Tradeify_Select_100K run1"]),
    ("missing_reference_gating_read_not_ambiguous",
     {"ref": _with(_with(_report(0.01, 0.70), TRADEIFY, run2={}), MFFU, run2={})},
     "INSUFFICIENT", ["reference Tradeify_Select_100K run2 missing"]),
    ("unevidenced_reference_gating_read_not_ambiguous",
     {"ref": _ref_two_clearing_gating_reads(),
      "ref_rec": _set(_set(_record(RSHA), TRADEIFY, "run2", n_sims=40), MFFU, "run2", n_sims=40)},
     "INSUFFICIENT", ["reference Tradeify_Select_100K run2", "reference MFFU_Rapid_100K run2"]),
    ("candidate_run1_missing", {"cand": _with(_report(), TRADEIFY, run1={})},
     "INSUFFICIENT", ["candidate Tradeify_Select_100K run1 missing"]),
    ("candidate_run2_missing_not_substituted", {"cand": _with(_report(), MFFU, run2={})},
     "INSUFFICIENT", ["candidate MFFU_Rapid_100K run2 missing"]),
    ("wrong_gated_on_label", {"cand": _with(_report(), "BluSky_Premium_100K", gated_on="run1_degenerate")},
     "INSUFFICIENT", ["BluSky_Premium_100K gated_on"]),
]


@pytest.mark.parametrize("case", MATRIX, ids=[m[0] for m in MATRIX])
def test_verdict_matrix(case):
    _, kw, verdict, needles = case
    v = _derive(**copy.deepcopy(kw))
    assert v["verdict"] == verdict, v["insufficient_reasons"]
    if needles is None:
        assert v["insufficient_reasons"] == []
    for n in needles or ():
        assert any(n in r for r in v["insufficient_reasons"]), (n, v["insufficient_reasons"])


def test_ambiguous_counts_only_evidenced_reference_gating_reads():
    assert _derive(ref=_ref_two_clearing_gating_reads())["ambiguous"] is True
    v = _derive(ref=_ref_two_clearing_gating_reads(), ref_rec=_set(_record(RSHA), MFFU, "run2", n_sims=40))
    assert v["ambiguous"] is False and v["reference_bust"][MFFU] is None


def test_gating_run_by_tier_semantics():
    ref = _with(_with(_report(0.70, 0.70), BULENOX, run1=_run(0.01)), TRADEIFY, run1=_run(0.01))
    v = _derive(ref=ref)
    assert v["reference_bust"][BULENOX] == 0.01 and v["reference_bust"][TRADEIFY] == 0.70
    assert v["ambiguous"] is False


def test_g1_halted_candidate_record_content_is_never_read():
    for rec in (None, {"report_sha256": "x" * 64},
                {"report_sha256": CSHA, "arms": {"junk": 1}, "guard": {"t": "fail"}}):
        v = _derive(cand=_g1_halted(), cand_rec=rec)
        assert v["verdict"] == EARLY and v["insufficient_reasons"] == []


def test_lattice_fallback_removed():
    assert not hasattr(runner, "lattice_paths")
    v = _derive(cand_rec=None)
    assert v["verdict"] == "INSUFFICIENT"
    assert v["insufficient_reasons"] and all("no bound depth record" in r for r in v["insufficient_reasons"])
    assert v["row_verdict"] == EARLY


def test_derive_verdict_is_pure():
    args = (_report(), _report(0.55, 0.70), _record(CSHA), _record(RSHA))
    snap = copy.deepcopy(args)
    _derive(cand=args[0], ref=args[1], cand_rec=args[2], ref_rec=args[3])
    assert args == snap


# ── score-stage writer (I3, I6): what it writes is what derive_verdict accepts ──

def _write(tmp_path, name, rep, n_sims):
    p = tmp_path / f"{name}_report.json"
    p.write_text(json.dumps(rep))
    runner.write_depth_record(p, rep, THR, n_sims=n_sims)
    return hashlib.sha256(p.read_bytes()).hexdigest(), json.loads((tmp_path / f"{name}_report.depth.json").read_text())


def test_write_depth_record_round_trip(tmp_path):
    csha, crec = _write(tmp_path, "candidate", _report(), THR.sims_per_seed)
    rsha, rrec = _write(tmp_path, "reference", _report(0.55, 0.70), THR.sims_per_seed)
    assert set(crec["arms"][BULENOX]) == {"run1"} and set(crec["arms"][TRADEIFY]) == {"run1", "run2"}
    v = runner.derive_verdict(PREP, _report(), _report(0.55, 0.70), THR, cand_sha=csha, ref_sha=rsha,
                              cand_depth=crec, ref_depth=rrec)
    assert v["verdict"] == EARLY and v["insufficient_reasons"] == []


def test_write_depth_record_records_shallow_depth_and_guard_failures(tmp_path):
    rep = _with(_report(), MFFU, gated_on="g2_killed", run1={}, run2={})
    rep["gate_grade_reasons"] = [f"{TRADEIFY}: non-vacuity failed: x"]
    _, rec = _write(tmp_path, "candidate", rep, 40)
    assert rec["arms"][TRADEIFY]["run1"]["n_sims"] == 40
    assert MFFU not in rec["arms"] and MFFU not in rec["guard"]
    assert rec["guard"][TRADEIFY] == "fail" and rec["guard"][BULENOX] == "pass"


def test_write_depth_record_eod_clock_has_no_guard_pass(tmp_path):
    rep = _report()
    rep["breach_clock"] = "eod"
    _, rec = _write(tmp_path, "reference", rep, THR.sims_per_seed)
    assert set(rec["guard"].values()) == {"not_run"}


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
