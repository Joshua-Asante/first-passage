"""One-shot collection CLI. Output contains no private response bodies."""
import argparse
import json
from pathlib import Path
import sqlite3
import sys

from .collector import collect
from .journal import Journal
from .transport import ReadClient


def main(argv=None):
    parser = argparse.ArgumentParser(description='Collect observations; E1–E3 always remain unproven.')
    parser.add_argument('--config', required=True, help='Local rail JSON; credential is read in memory')
    parser.add_argument('--journal', default='.crosstrade-observer/observations.sqlite3')
    parser.add_argument('--limit', type=int, default=500)
    parser.add_argument('--max-pages', type=int, default=10)
    args = parser.parse_args(argv)
    try:
        config = json.loads(Path(args.config).read_text(encoding='utf-8-sig'))
        if not isinstance(config, dict) or config.get('destination') != 'tradovate':
            raise ValueError('wrong destination')
        account = config['account']
        client = ReadClient(config['secret_key'])
        path = Path(args.journal)
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        with Journal(path, account) as journal:
            result = collect(client, journal, account, limit=args.limit, max_pages=args.max_pages)
        print(json.dumps(result, sort_keys=True))
        return 0 if result['state'] == 'collected' else 2
    except (OSError, ValueError, KeyError, TypeError, sqlite3.Error):
        print('Observer failed; check local config, journal and arguments. No recovery authority granted.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
