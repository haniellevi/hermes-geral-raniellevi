# Hermes Desenvolvedor Local + Codex CLI

## Decisao

Para desenvolvimento, o Hermes Desenvolvedor roda no proprio computador do usuario.

Isso evita fila, tunel reverso, webhook local e execucao remota pela VPS. O bot do Telegram usa polling, entao nao precisa abrir porta publica no PC.

## Como funciona

```text
Telegram Desenvolvedor
  -> app.telegram_bot rodando no PC
    -> comando /codex
      -> codex exec local
        -> pastas autorizadas do PC
```

## Comando para iniciar no PC

```powershell
powershell -ExecutionPolicy Bypass -File scripts\start_hermes_dev_local.ps1
```

Esse script liga:

```env
HERMES_CODEX_LOCAL_ENABLED=1
```

## Comando no Telegram

```text
/codex hermes-geral | verifique o status do git e rode os testes
/codex hermes-pastoral | analise o README e diga qual a proxima tarefa
```

Projetos permitidos:

- `hermes-geral`
- `hermes-pastoral`

Aliases aceitos:

- `geral`
- `desenvolvedor`
- `pastoral`
- `gestao-pastoral`

## Seguranca

- A execucao do Codex so acontece se `HERMES_CODEX_LOCAL_ENABLED=1`.
- Essa variavel deve ficar ligada apenas no PC local.
- A VPS nao deve habilitar `HERMES_CODEX_LOCAL_ENABLED`.
- O Telegram deve ter `TELEGRAM_ALLOWED_CHAT_IDS` preenchido.
- O Codex so executa nas pastas de projeto permitidas em `app/local_codex.py`.
- Nao existe endpoint publico de execucao no computador.

## Codex CLI

O Hermes chama:

```powershell
codex exec -c model_reasoning_effort=high -C "<pasta-do-projeto>" --full-auto "<pedido>"
```

Se aparecer `401 Unauthorized`, o Codex CLI local precisa de login:

```powershell
codex login
codex login status
```

Se aparecer erro de modelo nao suportado, ajuste o modelo do Codex CLI ou defina:

```env
HERMES_CODEX_MODEL=modelo-que-funciona-no-seu-codex-cli
```

## Observacao

Quando o computador estiver desligado, o Hermes local nao executa Codex nem acessa pastas locais. A VPS pode continuar respondendo conversas normais, mas desenvolvimento local depende do PC ligado.
