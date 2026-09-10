"""HTTP POST client for the origin-agnostic listener B1 path."""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any, Callable


Transport = Callable[[str, bytes, dict[str, str]], tuple[int, str]]


def serialize_b1_payload(payload: dict[str, Any]) -> bytes:
    """The exact request bytes used both by the journal and HTTP transport."""
    return json.dumps(payload, separators=(",", ":"), allow_nan=False).encode("utf-8")


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # A reservation permits one HTTP attempt, including on 301/302/303.
        return None


def default_transport(url: str, body: bytes, headers: dict[str, str]) -> tuple[int, str]:
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.build_opener(_NoRedirect()).open(req, timeout=30) as resp:
            return int(resp.status), resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        return int(exc.code), exc.read().decode("utf-8", errors="replace")


def listener_post_url(base_url: str, path_token: str) -> str:
    """Exact listener sizing path — /c1/<path_token> (no trailing slash)."""
    base = base_url.rstrip("/")
    if len(path_token) < 32:
        raise ValueError("path_token must be len >= 32")
    return f"{base}/c1/{path_token}"


class ListenerClient:
    """POSTs B1 JSON; never talks to CrossTrade."""

    def __init__(
        self,
        *,
        base_url: str,
        path_token: str,
        transport: Transport | None = None,
    ) -> None:
        self._url = listener_post_url(base_url, path_token)
        self._transport = transport or default_transport

    @property
    def url(self) -> str:
        return self._url

    def post_b1(self, payload: dict[str, Any]) -> tuple[int, str]:
        body = serialize_b1_payload(payload)
        headers = {"Content-Type": "application/json"}
        return self._transport(self._url, body, headers)
