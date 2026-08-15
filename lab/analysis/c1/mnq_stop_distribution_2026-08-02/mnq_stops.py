#!/usr/bin/env python3
"""Stop-distance distribution vs the integer-sizing floor — MNQ and MYM.

Operator questions (2026-08-02): item 5 needs a real TV strategy entry with
NON-ZERO sizing. Is Monday's MNQ window a real shot? And how robust is Tuesday's
MYM qty by the same measurement?

The two legs fail differently, which is the reason this is one harness:

  MNQ  reserve_cap = floor(11 / (1+1000%))  = 1  -> qty is BINARY, 1 or 0.
       Binding threshold = RISK/PT = 185/2   = 92.5 pts. Above it: qty 0.
  MYM  reserve_cap = floor(69 / (1+750%))   = 8  -> qty SATURATES at 8.
       The operative cliff is where floor(RISK/(PT*stop)) drops below 8,
       i.e. RISK/(PT*8) = 350/(0.5*8)        = 87.5 pts. Above it: 7, not 0.

So a wide stop COSTS MNQ the entire entry and costs MYM one contract. That
asymmetry is the whole reason MYM is the higher-probability item-5 path.

Read-only over gitignored TV exports in the PRIMARY tree. No K spend, nothing armed.

METHOD, and its one load-bearing subtlety. The exports do not carry stop_dist_pts
(that is a Pine alert-payload field). It is recovered from realized trades:
  * a passive "Exit Long" at a LOSS is a stop-out => stop = entry - exit, EXACT
    when the stop never trailed;
  * the trail biases this DOWNWARD, so it is a LOWER BOUND on the initial stop;
  * MAE is ~exact for stopped-out trades and is carried as a cross-check --
    and the check passes (median |MAE - (entry-exit)| / (entry-exit) ~ 0%).

THE PRICE-LEVEL POINT IS THE ANSWER. The thresholds are ABSOLUTE points; an
ATR-style stop is roughly PROPORTIONAL to price. Both instruments roughly tripled
over the panel, so historical point-distributions FLATTER the answer badly. The
decision statistic is stop-as-%-of-price projected to the CURRENT level.

Run:  python lab/analysis/c1/mnq_stop_distribution_2026-08-02/mnq_stops.py
"""
from __future__ import annotations

import csv
import json
import os
import statistics as st
from pathlib import Path

PRIMARY = Path("C:/Users/joshu/multi_firm_operations")
OUT = Path(__file__).resolve().parent / "out"
DD_SCALE = 0.40

LEGS = {
    "MNQ": dict(
        point_value=2.0, risk_usd=185.00, reserve_cap=1, cur_price=29600,
        obs=(28051.5, 126.75),          # the one real payload; floored to qty 0
        panels={
            "v1 on MNQ1! (2020-2026)":
                "core/data/tv_exports/cme/Striker_NAS100_v1_CME_MINI_MNQ1!_2026-07-11_beabf.csv",
            "MNQ edition (2025-09+)":
                "core/data/tv_exports/cme/Striker_NAS100_MNQ_CME_MINI_MNQ1!_2026-07-17_06861.csv",
        }),
    "MYM": dict(
        point_value=0.50, risk_usd=350.00, reserve_cap=8, cur_price=47000,
        obs=None,
        panels={
            "v4.5 on MYM1! (2020-2026)":
                "core/data/tv_exports/cme/Striker_DJ30_v4.5_CBOT_MINI_MYM1!_2026-07-08_7127d.csv",
            "MYM edition (2025-08+)":
                "core/data/tv_exports/cme/Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-21_73182.csv",
        }),
}


