#!/usr/bin/env python3
"""Offline Linux verification with durable setup evidence and owned cleanup."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('docker_recorder', ROOT / 'scripts/record_verification.py')
recorder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(recorder)
RunRecord = recorder.RunRecord
IMAGE = 'first-passage-verification:py311'
LABEL = 'fp.verification.run'
DEFAULT_TESTS = [f'tests/ops/{name}.py' for name in (
    'test_book_takeover_phases', 'test_book_account_owner', 'test_four_leg_runtime',
    'test_book_close_reconciliation', 'test_book_close_review_edges',
    'test_book_runtime_chronology', 'test_book_runtime_close_feedback')]
DEFAULT_TESTS += ['tests/test_record_verification.py', 'tests/sequence_verification/book_event_sequences.py']

RUNTIME_PROBE = r'''
import json,sys,platform,re,hashlib,importlib.metadata as m
lock=open('/build/requirements-ops.lock','rb').read()
extra=open('/build/requirements-extra.txt','rb').read()
requirements=re.findall(r'^([\w.-]+)==([^\s\\]+)',lock.decode(),re.M)
errors=[n for n,v in requirements if m.version(n)!=v]
print(json.dumps(dict(python=sys.version,platform=platform.platform(),
    packages={d.metadata['Name']:d.version for d in m.distributions()},
    locked_count=len(requirements),lock_mismatches=errors,
    lock_sha256=hashlib.sha256(lock).hexdigest(),extra_sha256=hashlib.sha256(extra).hexdigest())))
sys.exit(bool(errors) or not requirements)
'''


def find_docker(explicit):
    candidate = explicit or shutil.which('docker')
    if not candidate and os.environ.get('LOCALAPPDATA'):
        candidate = str(Path(os.environ['LOCALAPPDATA']) / 'Programs/DockerDesktop/resources/bin/docker.exe')
    if not candidate or not Path(candidate).is_file():
        raise ValueError('Docker CLI not found; install/start Docker Desktop or put docker on PATH')
    return candidate


class DockerOwner:
    def __init__(self, record, docker):
        self.record, self.docker = record, docker
        self.identity = record.data['run_id']
        self.cid_file = record.output / 'container.cid'
        self.env = os.environ.copy()
        self.env['PATH'] = str(Path(docker).parent) + os.pathsep + self.env.get('PATH', '')

    def call(self, arguments, *, check=True, timeout=60):
        command = [self.docker, *map(str, arguments)]
        self.record.data.setdefault('setup_commands', []).append(command)
        self.record.persist()
        result = subprocess.run(command, capture_output=True, text=True, env=self.env,
                                timeout=timeout, check=False)
        with (self.record.output / 'setup.log').open('a', encoding='utf-8') as log:
            log.write(json.dumps(command) + '\n' + result.stdout + result.stderr)
        if check and result.returncode:
            raise RuntimeError(f'Docker command failed ({result.returncode}): {result.stderr.strip()}')
        return result.stdout

    def create(self, arguments):
        cid = self.call(['create', '--label', f'{LABEL}={self.identity}',
                         '--cidfile', str(self.cid_file), *arguments]).strip()
        if not re.fullmatch(r'[0-9a-f]{64}', cid):
            raise ValueError('Docker did not return a valid container ID')
        return cid

    def cleanup(self):
        """Remove exact owned IDs, then ask the daemon to confirm absence."""
        cleanup = {'ok': False, 'removed': [], 'error': None}
        self.record.data['cleanup'] = cleanup
        handlers = {}
        try:
            for sig in (signal.SIGINT, getattr(signal, 'SIGBREAK', signal.SIGINT)):
                if sig not in handlers:
                    handlers[sig] = signal.signal(sig, signal.SIG_IGN)
            ids = set(self.call(['ps', '-aq', '--filter', f'label={LABEL}={self.identity}'], timeout=10).split())
            if self.cid_file.exists():
                cid = self.cid_file.read_text().strip()
                if not re.fullmatch(r'[0-9a-f]{64}', cid):
                    raise ValueError('Invalid owned CID file')
                ids.add(cid)
            for cid in ids:
                inspected = self.call(['inspect', cid], check=False, timeout=10)
                if not inspected.strip() or inspected.strip() == '[]':
                    continue  # The final query still must confirm absence.
                labels = json.loads(inspected)[0]['Config'].get('Labels') or {}
                if labels.get(LABEL) != self.identity:
                    raise ValueError(f'Refusing to remove container without matching ownership: {cid}')
                self.call(['rm', '-f', cid], timeout=10)
                cleanup['removed'].append(cid)
            remaining = self.call(['ps', '-aq', '--filter', f'label={LABEL}={self.identity}'], timeout=10).strip()
            if remaining:
                raise RuntimeError(f'Owned containers remain: {remaining}')
            cleanup['ok'] = True
        except Exception as exc:
            cleanup['error'] = str(exc)
        finally:
            for sig, handler in handlers.items():
                signal.signal(sig, handler)
            self.record.persist()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--build', action='store_true')
    parser.add_argument('--workers', type=int, choices=range(9), default=0)
    parser.add_argument('--docker', help='Explicit Docker CLI path')
    parser.add_argument('--test-path', action='append')
    options = parser.parse_args(argv)
    identity = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid4().hex[:12]
    output = options.output or ROOT / '.cache/fp-docker-verification' / identity
    try:
        with RunRecord(ROOT, output, ['docker-verification', *(argv if argv is not None else sys.argv[1:])], allow_ignored=True) as record:
            record.begin()
            owner = DockerOwner(record, find_docker(options.docker))
            try:
                owner.call(['version', '--format', '{{.Server.Version}}'])
                if options.build:
                    with tempfile.TemporaryDirectory(prefix='fp-build-') as context:
                        for source in (ROOT / 'requirements-ops.lock', ROOT / 'tools/local_verification/Dockerfile',
                                       ROOT / 'tools/local_verification/requirements-extra.txt'):
                            shutil.copy2(source, context)
                        owner.call(['build', '-t', IMAGE, context], timeout=900)
                image = owner.call(['image', 'inspect', IMAGE, '--format', '{{.Id}}']).strip()
                runtime = json.loads(owner.call(['run', '--rm', '--network', 'none', '--label',
                    f'{LABEL}={owner.identity}', image, 'python', '-c', RUNTIME_PROBE]))
                for key, path in [('lock_sha256', ROOT / 'requirements-ops.lock'),
                                  ('extra_sha256', ROOT / 'tools/local_verification/requirements-extra.txt')]:
                    if runtime[key] != recorder.digest(path.read_bytes()):
                        raise ValueError('Image dependencies differ from this checkout; rebuild with -Build')
                record.data['metadata'] = dict(image_id=image, runtime=runtime, workers=options.workers)
                arguments = ['--network', 'none', '--mount', f'type=bind,source={ROOT},target=/repo,readonly',
                    '--mount', f'type=bind,source={record.output},target=/evidence', '--tmpfs', '/tmp:exec,size=2g',
                    '--env', 'COVERAGE_FILE=/evidence/.coverage', image, 'python', '-m', 'pytest',
                    *(options.test_path or DEFAULT_TESTS), '-n', str(options.workers)]
                if options.workers:
                    arguments += ['--dist=loadscope']
                arguments += ['-q', '-p', 'no:cacheprovider', '--tb=short', '--hypothesis-show-statistics',
                    '--basetemp=/tmp/pytest', '--junitxml=/evidence/junit.xml', '--cov=c1_rail.book_account_owner',
                    '--cov=c1_rail.book_takeover_owner', '--cov=c1_signal_daemon.book_runtime',
                    '--cov-branch', '--cov-report=json:/evidence/coverage.json']
                cid = owner.create(arguments)
                record.execute([owner.docker, 'start', '-a', cid], env=owner.env,
                               reports=[record.output / 'junit.xml'])
            finally:
                owner.cleanup()
        return record.data['verification_exit_code']
    except (OSError, ValueError) as exc:
        print(f'Cannot retain verification evidence: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
