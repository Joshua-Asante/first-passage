"""Phase 3 planning only: calculator + synthetic component timing; no qualification.

No panels, private ports, account state, qualification seeds or outcome files are
read. Stdout is a preparation report, never a frozen manifest or a result seal.
Run single-process from this worktree; redirect to a NEW temporary output file.
"""
from __future__ import annotations

import hashlib
import json
import platform
import random
import statistics
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT), str(ROOT / "core"), str(ROOT / "ops")]
from scripts import certification_power as cp
from c1_rail.book_policy import candidate_book_protection_policy, entry_quantities
from c1_signal_daemon.book_protocol import FillTiming, Mode, OrderIntent, Side
from c1_signal_daemon.feed import Bar
from c1_signal_daemon.tv_broker_emulator import TVBrokerEmulator

BENCH_NAMESPACE = "phase3-preparation/synthetic-component-benchmark/v1"
SESSIONS, BARS, REPEATS = 25, 92, 3


def synthetic_workload():
    # Deliberately generic prices and instruments, not a portfolio path.
    rng = random.Random(BENCH_NAMESPACE)
    brokers = [TVBrokerEmulator(f"synthetic-{i}", .25, 1., 1, .1) for i in range(4)]
    policy = candidate_book_protection_policy()
    start = datetime(2000, 1, 3, tzinfo=timezone.utc)
    for session in range(SESSIONS):
        mode = Mode.NORMAL if session % 2 == 0 else Mode.PROTECTED
        for index in range(BARS):
            price = 100 + rng.random()
            bar = Bar(start + timedelta(minutes=15 * (session * BARS + index)),
                      price, price + 1, price - 1, price + .1, 1.)
            for broker in brokers:
                # Exercise real shared arithmetic and emulator, without private
                # adapter logic, account serialization or the absent MC assembler.
                entry_quantities("dj30_mym_p250", mode=mode, policy=policy,
                                 lifecycle_tier="AUTHORIZED", risk_dollars=700,
                                 per_contract_risk=50, cap_alloc=80)
                broker.process_bar(bar)
                if index == 0:
                    broker.submit([OrderIntent(f"entry-{session}", broker.leg_id,
                        "entry", Side.BUY, 1, timing=FillTiming.THIS_CLOSE)], bar)
                if index == BARS - 1:
                    broker.submit([OrderIntent(f"flat-{session}", broker.leg_id,
                        "flat", Side.SELL, None, timing=FillTiming.THIS_CLOSE)], bar)
        assert all(b.position() == 0 and not b.pending_order_ids() for b in brokers)
    assert sum(len(b.closed_trades) for b in brokers) == SESSIONS * 4


def main():
    planning = []
    for fail, speed in ((.03, .65), (.03, .60), (.02, .60)):
        n = cp.size_for_joint_four(fail, speed, .80, dependence="frechet")
        planning.append({"assumed_failure_rate": fail, "assumed_pass_by_200": speed,
            "n_per_population": n, "failure_limb_power": cp.per_limb_power(n, fail),
            "speed_limb_power": cp.speed_limb_power(n, speed),
            "joint_power_frechet": cp.joint_power_four(cp.per_limb_power(n, fail),
                cp.speed_limb_power(n, speed), "frechet"),
            "max_failures": cp.max_certifying_busts(n),
            "min_pass_by_200": cp.min_certifying_passes(n)})
    times = []
    for _ in range(REPEATS):
        began = time.perf_counter()
        synthetic_workload()
        times.append(time.perf_counter() - began)
    # Scale only this component fixture, never assert a full replay time bound.
    proxy = max(times) * 500 / SESSIONS
    files = ["scripts/certification_power.py", "tests/test_certification_power.py",
        "ops/c1_rail/policy_fingerprint.py", "tests/ops/test_policy_fingerprint.py",
        "tests/ops/fixtures/policy_fingerprint_vectors.json", "core/dd_geometry.py",
        "core/dd_protection.py", "core/firm_rules.py", "core/lifecycle.py",
        "core/mc/simulation.py", "core/mc/preflight.py", "ops/c1_rail/book_policy.py",
        "ops/c1_rail/book_capacity.py", "ops/c1_rail/book_sizing_context.py",
        "ops/c1_rail/book_session_calendar.py", "ops/c1_signal_daemon/book_protocol.py",
        "ops/c1_signal_daemon/feed.py", "ops/c1_signal_daemon/pine_ta.py",
        "ops/c1_signal_daemon/tv_broker_emulator.py", "requirements-ops.lock",
        "requirements-research.lock"]
    seeds = {f"n{i}": hashlib.sha256(f"tradeify-f1-candidate-2026-09-15/n{i}/v1".encode()).hexdigest()[:16]
             for i in (1, 2, 3)}
    assert len(set(seeds.values())) == 3
    print(json.dumps({"artifact_class": "DRAFT_PREPARATION_NOT_FROZEN_NOT_QUALIFICATION",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "runtime": {"implementation": platform.python_implementation(),
                    "version": platform.python_version(), "platform": platform.platform(),
                    "executable_sha256": hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest()},
        "source_sha256": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in files},
        "preparation_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "design_only": planning, "candidate_seed64_hex_not_consumed": seeds,
        "benchmark": {"namespace": BENCH_NAMESPACE, "sessions": SESSIONS,
            "bars_per_session": BARS, "generic_brokers": 4, "repeats": REPEATS,
            "seconds": times, "median_seconds": statistics.median(times),
            "max_seconds": max(times), "scaled_500_session_component_seconds": proxy,
            "e1_worst_43510_component_hours": proxy * 43510 / 3600,
            "n3_2910_component_hours": proxy * 2910 / 3600,
            "limitation": "Component proxy only; excludes actual adapters, account/replay/MC, I/O, warmup and bootstrap. Not a runtime bound or F1 budget proof."}}, indent=2))


if __name__ == "__main__":
    main()
