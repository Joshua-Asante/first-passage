"""Once-only E1 checkpoint dispatch and retained evidence assembly.

This module neither signs results nor issues authority. The public production
route revalidates G1/G2 inputs and constructs the concrete production executor.
The private recording seam exists for deterministic controller tests only.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
import hashlib
import json
from types import MappingProxyType

from .model import PathOutcome
from .part_a import SyntheticPanelResult, SyntheticPartAResult
from .regime import domain_seed
from .result_adjudication import adjudicate_e1_outcomes
from .runner import StageRun


def canonical_bytes(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,
                      allow_nan=False).encode('utf-8')


def _sha(value):
    return hashlib.sha256(value).hexdigest()


def _outcome(row):
    if type(row) is not PathOutcome:
        raise TypeError('exact immutable PathOutcome required')
    return {'status':row.status,'sessions_to_pass':row.sessions_to_pass,
            'failure_reason':row.failure_reason,'diagnostics':[list(p) for p in row.diagnostics]}


@dataclass(frozen=True)
class SeedInput:
    population: str
    path_index: int
    panel_index: int | None
    purpose: str
    canonical_bytes: bytes

    @property
    def sha256(self):
        return _sha(self.canonical_bytes)


@dataclass(frozen=True)
class E1Execution:
    contract_sha256: str
    trust_domain_sha256: str
    outcomes: tuple
    path_inventory_bytes: bytes
    stage_input_sha256: tuple[tuple[str,str], ...]
    checkpoint_receipts: tuple[tuple[str,bytes], ...]
    decisions: tuple[tuple[str,str], ...]
    synthetic: bool

    @property
    def passed(self):
        return bool(self.decisions) and all(value=='PASS' for _,value in self.decisions)

    @property
    def path_outcomes(self):
        return MappingProxyType({stage:MappingProxyType(dict(populations))
                                 for stage,populations in self.outcomes})


def seed_input(contract, *, stage, population, panel_index, path_index,
               synthetic, purpose='path'):
    """Bind actual shared RNG call arguments and frozen source pool identity."""
    root=contract.replay.root_rng_namespace
    seed=domain_seed(root=root,stage=stage,population=population,panel_index=panel_index,
                     path_index=path_index,synthetic=synthetic,purpose=purpose)
    raw=canonical_bytes({'schema':'qualification-seed-input/v1',
        'contract_sha256':contract.contract_sha256,'root_rng_namespace':root,
        'trust_domain_sha256':contract.trust_domain_sha256,
        'stage':stage,'population':population,'panel_index':panel_index,
        'path_index':path_index,'purpose':purpose,'synthetic':synthetic,'seed':seed,
        'source_session_ids_sha256':_sha(canonical_bytes(list(contract.populations[population])))})
    return SeedInput(population,path_index,panel_index,purpose,raw)


def panel_identity(contract, panel):
    return _sha(canonical_bytes({'schema':'qualification-panel/v1',
        'contract_sha256':contract.contract_sha256,
        'trust_domain_sha256':contract.trust_domain_sha256,
        'root_rng_namespace':contract.replay.root_rng_namespace,
        'panel_index':panel.index,'source_session_ids':list(panel.source_session_ids)}))


def _depths(contract, stage):
    specs=contract.stage_specs
    populations=(('FULL','H1','H2') if stage=='N1' else ('FULL',) if stage=='N2' else ('H1','H2'))
    spec=specs[stage]
    if set(spec.population_counts)!=set(populations):
        raise ValueError('frozen population inventory differs')
    result=[]
    for population in populations:
        counts=spec.population_counts[population]
        if (type(counts) is not tuple or len(counts)!=1
                or type(counts[0]) is not int or counts[0]<=0):
            raise ValueError('single exact positive depth required per population')
        result.append((population,counts[0]))
    return tuple(result)


def _stage_seeds(contract, stage, synthetic):
    depths=_depths(contract,'N1') if stage=='n1' else (*_depths(contract,'N2'),*_depths(contract,'PART_B'))
    return tuple(seed_input(contract,stage=stage,population=p,panel_index=None,path_index=i,
                            synthetic=synthetic) for p,n in depths for i in range(n))


def _part_a_seeds(contract,synthetic):
    spec=contract.replay.part_a
    rows=[]
    for panel in range(spec.expanded_panels):
        rows.append(seed_input(contract,stage='n2',population='FULL',panel_index=panel,
                               path_index=0,purpose='outer',synthetic=synthetic))
        rows.extend(seed_input(contract,stage='n2',population='FULL',panel_index=panel,
                    path_index=i,synthetic=synthetic)
                    for i in range(spec.paths_per_population_per_panel))
    return tuple(rows)


def _validate_stage(run, stage, seeds, synthetic):
    if type(run) is not StageRun or run.stage!=stage or run.synthetic is not synthetic:
        raise ValueError('stage result type, stage or authority route differs')
    if type(run.populations) is not tuple or tuple(p for p,_ in run.populations)!=('FULL','H1','H2'):
        raise ValueError('ordered full joint population result required')
    for population,rows in run.populations:
        expected=sum(seed.population==population for seed in seeds)
        if type(rows) is not tuple or len(rows)!=expected:
            raise ValueError('stage result depth differs from dispatched frozen plan')
        for row in rows:_outcome(row)


def _execute_e1(contract, *, store, executor, preflight_binding,
                exact_depth_approval_sha256, now, synthetic, authorize=lambda instant:None):
    """Private recording seam; callers receive evidence, never a seal.

    No exception is caught: a callback/receipt failure leaves its durable
    checkpoint in doubt. Re-entering this function cannot dispatch it again.
    """
    if type(synthetic) is not bool or type(preflight_binding) is not bytes:
        raise TypeError('explicit route and immutable preflight binding required')
    from .production import ProductionExecutor
    if not synthetic:
        if type(executor) is not ProductionExecutor:
            raise TypeError('concrete production executor required')
    if type(executor) is ProductionExecutor:
        from .trust_domain import require_validated_trust_domain
        domain=require_validated_trust_domain(executor._trust_domain)
        if contract.trust_domain is not domain or synthetic is not domain.permits_synthetic:
            raise ValueError('concrete executor trust domain differs')
    if store.contract_digest!=contract.contract_sha256:
        raise ValueError('journal contract differs')
    domain_sha=contract.trust_domain_sha256
    if (type(domain_sha) is not str or len(domain_sha)!=64
            or any(c not in '0123456789abcdef' for c in domain_sha)
            or store.trust_domain_sha256!=domain_sha):
        raise ValueError('journal trust domain differs')
    binding=json.loads(preflight_binding)
    if canonical_bytes(binding)!=preflight_binding or binding.get('attempt_id')!=store.campaign_id:
        raise ValueError('preflight binding differs from journal attempt')
    if binding.get('contract_sha256')!=contract.contract_sha256:
        raise ValueError('preflight contract differs')
    if binding.get('trust_domain_sha256')!=domain_sha:
        raise ValueError('preflight trust domain differs')
    if (type(exact_depth_approval_sha256) is not str or len(exact_depth_approval_sha256)!=64
            or any(c not in '0123456789abcdef' for c in exact_depth_approval_sha256)):
        raise ValueError('exact depth approval digest required')
    reserved_at=now()
    authorize(reserved_at)
    store.reserve('TB_E1',preflight_binding,now=reserved_at)
    claim=store.claimed_reservation('TB_E1')
    started_at=now()
    authorize(started_at)
    store.start_once('TB_E1',claim,now=started_at)
    claim=store.claimed_reservation('TB_E1')
    store.verify_claim(claim,require_state='STARTED_IN_DOUBT')
    outcomes={'LEGALITY':{}}
    inventory={'schema':'qualification_path_inventory/v1','trust_domain_sha256':domain_sha,'records':[]}
    inputs={'LEGALITY':_sha(canonical_bytes({'stage':'LEGALITY',
            'contract_sha256':contract.contract_sha256,
            'trust_domain_sha256':domain_sha,
            'exact_depth_approval_sha256':exact_depth_approval_sha256}))}
    receipts=[]

    def dispatch(checkpoint,seeds=(),extra=None):
        dispatched_at=now()
        authorize(dispatched_at)
        store.verify_claim(claim,require_state='STARTED_IN_DOUBT')
        plan={'schema':'e1_checkpoint_plan/v1','checkpoint':checkpoint,
              'contract_sha256':contract.contract_sha256,'synthetic':synthetic,
              'trust_domain_sha256':domain_sha,
              'exact_depth_approval_sha256':exact_depth_approval_sha256,
              'horizon_sessions':contract.replay.horizon_sessions,
              'seed_inputs':[json.loads(seed.canonical_bytes) for seed in seeds],
              'extra':extra}
        return store.start_checkpoint_once(checkpoint,claim,canonical_bytes(plan),now=dispatched_at)

    def decisions():
        return adjudicate_e1_outcomes(contract,outcomes,inventory)

    def complete(checkpoint,dispatched,extra=None):
        checkpoint_stages={'N1':('N1',),'CUTOFF':(),'N2':('N2','PART_B'),'PART_A':('PART_A',)}
        decision_stages={'N1':(),'CUTOFF':('N1',),'N2':('N2','PART_B'),'PART_A':('PART_A',)}
        retained_stages=checkpoint_stages[checkpoint]
        evaluated=decisions()
        receipt=canonical_bytes({'schema':'e1_checkpoint_receipt/v1','checkpoint':checkpoint,
            'attempt_id':store.campaign_id,'contract_sha256':contract.contract_sha256,
            'trust_domain_sha256':domain_sha,
            'binding_sha256':dispatched.binding_sha256,
            'dispatch_event_digest':dispatched.dispatch_event_digest,
            'synthetic':synthetic,'decisions':{stage:evaluated[stage] for stage in decision_stages[checkpoint]},
            'stage_input_sha256':{stage:inputs[stage] for stage in checkpoint_stages[checkpoint]},
            'path_inventory':[row for row in inventory['records'] if row['stage'] in retained_stages],
            'outcomes':{s:{p:[_outcome(row) for row in rows] for p,rows in pops.items()}
                        for s,pops in outcomes.items() if s in retained_stages},'extra':{} if extra is None else extra})
        stored=store.complete_checkpoint(checkpoint,dispatched,receipt,now=now())
        if stored!=receipt:raise ValueError('durable checkpoint receipt differs')
        receipts.append((checkpoint,receipt))

    def retain(stage,populations,seeds,panel_id=None):
        outcomes[stage]=dict(populations)
        stage_rows=[]
        for population,rows in populations:
            selected=[seed for seed in seeds if seed.population==population]
            if len(selected)!=len(rows):raise ValueError('retained path/seed count differs')
            for seed,row in zip(selected,rows):
                record={'stage':stage,'population':population,'path_index':seed.path_index,
                        'panel_id':panel_id,'seed_input_sha256':seed.sha256,
                        'outcome_sha256':_sha(canonical_bytes(_outcome(row)))}
                stage_rows.append(record)
        inventory['records'].extend(stage_rows)
        inputs[stage]=_sha(canonical_bytes({'stage':stage,'paths':[
            {key:row[key] for key in ('population','path_index','panel_id','seed_input_sha256')}
            for row in stage_rows]}))

    def result():
        return E1Execution(contract.contract_sha256,domain_sha,
            tuple((s,tuple(pops.items())) for s,pops in outcomes.items()),canonical_bytes(inventory),
            tuple(inputs.items()),tuple(receipts),tuple(decisions().items()),synthetic)

    seeds=_stage_seeds(contract,'n1',synthetic)
    issued=dispatch('N1',seeds)
    run=executor.run_stage('n1',issued)
    _validate_stage(run,'n1',seeds,synthetic)
    retain('N1',run.populations,seeds)
    complete('N1',issued)

    cutoff={'stages':[{ 'stage':name,'exact_depth':contract.stage_specs[name].exact_depth,
                       'max_failures_per_population':contract.stage_specs[name].max_failures_per_population}
                      for name in ('N2','PART_B')]}
    issued=dispatch('CUTOFF',extra=cutoff)
    store.consume_checkpoint_dispatch(issued)
    complete('CUTOFF',issued,extra=cutoff)
    if decisions()['N1']!='PASS':return result()

    seeds=_stage_seeds(contract,'n2',synthetic)
    issued=dispatch('N2',seeds)
    run=executor.run_stage('n2',issued)
    _validate_stage(run,'n2',seeds,synthetic)
    # One joint batch: FULL supplies both speed and failure statistics. The two
    # half populations are exposed as Part B with no callback or redraw.
    retain('N2',run.populations[:1],tuple(s for s in seeds if s.population=='FULL'))
    retain('PART_B',run.populations[1:],tuple(s for s in seeds if s.population!='FULL'))
    complete('N2',issued)
    if any(decisions()[name]!='PASS' for name in ('N2','PART_B')):return result()

    seeds=_part_a_seeds(contract,synthetic)
    issued=dispatch('PART_A',seeds,{'initial_panels':contract.replay.part_a.initial_panels,
                                  'expanded_panels':contract.replay.part_a.expanded_panels})
    full=outcomes['N2']['FULL']
    full_rate=Decimal(sum(row.status=='PASS' for row in full))/len(full)
    part=executor.run_part_a(issued,full_rate)
    if type(part) is not SyntheticPartAResult or part.synthetic is not synthetic or type(part.panels) is not tuple:
        raise ValueError('Part A result type or authority route differs')
    spec=contract.replay.part_a
    if len(part.panels) not in (spec.initial_panels,spec.expanded_panels):
        raise ValueError('Part A panel count differs from frozen plan')
    rows=[];panel_records=[];part_records=[]
    for index,panel in enumerate(part.panels):
        if (type(panel) is not SyntheticPanelResult or panel.index!=index
                or type(panel.source_session_ids) is not tuple
                or len(panel.source_session_ids)!=len(contract.populations['FULL'])
                or any(s not in contract.populations['FULL'] for s in panel.source_session_ids)
                or type(panel.outcomes) is not tuple
                or len(panel.outcomes)!=spec.paths_per_population_per_panel):
            raise ValueError('Part A retained panel identity/order/depth differs')
        identity=panel_identity(contract,panel)
        panel_records.append({'panel_index':index,'panel_id':identity,
                              'source_session_ids':list(panel.source_session_ids)})
        selected=[seed for seed in seeds if seed.panel_index==index and seed.purpose=='path']
        for seed,row in zip(selected,panel.outcomes):
            rows.append(row)
            part_records.append({'stage':'PART_A','population':'REGIME','path_index':seed.path_index,
                'panel_id':identity,'seed_input_sha256':seed.sha256,
                'outcome_sha256':_sha(canonical_bytes(_outcome(row)))})
    outcomes['PART_A']={'REGIME':tuple(rows)}
    inventory['records'].extend(part_records)
    inputs['PART_A']=_sha(canonical_bytes({'stage':'PART_A','paths':[
        {key:row[key] for key in ('population','path_index','panel_id','seed_input_sha256')}
        for row in part_records]}))
    complete('PART_A',issued,extra={'panels':panel_records})
    return result()


def run_production_e1(contract, *, source, store, preflight, exact_depth_approval_bytes,
                      trusted_keys, now):
    """Execute only through verified contracts and the concrete production route.

    ``now`` is a clock callable so approval expiry is rechecked at each durable
    dispatch. This entry point performs no signing or automatic result commit.
    """
    from .contract import ValidatedFrozenContract
    from .preflight import PreflightReceipt
    from .production import _execution_domain
    if type(contract) is not ValidatedFrozenContract or type(preflight) is not PreflightReceipt:
        raise TypeError('exact validated contract and preflight receipt required')
    if contract.approval.authority_class!='OPERATOR' or preflight.exact_depth_approval.authority_class!='OPERATOR':
        raise ValueError('production operator authority required')
    domain=_execution_domain(contract,'OPERATOR')
    return _run_bound_e1(contract,source=source,store=store,preflight=preflight,
        exact_depth_approval_bytes=exact_depth_approval_bytes,trusted_keys=trusted_keys,
        now=now,domain=domain)


def _run_composition_e1(contract, *, source, store, preflight, exact_depth_approval_bytes,
                        trusted_keys, now):
    """Internal composition-test entry; output remains signed TEST_ONLY evidence."""
    from .contract import ValidatedFrozenContract
    from .preflight import PreflightReceipt
    from .production import _execution_domain
    if type(contract) is not ValidatedFrozenContract or type(preflight) is not PreflightReceipt:
        raise TypeError('exact validated contract and preflight receipt required')
    domain=_execution_domain(contract,'TEST_ONLY')
    return _run_bound_e1(contract,source=source,store=store,preflight=preflight,
        exact_depth_approval_bytes=exact_depth_approval_bytes,trusted_keys=trusted_keys,
        now=now,domain=domain)


def _run_bound_e1(contract, *, source, store, preflight, exact_depth_approval_bytes,
                  trusted_keys, now, domain):
    from .preflight import preflight_binding_bytes, revalidate_e1_preflight
    from .production import ProductionExecutor, _composition_executor
    from .trust_domain import require_validated_trust_domain
    domain=require_validated_trust_domain(domain)
    if (contract.trust_domain is not domain or preflight.trust_domain_sha256!=domain.sha256
            or preflight.exact_depth_approval.authority_class!=domain.authority_class
            or store.trust_domain_sha256!=domain.sha256):
        raise ValueError('preflight or journal trust domain differs')
    def authorize(instant):
        revalidate_e1_preflight(contract,preflight,exact_depth_approval_bytes=exact_depth_approval_bytes,
                               trusted_keys=trusted_keys,now=instant,trust_domain=domain)
    authorize(now())
    executor=(_composition_executor(contract,source,store) if domain.permits_synthetic
              else ProductionExecutor(contract,source,store))
    return _execute_e1(contract,store=store,executor=executor,
        preflight_binding=preflight_binding_bytes(preflight),
        exact_depth_approval_sha256=preflight.exact_depth_approval.approval_sha256,
        now=now,synthetic=domain.permits_synthetic,authorize=authorize)
