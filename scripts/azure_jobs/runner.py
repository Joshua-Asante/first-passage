"""Shared CLI for Codex and Claude Code. All instance binding is local configuration."""
from __future__ import annotations
import argparse
import base64
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import zipfile
from .control import Azure, Ledger, OVERHEAD_SECONDS, SHUTDOWN_MARGIN, PUBLICATION_SECONDS, RATE, atomic, locked, retire
from .contract import validate, inside, sha256, verify_inventory, verified

ROOT = Path(__file__).resolve().parents[2]


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def encoded(value):
    return base64.b64encode(json.dumps(value).encode()).decode()


def unpack(archive, destination):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as stream:
        names = stream.namelist()
        if len(names) != len(set(names)) or "manifest.json" not in names:
            raise ValueError("invalid archive inventory")
        rows = json.loads(stream.read("manifest.json"))
        if set(names) != set(rows) | {"manifest.json"}:
            raise ValueError("archive inventory mismatch")
        for name in names:
            path = inside(destination, name)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(stream.read(name))
    verify_inventory(destination, rows)
    return rows


def blob(config, action, name, file):
    azure = Azure(config)
    return azure.call(["storage", "blob", action, "--auth-mode", "login",
                       "--account-name", config["storage_account"], "--container-name", config["container"],
                       "--name", name, "--file", str(file), "--overwrite", "true"], timeout=300)


def results(config, job_id):
    target = Path(config["state_dir"]) / "results" / job_id
    target.mkdir(parents=True, exist_ok=True)
    blob(config, "download", job_id + "/archive.json", target / "archive.json")
    expected = read(target / "archive.json")
    if not re.fullmatch(r"[0-9a-f]{64}", expected.get("sha256", "")):
        raise ValueError("invalid archive digest")
    blob(config, "download", job_id + "/" + expected["sha256"] + ".zip", target / "results.zip")
    archive = target / "results.zip"
    if archive.stat().st_size != expected["bytes"] or sha256(archive) != expected["sha256"]:
        raise ValueError("result archive hash mismatch")
    rows = unpack(archive, target / "files")
    record = read(target / "files/runner/record.json")
    ledger = Ledger(Path(config["state_dir"]) / "ledger.json")
    sessions = [s for s in ledger.read()["sessions"] if s.get("source_job_id", s["job_id"]) == job_id]
    vm_seconds = sum(s["end"] - s["start"] for s in sessions)
    return {"directory": str(target), "artifacts": len(rows), "record": record,
            "verified": verified(record), "archive": expected, "deallocation_confirmed": bool(sessions),
            "vm_seconds": vm_seconds, "estimated_dollars": vm_seconds * RATE / 3600,
            "cpu_report": cpu_report(config)}


def cpu_report(config, *, now=None):
    now = time.time() if now is None else now
    from datetime import datetime, timezone
    from .control import week_start
    month = datetime.fromtimestamp(now, timezone.utc).strftime("%Y-%m")
    weekly = monthly = 0.0
    known = set()
    for path in (Path(config["state_dir"]) / "results").glob("*/files/runner/record.json"):
        record = read(path)
        if not isinstance(record.get("cpu_seconds"), (int, float)) or not record.get("finished_at"):
            continue
        known.add(path.parents[2].name)
        ended = record["finished_at"]
        if week_start(ended) == week_start(now):
            weekly += record["cpu_seconds"] / 3600
        if datetime.fromtimestamp(ended, timezone.utc).strftime("%Y-%m") == month:
            monthly += record["cpu_seconds"] / 3600
    submitted = {p.name for p in (Path(config["state_dir"]) / "jobs").glob("*") if p.is_dir()}
    return {"week_process_cpu_hours": weekly, "month_process_cpu_hours": monthly,
            "monthly_planning_allowance_cpu_hours": 5000,
            "basis": "retrieved process-tree measurements, assigned to completion period",
            "jobs_without_cpu_results": sorted(submitted - known)}


