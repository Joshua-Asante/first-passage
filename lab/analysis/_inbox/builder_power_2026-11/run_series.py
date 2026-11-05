"""Series-layer grid (DESIGN.md). Usage, from the repo root:

    python -I scripts/fp.py python lab/analysis/_inbox/builder_power_2026-11/run_series.py --out <json>
"""
from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path[:0] = [str(ROOT / "lab"), str(ROOT / "core"), str(Path(__file__).parent)]

import numpy as np  # noqa: E402

SHARPES = (0.0, 0.5, 0.85, 0.89, 1.0, 1.5)
NS = (1510, 2350)
QS = (0.15, 0.40, 0.85)
SHAPES = ("normal", "orb_skew")
KS = (1, 2, 4)
H = 378
SEED = 20261104
BOOK = {"book_sharpe": 1.0, "book_active": 0.9}


def cells() -> list[dict]:
    main = [dict(S=S, n=n, q=q, shape=sh, rho=0.0, paths=2000)
            for S, n, q, sh in itertools.product(SHARPES, NS, QS, SHAPES)]
    rho = [dict(S=S, n=n, q=0.40, shape="orb_skew", rho=0.3, paths=1000) for S, n in itertools.product(SHARPES, NS)]
    return [dict(c, cell=i) for i, c in enumerate(main + rho)]


def run_cell(c: dict) -> dict:
    import harness as Hm
    rng = np.random.default_rng(np.random.SeedSequence([SEED, c["cell"]]))
    rows = [Hm.series_path(rng, c["S"], c["n"], H, c["q"], c["shape"], KS, c["rho"], **BOOK) for _ in range(c["paths"])]
    P = len(rows)
    out = dict(c)
    out["mean_trades"] = float(np.mean([r["trades"] for r in rows]))
    out["standalone"] = {"5a": sum(r["5a"] for r in rows) / P, "5c": sum(r["5c"] for r in rows) / P,
                         "holdout": sum(r["holdout"] for r in rows) / P,
                         "5g_clear_any": sum(r["placement_any"] == "clear" for r in rows) / P}
    out["by_k"] = {}
    for k in KS:
        kill = {"5a": 0, "5c": 0, "5f": 0, "holdout": 0}
        passed, clear = 0, 0
        for r in rows:
            first = next((g for g, ok in (("5a", r["5a"]), ("5c", r["5c"]), ("5f", r["5f"][k]),
                                          ("holdout", r["holdout"])) if not ok), None)
            if first:
                kill[first] += 1
            else:
                passed += 1
                clear += r["placement"] == "clear"
        out["by_k"][k] = {"stack_pass": passed / P, "kill_share": {g: v / P for g, v in kill.items()},
                          "5f_standalone": sum(r["5f"][k] for r in rows) / P,
                          "5f_closed_form": Hm.closed_form_5f(c["S"], k, c["n"]),
                          "5g_clear_given_pass": (clear / passed) if passed else None,
                          "stack_and_5g_clear": clear / P}
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--limit", type=int, default=None, help="first N cells only (pilot)")
    a = ap.parse_args()
    cs = cells()[: a.limit]
    t = time.time()
    with ProcessPoolExecutor(a.workers) as ex:
        res = list(ex.map(run_cell, cs))
    meta = {"engine_sha256": __import__("builder.gates", fromlist=["x"]).engine_version(), "seed": SEED,
            "holdout": H, "book": BOOK, "seconds": round(time.time() - t, 1)}
    Path(a.out).write_text(json.dumps({"meta": meta, "cells": res}, indent=1), encoding="utf-8")
    print(f"{len(res)} cells in {meta['seconds']} s -> {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
