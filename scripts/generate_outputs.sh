#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export MPLBACKEND=Agg
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python scripts/generate_outputs.py
