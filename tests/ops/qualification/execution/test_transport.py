"""Real sockets enforce one frame deadline even when a peer keeps sending."""
from concurrent.futures import ThreadPoolExecutor
import socket
import time

import pytest

from c1_rail.qualification.execution.protocol import encode_frame
from c1_rail.qualification.execution.transport import receive


def test_dripping_frame_cannot_extend_connection_deadline():
    reader, writer = socket.socketpair()
    reader.settimeout(0.15)

    def drip():
        try:
            for byte in encode_frame(b'{}', limit=100):
                writer.sendall(bytes([byte]))
                time.sleep(0.06)
            writer.shutdown(socket.SHUT_WR)
        except OSError:
            pass

    with ThreadPoolExecutor(max_workers=1) as pool:
        pending = pool.submit(drip)
        try:
            with pytest.raises(TimeoutError):
                receive(reader, limit=100)
        finally:
            reader.close()
            pending.result(timeout=2)
            writer.close()


def test_complete_frame_with_finite_deadline_is_accepted():
    reader, writer = socket.socketpair()
    try:
        reader.settimeout(1)
        writer.sendall(encode_frame(b'{}', limit=100))
        writer.shutdown(socket.SHUT_WR)
        assert receive(reader, limit=100) == b'{}'
        assert reader.gettimeout() == 1
    finally:
        reader.close()
        writer.close()
