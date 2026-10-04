"""Row tests for the T00 screen verdict (design 2026-10-02 rows V1-V4; card #634 section 2.6).

Every outcome row is synthetic: invented statuses, pass days and split counts in
the shape of the journal PATH body (card section 3.5), with no account, P&L or
market value. The only tracked bytes read are the #581 pre-registration's A5 and
A6 sections (row V3), never the real source. Each test imports the module inside
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


def _deadline_only(kernel='pass', splits=0):
    """A5 (1) FAILURE ``own_flat_deadline`` run: a bust if the kernel is a ``bust_*`` status, else deadline-only."""
    return _run('FAILURE', reason='own_flat_deadline', kernel=kernel, splits=splits)


def _agree(rows, population, busts=0, passes=0, open_paths=0):
    """Agreed paths only: ``busts`` busts, ``passes`` passes and ``open_paths`` open, in that order."""
    rows.add(population, _bust(), _bust(), busts).add(population, _pass(), _pass(), passes)
    return rows.add(population, _open(), _open(), open_paths)


def _shaped_book(full=(2, 20, 18), h1=(0, 10, 10), h2=(0, 10, 10), full_extra=()):
    """A 40-path FULL and two 20-path halves from (busts, passes, open) counts per population.

    ``full_extra`` appends one FULL path per (r1, r2) pair; the caller lowers FULL's open count by
    that many, so FULL stays at 40 paths and every population a case does not isolate stays GO-shaped.
    """
    rows = _agree(_Rows(), 'FULL', *full)
    for r1, r2 in full_extra:
        rows.add('FULL', r1, r2)
    return _agree(_agree(rows, 'H1', *h1), 'H2', *h2)


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


def test_V2_pass_floor_full():
    verdict = importlib.import_module(_MODULE)
    # (a) FULL 0 busts, 19 passes and 21 open paths out of 40: no bust and no UNDETERMINED, so the
    # pass floor alone (2 * 19 < 40, and a median at rank 19 with only 19 pass days) decides.
    out = verdict.evaluate(_shaped_book(full=(0, 19, 21)).rows, _parameters(), [])
    full = out.tallies['pessimistic']['FULL']
    assert (full['bust_numerator'], full['pass_numerator'], full['undetermined'],
            full['denominator']) == (0, 19, 0, 40)
    assert out.label == 'NO-GO-evidence-robust'
    # Twin: the 20th pass puts FULL exactly on the floor again.
    assert verdict.evaluate(_shaped_book(full=(0, 20, 20)).rows, _parameters(), []).label == 'GO-evidence'


def test_V2_half_bust_ceiling():
    verdict = importlib.import_module(_MODULE)
    # (b) Every population carries the bust ceiling. H1: 2 busts out of 20 (20 * 2 > 20), pass floor REPORTED.
    over = verdict.evaluate(_shaped_book(h1=(2, 10, 8)).rows, _parameters(), [])
    h1 = over.tallies['pessimistic']['H1']
    assert (h1['bust_numerator'], h1['pass_numerator'], h1['undetermined'], h1['denominator']) == (2, 10, 0, 20)
    assert over.label == 'NO-GO-evidence-robust'
    # Twin: 1 bust out of 20 sits exactly on the 5% ceiling and GO stands.
    assert verdict.evaluate(_shaped_book(h1=(1, 10, 9)).rows, _parameters(), []).label == 'GO-evidence'


def test_V2_binding_halves_floor():
    verdict = importlib.import_module(_MODULE)
    # (c) H1: 9 passes out of 20. Only the pass-floor setting separates the labels; the bust ceiling holds.
    rows = _shaped_book(h1=(0, 9, 11)).rows
    reported = verdict.evaluate(rows, _parameters(), [])
    assert reported.tallies['pessimistic']['H1']['pass_numerator'] == 9
    assert reported.label == 'GO-evidence'
    binding = verdict.evaluate(rows, _parameters(pass_floor_halves='BINDING'), [])
    assert binding.tallies['pessimistic']['H1']['pass_numerator'] == 9
    assert binding.label == 'NO-GO-evidence-robust'


def test_V2_deadline_only_flag():
    verdict = importlib.import_module(_MODULE)
    # (d) FULL: 2 busts, 20 passes, 17 open and one agreed deadline-only path (kernel 'pass') at 40 paths.
    deadline = _deadline_only('pass')
    rows = _shaped_book(full=(2, 20, 17), full_extra=((deadline, deadline),)).rows
    bust = verdict.evaluate(rows, _parameters(deadline_only_is_bust=True), [])
    counted = bust.tallies['pessimistic']['FULL']
    assert (counted['bust_numerator'], counted['denominator']) == (3, 40)
    assert bust.label == 'NO-GO-evidence-robust'      # 20 * 3 > 40
    # Twin: with the flag off the path is in neither numerator, so FULL is back on both thresholds.
    neither = verdict.evaluate(rows, _parameters(deadline_only_is_bust=False), [])
    full = neither.tallies['pessimistic']['FULL']
    assert (full['bust_numerator'], full['pass_numerator'], full['undetermined'],
            full['denominator']) == (2, 20, 0, 40)
    assert neither.label == 'GO-evidence'


def test_V2_deadline_kernel_bust():
    verdict = importlib.import_module(_MODULE)
    # (e) A `bust_*` kernel_outcome is a bust whatever the flag decides about the deadline-only case.
    deadline = _deadline_only('bust_static')
    rows = _shaped_book(full=(2, 20, 17), full_extra=((deadline, deadline),)).rows
    out = verdict.evaluate(rows, _parameters(deadline_only_is_bust=False), [])
    assert out.tallies['pessimistic']['FULL']['bust_numerator'] == 3
    assert out.label == 'NO-GO-evidence-robust'


def test_V2_agreed_bust_with_deadline_run():
    verdict = importlib.import_module(_MODULE)
    # (f) An agreed FAILURE path is a bust if *either* run is a bust: the deadline-only twin run does
    # not dilute it, whatever the flag, and the path stays out of the pass numerator (T = inf).
    rows = _shaped_book(full=(2, 20, 17), full_extra=((_bust(), _deadline_only('pass')),)).rows
    out = verdict.evaluate(rows, _parameters(deadline_only_is_bust=False), [])
    full = out.tallies['pessimistic']['FULL']
    assert (full['bust_numerator'], full['pass_numerator'], full['undetermined'],
            full['denominator']) == (3, 20, 0, 40)
    assert out.label == 'NO-GO-evidence-robust'


def test_V2_bust_ceiling_denominator(monkeypatch):
    verdict = importlib.import_module(_MODULE)
    rows = _go_book(full_busts=2).rows      # FULL: 2 busts out of 40, i.e. exactly 5%
    assert verdict.evaluate(rows, _parameters(), []).label == 'GO-evidence'
    # A ceiling of 2.5% reads the same rows as a robust NO-GO; the halves stay at 0 busts.
    monkeypatch.setattr(verdict, '_BUST_CEILING_DENOMINATOR', 40)
    tighter = verdict.evaluate(rows, _parameters(), [])
    assert tighter.label == 'NO-GO-evidence-robust'
    assert tighter.tallies['pessimistic']['FULL']['bust_numerator'] == 2


def test_evaluate_reads_an_outcomes_iterable_once():
    verdict = importlib.import_module(_MODULE)
    rows = _go_book().rows
    from_generator = verdict.evaluate((row for row in rows), _parameters(), [])
    assert from_generator.label == 'GO-evidence'
    assert verdict.as_json(from_generator) == verdict.as_json(verdict.evaluate(rows, _parameters(), []))


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
    blob = _PREREG.read_bytes().replace(b'\r\n', b'\n')
    a6 = verdict.section_text(blob, 'A6')
    assert hashlib.sha256(a6).hexdigest() == verdict.A6_TEXT_SHA256
    assert hashlib.sha256(verdict.section_text(blob, 'A5')).hexdigest() == verdict.A5_TEXT_SHA256
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
