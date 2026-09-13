"""TB-S3 kernel model — the spec's §2d acceptance cases AC-1..AC-10, executable.

Spec: docs/spec/2026-09-12-c1-multi-leg-rail-extension-spec.md (rev 5.4). Each test names the
case it encodes; the acceptance question is the spec's: can the complete behavior execute and
reach a confirmed outcome under the stated failure case?
"""


from __future__ import annotations


from datetime import datetime


import pytest


from book_protocol import Bracket


from tests.ops.tb_s3_kernel.broker import NOT_SUPPORTED, STALENESS_WINDOW


from tests.ops.tb_s3_kernel.harness import BAR, MIN, entry, fill_lot, make_world


from tests.ops.tb_s3_kernel.kernel import Kernel, KernelRefusal


_fill_entry = fill_lot
