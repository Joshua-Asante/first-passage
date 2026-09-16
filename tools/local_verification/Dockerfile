FROM python:3.11-slim-bookworm@sha256:528257d48c1da0dcecc2e725d1ae34498d60c965f1241e39cd6a85a8859bdf84
RUN apt-get update && apt-get install -y --no-install-recommends git ripgrep && rm -rf /var/lib/apt/lists/*
RUN python -m venv /opt/ops
ENV PATH="/opt/ops/bin:${PATH}" PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
COPY requirements-ops.lock requirements-extra.txt /build/
RUN python -m pip install --require-hashes -r /build/requirements-ops.lock && python -m pip install -r /build/requirements-extra.txt && python -m pip check
WORKDIR /repo
