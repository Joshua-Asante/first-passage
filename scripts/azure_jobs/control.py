"""Persistent VM-time accounting and a deliberately small Azure CLI boundary."""
from __future__ import annotations
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import json
import math
import os
from pathlib import Path
import subprocess
import time
import uuid

RATE = 2.90
WEEKLY_DOLLARS = 125.0
WEEKLY_SECONDS = WEEKLY_DOLLARS / RATE * 3600
OVERHEAD_SECONDS = 3600
SHUTDOWN_MARGIN = 900
PUBLICATION_SECONDS = 900
BOOTSTRAP_SECONDS = 1800
UPLOAD_RESERVE_SECONDS = 300


def atomic(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    with temporary.open("w", encoding="utf-8") as out:
        json.dump(value, out, indent=2, allow_nan=False)
        out.flush()
        os.fsync(out.fileno())
    os.replace(temporary, path)


@contextmanager
def locked(path, *, blocking=False):
    """OS lock is released on crash; do not use a stale PID as ownership."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+b") as handle:
        if handle.tell() == 0:
            handle.write(b"0")
            handle.flush()
        handle.seek(0)
        if os.name == "nt":
            import msvcrt
            msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK if blocking else msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | (0 if blocking else fcntl.LOCK_NB))
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == "nt":
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def week_start(now):
    day = datetime.fromtimestamp(now, timezone.utc)
    return (day - timedelta(days=day.weekday())).replace(
        hour=0, minute=0, second=0, microsecond=0).timestamp()


def number(value, *, positive=True):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError("duration must be finite")
    if value < 0 or (positive and value == 0):
        raise ValueError("duration must be positive")
    return value


class Ledger:
    def __init__(self, path, *, initial_seconds=None, initial_week=None):
        self.path = Path(path)
        if initial_seconds is not None:
            number(initial_seconds, positive=False)
            with locked(str(self.path) + ".lock"):
                if self.path.exists():
                    raise ValueError("ledger already exists; cannot reset usage")
                atomic(self.path, {
                    "schema_version": 1, "sessions": [], "active": None,
                    "seed": {"week": week_start(time.time() if initial_week is None else initial_week),
                             "seconds": initial_seconds},
                })

    def read(self):
        if not self.path.exists():
            raise ValueError("ledger requires an explicit historical usage seed")
        data = json.loads(self.path.read_text(encoding="utf-8"))
        if data.get("schema_version") != 1 or not isinstance(data.get("sessions"), list):
            raise ValueError("invalid ledger")
        return data

    @staticmethod
    def usage(data, now):
        start = week_start(now)
        end = start + 7 * 86400
        seconds = data["seed"]["seconds"] if data["seed"]["week"] == start else 0
        for item in data["sessions"] + ([data["active"]] if data["active"] else []):
            stop = item.get("end", now)
            seconds += max(0, min(end, stop) - max(start, item["start"]))
        return seconds

    def week_seconds(self, now):
        return self.usage(self.read(), now)

    def reserve(self, job_id, seconds, now, *, source_job_id=None):
        number(seconds)
        number(now)
        with locked(str(self.path) + ".lock"):
            data = self.read()
            if data["active"]:
                raise ValueError("an active or unconfirmed session already exists")
            if any(s["job_id"] == job_id for s in data["sessions"]):
                raise ValueError("job identity already used")
            if now + seconds >= week_start(now) + 7 * 86400:
                raise ValueError("reservation crosses weekly boundary")
            if self.usage(data, now) + seconds > WEEKLY_SECONDS:
                raise ValueError("reservation exceeds weekly ceiling")
            data["active"] = {"job_id": job_id, "start": now, "reserved_seconds": seconds,
                              "deadline": now + seconds, "source_job_id": source_job_id or job_id}
            atomic(self.path, data)
            return data["active"]

    def finish(self, now):
        with locked(str(self.path) + ".lock"):
            data = self.read()
            if not data["active"]:
                return
            if now < data["active"]["start"]:
                raise ValueError("clock reversed; refusing negative usage")
            data["active"]["end"] = now
            data["sessions"].append(data["active"])
            data["active"] = None
            atomic(self.path, data)


class Azure:
    def __init__(self, config, execute=subprocess.run):
        self.config = config
        self.execute = execute

    def call(self, args, timeout=180):
        result = self.execute([self.config["az"], *args, "--subscription", self.config["subscription"],
                               "--only-show-errors", "-o", "json"],
                              capture_output=True, text=True, timeout=timeout)
        if result.returncode:
            # Private diagnostics are deliberately excluded from result bundles/public comments.
            if self.config.get("state_dir"):
                atomic(Path(self.config["state_dir"]) / "azure-error.json",
                       {"time": time.time(), "returncode": result.returncode, "stderr": result.stderr})
            raise RuntimeError("Azure CLI failed; inspect private controller log")
        return json.loads(result.stdout) if result.stdout.strip() else None

    def vm_args(self):
        return ["--resource-group", self.config["resource_group"], "--name", self.config["vm"]]

    def power(self):
        value = self.call(["vm", "get-instance-view", *self.vm_args(),
                          "--query", "instanceView.statuses[?starts_with(code, 'PowerState/')].displayStatus"])
        return value[0] if isinstance(value, list) and len(value) == 1 else "unknown"

    def set_lease(self, job_id, deadline, *, bootstrap_deadline=None):
        cfg = self.config
        resource = ("/subscriptions/" + cfg["subscription"] + "/resourceGroups/"
                    + cfg["resource_group"] + "/providers/Microsoft.Compute/virtualMachines/" + cfg["vm"])
        # Generic vm update cannot set a nested key when Azure omits the tags object.
        # Merge works for bare VMs and retains unrelated operator tags.
        self.call(["tag", "update", "--resource-id", resource, "--operation", "Merge", "--tags",
                   "FPOfflineJob=" + job_id, "FPOfflineDeadline=" + str(deadline),
                   "FPOfflineBootstrapDeadline=" + str(bootstrap_deadline if bootstrap_deadline is not None else deadline - PUBLICATION_SECONDS)])

    def start(self):
        self.call(["vm", "start", *self.vm_args(), "--no-wait"])

    def deallocate(self):
        self.call(["vm", "deallocate", *self.vm_args(), "--no-wait"])

    def submit(self, name, script, *, timeout=300):
        # File-backed REST keeps complete scripts out of cmd.exe's length/quoting boundary.
        from urllib.parse import quote
        cfg = self.config
        request = Path(cfg["state_dir"]) / "requests" / (name + ".json")
        atomic(request, {"location": cfg["location"], "properties": {
            "source": {"script": script}, "asyncExecution": True, "timeoutInSeconds": int(timeout)}})
        url = ("https://management.azure.com/subscriptions/" + quote(cfg["subscription"], safe="")
               + "/resourceGroups/" + quote(cfg["resource_group"], safe="")
               + "/providers/Microsoft.Compute/virtualMachines/" + quote(cfg["vm"], safe="")
               + "/runCommands/" + quote(name, safe="") + "?api-version=2025-04-01")
        return self.call(["rest", "--method", "put", "--url", url, "--body", "@" + str(request)], timeout=240)

    def command(self, name):
        return self.call(["vm", "run-command", "show",
                          "--resource-group", self.config["resource_group"],
                          "--vm-name", self.config["vm"], "--name", name,
                          "--expand", "instanceView"])

    def delete_command(self, name):
        self.call(["vm", "run-command", "delete", "--resource-group", self.config["resource_group"],
                   "--vm-name", self.config["vm"], "--name", name, "--yes"])

    def cleanup(self, name):
        pending = Path(self.config["state_dir"]) / "pending-command-cleanup" / (name + ".json")
        completed = Path(self.config["state_dir"]) / "completed-command-cleanup" / (name + ".json")
        if completed.exists():
            return True
        try:
            self.delete_command(name)
            atomic(completed, {"command": name, "time": time.time()})
            pending.unlink(missing_ok=True)
            return True
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError):
            atomic(pending, {"command": name, "time": time.time()})
            return False

    def script(self, script, *, timeout=180):
        name = "fp-read-" + uuid.uuid4().hex[:16]
        try:
            self.submit(name, script, timeout=timeout)
            deadline = time.monotonic() + timeout + 120
            while time.monotonic() < deadline:
                value = self.command(name).get("instanceView", {})
                state = str(value.get("executionState", "")).lower()
                if state in {"succeeded", "failed", "timedout", "canceled"}:
                    if state != "succeeded" or value.get("exitCode") != 0:
                        raise RuntimeError("guest management command failed")
                    return value.get("output", "").strip()
                time.sleep(3)
            raise TimeoutError("guest management command did not finish")
        finally:
            self.cleanup(name)


def retire(azure, ledger, *, expected_job=None, clock=time.time, sleep=time.sleep, attempts=20):
    """Fenced against successor admission; never release an unconfirmed interval."""
    if expected_job is None:
        active = ledger.read()["active"]
        if active is None:
            return
        expected_job = active["job_id"]
    for _ in range(attempts):
        try:
            with locked(ledger.path.parent / "admission.lock"):
                active = ledger.read()["active"]
                if active is None or active["job_id"] != expected_job:
                    return
                azure.deallocate()
                if azure.power() == "VM deallocated":
                    ledger.finish(clock())
                    return
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError):
            pass
        sleep(5)
    raise RuntimeError("deallocation unconfirmed; ledger remains active")
