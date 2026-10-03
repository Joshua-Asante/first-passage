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
from scripts.check_qualification_invariants import _manifest, registered_e_cases, validate_manifest
from tools.qualification_verification.host import cleanup, ownership_lock, protected,create_process_group,owned_command

INVARIANT_MANIFEST = ROOT / 'tests/ops/qualification/invariant_manifest.json'
# Ordered: the supervision file's last case contaminates the common memory
# group, so the service-metering file runs first on the same fresh host.
S2_CASES = ('tests/integration/qualification_boundary/test_campaign_service_linux.py',
            'tests/integration/qualification_boundary/test_campaign_supervision_linux.py')
# S3: the full S2 file set plus the genuine N1 capture/G5 file, on the
# dispatch/v5 installation (FP_QUALIFICATION_S3=1, never FP_QUALIFICATION_S4).
# The supervision file stays LAST: its final case deliberately contaminates the
# common memory group (never-reset oom counters on the host parent the guardian
# polls), which would terminalise every later admission's settlement at
# oom_events > 0 -- the same ordering constraint that already puts the
# service-metering file ahead of it. The service file keeps its established
# first position and the N1 file runs between them; the poll is not baselined.
# The N1_ONLY --test-only selection is untouched; --s3 is a separate, strictly
# larger mode that keeps S3's accepted meaning on the v5 installation.
# S4: a strictly larger mode again -- the joint N2/Part B file joins the S3 set
# between the N1 file and the supervision file on the joint dispatch/v6
# installation (FP_QUALIFICATION_S4=1). The supervision file still stays LAST,
# so its OOM case still runs last; --test-only excludes the whole S4 file set
# (S4 includes the S3 and S2 files).
S3_CASES = (S2_CASES[0], 'tests/integration/qualification_boundary/test_campaign_n1_linux.py',
            S2_CASES[1])
S4_CASES = (S2_CASES[0], 'tests/integration/qualification_boundary/test_campaign_n1_linux.py',
            'tests/integration/qualification_boundary/test_campaign_n2_linux.py', S2_CASES[1])
