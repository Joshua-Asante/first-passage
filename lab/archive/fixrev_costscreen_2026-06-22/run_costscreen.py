"""Fixing-reversal cost pre-screen — driver (2026-06-22).

Thin orchestration over the tested ``fixrev_costscreen`` library: locate the
canonical Pepperstone EURUSD BAR_EXPORT pages (skip-if-missing), decode, run the
(hold × stop) screen, derive the verdict, write RESULTS.md.

Vendor CSVs are read in place from ~/Downloads and NEVER copied into the repo;
only the aggregate RESULTS.md is committed.

    python run_costscreen.py            # default grid + FXIFY all-in cost 0.8 pip
    python run_costscreen.py --fxify-cost 0.6
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")  # Windows console is cp1252 by default
except Exception:
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fixrev_costscreen as F  # noqa: E402

# Representative, NON-optimized grid (reported in full — not cherry-picked):
HOLD_GRID_BARS = [3, 6, 12]          # 15 / 30 / 60-minute holds
STOP_GRID_PIPS = [5.0, 10.0, 20.0]   # maps the cost-law geometry (wider stop → lower cost/R)
# "spread" here = ALL-IN round-trip cost in pips (spread + commission folded in):
COST_GRID_PIPS = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
N_FLOOR = 100
DEFAULT_DOWNLOADS = Path.home() / "Downloads"


def render_results(summary: dict, *, fxify_cost_pips: float) -> str:
    cells = summary["cells"]
    best_be = max((c["breakeven_spread_pips"] for c in cells if c["n_trades"] >= N_FLOOR),
                  default=float("nan"))
    n_max = max((c["n_trades"] for c in cells), default=0)
    verdict = F.classify_verdict(best_breakeven_pips=best_be, fxify_spread_pips=fxify_cost_pips,
                                 n_trades=n_max, n_floor=N_FLOOR)

    L = []
    L.append("# Fixing-reversal cost pre-screen — RESULTS (2026-06-22)\n")
    L.append(f"**Verdict: {verdict}** "
             f"(best-of-grid break-even {best_be:.3f} pip vs FXIFY all-in {fxify_cost_pips:.2f} pip).\n")
    L.append("**Scope:** scouting cost pre-screen on the canonical Pepperstone 5m EURUSD feed. "
             "Claims NO edge — measures whether the London-fix fade can clear FXIFY cost. "
             "Long EURUSD entered at the fix bar's close (fade the pre-fix USD strength), "
             "protective stop, time-exit. Rule is fixed/representative, NOT optimized.\n")
    L.append(f"**Coverage:** {summary['date_min']} → {summary['date_max']}, "
             f"{summary['n_fix_days']} fix-days used, {summary['n_skipped_days']} skipped (no fix bar).\n")
    L.append("\n## Per-cell (hold × stop) — gross, no cost\n")
    L.append("`breakeven_spread_pips` = the gross post-fix edge expressed as the all-in cost (pips) "
             "it can absorb before mean net R goes ≤ 0. Above FXIFY's all-in cost ⇒ survives.\n")
    L.append("\n| hold (min) | stop (pip) | n | mean gross R | win% | stop-out% | break-even cost (pip) |")
    L.append("|---:|---:|---:|---:|---:|---:|---:|")
    for c in cells:
        L.append(f"| {c['hold_min']} | {c['stop_pips']:.0f} | {c['n_trades']} | "
                 f"{c['mean_gross_R']:+.4f} | {100*c['win_rate']:.1f} | "
                 f"{100*c['stop_out_share']:.1f} | {c['breakeven_spread_pips']:.3f} |")

    L.append("\n## Net mean R by all-in cost (the paper's cost-geometry wall)\n")
    L.append("Each entry = mean net R at that all-in round-trip cost (spread + commission, pips).\n")
    header = "| hold/stop | " + " | ".join(f"{s:.1f}p" for s in COST_GRID_PIPS) + " |"
    L.append(header)
    L.append("|" + "---|" * (len(COST_GRID_PIPS) + 1))
    for c in cells:
        cellvals = " | ".join(f"{ps['mean_net_R']:+.3f}" for ps in c["per_spread"])
        L.append(f"| {c['hold_min']}m/{c['stop_pips']:.0f}p | {cellvals} |")

    L.append("\n## Read\n")
    if verdict == "FAIL-COST":
        L.append(f"- Even the most favorable grid cell breaks even only at {best_be:.3f} pip all-in, "
                 f"**below** FXIFY's ~{fxify_cost_pips:.2f} pip → the London-fix fade does **not** clear "
                 "retail cost on EURUSD. This **confirms the paper** (edge negative at full retail spread). "
                 "5th-leg slot stays empty on this mechanism; pivot effort to T2 (regime-adaptive sizing).")
    elif verdict == "PASS-PROVISIONAL":
        L.append(f"- Best-of-grid break-even {best_be:.3f} pip **exceeds** FXIFY's ~{fxify_cost_pips:.2f} pip → "
                 "the fade may clear retail cost. This is best-of-grid (multiplicity); it does NOT establish "
                 "an edge. Next: a **separate, pre-registered** edge validation + `ops/instruments/EURUSD.md` "
                 "ledger + feed-equivalence — NOT a deploy decision.")
    else:
        L.append(f"- n={n_max} < floor {N_FLOOR}: insufficient fix-days to conclude.")
    L.append("\n**Caveats:** scouting-only until re-confirmed under a feed-equivalence pre-flight "
             "(a fix-timestamp signal is acutely feed-sensitive). `--fxify-cost` is a parameter — "
             "set it from the real FXIFY/DXTrade EURUSD round-trip cost; the break-even column is "
             "robust to that choice. The (hold × stop) grid is reported in full to avoid best-cell selection.\n")
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--downloads", default=str(DEFAULT_DOWNLOADS))
    ap.add_argument("--fxify-cost", type=float, default=0.8,
                    help="FXIFY-realistic EURUSD all-in round-trip cost, pips (set from live)")
    args = ap.parse_args()

    paths = F.find_input_csvs(args.downloads, pattern="BAR_EXPORT_*_EURUSD_*.csv")
    if not paths:
        print(f"=== SKIP: no EURUSD BAR_EXPORT pages in {args.downloads} "
              f"(vendor-licensed, not committed). Drop them in and re-run. ===")
        return 0

    print(f"Decoding {len(paths)} page(s):")
    for p in paths:
        print(f"  {Path(p).name}")
    bars = F.decode_bars(paths)
    print(f"Decoded {len(bars):,} unique 5m bars: {bars['time'].min()} → {bars['time'].max()}")

    summary = F.run_screen(
        bars, hold_grid_bars=HOLD_GRID_BARS, stop_grid_pips=STOP_GRID_PIPS,
        spread_grid_pips=COST_GRID_PIPS, commission_pips=0.0, side=+1,
    )
    md = render_results(summary, fxify_cost_pips=args.fxify_cost)
    out = Path(__file__).resolve().parent / "RESULTS.md"
    out.write_text(md, encoding="utf-8")
    print("\n" + md)
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
