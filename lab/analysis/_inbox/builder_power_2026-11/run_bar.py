"""Bar-layer calibration and grid (DESIGN.md). Usage, from the repo root:

    python -I scripts/fp.py python lab/analysis/_inbox/builder_power_2026-11/run_bar.py --out <json>
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path[:0] = [str(ROOT / "lab"), str(ROOT / "core"), str(Path(__file__).parent)]

import numpy as np  # noqa: E402

DRIFTS = (0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0)
CAL_SEED, VER_SEED, SEED = 20261106, 20261107, 20261105
CHUNK, CHUNKS = 20_000, 5
CELLS = [(0.0, 1510), (0.85, 1510), (1.5, 1510), (0.85, 2350)]
KS = (1, 2, 4)
H = 378
PATHS = 200


def _sharpe_chunk(args) -> tuple[float, int]:
    import harness as Hm
    d, seed, i = args
    rng = np.random.default_rng(np.random.SeedSequence([seed, int(d * 1000), i]))
    b, ds = Hm.bar_panel(rng, CHUNK, d)
    x = Hm.gates.daily(Hm.CARD, Hm.gates.resolved(Hm.C.simulate(Hm.CARD, b, ds), "calibration"), ds, Hm.COSTS)
    return float(x.mean()), float((x ** 2).mean())


def estimate(ex, drifts, seed) -> dict:
    """Annual net Sharpe of the card at each drift, pooled over CHUNKS chunks of CHUNK sessions."""
    jobs = [(d, seed, i) for d in drifts for i in range(CHUNKS)]
    res = list(ex.map(_sharpe_chunk, jobs))
    out = {}
    for j, d in enumerate(drifts):
        m = np.array(res[j * CHUNKS:(j + 1) * CHUNKS])
        mean, m2 = m[:, 0].mean(), m[:, 1].mean()
        s = mean / np.sqrt(m2 - mean ** 2)
        N = CHUNK * CHUNKS
        out[d] = {"annual_sharpe": float(s * np.sqrt(252)), "se": float(np.sqrt((1 + s * s / 2) / N) * np.sqrt(252)),
                  "sessions": N}
    return out


def _path(args) -> dict:
    import harness as Hm
    d, n, cell, p = args
    rng = np.random.default_rng(np.random.SeedSequence([SEED, cell, p]))
    return Hm.bar_path(rng, d, n, H, KS)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--paths", type=int, default=PATHS)
    a = ap.parse_args()
    t = time.time()
    with ProcessPoolExecutor(a.workers) as ex:
        cal = estimate(ex, DRIFTS, CAL_SEED)
        xs = np.array([cal[d]["annual_sharpe"] for d in DRIFTS])
        if np.any(np.diff(xs) <= 0):
            raise SystemExit(f"calibration is not increasing in drift: {xs}")
        targets = sorted({S for S, _ in CELLS})
        chosen = {S: float(np.interp(S, xs, DRIFTS)) for S in targets}
        ver = estimate(ex, [chosen[S] for S in targets], VER_SEED)
        cal_rec = {"grid": {str(d): v for d, v in cal.items()},
                   "chosen": {str(S): {"drift": chosen[S], **ver[chosen[S]],
                                       "v2_pass": abs(ver[chosen[S]]["annual_sharpe"] - S) <= 0.10} for S in targets}}
        print("calibration", json.dumps(cal_rec["chosen"]), round(time.time() - t), "s", flush=True)
        cells = []
        for ci, (S, n) in enumerate(CELLS):
            rows = list(ex.map(_path, [(chosen[S], n, ci, p) for p in range(a.paths)]))
            cells.append(summarise(S, n, ci, chosen[S], rows))
            print("cell", ci, S, n, round(time.time() - t), "s", flush=True)
    meta = {"engine_sha256": __import__("builder.gates", fromlist=["x"]).engine_version(), "seeds":
            {"calibration": CAL_SEED, "verification": VER_SEED, "paths": SEED}, "holdout": H,
            "seconds": round(time.time() - t, 1)}
    Path(a.out).write_text(json.dumps({"meta": meta, "calibration": cal_rec, "cells": cells}, indent=1), encoding="utf-8")
    return 0


ORDER = ("5a", "5c", "5d", "5e", "5f")


def summarise(S, n, ci, d, rows) -> dict:
    P = len(rows)
    unresolved = sum(r["verdict"] == "unresolved" for r in rows)
    ok = [r for r in rows if r["verdict"] != "unresolved"]
    stand = {g: sum(r["gates"].get(g, False) for r in ok if g in r["gates"]) / max(1, sum(g in r["gates"] for r in ok))
             for g in ORDER}
    stand["holdout"] = sum(r["holdout"] for r in ok) / max(1, len(ok))
    by_k = {}
    for k in KS:
        kill = dict.fromkeys(ORDER + ("holdout",), 0)
        passed = 0
        for r in ok:
            seq = [(g, r["gates"][g]) for g in ORDER[:4] if g in r["gates"]]
            if all(v for _, v in seq) and len(seq) == 4:
                seq.append(("5f", r["5f_k"][k]))
                seq.append(("holdout", r["holdout"]))
            first = next((g for g, v in seq if not v), None)
            if first:
                kill[first] += 1
            else:
                passed += 1
        by_k[k] = {"stack_pass": passed / P, "kill_share": {g: v / P for g, v in kill.items()},
                   "5f_standalone": sum(r["5f_k"][k] for r in ok) / max(1, len(ok))}
    return {"cell": ci, "target_S": S, "n": n, "drift": d, "paths": P, "unresolved": unresolved,
            "mean_trades": float(np.mean([r["trades"] for r in rows])), "standalone_reached": stand, "by_k": by_k}


if __name__ == "__main__":
    raise SystemExit(main())
