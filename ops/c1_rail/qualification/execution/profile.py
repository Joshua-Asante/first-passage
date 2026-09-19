"""Canonical administrator-selected N1 isolation configuration."""
from dataclasses import dataclass
from types import MappingProxyType

from ..contract import parse_canonical_json
from .protocol import fields, positive, sha256

_FIXED = {
    'schema': 'qualification_execution_profile/v1', 'protocol_version': 1,
    'supported_checkpoints': ['N1'], 'capability': 'N1_ONLY',
    'production_execution': False, 'network': 'none', 'read_only': True,
    'capabilities': [], 'no_new_privileges': True, 'privileged': False,
    'pid_mode': 'private', 'ipc_mode': 'private', 'restart': 'no',
}
_LIMITS = ('input_byte_limit', 'output_byte_limit', 'log_byte_limit', 'rpc_byte_limit',
           'worker_uid', 'memory_bytes', 'pids_limit', 'scratch_bytes',
           'admission_seconds', 'capture_seconds')


@dataclass(frozen=True)
class ExecutionProfile:
    canonical_bytes: bytes
    values: object

    @property
    def sha256(self):
        return sha256(self.canonical_bytes)

    def __getattr__(self, name):
        try:
            return self.values[name]
        except KeyError as exc:
            raise AttributeError(name) from exc


# The installed identity includes attribution and the finite launch allowance.
CAMPAIGN_RESOURCE_SCOPE = MappingProxyType(dict(
    schema='qualification_campaign_resource_scope/v1',
    platform='shared_daemons_outside_scope_excluded',
    memory='shared_host_parent_conservative',
    cpu='payload_raw_plus_full_controller_bound',
    wall='original_boottime_including_platform_waits',
    control_calls=3, control_cpu_seconds=1, control_wall_seconds=10, cpu_granularity_seconds=1,
    controller_environment=dict(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')))


_DIAGNOSTIC_FIXED = MappingProxyType(dict(_FIXED,
    schema='qualification_execution_profile/v3', protocol_version=3,
    supported_checkpoints=[], capability='FULL_E1', dispatch_enabled=False,
    diagnostic_work_enabled=True, docker_cgroup_driver='systemd',
    resource_scope=dict(CAMPAIGN_RESOURCE_SCOPE)))


def parse_profile(raw: bytes) -> ExecutionProfile:
    doc = parse_canonical_json(raw, label='execution profile')
    if type(doc) is not dict:
        raise ValueError('closed schema object required')
    fixed = _FIXED
    if doc.get('schema') == 'qualification_execution_profile/v2':
        fixed = dict(_FIXED, schema='qualification_execution_profile/v2', protocol_version=2,
            supported_checkpoints=[], capability='FULL_E1', dispatch_enabled=False)
    if doc.get('schema') == 'qualification_execution_profile/v3':
        fixed = dict(_DIAGNOSTIC_FIXED)
    fields(doc, (*fixed, *_LIMITS))
    for name, value in fixed.items():
        if type(doc[name]) is not type(value) or doc[name] != value:
            raise ValueError(f'unsupported execution profile {name}')
    for name in _LIMITS:
        positive(doc[name])
    if doc['worker_uid'] >= 2**32 - 1:
        raise ValueError('worker UID out of range')
    if any(doc[name] > 2**32 - 1 for name in ('output_byte_limit', 'rpc_byte_limit')):
        raise ValueError('transport byte limit out of range')
    if doc['capability'] == 'FULL_E1':
        from .campaign_protocol import CAMPAIGN_RPC_MINIMUM
        if doc['rpc_byte_limit'] < CAMPAIGN_RPC_MINIMUM:
            raise ValueError('campaign chunk transport requires bounded response capacity')
    return ExecutionProfile(raw, MappingProxyType({
        key: tuple(value) if type(value) is list else value for key, value in doc.items()}))


def parse_campaign_budget_profile(raw: bytes) -> dict:
    """Resolved installed phase ceilings; not an executable release/profile.

    S2 must bind these exact bytes to its installed release. No defaults or
    statistical constants are inferred here. PART_A includes maximum expansion;
    capture phases include attestation, RESULT/SEAL include finalization.
    """
    from .campaign_budget import PHASES, limits, integer
    from .protocol import digest
    doc = parse_canonical_json(raw, label='campaign budget profile')
    revised = type(doc) is dict and doc.get('schema') == 'qualification_campaign_budget_profile/v2'
    fields(doc, {'schema', 'installed_profile_sha256', 'phases', 'record_byte_limit'} |
           ({'orchestration_cpu_ns'} if revised else set()))
    if doc['schema'] not in ('qualification_campaign_budget_profile/v1', 'qualification_campaign_budget_profile/v2'):
        raise ValueError('campaign budget profile schema required')
    digest(doc['installed_profile_sha256'])
    integer(doc['record_byte_limit'], positive=True)
    fields(doc['phases'], PHASES)
    for value in doc['phases'].values():
        limits(value)
    if revised:
        fields(doc['orchestration_cpu_ns'], PHASES)
        for phase, charge in doc['orchestration_cpu_ns'].items():
            integer(charge, positive=True)
            if charge > doc['phases'][phase]['cpu_ns']:
                raise ValueError('orchestration bound exceeds phase reservation')
    return doc


# Installed operational ceilings, never statistical thresholds. Shared variants
# are defined once; the resolved bytes are signed in the release, not this name.
_DIAGNOSTIC_PHASE = MappingProxyType(dict(cpu_ns=120_000_000_000,
                                         wall_ns=300_000_000_000))
_DIAGNOSTIC_CONTROLLER_CPU_NS = 20_000_000_000


def diagnostic_budget_profile(profile_bytes):
    from .campaign_budget import PHASES
    from ..contract import canonical_json_bytes as encoded
    profile = parse_profile(profile_bytes)
    if profile.values['schema'] != 'qualification_execution_profile/v3':
        raise ValueError('fresh diagnostic execution profile required')
    result = dict(schema='qualification_campaign_budget_profile/v2',
        installed_profile_sha256=profile.sha256, record_byte_limit=131072,
        phases={phase: dict(_DIAGNOSTIC_PHASE, memory_bytes=profile.memory_bytes) for phase in PHASES},
        orchestration_cpu_ns={phase: _DIAGNOSTIC_CONTROLLER_CPU_NS for phase in PHASES})
    parse_campaign_budget_profile(encoded(result))
    return result


def diagnostic_execution_profile(base_bytes):
    """Compose the diagnostic variant once from validated deployment limits."""
    from ..contract import canonical_json_bytes as encoded
    base = parse_profile(base_bytes)
    result = dict(_DIAGNOSTIC_FIXED, **{name: base.values[name] for name in _LIMITS})
    raw = encoded(result)
    parse_profile(raw)
    return parse_canonical_json(raw, label='resolved diagnostic profile')
