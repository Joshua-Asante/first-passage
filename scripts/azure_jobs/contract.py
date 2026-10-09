"""Public job contracts and evidence integrity. No file-upload interface exists."""
from __future__ import annotations
import hashlib
from pathlib import Path, PurePosixPath
import re
from .control import number


def relative(value):
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        raise ValueError("expected a safe relative path")
    path = PurePosixPath(value)
    # Windows aliases private components regardless of case. Normalize only the
    # comparison: accepted artifact names must retain their original spelling.
    parts = [p.casefold() for p in path.parts]
    if path.is_absolute() or any(p in {"..", ".git"} or p.startswith(".env") for p in parts):
        raise ValueError("forbidden output path")
    return value


def validate(spec):
    if not isinstance(spec, dict):
        raise ValueError("job spec must be an object")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", str(spec.get("job_id", ""))):
        raise ValueError("invalid job identity")
    if not re.fullmatch(r"[0-9a-f]{40}", str(spec.get("commit", ""))):
        raise ValueError("commit must be a pinned 40-character SHA")
    if spec.get("environment") not in {"operations", "research"}:
        raise ValueError("select operations or research environment")
    number(spec.get("max_wall_seconds"))
    command = spec.get("command")
    if not isinstance(command, list) or not command or any(not isinstance(a, str) or not a or "\0" in a for a in command):
        raise ValueError("command must be a nonempty argument array")
    relative(command[0])
    if spec["environment"] == "operations" and command[0] != "scripts/fp.py":
        raise ValueError("operations commands must use scripts/fp.py")
    if not isinstance(spec.get("authority"), str) or not spec["authority"].strip():
        raise ValueError("explicit run authority is required")
    if spec.get("private_inputs") != []:
        raise ValueError("private transfers are unsupported; a ruling does not enable copying")
    outputs = spec.get("expected_outputs")
    if not isinstance(outputs, list) or not outputs:
        raise ValueError("expected outputs are required")
    for output in outputs:
        relative(output)
    return spec


def inside(root, name):
    relative(name)
    root = Path(root).resolve()
    path = root / name
    for part in (path, *path.parents):
        if part == root:
            break
        if part.is_symlink() or (hasattr(part, "is_junction") and part.is_junction()):
            raise ValueError("forbidden artifact link")
    path.resolve().relative_to(root)
    return path


def sha256(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def inventory(root, outputs, *, partial=False):
    result = {}
    for name in outputs:
        path = inside(root, name)
        if not path.exists():
            if partial:
                continue
            raise ValueError("expected output missing: " + name)
        files = sorted(path.rglob("*")) if path.is_dir() else [path]
        for file in files:
            rel = file.relative_to(root).as_posix()
            inside(root, rel)
            if file.is_file():
                result[rel] = {"sha256": sha256(file), "bytes": file.stat().st_size}
    return result


def verify_inventory(root, rows):
    for name, expected in rows.items():
        path = inside(root, name)
        if not path.is_file() or path.stat().st_size != expected["bytes"] or sha256(path) != expected["sha256"]:
            raise ValueError("artifact hash/size mismatch: " + name)


def verified(record):
    return (record.get("status") == "completed"
            and type(record.get("exit_code")) is int and record["exit_code"] == 0
            and type(record.get("verification_exit_code")) is int and record["verification_exit_code"] == 0
            and record.get("source_stable") is True
            and record.get("capture_complete") is True
            and record.get("report_errors") == [])
