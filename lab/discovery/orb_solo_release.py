"""Fixed-study release primitives. They do not authorize or initiate scoring.

Worker execution is read-only with one bounded stdout document. The controller
owns the only bounded publication path. A durable phase lease cannot auto-resume.
"""
from __future__ import annotations

from datetime import datetime, timezone
from collections import deque
import hashlib
import io
import json
import math
import os
from pathlib import Path
import re
import sys

from discovery.orb_solo_executor import TIERS

STUDY = 'ORB-MNQ-v7-solo-S4-2026-10'
ALLOCATIONS = dict(setup=21., candidate=9.5, reference=9.5, seal=2.)
DEPTH = dict(groups_per_population=19, sims_per_seed=10000, seeds=[42,123,2026], horizon=1500)
FIXED_INPUT_PINS = dict(
    candidate='bff235ea0934dace8a000dbad7eeede8673506718bd020f54f2c04cbae304568',
    reference='a2e9192aec54dd081245232247f5f5306553910a2956f3601364c050f9aa50a2',
    binding='a4ddd99572584e47b505677172b25b9f4a3d8aca1984fbbe05f3a903f2fbd9f1',
    rules='23a706d36f2c1840a6b4da5da44df3eb8d4f9f81136da6a124564722dc1876d9')
MAX_CAPTURE_BYTES = 32*1024**2
MAX_PLAN_BYTES = 256*1024
MAX_RECEIPT_BYTES = 2*1024**2
MAX_SAMPLES = 4096
SEAL_RESERVE_SECONDS = 60


class ReleaseError(RuntimeError):
    pass


class SampleRing:
    """Keep finite summaries and a bounded tail, even during a 48-hour phase."""
    def __init__(self,*,capacity=MAX_SAMPLES):
        if type(capacity) is not int or not 1 <= capacity <= MAX_SAMPLES:
            raise ReleaseError('invalid sample capacity')
        self.tail=deque(maxlen=capacity)
        self.first=None
        self.last=None
        self.observations=0
        self.maxima={}

    def append(self,sample):
        allowed={'elapsed','cpu_seconds','memory_bytes','new_disk_bytes','active_processes'}
        if set(sample) != allowed or any(not isinstance(v,(float,int)) or not math.isfinite(v) or v < 0 for v in sample.values()):
            raise ReleaseError('invalid native sample')
        if self.last and (sample['elapsed'] < self.last['elapsed'] or sample['cpu_seconds'] < self.last['cpu_seconds']):
            raise ReleaseError('nonmonotone native sample')
        self.first=sample if self.first is None else self.first
        self.last=sample
        self.observations+=1
        for name,value in sample.items():
            self.maxima[name+'_max']=max(self.maxima.get(name+'_max',0),value)
        self.tail.append(sample)

    def evidence(self):
        return dict(observations=self.observations,first=self.first,last=self.last,tail=list(self.tail),**self.maxima)


class WorkerPolicy:
    """Read-only scientific worker. File publication belongs to the controller.

    This is a trusted-code I/O policy, not a sandbox for hostile native binaries.
    The pinned worker imports no arbitrary user code; tested Python operations
    cannot write or launch children. Runtime libraries are read-only dependencies.
    """
    def __init__(self,paths,*,runtime_roots=None):
        self.paths={Path(p).resolve() for p in paths}
        roots=runtime_roots if runtime_roots is not None else (sys.prefix,sys.base_prefix)
        self.runtime_roots=tuple(Path(p).resolve() for p in roots)

    def __call__(self,event,args):
        guarded_event(event,args)
        if event == 'open':
            path,_,_=args
            if isinstance(path,int):
                return
            resolved=Path(path).resolve()
            if resolved.suffix == '.pyc' and resolved.parent.name == '__pycache__':
                source=resolved.parent.parent/(resolved.name.split('.')[0]+'.py')
                if source in self.paths:
                    return
            if resolved not in self.paths and not any(resolved.is_relative_to(root) for root in self.runtime_roots):
                raise ReleaseError('worker read outside pinned inputs/runtime')


