"""Tradeify Select Flex re-MC (2026-07-10) — barrier-geometry test vs Bulenox.

Answers the CC-HANDOFF §4 falsifier: with the locked strategies held FIXED and
only the firm's barrier geometry changed (FXIFY static -> Bulenox pure-trailing
-> Tradeify EOD-trailing-that-LOCKS at start+$100), does the challenge
pass/bust distribution fall within the pre-registered gates (bust < 1%,
p99 DD < 5%) at >=1 account size Bulenox failed?

Design ("shop the barrier, hold the edge fixed"):
  * Same futures-hostable book Bulenox used, on the SAME canonical Pepperstone
    panels (DJ30 v4.5 567e1 force-flatted at 17:00 ET + NAS100 v1 11605 clean),
    optionally + the provisional Aegis->6J v0.3 leg (3-strat book, per the
    parent re-dispatch; flagged PROVISIONAL — non-canonical prototype).
  * 1R pinned to PRE-force-flat values (M-SWAP-1 / Q-SWAP-2): striker $4,229,
    striker_nas100 $3,940 (both = portfolio_mc.PRE_SHOCK_1R), aegis(6J) $1,385.74
    (the 6J panel's own full-stop mean, NOT the USDJPY-CFD $3,293).
  * dd-protection OFF (C2-off): the TV->CrossTrade->NT8->Rithmic rail cannot run
    a portfolio-equity overlay — matches the Bulenox C4/C5 canonical arm.
  * Tradeify vs Bulenox are compared on IDENTICAL fixed-$ trailing arithmetic so
    the ONLY difference is the lock: Tradeify = trailing_locking(offset=$100),
    matched-Bulenox = trailing_locking(offset=unreachable) == pure fixed-$ trail.
    At 100K/150K the two firms' DD ($3,000/$4,500) and target (6%) are IDENTICAL,
    so those tiers isolate PURELY the lock geometry. The shipped %-of-peak Bulenox
    arithmetic (dd_type="trailing") is also reported as a cross-ref to the
    recorded C4 numbers.

ZERO fork of locked core/portfolio_mc — reuses load_trades / build_daily_panel /
build_week_blocks / run_seed and the 2026-07-10 trailing_locking + consistency
engine support. Reuses the Bulenox force_flat_transform for the DJ30 leg.

Run:  python lab/analysis/tradeify_selectflex_remc_2026-07-10/run_tradeify_remc.py
Needs (gitignored vendor data, dropped into the worktree from the main checkout):
  core/data/tv_exports/pepperstone/Striker_DJ30_v4.5_..._567e1.csv
  core/data/tv_exports/pepperstone/Striker_NAS100_v1_..._11605.csv
  core/data/bar_data/US30_M15.csv
  lab/analysis/aegis_6j_transfer_2026-07-05/inputs/Aegis_JPY-Futures_v0.3_PROTOTYPE_..._8e269.csv
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[2]  # repo root
_CORE = _ROOT / "core"
_BULENOX = _ROOT / "lab" / "analysis" / "bulenox_futures_remc_2026-07-01"
for _p in (_CORE, _BULENOX):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from portfolio_mc import (  # noqa: E402
    ALLOCATIONS,
    BASELINE_BALANCE,
    HORIZON_CAP,
    PEPPERSTONE_PANELS,
    SEEDS,
    SIMS_PER_SEED,
    build_daily_panel,
    build_week_blocks,
    load_trades,
    run_seed,
)
from firm_rules import FIRM_RULES  # noqa: E402
from force_flat_transform import bars_utc_to_et, force_flat_csv  # noqa: E402

# ── Inputs ────────────────────────────────────────────────────────────────
DJ30_CSV = PEPPERSTONE_PANELS["striker"]          # canonical 2026-05-24 567e1
NAS100_CSV = PEPPERSTONE_PANELS["striker_nas100"]  # canonical 2026-05-24 11605
US30_BARS = _CORE / "data" / "bar_data" / "US30_M15.csv"
AEGIS_6J_CSV = (_ROOT / "lab" / "analysis" / "aegis_6j_transfer_2026-07-05" / "inputs" /
                "Aegis_JPY-Futures_v0.3_PROTOTYPE_(MJY_6J)_CME_6J1!_2026-07-05_8e269.csv")
_INPUTS = _HERE / "inputs"

# Pinned 1R (USD/1R). striker/striker_nas100 = portfolio_mc.PRE_SHOCK_1R;
# aegis(6J) = the 6J panel's own full-stop mean (provisional lane).
FIXED_1R = {"striker": 4229.0, "striker_nas100": 3940.0, "aegis": 1385.74}

BOOKS = {
    "2-strat (DJ30+NAS100, canonical Bulenox book)": ("striker", "striker_nas100"),
    "3-strat (+ Aegis/6J, PROVISIONAL)": ("striker", "striker_nas100", "aegis"),
}

SIZES = ("25K", "50K", "100K", "150K")
GATE_BUST = 0.01
GATE_P99 = 0.05
NO_PROTECTION_TRIGGER = 10.0  # sentinel: dd-protection OFF
DD_SCALE = 0.40               # inert when trigger never fires
INACT_OFF = HORIZON_CAP + 1   # inactivity disabled (>=1 trade/week token mitigation assumed)

_OUTCOME_KEYS = ("pass", "bust_daily", "bust_static", "bust_trailing",
                 "bust_inactivity", "horizon_cap")


# ── Panel build ───────────────────────────────────────────────────────────

def build_book_panel(strats: tuple[str, ...]) -> pd.DataFrame:
    """$200K-normalized daily panel for `strats` (fixed-1R, force-flat DJ30)."""
    tbs: dict[str, pd.DataFrame] = {}
    if "striker" in strats:
        raw = pd.read_csv(DJ30_CSV, encoding="utf-8-sig")
        bars = bars_utc_to_et(pd.read_csv(US30_BARS))
        ff = force_flat_csv(raw, bars)
        _INPUTS.mkdir(exist_ok=True)
        ff_path = _INPUTS / "dj30_forceflat.csv"
        ff.to_csv(ff_path, index=False)
        tbs["striker"] = load_trades(ff_path, strategy="striker")
    if "striker_nas100" in strats:
        tbs["striker_nas100"] = load_trades(NAS100_CSV, strategy="striker_nas100")
    if "aegis" in strats:
        tbs["aegis"] = load_trades(AEGIS_6J_CSV, strategy="aegis")
    alloc = {s: ALLOCATIONS[s] for s in strats}
    ref = {s: FIXED_1R[s] for s in strats}
    panel, _scale = build_daily_panel(tbs, alloc, fixed_1r_reference=ref)
    # build_daily_panel orders columns by tbs insertion; keep that order for attribution.
    return panel[[s for s in strats if s in panel.columns]]


# ── firm_kwargs builders ──────────────────────────────────────────────────

def _base_kwargs(f: dict) -> dict:
    bal = float(f["starting_balance"])
    return dict(
        starting_equity=bal,
        daily_loss_pct=(None if f["daily_loss_pct"] is None else -f["daily_loss_pct"] / 100),
        profit_target=bal * (1 + f["profit_target_pct"] / 100),
        min_trading_days=f["min_trading_days"],
        inactivity_limit=INACT_OFF,
    )


def tradeify_kwargs(size: str, consistency: float | None = None) -> dict:
    f = FIRM_RULES[f"Tradeify_Select_{size}"]
    kw = _base_kwargs(f)
    kw.update(
        dd_type="trailing_locking",
        trailing_dd_pct=-f["max_dd_pct"] / 100,
        dd_lock_offset_usd=float(f["dd_lock_offset_usd"]),
        consistency_frac=consistency,
    )
    return kw


def bulenox_fixed_dollar_kwargs(size: str) -> dict:
    """Matched baseline: identical fixed-$ trailing arithmetic, lock unreachable."""
    f = FIRM_RULES[f"Bulenox_{size}"]
    kw = _base_kwargs(f)
    kw.update(
        dd_type="trailing_locking",
        trailing_dd_pct=-f["max_dd_pct"] / 100,
        dd_lock_offset_usd=1e12,  # never reached -> pure fixed-$ trailing (no lock)
    )
    return kw


def bulenox_pctpeak_kwargs(size: str) -> dict:
    """Shipped %-of-peak arithmetic — cross-ref to the recorded C4 numbers."""
    f = FIRM_RULES[f"Bulenox_{size}"]
    kw = _base_kwargs(f)
    kw.update(dd_type="trailing", trailing_dd_pct=-f["max_dd_pct"] / 100)
    return kw


# ── Run one config ────────────────────────────────────────────────────────

def run_config(panel_200k: pd.DataFrame, size: str, firm_kwargs: dict,
               strats: tuple[str, ...]) -> dict:
    f_bal = float(FIRM_RULES.get(f"Tradeify_Select_{size}", FIRM_RULES[f"Bulenox_{size}"])["starting_balance"])
    tier_balance = float(firm_kwargs["starting_equity"])
    assert tier_balance == f_bal, (tier_balance, f_bal)
    panel = panel_200k * (tier_balance / BASELINE_BALANCE)
    blocks = build_week_blocks(panel)
    seeds_results = [
        run_seed(seed, SIMS_PER_SEED, blocks, NO_PROTECTION_TRIGGER, DD_SCALE,
                 strats=strats, firm_kwargs=firm_kwargs)
        for seed in SEEDS
    ]
    per = SIMS_PER_SEED
    rates = {k: float(np.mean([r["outcomes"][k] / per for r in seeds_results])) for k in _OUTCOME_KEYS}
    all_dds = [d for r in seeds_results for d in r["max_dds"]]
    all_days = [d for r in seeds_results for d in r["days_to_pass"]]
    bust = rates["bust_daily"] + rates["bust_static"] + rates["bust_trailing"]
    return {
        "pass": rates["pass"],
        "bust": bust,
        "p99_dd": float(np.percentile(all_dds, 99)) if all_dds else float("nan"),
        "median": int(np.median(all_days)) if all_days else -1,
        "n_blocks": len(blocks),
        "n_bdays": len(panel),
    }


def _gate(res: dict) -> str:
    ok_b = res["bust"] < GATE_BUST
    ok_p = res["p99_dd"] < GATE_P99
    return ("PASS" if (ok_b and ok_p) else "FAIL") + f" (bust{'<' if ok_b else '>='}1% p99{'<' if ok_p else '>='}5%)"


# ── Main ──────────────────────────────────────────────────────────────────

def main() -> None:
    lines: list[str] = []

    def emit(s: str = "") -> None:
        print(s)
        lines.append(s)

    emit("=" * 108)
    emit("TRADEIFY SELECT FLEX re-MC (2026-07-10) — barrier-geometry test vs Bulenox")
    emit(f"Sims: {SIMS_PER_SEED:,} x {len(SEEDS)} seeds | dd-protection OFF (C2-off) | "
         f"inactivity DISABLED | horizon {HORIZON_CAP}d")
    emit(f"1R pinned: striker=${FIXED_1R['striker']:,.0f} nas100=${FIXED_1R['striker_nas100']:,.0f} "
         f"aegis(6J)=${FIXED_1R['aegis']:,.2f} | Gates: bust<{GATE_BUST:.0%} AND p99 DD<{GATE_P99:.0%}")
    emit("=" * 108)

    verdict_rows: list[tuple] = []

    for book_label, strats in BOOKS.items():
        panel = build_book_panel(strats)
        emit()
        emit(f"### BOOK: {book_label}   ({len(strats)} legs: {', '.join(strats)})")
        emit(f"    panel: {panel.index.min().date()} -> {panel.index.max().date()}  "
             f"({len(panel)} bdays)")
        emit()
        emit(f"    {'Size':<6} {'Config':<34} {'Pass':>8} {'Bust':>8} {'p99 DD':>8} {'Median':>7}  Gate")
        emit("    " + "-" * 96)
        for size in SIZES:
            configs = [
                ("Tradeify (lock, geometry-only)", tradeify_kwargs(size), strats),
                ("Tradeify (lock, +40% consistency)", tradeify_kwargs(size, consistency=0.40), strats),
                ("Bulenox matched (fixed-$, no lock)", bulenox_fixed_dollar_kwargs(size), strats),
                ("Bulenox shipped (%-of-peak, C4 xref)", bulenox_pctpeak_kwargs(size), strats),
            ]
            for cfg_label, kw, st in configs:
                res = run_config(panel, size, kw, st)
                gate = _gate(res)
                emit(f"    {size:<6} {cfg_label:<34} {res['pass']:>8.2%} {res['bust']:>8.2%} "
                     f"{res['p99_dd']:>8.2%} {res['median']:>7}  {gate}")
                if cfg_label.startswith("Tradeify (lock, geometry-only)"):
                    verdict_rows.append((book_label, size, "T-geom", res))
                if cfg_label.startswith("Tradeify (lock, +40%"):
                    verdict_rows.append((book_label, size, "T-consist", res))
                if cfg_label.startswith("Bulenox matched"):
                    verdict_rows.append((book_label, size, "B-matched", res))
            emit()

    # ── §4 verdict ──
    emit("=" * 108)
    emit("§4 VERDICT — does the lock geometry move >=1 size within the gates that Bulenox failed?")
    emit("=" * 108)
    by = {}
    for book, size, tag, res in verdict_rows:
        by[(book, size, tag)] = res
    for book_label, strats in BOOKS.items():
        emit(f"\n{book_label}:")
        for size in SIZES:
            tg = by.get((book_label, size, "T-geom"))
            bm = by.get((book_label, size, "B-matched"))
            if not tg or not bm:
                continue
            t_pass = tg["bust"] < GATE_BUST and tg["p99_dd"] < GATE_P99
            b_pass = bm["bust"] < GATE_BUST and bm["p99_dd"] < GATE_P99
            flip = "  <== LOCK FIXES THE GATE" if (t_pass and not b_pass) else ""
            emit(f"  {size:<5} Tradeify bust {tg['bust']:.2%}/p99 {tg['p99_dd']:.2%} -> {'PASS' if t_pass else 'FAIL'}"
                 f"   |  Bulenox-matched bust {bm['bust']:.2%}/p99 {bm['p99_dd']:.2%} -> {'PASS' if b_pass else 'FAIL'}{flip}")

    out = _HERE / "RESULTS_tradeify_remc_2026-07-10.md"
    out.write_text("```\n" + "\n".join(lines) + "\n```\n", encoding="utf-8")
    print(f"\n[written] {out}")


if __name__ == "__main__":
    main()
