"""PR 365 review at 2eb6c12: composed outcomes, with external event expectations."""


from dataclasses import replace


import pytest


from book_protocol import Bracket


from tests.ops.tb_s3_kernel.broker import BrokerOrder


from tests.ops.tb_s3_kernel.harness import BAR, MIN, Sequence, entry, fill_lot, make_world


from tests.ops.tb_s3_cases.support.test_tb_s3_kernel_redesign import Crash, crash_once