class ControllerMemoryJob:
    """Hard native aggregate memory bound including this controller's children.

    Created only inside the dedicated execution process, never in the interactive
    tool host. No kill-on-close on the self job; a separate child Job retains that
    shutdown guarantee. Nested descendants inherit this memory ceiling before run.
    """
    def __init__(self,memory_bytes=15*1024**3):
        if os.name != 'nt' or type(memory_bytes) is not int or not 16*1024**2 <= memory_bytes <= 15*1024**3:
            raise ReleaseError('unsupported controller memory bound')
        from scripts.agent_handoff import WindowsJob
        from discovery.orb_solo_executor import _native_types
        from types import SimpleNamespace
        self.job=WindowsJob.create()
        c,w=self.job._ctypes,self.job._wintypes
        Extended,_=_native_types(self.job)
        info=Extended()
        info.basic.flags=0x200|0x8  # aggregate memory + active-process ceiling
        info.basic.active_limit=4  # one controller, one worker and venv launchers
        info.job_memory=memory_bytes
        if not self.job._kernel.SetInformationJobObject(self.job.handle,9,c.byref(info),c.sizeof(info)):
            self.job.close()
            raise ReleaseError('native controller memory limit unavailable')
        self.job._kernel.GetCurrentProcess.restype=w.HANDLE
        try:
            self.job.assign(SimpleNamespace(_handle=self.job._kernel.GetCurrentProcess()))
        except BaseException:
            self.job.close()
            raise
        self.memory_bytes=memory_bytes

    def close(self):
        self.job.close()


class PhaseWatchdog:
    """Threaded native accounting/deadline stop for GIL-releasing preflight.

    A forced stop leaves the durable reservation unresolved; it cannot release
    another phase. The native job includes this controller and all descendants.
    Native controller calls holding the GIL can delay this thread: that lifecycle
    resource gap remains a release blocker, not an unconditional hard wall bound.
    """
    def __init__(self,job,*,cpu_ceiling,initialization_allowance,wall_deadline):
        import threading
        self.job=job
        self.cpu_ceiling=cpu_ceiling
        self.allowance=initialization_allowance
        self.deadline=wall_deadline
        if not all(math.isfinite(v) for v in (cpu_ceiling,initialization_allowance,wall_deadline)) or cpu_ceiling<=0 or initialization_allowance<0:
            raise ReleaseError('invalid watchdog limits')
        self.event=threading.Event()
        self.thread=threading.Thread(target=self._watch,daemon=True)

    def start(self):
        self.thread.start()

    def stop(self):
        self.event.set()
        self.thread.join(timeout=2)
        if self.thread.is_alive():
            self.job.terminate()
            os._exit(70)

    def _watch(self):
        import time
        last_cpu=0.
        last_time=time.monotonic()
        try:
            while not self.event.is_set():
                now=time.monotonic()
                info=self.job._accounting()
                returned=self.job._wintypes.DWORD()
                c=self.job._ctypes
                if not self.job._kernel.QueryInformationJobObject(self.job.handle,1,c.byref(info),c.sizeof(info),c.byref(returned)):
                    raise ReleaseError('watchdog accounting unavailable')
                cpu=(info.TotalUserTime+info.TotalKernelTime)/10000000
                if cpu<last_cpu or now-last_time>2 or now>=self.deadline or cpu+self.allowance>=self.cpu_ceiling:
                    raise ReleaseError('watchdog limit or accounting failure')
                last_cpu,last_time=cpu,now
                self.event.wait(.25)
        except BaseException:
            self.job.terminate()
            os._exit(70)


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def file_digest(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for block in iter(lambda:handle.read(1024*1024),b''):
            value.update(block)
    return value.hexdigest()


class BoundedText(io.TextIOBase):
    def __init__(self,target,*,limit=MAX_CAPTURE_BYTES):
        if type(limit) is not int or limit <= 0 or limit > MAX_CAPTURE_BYTES:
            raise ReleaseError('invalid capture bound')
        self.target,self.limit,self.used = target,limit,0

    def write(self,text):
        size=len(text.encode('utf-8'))
        if self.used+size > self.limit:
            raise ReleaseError('capture byte limit')
        self.used+=size
        self.target.write(text)
        self.target.flush()
        return len(text)

    def flush(self):
        self.target.flush()


def atomic_json(path,value,*,limit=MAX_RECEIPT_BYTES):
    """Size-check before opening; exclusive new output, manifest publication last.

    Callers create a fresh leased output directory. No overwrite or replacement
    of an earlier attempt is permitted. A partial file is never a success marker.
    """
    data=canonical(value)
    if len(data) > limit:
        raise ReleaseError('publication exceeds declared bound')
    path=Path(path)
    with path.open('xb') as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    return hashlib.sha256(data).hexdigest()


def guarded_event(event,args):
    if event == 'socket.gethostname':
        return
    if event == 'open':
        _,mode,flags=args
        if (mode and any(char in mode for char in 'wax+')) or flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND):
            raise ReleaseError('worker file writes prohibited')
    if event.startswith(('socket.','subprocess.')) or event in (
        'os.system','os.spawn','os.fork','os.exec','os.remove','os.rename',
        'os.mkdir','os.rmdir','os.symlink','os.link','os.truncate','os.chmod',
        'os.chown','os.utime','os.setxattr','os.removexattr',
    ):
        raise ReleaseError('worker external operation prohibited')


