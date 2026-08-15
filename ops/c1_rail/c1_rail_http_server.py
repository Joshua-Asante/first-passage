"""c1 rail HTTP-server socket adapter — TV webhook → handle_signal.

Thin process wrapper around ops/c1_rail/c1_rail_listener.handle_signal. TradingView
points its alert webhook at this server; on each authorized POST the body is
parsed as a B1 JSON payload (or ignored as informational noise if it isn't),
current_equity is read, and the already-tested decision-routing layer does
the rest.

UNTESTED BY DESIGN (socket / real-network process paths) — same split as:
  - ops/c1_rail/crosstrade_payload._urllib_sender (real network path)
  - the original NT8/ATI host process vs ops/c1_rail/c1_sizing_host_reference.py
    (algorithm tested; process wiring not)

Pure helpers that encode the §2.5 contract (path-token gate, equity parse /
source dispatch) ARE unit-tested. Do not grow sizing-law logic here.

§2.5(A) inbound auth: sizing POSTs accepted ONLY at POST /c1/<path_token>
(exact path match). Wrong path → 404 before body parse / equity /
handle_signal. GET / stays unauthenticated (health only). TLS terminates at
the reverse proxy; this process stays loopback-bound (bind_host=127.0.0.1).

§2.5(B) equity: equity_source "file" (default until B6 field-name verify) or
"crosstrade" (GET /v1/api/tv/accounts/{account}, Bearer crosstrade_api_token).
Balance field name is config-driven (equity_field) — never a hardcoded guess.
Unreadable/missing → CRITICAL + HTTP 503 + no handle_signal (never invent).
Peak ratchet on a successful read persists into dd_state_path (spec §2.3).

Run:
  python ops/c1_rail/c1_rail_http_server.py --config <host-dir>/c1_rail_config.json
"""
from __future__ import annotations

import argparse
import json
import logging
import math
import secrets
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

