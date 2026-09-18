"""Private credentials are outside wire objects and require protected ownership."""
import importlib
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

import pytest
from c1_rail.qualification.contract import canonical_json_bytes as encoded


def test_credential_reader_rejects_wrong_schema_before_signing(tmp_path):
    credentials = importlib.import_module('c1_rail.qualification.execution.credentials')
    if sys.platform != 'linux':
        with pytest.raises(RuntimeError, match='Linux'):
            credentials.load_credential(str(tmp_path / 'key.json'))
        return
    # /tmp is world-writable, so it cannot exercise validation after custody checks.
    with TemporaryDirectory(prefix='qualification-credential-', dir=Path.home()) as directory:
        path = Path(directory) / 'key.json'
        path.write_bytes(encoded({
            'schema': 'wrong_schema/v1',
            'key_id': 'test-key',
            'authority_class': 'TEST_ONLY',
            'private_seed_b64': 'not-used-before-schema-validation',
        }))
        path.chmod(0o400)
        with pytest.raises(ValueError, match='credential schema differs'):
            credentials.load_credential(str(path))
