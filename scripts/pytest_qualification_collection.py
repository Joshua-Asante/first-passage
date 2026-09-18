"""Retain exact selection from the executing, serial boundary pytest session."""
import json
from pathlib import Path

import pytest


def pytest_addoption(parser):
    parser.addoption('--qualification-collection', help='Write exact selected node IDs')


def pytest_configure(config):
    if config.getoption('--qualification-collection') and getattr(config.option, 'numprocesses', 0):
        raise pytest.UsageError('qualification collection requires serial pytest (-n 0)')


def pytest_collection_finish(session):
    destination = session.config.getoption('--qualification-collection')
    if destination:
        nodes = [item.nodeid for item in session.items]
        if len(nodes) != len(set(nodes)):
            raise pytest.UsageError('duplicate qualification node IDs')
        Path(destination).write_text(json.dumps(sorted(nodes), indent=2) + '\n', encoding='utf-8')
