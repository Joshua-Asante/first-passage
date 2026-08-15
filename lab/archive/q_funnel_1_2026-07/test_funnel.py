"""Q-FUNNEL-1 funnel wrapper tests — TDD against frozen pre-registration."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import funnel as F  # noqa: E402


# ---------------------------------------------------------------------------
# Step 2.2 — fee / reset recursion
# ---------------------------------------------------------------------------

def test_no_retry_spend_is_exactly_one_eval_fee():
    assert F.attempt_spend(1) == F.EVAL_FEE_USD
    assert F.max_attempts("no_retry") == 1


def test_retry_to_cap_spend_bounded_by_six_fees():
    assert F.max_attempts("retry_to_cap") == 1 + F.MAX_RETRIES  # 6
    assert F.attempt_spend(6) == 6 * F.EVAL_FEE_USD
    assert F.MAX_RETRIES == 5


def test_fixture_bust_chain_cumulative_spend_and_days():
    """Hand-computable: three busts under retry-to-cap → 3× fee, days sum."""
    # Scripted lineage accounting without RNG: mimic three failed attempts.
    attempts = 3
    days_each = (10, 20, 15)
    spend = F.attempt_spend(attempts)
    assert spend == 3 * F.EVAL_FEE_USD
    assert sum(days_each) == 45
    L = F.LineageResult(
        terminal_kind="retries_exhausted",
        cumulative_spend=spend,
        cumulative_days=sum(days_each),
        payouts_total=0.0,
        eval_attempts=attempts,
    )
    assert L.net_value == -spend


# ---------------------------------------------------------------------------
# Step 2.3 — funded-phase payout arithmetic
# ---------------------------------------------------------------------------

def test_payout_request_102500_balance_is_1250():
    """Pre-reg §5: 50% of $2,500 profit = $1,250 (< $4,000 cap)."""
    assert F.compute_payout_request(102_500.0) == 1_250.0
    assert F.trader_receives(1_250.0) == 1_125.0  # 90/10


def test_payout_cap_at_4000():
    # profit $20,000 → 50% = $10,000 → capped at $4,000
    assert F.compute_payout_request(120_000.0) == 4_000.0


def test_scripted_funded_path_five_winning_days_one_payout():
    """Pre-reg §5 worked shape: land at $102,500 on the 5th winning day → $1,250 request."""
    # start $101,500 + 5×$200 = $102,500 → request = min(50%×$2,500, $4k) = $1,250
    days = [200.0] * 5
    kind, total, events, used = F.simulate_funded_phase(
        days, start_equity=101_500.0, start_peak=101_500.0
    )
    assert kind == "funded_horizon"
    assert used == 5
    assert len(events) == 1
    assert events[0].request_usd == 1_250.0
    assert events[0].trader_received_usd == 1_125.0
    assert total == 1_125.0
    # Balance after: 102500 - 1250 = 101250
    assert events[0].balance_after == pytest.approx(101_250.0)


def test_winning_day_counter_resets_after_payout():
    """Resolution C — need another 5 winning days for the second payout."""
    days = [200.0] * 5 + [200.0] * 4
    _kind, total, events, _ = F.simulate_funded_phase(
        days, start_equity=101_500.0, start_peak=101_500.0
    )
    assert len(events) == 1
    assert total == 1_125.0


def test_busted_post_funding_keeps_prior_payouts():
    """Resolution A — no clawback of realized payouts."""
    days = [200.0] * 5 + [-5_000.0]
    kind, total, events, _ = F.simulate_funded_phase(
        days, start_equity=101_500.0, start_peak=101_500.0, floor_locked=True
    )
    assert kind == "busted_post_funding"
    assert total == 1_125.0
    assert len(events) == 1
    L = F.LineageResult(
        terminal_kind=kind,
        cumulative_spend=F.EVAL_FEE_USD,
        cumulative_days=6,
        payouts_total=total,
        payouts=events,
    )
    assert L.net_value == total - F.EVAL_FEE_USD


# ---------------------------------------------------------------------------
# Step 2.4 — EV/day aggregation + edge sanity
# ---------------------------------------------------------------------------

def test_ev_day_hand_computed_two_lineages():
    L1 = F.LineageResult("funded_horizon", 328.0, 10, 1328.0)
    L2 = F.LineageResult("busted_eval", 328.0, 10, 0.0)
    # nets: (1328-328)=1000, (0-328)=-328; mean_net=336; mean_days=10; EV/day=33.6
    ev = F.ev_day_from_lineages([L1, L2], n_boot=50, boot_seed=1)
    assert ev.ev_day == pytest.approx(33.6)
    assert ev.mean_net == pytest.approx(336.0)
    assert ev.mean_days == pytest.approx(10.0)


def test_edge0_ev_leq_panel_historical_synthetic():
    """Sanity: zero-edge book must not beat historical-edge on EV/day."""
    rng = np.random.default_rng(0)
    # Positive-drift synthetic daily series
    hist = rng.normal(30.0, 80.0, size=400)
    zero = hist - hist.mean()
    blocks_h = __import__(
        "discovery.prop_survivor_scoring", fromlist=["blocks_from_daily_pnl"]
    ).blocks_from_daily_pnl(hist)
    blocks_z = __import__(
        "discovery.prop_survivor_scoring", fromlist=["blocks_from_daily_pnl"]
    ).blocks_from_daily_pnl(zero)

    def _cell(blocks, seed):
        r = np.random.default_rng(seed)
        lins = [
            F.simulate_lineage(
                blocks,
                r,
                policy="no_retry",
                haircut=0.50,
                eval_fee=0.0,
                eval_horizon=200,
                funded_horizon=60,
                fund_payouts=True,
            )
            for _ in range(80)
        ]
        return F.ev_day_from_lineages(lins, n_boot=40, boot_seed=seed)

    ev_h = _cell(blocks_h, 7)
    ev_z = _cell(blocks_z, 7)
    assert ev_z.ev_day <= ev_h.ev_day + 1e-9


def test_materiality_threshold_is_literal_25pct():
    assert F.MATERIALITY_RELATIVE == 0.25


# ---------------------------------------------------------------------------
# Step 2.1 — panel smoke (requires CME CSVs)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def panel_bundle():
    try:
        return F.load_c1_panel()
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"panel unavailable: {exc}")


def test_panel_loads_and_edge_scenarios_preserve_length(panel_bundle):
    panel, meta, daily = panel_bundle
    assert meta["n_bdays"] > 100
    assert daily.shape[0] == meta["n_bdays"]
    e0 = F.apply_edge_scenario(panel, "edge_0")
    eh = F.apply_edge_scenario(panel, "edge_half_panel")
    ep = F.apply_edge_scenario(panel, "edge_panel_historical")
    assert e0.shape == daily.shape == eh.shape == ep.shape
    assert abs(float(e0.mean())) < 1e-8
    # half-panel mean ≈ 0.5 × historical mean (per-leg de-mean → book mean halves)
    assert float(eh.mean()) == pytest.approx(0.5 * float(ep.mean()), rel=0.05)


def test_smoke_repro_1p00_within_tolerance(panel_bundle):
    """Step 2.1 gate — 1.00× H1 vs REGIME_GATE baseline (≤1pp) at full sims.

    Bootstrap-95th at n_panels=5 is too noisy for the ≤2pp band against the
    n=100 ratification; H1 (seeded, full 10k×3) is the load-bearing smoke pin.
    Bootstrap fidelity is covered by the WATCH-1 regression pin.
    """
    _ = panel_bundle
    out = F.smoke_repro_1p00(n_sims=None, include_bootstrap=False)
    assert abs(out["H1_bust"] - out["H1_baseline"]) <= F.REPRO_H1_TOL_PP


def test_regression_pin_matches_watch1_ratification(panel_bundle):
    """fees=0 / funded_value=0 / retry=never — bust/pass via regime-gate primitives.

    Full-panel + H1 + bootstrap must match haircut RESULTS within Step 2.1
    tolerances. Uses full thr sims; bootstrap n_panels=100 matches ratification.
    """
    _ = panel_bundle
    m = F.watch1_regression_metrics(
        n_sims=None,
        n_panels=100,
        n_jobs=-1,
        include_bootstrap=True,
    )
    assert abs(m["full_panel_bust"] - F.WATCH1_FULL_BUST) <= F.REPRO_H1_TOL_PP
    assert abs(m["H1_bust"] - F.WATCH1_H1_BUST) <= F.REPRO_H1_TOL_PP
    assert abs(m["boot_bust_95th"] - F.WATCH1_BOOT_BUST_95TH) <= F.REPRO_BOOT95_TOL_PP
    assert m["boot_pass_5th"] >= 0.50
    # Soft pin on pass-5th magnitude (ratified 95.76%)
    assert abs(m["boot_pass_5th"] - F.WATCH1_PASS_5TH) <= 0.05
