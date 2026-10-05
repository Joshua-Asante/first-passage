"""Missed-heartbeat monitor for the book runtime and its incident notifier (D-MON-1).

Card: docs/briefs/handoffs/2026-10-03-dmon-missed-heartbeat-monitor-card-DRAFT.md (FROZEN
2026-10-05), §3. A ``HeartbeatPinger`` pings one Grafana IRM heartbeat integration, and IRM
pages Joshua when the pings stop. Pings follow observed progress only; there is no timer
thread, so a dead, hung or storage-failed loop stops pinging and the provider-side timeout
pages (§2).

- ``step_with_heartbeat`` marks after a ``FourLegEvaluateLoop.step`` and an owner status
  read both return (§3.1). HALTED and INTERVENTION still count as progress.
- ``notifier_round_with_heartbeat`` marks after a notifier ``run_once`` only when the
  notifier's ``progress()`` count increased (§3.9); never on its clock-time liveness.
- Each side has its own reference and integration; ``build_pingers`` refuses a shared one.

Independence (§0.5 item 7): this module imports nothing from the notifier, the IRM channel,
the owner or any broker, dispatch, arm or config-write surface, and it keeps no journal or
persisted state. The transport is written here on purpose rather than imported. The URL is
resolved from an ``env:`` reference once, held in one private attribute and never appears in
``repr``, exception text, logs or counters. Host wiring is TB-I3-HOST's (P7, P9); nothing
here starts a process.
"""
from __future__ import annotations

from collections.abc import Callable, Mapping
import logging
import math
import os
import ssl
import threading
import time
import urllib.error
import urllib.parse
import urllib.request


RUNTIME_SECRET_REF = "env:FP_DMON_GRAFANA_IRM_HEARTBEAT_URL"
NOTIFIER_SECRET_REF = "env:FP_DMON_GRAFANA_IRM_NOTIFIER_HEARTBEAT_URL"
HOST_SUFFIX = ".grafana.net"
PATH_SUFFIX = "/heartbeat/"  # UNVERIFIED for Formatted Webhook; HB-L1 confirms (§0.5 item 1)
MAX_RESPONSE_BYTES = 64 * 1024
BINDING_KEYS = frozenset({"secret_ref", "period_s", "timeout_s"})

_LOG = logging.getLogger(__name__)


class HeartbeatConfigError(ValueError):
    """A refused reference, URL or binding. The text names the rule, never a URL."""


def resolve_secret_ref(secret_ref, environ=None):
    """The value behind ``env:NAME``. ``secret:NAME`` waits for a store convention (OQ-5)."""
    if not isinstance(secret_ref, str):
        raise HeartbeatConfigError("secret_ref must be a string reference")
    scheme, _, name = secret_ref.partition(":")
    if scheme == "secret" and name:
        raise HeartbeatConfigError("secret reference " + secret_ref
                                   + " refused: no secret store convention exists (OQ-5)")
    if scheme != "env" or not name or not name.replace("_", "").isalnum():
        raise HeartbeatConfigError("secret_ref must name env:NAME, never a value")
    value = (os.environ if environ is None else environ).get(name)
    if not value:
        raise HeartbeatConfigError("secret reference " + secret_ref + " is not set")
    return value


def url_refusal(url, *, allow_loopback_http=False):
    """The name of the first failed URL rule, or None. Never echoes the URL (§3.4)."""
    try:
        parts = urllib.parse.urlsplit(url)
        host = parts.hostname or ""
        userinfo = parts.username is not None or parts.password is not None or "@" in parts.netloc
        _ = parts.port  # raises ValueError on an invalid port
    except (TypeError, ValueError):
        return "unparseable"
    loopback = allow_loopback_http and parts.scheme == "http" and host == "127.0.0.1"
    if parts.scheme != "https" and not loopback:
        return "scheme must be https"
    if userinfo:
        return "userinfo is refused"
    if not loopback and not host.endswith(HOST_SUFFIX):
        return "host must end in " + HOST_SUFFIX
    if not parts.path.endswith(PATH_SUFFIX) or parts.query or parts.fragment:
        return "path must end in " + PATH_SUFFIX + " with no query"
    return None


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):  # noqa: ARG002 - a redirect is never followed
        return None


def _positive(name, value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) \
            or value <= 0:
        raise HeartbeatConfigError(name + " must be a positive finite number")
    return float(value)


