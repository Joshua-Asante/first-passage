"""Installation configuration is a closed administrator-owned binding."""
import pytest
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution.release import parse_instance


def instance():
    return dict(schema='qualification_execution_instance/v1', authority_class='TEST_ONLY',
        installation_root='/opt/qualification/installation', data_root='/var/lib/qualification',
        daemon_data_root='/var/lib/qualification', socket_path='/run/qualification/service.sock',
        socket_gid=31000, client_uid=31001, service_uid=31002, g5_uid=31003, operator_uid=0,
        execution_credential='/etc/qualification/execution/key.json',host_run_id='a'*32)


@pytest.mark.parametrize('name,value', [('service_uid', 0), ('g5_uid', 31002), ('socket_gid', True),
                                      ('installation_root', 'relative'), ('command', 'sh'),('host_run_id','foreign')])
def test_instance_rejects_unsafe_or_unknown_bindings(name, value):
    doc = instance()
    doc[name] = value
    with pytest.raises(ValueError):
        parse_instance(encoded(doc))


def funded_release(tmp_path, **changes):
    import json
    from bundle_fixture import build_bundle
    from c1_rail.qualification.execution.protocol import sha256
    case = build_bundle(tmp_path / 'staged', capability='FULL_E1', funded=True)
    doc = json.loads(case['release'])
    doc.update(changes)
    if 'profile' in changes:
        doc['profile_sha256'] = sha256(encoded(doc['profile']))
    return doc


def test_executable_diagnostic_release_pairs_funded_profile_without_dispatch(tmp_path):
    from c1_rail.qualification.execution.release_schema import parse_release, EXECUTABLE_DIAGNOSTIC_RELEASE
    from c1_rail.qualification.execution.profile import parse_profile
    from c1_rail.qualification.execution.service import schedule_eligibility
    release = parse_release(encoded(funded_release(tmp_path)))
    assert release['schema'] == EXECUTABLE_DIAGNOSTIC_RELEASE == 'qualification_execution_release/v4'
    assert release['profile']['schema'] == 'qualification_execution_profile/v4'
    assert release['campaign_budget_profile']['schema'] == 'qualification_campaign_budget_profile/v3'
    assert release['capability'] == 'FULL_E1' and release['dispatch_enabled'] is False
    assert release['production_execution'] is False and release['profile']['dispatch_enabled'] is False
    assert schedule_eligibility(release, parse_profile(encoded(release['profile']))) is True


@pytest.mark.parametrize('field,value', [('dispatch_enabled', True), ('production_execution', True),
                                         ('authority_class', 'OPERATOR'), ('capability', 'N1_ONLY')])
def test_executable_diagnostic_release_keeps_every_v3_restriction(tmp_path, field, value):
    from c1_rail.qualification.execution.release_schema import parse_release
    with pytest.raises(ValueError):
        parse_release(encoded(funded_release(tmp_path, **{field: value})))


@pytest.mark.parametrize('older', ['qualification_execution_release/v3', 'qualification_execution_release/v2',
                                   'qualification_execution_release/v1'])
def test_older_release_literals_still_refuse_the_funded_profile(tmp_path, older):
    """release_schema keeps the persistence-only refusal for every literal but v4."""
    from c1_rail.qualification.execution.release_schema import parse_release
    doc = funded_release(tmp_path, schema=older)
    if older.endswith('/v1'):
        doc.update(capability='N1_ONLY'); doc.pop('dispatch_enabled'); doc.pop('campaign_budget_profile')
    elif older.endswith('/v2'):
        doc.pop('campaign_budget_profile')
    with pytest.raises(ValueError, match='persistence-only|unsupported'):
        parse_release(encoded(doc))


def test_executable_release_refuses_unfunded_profile_or_budget_pairing(tmp_path):
    import json
    from bundle_fixture import build_bundle
    from c1_rail.qualification.execution.release_schema import parse_release
    from c1_rail.qualification.execution.profile import diagnostic_execution_profile, diagnostic_budget_profile
    from c1_rail.qualification.execution.service import schedule_eligibility
    from c1_rail.qualification.execution.profile import parse_profile
    doc = funded_release(tmp_path)
    old_profile = diagnostic_execution_profile(encoded(doc['profile']))
    with pytest.raises(ValueError, match='binding differs'):
        parse_release(encoded(funded_release(tmp_path / 'b', profile=old_profile,
                                             campaign_budget_profile=diagnostic_budget_profile(encoded(old_profile)))))
    with pytest.raises(ValueError, match='binding differs'):
        parse_release(encoded(dict(doc, campaign_budget_profile=diagnostic_budget_profile(encoded(old_profile)))))
    v3 = json.loads(build_bundle(tmp_path / 'v3', capability='FULL_E1', diagnostic=True)['release'])
    assert parse_release(encoded(v3))['schema'] == 'qualification_execution_release/v3'
    assert schedule_eligibility(v3, parse_profile(encoded(v3['profile']))) is False

# ---- S3 v5 pinned vectors (C1 GO condition b; extended, never replaced) ------

