"""Q-TRAINKILL-3 -- two-block concordance of NEG vs DEP-ZERO.

Freeze-before-compute: sha256 the prereg bytes BEFORE opening TK2 RESULTS.json.
Stdlib only. $0 / K=0.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
PREREG = REPO / "docs" / "briefs" / "pre-registration" / "Q-TRAINKILL-3-verdict-preregistration.md"
TK2 = REPO / "lab" / "analysis" / "_inbox" / "q_trainkill_2_2026-08" / "RESULTS.json"
EXPECTED_SHA = "93c21d21eb0fd2d0e580a384a586dbf10d19d8a23a593dea6e147f63ad57e7f6"

BLOCK_F = ("MSL-C1", "MSL-C2", "MSL-C3-K2", "Q-MNQDTL-CON-1")
BLOCK_A = (
    "Q-TNEC-CON-2",
    "Q-TNEC-CON-3",
    "Q-TNEC-CON-4",
    "Q-TNEC-CON-5",
    "MSL-S2A",
)
TIE_RATIO = 2.0
EPS = 1e-6


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def geo_mean(ps: list[float]) -> float:
    return math.exp(sum(math.log(max(EPS, p)) for p in ps) / len(ps))


def winner(g_neg: float, g_dep: float) -> str:
    if g_neg / g_dep >= TIE_RATIO:
        return "NEG"
    if g_dep / g_neg >= TIE_RATIO:
        return "DEP"
    return "TIE"


def block_gs(by_id_neg: dict[str, float], by_id_dep: dict[str, float], ids: tuple[str, ...]) -> dict:
    missing = [i for i in ids if i not in by_id_neg or i not in by_id_dep]
    if missing:
        raise SystemExit(f"ABORT: missing P rows {missing}")
    g_neg = geo_mean([by_id_neg[i] for i in ids])
    g_dep = geo_mean([by_id_dep[i] for i in ids])
    return {
        "ids": list(ids),
        "g_neg": g_neg,
        "g_dep": g_dep,
        "ratio_neg_over_dep": g_neg / g_dep,
        "winner": winner(g_neg, g_dep),
    }


def main() -> dict:
    if not PREREG.is_file():
        raise SystemExit(f"ABORT: prereg missing: {PREREG}")
    prereg_sha = sha256_file(PREREG)
    print(f"prereg_sha256 {prereg_sha}")
    print(f"prereg_path   {PREREG.relative_to(REPO).as_posix()}")
    if prereg_sha != EXPECTED_SHA:
        raise SystemExit(f"ABORT: prereg sha drifted from freeze {EXPECTED_SHA}")

    tk2 = json.loads(TK2.read_text(encoding="utf-8"))
    by_neg = {row["id"]: float(row["P"]) for row in tk2["P_neg"]}
    by_dep = {row["id"]: float(row["P"]) for row in tk2["P_dep_zero"]}

    block_f = block_gs(by_neg, by_dep, BLOCK_F)
    block_a = block_gs(by_neg, by_dep, BLOCK_A)
    wf, wa = block_f["winner"], block_a["winner"]

    if wf == wa == "NEG":
        verdict, named = "RESOLVED", "NEG-FAMILIES"
    elif wf == wa == "DEP":
        verdict, named = "RESOLVED", "KILLS-INFORMATIVE-DEP"
    else:
        verdict, named = "AMBIGUOUS-HOLD", f"{wf}|{wa}"

    payload = {
        "prereg_sha256": prereg_sha,
        "tk2_source": TK2.relative_to(REPO).as_posix(),
        "election_fired": False,
        "block_f": block_f,
        "block_a": block_a,
        "verdict": verdict,
        "named_reading": named,
    }
    (HERE / "RESULTS.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"block_F winner {wf}  g_neg={block_f['g_neg']:.6g}  g_dep={block_f['g_dep']:.6g}  ratio={block_f['ratio_neg_over_dep']:.4g}")
    print(f"block_A winner {wa}  g_neg={block_a['g_neg']:.6g}  g_dep={block_a['g_dep']:.6g}  ratio={block_a['ratio_neg_over_dep']:.4g}")
    print(f"verdict {verdict}  named {named}")
    return payload


if __name__ == "__main__":
    main()
