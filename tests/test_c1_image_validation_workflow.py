"""The c1 image-validation workflow is one matrix job covering both images (2026-09-17)."""
from pathlib import Path

import yaml

WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/c1-image-validation.yml"


def test_matrix_covers_both_images_with_independent_verdicts():
    jobs = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))["jobs"]
    assert list(jobs) == ["image"]
    job = jobs["image"]
    assert job["strategy"]["matrix"]["service"] == ["listener", "daemon"]
    assert job["strategy"]["fail-fast"] is False
    assert job["name"] == "${{ matrix.service }}"  # check names stay `listener` / `daemon`
    runs = [s["run"] for s in job["steps"] if "run" in s]
    assert runs == ["./scripts/c1_image_validation.sh ${{ matrix.service }}"]
    upload = [s for s in job["steps"] if "upload-artifact" in s.get("uses", "")]
    assert len(upload) == 1 and upload[0]["if"] == "always()"
    assert upload[0]["with"]["name"] == "c1-image-validation-${{ matrix.service }}"
