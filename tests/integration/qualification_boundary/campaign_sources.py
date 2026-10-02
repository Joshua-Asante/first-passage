"""S8 synthetic source scenarios for the integrated full-E1 campaign (TEST_ONLY).

Each scenario is an actual synthetic market/session source: the composition
fixture's signed ORB port, optionally idle on every session or on a declared
pair of source session dates. Nothing here supplies PathOutcome, StageRun,
adjudication, capture or a receipt; verdicts come only from replaying these
sources through the frozen engine (``establish_verdict``) or the installed
route. The expected verdicts are declared in test_full_campaign_boundary.py,
before any admission.

Idle-pair derivation (recorded on the composition fixture at the Linux depth:
N1 2, N2 FULL/H1/H2 60, horizon 5, inner block 5). Every trading path passes
on its fourth winning session, so one idle session leaves a path PASS (day 5)
and two idle sessions leave it UNRESOLVED; at depth 60 the joint rule
tolerates no failure (max_certifying_busts(60, 0.05, 0.05) == 0) and N1
tolerates none (int(2 * 0.05) == 0). A pair therefore fails exactly the paths
that contain both dates:

- ``n2_full_fails``: 2024-01-16 and 2024-01-19 share exactly one N2 FULL path,
  no N2 H1/H2 path and no N1 path. FULL fails, both halves pass.
- ``n2_halves_fail``: 2024-01-08 and 2024-01-12 share one N2 H1 path, no N2
  FULL or H2 path and no N1 path. FULL passes (one idle session at most),
  H1 fails.
- ``part_a_below_floor``: the S5 producer's own pair
  (fixture_producer.PART_A_BELOW_FLOOR_IDLE_DATES); only Part A panel 1, path 0
  contains both.

``path_inventory`` recomputes these placements from the real samplers without
replaying any path; ``establish_verdict`` replays the actual engine. Any change
to seeds, calendar or samplers fails those checks before a host is used. The
engine and fixture imports are deferred so the administrator wrapper
(fixture_install_s8.py) needs only ``port_transform``.
"""
# pylint: disable=import-outside-toplevel,protected-access
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import itertools
from pathlib import Path

ORB_LEG = 'orb_mnq_v7'
ORB_ROLE = 'orb_runtime_port'


@dataclass(frozen=True)
class SourceScenario:
    """One declared source: idle everywhere, idle on a date pair, or trading.

    ``producer`` names the installed bundle producer: 'fixture_install' takes
    the idle variant and its own SCENARIOS; 'derived' needs fixture_install_s8.
    """
    name: str
    idle: bool
    idle_dates: tuple[str, ...]
    producer: str


SCENARIOS = {
    'trading': SourceScenario('trading', False, (), 'fixture_install'),
    'idle': SourceScenario('idle', True, (), 'fixture_install'),
    'n2_full_fails': SourceScenario('n2_full_fails', False, ('2024-01-16', '2024-01-19'),
                                    'derived'),
    'n2_halves_fail': SourceScenario('n2_halves_fail', False, ('2024-01-08', '2024-01-12'),
                                     'derived'),
    'part_a_below_floor': SourceScenario('part_a_below_floor', False,
                                         ('2024-04-15', '2024-04-17'), 'fixture_install'),
}
DERIVED = tuple(name for name, row in SCENARIOS.items() if row.producer == 'derived')

# The S5 producer's exact entry branch and guard (fixture_producer.scenario_port_transform);
# test_full_campaign_boundary pins byte parity with it for the shared scenario.
_ENTRY = b"        if local.hour == 9 and local.minute == 0 and not self.position:\n"
_GUARDED = (b"        if (local.hour == 9 and local.minute == 0 and not self.position\n"
            b"                and local.date().isoformat() not in _IDLE_SOURCE_DATES):\n")


def scenario(name):
    """The registered scenario, or a refusal."""
    if name not in SCENARIOS:
        raise ValueError('unknown S8 source scenario')
    return SCENARIOS[name]


def port_transform(name):
    """The signed synthetic ORB program for one scenario, or None for no change."""
    row = scenario(name)
    if not row.idle_dates:
        return None
    tail = ('\n_IDLE_SOURCE_DATES = frozenset(' + repr(row.idle_dates) + ')\n').encode()

    def transform(leg, raw):
        if leg != ORB_LEG:
            return raw
        if raw.count(_ENTRY) != 1:
            raise ValueError('synthetic port entry branch differs')
        return raw.replace(_ENTRY, _GUARDED) + tail
    return transform


def source_identity(name, root):
    """sha256 of the scenario's ORB runtime port: the admitted source identity."""
    from composition_fixture import build_artifacts
    row = scenario(name)
    fixture = build_artifacts(Path(root), idle=row.idle, port_transform=port_transform(name))
    return hashlib.sha256(fixture.payloads[ORB_ROLE]).hexdigest()


