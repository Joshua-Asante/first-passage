"""Give each qualification test the canonical import view of a clean process.

Legacy ops tests import package children such as ``c1_rail.c1_rail_listener``
whose source binds flat aliases (``from c1_rail_telemetry import ...``). Python
records each child as an attribute of its package, and the runtime inventory
inspects package attributes, so an explicit mixed selection pulls the child into
every signed closure, where the collector correctly refuses the flat alias.
Directory runs avoid this with a clean child process (``tests/ops/conftest.py``).
Here the package attributes of such children are detached for each test and
restored afterwards; ``sys.modules`` and the inventory check are unchanged.
"""
from pathlib import Path
import sys
from types import FunctionType, ModuleType

import pytest

from c1_rail.qualification.runtime_inventory import REPOSITORY_ROOT, _module_name


_TESTS = REPOSITORY_ROOT / 'tests'
_CANONICAL = {}  # origin -> canonical module name, '' if none, None outside scope


def _canonical_name(raw):
    if raw not in _CANONICAL:
        try:
            path = Path(raw).resolve()
        except OSError:
            path = None
        if path is None or not path.is_relative_to(REPOSITORY_ROOT) or path.is_relative_to(_TESTS):
            _CANONICAL[raw] = None
        else:
            try:
                _CANONICAL[raw] = _module_name(path.relative_to(REPOSITORY_ROOT))
            except ValueError:
                _CANONICAL[raw] = ''
    return _CANONICAL[raw]


def _flat_alias_children():
    """Return canonical package children whose loaded objects reach a flat alias."""
    loaded = {}
    for name, module in tuple(sys.modules.items()):
        raw = getattr(module, '__file__', None) if type(module) is ModuleType else None
        canonical = _canonical_name(raw) if isinstance(raw, str) and raw else None
        if canonical is not None:
            loaded[name] = (module, canonical == name)
    tainted = {name for name, (_, canonical) in loaded.items() if not canonical}
    if not tainted:
        return []
    grew = True
    while grew:
        grew = False
        for name, (module, _) in loaded.items():
            if name in tainted:
                continue
            for key, value in tuple(vars(module).items()):
                if type(value) is ModuleType:
                    # A package's own child attribute is the edge being detached.
                    if value.__name__ == name + '.' + key:
                        continue
                    dependency = value.__name__
                elif isinstance(value, (FunctionType, type)):
                    dependency = getattr(value, '__module__', None)
                else:
                    continue
                if dependency in tainted:
                    tainted.add(name)
                    grew = True
                    break
    return [(sys.modules[parent], child, loaded[name][0])
            for name in sorted(tainted) if loaded[name][1] and '.' in name
            for parent, _, child in [name.rpartition('.')] if parent in sys.modules
            and vars(sys.modules[parent]).get(child) is loaded[name][0]]


@pytest.fixture(autouse=True)
def _canonical_package_view():
    detached = _flat_alias_children()
    for package, child, _ in detached:
        delattr(package, child)
    yield
    for package, child, module in detached:
        setattr(package, child, module)
