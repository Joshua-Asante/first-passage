#!/usr/bin/env python3
"""Fail when an orientation document, or the T0 session-start set, exceeds its byte cap.

Gate id ``doc-budgets`` (always tier, scripts/gates.yml). Caps live in
scripts/doc_budgets.yml; sizes are measured after CRLF/CR -> LF normalisation so
a checkout's line endings never change the verdict. Fails closed (Rule 38): a
missing, empty or malformed config, an unknown key, a non-positive cap, an empty
T0 set or an untracked or missing path all exit 2.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG = Path("scripts/doc_budgets.yml")


def _cap(value, where: str) -> int:
    if type(value) is not int or value <= 0:
        raise ValueError(f"{where}: cap must be a positive integer, got {value!r}")
    return value


def load(repo: Path, config: Path) -> tuple[dict[str, int], list[str], int]:
    path = repo / config
    if not path.is_file():
        raise ValueError(f"{config}: missing")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not data:
        raise ValueError(f"{config}: empty or not a mapping")
    if set(data) != {"version", "files", "t0"}:
        raise ValueError(f"{config}: keys must be version, files, t0; got {sorted(data)}")
    if data["version"] != 1:
        raise ValueError(f"{config}: unsupported version {data['version']!r}")
    files, t0 = data["files"], data["t0"]
    if not isinstance(files, dict) or not files:
        raise ValueError(f"{config}: files must be a non-empty mapping")
    caps = {str(name): _cap(cap, f"files.{name}") for name, cap in files.items()}
    if not isinstance(t0, dict) or set(t0) != {"files", "cap"}:
        raise ValueError(f"{config}: t0 must have exactly files and cap")
    members = t0["files"]
    if not isinstance(members, list) or not members or len(set(members)) != len(members):
        raise ValueError(f"{config}: t0.files must be a non-empty list without repeats")
    return caps, [str(name) for name in members], _cap(t0["cap"], "t0.cap")


def size(repo: Path, name: str, tracked: set[str]) -> int:
    if name not in tracked or not (repo / name).is_file():
        raise ValueError(f"{name}: not a tracked file")
    data = (repo / name).read_bytes()
    return len(data.replace(b"\r\n", b"\n").replace(b"\r", b"\n"))


def check(repo: Path, config: Path = CONFIG) -> list[str]:
    """Return one report line per budget; raise ValueError on any malformed input."""
    caps, members, t0_cap = load(repo, config)
    listed = subprocess.run(["git", "ls-files", "-z", "--", *sorted(set(caps) | set(members))],
                            cwd=repo, check=True, stdout=subprocess.PIPE)
    tracked = {name for name in listed.stdout.decode("utf-8").split("\0") if name}
    sizes = {name: size(repo, name, tracked) for name in sorted(set(caps) | set(members))}
    lines = []
    for name, cap in caps.items():
        lines.append(f"{'OVER' if sizes[name] > cap else 'ok'} {name}: {sizes[name]} / {cap} B "
                     f"(headroom {cap - sizes[name]})")
    total = sum(sizes[name] for name in members)
    lines.append(f"{'OVER' if total > t0_cap else 'ok'} t0 ({' + '.join(members)} + hook): "
                 f"{total} / {t0_cap} B (headroom {t0_cap - total})")
    return lines


def main(argv=None, *, repo_root: Path = REPO_ROOT) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--config", type=Path, default=CONFIG)
    args = parser.parse_args(argv)
    try:
        lines = check(repo_root, args.config)
    except (OSError, UnicodeError, ValueError, yaml.YAMLError, subprocess.SubprocessError) as error:
        print(f"check_doc_budgets: {error}", file=sys.stderr)
        return 2
    for line in lines:
        print(line)
    return int(any(line.startswith("OVER") for line in lines))


if __name__ == "__main__":
    sys.exit(main())
