"""T00 source-only contract (design rev 4.2, spec §2.2–§2.6b, §5 A1–A15, A18).

Signing keys and compiled source constants are replaced only inside this test
process (``SOURCE_SIGNING_KEYS`` / ``SOURCE_TRUST_CONSTANTS``); no guard function
is patched. Every negative asserts its own refusal code against a twin that passes.
"""
from __future__ import annotations

import base64
import hashlib
import json
import re
from dataclasses import dataclass, replace
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from types import MappingProxyType

import pytest

cryptography = pytest.importorskip("cryptography")
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from c1_rail.qualification import contract as contract_module
from c1_rail.qualification import trust_domain as trust_module
from c1_rail.qualification.contract import (
    ACCEPTED_HISTORICAL_PINS, ContractValidationError, ObservedBindings, canonical_json_bytes,
)
from c1_rail.qualification.model import LEG_IDS

UTC = timezone.utc
NOW = datetime(2026, 9, 15, 20, 0, tzinfo=UTC)
KEY_ID = 'source:test'
PORT_ROLES = dict(zip(LEG_IDS, ('aegis_runtime_port', 'striker_runtime_port', 'vanguard_runtime_port', 'orb_runtime_port')))
SOURCE_ROLES = ('source_startup_policy', 'source_calendar', 'source_calendar_review', 'population_index',
                'population_index_review', 'schedule_execution_evidence', 'schedule_execution_evidence_review',
                'cost_model')
REVIEW_SCOPES = {'source_calendar': 'SOURCE_CALENDAR', 'population_index': 'SOURCE_POPULATION_INDEX',
                 'schedule_execution_evidence': 'SCHEDULE_EXECUTION'}
REFUSALS = ["QUALIFICATION_STAGES", "BUDGET", "DECISION_RULES", "SCREEN", "MONTE_CARLO", "SEAL",
            "ADMISSION", "DEPLOYMENT"]


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def raw_public(private) -> bytes:
    return private.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)


def v2_review(role, artifact_sha256, *, binding_sha256=None, reviewer='test-reviewer'):
    doc = {'schema': 'qualification-source-review/v2', 'artifact_role': role, 'artifact_sha256': artifact_sha256,
           'scope': REVIEW_SCOPES[role], 'decision': 'ACCEPTED', 'reviewer': reviewer,
           'reviewed_at': '2026-09-15T19:30:00Z', 'notes': ['TEST_ONLY reviewer statement']}
    if binding_sha256 is not None:
        doc['source_binding_sha256'] = binding_sha256
    return canonical_json_bytes(doc)


# A Ruling-2 deadline-fact record for the synthetic calendar: every synthetic OPEN
# row carries the 16:45 ET regular deadline, so no venue-flat date is listed.
SYNTHETIC_CALENDAR_PRODUCER = {
    'schema': 't00-p7-calendar-deadline-facts/v1',
    'label': 'RULED_MODEL_DEADLINES_NOT_OBSERVED_VENUE_HISTORY',
    'deadline_rule': {'scope': 'TEST_ONLY all four legs', 'venue_flat_date_et': '12:59', 'regular_et': '16:45'},
    'venue_flat_dates_in_interval': [],
}


def source_payloads(root: Path, *, transform=None, calendar_producer=None):
    """Synthetic source-only role payloads derived from the composition fixture."""
    from composition_fixture import build_artifacts, encoded
    fixture = build_artifacts(root / 'composition')
    base = fixture.payloads
    payloads = {role: base[role] for role in ACCEPTED_HISTORICAL_PINS}
    for leg in LEG_IDS:
        payloads['panel_' + leg] = base[leg + '_panel']
    payloads['effective_settings_successor'] = base['effective_settings_successor']
    payloads['calendar_producer'] = (canonical_json_bytes(SYNTHETIC_CALENDAR_PRODUCER)
                                     if calendar_producer is None else calendar_producer)
    fact = {'role': 'calendar_producer', 'sha256': sha(payloads['calendar_producer'])}
    calendar = json.loads(base['source_calendar'])
    for row in calendar['sessions']:
        row['facts'] = [fact]
        for item in row['venue_deadlines'].values():
            item['fact'] = fact
    if transform is not None:
        transform('source_calendar', calendar)
    payloads['source_calendar'] = encoded(calendar)
    index = json.loads(base['population_index'])
    index['source_binding']['source_calendar_sha256'] = sha(payloads['source_calendar'])
    if transform is not None:
        transform('population_index', index)
    payloads['population_index'] = encoded(index)
    payloads['source_startup_policy'] = base['source_startup_policy']
    payloads['schedule_execution_evidence'] = base['schedule_execution_evidence']
    payloads['cost_model'] = base['cost_model']
    binding_sha = sha(encoded(index['source_binding']))
    for role in REVIEW_SCOPES:
        payloads[role + '_review'] = v2_review(role, sha(payloads[role]),
                                               binding_sha256=binding_sha if role == 'population_index' else None)
    return payloads, fixture


