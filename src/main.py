from fastapi import FastAPI, Query
import logging

app = FastAPI(title="Render DevSecOps API")

# Configurar logging para que aparezca en los logs de Render
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
    """
    Ruta de prueba para detectar XSS/SQLi en logs.
    Ejemplo: /search?q=<script>alert('xss')</script>
    Ejemplo: /search?q=' OR 1=1 --
    """
    # Log del query para que aparezca en los logs de Render
    logger.info(f"SEARCH_QUERY: {q}")

    # Detectar patrones sospechosos
    xss_patterns = ["<script", "javascript:", "onerror=", "onload=", "<img", "<svg"]
    sqli_patterns = ["' OR", "1=1", "--", "DROP TABLE", "UNION SELECT", "'; DELETE"]

    detected = []
    q_lower = q.lower()

    for pattern in xss_patterns:
        if pattern.lower() in q_lower:
            detected.append(f"XSS_DETECTED: {pattern}")
            logger.warning(f"XSS_DETECTED: pattern={pattern} query={q}")

    for pattern in sqli_patterns:
        if pattern.lower() in q_lower:
            detected.append(f"SQLI_DETECTED: {pattern}")
            logger.warning(f"SQLI_DETECTED: pattern={pattern} query={q}")

    if detected:
        logger.critical(f"SECURITY_ALERT: {detected} in query: {q}")
        return {"warning": "Suspicious input detected", "detections": detected}

    return {"query": q, "results": []}
