"""Gated E1 executor. Never freezes contracts or signs qualification results."""
from datetime import date
import hashlib
import os
import weakref
from dataclasses import dataclass
from time import perf_counter, process_time

from mc.simulation import EvaluationState
from .runner import SyntheticStageRequest, NeedsContext, _run_stage
from .part_a import SyntheticPartARequest, _run_part_a
from .provider import _ReplayProvider


@dataclass(frozen=True)
class _ExecutorBinding:
    reference: object
    contract: object
    source: object
    store: object
    domain: object
    wall_start: float
    cpu_start: float


_ISSUED_EXECUTORS={}


def _forget_executor(identity):
    _ISSUED_EXECUTORS.pop(identity,None)


def _initial_state(contract):
    state=contract.initial_state
    return EvaluationState(float(state.original_basis),float(state.current_equity),
        float(state.historical_eod_peak),state.prior_trade_days,float(state.prior_max_day_profit))


def _execution_domain(contract, authority_class):
    from .contract import ValidatedFrozenContract, require_validated_frozen_contract
    from .trust_domain import require_validated_trust_domain
    if type(contract) is not ValidatedFrozenContract:
        raise TypeError('exact validated frozen contract required')
    require_validated_frozen_contract(contract)
    domain=require_validated_trust_domain(contract.trust_domain)
    if (domain.authority_class!=authority_class
            or contract.approval.authority_class!=authority_class
            or domain.permits_synthetic!=(authority_class=='TEST_ONLY')
            or contract.trust_domain_sha256!=domain.sha256):
        raise ValueError('execution trust domain or authority differs')
    return domain


def _stage_request(contract,stage,budget_seconds):
    if stage not in ('n1','n2'):
        raise ValueError('E1 executor only permits n1/n2; n3 requires its own authorization')
    specs=contract.stage_specs
    full=specs[stage.upper()].exact_depth
    half=full if stage=='n1' else specs['PART_B'].exact_depth
    return SyntheticStageRequest(stage,(('FULL',full),('H1',half),('H2',half)),
        contract.replay.horizon_sessions,contract.replay.root_rng_namespace,budget_seconds)


def _part_a_request(contract,path_start_date,budget_seconds):
    part=contract.replay.part_a
    if part.percentile_method!='INVERSE_ECDF_LEFT':
        raise ValueError('unsupported frozen percentile method')
    return SyntheticPartARequest('n2',contract.replay.outer_months,contract.replay.inner_block_sessions,
        part.paths_per_population_per_panel,contract.replay.horizon_sessions,part.initial_panels,
        part.expanded_panels,float(part.percentile),'nearest_rank',float(part.expansion_center_p5),
        float(part.expansion_tolerance),contract.replay.root_rng_namespace,budget_seconds,path_start_date)


def _peak_memory_bytes():
    if os.name=='nt':
        import ctypes
        from ctypes import wintypes
        class Counters(ctypes.Structure):
            _fields_=[('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD)]+[
                (name,ctypes.c_size_t) for name in ('PeakWorkingSetSize','WorkingSetSize',
                'QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaPeakNonPagedPoolUsage',
                'QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage')]
        counters=Counters()
        counters.cb=ctypes.sizeof(counters)
        kernel=ctypes.WinDLL('kernel32',use_last_error=True)
        kernel.GetCurrentProcess.restype=wintypes.HANDLE
        psapi=ctypes.WinDLL('psapi',use_last_error=True)
        psapi.GetProcessMemoryInfo.argtypes=[wintypes.HANDLE,ctypes.POINTER(Counters),wintypes.DWORD]
        if not psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(),ctypes.byref(counters),counters.cb):
            raise NeedsContext('process memory observation unavailable')
        return counters.PeakWorkingSetSize
    try:
        import resource
        import sys
        return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)*(1 if sys.platform=='darwin' else 1024)
    except (ImportError,AttributeError) as exc:
        raise NeedsContext('process memory observation unavailable') from exc


