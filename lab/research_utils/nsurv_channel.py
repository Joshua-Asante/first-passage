"""N-SURV candidate-P&L scoring channel (TNEC-1 limb).

Candidate-independent harness: take an arbitrary daily P&L series at a declared
$100K-basis deployable integer sizing, plus a regime-half boundary date, and
emit the frozen Part-A scoring block on the incumbent ``Tradeify_Select_100K``
eval at the **intraday-honest** clock — full panel + both regime halves — with a
single ``N-SURV PASS|FAIL`` line.

Engine path is the same W1 used
(``lab/discovery/prop_survivor_scoring.py`` → ``run_tier_remc`` / ``run_seed`` /
``simulate_path``). Thresholds are parsed at runtime from
``prop_survivor_scoring.DEFAULT_PREREG`` — never restated here. No MC
re-calibration, no ``dd_protection`` / ``firm_rules`` edits.

Inequality directions (prereg Part A / ``score_part_a``) — this module pins the
DIRECTION and inclusivity, never the number:
  bust ≤ eval_bust_ceiling  ∧  P(pass) ≥ pass_floor
Both bounds are **non-strict** (a value exactly ON the ceiling/floor clears).

⚠ The live ceiling is **5.0%** (``2026-08-26-prop-survivor-scoring-prereg-v2.md``
§3, which ``DEFAULT_PREREG`` points at). Docstrings and tests here previously read
**3.0%** — that is the CLOSED 2026-07-13 v1 value, kept only as a loader fixture.
Whatever ``DEFAULT_PREREG`` resolves to is the gate; do not transcribe either
number into this module.

Input contract
--------------
CSV or JSON rows with at least ``date``, ``pnl_usd``. For the intraday-honest
clock, rows must also carry ``intraday_low`` (≤ 0 same-day equity excursion from
the day's open, paired 1:1 with ``pnl_usd`` — Phase-4 invariant). The series is
already at the sizing under test; this channel does not apply a further lifecycle
haircut.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal, Sequence

import numpy as np
import pandas as pd

from discovery.prop_survivor_scoring import (
    ScoringThresholds,
    load_scoring_thresholds,
    paired_blocks_from_daily,
    run_tier_remc,
    score_part_a,
)
from firm_rules import FIRM_RULES
from research_utils.repo_root import repo_root

# Incumbent eval for TNEC-1 N-SURV (docs/spec/2026-08-08-tradeify-necessary-conditions-target-spec.md).
DEFAULT_FIRM_KEY = "Tradeify_Select_100K"
SIZING_BASIS_USD = 100_000.0

NSurvVerdict = Literal["PASS", "FAIL"]

_REQUIRED_COLUMNS = frozenset({"date", "pnl_usd"})
_OPTIONAL_INTRADAY = "intraday_low"


@dataclass(frozen=True)
class PartitionScore:
    """One (full | H1 | H2) remc partition at the frozen gate."""

    label: str
    headline_bust: float
    pass_rate: float
    floor_ok: bool
    n_bdays: int
    n_sims: int
    consistency: float | None
    gated_on: str
    intraday_low: bool


@dataclass(frozen=True)
class NSurvReport:
    """Frozen-format N-SURV scoring block for one candidate series."""

    firm_key: str
    sizing_basis_usd: float
    half_boundary_date: str  # ISO date; H1 is strictly before, H2 from boundary onward
    thresholds_source: str
    eval_bust_ceiling: float
    pass_floor: float
    full: PartitionScore
    h1: PartitionScore
    h2: PartitionScore
    nsurv: NSurvVerdict

    @property
    def nsurv_line(self) -> str:
        return f"N-SURV {self.nsurv}"

    def to_dict(self) -> dict:
        return {
            "firm_key": self.firm_key,
            "sizing_basis_usd": self.sizing_basis_usd,
            "half_boundary_date": self.half_boundary_date,
            "thresholds_source": self.thresholds_source,
            "eval_bust_ceiling": self.eval_bust_ceiling,
            "pass_floor": self.pass_floor,
            "full": asdict(self.full),
            "H1": asdict(self.h1),
            "H2": asdict(self.h2),
            "nsurv": self.nsurv,
            "nsurv_line": self.nsurv_line,
        }

    def format_block(self) -> str:
        """Human-readable frozen scoring block + single N-SURV line."""

        def _row(p: PartitionScore) -> str:
            return (
                f"{p.label}: bust={p.headline_bust:.2%} pass={p.pass_rate:.2%} "
                f"{'PASS' if p.floor_ok else 'FAIL'} (n={p.n_bdays})"
            )

        lines = [
            f"firm={self.firm_key} sizing_basis=${self.sizing_basis_usd:,.0f} "
            f"half_boundary={self.half_boundary_date}",
            f"floor: bust≤{self.eval_bust_ceiling:.1%} ∧ P(pass)≥{self.pass_floor:.0%}",
            _row(self.full),
            _row(self.h1),
            _row(self.h2),
            self.nsurv_line,
        ]
        return "\n".join(lines)


def clears_nsurv_floor(
    headline_bust: float,
    pass_rate: float,
    thresholds: ScoringThresholds,
) -> bool:
    """Part A inequality directions — bust ≤ ceiling ∧ pass ≥ floor (non-strict)."""
    return score_part_a(
        {"headline_bust": float(headline_bust), "pass_rate": float(pass_rate)},
        thresholds,
    )


def load_candidate_daily_pnl(path: Path | str) -> pd.DataFrame:
    """Load CSV or JSON daily series: ``date``, ``pnl_usd`` [, ``intraday_low``]."""
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(p)
    suffix = p.suffix.lower()
    if suffix == ".csv":
        df = pd.read_csv(p)
    elif suffix == ".json":
        raw = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(raw, dict) and "rows" in raw:
            raw = raw["rows"]
        df = pd.DataFrame(raw)
    else:
        raise ValueError(f"unsupported candidate series format: {p.suffix!r} (use .csv or .json)")

    missing = _REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"candidate series missing columns {sorted(missing)}: {p}")

    out = pd.DataFrame(
        {
            "date": pd.to_datetime(df["date"]).dt.normalize(),
            "pnl_usd": pd.to_numeric(df["pnl_usd"], errors="raise").astype(float),
        }
    )
    if _OPTIONAL_INTRADAY in df.columns:
        out[_OPTIONAL_INTRADAY] = pd.to_numeric(
            df[_OPTIONAL_INTRADAY], errors="raise"
        ).astype(float)
    out = out.sort_values("date").reset_index(drop=True)
    if out["date"].duplicated().any():
        raise ValueError(f"candidate series has duplicate dates: {p}")
    return out


def split_at_boundary(
    frame: pd.DataFrame,
    half_boundary_date: str | pd.Timestamp,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split on the declared regime-half boundary.

    H1 = rows with ``date < boundary``; H2 = rows with ``date >= boundary``.
    Both halves must be non-empty.
    """
    boundary = pd.Timestamp(half_boundary_date).normalize()
    h1 = frame.loc[frame["date"] < boundary].copy()
    h2 = frame.loc[frame["date"] >= boundary].copy()
    if h1.empty or h2.empty:
        raise ValueError(
            f"regime-half boundary {boundary.date().isoformat()} yields an empty half "
            f"(H1 n={len(h1)}, H2 n={len(h2)}; series "
            f"{frame['date'].iloc[0].date()}→{frame['date'].iloc[-1].date()})"
        )
    return h1, h2


