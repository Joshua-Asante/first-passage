"""T00 screen authority: a separately signed second door around r3c (design 2026-10-02 §2-§3).

A ``t00_screen_authority/v1`` document signed under ``APPROVE_T00_SCREEN_AUTHORITY`` becomes a
``ValidatedScreenAuthority`` receipt. ``validate_screen_authority`` checks, in this order, so
that unsigned input never reaches ``git`` (design §3.2): the bytes alone (rows A1, A4, A11),
the signature (A2, A3), then ``_check_bindings`` with the authority, the receipt, the P7 record,
the reality it reads and every blob in hand (A5-A10); only then is the receipt issued.
``require_validated_screen_authority`` re-checks it on every use (K1-K4). Screen epochs and
their stat guard serve this module's ``screen_epoch``/``screen_bracket`` (§3.3; rows K6 and
K8 are tested by P-B2); ``validate_screen_act`` checks Joshua's signed acts (X2, X3). Build card
2026-10-03 §2.3, §3.1. ``contract.py`` is imported, never edited.

A second purpose, ``T00_SUCCESSOR_SCREEN`` (successor build card 2026-10-10 §2.5, S-3 to S-7),
screens one successor configuration: r3d, which is r3c with only ``contract_id`` and the
startup-policy row changed, over a signed v2 startup policy whose ``sizing`` vector is the only
startup change. ``PURPOSE_PROFILES`` holds each purpose's grant, evidence class, chain entry,
contract rule and expressions rule; the original purpose's row is the behaviour above, unchanged.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from datetime import date
import errno
import hashlib
import math
import os
from pathlib import Path
import re
import socket
import subprocess
import sys
from types import MappingProxyType
from typing import Any, Mapping
import weakref

from c1_rail.book_policy import validate_size_vector
from . import p7_evidence
from .contract import (
    SOURCE_EVIDENCE_CLASS, SOURCE_KEY_PREFIX, ApprovalRecord, ContractValidationError, TrustedApprovalKey, ValidatedSourceContract,
    _check_source_key_lifecycle, _fields, _pinned_source_keys, _receipt_snapshot, _source_trust_document,
    canonical_json_bytes, parse_canonical_json, require_validated_source_contract, verify_detached_approval,
)
from .model import BracketReplayResult
from .t00_screen import journal, verdict

# Exact JSON types are intended: bool is an int subclass, so isinstance() would admit it.
# pylint: disable=unidiomatic-typecheck

SCREEN_SCHEMA = 't00_screen_authority/v1'
SCREEN_SCOPE = 'APPROVE_T00_SCREEN_AUTHORITY'
SCREEN_ACT_SCHEMA = 't00_screen_act/v1'
SCREEN_ACT_SCOPE = 'APPROVE_T00_SCREEN_ACT'
SCREEN_PURPOSE = 'T00_STEP3_SELECTED_BOOK_SCREEN'
SCREEN_GRANTS = ('T00_STEP3_SCREEN_ONCE',)
SCREEN_REFUSALS = ('QUALIFICATION_STAGES', 'PART_A', 'F1', 'DECISION_RULES', 'SEAL', 'ADMISSION', 'DEPLOYMENT',
                   'ARM', 'FALSIFIER_EVIDENCE', 'PARAMETER_CHANGE')
SCREEN_EVIDENCE_CLASS = 'T00_STEP3_SCREEN'
# The successor purpose (successor card S-7; Q3): the same refusals, where PARAMETER_CHANGE means
# any change beyond the size vector frozen in the successor pre-registration.
SUCCESSOR_PURPOSE = 'T00_SUCCESSOR_SCREEN'
SUCCESSOR_GRANTS = ('T00_SUCCESSOR_SCREEN_ONCE',)
SUCCESSOR_EVIDENCE_CLASS = 'T00_SUCCESSOR_SCREEN'

# Compiled r3c digest (design §1); the authority binds the contract, never one approval (C2).
R3C_CONTRACT_SHA256 = 'a526b50fa75e68451bdd2b5b57fa7a04e6ee08e61f96865c915ae8116a848d97'
# r3c's contract_id and complete source_startup_policy artifact row (successor card S-3; public
# metadata read from r3c by the coordinator, 2026-10-10). The derivation check puts them back.
R3C_CONTRACT_ID: str | None = 't00-p7-source-contract-r3c'
R3C_STARTUP_POLICY_ROW: Mapping[str, str] | None = MappingProxyType({
    'authority_class': 'PRODUCTION_REVIEWED',
    'path': 'lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts/t00-p7-closure-2026-09-24/'
            'task3-source-pack-r3/source_startup_policy.json',
    'producer': 'executor:claude/t00-p7-tasks-3-4@67becc1708ed r3-producer:278201c451ae',
    'role': 'source_startup_policy',
    'sha256': '240caf5aaf276f5acb987e63edcd4a3d41e2c49f9c2d256ccc040f9be272eb8e',
})
# Compiled pre-registration chain (row A8; design §4.5): entry 0 is #581, bound by the original
# purpose; entry 1 is #733, bound by the successor purpose (successor card S-4).
PREREG_CHAIN = ('docs/briefs/pre-registration/2026-10-01-tradeify-t00-step2-screen-prereg.md',
                'docs/briefs/pre-registration/2026-10-08-tradeify-book-successor-screen-prereg-DRAFT.md')
# A3 successors (row A10): path -> (§3 row prefix, answerer-exposure regex, OWED pattern). The
# exposure form is the successors' own: "Answerer exposure: seen|not seen — <name>".
_EXPOSURE = re.compile(r'Answerer exposure: (?:seen|not seen) — [^\s<`|]')
_OWED = re.compile(r'\| \*\*OWED|\(OWED,|— OWED \(')
A3_SUCCESSORS = MappingProxyType({
    'docs/briefs/pre-registration/2026-10-02-tradeify-route-native-editions-successor-prereg.md':
        ('| ORB-3 ', _EXPOSURE, _OWED),
    'docs/briefs/pre-registration/2026-10-02-tradeify-vanguard-fixed-stop-edition-successor-prereg.md':
        ('| VAN-3 ', _EXPOSURE, _OWED),
})
# The validator reads HEAD, the tree and the interpreter here, never from an argument (row A5).
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
RUN_ROOT_NAME = 't00-step3'
RNG_TAG = 't00-screen-rng/v1'
BLOCK_FAMILY = 'JOINT_FLAT_BOTH_RUNS'
POPULATIONS = journal.POPULATIONS
# Step 12's compiled RNG roots and probe root (#581 values block); the successor's are disjoint (S-5).
STEP12_RNG_ROOTS = ('42', '123', '2026', 'probe')
STARTUP_V1, STARTUP_V2 = 'qualification-source-startup/v1', 'qualification-source-startup/v2'
STARTUP_ROLE = 'source_startup_policy'


@dataclass(frozen=True)
class PurposeProfile:
    """One purpose's row: its grants, evidence class, ``PREREG_CHAIN`` index, contract rule
    (``R3C_COMPILED``: the compiled r3c digest; ``R3C_DERIVED``: the carried digest, derived from
    r3c by S-3) and expressions rule (``DECLARED_BOOK``, or ``SIZE_VECTOR`` bound to the vector)."""
    grants: tuple[str, ...]
    evidence_class: str
    chain_entry: int
    contract_rule: str
    expressions_rule: str


PURPOSE_PROFILES = MappingProxyType({
    SCREEN_PURPOSE: PurposeProfile(SCREEN_GRANTS, SCREEN_EVIDENCE_CLASS, 0, 'R3C_COMPILED', 'DECLARED_BOOK'),
    SUCCESSOR_PURPOSE: PurposeProfile(SUCCESSOR_GRANTS, SUCCESSOR_EVIDENCE_CLASS, 1, 'R3C_DERIVED', 'SIZE_VECTOR'),
})


def _profile(purpose) -> PurposeProfile | None:
    return PURPOSE_PROFILES.get(purpose) if type(purpose) is str else None


def _successor(doc) -> bool:
    return PURPOSE_PROFILES[doc['purpose']].contract_rule == 'R3C_DERIVED'

PARAMETER_KEYS = frozenset({
    'expressions', 'scenarios', 'initial_state', 'horizon_sessions', 'rng', 'depth_per_root', 'block',
    'path_start_date', 'pass_floor_halves', 'deadline_only_is_bust', 'run1_diagnostic', 'a5_rule',
    'median_rule', 'budget'})
# Closed field set (row A1): top-level name -> its closed sub-field set, or None for a leaf.
SCREEN_AUTHORITY_FIELDS = MappingProxyType({
    'schema': None, 'authority_id': None, 'purpose': None, 'grants': None, 'refusals': None,
    'evidence_class': None, 'source': frozenset({'contract_sha256'}), 'run_root_sha256': None,
    'p7': frozenset({'record_sha256', 'code_head', 'code_closure_sha256', 'bootstrap_sha256', 'interpreter'}),
    'prereg': frozenset({'path', 'ratifying_commit', 'commit', 'blob_sha256', 'a5_text_sha256',
                         'a6_text_sha256'}),
    'a3_answers': frozenset({'path', 'commit', 'blob_sha256'}),
    'parameters': PARAMETER_KEYS, 'source_trust': None,
})
SCREEN_ACT_FIELDS = frozenset({'schema', 'authority_sha256', 'act', 'ledger_head_sha256', 'statement', 'readers'})
ACT_KINDS = ('TERMINATE', 'CONTINUE')
EXPOSURES = ('seen', 'not seen')

# #581's values block and §3 pointers (row A8). Encoding proposed by P-A for the coordinator to
# freeze: one fence in §6 opened by "```t00-step2-values/v1" whose single content line is
# canonical_json_bytes(parameters); each active §3 item's Ratified value cell names its keys only.
VALUES_SCHEMA = 't00-step2-values/v1'
SECTION3_KEYS = MappingProxyType({
    1: ('depth_per_root', 'budget'), 2: ('pass_floor_halves',), 3: ('deadline_only_is_bust',),
    4: ('rng', 'block', 'path_start_date'), 5: ('run1_diagnostic',), 7: ('scenarios',), 8: ('a5_rule',)})
# The whole Status field: one backticked RATIFIED <date> (an optional final period), then free text.
_RATIFIED = re.compile(r'\*\*Status:\*\* `RATIFIED ([0-9]{4}-[0-9]{2}-[0-9]{2})\.?`(?: .*)?')
_RATIFYING_LINE = '- **Ratifying commit SHA:**'
_SECTION6_FIELDS = ('- **Ruling:**', '- **OD-1 / OD-2:**')
_ORIGIN_MAIN = 'refs/remotes/origin/main'
_COMMIT = re.compile(r'[0-9a-f]{40}')
_SHA256 = re.compile(r'[0-9a-f]{64}')
_P7_BOUND = ('code_head', 'code_closure_sha256', 'bootstrap_sha256', 'interpreter')


class ScreenAuthorityError(ContractValidationError):
    """A screen refusal; the message leads with its code."""

    def __init__(self, code: str, detail: str):
        super().__init__(f'{code}: {detail}')
        self.code = code


def _refuse(code, condition, detail):
    if condition:
        raise ScreenAuthorityError(code, detail)


def _hex(value, pattern=_SHA256):
    return type(value) is str and pattern.fullmatch(value) is not None


def _text(value):
    return type(value) is str and value != ''


def _positive(value):
    """A count: a positive integer (never bool)."""
    return type(value) is int and value > 0


def _budget(value):
    """A CPU-seconds budget (design §3 ``budget``: finite and positive; no maximum): a positive
    int (finite as it stands, never converted to float) or a finite positive float; never bool."""
    if type(value) is int:
        return value > 0
    return type(value) is float and math.isfinite(value) and value > 0


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _freeze(value):
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    return value


def _git(*args: str) -> tuple[int, bytes]:
    """``git`` at the fixed repository root with ``core.autocrlf=false``. Callers pass signed
    values only, and only after ``--end-of-options``."""
    done = subprocess.run(['git', '-C', str(REPOSITORY_ROOT), '-c', 'core.autocrlf=false', *args],
                          capture_output=True, check=False)
    return done.returncode, done.stdout


def _is_ancestor(older: str, newer: str) -> bool:
    return _git('merge-base', '--is-ancestor', '--end-of-options', older, newer)[0] == 0


def _blob(commit: str, path: str) -> bytes | None:
    status, out = _git('cat-file', 'blob', '--end-of-options', f'{commit}:{path}')
    return out if status == 0 else None


# ---- step 1: the bytes alone (rows A1, A4, A11) ----------------------------------------------

def _check_document(doc) -> None:
    code = 'SCREEN_AUTHORITY_FIELDS'
    _refuse(code, type(doc) is not dict or set(doc) != set(SCREEN_AUTHORITY_FIELDS),
            'the authority field set is closed')
    for name in ('source', 'p7', 'prereg'):
        _refuse(code, type(doc[name]) is not dict or set(doc[name]) != SCREEN_AUTHORITY_FIELDS[name],
                f'{name} fields differ from the closed set')
    profile = _profile(doc['purpose'])
    _refuse(code, doc['schema'] != SCREEN_SCHEMA or profile is None
            or doc['grants'] != list(profile.grants) or doc['refusals'] != list(SCREEN_REFUSALS)
            or doc['evidence_class'] != profile.evidence_class,
            'schema, purpose, grants, refusals and evidence_class must be exact')
    _refuse(code, not _text(doc['authority_id']), 'authority_id must be non-empty text')
    answers = doc['a3_answers']
    _refuse(code, type(answers) is not list or any(
        type(row) is not dict or set(row) != SCREEN_AUTHORITY_FIELDS['a3_answers'] for row in answers),
        'a3_answers rows differ from the closed set')
    p7, prereg = doc['p7'], doc['prereg']
    # Row A4: unsigned text never reaches git unchecked.
    commits = (p7['code_head'], prereg['ratifying_commit'], prereg['commit'], *(row['commit'] for row in answers))
    _refuse(code, not all(_hex(value, _COMMIT) for value in commits),
            'every commit field must match ^[0-9a-f]{40}$')
    _refuse(code, any(type(row['path']) is not str for row in answers),
            'every a3_answers path must be text')
    _refuse(code, type(prereg['path']) is not str or prereg['path'] != PREREG_CHAIN[profile.chain_entry]
            or sorted(row['path'] for row in answers) != sorted(A3_SUCCESSORS),
            'every path must equal a compiled constant')
    digests = (doc['source']['contract_sha256'], doc['run_root_sha256'], p7['record_sha256'],
               p7['code_closure_sha256'], p7['bootstrap_sha256'], prereg['blob_sha256'],
               prereg['a5_text_sha256'], prereg['a6_text_sha256'], *(row['blob_sha256'] for row in answers))
    _refuse(code, not all(map(_hex, digests)), 'every digest must be a lowercase SHA-256')
    _refuse(code, type(p7['interpreter']) is not dict or type(doc['source_trust']) is not dict,
            'p7.interpreter and source_trust must be objects')
    _check_parameters(doc['parameters'], profile)


def _expressions(value, profile) -> bool:
    """Row A11's ``expressions``: the declared book, or under the successor the declared book bound
    to its size vector, ``{"base": "DECLARED_BOOK", "size_vector_sha256": <hex>}``."""
    if profile.expressions_rule == 'DECLARED_BOOK':
        return value == 'DECLARED_BOOK'
    return (type(value) is dict and set(value) == {'base', 'size_vector_sha256'} and value['base'] == 'DECLARED_BOOK'
            and _hex(value['size_vector_sha256']))


def _check_parameters(params, profile=None) -> None:  # pylint: disable=too-many-locals
    """Row A11 on the bytes; its receipt-bound rules run in ``_check_bindings``. ``profile`` is the
    document's purpose row (the original purpose's by default)."""
    code = 'SCREEN_PARAMETER_UNSUPPORTED'
    profile = PURPOSE_PROFILES[SCREEN_PURPOSE] if profile is None else profile
    _refuse(code, type(params) is not dict or set(params) != PARAMETER_KEYS, 'parameters are a closed set')
    rng, depth, block, budget = params['rng'], params['depth_per_root'], params['block'], params['budget']
    horizon = params['horizon_sessions']
    rng_ok = (type(rng) is dict and set(rng) == {'tag', 'roots', 'probe_root'} and rng['tag'] == RNG_TAG
              and type(rng['roots']) is list and len(rng['roots']) == 3 and all(map(_text, rng['roots']))
              and len(set(rng['roots'])) == 3 and _text(rng['probe_root'])
              and rng['probe_root'] not in rng['roots'])
    if rng_ok and profile.contract_rule == 'R3C_DERIVED':  # S-5: keys disjoint from step 12's
        rng_ok = not set(STEP12_RNG_ROOTS) & {*rng['roots'], rng['probe_root']}
    supported = {
        'expressions': _expressions(params['expressions'], profile),
        'scenarios': params['scenarios'] == ['S0'],
        'initial_state': type(params['initial_state']) is dict,
        'horizon_sessions': type(horizon) is int and horizon == verdict.A6_HORIZON_SESSIONS,
        'rng': rng_ok,
        'depth_per_root': (type(depth) is dict and set(depth) == set(POPULATIONS)
                           and all(map(_positive, depth.values()))),
        'block': (type(block) is dict and set(block) == {'family', 'length_sessions'}
                  and block['family'] == BLOCK_FAMILY and _positive(block['length_sessions'])
                  and type(horizon) is int and horizon % block['length_sessions'] == 0),
        'path_start_date': _text(params['path_start_date']),
        'pass_floor_halves': params['pass_floor_halves'] in ('BINDING', 'REPORTED'),
        'deadline_only_is_bust': type(params['deadline_only_is_bust']) is bool,
        'run1_diagnostic': params['run1_diagnostic'] == 'WAIVED',
        'a5_rule': type(params['a5_rule']) is str and params['a5_rule'] in verdict.A5_RULE_IDS,
        'median_rule': params['median_rule'] == verdict.MEDIAN_RULE,
        'budget': (type(budget) is dict and set(budget) == {'path_cpu_seconds', 'overhead_cpu_seconds', 'basis'}
                   and _budget(budget['path_cpu_seconds']) and _budget(budget['overhead_cpu_seconds'])
                   and _text(budget['basis'])),
    }
    unsupported = sorted(name for name, ok in supported.items() if not ok)
    _refuse(code, unsupported, 'unsupported: ' + ', '.join(unsupported))


# ---- step 2: the signature (rows A2, A3) -----------------------------------------------------

def _screen_lifecycle(approval: ApprovalRecord, now: datetime, key_sha256: str) -> None:
    """``_check_source_key_lifecycle`` with the screen expiry named as such (row K2); the key
    codes stay, because one key signs both approvals."""
    try:
        _check_source_key_lifecycle(approval, now, key_sha256)
    except ContractValidationError as exc:
        if str(exc).startswith('SOURCE_APPROVAL_EXPIRED'):
            raise ScreenAuthorityError('SCREEN_APPROVAL_EXPIRED',
                                       'the screen approval is not valid at this time') from None
        raise


def _verify_operator_approval(approval_bytes, public_keys, *, scope, subject_sha256, now):  # pylint: disable=too-many-locals
    """An OPERATOR approval by a pinned ``source:`` key over ``subject_sha256`` (as contract.py:1167-1195)."""
    pinned = _pinned_source_keys()
    _refuse('SCREEN_TRUST_ROOT_MISMATCH', not isinstance(public_keys, Mapping) or set(public_keys) != set(pinned)
            or any(type(raw) is not bytes or _sha(raw) != pinned[key].sha256 for key, raw in public_keys.items()),
            'supplied public keys differ from the pinned root')
    try:
        outer = parse_canonical_json(approval_bytes, label='approval')
    except ContractValidationError as exc:
        raise ScreenAuthorityError('SCREEN_APPROVAL_INVALID', str(exc)) from None
    signature = outer.get('signature') if isinstance(outer, dict) else None
    payload = outer.get('payload') if isinstance(outer, dict) else None
    signer = signature.get('key_id') if isinstance(signature, dict) else None
    authority = payload.get('authority_class') if isinstance(payload, dict) else None
    _refuse('SOURCE_KEY_ID', not isinstance(signer, str) or not signer.startswith(SOURCE_KEY_PREFIX),
            'screen approvals are signed only by source: keys')
    _refuse('SCREEN_TRUST_ROOT_MISMATCH', signer not in pinned, 'signer is not a pinned source key')
    _refuse('SCREEN_TRUST_ROOT_MISMATCH', authority != 'OPERATOR',
            f'TEST_ONLY or non-OPERATOR approval authority is refused: {authority!r}')
    revoked = pinned[signer].revoked_at
    _refuse('SOURCE_KEY_REVOKED', revoked is not None and now >= revoked, 'signing key is revoked in the pinned root')
    trusted = {key: TrustedApprovalKey(key, public_keys[key], 'OPERATOR', pinned[key].revoked_at) for key in pinned}
    try:
        approval = verify_detached_approval(
            approval_bytes, trusted_keys=trusted, expected_scope=scope, expected_subject_sha256=subject_sha256,
            expected_contract_sha256=subject_sha256, now=now, allow_test_authority=False)
    except ContractValidationError as exc:
        raise ScreenAuthorityError('SCREEN_APPROVAL_INVALID', str(exc)) from None
    key_sha256 = _sha(public_keys[signer])
    _screen_lifecycle(approval, now, key_sha256)
    return approval, key_sha256


# ---- step 3: _check_bindings (rows A5-A10) ---------------------------------------------------

def _check_reality(doc) -> str:
    """Row A5: HEAD, a clean tree (untracked files included) and the interpreter, read here."""
    code = 'SCREEN_P7_MISMATCH'
    status, out = _git('rev-parse', '--verify', 'HEAD^{commit}')
    head = out.decode('ascii', errors='replace').strip()
    _refuse(code, status != 0 or not _hex(head, _COMMIT), 'HEAD cannot be read at the repository root')
    status, out = _git('status', '--porcelain', '--untracked-files=all')
    _refuse(code, status != 0 or out.strip(), 'the repository tree is not clean (untracked files included)')
    try:
        current = p7_evidence.current_interpreter_binding(REPOSITORY_ROOT)
    except (ValueError, OSError) as exc:  # a reachable base site-packages, an unreadable install
        raise ScreenAuthorityError(code, f'the running interpreter cannot be bound ({exc})') from None
    _refuse(code, current != doc['p7']['interpreter'],
            'the running interpreter differs from the bound P7 interpreter (including its install tree)')
    return head


def _derived_from_r3c(contract_doc) -> bool:
    """S-3: the contract with ``contract_id`` and its startup-policy row put back to r3c's compiled
    values hashes to the compiled r3c digest, so no other role or field differs from r3c."""
    if R3C_CONTRACT_ID is None or R3C_STARTUP_POLICY_ROW is None:
        return False
    rows = contract_doc['artifacts']
    at = [i for i, row in enumerate(rows) if row['role'] == STARTUP_ROLE]
    if len(at) != 1:
        return False
    restored = dict(contract_doc, contract_id=R3C_CONTRACT_ID,
                    artifacts=[dict(R3C_STARTUP_POLICY_ROW) if i == at[0] else row for i, row in enumerate(rows)])
    return _sha(canonical_json_bytes(restored)) == R3C_CONTRACT_SHA256


def _startup_bytes(artifact_root, path, digest) -> bytes | None:
    try:
        raw = (Path(artifact_root) / path).read_bytes()
    except (OSError, TypeError):
        return None
    return raw if _sha(raw) == digest else None


def _check_size_vector(doc, receipt, artifact_root) -> None:
    """S-3, S-5 and §2.5: r3d's startup bytes are the receipt's, a v2 policy equal to r3c's v1
    outside ``sizing``, whose vector is canonical, not the identity, and is the authority's
    ``size_vector_sha256 = sha256(canonical_json_bytes(sizing))``."""
    from .production_source import _json  # pylint: disable=import-outside-toplevel  # the source's own parser
    code = 'SCREEN_SOURCE_MISMATCH'
    row = next(row for row in receipt.artifacts if row.role == STARTUP_ROLE)
    r3d_raw = _startup_bytes(artifact_root, row.path, row.sha256)
    r3c_raw = _startup_bytes(artifact_root, R3C_STARTUP_POLICY_ROW['path'], R3C_STARTUP_POLICY_ROW['sha256'])
    _refuse(code, r3d_raw is None or r3c_raw is None,
            "the r3d and r3c startup bytes must be present under artifact_root at their contract digests")
    try:
        policy, r3c_policy = _json(r3d_raw), _json(r3c_raw)
    except (ValueError, UnicodeDecodeError) as exc:
        raise ScreenAuthorityError(code, f'a startup policy cannot be read ({exc})') from None
    unsupported = 'SCREEN_PARAMETER_UNSUPPORTED'
    _refuse(unsupported, type(policy) is not dict or policy.get('schema') != STARTUP_V2 or 'sizing' not in policy,
            'the successor requires a v2 startup policy with a sizing vector')
    _refuse(code, type(r3c_policy) is not dict or r3c_policy.get('schema') != STARTUP_V1
            or {k: v for k, v in policy.items() if k not in ('schema', 'sizing')}
            != {k: v for k, v in r3c_policy.items() if k != 'schema'},
            "the v2 startup policy differs from r3c's v1 policy outside sizing")
    try:
        vector = validate_size_vector(policy['sizing'])
    except (ValueError, TypeError, KeyError) as exc:
        raise ScreenAuthorityError(unsupported, f'the sizing vector is refused ({exc})') from None
    _refuse(unsupported, canonical_json_bytes(policy['sizing']) != canonical_json_bytes(vector.as_mapping()),
            'the sizing vector is not in its canonical encoding')
    _refuse(unsupported, vector.is_identity, 'the identity vector re-runs the declared book; it is not a successor')
    _refuse(unsupported, _sha(canonical_json_bytes(policy['sizing']))
            != doc['parameters']['expressions']['size_vector_sha256'],
            'size_vector_sha256 differs from sha256(canonical_json_bytes(sizing)) of the r3d startup policy')


def _check_contract(doc, receipt, artifact_root) -> None:
    """Row A6's contract rule, per purpose: the compiled r3c digest, or (successor, S-3) the carried
    digest, equal to the receipt's, not r3c's, derived from r3c and bound to the size vector."""
    code = 'SCREEN_SOURCE_MISMATCH'
    if not _successor(doc):
        _refuse(code, receipt.contract_sha256 != R3C_CONTRACT_SHA256
                or doc['source']['contract_sha256'] != R3C_CONTRACT_SHA256
                or receipt.evidence_class != SOURCE_EVIDENCE_CLASS,
                'the source receipt and the authority must both bind the compiled r3c digest (source evidence class)')
        return
    _refuse(code, receipt.evidence_class != SOURCE_EVIDENCE_CLASS, 'the source receipt is not of the source evidence class')
    _refuse(code, receipt.contract_sha256 != doc['source']['contract_sha256'],
            "the authority's contract digest is not the source receipt's")
    _refuse(code, receipt.contract_sha256 == R3C_CONTRACT_SHA256, 'the successor screens r3d, never r3c itself')
    _refuse(code, not _derived_from_r3c(parse_canonical_json(receipt.canonical_bytes, label='source contract')),
            "the derivation check fails: the contract differs from r3c beyond contract_id and the startup-policy row")
    _check_size_vector(doc, receipt, artifact_root)


def _check_source(doc, source_receipt, artifact_root, now):
    """Row A6, and row A11's receipt-bound rules (initial state, path start, L <= smallest pool)."""
    code = 'SCREEN_SOURCE_MISMATCH'
    try:
        receipt = require_validated_source_contract(source_receipt, now=now)
    except ContractValidationError as exc:
        raise ScreenAuthorityError(code, f'the source receipt is not issued and unexpired ({exc})') from None
    _check_contract(doc, receipt, artifact_root)
    run_root = (Path(artifact_root) / RUN_ROOT_NAME).resolve()
    _refuse('SCREEN_RUN_ROOT_MISMATCH', _sha(str(run_root).encode('utf-8')) != doc['run_root_sha256'],
            'run_root_sha256 differs from the resolved <private_root>/t00-step3 path')
    params = doc['parameters']
    contract_doc = parse_canonical_json(receipt.canonical_bytes, label='source contract')
    smallest = min(len(receipt.populations[name]) for name in POPULATIONS)
    _refuse('SCREEN_PARAMETER_UNSUPPORTED', params['initial_state'] != contract_doc['initial_state']
            or params['path_start_date'] != contract_doc['path_start_date']
            or params['block']['length_sessions'] > smallest,
            "initial_state and path_start_date must equal the receipt's, and L the smallest pool or less")
    return receipt, run_root


