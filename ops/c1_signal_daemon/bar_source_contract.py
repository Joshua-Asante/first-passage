"""Provider-neutral BarSource contract for a production feed adapter (Track A A9-PREP).

Owners: the frozen feed-equivalence spec
(``docs/spec/2026-09-27-cme-execution-feed-equivalence-test-DRAFT.md`` §4, §5, §7,
§16.2) and the S2b build ADR §2 Reconnect / Staleness / Fail-closed rows
(``docs/adr/2026-08-08-s2b-signal-daemon-build.md``).

A provider adapter implements only ``BarTransport``. ``ContractBarSource`` wraps it,
satisfies ``feed.BarSource`` and owns every rule below, so no adapter can weaken one:

* only completed bars, keyed by bar-open UTC on the 15-minute grid, forwarded in
  ``ts`` order, at most once, and only by ``bar_open + BAR_PERIOD + BAR_SLACK`` (M5);
* aware timestamps only: naive and DST gap/fold wall times are refused; nothing in
  the America/New_York daily break or weekend, or outside the bound product session;
* no empty, synthetic, revised, out-of-order or other-contract bar is forwarded
  (§4.3, M7, R-MAP-2); each refusal is counted and recorded in ``events``;
* a revision of a pending (not yet forwarded) bar withdraws the slot: neither value
  is forwarded and the consumer halts on the absent slot; a revision of an already
  forwarded bar latches ``REFUSED`` (operator ruling on A9-PREP Q1);
* bars are forwarded only while connected; the source is unhealthy while
  disconnected or stale (``2 x bar_period + 30 s``) and reconnects with capped backoff;
* a rejected credential (at authentication, renewal or mid-stream) or an expired
  symbol binding latches ``REFUSED``: no retry, no fallback contract, no bar until a
  new source is constructed.

Recovery grants no permission: consumer halt state is not this module's.
Out of scope: building 15-minute bars from finer constituents (spec OPEN-1),
provider code, credentials (a transport resolves its own credential reference).
"""
from __future__ import annotations

import re
from collections import Counter, deque
from dataclasses import dataclass
from datetime import datetime, time, timedelta, timezone
from typing import Callable, Protocol, Sequence
from zoneinfo import ZoneInfo

from c1_signal_daemon.book_protocol import BAR_PERIOD, BAR_SLACK
from c1_signal_daemon.book_validation import validate_bar
from c1_signal_daemon.feed import Bar, feed_healthy

NEW_YORK = ZoneInfo("America/New_York")
SESSION_OPEN = time(18)   # Sunday-Friday 18:00-17:00 ET; daily break 17:00-18:00 ET
SESSION_CLOSE = time(17)
# Root and exchange per book leg (spec §16.2 §5 row, ADOPTED; note §2).
LEG_FEEDS = {
    "aegis_6j": ("6J", "CME"),
    "dj30_mym_p250": ("MYM", "CBOT"),
    "vanguard_mgc": ("MGC", "COMEX"),
    "orb_mnq_v7": ("MNQ", "CME"),
}
_RETAIN = timedelta(days=1)
_EVENT_LOG = 4096


class AuthRejected(Exception):
    """The provider rejected the credential. Never retried: refusal latches."""


class TransportError(Exception):
    """Transient connection or authentication-service failure. Retried with backoff."""


@dataclass(frozen=True)
class Lease:
    """An authenticated session; the credential value never enters this module."""

    expires_at: datetime


@dataclass(frozen=True)
class DeliveredBar:  # pylint: disable=too-many-instance-attributes
    """One decoded provider bar, not yet admitted."""

    symbol: str            # provider-native code
    stamp: datetime        # meaning set by SymbolBinding.stamp
    open: float
    high: float
    low: float
    close: float
    volume: float
    final: bool = True           # provider marks the bar complete
    trade_evidence: bool = True  # False: synthetic, filled-forward or no-trade


class BarTransport(Protocol):
    """The provider-specific port; every method may raise AuthRejected or TransportError."""

    def authenticate(self) -> Lease:
        """Open an authenticated session."""

    def renew(self, lease: Lease) -> Lease:
        """Renew the session before ``lease.expires_at``."""

    def connect(self, lease: Lease) -> None:
        """Open the stream for the bound symbol."""

    def receive(self) -> Sequence[DeliveredBar]:
        """Return bars delivered since the last call without blocking."""

    def close(self) -> None:
        """Close the stream."""


def _aware(value: datetime) -> bool:
    return isinstance(value, datetime) and value.utcoffset() is not None


