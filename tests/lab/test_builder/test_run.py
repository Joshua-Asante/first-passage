"""One builder run end to end on a synthetic raw export (I-R1..I-R3, I-C1, I-D3, I-K2, I-L4)."""
from __future__ import annotations

import json

import pytest

from builder import data, ledger, run
from tests.lab.test_builder.builder_inputs import CARD, export_lines, panel, write


@pytest.fixture
def spec(tmp_path):
    """A valid run.yaml (as JSON) over 260 sessions of a clean synthetic export; returns (path, dict, dates)."""
    b, dates = panel(260)
    p, sha = write(tmp_path, export_lines(b))
    (tmp_path / "c.yaml").write_text(CARD)
    s = {"run_id": "r1", "ledger": str(tmp_path / "l.jsonl"), "firm": "Tradeify_Select_100K",
         "data": {"MCL": {"path": str(p), "sha256": sha}}, "roll": "as exported",
         "cards": [str(tmp_path / "c.yaml")], "out": str(tmp_path / "out"), "book": None}
    path = tmp_path / "run.yaml"
    path.write_text(json.dumps(s))
    return path, s, dates


def go(path, s):
    path.write_text(json.dumps(s))
    return run.main([str(path)])


def book_file(tmp_path, book: dict) -> dict:
    p = tmp_path / "book.json"
    p.write_text(json.dumps(book))
    return {"path": str(p), "sha256": data.file_sha256(p)}


def test_run_writes_reports_with_the_data_summary(spec):
    path, s, _ = spec
    assert go(path, s) == 0
    [v] = json.loads((path.parent / "out" / "verdict.json").read_text())
    rep = json.loads((path.parent / "out" / "g-001.report.json").read_text())
    assert v["card"] == "g-001" and rep["data"]["sha256"] == s["data"]["MCL"]["sha256"] and rep["k"] == 1


@pytest.mark.parametrize("mutate,msg", [
    (lambda s: s.pop("book"), "needs keys"),                        # book must be declared
    (lambda s: s.update(boook=None), "needs keys"),                 # unknown key is not ignored
    (lambda s: s.update(run_id=""), "run_id"),
    (lambda s: s.update(cards=[]), "cards must be"),
    (lambda s: s["data"]["MCL"].pop("sha256"), "path, sha256"),     # I-R2: data must be pinned
    (lambda s: s.update(data={"MCL": "x.csv"}), "path, sha256"),
    (lambda s: s.update(book={"path": "b.json", "sha256": "0"}), "min_overlap"),   # I-R3
    (lambda s: s.update(book={"path": "b.json", "sha256": "0", "min_overlap": 0}), "min_overlap"),
    (lambda s: s.update(book={"path": "b.json", "sha256": "0", "min_overlap": True}), "min_overlap"),
])
def test_I_R1_R3_run_spec_is_strict_and_checked_before_ledgering(spec, mutate, msg):
    path, s, _ = spec
    mutate(s)
    with pytest.raises(run.RunError, match=msg):
        go(path, s)
    assert not (path.parent / "l.jsonl").exists()


def test_I_R2_instrument_without_data_refused_before_ledgering(spec):
    path, s, _ = spec
    s["data"] = {"M2K": s["data"]["MCL"]}
    with pytest.raises(run.RunError, match="no data for"):
        go(path, s)
    assert not (path.parent / "l.jsonl").exists()


def test_I_L4_cards_are_ledgered_before_the_data_is_read(spec):
    path, s, _ = spec
    s["data"]["MCL"]["sha256"] = "0" * 64  # wrong pin: the load aborts after ledgering
    with pytest.raises(data.DataError, match="pinned"):
        go(path, s)
    assert ledger.k(path.parent / "l.jsonl", "MCL") == 1 and not (path.parent / "out").exists()


@pytest.mark.parametrize("firm,override,msg", [
    ("Tradeify_Select_100K", 0.5, "has a commission row"),
    ("Bulenox_100K", None, "positive commission_per_side"),
    ("Bulenox_100K", -1, "positive commission_per_side"),
    ("Bulenox_100K", float("nan"), "positive commission_per_side"),
    ("Bulenox_100K", True, "positive commission_per_side"),
])
def test_I_C1_cost_row_resolved_before_ledgering(spec, firm, override, msg):
    path, s, _ = spec
    s["firm"] = firm
    if override is not None:
        s["commission_per_side"] = {"MCL": override}
    with pytest.raises(run.RunError, match=msg):
        go(path, s)
    assert not (path.parent / "l.jsonl").exists()


def test_I_C1_override_accepted_only_where_no_row(spec):
    path, s, _ = spec
    s.update(firm="Bulenox_100K", commission_per_side={"MCL": 1.5})
    assert go(path, s) == 0
    assert json.loads((path.parent / "out" / "g-001.report.json").read_text())["cost_per_trade_usd"] == pytest.approx(5.0)


def test_I_D3_duplicate_card_ids_rejected_before_ledgering(spec):
    path, s, _ = spec
    (path.parent / "c2.yaml").write_text(CARD.replace("value: 2, step: 1", "value: 3, step: 1"))
    s["cards"].append(str(path.parent / "c2.yaml"))
    with pytest.raises(run.RunError, match="duplicate card ids"):
        go(path, s)
    assert not (path.parent / "l.jsonl").exists()


def test_I_K2_book_must_cover_min_overlap_development_sessions(spec, tmp_path):
    path, s, dates = spec
    dev, _ = data.split(dates)
    s["book"] = {**book_file(tmp_path, {d: -1.0 for d in dev[:10]}), "min_overlap": 11}
    with pytest.raises(data.BookError, match="covers 10 MCL development sessions"):
        go(path, s)
    assert not (path.parent / "out").exists()
    s["book"] = {**book_file(tmp_path, {d: -1.0 for d in dev[:10]}), "min_overlap": 10}
    assert go(path, s) == 0


def test_I_K2_book_dated_only_in_the_holdout_is_refused(spec, tmp_path):
    path, s, dates = spec
    _, hold = data.split(dates)
    s["book"] = {**book_file(tmp_path, {d: -1.0 for d in hold}), "min_overlap": 1}
    with pytest.raises(data.BookError, match="covers 0"):
        go(path, s)
