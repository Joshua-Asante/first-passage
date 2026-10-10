"""scripts/r1r2_evidence.py on synthetic fixtures only (no vendor data, no retained private inputs).

One OPEN session (2026-03-04, EST) whose schedule puts flatten_start (15:55 ET) strictly inside
the 15:45 ET M15 bar; cutoff (15:45) and own-flat deadline (16:00) are grid boundaries. Each leg's
5m export tiles that bar so the instant is located on segment far -> close.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import zipfile

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'scripts'))
_spec = importlib.util.spec_from_file_location('r1r2_evidence', REPO / 'scripts' / 'r1r2_evidence.py')
r1r2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r1r2)

from c1_rail.qualification.model import LEG_IDS  # noqa: E402  (layer roots set by the script import)
from c1_rail.qualification.production_source import (  # noqa: E402
    decode_admitted_csv, parse_schedule_execution_evidence)

DAY = '2026-03-04'
M15_BAR = (datetime(2026, 3, 4, 20, 45, tzinfo=timezone.utc), 100.0, 103.0, 99.0, 101.0, 30)
FINE = [(datetime(2026, 3, 4, 20, 45, tzinfo=timezone.utc), 100.0, 100.5, 99.0, 100.0, 10),
        (datetime(2026, 3, 4, 20, 50, tzinfo=timezone.utc), 100.0, 103.0, 100.0, 102.0, 10),
        (datetime(2026, 3, 4, 20, 55, tzinfo=timezone.utc), 102.0, 102.0, 101.0, 101.0, 10)]
STEMS = {'aegis_6j': '6J1', 'dj30_mym_p250': 'MYM1', 'vanguard_mgc': 'MGC1', 'orb_mnq_v7': 'MNQ1'}

M = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
P = 'http://schemas.openxmlformats.org/package/2006/relationships'


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def signal(ts, o, h, l, c, v):
    return f'{int(ts.timestamp() * 1000)}|{o}|{h}|{l}|{c}|{v}'


def write_xlsx(path: Path, rows, *, sheet='Trades'):
    """A minimal workbook: the trades sheet is the second sheet (sheet2.xml) with inline-typed cells."""
    def cell(ref, text):
        return f'<c r="{ref}" t="str"><v>{text}</v></c>'
    body = ''.join(f'<row r="{i}">' + ''.join(cell(f'{chr(65 + j)}{i}', v) for j, v in enumerate(row)) + '</row>'
                   for i, row in enumerate(rows, start=1))
    with zipfile.ZipFile(path, 'w') as z:
        z.writestr('xl/workbook.xml', f'<workbook xmlns="{M}" xmlns:r="{R}"><sheets>'
                   f'<sheet name="Performance" sheetId="1" r:id="rId1"/>'
                   f'<sheet name="{sheet}" sheetId="2" r:id="rId2"/></sheets></workbook>')
        z.writestr('xl/_rels/workbook.xml.rels', f'<Relationships xmlns="{P}">'
                   f'<Relationship Id="rId1" Target="worksheets/sheet1.xml"/>'
                   f'<Relationship Id="rId2" Target="worksheets/sheet2.xml"/></Relationships>')
        z.writestr('xl/worksheets/sheet1.xml', f'<worksheet xmlns="{M}"><sheetData/></worksheet>')
        z.writestr('xl/worksheets/sheet2.xml', f'<worksheet xmlns="{M}"><sheetData>{body}</sheetData></worksheet>')


def trade_rows(*, price_offset=0.0, reverse=False):
    rows = []
    for n, bar in enumerate(FINE, start=1):
        rows.append([str(n), 'Exit long', 'Close', str(bar[4])])
        rows.append([str(n), 'Entry long', signal(*bar), str(bar[4] + price_offset)])
    rows.append(['9', 'Entry long', 'not-a-bar-signal', '1'])
    if reverse:
        rows.reverse()
    return [['Trade #', 'Type', 'Signal', 'Price USD']] + rows


def build_case(root: Path, **rows_kw):
    """Retained panels + calendar under root/artifacts, a contract, and four exports."""
    art = root / 'artifacts'
    art.mkdir()
    ts, o, h, l, c, v = M15_BAR
    panel = f'time,open,high,low,close,volume\n{ts.isoformat().replace("+00:00", "Z")},{o},{h},{l},{c},{v}\n'.encode()
    payloads = {f'panel_{leg}': panel for leg in LEG_IDS}
    fact = {'role': 'panel_aegis_6j', 'sha256': sha(panel)}
    calendar = {'schema': 'qualification-source-calendar/v1', 'coverage_start': DAY, 'coverage_end': DAY,
                'tail_covered': True, 'sessions': [{
                    'date': DAY, 'status': 'OPEN', 'reason': 'synthetic', 'facts': [fact],
                    'venue_deadlines': {leg: {'instant': '2026-03-04T22:00:00Z', 'fact': fact} for leg in LEG_IDS}}]}
    payloads['source_calendar'] = json.dumps(calendar).encode()
    for role, raw in payloads.items():
        (art / f'{role}.bin').write_bytes(raw)
    contract = {'artifacts': [{'role': role, 'path': f'{role}.bin', 'sha256': sha(raw)} for role, raw in payloads.items()],
                'populations': {'FULL': [DAY]}}
    contract_path = root / 'contract.json'
    contract_path.write_bytes(json.dumps(contract).encode())
    exports = root / 'exports'
    exports.mkdir()
    for stem in STEMS.values():
        write_xlsx(exports / f'{stem}_5m_window_synthetic.xlsx', trade_rows(**rows_kw))
    return {'contract': contract_path, 'contract_sha256': sha(contract_path.read_bytes()),
            'artifact_root': art, 'exports': exports, 'panels': payloads}


def run(case, out):
    return r1r2.main(['--contract', str(case['contract']), '--contract-sha256', case['contract_sha256'],
                      '--artifact-root', str(case['artifact_root']), '--exports', str(case['exports']),
                      '--out', str(out)])


def test_xlsx_decode_resolves_sheet_by_name_and_skips_non_entries(tmp_path):
    path = tmp_path / 'x.xlsx'
    write_xlsx(path, trade_rows())
    bars, info = r1r2.decode_export(path, '6J')
    assert sorted(bars) == [b[0] for b in FINE]
    assert [(b.open, b.high, b.low, b.close, b.volume) for _, b in sorted(bars.items())] == [b[1:] for b in FINE]
    assert info['undecodable_entries'] == 1 and info['entry_bars'] == 3


def test_xlsx_without_trades_sheet_is_refused(tmp_path):
    path = tmp_path / 'x.xlsx'
    write_xlsx(path, trade_rows(), sheet='Other')
    with pytest.raises(r1r2.Refusal, match='Trades'):
        r1r2.decode_export(path, '6J')


def test_entry_price_not_equal_close_is_refused(tmp_path):
    case = build_case(tmp_path, price_offset=0.5)
    with pytest.raises(r1r2.Refusal, match='cross-check'):
        run(case, tmp_path / 'out')
    assert not (tmp_path / 'out').exists()


def test_retained_digest_mismatch_is_refused(tmp_path):
    case = build_case(tmp_path)
    (case['artifact_root'] / 'panel_orb_mnq_v7.bin').write_bytes(case['panels']['panel_orb_mnq_v7'] + b'\n')
    with pytest.raises(r1r2.Refusal, match='digest mismatch: panel_orb_mnq_v7'):
        run(case, tmp_path / 'out')
    assert not (tmp_path / 'out').exists()


def test_contract_digest_mismatch_is_refused(tmp_path):
    case = build_case(tmp_path)
    case['contract_sha256'] = '0' * 64
    with pytest.raises(r1r2.Refusal, match='contract digest'):
        run(case, tmp_path / 'out')


def test_output_is_deterministic(tmp_path):
    (tmp_path / 'a').mkdir()
    a = build_case(tmp_path / 'a')
    assert run(a, tmp_path / 'a' / 'out') == 0 and run(a, tmp_path / 'a' / 'out2') == 0
    for name in ('schedule_execution_evidence.json', 'yield_summary.json', 'SHA256SUMS'):
        assert (tmp_path / 'a' / 'out' / name).read_bytes() == (tmp_path / 'a' / 'out2' / name).read_bytes()
    (tmp_path / 'b').mkdir()
    b = build_case(tmp_path / 'b', reverse=True)   # export row order does not change the evidence
    assert run(b, tmp_path / 'b' / 'out') == 0
    evidence = (tmp_path / 'a' / 'out' / 'schedule_execution_evidence.json').read_bytes()
    assert (tmp_path / 'b' / 'out' / 'schedule_execution_evidence.json').read_bytes() == evidence
    assert evidence == json.dumps(json.loads(evidence), sort_keys=True, separators=(',', ':')).encode()


def test_round_trip_through_production_parser(tmp_path):
    case = build_case(tmp_path)
    assert run(case, tmp_path / 'out') == 0
    raw = (tmp_path / 'out' / 'schedule_execution_evidence.json').read_bytes()
    parsed = parse_schedule_execution_evidence(raw)
    panels = tuple((leg, decode_admitted_csv(case['panels'][f'panel_{leg}'], sha(case['panels'][f'panel_{leg}'])))
                   for leg in LEG_IDS)
    parsed.validate_supplied(panels)
    instant = datetime(2026, 3, 4, 20, 55, tzinfo=timezone.utc)
    assert sorted(parsed.located) == sorted((datetime(2026, 3, 4).date(), leg, M15_BAR[0], M15_BAR[0], instant)
                                            for leg in LEG_IDS)
    rows = json.loads(raw)['rows']
    assert {r['price'] for r in rows} == {102.0}
    summary = json.loads((tmp_path / 'out' / 'yield_summary.json').read_bytes())
    assert summary['all_open_sessions']['located'] == 4 and summary['full_population_sessions']['candidates'] == 4
    assert 'strictly inside an M15 bar present in the retained panel' in summary['candidate_rule']
    assert summary['evidence_file_sha256'] == sha(raw)
    sums = (tmp_path / 'out' / 'SHA256SUMS').read_text(encoding='utf-8')
    assert f'{sha(raw)} *schedule_execution_evidence.json' in sums
