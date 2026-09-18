"""One bounded canonical frame per Unix-stream connection."""
import struct
import time
from .protocol import decode_frame


def receive(connection, *, limit):
    timeout = connection.gettimeout()
    if timeout is None or timeout <= 0:
        raise ValueError('finite positive frame timeout required')
    deadline = time.monotonic() + timeout

    def bounded_recv(count):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError('frame deadline exceeded')
        connection.settimeout(remaining)
        return connection.recv(count)

    def exact(count):
        chunks = bytearray()
        while len(chunks) < count:
            chunk = bounded_recv(min(65536, count - len(chunks)))
            if not chunk:
                raise ValueError('truncated frame')
            chunks.extend(chunk)
        return bytes(chunks)
    try:
        header = exact(4)
        length = struct.unpack('!I', header)[0]
        if not 0 < length <= limit:
            raise ValueError('frame exceeds limit')
        raw = exact(length)
        if bounded_recv(1):
            raise ValueError('trailing frame')
        return decode_frame(header + raw, limit=limit)
    finally:
        connection.settimeout(timeout)