def _check_p7(doc, record_bytes, artifact_root, head) -> None:
    """Row A7: the P7 record binds by its bytes, compiled bootstrap, closure digest and current
    bytes. Only binding fields are read, never ``result`` (row X6)."""
    code = 'SCREEN_P7_MISMATCH'
    p7 = doc['p7']
    _refuse(code, type(record_bytes) is not bytes or _sha(record_bytes) != p7['record_sha256'],
            'the P7 record bytes do not hash to p7.record_sha256')
    try:
        record = p7_evidence.parse_record(record_bytes)
        bound = {name: record[name] for name in ('schema', 'contract_sha256', *_P7_BOUND)}
        closure_sha256 = p7_evidence.sha256_bytes(p7_evidence.canonical(record['loaded_closure']))
    except (KeyError, TypeError, ValueError) as exc:
        raise ScreenAuthorityError(code, f'the P7 record cannot be read ({exc})') from None
    _refuse(code, bound['schema'] != p7_evidence.RECORD_SCHEMA, 'the record is not a P7 record')
    if _successor(doc):  # S-3: the digest the authority carries, already equal to the receipt's
        _refuse(code, bound['contract_sha256'] != doc['source']['contract_sha256'],
                "the P7 record is not over the authority's contract")
    else:
        _refuse(code, bound['contract_sha256'] != R3C_CONTRACT_SHA256, 'the P7 record is not over r3c')
    _refuse(code, bound['code_head'] != head, 'the P7 record code_head is not HEAD')
    _refuse(code, bound['bootstrap_sha256'] != p7_evidence.P7_BOOTSTRAP_SHA256,
            'the P7 record bootstrap differs from the compiled P7_BOOTSTRAP_SHA256')
    _refuse(code, bound['code_closure_sha256'] != closure_sha256,
            'code_closure_sha256 is not the SHA-256 of the canonical loaded_closure')
    _refuse(code, any(p7[name] != bound[name] for name in _P7_BOUND),
            "the authority's p7 fields differ from the record's")
    try:
        p7_evidence._current_bytes_check(  # pylint: disable=protected-access
            record, code_root=REPOSITORY_ROOT, artifact_root=artifact_root)
    except (KeyError, TypeError, ValueError, OSError) as exc:
        raise ScreenAuthorityError(code, f'the P7 record fails the current-bytes check ({exc})') from None