def _consistency_frac(firm_key: str) -> float | None:
    raw = FIRM_RULES[firm_key].get("consistency_rule_pct")
    if raw is None:
        return None
    return float(raw) / 100.0


def _require_intraday(frame: pd.DataFrame) -> np.ndarray:
    if _OPTIONAL_INTRADAY not in frame.columns:
        raise ValueError(
            "N-SURV requires paired intraday_low (intraday-honest clock); "
            "series has only date/pnl_usd"
        )
    low = frame[_OPTIONAL_INTRADAY].to_numpy(dtype=float)
    if np.any(low > 0.0):
        raise ValueError("intraday_low entries must be ≤ 0.0")
    return low


def _run_partition(
    daily: np.ndarray,
    intraday: np.ndarray,
    *,
    firm_key: str,
    thr: ScoringThresholds,
    label: str,
    n_sims: int | None,
) -> PartitionScore:
    blocks_p, blocks_l = paired_blocks_from_daily(daily, intraday)
    cons = _consistency_frac(firm_key)
    run = run_tier_remc(
        firm_key,
        blocks_p,
        thr,
        n_sims=n_sims,
        consistency=cons,
        intraday_blocks=blocks_l,
    )
    floor_ok = bool(clears_nsurv_floor(run["headline_bust"], run["pass_rate"], thr))
    return PartitionScore(
        label=label,
        headline_bust=float(run["headline_bust"]),
        pass_rate=float(run["pass_rate"]),
        floor_ok=floor_ok,
        n_bdays=int(daily.size),
        n_sims=int(run["n_sims"]),
        consistency=cons,
        gated_on="run2" if cons is not None else "run1_degenerate",
        intraday_low=True,
    )


