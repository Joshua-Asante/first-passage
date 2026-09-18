"""Authenticated qualification result envelopes and external E1 PASS seals."""
from __future__ import annotations

import base64
import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from .contract import (
    TrustedApprovalKey, canonical_json_bytes, parse_canonical_json,
    require_validated_frozen_contract,
)
from .attempt import (
    AttemptStore, StageClaim, ValidatedResultClaim, _issue_validated_result_claim,
    AttemptJournalError,
)
from .preflight import (
    PreflightReceipt, _is_reparse_point, preflight_binding_bytes,
    revalidate_e1_preflight,
)
from .result_adjudication import FrozenAdjudicator
from .trust_domain import require_trusted_domain_key, require_validated_trust_domain
from ..ed25519_verify import is_strong_public_key, verify as verify_ed25519


RESULT_SCHEMA = "qualification_result_envelope/v1"
AUTH_SCHEMA = "qualification_result_authentication/v1"
SEAL_SCHEMA = "e1_qualification_seal/v1"
MANDATORY_E1_STAGES = ("LEGALITY", "N1", "N2", "PART_B", "PART_A")


class ResultValidationError(ValueError):
    """A result, authentication, or proposed seal fails closed."""


@dataclass(frozen=True)
class TrustedResultKey:
    key_id: str
    public_key: bytes
    authority_class: str
    scopes: tuple[str, ...]
    revoked_at: datetime | None = None


@dataclass(frozen=True)
class ValidatedResult:
    attempt_id: str
    contract_sha256: str
    trust_domain_sha256: str
    result_sha256: str
    canonical_bytes: bytes
    completion: str
    verdict: str
    stage_output_sha256: Mapping[str, str]
    output_sha256: Mapping[str, str]
    shared_manifest_sha256: str
    path_inventory_sha256: str
    output_root: str
    output_paths: Mapping[str, str]
    attempt_journal_path: str
    attempt_journal_event_head: str
    attempt_journal_event_count: int
    attempt_reservation_event_digest: str


@dataclass(frozen=True)
class AuthenticatedResult:
    result: ValidatedResult
    authentication_sha256: str
    key_id: str
    canonical_bytes: bytes
    trust_domain_sha256: str


def _validation_provenance_registry():
    issued: dict[int, ValidatedResult] = {}

    def register(result: ValidatedResult) -> ValidatedResult:
        issued[id(result)] = result
        return result

    def require(result: ValidatedResult) -> None:
        if type(result) is not ValidatedResult or issued.get(id(result)) is not result:
            raise ResultValidationError("validator-issued result provenance is required")

    return register, require


_register_validated_result, _require_validated_result = _validation_provenance_registry()


def _revalidate_validated_result(result: ValidatedResult) -> Mapping[str, Any]:
    _require_validated_result(result)
    if hashlib.sha256(result.canonical_bytes).hexdigest() != result.result_sha256:
        raise ResultValidationError("validated result canonical bytes differ")
    try:
        doc = parse_canonical_json(result.canonical_bytes, label="validated result envelope")
    except Exception as exc:
        raise ResultValidationError(str(exc)) from exc
    if (doc.get("attempt_id") != result.attempt_id
            or doc.get("contract_sha256") != result.contract_sha256
            or doc.get("trust_domain_sha256") != result.trust_domain_sha256
            or doc.get("completion") != result.completion
            or doc.get("verdict") != result.verdict
            or doc.get("shared_manifest_sha256") != result.shared_manifest_sha256
            or doc.get("path_inventory_sha256") != result.path_inventory_sha256):
        raise ResultValidationError("validated result receipt fields differ from canonical bytes")
    stages = doc.get("stage_results")
    outputs = doc.get("outputs")
    if (not isinstance(stages, list) or
            {row.get("stage"): row.get("output_sha256") for row in stages
             if isinstance(row, dict)} != dict(result.stage_output_sha256)):
        raise ResultValidationError("validated stage receipt fields differ from canonical bytes")
    if (not isinstance(outputs, list) or
            {row.get("role"): row.get("sha256") for row in outputs
             if isinstance(row, dict)} != dict(result.output_sha256)
            or {row.get("role"): row.get("path") for row in outputs
                if isinstance(row, dict)} != dict(result.output_paths)):
        raise ResultValidationError("validated output receipt fields differ from canonical bytes")
    return doc


def _require_attempt_store_binding(
    result: ValidatedResult, attempt_store: AttemptStore, *, precommit: bool,
) -> None:
    if type(attempt_store) is not AttemptStore:
        raise ResultValidationError("exact durable AttemptStore is required")
    if Path(attempt_store.path).resolve() != Path(result.attempt_journal_path).resolve():
        raise ResultValidationError("attempt journal binding differs")
    try:
        status = attempt_store.status()
        claim = attempt_store.claimed_reservation("TB_E1")
    except Exception as exc:
        raise ResultValidationError("attempt journal binding cannot be verified") from exc
    if claim.reservation_event_digest != result.attempt_reservation_event_digest:
        raise ResultValidationError("attempt journal binding differs")
    # A completed retry is checked against the durable manifest and full
    # authentication identity under the commit lock. Its journal necessarily
    # differs from the precommit snapshot, including after a boot-fence event.
    if precommit and attempt_store.result("TB_E1") is None:
        if (status["event_head"] != result.attempt_journal_event_head
                or status["event_count"] != result.attempt_journal_event_count):
            raise ResultValidationError("attempt journal binding differs")
        doc = _revalidate_validated_result(result)
        if hashlib.sha256(attempt_store.path.read_bytes()).hexdigest() != doc.get(
                "attempt_journal_sha256"):
            raise ResultValidationError("attempt journal binding differs")


def _revalidate_result_outputs(result: ValidatedResult) -> None:
    root = Path(result.output_root)
    if not root.is_dir() or _is_reparse_point(root):
        raise ResultValidationError("validated output root is missing or unsafe")
    actual_files: set[str] = set()
    for item in root.rglob("*"):
        if _is_reparse_point(item):
            raise ResultValidationError("validated output root contains a link/reparse point")
        if item.is_file():
            actual_files.add(item.relative_to(root).as_posix())
        elif not item.is_dir():
            raise ResultValidationError("validated output root contains a non-file entry")
    if actual_files != set(result.output_paths.values()):
        raise ResultValidationError("validated output inventory drifted")
    for role, relative in result.output_paths.items():
        payload = root.joinpath(*PurePosixPath(relative).parts).read_bytes()
        if hashlib.sha256(payload).hexdigest() != result.output_sha256[role]:
            raise ResultValidationError("validated output bytes drifted")


