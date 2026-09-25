#!/usr/bin/env python3
"""evidence_archive.py — keep a second copy of every pinned private file.

A public record that pins a private file's SHA-256 proves which bytes were
used; it does not keep them. M-41 (docs/methodology/lessons/methodology_lessons.md)
records three losses where the only copy sat in a disposable worktree or VM:
the Striker MNQ Pine source (2026-07-03), the ORB D5 pin (2026-07-31) and the
Tradeify seven-strategy evidence base (2026-09-10).

The durable copy lives in the private ``first-passage-archive`` repository,
content-addressed as ``evidence/sha256/<aa>/<digest>`` with one
``evidence/INDEX.tsv`` row per archived file.

``put`` writes ``evidence/.gitattributes`` (``* -text``) into the clone so git
never rewrites the archived bytes' line endings, and the commits it prints must
run with ``-c core.autocrlf=false``; otherwise a global ``core.autocrlf=true``
would convert CRLF to LF and the committed blob would no longer hash to its own
content address.

  put <file>...   copy files into a local clone of the archive (verified), then
                  print the commit/push commands; ``--pinned`` archives every
                  pinned file present in this checkout.
  audit           report-only: every pinned digest is ARCHIVED (on the
                  archive's remote-tracking branch), UNPUSHED (only in the local
                  clone) or MISSING. With no archive clone it prints UNVERIFIED.

Pinned digests are read from the tracked manifests (``*SHA256SUMS``,
``*MANIFEST.sha256``) and from docs/evidence/PRIVATE_EVIDENCE.sha256, where a
record that pins private evidence outside those manifests registers it.

The archive clone is ``--archive``, else ``$FP_EVIDENCE_ARCHIVE``, else a
``first-passage-archive`` directory beside this checkout. ``put`` refuses any
clone whose ``origin`` is not the archive repository, so private bytes are never
staged into the public clone.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY = Path("docs/evidence/PRIVATE_EVIDENCE.sha256")
ARCHIVE_NAME = "first-passage-archive"
EVIDENCE_DIR = "evidence/sha256"
INDEX = "evidence/INDEX.tsv"
ATTRIBUTES = "evidence/.gitattributes"
ATTRIBUTES_TEXT = "* -text\n"
# GitHub rejects pushes carrying a file over 100 MB.
MAX_BYTES = 95 * 1024 * 1024
_LINE = re.compile(r"^([0-9a-fA-F]{64})\s+\*?(.+?)\s*$")


@dataclass(frozen=True)
class Pin:
    """One pinned digest and the manifest line that pins it."""

    digest: str
    name: str
    manifest: str

    def local_path(self, root: Path) -> Path:
        """Where the pinned bytes sit in a checkout: registry names are
        repo-root relative, manifest names are relative to the manifest."""
        registry = self.manifest == REGISTRY.as_posix()
        base = root if registry else root / Path(self.manifest).parent
        return base / self.name


def _git(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=str(cwd), check=False, capture_output=True,
                          text=True, encoding="utf-8", errors="replace")


def _manifests(root: Path) -> list[str]:
    listed = _git(root, "ls-files", "-z").stdout.split("\0")
    found = sorted(p for p in listed if p.endswith(("SHA256SUMS", "MANIFEST.sha256")))
    if REGISTRY.as_posix() not in found and (root / REGISTRY).is_file():
        found.append(REGISTRY.as_posix())
    return found


def collect_pins(root: Path) -> list[Pin]:
    """Every (digest, name) line of every pin manifest; comments and blanks skipped."""
    pins: list[Pin] = []
    for manifest in _manifests(root):
        path = root / manifest
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            match = _LINE.match(line.strip())
            if match:
                pins.append(Pin(match.group(1).lower(), match.group(2), manifest))
    return pins


def sha256_file(path: Path) -> str:
    """Streamed SHA-256 of a file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def blob_path(digest: str) -> str:
    """Content address of a digest inside the archive clone."""
    return f"{EVIDENCE_DIR}/{digest[:2]}/{digest}"


