"""HB-L1/HB-L2 live-check driver for the missed-heartbeat monitor.

Card: docs/briefs/handoffs/2026-10-03-dmon-missed-heartbeat-monitor-card-DRAFT.md (FROZEN
2026-10-05), §3.8 and §6.3. OUTWARD-FACING: once the pings stop, Grafana IRM pages Joshua's
phone. Joshua runs it himself, attended, with an explicit go for each run (OA-H5); no agent
runs it or holds the URL.

It builds one pinger from the side's ``env:`` reference, marks progress every
``--mark-interval-s`` for ``--ping-seconds``, then stops pinging and stays alive for
``--silent-seconds``. It prints UTC times of the last ping and of each send outcome, never
the URL. It builds no owner or notifier and touches no account, arm or broker surface.

    python ops/c1_signal_daemon/book_heartbeat_live_check.py --side runtime \
        --ping-seconds 180 --silent-seconds 300 --period-s <P> --timeout-s <timeout> \
        --confirm-live-check

For HB-L2, run one process per side and stop only ``--side notifier``.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import sys
import time

if not __package__:  # run as a script: put the ops layer root on the path
    _OPS = Path(__file__).resolve().parents[1]
    if str(_OPS) not in sys.path:
        sys.path.insert(0, str(_OPS))

from c1_signal_daemon.book_heartbeat import (  # noqa: E402
    NOTIFIER_SECRET_REF, RUNTIME_SECRET_REF, HeartbeatConfigError, HeartbeatPinger)


REFERENCES = {"runtime": RUNTIME_SECRET_REF, "notifier": NOTIFIER_SECRET_REF}


def _utc():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _parser():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--side", choices=sorted(REFERENCES), required=True)
    parser.add_argument("--ping-seconds", type=float, required=True)
    parser.add_argument("--silent-seconds", type=float, required=True)
    parser.add_argument("--period-s", type=float, required=True)
    parser.add_argument("--timeout-s", type=float, required=True)
    parser.add_argument("--mark-interval-s", type=float, default=5.0)
    parser.add_argument("--confirm-live-check", action="store_true")
    return parser


def main(argv=None, *, environ=None, out=None, sleep=time.sleep, clock=time.monotonic):
    out = out or sys.stdout
    args = _parser().parse_args(argv)
    if not args.confirm_live_check:
        print("refused: --confirm-live-check is required (an attended, per-run go)", file=out)
        return 2
    if min(args.ping_seconds, args.mark_interval_s) <= 0 or args.silent_seconds < 0:
        print("refused: durations must be positive", file=out)
        return 2
    try:
        pinger = HeartbeatPinger(REFERENCES[args.side], period_s=args.period_s,
                                 timeout_s=args.timeout_s, clock=clock, environ=environ)
    except HeartbeatConfigError as exc:
        print("refused: " + str(exc), file=out)
        return 2
    print("%s side=%s pinging for %ss" % (_utc(), args.side, args.ping_seconds), file=out)
    reported, start, last_ping = 0, clock(), None
    while clock() - start < args.ping_seconds:
        pinger.mark_progress()
        last_ping = _utc()
        sleep(args.mark_interval_s)
        reported = _report(pinger, reported, out)
    pinger.drain(args.timeout_s + 1)
    reported = _report(pinger, reported, out)
    print("%s pings stopped; last ping mark at %s; silent for %ss" % (
        _utc(), last_ping, args.silent_seconds), file=out)
    sleep(args.silent_seconds)
    stats = pinger.stats()
    print("%s done: sends_ok=%d sends_failed=%d" % (
        _utc(), stats["sends_ok"], stats["sends_failed"]), file=out)
    return 0


def _report(pinger, reported, out):
    stats = pinger.stats()
    finished = stats["sends_ok"] + stats["sends_failed"]
    if finished > reported:
        print("%s send outcome: %s" % (_utc(), stats["last_outcome"]), file=out)
    return finished


if __name__ == "__main__":
    sys.exit(main())