@dataclass
class SourceCase:
    root: Path
    payloads: dict
    paths: dict
    document: dict
    private: object
    public_keys: dict
    fixture: object

    def contract_bytes(self):
        return canonical_json_bytes(self.document)

    def approval(self, *, scope='APPROVE_T00_SOURCE_CONTRACT', key_id=KEY_ID, private=None, authority='OPERATOR',
                 issued_at='2026-09-15T19:00:00Z', expires_at='2026-09-16T19:00:00Z', subject=None):
        raw = self.contract_bytes() if subject is None else subject
        digest = sha(raw)
        payload = {'schema': 'qualification_approval_payload/v1', 'scope': scope, 'subject_sha256': digest,
                   'contract_sha256': digest, 'issued_at': issued_at, 'expires_at': expires_at,
                   'authority_class': authority}
        key = self.private if private is None else private
        return canonical_json_bytes({'schema': 'qualification_approval/v1', 'payload': payload,
            'signature': {'algorithm': 'Ed25519', 'key_id': key_id,
                          'value_b64': base64.b64encode(key.sign(canonical_json_bytes(payload))).decode()}})

    def observed(self, overrides=None):
        artifacts = {row['path']: row['sha256'] for row in self.document['artifacts']}
        artifacts.update(overrides or {})
        return ObservedBindings(artifact_sha256=artifacts,
            runtime_load_sha256={row['role']: row['sha256'] for row in self.document['artifacts']},
            effective_settings_sha256=self.document['effective_settings']['settings_sha256'], orb_normal_base=1)

    def validate(self, *, approval=None, public_keys=None, observed=None, now=NOW, contract_bytes=None):
        return contract_module.validate_source_contract(
            self.contract_bytes() if contract_bytes is None else contract_bytes,
            self.approval() if approval is None else approval,
            self.public_keys if public_keys is None else public_keys,
            self.observed() if observed is None else observed, now=now)


def pin_source_constants(monkeypatch, payloads, fixture, key_fingerprints):
    """In-process only: enroll the test key and the synthetic fixture's pins."""
    pins = {leg: trust_module.PortRuntimePin(leg, sha(payloads[PORT_ROLES[leg]]), fixture.pine_sha256[leg])
            for leg in LEG_IDS}
    constants = trust_module.SourceTrustConstants(
        accepted_historical_pins=MappingProxyType({role: sha(payloads[role]) for role in ACCEPTED_HISTORICAL_PINS}),
        port_runtime_pins=MappingProxyType(pins),
        effective_settings_sha256=sha(payloads['effective_settings_successor']))
    monkeypatch.setattr(trust_module, 'SOURCE_TRUST_CONSTANTS', constants)
    monkeypatch.setattr(contract_module, 'SOURCE_SIGNING_KEYS', MappingProxyType(
        {key_id: contract_module.SourceKeyPin(fp, revoked) for key_id, (fp, revoked) in key_fingerprints.items()}))


def build_source_case(root: Path, monkeypatch, *, transform=None, producer='test-producer',
                      calendar_producer=None, review_producer='test-reviewer') -> SourceCase:
    payloads, fixture = source_payloads(root, transform=transform, calendar_producer=calendar_producer)
    paths = {role: f'retained/{role}.bin' for role in payloads}
    for role, raw in payloads.items():
        path = root / paths[role]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    private = Ed25519PrivateKey.generate()
    public = raw_public(private)
    pin_source_constants(monkeypatch, payloads, fixture, {KEY_ID: (sha(public), None)})
    populations = json.loads(payloads['population_index'])['populations']
    document = {
        'schema': 't00_source_contract/v1', 'contract_id': 'TEST_ONLY-source-contract',
        'purpose': 'T00_P7_SOURCE_VERIFICATION',
        'artifacts': [{'role': role, 'path': paths[role], 'sha256': sha(payloads[role]),
                       'producer': review_producer if role.endswith('_review') else producer,
                       'authority_class': 'PRODUCTION_REVIEWED'} for role in sorted(payloads)],
        'historical_pins': {role: sha(payloads[role]) for role in ACCEPTED_HISTORICAL_PINS},
        'port_runtime_pins': {leg: {'runtime_sha256': sha(payloads[PORT_ROLES[leg]]),
                                    'pine_sha256': fixture.pine_sha256[leg]} for leg in LEG_IDS},
        'effective_settings': {'settings_sha256': sha(payloads['effective_settings_successor']), 'orb_normal_base': 1},
        'populations': populations,
        'initial_state': {'class': 'PRISTINE', 'original_basis': '100000', 'current_equity': '100000',
                          'historical_eod_peak': '100000', 'prior_trade_days': 0, 'prior_max_day_profit': '0'},
        'path_start_date': json.loads(payloads['source_startup_policy'])['path_start_date'],
        'source_trust': {KEY_ID: {'sha256': sha(public), 'revoked_at': None}},
        'refusals': list(REFUSALS),
    }
    return SourceCase(root, payloads, paths, document, private, {KEY_ID: public}, fixture)


@pytest.fixture
def case(tmp_path, monkeypatch):
    from c1_rail.qualification import production_source
    monkeypatch.setattr(production_source, '_now', lambda: NOW)
    return build_source_case(tmp_path, monkeypatch)


def refused(code, call):
    with pytest.raises((ContractValidationError, ValueError)) as error:
        call()
    assert code in str(error.value), str(error.value)


# ---- shipped constants --------------------------------------------------------

OPERATOR_SOURCE_KEY_SHA256 = '1ebae5d45bc512801e5217006ad84e188e5862d82b18f3be8a5094ea6332a4cb'
OPERATOR_SOURCE_PUBLIC_KEY_HEX = 'edf84922db9d92db7036969aef9178448da2ca7f7e884bf3d663420a0cc72e43'


