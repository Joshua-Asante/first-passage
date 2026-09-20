"""Canonical disposable role memberships and owned-tree bindings, shared by setup, probes and cleanup."""
import hashlib
import json
from types import MappingProxyType

ROLE_GROUPS = MappingProxyType({'qclient': (), 'qexec': ('docker',), 'qg5': ('qclient',)})
ROLES = tuple(ROLE_GROUPS)

# Top-level owned trees in creation order: (owner role, group role, mode). The
# administrator is uid/gid 0 and is never a provisioned role or identity resource.
# Changing a binding is a new schema version; cleanup of manifests retained under
# the previous version then needs that version's table, never today's defaults.
TREE_BINDINGS_SCHEMA = 'qualification_tree_bindings/v1'
ADMINISTRATOR = 'administrator'
TREE_BINDINGS = MappingProxyType({
    'code': (ADMINISTRATOR, ADMINISTRATOR, 0o755),
    'env': (ADMINISTRATOR, ADMINISTRATOR, 0o755),
    'data': ('qexec', 'qexec', 0o700),
    'keys': (ADMINISTRATOR, ADMINISTRATOR, 0o755),
    'scratch': ('qexec', 'qexec', 0o700),
})
TREES = tuple(TREE_BINDINGS)
# Records written before tree bindings (host.py 1339604..9680ed2) retained only the
# UID. That producer owned each tree by these roles and ran chown(uid, uid), so the
# group is known to have equalled the owner; its mkdir(mode) was umask-dependent, so
# the mode is not known and is never synthesized.
LEGACY_TREE_OWNERS = MappingProxyType({'code': ADMINISTRATOR, 'env': ADMINISTRATOR, 'data': 'qexec',
                                       'keys': ADMINISTRATOR, 'scratch': 'qexec'})


def owned_group_members(name):
    return frozenset(role for role,groups in ROLE_GROUPS.items() if name in groups)


def principal(role, roles):
    return 0 if role == ADMINISTRATOR else roles[role]


def resolve_tree_binding(name, roles):
    """The retained record shape: numeric owner and group, 12-bit mode as four octal digits."""
    owner, group, mode = TREE_BINDINGS[name]
    return {'uid': principal(owner, roles), 'gid': principal(group, roles), 'mode': format(mode, '04o')}


def resolve_legacy_tree_owner(name, roles):
    return principal(LEGACY_TREE_OWNERS[name], roles)


def tree_bindings_identity():
    """Retained with the manifest so validation and creation refer to one configuration."""
    table = {name: [owner, group, format(mode, '04o')] for name, (owner, group, mode) in TREE_BINDINGS.items()}
    digest = hashlib.sha256(json.dumps(table, sort_keys=True).encode()).hexdigest()
    return {'schema': TREE_BINDINGS_SCHEMA, 'sha256': digest}
