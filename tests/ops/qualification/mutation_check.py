"""Three bounded structural mutations in a retained disposable source copy.

Use the checkout's operations launcher. Never modify the implementation checkout.
Each control must pass; each mutation must fail in the named test call with the
intended DID NOT RAISE assertion. Collection/setup errors are inconclusive.
"""
import argparse
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET


MUTATIONS = (
    ('product-basis', 'ops/c1_rail/qualification/policy.py',
     'if basis != policy.original_basis:', 'if False:  # controlled mutation: basis comparison disabled',
     'tests/ops/qualification/execution/test_semantic_admission.py::test_resigned_wrong_product_reaches_semantic_rejection'),
    ('registry', 'ops/c1_rail/qualification/legality.py',
     'validate_registry(geometry_bytes, expected_rows={})', 'pass  # controlled mutation: registry validation disabled',
     'tests/ops/qualification/test_legality_evidence.py::test_bound_nonempty_registry_is_not_legality_pass'),
    ('role-content', 'ops/c1_rail/qualification/evidence.py',
     'if proposed.envelope_bytes != expected.envelope_bytes or dict(proposed.output_bytes_by_role) != dict(expected.output_bytes_by_role):',
     'if False:  # controlled mutation: final role-content comparison disabled',
     'tests/ops/qualification/execution/test_artifact_acceptance.py::test_coherent_valid_role_content_still_must_equal_captured_reconstruction'),
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[3]
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    scratch = Path(tempfile.mkdtemp(prefix='fp-qualification-mutations-')).resolve()
    files = subprocess.check_output(['git', '-C', str(source), 'ls-files', '-z',
        '--cached', '--others', '--exclude-standard']).decode().split('\0')
    for relative in filter(None, files):
        original, destination = source / relative, scratch / relative
        if not destination.resolve().is_relative_to(scratch):
            raise ValueError('copy path escaped disposable root')
        if original.is_file():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(original, destination)
    subprocess.run(['git', 'init', '-q', str(scratch)], check=True)
    subprocess.run(['git', '-C', str(scratch), 'add', '.'], check=True)
    subprocess.run(['git', '-C', str(scratch), '-c', 'user.name=Mutation control',
        '-c', 'user.email=mutation@example.invalid', 'commit', '-qm', 'Disposable candidate copy'], check=True,
        stdout=subprocess.DEVNULL)
    launcher = [sys.executable, '-I', str(scratch / 'scripts/fp.py'), '--env', sys.prefix]
    subprocess.run([*launcher, 'doctor'], cwd=scratch, check=True)
    results = []

    def run(label, node):
        records = scratch / '.cache/fp-verification'
        before = set(records.glob('*/record.json'))
        command = [*launcher, '--workers', '1', 'python', '-m', 'pytest', node, '-q', '--tb=short']
        with (output / (label + '.log')).open('w', encoding='utf-8') as stream:
            completed = subprocess.run(command, cwd=scratch, stdout=stream, stderr=subprocess.STDOUT, check=False)
        created = set(records.glob('*/record.json')) - before
        if len(created) != 1:
            raise ValueError('mutation run did not retain exactly one recorder record')
        path = created.pop()
        record = json.loads(path.read_bytes())
        shutil.copytree(path.parent, output / label)
        if not record['source_stable'] or not record['capture_complete'] or record['capture_errors']:
            raise ValueError('mutation/control run lacks stable complete evidence')
        return completed.returncode, record, ET.parse(path.parent / 'junit.xml').findall('.//testcase')

    for name, relative, before, after, node in MUTATIONS:
        code, control, cases = run(name + '-control', node)
        if code != 0 or control['verification_exit_code'] != 0 or len(cases) != 1 or list(cases[0]):
            raise ValueError(name + ': unchanged control did not pass')
        path = scratch / relative
        original_bytes = path.read_bytes()
        raw = original_bytes.decode('utf-8')
        if raw.count(before) != 1:
            raise ValueError(name + ': mutation target is not unique')
        mutated = raw.replace(before, after)
        patch = ''.join(difflib.unified_diff(raw.splitlines(True), mutated.splitlines(True),
            fromfile='a/' + relative, tofile='b/' + relative))
        patch_path = output / (name + '.patch')
        patch_path.write_bytes(patch.encode('utf-8'))
        try:
            path.write_bytes(mutated.encode('utf-8'))
            code, record, cases = run(name + '-mutated', node)
            if (code != 1 or record['exit_code'] != 1 or len(cases) != 1
                    or cases[0].get('name') != node.split('::')[-1]
                    or cases[0].find('error') is not None or cases[0].find('skipped') is not None
                    or cases[0].find('failure') is None
                    or 'DID NOT RAISE' not in (cases[0].find('failure').text or '')):
                raise ValueError(name + ': mutation survived or failed inconclusively')
            results.append(dict(name=name, nodeid=node, killed=True,
                patch_sha256=hashlib.sha256(patch_path.read_bytes()).hexdigest(),
                control_fingerprint=control['before']['fingerprint'],
                mutation_fingerprint=record['before']['fingerprint'], assertion='DID NOT RAISE'))
        finally:
            path.write_bytes(original_bytes)
        # Prove restoration before moving on; preserve scratch and all records.
        if path.read_bytes() != original_bytes:
            raise ValueError('mutation source was not restored')
        print(name + ': control passed; mutation killed by intended assertion', flush=True)
    summary = dict(source=str(source), scratch=str(scratch), restored=True, results=results)
    (output / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
