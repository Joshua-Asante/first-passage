"""Grafana Cloud IRM Formatted-webhook channel for the book incident notifier.

Card: docs/briefs/handoffs/2026-10-03-dmon-grafana-irm-binding-card-DRAFT.md (FROZEN 2026-10-04),
§3.2-§3.3. Each publish posts one important alert whose ``alert_uid`` is the incident key, so
IRM groups every retry of one incident while its alert group is open. The 60 s escalation runs
provider-side through Joshua's Important notification rules (C-2); the rail sends one webhook
per round. A 2xx is provider acceptance only, never delivery.

The integration URL embeds the integration token, so the whole URL is the secret. It is
resolved once from a reference at construction and lives only in a closure: never in
``repr``, ``str``, exception text, the evidence digest, the payload or the journal.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import ssl
import urllib.error
import urllib.parse
import urllib.request

try:  # package import (tests, the live-page driver); a plain-path import is the fallback
    from .book_incident_notifier import ChannelSpec, NotifierConfigError, PublishResult
except ImportError:
    from book_incident_notifier import ChannelSpec, NotifierConfigError, PublishResult
try:
    from c1_rail_telemetry import assert_no_secrets
except ImportError:  # pragma: no cover - exercised only outside the rail's path setup
    from .c1_rail_telemetry import assert_no_secrets


KIND = "grafana_irm"
# The important marker (card §0.5 item 3): fixed, with no constructor or config override.
SEVERITY = "critical"
STATE = "alerting"  # the rail never sends "ok": recovery is attended (HR §3)
TITLE = "First Passage book incident: "
QUALIFICATION_LABEL = "[QUALIFICATION TEST] "
WEBHOOK_PATH = "/integrations/v1/formatted_webhook/"
HOST_SUFFIX = ".grafana.net"
MAX_RESPONSE_BYTES = 64 * 1024
_KEY = re.compile(r"^[0-9a-f]{64}$")
_UNKNOWN_STATUSES = {408, 429}


class GrafanaIRMTransportError(Exception):
    """Timeout, connection, DNS or TLS failure. Carries no text: the core journals the class
    name only, and the URL must never reach exception text."""


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):  # noqa: ARG002 - a redirect is never followed
        return None


def resolve_secret_ref(secret_ref):
    """The value behind ``env:NAME``. ``secret:NAME`` waits for a store convention (OQ-5).

    A refusal names the reference, never a value.
    """
    scheme, _, name = secret_ref.partition(":")
    if scheme != "env":
        raise NotifierConfigError("secret reference " + secret_ref
                                  + " refused: no secret store convention exists (OQ-5)")
    value = os.environ.get(name)
    if not value:
        raise NotifierConfigError("secret reference " + secret_ref + " is not set")
    return value


def _url_refusal(url, allow_loopback_http):
    """The name of the first failed URL rule, or None. Never echoes the URL."""
    try:
        parts = urllib.parse.urlsplit(url)
        host = parts.hostname or ""
        userinfo = parts.username is not None or parts.password is not None or "@" in parts.netloc
        _ = parts.port  # raises ValueError on an invalid port
    except ValueError:
        return "unparseable"
    loopback = allow_loopback_http and parts.scheme == "http" and host == "127.0.0.1"
    if parts.scheme != "https" and not loopback:
        return "scheme must be https"
    if userinfo:
        return "userinfo is refused"
    if not loopback and not host.endswith(HOST_SUFFIX):
        return "host must end in " + HOST_SUFFIX
    if WEBHOOK_PATH not in parts.path:
        return "path must be a formatted webhook integration path"
    return None


def body(idempotency_key, payload, *, qualification_test=False):
    """The Formatted-webhook body (card §3.2): no URL, raw incident id, account or figure."""
    reason, detected_at = str(payload["reason"]), str(payload["detected_at"])
    return {
        "alert_uid": idempotency_key,
        "title": (QUALIFICATION_LABEL if qualification_test else "") + TITLE + reason,
        "message": "reason: %s; detected_at: %s; key: %s" % (reason, detected_at,
                                                             idempotency_key[:12]),
        "state": STATE,
        "severity": SEVERITY,
    }


class GrafanaIRMChannel:
    """A delivering ``grafana_irm`` channel (card §3.2). ``publish`` returns acceptance only."""
    kind = KIND

    def __init__(self, name, secret_ref, *, publish_timeout_s, timeout_s=None,
                 qualification_test=False, allow_loopback_http=False):
        spec = ChannelSpec(name, KIND, secret_ref)
        if (isinstance(publish_timeout_s, bool) or not isinstance(publish_timeout_s, (int, float))
                or not math.isfinite(publish_timeout_s) or publish_timeout_s <= 0):
            raise NotifierConfigError("publish_timeout_s must be a positive finite number")
        timeout_s = publish_timeout_s / 2 if timeout_s is None else timeout_s
        if (isinstance(timeout_s, bool) or not isinstance(timeout_s, (int, float))
                or not math.isfinite(timeout_s) or not 0 < timeout_s < publish_timeout_s):
            raise NotifierConfigError("transport timeout must be positive and below publish_timeout_s")
        self.name = spec.name
        self.secret_ref = spec.secret_ref
        self.timeout_s = float(timeout_s)
        self.qualification_test = bool(qualification_test)
        self.last_status = None  # the last HTTP status seen; Q7 (e) records it
        url = resolve_secret_ref(spec.secret_ref)
        refusal = _url_refusal(url, allow_loopback_http)
        if refusal:
            raise NotifierConfigError("integration URL refused: " + refusal)
        self._post = _poster(url, self.timeout_s)

    def __repr__(self):
        return "GrafanaIRMChannel(name=%r, secret_ref=%r)" % (self.name, self.secret_ref)

    __str__ = __repr__

    def publish(self, idempotency_key, payload):
        if not isinstance(idempotency_key, str) or not _KEY.match(idempotency_key):
            raise ValueError("incident key must be a sha256 hex digest")
        message = body(idempotency_key, payload, qualification_test=self.qualification_test)
        assert_no_secrets(message)
        self.last_status = None  # a transport failure must not report an earlier status
        status, content = self._post(json.dumps(message, sort_keys=True).encode("utf-8"))
        self.last_status = status
        if 200 <= status < 300:
            return PublishResult("accepted", evidence_digest=hashlib.sha256(
                b"%d\x00" % status + content).hexdigest())
        if status in _UNKNOWN_STATUSES or status >= 500:
            return PublishResult("unknown")
        if 300 <= status < 500:
            return PublishResult("rejected")
        return PublishResult("unknown")


def _poster(url, timeout_s):
    """A closure that POSTs one body and returns ``(status, capped body)``; holds the URL.

    Redirects are never followed and environment proxies are ignored, so the URL goes to its
    own host only; HTTPS uses default certificate verification.
    """
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({}),
        urllib.request.HTTPSHandler(context=ssl.create_default_context()),
        _NoRedirect())

    def post(data):
        request = urllib.request.Request(url, data=data, method="POST",
                                         headers={"Content-Type": "application/json"})
        failed = False
        try:
            with opener.open(request, timeout=timeout_s) as response:
                return response.status, response.read(MAX_RESPONSE_BYTES)
        except urllib.error.HTTPError as exc:  # carries the URL: mapped here, never propagated
            status = exc.code
            exc.close()
        except Exception:  # noqa: BLE001 - raised below, outside this block, with no context
            failed = True
        if failed:
            raise GrafanaIRMTransportError()
        return status, b""

    return post
