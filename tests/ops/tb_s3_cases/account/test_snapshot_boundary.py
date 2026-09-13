"""Account recovery cannot silently discard its persisted control state."""
import pytest

from tests.ops.tb_s3_kernel.account import AccountKernel
from tests.ops.tb_s3_kernel.account_harness import make_world
from tests.ops.tb_s3_kernel.harness import make_world as primitive_world
from tests.ops.tb_s3_kernel.kernel import Kernel, KernelRefusal


def test_primitive_restart_refuses_account_snapshot():
    world = make_world()
    with pytest.raises(KernelRefusal, match="incompatible store schema"):
        Kernel.restart(world.kernel.store, world.broker, world.clock, world.now)


def test_account_restart_refuses_primitive_snapshot():
    world = primitive_world()
    world.kernel.persist()
    with pytest.raises(KernelRefusal, match="incompatible store schema"):
        AccountKernel.restart(world.kernel.store, world.broker, world.clock, world.now)
