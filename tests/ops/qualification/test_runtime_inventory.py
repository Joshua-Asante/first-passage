"""Source-free loaded-origin collector tests; no qualification authority."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from types import MappingProxyType

import pytest

from c1_rail.qualification.contract import ArtifactRecord, ValidatedFrozenContract
from c1_rail.qualification.runtime_inventory import collect_runtime_inventory
import c1_rail.qualification.runtime_inventory as inventory


def fixture(tmp_path,monkeypatch,sources,paths=None):
    monkeypatch.setattr(inventory,'REPOSITORY_ROOT',tmp_path)
    modules={};raw={};artifacts=[]
    for name,text in sources.items():
        relative=(paths or {}).get(name,'ops/'+name.replace('.','/')+'.py')
        path=tmp_path/relative;path.parent.mkdir(parents=True,exist_ok=True)
        source=text.encode();path.write_bytes(source)
        spec=importlib.util.spec_from_file_location(name,path)
        module=importlib.util.module_from_spec(spec)
        monkeypatch.setitem(sys.modules,name,module)
        spec.loader.exec_module(module)
        modules[name]=module;raw[name]=source
        artifacts.append(ArtifactRecord(name,relative,hashlib.sha256(source).hexdigest(),'fixture','TEST_ONLY'))
    raw['data']=b'fixture-data'
    artifacts.append(ArtifactRecord('data','data.json',hashlib.sha256(raw['data']).hexdigest(),'fixture','TEST_ONLY'))
    contract=object.__new__(ValidatedFrozenContract)
    object.__setattr__(contract,'contract_sha256','a'*64)
    object.__setattr__(contract,'artifacts',tuple(artifacts))
    object.__setattr__(contract,'runtime_load_sha256',MappingProxyType({a.role:a.sha256 for a in artifacts}))
    return contract,modules,raw


def test_actual_origins_sources_and_data_are_immutable(tmp_path,monkeypatch):
    contract,modules,raw=fixture(tmp_path,monkeypatch,{'c1_rail.fixture_root':'VALUE=7\n'})
    receipt=collect_runtime_inventory(contract,loaded_modules=modules,retained_source_bytes=raw)
    assert receipt.contract_sha256=='a'*64
    assert receipt.modules[0].module_name=='c1_rail.fixture_root'
    assert receipt.modules[0].source_bytes==raw['c1_rail.fixture_root']
    assert dict(receipt.runtime_load_sha256)==dict(contract.runtime_load_sha256)
    assert receipt.data_bindings[0].source_bytes==b'fixture-data'
    with pytest.raises((AttributeError,TypeError)):receipt.modules=()


def test_disk_drift_is_not_hidden_by_caller_retained_hash(tmp_path,monkeypatch):
    contract,modules,raw=fixture(tmp_path,monkeypatch,{'c1_rail.fixture_root':'VALUE=7\n'})
    (tmp_path/contract.artifacts[0].path).write_bytes(b'VALUE=8\n')
    with pytest.raises(ValueError,match='actual source'):
        collect_runtime_inventory(contract,loaded_modules=modules,retained_source_bytes=raw)


def test_same_origin_alias_is_rejected(tmp_path,monkeypatch):
    contract,modules,raw=fixture(tmp_path,monkeypatch,{'c1_rail.fixture_root':'VALUE=7\n'})
    monkeypatch.setitem(sys.modules,'ops.c1_rail.fixture_root',modules['c1_rail.fixture_root'])
    with pytest.raises(ValueError,match='alias'):
        collect_runtime_inventory(contract,loaded_modules=modules,retained_source_bytes=raw)


def test_imported_function_dependency_requires_its_own_role(tmp_path,monkeypatch):
    contract,modules,raw=fixture(tmp_path,monkeypatch,{
        'c1_rail.fixture_child':'def compute(): return 7\n',
        'c1_rail.fixture_root':'from c1_rail.fixture_child import compute\n'})
    root=contract.artifacts[1];data=contract.artifacts[2]
    object.__setattr__(contract,'artifacts',(root,data))
    object.__setattr__(contract,'runtime_load_sha256',MappingProxyType({a.role:a.sha256 for a in (root,data)}))
    with pytest.raises(ValueError,match='dependency.*inventory'):
        collect_runtime_inventory(contract,loaded_modules={'c1_rail.fixture_root':modules['c1_rail.fixture_root']},
                                  retained_source_bytes={key:raw[key] for key in (root.role,'data')})


def test_transitive_from_import_and_local_import_closure(tmp_path,monkeypatch):
    contract,modules,raw=fixture(tmp_path,monkeypatch,{
        'c1_rail.fixture_leaf':'def value(): return 7\n',
        'c1_rail.fixture_child':'from c1_rail.fixture_leaf import value\ndef compute(): return value()\n',
        'c1_rail.fixture_root':'def run():\n from c1_rail.fixture_child import compute\n return compute()\n'})
    receipt=collect_runtime_inventory(contract,loaded_modules=modules,retained_source_bytes=raw)
    assert len(receipt.modules)==3


def test_missing_loaded_code_or_retained_data_refuses(tmp_path,monkeypatch):
    contract,modules,raw=fixture(tmp_path,monkeypatch,{'c1_rail.fixture_root':'VALUE=7\n'})
    with pytest.raises(ValueError,match='code role'):
        collect_runtime_inventory(contract,loaded_modules={},retained_source_bytes=raw)
    with pytest.raises(ValueError,match='complete retained'):
        collect_runtime_inventory(contract,loaded_modules=modules,retained_source_bytes={})


def test_origin_must_equal_frozen_path_even_when_source_bytes_equal(tmp_path,monkeypatch):
    contract,modules,raw=fixture(tmp_path,monkeypatch,{'c1_rail.fixture_root':'VALUE=7\n'})
    alternate=tmp_path/'alternate.py';alternate.write_bytes(raw['c1_rail.fixture_root'])
    modules['c1_rail.fixture_root'].__file__=str(alternate)
    with pytest.raises(ValueError,match='origin'):
        collect_runtime_inventory(contract,loaded_modules=modules,retained_source_bytes=raw)


def test_actual_origin_source_is_read_once(tmp_path,monkeypatch):
    from pathlib import Path
    contract,modules,raw=fixture(tmp_path,monkeypatch,{'c1_rail.fixture_root':'VALUE=7\n'})
    calls=[];original=Path.read_bytes
    def read(path):
        calls.append(path)
        return original(path)
    monkeypatch.setattr(Path,'read_bytes',read)
    collect_runtime_inventory(contract,loaded_modules=modules,retained_source_bytes=raw)
    assert calls==[(tmp_path/contract.artifacts[0].path).resolve()]


def test_unloaded_deferred_first_party_import_cannot_claim_closure(tmp_path,monkeypatch):
    contract,modules,raw=fixture(tmp_path,monkeypatch,{
        'c1_rail.fixture_root':'def execute():\n from c1_rail.not_loaded import calculate\n return calculate()\n'})
    with pytest.raises(ValueError,match='dependency.*inventory'):
        collect_runtime_inventory(contract,loaded_modules=modules,retained_source_bytes=raw)


@pytest.mark.parametrize('statement', ['from . import child', 'from c1_rail.fixture_pkg import child'])
def test_unloaded_package_submodule_requires_inventory(tmp_path, monkeypatch, statement):
    package = 'c1_rail.fixture_pkg'
    contract, modules, raw = fixture(tmp_path, monkeypatch, {
        package: 'VALUE=7\n',
        package + '.root': f'def execute():\n {statement}\n return child.VALUE\n',
    }, paths={package: 'ops/c1_rail/fixture_pkg/__init__.py'})
    (tmp_path/'ops/c1_rail/fixture_pkg/child.py').write_text('VALUE=8\n')
    monkeypatch.delitem(sys.modules, package + '.child', raising=False)
    with pytest.raises(ValueError, match='dependency.*child.*inventory'):
        collect_runtime_inventory(contract, loaded_modules=modules, retained_source_bytes=raw)


def test_deferred_package_symbol_is_not_mistaken_for_submodule(tmp_path, monkeypatch):
    package = 'c1_rail.fixture_pkg'
    contract, modules, raw = fixture(tmp_path, monkeypatch, {
        package: 'VALUE=7\n',
        package + '.root': 'def execute():\n from . import VALUE\n return VALUE\n',
    }, paths={package: 'ops/c1_rail/fixture_pkg/__init__.py'})
    receipt = collect_runtime_inventory(contract, loaded_modules=modules, retained_source_bytes=raw)
    assert next(row for row in receipt.modules if row.module_name.endswith('.root')).dependencies == (package,)


def test_distinct_module_with_same_origin_alias_is_rejected(tmp_path,monkeypatch):
    from types import ModuleType
    contract,modules,raw=fixture(tmp_path,monkeypatch,{'c1_rail.fixture_root':'VALUE=7\n'})
    alias=ModuleType('ops.c1_rail.fixture_root')
    alias.__file__=modules['c1_rail.fixture_root'].__file__
    monkeypatch.setitem(sys.modules,alias.__name__,alias)
    with pytest.raises(ValueError,match='alias'):
        collect_runtime_inventory(contract,loaded_modules=modules,retained_source_bytes=raw)


def test_import_spec_must_use_same_canonical_name(tmp_path,monkeypatch):
    contract,modules,raw=fixture(tmp_path,monkeypatch,{'c1_rail.fixture_root':'VALUE=7\n'})
    modules['c1_rail.fixture_root'].__spec__.name='ops.c1_rail.fixture_root'
    with pytest.raises(ValueError,match='canonical'):
        collect_runtime_inventory(contract,loaded_modules=modules,retained_source_bytes=raw)


def test_dynamic_code_sites_are_retained_for_consumer_resolution_not_blanket_denied(tmp_path,monkeypatch):
    contract,modules,raw=fixture(tmp_path,monkeypatch,{'c1_rail.fixture_root':
        'from importlib import import_module as load\n'
        'def dynamic(name, source):\n'
        ' result = load(name)\n'
        ' exec(compile(source, "fixture", "exec"))\n'
        ' return result\n'})
    receipt=collect_runtime_inventory(contract,loaded_modules=modules,retained_source_bytes=raw)
    assert receipt.modules[0].dynamic_code_sites==((3,'load'),(4,'compile'),(4,'exec'))


def test_core_directory_is_canonical_python_import_root(tmp_path,monkeypatch):
    contract,modules,raw=fixture(tmp_path,monkeypatch,{'fixture_geometry':'VALUE=7\n'},
                                 paths={'fixture_geometry':'core/fixture_geometry.py'})
    receipt=collect_runtime_inventory(contract,loaded_modules=modules,retained_source_bytes=raw)
    assert receipt.modules[0].module_name=='fixture_geometry'


def test_flat_core_module_skips_impossible_relative_import_and_keeps_fallback(
        tmp_path, monkeypatch):
    contract, modules, raw = fixture(tmp_path, monkeypatch, {
        'fixture_leaf': 'VALUE=7\n',
        'fixture_geometry': (
            'try:\n'
            ' from .fixture_leaf import VALUE\n'
            'except ImportError:\n'
            ' from fixture_leaf import VALUE\n'),
    }, paths={
        'fixture_leaf': 'core/fixture_leaf.py',
        'fixture_geometry': 'core/fixture_geometry.py',
    })

    receipt = collect_runtime_inventory(
        contract, loaded_modules=modules, retained_source_bytes=raw)

    geometry = next(row for row in receipt.modules
                    if row.module_name == 'fixture_geometry')
    assert geometry.dependencies == ('fixture_leaf',)


def port_fixture(tmp_path,monkeypatch,suffix='.py'):
    from types import ModuleType
    roles={'aegis_runtime_port':'aegis_6j','striker_runtime_port':'dj30_mym_p250',
           'vanguard_runtime_port':'vanguard_mgc','orb_runtime_port':'orb_mnq_v7'}
    artifacts=[];modules={};raw={}
    for role,leg in roles.items():
        relative=f'accepted-private-generation/{leg}-corrected{suffix}'
        path=tmp_path/relative;path.parent.mkdir(parents=True,exist_ok=True)
        source=b'VALUE=7\n';path.write_bytes(source)
        module=ModuleType('fp_qualification_port_'+leg)
        module.__file__=relative;module.__package__=''
        exec(compile(source,relative,'exec'),module.__dict__)
        monkeypatch.setitem(sys.modules,module.__name__,module)
        modules[role]=module;raw[role]=source
        artifacts.append(ArtifactRecord(role,relative,hashlib.sha256(source).hexdigest(),'fixture','TEST_ONLY'))
    contract=object.__new__(ValidatedFrozenContract)
    object.__setattr__(contract,'contract_sha256','a'*64)
    object.__setattr__(contract,'artifacts',tuple(artifacts))
    object.__setattr__(contract,'runtime_load_sha256',MappingProxyType({a.role:a.sha256 for a in artifacts}))
    return contract,modules,raw


@pytest.mark.parametrize('suffix',['.py','.bin'])
def test_closed_private_port_names_relative_origins_and_external_artifact_root(tmp_path,monkeypatch,suffix):
    contract,modules,raw=port_fixture(tmp_path,monkeypatch,suffix)
    receipt=collect_runtime_inventory(contract,loaded_modules=modules,retained_source_bytes=raw,artifact_root=tmp_path)
    assert len(receipt.modules)==4
    assert {m.module_name for m in receipt.modules}=={m.__name__ for m in modules.values()}
    assert all(m.origin.startswith(str(tmp_path)) for m in receipt.modules)


def test_closed_private_loader_requires_every_port_observation(tmp_path,monkeypatch):
    contract,modules,raw=port_fixture(tmp_path,monkeypatch)
    del modules['striker_runtime_port']
    with pytest.raises(ValueError,match='four|code role'):
        collect_runtime_inventory(contract,loaded_modules=modules,retained_source_bytes=raw,artifact_root=tmp_path)


def test_closed_private_loader_cannot_omit_a_role_from_contract(tmp_path,monkeypatch):
    contract,modules,raw=port_fixture(tmp_path,monkeypatch)
    del modules['striker_runtime_port'];del raw['striker_runtime_port']
    artifacts=tuple(a for a in contract.artifacts if a.role!='striker_runtime_port')
    object.__setattr__(contract,'artifacts',artifacts)
    object.__setattr__(contract,'runtime_load_sha256',MappingProxyType({a.role:a.sha256 for a in artifacts}))
    with pytest.raises(ValueError,match='four port roles'):
        collect_runtime_inventory(contract,loaded_modules=modules,retained_source_bytes=raw,artifact_root=tmp_path)


def test_repository_imports_and_retained_ports_use_distinct_roots(tmp_path,monkeypatch):
    repository=tmp_path/'repository';private=tmp_path/'retained'
    repository.mkdir();private.mkdir()
    ordinary,ordinary_modules,ordinary_raw=fixture(repository,monkeypatch,
        {'fixture_geometry':'VALUE=7\n'},paths={'fixture_geometry':'core/fixture_geometry.py'})
    contract,modules,raw=port_fixture(private,monkeypatch,suffix='.bin')
    artifacts=contract.artifacts+ordinary.artifacts
    object.__setattr__(contract,'artifacts',artifacts)
    object.__setattr__(contract,'runtime_load_sha256',MappingProxyType({a.role:a.sha256 for a in artifacts}))
    modules.update(ordinary_modules);raw.update(ordinary_raw)
    receipt=collect_runtime_inventory(contract,loaded_modules=modules,
        retained_source_bytes=raw,artifact_root=private)
    observed={m.role:m for m in receipt.modules}
    assert observed['fixture_geometry'].origin==str((repository/'core/fixture_geometry.py').resolve())
    assert all(observed[role].origin.startswith(str(private)) for role in modules if role.endswith('_runtime_port'))
    # Identical retained bytes never authorize replacing an ordinary import's origin.
    copied=private/'core/fixture_geometry.py';copied.parent.mkdir();copied.write_bytes(ordinary_raw['fixture_geometry'])
    modules['fixture_geometry'].__file__=str(copied)
    modules['fixture_geometry'].__spec__.origin=str(copied)
    with pytest.raises(ValueError,match='origin'):
        collect_runtime_inventory(contract,loaded_modules=modules,retained_source_bytes=raw,artifact_root=private)


def test_private_port_origin_cannot_move_outside_retained_root(tmp_path,monkeypatch):
    private=tmp_path/'retained';private.mkdir()
    contract,modules,raw=port_fixture(private,monkeypatch,suffix='.bin')
    outside=tmp_path/'identical.py';outside.write_bytes(raw['aegis_runtime_port'])
    modules['aegis_runtime_port'].__file__=str(outside)
    with pytest.raises(ValueError,match='origin'):
        collect_runtime_inventory(contract,loaded_modules=modules,retained_source_bytes=raw,artifact_root=private)


def test_canonical_account_owner_does_not_load_flat_c1_rail_aliases():
    repository = Path(__file__).resolve().parents[3]
    script = (
        "import json,sys\n"
        "import c1_rail.book_account_owner\n"
        "print(json.dumps(sorted(name for name in sys.modules if name in "
        "('book_policy','book_capacity','book_sizing_context','book_account_lock','book_schedule'))))\n"
    )
    completed = subprocess.run(
        [sys.executable, "-c", script], cwd=repository,
        env={**__import__('os').environ,
             "PYTHONPATH": __import__('os').pathsep.join((
                 str(repository / "ops"), str(repository / "core")))},
        text=True, capture_output=True, check=True)

    assert json.loads(completed.stdout) == []
