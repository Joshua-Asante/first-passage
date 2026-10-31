"""Leave the retired qualification suite out of whole-suite runs.

The c1 rail is retired (rail ADR addendum 2026-10-29). Unfiltered
ancestor-directory runs skip the qualification package and its provenance file;
explicit selections still collect them normally.
"""
from pathlib import Path


_QUALIFICATION = Path(__file__).resolve().parent / "qualification"
_PROVENANCE = Path(__file__).resolve().parent / "test_phase3_provenance_acceptance.py"


def _isolate_qualification(config):
    options = config.option
    # Focused runs retain normal collection, including alias failures.
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
    # Explicitly requested qualification runs as ordinary tests.
    if any(path == _QUALIFICATION or path.is_relative_to(_QUALIFICATION)
           for path in selections):
        return False
    return any(path.is_dir() and _QUALIFICATION.is_relative_to(path)
               for path in selections)


def pytest_ignore_collect(collection_path, config):
    if _isolate_qualification(config) and collection_path.resolve() in (_QUALIFICATION, _PROVENANCE):
        return True
    return None

