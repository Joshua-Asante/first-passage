"""TB-S3 kernel model — one test per review-finding class from PR #360's Codex rounds.

Each test is the scenario the finding described, encoded against the model so that the
composition it exposed cannot regress silently. Names cite the spec clause that closed it.
"""


from __future__ import annotations


import pytest


from c1_rail.book_policy import TakeoverPlan


from book_protocol import Bracket


from tests.ops.tb_s3_kernel.broker import NOT_SUPPORTED


from tests.ops.tb_s3_kernel.harness import BAR, MIN, entry, fill_lot, make_world


from tests.ops.tb_s3_kernel.kernel import Kernel, KernelRefusal


_lot = fill_lot


def _fill_book_except_aegis(world):
    _lot(world, "dj30_mym_p250", 22)
    _lot(world, "vanguard_mgc", 2, Bracket(stop=2_400.0))
    _lot(world, "orb_mnq_v7", 1, Bracket(stop=18_450.0))
    assert world.kernel.ledger.micro_used() == 25
