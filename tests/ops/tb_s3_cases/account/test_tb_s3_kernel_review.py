"""TB-S3 kernel model — regressions for the review findings on PR #365 (`2015eef`).

Each test reproduces one finding against the model exactly as reported, so the composition
it exposed cannot return silently.
"""


from __future__ import annotations


from dataclasses import replace


from book_protocol import Bracket


from tests.ops.tb_s3_kernel.account_harness import BAR, MIN, entry, fill_lot, make_world


def _position_only(ev):
    """A read that carries the position but no order-level data (spec: aggregate P)."""
    return replace(ev, working=(), order_status={}, fills={}, lots={}, order_level=False)


def test_symbol_wide_kill_close_is_queued_behind_an_unresolved_fill_close():
    """Symbol-wide kill close is queued behind an unresolved fill close."""
    world = make_world()
    lot1 = fill_lot(world, "vanguard_mgc", 1, Bracket(stop=2_400.0))
    lot2 = fill_lot(world, "vanguard_mgc", 1, Bracket(stop=2_400.0), kind="add")
    world.broker.inject["close"] = "unknown"
    first = world.kernel.handle_exit("vanguard_mgc", world.now, fill_id=lot1)
    assert first.status == "unknown"
    ops = world.kernel.kill(world.now)
    mgc = next(o for o in ops if o.sym == "MGC")
    assert mgc is not first and mgc.status == "queued"               # not dropped
    world.advance(MIN)
    world.snap()                                                     # first had executed
    assert first.status == "complete"
    assert mgc.status in ("sent", "complete")                        # dispatched in turn
    world.advance(MIN)
    world.snap()
    assert mgc.status == "complete" and world.kernel.lots[lot2].qty == 0
    assert world.kernel.flatten_complete("kill", world.now)
