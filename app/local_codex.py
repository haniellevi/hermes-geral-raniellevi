from __future__ import annotations

import subprocess
import shutil
import os
from dataclasses import dataclass

from .config import env


PROJECTS = {
    "hermes-geral": r"C:\Users\hanie\OneDrive\Documentos\WORKSPACE\Projetos Locais\HERMES-GERAL",
    "geral": r"C:\Users\hanie\OneDrive\Documentos\WORKSPACE\Projetos Locais\HERMES-GERAL",
    "desenvolvedor": r"C:\Users\hanie\OneDrive\Documentos\WORKSPACE\Projetos Locais\HERMES-GERAL",
    "hermes-pastoral": r"C:\Users\hanie\OneDrive\Documentos\WORKSPACE\Projetos Locais\Gestao Pastoral - Pr Raniel Levi\HERMES-LOCAL",
    "pastoral": r"C:\Users\hanie\OneDrive\Documentos\WORKSPACE\Projetos Locais\Gestao Pastoral - Pr Raniel Levi\HERMES-LOCAL",
    "gestao-pastoral": r"C:\Users\hanie\OneDrive\Documentos\WORKSPACE\Projetos Locais\Gestao Pastoral - Pr Raniel Levi\HERMES-LOCAL",
}


@dataclass(frozen=True)
class CodexRequest:
    project: str
    workdir: str
    prompt: str


def local_codex_enabled() -> bool:
    return env("HERMES_CODEX_LOCAL_ENABLED", "0").lower() in {"1", "true", "sim", "yes"}


def parse_codex_request(text: str) -> CodexRequest | None:
    raw = text.strip()
    if not raw.lower().startswith("/codex"):
        return None

    body = raw[len("/codex"):].strip()
    if "|" not in body:
        raise ValueError("Use: /codex <projeto> | <pedido>")

    project_raw, prompt = body.split("|", 1)
    project = project_raw.strip().lower().replace("_", "-")
    prompt = prompt.strip()
    workdir = PROJECTS.get(project)

    if not workdir:
        raise ValueError("Projeto nao autorizado. Use: hermes-geral ou hermes-pastoral.")
    if not prompt:
        raise ValueError("Informe o pedido depois de `|`.")

    return CodexRequest(project=project, workdir=workdir, prompt=prompt)


def codex_command() -> str:
    configured = env("HERMES_CODEX_COMMAND", "")
    if configured:
        return configured
    desktop_cli = env("CODEX_CLI_PATH", "")
    if desktop_cli:
        return desktop_cli
    if os.name == "nt":
        desktop_default = r"C:\Users\hanie\AppData\Local\OpenAI\Codex\bin\716dda49c14d31a0\codex.exe"
        if os.path.exists(desktop_default):
            return desktop_default
        return shutil.which("codex.cmd") or shutil.which("codex.exe") or "codex.cmd"
    return shutil.which("codex") or "codex"


def codex_model() -> str:
    return env("HERMES_CODEX_MODEL", "")


def run_codex(request: CodexRequest) -> str:
    if not local_codex_enabled():
        return (
            "Codex local esta desativado neste ambiente. "
            "No PC, rode o Hermes com HERMES_CODEX_LOCAL_ENABLED=1."
        )

    timeout = int(env("HERMES_CODEX_TIMEOUT_SECONDS", "3600"))
    command = [
        codex_command(),
        "exec",
        "-c",
        "model_reasoning_effort=high",
        "-C",
        request.workdir,
        "--full-auto",
        request.prompt,
    ]
    model = codex_model()
    if model:
        command[4:4] = ["-m", model]
    completed = subprocess.run(
        command,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    output = "\n".join(part for part in [completed.stdout.strip(), completed.stderr.strip()] if part)
    if not output:
        output = f"Codex finalizou sem saida. Codigo: {completed.returncode}"
    return output[-3500:]
