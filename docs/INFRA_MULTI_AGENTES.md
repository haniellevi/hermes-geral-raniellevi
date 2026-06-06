# Infraestrutura Multiagentes Hermes

## Principio

Cada Hermes deve ser um sistema separado:

- repositorio separado;
- `.env` separado;
- banco separado;
- volumes separados;
- containers separados;
- portas internas separadas;
- conhecimento separado.

O compartilhamento entre agentes deve acontecer por uma camada explicita de comunicacao, nao por banco compartilhado nem por arquivos misturados.

## Configuracao recomendada na VPS

```text
/opt/hermes-geral
/opt/gestor-pastoral-agente-hermes/HERMES-LOCAL
/opt/hermes-edge              # recomendado para o proxy publico no futuro
```

## Containers atuais

Hermes Pastoral:

```text
hermes-api                    # API/webhooks pastorais, porta interna 5050
hermes-dashboard              # painel pastoral, porta interna 8501
hermes-drive-sync             # sincronizacao pastoral
hermes-caddy                  # proxy publico atual do pastoral
```

Hermes Geral:

```text
hermes-geral-api              # API privada do Hermes Geral, porta interna 5060
hermes-geral-telegram         # worker Telegram Desenvolvedor
```

## Rede compartilhada para comunicacao entre agentes

Criar uma rede Docker externa:

```bash
docker network create hermes-agents
```

Aliases recomendados:

```text
hermes-pastoral-api      -> hermes-api:5050
hermes-pastoral-dashboard -> hermes-dashboard:8501
hermes-geral-api         -> hermes-geral-api:5060
hermes-geral-telegram    -> hermes-geral-telegram
```

Assim, quando os agentes precisarem conversar:

```text
Hermes Geral -> http://hermes-pastoral-api:5050
Hermes Pastoral -> http://hermes-geral-api:5060
```

Essa conversa deve ser mediada por endpoints especificos e tokens internos. Nao usar acesso direto ao banco do outro agente.

## Proxy publico

Hoje o Caddy esta dentro do compose pastoral. Funciona, mas nao e a arquitetura ideal para varios agentes.

Configuracao recomendada:

```text
/opt/hermes-edge/docker-compose.yml
/opt/hermes-edge/Caddyfile
```

O edge proxy deve ser o unico container usando portas `80` e `443`.

Exemplo de rotas:

```caddyfile
api.filadelfiacorrente.com {
    reverse_proxy hermes-pastoral-api:5050
}

painel.filadelfiacorrente.com {
    reverse_proxy hermes-pastoral-dashboard:8501
}

dev-api.filadelfiacorrente.com {
    reverse_proxy hermes-geral-api:5060
}
```

Para Telegram do Hermes Geral, nao precisa rota publica porque o worker usa polling.

## Conversa futura entre agentes

Quando o Hermes Geral e o Hermes Pastoral precisarem conversar, criar endpoints dedicados:

```text
POST /internal/messages
POST /internal/tasks
GET /internal/health
```

Regras:

- autenticar com `HERMES_INTERNAL_TOKEN`;
- registrar auditoria;
- nao expor dados pessoais sem necessidade;
- Hermes Geral pode consultar contexto pastoral quando autorizado;
- Hermes Pastoral nao consulta memoria privada do Hermes Geral por padrao.

## Comando operacional

Para reconectar os containers existentes na rede compartilhada:

```bash
cd /opt/hermes-geral
bash deploy/connect_existing_agents.sh
```
