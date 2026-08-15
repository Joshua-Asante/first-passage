"""Class-S candidate #2 G0–G8 scoring (3-leg MYM+MNQ+6J, Aegis ae744 @ 0.75%).

Implements candidate #2 §8 against the frozen survivor gate.
Does NOT re-run §3 calibration (full-Aegis 1.50% already 0/4 on candidate #1 RESULTS).

Does NOT switch ``ACTIVE_FIRM``. FXIFY is retired as a live firm; the config key
``ACTIVE_FIRM="FXIFY"`` is the historical MC-anchor fixture only and must stay put
for anchor byte-repro. Threads tiers via ``firm_kwargs``. Reads headline bust via
``summarize_outcomes`` only (never ``compute_default_config()['bust_rate']``).

Panel construction = futures3/bustcut of record:
  decompound static @ $200K (roe) → pin_r_basis(full_stop_mean) → scale to per-leg risk%.
§8.3 binding 1R guard: FALLBACK method or n<5 hard-fails (NEEDS_CONTEXT).

Exit codes:
  0 — scoring completed; verdict written
  2 — NEEDS_CONTEXT (missing/mismatched panel bytes or 1R guard)
  3 — Phase-0 signature / ACTIVE_FIRM / pre-reg intactness failure
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
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

from firm_rules import ACTIVE_FIRM, BASELINE_BALANCE, FIRM_RULES  # noqa: E402
from portfolio_mc import ALLOCATIONS  # noqa: E402
from reconcile import load_csv, pin_r_basis  # noqa: E402
from discovery.prop_survivor_scoring import (  # noqa: E402
    load_scoring_thresholds,
    score_candidate,
)

CANDIDATE_PREREG = (
    _ROOT
    / "docs"
    / "briefs"
    / "pre-registration"
    / "2026-07-15-existing-strategy-book-candidate-2-prereg.md"
)
GATE_PREREG = (
    _ROOT
    / "docs"
    / "briefs"
    / "pre-registration"
    / "2026-07-13-prop-survivor-scoring-prereg.md"
)
CME_DIR = _ROOT / "core" / "data" / "tv_exports" / "cme"
ACCOUNT = float(BASELINE_BALANCE)  # $200K decompound basis
R_BASIS = "full_stop_mean"
MIN_FULL_STOP_N = 5

# Byte-pinned panels (candidate §2 / §3) — filenames + expected sha256 from SHA256SUMS.
PANEL_FILES = {
    "striker": (
        "Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-11_15d8b.csv",
        "9acfa29726a9530d2a3de5fc2290cc67672441fac2c805defd524677cce01b9e",
    ),
    "striker_nas100": (
        "Striker_NAS100_v1_CME_MINI_MNQ1!_2026-07-11_beabf.csv",
        "8884e6dd56c786e1e59a8ab0b962a70be82f34e06af26a9582554c9f8ddc6419",
    ),
    "aegis": (
        "Aegis_JPY-Futures_v0.3_BEPAD-TEST_(MJY_6J)_CME_6J1!_2026-07-11_ae744.csv",
        "e82a2c25a94c42b12888f2f8b70daa56f579c6fe02a633418edcf4b3d148ca38",
    ),
}

# Expected 1R pins (candidate §2) — asserted after pin_r_basis.
EXPECTED_1R = {
    "striker": {"dollars": 2535.61, "n": 8, "scale": 0.5521},
    "striker_nas100": {"dollars": 5899.32, "n": 19, "scale": 0.1254},
    "aegis": {"dollars": 2912.96, "n": 11, "scale": 0.5149},
}

C2_STRATS = ("striker", "striker_nas100", "aegis")
C2_ALLOCS = {"striker": 0.0070, "striker_nas100": 0.0037, "aegis": 0.0075}

SIGNATURE_RE = re.compile(r"SIGNED / FROZEN:\s*2026-07-15\s*/\s*JA")
ONE_R_TOL_USD = 0.50  # absolute $ tolerance on pinned 1R
SCALE_TOL = 0.0005


class NeedsContext(RuntimeError):
    """Missing / mismatched inputs that the operator must supply — do not improvise."""


class Phase0Error(RuntimeError):
    """Pre-reg / governance intactness failure."""


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def phase0_verify() -> None:
    """Signature-before-run + ACTIVE_FIRM + gate ceilings byte-stable."""
    text = CANDIDATE_PREREG.read_text(encoding="utf-8")
    if not SIGNATURE_RE.search(text):
        raise Phase0Error(
            f"candidate §9 signature not in expected signed form: {CANDIDATE_PREREG}"
        )
    if "DOES contain an Aegis leg" not in text:
        raise Phase0Error("candidate missing explicit Aegis-inclusive declaration (ADR §5 / §10.4)")
    # FXIFY is retired as a live firm; this asserts the historical fixture key only.
    if ACTIVE_FIRM != "FXIFY":
        raise Phase0Error(
            f"ACTIVE_FIRM={ACTIVE_FIRM!r} — must remain the FXIFY historical "
            f"MC-anchor fixture (venue retired; do not treat as live firm)"
        )
    thr = load_scoring_thresholds(GATE_PREREG)
    if thr.eval_bust_ceiling != 0.03 or thr.pass_floor != 0.5:
        raise Phase0Error(f"gate ceilings drifted: {thr}")
    expected_tiers = (
        "Bulenox_100K",
        "Tradeify_Select_100K",
        "MFFU_Rapid_100K",
        "BluSky_Premium_100K",
    )
    if thr.tier_keys != expected_tiers:
        raise Phase0Error(f"frozen tiers drifted: {thr.tier_keys}")


def resolve_panel_path(leg: str) -> Path:
    name, expect_sha = PANEL_FILES[leg]
    path = CME_DIR / name
    if not path.is_file():
        raise NeedsContext(
            f"missing panel bytes for {leg}: {path}\n"
            f"  (gitignored vendor CSV; drop into core/data/tv_exports/cme/ with "
            f"sha256={expect_sha} then re-run)"
        )
    got = _sha256(path)
    if got != expect_sha:
        raise NeedsContext(
            f"panel sha256 mismatch for {leg}:\n"
            f"  path={path}\n  expected={expect_sha}\n  got={got}"
        )
    return path


def detect_initial(exits: pd.DataFrame) -> float:
    last = exits.iloc[-1]
    cum = float(last["Cumulative P&L USD"])
    pct = float(last["Cumulative P&L %"])
    if abs(pct) < 1e-9:
        return ACCOUNT
    return float(round((cum / (pct / 100.0)) / 1000) * 1000)


def pair_trades(df: pd.DataFrame) -> pd.DataFrame:
    entries = df[df["Type"].astype(str).str.startswith("Entry")].copy()
    exits = df[df["Type"].astype(str).str.startswith("Exit")].copy()
    rows = []
    for tnum in sorted(df["Trade #"].dropna().unique()):
        e = entries[entries["Trade #"] == tnum]
        x = exits[exits["Trade #"] == tnum]
        if e.empty or x.empty:
            continue
        rows.append(
            {
                "trade_no": int(tnum),
                "entry_dt": e["dt"].min(),
                "exit_dt": x["dt"].max(),
                "net_pnl": float(x["Net P&L USD"].sum()),
                "cum_after": float(x.sort_values("dt").iloc[-1]["Cumulative P&L USD"]),
            }
        )
    return pd.DataFrame(rows).sort_values("exit_dt").reset_index(drop=True)


def reconstruct_static(trades: pd.DataFrame, initial: float) -> pd.DataFrame:
    t = trades.copy()
    cum_before = t["cum_after"].shift(1).fillna(0.0)
    t["equity_before"] = initial + cum_before
    t["roe"] = t["net_pnl"] / t["equity_before"]
    t["pnl_static"] = t["roe"] * ACCOUNT
    return t


def _assert_1r_guard(
    leg: str,
    method: str,
    r_dollars: float,
    r_n: int,
    warn: bool,
    *,
    expect: dict | None,
) -> None:
    """§8.3 binding adapter guard (PANEL_OF_RECORD §3 adopted)."""
    # pin_r_basis labels zero-full-stop fallback as "...(FALLBACK — zero full stops)"
    if "FALLBACK" in method or r_n == 0:
        raise NeedsContext(
            f"1R pin fallback blocked for candidate scoring: leg={leg} "
            f"method={method!r} n={r_n} warn={warn}. Panel has zero full-stop "
            f"cohort after decompound — fix export sizing or pin 1R explicitly."
        )
    if r_n < MIN_FULL_STOP_N:
        raise NeedsContext(
            f"1R thin-cohort blocked for candidate scoring: leg={leg} n={r_n} "
            f"full-stops (require n>={MIN_FULL_STOP_N})."
        )
    if expect is not None:
        if abs(r_dollars - float(expect["dollars"])) > ONE_R_TOL_USD:
            raise NeedsContext(
                f"1R dollar pin drifted for {leg}: got {r_dollars:.2f} "
                f"expected {expect['dollars']:.2f} (±{ONE_R_TOL_USD})"
            )
        if int(r_n) != int(expect["n"]):
            raise NeedsContext(
                f"1R cohort n drifted for {leg}: got {r_n} expected {expect['n']}"
            )


def build_scaled_panel(
    strats: Sequence[str],
    allocations: dict[str, float],
    *,
    expect_1r: dict[str, dict] | None = None,
) -> tuple[pd.DataFrame, dict, dict[str, pd.Series]]:
    """$200K-static decompounded, risk%-scaled business-day panel + per-leg trade PnLs."""
    meta: dict = {"legs": {}}
    series = []
    trade_pnls: dict[str, pd.Series] = {}
    for strat in strats:
        path = resolve_panel_path(strat)
        df = load_csv(path)
        trades = pair_trades(df)
        exits = df[df["Type"].astype(str).str.startswith("Exit")].sort_values("dt")
        initial = detect_initial(exits)
        t = reconstruct_static(trades, initial)

        method, r_dollars, r_n, warn = pin_r_basis(
            pd.Series(t["pnl_static"]), R_BASIS, ACCOUNT
        )
        expect = None if expect_1r is None else expect_1r.get(strat)
        _assert_1r_guard(strat, method, r_dollars, r_n, warn, expect=expect)

        target_1r = allocations[strat] * ACCOUNT
        scale = (target_1r / r_dollars) if r_dollars > 0 else 1.0
        if expect is not None and "scale" in expect:
            if abs(scale - float(expect["scale"])) > SCALE_TOL:
                raise NeedsContext(
                    f"scale drifted for {strat}: got {scale:.6f} "
                    f"expected {expect['scale']:.6f}"
                )
        t["pnl_scaled"] = t["pnl_static"] * scale
        trade_pnls[strat] = t["pnl_scaled"].astype(float)

        daily = (
            t.assign(exit_date=t["exit_dt"].dt.normalize())
            .groupby("exit_date")["pnl_scaled"]
            .sum()
        )
        daily.name = strat
        series.append(daily)

        meta["legs"][strat] = {
            "file": path.name,
            "sha256": PANEL_FILES[strat][1],
            "export_initial": initial,
            "n_trades": len(t),
            "span": f"{t['exit_dt'].min().date()}->{t['exit_dt'].max().date()}",
            "1r_method": method,
            "1r_dollars": float(r_dollars),
            "1r_n": int(r_n),
            "1r_warn": bool(warn),
            "scale": float(scale),
            "risk_pct": allocations[strat],
            "target_1r": float(target_1r),
            "net_scaled": float(t["pnl_scaled"].sum()),
            "n_overnight_holds": int(
                (
                    t["entry_dt"].dt.normalize() != t["exit_dt"].dt.normalize()
                ).sum()
                if "entry_dt" in t.columns
                else -1
            ),
        }

    panel = pd.concat(series, axis=1, sort=True).fillna(0.0)
    panel = panel[list(strats)]
    bdays = pd.bdate_range(panel.index.min(), panel.index.max())
    panel = panel.reindex(bdays).fillna(0.0)
    meta["panel_span"] = f"{panel.index.min().date()}->{panel.index.max().date()}"
    meta["n_bdays"] = int(len(panel))
    meta["book_net_200k"] = float(panel.sum().sum())
    return panel, meta, trade_pnls


def scale_panel_to_tier(panel_200k: pd.DataFrame, tier_key: str) -> pd.DataFrame:
    bal = float(FIRM_RULES[tier_key]["starting_balance"])
    return panel_200k * (bal / ACCOUNT)


def book_daily_at_100k(panel_200k: pd.DataFrame) -> np.ndarray:
    """Summed book daily PnL at the $100K common band (all frozen tiers)."""
    # All four frozen $100K tiers share starting_balance == 100_000.
    return (panel_200k.sum(axis=1) * (100_000.0 / ACCOUNT)).to_numpy(dtype=float)


def per_leg_cost_law(
    trade_pnls: dict[str, pd.Series],
    firm_key: str,
    *,
    cost_law_multiple: float,
) -> dict:
    """G2 — per-leg gross-edge ≥ N× RT cost at that leg's R_deploy (candidate §2)."""
    cps = FIRM_RULES[firm_key].get("cost_per_side_usd")
    if cps is None:
        raise NeedsContext(f"{firm_key} missing cost_per_side_usd")
    rt = 2.0 * float(cps)
    per_leg = {}
    all_ok = True
    for leg, series in trade_pnls.items():
        r_deploy = int(len(series))
        gross = float(series[series > 0].sum())
        hurdle = cost_law_multiple * rt * r_deploy
        ok = gross >= hurdle
        all_ok = all_ok and ok
        per_leg[leg] = {
            "r_deploy": r_deploy,
            "gross_edge_usd": gross,
            "rt_cost_usd": rt,
            "hurdle_usd": hurdle,
            "passed": ok,
        }
    return {
        "firm_key": firm_key,
        "cost_per_side_usd": float(cps),
        "all_legs_passed": all_ok,
        "legs": per_leg,
    }


