"""Fixture inventory is captured before signing, including loaded children."""
def test_loaded_package_child_is_retained_with_its_real_dependencies():
    import c1_rail.qualification.seal
    from runtime_fixture import ordinary_runtime_fixture
    rows=ordinary_runtime_fixture(role_modules={},seeds=('c1_rail.qualification.model',))
    names={row.name for row in rows}
    assert 'c1_rail.qualification.seal' in names
    assert 'c1_rail.qualification.contract' in names
    assert all(row.source_bytes for row in rows if not row.path.endswith('__init__.py'))
