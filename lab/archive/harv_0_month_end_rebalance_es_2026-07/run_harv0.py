"""HARV-2026-001 battery: H1 + bundled controls + micro OOS + deployability.

Frozen operationalization — brief §4. Do not retune thresholds/windows.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from build_panel import (
    R_SPREAD_THRESHOLD_LOG,
    build_monthly_panel,
    load_symbol_frame,
)
from cost_hurdle import report_hurdles
from step0_checks import run_step0

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
N_PERM = 10_000
DEFAULT_SEED = 20260711

# Frozen §6 trade-rate clause (not a tuning license).
TRADE_RATE_LO = 0.40
TRADE_RATE_HI = 0.90


@dataclass
class EffectResult:
    name: str
    n_qual: int
    mean_signed: float
    sigma: float
    ci95_lo: float
    ci95_hi: float
    perm_p: float
    trade_rate: float


def perm_test_signed(
    window: np.ndarray,
    signal: np.ndarray,
    observed: float,
    n_perm: int = N_PERM,
    rng: np.random.Generator | None = None,
) -> float:
    """Label-permutation: shuffle signal labels across months; P(effect ≥ observed).

    Recomputes mean(signal * window) on months with |signal| > 0 after each shuffle.
    Does NOT shuffle returns within months (brief §7).
    """
    if rng is None:
        rng = np.random.default_rng(DEFAULT_SEED)
    if not np.isfinite(observed) or len(window) == 0:
        return 1.0
    sig = np.asarray(signal, dtype=float).copy()
    win = np.asarray(window, dtype=float)
    count = 0
    for _ in range(n_perm):
        shuf = rng.permutation(sig)
        mask = shuf != 0
        if not np.any(mask):
            continue
        eff = float(np.nanmean(shuf[mask] * win[mask]))
        if not np.isfinite(eff):
            continue
        if eff >= observed:
            count += 1
    return count / n_perm


def effect_on(
    panel: pd.DataFrame,
    window_col: str,
    signed_col: str,
    name: str,
    *,
    n_perm: int = N_PERM,
    rng: np.random.Generator | None = None,
) -> EffectResult:
    q = panel.loc[panel["qualifying"]].copy()
    signed = q[signed_col].to_numpy(dtype=float)
    mean = float(np.nanmean(signed)) if len(signed) else float("nan")
    n_finite = int(np.isfinite(signed).sum())
    sigma = (
        float(np.nanstd(signed, ddof=1)) if n_finite > 1 else float("nan")
    )
    se = sigma / np.sqrt(n_finite) if n_finite else float("nan")
    p = perm_test_signed(
        panel[window_col].to_numpy(dtype=float),
        panel["signal"].to_numpy(dtype=float),
        mean,
        n_perm=n_perm,
        rng=rng,
    )
    return EffectResult(
        name=name,
        n_qual=int(len(q)),
        mean_signed=mean,
        sigma=sigma,
        ci95_lo=mean - 1.96 * se if np.isfinite(se) else float("nan"),
        ci95_hi=mean + 1.96 * se if np.isfinite(se) else float("nan"),
        perm_p=p,
        trade_rate=float(len(q) / len(panel)) if len(panel) else float("nan"),
    )


def tercile_covariance(panel: pd.DataFrame) -> dict:
    """P-covariance: |effect| top |R_spread| tercile > bottom tercile."""
    q = panel.loc[panel["qualifying"]].copy()
    if len(q) < 3:
        return {"low": float("nan"), "mid": float("nan"), "high": float("nan"), "pass": False}
    q = q.copy()
    q["abs_rs"] = q["R_spread"].abs()
    try:
        q["tercile"] = pd.qcut(q["abs_rs"], 3, labels=["low", "mid", "high"], duplicates="drop")
    except ValueError:
        return {"low": float("nan"), "mid": float("nan"), "high": float("nan"), "pass": False}
    means = q.groupby("tercile", observed=True)["signed_window"].mean()
    low = float(means["low"]) if "low" in means.index else float("nan")
    high = float(means["high"]) if "high" in means.index else float("nan")
    return {
        "low": low,
        "mid": float(means["mid"]) if "mid" in means.index else float("nan"),
        "high": high,
        "pass": bool(np.isfinite(high) and np.isfinite(low) and high > low),
    }


def deployability_annotation(
    mean_signed_c: float,
    h1_mean_signed: float,
    two_rt_hurdle_4x_bp: float,
) -> str:
    """DEPLOYABLE-DEFAULT-ENVELOPE: YES iff C same-signed as H1 and ≥ 4× 2-RT hurdle."""
    if not (np.isfinite(mean_signed_c) and np.isfinite(h1_mean_signed)):
        return "NO"
    if h1_mean_signed == 0:
        return "NO"
    same_sign = bool(np.sign(mean_signed_c) == np.sign(h1_mean_signed))
    econ = (mean_signed_c * 10_000.0) >= two_rt_hurdle_4x_bp
    return "YES" if (same_sign and econ) else "NO"


def micro_same_sign_oos(
    parent_mean: float,
    micro_mean: float | None,
) -> bool:
    """P-micro-OOS: native-MES conditional effect same-signed as parent (§4 / §8)."""
    if micro_mean is None or not np.isfinite(parent_mean) or not np.isfinite(micro_mean):
        return False
    if parent_mean == 0 or micro_mean == 0:
        return False
    return bool(np.sign(micro_mean) == np.sign(parent_mean))


def verdict_from(
    h1: EffectResult,
    hurdle_4x_bp: float,
    hurdle_1x_bp: float,
    placebo: EffectResult,
    instrument: EffectResult,
    cov: dict,
    micro_same_sign: bool,
    trade_rate: float,
) -> tuple[str, list[str]]:
    """Return (verdict, triggers). Three-way partition per brief §6.

    FALSIFIED (at primary, no controls needed):
      wrong-signed OR perm_p > 0.20 OR effect < 1× hurdle
    RESOLVED:
      H1 (effect ≥ 4× AND p ≤ 0.05) ∧ P-placebo ∧ P-instrument ∧ P-covariance ∧ P-micro-OOS
      (and trade-rate in [40%, 90%])
    AMBIGUOUS: everything else (enumerated triggers).
    """
    effect_bp = h1.mean_signed * 10_000.0 if np.isfinite(h1.mean_signed) else float("nan")
    notes: list[str] = []

    # --- FALSIFIED-at-primary ---
    wrong_signed = np.isfinite(h1.mean_signed) and h1.mean_signed < 0
    weak_p = h1.perm_p > 0.20
    below_1x = (not np.isfinite(effect_bp)) or effect_bp < hurdle_1x_bp
    if wrong_signed or weak_p or below_1x:
        notes.append(
            f"H1 fail: mean_bp={effect_bp:.2f} p={h1.perm_p:.4f} "
            f"1x_hurdle={hurdle_1x_bp:.2f}"
        )
        return "FALSIFIED", notes

    # Trade-rate clause → AMBIGUOUS (not a threshold-tuning license).
    if not np.isfinite(trade_rate) or trade_rate < TRADE_RATE_LO or trade_rate > TRADE_RATE_HI:
        notes.append(f"trade-rate clause: {trade_rate:.1%}")
        return "AMBIGUOUS", notes

    h1_pass = effect_bp >= hurdle_4x_bp and h1.perm_p <= 0.05
    placebo_ok = (
        placebo.perm_p > 0.10
        and abs(placebo.mean_signed) < 0.5 * abs(h1.mean_signed)
    )
    instrument_ok = instrument.perm_p > 0.10
    cov_ok = bool(cov.get("pass", False))
    micro_ok = micro_same_sign

    if h1_pass and placebo_ok and instrument_ok and cov_ok and micro_ok:
        return "RESOLVED", notes

    # --- AMBIGUOUS partition (enumerated) ---
    if h1_pass:
        if not placebo_ok:
            notes.append("P-placebo fail")
        if not instrument_ok:
            notes.append("P-instrument fail")
        if not cov_ok:
            notes.append("P-covariance fail")
        if not micro_ok:
            notes.append("P-micro-OOS fail")
        return "AMBIGUOUS", notes

    if h1.perm_p <= 0.05 and hurdle_1x_bp <= effect_bp < hurdle_4x_bp:
        notes.append("economically thin: [1×, 4×)")
        return "AMBIGUOUS", notes
    if 0.05 < h1.perm_p <= 0.20 and effect_bp >= hurdle_1x_bp:
        notes.append("p in (0.05, 0.20]")
        return "AMBIGUOUS", notes

    notes.append("unclassified residual → AMBIGUOUS")
    return "AMBIGUOUS", notes


def _mes_signed_windows(
    mes: pd.DataFrame,
    panel: pd.DataFrame,
) -> list[float]:
    """Native-MES signed window returns on micro-era qualifying months."""
    mes_panel = panel.loc[panel["micro_era"] & panel["qualifying"]].copy()
    signed_mes: list[float] = []
    for _, row in mes_panel.iterrows():
        t3, t1 = row["T_3"], row["T_1"]
        if t3 in mes.index and t1 in mes.index and row["signal"] != 0:
            w = float(np.log(mes.loc[t1, "close"] / mes.loc[t3, "close"]))
            signed_mes.append(float(row["signal"]) * w)
    return signed_mes


def main() -> None:
    parents = DATA / "parents_ohlcv_1d.parquet"
    micros = DATA / "micros_ohlcv_1d.parquet"
    if not parents.exists():
        raise SystemExit(f"missing {parents} — run chunked_pull.py first")

    rng = np.random.default_rng(DEFAULT_SEED)

    es = load_symbol_frame(parents, "ES.c.0")
    zn = load_symbol_frame(parents, "ZN.c.0")
    ym = load_symbol_frame(parents, "YM.c.0")
    gc = load_symbol_frame(parents, "GC.c.0")
    panel = build_monthly_panel(es, zn, ym, gc)
    DATA.mkdir(parents=True, exist_ok=True)
    panel.to_parquet(DATA / "monthly_panel.parquet", index=False)
    panel.to_csv(DATA / "monthly_panel.csv", index=False)

    step0 = run_step0(panel)
    print("STEP0", asdict(step0))

    mes_price = float(es["close"].median())
    if micros.exists():
        mes = load_symbol_frame(micros, "MES.c.0")
        if len(mes):
            mes_price = float(mes["close"].median())
    else:
        mes = None

    hurdles = report_hurdles(mes_price)
    h1x = hurdles["single_rt"].hurdle_1x_bp
    h4x = hurdles["single_rt"].hurdle_4x_bp
    h2_4x = hurdles["two_rt"].hurdle_4x_bp
    print("HURDLES", {k: asdict(v) for k, v in hurdles.items()})

    h1 = effect_on(panel, "window", "signed_window", "H1", rng=rng)

    panel_p = panel.copy()
    panel_p["signed_placebo"] = panel_p["signal"] * panel_p["placebo"]
    placebo = effect_on(panel_p, "placebo", "signed_placebo", "P-placebo", rng=rng)

    if "signed_gc_window" in panel.columns:
        gc_eff = effect_on(panel, "gc_window", "signed_gc_window", "P-instrument", rng=rng)
    else:
        # GC (negative control) not evaluable → fail SAFE. perm_p=NaN makes
        # instrument_ok = (NaN > 0.10) = False in verdict_from, so a missing control
        # BLOCKS RESOLVED rather than vacuously "passing" it. (A perm_p of 1.0 here
        # would auto-corroborate an un-run control — the asymmetry the micro-OOS gate
        # already avoids by returning False on absent MES.)
        gc_eff = EffectResult(
            "P-instrument", 0, float("nan"), float("nan"), float("nan"), float("nan"),
            float("nan"), 0.0,
        )

    cov = tercile_covariance(panel)
    unc = float(panel["window"].mean())

    micro_mean: float | None = None
    micro_eff: dict | None = None
    if mes is not None and len(mes):
        signed_mes = _mes_signed_windows(mes, panel)
        if signed_mes:
            micro_mean = float(np.mean(signed_mes))
            micro_eff = {
                "n": len(signed_mes),
                "mean": micro_mean,
                "same_sign": micro_same_sign_oos(h1.mean_signed, micro_mean),
            }

    micro_same = micro_same_sign_oos(h1.mean_signed, micro_mean)

    q = panel.loc[panel["qualifying"]]
    mean_c = float(q["signed_C"].mean()) if len(q) else float("nan")
    annotation = deployability_annotation(mean_c, h1.mean_signed, h2_4x)

    verd, triggers = verdict_from(
        h1, h4x, h1x, placebo, gc_eff, cov, micro_same, h1.trade_rate
    )
    if not step0.ok:
        verd = "AMBIGUOUS"
        triggers = ["Step-0 panel defects"] + triggers

    results = {
        "verdict": verd,
        "triggers": triggers,
        "DEPLOYABLE_DEFAULT_ENVELOPE": annotation,
        "step0": asdict(step0),
        "hurdles": {k: asdict(v) for k, v in hurdles.items()},
        "mes_price_used": mes_price,
        "H1": asdict(h1),
        "H1_effect_bp": h1.mean_signed * 10_000.0 if np.isfinite(h1.mean_signed) else None,
        "placebo": asdict(placebo),
        "instrument_gc": asdict(gc_eff),
        "covariance": cov,
        "unconditional_TOM_window_mean": unc,
        "micro_oos": micro_eff,
        "mean_signed_C": mean_c,
        "mean_signed_C_bp": mean_c * 10_000.0 if np.isfinite(mean_c) else None,
        "n_months": len(panel),
        "n_qualifying": int(panel["qualifying"].sum()),
        "r_spread_threshold_log": float(R_SPREAD_THRESHOLD_LOG),
    }
    (HERE / "results.json").write_text(json.dumps(results, indent=2, default=str))
    print(json.dumps(results, indent=2, default=str))


if __name__ == "__main__":
    main()

