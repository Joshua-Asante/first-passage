"""Fail-closed validation for immutable Phase 3 qualification contracts.

This module verifies externally produced bytes and signatures.  It deliberately
contains no signing or freeze operation.
"""

from __future__ import annotations

import base64
import hashlib
import json
import math
from dataclasses import dataclass, fields, is_dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from types import MappingProxyType
from typing import Any, Mapping
import weakref


from ..ed25519_verify import is_strong_public_key, verify as verify_ed25519


SCHEMA = "frozen_qualification_contract/v1"
APPROVAL_SCHEMA = "qualification_approval/v1"
APPROVAL_PAYLOAD_SCHEMA = "qualification_approval_payload/v1"
FREEZE_SCOPE = "FREEZE_F1"
HISTORICAL_EFFECTIVE_INPUTS = "66406dee955fa69f237fde60eacdd24259a08d5320352d98e59889acaa18158d"

ACCEPTED_HISTORICAL_PINS: Mapping[str, str] = MappingProxyType({
    "step6_admission_contract": "4f027af56f18c119c18b24f6f867ecb0a64188085ea7a8a95c18b0a77d0e9dde",
    "step6_independent_review": "dd9c5e7296535a934b973df7ec0ff8b87c6c3554fc092822820f633588654cfd",
    "step6_accepted_run": "8ddf727b38b3044ad2c0e8cb05330933f94b9fb8c9f21be38dbeff41d7ad75e0",
    "step3_admission_contract": "acfa7920fe025443dd321057f4e1c192d8bc7ccbabd66c94bb25bef6233b6e6d",
    "step3_evidence_index": "95ac6dcb18c37a2e5809c567cd1795f86fc324b21690b45108501505f06e7538",
    "step3_independent_acceptance": "ebcb2efb73042d2e86f46db146246a6a84ff04230b37a47f77d5951994c14f1e",
    "aegis_runtime_port": "11763740bc3fdcc8b9e94cb0b465823aec202cd8333379c46878185db5e9e84f",
    "striker_runtime_port": "efd479b6b4c7eeaa7d8df3f40f36593f87d96b9d5f512dc79c4dd9b0520211f4",
    "vanguard_runtime_port": "e6a03d04c65a19e7fde71103560a229630c3663f445676f06622feec4e9157a3",
    "orb_runtime_port": "b1f4e573009e62b976013e08e7ef2784497d840f490f04e3878fdaef553f317d",
    "historical_effective_inputs": HISTORICAL_EFFECTIVE_INPUTS,
})

REQUIRED_LEGS = frozenset({"aegis_6j", "dj30_mym_p250", "vanguard_mgc", "orb_mnq_v7"})
REQUIRED_STATES = frozenset({
    "AUTHORIZED/NORMAL", "AUTHORIZED/PROTECTED", "WATCH-1", "WATCH-2", "RETIRED"
})
REQUIRED_COVERAGE_WITNESSES = frozenset({
    "allocation", "confirmed_base", "refusal", "risk", "schedule", "stop", "zero",
})
REQUIRED_CLOCKS: Mapping[str, str] = MappingProxyType({
    "source": "immutable_source_metadata",
    "path": "strict_monotonic_unique_path_time",
    "deployment": "ratified_forward_calendar",
})
REQUIRED_QUALIFICATION_ROLES = frozenset({
    "calendar_producer", "cost_model", "coverage_map", "effective_settings_successor",
    "effective_settings_successor_review", "listener_account_owner", "part_a_runner",
    "path_sampler", "population_index", "qualification_adjudicator",
    "qualification_runner", "replay_kernel", "rng_allocation", "runtime_distribution",
    "qualification_adjudication_rules", "qualification_model",
    "qualification_certification_power",
    "schedule_execution_evidence", "schedule_execution_evidence_review",
    "shared_manifest", "source_calendar", "source_calendar_review",
    "source_startup_policy",
})
REQUIRED_ARTIFACT_ROLES = frozenset(ACCEPTED_HISTORICAL_PINS) | REQUIRED_QUALIFICATION_ROLES


class ContractValidationError(ValueError):
    """The proposed frozen contract or approval is not admissible."""


@dataclass(frozen=True)
class EvaluationState:
    state_class: str
    original_basis: Decimal
    current_equity: Decimal
    historical_eod_peak: Decimal
    prior_trade_days: int
    prior_max_day_profit: Decimal


@dataclass(frozen=True)
class StageSpec:
    name: str
    outcome_bearing: bool
    included_in_e1_seal: bool
    population_counts: Mapping[str, tuple[int, ...]]
    exact_depth: int
    max_failures_per_population: int | None
    rng_namespace: str


@dataclass(frozen=True)
class PartASpec:
    initial_panels: int
    expanded_panels: int
    paths_per_population_per_panel: int
    expansion_center_p5: Decimal
    expansion_tolerance: Decimal
    expansion_rule: str
    percentile: Decimal
    percentile_method: str
    sanity_rule: str
    rng_namespace: str

    def should_expand(self, p5: Decimal) -> bool:
        """Return the frozen inclusive expansion decision."""
        if not isinstance(p5, Decimal) or not p5.is_finite():
            raise ContractValidationError("Part A p5 must be a finite Decimal")
        return abs(p5 - self.expansion_center_p5) <= self.expansion_tolerance

    def sanity_passes(self, p5: Decimal, n2_full_point_pass_rate: Decimal) -> bool:
        """Apply the frozen p5 <= n2 FULL point-pass sanity rule."""
        if (not isinstance(p5, Decimal) or not p5.is_finite()
                or not isinstance(n2_full_point_pass_rate, Decimal)
                or not n2_full_point_pass_rate.is_finite()):
            raise ContractValidationError("Part A sanity inputs must be finite Decimals")
        return p5 <= n2_full_point_pass_rate


