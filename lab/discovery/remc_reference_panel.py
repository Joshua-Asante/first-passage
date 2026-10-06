"""Four-firm re-MC §8 step 2(e): calibration-reference panel reassembly.

Card: ``docs/briefs/handoffs/2026-10-06-four-firm-remc-reference-reassembly-card.md``.

Reproduces the archived ``tradeify_futures3_remc_2026-07-11`` panel exactly (archive
``first-passage-archive`` ``283d1def^``, ``run_tradeify_futures3_remc.py``
``build_scaled_panel``) and adds the paired ``intraday_low`` channel the four-firm
prereg I-20 requires ("Accept, intraday"):

* Each export is decompounded to a static $200K account: ``roe = net / equity_before``.
* Each leg is scaled to its locked risk via ``pin_r_basis(full_stop_mean)``.
* Daily P&L is summed by exit date and reindexed to every business day.
* Each trade's ``|Adverse excursion USD|`` is decompounded and scaled exactly like
  its P&L. The day's low is the conservative coincident sum over all legs. There is
  no cost subtraction; the exports are cost-netted as archived.

This module builds a panel only. It never runs a tier, an MC or a score (prereg §R).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Mapping, Sequence

import numpy as np
import pandas as pd

_REPO_ROOT = Path(__file__).resolve().parents[2]
_RECONCILE = _REPO_ROOT / ".claude" / "skills" / "trade-csv-reconcile" / "scripts"
for _p in (_REPO_ROOT / "core", _RECONCILE, _REPO_ROOT / "lab"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from historical_challenge import (  # noqa: E402
    HISTORICAL_CHALLENGE_BALANCE,
    HISTORICAL_CHALLENGE_BASE_RISK,
)
from reconcile import load_csv, pin_r_basis  # noqa: E402
from discovery.remc_series_builder import (  # noqa: E402
    assert_out_dir_allowed,
    sha256_file,
    verify_sha256,
)

ACCOUNT = float(HISTORICAL_CHALLENGE_BALANCE)
STRATS: tuple[str, ...] = ("striker", "striker_nas100", "aegis")  # archived attribution order
R_BASIS = "full_stop_mean"
#: Archived per-leg scales (archive RESULTS.md :34-38); reproduction must match within SCALE_TOL.
ARCHIVED_SCALES: dict[str, float] = {"striker": 0.5521, "striker_nas100": 0.1254, "aegis": 1.0299}
SCALE_TOL = 1e-4
ARCHIVED_WINDOW = ("2020-01-06", "2026-07-01")
ARCHIVED_N_BDAYS = 1693
ADVERSE = "Adverse excursion USD"


class ReproductionError(ValueError):
    """The rebuilt panel does not reproduce the archived construction."""


def detect_initial(exits: pd.DataFrame) -> float:
    """Archived rule: initial capital implied by the last cumulative P&L and its percent."""
    last = exits.iloc[-1]
    cum = float(last["Cumulative P&L USD"])
    pct = float(last["Cumulative P&L %"])
    if abs(pct) < 1e-9:
        return ACCOUNT
    return float(round((cum / (pct / 100.0)) / 1000) * 1000)


def pair_trades(df: pd.DataFrame) -> pd.DataFrame:
    """Archived pairing, plus each trade's adverse excursion (absolute, from its Exit rows)."""
    if ADVERSE not in df.columns:
        raise ValueError(f"export has no {ADVERSE!r} column; the intraday channel cannot be built")
    entries = df[df["Type"].astype(str).str.startswith("Entry")]
    exits = df[df["Type"].astype(str).str.startswith("Exit")]
    rows = []
    for tnum in sorted(df["Trade #"].dropna().unique()):
        e = entries[entries["Trade #"] == tnum]
        x = exits[exits["Trade #"] == tnum]
        if e.empty or x.empty:
            continue
        adverse = pd.to_numeric(x[ADVERSE], errors="coerce").abs()
        if adverse.isna().any():
            raise ValueError(f"trade {int(tnum)}: non-numeric {ADVERSE}")
        rows.append({
            "trade_no": int(tnum),
            "entry_dt": e["dt"].min(),
            "exit_dt": x["dt"].max(),
            "net_pnl": float(x["Net P&L USD"].sum()),
            "cum_after": float(x.sort_values("dt").iloc[-1]["Cumulative P&L USD"]),
            "adverse": float(adverse.max()),
        })
    return pd.DataFrame(rows).sort_values("exit_dt").reset_index(drop=True)


def reconstruct_static(trades: pd.DataFrame, initial: float) -> pd.DataFrame:
    """Archived decompound; the adverse excursion uses the same equity_before."""
    t = trades.copy()
    cum_before = t["cum_after"].shift(1).fillna(0.0)
    t["equity_before"] = initial + cum_before
    t["roe"] = t["net_pnl"] / t["equity_before"]
    t["pnl_static"] = t["roe"] * ACCOUNT
    t["adverse_static"] = t["adverse"] / t["equity_before"] * ACCOUNT
    return t