def _fields(value: Any, required: set[str], label: str) -> Mapping[str, Any]:
    if not isinstance(value, dict) or set(value) != required:
        raise ResultValidationError(f"{label} fields differ")
    return value


def _sha(value: Any, label: str) -> str:
    if (not isinstance(value, str) or len(value) != 64
            or any(ch not in "0123456789abcdef" for ch in value)):
        raise ResultValidationError(f"{label} must be a lowercase SHA-256 digest")
    return value


def _instant(value: Any, label: str) -> datetime:
    if not isinstance(value, str):
        raise ResultValidationError(f"{label} must be a UTC instant")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ResultValidationError(f"{label} must be a UTC instant") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ResultValidationError(f"{label} must be timezone-aware")
    return parsed.astimezone(timezone.utc)


def _outcome_record(outcome: Any) -> dict[str, Any]:
    try:
        status = outcome.status
        sessions = outcome.sessions_to_pass
        failure = outcome.failure_reason
        diagnostics = outcome.diagnostics
    except AttributeError as exc:
        raise ResultValidationError("typed PathOutcome values are required") from exc
    if status not in ("PASS", "FAILURE", "UNRESOLVED"):
        raise ResultValidationError("PathOutcome status is invalid")
    if sessions is not None and (isinstance(sessions, bool) or not isinstance(sessions, int) or sessions < 0):
        raise ResultValidationError("PathOutcome sessions_to_pass is invalid")
    if failure is not None and not isinstance(failure, str):
        raise ResultValidationError("PathOutcome failure_reason is invalid")
    if not isinstance(diagnostics, tuple) or any(
            not isinstance(row, tuple) or len(row) != 2
            or not all(isinstance(item, str) for item in row) for row in diagnostics):
        raise ResultValidationError("PathOutcome diagnostics must be immutable string pairs")
    if status == "PASS" and (sessions is None or failure is not None):
        raise ResultValidationError("passing PathOutcome must have sessions and no failure")
    if status != "PASS" and (sessions is not None or not failure):
        raise ResultValidationError("nonpassing PathOutcome must retain its failure reason")
    return {"diagnostics": [list(row) for row in diagnostics],
            "failure_reason": failure, "sessions_to_pass": sessions, "status": status}


def _validate_checkpoint_plan_inputs(
    binding_bytes: bytes, *, checkpoint: str, contract: Any,
    exact_depth_approval_sha256: str, synthetic: bool,
    inventory_records: Sequence[Mapping[str, Any]],
) -> None:
    try:
        plan = _fields(
            parse_canonical_json(binding_bytes, label=f"{checkpoint} checkpoint plan"),
            {"schema", "checkpoint", "contract_sha256", "trust_domain_sha256", "synthetic",
             "exact_depth_approval_sha256", "horizon_sessions", "seed_inputs", "extra"},
            "checkpoint plan",
        )
    except Exception as exc:
        raise ResultValidationError(str(exc)) from exc
    if (plan["schema"] != "e1_checkpoint_plan/v1"
            or plan["checkpoint"] != checkpoint
            or plan["contract_sha256"] != contract.contract_sha256
            or plan["trust_domain_sha256"] != contract.trust_domain_sha256
            or plan["synthetic"] is not synthetic
            or plan["exact_depth_approval_sha256"] != exact_depth_approval_sha256
            or plan["horizon_sessions"] != contract.replay.horizon_sessions
            or not isinstance(plan["seed_inputs"], list)
            or (plan["extra"] is not None and not isinstance(plan["extra"], dict))):
        raise ResultValidationError("checkpoint plan identity or execution policy differs")
    path_seed_digests: list[str] = []
    # Derive the complete authorized inventory from F1, not from caller rows.
    # These are the same canonical stream-address producers used at dispatch.
    from .orchestration import _stage_seeds, _part_a_seeds
    expected_seeds = (
        _stage_seeds(contract, 'n1', synthetic) if checkpoint == 'N1' else
        _stage_seeds(contract, 'n2', synthetic) if checkpoint == 'N2' else
        _part_a_seeds(contract, synthetic) if checkpoint == 'PART_A' else ())
    if canonical_json_bytes(plan['seed_inputs']) != canonical_json_bytes([
            parse_canonical_json(seed.canonical_bytes, label='derived seed')
            for seed in expected_seeds]):
        raise ResultValidationError('checkpoint plan seed inputs differ from frozen derivation')
    for raw in plan["seed_inputs"]:
        seed = _fields(raw, {
            "schema", "contract_sha256", "root_rng_namespace", "stage",
            "trust_domain_sha256",
            "population", "panel_index", "path_index", "purpose", "synthetic",
            "seed", "source_session_ids_sha256",
        }, "checkpoint seed input")
        if (seed["schema"] != "qualification-seed-input/v1"
                or seed["contract_sha256"] != contract.contract_sha256
                or seed["trust_domain_sha256"] != contract.trust_domain_sha256
                or seed["synthetic"] is not synthetic
                or not isinstance(seed["population"], str)
                or not seed["population"]
                or type(seed["path_index"]) is not int
                or seed["path_index"] < 0
                or (seed["panel_index"] is not None
                    and (type(seed["panel_index"]) is not int
                         or seed["panel_index"] < 0))
                or seed["purpose"] not in ("path", "outer")):
            raise ResultValidationError("checkpoint seed input identity differs")
        if type(seed["seed"]) is not int or seed["seed"] < 0:
            raise ResultValidationError("checkpoint seed must be a non-negative integer")
        _sha(seed["source_session_ids_sha256"], "checkpoint source sessions")
        digest = hashlib.sha256(canonical_json_bytes(dict(seed))).hexdigest()
        if seed["purpose"] == "path":
            path_seed_digests.append(digest)
    retained_stages = {
        "N1": ("N1",), "CUTOFF": (), "N2": ("N2", "PART_B"),
        "PART_A": ("PART_A",),
    }[checkpoint]
    expected = [row["seed_input_sha256"] for row in inventory_records
                if row["stage"] in retained_stages]
    matches = (path_seed_digests[:len(expected)] == expected
               if checkpoint == "PART_A" else path_seed_digests == expected)
    if not matches:
        raise ResultValidationError(
            "checkpoint plan seed inputs differ from retained result inputs")


