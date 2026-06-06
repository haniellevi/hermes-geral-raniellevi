# Deploy do Hermes Geral na VPS

## Objetivo

Rodar o Hermes Geral 24h na VPS, separado do Hermes Pastoral.

Endpoint do Hermes Geral:

```text
POST /webhook/botconversa
GET /health
```

Porta padrao:

```text
5060
```

## Numero autorizado

O Hermes Geral so deve responder ao numero pessoal:

```text
89994315927
5589994315927
```

Configure no `.env`:

```env
HERMES_GERAL_OWNER_PHONES=89994315927,5589994315927
```

## Variaveis

Copie `.env.example` para `.env` e configure:

```env
HERMES_GERAL_OWNER_PHONES=89994315927,5589994315927
HERMES_GERAL_DB_PATH=database/hermes_geral.db
GEMINI_API_KEY=
GOOGLE_API_KEY=
HERMES_GERAL_COMMON_MODEL=gemini-2.5-flash
HERMES_GERAL_DEV_MODEL=gemini-2.5-pro
OPENAI_API_KEY=
OPENROUTER_API_KEY=
OPENAI_MODEL=openai/gpt-4.1-mini
OPENAI_BASE_URL=
HERMES_GERAL_PORT=5060
TELEGRAM_BOT_TOKEN=
TELEGRAM_ALLOWED_CHAT_IDS=
```

## Subir com Docker

```bash
docker compose up -d --build
```

Validar:

```bash
curl http://localhost:5060/health
docker compose logs -f hermes-geral-telegram
```

Conectar na rede compartilhada dos agentes:

```bash
bash deploy/connect_existing_agents.sh
```

## Bootstrap opcional

Na VPS, o caminho recomendado e:

```text
/opt/hermes-geral
```

Se o projeto ja estiver copiado para a VPS:

```bash
cd /opt/hermes-geral
cp .env.example .env
nano .env
docker compose up -d --build
```

Se for clonar por GitHub, use:

```bash
APP_DIR=/opt/hermes-geral REPO_URL=https://github.com/SEU_USUARIO/SEU_REPO.git bash deploy/hostinger_bootstrap_hermes_geral.sh
```

## BotConversa

No fluxo privado do seu numero pessoal, configurar webhook:

```text
POST https://SEU-DOMINIO-DO-HERMES-GERAL/webhook/botconversa
```

Payload minimo esperado:

```json
{
  "telefone": "{{telefone}}",
  "nome": "{{nome}}",
  "mensagem": "{{mensagem}}"
}
```

O servico bloqueia qualquer telefone diferente dos numeros em `HERMES_GERAL_OWNER_PHONES`.

## Separacao obrigatoria

Nao apontar esse webhook para o dominio/servico do Hermes Pastoral.
Nao usar banco pastoral.
Nao gravar memoria do Hermes Geral dentro de `HERMES-LOCAL/conhecimento`.

## Telegram Desenvolvedor

O Telegram do Hermes Geral roda como servico separado:

```text
hermes-geral-telegram
```

Ele usa polling via Bot API, entao nao precisa expor webhook publico.

Depois de iniciar, mande `/start` no bot. Ele respondera seu `chat_id`.
Em seguida, coloque esse ID no `.env`:

```env
TELEGRAM_ALLOWED_CHAT_IDS=SEU_CHAT_ID
```

E reinicie:

```bash
docker compose up -d
```
