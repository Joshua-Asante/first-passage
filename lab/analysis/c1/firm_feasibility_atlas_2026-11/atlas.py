"""Firm feasibility atlas: grid, synthetic generator, tier configs and the T3 lookup.

Design (frozen before any run): DESIGN.md in this directory. Synthetic streams only (K = 0).
The engine is ``core.mc.simulation.simulate_path``, called unmodified per path; firm geometry
comes only from ``core.mc.preflight.firm_kwargs`` over ``core.firm_rules``.
"""
from __future__ import annotations

import csv
import itertools
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ATLAS_CSV = HERE / "atlas.csv"

# Grid (DESIGN.md "Grid"). Row-major order over this tuple defines the shape index and seed.
RISK_FRACS = (0.05, 0.10, 0.15, 0.25, 0.33)
EXPECTANCIES = (0.00, 0.05, 0.10, 0.20)
WIN_RATES = (0.35, 0.50, 0.65)
TRADES_PER_SESSION = (0.25, 1.0, 3.0)
MAE_PROFILES = {"tight": (0.0, 0.3), "mid": (0.2, 0.6), "deep": (0.5, 0.95)}
MAE_ORDER = ("tight", "mid", "deep")

HORIZON = 1500          # HORIZON_CAP, asserted against the engine in run_atlas
PATHS = 1000
SEED_BASE = 20261104
DD_TRIGGER, DD_SCALE = 10.0, 1.0   # fixed size, no protection (gate-5h idiom)
UNREACHABLE_LOCK = 1_000_000.0      # trailing_locking with no lock = pure fixed-$ trail
PASS_WINDOWS = (22, 63)             # bdays: ~30 calendar days (Bulenox access, D14), ~1 quarter

# Reliability marks, decided before results (DESIGN.md "Reliability by tier").
MARKS = {
    "tradeify": "HIGH",
    "myfundedfutures": "MEDIUM",
    "blusky": "MEDIUM",
    "fxify_futures": "PROVISIONAL",
    "bulenox": "EXCLUDED",
}
MARK_REASONS = {
    "HIGH": "fixed-$ EOD ratchet with intraday breach matches the venue rule (register I.2)",
    "MEDIUM": "engine-vs-venue gap bounded by a paired sensitivity run (register A2.1 / F2)",
    "PROVISIONAL": "row is provisional (fees, capture unverified; register A1.7, row hold)",
    "EXCLUDED": ("venue trails the intraday high including open positions; engine ratchets on "
                 "the EOD close (register A1.1, severity H): bust is a lower bound of unknown size"),
}


@dataclass(frozen=True)
class Shape:
    f: float      # risk per trade as a fraction of the tier's drawdown allowance
    e: float      # expectancy per trade, R, net of costs
    p: float      # win rate
    lam: float    # mean trades per session (Poisson)
    mae: str      # winner adverse-excursion profile

    @property
    def payoff(self) -> float:
        """Winner size in R so that p*b - (1-p) == e."""
        return (self.e + 1.0 - self.p) / self.p


def shapes() -> list[Shape]:
    return [Shape(*t) for t in itertools.product(
        RISK_FRACS, EXPECTANCIES, WIN_RATES, TRADES_PER_SESSION, MAE_ORDER)]


