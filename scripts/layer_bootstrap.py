"""Shared direct-script bootstrap for repository layer roots."""

from __future__ import annotations

import sys
from pathlib import Path


def add_layer_roots(*layers: str) -> Path:
    """Add requested repository layer roots to ``sys.path`` and return repo root."""
    repo_root = Path(__file__).resolve().parent.parent
    supported_layers = {"core", "lab", "ops"}
    unknown_layers = set(layers) - supported_layers
    if unknown_layers:
        unknown = ", ".join(sorted(unknown_layers))
        raise ValueError(f"unknown repository layer(s): {unknown}")

    paths = (repo_root, *(repo_root / layer for layer in layers))
    for path in reversed(paths):
        path_text = str(path)
        if path_text not in sys.path:
            sys.path.insert(0, path_text)
    return repo_root
