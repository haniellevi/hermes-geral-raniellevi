#!/bin/bash
# deploy_web_navigator.sh
# Script de deploy do serviço web_navigator na VPS
# Uso: bash deploy_web_navigator.sh

set -e

DEPLOY_DIR="/opt/hermes-geral/scripts"
SERVICE_NAME="web_navigator"
SERVICE_FILE="web_navigator.service"
VENV_DIR="/opt/hermes-geral/venv"

echo "======================================"
echo " Hermes Geral — Deploy: web_navigator"
echo "======================================"

# 1. Cria diretório se não existir
mkdir -p "$DEPLOY_DIR"

# 2. Copia os arquivos
echo "[1/5] Copiando arquivos..."
cp web_navigator_service.py "$DEPLOY_DIR/"
cp web_navigator_requirements.txt "$DEPLOY_DIR/"

# 3. Cria virtualenv se não existir
if [ ! -d "$VENV_DIR" ]; then
    echo "[2/5] Criando virtualenv..."
    python3 -m venv "$VENV_DIR"
fi

# 4. Instala dependências
echo "[3/5] Instalando dependências..."
"$VENV_DIR/bin/pip" install --upgrade pip -q
"$VENV_DIR/bin/pip" install -r "$DEPLOY_DIR/web_navigator_requirements.txt" -q
echo "      ✅ Dependências instaladas"

# 5. Instala e ativa o serviço systemd
echo "[4/5] Configurando systemd..."
cp "$SERVICE_FILE" /etc/systemd/system/
systemctl daemon-reload
systemctl enable "$SERVICE_NAME"
systemctl restart "$SERVICE_NAME"

# 6. Verifica status
echo "[5/5] Verificando serviço..."
sleep 2
STATUS=$(systemctl is-active "$SERVICE_NAME")
if [ "$STATUS" = "active" ]; then
    echo ""
    echo "✅ web_navigator está ATIVO na porta 5055"
    echo ""
    echo "Teste rápido:"
    echo "  curl 'http://127.0.0.1:5055/health'"
    echo "  curl 'http://127.0.0.1:5055/search_web?query=inteligência+artificial'"
    echo "  curl 'http://127.0.0.1:5055/fetch_url?url=https://example.com'"
else
    echo "❌ FALHA ao iniciar o serviço. Status: $STATUS"
    echo "Logs: journalctl -u $SERVICE_NAME -n 30"
    exit 1
fi