def test_shipped_source_signing_pin_is_the_enrolled_operator_key_and_constants_are_compiled():
    from c1_signal_daemon.book_adapters import ADAPTERS, RUNTIME_EFFECTIVE_INPUTS_SHA256
    # Exactly one operator-enrolled key (2026-10-01); its ID derives from its pinned digest.
    assert dict(contract_module.SOURCE_SIGNING_KEYS) == {
        'source:' + OPERATOR_SOURCE_KEY_SHA256[:16]: contract_module.SourceKeyPin(OPERATOR_SOURCE_KEY_SHA256, None)}
    for key_id, pin in contract_module.SOURCE_SIGNING_KEYS.items():
        assert key_id == contract_module.SOURCE_KEY_PREFIX + pin.sha256[:16]
        assert re.fullmatch(r'[0-9a-f]{64}', pin.sha256) and pin.revoked_at is None
    constants = trust_module.SOURCE_TRUST_CONSTANTS
    assert dict(constants.accepted_historical_pins) == dict(ACCEPTED_HISTORICAL_PINS)
    assert {leg: pin.runtime_sha256 for leg, pin in constants.port_runtime_pins.items()} == \
        {spec.leg_id: spec.runtime_sha256 for spec in ADAPTERS}
    assert constants.effective_settings_sha256 == RUNTIME_EFFECTIVE_INPUTS_SHA256


def test_enrolled_operator_pin_is_a_strong_ed25519_public_key():
    raw = bytes.fromhex(OPERATOR_SOURCE_PUBLIC_KEY_HEX)
    assert len(raw) == 32 and sha(raw) == OPERATOR_SOURCE_KEY_SHA256
    assert contract_module.is_strong_public_key(raw)


def test_empty_pin_refuses_every_source_contract(case, monkeypatch):
    case.validate()
    monkeypatch.setattr(contract_module, 'SOURCE_SIGNING_KEYS', MappingProxyType({}))
    refused('SOURCE_TRUST_ROOT_UNENROLLED', case.validate)


# ---- A1–A4 ---------------------------------------------------------------------

def test_source_contract_canonical_roundtrip_and_closed_fields(case):  # A1
    receipt = case.validate()
    assert type(receipt) is contract_module.ValidatedSourceContract
    assert receipt.contract_sha256 == sha(case.contract_bytes())
    assert receipt.evidence_class == 'T00_P7_SOURCE_ONLY'
    pretty = json.dumps(case.document, indent=1, sort_keys=True).encode()
    refused('canonical', lambda: case.validate(contract_bytes=pretty,
                                                approval=case.approval(subject=pretty)))
    extra = dict(case.document, unexpected=1)
    raw = canonical_json_bytes(extra)
    refused('SOURCE_CONTRACT_FIELDS', lambda: case.validate(contract_bytes=raw, approval=case.approval(subject=raw)))


@pytest.mark.parametrize('field', ['replay', 'result_plan', 'approval_policy', 'coverage', 'clocks',
                                   'trust_domain_sha256', 'policy_sha256'])
def test_source_contract_refuses_every_f1_field(case, field):  # A2
    case.validate()
    raw = canonical_json_bytes(dict(case.document, **{field: {}}))
    refused('SOURCE_CONTRACT_FIELDS', lambda: case.validate(contract_bytes=raw, approval=case.approval(subject=raw)))


@pytest.mark.parametrize('change', ['remove', 'add', 'rename'])
def test_source_contract_role_set_is_exact(case, change):  # A3
    case.validate()
    rows = [dict(row) for row in case.document['artifacts']]
    if change == 'remove':
        rows = [row for row in rows if row['role'] != 'cost_model']
    elif change == 'add':
        rows.append(dict(rows[0], role='extra_role', path='retained/extra.bin'))
    else:
        rows[0]['role'] = 'renamed_role'
    case.document['artifacts'] = rows
    raw = case.contract_bytes()
    observed = ObservedBindings({row['path']: row['sha256'] for row in rows},
                                {row['role']: row['sha256'] for row in rows},
                                case.document['effective_settings']['settings_sha256'], 1)
    refused('SOURCE_ROLE_SET', lambda: case.validate(contract_bytes=raw, approval=case.approval(subject=raw),
                                                     observed=observed))


def test_observed_digest_mismatch_refused_at_digest_check(case):  # A3b / row 3
    case.validate()
    path = case.paths['cost_model']
    refused('SOURCE_OBSERVED_DIGEST', lambda: case.validate(observed=case.observed({path: '0' * 64})))


@pytest.mark.parametrize('mutation', ['historical', 'port', 'settings', 'striker_original', 'historical_settings'])
def test_source_contract_pins_are_compiled_constants(case, mutation):  # A4
    case.validate()
    doc = case.document
    if mutation == 'historical':
        doc['historical_pins']['step6_accepted_run'] = '1' * 64
    elif mutation == 'port':
        doc['port_runtime_pins']['orb_mnq_v7']['runtime_sha256'] = '2' * 64
    elif mutation == 'settings':
        doc['effective_settings']['settings_sha256'] = '3' * 64
    elif mutation == 'striker_original':
        doc['port_runtime_pins']['dj30_mym_p250']['runtime_sha256'] = (
            'c81aa59c811dd2f318bf2f6b51e9df32fca20315ffab0885ec1d4ec6a2ab5379')
    else:
        doc['effective_settings']['settings_sha256'] = contract_module.HISTORICAL_EFFECTIVE_INPUTS
    raw = case.contract_bytes()
    refused('SOURCE_PIN_MISMATCH', lambda: case.validate(contract_bytes=raw, approval=case.approval(subject=raw)))


# ---- A5, A6, A6b, A6c ------------------------------------------------------------

@pytest.mark.parametrize('scope', ['FREEZE_F1', 'BIND_QUALIFICATION_TRUST_DOMAIN'])
def test_source_approval_scope_is_exclusive(case, scope):  # A5
    case.validate()
    refused('approval scope does not match', lambda: case.validate(approval=case.approval(scope=scope)))


