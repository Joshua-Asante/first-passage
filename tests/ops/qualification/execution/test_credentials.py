"""Private credentials are outside wire objects and require protected ownership."""
import importlib
import os

import pytest
from c1_rail.qualification.contract import canonical_json_bytes as encoded


def test_credential_reader_rejects_wrong_schema_before_signing(tmp_path):
    credentials = importlib.import_module('c1_rail.qualification.execution.credentials')
    path = tmp_path / 'key.json'
    path.write_bytes(encoded({'arbitrary_payload': 'not a key'}))
    if os.name == 'posix':
        path.chmod(0o400)
        with pytest.raises(ValueError, match='schema'):
            credentials.load_credential(str(path))
    else:
        with pytest.raises(RuntimeError, match='Linux'):
            credentials.load_credential(str(path))
