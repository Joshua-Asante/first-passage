#!/usr/bin/env python3
"""
trade-csv-reconcile — canonical pipeline for TradingView trade CSV exports.

Compresses the boilerplate that was being re-derived every analytical session:
  - CSV load with BOM handling
  - Entry/Exit pairing by Trade # (pyramid-safe)
  - R-pinning per strategy archetype
  - Headline metrics (PF/WR/DD/RF/Net/RF)
  - Reconciliation against Pine-header baselines

Usage:
  python reconcile.py <csv_path> [--strategy NAME] [--baseline] [--scale]
                                 [--account 200000]

  --strategy   guardian | striker_dj30 | striker_nas | aegis
               (auto-detect from filename if omitted)
  --baseline   reconcile against references/baselines.md anchors
  --scale      report allocation-scaled P&L for portfolio aggregation
  --account    initial equity for DD reconstruction (default $200,000)

Conventions enforced (do not bypass without strong reason):
  - Realized P&L only on Exit rows (filter Type.startswith('Exit'))
  - Pyramid arch: pair by Trade #, not row sequence
  - Guardian uses median loss; Striker/NAS/Aegis use full-stop mean (|loss| > 1% of account)
  - Fallback to median ONLY if n_full_stops == 0 (corrected commit bf32aa3, 2026-04-23)
  - Thin-cohort warning when 1 <= n < 5

If reconciliation fails, this script does NOT silently re-baseline. It prints
HALT and the triage path from SKILL.md Step 5.
"""

from __future__ import annotations
import argparse
import sys
import re
import json
from dataclasses import dataclass, asdict, field
from pathlib import Path

import pandas as pd  # type: ignore
import numpy as np  # type: ignore


# ---------------------------------------------------------------------------
# Strategy registry — embedded copy of references/baselines.md anchors.
# Update on every re-lock. The references file is the authoritative narrative;
# this dict is the executable subset used by --baseline reconciliation.
# ---------------------------------------------------------------------------

STRATEGIES = {
    "guardian": {
        "label": "Guardian Gold v5.5",
        "instrument": "XAUUSD",
        "architecture": "trend_rider",  # no BE, no trail
        "r_basis": "median",
        "risk_pct": 0.34,
        "contract_value": 100,
        "pyramid": False,
        "baselines": {
            "pepperstone": {
                "n": 203, "pf": 3.750, "wr_pct": 22.17,
                "net": 571_840.77, "dd_pct": 5.01, "rf": 23.65,
                "lock_date": "2026-04-23",
                "panel": "2022-01-04 to 2026-04-20 (52mo)",
            },
        },
    },
    "striker_dj30": {
        "label": "Striker DJ30 v4.5",
        "instrument": "DJ30 / US30",
        "architecture": "breakout_pyramid_be",
        "r_basis": "full_stop_mean",
        "risk_pct": 0.70,
        "contract_value": 10,  # CRITICAL — default of 1 is 10x wrong
        "pyramid": True,
        "expected_pyramid_share": 0.427,  # ~42.7% (Q-DJ30-2 Phase B); the prior 0.94 was a NAS100 cross-strategy misattribution corrected 2026-06-08 in references/baselines.md
        "baselines": {
            "oanda": {
                "n": 225, "pf": 2.755, "wr_pct": 72.00,
                "net": 433_000.00, "dd_pct": 4.81, "rf": None,
                "lock_date": "2026-05-05",
                "panel": "4yr OANDA",
            },
            "pepperstone": {
                # v4.5 Pepperstone: full PF/WR/DD pending re-export per memory
                "n": 218, "pf": 3.373, "wr_pct": 72.94,
                "net": 440_447.54, "dd_pct": 6.22, "rf": 21.40,
                "r_dollars": 4_240.13,
                "lock_date": "2026-05-05",
                "panel": "4yr Pepperstone",
                "note": "1R pinned; full headline pending re-export",
            },
        },
        "legacy": {
            "v4_4_pepperstone": {
                "n": 229, "pf": 2.272, "wr_pct": 71.18,
                "net": 279_437.56, "dd_pct": 5.09, "rf": 18.29,
                "lock_date": "2026-04-20",
            },
        },
    },
    "striker_nas": {
        "label": "Striker NAS100 v1",
        "instrument": "NAS100",
        "architecture": "breakout_pyramid_be",
        "r_basis": "full_stop_mean",
        "risk_pct": 0.37,
        "contract_value": 10,
        "pyramid": True,
        "expected_pyramid_share": 0.885,
        "baselines": {
            "pepperstone": {
                "n": 196, "pf": 3.717, "wr_pct": 55.61,
                "net": 369_698.41, "dd_pct": 3.54, "rf": 18.82, "r_dollars": 3_940.31,
                "lock_date": "2026-05-05",
                "panel": "4yr+ Pepperstone",
            },
        },
    },
    "aegis": {
        "label": "Aegis-Reversion USDJPY v4.3",
        "instrument": "USDJPY",
        "architecture": "mean_revert_be",
        "r_basis": "full_stop_mean",
        "risk_pct": 1.50,
        "contract_value": 1,  # default — USDJPY direct match
        "pyramid": False,
        "baselines": {
            "pepperstone": {
                "n": 124, "pf": 4.188, "wr_pct": 60.48,
                "net": 178_298.13, "dd_pct": 4.30, "rf": 20.72, "r_dollars": 3_293.45,
                "lock_date": "2026-04-22",
                "panel": "4yr Pepperstone",
            },
            "oanda": {
                "n": 123, "pf": 4.91, "wr_pct": 63.41,
                "net": 212_678.00, "dd_pct": 4.27, "rf": 24.90,
                "lock_date": "2026-04-22",
                "panel": "4yr OANDA",
                "note": "USDJPY broker-uniform (123t identical across feeds)",
            },
        },
    },
}