def _validate_part_a_panels(contract, extra, inventory_records):
    """Bind the retained panel order and source membership to frozen FULL.

    This validates declared panel evidence, not execution of the sampler.
    """
    from types import SimpleNamespace
    from .orchestration import panel_identity
    extra = _fields(extra, {'panels'}, 'Part A panel evidence')
    panels = extra['panels']
    spec = contract.replay.part_a
    records = [row for row in inventory_records if row['stage'] == 'PART_A']
    if (type(panels) is not list or len(panels) not in
            (spec.initial_panels, spec.expanded_panels)
            or len(records) != len(panels) * spec.paths_per_population_per_panel):
        raise ResultValidationError('Part A panel inventory differs from frozen depth')
    full = contract.populations['FULL']
    for index, panel in enumerate(panels):
        panel = _fields(panel, {'panel_index', 'panel_id', 'source_session_ids'}, 'Part A panel')
        sources = panel['source_session_ids']
        if (type(panel['panel_index']) is not int or panel['panel_index'] != index
                or type(sources) is not list or len(sources) != len(full)
                or any(type(source) is not str or source not in full for source in sources)):
            raise ResultValidationError('Part A panel source membership or order differs')
        identity = panel_identity(contract, SimpleNamespace(index=index, source_session_ids=tuple(sources)))
        if panel['panel_id'] != identity:
            raise ResultValidationError('Part A panel source identity differs')
        offset = index * spec.paths_per_population_per_panel
        if any(row['panel_id'] != identity or row['population'] != 'REGIME' or row['path_index'] != path
               for path, row in enumerate(records[offset:offset + spec.paths_per_population_per_panel])):
            raise ResultValidationError('Part A panel path binding differs')


def _expected_stage_counts(contract: Any) -> Mapping[str, Mapping[str, tuple[int, ...]]]:
    specs = getattr(contract, "stage_specs", None)
    if specs is None:
        raise ResultValidationError("frozen contract lacks stage specifications")
    if isinstance(specs, Mapping):
        specs = tuple(specs.values())
    result: dict[str, Mapping[str, int]] = {}
    for spec in specs:
        if getattr(spec, "included_in_e1_seal", True) is not True:
            continue
        name = getattr(spec, "name", None)
        counts = getattr(spec, "population_counts", None)
        if name in result or not isinstance(name, str) or not isinstance(counts, Mapping):
            raise ResultValidationError("frozen stage specification is invalid")
        normalized = {}
        for population, count in counts.items():
            allowed = (count,) if isinstance(count, int) and not isinstance(count, bool) else count
            if (not isinstance(population, str) or not isinstance(allowed, tuple)
                    or not allowed or any(isinstance(item, bool) or not isinstance(item, int)
                                          or item < 0 for item in allowed)
                    or len(set(allowed)) != len(allowed)):
                raise ResultValidationError("frozen stage population count is invalid")
            normalized[population] = tuple(allowed)
        result[name] = MappingProxyType(normalized)
    if tuple(result) != MANDATORY_E1_STAGES:
        raise ResultValidationError("frozen E1 stage inventory/order is invalid")
    return MappingProxyType(result)