def resolve_archive(explicit: str | None) -> Path:
    """--archive, else $FP_EVIDENCE_ARCHIVE, else a sibling first-passage-archive."""
    if explicit:
        return Path(explicit).expanduser().resolve()
    env = os.environ.get("FP_EVIDENCE_ARCHIVE")
    if env:
        return Path(env).expanduser().resolve()
    return REPO_ROOT.parent / ARCHIVE_NAME


def is_archive_clone(archive: Path) -> bool:
    """True only for a git checkout whose origin is the private archive repository."""
    if not (archive / ".git").exists():
        return False
    url = _git(archive, "remote", "get-url", "origin").stdout.strip()
    # Windows clones record local origin paths with backslashes; normalize first.
    url = url.replace("\\", "/").rstrip("/").removesuffix(".git").lower()
    return url.endswith("/" + ARCHIVE_NAME)


def ensure_attributes(archive: Path) -> bool:
    """Pin the evidence tree to ``* -text`` so git never converts line endings;
    False when a conflicting .gitattributes is already there."""
    attributes = archive / ATTRIBUTES
    if attributes.exists():
        return attributes.read_bytes() == ATTRIBUTES_TEXT.encode("utf-8")
    attributes.parent.mkdir(parents=True, exist_ok=True)
    attributes.write_bytes(ATTRIBUTES_TEXT.encode("utf-8"))
    return True


def _remote_ref(archive: Path) -> str | None:
    """The clone's upstream branch, else origin/HEAD, else None."""
    ref = _git(archive, "rev-parse", "--abbrev-ref", "--symbolic-full-name",
               "@{upstream}").stdout.strip()
    if not ref and _git(archive, "rev-parse", "--verify", "-q", "origin/HEAD").returncode == 0:
        ref = "origin/HEAD"
    return ref or None


def _remote_blobs(archive: Path) -> set[str] | None:
    """Digests committed on the archive's remote-tracking branch, or None when
    the clone has no upstream to compare against."""
    ref = _remote_ref(archive)
    if ref is None:
        return None
    listed = _git(archive, "ls-tree", "-r", "--name-only", ref, "--", EVIDENCE_DIR)
    if listed.returncode != 0:
        return None
    return {Path(line).name for line in listed.stdout.splitlines() if line}


def _committed_sha256(archive: Path, ref: str, path: str) -> str | None:
    """SHA-256 of the blob as committed at ref — bytes straight from git, so no
    working-tree line-ending filter applies — or None when git cannot read it."""
    blob = subprocess.run(["git", "cat-file", "blob", f"{ref}:{path}"], cwd=str(archive),
                          check=False, capture_output=True)
    if blob.returncode != 0:
        return None
    return hashlib.sha256(blob.stdout).hexdigest()


def audit(root: Path, archive: Path, *, verify: bool = False, out=None) -> dict[str, int]:
    """Report each pin's archive state. Report-only: the counts are returned, never raised."""
    out = out or sys.stdout
    pins = collect_pins(root)
    counts = {"ARCHIVED": 0, "UNPUSHED": 0, "MISSING": 0, "CORRUPT": 0}
    if not archive.is_dir() or not is_archive_clone(archive):
        print(f"UNVERIFIED — no {ARCHIVE_NAME} clone at {archive}; pass --archive or set "
              f"FP_EVIDENCE_ARCHIVE. {len(pins)} pinned digests unchecked.", file=out)
        return counts
    ref = _remote_ref(archive)
    remote = _remote_blobs(archive)
    if remote is None:
        print(f"note: {archive} has no upstream branch; ARCHIVED cannot be told from UNPUSHED.",
              file=out)
        remote = set()
    for pin in pins:
        local = archive / blob_path(pin.digest)
        if pin.digest in remote:
            state = "ARCHIVED"
            if verify and (ref is None
                           or _committed_sha256(archive, ref, blob_path(pin.digest)) != pin.digest):
                state = "CORRUPT"
        elif local.is_file():
            state = "UNPUSHED"
            if verify and sha256_file(local) != pin.digest:
                state = "CORRUPT"
        else:
            state = "MISSING"
        counts[state] += 1
        if state != "ARCHIVED":
            present = (" (bytes present here: run put --pinned)"
                       if pin.local_path(root).is_file() else "")
            print(f"{state:9} {pin.digest[:12]}  {pin.manifest}: {pin.name}{present}", file=out)
    summary = ", ".join(f"{k} {v}" for k, v in counts.items())
    print(f"{len(pins)} pinned digests in {len(_manifests(root))} manifests: {summary}", file=out)
    return counts


