# Ponte Local Codex -> Hermes Geral

## Objetivo

Permitir que o Hermes Geral na VPS consulte chats locais do Codex sem abrir acesso irrestrito ao computador.

## Como funciona agora

O computador local exporta os chats do Codex para Markdown sanitizado:

```text
HERMES-GERAL/conhecimento/codex_chats/
```

Depois sincroniza essa pasta para:

```text
/opt/hermes-geral/conhecimento/codex_chats/
```

Como o Hermes Geral lê `conhecimento/` a cada resposta, ele passa a conseguir consultar esses chats.

## Comando local

```powershell
powershell -ExecutionPolicy Bypass -File scripts\sync_codex_chats_to_vps.ps1
```

## Segurança

O exportador mascara padrões comuns de segredo:

- `github_pat_...`
- `sk-...`
- `AIza...`
- tokens de Telegram no formato `numero:token`
- tokens Google iniciados com `AQ.`

Ainda assim, os chats podem conter informação sensível. Por isso a pasta `conhecimento/codex_chats/` fica fora do Git.

## Próxima etapa

Para execução remota de comandos, criar um runner local separado com fila e allowlist. A leitura de chats já está resolvida por sincronização push local -> VPS.