class ProductionExecutor:
    """Concrete mechanics accessible only after durable checkpoint dispatch.

    The source factory owns admitted artifacts and market/session evidence.
    The orchestration entrypoint revalidates approvals before each dispatch.
    Budget checks occur at replay boundaries; they are not an OS memory limit.
    """
    __slots__=('contract','source','store','_trust_domain','_consumed','__weakref__')

    def __init__(self,contract,source,store):
        from .contract import ValidatedFrozenContract
        if type(contract) is not ValidatedFrozenContract or contract.approval.authority_class!='OPERATOR':
            raise TypeError('production requires operator-validated frozen contract')
        self._initialize(contract,source,store,_execution_domain(contract,'OPERATOR'))

    def _initialize(self,contract,source,store,domain):
        from .attempt import AttemptStore
        from .contract import require_validated_frozen_contract
        from .production_source import ProductionSource
        from .trust_domain import require_validated_trust_domain
        issued=_ISSUED_EXECUTORS.get(id(self))
        if issued is not None and issued.reference() is self:
            raise ValueError('executor is already initialized; budget and provider cannot reset')
        require_validated_frozen_contract(contract)
        domain=require_validated_trust_domain(domain)
        if contract.trust_domain is not domain:
            raise ValueError('executor domain differs from validated contract')
        if type(source) is not ProductionSource or type(store) is not AttemptStore:
            raise TypeError('concrete admitted source and durable store required')
        source.verify_for(contract)
        if store.contract_digest!=contract.contract_sha256:
            raise ValueError('journal contract differs')
        if store.trust_domain_sha256!=domain.sha256:
            raise ValueError('journal trust domain differs')
        self.contract,self.source,self.store=contract,source,store
        self._trust_domain=domain
        self._consumed=set()
        identity=id(self)
        _ISSUED_EXECUTORS[identity]=_ExecutorBinding(
            weakref.ref(self,lambda ref:_forget_executor(identity)),
            contract,source,store,domain,perf_counter(),process_time())

    @property
    def initial_state(self):
        # No caller-held mutable state object is later consumed by a stage.
        self._checked_domain()
        return _initial_state(self.contract)

    def _checked_domain(self):
        from .contract import require_validated_frozen_contract
        from .production_source import ProductionSource
        from .attempt import AttemptStore
        from .trust_domain import require_validated_trust_domain
        binding=_ISSUED_EXECUTORS.get(id(self))
        if (binding is None or binding.reference() is not self
                or self.contract is not binding.contract
                or self.source is not binding.source or type(self.source) is not ProductionSource
                or self.store is not binding.store or type(self.store) is not AttemptStore
                or self._trust_domain is not binding.domain):
            raise ValueError('issued executor inputs or trust domain changed')
        require_validated_frozen_contract(self.contract)
        domain=require_validated_trust_domain(self._trust_domain)
        if (self.contract.trust_domain is not domain
                or self.contract.trust_domain_sha256!=domain.sha256
                or self.store.trust_domain_sha256!=domain.sha256):
            raise ValueError('executor trust domain differs from contract or journal')
        return domain

    def _budget(self):
        self._checked_domain()
        binding=_ISSUED_EXECUTORS[id(self)]
        budget=self.contract.replay.budget
        remaining=budget.maximum_wall_seconds-(perf_counter()-binding.wall_start)
        if remaining<=0 or process_time()-binding.cpu_start>budget.maximum_cpu_seconds:
            raise NeedsContext('frozen execution CPU/wall budget exhausted; no replacement draws')
        if _peak_memory_bytes()>budget.maximum_memory_bytes:
            raise NeedsContext('frozen execution memory budget exceeded; no replacement draws')
        return remaining

    def _admit(self,dispatch,checkpoint):
        from .attempt import CheckpointDispatch
        self._checked_domain()
        if type(dispatch) is not CheckpointDispatch or dispatch.checkpoint!=checkpoint:
            raise TypeError('exact designated checkpoint dispatch required')
        claim=self.store.claimed_reservation('TB_E1')
        self.store.verify_claim(claim,require_state='STARTED_IN_DOUBT')
        row=next(row for row in self.store.checkpoints() if row['checkpoint']==checkpoint)
        if (dispatch.campaign_id!=self.store.campaign_id
                or dispatch.contract_digest!=self.contract.contract_sha256
                or dispatch.parent_reservation_event_digest!=claim.reservation_event_digest
                or row['state']!='STARTED_IN_DOUBT'
                or row['dispatch_event_digest']!=dispatch.dispatch_event_digest
                or hashlib.sha256(row['binding_bytes']).hexdigest()!=dispatch.binding_sha256):
            raise ValueError('checkpoint dispatch differs from durable authority')
        if dispatch.dispatch_event_digest in self._consumed:
            raise ValueError('checkpoint execution cannot be repeated')
        self.source.verify_for(self.contract)
        self._budget()
        # The issuing store consumes the exact in-process capability once.
        # Durable STARTED state alone cannot authorize a recreated executor.
        self.store.consume_checkpoint_dispatch(dispatch)
        self._consumed.add(dispatch.dispatch_event_digest)

    def _replay(self,path):
        self._budget()
        try:
            return self.source.replay(path)
        finally:
            self._budget()

    def run_stage(self,stage,dispatch):
        self._admit(dispatch,stage.upper())
        try:
            # Construct from the admitted source for this dispatch. A mutable
            # process-global cache must never select the replay implementation.
            reference=weakref.ref(self)
            def replay(path):
                executor=reference()
                if executor is None:
                    raise ValueError('issuing executor no longer exists')
                return executor._replay(path)
            provider=_ReplayProvider(self.source.sessions,self.source.adjacent,
                block_sessions=self.contract.replay.inner_block_sessions,
                path_start_date=self.source.path_start_date,replay=replay)
            return _run_stage(_stage_request(self.contract,stage,self._budget()),provider,
                              initial_state=self.initial_state,synthetic=self._checked_domain().permits_synthetic)
        finally:
            # Kernel evaluation and result aggregation happen after _replay.
            self._budget()

    def run_part_a(self,dispatch,full_pass_rate):
        self._admit(dispatch,'PART_A')
        def proof(panel):
            self._budget()
            try:
                return self.source.proof(panel)
            finally:
                self._budget()
        try:
            return _run_part_a(_part_a_request(self.contract,self.source.path_start_date,self._budget()),
                self.source.sessions,adjacent=self.source.adjacent,covered_until=self.source.covered_until,
                tail_covered=self.source.tail_covered,proof_provider=proof,replay_provider=self._replay,
                initial_state=self.initial_state,full_pass_rate=float(full_pass_rate),
                synthetic=self._checked_domain().permits_synthetic)
        finally:
            self._budget()


def _composition_executor(contract,source,store):
    """Internal signed test-domain route; it cannot create production evidence."""
    domain=_execution_domain(contract,'TEST_ONLY')
    executor=object.__new__(ProductionExecutor)
    executor._initialize(contract,source,store,domain)
    return executor
