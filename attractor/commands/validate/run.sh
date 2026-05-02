#!/bin/sh
set -eu

exec python3 "$GC_PACK_DIR/scripts/attractor_cli.py" validate "$@"
