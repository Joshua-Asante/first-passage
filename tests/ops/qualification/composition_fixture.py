"""Synthetic retained-byte fixture. No production authority or private inputs."""
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
import hashlib
import json

from c1_rail.qualification.contract import REQUIRED_ARTIFACT_ROLES, ACCEPTED_HISTORICAL_PINS
from c1_rail.qualification.model import ET, LEG_IDS


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


PORT_ROLES = dict(zip(LEG_IDS, ('aegis_runtime_port','striker_runtime_port','vanguard_runtime_port','orb_runtime_port')))


def port_bytes(leg, pine_sha256, *, idle=False):
    return f'''# Explicit synthetic composition fixture; no accepted production identity.
from types import SimpleNamespace
from zoneinfo import ZoneInfo
from c1_signal_daemon.book_protocol import OrderIntent, Side, FillTiming
LEG_ID = {leg!r}
PINE_SHA256 = {pine_sha256!r}
class Adapter:
    def __init__(self, mode, **settings):
        self.leg_id = LEG_ID
        self.params = SimpleNamespace(**settings)
        self.mode = mode
        self.position = 0
        self.bar_count = 0
    def set_mode(self, mode):
        self.mode = mode
        return []
    def on_execution(self, event):
        if event.fill:
            self.position += event.fill.qty * (1 if event.fill.side is Side.BUY else -1)
    def on_bar(self, bar):
        self.bar_count += 1
        if {idle!r} or LEG_ID != 'orb_mnq_v7':
            return []
        local = bar.ts.astimezone(ZoneInfo('America/New_York'))
        if local.hour == 9 and local.minute == 0 and not self.position:
            return [OrderIntent('fixture-entry', LEG_ID, 'entry', Side.BUY, 1, timing=FillTiming.THIS_CLOSE, bar_time=bar.ts)]
        if local.hour == 9 and local.minute == 15 and self.position:
            return [OrderIntent('fixture-exit', LEG_ID, 'exit', Side.SELL, None, timing=FillTiming.THIS_CLOSE, bar_time=bar.ts)]
        return []
def build(*, mode, **settings):
    return Adapter(mode, **settings)
'''.encode()


@dataclass(frozen=True)
class ArtifactFixture:
    payloads: dict
    paths: dict
    populations: dict
    source_binding: dict
    pine_sha256: dict
    ordinary_modules: tuple = ()

    def identity_fields(self):
        """Input to the separate signed test profile; this grants no trust."""
        return {
            'accepted_historical_pins':{role:digest(self.payloads[role]) for role in ACCEPTED_HISTORICAL_PINS},
            'required_artifact_roles':sorted(self.payloads),
            'port_runtime_pins':{leg:{'runtime_sha256':digest(self.payloads[PORT_ROLES[leg]]),
                                      'pine_sha256':self.pine_sha256[leg]} for leg in LEG_IDS},
            'effective_settings_sha256':digest(self.payloads['effective_settings_successor']),
        }

    def with_runtime_artifacts(self, root):
        from runtime_fixture import ordinary_runtime_fixture
        roles={'qualification_runner':'c1_rail.qualification.orchestration',
               'replay_kernel':'c1_rail.qualification.replay','path_sampler':'c1_rail.qualification.paths',
               'rng_allocation':'c1_rail.qualification.regime','part_a_runner':'c1_rail.qualification.part_a',
               'qualification_adjudicator':'c1_rail.qualification.result_adjudication',
               'qualification_sealer':'c1_rail.qualification.seal',
               'listener_account_owner':'c1_rail.book_account_owner',
               'qualification_adjudication_rules':'c1_rail.qualification.adjudication',
               'qualification_model':'c1_rail.qualification.model',
               'qualification_certification_power':'scripts.certification_power'}
        modules=ordinary_runtime_fixture(role_modules=roles)
        payloads=dict(self.payloads);paths=dict(self.paths)
        for row in modules:
            payloads[row.role]=row.source_bytes;paths[row.role]=row.path
            path=root/row.path;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(row.source_bytes)
        return ArtifactFixture(payloads,paths,self.populations,self.source_binding,self.pine_sha256,modules)


