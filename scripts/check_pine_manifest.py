#!/usr/bin/env python3
"""check_pine_manifest.py — verify the strategies/ hash manifests against on-disk Pine.

Covers BOTH `strategies/MANIFEST.sha256` (locked strategy source) and
`strategies/PORT_MANIFEST.sha256` (port / futures venue-edition source) with
identical semantics.

Closes M-9 for the Pine manifests specifically. `check_data_manifests.py` covers
the `data/` SHA256SUMS trees only. Membership/hash of every pinned `.pine` is
this gate's job — a `.pine` dropped from disk (or a stale entry that outlived
its file) drifts silently without it (three archived `.pine` pruned 2026-06-05;
PORT_MANIFEST recurrence 2026-07-17: striker_dj30_v4.5_mym.pine drifted from its
pin with no gate firing, and striker_nas100_v1_mnq.pine went MISSING).

PORT_MANIFEST entries may legitimately lag right after a venue-edition re-author;
hard-fail is still correct — it forces the re-pin in the same motion (M-9
doctrine: manual regen drifts silently).

LINKED-WORKTREE relaxation (2026-08-11): a `git worktree add` checkout shares
the tracked object database with the main checkout but starts with an empty
untracked/gitignored working tree — gitignored `.pine` bytes are never copied
there by git itself, on any worktree, always. Authoring even one new `.pine`
in a linked worktree used to flip the presence gate to "environment has Pine,
verify everything," hard-failing every OTHER pin whose file the worktree was
simply never given — not drift, an artifact of which checkout this is. MISSING
is now a WARN specifically when `repo_root` resolves to a linked worktree
(`git rev-parse --git-dir` != `--git-common-dir`); MISMATCH (a file present
with the wrong hash) still hard-fails everywhere, worktree or not — presence
plus a wrong hash is real signal regardless of checkout. Detection defaults to
strict main-checkout behavior when git plumbing is unavailable or `repo_root`
is not a git repository at all (this gate's own synthetic tmp-tree tests).

This is a PRESENCE-AWARE gate, not a tracked-file gate:
`**/*.pine` is gitignored, so the manifests are the only tracked artifacts and the
files they pin live only on Joshua's local disk.

  - No Pine present at all (public clone / CI / a fresh worktree) → WARN, exit 0.
    Absence is not drift; we cannot hash bytes that were never checked out.
  - Some Pine present (Joshua's local checkout) → every entry in every manifest
    MUST resolve to a file AND hash-match. MISSING (pinned file gone) / MISMATCH
    (stale pin) / parse errors → hard-fail exit 1, because the manifest is then
    asserting something false. An on-disk `*.pine` not in ANY manifest is EXTRA
    → WARN only: a coverage gap, not a lie, and hard-failing it on an always-on
    hook would block unrelated commits over a not-yet-pinned file.

The presence gate is a single environment read across the UNION of both
manifests: locked Pine on disk while a port entry points at a deleted file is a
"present" environment, so the port entry MISSING hard-fails (the 2026-07-17 MNQ
case). The partial-presence case is the M-9 catch: 8 live files present while 3
stale entries point at deleted files = "present" environment = MISSING hard-fail.

One path pinned in both manifests with two different digests cannot be true in
both — that CROSS_MANIFEST_CONFLICT is a manifest-shape lie detectable without
Pine bytes, so (like BAD_LINE / DUPLICATE) it hard-fails even on CI.

Hashes working-tree bytes via open(..., "rb"), matching how the manifest was
generated (CRLF as checked out on Windows with core.autocrlf=true) — identical
to `check_data_manifests.py`.

`--check-pin-provenance` is a SECOND, independent gate (2026-07-31) closing the
"unrecoverable pin bytes" class, which the hash check above cannot see. A pin is a
claim about bytes that only exist on one disk. If the machine that made the claim is
ephemeral, the bytes die with it and the pin becomes permanently unverifiable — while
still reading as authoritative. The hash check passes on that machine (the file IS
there, and DOES match), so nothing fires; the loss only surfaces later, on a durable
machine, as a MISSING/MISMATCH nobody can resolve.

Twice recorded in PORT_MANIFEST.sha256: striker_dj30 `fd91f37b…` ("unrecoverable pin
bytes"), and orb_mnq_v0_2 `bad8068d…` — pinned 2026-07-31 by commit 66c2a14 (PR #574),
authored by a Cursor CLOUD AGENT on a throwaway VM. Gitignored, so never pushed; the
D5 edition it pinned as the "active working edition" was gone within hours and had to
be reconstructed from its predecessor.

The gate refuses a pin ADDED for a GITIGNORED path by an ephemeral identity. Both
conditions are load-bearing: a tracked file's bytes live in git and survive any
machine, and a durable machine can always re-exhibit its own bytes. Detection is by
commit-author identity (agent/bot addresses) and CI-environment markers, so a re-pin
from Joshua's local checkout — the only place these bytes durably live — passes
untouched. Remedy is never to relax the pin: re-pin from a machine that keeps the file.

Three call sites, all three live (updated 2026-08-19, Q-GATESTACK-1 Limb-D — GitHub
Actions has run live and green since the 2026-08-15 public transition):
  - pre-commit (staged mode) — cannot see the case it was written for: a fresh
    cloud-agent clone has no hooks installed. It guards the durable machine only.
  - a pull_request job (.github/workflows/manifest-check.yml pine-pin-provenance) —
    the surface that catches a pin BEFORE the bytes are lost; confirmed executing
    and passing at job granularity, not just skipped/inert.
  - post-merge (range mode, --base ORIG_HEAD) — fires on arrival, i.e. after the
    bytes are already gone; now a backstop for what the PR job's checkout-based view
    can miss, not the only detection point. Worth having anyway: acting while the
    authoring PR is fresh is the difference between re-pinning from a source that
    still exists and reconstructing one that does not.
  None of the three block a merge — but NOT because main is unprotected. The
  `main-protection` ruleset (created 2026-08-19, Q-GATESTACK-1 closure addendum)
  requires a PR and the `skills (3.12)` check; none of these three limbs is among
  the required checks, so a red run here is advisory only.

Exit codes:
    0 — check passed (EXTRA warns), or no Pine present locally (warn-only)
    1 — a manifest lies about a file (MISSING / MISMATCH / CROSS_MANIFEST_CONFLICT
        / parse error), or (--check-pin-provenance) a gitignored pin was added from
        an environment that cannot persist the bytes
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_MANIFEST = REPO_ROOT / "core" / "strategies" / "MANIFEST.sha256"
DEFAULT_PORT_MANIFEST = REPO_ROOT / "core" / "strategies" / "PORT_MANIFEST.sha256"
DEFAULT_MANIFESTS = [DEFAULT_MANIFEST, DEFAULT_PORT_MANIFEST]

# Directories whose `*.pine` the manifest is expected to cover exhaustively.
# Scoped to the live strategy tree: a new strategy `.pine` here that is not
# pinned is a real integrity gap (the live edge unprotected). Archived `.pine`
# elsewhere are recoverable from git history and intentionally not required.
PINE_ROOTS = [REPO_ROOT / "core" / "strategies"]

# Pine manifest line: "<64 hex>  <repo-relative posix path>" (two spaces, no
# "*basename" prefix — unlike the data SHA256SUMS format). Tolerant of 1+ spaces
# and trailing CR/whitespace.
LINE_RE = re.compile(r"^([0-9a-f]{64})\s+(\S.*?)\s*$")

REGEN_HINT = (
    "Pine manifest drift. If a strategy `.pine` was intentionally added/removed/"
    "re-authored, re-pin it (regenerate the hash line) in the same change: locked "
    "strategy source in strategies/MANIFEST.sha256, port/venue editions in "
    "strategies/PORT_MANIFEST.sha256 — a post-re-author pin lag is exactly the "
    "skew this gate forces closed (M-9). If a file went missing unexpectedly, "
    "restore it before committing. Archived `.pine` are recoverable from git "
    "history (b71e4a4^)."
)


def _rel_posix(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_manifest(manifest_path: Path) -> tuple[dict[str, str], list[str]]:
    """Returns (repo-relative posix path -> hex digest, parse errors)."""
    errors: list[str] = []
    entries: dict[str, str] = {}
    if not manifest_path.is_file():
        errors.append(f"MISSING_MANIFEST {_rel_posix(manifest_path)}")
        return entries, errors
    text = manifest_path.read_text(encoding="utf-8", errors="replace")
    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = LINE_RE.match(line)
        if not m:
            errors.append(f"BAD_LINE {_rel_posix(manifest_path)}:{lineno} {line!r}")
            continue
        digest, name = m.group(1), m.group(2)
        if name in entries:
            errors.append(f"DUPLICATE {_rel_posix(manifest_path)} path={name!r}")
            continue
        entries[name] = digest
    return entries, errors


def _is_linked_worktree(repo_root: Path) -> bool:
    """True when `repo_root` is a linked `git worktree`, not the main checkout.

    A linked worktree's `.git` is a file pointing back at the shared repo's
    `.git/worktrees/<name>` dir, so `--git-dir` (the worktree-private admin
    dir) and `--git-common-dir` (the shared repo root's `.git`) resolve to
    different paths there and identical paths in the main checkout. Gitignored
    files are never synced by either — only tracked history is shared — so
    this is a mechanical, non-spoofable read of "which kind of checkout is
    this," not a self-reported flag.

    Defaults to False (main-checkout-strict: MISSING stays a hard fail) when
    git plumbing errors or `repo_root` isn't a git repository at all — e.g.
    this gate's own synthetic tmp-tree tests, which must keep exercising the
    strict M-9 partial-presence hard-fail unchanged.
    """
    try:
        git_dir = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
        common_dir = subprocess.run(
            ["git", "rev-parse", "--git-common-dir"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
        if git_dir.returncode != 0 or common_dir.returncode != 0:
            return False
        gd = Path(git_dir.stdout.strip())
        cd = Path(common_dir.stdout.strip())
        gd_abs = (gd if gd.is_absolute() else repo_root / gd).resolve()
        cd_abs = (cd if cd.is_absolute() else repo_root / cd).resolve()
        return gd_abs != cd_abs
    except OSError:
        return False


def scan_pine(pine_roots: list[Path], repo_root: Path = REPO_ROOT) -> set[str]:
    """repo-relative posix paths of every *.pine under the covered roots."""
    found: set[str] = set()
    for root in pine_roots:
        if not root.is_dir():
            continue
        for p in root.rglob("*.pine"):
            if p.is_file():
                found.add(p.relative_to(repo_root).as_posix())
    return found


class CheckResult:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.warnings: list[str] = []

    @property
    def ok(self) -> bool:
        return not self.failures


def check(
    manifest_paths: list[Path] | None = None,
    repo_root: Path = REPO_ROOT,
    pine_roots: list[Path] | None = None,
    is_linked_worktree: bool | None = None,
) -> CheckResult:
    if manifest_paths is None:
        manifest_paths = DEFAULT_MANIFESTS
    if pine_roots is None:
        pine_roots = PINE_ROOTS
    if is_linked_worktree is None:
        is_linked_worktree = _is_linked_worktree(repo_root)
    result = CheckResult()

    parsed: list[tuple[Path, dict[str, str]]] = []
    for manifest_path in manifest_paths:
        entries, parse_errs = parse_manifest(manifest_path)
        result.failures.extend(parse_errs)
        parsed.append((manifest_path, entries))
    if result.failures:
        # A malformed/missing manifest is always a hard fail; don't try to
        # reason about disk state on top of a manifest we couldn't read.
        return result

    # One path pinned under two different digests cannot be true in both
    # manifests — a manifest-shape lie, checkable without Pine bytes, so it
    # fails in every environment (same class as BAD_LINE / DUPLICATE).
    pin_owner: dict[str, tuple[str, str]] = {}
    for manifest_path, entries in parsed:
        for rel, digest in entries.items():
            prior = pin_owner.setdefault(rel, (manifest_path.name, digest))
            if prior[1] != digest:
                result.failures.append(
                    f"CROSS_MANIFEST_CONFLICT {rel} {prior[0]}={prior[1][:8]}... "
                    f"{manifest_path.name}={digest[:8]}..."
                )
    if result.failures:
        return result

    on_disk = scan_pine(pine_roots, repo_root)
    resolved = {rel for rel in pin_owner if (repo_root / rel).is_file()}

    # Presence gate — one environment read across the UNION of all manifests:
    # if nothing maps to a real file AND no *.pine is on disk, this is a
    # clone / CI / bare worktree. Absence is not drift. Conversely, ANY Pine on
    # disk makes this a "present" environment for every manifest, so a port
    # entry whose file is gone hard-fails even while the locked set is intact.
    if not resolved and not on_disk:
        result.warnings.append(
            "no Pine source present locally (public clone / CI / bare worktree) "
            "- manifests not verified against disk"
        )
        return result

    # Present environment: full verification.
    #
    # MISSING / MISMATCH are HARD: the manifest asserts something false about a
    # file (the M-9 silent-drift class — a pinned entry whose file was dropped,
    # or an edited file whose pin is stale). EXTRA is a WARN: an on-disk .pine
    # that isn't pinned yet is a coverage gap, not a lie — and because this gate
    # is always-on, hard-failing EXTRA would block every unrelated commit while a
    # new/in-progress strategy file sits unpinned, inviting --no-verify.
    #
    # MISSING is downgraded to a WARN specifically in a linked worktree: git
    # never copies gitignored bytes there, so a pin the main checkout satisfies
    # is an expected absence, not drift. MISMATCH stays hard in every
    # environment — the file IS present with the wrong hash, which is real
    # regardless of which checkout found it.
    hashed: dict[str, str] = {}
    for manifest_path, entries in parsed:
        for rel in sorted(entries):
            if rel not in resolved:
                msg = f"MISSING {rel} (pinned in {manifest_path.name}, not on disk)"
                if is_linked_worktree:
                    result.warnings.append(
                        f"{msg} — linked worktree: gitignored bytes are never "
                        "copied to a linked checkout; not treated as drift here"
                    )
                else:
                    result.failures.append(msg)
                continue
            got = hashed.setdefault(rel, hash_file(repo_root / rel))
            exp = entries[rel]
            if got != exp:
                result.failures.append(
                    f"MISMATCH {rel} {manifest_path.name}={exp[:8]}... ondisk={got[:8]}..."
                )

    for rel in sorted(on_disk - set(pin_owner)):
        result.warnings.append(f"EXTRA {rel} (on disk, not pinned in any manifest)")

    return result


# Identities that commit from disposable filesystems. A `.pine` authored under one
# of these is gone as soon as the run ends, so a hash pinned there can never be
# re-exhibited. cursoragent@cursor.com is the identity that landed bad8068d….
EPHEMERAL_AUTHOR_EMAILS = frozenset(
    {
        "cursoragent@cursor.com",
        "actions@github.com",
        "github-actions@github.com",
        "github-actions[bot]@users.noreply.github.com",
        "noreply@github.com",
    }
)

# Environment markers for a disposable checkout, used in staged mode where no commit
# object exists yet to read an author from.
#
# Deliberately NOT including CURSOR_AGENT: a *local* Cursor agent session sets it while
# running on Joshua's durable disk, so it flags the one environment where re-pinning is
# correct (caught in testing 2026-07-31 — the first run of this gate failed its own
# author's legitimate re-pin). Cloud agents are disposable but commit as
# cursoragent@cursor.com, so identity catches them without the false positive; that is
# also the discriminator the real bad8068d… incident is on record for.
EPHEMERAL_ENV_VARS = ("CI", "GITHUB_ACTIONS")

PIN_PROVENANCE_HINT = (
    "Unrecoverable pin bytes. A `.pine` pin is a claim about bytes that live on exactly "
    "one disk; `**/*.pine` is gitignored, so the file is NOT in this commit. Pinned from "
    "a disposable checkout, the bytes vanish with the runner and the manifest is left "
    "asserting an 'active working edition' nobody can ever produce — this already "
    "happened twice (fd91f37b…, bad8068d…). Re-pin from the durable machine that keeps "
    "the file, in a commit authored by that machine. Do NOT weaken or delete the pin to "
    "clear this gate."
)


def _git(args: list[str], repo_root: Path) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    ).stdout


def _is_gitignored(rel: str, repo_root: Path) -> bool:
    """True when the pinned path is gitignored, i.e. its bytes are not in the commit."""
    return (
        subprocess.run(
            ["git", "check-ignore", "-q", "--", rel],
            cwd=repo_root,
            capture_output=True,
            check=False,
        ).returncode
        == 0
    )


def _added_pins(diff_text: str) -> list[tuple[str, str]]:
    """(digest, path) for pin lines ADDED by a diff. Ignores comments and removals."""
    added: list[tuple[str, str]] = []
    for raw in diff_text.splitlines():
        if not raw.startswith("+") or raw.startswith("+++"):
            continue
        line = raw[1:].strip()
        if not line or line.startswith("#"):
            continue
        m = LINE_RE.match(line)
        if m:
            added.append((m.group(1), m.group(2)))
    return added


def check_pin_provenance(
    base: str | None = None,
    repo_root: Path = REPO_ROOT,
    manifest_paths: list[Path] | None = None,
) -> CheckResult:
    """Refuse gitignored pins added where the bytes cannot survive.

    base=None  → staged mode (pre-commit): judge the current environment/identity.
    base=<ref> → range mode (CI): judge each commit in base..HEAD by its own author,
                 so one bad commit is caught even if later ones are fine.
    """
    if manifest_paths is None:
        manifest_paths = DEFAULT_MANIFESTS
    result = CheckResult()
    rel_manifests = [_rel_posix(p) for p in manifest_paths]

    def flag(digest: str, rel: str, who: str, where: str) -> None:
        if not _is_gitignored(rel, repo_root):
            return  # tracked: bytes travel with the commit, nothing to lose
        result.failures.append(
            f"EPHEMERAL_PIN {rel}={digest[:8]}... added by {who} in {where}"
        )

    if base:
        log = _git(
            ["log", "--format=%H%x1f%ae", f"{base}..HEAD", "--", *rel_manifests],
            repo_root,
        )
        for entry in log.splitlines():
            if "\x1f" not in entry:
                continue
            sha, email = entry.split("\x1f", 1)
            if email.strip().lower() not in EPHEMERAL_AUTHOR_EMAILS:
                continue
            diff = _git(["show", "-U0", "--format=", sha, "--", *rel_manifests], repo_root)
            for digest, rel in _added_pins(diff):
                flag(digest, rel, email.strip(), f"commit {sha[:8]}")
        return result

    diff = _git(["diff", "--cached", "-U0", "--", *rel_manifests], repo_root)
    pins = _added_pins(diff)
    if not pins:
        return result

    email = _git(["config", "user.email"], repo_root).strip().lower()
    env_hits = [v for v in EPHEMERAL_ENV_VARS if os.environ.get(v)]
    if email in EPHEMERAL_AUTHOR_EMAILS:
        where = f"user.email={email}"
    elif env_hits:
        where = f"environment {'+'.join(env_hits)} set"
    else:
        return result
    for digest, rel in pins:
        flag(digest, rel, email or "unknown", where)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify strategies/MANIFEST.sha256 + strategies/PORT_MANIFEST.sha256 "
            "against on-disk Pine source."
        ),
    )
    parser.add_argument(
        "--check-pin-provenance",
        action="store_true",
        help=(
            "Instead of hashing, refuse gitignored pins ADDED from an environment "
            "that cannot persist the bytes (staged changes, or --base REF..HEAD)."
        ),
    )
    parser.add_argument(
        "--base",
        default=None,
        help="Base ref for --check-pin-provenance range mode (e.g. origin/main).",
    )
    args = parser.parse_args(argv)

    if args.check_pin_provenance:
        result = check_pin_provenance(base=args.base)
        for f in result.failures:
            print(f, file=sys.stderr)
        if not result.ok:
            print(PIN_PROVENANCE_HINT, file=sys.stderr)
            return 1
        return 0

    result = check()
    for w in result.warnings:
        print(f"WARN {w}", file=sys.stderr)
    for f in result.failures:
        print(f, file=sys.stderr)
    if not result.ok:
        print(REGEN_HINT, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
