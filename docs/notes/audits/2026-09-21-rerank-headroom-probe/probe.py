#!/usr/bin/env python3
"""EXPLORATORY, READ-ONLY reranker-headroom probe (2026-09-21).

NOT a Limb B Run C. Revises no verdict, edits no indexed code, writes only
into its own directory. The frozen v3 pre-registration's ASSISTIVE-ONLY
result and its one-revision cap are untouched by this file.

Question
--------
A reranker (Jev or any other) can only REORDER candidates that first-stage
retrieval already returned. Therefore recall@N of the shipped engine is the
ORACLE CEILING for a perfect reranker given shortlist depth N. Measuring that
curve costs nothing and bounds every possible reranker before any spend.

Fixture
-------
RECONSTRUCTED from the v3 pre-registration's written six-step rule; the
byte-identical harness (falsifier_v2.build_fixture) is archived out of this
clone and could not be retrieved. Absolute recall here is therefore NOT
comparable to the frozen R@5 = 0.500 -- this probe sits at a different, harsher
operating point. The curve SHAPE, read against this probe's own R@5, is the
finding.

Run:  python docs/notes/audits/2026-09-21-rerank-headroom-probe/probe.py
"""
from __future__ import annotations

import json
import re
import statistics as st
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "scripts"))
import repo_retrieve as rr  # noqa: E402  (shipped engine, called not reimplemented)

LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b|\b\d{4}-\d{2}\b")
QID = re.compile(r"\bQ-[A-Z0-9]+(?:-\d+)?\b", re.I)
FILENAME = re.compile(r"\b[\w./-]+\.(?:md|py|json|yml|yaml|ps1|toml)\b", re.I)
SLUGGY = re.compile(r"\b\w+(?:-\w+){2,}\b")
NONWORD = re.compile(r"[^\w\s]+")

DEPTHS = (1, 3, 5, 10, 12, 20, 50, 100, 200, 593)
JEV_REQUEST_TOKEN_LIMIT = 64_000  # docs.typesafe.ai/models, retained claim


def strip_identifiers(s: str) -> str:
    s = LINK.sub(r" \1 ", s)
    for pat in (DATE, QID, FILENAME, SLUGGY):
        s = pat.sub(" ", s)
    return " ".join(NONWORD.sub(" ", s).split())


def is_sessions_family(rel: str) -> bool:
    return "SESSIONS" in Path(rel).name.upper()


def build_fixture() -> tuple[list[tuple[str, str]], dict]:
    text = (REPO / "docs/SESSIONS.md").read_text(encoding="utf-8", errors="replace")
    entries, cur, buf = [], None, []
    for line in text.splitlines():
        if line.startswith("## "):
            if cur is not None:
                entries.append((cur, "\n".join(buf)))
            cur, buf = line[3:].strip(), []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        entries.append((cur, "\n".join(buf)))

    pairs, drops = [], {"short_query": 0, "no_resolvable_link": 0, "verbatim_confound": 0}
    for heading, body in entries:
        q = strip_identifiers(heading)
        if len(q.split()) < 3:
            drops["short_query"] += 1
            continue
        target = None
        for _label, href in LINK.findall(body):
            href = href.split("#")[0].strip()
            if not href.endswith(".md") or href.startswith(("http://", "https://")):
                continue
            for base in (REPO / "docs", REPO):
                cand = (base / href).resolve()
                if cand.is_file() and REPO in cand.parents:
                    rel = cand.relative_to(REPO).as_posix()
                    if not is_sessions_family(rel):
                        target = rel
                    break
            if target:
                break
        if target is None:
            drops["no_resolvable_link"] += 1
            continue
        body_text = " ".join((REPO / target).read_text(encoding="utf-8", errors="replace").split())
        if q.lower() in body_text.lower():
            drops["verbatim_confound"] += 1
            continue
        pairs.append((q, target))
    drops["entries_scanned"] = len(entries)
    return pairs, drops


def first_rank(db: Path, q: str, target: str, limit: int) -> int | None:
    seen: list[str] = []
    for path, _h, _s in rr.query(db, q, limit=limit):
        if path not in seen:
            seen.append(path)
        if path == target:
            return len(seen)
    return None


def main() -> int:
    pairs, drops = build_fixture()
    if len(pairs) < 15:
        print(f"AMBIGUOUS: {len(pairs)} pairs < MIN_PAIRS=15")
        return 1

    db = Path(tempfile.mkdtemp()) / "probe.sqlite"
    n_chunks = rr.rebuild(REPO, db)
    chunks = rr.collect_chunks(REPO)
    corpus_paths = {c["path"] for c in chunks}
    avg_chunk_tok = st.mean(len(c["text"]) for c in chunks) / 4

    reachable = [(q, t) for q, t in pairs if t in corpus_paths]
    ranks_all = [first_rank(db, q, t, max(DEPTHS)) for q, t in pairs]
    ranks_reach = [first_rank(db, q, t, max(DEPTHS)) for q, t in reachable]

    def curve(ranks: list[int | None]) -> dict:
        n = len(ranks)
        base = sum(1 for r in ranks if r and r <= 5) / n
        return {
            str(d): {
                "recall": round(sum(1 for r in ranks if r and r <= d) / n, 4),
                "oracle_gain_vs_depth5": round(sum(1 for r in ranks if r and r <= d) / n - base, 4),
                "rerank_input_tokens_per_query": int(min(d, n_chunks) * avg_chunk_tok),
                "fits_one_jev_request": int(min(d, n_chunks) * avg_chunk_tok) <= JEV_REQUEST_TOKEN_LIMIT,
            }
            for d in DEPTHS
        }

    indexed_chars = sum(len(c["text"]) for c in chunks)
    full_chars = sum(
        len((REPO / p).read_text(encoding="utf-8", errors="replace"))
        for p in corpus_paths if (REPO / p).is_file()
    )

    out = {
        "kind": "exploratory_readonly_probe",
        "not_a_run_c": True,
        "revises_no_verdict": True,
        "date": "2026-09-21",
        "repo_head": rr._git_head(REPO),
        "repo_retrieve_blob": "a6fc6ba4e4e25d1a62d68256d2b0fe37543f2f14",
        "fixture": {
            "source": "reconstructed from v3 prereg six-step rule; archived harness unavailable",
            "comparable_to_frozen_R5_0.500": False,
            "pairs": len(pairs), "reachable_pairs": len(reachable), "drops": drops,
        },
        "corpus": {
            "chunks": n_chunks, "distinct_paths": len(corpus_paths),
            "indexed_chars": indexed_chars, "full_chars_of_same_files": full_chars,
            "indexed_fraction_of_own_files": round(indexed_chars / full_chars, 4),
        },
        "reachability": round(len(reachable) / len(pairs), 4),
        "oracle_ceiling_all_pairs": curve(ranks_all),
        "oracle_ceiling_reachable_only": curve(ranks_reach),
        "never_retrieved_at_any_depth": round(
            sum(1 for r in ranks_all if r is None) / len(pairs), 4),
    }
    (HERE / "results.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
