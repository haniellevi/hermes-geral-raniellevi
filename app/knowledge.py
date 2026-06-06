from __future__ import annotations

import re
from pathlib import Path

from .config import PROJECT_ROOT


KNOWLEDGE_DIR = PROJECT_ROOT / "conhecimento"
AGENTS_PATH = PROJECT_ROOT / "AGENTS.md"
CODEX_CHATS_DIR = KNOWLEDGE_DIR / "codex_chats"


def _tokens(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-zA-Z0-9_À-ÿ-]{3,}", text.lower()) if token}


def _read_limited(path: Path, limit: int = 16000) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text) <= limit:
        return text
    return text[:limit] + "\n\n[conteudo truncado para caber no contexto]\n"


def _codex_chat_files(query: str, max_files: int = 3) -> list[Path]:
    if not CODEX_CHATS_DIR.exists():
        return []

    index = CODEX_CHATS_DIR / "index.md"
    query_tokens = _tokens(query)
    files = [path for path in CODEX_CHATS_DIR.glob("*.md") if path.name != "index.md"]

    if not query_tokens:
        return [index] if index.exists() else []

    scored: list[tuple[int, float, Path]] = []
    for path in files:
        haystack = _tokens(path.stem.replace("-", " "))
        try:
            haystack |= _tokens(path.read_text(encoding="utf-8", errors="replace")[:4000])
        except OSError:
            pass
        score = len(query_tokens & haystack)
        if score:
            scored.append((score, path.stat().st_mtime, path))

    result = [index] if index.exists() else []
    result.extend(path for _, _, path in sorted(scored, reverse=True)[:max_files])
    return result


def read_knowledge(query: str = "") -> str:
    parts: list[str] = []

    if AGENTS_PATH.exists():
        parts.append("# AGENTS.md\n\n" + AGENTS_PATH.read_text(encoding="utf-8"))

    if KNOWLEDGE_DIR.exists():
        for path in sorted(KNOWLEDGE_DIR.rglob("*.md")):
            if CODEX_CHATS_DIR in path.parents:
                continue
            if any(part.startswith(".") for part in path.relative_to(KNOWLEDGE_DIR).parts):
                continue
            rel = path.relative_to(PROJECT_ROOT)
            parts.append(f"# {rel}\n\n{path.read_text(encoding='utf-8')}")

    for path in _codex_chat_files(query):
        rel = path.relative_to(PROJECT_ROOT)
        parts.append(f"# {rel}\n\n{_read_limited(path)}")

    return "\n\n---\n\n".join(parts)