def validate_result_envelope(
    contract: Any,
    result_bytes: bytes,
    *,
    path_outcomes: Mapping[str, Mapping[str, Sequence[Any]]],
    path_inventory_bytes: bytes,
    attempt_store: AttemptStore,
    runtime_load_trace_bytes: bytes,
    preflight_receipt: PreflightReceipt,
    exact_depth_approval_bytes: bytes,
    exact_depth_trusted_keys: Mapping[str, TrustedApprovalKey],
    approval_now: datetime,
    stage_input_sha256: Mapping[str, str],
    adjudicator: FrozenAdjudicator,
    trust_domain: object,
) -> ValidatedResult:
    """Validate a retained envelope; this grants no authority and signs nothing."""
    try:
        contract = require_validated_frozen_contract(contract)
        domain = require_validated_trust_domain(trust_domain)
    except Exception as exc:
        raise ResultValidationError(f"validated contract/trust domain required: {exc}") from exc
    if contract.trust_domain is not domain or contract.trust_domain_sha256 != domain.sha256:
        raise ResultValidationError("result trust domain differs from frozen contract")
    try:
        doc = parse_canonical_json(result_bytes, label="result envelope")
    except Exception as exc:
        raise ResultValidationError(str(exc)) from exc
    doc = _fields(doc, {
        "schema", "attempt_id", "contract_sha256", "trust_domain_sha256",
        "shared_manifest_sha256",
        "exact_depth_approval_sha256", "producer", "started_utc", "completed_utc",
        "completion", "verdict", "terminal_reason", "stage_results", "outputs",
        "path_inventory_sha256",
        "runtime_load_trace_sha256", "attempt_journal_sha256", "previous_result_sha256",
    }, "result envelope")
    if (doc["schema"] != RESULT_SCHEMA
            or doc["contract_sha256"] != contract.contract_sha256
            or doc["trust_domain_sha256"] != domain.sha256):
        raise ResultValidationError("result schema/contract/trust domain identity differs")
    attempt_id = doc["attempt_id"]
    if not isinstance(attempt_id, str) or not attempt_id:
        raise ResultValidationError("attempt_id is invalid")
    try:
        preflight_receipt = revalidate_e1_preflight(
            contract, preflight_receipt,
            exact_depth_approval_bytes=exact_depth_approval_bytes,
            trusted_keys=exact_depth_trusted_keys, now=approval_now,
            trust_domain=domain,
        )
    except Exception as exc:
        raise ResultValidationError(f"exact-depth preflight differs: {exc}") from exc
    exact_depth_approval_sha256 = preflight_receipt.exact_depth_approval.approval_sha256
    if (preflight_receipt.attempt_id != attempt_id
            or doc["exact_depth_approval_sha256"] != exact_depth_approval_sha256):
        raise ResultValidationError("exact-depth approval identity differs")
    if type(attempt_store) is not AttemptStore:
        raise ResultValidationError("exact durable AttemptStore is required")
    if attempt_store.trust_domain_sha256 != domain.sha256:
        raise ResultValidationError("attempt journal trust domain differs")
    try:
        attempt_snapshot = AttemptStore.inspect(attempt_store.path)
        stage_claim = attempt_store.claimed_reservation("TB_E1")
        attempt_journal_bytes = attempt_store.path.read_bytes()
    except Exception as exc:
        raise ResultValidationError("durable attempt journal cannot be inspected") from exc
    preflight_binding_sha256 = hashlib.sha256(
        preflight_binding_bytes(preflight_receipt)).hexdigest()
    if (not isinstance(stage_claim, StageClaim)
            or stage_claim.campaign_id != attempt_id
            or stage_claim.contract_digest != contract.contract_sha256
            or stage_claim.stage != "TB_E1"
            or stage_claim.binding_sha256 != preflight_binding_sha256
            or stage_claim.state != "STARTED_IN_DOUBT"):
        raise ResultValidationError("durable TB_E1 stage claim differs")
    try:
        snapshot_status = attempt_snapshot["status"]
        snapshot_stage = next(row for row in attempt_snapshot["stages"]
                              if row["stage"] == "TB_E1")
    except (KeyError, TypeError, StopIteration) as exc:
        raise ResultValidationError("attempt snapshot is incomplete") from exc
    if (snapshot_status.get("campaign_id"), snapshot_status.get("contract_digest"),
            snapshot_status.get("validity"), snapshot_stage.get("state")) != (
            attempt_id, contract.contract_sha256, "VALID", "STARTED_IN_DOUBT"):
        raise ResultValidationError("attempt snapshot differs from durable TB_E1 claim")
    producer = _fields(doc["producer"], {"producer_id", "boot_id", "tool_sha256", "runtime_sha256"}, "producer")
    if not all(isinstance(producer[name], str) and producer[name]
               for name in ("producer_id", "boot_id")):
        raise ResultValidationError("producer identity is invalid")
    _sha(producer["tool_sha256"], "producer tool")
    _sha(producer["runtime_sha256"], "producer runtime")
    if (producer["tool_sha256"] != contract.runtime_load_sha256.get("qualification_runner")
            or producer["runtime_sha256"] != contract.runtime_load_sha256.get("runtime_distribution")):
        raise ResultValidationError("producer identities differ from their exact frozen roles")
    _instant(doc["started_utc"], "started_utc")
    completion = doc["completion"]
    verdict = doc["verdict"]
    if completion == "PARTIAL":
        if verdict != "NONE" or doc["completed_utc"] is not None:
            raise ResultValidationError("partial result must remain undecided and incomplete")
    elif completion == "COMPLETE":
        completed = _instant(doc["completed_utc"], "completed_utc")
        if completed < _instant(doc["started_utc"], "started_utc"):
            raise ResultValidationError("result completion precedes start")
    else:
        raise ResultValidationError("result completion is invalid")
    if verdict not in ("PASS", "FAIL", "AMBIGUOUS", "BLOCKED", "VOID", "NONE"):
        raise ResultValidationError("result verdict is invalid")
    if verdict == "PASS" and doc["terminal_reason"] is not None:
        raise ResultValidationError("PASS result cannot have a terminal reason")
    if completion == "COMPLETE" and verdict == "NONE":
        raise ResultValidationError("complete result must carry a terminal verdict")
    if (completion == "COMPLETE" and verdict != "PASS"
            and (not isinstance(doc["terminal_reason"], str)
                 or not doc["terminal_reason"])):
        raise ResultValidationError("non-PASS complete result requires a terminal reason")
    if completion == "PARTIAL" and doc["terminal_reason"] is not None:
        raise ResultValidationError("partial result cannot claim a terminal reason")
    if doc["previous_result_sha256"] is not None:
        _sha(doc["previous_result_sha256"], "previous result")

    if hashlib.sha256(attempt_journal_bytes).hexdigest() != doc["attempt_journal_sha256"]:
        raise ResultValidationError("attempt journal identity differs")
    if hashlib.sha256(runtime_load_trace_bytes).hexdigest() != doc["runtime_load_trace_sha256"]:
        raise ResultValidationError("runtime load trace identity differs")
    try:
        runtime_trace = parse_canonical_json(runtime_load_trace_bytes, label="runtime load trace")
    except Exception as exc:
        raise ResultValidationError(str(exc)) from exc
    if runtime_trace != dict(contract.runtime_load_sha256):
        raise ResultValidationError("runtime load trace differs from frozen contract")
    if type(adjudicator) is not FrozenAdjudicator:
        raise ResultValidationError("exact frozen adjudicator dispatcher is required")
    try:
        adjudicator.verify_for(contract)
    except Exception as exc:
        raise ResultValidationError("adjudicator identity differs from frozen contract") from exc
    artifact_by_role = {getattr(row, "role", None): getattr(row, "sha256", None)
                        for row in getattr(contract, "artifacts", ())}
    if doc["shared_manifest_sha256"] != artifact_by_role.get("shared_manifest"):
        raise ResultValidationError("shared manifest differs from its exact frozen role")

    try:
        path_inventory = _fields(
            parse_canonical_json(path_inventory_bytes, label="path inventory"),
            {"schema", "trust_domain_sha256", "records"}, "path inventory",
        )
    except Exception as exc:
        raise ResultValidationError(str(exc)) from exc
    if (path_inventory["schema"] != "qualification_path_inventory/v1"
            or path_inventory["trust_domain_sha256"] != domain.sha256):
        raise ResultValidationError("path inventory schema differs")
    path_inventory_sha256 = hashlib.sha256(path_inventory_bytes).hexdigest()
    if doc["path_inventory_sha256"] != path_inventory_sha256:
        raise ResultValidationError("path inventory identity differs")
    inventory_records = path_inventory["records"]
    if not isinstance(inventory_records, list):
        raise ResultValidationError("path inventory records must be a list")

    required_roles = tuple(getattr(contract, "required_output_roles", ()))
    optional_roles = tuple(getattr(contract, "permitted_optional_output_roles",
                                   getattr(contract, "optional_output_roles", ())))
    outputs = doc["outputs"]
    if not isinstance(outputs, list):
        raise ResultValidationError("outputs must be a list")
    declared: dict[str, str] = {}
    declared_paths: set[str] = set()
    for raw in outputs:
        row = _fields(raw, {"role", "path", "sha256", "byte_length", "privacy"}, "output")
        role = row["role"]
        if role in declared or role not in set(required_roles) | set(optional_roles):
            raise ResultValidationError("output role is duplicate or undeclared")
        if row["privacy"] not in ("PRIVATE", "PUBLIC_PROJECTION"):
            raise ResultValidationError("output privacy class is invalid")
        relative = row["path"]
        if (not isinstance(relative, str) or not relative or relative in declared_paths
                or "\\" in relative or PurePosixPath(relative).is_absolute()
                or any(part in ("", ".", "..") for part in PurePosixPath(relative).parts)):
            raise ResultValidationError("output path is invalid, duplicate, or noncanonical")
        declared_paths.add(relative)
        target = Path(preflight_receipt.output_root).joinpath(*PurePosixPath(relative).parts)
        if not target.is_file() or _is_reparse_point(target):
            raise ResultValidationError("output is missing or unsafe")
        payload = target.read_bytes()
        if (isinstance(row["byte_length"], bool)
                or not isinstance(row["byte_length"], int)
                or row["byte_length"] != len(payload)):
            raise ResultValidationError("output has wrong length")
        digest = hashlib.sha256(payload).hexdigest()
        if digest != row["sha256"]:
            raise ResultValidationError("output digest differs")
        declared[role] = digest
    root = Path(preflight_receipt.output_root)
    actual_files: set[str] = set()
    actual_dirs: set[str] = set()
    for item in root.rglob("*"):
        if _is_reparse_point(item):
            raise ResultValidationError("output root contains a link/reparse point")
        relative = item.relative_to(root).as_posix()
        if item.is_file():
            actual_files.add(relative)
        elif item.is_dir():
            actual_dirs.add(relative)
        else:
            raise ResultValidationError("output root contains a non-file entry")
    expected_dirs = {
        parent.as_posix()
        for path in declared_paths for parent in PurePosixPath(path).parents
        if parent.as_posix() != "."
    }
    if ((completion == "COMPLETE" and not set(required_roles).issubset(declared))
            or actual_files != declared_paths or actual_dirs != expected_dirs):
        raise ResultValidationError("output inventory is missing or contains extras")

    expected = _expected_stage_counts(contract)
    stage_rows = doc["stage_results"]
    stage_order = tuple(row.get("stage") for row in stage_rows) if isinstance(stage_rows, list) else ()
    required_order = MANDATORY_E1_STAGES[:len(stage_order)]
    if (not isinstance(stage_rows, list) or not stage_order
            or stage_order != required_order):
        raise ResultValidationError("stage result inventory/order differs")
    if set(path_outcomes) != set(stage_order):
        raise ResultValidationError("PathOutcome stage inventory differs")
    if set(stage_input_sha256) != set(stage_order):
        raise ResultValidationError("stage input identity inventory differs")
    stage_digests: dict[str, str] = {}
    normalized_by_stage: dict[str, dict[str, list[dict[str, Any]]]] = {}
    declared_stage_status: dict[str, str] = {}
    expected_inventory: list[dict[str, Any]] = []
    inventory_cursor = 0
    seed_inputs: set[str] = set()
    for raw in stage_rows:
        row = _fields(raw, {"stage", "status", "input_sha256", "output_sha256", "population_counts"}, "stage result")
        name = row["stage"]
        if row["status"] not in ("PASS", "FAIL", "PARTIAL", "NOT_RUN"):
            raise ResultValidationError("stage status is invalid")
        _sha(row["input_sha256"], "stage input")
        _sha(row["output_sha256"], "stage output")
        declared_counts = row["population_counts"]
        if not isinstance(declared_counts, dict) or set(declared_counts) != set(expected[name]):
            raise ResultValidationError("stage population counts differ from frozen contract")
        for population, count in declared_counts.items():
            if count not in expected[name][population]:
                raise ResultValidationError("stage population count is not an allowed frozen depth")
        observed = path_outcomes.get(name)
        if not isinstance(observed, Mapping) or set(observed) != set(expected[name]):
            raise ResultValidationError("PathOutcome population inventory differs")
        normalized: dict[str, list[dict[str, Any]]] = {}
        stage_inventory_start = len(expected_inventory)
        for population, count in declared_counts.items():
            rows = observed[population]
            if name == "PART_A":
                try:
                    part_a_depth = contract.replay.part_a.paths_per_population_per_panel
                except AttributeError as exc:
                    raise ResultValidationError(
                        "frozen contract lacks Part A path depth") from exc
                if (isinstance(part_a_depth, bool) or not isinstance(part_a_depth, int)
                        or part_a_depth < 1):
                    raise ResultValidationError("frozen Part A path depth is invalid")
                expected_row_count = count * part_a_depth
            else:
                part_a_depth = None
                expected_row_count = count
            if len(rows) != expected_row_count:
                raise ResultValidationError("PathOutcome count differs from frozen contract")
            normalized[population] = [_outcome_record(item) for item in rows]
            part_a_panels: list[str] = []
            for flat_index, outcome_record in enumerate(normalized[population]):
                if inventory_cursor >= len(inventory_records):
                    raise ResultValidationError("path inventory is incomplete")
                inventory = _fields(
                    inventory_records[inventory_cursor],
                    {"stage", "population", "path_index", "panel_id",
                     "seed_input_sha256", "outcome_sha256"},
                    "path inventory record",
                )
                panel_id = inventory["panel_id"]
                if name == "PART_A":
                    if not isinstance(panel_id, str) or not panel_id:
                        raise ResultValidationError("Part A path inventory requires panel identity")
                    assert part_a_depth is not None
                    panel_index, path_index = divmod(flat_index, part_a_depth)
                    if path_index == 0:
                        if panel_id in part_a_panels:
                            raise ResultValidationError("Part A panel identity is duplicated")
                        part_a_panels.append(panel_id)
                    elif panel_id != part_a_panels[panel_index]:
                        raise ResultValidationError(
                            "Part A panel identity is not stable for its frozen-depth block")
                elif panel_id is not None:
                    raise ResultValidationError("non-Part-A path inventory cannot carry panel identity")
                else:
                    path_index = flat_index
                seed_input = _sha(inventory["seed_input_sha256"], "path seed input")
                if seed_input in seed_inputs:
                    raise ResultValidationError("path seed input identity is duplicated")
                seed_inputs.add(seed_input)
                expected_record = {
                    "stage": name,
                    "population": population,
                    "path_index": path_index,
                    "panel_id": panel_id,
                    "seed_input_sha256": seed_input,
                    "outcome_sha256": hashlib.sha256(
                        canonical_json_bytes(outcome_record)).hexdigest(),
                }
                if dict(inventory) != expected_record:
                    raise ResultValidationError(
                        "path inventory stage/population/index/outcome binding differs")
                expected_inventory.append(expected_record)
                inventory_cursor += 1
            if name == "PART_A" and len(part_a_panels) != count:
                raise ResultValidationError("Part A panel inventory count differs")
        if name == "LEGALITY":
            seed_binding = {
                "contract_sha256": contract.contract_sha256,
                "trust_domain_sha256": domain.sha256,
                "exact_depth_approval_sha256": exact_depth_approval_sha256,
                "stage": name,
            }
        else:
            seed_binding = {
                "stage": name,
                "paths": [{
                    "population": item["population"],
                    "path_index": item["path_index"],
                    "panel_id": item["panel_id"],
                    "seed_input_sha256": item["seed_input_sha256"],
                } for item in expected_inventory[stage_inventory_start:]],
            }
        observed_input_sha256 = hashlib.sha256(
            canonical_json_bytes(seed_binding)).hexdigest()
        if (row["input_sha256"] != observed_input_sha256
                or stage_input_sha256[name] != observed_input_sha256):
            raise ResultValidationError(
                "stage input identity differs from durable checkpoint binding")
        digest = hashlib.sha256(canonical_json_bytes(normalized)).hexdigest()
        if digest != row["output_sha256"]:
            raise ResultValidationError("stage output does not bind exact PathOutcome values")
        declared_stage_status[name] = row["status"]
        stage_digests[name] = digest
        normalized_by_stage[name] = normalized
    if inventory_cursor != len(inventory_records):
        raise ResultValidationError("path inventory contains extra records")
    checkpoint_receipts: dict[str, Mapping[str, Any]] = {}
    if completion == "COMPLETE":
        checkpoints = attempt_snapshot.get("checkpoints")
        if (not isinstance(checkpoints, list)
                or tuple(row.get("checkpoint") for row in checkpoints)
                != ("N1", "CUTOFF", "N2", "PART_A")):
            raise ResultValidationError("durable E1 checkpoint inventory differs")
        required_checkpoint_maps: dict[str, dict[str, str]] = {
            "N1": {"N1": stage_input_sha256["N1"]},
            "CUTOFF": {},
        }
        if "N2" in stage_order:
            if "PART_B" not in stage_order:
                raise ResultValidationError("N2/PART_B checkpoint batch is incomplete")
            required_checkpoint_maps["N2"] = {
                "N2": stage_input_sha256["N2"],
                "PART_B": stage_input_sha256["PART_B"],
            }
        if "PART_A" in stage_order:
            required_checkpoint_maps["PART_A"] = {
                "PART_A": stage_input_sha256["PART_A"],
            }
        for checkpoint in checkpoints:
            name = checkpoint["checkpoint"]
            if name not in required_checkpoint_maps:
                if checkpoint.get("state") != "PENDING":
                    raise ResultValidationError(
                        "durable checkpoint continues beyond terminal result prefix")
                continue
            if checkpoint.get("state") != "COMPLETED":
                raise ResultValidationError("required durable checkpoint is incomplete")
            receipt_bytes = checkpoint.get("receipt_bytes")
            try:
                receipt = _fields(
                    parse_canonical_json(receipt_bytes, label=f"{name} checkpoint receipt"),
                    {"schema", "checkpoint", "attempt_id", "contract_sha256",
                     "trust_domain_sha256",
                     "binding_sha256", "dispatch_event_digest", "synthetic",
                     "decisions", "stage_input_sha256", "path_inventory",
                     "outcomes", "extra"},
                    "checkpoint receipt",
                )
            except Exception as exc:
                raise ResultValidationError(str(exc)) from exc
            binding_bytes = checkpoint.get("binding_bytes")
            dispatch_digest = checkpoint.get("dispatch_event_digest")
            if (not isinstance(binding_bytes, bytes)
                    or not isinstance(dispatch_digest, str)):
                raise ResultValidationError("checkpoint durable dispatch binding is incomplete")
            if (receipt["schema"] != "e1_checkpoint_receipt/v1"
                    or receipt["checkpoint"] != name
                    or receipt["attempt_id"] != attempt_id
                    or receipt["contract_sha256"] != contract.contract_sha256
                    or receipt["trust_domain_sha256"] != domain.sha256
                    or receipt["binding_sha256"] != hashlib.sha256(binding_bytes).hexdigest()
                    or receipt["dispatch_event_digest"] != dispatch_digest
                    or receipt["stage_input_sha256"] != required_checkpoint_maps[name]):
                raise ResultValidationError(
                    "checkpoint receipt does not bind exact result stage inputs")
            _validate_checkpoint_plan_inputs(
                binding_bytes, checkpoint=name, contract=contract,
                exact_depth_approval_sha256=exact_depth_approval_sha256,
                synthetic=receipt["synthetic"], inventory_records=inventory_records)
            if (not isinstance(receipt["synthetic"], bool)
                    or receipt["synthetic"] is not domain.permits_synthetic):
                raise ResultValidationError("checkpoint synthetic policy differs from trust domain")
            if (not isinstance(receipt["decisions"], dict)
                    or not isinstance(receipt["path_inventory"], list)
                    or not isinstance(receipt["outcomes"], dict)
                    or not isinstance(receipt["extra"], dict)):
                raise ResultValidationError("checkpoint retained evidence shape differs")
            checkpoint_receipts[name] = receipt
            if name == 'PART_A':
                _validate_part_a_panels(contract, receipt['extra'], inventory_records)
    try:
        decisions = adjudicator(path_outcomes, path_inventory)
    except Exception as exc:
        raise ResultValidationError("frozen adjudication failed") from exc
    if (not isinstance(decisions, Mapping) or set(decisions) != set(stage_order)
            or any(value not in ("PASS", "FAIL") for value in decisions.values())):
        raise ResultValidationError("frozen adjudication returned an invalid stage inventory")
    receipt_stages = {
        "N1": ("N1",), "CUTOFF": (), "N2": ("N2", "PART_B"),
        "PART_A": ("PART_A",),
    }
    decision_stages = {
        "N1": (), "CUTOFF": ("N1",), "N2": ("N2", "PART_B"),
        "PART_A": ("PART_A",),
    }
    for checkpoint, receipt in checkpoint_receipts.items():
        stages = tuple(stage for stage in receipt_stages[checkpoint] if stage in stage_order)
        expected_outcomes = {stage: normalized_by_stage[stage] for stage in stages}
        expected_inventory_records = [
            record for record in inventory_records if record["stage"] in stages
        ]
        expected_decisions = {
            stage: decisions[stage] for stage in decision_stages[checkpoint]
            if stage in decisions
        }
        if (receipt["outcomes"] != expected_outcomes
                or receipt["path_inventory"] != expected_inventory_records
                or receipt["decisions"] != expected_decisions):
            raise ResultValidationError(
                "checkpoint receipt retained evidence differs from result envelope")
    if declared_stage_status != dict(decisions):
        raise ResultValidationError("stage label differs from frozen adjudication")
    failed = tuple(name for name, decision in decisions.items() if decision != "PASS")
    if completion == "PARTIAL" and failed:
        raise ResultValidationError("failed stage must be retained as a terminal complete prefix")
    if completion == "COMPLETE":
        if failed:
            first_failure = failed[0]
            terminal_orders = {
                "LEGALITY": ("LEGALITY",),
                "N1": ("LEGALITY", "N1"),
                "N2": ("LEGALITY", "N1", "N2", "PART_B"),
                "PART_B": ("LEGALITY", "N1", "N2", "PART_B"),
                "PART_A": MANDATORY_E1_STAGES,
            }
            if stage_order != terminal_orders[first_failure] or verdict != "FAIL":
                raise ResultValidationError(
                    "terminal failure verdict/prefix differs from frozen adjudication")
        elif stage_order != MANDATORY_E1_STAGES or verdict != "PASS":
            raise ResultValidationError(
                "complete passing verdict/inventory differs from frozen adjudication")
    return _register_validated_result(ValidatedResult(
        attempt_id, contract.contract_sha256, domain.sha256,
        hashlib.sha256(result_bytes).hexdigest(),
        bytes(result_bytes), completion, verdict, MappingProxyType(stage_digests),
        MappingProxyType(declared), _sha(doc["shared_manifest_sha256"], "shared manifest"),
        path_inventory_sha256, preflight_receipt.output_root,
        MappingProxyType({row["role"]: row["path"] for row in outputs}),
        str(attempt_store.path.resolve()), snapshot_status["event_head"],
        snapshot_status["event_count"], stage_claim.reservation_event_digest,
    ))