def read_json(path,*,limit=MAX_PLAN_BYTES):
    path=Path(path)
    if path.is_symlink() or path.stat().st_size > limit:
        raise ReleaseError('unsafe or oversize input document')
    def pairs(items):
        result={}
        for key,value in items:
            if key in result:
                raise ReleaseError('duplicate document key')
            result[key]=value
        return result
    return json.loads(path.read_text(encoding='utf-8-sig'),object_pairs_hook=pairs,
                      parse_constant=lambda _: (_ for _ in ()).throw(ReleaseError('nonfinite JSON')))


class PhaseJournal:
    """Persistent aggregate budget, absolute clock and once-only phase leases."""
    def __init__(self,path):
        self.path=Path(path)
        self.lock=self.path.with_suffix(self.path.suffix+'.lease')
        self.owned=False

    @classmethod
    def create(cls,path,*,setup_charged,deadline):
        if not math.isfinite(setup_charged) or not 14.28 <= setup_charged <= 21:
            raise ReleaseError('setup charge would reset or exceed approved budget')
        end=datetime.fromisoformat(deadline)
        if end.utcoffset() is None:
            raise ReleaseError('absolute timezone-aware deadline required')
        journal=cls(path)
        atomic_json(journal.path,dict(schema='orb-s4-budget/v1',study=STUDY,
            allocation=ALLOCATIONS,charges=dict(setup=setup_charged,candidate=0.,reference=0.,seal=0.),
            deadline=end.isoformat(),status='idle',completed=[],receipts={},plan_sha256=None,
            reserved_phase_cpu_hours=0.,active_phase=None))
        return journal

    def read(self):
        state=read_json(self.path)
        try:
            charges=state['charges']
            if state['schema'] != 'orb-s4-budget/v1' or state['study'] != STUDY or state['allocation'] != ALLOCATIONS:
                raise ReleaseError('budget identity or allocation drift')
            if set(charges) != set(ALLOCATIONS) or charges['setup'] < 14.28:
                raise ReleaseError('budget charge reset')
            if any(isinstance(charges[k],bool) or not math.isfinite(charges[k]) or not 0 <= charges[k] <= ALLOCATIONS[k] for k in charges):
                raise ReleaseError('invalid phase charge')
            if sum(charges.values()) > 42 or state['status'] not in ('idle','running','sealing','unknown','failed'):
                raise ReleaseError('invalid aggregate budget state')
            for phase in state['completed']:
                published=state['receipts'][phase]
                path=Path(published['path'])
                if not path.resolve().is_relative_to(self.path.resolve().parent) or path.stat().st_size>MAX_RECEIPT_BYTES or file_digest(path)!=published['sha256']:
                    raise ReleaseError('completed phase publication missing or changed')
            return state
        except (KeyError,TypeError,ValueError,OSError) as exc:
            raise ReleaseError('malformed budget') from exc

    def _write(self,state):
        pending=self.path.with_suffix(self.path.suffix+'.pending')
        atomic_json(pending,state)
        os.replace(pending,self.path)

    def begin(self,phase,plan_sha256,*,now=None):
        if phase not in ('candidate','reference','seal') or re.fullmatch('[0-9a-f]{64}',plan_sha256) is None:
            raise ReleaseError('invalid phase or plan identity')
        now=now or datetime.now(timezone.utc)
        def check(state):
            if now.utcoffset() is None or now >= datetime.fromisoformat(state['deadline']):
                raise ReleaseError('absolute study deadline reached')
            if state['status'] != 'idle' or phase in state['completed'] or state['charges'][phase]:
                raise ReleaseError('phase restart or unresolved prior attempt')
            if state['plan_sha256'] not in (None,plan_sha256):
                raise ReleaseError('frozen configuration drift')
            if phase == 'reference' and 'candidate' not in state['completed']:
                raise ReleaseError('candidate precedes reference')
            if phase == 'seal' and set(state['completed']) != {'candidate','reference'}:
                raise ReleaseError('both populations precede sealing')
        check(self.read())
        try:
            with self.lock.open('x',encoding='utf-8') as handle:
                handle.write(str(os.getpid()))
                handle.flush(); os.fsync(handle.fileno())
        except FileExistsError as exc:
            raise ReleaseError('unresolved budget lease; restart refused') from exc
        self.owned=True
        state=self.read()
        check(state)
        state.update(status='running',active_phase=phase,plan_sha256=plan_sha256,
                     reserved_phase_cpu_hours=ALLOCATIONS[phase])
        self._write(state)
        return state

    def finish(self,*,cpu_seconds,complete,receipt_path=None,receipt=None):
        if not self.owned or not math.isfinite(cpu_seconds) or cpu_seconds < 0:
            raise ReleaseError('invalid completion or missing lease')
        state=self.read()
        if state['status'] not in ('running','sealing'):
            raise ReleaseError('no running attempt')
        phase=state['active_phase']
        if complete:
            charge=(cpu_seconds+SEAL_RESERVE_SECONDS)/3600
            if charge > state['reserved_phase_cpu_hours']:
                raise ReleaseError('phase ceiling exceeded')
            if receipt_path is None or not isinstance(receipt,dict):
                raise ReleaseError('confirmed publication required before phase advance')
            receipt_path=Path(receipt_path).absolute()
            if receipt_path.resolve()!=receipt_path or not receipt_path.is_relative_to(self.path.resolve().parent):
                raise ReleaseError('phase publication outside leased journal custody')
            # Reserve the full phase through the commit boundary. A controller
            # crash at either write leaves sealing + lease and cannot advance.
            state['status']='sealing'
            state['charges'][phase]=state['reserved_phase_cpu_hours']
            self._write(state)
            final=json.loads(canonical(state))
            final['charges'][phase]=charge
            final['completed'].append(phase)
            final.update(status='idle',active_phase=None,reserved_phase_cpu_hours=0.)
            payload=dict(receipt,phase=phase,journal_configuration_sha256=state['plan_sha256'],
                         charges=final['charges'],completed=final['completed'])
            receipt_sha=atomic_json(receipt_path,payload)
            if file_digest(receipt_path)!=receipt_sha:
                raise ReleaseError('phase publication verification failed')
            final['receipts'][phase]=dict(path=str(receipt_path),sha256=receipt_sha)
            self._write(final)
            self.lock.unlink(); self.owned=False
            return final
        else:
            state['charges'][phase]=state['reserved_phase_cpu_hours']
            state['status']='unknown'
        state.update(active_phase=None,reserved_phase_cpu_hours=0.)
        self._write(state)
        self.lock.unlink(); self.owned=False
        return state


