"""Independent validation regressions; fabricated fixtures are not execution proof."""
from pathlib import Path
from types import SimpleNamespace
import pytest
import test_trust_domain as domains
from c1_rail.qualification import model
from c1_rail.qualification.result_adjudication import _verify_retained_executable_modules

@pytest.mark.parametrize('alias', [False, True])
@pytest.mark.parametrize('entry', ['generic', 'production'])
def test_operator_rejects_shared_result_seal_authority(alias, entry):
    from dataclasses import replace
    doc, policy, private, keys = domains.operator_case()
    keys.pop('seal')
    doc['trusted_key_sha256'].pop('seal')
    doc['seal_key_ids'] = ['alias' if alias else 'test']
    if alias:
        keys['alias'] = replace(keys['test'], key_id='alias')
        doc['trusted_key_sha256']['alias'] = doc['trusted_key_sha256']['test']
    with pytest.raises(ValueError, match='distinct|separat'):
        if entry == 'generic':
            domains.validate(doc, policy, private, keys)
        else:
            domains.production_trust_domain(*domains.signed(doc, private), keys, now=domains.NOW)

class Override:
    def __init__(self, value): self.value = value
    def __get__(self, obj, owner=None): return self.value
    def __set__(self, obj, value): raise RuntimeError('read only')

@pytest.mark.parametrize('name,value', [
    ('status', 'PASS'), ('sessions_to_pass', 1), ('failure_reason', None),
    ('diagnostics', ()), ('unexpected', 'injected'),
])
def test_model_verifier_rejects_injected_data_descriptor(monkeypatch, name, value):
    failed = model.PathOutcome('FAILURE', None, 'failed', ())
    monkeypatch.setattr(model.PathOutcome, name, Override(value), raising=False)
    assert getattr(failed, name) == value
    assert vars(failed)['status'] == 'FAILURE'
    with pytest.raises(ValueError):
        _verify_retained_executable_modules(
            {model.__name__: SimpleNamespace(source_bytes=Path(model.__file__).read_bytes())},
            {model.__name__}, set())

def test_unmodified_model_verifies():
    _verify_retained_executable_modules(
        {model.__name__: SimpleNamespace(source_bytes=Path(model.__file__).read_bytes())},
        {model.__name__}, set())

@pytest.mark.parametrize('when',['before_seal','after_validation'])
def test_committed_pass_cannot_seal_after_void(monkeypatch,when):
    import test_seal as t
    from c1_rail.qualification.attempt import AttemptStore
    original=t.seal_e1_pass
    commit=AttemptStore._commit_e1_seal
    if when=='after_validation':
        def invalidate_at_commit(self,*args,**kwargs):
            self.void('evidence invalidated',now=t.NOW)
            return commit(self,*args,**kwargs)
    def invalidate_then_seal(*args,**kwargs):
        store=kwargs['attempt_store']
        if store.result('TB_E1') is not None:
            if when=='after_validation':
                monkeypatch.setattr(AttemptStore,'_commit_e1_seal',invalidate_at_commit)
            if when=='before_seal':store.void('evidence invalidated',now=t.NOW)
            with pytest.raises(t.ResultValidationError,match='VOID|valid'):
                original(*args,**kwargs)
            # End the existing positive scenario after checking actual rejection.
            raise Stopped
        return original(*args,**kwargs)
    class Stopped(Exception): pass
    monkeypatch.setattr(t,'seal_e1_pass',invalidate_then_seal)
    with pytest.raises(Stopped):
        t.test_complete_exact_pass_authenticates_and_seals_without_authority_grants()


@pytest.mark.parametrize('kind',['seed','panel'])
def test_complete_g5_rejects_coherently_substituted_evidence(monkeypatch,kind):
    import test_seal as t
    from c1_rail.qualification.orchestration import panel_identity
    if kind=='seed':
        original=t.checkpoint_seed_input
        def substitute(*args):
            row=original(*args)
            row.update(root_rng_namespace='foreign',stage='n3',seed=row['seed']+1,
                       source_session_ids_sha256='0'*64)
            return row
        monkeypatch.setattr(t,'checkpoint_seed_input',substitute)
    else:
        original=t.panel_record
        def substitute(frozen,index):
            row=original(frozen,index)
            row['source_session_ids'][0]='foreign-session'
            row['panel_id']=panel_identity(frozen,SimpleNamespace(
                index=index,source_session_ids=tuple(row['source_session_ids'])))
            return row
        monkeypatch.setattr(t,'panel_record',substitute)
    with pytest.raises(t.ResultValidationError,match='seed|panel source'):
        t.validate(t.result_case())


def test_slot_descriptor_replacement_is_detected(monkeypatch):
    import c1_rail.qualification.attempt as module
    claim=module.StageClaim('a','b','c','d',1,'e','FAILURE')
    monkeypatch.setattr(module.StageClaim,'state',Override('PASS'))
    assert claim.state=='PASS'
    with pytest.raises(ValueError):
        _verify_retained_executable_modules(
            {module.__name__:SimpleNamespace(source_bytes=Path(module.__file__).read_bytes())},
            {module.__name__},set())
