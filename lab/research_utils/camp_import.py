"""Load a camp-local sibling module under ``--import-mode=importlib``.

Hyphenated camp dirs are not valid packages; shared basenames like
``construct_lib`` must be loaded from *this* camp's file, not a cached
copy from another camp.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def load_camp_sibling(modname: str, file: str) -> ModuleType:
    """Import ``<camp>/<modname>.py`` bound to a unique ``sys.modules`` key."""
    here = Path(file).resolve().parent
    path = here / f"{modname}.py"
    if not path.is_file():
        raise FileNotFoundError(path)
    # Unique key avoids colliding with another camp's same basename.
    key = f"_camp_{here.name}__{modname}"
    existing = sys.modules.get(key)
    if existing is not None:
        return existing
    spec = importlib.util.spec_from_file_location(key, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[key] = module
    # Also publish under the bare name so in-module relative expectations work.
    sys.modules[modname] = module
    spec.loader.exec_module(module)
    return module
