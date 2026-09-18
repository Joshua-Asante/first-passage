"""Capture archival requires a complete frame and normal observed exit."""
import importlib
from dataclasses import replace
import pytest
from c1_rail.qualification.execution.protocol import CapturedOutput, encode_frame, sha256


def capture():
    return CapturedOutput('c'*64, encode_frame(b'{"observed":true}',limit=1024), 0, False, 100)


def test_complete_capture_archives_exact_observed_bytes(tmp_path):
    archive = importlib.import_module('c1_rail.qualification.execution.archive')
    raw = b'{"observed":true}'
    assert archive.archive_capture(capture(), archive_dir=tmp_path) == {sha256(raw):raw}
    assert (tmp_path/sha256(raw)).read_bytes() == raw


@pytest.mark.parametrize('changes', [dict(exit_code=1),dict(oom_killed=True),
    dict(result_bytes=b'broken'),dict(result_bytes=encode_frame(b'{}',limit=1024)+b'extra'),
    dict(result_bytes=encode_frame(b'{}',limit=1024)[:-1])])
def test_abnormal_or_incomplete_capture_publishes_nothing(tmp_path,changes):
    archive = importlib.import_module('c1_rail.qualification.execution.archive')
    with pytest.raises(ValueError):
        archive.archive_capture(replace(capture(),**changes),archive_dir=tmp_path)
    assert list(tmp_path.iterdir()) == []
