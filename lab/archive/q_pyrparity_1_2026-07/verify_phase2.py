"""Q-PYRPARITY-1 Phase 2 — Branch B equity-normalized qty-ratio verification.

Pairs entry fills by (timestamp, signal cohort). Statistic per Phase 0 / pre-reg:
  [qty/equity](r0/2) / [qty/equity](r0)
Add fills normalize on the parent base entry's equity (initialSize capture bar),
not the add-bar equity.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
INIT_CAPITAL = 200_000.0
BAND_FILL = 0.02  # accept if |stat - 0.5| <= this
BAND_MEDIAN = 0.005
FILL_FRAC = 0.95
TARGET = 0.5

PANELS = {
    "MYM": {
        "r0": HERE / "MYM_r070_f5ecb.csv",
        "r_half": HERE / "MYM_r035_8d6b5.csv",
        "r0_label": "0.70",
        "r_half_label": "0.35",
    },
    "MNQ": {
        "r0": HERE / "MNQ_r037_9b6c8.csv",
        "r_half": HERE / "MNQ_r0185_b2723.csv",
        "r0_label": "0.37",
        "r_half_label": "0.185",
    },
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_entries(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    ent = df[df["Type"].astype(str).str.contains("Entry", case=False)].copy()
    ent["ts"] = pd.to_datetime(ent["Date and time"])
    ent["qty"] = ent["Size (qty)"].astype(float)
    ent["net_pnl"] = ent["Net PnL USD"].astype(float)
    ent["cum_pnl"] = ent["Cumulative PnL USD"].astype(float)
    # Equity at entry = capital + cum before this trade's PnL lands.
    # Export stamps post-trade cum on both entry and exit rows of the same trade#.
    ent["equity_at_entry"] = INIT_CAPITAL + (ent["cum_pnl"] - ent["net_pnl"])
    ent["cohort"] = np.where(
        ent["Signal"].astype(str).str.contains("Add", case=False), "add", "base"
    )
    return ent.reset_index(drop=True)


def attach_entry_bar_equity(ent: pd.DataFrame) -> pd.DataFrame:
    """For add fills, replace equity with the most recent prior base entry equity.

    Phase 0: addSize = initialSize * pyramid%; initialSize captured at base entry.
    """
    out = ent.sort_values("ts").copy()
    last_base_eq: float | None = None
    eqs: list[float] = []
    for _, row in out.iterrows():
        if row["cohort"] == "base":
            last_base_eq = float(row["equity_at_entry"])
            eqs.append(last_base_eq)
        else:
            if last_base_eq is None:
                eqs.append(float(row["equity_at_entry"]))  # orphan add — flag later
            else:
                eqs.append(last_base_eq)
    out["equity_norm"] = eqs
    out["qty_per_eq"] = out["qty"] / out["equity_norm"]
    return out


def pair_cohort(r0: pd.DataFrame, rh: pd.DataFrame, cohort: str) -> dict:
    a = r0[r0["cohort"] == cohort].set_index("ts").sort_index()
    b = rh[rh["cohort"] == cohort].set_index("ts").sort_index()
    common = a.index.intersection(b.index)
    only_r0 = a.index.difference(b.index)
    only_rh = b.index.difference(a.index)

    paired = []
    for ts in common:
        # duplicate timestamps rare; take first if multi
        ra = a.loc[ts]
        rb = b.loc[ts]
        if isinstance(ra, pd.DataFrame):
            ra = ra.iloc[0]
        if isinstance(rb, pd.DataFrame):
            rb = rb.iloc[0]
        raw_ratio = float(rb["qty"] / ra["qty"]) if ra["qty"] else float("nan")
        stat = float(rb["qty_per_eq"] / ra["qty_per_eq"]) if ra["qty_per_eq"] else float("nan")
        paired.append(
            {
                "ts": str(ts),
                "qty_r0": float(ra["qty"]),
                "qty_rh": float(rb["qty"]),
                "eq_r0": float(ra["equity_norm"]),
                "eq_rh": float(rb["equity_norm"]),
                "raw_qty_ratio": raw_ratio,
                "stat_branch_b": stat,
                "in_band": abs(stat - TARGET) <= BAND_FILL,
            }
        )

    stats = np.array([p["stat_branch_b"] for p in paired], dtype=float)
    n = len(stats)
    n_in = int(np.sum(np.abs(stats - TARGET) <= BAND_FILL)) if n else 0
    median = float(np.median(stats)) if n else float("nan")
    return {
        "cohort": cohort,
        "n_r0": int(len(a)),
        "n_rh": int(len(b)),
        "n_paired": n,
        "n_only_r0": int(len(only_r0)),
        "n_only_rh": int(len(only_rh)),
        "only_r0_ts": [str(t) for t in only_r0[:20]],
        "only_rh_ts": [str(t) for t in only_rh[:20]],
        "frac_in_band": (n_in / n) if n else float("nan"),
        "n_in_band": n_in,
        "median": median,
        "mean": float(np.mean(stats)) if n else float("nan"),
        "min": float(np.min(stats)) if n else float("nan"),
        "max": float(np.max(stats)) if n else float("nan"),
        "p05": float(np.percentile(stats, 5)) if n else float("nan"),
        "p95": float(np.percentile(stats, 95)) if n else float("nan"),
        "accept_fill_band": bool(n and (n_in / n) >= FILL_FRAC),
        "accept_median_band": bool(n and abs(median - TARGET) <= BAND_MEDIAN),
        "paired_sample": paired[:5],
        "raw_qty_ratio_median": float(np.median([p["raw_qty_ratio"] for p in paired]))
        if paired
        else float("nan"),
    }


def score_leg(leg: str, cfg: dict) -> dict:
    r0 = attach_entry_bar_equity(load_entries(cfg["r0"]))
    rh = attach_entry_bar_equity(load_entries(cfg["r_half"]))
    base = pair_cohort(r0, rh, "base")
    add = pair_cohort(r0, rh, "add")

    # Timestamp identity: all paired entries should also have matching exits —
    # entry-time pairing is the §4 signal-path check; count drift handled below.
    add_count_drop = add["n_rh"] < add["n_r0"]
    lists_misaligned = (
        base["n_only_r0"] > 0
        or base["n_only_rh"] > 0
        or add["n_only_r0"] > 0
        or add["n_only_rh"] > 0
    )

    bands_ok = all(
        [
            base["accept_fill_band"],
            base["accept_median_band"],
            add["accept_fill_band"],
            add["accept_median_band"],
        ]
    )

    if add_count_drop:
        verdict = "FALSIFIED-NONPROPORTIONAL"
        reason = "add cohort fill count dropped run-to-run"
    elif lists_misaligned and not bands_ok:
        verdict = "AMBIGUOUS-HOLD"
        reason = "trade lists misaligned (non-add-clipping) and bands not cleanly met"
    elif lists_misaligned and bands_ok:
        # Misalignment with still-passing paired bands — still AMBIGUOUS per §4
        # (risk input may touch signal path via day-stop / halt gates).
        verdict = "AMBIGUOUS-HOLD"
        reason = "trade lists misaligned (count/timing drift); paired subset may pass bands"
    elif bands_ok:
        verdict = "RESOLVED-PROPORTIONAL"
        reason = "both cohorts meet §4 fill + median bands; timestamps pair cleanly"
    else:
        # Clean pairing but bands fail
        med_fail = (
            abs(base["median"] - TARGET) > 0.02 or abs(add["median"] - TARGET) > 0.02
        )
        if med_fail:
            verdict = "FALSIFIED-NONPROPORTIONAL"
            reason = "cohort median outside 0.500 ± 0.02"
        else:
            verdict = "AMBIGUOUS-HOLD"
            reason = "pairing clean but fill-frac or tight median band not met"

    return {
        "leg": leg,
        "r0_file": cfg["r0"].name,
        "r_half_file": cfg["r_half"].name,
        "r0_sha256": sha256(cfg["r0"]),
        "r_half_sha256": sha256(cfg["r_half"]),
        "r0_label": cfg["r0_label"],
        "r_half_label": cfg["r_half_label"],
        "base": base,
        "add": add,
        "add_count_drop": add_count_drop,
        "lists_misaligned": lists_misaligned,
        "bands_ok": bands_ok,
        "leg_verdict": verdict,
        "reason": reason,
    }


def main() -> None:
    legs = {leg: score_leg(leg, cfg) for leg, cfg in PANELS.items()}
    verdicts = {leg: r["leg_verdict"] for leg, r in legs.items()}

    # Portfolio-level: any FALSIFIED wins; else any AMBIGUOUS; else RESOLVED
    if any(v == "FALSIFIED-NONPROPORTIONAL" for v in verdicts.values()):
        overall = "FALSIFIED-NONPROPORTIONAL"
    elif any(v == "AMBIGUOUS-HOLD" for v in verdicts.values()):
        overall = "AMBIGUOUS-HOLD"
    else:
        overall = "RESOLVED-PROPORTIONAL"

    report = {
        "brief": "Q-PYRPARITY-1",
        "branch": "B",
        "init_capital": INIT_CAPITAL,
        "bands": {"fill": BAND_FILL, "median": BAND_MEDIAN, "fill_frac": FILL_FRAC},
        "overall_verdict": overall,
        "legs": legs,
    }
    out = HERE / "phase2_report.json"
    # Drop bulky paired samples from nested for cleaner JSON? keep sample of 5.
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(json.dumps({"overall": overall, "per_leg": verdicts}, indent=2))
    for leg, r in legs.items():
        print(f"\n=== {leg} ({r['reason']}) ===")
        for cohort in ("base", "add"):
            c = r[cohort]
            print(
                f"  {cohort}: n_r0={c['n_r0']} n_rh={c['n_rh']} paired={c['n_paired']} "
                f"only_r0={c['n_only_r0']} only_rh={c['n_only_rh']} | "
                f"median={c['median']:.6f} frac_in_band={c['frac_in_band']:.4f} "
                f"raw_qty_med={c['raw_qty_ratio_median']:.4f}"
            )


if __name__ == "__main__":
    main()