def build_reference_panel(frames: Mapping[str, pd.DataFrame]) -> tuple[pd.DataFrame, dict]:
    """Business-day panel (one column per leg, plus ``intraday_low``) and its meta."""
    missing = [s for s in STRATS if s not in frames]
    if missing:
        raise ValueError(f"missing required reference legs: {missing}")
    meta: dict = {"legs": {}}
    pnl_series, low_series = [], []
    for strat in STRATS:
        df = frames[strat]
        trades = pair_trades(df)
        exits = df[df["Type"].astype(str).str.startswith("Exit")].sort_values("dt")
        initial = detect_initial(exits)
        t = reconstruct_static(trades, initial)
        method, r_dollars, r_n, warn = pin_r_basis(pd.Series(t["pnl_static"]), R_BASIS, ACCOUNT)
        target_1r = HISTORICAL_CHALLENGE_BASE_RISK[strat] * ACCOUNT
        scale = (target_1r / r_dollars) if r_dollars > 0 else 1.0
        t["pnl_scaled"] = t["pnl_static"] * scale
        t["adverse_scaled"] = t["adverse_static"] * scale
        dated = t.assign(exit_date=t["exit_dt"].dt.normalize())
        daily = dated.groupby("exit_date")["pnl_scaled"].sum()
        daily.name = strat
        pnl_series.append(daily)
        low = -dated.groupby("exit_date")["adverse_scaled"].sum()
        low.name = strat
        low_series.append(low)
        meta["legs"][strat] = {
            "export_initial": initial, "n_trades": len(t), "1r_method": method,
            "1r_dollars": r_dollars, "1r_n": r_n, "1r_warn": bool(warn),
            "scale": scale, "target_1r": target_1r,
            "net_scaled": float(t["pnl_scaled"].sum()),
        }
    panel = pd.concat(pnl_series, axis=1, sort=True).fillna(0.0)[list(STRATS)]
    lows = pd.concat(low_series, axis=1, sort=True).fillna(0.0)
    bdays = pd.bdate_range(panel.index.min(), panel.index.max())
    panel = panel.reindex(bdays).fillna(0.0)
    panel["intraday_low"] = lows.reindex(bdays).fillna(0.0).sum(axis=1) + 0.0
    if not np.isfinite(panel.to_numpy()).all() or (panel["intraday_low"] > 0).any():
        raise ValueError("panel must be finite with intraday_low <= 0")
    meta["window"] = [str(panel.index.min().date()), str(panel.index.max().date())]
    meta["n_bdays"] = len(panel)
    meta["book_net"] = float(panel[list(STRATS)].sum().sum())
    return panel, meta


def check_reproduction(meta: dict) -> None:
    """Raise unless scales and window reproduce the archived panel (card §0.5 item 1, §4)."""
    for strat, archived in ARCHIVED_SCALES.items():
        got = meta["legs"][strat]["scale"]
        if abs(got - archived) > SCALE_TOL:
            raise ReproductionError(f"{strat} scale {got:.6f} != archived {archived} (tol {SCALE_TOL})")
    if tuple(meta["window"]) != ARCHIVED_WINDOW or meta["n_bdays"] != ARCHIVED_N_BDAYS:
        raise ReproductionError(
            f"window {meta['window']} / {meta['n_bdays']} bdays != archived "
            f"{list(ARCHIVED_WINDOW)} / {ARCHIVED_N_BDAYS}")


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Reassemble the four-firm re-MC calibration-reference panel.")
    ap.add_argument("--input", action="append", required=True, metavar="LEG=PATH@SHA256")
    ap.add_argument("--out", required=True, metavar="DIR")
    args = ap.parse_args(list(argv) if argv is not None else None)
    out = Path(args.out)
    assert_out_dir_allowed(out)
    frames, pins = {}, {}
    for token in args.input:
        leg, _, rest = token.partition("=")
        path_text, _, sha = rest.rpartition("@")
        if leg not in STRATS or not path_text or len(sha) != 64:
            raise ValueError(f"--input must be LEG=PATH@SHA256 with LEG in {STRATS}, got {token!r}")
        verify_sha256(path_text, sha)
        frames[leg] = load_csv(path_text)
        pins[leg] = {"file": Path(path_text).name, "sha256": sha.lower()}
    panel, meta = build_reference_panel(frames)
    check_reproduction(meta)
    out.mkdir(parents=True, exist_ok=True)
    target = out / "reference_panel.csv"
    panel.to_csv(target, index_label="date", float_format="%.10g", lineterminator="\n")
    meta.update({"inputs": pins, "panel_file": target.name, "panel_sha256": sha256_file(target)})
    (out / "manifest.json").write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"[remc-reference-panel] {meta['window'][0]}..{meta['window'][1]} ({meta['n_bdays']} bdays) "
          f"scales {[round(meta['legs'][s]['scale'], 4) for s in STRATS]} panel_sha256={meta['panel_sha256']}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
