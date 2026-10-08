"""scripts/t00_tier1_diagnostic.py (T00 step-12 diagnostic, Tier 1 card §0.5, §3, §5).

The load-bearing claim is that identities computed from a sealed ``replay_bracket`` run equal
the ones the screen worker wrote from the raw run, so a mismatch at replay means a
non-reproduction and not a driver defect. No real source is read here.
"""
from __future__ import annotations

from datetime import date, datetime
import hashlib
import importlib.util
from pathlib import Path
from types import SimpleNamespace

import pytest

from c1_rail.qualification.contract import canonical_json_bytes as canonical
from c1_rail.qualification.model import LEG_IDS, EdgeState, PathOutcome, ReplayEvent, ReplayResult, SessionRecord
from c1_rail.qualification.p7_evidence import canonical as p7_canonical, sha256_bytes
from c1_rail.qualification.production_source import _consumed_splits, _seal
from c1_rail.qualification.t00_screen import worker

SCRIPT = Path(__file__).resolve().parents[3] / 'scripts' / 't00_tier1_diagnostic.py'


def _driver():
    spec = importlib.util.spec_from_file_location('t00_tier1_diagnostic', SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _edge(held=0):
    positions = tuple((leg, held if i == 0 else 0) for i, leg in enumerate(LEG_IDS))
    zeros = tuple((leg, 0) for leg in LEG_IDS)
    return EdgeState(positions, zeros, zeros)


def _result():
    sessions = (
        SessionRecord(0, date(2022, 9, 1), 's-a', 125.5, -40.25, 3, True, _edge(), _edge(1)),
        SessionRecord(1, date(2022, 9, 2), 's-b', -0.1, -310.0, 0, False, _edge(1), _edge()),
    )
    events = (ReplayEvent(datetime(2022, 9, 1, 10, 7), 'fill', LEG_IDS[0], '{"qty":1}'),
              ReplayEvent(datetime(2022, 9, 2, 15, 0), 'session_mode', '', 'normal'))
    return ReplayResult(sessions, events)


@pytest.mark.parametrize('failed', [False, True])
def test_sealed_identity_equals_worker_projection(failed):
    result = _result()
    provider = SimpleNamespace(_placed=[(1, LEG_IDS[1], datetime(2022, 9, 2, 10, 7, 30)),
                                        (0, LEG_IDS[0], datetime(2022, 9, 1, 9, 45)),  # grid instant: not a split
                                        (0, LEG_IDS[2], datetime(2022, 9, 1, 11, 3))])
    contract = SimpleNamespace(evidence_class='T00_STEP3_SCREEN', contract_sha256='0' * 64,
                               approval=SimpleNamespace(approval_sha256='1' * 64))
    sealed = _seal(contract, result, provider=provider, deadline_failure=failed)
    outcome = PathOutcome('PASS', 1, None, (('kernel_outcome', 'pass'),))
    expected = worker.run_projection(result, failed, _consumed_splits(provider), outcome)
    got = _driver().sealed_identity(sealed, p7_canonical, sha256_bytes)
    assert {field: expected[field] for field in got} == got
    assert set(got) == set(_driver().COMPARED)


def test_mismatches_names_each_differing_field():
    driver = _driver()
    runs = {name: {field: 0 for field in driver.COMPARED} for name in ('r1', 'r2')}
    replayed = {name: dict(fields) for name, fields in runs.items()}
    assert driver.mismatches(runs, replayed) == []
    replayed['r2']['events_sha256'] = 1
    assert driver.mismatches(runs, replayed) == ['r2.events_sha256']


def _outcome(root, population, index, status):
    return {'key': [root, population, index], 'bracket_status': status}


def test_select_keys_rule():
    driver = _driver()
    outcomes = [_outcome(r, p, i, s) for r in ('a', 'b') for p in driver.POPULATIONS for i in range(3)
                for s in ('PASS',) if not (p == 'H2')]
    outcomes += [_outcome('a', 'FULL', 10 + i, 'FAILURE') for i in range(5)]
    outcomes += [_outcome('a', 'H1', 20, 'UNDETERMINED')]        # a stratum with one path
    outcomes += [_outcome('a', 'FULL', 30, 'UNRESOLVED')]        # not a sampled class
    keys, available = driver.select_keys(outcomes, canonical)
    by_hash = sorted([('a', 'FULL', 10 + i) for i in range(5)],
                     key=lambda k: hashlib.sha256(canonical(list(k))).hexdigest())
    assert keys[:2] == by_hash[:2]                                # checkpoint stratum first, hash order
    assert ('a', 'H1', 20) in keys                                # shortfall: all it has, no substitution
    assert all(k[1] != 'H2' for k in keys) and ('a', 'FULL', 30) not in keys
    assert available['H2|PASS'] == 0 and available['H1|UNDETERMINED'] == 1
    assert len(keys) == 2 + 2 + 2 + 1                             # FULL/FAILURE, FULL/PASS, H1/PASS, H1/UNDETERMINED


def test_outputs_are_create_once(tmp_path):
    driver = _driver()
    driver._write_once(tmp_path / 'k' / 'keys.json', b'x')
    with pytest.raises(FileExistsError):
        driver._write_once(tmp_path / 'k' / 'keys.json', b'y')


def test_imports_nothing_outside_the_standard_library_at_module_level():
    """The H modules are imported only by _modules(code_root), after the code root is on sys.path."""
    import ast
    tree = ast.parse(SCRIPT.read_text(encoding='utf-8'))
    top = [node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))]
    names = {alias.name.split('.')[0] for node in top for alias in node.names} | {
        (node.module or '').split('.')[0] for node in top if isinstance(node, ast.ImportFrom)}
    assert not names & {'c1_rail', 'mc', 'core', 'ops'}
