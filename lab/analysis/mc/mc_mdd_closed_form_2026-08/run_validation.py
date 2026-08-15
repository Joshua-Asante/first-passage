"""CLI: Appendix B Q check → G_D vs simulate_path grid → gated trail/static equiv."""

from __future__ import annotations

import csv
import json
import sys
import time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from closed_form import check_appendix_b, solve_h_static_equiv  # noqa: E402
from harness import GRID, mc_bust_rate  # noqa: E402

OUT_JSON = _HERE / "validation_raw.json"
EQUIV_CSV = _HERE / "trail_static_equiv.csv"

APP_B_SAMPLES = {
    "qp": [0.5],
    "qn": [0.5],
}


def main() -> int:
    t0 = time.perf_counter()
    print("=== Appendix B Q sanity ===", flush=True)
    app_b_rows = []
    for kind, xs in APP_B_SAMPLES.items():
        rows = check_appendix_b(kind, xs, include_integral=False)
        app_b_rows.extend(rows)
        for r in rows:
            flag = "PASS" if r["pass"] else "FAIL"
            print(
                f"  {flag} {r['kind']} {r.get('check','?')} x={r['x']}: "
                f"Q_impl={r['Q_impl']:.6f} Q_tab={r['Q_table']:.6f} "
                f"|err|={r['abs_err']:.6f} (tol {r['tol']})",
                flush=True,
            )

    print("\n=== G_D vs simulate_path grid ===", flush=True)
    grid_rows = []
    for spec in GRID:
        name = spec["name"]
        print(f"  running {name} ...", flush=True)
        t1 = time.perf_counter()
        row = mc_bust_rate(
            mu=spec["mu"],
            sigma=spec["sigma"],
            h=spec["h"],
            T=spec["T"],
            n_steps=spec["n_steps"],
            n_paths=spec["n_paths"],
            seed=spec["seed"],
        )
        row["name"] = name
        # Half-step diagnostic when disagreeing
        if not row["agree"]:
            half = mc_bust_rate(
                mu=spec["mu"],
                sigma=spec["sigma"],
                h=spec["h"],
                T=spec["T"],
                n_steps=max(10, spec["n_steps"] // 2),
                n_paths=min(5000, spec["n_paths"]),
                seed=spec["seed"] + 99,
            )
            row["half_steps_p_mc"] = half["p_mc"]
            row["half_steps_abs_err"] = half["abs_err"]
        grid_rows.append(row)
        flag = "AGREE" if row["agree"] else "DIVERGE"
        print(
            f"  {flag} {name}: p_mc={row['p_mc']:.4f}±{row['se']:.4f} "
            f"G_D={row['G_D']:.4f} |err|={row['abs_err']:.4f} tol={row['tol']:.4f} "
            f"({time.perf_counter()-t1:.1f}s)",
            flush=True,
        )

    agrees = [r["agree"] for r in grid_rows]
    mean_signed = float(sum(r["signed_err"] for r in grid_rows) / len(grid_rows))
    gate = all(agrees) and (-0.03 <= mean_signed <= 0.03)
    print(
        f"\n=== Equivalence gate: {'PASS' if gate else 'FAIL'} "
        f"(all_agree={all(agrees)} mean_signed_err={mean_signed:+.4f}) ===",
        flush=True,
    )

    equiv_rows = []
    if gate:
        # Small (mu,sigma,T) slice + several h_trail
        slices = [
            (0.0, 1.0, 4.0),
            (0.5, 1.0, 4.0),
            (1.0, 1.0, 9.0),
        ]
        h_trails = [1.5, 2.0, 2.5, 3.0]
        with EQUIV_CSV.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(
                fh,
                fieldnames=["mu", "sigma", "T", "h_trail", "h_static", "G"],
            )
            w.writeheader()
            for mu, sigma, T in slices:
                for ht in h_trails:
                    hs, g = solve_h_static_equiv(ht, mu, sigma, T)
                    row = {
                        "mu": mu,
                        "sigma": sigma,
                        "T": T,
                        "h_trail": ht,
                        "h_static": hs,
                        "G": g,
                    }
                    w.writerow(row)
                    equiv_rows.append(row)
                    print(
                        f"  equiv mu={mu} T={T} h_trail={ht} -> "
                        f"h_static={hs:.4f} G={g:.4f}",
                        flush=True,
                    )
        print(f"  wrote {EQUIV_CSV}", flush=True)
    else:
        if EQUIV_CSV.exists():
            EQUIV_CSV.unlink()
        print("  (no equiv CSV — gate failed)", flush=True)

    payload = {
        "appendix_b": app_b_rows,
        "grid": grid_rows,
        "mean_signed_err": mean_signed,
        "equiv_gate": gate,
        "equiv": equiv_rows,
        "elapsed_s": time.perf_counter() - t0,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nwrote {OUT_JSON} ({payload['elapsed_s']:.1f}s total)", flush=True)
    return 0 if gate or all(agrees) else 0  # always 0 — divergence is a finding


if __name__ == "__main__":
    raise SystemExit(main())
