"""Q-SFCLEAR-2 G1/G3 calculator (build card v3 §4): synthetic panels, tuple and ports only.

The calculator is private (card §0.5); ``SFCLEAR2_CALCULATOR`` locates it and the module skips when the variable
is unset, as vendor-dependent tests do. Its ``--build-fixture`` writes the synthetic two-week fixture and the
hand-derived G1/G3/G1-D/G3-D values, so no port name, parameter field or stop formula appears in this public file.
Nothing here reads a real panel, tuple or port.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import pathlib
import re
import subprocess
import sys

import pytest

CALC = os.environ.get("SFCLEAR2_CALCULATOR")
pytestmark = pytest.mark.skipif(not CALC, reason="SFCLEAR2_CALCULATOR not set (private calculator absent)")
ROOT = pathlib.Path(__file__).resolve().parents[2]
CELLS = ("G1", "G3", "G1_D", "G3_D")


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


@pytest.fixture
def fx(tmp_path):
    proc = subprocess.run([sys.executable, "-I", CALC, "--repo-root", str(ROOT), "--build-fixture", str(tmp_path / "fx")],
                          capture_output=True, text=True)
    assert proc.returncode == 0 and proc.stdout == "", proc.stderr
    man = json.loads((tmp_path / "fx" / "manifest.json").read_text(encoding="ascii"))
    count = iter(range(1000))

    def run(variant="map12", m_star=None, calc=CALC, bad=None):
        out = tmp_path / f"out{next(count)}"
        out.mkdir()
        args = [sys.executable, "-I", str(calc), "--repo-root", man["repo_root"], "--out-root", str(out),
                "--m-star", str(man["m_star"] if m_star is None else m_star)]
        for name, p in {**man["inputs"], "tuple": man["variants"][variant]["tuple"]}.items():
            args += ["--input", name, p, "0" * 64 if name == bad else sha(p)]
        proc = subprocess.run(args, capture_output=True, text=True)
        files = list(out.glob("*.json"))
        return proc, (json.loads(files[0].read_text(encoding="ascii")) if len(files) == 1 else None), files

    return run, man


def _close(got, want):
    if isinstance(want, dict):
        return isinstance(got, dict) and set(want) <= set(got) and all(_close(got[k], want[k]) for k in want)
    return isinstance(got, (int, float)) and math.isclose(got, want, rel_tol=0, abs_tol=1e-9)


def test_calculator_exists():
    assert pathlib.Path(CALC).is_file(), f"SFCLEAR2_CALCULATOR points at a missing file: {CALC}"


@pytest.mark.parametrize("variant", ["map12", "map02"])
def test_hand_computed_g1_g3_and_drift(fx, variant):
    run, man = fx
    proc, doc, files = run(variant)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout == sha(files[0]) + "\n"
    want = man["variants"][variant]["expected"]
    for key in CELLS:
        assert _close(doc[key], want[key]), (key, doc[key], want[key])
    assert set(doc["G1"]) == {"aegis_6j", "dj30_mym_p250", "vanguard_mgc"}   # OFF leg (rule max 0) excluded
    assert len(doc["nonce"]) >= 32 and doc["calculator_sha256"] == sha(CALC)


def test_m_star_one_reproduces_g1_g3(fx):
    run, man = fx
    proc, doc, _ = run(m_star=1)
    assert proc.returncode == 0, proc.stderr
    want = man["variants"]["map12"]["expected"]
    assert _close(doc["G1_D"], want["G1"]) and _close(doc["G3_D"], want["G3"])
    assert not _close(want["G1_D"], want["G1"])          # the fixture's m* moves Vanguard's cap


MUTANTS = {
    "gap_once": ("GAP_FACTOR = 2", "GAP_FACTOR = 1"),
    "striker_times_n": ("t3 = {s: m * risk_usd for s in STATS}", "t3 = {s: n * m * risk_usd for s in STATS}"),
    "denied_row_held": ('if row["permission"] == "PERMITTED"', "if True"),
    "bar_after_flatten_start": ("<= flat_start", "<= flat_start + timedelta(minutes=5)"),
    "m_star_ignored": ("paper * m_star", "paper"),
}


@pytest.mark.parametrize("name", MUTANTS)
def test_mutant_is_caught(fx, tmp_path, name):
    run, man = fx
    old, new = MUTANTS[name]
    src = pathlib.Path(CALC).read_text(encoding="utf-8")
    assert src.count(old) == 1, f"mutation point not unique: {old!r}"
    mut = tmp_path / "mutant.py"
    mut.write_text(src.replace(old, new), encoding="utf-8")
    proc, doc, _ = run(calc=mut)
    assert proc.returncode == 0, proc.stderr          # killed by value, not by a crash
    want = man["variants"]["map12"]["expected"]
    assert not all(_close(doc[k], want[k]) for k in CELLS)


@pytest.mark.parametrize("name", ["schedule", "tuple", "e0", "effective_inputs", "book_sources",
                                  "panel:6J", "meta:6J", "panel:MYM", "meta:MYM", "panel:MGC", "meta:MGC"])
def test_sha256_mismatch_refuses(fx, name):
    run, _ = fx
    proc, _, files = run(bad=name)
    assert proc.returncode != 0 and not files and proc.stdout == ""
    assert "sha256 mismatch" in proc.stderr


def test_stdout_never_carries_an_input_value(fx):
    run, _ = fx
    proc, _, files = run()
    assert proc.returncode == 0 and proc.stdout == sha(files[0]) + "\n"   # the output file's sha256 and nothing else
    assert proc.stderr == ""


def test_no_default_paths_and_self_test():
    assert subprocess.run([sys.executable, "-I", CALC], capture_output=True, text=True).returncode != 0
    assert subprocess.run([sys.executable, "-I", CALC, "--repo-root", str(ROOT)],
                          capture_output=True, text=True).returncode != 0
    proc = subprocess.run([sys.executable, "-I", CALC, "--repo-root", str(ROOT), "--self-test"],
                          capture_output=True, text=True)
    assert proc.returncode == 0 and re.fullmatch(r"self-test ok\n", proc.stdout), proc.stdout + proc.stderr
