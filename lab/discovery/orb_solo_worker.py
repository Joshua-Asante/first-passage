"""Fixed single-role read-only study worker. Never invoked without release.

--verify-controls imports the dependencies and tests refusals without loading
study returns, producing admissions or calling a simulation function.
"""
from __future__ import annotations

import csv
import json
import math
import os
from pathlib import Path
import sys

from discovery.orb_solo_release import (
    BoundedText, WorkerPolicy, ReleaseError, DEPTH, MAX_CAPTURE_BYTES, TIERS,
    read_json, file_digest, validate_plan, configuration_of, required_source_paths,
    derive_candidate_admission, validate_admission, validate_reference_route,
    json_ready, canonical,
)


def candidate_context(plan,configuration):
    """Pinned source loader/derivation. Actual invocation is held until admission GO."""
    import numpy as np
    from discovery.orb_solo_series import load_solo_export,build_solo_series
    binding=read_json(configuration['inputs']['binding']['path'])
    if binding['mode']!='NORMAL' or binding['protection']!='OFF' or binding['qty_scale']!=1:
        raise ReleaseError('elected capture configuration drift')
    source=configuration['inputs']['candidate']
    if binding['source_export_sha256']!=source['sha256']:
        raise ReleaseError('binding/export identity mismatch')
    trades=load_solo_export(source['path'],source['sha256'],
            export_tz=binding['source_export_timezone'],
            expected_quantity=binding['resolved_port_parameters']['qty'],
            capture_commission_per_side=binding['capture_emulator_overrides']['commission_per_side'])
    bundle=build_solo_series(trades,expected_quantity=binding['resolved_port_parameters']['qty'],tier_keys=TIERS)
    if [bundle.manifest['window_start'],bundle.manifest['window_end']]!=binding['proposed_complete_week_window']:
        raise ReleaseError('elected complete-week window drift')
    retained=[trade for trade in trades if trade.exit_ny.date() in set(bundle.dates)]
    daily=np.array([math.fsum(trade.gross_usd for trade in retained if trade.exit_ny.date()==day) for day in bundle.dates])
    admission=json_ready(derive_candidate_admission(retained,daily,plan))
    return retained,bundle,daily,admission


def reference_context(configuration):
    """Load the exact accepted already-cost-netted I20 panel; never rebuild it."""
    import numpy as np
    from datetime import date,timedelta
    route=validate_reference_route(configuration)
    entry=configuration['inputs']['reference']
    if entry['sha256']!=route['panel_sha256'] or file_digest(entry['path'])!=route['panel_sha256']:
        raise ReleaseError('reference panel identity drift')
    with Path(entry['path']).open(encoding='utf-8-sig',newline='') as handle:
        reader=csv.DictReader(handle)
        if reader.fieldnames!=['date','striker','striker_nas100','aegis','intraday_low']:
            raise ReleaseError('reference column identity drift')
        rows=list(reader)
    dates=[date.fromisoformat(row['date']) for row in rows]
    first,last=date(2020,1,6),date(2026,7,1)
    expected=[first+timedelta(days=i) for i in range((last-first).days+1) if (first+timedelta(days=i)).weekday()<5]
    if dates!=expected or len(rows)!=1693:
        raise ReleaseError('reference calendar identity drift')
    net=np.array([math.fsum(float(row[key]) for key in ('striker','striker_nas100','aegis')) for row in rows[:1690]])
    low=np.array([float(row['intraday_low']) for row in rows[:1690]])
    if not np.isfinite(net).all() or not np.isfinite(low).all() or (low>0).any():
        raise ReleaseError('invalid pinned reference channels')
    return net,low


