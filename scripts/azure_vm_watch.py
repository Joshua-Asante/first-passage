#!/usr/bin/env python3
"""Local watcher that deallocates the Azure compute VM (fp-compute-01).

Joshua's ruling 2026-10-24: the session that starts the VM confirms "VM
deallocated" before its turn ends; runs of up to 12 h keep this watcher on,
with the PC plugged in, for the whole allocation.

The watcher only reads power state (``az vm get-instance-view``) and calls
``az vm deallocate``; it never starts, resizes or runs commands on the VM.
It deallocates when the deadline passes, when this week's watched VM time
reaches the dollar cap, when the VM is stopped but still allocated (billing),
or when power state stays unreadable. It exits 0 once the VM is verified
deallocated (or never started within the grace period) and 2, writing
``ALARM.txt``, if deallocation cannot be verified.

The weekly ledger counts only time this watcher observed, by UTC week
starting Monday. Run it before or right after starting the VM, e.g.
``.\\fp.ps1 python scripts/azure_vm_watch.py --hours 6``.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

MAX_HOURS = 12.0
DEALLOCATED, DEALLOCATING, STOPPED = "VM deallocated", "VM deallocating", "VM stopped"
_SUB = re.compile(r"/subscriptions/[0-9a-fA-F-]{36}", re.I)
_DEFAULT_AZ = r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd"


def redact(text: str) -> str:
    return _SUB.sub("/subscriptions/<redacted>", text)


class Vm:
    def __init__(self, az: str, group: str, name: str):
        self.base, self.args = [az, "vm"], ["-g", group, "-n", name]

    def _az(self, *cmd: str, timeout: float) -> str:
        p = subprocess.run([*self.base, *cmd, *self.args, "-o", "json"],
                           capture_output=True, text=True, timeout=timeout)
        if p.returncode:
            raise RuntimeError(redact(p.stderr.strip()) or f"az exit {p.returncode}")
        return p.stdout

    def power(self) -> str:
        view = json.loads(self._az("get-instance-view", timeout=120))  # short: every safety check waits on it
        for s in view["instanceView"]["statuses"]:
            if s["code"].startswith("PowerState/"):
                return s["displayStatus"]
        raise RuntimeError("no PowerState status")

    def deallocate(self) -> None:
        self._az("deallocate", timeout=1800)


def week_key(now: float) -> str:
    d = dt.datetime.fromtimestamp(now, dt.timezone.utc).date()
    return (d - dt.timedelta(days=d.weekday())).isoformat()


class Ledger:
    def __init__(self, path: Path):
        self.path = path

    def _read(self) -> dict:
        return json.loads(self.path.read_text()) if self.path.exists() else {}

    def seconds(self, now: float) -> float:
        return self._read().get(week_key(now), 0.0)

    def add(self, now: float, seconds: float) -> None:
        data = self._read()
        data[week_key(now)] = data.get(week_key(now), 0.0) + seconds
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=1))
        tmp.replace(self.path)


def keep_awake() -> None:
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000001)  # CONTINUOUS | SYSTEM_REQUIRED


def log(msg: str) -> None:
    print(f"{dt.datetime.now().isoformat(timespec='seconds')} {msg}", flush=True)


def deallocate_verified(vm, state_dir: Path, reason: str, sleep, attempts: int = 3) -> int:
    for i in range(1, attempts + 1):
        log(f"deallocating ({reason}), attempt {i}")
        try:
            vm.deallocate()
            if vm.power() == DEALLOCATED:
                log("verified: VM deallocated")
                return 0
        except Exception as e:  # keep retrying; the alarm below is the backstop
            log(f"deallocate error: {redact(str(e))}")
        sleep(60)
    msg = f"ALARM: deallocation NOT verified after {attempts} attempts ({reason}); the VM may still be billing"
    print(msg, file=sys.stderr, flush=True)
    try:
        state_dir.mkdir(parents=True, exist_ok=True)
        (state_dir / "ALARM.txt").write_text(f"{dt.datetime.now().isoformat()} {msg}\n")
    except OSError as e:
        print(f"ALARM.txt not written: {e}", file=sys.stderr, flush=True)
    return 2


def watch(vm, ledger: Ledger, state_dir: Path, *, hours: float, poll: float, grace: float,
          rate: float, cap: float, max_unreadable: float, clock=time.time, sleep=time.sleep) -> int:
    start = last = clock()
    deadline, seen_allocated, unreadable_since = start + hours * 3600, False, None

    def stop(reason: str) -> int:
        rc = deallocate_verified(vm, state_dir, reason, sleep)
        try:  # conservatively bill the whole deallocation window, retries included
            ledger.add(clock(), clock() - last)
        except (OSError, ValueError) as e:
            log(f"ledger unavailable; deallocation time not recorded: {e}")
        return rc

    while True:
        keep_awake()
        try:
            state, unreadable_since = vm.power(), None
        except Exception as e:
            log(f"power read failed: {redact(str(e))}")
            unreadable_since = unreadable_since or clock()
            if clock() - unreadable_since >= max_unreadable:
                return stop("power state unreadable")
            state = None
        now = clock()  # after the read, so a slow read cannot defer the checks below
        try:
            if state not in (None, DEALLOCATED) or (state is None and seen_allocated):
                seen_allocated = True
                ledger.add(now, now - last)  # unreadable polls count once the VM was seen allocated
            dollars = ledger.seconds(now) * rate / 3600
        except (OSError, ValueError) as e:  # the cap cannot be enforced without the ledger
            log(f"ledger unavailable: {e}")
            return stop("weekly ledger unavailable")
        last = now
        reason = ("deadline" if now >= deadline else
                  f"weekly cap ${cap:.0f} reached (${dollars:.2f})" if dollars >= cap else
                  "stopped but still allocated" if state == STOPPED else None)
        if reason and state != DEALLOCATED:
            return stop(reason)
        if state == DEALLOCATED and (seen_allocated or now - start >= grace):
            log("VM deallocated; watcher done" if seen_allocated else "VM never started within grace; watcher done")
            return 0
        log(f"state={state} week=${dollars:.2f}/{cap:.0f} deadline_in={(deadline - now) / 3600:.2f}h")
        sleep(poll)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--hours", type=float, required=True, help=f"allocation deadline, at most {MAX_HOURS:g}")
    ap.add_argument("--group", default="fp-compute-01_group")
    ap.add_argument("--vm", default="fp-compute-01")
    ap.add_argument("--poll", type=float, default=60, help="seconds between power-state reads")
    ap.add_argument("--grace-min", type=float, default=15, help="exit if the VM has not started by then")
    ap.add_argument("--rate", type=float, default=2.90, help="USD per running VM-hour")
    ap.add_argument("--weekly-cap", type=float, default=125.0, help="USD per UTC week")
    ap.add_argument("--state-dir", type=Path, default=Path(__file__).resolve().parent.parent / ".cache" / "azure-vm-watch")
    ap.add_argument("--az", default=shutil.which("az") or _DEFAULT_AZ)
    a = ap.parse_args(argv)
    if not 0 < a.hours <= MAX_HOURS:
        ap.error(f"--hours must be in (0, {MAX_HOURS:g}]")
    return watch(Vm(a.az, a.group, a.vm), Ledger(a.state_dir / "ledger.json"), a.state_dir,
                 hours=a.hours, poll=a.poll, grace=a.grace_min * 60, rate=a.rate,
                 cap=a.weekly_cap, max_unreadable=600)


if __name__ == "__main__":
    sys.exit(main())
