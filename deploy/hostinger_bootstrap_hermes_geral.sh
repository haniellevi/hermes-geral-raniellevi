#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/hermes-geral}"
REPO_URL="${REPO_URL:-}"

echo "[Hermes Geral] Preparando VPS em ${APP_DIR}"

if ! command -v docker >/dev/null 2>&1; then
  curl -fsSL https://get.docker.com | sh
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose plugin nao encontrado. Instale o plugin docker-compose antes de continuar."
  exit 1
fi

mkdir -p "${APP_DIR}"

if [ -n "${REPO_URL}" ]; then
  if [ -d "${APP_DIR}/.git" ]; then
    git -C "${APP_DIR}" pull --ff-only
  else
    rm -rf "${APP_DIR:?}"/*
    git clone "${REPO_URL}" "${APP_DIR}"
  fi
fi

cd "${APP_DIR}"

if [ ! -f ".env" ]; then
  cp .env.example .env
  echo "Arquivo .env criado. Configure TELEGRAM_BOT_TOKEN e OPENAI_API_KEY antes de subir."
  exit 0
fi

docker compose up -d --build
docker compose ps

echo "[Hermes Geral] Deploy concluido."
