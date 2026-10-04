"""K3/RC-4 negative client cases, written before the slice (test-first).

What each case encodes, and where its text is owned:
- S5 decision draft §1.6 (docs/notes/2026-09-26-s5-decision-draft.md:156): "no salt or seed
  value reaches the `client` role through `STATUS`, `FETCH_PLAN_CHUNK` or the receipt before
  closure". F1 admission-check condition 2 requires these cases on the release's own bytes.
- Full-E1 spec §2.2a (docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md:84):
  the client view, its receipt digests, and client-side verification (F1 condition 3).
- F1 admission-check condition 1 (execution-slices ledger, RC-4 entry of 2026-09-27): the
  service refuses a `tb-s2-rng-v3` admission on a release without the digests-only view.

Every K3/RC-4 case is xfail(strict=True) until the slice lands. The slice removes the
markers and changes no assertion; only the two seam functions may be re-pointed to the
slice's fixture API (card docs/briefs/handoffs/2026-10-02-k3-rc4-service-salt-client-view-DRAFT.md
§3.2 and §4). The leak-detector self-test is not marked: it passes today and guards the
detectors the marked cases rely on.

Real SQLite journal and signed TEST_ONLY bundles. The admission guardian, the clock and
the OS runtime are simulated (test_campaign_cancellation.funded_service). Nothing here is
Linux evidence: F1 condition 2 needs the card's Linux node on the release's bytes.
"""
import base64
import hashlib
import json
import re
import secrets
from types import SimpleNamespace

import pytest

from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution import client
from c1_rail.qualification.execution.campaign_protocol import PLAN_CHUNK_LIMIT
from c1_rail.qualification.execution.campaign_store import CampaignStore
from c1_rail.qualification.execution.store import ExecutionStore

CLIENT = 1001
V3 = 'tb-s2-rng-v3'                          # owner text: full-E1 spec §2.4
DIGESTS_ONLY = 'client_view_digests_only'    # owner text: ledger RC-4 entry, F1 condition 1
VIEW_DIGEST = 'client_view_sha256'           # owner text: full-E1 spec §2.2a
VIEW_LENGTH = 'client_view_byte_length'      # owner text: full-E1 spec §2.2a
# PROPOSED names (card §3.2), not owner text. The coordinator freezes them at dispatch.
RECIPE_OPTION = 'rng_recipe'                 # build_bundle keyword: the frozen contract's recipe
VIEW_MODE_OPTION = 'client_plan_view_mode'   # build_bundle keyword and release field
COMMITMENT = 'salt_sha256'                   # admission-receipt field holding sha256(salt)

pending = pytest.mark.xfail(strict=True, reason='awaits K3/RC-4')


# --- Seams: the only functions the slice may re-point (card §3.2) -------------------------

def _v3_service(tmp_path, monkeypatch, **release):
    """Seam 1: a funded TEST_ONLY FULL_E1 service whose frozen contract uses `V3`.

    `client_plan_view_mode=None` means the installed release carries no plan-view mode.
    """
    from test_campaign_cancellation import funded_service
    options = {RECIPE_OPTION: V3, VIEW_MODE_OPTION: DIGESTS_ONLY, **release}
    return funded_service(tmp_path, monkeypatch, **options)


def _admit(instance, case):
    """Seam 2: play the simulated admission guardian to BOUND, then return what the client
    sees for the stored admission (an identical re-submission returns it)."""
    from test_campaign_cancellation import admit
    raw, _ = admit(instance, case)
    return json.loads(instance.handle_request(CLIENT, raw))


# --- Privileged reads and leak detectors ---------------------------------------------------

def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _request(case, operation, **values):
    from test_campaign_cancellation import request
    return request(case, operation, **values)


def _canonical_plan(instance, case, receipt):
    """The service's canonical plan, read through qexec's store (never a client route)."""
    bodies = [body for body in CampaignStore(instance.store).objects(case['attempt_id']).values()
              if _sha(body) == receipt['plan_sha256']]
    assert len(bodies) == 1, 'exactly one stored object is the canonical plan'
    return bodies[0]


def _seed_values(plan_bytes):
    """Every integer under a `seed` key, whatever the seed record's schema."""
    found, stack = set(), [json.loads(plan_bytes)]
    while stack:
        node = stack.pop()
        if isinstance(node, dict):
            found.update(v for k, v in node.items() if k == 'seed' and type(v) is int)
            stack.extend(node.values())
        elif isinstance(node, list):
            stack.extend(node)
    return found


def _strings(node):
    stack = [node]
    while stack:
        node = stack.pop()
        if isinstance(node, str):
            yield node
        elif isinstance(node, dict):
            stack.extend(node.values())
        elif isinstance(node, list):
            stack.extend(node)


_B64 = re.compile(r'[A-Za-z0-9+/]+={0,2}')