def validate_plan(plan):
    if plan.get('schema') != 'orb-s4-release/v1' or plan.get('study') != STUDY:
        raise ReleaseError('wrong study')
    if plan.get('phase') not in ('candidate','reference') or plan.get('tiers') != list(TIERS):
        raise ReleaseError('phase or frozen tier set drift')
    if plan.get('depth') != DEPTH or plan.get('mode') != 'NORMAL' or plan.get('protection') != 'OFF' or plan.get('inactivity_off') is not True:
        raise ReleaseError('depth or policy drift')
    pins=plan.get('source_pins')
    if not isinstance(pins,dict) or not pins or any(not isinstance(k,str) or not isinstance(v,str) or re.fullmatch('[0-9a-f]{64}',v) is None for k,v in pins.items()):
        raise ReleaseError('missing source identities')
    for field in ('binding_sha256','rules_sha256','input_sha256','producer_sha256','admission_sha256','freeze_contract_sha256','operator_release'):
        if not isinstance(plan.get(field),str) or re.fullmatch('[0-9a-f]{64}',plan[field]) is None:
            raise ReleaseError('missing exact release identity: '+field)
    if not isinstance(plan.get('freeze_commit'),str) or re.fullmatch('[0-9a-f]{40}',plan['freeze_commit']) is None:
        raise ReleaseError('missing effective freeze')
    if 'command' in plan or 'worker_count' in plan:
        raise ReleaseError('caller cannot choose command or worker topology')


def phase_command(plan_path,plan_sha256):
    if re.fullmatch('[0-9a-f]{64}',plan_sha256) is None:
        raise ReleaseError('invalid plan digest')
    return [sys.executable,'-B','-m','discovery.orb_solo_worker',str(Path(plan_path).resolve()),plan_sha256]


