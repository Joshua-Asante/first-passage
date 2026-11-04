"""Run the firm feasibility atlas (DESIGN.md) and write atlas.csv plus run_record.json.

    python -I scripts/fp.py python lab/analysis/c1/firm_feasibility_atlas_2026-11/run_atlas.py

Synthetic streams only (K = 0). ``--smoke`` runs a tiny grid into a scratch directory.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
for p in (ROOT / "core", ROOT / "lab", HERE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import numpy as np  # noqa: E402

from research_utils.camp_import import load_camp_sibling  # noqa: E402

A = load_camp_sibling("atlas", __file__)

from firm_rules import AUTOMATION_FRIENDLY_PROP_FIRMS, FIRM_RULES  # noqa: E402
from mc import preflight  # noqa: E402
from mc.simulation import HORIZON_CAP, simulate_path  # noqa: E402

FIELDS = ("config", "tier", "family", "variant", "mark", "consistency", "fixed_dollar_trail",
          "shape_index", "seed", "f", "e", "p", "payoff", "lam", "mae", "risk_usd", "n",
          "pass", "bust", "unresolved", "se_pass", "se_bust", "ttp_p10", "ttp_p50", "ttp_p90",
          "p_pass_22", "p_pass_63", *(f"n_{k}" for k in preflight.OUTCOME_KEYS))

_CFGS: list = []
_KW: dict = {}


def _init(cfgs, kws):
    _CFGS[:] = cfgs
    _KW.update(kws)


def run_shape(task) -> list[dict]:
    idx, shape, n_paths, horizon = task
    seed = A.SEED_BASE + idx
    pnl, low = A.generate(shape.e, shape.p, shape.lam, shape.mae, n_paths, horizon, seed)
    rows = []
    for cfg in _CFGS:
        kw = _KW[cfg.name]
        risk = shape.f * A.dd_allowance(kw)
        counts = dict.fromkeys(preflight.OUTCOME_KEYS, 0)
        days = []
        for i in range(n_paths):
            out, day, _dd, _c = simulate_path(
                (pnl[i] * risk)[:, None], A.DD_TRIGGER, A.DD_SCALE, horizon,
                intraday_low=low[i] * risk, **kw)
            counts[out] += 1
            if out == "pass":
                days.append(day)
        if sum(counts.values()) != n_paths:  # F1 bucket-sum invariant
            raise AssertionError(f"{cfg.name} shape {idx}: buckets sum {sum(counts.values())}")
        n = n_paths
        ps = counts["pass"] / n
        bust = sum(counts[k] for k in preflight.BUST_KEYS) / n
        d = np.asarray(days, dtype=float)
        q = np.percentile(d, [10, 50, 90]) if len(d) else [np.nan] * 3
        rows.append({
            "config": cfg.name, "tier": cfg.tier, "family": cfg.family, "variant": cfg.variant,
            "mark": cfg.mark, "consistency": "" if cfg.consistency is None else cfg.consistency,
            "fixed_dollar_trail": int(cfg.fixed_dollar_trail), "shape_index": idx, "seed": seed,
            "f": shape.f, "e": shape.e, "p": shape.p, "payoff": round(shape.payoff, 6),
            "lam": shape.lam, "mae": shape.mae, "risk_usd": round(risk, 2), "n": n,
            "pass": ps, "bust": bust, "unresolved": counts["horizon_cap"] / n,
            "se_pass": round(float(np.sqrt(ps * (1 - ps) / n)), 6),
            "se_bust": round(float(np.sqrt(bust * (1 - bust) / n)), 6),
            "ttp_p10": q[0], "ttp_p50": q[1], "ttp_p90": q[2],
            "p_pass_22": float((d <= 22).sum()) / n, "p_pass_63": float((d <= 63).sum()) / n,
            **{f"n_{k}": v for k, v in counts.items()},
        })
    return rows


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(*args) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout.strip()


def main(argv=None) -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true", help="tiny grid; requires --out")
    ap.add_argument("--out", type=Path, default=None,
                    help="output directory (default: this directory, full runs only)")
    ap.add_argument("--workers", type=int, default=os.cpu_count() or 1)
    a = ap.parse_args(argv)
    if a.out is None:
        if a.smoke:  # never let a smoke grid overwrite the committed atlas
            ap.error("--smoke requires --out (a scratch directory)")
        a.out = HERE
    elif a.smoke and a.out.resolve() == HERE:
        ap.error("--smoke must not write into the atlas directory")

    if A.HORIZON != HORIZON_CAP:
        raise SystemExit(f"design horizon {A.HORIZON} != engine HORIZON_CAP {HORIZON_CAP}")
    cfgs = A.configs(FIRM_RULES, AUTOMATION_FRIENDLY_PROP_FIRMS)
    kws = {c.name: A.engine_kwargs(c, preflight.firm_kwargs) for c in cfgs}
    for c in cfgs:  # constraint-D pre-flight on every tier
        preflight.assert_engine_ready(c.tier, allow_provisional_rules=(c.mark == "PROVISIONAL"))

    all_shapes = A.shapes()
    tasks = [(i, s, A.PATHS, A.HORIZON) for i, s in enumerate(all_shapes)]
    if a.smoke:
        tasks = [(i, s, 20, 120) for i, s in enumerate(all_shapes) if i % 97 == 0]
    status = "dirty" if _git("status", "--porcelain", "--untracked-files=no") else "clean"
    head = _git("rev-parse", "HEAD")
    t0 = time.time()
    rows: list[dict] = []
    with Pool(a.workers, initializer=_init, initargs=(cfgs, kws)) as pool:
        for k, part in enumerate(pool.imap_unordered(run_shape, tasks, chunksize=1), 1):
            rows.extend(part)
            if k % 20 == 0 or k == len(tasks):
                el = time.time() - t0
                print(f"{k}/{len(tasks)} shapes, {el / 60:.1f} min elapsed, "
                      f"~{el / k * (len(tasks) - k) / 60:.1f} min left", flush=True)
    rows.sort(key=lambda r: (r["config"], r["shape_index"]))
    a.out.mkdir(parents=True, exist_ok=True)
    out_csv = a.out / "atlas.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.6g}" if isinstance(v, float) else v) for k, v in r.items()})
    record = {
        "status": "completed", "smoke": a.smoke, "git_head": head, "tracked_tree": status,
        "python": sys.version.split()[0], "platform": platform.platform(),
        "numpy": np.__version__, "workers": a.workers, "wall_seconds": round(time.time() - t0, 1),
        "shapes": len(tasks), "configs": [c.name for c in cfgs], "rows": len(rows),
        "paths_per_cell": tasks[0][2], "horizon": tasks[0][3],
        "sha256": {"atlas.csv": _sha(out_csv),
                   **{p: _sha(ROOT / p) for p in ("core/mc/simulation.py", "core/mc/preflight.py",
                                                  "core/firm_rules.py")},
                   **{f"{HERE.relative_to(ROOT)}/{p}": _sha(HERE / p)
                      for p in ("atlas.py", "run_atlas.py", "DESIGN.md")}},
    }
    (a.out / "run_record.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out_csv} ({len(rows)} rows) in {record['wall_seconds']} s")


if __name__ == "__main__":
    main()
