from __future__ import annotations

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = PROJECT_ROOT / ".env"


def load_env() -> dict[str, str]:
    values: dict[str, str] = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip()
    return values


ENV = load_env()


def env(name: str, default: str = "") -> str:
    return os.environ.get(name) or ENV.get(name) or default


def normalize_phone(value: object) -> str:
    return "".join(ch for ch in str(value or "") if ch.isdigit())


def owner_phones() -> set[str]:
    raw = env("HERMES_GERAL_OWNER_PHONES", "89994315927,5589994315927")
    return {normalize_phone(value) for value in raw.split(",") if normalize_phone(value)}


def is_owner_phone(value: object) -> bool:
    phone = normalize_phone(value)
    if not phone:
        return False
    allowed = owner_phones()
    return phone in allowed or any(phone.endswith(allowed_phone) or allowed_phone.endswith(phone) for allowed_phone in allowed)


def telegram_allowed_chat_ids() -> set[str]:
    raw = env("TELEGRAM_ALLOWED_CHAT_IDS", "")
    return {value.strip() for value in raw.split(",") if value.strip()}


def is_allowed_telegram_chat(chat_id: object) -> bool:
    allowed = telegram_allowed_chat_ids()
    if not allowed:
        return True
    return str(chat_id) in allowed