def test_source_signer_must_be_enrolled_source_key(case, monkeypatch):  # A6
    case.validate()
    other = Ed25519PrivateKey.generate()
    refused('TEST_ONLY', lambda: case.validate(approval=case.approval(authority='TEST_ONLY')))
    refused('SOURCE_KEY_ID', lambda: case.validate(approval=case.approval(key_id='operator')))
    refused('SOURCE_TRUST_ROOT_MISMATCH', lambda: case.validate(
        approval=case.approval(key_id='source:other', private=other),
        public_keys=dict(case.public_keys, **{'source:other': raw_public(other)})))
    refused('approval is not valid at verification time', lambda: case.validate(now=NOW + timedelta(days=2)))
    refused('signature is invalid', lambda: case.validate(approval=case.approval(private=other)))
    refused('SOURCE_TRUST_ROOT_MISMATCH', lambda: case.validate(public_keys={KEY_ID: raw_public(other)}))


def test_self_signed_source_contract_with_matching_self_registry_is_refused(case):  # A6b
    case.validate()
    forger = Ed25519PrivateKey.generate()
    public = raw_public(forger)
    case.document['source_trust'] = {'source:forger': {'sha256': sha(public), 'revoked_at': None}}
    raw = case.contract_bytes()
    approval = case.approval(key_id='source:forger', private=forger, subject=raw)
    refused('SOURCE_TRUST_ROOT_MISMATCH', lambda: case.validate(contract_bytes=raw, approval=approval,
                                                                public_keys={'source:forger': public}))


def test_revoked_or_removed_pin_key_refused(case, monkeypatch):  # A6c
    from c1_rail.qualification import production_source
    receipt = case.validate()
    revoked = MappingProxyType({KEY_ID: contract_module.SourceKeyPin(sha(case.public_keys[KEY_ID]),
                                                                    NOW - timedelta(minutes=1))})
    monkeypatch.setattr(contract_module, 'SOURCE_SIGNING_KEYS', revoked)
    case.document['source_trust'][KEY_ID]['revoked_at'] = '2026-09-15T19:59:00Z'
    raw = case.contract_bytes()
    refused('SOURCE_KEY_REVOKED', lambda: case.validate(contract_bytes=raw, approval=case.approval(subject=raw)))
    refused('SOURCE_KEY_REVOKED', lambda: contract_module.require_validated_source_contract(receipt, now=NOW))
    monkeypatch.setattr(contract_module, 'SOURCE_SIGNING_KEYS', MappingProxyType({}))
    refused('SOURCE_KEY_REMOVED', lambda: contract_module.require_validated_source_contract(receipt, now=NOW))


def test_replaced_pin_fingerprint_under_the_same_key_id_refuses_issued_receipt(case, monkeypatch):  # Codex P2 #594
    receipt = case.validate()
    assert receipt.source_key_sha256 == sha(case.public_keys[KEY_ID])
    contract_module.require_validated_source_contract(receipt, now=NOW)
    replaced = MappingProxyType({KEY_ID: contract_module.SourceKeyPin(sha(b'a different enrolled key'), None)})
    monkeypatch.setattr(contract_module, 'SOURCE_SIGNING_KEYS', replaced)
    refused('SOURCE_KEY_CHANGED', lambda: contract_module.require_validated_source_contract(receipt, now=NOW))


# ---- A7, A7b: qualification validators refuse source keys and approvals ----------

def test_qualification_validators_refuse_source_key_ids():  # A7
    from test_trust_domain import case as domain_case, validate
    from c1_rail.qualification.trust_domain import validate_qualification_trust_domain
    doc, policy, private, keys = domain_case()
    validate(doc, policy, private, keys)
    renamed = {'source:test': replace(keys['test'], key_id='source:test')}
    for field in ('freeze_key_ids', 'result_key_ids', 'seal_key_ids'):
        doc[field] = ['source:test']
    doc['trusted_key_sha256'] = {'source:test': doc['trusted_key_sha256']['test']}
    raw = canonical_json_bytes(doc)
    digest = sha(raw)
    payload = {'schema': 'qualification_approval_payload/v1', 'scope': 'BIND_QUALIFICATION_TRUST_DOMAIN',
               'subject_sha256': digest, 'contract_sha256': digest, 'authority_class': doc['authority_class'],
               'issued_at': '2026-09-15T19:00:00Z', 'expires_at': '2026-09-16T19:00:00Z'}
    approval = canonical_json_bytes({'schema': 'qualification_approval/v1', 'payload': payload,
        'signature': {'algorithm': 'Ed25519', 'key_id': 'source:test',
                      'value_b64': base64.b64encode(private.sign(canonical_json_bytes(payload))).decode()}})
    refused('SOURCE_KEY_IN_QUALIFICATION_DOMAIN', lambda: validate_qualification_trust_domain(
        raw, approval, renamed, policy=policy, now=NOW))
    # F1 contract validator: a source: freeze key ID is refused before enrollment comparison.
    import test_contract
    from c1_rail.qualification.contract import validate_frozen_contract
    document = test_contract._document()
    domain, fprivate, fkeys = test_contract._operator_domain(document)
    document['trust_domain_sha256'] = domain.sha256
    document['approval_policy']['freeze_key_ids'] = ['test']
    good = canonical_json_bytes(document)
    validate_frozen_contract(good, test_contract._approval(good, fprivate, key_id='test'), fkeys,
                             test_contract._observed(document), now=test_contract.NOW, trust_domain=domain)
    document['approval_policy']['freeze_key_ids'] = ['source:test']
    bad = canonical_json_bytes(document)
    refused('SOURCE_KEY_IN_QUALIFICATION_DOMAIN', lambda: validate_frozen_contract(
        bad, test_contract._approval(bad, fprivate, key_id='test'), fkeys, test_contract._observed(document),
        now=test_contract.NOW, trust_domain=domain))