def validate_admission(admission,plan,*,derived=None):
    """Only freshly source-derived evidence can discharge the admission gate.

    The authoritative input loader/derivation is bound by the release manifest;
    caller booleans or a stored report without matching derivation never pass.
    """
    if derived is None or not isinstance(admission,dict):
        raise ReleaseError('actual pinned admission derivation required')
    if admission.get('schema') != 'orb-s4-admission/v1' or admission.get('input_sha256') != plan['input_sha256']:
        raise ReleaseError('admission input identity mismatch')
    if digest(admission) != plan['admission_sha256'] or canonical(admission) != canonical(derived):
        raise ReleaseError('admission not equal to fresh source derivation')
    for key in ('binding_sha256','rules_sha256','producer_sha256'):
        if admission.get(key) != plan[key]:
            raise ReleaseError('admission provenance mismatch')
    if set(admission.get('tiers',{})) != set(TIERS):
        raise ReleaseError('admission must enumerate frozen four tiers')
    return admission


def derive_candidate_admission(trades,daily_gross,plan):
    """Frozen Oct6 executor §0.5(4), one solo leg, filled rows counted once.

    Call only on the parser-validated, pinned, in-window capture after freeze and
    admission authorization. This pure function is tested on synthetic lots here.
    It does not change per-contract cost netting of the separate MC series.
    """
    from dataclasses import asdict
    from discovery.prop_survivor_scoring import load_scoring_thresholds, cost_law_kill, reduce_to_deployable
    from discovery.orb_solo_executor import admit_tier
    from firm_rules import FIRM_RULES
    from discovery.orb_solo_series import _validate_trades
    if not trades:
        raise ReleaseError('empty actual admission input')
    quantity=trades[0].qty
    if int(quantity) != quantity:
        raise ReleaseError('noninteger elected quantity')
    _validate_trades(trades,int(quantity))
    thr=load_scoring_thresholds()
    if thr.cost_law_multiple != 4 or thr.seeds != (42,123,2026) or thr.horizon != 1500:
        raise ReleaseError('frozen scoring criteria drift')
    gross=[trade.gross_usd for trade in trades]
    if any(not math.isfinite(value) for value in gross):
        raise ReleaseError('nonfinite source edge')
    costs={key:cost_law_kill(key,r_deploy=len(trades),gross_edge_usd=math.fsum(gross),thresholds=thr) for key in TIERS}
    verdict='YES' if any(value.passed for value in costs.values()) else 'NO'
    g1=reduce_to_deployable(gross,daily_gross,envelope_verdict=verdict)
    tiers={key:dict(g2=asdict(costs[key]),clock_cap=admit_tier(key,trades,
               micro_cap=FIRM_RULES[key]['micro_contract_cap'],g1=not g1.halted,
               cost_multiple=thr.cost_law_multiple)) for key in TIERS}
    return json_ready(dict(schema='orb-s4-admission/v1',input_sha256=plan['input_sha256'],
                binding_sha256=plan['binding_sha256'],rules_sha256=plan['rules_sha256'],
                producer_sha256=plan['producer_sha256'],g1=asdict(g1),tiers=tiers,
                basis='frozen-executor-per-leg-gross/fill-count; no size or parameter variant'))


def validate_reference_route(configuration):
    """Require a specifically frozen disposition; never invent reference trades."""
    expected=dict(kind='I20-bust-only',source='2026-10-06-executor-0.5-5',
                  panel_sha256='a2e9192aec54dd081245232247f5f5306553910a2956f3601364c050f9aa50a2',
                  cost_policy='already-net-no-additional-cost',g1_g2='documented-reference-only-bypass',
                  explicit_in_frozen_contract=True)
    if configuration.get('reference_route') != expected:
        raise ReleaseError('explicit frozen reference route required; interpretation held')
    return expected


def validate_release_authorization(release,configuration,phase,*,now=None):
    """Bind an operator-release record; it is an attestation, not a signature.

    The agent still requires direct human GO. A local JSON file cannot create
    permission by itself. No such release is emitted by preparation/tests.
    """
    now=now or datetime.now(timezone.utc)
    try:
        end=datetime.fromisoformat(release['expires_at'])
        if (release['study'] != STUDY or release['phase'] != phase or
                release['configuration_sha256'] != digest(configuration) or
                release['operator'] != 'Joshua' or release['authorized'] is not True or
                end.utcoffset() is None or now.utcoffset() is None or now >= end):
            raise ReleaseError('operator release does not bind this execution')
    except (KeyError,TypeError,ValueError) as exc:
        raise ReleaseError('missing operator release') from exc
    return release


