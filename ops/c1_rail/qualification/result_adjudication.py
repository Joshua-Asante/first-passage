"""Deterministic result decisions from retained per-path evidence."""
from decimal import Decimal, ROUND_CEILING
from types import SimpleNamespace
from dataclasses import dataclass
from dataclasses import field, Field
from dataclasses import is_dataclass
from collections.abc import Mapping
from enum import Enum
from datetime import date, timedelta
from pathlib import Path
import hashlib
import __future__
import json
import marshal
import sys
from types import FunctionType, ModuleType, MemberDescriptorType, GetSetDescriptorType
from typing import TypeVar, get_args, get_origin
from fractions import Fraction
import re

from scripts.certification_power import max_certifying_busts, min_certifying_passes
from .adjudication import DecisionRules, adjudicate_stage

from .model import PathOutcome
from .runtime_inventory import RuntimeInventoryReceipt, revalidate_runtime_inventory


def _closure_identity(sources):
    subject={'schema':'qualification-adjudicator-closure/v1','sources':dict(sources)}
    return hashlib.sha256(json.dumps(subject,sort_keys=True,separators=(',',':'),
                                    ensure_ascii=False,allow_nan=False).encode()).hexdigest()


def _code_identity(function):
    return hashlib.sha256(marshal.dumps(function.__code__)).hexdigest()


def _runtime_dependencies():
    return (
        ('adjudicate_e1_outcomes', adjudicate_e1_outcomes),
        ('adjudicate_panel_inventory', adjudicate_panel_inventory),
        ('adjudicate_stage', adjudicate_stage),
        ('max_certifying_busts', max_certifying_busts),
        ('min_certifying_passes', min_certifying_passes),
        ('DecisionRules', DecisionRules),
        ('PathOutcome', PathOutcome),
    )



def _same_executable_value(actual, expected, module_globals, reference_globals, seen):
    """Compare retained definitions, including generated dataclass methods."""
    pair = (id(actual), id(expected))
    if pair in seen:
        return True
    seen.add(pair)
    if isinstance(expected, Enum):
        return (isinstance(actual, Enum) and actual.name == expected.name
                and _same_executable_value(type(actual), type(expected), module_globals, reference_globals, seen)
                and _same_executable_value(actual.value, expected.value, module_globals, reference_globals, seen))
    if not isinstance(expected, type) and is_dataclass(expected):
        return (is_dataclass(actual)
                and _same_executable_value(type(actual), type(expected), module_globals, reference_globals, seen)
                and _same_executable_value(vars(actual), vars(expected), module_globals, reference_globals, seen))
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, TypeVar):
        return all(_same_executable_value(getattr(actual, key), getattr(expected, key),
                                         module_globals, reference_globals, seen)
                   for key in ('__name__', '__bound__', '__constraints__',
                               '__covariant__', '__contravariant__'))
    if isinstance(expected, re.Pattern):
        return (actual.pattern, actual.flags) == (expected.pattern, expected.flags)
    if get_origin(expected) is not None:
        return (get_origin(actual) is get_origin(expected)
                and _same_executable_value(get_args(actual), get_args(expected),
                                           module_globals, reference_globals, seen))
    if isinstance(expected, FunctionType):
        if actual.__code__ != expected.__code__:
            return False
        expected_globals = (module_globals if expected.__globals__ is reference_globals
                            else expected.__globals__)
        if actual.__globals__ is not expected_globals:
            return False
        if not _same_executable_value(actual.__defaults__, expected.__defaults__,
                                      module_globals, reference_globals, seen):
            return False
        if not _same_executable_value(actual.__kwdefaults__, expected.__kwdefaults__,
                                      module_globals, reference_globals, seen):
            return False
        left, right = actual.__closure__ or (), expected.__closure__ or ()
        provenance_registry = (
            reference_globals['__name__'] == 'c1_rail.qualification.seal'
            and expected.__qualname__ in (
                '_validation_provenance_registry.<locals>.register',
                '_validation_provenance_registry.<locals>.require'))
        executor_registry = (
            reference_globals['__name__'] == 'c1_rail.qualification.production'
            and expected.__qualname__ in (
                '_executor_registry.<locals>.register',
                '_executor_registry.<locals>.lookup'))
        return len(left) == len(right) and all(
            (type(a.cell_contents) is dict and type(b.cell_contents) is dict)
            if (provenance_registry or executor_registry) and key == 'issued' else _same_executable_value(
                a.cell_contents, b.cell_contents, module_globals, reference_globals, seen)
            for key, a, b in zip(expected.__code__.co_freevars, left, right))
    if isinstance(expected, type):
        if expected.__module__ != reference_globals['__name__']:
            return actual is expected
        if (actual.__module__, actual.__qualname__) != (
                expected.__module__, expected.__qualname__) or not _same_executable_value(
                    actual.__bases__, expected.__bases__, module_globals, reference_globals, seen):
            return False
        # Inspect raw namespaces, never invoking descriptors. Generated layout
        # entries still participate: an injected data descriptor shadows instance
        # fields even when every method's bytecode remains unchanged.
        left, right = vars(actual), vars(expected)
        return left.keys() == right.keys() and all(_same_executable_value(
            left[name], value, module_globals, reference_globals, seen)
            if name != '_abc_impl' else (type(left[name]) is type(value)
                                        and type(value).__module__ == '_abc')
            for name, value in right.items())
    if isinstance(expected, (MemberDescriptorType, GetSetDescriptorType)):
        return (actual.__name__ == expected.__name__ and _same_executable_value(
            actual.__objclass__, expected.__objclass__, module_globals, reference_globals, seen))
    if isinstance(expected, Field) or type(expected).__name__ == '_DataclassParams':
        return all(_same_executable_value(getattr(actual, name), getattr(expected, name),
            module_globals, reference_globals, seen) for name in type(expected).__slots__)
    if isinstance(expected, (staticmethod, classmethod)):
        return _same_executable_value(actual.__func__, expected.__func__,
                                      module_globals, reference_globals, seen)
    if isinstance(expected, property):
        return all(_same_executable_value(getattr(actual, name), getattr(expected, name),
                                         module_globals, reference_globals, seen)
                   for name in ('fget', 'fset', 'fdel'))
    if isinstance(expected, (tuple, list)):
        return len(actual) == len(expected) and all(_same_executable_value(
            a, b, module_globals, reference_globals, seen) for a, b in zip(actual, expected))
    if isinstance(expected, Mapping):
        return actual.keys() == expected.keys() and all(_same_executable_value(
            actual[name], value, module_globals, reference_globals, seen)
            for name, value in expected.items())
    if isinstance(expected, (str, int, float, bool, bytes, set, frozenset, date, timedelta, Decimal, Fraction, Path)) or expected is None:
        return actual == expected
    return actual is expected