def _verify_external_record(
    record_bytes: bytes, *, schema: str, scope: str, subject_sha256: str,
    contract_sha256: str, attempt_id: str, trusted_keys: Mapping[str, TrustedResultKey],
    now: datetime, trust_domain: object, enrolled_key_ids: tuple[str, ...],
) -> str:
    if type(record_bytes) is not bytes:
        raise ResultValidationError("authentication record requires immutable bytes")
    try:
        domain = require_validated_trust_domain(trust_domain)
    except Exception as exc:
        raise ResultValidationError(f"validator-issued trust domain required: {exc}") from exc
    try:
        outer = _fields(parse_canonical_json(record_bytes, label=scope),
                        {"schema", "payload", "signature"}, scope)
    except Exception as exc:
        raise ResultValidationError(str(exc)) from exc
    if outer["schema"] != schema:
        raise ResultValidationError("authentication schema differs")
    payload = _fields(outer["payload"],
                      {"scope", "subject_sha256", "contract_sha256", "trust_domain_sha256",
                       "attempt_id", "issued_utc", "expires_utc"},
                      "authentication payload")
    signature = _fields(outer["signature"], {"algorithm", "key_id", "value_b64"}, "authentication signature")
    if (payload["scope"], payload["subject_sha256"], payload["contract_sha256"],
            payload["trust_domain_sha256"], payload["attempt_id"]) != (
            scope, subject_sha256, contract_sha256, domain.sha256, attempt_id):
        raise ResultValidationError("authentication scope/subject differs")
    issued = _instant(payload["issued_utc"], "issued_utc")
    expires = _instant(payload["expires_utc"], "expires_utc")
    if now.tzinfo is None or now.utcoffset() is None:
        raise ResultValidationError("authentication verification time must be timezone-aware")
    now_utc = now.astimezone(timezone.utc)
    if not issued <= now_utc < expires:
        raise ResultValidationError("authentication is outside its validity window")
    key = trusted_keys.get(signature["key_id"])
    if (key is None or key.key_id != signature["key_id"] or scope not in key.scopes
            or signature["key_id"] not in enrolled_key_ids):
        raise ResultValidationError("authentication key/scope is not trusted")
    if key.authority_class != domain.authority_class:
        raise ResultValidationError("authentication authority class differs")
    try:
        require_trusted_domain_key(domain, key.key_id, key.public_key)
    except Exception as exc:
        raise ResultValidationError(f"authentication key differs from trust domain: {exc}") from exc
    if key.revoked_at is not None:
        if key.revoked_at.tzinfo is None or key.revoked_at.utcoffset() is None:
            raise ResultValidationError("authentication key revocation time must be timezone-aware")
        if key.revoked_at.astimezone(timezone.utc) <= now_utc:
            raise ResultValidationError("authentication key is revoked")
    if signature["algorithm"] != "Ed25519":
        raise ResultValidationError("authentication algorithm differs")
    try:
        encoded = signature["value_b64"]
        if not isinstance(encoded, str):
            raise ValueError("not a string")
        raw = base64.b64decode(encoded, validate=True)
        if base64.b64encode(raw).decode("ascii") != encoded:
            raise ValueError("non-canonical base64")
    except ValueError as exc:
        raise ResultValidationError("authentication signature is invalid") from exc
    if not is_strong_public_key(key.public_key):
        raise ResultValidationError("authentication key is not a strong Ed25519 public key")
    if not verify_ed25519(key.public_key, canonical_json_bytes(dict(payload)), raw):
        raise ResultValidationError("authentication signature is invalid")
    return key.key_id