def _section(lines, heading):
    starts = [i for i, line in enumerate(lines) if line.startswith(heading)]
    if len(starts) != 1:
        return None
    end = next((i for i in range(starts[0] + 1, len(lines)) if lines[i].startswith('## ')), len(lines))
    return lines[starts[0] + 1:end]


def _ratified(blob: bytes) -> bool:
    """Exactly one Status field, in its canonical place (title, blank line, Status line), whose
    complete field is RATIFIED with a valid ISO date."""
    lines = blob.decode('utf-8', errors='replace').split('\n')
    if (len(lines) < 3 or not lines[0].startswith('# ') or lines[1] != ''
            or [i for i, line in enumerate(lines) if line.startswith('**Status:**')] != [2]):
        return False
    found = _RATIFIED.fullmatch(lines[2])
    try:
        return found is not None and date.fromisoformat(found.group(1)).isoformat() == found.group(1)
    except ValueError:
        return False


def _values_and_cells(text: str, params) -> bool:
    """At C: the §6 Ruling and OD-1/OD-2 fields, the values block equal to ``parameters``, and
    each active §3 Ratified value cell naming only its block keys."""
    lines = text.split('\n')
    section3, section6 = _section(lines, '## §3'), _section(lines, '## §6')
    if section3 is None or section6 is None:
        return False
    for prefix in _SECTION6_FIELDS:
        found = [line[len(prefix):].strip() for line in section6 if line.startswith(prefix)]
        if len(found) != 1 or found[0] in ('', '—'):
            return False
    fences = [i for i, line in enumerate(section6) if line == '```' + VALUES_SCHEMA]
    if (len(fences) != 1 or fences[0] + 2 >= len(section6) or section6[fences[0] + 2] != '```'
            or section6[fences[0] + 1].encode('utf-8') != canonical_json_bytes(params)):
        return False
    for item, keys in SECTION3_KEYS.items():
        rows = [line.strip() for line in section3 if line.startswith(f'| {item} |')]
        expected = 'values block: ' + ', '.join(f'`{key}`' for key in keys)
        if len(rows) != 1 or not rows[0].endswith('|') or rows[0][:-1].split('|')[-1].strip() != expected:
            return False
    return True


