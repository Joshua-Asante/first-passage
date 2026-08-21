"""Q-CONDVAL-1 -- R-term arithmetic on already-committed S1b scalars.

Freeze-before-substitute: sha256 the prereg bytes BEFORE opening s1b_results.json.
Stdlib only. $0 / K=0. Does not read vendor bars.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
PREREG = REPO / "docs" / "briefs" / "pre-registration" / "Q-CONDVAL-1-verdict-preregistration.md"
S1B_JSON = REPO / "lab" / "analysis" / "_inbox" / "rangestate_mcl_2026-08" / "s1b_results.json"

# Frozen §A (must match the prereg; changing these after substitute voids the run)
RR = 2.5
WR = 0.36
R_DOLLARS = 75.0
RT_DOLLARS = 4.12
MATERIAL_FRAC = 0.50
COST_MULT = 4.0


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> dict:
    if not PREREG.is_file():
        raise SystemExit(f"ABORT: prereg missing: {PREREG}")
    prereg_sha = sha256_file(PREREG)
    print(f"prereg_sha256 {prereg_sha}")
    print(f"prereg_path   {PREREG.relative_to(REPO).as_posix()}")

    e_box = WR * RR - (1.0 - WR)
    if e_box <= 0:
        verdict = "AMBIGUOUS-HOLD"
        payload = {
            "verdict": verdict,
            "reason": "E_box <= 0 at gating cell",
            "prereg_sha256": prereg_sha,
            "E_box": e_box,
        }
        (HERE / "RESULTS.json").write_text(json.dumps(payload, indent=2) + "\n")
        return payload

    hurdle_4x = COST_MULT * RT_DOLLARS / R_DOLLARS
    bar_de = MATERIAL_FRAC * hurdle_4x
    l_star = bar_de / e_box

    raw = json.loads(S1B_JSON.read_text())
    if "gateHit" not in raw or "p_up_unconditional" not in raw:
        verdict = "AMBIGUOUS-HOLD"
        payload = {
            "verdict": verdict,
            "reason": "committed key missing",
            "prereg_sha256": prereg_sha,
            "keys_present": sorted(raw),
        }
        (HERE / "RESULTS.json").write_text(json.dumps(payload, indent=2) + "\n")
        return payload

    p_cond = float(raw["gateHit"])
    p_uncond = float(raw["p_up_unconditional"])
    lift = p_cond - p_uncond
    delta_e = lift * e_box
    verdict = "RESOLVED" if lift >= l_star else "FALSIFIED"

    # Disclosure only -- never gates
    corners = []
    for wr in (0.30, 0.36, 0.42):
        for rr in (2.0, 2.5, 3.0):
            e = wr * rr - (1.0 - wr)
            if e <= 0:
                corners.append({"WR": wr, "rr": rr, "E_box": e, "status": "excluded_nonpositive"})
                continue
            corners.append(
                {
                    "WR": wr,
                    "rr": rr,
                    "E_box": e,
                    "delta_E": lift * e,
                    "clears_gating_bar": (lift * e) >= bar_de,
                }
            )
    envelope_ends = []
    for r_dol, rt in ((75.0, 4.12), (200.0, 2.82)):
        h = COST_MULT * rt / r_dol
        envelope_ends.append(
            {
                "R": r_dol,
                "RT": rt,
                "hurdle_4x": h,
                "bar_dE_at_0_50": 0.50 * h,
                "gating_delta_E_clears": delta_e >= (0.50 * h),
            }
        )

    payload = {
        "verdict": verdict,
        "prereg_sha256": prereg_sha,
        "frozen": {
            "rr": RR,
            "WR": WR,
            "R_dollars": R_DOLLARS,
            "RT_dollars": RT_DOLLARS,
            "material_frac": MATERIAL_FRAC,
            "E_box": e_box,
            "hurdle_4x": hurdle_4x,
            "bar_dE": bar_de,
            "L_star": l_star,
        },
        "measured": {
            "source": S1B_JSON.relative_to(REPO).as_posix(),
            "gateHit": p_cond,
            "p_up_unconditional": p_uncond,
            "L": lift,
            "delta_E": delta_e,
            "L_minus_L_star": lift - l_star,
        },
        "disclosure_corners": corners,
        "disclosure_envelope": envelope_ends,
        "used_0_60": False,
        "used_iaaft_excess": False,
        "spend": 0.0,
        "K": 0,
    }
    (HERE / "RESULTS.json").write_text(json.dumps(payload, indent=2) + "\n")
    print(f"L            {lift:.6f}")
    print(f"L_star       {l_star:.6f}")
    print(f"delta_E      {delta_e:.6f}")
    print(f"bar_dE       {bar_de:.6f}")
    print(f"verdict      {verdict}")
    return payload


if __name__ == "__main__":
    main()