# S5: the S4 file set plus the Part A Linux file, which is inserted immediately
# before the supervision file so its OOM case still runs last -- built exactly
# as scripts/s2_run_evidence.py builds SCOPE_FILES['S5_PART_A']. --test-only
# excludes the whole S5 file set (S5 includes the S4, S3 and S2 files).
PART_A_CASE = 'tests/integration/qualification_boundary/test_campaign_part_a_linux.py'
S5_CASES = (*S4_CASES[:-1], PART_A_CASE, S4_CASES[-1])
# S8: the integrated full-E1 acceptance -- the S5 file set plus the full-campaign
# file (E01-E12), again immediately before the supervision file so its OOM case
# stays last. --s8 is strictly larger than --s5; --test-only excludes the whole
# S8 file set. Full acceptance requires E01-E12 registered in the one invariant
# manifest; a --cases diagnostic subset does not (it is never acceptance).
FULL_CAMPAIGN_CASE = 'tests/integration/qualification_boundary/test_full_campaign_boundary.py'
S8_CASES = (*S5_CASES[:-1], FULL_CAMPAIGN_CASE, S5_CASES[-1])


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
    """Why the selection cannot run, or None; checked before any host prerequisite.

    A diagnostic subset exists for S3/S4/S5/S8 iteration only. A whitespace-only value is
    no selection at all (pytest's -k ignores it and runs everything), and an
    expression pytest cannot compile would otherwise fail only after the host
    ran; both are refused here, in seconds. Full --s8 acceptance is refused here
    too while E01-E12 are unregistered: the invariant gate could not pass.
    """
    if args.cases is None:
        if args.s8:
            try:
                registered = registered_e_cases(INVARIANT_MANIFEST.read_bytes())
            except (OSError, ValueError) as exc:
                return f'--s8 cannot read the invariant manifest: {exc}'
            if not registered:
                return '--s8 acceptance requires E01-E12 registered in the invariant manifest'
        return None
    if not (args.s3 or args.s4 or args.s5 or args.s8):
        return '--cases is a diagnostic-subset selector for --s3/--s4/--s5/--s8 iteration only'
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
    mode.add_argument('--s4', action='store_true', help='S3 plus the joint N2/Part B file on the joint dispatch/v6 installation, never full E1 acceptance')
    mode.add_argument('--s5', action='store_true', help='S4 plus the Part A Linux file, never full E1 acceptance')
    mode.add_argument('--s8', action='store_true',
                      help='S5 plus the full-campaign E01-E12 file on the integrated installation')
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
                    # --s8 is --s5's environment plus FP_QUALIFICATION_S8 (the
                    # integrated installation, selected by the boundary fixture seam).
                    staged = args.s2 or args.s3 or args.s4 or args.s5 or args.s8
                    if args.test_only or staged:
                        selected_cases = (S8_CASES if args.s8 else S5_CASES if args.s5 else S4_CASES if args.s4
                                          else S3_CASES if args.s3 else S2_CASES)
                        invariant_bytes = INVARIANT_MANIFEST.read_bytes()
                        all_required = _manifest(invariant_bytes)
                        if staged:
                            required = {node for node in all_required
                                        if node.startswith(tuple(case+'::' for case in selected_cases))}
                        else:
                            # N1_ONLY (--test-only): every registered node outside the S8
                            # file set (S8_CASES includes the S5, S4, S3 and S2 files). Those
                            # nodes skip here by design, and the manifest validator refuses
                            # a required node that is skipped or never collected.
                            required = {node for node in all_required
                                        if not node.startswith(tuple(case+'::' for case in S8_CASES))}
                        record.data['metadata'].update(
                            acceptance_scope=('S8_FULL_E1' if args.s8 else
                                              'S5_PART_A' if args.s5 else
                                              'S4_JOINT_N2' if args.s4 else
                                              'S3_N1_CAPTURE' if args.s3 else
                                              'S2_DIAGNOSTIC_SUPERVISION' if args.s2 else
                                              'N1_ONLY_TEST_ONLY'),
                            qualification_acceptance='coordinator_review_required',
                            invariant_manifest_sha256=hashlib.sha256(invariant_bytes).hexdigest())
                        if args.cases is not None:
                            if not (args.s3 or args.s4 or args.s5 or args.s8):
                                raise ValueError('--cases is a diagnostic-subset selector for S3/S4/S5/S8 iteration only')
                            record.data['metadata'].update(acceptance_scope='DIAGNOSTIC_SUBSET',
                                diagnostic_expression=args.cases)
                    if args.instance or args.profile:
                        raise ValueError('Canonical fixture producer owns instance/profile bindings')
                    report = output / 'junit.xml'
                    env = os.environ.copy()
                    env['FP_QUALIFICATION_HOST_MANIFEST'] = str(manifest_path)
                    if staged: env['FP_QUALIFICATION_S2'] = '1'
                    else: env.pop('FP_QUALIFICATION_S2', None)
                    if args.s3 or args.s4 or args.s5 or args.s8: env['FP_QUALIFICATION_S3'] = '1'
                    else: env.pop('FP_QUALIFICATION_S3', None)
                    # --s3 keeps the v5 installation: --s4 sets the joint v6 one, and
                    # --s5 sets it too (coordinator ruling E1: --s5 is --s4's
                    # environment plus FP_QUALIFICATION_S5, which selects the Part A
                    # /v7 installation); every other mode pops the S5 variable.
                    if args.s4 or args.s5 or args.s8: env['FP_QUALIFICATION_S4'] = '1'
                    else: env.pop('FP_QUALIFICATION_S4', None)
                    if args.s5 or args.s8: env['FP_QUALIFICATION_S5'] = '1'
                    else: env.pop('FP_QUALIFICATION_S5', None)
                    if args.s8: env['FP_QUALIFICATION_S8'] = '1'
                    else: env.pop('FP_QUALIFICATION_S8', None)
                    selection=['tests/integration/qualification_host']
                    if args.test_only or staged:
                        # Run boundary files in full so new lifecycle cases also run.
                        # Exact manifest cases remain mandatory even if renamed/deleted.
                        selection = ([*selected_cases] if staged else
                            ['tests/integration/qualification_boundary', *('--ignore='+case for case in S8_CASES)] + sorted(
                            node for node in required if not node.startswith('tests/integration/qualification_boundary/')))
                        if args.cases is not None:
                            selection = ['-k', args.cases, *selection]
                    command=[sys.executable, '-m', 'pytest', *selection, '-n', '0',
                             '-q', '--tb=short', f'--junitxml={report}']
                    if args.test_only or staged:
                        collection = output / 'collected.json'
                        command += ['-p', 'scripts.pytest_qualification_collection',
                                    f'--qualification-collection={collection}']
                        command=owned_command(create_process_group(manifest_path.parent),command,sys.executable)
                    record.execute(command, env=env, reports=[report])
                    if args.cases is not None:
                        raise ValueError('diagnostic-subset runs can never be acceptance evidence')
                    if args.test_only or staged:
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