def status(config, job_id):
    state = Path(config["state_dir"])
    cached = state / "status" / (job_id + ".json")
    cached.parent.mkdir(parents=True, exist_ok=True)
    try:
        blob(config, "download", job_id + "/state.json", cached)
        result = read(cached)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError):
        result = {"status": "unknown", "reason": "published state unavailable; inspect private Azure diagnostics", "state_read_failed": True}
    azure = Azure(config)
    power = azure.power()
    if power == "VM running":
        directory = (config["guest_root"] + "/jobs/" + job_id).replace("'", "''")
        script = ("$d='" + directory + "'; "
                  "if(Test-Path -LiteralPath ($d+'/state.json')) {"
                  "$s=Get-Content -Raw -LiteralPath ($d+'/state.json') | ConvertFrom-Json;"
                  "$p=$null; if(Test-Path -LiteralPath ($d+'/progress.json')) {"
                  "$p=Get-Content -Raw -LiteralPath ($d+'/progress.json') | ConvertFrom-Json };"
                  "@{status=$s.status;phase=$s.phase;exit_code=$s.exit_code;"
                  "source_stable=$s.source_stable;progress=$p}|ConvertTo-Json -Depth 6 -Compress"
                  "} else { '{\"status\":\"preparing\"}' }")
        try:
            result = json.loads(azure.script(script))
        except (ValueError, RuntimeError, OSError, subprocess.SubprocessError):
            result["guest_state_read_failed"] = True
    local = state / "jobs" / job_id
    for filename in ("controller-error.json", "observation.json", "terminal-observation.json", "stop-request.json"):
        if (local / filename).exists():
            result[filename.removesuffix(".json")] = read(local / filename)
    result["cpu_report"] = cpu_report(config)
    result["vm_power"] = power
    result["week_vm_seconds"] = Ledger(state / "ledger.json").week_seconds(time.time())
    result["week_estimated_dollars"] = result["week_vm_seconds"] * RATE / 3600
    return result


def clean_source():
    commit = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
    dirty = subprocess.check_output(["git", "-C", str(ROOT), "status", "--porcelain", "--untracked-files=all"], text=True).strip()
    if dirty or not re.fullmatch("[0-9a-f]{40}", commit):
        raise ValueError("runner refuses dirty or unpinned source")
    return commit


def launch_guardian(config_path, session_path):
    args = [sys.executable, "-I", str(ROOT / "scripts/azure_jobs/entry.py"),
            "--config", str(config_path), "_guardian", str(session_path)]
    output = Path(session_path).parent / "guardian.log"
    with output.open("ab") as log:
        flags = 0x00000008 | 0x00000200 | 0x01000000 if os.name == "nt" else 0
        subprocess.Popen(args, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=log, stderr=log,
                         creationflags=flags, start_new_session=os.name != "nt", close_fds=True)
    deadline = time.monotonic() + 20
    ack = Path(session_path).parent / "guardian-ready.json"
    while time.monotonic() < deadline:
        if ack.exists():
            return
        time.sleep(0.2)
    raise RuntimeError("independent guardian did not acknowledge; VM must not start")


def run(config, config_path, spec, *, mode="execute"):
    if mode not in {"execute", "republish"}:
        raise ValueError("invalid session mode")
    validate(spec)
    source = clean_source()
    azure = Azure(config)
    state = Path(config["state_dir"])
    ledger = Ledger(state / "ledger.json")
    import uuid
    session_id = spec["job_id"] if mode == "execute" else "recover-" + uuid.uuid4().hex[:24]
    with locked(state / "admission.lock"):
        if mode == "republish" and not (state / "jobs" / spec["job_id"] / "session.json").exists():
            raise ValueError("cannot recover an unknown job")
        job_dir = state / "jobs" / session_id
        if job_dir.exists():
            raise ValueError("job already submitted; use status/results")
        if azure.power() != "VM deallocated":
            raise ValueError("VM must be verified deallocated before admission")
        seconds = spec["max_wall_seconds"] + OVERHEAD_SECONDS if mode == "execute" else OVERHEAD_SECONDS
        session = ledger.reserve(session_id, seconds, time.time(), source_job_id=spec["job_id"])
        job_dir.mkdir(parents=True)
        session.update(spec=spec, mode=mode, runner_commit=source, bootstrap_deadline=min(time.time() + 2400, session["deadline"] - SHUTDOWN_MARGIN - PUBLICATION_SECONDS))
        atomic(job_dir / "session.json", session)
        atomic(job_dir / "spec.json", spec)
        try:
            launch_guardian(config_path, job_dir / "session.json")
        except BaseException:
            # No start has been issued; verify the observed state before closing.
            if azure.power() == "VM deallocated":
                ledger.finish(time.time())
            raise
        # The independent guardian owns start + submission, closing the crash window
        # between request admission and launch. The front-end never starts the VM.
        return {"job_id": spec["job_id"], "session_id": session_id, "mode": mode, "status": "admitted",
                "reserved_seconds": session["reserved_seconds"]}


def reap_reason(session, heartbeat, now):
    if now >= session["deadline"]:
        return "deadline"
    if now - (heartbeat if heartbeat is not None else session["start"]) > 600:
        return "controller lost"
    return None


