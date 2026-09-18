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
    doc = fields(parse_canonical_json(raw, label='execution profile'), (*_FIXED, *_LIMITS))
    for name, value in _FIXED.items():
        if type(doc[name]) is not type(value) or doc[name] != value:
            raise ValueError(f'unsupported execution profile {name}')
    for name in _LIMITS:
        positive(doc[name])
    if doc['worker_uid'] >= 2**32 - 1:
        raise ValueError('worker UID out of range')
    if any(doc[name] > 2**32 - 1 for name in ('output_byte_limit', 'rpc_byte_limit')):
        raise ValueError('transport byte limit out of range')
    return ExecutionProfile(raw, MappingProxyType({
        key: tuple(value) if type(value) is list else value for key, value in doc.items()}))
