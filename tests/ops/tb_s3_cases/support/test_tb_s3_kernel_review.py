"""TB-S3 kernel model — regressions for the review findings on PR #365 (`2015eef`).

Each test reproduces one finding against the model exactly as reported, so the composition
it exposed cannot return silently.
"""


from __future__ import annotations


from dataclasses import replace


from book_protocol import Bracket


from tests.ops.tb_s3_kernel.harness import BAR, MIN, entry, fill_lot, make_world


def _position_only(ev):
    """A read that carries the position but no order-level data (spec: aggregate P)."""
    return replace(ev, working=(), order_status={}, fills={}, lots={}, order_level=False)
