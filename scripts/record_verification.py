#!/usr/bin/env python3
"""Durable, source-bound verification records shared by local entry points."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys
import threading
import time
from uuid import uuid4
import xml.etree.ElementTree as ET


PROGRESS_INTERVAL_SECONDS = 30.0
MAX_PROGRESS_BYTES = 160_000


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


def external_file_identity(path):
    """Bind the lexical selection, symlink ancestors, resolved target and bytes."""
    path = Path(path)
    links = {str(p): os.readlink(p) for p in (path, *path.parents) if p.is_symlink()}
    return dict(sha256=digest(path.read_bytes()), resolved_path=str(path.resolve(strict=True)),
                symlinks=links)


def report_identity(path):
    if not path.exists():
        return None
    stat = path.stat()
    return stat.st_mtime_ns, stat.st_ctime_ns, stat.st_size, digest(path.read_bytes())


def junit_summary(root):
    if root.tag not in ('testsuite', 'testsuites'):
        raise ValueError('Expected a testsuite or testsuites root')
    counts = dict(collected=0, passed=0, failed=0, errors=0, skipped=0)
    for case in root.findall('testcase'):
        present = [key for tag, key in [('failure', 'failed'), ('error', 'errors'), ('skipped', 'skipped')]
                   if case.find(tag) is not None]
        if len(present) > 1:
            raise ValueError('Contradictory testcase outcomes')
        counts['collected'] += 1
        counts[present[0] if present else 'passed'] += 1
    for suite in root.findall('testsuite'):
        child = junit_summary(suite)
        for key in counts:
            counts[key] += child[key]
    for attribute, key in [('tests', 'collected'), ('failures', 'failed'), ('errors', 'errors'), ('skipped', 'skipped')]:
        if attribute in root.attrib and int(root.attrib[attribute]) != counts[key]:
            raise ValueError(f'JUnit {attribute} count does not match testcase outcomes')
    if root.tag == 'testsuite' and 'tests' not in root.attrib:
        raise ValueError('JUnit suite is missing its tests count')
    return counts


class RunRecord:
    """One owner reserves, updates and finalizes a run; incomplete is never success."""

    def __init__(self, repo, output, requested_command, *, allow_ignored=False,
                 progress_interval=PROGRESS_INTERVAL_SECONDS):
        if not math.isfinite(progress_interval) or progress_interval <= 0:
            raise ValueError('Progress interval must be positive and finite')
        self.progress_interval = progress_interval
        self.repo, self.output = Path(repo).resolve(), Path(output).resolve()
        if self.output.is_relative_to(self.repo):
            if not allow_ignored or subprocess.run(
                ['git', '-C', str(self.repo), 'check-ignore', '-q', '--',
                 str(self.output.relative_to(self.repo))], check=False).returncode:
                raise ValueError('Evidence output must be outside the measured source tree or explicitly ignored')
        self.output.mkdir(parents=True, exist_ok=False)
        self.clock = time.monotonic()
        self.started_child = False
        self.data = dict(schema_version=2, run_id=uuid4().hex, status='not_started',
                         started_at=datetime.now(timezone.utc).isoformat(), finished_at=None,
                         source_root=str(self.repo), requested_command=requested_command, command=None,
                         before=None, after=None, source_stable=False, exit_code=None,
                         verification_exit_code=None, error=None, launch_error=None,
                         recorder_python=sys.version, recorder_platform=platform.platform(),
                         metadata={}, capture_complete=False, capture_errors=[],
                         junit=[], report_errors=[], test_summary=None, artifacts={})
        self.persist()
        print(f'Verification record: {self.output / "record.json"}', flush=True)

    def persist(self):
        temporary = self.output / 'record.json.tmp'
        with temporary.open('w', encoding='utf-8') as target:
            json.dump(self.data, target, indent=2)
            target.write('\n')
            target.flush()
            os.fsync(target.fileno())
        os.replace(temporary, self.output / 'record.json')

    def __enter__(self):
        return self

    def begin(self):
        self.data['before'] = snapshot(self.repo)
        self.persist()

    def track_external_files(self, paths):
        """Measure explicit files only, not their import/data dependency closure."""
        self.data['external_files'] = dict(
            before={str(p): external_file_identity(p) for p in sorted(set(paths))},
            after=None, stable=False,
            scope='Explicit external files only; supporting imports/data are outside the source inventory')
        self.persist()

    def heartbeat(self):
        activity = 'test activity unavailable'
        try:
            with (self.output / 'progress.json').open('rb') as source:
                raw = source.read(MAX_PROGRESS_BYTES + 1)
            if len(raw) > MAX_PROGRESS_BYTES:
                raise ValueError('Oversized progress')
            progress = json.loads(raw)
            observed = progress['observed_at']
            started = datetime.fromisoformat(self.data['started_at']).timestamp()
            if (progress['run_id'] != self.data['run_id'] or
                    not isinstance(observed, (float, int)) or
                    not started <= observed <= time.time() + 1):
                raise ValueError('Stale progress')
            completed, collected = progress['completed'], progress['collected']
            active = progress['active_nodeids']
            if (type(completed) is not int or completed < 0 or
                    (collected is not None and (type(collected) is not int or collected < 0)) or
                    not isinstance(active, list) or not all(isinstance(s, str) for s in active)):
                raise ValueError('Invalid progress')
            activity = (f'observed completed={completed}, collected={collected}, '
                        f'active={json.dumps([s[:200] for s in active[:5]], ensure_ascii=True)}, '
                        f'observation age={time.time() - observed:.0f}s (advisory)')
        except (OSError, ValueError, KeyError, TypeError):
            pass
        try:
            print(f'[verification progress] elapsed={time.monotonic() - self.clock:.1f}s; {activity}', flush=True)
        except OSError:
            pass

    def execute(self, command, *, env=None, reports=()):
        command = [str(part) for part in command]
        reports = [Path(p).resolve() for p in reports]
        identities = [report_identity(p) for p in reports]
        self.data.update(command=command, status='running')
        self.persist()
        errors = self.data['capture_errors']
        lock, stopped = threading.Lock(), threading.Event()

        def copy_stream(source, destination, live):
            try:
                while data := source.read1(8192):
                    with lock:
                        if stopped.is_set():
                            return
                        if destination is not None:
                            try:
                                destination.write(data)
                                destination.flush()
                            except OSError as exc:
                                errors.append(str(exc))
                                destination = None
                        if live is not None:
                            try:
                                live.buffer.write(data)
                                live.buffer.flush()
                            except (OSError, AttributeError):
                                live = None
            except OSError as exc:
                with lock:
                    if not stopped.is_set():
                        errors.append(str(exc))
            finally:
                source.close()

        with (self.output / 'stdout.txt').open('wb') as stdout, (self.output / 'stderr.txt').open('wb') as stderr:
            try:
                process = subprocess.Popen(command, cwd=self.repo, env=env,
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except OSError as exc:
                self.data.update(exit_code=127, launch_error=str(exc))
                raise
            self.started_child = True
            threads = [threading.Thread(target=copy_stream, args=pair, daemon=True) for pair in (
                (process.stdout, stdout, sys.stdout), (process.stderr, stderr, sys.stderr))]
            for thread in threads:
                thread.start()
            try:
                next_heartbeat = time.monotonic() + self.progress_interval
                while True:
                    try:
                        self.data['exit_code'] = process.wait(timeout=min(.25, self.progress_interval))
                        break
                    except subprocess.TimeoutExpired:
                        if time.monotonic() >= next_heartbeat:
                            self.heartbeat()
                            next_heartbeat = time.monotonic() + self.progress_interval
            except BaseException:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
                raise
            finally:
                deadline = time.monotonic() + 3
                for thread in threads:
                    thread.join(timeout=max(0, deadline - time.monotonic()))
                with lock:
                    stopped.set()
                    if any(thread.is_alive() for thread in threads):
                        errors.append('Output pipes remained open after child exit; capture stopped')
                self.data['capture_complete'] = not errors
        self.collect_reports(reports, identities)
        return self.data['exit_code']

    def collect_reports(self, reports, identities):
        total = dict(collected=0, passed=0, failed=0, errors=0, skipped=0)
        for index, (report, old_identity) in enumerate(zip(reports, identities)):
            try:
                raw = report.read_bytes()
                retained = report if report.parent == self.output else self.output / f'junit-{index}.xml'
                if retained != report:
                    retained.write_bytes(raw)
                entry = dict(file=retained.name, original_path=str(report))
                self.data['junit'].append(entry)
                if report_identity(report) == old_identity:
                    raise ValueError('Expected JUnit report was not refreshed by this run')
                root = ET.fromstring(raw)
                counts = junit_summary(root)
                entry['suites'] = [dict(s.attrib) for s in root.iter('testsuite')]
                entry['counts'] = counts
                for key in total:
                    total[key] += counts[key]
                if counts['failed'] or counts['errors']:
                    raise ValueError('JUnit contains failed tests or errors')
            except (OSError, ValueError, ET.ParseError) as exc:
                self.data['report_errors'].append(f'{report}: {exc}')
        if reports:
            self.data['test_summary'] = total

    def __exit__(self, kind, exc, traceback):
        interrupted = isinstance(exc, KeyboardInterrupt)
        if exc is not None:
            self.data['error'] = f'{type(exc).__name__}: {exc}'
            print(self.data['error'], file=sys.stderr)
        try:
            self.data['after'] = snapshot(self.repo)
            self.data['source_stable'] = self.data['before'] is not None and self.data['before'] == self.data['after']
        except Exception as snapshot_error:
            self.data['after'] = {'snapshot_error': str(snapshot_error)}
        external = self.data.get('external_files')
        if external is not None:
            try:
                external['after'] = {p: external_file_identity(p) for p in external['before']}
                external['stable'] = external['before'] == external['after']
            except (OSError, RuntimeError) as external_error:
                external['error'] = str(external_error)
        code = (130 if interrupted else self.data['exit_code']) or (
            2 if exc is not None or not self.started_child else
            4 if not self.data['capture_complete'] else
            5 if self.data['report_errors'] else
            6 if self.data.get('cleanup', {}).get('ok') is False else
            3 if not self.data['source_stable'] or (external is not None and not external['stable']) else 0)
        self.data.update(verification_exit_code=code,
                         status='interrupted' if interrupted else ('not_started' if not self.started_child else ('failed' if code else 'completed')),
                         finished_at=datetime.now(timezone.utc).isoformat(),
                         duration_seconds=time.monotonic() - self.clock)
        try:
            self.data['artifacts'] = {p.name: digest(p.read_bytes()) for p in sorted(self.output.iterdir())
                                      if p.is_file() and p.name not in ('record.json', 'record.json.tmp')}
        except OSError as artifact_error:
            self.data.update(error=str(artifact_error), verification_exit_code=4,
                             status='interrupted' if interrupted else ('failed' if self.started_child else 'not_started'))
        self.persist()
        print(json.dumps({key: self.data[key] for key in ('status', 'exit_code', 'verification_exit_code', 'source_stable')}))
        return exc is not None and isinstance(exc, (Exception, KeyboardInterrupt))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--metadata', type=Path)
    parser.add_argument('--progress-interval', type=float, default=PROGRESS_INTERVAL_SECONDS)
    parser.add_argument('--allow-ignored-output', action='store_true')
    parser.add_argument('--junit-report', action='append', default=[], type=Path)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    if not command:
        parser.error('A command is required after --')
    try:
        with RunRecord(args.repo, args.output, command, allow_ignored=args.allow_ignored_output,
                       progress_interval=args.progress_interval) as record:
            record.begin()
            if args.metadata:
                record.data['metadata'] = json.loads(args.metadata.read_text(encoding='utf-8-sig'))
            record.execute(command, reports=args.junit_report)
        return record.data['verification_exit_code']
    except (OSError, ValueError) as exc:
        print(f'Cannot retain verification evidence: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
