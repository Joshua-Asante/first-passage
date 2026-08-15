"""MSL slate-card preflight — evidence tables only (no campaign verdicts).

Reads a slate-card YAML and emits three evidence blocks:

1. Dedup — raw ``rg`` hit lines against registry/graveyard paths
2. Instrument cell — raw stdout from ``scripts/instrument_profiles.py cell``
3. Arithmetic — cost-law / payability / worst-day / sigma_d / implied-SR

**Surfacing ≠ killing.** Exit 0 on successful evidence emission even when
registry hits or BINDING BAR lines appear. Campaign-manager verdict strings are owned by P3.x, never this tool.

Formula pin (implied-SR; design_law / ADR 2026-08-13 report-only;
2026-08-10 freeze-time gate superseded)::

    expectancy_r = p * rr - (1 - p)
    per_trade_sharpe = expectancy_r / (sqrt(p*(1-p)) * (1+rr))
    implied_annualized_sr = per_trade_sharpe * sqrt(n_trades) * sqrt(252)
"""
from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

TOOLING_DISCLAIMER = "evidence only; computes evidence only"
TRADING_DAYS_PER_YEAR = 252
COST_LAW_MULTIPLES = (1.0, 2.0, 4.0)
PAYOUT_MIN_USD = 200.0
WORST_DAY_BOUND_USD = 750.0
DEFAULT_DEDUP_PATHS = (
    "docs/rejected_candidates.md",
    "lab/CATALOG.md",
)


def _repo_root() -> Path:
    """Resolve repo root from this file: lab/research_utils/msl_preflight.py."""
    return Path(__file__).resolve().parents[2]


def per_trade_sharpe(p: float, rr: float) -> float:
    """Scale-free Sharpe of one bracket at win rate ``p`` and reward:risk ``rr``."""
    expectancy_r = p * rr - (1.0 - p)
    denom = math.sqrt(p * (1.0 - p)) * (1.0 + rr)
    if denom == 0.0:
        raise ValueError("per_trade_sharpe denominator is zero")
    return expectancy_r / denom


def implied_annualized_sr(p: float, rr: float, n_trades: int) -> float:
    """Annualized Sharpe assumed by a (p, rr, n) cell — report-only (ADR 2026-08-13)."""
    if n_trades < 0:
        raise ValueError("n_trades must be non-negative")
    return per_trade_sharpe(p, rr) * math.sqrt(n_trades) * math.sqrt(TRADING_DAYS_PER_YEAR)


def expectancy_r(p: float, rr: float) -> float:
    return p * rr - (1.0 - p)


def stop_floor_usd(rt_usd: float, expectancy: float, multiple: float) -> float:
    if expectancy <= 0:
        raise ValueError("expectancy_r must be positive for stop_floor_usd")
    return multiple * rt_usd / expectancy


def daily_sigma(
    p: float,
    span_pts: float,
    point_value_usd: float,
    n_trades: int,
    contracts: int,
) -> float:
    per_trade = math.sqrt(p * (1.0 - p)) * span_pts * point_value_usd
    return per_trade * contracts * math.sqrt(n_trades)


def all_win_day(
    n_trades: int,
    contracts: int,
    target_pts: float,
    point_value_usd: float,
    rt_usd: float,
) -> float:
    return n_trades * contracts * (target_pts * point_value_usd - rt_usd)


def all_lose_day(
    n_trades: int,
    contracts: int,
    stop_pts: float,
    point_value_usd: float,
    rt_usd: float,
) -> float:
    return n_trades * contracts * (stop_pts * point_value_usd + rt_usd)


@dataclass(frozen=True)
class SlateCard:
    """Minimal slate-card fields consumed by the evidence CLI."""

    path: Path
    raw: Mapping[str, Any]
    card_id: str
    instrument: str
    mechanism: str
    dedup_query: str
    dedup_paths: tuple[str, ...]
    p: float
    rr: float
    n_trades: int
    rt_cost_usd: float | None = None
    point_value_usd: float | None = None
    contracts: int = 1
    stop_pts: float | None = None
    target_pts: float | None = None
    cost_law_multiple: float = 4.0

    @classmethod
    def load(cls, path: Path) -> "SlateCard":
        text = path.read_text(encoding="utf-8")
        data = yaml.safe_load(text)
        if not isinstance(data, dict):
            raise ValueError(f"card {path} must be a YAML mapping")
        required = ("instrument", "mechanism", "p", "rr", "n_trades")
        missing = [k for k in required if k not in data]
        if missing:
            raise ValueError(f"card {path} missing required fields: {missing}")

        query = data.get("dedup_query")
        if query is None:
            query = data.get("dedup_needle")
        if query is None:
            query = data.get("id") or data.get("card_id") or ""
        if not isinstance(query, str):
            raise ValueError("dedup_query must be a string")

        paths_raw = data.get("dedup_paths")
        if paths_raw is None:
            paths = DEFAULT_DEDUP_PATHS
        elif isinstance(paths_raw, (list, tuple)):
            paths = tuple(str(p) for p in paths_raw)
        else:
            raise ValueError("dedup_paths must be a list of path strings")

        def _opt_float(key: str) -> float | None:
            if key not in data or data[key] is None:
                return None
            return float(data[key])

        return cls(
            path=path,
            raw=data,
            card_id=str(data.get("id") or data.get("card_id") or path.stem),
            instrument=str(data["instrument"]),
            mechanism=str(data["mechanism"]),
            dedup_query=query,
            dedup_paths=paths,
            p=float(data["p"]),
            rr=float(data["rr"]),
            n_trades=int(data["n_trades"]),
            rt_cost_usd=_opt_float("rt_cost_usd"),
            point_value_usd=_opt_float("point_value_usd"),
            contracts=int(data.get("contracts", 1)),
            stop_pts=_opt_float("stop_pts"),
            target_pts=_opt_float("target_pts"),
            cost_law_multiple=float(data.get("cost_law_multiple", 4.0)),
        )