def _verify_retained_executable_modules(by_module, required_modules, decision_modules):
    """Detect drift in frozen code modules against retained definitions.

    This is not isolation from arbitrary code in this interpreter and does not
    prove that these definitions remained unchanged during an earlier execution.

    Evaluating module definitions in a private namespace reconstructs functions
    and dataclass constructors from verified bytes. It never replaces live
    modules or executes a qualification path. All frozen modules' functions,
    classes, defaults and imported executable bindings are checked. Decision
    globals are checked, with explicit exceptions for mutable issuance and lock
    state. Policy constants and configuration containers are never exempted.
    """
    for name in required_modules:
        module = sys.modules[name]
        row = by_module[name]
        live = vars(module)
        reference = {'__name__': name, '__package__': module.__package__,
                     '__file__': module.__file__}
        # Compile the complete module: conditional imports affect generated
        # bytecode too. Registries are reconstructed privately, never installed.
        flags = __future__.annotations.compiler_flag if name.startswith('fp_qualification_port_') else 0
        exec(compile(row.source_bytes, module.__file__, 'exec', flags=flags,
                     dont_inherit=True), reference)
        for key, expected in reference.items():
            if key.startswith('__'):
                continue
            state_globals = {
                'c1_rail.qualification.contract': {'_ISSUED_CONTRACTS'},
                'c1_rail.qualification.trust_domain': {'_ISSUED'},
                'c1_rail.qualification.production': {'_ISSUED_EXECUTORS'},
                'c1_rail.qualification.production_source': {'_SOURCE_ISSUED', '_SOURCE_TOKEN'},
                'c1_rail.qualification.attempt': {'_VALIDATED_RESULT_TOKEN'},
                'c1_rail.book_account_lock': {'_REGISTRY', '_REGISTRY_LOCK'},
                'c1_signal_daemon.m1_stage1_state': {'_mutexes', '_mutex_guard'},
            }
            if key in state_globals.get(name, ()) and key in live and type(live[key]) is type(expected):
                continue
            if key not in live or not _same_executable_value(
                    live[key], expected, live, reference, set()):
                raise ValueError(f'runtime dependency executable differs from retained source: {name}.{key}')
        # A newly injected global can shadow a builtin consumed by verified code.
        if any(key not in reference and not key.startswith('__')
               and not (isinstance(value, ModuleType) and value.__name__ == name + '.' + key
                        and sys.modules.get(value.__name__) is value)
               for key, value in live.items()):
            raise ValueError(f'runtime dependency globals differ from retained source: {name}')


