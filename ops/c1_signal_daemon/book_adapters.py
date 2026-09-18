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
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

_REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PORT_ROOT = _REPO_ROOT / "ops" / "c1_signal_daemon" / "ports"


@dataclass(frozen=True)
class AdapterSpec:
    leg_id: str
    module: str
    symbol: str
    pine_sha256: str
    runtime_sha256: str
    mintick: float
    pointvalue: float
    pine_slippage_ticks: int
    pine_commission_per_side: float   # the pinned Pine's literal (the capture may differ)


ADAPTERS: tuple[AdapterSpec, ...] = (
    AdapterSpec("aegis_6j", "aegis_6j", "6J",
                "db78ecba95ae78aca14501a5eaccfda2a42164d83cac12321cb7f293a9adca7c",
                "11763740bc3fdcc8b9e94cb0b465823aec202cd8333379c46878185db5e9e84f",
                mintick=5e-7, pointvalue=12_500_000.0, pine_slippage_ticks=1,
                pine_commission_per_side=1.30),
    AdapterSpec("dj30_mym_p250", "dj30_mym_p250", "MYM",
                "712cf395396568ce22ae43f1f15b085eaba23acf1b85502abb92129f277fffd7",
                # Step 3/Step 6 accepted corrected-ports generation.  The
                # preserved original private port is c81aa59c... and must fail.
                "efd479b6b4c7eeaa7d8df3f40f36593f87d96b9d5f512dc79c4dd9b0520211f4",
                mintick=1.0, pointvalue=0.5, pine_slippage_ticks=1,
                pine_commission_per_side=0.91),
    AdapterSpec("vanguard_mgc", "vanguard_mgc", "MGC",
                "af26899ca94bb0e9ee26d09e0176b6b94bba2f5da252399ce4d899fe7e3bad15",
                "e6a03d04c65a19e7fde71103560a229630c3663f445676f06622feec4e9157a3",
                mintick=0.1, pointvalue=10.0, pine_slippage_ticks=3,
                pine_commission_per_side=1.06),
    AdapterSpec("orb_mnq_v7", "orb_mnq_v7", "MNQ",
                "176c4f70c67d58053c4d3b8170d0a9be3733bc6b76b1e2f928bd7a877be052a3",
                "b1f4e573009e62b976013e08e7ef2784497d840f490f04e3878fdaef553f317d",
                mintick=0.25, pointvalue=2.0, pine_slippage_ticks=1,
                pine_commission_per_side=0.91),
)
ADAPTER_BY_LEG: dict[str, AdapterSpec] = {a.leg_id: a for a in ADAPTERS}

# Digest of the historical private ``effective_inputs.json`` (reconstructed
# 2026-09-03 capture inputs).  These accepted bytes remain immutable provenance.
EFFECTIVE_INPUTS_SHA256 = "66406dee955fa69f237fde60eacdd24259a08d5320352d98e59889acaa18158d"

# Phase-2 runtime successor: preserve every historical input, but bind ORB's
# executable base quantity to the shared fixed-book law before constructing the
# adapter.  The digest is over canonical effective values after that derivation;
# it is deliberately distinct from the historical source-byte identity above.
RUNTIME_EFFECTIVE_INPUTS_SHA256 = "9d4d4e1d622a3fb0ae37b7b20f8bdf960244f9e66b5d88ded79db4de6089dade"


class AdapterRegistry(dict):
    """Adapter mapping carrying the loader receipt checked at runtime bind."""

    def __init__(self, values, *, kind, runtime_identities, effective_inputs_sha256,
                 historical_effective_inputs_sha256=None):
        super().__init__(values)
        self.kind = kind
        self.runtime_identities = dict(runtime_identities)
        self.effective_inputs_sha256 = effective_inputs_sha256
        self.historical_effective_inputs_sha256 = historical_effective_inputs_sha256


def synthetic_adapter_registry(values):
    """Explicitly label test doubles; accepted identities are never implied."""
    return AdapterRegistry(
        values, kind="synthetic",
        runtime_identities={leg_id: type(adapter).__name__
                            for leg_id, adapter in values.items()},
        effective_inputs_sha256="synthetic",
        historical_effective_inputs_sha256="synthetic",
    )


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
    source = path.read_bytes()
    if hashlib.sha256(source).hexdigest() != spec_row.runtime_sha256:
        raise ValueError(f"port {path} does not match the accepted runtime identity")
    for p in (str(_REPO_ROOT / "ops"), str(_REPO_ROOT / "core")):
        if p not in sys.path:
            sys.path.insert(0, p)
    module_name = f"fp_port_{spec_row.module}"
    module = ModuleType(module_name)
    module.__file__ = str(path)
    module.__package__ = ""
    sys.modules[module_name] = module  # dataclasses resolve annotations via sys.modules
    try:
        exec(compile(source, str(path), "exec"), module.__dict__)
    except Exception:
        sys.modules.pop(module_name, None)
        raise
    if getattr(module, "LEG_ID", None) != leg_id:
        raise ValueError(f"port {path} declares LEG_ID {getattr(module, 'LEG_ID', None)!r}, "
                         f"expected {leg_id!r}")
    if getattr(module, "PINE_SHA256", None) != spec_row.pine_sha256:
        raise ValueError(f"port {path} declares PINE_SHA256 {getattr(module, 'PINE_SHA256', None)!r}, "
                         f"expected {spec_row.pine_sha256!r}")
    return module