@dataclass(frozen=True)
class BudgetSpec:
    identity_sha256: str
    maximum_cpu_seconds: int
    maximum_wall_seconds: int
    maximum_memory_bytes: int
    n1_paths: int
    n2_paths: int
    part_a_initial_paths: int
    part_a_expanded_paths: int
    n3_paths: int


@dataclass(frozen=True)
class DecisionRuleSpec:
    failure_ceiling: Decimal
    alpha: Decimal
    speed_target: Decimal
    speed_horizon_sessions: int


@dataclass(frozen=True)
class ReplayConfiguration:
    horizon_sessions: int
    speed_horizon_sessions: int
    inner_block_sessions: int
    outer_months: int
    root_rng_namespace: str
    stages: Mapping[str, StageSpec]
    part_a: PartASpec
    budget: BudgetSpec
    decision_rules: DecisionRuleSpec


@dataclass(frozen=True)
class ArtifactRecord:
    role: str
    path: str
    sha256: str
    producer: str
    authority_class: str


@dataclass(frozen=True)
class TrustedApprovalKey:
    key_id: str
    public_key: bytes
    authority_class: str
    revoked_at: datetime | None = None


@dataclass(frozen=True)
class ApprovalRecord:
    key_id: str
    scope: str
    subject_sha256: str
    contract_sha256: str
    issued_at: datetime
    expires_at: datetime
    authority_class: str
    approval_sha256: str


@dataclass(frozen=True)
class ObservedBindings:
    artifact_sha256: Mapping[str, str]
    runtime_load_sha256: Mapping[str, str]
    effective_settings_sha256: str
    orb_normal_base: int


@dataclass(frozen=True)
class ValidatedFrozenContract:
    contract_id: str
    contract_sha256: str
    canonical_bytes: bytes
    artifacts: tuple[ArtifactRecord, ...]
    runtime_load_sha256: Mapping[str, str]
    populations: Mapping[str, tuple[str, ...]]
    replay: ReplayConfiguration
    initial_state: EvaluationState
    effective_settings_sha256: str
    required_output_roles: tuple[str, ...]
    permitted_optional_output_roles: tuple[str, ...]
    adjudicator_sha256: str
    approval: ApprovalRecord
    trust_domain: object
    trust_domain_sha256: str

    @property
    def stage_specs(self) -> Mapping[str, StageSpec]:
        """Exact frozen stage inventory used by result-envelope validation."""
        return self.replay.stages


_ISSUED_CONTRACTS: dict[int, tuple[weakref.ReferenceType, object]] = {}


def _receipt_snapshot(value: Any) -> Any:
    """Deep immutable snapshot for same-object receipt mutation detection."""
    if is_dataclass(value) and not isinstance(value, type):
        return (type(value).__module__, type(value).__qualname__,
                tuple((field.name, _receipt_snapshot(getattr(value, field.name)))
                      for field in fields(value)))
    if isinstance(value, Mapping):
        return ("mapping", tuple(sorted((str(key), _receipt_snapshot(item))
                                        for key, item in value.items())))
    if isinstance(value, tuple):
        return ("tuple", tuple(_receipt_snapshot(item) for item in value))
    if isinstance(value, list):
        return ("list", tuple(_receipt_snapshot(item) for item in value))
    if isinstance(value, Decimal):
        return ("Decimal", str(value))
    if isinstance(value, datetime):
        return ("datetime", value.astimezone(timezone.utc).isoformat())
    if isinstance(value, bytes):
        return ("bytes", hashlib.sha256(value).hexdigest(), len(value))
    if value is None:
        return ("none",)
    if type(value) in (str, int, bool):
        return (type(value).__name__, value)
    raise TypeError(f"unsupported validated contract receipt field: {type(value).__name__}")


def require_validated_frozen_contract(contract: Any) -> ValidatedFrozenContract:
    """Require the exact unchanged receipt issued by ``validate_frozen_contract``."""
    issued = _ISSUED_CONTRACTS.get(id(contract))
    if (type(contract) is not ValidatedFrozenContract or issued is None
            or issued[0]() is not contract):
        raise ContractValidationError("validator-issued frozen contract required")
    from .trust_domain import require_validated_trust_domain
    domain = require_validated_trust_domain(contract.trust_domain)
    if (contract.trust_domain_sha256 != domain.sha256
            or issued[1] != _receipt_snapshot(contract)):
        raise ContractValidationError("validated frozen contract fields changed")
    return contract


def canonical_json_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ContractValidationError(f"value cannot be encoded as canonical JSON: {exc}") from exc


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ContractValidationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise ContractValidationError(f"non-finite JSON constant is forbidden: {value}")


def parse_canonical_json(data: bytes, *, label: str) -> Any:
    if data.startswith(b"\xef\xbb\xbf"):
        raise ContractValidationError(f"{label} must be UTF-8 without BOM")
    try:
        text = data.decode("utf-8", errors="strict")
        value = json.loads(text, object_pairs_hook=_unique_object, parse_constant=_reject_constant)
    except ContractValidationError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractValidationError(f"invalid UTF-8 JSON for {label}: {exc}") from exc
    if canonical_json_bytes(value) != data:
        raise ContractValidationError(f"{label} bytes are not canonical JSON")
    return value