def json_ready(value):
    """Preserve nonfinite diagnostics explicitly; never convert them to zero."""
    if value is None or isinstance(value,(str,bool,int)):
        return value
    if isinstance(value,float):
        return value if math.isfinite(value) else {'nonfinite':str(value)}
    if isinstance(value,dict):
        return {str(k):json_ready(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):
        return [json_ready(v) for v in value]
    if type(value).__module__.startswith('numpy') and hasattr(value,'item'):
        return json_ready(value.item())
    raise ReleaseError('unsupported report value type')


def configuration_of(plan):
    configuration=plan.get('configuration')
    if not isinstance(configuration,dict):
        raise ReleaseError('complete frozen two-population configuration required')
    for key,expected in (('study',STUDY),('depth',DEPTH),('tiers',list(TIERS)),
                         ('mode','NORMAL'),('protection','OFF'),('inactivity_off',True)):
        if configuration.get(key) != expected:
            raise ReleaseError('global configuration drift: '+key)
    if configuration.get('source_pins') != plan['source_pins']:
        raise ReleaseError('phase/global import identities differ')
    inputs=configuration.get('inputs')
    if not isinstance(inputs,dict) or set(inputs) != {'candidate','reference','binding','rules','candidate_admission'}:
        raise ReleaseError('exact two-population inputs/admission required')
    if any(inputs[role].get('sha256')!=expected for role,expected in FIXED_INPUT_PINS.items()):
        raise ReleaseError('elected input/reference identity changed')
    if inputs[plan['phase']]['sha256'] != plan['input_sha256']:
        raise ReleaseError('phase input not bound by global configuration')
    for role,key in (('binding','binding_sha256'),('rules','rules_sha256'),('candidate_admission','admission_sha256')):
        if inputs[role]['sha256'] != plan[key]:
            raise ReleaseError('input binding mismatch: '+role)
    validate_reference_route(configuration)
    if configuration.get('freeze') != dict(commit=plan['freeze_commit'],contract_sha256=plan['freeze_contract_sha256']):
        raise ReleaseError('freeze/global configuration mismatch')
    return configuration


def verify_host(configuration):
    """Timing evidence applies only to the same host/runtime/thread posture."""
    import platform
    if os.name!='nt':
        raise ReleaseError('verified Windows host required')
    import winreg
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r'HARDWARE\DESCRIPTION\System\CentralProcessor\0') as key:
        model=winreg.QueryValueEx(key,'ProcessorNameString')[0]
    threads={name:os.environ.get(name) for name in (
        'OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS')}
    actual=dict(platform=platform.platform(),logical_cpus=os.cpu_count(),processor=platform.processor(),
                processor_model=model,threads=threads)
    if actual!=configuration.get('host') or actual['logical_cpus']!=8 or any(value!='1' for value in threads.values()):
        raise ReleaseError('host/thread identity drift invalidates timing evidence')
    return actual


def required_source_paths(root):
    names=(
        'core/dd_protection.py','core/firm_rules.py','core/historical_challenge.py',
        'core/lib/atomic_io.py','core/lib/mvd.py','core/lib/validation.py','core/lifecycle.py',
        'core/mc/__init__.py','core/mc/ingest.py','core/mc/modes.py','core/mc/preflight.py',
        'core/mc/simulation.py','core/tv_schema.py','lab/discovery/__init__.py',
        'lab/discovery/orb_solo_series.py','lab/discovery/remc_series_builder.py',
        'lab/discovery/prop_survivor_scoring.py','lab/discovery/orb_solo_executor.py',
        'lab/discovery/orb_solo_release.py','lab/discovery/orb_solo_worker.py',
        'scripts/agent_handoff.py','requirements-ops.lock',
        'docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md',
    )
    return [Path(root)/name for name in names]


def verify_frozen_sources(plan,root):
    from discovery.orb_solo_executor import verify_identity
    expected={str(path.resolve()) for path in required_source_paths(root)}|{str(Path(sys.executable).resolve())}
    if set(plan['source_pins']) != expected:
        raise ReleaseError('executed import/dependency closure must match exactly')
    verify_identity(plan['source_pins'])
    if plan['producer_sha256'] != plan['source_pins'][str((root/'lab/discovery/orb_solo_series.py').resolve())]:
        raise ReleaseError('producer identity mismatch')


