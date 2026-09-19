"""Bounded generic transport for the private scheduler route; no campaign imports.

Test orchestration (the parent) pre-encodes one closed schedule frame. An
already-initialized forked child adopts the service identity, opens the Unix
socket, moves that frame in and one reply out, then exits. The child selects
no code, path, credential, counter or limit and performs no campaign
computation; the warm installed service is the only intent producer.
"""
import os
import socket

from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution.protocol import encode_frame
from c1_rail.qualification.execution.transport import receive

SCHEDULE_SCHEMA = 'qualification_campaign_schedule_request/v1'
FRAME_LIMIT = 1024        # the service's private-route framing bound
REPLY_LIMIT = 1024 * 1024  # bounded compact status reply; never a plan chunk


def schedule_frame(document):
    """Pre-encode one closed private request; the child never sees a document."""
    if type(document) is not dict or document.get('schema') != SCHEDULE_SCHEMA:
        raise ValueError('private route carries only the schedule schema')
    return encode_frame(encoded(document), limit=FRAME_LIMIT)


def exchange(peer, frame, *, timeout, reply_limit=REPLY_LIMIT):
    """One pre-encoded frame in, one bounded reply out, on a connected stream."""
    if type(frame) is not bytes or not 4 < len(frame) <= FRAME_LIMIT + 4:
        raise ValueError('bounded pre-encoded frame required')
    peer.settimeout(timeout)
    peer.sendall(frame)
    peer.shutdown(socket.SHUT_WR)
    return receive(peer, limit=reply_limit)


def forked_exchange(frame, *, socket_path, uid, gid, groups, timeout=30):
    """Fork after preload; adopt the fixed identity before connecting."""
    if type(frame) is not bytes or not 4 < len(frame) <= FRAME_LIMIT + 4:
        raise ValueError('bounded pre-encoded frame required')
    reader, writer = os.pipe()
    pid = os.fork()
    if pid == 0:
        status = 1
        try:
            os.close(reader)
            os.setgroups(list(groups))
            os.setgid(gid)
            os.setuid(uid)
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as peer:
                peer.settimeout(timeout)
                peer.connect(socket_path)
                reply = exchange(peer, frame, timeout=timeout)
            view = memoryview(reply)
            while view:
                view = view[os.write(writer, view):]
            status = 0
        finally:
            os._exit(status)
    os.close(writer)
    with os.fdopen(reader, 'rb') as stream:
        reply = stream.read()
    _, code = os.waitpid(pid, 0)
    if os.waitstatus_to_exitcode(code) != 0:
        raise ValueError('private transport child failed')
    return reply
