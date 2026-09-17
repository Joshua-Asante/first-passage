"""Deterministic synthetic integration workload; never loads market/account data.

Run from repository root with the documented core/ops import roots. Output is
timing and synthetic workload counts only, never a qualification verdict.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
from datetime import date, datetime, time, timedelta, timezone
import hashlib
import json
import random
import platform
from pathlib import Path
from time import perf_counter

from mc.simulation import EvaluationState
from c1_rail.book_policy import candidate_book_protection_policy
from c1_signal_daemon.book_adapters import ADAPTERS
from c1_signal_daemon.book_protocol import OrderIntent, Side, FillTiming
from c1_signal_daemon.feed import Bar
from .model import ET, LEG_IDS, SourceBar, SourceSession, SessionSchedule
from .paths import PathAssembler
from .replay import BookReplay, Instrument
from .runner import evaluate_replay


class SyntheticAdapter:
    """Four explicitly planted trading schedules plus persistent indicator state."""
    def __init__(self, leg_id):
        self.leg_id=leg_id
        self.mode=None
        self.position=0
        self.ema=None
        self.bar_count=0
        self.feedback_count=0

    def set_mode(self, mode):
        self.mode=mode
        return []

    def on_execution(self,event):
        self.feedback_count+=1
        if event.fill:
            self.position+=event.fill.qty*(1 if event.fill.side is Side.BUY else -1)

    def on_bar(self,bar):
        self.bar_count+=1
        self.ema=bar.close if self.ema is None else .07*bar.close+.93*self.ema
        local=bar.ts.astimezone(ET)
        if local.minute!=0:
            return []
        if self.leg_id=='aegis_6j':
            if local.hour in (9,15) and not self.position:
                return [OrderIntent('synthetic-base',self.leg_id,'entry',Side.SELL,8,timing=FillTiming.NEXT_OPEN,bar_time=bar.ts)]
            if local.hour==11 and self.position:
                return [OrderIntent('synthetic-exit',self.leg_id,'exit',Side.BUY,None,timing=FillTiming.THIS_CLOSE,bar_time=bar.ts)]
        elif local.hour==12 and not self.position:
            normal={'dj30_mym_p250':20,'vanguard_mgc':2,'orb_mnq_v7':1}[self.leg_id]
            return [OrderIntent('synthetic-base',self.leg_id,'entry',Side.BUY,normal,timing=FillTiming.THIS_CLOSE,bar_time=bar.ts)]
        elif local.hour==14 and self.position:
            return [OrderIntent('synthetic-add',self.leg_id,'add',Side.BUY,1,timing=FillTiming.THIS_CLOSE,bar_time=bar.ts)]
        return []


class SyntheticQuotes:
    def __call__(self,session,instant,leg):
        return .006 if leg=='aegis_6j' else 100.

    def split_bar(self,session,pb,instant,leg):
        original=dict(pb.bars)[leg]
        price=self(session,instant,leg)
        if not original.open==original.high==original.low==original.close==price:
            raise ValueError('planted schedule bar must be flat')
        return original,Bar(instant,price,price,price,price)


def synthetic_source(day):
    origin=datetime.combine(day-timedelta(days=1),time(18),ET).astimezone(timezone.utc)
    end=datetime.combine(day,time(17),ET).astimezone(timezone.utc)
    deadline=datetime.combine(day,time(16),ET).astimezone(timezone.utc)
    rows=[]
    instant=origin
    while instant<end:
        bars=[]
        for spec in ADAPTERS:
            price=.006 if spec.leg_id=='aegis_6j' else 100.
            spread=0. if instant.astimezone(ET).time()>=time(15,45) else spec.mintick*2
            bars.append((spec.leg_id,Bar(instant,price,price+spread,price-spread,price)))
        rows.append(SourceBar(instant,tuple(bars)))
        instant+=timedelta(minutes=15)
    return SourceSession('synthetic:'+day.isoformat(),day,tuple(rows),
                         SessionSchedule(deadline-timedelta(minutes=15),deadline-timedelta(minutes=5),deadline))


def synthetic_replay(path):
    adapters={leg:SyntheticAdapter(leg) for leg in LEG_IDS}
    instruments={spec.leg_id:Instrument(spec.mintick,spec.pointvalue,spec.pine_slippage_ticks,
                 3.10 if spec.leg_id=='aegis_6j' else spec.pine_commission_per_side,
                 spec.leg_id in ('orb_mnq_v7','dj30_mym_p250')) for spec in ADAPTERS}
    def sizing(leg,action,pb):
        values={'lifecycle_tier':'AUTHORIZED'}
        if leg=='dj30_mym_p250':
            values.update(risk_dollars=700,per_contract_risk=35,cap_alloc=80)
        elif leg=='vanguard_mgc':
            values['normal_base']=2
        return values
    engine=BookReplay(adapters,instruments,policy=candidate_book_protection_policy(),
        initial_state=EvaluationState(100000,100000,100000,0,0),sizing_inputs=sizing,
        schedule_quotes=SyntheticQuotes())
    return engine.run(path)


def benchmark(*, horizon_sessions, seed):
    if type(horizon_sessions) is not int or horizon_sessions<=0 or horizon_sessions%5:
        raise ValueError('benchmark horizon must contain whole five-session blocks')
    sources=tuple(synthetic_source(date(2020,1,6)+timedelta(days=i)) for i in range(5))
    # Planted source session repetition deliberately exercises source/path separation.
    rng=random.Random(seed)
    blocks=tuple(tuple(rng.sample(sources,len(sources))) for _ in range(horizon_sessions//5))
    start=perf_counter()
    path=PathAssembler(date(2020,2,3)).assemble(blocks,horizon_sessions=horizon_sessions)
    result=synthetic_replay(path)
    evaluate_replay(result,initial_state=EvaluationState(100000,100000,100000,0,0))
    canonical=json.dumps(asdict(result),default=str,sort_keys=True,separators=(',',':')).encode()
    elapsed=perf_counter()-start
    root=Path(__file__).resolve().parents[3]
    sources=sorted((root/'ops/c1_rail/qualification').glob('*.py'))
    sources.extend(root/name for name in (
        'ops/c1_rail/book_policy.py','ops/c1_signal_daemon/tv_broker_emulator.py',
        'ops/c1_signal_daemon/book_protocol.py','ops/c1_signal_daemon/pine_ta.py',
        'ops/c1_signal_daemon/book_adapters.py','core/mc/simulation.py','core/mc/preflight.py',
        'core/firm_rules.py','core/dd_geometry.py','core/lifecycle.py','requirements-ops.lock'))
    return {'schema':'synthetic-replay-benchmark/v1','synthetic':True,'seed':seed,
            'sessions':len(result.sessions),'path_bars':sum(len(s.bars) for s in path),
            'adapter_bars':4*sum(len(s.bars) for s in path),'fills':sum(s.fills for s in result.sessions),
            'events':len(result.events),'elapsed_seconds':elapsed,
            'serialized_bytes':len(canonical),'python':platform.python_version(),
            'platform':platform.platform(),'processes':1,
            'source_sha256':{p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
            'equivalence_sha256':hashlib.sha256(canonical).hexdigest()}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--horizon',type=int,required=True)
    parser.add_argument('--seed',type=int,required=True)
    args=parser.parse_args()
    print(json.dumps(benchmark(horizon_sessions=args.horizon,seed=args.seed),sort_keys=True))
