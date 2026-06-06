from __future__ import annotations

import json
import logging
import time
import urllib.parse
import urllib.request
from typing import Any

from .config import env, is_allowed_telegram_chat
from .db import save_message
from .llm import generate_response


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("hermes-geral-telegram")


def telegram_token() -> str:
    return env("TELEGRAM_BOT_TOKEN")


def api_url(method: str) -> str:
    token = telegram_token()
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN nao configurado.")
    return f"https://api.telegram.org/bot{token}/{method}"


def telegram_request(method: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(api_url(method), data=data, headers=headers, method="POST" if payload else "GET")
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def send_message(chat_id: int | str, text: str) -> None:
    telegram_request("sendMessage", {
        "chat_id": chat_id,
        "text": text[:3900],
    })


def get_updates(offset: int | None) -> list[dict[str, Any]]:
    params = {"timeout": 50}
    if offset is not None:
        params["offset"] = offset
    query = urllib.parse.urlencode(params)
    result = telegram_request(f"getUpdates?{query}")
    return result.get("result", [])


def handle_update(update: dict[str, Any]) -> None:
    message = update.get("message") or update.get("edited_message") or {}
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    text = message.get("text") or ""
    user = message.get("from") or {}
    nome = " ".join(part for part in [user.get("first_name"), user.get("last_name")] if part) or user.get("username") or "Telegram"

    if not chat_id or not text:
        return

    if not is_allowed_telegram_chat(chat_id):
        logger.warning("Chat Telegram nao autorizado: %s", chat_id)
        send_message(chat_id, "Este bot esta restrito ao Hermes Geral autorizado.")
        return

    if text.strip().lower() in {"/start", "start"}:
        resposta = (
            "Hermes Geral Desenvolvedor online. "
            f"Seu chat_id e {chat_id}. Use esse ID em TELEGRAM_ALLOWED_CHAT_IDS para restringir o acesso."
        )
    else:
        resposta = generate_response(text)

    save_message(
        telefone=f"telegram:{chat_id}",
        nome=nome,
        mensagem=text,
        resposta=resposta,
        payload=update,
    )
    send_message(chat_id, resposta)


def run_polling() -> None:
    if not telegram_token():
        raise RuntimeError("TELEGRAM_BOT_TOKEN nao configurado.")

    logger.info("Hermes Geral Telegram iniciado.")
    offset: int | None = None
    while True:
        try:
            for update in get_updates(offset):
                offset = int(update["update_id"]) + 1
                handle_update(update)
        except Exception as exc:
            logger.exception("Erro no polling Telegram: %s", exc)
            time.sleep(5)


if __name__ == "__main__":
    run_polling()
