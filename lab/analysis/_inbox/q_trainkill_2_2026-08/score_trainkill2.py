"""Q-TRAINKILL-2 -- recovery + named alternate DGPs.

Freeze-before-table: sha256 the prereg bytes BEFORE opening TABLE.json.
Stdlib only. $0 / K=0.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
PREREG = REPO / "docs" / "briefs" / "pre-registration" / "Q-TRAINKILL-2-verdict-preregistration.md"
TABLE = HERE / "TABLE.json"
EXPECTED_SHA = "86049b89b413b33430e7dfe31d9fc5de5cc46b81c0f23f3ea7877d78c7605b5d"

MU_0 = 0.0
MU_BAR = 0.10
MU_NEG = -0.10
Z = 1.96
FIT_FLOOR = 0.05
EPS = 1e-6


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def phi(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def se_from_ci(ci: list[float]) -> float:
    lo, hi = float(ci[0]), float(ci[1])
    width = hi - lo
    if width <= 0:
        raise SystemExit(f"ABORT: non-positive CI width {ci}")
    return width / 3.92


def p_event(event: str, mu: float, se: float) -> float:
    p_f = phi(-Z - mu / se)
    p_c = phi(mu / se - Z)
    p_a = 1.0 - p_f - p_c
    raw = {"FALSIFIED": p_f, "CLEARED": p_c, "AMBIGUOUS": p_a}[event]
    return min(1.0 - EPS, max(EPS, raw))


def arm_p(row: dict, mu: float) -> tuple[float, float] | float:
    event = row["event"]
    if row["mode"] == "one_arm":
        return p_event(event, mu, se_from_ci(row["ci"]))
    p_l = p_event(event, mu, se_from_ci(row["ci_long"]))
    p_s = p_event(event, mu, se_from_ci(row["ci_short"]))
    return p_l, p_s


def row_p(row: dict, mu: float, joint: str) -> float:
    arms = arm_p(row, mu)
    if isinstance(arms, float):
        return arms
    p_l, p_s = arms
    if joint == "indep":
        return p_l * p_s
    if joint == "frechet_hi":
        return min(p_l, p_s)
    if joint == "frechet_lo":
        return max(0.0, p_l + p_s - 1.0)
    raise SystemExit(f"ABORT: unknown joint {joint}")


def geo_mean(ps: list[float]) -> float:
    if not ps:
        return float("nan")
    return math.exp(sum(math.log(max(EPS, p)) for p in ps) / len(ps))


def reading(g0: float, gbar: float) -> str:
    zero_fits = g0 >= FIT_FLOOR
    bar_fits = gbar >= FIT_FLOOR
    if bar_fits:
        return "GATES-UNDERPOWERED"
    if zero_fits:
        return "KILLS-INFORMATIVE"
    return "MISCALIBRATED"


def main() -> dict:
    if not PREREG.is_file():
        raise SystemExit(f"ABORT: prereg missing: {PREREG}")
    prereg_sha = sha256_file(PREREG)
    print(f"prereg_sha256 {prereg_sha}")
    print(f"prereg_path   {PREREG.relative_to(REPO).as_posix()}")
    if prereg_sha != EXPECTED_SHA:
        raise SystemExit(f"ABORT: prereg sha drifted from freeze {EXPECTED_SHA}")

    table = json.loads(TABLE.read_text(encoding="utf-8"))
    rows = table["rows"]
    if len(rows) != 15:
        raise SystemExit(f"ABORT: expected 15 rows, got {len(rows)}")

    scored: list[dict] = []
    bounded: list[dict] = []
    n_promoted = 0
    for row in rows:
        if row["class"] == "bounded":
            bounded.append({"id": row["id"], "reason": row["reason"]})
            continue
        if row.get("promoted"):
            n_promoted += 1
        scored.append(row)

    def gs(mu: float, joint: str) -> tuple[float, list[dict]]:
        ps = []
        detail = []
        for row in scored:
            p = row_p(row, mu, joint)
            ps.append(p)
            detail.append({"id": row["id"], "event": row["event"], "mode": row["mode"], "P": p})
        return geo_mean(ps), detail

    g0, d0 = gs(MU_0, "indep")
    gbar, dbar = gs(MU_BAR, "indep")
    gneg, dneg = gs(MU_NEG, "indep")
    gdep, ddep = gs(MU_0, "frechet_hi")
    gdep_lo, _ = gs(MU_0, "frechet_lo")
    core = reading(g0, gbar)

    n_b = len(bounded)
    p0 = [x["P"] for x in d0]
    pbar = [x["P"] for x in dbar]
    if n_b == 0:
        lo_read = hi_read = core
    else:
        def g_with(fill: float, base: list[float]) -> float:
            return geo_mean(base + [fill] * n_b)

        lo_read = reading(g_with(EPS, p0), g_with(EPS, pbar))
        hi_read = reading(g_with(1.0 - EPS, p0), g_with(1.0 - EPS, pbar))

    limb1_fire = n_promoted >= 1 and lo_read == hi_read
    if limb1_fire:
        if lo_read == "MISCALIBRATED":
            verdict = "MISCALIBRATED"
        else:
            verdict = "RESOLVED"
        named = lo_read
        limb = 1
    else:
        limb = 2
        neg_fits = gneg >= FIT_FLOOR
        dep_fits = gdep >= FIT_FLOOR
        if neg_fits and dep_fits:
            verdict = "AMBIGUOUS-HOLD"
            named = "NEG-FAMILIES|KILLS-INFORMATIVE-DEP"
        elif neg_fits:
            verdict = "RESOLVED"
            named = "NEG-FAMILIES"
        elif dep_fits:
            verdict = "RESOLVED"
            named = "KILLS-INFORMATIVE-DEP"
        elif not scored:
            verdict = "AMBIGUOUS-HOLD"
            named = "n*=0"
        else:
            verdict = "MISCALIBRATED"
            named = "MISCALIBRATED"

    payload = {
        "prereg_sha256": prereg_sha,
        "n_set": 15,
        "n_scored": len(scored),
        "n_bounded": n_b,
        "n_promoted": n_promoted,
        "promoted": table.get("promoted", []),
        "g0": g0,
        "gbar": gbar,
        "gneg": gneg,
        "gdep_zero": gdep,
        "gdep_lo_disclosed": gdep_lo,
        "fit_floor": FIT_FLOOR,
        "core_reading": core,
        "bounded_lo_reading": lo_read,
        "bounded_hi_reading": hi_read,
        "limb1_fire": limb1_fire,
        "limb": limb,
        "verdict": verdict,
        "named_reading": named,
        "P_mu0": d0,
        "P_mubar": dbar,
        "P_neg": dneg,
        "P_dep_zero": ddep,
        "bounded": bounded,
    }
    (HERE / "RESULTS.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"n_scored {len(scored)}  n_bounded {n_b}  n_promoted {n_promoted}")
    print(f"g(0)={g0:.6g}  g(+0.10)={gbar:.6g}  g(-0.10)={gneg:.6g}  g(DEP-ZERO)={gdep:.6g}")
    print(f"g(DEP-lo disclosed)={gdep_lo:.6g}  floor={FIT_FLOOR}")
    print(f"core {core}  bounded-extremes {lo_read} / {hi_read}  limb1_fire {limb1_fire}")
    print(f"limb {limb}  verdict {verdict}  named {named}")
    return payload


if __name__ == "__main__":
    main()
