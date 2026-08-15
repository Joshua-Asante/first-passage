"""Task 12 executor — 15m-vs-5m matched-window comparison + descriptive re-MC.

Adapts the plan's compare.main() to the real data: the 5m protos run from 2020
while the 15m baselines start 2022, so the matched window is the INTERSECTION
of each pair (not baseline-clipped-to-proto, which the plan assumed). All dollar
metrics are static-$200K (net_pnl_pct/100 * 200_000) per the reconcile skill.

Run: python lab/analysis/timeframe_5m_2026-06-25/run_task12.py
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd

_H = Path(__file__).resolve().parent
_CORE = _H.parents[2] / "core"
for _p in (_H, _CORE):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import metrics        # noqa: E402
import remc           # noqa: E402
import portfolio_mc as pmc  # noqa: E402

# Baselines are gitignored vendor CSVs — present only in the MAIN checkout, not the worktree.
BASE = Path(r"C:/Users/joshu/multi_firm_operations/core/data/tv_exports/pepperstone")
DATA = _H / "data"

PANELS = {
    "guardian":       (BASE / "Guardian_Gold_v5.5_PEPPERSTONE_XAUUSD_2026-05-24_1bb97.csv", DATA / "guardian_5m.csv"),
    "striker":        (BASE / "Striker_DJ30_v4.5_PEPPERSTONE_US30_2026-05-24_567e1.csv",     DATA / "striker_dj30_5m.csv"),
    "striker_nas100": (BASE / "Striker_NAS100_v1_PEPPERSTONE_NAS100_2026-05-24_11605.csv",   DATA / "striker_nas100_5m.csv"),
    "aegis":          (BASE / "Aegis_USDJPY_v4.3_PEPPERSTONE_USDJPY_2026-05-24_e8e1c.csv",   DATA / "aegis_5m.csv"),
}
LABEL = {"guardian": "Guardian XAUUSD", "striker": "Striker DJ30",
         "striker_nas100": "Striker NAS100", "aegis": "Aegis USDJPY"}
ANCHOR_WINDOW_START = pd.Timestamp("2022-01-01")


def load(path: Path) -> pd.DataFrame:
    """Exit-row loader WITHOUT io_tv's 100-row floor. The floor guards against
    truncated exports; here the inventory step has confirmed every file is
    complete (full 2020-2026 span). NAS100 5m legitimately has only 39 trades
    (78 rows) — the signal-frequency collapse IS the finding, not a short fetch."""
    df = pd.read_csv(path, encoding="utf-8-sig")
    df = pmc._normalize_tv_columns(df)  # pylint: disable=protected-access
    ex = df[df["Type"].astype(str).str.startswith("Exit")].copy()
    ts = pd.to_datetime(ex["Date and time"])
    out = pd.DataFrame({
        "exit_ts": ts.values, "exit_date": ts.dt.normalize().values,
        "net_pnl_usd": ex["Net P&L USD"].astype(float).values,
        "net_pnl_pct": ex["Net P&L %"].astype(float).values,
    })
    return out.sort_values("exit_ts").reset_index(drop=True)


def pyramid_adds(path: Path) -> int:
    """Count entry legs whose Signal marks a pyramid add."""
    df = pd.read_csv(path, encoding="utf-8-sig")
    df = pmc._normalize_tv_columns(df)  # pylint: disable=protected-access
    typ = df["Type"].astype(str)
    sig = df["Signal"].astype(str) if "Signal" in df.columns else pd.Series([""] * len(df))
    return int((typ.str.startswith("Entry") & sig.str.contains("Add", case=False)).sum())


def clip(exits: pd.DataFrame, start, end) -> pd.DataFrame:
    """Restrict exit rows to [start, end] (inclusive) on exit_ts."""
    t = pd.to_datetime(exits["exit_ts"])
    return exits[(t >= start) & (t <= end)].reset_index(drop=True)


def fmt(m: dict) -> str:
    """One-line metric row for console output."""
    pf = "inf" if m["pf"] == float("inf") else f"{m['pf']:.3f}"
    rf = "inf" if m["rf"] == float("inf") else f"{m['rf']:.2f}"
    fb = "  [1R-fellback]" if m["r1_fell_back"] else ""
    return (f"N={m['trades']:>4}  PF={pf:>6}  WR={m['win_rate']*100:>5.1f}%  "
            f"Net=${m['net_usd']:>11,.0f}  MaxDD=${m['max_dd_usd']:>10,.0f}  RF={rf:>6}  "
            f"1R=${m['r1_usd']:>7,.0f}{fb}")


def compare_one(strategy: str, bpath: Path, ppath: Path) -> dict:
    """15m-vs-5m metrics for one strategy on the intersection window + full 5m span."""
    b, p = load(bpath), load(ppath)
    bt, pt = pd.to_datetime(b["exit_ts"]), pd.to_datetime(p["exit_ts"])
    start, end = max(bt.min(), pt.min()), min(bt.max(), pt.max())
    return {
        "s": strategy, "start": start, "end": end,
        "mb": metrics.compute_metrics(clip(b, start, end), strategy),
        "mp": metrics.compute_metrics(clip(p, start, end), strategy),
        "mp_full": metrics.compute_metrics(p, strategy),
        "p_full_n": len(p),
        "b_adds": pyramid_adds(bpath), "p_adds": pyramid_adds(ppath),
    }


def run_remc(trades_by_strat: dict) -> dict:
    """Run the core MC kernel on a {strategy: [exit_date, pnl]} panel; return the
    aggregate verdict plus disclosure (window, blocks, 1R fell-back flags)."""
    panel, scale_info = pmc.build_daily_panel(trades_by_strat, pmc.ALLOCATIONS)
    blocks = pmc.build_week_blocks(panel)
    seeds = pmc._run_seeds(  # pylint: disable=protected-access
        blocks, pmc.DD_TRIGGER, pmc.DD_SCALE, strats=tuple(trades_by_strat.keys()))
    agg = remc.aggregate(seeds)
    agg.update({
        "start": panel.index.min().date(), "end": panel.index.max().date(),
        "n_bdays": len(panel), "n_blocks": len(blocks),
        "fell_back": {s: bool(i["fell_back"]) for s, i in scale_info.items()},
    })
    return agg


def main() -> None:
    """Print the per-strategy comparison + anchor cross-check + descriptive re-MC."""
    print("=" * 100)
    print("TASK 12 — 15m baseline vs 5m prototype (matched intersection window, static-$200K basis)")
    print("=" * 100)

    rows = [compare_one(s, b, p) for s, (b, p) in PANELS.items()]
    for r in rows:
        print(f"\n### {LABEL[r['s']]}   matched window {r['start'].date()} -> {r['end'].date()}")
        print(f"  15m baseline : {fmt(r['mb'])}")
        print(f"  5m proto     : {fmt(r['mp'])}")
        print(f"  5m FULL span : {fmt(r['mp_full'])}   (2020->2026, full proto {r['p_full_n']} trades)")
        if r["s"] in ("striker", "striker_nas100"):
            print(f"  pyramid adds : 15m={r['b_adds']}   5m={r['p_adds']}   "
                  "(Striker edge IS the pyramid; 88-94% of P&L on 15m)")

    gm = metrics.compute_metrics(load(PANELS["guardian"][0]), "guardian")
    print("\n" + "-" * 100)
    print("ANCHOR CROSS-CHECK (Guardian 15m FULL window vs CLAUDE.md anchor N=203 / PF 3.750 / WR 22.17%):")
    nflag = "OK" if gm["trades"] == 203 else "DRIFT"
    print(f"  harness: N={gm['trades']}  PF={gm['pf']:.3f}  WR={gm['win_rate']*100:.2f}%  "
          f"[N {nflag}; PF/WR basis-independent should match]")

    print("\n" + "-" * 100)
    print("DESCRIPTIVE RE-MC — 5m portfolio, FXIFY gates, vs locked anchor 99.83% / 0.17% / 4.37%")
    matched = {s: remc.to_mc_trades(load(p)) for s, (_, p) in PANELS.items()}
    matched = {s: t[pd.to_datetime(t["exit_date"]) >= ANCHOR_WINDOW_START].reset_index(drop=True)
               for s, t in matched.items()}
    a = run_remc(matched)
    print(f"  matched 2022-26: window {a['start']} -> {a['end']} ({a['n_bdays']} bdays, {a['n_blocks']} blocks)")
    print(f"  trades: " + " | ".join(f"{s}:{len(t)}" for s, t in matched.items()))
    print(f"  1R fell-back: {a['fell_back']}")
    print(f"  PASS {a['pass_rate']:.2%}   BUST {a['bust_rate']:.2%}   p99 DD {a['p99_dd']:.2%}   "
          "(anchor: PASS 99.83%  BUST 0.17%  p99 DD 4.37%)")

    full = {s: remc.to_mc_trades(load(p)) for s, (_, p) in PANELS.items()}
    f = run_remc(full)
    print(f"\n  FULL-span 2020-26 (incl. chop): window {f['start']} -> {f['end']} ({f['n_blocks']} blocks)")
    print(f"  PASS {f['pass_rate']:.2%}   BUST {f['bust_rate']:.2%}   p99 DD {f['p99_dd']:.2%}")


if __name__ == "__main__":
    main()
