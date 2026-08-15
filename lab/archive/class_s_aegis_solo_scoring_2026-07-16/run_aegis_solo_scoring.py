"""Stage-2 — Aegis-6J **solo** Part A scoring (H-SOLO on the v2.1 winner c05).

Native-futures panel (NOT the CFD-decompound-and-rescale path of candidate #1/#2):
c05 is a native CME:6J1! export already sized cap8 / 0.40% @ $100K, so we decompound to
STATIC $100K and score the daily book DIRECTLY. The 1R pin is a DIAGNOSTIC guard only
(>=5 full-stops, no FALLBACK) — it does NOT feed a re-scale. See HANDOFF.md §1.

H-SOLO (stricter than the gate's >=2-of-4): Part A must PASS on BOTH Tradeify_Select_100K
AND MFFU_Rapid_100K. Bulenox/BluSky diagnostic. Does NOT switch ACTIVE_FIRM; reads bust via
summarize_outcomes (inside score_candidate) — never compute_default_config()['bust_rate'].

Exit codes: 0 scored; 2 NEEDS_CONTEXT (panel bytes / 1R guard); 3 PHASE0_FAIL.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Sequence

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[2]
_CORE = _ROOT / "core"
_LAB = _ROOT / "lab"
_RECONCILE = _ROOT / ".claude" / "skills" / "trade-csv-reconcile" / "scripts"
for _p in (_CORE, _LAB, _RECONCILE):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from firm_rules import ACTIVE_FIRM, FIRM_RULES  # noqa: E402
from reconcile import pin_r_basis  # noqa: E402
from discovery.prop_survivor_scoring import (  # noqa: E402
    load_scoring_thresholds,
    score_candidate,
)

V21_PREREG = (
    _ROOT / "docs" / "briefs" / "pre-registration"
    / "2026-07-16-aegis-6j-prop-reconstruction-v2.1-tiebreak-prereg.md"
)
V22_PREREG = (
    _ROOT / "docs" / "briefs" / "pre-registration"
    / "2026-07-16-aegis-6j-prop-reconstruction-v2.2-1r-native-guard-prereg.md"
)
GATE_PREREG = (
    _ROOT / "docs" / "briefs" / "pre-registration"
    / "2026-07-13-prop-survivor-scoring-prereg.md"
)
PANEL_CSV = (
    _ROOT / "lab" / "analysis" / "aegis_6j_prop_reconstruction_2026-07"
    / "c05_fill1600_cap8_r40_ed91cd2d.csv"
)
WINNER_SHA = "ED91CD2D5D4075086F3571561AC7F88CE5F36D416E3B088AB4D112050C25C851"
PANEL_START = date(2022, 1, 12)
PANEL_END = date(2026, 6, 30)          # v2 §2.5; drops the 2 post-panel July-2026 tail exits
STATIC_BASE = 100_000.0                 # native $100K band = the firm-tier band
R_BASIS = "full_stop_mean"
MIN_FULL_STOP_N = 5
HSOLO_FIRMS = ("Tradeify_Select_100K", "MFFU_Rapid_100K")
SIG_RE = re.compile(r"SIGNED / FROZEN:\s*2026-07-16\s*/\s*JA")


class NeedsContext(RuntimeError):
    pass


class Phase0Error(RuntimeError):
    pass


def _sha256_lf(path: Path) -> str:
    """Hash CRLF->LF-normalized bytes (manifest is LF-blob-based; robust to autocrlf checkout)."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest().upper()