def _check_prereg(prereg, params, profile) -> bytes:  # pylint: disable=too-many-locals
    """Row A8: C ratifies the purpose's chain entry (#581 or #733) with the values block; C′
    records C's SHA and nothing else."""
    code = 'SCREEN_PREREG_MISMATCH'
    path, ratifying, commit = prereg['path'], prereg['ratifying_commit'], prereg['commit']
    _refuse(code, path != PREREG_CHAIN[profile.chain_entry], "prereg.path is not the purpose's compiled chain entry")
    _refuse(code, not _is_ancestor(ratifying, commit), 'C is not an ancestor of C′')
    _refuse(code, not _is_ancestor(commit, _ORIGIN_MAIN), 'C′ is not reachable from origin/main')
    status, names = _git('diff', '--name-only', '--end-of-options', ratifying, commit)
    _refuse(code, status != 0 or names.decode('utf-8', errors='replace').splitlines() != [path],
            'C→C′ changes a file other than the pre-registration')
    at_c, at_c2 = _blob(ratifying, path), _blob(commit, path)
    _refuse(code, at_c is None or at_c2 is None or _sha(at_c2) != prereg['blob_sha256'],
            'prereg.blob_sha256 is not the blob at C′')
    before, after = at_c.split(b'\n'), at_c2.split(b'\n')
    changed = [i for i, (old, new) in enumerate(zip(before, after)) if old != new]
    _refuse(code, len(before) != len(after) or len(changed) != 1
            or not before[changed[0]].startswith(_RATIFYING_LINE.encode('utf-8'))
            or after[changed[0]] != f'{_RATIFYING_LINE} `{ratifying}`'.encode('utf-8'),
            'C→C′ must change only the §6 Ratifying commit SHA line, to C')
    try:
        text = at_c.decode('utf-8')
    except UnicodeDecodeError:
        text = ''
    _refuse(code, not _ratified(at_c) or not _values_and_cells(text, params),
            'at C the Status, §6 fields, values block or §3 cells are not ratified as bound')
    # Oldest by topology, not dates: every commit reachable from origin/main that changes the
    # file (full history, so a merged-away side branch is kept) and reads RATIFIED descends from C.
    status, history = _git('rev-list', '--full-history', '--end-of-options', _ORIGIN_MAIN, '--', path)
    ratified = [sha for sha in history.decode('ascii', errors='replace').split()
                if (blob := _blob(sha, path)) is not None and _ratified(blob)]
    _refuse(code, status != 0 or ratifying not in ratified
            or not all(sha == ratifying or _is_ancestor(ratifying, sha) for sha in ratified),
            'C is not the oldest RATIFIED commit reachable from origin/main')
    return at_c2