def build_scenario_composition(root, name):
    """composition_fixture.build_verified_composition with the scenario's port."""
    import sys
    from test_contract import NOW
    from composition_fixture import (PORT_ROLES, VerifiedComposition, build_artifacts,
                                     contract_document, digest, encoded, signed_approval,
                                     verified_domain)
    from c1_rail.qualification.contract import ObservedBindings, validate_frozen_contract
    from c1_rail.qualification.production_source import ProductionSource
    from c1_rail.qualification.runtime_inventory import collect_runtime_inventory
    row = scenario(name)
    root = Path(root)
    fixture = build_artifacts(root, idle=row.idle, port_transform=port_transform(name))
    fixture = fixture.with_runtime_artifacts(root)
    domain, private, keys = verified_domain(fixture)
    raw = encoded(contract_document(fixture, domain))
    approval = signed_approval(raw, private['test-freeze'], key_id='test-freeze',
                               scope='FREEZE_F1')
    retained = {role: (root / path).read_bytes() for role, path in fixture.paths.items()}
    observed = ObservedBindings(
        artifact_sha256={fixture.paths[r]: digest(b) for r, b in retained.items()},
        runtime_load_sha256={r: digest(b) for r, b in retained.items()},
        effective_settings_sha256=digest(retained['effective_settings_successor']),
        orb_normal_base=1)
    contract = validate_frozen_contract(raw, approval, keys, observed, now=NOW,
                                        trust_domain=domain)
    source = ProductionSource._build_composition(contract, artifact_root=root)
    modules = {module.role: module.module for module in fixture.ordinary_modules}
    modules.update({role: sys.modules['fp_qualification_port_' + leg]
                    for leg, role in PORT_ROLES.items()})
    inventory = collect_runtime_inventory(contract, loaded_modules=modules,
                                          retained_source_bytes=retained, artifact_root=root)
    return VerifiedComposition(fixture, domain, contract, source, private, keys, modules,
                               retained, raw, approval, inventory)


def path_inventory(contract, source):
    """Source session dates of every N1/N2 path, sampled exactly as the engine
    samples them (domain seeds, candidate blocks), without replaying a path."""
    from random import Random
    from c1_rail.qualification.provider import _ReplayProvider
    from c1_rail.qualification.regime import domain_seed
    provider = _ReplayProvider(source.sessions, source.adjacent,
                               block_sessions=contract.replay.inner_block_sessions,
                               path_start_date=source.path_start_date, replay=source.replay)
    synthetic = contract.trust_domain.permits_synthetic
    horizon = contract.replay.horizon_sessions
    specs = contract.stage_specs

    def dates(stage, population, index):
        seed = domain_seed(root=contract.replay.root_rng_namespace, stage=stage,
                           population=population, panel_index=None, path_index=index,
                           synthetic=synthetic)
        path = provider.assembler.sample(provider.candidates[population], Random(seed),
                                         horizon_sessions=horizon)
        return tuple(row.source.source_session_date.isoformat() for row in path)
    half = specs['PART_B'].exact_depth
    depths = {'n1': {name: specs['N1'].exact_depth for name in ('FULL', 'H1', 'H2')},
              'n2': {'FULL': specs['N2'].exact_depth, 'H1': half, 'H2': half}}
    return {stage: {population: tuple(dates(stage, population, index) for index in range(depth))
                    for population, depth in by_population.items()}
            for stage, by_population in depths.items()}


def co_occurrences(inventory, pair):
    """How many paths per (stage, population) contain both dates of ``pair``."""
    wanted = set(pair)
    return {(stage, population): sum(wanted <= set(path) for path in paths)
            for stage, by_population in inventory.items()
            for population, paths in by_population.items()}


def isolated_pairs(inventory, *, inside, outside):
    """Date pairs present together in some ``inside`` path and in no ``outside``
    path (each a (stage, population) key) -- the derivation of DERIVED pairs."""
    def pairs(keys):
        found = set()
        for stage, population in keys:
            for path in inventory[stage][population]:
                found.update(itertools.combinations(sorted(set(path)), 2))
        return found
    return sorted(pairs(inside) - pairs(outside))


def establish_verdict(root, name):
    """Replay one scenario through the frozen engine: the checkpoint compute
    adapters (run_n1/n2/part_a_compute) and the canonical replay adjudicator.

    Returns the stage statuses in result-aggregate vocabulary plus the Part A
    facts. Stops at the first failed checkpoint exactly as the route does.
    """
    from c1_rail.qualification.execution import compute
    from c1_rail.qualification.execution.budget import BudgetGuard
    from c1_rail.qualification.result_adjudication import adjudicate_replay_outcomes
    setup = build_scenario_composition(root, name)
    contract, source = setup.contract, setup.source

    def guard():
        return BudgetGuard.from_contract(contract)
    outcomes = {'N1': dict(compute.run_n1_compute(contract, source, guard()).populations)}
    stages = {'LEGALITY': 'PASS', **adjudicate_replay_outcomes(contract, outcomes, None)}
    part_a = None
    if stages['N1'] == 'PASS':
        joint = dict(compute.run_n2_compute(contract, source, guard()).populations)
        outcomes.update(N2={'FULL': joint['FULL']}, PART_B={'H1': joint['H1'], 'H2': joint['H2']})
        stages = {'LEGALITY': 'PASS', **adjudicate_replay_outcomes(contract, outcomes, None)}
        if stages['N2'] == 'PASS' and stages['PART_B'] == 'PASS':
            run = compute.run_part_a_compute(
                contract, source, guard(),
                n2_full_outcomes=tuple(row.status for row in joint['FULL']))
            result = run.result
            stages['PART_A'] = 'PASS' if result.passed else 'FAIL'
            initial = run.initial_panel_bytes
            part_a = {'expansion_required': run.expansion_required,
                      'final_panels': run.final_panels,
                      'failure_reason': result.failure_reason,
                      'prefix_preserved': run.final_panel_bytes[:len(initial)] == initial}
    return {'stages': stages, 'part_a': part_a}
