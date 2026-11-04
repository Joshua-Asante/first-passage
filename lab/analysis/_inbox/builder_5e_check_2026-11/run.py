"""T1/T2 runner (DESIGN.md). From the repo root:

    python -I scripts/fp.py python lab/analysis/_inbox/builder_5e_check_2026-11/run.py --out <json>
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path[:0] = [str(ROOT / "lab"), str(ROOT / "core"), str(Path(__file__).parent)]

import numpy as np  # noqa: E402

DRIFTS = (0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0)
CAL_SEED, VER_SEED, PATH_SEED, AUX_SEED = 20261108, 20261109, 20261110, 20261111
CHUNK, CHUNKS = 20_000, 5
TARGET_S = 1.5
N_DEV = 1000
PATHS = 400
WALL_LIMIT_S = 3600


def _chunk(args):
    import harness as Hm
    d, seed, i = args
    x, g = Hm.daily_net_gross(np.random.default_rng(np.random.SeedSequence([seed, int(d * 1000), i])), d, CHUNK)
    return float(x.sum()), float((x ** 2).sum()), float(g.sum()), float((g ** 2).sum()), len(x)


def estimate(ex, drifts, seed) -> dict:
    jobs = [(d, seed, i) for d in drifts for i in range(CHUNKS)]
    res = list(ex.map(_chunk, jobs))
    out = {}
    for j, d in enumerate(drifts):
        r = np.array(res[j * CHUNKS:(j + 1) * CHUNKS]).sum(axis=0)
        N = r[4]
        rec = {"sessions": int(N)}
        for name, s1, s2 in (("net", r[0], r[1]), ("gross", r[2], r[3])):
            m = s1 / N
            sr = m / math.sqrt(s2 / N - m * m)
            rec[f"{name}_annual_sharpe"] = sr * math.sqrt(252)
            rec[f"{name}_se"] = math.sqrt((1 + sr * sr / 2) / N) * math.sqrt(252)
        out[d] = rec
    return out


def _path(args):
    import harness as Hm
    d, cell, p = args
    rng = np.random.default_rng(np.random.SeedSequence([PATH_SEED, cell, p]))
    aux = np.random.default_rng(np.random.SeedSequence([AUX_SEED, cell, p]))
    return Hm.path_result(rng, aux, d, N_DEV)


def wilson(k: int, n: int, z: float = 1.959964) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    hw = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (c - hw, c + hw)


def summarise(cell, label, drift, rows) -> dict:
    ok = [r for r in rows if not r["unresolved"]]
    out = {"cell": cell, "label": label, "drift": drift, "paths": len(rows), "unresolved": len(rows) - len(ok),
           "v1_all_equal": all(r["v1_equal"] for r in ok), "mean_trades": float(np.mean([r["trades"] for r in ok])),
           "mean_net_annual_sharpe": float(np.mean([r["net_annual_sharpe"] for r in ok]))}
    for m in ("realised", "causal", "coin"):
        v = np.array([r[f"share_{m}"] for r in ok])
        k = int((v >= 0.95).sum())
        out[m] = {"pass": k, "pass_rate": k / len(ok), "wilson95": wilson(k, len(ok)),
                  "mean_share": float(v.mean()), "quantiles_10_50_90": [float(q) for q in np.quantile(v, [0.1, 0.5, 0.9])]}
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    t0 = time.time()
    with ProcessPoolExecutor(a.workers) as ex:
        cal = estimate(ex, DRIFTS, CAL_SEED)
        xs = np.array([cal[d]["net_annual_sharpe"] for d in DRIFTS])
        if np.any(np.diff(xs) <= 0):
            raise SystemExit(f"calibration is not increasing in drift: {xs}")
        if TARGET_S > xs[-1]:
            raise SystemExit(f"target {TARGET_S} above the drift grid's reach {xs[-1]}")
        d15 = float(np.interp(TARGET_S, xs, DRIFTS))
        ver = estimate(ex, [d15], VER_SEED)[d15]
        cal_rec = {"grid": {str(d): v for d, v in cal.items()}, "chosen_drift": d15, "verification": ver,
                   "v2_zero_drift_gross_ok": abs(cal[0.0]["gross_annual_sharpe"]) <= 0.10,
                   "v3_target_ok": abs(ver["net_annual_sharpe"] - TARGET_S) <= 0.10}
        print("calibration done", round(time.time() - t0), "s", flush=True)
        cells = []
        for ci, (label, d) in enumerate((("zero_drift", 0.0), ("S1.5", d15))):
            rows = []
            for chunk in range(0, PATHS, 40):
                if time.time() - t0 > WALL_LIMIT_S:
                    print("wall limit reached; partial cell", flush=True)
                    break
                rows += list(ex.map(_path, [(d, ci, p) for p in range(chunk, min(chunk + 40, PATHS))]))
            cells.append(summarise(ci, label, d, rows))
            print("cell", ci, label, len(rows), "paths", round(time.time() - t0), "s", flush=True)
    import builder.gates as G
    meta = {"engine_sha256": G.engine_version(), "seeds": {"calibration": CAL_SEED, "verification": VER_SEED,
            "paths": PATH_SEED, "aux": AUX_SEED, "placebo": G.THRESHOLDS["5e_seed"]},
            "placebo_runs": G.THRESHOLDS["5e_placebo_runs"], "threshold": G.THRESHOLDS["5e_min_beaten_share"],
            "n_dev": N_DEV, "paths": PATHS, "seconds": round(time.time() - t0, 1)}
    Path(a.out).write_text(json.dumps({"meta": meta, "calibration": cal_rec, "cells": cells}, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
