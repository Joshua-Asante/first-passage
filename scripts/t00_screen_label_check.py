#!/usr/bin/env python3
"""Independent T00 screen label recompute (design 2026-10-02 §5.6 ``verify`` step 3; row X5).

Recomputes the step-3 label from the outcome rows alone, by #581 A5 (1)-(3) and A6 as written
(docs/briefs/pre-registration/2026-10-01-tradeify-t00-step2-screen-prereg.md), and imports
nothing from ``c1_rail`` (so nothing from ``t00_screen.verdict``): it is a second, separately
written reading of the same text, which ``t00_screen verify`` compares with ``results.json``.

Input (stdin): canonical JSON ``{"outcomes": [...], "parameters": {...}, "reasons": [...]}``,
where each outcome is a PATH body without timing (``key``, ``runs.r1``/``runs.r2`` with
``status``, ``sessions_to_pass``, ``failure_reason`` and ``kernel_outcome``), ``parameters``
is the signed authority's ``parameters`` and ``reasons`` the run's insufficiency codes. The
parameters must carry the compiled rule values with the horizon pinned below, and without a
reason code the outcomes must be exactly the plan's key universe (every root x population x
depth); anything short of that is malformed and never a label.
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
# A5 (1): the three headline busts (prereg v2) plus inactivity, which is also one of the run's
# possible kernel outcomes alongside 'pass' and 'horizon_cap' -- read as exactly those, never
# as a 'bust_' prefix.
BUST_REASONS = ('bust_daily', 'bust_static', 'bust_trailing', 'bust_inactivity')
KERNEL_OUTCOMES = BUST_REASONS + ('pass', 'horizon_cap')
# A6's own numbers and the parameters' compiled rule values, taken from the pinned text here
# and never from the input document: the horizon the pass day and the median are read against.
HORIZON_SESSIONS = 1500
A5_RULE = 'T00_A5/v1'
MEDIAN_RULE = 'LOWER_NEAREST_RANK_INF_INCLUDED'
SCENARIOS = ['S0']
PASS_FLOOR_HALVES = ('BINDING', 'REPORTED')
INFINITY = float('inf')


class LabelInputError(ValueError):
    """The input is not a complete, well-formed outcome set."""


def classify_run(run, deadline_only_is_bust):
    """A5 (1): ('pass', T), 'bust', or 'neither' (deadline-only uncounted, or open)."""
    if type(run) is not dict:
        raise LabelInputError('a run is an object with status, sessions_to_pass, failure_reason, kernel_outcome')
    status, day = run.get('status'), run.get('sessions_to_pass')
    reason, kernel = run.get('failure_reason'), run.get('kernel_outcome')
    if kernel not in KERNEL_OUTCOMES:
        raise LabelInputError(f'kernel_outcome {kernel!r} is not one of the A5 (1) outcomes')
    if status == 'PASS':
        if reason is not None or type(day) is not int or not 0 <= day <= HORIZON_SESSIONS:
            raise LabelInputError('a passing run has no failure reason and 0 <= sessions_to_pass <= 1500')
        return 'pass', day
    if day is not None:
        raise LabelInputError('only a passing run carries its sessions_to_pass')
    if status == 'UNRESOLVED':
        if reason != 'horizon_cap':
            raise LabelInputError('an unresolved run stopped at the horizon cap')
        return 'neither', INFINITY
    if status == 'FAILURE':
        if reason in BUST_REASONS:
            return 'bust', INFINITY
        if reason == 'own_flat_deadline':
            if kernel in BUST_REASONS or deadline_only_is_bust:
                return 'bust', INFINITY
            return 'neither', INFINITY
    raise LabelInputError(f'status {status!r} with failure reason {reason!r} is not an A5 (1) class')


def path_values(outcome, deadline_only_is_bust):
    """A5 (2)-(3): the path's (bust, T) under the pessimistic and the optimistic assignment."""
    runs = outcome.get('runs')
    if type(runs) is not dict or 'r1' not in runs or 'r2' not in runs:
        raise LabelInputError('an outcome carries runs r1 and r2')
    first, second = runs['r1'], runs['r2']
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


def _outcome_keys(outcomes):
    """The outcome rows' plan keys: each a [root, population, index], none twice."""
    keys = []
    for outcome in outcomes:
        if type(outcome) is not dict:
            raise LabelInputError('an outcome is an object with key and runs')
        key = outcome.get('key')
        if not _is_key(key):
            raise LabelInputError('an outcome key is [root, population, path index]')
        keys.append(tuple(key))
    if len(set(keys)) != len(keys):
        raise LabelInputError('an outcome key occurs twice')
    return keys


def _is_key(key):
    if type(key) is not list or len(key) != 3:
        return False
    root, population, index = key
    return type(root) is str and population in POPULATIONS and type(index) is int and index >= 0


def _check_parameters(parameters):
    """The compiled values the signed authority must carry; the horizon comes from A6, not here."""
    if parameters.get('a5_rule') != A5_RULE or parameters.get('median_rule') != MEDIAN_RULE \
            or parameters.get('scenarios') != SCENARIOS:
        raise LabelInputError('a5_rule, median_rule and scenarios must be the compiled values')
    horizon = parameters.get('horizon_sessions')
    if type(horizon) is not int or horizon != HORIZON_SESSIONS:
        raise LabelInputError('horizon_sessions is the A6 horizon, 1500')
    if parameters.get('pass_floor_halves') not in PASS_FLOOR_HALVES:
        raise LabelInputError("pass_floor_halves is 'BINDING' or 'REPORTED'")
    if type(parameters.get('deadline_only_is_bust')) is not bool:
        raise LabelInputError('deadline_only_is_bust is a boolean')
    depths = parameters['depth_per_root']
    if set(depths) != set(POPULATIONS) or any(type(depths[name]) is not int or depths[name] < 1
                                              for name in POPULATIONS):
        raise LabelInputError('depth_per_root is a positive depth for FULL, H1 and H2')
    roots = parameters['rng'].get('roots')
    if not _are_roots(roots):
        raise LabelInputError('rng.roots are distinct non-empty strings')


def _are_roots(roots):
    if type(roots) is not list or not roots or len(set(roots)) != len(roots):
        return False
    return all(type(root) is str and root for root in roots)


def label(outcomes, parameters, reasons):
    """The A6 label for one complete outcome set; INSUFFICIENT only with a stated reason code."""
    _check_input({'outcomes': outcomes, 'parameters': parameters, 'reasons': reasons})
    keys = _outcome_keys(outcomes)
    if reasons:
        return 'INSUFFICIENT'
    _check_parameters(parameters)
    roots = parameters['rng']['roots']
    expected = {(root, population, index) for root in roots for population in POPULATIONS
                for index in range(parameters['depth_per_root'][population])}
    if set(keys) != expected:
        raise LabelInputError('without a reason, the outcomes are exactly the plan key universe')
    deadline = parameters['deadline_only_is_bust']
    halves = parameters['pass_floor_halves'] == 'BINDING'
    pessimistic = {population: [] for population in POPULATIONS}
    optimistic = {population: [] for population in POPULATIONS}
    for outcome in outcomes:
        low, high = path_values(outcome, deadline)
        pessimistic[outcome['key'][1]].append(low)
        optimistic[outcome['key'][1]].append(high)

    def go(assignment):
        return all(meets(assignment[population], horizon=HORIZON_SESSIONS, pass_floor=population == 'FULL' or halves)
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
