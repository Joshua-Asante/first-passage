"""T00 screen verdict: #581 A5 (1)-(3) and A6 by reference (design 2026-10-02 section 5.5, rows V1-V4).

The pre-registration of record is
``docs/briefs/pre-registration/2026-10-01-tradeify-t00-step2-screen-prereg.md``
(#581). Its A5 and A6 sections are pinned by ``A5_TEXT_SHA256`` and
``A6_TEXT_SHA256`` over the spans :func:`section_text` returns (build card #634
section 2.6). A6's thresholds appear only as the exact integer comparisons
``20 * bust <= n`` and ``2 * pass >= n`` (design row G2); row V3 checks that
each compiled constant occurs as a token in the pinned A6 text.

:func:`evaluate` is pure and deterministic: no I/O, clock or draw. Each outcome
is a journal PATH body without its timing fields (card section 3.5): ``key``
(root, population, index), ``bracket_status`` and ``runs``. Only ``runs['r1']``
and ``runs['r2']`` are read, so a labelled R2-P&L/R1-lows hybrid carried
alongside them never enters the verdict (row V4). Each run supplies
``status``, ``sessions_to_pass``, ``failure_reason``, ``kernel_outcome`` and
``consumed_intrabar_split_count``. Malformed input raises ``ValueError``; it
never yields a label.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from types import MappingProxyType

A5_TEXT_SHA256 = 'a8f6f25e025a2e136e477580b7e569531d770a1e35e712b72f5a6b9b50eb391b'
A6_TEXT_SHA256 = 'b3bdc77baf3e6383f1df08afd2f0fbb8a7c930d95a0f56b0c5669a5e18b217d9'
A6_HORIZON_SESSIONS = 1500
A5_RULE_IDS = ('T00_A5/v1',)
MEDIAN_RULE = 'LOWER_NEAREST_RANK_INF_INCLUDED'

# A6 "bust proportion is <= 5.0%" and "P(pass within 1500 sessions) is >= 50%",
# as 20 * bust <= n and 2 * pass >= n (row V3 token-checks both).
_BUST_CEILING_DENOMINATOR = 20
_PASS_FLOOR_DENOMINATOR = 2

_POPULATIONS = ('FULL', 'H1', 'H2')
_ASSIGNMENTS = ('pessimistic', 'optimistic')
_UNDETERMINED = 'UNDETERMINED'
# A5 (1): the headline reasons plus bust_inactivity (unreachable at the runner's barrier).
_BUST_REASONS = frozenset(('bust_daily', 'bust_static', 'bust_trailing', 'bust_inactivity'))
_KERNEL_OUTCOMES = _BUST_REASONS | {'pass', 'horizon_cap'}
_LABELS = ('GO-evidence', 'NO-GO-evidence-robust', 'NO-GO-evidence-UNDETERMINED-dependent')
_SPANS = {'A5': (b'### A5', b'### A6'), 'A6': (b'### A6', '## §3'.encode())}


def section_text(blob: bytes, section: str) -> bytes:
    """The bytes from the start of the section's heading line up to, not including, the next heading line."""
    if section not in _SPANS:
        raise ValueError("section must be 'A5' or 'A6'")
    first, following = _SPANS[section]
    lines = bytes(blob).splitlines(keepends=True)
    starts = [i for i, line in enumerate(lines) if line.startswith(first)]
    if len(starts) != 1:
        raise ValueError(f'{section}: expected exactly one heading line')
    end = next((i for i in range(starts[0] + 1, len(lines)) if lines[i].startswith(b'#')), None)
    if end is None or not lines[end].startswith(following):
        raise ValueError(f'{section}: the next heading line is not the expected one')
    return b''.join(lines[starts[0]:end])


def _frozen(mapping):
    return MappingProxyType(dict(mapping))


@dataclass(frozen=True)
class Insufficient:
    """Row V1: sorted distinct reason codes and completed scored paths per population; no tallies."""

    reasons: tuple[str, ...]
    completed: Mapping[str, int]

    def __post_init__(self):
        reasons = tuple(sorted(set(self.reasons)))
        if not reasons or not all(isinstance(r, str) and r for r in reasons):
            raise ValueError('INSUFFICIENT needs at least one non-empty reason code')
        object.__setattr__(self, 'reasons', reasons)
        object.__setattr__(self, 'completed', _frozen(self.completed))


