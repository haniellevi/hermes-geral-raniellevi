# Hermes Geral

Este e o ambiente separado do **Hermes Desenvolvimento**, voltado para tecnologia, projetos, Codex, Antigravity, Claude Code, Supabase, BotConversa, programacao e automacoes.

## Separacao dos Hermes

- `HERMES-GERAL`: agente principal de desenvolvimento do usuario.
- `HERMES-LOCAL`: Hermes Agente Pastoral da Igreja Filadelfia.

O Hermes Geral pode saber tudo sobre o Hermes Pastoral para ajudar a desenvolver e manter o sistema. O Hermes Pastoral nao deve acessar automaticamente conhecimento, tarefas, banco ou decisoes do Hermes Geral.

## Estrutura

- `AGENTS.md`: regras e persona do Hermes Desenvolvimento.
- `conhecimento/`: base de conhecimento geral do Hermes Desenvolvimento.
- `tasks/`: tarefas tecnicas para Codex, Claude Code, Antigravity e outros agentes.
- `docs/`: documentacao tecnica.
- `scripts/`: automacoes locais futuras.

## Ferramentas locais detectadas

- Codex CLI: `codex`
- Claude Code CLI: `claude`
- Antigravity: instalado como app local, sem CLI no PATH no momento da verificacao.

## Proxima etapa recomendada

Criar uma ponte de tarefas em `tasks/DEV_TASKS.md` ou GitHub Issues para o Hermes Geral registrar pedidos e o Codex executar com rastreabilidade.

## WhatsApp pessoal

O numero pessoal autorizado para falar com o Hermes Geral e:

```text
89994315927
5589994315927
```

O webhook proprio do Hermes Geral fica em:

```text
POST /webhook/botconversa
```

Documentacao de deploy:

```text
docs/DEPLOY_VPS.md
```

## Telegram Desenvolvedor

O Hermes Geral tambem tem um worker Telegram separado:

```bash
python -m app.telegram_bot
```

Na VPS, ele roda pelo Docker Compose como:

```text
hermes-geral-telegram
```