def _check_sections(prereg, blob: bytes) -> None:
    """Row A9: the A5/A6 text is frozen."""
    code = 'SCREEN_PREREG_MISMATCH'
    try:
        a5, a6 = verdict.section_text(blob, 'A5'), verdict.section_text(blob, 'A6')
    except ValueError as exc:
        raise ScreenAuthorityError(code, f'A5/A6 sections cannot be located ({exc})') from None
    _refuse(code, _sha(a5) != verdict.A5_TEXT_SHA256 or _sha(a6) != verdict.A6_TEXT_SHA256
            or prereg['a5_text_sha256'] != verdict.A5_TEXT_SHA256
            or prereg['a6_text_sha256'] != verdict.A6_TEXT_SHA256,
            'the A5/A6 text differs from the compiled section hashes')


def _check_a3(answers) -> None:
    """Row A10: in each successor, the first ORB-3/VAN-3 row is the only exposure line, not OWED."""
    code = 'SCREEN_A3_UNANSWERED'
    for answer in answers:
        prefix, exposure, owed = A3_SUCCESSORS[answer['path']]
        _refuse(code, not _is_ancestor(answer['commit'], _ORIGIN_MAIN), 'an A3 commit is not reachable')
        blob = _blob(answer['commit'], answer['path'])
        _refuse(code, blob is None or _sha(blob) != answer['blob_sha256'], 'an A3 blob digest differs')
        lines = blob.decode('utf-8', errors='replace').split('\n')
        rows = [i for i, line in enumerate(lines) if line.startswith(prefix)]
        marked = [i for i, line in enumerate(lines) if exposure.search(line)]
        _refuse(code, not rows or marked != [rows[0]] or owed.search(lines[rows[0]]) is not None,
                f'{prefix.strip("| ")} is not answered with its exposure marker')


def _check_bindings(doc, *, source_receipt, p7_record_bytes, artifact_root, now):
    """Rows A5-A10 (and A11's receipt-bound rules), with the whole record in hand."""
    head = _check_reality(doc)
    receipt, run_root = _check_source(doc, source_receipt, artifact_root, now)
    _check_p7(doc, p7_record_bytes, artifact_root, head)
    blob = _check_prereg(doc['prereg'], doc['parameters'], PURPOSE_PROFILES[doc['purpose']])
    _check_sections(doc['prereg'], blob)
    _check_a3(doc['a3_answers'])
    return head, receipt, run_root


# ---- step 4: the receipt, and its use (rows K1-K4) -------------------------------------------

@dataclass(frozen=True)
class ValidatedScreenAuthority:  # pylint: disable=too-many-instance-attributes
    """Issued only by ``validate_screen_authority``; bound to the exact ``source_receipt`` object."""
    authority_id: str
    authority_sha256: str
    canonical_bytes: bytes
    approval: ApprovalRecord
    approval_bytes: bytes
    key_sha256: str
    source_receipt: ValidatedSourceContract
    artifact_root: str
    run_root: str
    code_head: str
    parameters: Mapping[str, Any]
    p7: Mapping[str, Any]
    prereg: Mapping[str, Any]
    evidence_class: str = SCREEN_EVIDENCE_CLASS


_ISSUED: dict[int, tuple[weakref.ReferenceType, object, weakref.ReferenceType]] = {}


def _thaw(value):
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw(item) for item in value]
    return value


def _snapshot(auth: ValidatedScreenAuthority):
    # parameters may hold float budgets, which _receipt_snapshot does not take: snapshot their bytes.
    return (_receipt_snapshot(replace(auth, source_receipt=None, parameters=None)),
            canonical_json_bytes(_thaw(auth.parameters)))


