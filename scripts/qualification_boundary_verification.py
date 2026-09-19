"""Record real TEST_ONLY Linux execution and require every canonical invariant."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.record_verification import RunRecord
from scripts.check_qualification_invariants import _manifest, validate_manifest
from tools.qualification_verification.host import cleanup, ownership_lock, protected,create_process_group,owned_command

INVARIANT_MANIFEST = ROOT / 'tests/ops/qualification/invariant_manifest.json'
S2_CASES = 'tests/integration/qualification_boundary/test_campaign_supervision_linux.py'


def require_cleanup(result):
    if type(result) is not dict or result.get('ok') is not True:
        raise ValueError('Owned cleanup did not explicitly succeed')


def require_invariants(raw, collection, report, output, *, required_nodeids=None):
    nodes = json.loads(collection.read_bytes())
    if type(nodes) is not list or any(type(node) is not str for node in nodes) or len(set(nodes)) != len(nodes):
        raise ValueError('Malformed actual collection inventory')
    result = validate_manifest(raw, collected_nodeids=set(nodes),
        junit_paths=(report,), evidence_root=output, required_nodeids=required_nodeids)
    (output / 'invariants.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    if not result['passed']:
        raise ValueError('Qualification invariants missing, skipped or failed; see invariants.json')
    return result


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
    mode.add_argument('--s2', action='store_true', help='targeted diagnostic supervision, never full E1 acceptance')
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
                # Keep cleanup outside this context: cleanup acquires a new open file
                # description for the same non-reentrant flock.
                with ownership_lock(manifest_path.parent):
                    record.begin()
                    if record.data['before'] != manifest['source']:
                        raise ValueError('Candidate source differs from provisioned snapshot')
                    if args.test_only or args.s2:
                        invariant_bytes = INVARIANT_MANIFEST.read_bytes()
                        all_required = _manifest(invariant_bytes)
                        required = {node for node in all_required if node.startswith(S2_CASES+'::') == args.s2}
                        record.data['metadata'].update(acceptance_scope='S2_DIAGNOSTIC_SUPERVISION' if args.s2 else 'N1_ONLY_TEST_ONLY',
                            qualification_acceptance='coordinator_review_required',
                            invariant_manifest_sha256=hashlib.sha256(invariant_bytes).hexdigest())
                    if args.instance or args.profile:
                        raise ValueError('Canonical fixture producer owns instance/profile bindings')
                    report = output / 'junit.xml'
                    env = os.environ.copy()
                    env['FP_QUALIFICATION_HOST_MANIFEST'] = str(manifest_path)
                    if args.s2: env['FP_QUALIFICATION_S2'] = '1'
                    else: env.pop('FP_QUALIFICATION_S2', None)
                    selection=['tests/integration/qualification_host']
                    if args.test_only or args.s2:
                        # Run boundary files in full so new lifecycle cases also run.
                        # Exact manifest cases remain mandatory even if renamed/deleted.
                        selection = ([S2_CASES] if args.s2 else
                            ['tests/integration/qualification_boundary', '--ignore='+S2_CASES] + sorted(
                            node for node in required if not node.startswith('tests/integration/qualification_boundary/')))
                    command=[sys.executable, '-m', 'pytest', *selection, '-n', '0',
                             '-q', '--tb=short', f'--junitxml={report}']
                    if args.test_only or args.s2:
                        collection = output / 'collected.json'
                        command += ['-p', 'scripts.pytest_qualification_collection',
                                    f'--qualification-collection={collection}']
                        command=owned_command(create_process_group(manifest_path.parent),command,sys.executable)
                    record.execute(command, env=env, reports=[report])
                    if args.test_only or args.s2:
                        record.data['invariants'] = require_invariants(invariant_bytes, collection, report, output, required_nodeids=required)
                    require_tests(record.data['test_summary'])
            finally:
                # The ownership_lock context has exited, including on check failure.
                record.data['cleanup'] = cleanup(manifest_path)
                require_cleanup(record.data['cleanup'])
        return record.data['verification_exit_code']
    except (OSError, ValueError) as exc:
        print(f'Failed setup: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
