"""Daemon entrypoint — feed + evaluate loop + health HTTP.

Warm default: emit_enabled=false. Live Databento adapter is optional at import
time so unit tests stay vendor-free.
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

# Standalone-run bootstrap (mirror c1_rail_http_server).
_REPO_ROOT = Path(__file__).resolve().parents[2]
_DAEMON_DIR = Path(__file__).resolve().parent
for _p in (str(_REPO_ROOT / "ops"), str(_DAEMON_DIR), str(_REPO_ROOT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from c1_signal_daemon.evaluate_loop import EvaluateLoop  # noqa: E402
from c1_signal_daemon.feed import Bar  # noqa: E402
from c1_signal_daemon.http_status import serve_health  # noqa: E402
from c1_signal_daemon.listener_client import ListenerClient  # noqa: E402
from c1_signal_daemon.strategy_protocol import NullStrategy  # noqa: E402

log = logging.getLogger("c1_signal_daemon")


class IdleBarSource:
    """Connected placeholder until a live Databento session is wired."""

    def __init__(self) -> None:
        self._connected = True

    @property
    def connected(self) -> bool:
        return self._connected

    def poll(self) -> Bar | None:
        return None


def load_config(path: Path) -> dict:
    cfg = json.loads(path.read_text(encoding="utf-8"))
    required = (
        "listener_base_url",
        "path_token",
        "bind_host",
        "bind_port",
        "bar_period_s",
        "emit_enabled",
        "poll_interval_s",
    )
    missing = [k for k in required if k not in cfg]
    if missing:
        raise SystemExit(f"config missing keys: {missing}")
    if len(str(cfg["path_token"])) < 32:
        raise SystemExit("path_token must be len >= 32")
    if cfg.get("emit_enabled") is True:
        log.warning(
            "emit_enabled=true in config — requires a separate strategy emit GO; "
            "NullStrategy still emits nothing"
        )
    return cfg


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="c1 Python signal daemon (S2b)")
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    cfg = load_config(args.config)

    client = ListenerClient(
        base_url=str(cfg["listener_base_url"]),
        path_token=str(cfg["path_token"]),
    )
    loop = EvaluateLoop(
        source=IdleBarSource(),
        client=client,
        strategy=NullStrategy(),
        bar_period_s=float(cfg["bar_period_s"]),
        emit_enabled=bool(cfg["emit_enabled"]),
    )

    httpd = serve_health(
        host=str(cfg["bind_host"]),
        port=int(cfg["bind_port"]),
        get_heartbeat=lambda: loop.heartbeat(datetime.now(timezone.utc)),
    )
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    log.info(
        "daemon up bind=%s:%s emit_enabled=%s listener=%s",
        cfg["bind_host"],
        cfg["bind_port"],
        cfg["emit_enabled"],
        # redact token: show only host
        str(cfg["listener_base_url"]).rstrip("/"),
    )

    interval = float(cfg["poll_interval_s"])
    try:
        while True:
            record = loop.step(datetime.now(timezone.utc))
            if record.get("action") not in ("idle",):
                log.info("step %s", record)
            time.sleep(interval)
    except KeyboardInterrupt:
        log.info("shutdown")
        httpd.shutdown()
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