def test_real_source_approval_refused_by_both_qualification_validators(case):  # A7b
    import test_contract
    from test_trust_domain import case as domain_case, signed, validate
    from c1_rail.qualification.contract import validate_frozen_contract
    from c1_rail.qualification.trust_domain import validate_qualification_trust_domain
    document = test_contract._document()
    domain, private, keys = test_contract._operator_domain(document)
    document['trust_domain_sha256'] = domain.sha256
    document['approval_policy']['freeze_key_ids'] = ['test']
    raw = canonical_json_bytes(document)
    observed = test_contract._observed(document)
    validate_frozen_contract(raw, test_contract._approval(raw, private, key_id='test'), keys, observed,
                             now=test_contract.NOW, trust_domain=domain)
    source_approval = test_contract._approval(raw, private, key_id='test', scope='APPROVE_T00_SOURCE_CONTRACT')
    refused('approval scope does not match', lambda: validate_frozen_contract(
        raw, source_approval, keys, observed, now=test_contract.NOW, trust_domain=domain))
    doc, policy, dprivate, dkeys = domain_case()
    validate(doc, policy, dprivate, dkeys)
    raw_domain, _ = signed(doc, dprivate)
    _, source_signed = signed(doc, dprivate, scope='APPROVE_T00_SOURCE_CONTRACT')
    refused('approval scope does not match', lambda: validate_qualification_trust_domain(
        raw_domain, source_signed, dkeys, policy=policy, now=NOW))


# ---- A8, A9 -------------------------------------------------------------------

def test_source_receipt_mutation_and_lookalike_refused(case):  # A8
    receipt = case.validate()
    contract_module.require_validated_source_contract(receipt, now=NOW)
    lookalike = replace(receipt)
    refused('validator-issued source contract required',
            lambda: contract_module.require_validated_source_contract(lookalike, now=NOW))
    object.__setattr__(receipt, 'contract_id', 'mutated')
    refused('source contract fields changed', lambda: contract_module.require_validated_source_contract(receipt, now=NOW))


def test_build_dispatches_on_exact_contract_type(case):  # A9
    from c1_rail.qualification.production_source import ProductionSource
    receipt = case.validate()
    source = ProductionSource.build(receipt, artifact_root=case.root)
    assert source.evidence_class == 'T00_P7_SOURCE_ONLY'

    class Sub(contract_module.ValidatedSourceContract):
        pass
    for wrong in (object(), Sub.__new__(Sub)):
        with pytest.raises((ValueError, TypeError)):
            ProductionSource.build(wrong, artifact_root=case.root)


# ---- A11, A12, A12b ----------------------------------------------------------

def _rewrite(case, role, raw):
    case.payloads[role] = raw
    for row in case.document['artifacts']:
        (case.root / row['path']).write_bytes(case.payloads[row['role']])
        row['sha256'] = sha(case.payloads[row['role']])


