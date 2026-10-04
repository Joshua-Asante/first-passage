"""Q7 live-page driver: one synthetic book incident paged through Grafana IRM.

Card: docs/briefs/handoffs/2026-10-03-dmon-grafana-irm-binding-card-DRAFT.md (FROZEN 2026-10-04),
§3.5 and §6.3. OUTWARD-FACING: it sends a real page to Joshua's phone. Joshua runs it himself,
attended, with an explicit go for each run (OA-7); no agent runs it or holds the URL.

It writes ``notifier-config.json`` (references only) beside the journal, boots a scratch
``BookAccountOwner`` on synthetic inputs with no broker, commits one ``operator`` halt, publishes
once, waits, republishes once under the same key, prints the incident key and the journal
events (times and kinds only) and exits. Its only owner calls are ``boot`` (with
``synthetic_broker=None``) and ``halt``. It never prints the URL and starts no background
process beyond the notifier's bounded publish thread.

    python ops/c1_rail/book_incident_irm_live_page.py --dir <fresh private dir> --confirm-live-page

Then, in order: acknowledge in IRM after the call rings; run ``book_incident_operator_cli.py
record-delivery --journal <dir>/notifier-journal.sqlite --config <dir>/notifier-config.json
<key>``; wait for ``safe to resolve (rail side)``; only then resolve the alert group.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import functools
import json
from pathlib import Path
import sys
import time
from uuid import uuid4

if not __package__:  # run as a script: put the ops and core layer roots on the path
    _ROOT = Path(__file__).resolve().parents[2]
    for _path in (_ROOT / "ops" / "c1_rail", _ROOT / "ops", _ROOT / "core"):
        if str(_path) not in sys.path:
            sys.path.insert(0, str(_path))

from c1_rail.book_account_owner import BookAccountOwner  # noqa: E402
from c1_rail.book_incident_grafana_irm import GrafanaIRMChannel  # noqa: E402
from c1_rail.book_incident_notifier import (  # noqa: E402
    IncidentNotifier, LocalFileChannel, NotifierConfig, NotifierConfigError)
from c1_rail.book_policy import candidate_book_protection_policy  # noqa: E402
from c1_rail.book_sizing_context import BookSession, SettledClose  # noqa: E402


SECRET_REF = "env:FP_DMON_GRAFANA_IRM_URL"
JOURNAL = "notifier-journal.sqlite"
CONFIG = "notifier-config.json"
OWNER = "qualification-owner.sqlite"
LEGS = ("aegis_6j", "dj30_mym_p250", "vanguard_mgc", "orb_mnq_v7")


def _config(secret_ref):
    return NotifierConfig.from_mapping({
        "channels": [{"name": "irm", "kind": "grafana_irm", "secret_ref": secret_ref},
                     {"name": "local", "kind": "local_file"}],
        "publish_timeout_s": 10.0, "retry_initial_s": 5.0, "retry_max_s": 30.0})


def _binding(now):
    """A synthetic binding for the scratch owner only: no real account, session or figure."""
    session = BookSession("qualification-day:live-page", "qualification-day:prior",
                          now - timedelta(hours=1), now + timedelta(hours=1),
                          now + timedelta(hours=2), "c" * 64,
                          now + timedelta(hours=1, minutes=10), now + timedelta(hours=1, minutes=15))
    settled = SettledClose(session.prior_session_id, session.opens_at - timedelta(minutes=1),
                           1.0, 1.0, "e" * 64)
    return {"session": session, "settlement": settled,
            "policy": candidate_book_protection_policy(), "policy_digest": "d" * 64,
            "snapshot_digest": "a" * 64, "as_of": now - timedelta(seconds=1),
            "valid_until": now + timedelta(minutes=5), "max_evidence_age": timedelta(seconds=30),
            "lifecycle_tiers": {leg_id: "AUTHORIZED" for leg_id in LEGS},
            "cap_allocations": {leg_id: 0 for leg_id in LEGS}, "risk_dollars": {}}


def _print_events(notifier, key):
    for event in notifier.events(key):
        print("  %s %-18s %s" % (event["at"], event["kind"], event["channel"] or "-"), flush=True)


def run(directory, *, secret_ref=SECRET_REF, republish_after_s=90.0):
    directory = Path(directory)
    config = _config(secret_ref)
    irm = GrafanaIRMChannel("irm", secret_ref, publish_timeout_s=config.publish_timeout_s,
                            qualification_test=True)  # resolves the reference; no request yet
    if any((directory / name).exists() for name in (JOURNAL, CONFIG, OWNER)):
        raise NotifierConfigError("directory already holds a run; name a fresh directory")
    directory.mkdir(parents=True, exist_ok=True)
    (directory / CONFIG).write_text(json.dumps(config.resolved(), sort_keys=True, indent=2),
                                    encoding="utf-8")
    clock = functools.partial(datetime.now, timezone.utc)
    now = clock().replace(microsecond=0)
    owner = BookAccountOwner.boot(directory / OWNER, "synthetic-qualification",
                                  binding=_binding(now), synthetic_broker=None)
    owner.halt("qualification-live-page:" + uuid4().hex, "operator", now=now)
    notifier = IncidentNotifier(
        directory / JOURNAL,
        read_incidents=functools.partial(BookAccountOwner.read_incidents, owner.path),
        channels={"irm": irm, "local": LocalFileChannel("local", directory / "local-evidence")},
        config=config, clock=clock)
    notifier.run_once()
    key = notifier.jobs()[0]["incident_key"]
    print("t0 publish: provider status %s" % irm.last_status, flush=True)
    print("waiting %.0f s; do not acknowledge until the call rings" % republish_after_s, flush=True)
    time.sleep(republish_after_s)
    notifier.run_once()
    print("republish: provider status %s" % irm.last_status, flush=True)
    print("incident key (alert_uid): " + key)
    _print_events(notifier, key)
    print("journal: %s\nconfig: %s" % (directory / JOURNAL, directory / CONFIG), flush=True)
    return key


def main(argv=None):
    parser = argparse.ArgumentParser(prog="book_incident_irm_live_page")
    parser.add_argument("--dir", required=True, help="a fresh private directory for this run")
    parser.add_argument("--confirm-live-page", action="store_true",
                        help="required: this sends a real page")
    parser.add_argument("--secret-ref", default=SECRET_REF)
    parser.add_argument("--republish-after-s", type=float, default=90.0)
    args = parser.parse_args(argv)
    if not args.confirm_live_page:
        print("refused: --confirm-live-page is required (this sends a real page)", file=sys.stderr)
        return 2
    try:
        run(args.dir, secret_ref=args.secret_ref, republish_after_s=args.republish_after_s)
    except NotifierConfigError as exc:
        print("refused: " + str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
