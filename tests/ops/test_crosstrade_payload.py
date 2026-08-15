"""Tests for ops/c1_rail/crosstrade_payload.py — production CrossTrade webhook payload
builder + sender (Option C, resolved 2026-07-18).

Promotes tests/rail_crosstrade/translator.py's already-tested payload shape
to a production module, adding destination parameterization
(destination=tradovate; per crosstrade.io/docs/webhooks/commands/place-order)
and a real send function. The `sender` parameter is dependency-injected so
tests never make a real network call — production code supplies the default
urllib-based sender; tests supply a capturing fake.
"""
from __future__ import annotations

import pytest

from crosstrade_payload import SendResult, build_crosstrade_payload, send_to_crosstrade


# ── payload construction ──────────────────────────────────────────────────

def test_entry_payload_default_has_no_destination_clause():
    """Backward-compatible default (NT8-forwarded path) — no destination= field."""
    text = build_crosstrade_payload(
        leg="entry", action="buy", symbol="MYM1!", qty=9, order_id="dj30_mym-entry-1",
        account="sim101", secret_key="test-secret", sl=44000.0, tp=44500.0,
    )
    assert "destination=" not in text
    assert "command=place;" in text
    assert "qty=9;" in text
    assert "instrument=MYM1!;" in text
    assert "stop_loss=44000.0;" in text
    assert "take_profit=44500.0;" in text
    assert "key=test-secret;" in text


def test_entry_payload_tradovate_destination_included():
    text = build_crosstrade_payload(
        leg="entry", action="buy", symbol="MYM1!", qty=9, order_id="dj30_mym-entry-1",
        account="TDFYSL100642026", secret_key="test-secret",
        sl=44000.0, tp=44500.0, destination="tradovate",
    )
    assert "destination=tradovate;" in text
    assert "command=place;" in text
    assert "flatten_first=true" in text  # entry leg still flattens-first (unchanged rule)


def test_add_payload_tradovate_no_flatten_first():
    text = build_crosstrade_payload(
        leg="add", action="buy", symbol="MYM1!", qty=67, order_id="dj30_mym-add-1",
        account="TDFYSL100642026", secret_key="test-secret", destination="tradovate",
    )
    assert "destination=tradovate;" in text
    assert "flatten_first" not in text  # only entry sets flatten_first


def test_exit_close_payload_omits_quantity_when_size_unknown():
    """The sizing host deliberately doesn't track live position size (spec:
    'this host does not manage exits') — qty=0 is its exit/flat sentinel,
    which means "flatten whatever's actually open," not "close zero"."""
    text = build_crosstrade_payload(
        leg="exit", action="close", symbol="MYM1!", qty=0, order_id="dj30_mym-exit-1",
        account="TDFYSL100642026", secret_key="test-secret", destination="tradovate",
    )
    assert "command=closeposition;" in text
    assert "destination=tradovate;" in text
    assert "quantity=" not in text


def test_exit_close_payload_includes_quantity_when_known():
    text = build_crosstrade_payload(
        leg="exit", action="close", symbol="MYM1!", qty=76, order_id="dj30_mym-exit-1",
        account="TDFYSL100642026", secret_key="test-secret", destination="tradovate",
    )
    assert "quantity=76;" in text


def test_unknown_destination_rejected():
    with pytest.raises(ValueError, match="destination"):
        build_crosstrade_payload(
            leg="entry", action="buy", symbol="MYM1!", qty=9, order_id="x",
            account="a", secret_key="s", destination="rithmic",
        )


# ── sending (dependency-injected transport; no real network in tests) ─────

def test_send_to_crosstrade_posts_to_expected_url():
    captured = {}

    def fake_sender(url: str, body: str, headers: dict) -> int:
        captured["url"] = url
        captured["body"] = body
        captured["headers"] = headers
        return 200

    result = send_to_crosstrade(
        "payload-body-text;", webhook_id="abc123", webhook_secret="xyz789",
        sender=fake_sender,
    )
    assert isinstance(result, SendResult)
    assert result.state == "accepted"
    assert result.http_status == 200
    assert captured["url"] == "https://app.crosstrade.io/v1/send/abc123/xyz789"
    assert captured["body"] == "payload-body-text;"
    assert captured["headers"]["Content-Type"] == "text/plain"


def test_send_to_crosstrade_propagates_non_200():
    def failing_sender(url, body, headers):
        return 500

    result = send_to_crosstrade(
        "x;", webhook_id="a", webhook_secret="b", sender=failing_sender)
    assert isinstance(result, SendResult)
    assert result.state == "accepted"
    assert result.http_status == 500
