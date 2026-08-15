#!/usr/bin/env python3
"""Arm / disarm the c1 rail config — one validated, atomic edit.

Replaces the hand-typed `python3 -c "import json..."` heredoc the RUNBOOK used
to carry. That snippet was correct but unversioned and unvalidated, and it was
retyped at the desk under time pressure every session — the 2026-07-27 incident
happened in exactly that gap (an edit that was never made, followed by a
restart that silently re-applied the old armed state).

What this does NOT do: restart the host. It cannot — the running process holds
its config in a boot-time closure, so the edit takes effect only on restart.
That separation is deliberate and safe in this direction: a written-but-not-
restarted arm leaves the rail DISARMED (the safe state), and a restart without
a valid future `armed_until` is refused by the boot gate in
c1_rail_http_server.load_config. Neither half can silently arm the rail alone.

Usage (in-container, `fly ssh console -a c1-rail`):
    python ops/c1_rail/c1_rail_arm.py --status
    python ops/c1_rail/c1_rail_arm.py --arm --hours 4
    python ops/c1_rail/c1_rail_arm.py --disarm

Prints only operational fields. Never prints secrets, and never logs the
config body.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping

# Standalone-run bootstrap (same pattern as ops/c1_rail/c1_rail_http_server.py).
# parents[2] = repo root (this file lives under ops/c1_rail/).
_REPO_ROOT = Path(__file__).resolve().parents[2]
_RAIL_DIR = Path(__file__).resolve().parent
for _p in (str(_REPO_ROOT / "core"), str(_RAIL_DIR), str(_REPO_ROOT / "scripts")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from c1_rail_listener import arming_expiry_reason  # noqa: E402
from lib.atomic_io import atomic_write_text  # noqa: E402
from validate_c1_monitoring_acceptance import validate as validate_m1_acceptance  # noqa: E402

DEFAULT_CONFIG_PATH = "/data/c1_rail_config.json"

# The M1 acceptance artifact. Ships in the Fly image (deploy/c1_rail/Dockerfile
# COPYs it, .dockerignore re-includes it), so `_REPO_ROOT` resolves it both in
# the repo and in-container at /app.
#
# Baking a STATUS into the image is deliberate, not an oversight: the deployed
# host should gate on the acceptance record that was deployed WITH it. If M1
# flips to RESOLVED in the repo, arming requires a redeploy — which is already
# required to refresh `fixture_hashes` anyway, so it is the same motion, not an
# extra one. The alternative (reading a mutable file on the volume) would let
# the gate be satisfied by editing the thing being gated on.
DEFAULT_ACCEPTANCE_PATH = _REPO_ROOT / "docs" / "notes" / "rail_build" / \
    "M1_MONITORING_ACCEPTANCE.json"

M1_RESOLVED = "RESOLVED"

# Keys safe to echo. Anything not listed here is treated as potentially
# sensitive and never printed — an allow-list, so a newly-added secret key
# cannot leak by default.
_PRINTABLE = ("dry_run", "armed_until", "equity_source", "equity_field",
              "destination", "account", "bind_host", "bind_port")

# A window longer than this defeats the point of having one. Warned, not
# refused — the operator may have a legitimate reason, and this tool should
# not invent policy the RUNBOOK doesn't state.
_LONG_WINDOW_HOURS = 8.0


class ArmError(Exception):
    """Refused: the requested change would produce an unsafe config."""


def m1_acceptance_reason(path: Path | None = None) -> str | None:
    """Return a refusal reason if M1 is not a *validated* `RESOLVED`, else None.

    FAIL-SAFE on every path, mirroring `arming_expiry_reason`: missing,
    unreadable, malformed, structurally incomplete, or any status other than
    a validator-passing `RESOLVED` all refuse. An absent or forged artifact
    must never read as permission — that is the one direction this gate exists
    to prevent.

    Invokes `scripts/validate_c1_monitoring_acceptance.validate` with
    `require_resolved=True`. A status-only file like `{"status":"RESOLVED"}`
    fails that validator (~19 errors) and must fail here too (programme audit
    2026-08-08 §5 item 4). Do not re-implement the schema checks in this
    module — the validator is the single schema owner.
    """
    path = Path(path) if path is not None else DEFAULT_ACCEPTANCE_PATH
    errors = validate_m1_acceptance(path, require_resolved=True)
    if not errors:
        return None
    head = errors[0]
    more = f" (+{len(errors) - 1} more)" if len(errors) > 1 else ""
    return (
        f"M1 monitoring gate: acceptance artifact failed validation "
        f"({len(errors)} error(s)): {head}{more} "
        f"(ADR 2026-07-22 §4, trigger amended 2026-07-31b — dry_run=false may "
        f"not be set while M1 is unresolved; "
        f"scripts/validate_c1_monitoring_acceptance.py --require-resolved)"
    )


def m1_acceptance_structurally_valid(path: Path | None = None) -> bool:
    """True iff the artifact clears validate() without --require-resolved.

    Used to decide whether `--acknowledge-m1-unresolved` may apply: the escape
    hatch is for a *valid but unresolved* record (e.g. CODE_LANDED), never for
    a forged or truncated file that happens to contain `"status":"RESOLVED"`.
    """
    path = Path(path) if path is not None else DEFAULT_ACCEPTANCE_PATH
    return not validate_m1_acceptance(path, require_resolved=False)


def plan_arm(cfg: Mapping[str, Any], *, hours: float,
             now: datetime | None = None,
             acceptance_path: Path | None = None,
             acknowledge_unresolved: str | None = None) -> dict:
    """Return a new config armed until now+hours. Pure; does not touch disk.

    `now` is injectable so tests are deterministic rather than racing a clock.
    It is threaded into the self-check below as well: judging a config against
    a clock other than the one that built it is not a stricter test, just a
    different question, and it made a pinned-instant test fail once real time
    passed the pinned deadline (2026-07-28).
    """
    if hours <= 0:
        raise ArmError(f"--hours must be positive (got {hours})")
    # Mirrors the boot gate: arming without a structured event path is refused
    # there too, and finding out at boot is strictly worse than finding out here.
    if not cfg.get("events_log_path"):
        raise ArmError(
            "refusing to arm: events_log_path missing (M1 monitoring gate). "
            "The rail cannot record a structured decision, and the deviation "
            "record below would have nowhere to go.")
    # M1 acceptance interlock (ADR Addendum 2026-07-31b, operator-ratified).
    # Soft by design for a *structurally valid* but unresolved artifact: the
    # operator KEEPS the ability to arm against CODE_LANDED / PENDING — that
    # discretion was exercised knowingly on 07-28 and 07-31 and is not being
    # taken away. What changes is that exercising it now writes its own record.
    # Acknowledgement NEVER clears an invalid/forged artifact (audit 2026-08-08
    # §5.4): a hand-written `{"status":"RESOLVED"}` must fail closed.
    m1_reason = m1_acceptance_reason(acceptance_path)
    if m1_reason is not None:
        if not acknowledge_unresolved:
            raise ArmError(
                f"refusing to arm: {m1_reason}. If this is a deliberate, attended "
                f"deviation against a *valid* unresolved artifact, re-run with "
                f"--acknowledge-m1-unresolved '<reason>'; that arms the rail AND "
                f"writes an `arming_deviation` record to the events ledger.")
        if not m1_acceptance_structurally_valid(acceptance_path):
            raise ArmError(
                f"refusing to arm: {m1_reason}. Acknowledgement cannot clear an "
                f"invalid or forged acceptance artifact — only a structurally "
                f"valid unresolved record (e.g. CODE_LANDED) may be overridden.")
    now = now or datetime.now(timezone.utc)
    deadline = (now + timedelta(hours=hours)).replace(microsecond=0)
    out = dict(cfg)
    out["dry_run"] = False
    out["armed_until"] = deadline.isoformat()
    # Self-check with the SAME predicate the rail enforces per request, so this
    # tool cannot drift from the gate it is meant to satisfy. Evaluated at the
    # same instant that produced the deadline. Still a live guard, not a
    # tautology: `.replace(microsecond=0)` truncates BACKWARD, so a sub-second
    # window yields a deadline at or before `now` and is refused here.
    reason = arming_expiry_reason(out, now=now)
    if reason is not None:
        raise ArmError(f"refusing to arm: produced config is invalid — {reason}")
    return out


def plan_disarm(cfg: Mapping[str, Any]) -> dict:
    """Return a new disarmed config. Clears the deadline as well as the flag.

    Clearing `armed_until` matters: leaving a stale future deadline behind
    would let a later bare `dry_run=false` edit inherit a window the operator
    never consciously granted.
    """
    out = dict(cfg)
    out["dry_run"] = True
    out["armed_until"] = None
    return out


def describe(cfg: Mapping[str, Any]) -> str:
    """One-line operational summary. Secret-free by allow-list."""
    parts = []
    for key in _PRINTABLE:
        if key in cfg:
            parts.append(f"{key}={cfg[key]!r}")
    armed = not cfg.get("dry_run", True)
    if armed:
        reason = arming_expiry_reason(cfg)
        parts.append(f"window={'EXPIRED/INVALID — ' + reason if reason else 'open'}")
    return " ".join(parts)


def describe_m1_gate(path: Path | None = None) -> str:
    """One-line M1 acceptance gate summary for `--status`.

    Surfaces the artifact's `status` and whether `--arm` would clear the
    interlock (PASS) or need `--acknowledge-m1-unresolved` (FAIL). Uses the
    same validator-backed predicate as `plan_arm` — an unreadable, forged, or
    incomplete artifact is FAIL, never a silent pass. Does not dump the
    refusal prose; operators who need that get it from a refused `--arm`.
    """
    path = Path(path) if path is not None else DEFAULT_ACCEPTANCE_PATH
    status: Any = None
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(doc, dict):
            status = doc.get("status")
    except (OSError, ValueError):
        status = None
    result = "PASS" if m1_acceptance_reason(path) is None else "FAIL"
    return f"m1_gate: status={status!r} result={result}"


def _load(path: Path) -> dict:
    cfg = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(cfg, dict):
        raise ArmError(f"config {path} is not a JSON object")
    return cfg


def _record_deviation(cfg: Mapping[str, Any], *, reason: str, gate_reason: str,
                      hours: float) -> dict:
    """Append an `arming_deviation` event. Raises on any failure — see caller.

    Imported lazily so `--status` / `--disarm` stay usable on a host whose
    ledger is unhealthy: a broken telemetry module must never block the SAFE
    direction. Only the arm-with-acknowledgement path needs this.
    """
    from c1_rail_telemetry import EventLedger, new_event_id  # noqa: PLC0415

    ledger = EventLedger(Path(cfg["events_log_path"]))
    return ledger.append(
        "arming_deviation",
        {
            "gate": "M1",
            "gate_reason": gate_reason,
            "operator_reason": reason,
            "requested_hours": hours,
            "adr": "2026-07-22-c1-venue-native-monitoring-maturity.md",
            "addendum": "2026-07-31b",
        },
        event_id=new_event_id(),
    )


def _write(path: Path, cfg: Mapping[str, Any]) -> Path:
    """Atomic write, keeping a one-deep backup for rollback."""
    backup = path.with_suffix(path.suffix + ".prev")
    if path.exists():
        backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    atomic_write_text(path, json.dumps(cfg, indent=2) + "\n")
    return backup


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", type=Path, default=Path(DEFAULT_CONFIG_PATH))
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--arm", action="store_true")
    mode.add_argument("--disarm", action="store_true")
    mode.add_argument("--status", action="store_true")
    ap.add_argument("--hours", type=float, default=4.0,
                    help="armed window length (default 4.0)")
    ap.add_argument("--acceptance", type=Path, default=None,
                    help=argparse.SUPPRESS)  # test seam; default is the shipped artifact
    ap.add_argument("--acknowledge-m1-unresolved", metavar="REASON", default=None,
                    help="arm despite an unresolved M1 gate. Requires a written "
                         "reason, which is recorded as an `arming_deviation` "
                         "event in the ledger. Attended deviations only.")
    args = ap.parse_args(argv)

    try:
        cfg = _load(args.config)
    except (OSError, ValueError, ArmError) as exc:
        print(f"ERROR: cannot read config: {exc}", file=sys.stderr)
        return 1

    if args.status:
        print(f"current: {describe(cfg)}")
        print(describe_m1_gate(args.acceptance))
        return 0

    try:
        new_cfg = (plan_arm(cfg, hours=args.hours,
                            acceptance_path=args.acceptance,
                            acknowledge_unresolved=args.acknowledge_m1_unresolved)
                   if args.arm else plan_disarm(cfg))
    except ArmError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    # Write the deviation record BEFORE the config edit. If the ledger refuses
    # (unhealthy, truncated tail, unwritable), the arm does not happen at all —
    # the escape hatch is only available when the deviation can actually be
    # recorded. Ordering matters: a config written first would leave an armed
    # rail with no record if this then failed.
    if args.arm and args.acknowledge_m1_unresolved:
        m1_reason = m1_acceptance_reason(args.acceptance)
        try:
            _record_deviation(cfg, reason=args.acknowledge_m1_unresolved,
                              gate_reason=m1_reason or "(gate reported resolved)",
                              hours=args.hours)
        except Exception as exc:  # noqa: BLE001 — any failure must refuse the arm
            print(f"ERROR: refusing to arm — could not record the deviation "
                  f"({exc.__class__.__name__}: {exc}). The acknowledgement path "
                  f"requires a writable, healthy event ledger.", file=sys.stderr)
            return 1

    backup = _write(args.config, new_cfg)

    print(f"before : {describe(cfg)}")
    print(f"after  : {describe(new_cfg)}")
    print(f"backup : {backup}")
    if args.arm and args.hours > _LONG_WINDOW_HOURS:
        print(f"WARNING: {args.hours}h window is long — it should not outlast "
              f"the attended session or the 16:45 ET flat deadline.")
    print()
    print("*** NOT YET IN EFFECT — the running process still holds its old "
          "config. Restart to apply:  fly apps restart c1-rail")
    print("*** Then CONFIRM by reading the boot line (dry_run= / armed_until=).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
