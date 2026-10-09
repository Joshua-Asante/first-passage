"""Guest supervision, process CPU accounting and durable result publication."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import threading
import zipfile
from scripts.agent_handoff import WindowsJob, spawn_provider
from .contract import validate, inventory, sha256, verified
from .control import atomic, locked, UPLOAD_RESERVE_SECONDS


def accounting(job):
    info = job._accounting()
    returned = job._wintypes.DWORD()
    if not job._kernel.QueryInformationJobObject(
        job.handle, job.JobObjectBasicAccountingInformation, job._ctypes.byref(info),
        job._ctypes.sizeof(info), job._ctypes.byref(returned)
    ):
        raise OSError("job CPU accounting failed")
    return (info.TotalUserTime + info.TotalKernelTime) / 10_000_000


def run_tree(command, cwd, output, *, deadline, job_name=None):
    """Assign suspended process before execution; closing owner kills descendants."""
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    started = time.time()
    mono = time.monotonic()
    duration = max(0, deadline - started)
    if (output / "cancel").exists() or duration <= 0:
        return {"status": "interrupted", "exit_code": 130, "reason": "cancelled" if (output / "cancel").exists() else "timeout",
                "cpu_seconds": 0, "wall_seconds": 0, "started_at": started, "finished_at": time.time()}
    owned = WindowsJob.create(name="Local\\FP-Offline-" + job_name if job_name else None)
    process = None
    cpu = 0.0
    reason = None
    try:
        with (output / "stdout.log").open("wb") as stdout, (output / "stderr.log").open("wb") as stderr:
            process = spawn_provider(command, cwd, stdout, stderr, job=owned)
            while process.poll() is None or owned.active_processes():
                cpu = accounting(owned)
                atomic(output / "progress.json", {"cpu_seconds": cpu, "wall_seconds": time.monotonic() - mono,
                                                  "heartbeat": time.time(), "pid": process.pid})
                if (output / "cancel").exists():
                    reason = "cancelled"
                    break
                if time.monotonic() - mono >= duration or time.time() >= deadline:
                    reason = "timeout"
                    break
                time.sleep(0.25)
            if reason:
                owned.terminate()
                process.wait(timeout=10)
                for _ in range(40):
                    if not owned.active_processes():
                        break
                    time.sleep(0.1)
                if owned.active_processes():
                    raise RuntimeError("owned descendants did not stop")
            cpu = accounting(owned)
            code = process.poll()
            if (output / "cancel").exists():
                reason = "cancelled"
            return {"status": "interrupted" if reason else ("completed" if code == 0 else "failed"),
                    "exit_code": 130 if reason else code, "reason": reason,
                    "cpu_seconds": cpu, "wall_seconds": time.monotonic() - mono,
                    "started_at": started, "finished_at": time.time()}
    finally:
        owned.close()


def bounded_snapshot(repo, directory, deadline):
    """Keep Git and hashing inside a killable process tree with a real cutoff."""
    result_path = directory / "snapshot.json"
    result = run_tree([sys.executable, "-I", str(Path(__file__).with_name("guest_entry.py")),
                       "snapshot", str(repo), str(result_path)], repo, directory, deadline=deadline)
    if result["status"] != "completed" or result["exit_code"] != 0:
        raise TimeoutError("source snapshot incomplete before its cutoff")
    return json.loads(result_path.read_text(encoding="utf-8"))


def checked(command, cwd=None, timeout=600, deadline=None):
    if deadline is not None:
        timeout = min(timeout, deadline - time.time())
        if timeout <= 0:
            raise TimeoutError("execution/publication cutoff reached")
    result = subprocess.run(list(map(str, command)), cwd=cwd, capture_output=True, text=True, timeout=timeout)
    if result.returncode:
        diagnostic = Path(__file__).resolve().parents[2] / ".cache/azure-private-error.json"
        atomic(diagnostic, {"stderr": result.stderr, "returncode": result.returncode})
        raise RuntimeError("guest preparation failed; diagnostics retained privately")
    return result.stdout.strip()


def checkout(config, commit, destination):
    from functools import partial
    checked = partial(globals()["checked"], deadline=config.get("preparation_deadline", config.get("execution_deadline")))
    if not destination.exists():
        destination.mkdir(parents=True)
        checked([config["git"], "init", destination])
        checked([config["git"], "-C", destination, "remote", "add", "origin", config["repository"]])
        checked([config["git"], "-C", destination, "config", "core.autocrlf", "false"])
        checked([config["git"], "-C", destination, "fetch", "--depth", "1", "origin", commit])
        checked([config["git"], "-C", destination, "checkout", "--detach", "FETCH_HEAD"])
    head = checked([config["git"], "-C", destination, "rev-parse", "HEAD"])
    dirty = checked([config["git"], "-C", destination, "status", "--porcelain", "--untracked-files=all"])
    if head != commit or dirty:
        raise ValueError("refusing dirty or unpinned guest checkout")


def environment(config, spec, repo):
    from functools import partial
    checked = partial(globals()["checked"], deadline=config.get("preparation_deadline", config.get("execution_deadline")))
    lock = repo / ("requirements-ops.lock" if spec["environment"] == "operations" else "requirements-research.lock")
    identity = sha256(lock)
    directory = Path(config["guest_root"]) / "envs" / spec["environment"] / identity
    python = directory / "Scripts/python.exe"
    if not python.exists():
        checked([config["python"], "-m", "venv", directory])
    checked([python, "-m", "pip", "install", "--disable-pip-version-check", "--require-hashes", "-r", lock], timeout=1200)
    if spec["environment"] == "operations":
        checked([python, "-m", "pip", "install", "--disable-pip-version-check", "-r", repo / "tools/local_verification/requirements-extra.txt"], timeout=1200)
        checked([python, "-I", repo / "scripts/fp.py", "--env", directory, "doctor"], cwd=repo)
    return python, directory, identity


def bundle(job_dir, repo, outputs, *, partial):
    started = time.monotonic()
    rows = inventory(repo, outputs, partial=partial) if repo.exists() else {}
    files = {name: repo / name for name in rows}
    for name in ("stdout.log", "stderr.log", "progress.json", "record.json", "spec.json", "bootstrap.log"):
        path = job_dir / name
        if path.exists():
            key = "runner/" + name
            files[key] = path
            rows[key] = {"sha256": sha256(path), "bytes": path.stat().st_size}
    atomic(job_dir / "manifest.json", rows)
    archive = job_dir / "results.zip.tmp"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as stream:
        for name, path in files.items():
            stream.write(path, name)
        stream.write(job_dir / "manifest.json", "manifest.json")
    os.replace(archive, job_dir / "results.zip")
    archive = job_dir / "results.zip"
    return {"sha256": sha256(archive), "bytes": archive.stat().st_size, "artifacts": len(rows), "bundle_seconds": time.monotonic() - started}


def keep_heartbeat(job_dir, stop):
    while not stop.is_set():
        try:
            atomic(job_dir / "heartbeat.json", {"time": time.time()})
        except OSError:
            pass  # A missed tick must not permanently disable liveness updates.
        stop.wait(2)


def execute(config, spec):
    validate(spec)
    root = Path(config["guest_root"])
    job_dir = root / "jobs" / spec["job_id"]
    job_dir.mkdir(parents=True, exist_ok=True)
    with locked(root / "guest.lock"):
        if (job_dir / "record.json").exists():
            atomic(root / "idle.json", {"job_id": config.get("session_id", spec["job_id"]), "time": time.time()})
            return  # Never retry a submitted identity, including interrupted jobs.
        atomic(job_dir / "spec.json", spec)
        state = {"status": "running", "phase": "preparing", "job_id": spec["job_id"],
                 "started_at": time.time(), "heartbeat": time.time()}
        atomic(job_dir / "state.json", state)
        record = {"schema_version": 2, "status": "not_started", "exit_code": None,
                  "verification_exit_code": None, "source_stable": False,
                  "capture_complete": False, "report_errors": [], "cpu_seconds": 0,
                  "wall_seconds": 0, "commit": spec["commit"]}
        atomic(job_dir / "record.json", record)
        repo = root / "repos" / spec["job_id"]
        stop_heartbeat = threading.Event()
        heart = threading.Thread(target=keep_heartbeat, args=(job_dir, stop_heartbeat), daemon=True)
        atomic(job_dir / "heartbeat.json", {"time": time.time()})
        heart.start()
        before = None
        publication_started = None
        try:
            checkout(config, spec["commit"], repo)
            python, env_dir, lock_hash = environment(config, spec, repo)
            os.environ["PATH"] = str(python.parent) + os.pathsep + str(Path(config["git"]).parent) + os.pathsep + os.environ["PATH"]
            os.environ["VIRTUAL_ENV"] = str(env_dir)
            os.environ.pop("PYTHONPATH", None)
            os.environ.pop("PYTHONHOME", None)
            os.environ.pop("FP_VERIFICATION_ID", None)
            before = bounded_snapshot(repo, job_dir / "source-before", config.get("preparation_deadline", config.get("execution_deadline", config["deadline"])))
            record["preparation_seconds"] = time.time() - state["started_at"]
            if before["commit"] != spec["commit"] or before["status"]:
                raise ValueError("refusing dirty source")
            command = [str(python), "-I", *spec["command"]]
            if spec["environment"] == "operations":
                command = [str(python), "-I", "scripts/fp.py", "--env", str(env_dir), *spec["command"][1:]]
            deadline = min(time.time() + spec["max_wall_seconds"], config.get("execution_deadline", config["deadline"]))
            atomic(job_dir / "state.json", {**state, "phase": "executing", "deadline": deadline})
            record.update(run_tree(command, repo, job_dir, deadline=deadline, job_name=spec["job_id"]))
            publication_started = time.time()
            after = bounded_snapshot(repo, job_dir / "source-after", config["deadline"] - UPLOAD_RESERVE_SECONDS)
            record["post_execution_snapshot_seconds"] = time.time() - publication_started
            record.update(source_stable=before == after, capture_complete=True,
                          interpreter=str(python), environment=spec["environment"], lock_sha256=lock_hash,
                          command=command)
            record["verification_exit_code"] = record["exit_code"] or (0 if record["source_stable"] else 3)
            # Operations pytest/check acceptance also requires the original launcher's full record.
            if spec["environment"] == "operations":
                records = list((repo / ".cache/fp-verification").glob("*/record.json"))
                record["launcher_records"] = [p.relative_to(repo).as_posix() for p in records]
                if not records or not all(verified(json.loads(p.read_text(encoding="utf-8"))) for p in records):
                    record["report_errors"].append("launcher evidence is incomplete or unsuccessful")
                    record["verification_exit_code"] = record["verification_exit_code"] or 5
            inventory(repo, spec["expected_outputs"], partial=record["status"] != "completed")
            if not verified(record) and record["status"] == "completed":
                record["status"] = "failed"
        except BaseException as exc:
            record.update(status="failed", verification_exit_code=record["verification_exit_code"] or 1,
                          error=type(exc).__name__ + ": " + str(exc))
        finally:
            record["session_wall_seconds"] = time.time() - state["started_at"]
            atomic(job_dir / "record.json", record)
            archive = bundle(job_dir, repo, spec["expected_outputs"], partial=True)
            atomic(job_dir / "archive.json", archive)
            # Publishing precedes idle shutdown. Failure retains disk files for later recovery.
            atomic(job_dir / "state.json", {**record, "job_id": spec["job_id"], "archive": archive})
            try:
                upload({**config, "publication_started_at": publication_started or time.time()}, job_dir, spec["job_id"])
                published = True
            except Exception:
                published = False
            atomic(job_dir / "state.json", {**record, "job_id": spec["job_id"],
                                           "results_published": published, "archive": archive})
            atomic(root / "idle.json", {"job_id": config.get("session_id", spec["job_id"]), "time": time.time()})
            stop_heartbeat.set()
            heart.join(timeout=5)


def upload(config, job_dir, job_id):
    if not config.get("storage_account") or not config.get("container"):
        raise RuntimeError("results destination is not configured")
    started = time.monotonic()
    descriptor = json.loads((job_dir / "archive.json").read_text())
    for filename in ("results.zip", "state.json", "archive.json"):
        if filename == "archive.json":
            descriptor["upload_seconds_before_descriptor"] = time.monotonic() - started
            if config.get("publication_started_at"):
                descriptor["publication_seconds_before_descriptor"] = time.time() - config["publication_started_at"]
            atomic(job_dir / "archive.json", descriptor)
        blob_name = descriptor["sha256"] + ".zip" if filename == "results.zip" else filename
        checked([config["az"], "storage", "blob", "upload", "--auth-mode", "login",
                 "--account-name", config["storage_account"], "--container-name", config["container"],
                 "--name", job_id + "/" + blob_name, "--file", job_dir / filename,
                 "--overwrite", "true", "--only-show-errors", "-o", "none"], timeout=300, deadline=config.get("deadline"))


def republish(config, spec):
    """Publish retained files only. No checkout, environment setup or execution."""
    validate(spec)
    root = Path(config["guest_root"])
    job = root / "jobs" / spec["job_id"]
    with locked(root / "guest.lock"):
        job.mkdir(parents=True, exist_ok=True)
        record_path = job / "record.json"
        record = json.loads(record_path.read_text()) if record_path.exists() else {}
        if record.get("status") not in {"completed", "failed", "interrupted"}:
            progress_path = job / "progress.json"
            progress = json.loads(progress_path.read_text()) if progress_path.exists() else {}
            record.update(status="interrupted", exit_code=130, verification_exit_code=130,
                          source_stable=False, capture_complete=False,
                          cpu_seconds=progress.get("cpu_seconds"), wall_seconds=progress.get("wall_seconds"),
                          finished_at=progress.get("heartbeat"), cpu_measurement="partial lower bound",
                          reason="supervisor ended without terminal evidence")
            atomic(record_path, record)
        if not (job / "spec.json").exists():
            atomic(job / "spec.json", spec)
        try:
            archive = bundle(job, root / "repos" / spec["job_id"], spec["expected_outputs"], partial=True)
            atomic(job / "archive.json", archive)
            atomic(job / "state.json", {**record, "job_id": spec["job_id"], "archive": archive})
            upload(config, job, spec["job_id"])
        finally:
            atomic(root / "idle.json", {"job_id": config["session_id"], "time": time.time()})


def main(mode="execute"):
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=Path)
    parser.add_argument("spec", type=Path)
    args = parser.parse_args()
    action = execute if mode == "execute" else republish
    action(json.loads(args.config.read_text(encoding="utf-8-sig")),
            json.loads(args.spec.read_text(encoding="utf-8-sig")))


if __name__ == "__main__":
    main()