def reaper(config, session_path):
    session_path = Path(session_path)
    session = read(session_path)
    ledger = Ledger(Path(config["state_dir"]) / "ledger.json")
    azure = Azure(config)
    atomic(session_path.parent / "reaper-ready.json", {"time": time.time()})
    while True:
        active = ledger.read()["active"]
        if active is None or active["job_id"] != session["job_id"]:
            return
        beat_path = session_path.parent / "heartbeat.json"
        try:
            heartbeat = read(beat_path)["time"]
        except (OSError, ValueError):
            heartbeat = None
        reason = reap_reason({**session, "deadline": session["deadline"] - SHUTDOWN_MARGIN}, heartbeat, time.time())
        if reason:
            atomic(session_path.parent / "stop-request.json", {"reason": reason})
            try:
                retire(azure, ledger, expected_job=session["job_id"])
                return
            except (OSError, ValueError, RuntimeError, subprocess.SubprocessError):
                pass
        time.sleep(5)


def launch_reaper(config_path, session_path):
    args = [sys.executable, "-I", str(ROOT / "scripts/azure_jobs/entry.py"),
            "--config", str(config_path), "_reaper", str(session_path)]
    with (Path(session_path).parent / "reaper.log").open("ab") as log:
        flags = 0x00000008 | 0x00000200 | 0x01000000 if os.name == "nt" else 0
        subprocess.Popen(args, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=log, stderr=log,
                         creationflags=flags, start_new_session=os.name != "nt", close_fds=True)
    until = time.monotonic() + 20
    while time.monotonic() < until:
        if (Path(session_path).parent / "reaper-ready.json").exists():
            return
        time.sleep(0.2)
    raise RuntimeError("reaper did not acknowledge")


def heartbeat(session_path):
    if (Path(session_path).parent / "stop-request.json").exists():
        raise RuntimeError("independent reaper fenced this session")
    atomic(Path(session_path).parent / "heartbeat.json", {"time": time.time()})


def retain_and_cleanup(azure, directory, name):
    """Attempt one last read before deletion; retain earlier observations separately."""
    try:
        value = azure.command(name)
        atomic(directory / "terminal-observation.json", {"time": time.time(), **value})
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        atomic(directory / "terminal-read-error.json", {"type": type(exc).__name__})
    azure.cleanup(name)


def retry_cleanup(config, azure, current_job, session_path, deadline):
    state = Path(config["state_dir"])
    commands = {read(p)["command"] for p in (state / "pending-command-cleanup").glob("*.json")}
    # Include submissions from earlier runner versions, which had no retry tracker.
    for path in (state / "jobs").glob("*/submitted.json"):
        if path.parent.name != current_job:
            commands.add(read(path)["command"])
    for name in sorted(commands):
        if not re.fullmatch(r"fp-(?:job|read)-[a-z0-9-]+", name):
            raise ValueError("invalid retained command identity")
        if time.time() + 240 >= deadline:
            raise TimeoutError("bootstrap cleanup exhausted its allowance")
        heartbeat(session_path)
        azure.cleanup(name)


def guardian(config, session_path, config_path=None):
    session_path = Path(session_path)
    session = read(session_path)
    state = Path(config["state_dir"])
    ledger = Ledger(state / "ledger.json")
    azure = Azure(config)
    atomic(session_path.parent / "guardian-ready.json", {"pid": os.getpid(), "time": time.time()})
    try:
        heartbeat(session_path)
        launch_reaper(config_path, session_path)
        heartbeat(session_path)
        with locked(state / "admission.lock", blocking=True):
            active = ledger.read()["active"]
            if not active or active["job_id"] != session["job_id"]:
                return
            heartbeat(session_path)
            azure.set_lease(session["job_id"], session["deadline"] - SHUTDOWN_MARGIN)
            heartbeat(session_path)
            azure.start()
        while azure.power() != "VM running":
            heartbeat(session_path)
            if time.time() >= session["bootstrap_deadline"]:
                raise TimeoutError("startup deadline")
            time.sleep(5)
        retry_cleanup(config, azure, session["job_id"], session_path, session["bootstrap_deadline"])
        guest_config = {**config, "deadline": session["deadline"] - SHUTDOWN_MARGIN,
                        "execution_deadline": session["deadline"] - SHUTDOWN_MARGIN - PUBLICATION_SECONDS,
                        "session_id": session["job_id"], "mode": session.get("mode", "execute")}
        # Resource identity remains private and is never included in result bundles.
        request = {"config": guest_config, "spec": session["spec"], "runner_commit": session["runner_commit"]}
        script = (ROOT / "scripts/azure_jobs/bootstrap.ps1").read_text(encoding="utf-8-sig")
        script = "$RequestBase64 = '" + encoded(request) + "'\n" + script
        name = "fp-job-" + session["job_id"]
        heartbeat(session_path)
        azure.submit(name, script, timeout=int(session["reserved_seconds"] - SHUTDOWN_MARGIN))
        atomic(session_path.parent / "submitted.json", {"command": name})
        while time.time() < session["deadline"] - SHUTDOWN_MARGIN:
            heartbeat(session_path)
            power = azure.power()
            atomic(session_path.parent / "power.json", {"time": time.time(), "power": power})
            if power == "VM deallocated":
                retire(azure, ledger, expected_job=session["job_id"])
                return
            view = azure.command(name).get("instanceView", {})
            atomic(session_path.parent / "observation.json", {"time": time.time(), "instanceView": view})
            execution = str(view.get("executionState", "")).lower()
            if execution in {"succeeded", "failed", "timedout", "canceled"}:
                break
            time.sleep(15)
    except BaseException as exc:
        atomic(session_path.parent / "controller-error.json", {"type": type(exc).__name__, "time": time.time()})
    finally:
        # Azure cannot delete Run Commands while the VM is deallocated. Try before
        # shutdown and persist each failure for the next bounded start.
        submitted = session_path.parent / "submitted.json"
        try:
            if submitted.exists():
                retain_and_cleanup(azure, session_path.parent, read(submitted)["command"])
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError):
            pass  # Diagnostic storage and cleanup cannot veto deallocation.
        # Never abandon an open billing interval because a deallocation API call failed.
        while True:
            try:
                active = ledger.read()["active"]
                if active is None or active["job_id"] != session["job_id"]:
                    break
                retire(azure, ledger, expected_job=session["job_id"])
            except (OSError, ValueError, RuntimeError, subprocess.SubprocessError):
                time.sleep(10)


