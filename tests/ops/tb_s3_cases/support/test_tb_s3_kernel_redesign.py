"""Contract regressions: independently stated outcomes across composed events."""


import copy


from dataclasses import replace


import pytest


from book_protocol import Bracket


from tests.ops.tb_s3_kernel.harness import BAR, MIN, entry, fill_lot, make_world


from tests.ops.tb_s3_kernel.kernel import Kernel, KernelRefusal, Store


def restart(world):
    """Replace the listener, retaining only its durable store and external broker."""
    world.kernel = type(world.kernel).restart(world.kernel.store, world.broker, world.clock, world.now,
                                  protection_cases=world.kernel.protection_cases)
    if hasattr(world, "daemon"):
        world.daemon.kernel = world.kernel
    return world.kernel


class Crash(RuntimeError):
    """Abrupt process death; callers may not finish their current transition."""


def crash_once(kernel, kind, boundary):
    """Interrupt one real dispatch at a persisted boundary, without changing its result."""
    def hook(stage, effect):
        if effect.kind == kind and stage == boundary:
            kernel.effect_hook = None
            raise Crash(stage)
    kernel.effect_hook = hook
