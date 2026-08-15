"""Tradeify Select Flex INTEGER-micro-contract re-MC (2026-07-10) — pessimistic-bound arm.

Layers the C5 integer-contract sizing model (lab/analysis/bulenox_futures_remc_2026-07-01/
c5_integer_remc.py) onto the Tradeify trailing_locking barrier. Answers the parent
follow-up to the §4-FALSIFIED verdict: the %-equity arm (run_tradeify_remc.py) is the
OPTIMISTIC fidelity; integer sizing adds contract caps, granularity floors, and
commission drag — all STRICTER — so this bounds the pessimistic side.

Sizing (faithful to C5, RESERVE cap policy):
  ideal_qty_i = B*risk% / (1.2 * ATR_fut(entry_i) * $/pt)   [futures ATR(11), roll-masked,
                                                              time-matched at each entry]
  base_int = min(floor(ideal), floor(cap/(1+pyr)))          [RESERVE: pyramid add always fits]
  add_int  = min(floor(base_int*pyr), cap-base_int)         [0 if base rounds to 0 -> design-void]
  ratio    = int_qty / ideal_qty ;  pnl_adj = pnl*scale*ratio - qty*RT_COST

Tradeify Select micro caps (§1 ADDENDUM eval-full): 25K:20 / 50K:40 / 100K:80 / 150K:120.
Barrier: dd_type="trailing_locking" (offset $100) vs matched-Bulenox fixed-$ (no lock,
isolates the lock) and shipped %-of-peak (Bulenox C5 cross-ref).

COMMISSION IS A PROXY (NEEDS_CONTEXT). Tradeify's exact per-side commission was NOT in
the §1 ADDENDUM. This reuses the Bulenox CME-micro all-in round-turn $2.22/contract
($0.61/side x2 + 1 tick x2 slip) as a conservative proxy, and reports a no-cost
sensitivity to isolate the cost contribution. Re-verify before any lock-grade read.

1R pinned PRE_SHOCK_1R (striker $4,229 / nas100 $3,940). Panel = canonical 567e1 DJ30
(force-flat 17:00 ET) + 11605 NAS100 (clean) — the SAME panel as the %-equity Tradeify
run, so integer-vs-%equity is apples-to-apples. (Recorded Bulenox C5 used the 2026-07-03
full-history DJ30 export, so the C5 cross-ref is DIRECTIONAL, not an exact reproduction.)

2-strat book only: the C5 integer model is the DJ30-MYM + NAS100-MNQ index book. The
Aegis/6J leg has no integer contract-spec model here (needs 6J-micro tick/$pt/cap) ->
3-strat integer is NEEDS_CONTEXT.

Needs (gitignored, dropped into the worktree): the two Striker panels + US30_M15.csv
(force-flat) + YM_M15.csv + NQ_M15.csv (futures ATR; produced by
`scripts/parse_bar_export.py --symbol YM/NQ` from the Downloads BAR_EXPORT v0.2 files).
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[2]
_CORE = _ROOT / "core"
_BULENOX = _ROOT / "lab" / "analysis" / "bulenox_futures_remc_2026-07-01"
_FUTCONV = _ROOT / "lab" / "analysis" / "futures_conversion_2026-07-01"
for _p in (_CORE, _BULENOX, _FUTCONV):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from portfolio_mc import (  # noqa: E402
    ALLOCATIONS, BASELINE_BALANCE, HORIZON_CAP, PEPPERSTONE_PANELS, PRE_SHOCK_1R,
    SEEDS, SIMS_PER_SEED, _normalize_tv_columns, build_week_blocks, run_seed,
)
from firm_rules import FIRM_RULES  # noqa: E402
from force_flat_transform import bars_utc_to_et, force_flat_csv  # noqa: E402
import roll_mask as rm  # noqa: E402

BAR_DIR = _CORE / "data" / "bar_data"
ATR_LEN = 11
# VERIFIED 2026-07-10 — Tradeify Help Center "Trading Commission Fees" (last updated
# 2026-04-28): Micro E-Mini Dow (MYM) and Micro E-Mini NASDAQ (MNQ) = $1.82 per contract
# ROUND-TURN. Page states "Total Round Trip Cost includes Exchange fees, NFA fees,
# Clearing fees, and Commissions" -> ALL-IN (no execution slippage), free-membership tier.
# (Supersedes the earlier $2.22 Bulenox proxy in RESULTS_tradeify_integer_2026-07-10.md.)
RT_COST_FEES = 1.82   # verified all-in fees, no slippage (PRIMARY)
RT_COST_SLIP = 2.82   # 1.82 + 2-tick ($1.00) round-turn slippage (conservative live-exec sensitivity)

LEGS = {
    "striker":        dict(csv=PEPPERSTONE_PANELS["striker"], fut="YM", dpp=0.50,
                           risk=0.0070, pyr=7.5, sl_mult=1.20, forceflat=True),
    "striker_nas100": dict(csv=PEPPERSTONE_PANELS["striker_nas100"], fut="NQ", dpp=2.00,
                           risk=0.0037, pyr=10.0, sl_mult=1.20, forceflat=False),
}
STRATS = tuple(LEGS)

# Micro-contract caps per firm/tier.
TRADEIFY_CAPS = {"25K": 20, "50K": 40, "100K": 80, "150K": 120}   # §1 ADDENDUM eval-full
BULENOX_CAPS = {"25K": 30, "50K": 70, "100K": 120, "150K": 150}   # firm_rules micro_contract_cap
SIZES = ("25K", "50K", "100K", "150K")

GATE_BUST, GATE_P99 = 0.01, 0.05
NO_PROTECTION_TRIGGER, DD_SCALE = 10.0, 0.40
INACT_OFF = HORIZON_CAP + 1
_OUTCOME_KEYS = ("pass", "bust_daily", "bust_static", "bust_trailing",
                 "bust_inactivity", "horizon_cap")


# ── C5 sizing (faithful replica) ────────────────────────────────────────────

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


def integer_panel(size: str, caps: dict, *, rt_cost: float):
    """(panel_at_tier_B, stats) — 1R-pinned ideal panel x per-trade integer ratio, minus
    rt_cost*qty per trade (rt_cost=0.0 -> no-cost sensitivity).

    NOTE the returned panel is ALREADY denominated at the tier balance B (the scale
    folds in B/BASELINE), so run_config must NOT rescale it again.
    """
    B = float(FIRM_RULES[f"Tradeify_Select_{size}"]["starting_balance"])
    cap = caps[size]
    rows, stats = [], {}
    for leg, cfg in LEGS.items():
        atr = atr_series_et(cfg["fut"])
        tr = load_leg_trades(leg)
        idx = atr.index.searchsorted(tr["entry_dt"].values, side="right") - 1
        if (idx < 0).any():
            raise ValueError(f"{leg}: entry before first ATR bar")
        tr["atr"] = atr.values[idx]
        tr["ideal"] = (B * cfg["risk"]) / (cfg["sl_mult"] * tr["atr"] * cfg["dpp"])
        base_cap = math.floor(cap / (1.0 + cfg["pyr"]))          # RESERVE policy
        tr["base_int"] = np.minimum(np.floor(tr["ideal"]), base_cap).astype(int)
        qty, ratio = {}, {}
        for tnum, r in tr.iterrows():
            if not r["is_add"]:
                qty[tnum] = int(r["base_int"])
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
        if rt_cost > 0:
            tr["pnl_adj"] -= tr["qty"] * rt_cost
        s = tr.groupby("exit_date")["pnl_adj"].sum()
        s.name = leg
        rows.append(s)
        b_mask, a_mask = ~tr["is_add"], tr["is_add"]
        stats[leg] = {
            "n_base": int(b_mask.sum()), "n_add": int(a_mask.sum()),
            "skipped_base": int((tr.loc[b_mask, "qty"] == 0).sum()),
            "mean_ratio_base": float(tr.loc[b_mask & (tr["ideal"] > 0), "ratio"].mean()),
            "base_cap": base_cap,
        }
    panel = pd.concat(rows, axis=1)
    bdays = pd.bdate_range(panel.index.min(), panel.index.max())
    return panel.reindex(bdays).fillna(0.0), stats


# ── barrier kwargs ──────────────────────────────────────────────────────────

def _base_kwargs(B: float, target_pct: float, min_days: int) -> dict:
    return dict(starting_equity=B, daily_loss_pct=None,
               profit_target=B * (1 + target_pct / 100), min_trading_days=min_days,
               inactivity_limit=INACT_OFF)


def barrier_kwargs(kind: str, size: str) -> dict:
    """kind in {tradeify, tradeify_consist, matched, pctpeak}."""
    tf = FIRM_RULES[f"Tradeify_Select_{size}"]
    bx = FIRM_RULES[f"Bulenox_{size}"]
    if kind in ("tradeify", "tradeify_consist"):
        B = float(tf["starting_balance"])
        kw = _base_kwargs(B, tf["profit_target_pct"], tf["min_trading_days"])
        kw.update(dd_type="trailing_locking", trailing_dd_pct=-tf["max_dd_pct"] / 100,
                  dd_lock_offset_usd=float(tf["dd_lock_offset_usd"]),
                  consistency_frac=(0.40 if kind == "tradeify_consist" else None))
        return kw
    # Bulenox comparison arms run on the Tradeify tier balance/target/min_days so the
    # ONLY difference vs Tradeify is the barrier (matched = fixed-$ no-lock; pctpeak =
    # shipped %-of-peak). Bulenox's own max_dd_pct is used for the trailing cushion.
    B = float(tf["starting_balance"])
    kw = _base_kwargs(B, tf["profit_target_pct"], tf["min_trading_days"])
    if kind == "matched":
        kw.update(dd_type="trailing_locking", trailing_dd_pct=-bx["max_dd_pct"] / 100,
                  dd_lock_offset_usd=1e12)   # unreachable -> pure fixed-$ trailing
    elif kind == "pctpeak":
        kw.update(dd_type="trailing", trailing_dd_pct=-bx["max_dd_pct"] / 100)
    else:
        raise ValueError(kind)
    return kw


def run_config(panel_tierB: pd.DataFrame, firm_kwargs: dict) -> dict:
    blocks = build_week_blocks(panel_tierB)
    res = [run_seed(s, SIMS_PER_SEED, blocks, NO_PROTECTION_TRIGGER, DD_SCALE,
                    strats=STRATS, firm_kwargs=firm_kwargs) for s in SEEDS]
    per = SIMS_PER_SEED
    rates = {k: float(np.mean([r["outcomes"][k] / per for r in res])) for k in _OUTCOME_KEYS}
    dds = [d for r in res for d in r["max_dds"]]
    days = [d for r in res for d in r["days_to_pass"]]
    return {
        "pass": rates["pass"],
        "bust": rates["bust_daily"] + rates["bust_static"] + rates["bust_trailing"],
        "p99_dd": float(np.percentile(dds, 99)) if dds else float("nan"),
        "median": int(np.median(days)) if days else -1,
    }


def _gate(r: dict) -> str:
    ok_b, ok_p = r["bust"] < GATE_BUST, r["p99_dd"] < GATE_P99
    return ("PASS" if (ok_b and ok_p) else "FAIL") + f" (bust{'<' if ok_b else '>='}1% p99{'<' if ok_p else '>='}5%)"


def main() -> None:
    lines: list[str] = []

    def emit(s: str = "") -> None:
        print(s)
        lines.append(s)

    emit("=" * 116)
    emit("TRADEIFY SELECT FLEX — INTEGER-MICRO re-MC (2026-07-10)  [VERIFIED-COST RESOLVED; C5 sizing model]")
    emit(f"Sims: {SIMS_PER_SEED:,} x {len(SEEDS)} seeds | dd-protection OFF | inactivity DISABLED | RESERVE cap policy")
    emit(f"Commission VERIFIED (Tradeify Help Center, updated 2026-04-28): MYM=MNQ ${RT_COST_FEES}/ctr ROUND-TURN, "
         f"ALL-IN (exchange+NFA+clearing+commission), free tier")
    emit(f"1R pinned striker=${PRE_SHOCK_1R['striker']:,.0f} nas=${PRE_SHOCK_1R['striker_nas100']:,.0f} | "
         f"Gates bust<{GATE_BUST:.0%} AND p99 DD<{GATE_P99:.0%} | book: DJ30-MYM + NAS100-MNQ (2-strat)")
    emit("=" * 116)
    emit()
    emit(f"    {'Size':<6} {'Config':<42} {'Pass':>8} {'Bust':>8} {'p99 DD':>8} {'Median':>7}  Gate")
    emit("    " + "-" * 106)

    verdict = {}
    for size in SIZES:
        tf_nocost, tf_stats = integer_panel(size, TRADEIFY_CAPS, rt_cost=0.0)
        tf_fees, _ = integer_panel(size, TRADEIFY_CAPS, rt_cost=RT_COST_FEES)
        tf_slip, _ = integer_panel(size, TRADEIFY_CAPS, rt_cost=RT_COST_SLIP)

        configs = [
            ("Tradeify int (lock) NO cost [bound]",       tf_nocost, barrier_kwargs("tradeify", size)),
            ("Tradeify int (lock) @ $1.82 [VERIFIED]",    tf_fees,   barrier_kwargs("tradeify", size)),
            ("Tradeify int (lock) @ $2.82 [+2t slip]",    tf_slip,   barrier_kwargs("tradeify", size)),
            ("Tradeify int (lock,+40%consist) @ $1.82",   tf_fees,   barrier_kwargs("tradeify_consist", size)),
            ("Tradeify int matched no-lock @ $1.82",      tf_fees,   barrier_kwargs("matched", size)),
        ]
        dj = tf_stats["striker"]; nq = tf_stats["striker_nas100"]
        for label, panel, kw in configs:
            r = run_config(panel, kw)
            emit(f"    {size:<6} {label:<42} {r['pass']:>8.2%} {r['bust']:>8.2%} "
                 f"{r['p99_dd']:>8.2%} {r['median']:>7}  {_gate(r)}")
            if "VERIFIED" in label:
                verdict[size] = r
        emit(f"           caps micro={TRADEIFY_CAPS[size]} | DJ base_int_cap={dj['base_cap']} "
             f"r_base={dj['mean_ratio_base']:.2f} skip={dj['skipped_base']}/{dj['n_base']} | "
             f"NAS base_int_cap={nq['base_cap']} r_base={nq['mean_ratio_base']:.2f} "
             f"skip={nq['skipped_base']}/{nq['n_base']}")
        emit()

    emit("=" * 116)
    emit("§4 (integer arm, VERIFIED $1.82 all-in) — does any Tradeify tier fall within the gates?")
    emit("=" * 116)
    any_pass = False
    for size in SIZES:
        r = verdict[size]
        ok = r["bust"] < GATE_BUST and r["p99_dd"] < GATE_P99
        any_pass = any_pass or ok
        emit(f"  {size:<5} Tradeify integer @ $1.82 verified: bust {r['bust']:.2%} / p99 {r['p99_dd']:.2%} "
             f"/ median {r['median']}d -> {'PASS' if ok else 'FAIL'}")
    emit()
    emit(f"VERDICT (verified $1.82 all-in cost): "
         f"{'>=1 TIER PASSES both gates' if any_pass else 'NO tier passes both gates'}")

    out = _HERE / "RESULTS_tradeify_integer_RESOLVED_2026-07-10.md"
    out.write_text("```\n" + "\n".join(lines) + "\n```\n", encoding="utf-8")
    print(f"\n[written] {out}")


if __name__ == "__main__":
    main()
