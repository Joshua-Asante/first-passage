"""Semantic inputs only: no signatures or execution authority."""
from test_contract import _document
from c1_rail.qualification.trust_domain import QualificationWorkloadPolicy


def semantic_case():
    from c1_rail.qualification.policy import parse_policy
    from c1_rail.qualification.policy_sources import build_qualification_policy
    document = _document()
    policy = parse_policy(build_qualification_policy())
    document['schema'] = 'frozen_qualification_contract/v2'
    document['policy_sha256'] = policy.sha256
    document['result_plan'] = {
        'policy_sha256': policy.sha256,
        'adjudicator_closure_sha256': document['result_plan']['adjudicator_closure_sha256'],
    }
    replay = document['replay']
    workload = QualificationWorkloadPolicy(
        {row['name']: row['population_counts'] for row in replay['stages']},
        replay['horizon_sessions'], replay['inner_block_sessions'], replay['outer_months'],
        replay['part_a']['initial_panels'], replay['part_a']['expanded_panels'],
        replay['part_a']['paths_per_population_per_panel'])
    return document, policy, workload


def stage_case(stage='N1', *, passing=True):
    """Consistency-only outcome bytes; never a completed execution fixture."""
    import hashlib
    from types import SimpleNamespace
    from test_orchestration import contract
    from c1_rail.qualification.contract import canonical_json_bytes
    from c1_rail.qualification.orchestration import seed_input
    from c1_rail.qualification.policy import parse_policy
    from c1_rail.qualification.policy_sources import build_qualification_policy
    c = contract()
    c.trust_domain = SimpleNamespace(permits_synthetic=True)
    p = parse_policy(build_qualification_policy())
    order = ('FULL','H1','H2') if stage == 'N1' else ('FULL',) if stage == 'N2' else ('H1','H2') if stage == 'PART_B' else ('REGIME',)
    populations, records = [], []
    for population in order:
        depth = c.stage_specs[stage].exact_depth
        count = depth * c.replay.part_a.initial_panels if stage == 'PART_A' else depth
        rows = []
        for index in range(count):
            row = dict(status='PASS' if passing else 'UNRESOLVED', sessions_to_pass=1 if passing else None,
                       failure_reason=None if passing else 'horizon_cap', diagnostics=[['source','consistency-only']])
            rows.append(row)
            panel = index // depth if stage == 'PART_A' else None
            path = index % depth if stage == 'PART_A' else index
            seed = seed_input(c, stage='n1' if stage == 'N1' else 'n2', population='FULL' if stage == 'PART_A' else population,
                              panel_index=panel, path_index=path, synthetic=True)
            records.append(dict(stage=stage, population=population, path_index=path,
                                panel_id=None if panel is None else hashlib.sha256(str(panel).encode()).hexdigest(),
                                seed_input_sha256=seed.sha256, outcome_sha256=hashlib.sha256(canonical_json_bytes(row)).hexdigest()))
        populations.append(dict(population=population, outcomes=rows))
    inventory = dict(schema='qualification_path_inventory/v1', trust_domain_sha256=c.trust_domain_sha256, records=records)
    return c, p, canonical_json_bytes(populations), canonical_json_bytes(inventory)
