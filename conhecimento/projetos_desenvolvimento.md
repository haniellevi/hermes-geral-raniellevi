# Projetos de Desenvolvimento do Hermes Geral

Este arquivo e o registro de projetos que o Hermes Geral pode desenvolver ou coordenar.

## Regra de Identificacao

Antes de iniciar qualquer desenvolvimento, o Hermes Geral deve identificar o projeto alvo.

Se o usuario disser apenas "Hermes", perguntar se e:

1. **Hermes Geral / Desenvolvedor**
2. **Hermes Gestao Pastoral / Igreja Filadelfia**
3. Outro projeto

Nao assumir o projeto quando houver ambiguidade.

## Projeto: Hermes Geral / Desenvolvedor

Nome canonico: `hermes-geral`

Aliases:

- Hermes Geral
- Hermes Desenvolvedor
- Desenvolvedor
- agente desenvolvedor
- bot desenvolvedor
- Telegram Desenvolvedor

GitHub:

```text
https://github.com/haniellevi/hermes-geral-raniellevi
```

Pasta local:

```text
C:\Users\hanie\OneDrive\Documentos\WORKSPACE\Projetos Locais\HERMES-GERAL
```

Pasta na VPS:

```text
/opt/hermes-geral
```

Branch padrao:

```text
main
```

Servicos na VPS:

```text
hermes-geral-api
hermes-geral-telegram
```

Responsabilidade:

- desenvolvimento de projetos;
- Codex, Claude Code, Antigravity;
- planejamento tecnico;
- GitHub;
- Supabase;
- BotConversa;
- VPS;
- comunicacao futura com outros agentes.

## Projeto: Hermes Gestao Pastoral / Igreja Filadelfia

Nome canonico: `hermes-pastoral`

Aliases:

- Hermes Pastoral
- Hermes Gestao Pastoral
- Gestao Pastoral
- Igreja Filadelfia
- Rute
- Caleb
- Barnabe
- Neemias
- G12
- dashboard pastoral
- WhatsApp pastoral

GitHub:

```text
https://github.com/haniellevi/gestor-pastoral-agente-hermes
```

Pasta local:

```text
C:\Users\hanie\OneDrive\Documentos\WORKSPACE\Projetos Locais\Gestao Pastoral - Pr Raniel Levi\HERMES-LOCAL
```

Pasta na VPS:

```text
/opt/gestor-pastoral-agente-hermes/HERMES-LOCAL
```

Branch atual usada:

```text
feature/instalacao-hermes
```

Servicos na VPS:

```text
hermes-api
hermes-dashboard
hermes-drive-sync
hermes-caddy
```

Responsabilidade:

- atendimento pastoral;
- WhatsApp do Gestor Pastoral;
- BotConversa pastoral;
- agenda, G12, consolidacao, conteudo e produtividade pastoral;
- banco pastoral e Supabase pastoral;
- dashboard pastoral.

## Regra de Trabalho por Projeto

Sempre que for desenvolver:

1. Identificar projeto alvo.
2. Confirmar caminho local.
3. Rodar `scripts/check_git_freshness.ps1` no caminho local do projeto.
4. Se sincronizado, trabalhar localmente.
5. Commitar e fazer push no GitHub correto.
6. Se a VPS precisar refletir a mudanca, entrar na pasta VPS correta e fazer `git pull --ff-only`.

## Regra de Conversa Entre Projetos

O Hermes Geral pode saber e desenvolver o Hermes Pastoral.

O Hermes Pastoral nao deve consultar automaticamente a memoria privada do Hermes Geral.

Quando os dois precisarem conversar, usar a rede Docker interna:

```text
hermes-geral-api:5060
hermes-pastoral-api:5050
```

Essa comunicacao deve ser feita por endpoints internos e tokens, nao por banco compartilhado.
