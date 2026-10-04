"""T00 screen P-D follow-up: R-INT-1 and R-INT-2 (build card §8, ruled 2026-10-04).

R-INT-1 (option (b), strict; option 1): ``check_record`` re-verifies every stored act's
detached approval on every check with ``contract.verify_detached_approval(...,
allow_test_authority=False)`` at the caller's ``now``. R-INT-2 (K6 amended): ``EPOCH_CLOSE``
carries the final closure, and a module or port named with two different rows across the epoch
closes of the candidate (with the probe), segment and verify journals is
``CODE_OR_ARTIFACT_DRIFT``. Synthetic records and in-process test keys only.
"""
from __future__ import annotations

import base64
from datetime import timedelta
import json

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from c1_rail.qualification.contract import canonical_json_bytes as canonical
from test_contract import NOW, _approval
from test_t00_screen_state import (
    ACT_SCOPE, FINAL_CLOSURE, OPERATOR, Act, Chain, Seg, act_file, candidate_journal, check,
    epoch_close, hexd, idle_ledger, manifest, modules, sha, simulate, trusted, verified_run)

KEY = ('root-a', 'FULL', 0)
LATE = NOW + timedelta(days=2)  # past _approval's window (2026-09-15T19:00Z, +1 day)


def halted_run(**act_kwargs):
    """A run HALTED from IDLE and resumed by one CONTINUE act: (ledger, journals, m, acts)."""
    m = manifest()
    halted = idle_ledger(m).add('HALT', {'code': 'OVERHEAD_EXHAUSTED', 'from': 'IDLE'})
    act_sha, acts = act_file(sha(canonical(halted.records[-1])), **act_kwargs)
    ledger = halted.add('ACT', {'act_sha256': act_sha, 'act': 'CONTINUE'}).records
    return ledger, {'c1-w0.jsonl': candidate_journal(m)}, m, acts


def signed(private=OPERATOR, **kwargs):
    """An ``act_file`` approval: ``_approval`` over the act bytes under ``ACT_SCOPE``."""
    return lambda raw: _approval(raw, private, **{'scope': ACT_SCOPE, **kwargs})


def flipped(raw):
    """A genuine approval with one signature bit flipped."""
    doc = json.loads(_approval(raw, OPERATOR, scope=ACT_SCOPE))
    value = bytearray(base64.b64decode(doc['signature']['value_b64']))
    value[0] ^= 1
    doc['signature']['value_b64'] = base64.b64encode(bytes(value)).decode('ascii')
    return canonical(doc)


def test_rint1_act_scope_pinned():
    """The act scope check_record verifies under."""
    state, _ = modules()
    # must equal screen_authority.SCREEN_ACT_SCOPE (P-A); switch to import after #672 merges
    assert state.ACT_SCOPE == 'APPROVE_T00_SCREEN_ACT' == ACT_SCOPE


def test_rint1_valid_act_passes():
    """Twin: an OPERATOR approval under the act scope over sha256(act) passes at ``now``."""
    assert check(*halted_run()).code is None


def test_rint1_forged_approval_refused():
    """A key outside ``trusted_keys``, a flipped signature bit, the screen-authority scope or
    an unparseable approval: each is refused."""
    for approval in (signed(Ed25519PrivateKey.generate()), flipped,
                     signed(scope='APPROVE_T00_SCREEN_AUTHORITY'), lambda raw: b'{}'):
        assert check(*halted_run(approval=approval)).code == 'CORRUPTION'


def test_rint1_expired_act_refused():
    """No post-window re-audit (option 1): the act at ``now`` past its window, or before it
    was issued, is refused; inside its window it passes (twin)."""
    run = halted_run()
    assert check(*run).code is None
    assert check(*run, now=LATE).code == 'CORRUPTION'
    assert check(*run, now=NOW - timedelta(days=2)).code == 'CORRUPTION'


def test_rint1_swapped_approval_refused():
    """Another act's genuine approval does not sign this act (subject is sha256(act_bytes))."""
    ledger, journals, m, acts = halted_run()
    ((name, raw),) = acts.items()
    _, other = act_file(hexd('another head'), act='TERMINATE')
    container = {**json.loads(raw), 'approval_b64': json.loads(*other.values())['approval_b64']}
    assert check(ledger, journals, m, {name: canonical(container)}).code == 'CORRUPTION'


def test_rint1_test_only_authority_refused():
    """allow_test_authority is False: a key trusted as TEST_ONLY is refused; the same key
    trusted as OPERATOR passes (twin)."""
    run = halted_run(approval=signed(authority_class='TEST_ONLY'))
    assert check(*run, trusted_keys=trusted(authority_class='TEST_ONLY')).code == 'CORRUPTION'
    assert check(*halted_run(), trusted_keys=trusted(authority_class='OPERATOR')).code is None


