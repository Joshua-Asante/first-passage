"""JSON CLI for explicit source capture, reviewed records and correction queries."""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

from .model import EvidenceError
from .store import Store, _unique_object


def _object(path):
    data = json.loads(Path(path).read_text(encoding='utf-8-sig'), object_pairs_hook=_unique_object)
    if not isinstance(data, dict):
        raise EvidenceError('annotation file must contain a JSON object')
    return data


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path.cwd())
    parser.add_argument('--store', type=Path, help='durable local store; defaults to REPO/.evidence')
    commands = parser.add_subparsers(dest='command', required=True)
    capture = commands.add_parser('capture', help='preserve one explicitly named source')
    capture.add_argument('source_id')
    capture.add_argument('path')
    capture.add_argument('--kind', default='document')
    capture.add_argument('--commit', help='full local Git commit SHA-1; never fetches')
    for name in ('record', 'depend', 'retrieve', 'use', 'assess'):
        commands.add_parser(name).add_argument('file', type=Path)
    for name in ('source', 'impact', 'receipt'):
        commands.add_parser(name).add_argument('id')
    decision = commands.add_parser('decision')
    decision.add_argument('record_id')
    decision.add_argument('--known-at', help='timezone-aware recorded-time cutoff')
    decision.add_argument('--as-of', help='timezone-aware effective-time cutoff')
    belief = commands.add_parser('belief', help='read a belief assessment with current checks')
    belief.add_argument('record_id')
    belief.add_argument('--context', type=Path, help='JSON object containing situation fields')
    belief.add_argument('--known-at')
    belief.add_argument('--as-of')
    for name in ('check', 'rebuild', 'export'):
        commands.add_parser(name)
    args = parser.parse_args(argv)
    try:
        store = Store(args.repo, args.store or args.repo / '.evidence')
        if args.command == 'capture':
            result = store.capture(args.source_id, args.path, args.kind, commit=args.commit)
        elif args.command in {'record', 'depend', 'retrieve', 'use', 'assess'}:
            result = getattr(store, args.command)(**_object(args.file))
        elif args.command in {'source', 'impact', 'receipt'}:
            result = getattr(store, args.command)(args.id)
        elif args.command == 'decision':
            result = store.decision(args.record_id, known_at=args.known_at, as_of=args.as_of)
        elif args.command == 'belief':
            result = store.belief(args.record_id, context=_object(args.context) if args.context else None,
                                  known_at=args.known_at, as_of=args.as_of)
        else:
            result = getattr(store, args.command)()
        print(json.dumps(result, sort_keys=True, ensure_ascii=True, allow_nan=False))
        return 0
    except (EvidenceError, OSError, ValueError, TypeError, sqlite3.Error) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=True), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
