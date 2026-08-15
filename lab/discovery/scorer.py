"""Stage-4 scorer — IS triage (cost-law + permutation p) + OOS matrix + low-n flag.

IS-only selection; OOS is evaluation-only. Low-n (≤250 OOS trades) is flagged
``dsr_unreachable_low_n: true`` and still emitted (never silently dropped).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from discovery.cost_mgc import hurdle_from_price, passes_cost_law
from discovery.motif_rules import FrozenRule, RuleEval, evaluate_rule

DSR_UNREACHABLE_N = 250  # ADR §6 / pre-reg §2 power disclosure


@dataclass
class ScoredCandidate:
    rule: FrozenRule
    is_eval: RuleEval
    oos_eval: RuleEval
    is_pvalue: float
    cost_law_pass: bool
    dsr_unreachable_low_n: bool
    mean_is_trade: float


@dataclass
class ScoreBundle:
    survivors: list[ScoredCandidate]
    killed_cost: list[ScoredCandidate] = field(default_factory=list)


def _perm_pvalue(
    trade_returns: list[float],
    *,
    n_perm: int = 200,
    seed: int = 0,
) -> float:
    """One-sided permutation p: P(mean_perm >= mean_obs) under sign flips."""
    x = np.asarray(trade_returns, dtype=float)
    if x.size < 2:
        return 1.0
    rng = np.random.default_rng(seed)
    obs = float(x.mean())
    if obs <= 0:
        return 1.0
    null = np.empty(n_perm, dtype=float)
    for i in range(n_perm):
        signs = rng.choice([-1.0, 1.0], size=x.size)
        null[i] = float((x * signs).mean())
    return float((np.sum(null >= obs) + 1) / (n_perm + 1))


def score_rules(
    rules: list[FrozenRule],
    series_is: np.ndarray,
    series_oos: np.ndarray,
    *,
    mgc_price: float = 1800.0,
    cost_frac_per_rt: float | None = None,
    n_perm: int = 200,
    seed: int = 0,
) -> ScoreBundle:
    """Score frozen rules on IS (triage) and OOS (matrix). Holdout unseen for selection."""
    hurdle = hurdle_from_price(mgc_price)
    cost = (
        float(cost_frac_per_rt)
        if cost_frac_per_rt is not None
        else float(hurdle.rt_cost_frac)
    )
    survivors: list[ScoredCandidate] = []
    killed: list[ScoredCandidate] = []
    for i, rule in enumerate(rules):
        is_ev = evaluate_rule(rule, series_is, cost_frac_per_rt=cost)
        oos_ev = evaluate_rule(rule, series_oos, cost_frac_per_rt=cost)
        mean_is = float(np.mean(is_ev.trade_returns)) if is_ev.trade_returns else 0.0
        cost_ok = passes_cost_law(mean_is, hurdle) if is_ev.n_trades else False
        p = _perm_pvalue(is_ev.trade_returns, n_perm=n_perm, seed=seed + i)
        low_n = oos_ev.n_trades <= DSR_UNREACHABLE_N
        cand = ScoredCandidate(
            rule=rule,
            is_eval=is_ev,
            oos_eval=oos_ev,
            is_pvalue=p,
            cost_law_pass=cost_ok,
            dsr_unreachable_low_n=low_n,
            mean_is_trade=mean_is,
        )
        if cost_ok and is_ev.n_trades > 0:
            survivors.append(cand)
        else:
            killed.append(cand)
    return ScoreBundle(survivors=survivors, killed_cost=killed)
