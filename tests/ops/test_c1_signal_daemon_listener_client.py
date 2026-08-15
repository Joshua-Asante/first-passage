"""Listener client — URL shape + DI transport."""
from __future__ import annotations

import json

import pytest

from c1_signal_daemon.listener_client import ListenerClient, listener_post_url

TOKEN = "a" * 32


def test_listener_post_url_exact_path():
    url = listener_post_url("https://c1-rail.fly.dev", TOKEN)
    assert url == f"https://c1-rail.fly.dev/c1/{TOKEN}"


def test_path_token_min_len():
    with pytest.raises(ValueError, match="path_token"):
        listener_post_url("https://c1-rail.fly.dev", "short")


def test_post_b1_uses_transport():
    captured: list[tuple[str, bytes, dict]] = []

    def transport(url, body, headers):
        captured.append((url, body, headers))
        return 200, "dry_run: computed, not sent"

    client = ListenerClient(
        base_url="https://c1-rail.fly.dev",
        path_token=TOKEN,
        transport=transport,
    )
    status, body = client.post_b1(
        {
            "leg_id": "nas100_mnq",
            "signal_type": "entry",
            "bar_time": "t1",
            "close": 1.0,
            "stop_dist_pts": 2.0,
        }
    )
    assert status == 200
    assert "dry_run" in body
    assert captured[0][0].endswith(f"/c1/{TOKEN}")
    assert json.loads(captured[0][1].decode())["leg_id"] == "nas100_mnq"
