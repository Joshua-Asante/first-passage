"""Q-GEOFIT-1 §2 deliverable (iii) — book profile positions relative to the grid.

Context only, NO re-scoring claim (brief §2). This fits the two real books this
programme has onto the frozen §2 4-tuple family and reports where they sit relative
to the declared axis ranges. It runs NO Monte Carlo and consumes no data budget.

Books:
  c1  — the live 2-leg futures book (Striker DJ30->MYM + Striker NAS100->MNQ),
        built by the frozen Class-S adapter, at the $100K basis.
  CFD — the four locked CFD legs (Guardian XAUUSD / Striker DJ30 / Aegis USDJPY /
        Striker NAS100) on the canonical clean-vintage 2026-06-25 Pepperstone panel,
        static-decompounded at $200K then scaled to the $100K basis so the two books
        are directly comparable on the same account denominator.

Both books are reported on BOTH readings of §2's moment definitions:
  active-day  — sigma_d / mu-sigma computed over non-zero days only (the runner's
                declared reading R1, since §2 defines sigma_d as "daily vol on
                active days")
  all-day     — the same moments over every business day (the competing reading)
The two readings place a book very differently, so both are published rather than
silently collapsing to one.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[2]
_SCORING = _ROOT / "lab" / "analysis" / "class_s_candidate1_scoring_2026-07-15"
_DECOMP = _ROOT / "lab" / "analysis" / "decompound_remc_2026-06-07"
for _p in (_ROOT / "core", _ROOT / "lab", str(_SCORING), str(_DECOMP), str(_HERE)):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import run_envelope_map as M  # noqa: E402

CLEAN_VINTAGE = {
    "guardian": "Guardian_Gold_v5.5_PEPPERSTONE_XAUUSD_2026-06-25_94d8f.csv",
    "striker": "Striker_DJ30_v4.5_PEPPERSTONE_US30_2026-06-25_0b865.csv",
    "aegis": "Aegis_USDJPY_v4.3_PEPPERSTONE_USDJPY_2026-06-25_027bd.csv",
    "striker_nas100": "Striker_NAS100_v1_PEPPERSTONE_NAS100_2026-06-25_27e52.csv",
}


def all_day_fit(daily: np.ndarray) -> dict:
    """The competing reading: moments over EVERY business day."""
    d = np.asarray(daily, dtype=float).reshape(-1)
    sd = float(d.std(ddof=1))
    mean = float(d.mean())
    m = d - mean
    return {
        "sigma_d_pct": sd / M.ACCOUNT * 100.0,
        "mu_sigma": mean / sd,
        "z": float((d == 0.0).mean()),
        "excess_kurtosis": float((m**4).mean() / (m**2).mean() ** 2 - 3.0),
        "n_days": int(d.size),
    }


def in_range(fit: dict) -> dict:
    return {
        "sigma_d_pct": bool(min(M.SIGMA_D_PCT) <= fit["sigma_d_pct"] <= max(M.SIGMA_D_PCT)),
        "mu_sigma": bool(min(M.MU_SIG) <= fit["mu_sigma"] <= max(M.MU_SIG)),
        "z": bool(min(M.Z_FRAC) <= fit["z"] <= max(M.Z_FRAC)),
    }


def c1_daily_100k() -> np.ndarray:
    sys.argv = [sys.argv[0]]
    import run_class_s_c1_scoring as S

    S.phase0_verify()
    for leg in S.C1_STRATS:
        S.resolve_panel_path(leg)
    panel, meta, _ = S.build_scaled_panel(
        S.C1_STRATS, S.C1_ALLOCS, expect_1r=dict(S.EXPECTED_1R)
    )
    print(f"[profile] c1 panel {meta['panel_span']} n_bdays={meta['n_bdays']}", flush=True)
    return panel.sum(axis=1).to_numpy(dtype=float) * (M.ACCOUNT / S.ACCOUNT)


def cfd_daily_100k() -> np.ndarray:
    """Clean-vintage 4-leg CFD book, static-decompounded @ $200K, scaled to $100K."""
    import decompound as D
    from portfolio_mc import build_daily_panel

    inputs = _ROOT / "core" / "data" / "tv_exports" / "pepperstone"
    base = {
        s: D.reconstruct_roe(D.load_file(inputs / f)) for s, f in CLEAN_VINTAGE.items()
    }
    static = {s: D.rebank(df, "static") for s, df in base.items()}
    panel, scale_info = build_daily_panel(static, dict(D.ALLOC), fixed_1r_reference=D.FIXED_1R)
    print(f"[profile] CFD panel n_bdays={len(panel)} scale_info={scale_info}", flush=True)
    return panel.sum(axis=1).to_numpy(dtype=float) * (M.ACCOUNT / D.ACCOUNT)


def describe(name: str, daily: np.ndarray) -> dict:
    active = M.fit_profile(daily)
    allday = all_day_fit(daily)
    rec = {
        "book": name,
        "n_days": int(daily.size),
        "active_day_reading": {**active, "in_range": in_range(active)},
        "all_day_reading": {**allday, "in_range": in_range(allday)},
    }
    for tag, f in (("active-day", active), ("all-day", allday)):
        ir = in_range(f)
        print(
            f"[profile] {name:4s} {tag:11s} sigma_d={f['sigma_d_pct']:.4f}% "
            f"mu/sig={f['mu_sigma']:+.4f} z={f['z']:.4f}  "
            f"in_range: sd={ir['sigma_d_pct']} ms={ir['mu_sigma']} z={ir['z']}",
            flush=True,
        )
    return rec


def main() -> int:
    grid = {
        "sigma_d_pct_range": [min(M.SIGMA_D_PCT), max(M.SIGMA_D_PCT)],
        "mu_sigma_range": [min(M.MU_SIG), max(M.MU_SIG)],
        "z_range": [min(M.Z_FRAC), max(M.Z_FRAC)],
        "shapes": list(M.SHAPES),
    }
    print(f"[profile] declared grid ranges: {grid}", flush=True)

    out = {"grid_ranges": grid, "books": []}
    out["books"].append(describe("c1", c1_daily_100k()))
    try:
        out["books"].append(describe("CFD", cfd_daily_100k()))
    except Exception as e:
        print(f"[profile] CFD book unavailable: {e}", file=sys.stderr)
        out["cfd_error"] = str(e)

    dest = _HERE / "profile_positions.json"
    dest.write_text(json.dumps(out, indent=2, default=str) + "\n", encoding="utf-8")
    print(f"[written] {dest}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
