"""T00 P7 driver: runs only under the pinned bootstrap (``p7_evidence.P7_BOOTSTRAP``).

Validates the signed source-only contract against the pinned root, builds the
source, runs ``replay_bracket`` on the named real path and writes one evidence
record of hashes, counts and labels. It imports no runner-kernel, stage, Part A,
adjudication, seal or execution entry point, and its output is never an input to
MC, the screen or qualification (P7-closure packet §6). Design rev 4.2 §2.5a–§2.5b.
"""
import sys

_STATE = getattr(sys, 'p7_recorder', None)


def _fail(message):
    sys.stderr.write(message + '\n')
    raise SystemExit(3)


def _run(p7_evidence, argv):
    import base64
    import json
    from pathlib import Path
    from c1_rail.qualification.contract import SOURCE_EVIDENCE_CLASS, ObservedBindings, validate_source_contract
    from c1_rail.qualification.paths import PathAssembler
    from c1_rail.qualification.production_source import ProductionSource, _now

    code_root, contract_path, approval_path, registry_path, artifact_root, path_spec, _ = argv
    contract_bytes = Path(contract_path).read_bytes()
    approval_bytes = Path(approval_path).read_bytes()
    registry = {key: base64.b64decode(value) for key, value in
                json.loads(Path(registry_path).read_text(encoding='utf-8')).items()}
    contract_doc = json.loads(contract_bytes)
    root = Path(artifact_root)
    digests = {row['path']: p7_evidence.sha256_bytes((root / row['path']).read_bytes())
               for row in contract_doc['artifacts']}
    observed = ObservedBindings(digests, {row['role']: digests[row['path']] for row in contract_doc['artifacts']},
                                contract_doc['effective_settings']['settings_sha256'],
                                contract_doc['effective_settings']['orb_normal_base'])
    receipt = validate_source_contract(contract_bytes, approval_bytes, registry, observed, now=_now())
    if receipt.evidence_class != SOURCE_EVIDENCE_CLASS:
        # P7 is source verification only; a diagnostic receipt never yields a P7 record (#736 review).
        raise p7_evidence.P7Refusal(f'P7_PURPOSE_MISMATCH: P7 runs only under {SOURCE_EVIDENCE_CLASS}, '
                                    f'not {receipt.evidence_class}')
    source = ProductionSource.build(receipt, artifact_root=root)
    session_ids = json.loads(Path(path_spec).read_text(encoding='utf-8'))['sessions']
    by_id = {session.session_id: session for session in source.sessions}
    missing = [value for value in session_ids if value not in by_id]
    if not session_ids or missing:
        raise p7_evidence.P7Refusal(f'P7_PATH_UNKNOWN: sessions outside the covered FULL population: {missing}')
    block = tuple(by_id[value] for value in session_ids)
    path = PathAssembler(source.path_start_date).assemble((block,), horizon_sessions=len(block))
    result = source.replay_bracket(path)

    ports = {row['path']: row['sha256'] for row in contract_doc['artifacts'] if row['role'].endswith('_runtime_port')}
    if dict(_STATE.ports) != ports:
        raise p7_evidence.P7Refusal('P7_UNAUDITED_EXEC: compiled port bytes differ from the contract port artifacts')

    runs = {}
    for name, run in (('r1', result.r1), ('r2', result.r2)):
        projection = [[row.source_session_id, row.occurrence, float.hex(row.pnl), float.hex(row.intraday_low),
                       row.fills, row.flat_before_deadline, row.start_flat, row.end_flat] for row in run.sessions]
        runs[name] = {
            'digest': p7_evidence.sha256_bytes(p7_evidence.canonical([projection, run.events_sha256])),
            'sessions': len(run.sessions), 'fills': sum(row.fills for row in run.sessions),
            'events_sha256': run.events_sha256, 'deadline_failure': run.deadline_failure,
            # Hashes and counts only: split occurrence, leg and instant stay private (Task 4 worksheet).
            'consumed_intrabar_split_count': len(run.consumed_intrabar_splits),
            'consumed_intrabar_splits_sha256': p7_evidence.sha256_bytes(p7_evidence.canonical(
                sorted(list(item) for item in run.consumed_intrabar_splits))),
        }
    labels = []
    both = (result.r1, result.r2)
    if all(len(run.sessions) == len(block) and not run.deadline_failure for run in both):
        labels.append('BOTH_RUNS_COMPLETE')
    if all(row.intraday_low <= 0 for run in both for row in run.sessions):
        labels.append('INTRADAY_LOW_NONPOSITIVE')
    if all(run.consumed_intrabar_splits for run in both):
        labels.append('CONSUMED_INTRABAR_SPLIT')
    return {
        'evidence_class': receipt.evidence_class, 'contract_sha256': receipt.contract_sha256,
        'approval_sha256': receipt.approval.approval_sha256,
        'contract_b64': base64.b64encode(contract_bytes).decode('ascii'),
        'approval_b64': base64.b64encode(approval_bytes).decode('ascii'),
        'artifact_inventory': {row['role']: {'path': row['path'], 'sha256': row['sha256']}
                               for row in contract_doc['artifacts']},
        'path': list(session_ids), 'horizon_sessions': len(block),
        'result': {'labels': sorted(labels), 'r1': runs['r1'], 'r2': runs['r2']},
    }


def main():
    if _STATE is None:
        _fail('P7_BOOTSTRAP_MISMATCH: the driver runs only under the pinned bootstrap')
    from c1_rail.qualification import p7_evidence
    if _STATE.bootstrap_sha256 != p7_evidence.P7_BOOTSTRAP_SHA256:
        _fail('P7_BOOTSTRAP_MISMATCH: bootstrap hash differs from the pinned constant')
    import uuid
    from datetime import datetime, timezone
    started = datetime.now(timezone.utc).isoformat()
    argv = sys.argv[1:8]
    try:
        fields = _run(p7_evidence, argv)
        fields.update(run_started_at=started, host_run_id=uuid.uuid4().hex)
        p7_evidence.finish_record(_STATE, fields, argv[6])
    except SystemExit:
        raise
    except BaseException as exc:  # every refusal leaves no record
        _fail('; '.join(list(_STATE.refusals) + [f'{type(exc).__name__}: {exc}']))


if __name__ == '__main__':
    main()
