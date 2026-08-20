"""Candidate return-series reproducibility index (Stage 2).

Regenerate a date-indexed daily/bar return series on demand from a closed
discovery-manifest pointer to a FrozenRule provenance file — store the pointer,
not the numeric series (design §3.2 Approach C).
"""
from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from discovery.frozen_rules import load_frozen_rules
from discovery.motif_rules import evaluate_rule
from discovery import register_search as rs


SeriesLoader = Callable[[str, str], np.ndarray | pd.Series]


def _load_manifest(run_id: str, ledger_dir: Path | str | None) -> dict[str, Any]:
    """Reuse register_search path convention; honor ledger_dir without mutating LEDGER."""
    if ledger_dir is None:
        return rs._load(run_id)
    path = Path(ledger_dir) / f"{run_id}.json"
    if not path.exists():
        raise FileNotFoundError(
            f"No registration for run-id '{run_id}' under ledger_dir={ledger_dir!s}. "
            "Run `open` first (declare K before results)."
        )
    import json

    return json.loads(path.read_text(encoding="utf-8"))


def _instrument_tag(manifest: dict[str, Any]) -> str:
    """First arg for series_loader: profile_cell symbol when present, else data_window."""
    cell = manifest.get("profile_cell")
    if isinstance(cell, str) and cell.strip():
        return cell.split(":", 1)[0].strip() or cell
    return str(manifest.get("data_window", ""))


def _data_window_start(data_window: str) -> str:
    """Parse the start half of an open_run data_window (e.g. 2010-06-06:2026-01-01)."""
    if ":" not in data_window:
        raise ValueError(
            f"manifest data_window {data_window!r} is not 'start:end'; cannot "
            "synthesize a date index for a bare ndarray from series_loader"
        )
    return data_window.split(":", 1)[0].strip()


def _cost_frac_per_rt(manifest: dict[str, Any]) -> float:
    """Prefer an explicit recorded cost; else 0.0 (do not guess a nonzero)."""
    results = manifest.get("results") or {}
    for key in ("cost_frac_per_rt", "cost_frac"):
        if key in results:
            return float(results[key])
        if key in manifest:
            return float(manifest[key])
    return 0.0


def _find_candidate(manifest: dict[str, Any], candidate_id: str) -> dict[str, Any]:
    results = manifest.get("results")
    if not isinstance(results, dict):
        raise ValueError(
            f"run '{manifest.get('run_id')}' has no results block; close the run first"
        )
    candidates = results.get("candidates") or []
    for row in candidates:
        if row.get("id") == candidate_id:
            return row
    raise ValueError(
        f"candidate_id {candidate_id!r} not found in run "
        f"'{manifest.get('run_id')}' results.candidates"
    )


def regenerate_return_series(
    run_id: str,
    candidate_id: str,
    *,
    ledger_dir: Path | str | None = None,
    series_loader: SeriesLoader,
) -> pd.Series:
    """Rebuild a candidate's bar-return series from its frozen-rule pointer.

    Loads the K-ledger manifest for ``run_id``, resolves ``rule_provenance_path``
    for ``candidate_id``, loads the matching ``FrozenRule``, asks ``series_loader``
    for the underlying market series, re-runs ``evaluate_rule``, and returns a
    date-indexed ``pandas.Series`` named ``candidate_id`` (injectable into
    ``breadth.compute_breadth(..., candidate=...)``).

    ``series_loader`` is required (keyword-only), signature
    ``(instrument_or_data_window_tag, data_window) -> np.ndarray | pd.Series``.
    No production CME-series loader is wired in by this function — supplying one
    that reads real market data is Stage 1 / a separate follow-up, deliberately
    out of scope here so this module has zero vendor-data dependency.

    If ``series_loader`` returns a ``pandas.Series``, its index is attached to the
    output (must be datetime-like for breadth injection). If it returns a bare
    ``np.ndarray``, a business-day index of matching length is synthesized from
    the manifest ``data_window`` start date.
    """
    manifest = _load_manifest(run_id, ledger_dir)
    row = _find_candidate(manifest, candidate_id)
    provenance_path = row.get("rule_provenance_path")
    if not provenance_path:
        raise ValueError(
            f"candidate_id {candidate_id!r} in run '{run_id}' has no recorded "
            "rule_provenance_path; regenerate_return_series cannot reproduce it "
            "from the ledger alone (close with --rule-provenance-file)."
        )

    rules = load_frozen_rules(provenance_path)
    matches = [r for r in rules if r.candidate_id == candidate_id]
    if not matches:
        raise ValueError(
            f"no FrozenRule with candidate_id={candidate_id!r} in provenance file "
            f"{provenance_path!s} (file has "
            f"{[r.candidate_id for r in rules]!r})"
        )
    rule = matches[0]

    data_window = str(manifest.get("data_window", ""))
    tag = _instrument_tag(manifest)
    loaded = series_loader(tag, data_window)

    if isinstance(loaded, pd.Series):
        values = np.asarray(loaded.to_numpy(), dtype=float)
        index = loaded.index
    else:
        values = np.asarray(loaded, dtype=float)
        start = _data_window_start(data_window)
        index = pd.bdate_range(start=start, periods=len(values))

    cost = _cost_frac_per_rt(manifest)
    evaluation = evaluate_rule(rule, values, cost_frac_per_rt=cost)
    if len(evaluation.bar_returns) != len(index):
        raise ValueError(
            f"evaluate_rule bar_returns length {len(evaluation.bar_returns)} != "
            f"series index length {len(index)}"
        )
    return pd.Series(evaluation.bar_returns, index=index, name=candidate_id)
