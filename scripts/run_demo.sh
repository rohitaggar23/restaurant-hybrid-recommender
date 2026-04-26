#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHONPATH=src "${PYTHON:-python3}" -m restaurant_recsys.cli --user-id u1 --query "spicy noodles" --lat 40.73 --lon -73.99
