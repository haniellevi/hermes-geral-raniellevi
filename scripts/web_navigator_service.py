"""
web_navigator_service.py
Serviço HTTP Flask para o Hermes Geral navegar na web.

Endpoints:
  GET /health             - Status do serviço
  GET /fetch_url?url=...  - Baixa e extrai texto de uma URL
  GET /search_web?query=& [engine=duckduckgo|serper] - Busca na web

Estratégia de busca (sem custo por padrão):
  - Motor primário:  DuckDuckGo via biblioteca `ddgs` (100% gratuito, sem chave)
  - Motor fallback:  Serper.dev (requer SERPER_API_KEY, 2.500 req gratuitos)

Variáveis de ambiente:
  SERPER_API_KEY     - (Opcional) Chave do Serper.dev para fallback Google
  SERVICE_PORT       - Porta do serviço (padrão: 5055)
  SERVICE_HOST       - Host do serviço (padrão: 127.0.0.1)
"""

import os
import logging
import time
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

# ── Configuração ──────────────────────────────────────────────────────────────
app = Flask(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)

SERPER_API_KEY = os.getenv("SERPER_API_KEY")  # Opcional – fallback Google
SERVICE_PORT = int(os.getenv("SERVICE_PORT", 5055))
SERVICE_HOST = os.getenv("SERVICE_HOST", "127.0.0.1")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _search_duckduckgo(query: str, max_results: int = 8) -> list[dict]:
    """
    Busca via DuckDuckGo usando a biblioteca `ddgs`.
    Gratuito, sem chave de API, sem limite formal.
    """
    try:
        from duckduckgo_search import DDGS

        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "link":  r.get("href", ""),
                    "snippet": r.get("body", ""),
                    "source": "duckduckgo",
                })
        log.info(f"DuckDuckGo retornou {len(results)} resultados para: {query!r}")
        return results

    except Exception as exc:
        log.error(f"Erro no DuckDuckGo: {exc}")
        return []


def _search_serper(query: str, max_results: int = 8) -> list[dict]:
    """
    Busca via Serper.dev (resultados do Google).
    Requer SERPER_API_KEY. Plano gratuito: 2.500 req sem cartão.
    Preço posterior: ~$0,30/1.000 req (muito barato).
    """
    if not SERPER_API_KEY:
        log.warning("SERPER_API_KEY não definida – motor Serper indisponível.")
        return []

    try:
        resp = requests.post(
            "https://google.serper.dev/search",
            headers={
                "X-API-KEY": SERPER_API_KEY,
                "Content-Type": "application/json",
            },
            json={"q": query, "num": max_results},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        results = []
        for item in data.get("organic", []):
            results.append({
                "title":   item.get("title", ""),
                "link":    item.get("link", ""),
                "snippet": item.get("snippet", ""),
                "source":  "serper/google",
            })
        log.info(f"Serper.dev retornou {len(results)} resultados para: {query!r}")
        return results

    except Exception as exc:
        log.error(f"Erro no Serper.dev: {exc}")
        return []


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "web_navigator",
        "engines": {
            "duckduckgo": "ativo (gratuito)",
            "serper": "ativo" if SERPER_API_KEY else "inativo (sem SERPER_API_KEY)",
        }
    })


@app.route("/fetch_url")
def fetch_url():
    url = request.args.get("url", "").strip()
    if not url:
        return jsonify({"error": "Parâmetro 'url' é obrigatório."}), 400

    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        # Remove scripts, estilos e elementos de navegação
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)

        # Limita o tamanho para não sobrecarregar o contexto do Hermes
        MAX_CHARS = 8_000
        truncated = len(text) > MAX_CHARS
        text = text[:MAX_CHARS]

        log.info(f"fetch_url: {url} — {len(text)} chars (truncado={truncated})")
        return jsonify({
            "url": url,
            "content": text,
            "truncated": truncated,
            "chars": len(text),
        })

    except requests.exceptions.RequestException as exc:
        log.error(f"fetch_url erro em {url}: {exc}")
        return jsonify({"error": str(exc)}), 502


@app.route("/search_web")
def search_web():
    """
    Busca na web com seleção inteligente de motor.

    Query params:
      query    (str) - Termo de busca (obrigatório)
      engine   (str) - 'duckduckgo' (padrão) | 'serper' | 'auto'
      max      (int) - Número máximo de resultados (padrão: 8)
    """
    query = request.args.get("query", "").strip()
    engine = request.args.get("engine", "duckduckgo").lower()
    max_results = min(int(request.args.get("max", 8)), 20)

    if not query:
        return jsonify({"error": "Parâmetro 'query' é obrigatório."}), 400

    results = []
    used_engine = engine

    if engine in ("duckduckgo", "auto"):
        results = _search_duckduckgo(query, max_results)
        used_engine = "duckduckgo"
        # Fallback automático para Serper se DDG falhar e chave disponível
        if not results and engine == "auto" and SERPER_API_KEY:
            log.info("DDG sem resultados → fallback para Serper.dev")
            results = _search_serper(query, max_results)
            used_engine = "serper"

    elif engine == "serper":
        results = _search_serper(query, max_results)
        used_engine = "serper"

    return jsonify({
        "query": query,
        "engine_used": used_engine,
        "count": len(results),
        "results": results,
    })


# ── Inicialização ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    log.info(f"Iniciando web_navigator na porta {SERVICE_PORT}...")
    log.info(f"DuckDuckGo: ativo (gratuito)")
    log.info(f"Serper.dev: {'ativo' if SERPER_API_KEY else 'inativo (sem SERPER_API_KEY)'}")
    app.run(host=SERVICE_HOST, port=SERVICE_PORT, debug=False)