def put(files: list[Path], archive: Path, root: Path, *, out=None) -> int:
    """Copy each file to its content address in the archive clone and index it."""
    out = out or sys.stdout
    if not is_archive_clone(archive):
        print(f"refused: {archive} is not a clone whose origin is {ARCHIVE_NAME}", file=sys.stderr)
        return 2
    if not ensure_attributes(archive):
        print(f"refused: {archive}/{ATTRIBUTES} exists with other content; "
              f"it must be exactly \"* -text\"", file=sys.stderr)
        return 2
    index = archive / INDEX
    index.parent.mkdir(parents=True, exist_ok=True)
    added = 0
    for source in files:
        if not source.is_file():
            print(f"skip (not a file): {source}", file=sys.stderr)
            continue
        if source.stat().st_size > MAX_BYTES:
            print(f"skip (over {MAX_BYTES // (1024 * 1024)} MB, GitHub would reject it): {source}",
                  file=sys.stderr)
            continue
        digest = sha256_file(source)
        target = archive / blob_path(digest)
        if target.is_file() and sha256_file(target) == digest:
            print(f"already archived {digest[:12]}  {source}", file=out)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        if sha256_file(target) != digest:
            target.unlink()
            print(f"refused: copy of {source} did not verify", file=sys.stderr)
            return 1
        try:
            label = source.resolve().relative_to(root).as_posix()
        except ValueError:
            label = source.name
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with index.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(f"{digest}\t{source.stat().st_size}\t{stamp}\t{label}\n")
        added += 1
        print(f"archived {digest[:12]}  {source}", file=out)
    if added:
        print("\nNot safe until pushed:\n"
              f"  git -C \"{archive}\" -c core.autocrlf=false add evidence\n"
              f"  git -C \"{archive}\" -c core.autocrlf=false commit "
              f"-m \"evidence: archive {added} file(s)\"\n"
              f"  git -C \"{archive}\" push", file=out)
    return 0


def main(argv: list[str] | None = None) -> int:
    """CLI entry point; audit always exits 0."""
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--archive", help=f"local clone of {ARCHIVE_NAME}")
    sub = parser.add_subparsers(dest="command", required=True)
    put_cmd = sub.add_parser("put", help="archive files by content address")
    put_cmd.add_argument("files", nargs="*", type=Path)
    put_cmd.add_argument("--pinned", action="store_true",
                         help="also archive every pinned file present in this checkout")
    audit_cmd = sub.add_parser("audit", help="report each pinned digest's archive state")
    audit_cmd.add_argument("--verify", action="store_true",
                           help="re-hash archived bytes (committed blobs on the remote-tracking "
                                "ref; working-tree copies for unpushed files)")
    args = parser.parse_args(argv)
    archive = resolve_archive(args.archive)
    if args.command == "audit":
        audit(REPO_ROOT, archive, verify=args.verify)
        return 0
    files = list(args.files)
    if args.pinned:
        files += [p.local_path(REPO_ROOT) for p in collect_pins(REPO_ROOT)
                  if p.local_path(REPO_ROOT).is_file()]
    if not files:
        parser.error("put needs files or --pinned")
    return put(files, archive, REPO_ROOT)


if __name__ == "__main__":
    sys.exit(main())
