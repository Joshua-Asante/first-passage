"""Daemon entrypoint — feed + evaluate loop + health HTTP.

No approved live source: the runtime stays on NullStrategy and an unavailable
bar source regardless of stale ceremony configuration.
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
import threading
import time
import uuid
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
    """Unavailable source until a replacement is explicitly approved and built."""

    feed_mode = "unavailable"

    def __init__(self) -> None:
        self._connected = False

    @property
    def connected(self) -> bool:
        return self._connected

    def poll(self) -> Bar | None:
        return None

    def deactivate(self):
        pass


def load_config(path: Path) -> dict:
    cfg = json.loads(path.read_text(encoding="utf-8"))
    cfg.setdefault("strategy", "null")
    cfg.setdefault("m1_test", {"enabled": False})
    if not isinstance(cfg["m1_test"], dict):
        raise ValueError("m1_test must be an object")
    cfg["m1_test"].setdefault("enabled", False)
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
    if type(cfg["emit_enabled"]) is not bool or type(cfg["m1_test"]["enabled"]) is not bool:
        raise ValueError("emit and ceremony enabled flags must be booleans")
    if cfg["strategy"] not in ("null", "m1_stage1_test"):
        raise ValueError("unknown strategy")
    if cfg["m1_test"]["enabled"] or cfg["emit_enabled"]:
        gate = cfg["m1_test"]
        if (cfg["strategy"] != "m1_stage1_test" or cfg["bar_period_s"] != 60
                or not all(key in gate for key in
                           ("boot_id", "ceremony_id", "generation", "manifest_sha256"))
                or cfg["m1_test"]["enabled"] is not cfg["emit_enabled"]):
            raise ValueError("complete enabled ceremony configuration required")
        if type(gate["generation"]) is not int or gate["generation"] <= 0:
            raise ValueError("ceremony generation must be a positive integer")
    return cfg


def build_loop(config_path, *, boot_id, transport=None):
    """Construct an inert runtime. The caller holds DaemonOwnership for its lifetime."""
    from c1_signal_daemon.m1_stage1_state import CeremonyStore, DEFAULT_STATE_PATH
    cfg = load_config(config_path)
    store = CeremonyStore(cfg["m1_test"].get("state_path", DEFAULT_STATE_PATH))
    store.boot(boot_id)
    return EvaluateLoop(
        source=IdleBarSource(),
        client=ListenerClient(base_url=cfg["listener_base_url"], path_token=cfg["path_token"],
                              transport=transport),
        strategy=NullStrategy(), bar_period_s=60, emit_enabled=False, boot_id=boot_id)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="c1 Python signal daemon (S2b)")
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    cfg = load_config(args.config)

    from c1_signal_daemon.m1_stage1_state import DaemonOwnership, DEFAULT_STATE_PATH
    state_path = Path(cfg["m1_test"].get("state_path", DEFAULT_STATE_PATH))
    ownership = DaemonOwnership(state_path.with_suffix(".owner.lock"))
    with ownership:
        return run_daemon(args.config, cfg)


def run_daemon(config_path, cfg):
    loop = build_loop(config_path, boot_id=uuid.uuid4().hex)

    httpd = serve_health(
        host=str(cfg["bind_host"]),
        port=int(cfg["bind_port"]),
        get_heartbeat=lambda: loop.heartbeat(datetime.now(timezone.utc)),
    )
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    log.info(
        "daemon up bind=%s:%s emit_enabled=false boot_id=%s",
        cfg["bind_host"],
        cfg["bind_port"],
        loop.heartbeat().boot_id,
    )

    interval = float(cfg["poll_interval_s"])
    try:
        while True:
            record = loop.step()
            disabled = (record.get("action") == "suppress"
                        and (record.get("reason") == "ceremony_disabled"
                             or (record.get("reason") == "feed_unhealthy"
                                 and loop._source.feed_mode == "unavailable")))
            if record.get("action") != "idle" and not disabled:
                log.info("step %s", record)
            time.sleep(interval)
    except KeyboardInterrupt:
        log.info("shutdown")
        httpd.shutdown()
        return 0
    finally:
        loop._source.deactivate()
        httpd.shutdown()


if __name__ == "__main__":
    raise SystemExit(main())
