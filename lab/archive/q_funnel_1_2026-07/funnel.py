"""Q-FUNNEL-1 funnel wrapper — fee / reset / funded-phase EV harness.

Implements the FROZEN pre-registration
``docs/briefs/pre-registration/Q-FUNNEL-1-verdict-preregistration.md``
as a sibling runner to ``run_haircut_regime_remc.py``: imports panel-build +
regime-gate primitives read-only; adds eval-fee / reset recursion + Select Flex
funded-payout accounting on top. No ``core/`` edits.

§0.5 resolutions (operator-confirmed 2026-07-21):
  A — busted-post-funding keeps prior payouts (no clawback)
  B — funded continuation draws from the same week-block-bootstrap panel
  C — winning-day counter is cycle-based (resets after each payout)
  D — edge de-meaning is per-leg before recombine
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Sequence

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[2]
_SCORING = _ROOT / "lab" / "analysis" / "class_s_candidate1_scoring_2026-07-15"
for _p in (_ROOT / "core", _ROOT / "lab", str(_SCORING), str(_HERE)):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from discovery.prop_survivor_scoring import (  # noqa: E402
    NO_PROTECTION_TRIGGER,
    DD_SCALE,
    blocks_from_daily_pnl,
    load_scoring_thresholds,
)
from mc.preflight import firm_kwargs  # noqa: E402
from mc.simulation import simulate_path  # noqa: E402
import run_class_s_c1_scoring as S  # noqa: E402
import run_class_s_c1_regime_gate as R  # noqa: E402

# ---------------------------------------------------------------------------
# Frozen pre-reg constants (literal — do not re-derive)
# ---------------------------------------------------------------------------
MAX_RETRIES = 5  # pre-reg §4
MATERIALITY_RELATIVE = 0.25  # pre-reg §3(a)
RUNGS = (0.25, 0.50, 1.00)
RETRY_POLICIES = ("no_retry", "retry_to_cap")
EDGE_SCENARIOS = ("edge_0", "edge_panel_historical", "edge_half_panel")
REGIME_HALVES = ("H1", "H2", "full")

FIRM_KEY = "Tradeify_Select_100K"
STARTING_BALANCE = 100_000.0
# Q-RAIL-1 Phase 4 — Tradeify Select cost-to-first-fill (list). Each attempt
# (initial + reset) costs EVAL_FEE_USD per pre-reg §2 spend formula.
EVAL_FEE_USD = 328.0
EVAL_FEE_PROMO_USD = 258.0  # logged; not the default pin
WORST_PLUS_RESET_USD = 681.0  # cross-tier contingency pin (logged)

# Select Flex 100K funded-payout config (pre-reg §5)
PROFIT_SPLIT_TRADER = 0.90
WINNING_DAY_THRESHOLD_USD = 200.0
WINNING_DAYS_PER_PAYOUT = 5
PAYOUT_PROFIT_FRACTION = 0.50
PAYOUT_CAP_USD = 4_000.0
DD_LOCK_TRIGGER_EQUITY = 103_100.0  # EOD first exceed → floor locks
DD_LOCK_FLOOR_USD = 100_100.0
FUNDED_HORIZON_DAYS = 252  # post-pass continuation cap (1y bdays)

# WATCH-1 0.50× ratification targets (haircut RESULTS.md)
WATCH1_FULL_BUST = 0.0008
WATCH1_H1_BUST = 0.0014
WATCH1_BOOT_BUST_95TH = 0.0077
WATCH1_PASS_5TH = 0.9576

# Reproduction tolerances (same as run_haircut_regime_remc._repro_check)
REPRO_H1_TOL_PP = 0.010
REPRO_BOOT95_TOL_PP = 0.020

RetryPolicy = Literal["no_retry", "retry_to_cap"]
EdgeScenario = Literal["edge_0", "edge_panel_historical", "edge_half_panel"]


@dataclass
class PayoutEvent:
    day_index: int
    request_usd: float
    trader_received_usd: float
    balance_after: float


@dataclass
class LineageResult:
    terminal_kind: str  # retries_exhausted | busted_eval | busted_post_funding | funded_horizon
    cumulative_spend: float
    cumulative_days: int
    payouts_total: float
    payouts: list[PayoutEvent] = field(default_factory=list)
    eval_attempts: int = 0
    eval_outcome: str | None = None

    @property
    def net_value(self) -> float:
        """Numerator contribution: Σ payouts − cumulative_spend (single subtraction).

        Interprets the pre-reg formula ``terminal_value − cumulative_spend`` with
        ``terminal_value = Σ realized payouts`` (resolution A: no clawback).
        """
        return self.payouts_total - self.cumulative_spend


@dataclass
class EvDayResult:
    ev_day: float
    mean_net: float
    mean_days: float
    n_lineages: int
    boot_5th: float
    boot_95th: float


# ---------------------------------------------------------------------------
# Panel / edge-scenario construction (sibling pattern)
# ---------------------------------------------------------------------------

def load_c1_panel() -> tuple[pd.DataFrame, dict, np.ndarray]:
    """Phase-0 verify + build scaled MYM+MNQ panel; return (panel_200k, meta, daily_100k)."""
    S.phase0_verify()
    for leg in S.C1_STRATS:
        S.resolve_panel_path(leg)
    panel, meta, _ = S.build_scaled_panel(
        S.C1_STRATS, S.C1_ALLOCS, expect_1r=dict(S.EXPECTED_1R)
    )
    daily = S.book_daily_at_100k(panel)
    return panel, meta, daily


def apply_edge_scenario(
    panel_200k: pd.DataFrame,
    scenario: EdgeScenario,
) -> np.ndarray:
    """Per-leg de-mean (resolution D), then book-sum at $100K band.

    edge_0             — each leg de-meaned to zero mean
    edge_half_panel    — each leg mean scaled to 0.5× historical
    edge_panel_historical — unmodified
    """
    scaled = panel_200k * (100_000.0 / float(S.ACCOUNT))
    if scenario == "edge_panel_historical":
        return scaled.sum(axis=1).to_numpy(dtype=float)

    out = scaled.copy()
    for col in out.columns:
        series = out[col].to_numpy(dtype=float)
        mu = float(series.mean())
        if scenario == "edge_0":
            out[col] = series - mu
        elif scenario == "edge_half_panel":
            out[col] = series - 0.5 * mu
        else:  # pragma: no cover
            raise ValueError(f"unknown edge scenario {scenario!r}")
    return out.sum(axis=1).to_numpy(dtype=float)


def regime_half_slice(daily: np.ndarray, half: str) -> np.ndarray:
    h1, h2, _ = R.half_panel_split(daily)
    if half == "H1":
        return h1
    if half == "H2":
        return h2
    if half == "full":
        return np.asarray(daily, dtype=float).reshape(-1)
    raise ValueError(f"unknown regime half {half!r}")


# ---------------------------------------------------------------------------
# Eval-path sampling (read-only reuse of simulate_path + week blocks)
# ---------------------------------------------------------------------------

def _eval_firm_kwargs() -> dict:
    cons = R._consistency_frac(FIRM_KEY)
    return firm_kwargs(FIRM_KEY, inactivity_off=True, consistency=cons)


def sample_path(
    blocks: np.ndarray,
    rng: np.random.Generator,
    horizon: int,
) -> np.ndarray:
    """Week-block bootstrap path — same mechanism as ``run_seed``."""
    n_blocks = len(blocks)
    blocks_per_sim = (horizon + 4) // 5
    indices = rng.integers(0, n_blocks, blocks_per_sim)
    return np.concatenate([blocks[i] for i in indices])[:horizon]


def _path_day_pnl(path: np.ndarray, day: int) -> float:
    return float(np.asarray(path[day]).sum())


def _remaining_daily_pnl(
    path: np.ndarray,
    pass_day: int,
    funded_horizon: int,
    blocks: np.ndarray,
    rng: np.random.Generator,
    haircut: float,
) -> np.ndarray:
    """Daily PnL series for funded continuation (same bootstrap draw, resolution B)."""
    need = int(funded_horizon)
    out: list[float] = []
    for d in range(pass_day, len(path)):
        out.append(_path_day_pnl(path, d))
        if len(out) >= need:
            return np.asarray(out[:need], dtype=float)
    extra = sample_path(blocks, rng, need - len(out) + 5) * float(haircut)
    for d in range(len(extra)):
        out.append(_path_day_pnl(extra, d))
        if len(out) >= need:
            break
    return np.asarray(out[:need], dtype=float)


def run_eval_on_path(path: np.ndarray, firm_kw: dict | None = None) -> tuple[str, int, float]:
    """Run frozen ``simulate_path``; return (outcome, days, end_equity_approx).

    End equity is recovered by replaying the scaled daily PnL under the same
    DD-protection schedule the engine uses (needed for funded handoff).
    """
    kw = firm_kw or _eval_firm_kwargs()
    horizon = len(path)
    outcome, days, _max_dd, _culprit = simulate_path(
        path,
        NO_PROTECTION_TRIGGER,
        DD_SCALE,
        horizon,
        **kw,
    )
    equity = _replay_equity(path, days, kw)
    return outcome, int(days), float(equity)


def _replay_equity(path: np.ndarray, days: int, kw: dict) -> float:
    """Replay daily PnL with the same dd_protection scale rule as simulate_path."""
    equity = float(kw["starting_equity"])
    peak = equity
    dd_trigger = NO_PROTECTION_TRIGGER
    dd_scale = DD_SCALE
    for day in range(min(days, len(path))):
        dd_from_peak = (equity - peak) / peak if peak > 0 else 0.0
        scale = dd_scale if round(dd_from_peak, 6) <= -dd_trigger else 1.0
        pnl = float(np.asarray(path[day]).sum() * scale)
        equity = equity + pnl
        if equity > peak:
            peak = equity
    return equity


# ---------------------------------------------------------------------------
# Fee / reset recursion (Step 2.2)
# ---------------------------------------------------------------------------

def attempt_spend(n_attempts: int, eval_fee: float = EVAL_FEE_USD) -> float:
    """cumulative_spend = eval_fee × (1 + resets) = eval_fee × n_attempts."""
    return float(eval_fee) * int(n_attempts)


def max_attempts(policy: RetryPolicy) -> int:
    if policy == "no_retry":
        return 1
    if policy == "retry_to_cap":
        return 1 + MAX_RETRIES  # original + 5 resets
    raise ValueError(f"unknown retry policy {policy!r}")


# ---------------------------------------------------------------------------
# Funded-phase continuation (Step 2.3) — resolution B/C
# ---------------------------------------------------------------------------

def compute_payout_request(balance: float, starting: float = STARTING_BALANCE) -> float:
    """Select Flex: min(50% of total profit, $4,000)."""
    total_profit = balance - starting
    if total_profit <= 0:
        return 0.0
    return float(min(PAYOUT_PROFIT_FRACTION * total_profit, PAYOUT_CAP_USD))


def trader_receives(request_usd: float) -> float:
    return float(PROFIT_SPLIT_TRADER * request_usd)


def simulate_funded_phase(
    daily_returns: Sequence[float],
    *,
    start_equity: float,
    start_peak: float | None = None,
    starting_balance: float = STARTING_BALANCE,
    floor_locked: bool = False,
    max_dd_usd: float = 3_000.0,
    lock_offset: float = 100.0,
) -> tuple[str, float, list[PayoutEvent], int]:
    """Continue past eval ``pass`` with Select Flex payout policy.

    Returns (terminal_kind, payouts_total, payout_events, days_used).
    terminal_kind: funded_horizon | busted_post_funding
    """
    equity = float(start_equity)
    peak = float(start_peak if start_peak is not None else start_equity)
    locked = bool(floor_locked)
    # Pre-lock trailing floor uses engine formula; once triggered, floor = DD_LOCK_FLOOR.
    winning_days = 0
    cycle_pnl = 0.0  # net P&L since last payout (loss-recovery rule)
    payouts: list[PayoutEvent] = []
    payouts_total = 0.0
    first_payout_done = False

    for i, raw in enumerate(daily_returns):
        pnl = float(raw)
        equity_new = equity + pnl

        # Trailing-locking floor (eval geometry continues; lock freezes floor).
        if locked:
            floor = DD_LOCK_FLOOR_USD
        else:
            floor = min(peak - max_dd_usd, starting_balance + lock_offset)
            if equity_new > DD_LOCK_TRIGGER_EQUITY:
                locked = True
                floor = DD_LOCK_FLOOR_USD

        if round((equity_new - floor) / starting_balance, 6) <= 0.0:
            return "busted_post_funding", payouts_total, payouts, i + 1

        equity = equity_new
        if equity > peak:
            peak = equity

        cycle_pnl += pnl
        if pnl >= WINNING_DAY_THRESHOLD_USD:
            winning_days += 1

        # Payout eligibility: 5 winning days in cycle; after first, require cycle net > 0.
        if winning_days >= WINNING_DAYS_PER_PAYOUT:
            if first_payout_done and cycle_pnl <= 0:
                continue
            request = compute_payout_request(equity, starting_balance)
            if request <= 0:
                continue
            received = trader_receives(request)
            equity -= request
            # Peak does not ratchet down on withdrawal (EOD peak is pre-payout high).
            payouts.append(
                PayoutEvent(
                    day_index=i + 1,
                    request_usd=request,
                    trader_received_usd=received,
                    balance_after=equity,
                )
            )
            payouts_total += received
            first_payout_done = True
            winning_days = 0  # resolution C — cycle reset
            cycle_pnl = 0.0

    return "funded_horizon", payouts_total, payouts, len(daily_returns)


# ---------------------------------------------------------------------------
# Lineage simulation (eval retries + funded)
# ---------------------------------------------------------------------------

def simulate_lineage(
    blocks: np.ndarray,
    rng: np.random.Generator,
    *,
    policy: RetryPolicy,
    haircut: float,
    eval_fee: float = EVAL_FEE_USD,
    eval_horizon: int = 1500,
    funded_horizon: int = FUNDED_HORIZON_DAYS,
    fund_payouts: bool = True,
) -> LineageResult:
    """One full funnel lineage under a retry policy.

    ``haircut`` multiplies daily path PnL (book-level lifecycle rung).
    ``fund_payouts=False`` zeros funded value (regression / fees-only modes).
    """
    firm_kw = _eval_firm_kwargs()
    max_att = max_attempts(policy)
    total_days = 0
    attempts = 0

    for _ in range(max_att):
        attempts += 1
        path = sample_path(blocks, rng, eval_horizon + funded_horizon)
        path = path * float(haircut)
        outcome, days, equity = run_eval_on_path(path, firm_kw)
        total_days += days

        if outcome.startswith("bust") or outcome == "horizon_cap":
            if attempts >= max_att or policy == "no_retry":
                spend = attempt_spend(attempts, eval_fee)
                kind = "busted_eval" if outcome.startswith("bust") else "retries_exhausted"
                if policy == "retry_to_cap" and attempts >= max_att:
                    kind = "retries_exhausted"
                return LineageResult(
                    terminal_kind=kind,
                    cumulative_spend=spend,
                    cumulative_days=total_days,
                    payouts_total=0.0,
                    eval_attempts=attempts,
                    eval_outcome=outcome,
                )
            continue  # retry-to-cap: burn another attempt

        # pass → funded continuation on remaining path days (resolution B)
        if not fund_payouts:
            spend = attempt_spend(attempts, eval_fee)
            return LineageResult(
                terminal_kind="funded_horizon",
                cumulative_spend=spend,
                cumulative_days=total_days,
                payouts_total=0.0,
                eval_attempts=attempts,
                eval_outcome="pass",
            )

        rem_pnl = _remaining_daily_pnl(
            path, days, funded_horizon, blocks, rng, haircut
        )
        peak = max(float(firm_kw["starting_equity"]), equity)
        term, pay_total, events, fund_days = simulate_funded_phase(
            rem_pnl,
            start_equity=equity,
            start_peak=peak,
        )
        total_days += fund_days
        spend = attempt_spend(attempts, eval_fee)
        return LineageResult(
            terminal_kind=term,
            cumulative_spend=spend,
            cumulative_days=total_days,
            payouts_total=pay_total if fund_payouts else 0.0,
            payouts=events,
            eval_attempts=attempts,
            eval_outcome="pass",
        )

    spend = attempt_spend(attempts, eval_fee)
    return LineageResult(
        terminal_kind="retries_exhausted",
        cumulative_spend=spend,
        cumulative_days=total_days,
        payouts_total=0.0,
        eval_attempts=attempts,
        eval_outcome=None,
    )


def ev_day_from_lineages(
    lineages: Sequence[LineageResult],
    *,
    n_boot: int = 200,
    boot_seed: int = 20260721,
) -> EvDayResult:
    """Frozen EV/day formula + bootstrap 5th–95th bands on lineage nets/days."""
    if not lineages:
        raise ValueError("ev_day_from_lineages: empty lineages")
    nets = np.array([L.net_value for L in lineages], dtype=float)
    days = np.array([max(L.cumulative_days, 1) for L in lineages], dtype=float)
    mean_net = float(nets.mean())
    mean_days = float(days.mean())
    ev = mean_net / mean_days

    rng = np.random.default_rng(boot_seed)
    n = len(lineages)
    boot_ev = np.empty(n_boot, dtype=float)
    for i in range(n_boot):
        idx = rng.integers(0, n, n)
        boot_ev[i] = float(nets[idx].mean() / days[idx].mean())
    return EvDayResult(
        ev_day=ev,
        mean_net=mean_net,
        mean_days=mean_days,
        n_lineages=n,
        boot_5th=float(np.percentile(boot_ev, 5)),
        boot_95th=float(np.percentile(boot_ev, 95)),
    )


def run_cell(
    daily: np.ndarray,
    *,
    rung: float,
    policy: RetryPolicy,
    n_lineages: int = 500,
    seed: int = 42,
    eval_fee: float = EVAL_FEE_USD,
    fund_payouts: bool = True,
    eval_horizon: int | None = None,
) -> EvDayResult:
    """One (rung × retry × already-sliced daily) EV/day cell."""
    thr = load_scoring_thresholds(S.GATE_PREREG)
    horizon = int(eval_horizon if eval_horizon is not None else thr.horizon)
    blocks = blocks_from_daily_pnl(daily)
    rng = np.random.default_rng(seed)
    lineages = [
        simulate_lineage(
            blocks,
            rng,
            policy=policy,
            haircut=float(rung),
            eval_fee=eval_fee,
            eval_horizon=horizon,
            fund_payouts=fund_payouts,
        )
        for _ in range(n_lineages)
    ]
    return ev_day_from_lineages(lineages)


# ---------------------------------------------------------------------------
# Regression pin — fees=0, funded_value=0, retry=never → WATCH-1 bust/pass
# ---------------------------------------------------------------------------

def watch1_regression_metrics(
    *,
    n_sims: int | None = None,
    n_panels: int = 100,
    n_jobs: int = -1,
    include_bootstrap: bool = True,
) -> dict:
    """Reproduce WATCH-1 0.50× regime metrics via sibling regime-gate primitives.

    fees/funded/retry are structurally absent here — this is the bust/pass
    regression surface the funnel must not alter (Step 2.5).
    """
    _panel, meta, daily = load_c1_panel()
    dh = daily * 0.50
    thr = load_scoring_thresholds(S.GATE_PREREG)
    tiers = (FIRM_KEY,)
    full = R.full_panel_reference(dh, thr, n_sims=n_sims, tiers=tiers)
    half = R.part_b_half_panel(dh, thr, n_sims=n_sims, tiers=tiers)
    out = {
        "panel_meta": meta,
        "full_panel_bust": float(full[FIRM_KEY]["headline_bust"]),
        "full_panel_pass": float(full[FIRM_KEY]["pass_rate"]),
        "H1_bust": float(half["tiers"][FIRM_KEY]["H1"]["headline_bust"]),
        "H1_pass": float(half["tiers"][FIRM_KEY]["H1"]["pass_rate"]),
        "H2_bust": float(half["tiers"][FIRM_KEY]["H2"]["headline_bust"]),
        "H2_pass": float(half["tiers"][FIRM_KEY]["H2"]["pass_rate"]),
    }
    if include_bootstrap:
        boot = R.part_a_bootstrap(
            dh, thr, n_panels=n_panels, n_sims=n_sims, n_jobs=n_jobs, tiers=tiers
        )
        t = boot["tiers"][FIRM_KEY]
        out["boot_bust_95th"] = float(t["bust_95th"])
        out["boot_pass_5th"] = float(t["pass_5th"])
    return out


def smoke_repro_1p00(
    *,
    n_sims: int | None = None,
    n_panels: int = 5,
    include_bootstrap: bool = False,
) -> dict:
    """Step 2.1 — 1.00× reproduction control vs REGIME_GATE baseline tolerances.

    ``n_sims=None`` uses the frozen thr default (10k×3) so H1 matches the
    seeded baseline to the basis point; low-n smoke draws are too noisy for
    the ≤1pp band (observed 5.67% vs 4.37% at n=200).
    """
    _panel, _meta, daily = load_c1_panel()
    thr = load_scoring_thresholds(S.GATE_PREREG)
    tiers = (FIRM_KEY,)
    half = R.part_b_half_panel(daily, thr, n_sims=n_sims, tiers=tiers)
    h1 = float(half["tiers"][FIRM_KEY]["H1"]["headline_bust"])
    exp_h1 = 0.0437
    exp_b95 = 0.1037
    out = {
        "H1_bust": h1,
        "H1_baseline": exp_h1,
        "boot95_baseline": exp_b95,
        "ok": abs(h1 - exp_h1) <= REPRO_H1_TOL_PP,
    }
    if include_bootstrap:
        boot = R.part_a_bootstrap(
            daily, thr, n_panels=n_panels, n_sims=n_sims, n_jobs=1, tiers=tiers
        )
        b95 = float(boot["tiers"][FIRM_KEY]["bust_95th"])
        out["boot_bust_95th"] = b95
        out["ok"] = out["ok"] and abs(b95 - exp_b95) <= REPRO_BOOT95_TOL_PP
    return out


# ---------------------------------------------------------------------------
# Gate application (pre-reg §6 — mechanical)
# ---------------------------------------------------------------------------

def bands_overlap(a_lo: float, a_hi: float, b_lo: float, b_hi: float) -> bool:
    return not (a_hi < b_lo or b_hi < a_lo)


def materiality_pair(
    better: EvDayResult,
    worse: EvDayResult,
) -> dict:
    """§3(a)+(b) for one ordered pair (caller supplies which is better by point est)."""
    if worse.ev_day == 0:
        rel = float("inf") if better.ev_day > 0 else 0.0
    else:
        rel = (better.ev_day - worse.ev_day) / abs(worse.ev_day)
    econ = rel >= MATERIALITY_RELATIVE
    stat = not bands_overlap(
        better.boot_5th, better.boot_95th, worse.boot_5th, worse.boot_95th
    )
    return {
        "relative_lift": rel,
        "economic_ok": econ,
        "statistical_ok": stat,
        "pair_ok": econ and stat,
    }


def apply_section6_gate(cells: dict) -> dict:
    """Mechanical §6 readout over cells keyed (rung, policy, edge, half) → EvDayResult.

    RESOLVED iff §3(a)+(b)+(c) hold at ≥1 edge-scenario grid point across rungs.
    FALSIFIED iff no grid point clears (a)+(b).
    AMBIGUOUS-HOLD iff (a)+(b) hold somewhere but (c) fails (H1↔H2 direction flip).
    """
    edges = EDGE_SCENARIOS
    policies = RETRY_POLICIES
    resolved_points = []
    ambiguous_points = []

    for edge in edges:
        for policy in policies:
            # Compare rungs on H1 and H2 separately for (c)
            for half in ("H1", "H2"):
                pass  # direction checked below across halves

            # Find best vs worst rung by full-panel (or mean of halves) point EV
            # Materiality is judged per half; (c) requires same-sign across halves.
            lifts_h1 = _best_vs_worst_lift(cells, edge, policy, "H1")
            lifts_h2 = _best_vs_worst_lift(cells, edge, policy, "H2")
            if lifts_h1 is None or lifts_h2 is None:
                continue
            ab_h1 = lifts_h1["pair_ok"]
            ab_h2 = lifts_h2["pair_ok"]
            same_sign = lifts_h1["better_rung"] == lifts_h2["better_rung"]
            if ab_h1 and ab_h2 and same_sign:
                resolved_points.append(
                    {
                        "edge": edge,
                        "policy": policy,
                        "better_rung": lifts_h1["better_rung"],
                        "H1": lifts_h1,
                        "H2": lifts_h2,
                    }
                )
            elif (ab_h1 or ab_h2) and not same_sign:
                ambiguous_points.append(
                    {
                        "edge": edge,
                        "policy": policy,
                        "H1_better": lifts_h1["better_rung"],
                        "H2_better": lifts_h2["better_rung"],
                        "H1": lifts_h1,
                        "H2": lifts_h2,
                    }
                )
            elif ab_h1 and ab_h2 and not same_sign:
                ambiguous_points.append(
                    {
                        "edge": edge,
                        "policy": policy,
                        "reason": "direction_reverses_H1_H2",
                        "H1": lifts_h1,
                        "H2": lifts_h2,
                    }
                )

    if resolved_points:
        verdict = "RESOLVED"
    elif ambiguous_points:
        verdict = "AMBIGUOUS-HOLD"
    else:
        verdict = "FALSIFIED"

    return {
        "verdict": verdict,
        "resolved_points": resolved_points,
        "ambiguous_points": ambiguous_points,
        "materiality_relative": MATERIALITY_RELATIVE,
        "max_retries": MAX_RETRIES,
    }


def _best_vs_worst_lift(cells: dict, edge: str, policy: str, half: str) -> dict | None:
    keyed = []
    for rung in RUNGS:
        key = (rung, policy, edge, half)
        if key not in cells:
            return None
        keyed.append((rung, cells[key]))
    keyed.sort(key=lambda x: x[1].ev_day, reverse=True)
    best_rung, best = keyed[0]
    worst_rung, worst = keyed[-1]
    if best_rung == worst_rung:
        return {
            "better_rung": best_rung,
            "worse_rung": worst_rung,
            "pair_ok": False,
            "relative_lift": 0.0,
            "economic_ok": False,
            "statistical_ok": False,
        }
    m = materiality_pair(best, worst)
    return {
        "better_rung": best_rung,
        "worse_rung": worst_rung,
        **m,
        "better_ev": best.ev_day,
        "worse_ev": worst.ev_day,
    }
