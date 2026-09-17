"""Pure fixed-depth decisions using the reviewed certification-count calculator."""
from dataclasses import dataclass
from fractions import Fraction
from math import isfinite

from scripts.certification_power import max_certifying_busts, min_certifying_passes
from .model import PathOutcome, positive_int


@dataclass(frozen=True)
class DecisionRules:
    failure_ceiling: float
    alpha: float
    speed_target: float
    speed_horizon_sessions: int

    def __post_init__(self):
        for value in (self.failure_ceiling,self.alpha,self.speed_target):
            if isinstance(value,bool) or not isfinite(value) or not 0<value<1:
                raise ValueError('finite open-interval decision probabilities required')
        positive_int(self.speed_horizon_sessions,'speed horizon')


@dataclass(frozen=True)
class StageDecision:
    status: str
    failure_counts: tuple[tuple[str,int], ...]
    speed_successes: int | None
    cutoffs: tuple[tuple[str,int], ...]


def adjudicate_stage(run, rules: DecisionRules):
    if type(rules) is not DecisionRules or run.stage not in ('n1','n2','n3'):
        raise ValueError('typed rules and designated stage required')
    if len(run.populations)!=3 or {name for name,_ in run.populations}!={'FULL','H1','H2'}:
        raise ValueError('exact independent population inventory required')
    failures=[]
    cutoffs=[]
    populations=dict(run.populations)
    passed=True
    for name in ('FULL','H1','H2'):
        rows=populations[name]
        if type(rows) is not tuple or not rows or any(type(row) is not PathOutcome for row in rows):
            raise ValueError('complete immutable outcome population required')
        count=sum(row.status!='PASS' for row in rows)
        failures.append((name,count))
        if run.stage=='n1':
            cutoff=int(len(rows)*Fraction(str(rules.failure_ceiling)))
        else:
            cutoff=max_certifying_busts(len(rows),float(rules.failure_ceiling),rules.alpha)
        cutoffs.append((name,cutoff))
        passed &= count<=cutoff
    speed=None
    if run.stage!='n1':
        full=populations['FULL']
        speed=sum(row.status=='PASS' and row.sessions_to_pass<=rules.speed_horizon_sessions for row in full)
        minimum=min_certifying_passes(len(full),rules.speed_target,rules.alpha)
        cutoffs.append(('SPEED',minimum))
        passed &= minimum>=0 and speed>=minimum
    status=('CONTINUE' if run.stage=='n1' else 'PASS') if passed else 'FAILURE'
    return StageDecision(status,tuple(failures),speed,tuple(cutoffs))