@dataclass
class EvidenceReport:
    card_id: str
    card_path: str
    disclaimer: str = TOOLING_DISCLAIMER
    dedup_query: str = ""
    dedup_paths: list[str] = field(default_factory=list)
    dedup_hits: list[str] = field(default_factory=list)
    cell_command: list[str] = field(default_factory=list)
    cell_stdout: str = ""
    cell_returncode: int | None = None
    arithmetic: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _resolve_rg() -> str:
    found = shutil.which("rg")
    if found:
        return found
    # Cursor ships ripgrep; fall back if PATH is thin.
    cursor_rg = (
        Path(os.environ.get("LOCALAPPDATA", ""))
        / "Programs"
        / "cursor"
        / "resources"
        / "app"
        / "node_modules"
        / "@vscode"
        / "ripgrep"
        / "bin"
        / "rg.exe"
    )
    if cursor_rg.is_file():
        return str(cursor_rg)
    raise FileNotFoundError(
        "rg (ripgrep) not found on PATH; required for dedup evidence block"
    )


def run_dedup(
    query: str,
    paths: Sequence[str],
    *,
    repo_root: Path | None = None,
) -> list[str]:
    """Return raw ``rg`` hit lines for ``query`` across ``paths`` (evidence only)."""
    root = repo_root or _repo_root()
    if not query:
        return []
    existing = [str(root / p) for p in paths if (root / p).exists()]
    if not existing:
        return []
    rg = _resolve_rg()
    # --no-heading --line-number keeps lines parseable; exit 1 = no matches.
    proc = subprocess.run(
        [rg, "--no-heading", "--line-number", "--fixed-strings", "--", query, *existing],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(root),
        check=False,
    )
    if proc.returncode not in (0, 1):
        err = (proc.stderr or "").strip() or f"rg exited {proc.returncode}"
        raise RuntimeError(f"dedup rg failed: {err}")
    lines = [ln for ln in (proc.stdout or "").splitlines() if ln.strip()]
    return lines


def run_cell(
    instrument: str,
    mechanism: str,
    *,
    repo_root: Path | None = None,
    python_exe: str | None = None,
) -> tuple[str, int, list[str]]:
    """Shell ``instrument_profiles.py cell`` and return (stdout, returncode, cmd)."""
    root = repo_root or _repo_root()
    script = root / "scripts" / "instrument_profiles.py"
    if not script.is_file():
        raise FileNotFoundError(f"missing {script}")
    exe = python_exe or sys.executable
    cmd = [exe, str(script), "cell", instrument, mechanism]
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(root),
        check=False,
    )
    # Surface stdout even when the cell command exits 1 (bars are blocking for
    # that tool; this preflight still emits evidence and exits 0).
    out = proc.stdout or ""
    if proc.stderr:
        # Keep stderr visible in the evidence stream without inventing verdicts.
        out = out + (("\n" if out and not out.endswith("\n") else "") + proc.stderr)
    return out, int(proc.returncode), cmd