def test_rint1_every_stored_act_on_every_check():
    """Every act file is re-verified, also one no ACT record names, and in a full run."""
    ledger, journals, m, acts = halted_run()
    _, stray = act_file(hexd('elsewhere'), approval=signed(Ed25519PrivateKey.generate()))
    assert check(ledger, journals, m, {**acts, **stray}).code == 'CORRUPTION'
    run = simulate([Seg(1, stop=0, end='CRASHED'), Seg(1, stop=0, end='CRASHED'),
                    Seg(1, stop=0, end='CRASHED', cap='RESOURCE_EXHAUSTED'), Act(), Seg(1)])
    assert check(*run).code is None
    assert check(*run, now=LATE).code == 'CORRUPTION'


def test_rint1_keywords_required():
    """``trusted_keys`` and ``now`` are keyword-only and required; ``now`` is timezone-aware."""
    state, _ = modules()
    ledger, journals, m, acts = halted_run()
    with pytest.raises(TypeError):
        state.check_record(ledger, journals, m, acts, keys=())  # pylint: disable=missing-kwoa
    with pytest.raises(ValueError):
        state.check_record(ledger, journals, m, acts, keys=(), trusted_keys=trusted(),
                           now=NOW.replace(tzinfo=None))


def with_closures(run, closures):
    """``run`` with every EPOCH_CLOSE closure of each named journal replaced, re-chained."""
    ledger, journals, m, acts = run
    changed = dict(journals)
    for name, value in closures.items():
        changed[name] = Chain([{**r, 'body': {**r['body'], 'closure': value}}
                               if r['type'] == 'EPOCH_CLOSE' else r
                               for r in journals[name]]).records
    return ledger, changed, m, acts


def closure(**families):
    """FINAL_CLOSURE with ``families`` replaced."""
    return {**FINAL_CLOSURE, **families}


def test_rint2_same_rows_pass():
    """Twin: the same rows in every epoch close of the candidate, segment and verify journals."""
    assert check(*verified_run([KEY], [KEY])).code is None


@pytest.mark.parametrize('journal_name', ['c1-w0.jsonl', 's1-w1.jsonl', 'v1-w0.jsonl'])
def test_rint2_different_row_is_drift(journal_name):
    """A module or port with another row in one covered journal's closes is TERMINAL
    CODE_OR_ARTIFACT_DRIFT: another digest, path or family (stdlib included)."""
    run = verified_run([KEY], [KEY])
    changes = (
        closure(first_party={'ops.a': {'path': 'ops/a.py', 'sha256': hexd('other')}}),
        closure(third_party={'numpy': {'path': 'numpy/other.py', 'sha256': hexd('numpy')}}),
        closure(ports={'ports/p.py': hexd('other port')}),
        closure(first_party={}, third_party={**FINAL_CLOSURE['third_party'],
                                             **FINAL_CLOSURE['first_party']}),
        closure(third_party={}, stdlib=['json', 'numpy']),
    )
    for changed in changes:
        assert check(*with_closures(run, {journal_name: changed})).code == \
            'CODE_OR_ARTIFACT_DRIFT', changed


def test_rint2_disjoint_lazy_sets_pass():
    """Final closures may otherwise differ: disjoint lazy imports per journal pass."""
    lazy = {
        'c1-w0.jsonl': closure(third_party={'scipy': {'path': 'scipy/__init__.py',
                                                      'sha256': hexd('scipy')}}),
        's1-w0.jsonl': closure(first_party={**FINAL_CLOSURE['first_party'],
                                            'ops.b': {'path': 'ops/b.py', 'sha256': hexd('b')}},
                               stdlib=['csv', 'json']),
        'v1-w0.jsonl': {'first_party': {}, 'third_party': {}, 'ports': {}, 'stdlib': []},
    }
    assert check(*with_closures(verified_run([KEY], [KEY]), lazy)).code is None


def test_rint2_old_schema_epoch_close_refused(tmp_path):
    """An EPOCH_CLOSE without ``closure``, or with a malformed one, is a schema error: refused
    on validate and read, and CORRUPTION in check_record."""
    _, journal = modules()
    old = {'integrity': {'cpu_s': 1.0, 'wall_s': 1.0}, 'closure_match': True}
    bad = [old, {**old, 'closure': {}}, {**old, 'closure': closure(stdlib=['json', 'json'])},
           {**old, 'closure': closure(ports={'ports/p.py': 'nothex'})},
           {**old, 'closure': closure(first_party={'ops.a': {'path': 'ops/a.py'}})},
           {**old, 'closure': {**FINAL_CLOSURE, 'extra': []}}]
    for body in bad:
        with pytest.raises(journal.JournalCorrupt):
            journal.validate_body('EPOCH_CLOSE', body)
    journal.validate_body('EPOCH_CLOSE', epoch_close())  # twin
    path = tmp_path / 'journal' / 's1-w0.jsonl'
    path.parent.mkdir()
    path.write_bytes(canonical({'body': old, 'prev_sha256': None, 'type': 'EPOCH_CLOSE'}) + b'\n')
    with pytest.raises(journal.JournalCorrupt):
        journal.read(path, prev_sha256=None)
    ledger, journals, m, acts = verified_run([KEY], [KEY])
    stale = Chain([{**r, 'body': old} if r['type'] == 'EPOCH_CLOSE' else r
                   for r in journals['s1-w0.jsonl']]).records
    assert check(ledger, {**journals, 's1-w0.jsonl': stale}, m, acts).code == 'CORRUPTION'