def inspect_result_authentication(
    result: ValidatedResult, authentication_bytes: bytes, *,
    trusted_keys: Mapping[str, TrustedResultKey], now: datetime,
    trust_domain: object,
) -> AuthenticatedResult:
    """Inspect historical v1 consistency; this value grants no active authority."""
    domain = require_validated_trust_domain(trust_domain)
    _revalidate_validated_result(result)
    if result.trust_domain_sha256 != domain.sha256:
        raise ResultValidationError("result trust domain differs")
    _revalidate_result_outputs(result)
    key_id = _verify_external_record(
        authentication_bytes, schema=AUTH_SCHEMA, scope="ATTEST_E1_RESULT",
        subject_sha256=result.result_sha256, contract_sha256=result.contract_sha256,
        attempt_id=result.attempt_id, trusted_keys=trusted_keys, now=now,
        trust_domain=domain, enrolled_key_ids=domain.result_key_ids,
    )
    return AuthenticatedResult(result, hashlib.sha256(authentication_bytes).hexdigest(),
                               key_id, bytes(authentication_bytes), domain.sha256)


def authenticate_result(result, authentication_bytes, *, trusted_keys, now, trust_domain):
    raise ResultValidationError('LEGACY_QUALIFICATION_INSPECTION_ONLY: legacy authentication is inspection-only')


