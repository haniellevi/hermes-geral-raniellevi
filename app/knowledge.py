from __future__ import annotations

from .config import PROJECT_ROOT


KNOWLEDGE_DIR = PROJECT_ROOT / "conhecimento"
AGENTS_PATH = PROJECT_ROOT / "AGENTS.md"


def read_knowledge() -> str:
    parts: list[str] = []

    if AGENTS_PATH.exists():
        parts.append("# AGENTS.md\n\n" + AGENTS_PATH.read_text(encoding="utf-8"))

    if KNOWLEDGE_DIR.exists():
        for path in sorted(KNOWLEDGE_DIR.rglob("*.md")):
            if any(part.startswith(".") for part in path.relative_to(KNOWLEDGE_DIR).parts):
                continue
            rel = path.relative_to(PROJECT_ROOT)
            parts.append(f"# {rel}\n\n{path.read_text(encoding='utf-8')}")

    return "\n\n---\n\n".join(parts)
