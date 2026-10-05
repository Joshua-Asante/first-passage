#!/usr/bin/env python3
"""Independent T00 screen label recompute (design 2026-10-02 §5.6 ``verify`` step 3; row X5).

Recomputes the step-3 label from the outcome rows alone, by #581 A5 (1)-(3) and A6 as written
(docs/briefs/pre-registration/2026-10-01-tradeify-t00-step2-screen-prereg.md), and imports
nothing from ``c1_rail`` (so nothing from ``t00_screen.verdict``): it is a second, separately
written reading of the same text, which ``t00_screen verify`` compares with ``results.json``.

Input (stdin): canonical JSON ``{"outcomes": [...], "parameters": {...}, "reasons": [...]}``,
where each outcome is a PATH body without timing (``key``, ``runs.r1``/``runs.r2`` with
``status``, ``sessions_to_pass``, ``failure_reason`` and ``kernel_outcome``), ``parameters`` is
the signed authority's ``parameters`` and ``reasons`` the run's insufficiency codes.
Output (stdout): exactly one label: ``INSUFFICIENT``, ``GO-evidence``,
``NO-GO-evidence-robust`` or ``NO-GO-evidence-UNDETERMINED-dependent``. A malformed input
prints ``LABEL_INPUT_INVALID`` on stderr and exits 2.
"""
from __future__ import annotations

import json
import sys

# Exact JSON types are intended: bool is an int subclass.
# pylint: disable=unidiomatic-typecheck

POPULATIONS = ('FULL', 'H1', 'H2')
HEADLINE_BUSTS = ('bust_daily', 'bust_static', 'bust_trailing')  # prereg v2: daily + static + trailing
INFINITY = float('inf')


class LabelInputError(ValueError):
    """The input is not a complete, well-formed outcome set."""


def classify_run(run, deadline_only_is_bust):
    """A5 (1): ('pass', T), 'bust', or 'neither' (deadline-only uncounted, or open)."""
    status, reason = run['status'], run['failure_reason']
    if status == 'PASS':
        if type(run['sessions_to_pass']) is not int:
            raise LabelInputError('a passing run needs its sessions_to_pass')
        return 'pass', run['sessions_to_pass']
    if status == 'UNRESOLVED':
        return 'neither', INFINITY
    if status != 'FAILURE':
        raise LabelInputError(f'unknown run status {status!r}')
    if reason in HEADLINE_BUSTS or reason == 'bust_inactivity':
        return 'bust', INFINITY
    if reason == 'own_flat_deadline':
        if str(run['kernel_outcome']).startswith('bust_') or deadline_only_is_bust:
            return 'bust', INFINITY
        return 'neither', INFINITY
    raise LabelInputError(f'unclassified failure reason {reason!r}')


def path_values(outcome, deadline_only_is_bust):
    """A5 (2)-(3): the path's (bust, T) under the pessimistic and the optimistic assignment."""
    first, second = outcome['runs']['r1'], outcome['runs']['r2']
    one, two = (classify_run(run, deadline_only_is_bust) for run in (first, second))
    if first['status'] == second['status']:  # an agreed path: both assignments read it alike
        if one[0] == 'pass':
            agreed = (False, max(one[1], two[1]))  # the later of the two passing days
        else:
            agreed = ('bust' in (one[0], two[0]), INFINITY)
        return agreed, agreed
    # UNDETERMINED: pessimistic counts it a bust and never a pass; optimistic takes the better
    # outcome one of its runs actually produced (a passing run's day), else neither.
    passing = [value for kind, value in (one, two) if kind == 'pass']
    return (True, INFINITY), (False, passing[0] if passing else INFINITY)


def lower_median(values):
    """LOWER_NEAREST_RANK_INF_INCLUDED: the ceil(n/2)-th smallest, with T = infinity kept."""
    ordered = sorted(values)
    return ordered[(len(ordered) - 1) // 2]


def meets(paths, *, horizon, pass_floor):
    """A6's GO test on one population's (bust, T) values; integer comparisons only."""
    n = len(paths)
    busts = sum(1 for bust, _ in paths if bust)
    if 20 * busts > n:  # bust proportion <= 5.0%
        return False
    if not pass_floor:
        return True
    passes = sum(1 for _, day in paths if day <= horizon)
    median = lower_median([day for _, day in paths])
    return 2 * passes >= n and median <= horizon  # P(pass) >= 50% with a finite median inside H


def _check_input(doc):
    if type(doc) is not dict or set(doc) != {'outcomes', 'parameters', 'reasons'}:
        raise LabelInputError('input fields are outcomes, parameters and reasons')
    params, reasons = doc['parameters'], doc['reasons']
    if type(reasons) is not list or any(type(code) is not str or not code for code in reasons):
        raise LabelInputError('reasons are codes')
    if type(params) is not dict or type(params.get('depth_per_root')) is not dict \
            or type(params.get('rng')) is not dict or type(params.get('horizon_sessions')) is not int:
        raise LabelInputError('parameters lack depth_per_root, rng or horizon_sessions')
    if type(doc['outcomes']) is not list:
        raise LabelInputError('outcomes are a list')


def label(outcomes, parameters, reasons):
    """The A6 label for one complete outcome set; INSUFFICIENT when any reason exists or any
    population is short of its frozen depth (3 roots x depth_per_root)."""
    _check_input({'outcomes': outcomes, 'parameters': parameters, 'reasons': reasons})
    if reasons:
        return 'INSUFFICIENT'
    roots = parameters['rng']['roots']
    keys = [tuple(outcome['key']) for outcome in outcomes]
    if len(set(keys)) != len(keys):
        raise LabelInputError('an outcome key occurs twice')
    expected = {(root, population, index) for root in roots for population in POPULATIONS
                for index in range(parameters['depth_per_root'][population])}
    if set(keys) != expected:
        return 'INSUFFICIENT'  # not every population reached its frozen depth
    deadline = parameters['deadline_only_is_bust']
    horizon = parameters['horizon_sessions']
    halves = parameters['pass_floor_halves'] == 'BINDING'
    pessimistic = {population: [] for population in POPULATIONS}
    optimistic = {population: [] for population in POPULATIONS}
    for outcome in outcomes:
        low, high = path_values(outcome, deadline)
        pessimistic[outcome['key'][1]].append(low)
        optimistic[outcome['key'][1]].append(high)

    def go(assignment):
        return all(meets(assignment[population], horizon=horizon, pass_floor=population == 'FULL' or halves)
                   for population in POPULATIONS)
    if go(pessimistic):
        return 'GO-evidence'
    return 'NO-GO-evidence-robust' if not go(optimistic) else 'NO-GO-evidence-UNDETERMINED-dependent'


def main(stdin=None, stdout=None, stderr=None):
    """Read the input document, print the label; exit 2 on a malformed input."""
    stdin, stdout, stderr = stdin or sys.stdin, stdout or sys.stdout, stderr or sys.stderr
    try:
        doc = json.loads(stdin.read())
        _check_input(doc)
        result = label(doc['outcomes'], doc['parameters'], doc['reasons'])
    except (LabelInputError, ValueError, KeyError, TypeError, IndexError):
        stderr.write('LABEL_INPUT_INVALID\n')
        return 2
    stdout.write(result + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