def _verify_runtime_inventory(contract, receipt, dependencies):
    if type(receipt) is not RuntimeInventoryReceipt:
        raise ValueError('collector-issued runtime inventory receipt required')
    if (receipt.contract_sha256 != contract.contract_sha256
            or dict(receipt.runtime_load_sha256) != dict(contract.runtime_load_sha256)):
        raise ValueError('runtime inventory contract binding differs')
    by_module = {row.module_name: row for row in receipt.modules}
    if len(by_module) != len(receipt.modules):
        raise ValueError('runtime inventory module names are not unique')
    domain = getattr(contract, 'trust_domain', None)
    if domain is not None and {row.role: row.module_name for row in receipt.modules} != dict(domain.runtime_code_roles):
        raise ValueError('runtime inventory code roles differ from frozen trust domain')
    required_modules = {value.__module__ for _, value in dependencies}
    decision_modules = set(required_modules)
    if not required_modules.issubset(by_module):
        raise ValueError('runtime inventory omits adjudicator dependency modules')
    required_modules = set(by_module)
    own = by_module.get(__name__)
    if own is None or own.role != 'qualification_adjudicator':
        raise ValueError('runtime inventory adjudicator role differs')
    observed_origins = set()
    for module_name in required_modules:
        row = by_module[module_name]
        module = sys.modules.get(module_name)
        if type(module) is not ModuleType:
            raise ValueError('runtime inventory dependency module is not loaded')
        module_file = Path(getattr(module, '__file__', ''))
        if not module_file.is_absolute() and module_name.startswith('fp_qualification_port_'):
            artifact = next(item for item in contract.artifacts if item.role == row.role)
            if module_file.as_posix() != Path(artifact.path).as_posix():
                raise ValueError('runtime inventory port origin differs')
            origin = Path(row.origin).resolve(strict=True)
        else:
            origin = module_file.resolve(strict=True)
        if origin != Path(row.origin).resolve(strict=True) or str(origin) in observed_origins:
            raise ValueError('runtime inventory dependency origin differs or aliases')
        observed_origins.add(str(origin))
        source = origin.read_bytes()
        digest = hashlib.sha256(source).hexdigest()
        if (source != row.source_bytes or digest != row.sha256
                or dict(contract.runtime_load_sha256).get(row.role) != digest):
            raise ValueError('runtime inventory dependency source differs')
    for _, value in dependencies:
        module = sys.modules[value.__module__]
        if (isinstance(value, FunctionType) and value.__globals__ is not vars(module)):
            raise ValueError('runtime dependency globals differ from observed module')
        if getattr(module, value.__name__, None) is not value:
            raise ValueError('runtime dependency object differs from observed module')
    if domain is not None:
        # A receipt is source data, not an issuance capability. Recollect the
        # actual import closure instead of trusting its declared edge list.
        revalidate_runtime_inventory(contract, receipt)
    _verify_retained_executable_modules(by_module, required_modules, decision_modules)