@dataclass(frozen=True)
class Labelled:
    """A6's label with the A5 counts under both assignments and the descriptive counts (row V4).

    ``tallies``: assignment -> population -> {``bust_numerator``, ``pass_numerator``,
    ``undetermined``, ``denominator``}. ``descriptive``: population ->
    {``consumed_split_paths``, ``undetermined_paths``}; neither has a verdict role.
    """

    label: str
    tallies: Mapping[str, Mapping[str, Mapping[str, int]]]
    descriptive: Mapping[str, Mapping[str, int]]

    def __post_init__(self):
        if self.label not in _LABELS:
            raise ValueError('label must be one of the three A6 labels')
        object.__setattr__(self, 'tallies', _frozen(
            {a: _frozen({p: _frozen(c) for p, c in per.items()}) for a, per in self.tallies.items()}))
        object.__setattr__(self, 'descriptive', _frozen({p: _frozen(c) for p, c in self.descriptive.items()}))


Verdict = Insufficient | Labelled


def as_json(verdict: Verdict) -> dict:
    if isinstance(verdict, Insufficient):
        return {'kind': 'INSUFFICIENT', 'reasons': list(verdict.reasons), 'completed': dict(verdict.completed)}
    if isinstance(verdict, Labelled):
        return {'kind': 'LABELLED', 'label': verdict.label,
                'tallies': {a: {p: dict(c) for p, c in per.items()} for a, per in verdict.tallies.items()},
                'descriptive': {p: dict(c) for p, c in verdict.descriptive.items()}}
    raise TypeError('verdict required')


def _population(outcome, seen) -> str:
    if not isinstance(outcome, Mapping):
        raise ValueError('outcome must be a mapping')
    key = outcome.get('key')
    if (not isinstance(key, (list, tuple)) or len(key) != 3 or not isinstance(key[0], str)
            or key[1] not in _POPULATIONS or type(key[2]) is not int or key[2] < 0):
        raise ValueError('outcome key must be [root, population, path index]')
    if tuple(key) in seen:
        raise ValueError('duplicate outcome key')
    seen.add(tuple(key))
    return key[1]


def _parameters(parameters):
    if not isinstance(parameters, Mapping):
        raise ValueError('parameters mapping required')
    if (list(parameters.get('scenarios') or ()) != ['S0'] or parameters.get('a5_rule') not in A5_RULE_IDS
            or parameters.get('median_rule') != MEDIAN_RULE):
        raise ValueError('scenarios, a5_rule and median_rule must be the compiled values')
    horizon = parameters.get('horizon_sessions')
    if type(horizon) is not int or horizon != A6_HORIZON_SESSIONS:
        raise ValueError('horizon_sessions must equal A6_HORIZON_SESSIONS')
    halves, deadline_only_is_bust = parameters.get('pass_floor_halves'), parameters.get('deadline_only_is_bust')
    if halves not in ('BINDING', 'REPORTED') or type(deadline_only_is_bust) is not bool:
        raise ValueError('pass_floor_halves and deadline_only_is_bust are unset or invalid')
    return horizon, halves == 'BINDING', deadline_only_is_bust


def _run_class(run, horizon):
    """A5 (1): (status, class, pass day or None, consumed split count)."""
    if not isinstance(run, Mapping):
        raise ValueError('run must be a mapping')
    status, day, reason = run.get('status'), run.get('sessions_to_pass'), run.get('failure_reason')
    kernel, splits = run.get('kernel_outcome'), run.get('consumed_intrabar_split_count')
    if type(splits) is not int or splits < 0 or kernel not in _KERNEL_OUTCOMES:
        raise ValueError('run needs its consumed split count and kernel_outcome')
    if status == 'PASS' and type(day) is int and 0 <= day <= horizon and reason is None:
        return status, 'pass', day, splits
    if day is not None:
        raise ValueError('only a PASS run carries sessions_to_pass, inside the horizon')
    if status == 'UNRESOLVED' and reason == 'horizon_cap':
        return status, 'open', None, splits
    if status == 'FAILURE' and reason in _BUST_REASONS:
        return status, 'bust', None, splits
    if status == 'FAILURE' and reason == 'own_flat_deadline':
        return status, 'bust' if kernel in _BUST_REASONS else 'deadline_only', None, splits
    raise ValueError('run status and failure reason are not an A5 (1) class')