def score_nsurv(
    frame: pd.DataFrame,
    *,
    half_boundary_date: str | pd.Timestamp,
    firm_key: str = DEFAULT_FIRM_KEY,
    sizing_basis_usd: float = SIZING_BASIS_USD,
    thresholds: ScoringThresholds | None = None,
    n_sims: int | None = None,
) -> NSurvReport:
    """Score full + both halves on the intraday-honest clock; emit N-SURV PASS/FAIL.

    N-SURV PASS iff full ∧ H1 ∧ H2 each clear Part A (bust ≤ ceiling ∧ pass ≥ floor).
    """
    if firm_key not in FIRM_RULES:
        raise KeyError(firm_key)
    if abs(float(sizing_basis_usd) - SIZING_BASIS_USD) > 1e-9:
        raise ValueError(
            f"N-SURV channel expects sizing_basis_usd={SIZING_BASIS_USD:.0f} "
            f"(declared $100K-basis); got {sizing_basis_usd}"
        )
    if frame.empty or len(frame) < 5:
        raise ValueError(
            f"candidate series needs ≥5 business days for week-blocks; got {len(frame)}"
        )

    thr = thresholds if thresholds is not None else load_scoring_thresholds()
    daily = frame["pnl_usd"].to_numpy(dtype=float)
    intraday = _require_intraday(frame)
    if daily.size != intraday.size:
        raise ValueError("pnl_usd / intraday_low length mismatch")

    h1_frame, h2_frame = split_at_boundary(frame, half_boundary_date)
    full = _run_partition(
        daily, intraday, firm_key=firm_key, thr=thr, label="full", n_sims=n_sims
    )
    h1 = _run_partition(
        h1_frame["pnl_usd"].to_numpy(dtype=float),
        _require_intraday(h1_frame),
        firm_key=firm_key,
        thr=thr,
        label="H1",
        n_sims=n_sims,
    )
    h2 = _run_partition(
        h2_frame["pnl_usd"].to_numpy(dtype=float),
        _require_intraday(h2_frame),
        firm_key=firm_key,
        thr=thr,
        label="H2",
        n_sims=n_sims,
    )
    verdict: NSurvVerdict = (
        "PASS" if (full.floor_ok and h1.floor_ok and h2.floor_ok) else "FAIL"
    )
    boundary = pd.Timestamp(half_boundary_date).normalize().date().isoformat()
    return NSurvReport(
        firm_key=firm_key,
        sizing_basis_usd=float(sizing_basis_usd),
        half_boundary_date=boundary,
        thresholds_source=thr.source_path,
        eval_bust_ceiling=float(thr.eval_bust_ceiling),
        pass_floor=float(thr.pass_floor),
        full=full,
        h1=h1,
        h2=h2,
        nsurv=verdict,
    )


def score_nsurv_from_path(
    path: Path | str,
    *,
    half_boundary_date: str | pd.Timestamp,
    firm_key: str = DEFAULT_FIRM_KEY,
    sizing_basis_usd: float = SIZING_BASIS_USD,
    thresholds: ScoringThresholds | None = None,
    n_sims: int | None = None,
) -> NSurvReport:
    """Load CSV/JSON then ``score_nsurv``."""
    return score_nsurv(
        load_candidate_daily_pnl(path),
        half_boundary_date=half_boundary_date,
        firm_key=firm_key,
        sizing_basis_usd=sizing_basis_usd,
        thresholds=thresholds,
        n_sims=n_sims,
    )


def default_prereg_path() -> Path:
    return (
        repo_root()
        / "docs"
        / "briefs"
        / "pre-registration"
        / "2026-07-13-prop-survivor-scoring-prereg.md"
    )


def w1_campaign_dir() -> Path:
    return (
        repo_root()
        / "lab"
        / "analysis"
        / "c1"
        / "class_s_c1_haircut_regime_remc_2026-07-16"
    )


def w1_published_pins(firm_key: str = DEFAULT_FIRM_KEY) -> dict:
    """Quote published W1 pins from the committed report JSON (do not re-derive)."""
    report_path = w1_campaign_dir() / "w1_intraday_both_halves_report.json"
    raw = json.loads(report_path.read_text(encoding="utf-8"))
    tier = raw["tiers"][firm_key]
    return {
        "arm": raw["arm"],
        "floor": raw["floor"],
        "full": {
            "headline_bust": tier["full"]["headline_bust"],
            "pass_rate": tier["full"]["pass_rate"],
        },
        "H1": {
            "headline_bust": tier["H1"]["headline_bust"],
            "pass_rate": tier["H1"]["pass_rate"],
        },
        "H2": {
            "headline_bust": tier["H2"]["headline_bust"],
            "pass_rate": tier["H2"]["pass_rate"],
        },
        "gate_pass_full_and_halves": tier["gate_pass_full_and_halves"],
        "panel_n_bdays": raw["panel_meta"]["n_bdays"],
        "panel_span": raw["panel_meta"]["panel_span"],
    }


def w1_panel_inputs_present() -> tuple[bool, Sequence[str]]:
    """Return (ok, missing_paths) for the gitignored W1 vendor panels + 15m bars."""
    root = repo_root()
    # Filenames pinned in the committed W1 report (panel_meta / intraday_coverage).
    report = json.loads(
        (w1_campaign_dir() / "w1_intraday_both_halves_report.json").read_text(
            encoding="utf-8"
        )
    )
    missing: list[str] = []
    for _leg, meta in report["panel_meta"]["legs"].items():
        path = root / "core" / "data" / "tv_exports" / "cme" / meta["file"]
        if not path.is_file():
            missing.append(str(path))
    for _leg, meta in report["intraday_coverage"]["legs"].items():
        path = root / "core" / "data" / "bar_data" / meta["bar_file"]
        if not path.is_file():
            missing.append(str(path))
    return (len(missing) == 0, missing)