TOLERANCES = {
    "n": 0,           # exact
    "pct_metric": 0.005,  # PF / Net within 0.5%
    "dd": 0.01,       # DD within 1% absolute
    "wr": 0.005,      # WR within 0.5pp
}


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Metrics:
    n: int
    wins: int
    losses: int
    wr_pct: float
    gross_win: float
    gross_loss: float
    pf: float
    net: float
    avg_win: float
    avg_loss: float
    max_dd_dollars: float
    max_dd_pct: float
    rf: float
    r_basis: str
    r_n_cohort: int
    r_dollars: float
    cohort_warning: bool
    pyramid_pnl_share: float | None = None


@dataclass
class ReconcileResult:
    strategy: str
    feed: str | None
    metrics: Metrics
    baseline: dict | None
    drifts: list[str] = field(default_factory=list)
    halted: bool = False


# ---------------------------------------------------------------------------
# Parser — handles BOM, pyramid pairing, double-count trap
# ---------------------------------------------------------------------------

# TradingView renamed several export columns in its 2026 schema. Map every known
# variant back to the canonical internal names the rest of the pipeline depends
# on, WITHOUT clobbering a canonical column already present (so a file carrying
# both forms keeps the canonical one). Handles legacy + current headers.
COLUMN_ALIASES = {
    "Trade number": "Trade #",
    "Net PnL USD": "Net P&L USD",
    "Net PnL %": "Net P&L %",
    # 2026-07-05 (Aegis→6J deep export): TV renamed the per-trade return
    # column again — current futures-era exports carry "Return %" where the
    # 2026-06 schema had "Net PnL %". Same normalization rule (no clobber).
    "Return %": "Net P&L %",
    "Cumulative PnL USD": "Cumulative P&L USD",
    "Cumulative PnL %": "Cumulative P&L %",
}


