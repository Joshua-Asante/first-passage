"""C5 — integer-contract Bulenox re-MC (cap-aware, cost-aware, time-matched ATR).

Layers onto the C4 pipeline (FF DJ30 + clean NAS100, static tier balance,
PRE_SHOCK_1R-pinned ideal panel, C2-off gate arm):
  per-trade integer ratio r_i = int_qty_i / ideal_qty_i, where
  ideal_qty_i = B*risk% / (1.2 * ATR_fut(entry_i) * $/pt)   [futures ATR(11),
  roll-masked, time-matched at each trade's entry bar — era-correct]

Bulenox primary-confirmed inputs (2026-07-03 sweep):
  caps (Option 1): 25K:30 / 50K:70 / 100K:120 / 150K:150 / 250K:250 micros
  target 6.0% all tiers; trailing DD $1.5K/2.5K/3K/4.5K/5.5K (= firm_rules);
  flat before 15:59 CT (17:00 ET boundary = C4 model, correct);
  all-in commissions MNQ/MYM $0.61/side; both tick $0.50 -> RT+1-tick-slip
  cost = $2.22/contract round turn.

Cap policy (design choice for the editions, documented): RESERVE — base is
capped at floor(cap/(1+pyr)) so the pyramid add always fits at full ratio;
preserves the edge's shape (pyramid IS the edge) at the cost of base size.
Assumes ONE strategy per master account (copy fan-out), so caps aren't shared.

Arms: gate = integer + costs + token-trade inactivity mitigation (limit 60);
      sensitivities = no-cost, and unmitigated inactivity=5 at 150K.
"""
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(r"C:/Users/joshu/multi_firm_operations/.claude/worktrees/adoring-nobel-143d23")
for p in (REPO / "core", REPO / "lab/analysis/bulenox_futures_remc_2026-07-01",
          REPO / "lab/analysis/futures_conversion_2026-07-01"):
    sys.path.insert(0, str(p))

from dd_protection import DD_TRIGGER  # noqa: E402
from firm_rules import FIRM_RULES  # noqa: E402
from portfolio_mc import (  # noqa: E402
    ALLOCATIONS, BASELINE_BALANCE, PEPPERSTONE_PANELS, PRE_SHOCK_1R,
    SEEDS, SIMS_PER_SEED, build_week_blocks, run_seed, _normalize_tv_columns,
)
from force_flat_transform import bars_utc_to_et, force_flat_csv  # noqa: E402
import roll_mask as rm  # noqa: E402

BAR_DIR = REPO / "core" / "data" / "bar_data"
ATR_LEN = 11
RT_COST = 2.22  # $/contract round turn: $0.61x2 all-in + 1 tick ($0.50) x2 slip

LEGS = {
    "striker":        dict(csv=PEPPERSTONE_PANELS["striker"], fut="YM", dpp=0.50,
                           risk=0.0070, pyr=7.5, sl_mult=1.20, forceflat=True),
    "striker_nas100": dict(csv=PEPPERSTONE_PANELS["striker_nas100"], fut="NQ", dpp=2.00,
                           risk=0.0037, pyr=10.0, sl_mult=1.20, forceflat=False),
}
CAPS = {"Bulenox_25K": 30, "Bulenox_50K": 70, "Bulenox_100K": 120,
        "Bulenox_150K": 150, "Bulenox_250K": 250}
TIERS = list(CAPS)


def atr_series_et(sym: str) -> pd.Series:
    """Roll-masked RMA ATR(11) on the futures panel, indexed by tz-naive ET bar time."""
    b = rm.flag_roll_seams(pd.read_csv(BAR_DIR / f"{sym}_M15.csv"), symbol=sym)
    b = b[~b["roll_seam"]].reset_index(drop=True)
    prev_close = b["close"].shift(1)
    tr = pd.concat([b["high"] - b["low"], (b["high"] - prev_close).abs(),
                    (b["low"] - prev_close).abs()], axis=1).max(axis=1)
    atr = tr.ewm(alpha=1.0 / ATR_LEN, adjust=False, min_periods=ATR_LEN).mean()
    t = (pd.to_datetime(b["time"], utc=True).dt.tz_convert("America/New_York")
         .dt.tz_localize(None))
    return pd.Series(atr.values, index=pd.DatetimeIndex(t)).dropna().sort_index()


