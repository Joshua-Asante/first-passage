"""Public job contracts and evidence integrity. No file-upload interface exists."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from .control import number


def relative(value):
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        raise ValueError("expected a safe relative path")
    path = PurePosixPath(value)
    # Win32 aliases trailing dots/spaces and case. Refuse ambiguous components;
    # normalize only the comparison so safe names retain their original spelling.
    parts = [p.casefold() for p in path.parts]
    if path.is_absolute() or any(p.endswith((".", " ")) or p == ".git"
                                 or p.startswith(".env") for p in parts):
        raise ValueError("forbidden output path")
    return value


def validate(spec):
    if not isinstance(spec, dict):
        raise ValueError("job spec must be an object")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", str(spec.get("job_id", ""))):
        raise ValueError("invalid job identity")
    if not re.fullmatch(r"[0-9a-f]{40}", str(spec.get("commit", ""))):
        raise ValueError("commit must be a pinned 40-character SHA")
    if spec.get("environment") != "operations":
        raise ValueError("v1 supports operations environment only")
    number(spec.get("max_wall_seconds"))
    command = spec.get("command")
    if not isinstance(command, list) or not command or any(not isinstance(a, str) or not a or "\0" in a for a in command):
        raise ValueError("command must be a nonempty argument array")
    entrypoint(command[0])
    if spec["environment"] == "operations" and command[0] != "scripts/fp.py":
        raise ValueError("operations commands must use scripts/fp.py")
    args = command[1:]
    if args[:1] == ['--workers']:
        if len(args) < 3 or args[1] not in {str(n) for n in range(9)}:
            raise ValueError('invalid operations launcher worker count')
        args = args[2:]
    elif args and args[0].startswith('--workers='):
        if args[0].split('=', 1)[1] not in {str(n) for n in range(9)}:
            raise ValueError('invalid operations launcher worker count')
        args = args[1:]
    if not args or (args[0] not in {'test', 'test-ops', 'check'}
                    and args[:3] != ['python', '-m', 'pytest']):
        raise ValueError('v1 requires a recorded operations launcher task')
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


def entrypoint(value, root=None):
    """Accept a checkout script, never a Python switch, stdin or a directory."""
    relative(value)
    if value.startswith('-') or value.endswith('/') or not PurePosixPath(value).parts:
        raise ValueError('entrypoint must be a checkout file')
    if root is None:
        return value
    path = inside(root, value)
    if not path.is_file():
        raise ValueError('entrypoint must be a checkout file')
    return path.resolve()


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


def launcher_directories(paths):
    if not isinstance(paths, list):
        raise ValueError('invalid launcher record list')
    directories = []
    for name in paths:
        relative(name)
        parts = PurePosixPath(name).parts
        if len(parts) != 4 or parts[:2] != ('.cache', 'fp-verification') or parts[-1] != 'record.json':
            raise ValueError('invalid launcher record path')
        directories.append(PurePosixPath(name).parent.as_posix())
    return directories


def completed_outputs(rows, outputs):
    """File-only archives cannot attest an empty directory or a stale disk copy."""
    for name in outputs:
        normalized = PurePosixPath(relative(name)).as_posix()
        prefix = '' if normalized == '.' else normalized + '/'
        if normalized not in rows and not any(p.startswith(prefix) and not p.startswith('runner/') for p in rows):
            raise ValueError('required output absent from archive: ' + name)


def launcher_evidence(root, paths, rows):
    directories = launcher_directories(paths)
    if not directories:
        raise ValueError('launcher evidence missing')
    for name, directory in zip(paths, directories):
        if name not in rows:
            raise ValueError('launcher record absent from archive')
        record = json.loads(inside(root, name).read_text(encoding='utf-8'))
        if not isinstance(record, dict) or not verified(record):
            raise ValueError('launcher record unsuccessful')
        artifacts = record.get('artifacts')
        if not isinstance(artifacts, dict) or not {'stdout.txt', 'stderr.txt'} <= artifacts.keys():
            raise ValueError('launcher captures missing')
        reports = record.get('junit', [])
        if not isinstance(reports, list) or any(not isinstance(r, dict) or not isinstance(r.get('file'), str)
                                               or r['file'] not in artifacts for r in reports):
            raise ValueError('launcher JUnit artifact missing')
        for artifact, digest in artifacts.items():
            relative(artifact)
            path = (PurePosixPath(directory) / artifact).as_posix()
            if (path not in rows or not isinstance(digest, str)
                    or not re.fullmatch('[0-9a-f]{64}', digest)
                    or rows[path]['sha256'] != digest or sha256(inside(root, path)) != digest):
                raise ValueError('launcher artifact missing or hash mismatch')


def completed_evidence(root, rows, record, spec):
    """Common publication/retrieval boundary; current manifest owns coverage."""
    if record.get('status') != 'completed':
        return
    validate(spec)
    completed_outputs(rows, spec['expected_outputs'])
    if spec['environment'] == 'operations':
        launcher_evidence(root, record.get('launcher_records', []), rows)