@dataclass(frozen=True)
class FrozenAdjudicator:
    """Concrete dispatcher; G5 also requires its validated contract exact type.

    This is not an independent authority token. Each consuming boundary checks
    this exact implementation type and calls verify_for with its G1 contract.
    G1 owns runtime inventory completeness and observed module-load provenance.
    """
    contract: object
    contract_sha256: str
    identity_sha256: str
    source_sha256: tuple[tuple[str,str], ...]
    _entrypoint: object = field(repr=False, compare=False)
    _dependencies: tuple[tuple[str, object, str | None], ...] = field(repr=False, compare=False)
    _runtime_inventory: RuntimeInventoryReceipt = field(repr=False, compare=False)

    def verify_for(self, contract):
        if (type(self) is not FrozenAdjudicator or self.contract is not contract
                or self.contract_sha256!=contract.contract_sha256):
            raise ValueError('dispatcher contract binding differs')
        if dict(self.source_sha256)!=dict(contract.runtime_load_sha256):
            raise ValueError('dispatcher runtime source inventory differs')
        if (self.identity_sha256!=_closure_identity(self.source_sha256)
                or self.identity_sha256!=contract.adjudicator_sha256):
            raise ValueError('dispatcher source closure identity differs')
        own=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        if dict(self.source_sha256).get('qualification_adjudicator')!=own:
            raise ValueError('dispatcher implementation source differs')
        if self._entrypoint is not adjudicate_e1_outcomes:
            raise ValueError('dispatcher entrypoint object differs')
        current = {
            'adjudicate_e1_outcomes': adjudicate_e1_outcomes,
            'adjudicate_panel_inventory': adjudicate_panel_inventory,
            'adjudicate_stage': adjudicate_stage,
            'max_certifying_busts': max_certifying_busts,
            'min_certifying_passes': min_certifying_passes,
        }
        _verify_runtime_inventory(contract, self._runtime_inventory,
                                  tuple((name, value) for name, value, _ in self._dependencies))
        current.update({'DecisionRules': DecisionRules, 'PathOutcome': PathOutcome})
        for name, function, code_sha256 in self._dependencies:
            if (current.get(name) is not function
                    or (code_sha256 is not None and _code_identity(function) != code_sha256)):
                raise ValueError('dispatcher loaded dependency identity differs')
        if _code_identity(self._entrypoint) != dict(
                (name, digest) for name, _, digest in self._dependencies
                ).get('adjudicate_e1_outcomes'):
            raise ValueError('dispatcher loaded entrypoint code differs')

    def __call__(self,outcomes,inventory):
        self.verify_for(self.contract)
        return self._entrypoint(self.contract,outcomes,inventory)


def frozen_adjudicator(contract, *, retained_source_bytes, runtime_inventory):
    """Bind every retained G1 runtime role, refusing omissions or byte drift."""
    if set(retained_source_bytes)!=set(contract.runtime_load_sha256):
        raise ValueError('complete retained runtime source inventory required')
    if any(type(raw) is not bytes for raw in retained_source_bytes.values()):
        raise ValueError('immutable retained source bytes required')
    observed={name:hashlib.sha256(raw).hexdigest() for name,raw in retained_source_bytes.items()}
    if observed!=dict(contract.runtime_load_sha256):
        raise ValueError('retained runtime source bytes differ')
    functions=_runtime_dependencies()
    _verify_runtime_inventory(contract, runtime_inventory, functions)
    result=FrozenAdjudicator(
        contract,contract.contract_sha256,_closure_identity(observed),
        tuple(sorted(observed.items())),adjudicate_e1_outcomes,
        tuple((name,function,_code_identity(function)
               if isinstance(function, FunctionType) else None)
              for name,function in functions),runtime_inventory,
    )
    result.verify_for(contract)
    return result


def adjudicate_e1_outcomes(contract, outcomes, inventory):
    """Pure decision adapter; authority and exact counts are G1/G5 boundaries."""
    order=('LEGALITY','N1','N2','PART_B','PART_A')
    if tuple(outcomes)!=order[:len(outcomes)] or not outcomes or outcomes['LEGALITY']!={}:
        raise ValueError('ordered E1 stage prefix required')
    return {'LEGALITY': 'PASS', **adjudicate_replay_outcomes(
        contract, {name: rows for name, rows in outcomes.items() if name != 'LEGALITY'}, inventory)}