def generate(e: float, p: float, lam: float, mae: str, n_paths: int, horizon: int,
             seed: int) -> tuple[np.ndarray, np.ndarray]:
    """(daily_pnl, intraday_low) in R, each shaped (n_paths, horizon).

    Trades run in sequence inside a day. intraday_low is the day's lowest point relative to its
    open: min(0, min_i(cum_before_i - mae_i)); a loser's mae is its full 1R stop.
    """
    if not 0.0 < p < 1.0:
        raise ValueError(f"win rate must be in (0, 1): {p}")
    b = (e + 1.0 - p) / p
    if b <= 0.0:
        raise ValueError(f"derived payoff must be positive: {b}")
    lo, hi = MAE_PROFILES[mae]
    rng = np.random.default_rng(seed)
    counts = rng.poisson(lam, size=n_paths * horizon)
    total = int(counts.sum())
    win = rng.random(total) < p
    r = np.where(win, b, -1.0)
    excursion = np.where(win, rng.uniform(lo, hi, total), 1.0)
    pnl = np.zeros(n_paths * horizon)
    low = np.zeros(n_paths * horizon)
    active = counts > 0
    if total:
        # Sum within each day only, trade by trade (no global running sum: its float drift
        # let a day's low sit above its close).
        first = (np.cumsum(counts) - counts)[active]
        n_day = counts[active]
        cum = np.zeros(len(first))
        day_low = np.zeros(len(first))
        for k in range(int(n_day.max())):
            sel = n_day > k
            t = first[sel] + k
            day_low[sel] = np.minimum(day_low[sel], cum[sel] - excursion[t])
            cum[sel] += r[t]
        pnl[active] = cum
        low[active] = day_low
    return pnl.reshape(n_paths, horizon), low.reshape(n_paths, horizon)


# ---------------------------------------------------------------------------------------------
# Configs


@dataclass(frozen=True)
class Config:
    name: str          # unique config id
    tier: str          # FIRM_RULES key
    family: str        # AUTOMATION_FRIENDLY_PROP_FIRMS key
    variant: str       # "row" or the named sensitivity
    consistency: float | None
    fixed_dollar_trail: bool = False

    @property
    def mark(self) -> str:
        return MARKS[self.family]


def configs(firm_rules: dict, families: dict) -> list[Config]:
    """Every tier at its row's consistency, plus the DESIGN.md sensitivities."""
    out: list[Config] = []
    for family, tiers in families.items():
        for tier in tiers:
            pct = firm_rules[tier].get("consistency_rule_pct")
            cons = None if pct is None else pct / 100.0
            out.append(Config(tier, tier, family, "row", cons))
            if family == "myfundedfutures":
                out.append(Config(f"{tier}@cons0.30", tier, family, "consistency 0.30 (A2.1)", 0.30))
            if family == "blusky":
                out.append(Config(f"{tier}@fixed$", tier, family, "fixed-$ trail (F2)", cons, True))
    return out


def engine_kwargs(cfg: Config, firm_kwargs) -> dict:
    kw = firm_kwargs(cfg.tier, inactivity_off=True, consistency=cfg.consistency,
                     allow_provisional_rules=(cfg.mark == "PROVISIONAL"))
    if cfg.fixed_dollar_trail:
        if kw["dd_type"] != "trailing":
            raise ValueError(f"{cfg.name}: fixed-$ twin only applies to a %-of-peak trail")
        kw = {**kw, "dd_type": "trailing_locking", "dd_lock_offset_usd": UNREACHABLE_LOCK}
    return kw


def dd_allowance(kw: dict) -> float:
    return -kw["trailing_dd_pct"] * kw["starting_equity"] if kw.get("trailing_dd_pct") is not None \
        else -kw["static_dd_pct"] * kw["starting_equity"]


# ---------------------------------------------------------------------------------------------
# T3 lookup

_NUMERIC_AXES = (("e", EXPECTANCIES), ("p", WIN_RATES), ("lam", TRADES_PER_SESSION),
                 ("f", RISK_FRACS))
_MAE_MEANS = {k: sum(v) / 2 for k, v in MAE_PROFILES.items()}  # tight .15, mid .40, deep .725


class Refused(ValueError):
    """The atlas cannot answer this query; the reason says why. Never extrapolated."""


def _bracket(name: str, v: float, grid: tuple) -> list:
    if any(math.isclose(v, g, abs_tol=1e-9) for g in grid):
        return [min(grid, key=lambda g: abs(g - v))]
    if not grid[0] < v < grid[-1]:
        raise Refused(f"{name}={v} is outside the atlas grid {grid}; no extrapolation")
    i = next(k for k, g in enumerate(grid) if g > v)
    return [grid[i - 1], grid[i]]