@dataclass(frozen=True)
class SymbolBinding:
    """One provider code bound to exactly one dated contract until ``valid_until`` (R-MAP-2)."""

    leg_id: str
    exchange: str
    provider_code: str
    venue_contract: str
    valid_until: datetime  # contract expiry or roll under the live selection rule (OPEN-3)
    stamp: str             # "open" or "close": the provider's bar-time convention (§4.1)

    def __post_init__(self):
        if self.leg_id not in LEG_FEEDS:
            raise ValueError(f"unknown leg {self.leg_id!r}")
        root, exchange = LEG_FEEDS[self.leg_id]
        if self.exchange != exchange:
            raise ValueError(f"{self.leg_id} trades on {exchange}, not {self.exchange!r}")
        if not re.fullmatch(re.escape(root) + r"[FGHJKMNQUVXZ]\d{1,2}", str(self.venue_contract)):
            raise ValueError(f"venue_contract must be a dated {root} contract")
        if not isinstance(self.provider_code, str) or not self.provider_code.strip():
            raise ValueError("provider_code required")
        if not _aware(self.valid_until):
            raise ValueError("valid_until must be timezone-aware")
        if self.stamp not in ("open", "close"):
            raise ValueError("stamp must be 'open' or 'close'")


@dataclass(frozen=True)
class TransportPolicy:
    """Reconnect backoff and renewal margin (later binding inside the frozen timing bounds)."""

    backoff_initial_s: float
    backoff_max_s: float
    renew_margin_s: float

    def __post_init__(self):
        # A cap above BAR_SLACK could skip a bar's whole M5 delivery window.
        if not 0 < self.backoff_initial_s <= self.backoff_max_s <= BAR_SLACK.total_seconds():
            raise ValueError("require 0 < backoff_initial_s <= backoff_max_s <= BAR_SLACK")
        if not self.renew_margin_s > 0:
            raise ValueError("renew_margin_s must be > 0")

    def delay(self, attempt: int) -> timedelta:
        """Capped exponential backoff for the given zero-based attempt."""
        return timedelta(seconds=min(self.backoff_initial_s * 2 ** min(attempt, 32),
                                     self.backoff_max_s))


def bar_open_utc(stamp: datetime, convention: str) -> datetime:
    """Translate a provider stamp to the consumer key; refuse naive, DST-ambiguous or off-grid."""
    if not _aware(stamp) or stamp.replace(fold=0).utcoffset() != stamp.replace(fold=1).utcoffset():
        raise ValueError("stamp must be an unambiguous aware instant")
    ts = stamp.astimezone(timezone.utc) - (BAR_PERIOD if convention == "close" else timedelta(0))
    if ts.minute % 15 or ts.second or ts.microsecond:
        raise ValueError("stamp is off the 15-minute grid")
    return ts


def in_product_frame(ts: datetime) -> bool:
    """True if a bar opening at ``ts`` lies in the Sunday-Friday 18:00-17:00 ET frame."""
    local = ts.astimezone(NEW_YORK)
    day, clock = local.weekday(), local.time()
    in_break = SESSION_CLOSE <= clock < SESSION_OPEN
    return not (day == 5 or (day == 6 and clock < SESSION_OPEN)
                or (day == 4 and clock >= SESSION_CLOSE) or in_break)


