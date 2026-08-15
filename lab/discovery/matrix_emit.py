"""Stage-4 matrix emitter — option-(i) contract for ``universe_gate.load_returns_matrix``.

Emits beside a run id:
  ``<run_id>__stage4_matrix.parquet`` / ``.csv``
  ``<run_id>__stage4_matrix.meta.json``
  ``<run_id>__stage4_trades.json``
  ``<run_id>__regime_labels.parquet``

Synthetic mode never calls real ``register_search open`` (operator-gated).
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from discovery.k_count import KBracket
from discovery.scorer import ScoredCandidate

V_RULE = "1/n"


@dataclass
class Stage4Artifacts:
    matrix_csv: Path
    matrix_parquet: Path | None
    meta_json: Path
    trades_json: Path
    regime_parquet: Path | None
    meta: dict


def _align_bar_matrix(
    survivors: list[ScoredCandidate],
    timestamps: pd.DatetimeIndex,
    *,
    zero_benchmark: bool = True,
    underlying_ret: np.ndarray | None = None,
    dedrift: bool = False,
) -> pd.DataFrame:
    """Build timestamp-indexed candidate columns + benchmark."""
    data: dict[str, np.ndarray] = {}
    for s in survivors:
        col = s.oos_eval.bar_returns
        if dedrift and underlying_ret is not None:
            # Off-by-default real-campaign transform (§0.5(B)): subtract exposure-
            # matched unconditional drift on active bars.
            active = np.abs(col) > 0
            if active.any():
                mu = float(underlying_ret[active].mean())
                col = col.copy()
                col[active] = col[active] - mu
        data[s.rule.candidate_id] = col
    if zero_benchmark:
        data["benchmark"] = np.zeros(len(timestamps), dtype=float)
    else:
        if underlying_ret is None:
            raise ValueError("buy-hold benchmark requires underlying_ret")
        data["benchmark"] = np.asarray(underlying_ret, dtype=float)
    df = pd.DataFrame(data, index=pd.Index(timestamps, name="timestamp"))
    return df


def emit_stage4(
    survivors: list[ScoredCandidate],
    timestamps: pd.DatetimeIndex,
    bracket: KBracket,
    *,
    out_dir: Path,
    run_id: str,
    regime_labels: np.ndarray | None = None,
    era_bounds: dict | None = None,
    cost_constants: dict | None = None,
    zero_benchmark: bool = True,
    underlying_ret: np.ndarray | None = None,
    dedrift: bool = False,
) -> Stage4Artifacts:
    """Write the Stage-4 bundle. ``k_spa`` = scored survivor count ≠ ``k_dsr``."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    prefix = out_dir / f"{run_id}__stage4"

    df = _align_bar_matrix(
        survivors,
        timestamps,
        zero_benchmark=zero_benchmark,
        underlying_ret=underlying_ret,
        dedrift=dedrift,
    )
    csv_path = Path(str(prefix) + "_matrix.csv")
    # CSV contract: timestamp as first column (load_returns_matrix).
    df_out = df.reset_index()
    df_out.to_csv(csv_path, index=False)

    pq_path = Path(str(prefix) + "_matrix.parquet")
    try:
        df.to_parquet(pq_path)
    except Exception:
        pq_path = None  # parquet engine optional

    trades = {
        s.rule.candidate_id: {
            "trade_returns": list(map(float, s.oos_eval.trade_returns)),
            "n_trades": s.oos_eval.n_trades,
            "V": (1.0 / s.oos_eval.n_trades) if s.oos_eval.n_trades else None,
            "dsr_unreachable_low_n": s.dsr_unreachable_low_n,
            "is_pvalue": s.is_pvalue,
        }
        for s in survivors
    }
    trades_path = Path(str(prefix) + "_trades.json")
    trades_path.write_text(json.dumps(trades, indent=2), encoding="utf-8")

    meta = {
        "run_id": run_id,
        "era_bounds": era_bounds or {},
        "tz": "UTC",
        "cost_constants": cost_constants or {},
        "k_dsr": bracket.k_dsr,
        "k_raw": bracket.k_raw,
        "k_spa": len(survivors),
        "k_bracket": bracket.as_dict()["bracket"],
        "v_rule": V_RULE,
        "zero_benchmark": zero_benchmark,
        "dedrift": dedrift,
        "candidates": [
            {
                **s.rule.as_provenance(),
                "n_trades": s.oos_eval.n_trades,
                "dsr_unreachable_low_n": s.dsr_unreachable_low_n,
                "is_pvalue": s.is_pvalue,
                "cost_law_pass": s.cost_law_pass,
            }
            for s in survivors
        ],
    }
    meta_path = Path(str(prefix) + "_matrix.meta.json")
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    regime_path = None
    if regime_labels is not None:
        regime_path = Path(str(prefix)[:-8] + "__regime_labels.parquet")
        # Keep beside the matrix with the handoff name pattern.
        regime_path = out_dir / f"{run_id}__regime_labels.parquet"
        reg = pd.DataFrame(
            {"regime": np.asarray(regime_labels)},
            index=pd.Index(timestamps[: len(regime_labels)], name="timestamp"),
        )
        try:
            reg.to_parquet(regime_path)
        except Exception:
            # CSV fallback
            regime_path = out_dir / f"{run_id}__regime_labels.csv"
            reg.reset_index().to_csv(regime_path, index=False)

    return Stage4Artifacts(
        matrix_csv=csv_path,
        matrix_parquet=pq_path,
        meta_json=meta_path,
        trades_json=trades_path,
        regime_parquet=regime_path,
        meta=meta,
    )


def trade_matrix_for_gate(
    survivors: list[ScoredCandidate],
    *,
    n_pad: int | None = None,
) -> tuple[np.ndarray, np.ndarray, list[str]]:
    """Align per-trade returns into a (n, K) matrix for ``run_universe_gate``.

    Rows are trade observations (DSR n source), not bars. Shorter columns are
    padded with 0.0 so SPA/PBO see a rectangular array; the selected column's
    leading ``n_trades`` moments dominate DSR when noise pads are mean-zero.
    Prefer passing equal-length columns from the synthetic generator.
    """
    if not survivors:
        raise ValueError("no survivors to build trade matrix")
    ids = [s.rule.candidate_id for s in survivors]
    lengths = [s.oos_eval.n_trades for s in survivors]
    n = int(n_pad or max(lengths))
    mat = np.zeros((n, len(survivors)), dtype=float)
    for j, s in enumerate(survivors):
        tr = np.asarray(s.oos_eval.trade_returns, dtype=float)
        mat[: tr.size, j] = tr
    bench = np.zeros(n, dtype=float)
    return mat, bench, ids
