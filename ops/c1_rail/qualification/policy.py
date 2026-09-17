"""Pure semantic policy. Parsed values establish consistency, never authority.

The installed-release consumer must separately compare exact approved policy
bytes. No code-owner imports, signing, source execution or persistence live here.
"""
from dataclasses import dataclass
from decimal import Decimal
import hashlib

from .contract import (
    canonical_json_bytes, parse_canonical_json, _decimal, _fields,
    _positive_int, _sha256, _text,
)


def _policy_document(*, tier, basis, owners):
    """Single owner of the closed policy schema and fixed semantic inventory."""
    return {
        'schema': 'qualification_policy/v1',
        'policy_id': 'tradeify-e1-pristine/v1',
        'product': {'tier': tier, 'original_basis': basis, 'state_class': 'PRISTINE'},
        'pre_admission_registry': 'EMPTY',
        'stage_order': ['LEGALITY', 'N1', 'N2', 'PART_B', 'PART_A'],
        'stage_populations': {'LEGALITY': [], 'N1': ['FULL', 'H1', 'H2'],
                              'N2': ['FULL'], 'PART_B': ['H1', 'H2'], 'PART_A': ['REGIME']},
        'checkpoint_groups': {'N1': ['N1'], 'CUTOFF': [], 'N2': ['N2', 'PART_B'], 'PART_A': ['PART_A']},
        'stage_artifact_roles': {'LEGALITY': 'legality_result', 'N1': 'n1_result',
                                 'N2': 'n2_result', 'PART_B': 'part_b_result', 'PART_A': 'part_a_result'},
        'base_artifact_roles': ['attempt_journal', 'path_inventory', 'runtime_load_trace'],
        'optional_artifact_roles': ['diagnostics_private'],
        'source_owner_sha256': owners,
    }


@dataclass(frozen=True)
class QualificationPolicy:
    canonical_bytes: bytes
    sha256: str
    tier: str
    original_basis: Decimal


def parse_policy(raw: bytes) -> QualificationPolicy:
    if type(raw) is not bytes:
        raise ValueError('POLICY_BYTES_REQUIRED')
    doc = parse_canonical_json(raw, label='qualification policy')
    if type(doc) is not dict or 'product' not in doc or 'source_owner_sha256' not in doc:
        raise ValueError('POLICY_SCHEMA_MISMATCH')
    product = _fields(doc['product'], {'tier', 'original_basis', 'state_class'}, label='product')
    tier = _text(product['tier'], label='product tier')
    basis = _decimal(product['original_basis'], label='product basis')
    if basis <= 0 or format(basis, 'f') != product['original_basis']:
        raise ValueError('INVALID_CANONICAL_PRODUCT_BASIS')
    owners = _fields(doc['source_owner_sha256'], {'book_policy', 'firm_rules', 'policy_fingerprint'}, label='policy owners')
    for name, digest in owners.items():
        _sha256(digest, label=name)
    expected = _policy_document(tier=tier, basis=product['original_basis'], owners=dict(owners))
    if raw != canonical_json_bytes(expected):
        raise ValueError('POLICY_SCHEMA_MISMATCH')
    return QualificationPolicy(raw, hashlib.sha256(raw).hexdigest(), tier, basis)


def _document(policy):
    if type(policy) is not QualificationPolicy or parse_policy(policy.canonical_bytes) != policy:
        raise ValueError('POLICY_IDENTITY_MISMATCH')
    return parse_canonical_json(policy.canonical_bytes, label='qualification policy')


