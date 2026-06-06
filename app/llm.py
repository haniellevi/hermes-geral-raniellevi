from __future__ import annotations

import json
import urllib.error
import urllib.request

from .config import env
from .db import recent_messages
from .knowledge import read_knowledge


def build_system_prompt(message: str = "") -> str:
    return (
        "Voce e o Hermes Geral, agente principal de desenvolvimento do usuario. "
        "Responda em portugues do Brasil, com tom tecnico, direto e pragmatico. "
        "Nao misture dados do Hermes Geral com o Hermes Pastoral. "
        "Use o conhecimento abaixo como fonte de verdade.\n\n"
        f"{read_knowledge(message)}"
    )


def offline_response(_: str) -> str:
    return (
        "Hermes Geral recebeu sua mensagem e registrou no banco proprio. "
        "O LLM ainda nao esta configurado na VPS. Configure GEMINI_API_KEY no .env do HERMES-GERAL "
        "para eu responder com todo o conhecimento sincronizado."
    )


DEV_TERMS = (
    "/dev",
    "desenvolvimento completo",
    "codex",
    "claude code",
    "antigravity",
    "supabase",
    "botconversa",
    "programacao",
    "programação",
    "codigo",
    "código",
    "arquitetura",
    "docker",
    "deploy",
    "vps",
    "webhook",
    "banco de dados",
    "debug",
)


def is_development_request(message: str) -> bool:
    text = message.lower()
    return any(term in text for term in DEV_TERMS)


def selected_gemini_model(message: str) -> str:
    if is_development_request(message):
        return env("HERMES_GERAL_DEV_MODEL", "gemini-2.5-pro")
    return env("HERMES_GERAL_COMMON_MODEL", "gemini-2.5-flash")


def gemini_response(message: str, api_key: str) -> str:
    model = selected_gemini_model(message)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    history = []
    for item in recent_messages():
        history.append({
            "role": "user",
            "parts": [{"text": item["mensagem"]}],
        })
        if item.get("resposta"):
            history.append({
                "role": "model",
                "parts": [{"text": item["resposta"]}],
            })

    payload = {
        "systemInstruction": {
            "parts": [{"text": build_system_prompt(message)}],
        },
        "contents": [
            *history,
            {
                "role": "user",
                "parts": [{"text": message}],
            },
        ],
        "generationConfig": {
            "temperature": 0.2,
        },
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=90) as response:
        body = json.loads(response.read().decode("utf-8"))

    parts = body["candidates"][0]["content"]["parts"]
    return "".join(part.get("text", "") for part in parts).strip()


def openai_compatible_response(message: str, api_key: str) -> str:
    api_key = env("OPENAI_API_KEY") or env("OPENROUTER_API_KEY")
    using_openrouter = bool(env("OPENROUTER_API_KEY")) and not env("OPENAI_API_KEY")
    model = env("OPENAI_MODEL", "openai/gpt-4.1-mini" if using_openrouter else "gpt-4.1-mini")
    base_url = env("OPENAI_BASE_URL")
    if using_openrouter and (not base_url or "api.openai.com" in base_url):
        base_url = "https://openrouter.ai/api/v1/chat/completions"
    url = base_url or ("https://openrouter.ai/api/v1/chat/completions" if using_openrouter else "https://api.openai.com/v1/chat/completions")
    if not url.rstrip("/").endswith("/chat/completions"):
        url = url.rstrip("/") + "/chat/completions"

    history = []
    for item in recent_messages():
        history.append({"role": "user", "content": item["mensagem"]})
        if item.get("resposta"):
            history.append({"role": "assistant", "content": item["resposta"]})

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": build_system_prompt(message)},
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
            "HTTP-Referer": "https://github.com/haniellevi/hermes-geral-raniellevi",
            "X-Title": "Hermes Geral Raniel Levi",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = json.loads(response.read().decode("utf-8"))
        return body["choices"][0]["message"]["content"].strip()
    except (urllib.error.URLError, KeyError, IndexError, json.JSONDecodeError) as exc:
        return f"Recebi sua mensagem, mas houve erro ao chamar o modelo: {exc}"


def generate_response(message: str) -> str:
    gemini_key = env("GEMINI_API_KEY") or env("GOOGLE_API_KEY")
    if gemini_key:
        try:
            return gemini_response(message, gemini_key)
        except (urllib.error.URLError, KeyError, IndexError, json.JSONDecodeError) as exc:
            return f"Recebi sua mensagem, mas houve erro ao chamar Gemini: {exc}"

    openai_key = env("OPENAI_API_KEY") or env("OPENROUTER_API_KEY")
    if openai_key:
        return openai_compatible_response(message, openai_key)

    return offline_response(message)
