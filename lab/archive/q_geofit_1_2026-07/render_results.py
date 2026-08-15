"""Q-GEOFIT-1 — render RESULTS.md from envelope.json / anchors.json / profile_positions.json.

Pure rendering: reads the artifacts the runner produced and formats the §2 deliverables.
It computes no new MC and re-decides no frozen number. Deliverables (brief §2):
  (i)  boundary table — minimum mu/sigma that clears, per (sigma_d, shape, z)
  (ii) the sigma_d ceiling — max vol fundable at any declared mu/sigma
  (iii) c1 and CFD-book profile positions relative to the boundary (context only)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
import run_envelope_map as M  # noqa: E402

NA = "—"


def load(name: str):
    p = _HERE / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def boundary_table(cells: list[dict]) -> list[str]:
    """(i) minimum clearing mu/sigma per (sigma_d, shape, z)."""
    idx = {(c["sigma_d_pct"], c["shape"], c["z"], c["mu_sigma"]): c for c in cells}
    out = [
        "| σ_d (% acct) | shape | z | min μ/σ that clears | bust @ that cell | pass @ that cell |",
        "|---|---|---|---|---|---|",
    ]
    for sd in M.SIGMA_D_PCT:
        for sh in M.SHAPES:
            for z in M.Z_FRAC:
                hit = None
                for ms in M.MU_SIG:  # ascending — first clearer is the minimum
                    c = idx.get((sd, sh, z, ms))
                    if c and c["floor_ok"]:
                        hit = c
                        break
                if hit:
                    star = " *" if hit["mu_sigma"] > M.PRACTICALITY_CEILING else ""
                    out.append(
                        f"| {sd:.2f} | {sh} | {z:.1f} | **{hit['mu_sigma']:.3f}**{star} | "
                        f"{hit['headline_bust']:.2%} | {hit['pass_rate']:.2%} |"
                    )
                else:
                    out.append(f"| {sd:.2f} | {sh} | {z:.1f} | {NA} (none clears) | {NA} | {NA} |")
    out.append("")
    out.append("`*` = clears only ABOVE the practicality ceiling (μ/σ > 0.10) — diagnostic, "
               "cannot accept H-GEOFIT per §4.")
    return out


def sigma_ceiling(cells: list[dict]) -> list[str]:
    """(ii) max sigma_d that clears at ANY declared mu/sigma, split practical vs any."""
    out = [
        "| scope | max σ_d that clears | at μ/σ | shape | z |",
        "|---|---|---|---|---|",
    ]
    for label, pool in (
        ("practical (μ/σ ≤ 0.10)", [c for c in cells if c["practical"] and c["floor_ok"]]),
        ("any μ/σ (incl. diagnostic)", [c for c in cells if c["floor_ok"]]),
    ):
        if not pool:
            out.append(f"| {label} | {NA} (no cell clears) | {NA} | {NA} | {NA} |")
            continue
        best = max(pool, key=lambda c: c["sigma_d_pct"])
        out.append(
            f"| {label} | **{best['sigma_d_pct']:.2f}%** | {best['mu_sigma']:.3f} | "
            f"{best['shape']} | {best['z']:.1f} |"
        )
    return out


def skew_diagnostic(anch: dict) -> list[str]:
    """Why A2 missed: re-draw the fitted cell and compare higher moments to the real book.

    Cheap and MC-free — it re-uses the runner's own generator at the fitted 4-tuple and
    contrasts the moments the family does NOT parameterize.
    """
    import numpy as np

    a2 = (anch or {}).get("A2") or {}
    fit = a2.get("fit")
    if not fit:
        return ["_no A2 fit available._"]

    sys.path.insert(0, str(_HERE))
    import run_class_s_c1_scoring as S  # noqa: E402

    S.phase0_verify()
    for leg in S.C1_STRATS:
        S.resolve_panel_path(leg)
    panel, _meta, _ = S.build_scaled_panel(
        S.C1_STRATS, S.C1_ALLOCS, expect_1r=dict(S.EXPECTED_1R)
    )
    real = panel.sum(axis=1).to_numpy(dtype=float) * (M.ACCOUNT / S.ACCOUNT)
    ra = real[real != 0]

    syn, _ = M.make_series(
        sigma_d_pct=fit["sigma_d_pct"], mu_sigma=fit["mu_sigma"],
        shape=fit["shape"], z=fit["z"], seed=M.CELL_SEED_BASE - 1,
    )
    sa = syn[syn != 0]

    def mom(x):
        m = x - x.mean()
        return (
            float((m**3).mean() / (m**2).mean() ** 1.5),
            float((m**4).mean() / (m**2).mean() ** 2 - 3.0),
            float((x > 0).mean()),
            float(x.min()),
        )

    rs, rk, rw, rmin = mom(ra)
    ss, sk, sw, smin = mom(sa)
    return [
        "The A2 residual is not a range problem — it survives an **exact** parameter match. "
        "Re-drawing the fitted 4-tuple and comparing the moments the family does *not* "
        "parameterize shows why:",
        "",
        "| moment | real c1 (active days) | synthetic at identical (σ_d, μ/σ, shape, z) |",
        "|---|---|---|",
        f"| skewness | **{rs:+.3f}** | **{ss:+.3f}** |",
        f"| excess kurtosis | {rk:.2f} | {sk:.2f} |",
        f"| win fraction | {rw:.4f} | {sw:.4f} |",
        f"| worst single day | ${rmin:,.0f} | ${smin:,.0f} |",
        "",
        f"The real book is a **positively-skewed trend-rider** (skew {rs:+.2f}): frequent small "
        f"losses, rare very large wins. Its losses never approach the $3,000 EOD trail. The "
        f"declared shape axis cannot express that — `student_t4` is **symmetric**, so it returns "
        f"single days of ${smin:,.0f} that exhaust the entire drawdown allowance on their own, "
        f"and the two-point mixtures have bounded kurtosis by construction and cannot reach "
        f"{rk:.0f}.",
        "",
        "**Load-bearing conclusion — the 4-tuple omits skew.** For a path-dependent fixed-$ "
        "trailing barrier, survival is governed by the *loss-side* shape of the daily "
        "distribution, which `(σ_d, μ/σ, shape, z)` does not parameterize. Any successor family "
        "must carry an explicit skew / loss-tail dimension; matching the first two moments plus a "
        "symmetric tail class is demonstrably not sufficient (23.63pp error at exact fit).",
    ]


def profile_section(prof: dict) -> list[str]:
    if not prof:
        return ["_profile_positions.json not present — run `python profile_positions.py`._"]
    g = prof["grid_ranges"]
    out = [
        f"Declared grid ranges — σ_d ∈ [{g['sigma_d_pct_range'][0]}, {g['sigma_d_pct_range'][1]}]%, "
        f"μ/σ ∈ [{g['mu_sigma_range'][0]}, {g['mu_sigma_range'][1]}], "
        f"z ∈ [{g['z_range'][0]}, {g['z_range'][1]}].",
        "",
        "| book | reading | σ_d (% acct) | μ/σ | z | inside grid? |",
        "|---|---|---|---|---|---|",
    ]
    for b in prof["books"]:
        for tag, key in (("active-day", "active_day_reading"), ("all-day", "all_day_reading")):
            f = b[key]
            ir = f["in_range"]
            mark = lambda v, ok: f"{v} {'✅' if ok else '❌'}"  # noqa: E731
            inside = "yes" if all(ir.values()) else "**no**"
            # Hoist formats — nested same-quote f-strings are 3.12+ (PEP 701);
            # gate floor is 3.11 (pyproject requires-python / .venv-research).
            sigma_s = f"{f['sigma_d_pct']:.4f}"
            mu_s = f"{f['mu_sigma']:+.4f}"
            z_s = f"{f['z']:.4f}"
            out.append(
                f"| {b['book']} | {tag} | {mark(sigma_s, ir['sigma_d_pct'])} | "
                f"{mark(mu_s, ir['mu_sigma'])} | "
                f"{mark(z_s, ir['z'])} | {inside} |"
            )
    return out


def main() -> int:
    env = load("envelope.json")
    anch = load("anchors.json")
    prof = load("profile_positions.json")
    if not env:
        print("envelope.json missing — run the sweep first", file=sys.stderr)
        return 1

    cells = env.get("cells", [])
    adj = env.get("adjudication", {})
    cr = adj.get("ceiling_reading", {})
    gg = env.get("geometry_guard", {})

    L: list[str] = []
    A = L.append
    A("# Q-GEOFIT-1 — trailing-DD funding-envelope map — RESULTS")
    A("")
    A(f"**Verdict:** `{adj.get('verdict', 'PENDING')}`")
    A(f"**Brief:** [`{env['brief']}`](../../../{env['brief']}) · "
      f"**Signature:** `{env['signature']}`")
    A(f"**Gate pre-registration:** [`{env['gate_prereg']}`](../../../{env['gate_prereg']})")
    A(f"**Geometry:** {env['geometry']} · **Tier:** `{env['tier']}` · "
      f"**Floor:** bust ≤ {env['floor']['bust_ceiling']:.1%}, pass ≥ {env['floor']['pass_floor']:.0%}")
    A(f"**Sims:** {env['n_sims_per_seed']:,}/seed × 3 seeds · **cells scored:** {len(cells)}")
    A("")

    A("## Validation anchors (§2) — gate the interpretation of every grid cell")
    A("")
    if anch:
        A("| anchor | measured | published pin | Δ | verdict |")
        A("|---|---|---|---|---|")
        for arm, a in (anch.get("A1") or {}).items():
            A(f"| A1 engine repro {arm} | {a['headline_bust']:.2%} | {a['published_pin']:.2%} | "
              f"{a['abs_delta_pp']:.3f}pp | {'**MATCH**' if a['ok'] else '**MISMATCH**'} |")
        a2 = anch.get("A2") or {}
        if a2:
            A(f"| A2 profile sufficiency (nearest cell) | {a2.get('nearest_cell_bust', float('nan')):.2%} | "
              f"{a2.get('real_bust', float('nan')):.2%} (real c1) | "
              f"{a2.get('nearest_residual_pp', float('nan')):.3f}pp | "
              f"{'**OK**' if a2.get('nearest_ok') else '**MISS**'} |")
            A(f"| A2 off-grid exact fit (diagnostic) | {a2.get('offgrid_exact_bust', float('nan')):.2%} | "
              f"{a2.get('real_bust', float('nan')):.2%} (real c1) | "
              f"{a2.get('offgrid_exact_residual_pp', float('nan')):.3f}pp | "
              f"{'ok' if a2.get('offgrid_exact_ok') else 'miss'} |")
            A("")
            if a2.get("any_out_of_range"):
                oor = a2.get("out_of_range", {})
                A(f"> **The c1 fit falls OUTSIDE the declared grid** on: "
                  f"{', '.join(k for k, v in oor.items() if v)}. The nearest-cell row is therefore "
                  f"a *clamped* comparison, not a faithful fit — which is why the off-grid exact "
                  f"row is reported alongside it. Both miss, so the failure is not attributable to "
                  f"clamping. Book positions relative to the declared ranges are in §(iii).")
        A("")
        A(f"**Anchors hold:** `{anch.get('anchors_hold')}`")
    else:
        A("_anchors.json missing._")
    A("")

    A("## Why A2 missed — the family defect")
    A("")
    try:
        L.extend(skew_diagnostic(anch))
    except Exception as e:  # diagnostic only; never blocks the closure
        A(f"_skew diagnostic unavailable: {e}_")
    A("")

    grid_run = env.get("grid_executed", bool(cells))

    A("## (i) Boundary table — minimum μ/σ that clears, per (σ_d, shape, z)")
    A("")
    if grid_run:
        L.extend(boundary_table(cells))
    else:
        A("**NOT EXECUTED.** This is *not* a finding of \"nothing clears\" — the grid was never "
          "scored, so no cell has a bust/pass value at all. The two states are different claims "
          "and must not be conflated.")
        A("")
        A(f"> {env.get('grid_not_run_reason', '')}")
    A("")

    A("## (ii) σ_d ceiling — max daily vol fundable at any declared μ/σ")
    A("")
    if grid_run:
        L.extend(sigma_ceiling(cells))
    else:
        A("**NOT EXECUTED** — same reason as (i). No σ_d ceiling is claimed in either direction.")
    A("")

    A("## Interpretive readings the brief did not fix (declared at execution)")
    A("")
    A("§2 fixes the axes; these mechanics were chosen by the runner and are recorded so the "
      "successor brief can adopt or overturn them deliberately:")
    A("")
    A("- **R1 — μ and σ are ACTIVE-day moments.** §2 defines σ_d as \"daily vol on active days\", "
      "and μ/σ is the ratio of the same distribution's moments. This is what makes §2's own "
      "identity hold (0.10 × √252 ≈ 1.59 ≈ \"annualized Sharpe ≳ 1.6\"). Book positions are "
      "published on **both** readings in §(iii) rather than collapsing to one.")
    A("- **R2 — active-day draws are affinely standardized** to hit (μ, σ) exactly. The MC "
      "block-bootstraps the empirical series, so empirical moments are the effective cell "
      "parameters; unstandardized, the sampling error on μ (≈0.03σ at n≈1000) is the size of the "
      "whole μ/σ grid spacing (0.025) and would mislabel cells. Affine ⇒ skew/kurtosis preserved.")
    A("- **R3 — exact-count z mask** (`floor(N(1−z))` via permutation), so realized z equals "
      "declared z instead of carrying binomial noise.")
    A("- **R4 — zero-day PLACEMENT is uniform at random, and the brief never declared it.** "
      "`build_week_blocks` takes fixed Mon-anchored 5-day slices, so placement determines the "
      "within-block active count. A real sparse book *clusters* its idleness (a quiet week is "
      "five consecutive zeros), so **temporal clustering of inactivity is a second "
      "unparameterized dimension** alongside skew. A successor family must declare a placement "
      "law. **Direction unmeasured:** measured directly at frozen sims and the real book's "
      "parameters, the placement effect is −0.29pp (clustered − uniform), combined SE ≈1.37pp = "
      "**0.21σ, indistinguishable from zero** — see "
      "`lab/analysis/geofit_skew_probe_2026-07-25/`. An earlier directional claim (that uniform "
      "is the higher-bust, anti-clearing, therefore conservative choice) rested on a 2,000-sim "
      "proxy at non-c1 parameters and is **withdrawn**; no conservatism may be claimed from R4.")
    A("")

    A("## (iii) Book profile positions relative to the grid (context only — no re-scoring claim)")
    A("")
    L.extend(profile_section(prof))
    A("")

    A("## §4 accept/reject accounting")
    A("")
    if grid_run:
        A(f"- Practical cells (μ/σ ≤ 0.10): **{adj.get('n_practical', NA)}**")
        A(f"- Practical cells clearing the floor: **{adj.get('n_practical_clearing', NA)}**")
        A(f"- Diagnostic cells (μ/σ > 0.10) clearing: {adj.get('n_diagnostic_clearing', NA)}")
    else:
        A("**H-GEOFIT is neither accepted nor rejected.** §4's accept/reject rule is conditioned "
          "on \"**and** the validation anchors hold\" — they do not. No count of clearing cells "
          "exists, and none may be inferred. The hypothesis returns to the successor brief intact.")
    A("")
    if cr.get("brief_count_discrepancy"):
        A(f"> **Brief arithmetic slip recorded (independent of this closure).** §4 states "
          f"\"192 practical / 96 diagnostic\", but the declared predicate `μ/σ ≤ 0.10` partitions "
          f"the {cr.get('n_declared_cells')} declared cells as "
          f"**{cr.get('n_declared_practical')} practical / {cr.get('n_declared_diagnostic')} "
          f"diagnostic** — the stated counts require a strict `< 0.10`. §2's prose (\"a persistent "
          f"daily edge ratio **above** 0.10 …\") settles it in favour of `≤`, which is what the "
          f"runner executes. This is a defect in the frozen text, not in the run; it does not "
          f"affect the accept rule (≥1 clears) unless every clearer sits exactly on μ/σ = 0.10. "
          f"The successor brief should state the predicate and the counts consistently.")
        A("")
    if grid_run:
        A(f"**Geometry guard:** {gg.get('checked', 0)} cells attested, "
          f"{gg.get('violations', NA)} violations → `{gg.get('ok')}`. "
          f"(Every worker process re-applies the corrected-geometry patch locally and reports the "
          f"`dd_lock_offset_usd` it actually used; a parent-only patch would have silently scored "
          f"the whole grid at defective geometry.)")
    else:
        A("**Geometry guard:** not exercised — no grid cells were scored. It was proven live "
          "during smoke testing (6/6 workers attested `dd_lock_offset_usd = 1e6` under the "
          "process pool), and the anchor runs above were executed under the same corrected "
          "patch in-process.")
    A("")

    dest = _HERE / "RESULTS.md"
    dest.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"[written] {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