def validate_contract_semantics(document: dict, policy: QualificationPolicy, *, workload_policy) -> None:
    resolved = _document(policy)
    if document.get('policy_sha256') != policy.sha256:
        raise ValueError('POLICY_IDENTITY_MISMATCH')
    plan = _fields(document.get('result_plan'), {'policy_sha256', 'adjudicator_closure_sha256'}, label='result_plan')
    if plan['policy_sha256'] != policy.sha256:
        raise ValueError('POLICY_IDENTITY_MISMATCH')
    _sha256(plan['adjudicator_closure_sha256'], label='adjudicator closure')
    state = _fields(document.get('initial_state'), {
        'class', 'original_basis', 'current_equity', 'historical_eod_peak',
        'prior_trade_days', 'prior_max_day_profit'}, label='initial_state')
    basis = _decimal(state['original_basis'], label='original_basis')
    if basis != policy.original_basis:
        raise ValueError('PRODUCT_BASIS_MISMATCH')
    equity = _decimal(state['current_equity'], label='current_equity')
    peak = _decimal(state['historical_eod_peak'], label='historical_eod_peak')
    days = _positive_int(state['prior_trade_days'], label='prior_trade_days', allow_zero=True)
    profit = _decimal(state['prior_max_day_profit'], label='prior_max_day_profit')
    if state['class'] != resolved['product']['state_class'] or equity != basis or peak != basis or days != 0 or profit != 0:
        raise ValueError('INITIAL_STATE_ALTERNATIVE_UNSUPPORTED')
    replay = document.get('replay')
    if type(replay) is not dict or type(replay.get('stages')) is not list:
        raise ValueError('STAGE_POLICY_MISMATCH')
    rows = replay['stages']
    order = resolved['stage_order'] + ['N3']
    if any(type(row) is not dict for row in rows) or [row.get('name') for row in rows] != order:
        raise ValueError('STAGE_POLICY_MISMATCH')
    stages = {}
    for row in rows:
        _fields(row, {'name', 'outcome_bearing', 'included_in_e1_seal', 'population_counts',
                      'exact_depth', 'max_failures_per_population', 'rng_namespace'}, label='stage')
        name = row['name']
        pops = resolved['stage_populations'].get(name, ['FULL', 'H1', 'H2'])
        counts = _fields(row['population_counts'], set(pops), label='stage populations')
        normalized = {}
        for pop, depths in counts.items():
            if type(depths) is not list or not depths:
                raise ValueError('STAGE_POLICY_MISMATCH')
            normalized[pop] = tuple(_positive_int(d, label='population depth') for d in depths)
        if normalized != dict(workload_policy.stage_population_depths[name]):
            raise ValueError('SIGNED_WORKLOAD_MISMATCH')
        depth = _positive_int(row['exact_depth'], label='exact_depth')
        namespace = 'n2' if name == 'PART_B' else name.lower()
        if (row['outcome_bearing'] is not True or row['included_in_e1_seal'] is not (name != 'N3')
                or row['rng_namespace'] != namespace):
            raise ValueError('STAGE_POLICY_MISMATCH')
        expected_depth = (1 if name == 'LEGALITY' else workload_policy.part_a_paths_per_population_per_panel
                          if name == 'PART_A' else next(iter(normalized.values()))[0])
        if depth != expected_depth:
            raise ValueError('SIGNED_WORKLOAD_MISMATCH')
        stages[name] = row
    for name in ('horizon_sessions', 'inner_block_sessions', 'outer_months'):
        if _positive_int(replay.get(name), label=name) != getattr(workload_policy, name):
            raise ValueError('SIGNED_WORKLOAD_MISMATCH')
    part_a = replay.get('part_a')
    if type(part_a) is not dict:
        raise ValueError('SIGNED_WORKLOAD_MISMATCH')
    for name in ('initial_panels', 'expanded_panels', 'paths_per_population_per_panel'):
        if _positive_int(part_a.get(name), label=name) != getattr(workload_policy, 'part_a_' + name):
            raise ValueError('SIGNED_WORKLOAD_MISMATCH')


def required_output_roles(policy: QualificationPolicy, *, stages: tuple[str, ...], completion: str, verdict: str) -> tuple[str, ...]:
    doc = _document(policy)
    order = tuple(doc['stage_order'])
    valid = ((stages == order[:2] and (completion, verdict) in {('COMPLETE', 'FAIL'), ('PARTIAL', 'NONE')})
             or (stages == order[:4] and (completion, verdict) == ('COMPLETE', 'FAIL'))
             or (stages == order and completion == 'COMPLETE' and verdict in {'PASS', 'FAIL'}))
    if not valid:
        raise ValueError('UNSUPPORTED_STAGE_ASSESSMENT')
    return tuple(sorted(doc['base_artifact_roles'] + [doc['stage_artifact_roles'][stage] for stage in stages]))