def _reauthenticate(
    result: AuthenticatedResult, *, trusted_keys: Mapping[str, TrustedResultKey],
    now: datetime, trust_domain: object,
) -> AuthenticatedResult:
    if type(result) is not AuthenticatedResult:
        raise ResultValidationError("authenticated result is required")
    verified = inspect_result_authentication(
        result.result, result.canonical_bytes, trusted_keys=trusted_keys, now=now,
        trust_domain=trust_domain,
    )
    if verified != result:
        raise ResultValidationError("authenticated result receipt differs from verified bytes")
    return verified


def authenticated_result_claim(
    result: AuthenticatedResult, *, trusted_keys: Mapping[str, TrustedResultKey],
    now: datetime, trust_domain: object,
) -> ValidatedResultClaim:
    raise ResultValidationError('LEGACY_QUALIFICATION_INSPECTION_ONLY: legacy authority retired')


def verify_authenticated_result_claim(
    result: AuthenticatedResult, claim: ValidatedResultClaim, *,
    trusted_keys: Mapping[str, TrustedResultKey], now: datetime,
    trust_domain: object,
) -> bool:
    """Legacy claims cannot grant authority after the v2 cutover."""
    try:
        return claim == authenticated_result_claim(
            result, trusted_keys=trusted_keys, now=now,
            trust_domain=trust_domain,
        )
    except ResultValidationError:
        return False