def build_artifacts(root, *, idle=False):
    payloads = {role:encoded({'synthetic_fixture':role}) for role in REQUIRED_ARTIFACT_ROLES}
    pine = {leg:digest(('synthetic-pine:'+leg).encode()) for leg in LEG_IDS}
    for leg in LEG_IDS:
        payloads[PORT_ROLES[leg]]=port_bytes(leg,pine[leg],idle=idle)
    days=[]
    current=date(2024,1,2)
    while current<date(2024,9,1):
        if current.weekday()<5: days.append(current)
        current+=timedelta(days=1)
    dates=[d.isoformat() for d in days]
    split=(len(dates)+1)//2
    populations={'FULL':dates,'H1':dates[:split],'H2':dates[split:]}
    settings={'_note':'TEST_ONLY composition fixture'}
    for leg in LEG_IDS:
        params=dict(initial_capital=100000,use_session=True,sess_start_min=540,sess_end_min=1020,
                    account_size=100000,risk_per_trade_pct=.7,point_value=.5)
        if leg=='orb_mnq_v7': params['qty']=1
        settings[leg]={'adapter':params,'emulator':{'slippage_ticks':1,'orders_on_close':True},'qty_scale':1}
    payloads['effective_settings_successor']=encoded(settings)
    payloads['source_startup_policy']=encoded({'schema':'qualification-source-startup/v1',
        'initialization':'FRESH_ONCE_CONTINUOUS','positions':'ZERO','working_orders':'ZERO',
        'splice_behavior':'CARRY_ALL_STATE','path_start_date':'2030-01-07',
        'shared_account_cap_micro_equivalents':80,'legs':{leg:{'paper_initial_capital':'100000',
        'lifecycle_tier':'AUTHORIZED','request_cap_micro_equivalents':80} for leg in LEG_IDS}})
    payloads['hours']=b'Explicit synthetic calendar facts, never market evidence.'
    fact={'role':'hours','sha256':digest(payloads['hours'])}
    calendar=[]; executions=[]; slots={}; csv={leg:['time,open,high,low,close,volume'] for leg in LEG_IDS}
    for day in days:
        instant=lambda h,m:datetime.combine(day,time(h,m),ET).astimezone(timezone.utc)
        timestamps=[instant(h,m) for h,m in ((9,0),(9,15),(15,45),(16,0))]
        slots[day.isoformat()]=[ts.isoformat() for ts in timestamps]
        calendar.append({'date':day.isoformat(),'status':'OPEN','reason':'explicit synthetic hours',
            'facts':[fact],'venue_deadlines':{leg:{'instant':instant(16,45).isoformat(),'fact':fact} for leg in LEG_IDS}})
        for leg in LEG_IDS:
            price=.006 if leg=='aegis_6j' else (101 if leg=='dj30_mym_p250' else 102 if leg=='vanguard_mgc' else 100)
            for n,ts in enumerate(timestamps):
                value=1100 if leg=='orb_mnq_v7' and n else price
                csv[leg].append(f'{ts.isoformat()},{value},{value},{value},{value},0')
            final_price=1100 if leg=='orb_mnq_v7' else price
            values=dict(open=final_price,high=final_price,low=final_price,close=final_price,volume=0)
            for h,m in ((15,45),(15,55),(16,0)):
                boundary=instant(h,m); start=boundary.replace(minute=m//15*15)
                executions.append({'source_session_date':day.isoformat(),'leg_id':leg,
                    'source_bar_time':start.isoformat(),'interval_start':start.isoformat(),
                    'instant':boundary.isoformat(),'price':final_price,
                    'prefix':values if m%15 else None,'suffix':values if m%15 else None})
    for leg in LEG_IDS: payloads[leg+'_panel']=('\n'.join(csv[leg])+'\n').encode()
    payloads['source_calendar']=encoded({'schema':'qualification-source-calendar/v1','coverage_start':dates[0],
        'coverage_end':dates[-1],'tail_covered':True,'sessions':calendar})
    payloads['schedule_execution_evidence']=encoded({'schema':'qualification-schedule-execution/v1','rows':executions})
    binding={'panel_sha256':{leg:digest(payloads[leg+'_panel']) for leg in LEG_IDS},
        'port_sha256':{leg:digest(payloads[PORT_ROLES[leg]]) for leg in LEG_IDS},
        'effective_settings_sha256':digest(payloads['effective_settings_successor']),
        'source_calendar_sha256':digest(payloads['source_calendar']),'slot_presence_rule':'QUALIFIED_GENERATION_UNION'}
    payloads['population_index']=encoded({'schema':'qualification-population-index/v1',
        'expected_source_dates':dates,'expected_source_slots':slots,'source_binding':binding,
        'slot_provenance':{day:[{'instant':ts,'state':'PROVIDER_PRESENT','present_legs':list(LEG_IDS)} for ts in times] for day,times in slots.items()},
        'populations':populations,'expected_exclusions':[]})
    for role,scope in (('source_calendar','SOURCE_CALENDAR'),('population_index','SOURCE_POPULATION_INDEX'),('schedule_execution_evidence','SCHEDULE_EXECUTION')):
        review={'schema':'qualification-source-review/v1','artifact_role':role,'artifact_sha256':digest(payloads[role]),'scope':scope,'decision':'ACCEPTED'}
        if role=='population_index': review['source_binding_sha256']=digest(encoded(binding))
        payloads[role+'_review']=encoded(review)
    cases={}
    for name in ('O-N','O-P','S-P','S-W1','S-W1P','S-W2','S-W2P','aegis_6j','vanguard_mgc'):
        leg='orb_mnq_v7' if name.startswith('O-') else 'dj30_mym_p250' if name.startswith('S-') else name
        cases[name]={'panel_sha256':binding['panel_sha256'][leg],'port_sha256':binding['port_sha256'][leg]}
    payloads['step3_admission_contract']=encoded({'schema':'packet1-step3-evidence-admission-v1',
        'review_status':'PENDING_INDEPENDENT_REVIEW','cases':cases,
        'interval_utc':[datetime.combine(days[0],time(9),ET).astimezone(timezone.utc).isoformat(),datetime.combine(days[-1],time(16),ET).astimezone(timezone.utc).isoformat()],
        'evidence_index_sha256':digest(payloads['step3_evidence_index'])})
    payloads['step3_independent_acceptance']=encoded({'schema':'packet1-step3-review-approval-v1','decision':'ACCEPTED',
        'accepted_contract_sha256':digest(payloads['step3_admission_contract']),'evidence_index_v4_sha256':digest(payloads['step3_evidence_index'])})
    payloads['step6_admission_contract']=encoded({'schema':'book-bundle-admissions-v1',
        'bundles':{name:{} for name in ('O-N','O-P','S-P','S-W1','S-W1P','S-W2','S-W2P')}})
    from pathlib import Path
    payloads['cost_model']=(Path(__file__).resolve().parents[3]/'lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/tradeify_commission_schedule.json').read_bytes()
    paths={role:'synthetic/'+role+'.bin' for role in payloads}
    for role,raw in payloads.items():
        path=root/paths[role];path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
    return ArtifactFixture(payloads,paths,populations,binding,pine)


def verified_domain(fixture, *, confirmation_depth=60):
    """Issue a real signed TEST_ONLY profile for these exact retained identities."""
    from test_trust_domain import case, NOW
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives import serialization
    from c1_rail.qualification.contract import TrustedApprovalKey
    from c1_rail.qualification.trust_domain import (
        PortRuntimePin, QualificationWorkloadPolicy, _composition_test_trust_policy, validate_qualification_trust_domain,
    )
    doc,base_policy,_,_=case()
    private={key:Ed25519PrivateKey.generate() for key in ('test-freeze','test-producer','test-seal')}
    keys={key:TrustedApprovalKey(key,value.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw),'TEST_ONLY') for key,value in private.items()}
    counts=doc['workload_policy']['stage_population_depths']
    counts['N2']={'FULL':[confirmation_depth]}
    counts['PART_B']={population:[confirmation_depth] for population in ('H1','H2')}
    workload=QualificationWorkloadPolicy(counts,5,5,6,2,4,2)
    identities=fixture.identity_fields()
    code={row.role:row.name for row in fixture.ordinary_modules}
    code.update({role:'fp_qualification_port_'+leg for leg,role in PORT_ROLES.items()})
    pins={leg:PortRuntimePin(leg,values['runtime_sha256'],values['pine_sha256']) for leg,values in identities['port_runtime_pins'].items()}
    doc.update(domain_id='TEST_ONLY-composition-fixture/v1',**identities,runtime_code_roles=code,
               freeze_key_ids=['test-freeze'],result_key_ids=['test-producer'],seal_key_ids=['test-seal'])
    doc['trusted_key_sha256']={key:digest(value.public_key) for key,value in keys.items()}
    doc['port_runtime_pins']={leg:{'leg_id':leg,'runtime_sha256':pin.runtime_sha256,'pine_sha256':pin.pine_sha256} for leg,pin in pins.items()}
    policy=_composition_test_trust_policy(accepted_historical_pins=identities['accepted_historical_pins'],
        required_artifact_roles=tuple(identities['required_artifact_roles']),runtime_code_roles=code,
        port_runtime_pins=pins,effective_settings_sha256=identities['effective_settings_sha256'],
        workload_policy=workload)
    raw=encoded(doc)
    approval=signed_approval(raw,private['test-freeze'],key_id='test-freeze',scope='BIND_QUALIFICATION_TRUST_DOMAIN')
    domain=validate_qualification_trust_domain(raw,approval,keys,policy=policy,now=NOW)
    return domain,private,keys


