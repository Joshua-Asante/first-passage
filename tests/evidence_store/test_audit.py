"""Decision audits follow receipt-time provenance, not today's replacement graph."""
import json
import tempfile
import unittest
from pathlib import Path

from scripts.evidence_store.store import EvidenceError, Store


class AuditTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.now = '2026-09-08T10:00:00Z'
        self.store = Store(self.repo, self.repo / '.evidence', clock=lambda: self.now)

    def record(self, name, kind='finding'):
        path = self.repo / (name + '.md')
        path.write_text('# Record\n## Claim\nRecorded claim\n', encoding='utf-8')
        source = self.store.capture(name, path.name, 'document')['version_id']
        return self.store.record(record_id=name, kind=kind, source_version=source, section='## Claim',
                                 statement='Recorded claim', status='recorded', conditions={'scope': 'test'},
                                 effective_at=self.now)

    def assess(self, belief, evidence, supersedes=None):
        return self.store.assess(belief_revision=belief['id'], judgment='supported', reviewer='fixture',
                                source_version=belief['source_version'], section='## Claim',
                                statement='Recorded claim', evidence=[dict(revision_id=evidence['id'],
                                relationship='supporting', rationale='fixture', resolution=None)], supersedes=supersedes)

    def use(self, receipt, decision, selected, disposition='applied'):
        return self.store.use(receipt['id'], decision['id'], [dict(revision_id=selected['id'],
                              disposition=disposition, reason='Recorded fixture reason')])

    def test_historical_assessment_and_old_evidence_still_find_applied_decision(self):
        belief = self.record('belief', 'belief')
        old = self.record('old')
        new = self.record('new')
        decision = self.record('decision', 'decision')
        assessment = self.assess(belief, old)
        receipt = self.store.retrieve(record_ids=['belief'], context={'scope': 'test'})
        self.use(receipt, decision, belief)
        self.assess(belief, new, assessment['id'])
        (self.repo / 'old.md').unlink()
        for node in (old['id'], old['source_version'], assessment['id']):
            report = self.store.use_impact(node)
            self.assertEqual(report['applied_decisions'], [decision['id']])
        self.assertEqual(self.store.use_impact(new['id'])['matches'], [])
        report = self.store.review(decision['id'])
        self.assertEqual(report['uses'][0]['receipt'], receipt)
        self.assertEqual(report['review_status'], 'needs_review')
        checks = report['uses'][0]['items'][0]['current_checks']
        self.assertTrue(any(row['id'] == assessment['id'] and row['status'] == 'needs_review' for row in checks))

    def test_applied_declined_and_unassessed_are_distinct(self):
        first, second = self.record('first'), self.record('second')
        applied, declined = self.record('applied', 'decision'), self.record('declined', 'decision')
        receipt = self.store.retrieve(record_ids=['first', 'second'])
        self.use(receipt, applied, first)
        self.use(receipt, declined, first, 'not_applied')
        report = self.store.use_impact(first['id'])
        self.assertEqual(report['applied_decisions'], [applied['id']])
        dispositions = {entry['disposition'] for entry in report['matches'][0]['decisions']}
        self.assertEqual(dispositions, {'applied', 'not_applied'})
        report = self.store.use_impact(second['id'])
        self.assertEqual(report['applied_decisions'], [])
        self.assertEqual({e['disposition'] for e in report['matches'][0]['decisions']}, {'unassessed'})

    def test_journal_prefix_excludes_later_declared_dependencies_and_handles_cycles(self):
        first, second = self.record('first'), self.record('second')
        decision = self.record('decision', 'decision')
        receipt = self.store.retrieve(record_ids=['first'])
        self.use(receipt, decision, first)
        self.store.depend(consumer=first['id'], dependency=second['id'], evidence_version=first['source_version'], note='later')
        self.store.depend(consumer=second['id'], dependency=first['id'], evidence_version=second['source_version'], note='cycle')
        self.assertEqual(self.store.use_impact(second['id'])['matches'], [])
        later = self.store.retrieve(record_ids=['first'])
        self.use(later, decision, first)
        self.assertEqual(len(self.store.use_impact(second['id'])['matches']), 1)

    def test_known_at_selects_pinned_assessment_not_latest_at_receipt(self):
        belief = self.record('belief', 'belief')
        first, second = self.record('first'), self.record('second')
        a1 = self.assess(belief, first)
        self.now = '2026-09-08T11:00:00Z'
        a2 = self.assess(belief, second, a1['id'])
        receipt = self.store.retrieve(record_ids=['belief'], known_at='2026-09-08T10:30:00Z')
        self.assertEqual(self.store.use_impact(a1['id'])['matches'][0]['receipt_id'], receipt['id'])
        self.assertEqual(self.store.use_impact(a2['id'])['matches'], [])

    def test_read_only_empty_unknown_and_markdown(self):
        decision = self.record('decision', 'decision')
        original = (self.store.root / 'events.jsonl').read_bytes()
        report = self.store.review(decision['id'])
        self.assertEqual(report['review_status'], 'unassessed')
        self.assertEqual(report['uses'], [])
        self.assertIn('no_recorded_use', report['warnings'])
        self.assertEqual(self.store.use_impact(decision['id'])['applied_decisions'], [])
        with self.assertRaises(EvidenceError):
            self.store.review('decision')
        with self.assertRaises(EvidenceError):
            self.store.use_impact('unknown')
        self.assertEqual((self.store.root / 'events.jsonl').read_bytes(), original)

    def test_legacy_receipts_rebuild_without_new_annotations(self):
        evidence = self.record('evidence')
        receipt = self.store.retrieve(record_ids=['evidence'])
        journal = self.store.root / 'events.jsonl'
        lines = journal.read_bytes().splitlines(keepends=True)
        receipt['schema'] = 2
        for row in receipt['data']['results']:
            row.pop('belief')
        journal.write_bytes(b''.join(lines[:-1]) + (json.dumps(receipt) + '\n').encode())
        decision = self.record('decision', 'decision')
        self.use(receipt, decision, evidence)
        self.store.rebuild()
        self.assertEqual(self.store.use_impact(evidence['source_version'])['applied_decisions'], [decision['id']])
