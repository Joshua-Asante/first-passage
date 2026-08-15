"""Clip a 15m baseline export to the [first, last] exit timestamp of the 5m
proto export, so per-strategy metrics compare on a matched window."""
from __future__ import annotations
import pandas as pd

def match(baseline: pd.DataFrame, proto: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Clip `baseline` to the proto's [min, max] exit_ts; return (clipped, span)."""
    b = pd.to_datetime(baseline["exit_ts"])
    p = pd.to_datetime(proto["exit_ts"])
    start, end = p.min(), p.max()
    clipped = baseline[(b >= start) & (b <= end)].reset_index(drop=True)
    span = {
        "start": start,
        "end": end,
        "span_days": int((end - start).days),
        "proto_n": int(len(proto)),
        "baseline_in_window_n": int(len(clipped)),
    }
    return clipped, span
