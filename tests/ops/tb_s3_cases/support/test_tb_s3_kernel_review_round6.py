"""PR 365 at bafdd97: restart fences, complete attach intents and trustworthy risk fields."""


from dataclasses import replace


import pytest


from book_protocol import Bracket


from tests.ops.tb_s3_kernel.harness import MIN, Sequence, entry, fill_lot, make_world


from tests.ops.tb_s3_cases.support.test_tb_s3_kernel_redesign import Crash, crash_once


from tests.ops.tb_s3_cases.support.test_tb_s3_kernel_review_round4 import CutStore


from tests.ops.tb_s3_kernel.broker import BAR