def _visible(*raws):
    """The given bytes plus every base64 string nested in their JSON, decoded recursively."""
    blobs, queue = list(raws), list(raws)
    while queue:
        try:
            doc = json.loads(queue.pop())
        except (ValueError, UnicodeDecodeError):
            continue
        for text in _strings(doc):
            if len(text) >= 8 and len(text) % 4 == 0 and _B64.fullmatch(text):
                try:
                    decoded = base64.b64decode(text, validate=True)
                except ValueError:
                    continue
                blobs.append(decoded)
                queue.append(decoded)
    return blobs


_DECIMAL = re.compile(rb'\d+')
_HEX = re.compile(rb'[0-9a-fA-F]+')
_HEX64 = re.compile(rb'(?<![0-9a-fA-F])[0-9a-fA-F]{64}(?![0-9a-fA-F])')


def _seed_leaks(blobs, seeds):
    """Seeds visible as a whole decimal or hexadecimal token in any blob."""
    decimal, hexa = set(), set()
    for blob in blobs:
        decimal.update(_DECIMAL.findall(blob))
        hexa.update(token.lower() for token in _HEX.findall(blob))
    return sorted(s for s in seeds if str(s).encode() in decimal
                  or format(s, 'x').encode() in hexa or format(s, '016x').encode() in hexa)


def _salt_leaks(blobs, commitment):
    """Salts visible in any blob: a 64-hex token, or 32 raw bytes, whose SHA-256 is the
    commitment under either candidate preimage encoding (card §3.1, item c2)."""
    leaks = set()
    for blob in blobs:
        candidates = [token.lower() for token in _HEX64.findall(blob)]
        if len(blob) == 32:
            candidates.append(blob.hex().encode())
        for text in candidates:
            if commitment in (_sha(bytes.fromhex(text.decode())), _sha(text)):
                leaks.add(text.decode())
    return sorted(leaks)


def _client_surface(instance, case, admitted, surface):
    """Every byte string the client role receives on one owner-named surface."""
    if surface == 'receipt':
        return [encoded(admitted)]
    if surface == 'status':
        return [instance.handle_request(CLIENT, _request(case, 'STATUS'))]
    receipt, replies, view = admitted['receipt'], [], bytearray()
    while len(view) < receipt[VIEW_LENGTH]:
        reply = instance.handle_request(CLIENT, _request(case, 'FETCH_PLAN_CHUNK',
            object_sha256=receipt[VIEW_DIGEST], offset=len(view), length=PLAN_CHUNK_LIMIT))
        replies.append(reply)
        view.extend(base64.b64decode(json.loads(reply)['bytes_b64']))
    # The reassembled view too: a value split across a chunk boundary is still a leak.
    return [*replies, bytes(view)]


# --- Detector self-test (passes today; not K3/RC-4 behaviour) -------------------------------

def test_leak_detectors_find_every_planted_seed_and_salt(tmp_path, monkeypatch):
    """The detectors are not vacuous: on a real canonical plan they find every seed, also
    base64-wrapped, and none once each seed is replaced by a digest. A planted salt is found
    under both candidate commitment encodings, as hex text or base64-wrapped raw bytes."""
    from test_campaign_admission import message, running
    instance, case = running(tmp_path, monkeypatch)
    receipt = json.loads(instance.handle_request(CLIENT, message(case)))['receipt']
    plan = _canonical_plan(instance, case, receipt)
    seeds = _seed_values(plan)
    assert seeds and len(seeds) == len(set(re.findall(rb'"seed":(\d+)', plan)))
    assert _seed_leaks(_visible(plan), seeds) == sorted(seeds)
    wrapped = encoded({'bytes_b64': base64.b64encode(plan).decode('ascii')})
    assert _seed_leaks(_visible(wrapped), seeds) == sorted(seeds)
    assert _seed_leaks([wrapped], seeds) == []  # why _visible exists
    scrubbed = re.sub(rb'"seed":\d+', lambda m: b'"seed":"%s"' % _sha(m.group()).encode(), plan)
    assert _seed_values(scrubbed) == set() and _seed_leaks(_visible(scrubbed), seeds) == []
    salt = secrets.token_bytes(32)
    for commitment in (_sha(salt), _sha(salt.hex().encode())):
        for planted in (encoded({'salt': salt.hex()}),
                        encoded({'b': base64.b64encode(salt).decode()}),
                        encoded({'b': base64.b64encode(salt.hex().encode()).decode()})):
            assert _salt_leaks(_visible(planted), commitment) == [salt.hex()]
        assert _salt_leaks(_visible(encoded({'commitment': commitment})), commitment) == []


# --- K3/RC-4 cases (xfail until the slice lands) --------------------------------------------

@pending
def test_receipt_binds_the_client_view_and_salt_commitment_beside_the_plan(tmp_path, monkeypatch):
    """Spec §2.2a and F1 condition 3: `client_view_sha256`/`client_view_byte_length` beside
    `plan_sha256`/`plan_byte_length`; spec §2.4: the receipt publishes the salt commitment
    (canonical 64 lowercase hex, delta K3 row) and the canonical plan is the v3 recipe's."""
    instance, case = _v3_service(tmp_path, monkeypatch)
    receipt = _admit(instance, case)['receipt']
    for field in ('plan_sha256', VIEW_DIGEST, COMMITMENT):
        assert type(receipt[field]) is str and re.fullmatch(r'[0-9a-f]{64}', receipt[field]), field
    for field in ('plan_byte_length', VIEW_LENGTH):
        assert type(receipt[field]) is int and receipt[field] > 0, field
    assert receipt[VIEW_DIGEST] != receipt['plan_sha256']
    assert json.loads(_canonical_plan(instance, case, receipt))['mechanics_version'] == V3


