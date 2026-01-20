from fastapi import FastAPI, Query
import logging

app = FastAPI(title="Render DevSecOps API")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
def root():
    return {"status": "ok", "message": "API running"}

@app.get("/health")
def health():
    return {"healthy": True}

@app.get("/search")
def search(q: str = Query(default="")):
    """Ruta que loguea el query. El agente MCP detecta XSS/SQLi en los logs."""
    logger.info(f"SEARCH_QUERY: {q}")
    return {"query": q, "results": []}
