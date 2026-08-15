"""CrossTrade webhook payload builder + sender — Option C production module.

Promotes the payload shape already proven in tests/rail_crosstrade/translator.py
(P5 golden-path infra) to a production component, adding the destination
parameterization CrossTrade's "Tradovate Goes GA" release requires
(crosstrade.io/docs/webhooks/commands/place-order: "destination=tradovate;"
on the same webhook path used for NT8) and an actual sender.

Auth (crosstrade.io/docs/api/webhook-trading, verified 2026-07-18): the
webhook URL is https://app.crosstrade.io/v1/send/{webhook_id}/{webhook_secret}
— "no difference between the way these webhooks are sent and any other
external webhook CrossTrade receives," so this module sending on the sizing
host's behalf is exactly as legitimate as TradingView doing so. The Secret
Key additionally rides in the payload body (key=...;).

`sender` is dependency-injected everywhere a real HTTP call would happen —
tests supply a capturing fake; send_to_crosstrade's default is the one place
a real urllib.request call is made, and only that path is untested by design
(it needs a live network + real credentials, exactly the class of thing this
module's own tests must not depend on).

Transport honesty (monitoring ADR 2026-07-22 M1): an HTTP response is
`accepted` (never execution-verified). A timeout / connection reset /
exception after bytes may have left is `unknown` — never auto-retried.
"""
from __future__ import annotations

import urllib.error
import urllib.request
from dataclasses import dataclass

_VALID_DESTINATIONS = frozenset({None, "tradovate"})


@dataclass(frozen=True)
class SendResult:
    """Honest CrossTrade transport outcome (not broker fill truth)."""
    state: str  # accepted | failed | unknown
    http_status: int | None = None
    error: str | None = None


def build_crosstrade_payload(
    *, leg: str, action: str, symbol: str, qty: int, order_id: str,
    account: str, secret_key: str,
    sl: float | None = None, tp: float | None = None,
    destination: str | None = None,
) -> str:
    """Build the CrossTrade semicolon key=value payload.

    `destination=None` omits the clause (NT8-forwarded path, unchanged from
    the original translator); `destination="tradovate"` adds the clause
    documented for direct-Tradovate routing. Any other value is a hard error
    — no silent fallback to an unverified destination string.
    """
    if destination not in _VALID_DESTINATIONS:
        raise ValueError(
            f"unknown destination {destination!r}; valid: {sorted(d for d in _VALID_DESTINATIONS if d)}")

    parts = [f"key={secret_key}"]

    if leg == "exit" and action == "close":
        parts.append("command=closeposition")
        parts.extend([f"account={account}", f"instrument={symbol}"])
        if destination:
            parts.append(f"destination={destination}")
        if qty > 0:
            # qty=0 is the sizing host's exit/flat sentinel (it deliberately
            # does not track live position size — spec: "this host does not
            # manage exits"). Omitting quantity lets closeposition flatten
            # whatever is actually open, rather than trusting stale bookkeeping.
            parts.append(f"quantity={qty}")
        return ";".join(parts) + ";"

    parts.append("command=place")
    parts.extend([
        f"account={account}", f"instrument={symbol}", f"action={action}",
        f"qty={qty}", "order_type=market", "tif=day", f"order_id={order_id}",
    ])
    if destination:
        parts.append(f"destination={destination}")
    if sl is not None:
        parts.append(f"stop_loss={sl}")
    if tp is not None:
        parts.append(f"take_profit={tp}")
    if leg == "entry":
        parts.append("flatten_first=true")
    return ";".join(parts) + ";"


def _urllib_sender(url: str, body: str, headers: dict) -> int:
    """The one real-network path in this module — not covered by unit tests."""
    req = urllib.request.Request(url, data=body.encode("utf-8"), headers=headers,
                                  method="POST")
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status


def send_to_crosstrade(
    payload_text: str, *, webhook_id: str, webhook_secret: str,
    sender=None,
) -> SendResult:
    """POST the payload to CrossTrade's webhook URL.

    Returns a SendResult:
      - accepted: an HTTP response was received (status recorded; never means
        CrossTrade validated or Tradovate filled)
      - failed: connection refused / DNS / clear pre-send failure
      - unknown: timeout / reset / exception after bytes may have left — do
        not auto-retry; reconcile before any operator retry

    `sender(url, body, headers) -> int` is dependency-injected; defaults to a
    real urllib POST. Tests always supply a fake — this function never makes
    a network call under pytest.
    """
    if sender is None:
        sender = _urllib_sender
    url = f"https://app.crosstrade.io/v1/send/{webhook_id}/{webhook_secret}"
    headers = {"Content-Type": "text/plain"}
    try:
        status = sender(url, payload_text, headers)
        return SendResult(state="accepted", http_status=int(status))
    except (TimeoutError, urllib.error.URLError) as exc:
        # Bytes may already have left — treat as unknown, never auto-retry.
        return SendResult(state="unknown", error=f"{type(exc).__name__}: {exc}")
    except OSError as exc:
        # Connection refused / reset mid-flight — unknown if post may exist.
        return SendResult(state="unknown", error=f"{type(exc).__name__}: {exc}")
    except Exception as exc:  # noqa: BLE001 — fail honest on surprise
        return SendResult(state="unknown", error=f"{type(exc).__name__}: {exc}")