@pytest.mark.parametrize('negative,code', [
    ('missing_role', 'SOURCE_ROLE_SET'),
    ('review_digest', 'review companion'),
    ('unknown_date', 'UNKNOWN_SOURCE_DATE'),
    ('population', 'population'),
    ('capital', 'startup paper capital differs'),
])
def test_source_only_build_runs_the_same_source_checks(tmp_path, monkeypatch, negative, code):  # A11
    """Existing source-pack negatives fail on the source-only path; a missing role is caught
    earlier, at validation, because the source-only role set is closed (spec §2.4)."""
    from c1_rail.qualification import production_source
    from c1_rail.qualification.production_source import ProductionSource, ProductionSourceNeedsContext
    monkeypatch.setattr(production_source, '_now', lambda: NOW)
    twin = build_source_case(tmp_path / 'twin', monkeypatch)
    ProductionSource.build(twin.validate(), artifact_root=twin.root)

    def transform(role, doc):
        if negative == 'unknown_date' and role == 'source_calendar':
            doc['sessions'][3] = {'date': doc['sessions'][3]['date'], 'status': 'unknown', 'reason': 'unknown',
                                  'facts': doc['sessions'][3]['facts'], 'venue_deadlines': {}}
        if negative == 'population' and role == 'population_index':
            doc['populations']['FULL'] = doc['populations']['FULL'][1:]
    bad = build_source_case(tmp_path / 'bad', monkeypatch, transform=transform)
    if negative == 'missing_role':
        bad.document['artifacts'] = [row for row in bad.document['artifacts'] if row['role'] != 'source_calendar_review']
    if negative == 'review_digest':
        _rewrite(bad, 'schedule_execution_evidence_review', v2_review('schedule_execution_evidence', '0' * 64))
    if negative == 'capital':
        startup = json.loads(bad.payloads['source_startup_policy'])
        startup['legs']['aegis_6j']['paper_initial_capital'] = '99999'
        _rewrite(bad, 'source_startup_policy', canonical_json_bytes(startup))
    if negative == 'population':
        full = bad.document['populations']['FULL']
        bad.document['populations'] = {'FULL': full, 'H1': full[:(len(full) + 1) // 2],
                                       'H2': full[(len(full) + 1) // 2:]}
    observed = ObservedBindings({row['path']: row['sha256'] for row in bad.document['artifacts']},
                                {row['role']: row['sha256'] for row in bad.document['artifacts']},
                                bad.document['effective_settings']['settings_sha256'], 1)
    with pytest.raises((ValueError, ProductionSourceNeedsContext)) as error:
        raw = bad.contract_bytes()
        receipt = bad.validate(contract_bytes=raw, approval=bad.approval(subject=raw), observed=observed)
        ProductionSource.build(receipt, artifact_root=bad.root)
    text = str(error.value) + ' '.join(getattr(g, 'code', '') for g in getattr(error.value, 'gaps', ()))
    assert code in text, text


def _held_orb(monkeypatch):
    import composition_fixture as fixture_module
    original = fixture_module.build_artifacts

    def holding(root, *, idle=False, port_transform=None):
        def hold(leg, raw):
            if leg != 'orb_mnq_v7':
                return raw
            return raw.replace(b'local.minute == 15 and self.position', b'local.minute == 59 and self.position')
        return original(root, idle=idle, port_transform=hold)
    monkeypatch.setattr(fixture_module, 'build_artifacts', holding)


def test_source_only_replay_and_proof_never_leak_a_raw_deadline_result(tmp_path, monkeypatch):  # Codex P2 on #594
    from c1_rail.qualification import production_source
    from c1_rail.qualification.paths import PathAssembler
    from c1_rail.qualification.replay import ReplayDeadlineFailure
    monkeypatch.setattr(production_source, '_now', lambda: NOW)
    case = build_source_case(tmp_path, monkeypatch)
    source = production_source.ProductionSource.build(case.validate(), artifact_root=case.root)
    panel = source.sessions[:2]
    path = PathAssembler(source.path_start_date).assemble((panel,), horizon_sessions=2)
    raw = source._replay_raw(path)

    def violated(self, path):
        raise ReplayDeadlineFailure(raw)
    monkeypatch.setattr(production_source.ProductionSource, '_replay_raw', violated)
    sealed = source.replay(path)
    assert type(sealed) is production_source.SourceOnlyReplay and sealed.deadline_failure is True
    assert [row.source_session_id for row in sealed.sessions] == [row.source_session_id for row in raw.sessions]
    with pytest.raises(ValueError, match='SOURCE_ONLY_PROOF_DEADLINE_FAILURE') as refusal:
        source.proof(panel)
    assert refusal.value.__context__ is None and refusal.value.__cause__ is None
    assert not hasattr(refusal.value, 'result')


def test_source_only_replay_bracket_fresh_engines_and_label(tmp_path, monkeypatch):  # A12
    """End to end with every guard intact; only keys/constants are pinned in-process."""
    from c1_signal_daemon import book_adapters
    from c1_rail.book_policy import candidate_book_protection_policy
    from c1_rail.qualification import production_source
    from c1_rail.qualification import replay as replay_module
    from c1_rail.qualification.model import ReplayResult
    from c1_rail.qualification.paths import PathAssembler
    monkeypatch.setattr(production_source, '_now', lambda: NOW)
    _held_orb(monkeypatch)
    case = build_source_case(tmp_path, monkeypatch)
    receipt = case.validate()
    source = production_source.ProductionSource.build(receipt, artifact_root=case.root)
    assert source.evidence_class == 'T00_P7_SOURCE_ONLY'
    path = PathAssembler(source.path_start_date).assemble((source.sessions[:3],), horizon_sessions=3)
    loads, engines = [], []
    load = book_adapters._load_domain_adapters

    def counting(contract, *, retained_bytes, domain):
        loads.append(load(contract, retained_bytes=retained_bytes, domain=domain))
        return loads[-1]

    class Recorded(replay_module.BookReplay):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            engines.append(self)
    monkeypatch.setattr(book_adapters, '_load_domain_adapters', counting)
    monkeypatch.setattr(replay_module, 'BookReplay', Recorded)
    result = source.replay_bracket(path)
    assert type(result) is production_source.SourceOnlyBracket
    assert type(result.r1) is production_source.SourceOnlyReplay and type(result.r2) is production_source.SourceOnlyReplay
    assert not isinstance(result.r1, ReplayResult) and not isinstance(result, ReplayResult)
    assert len(loads) == len(engines) == 2 and engines[0].ledger is not engines[1].ledger
    assert [e.schedule_quotes.run for e in engines] == ['R1', 'R2']
    assert all(e.policy == candidate_book_protection_policy() for e in engines)
    for run in (result.r1, result.r2):
        assert run.evidence_class == 'T00_P7_SOURCE_ONLY'
        assert run.contract_sha256 == receipt.contract_sha256 and run.approval_sha256 == receipt.approval.approval_sha256
        assert len(run.sessions) == 3 and all(row.intraday_low <= 0 for row in run.sessions)
        assert run.consumed_intrabar_splits and all(leg == 'orb_mnq_v7' for _, leg, _ in run.consumed_intrabar_splits)
    refused('SOURCE_ONLY_NOT_QUALIFICATION', lambda: source.verify_for(source.contract))


def test_receipt_expires_between_build_and_replay(case, monkeypatch):  # A12b
    from c1_rail.qualification import production_source
    from c1_rail.qualification.paths import PathAssembler
    source = production_source.ProductionSource.build(case.validate(), artifact_root=case.root)
    path = PathAssembler(source.path_start_date).assemble((source.sessions[:2],), horizon_sessions=2)
    source.replay_bracket(path)
    monkeypatch.setattr(production_source, '_now', lambda: NOW + timedelta(days=2))
    refused('SOURCE_APPROVAL_EXPIRED', lambda: source.replay_bracket(path))


# ---- A13, A14, A15, A18 ------------------------------------------------------

def _calendar_rows(case):
    return json.loads(case.payloads['source_calendar'])


def test_source_truncated_disposition_only_at_interval_ends(case):  # A13
    from c1_rail.qualification.clock import SourceDayStatus
    from c1_rail.qualification.production_source import (
        parse_population_index, parse_source_calendar, validate_source_only_calendar)
    receipt = case.validate()
    doc = _calendar_rows(case)
    fact = doc['sessions'][0]['facts'][0]
    last = doc['sessions'][-1]
    reason = 'panel truncated at interval end: slots 18:00-20:00 ET'
    doc['sessions'][-1] = {'date': last['date'], 'status': 'source_truncated', 'reason': reason,
                           'facts': [fact], 'venue_deadlines': {}}
    raw = canonical_json_bytes(doc)
    validate_source_only_calendar(raw, contract=receipt, truncated_slots={last['date']: '18:00-20:00'})
    clock, _ = parse_source_calendar(raw, artifact_digests={'calendar_producer': fact['sha256']})
    assert dict(clock.schedules)[date.fromisoformat(last['date'])].status is SourceDayStatus.SOURCE_TRUNCATED
    index = json.loads(case.payloads['population_index'])
    index['expected_exclusions'] = [{'source_date': last['date'], 'reason': 'source_truncated', 'detail': reason}]
    parse_population_index(canonical_json_bytes(index), populations=index['populations'])
    interior = json.loads(raw)
    interior['sessions'][5], interior['sessions'][-1] = dict(interior['sessions'][-1], date=interior['sessions'][5]['date']), last
    refused('SOURCE_TRUNCATION_INTERIOR', lambda: validate_source_only_calendar(
        canonical_json_bytes(interior), contract=receipt, truncated_slots={}))
    unnamed = json.loads(raw)
    unnamed['sessions'][-1]['reason'] = 'panel ended'
    refused('SOURCE_TRUNCATION_REASON', lambda: validate_source_only_calendar(
        canonical_json_bytes(unnamed), contract=receipt, truncated_slots={last['date']: '18:00-20:00'}))
    stand_in = json.loads(raw)
    stand_in['sessions'][-1] = dict(stand_in['sessions'][-1], status='policy_denied',
                                    reason='panel truncated at interval end: 9 slots')
    refused('TRUNCATION_STAND_IN_RETIRED', lambda: validate_source_only_calendar(
        canonical_json_bytes(stand_in), contract=receipt, truncated_slots={}))


@pytest.mark.parametrize('defect', ['template', 'v1', 'self_review', 'missing_reviewer'])
def test_review_companion_v2_reviewer_authored(tmp_path, monkeypatch, defect):  # A14
    from c1_rail.qualification import production_source
    from c1_rail.qualification.production_source import ProductionSource
    monkeypatch.setattr(production_source, '_now', lambda: NOW)
    twin = build_source_case(tmp_path / 'twin', monkeypatch)
    ProductionSource.build(twin.validate(), artifact_root=twin.root)
    bad = build_source_case(tmp_path / 'bad', monkeypatch,
                            producer='test-reviewer' if defect == 'self_review' else 'test-producer')
    role = 'source_calendar_review'
    doc = json.loads(bad.payloads[role])
    if defect == 'template':
        doc = {'schema': 'qualification-source-review/v1', 'artifact_role': 'source_calendar',
               'artifact_sha256': doc['artifact_sha256'], 'scope': 'SOURCE_CALENDAR', 'decision': 'ACCEPTED'}
    elif defect == 'v1':
        for key in ('reviewer', 'reviewed_at', 'notes'):
            doc.pop(key)
        doc['schema'] = 'qualification-source-review/v1'
    elif defect == 'missing_reviewer':
        doc.pop('reviewer')
    bad.payloads[role] = canonical_json_bytes(doc)
    for row in bad.document['artifacts']:
        (bad.root / row['path']).write_bytes(bad.payloads[row['role']])
        row['sha256'] = sha(bad.payloads[row['role']])
    code = 'REVIEW_NOT_INDEPENDENT' if defect == 'self_review' else 'review companion'
    refused(code, lambda: ProductionSource.build(bad.validate(), artifact_root=bad.root))


def test_qualification_path_refuses_source_truncated(tmp_path, monkeypatch):  # Codex P1 on #594
    from c1_rail.qualification import production_source
    from c1_rail.qualification.production_source import refuse_source_truncated_on_qualification
    from composition_fixture import build_artifacts, build_verified_composition
    base = build_artifacts(tmp_path / 'plain').payloads
    refuse_source_truncated_on_qualification(base['source_calendar'], base['population_index'])
    calendar, index = json.loads(base['source_calendar']), json.loads(base['population_index'])
    last = calendar['sessions'][-1]
    calendar['sessions'][-1] = dict(last, status='source_truncated', reason='panel truncated: slots 18:00-20:00 ET',
                                    venue_deadlines={})
    refused('SOURCE_TRUNCATED_QUALIFICATION_REFUSED', lambda: refuse_source_truncated_on_qualification(
        canonical_json_bytes(calendar), base['population_index']))
    index['expected_exclusions'] = [{'source_date': last['date'], 'reason': 'source_truncated', 'detail': 'x'}]
    refused('SOURCE_TRUNCATED_QUALIFICATION_REFUSED', lambda: refuse_source_truncated_on_qualification(
        base['source_calendar'], canonical_json_bytes(index)))
    # Wiring: the qualification (frozen-contract) build runs the guard; the source-only build does not.
    calls = []

    def guard(calendar_raw, index_raw):
        calls.append(len(calendar_raw))
        raise ValueError('SOURCE_TRUNCATED_QUALIFICATION_REFUSED: guard reached')
    monkeypatch.setattr(production_source, 'refuse_source_truncated_on_qualification', guard)
    refused('SOURCE_TRUNCATED_QUALIFICATION_REFUSED', lambda: build_verified_composition(tmp_path / 'qualification'))
    assert calls, 'the qualification build must run the source_truncated guard'
    calls.clear()
    monkeypatch.setattr(production_source, '_now', lambda: NOW)
    case = build_source_case(tmp_path / 'source', monkeypatch)
    production_source.ProductionSource.build(case.validate(), artifact_root=case.root)
    assert not calls, 'the source-only build keeps its own truncation rules'


def test_producer_cannot_self_certify_a_review_under_another_name(tmp_path, monkeypatch):  # Codex P1 on #594
    """The companion claims reviewer "test-reviewer", but the signed contract says the
    reviewed artifact's own producer produced the companion: self-certification."""
    from c1_rail.qualification import production_source
    from c1_rail.qualification.production_source import ProductionSource
    monkeypatch.setattr(production_source, '_now', lambda: NOW)
    bad = build_source_case(tmp_path / 'bad', monkeypatch, review_producer='test-producer')
    assert json.loads(bad.payloads['source_calendar_review'])['reviewer'] == 'test-reviewer'
    refused('REVIEW_NOT_INDEPENDENT', lambda: ProductionSource.build(bad.validate(), artifact_root=bad.root))


@pytest.mark.parametrize('value', ['2030-01-08', '2030-01-05'])
def test_path_start_date_signed_and_consistent(case, value):  # A15
    from c1_rail.qualification.production_source import ProductionSource
    ProductionSource.build(case.validate(), artifact_root=case.root)
    case.document['path_start_date'] = value
    raw = case.contract_bytes()
    code = 'weekday' if date.fromisoformat(value).weekday() >= 5 else 'path_start_date'

    def attempt():
        receipt = case.validate(contract_bytes=raw, approval=case.approval(subject=raw))
        ProductionSource.build(receipt, artifact_root=case.root)
    refused(code, attempt)


def test_calendar_fact_must_bind_calendar_producer(case):  # A18
    from c1_rail.qualification.production_source import parse_source_calendar, validate_source_only_calendar
    receipt = case.validate()
    doc = _calendar_rows(case)
    validate_source_only_calendar(canonical_json_bytes(doc), contract=receipt, truncated_slots={})
    other = {'role': 'cost_model', 'sha256': sha(case.payloads['cost_model'])}
    doc['sessions'][0]['facts'] = [other]
    raw = canonical_json_bytes(doc)
    digests = {row['role']: row['sha256'] for row in case.document['artifacts']}
    parse_source_calendar(raw, artifact_digests=digests)  # the generic _fact alone accepts it
    refused('CALENDAR_FACT_ROLE', lambda: validate_source_only_calendar(raw, contract=receipt, truncated_slots={}))


@pytest.mark.parametrize('defect,producer_bytes', [
    ('empty', b''),
    ('malformed', b'{"schema": "t00-p7-calendar-deadline-facts/v1", '),
    ('wrong_label', canonical_json_bytes(dict(SYNTHETIC_CALENDAR_PRODUCER, label='OBSERVED_VENUE_HISTORY'))),
    ('wrong_schema', canonical_json_bytes(dict(SYNTHETIC_CALENDAR_PRODUCER, schema='t00-p7-calendar-deadline-facts/v0'))),
    ('wrong_rule', canonical_json_bytes(dict(SYNTHETIC_CALENDAR_PRODUCER, deadline_rule={
        'venue_flat_date_et': '13:00', 'regular_et': '16:45'}))),
    ('hours_text', b'Explicit synthetic calendar facts, never market evidence.'),
])
def test_build_refuses_a_calendar_producer_that_is_not_the_deadline_fact_record(
        tmp_path, monkeypatch, defect, producer_bytes):  # Codex P2 on #594
    from c1_rail.qualification import production_source
    from c1_rail.qualification.production_source import ProductionSource
    monkeypatch.setattr(production_source, '_now', lambda: NOW)
    twin = build_source_case(tmp_path / 'twin', monkeypatch)
    ProductionSource.build(twin.validate(), artifact_root=twin.root)
    bad = build_source_case(tmp_path / 'bad', monkeypatch, calendar_producer=producer_bytes)
    refused('CALENDAR_PRODUCER_INVALID', lambda: ProductionSource.build(bad.validate(), artifact_root=bad.root))


def test_build_refuses_calendar_deadlines_the_producer_record_does_not_state(tmp_path, monkeypatch):  # Codex P2 #594
    from c1_rail.qualification import production_source
    from c1_rail.qualification.production_source import ProductionSource
    monkeypatch.setattr(production_source, '_now', lambda: NOW)
    first_open = json.loads(source_payloads(tmp_path / 'probe')[0]['source_calendar'])['sessions'][0]['date']
    lying = canonical_json_bytes(dict(SYNTHETIC_CALENDAR_PRODUCER, venue_flat_dates_in_interval=[first_open]))
    bad = build_source_case(tmp_path / 'bad', monkeypatch, calendar_producer=lying)
    refused('CALENDAR_PRODUCER_MISMATCH', lambda: ProductionSource.build(bad.validate(), artifact_root=bad.root))