class HeartbeatPinger:
    """Progress-driven pings to one heartbeat integration (§3.2).

    ``mark_progress`` returns at once. It starts one short-lived daemon thread for one bounded
    POST only when no send is in flight and the last send began at least ``period_s`` ago;
    otherwise it does nothing and nothing is queued. A failed send is counted and logged by
    exception class only; it never raises into the caller.
    """

    def __init__(self, secret_ref, *, period_s, timeout_s,
                 clock: Callable[[], float] = time.monotonic,
                 environ: Mapping[str, str] | None = None, allow_loopback_http=False):
        self.period_s = _positive("period_s", period_s)
        self.timeout_s = _positive("timeout_s", timeout_s)
        if self.timeout_s >= self.period_s:
            raise HeartbeatConfigError("timeout_s must be below period_s (§3.3 (a))")
        url = resolve_secret_ref(secret_ref, environ)
        refusal = url_refusal(url, allow_loopback_http=allow_loopback_http)
        if refusal:
            raise HeartbeatConfigError("heartbeat URL behind " + secret_ref + " refused: "
                                       + refusal)
        self.secret_ref = secret_ref
        self.__url = url
        self._clock = clock
        self._lock = threading.Lock()
        self._idle = threading.Event()
        self._idle.set()
        self._last_progress = None
        self._last_send_start = None
        self._seen_count = None
        self._stats = {"marks": 0, "sends_started": 0, "sends_ok": 0, "sends_failed": 0,
                       "last_outcome": None, "last_send_start": None}
        self._opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({}),
            urllib.request.HTTPSHandler(context=ssl.create_default_context()),
            _NoRedirect())

    def __repr__(self):
        return "HeartbeatPinger(secret_ref=%r, period_s=%r, timeout_s=%r)" % (
            self.secret_ref, self.period_s, self.timeout_s)

    __str__ = __repr__

    def _same_target(self, other):
        return isinstance(other, HeartbeatPinger) and other.__url == self.__url

    # -- progress ------------------------------------------------------------------------------

    def mark_progress(self):
        """Record progress; start one bounded send if none is in flight and P has passed."""
        with self._lock:
            now = self._clock()
            self._last_progress = now
            self._stats["marks"] += 1
            if not self._idle.is_set() or (self._last_send_start is not None
                                           and now - self._last_send_start < self.period_s):
                return
            self._last_send_start = now
            self._stats["sends_started"] += 1
            self._stats["last_send_start"] = now
            self._idle.clear()
        try:
            threading.Thread(target=self._send, name="book-heartbeat-send", daemon=True).start()
        except Exception as exc:  # noqa: BLE001 - a thread that cannot start is a failed send
            self._finish(type(exc).__name__)

    def observe_count(self, count):
        """Record a progress count; True when it increased since the previous observation."""
        if isinstance(count, bool) or not isinstance(count, int) or count < 0:
            raise HeartbeatConfigError("progress count must be a non-negative integer")
        with self._lock:
            previous, self._seen_count = self._seen_count, count
        return previous is not None and count > previous

    @property
    def has_count(self):
        return self._seen_count is not None

    # -- transport -----------------------------------------------------------------------------

    def _send(self):
        outcome = "ok"
        request = urllib.request.Request(self.__url, data=b"", method="POST")
        try:
            with self._opener.open(request, timeout=self.timeout_s) as response:
                response.read(MAX_RESPONSE_BYTES)
                if not 200 <= response.status < 300:
                    outcome = "HTTPStatus"
        except urllib.error.HTTPError as exc:  # carries the URL: mapped here, never propagated
            outcome = "HTTPError"
            exc.close()
        except Exception as exc:  # noqa: BLE001 - timeout, refusal, DNS or TLS: class name only
            outcome = type(exc).__name__
        self._finish(outcome)

    def _finish(self, outcome):
        with self._lock:
            self._stats["last_outcome"] = outcome
            self._stats["sends_ok" if outcome == "ok" else "sends_failed"] += 1
            self._idle.set()
        if outcome != "ok":
            _LOG.warning("heartbeat send failed: %s", outcome)

    def drain(self, timeout=None):
        """Wait for an in-flight send to finish; True when none is in flight."""
        return self._idle.wait(timeout)

    def stats(self):
        """Counters and the last outcome class; never the URL."""
        with self._lock:
            return dict(self._stats, in_flight=not self._idle.is_set())


def step_with_heartbeat(loop, pinger, *, now, read_status):
    """``loop.step(now=now)``, then ``read_status()``, then one progress mark (§3.1).

    The step result is returned unchanged. An exception from either call propagates unchanged
    and no mark is set.
    """
    result = loop.step(now=now)
    read_status()
    pinger.mark_progress()
    return result


def notifier_round_with_heartbeat(notifier, pinger):
    """``notifier.run_once()``, then a mark only if ``notifier.progress()`` increased (§3.9).

    The first call reads the count before the round to set the baseline. An exception from
    ``run_once`` or ``progress`` propagates unchanged and no mark is set. Duck-typed: nothing
    is imported from the notifier.
    """
    if not pinger.has_count:
        pinger.observe_count(notifier.progress())
    notifier.run_once()
    if pinger.observe_count(notifier.progress()):
        pinger.mark_progress()


def _binding(raw, name):
    if not isinstance(raw, Mapping) or set(raw) != BINDING_KEYS:
        raise HeartbeatConfigError(name + " binding must hold exactly secret_ref, period_s and "
                                   "timeout_s (inline values are refused)")
    return raw


def build_pingers(runtime_binding, notifier_binding, *, environ=None,
                  allow_loopback_http=False, clock=time.monotonic):
    """The runtime and notifier pingers from their bindings (§3.7).

    Equal references or equal resolved URLs are refused: one live side would otherwise mask
    the other.
    """
    runtime = _binding(runtime_binding, "runtime")
    notifier = _binding(notifier_binding, "notifier")
    if runtime["secret_ref"] == notifier["secret_ref"]:
        raise HeartbeatConfigError("runtime and notifier heartbeats need separate references")
    pingers = tuple(HeartbeatPinger(binding["secret_ref"], period_s=binding["period_s"],
                                    timeout_s=binding["timeout_s"], clock=clock,
                                    environ=environ, allow_loopback_http=allow_loopback_http)
                    for binding in (runtime, notifier))
    if pingers[0]._same_target(pingers[1]):
        raise HeartbeatConfigError("runtime and notifier heartbeats resolve to the same URL")
    return pingers
