#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.."
exec /usr/bin/python3 -I tools/qualification_verification/host.py "$@"
