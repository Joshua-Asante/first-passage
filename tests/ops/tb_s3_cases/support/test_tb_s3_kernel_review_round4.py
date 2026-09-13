"""PR 365 at ea8a5db: coherent reads, durable commands and broker quantity conservation."""


from dataclasses import replace


import pytest


from book_protocol import Bracket


from tests.ops.tb_s3_kernel.broker import BrokerOrder


from tests.ops.tb_s3_kernel.harness import MIN, Sequence, entry, fill_lot, make_world


from tests.ops.tb_s3_kernel.kernel import KernelRefusal


from tests.ops.tb_s3_cases.support.test_tb_s3_kernel_redesign import Crash, crash_once


class CutStore:
    """Cut after an actual atomic durable write, independent of persist call counts."""

    def __init__(self, data, writes):
        self._data = data
        self.remaining = writes

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
        self.remaining -= 1
        if self.remaining == 0:
            raise Crash("durable write completed")
