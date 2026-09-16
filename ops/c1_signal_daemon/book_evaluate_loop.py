"""Offline four-leg daemon loop bound to the durable account runtime.

This component deliberately has no config constructor, HTTP endpoint, sender,
or daemon CLI registration.  Tests and an attended integration harness must
inject the four accepted completed-bar sources and an already-bound runtime.
"""
from __future__ import annotations

import threading

from c1_signal_daemon.book_runtime import FourLegRuntime, LEG_ORDER, BAR_PERIOD, BAR_SLACK
from c1_signal_daemon.feed import Bar


class FourLegEvaluateLoop:
    """Poll exactly one source per accepted leg and feed the durable barrier."""

    def __init__(self, *, sources, runtime):
        if not isinstance(runtime, FourLegRuntime):
            raise TypeError("typed FourLegRuntime required")
        if not isinstance(sources, dict) or tuple(sources) != LEG_ORDER:
            raise ValueError("ordered exact four-leg source registry required")
        if any(not callable(getattr(sources[leg_id], "poll", None)) for leg_id in LEG_ORDER):
            raise TypeError("every four-leg source must provide poll()")
        self.sources = dict(sources)
        self.runtime = runtime
        self._step_lock = threading.Lock()

    def step(self, *, now):
        """Poll once; return completed barrier dispatches, or ``None``."""
        with self._step_lock:
            self.runtime.owner.check_protection_deadlines(now=now)
            self.runtime.owner.check_source_silence(now=now, max_silence=2 * BAR_PERIOD + BAR_SLACK)
            self.runtime.advance_schedule(now=now)
            for bar_time in self.runtime.pending_bar_times:
                self.runtime.expire_barrier(bar_time, now=now)
            if self.runtime.owner.authority == "INTERVENTION":
                return None
            completed = None
            for leg_id in LEG_ORDER:
                bar = self.sources[leg_id].poll()
                if bar is None:
                    continue
                result = self.runtime.on_completed_bar(leg_id, bar, now=now)
                if result is not None:
                    completed = result
            for bar_time in self.runtime.pending_bar_times:
                self.runtime.expire_barrier(bar_time, now=now)
            return completed
