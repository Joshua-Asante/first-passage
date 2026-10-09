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
from .control import Azure, Ledger, OVERHEAD_SECONDS, SHUTDOWN_MARGIN, PUBLICATION_SECONDS, BOOTSTRAP_SECONDS, RATE, atomic, locked, retire, alarm, cleanup_pending
from .contract import validate, inside, sha256, verify_inventory, verified, completed_evidence

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
    if 'runner/record.json' not in rows:
        raise ValueError('runner record absent from archive')
    record = read(target / "files/runner/record.json")
    if record.get('status') == 'completed':
        if 'runner/spec.json' not in rows:
            raise ValueError('completed output missing job spec')
        completed_evidence(target / 'files', rows, record, read(target / 'files/runner/spec.json'))
    ledger = Ledger(Path(config["state_dir"]) / "ledger.json")
    ledger_state = ledger.read()
    sessions = [s for s in ledger_state["sessions"] if s.get("source_job_id", s["job_id"]) == job_id]
    vm_seconds = sum(s["end"] - s["start"] for s in sessions)
    workload_verified = verified(record)
    settled = bool(sessions) and not cleanup_pending(config["state_dir"])
    active = ledger_state["active"]
    if active and active.get("source_job_id", active["job_id"]) == job_id:
        settled = False
    return {"directory": str(target), "artifacts": len(rows), "record": record,
            "workload_verified": workload_verified, "verified": workload_verified and settled, "archive": expected, "deallocation_confirmed": bool(sessions),
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
    submitted = set()
    for path in (Path(config['state_dir']) / 'jobs').glob('*'):
        if not path.is_dir():
            continue
        try:
            session = read(path / 'session.json')
        except (OSError, ValueError):
            session = {}  # An unreadable session remains unknown; never hide its ID.
        source = session.get('source_job_id') if isinstance(session, dict) else None
        if (isinstance(session, dict) and session.get('mode') == 'republish'
                and isinstance(source, str) and re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', source)):
            submitted.add(source)
        else:
            submitted.add(path.name)
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
            with locked(state / "admission.lock", blocking=True):
                active = Ledger(state / "ledger.json").read()["active"]
                if (active and active.get("source_job_id", active["job_id"]) == job_id
                        and not active.get("start_pending") and not active.get("stop_requested")
                        and azure.power() == "VM running"):
                    result = json.loads(azure.script(script))
        except (ValueError, RuntimeError, OSError, subprocess.SubprocessError):
            result["guest_state_read_failed"] = True
    local = state / "jobs" / job_id
    if (state / "alarm.json").exists():
        result["alarm"] = read(state / "alarm.json")
    result["cleanup_pending"] = cleanup_pending(state)
    for filename in ("controller-error.json", "observation.json", "terminal-observation.json", "stop-request.json"):
        if (local / filename).exists():
            result[filename.removesuffix(".json")] = read(local / filename)
    result["cpu_report"] = cpu_report(config)
    result["vm_power"] = power
    if result.get("status") == "completed":
        result["workload_status"] = "completed"
        try:
            proof = results(config, job_id)
            result["status"] = "completed" if proof["verified"] else "cleanup"
            result["verified"] = proof["verified"]
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError):
            result["status"] = "publishing"
            result["verified"] = False
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
    if mode != "execute":
        raise ValueError("disk recovery mode is deferred")
    validate(spec)
    source = clean_source()
    azure = Azure(config)
    state = Path(config["state_dir"])
    ledger = Ledger(state / "ledger.json")
    session_id = spec["job_id"]
    with locked(state / "admission.lock"):
        if cleanup_pending(state):
            raise ValueError("pending command cleanup blocks admission")
        job_dir = state / "jobs" / session_id
        if job_dir.exists():
            raise ValueError("job already submitted; use status/results")
        if azure.power() != "VM deallocated":
            raise ValueError("VM must be verified deallocated before admission")
        seconds = spec["max_wall_seconds"] + OVERHEAD_SECONDS
        session = ledger.reserve(session_id, seconds, time.time(), source_job_id=spec["job_id"])
        try:
            job_dir.mkdir(parents=True)
            session.update(spec=spec, mode=mode, runner_commit=source,
                           bootstrap_deadline=min(time.time() + BOOTSTRAP_SECONDS,
                                                  session["deadline"] - SHUTDOWN_MARGIN - PUBLICATION_SECONDS))
            atomic(job_dir / "session.json", session)
            atomic(job_dir / "spec.json", spec)
            launch_guardian(config_path, job_dir / "session.json")
        except BaseException:
            # Admission lock fences a delayed guardian while closing its reservation.
            if azure.power() == "VM deallocated":
                ledger.finish(time.time())
            else:
                alarm(state, 'admission failed and deallocation is unconfirmed')
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
            try:
                atomic(session_path.parent / "stop-request.json", {"reason": reason})
            except OSError:
                pass  # State storage failure cannot veto the shutdown backstop.
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
            if not active or active["job_id"] != session["job_id"] or active.get("stop_requested"):
                return
            heartbeat(session_path)
            azure.set_lease(session["job_id"], session["deadline"] - SHUTDOWN_MARGIN,
                            bootstrap_deadline=session["bootstrap_deadline"])
            heartbeat(session_path)
            ledger.update_active(session['job_id'], start_pending=True)
            azure.start()
            ledger.update_active(session['job_id'], start_pending=False)
        while azure.power() != "VM running":
            heartbeat(session_path)
            if time.time() >= session["bootstrap_deadline"]:
                raise TimeoutError("startup deadline")
            time.sleep(5)
        if cleanup_pending(state):
            raise RuntimeError("pending cleanup blocks workload submission")
        guest_config = {**config, "deadline": session["deadline"] - SHUTDOWN_MARGIN,
                        "execution_deadline": session["deadline"] - SHUTDOWN_MARGIN - PUBLICATION_SECONDS,
                        "preparation_deadline": session["bootstrap_deadline"],
                        "session_id": session["job_id"], "mode": session.get("mode", "execute")}
        # Resource identity remains private and is never included in result bundles.
        request = {"config": guest_config, "spec": session["spec"], "runner_commit": session["runner_commit"]}
        script = (ROOT / "scripts/azure_jobs/bootstrap.ps1").read_text(encoding="utf-8-sig")
        script = "$RequestBase64 = '" + encoded(request) + "'\n" + script
        name = "fp-job-" + session["job_id"]
        with locked(state / "admission.lock", blocking=True):
            active = ledger.read()["active"]
            if not active or active["job_id"] != session["job_id"] or active.get("stop_requested"):
                return
            heartbeat(session_path)
            atomic(session_path.parent / "submitted.json", {"command": name})
            azure.submit(name, script, timeout=int(session["reserved_seconds"] - SHUTDOWN_MARGIN))
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
        alarm(state, "controller failed: " + type(exc).__name__)
        try:
            atomic(session_path.parent / "controller-error.json", {"type": type(exc).__name__, "time": time.time()})
        except OSError:
            pass
    finally:
        # Azure cannot delete Run Commands while the VM is deallocated. Try before
        # shutdown. Persisted failure blocks subsequent admissions.
        submitted = session_path.parent / "submitted.json"
        try:
            if submitted.exists():
                retain_and_cleanup(azure, session_path.parent, read(submitted)["command"])
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError):
            pass  # Diagnostic storage and cleanup cannot veto deallocation.
        retire(azure, ledger, expected_job=session["job_id"])
        if cleanup_pending(state):
            alarm(state, 'command cleanup remains pending; admission blocked')


