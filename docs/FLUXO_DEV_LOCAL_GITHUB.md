# Fluxo de Desenvolvimento Local + GitHub

## Regra

O desenvolvimento principal acontece na maquina local. GitHub e a fonte de sincronizacao entre PC, VPS e qualquer ambiente online.

```text
PC local -> desenvolve -> commit -> push GitHub
VPS/nuvem -> pull GitHub -> executa/deploy
```

## Antes de qualquer desenvolvimento

Primeiro identificar o projeto alvo no registro:

```text
conhecimento/projetos_desenvolvimento.md
```

Rodar no repositorio do projeto:

```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\hanie\OneDrive\Documentos\WORKSPACE\Projetos Locais\HERMES-GERAL\scripts\check_git_freshness.ps1 -Path "CAMINHO_DO_PROJETO"
```

Interpretacao:

- `status=sincronizado`: pode trabalhar.
- `status=remoto_na_frente`: rodar `git pull --ff-only` antes de editar.
- `status=local_na_frente`: ha commits locais nao enviados; fazer `git push` ou decidir antes.
- `status=divergente`: parar; nao editar ate decidir merge/rebase.
- `working_tree` com arquivos modificados: entender se sao mudancas suas ou do usuario antes de mexer.

## Depois de desenvolver

1. Rodar testes/validacoes.
2. Revisar `git diff`.
3. Commitar.
4. Fazer push.
5. Se houver deploy na VPS, entrar na VPS e fazer `git pull --ff-only`.

## Regra para Hermes

Sempre que o usuario iniciar desenvolvimento, o Hermes deve:

1. Confirmar o repositorio/pasta.
2. Checar GitHub vs local.
3. Evitar sobrescrever alteracoes locais.
4. Trabalhar localmente.
5. Salvar no GitHub ao final.

## Projetos conhecidos

```powershell
powershell -ExecutionPolicy Bypass -File scripts\list_projects.ps1
```