def load_csv(path: str | Path) -> pd.DataFrame:
    """
    Load a TradingView trade CSV with BOM handling and column normalization.
    Returns the full DataFrame including both Entry and Exit rows.
    """
    df = pd.read_csv(path, encoding="utf-8-sig")
    df.columns = [c.strip().replace("\ufeff", "") for c in df.columns]

    rename_map = {
        src: dst
        for src, dst in COLUMN_ALIASES.items()
        if src in df.columns and dst not in df.columns
    }
    if rename_map:
        df = df.rename(columns=rename_map)

    required = {"Trade #", "Type", "Date and time", "Net P&L USD"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(
            f"CSV missing required columns: {missing}. "
            f"Available: {list(df.columns)}"
        )

    df["dt"] = pd.to_datetime(df["Date and time"], errors="coerce")
    return df


def detect_strategy_from_filename(path: str | Path) -> str | None:
    """Best-effort strategy detection from filename."""
    name = Path(path).name.lower()
    if "guardian" in name or "xauusd" in name:
        return "guardian"
    if "striker" in name and ("nas100" in name or "us100" in name):
        return "striker_nas"
    if "striker" in name and ("dj30" in name or "us30" in name):
        return "striker_dj30"
    if "aegis" in name or "usdjpy" in name:
        return "aegis"
    return None


def detect_feed_from_filename(path: str | Path) -> str | None:
    name = Path(path).name.upper()
    for feed in ("PEPPERSTONE", "OANDA", "ALCHEMY"):
        if feed in name:
            return feed.lower()
    return None


# ---------------------------------------------------------------------------
# Metrics computation — exits-only for P&L, pyramid-aware
# ---------------------------------------------------------------------------

def compute_metrics(
    df: pd.DataFrame,
    strategy: str,
    account: float = 200_000.0,
) -> Metrics:
    spec = STRATEGIES[strategy]
    is_pyramid = spec["pyramid"]

    # Trap #3: P&L on Exit rows ONLY (Q-A1-c, 2026-04-29 — Entry+Exit double-count)
    exits = df[df["Type"].str.startswith("Exit", na=False)].copy()

    # For pyramid arch, multiple Entry rows per Trade # — but realized P&L
    # is on the (single) Exit row per Trade #. Group by Trade # at exit to
    # collapse any rare multi-exit cases.
    exits = exits.sort_values("dt").reset_index(drop=True)

    n = len(exits)
    if n == 0:
        raise ValueError("No Exit rows found — check CSV provenance and Type column")

    pnl = exits["Net P&L USD"].astype(float)
    wins_mask = pnl > 0
    wins = int(wins_mask.sum())
    losses = n - wins

    gross_win = float(pnl[wins_mask].sum())
    gross_loss = float(pnl[~wins_mask].sum())  # negative
    pf = gross_win / abs(gross_loss) if gross_loss != 0 else float("inf")
    net = float(pnl.sum())
    avg_win = gross_win / wins if wins else 0.0
    avg_loss = gross_loss / losses if losses else 0.0
    wr_pct = wins / n * 100

    # DD reconstruction on static initial equity
    eq = account
    peak = eq
    max_dd_dollars = 0.0
    max_dd_pct = 0.0
    for x in pnl:
        eq += x
        if eq > peak:
            peak = eq
        dd_d = peak - eq
        if dd_d > max_dd_dollars:
            max_dd_dollars = dd_d
            max_dd_pct = dd_d / peak * 100

    rf = net / max_dd_dollars if max_dd_dollars else float("inf")

    # R-basis pinning per architecture
    r_basis_method, r_dollars, r_n_cohort, cohort_warning = pin_r_basis(
        pnl, spec["r_basis"], account
    )

    # Pyramid share (if applicable) — sum of P&L attributable to pyramid-add legs.
    # Heuristic: TradingView labels Signal column with the entry tag, e.g.
    # "Add 1", "Add 2" for pyramid legs vs base entry signal. Match exits whose
    # corresponding entry was a pyramid add by joining on Trade # and entry order.
    pyramid_pnl_share = None
    if is_pyramid:
        pyramid_pnl_share = compute_pyramid_share(df, exits)

    return Metrics(
        n=n,
        wins=wins,
        losses=losses,
        wr_pct=wr_pct,
        gross_win=gross_win,
        gross_loss=gross_loss,
        pf=pf,
        net=net,
        avg_win=avg_win,
        avg_loss=avg_loss,
        max_dd_dollars=max_dd_dollars,
        max_dd_pct=max_dd_pct,
        rf=rf,
        r_basis=r_basis_method,
        r_n_cohort=r_n_cohort,
        r_dollars=r_dollars,
        cohort_warning=cohort_warning,
        pyramid_pnl_share=pyramid_pnl_share,
    )


def pin_r_basis(
    pnl: pd.Series,
    method: str,
    account: float,
) -> tuple[str, float, int, bool]:
    """
    Apply the R-basis convention. Returns (method_used, r_dollars, n_cohort, warning).

    Convention (locked):
      - method == 'median': median of |loss| values
      - method == 'full_stop_mean': mean of |loss| values where |loss| > 1% of account
        - Fallback: if n_full_stops == 0, fall back to median (NOT n<5 — that was the trap)
        - Warning: if 1 <= n_full_stops < 5, flag thin-cohort
    """
    losses = pnl[pnl < 0].abs()
    if len(losses) == 0:
        # No losses at all — pathological; return 0 with warning
        return ("median (zero losses)", 0.0, 0, True)

    median_loss = float(losses.median())

    if method == "median":
        return ("median loss (trend-rider)", median_loss, len(losses), False)

    if method == "full_stop_mean":
        full_stop_threshold = 0.01 * account  # 1% of account
        full_stops = losses[losses > full_stop_threshold]
        n_fs = len(full_stops)

        if n_fs == 0:
            return (
                "median loss (FALLBACK — zero full stops)",
                median_loss,
                0,
                True,
            )

        warning = 1 <= n_fs < 5
        return (
            f"full-stop mean (|loss| > 1% acct, n={n_fs})"
            + (" THIN COHORT" if warning else ""),
            float(full_stops.mean()),
            n_fs,
            warning,
        )

    raise ValueError(f"Unknown r_basis method: {method}")


def compute_pyramid_share(df: pd.DataFrame, exits: pd.DataFrame) -> float | None:
    """
    Estimate pyramid P&L share. Each Trade # may have multiple Entry rows
    (base + pyramid adds). Realized P&L is at exit; we approximate the
    pyramid-add contribution by treating non-base entries as pyramid legs
    and apportioning the trade's P&L by qty.

    This is an estimate, not exact — for precise attribution use the Pine
    source's signal labels. Returns None if the structure isn't detectable.
    """
    if "Signal" not in df.columns:
        return None

    # Current TV schema: each pyramid leg is its own Trade # whose Signal carries
    # an "Add" tag ("Long Add" / "Exit Long Add"). P&L is realized per-leg, so the
    # pyramid share is add-leg exit P&L over total net (direct attribution). NB
    # this differs structurally from the legacy qty-apportionment below and from
    # the counterfactual "pyramid is the edge" framing — the expected_pyramid_share
    # anchors predate the per-leg schema, so the RED FLAG is advisory under the new
    # format until those anchors are re-measured.
    exit_signal = exits["Signal"].astype(str)
    add_exits = exit_signal.str.contains("Add", case=False, na=False)
    if add_exits.any():
        total = float(exits["Net P&L USD"].astype(float).sum())
        if total == 0:
            return None
        add_pnl = float(exits.loc[add_exits, "Net P&L USD"].astype(float).sum())
        return add_pnl / total

    # Legacy schema: multiple Entry rows per Trade #, one combined exit; apportion
    # the trade's realized P&L by entry-leg size.
    if "Size (qty)" not in df.columns:
        return None

    entries = df[df["Type"].str.startswith("Entry", na=False)].copy()
    if entries.empty:
        return None

    # Group entries by Trade #; "pyramid" entries are the 2nd+ entries per Trade #
    # (or those whose Signal contains "Add", "Pyr", "P1", "P2" — depends on Pine).
    pyramid_pnl_total = 0.0
    base_pnl_total = 0.0

    for trade_num, exit_row in exits.set_index("Trade #").iterrows():
        trade_entries = entries[entries["Trade #"] == trade_num].sort_values("dt")
        if len(trade_entries) <= 1:
            base_pnl_total += float(exit_row["Net P&L USD"])
            continue

        # Apportion the Trade #'s realized P&L by size of each entry leg
        sizes = trade_entries["Size (qty)"].astype(float).values
        total_size = sizes.sum()
        if total_size == 0:
            continue

        trade_pnl = float(exit_row["Net P&L USD"])
        # Base entry = first; pyramid adds = subsequent
        base_share = sizes[0] / total_size
        pyr_share = 1.0 - base_share

        base_pnl_total += trade_pnl * base_share
        pyramid_pnl_total += trade_pnl * pyr_share

    total = base_pnl_total + pyramid_pnl_total
    if total == 0:
        return None
    return pyramid_pnl_total / total


# ---------------------------------------------------------------------------
# Futures P&L identity check (2026-07-05, Aegis→6J transfer lane)
# ---------------------------------------------------------------------------

@dataclass
class FuturesIdentityResult:
    n_checked: int
    n_pass: int
    max_abs_dev: float
    tolerance: float
    off_grid_prices: int
    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.n_pass == self.n_checked and self.off_grid_prices == 0


def check_futures_identity(
    df: pd.DataFrame,
    pointvalue: float,
    tick: float | None = None,
    commission: float = 0.0,
    tolerance: float = 0.51,
) -> FuturesIdentityResult:
    """
    Verify the per-trade futures P&L identity against Entry/Exit fill prices:

        short:  net == qty * (entry - exit) * pointvalue - 2 * commission * qty
        long:   net == qty * (exit - entry) * pointvalue - 2 * commission * qty

    TV embeds slippage in the recorded fill prices, so the identity holds on
    CSV prices as-is; commission is cash-per-contract per side. `tick`, when
    given, additionally verifies every fill price sits on the contract tick
    grid (an off-grid price means the CSV is not from the futures symbol it
    claims). Default tolerance $0.51 covers cent-rounding on both rows.

    Pairs Entry/Exit rows by Trade #. Multi-exit trades (pyramid per-leg
    schema) are checked per Trade # using that trade's own entry row.
    """
    need = {"Trade #", "Type", "Price USD", "Size (qty)", "Net P&L USD"}
    missing = need - set(df.columns)
    if missing:
        raise ValueError(f"futures identity check needs columns {missing}")

    entries = df[df["Type"].str.startswith("Entry", na=False)]
    exits = df[df["Type"].str.startswith("Exit", na=False)]

    n_checked = 0
    n_pass = 0
    max_abs_dev = 0.0
    off_grid = 0
    failures: list[str] = []

    def on_grid(price: float) -> bool:
        if tick is None or tick <= 0:
            return True
        ratio = price / tick
        return abs(ratio - round(ratio)) < 1e-6

    for trade_num, exit_row in exits.set_index("Trade #").iterrows():
        ent = entries[entries["Trade #"] == trade_num]
        if ent.empty:
            failures.append(f"Trade {trade_num}: no Entry row")
            n_checked += 1
            continue
        ent_row = ent.iloc[0]

        qty = float(exit_row["Size (qty)"])
        entry_p = float(ent_row["Price USD"])
        exit_p = float(exit_row["Price USD"])
        net = float(exit_row["Net P&L USD"])
        is_short = "short" in str(exit_row["Type"]).lower()

        for label, price in (("entry", entry_p), ("exit", exit_p)):
            if not on_grid(price):
                off_grid += 1
                failures.append(
                    f"Trade {trade_num}: {label} price {price} off the "
                    f"{tick} tick grid"
                )

        sign = 1.0 if is_short else -1.0
        expected = sign * qty * (entry_p - exit_p) * pointvalue \
            - 2.0 * commission * qty
        dev = abs(net - expected)
        max_abs_dev = max(max_abs_dev, dev)
        n_checked += 1
        if dev <= tolerance:
            n_pass += 1
        else:
            failures.append(
                f"Trade {trade_num}: net={net:.2f} expected={expected:.2f} "
                f"dev={dev:.2f} (qty={qty:g}, {'short' if is_short else 'long'})"
            )

    return FuturesIdentityResult(
        n_checked=n_checked,
        n_pass=n_pass,
        max_abs_dev=max_abs_dev,
        tolerance=tolerance,
        off_grid_prices=off_grid,
        failures=failures,
    )


# ---------------------------------------------------------------------------
# Reconciliation
# ---------------------------------------------------------------------------

def reconcile(
    metrics: Metrics,
    strategy: str,
    feed: str | None,
) -> tuple[dict | None, list[str]]:
    """Return (baseline_dict_used, list_of_drift_messages)."""
    spec = STRATEGIES[strategy]
    if feed is None or feed not in spec.get("baselines", {}):
        return (None, [
            f"NO BASELINE for feed={feed} on strategy={strategy}. "
            "Reconciliation skipped — provide --strategy and ensure feed in filename."
        ])

    bl = spec["baselines"][feed]
    drifts: list[str] = []

    def cmp_n(actual, baseline, label):
        if baseline is None:
            return
        if int(actual) != int(baseline):
            drifts.append(f"{label}: actual={actual} baseline={baseline}")

    def cmp_pct(actual, baseline, label, tol_key):
        if baseline is None:
            return
        if baseline == 0:
            return
        rel = abs(actual - baseline) / abs(baseline)
        if rel > TOLERANCES[tol_key]:
            drifts.append(
                f"{label}: actual={actual:.4f} baseline={baseline:.4f} "
                f"rel_drift={rel*100:.2f}% (tol={TOLERANCES[tol_key]*100:.1f}%)"
            )

    def cmp_abs(actual, baseline, label, tol):
        if baseline is None:
            return
        if abs(actual - baseline) > tol:
            drifts.append(
                f"{label}: actual={actual:.4f} baseline={baseline:.4f} "
                f"abs_drift={abs(actual-baseline):.4f} (tol={tol:.4f})"
            )

    cmp_n(metrics.n, bl.get("n"), "N (trade count)")
    cmp_pct(metrics.pf, bl.get("pf"), "PF", "pct_metric")
    cmp_pct(metrics.net, bl.get("net"), "Net", "pct_metric")
    cmp_abs(metrics.max_dd_pct, bl.get("dd_pct"), "DD%", TOLERANCES["dd"])
    cmp_abs(metrics.wr_pct / 100, (bl.get("wr_pct") or 0) / 100, "WR", TOLERANCES["wr"])

    return (bl, drifts)


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def format_output(
    result: ReconcileResult,
    do_scale: bool = False,
    account: float = 200_000.0,
) -> str:
    m = result.metrics
    spec = STRATEGIES[result.strategy]
    lines = []
    lines.append(f"=== {spec['label']} — {result.feed or 'feed=?'} ===")

    def reconcile_tag(label: str) -> str:
        if not result.baseline:
            return ""
        for d in result.drifts:
            if d.startswith(label):
                return f"  [reconcile: DRIFT — {d.split(':',1)[1].strip()}]"
        return "  [reconcile: OK]" if result.baseline else ""

    lines.append(f"N        : {m.n}{reconcile_tag('N (trade count)')}")
    lines.append(f"PF       : {m.pf:.3f}{reconcile_tag('PF')}")
    lines.append(f"WR       : {m.wr_pct:.2f}%{reconcile_tag('WR')}")
    lines.append(f"Net      : ${m.net:,.2f}{reconcile_tag('Net')}")
    lines.append(f"DD       : {m.max_dd_pct:.2f}% (${m.max_dd_dollars:,.2f}){reconcile_tag('DD%')}")
    lines.append(f"RF       : {m.rf:.2f}")
    lines.append(f"1R basis : {m.r_basis}")
    lines.append(f"1R       : ${m.r_dollars:,.2f}")

    if m.pyramid_pnl_share is not None:
        expected = spec.get("expected_pyramid_share")
        exp_str = f" (expected ~{expected*100:.0f}%)" if expected else ""
        flag = ""
        if expected and m.pyramid_pnl_share < 0.50:
            flag = ("  [advisory: add-leg P&L share < 50% — under the current "
                    "per-leg TV schema this is direct attribution, not the legacy "
                    "qty-apportioned anchor; re-measure expected_pyramid_share "
                    "before treating as a flag]")
        lines.append(f"Pyramid  : {m.pyramid_pnl_share*100:.1f}%{exp_str}{flag}")

    if do_scale and m.r_dollars > 0:
        target_pct = spec["risk_pct"]
        implied_pct = (m.r_dollars / account) * 100
        scale = target_pct / implied_pct
        scaled_net = m.net * scale
        scaled_dd = m.max_dd_pct * scale
        lines.append("")
        lines.append(f"--- Scaled to {target_pct:.2f}% target ---")
        lines.append(f"  scale_factor : {scale:.4f}  (implied={implied_pct:.3f}%, target={target_pct:.2f}%)")
        lines.append(f"  scaled Net   : ${scaled_net:,.2f}")
        lines.append(f"  scaled DD    : ~{scaled_dd:.2f}%")

    if result.drifts:
        lines.append("")
        lines.append("*** HALT — DRIFT DETECTED ***")
        for d in result.drifts:
            lines.append(f"  - {d}")
        lines.append("")
        lines.append("Triage path (SKILL.md Step 5):")
        lines.append("  1. Filename/feed mislabel? Check CSV symbol header.")
        lines.append("  2. Stale anchor in references/baselines.md? Re-read Pine.")
        lines.append("  3. Genuine version drift? Confirm with user before re-baseline.")
        lines.append("  4. Pine paste mid-edit? Reproduce headline before treating as canonical.")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv_path", help="Path to TradingView trade CSV")
    ap.add_argument("--strategy", choices=list(STRATEGIES.keys()),
                    help="Strategy identifier (auto-detected from filename if omitted)")
    ap.add_argument("--feed", choices=["pepperstone", "oanda", "alchemy"],
                    help="Feed identifier (auto-detected from filename if omitted)")
    ap.add_argument("--baseline", action="store_true",
                    help="Reconcile against Pine-header baseline anchors")
    ap.add_argument("--scale", action="store_true",
                    help="Report allocation-scaled P&L for portfolio aggregation")
    ap.add_argument("--account", type=float, default=200_000.0,
                    help="Initial equity for DD reconstruction (default $200,000)")
    ap.add_argument("--json", action="store_true",
                    help="Emit JSON output instead of formatted text")
    ap.add_argument("--pointvalue", type=float, default=None,
                    help="Futures point value (USD per 1.00 price move per "
                         "contract, e.g. 12500000 for CME 6J). Enables the "
                         "per-trade futures P&L identity check.")
    ap.add_argument("--tick", type=float, default=None,
                    help="Contract tick size (e.g. 0.0000005 for 6J). With "
                         "--pointvalue, also verifies fills sit on the tick grid.")
    ap.add_argument("--commission", type=float, default=0.0,
                    help="Cash commission per contract per side (e.g. 1.30). "
                         "Used by the futures identity check.")
    args = ap.parse_args(argv)

    strategy = args.strategy or detect_strategy_from_filename(args.csv_path)
    if strategy is None:
        print("ERROR: could not detect strategy from filename. Use --strategy.",
              file=sys.stderr)
        return 2

    feed = args.feed or detect_feed_from_filename(args.csv_path)

    df = load_csv(args.csv_path)
    metrics = compute_metrics(df, strategy, account=args.account)

    fut_identity = None
    if args.pointvalue is not None:
        fut_identity = check_futures_identity(
            df, pointvalue=args.pointvalue, tick=args.tick,
            commission=args.commission,
        )

    baseline = None
    drifts: list[str] = []
    if args.baseline:
        baseline, drifts = reconcile(metrics, strategy, feed)

    result = ReconcileResult(
        strategy=strategy,
        feed=feed,
        metrics=metrics,
        baseline=baseline,
        drifts=drifts,
        halted=bool(drifts),
    )

    if args.json:
        out = {
            "strategy": strategy,
            "feed": feed,
            "metrics": asdict(metrics),
            "baseline": baseline,
            "drifts": drifts,
            "halted": bool(drifts),
        }
        if fut_identity is not None:
            out["futures_identity"] = asdict(fut_identity)
            out["futures_identity"]["ok"] = fut_identity.ok
        print(json.dumps(out, indent=2, default=str))
    else:
        print(format_output(result, do_scale=args.scale, account=args.account))
        if fut_identity is not None:
            fi = fut_identity
            status = "OK" if fi.ok else "FAIL"
            print(f"Futures identity ({status}): {fi.n_pass}/{fi.n_checked} trades "
                  f"within ${fi.tolerance:.2f} (max dev ${fi.max_abs_dev:.2f}); "
                  f"off-grid prices: {fi.off_grid_prices}")
            for f in fi.failures[:20]:
                print(f"  - {f}")

    # Exit code: non-zero if drift or identity failure detected (CI-friendly)
    if fut_identity is not None and not fut_identity.ok:
        return 1
    return 1 if drifts else 0


if __name__ == "__main__":
    sys.exit(main())