def phase0_verify() -> None:
    text = V21_PREREG.read_text(encoding="utf-8")
    if not SIG_RE.search(text):
        raise Phase0Error(f"v2.1 §9 signature not in signed form: {V21_PREREG}")
    if "RESOLVED" not in text or "c05" not in text:
        raise Phase0Error("v2.1 does not carry the RESOLVED->c05 winner declaration")
    v22 = V22_PREREG.read_text(encoding="utf-8")
    if not SIG_RE.search(v22):
        raise Phase0Error(f"v2.2 §9 signature not in signed form: {V22_PREREG}")
    if "native-no-rescale only" not in v22:
        raise Phase0Error("v2.2 missing the native-path 1R re-spec scope guard")
    if ACTIVE_FIRM != "FXIFY":
        raise Phase0Error(f"ACTIVE_FIRM={ACTIVE_FIRM!r} — must stay the FXIFY anchor fixture")
    thr = load_scoring_thresholds(GATE_PREREG)
    if thr.eval_bust_ceiling != 0.03 or thr.pass_floor != 0.5:
        raise Phase0Error(f"gate ceilings drifted: {thr}")
    for fk in HSOLO_FIRMS:
        if FIRM_RULES[fk].get("dd_type") != "trailing_locking":
            raise Phase0Error(f"{fk} not trailing_locking (H-SOLO surface changed)")


def resolve_panel() -> Path:
    if not PANEL_CSV.is_file():
        raise NeedsContext(f"winner panel missing: {PANEL_CSV}")
    got = _sha256_lf(PANEL_CSV)
    if got != WINNER_SHA:
        raise NeedsContext(
            f"winner panel sha256 mismatch (LF-normalized):\n  expected {WINNER_SHA}\n  got      {got}"
        )
    return PANEL_CSV


def load_static_panel() -> tuple[np.ndarray, list[float], dict]:
    """Native c05 -> decompound to STATIC $100K -> (business-day daily PnL, per-trade PnLs, meta)."""
    df = pd.read_csv(PANEL_CSV, encoding="utf-8-sig")
    df["dt"] = pd.to_datetime(df["Date and time"])
    exits = df[df["Type"].astype(str).str.startswith("Exit")].copy()
    entries = df[df["Type"].astype(str).str.startswith("Entry")].copy()
    # pair by trade number for entry/exit dates
    ent_dt = entries.set_index("Trade number")["dt"]
    exits = exits.sort_values("dt").reset_index(drop=True)
    exits["entry_dt"] = exits["Trade number"].map(ent_dt).values
    exits["edate"] = exits["dt"].dt.date
    win = exits[(exits["edate"] >= PANEL_START) & (exits["edate"] <= PANEL_END)].copy()
    win = win.sort_values("dt").reset_index(drop=True)

    # detect native band from the compounding path (sanity: ~ $100K)
    last = win.iloc[-1]
    pct = float(last["Cumulative PnL %"])
    detected = STATIC_BASE if abs(pct) < 1e-9 else round((float(last["Cumulative PnL USD"]) / (pct / 100.0)) / 1000) * 1000
    if not (90_000 <= detected <= 110_000):
        raise NeedsContext(f"detected native band ${detected:,.0f} not ~$100K — wrong export?")

    # decompound to STATIC $100K: roe on the compounding equity path, re-based to fixed $100K
    cum_after = win["Cumulative PnL USD"].astype(float)
    cum_before = cum_after.shift(1).fillna(0.0)
    equity_before = detected + cum_before
    roe = win["Net PnL USD"].astype(float) / equity_before
    win["pnl_static"] = roe * STATIC_BASE

    overnight = int((win["entry_dt"].dt.normalize() != win["dt"].dt.normalize()).sum())
    daily = win.assign(d=win["dt"].dt.normalize()).groupby("d")["pnl_static"].sum()
    bdays = pd.bdate_range(daily.index.min(), daily.index.max())
    daily = daily.reindex(bdays).fillna(0.0)

    meta = {
        "panel_file": PANEL_CSV.name,
        "sha256_lf": WINNER_SHA,
        "detected_band": detected,
        "static_base": STATIC_BASE,
        "n_trades": int(len(win)),
        "panel_window": f"{PANEL_START}->{PANEL_END}",
        "span": f"{win['dt'].min().date()}->{win['dt'].max().date()}",
        "n_bdays": int(len(daily)),
        "overnight_holds": overnight,
        "net_static": float(win["pnl_static"].sum()),
        "gross_pos": float(win.loc[win["pnl_static"] > 0, "pnl_static"].sum()),
    }
    _sl = win.loc[win["pnl_static"] < 0, "pnl_static"].abs()
    meta["n_losers"] = int(len(_sl))
    meta["max_static_loss"] = float(_sl.max()) if len(_sl) else 0.0
    meta["full_stop_threshold_1pct"] = 0.01 * STATIC_BASE
    meta["n_full_stops_1pct"] = int((_sl > 0.01 * STATIC_BASE).sum())
    return daily.to_numpy(dtype=float), [float(x) for x in win["pnl_static"]], meta