def overnight_hold_pct(meta: dict) -> float:
    holds = 0
    trades = 0
    for leg in meta["legs"].values():
        n = int(leg["n_trades"])
        h = int(leg["n_overnight_holds"])
        trades += n
        holds += max(h, 0)
    if trades == 0:
        return float("nan")
    return 100.0 * holds / trades


def assign_verdict(report: dict) -> str:
    """Candidate #2 §6 disposition (mechanical). Program falsifier already discharged by #1."""
    tiers = report["tiers"]
    clearers = [k for k, s in tiers.items() if s["clears_part_a"]]
    locking = {
        k
        for k in clearers
        if FIRM_RULES[k].get("dd_type") == "trailing_locking"
    }
    if len(clearers) >= 2 and locking:
        return "RESOLVED"
    if not clearers:
        return "FALSIFIED — all-four-fail"
    return (
        "FALSIFIED — partial (NOT-cleared) "
        f"(clearers={clearers}; trailing_locking={sorted(locking)})"
    )


def score_book(
    *,
    label: str,
    panel_200k: pd.DataFrame,
    trade_pnls: dict[str, pd.Series],
    meta: dict,
    envelope: str,
    n_sims: int | None = None,
) -> dict:
    thr = load_scoring_thresholds(GATE_PREREG)
    daily_100k = book_daily_at_100k(panel_200k)
    # Full-res trades = concatenated scaled trade PnLs (G1 R_deploy = fill count).
    trades = np.concatenate([s.to_numpy(dtype=float) for s in trade_pnls.values()])
    g2 = {
        fk: per_leg_cost_law(trade_pnls, fk, cost_law_multiple=thr.cost_law_multiple)
        for fk in thr.tier_keys
    }
    # If any frozen tier fails per-leg cost law, still run MC but annotate (harness
    # kills per-tier via its own G2; we override gross_edge so harness G2 sees book).
    report = score_candidate(
        strategy_label=label,
        candidate_daily_pnl=daily_100k,
        full_res_trades=list(trades),
        envelope_verdict=envelope,  # type: ignore[arg-type]
        thresholds=thr,
        n_sims=n_sims,
        gross_edge_usd=float(trades[trades > 0].sum()),
    )
    out = report.to_dict()
    out["panel_meta"] = meta
    out["g2_per_leg"] = g2
    out["overnight_hold_pct"] = overnight_hold_pct(meta)
    out["candidate_prereg"] = str(CANDIDATE_PREREG.relative_to(_ROOT))
    out["gate_prereg"] = str(GATE_PREREG.relative_to(_ROOT))
    return out


