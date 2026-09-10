"""Lazy Databento 0.81.0 Live adapter; no historical replay or network at boot.

Verified against installed databento/live/client.py and databento_dbn 0.62.0
_lib.pyi. The injectable factory implements Live.add_callback, subscribe, start,
is_connected, terminate. OHLCV ts_event denotes minute start; bars are accepted
only after minute end. DBN raw fixed-point prices use 1e9 scale. Fixture records
are useful for software tests but never genuine monitoring evidence.
"""
from __future__ import annotations

from collections import deque
from datetime import datetime, timezone
import threading

from c1_signal_daemon.feed import Bar
from c1_signal_daemon.m1_stage1_control import digest
from c1_signal_daemon.m1_stage1_state import CeremonyError


def _sdk_factory():
    import databento as db
    # Live reads DATABENTO_API_KEY from the environment. subscribe opens TCP.
    return db.Live(reconnect_policy="none")


class DatabentoLiveBarSource:
    feed_mode = "databento_live_ohlcv_1m"

    def __init__(self, store, *, sdk_factory=None, clock=None):
        self.store = store
        self._factory = sdk_factory or _sdk_factory
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._client = None
        self._requested = None
        self.binding = None
        self._mapping = None
        self._queue = deque(maxlen=256)
        self._mutex = threading.RLock()
        self._retry_at = 0.0
        self._backoff = 1.0
        self._session = 0

    @property
    def connected(self):
        try:
            return self._client is not None and self._client.is_connected()
        except Exception:
            return False

    def _detach_locked(self):
        client, self._client = self._client, None
        self._session += 1
        self.binding = None
        self._mapping = None
        self._queue.clear()
        return client

    @staticmethod
    def _terminate(client):
        if client is not None:
            try:
                client.terminate()
            except Exception:
                pass

    def _disconnect(self):
        with self._mutex:
            client = self._detach_locked()
        self._terminate(client)

    def deactivate(self):
        with self._mutex:
            self._requested = None
            client = self._detach_locked()
        self._terminate(client)

    def _failed(self, *_, session=None):
        with self._mutex:
            if session is not None and session != self._session:
                return
            client = self._detach_locked()
            self._retry_at = self._clock().timestamp() + self._backoff
            self._backoff = min(self._backoff * 2, 30)
        self._terminate(client)

    def activate(self, binding):
        if self._requested is not None and self._requested != binding:
            self.deactivate()
        self._requested = dict(binding)
        if self.connected:
            return
        if self._client is not None:
            # Runtime activation precedes poll, so detect established loss here too.
            self._failed()
            return
        if self._clock().timestamp() < self._retry_at:
            return
        self._disconnect()
        with self._mutex:
            session = self._session
        try:
            client = self._factory()
            with self._mutex:
                current = session == self._session and self._requested == binding
                if current:
                    self._client = client
            if not current:
                self._terminate(client)
                return
            # SDK calls can wait on its callback thread; never hold our mutex here.
            client.add_callback(
                lambda record: self._on_record(record, session),
                lambda error: self._failed(error, session=session))
            client.subscribe(dataset="GLBX.MDP3", schema="ohlcv-1m",
                                   symbols=[binding["raw_symbol"]], stype_in="raw_symbol")
            client.start()
        except Exception:
            self._failed(session=session)

    def _on_record(self, record, session):
        with self._mutex:
            if session != self._session or self._requested is None:
                return
            name = type(record).__name__
            if name not in {"SymbolMappingMsg", "OHLCVMsg"}:
                return
            self._queue.append(record)

    def _map(self, record):
        wanted = self._requested
        self._mapping = None
        self.binding = None
        if (record.instrument_id != wanted["instrument_id"]
                or record.publisher_id != wanted["publisher_id"]
                # Input matches this subscription; DBN output is always RAW_SYMBOL.
                # Numeric instrument identity belongs to the record header.
                or str(record.stype_in) != "raw_symbol"
                or str(record.stype_out) != "raw_symbol"
                or record.stype_in_symbol != wanted["raw_symbol"]
                or record.stype_out_symbol != wanted["raw_symbol"]
                or not isinstance(record.start_ts, int) or not isinstance(record.end_ts, int)
                or record.start_ts >= record.end_ts):
            return
        self._mapping = (record.start_ts, record.end_ts)
        self.binding = dict(wanted)

    def _bar(self, record):
        wanted = self._requested
        stamp = record.ts_event
        if (self._mapping is None or int(record.rtype) != 33
                or record.instrument_id != wanted["instrument_id"]
                or record.publisher_id != wanted["publisher_id"]
                or type(stamp) is not int or stamp % (60 * 10**9) != 0
                or not self._mapping[0] <= stamp < self._mapping[1]):
            return None
        age = self._clock().timestamp() - stamp / 10**9
        if not 60 <= age <= 150:
            return None
        prices = [getattr(record, name) for name in ("open", "high", "low", "close")]
        if (not all(type(value) is int and 0 < value < 2**63 - 1 for value in prices)
                or type(record.volume) is not int or record.volume <= 0):
            return None
        opn, high, low, close = [value / 10**9 for value in prices]
        if not low <= min(opn, close) <= max(opn, close) <= high:
            return None
        bar = Bar(datetime.fromtimestamp(stamp / 10**9, timezone.utc), opn, high,
                  low, close, record.volume)
        if not self.store.watermark(digest(wanted), stamp):
            return None
        self._backoff = 1.0
        return bar

    def poll(self):
        if self._requested is None:
            return None
        if not self.connected:
            if self._client is not None:
                self._failed()
            return None
        with self._mutex:
            while self._queue:
                record = self._queue.popleft()
                try:
                    if type(record).__name__ == "SymbolMappingMsg":
                        self._map(record)
                    else:
                        bar = self._bar(record)
                        if bar is not None:
                            return bar
                except (AttributeError, ValueError, TypeError, OverflowError):
                    continue
        return None