def dispatch_release(tmp_path, **changes):
    import json
    from bundle_fixture import build_bundle
    case = build_bundle(tmp_path / 'staged', capability='FULL_E1', dispatch=True)
    document = json.loads(case['release'])
    document.update(changes)
    return encoded(document)


def test_dispatch_release_pairs_dispatch_profile_with_closed_n1_checkpoint(tmp_path):
    from c1_rail.qualification.execution.release_schema import (parse_release,
        DISPATCH_DIAGNOSTIC_RELEASE, EXECUTABLE_DIAGNOSTIC_RELEASE)
    release = parse_release(dispatch_release(tmp_path))
    assert release['schema'] == DISPATCH_DIAGNOSTIC_RELEASE == 'qualification_execution_release/v5'
    assert release['profile']['schema'] == 'qualification_execution_profile/v5'
    assert release['dispatch_enabled'] is True and release['dispatch_checkpoints'] == ['N1']
    assert release['campaign_budget_profile']['schema'] == 'qualification_campaign_budget_profile/v3'
    assert release['production_execution'] is False and release['authority_class'] == 'TEST_ONLY'


@pytest.mark.parametrize('field,value', [
    ('production_execution', True), ('authority_class', 'OPERATOR'), ('capability', 'N1_ONLY'),
    ('dispatch_checkpoints', ['N1', 'N2']), ('dispatch_checkpoints', []),
    ('dispatch_enabled', False), ('worker_image_digest', 'not-a-digest')])
def test_dispatch_release_refuses_open_dispatch_facts(tmp_path, field, value):
    from c1_rail.qualification.execution.release_schema import parse_release
    with pytest.raises(ValueError):
        parse_release(dispatch_release(tmp_path, **{field: value}))


def test_v4_with_dispatch_enabled_is_still_refused(tmp_path):
    """D4's refusal is per-literal: a genuine v4 release with dispatch flipped
    on refuses, and the untouched v4 beside it still parses."""
    import json
    from bundle_fixture import build_bundle
    from c1_rail.qualification.execution.release_schema import parse_release
    case = build_bundle(tmp_path / 'staged', capability='FULL_E1', funded=True)
    document = json.loads(case['release'])
    assert document['schema'] == 'qualification_execution_release/v4'
    assert document['dispatch_enabled'] is False
    parse_release(encoded(document))
    flipped = dict(document, dispatch_enabled=True)
    with pytest.raises(ValueError):
        parse_release(encoded(flipped))
    with_checkpoints = dict(document, dispatch_checkpoints=['N1'])
    with pytest.raises(ValueError):
        parse_release(encoded(with_checkpoints))


# ---- S4 v6 joint vectors (D3; beside the v5 pins, never replacing them) ------


def joint_release(tmp_path, **changes):
    import json
    from bundle_fixture import build_bundle
    case = build_bundle(tmp_path / 'staged', capability='FULL_E1', joint=True)
    document = json.loads(case['release'])
    document.update(changes)
    return encoded(document)


def test_joint_release_pairs_v6_profile_with_the_closed_n1_n2_set(tmp_path):
    from c1_rail.qualification.execution.release_schema import (
        JOINT_DISPATCH_DIAGNOSTIC_RELEASE,
        parse_release,
    )

    release = parse_release(joint_release(tmp_path))
    assert (
        release['schema']
        == JOINT_DISPATCH_DIAGNOSTIC_RELEASE
        == 'qualification_execution_release/v6'
    )
    assert release['profile']['schema'] == 'qualification_execution_profile/v6'
    assert release['dispatch_enabled'] is True
    assert release['dispatch_checkpoints'] == ['N1', 'N2']
    assert release['campaign_budget_profile']['schema'] == (
        'qualification_campaign_budget_profile/v3'
    )
    assert release['production_execution'] is False
    from c1_rail.qualification.execution.service import (
        dispatch_eligibility,
        joint_dispatch_eligibility,
        schedule_eligibility,
    )
    from c1_rail.qualification.execution.profile import parse_profile

    profile = parse_profile(encoded(release['profile']))
    assert joint_dispatch_eligibility(release, profile)
    assert dispatch_eligibility(release, profile)
    assert schedule_eligibility(release, profile)
    # The v5 pins beside it keep their closed N1-only set.
    v5 = parse_release(dispatch_release(tmp_path))
    assert v5['dispatch_checkpoints'] == ['N1']
    v5_profile = parse_profile(encoded(v5['profile']))
    assert dispatch_eligibility(v5, v5_profile)
    assert not joint_dispatch_eligibility(v5, v5_profile)


@pytest.mark.parametrize('field,value', [
    ('dispatch_checkpoints', ['N1']), ('dispatch_checkpoints', ['N1', 'N2', 'PART_A']),
    ('dispatch_checkpoints', []), ('dispatch_enabled', False)])
def test_joint_release_refuses_open_dispatch_facts(tmp_path, field, value):
    from c1_rail.qualification.execution.release_schema import parse_release

    with pytest.raises(ValueError):
        parse_release(joint_release(tmp_path, **{field: value}))
