"""FTS5-as-Delete falsifier v3 -- executes the frozen v3 pre-registration.

docs/briefs/pre-registration/2026-08-15-fts5-delete-falsifier-prereg-v3.md

Fixture construction is reused verbatim from v2 (frozen; ported unmodified
from the pruned harness at
git show pre-prune-2026-08-08:lab/analysis/harvest/fts5_delete_falsifier_2026-07-27/falsifier_v2.py).

The retrieval side is NOT reimplemented: this script imports
scripts/repo_retrieve.py and calls its own rebuild()/query() functions
directly, so the number measured is the number the shipped artifact
actually produces (the "measured = shipped" binding clause in the v3
pre-registration). Contains no discretion of its own beyond that binding.

Usage: python remeasure.py <repo_root>
"""
from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(sys.argv[1]).resolve()

K = 5                     # frozen
MIN_PAIRS = 15            # frozen
RECALL_FLOOR = 0.70       # frozen, carried verbatim from v1/v2

SESSIONS = REPO / "docs" / "SESSIONS.md"

LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
QID = re.compile(r"\bQ-[A-Z0-9-]+\b")
FILENAME = re.compile(r"\b[\w.-]+\.(?:md|py|json|csv|pine|toml)\b", re.I)
SLUGGY = re.compile(r"\b[\w]*[_/][\w/_.-]*\b")
NONWORD = re.compile(r"[^a-z0-9\s]+")


def strip_identifiers(text: str) -> str:
    t = text.replace("`", " ")
    for rx in (DATE, QID, FILENAME, SLUGGY):
        t = rx.sub(" ", t)
    return " ".join(NONWORD.sub(" ", t.lower()).split())


def normalise(text: str) -> str:
    return " ".join(NONWORD.sub(" ", text.lower()).split())


def is_sessions_family(p: Path) -> bool:
    """Frozen exclusion: queries come from this corpus; archives copy it verbatim."""
    return p.name.startswith("SESSIONS")


def build_fixture():
    """Frozen rules 1-6 (v2, reused verbatim)."""
    text = SESSIONS.read_text(encoding="utf-8", errors="replace")
    pairs, dropped_verbatim = [], 0
    for blk in re.split(r"^##\s+", text, flags=re.M)[1:]:
        head, _, body = blk.partition("\n")
        query = strip_identifiers(head)
        if len(query.split()) < 3:                                  # rule 4
            continue
        target = None
        for _txt, href in LINK.findall(body):                       # rule 3: FIRST
            cand = SESSIONS.parent / href.split("#")[0]
            try:
                cand = cand.resolve()
            except OSError:
                continue
            if cand.exists() and cand.suffix == ".md" and not is_sessions_family(cand):
                target = cand
                break
        if target is None:
            continue
        if query in normalise(target.read_text(encoding="utf-8", errors="replace")):
            dropped_verbatim += 1                                   # rule 5
            continue
        pairs.append((query, target))                               # rule 6: keep all
    return pairs, dropped_verbatim


def load_corpus():
    """rg baseline's own (wider) corpus -- frozen, reused verbatim from v2."""
    docs = []
    for p in sorted(REPO.rglob("*.md")):
        if ".git" in p.parts or is_sessions_family(p):
            continue
        try:
            docs.append((p, p.read_text(encoding="utf-8", errors="replace")))
        except OSError:
            pass
    return docs


def terms_of(query: str) -> list[str]:
    """Frozen engine parity: identical term list to both engines."""
    return [t for t in query.split() if len(t) > 2]


def rg_topk(docs, query, k):
    terms = terms_of(query)
    if not terms:
        return []
    rx = re.compile("|".join(re.escape(t) for t in terms), re.I)
    scored = [(len(rx.findall(body)), path) for path, body in docs]
    scored = [(n, p) for n, p in scored if n]
    scored.sort(key=lambda x: (-x[0], str(x[1])))
    return [p for _, p in scored[:k]]


