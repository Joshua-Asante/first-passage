"""One source admission path checks legality before creating the real source."""
from dataclasses import dataclass
import hashlib

from c1_signal_daemon.book_adapters import _qualification_domain
from .contract import canonical_json_bytes
from .legality import SOURCE_CHECKS, geometry_role, verify_static_legality, build_legality_record
from .policy_sources import require_installed_policy
from .production_source import ProductionSource, _prepare_domain_inputs


@dataclass(frozen=True)
class AdmittedSource:
    source: ProductionSource
    source_admission_bytes: bytes
    legality_bytes: bytes


def admit_source(contract, *, artifact_root, policy) -> AdmittedSource:
    require_installed_policy(policy)
    domain = _qualification_domain(contract)
    role = geometry_role(domain.runtime_code_roles)
    prepared = _prepare_domain_inputs(contract, artifact_root=artifact_root, domain=domain)
    retained = dict(prepared.retained_bytes)
    trace = {name: (path, digest) for name, path, digest in prepared.load_trace}
    if role not in trace:
        raise ValueError('LEGALITY_GEOMETRY_ROLE_MISSING')
    path, digest = trace[role]
    arguments = dict(contract_sha256=contract.contract_sha256, domain_sha256=domain.sha256,
                     policy=policy, geometry_bytes=retained[path], expected_geometry_sha256=digest)
    verify_static_legality(**arguments)
    source = ProductionSource._build_from_prepared(contract, prepared, domain=domain)
    source.verify_for(contract)
    admission = canonical_json_bytes({
        'schema': 'qualification_source_admission/v1',
        'contract_sha256': contract.contract_sha256, 'trust_domain_sha256': domain.sha256,
        'policy_sha256': policy.sha256,
        'retained_roles': [{'role': name, 'sha256': digest} for name, _, digest in sorted(prepared.load_trace)],
        'population_sha256': {pop: hashlib.sha256(canonical_json_bytes(list(contract.populations[pop]))).hexdigest()
                              for pop in ('FULL', 'H1', 'H2')},
        'effective_settings_sha256': contract.effective_settings_sha256,
        'checks': list(SOURCE_CHECKS),
    })
    return AdmittedSource(source, admission, build_legality_record(**arguments, source_admission_bytes=admission))
