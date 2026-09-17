"""Bounded advisory pytest observations; JUnit remains the outcome authority."""
from __future__ import annotations

import json
import os
from pathlib import Path
import time

import pytest

MAX_ITEMS = 64
MAX_NODE_CHARS = 200


class Progress:
    def __init__(self, config, directory, run_id):
        self.worker = getattr(config, 'workerinput', {}).get('workerid', 'controller')
        self.path = directory / ('progress.json' if self.worker == 'controller'
                                 else f'progress-{self.worker}.json')
        self.run_id = run_id
        self.collected = None
        self.completed = set()
        self.active = set()
        self.finished = False
        self.publish()

    def publish(self):
        data = dict(run_id=self.run_id, worker_id=self.worker, observed_at=time.time(),
                    collected=self.collected, completed=len(self.completed),
                    completed_nodeids=[s[:MAX_NODE_CHARS] for s in sorted(self.completed)[-MAX_ITEMS:]],
                    active_nodeids=[s[:MAX_NODE_CHARS] for s in sorted(self.active)[:MAX_ITEMS]],
                    truncated=(len(self.completed) > MAX_ITEMS or len(self.active) > MAX_ITEMS or
                               any(len(s) > MAX_NODE_CHARS for s in self.completed | self.active)),
                    session_finished=self.finished)
        try:
            temporary = self.path.with_suffix('.tmp')
            temporary.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
            os.replace(temporary, self.path)
        except OSError:
            # Progress cannot interrupt testing or qualify its results.
            pass

    def pytest_collection_finish(self, session):
        self.collected = len(session.items)
        self.publish()

    @pytest.hookimpl(optionalhook=True)
    def pytest_xdist_node_collection_finished(self, node, ids):
        self.collected = len(ids)
        self.publish()

    def pytest_runtest_logstart(self, nodeid, location):
        self.active.add(nodeid)
        self.publish()

    def pytest_runtest_logfinish(self, nodeid, location):
        # xdist forwards these observations to its controller. Deduplication
        # aggregates worker observations without competing writes to one file.
        self.active.discard(nodeid)
        self.completed.add(nodeid)
        self.publish()

    def pytest_sessionfinish(self, session, exitstatus):
        self.finished = True
        self.publish()


def pytest_configure(config):
    directory = os.environ.get('FP_PYTEST_PROGRESS_DIR')
    run_id = os.environ.get('FP_PYTEST_PROGRESS_RUN')
    if directory and run_id:
        config.pluginmanager.register(Progress(config, Path(directory), run_id), 'fp-progress-observer')
