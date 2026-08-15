"""Stage-7 native-micro realism engine — GC→MGC venue gate (DISC-CAMP-0).

Re-evaluates frozen survivor rules on native MGC 1h bars with two independent
predicate clauses (ratio + hurdle). Synthetic-only until operator authorizes pull.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from discovery.cost_mgc import (
    COMMISSION_PER_SIDE_USD,
    MGC_MULTIPLIER,
    MGC_TICK_VALUE,
    SLIPPAGE_TICKS_PER_SIDE,
    MgcCostHurdle,
    hurdle_from_price,
    mgc_rt_cost_usd,
    passes_cost_law,
)
from discovery.motif_rules import FrozenRule, RuleEval, evaluate_rule
from research_utils.repo_root import repo_root

# Pre-registered thin-market thresholds (§0.5(C) — operator-confirm at freeze).
BAR_COVERAGE_MIN = 0.95
MEDIAN_VOLUME_MIN_MULTIPLE = 20  # shakedown = 1 contract → ≥ 20/hr
INTENDED_CONTRACTS_DEFAULT = 1

# Campaign cost gate (pre-reg §5).
CAMPAIGN_MAX_COST_USD = 5.00
OOS_START = "2019-05-06"
OOS_END = "2026-07-01"
RATIO_GC_MULTIPLE = 0.8

NAUTILUS_RUNBOOK = (
    "Nautilus fill-realism is survivor-gated and NOT implemented in this build. "
    "If a candidate passes the bar-level Stage-7 predicate, invoke a follow-on "
    "Nautilus backtest per docs/adr/2026-07-10-databento-research-stack.md "
    "(research-only; no execution rail)."
)


def ratio_clause(net_mgc_expectancy: float, gross_gc_expectancy: float) -> bool:
    """Clause 1: net MGC ≥ 0.8× GC-gross expectancy."""
    return net_mgc_expectancy >= RATIO_GC_MULTIPLE * gross_gc_expectancy


def hurdle_clause(net_mgc_expectancy: float, hurdle: MgcCostHurdle) -> bool:
    """Clause 2: net MGC ≥ 4× MGC round-trip cost hurdle."""
    return passes_cost_law(net_mgc_expectancy, hurdle)


def rt_cost_frac(
    mgc_price: float,
    *,
    extra_slip_ticks_per_side: float = 0.0,
) -> float:
    """Round-trip cost as a fraction of notional at ``mgc_price``."""
    slip = SLIPPAGE_TICKS_PER_SIDE + float(extra_slip_ticks_per_side)
    rt_usd = mgc_rt_cost_usd(
        COMMISSION_PER_SIDE_USD,
        slip,
    )
    notional = mgc_price * MGC_MULTIPLIER
    return rt_usd / notional if notional > 0 else float("inf")


def reconstruct_gross_gc(
    trade_returns_net: list[float],
    rt_frac: float,
) -> list[float]:
    """Bit-exact add-back of frozen RT cost (§0.5(A))."""
    return [float(n) + float(rt_frac) for n in trade_returns_net]


def mean_or_zero(values: list[float]) -> float:
    return float(np.mean(values)) if values else 0.0


def oos_timestamps(gc_grid: pd.DatetimeIndex) -> pd.DatetimeIndex:
    """Ratified OOS era grid (temporal axis)."""
    start = pd.Timestamp(OOS_START, tz="UTC")
    end = pd.Timestamp(OOS_END, tz="UTC")
    return gc_grid[(gc_grid >= start) & (gc_grid <= end)]


def mgc_oos_returns(
    mgc_bars: pd.DataFrame,
    gc_grid: pd.DatetimeIndex,
) -> np.ndarray:
    """Align native MGC returns to the GC 1h OOS grid (0.0 where MGC bar missing)."""
    ts = oos_timestamps(gc_grid)
    if len(ts) == 0:
        return np.array([], dtype=float)
    aligned = mgc_bars.reindex(ts)["ret"].fillna(0.0).to_numpy(dtype=float)
    return aligned


def identity_fill_coincidence_note(rt_frac: float) -> str:
    """Disclosure: at identity fills both clauses reduce to gross ≥ 5× rt_frac."""
    return (
        "At identity fills (net = gross − rt), ratio and hurdle clauses both "
        f"require gross ≥ 5 × rt_frac (rt_frac={rt_frac:.8f})."
    )


def effective_bar_disclosure_bp(mgc_price: float, rt_frac: float) -> float:
    """Stage-7 analog of DSR power disclosure — 5× RT hurdle in basis points."""
    return float(5.0 * rt_frac * 10_000.0)


def verify_rule_provenance(rule: FrozenRule, meta_row: dict) -> None:
    """Ensure every rule parameter came from meta, not recomputation."""
    prov = rule.as_provenance()
    for key in ("candidate_id", "kind", "m", "trigger", "direction", "horizon", "shape_hash"):
        if prov[key] != meta_row.get(key):
            raise ValueError(
                f"rule/meta mismatch on {key}: rule={prov[key]!r} meta={meta_row.get(key)!r}"
            )


def evaluate_rule_native(
    rule: FrozenRule,
    mgc_returns: np.ndarray,
    *,
    mgc_price: float,
    extra_slip_ticks_per_side: float = 0.0,
) -> RuleEval:
    """Re-evaluate a frozen rule on native MGC returns with optional slip delta."""
    cost = rt_cost_frac(mgc_price, extra_slip_ticks_per_side=extra_slip_ticks_per_side)
    return evaluate_rule(rule, mgc_returns, cost_frac_per_rt=cost)


def gross_from_eval(ev: RuleEval, rt_frac: float) -> list[float]:
    return reconstruct_gross_gc(ev.trade_returns, rt_frac)


def thin_market_assessment(
    mgc_bars: pd.DataFrame,
    gc_grid: pd.DatetimeIndex,
    *,
    intended_contracts: int = INTENDED_CONTRACTS_DEFAULT,
    active_bar_mask: np.ndarray | None = None,
) -> dict[str, Any]:
    """Per-candidate liquidity flag — evaluate always, never silently drop."""
    mgc_index = mgc_bars.index
    gc_oos = oos_timestamps(gc_grid)
    if len(gc_oos) == 0:
        coverage = 0.0
    else:
        overlap = mgc_index.intersection(gc_oos)
        coverage = len(overlap) / len(gc_oos)

    vol_oos = mgc_bars.reindex(gc_oos)["volume"].fillna(0.0).to_numpy(dtype=float)
    if vol_oos.size == 0:
        median_vol = 0.0
    elif active_bar_mask is not None and active_bar_mask.size == vol_oos.size and active_bar_mask.any():
        median_vol = float(np.median(vol_oos[active_bar_mask]))
    else:
        median_vol = float(np.median(vol_oos))

    min_vol = MEDIAN_VOLUME_MIN_MULTIPLE * intended_contracts
    thin = coverage < BAR_COVERAGE_MIN or median_vol < min_vol
    return {
        "thin_market": bool(thin),
        "bar_coverage": float(coverage),
        "median_hourly_volume": median_vol,
        "coverage_threshold": BAR_COVERAGE_MIN,
        "volume_threshold": float(min_vol),
    }


@dataclass
class CandidateRealismResult:
    candidate_id: str
    gross_gc: float
    gross_mgc_native: float
    net_mgc: float
    rt_frac: float
    rt_frac_base: float
    ratio_clause: bool
    hurdle_clause: bool
    effective_bar_bp: float
    thin_market: bool
    bar_coverage: float
    median_hourly_volume: float
    verdict: str
    n_trades: int
    extra_slip_ticks_per_side: float = 0.0
    gross_scale_mgc: float = 1.0
    identity_fill_coincidence: str = ""
    clauses_degenerate: bool = False


@dataclass
class Stage7Record:
    run_id: str
    candidates: list[CandidateRealismResult]
    fill_delta_observed: bool
    fill_delta_note: str
    nautilus: str = NAUTILUS_RUNBOOK
    thin_market_thresholds: dict[str, float] = field(
        default_factory=lambda: {
            "bar_coverage_min": BAR_COVERAGE_MIN,
            "median_volume_min_multiple": MEDIAN_VOLUME_MIN_MULTIPLE,
        }
    )

    def to_dict(self) -> dict:
        return {
            "run_id": self.run_id,
            "fill_delta_observed": self.fill_delta_observed,
            "fill_delta_note": self.fill_delta_note,
            "nautilus": self.nautilus,
            "thin_market_thresholds": self.thin_market_thresholds,
            "candidates": [asdict(c) for c in self.candidates],
        }


def _verdict(ratio_ok: bool, hurdle_ok: bool) -> str:
    if ratio_ok and hurdle_ok:
        return "PASS"
    if not ratio_ok and not hurdle_ok:
        return "FAIL_BOTH"
    if not ratio_ok:
        return "FAIL_RATIO"
    return "FAIL_HURDLE"


def evaluate_candidate_realism(
    rule: FrozenRule,
    meta_row: dict,
    gc_trade_returns_net: list[float],
    mgc_returns: np.ndarray,
    mgc_bars: pd.DataFrame,
    gc_grid: pd.DatetimeIndex,
    *,
    mgc_price: float,
    extra_slip_ticks_per_side: float = 0.0,
    gross_scale_mgc: float = 1.0,
    intended_contracts: int = INTENDED_CONTRACTS_DEFAULT,
    native_eval: RuleEval | None = None,
) -> CandidateRealismResult:
    """Full Stage-7 evaluation for one survivor.

    ``native_eval`` is an offline synthetic-proof escape hatch only: when set,
    skips ``evaluate_rule_native`` and uses the supplied ``RuleEval`` (must
    still be produced by ``evaluate_rule`` / ``evaluate_rule_native`` on the
    same frozen rule elsewhere in the test harness).
    """
    verify_rule_provenance(rule, meta_row)
    rt_base = rt_cost_frac(mgc_price)
    rt_real = rt_cost_frac(mgc_price, extra_slip_ticks_per_side=extra_slip_ticks_per_side)
    hurdle = hurdle_from_price(mgc_price)

    gross_gc = mean_or_zero(reconstruct_gross_gc(gc_trade_returns_net, rt_base))
    if native_eval is not None:
        native = native_eval
    else:
        native = evaluate_rule_native(
            rule,
            mgc_returns,
            mgc_price=mgc_price,
            extra_slip_ticks_per_side=extra_slip_ticks_per_side,
        )
    gross_mgc = mean_or_zero(gross_from_eval(native, rt_real))
    net_mgc = mean_or_zero(native.trade_returns)

    ratio_ok = ratio_clause(net_mgc, gross_gc)
    hurdle_ok = hurdle_clause(net_mgc, hurdle)

    active = np.abs(native.bar_returns) > 0
    liq = thin_market_assessment(
        mgc_bars,
        gc_grid,
        intended_contracts=intended_contracts,
        active_bar_mask=active,
    )

    degenerate = (
        extra_slip_ticks_per_side == 0.0
        and gross_scale_mgc == 1.0
        and abs(gross_mgc - gross_gc) < 1e-12
        and abs(net_mgc - (gross_gc - rt_base)) < 1e-12
    )

    return CandidateRealismResult(
        candidate_id=rule.candidate_id,
        gross_gc=gross_gc,
        gross_mgc_native=gross_mgc,
        net_mgc=net_mgc,
        rt_frac=rt_real,
        rt_frac_base=rt_base,
        ratio_clause=ratio_ok,
        hurdle_clause=hurdle_ok,
        effective_bar_bp=effective_bar_disclosure_bp(mgc_price, rt_base),
        thin_market=liq["thin_market"],
        bar_coverage=liq["bar_coverage"],
        median_hourly_volume=liq["median_hourly_volume"],
        verdict=_verdict(ratio_ok, hurdle_ok),
        n_trades=native.n_trades,
        extra_slip_ticks_per_side=extra_slip_ticks_per_side,
        gross_scale_mgc=gross_scale_mgc,
        identity_fill_coincidence=identity_fill_coincidence_note(rt_base),
        clauses_degenerate=degenerate,
    )


def run_stage7_realism(
    *,
    run_id: str,
    candidate_ids: list[str],
    rules: dict[str, FrozenRule],
    meta: dict,
    gc_trades: dict,
    mgc_bars: pd.DataFrame,
    gc_grid: pd.DatetimeIndex,
    mgc_price: float,
    per_candidate_slip: dict[str, float] | None = None,
    gross_scale_mgc: float = 1.0,
    mgc_returns: np.ndarray | None = None,
    native_evals: dict[str, RuleEval] | None = None,
) -> Stage7Record:
    """Evaluate all survivors and assemble the one-shot output record."""
    meta_by_id = {c["candidate_id"]: c for c in meta.get("candidates", [])}
    results: list[CandidateRealismResult] = []
    any_delta = False

    for cid in candidate_ids:
        if cid not in rules:
            raise KeyError(f"missing frozen rule for candidate {cid}")
        if cid not in gc_trades:
            raise KeyError(f"missing stage-4 trades for candidate {cid}")
        meta_row = meta_by_id.get(cid)
        if meta_row is None:
            raise KeyError(f"candidate {cid} not in stage-4 meta")

        slip = (per_candidate_slip or {}).get(cid, 0.0)
        oos_ret = mgc_returns if mgc_returns is not None else mgc_oos_returns(mgc_bars, gc_grid)
        native_override = (native_evals or {}).get(cid)
        res = evaluate_candidate_realism(
            rules[cid],
            meta_row,
            gc_trades[cid]["trade_returns"],
            oos_ret,
            mgc_bars,
            gc_grid,
            mgc_price=mgc_price,
            extra_slip_ticks_per_side=slip,
            gross_scale_mgc=gross_scale_mgc,
            native_eval=native_override,
        )
        if not res.clauses_degenerate:
            any_delta = True
        if slip != 0.0 or gross_scale_mgc != 1.0:
            any_delta = True
        if abs(res.gross_mgc_native - res.gross_gc) > 1e-12:
            any_delta = True
        results.append(res)

    if not any_delta:
        note = (
            "Native MGC path matched pure GC re-scale (identity fills); the two "
            "predicate clauses were degenerate on this run — both reduce to "
            "gross ≥ 5 × rt_frac."
        )
    else:
        note = "Fill or gross delta observed; ratio and hurdle clauses carry independent information."

    return Stage7Record(
        run_id=run_id,
        candidates=results,
        fill_delta_observed=any_delta,
        fill_delta_note=note,
    )


def emit_stage7_record(record: Stage7Record, *, out_dir: Path | None = None) -> Path:
    """Write ``<run_id>__stage7_realism.json``."""
    out = Path(out_dir or repo_root() / "discovery_manifests")
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{record.run_id}__stage7_realism.json"
    path.write_text(json.dumps(record.to_dict(), indent=2), encoding="utf-8")
    return path


def load_stage4_bundle(
    manifest_dir: Path,
    run_id: str,
) -> tuple[dict, dict]:
    """Load stage-4 meta + trades sidecars."""
    base = Path(manifest_dir)
    meta = json.loads((base / f"{run_id}__stage4_matrix.meta.json").read_text(encoding="utf-8"))
    trades = json.loads((base / f"{run_id}__stage4_trades.json").read_text(encoding="utf-8"))
    return meta, trades


def estimate_mgc_oos_pull(*, python: str | None = None) -> dict[str, Any]:
    """Cost-gated estimate for MGC 1h OOS pull (no network in tests)."""
    py = python or sys.executable
    cmd = [
        py,
        "-m",
        "databento_fetch.db_fetch",
        "estimate",
        "--symbols",
        "MGC.FUT",
        "--stype",
        "parent",
        "--schema",
        "ohlcv-1h",
        "--start",
        OOS_START,
        "--end",
        OOS_END,
        "--phase",
        "oos",
    ]
    env = {"PYTHONPATH": str(repo_root() / "lab")}
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env={**dict(**__import__("os").environ), **env},
        check=False,
    )
    return {
        "command": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def assert_campaign_cost_gate(estimate_cost_usd: float) -> None:
    """Pre-reg §5 — HALT if summed estimate exceeds $5.00."""
    if estimate_cost_usd > CAMPAIGN_MAX_COST_USD:
        raise RuntimeError(
            f"Campaign cost gate: estimate ${estimate_cost_usd:.4f} exceeds "
            f"frozen --max-cost ${CAMPAIGN_MAX_COST_USD:.2f} "
            f"(docs/ltm/briefs/pre-registration/DISC-CAMP-0-preregistration.md §5)."
        )


def run_real_mgc_pull(*, operator_go: bool = False, max_cost: float = CAMPAIGN_MAX_COST_USD) -> None:
    """Pull MGC OOS bars — refuses without explicit operator authorization."""
    if not operator_go:
        raise RuntimeError(
            "Refusing MGC pull without --operator-go. Pre-reg §5 requires summed "
            "estimate ≤ $5.00 recorded before the first pull; synthetic-only "
            "until Joshua authorizes."
        )
    cmd = [
        sys.executable,
        "-m",
        "databento_fetch.db_fetch",
        "pull",
        "--symbols",
        "MGC.FUT",
        "--stype",
        "parent",
        "--schema",
        "ohlcv-1h",
        "--start",
        OOS_START,
        "--end",
        OOS_END,
        "--phase",
        "oos",
        "--max-cost",
        f"{max_cost:.2f}",
    ]
    env = {**dict(**__import__("os").environ), "PYTHONPATH": str(repo_root() / "lab")}
    subprocess.run(cmd, check=True, env=env)


def nautilus_realism_stub(*, candidate_id: str, passed_bar_level: bool) -> dict[str, str]:
    """Survivor-gated Nautilus placeholder — full integration is follow-on."""
    if not passed_bar_level:
        return {"status": "SKIPPED", "reason": "bar-level predicate failed", "runbook": NAUTILUS_RUNBOOK}
    return {"status": "PENDING_FOLLOWON", "candidate_id": candidate_id, "runbook": NAUTILUS_RUNBOOK}


def _self_test() -> int:
    from discovery.motif_rules import RuleEval, freeze_rule_from_spec
    from discovery.synthetic_bars import default_motif_shape

    rt = rt_cost_frac(1800.0)
    shape = default_motif_shape(30, seed=99)
    rule = freeze_rule_from_spec(
        shape, direction=1, horizon=3, trigger=1e9, candidate_id="self_case"
    )
    idx = pd.date_range("2019-05-06", periods=500, freq="h", tz="UTC")
    mgc = pd.DataFrame({"ret": np.zeros(500), "volume": 100.0}, index=idx)
    for mult, label, expect_pass in ((8.0, "pass", True), (3.0, "venue_kill", False)):
        gross = mult * rt
        net = gross - rt
        n = 40
        meta = {"candidates": [{**rule.as_provenance(), "n_trades": n}]}
        trades = {rule.candidate_id: {"trade_returns": [net] * n}}
        native = RuleEval(
            bar_returns=np.zeros(500),
            trade_returns=[net] * n,
            entry_indices=[],
            n_trades=n,
        )
        rec = run_stage7_realism(
            run_id=f"self_{label}",
            candidate_ids=[rule.candidate_id],
            rules={rule.candidate_id: rule},
            meta=meta,
            gc_trades=trades,
            mgc_bars=mgc,
            gc_grid=idx,
            mgc_price=1800.0,
            native_evals={rule.candidate_id: native},
        )
        passed = rec.candidates[0].verdict == "PASS"
        if passed != expect_pass:
            print(f"self-test failed on {label}: verdict={rec.candidates[0].verdict}")
            return 1
    print("realism_mgc self-test OK")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Stage-7 MGC realism engine")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--estimate-mgc-oos", action="store_true")
    parser.add_argument("--operator-go", action="store_true", help="Authorize real MGC pull")
    parser.add_argument("--pull-mgc-oos", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return _self_test()
    if args.estimate_mgc_oos:
        print(json.dumps(estimate_mgc_oos_pull(), indent=2))
        return 0
    if args.pull_mgc_oos:
        run_real_mgc_pull(operator_go=args.operator_go)
        return 0
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