def load_book_adapters(*, mode=None):
    """Load the four accepted private runtimes and their exact input binding."""
    from c1_signal_daemon.book_protocol import Mode
    mode = Mode.NORMAL if mode is None else Mode(mode)
    inputs_path = port_root() / "effective_inputs.json"
    inputs_bytes = inputs_path.read_bytes()
    if hashlib.sha256(inputs_bytes).hexdigest() != EFFECTIVE_INPUTS_SHA256:
        raise ValueError("effective input bytes do not match the accepted identity")
    values = json.loads(inputs_bytes.decode("utf-8"))
    if set(values) != {"_note"} | set(ADAPTER_BY_LEG):
        raise ValueError("effective input registry is incomplete")
    # The historical ORB chart ran a quantity incompatible with the ratified
    # fixed-book base.  Preserve its source bytes above, then derive the reviewed
    # runtime successor from the shared law rather than editing private history.
    from c1_rail.book_policy import leg
    runtime_values = json.loads(json.dumps(values))
    runtime_values["orb_mnq_v7"]["adapter"]["qty"] = leg(
        "orb_mnq_v7").normal_base_values[0]
    runtime_bytes = json.dumps(
        runtime_values, sort_keys=True, separators=(",", ":"), allow_nan=False,
    ).encode("utf-8")
    if hashlib.sha256(runtime_bytes).hexdigest() != RUNTIME_EFFECTIVE_INPUTS_SHA256:
        raise ValueError("derived runtime input identity does not match the reviewed successor")
    result = {}
    for spec_row in ADAPTERS:
        row = runtime_values[spec_row.leg_id]
        if not isinstance(row, dict) or set(row) != {"adapter", "emulator", "qty_scale"}:
            raise ValueError("effective input row is incomplete")
        module = load_port(spec_row.leg_id)
        result[spec_row.leg_id] = module.build(mode=mode, **row["adapter"])
    return AdapterRegistry(
        result, kind="accepted",
        runtime_identities={
            row.leg_id: {"pine_sha256": row.pine_sha256,
                         "runtime_sha256": row.runtime_sha256}
            for row in ADAPTERS
        },
        effective_inputs_sha256=RUNTIME_EFFECTIVE_INPUTS_SHA256,
        historical_effective_inputs_sha256=EFFECTIVE_INPUTS_SHA256,
    )


@dataclass(frozen=True)
class QualificationAdapterLoad:
    """Fresh adapter objects and immutable trace of the consumed byte inventory."""

    registry: AdapterRegistry
    load_trace: tuple[tuple[str, str, str], ...]