def load_repo_retrieve():
    """Import the SHIPPED scripts/repo_retrieve.py -- not a reimplementation."""
    path = REPO / "scripts" / "repo_retrieve.py"
    spec = importlib.util.spec_from_file_location("repo_retrieve_shipped", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod, path


def reachability_ceiling(fixture, rr, db_path) -> tuple[int, int]:
    """What fraction of fixture targets appear anywhere in the shipped corpus,
    independent of ranking or query matching. Diagnostic for the one-revision
    cap -- computed before any query-level recall number."""
    chunks = rr.collect_chunks(REPO)
    reachable_paths = {(REPO / c["path"]).resolve() for c in chunks}
    n_reach = sum(1 for _q, exp in fixture if exp.resolve() in reachable_paths)
    return n_reach, len(fixture)


def main() -> None:
    fixture, dropped = build_fixture()
    n = len(fixture)
    print(f"fixture pairs: {n}   (verbatim-confound drops: {dropped})")
    if n < MIN_PAIRS:
        print(f"\nVERDICT: AMBIGUOUS (N={n} < {MIN_PAIRS})")
        return

    rr, rr_path = load_repo_retrieve()
    # Shell out to git itself for the blob hash -- do not reimplement it.
    # A hand-rolled sha1("blob <len>\0<bytes>") over raw working-tree bytes
    # disagrees with git's own hash-object under core.autocrlf=true (git
    # LF-normalizes before hashing; raw disk bytes here are CRLF). Caught
    # this by cross-checking against `git rev-parse <commit>:<path>` when
    # freezing this artifact -- the two didn't match. Calling git directly
    # is the fix, not correcting the normalization by hand.
    try:
        out = subprocess.run(
            ["git", "hash-object", str(rr_path)],
            cwd=REPO, capture_output=True, text=True, timeout=5, check=False,
        )
        blob_hash = out.stdout.strip() if out.returncode == 0 else "<git hash-object failed>"
    except (OSError, subprocess.TimeoutExpired):
        blob_hash = "<git unavailable>"
    print(f"scripts/repo_retrieve.py blob hash (this run, via git hash-object): {blob_hash}")

    n_reach, n_total = reachability_ceiling(fixture, rr, None)
    print(f"reachability ceiling (corpus contains target, any rank): "
          f"{n_reach}/{n_total} = {n_reach / n_total:.3f}")

    docs = load_corpus()
    print(f"rg baseline corpus (SESSIONS family excluded): {len(docs)} docs")

    db = REPO.parent / "_remeasure_tmp.sqlite"
    if db.exists():
        db.unlink()
    rr.rebuild(REPO, db)

    hits_shipped = hits_rg = 0
    misses = []
    for query, expected in fixture:
        hits = rr.query(db, query, limit=K)
        hit_paths = {(REPO / p).resolve() for p, _h, _s in hits}
        ok_shipped = expected.resolve() in hit_paths
        ok_rg = expected in rg_topk(docs, query, K)
        hits_shipped += ok_shipped
        hits_rg += ok_rg
        if not ok_shipped:
            misses.append((query[:56], expected.name[:40]))

    db.unlink(missing_ok=True)

    r_shipped, r_rg = hits_shipped / n, hits_rg / n
    print(f"\nN={n}  k={K}")
    print(f"R_shipped@{K} = {r_shipped:.3f}  ({hits_shipped}/{n})")
    print(f"R_rg@{K}      = {r_rg:.3f}  ({hits_rg}/{n})")

    floor_ok = r_shipped >= RECALL_FLOOR
    beats_rg = r_shipped > r_rg
    print(f"\nlimb 1  R_shipped >= {RECALL_FLOOR:.2f} : {'PASS' if floor_ok else 'FAIL'}")
    print(f"limb 2  R_shipped >  R_rg       : {'PASS' if beats_rg else 'FAIL'}")

    if floor_ok and beats_rg:
        verdict = "REAUTHORIZE"
    elif beats_rg:
        verdict = "ASSISTIVE-ONLY"
    else:
        verdict = "WITHDRAW"
    print(f"\nVERDICT: {verdict}")

    if misses:
        print(f"\nRepo_retrieve misses ({len(misses)}), first 12:")
        for q, e in misses[:12]:
            print(f"  {q:<58} -> {e}")


if __name__ == "__main__":
    main()
