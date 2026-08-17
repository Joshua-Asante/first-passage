"""Stage-1 OUTCOME-FREE diagnostics for MNQ-SIZEDIV-1 (DESIGN_FREEZE §4).

Reads the confirm-year trades cache (conditioner only) + the panel's TIME
column (session calendar). NO price/return series is loaded here — the
quarantine is structural: this module imports load_calendar, never
load_slot_returns.

Writes STAGE1_DIAG.md (committed) + stage1_sessions.csv (gitignored,
QUARANTINED: contains A(s) for confirm-era sessions; never join returns to it
outside the Stage-3 battery).
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from datetime import date as _date
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from sizediv_lib import combine_stats, load_calendar, session_stats, sizediv  # noqa: E402

try:
    import databento as db
except ImportError:
    sys.exit("databento not installed (research venv required).")

PANEL_DEFAULT = r"C:\Users\joshu\multi_firm_operations\core\data\bar_data\MNQ_M15.csv"
CACHE_DEFAULT = Path.home() / ".databento_cache" / "mnq_sizediv_blind_2026-08" / "confirm_year"
PANEL_END = _date(2026, 7, 3)  # calendar authority ends here; span rule after (FREEZE §1)
CHUNK = 5_000_000

# FROZEN Stage-1 rules (FREEZE §4)
D1_MIN_SIGNABLE_SHARE = 0.50
D1_MIN_FULL_SESSIONS = 240
D2_MAX_CORR = 0.995
D3_MIN_TICK_AGREE = 0.50


def iter_chunks(path: Path):
    store = db.DBNStore.from_file(path)
    try:
        it = store.to_df(count=CHUNK)
    except TypeError:  # older SDK: no count kwarg
        yield store.to_df()
        return
    if isinstance(it, pd.DataFrame):
        yield it
        return
    for chunk in it:
        yield chunk


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache-dir", default=str(CACHE_DEFAULT))
    ap.add_argument("--panel", default=PANEL_DEFAULT)
    ap.add_argument("--out", default=str(Path(__file__).parent / "STAGE1_DIAG.md"))
    args = ap.parse_args()

    files = sorted(Path(args.cache_dir).rglob("*.dbn*"))
    files = [f for f in files if f.suffix != ".json" and "metadata" not in f.name]
    if not files:
        sys.exit(f"no DBN files under {args.cache_dir}")
    print(f"[diag] {len(files)} files", flush=True)

    parts = []
    for f in files:
        for chunk in iter_chunks(f):
            if "side" not in chunk.columns:
                sys.exit(f"ABORT D1: no `side` column in {f.name} — trades schema unusable as frozen; "
                         f"STOP + operator re-election (FREEZE §2).")
            parts.append(session_stats(chunk))
        print(f"[diag] {f.name} done", flush=True)

    stats = sizediv(combine_stats(parts))

    panel_hash = hashlib.sha256(Path(args.panel).read_bytes()).hexdigest()
    cal = load_calendar(args.panel)
    full_panel_dates = set(cal.loc[cal["full"], "date"])

    def is_full(row) -> bool:
        d = row["date"]
        if d <= PANEL_END:
            return d in full_panel_dates
        return d.weekday() < 5 and (row["span_h"] or 0) >= 6.0

    stats["full"] = stats.apply(is_full, axis=1)
    fs = stats[stats["full"]].sort_values("date").reset_index(drop=True)

    signable_share = stats["n_signable"].sum() / max(stats["n_prints"].sum(), 1)
    corr_vw_cw = float(fs["I_vw"].corr(fs["I_cw"]))
    tick_num = stats["tick_agree"].sum()
    tick_den = tick_num + stats["tick_disagree"].sum()
    tick_agree = tick_num / max(tick_den, 1)
    a = fs["A"].to_numpy()
    ac1 = float(pd.Series(a).autocorr(1)) if len(a) > 2 else np.nan

    d1_kill = (signable_share < D1_MIN_SIGNABLE_SHARE) or (len(fs) < D1_MIN_FULL_SESSIONS)
    d2_kill = corr_vw_cw > D2_MAX_CORR
    d3_flip = tick_agree < D3_MIN_TICK_AGREE
    verdict = "KILL" if (d1_kill or d2_kill) else "CLEAN"

    monthly = fs.assign(month=fs["date"].map(lambda d: f"{d.year}-{d.month:02d}")) \
                .groupby("month")["A"].agg(["mean", "std", "count"])

    out_csv = Path(__file__).parent / "stage1_sessions.csv"
    fs.to_csv(out_csv, index=False)

    lines = [
        "# MNQ-SIZEDIV-1 — STAGE1_DIAG (outcome-free; confirm-year conditioner)",
        "",
        f"**Run:** {pd.Timestamp.utcnow().isoformat(timespec='seconds')} · cache `{args.cache_dir}`",
        f"**Panel (calendar only):** `{args.panel}` sha256 `{panel_hash[:16]}…` (time column read; no prices)",
        "",
        "> ⚠ **QUARANTINE.** `stage1_sessions.csv` holds A(s) for CONFIRM-era sessions.",
        "> No return series may be joined to it before the Stage-3 battery (FREEZE §3).",
        "",
        "| Metric | Value | Frozen rule | Result |",
        "|---|---|---|---|",
        f"| Sessions parsed / full | {len(stats)} / {len(fs)} | full ≥ {D1_MIN_FULL_SESSIONS} | {'KILL' if len(fs) < D1_MIN_FULL_SESSIONS else 'ok'} |",
        f"| Signable share | {signable_share:.4f} | ≥ {D1_MIN_SIGNABLE_SHARE} | {'KILL' if signable_share < D1_MIN_SIGNABLE_SHARE else 'ok'} |",
        f"| corr(I_vw, I_cw) | {corr_vw_cw:.4f} | ≤ {D2_MAX_CORR} | {'KILL' if d2_kill else 'ok'} |",
        f"| Tick-rule agreement | {tick_agree:.4f} (n={tick_den:,}) | ≥ {D3_MIN_TICK_AGREE} else flip | {'FLIP' if d3_flip else 'B=buy confirmed'} |",
        f"| sd(A) / AC1(A) | {np.nanstd(a):.5f} / {ac1:.3f} | report-only | — |",
        "",
        f"**Verdict: `{verdict}`**" + (" — side semantics FLIP recorded (symmetric, per FREEZE §1)." if d3_flip else ""),
        "",
        "## Monthly A(s) (report-only)",
        "",
        monthly.to_markdown(),
        "",
    ]
    Path(args.out).write_text("\n".join(lines), encoding="utf-8")
    print(f"[diag] verdict={verdict} flip={d3_flip} -> {args.out}", flush=True)


if __name__ == "__main__":
    main()
