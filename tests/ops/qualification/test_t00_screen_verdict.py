"""Row tests for the T00 screen verdict (design 2026-10-02 rows V1-V4; card #634 section 2.6).

Every outcome row is synthetic: invented statuses, pass days and split counts in
the shape of the journal PATH body (card section 3.5), with no account, P&L or
market value. The only tracked bytes read are the #581 pre-registration's A6
section (row V3), never the real source. Each test imports the module inside
its own body, so each row fails on its own while the module is absent.
"""
from __future__ import annotations

import hashlib
import importlib
import re
from fractions import Fraction
from pathlib import Path

_MODULE = 'c1_rail.qualification.t00_screen.verdict'
_PREREG = (Path(__file__).resolve().parents[3]
           / 'docs/briefs/pre-registration/2026-10-01-tradeify-t00-step2-screen-prereg.md')


def _parameters(**overrides):
    return {'scenarios': ['S0'], 'horizon_sessions': 1500, 'pass_floor_halves': 'REPORTED',
            'deadline_only_is_bust': True, 'a5_rule': 'T00_A5/v1',
            'median_rule': 'LOWER_NEAREST_RANK_INF_INCLUDED', **overrides}


def _run(status, *, day=None, reason=None, kernel=None, splits=0):
    return {'status': status, 'sessions_to_pass': day, 'failure_reason': reason,
            'kernel_outcome': kernel, 'consumed_intrabar_split_count': splits}


def _pass(day=10, splits=0):
    return _run('PASS', day=day, kernel='pass', splits=splits)


def _bust(reason='bust_daily', splits=0):
    return _run('FAILURE', reason=reason, kernel=reason, splits=splits)


def _open(splits=0):
    return _run('UNRESOLVED', reason='horizon_cap', kernel='horizon_cap', splits=splits)


class _Rows:
    """Synthetic PATH bodies (card section 3.5) with distinct keys (root, population, index)."""

    def __init__(self):
        self.rows, self._next = [], {}

    def add(self, population, r1, r2, count=1):
        for _ in range(count):
            index = self._next.get(population, 0)
            self._next[population] = index + 1
            status = r1['status'] if r1['status'] == r2['status'] else 'UNDETERMINED'
            self.rows.append({'key': ['root-a', population, index], 'seed': index, 'path_sha256': '0' * 64,
                              'bracket_status': status, 'runs': {'r1': r1, 'r2': r2}})
        return self


def _halves(rows):
    """H1 and H2: 20 paths each, no bust, 10 passes (the pass floor is REPORTED on halves)."""
    for population in ('H1', 'H2'):
        rows.add(population, _pass(), _pass(), 10).add(population, _open(), _open(), 10)
    return rows


def _go_book(full_busts=2):
    """FULL: 40 paths, ``full_busts`` busts and 20 passes (exactly 50%)."""
    rows = _Rows().add('FULL', _bust(), _bust(), full_busts).add('FULL', _pass(), _pass(), 20)
    return _halves(rows.add('FULL', _open(), _open(), 20 - full_busts))


def test_V1():
    verdict = importlib.import_module(_MODULE)
    rows = _go_book().rows
    # Reasons plus tallies that would give GO: INSUFFICIENT with sorted distinct codes and
    # completed counts per population only; parameters and tallies are never read.
    out = verdict.evaluate(rows, {}, ['PROBE_INCOMPLETE', 'BUDGET_EXHAUSTED', 'PROBE_INCOMPLETE'])
    assert type(out) is verdict.Insufficient
    assert out.reasons == ('BUDGET_EXHAUSTED', 'PROBE_INCOMPLETE')
    assert dict(out.completed) == {'FULL': 40, 'H1': 20, 'H2': 20}
    assert verdict.as_json(out) == {'kind': 'INSUFFICIENT', 'reasons': ['BUDGET_EXHAUSTED', 'PROBE_INCOMPLETE'],
                                    'completed': {'FULL': 40, 'H1': 20, 'H2': 20}}
    # Twin: no reasons, the same rows are labelled.
    twin = verdict.evaluate(rows, _parameters(), [])
    assert type(twin) is verdict.Labelled and twin.label == 'GO-evidence'
    assert set(verdict.as_json(twin)) == {'kind', 'label', 'tallies', 'descriptive'}