def reconcile(config):
    state = Path(config["state_dir"])
    with locked(state / "admission.lock"):
        if Azure(config).power() != "VM deallocated":
            raise ValueError("VM is not deallocated; use cancel to stop active work")
        ledger = Ledger(state / "ledger.json")
        active = ledger.read()["active"]
        if active and active.get("start_pending"):
            raise ValueError("pending start requires independent settlement; cannot reconcile")
        ledger.finish(time.time())
    return {"deallocation_confirmed": True}


def cancel(config, job_id, *, force=False):
    state = Path(config["state_dir"])
    ledger = Ledger(state / "ledger.json")
    azure = Azure(config)
    with locked(state / "admission.lock", blocking=True):
        data = ledger.read()
        active = data['active']
        if not active or job_id not in {active['job_id'], active.get('source_job_id')}:
            if any(s['job_id'] == job_id for s in data['sessions']):
                return {'job_id': job_id, 'status': 'already_terminal'}
            raise ValueError('job is not the active session')
        directory = state / 'jobs' / active['job_id']
        try:
            atomic(directory / 'stop-request.json', {'reason': 'cancelled'})
            ledger.update_active(active['job_id'], stop_requested=True)
        except OSError:
            alarm(state, 'cancel state write failed; forcing deallocation')
        try:
            if not force and (directory / 'submitted.json').exists():
                path = config['guest_root'].replace("'", "''") + '/jobs/' + job_id + '/cancel'
                azure.script("$p='" + path + "'; New-Item -ItemType Directory -Force (Split-Path $p) | Out-Null; Set-Content -LiteralPath $p -Value cancel")
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError):
            alarm(state, 'guest cancellation delivery failed; forcing deallocation')
        finally:
            retire(azure, ledger, expected_job=active['job_id'], admission_locked=True)
    return {'job_id': job_id, 'status': 'cancelled', 'deallocation_confirmed': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    subs = parser.add_subparsers(dest="action", required=True)
    subs.add_parser("run").add_argument("spec", type=Path)
    for action in ("status", "results", "cancel"):
        command = subs.add_parser(action)
        command.add_argument("job_id")
        if action == "cancel":
            command.add_argument("--force", action="store_true", help="fence controller and deallocate without waiting for guest transport")
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
        if args.action == "cancel":
            output = cancel(config, args.job_id, force=args.force)
        else:
            output = globals()[args.action](config, args.job_id)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
