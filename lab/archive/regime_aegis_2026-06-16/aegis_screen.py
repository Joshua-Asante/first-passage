"""Q-REGIME-AEGIS-1 Phase-1 screen — does USDJPY trend-persistence separate Aegis's win/loss regime?

Pre-registration: docs/briefs/pre-registration/Q-REGIME-AEGIS-1-verdict-preregistration.md (committed
81d529f, BEFORE this script). Brief: docs/briefs/Q-REGIME-AEGIS-1.md.

Validates the gold gate's already-logged-but-never-tested `aegis_flag` (TSMOM_252>0 AND KER_126>=0.12 on
USDJPY): do Aegis trades entered when USDJPY is trending lose more than when it isn't? Per-trade, causal
(detector uses USDJPY data through entry only). n=2 ceiling => weak backtest evidence; the frozen-flag
outcome gap is the decision-relevant number.

Run:  PYTHONPATH=core python lab/analysis/regime_aegis_2026-06-16/aegis_screen.py
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_REPO = next(p for p in _HERE.parents if (p / "CLAUDE.md").exists())
BARS = _REPO / "core" / "data" / "bar_data"
AEGIS_GLOB = str(_REPO / "lab" / "analysis" / "decompound_remc_2026-06-07" / "inputs" / "Aegis_USDJPY*.csv")

# frozen flag (gold_gate_shadow.py) + pre-registered gates
THR_KER126 = 0.12
AUC_BAR = 0.70
AUC_ROBUST_FLOOR = 0.65
EXCLUDE_YEAR = 2022
FLAG_GAP_RESOLVED_PP = 0.15   # loss-rate gap flag-ON minus flag-OFF
FLAG_GAP_FALSIFIED_PP = 0.05
FLAG_MIN_N = 10


def aegis_trades() -> pd.DataFrame:
    path = sorted(glob.glob(AEGIS_GLOB))[0]
    df = pd.read_csv(path, encoding="utf-8-sig")
    df.columns = [c.strip() for c in df.columns]
    ent = df[df["Type"].str.contains("Entry", na=False)].copy()
    ent["entry"] = pd.to_datetime(ent["Date and time"]).dt.normalize()
    ent["pnl"] = pd.to_numeric(ent["Net PnL USD"], errors="coerce")
    ent = ent.dropna(subset=["entry", "pnl"]).sort_values("entry")
    return ent[["entry", "pnl"]].reset_index(drop=True)


def usdjpy_daily() -> pd.Series:
    df = pd.read_csv(BARS / "USDJPY.csv", usecols=["time", "close"])
    t = pd.to_datetime(df["time"], format="ISO8601", utc=True).dt.tz_localize(None).dt.normalize()
    return pd.Series(df["close"].to_numpy(), index=t).sort_index().groupby(level=0).last()


def ker(close: pd.Series, n: int) -> pd.Series:
    return (close.diff(n).abs() / close.diff().abs().rolling(n).sum()).replace([np.inf, -np.inf], np.nan)


def tsmom(close: pd.Series, n: int) -> pd.Series:
    return close / close.shift(n) - 1.0


def auc_bad(score: np.ndarray, bad: np.ndarray) -> tuple[float, int, int]:
    """P[score higher on a BAD trade than a GOOD trade]. Inverted detector: high trend should -> bad."""
    m = ~np.isnan(score)
    s, b = score[m], bad[m]
    nbad, ngood = int((b == 1).sum()), int((b == 0).sum())
    if nbad == 0 or ngood == 0:
        return float("nan"), nbad, ngood
    order = np.argsort(s, kind="mergesort")
    ranks = np.empty(len(s)); ranks[order] = np.arange(1, len(s) + 1)
    ss = s[order]; i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and ss[j + 1] == ss[i]:
            j += 1
        if j > i:
            ranks[order[i:j + 1]] = (i + 1 + j + 1) / 2.0
        i = j + 1
    return float((ranks[b == 1].sum() - nbad * (nbad + 1) / 2.0) / (nbad * ngood)), nbad, ngood


def main() -> dict:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    tr = aegis_trades()
    jpy = usdjpy_daily()
    k = ker(jpy, 126); t252 = tsmom(jpy, 252)
    feat = pd.DataFrame({"ker126": k, "tsmom252": t252}).sort_index()
    feat = feat.reindex(feat.index.union(tr["entry"])).ffill().reindex(tr["entry"])
    tr["ker126"] = feat["ker126"].to_numpy()
    tr["tsmom252"] = feat["tsmom252"].to_numpy()
    tr["year"] = tr["entry"].dt.year
    tr["loss"] = (tr["pnl"] < 0).astype(int)
    med = tr["pnl"].median()
    tr["belowmed"] = (tr["pnl"] < med).astype(int)
    tr["flag_on"] = ((tr["tsmom252"] > 0) & (tr["ker126"] >= THR_KER126)).astype(int)

    valid = ~tr["ker126"].isna() & ~tr["tsmom252"].isna()
    v = tr[valid].copy()
    print("=" * 96)
    print("Q-REGIME-AEGIS-1 PHASE-1 — USDJPY trend-persistence vs Aegis trade outcomes (per-trade, causal)")
    print(f"trades {len(tr)} | valid (USDJPY warmup ok) {len(v)} | losses {int(v['loss'].sum())} "
          f"| WR {1 - v['loss'].mean():.1%} | dates {v['entry'].min().date()}->{v['entry'].max().date()}")
    print("=" * 96)

    ker_arr = v["ker126"].to_numpy(); t_arr = v["tsmom252"].to_numpy()
    loss = v["loss"].to_numpy(); below = v["belowmed"].to_numpy(); yr = v["year"].to_numpy()

    # ── AUC: detector higher on bad trades (inverted; high trend -> loss) ──
    auc_ker_loss, nb, ng = auc_bad(ker_arr, loss)
    auc_t_loss, _, _ = auc_bad(t_arr, loss)
    auc_ker_below, _, _ = auc_bad(ker_arr, below)
    print(f"\nAUC (P[USDJPY-trend higher on BAD trade]; >=0.70 separates, high trend -> Aegis bad):")
    print(f"   KER_126   vs loss      : {auc_ker_loss:.3f}  (bad {nb} / good {ng})")
    print(f"   TSMOM_252 vs loss      : {auc_t_loss:.3f}")
    print(f"   KER_126   vs below-med : {auc_ker_below:.3f}")

    PRIMARY = auc_ker_loss
    # robustness: 2022 excluded
    mex = yr != EXCLUDE_YEAR
    auc_ex22, nbx, ngx = auc_bad(ker_arr[mex], loss[mex])
    print(f"   KER_126 vs loss, 2022-excluded: {auc_ex22:.3f}  (bad {nbx} / good {ngx})")
    # LOYO
    loyo = {}
    for y in sorted(set(yr.tolist())):
        a, _, _ = auc_bad(ker_arr[yr != y], loss[yr != y])
        if not np.isnan(a):
            loyo[int(y)] = a
    loyo_min = min(loyo.values()) if loyo else float("nan")
    print(f"   LOYO KER_126 vs loss: " + ", ".join(f"{y}:{a:.3f}" for y, a in loyo.items()) + f"  | min {loyo_min:.3f}")

    # ── frozen flag ON/OFF (the decision-relevant test) ──
    on = v[v["flag_on"] == 1]; off = v[v["flag_on"] == 0]
    on_lr = on["loss"].mean() if len(on) else float("nan")
    off_lr = off["loss"].mean() if len(off) else float("nan")
    on_mp = on["pnl"].mean() if len(on) else float("nan")
    off_mp = off["pnl"].mean() if len(off) else float("nan")
    gap_pp = (on_lr - off_lr) if (len(on) and len(off)) else float("nan")
    print(f"\nFROZEN aegis_flag (TSMOM_252>0 AND KER_126>=0.12) ON/OFF — the logged rule under test:")
    print(f"   flag-ON  n={len(on):3d}  loss-rate {on_lr:.1%}  mean PnL ${on_mp:,.0f}")
    print(f"   flag-OFF n={len(off):3d}  loss-rate {off_lr:.1%}  mean PnL ${off_mp:,.0f}")
    print(f"   loss-rate gap (ON-OFF): {gap_pp:+.1%}  (RESOLVED>=+15pp / FALSIFIED<+5pp); mean-PnL worse-on-ON: {on_mp < off_mp}")

    # ── verdict (§6) ──
    robust_ok = (PRIMARY >= AUC_BAR) and (auc_ex22 >= AUC_ROBUST_FLOOR) and (loyo_min >= AUC_ROBUST_FLOOR)
    flag_material_resolved = (len(on) >= FLAG_MIN_N) and (gap_pp >= FLAG_GAP_RESOLVED_PP or on_mp < off_mp and gap_pp >= FLAG_GAP_RESOLVED_PP)
    flag_resolved = (len(on) >= FLAG_MIN_N) and (gap_pp >= FLAG_GAP_RESOLVED_PP)
    resolved = robust_ok and flag_resolved
    flag_immaterial = (gap_pp < FLAG_GAP_FALSIFIED_PP and not (on_mp < off_mp))
    falsified = (0.40 <= PRIMARY <= 0.60) or (auc_ex22 < 0.60) or flag_immaterial or (len(on) < FLAG_MIN_N)
    verdict = "RESOLVED" if resolved else ("FALSIFIED" if falsified else "AMBIGUOUS-HOLD")

    print("\n" + "=" * 96)
    print(f"## VERDICT (pre-registered §6): {verdict}")
    print(f"   primary AUC {PRIMARY:.3f} (bar {AUC_BAR}) | ex-2022 {auc_ex22:.3f} | LOYO-min {loyo_min:.3f} (floor {AUC_ROBUST_FLOOR})")
    print(f"   frozen-flag loss-rate gap {gap_pp:+.1%}, flag-ON n={len(on)} (need >=10 and >=+15pp for RESOLVED)")
    print("=" * 96)

    out = {
        "investigation": "Q-REGIME-AEGIS-1 Phase-1 screen", "prereg_commit": "81d529f",
        "n_trades": len(tr), "n_valid": len(v), "WR": float(1 - v["loss"].mean()),
        "auc": {"ker126_vs_loss": auc_ker_loss, "tsmom252_vs_loss": auc_t_loss,
                "ker126_vs_belowmed": auc_ker_below, "ker126_vs_loss_ex2022": auc_ex22,
                "loyo": loyo, "loyo_min": loyo_min},
        "frozen_flag": {"on_n": len(on), "off_n": len(off), "on_loss_rate": on_lr, "off_loss_rate": off_lr,
                        "on_mean_pnl": on_mp, "off_mean_pnl": off_mp, "loss_rate_gap_pp": gap_pp},
        "gates": {"AUC_BAR": AUC_BAR, "ROBUST_FLOOR": AUC_ROBUST_FLOOR, "flag_gap_resolved": FLAG_GAP_RESOLVED_PP,
                  "flag_gap_falsified": FLAG_GAP_FALSIFIED_PP, "flag_min_n": FLAG_MIN_N},
        "verdict": verdict,
    }
    (_HERE / "aegis_screen.json").write_text(json.dumps(out, indent=2, default=str))
    print(f"\nwrote {_HERE / 'aegis_screen.json'}")
    return out


if __name__ == "__main__":
    main()
