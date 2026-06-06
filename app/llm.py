from __future__ import annotations

import json
import urllib.error
import urllib.request

from .config import env
from .db import recent_messages
from .knowledge import read_knowledge


def build_system_prompt() -> str:
    return (
        "Voce e o Hermes Geral, agente principal de desenvolvimento do usuario. "
        "Responda em portugues do Brasil, com tom tecnico, direto e pragmatico. "
        "Nao misture dados do Hermes Geral com o Hermes Pastoral. "
        "Use o conhecimento abaixo como fonte de verdade.\n\n"
        f"{read_knowledge()}"
    )


def offline_response(_: str) -> str:
    return (
        "Hermes Geral recebeu sua mensagem e registrou no banco proprio. "
        "O LLM ainda nao esta configurado na VPS. Configure OPENAI_API_KEY no .env do HERMES-GERAL "
        "para eu responder com todo o conhecimento sincronizado."
    )


def generate_response(message: str) -> str:
    api_key = env("OPENAI_API_KEY")
    if not api_key:
        return offline_response(message)

    model = env("OPENAI_MODEL", "gpt-4.1-mini")
    url = env("OPENAI_BASE_URL", "https://api.openai.com/v1/chat/completions")

    history = []
    for item in recent_messages():
        history.append({"role": "user", "content": item["mensagem"]})
        if item.get("resposta"):
            history.append({"role": "assistant", "content": item["resposta"]})

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": build_system_prompt()},
            *history,
            {"role": "user", "content": message},
        ],
        "temperature": 0.2,
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = json.loads(response.read().decode("utf-8"))
        return body["choices"][0]["message"]["content"].strip()
    except (urllib.error.URLError, KeyError, IndexError, json.JSONDecodeError) as exc:
        return f"Recebi sua mensagem, mas houve erro ao chamar o modelo: {exc}"
