"""Credential-free guest watchdog. Task Scheduler restarts this after a crash."""
from __future__ import annotations
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from scripts.agent_handoff import WindowsJob, spawn_provider
from .control import Azure, atomic, locked, PUBLICATION_SECONDS
from .guest import bundle, upload


def metadata_lease(compute):
    import math
    import re
    tags = {t["name"]: t["value"] for t in compute.get("tagsList", [])}
    job_id = tags.get("FPOfflineJob", "")
    deadline = float(tags.get("FPOfflineDeadline", "nan"))
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", job_id) or not math.isfinite(deadline):
        raise ValueError("missing current Azure lease")
    bootstrap = float(tags.get("FPOfflineBootstrapDeadline", deadline - PUBLICATION_SECONDS))
    if not math.isfinite(bootstrap) or bootstrap > deadline:
        raise ValueError("invalid bootstrap deadline")
    return {"job_id": job_id, "deadline": deadline, "bootstrap_deadline": bootstrap}


def cloud_lease():
    import urllib.request
    request = urllib.request.Request(
        "http://169.254.169.254/metadata/instance/compute?api-version=2021-02-01",
        headers={"Metadata": "true"})
    # Metadata is link-local. Never forward it through an inherited proxy.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(request, timeout=2) as response:
        return metadata_lease(json.load(response))


def stop_reason(lease, idle, now):
    if not lease:
        return "missing lease"
    if now >= lease["deadline"]:
        return "deadline"
    if idle and idle.get("job_id") == lease["job_id"]:
        return "idle"
    return None


def job_stop_reason(lease, state, heartbeat, cancelled, now):
    if (not state or state.get("phase") == "preparing") and now >= lease["bootstrap_deadline"]:
        return "bootstrap deadline"
    if now >= lease["deadline"] - PUBLICATION_SECONDS:
        return "execution deadline"
    if cancelled and state.get("status") == "running":
        return "cancelled"
    if state.get("status") == "running" and now - heartbeat.get("time", state.get("started_at", now)) > 120:
        return "guest supervisor lost"
    return None


def read(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return None


def terminate_tree(name):
    import ctypes
    from ctypes import wintypes
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.OpenJobObjectW.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.LPCWSTR]
    kernel.OpenJobObjectW.restype = wintypes.HANDLE
    kernel.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
    kernel.TerminateJobObject.restype = wintypes.BOOL
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    handle = kernel.OpenJobObjectW(8, False, "Local\\FP-Offline-" + name)
    if not handle:
        if ctypes.get_last_error() == 2:
            return False
        raise OSError("cannot open owned job")
    try:
        if not kernel.TerminateJobObject(handle, 130):
            raise OSError("cannot terminate owned job")
        return True
    finally:
        kernel.CloseHandle(handle)


def recover(config, lease, reason):
    """Keep partial evidence; never turn missing terminal evidence into success."""
    job_id = lease.get("source_job_id", lease["job_id"])
    job_dir = Path(config["guest_root"]) / "jobs" / job_id
    job_dir.mkdir(parents=True, exist_ok=True)
    if reason != "guest supervisor lost":
        (job_dir / "cancel").touch()
        terminate_tree(job_id)
    lock = locked(Path(config["guest_root"]) / "guest.lock")
    try:
        lock.__enter__()
    except OSError:
        return False  # Live supervisor owns finalization and publication.
    try:
        if reason == "guest supervisor lost":
            (job_dir / "cancel").touch()
            terminate_tree(job_id)
        record = read(job_dir / "record.json") or {}
        if record.get("status") not in {"completed", "failed", "interrupted"}:
            progress = read(job_dir / "progress.json") or {}
            record.update(status="interrupted", exit_code=130, verification_exit_code=130,
                          source_stable=False, capture_complete=False, reason=reason,
                          cpu_seconds=progress.get("cpu_seconds"), wall_seconds=progress.get("wall_seconds"),
                          finished_at=progress.get("heartbeat"), cpu_measurement="partial lower bound")
            atomic(job_dir / "record.json", record)
        spec = read(job_dir / "spec.json")
        if spec:
            archive = bundle(job_dir, Path(config["guest_root"]) / "repos" / job_id,
                             spec["expected_outputs"], partial=True)
            atomic(job_dir / "archive.json", archive)
        atomic(job_dir / "state.json", record)
        try:
            upload(config, job_dir, job_id)
        except Exception:
            pass  # Retain disk results; never hold paid compute indefinitely for upload.
        return True
    finally:
        lock.__exit__(None, None, None)


