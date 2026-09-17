"""Keep signed qualification inventories separate from legacy import aliases.

Unfiltered ancestor-directory runs execute qualification in one clean child.
Explicit qualification selections retain ordinary pytest collection and behavior.
"""
from pathlib import Path


_QUALIFICATION = Path(__file__).resolve().parent / "qualification"
_PROVENANCE = Path(__file__).resolve().parent / "test_phase3_provenance_acceptance.py"
_BRIDGE = Path(__file__).resolve().parent / "test_qualification_isolation.py"


def _isolate_qualification(config):
    options = config.option
    # A filter could deselect the bridge after suppressing qualification tests.
    # Focused runs therefore retain normal collection, including alias failures.
    if any(getattr(options, name, None) for name in (
            "keyword", "markexpr", "deselect", "ignore", "ignore_glob",
            "lf", "ff", "stepwise", "pyargs")):
        return False
    selections = []
    for argument in config.args:
        if "::" in str(argument):
            return False
        path = Path(argument)
        if not path.is_absolute():
            path = Path(config.invocation_params.dir) / path
        selections.append(path.resolve())
    # Do not substitute a child when qualification was explicitly requested.
    if any(path == _QUALIFICATION or path.is_relative_to(_QUALIFICATION)
           for path in selections):
        return False
    return any(path.is_dir() and _QUALIFICATION.is_relative_to(path)
               for path in selections)


def pytest_ignore_collect(collection_path, config):
    if _isolate_qualification(config) and collection_path.resolve() in (_QUALIFICATION, _PROVENANCE):
        return True
    return None


def pytest_collection_modifyitems(config, items):
    if not _isolate_qualification(config):
        # The bridge is a replacement only for whole-suite collection, not an
        # extra skipped test on explicitly selected qualification/legacy runs.
        items[:] = [item for item in items if Path(item.path).resolve() != _BRIDGE]