def _score(outcome, horizon, deadline_only_is_bust):
    """A5 (2)-(3): ({assignment: (bust, pass day or None)}, undetermined, consumed split)."""
    runs = outcome.get('runs')
    if not isinstance(runs, Mapping):
        raise ValueError('outcome runs must be a mapping with r1 and r2')
    (s1, c1, d1, n1), (s2, c2, d2, n2) = (_run_class(runs.get(r), horizon) for r in ('r1', 'r2'))
    undetermined = s1 != s2
    if outcome.get('bracket_status') != (_UNDETERMINED if undetermined else s1):
        raise ValueError('bracket_status does not follow run agreement')
    if undetermined:
        day = d1 if c1 == 'pass' else d2   # at most one run passed; FAILURE-versus-UNRESOLVED: None
        scored = {'pessimistic': (True, None), 'optimistic': (False, day)}
    else:
        bust = any(c == 'bust' or (c == 'deadline_only' and deadline_only_is_bust) for c in (c1, c2))
        day = max(d1, d2) if s1 == 'PASS' else None
        scored = {a: (bust, day) for a in _ASSIGNMENTS}
    return scored, undetermined, n1 > 0 or n2 > 0


def _lower_median_inf_included(days, n):
    """MEDIAN_RULE: lower nearest-rank median over all n paths, non-passing paths at T = inf."""
    rank = (n - 1) // 2
    return sorted(days)[rank] if rank < len(days) else None


def _go(counts, days, floor):
    """A6 GO-evidence under one assignment: every population's bust ceiling; the pass floor where binding."""
    for p in _POPULATIONS:
        n = counts[p]['denominator']
        if _BUST_CEILING_DENOMINATOR * counts[p]['bust_numerator'] > n:
            return False
        if p in floor and (_PASS_FLOOR_DENOMINATOR * counts[p]['pass_numerator'] < n
                           or _lower_median_inf_included(days[p], n) is None):
            return False
    return True


def evaluate(outcomes: Sequence[Mapping[str, object]], parameters: Mapping[str, object],
             reasons: Sequence[str]) -> Verdict:
    outcomes = tuple(outcomes)   # read twice below (keys first, then scoring); a one-pass iterable is fine
    if isinstance(reasons, (str, bytes)):
        raise ValueError('reasons must be a sequence of codes')
    seen, completed = set(), dict.fromkeys(_POPULATIONS, 0)
    populations = [_population(outcome, seen) for outcome in outcomes]
    for p in populations:
        completed[p] += 1
    if reasons:
        return Insufficient(tuple(reasons), completed)   # row V1: tallies are never read
    horizon, halves_binding, deadline_only_is_bust = _parameters(parameters)
    if not all(completed.values()):
        raise ValueError('a population without scored paths needs an insufficiency reason')
    counts = {a: {p: {'bust_numerator': 0, 'pass_numerator': 0, 'undetermined': 0, 'denominator': completed[p]}
                  for p in _POPULATIONS} for a in _ASSIGNMENTS}
    days = {a: {p: [] for p in _POPULATIONS} for a in _ASSIGNMENTS}
    descriptive = {p: {'consumed_split_paths': 0, 'undetermined_paths': 0} for p in _POPULATIONS}
    for p, outcome in zip(populations, outcomes):
        scored, undetermined, consumed = _score(outcome, horizon, deadline_only_is_bust)
        descriptive[p]['consumed_split_paths'] += consumed
        descriptive[p]['undetermined_paths'] += undetermined
        for a, (bust, day) in scored.items():
            counts[a][p]['bust_numerator'] += bust
            counts[a][p]['undetermined'] += undetermined
            if day is not None:
                counts[a][p]['pass_numerator'] += 1
                days[a][p].append(day)
    floor = _POPULATIONS if halves_binding else ('FULL',)
    if _go(counts['pessimistic'], days['pessimistic'], floor):
        label = 'GO-evidence'
    elif _go(counts['optimistic'], days['optimistic'], floor):
        label = 'NO-GO-evidence-UNDETERMINED-dependent'
    else:
        label = 'NO-GO-evidence-robust'
    return Labelled(label, counts, descriptive)
