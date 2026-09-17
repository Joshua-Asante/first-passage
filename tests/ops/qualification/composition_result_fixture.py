"""Serialize actual synthetic controller evidence for the real G5 consumer."""
import hashlib
from pathlib import Path

from c1_rail.qualification.contract import canonical_json_bytes


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def normalized_outcomes(populations):
    return {population:[{'status':row.status,'sessions_to_pass':row.sessions_to_pass,
        'failure_reason':row.failure_reason,'diagnostics':[list(item) for item in row.diagnostics]}
        for row in rows] for population,rows in populations.items()}


def retained_result_envelope(contract,execution,store,preflight):
    """No invented outcomes: every stage count/digest comes from the controller."""
    outcomes={stage:normalized_outcomes(populations)
              for stage,populations in execution.path_outcomes.items()}
    private=canonical_json_bytes({'trust_domain_sha256':contract.trust_domain_sha256,
                                 'evidence_class':'TEST_ONLY','outcomes':outcomes})
    public=canonical_json_bytes({'trust_domain_sha256':contract.trust_domain_sha256,
                                'evidence_class':'TEST_ONLY','production_authority':False})
    outputs={'private-result':private,'public-projection':public}
    if set(outputs)!=set(contract.required_output_roles):
        raise ValueError('composition fixture output roles differ from signed plan')
    declarations=[]
    for role,raw in outputs.items():
        relative=role+'.json'
        (Path(preflight.output_root)/relative).write_bytes(raw)
        declarations.append({'role':role,'path':relative,'sha256':sha(raw),'byte_length':len(raw),
            'privacy':'PRIVATE' if role=='private-result' else 'PUBLIC_PROJECTION'})
    runtime=canonical_json_bytes(dict(contract.runtime_load_sha256))
    inputs=dict(execution.stage_input_sha256)
    decisions=dict(execution.decisions)
    stages=[]
    for stage,populations in execution.path_outcomes.items():
        counts={population:len(rows) for population,rows in populations.items()}
        if stage=='PART_A':
            counts={population:count//contract.replay.part_a.paths_per_population_per_panel
                    for population,count in counts.items()}
        stages.append({'stage':stage,'status':decisions[stage],
            'input_sha256':inputs[stage],'output_sha256':sha(canonical_json_bytes(outcomes[stage])),
            'population_counts':counts})
    document={'schema':'qualification_result_envelope/v1','attempt_id':store.campaign_id,
        'contract_sha256':contract.contract_sha256,'trust_domain_sha256':contract.trust_domain_sha256,
        'shared_manifest_sha256':next(a.sha256 for a in contract.artifacts if a.role=='shared_manifest'),
        'exact_depth_approval_sha256':preflight.exact_depth_approval.approval_sha256,
        'producer':{'producer_id':'TEST_ONLY-composition','boot_id':store.boot_id,
            'tool_sha256':contract.runtime_load_sha256['qualification_runner'],
            'runtime_sha256':contract.runtime_load_sha256['runtime_distribution']},
        'started_utc':'2026-09-15T19:00:00Z','completed_utc':'2026-09-15T19:30:00Z',
        'completion':'COMPLETE','verdict':'PASS' if execution.passed else 'FAIL',
        'terminal_reason':None if execution.passed else 'TEST_ONLY_TERMINAL',
        'stage_results':stages,'outputs':declarations,
        'path_inventory_sha256':sha(execution.path_inventory_bytes),
        'runtime_load_trace_sha256':sha(runtime),'attempt_journal_sha256':sha(store.path.read_bytes()),
        'previous_result_sha256':None}
    return canonical_json_bytes(document),runtime
