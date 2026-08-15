"""B1 payload builder — five-field contract, fresh tags."""
from __future__ import annotations

import pytest

from c1_signal_daemon.b1_payload import (
    B1PayloadError,
    build_b1_payload,
    fresh_bar_time,
)


def test_build_b1_payload_five_fields():
    p = build_b1_payload(
        leg_id="nas100_mnq",
        signal_type="entry",
        bar_time="t1",
        close=21000.5,
        stop_dist_pts=12.0,
    )
    assert set(p) == {
        "leg_id",
        "signal_type",
        "bar_time",
        "close",
        "stop_dist_pts",
    }
    assert p["close"] == 21000.5


def test_reject_unknown_signal_type():
    with pytest.raises(B1PayloadError, match="unknown signal_type"):
        build_b1_payload(
            leg_id="x",
            signal_type="scale_in",
            bar_time="t",
            close=1.0,
            stop_dist_pts=1.0,
        )


def test_fresh_bar_time_unique_per_fire():
    a = fresh_bar_time("nas100_mnq", "entry", "2026-08-08T14:00:00Z")
    b = fresh_bar_time("nas100_mnq", "entry", "2026-08-08T14:15:00Z")
    assert a != b
    assert a.startswith("nas100_mnq-entry-")