def verify_effective_freeze(plan,root):
    """Read-only local Git proof. Operator/combined acceptance still required."""
    import subprocess
    commit=plan['freeze_commit']
    check=subprocess.run(['git','merge-base','--is-ancestor',commit,'origin/main'],cwd=root,
                         capture_output=True,timeout=5)
    if check.returncode:
        raise ReleaseError('effective approved main freeze not established')
    name='docs/briefs/pre-registration/2026-10-17-orb-mnq-v7-s4-prereg-DRAFT.md'
    result=subprocess.run(['git','show',commit+':'+name],cwd=root,capture_output=True,timeout=5)
    if result.returncode or len(result.stdout)>MAX_PLAN_BYTES or hashlib.sha256(result.stdout).hexdigest()!=plan['freeze_contract_sha256']:
        raise ReleaseError('frozen contract bytes not bound')
    required=b'Reference scoring: I20-bust-only; G1/G2 reference-only bypass; no additional costs'
    if required not in result.stdout:
        raise ReleaseError('reference-route interpretation not explicitly frozen')
    # Public scientific code must be the reviewed frozen code, allowing checkout
    # CRLF normalization only. Private data/source bodies are never Git-showed.
    for path in required_source_paths(root):
        if path.suffix != '.py':
            continue
        relative=path.relative_to(root).as_posix()
        blob=subprocess.run(['git','show',commit+':'+relative],cwd=root,capture_output=True,timeout=5)
        if blob.returncode or len(blob.stdout)>MAX_RECEIPT_BYTES or blob.stdout.replace(b'\r\n',b'\n')!=path.read_bytes().replace(b'\r\n',b'\n'):
            raise ReleaseError('executed source differs from effective freeze: '+relative)


def study_disk_bytes(root):
    count=total=0
    for path in Path(root).rglob('*'):
        count+=1
        if count>65536:
            raise ReleaseError('study artifact-count bound')
        if path.is_symlink() or getattr(path,'is_junction',lambda:False)():
            total+=4096  # never follow existing test/archive links
        elif path.is_file():
            total+=path.stat().st_size
    return total


def _launch_fixed_worker(command,*,root,output,pins,limits):
    from discovery.orb_solo_executor import run_owned
    return run_owned([command],cwd=root,output=output,pins=pins,limits=limits)


