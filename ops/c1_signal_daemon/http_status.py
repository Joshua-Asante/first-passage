"""Minimal health HTTP server for the daemon app (stdlib only)."""
from __future__ import annotations

import json
import logging
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Callable

from c1_signal_daemon.heartbeat import HeartbeatState

log = logging.getLogger(__name__)

HeartbeatGetter = Callable[[], HeartbeatState]


def make_handler(get_heartbeat: HeartbeatGetter) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt: str, *args) -> None:  # noqa: A003
            log.info("%s - " + fmt, self.address_string(), *args)

        def do_GET(self) -> None:  # noqa: N802
            if self.path.split("?", 1)[0] != "/":
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"not found")
                return
            body = json.dumps(get_heartbeat().as_json_dict()).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    return Handler


def serve_health(
    *,
    host: str,
    port: int,
    get_heartbeat: HeartbeatGetter,
) -> ThreadingHTTPServer:
    handler = make_handler(get_heartbeat)
    httpd = ThreadingHTTPServer((host, port), handler)
    return httpd
