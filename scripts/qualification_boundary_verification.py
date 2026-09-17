"""One recorder for disposable host checks and future boundary acceptance."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import platform
import sys
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.record_verification import RunRecord
from scripts.qualification_boundary_environment import inspect_environment, require_environment
from tools.qualification_verification.host import cleanup, ownership_lock, protected


def require_tests(counts):
    keys = {'collected', 'passed', 'failed', 'errors', 'skipped'}
    if (not isinstance(counts, dict) or set(counts) != keys
            or any(type(value) is not int or value < 0 for value in counts.values())
            or counts['collected'] == 0 or counts['passed'] != counts['collected']
            or any(counts[name] for name in ('failed', 'errors', 'skipped'))):
        raise ValueError('Critical tests missing, failed, skipped or malformed')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--test-only', action='store_true')
    mode.add_argument('--host-only', action='store_true', help='host readiness, never boundary acceptance')
    parser.add_argument('--manifest', type=Path)
    parser.add_argument('--instance', type=Path)
    parser.add_argument('--profile', type=Path)
    args = parser.parse_args(argv)
    if platform.system() != 'Linux' or os.geteuid() != 0:
        print('Failed prerequisite: Linux administrator on a disposable host', file=sys.stderr)
        return 2
    if not args.manifest:
        print('Failed prerequisite: --manifest from provision.sh is required', file=sys.stderr)
        return 2
    try:
        manifest_path = protected(args.manifest)
        manifest = json.loads(manifest_path.read_bytes())
        output = manifest_path.parent / 'evidence' / uuid4().hex
        with RunRecord(ROOT, output, sys.argv if argv is None else argv) as record:
            record.data['metadata'] = {'purpose': 'host_readiness' if args.host_only else 'boundary_acceptance',
                                       'ownership_manifest': str(manifest_path),
                                       'host_config_sha256': manifest['host_config_sha256']}
            try:
                with ownership_lock(manifest_path.parent):
                    record.begin()
                    if record.data['before'] != manifest['source']:
                        raise ValueError('Candidate source differs from provisioned snapshot')
                    if not args.host_only:
                        if not args.instance or not args.profile:
                            raise ValueError('Boundary fixture producer missing: protected instance/profile required')
                        report = inspect_environment(args.instance, protected(args.profile).read_bytes())
                        (output / 'environment.json').write_text(json.dumps(report, indent=2) + '\n')
                        require_environment(report)
                        raise ValueError('Boundary acceptance integration unavailable: canonical fixture producer, '
                                         'release/image enrollment and launch-to-G5 suite must be integrated by boundary owner')
                    report = output / 'junit.xml'
                    env = os.environ.copy()
                    env['FP_QUALIFICATION_HOST_MANIFEST'] = str(manifest_path)
                    record.execute([sys.executable, '-m', 'pytest', 'tests/integration/qualification_host',
                                    '-q', '--tb=short', f'--junitxml={report}'], env=env, reports=[report])
                    require_tests(record.data['test_summary'])
            finally:
                record.data['cleanup'] = cleanup(manifest_path)
        return record.data['verification_exit_code']
    except (OSError, ValueError) as exc:
        print(f'Failed setup: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
