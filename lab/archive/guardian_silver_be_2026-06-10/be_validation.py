#!/usr/bin/env python3
"""Guardian Silver v1.0 beTriggerAtr=4.8 vs no-BE baseline — TV/Pepperstone validation.

Executes the metric/split/critical-trade steps of the 2026-06-10 CC handoff
(docs/briefs/2026-06-10-cc-handoff-guardian-silver-be-validation.md), as
re-scoped by Joshua: the Dukascopy leg is dropped (all runs TradingView-side);
the rejected-candidates collision is overridden by explicit operator decision —
see the brief's amendment block.

Inputs (gitignored vendor CSVs, manifest-pinned in
core/data/tv_exports/pepperstone/SHA256SUMS):
  Guardian_Silver_v1.0_PEPPERSTONE_XAGUSD_2026-06-10_d87c2.csv        (baseline, BE off)
  Guardian_Silver_v1.0_PEPPERSTONE_XAGUSD_2026-06-10_7c8c2_be4.8.csv  (beTriggerAtr=4.8)

Computes per config, on two bases:
  raw     — TV compounded dollars as exported (matches the parent-session table)
  static  — decompounded to a static $200K base: pnl_i * 200_000 / equity_before_i
            (TV sizes percent-of-equity; trades are sequential, so equity_before
            is exact, not approximate — the script verifies non-overlap)
  N / WR / PF / Net / maxDD$ / maxDD% / RF / median-loss 1R / max consecutive losses,
  the 2024-01-01 half-panel split (fresh $200K per half), RF(4.8)/RF(baseline)
  ratios, and the Aug-2023 critical-trade rows.

Headline raw metrics are cross-checked against the canonical skill pipeline
(.claude/skills/trade-csv-reconcile/scripts/reconcile.py --strategy guardian) on a
column-normalized copy — the 2026-06 TV export renamed "Trade #" -> "Trade number"
and "Net P&L USD" -> "Net PnL USD"; reconcile.py expects the older names.

Run: python lab/analysis/guardian_silver_be_2026-06-10/be_validation.py
Skips with a message if the gitignored CSVs are absent (public clone).
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
PEP_DIR = REPO_ROOT / "core/data/tv_exports/pepperstone"
RECONCILE = REPO_ROOT / ".claude/skills/trade-csv-reconcile/scripts/reconcile.py"

CONFIGS = {
    "baseline": PEP_DIR / "Guardian_Silver_v1.0_PEPPERSTONE_XAGUSD_2026-06-10_d87c2.csv",
    "be4.8": PEP_DIR / "Guardian_Silver_v1.0_PEPPERSTONE_XAGUSD_2026-06-10_7c8c2_be4.8.csv",
}

SPLIT_DATE = pd.Timestamp("2024-01-01")
ACCOUNT = 200_000.0

# 2026-06 TV export column names -> the names reconcile.py / the skill expect.
RENAME = {
    "Trade number": "Trade #",
    "Net PnL USD": "Net P&L USD",
    "Net PnL %": "Net P&L %",
    "Cumulative PnL USD": "Cumulative P&L USD",
    "Cumulative PnL %": "Cumulative P&L %",
}

# Parent-session (claude.ai TV sweep) claimed values, for drift reporting.
BRIEF_CLAIMS = {
    "baseline": {"n": 271, "rf": 13.30, "h1_rf": 0.69, "h2_rf": 17.20},
    "be4.8": {"n": 239, "rf": 20.04, "h1_rf": 2.59, "h2_rf": 23.25},
}


def load_trades(path: Path) -> pd.DataFrame:
    """One row per closed trade: entry/exit dt + price, raw pnl, static pnl."""
    df = pd.read_csv(path, encoding="utf-8-sig").rename(columns=RENAME)
    df["dt"] = pd.to_datetime(df["Date and time"])
    entries = df[df["Type"].str.startswith("Entry")].set_index("Trade #")
    exits = df[df["Type"].str.startswith("Exit")].set_index("Trade #")
    if not entries.index.sort_values().equals(exits.index.sort_values()):
        raise ValueError(f"{path.name}: entry/exit Trade # mismatch")
    t = pd.DataFrame({
        "entry_dt": entries["dt"], "entry_px": entries["Price USD"],
        "exit_dt": exits["dt"], "exit_px": exits["Price USD"],
        "pnl": exits["Net P&L USD"].astype(float),
    }).sort_values("exit_dt")

    overlaps = int((t["entry_dt"].iloc[1:].values < t["exit_dt"].iloc[:-1].values).sum())
    if overlaps:
        print(f"  WARNING {path.name}: {overlaps} overlapping trades — "
              f"static decompounding is approximate for those")

    equity_before = ACCOUNT + t["pnl"].cumsum().shift(fill_value=0.0)
    t["pnl_static"] = t["pnl"] * ACCOUNT / equity_before
    return t


def metrics(pnl: pd.Series) -> dict:
    eq, peak = ACCOUNT, ACCOUNT
    max_dd, dd_pct_at_trough = 0.0, 0.0
    for p in pnl:
        eq += p
        peak = max(peak, eq)
        if peak - eq > max_dd:
            max_dd = peak - eq
            dd_pct_at_trough = max_dd / peak * 100
    wins = pnl[pnl > 0]
    losses = pnl[pnl <= 0]
    streak = best = 0
    for p in pnl:
        streak = streak + 1 if p <= 0 else 0
        best = max(best, streak)
    return {
        "n": len(pnl),
        "wr": len(wins) / len(pnl) * 100 if len(pnl) else float("nan"),
        "pf": wins.sum() / abs(losses.sum()) if losses.sum() else float("inf"),
        "net": pnl.sum(),
        "dd_usd": max_dd,
        "dd_pct": dd_pct_at_trough,
        "rf": pnl.sum() / max_dd if max_dd else float("inf"),
        "r1_median_loss": abs(losses.median()) if len(losses) else float("nan"),
        "max_consec_losses": best,
    }


def report(label: str, m: dict) -> None:
    print(f"  {label:18s} N={m['n']:<4d} WR={m['wr']:5.2f}%  PF={m['pf']:6.3f}  "
          f"Net=${m['net']:>12,.2f}  DD=${m['dd_usd']:>10,.2f} ({m['dd_pct']:.2f}%)  "
          f"RF={m['rf']:6.2f}  1R=${m['r1_median_loss']:,.2f}  maxLstreak={m['max_consec_losses']}")


def main() -> int:
    missing = [p for p in CONFIGS.values() if not p.exists()]
    if missing:
        print("SKIP — gitignored vendor CSVs absent (public clone?):")
        for p in missing:
            print(f"  {p}")
        return 0

    results: dict[str, dict] = {}
    for name, path in CONFIGS.items():
        print(f"\n=== {name} — {path.name} ===")
        t = load_trades(path)
        h1 = t[t["exit_dt"] < SPLIT_DATE]
        h2 = t[t["exit_dt"] >= SPLIT_DATE]
        r = {
            "full_raw": metrics(t["pnl"]), "full_static": metrics(t["pnl_static"]),
            "h1_raw": metrics(h1["pnl"]), "h1_static": metrics(h1["pnl_static"]),
            "h2_raw": metrics(h2["pnl"]), "h2_static": metrics(h2["pnl_static"]),
        }
        results[name] = r
        for k in ("full_raw", "full_static", "h1_raw", "h1_static", "h2_raw", "h2_static"):
            report(k, r[k])

        claims = BRIEF_CLAIMS[name]
        print(f"  vs parent-session table: N {r['full_raw']['n']} vs {claims['n']} "
              f"| RF {r['full_raw']['rf']:.2f} vs {claims['rf']} "
              f"| H1 RF {r['h1_raw']['rf']:.2f} vs {claims['h1_rf']} "
              f"| H2 RF {r['h2_raw']['rf']:.2f} vs {claims['h2_rf']}")

        # Aug 2023 critical trade (brief §2.3: entry ~2023-08-17, ~22.65)
        win = t[(t["entry_dt"] >= "2023-08-10") & (t["entry_dt"] <= "2023-08-25")]
        print("  Aug-2023 window trades:")
        for _, row in win.iterrows():
            print(f"    entry {row['entry_dt']} @ {row['entry_px']}  ->  "
                  f"exit {row['exit_dt']} @ {row['exit_px']}  pnl ${row['pnl']:,.2f}")

    print("\n=== RF improvement, be4.8 vs baseline ===")
    for seg in ("full", "h1", "h2"):
        for basis in ("raw", "static"):
            a = results["be4.8"][f"{seg}_{basis}"]["rf"]
            b = results["baseline"][f"{seg}_{basis}"]["rf"]
            print(f"  {seg:5s} {basis:6s}: {a:6.2f} / {b:6.2f}  = {a / b:5.2f}x  ({(a / b - 1) * 100:+.1f}%)")

    print("\n=== cross-check: canonical reconcile.py (raw basis) ===")
    for name, path in CONFIGS.items():
        df = pd.read_csv(path, encoding="utf-8-sig").rename(columns=RENAME)
        tmp = Path(tempfile.gettempdir()) / f"gs_norm_{name.replace('.', '')}.csv"
        df.to_csv(tmp, index=False)
        out = subprocess.run([sys.executable, str(RECONCILE), str(tmp), "--strategy", "guardian"],
                             capture_output=True, text=True)
        print(f"--- {name} ---")
        print(out.stdout.strip())
        if out.returncode != 0:
            print("RECONCILE STDERR:", out.stderr[-1000:])
    return 0


if __name__ == "__main__":
    sys.exit(main())
