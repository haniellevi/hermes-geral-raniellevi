from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .config import PROJECT_ROOT, env


def db_path() -> Path:
    raw = env("HERMES_GERAL_DB_PATH", "database/hermes_geral.db")
    path = Path(raw)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(db_path())
    conn.row_factory = sqlite3.Row
    ensure_schema(conn)
    return conn


def ensure_schema(conn: sqlite3.Connection) -> None:
    conn.execute("""
    CREATE TABLE IF NOT EXISTS mensagens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        provider TEXT NOT NULL DEFAULT 'botconversa',
        external_id TEXT,
        telefone TEXT NOT NULL,
        nome TEXT,
        mensagem TEXT NOT NULL,
        resposta TEXT,
        payload TEXT NOT NULL DEFAULT '{}',
        criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS tarefas_dev (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        origem TEXT NOT NULL DEFAULT 'whatsapp',
        titulo TEXT NOT NULL,
        descricao TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Pendente',
        prioridade TEXT NOT NULL DEFAULT 'Normal',
        payload TEXT NOT NULL DEFAULT '{}',
        criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        atualizado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()


def save_message(*, telefone: str, nome: str, mensagem: str, resposta: str, payload: dict[str, Any]) -> None:
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO mensagens (external_id, telefone, nome, mensagem, resposta, payload)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                str(payload.get("event_id") or payload.get("message_id") or ""),
                telefone,
                nome,
                mensagem,
                resposta,
                json.dumps(payload, ensure_ascii=False, sort_keys=True),
            ),
        )
        conn.commit()


def recent_messages(limit: int = 8) -> list[dict[str, Any]]:
    with connect() as conn:
        rows = conn.execute(
            "SELECT nome, mensagem, resposta, criado_em FROM mensagens ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(row) for row in reversed(rows)]
