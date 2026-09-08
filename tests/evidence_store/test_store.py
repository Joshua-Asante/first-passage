"""Behavioral checks for the durable evidence/correction boundary (stdlib only)."""
import json
import os
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

from scripts.evidence_store.store import EvidenceError, Store


class StoreTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / 'repo'
        self.repo.mkdir()
        self.root = Path(self.temp.name) / 'evidence'
        self.now = '2026-09-08T12:00:00Z'
        self.store = Store(self.repo, self.root, clock=lambda: self.now)
        self.write('decision.md', '# Decision\n## Ruling\nStatus: parked\n')

    def write(self, path, text):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8')

    def capture(self, source_id='venue:F1', path='decision.md'):
        return self.store.capture(source_id, path, 'document')['version_id']

    def git(self, *args):
        # Hooks export Git repository/index bindings. A fixture must never inherit
        # those bindings or invoke the caller's hooks while creating its own history.
        env = {key: value for key, value in os.environ.items() if not key.startswith('GIT_')}
        return subprocess.run(['git', '-c', 'core.hooksPath=', '-C', str(self.repo), *args],
                              env=env, capture_output=True, check=True, text=True).stdout.strip()

    def test_original_bytes_survive_edit_and_deletion(self):
        version = self.capture()
        original = (self.repo / 'decision.md').read_bytes()
        self.write('decision.md', '# Changed\n')
        result = self.store.source(version)
        self.assertEqual(result['current'], 'changed')
        self.assertEqual(result['preserved'], 'available')
        self.assertEqual(self.store.read_bytes(version), original)
        (self.repo / 'decision.md').unlink()
        self.assertEqual(self.store.source(version)['current'], 'missing')
        self.assertEqual(self.store.read_bytes(version), original)

    def test_repeat_capture_and_rename_keep_version_identity(self):
        first = self.capture()
        self.assertEqual(first, self.capture())
        (self.repo / 'decision.md').rename(self.repo / 'renamed.md')
        self.assertEqual(first, self.capture(path='renamed.md'))
        self.assertEqual(self.store.source(first)['current'], 'unchanged')
        self.assertEqual(self.store.source(first)['current_path'], 'renamed.md')
        self.assertNotEqual(first, self.capture('other:F1', 'renamed.md'))

    def test_unavailable_capture_is_explicit_not_fabricated_content(self):
        missing = self.capture('absent', 'absent.md')
        self.assertEqual(self.store.source(missing)['preserved'], 'missing')
        with self.assertRaises(EvidenceError):
            self.store.read_bytes(missing)

    def test_local_git_capture_preserves_the_named_commit(self):
        git = self.git
        git('init', '-q')
        self.write('docs/record.md', 'tracked source')
        git('add', 'decision.md', 'docs/record.md')
        git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
            '-c', 'commit.gpgsign=false', 'commit', '-qm', 'fixture')
        commit = git('rev-parse', 'HEAD')
        self.write('decision.md', 'working copy changed')
        data = self.store.capture('historical', 'decision.md', 'document', commit=commit)
        self.assertIn(b'Status: parked', self.store.read_bytes(data['version_id']))
        unknown = self.store.capture('unavailable', 'decision.md', 'document', commit='f' * 40)
        self.assertEqual(self.store.source(unknown['version_id'])['preserved'], 'unavailable')
        with self.assertRaises(EvidenceError):
            self.store.capture('directory', 'docs', 'document', commit=commit)

    def test_historical_reader_ignores_callers_git_repository_binding(self):
        self.git('init', '-q')
        self.git('add', 'decision.md')
        self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                 '-c', 'commit.gpgsign=false', 'commit', '-qm', 'fixture')
        commit = self.git('rev-parse', 'HEAD')
        with patch.dict(os.environ, {'GIT_DIR': str(self.repo / 'wrong.git'),
                                     'GIT_INDEX_FILE': str(self.repo / 'wrong.index')}):
            result = self.store.capture('historical', 'decision.md', 'document', commit=commit)
        self.assertEqual(result['availability'], 'available')
        self.assertIn(b'Status: parked', self.store.read_bytes(result['version_id']))

    def test_path_escape_and_invalid_commit_are_rejected(self):
        for path in ['../outside.md', str(self.repo / 'decision.md'), '.git/config', 'a/../../x']:
            with self.subTest(path=path), self.assertRaises(EvidenceError):
                self.capture(path=path)
        with self.assertRaises(EvidenceError):
            self.store.capture('x', 'decision.md', 'document', commit='HEAD:secret')

    def test_torn_journal_is_not_silently_repaired(self):
        version = self.capture()
        self.store.rebuild()
        index_bytes = (self.root / 'index.sqlite').read_bytes()
        with (self.root / 'events.jsonl').open('ab') as handle:
            handle.write(b'{"torn":')
        with self.assertRaises(EvidenceError):
            self.store.source(version)
        self.assertEqual((self.root / 'index.sqlite').read_bytes(), index_bytes)
        self.assertTrue((self.root / 'events.jsonl').read_bytes().endswith(b'{"torn":'))

    def test_blob_corruption_is_not_reported_as_available(self):
        version = self.capture()
        digest = self.store.source(version)['sha256']
        (self.root / 'blobs' / digest).write_bytes(b'corrupted')
        self.assertEqual(self.store.source(version)['preserved'], 'corrupt')
        with self.assertRaises(EvidenceError):
            self.store.read_bytes(version)

    def test_active_writer_lock_fails_without_touching_journal(self):
        self.capture()
        before = (self.root / 'events.jsonl').read_bytes()
        (self.root / 'writer.lock').write_text('another writer')
        with self.assertRaises(EvidenceError):
            self.capture()
        self.assertEqual((self.root / 'events.jsonl').read_bytes(), before)

    def test_invalid_schema_or_sequence_cannot_be_replayed(self):
        self.capture()
        path = self.root / 'events.jsonl'
        event = json.loads(path.read_text())
        for field, value in [('schema', 999), ('seq', 4), ('recorded_at', 'yesterday')]:
            damaged = dict(event, **{field: value})
            path.write_text(json.dumps(damaged) + '\n', encoding='utf-8')
            with self.subTest(field=field), self.assertRaises(EvidenceError):
                self.store.rebuild()

    def record(self, record_id='venue:F1', version=None, **changes):
        data = dict(record_id=record_id, kind='decision', source_version=version or self.capture(),
                    section='## Ruling', statement='Status: parked', status='parked',
                    conditions={'venue': 'example'}, effective_at='2026-08-01T00:00:00Z')
        data.update(changes)
        return self.store.record(**data)

    def test_explicit_revisions_preserve_conditions_and_known_at_history(self):
        first = self.record()
        self.now = '2026-09-09T12:00:00Z'
        self.write('decision.md', '# Decision\n## Ruling\nStatus: admitted\n')
        second = self.record(statement='Status: admitted', status='admitted',
                             supersedes=first['id'], effective_at='2026-09-01T00:00:00Z')
        current = self.store.decision('venue:F1')
        self.assertEqual(current['current']['id'], second['id'])
        self.assertEqual(current['current']['conditions'], {'venue': 'example'})
        self.assertEqual(len(current['history']), 2)
        earlier = self.store.decision('venue:F1', known_at='2026-09-08T23:59:59Z')
        self.assertEqual(earlier['current']['id'], first['id'])
        self.assertEqual(len(earlier['history']), 1)
        effective = self.store.decision('venue:F1', as_of='2026-08-15T00:00:00Z')
        self.assertEqual(effective['current']['id'], first['id'])

    def test_future_and_undated_records_do_not_invent_current_authority(self):
        self.record(effective_at='2030-01-01T00:00:00Z')
        self.assertIsNone(self.store.decision('venue:F1')['current'])
        undated = self.record('other:F1', effective_at=None)
        result = self.store.decision('other:F1')
        self.assertIsNone(result['current'])
        self.assertEqual(result['undated'][0]['id'], undated['id'])
        self.assertIn('unknown_effective_time', result['warnings'])

    def test_conflicting_supersession_is_rejected_without_appending(self):
        first = self.record()
        before = (self.root / 'events.jsonl').read_bytes()
        with self.assertRaises(EvidenceError):
            self.record(version=first['source_version'])
        self.assertEqual((self.root / 'events.jsonl').read_bytes(), before)
        with self.assertRaises(EvidenceError):
            self.record('other:F1', supersedes=first['id'])

    def test_annotation_requires_verbatim_preserved_source_and_real_fields(self):
        version = self.capture()
        for changes in [{'statement': 'invented statement'}, {'section': 'nonexistent section'},
                        {'conditions': []}, {'status': ''}, {'effective_at': 'yesterday'}]:
            with self.subTest(changes=changes), self.assertRaises(EvidenceError):
                self.record(version=version, **changes)
        missing = self.capture('absent', 'missing.md')
        with self.assertRaises(EvidenceError):
            self.record(version=missing)

    def test_dependency_impact_is_transitive_cycle_safe_and_driven_by_bytes(self):
        self.write('data.csv', 'value\n1\n')
        data = self.capture('data', 'data.csv')
        a = self.record('analysis:A')
        b = self.record('analysis:B', version=a['source_version'])
        self.store.depend(consumer=a['id'], dependency=data,
                          evidence_version=a['source_version'], note='input declaration')
        self.store.depend(consumer=b['id'], dependency=a['id'],
                          evidence_version=b['source_version'], note='derived from A')
        self.store.depend(consumer=a['id'], dependency=b['id'],
                          evidence_version=a['source_version'], note='mutual review')
        self.assertEqual({x['record_id'] for x in self.store.impact(data)['dependents']},
                         {'analysis:A', 'analysis:B'})
        self.assertEqual(self.store.check()['findings'], [])
        self.write('data.csv', 'value\n2\n')  # no commit, mtime comparison or index rebuild
        findings = self.store.check()['findings']
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]['status'], 'needs_review')
        self.assertEqual({x['record_id'] for x in findings[0]['dependents']},
                         {'analysis:A', 'analysis:B'})

    def test_unknown_dependencies_and_uncited_declarations_are_rejected(self):
        record = self.record()
        for changes in [{'dependency': 'missing'}, {'consumer': 'missing'},
                        {'evidence_version': 'missing'}, {'note': ''}]:
            data = dict(consumer=record['id'], dependency=record['source_version'],
                        evidence_version=record['source_version'], note='declaration')
            data.update(changes)
            with self.subTest(changes=changes), self.assertRaises(EvidenceError):
                self.store.depend(**data)

    def test_source_drift_and_corruption_are_visible_on_decision_read(self):
        record = self.record()
        self.write('decision.md', '# Revised')
        self.assertIn('source_needs_review', self.store.decision('venue:F1')['warnings'])
        digest = self.store.source(record['source_version'])['sha256']
        (self.root / 'blobs' / digest).write_bytes(b'bad')
        self.assertIn('preserved_source_unavailable', self.store.decision('venue:F1')['warnings'])

    def test_rebuild_and_graph_export_are_deterministic_and_complete(self):
        first = self.record()
        second = self.record(version=first['source_version'], supersedes=first['id'])
        self.store.depend(consumer=second['id'], dependency=first['id'],
                          evidence_version=first['source_version'], note='explicit dependency')
        before = self.store.export()
        self.assertEqual({x['type'] for x in before['edges']},
                         {'VERSION_OF', 'BASED_ON', 'SUPERSEDES', 'DEPENDS_ON'})
        self.assertEqual(len({x['id'] for x in before['nodes']}), len(before['nodes']))
        (self.root / 'index.sqlite').unlink()
        self.store.rebuild()
        self.assertEqual(before, self.store.export())
        self.store.rebuild()
        self.assertEqual(before, self.store.export())

    def test_journal_modification_invalidates_cached_index(self):
        self.record('one:F1')
        before = self.store.export()['revision']
        self.record('two:F1')
        self.assertNotEqual(before, self.store.export()['revision'])
        self.assertEqual(self.store.decision('one:F1')['current']['record_id'], 'one:F1')
        self.assertEqual(self.store.decision('two:F1')['current']['record_id'], 'two:F1')

    def test_git_case_alias_and_symlink_into_git_are_rejected(self):
        self.write('.git/config', 'private configuration')
        with self.assertRaises(EvidenceError):
            self.capture(path='.GIT/config')
        link = self.repo / 'alias'
        try:
            link.symlink_to(self.repo / '.git', target_is_directory=True)
        except OSError:
            return  # Case-alias check above still runs on hosts without symlink privilege.
        with self.assertRaises(EvidenceError):
            self.capture(path='alias/config')

    def test_replay_rejects_fabricated_excerpt_before_replacing_index(self):
        self.record()
        self.store.rebuild()
        before = (self.root / 'index.sqlite').read_bytes()
        journal = self.root / 'events.jsonl'
        events = [json.loads(line) for line in journal.read_text().splitlines()]
        events[-1]['data']['statement'] = 'FABRICATED'
        journal.write_text(''.join(json.dumps(event) + '\n' for event in events), encoding='utf-8')
        with self.assertRaises(EvidenceError):
            self.store.rebuild()
        self.assertEqual((self.root / 'index.sqlite').read_bytes(), before)

    def test_statement_from_another_section_is_not_valid_provenance(self):
        self.write('decision.md', '# Decision\n## Ruling\nStatus: parked\n## Other\nStatus: admitted\n')
        with self.assertRaises(EvidenceError):
            self.record(statement='Status: admitted', status='admitted')

    def test_dependency_declaration_evidence_is_itself_a_review_dependency(self):
        record = self.record()
        self.write('declaration.md', 'Independent input declaration')
        declaration = self.capture('declaration', 'declaration.md')
        self.store.depend(consumer=record['id'], dependency=record['source_version'],
                          evidence_version=declaration, note='input declaration')
        self.write('declaration.md', 'Retracted input declaration')
        affected = self.store.check()['findings'][0]['dependents']
        self.assertEqual([row['record_id'] for row in affected], ['venue:F1'])

    def test_corrupt_index_is_rebuilt_from_the_journal(self):
        record = self.record()
        self.store.rebuild()
        (self.root / 'index.sqlite').write_bytes(b'not a database')
        self.assertEqual(self.store.decision('venue:F1')['current']['id'], record['id'])


if __name__ == '__main__':
    unittest.main()
