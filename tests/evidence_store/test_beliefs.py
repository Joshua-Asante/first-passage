"""Conditional beliefs retain reviewed judgment independently of live checks."""
import json
import tempfile
import unittest
from pathlib import Path

from scripts.evidence_store.store import EvidenceError, Store


class BeliefTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.now = '2026-09-08T10:00:00Z'
        self.store = Store(self.repo, self.repo / '.evidence', clock=lambda: self.now)
        self.context = {'instrument': 'ES'}

    def record(self, name, kind='finding', conditions=None, supersedes=None):
        path = self.repo / (name + '.md')
        path.write_text('# Record\n## Evidence\nObserved claim\n', encoding='utf-8')
        version = self.store.capture(name, path.name, 'document')['version_id']
        return self.store.record(record_id=name, kind=kind, source_version=version,
                                 section='## Evidence', statement='Observed claim',
                                 status='recorded', conditions=self.context if conditions is None else conditions,
                                 effective_at=self.now, supersedes=supersedes)

    def assessment(self, belief, evidence, judgment='supported', supersedes=None, **overrides):
        path = self.repo / 'review.md'
        path.write_text('# Review\n## Judgment\nReviewed the claim against the cited evidence.\n', encoding='utf-8')
        source = self.store.capture('review', path.name, 'review')['version_id']
        kwargs = dict(belief_revision=belief['id'], judgment=judgment, reviewer='fixture reviewer',
                      source_version=source, section='## Judgment',
                      statement='Reviewed the claim against the cited evidence.',
                      evidence=evidence, supersedes=supersedes)
        kwargs.update(overrides)
        return self.store.assess(**kwargs)

    @staticmethod
    def link(record, relationship='supporting', resolution=None):
        return dict(revision_id=record['id'], relationship=relationship,
                    rationale='Reviewed for this conditional claim', resolution=resolution)

    def test_challenges_remain_visible_without_rewriting_judgment(self):
        belief = self.record('belief', 'belief')
        pro = self.record('pro')
        con = self.record('con')
        assessment = self.assessment(belief, [self.link(pro), self.link(con, 'challenging')])
        view = self.store.belief('belief', context=self.context)['belief']
        self.assertEqual(view['judgment'], 'supported')
        self.assertEqual(view['assessment'], assessment)
        self.assertEqual(view['unresolved_challenges'], [con['id']])
        self.assertEqual(view['review_status'], 'needs_review')
        self.assertIn('unresolved_challenges', view['warnings'])

    def test_scope_and_shared_bytes_are_not_independent_votes(self):
        belief = self.record('belief', 'belief')
        first = self.record('first')
        alias = self.record('alias', conditions={'instrument': 'NQ'})
        self.assessment(belief, [self.link(first), self.link(alias, 'scope_limiting')])
        view = self.store.belief('belief', context=self.context)['belief']
        self.assertEqual(len(view['shared_source_groups']), 1)
        self.assertEqual(view['evidence'][1]['applicability']['status'], 'conflicting')
        self.assertIn('evidence_scope_unresolved', view['warnings'])
        self.assertNotIn('confidence', view)

    def test_assessment_history_and_new_belief_revision_do_not_transfer(self):
        belief = self.record('belief', 'belief')
        evidence = self.record('evidence')
        first = self.assessment(belief, [self.link(evidence)])
        self.now = '2026-09-08T11:00:00Z'
        second = self.assessment(belief, [], 'insufficient', first['id'])
        historic = self.store.belief('belief', context=self.context, known_at='2026-09-08T10:30:00Z')
        self.assertEqual(historic['belief']['assessment']['id'], first['id'])
        self.assertEqual(self.store.belief('belief')['belief']['assessment']['id'], second['id'])
        self.now = '2026-09-08T12:00:00Z'
        self.record('belief', 'belief', supersedes=belief['id'])
        self.assertEqual(self.store.belief('belief')['belief']['review_status'], 'unassessed')

    def test_corrections_propagate_through_belief_into_decision(self):
        belief = self.record('belief', 'belief')
        evidence = self.record('evidence')
        decision = self.record('decision', 'decision')
        self.assessment(belief, [self.link(evidence)])
        self.store.depend(consumer=decision['id'], dependency=belief['id'],
                          evidence_version=decision['source_version'], note='uses belief')
        receipt = self.store.retrieve(record_ids=['belief'], context=self.context)
        (self.repo / 'evidence.md').write_text('changed', encoding='utf-8')
        view = self.store.belief('belief', context=self.context)['belief']
        self.assertEqual(view['judgment'], 'supported')
        self.assertEqual(view['review_status'], 'needs_review')
        affected = self.store.impact(evidence['source_version'])['dependents']
        self.assertTrue({belief['id'], decision['id']} <= {r['id'] for r in affected})
        current = self.store.retrieve(record_ids=['decision'])
        self.assertIn('dependencies_need_review', current['data']['results'][0]['warnings'])
        self.assertEqual(self.store.receipt(receipt['id'])['receipt'], receipt)

    def test_replaced_assessment_retires_old_active_dependencies(self):
        belief = self.record('belief', 'belief')
        first = self.record('first')
        second = self.record('second')
        old = self.assessment(belief, [self.link(first)])
        self.assessment(belief, [self.link(second)], supersedes=old['id'])
        self.assertNotIn(belief['id'], {r['id'] for r in self.store.impact(first['source_version'])['dependents']})
        self.assertIn(belief['id'], {r['id'] for r in self.store.impact(second['source_version'])['dependents']})

    def test_belief_checks_ordinary_dependencies_as_well_as_assessment_evidence(self):
        belief = self.record('belief', 'belief')
        evidence = self.record('evidence')
        dependency = self.record('dependency')
        self.assessment(belief, [self.link(evidence)])
        self.store.depend(consumer=belief['id'], dependency=dependency['id'],
                          evidence_version=belief['source_version'], note='additional input')
        (self.repo / 'dependency.md').write_text('changed', encoding='utf-8')
        view = self.store.belief('belief', context=self.context)['belief']
        self.assertEqual(view['review_status'], 'needs_review')
        self.assertIn(dependency['source_version'], {item['id'] for item in view['sources']})

    def test_historical_cycle_does_not_reintroduce_replaced_root_assessment(self):
        belief = self.record('belief', 'belief')
        evidence = self.record('evidence')
        first = self.assessment(belief, [self.link(evidence)])
        self.store.depend(consumer=evidence['id'], dependency=belief['id'],
                          evidence_version=evidence['source_version'], note='cyclic context')
        self.now = '2026-09-08T11:00:00Z'
        replacement = self.record('replacement')
        self.assessment(belief, [self.link(replacement)], supersedes=first['id'])
        (self.repo / 'replacement.md').write_text('changed', encoding='utf-8')
        view = self.store.belief('belief', context=self.context, known_at='2026-09-08T10:30:00Z')['belief']
        self.assertEqual(view['assessment']['id'], first['id'])
        self.assertNotIn(replacement['source_version'], {item['id'] for item in view['sources']})
        self.assertEqual(view['review_status'], 'no_flags')

    def test_duplicate_self_invalid_and_fabricated_reviews_are_rejected(self):
        belief = self.record('belief', 'belief')
        evidence = self.record('evidence')
        link = self.link(evidence)
        for entries, kwargs in [([link, link], {}), ([self.link(belief)], {}),
                                ([], {}), ([link], {'judgment': 'contested'}),
                                ([link], {'statement': 'fabricated'}),
                                ([dict(link, rationale='')], {})]:
            with self.subTest(entries=entries, kwargs=kwargs), self.assertRaises(EvidenceError):
                self.assessment(belief, entries, **kwargs)
        with self.assertRaises(EvidenceError):
            self.assessment(evidence, [self.link(belief)])
        first = self.assessment(belief, [link])
        with self.assertRaises(EvidenceError):
            self.assessment(belief, [link])
        self.assertEqual(self.store.belief('belief')['belief']['assessment']['id'], first['id'])

    def test_graph_and_receipts_rebuild_and_reject_forged_assessment(self):
        belief = self.record('belief', 'belief')
        evidence = self.record('evidence')
        self.assessment(belief, [self.link(evidence)])
        receipt = self.store.retrieve(record_ids=['belief'], context=self.context)
        graph = self.store.export()
        self.assertEqual(graph['schema'], 3)
        self.assertIn('Assessment', {n['label'] for n in graph['nodes']})
        active_types = {'BASED_ON', 'DEPENDS_ON', 'SUPPORTING', 'CHALLENGING', 'SCOPE_LIMITING'}
        affected = {evidence['source_version']}
        while True:
            expanded = affected | {edge['from'] for edge in graph['edges']
                                   if edge['type'] in active_types and edge['to'] in affected}
            if expanded == affected:
                break
            affected = expanded
        graph_records = {node['id'] for node in graph['nodes']
                         if node['label'] == 'RecordRevision' and node['id'] in affected}
        sql_records = {row['id'] for row in self.store.impact(evidence['source_version'])['dependents']}
        self.assertEqual(graph_records, sql_records)
        (self.store.root / 'index.sqlite').unlink()
        self.assertEqual(self.store.export(), graph)
        self.assertEqual(self.store.receipt(receipt['id'])['receipt'], receipt)
        journal = self.store.root / 'events.jsonl'
        lines = journal.read_bytes().splitlines(keepends=True)
        event = json.loads(lines[-1])
        event['data']['results'][0]['belief']['judgment'] = 'contested'
        journal.write_bytes(b''.join(lines[:-1]) + (json.dumps(event) + '\n').encode())
        with self.assertRaises(EvidenceError):
            self.store.rebuild()

    def test_legacy_receipt_is_unchanged_after_beliefs_and_assessments(self):
        finding = self.record('finding')
        self.store.retrieve(record_ids=['finding'])
        journal = self.store.root / 'events.jsonl'
        lines = journal.read_bytes().splitlines(keepends=True)
        legacy = json.loads(lines[-1])
        legacy['schema'] = 2
        for row in legacy['data']['results']:
            row.pop('belief')
        journal.write_bytes(b''.join(lines[:-1]) + (json.dumps(legacy) + '\n').encode())
        belief = self.record('belief', 'belief')
        self.assessment(belief, [self.link(finding)])
        self.store.rebuild()
        self.assertEqual(self.store.receipt(legacy['id'])['receipt'], legacy)

    def test_malformed_record_body_fails_as_integrity_error(self):
        self.record('finding')
        journal = self.store.root / 'events.jsonl'
        lines = journal.read_bytes().splitlines(keepends=True)
        event = json.loads(lines[-1])
        event['data'] = []
        journal.write_bytes(b''.join(lines[:-1]) + (json.dumps(event) + '\n').encode())
        with self.assertRaises(EvidenceError):
            self.store.rebuild()