def check_depth(report,sidecar,*,phase='candidate',admission=None):
    from firm_rules import FIRM_RULES
    groups=0
    if phase not in ('candidate','reference'):
        raise ReleaseError('unknown depth scope')
    if phase=='candidate' and getattr(getattr(report,'g1',None),'halted',False):
        if (not admission or admission['g1']['halted'] is not True or
                set(admission['tiers'])!=set(TIERS) or
                any(row['g2']['passed'] for row in admission['tiers'].values()) or report.tiers or sidecar):
            raise ReleaseError('unproved candidate G1 early halt')
        return 0
    if set(report.tiers)!=set(TIERS):
        raise ReleaseError('missing frozen tier report')
    eligible=set()
    for key,tier in report.tiers.items():
        if not tier.g3_ok:
            if (phase=='reference' or not admission or
                    admission['tiers'][key]['g2']['passed'] is not False or
                    tier.gated_on!='g2_killed' or key in sidecar):
                raise ReleaseError('non-killed tier missing G3/G4 depth')
            continue
        eligible.add(key)
        evidence=sidecar.get(key,{})
        arms=evidence.get('guard_arms',{})
        if set(arms)!={'eod','zeros','real'}:
            raise ReleaseError('missing mandatory guard arm')
        for arm in arms.values():
            if arm.get('sims_per_seed')!=10000 or arm.get('n_seeds')!=3:
                raise ReleaseError('guard depth incomplete')
        required={'run1','run2'}
        if set(evidence.get('days_to_pass',{}))!=required or any(evidence['days_to_pass'][run].get('n')!=30000 for run in required):
            raise ReleaseError('gating-run depth incomplete')
        if not FIRM_RULES[key].get('consistency_rule_pct'):
            if evidence['days_to_pass']['run2']!=evidence['days_to_pass']['run1']:
                raise ReleaseError('Bulenox Run2 must alias Run1 without extra simulation')
            groups+=4
        else:
            groups+=5
    if set(sidecar)!=eligible or (phase=='reference' and groups!=19):
        raise ReleaseError('phase depth evidence incomplete')
    return groups


def verify_loaded_sources(plan,root):
    allowed=set(plan['source_pins'])
    for module in list(sys.modules.values()):
        name=getattr(module,'__file__',None)
        if not name:
            continue
        path=Path(name).resolve()
        if path.is_relative_to(root) and path.parts[len(root.parts)] in ('core','lab','scripts'):
            if str(path) not in allowed:
                raise ReleaseError('unbound executed module: '+path.name)


def evaluate_phase(plan,configuration,*,plan_sha256=None):
    """Fixed candidate/reference routing, separately testable without a kernel run."""
    from discovery.prop_survivor_scoring import (
        DEFAULT_PREREG,score_candidate,load_scoring_thresholds,TierSeries,discharges_falsifier,
    )
    from discovery.orb_solo_release import digest
    # S4 froze under v2 alone, matching the admission derivation and source pins.
    thresholds=load_scoring_thresholds(DEFAULT_PREREG)
    if (list(thresholds.seeds)!=DEPTH['seeds'] or thresholds.horizon!=1500 or
            thresholds.sims_per_seed!=10000 or tuple(thresholds.tier_keys)!=TIERS):
        raise ReleaseError('frozen depth/tier drift')
    sidecar={}
    admission=None
    if plan['phase']=='candidate':
        trades,bundle,daily,derived=candidate_context(plan,configuration)
        admission=read_json(configuration['inputs']['candidate_admission']['path'],limit=2*1024**2)
        validate_admission(admission,plan,derived=derived)
        report=score_candidate(strategy_label=plan['study'],candidate_daily_pnl=daily,
            full_res_trades=[trade.gross_usd for trade in trades],
            envelope_verdict=derived['g1']['deployable_default_envelope'],thresholds=thresholds,
            gross_edge_usd=math.fsum(trade.gross_usd for trade in trades),
            tier_series={key:TierSeries(daily_pnl=bundle.tiers[key]['pnl'],intraday_low=bundle.tiers[key]['low']) for key in TIERS},
            sidecar=sidecar)
    elif plan['phase']=='reference':
        pnl,low=reference_context(configuration)
        # Only the explicitly frozen historical bust-only reference route may
        # bypass candidate G1/G2; it never manufactures candidate admission.
        report=score_candidate(strategy_label='I20-bust-only-reference',candidate_daily_pnl=pnl,
            full_res_trades=[],envelope_verdict='YES',gross_edge_usd=float('inf'),
            thresholds=thresholds,intraday_low=low,sidecar=sidecar)
    else:
        raise ReleaseError('unknown population')
    group_count=check_depth(report,sidecar,phase=plan['phase'],admission=admission)
    excluded={} if admission is None else {key:value['clock_cap']['reason'] for key,value in admission['tiers'].items() if not value['clock_cap']['admissible'] or not value['g2']['passed']}
    admitted={key:tier for key,tier in report.tiers.items() if key not in excluded}
    return json_ready(dict(schema='orb-s4-phase-result/v1',phase_status='completed',
        phase=plan['phase'],plan_sha256=plan_sha256 or digest(plan),depth=DEPTH,groups_completed=group_count,
        report=report.to_dict(),sidecar=sidecar,admission=admission,
        excluded_candidate_tiers=excluded,
        admitted_candidate_clear_tiers=[key for key,tier in admitted.items() if tier.clears_part_a] if admission else [],
        admitted_discharges_falsifier=bool(admission and report.gate_grade and discharges_falsifier(admitted,thresholds)),
        public_result_policy='raw engine report is diagnostic; withhold excluded tier G4 figures; use admitted clear flags'))