def commit_authenticated_result(
    attempt_store: AttemptStore, result: AuthenticatedResult, *,
    trusted_keys: Mapping[str, TrustedResultKey], now: datetime,
    trust_domain: object,
) -> bytes:
    raise ResultValidationError('LEGACY_QUALIFICATION_INSPECTION_ONLY: legacy authority retired')


def e1_seal_payload(result: AuthenticatedResult, *, sealed_utc: datetime) -> bytes:
    validated = result.result
    if validated.completion != "COMPLETE" or validated.verdict != "PASS":
        raise ResultValidationError("only a complete PASS result may be sealed")
    if sealed_utc.tzinfo is None or sealed_utc.utcoffset() is None:
        raise ResultValidationError("sealed_utc must be timezone-aware")
    if result.trust_domain_sha256 != validated.trust_domain_sha256:
        raise ResultValidationError("authenticated result trust domain differs")
    return canonical_json_bytes({
        "attempt_id": validated.attempt_id,
        "contract_sha256": validated.contract_sha256,
        "trust_domain_sha256": validated.trust_domain_sha256,
        "grants_activation": False,
        "grants_admission": False,
        "grants_deployment": False,
        "grants_n3": False,
        "part_a_result_sha256": validated.stage_output_sha256["PART_A"],
        "part_b_result_sha256": validated.stage_output_sha256["PART_B"],
        "result_authentication_sha256": result.authentication_sha256,
        "result_envelope_sha256": validated.result_sha256,
        "sealed_utc": sealed_utc.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "shared_manifest_sha256": validated.shared_manifest_sha256,
        "stage": "E1",
    })


def seal_e1_pass(
    result: AuthenticatedResult, seal_record_bytes: bytes, *, sealed_utc: datetime,
    trusted_keys: Mapping[str, TrustedResultKey], now: datetime,
    result_trusted_keys: Mapping[str, TrustedResultKey],
    attempt_store: AttemptStore,
    trust_domain: object,
) -> bytes:
    raise ResultValidationError('LEGACY_QUALIFICATION_INSPECTION_ONLY: legacy authority retired')


__all__ = [
    "AuthenticatedResult", "ResultValidationError", "TrustedResultKey",
    "ValidatedResult", "authenticate_result", "inspect_result_authentication", "authenticated_result_claim",
    "commit_authenticated_result", "e1_seal_payload", "seal_e1_pass", "validate_result_envelope",
    "verify_authenticated_result_claim",
]
