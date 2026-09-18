"""Installation configuration is a closed administrator-owned binding."""
import pytest
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution.release import parse_instance


def instance():
    return dict(schema='qualification_execution_instance/v1', authority_class='TEST_ONLY',
        installation_root='/opt/qualification/installation', data_root='/var/lib/qualification',
        daemon_data_root='/var/lib/qualification', socket_path='/run/qualification/service.sock',
        socket_gid=31000, client_uid=31001, service_uid=31002, g5_uid=31003, operator_uid=0,
        execution_credential='/etc/qualification/execution/key.json')


@pytest.mark.parametrize('name,value', [('service_uid', 0), ('g5_uid', 31002), ('socket_gid', True),
                                      ('installation_root', 'relative'), ('command', 'sh')])
def test_instance_rejects_unsafe_or_unknown_bindings(name, value):
    doc = instance()
    doc[name] = value
    with pytest.raises(ValueError):
        parse_instance(encoded(doc))
