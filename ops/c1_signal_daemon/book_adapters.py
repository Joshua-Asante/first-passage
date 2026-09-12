"""Registry + loader for the four private fixed-book adapters (Track B TB-A1..A4).

The adapter bodies are private ports (ops/c1_signal_daemon/ports/, gitignored on the
operator's primary checkout; they import daemon modules, so they live inside ops/). This tracked module carries only what is
public: the leg ids, the module names, the pinned Pine digests they port, the
per-symbol instrument constants, and a loader that imports a port by path.

Set ``FP_PORT_ROOT`` to point at a different port root (e.g. from a worktree
at the primary checkout's ports). Missing ports are reported, never faked.
"""
from __future__ import annotations

import hashlib
import importlib.util
import os
import sys
from dataclasses import dataclass
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PORT_ROOT = _REPO_ROOT / "ops" / "c1_signal_daemon" / "ports"


@dataclass(frozen=True)
class AdapterSpec:
    leg_id: str
    module: str
    symbol: str
    pine_sha256: str
    mintick: float
    pointvalue: float
    pine_slippage_ticks: int
    pine_commission_per_side: float   # the pinned Pine's literal (the capture may differ)


ADAPTERS: tuple[AdapterSpec, ...] = (
    AdapterSpec("aegis_6j", "aegis_6j", "6J",
                "db78ecba95ae78aca14501a5eaccfda2a42164d83cac12321cb7f293a9adca7c",
                mintick=5e-7, pointvalue=12_500_000.0, pine_slippage_ticks=1,
                pine_commission_per_side=1.30),
    AdapterSpec("dj30_mym_p250", "dj30_mym_p250", "MYM",
                "712cf395396568ce22ae43f1f15b085eaba23acf1b85502abb92129f277fffd7",
                mintick=1.0, pointvalue=0.5, pine_slippage_ticks=1,
                pine_commission_per_side=0.91),
    AdapterSpec("vanguard_mgc", "vanguard_mgc", "MGC",
                "af26899ca94bb0e9ee26d09e0176b6b94bba2f5da252399ce4d899fe7e3bad15",
                mintick=0.1, pointvalue=10.0, pine_slippage_ticks=3,
                pine_commission_per_side=1.06),
    AdapterSpec("orb_mnq_v7", "orb_mnq_v7", "MNQ",
                "176c4f70c67d58053c4d3b8170d0a9be3733bc6b76b1e2f928bd7a877be052a3",
                mintick=0.25, pointvalue=2.0, pine_slippage_ticks=1,
                pine_commission_per_side=0.91),
)
ADAPTER_BY_LEG: dict[str, AdapterSpec] = {a.leg_id: a for a in ADAPTERS}

# Digest of the private ``effective_inputs.json`` (reconstructed 2026-09-03 capture
# inputs; docs/notes/2026-09-11-track-b-adapters-and-book-rules.md). The loader
# refuses any other bytes; re-pin only with a recorded reason.
EFFECTIVE_INPUTS_SHA256 = "66406dee955fa69f237fde60eacdd24259a08d5320352d98e59889acaa18158d"


def port_root() -> Path:
    override = os.environ.get("FP_PORT_ROOT")
    return Path(override) if override else DEFAULT_PORT_ROOT


def port_path(leg_id: str) -> Path:
    return port_root() / f"{ADAPTER_BY_LEG[leg_id].module}.py"


def port_available(leg_id: str) -> bool:
    return port_path(leg_id).is_file()


def port_sha256(leg_id: str) -> str:
    return hashlib.sha256(port_path(leg_id).read_bytes()).hexdigest()


def load_port(leg_id: str):
    """Import the private port module by path; raises FileNotFoundError when absent."""
    spec_row = ADAPTER_BY_LEG[leg_id]
    path = port_path(leg_id)
    if not path.is_file():
        raise FileNotFoundError(f"private port for {leg_id!r} not found at {path}")
    for p in (str(_REPO_ROOT / "ops"), str(_REPO_ROOT / "core")):
        if p not in sys.path:
            sys.path.insert(0, p)
    spec = importlib.util.spec_from_file_location(f"fp_port_{spec_row.module}", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module   # dataclasses resolve annotations via sys.modules
    spec.loader.exec_module(module)
    if getattr(module, "LEG_ID", None) != leg_id:
        raise ValueError(f"port {path} declares LEG_ID {getattr(module, 'LEG_ID', None)!r}, "
                         f"expected {leg_id!r}")
    if getattr(module, "PINE_SHA256", None) != spec_row.pine_sha256:
        raise ValueError(f"port {path} declares PINE_SHA256 {getattr(module, 'PINE_SHA256', None)!r}, "
                         f"expected {spec_row.pine_sha256!r}")
    return module