def _mae_bracket(mae) -> list[str]:
    if isinstance(mae, str):
        if mae not in MAE_PROFILES:
            raise Refused(f"unknown MAE profile {mae!r}; expected one of {MAE_ORDER}")
        return [mae]
    means = [_MAE_MEANS[k] for k in MAE_ORDER]
    picked = _bracket("mae_mean_R", float(mae), tuple(means))
    return [MAE_ORDER[means.index(m)] for m in picked]


def load(path: Path = ATLAS_CSV) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    num = ("f", "e", "p", "lam", "pass", "bust", "unresolved", "ttp_p50", "ttp_p90",
           "p_pass_22", "p_pass_63", "se_pass", "se_bust")
    for r in rows:
        for k in num:
            r[k] = float(r[k]) if r[k] not in ("", "nan") else math.nan
    return rows


def lookup(tier: str, *, expectancy_r: float, win_rate: float, trades_per_session: float,
           risk_frac: float, mae="mid", rows: list[dict] | None = None,
           include_lower_bound: bool = False) -> dict:
    """Worst-case atlas reading for one tier at a dossier's shape priors.

    Each numeric axis is bracketed by its grid neighbours (exact grid values are used as is);
    ``mae`` is a profile name or the winners' mean adverse excursion in R. Every config of the
    tier (row plus sensitivities) and every bracketing corner is read, and the worst value of
    each output is returned: max bust, min pass, max time-to-pass. EXCLUDED tiers are refused
    unless ``include_lower_bound`` is set, and then bust is labelled a lower bound.
    """
    rows = load() if rows is None else rows
    mine = [r for r in rows if r["tier"] == tier]
    if not mine:
        raise Refused(f"{tier!r} is not in the atlas")
    mark = mine[0]["mark"]
    if mark == "EXCLUDED" and not include_lower_bound:
        raise Refused(f"{tier}: EXCLUDED — {MARK_REASONS['EXCLUDED']}")
    q = {"e": expectancy_r, "p": win_rate, "lam": trades_per_session, "f": risk_frac}
    brackets = {k: _bracket(k, float(q[k]), g) for k, g in _NUMERIC_AXES}
    maes = _mae_bracket(mae)
    corners = []
    for e, p, lam, f, m in itertools.product(brackets["e"], brackets["p"], brackets["lam"],
                                             brackets["f"], maes):
        hit = [r for r in mine if math.isclose(r["e"], e) and math.isclose(r["p"], p)
               and math.isclose(r["lam"], lam) and math.isclose(r["f"], f) and r["mae"] == m]
        if not hit:
            raise Refused(f"{tier}: atlas row missing for e={e} p={p} lam={lam} f={f} mae={m}")
        corners.extend(hit)

    def worst(key, fn):
        vals = [r[key] for r in corners if not math.isnan(r[key])]
        return fn(vals) if vals else math.nan

    out = {
        "tier": tier, "mark": mark, "mark_reason": MARK_REASONS[mark],
        "configs": sorted({r["config"] for r in corners}),
        "snapped": {**brackets, "mae": maes}, "corners_read": len(corners),
        "pass": worst("pass", min), "bust": worst("bust", max),
        "unresolved": worst("unresolved", max),
        "bust_upper_at_horizon": worst("bust", max) + worst("unresolved", max),
        "ttp_p50": worst("ttp_p50", max), "ttp_p90": worst("ttp_p90", max),
        "p_pass_22": worst("p_pass_22", min), "p_pass_63": worst("p_pass_63", min),
        "horizon_bdays": HORIZON,
        "label": "synthetic atlas reading (K = 0); a screen, not a verdict",
    }
    if mark == "EXCLUDED":
        out["bust_is_lower_bound"] = True
    return out
