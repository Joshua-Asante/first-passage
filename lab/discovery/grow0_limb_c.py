"""GROW-0 Limb C -- marginal-planted-effect extension orchestration.

Frozen per docs/briefs/pre-registration/2026-08-24-grow-0-limb-c-marginal-effect-prereg.md
(design-frozen 2026-08-24; every literal below is pinned per that document's §2/§3/§4.2/§7/§9
item 4 -- copied verbatim, not re-derived here). This module holds Limb C's own orchestration
only: root seed, per-condition N-panel loop, ledger write, and the §6 CI/verdict computation --
it imports and calls the additively-extended grow0_dgp.draw_daily_pnl / grow0_scoring.run_panel
(both gained an optional, default-preserving ``edge_dollars`` kwarg per this prereg's §9 items
1-2) and reuses grow0_dgp.spawn_panel_streams / grow0_harness.assert_seed_diversity verbatim.
No DGP, scoring, or nomination logic is reimplemented here.

GROW-0's own frozen v3 prereg, its RESOLVED closure, and grow0_harness.py's own five branches
(root SeedSequence(20260822)) are untouched by this module -- Limb C spawns from a new, separate
root (SeedSequence(20260824), §7) and writes to a separate retry ledger
(discovery_manifests/grow0_limb_c_retry_ledger.jsonl), never grow0_retry_ledger.jsonl.

Design note Status is PROPOSED, not FROZEN: parameters are pinned as literals, but this design
has not itself been through an explicit operator GO on these specific numbers. Running this
module is the companion execution task named (but explicitly not built) by the design note's own
header and §9 -- do not conflate "the design note exists" with "the execution task was GO'd."
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from discovery.grow0_dgp import TRUE_EDGE_VARIANT_INDEX, spawn_panel_streams
from discovery.grow0_harness import FLOOR, assert_seed_diversity
from discovery.grow0_scoring import PanelResult, run_panel
from research_utils.repo_root import repo_root

# --- Frozen literals (design note §2/§3/§4.2/§7/§9 item 4 -- hardcoded, not re-derived) ---
LIMB_C_ROOT_SEED = 20260824  # dated per repo convention; a NEW, separate root from GROW-0's own
# 20260822 -- distinct SeedSequence entropy pool, no shared lineage (design note §7/§5).

AS_RUN_TARGET_SR = 1.8
AS_RUN_EDGE_DOLLARS = 28.5002
AS_RUN_N = 1150
AS_RUN_COMPOSITE_ESTIMATE = 0.9095  # closed-form planning estimate (§4.1) -- the §4.3 H's target
# value, NOT a measured result; see the falsifiable-H framing below.

BOUNDARY_TARGET_SR = 1.265  # = FLOOR exactly (z=0 boundary, POWER_MIN=0.50 admissible edge)
BOUNDARY_EDGE_DOLLARS = 19.9857
BOUNDARY_N = 1150
BOUNDARY_COMPOSITE_ESTIMATE = 0.4656  # closed-form planning estimate (§4.1) -- ditto.

Z_95 = 1.96  # Wilson CI z-value, §6 formula verbatim (same convention GROW-0's own §4 used).

RETRY_LEDGER_PATH = repo_root() / "discovery_manifests" / "grow0_limb_c_retry_ledger.jsonl"


@dataclass(frozen=True)
class ConditionSpec:
    label: str
    target_sr: float
    edge_dollars: float
    n: int
    composite_estimate: float


AS_RUN = ConditionSpec(
    label="as_run",
    target_sr=AS_RUN_TARGET_SR,
    edge_dollars=AS_RUN_EDGE_DOLLARS,
    n=AS_RUN_N,
    composite_estimate=AS_RUN_COMPOSITE_ESTIMATE,
)
BOUNDARY = ConditionSpec(
    label="boundary",
    target_sr=BOUNDARY_TARGET_SR,
    edge_dollars=BOUNDARY_EDGE_DOLLARS,
    n=BOUNDARY_N,
    composite_estimate=BOUNDARY_COMPOSITE_ESTIMATE,
)


def wilson_ci(count: int, n: int, z: float = Z_95) -> tuple[float, float, float]:
    """Wilson score interval at 95% confidence, design note §6 formula verbatim:

        center     = (p_hat + z^2/(2n)) / (1 + z^2/n)
        half-width = z/(1+z^2/n) * sqrt(p_hat(1-p_hat)/n + z^2/(4n^2))

    Returns (p_hat, lo, hi). n=0 -> (nan, nan, nan) (a conditional-denominator guard -- structurally
    near-impossible at N=1,150 given both conditions' own composite estimates, but guarded rather
    than assumed).
    """
    if n <= 0:
        return (float("nan"), float("nan"), float("nan"))
    p_hat = count / n
    denom = 1.0 + z * z / n
    center = (p_hat + z * z / (2 * n)) / denom
    half = (z / denom) * math.sqrt(p_hat * (1.0 - p_hat) / n + z * z / (4 * n * n))
    # Clip to [0, 1]: the formula is exact but floating-point cancellation at p_hat=0 (or 1) can
    # produce a lo (or hi) of order -1e-18 -- a probability cannot be negative, so this is a
    # display-only clamp, not a change to the interval's own mathematics.
    lo = max(0.0, center - half)
    hi = min(1.0, center + half)
    return (p_hat, lo, hi)


def _aggregate_condition(spec: ConditionSpec, results: list[PanelResult]) -> dict:
    """Pure aggregation over an already-drawn panel list (design note §6/§8) -- no drawing, no
    DGP/scoring/nomination logic; only the counting/CI/verdict arithmetic §9 item 3 scopes to
    this module ("ledger write, §4.3's CI-containment verdict computation"). Split out from
    ``run_condition`` so the population-scoping logic (the exact known-error-class GROW-0's own
    history warns about) can be unit-tested against hand-built fixtures, not only RNG-drawn panels.

    Per-panel outcomes (design note §8), all derived from the unmodified PanelResult fields:
      nominee == 5            -> selection correctness
      abandoned (gate a or b) -> on THIS population (true edge present in every panel by
                                 construction, §8), *any* abandonment is false-abandonment,
                                 unconditional on which variant won the argmax.
      clears                  -> only meaningful (non-False) when not abandoned.
    """
    n = len(results)
    nominee5_count = sum(1 for r in results if r.nominee == TRUE_EDGE_VARIANT_INDEX)
    gatespass_count = sum(
        1 for r in results if r.nominee == TRUE_EDGE_VARIANT_INDEX and not r.abandoned
    )
    clears_count = sum(
        1
        for r in results
        if r.nominee == TRUE_EDGE_VARIANT_INDEX and not r.abandoned and r.clears
    )
    accept_count = clears_count  # composite P(accept) = P(nominee=5) x P(gatespass|nominee5) x
    # P(clears|nominee5,gatespass) -- i.e. accept IFF nominee==5 AND gates passed AND confirm
    # cleared, the identical three-conjunct definition Limb A's own PASS uses
    # (_evaluate_limb_a_shaped_verdict in grow0_harness.py), never "any variant's confirm cleared."
    abandoned_count = sum(1 for r in results if r.abandoned)  # unconditional on nominee (§8) --
    # includes panels where a NULL variant won the argmax and was itself gated out, not only
    # panels where variant 5 was the (gated-out) nominee. Population-scoped per §8, not the same
    # denominator/numerator pair as gatespass_count above.

    p_nominee5 = wilson_ci(nominee5_count, n)
    p_gatespass = wilson_ci(gatespass_count, nominee5_count)
    p_clears = wilson_ci(clears_count, gatespass_count)
    p_accept = wilson_ci(accept_count, n)
    p_false_abandon = wilson_ci(abandoned_count, n)

    accept_lo, accept_hi = p_accept[1], p_accept[2]
    if math.isnan(accept_lo) or math.isnan(accept_hi):
        verdict = "DIVERGED"  # a degenerate CI cannot be said to contain the estimate
    else:
        verdict = (
            "CORROBORATED" if accept_lo <= spec.composite_estimate <= accept_hi else "DIVERGED"
        )

    return {
        "condition": spec.label,
        "target_sr": spec.target_sr,
        "edge_dollars": spec.edge_dollars,
        "n": n,
        "nominee_5_count": nominee5_count,
        "gates_pass_given_nominee5_count": gatespass_count,
        "confirm_clears_given_nominee5_gatespass_count": clears_count,
        "accept_count": accept_count,
        "abandoned_count": abandoned_count,
        "p_nominee5": {"point": p_nominee5[0], "lo": p_nominee5[1], "hi": p_nominee5[2]},
        "p_gatespass_given_nominee5": {
            "point": p_gatespass[0], "lo": p_gatespass[1], "hi": p_gatespass[2]
        },
        "p_clears_given_nominee5_gatespass": {
            "point": p_clears[0], "lo": p_clears[1], "hi": p_clears[2]
        },
        "p_accept": {"point": p_accept[0], "lo": p_accept[1], "hi": p_accept[2]},
        "p_false_abandonment": {
            "point": p_false_abandon[0], "lo": p_false_abandon[1], "hi": p_false_abandon[2]
        },
        "composite_estimate": spec.composite_estimate,
        "verdict": verdict,
    }


def run_condition(spec: ConditionSpec, condition_seq) -> dict:
    """Draws ``spec.n`` panels for one Limb C condition (design note §7) and aggregates them via
    ``_aggregate_condition``.

    ``edge_variant_index`` is always TRUE_EDGE_VARIANT_INDEX (variant 5 always carries this
    condition's own ``edge_dollars``, §7) -- the identical call shape GROW-0's own Limb A uses,
    just with a smaller planted effect and this condition's own N and seed branch. Reuses
    ``grow0_scoring.run_panel`` unmodified in logic (only the additive ``edge_dollars`` kwarg
    differs from a Limb-A-shaped call) -- no nomination/gate/confirm logic is reimplemented here.
    """
    panel_seqs = condition_seq.spawn(spec.n)
    results: list[PanelResult] = []
    leaves = []
    for panel_seq in panel_seqs:
        train_children, confirm_children = spawn_panel_streams(panel_seq, 10)
        leaves.extend(train_children)
        leaves.extend(confirm_children)
        result = run_panel(
            train_children,
            confirm_children,
            edge_variant_index=TRUE_EDGE_VARIANT_INDEX,
            floor=FLOOR,
            edge_dollars=spec.edge_dollars,
        )
        results.append(result)
    # Runtime diversity assertion (design note §7, reusing grow0_harness's own check verbatim):
    # train + confirm, 10 variants each -> N*20, matching Limb B's own n*20 convention.
    assert_seed_diversity(leaves, min_distinct=spec.n * 20)
    return _aggregate_condition(spec, results)


def append_retry_ledger(entry: dict, *, path: Path | None = None) -> None:
    """Append-only, one JSON line per Limb C invocation (design note §7) -- a separate file from
    GROW-0's own grow0_retry_ledger.jsonl, never commingled with it."""
    target = path if path is not None else RETRY_LEDGER_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def run_limb_c(
    *,
    run_id: str,
    started_at_arg: str,
    prereg_commit: str,
    ledger_path: Path | None = None,
) -> dict:
    """Runs both Limb C conditions (as-run, then boundary -- fixed order per design note §7) off
    a single new root SeedSequence(20260824), appends one ledger line covering both conditions,
    and returns the same dict."""
    root = np.random.SeedSequence(LIMB_C_ROOT_SEED)
    as_run_seq, boundary_seq = root.spawn(2)  # fixed order: (a) as-run, then (b) boundary

    as_run_result = run_condition(AS_RUN, as_run_seq)
    boundary_result = run_condition(BOUNDARY, boundary_seq)

    entry = {
        "run_id": run_id,
        "started_at_arg": started_at_arg,
        "prereg_commit": prereg_commit,
        "as_run": as_run_result,
        "boundary": boundary_result,
    }
    append_retry_ledger(entry, path=ledger_path)
    return entry


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="GROW-0 Limb C marginal-effect extension")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--started-at", required=True, help="ISO timestamp, caller-supplied")
    parser.add_argument(
        "--prereg-commit",
        required=True,
        help="commit hash pinning the frozen Limb C design note this run is authoritative against",
    )
    args = parser.parse_args(argv)

    result = run_limb_c(
        run_id=args.run_id,
        started_at_arg=args.started_at,
        prereg_commit=args.prereg_commit,
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
