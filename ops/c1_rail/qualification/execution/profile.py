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


def parse_profile(raw: bytes) -> ExecutionProfile:
    doc = parse_canonical_json(raw, label='execution profile')
    if type(doc) is not dict:
        raise ValueError('closed schema object required')
    fixed = _FIXED
    if doc.get('schema') == 'qualification_execution_profile/v2':
        fixed = dict(_FIXED, schema='qualification_execution_profile/v2', protocol_version=2,
            supported_checkpoints=[], capability='FULL_E1', dispatch_enabled=False)
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
    doc = fields(parse_canonical_json(raw, label='campaign budget profile'),
                 {'schema', 'installed_profile_sha256', 'phases', 'record_byte_limit'})
    if doc['schema'] != 'qualification_campaign_budget_profile/v1':
        raise ValueError('campaign budget profile schema required')
    digest(doc['installed_profile_sha256'])
    integer(doc['record_byte_limit'], positive=True)
    fields(doc['phases'], PHASES)
    for value in doc['phases'].values():
        limits(value)
    return doc
