"""Run representative semantic mutations in disposable copies, never the working tree.

Usage: python tests/ops/tb_s3_kernel/mutation_check.py
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


MUTATIONS = {
    "overwrite_owner": ("kernel.py", [(
        "        self.obligations[(reason, owner)] = Obligation(reason, owner, detail)",
        "        self.obligations = {k: v for k, v in self.obligations.items() if k[0] != reason}\n"
        "        self.obligations[(reason, owner)] = Obligation(reason, owner, detail)")]),
    "ignore_working_remainder": ("kernel.py", [(
        "return scope_quiescent(ev, op.scope_kind, op.scope_id, self.pending)",
        "return ev.order_level and ev.position == 0")]),
    "trust_timestamp_without_causality": ("rules.py", [(
        "ev.request_fence and ev.acquired > boundary and ev.as_of > at",
        "ev.request_fence and ev.as_of > at")]),
    "ignore_protection_parameter": ("rules.py", [(
        "return all(order.get(k) == v for k, v in fields.items())", "return True")]),
    "omit_completion_disarm": ("kernel.py", [(
        'if self.flatten_complete("kill", now):', 'if False:')]),
}


def main():
    """Require clean controls, then require every mutant to fail behavioral assertions."""
    root = Path(__file__).resolve().parents[3]
    results = {}
    with tempfile.TemporaryDirectory(prefix="pr365-mutations-") as directory:
        scratch = Path(directory).resolve()
        assert scratch.is_relative_to(Path(tempfile.gettempdir()).resolve())
        suite = scratch / "tests" / "ops"
        suite.mkdir(parents=True)
        (scratch / "tests" / "__init__.py").touch()
        (suite / "__init__.py").touch()
        shutil.copytree(root / "tests/ops/tb_s3_kernel", suite / "tb_s3_kernel")
        for source in (root / "tests/ops").glob("test_tb_s3_kernel*.py"):
            shutil.copy2(source, suite / source.name)
        layers = [scratch] + [root / p for p in
                              ("core", "ops", "ops/c1_rail", "ops/c1_signal_daemon", "lab")]
        env = dict(os.environ, PYTHONPATH=os.pathsep.join(map(str, layers)),
                   PYTHONDONTWRITEBYTECODE="1")
        command = [sys.executable, "-m", "pytest", "tests/ops", "-q", "-p", "no:cacheprovider",
                   "--tb=no"]
        baseline = subprocess.run(command, cwd=scratch, env=env, capture_output=True, text=True,
                                  check=False)
        if baseline.returncode:
            raise RuntimeError(f"control failed: {baseline.stdout}\n{baseline.stderr}")
        results["control"] = baseline.stdout.strip().splitlines()[-1]
        for name, (filename, changes) in MUTATIONS.items():
            path = suite / "tb_s3_kernel" / filename
            original = path.read_text(encoding="utf-8")
            changed = original
            for old, new in changes:
                if changed.count(old) != 1:
                    raise RuntimeError(f"mutation anchor is not unique: {name}")
                changed = changed.replace(old, new)
            try:
                path.write_text(changed, encoding="utf-8")
                run = subprocess.run(command, cwd=scratch, env=env, capture_output=True,
                                     text=True, check=False)
                if run.returncode != 1 or "failed" not in run.stdout or "ERROR" in run.stdout:
                    raise RuntimeError(f"mutation survived or broke collection: {name}\n{run.stdout}")
                results[name] = run.stdout.strip().splitlines()[-1]
            finally:
                path.write_text(original, encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
