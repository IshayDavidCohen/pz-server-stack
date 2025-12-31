#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

SERVICE_NAME="${SERVICE_NAME:-pz_srv}"
FOLLOW_LOGS="${FOLLOW_LOGS:-1}"   # 1 = follow logs, 0 = don't
PULL_FIRST="${PULL_FIRST:-0}"     # 1 = docker compose pull, 0 = skip

if [[ "$PULL_FIRST" == "1" ]]; then
  docker compose pull
fi

docker compose up -d
docker compose ps

if [[ "$FOLLOW_LOGS" == "1" ]]; then
  docker compose logs -f --tail=200 "$SERVICE_NAME"
fi
