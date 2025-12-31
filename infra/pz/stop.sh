#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

SERVICE_NAME="${SERVICE_NAME:-pz_srv}"

# If you only want to stop the container(s) but keep the network/volumes:
docker compose stop "$SERVICE_NAME"

# Show status after stop
docker compose ps
