#!/usr/bin/env bash
set -euo pipefail

NETWORK="${NETWORK:-hermes-agents}"

docker network inspect "${NETWORK}" >/dev/null 2>&1 || docker network create "${NETWORK}"

connect_if_running() {
  local container="$1"
  local alias="$2"

  if ! docker inspect "${container}" >/dev/null 2>&1; then
    echo "[skip] container nao encontrado: ${container}"
    return 0
  fi

  if docker inspect "${container}" --format '{{json .NetworkSettings.Networks}}' | grep -q "\"${NETWORK}\""; then
    echo "[ok] ${container} ja esta na rede ${NETWORK}"
    return 0
  fi

  docker network connect --alias "${alias}" "${NETWORK}" "${container}"
  echo "[ok] ${container} conectado como ${alias}"
}

connect_if_running "hermes-api" "hermes-pastoral-api"
connect_if_running "hermes-dashboard" "hermes-pastoral-dashboard"
connect_if_running "hermes-geral-api" "hermes-geral-api"
connect_if_running "hermes-geral-telegram" "hermes-geral-telegram"

echo "[Hermes] rede compartilhada pronta: ${NETWORK}"