def one_r_diagnostic(trade_pnls: list[float]) -> dict:
    """v2.2 §2.7' — native-path 1R is a NON-GATING median diagnostic (1R is not a scoring input).

    The full-stop attempt is reported for transparency; no hard-fail on FALLBACK / n<5 here. The
    frozen full-stop hard-fail is retained on any path that re-scales a panel by 1R (not this one).
    """
    s = pd.Series(trade_pnls)
    fs_method, fs_dollars, fs_n, _ = pin_r_basis(s, "full_stop_mean", STATIC_BASE)
    med_method, med_dollars, med_n, _ = pin_r_basis(s, "median", STATIC_BASE)
    return {
        "basis": "median (native-path diagnostic; v2.2 §2.7')",
        "gating": False,
        "median_r_dollars": float(med_dollars),
        "median_n": int(med_n),
        "full_stop_attempt": {
            "method": fs_method,
            "n_full_stops": int(fs_n),
            "dollars": float(fs_dollars),
        },
    }


def main(argv: Sequence[str] | None = None) -> int:
    import argparse

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n-sims", type=int, default=None, help="override sims/seed (default gate 10k)")
    ap.add_argument("--out-dir", type=Path, default=_HERE)
    args = ap.parse_args(list(argv) if argv is not None else None)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    try:
        phase0_verify()
    except Phase0Error as e:
        print(f"[aegis-solo] PHASE0_FAIL: {e}", file=sys.stderr)
        return 3
    try:
        resolve_panel()
        daily, trades, meta = load_static_panel()
    except NeedsContext as e:
        (args.out_dir / "RESULTS.md").write_text(
            f"# Stage-2 — Aegis-6J solo Part A RESULTS\n\n**Verdict:** `NEEDS_CONTEXT`\n\n```\n{e}\n```\n",
            encoding="utf-8")
        print(f"[aegis-solo] NEEDS_CONTEXT: {e}", file=sys.stderr)
        return 2
    # v2.2 §2.7' — native-path 1R is a non-gating median diagnostic (no hard-fail; 1R not a scoring input).
    r_pin = one_r_diagnostic(trades)

    thr = load_scoring_thresholds(GATE_PREREG)
    envelope = "YES" if meta["overnight_holds"] == 0 else "NO"
    gross_edge = meta["gross_pos"]
    print(f"[aegis-solo] panel n={meta['n_trades']} net_static=${meta['net_static']:,.0f} "
          f"1R(median)=${r_pin['median_r_dollars']:,.0f} full_stops={r_pin['full_stop_attempt']['n_full_stops']} "
          f"envelope={envelope} sims/seed={args.n_sims or thr.sims_per_seed} ...", flush=True)

    report = score_candidate(
        strategy_label="aegis-6j-solo-c05",
        candidate_daily_pnl=daily,
        full_res_trades=trades,
        envelope_verdict=envelope,  # type: ignore[arg-type]
        thresholds=thr,
        n_sims=args.n_sims,
        gross_edge_usd=gross_edge,
    )
    out = report.to_dict()
    out["panel_meta"] = meta
    out["r_pin"] = r_pin
    out["hsolo_firms"] = list(HSOLO_FIRMS)

    tiers = out["tiers"]
    part_a = {fk: bool(tiers.get(fk, {}).get("clears_part_a", False)) for fk in HSOLO_FIRMS}
    hsolo = all(part_a.values())
    verdict = "RESOLVED (H-SOLO)" if hsolo else "FALSIFIED"
    out["hsolo_part_a"] = part_a
    out["verdict"] = verdict

    (args.out_dir / "aegis_solo_report.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")

    def _tier_line(fk: str) -> str:
        t = tiers.get(fk, {})
        r2 = t.get("run2", {}) or {}
        return (f"- **{fk}**: Part A {'PASS' if part_a[fk] else 'FAIL'} "
                f"(bust {r2.get('headline_bust', float('nan')):.4f} ≤ {thr.eval_bust_ceiling}, "
                f"pass {r2.get('pass_rate', float('nan')):.4f} ≥ {thr.pass_floor}; gated_on={t.get('gated_on')})")

    results = [
        "# Stage-2 — Aegis-6J solo Part A (H-SOLO) RESULTS",
        "",
        f"**Verdict:** `{verdict}`",
        "**Date:** 2026-07-16",
        f"**Winner (v2.1):** c05 — cap8 / 0.40% / 16:00 / panel `ED91CD2D` (native $100K, decompound-to-static; no re-scale).",
        f"**Engine:** Run-2; seeds {list(thr.seeds)}; {args.n_sims or thr.sims_per_seed}×3; horizon {thr.horizon}; "
        "dd_protection OFF; inactivity off; `summarize_outcomes`. `ACTIVE_FIRM=FXIFY` fixture untouched.",
        "",
        "## Citations",
        "- v2.2 (1R re-spec + Stage-2 re-run auth): [`docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2.2-1r-native-guard-prereg.md`](../../../docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2.2-1r-native-guard-prereg.md)",
        "- v2.1 winner: [`docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2.1-tiebreak-prereg.md`](../../../docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2.1-tiebreak-prereg.md)",
        "- Frozen gate: [`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`](../../../docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md)",
        "- Panel construction: [`HANDOFF.md`](HANDOFF.md) §1 (native, no re-scale)",
        "",
        "## H-SOLO surface (both required)",
        _tier_line("Tradeify_Select_100K"),
        _tier_line("MFFU_Rapid_100K"),
        "",
        "## Panel",
        f"- n_trades {meta['n_trades']} · span {meta['span']} · overnight {meta['overnight_holds']} · "
        f"envelope {envelope} · net_static ${meta['net_static']:,.0f} · 1R(median) ${r_pin['median_r_dollars']:,.0f} "
        f"(full-stops={r_pin['full_stop_attempt']['n_full_stops']}; 1R diagnostic-only per v2.2 §2.7′)",
        "",
        "## Prior-look (best-of-K)",
        "v1 Stage-1 FALSIFIED (N≥80 unreachable) → v2 realign 12/12 clear (a)–(e), AMBIGUOUS (c05≡c06) "
        "→ v2.1 tie-break → c05 → Stage-2 `NEEDS_CONTEXT` (full-stop 1R FALLBACK; `1ababcf`) → v2.2 "
        "native-path 1R re-spec (option c; guard-drop cannot bias MC — 1R not a scoring input). "
        "All 12 Stage-1 cells + degeneracies disclosed in v2/v2.1 §7; s2/gd in v2.2 §7.",
        "",
        "```json",
        json.dumps({"verdict": verdict, "hsolo_part_a": part_a,
                    "tiers": {k: {kk: tiers[k].get(kk) for kk in ("clears_part_a", "clears_funded", "gated_on", "run2")}
                              for k in HSOLO_FIRMS if k in tiers},
                    "r_pin": r_pin, "panel_meta": meta}, indent=2),
        "```",
        "",
    ]
    (args.out_dir / "RESULTS.md").write_text("\n".join(results) + "\n", encoding="utf-8")
    print(f"[aegis-solo] DONE verdict={verdict} part_a={part_a}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