def contract_document(fixture, domain, *, decision_alpha='0.05'):
    """Exact contract proposal, signed only by the fixture's TEST_ONLY key."""
    from test_contract import _document
    doc=_document()
    hashes={role:digest(raw) for role,raw in fixture.payloads.items()}
    roles=sorted(hashes)
    doc.update(contract_id='TEST_ONLY-composition/v1',trust_domain_sha256=domain.sha256,
        artifacts=[{'role':role,'path':fixture.paths[role],'sha256':hashes[role],
            'producer':'synthetic-composition-fixture','authority_class':'TEST_ONLY'} for role in roles],
        runtime_load_trace=[{'role':role,'sha256':hashes[role]} for role in roles],
        role_owners=[{'role':role,'owner':'synthetic-composition-fixture'} for role in roles],
        dependencies=[{'consumer_role':role,'requires_roles':[r for r in roles if r!=role] if role=='qualification_runner' else []} for role in roles],
        historical_pins=dict(domain.accepted_historical_pins),populations=fixture.populations,
        authority={'evidence_class':'TEST_ONLY','permits_synthetic_authority':True},
        approval_policy={'freeze_scope':'FREEZE_F1','freeze_authority_class':'TEST_ONLY','freeze_key_ids':['test-freeze']})
    doc['effective_settings']['settings_sha256']=domain.effective_settings_sha256
    replay=doc['replay']
    replay.update(horizon_sessions=5,speed_horizon_sessions=5,root_rng_namespace='TEST_ONLY/composition-fixture/v1')
    replay['decision_rules']['speed_horizon_sessions']=5
    replay['decision_rules']['alpha']=decision_alpha
    counts=domain.workload_policy.stage_population_depths
    confirmation_depth=counts['N2']['FULL'][0]
    depths={'LEGALITY':1,'N1':2,'N2':confirmation_depth,'PART_B':confirmation_depth,'PART_A':2,'N3':2}
    for stage in replay['stages']:
        stage['population_counts']={p:list(values) for p,values in counts[stage['name']].items()}
        stage['exact_depth']=depths[stage['name']]
        if stage['name']=='N1':stage['max_failures_per_population']=0
    replay['part_a'].update(initial_panels=2,expanded_panels=4,paths_per_population_per_panel=2)
    replay['budget'].update(n1_paths=6,n2_paths=3*confirmation_depth,part_a_initial_paths=4,part_a_expanded_paths=8,n3_paths=6)
    doc['result_plan']['required_output_roles']=['private-result','public-projection']
    doc['result_plan']['permitted_optional_output_roles']=[]
    doc['result_plan']['adjudicator_closure_sha256']=digest(encoded({'schema':'qualification-adjudicator-closure/v1','sources':hashes}))
    return doc