def adjudicate_replay_outcomes(contract, outcomes, inventory):
    """Unchanged replay decisions, without supplying a legality assertion."""
    order = ('N1', 'N2', 'PART_B', 'PART_A')
    if tuple(outcomes) != order[:len(outcomes)]:
        raise ValueError('ordered replay stage prefix required')
    frozen=contract.replay.decision_rules
    rules=DecisionRules(frozen.failure_ceiling,frozen.alpha,
                        frozen.speed_target,frozen.speed_horizon_sessions)
    decisions={}
    if 'N1' in outcomes:
        run=SimpleNamespace(stage='n1',populations=tuple(outcomes['N1'].items()))
        decisions['N1']='PASS' if adjudicate_stage(run,rules).status=='CONTINUE' else 'FAIL'
    def confirmed(rows):
        if type(rows) is not tuple or not rows or any(type(row) is not PathOutcome for row in rows):
            raise ValueError('typed immutable confirmation outcomes required')
        return sum(row.status!='PASS' for row in rows)<=max_certifying_busts(
            len(rows),rules.failure_ceiling,rules.alpha)
    if 'N2' in outcomes:
        if decisions['N1']!='PASS':
            raise ValueError('evidence continues after failed N1 screen')
        if set(outcomes['N2'])!={'FULL'}:
            raise ValueError('N2 requires only its designated FULL paths')
        full=outcomes['N2']['FULL']
        failure_ok=confirmed(full)
        speed=sum(row.status=='PASS' and row.sessions_to_pass<=rules.speed_horizon_sessions for row in full)
        minimum=min_certifying_passes(len(full),rules.speed_target,rules.alpha)
        decisions['N2']='PASS' if failure_ok and minimum>=0 and speed>=minimum else 'FAIL'
    if 'PART_B' in outcomes:
        if set(outcomes['PART_B'])!={'H1','H2'}:
            raise ValueError('Part B requires designated n2 half populations')
        checks=[confirmed(outcomes['PART_B'][name]) for name in ('H1','H2')]
        decisions['PART_B']='PASS' if all(checks) else 'FAIL'
    if 'PART_A' in outcomes:
        if decisions['N2']!='PASS' or decisions['PART_B']!='PASS':
            raise ValueError('evidence continues after failed joint N2/Part B batch')
        if set(outcomes['PART_A'])!={'REGIME'}:
            raise ValueError('Part A requires retained regime paths')
        full_rate=Decimal(sum(row.status=='PASS' for row in full))/len(full)
        decisions['PART_A']=adjudicate_panel_inventory(outcomes['PART_A']['REGIME'],inventory,
            spec=contract.replay.part_a,full_pass_rate=full_rate)
    return decisions


def adjudicate_panel_inventory(outcomes, inventory, *, spec, full_pass_rate):
    """Validate panel-major evidence and apply the frozen inverse-ECDF rule.

    The first initial_panels blocks are the retained initial run. No sorting of
    panel identities or selection by outcome occurs before expansion is tested.
    G5 separately verifies every seed/outcome digest and durable input binding.
    """
    if spec.percentile_method != 'INVERSE_ECDF_LEFT':
        raise ValueError('unsupported frozen percentile method')
    if type(outcomes) is not tuple or any(type(row) is not PathOutcome for row in outcomes):
        raise ValueError('typed immutable Part A outcomes required')
    depth=spec.paths_per_population_per_panel
    if type(depth) is not int or depth<=0 or len(outcomes)%depth:
        raise ValueError('complete frozen-depth panel blocks required')
    count=len(outcomes)//depth
    if count not in (spec.initial_panels,spec.expanded_panels):
        raise ValueError('frozen panel count required')
    records=[row for row in inventory['records'] if row['stage']=='PART_A']
    if len(records)!=len(outcomes):
        raise ValueError('complete panel path inventory required')
    seen=set()
    rates=[]
    for panel in range(count):
        block=records[panel*depth:(panel+1)*depth]
        identity=block[0]['panel_id']
        if not isinstance(identity,str) or not identity or identity in seen:
            raise ValueError('unique panel identities required')
        seen.add(identity)
        for index,row in enumerate(block):
            if row['panel_id']!=identity or row['path_index']!=index or row['population']!='REGIME':
                raise ValueError('ordered frozen-depth panel inventory required')
        passes=sum(row.status=='PASS' for row in outcomes[panel*depth:(panel+1)*depth])
        rates.append(Decimal(passes)/depth)
    def percentile(values):
        rank=int((spec.percentile*len(values)).to_integral_value(rounding=ROUND_CEILING))
        return sorted(values)[max(0,rank-1)]
    initial=percentile(rates[:spec.initial_panels])
    expand=abs(initial-spec.expansion_center_p5)<=spec.expansion_tolerance
    expected=spec.expanded_panels if expand else spec.initial_panels
    if count!=expected:
        raise ValueError('panel count differs from initial-prefix expansion decision')
    final=percentile(rates)
    return 'PASS' if final>=spec.expansion_center_p5 and final<=full_pass_rate else 'FAIL'