def compute_arithmetic(card: SlateCard) -> dict[str, Any]:
    """Build arithmetic evidence table from card fields (numeric evidence only)."""
    exp = expectancy_r(card.p, card.rr)
    pts = per_trade_sharpe(card.p, card.rr)
    implied = implied_annualized_sr(card.p, card.rr, card.n_trades)
    table: dict[str, Any] = {
        "p": card.p,
        "rr": card.rr,
        "n_trades": card.n_trades,
        "contracts": card.contracts,
        "expectancy_r": round(exp, 6),
        "per_trade_sharpe": round(pts, 6),
        "implied_annualized_sr": round(implied, 2),
        "implied_annualized_sr_raw": implied,
        "trading_days_per_year": TRADING_DAYS_PER_YEAR,
    }

    rt = card.rt_cost_usd
    pv = card.point_value_usd
    stop = card.stop_pts
    target = card.target_pts

    cost_rows: list[dict[str, Any]] = []
    if rt is not None and exp > 0:
        for multiple in COST_LAW_MULTIPLES:
            floor = stop_floor_usd(rt, exp, multiple)
            row: dict[str, Any] = {
                "multiple": multiple,
                "stop_floor_usd": round(floor, 4),
            }
            if pv is not None and pv > 0:
                row["stop_floor_pts"] = round(floor / pv, 4)
            cost_rows.append(row)
        table["cost_law"] = {
            "rt_cost_usd": rt,
            "rows": cost_rows,
            "card_multiple": card.cost_law_multiple,
            "stop_floor_usd_at_card_multiple": round(
                stop_floor_usd(rt, exp, card.cost_law_multiple), 4
            ),
        }
        # Derive stop/target from cost floor when the card omitted them.
        if stop is None and pv is not None and pv > 0:
            stop = stop_floor_usd(rt, exp, card.cost_law_multiple) / pv
            if target is None:
                target = stop * card.rr

    if (
        stop is not None
        and target is not None
        and pv is not None
        and rt is not None
    ):
        span = stop + target
        win = all_win_day(card.n_trades, card.contracts, target, pv, rt)
        lose = all_lose_day(card.n_trades, card.contracts, stop, pv, rt)
        sig = daily_sigma(card.p, span, pv, card.n_trades, card.contracts)
        table["geometry"] = {
            "stop_pts": round(stop, 4),
            "target_pts": round(target, 4),
            "span_pts": round(span, 4),
            "point_value_usd": pv,
            "rt_cost_usd": rt,
        }
        table["payability"] = {
            "all_win_day_usd": round(win, 4),
            "payout_min_usd_reference": PAYOUT_MIN_USD,
            "all_win_day_minus_ref": round(win - PAYOUT_MIN_USD, 4),
        }
        table["worst_day"] = {
            "all_lose_day_usd": round(lose, 4),
            "worst_day_bound_usd_reference": WORST_DAY_BOUND_USD,
            "bound_minus_all_lose_day": round(WORST_DAY_BOUND_USD - lose, 4),
        }
        table["sigma_d"] = {
            "sigma_d_usd": round(sig, 4),
            "sigma_d_usd_raw": sig,
        }
    else:
        table["geometry"] = None
        table["payability"] = None
        table["worst_day"] = None
        table["sigma_d"] = None
        table["geometry_note"] = (
            "optional stop_pts/target_pts/point_value_usd/rt_cost_usd "
            "absent — payability/worst-day/sigma_d not computed"
        )

    return table


def preflight(
    card_path: Path,
    *,
    repo_root: Path | None = None,
    python_exe: str | None = None,
) -> EvidenceReport:
    """Load card and collect all evidence blocks."""
    root = repo_root or _repo_root()
    card = SlateCard.load(Path(card_path))
    hits = run_dedup(card.dedup_query, card.dedup_paths, repo_root=root)
    stdout, rc, cmd = run_cell(
        card.instrument,
        card.mechanism,
        repo_root=root,
        python_exe=python_exe,
    )
    arithmetic = compute_arithmetic(card)
    return EvidenceReport(
        card_id=card.card_id,
        card_path=str(Path(card_path)),
        dedup_query=card.dedup_query,
        dedup_paths=list(card.dedup_paths),
        dedup_hits=hits,
        cell_command=cmd,
        cell_stdout=stdout,
        cell_returncode=rc,
        arithmetic=arithmetic,
    )


def format_report(report: EvidenceReport) -> str:
    """UTF-8 text evidence blocks for human/campaign-manager consumption."""
    lines: list[str] = []
    lines.append(f"=== MSL preflight evidence: {report.card_id} ===")
    lines.append(f"disclaimer: {report.disclaimer}")
    lines.append(f"card: {report.card_path}")
    lines.append("")
    lines.append("--- dedup ---")
    lines.append(f"query: {report.dedup_query!r}")
    lines.append(f"paths: {', '.join(report.dedup_paths)}")
    if report.dedup_hits:
        lines.append(f"hits ({len(report.dedup_hits)}):")
        lines.extend(report.dedup_hits)
    else:
        lines.append("hits (0):")
    lines.append("")
    lines.append("--- instrument cell ---")
    lines.append(f"command: {' '.join(report.cell_command)}")
    lines.append(f"cell_returncode: {report.cell_returncode}")
    lines.append("stdout:")
    lines.append(report.cell_stdout.rstrip("\n"))
    lines.append("")
    lines.append("--- arithmetic ---")
    lines.append(json.dumps(report.arithmetic, indent=2, sort_keys=True))
    lines.append("")
    return "\n".join(lines)


def _force_utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        except Exception:
            pass


def main(argv: list[str] | None = None) -> int:
    _force_utf8_stdio()
    ap = argparse.ArgumentParser(
        description=(
            "MSL slate-card preflight — evidence tables only "
            f"({TOOLING_DISCLAIMER})."
        )
    )
    ap.add_argument("card", type=Path, help="Path to slate-card YAML")
    ap.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON evidence report instead of text blocks",
    )
    ap.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Override repo root (default: inferred from this module)",
    )
    args = ap.parse_args(argv)
    report = preflight(args.card, repo_root=args.repo_root)
    if args.json:
        print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(format_report(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
