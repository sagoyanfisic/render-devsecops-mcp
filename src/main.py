from fastapi import FastAPI

app = FastAPI(title="Render DevSecOps API")

@app.get("/")
def root():
    return {"status": "ok", "message": "API running"}

@app.get("/health")
def health():
    return {"healthy": True}