def bounded_recover(config_path, lease, reason):
    """The watchdog owns the cutoff, independently of recovery I/O or Python.

    Kill-on-close owns the recovery worker and upload descendants. Never wait for
    them at the cutoff: deallocation takes priority; retained disk files can be
    republished under a separately admitted maintenance lease.
    """
    remaining = min(PUBLICATION_SECONDS, lease["deadline"] - time.time())
    if remaining <= 0:
        raise TimeoutError("recovery cutoff reached")
    cutoff = time.monotonic() + remaining
    owned = WindowsJob.create()
    try:
        with open(os.devnull, "wb") as output:
            process = spawn_provider(
                [sys.executable, "-I", str(Path(__file__).with_name("guest_entry.py")),
                 "recover", str(config_path), json.dumps(lease), reason],
                Path(__file__).resolve().parents[2], output, output, job=owned)
            while True:
                remaining = min(cutoff - time.monotonic(), lease["deadline"] - time.time())
                if remaining <= 0:
                    raise TimeoutError("recovery cutoff reached; disk evidence retained")
                code = process.poll()
                if code is not None:
                    if code not in {0, 75}:
                        raise RuntimeError("recovery failed; disk evidence retained")
                    return code == 0  # 75: live supervisor owns finalization.
                time.sleep(min(0.25, remaining))
    finally:
        owned.close()


def main(config_path):
    config = read(config_path)
    azure = Azure(config)
    root = Path(config["guest_root"])
    # A booted host gets a short bounded window to receive a new lease.
    boot_grace = time.monotonic() + 180
    lease = None
    lease_observed = 0
    while True:
        try:
            lease = cloud_lease()
            mapping = read(root / "control" / "sessions" / (lease["job_id"] + ".json"))
            if mapping and mapping.get("session_id") == lease["job_id"]:
                lease["source_job_id"] = mapping["source_job_id"]
            lease_observed = time.monotonic()
        except Exception:
            if time.monotonic() - lease_observed > 120:
                lease = None
        reason = stop_reason(lease, read(root / "idle.json"), time.time())
        if time.monotonic() < boot_grace and reason == "missing lease":
            time.sleep(2)
            continue
        if lease and not reason:
            job_dir = root / "jobs" / lease.get("source_job_id", lease["job_id"])
            state = read(job_dir / "state.json") or {}
            progress = read(job_dir / "heartbeat.json") or {}
            reason = job_stop_reason(lease, state, progress, (job_dir / "cancel").exists(), time.time())
        if reason:
            if lease and reason not in {"idle", "deadline"}:
                try:
                    recovered = bounded_recover(config_path, lease, reason)
                    if not recovered and reason != "bootstrap deadline" and time.time() < lease["deadline"]:
                        time.sleep(2)
                        continue
                except Exception as exc:
                    # No resource bindings or child diagnostics in public output.
                    try:
                        print("Watchdog recovery incomplete (" + type(exc).__name__
                              + "); deallocating with disk evidence retained", file=sys.stderr)
                    except OSError:
                        pass  # Even an unavailable diagnostic sink cannot veto shutdown.
            # Keep retrying even if controller/laptop has disappeared.
            try:
                try:
                    if lease and reason != "idle":
                        # Native calls only: no recovery, disk writes, polling or
                        # waits on the stalled supervisor. Stop only its named job.
                        terminate_tree(lease.get("source_job_id", lease["job_id"]))
                finally:
                    # Local stop failure must not veto deallocation or retries.
                    azure.deallocate()
            except (OSError, ValueError, RuntimeError, subprocess.SubprocessError):
                pass
            time.sleep(5)
        else:
            time.sleep(2)


if __name__ == "__main__":
    main(sys.argv[1])
