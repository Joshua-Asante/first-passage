#!/usr/bin/env python3
"""Build the R1/R2 ``qualification-schedule-execution/v1`` evidence file from 5m bar exports.

``.\\fp.ps1 python scripts/r1r2_evidence.py --contract C --contract-sha256 HEX --artifact-root ROOT
--exports DIR --out NEW_DIR``

- The source contract must hash to ``--contract-sha256``. Its ``source_calendar`` and
  ``panel_<leg>`` artifacts are read in place under ``--artifact-root`` and must match the
  contract digests.
- Each leg's export is the single ``<stem>_5m_*.xlsx`` in ``--exports`` (stems in ``EXPORTS``).
  The ``Trades`` sheet is decoded with the stdlib only; each ``Entry`` row's Signal is decoded by
  ``bar_export_loader`` and its price must equal the encoded close (``price_tolerance``).
- Candidates (``CANDIDATE_RULE``) go through ``schedule_evidence.evidence_rows``; the evidence is
  re-parsed by ``parse_schedule_execution_evidence`` and checked by ``validate_supplied`` against
  the retained panels before anything is written.
- ``--out`` must not exist. It receives ``schedule_execution_evidence.json`` (canonical JSON, no
  timestamps), ``yield_summary.json`` and ``SHA256SUMS``. Any refusal writes nothing.
"""
from __future__ import annotations

import argparse
from bisect import bisect_left
from collections import Counter
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import posixpath
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

from layer_bootstrap import add_layer_roots

REPO = add_layer_roots('core', 'ops')

from bar_export_loader import decode_bar_meta, decode_bar_signal, price_tolerance  # noqa: E402
from c1_signal_daemon.feed import Bar  # noqa: E402
from c1_rail.qualification.model import LEG_IDS, SessionSchedule  # noqa: E402
from c1_rail.qualification.production_source import (  # noqa: E402
    decode_admitted_csv, parse_schedule_execution_evidence, parse_source_calendar)
from c1_rail.qualification.schedule_evidence import evidence_rows  # noqa: E402

EXPORTS = {'aegis_6j': ('6J1', '6J'), 'dj30_mym_p250': ('MYM1', 'MYM'),
           'vanguard_mgc': ('MGC1', 'MGC'), 'orb_mnq_v7': ('MNQ1', 'MNQ')}
TRADES_SHEET = 'Trades'
CANDIDATE_RULE = ('a leg x schedule instant (cutoff, flatten start or own-flat deadline) strictly inside '
                  'an M15 bar present in the retained panel, on an OPEN source-calendar session; its finer '
                  'bars are the export Entry bars in that M15 window')
CODE = ('scripts/r1r2_evidence.py', 'ops/c1_rail/qualification/schedule_evidence.py',
        'ops/c1_rail/qualification/production_source.py', 'core/bar_export_loader.py')
M15 = timedelta(minutes=15)
_M = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
_R = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
_P = '{http://schemas.openxmlformats.org/package/2006/relationships}'


class Refusal(Exception):
    """An input failed a check; nothing is written."""


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _column(ref: str) -> int:
    letters = re.match(r'[A-Z]+', ref).group()
    return sum((ord(ch) - 64) * 26 ** i for i, ch in enumerate(reversed(letters))) - 1


