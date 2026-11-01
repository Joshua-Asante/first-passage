"""One builder run and its holdout looks end to end on a synthetic raw export (I-R1..I-R3, I-C1, I-D3, I-K2, I-L4)."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from builder import cards, data, holdout, ledger, run
from tests.lab.test_builder.builder_inputs import CARD, export_lines, panel, write

CAL = Path(__file__).resolve().parents[3] / "ops" / "calendars" / "cme_holiday_calendar_2022_2026.json"
CARD_B = CARD.replace("id: g-001", "id: a-002").replace("value: 2, step: 1", "value: 3, step: 1")


@pytest.fixture
def spec(tmp_path):
    """A valid run.yaml (as JSON) over 400 sessions of a clean synthetic export, split at session
    300 with 20 sessions after holdout_end; returns (path, dict, dates)."""
    b, dates = panel(400)
    p, sha = write(tmp_path, export_lines(b))
    (tmp_path / "c.yaml").write_text(CARD)
    s = {"run_id": "r1", "ledger": str(tmp_path / "l.jsonl"), "firm": "Tradeify_Select_100K",
         "data": {"MCL": {"path": str(p), "sha256": sha,
                          "split": {"dev_end": dates[299], "holdout_end": dates[379]}}},
         "roll": "as exported", "calendar": {"path": str(CAL), "sha256": data.file_sha256(CAL)},
         "k_scope": "instrument", "cards": [str(tmp_path / "c.yaml")], "out": str(tmp_path / "out"), "book": None}
    path = tmp_path / "run.yaml"
    path.write_text(json.dumps(s))
    return path, s, dates


def go(path, s, mod=run):
    path.write_text(json.dumps(s))
    return mod.main([str(path)])


def report(path, card_id="g-001", kind="report"):
    return json.loads((path.parent / "out" / f"{card_id}.{kind}.json").read_text())


def book_file(tmp_path, book: dict) -> dict:
    p = tmp_path / "book.json"
    p.write_text(json.dumps(book))
    return {"path": str(p), "sha256": data.file_sha256(p)}


def test_run_writes_reports_with_the_data_summary_split_and_calendar(spec):
    path, s, dates = spec
    assert go(path, s) == 0
    [v] = json.loads((path.parent / "out" / "verdict.json").read_text())
    rep = report(path)
    assert v["card"] == "g-001" and rep["data"]["sha256"] == s["data"]["MCL"]["sha256"]
    assert (rep["k"], rep["k_scope"]) == (1, "instrument") and rep["split"] == s["data"]["MCL"]["split"]
    assert rep["dev_sessions"] == [dates[0], dates[299], 300] and rep["calendar_sha256"] == s["calendar"]["sha256"]


def test_calendar_exception_days_are_skipped_and_kept_as_sessions(spec):
    path, s, dates = spec
    go(path, s)
    closed = data.load_calendar(CAL, s["calendar"]["sha256"]).closed
    n = len(closed & set(dates[:300]))
    assert n >= 10 and report(path)["skipped_days"] == {"calendar_exception": n}
    assert report(path)["dev_sessions"][2] == 300


def test_k_scope_ledger_counts_cards_of_every_instrument_in_the_ledger(spec):
    path, s, _ = spec
    ledger.append_cards(Path(s["ledger"]), "earlier", [cards.parse(CARD.replace("instrument: MCL", "instrument: M2K"))])
    s["k_scope"] = "ledger"
    go(path, s)
    assert (report(path)["k"], report(path)["k_scope"]) == (2, "ledger")


@pytest.mark.parametrize("mutate,msg", [
    (lambda s: s.pop("book"), "needs keys"),                        # book must be declared
    (lambda s: s.pop("calendar"), "needs keys"),
    (lambda s: s.pop("k_scope"), "needs keys"),
    (lambda s: s.update(boook=None), "needs keys"),                 # unknown key is not ignored
    (lambda s: s.update(run_id=""), "run_id"),
    (lambda s: s.update(cards=[]), "cards must be"),
    (lambda s: s["data"]["MCL"].pop("sha256"), "path, sha256, split"),     # I-R2: data must be pinned
    (lambda s: s["data"]["MCL"].pop("split"), "path, sha256, split"),
    (lambda s: s.update(data={"MCL": "x.csv"}), "path, sha256, split"),
    (lambda s: s["data"]["MCL"].update(split={"dev_end": "2023-06-01"}), "dev_end, holdout_end"),
    (lambda s: s["data"]["MCL"]["split"].update(dev_end="2023-6-1"), "YYYY-MM-DD"),
    (lambda s: s["data"]["MCL"]["split"].update(dev_end=0.7), "YYYY-MM-DD"),   # no percentage split
    (lambda s: s["data"]["MCL"]["split"].update(dev_end="2024-12-31"), "before holdout_end"),
    (lambda s: s.update(calendar={"path": "c.json"}), "calendar must be"),
    (lambda s: s.update(k_scope="family"), "k_scope"),
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


def test_unquoted_yaml_split_dates_are_accepted(spec):
    path, s, dates = spec
    split = s["data"]["MCL"]["split"]
    text = json.dumps(s).replace(f'"{split["dev_end"]}"', split["dev_end"])
    yaml_path = path.parent / "run_unquoted.yaml"
    yaml_path.write_text(text)
    assert run.spec(yaml_path)["data"]["MCL"]["split"] == split


def test_calendar_pin_is_checked_before_ledgering(spec):
    path, s, _ = spec
    s["calendar"]["sha256"] = "0" * 64
    with pytest.raises(data.DataError, match="pinned"):
        go(path, s)
    assert not (path.parent / "l.jsonl").exists()


@pytest.mark.parametrize("key,value", [("dev_end", "2023-06-03"), ("holdout_end", "2025-01-02")])  # a Saturday; past the export
def test_split_end_that_is_not_a_session_date_is_refused(spec, key, value):
    path, s, _ = spec
    s["data"]["MCL"]["split"][key] = value
    with pytest.raises(data.DataError, match=f"{key} .* not a session date"):
        go(path, s)
    assert not (path.parent / "out").exists()


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
    assert report(path)["cost_per_trade_usd"] == pytest.approx(5.0)


def test_I_D3_duplicate_card_ids_rejected_before_ledgering(spec):
    path, s, _ = spec
    (path.parent / "c2.yaml").write_text(CARD.replace("value: 2, step: 1", "value: 3, step: 1"))
    s["cards"].append(str(path.parent / "c2.yaml"))
    with pytest.raises(run.RunError, match="duplicate card ids"):
        go(path, s)
    assert not (path.parent / "l.jsonl").exists()


def test_I_K2_book_must_cover_min_overlap_development_sessions(spec, tmp_path):
    path, s, dates = spec
    dev = dates[:300]
    s["book"] = {**book_file(tmp_path, {d: -1.0 for d in dev[:10]}), "min_overlap": 11}
    with pytest.raises(data.BookError, match="covers 10 MCL development sessions"):
        go(path, s)
    assert not (path.parent / "out").exists()
    s["book"] = {**book_file(tmp_path, {d: -1.0 for d in dev[:10]}), "min_overlap": 10}
    assert go(path, s) == 0


@pytest.mark.parametrize("window", [slice(300, 380), slice(380, 400)])
def test_I_K2_book_dated_only_in_the_holdout_or_after_it_is_refused(spec, tmp_path, window):
    path, s, dates = spec
    s["book"] = {**book_file(tmp_path, {d: -1.0 for d in dates[window]}), "min_overlap": 1}
    with pytest.raises(data.BookError, match="covers 0"):
        go(path, s)


# --- holdout runner --------------------------------------------------------------------------

def two_cards(path, s):
    """Add a second card whose id sorts first though it is listed second."""
    (path.parent / "b.yaml").write_text(CARD_B)
    s["cards"].append(str(path.parent / "b.yaml"))


def looks(s):
    return [e for e in ledger.read(Path(s["ledger"])) if e["kind"] == "holdout_look"]


def test_holdout_looks_survivors_in_card_id_order_on_the_pinned_window(spec):
    path, s, dates = spec
    two_cards(path, s)
    go(path, s)
    assert [report(path, i)["verdict"] for i in ("g-001", "a-002")] == ["survivor", "survivor"]
    assert go(path, s, holdout) == 0
    ids = {cards.parse(t).sha256: cards.parse(t).id for t in (CARD, CARD_B)}
    assert [ids[e["card_sha256"]] for e in looks(s)] == ["a-002", "g-001"]
    h = report(path, "g-001", "holdout")
    assert h["holdout_sessions"] == [dates[300], dates[379], 80] and h["split"] == s["data"]["MCL"]["split"]
    assert h["verdict"] in {"pass", "fail"} and h["card_id"] == "g-001"


def test_holdout_skips_cards_that_did_not_survive(spec):
    path, s, _ = spec
    go(path, s)
    out = path.parent / "out"
    body = json.dumps({**report(path), "verdict": "killed"}).encode()
    (out / "g-001.report.json").write_bytes(body)
    [v] = json.loads((out / "verdict.json").read_text())
    (out / "verdict.json").write_text(json.dumps([{**v, "report_sha256": hashlib.sha256(body).hexdigest()}]))
    assert go(path, s, holdout) == 0 and looks(s) == [] and not (path.parent / "out" / "g-001.holdout.json").exists()


@pytest.mark.parametrize("damage", ["no_run", "no_verdict", "no_report", "not_final", "other_run"])
def test_holdout_refuses_an_unfinished_run(spec, damage):
    path, s, _ = spec
    if damage != "no_run":
        go(path, s)
    out = path.parent / "out"
    if damage == "no_verdict":
        (out / "verdict.json").unlink()
    elif damage == "no_report":
        (out / "g-001.report.json").unlink()
    elif damage in ("not_final", "other_run"):
        rep = report(path)
        rep.update(verdict="running") if damage == "not_final" else rep.update(run_id="r0")
        (out / "g-001.report.json").write_text(json.dumps(rep))
    with pytest.raises(holdout.HoldoutError):
        go(path, s, holdout)
    assert not Path(s["ledger"]).exists() or looks(s) == []


def test_holdout_refuses_a_run_yaml_card_without_a_report(spec):
    path, s, _ = spec
    go(path, s)
    two_cards(path, s)
    with pytest.raises(holdout.HoldoutError, match="does not list exactly"):
        go(path, s, holdout)
    assert looks(s) == []


def test_holdout_refuses_a_card_hash_mismatch(spec):
    path, s, _ = spec
    go(path, s)
    (path.parent / "c.yaml").write_text(CARD.replace('flat_at: "12:30"', 'flat_at: "12:45"'))
    with pytest.raises(holdout.HoldoutError, match="card_sha256"):
        go(path, s, holdout)
    assert looks(s) == []


def test_holdout_refuses_a_split_mismatch(spec):
    path, s, dates = spec
    go(path, s)
    s["data"]["MCL"]["split"]["holdout_end"] = dates[390]
    with pytest.raises(holdout.HoldoutError, match="split"):
        go(path, s, holdout)
    assert looks(s) == []


def test_holdout_look_is_taken_once(spec):
    path, s, _ = spec
    go(path, s)
    go(path, s, holdout)
    with pytest.raises(ledger.LedgerError, match="already"):
        go(path, s, holdout)


@pytest.mark.parametrize("pin", ["calendar", "data"])
def test_holdout_refuses_a_changed_calendar_or_data_pin(spec, tmp_path, pin):
    path, s, _ = spec
    go(path, s)
    if pin == "calendar":
        p = tmp_path / "cal2.json"
        p.write_text(CAL.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        s["calendar"] = {"path": str(p), "sha256": data.file_sha256(p)}
    else:
        src = Path(s["data"]["MCL"]["path"])
        p = tmp_path / "export2.csv"
        p.write_bytes(src.read_bytes() + b"\n")
        s["data"]["MCL"].update(path=str(p), sha256=data.file_sha256(p))
    with pytest.raises(holdout.HoldoutError, match=f"{pin}_sha256"):
        go(path, s, holdout)
    assert looks(s) == []


def test_holdout_refuses_changed_costs(spec):
    path, s, _ = spec
    s.update(firm="Bulenox_100K", commission_per_side={"MCL": 1.5})
    go(path, s)
    s["commission_per_side"] = {"MCL": 0.5}
    with pytest.raises(holdout.HoldoutError, match="cost_per_trade_usd"):
        go(path, s, holdout)
    assert looks(s) == []


def test_holdout_refuses_a_changed_engine(spec, monkeypatch):
    path, s, _ = spec
    go(path, s)
    monkeypatch.setattr(holdout.gates, "engine_version", lambda: "0" * 64)
    with pytest.raises(holdout.HoldoutError, match="engine_sha256"):
        go(path, s, holdout)


def test_an_interrupted_rerun_leaves_no_completion_marker(spec):
    path, s, _ = spec
    go(path, s)
    good = dict(s["data"]["MCL"])
    s["data"]["MCL"]["sha256"] = "0" * 64  # the rerun aborts after ledgering, before any report
    with pytest.raises(data.DataError):
        go(path, s)
    assert not (path.parent / "out" / "verdict.json").exists()
    s["data"]["MCL"] = good
    with pytest.raises(holdout.HoldoutError, match="has not finished"):
        go(path, s, holdout)


def test_holdout_refuses_a_report_edited_after_the_run(spec):
    path, s, _ = spec
    go(path, s)
    p = path.parent / "out" / "g-001.report.json"
    p.write_text(p.read_text() + " ")
    with pytest.raises(holdout.HoldoutError, match="stale or edited"):
        go(path, s, holdout)
    assert looks(s) == []