def _fields(value: Any, required: set[str], *, label: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise ContractValidationError(f"{label} must be an object")
    actual = set(value)
    if actual != required:
        raise ContractValidationError(
            f"{label} fields differ: missing={sorted(required - actual)}, extra={sorted(actual - required)}"
        )
    return value


def _text(value: Any, *, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ContractValidationError(f"{label} must be a non-empty string")
    return value


def _sha256(value: Any, *, label: str) -> str:
    text = _text(value, label=label)
    if len(text) != 64 or any(ch not in "0123456789abcdef" for ch in text):
        raise ContractValidationError(f"{label} must be a lowercase SHA-256 hex digest")
    return text


def _positive_int(value: Any, *, label: str, allow_zero: bool = False) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ContractValidationError(f"{label} must be an integer")
    minimum = 0 if allow_zero else 1
    if value < minimum:
        raise ContractValidationError(f"{label} must be >= {minimum}")
    return value


def _boolean(value: Any, *, label: str) -> bool:
    if not isinstance(value, bool):
        raise ContractValidationError(f"{label} must be a boolean")
    return value


def _decimal(value: Any, *, label: str) -> Decimal:
    if not isinstance(value, str):
        raise ContractValidationError(f"{label} must be a decimal string")
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise ContractValidationError(f"{label} is not a decimal") from exc
    if not result.is_finite():
        raise ContractValidationError(f"{label} must be finite")
    return result


def _instant(value: Any, *, label: str) -> datetime:
    text = _text(value, label=label)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContractValidationError(f"{label} must be an ISO-8601 instant") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ContractValidationError(f"{label} must be timezone-aware")
    return parsed.astimezone(timezone.utc)


def verify_detached_approval(
    approval_bytes: bytes,
    *,
    trusted_keys: Mapping[str, TrustedApprovalKey],
    expected_scope: str,
    expected_subject_sha256: str,
    expected_contract_sha256: str,
    now: datetime,
    allow_test_authority: bool = False,
) -> ApprovalRecord:
    outer = _fields(
        parse_canonical_json(approval_bytes, label="approval"),
        {"schema", "payload", "signature"}, label="approval",
    )
    if outer["schema"] != APPROVAL_SCHEMA:
        raise ContractValidationError("unsupported approval schema")
    payload = _fields(outer["payload"], {
        "schema", "scope", "subject_sha256", "contract_sha256", "issued_at",
        "expires_at", "authority_class",
    }, label="approval payload")
    signature = _fields(outer["signature"], {"algorithm", "key_id", "value_b64"}, label="approval signature")
    if payload["schema"] != APPROVAL_PAYLOAD_SCHEMA:
        raise ContractValidationError("unsupported approval payload schema")
    if payload["scope"] != expected_scope:
        raise ContractValidationError("approval scope does not match")
    if payload["subject_sha256"] != expected_subject_sha256 or payload["contract_sha256"] != expected_contract_sha256:
        raise ContractValidationError("approval subject/contract digest does not match")
    if signature["algorithm"] != "Ed25519":
        raise ContractValidationError("approval algorithm must be Ed25519")
    key_id = _text(signature["key_id"], label="approval key_id")
    key = trusted_keys.get(key_id)
    if key is None or key.key_id != key_id:
        raise ContractValidationError("approval key is not trusted")
    if payload["authority_class"] != key.authority_class:
        raise ContractValidationError("approval authority class does not match trusted key")
    if key.authority_class == "TEST_ONLY" and not allow_test_authority:
        raise ContractValidationError("TEST_ONLY approval authority is forbidden at this boundary")
    if key.authority_class != "OPERATOR" and not (allow_test_authority and key.authority_class == "TEST_ONLY"):
        raise ContractValidationError("approval authority is not authorized for this scope")
    issued_at = _instant(payload["issued_at"], label="approval issued_at")
    expires_at = _instant(payload["expires_at"], label="approval expires_at")
    if now.tzinfo is None or now.utcoffset() is None:
        raise ContractValidationError("approval verification time must be timezone-aware")
    now_utc = now.astimezone(timezone.utc)
    if not issued_at <= now_utc < expires_at:
        raise ContractValidationError("approval is not valid at verification time")
    if key.revoked_at is not None:
        if key.revoked_at.tzinfo is None or key.revoked_at.utcoffset() is None:
            raise ContractValidationError("approval key revocation time must be timezone-aware")
        if key.revoked_at.astimezone(timezone.utc) <= now_utc:
            raise ContractValidationError("approval key is revoked")
    try:
        encoded = signature["value_b64"]
        if not isinstance(encoded, str):
            raise ValueError("not a string")
        signature_bytes = base64.b64decode(encoded, validate=True)
        if base64.b64encode(signature_bytes).decode("ascii") != encoded:
            raise ValueError("non-canonical base64")
    except ValueError as exc:
        raise ContractValidationError("approval signature is invalid") from exc
    if not is_strong_public_key(key.public_key):
        raise ContractValidationError("approval key is not a strong Ed25519 public key")
    if not verify_ed25519(key.public_key, canonical_json_bytes(dict(payload)), signature_bytes):
        raise ContractValidationError("approval signature is invalid")
    return ApprovalRecord(
        key_id=key_id, scope=payload["scope"], subject_sha256=payload["subject_sha256"],
        contract_sha256=payload["contract_sha256"], issued_at=issued_at,
        expires_at=expires_at, authority_class=payload["authority_class"],
        approval_sha256=hashlib.sha256(approval_bytes).hexdigest(),
    )


def validate_frozen_contract(
    contract_bytes: bytes,
    freeze_approval_bytes: bytes,
    trusted_keys: Mapping[str, TrustedApprovalKey],
    observed: ObservedBindings,
    *,
    now: datetime,
    trust_domain: object | None = None,
) -> ValidatedFrozenContract:
    """Validate retained bytes and return immutable runner inputs.

    The signed, validator-issued trust domain is the sole authority selector.
    """
    if type(contract_bytes) is not bytes or type(freeze_approval_bytes) is not bytes:
        raise ContractValidationError("contract and approval require immutable bytes")
    doc = _fields(parse_canonical_json(contract_bytes, label="contract"), {
        "schema", "contract_id", "artifacts", "dependencies", "runtime_load_trace",
        "role_owners", "clocks", "populations", "coverage", "historical_pins",
        "effective_settings", "replay", "initial_state", "authority",
        "approval_policy", "result_plan",
        "trust_domain_sha256",
    }, label="contract")
    if doc["schema"] != SCHEMA:
        raise ContractValidationError("unsupported frozen contract schema")
    contract_id = _text(doc["contract_id"], label="contract_id")
    domain = None
    if trust_domain is not None:
        try:
            from .trust_domain import require_validated_trust_domain
            domain = require_validated_trust_domain(trust_domain)
        except Exception as exc:
            raise ContractValidationError(f"trust domain is not validator-issued: {exc}") from exc
    expected_artifact_authority = (
        "TEST_ONLY" if domain is not None and domain.authority_class == "TEST_ONLY"
        else "PRODUCTION_REVIEWED"
    )

    if not isinstance(doc["artifacts"], list) or not doc["artifacts"]:
        raise ContractValidationError("artifacts must be a non-empty list")
    artifacts: list[ArtifactRecord] = []
    roles: set[str] = set()
    paths: set[str] = set()
    for index, raw in enumerate(doc["artifacts"]):
        row = _fields(raw, {"role", "path", "sha256", "producer", "authority_class"}, label=f"artifact[{index}]")
        role = _text(row["role"], label="artifact role")
        path = _text(row["path"], label="artifact path")
        if role in roles or path in paths:
            raise ContractValidationError("artifact roles and paths must be unique")
        if row["authority_class"] != expected_artifact_authority:
            raise ContractValidationError("artifact authority differs from the signed trust domain")
        roles.add(role); paths.add(path)
        artifacts.append(ArtifactRecord(role, path, _sha256(row["sha256"], label="artifact sha256"),
                                        _text(row["producer"], label="artifact producer"), row["authority_class"]))
    expected_artifacts = {row.path: row.sha256 for row in artifacts}
    if dict(observed.artifact_sha256) != expected_artifacts:
        raise ContractValidationError("observed artifact inventory is not an exact closed-world match")
    if not REQUIRED_ARTIFACT_ROLES.issubset(roles):
        raise ContractValidationError(
            "artifact inventory lacks required historical/qualification semantic roles")
    if domain is not None and roles != set(domain.required_artifact_roles):
        raise ContractValidationError("artifact role inventory differs from the signed trust domain")
    artifacts_by_role = {row.role: row for row in artifacts}
    accepted_historical = (dict(domain.accepted_historical_pins) if domain is not None
                           else dict(ACCEPTED_HISTORICAL_PINS))
    for role, accepted_sha256 in accepted_historical.items():
        if artifacts_by_role[role].sha256 != accepted_sha256:
            raise ContractValidationError(
                f"historical role {role} does not bind its accepted Phase 1 identity")
    if domain is not None:
        if doc["historical_pins"] != dict(domain.accepted_historical_pins):
            raise ContractValidationError("historical pins differ from the signed trust domain")
        for role, accepted_sha256 in domain.accepted_historical_pins.items():
            if artifacts_by_role.get(role) is None or artifacts_by_role[role].sha256 != accepted_sha256:
                raise ContractValidationError("trust-domain historical artifact identity differs")

    owners: dict[str, str] = {}
    if not isinstance(doc["role_owners"], list):
        raise ContractValidationError("role_owners must be a list")
    for raw in doc["role_owners"]:
        row = _fields(raw, {"role", "owner"}, label="role owner")
        role = _text(row["role"], label="owned role")
        if role in owners:
            raise ContractValidationError("role ownership must be unique")
        owners[role] = _text(row["owner"], label="owner")
    if set(owners) != roles or any(owners[item.role] != item.producer for item in artifacts):
        raise ContractValidationError("role ownership must cover artifacts and equal their producers")

    if not isinstance(doc["dependencies"], list):
        raise ContractValidationError("dependencies must be a list")
    dependency_consumers: set[str] = set()
    graph: dict[str, tuple[str, ...]] = {}
    for raw in doc["dependencies"]:
        row = _fields(raw, {"consumer_role", "requires_roles"}, label="dependency")
        consumer = _text(row["consumer_role"], label="dependency consumer")
        required = row["requires_roles"]
        if consumer in dependency_consumers or consumer not in roles or not isinstance(required, list):
            raise ContractValidationError("dependency closure has duplicate/unknown consumer")
        if any(not isinstance(role, str) or role not in roles for role in required):
            raise ContractValidationError("dependency closure references an unknown role")
        if len(set(required)) != len(required) or consumer in required:
            raise ContractValidationError("dependency closure contains duplicate/self reference")
        dependency_consumers.add(consumer); graph[consumer] = tuple(required)
    if dependency_consumers != roles:
        raise ContractValidationError("dependency closure must enumerate every artifact role")
    visiting: set[str] = set(); visited: set[str] = set()
    def visit(role: str) -> None:
        if role in visiting:
            raise ContractValidationError("dependency graph contains a cycle")
        if role in visited:
            return
        visiting.add(role)
        for child in graph[role]: visit(child)
        visiting.remove(role); visited.add(role)
    for role in roles: visit(role)
    runner_reachable: set[str] = set()
    def collect_runner_dependencies(role: str) -> None:
        for child in graph[role]:
            if child not in runner_reachable:
                runner_reachable.add(child)
                collect_runner_dependencies(child)
    collect_runner_dependencies("qualification_runner")
    if runner_reachable != roles - {"qualification_runner"}:
        raise ContractValidationError(
            "qualification runner must reach every frozen artifact role")

    runtime: dict[str, str] = {}
    if not isinstance(doc["runtime_load_trace"], list):
        raise ContractValidationError("runtime_load_trace must be a list")
    for raw in doc["runtime_load_trace"]:
        row = _fields(raw, {"role", "sha256"}, label="runtime load")
        role = _text(row["role"], label="runtime role")
        if role in runtime or role not in roles:
            raise ContractValidationError("runtime load roles must be unique artifact roles")
        runtime[role] = _sha256(row["sha256"], label="runtime load sha256")
    if set(runtime) != roles or dict(observed.runtime_load_sha256) != runtime:
        raise ContractValidationError("observed runtime load trace is not an exact match")
    artifact_by_role = {item.role: item.sha256 for item in artifacts}
    if runtime != artifact_by_role:
        raise ContractValidationError("runtime load trace does not equal frozen artifact identities")

    clocks = _fields(doc["clocks"], {"source", "path", "deployment"}, label="clocks")
    clock_values = [_text(clocks[name], label=f"{name} clock") for name in ("source", "path", "deployment")]
    if len(set(clock_values)) != 3 or dict(clocks) != dict(REQUIRED_CLOCKS):
        raise ContractValidationError("source, path and deployment clock identities/semantics must be separate and exact")

    populations = _fields(doc["populations"], {"FULL", "H1", "H2"}, label="populations")
    normalized_populations: dict[str, tuple[str, ...]] = {}
    for name in ("FULL", "H1", "H2"):
        values = populations[name]
        if not isinstance(values, list) or not values or any(not isinstance(v, str) or not v for v in values):
            raise ContractValidationError(f"population {name} must contain session identities")
        if len(values) != len(set(values)):
            raise ContractValidationError(f"population {name} contains duplicate sessions")
        normalized_populations[name] = tuple(values)
    full = normalized_populations["FULL"]; h1 = normalized_populations["H1"]; h2 = normalized_populations["H2"]
    split = math.ceil(len(full) / 2)
    if h1 != full[:split] or h2 != full[split:] or set(h1) & set(h2):
        raise ContractValidationError("H1/H2 are not the exact ordered ceil partition of FULL")

    coverage = _fields(doc["coverage"], {"legs", "states", "matrix"}, label="coverage")
    if not isinstance(coverage["legs"], list) or set(coverage["legs"]) != REQUIRED_LEGS or len(coverage["legs"]) != 4:
        raise ContractValidationError("coverage must contain each required leg exactly once")
    if not isinstance(coverage["states"], list) or set(coverage["states"]) != REQUIRED_STATES or len(coverage["states"]) != len(REQUIRED_STATES):
        raise ContractValidationError("coverage must contain each required state exactly once")
    matrix = coverage["matrix"]
    if not isinstance(matrix, list):
        raise ContractValidationError("coverage matrix must be a list")
    observed_cells: set[tuple[str, str]] = set()
    for raw in matrix:
        cell = _fields(raw, {"leg", "state", "witnesses"}, label="coverage cell")
        identity = (cell["leg"], cell["state"])
        if identity in observed_cells or identity[0] not in REQUIRED_LEGS or identity[1] not in REQUIRED_STATES:
            raise ContractValidationError("coverage matrix has a duplicate or unknown cell")
        witnesses = cell["witnesses"]
        if (not isinstance(witnesses, list) or witnesses != sorted(REQUIRED_COVERAGE_WITNESSES)):
            raise ContractValidationError("coverage cell lacks exact risk/stop/allocation/base/schedule/zero/refusal witnesses")
        observed_cells.add(identity)
    expected_cells = {(leg_id, state) for leg_id in REQUIRED_LEGS for state in REQUIRED_STATES}
    if observed_cells != expected_cells:
        raise ContractValidationError("coverage matrix is incomplete")

    pins = _fields(doc["historical_pins"], set(accepted_historical), label="historical pins")
    if dict(pins) != accepted_historical:
        raise ContractValidationError("historical pins do not exactly match accepted Phase 1 identities")

    settings = _fields(doc["effective_settings"], {"settings_sha256", "reviewed", "orb_normal_base"}, label="effective settings")
    settings_sha = _sha256(settings["settings_sha256"], label="settings_sha256")
    if settings["reviewed"] is not True:
        raise ContractValidationError("effective settings require an explicit reviewed binding")
    if settings_sha == HISTORICAL_EFFECTIVE_INPUTS:
        raise ContractValidationError("historical effective-input bytes carry ORB qty=2; a reviewed successor is required")
    if domain is not None and settings_sha != domain.effective_settings_sha256:
        raise ContractValidationError("effective settings differ from the signed trust domain")
    if settings["orb_normal_base"] != 1 or observed.orb_normal_base != 1:
        raise ContractValidationError("ORB settings do not match fixed normal base 1")
    if observed.effective_settings_sha256 != settings_sha:
        raise ContractValidationError("observed effective settings identity does not match")
    if artifacts_by_role["effective_settings_successor"].sha256 != settings_sha:
        raise ContractValidationError(
            "reviewed effective settings successor is not bound into artifact inventory")

    replay_raw = _fields(doc["replay"], {
        "horizon_sessions", "speed_horizon_sessions", "inner_block_sessions", "outer_months",
        "root_rng_namespace", "stages", "part_a", "budget", "decision_rules",
    }, label="replay")
    stage_rows = replay_raw["stages"]
    if not isinstance(stage_rows, list):
        raise ContractValidationError("replay stages must be a list")
    stage_specs: dict[str, StageSpec] = {}
    for raw in stage_rows:
        row = _fields(raw, {
            "name", "outcome_bearing", "included_in_e1_seal", "population_counts",
            "exact_depth", "max_failures_per_population", "rng_namespace",
        }, label="stage spec")
        name = _text(row["name"], label="stage name")
        if name in stage_specs:
            raise ContractValidationError("stage names must be unique")
        counts_raw = row["population_counts"]
        if not isinstance(counts_raw, dict):
            raise ContractValidationError("stage population_counts must be an object")
        counts: dict[str, tuple[int, ...]] = {}
        for population, allowed in counts_raw.items():
            if population not in {"FULL", "H1", "H2", "REGIME"} or not isinstance(allowed, list) or not allowed:
                raise ContractValidationError("stage population/count is invalid")
            normalized = tuple(_positive_int(value, label="stage population count") for value in allowed)
            if tuple(sorted(set(normalized))) != normalized:
                raise ContractValidationError("stage population counts must be unique and sorted")
            counts[population] = normalized
        failure_cap = row["max_failures_per_population"]
        if failure_cap is not None:
            failure_cap = _positive_int(failure_cap, label="stage max_failures_per_population", allow_zero=True)
        stage_specs[name] = StageSpec(
            name=name,
            outcome_bearing=_boolean(row["outcome_bearing"], label="stage outcome_bearing"),
            included_in_e1_seal=_boolean(row["included_in_e1_seal"], label="stage included_in_e1_seal"),
            population_counts=MappingProxyType(counts),
            exact_depth=_positive_int(row["exact_depth"], label="stage exact_depth"),
            max_failures_per_population=failure_cap,
            rng_namespace=_text(row["rng_namespace"], label="stage rng_namespace"),
        )
    stage_order = ("LEGALITY", "N1", "N2", "PART_B", "PART_A", "N3")
    if tuple(stage_specs) != stage_order:
        raise ContractValidationError("stage specs do not contain the exact qualification stages")
    legality, n1, n2, part_b, part_a_stage, n3 = (stage_specs[name] for name in stage_order)
    if (dict(legality.population_counts) != {} or legality.exact_depth != 1
            or legality.rng_namespace != "legality"):
        raise ContractValidationError("LEGALITY stage shape differs")
    if (set(n1.population_counts) != {"FULL", "H1", "H2"}
            or any(values != (n1.exact_depth,) for values in n1.population_counts.values())
            or n1.rng_namespace != "n1"):
        raise ContractValidationError("N1 populations must use the signed frozen depth")
    if (dict(n2.population_counts) != {"FULL": (n2.exact_depth,)}
            or n2.rng_namespace != "n2"):
        raise ContractValidationError("N2 FULL must use the signed frozen depth")
    if (dict(part_b.population_counts) != {"H1": (n2.exact_depth,), "H2": (n2.exact_depth,)}
            or part_b.exact_depth != n2.exact_depth or part_b.rng_namespace != "n2"):
        raise ContractValidationError("PART_B must alias the same N2 depth and RNG namespace")
    expected_part_a_panels = ((100, 200) if domain is None else
                              domain.workload_policy.stage_population_depths["PART_A"]["REGIME"])
    if (dict(part_a_stage.population_counts) != {"REGIME": expected_part_a_panels}
            or part_a_stage.rng_namespace != "part_a"):
        raise ContractValidationError("PART_A panel inventory differs")
    if (set(n3.population_counts) != {"FULL", "H1", "H2"}
            or any(values != (n3.exact_depth,) for values in n3.population_counts.values())
            or n3.rng_namespace != "n3" or n3.included_in_e1_seal):
        raise ContractValidationError("N3 must have an independently frozen disjoint depth/namespace")
    if any(not stage.outcome_bearing for stage in stage_specs.values()) or any(
            not stage.included_in_e1_seal for name, stage in stage_specs.items() if name != "N3"):
        raise ContractValidationError("stage outcome/seal roles differ")

    rules_raw = _fields(replay_raw["decision_rules"], {
        "failure_ceiling", "alpha", "speed_target", "speed_horizon_sessions",
    }, label="decision rules")
    decision_rules = DecisionRuleSpec(
        _decimal(rules_raw["failure_ceiling"], label="failure ceiling"),
        _decimal(rules_raw["alpha"], label="decision alpha"),
        _decimal(rules_raw["speed_target"], label="speed target"),
        _positive_int(rules_raw["speed_horizon_sessions"], label="speed horizon sessions"),
    )
    if any(not Decimal(0) < value < Decimal(1) for value in (
            decision_rules.failure_ceiling, decision_rules.alpha, decision_rules.speed_target)):
        raise ContractValidationError("decision probabilities must be inside (0,1)")
    expected_n1_cutoff = int(Decimal(n1.exact_depth) * decision_rules.failure_ceiling)
    if n1.max_failures_per_population != expected_n1_cutoff:
        raise ContractValidationError("N1 cutoff does not match the reviewed certification calculator")

    part_a_raw = _fields(replay_raw["part_a"], {
        "initial_panels", "expanded_panels", "paths_per_population_per_panel",
        "expansion_center_p5", "expansion_tolerance", "expansion_rule", "percentile",
        "percentile_method", "sanity_rule", "rng_namespace",
    }, label="Part A")
    part_a = PartASpec(
        initial_panels=_positive_int(part_a_raw["initial_panels"], label="Part A initial_panels"),
        expanded_panels=_positive_int(part_a_raw["expanded_panels"], label="Part A expanded_panels"),
        paths_per_population_per_panel=_positive_int(
            part_a_raw["paths_per_population_per_panel"], label="Part A paths_per_population_per_panel"),
        expansion_center_p5=_decimal(part_a_raw["expansion_center_p5"], label="Part A expansion_center_p5"),
        expansion_tolerance=_decimal(part_a_raw["expansion_tolerance"], label="Part A expansion_tolerance"),
        expansion_rule=_text(part_a_raw["expansion_rule"], label="Part A expansion_rule"),
        percentile=_decimal(part_a_raw["percentile"], label="Part A percentile"),
        percentile_method=_text(part_a_raw["percentile_method"], label="Part A percentile_method"),
        sanity_rule=_text(part_a_raw["sanity_rule"], label="Part A sanity_rule"),
        rng_namespace=_text(part_a_raw["rng_namespace"], label="Part A rng_namespace"),
    )
    expected_initial_panels = (100 if domain is None
                               else domain.workload_policy.part_a_initial_panels)
    expected_expanded_panels = (200 if domain is None
                                else domain.workload_policy.part_a_expanded_panels)
    if part_a != PartASpec(
        expected_initial_panels, expected_expanded_panels, part_a_stage.exact_depth,
        Decimal("0.95"), Decimal("0.01"),
        "ABS_P5_MINUS_CENTER_LTE_TOLERANCE", Decimal("0.05"),
        "INVERSE_ECDF_LEFT", "P5_LTE_N2_FULL_POINT_PASS_RATE", "part_a",
    ):
        raise ContractValidationError(
            "Part A must freeze exact 100/200 panels, inclusive abs(p5-.95)<=.01 expansion, "
            "inverse-ECDF p5, and p5<=FULL sanity"
        )

    budget_raw = _fields(replay_raw["budget"], {
        "identity_sha256", "maximum_cpu_seconds", "maximum_wall_seconds", "maximum_memory_bytes",
        "n1_paths", "n2_paths", "part_a_initial_paths", "part_a_expanded_paths", "n3_paths",
    }, label="budget")
    budget = BudgetSpec(
        identity_sha256=_sha256(budget_raw["identity_sha256"], label="budget identity_sha256"),
        maximum_cpu_seconds=_positive_int(budget_raw["maximum_cpu_seconds"], label="budget maximum_cpu_seconds"),
        maximum_wall_seconds=_positive_int(budget_raw["maximum_wall_seconds"], label="budget maximum_wall_seconds"),
        maximum_memory_bytes=_positive_int(budget_raw["maximum_memory_bytes"], label="budget maximum_memory_bytes"),
        n1_paths=_positive_int(budget_raw["n1_paths"], label="budget n1_paths"),
        n2_paths=_positive_int(budget_raw["n2_paths"], label="budget n2_paths"),
        part_a_initial_paths=_positive_int(budget_raw["part_a_initial_paths"], label="budget part_a_initial_paths"),
        part_a_expanded_paths=_positive_int(budget_raw["part_a_expanded_paths"], label="budget part_a_expanded_paths"),
        n3_paths=_positive_int(budget_raw["n3_paths"], label="budget n3_paths"),
    )
    expected_budget_counts = (
        3 * n1.exact_depth, 3 * n2.exact_depth,
        part_a.initial_panels * part_a_stage.exact_depth,
        part_a.expanded_panels * part_a_stage.exact_depth,
        3 * n3.exact_depth,
    )
    if (budget.n1_paths, budget.n2_paths, budget.part_a_initial_paths,
            budget.part_a_expanded_paths, budget.n3_paths) != expected_budget_counts:
        raise ContractValidationError("budget path counts do not derive from signed stage depths")
    replay = ReplayConfiguration(
        horizon_sessions=_positive_int(replay_raw["horizon_sessions"], label="horizon_sessions"),
        speed_horizon_sessions=_positive_int(replay_raw["speed_horizon_sessions"], label="speed_horizon_sessions"),
        inner_block_sessions=_positive_int(replay_raw["inner_block_sessions"], label="inner_block_sessions"),
        outer_months=_positive_int(replay_raw["outer_months"], label="outer_months"),
        root_rng_namespace=_text(replay_raw["root_rng_namespace"], label="root_rng_namespace"),
        stages=MappingProxyType(stage_specs), part_a=part_a, budget=budget,
        decision_rules=decision_rules,
    )
    if replay.speed_horizon_sessions > replay.horizon_sessions:
        raise ContractValidationError("replay speed horizon exceeds full horizon")
    if decision_rules.speed_horizon_sessions != replay.speed_horizon_sessions:
        raise ContractValidationError("decision speed horizon differs from replay speed horizon")
    if replay.horizon_sessions % replay.inner_block_sessions:
        raise ContractValidationError("replay horizon must be divisible by inner block sessions")
    if domain is not None:
        workload = domain.workload_policy
        if (replay.horizon_sessions != workload.horizon_sessions
                or replay.inner_block_sessions != workload.inner_block_sessions
                or replay.outer_months != workload.outer_months
                or replay.part_a.initial_panels != workload.part_a_initial_panels
                or replay.part_a.expanded_panels != workload.part_a_expanded_panels
                or replay.part_a.paths_per_population_per_panel
                    != workload.part_a_paths_per_population_per_panel):
            raise ContractValidationError("replay workload differs from the signed trust domain")
        for stage_name, expected in workload.stage_population_depths.items():
            if dict(stage_specs[stage_name].population_counts) != dict(expected):
                raise ContractValidationError(
                    f"{stage_name} populations differ from the signed trust domain")

    state_raw = _fields(doc["initial_state"], {
        "class", "original_basis", "current_equity", "historical_eod_peak", "prior_trade_days", "prior_max_day_profit",
    }, label="initial_state")
    state = EvaluationState(
        state_class=_text(state_raw["class"], label="initial state class"),
        original_basis=_decimal(state_raw["original_basis"], label="original_basis"),
        current_equity=_decimal(state_raw["current_equity"], label="current_equity"),
        historical_eod_peak=_decimal(state_raw["historical_eod_peak"], label="historical_eod_peak"),
        prior_trade_days=_positive_int(state_raw["prior_trade_days"], label="prior_trade_days", allow_zero=True),
        prior_max_day_profit=_decimal(state_raw["prior_max_day_profit"], label="prior_max_day_profit"),
    )
    if (state.state_class != "PRISTINE" or state.original_basis <= 0
            or state.current_equity != state.original_basis
            or state.historical_eod_peak != state.original_basis
            or state.prior_trade_days != 0 or state.prior_max_day_profit != 0):
        raise ContractValidationError(
            "INITIAL_STATE_ALTERNATIVE_UNSUPPORTED: E1 currently consumes only PRISTINE state; "
            "a non-pristine state requires a separately specified and sealed consuming gate")
    authority = _fields(doc["authority"], {"evidence_class", "permits_synthetic_authority"}, label="authority")
    expected_authority = ({"evidence_class": "TEST_ONLY", "permits_synthetic_authority": True}
                          if domain is not None and domain.authority_class == "TEST_ONLY"
                          else {"evidence_class": "PRODUCTION_REVIEWED",
                                "permits_synthetic_authority": False})
    if authority != expected_authority:
        raise ContractValidationError("contract authority differs from the signed trust domain")

    approval_policy = _fields(doc["approval_policy"], {
        "freeze_scope", "freeze_authority_class", "freeze_key_ids",
    }, label="approval_policy")
    policy_authority = approval_policy["freeze_authority_class"]
    if (approval_policy["freeze_scope"] != FREEZE_SCOPE
            or policy_authority not in {"OPERATOR", "TEST_ONLY"}
            or (domain is not None and policy_authority != domain.authority_class)):
        raise ContractValidationError("freeze approval policy has the wrong scope/authority role")
    enrolled_keys = approval_policy["freeze_key_ids"]
    if (not isinstance(enrolled_keys, list) or not enrolled_keys
            or any(not isinstance(key, str) or not key for key in enrolled_keys)
            or enrolled_keys != sorted(set(enrolled_keys))):
        raise ContractValidationError("freeze approval key enrollment must be a sorted non-empty set")
    if domain is not None and tuple(enrolled_keys) != domain.freeze_key_ids:
        raise ContractValidationError("freeze key enrollment differs from the signed trust domain")

    result_plan = _fields(doc["result_plan"], {
        "required_output_roles", "permitted_optional_output_roles", "adjudicator_role",
        "adjudicator_closure_sha256",
    }, label="result_plan")
    output_sets: list[tuple[str, ...]] = []
    for field in ("required_output_roles", "permitted_optional_output_roles"):
        values = result_plan[field]
        if (not isinstance(values, list) or any(not isinstance(value, str) or not value for value in values)
                or values != sorted(set(values))):
            raise ContractValidationError(f"{field} must be a sorted unique role set")
        output_sets.append(tuple(values))
    required_output_roles, optional_output_roles = output_sets
    if not required_output_roles or set(required_output_roles) & set(optional_output_roles):
        raise ContractValidationError("result output roles must be required and disjoint")
    if result_plan["adjudicator_role"] != "qualification_adjudicator":
        raise ContractValidationError("result plan must bind the qualification adjudicator role")
    if "qualification_adjudicator" not in runtime:
        raise ContractValidationError("closed runtime inventory lacks qualification adjudicator")
    adjudicator_subject = canonical_json_bytes({
        "schema": "qualification-adjudicator-closure/v1",
        "sources": runtime,
    })
    adjudicator_sha256 = hashlib.sha256(adjudicator_subject).hexdigest()
    if _sha256(result_plan["adjudicator_closure_sha256"],
               label="adjudicator closure sha256") != adjudicator_sha256:
        raise ContractValidationError(
            "result plan adjudicator closure does not match the complete runtime inventory")

    if domain is None:
        raise ContractValidationError("validator-issued trust domain is required")
    trust_domain_sha256 = _sha256(doc["trust_domain_sha256"], label="trust_domain_sha256")
    if trust_domain_sha256 != domain.sha256:
        raise ContractValidationError("contract trust-domain identity differs")
    try:
        from .trust_domain import require_trusted_domain_key
        for key_id in enrolled_keys:
            key = trusted_keys.get(key_id)
            if key is None:
                raise ContractValidationError("freeze key is not trusted")
            require_trusted_domain_key(domain, key_id, key.public_key)
    except ContractValidationError:
        raise
    except Exception as exc:
        raise ContractValidationError(f"freeze key differs from the signed trust domain: {exc}") from exc

    contract_sha = hashlib.sha256(contract_bytes).hexdigest()
    approval = verify_detached_approval(
        freeze_approval_bytes, trusted_keys=trusted_keys, expected_scope=FREEZE_SCOPE,
        expected_subject_sha256=contract_sha, expected_contract_sha256=contract_sha,
        now=now, allow_test_authority=domain.authority_class == "TEST_ONLY",
    )
    if approval.key_id not in enrolled_keys or approval.authority_class != approval_policy["freeze_authority_class"]:
        raise ContractValidationError("freeze signature key/role is not enrolled by the contract")
    result = ValidatedFrozenContract(
        contract_id=contract_id, contract_sha256=contract_sha, canonical_bytes=bytes(contract_bytes),
        artifacts=tuple(artifacts), runtime_load_sha256=MappingProxyType(dict(runtime)),
        populations=MappingProxyType(dict(normalized_populations)), replay=replay,
        initial_state=state, effective_settings_sha256=settings_sha,
        required_output_roles=required_output_roles,
        permitted_optional_output_roles=optional_output_roles,
        adjudicator_sha256=adjudicator_sha256,
        approval=approval,
        trust_domain=domain,
        trust_domain_sha256=trust_domain_sha256,
    )
    identity = id(result)
    _ISSUED_CONTRACTS[identity] = (
        weakref.ref(result, lambda ref: _ISSUED_CONTRACTS.pop(identity, None)),
        _receipt_snapshot(result),
    )
    return result


__all__ = [
    "ACCEPTED_HISTORICAL_PINS", "ApprovalRecord", "ArtifactRecord", "BudgetSpec", "DecisionRuleSpec",
    "ContractValidationError", "EvaluationState", "ObservedBindings", "PartASpec",
    "ReplayConfiguration", "REQUIRED_ARTIFACT_ROLES", "StageSpec", "TrustedApprovalKey", "ValidatedFrozenContract",
    "canonical_json_bytes", "parse_canonical_json", "validate_frozen_contract",
    "verify_detached_approval", "require_validated_frozen_contract",
]
