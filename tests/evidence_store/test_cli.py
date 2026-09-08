"""Exercise the actual process interface, not argparse implementation details."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


class CliTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / 'repo'
        self.repo.mkdir()
        self.store = Path(self.temp.name) / 'store'
        (self.repo / 'decision.md').write_text('# Decision\n## Ruling\nStatus: parked\n', encoding='utf-8')

    def cli(self, *args, exit_code=0):
        proc = subprocess.run([sys.executable, '-m', 'scripts.evidence_store',
                               '--repo', str(self.repo), '--store', str(self.store), *args],
                              cwd=REPO, capture_output=True, text=True)
        self.assertEqual(proc.returncode, exit_code, proc.stdout + proc.stderr)
        self.assertNotIn('Traceback', proc.stderr)
        return json.loads(proc.stdout if proc.returncode == 0 else proc.stderr)

    def document(self, name, data):
        path = Path(self.temp.name) / name
        path.write_text(json.dumps(data), encoding='utf-8')
        return str(path)

    def test_end_to_end_decision_correction_and_rebuild(self):
        source = self.cli('capture', 'venue:F1', 'decision.md', '--kind', 'adr')
        annotation = self.document('record.json', dict(
            record_id='venue:F1', kind='decision', source_version=source['version_id'],
            section='## Ruling', statement='Status: parked', status='parked',
            conditions={'venue': 'example'}, effective_at='2026-08-01T00:00:00Z'))
        record = self.cli('record', annotation)
        dependency = self.document('dependency.json', dict(
            consumer=record['id'], dependency=source['version_id'],
            evidence_version=source['version_id'], note='declared input'))
        self.cli('depend', dependency)
        self.assertEqual(self.cli('decision', 'venue:F1')['current']['status'], 'parked')
        self.assertEqual(self.cli('source', source['version_id'])['current'], 'unchanged')
        before = self.cli('export')
        (self.repo / 'decision.md').write_text('Changed after decision', encoding='utf-8')
        findings = self.cli('check')['findings']
        self.assertEqual(findings[0]['dependents'][0]['record_id'], 'venue:F1')
        self.assertEqual(self.cli('impact', source['version_id'])['dependents'][0]['status'], 'needs_review')
        (self.store / 'index.sqlite').unlink()
        self.cli('rebuild')
        self.assertEqual(self.cli('export'), before)

    def test_malformed_annotation_is_machine_readable_failure(self):
        source = self.cli('capture', 'venue:F1', 'decision.md')
        wrong = self.document('bad.json', {'source_version': source['version_id']})
        error = self.cli('record', wrong, exit_code=2)
        self.assertIn('error', error)
        wrong = self.document('array.json', [])
        self.assertIn('error', self.cli('record', wrong, exit_code=2))
        self.assertIn('error', self.cli('source', 'unknown', exit_code=2))

    def test_retrieval_use_and_preserved_receipt_workflow(self):
        source = self.cli('capture', 'venue:F1', 'decision.md')
        annotation = self.document('record.json', dict(
            record_id='venue:F1', kind='decision', source_version=source['version_id'],
            section='## Ruling', statement='Status: parked', status='parked',
            conditions={'venue': 'example'}, effective_at='2026-08-01T00:00:00Z'))
        record = self.cli('record', annotation)
        receipt = self.cli('retrieve', self.document('request.json', {'context': {'venue': 'example'}}))
        self.assertEqual(receipt['data']['results'][0]['applicability']['status'], 'matching')
        self.cli('use', self.document('use.json', dict(receipt_id=receipt['id'], decision_revision=record['id'],
                 selections=[dict(revision_id=record['id'], disposition='applied', reason='reviewed ruling')])))
        (self.repo / 'decision.md').write_text('changed', encoding='utf-8')
        preserved = self.cli('receipt', receipt['id'])
        self.assertEqual(preserved['receipt'], receipt)
        self.assertEqual(preserved['uses'][0]['unassessed'], [])
        later = self.cli('retrieve', self.document('request.json', {'record_ids': ['venue:F1']}))
        self.assertIn('source_needs_review', later['data']['results'][0]['warnings'])
        graph = self.cli('export')
        self.cli('rebuild')
        self.assertEqual(self.cli('export'), graph)
        self.assertIn('error', self.cli('receipt', 'absent', exit_code=2))
        self.assertIn('error', self.cli('retrieve', self.document('empty.json', {}), exit_code=2))

    def test_missing_capture_is_advisory_and_raw_source_is_not_dumped(self):
        self.cli('capture', 'absent', 'absent.md')
        source = self.cli('capture', 'private', 'decision.md')
        self.assertNotIn('Status: parked', json.dumps(source))
        self.assertEqual(self.cli('check')['findings'][0]['source']['preserved'], 'missing')

    def test_belief_review_cli_preserves_judgment_and_receipt(self):
        source = self.cli('capture', 'claim', 'decision.md')
        fields = dict(source_version=source['version_id'], section='## Ruling',
                      statement='Status: parked', status='parked', conditions={'venue': 'example'},
                      effective_at='2026-08-01T00:00:00Z')
        belief = self.cli('record', self.document('belief.json', dict(fields, record_id='belief', kind='belief')))
        evidence = self.cli('record', self.document('finding.json', dict(fields, record_id='finding', kind='finding')))
        review = dict(belief_revision=belief['id'], judgment='supported', reviewer='fixture',
                      source_version=source['version_id'], section='## Ruling', statement='Status: parked',
                      evidence=[dict(revision_id=evidence['id'], relationship='supporting',
                                     rationale='Fixture comparison', resolution=None)])
        assessment = self.cli('assess', self.document('review.json', review))
        context = self.document('context.json', {'venue': 'example'})
        view = self.cli('belief', 'belief', '--context', context)
        self.assertEqual(view['belief']['assessment'], assessment)
        receipt = self.cli('retrieve', self.document('request.json', {'record_ids': ['belief'], 'context': {'venue': 'example'}}))
        (self.repo / 'decision.md').write_text('Changed', encoding='utf-8')
        self.assertEqual(self.cli('belief', 'belief', '--context', context)['belief']['review_status'], 'needs_review')
        self.assertEqual(self.cli('receipt', receipt['id'])['receipt'], receipt)
        graph = self.cli('export')
        self.cli('rebuild')
        self.assertEqual(self.cli('export'), graph)
        self.assertIn('error', self.cli('belief', 'finding', exit_code=2))


if __name__ == '__main__':
    unittest.main()