def validate_screen_authority(  # pylint: disable=too-many-arguments,too-many-locals
        authority_bytes, approval_bytes, public_keys, *, source_receipt, p7_record_bytes, artifact_root,
        now) -> ValidatedScreenAuthority:
    """Validate a signed screen authority (design §3.2); no HEAD, tree, interpreter or reader argument."""
    _refuse('SCREEN_AUTHORITY_FIELDS', type(authority_bytes) is not bytes or type(approval_bytes) is not bytes,
            'the authority and approval require immutable bytes')
    try:
        doc = parse_canonical_json(authority_bytes, label='screen authority')
    except ContractValidationError as exc:
        raise ScreenAuthorityError('SCREEN_AUTHORITY_FIELDS', str(exc)) from None
    _check_document(doc)                                                          # 1: A1, A4, A11
    authority_sha256 = _sha(authority_bytes)
    _refuse('SCREEN_TRUST_ROOT_MISMATCH', doc['source_trust'] != _source_trust_document(_pinned_source_keys()),
            'source_trust differs from the pinned root')                          # 2: A2, A3
    approval, key_sha256 = _verify_operator_approval(approval_bytes, public_keys, scope=SCREEN_SCOPE,
                                                     subject_sha256=authority_sha256, now=now)
    head, receipt, run_root = _check_bindings(doc, source_receipt=source_receipt,  # 3: A5-A10
                                              p7_record_bytes=p7_record_bytes, artifact_root=artifact_root, now=now)
    auth = ValidatedScreenAuthority(                                               # 4: issue
        authority_id=doc['authority_id'], authority_sha256=authority_sha256, canonical_bytes=bytes(authority_bytes),
        approval=approval, approval_bytes=bytes(approval_bytes), key_sha256=key_sha256, source_receipt=receipt,
        artifact_root=str(Path(artifact_root).resolve()), run_root=str(run_root), code_head=head,
        parameters=_freeze(doc['parameters']), p7=_freeze(doc['p7']), prereg=_freeze(doc['prereg']),
        evidence_class=doc['evidence_class'])
    identity = id(auth)
    _ISSUED[identity] = (weakref.ref(auth, lambda ref: _ISSUED.pop(identity, None)), _snapshot(auth),
                         weakref.ref(receipt))
    return auth


def _require_issued(auth):
    issued = _ISSUED.get(id(auth))
    _refuse('SCREEN_AUTHORITY_UNISSUED', type(auth) is not ValidatedScreenAuthority or issued is None
            or issued[0]() is not auth or issued[1] != _snapshot(auth),
            'a validator-issued, unchanged screen authority is required')
    return issued


def _norm(path) -> str:
    return os.path.normcase(os.path.realpath(path))


def _lock_held(path: Path) -> bool:
    """A non-blocking attempt on the run lock's byte at ``journal.LOCK_OFFSET`` fails (card §3.4)."""
    try:
        import msvcrt  # pylint: disable=import-outside-toplevel
    except ImportError:  # the run lock is a Windows byte-range lock
        return False
    fd = os.open(path, os.O_RDONLY | getattr(os, 'O_BINARY', 0))
    try:
        os.lseek(fd, journal.LOCK_OFFSET, os.SEEK_SET)
        try:
            msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
        except OSError as exc:  # a conflict is EACCES (CRT _locking: "Locking violation")
            if exc.errno == errno.EACCES:
                return True
            raise ScreenAuthorityError('SCREEN_RUN_UNBOUND', f'the run lock cannot be tested ({exc})') from None
        os.lseek(fd, journal.LOCK_OFFSET, os.SEEK_SET)
        msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
        return False
    finally:
        os.close(fd)


def _check_run(recorder, auth) -> None:
    """Row K4: the write-once binding names this authority's run directory, whose ledger opens
    with a durable AUTHORITY_BOUND for it and whose run lock this process's parent holds."""
    code = 'SCREEN_RUN_UNBOUND'
    run_dir = Path(auth.run_root) / auth.authority_sha256
    _refuse(code, getattr(recorder, 'screen_run', None) != (_norm(run_dir), auth.authority_sha256),
            "this process is not bound to this authority's run directory")
    try:
        ledger = journal.read(run_dir / 'ledger' / '0001.jsonl', prev_sha256=None)
        pid, host = journal.read_lock(run_dir / 'lock')
        held = _lock_held(run_dir / 'lock')
    except (OSError, ValueError) as exc:
        raise ScreenAuthorityError(code, f'the run record cannot be read ({exc})') from None
    _refuse(code, not ledger or ledger[0]['type'] != 'AUTHORITY_BOUND'
            or ledger[0]['body']['authority_sha256'] != auth.authority_sha256,
            'the ledger does not open with a durable AUTHORITY_BOUND for this authority')
    _refuse(code, pid != os.getppid() or host != socket.gethostname() or not held,
            "the run lock is not held by this process's parent")


def require_validated_screen_authority(auth, *, source_contract, now) -> ValidatedScreenAuthority:
    """Every use (rows K1-K4): the exact receipt object, both windows and the pin lifecycle, the
    screen bootstrap and a ledgered run."""
    issued = _require_issued(auth)
    _refuse('SCREEN_REQUIRES_SOURCE_RECEIPT', type(source_contract) is not ValidatedSourceContract,
            'the screen serves only a source-only receipt')
    successor = auth.evidence_class == SUCCESSOR_EVIDENCE_CLASS
    bound = (parse_canonical_json(auth.canonical_bytes, label='screen authority')['source']['contract_sha256']
             if successor else R3C_CONTRACT_SHA256)
    _refuse('SCREEN_SOURCE_MISMATCH', source_contract is not auth.source_receipt or issued[2]() is not source_contract
            or source_contract.contract_sha256 != bound
            or (successor and source_contract.contract_sha256 == R3C_CONTRACT_SHA256)
            or source_contract.evidence_class != SOURCE_EVIDENCE_CLASS,
            'the source receipt is not the object this authority binds')
    require_validated_source_contract(source_contract, now=now)          # r3c window and pin: SOURCE_* codes
    _screen_lifecycle(auth.approval, now, auth.key_sha256)               # screen window: SCREEN_APPROVAL_EXPIRED
    recorder = getattr(sys, 'p7_recorder', None)
    _refuse('SCREEN_BOOTSTRAP_MISMATCH', getattr(recorder, 'bootstrap_sha256', None)
            != p7_evidence.SCREEN_BOOTSTRAP_SHA256, 'only a screen-bootstrap process serves the screen')
    _check_run(recorder, auth)
    return auth


def bind_screen_run(run_dir, authority_sha256: str) -> None:
    """Row K4's write-once run binding, called once by ``t00_screen.worker`` (card K-4, O-7)."""
    recorder = getattr(sys, 'p7_recorder', None)
    _refuse('SCREEN_BOOTSTRAP_MISMATCH', getattr(recorder, 'bootstrap_sha256', None)
            != p7_evidence.SCREEN_BOOTSTRAP_SHA256, 'only a screen-bootstrap process binds a run')
    _refuse('SCREEN_RUN_UNBOUND', getattr(recorder, 'screen_run', None) is not None, 'the run binding is write-once')
    _refuse('SCREEN_RUN_UNBOUND', not _hex(authority_sha256), 'authority_sha256 must be a SHA-256')
    recorder.screen_run = (_norm(run_dir), authority_sha256)


# ---- the capability's wrapper and epochs (design §3.3; rows K6 and K8 are P-B2's tests) -------

@dataclass(frozen=True)
class ScreenBracket:
    """A ``BracketReplayResult`` plus each run's deadline flag and consumed splits."""
    bracket: BracketReplayResult
    deadline_failure: tuple[bool, bool]
    consumed_splits: tuple[tuple, tuple]

    def __post_init__(self):
        if type(self.bracket) is not BracketReplayResult:
            raise ValueError('ScreenBracket requires a BracketReplayResult')
        if (type(self.deadline_failure) is not tuple or len(self.deadline_failure) != 2
                or any(type(flag) is not bool for flag in self.deadline_failure)):
            raise ValueError('ScreenBracket requires one bool deadline flag per run')
        if (type(self.consumed_splits) is not tuple or len(self.consumed_splits) != 2
                or any(type(splits) is not tuple for splits in self.consumed_splits)):
            raise ValueError('ScreenBracket requires one tuple of consumed splits per run')


@dataclass(frozen=True, eq=False)
class ScreenEpoch:
    """One worker epoch, issued by ``open_screen_epoch`` for one (source, authority)."""
    authority_sha256: str
    guard_sha256: str
    closure_sha256: str


@dataclass(frozen=True)
class ScreenEpochClose:
    """``close_screen_epoch``'s result: the full final loaded closure (families first_party,
    third_party, ports, stdlib; for the EPOCH_CLOSE writer under the K6 amendment ruled
    2026-10-04T20:30:58Z), its canonical digest, and whether every closing check held."""
    closure_sha256: str
    closure_match: bool
    closure: Mapping[str, Any]