def read_sheet(path: Path, name: str = TRADES_SHEET) -> list[list[str]]:
    """Rows of the named worksheet as text (shared, inline and literal cells; sparse cells padded)."""
    with zipfile.ZipFile(path) as z:
        sheets = {s.get('name'): s.get(_R + 'id') for s in ET.fromstring(z.read('xl/workbook.xml')).iter(_M + 'sheet')}
        if name not in sheets:
            raise Refusal(f'no {name} sheet: {path.name}')
        targets = {r.get('Id'): r.get('Target') for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels')).iter(_P + 'Relationship')}
        target = targets[sheets[name]]
        member = target[1:] if target.startswith('/') else posixpath.normpath('xl/' + target)
        shared = ([''.join(t.text or '' for t in si.iter(_M + 't')) for si in ET.fromstring(z.read('xl/sharedStrings.xml')).iter(_M + 'si')]
                  if 'xl/sharedStrings.xml' in z.namelist() else [])
        root = ET.fromstring(z.read(member))
    rows = []
    for row in root.iter(_M + 'row'):
        cells = {}
        for position, c in enumerate(row.findall(_M + 'c')):
            v = c.find(_M + 'v')
            if c.get('t') == 'inlineStr':
                text = ''.join(t.text or '' for t in c.iter(_M + 't'))
            elif c.get('t') == 's':
                text = shared[int(v.text)]
            else:
                text = (v.text or '') if v is not None else ''
            cells[_column(c.get('r')) if c.get('r') else position] = text
        rows.append([cells.get(i, '') for i in range(max(cells, default=-1) + 1)])
    return rows


def decode_export(path: Path, symbol: str):
    """{bar-open UTC: Bar} from the Entry rows of one export, plus its non-private description."""
    header, *body = read_sheet(path)
    missing = {'Type', 'Signal', 'Price USD'} - set(header)
    if missing:
        raise Refusal(f'missing columns {sorted(missing)}: {path.name}')
    ix = {h: i for i, h in enumerate(header)}
    bars, meta, skipped = {}, None, 0
    for cells in body:
        cells = cells + [''] * (len(header) - len(cells))
        if not cells[ix['Type']].startswith('Entry'):
            continue
        sig = cells[ix['Signal']]
        try:
            enc = decode_bar_signal(sig)
        except ValueError:
            skipped += 1
            continue
        if 'epoch_ms' not in enc:
            raise Refusal(f'signal without bar time: {path.name}')
        if abs(float(cells[ix['Price USD']]) - enc['c']) > price_tolerance(symbol, enc['c']):
            raise Refusal(f'entry/close cross-check fail: {path.name}')
        m = decode_bar_meta(sig)
        const = {k: v for k, v in m.items() if not k.startswith('_')} if m else None
        if meta is None:
            meta = const
        elif const != meta:
            raise Refusal(f'meta drift: {path.name}')
        ts = datetime.fromtimestamp(int(enc['epoch_ms']) // 1000, timezone.utc)
        bar = Bar(ts, enc['o'], enc['h'], enc['l'], enc['c'], enc['v'])
        if ts in bars and bars[ts] != bar:
            raise Refusal(f'conflicting duplicate bar: {path.name}')
        bars[ts] = bar
    return bars, {'file': path.name, 'entry_bars': len(bars), 'undecodable_entries': skipped,
                  'timeframe': (meta or {}).get('timeframe'), 'ticker': (meta or {}).get('ticker')}


def _export_path(exports: Path, stem: str) -> Path:
    found = sorted(exports.glob(f'{stem}_5m_*.xlsx'))
    if len(found) != 1:
        raise Refusal(f'expected exactly one {stem}_5m_*.xlsx in --exports, found {len(found)}')
    return found[0]


def candidates(clock, panels, fine, full):
    """(leg, M15 Bar, instant, finer bars) per CANDIDATE_RULE, FULL membership, and no-source-bar counts."""
    panel_index = {leg: {b.ts: b for b in panels[leg]} for leg in LEG_IDS}
    fine_ts = {leg: sorted(fine[leg]) for leg in LEG_IDS}
    found, in_full, no_source = [], [], Counter()
    for day, schedule in clock.schedules:
        if type(schedule) is not SessionSchedule:
            continue
        for instant in (schedule.cutoff, schedule.flatten_start, schedule.own_flat_deadline):
            start = instant.replace(minute=instant.minute - instant.minute % 15, second=0, microsecond=0)
            if start == instant:
                continue                                    # grid boundary: no split needed
            for leg in LEG_IDS:
                original = panel_index[leg].get(start)
                if original is None:
                    no_source[leg] += 1
                    continue
                times = fine_ts[leg]
                window = times[bisect_left(times, start):bisect_left(times, start + M15)]
                found.append((leg, original, instant, [fine[leg][ts] for ts in window]))
                in_full.append(day.isoformat() in full)
    return found, in_full, no_source


def _tally(cands):
    rows, drops = evidence_rows(cands)
    per_leg = {}
    for leg in LEG_IDS:
        leg_rows, leg_drops = evidence_rows([c for c in cands if c[0] == leg])
        per_leg[leg] = {'candidates': len(leg_rows) + sum(leg_drops.values()), 'located': len(leg_rows),
                        'drops': dict(sorted(leg_drops.items()))}
    n = len(rows) + sum(drops.values())
    return {'candidates': n, 'located': len(rows), 'yield': round(len(rows) / n, 4) if n else None,
            'drops': dict(sorted(drops.items())), 'per_leg': per_leg}


def build(contract_path: Path, contract_sha256: str, artifact_root: Path, exports: Path):
    """(evidence bytes, yield summary); raises Refusal on any failed check."""
    contract_raw = contract_path.read_bytes()
    if sha(contract_raw) != contract_sha256:
        raise Refusal('source contract digest differs from --contract-sha256')
    artifacts = {a['role']: a for a in json.loads(contract_raw)['artifacts']}
    digests = {role: a['sha256'] for role, a in artifacts.items()}
    root = artifact_root.resolve()

    def retained(role):
        path = (root / artifacts[role]['path']).resolve()
        if not path.is_relative_to(root):
            raise Refusal(f'retained artifact escapes --artifact-root: {role}')
        raw = path.read_bytes()
        if sha(raw) != digests[role]:
            raise Refusal(f'retained digest mismatch: {role}')
        return raw

    panels = {leg: decode_admitted_csv(retained(f'panel_{leg}'), digests[f'panel_{leg}']) for leg in LEG_IDS}
    clock, _ = parse_source_calendar(retained('source_calendar'), artifact_digests=digests)
    full = set(json.loads(contract_raw)['populations']['FULL'])
    fine, export_info, input_hashes = {}, {}, {}
    for leg in LEG_IDS:
        stem, symbol = EXPORTS[leg]
        path = _export_path(exports, stem)
        input_hashes[path.name] = sha(path.read_bytes())
        fine[leg], export_info[leg] = decode_export(path, symbol)

    cands, in_full, no_source = candidates(clock, panels, fine, full)
    rows, _ = evidence_rows(cands)
    evidence = json.dumps({'schema': 'qualification-schedule-execution/v1', 'rows': rows},
                          sort_keys=True, separators=(',', ':')).encode()
    parsed = parse_schedule_execution_evidence(evidence)
    parsed.validate_supplied(tuple(panels.items()))
    summary = {
        'convention': 'evidence-located/v1', 'candidate_rule': CANDIDATE_RULE,
        'code_sha256': {name: sha((REPO / name).read_bytes()) for name in CODE},
        'source_contract_sha256': contract_sha256,
        'retained_inputs_sha256': {r: digests[r] for r in ['source_calendar', *(f'panel_{leg}' for leg in LEG_IDS)]},
        'export_inputs_sha256': input_hashes, 'exports': export_info,
        'not_candidates_no_source_bar': dict(sorted(no_source.items())),
        'all_open_sessions': _tally(cands),
        'full_population_sessions': _tally([c for c, keep in zip(cands, in_full) if keep]),
        'evidence_file_sha256': sha(evidence), 'evidence_rows': len(parsed.splits),
        'validated': 'parse_schedule_execution_evidence + validate_supplied(retained panels) passed',
    }
    return evidence, summary


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--contract', type=Path, required=True)
    ap.add_argument('--contract-sha256', required=True)
    ap.add_argument('--artifact-root', type=Path, required=True)
    ap.add_argument('--exports', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args(argv)
    if args.out.exists():
        raise Refusal('--out must not exist')
    evidence, summary = build(args.contract, args.contract_sha256, args.artifact_root, args.exports)
    args.out.mkdir(parents=True)
    files = {'schedule_execution_evidence.json': evidence,
             'yield_summary.json': (json.dumps(summary, indent=2, sort_keys=True) + '\n').encode()}
    for name, raw in files.items():
        (args.out / name).write_bytes(raw)
    (args.out / 'SHA256SUMS').write_bytes(''.join(f'{sha(raw)} *{name}\n' for name, raw in files.items()).encode())
    print(f'R1R2_EVIDENCE sha256={sha(evidence)}')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Refusal as exc:
        print(f'R1R2_EVIDENCE REFUSED {exc}', file=sys.stderr)
        sys.exit(2)