# Standalone-run bootstrap (same pattern as ops/cli.py tearsheet / c1_sizing_host_reference).
# parents[2] = repo root (this file lives under ops/c1_rail/).
_REPO_ROOT = Path(__file__).resolve().parents[2]
_RAIL_DIR = Path(__file__).resolve().parent
for _p in (str(_REPO_ROOT / "core"), str(_RAIL_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from c1_rail_listener import arming_expiry_reason, handle_signal  # noqa: E402
from c1_rail_telemetry import (  # noqa: E402
    EventLedger,
    ExecutionStateStore,
    FileAckNotifier,
    LoggingNotifier,
    body_sha256,
    make_request_received,
    new_event_id,
)
from c1_sizing_host_reference import C1SizingHostReference  # noqa: E402
from lib.atomic_io import atomic_write_text  # noqa: E402

log = logging.getLogger("c1_rail_http")

PATH_TOKEN_MIN_LEN = 32
_VALID_EQUITY_SOURCES = frozenset({"file", "crosstrade"})
_RISK_ADD_SIGNALS = frozenset({"entry", "add"})
_FLAT_SIGNALS = frozenset({"exit", "flat"})
_B1_SIGNAL_TYPES = _RISK_ADD_SIGNALS | _FLAT_SIGNALS

_REQUIRED_CONFIG = (
    "bind_host", "bind_port",
    "lifecycle_state_path", "dd_state_path", "constants_path", "equity_path",
    "path_token",
    "account", "secret_key", "webhook_id", "webhook_secret",
)


class EquityReadError(Exception):
    """Unreadable/invalid current_equity — fail closed, never invent."""


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sizing_post_path(path_token: str) -> str:
    """Canonical authorized sizing path (spec §2.5(A))."""
    return f"/c1/{path_token}"


def is_authorized_sizing_path(request_path: str, path_token: str) -> bool:
    """True iff the request path is exactly /c1/<path_token> (query ignored).

    Timing-safe compare. Spec §2.5(A): wrong path must never reach body parse,
    equity read, or handle_signal.
    """
    path = urllib.parse.urlparse(request_path).path
    expected = sizing_post_path(path_token)
    return secrets.compare_digest(path, expected)


def redact_token(text: str, token: str) -> str:
    """Scrub the path_token from any string bound for the logs (spec §2.5(A)).

    The path_token is the inbound-auth secret and logs persist (Fly retains
    them), so it must never appear there — not in the startup line, nor in a
    near-miss request path that embeds it verbatim (e.g. a trailing-slash
    probe `/c1/<token>/`, which fails the exact-match gate and would otherwise
    be logged in full).
    """
    if token and token in text:
        return text.replace(token, "<redacted>")
    return text


def startup_log_line(cfg: dict) -> str:
    """The 'listening' banner with the path_token redacted (never logged).

    Keeps the operational facts (bind, dry_run, equity_source) but replaces the
    token in the route with `<redacted>`. Topology-accurate: TLS terminates at
    the proxy/edge — the earlier 'keep bind_host=127.0.0.1' text was only true
    for the same-box-proxy variant and is dropped (spec §2.5(A), two topologies).
    """
    path = redact_token(sizing_post_path(cfg["path_token"]), cfg["path_token"])
    return (
        f"c1 rail HTTP adapter listening on "
        f"http://{cfg['bind_host']}:{cfg['bind_port']}{path}  "
        f"dry_run={cfg.get('dry_run', True)} "
        f"armed_until={cfg.get('armed_until') or '-'} "
        f"equity_source={cfg.get('equity_source', 'file')} "
        f"(auth: path-token gate; TLS terminates at the proxy/edge)"
    )


def load_config(path: Path) -> dict:
    cfg = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(cfg, dict):
        raise ValueError(f"config {path} is not a JSON object")
    missing = [k for k in _REQUIRED_CONFIG if k not in cfg]
    if missing:
        raise ValueError(f"config missing required keys: {missing}")

    # Safety default mirrors handle_signal: absent dry_run → True.
    cfg.setdefault("dry_run", True)
    # §2.5(B): file stays the explicit default until B6 field-name verify.
    cfg.setdefault("equity_source", "file")

    # M1: armed risk-add requires a writable structured event path.
    if not cfg.get("dry_run", True) and not cfg.get("events_log_path"):
        raise ValueError(
            "dry_run=false requires events_log_path (M1 monitoring gate)")

    # Arming carries an absolute expiry. If it is expired, absent, or malformed
    # at boot, treat that as an IMPLICIT DISARM and boot disarmed — do not
    # refuse to boot.
    #
    # This reverses the original behaviour, which raised here. The reversal is
    # not a relaxation: `arming_expiry_reason` is fail-safe, so every case it
    # flags ALREADY blocks risk-add on the per-request gate. Refusing to boot
    # therefore protected nothing the expiry had not already blocked, while
    # costing the operator the host itself.
    #
    # 2026-07-31 incident: the disarm sequence ran only its second half (restart
    # with no preceding `--disarm`). The volume still said dry_run=false and
    # armed_until had lapsed, so the boot gate raised, the machine crash-looped,
    # and Fly stopped it at max restart count 10. Recovery was NOT a restart —
    # editing /data needs `fly ssh`, `fly ssh` needs a booted machine, so the
    # documented remedy was unreachable and it took an entrypoint override to
    # get back in. A guard whose failure mode removes the operator's ability to
    # flatten a position is worse than the state it guards against.
    #
    # Deliberately IN-MEMORY only: this does not rewrite the volume config.
    # `load_config` is called by tooling and tests, a write side-effect would
    # surprise, and the volume may be read-only. The safe direction is preserved
    # either way (the process runs disarmed); the log line below tells the
    # operator how to make it durable, and the boot line prints dry_run=True.
    if not cfg.get("dry_run", True):
        boot_expiry = arming_expiry_reason(cfg)
        if boot_expiry is not None:
            log.warning(
                "IMPLICIT DISARM at boot — %s. The config on disk still says "
                "dry_run=false; this process is running DISARMED. Make it "
                "durable with: python ops/c1_rail/c1_rail_arm.py --disarm",
                boot_expiry)
            cfg["dry_run"] = True
            cfg["armed_until"] = None

    token = cfg["path_token"]
    if not isinstance(token, str) or len(token) < PATH_TOKEN_MIN_LEN:
        raise ValueError(
            f"path_token must be a string of length >= {PATH_TOKEN_MIN_LEN} "
            f"(got {type(token).__name__} len={len(token) if isinstance(token, str) else 'n/a'})"
        )
    if token.startswith("REPLACE"):
        raise ValueError(
            "path_token still looks like a REPLACE placeholder — set a real "
            f">={PATH_TOKEN_MIN_LEN}-char random token before starting")

    source = cfg["equity_source"]
    if source not in _VALID_EQUITY_SOURCES:
        raise ValueError(
            f"equity_source must be one of {sorted(_VALID_EQUITY_SOURCES)}; "
            f"got {source!r}")
    if source == "crosstrade":
        for key in ("crosstrade_api_token", "equity_field"):
            val = cfg.get(key)
            if not isinstance(val, str) or not val or val.startswith("REPLACE"):
                raise ValueError(
                    f"equity_source=crosstrade requires a real {key} "
                    f"(not missing/empty/REPLACE placeholder)")

    return cfg


def read_current_equity(equity_path: Path) -> float:
    """File-based equity source (spec §2.5(B) test/fallback hook)."""
    if not equity_path.exists():
        raise EquityReadError(f"equity file missing: {equity_path.name}")
    try:
        obj = json.loads(equity_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise EquityReadError(
            f"equity file unreadable ({equity_path.name}): {exc}") from exc
    if not isinstance(obj, dict):
        raise EquityReadError(
            f"equity file malformed ({equity_path.name}): not a JSON object")
    equity = obj.get("current_equity")
    if not isinstance(equity, (int, float)) or not math.isfinite(equity) or equity <= 0:
        raise EquityReadError(
            f"equity file has invalid current_equity: {equity!r}")
    return float(equity)


def parse_crosstrade_account_equity(payload: dict, equity_field: str) -> float:
    """Extract equity from a CrossTrade get-account JSON body (spec §2.5(B)).

    Field name is caller-supplied — never guessed (B6 verifies the live key).
    """
    if not isinstance(payload, dict):
        raise EquityReadError("crosstrade equity response is not a JSON object")
    if payload.get("success") is not True:
        raise EquityReadError(
            f"crosstrade equity response success!=true: {payload.get('success')!r}")
    data = payload.get("data")
    if not isinstance(data, dict):
        raise EquityReadError("crosstrade equity response missing data object")
    # equity_field may be a dotted path — the live CrossTrade Tradovate response
    # nests net-liq under data.balance.netLiq (B6 verify 2026-07-19). A field with
    # no dot stays a flat key (backward compatible with the pre-2026-07-19 shape).
    node = data
    parts = equity_field.split(".")
    for i, part in enumerate(parts):
        if not isinstance(node, dict) or part not in node:
            avail = sorted(node) if isinstance(node, dict) else f"<{type(node).__name__}>"
            raise EquityReadError(
                f"crosstrade equity field {equity_field!r} missing from data "
                f"(resolved={parts[:i]!r}, available={avail}); "
                f"verify live response before arming")
        node = node[part]
    equity = node
    if not isinstance(equity, (int, float)) or not math.isfinite(equity) or equity <= 0:
        raise EquityReadError(
            f"crosstrade equity field {equity_field!r} invalid: {equity!r}")
    return float(equity)


def _urllib_get_json(url: str, headers: dict) -> tuple[int, dict]:
    """The one real-network GET in this module — not covered by unit tests."""
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=10) as resp:
        raw = resp.read().decode("utf-8")
        try:
            body = json.loads(raw) if raw.strip() else {}
        except ValueError as exc:
            raise EquityReadError(
                f"crosstrade equity GET returned non-JSON: {exc}") from exc
        return int(resp.status), body if isinstance(body, dict) else {}


def fetch_crosstrade_equity(
    *, account: str, api_token: str, equity_field: str, getter=None,
) -> float:
    """GET CrossTrade Tradovate account snapshot → equity (spec §2.5(B)).

    `getter(url, headers) -> (status, body_dict)` is dependency-injected;
    tests supply a fake. Default is a real urllib GET (untested by design).
    """
    if getter is None:
        getter = _urllib_get_json
    url = f"https://app.crosstrade.io/v1/api/tv/accounts/{urllib.parse.quote(account, safe='')}"
    headers = {"Authorization": f"Bearer {api_token}",
               "Accept": "application/json"}
    try:
        status, body = getter(url, headers)
    except EquityReadError:
        raise
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise EquityReadError(f"crosstrade equity GET failed: {exc}") from exc
    except Exception as exc:  # noqa: BLE001 — fail closed on any transport surprise
        raise EquityReadError(f"crosstrade equity GET failed: {exc}") from exc
    if status != 200:
        raise EquityReadError(f"crosstrade equity GET HTTP {status}")
    return parse_crosstrade_account_equity(body, equity_field)


def resolve_current_equity(cfg: dict, *, getter=None) -> float:
    """Dispatch equity_source (spec §2.5(B)). Fail closed — never invent."""
    source = cfg.get("equity_source", "file")
    if source == "file":
        return read_current_equity(Path(cfg["equity_path"]))
    if source == "crosstrade":
        return fetch_crosstrade_equity(
            account=cfg["account"],
            api_token=cfg["crosstrade_api_token"],
            equity_field=cfg["equity_field"],
            getter=getter,
        )
    raise EquityReadError(f"unknown equity_source {source!r}")


def ratchet_peak_equity(dd_state_path: Path, current_equity: float) -> float:
    """Persist peak = max(peak, current) per spec §2.3. Returns effective peak.

    Atomic write (temp + replace), matching dd_protection's discipline. If the
    dd state file is missing/malformed the sizing host will halt on its own
    read — we still refuse to invent a peak here.
    """
    try:
        state = json.loads(dd_state_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise EquityReadError(
            f"dd state unreadable for peak ratchet ({dd_state_path.name}): "
            f"{exc}") from exc
    if not isinstance(state, dict):
        raise EquityReadError(
            f"dd state malformed ({dd_state_path.name}): not a JSON object")
    peak = state.get("peak_equity")
    if not isinstance(peak, (int, float)) or not math.isfinite(peak) or peak <= 0:
        raise EquityReadError(
            f"dd state has invalid peak_equity: {peak!r}")
    effective = max(float(peak), float(current_equity))
    if effective > float(peak):
        state["peak_equity"] = effective
        state["last_updated_utc"] = _utc_now_iso()
        atomic_write_text(dd_state_path, json.dumps(state, indent=2) + "\n")
        log.info("peak_equity ratcheted %.2f -> %.2f", peak, effective)
    return effective


def _rail_config_from(cfg: dict) -> dict:
    """Subset of the process config that handle_signal's `config=` expects."""
    out = {
        "account": cfg["account"],
        "secret_key": cfg["secret_key"],
        "webhook_id": cfg["webhook_id"],
        "webhook_secret": cfg["webhook_secret"],
        "dry_run": cfg.get("dry_run", True),
        # Absolute arming deadline; handle_signal fail-safes to EXPIRED when
        # absent/invalid, so forwarding it verbatim (including None) is correct.
        "armed_until": cfg.get("armed_until"),
    }
    if "destination" in cfg:
        out["destination"] = cfg["destination"]
    return out


def _audit(action, *, raw_body: str) -> None:
    d = action.decision
    log.info(
        "audit halt=%s submit=%s sent=%s dry_run=%s transport=%s "
        "event_id=%s order_id=%s leg=%s signal=%s qty=%s http_status=%s "
        "halt_reason=%s body_preview=%r",
        d.halt, d.submit, action.sent, action.dry_run, action.transport_state,
        action.event_id, action.order_id, d.leg_id, d.signal_type,
        d.qty_out, action.http_status, d.halt_reason, raw_body[:200],
    )


def _classify_signal_type(payload: dict) -> str | None:
    """Return B1 signal_type when present and valid; else None."""
    st = payload.get("signal_type")
    if isinstance(st, str) and st in _B1_SIGNAL_TYPES:
        return st
    return None


def _b1_order_id(payload: dict, signal_type: str) -> str | None:
    try:
        return f"{payload['leg_id']}-{signal_type}-{payload['bar_time']}"
    except (KeyError, TypeError):
        return None


def build_parsed_fields(payload: dict, signal_type: str) -> dict:
    """As-received B1 fields for request_received.parsed (verbatim .get)."""
    return {
        "leg_id": payload.get("leg_id"),
        "signal_type": signal_type,
        "bar_time": payload.get("bar_time"),
        "close": payload.get("close"),
        "stop_dist_pts": payload.get("stop_dist_pts"),
    }


def make_handler(
    host: C1SizingHostReference,
    cfg: dict,
    *,
    equity_getter=None,
    ledger: EventLedger | None = None,
    exec_state: ExecutionStateStore | None = None,
    notifier=None,
):
    """Build a BaseHTTPRequestHandler class closed over host + config.

    `equity_getter` is forwarded to resolve_current_equity for tests; production
    leaves it None (real urllib GET when equity_source=crosstrade).

    M1: classify signal_type before equity. exit/flat bypass equity/DD/lifecycle
    prerequisites and relay best-effort. entry/add require healthy ledger when
    configured and never invent equity.
    """
    notifier = notifier or LoggingNotifier()

    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, fmt: str, *args) -> None:
            # Route stdlib access log through our logger (not stderr print).
            log.debug("http: " + fmt, *args)

        def do_GET(self) -> None:
            # Health probe for deploy checks — never triggers sizing (§2.5(A)).
            body = b'{"ok":true,"service":"c1_rail_http_server"}\n'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self) -> None:
            length = int(self.headers.get("Content-Length", "0") or 0)
            event_id = new_event_id()
            # §2.5(A): reject BEFORE body parse / equity / handle_signal.
            if not is_authorized_sizing_path(self.path, cfg["path_token"]):
                if length > 0:
                    self.rfile.read(length)  # drain; do not parse
                log.warning("unauthorized path rejected (no sizing): %r",
                            redact_token(self.path, cfg["path_token"]))
                if ledger is not None:
                    try:
                        ledger.append(
                            "request_received",
                            make_request_received(
                                event_id=event_id, auth_ok=False,
                                body_category="unauthorized",
                                body_hash="",
                            ),
                            event_id=event_id,
                        )
                    except Exception:  # noqa: BLE001 — never fail open on auth
                        pass
                self._respond(404, "not found")
                return
            raw = (self.rfile.read(length).decode("utf-8", errors="replace")
                   if length > 0 else "")
            self._handle_post(raw, event_id=event_id)

        def _respond(self, status: int, message: str) -> None:
            body = (message + "\n").encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _emit_request(self, *, event_id: str, body_category: str,
                          raw: str, auth_ok: bool = True,
                          order_id: str | None = None,
                          parsed: dict | None = None) -> None:
            if ledger is None:
                return
            try:
                ledger.append(
                    "request_received",
                    make_request_received(
                        event_id=event_id, auth_ok=auth_ok,
                        body_category=body_category,
                        body_hash=body_sha256(raw) if raw else "",
                        order_id=order_id,
                        parsed_fields=parsed,
                    ),
                    event_id=event_id, order_id=order_id,
                )
            except Exception as exc:  # noqa: BLE001
                notifier.notify(
                    "CRITICAL",
                    f"request_received telemetry write failed: {exc}",
                    event_id=event_id,
                )

        def _handle_post(self, raw: str, *, event_id: str) -> None:
            # Informational TV alerts (entry/DD/trail/…) are plain text — noise
            # in the log, not a hazard. Acknowledge so TV doesn't retry.
            try:
                payload = json.loads(raw) if raw.strip() else None
            except ValueError:
                log.info("non-JSON alert body ignored (informational): %r",
                         raw[:200])
                self._emit_request(event_id=event_id,
                                   body_category="non_json", raw=raw)
                self._respond(200, "ignored: non-JSON")
                return
            if not isinstance(payload, dict):
                log.info("non-object JSON ignored: %r", raw[:200])
                self._emit_request(event_id=event_id,
                                   body_category="non_object_json", raw=raw)
                self._respond(200, "ignored: non-object JSON")
                return

            # Classify signal_type BEFORE equity/state (M1 §2.6).
            signal_type = _classify_signal_type(payload)
            order_id = (_b1_order_id(payload, signal_type)
                        if signal_type else None)
            parsed = None
            if signal_type is not None:
                parsed = build_parsed_fields(payload, signal_type)
            self._emit_request(
                event_id=event_id,
                body_category=("b1_json" if signal_type else "json_other"),
                raw=raw, order_id=order_id, parsed=parsed,
            )

            is_flat = signal_type in _FLAT_SIGNALS
            dd_state_path = Path(cfg["dd_state_path"])
            current_equity: float | None = None
            try:
                current_equity = resolve_current_equity(
                    cfg, getter=equity_getter)
                ratchet_peak_equity(dd_state_path, current_equity)
            except EquityReadError as exc:
                if is_flat:
                    # Fail open toward flatten — never block exit on equity.
                    log.critical(
                        "CRITICAL equity/peak read failed on exit/flat — "
                        "relaying flatten best-effort: %s", exc)
                    notifier.notify(
                        "CRITICAL",
                        f"equity failure on exit/flat; relaying: {exc}",
                        event_id=event_id, details={"order_id": order_id},
                    )
                    current_equity = 0.0  # unused by exit/flat sizing path
                else:
                    log.critical(
                        "CRITICAL equity/peak read failed - no order: %s", exc)
                    self._respond(503, f"halt: {exc}")
                    return

            if exec_state is not None:
                exec_state.load_into(host.open_leg_state)

            try:
                action = handle_signal(
                    payload, host, current_equity=float(current_equity or 0.0),
                    config=_rail_config_from(cfg),
                    ledger=ledger, notifier=notifier, event_id=event_id,
                )
            except Exception:
                log.exception("handle_signal raised - no order placed by adapter")
                self._respond(500, "error: handle_signal raised")
                return

            _audit(action, raw_body=raw)
            if action.transport_state == "unknown":
                # Acknowledge TV to suppress upstream retry; block risk-add.
                self._respond(200, "transport_unknown: reconcile before retry")
            elif action.decision.halt:
                self._respond(200, f"halted: {action.decision.halt_reason}")
            elif action.sent:
                self._respond(
                    200,
                    f"sent transport_accepted status={action.http_status} "
                    f"(not execution_verified)",
                )
            elif action.dry_run:
                self._respond(200, "dry_run: computed, not sent")
            else:
                self._respond(200, "not sent (floored or no-submit)")

    return Handler


def serve(cfg: dict) -> None:
    host = C1SizingHostReference(
        lifecycle_state_path=Path(cfg["lifecycle_state_path"]),
        dd_state_path=Path(cfg["dd_state_path"]),
        constants_path=Path(cfg["constants_path"]),
    )
    ledger = None
    exec_state = None
    notifier: LoggingNotifier | FileAckNotifier = LoggingNotifier()
    events_path = cfg.get("events_log_path")
    if events_path:
        ledger = EventLedger(Path(events_path))
        if ledger.risk_add_blocked:
            log.critical(
                "events ledger unhealthy/blocked at startup — risk-add "
                "halted until operator repair: %s", ledger.block_reason)
    exec_path = cfg.get("execution_state_path")
    if exec_path:
        exec_state = ExecutionStateStore(Path(exec_path))
        exec_state.load_into(host.open_leg_state)
    alert_path = cfg.get("alert_log_path")
    ack_dir = cfg.get("alert_ack_dir")
    if alert_path and ack_dir:
        notifier = FileAckNotifier(Path(alert_path), Path(ack_dir))
    handler = make_handler(
        host, cfg, ledger=ledger, exec_state=exec_state, notifier=notifier)
    bind_host = str(cfg["bind_host"])
    bind_port = int(cfg["bind_port"])
    server = ThreadingHTTPServer((bind_host, bind_port), handler)
    log.info("%s", startup_log_line(cfg))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log.info("shutting down")
    finally:
        server.server_close()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="c1 rail HTTP adapter - TV webhook -> CrossTrade (Option C)",
    )
    ap.add_argument("--config", required=True, type=Path,
                    help="path to c1_rail_config.json")
    args = ap.parse_args(argv)

    cfg = load_config(args.config)

    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stdout)]
    audit_path = cfg.get("audit_log_path")
    if audit_path:
        handlers.append(logging.FileHandler(audit_path, encoding="utf-8"))
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=handlers,
        force=True,
    )

    if cfg.get("dry_run", True):
        log.warning("DRY_RUN=true - will compute and audit, never call CrossTrade")
    else:
        log.warning("DRY_RUN=false - LIVE sends enabled; B6 must have passed")
    if cfg.get("equity_source", "file") == "file":
        log.warning(
            "equity_source=file (interim default) - flip to crosstrade only "
            "after B6 verifies equity_field against a live GET response")

    serve(cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
