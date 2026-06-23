#!/usr/bin/env bash
# get-node: install once, then run — auto-discovered, no registry path.
set -euo pipefail
urirun install urirun-connector-get-node            # local dev: pip install -e .
urirun run 'node://get/installer/query/script' --payload '{}' --execute --allow 'node://*'
