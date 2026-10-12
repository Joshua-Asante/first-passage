"""An explicit selection mixing legacy ops files with qualification inventory tests.

Legacy files load ``c1_rail.c1_rail_listener`` (flat ``c1_rail_telemetry``
alias) at collection; the signed inventory must still build in that process.
"""
import os
from pathlib import Path
import subprocess
import sys


def test_legacy_listener_import_does_not_contaminate_signed_inventory(tmp_path):
    repository = Path(__file__).resolve().parents[2]
    environment = os.environ.copy()
    for name in ("PYTEST_ADDOPTS", "PYTEST_XDIST_WORKER",
                 "PYTEST_XDIST_WORKER_COUNT", "PYTEST_XDIST_TESTRUNUID"):
        environment.pop(name, None)
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-n", "0", "-p", "no:cacheprovider",
         "--basetemp=" + str(tmp_path / "child"),
         "tests/ops/test_book_account_owner.py::test_existing_empty_account_database_is_not_reinitialized",
         "tests/ops/qualification/test_seal.py::"
         "test_historical_complete_pass_signatures_inspect_but_active_authority_is_retired"],
        cwd=repository, env=environment, capture_output=True, text=True, timeout=900, check=False)
    assert completed.returncode == 0, completed.stdout[-8000:] + completed.stderr[-4000:]
    assert "2 passed" in completed.stdout
