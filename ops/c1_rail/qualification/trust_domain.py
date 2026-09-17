"""Signed qualification trust domains and explicit TEST_ONLY composition policy.

Domain workload declarations do not ratify an execution depth by themselves:
consumers must also match the frozen contract and exact-depth approval. Proposed
N1/N2/N3 depths are deliberately absent from the compiled production policy.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
from types import MappingProxyType
import weakref

from .contract import (ACCEPTED_HISTORICAL_PINS,REQUIRED_ARTIFACT_ROLES,
    HISTORICAL_EFFECTIVE_INPUTS,canonical_json_bytes,parse_canonical_json,
    verify_detached_approval)
from c1_rail.ed25519_verify import is_strong_public_key
from c1_signal_daemon.book_adapters import ADAPTERS


SCHEMA='qualification_trust_domain/v1'
_PORT_ROLES={'aegis_runtime_port':'aegis_6j','striker_runtime_port':'dj30_mym_p250',
             'vanguard_runtime_port':'vanguard_mgc','orb_runtime_port':'orb_mnq_v7'}
_STAGES={'LEGALITY':(),'N1':('FULL','H1','H2'),'N2':('FULL',),
         'PART_B':('H1','H2'),'PART_A':('REGIME',),'N3':('FULL','H1','H2')}
_ISSUED={}


def _hash(value):
    if type(value) is not str or len(value)!=64 or any(c not in '0123456789abcdef' for c in value):
        raise ValueError('canonical SHA256 required')
    return value


def _text(value):
    if type(value) is not str or not value or value.strip()!=value:raise ValueError('nonempty canonical text required')
    return value


def _positive(value):
    if type(value) is not int or value<=0:raise ValueError('positive integer required')
    return value


def _mapping(values):
    return MappingProxyType(dict(sorted(values.items())))


def _fields(value,names):
    if type(value) is not dict or set(value)!=set(names):raise ValueError('closed schema fields required')
    return value


def _names(values):
    if type(values) not in (list,tuple) or not values or any(type(v) is not str or not v for v in values):
        raise ValueError('nonempty name inventory required')
    if list(values)!=sorted(set(values)):raise ValueError('sorted unique name inventory required')
    return tuple(values)


@dataclass(frozen=True)
class QualificationWorkloadPolicy:
    stage_population_depths: object
    horizon_sessions: int
    inner_block_sessions: int
    outer_months: int
    part_a_initial_panels: int
    part_a_expanded_panels: int
    part_a_paths_per_population_per_panel: int

    def __post_init__(self):
        counts=self.stage_population_depths
        if set(counts)!=set(_STAGES):raise ValueError('closed workload stage inventory required')
        normalized={}
        for stage,pops in _STAGES.items():
            if set(counts[stage])!=set(pops):raise ValueError('closed workload population inventory required')
            normalized[stage]={}
            for pop in pops:
                values=counts[stage][pop]
                if type(values) not in (list,tuple) or not values:raise ValueError('nonempty depth tuple required')
                numbers=tuple(_positive(v) for v in values)
                if numbers!=tuple(sorted(set(numbers))):raise ValueError('sorted unique workload depths required')
                if stage!='PART_A' and len(numbers)!=1:raise ValueError('single exact stage depth required')
                normalized[stage][pop]=numbers
            normalized[stage]=_mapping(normalized[stage])
        for name in ('horizon_sessions','inner_block_sessions','outer_months','part_a_initial_panels',
                     'part_a_expanded_panels','part_a_paths_per_population_per_panel'):
            _positive(getattr(self,name))
        if self.horizon_sessions%self.inner_block_sessions:raise ValueError('horizon must be divisible by inner block')
        if self.part_a_expanded_panels<=self.part_a_initial_panels:raise ValueError('expanded panels must exceed initial panels')
        if normalized['PART_A']['REGIME']!=(self.part_a_initial_panels,self.part_a_expanded_panels):
            raise ValueError('Part A population counts must equal frozen panel counts')
        for stage in ('N1','N3'):
            if len(set(normalized[stage].values()))!=1:raise ValueError('joint population depths differ')
        if any(v!=normalized['N2']['FULL'] for v in normalized['PART_B'].values()):
            raise ValueError('N2 and Part B depths differ')
        object.__setattr__(self,'stage_population_depths',_mapping(normalized))


@dataclass(frozen=True)
class PortRuntimePin:
    leg_id: str
    runtime_sha256: str
    pine_sha256: str

    def __post_init__(self):
        if self.leg_id not in _PORT_ROLES.values():raise ValueError('unknown port leg')
        _hash(self.runtime_sha256);_hash(self.pine_sha256)


def _pins(values):
    if set(values)!=set(_PORT_ROLES.values()):raise ValueError('exact four port pins required')
    for leg,pin in values.items():
        if type(pin) is not PortRuntimePin or pin.leg_id!=leg:raise ValueError('port pin leg differs')
    return _mapping(values)


@dataclass(frozen=True)
class TrustDomainPolicy:
    authority_class: str
    permits_synthetic: bool
    required_roles: tuple[str,...]
    required_code_roles: object
    production_workload_required: bool
    accepted_historical_pins: object
    port_runtime_pins: object
    effective_settings_sha256: str | None = None
    workload_policy: QualificationWorkloadPolicy | None = None

    def __post_init__(self):
        object.__setattr__(self,'required_roles',tuple(sorted(set(self.required_roles))))
        object.__setattr__(self,'required_code_roles',_mapping(self.required_code_roles))
        object.__setattr__(self,'accepted_historical_pins',_mapping(self.accepted_historical_pins))
        object.__setattr__(self,'port_runtime_pins',_pins(self.port_runtime_pins))


_PRODUCTION_CODE={
    'qualification_runner':'c1_rail.qualification.orchestration',
    'replay_kernel':'c1_rail.qualification.replay','path_sampler':'c1_rail.qualification.paths',
    'rng_allocation':'c1_rail.qualification.regime','part_a_runner':'c1_rail.qualification.part_a',
    'qualification_adjudicator':'c1_rail.qualification.result_adjudication',
    'qualification_sealer':'c1_rail.qualification.seal',
    'listener_account_owner':'c1_rail.book_account_owner',
    'qualification_adjudication_rules':'c1_rail.qualification.adjudication',
    'qualification_model':'c1_rail.qualification.model',
    'qualification_certification_power':'scripts.certification_power',
    **{role:'fp_qualification_port_'+leg for role,leg in _PORT_ROLES.items()},
}
PRODUCTION_TRUST_POLICY=TrustDomainPolicy('OPERATOR',False,
    tuple(sorted(set(REQUIRED_ARTIFACT_ROLES)|set(_PRODUCTION_CODE))),_PRODUCTION_CODE,True,
    ACCEPTED_HISTORICAL_PINS,{spec.leg_id:PortRuntimePin(spec.leg_id,spec.runtime_sha256,spec.pine_sha256) for spec in ADAPTERS})


def _composition_test_trust_policy(*,accepted_historical_pins,required_artifact_roles,
        runtime_code_roles,port_runtime_pins,effective_settings_sha256,workload_policy):
    """Internal TEST_ONLY fixture seam; never grants production authority."""
    if type(workload_policy) is not QualificationWorkloadPolicy:raise TypeError('exact workload policy required')
    _hash(effective_settings_sha256)
    for digest in accepted_historical_pins.values():_hash(digest)
    return TrustDomainPolicy('TEST_ONLY',True,tuple(required_artifact_roles),runtime_code_roles,False,
        accepted_historical_pins,port_runtime_pins,effective_settings_sha256,workload_policy)


@dataclass(frozen=True)
class QualificationTrustDomain:
    schema: str
    domain_id: str
    authority_class: str
    permits_synthetic: bool
    freeze_key_ids: tuple[str,...]
    result_key_ids: tuple[str,...]
    seal_key_ids: tuple[str,...]
    trusted_key_sha256: object
    accepted_historical_pins: object
    required_artifact_roles: tuple[str,...]
    runtime_code_roles: object
    port_runtime_pins: object
    effective_settings_sha256: str
    workload_policy: QualificationWorkloadPolicy
    canonical_bytes: bytes
    sha256: str


def _workload_dict(workload):
    return {name:({stage:{pop:list(counts) for pop,counts in populations.items()}
                    for stage,populations in workload.stage_population_depths.items()}
                 if name=='stage_population_depths' else getattr(workload,name))
            for name in QualificationWorkloadPolicy.__dataclass_fields__}


def _policy_bytes(policy):
    return canonical_json_bytes({
        'authority_class':policy.authority_class,'permits_synthetic':policy.permits_synthetic,
        'required_roles':list(policy.required_roles),'required_code_roles':dict(policy.required_code_roles),
        'production_workload_required':policy.production_workload_required,
        'accepted_historical_pins':dict(policy.accepted_historical_pins),
        'port_runtime_pins':{leg:{'leg_id':pin.leg_id,'runtime_sha256':pin.runtime_sha256,
                                  'pine_sha256':pin.pine_sha256} for leg,pin in policy.port_runtime_pins.items()},
        'effective_settings_sha256':policy.effective_settings_sha256,
        'workload_policy':None if policy.workload_policy is None else _workload_dict(policy.workload_policy),
    })


def _require_compiled_policy_unchanged(policy,*,compiled=PRODUCTION_TRUST_POLICY,
        baseline=_policy_bytes(PRODUCTION_TRUST_POLICY)):
    # Defaults capture the original object and immutable deep snapshot once.
    # Check before branching on any mutable field of the selected policy.
    try:unchanged=_policy_bytes(compiled)==baseline
    except (AttributeError,TypeError,ValueError):unchanged=False
    if not unchanged:raise ValueError('compiled production policy changed')
    if policy.authority_class=='OPERATOR' and policy is not compiled:
        raise ValueError('compiled production policy required')


def _domain_dict(domain):
    return {'schema':domain.schema,'domain_id':domain.domain_id,'authority_class':domain.authority_class,
        'permits_synthetic':domain.permits_synthetic,'freeze_key_ids':list(domain.freeze_key_ids),
        'result_key_ids':list(domain.result_key_ids),'seal_key_ids':list(domain.seal_key_ids),
        'trusted_key_sha256':dict(domain.trusted_key_sha256),
        'accepted_historical_pins':dict(domain.accepted_historical_pins),
        'required_artifact_roles':list(domain.required_artifact_roles),'runtime_code_roles':dict(domain.runtime_code_roles),
        'port_runtime_pins':{leg:{'leg_id':pin.leg_id,'runtime_sha256':pin.runtime_sha256,'pine_sha256':pin.pine_sha256}
                             for leg,pin in domain.port_runtime_pins.items()},
        'effective_settings_sha256':domain.effective_settings_sha256,'workload_policy':_workload_dict(domain.workload_policy)}


def require_validated_trust_domain(domain):
    """Reject reconstructed receipts and mutation of an issued frozen object."""
    issued=_ISSUED.get(id(domain))
    if type(domain) is not QualificationTrustDomain or issued is None or issued[0]() is not domain:
        raise ValueError('validator-issued trust domain required')
    raw=canonical_json_bytes(_domain_dict(domain))
    if raw!=issued[1] or domain.canonical_bytes!=raw or domain.sha256!=hashlib.sha256(raw).hexdigest():
        raise ValueError('validated trust domain fields changed')
    return domain


def require_trusted_domain_key(domain,key_id,public_key):
    """Check signed key bytes; consumers still enforce scope and revocation."""
    require_validated_trust_domain(domain)
    if (type(public_key) is not bytes or len(public_key)!=32
            or domain.trusted_key_sha256.get(key_id)!=hashlib.sha256(public_key).hexdigest()):
        raise ValueError('domain key fingerprint differs or key is not enrolled')


def validate_qualification_trust_domain(domain_bytes,approval_bytes,trusted_keys,*,policy,now):
    if type(policy) is not TrustDomainPolicy:raise TypeError('exact trust policy required')
    _require_compiled_policy_unchanged(policy)
    if type(domain_bytes) is not bytes or type(approval_bytes) is not bytes:
        raise TypeError('domain and approval require immutable bytes')
    if policy.authority_class not in ('OPERATOR','TEST_ONLY'):raise ValueError('unsupported policy authority')
    fields=set(QualificationTrustDomain.__dataclass_fields__)-{'canonical_bytes','sha256'}
    doc=_fields(parse_canonical_json(domain_bytes,label='trust domain'),fields)
    if doc['schema']!=SCHEMA:raise ValueError('unsupported trust domain schema')
    if doc['authority_class']!=policy.authority_class or doc['permits_synthetic'] is not policy.permits_synthetic:
        raise ValueError('domain authority/synthetic policy differs')
    if policy.authority_class=='TEST_ONLY' and policy.permits_synthetic is not True:
        raise ValueError('composition policy must remain TEST_ONLY synthetic')
    domain_id=_text(doc['domain_id'])
    keys_by_scope={name:_names(doc[name]) for name in ('freeze_key_ids','result_key_ids','seal_key_ids')}
    enrolled=set().union(*keys_by_scope.values())
    key_fingerprints=doc['trusted_key_sha256']
    if type(key_fingerprints) is not dict or set(key_fingerprints)!=enrolled:
        raise ValueError('domain key fingerprint inventory differs from enrolled key union')
    for key_id in enrolled:
        _hash(key_fingerprints[key_id])
        key=trusted_keys.get(key_id)
        if key is None or key.key_id!=key_id:raise ValueError('domain key is not trusted')
        if key.authority_class!=policy.authority_class:raise ValueError('mixed domain key authority')
        if not is_strong_public_key(key.public_key):raise ValueError('domain key must be strong Ed25519')
        if type(key.public_key) is not bytes or hashlib.sha256(key.public_key).hexdigest()!=key_fingerprints[key_id]:
            raise ValueError('domain key fingerprint differs from actual trusted public key')
        if key.revoked_at is not None and key.revoked_at<=now:raise ValueError('domain key revoked')
    roles=_names(doc['required_artifact_roles'])
    if not set(policy.required_roles)<=set(roles):raise ValueError('mandatory artifact role omitted')
    historical=doc['accepted_historical_pins']
    if type(historical) is not dict or historical!=dict(policy.accepted_historical_pins):
        raise ValueError('accepted historical pins differ')
    if not set(historical)<=set(roles):raise ValueError('historical pin role missing')
    for digest in historical.values():_hash(digest)
    code=doc['runtime_code_roles']
    if type(code) is not dict or not set(code)<=set(roles):raise ValueError('runtime code role inventory differs')
    for role,name in policy.required_code_roles.items():
        if code.get(role)!=name:raise ValueError('mandatory runtime code role/name omitted or changed')
    if len(set(code.values()))!=len(code):raise ValueError('duplicate runtime module roles')
    for name in code.values():
        if type(name) is not str or not all(part.isidentifier() for part in name.split('.')):
            raise ValueError('canonical runtime module name required')
        if name.startswith(('ops.c1_rail','ops.c1_signal_daemon','core.')):
            raise ValueError('runtime import alias forbidden')
    rawpins=_fields(doc['port_runtime_pins'],_PORT_ROLES.values())
    pins={leg:PortRuntimePin(**_fields(value,{'leg_id','runtime_sha256','pine_sha256'})) for leg,value in rawpins.items()}
    pins=_pins(pins)
    if dict(pins)!=dict(policy.port_runtime_pins):raise ValueError('port runtime/Pine pins differ')
    for role,leg in _PORT_ROLES.items():
        if historical.get(role)!=pins[leg].runtime_sha256 or code.get(role)!='fp_qualification_port_'+leg:
            raise ValueError('closed port role/hash/module binding differs')
    settings=_hash(doc['effective_settings_sha256'])
    if policy.effective_settings_sha256 is not None and settings!=policy.effective_settings_sha256:
        raise ValueError('effective settings pin differs')
    if policy.authority_class=='OPERATOR' and settings==HISTORICAL_EFFECTIVE_INPUTS:
        raise ValueError('historical settings are not the reviewed successor')
    workload=QualificationWorkloadPolicy(**_fields(doc['workload_policy'],QualificationWorkloadPolicy.__dataclass_fields__))
    if policy.workload_policy is not None and workload!=policy.workload_policy:raise ValueError('workload policy differs')
    if policy.production_workload_required and (workload.part_a_initial_panels,workload.part_a_expanded_panels)!=(100,200):
        raise ValueError('production Part A requires fixed 100/200 panels')
    if policy.production_workload_required and (workload.outer_months,workload.inner_block_sessions)!=(6,5):
        raise ValueError('production block structure requires 6 months and 5 sessions')
    digest=hashlib.sha256(domain_bytes).hexdigest()
    approval=verify_detached_approval(approval_bytes,trusted_keys=trusted_keys,
        expected_scope='BIND_QUALIFICATION_TRUST_DOMAIN',expected_subject_sha256=digest,
        expected_contract_sha256=digest,now=now,allow_test_authority=policy.authority_class=='TEST_ONLY')
    if approval.authority_class!=policy.authority_class or approval.key_id not in keys_by_scope['freeze_key_ids']:
        raise ValueError('domain binding signer not enrolled for freeze authority')
    domain=QualificationTrustDomain(SCHEMA,domain_id,policy.authority_class,policy.permits_synthetic,
        keys_by_scope['freeze_key_ids'],keys_by_scope['result_key_ids'],keys_by_scope['seal_key_ids'],
        _mapping(key_fingerprints),_mapping(historical),roles,_mapping(code),pins,settings,workload,domain_bytes,digest)
    if canonical_json_bytes(_domain_dict(domain))!=domain_bytes:raise ValueError('domain normalization differs from retained bytes')
    identity=id(domain)
    _ISSUED[identity]=(weakref.ref(domain,lambda ref:_ISSUED.pop(identity,None)),domain_bytes)
    return domain


def production_trust_domain(domain_bytes,approval_bytes,trusted_keys,*,now):
    return validate_qualification_trust_domain(domain_bytes,approval_bytes,trusted_keys,
        policy=PRODUCTION_TRUST_POLICY,now=now)
