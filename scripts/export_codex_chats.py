from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any


SECRET_PATTERNS = [
    (re.compile(r"github_pat_[A-Za-z0-9_]+"), "github_pat_***"),
    (re.compile(r"sk-[A-Za-z0-9_-]{20,}"), "sk-***"),
    (re.compile(r"AIza[0-9A-Za-z_-]{20,}"), "AIza***"),
    (re.compile(r"\b\d{8,12}:[A-Za-z0-9_-]{25,}\b"), "telegram-token-***"),
    (re.compile(r"\bAQ\.[A-Za-z0-9_-]{20,}\b"), "google-token-***"),
]


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")


def scrub(text: str) -> str:
    for pattern, replacement in SECRET_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def load_session_index(home: Path) -> list[dict[str, Any]]:
    index_path = home / "session_index.jsonl"
    if not index_path.exists():
        return []

    rows = []
    for line in index_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def find_session_file(home: Path, session_id: str) -> Path | None:
    sessions_dir = home / "sessions"
    if not sessions_dir.exists():
        return None
    matches = sorted(sessions_dir.rglob(f"*{session_id}.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    return matches[0] if matches else None


def content_to_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if not isinstance(item, dict):
                continue
            if item.get("type") in {"input_text", "output_text", "text"}:
                parts.append(str(item.get("text") or ""))
        return "\n".join(part for part in parts if part)
    return ""


def parse_session(path: Path) -> tuple[dict[str, Any], list[tuple[str, str]]]:
    meta: dict[str, Any] = {}
    messages: list[tuple[str, str]] = []
    last: tuple[str, str] | None = None

    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        event_type = event.get("type")
        payload = event.get("payload") or {}

        if event_type == "session_meta":
            meta.update(payload)
            continue

        role = ""
        text = ""
        if event_type == "event_msg" and payload.get("type") == "user_message":
            role = "user"
            text = str(payload.get("message") or "")
        elif event_type == "response_item" and payload.get("type") == "message":
            role = str(payload.get("role") or "")
            text = content_to_text(payload.get("content"))

        text = scrub(text.strip())
        if not role or not text:
            continue

        current = (role, text)
        if current != last:
            messages.append(current)
            last = current

    return meta, messages


def safe_slug(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9_-]+", "-", value)
    return value.strip("-")[:80] or "codex-thread"


def write_session(output_dir: Path, row: dict[str, Any], home: Path) -> dict[str, Any] | None:
    session_id = row.get("id")
    if not session_id:
        return None

    path = find_session_file(home, str(session_id))
    if not path:
        return None

    meta, messages = parse_session(path)
    thread_name = scrub(str(row.get("thread_name") or meta.get("thread_name") or session_id))
    updated_at = str(row.get("updated_at") or meta.get("timestamp") or "")
    cwd = scrub(str(meta.get("cwd") or ""))
    slug = safe_slug(f"{updated_at[:10]}-{thread_name}-{session_id[-6:]}")
    out_path = output_dir / f"{slug}.md"

    lines = [
        f"# {thread_name}",
        "",
        f"- Session ID: `{session_id}`",
        f"- Atualizado em: `{updated_at}`",
        f"- Workspace: `{cwd}`" if cwd else "- Workspace: n/d",
        f"- Arquivo local Codex: `{path}`",
        "",
        "## Conversa",
        "",
    ]
    for role, text in messages:
        label = "Usuario" if role == "user" else "Codex" if role == "assistant" else role
        lines.extend([f"### {label}", "", text, ""])

    out_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    return {
        "title": thread_name,
        "session_id": session_id,
        "updated_at": updated_at,
        "file": out_path.name,
        "messages": len(messages),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Exporta chats locais do Codex para Markdown.")
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--output", default="conhecimento/codex_chats")
    args = parser.parse_args()

    home = codex_home()
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    rows = load_session_index(home)
    rows.sort(key=lambda row: str(row.get("updated_at") or ""), reverse=True)
    selected = rows[: args.limit]

    exported = []
    for row in selected:
        item = write_session(output_dir, row, home)
        if item:
            exported.append(item)

    index_lines = [
        "# Codex Chats Exportados",
        "",
        f"Gerado em: `{datetime.now().isoformat(timespec='seconds')}`",
        f"Origem: `{home}`",
        "",
        "Estes arquivos sao exportacoes sanitizadas dos chats locais do Codex para consulta pelo Hermes Geral.",
        "",
        "## Sessoes",
        "",
    ]
    for item in exported:
        index_lines.append(f"- [{item['title']}]({item['file']}) - `{item['updated_at']}` - {item['messages']} mensagens")

    (output_dir / "index.md").write_text("\n".join(index_lines).strip() + "\n", encoding="utf-8")
    print(f"Exportadas {len(exported)} sessoes para {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