_EPOCHS: dict[int, dict[str, Any]] = {}


# Every dependency family the recorder keeps, as P7's loaded_closure records them
# (p7_evidence.finish_record): module rows keyed by name, ports keyed by artifact path, stdlib
# names. ``distributions`` is derived from third_party at P7 record time, not recorded.
CLOSURE_FAMILIES = ('first_party', 'third_party', 'ports', 'stdlib')


def _closure() -> dict:
    """The recorder's full loaded closure: every family, copied, in a canonical order."""
    recorder = getattr(sys, 'p7_recorder', None)

    def rows(family):
        return dict(getattr(recorder, family, None) or {})
    return {
        'first_party': {name: dict(row) for name, row in sorted(rows('first_party').items())},
        'third_party': {name: dict(row) for name, row in sorted(rows('third_party').items())},
        'ports': dict(sorted(rows('ports').items())),
        'stdlib': sorted(getattr(recorder, 'stdlib', None) or ()),
    }


def _guard(auth: ValidatedScreenAuthority) -> tuple:
    """(path, size, mtime_ns, inode, device) of every r3c artifact, tracked first-party file,
    the interpreter and the lock file (§3.3 stat guard). First-party files are every tracked
    file under ops/ and core/ plus every tracked *.py under the code root: the bootstrap's
    permitted import roots are core, lab, ops, ops/c1_rail, ops/c1_signal_daemon and the code
    root itself (p7_evidence.py:241-242), and it treats any *.py there as first party (:338)."""
    status, out = _git('ls-files', '-z', '--', 'ops', 'core', '*.py')
    _refuse('SCREEN_EPOCH_STALE', status != 0, 'tracked first-party files cannot be listed')
    root = Path(auth.artifact_root)
    paths = [root / row.path for row in auth.source_receipt.artifacts]
    paths += [REPOSITORY_ROOT / name for name in out.decode('utf-8').split('\0') if name]
    paths += [Path(sys.executable), Path(getattr(sys, '_base_executable', sys.executable)),
              REPOSITORY_ROOT / 'requirements-ops.lock']
    rows = []
    for path in paths:
        try:
            stat = os.stat(path)
            rows.append((str(path), stat.st_size, stat.st_mtime_ns, stat.st_ino, stat.st_dev))
        except OSError:
            rows.append((str(path), None, None, None, None))
    return tuple(rows)


def open_screen_epoch(source, authority) -> ScreenEpoch:
    """Record the stat-guard set and loaded closure for (source, authority); called by
    ``screen_epoch`` after its full integrity check."""
    _require_issued(authority)
    guard = _guard(authority)
    closure = _closure()
    epoch = ScreenEpoch(authority.authority_sha256, _sha(canonical_json_bytes(guard)),
                        _sha(canonical_json_bytes(closure)))
    identity = id(epoch)
    _EPOCHS[identity] = {'epoch': weakref.ref(epoch, lambda ref: _EPOCHS.pop(identity, None)),
                         'source': weakref.ref(source), 'authority': weakref.ref(authority),
                         'guard': guard, 'closure': closure, 'open': True}
    return epoch


def _open_entry(epoch):
    entry = _EPOCHS.get(id(epoch))
    _refuse('SCREEN_EPOCH_REQUIRED', type(epoch) is not ScreenEpoch or entry is None
            or entry['epoch']() is not epoch or not entry['open'], 'an open screen epoch is required')
    return entry


def require_open_screen_epoch(epoch, *, source, authority) -> None:
    """The epoch is open and issued for (source, authority), and no guarded file changed."""
    entry = _open_entry(epoch)
    _refuse('SCREEN_EPOCH_REQUIRED', entry['source']() is not source or entry['authority']() is not authority,
            'the epoch was issued for another source or authority')
    _refuse('SCREEN_EPOCH_STALE', _guard(authority) != entry['guard'], 'a guarded file changed since the epoch opened')


def _file_is(path: Path, digest) -> bool:
    return path.is_file() and _sha(path.read_bytes()) == digest


def _closure_holds(opened: dict, closure: dict, authority) -> bool:
    """Byte-exact over every family: no dependency recorded at open is gone at close; every
    first-party module equals its bytes at load and its blob at H; every third-party module its
    bytes at load under the recorded site-packages; every port its bytes at load under the
    artifact root (its compile filename); and every loaded module has a recorded load digest.
    A lazy import recorded after open is valid when it meets the same checks; agreement across
    epochs stays row K6's (``state.check_record``)."""
    for family in CLOSURE_FAMILIES:
        if set(opened[family]) - set(closure[family]):
            return False
    # The recorder overwrites a third-party or port entry when it is found or compiled again
    # (p7_evidence bootstrap); a digest recorded at open must still be the one at close.
    for family in ('first_party', 'third_party', 'ports'):
        if any(closure[family][name] != row for name, row in opened[family].items()):
            return False
    for row in closure['first_party'].values():
        if row.get('path') is None:
            continue
        blob = _blob(authority.code_head, row['path'])
        if not _file_is(REPOSITORY_ROOT / row['path'], row['sha256']) or blob is None or _sha(blob) != row['sha256']:
            return False
    site = getattr(getattr(sys, 'p7_recorder', None), 'site_packages_path', None)
    for row in closure['third_party'].values():
        if row.get('path') is not None and (site is None or not _file_is(Path(site) / row['path'], row['sha256'])):
            return False
    if not all(_file_is(Path(authority.artifact_root) / name, digest) for name, digest in closure['ports'].items()):
        return False
    return not _unrecorded(closure)


def _under(path: str, root: str) -> bool:
    return (path + os.sep).startswith(root.rstrip(os.sep) + os.sep)


def _unrecorded(closure: dict) -> tuple[str, ...]:
    """Loaded modules with a file origin and no recorded load digest. A module is recorded when
    its name is a hashed first- or third-party row or a recorded stdlib name, its origin is a
    port's compile filename, or its origin file is the file of a hashed row (an extension that
    registers a second sys.modules name, e.g. pandas' ``_cyutility``, executes the recorded
    file). Modules the interpreter loads before the audit hook is installed are never in the
    recorder's stdlib set; under the recorder's interpreter roots they are, like recorded stdlib
    names, bytes-free and bound through the pinned interpreter."""
    recorder = getattr(sys, 'p7_recorder', None)
    site = getattr(recorder, 'site_packages_path', None)
    roots = [_norm(root) for root in (getattr(recorder, 'installed_roots', None) or ()) if root != site]
    code_root = getattr(recorder, 'code_root', None) or REPOSITORY_ROOT
    hashed = {name for family in ('first_party', 'third_party') for name, row in closure[family].items()
              if row.get('sha256') is not None}
    files = {_norm(Path(code_root) / row['path']) for row in closure['first_party'].values()
             if row.get('path') is not None and row.get('sha256') is not None}
    files |= {_norm(Path(site) / row['path']) for row in closure['third_party'].values()
              if site is not None and row.get('path') is not None and row.get('sha256') is not None}
    stdlib, ports = set(closure['stdlib']), set(closure['ports'])
    found = []
    for name, module in list(sys.modules.items()):
        origin = getattr(getattr(module, '__spec__', None), 'origin', None) or getattr(module, '__file__', None)
        if (not isinstance(origin, str) or origin in ('built-in', 'frozen') or name in hashed or name in stdlib
                or origin.replace('\\', '/') in ports):
            continue
        real = _norm(origin)
        # Site-first, as the RecordingFinder classifies: a file under site-packages is never
        # interpreter-rooted, even when a stdlib root is its ancestor (POSIX lib/pythonX.Y).
        if real not in files and (site is not None and _under(real, _norm(site))
                                  or not any(_under(real, root) for root in roots)):
            found.append(name)
    return tuple(sorted(found))


def _interpreter_holds(authority) -> bool:
    """R-REC-2 at every close: the running interpreter binding, with its install-tree digest over
    the base install and the venv site-packages (``p7_evidence.install_tree_sha256``), still
    equals the one the authority bound at launch. This also catches a site-packages file changed
    after launch but before its first import (attack class 4). A file swapped and restored within
    the epoch is the accepted residual (class 3; ``p7_evidence`` threat model)."""
    return p7_evidence.current_interpreter_binding(REPOSITORY_ROOT) == _thaw(authority.p7['interpreter'])


