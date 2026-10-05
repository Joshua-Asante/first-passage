"""``python -m c1_rail.qualification.t00_screen {preflight|accept-p7|run|resume|finalize|verify|act}``.

Each subcommand prints only its fixed lines (design §5.6, row X1); stderr carries one refusal
code and nothing else. An unexpected exception prints ``UNCLASSIFIED_ERROR`` and its traceback
goes to the run directory's ``errors/``. No count, rate, key, progress or timing is printed.
"""
from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path
import sys
import warnings

from . import coordinator

SUBCOMMANDS = ('preflight', 'accept-p7', 'run', 'resume', 'finalize', 'verify', 'act')


class _Usage(Exception):
    """A malformed command line: the refusal code is USAGE."""


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise _Usage(message)


def _parser() -> _Parser:
    parser = _Parser(prog='t00_screen', add_help=False)
    parser.add_argument('subcommand', choices=SUBCOMMANDS)
    for name in ('--authority', '--approval', '--source-contract', '--source-approval', '--registry',
                 '--p7-record', '--artifact-root', '--act', '--act-approval'):
        parser.add_argument(name)
    parser.add_argument('--workers', type=int)
    return parser


def _inputs(options) -> coordinator.Inputs:
    names = ('authority', 'approval', 'source_contract', 'source_approval', 'registry', 'p7_record', 'artifact_root')
    if any(getattr(options, name) is None for name in names):
        raise _Usage('every launch input is required')
    registry = json.loads(Path(options.registry).read_text(encoding='utf-8'))
    return coordinator.Inputs(
        authority=Path(options.authority).read_bytes(), approval=Path(options.approval).read_bytes(),
        source_contract=Path(options.source_contract).read_bytes(),
        source_approval=Path(options.source_approval).read_bytes(),
        public_keys={key: base64.b64decode(value, validate=True) for key, value in registry.items()},
        p7_record=Path(options.p7_record).read_bytes(), artifact_root=Path(options.artifact_root))


def _stop_line(stop: coordinator.Stop) -> str:
    if stop.kind == coordinator.COMPLETE:
        return 'T00_SCREEN_COMPLETE'
    return f'T00_SCREEN_{stop.kind} {stop.code}'


def _dispatch(options, out) -> None:
    command = options.subcommand
    if command == 'accept-p7':
        if None in (options.p7_record, options.artifact_root, options.registry):
            raise _Usage('accept-p7 needs --p7-record, --artifact-root and --registry')
        registry = json.loads(Path(options.registry).read_text(encoding='utf-8'))
        digest = coordinator.accept_p7(
            p7_record=Path(options.p7_record).read_bytes(), artifact_root=Path(options.artifact_root),
            public_keys={key: base64.b64decode(value, validate=True) for key, value in registry.items()})
        out(f'T00_SCREEN_P7_ACCEPTED acceptance_sha256={digest}')
        return
    inputs = _inputs(options)
    if command == 'preflight':
        out(f'T00_SCREEN_PREFLIGHT OK authority_sha256={coordinator.preflight(inputs)}')
    elif command in ('run', 'resume'):
        call = coordinator.run if command == 'run' else coordinator.resume
        stop = call(inputs, workers=options.workers,
                    on_launch=lambda digest: out(f'T00_SCREEN_RUN authority_sha256={digest}'))
        out(_stop_line(stop))
    elif command == 'finalize':
        label, digest = coordinator.finalize(inputs)
        out(f'T00_SCREEN_VERDICT {label} results_sha256={digest}')
    elif command == 'verify':
        out(f'T00_SCREEN_VERIFY {coordinator.verify(inputs)}')
    else:
        if options.act is None or options.act_approval is None:
            raise _Usage('act needs --act and --act-approval')
        kind, digest = coordinator.act(inputs, Path(options.act).read_bytes(), Path(options.act_approval).read_bytes())
        out(f'T00_SCREEN_ACT_RECORDED {kind} act_sha256={digest}')


def main(argv=None, *, stdout=None, stderr=None) -> int:
    """Run one subcommand; the exit status is 0, or the refusal's class."""
    stdout, stderr = stdout or sys.stdout, stderr or sys.stderr
    warnings.simplefilter('ignore')  # row X1: nothing but the fixed lines

    def out(line):
        stdout.write(line + '\n')
        stdout.flush()
    inputs = None
    try:
        options = _parser().parse_args(sys.argv[1:] if argv is None else argv)
        if options.subcommand != 'accept-p7' and None not in (options.authority, options.artifact_root):
            try:
                inputs = _inputs(options)
            except (OSError, ValueError, _Usage):
                inputs = None
        _dispatch(options, out)
        return 0
    except _Usage:
        stderr.write('USAGE\n')
        return 2
    except coordinator.ScreenRefusal as refusal:
        stderr.write(refusal.code + '\n')
        return 3
    except OSError:
        stderr.write('IO_ERROR\n')
        return 4
    except KeyboardInterrupt:
        stderr.write('INTERRUPTED\n')
        return 130
    except Exception as exc:  # pylint: disable=broad-exception-caught  # row X1: the code only
        coordinator.write_error(inputs, exc)
        stderr.write('UNCLASSIFIED_ERROR\n')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