def test_V2():
    verdict = importlib.import_module(_MODULE)
    exact = verdict.evaluate(_go_book(full_busts=2).rows, _parameters(), [])
    full = exact.tallies['pessimistic']['FULL']
    assert 20 * full['bust_numerator'] == full['denominator'] == 40      # bust exactly 5%
    assert 2 * full['pass_numerator'] == full['denominator']             # pass exactly 50%
    assert exact.label == 'GO-evidence'
    # Twins: one bust either side of 5%.
    assert verdict.evaluate(_go_book(full_busts=1).rows, _parameters(), []).label == 'GO-evidence'
    assert verdict.evaluate(_go_book(full_busts=3).rows, _parameters(), []).label == 'NO-GO-evidence-robust'
    # UNDETERMINED stays in every denominator; the pessimistic assignment decides GO and the
    # optimistic one labels the NO-GO. FULL: 2 busts, 19 passes, 18 open, 1 PASS-versus-bust.
    rows = _Rows().add('FULL', _bust(), _bust(), 2).add('FULL', _pass(), _pass(), 19)
    rows = _halves(rows.add('FULL', _open(), _open(), 18).add('FULL', _pass(12), _bust()))
    dependent = verdict.evaluate(rows.rows, _parameters(), [])
    for assignment, busts, passes in (('pessimistic', 3, 19), ('optimistic', 2, 20)):
        counts = dependent.tallies[assignment]['FULL']
        assert (counts['bust_numerator'], counts['pass_numerator'], counts['undetermined'],
                counts['denominator']) == (busts, passes, 1, 40)
    assert dependent.label == 'NO-GO-evidence-UNDETERMINED-dependent'


def _token_failures(verdict, a6_text):
    """Names of compiled verdict constants that do not occur as a token in the A6 text."""
    integers = set(re.findall(r'(?<![\d.])\d+(?![\d.%])', a6_text))
    percents = {Fraction(token) for token in re.findall(r'(?<![\d.])(\d+(?:\.\d+)?)%', a6_text)}
    failures = [] if str(verdict.A6_HORIZON_SESSIONS) in integers else ['A6_HORIZON_SESSIONS']
    for name in ('_BUST_CEILING_DENOMINATOR', '_PASS_FLOOR_DENOMINATOR'):   # 20*bust <= n, 2*pass >= n
        if Fraction(100, getattr(verdict, name)) not in percents:
            failures.append(name)
    return failures


def test_V3(monkeypatch):
    verdict = importlib.import_module(_MODULE)
    a6 = verdict.section_text(_PREREG.read_bytes(), 'A6')
    assert hashlib.sha256(a6).hexdigest() == verdict.A6_TEXT_SHA256
    assert (verdict._BUST_CEILING_DENOMINATOR, verdict._PASS_FLOOR_DENOMINATOR) == (20, 2)
    assert _token_failures(verdict, a6.decode('utf-8')) == []
    # Violating case: one constant changed fails the token check.
    for name in ('A6_HORIZON_SESSIONS', '_BUST_CEILING_DENOMINATOR', '_PASS_FLOOR_DENOMINATOR'):
        with monkeypatch.context() as patch:
            patch.setattr(verdict, name, getattr(verdict, name) + 1)
            assert _token_failures(verdict, a6.decode('utf-8')) == [name]


def test_V4():
    verdict = importlib.import_module(_MODULE)
    # FULL: 10 paths, no agreed bust, 5 passes (two with a consumed split), 4 open and one
    # UNDETERMINED path (R1 open, R2 PASS) that the pessimistic assignment counts as a bust.
    rows = _Rows().add('FULL', _pass(splits=1), _pass(), 2).add('FULL', _pass(), _pass(), 3)
    rows = _halves(rows.add('FULL', _open(), _open(), 4).add('FULL', _open(), _pass(splits=2)))
    clean = verdict.evaluate(rows.rows, _parameters(), [])
    assert clean.label == 'NO-GO-evidence-UNDETERMINED-dependent'     # pessimistic 20*1 > 10
    assert dict(clean.descriptive['FULL']) == {'consumed_split_paths': 3, 'undetermined_paths': 1}
    assert dict(clean.descriptive['H1']) == dict(clean.descriptive['H2']) == \
        {'consumed_split_paths': 0, 'undetermined_paths': 0}
    # A labelled R2-P&L/R1-lows hybrid carried in each row never enters the verdict, even
    # where counting it as a run would settle the UNDETERMINED path.
    hybrid_rows = [dict(row, runs=dict(row['runs'], hybrid=_pass(splits=1))) for row in rows.rows]
    assert verdict.as_json(verdict.evaluate(hybrid_rows, _parameters(), [])) == verdict.as_json(clean)
    # The descriptive counts have no verdict role: more consumed splits change only them.
    split_rows = [dict(row, runs={k: dict(v, consumed_intrabar_split_count=1) for k, v in row['runs'].items()})
                  for row in rows.rows]
    split = verdict.evaluate(split_rows, _parameters(), [])
    assert (split.label, verdict.as_json(split)['tallies']) == (clean.label, verdict.as_json(clean)['tallies'])
    assert dict(split.descriptive['H1']) == {'consumed_split_paths': 20, 'undetermined_paths': 0}
