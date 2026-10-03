"""Administrator bundle preparation for the S8 derived source scenarios.

Delegates to fixture_install.prepare -- its isolated-Linux-administrator check,
canonical source staging, signed TEST_ONLY approvals and bundle staging are
unchanged -- and widens only the source-scenario port transform to the
campaign_sources registry (the idle-pair scenarios n2_full_fails and
n2_halves_fail). It never produces outcomes, attestations or receipts. Not an
active service entrypoint and not in the worker image.
"""
# fixture_install sets the import path first.
# pylint: disable=wrong-import-position
import argparse
import json
from pathlib import Path
import sys

_HERE = Path(__file__).resolve().parent
# -I drops the script directory from sys.path; fixture_install adds the rest.
sys.path.insert(0, str(_HERE))

import fixture_install  # noqa: E402  (performs the administrator check first)
import fixture_producer  # noqa: E402
import campaign_sources  # noqa: E402
from c1_rail.qualification.contract import canonical_json_bytes as encoded  # noqa: E402
from c1_rail.qualification.execution.runtime import protected_path  # noqa: E402
from tools.qualification_verification import host  # noqa: E402

_PRODUCER_TRANSFORM = fixture_producer.scenario_port_transform


def scenario_port_transform(scenario):
    """The S8 derived scenarios' transform; every other scenario is the producer's."""
    if scenario in campaign_sources.DERIVED:
        return campaign_sources.port_transform(scenario)
    return _PRODUCER_TRANSFORM(scenario)


def main():
    """``prepare`` one derived-scenario bundle; prints fixture_install's result."""
    parser =argparse.ArgumentParser()
    parser.add_argument('operation', choices=['prepare'])
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--attempt', required=True)
    parser.add_argument('--scenario', choices=list(campaign_sources.DERIVED), required=True)
    parser.add_argument('--depth-valid-seconds', type=int, default=14400)
    args = parser.parse_args()
    path = host.protected(args.manifest)
    root = path.parent
    manifest = json.loads(path.read_bytes())
    protected_path(fixture_install.CODE)
    if fixture_install.CODE != root / 'code' or manifest['run_id'] != root.name:
        raise ValueError('fixture must run from canonical protected source staging')
    # build_real_bundle resolves the transform at call time from its module.
    fixture_producer.scenario_port_transform = scenario_port_transform
    result = fixture_install.prepare(root, args.attempt, False, scenario=args.scenario,
                                     depth_valid_seconds=args.depth_valid_seconds)
    sys.stdout.buffer.write(encoded(result))


if __name__ == '__main__':
    main()
