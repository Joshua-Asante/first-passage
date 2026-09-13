"""TB-S3 kernel model — regressions for the Codex round on PR #365 (`f8e39af`, eight P1s).

Each test reproduces one finding as reported (spec §2e review contract: a §1/§2 finding is
accepted only with a reproducing scenario), then the kernel fix makes it pass.
"""


from __future__ import annotations


from book_protocol import Bracket


from tests.ops.tb_s3_kernel.broker import STALENESS_WINDOW


from tests.ops.tb_s3_kernel.harness import BAR, MIN, entry, fill_lot, make_world


def _book_with_partial_striker(world):
    decision = world.kernel.admit_entry(entry("dj30_mym_p250", 22), world.now)
    world.broker.fill(decision.ref, qty=10)                           # 12 still working
    fill_lot(world, "vanguard_mgc", 2, Bracket(stop=2_400.0))
    fill_lot(world, "orb_mnq_v7", 1, Bracket(stop=18_450.0))
    assert world.kernel.pending[decision.ref].status == "partial"
    assert world.kernel.ledger.reserved["dj30_mym_p250"] == 12
    return decision.ref
