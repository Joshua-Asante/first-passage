"""Canonical disposable role memberships, shared by setup, probes and cleanup."""
from types import MappingProxyType

ROLE_GROUPS = MappingProxyType({'qclient': (), 'qexec': ('docker',), 'qg5': ('qclient',)})
ROLES = tuple(ROLE_GROUPS)


def owned_group_members(name):
    return frozenset(role for role,groups in ROLE_GROUPS.items() if name in groups)