@pending
@pytest.mark.parametrize('surface', ['receipt', 'status', 'plan_chunks'])
def test_no_salt_or_seed_value_reaches_the_client_before_closure(tmp_path, monkeypatch, surface):
    """S5 draft §1.6 (F1 condition 2's negative client cases), on simulated runtime."""
    instance, case = _v3_service(tmp_path, monkeypatch)
    admitted = _admit(instance, case)
    assert admitted['state'] == 'BOUND' and admitted['validity'] == 'VALID'  # not closed
    receipt = admitted['receipt']
    seeds = _seed_values(_canonical_plan(instance, case, receipt))
    assert len(seeds) > 1
    blobs = _visible(*_client_surface(instance, case, admitted, surface))
    assert _seed_leaks(blobs, seeds) == []
    assert _salt_leaks(blobs, receipt[COMMITMENT]) == []


@pending
def test_client_is_served_only_the_client_view_before_closure(tmp_path, monkeypatch):
    """Spec §2.2a: the plan object served to the client is the client view; it reassembles
    to the receipt's client-view digest and length, and the canonical plan is refused."""
    instance, case = _v3_service(tmp_path, monkeypatch)
    admitted = _admit(instance, case)
    receipt = admitted['receipt']
    view = _client_surface(instance, case, admitted, 'plan_chunks')[-1]
    assert len(view) == receipt[VIEW_LENGTH] and _sha(view) == receipt[VIEW_DIGEST]
    with pytest.raises(ValueError):
        instance.handle_request(CLIENT, _request(case, 'FETCH_PLAN_CHUNK',
            object_sha256=receipt['plan_sha256'], offset=0, length=PLAN_CHUNK_LIMIT))


@pending
def test_client_verifies_the_reassembled_client_view_not_the_canonical_plan(monkeypatch):
    """Spec §2.2a / F1 condition 3, client side: with client-view digests in the receipt the
    client fetches only the client view and verifies it against them."""
    canonical, view = b'c' * (PLAN_CHUNK_LIMIT + 7), b'v' * (PLAN_CHUNK_LIMIT + 3)
    objects = {_sha(canonical): canonical, _sha(view): view}
    receipt = {'attempt_id': 'test', 'profile_sha256': 'a' * 64, 'plan_sha256': _sha(canonical),
               'plan_byte_length': len(canonical), VIEW_DIGEST: _sha(view), VIEW_LENGTH: len(view)}
    monkeypatch.setattr(client, '_configuration',
                        lambda path: ({}, SimpleNamespace(input_byte_limit=67108864, sha256='a' * 64)))
    requested = []

    def serving(substitute=None):
        def transport(_path, operation, fields):
            if operation == 'STATUS':
                return encoded({'receipt': receipt})
            requested.append(fields['object_sha256'])
            body = objects[fields['object_sha256']] if substitute is None else substitute
            part = body[fields['offset']:fields['offset'] + fields['length']]
            return encoded({'schema': 'qualification_campaign_plan_chunk/v1', 'attempt_id': 'test',
                            'object_sha256': fields['object_sha256'], 'offset': fields['offset'],
                            'total_byte_length': len(body), 'byte_length': len(part),
                            'bytes_b64': base64.b64encode(part).decode('ascii')})
        return transport

    monkeypatch.setattr(client, 'request', serving())
    assert client.fetch_campaign_plan('unused', attempt_id='test') == view
    assert set(requested) == {_sha(view)}
    # Same-length bytes under the client-view identity fail the client-view digest check.
    monkeypatch.setattr(client, 'request', serving(substitute=b'w' * len(view)))
    with pytest.raises(ValueError):
        client.fetch_campaign_plan('unused', attempt_id='test')


@pending
def test_v3_admission_is_refused_without_the_digests_only_view_and_consumes_no_attempt(
        tmp_path, monkeypatch):
    """F1 condition 1: refused before the binding transaction, so no admission work runs (no
    salt), and the same attempt ID is then admitted on a digests-only release."""
    from test_campaign_cancellation import Runtime
    refused, case = _v3_service(tmp_path / 'no-view-mode', monkeypatch, **{VIEW_MODE_OPTION: None})
    with pytest.raises(ValueError):
        refused.handle_request(CLIENT, _request(case, 'SUBMIT_E1'))
    assert Runtime.started == []
    admitted, other = _v3_service(tmp_path / 'digests-only', monkeypatch)
    assert other['attempt_id'] == case['attempt_id']
    admitted.store = ExecutionStore(refused.store.path)
    assert _admit(admitted, other)['receipt'][VIEW_DIGEST]
