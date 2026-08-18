"""Q-FILLTAX-1 V2 mutation battery — FROZEN 2026-08-18 (Pre-Q Track V2 Phase 1).

Each row applies one named Pine<->Python parity defect class to a synthetic
TV-anchor baseline and asserts the Gen-2 parity gate (parity_gate.py) detects
it (FAIL) on the correct diagnostic axis. A row that stays ADMIT means the
gate is not trustworthy for that defect class — fix the gate, never weaken
the battery (H-V2, Q-FILLTAX-1 SS4). One companion row (M8) asserts a
near-identical pair still ADMITs, proving detection above isn't achieved by
an always-FAIL gate.

Verdict rule (Q-FILLTAX-1 SS6): 100% detection (M1-M7 all FAIL) AND 0 false
passes (M8 ADMITs) -> RESOLVED, land as the standing local pre-commit /
`make validate` gate. Any miss -> FALSIFIED, repair the harness (never the
tolerance), re-run.

This battery is synthetic-only — it proves the harness's discriminating
power, not any real family's parity. It does not grant engine research
authority for any strategy family (Phase 2, still owed: first family TV
anchor, operator).

Freeze doc: docs/briefs/pre-registration/Q-FILLTAX-1-verdict-preregistration.md
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import pytest

_HARNESS = (
    Path(__file__).resolve().parents[2]
    / "lab" / "analysis" / "c1" / "parity_gen2_2026-08"
)
if str(_HARNESS) not in sys.path:
    sys.path.insert(0, str(_HARNESS))

import parity_gate as G  # noqa: E402


def _baseline_pnl(n: int = 40) -> list[float]:
    """Deterministic, distinct-valued synthetic TV-anchor series.

    16 wins (~300-339, i%5 in (0,1)) / 24 losses (~-100..-119.5) — a
    plausible PF>1 book. Every value is distinct so Spearman ties never mask
    a mutation's effect on rank order.
    """
    pnl: list[float] = []
    for i in range(n):
        if i % 5 in (0, 1):
            pnl.append(300.0 + i)
        else:
            pnl.append(-100.0 - i * 0.5)
    return pnl


def _write_csv(path: Path, trade_ids: list[str], pnl: list[float]) -> Path:
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["trade_id", "pnl"])
        writer.writeheader()
        for tid, p in zip(trade_ids, pnl):
            writer.writerow({"trade_id": tid, "pnl": p})
    return path


def test_m1_partial_direction_flip_detected():
    """M1 — direction/side-logic defect: a subset of trades reversed (e.g.
    only 'Add' signals mis-ported to the wrong side, distinct from a total
    strategy.entry inversion already covered by the harness's own generic
    test_evaluate_fail_on_rank_inversion). Detection axis: rank order.
    """
    tv = _baseline_pnl()
    engine = list(tv)
    for i in range(0, 12):  # 30% of 40 trades flipped
        engine[i] = -engine[i]
    result = G.evaluate(engine, tv)
    assert result.verdict == "FAIL"
    assert any("spearman_rho" in r for r in result.reasons)


def test_m2_uniform_commission_omission_detected():
    """M2 — engine omits a constant per-trade tax the TV export bakes in:
    the fill-optimism gap V1 exists to measure (Q-FILLTAX-1 SS1). A constant
    additive shift is rank-preserving (rho stays exactly 1.0) but is NOT
    PF-invariant like M3's multiplicative defect — measured: trips both
    net_rel and pf_rel. Assert net_rel here (pf_rel is a bonus signal, not
    asserted, since a smaller tax could plausibly clear PF_REL_BAND alone).
    """
    tv = _baseline_pnl()
    tax = 15.0  # $/trade the engine fails to charge
    engine = [p + tax for p in tv]  # engine shows MORE profit than TV (omits the tax)
    result = G.evaluate(engine, tv)
    assert result.verdict == "FAIL"
    assert any("net_rel" in r for r in result.reasons)
    assert result.spearman_rho == pytest.approx(1.0), (
        "a constant per-trade shift must not move rank order — if this "
        "assertion fails, the harness's rank metric has an unexpected "
        "sensitivity to translation and needs its own investigation"
    )


def test_m3_proportional_contractvalue_defect_detected():
    """M3 — contractValue mis-port (named historical defect: Striker DJ30
    default contractValue=1 vs required=10, CLAUDE.md strategy table).
    Proportional scaling is PF-invariant (the wins/losses ratio is unchanged
    by a common positive factor) — must be caught on net; PF_REL_BAND must
    NOT be why (a documented gate property, not a bug — see freeze SS2).
    """
    tv = _baseline_pnl()
    scale = 0.1  # 10x under-sized engine positions (contractValue 1 instead of 10)
    engine = [p * scale for p in tv]
    result = G.evaluate(engine, tv)
    assert result.verdict == "FAIL"
    assert any("net_rel" in r for r in result.reasons)
    assert not any("pf_rel" in r for r in result.reasons), (
        "PF is scale-invariant under a proportional defect — pf_rel staying "
        "in-band here is expected, not a false negative; net_rel is this "
        "mutation's sole tripwire"
    )


def test_m4_missing_trades_detected(tmp_path: Path):
    """M4 — engine silently drops a subset of trades TV has (e.g. a
    session/filter port bug). Alignment-level defect — exercised through
    run_gate/CSV (trade_id join), not evaluate() directly.
    """
    tv = _baseline_pnl()
    ids = [f"t{i}" for i in range(len(tv))]
    dropped = {"t3", "t11", "t22", "t30", "t37"}  # 5 of 40 missing from engine
    eng_ids = [tid for tid in ids if tid not in dropped]
    eng_pnl = [p for tid, p in zip(ids, tv) if tid not in dropped]

    eng_csv = _write_csv(tmp_path / "engine.csv", eng_ids, eng_pnl)
    tv_csv = _write_csv(tmp_path / "tv.csv", ids, tv)
    result = G.run_gate(eng_csv, tv_csv)
    assert result.verdict == "FAIL"
    assert any("align:" in r for r in result.reasons)


def test_m5_duplicate_trade_detected(tmp_path: Path):
    """M5 — engine double-counts one trade (e.g. a pyramid/re-entry
    counting bug in the port). The harness's own duplicate guard is written
    for the tv_anchor side; this proves an engine-side duplicate is still
    caught (indirectly, via the second occurrence finding its id already
    consumed) — the mechanism differs from M4 but the outcome must still be
    FAIL, not a silently mis-aligned ADMIT.
    """
    tv = _baseline_pnl()
    ids = [f"t{i}" for i in range(len(tv))]
    eng_ids = list(ids) + ["t7"]  # t7 fires twice in the engine's export
    eng_pnl = list(tv) + [tv[7]]

    eng_csv = _write_csv(tmp_path / "engine.csv", eng_ids, eng_pnl)
    tv_csv = _write_csv(tmp_path / "tv.csv", ids, tv)
    result = G.run_gate(eng_csv, tv_csv)
    assert result.verdict == "FAIL"
    assert any("align:" in r for r in result.reasons)


def test_m6_asymmetric_exit_timing_inflation_detected():
    """M6 — exit-timing/lag defect (named precedent: STEP2_PARITY's
    measured MYM native exits running up to +10 bars/2.5h longer than the
    CFD reference, lab/analysis/c1/q_rail_1_2026-07/STEP2_PARITY.md) —
    winners run further before the port detects the exit; losers untouched.
    Rank order among winners is preserved (same positive scalar applied to
    an already-top-ranked subset), so detection should land on PF, not rho.
    """
    tv = _baseline_pnl()
    engine = [p * 1.20 if p > 0 else p for p in tv]  # winners run 20% further
    result = G.evaluate(engine, tv)
    assert result.verdict == "FAIL"
    assert any("pf_rel" in r for r in result.reasons)


def test_m7_signal_identity_rank_decorrelation_detected():
    """M7 — tick-level re-evaluation defect (named precedent: the still-OPEN
    Q-SIGID-1 live-vs-backtest signal-identity gap,
    docs/briefs/Q-SIGID-1-intra-bar-signal-identity.md — calc_on_every_tick
    / mid-bar close mismatch). A contiguous block of trades gets permuted
    against the TV anchor's positional order — same value set, scrambled
    pairing — corrupting rank order without a comparable net/PF effect.
    Detection should land on rho.
    """
    tv = _baseline_pnl()
    engine = list(tv)
    lo, hi = 10, 30  # 50% of trades positionally scrambled vs the TV anchor
    engine[lo:hi] = list(reversed(engine[lo:hi]))
    result = G.evaluate(engine, tv)
    assert result.verdict == "FAIL"
    assert any("spearman_rho" in r for r in result.reasons)


def test_m8_near_identical_pair_still_admits():
    """M8 — sanity companion (Q-FILLTAX-1 SS6 "0 false passes"): tiny
    sub-tick rounding noise, well within any real fill-precision
    difference, must still ADMIT — proves M1-M7's detections above aren't
    achieved by a gate that just FAILs everything.
    """
    tv = _baseline_pnl()
    engine = [p + (0.01 if i % 2 == 0 else -0.01) for i, p in enumerate(tv)]
    result = G.evaluate(engine, tv)
    assert result.verdict == "ADMIT"
    assert result.reasons == ()


def test_battery_bands_still_match_prereg_literals():
    """Pin the battery to the harness's current FROZEN-PRE-RUN bands so a
    silent band drift shows up here, not as a confusing M1-M8 result change.
    """
    assert G.RANK_RHO_FLOOR == 0.75
    assert G.NET_REL_BAND == 0.02
    assert G.PF_REL_BAND == 0.02
    assert G.MIN_TRADES == 30
