#!/usr/bin/env python3
"""Run a command and retain source-bound evidence without hiding a failed run."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import xml.etree.ElementTree as ET


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])


def snapshot(repo):
    paths = set(git(repo, 'ls-files', '-z', '--cached', '--others', '--exclude-standard')
                .decode('utf-8').rstrip('\0').split('\0')) - {''}
    files = {}
    for relative in sorted(paths):
        path = repo / relative
        if path.is_symlink():
            files[relative] = 'symlink:' + digest(os.readlink(path).encode())
        elif path.is_file():
            files[relative] = digest(path.read_bytes())
        elif not path.exists():
            files[relative] = 'deleted'
        else:
            raise ValueError(f'Unsupported source entry: {relative}')
    return {'commit': git(repo, 'rev-parse', 'HEAD').decode().strip(),
            'status': git(repo, 'status', '--porcelain=v1', '--untracked-files=all').decode(),
            'diff_sha256': digest(git(repo, 'diff', '--binary', 'HEAD')),
            'fingerprint': digest(json.dumps(files, sort_keys=True).encode()),
            'lock_sha256': files.get('requirements-ops.lock'), 'files': files}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--metadata', type=Path)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    repo, output = args.repo.resolve(), args.output.resolve()
    if output.is_relative_to(repo):
        parser.error('Evidence output must be outside the measured source tree')
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    if not command:
        parser.error('A command is required after --')
    if output.exists():
        parser.error('Use a new output directory; prior evidence is never overwritten')
    before = snapshot(repo)
    metadata = json.loads(args.metadata.read_text(encoding='utf-8-sig')) if args.metadata else {}
    output.mkdir(parents=True)
    started = datetime.now(timezone.utc).isoformat()
    error = None
    with (output / 'stdout.txt').open('wb') as stdout, (output / 'stderr.txt').open('wb') as stderr:
        try:
            result = subprocess.run(command, cwd=repo, stdout=stdout, stderr=stderr, check=False)
            code = result.returncode
        except OSError as exc:
            code, error = 127, str(exc)
            stderr.write(error.encode())
    after = snapshot(repo)
    stable = before == after
    junit = []
    for report in sorted(output.glob('*.xml')):
        try:
            root = ET.parse(report).getroot()
            suites = [root] if root.tag == 'testsuite' else list(root.findall('testsuite'))
            junit.append({'file': report.name, 'suites': [dict(s.attrib) for s in suites]})
        except ET.ParseError as exc:
            junit.append({'file': report.name, 'parse_error': str(exc)})
    record = {'schema_version': 1, 'started_at': started,
              'finished_at': datetime.now(timezone.utc).isoformat(),
              'source_root': str(repo), 'before': before, 'after': after,
              'source_stable': stable, 'command': command, 'exit_code': code,
              'launch_error': error, 'recorder_python': sys.version,
              'recorder_platform': platform.platform(), 'metadata': metadata,
              'junit': junit,
              'artifacts': {p.name: digest(p.read_bytes()) for p in sorted(output.iterdir()) if p.is_file()}}
    (output / 'record.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'exit_code': code, 'source_stable': stable, 'record': str(output / 'record.json')}))
    return code if code else (0 if stable else 3)


if __name__ == '__main__':
    raise SystemExit(main())