def write_results(
    path: Path,
    *,
    status: str,
    detail: str,
    c2: dict | None = None,
) -> None:
    lines = [
        "# Class-S candidate #2 — G0–G8 scoring RESULTS",
        "",
        f"**Status:** `{status}`",
        "**Date:** 2026-07-16",
        "**Engine posture:** 10k×3 seeds 42/123/2026; horizon 1500; inactivity off;",
        "`dd_protection` OFF; `firm_kwargs`; `summarize_outcomes`; Run-2 gated.",
        'FXIFY retired; `ACTIVE_FIRM="FXIFY"` historical fixture untouched.',
        "",
        "## Citations (gate §10 hook 6 / candidate §10 hook 6)",
        "",
        "- Candidate pre-reg: [`docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-2-prereg.md`](../../../docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-2-prereg.md)",
        "- Frozen gate: [`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`](../../../docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md)",
        "- §3 calibration (NOT re-run): candidate #1 RESULTS — full-Aegis 1.50% 0/4 clear",
        "",
        "## Detail",
        "",
        detail,
        "",
    ]
    if c2 is not None:
        lines.extend(
            [
                "## Candidate #2 (S1 3-leg MYM+MNQ+6J, Aegis @ 0.75%)",
                "",
                "```json",
                json.dumps(
                    {
                        "discharges_falsifier": c2.get("discharges_falsifier"),
                        "halted_at": c2.get("halted_at"),
                        "verdict": c2.get("verdict"),
                        "g1": c2.get("g1"),
                        "tiers": {
                            k: {
                                "clears_part_a": v["clears_part_a"],
                                "clears_funded": v["clears_funded"],
                                "gated_on": v["gated_on"],
                                "f2_label": v["f2_label"],
                                "run2": v.get("run2"),
                            }
                            for k, v in c2.get("tiers", {}).items()
                        },
                        "panel_meta": c2.get("panel_meta"),
                        "overnight_hold_pct": c2.get("overnight_hold_pct"),
                        "envelope_final": c2.get("envelope_final"),
                        "g2_per_leg": c2.get("g2_per_leg"),
                    },
                    indent=2,
                ),
                "```",
                "",
            ]
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    import argparse

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n-sims", type=int, default=None)
    ap.add_argument("--out-dir", type=Path, default=_HERE)
    args = ap.parse_args(list(argv) if argv is not None else None)
    out_dir: Path = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        phase0_verify()
    except Phase0Error as e:
        write_results(out_dir / "RESULTS.md", status="PHASE0_FAIL", detail=str(e))
        print(f"[class-s-c2] PHASE0_FAIL: {e}", file=sys.stderr)
        return 3

    try:
        for leg in C2_STRATS:
            resolve_panel_path(leg)
        panel_c2, meta_c2, trades_c2 = build_scaled_panel(
            C2_STRATS, C2_ALLOCS, expect_1r=EXPECTED_1R
        )
    except NeedsContext as e:
        write_results(
            out_dir / "RESULTS.md",
            status="NEEDS_CONTEXT",
            detail=f"```\n{e}\n```",
        )
        print(f"[class-s-c2] NEEDS_CONTEXT: {e}", file=sys.stderr)
        return 2

    overnight = overnight_hold_pct(meta_c2)
    provisional_envelope = "YES" if (overnight == 0.0 or overnight != overnight) else "NO"
    print("[class-s-c2] scoring candidate #2 (3-leg Aegis@0.75%) ...", flush=True)
    c2 = score_book(
        label="class-s-c2-s1-mym-mnq-6j-aegis075",
        panel_200k=panel_c2,
        trade_pnls=trades_c2,
        meta=meta_c2,
        envelope=provisional_envelope,
        n_sims=args.n_sims,
    )
    g2_all = all(v["all_legs_passed"] for v in c2["g2_per_leg"].values())
    c2["envelope_final"] = "YES" if (provisional_envelope == "YES" and g2_all) else "NO"
    c2["g1"]["deployable_default_envelope"] = c2["envelope_final"]
    c2["verdict"] = assign_verdict(c2)

    (out_dir / "candidate2_report.json").write_text(
        json.dumps(c2, indent=2) + "\n", encoding="utf-8"
    )
    write_results(
        out_dir / "RESULTS.md",
        status=c2["verdict"],
        detail=(
            f"H-C2 only — program §4 already discharged by candidate #1. "
            f"discharges_falsifier={c2['discharges_falsifier']}; "
            f"overnight_hold_pct={c2['overnight_hold_pct']:.2f}%; "
            f"envelope={c2['envelope_final']}; ACTIVE_FIRM={ACTIVE_FIRM}; "
            f"sims/seed={args.n_sims or load_scoring_thresholds(GATE_PREREG).sims_per_seed}. "
            "§3 full-Aegis 1.50% calibration NOT re-run."
        ),
        c2=c2,
    )
    print(
        f"[class-s-c2] DONE verdict={c2['verdict']} "
        f"discharges={c2['discharges_falsifier']} envelope={c2['envelope_final']}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
