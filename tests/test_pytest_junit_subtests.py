"""Real pytest reports retain every outcome without weakening the recorder."""
import json
import os
from pathlib import Path
import subprocess
import sys
import textwrap
import xml.etree.ElementTree as ET

import pytest

from scripts.record_verification import junit_summary

ROOT = Path(__file__).resolve().parents[1]
CASES = [
    ('unittest', '''
        import unittest
        class TestValues(unittest.TestCase):
            def test_values(self):
                for value in range(3):
                    with self.subTest(label="repeated"):
                        if value == 1: self.fail("intentional-failure")
                        if value == 2: self.skipTest("intentional-skip")
        ''', dict(collected=4, passed=2, failed=1, errors=0, skipped=1)),
    ('fixture', '''
        import pytest
        def test_values(subtests):
            for value in range(3):
                with subtests.test(label="repeated"):
                    if value == 1: pytest.fail("intentional-failure")
                    if value == 2: pytest.skip("intentional-skip")
        ''', dict(collected=4, passed=1, failed=2, errors=0, skipped=1)),
    ('teardown', '''
        import pytest
        @pytest.fixture
        def broken():
            yield
            raise RuntimeError("teardown-error")
        def test_values(subtests, broken):
            with subtests.test(label="one"):
                pass
        ''', dict(collected=2, passed=1, failed=0, errors=1, skipped=0)),
    ('parent_and_teardown', '''
        import pytest
        @pytest.fixture
        def broken():
            yield
            raise RuntimeError("teardown-error")
        def test_values(subtests, broken):
            with subtests.test(label="one"):
                pass
            pytest.fail("intentional-failure")
        ''', dict(collected=3, passed=1, failed=1, errors=1, skipped=0)),
]


@pytest.mark.parametrize('workers', [0, 2])
@pytest.mark.parametrize('kind,source,expected', CASES, ids=[case[0] for case in CASES])
def test_complete_outcomes_and_original_reports(tmp_path, workers, kind, source, expected):
    target = tmp_path / 'test_report.py'
    target.write_text(textwrap.dedent(source), encoding='utf-8')
    config = tmp_path / 'pytest.ini'
    config.write_text('[pytest]\n', encoding='utf-8')
    # A second report consumer must still see original parent node IDs. In an
    # xdist run only the controller writes this observation file.
    observation = tmp_path / 'observed.json'
    (tmp_path / 'conftest.py').write_text(
        'import json\nfrom pathlib import Path\n'
        'from _pytest.subtests import SubtestReport\n'
        'reports = []\n'
        'def pytest_runtest_logreport(report):\n'
        '    if isinstance(report, SubtestReport): reports.append(report.nodeid)\n'
        'def pytest_sessionfinish(session):\n'
        '    if not hasattr(session.config, "workerinput"):\n'
        f'        Path({str(observation)!r}).write_text(json.dumps(reports))\n', encoding='utf-8')
    report = tmp_path / 'junit.xml'
    env = os.environ.copy()
    env.pop('PYTEST_ADDOPTS', None)
    result = subprocess.run(
        [sys.executable, '-m', 'pytest', '-p', 'scripts.pytest_junit_subtests',
         '-p', 'no:cacheprovider', '-c', str(config), '--confcutdir', str(tmp_path),
         '--basetemp', str(tmp_path / 'workers'),
         str(target), '-n', str(workers), '--junitxml', str(report),
         '--junitprefix', 'verification', '-o', 'junit_logging=all', '-q'],
        cwd=ROOT, env=env, capture_output=True, text=True, timeout=60, check=False,
    )
    assert result.returncode == 1, result.stdout + result.stderr
    tree = ET.parse(report).getroot()
    assert junit_summary(tree) == expected
    cases = tree.findall('.//testcase')
    names = [case.attrib['name'] for case in cases if 'subtest-' in case.attrib['name']]
    assert len(names) == (3 if kind in ('unittest', 'fixture') else 1)
    assert len(set(names)) == len(names)
    assert all(case.attrib['classname'].startswith('verification.') for case in cases)
    for case in cases:
        if 'subtest-' in case.attrib['name']:
            assert len(case.findall('system-out')) == 1
            assert len(case.findall('system-err')) == 1
    observed = json.loads(observation.read_text())
    assert len(observed) == len(names) and all('subtest-' not in name for name in observed)
    xml = report.read_text(encoding='utf-8')
    if expected['failed']:
        assert 'intentional-failure' in xml
    if expected['errors']:
        assert 'teardown-error' in xml
    if expected['skipped']:
        assert 'intentional-skip' in xml