def close_screen_epoch(epoch) -> ScreenEpochClose:
    """Close once: the full integrity check again, the interpreter binding (R-REC-2) and the
    loaded-closure check. A failure gives ``closure_match=False``, which ``state.check_record``
    reads as ``CODE_OR_ARTIFACT_DRIFT``."""
    entry = _open_entry(epoch)
    entry['open'] = False
    source, authority = entry['source'](), entry['authority']()
    closure = _closure()
    match = source is not None and authority is not None
    if match:
        try:
            source._verify_integrity()  # pylint: disable=protected-access
        except Exception:  # pylint: disable=broad-exception-caught  # any failure here is drift
            match = False
    try:
        match = match and _closure_holds(entry['closure'], closure, authority) and _interpreter_holds(authority)
    except Exception:  # pylint: disable=broad-exception-caught  # an unreadable dependency is drift
        match = False
    return ScreenEpochClose(_sha(canonical_json_bytes(closure)), match, closure)


# ---- the screen entry points (design §3.3; rows K5-K8). They live here, not on ProductionSource,
# so production_source imports no screen module (Codex r4180236028). Private source access is the
# screen capability's (A10b allowlist). -------------------------------------------------------
# pylint: disable=protected-access

def screen_epoch(source, *, authority) -> ScreenEpoch:
    """Open one worker epoch: the authority gate, then the full integrity check (row K6)."""
    from .production_source import ProductionSource, _is_source_only, _now
    if not isinstance(source, ProductionSource):
        raise TypeError('SCREEN_REQUIRES_PRODUCTION_SOURCE')
    if not _is_source_only(source.contract):
        raise ValueError('SCREEN_REQUIRES_SOURCE_RECEIPT: the screen serves only a source-only source')
    require_validated_screen_authority(authority, source_contract=source.contract, now=_now())
    source._verify_integrity()
    # The loaded-closure check close runs, at open: no epoch issues, so no engine is built,
    # over a closure that would close as drift (rows K5/K6; Codex r4179917167).
    loaded = _closure()
    _refuse('SCREEN_EPOCH_STALE', not _closure_holds(loaded, loaded, authority),
            'the loaded closure does not hold at open')
    return open_screen_epoch(source, authority)


def screen_bracket(source, path, *, authority, epoch) -> ScreenBracket:
    """R1 and R2 on fresh engines, unsealed, with each run's deadline flag and consumed splits.

    Every refusal fires before any engine is built (row K5)."""
    from .production_source import (BRACKET_RUNS, ProductionSource, ScheduleExecutionBracket, _consumed_splits,
                                    _is_source_only, _now)
    if not isinstance(source, ProductionSource):
        raise TypeError('SCREEN_REQUIRES_PRODUCTION_SOURCE')
    if not _is_source_only(source.contract):
        raise ValueError('SCREEN_REQUIRES_SOURCE_RECEIPT: the screen serves only a source-only source')
    from .replay import ReplayDeadlineFailure
    require_validated_screen_authority(authority, source_contract=source.contract, now=_now())
    require_open_screen_epoch(epoch, source=source, authority=authority)
    source._verify_identity()
    by_id = {s.session_id: s for s in source.sessions}
    if not path or any(by_id.get(s.source.session_id) != s.source for s in path):
        raise ValueError('path contains a source session outside retained covered panel')
    bracket = ScheduleExecutionBracket(source._quotes)
    results, failed, splits = [], [], []
    for run_id in BRACKET_RUNS:
        provider = bracket.for_run(run_id)
        engine = source._engine(provider)
        flag = False
        try:
            result = engine.run(path)
        except ReplayDeadlineFailure as exc:
            result, flag = exc.result, True
        results.append(result)
        failed.append(flag)
        splits.append(_consumed_splits(provider))
    return ScreenBracket(BracketReplayResult(*results), tuple(failed), tuple(splits))


# pylint: enable=protected-access


# ---- acts (rows X2, X3) ----------------------------------------------------------------------

@dataclass(frozen=True)
class ValidatedScreenAct:
    """A signed ``t00_screen_act/v1``, current at ``ledger_head_sha256``."""
    act_sha256: str
    act: str
    authority_sha256: str
    ledger_head_sha256: str
    readers: tuple
    approval: ApprovalRecord


def validate_screen_act(  # pylint: disable=too-many-arguments
        act_bytes, approval_bytes, public_keys, *, authority, ledger_head, now) -> ValidatedScreenAct:
    """Row X2 (closed fields; every reader seen or not seen) and row X3 (signed under
    ``APPROVE_T00_SCREEN_ACT``; binds ``sha256(authority)`` and the current ledger head).

    ``authority`` is the authority bytes; the caller checks their SHA-256 against the run's
    AUTHORITY_BOUND, and ``state.check_record`` re-checks recorded acts. Only the act approval's
    own window and the key lifecycle are checked, never the authority's or r3c's window.
    """
    code = 'SCREEN_ACT_FIELDS'
    _refuse(code, type(act_bytes) is not bytes or type(approval_bytes) is not bytes or type(authority) is not bytes,
            'the act, approval and authority require immutable bytes')
    try:
        doc = parse_canonical_json(act_bytes, label='screen act')
        _fields(doc, set(SCREEN_ACT_FIELDS), label='screen act')
    except ContractValidationError as exc:
        raise ScreenAuthorityError(code, str(exc)) from None
    _refuse(code, doc['schema'] != SCREEN_ACT_SCHEMA or doc['act'] not in ACT_KINDS
            or not _hex(doc['authority_sha256']) or not _hex(doc['ledger_head_sha256'])
            or not _text(doc['statement']), 'schema, act, digests and statement must be exact')
    readers = doc['readers']
    _refuse(code, type(readers) is not list or not readers or any(
        type(row) is not dict or set(row) != {'name', 'exposure'} or not _text(row['name'])
        or row['exposure'] not in EXPOSURES for row in readers)
        or len({row['name'] for row in readers}) != len(readers),
        'every reader is listed once, as seen or not seen')
    act_sha256 = _sha(act_bytes)
    try:
        approval, _ = _verify_operator_approval(approval_bytes, public_keys, scope=SCREEN_ACT_SCOPE,
                                                subject_sha256=act_sha256, now=now)
    except ScreenAuthorityError as exc:
        raise ScreenAuthorityError('SCREEN_ACT_UNSIGNED', str(exc)) from None
    _refuse(code, doc['authority_sha256'] != _sha(authority), 'the act binds another authority')
    _refuse('SCREEN_ACT_STALE', doc['ledger_head_sha256'] != ledger_head, 'the act binds an earlier ledger head')
    return ValidatedScreenAct(act_sha256, doc['act'], doc['authority_sha256'], doc['ledger_head_sha256'],
                              tuple((row['name'], row['exposure']) for row in readers), approval)


__all__ = [
    'A3_SUCCESSORS', 'PREREG_CHAIN', 'PURPOSE_PROFILES', 'PurposeProfile', 'R3C_CONTRACT_ID', 'R3C_CONTRACT_SHA256',
    'R3C_STARTUP_POLICY_ROW', 'REPOSITORY_ROOT', 'SCREEN_ACT_FIELDS', 'STEP12_RNG_ROOTS', 'SUCCESSOR_EVIDENCE_CLASS',
    'SUCCESSOR_GRANTS', 'SUCCESSOR_PURPOSE',
    'SCREEN_ACT_SCOPE', 'SCREEN_AUTHORITY_FIELDS', 'SCREEN_SCOPE', 'ScreenAuthorityError', 'ScreenBracket',
    'ScreenEpoch', 'ScreenEpochClose', 'ValidatedScreenAct', 'ValidatedScreenAuthority', 'bind_screen_run',
    'close_screen_epoch', 'open_screen_epoch', 'require_open_screen_epoch', 'require_validated_screen_authority',
    'validate_screen_act', 'validate_screen_authority',
]