def reconcile(config):
    state = Path(config["state_dir"])
    with locked(state / "admission.lock"):
        if Azure(config).power() != "VM deallocated":
            raise ValueError("VM is not deallocated; use cancel to stop active work")
        Ledger(state / "ledger.json").finish(time.time())
    return {"deallocation_confirmed": True}


def cancel(config, job_id):
    state = Path(config["state_dir"])
    ledger = Ledger(state / "ledger.json")
    active = ledger.read()["active"]
    if not active or job_id not in {active["job_id"], active.get("source_job_id")}:
        raise ValueError("job is not the active session")
    azure = Azure(config)
    directory = state / "jobs" / active["job_id"]
    session = read(directory / "session.json")
    if session.get("mode") == "republish":
        atomic(directory / "stop-request.json", {"reason": "cancelled"})
        retire(azure, ledger, expected_job=active["job_id"])
        return {"job_id": job_id, "session_id": active["job_id"], "status": "interrupted"}
    path = config["guest_root"].replace("'", "''") + "/jobs/" + job_id + "/cancel"
    azure.script("$p='" + path + "'; New-Item -ItemType Directory -Force (Split-Path $p) | Out-Null; Set-Content -LiteralPath $p -Value cancel")
    return {"job_id": job_id, "status": "cancellation_requested"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    subs = parser.add_subparsers(dest="action", required=True)
    subs.add_parser("run").add_argument("spec", type=Path)
    for action in ("status", "results", "cancel"):
        command = subs.add_parser(action)
        command.add_argument("job_id")
        if action == "results":
            command.add_argument("--recover", action="store_true", help="admit budgeted disk-only republishing; never rerun the job")
    subs.add_parser("_guardian").add_argument("session", type=Path)
    subs.add_parser("_reaper").add_argument("session", type=Path)
    subs.add_parser("reconcile", help="verify deallocation and close a stranded reservation")
    seed = subs.add_parser("init-ledger", help="one-time conservative historical running-time seed")
    seed.add_argument("--historical-seconds", type=float, required=True)
    args = parser.parse_args()
    config = read(args.config)
    if args.action == "run":
        output = run(config, args.config.resolve(), read(args.spec))
    elif args.action == "_guardian":
        guardian(config, args.session, args.config.resolve())
        return
    elif args.action == "_reaper":
        reaper(config, args.session)
        return
    elif args.action == "reconcile":
        output = reconcile(config)
    elif args.action == "init-ledger":
        Ledger(Path(config["state_dir"]) / "ledger.json", initial_seconds=args.historical_seconds)
        output = {"ledger_initialized": True}
    else:
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", args.job_id):
            raise ValueError("invalid job identity")
        if args.action == "results" and args.recover:
            spec = read(Path(config["state_dir"]) / "jobs" / args.job_id / "spec.json")
            output = run(config, args.config.resolve(), spec, mode="republish")
        else:
            output = globals()[args.action](config, args.job_id)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