def execute_phase(plan_path,expected_sha256,*,journal_path,output):
    """The only qualification dispatch: fixed module/one role/no caller commands.

    Never invoke without separately authorized admission/freeze/scoring release.
    Preparation tests exercise refusal and control mode, never this qualified run.
    """
    import time
    from dataclasses import replace
    from discovery.orb_solo_executor import Limits
    start=time.monotonic(); cpu_start=time.process_time()
    root=Path(__file__).resolve().parents[2]
    plan_path=Path(plan_path).resolve()
    plan=read_json(plan_path)
    if file_digest(plan_path)!=expected_sha256:
        raise ReleaseError('plan bytes differ from release')
    validate_plan(plan)
    configuration=configuration_of(plan)
    # No worktree input copy: actual release is primary-checkout-only.
    custody=root/'.cache/orb-mnq-v7-s4-2026-10'
    output=Path(output).absolute()
    journal_path=Path(journal_path).absolute()
    if journal_path!=custody/'execution-budget.json':
        raise ReleaseError('one canonical execution journal; new path cannot reset phases')
    for path in (plan_path,output,journal_path):
        if not path.is_relative_to(custody) or path.resolve()!=path:
            raise ReleaseError('execution paths outside primary study custody')
    if not (root/'.git').is_dir():
        raise ReleaseError('private qualification execution requires primary checkout')
    # A single explicit conservative allowance covers all process CPU accrued
    # before native self-job association, including interpreter/import startup.
    # It is not another measured counter and is never accumulated per sample.
    hard_memory=ControllerMemoryJob()
    initialization_allowance=max(1,math.ceil(time.process_time()))
    journal=PhaseJournal(journal_path)
    watchdog=None
    launched=False
    result=None
    try:
        state=journal.begin(plan['phase'],digest(configuration))
        remaining_wall=(datetime.fromisoformat(state['deadline'])-datetime.now(timezone.utc)).total_seconds()
        remaining_global=(42-sum(state['charges'].values()))*3600
        work_cap=min((ALLOCATIONS[plan['phase']]-1.5)*3600,remaining_global)
        watchdog=PhaseWatchdog(hard_memory.job,cpu_ceiling=work_cap-SEAL_RESERVE_SECONDS,
            initialization_allowance=initialization_allowance,wall_deadline=time.monotonic()+remaining_wall-90)
        watchdog.start()
        from datetime import timedelta
        budget=read_json(custody/'budget.private.json')
        if state['charges']['setup']!=budget['charged_setup_cpu_hours']:
            raise ReleaseError('execution journal would reset current setup charge')
        anchor=datetime.fromisoformat('2026-10-17T00:07:02-04:00')
        if datetime.fromisoformat(state['deadline'])>anchor+timedelta(hours=48):
            raise ReleaseError('absolute study wall clock cannot reset')
        verify_host(configuration)
        verify_frozen_sources(plan,root)
        verify_effective_freeze(plan,root)
        all_pins=dict(plan['source_pins'])
        for role,entry in configuration['inputs'].items():
            path=Path(entry['path']).resolve()
            if path.is_symlink() or path.stat().st_size>128*1024**2 or file_digest(path)!=entry['sha256']:
                raise ReleaseError('input identity/size failure: '+role)
            all_pins[str(path)]=entry['sha256']
        release_path=Path(plan.get('operator_release_path','')).resolve()
        release=read_json(release_path)
        if digest(release)!=plan['operator_release']:
            raise ReleaseError('operator release bytes mismatch')
        validate_release_authorization(release,configuration,plan['phase'])
        all_pins[str(plan_path)]=expected_sha256
        all_pins[str(release_path)]=file_digest(release_path)
        # Reserve a hard, finite space envelope for both populations, control
        # receipts and sealing. Worker can write only bounded stdout/stderr.
        if study_disk_bytes(custody)+256*1024**2>2*1024**3:
            raise ReleaseError('insufficient whole-study disk reserve')
        output.mkdir(parents=True,exist_ok=False)
        from discovery.orb_solo_executor import _native_sample
        # The self Job includes completed preflight children (including Git).
        # Do not sum per-PID totals or count the controller a second time.
        init_cpu=_native_sample(hard_memory.job)[0]+initialization_allowance
        remaining_wall=(datetime.fromisoformat(state['deadline'])-datetime.now(timezone.utc)).total_seconds()
        remaining_global=(42-sum(state['charges'].values()))*3600
        work_cap=min((ALLOCATIONS[plan['phase']]-1.5)*3600,remaining_global)
        limits=replace(Limits(),prior_cpu_seconds=init_cpu,phase_cpu_seconds=work_cap,
                       total_cpu_seconds=work_cap,wall_seconds=remaining_wall-90,
                       poll_seconds=.25,max_sample_gap=2,disk_bytes=72*1024**2,disk_reserve_bytes=4*1024**2)
        limits.validate()
        launched=True
        result=_launch_fixed_worker(phase_command(plan_path,expected_sha256),root=root,
                                    output=output/'owned',pins=all_pins,limits=limits)
        completed=(result['status']=='completed' and result['accounting_complete'] and result['active_processes']==0)
        document=None
        if completed:
            document=read_json(output/'owned/worker-0.stdout',limit=MAX_CAPTURE_BYTES)
            completed=(document.get('phase_status')=='completed' and document.get('plan_sha256')==expected_sha256
                       and document.get('depth')==DEPTH and document.get('phase')==plan['phase'])
        # Fixed-size controller evidence; publication marker is written last.
        measured_cpu=_native_sample(hard_memory.job)[0]
        charge=measured_cpu+initialization_allowance
        publication=dict(status='completed' if completed else 'stopped',
                    plan_sha256=expected_sha256,configuration_sha256=digest(configuration),
                    elapsed=time.monotonic()-start,cpu_seconds=charge,
                    measured_owned_job_cpu_seconds=measured_cpu,
                    conservative_initialization_allowance_seconds=initialization_allowance,
                    max_capture_bytes=MAX_CAPTURE_BYTES,worker_roles=1,
                    worker_document_sha256=file_digest(output/'owned/worker-0.stdout'))
        state=journal.finish(cpu_seconds=charge,complete=completed,
                             receipt_path=output/'phase-receipt.json',receipt=publication)
        if not completed:
            atomic_json(output/'phase-receipt.json',publication)
        if not completed:
            raise ReleaseError('phase incomplete; no retry')
        return document
    except BaseException:
        if journal.owned:
            # Native child job cleanup occurs inside run_owned. Missing terminal
            # evidence consumes the full phase reservation and blocks all restart.
            journal.finish(cpu_seconds=0,complete=False)
        raise
    finally:
        if watchdog is not None:
            watchdog.stop()
        hard_memory.close()