def load_leg_trades(leg: str) -> pd.DataFrame:
    """One row per Trade # with entry_dt, exit_date, pnl, is_add, parent linkage."""
    cfg = LEGS[leg]
    raw = pd.read_csv(cfg["csv"], encoding="utf-8-sig")
    if cfg["forceflat"]:
        bars = bars_utc_to_et(pd.read_csv(BAR_DIR / "US30_M15.csv"))
        df = force_flat_csv(raw, bars)
    else:
        df = _normalize_tv_columns(raw).copy()
    df["_dt"] = pd.to_datetime(df["Date and time"])
    ent = df[df["Type"].astype(str).str.startswith("Entry")].set_index("Trade #")
    ext = df[df["Type"].astype(str).str.startswith("Exit")].set_index("Trade #")
    out = pd.DataFrame({
        "entry_dt": ent["_dt"], "signal": ent["Signal"].astype(str),
        "exit_dt": ext["_dt"], "pnl": ext["Net P&L USD"].astype(float),
    })
    out["is_add"] = out["signal"].eq("Long Add")
    # pair each add to the base trade whose [entry, exit] window contains it
    bases = out[~out["is_add"]]
    parent = {}
    for tnum, r in out[out["is_add"]].iterrows():
        cand = bases[(bases["entry_dt"] <= r["entry_dt"]) & (bases["exit_dt"] >= r["entry_dt"])]
        if len(cand) != 1:
            raise ValueError(f"{leg} add #{tnum}: {len(cand)} parent candidates")
        parent[tnum] = cand.index[0]
    out["parent"] = pd.Series(parent)
    out["exit_date"] = out["exit_dt"].dt.normalize()
    return out


def integer_panel(tier: str, *, with_costs: bool):
    """(panel, stats) — ideal static-B panel x per-trade integer ratio, minus costs."""
    firm = FIRM_RULES[tier]
    B = float(firm["starting_balance"])
    cap = CAPS[tier]
    rows, stats = [], {}
    for leg, cfg in LEGS.items():
        atr = atr_series_et(cfg["fut"])
        tr = load_leg_trades(leg)
        # time-matched ATR at entry (asof backward on the ET bar index)
        idx = atr.index.searchsorted(tr["entry_dt"].values, side="right") - 1
        if (idx < 0).any():
            raise ValueError(f"{leg}: entry before first ATR bar")
        tr["atr"] = atr.values[idx]
        tr["ideal"] = (B * cfg["risk"]) / (cfg["sl_mult"] * tr["atr"] * cfg["dpp"])
        base_cap = math.floor(cap / (1.0 + cfg["pyr"]))          # RESERVE policy
        tr["base_int"] = np.minimum(np.floor(tr["ideal"]), base_cap).astype(int)
        # per-leg quantities + ratios
        qty, ratio = {}, {}
        for tnum, r in tr.iterrows():
            if not r["is_add"]:
                qty[tnum] = r["base_int"]
                ratio[tnum] = r["base_int"] / r["ideal"] if r["ideal"] > 0 else 0.0
            else:
                p = tr.loc[r["parent"]]
                add_int = int(math.floor(p["base_int"] * cfg["pyr"])) if p["base_int"] > 0 else 0
                add_int = min(add_int, cap - int(p["base_int"]))
                ideal_add = p["ideal"] * cfg["pyr"]
                qty[tnum] = add_int
                ratio[tnum] = add_int / ideal_add if ideal_add > 0 else 0.0
        tr["qty"] = pd.Series(qty)
        tr["ratio"] = pd.Series(ratio)
        scale = (ALLOCATIONS[leg] * BASELINE_BALANCE / PRE_SHOCK_1R[leg]) * (B / BASELINE_BALANCE)
        tr["pnl_adj"] = tr["pnl"] * scale * tr["ratio"]
        if with_costs:
            tr["pnl_adj"] -= tr["qty"] * RT_COST
        s = tr.groupby("exit_date")["pnl_adj"].sum()
        s.name = leg
        rows.append(s)
        b_mask, a_mask = ~tr["is_add"], tr["is_add"]
        stats[leg] = {
            "n_base": int(b_mask.sum()), "n_add": int(a_mask.sum()),
            "skipped_base": int((tr.loc[b_mask, "qty"] == 0).sum()),
            "skipped_add": int((tr.loc[a_mask, "qty"] == 0).sum()),
            "mean_ratio_base": float(tr.loc[b_mask & (tr["ideal"] > 0), "ratio"].mean()),
            "mean_ratio_add": float(tr.loc[a_mask, "ratio"].mean()) if a_mask.any() else float("nan"),
            "cap_bound_base": int((np.floor(tr.loc[b_mask, "ideal"]) > base_cap).sum()),
            "base_cap": base_cap,
        }
    panel = pd.concat(rows, axis=1)
    bdays = pd.bdate_range(panel.index.min(), panel.index.max())
    panel = panel.reindex(bdays).fillna(0.0)
    return panel, stats