def qty_at(stop, cfg):
    if stop <= 0:
        return cfg["reserve_cap"]
    return min(int(cfg["risk_usd"] // (cfg["point_value"] * stop)), cfg["reserve_cap"])


def cliff_pts(cfg):
    """Stop at which qty first drops BELOW reserve_cap (the operative threshold)."""
    return cfg["risk_usd"] / (cfg["point_value"] * cfg["reserve_cap"])


def load_trades(path: Path, point_value: float):
    rows = list(csv.DictReader(open(path, encoding="utf-8-sig")))
    by_num: dict[str, dict] = {}
    for r in rows:
        by_num.setdefault(r["Trade number"], {})[
            "entry" if r["Type"].startswith("Entry") else "exit"] = r
    out = []
    for pair in by_num.values():
        e, x = pair.get("entry"), pair.get("exit")
        if not e or not x or e["Signal"] != "Long":
            continue
        try:
            ep, xp = float(e["Price USD"]), float(x["Price USD"])
            qty = float(e["Size (qty)"])
            mae = abs(float(e["Adverse excursion USD"]))
        except (ValueError, KeyError):
            continue
        if qty <= 0 or ep <= 0:
            continue
        out.append({"date": e["Date and time"], "entry": ep, "exit": xp,
                    "exit_signal": x["Signal"], "move_pts": ep - xp,
                    "mae_pts": mae / (qty * point_value)})
    return out


def pctl(xs, p):
    return st.quantiles(sorted(xs), n=100)[p - 1] if len(xs) > 2 else float("nan")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    S: dict[str, object] = {}

    for leg, cfg in LEGS.items():
        thr = cliff_pts(cfg)
        thr_dd = thr * DD_SCALE
        print("\n" + "#" * 78)
        print(f"# {leg}   reserve_cap={cfg['reserve_cap']}   "
              f"${cfg['point_value']}/pt   risk ${cfg['risk_usd']:.0f}")
        print("#" * 78)
        print(f"  qty = min(floor({cfg['risk_usd']:.0f} / ({cfg['point_value']} x stop)), "
              f"{cfg['reserve_cap']})")
        print(f"  qty stays at cap {cfg['reserve_cap']} while stop <= {thr:.1f} pts "
              f"({thr_dd:.1f} under DD {DD_SCALE})")
        print(f"  at threshold+  -> qty {qty_at(thr + 0.01, cfg)}   "
              f"(MNQ loses the ENTRY; MYM loses ONE CONTRACT)")
        if cfg["obs"]:
            c, sp_ = cfg["obs"]
            print(f"  ground truth 2026-07-28: stop {sp_} @ close {c} = "
                  f"{sp_/c*100:.4f}% -> qty {qty_at(sp_, cfg)}")

        pooled = []
        S[leg] = {"threshold_pts": thr, "threshold_pts_dd": thr_dd, "panels": {}}
        for label, rel in cfg["panels"].items():
            path = PRIMARY / rel
            if not path.exists():
                print(f"\n  !! MISSING (gitignored, primary tree): {rel}")
                continue
            tr = load_trades(path, cfg["point_value"])
            stops = [t for t in tr if t["exit_signal"] == "Exit Long" and t["move_pts"] > 0]
            spct = [t["move_pts"] / t["entry"] * 100 for t in stops]
            sp = [t["move_pts"] for t in stops]
            pooled += spct
            print(f"\n  PANEL {label}   ({os.path.basename(rel)[:44]})")
            print(f"    base entries {len(tr)}   stop-outs {len(stops)}   "
                  f"span {min(t['date'] for t in tr)[:10]}->{max(t['date'] for t in tr)[:10]}")
            if not spct:
                continue
            print(f"    stop (pts)  med {st.median(sp):.2f} | p90 {pctl(sp,90):.2f} | max {max(sp):.2f}")
            print(f"    stop (%)    med {st.median(spct):.4f}% | p90 {pctl(spct,90):.4f}% "
                  f"| max {max(spct):.4f}%")
            # consistency: for real stop-outs MAE should equal entry-exit
            rel_err = [abs(t["mae_pts"] - t["move_pts"]) / t["move_pts"]
                       for t in stops if t["move_pts"] > 1]
            if rel_err:
                print(f"    MAE-vs-(entry-exit) consistency: med {st.median(rel_err)*100:.1f}%")
            need = thr / cfg["cur_price"] * 100
            ok = sum(1 for x in spct if x <= need)
            print(f"    @ price {cfg['cur_price']}: need <= {need:.4f}% -> "
                  f"qty at cap for {ok}/{len(spct)} = {ok/len(spct)*100:.1f}%")
            S[leg]["panels"][label] = {
                "n_base": len(tr), "n_stopouts": len(stops),
                "stop_pct_med": st.median(spct), "stop_pct_max": max(spct),
                "at_cap_frac": ok / len(spct)}

        if pooled:
            need = thr / cfg["cur_price"] * 100
            ok = sum(1 for x in pooled if x <= need)
            print(f"\n  POOLED @ {cfg['cur_price']}: median stop {st.median(pooled):.4f}% "
                  f"vs threshold {need:.4f}%  ->  {ok}/{len(pooled)} = "
                  f"{ok/len(pooled)*100:.1f}% size at cap")
            # what a leg actually LOSES above the cliff
            worst = max(pooled)
            print(f"    worst measured stop {worst:.4f}% = {worst/100*cfg['cur_price']:.1f} pts "
                  f"-> qty {qty_at(worst/100*cfg['cur_price'], cfg)} "
                  f"(cap {cfg['reserve_cap']})")
            S[leg]["pooled"] = {"n": len(pooled), "median_pct": st.median(pooled),
                                "at_cap_frac": ok / len(pooled),
                                "worst_pct": worst,
                                "qty_at_worst": qty_at(worst / 100 * cfg["cur_price"], cfg)}

    print("\n" + "=" * 78)
    print("WHY MYM IS THE HIGHER-PROBABILITY ITEM-5 PATH")
    print("=" * 78)
    for leg, cfg in LEGS.items():
        p = S.get(leg, {}).get("pooled")
        if not p:
            continue
        print(f"  {leg}: {p['at_cap_frac']*100:.1f}% size at cap; at the WORST measured "
              f"stop qty = {p['qty_at_worst']} (cap {cfg['reserve_cap']})")
    print("  => MNQ's downside is qty 0 (no item-5 evidence at all).")
    print("     MYM's downside is qty 7 instead of 8 -- still NON-ZERO, still valid.")

    (OUT / "stops.json").write_text(json.dumps(S, indent=2) + "\n", encoding="utf-8")
    print(f"\nstats -> {OUT / 'stops.json'}")


if __name__ == "__main__":
    main()