def _unique_settings(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate effective-settings JSON key')
        result[key] = value
    return result


def _qualification_snapshots(contract, retained_bytes):
    """Pure byte verification; this helper does not confer contract authority."""
    expected_paths = {row.path for row in contract.artifacts}
    expected_roles = {row.role for row in contract.artifacts}
    if len(expected_paths) != len(contract.artifacts) or len(expected_roles) != len(contract.artifacts):
        raise ValueError('duplicate qualification artifact paths or roles')
    if set(retained_bytes) != expected_paths or set(contract.runtime_load_sha256) != expected_roles:
        raise ValueError('qualification inventory must be an exact closed-world match')
    normalized = [os.path.normcase(os.path.abspath(row.path)) for row in contract.artifacts]
    if len(set(normalized)) != len(normalized):
        raise ValueError('qualification artifact path aliases are forbidden')
    snapshots, trace = {}, []
    for row in contract.artifacts:
        raw = retained_bytes[row.path]
        if type(raw) is not bytes:
            raise ValueError('immutable retained bytes required')
        digest = hashlib.sha256(raw).hexdigest()
        if digest != row.sha256 or digest != contract.runtime_load_sha256[row.role]:
            raise ValueError('qualification retained/runtime artifact digest mismatch')
        snapshots[row.role] = raw
        trace.append((row.role, row.path, digest))
    raw = snapshots.get('effective_settings_successor')
    if raw is None or hashlib.sha256(raw).hexdigest() != contract.effective_settings_sha256:
        raise ValueError('reviewed effective-settings successor digest missing or mismatched')
    if contract.effective_settings_sha256 == EFFECTIVE_INPUTS_SHA256:
        raise ValueError('historical ORB settings cannot be qualification settings')
    def reject_constant(value):
        raise ValueError('nonfinite effective-settings JSON value')
    values = json.loads(raw.decode('utf-8'), object_pairs_hook=_unique_settings, parse_constant=reject_constant)
    if set(values) != {'_note'} | set(ADAPTER_BY_LEG):
        raise ValueError('effective-settings registry is incomplete')
    for leg in ADAPTER_BY_LEG:
        row = values[leg]
        if not isinstance(row, dict) or set(row) != {'adapter', 'emulator', 'qty_scale'} or not isinstance(row['adapter'], dict):
            raise ValueError('effective-settings row is incomplete')
    qty = values['orb_mnq_v7']['adapter'].get('qty')
    if type(qty) is not int or qty != 1:
        raise ValueError('qualification ORB fixed normal base must be one')
    return snapshots, values, tuple(trace)


def load_qualification_adapters(contract, *, retained_bytes):
    """Load only G1-approved immutable successor settings and accepted ports.

    Historical ``load_book_adapters`` remains unchanged. No file is reopened,
    no pyc is consulted, and every retained byte is verified before execution.
    The caller must obtain the contract through the ordinary G1 verifier.
    """
    domain = _qualification_domain(contract)
    if domain.authority_class != 'OPERATOR' or domain.permits_synthetic:
        raise ValueError('production G1-validated frozen contract required')
    return _load_domain_adapters(contract, retained_bytes=retained_bytes, domain=domain)


def _qualification_domain(contract):
    from c1_rail.qualification.contract import ValidatedFrozenContract, require_validated_frozen_contract
    if type(contract) is not ValidatedFrozenContract:
        raise ValueError('exact G1-validated frozen contract required')
    require_validated_frozen_contract(contract)
    from c1_rail.qualification.trust_domain import QualificationTrustDomain, require_validated_trust_domain
    domain = getattr(contract, 'trust_domain', None)
    if type(domain) is not QualificationTrustDomain or contract.approval.authority_class != domain.authority_class:
        raise ValueError('validated contract trust domain required')
    require_validated_trust_domain(domain)
    if getattr(contract, 'trust_domain_sha256', None) != domain.sha256:
        raise ValueError('contract trust domain digest differs')
    if contract.effective_settings_sha256 != domain.effective_settings_sha256:
        raise ValueError('contract settings differ from trust domain')
    return domain


def _load_composition_adapters(contract, *, retained_bytes):
    """Internal TEST_ONLY composition entry; never exposed by production CLI."""
    domain = _qualification_domain(contract)
    if domain.authority_class != 'TEST_ONLY' or not domain.permits_synthetic:
        raise ValueError('TEST_ONLY composition contract domain required')
    return _load_domain_adapters(contract, retained_bytes=retained_bytes, domain=domain)


def _load_domain_adapters(contract, *, retained_bytes, domain):
    from c1_signal_daemon.book_protocol import Mode
    if _qualification_domain(contract) is not domain:
        raise ValueError('adapter domain differs from exact contract domain')
    if __name__ != 'c1_signal_daemon.book_adapters':
        raise ValueError('qualification adapter module alias is forbidden')
    snapshots, settings, trace = _qualification_snapshots(contract, retained_bytes)
    roles = {'aegis_6j': 'aegis_runtime_port', 'dj30_mym_p250': 'striker_runtime_port',
             'vanguard_mgc': 'vanguard_runtime_port', 'orb_mnq_v7': 'orb_runtime_port'}
    paths = {row.role: row.path for row in contract.artifacts}
    for spec_row in ADAPTERS:
        raw = snapshots.get(roles[spec_row.leg_id])
        if raw is None or hashlib.sha256(raw).hexdigest() != domain.port_runtime_pins[spec_row.leg_id].runtime_sha256:
            raise ValueError('qualification port differs from accepted corrected runtime')
    result = {}
    for spec_row in ADAPTERS:
        role = roles[spec_row.leg_id]
        module_name = f'fp_qualification_port_{spec_row.module}'
        module = ModuleType(module_name)
        module.__file__ = paths[role]
        module.__package__ = ''
        sys.modules[module_name] = module
        try:
            exec(compile(snapshots[role], paths[role], 'exec'), module.__dict__)
            if getattr(module, 'LEG_ID', None) != spec_row.leg_id or getattr(module, 'PINE_SHA256', None) != domain.port_runtime_pins[spec_row.leg_id].pine_sha256:
                raise ValueError('qualification port declared identity mismatch')
            result[spec_row.leg_id] = module.build(mode=Mode.NORMAL, **settings[spec_row.leg_id]['adapter'])
        except Exception:
            sys.modules.pop(module_name, None)
            raise
    registry = AdapterRegistry(result, kind='synthetic' if domain.permits_synthetic else 'accepted',
        runtime_identities={row.leg_id: {'pine_sha256': domain.port_runtime_pins[row.leg_id].pine_sha256,
                                      'runtime_sha256': domain.port_runtime_pins[row.leg_id].runtime_sha256} for row in ADAPTERS},
        effective_inputs_sha256=contract.effective_settings_sha256)
    return QualificationAdapterLoad(registry, trace)
