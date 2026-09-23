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
# Ordered: the supervision file's last case contaminates the common memory
# group, so the service-metering file runs first on the same fresh host.
S2_CASES = ('tests/integration/qualification_boundary/test_campaign_service_linux.py',
            'tests/integration/qualification_boundary/test_campaign_supervision_linux.py')
# S3: the full S2 file set plus the genuine N1 capture/G5 file. The supervision
# file stays LAST: its final case deliberately contaminates the common memory
# group (never-reset oom counters on the host parent the guardian polls), which
# would terminalise every later admission's settlement at oom_events > 0 -- the
# same ordering constraint that already puts the service-metering file ahead of
# it. The service file keeps its established first position and the N1 file
# runs between them; the poll is not baselined. The N1_ONLY --test-only
# selection is untouched; --s3 is a separate, strictly larger mode.
S3_CASES = (S2_CASES[0], 'tests/integration/qualification_boundary/test_campaign_n1_linux.py', S2_CASES[1])
# T05 (S6-S7): the result/seal file needs the integrated T05 seams (result_g5 and
# seal manifest roles, the seal principal) that no current mode installs, so no
# selection runs it yet and none of its nodes is registered. Like the S3 files it
# stays out of N1_ONLY (--test-only), where a skip would fail require_tests; the
# post-integration selector (T04) names the mode that runs and registers it.
T05_CASES = ('tests/integration/qualification_boundary/test_campaign_result_seal_linux.py',)


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


def cases_refusal(args):
    """Why `--cases` cannot run, or None; checked before any host prerequisite.

    A diagnostic subset exists for S3 iteration only. A whitespace-only value is
    no selection at all (pytest's -k ignores it and runs everything), and an
    expression pytest cannot compile would otherwise fail only after the host
    ran; both are refused here, in seconds.
    """
    if args.cases is None:
        return None
    if not args.s3:
        return '--cases is a diagnostic-subset selector for --s3 iteration only'
    if not args.cases.strip():
        return '--cases is empty or whitespace-only; omit it to run the full selection'
    try:
        # Private API, pinned by requirements-ops.lock: the parser pytest's -k uses.
        from _pytest.mark.expression import Expression  # pylint: disable=import-outside-toplevel
    except ImportError as exc:
        return f'--cases cannot be validated: pytest expression parser unavailable ({exc})'
    try:
        Expression.compile(args.cases)
    except (SyntaxError, RecursionError, MemoryError) as exc:
        # pytest's parser recurses per nesting level: too deep is as uncompilable.
        return f'--cases is not a valid pytest -k expression: {type(exc).__name__}: {exc}'
    return None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--test-only', action='store_true')
    mode.add_argument('--s2', action='store_true', help='targeted diagnostic supervision, never full E1 acceptance')
    mode.add_argument('--s3', action='store_true', help='S2 supervision plus genuine N1 capture/G5, never full E1 acceptance')
    mode.add_argument('--host-only', action='store_true', help='host readiness, never boundary acceptance')
    parser.add_argument('--cases', help='diagnostic subset: a -k expression; the record is marked DIAGNOSTIC_SUBSET and can never be acceptance evidence')
    parser.add_argument('--manifest', type=Path)
    parser.add_argument('--instance', type=Path)
    parser.add_argument('--profile', type=Path)
    args = parser.parse_args(argv)
    refusal = cases_refusal(args)
    if refusal is not None:
        print(f'Failed prerequisite: {refusal}', file=sys.stderr)
        return 2
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
                    if args.test_only or args.s2 or args.s3:
                        selected_cases = S3_CASES if args.s3 else S2_CASES
                        invariant_bytes = INVARIANT_MANIFEST.read_bytes()
                        all_required = _manifest(invariant_bytes)
                        if args.s3:
                            required = {node for node in all_required
                                        if node.startswith(tuple(case+'::' for case in selected_cases))}
                        elif args.s2:
                            required = {node for node in all_required
                                        if node.startswith(tuple(case+'::' for case in S2_CASES))}
                        else:
                            # N1_ONLY (--test-only): every registered node outside the S3
                            # file set (S3_CASES includes the S2 files). The S3 nodes skip
                            # here by design, and the manifest validator refuses a
                            # required node that is skipped or never collected.
                            required = {node for node in all_required
                                        if not node.startswith(tuple(case+'::' for case in S3_CASES))}
                        record.data['metadata'].update(
                            acceptance_scope=('S3_N1_CAPTURE' if args.s3 else 'S2_DIAGNOSTIC_SUPERVISION' if args.s2 else 'N1_ONLY_TEST_ONLY'),
                            qualification_acceptance='coordinator_review_required',
                            invariant_manifest_sha256=hashlib.sha256(invariant_bytes).hexdigest())
                        if args.cases is not None:
                            if not args.s3:
                                raise ValueError('--cases is a diagnostic-subset selector for S3 iteration only')
                            record.data['metadata'].update(acceptance_scope='DIAGNOSTIC_SUBSET',
                                diagnostic_expression=args.cases)
                    if args.instance or args.profile:
                        raise ValueError('Canonical fixture producer owns instance/profile bindings')
                    report = output / 'junit.xml'
                    env = os.environ.copy()
                    env['FP_QUALIFICATION_HOST_MANIFEST'] = str(manifest_path)
                    if args.s2 or args.s3: env['FP_QUALIFICATION_S2'] = '1'
                    else: env.pop('FP_QUALIFICATION_S2', None)
                    if args.s3: env['FP_QUALIFICATION_S3'] = '1'
                    else: env.pop('FP_QUALIFICATION_S3', None)
                    selection=['tests/integration/qualification_host']
                    if args.test_only or args.s2 or args.s3:
                        # Run boundary files in full so new lifecycle cases also run.
                        # Exact manifest cases remain mandatory even if renamed/deleted.
                        selection = ([*selected_cases] if (args.s2 or args.s3) else
                            ['tests/integration/qualification_boundary', *('--ignore='+case for case in S3_CASES + T05_CASES)] + sorted(
                            node for node in required if not node.startswith('tests/integration/qualification_boundary/')))
                        if args.cases is not None:
                            selection = ['-k', args.cases, *selection]
                    command=[sys.executable, '-m', 'pytest', *selection, '-n', '0',
                             '-q', '--tb=short', f'--junitxml={report}']
                    if args.test_only or args.s2 or args.s3:
                        collection = output / 'collected.json'
                        command += ['-p', 'scripts.pytest_qualification_collection',
                                    f'--qualification-collection={collection}']
                        command=owned_command(create_process_group(manifest_path.parent),command,sys.executable)
                    record.execute(command, env=env, reports=[report])
                    if args.cases is not None:
                        raise ValueError('diagnostic-subset runs can never be acceptance evidence')
                    if args.test_only or args.s2 or args.s3:
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
