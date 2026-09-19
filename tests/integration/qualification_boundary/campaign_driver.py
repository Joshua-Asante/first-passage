"""Privileged-harness-only bounded scheduler; no statistical or signing action."""
import argparse
import json
from pathlib import Path
import resource
import sys

CODE = Path(__file__).resolve().parents[3]
sys.dont_write_bytecode = True
sys.path[:0] = [str(CODE / part) for part in ('ops', 'core', 'lab', 'governance', '')]
from c1_rail.qualification.execution.runtime import load_instance, protected_path
from c1_rail.qualification.execution.release import parse_instance
from c1_rail.qualification.execution.service import ExecutionService
from c1_rail.qualification.contract import canonical_json_bytes as encoded

protected_path(CODE)
if resource.getrlimit(resource.RLIMIT_CPU) != (1, 1):
    raise SystemExit('bounded private scheduler required')
parser = argparse.ArgumentParser()
parser.add_argument('--attempt', required=True)
parser.add_argument('--work', required=True)
parser.add_argument('--role', choices=('probe_worker','probe_g5','probe_result','probe_seal'), required=True)
parser.add_argument('--probe', choices=('noop','cpu','descendants','wall','memory','intent','controller_cpu'), default='noop')
parser.add_argument('--retry-of')
args = parser.parse_args()
context = ExecutionService(parse_instance(encoded(load_instance(CODE / 'qualification-installation/supervisor.json'))))
sys.stdout.buffer.write(context.schedule_campaign_probe(args.attempt,args.work,args.role,args.probe,signing_retry_of=args.retry_of))