def run_tier(tier: str, *, with_costs: bool, inactivity: int | None = None,
             dd_scale: float = 1.0):
    firm = FIRM_RULES[tier]
    B = float(firm["starting_balance"])
    panel, stats = integer_panel(tier, with_costs=with_costs)
    blocks = build_week_blocks(panel)
    firm_kwargs = {
        "starting_equity": B, "dd_type": firm["dd_type"],
        "trailing_dd_pct": -firm["max_dd_pct"] / 100,
        "daily_loss_pct": (None if firm["daily_loss_pct"] is None
                            else -firm["daily_loss_pct"] / 100),
        "profit_target": B * (1 + firm["profit_target_pct"] / 100),
        "min_trading_days": firm["min_trading_days"],
        "inactivity_limit": inactivity if inactivity is not None
                            else firm["inactivity_max_idle_days"],
    }
    res = [run_seed(s, SIMS_PER_SEED, blocks, DD_TRIGGER, dd_scale,
                    strats=tuple(LEGS), firm_kwargs=firm_kwargs) for s in SEEDS]
    per = SIMS_PER_SEED
    keys = ("pass", "bust_daily", "bust_static", "bust_trailing",
            "bust_inactivity", "horizon_cap")
    rates = {k: float(np.mean([r["outcomes"][k] / per for r in res])) for k in keys}
    dds = [d for r in res for d in r["max_dds"]]
    days = [d for r in res for d in r["days_to_pass"]]
    # historical-path consistency: first day the 40% rule + $1K min + 10 tdays clear
    daily = panel.sum(axis=1)
    cum = daily.cumsum()
    best = daily.cummax()
    tdays = (daily != 0).cumsum()
    ok = (cum >= 1000) & (best <= 0.4 * cum) & (tdays >= 10)
    first_payout_day = int(np.argmax(ok.values) + 1) if ok.any() else -1
    # inactivity exposure: longest zero-P&L bday run in the historical panel
    z = (daily == 0.0).astype(int)
    runs = z.groupby((z != z.shift()).cumsum()).cumsum()
    return {
        "tier": tier, "B": B, **rates,
        "bust": rates["bust_daily"] + rates["bust_static"] + rates["bust_trailing"],
        "p99_dd": float(np.percentile(dds, 99)) if dds else float("nan"),
        "med_days": int(np.median(days)) if days else -1,
        "stats": stats, "first_payout_day": first_payout_day,
        "max_idle_run": int(runs.max()),
    }


def fmt(r):
    st = r["stats"]
    dj, nq = st["striker"], st["striker_nas100"]
    return (f"{r['tier']:13s} ${r['B']:>8,.0f} | pass {r['pass']:6.2%} bust {r['bust']:6.2%} "
            f"(t {r['bust_trailing']:.2%}) inact {r['bust_inactivity']:.2%} | "
            f"p99 {r['p99_dd']:5.2%} med {r['med_days']:>3}d | "
            f"DJ r {dj['mean_ratio_base']:.2f}/{dj['mean_ratio_add']:.2f} "
            f"skip {dj['skipped_base']}/{dj['skipped_add']} cap@{dj['base_cap']} "
            f"| NAS r {nq['mean_ratio_base']:.2f}/{nq['mean_ratio_add']:.2f} "
            f"skip {nq['skipped_base']}/{nq['skipped_add']} | payout d{r['first_payout_day']}")


print(f"C5 integer re-MC — RESERVE cap policy, 1R pinned "
      f"(striker ${PRE_SHOCK_1R['striker']:,.0f}/nas ${PRE_SHOCK_1R['striker_nas100']:,.0f}), "
      f"RT cost ${RT_COST}/contract, {len(SEEDS)}x{SIMS_PER_SEED:,} paths")
print("=" * 130)
print("--- GATE ARM: integer + costs, C2-off, inactivity mitigated (token trade) ---")
for tier in TIERS:
    print(fmt(run_tier(tier, with_costs=True)))
print("--- sensitivity: integer, NO costs (isolate cost drag) ---")
for tier in TIERS:
    print(fmt(run_tier(tier, with_costs=False)))
print("--- sensitivity: unmitigated Bulenox inactivity (5 idle bdays) @150K ---")
print(fmt(run_tier("Bulenox_150K", with_costs=True, inactivity=5)))
