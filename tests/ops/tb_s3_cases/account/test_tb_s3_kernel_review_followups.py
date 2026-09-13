"""Composed evidence and recovery regressions from the second PR #365 review."""


import pytest


from book_protocol import Bracket


from tests.ops.tb_s3_kernel.account_harness import BAR, MIN, entry, fill_lot, make_world


from tests.ops.tb_s3_kernel.kernel import KernelRefusal


from tests.ops.tb_s3_cases.support.test_tb_s3_kernel_review import _position_only


def test_kill_after_eod_preserves_both_completion_requests():
    """Two reasons sharing a symbol must each reach a confirmed outcome."""
    world = make_world()
    fill_lot(world, "vanguard_mgc", 2)
    world.kernel.eod(world.now)
    world.kernel.kill(world.now)
    world.advance(MIN)
    world.snap()
    assert world.kernel.flatten_complete("eod_flatten", world.now)
    assert world.kernel.kill_status(False, world.now)["complete"]
    assert world.kernel.dry_run