class ContractBarSource:  # pylint: disable=too-many-instance-attributes
    """``feed.BarSource`` for one leg over a provider transport; owns every contract rule.

    ``session_window(ts)`` returns the bound product session containing ``ts`` (an object
    with ``opens_at``/``closes_at``, e.g. a ratified calendar row) or ``None`` outside coverage.
    """

    feed_mode = "contract"

    def __init__(self, transport: BarTransport, *, binding: SymbolBinding,
                 policy: TransportPolicy, session_window: Callable[[datetime], object | None],
                 clock: Callable[[], datetime]):
        if type(binding) is not SymbolBinding or type(policy) is not TransportPolicy:
            raise TypeError("typed SymbolBinding and TransportPolicy required")
        self.binding, self._transport, self._policy = binding, transport, policy
        self._session_window, self._clock = session_window, clock
        self.state, self.refusal = "DISCONNECTED", None
        self.last_bar_ts: datetime | None = None
        self.events: deque[tuple[datetime, str, dict]] = deque(maxlen=_EVENT_LOG)
        self.counts: Counter[str] = Counter()  # e.g. M7 revisions seen in the raw stream
        self._lease: Lease | None = None
        self._attempt, self._retry_at = 0, None
        self._pending: dict[datetime, Bar] = {}
        self._delivered: dict[datetime, Bar] = {}
        self._withdrawn: set[datetime] = set()

    @property
    def connected(self) -> bool:
        """True only while authenticated and streaming."""
        return self.state == "CONNECTED"

    def healthy(self, now: datetime | None = None) -> bool:
        """S2b staleness rule; never healthy once refused."""
        return self.state != "REFUSED" and feed_healthy(
            connected=self.connected, last_bar_ts=self.last_bar_ts,
            now=now or self._now(), bar_period_s=BAR_PERIOD.total_seconds())

    def poll(self) -> Bar | None:
        """Return the next admitted completed bar in ``ts`` order, or ``None``."""
        now = self._now()
        if self.state == "REFUSED":
            return None
        if now >= self.binding.valid_until:
            self._refuse("binding_expired", now)
            return None
        self._maintain(now)
        if self.connected:
            try:
                delivered = self._transport.receive()
            except AuthRejected:
                self._refuse("auth_rejected", now)
            except TransportError:
                self._disconnect("transport_error", now)
            else:
                for item in delivered:
                    reason = self._admit(item, now)
                    if reason:
                        self._event(now, reason, item=item)
        return self._next(now)

    def _now(self) -> datetime:
        now = self._clock()
        if not _aware(now):
            raise ValueError("clock must return an aware datetime")
        return now

    def _event(self, now, kind, **detail):
        self.counts[kind] += 1
        self.events.append((now, kind, detail))

    def _lease_ok(self, now) -> bool:
        lease = self._lease
        return (type(lease) is Lease and _aware(lease.expires_at)
                and lease.expires_at - timedelta(seconds=self._policy.renew_margin_s) > now)

    def _maintain(self, now):
        if self.connected and not self._lease_ok(now):
            try:
                self._lease = self._transport.renew(self._lease)
            except AuthRejected:
                self._refuse("auth_rejected", now)
                return
            except TransportError:
                self._lease = None
            if not self._lease_ok(now):
                self._disconnect("renewal_failed", now)
                return
            self._event(now, "renewed")
        if self.state != "DISCONNECTED" or (self._retry_at and now < self._retry_at):
            return
        try:
            self._lease = self._transport.authenticate()
            if not self._lease_ok(now):
                raise TransportError("lease shorter than the renewal margin")
            self._transport.connect(self._lease)
        except AuthRejected:
            self._refuse("auth_rejected", now)
            return
        except TransportError:
            self._lease = None
            self._schedule_retry(now, "connect_failed")
            return
        self.state, self._attempt, self._retry_at = "CONNECTED", 0, None
        self._event(now, "connected")

    def _schedule_retry(self, now, kind):
        self._retry_at = now + self._policy.delay(self._attempt)
        self._attempt += 1
        self._event(now, kind, retry_at=self._retry_at)

    def _close(self):
        try:
            self._transport.close()
        except (AuthRejected, TransportError):
            pass

    def _disconnect(self, reason, now):
        self._close()
        self.state, self._lease = "DISCONNECTED", None
        self._schedule_retry(now, "disconnected:" + reason)

    def _refuse(self, reason, now):
        self._close()
        self.state, self.refusal, self._lease = "REFUSED", reason, None
        self._pending.clear()
        self._event(now, "refused:" + reason)

    def _admit(self, item, now) -> str | None:  # pylint: disable=too-many-return-statements
        """Queue a delivered bar, or return the reason it is never forwarded."""
        if type(item) is not DeliveredBar:
            return "invalid_bar"
        if type(item.final) is not bool or type(item.trade_evidence) is not bool:
            return "invalid_metadata"
        if item.symbol != self.binding.provider_code:
            return "foreign_symbol"
        try:
            ts = bar_open_utc(item.stamp, self.binding.stamp)
        except ValueError:
            return "invalid_time"
        bar = Bar(ts, item.open, item.high, item.low, item.close, item.volume)
        if validate_bar(bar) is not None:
            return "invalid_bar"
        if ts in self._withdrawn:
            return "withdrawn"
        known = self._delivered.get(ts) or self._pending.get(ts)
        if known is not None:
            if known == bar:
                return "duplicate"
            if ts in self._delivered:
                self._refuse("revision_after_delivery", now)
            else:  # conflicting pending finals: forward neither (absent is absent)
                self._pending.pop(ts)
                self._withdrawn.add(ts)
            return "revision"
        if self.last_bar_ts is not None and ts < self.last_bar_ts:
            return "out_of_order"
        if not item.final or now < ts + BAR_PERIOD:
            return "incomplete"
        if not item.trade_evidence or item.volume == 0:
            return "no_trade_evidence"
        window = self._session_window(ts)
        if (not in_product_frame(ts) or window is None
                or not window.opens_at <= ts < window.closes_at):
            return "outside_session"
        if now > ts + BAR_PERIOD + BAR_SLACK:
            return "late"
        self._pending[ts] = bar
        return None

    def _next(self, now) -> Bar | None:
        while self.connected and self._pending:
            ts = min(self._pending)
            bar = self._pending.pop(ts)
            if now > ts + BAR_PERIOD + BAR_SLACK:
                self._event(now, "late", ts=ts)
                continue
            self._delivered = {t: b for t, b in self._delivered.items() if t > ts - _RETAIN}
            self._withdrawn = {t for t in self._withdrawn if t > ts - _RETAIN}
            self._delivered[ts] = bar
            self.last_bar_ts = ts
            return bar
        return None
