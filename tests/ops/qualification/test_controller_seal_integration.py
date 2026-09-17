"""Controller receipts consumed by real G5; all authority and paths are fixtures."""
import json
from pathlib import Path

from c1_rail.qualification.attempt import AttemptStore
from c1_rail.qualification.model import PathOutcome
from c1_rail.qualification.orchestration import _execute_e1,canonical_bytes
from c1_rail.qualification.part_a import SyntheticPanelResult,SyntheticPartAResult
from c1_rail.qualification.preflight import preflight_binding_bytes
from c1_rail.qualification.result_adjudication import frozen_adjudicator
from c1_rail.qualification.runner import StageRun
from c1_rail.qualification.seal import validate_result_envelope
from test_seal import NOW,result_case,sha,outcome_digest,context


def test_real_controller_receipts_are_accepted_by_g5(tmp_path):
    frozen,raw,outputs,_,_,_,runtime,preflight,approval,keys=result_case()
    class Executor:
        def run_stage(self,stage,dispatch):
            store.consume_checkpoint_dispatch(dispatch)
            depth=frozen.stage_specs[stage.upper()].exact_depth
            rows=tuple(PathOutcome('PASS',1,None,()) for _ in range(depth))
            return StageRun(stage,tuple((name,rows) for name in ('FULL','H1','H2')),0.,0.,True)
        def run_part_a(self,dispatch,full_pass_rate):
            store.consume_checkpoint_dispatch(dispatch)
            rows=tuple(PathOutcome('PASS',1,None,()) for _ in range(frozen.replay.part_a.paths_per_population_per_panel))
            panels=tuple(SyntheticPanelResult(index,frozen.populations['FULL'],rows) for index in range(frozen.replay.part_a.initial_panels))
            return SyntheticPartAResult(panels,1.,1.,False,True,None,0.,0.,0.,True)
    store=AttemptStore.open(tmp_path/'journal.sqlite',campaign_id='attempt-1',
        contract_digest=frozen.contract_sha256,trust_domain_sha256=frozen.trust_domain_sha256,
        boot_id='boot-1',now=NOW)
    result=_execute_e1(frozen,store=store,executor=Executor(),
        preflight_binding=preflight_binding_bytes(preflight),
        exact_depth_approval_sha256=preflight.exact_depth_approval.approval_sha256,
        now=lambda:NOW,synthetic=True)
    document=json.loads(raw)
    document['path_inventory_sha256']=sha(result.path_inventory_bytes)
    document['attempt_journal_sha256']=sha(store.path.read_bytes())
    for row in document['stage_results']:
        row['input_sha256']=dict(result.stage_input_sha256)[row['stage']]
        row['output_sha256']=outcome_digest(result.path_outcomes[row['stage']])
    for role,payload in outputs.items():
        (Path(preflight.output_root)/f'{role}.bin').write_bytes(payload)
    validated=validate_result_envelope(frozen,canonical_bytes(document),
        path_outcomes=result.path_outcomes,path_inventory_bytes=result.path_inventory_bytes,
        attempt_store=store,runtime_load_trace_bytes=runtime,preflight_receipt=preflight,
        exact_depth_approval_bytes=approval,exact_depth_trusted_keys=keys,approval_now=NOW,
        stage_input_sha256=dict(result.stage_input_sha256),
        adjudicator=frozen_adjudicator(
            frozen,retained_source_bytes=context(frozen).retained_source_bytes,
            runtime_inventory=context(frozen).runtime_inventory),
        trust_domain=frozen.trust_domain)
    assert validated.verdict=='PASS'
