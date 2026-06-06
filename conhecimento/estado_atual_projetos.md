# Estado Atual dos Projetos

Este arquivo registra o estado operacional atual dos projetos conhecidos pelo Hermes Geral.

Regra de leitura:

1. Este arquivo e fonte de verdade para status atual, salvo se o usuario ou o GitHub indicarem informacao mais recente.
2. `TAREFAS.md`, `README.md`, `git log`, status local/remoto e status da VPS tem prioridade sobre chats antigos.
3. `conhecimento/codex_chats/` e apenas historico de conversas. Nao use chats antigos para concluir que um projeto ainda esta em planejamento quando houver commit, tarefa ou deploy mais recente.

## hermes-pastoral

Nome: Hermes Gestao Pastoral / Igreja Filadelfia.

Repositorio:

```text
https://github.com/haniellevi/gestor-pastoral-agente-hermes
```

Branch atual:

```text
feature/instalacao-hermes
```

Estado atual conhecido:

- Hermes Pastoral 2.0 MVP concluido e salvo no GitHub.
- Fase 1, Supabase/Banco Central Online: concluida.
- Fase 2, Deploy/VPS/SSL: concluida.
- Fase atual: Fase 3, BotConversa/WhatsApp em producao, ajustes operacionais e testes reais.
- Ultimo commit local/GitHub conhecido: `51827e5 feat: salva desenvolvimento Hermes pastoral v2`.
- A VPS pastoral ja recebeu `git pull --ff-only` para `51827e5`.
- Os containers pastorais estavam rodando sem rebuild/restart apos esse pull; se o usuario perguntar sobre execucao real, avisar que pode ser necessario rebuild/restart para a imagem refletir o codigo novo.

Resposta correta quando perguntarem o estagio:

```text
O projeto nao esta mais em planejamento inicial. O Hermes Pastoral 2.0 MVP ja esta concluido, salvo no GitHub e sincronizado na VPS. A fase atual e BotConversa/WhatsApp em producao, com ajustes operacionais e testes reais.
```

## hermes-geral

Nome: Hermes Geral / Desenvolvedor.

Repositorio:

```text
https://github.com/haniellevi/hermes-geral-raniellevi
```

Branch atual:

```text
main
```

Estado atual conhecido:

- Agente separado do Hermes Pastoral.
- Telegram Desenvolvedor ativo.
- Modelo comum configurado para Gemini Flash rapido.
- Modo desenvolvimento `/dev` configurado para modelo Gemini de desenvolvimento.
- Base de conhecimento propria em `conhecimento/`.
- Chats locais do Codex podem ser exportados para `conhecimento/codex_chats/`, mas sao historico e nao substituem o estado atual dos repositorios.
