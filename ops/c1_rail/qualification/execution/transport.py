"""One bounded canonical frame per Unix-stream connection."""
import struct
from .protocol import decode_frame


def receive(connection, *, limit):
    def exact(count):
        chunks = bytearray()
        while len(chunks) < count:
            chunk = connection.recv(min(65536, count - len(chunks)))
            if not chunk:
                raise ValueError('truncated frame')
            chunks.extend(chunk)
        return bytes(chunks)
    header = exact(4)
    length = struct.unpack('!I', header)[0]
    if not 0 < length <= limit:
        raise ValueError('frame exceeds limit')
    raw = exact(length)
    if connection.recv(1):
        raise ValueError('trailing frame')
    return decode_frame(header + raw, limit=limit)
