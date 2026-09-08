"""End-to-end retrieval and reported-use behavior over real local stores."""
import hashlib
import json
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

from scripts.evidence_store.store import EvidenceError, Store


class RetrievalTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.now = '2026-09-08T12:00:00Z'
        self.store = Store(self.repo, self.repo / '.evidence', clock=lambda: self.now)

    def record(self, name, conditions, kind='finding', **kwargs):
        path = self.repo / (name + '.md')
        path.write_text('# Evidence\n## Finding\nObserved result\n', encoding='utf-8')
        version = self.store.capture(name, path.name, 'document')['version_id']
        return self.store.record(record_id=name, kind=kind, source_version=version,
                                 section='## Finding', statement='Observed result',
                                 status='recorded', conditions=conditions,
                                 effective_at=kwargs.pop('effective_at', '2026-09-01T00:00:00Z'), **kwargs)

    def test_matching_unknown_and_conflicting_are_visible_in_stable_order(self):
        self.record('a-conflict', {'instrument': 'NQ'})
        self.record('z-match', {'instrument': 'ES'})
        self.record('b-unknown', {'instrument': 'ES', 'regime': ['trend']})
        self.record('c-empty', {})
        result = self.store.retrieve(context={'instrument': 'ES'})
        rows = result['data']['results']
        self.assertEqual([row['record_id'] for row in rows], ['z-match', 'b-unknown', 'c-empty', 'a-conflict'])
        self.assertEqual([row['applicability']['status'] for row in rows],
                         ['matching', 'unknown', 'unknown', 'conflicting'])
        self.assertEqual(rows[1]['applicability']['unknown'], ['regime'])

    def test_type_sensitive_conditions_and_explicit_selection(self):
        self.record('boolean', {'enabled': True})
        self.record('number', {'enabled': 1})
        rows = self.store.retrieve(context={'enabled': 1}, record_ids=['boolean'])['data']['results']
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['applicability']['status'], 'conflicting')
        for args in ({}, {'record_ids': ['absent']}, {'record_ids': []}, {'context': {'x': float('nan')}}):
            with self.subTest(args=args), self.assertRaises(EvidenceError):
                self.store.retrieve(**args)

    def test_future_and_unknown_dates_are_unselectable(self):
        self.record('future', {}, effective_at='2027-01-01T00:00:00Z')
        self.record('undated', {}, effective_at=None)
        rows = self.store.retrieve(record_ids=['future', 'undated'])['data']['results']
        self.assertTrue(all(row['current'] is None for row in rows))
        self.assertTrue(all(row['applicability']['status'] == 'unknown' for row in rows))

    def test_numbers_share_json_type_but_boolean_is_distinct(self):
        self.record('number', {'count': 1})
        result = self.store.retrieve(context={'count': 1.0})
        self.assertEqual(result['data']['results'][0]['applicability']['status'], 'matching')

    def test_registry_identity_is_visible_without_content_before_known_at(self):
        self.record('later', {'instrument': 'ES'})
        for kwargs in ({'context': {'instrument': 'ES'}}, {'record_ids': ['later']}):
            result = self.store.retrieve(known_at='2026-09-07T00:00:00Z', **kwargs)
            rows = result['data']['results']
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]['history'], [])
            self.assertIsNone(rows[0]['current'])
            self.assertEqual(rows[0]['applicability']['status'], 'unknown')

    def test_transitive_correction_and_receipt_survive_edits_and_rebuild(self):
        source = self.record('source', {})
        middle = self.record('middle', {})
        decision = self.record('decision', {'instrument': 'ES'}, kind='decision')
        self.store.depend(consumer=middle['id'], dependency=source['id'],
                          evidence_version=middle['source_version'], note='uses source')
        self.store.depend(consumer=decision['id'], dependency=middle['id'],
                          evidence_version=decision['source_version'], note='uses middle')
        self.store.depend(consumer=middle['id'], dependency=decision['id'],
                          evidence_version=middle['source_version'], note='cycle')
        (self.repo / 'source.md').write_text('changed', encoding='utf-8')
        receipt = self.store.retrieve(record_ids=['decision'])
        corrections = receipt['data']['results'][0]['corrections']
        self.assertIn(source['source_version'], [item['id'] for item in corrections])
        self.record('source', {}, supersedes=source['id'])
        later = self.store.retrieve(record_ids=['decision'])
        self.assertIn('dependency_superseded', str(later['data']['results'][0]['corrections']))
        self.store.rebuild()
        self.assertEqual(self.store.receipt(receipt['id'])['receipt'], receipt)

    def test_use_membership_reasons_and_unassessed_are_explicit(self):
        first = self.record('first', {})
        second = self.record('second', {})
        decision = self.record('decision', {}, kind='decision')
        receipt = self.store.retrieve(record_ids=['first', 'second'])
        for selections in ([{'revision_id': decision['id'], 'disposition': 'applied', 'reason': 'outside'}],
                           [{'revision_id': first['id'], 'disposition': 'applied', 'reason': ''}]):
            with self.assertRaises(EvidenceError):
                self.store.use(receipt['id'], decision['id'], selections)
        selected = [{'revision_id': first['id'], 'disposition': 'not_applied', 'reason': 'different regime'}]
        use = self.store.use(receipt['id'], decision['id'], selected)
        report = self.store.receipt(receipt['id'])
        self.assertEqual(report['uses'][0]['unassessed'], [second['id']])
        self.assertEqual(report['uses'][0]['event'], use)
        with self.assertRaises(EvidenceError):
            self.store.use(receipt['id'], decision['id'], selected)

    def test_graph_and_legacy_replay_are_deterministic(self):
        finding = self.record('finding', {})
        decision = self.record('decision', {}, kind='decision')
        receipt = self.store.retrieve(record_ids=['finding'])
        self.store.use(receipt['id'], decision['id'],
                       [{'revision_id': finding['id'], 'disposition': 'applied', 'reason': 'supports decision'}])
        before = self.store.export()
        (self.store.root / 'index.sqlite').unlink()
        self.assertEqual(before, self.store.export())
        self.assertEqual(before['schema'], 3)
        self.assertTrue({'RetrievalReceipt', 'EvidenceUse'} <= {n['label'] for n in before['nodes']})
        self.assertTrue({'RETRIEVED', 'FOR_DECISION', 'FROM_RECEIPT', 'ASSESSED'} <=
                        {e['type'] for e in before['edges']})

    def test_stale_append_and_tampered_receipt_fail_without_journal_mutation(self):
        self.record('finding', {})
        receipt = self.store.retrieve(record_ids=['finding'])
        journal = self.store.root / 'events.jsonl'
        original = journal.read_bytes()
        with self.assertRaises(EvidenceError):
            self.store._append('retrieval', receipt['data'], expected_revision=hashlib.sha256(b'').hexdigest())
        self.assertEqual(journal.read_bytes(), original)
        lines = original.splitlines(keepends=True)
        event = json.loads(lines[-1])
        event['data']['results'][0]['current']['statement'] = 'invented'
        journal.write_bytes(b''.join(lines[:-1]) + (json.dumps(event) + '\n').encode())
        with self.assertRaises(EvidenceError):
            self.store.rebuild()

    def test_non_json_context_keys_cannot_poison_journal(self):
        self.record('finding', {'1': 'a'})
        journal = self.store.root / 'events.jsonl'
        original = journal.read_bytes()
        for context in ({1: 'a'}, {'nested': {1: 'a'}}):
            with self.assertRaises(EvidenceError):
                self.store.retrieve(context=context)
            self.assertEqual(journal.read_bytes(), original)
        self.store.rebuild()

    def test_replay_rejects_boolean_replaced_with_number_in_receipt(self):
        self.record('finding', {'enabled': True})
        self.store.retrieve(context={'enabled': True})
        journal = self.store.root / 'events.jsonl'
        lines = journal.read_bytes().splitlines(keepends=True)
        event = json.loads(lines[-1])
        event['data']['results'][0]['current']['conditions']['enabled'] = 1
        journal.write_bytes(b''.join(lines[:-1]) + (json.dumps(event) + '\n').encode())
        with self.assertRaises(EvidenceError):
            self.store.rebuild()

    def test_concurrent_journal_change_does_not_append_mixed_receipt(self):
        self.record('finding', {})
        append = self.store._append

        def concurrent_append(kind, data, **kwargs):
            other = Store(self.repo, self.store.root, clock=lambda: self.now)
            other.capture('another', 'finding.md', 'document')
            return append(kind, data, **kwargs)

        with patch.object(self.store, '_append', side_effect=concurrent_append):
            with self.assertRaisesRegex(EvidenceError, 'retry'):
                self.store.retrieve(record_ids=['finding'])
        events = [json.loads(line) for line in (self.store.root / 'events.jsonl').read_bytes().splitlines()]
        self.assertNotIn('retrieval', [event['type'] for event in events])
        self.store.rebuild()

    def test_schema_one_index_is_rebuilt_and_invalid_uses_leave_no_events(self):
        finding = self.record('finding', {})
        decision = self.record('decision', {}, kind='decision')
        self.store.rebuild()
        with closing(sqlite3.connect(self.store.root / 'index.sqlite')) as conn, conn:
            conn.execute("UPDATE meta SET value='1' WHERE key='schema'")
            conn.execute('DROP TABLE receipts')
            conn.execute('DROP TABLE uses')
        receipt = self.store.retrieve(record_ids=['finding'])
        journal = self.store.root / 'events.jsonl'
        before = journal.read_bytes()
        selection = dict(revision_id=finding['id'], disposition='applied', reason='observed')
        for receipt_id, decision_id, selections in (
                ('absent', decision['id'], [selection]),
                (receipt['id'], finding['id'], [selection]),
                (receipt['id'], decision['id'], [selection, selection])):
            with self.assertRaises(EvidenceError):
                self.store.use(receipt_id, decision_id, selections)
            self.assertEqual(journal.read_bytes(), before)
        with self.assertRaises(EvidenceError):
            self.store.retrieve(record_ids=['finding'], known_at='2027-01-01T00:00:00Z')
        self.assertEqual(journal.read_bytes(), before)
