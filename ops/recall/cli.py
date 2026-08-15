"""Command surface for the recall sidecar.

    python -m ops.recall build              # (re)index the markdown corpus
    python -m ops.recall search "<query>"   # verbatim FTS5 search, incl. cold store
    python -m ops.recall add "<note>"       # stage a note (Rule-7 guarded)
    python -m ops.recall notes              # list staged notes

Frozen scope: search + staged write. No summarisation subcommand — that path
re-creates the retired weekly_review_feeder.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ops.recall import index as rindex

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DB = REPO_ROOT / "ops" / "data" / "recall.db"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="ops.recall", description=__doc__)
    ap.add_argument("--db", default=str(DEFAULT_DB))
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build")
    sub.add_parser("notes")
    p_search = sub.add_parser("search")
    p_search.add_argument("query", nargs="+")
    # --limit lives on the subparser so `search <q> --limit 3` works; on the
    # top-level parser argparse only accepts it BEFORE the subcommand.
    p_search.add_argument("--limit", type=int, default=10)
    sub.add_parser("add").add_argument("note", nargs="+")
    args = ap.parse_args(argv)

    db_path = Path(args.db)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = rindex.open_db(db_path)

    if args.cmd == "build":
        n = rindex.build(conn, REPO_ROOT)
        print(f"indexed {n} markdown documents (cold store included) -> {db_path}")
        return 0

    if args.cmd == "search":
        hits = rindex.search(conn, " ".join(args.query), limit=args.limit)
        if not hits:
            print("no hits")
            return 1
        if all(h.weak for h in hits):
            print("NOTE: no strong match — every hit below covers less than half\n"
                  "      the query. Likely nothing here is about this.\n")
        for h in hits:
            flag = "  [weak]" if h.weak else ""
            print(f"{h.path}  ({h.matched_terms}/{h.query_terms} terms){flag}"
                  f"\n    {h.snippet}")
        return 0

    if args.cmd == "add":
        v = rindex.stage_note(conn, " ".join(args.note), repo_root=REPO_ROOT)
        if not v.ok:
            print(f"REFUSED: {v.reason}", file=sys.stderr)
            return 1
        print("staged for review")
        return 0

    if args.cmd == "notes":
        notes = rindex.staged_notes(conn)
        if not notes:
            print("no staged notes")
        for n in notes:
            print(f"[{n.id}] {n.created}  {n.text}")
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
