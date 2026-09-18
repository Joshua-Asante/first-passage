"""Protected Linux credential loading, shared only by the two signing processes."""
import os
from pathlib import Path
import stat
import sys

from ..contract import parse_canonical_json
from .files import read_regular
from .protocol import decode_base64, fields, identity


def load_credential(reference):
    if sys.platform != 'linux':
        raise RuntimeError('protected signing requires Linux ownership')
    path = Path(reference)
    if not path.is_absolute():
        raise ValueError('absolute protected credential reference required')
    info = path.lstat()
    if (info.st_uid != os.geteuid() or stat.S_IMODE(info.st_mode) != 0o400
            or not stat.S_ISREG(info.st_mode) or info.st_nlink != 1):
        raise ValueError('private credential ownership or mode differs')
    for parent in path.parents:
        owner = parent.lstat()
        if not stat.S_ISDIR(owner.st_mode) or owner.st_uid not in (0, os.geteuid()) or owner.st_mode & 0o022:
            raise ValueError('credential ancestor is not protected')
    doc = fields(parse_canonical_json(read_regular(path.parent, path.name, limit=4096), label='credential'),
                 {'schema', 'key_id', 'authority_class', 'private_seed_b64'})
    if doc['schema'] != 'qualification_private_credential/v1' or doc['authority_class'] not in ('TEST_ONLY', 'OPERATOR'):
        raise ValueError('credential schema differs')
    identity(doc['key_id'])
    seed = decode_base64(doc['private_seed_b64'])
    if len(seed) != 32:
        raise ValueError('Ed25519 private seed length differs')
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    return doc['key_id'], doc['authority_class'], Ed25519PrivateKey.from_private_bytes(seed)
