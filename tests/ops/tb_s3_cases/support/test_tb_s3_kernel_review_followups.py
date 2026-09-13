"""Composed evidence and recovery regressions from the second PR #365 review."""


import pytest


from book_protocol import Bracket


from tests.ops.tb_s3_kernel.harness import BAR, MIN, entry, fill_lot, make_world


from tests.ops.tb_s3_kernel.kernel import KernelRefusal


from tests.ops.tb_s3_cases.support.test_tb_s3_kernel_review import _position_only
