"""Q-TRAINKILL-1 -- joint kill-record likelihood under mu=0 and mu=+0.10R.

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
PREREG = REPO / "docs" / "briefs" / "pre-registration" / "Q-TRAINKILL-1-verdict-preregistration.md"
TABLE = HERE / "TABLE.json"

MU_0 = 0.0
MU_BAR = 0.10
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


def row_p(row: dict, mu: float) -> float:
    event = row["event"]
    if row["mode"] == "one_arm":
        return p_event(event, mu, se_from_ci(row["ci"]))
    if row["mode"] == "both_arms":
        return p_event(event, mu, se_from_ci(row["ci_long"])) * p_event(
            event, mu, se_from_ci(row["ci_short"])
        )
    raise SystemExit(f"ABORT: unknown mode {row['mode']}")


def geo_mean(ps: list[float]) -> float:
    if not ps:
        return float("nan")
    return math.exp(sum(math.log(p) for p in ps) / len(ps))


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

    table = json.loads(TABLE.read_text(encoding="utf-8"))
    rows = table["rows"]
    if len(rows) != 15:
        raise SystemExit(f"ABORT: expected 15 rows, got {len(rows)}")

    scored_detail = []
    p0: list[float] = []
    pbar: list[float] = []
    bounded = []
    for row in rows:
        if row["class"] == "bounded":
            bounded.append({"id": row["id"], "reason": row["reason"]})
            continue
        a = row_p(row, MU_0)
        b = row_p(row, MU_BAR)
        if row["mode"] == "one_arm":
            se = se_from_ci(row["ci"])
            se_note = se
        else:
            se_note = {
                "long": se_from_ci(row["ci_long"]),
                "short": se_from_ci(row["ci_short"]),
            }
        scored_detail.append(
            {
                "id": row["id"],
                "event": row["event"],
                "mode": row["mode"],
                "se": se_note,
                "P_mu0": a,
                "P_mubar": b,
            }
        )
        p0.append(a)
        pbar.append(b)

    g0 = geo_mean(p0)
    gbar = geo_mean(pbar)
    core = reading(g0, gbar)

    # BOUNDED extremes: scored rows fixed; each bounded P in {EPS, 1-EPS}
    n_b = len(bounded)
    if n_b == 0:
        lo_read = hi_read = core
        g0_lo = g0_hi = g0
        gbar_lo = gbar_hi = gbar
    else:
        def g_with(fill: float, base: list[float]) -> float:
            return geo_mean(base + [fill] * n_b)

        g0_lo, g0_hi = g_with(EPS, p0), g_with(1.0 - EPS, p0)
        gbar_lo, gbar_hi = g_with(EPS, pbar), g_with(1.0 - EPS, pbar)
        lo_read = reading(g0_lo, gbar_lo)
        hi_read = reading(g0_hi, gbar_hi)

    if lo_read != hi_read:
        verdict = "AMBIGUOUS-HOLD"
        named = f"{lo_read}|{hi_read}"
    elif core == "MISCALIBRATED":
        verdict = "MISCALIBRATED"
        named = core
    else:
        verdict = "RESOLVED"
        named = core

    payload = {
        "prereg_sha256": prereg_sha,
        "n_set": 15,
        "n_scored": len(scored_detail),
        "n_bounded": n_b,
        "g0": g0,
        "gbar": gbar,
        "fit_floor": FIT_FLOOR,
        "core_reading": core,
        "bounded_lo_reading": lo_read,
        "bounded_hi_reading": hi_read,
        "verdict": verdict,
        "named_reading": named,
        "scored": scored_detail,
        "bounded": bounded,
    }
    (HERE / "RESULTS.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"n_scored {len(scored_detail)}  n_bounded {n_b}")
    print(f"g(0)={g0:.6g}  g(0.10)={gbar:.6g}  floor={FIT_FLOOR}")
    print(f"core {core}  bounded-extremes {lo_read} / {hi_read}")
    print(f"verdict {verdict}  named {named}")
    return payload


if __name__ == "__main__":
    main()