def signed_approval(subject_bytes, private, *, key_id, scope, contract_sha256=None):
    import base64
    sha=digest(subject_bytes)
    payload={'schema':'qualification_approval_payload/v1','scope':scope,
        'subject_sha256':sha,'contract_sha256':sha if contract_sha256 is None else contract_sha256,
        'authority_class':'TEST_ONLY','issued_at':'2026-09-15T19:00:00Z','expires_at':'2026-09-16T19:00:00Z'}
    return encoded({'schema':'qualification_approval/v1','payload':payload,
        'signature':{'algorithm':'Ed25519','key_id':key_id,'value_b64':base64.b64encode(private.sign(encoded(payload))).decode()}})


@dataclass(frozen=True)
class VerifiedComposition:
    fixture: ArtifactFixture
    domain: object
    contract: object
    source: object
    private_keys: dict
    trusted_keys: dict
    loaded_modules: dict
    retained_source_bytes: dict
    contract_bytes: bytes
    freeze_approval_bytes: bytes
    runtime_inventory: object

    def current_loaded_modules(self):
        """Fresh path construction replaces port module objects, never identities."""
        import sys
        return {role:sys.modules[name] for role,name in self.domain.runtime_code_roles.items()}


def build_verified_composition(root, *, confirmation_depth=60, decision_alpha='0.05'):
    """Real G1→retained source→loader composition under signed TEST_ONLY context."""
    import sys
    from test_contract import NOW
    from c1_rail.qualification.contract import validate_frozen_contract, ObservedBindings
    from c1_rail.qualification.production_source import ProductionSource
    from c1_rail.qualification.runtime_inventory import collect_runtime_inventory
    fixture=build_artifacts(root).with_runtime_artifacts(root)
    domain,private,keys=verified_domain(fixture,confirmation_depth=confirmation_depth)
    document=contract_document(fixture,domain,decision_alpha=decision_alpha)
    raw=encoded(document)
    approval=signed_approval(raw,private['test-freeze'],key_id='test-freeze',scope='FREEZE_F1')
    retained={role:(root/path).read_bytes() for role,path in fixture.paths.items()}
    observed=ObservedBindings(artifact_sha256={fixture.paths[r]:digest(b) for r,b in retained.items()},
        runtime_load_sha256={r:digest(b) for r,b in retained.items()},
        effective_settings_sha256=digest(retained['effective_settings_successor']),orb_normal_base=1)
    contract=validate_frozen_contract(raw,approval,keys,observed,now=NOW,trust_domain=domain)
    source=ProductionSource._build_composition(contract,artifact_root=root)
    modules={row.role:row.module for row in fixture.ordinary_modules}
    modules.update({role:sys.modules['fp_qualification_port_'+leg] for leg,role in PORT_ROLES.items()})
    inventory=collect_runtime_inventory(contract,loaded_modules=modules,retained_source_bytes=retained,artifact_root=root)
    return VerifiedComposition(fixture,domain,contract,source,private,keys,modules,retained,raw,approval,inventory)
