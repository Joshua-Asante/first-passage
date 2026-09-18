"""Retain actual pytest collection and exact report identity for the invariant gate."""
import json
from pathlib import Path

import pytest


def pytest_addoption(parser):
    parser.addoption('--qualification-collection', help='Actual collected node IDs for the invariant gate')


def pytest_collection_finish(session):
    output = session.config.getoption('--qualification-collection')
    if output:
        Path(output).write_text(json.dumps(dict(schema='qualification_collection/v1',
            nodeids=[item.nodeid for item in session.items]), indent=2) + '\n', encoding='utf-8')


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    result = yield
    report = result.get_result()
    report.user_properties = [*report.user_properties, ('qualification_nodeid', item.nodeid)]
