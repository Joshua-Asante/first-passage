"""Stage-2/4 campaign runner — Mine → Bind-K → Score → emit-matrix.

Template numbering (discovery-campaign-template.md):
  Stage 2 Mine · Stage 3 Bind-K · Stage 4 Score (IS)

Research-venv-only. Synthetic mode is the default until the operator authorizes
a real ``register_search open`` / ``db_fetch pull`` (DSR K/V ADR Accepted
2026-07-12 — spent limb). Real-campaign open is gated behind ``bind_real_k=True``.

Usage
-----
  PYTHONPATH=lab python -m discovery.stage24_runner --self-test
  PYTHONPATH=lab python -m discovery.stage24_runner --synthetic-e2e
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from discovery.k_count import DEFAULT_WINDOWS, KBracket, compute_k_bracket
from discovery.matrix_emit import emit_stage4, trade_matrix_for_gate
from discovery.miner import MotifHit, best_hit_distance_to_shape, mine_series
from discovery.motif_rules import (
    FrozenRule,
    freeze_rule_from_hit,
    freeze_rule_from_spec,
)
from discovery.scorer import ScoredCandidate, ScoreBundle, score_rules
from discovery.synthetic_bars import (
    MotifSpec,
    SyntheticBars,
    default_motif_shape,
    generate_synthetic_bars,
)
from research_utils.repo_root import repo_root
from research_utils.prereg_paths import DISC_CAMP_0_PREREG

# Campaign-scale T for the ~3,200 K_DSR bound (formula applied — not a bare K).
CAMPAIGN_SCALE_T = 52_000


@dataclass
class Stage24Result:
    bracket: KBracket
    artifacts: object
    survivors: list[ScoredCandidate]
    mine_hits: list[MotifHit]
    synthetic: SyntheticBars
    planted_recovered: bool


def _noise_rules(n: int, m: int, horizon: int, seed: int) -> list[FrozenRule]:
    """Decoy frozen rules (IS-shaped noise) so K_SPA > 1 for PBO."""
    rng = np.random.default_rng(seed)
    rules = []
    for i in range(n):
        shape = rng.normal(size=m)
        rules.append(
            freeze_rule_from_spec(
                shape,
                direction=1 if i % 2 == 0 else -1,
                horizon=horizon,
                trigger=0.5,  # tight — rarely fires / weak
                candidate_id=f"noise_{i:03d}",
                kind="motif",
            )
        )
    return rules


def run_synthetic_stage24(
    *,
    seed: int = 0,
    per_trade_sr: float = 0.30,
    max_oos_trades: int | None = 800,
    period: int = 40,
    m: int = 30,
    horizon: int = 3,
    n_noise: int = 4,
    out_dir: Path | None = None,
    run_id: str = "synthetic_stage24",
    bind_real_k: bool = False,
    use_miner_rule: bool = True,
    include_oracle_rule: bool = True,
    campaign_t_for_k: int | None = CAMPAIGN_SCALE_T,
    # Short eras keep STUMPY tractable in unit tests; campaign K still comes
    # from ``campaign_t_for_k`` via the ADR formula (never a bare hardcoded K).
    is_start: str = "2016-01-01",
    is_end: str = "2016-06-30",
    oos_start: str = "2019-05-06",
    oos_end: str = "2019-12-31",
) -> Stage24Result:
    """Full synthetic Mine→Score→emit path. Never opens a real campaign ledger."""
    if bind_real_k:
        raise RuntimeError(
            "bind_real_k requires ADR Accepted + operator go — refusing."
        )

    shape = default_motif_shape(m=m, seed=seed + 1)
    motif = MotifSpec(
        shape=shape,
        horizon=horizon,
        direction=1,
        per_trade_sr=per_trade_sr,
        trade_vol=0.01,
        period=period,
        max_oos_trades=max_oos_trades,
    )
    synth = generate_synthetic_bars(
        seed=seed,
        motif=motif,
        is_start=is_start,
        is_end=is_end,
        oos_start=oos_start,
        oos_end=oos_end,
    )
    bars = synth.bars
    hours = bars.index.hour.to_numpy()
    is_ret = bars["ret"].to_numpy()[synth.is_mask]
    is_hours = hours[synth.is_mask]
    oos_ret = bars["ret"].to_numpy()[synth.oos_mask]

    mine_hits: list[MotifHit] = []
    planted_recovered = False
    reg_is: np.ndarray | None = None
    if use_miner_rule:
        mine = mine_series(is_ret, hours=is_hours, windows=DEFAULT_WINDOWS)
        mine_hits = mine.hits
        reg_is = mine.regime_labels
        best, dist = best_hit_distance_to_shape(
            [h for h in mine.hits if h.m == m and h.kind == "motif"], shape
        )
        planted_recovered = best is not None and dist < 2.5
    else:
        best, dist = None, float("inf")

    rules: list[FrozenRule] = []
    if include_oracle_rule:
        # Oracle frozen from the planted shape (IS trigger calibrated on IS).
        from discovery.motif_rules import _rolling_z_distance

        dists = _rolling_z_distance(is_ret, shape)
        valid = dists[np.isfinite(dists)]
        trig = float(np.quantile(valid, 0.08)) if valid.size else 1.0
        rules.append(
            freeze_rule_from_spec(
                shape,
                direction=1,
                horizon=horizon,
                trigger=trig,
                candidate_id="planted_oracle",
                kind="motif",
            )
        )
    if use_miner_rule and best is not None:
        rules.append(
            freeze_rule_from_hit(
                best, is_ret, horizon=horizon, candidate_id="mined_motif"
            )
        )
    rules.extend(_noise_rules(n_noise, m=m, horizon=horizon, seed=seed + 9))

    bundle: ScoreBundle = score_rules(rules, is_ret, oos_ret, seed=seed)

    # K from campaign-scale T (formula), not a hardcoded bare integer.
    T_k = int(campaign_t_for_k if campaign_t_for_k is not None else synth.is_mask.sum())
    bracket = compute_k_bracket(T_k, DEFAULT_WINDOWS)

    out = Path(out_dir) if out_dir else (repo_root() / "discovery_manifests" / "synthetic")
    oos_ts = bars.index[synth.oos_mask]
    if reg_is is None:
        reg_oos = np.zeros(len(oos_ts), dtype=int)
    else:
        reg_oos = np.resize(reg_is, len(oos_ts))

    artifacts = emit_stage4(
        bundle.survivors,
        oos_ts,
        bracket,
        out_dir=out,
        run_id=run_id,
        regime_labels=reg_oos,
        era_bounds={
            "is": "2010-01-01:2018-12-31",
            "oos": "2019-05-06:2026-07-01",
        },
        cost_constants={"mgc_tick_value": 1.0, "v_rule": "1/n"},
        zero_benchmark=True,
        underlying_ret=oos_ret,
        dedrift=False,
    )
    return Stage24Result(
        bracket=bracket,
        artifacts=artifacts,
        survivors=bundle.survivors,
        mine_hits=mine_hits,
        synthetic=synth,
        planted_recovered=planted_recovered,
    )


def run_gate_on_survivors(
    survivors: list[ScoredCandidate],
    bracket: KBracket,
    *,
    thresholds,
    seed: int = 0,
    run_pbo: bool = True,
    reps: int = 200,
):
    """Invoke the REAL universe_gate with V=1/n pin (never the biased default)."""
    from research_utils.universe_gate import run_universe_gate

    if not survivors:
        raise ValueError("no survivors")
    # Prefer the oracle / best-n candidate for V.
    best = max(survivors, key=lambda s: s.oos_eval.n_trades)
    n = max(best.oos_eval.n_trades, 1)
    mat, bench, ids = trade_matrix_for_gate(survivors)
    return run_universe_gate(
        returns=mat,
        benchmark=bench,
        candidate_ids=ids,
        cumulative_k=bracket.k_dsr,
        thresholds=thresholds,
        var_trials=1.0 / n,
        seed=seed,
        run_pbo=run_pbo,
        reps=reps,
    )


def run_temporal_on_survivor(survivor: ScoredCandidate, timestamps, thresholds, labels=None):
    from research_utils.temporal_consistency import run_temporal_battery

    edge = np.asarray(survivor.oos_eval.bar_returns, dtype=float)
    # Map trade PnL onto calendar stamps already aligned to OOS bars.
    return run_temporal_battery(
        edge, list(map(str, timestamps)), thresholds, labels=labels, seed=0
    )


def _build_trade_only_bundle(
    *,
    n_trades: int,
    sr: float,
    vol: float,
    n_noise: int,
    seed: int,
    candidate_id: str,
) -> list[ScoredCandidate]:
    """Construct scored candidates with exact trade counts (gate power tests)."""
    from discovery.motif_rules import RuleEval

    rng = np.random.default_rng(seed)
    mean = sr * vol
    edge_tr = list(rng.normal(mean, vol, size=n_trades))
    rule = freeze_rule_from_spec(
        default_motif_shape(30, seed=3),
        direction=1,
        horizon=3,
        trigger=0.1,
        candidate_id=candidate_id,
    )
    is_tr = list(rng.normal(mean, vol, size=max(50, n_trades // 3)))
    primary = ScoredCandidate(
        rule=rule,
        is_eval=RuleEval(
            bar_returns=np.zeros(1),
            trade_returns=is_tr,
            entry_indices=[],
            n_trades=len(is_tr),
        ),
        oos_eval=RuleEval(
            bar_returns=np.zeros(1),
            trade_returns=edge_tr,
            entry_indices=[],
            n_trades=n_trades,
        ),
        is_pvalue=0.01,
        cost_law_pass=True,
        dsr_unreachable_low_n=n_trades <= 250,
        mean_is_trade=float(np.mean(is_tr)),
    )
    out = [primary]
    for i in range(n_noise):
        noise = list(rng.normal(0.0, vol, size=n_trades))
        nr = freeze_rule_from_spec(
            rng.normal(size=30),
            direction=1,
            horizon=3,
            trigger=0.1,
            candidate_id=f"noise_{i:03d}",
        )
        out.append(
            ScoredCandidate(
                rule=nr,
                is_eval=RuleEval(
                    bar_returns=np.zeros(1),
                    trade_returns=noise,
                    entry_indices=[],
                    n_trades=n_trades,
                ),
                oos_eval=RuleEval(
                    bar_returns=np.zeros(1),
                    trade_returns=noise,
                    entry_indices=[],
                    n_trades=n_trades,
                ),
                is_pvalue=0.5,
                cost_law_pass=True,
                dsr_unreachable_low_n=n_trades <= 250,
                mean_is_trade=0.0,
            )
        )
    return out


def synthetic_e2e_report(*, seed: int = 0) -> dict:
    """Campaign-K pos / low-n / neg discrimination via real universe_gate."""
    from research_utils.universe_gate import load_thresholds_from_prereg
    from research_utils.temporal_consistency import run_temporal_battery

    prereg = DISC_CAMP_0_PREREG
    thr = load_thresholds_from_prereg(prereg)
    bracket = compute_k_bracket(CAMPAIGN_SCALE_T)

    # --- positive: SR≈0.30, n≥750 → promote ---
    pos = _build_trade_only_bundle(
        n_trades=800, sr=0.30, vol=0.01, n_noise=4, seed=seed, candidate_id="pos_edge"
    )
    v_pos = run_gate_on_survivors(pos, bracket, thresholds=thr, seed=11)
    # Temporal battery on a synthetic year-balanced edge series.
    n_years = thr.consistency_years
    per = 30
    stamps = []
    for y in range(2019, 2019 + n_years):
        for i in range(per):
            stamps.append(f"{y}-06-{(i % 27) + 1:02d}")
    edge = np.full(n_years * per, 0.02)
    labels = np.array(["A", "B"] * (len(edge) // 2))
    if len(labels) < len(edge):
        labels = np.append(labels, "A")
    bat_pos = run_temporal_battery(edge, stamps, thr, labels=labels, seed=0, reps=200)

    # --- low-n: SR≈0.30, n≈150 → flagged + DSR fail (expected) ---
    low = _build_trade_only_bundle(
        n_trades=150, sr=0.30, vol=0.01, n_noise=4, seed=seed + 1, candidate_id="low_n"
    )
    assert low[0].dsr_unreachable_low_n is True
    v_low = run_gate_on_survivors(low, bracket, thresholds=thr, seed=12)

    # --- negative: pure noise ---
    neg = _build_trade_only_bundle(
        n_trades=800, sr=0.0, vol=0.01, n_noise=4, seed=seed + 2, candidate_id="noise_only"
    )
    # Force the "best" to be noise-like: zero mean primary.
    v_neg = run_gate_on_survivors(neg, bracket, thresholds=thr, seed=13)

    return {
        "k_dsr": bracket.k_dsr,
        "k_raw": bracket.k_raw,
        "positive_promote": bool(v_pos.promote),
        "positive_gates": dict(v_pos.gate_results),
        "positive_battery": bat_pos["overall"],
        "low_n_flag": True,
        "low_n_promote": bool(v_low.promote),
        "low_n_dsr_pass": bool(v_low.gate_results.get("dsr")),
        "negative_promote": bool(v_neg.promote),
        "negative_gates": dict(v_neg.gate_results),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Stage-2/4 discovery campaign runner.")
    ap.add_argument(
        "--synthetic-e2e",
        action="store_true",
        help="Run campaign-K pos/low-n/neg gate discrimination (offline).",
    )
    ap.add_argument(
        "--mine-synthetic",
        action="store_true",
        help="Run Mine→Score→emit on synthetic bars (no real ledger open).",
    )
    ap.add_argument("--out-dir", default=None)
    ap.add_argument("--run-id", default="synthetic_stage24")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument(
        "--bind-real-k",
        action="store_true",
        help="FORBIDDEN without ADR Accepted + operator go (always errors).",
    )
    args = ap.parse_args(argv)

    if args.synthetic_e2e:
        rep = synthetic_e2e_report(seed=args.seed)
        print(json.dumps(rep, indent=2))
        ok = (
            rep["positive_promote"]
            and rep["positive_battery"] == "PASS"
            and (not rep["low_n_promote"])
            and (not rep["low_n_dsr_pass"])
            and (not rep["negative_promote"])
        )
        print(f"[stage24] e2e discriminates: {ok}")
        return 0 if ok else 1

    if args.mine_synthetic:
        res = run_synthetic_stage24(
            seed=args.seed,
            out_dir=Path(args.out_dir) if args.out_dir else None,
            run_id=args.run_id,
            bind_real_k=args.bind_real_k,
        )
        print(
            f"[stage24] k_dsr={res.bracket.k_dsr} k_raw={res.bracket.k_raw} "
            f"k_spa={len(res.survivors)} planted_recovered={res.planted_recovered}"
        )
        print(f"[stage24] matrix -> {res.artifacts.matrix_csv}")
        return 0

    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
