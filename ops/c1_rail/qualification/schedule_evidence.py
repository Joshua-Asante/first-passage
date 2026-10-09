"""Evidence-located schedule placements on the accepted path (ratified 2026-10-09).

Builds ``qualification-schedule-execution/v1`` rows (``parse_schedule_execution_evidence``)
for an intrabar schedule instant from finer bars of the same feed (for example
5-minute bars of the same TradingView continuous symbol) that tile the retained M15
source bar. The accepted emulator path (``replay.accepted_path``) stays fixed, as in
the 2026-09-23 bracket convention; the finer bars only locate the instant on it:

- the instant price ``p`` is the open of the finer bar starting at the instant;
- the segment is set by which of the path's two extremes the finer bars reached
  before the instant (neither: open -> near extreme; near only: near -> far;
  both: far -> close);
- prefix = the path up to ``p`` on that segment, suffix = the rest, so the split
  preserves the path's turning points like ``vertex_split`` (volume whole on the
  prefix).

Candidates that cannot be located are dropped with a reason, and that instant
stays on the bracket's R1/R2 vertex placement:

- ``MALFORMED``: a finer bar is not an aware, finite, valid OHLCV bar
  (``0 < low <= min(open, close) <= max(open, close) <= high``, volume >= 0);
- ``MISSING``: the finer bars do not tile the M15 bar contiguously at one interval,
  or none starts at the instant;
- ``AGGREGATE``: the finer bars do not aggregate exactly to the M15 bar (OHLC, volume);
- ``REVERSED``: by first touch in the finer bars, the far extreme was reached before
  the near one, or without it (the real order contradicts the path);
- ``TIED``: both extremes were first reached inside the same finer bar, so their
  order is undecidable at that resolution;
- ``SEGMENT``: ``p`` does not lie on the located segment;
- ``LATER_BOUNDARY`` (``evidence_rows``): a second intrabar boundary of the same
  leg and bar (only the first can be located);
- ``PATH``: the prefix's or suffix's own emulator path would add a turning point
  (the replay's split validator would reject the row).

Pure: no I/O, no private values. The convention was ratified 2026-10-09; the parser
accepts marked rows while ``production_source.LOCATED_CONVENTION_RATIFIED`` is True.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta
from math import isfinite

from c1_signal_daemon.feed import Bar
from .model import LEG_IDS
from .panel import source_session_date
from .production_source import LOCATED_CONVENTION
from .replay import accepted_path, path_turns

M15 = timedelta(minutes=15)


def _ohlcv(open_, values, close, volume):
    return {'open': open_, 'high': max(values), 'low': min(values), 'close': close, 'volume': volume}


def evidence_row(leg, original, instant, fine):
    """(row, None) or (None, drop reason) for one leg's M15 bar and intrabar instant."""
    if leg not in LEG_IDS:
        raise ValueError('unknown schedule evidence leg')
    if not isinstance(original, Bar) or not isinstance(instant, datetime) or instant.tzinfo is None:
        raise ValueError('aware M15 Bar and instant required')
    if not original.ts < instant < original.ts + M15:
        raise ValueError('instant must be strictly inside the M15 bar')
    for b in fine:
        if (not isinstance(b, Bar) or not isinstance(b.ts, datetime) or b.ts.tzinfo is None
                or not all(isinstance(v, (int, float)) and isfinite(v) for v in (b.open, b.high, b.low, b.close, b.volume))
                or b.volume < 0 or not 0 < b.low <= min(b.open, b.close) <= max(b.open, b.close) <= b.high):
            return None, 'MALFORMED'
    fine = sorted(fine, key=lambda b: b.ts)
    head = [b for b in fine if b.ts < instant]
    tail = [b for b in fine if b.ts >= instant]
    steps = {later.ts - earlier.ts for earlier, later in zip(fine, fine[1:])}
    if (not head or not tail or head[0].ts != original.ts or tail[0].ts != instant or len(steps) != 1
            or fine[-1].ts + steps.pop() != original.ts + M15):
        return None, 'MISSING'
    if (fine[0].open != original.open or fine[-1].close != original.close
            or max(b.high for b in fine) != original.high or min(b.low for b in fine) != original.low
            or sum(b.volume for b in fine) != original.volume):
        return None, 'AGGREGATE'
    path = accepted_path(original)

    def first_reached(value):
        """Index of the first prefix bar touching ``value``; -1 when it is the open; None if never."""
        if value == path[0]:
            return -1
        hits = (i for i, b in enumerate(head) if (b.low <= value if value == original.low else b.high >= value))
        return next(hits, None)
    near, far = first_reached(path[1]), first_reached(path[2])
    if far is not None and (near is None or far < near):
        return None, 'REVERSED'
    if far is not None and far == near >= 0:
        return None, 'TIED'
    segment = int(near is not None) + int(far is not None)
    price = tail[0].open
    if not min(path[segment], path[segment+1]) <= price <= max(path[segment], path[segment+1]):
        return None, 'SEGMENT'
    head_values, tail_values = path[:segment+1] + [price], [price] + path[segment+1:]
    prefix = _ohlcv(path[0], head_values, price, original.volume)
    suffix = _ohlcv(price, tail_values, path[-1], 0.0)
    own = lambda ts, s: accepted_path(Bar(ts, s['open'], s['high'], s['low'], s['close'], s['volume']))
    if path_turns(own(original.ts, prefix) + own(instant, suffix)) != path_turns(path):
        return None, 'PATH'
    return {'source_session_date': source_session_date(original.ts).isoformat(), 'leg_id': leg,
            'source_bar_time': original.ts.isoformat(), 'interval_start': original.ts.isoformat(),
            'instant': instant.isoformat(), 'price': price,
            'prefix': prefix, 'suffix': suffix, 'convention': LOCATED_CONVENTION}, None


def evidence_rows(candidates):
    """Rows and drop counts for ``(leg, original M15 Bar, instant, finer bars)`` candidates.

    Pass every intrabar schedule instant of a bar. Only the first per (leg, bar)
    can be located: a later same-bar boundary drops as ``LATER_BOUNDARY``, because
    the bracket refuses a marked row that follows an earlier same-bar split.
    """
    rows, drops, seen = [], Counter(), set()
    for leg, original, instant, fine in sorted(candidates, key=lambda c: (c[0], c[1].ts, c[2])):
        if (leg, original.ts) in seen:
            drops['LATER_BOUNDARY'] += 1
            continue
        seen.add((leg, original.ts))
        row, reason = evidence_row(leg, original, instant, fine)
        if row is None:
            drops[reason] += 1
        else:
            rows.append(row)
    return rows, drops
