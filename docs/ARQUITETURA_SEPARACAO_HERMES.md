# Arquitetura de Separacao dos Hermes

## Ambientes

### Hermes Geral

Finalidade: desenvolvimento de projetos, tecnologia, programacao, automacoes e suporte tecnico pessoal.

Fonte de verdade:

- `HERMES-GERAL/AGENTS.md`
- `HERMES-GERAL/conhecimento/`
- `HERMES-GERAL/tasks/`

### Hermes Pastoral

Finalidade: gestao pastoral da Igreja Filadelfia, atendimento, agenda, G12, consolidacao, comunicacao e produtividade pastoral.

Fonte de verdade:

- `HERMES-LOCAL/AGENTS.md`
- `HERMES-LOCAL/conhecimento/`
- banco pastoral local ou Supabase pastoral
- webhooks pastorais

## Regra de Fluxo

Permitido:

```text
Hermes Geral -> consulta/desenvolve/audita -> Hermes Pastoral
```

Bloqueado por padrao:

```text
Hermes Pastoral -> consulta -> Hermes Geral
Hermes Pastoral -> grava -> banco/tarefas/conhecimento do Hermes Geral
Hermes Geral -> grava memoria privada -> Hermes Pastoral
```

## Integracao Segura

Quando o Hermes Geral precisar alterar o Hermes Pastoral:

1. Criar tarefa tecnica.
2. Definir arquivos ou sistemas afetados.
3. Implementar no repositorio pastoral.
4. Testar.
5. Registrar resultado.

Nao usar o banco pastoral para tarefas gerais de desenvolvimento.
