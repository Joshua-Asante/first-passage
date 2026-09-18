"""Archive immutable bytes only after complete, normal daemon-observed exit."""
from .files import archive_bytes
from .protocol import decode_frame


def archive_capture(capture, *, archive_dir):
    if capture.exit_code != 0 or capture.oom_killed:
        raise ValueError('abnormal worker completion')
    raw = decode_frame(capture.result_bytes, limit=max(1, len(capture.result_bytes)))
    return {archive_bytes(archive_dir, raw): raw}
