"""Emit one JUnit testcase per subtest with the locked pytest 9 producer.

Pytest 9.1.1 counts subtest outcomes but reuses their parent's XML node. Keep
the normal writer and strict downstream validation; only give those reports
separate identities and lifetimes. Other pytest consumers see original reports.
"""
from copy import copy

import pytest
from _pytest.junitxml import LogXML, xml_key
from _pytest.subtests import SubtestReport


class SubtestLogXML(LogXML):
    """Pinned pytest adapter; process regressions guard the private API boundary."""

    @pytest.hookimpl(trylast=True)
    def pytest_runtest_logreport(self, report):
        if not isinstance(report, SubtestReport):
            return super().pytest_runtest_logreport(report)
        # The controller owns this ordinal, so repeated labels and worker-local
        # parameter values cannot collide. Do not change terminal/xdist reports.
        subtest = copy(report)
        ordinal = len(self.node_reporters_ordered)
        subtest.nodeid = f'{report.nodeid}::subtest-{ordinal} {report._sub_test_description()}'
        super().pytest_runtest_logreport(subtest)
        # Ordinary skips and failures with passing-output disabled were already
        # written by the base handler. Xfails do not use its ordinary-skip path.
        capture_written = (subtest.skipped and not hasattr(subtest, 'wasxfail')) or (
            subtest.failed and not self.log_passing_tests
        )
        if not capture_written:
            self.node_reporter(subtest).write_captured_output(subtest)
        # Subtests have no separate teardown event. A parent's eventual teardown
        # must not finalize or attach errors to any of these completed outcomes.
        self.finalize(subtest)
        if subtest in self.open_reports:
            self.open_reports.remove(subtest)
        return None


@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    """Replace only the controller's configured writer, retaining all options."""
    original = config.stash.get(xml_key, None)
    if original is None:
        return
    writer = SubtestLogXML(
        original.logfile, original.prefix, original.suite_name, original.logging,
        original.report_duration, original.family, original.log_passing_tests,
    )
    config.pluginmanager.unregister(original)
    config.stash[xml_key] = writer
    config.pluginmanager.register(writer)
