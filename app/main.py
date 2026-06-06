from __future__ import annotations

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from .config import is_owner_phone, normalize_phone, owner_phones
from .db import save_message
from .llm import generate_response


def _field(payload: dict, *names: str) -> str:
    campos = payload.get("campos") if isinstance(payload.get("campos"), dict) else {}
    for name in names:
        value = payload.get(name)
        if value not in (None, ""):
            return str(value)
        value = campos.get(name)
        if value not in (None, ""):
            return str(value)
    return ""


def extract_phone(payload: dict) -> str:
    return normalize_phone(_field(payload, "telefone", "phone", "whatsapp", "from", "subscriber_phone"))


def extract_message(payload: dict) -> str:
    return _field(payload, "mensagem", "message", "texto", "text", "resumo", "resumo_ia")


async def health(_: Request) -> JSONResponse:
    return JSONResponse({
        "status": "ok",
        "service": "hermes-geral",
        "owner_phones_configured": sorted(owner_phones()),
    })


async def botconversa_webhook(request: Request) -> JSONResponse:
    payload = await request.json()
    telefone = extract_phone(payload)
    nome = _field(payload, "nome", "name") or "Hanie"
    mensagem = extract_message(payload)

    if not is_owner_phone(telefone):
        return JSONResponse({
            "status": "ignored",
            "reason": "numero_nao_autorizado",
            "telefone": telefone,
        }, status_code=200)

    if not mensagem:
        resposta = "Recebi seu evento, mas nao encontrei texto de mensagem no payload."
    else:
        resposta = generate_response(mensagem)

    save_message(
        telefone=telefone,
        nome=nome,
        mensagem=mensagem,
        resposta=resposta,
        payload=payload,
    )

    return JSONResponse({
        "status": "ok",
        "service": "hermes-geral",
        "telefone": telefone,
        "resposta": resposta,
    })


app = Starlette(debug=False, routes=[
    Route("/health", health, methods=["GET"]),
    Route("/webhook/botconversa", botconversa_webhook, methods=["POST"]),
])