def main(argv=None):
    argv=sys.argv[1:] if argv is None else argv
    root=Path(__file__).resolve().parents[2]
    sys.dont_write_bytecode=True
    sys.stdout,sys.stderr=BoundedText(sys.stdout),BoundedText(sys.stderr,limit=64*1024)
    if argv==['--verify-controls']:
        policy=WorkerPolicy(required_source_paths(root))
        sys.addaudithook(policy)
        import numpy
        import discovery.prop_survivor_scoring
        import socket
        import subprocess
        assert isinstance(socket.gethostname(),str)
        denied=0
        for operation in (lambda:socket.socket(),
                lambda:subprocess.Popen([sys.executable,'-c','pass']),
                lambda:os.system('exit 99'),
                lambda:(root/'FORBIDDEN-ORB-WRITE').write_text('must not exist')):
            try:
                operation()
            except ReleaseError:
                denied+=1
            else:
                raise ReleaseError('prohibited control operation succeeded')
        print(json.dumps(dict(imports_ok=True,denials_verified=denied,qualification_groups=0)))
        return 0
    if len(argv)!=2:
        raise ReleaseError('exact pinned plan and SHA required')
    path=Path(argv[0]).resolve(); expected=argv[1]
    if file_digest(path)!=expected:
        raise ReleaseError('worker plan identity mismatch')
    plan=read_json(path); validate_plan(plan)
    configuration=configuration_of(plan)
    pins=dict(plan['source_pins'])
    for entry in configuration['inputs'].values():
        pins[str(Path(entry['path']).resolve())]=entry['sha256']
    pins[str(path)]=expected
    sys.addaudithook(WorkerPolicy(pins))
    from discovery.prop_survivor_scoring import score_candidate,load_scoring_thresholds,TierSeries
    verify_loaded_sources(plan,root)
    for source,digest in pins.items():
        if file_digest(source)!=digest:
            raise ReleaseError('worker observed input/source drift')
    rules=read_json(configuration['inputs']['rules']['path'])
    from firm_rules import FIRM_RULES
    from discovery.orb_solo_release import digest
    if rules['rows']!={key:FIRM_RULES[key] for key in TIERS}:
        raise ReleaseError('canonical tier rows differ from admission binding')
    payload=evaluate_phase(plan,configuration,plan_sha256=expected)
    data=canonical(payload)
    if len(data)>MAX_CAPTURE_BYTES:
        raise ReleaseError('phase output exceeds capture allowance')
    sys.stdout.write(data.decode('utf-8'))
    return 0


if __name__=='__main__':
    raise SystemExit(main())
