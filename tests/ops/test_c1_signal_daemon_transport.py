"""Exercise real urllib response handling without opening a socket."""
from email.message import Message
import io
import urllib.request
from urllib.response import addinfourl

import pytest

from c1_signal_daemon.listener_client import default_transport


@pytest.mark.parametrize("code", [301, 302, 303, 307, 308])
def test_redirect_is_terminal_without_a_second_http_attempt(monkeypatch, code):
    attempts = []

    def offline_open(self, request):
        attempts.append((request.get_method(), request.full_url))
        headers = Message()
        headers["Location"] = "https://redirect.invalid/other"
        response = addinfourl(io.BytesIO(b"redirect refused"), headers,
                             request.full_url, code if len(attempts) == 1 else 200)
        response.msg = "Offline fixture"
        return response

    monkeypatch.setattr(urllib.request.HTTPSHandler, "https_open", offline_open)
    status, body = default_transport("https://offline.invalid/c1/test", b"{}",
                                     {"Content-Type": "application/json"})
    assert attempts == [("POST", "https://offline.invalid/c1/test")]
    assert status == code
    assert body == "redirect refused"
