"""Administrator fixture operations in PR420's protected staged checkout.

This script creates TEST_ONLY approvals, never outcomes or execution attestations.
It is not an active service entrypoint and is not included in the worker image.
"""
import argparse
import base64
import json
import os
from pathlib import Path
import sys

CODE=Path(__file__).resolve().parents[3]
if sys.platform!='linux' or not sys.flags.isolated or os.geteuid()!=0:
    raise SystemExit('isolated disposable Linux administrator required')
sys.dont_write_bytecode=True
sys.path[:0]=[str(CODE/part) for part in ('ops','core','lab','governance','',
    'tests/ops/qualification','tests/ops/qualification/execution','tests/integration/qualification_boundary')]

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from c1_rail.qualification.contract import canonical_json_bytes as encoded,TrustedApprovalKey
from c1_rail.qualification.execution.release import install_release,stage_bundle
from c1_rail.qualification.execution.runtime import protected_path
from c1_rail.qualification.execution.protocol import sha256
from tools.qualification_verification import host
from fixture_producer import fresh_keys,approve,release_document,build_real_bundle


def write(path,raw,*,uid=0,gid=None,mode=0o444):
    with path.open('xb') as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    os.chown(path,uid,uid if gid is None else gid); path.chmod(mode)


def install(root,manifest,image):
    private,keys,registry=fresh_keys(execution_seed=(root/'keys/qexec/TEST_ONLY.key').read_bytes(),
                                   result_seed=(root/'keys/qg5/TEST_ONLY.key').read_bytes())
    roles=manifest['roles']; installation=CODE/'qualification-installation'
    installation.mkdir(mode=0o755)
    write(installation/'keys.json',registry)
    write(CODE/'bootstrap.py',(CODE/'deploy/qualification/bootstrap.py').read_bytes())
    for name,key in (('qexec','test-execution'),('qg5','test-producer')):
        write(root/'keys'/name/'credential.json',encoded(dict(schema='qualification_private_credential/v1',
            key_id=key,authority_class='TEST_ONLY',private_seed_b64=base64.b64encode(private[key].private_bytes_raw()).decode())),
            uid=roles[name],mode=0o400)
    write(root/'keys/test-authority.json',encoded({name:base64.b64encode(key.private_bytes_raw()).decode()
        for name,key in private.items()}),mode=0o400)
    socket_root=root/'keys/socket'; socket_root.mkdir(mode=0o750)
    os.chown(socket_root,roles['qexec'],roles['qclient'])
    socket_root.chmod(0o2750)
    scratch=root/'keys/qg5/scratch'; scratch.mkdir(mode=0o700); os.chown(scratch,roles['qg5'],roles['qg5'])
    config=dict(schema='qualification_execution_instance/v1',authority_class='TEST_ONLY',host_run_id=root.name,
        installation_root=str(installation),data_root=str(root/'data'),daemon_data_root=str(root/'data'),
        socket_path=str(socket_root/'service.sock'),socket_gid=roles['qclient'],client_uid=roles['qclient'],
        service_uid=roles['qexec'],g5_uid=roles['qg5'],operator_uid=0,
        execution_credential=str(root/'keys/qexec/credential.json'))
    profile=json.loads((CODE/'deploy/qualification/test-profile.json').read_bytes())
    release=encoded(release_document(CODE,profile,image,keys))
    install_release(release,approve(release,private,'APPROVE_EXECUTION_RELEASE'),instance_config=encoded(config))
    write(installation/'g5.json',encoded(dict(installation_root=str(installation),socket_path=config['socket_path'],
        g5_uid=roles['qg5'],scratch_root=str(scratch),result_credential=str(root/'keys/qg5/credential.json'))))
    write(installation/'profile.json',encoded(profile))
    instance=dict(schema='qualification_test_instance/v1',authority_class='TEST_ONLY',roles=roles,
        trusted_roots=[str(CODE),str(root/'env')],data=str(root/'data'),
        execution_key=config['execution_credential'],result_key=str(root/'keys/qg5/credential.json'),
        scratch=str(root/'scratch'),evidence=str(root/'evidence'),docker_socket='/var/run/docker.sock',
        worker_image_id=image,profile_sha256=sha256(encoded(profile)))
    write(installation/'test-instance.json',encoded(instance))
    host.enroll_boundary(root,image_id=image,release_bytes=release)
    write(root/'evidence/release.json',release)
    return dict(installation_root=str(installation),image_id=image)


def prepare(root,attempt,idle,*,fault=None,depth_valid_seconds=14400):
    private={name:Ed25519PrivateKey.from_private_bytes(base64.b64decode(value))
        for name,value in json.loads((root/'keys/test-authority.json').read_bytes()).items()}
    keys={name:TrustedApprovalKey(name,key.public_key().public_bytes_raw(),'TEST_ONLY') for name,key in private.items()}
    installation=CODE/'qualification-installation'
    release=(installation/'release.json').read_bytes()
    from c1_rail.qualification.execution.protocol import identity
    identity(attempt)
    source=root/'keys/retained'/attempt
    bundle=build_real_bundle(source,repo=CODE,release=release,private=private,keys=keys,attempt_id=attempt,idle=idle,
        fault=fault,depth_valid_seconds=depth_valid_seconds)
    # Administrator pre-dispatch diagnostics, not protected worker attestation.
    write(root/'evidence'/f'{attempt}-source-admission.json',bundle['source_admission'])
    write(root/'evidence'/f'{attempt}-legality.json',bundle['legality'])
    digest=stage_bundle(source,instance_config=(installation/'supervisor.json').read_bytes())
    expires=json.loads(bundle['payloads']['exact_depth_approval'])['payload']['expires_at']
    return dict(attempt_id=attempt,bundle_sha256=digest,contract_sha256=bundle['contract'].contract_sha256,
        depth_expires_at=expires)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('operation',choices=['install','prepare','void-approval'])
    parser.add_argument('--manifest',type=Path,required=True)
    parser.add_argument('--image'); parser.add_argument('--attempt'); parser.add_argument('--idle',action='store_true')
    parser.add_argument('--contract'); parser.add_argument('--reason')
    parser.add_argument('--fault',choices=['stop','partial_output','exit_zero','cpu','memory','wall'])
    parser.add_argument('--depth-valid-seconds',type=int,default=14400)
    args=parser.parse_args()
    path=host.protected(args.manifest); root=path.parent
    manifest=json.loads(path.read_bytes())
    protected_path(CODE)
    if CODE!=root/'code' or manifest['run_id']!=root.name:
        raise ValueError('fixture must run from canonical protected source staging')
    if args.operation=='void-approval':
        private={name:Ed25519PrivateKey.from_private_bytes(base64.b64decode(value))
            for name,value in json.loads((root/'keys/test-authority.json').read_bytes()).items()}
        subject=encoded(dict(attempt_id=args.attempt,reason=args.reason,contract_sha256=args.contract))
        approval=approve(subject,private,'VOID_QUALIFICATION_ATTEMPT',contract_sha256=args.contract)
        result=dict(operator_approval_bytes=base64.b64encode(approval).decode())
    else:
        result=install(root,manifest,args.image) if args.operation=='install' else prepare(root,args.attempt,args.idle,
            fault=args.fault,depth_valid_seconds=args.depth_valid_seconds)
    sys.stdout.buffer.write(encoded(result))


if __name__=='__main__': main()
